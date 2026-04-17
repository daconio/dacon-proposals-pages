#!/usr/bin/env python3
"""Summarise an HWPX template as a JSON report Claude can read.

The report answers the three questions Claude needs before it can draft
replacement content:

1. What are the text slots in this template, in document order?
   Each slot is a paragraph index, its inferred outline level (section,
   h1, h2, h3, h4, body), and the sample text that is currently there.

2. Which archetype paragraphs are reusable for rebuilding the section?
   We record the raw XML of one "best exemplar" per level so the builder
   can clone it and substitute text without inventing new paraPr/charPr
   references.

3. What's the table inventory? We list tables with (rows, cols, cell
   text previews) so Claude knows whether the template has tables it
   should fill vs. regenerate.

The report is consumed by `build_section.py` (which needs archetypes +
secPr paragraph) and by the human/Claude (who needs the slot listing).
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
    Paragraph,
    Section,
    classify_paragraphs,
    guess_level,
    parse_section,
    read_hwpx_members,
)


def inspect(hwpx_path: Path) -> dict:
    members = read_hwpx_members(hwpx_path)
    sections: list[dict] = []
    archetypes: dict[str, dict] = {}
    secpr_xml: str | None = None

    for name in sorted(members):
        if not (name.startswith("Contents/section") and name.endswith(".xml")):
            continue
        section = parse_section(name, members[name])

        # Slot listing: walk every <hp:t> in document order (including
        # text inside table cells). This is what `autofill.py` slot
        # mode actually rewrites, so the indices Claude sees here are
        # the ones it should use when assembling content.json.
        #
        # We record both the positional "slot" index (counting only
        # non-empty text nodes — what slot mode uses) and the absolute
        # `abs` index (counting every <hp:t>, including whitespace —
        # what targeted mode uses). The distinction matters for
        # templates that pre-render a blank TOC into empty cells.
        xml = members[name].decode("utf-8")
        slots: list[dict] = []
        all_slots: list[dict] = []  # includes empty/whitespace
        slot_counter = 0
        for abs_idx, m in enumerate(re.finditer(r"<hp:t>([^<]*)</hp:t>", xml)):
            text = m.group(1)
            record = {
                "abs": abs_idx,
                "level": guess_level(text) if text.strip() else "empty",
                "text": text.strip() if text.strip() else "",
                "raw": text,
            }
            all_slots.append(record)
            if text.strip():
                slots.append(
                    {
                        "slot": slot_counter,
                        "abs": abs_idx,
                        "level": guess_level(text),
                        "text": text.strip(),
                    }
                )
                slot_counter += 1

        section_report = {
            "path": name,
            "paragraph_count": len(section.paragraphs),
            "slots": slots,
            "all_slots": all_slots,
            "tables": [],
        }

        for p in section.paragraphs:
            if p.has_secpr and secpr_xml is None:
                secpr_xml = p.xml

            if p.kind == "text":
                level = guess_level(p.text)
                # Record one archetype per level — prefer a clean,
                # non-secPr paragraph with a short, representative text.
                if level not in archetypes and not p.has_secpr:
                    archetypes[level] = {
                        "level": level,
                        "para_pr_id": p.para_pr_id,
                        "style_id": p.style_id,
                        "sample_text": p.text.strip(),
                        "xml": p.xml,
                    }
            elif p.kind == "table":
                section_report["tables"].append(_summarise_table(p))

        sections.append(section_report)

    report = {
        "source": str(hwpx_path),
        "sections": sections,
        "archetypes": archetypes,
        "section_properties_xml": secpr_xml,
        "style_legend": {
            "section": "로마숫자로 시작하는 장 제목 (Ⅰ, Ⅱ, ...)",
            "h1": "□ 로 시작하는 15pt 대제목",
            "h2": "○ 로 시작하는 14pt 중제목",
            "h3": "- 로 시작하는 14pt 소제목",
            "h4": "※ 로 시작하는 11pt 주석",
            "body": "기타 본문 텍스트",
        },
    }
    return report


def _summarise_table(p: Paragraph) -> dict:
    """Produce a compact summary of a table paragraph.

    We pull row/col counts from the first `<hp:tbl>` attributes and the
    first ~20 cell texts. This is enough for Claude to recognise which
    table is which without loading the full XML.
    """
    m = re.search(r'<hp:tbl\b[^>]*rowCnt="(\d+)"[^>]*colCnt="(\d+)"', p.xml)
    rows = int(m.group(1)) if m else 0
    cols = int(m.group(2)) if m else 0
    cells = re.findall(r"<hp:t>([^<]*)</hp:t>", p.xml)
    return {
        "paragraph_index": p.index,
        "rows": rows,
        "cols": cols,
        "cell_preview": [c for c in cells[:20] if c.strip()],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Inspect an HWPX template")
    ap.add_argument("template", type=Path, help="Path to template .hwpx")
    ap.add_argument(
        "--out",
        type=Path,
        help="Write full JSON report here (default: print to stdout)",
    )
    ap.add_argument(
        "--summary",
        action="store_true",
        help="Print a human-readable summary instead of JSON",
    )
    ap.add_argument(
        "--all",
        action="store_true",
        help="Also list empty/whitespace <hp:t> nodes (use with targeted mode)",
    )
    args = ap.parse_args()

    if not args.template.exists():
        print(f"error: template not found: {args.template}", file=sys.stderr)
        return 2

    report = inspect(args.template)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[inspect] wrote {args.out}")

    if args.summary or not args.out:
        _print_summary(report, show_empty=args.all)

    return 0


def _print_summary(report: dict, show_empty: bool = False) -> None:
    print(f"# Template: {report['source']}")
    for section in report["sections"]:
        print(f"\n## {section['path']}  ({section['paragraph_count']} paragraphs)")
        total_all = len(section.get("all_slots", section["slots"]))
        print(
            f"   Text slots (non-empty): {len(section['slots'])}  |  "
            f"Total <hp:t> nodes: {total_all}  |  Tables: {len(section['tables'])}"
        )
        if show_empty:
            print("\n   All text nodes with absolute index (--all):")
            for s in section.get("all_slots", [])[:60]:
                if s["text"]:
                    tag = f"{s['level']:7s}"
                    preview = s["text"][:60].replace("\n", " ")
                else:
                    tag = "empty  "
                    preview = f"<ws len={len(s['raw'])}>"
                print(f"     abs[{s['abs']:3d}] {tag}  {preview}")
            if total_all > 60:
                print(f"     ... ({total_all - 60} more)")
            continue
        print("\n   Slots (first 40):")
        for slot in section["slots"][:40]:
            preview = slot["text"][:60].replace("\n", " ")
            print(f"     [{slot['slot']:3d}] abs={slot['abs']:3d} {slot['level']:7s}  {preview}")
        if len(section["slots"]) > 40:
            print(f"     ... ({len(section['slots']) - 40} more)")
        if section["tables"]:
            print("\n   Tables:")
            for t in section["tables"]:
                cells = ", ".join(c[:12] for c in t["cell_preview"][:8])
                print(f"     para {t['paragraph_index']:3d}: {t['rows']}x{t['cols']}  [{cells}]")

    print(f"\n## Archetypes detected: {', '.join(sorted(report['archetypes']))}")
    for level, info in report["archetypes"].items():
        print(f"   {level:7s} → paraPrIDRef={info['para_pr_id']}  sample: {info['sample_text'][:50]}")


if __name__ == "__main__":
    raise SystemExit(main())
