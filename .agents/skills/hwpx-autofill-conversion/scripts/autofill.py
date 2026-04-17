#!/usr/bin/env python3
"""Autofill an HWPX template with new content.

Two modes are supported, chosen automatically from the shape of
`content.json`:

- **slot mode** (safest) — the JSON is a list of text strings mapped
  positionally to the template's existing text-bearing paragraphs. The
  output keeps every paragraph, table, style, and image exactly where
  the template had them; only the text inside `<hp:t>` nodes is
  rewritten. Use this when the template's outline already matches what
  you want to produce (common case: "fill in this report form").

- **blocks mode** (more flexible) — the JSON is a list of semantic
  blocks (`{"level": "h1", "text": "..."}`). The script rebuilds the
  body of the section by cloning the template's paragraph archetypes
  (h1/h2/h3/body) with new text. The section-properties paragraph (the
  one carrying `<hp:secPr>`) is always preserved and is used to hold
  the document title, so the page size / margins / headers are kept.
  Tables from the template are appended as-is at the positions the
  JSON marks with `{"type": "keep_table", "template_index": N}` — this
  is the only supported way to emit a table for now; regenerating
  tables from scratch is not reliable enough.

The orchestrator only needs the template path, a content.json, and an
output path. It does all the archive surgery in one pass.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from _hwpx_common import (  # noqa: E402
    TEXT_RE,
    parse_section,
    read_hwpx_members,
    replace_text_runs,
    write_hwpx,
)
from inspect_template import inspect  # noqa: E402


def _xml_escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------------------------------------------------------------------------
# Mode detection
# ---------------------------------------------------------------------------


def detect_mode(content: dict | list) -> str:
    """Figure out which mode the content.json is asking for.

    Three modes supported:

    - **slots** — `list[str]` or `{"slots": [...]}` — positional over
      the template's non-empty text nodes (the default, matches what
      `inspect --summary` prints).
    - **blocks** — `list[dict]` or `{"blocks": [...]}` — semantic
      paragraph reconstruction via archetype cloning.
    - **targeted** — `{"targeted": {"<abs_index>": "new text", ...}}` —
      replaces specific text nodes by absolute index, counted across
      ALL `<hp:t>` occurrences including whitespace-only ones. Use this
      when you need to fill empty template cells (e.g., a TOC table
      whose entries are blank placeholders) that positional slot mode
      can't reach. Run `inspect --all` to see absolute indices.

    `targeted` can be combined with `slots` in a single dict — slots
    are applied first (positional, non-empty), then targeted overrides
    specific absolute indices.
    """
    if isinstance(content, list):
        if not content:
            return "slots"
        if all(isinstance(x, str) for x in content):
            return "slots"
        if all(isinstance(x, dict) for x in content):
            return "blocks"
    if isinstance(content, dict):
        if "targeted" in content and "blocks" not in content:
            return "slots_targeted" if "slots" in content else "targeted"
        if "slots" in content:
            return "slots"
        if "blocks" in content:
            return "blocks"
    raise ValueError(
        "Cannot detect content mode — expected list[str] (slot), "
        "list[dict] (blocks), or dict with 'slots'/'blocks'/'targeted'."
    )


# ---------------------------------------------------------------------------
# Slot mode
# ---------------------------------------------------------------------------


def apply_targeted_mode(section_xml: bytes, targeted: dict[str, str]) -> bytes:
    """Replace text nodes by absolute `<hp:t>` index, including empty ones.

    `targeted` maps string index (JSON keys are strings) to the new text
    for that node. Indices count every `<hp:t>...</hp:t>` occurrence in
    document order starting at 0 — including whitespace-only nodes,
    which positional slot mode skips. Use `inspect --all` to see them.

    Why this exists: Korean government templates frequently pre-render
    their 목차 (table of contents) as a grid of empty placeholder cells
    that HWP's TOC generator is supposed to fill. When you repurpose
    such a template via autofill, those cells stay empty and the old
    cached PrvText TOC no longer matches your new chapter titles. This
    mode lets you drop text straight into those cells.
    """
    xml = section_xml.decode("utf-8")
    all_matches = list(TEXT_RE.finditer(xml))

    # Normalise keys: JSON objects always have string keys, convert to int.
    try:
        replacements = {int(k): v for k, v in targeted.items()}
    except ValueError as e:
        raise ValueError(f"targeted keys must be integers: {e}") from e

    for idx in sorted(replacements):
        if idx >= len(all_matches):
            print(
                f"[autofill] warning: targeted index {idx} out of range "
                f"(template has {len(all_matches)} text nodes)",
                file=sys.stderr,
            )

    # Replace from right to left so earlier offsets stay valid.
    out = xml
    for idx in sorted(replacements, reverse=True):
        if idx >= len(all_matches):
            continue
        m = all_matches[idx]
        out = out[:m.start(1)] + _xml_escape(replacements[idx]) + out[m.end(1):]
    return out.encode("utf-8")


def apply_slot_mode(section_xml: bytes, slots: list[str]) -> bytes:
    """Rewrite every `<hp:t>` node in document order.

    We walk the entire section XML (not just top-level paragraphs) and
    collect every `<hp:t>...</hp:t>` match. Slot N replaces the Nth
    non-empty text node. This way the same mechanism fills both regular
    body paragraphs AND text inside table cells — which matters because
    most Korean report templates put their fillable fields inside info
    boxes that are tables. Empty or whitespace-only text nodes are left
    alone so spacers/formatting survive.

    Pros: dead simple, no structural edits, 100% valid output.
    Cons: you have to know the exact slot order, which the inspector
    prints for you. If two slots collide (template only has N but you
    gave N+k) the extras are ignored.
    """
    xml = section_xml.decode("utf-8")

    # Collect the positions of all non-empty <hp:t> runs in document order.
    matches: list[tuple[int, int]] = []
    for m in TEXT_RE.finditer(xml):
        if m.group(1).strip():
            matches.append((m.start(1), m.end(1)))

    if len(slots) > len(matches):
        print(
            f"[autofill] warning: got {len(slots)} slots but template only "
            f"has {len(matches)} text nodes — extras ignored",
            file=sys.stderr,
        )

    # Replace from right to left so earlier offsets stay valid.
    out = xml
    for i in range(min(len(slots), len(matches)) - 1, -1, -1):
        start, end = matches[i]
        out = out[:start] + _xml_escape(slots[i]) + out[end:]
    return out.encode("utf-8")




# ---------------------------------------------------------------------------
# Blocks mode
# ---------------------------------------------------------------------------


def apply_blocks_mode(
    section_xml: bytes,
    blocks: list[dict],
    template_report: dict,
) -> bytes:
    """Rebuild the section body from semantic blocks.

    The first paragraph (which carries `<hp:secPr>`) is preserved but
    its text runs are replaced with the document title — the first
    block of `type: "title"` (falling back to the first heading).

    Subsequent paragraphs are cloned from archetypes keyed by level.
    Tables are re-emitted from the template verbatim when a block
    asks for `keep_table`.
    """
    section = parse_section("section", section_xml)
    archetypes: dict[str, dict] = template_report["archetypes"]

    if not section.paragraphs:
        raise ValueError("template section has no paragraphs")

    # Find the secPr paragraph — conventionally the first.
    secpr_para = next((p for p in section.paragraphs if p.has_secpr), None)
    if secpr_para is None:
        raise ValueError(
            "template section has no <hp:secPr> paragraph — cannot preserve "
            "page layout; please use slot mode on this template instead"
        )

    # Pull the title from the first title/heading block.
    title_text = ""
    for b in blocks:
        t = b.get("type") or b.get("level") or ""
        if t in {"title", "section", "h1"} and b.get("text"):
            title_text = b["text"]
            break
    if not title_text and blocks and blocks[0].get("text"):
        title_text = blocks[0]["text"]

    head_xml = (
        replace_text_runs(secpr_para.xml, title_text)
        if title_text
        else secpr_para.xml
    )

    # Build the body paragraphs by cloning archetypes.
    body_xmls: list[str] = []
    # Build a lookup of table paragraphs by template index for keep_table.
    tables_by_index = {
        p.index: p.xml for p in section.paragraphs if p.kind == "table"
    }

    for b in blocks:
        btype = b.get("type", "")
        level = b.get("level") or _infer_level(btype)
        text = b.get("text", "")

        if btype == "keep_table":
            idx = b.get("template_index")
            if idx is not None and idx in tables_by_index:
                body_xmls.append(tables_by_index[idx])
            else:
                print(
                    f"[autofill] warning: keep_table asked for index {idx} "
                    f"but no such table in template",
                    file=sys.stderr,
                )
            continue

        if btype == "blank":
            # Clone an empty spacer paragraph if available.
            empty = _first_empty_paragraph(section)
            if empty is not None:
                body_xmls.append(empty.xml)
            continue

        archetype = _pick_archetype(archetypes, level)
        if archetype is None:
            print(
                f"[autofill] warning: no archetype for level={level!r}, "
                f"using the first available",
                file=sys.stderr,
            )
            archetype = next(iter(archetypes.values()), None)
        if archetype is None:
            raise ValueError("template has no usable text archetypes")

        body_xmls.append(replace_text_runs(archetype["xml"], text))

    new_paragraphs = [head_xml] + body_xmls
    return section.serialize(new_paragraphs).encode("utf-8")


def _pick_archetype(archetypes: dict[str, dict], level: str) -> dict | None:
    # Try exact match; if missing, fall back through a sensible chain.
    if level in archetypes:
        return archetypes[level]
    fallback_order = {
        "section": ["h1", "h2", "body"],
        "h1": ["section", "h2", "body"],
        "h2": ["h3", "h1", "body"],
        "h3": ["h2", "h4", "body"],
        "h4": ["h3", "body"],
        "body": ["h3", "h2", "h1"],
    }
    for candidate in fallback_order.get(level, []):
        if candidate in archetypes:
            return archetypes[candidate]
    return None


def _first_empty_paragraph(section) -> object | None:
    for p in section.paragraphs:
        if p.kind == "empty":
            return p
    return None


def _infer_level(btype: str) -> str:
    mapping = {
        "title": "section",
        "chapter": "section",
        "heading1": "h1",
        "heading2": "h2",
        "heading3": "h3",
        "paragraph": "body",
        "body": "body",
        "list": "h3",
        "note": "h4",
    }
    return mapping.get(btype, btype or "body")


# ---------------------------------------------------------------------------
# Preview text
# ---------------------------------------------------------------------------


def rewrite_prvtext(original: bytes, new_text: str) -> bytes:
    """Replace `Preview/PrvText.txt` with a short plain-text excerpt.

    This is cosmetic — it's the plaintext HWP uses in file-preview
    panes. We regenerate it so the preview doesn't show the template's
    placeholder text after autofill.
    """
    return new_text.encode("utf-8")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def run(template_path: Path, content_path: Path, out_path: Path) -> int:
    members = read_hwpx_members(template_path)
    content = json.loads(content_path.read_text(encoding="utf-8"))
    mode = detect_mode(content)

    section_names = sorted(
        n for n in members if n.startswith("Contents/section") and n.endswith(".xml")
    )
    if not section_names:
        print("error: template has no Contents/section*.xml", file=sys.stderr)
        return 2

    # For simplicity, autofill only touches the first section. Templates
    # with multiple sections will keep sections 1+ untouched.
    primary = section_names[0]

    # Normalise content → bytes, depending on mode.
    if mode == "slots":
        slots = content if isinstance(content, list) else content.get("slots", [])
        new_section = apply_slot_mode(members[primary], slots)
        preview_text = "\n".join(str(s) for s in slots[:20])
    elif mode == "targeted":
        targeted = content.get("targeted", {}) if isinstance(content, dict) else {}
        new_section = apply_targeted_mode(members[primary], targeted)
        preview_text = "\n".join(str(v) for v in list(targeted.values())[:20])
    elif mode == "slots_targeted":
        # Apply positional slots first, then targeted overrides on top.
        slots = content.get("slots", [])
        targeted = content.get("targeted", {})
        stage1 = apply_slot_mode(members[primary], slots)
        new_section = apply_targeted_mode(stage1, targeted)
        preview_text = "\n".join(str(s) for s in slots[:20])
    else:  # blocks
        blocks = content if isinstance(content, list) else content.get("blocks", [])
        template_report = inspect(template_path)
        new_section = apply_blocks_mode(members[primary], blocks, template_report)
        preview_lines = [b.get("text", "") for b in blocks[:20] if isinstance(b, dict)]
        preview_text = "\n".join(x for x in preview_lines if x)

    members[primary] = new_section
    if "Preview/PrvText.txt" in members:
        members["Preview/PrvText.txt"] = rewrite_prvtext(
            members["Preview/PrvText.txt"], preview_text
        )

    write_hwpx(out_path, members)
    print(f"[autofill] mode={mode}  wrote {out_path}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Autofill HWPX template")
    ap.add_argument("template", type=Path)
    ap.add_argument("content", type=Path, help="content.json (slots or blocks)")
    ap.add_argument("out", type=Path, help="output .hwpx path")
    args = ap.parse_args()

    for p in (args.template, args.content):
        if not p.exists():
            print(f"error: not found: {p}", file=sys.stderr)
            return 2

    try:
        return run(args.template, args.content, args.out)
    except Exception as e:
        print(f"[autofill] FAILED: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
