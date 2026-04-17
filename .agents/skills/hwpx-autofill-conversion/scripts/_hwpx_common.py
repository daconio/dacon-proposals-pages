"""Shared helpers for HWPX autofill pipeline.

Why this file exists: both the inspector and the builder need to read an
HWPX archive, parse the section XML, and classify paragraphs. Putting the
low-level primitives here keeps the orchestrator thin and the same rules
apply consistently to inspection and rebuilding — if one side sees a
paragraph as "body" and the other doesn't, the output drifts.

HWPX is just a ZIP of XML. We deliberately avoid a real XML parser because
the namespace prefixes are verbose and the serializer would re-write every
tag (changing whitespace, attribute order, etc.) in a way HWP viewers
sometimes reject. Instead we work on the raw string with targeted regexes
on well-known tags — the HWPX format is machine-generated and stable
enough for this to be safe.
"""
from __future__ import annotations

import re
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator


# ---------------------------------------------------------------------------
# ZIP I/O
# ---------------------------------------------------------------------------


def read_hwpx_members(path: Path) -> dict[str, bytes]:
    """Read every file in the HWPX archive into memory.

    We load everything because we repack it later and want to preserve
    metadata files (mimetype, META-INF/*, BinData/*, Preview/*, etc.)
    byte-for-byte. Only Contents/section*.xml and Preview/PrvText.txt are
    modified.
    """
    members: dict[str, bytes] = {}
    with zipfile.ZipFile(path, "r") as zf:
        for name in zf.namelist():
            members[name] = zf.read(name)
    return members


def write_hwpx(out_path: Path, members: dict[str, bytes]) -> None:
    """Write an HWPX archive with the `mimetype` entry first and STORED.

    The HWPX/EPUB convention requires `mimetype` to be the first entry and
    stored uncompressed so tools can sniff the format by reading the first
    ~30 bytes of the zip. Everything else is deflated.
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out_path, "w", allowZip64=True) as zf:
        if "mimetype" in members:
            info = zipfile.ZipInfo("mimetype")
            info.compress_type = zipfile.ZIP_STORED
            zf.writestr(info, members["mimetype"])
        for name, data in members.items():
            if name == "mimetype":
                continue
            info = zipfile.ZipInfo(name)
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, data)


# ---------------------------------------------------------------------------
# Section XML parsing
# ---------------------------------------------------------------------------


PARA_OPEN_RE = re.compile(r"<hp:p\b[^>]*>")
PARA_CLOSE_RE = re.compile(r"</hp:p\s*>")
PARA_SELF_CLOSE_RE = re.compile(r"<hp:p\b[^>]*/>")
ROOT_RE = re.compile(r"(<\?xml[^>]*\?>\s*<hs:sec\b[^>]*>)", re.DOTALL)


def iter_top_level_paragraphs(xml: str, start: int, end: int) -> Iterator[tuple[int, int]]:
    """Yield (start, end) byte ranges of top-level `<hp:p>` blocks.

    HWPX tables contain `<hp:subList>` with their own `<hp:p>` children,
    so a naive non-greedy match matches at the wrong depth. We walk the
    string and track `<hp:p` open/close events with a depth counter so
    only depth-1 paragraphs (direct children of `<hs:sec>`) get emitted.
    Self-closing `<hp:p .../>` tags are yielded as-is.
    """
    pos = start
    while pos < end:
        # Find next <hp:p ...
        open_match = PARA_OPEN_RE.search(xml, pos, end)
        if not open_match:
            return
        open_start = open_match.start()
        open_end = open_match.end()

        # Self-closing `<hp:p .../>`?
        if xml[open_end - 2:open_end] == "/>":
            yield (open_start, open_end)
            pos = open_end
            continue

        # Scan forward balancing <hp:p> ... </hp:p> nesting.
        depth = 1
        cursor = open_end
        while depth > 0 and cursor < end:
            next_open = PARA_OPEN_RE.search(xml, cursor, end)
            next_close = PARA_CLOSE_RE.search(xml, cursor, end)
            if not next_close:
                return  # malformed; stop
            if next_open and next_open.start() < next_close.start():
                # Check self-closing — doesn't increase depth.
                if xml[next_open.end() - 2:next_open.end()] == "/>":
                    cursor = next_open.end()
                else:
                    depth += 1
                    cursor = next_open.end()
            else:
                depth -= 1
                cursor = next_close.end()
        yield (open_start, cursor)
        pos = cursor
SEC_CLOSE = "</hs:sec>"
PARA_PR_RE = re.compile(r'paraPrIDRef="(\d+)"')
STYLE_REF_RE = re.compile(r'styleIDRef="(\d+)"')
CHAR_PR_RE = re.compile(r'charPrIDRef="(\d+)"')
TEXT_RE = re.compile(r"<hp:t>([^<]*)</hp:t>", re.DOTALL)
TBL_RE = re.compile(r"<hp:tbl\b", re.DOTALL)
SECPR_RE = re.compile(r"<hp:secPr\b", re.DOTALL)


@dataclass
class Paragraph:
    """One `<hp:p>...</hp:p>` block with the derived classification we use."""

    index: int
    xml: str
    para_pr_id: str
    style_id: str
    has_text: bool
    has_table: bool
    has_secpr: bool
    text: str  # concatenation of all <hp:t> contents in this paragraph

    @property
    def kind(self) -> str:
        if self.has_secpr:
            return "secpr"
        if self.has_table:
            return "table"
        if self.has_text:
            return "text"
        return "empty"


@dataclass
class Section:
    path: str  # e.g. "Contents/section0.xml"
    root_open: str  # `<?xml?> ... <hs:sec xmlns:...>`
    paragraphs: list[Paragraph] = field(default_factory=list)
    trailing: str = ""  # anything between last para and </hs:sec> (usually empty)

    def serialize(self, paragraphs: list[str]) -> str:
        return self.root_open + "".join(paragraphs) + self.trailing + SEC_CLOSE


def parse_section(path: str, xml_bytes: bytes) -> Section:
    xml = xml_bytes.decode("utf-8")

    m = ROOT_RE.match(xml)
    if not m:
        raise ValueError(f"{path}: not a recognisable HWPX section XML")
    root_open = m.group(1)

    # Find all top-level paragraphs (depth-1 children of <hs:sec>).
    root_end = m.end()
    close_idx = xml.rfind(SEC_CLOSE)
    if close_idx < 0:
        close_idx = len(xml)

    paragraphs: list[Paragraph] = []
    last_para_end = root_end
    for i, (p_start, p_end) in enumerate(iter_top_level_paragraphs(xml, root_end, close_idx)):
        pxml = xml[p_start:p_end]
        last_para_end = p_end
        ppr = PARA_PR_RE.search(pxml)
        sty = STYLE_REF_RE.search(pxml)
        text_parts = TEXT_RE.findall(pxml)
        paragraphs.append(
            Paragraph(
                index=i,
                xml=pxml,
                para_pr_id=ppr.group(1) if ppr else "",
                style_id=sty.group(1) if sty else "",
                has_text=bool(text_parts) and any(t.strip() for t in text_parts),
                has_table=bool(TBL_RE.search(pxml)),
                has_secpr=bool(SECPR_RE.search(pxml)),
                text="".join(text_parts),
            )
        )

    # Everything between last top-level </hp:p> and </hs:sec>.
    trailing = xml[last_para_end:close_idx]

    return Section(path=path, root_open=root_open, paragraphs=paragraphs, trailing=trailing)


# ---------------------------------------------------------------------------
# Paragraph rewriting
# ---------------------------------------------------------------------------


def iter_text_ranges(para_xml: str) -> list[tuple[int, int, str]]:
    """Return (start, end, inner_text) for each <hp:t>...</hp:t> in order."""
    out: list[tuple[int, int, str]] = []
    for m in TEXT_RE.finditer(para_xml):
        out.append((m.start(1), m.end(1), m.group(1)))
    return out


def replace_text_runs(para_xml: str, new_text: str) -> str:
    """Replace all <hp:t> contents in this paragraph with `new_text`.

    Strategy: put the full `new_text` in the first run that currently has
    non-whitespace text (to inherit its charPrIDRef), and clear the rest.
    This keeps at least one run present so the paragraph still renders,
    preserves its character style, and avoids creating runs from scratch
    which would need a charPr reference we'd have to guess.
    """
    ranges = iter_text_ranges(para_xml)
    if not ranges:
        return para_xml  # no text runs to touch (e.g., empty spacer)

    # Find the first "primary" run with actual text; fall back to the first.
    primary_idx = 0
    for i, (_, _, text) in enumerate(ranges):
        if text.strip():
            primary_idx = i
            break

    # Rebuild from right to left so earlier offsets stay valid.
    result = para_xml
    for i in range(len(ranges) - 1, -1, -1):
        start, end, _ = ranges[i]
        replacement = _xml_escape(new_text) if i == primary_idx else ""
        result = result[:start] + replacement + result[end:]
    return result


def _xml_escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


# ---------------------------------------------------------------------------
# Archetype classification
# ---------------------------------------------------------------------------


# Korean bullet characters that signal the template's outline level.
LEVEL_HINTS: list[tuple[str, str]] = [
    ("□", "h1"),   # 15pt 헤드라인
    ("■", "h1"),
    ("○", "h2"),   # 14pt 서브헤딩
    ("●", "h2"),
    ("-", "h3"),   # 14pt detail
    ("※", "h4"),   # 11pt note
    ("Ⅰ", "section"),
    ("Ⅱ", "section"),
    ("Ⅲ", "section"),
    ("Ⅳ", "section"),
    ("Ⅴ", "section"),
    ("Ⅵ", "section"),
]


def guess_level(text: str) -> str:
    """Return one of: section, h1, h2, h3, h4, body — based on bullet prefix."""
    stripped = text.lstrip()
    for prefix, level in LEVEL_HINTS:
        if stripped.startswith(prefix):
            return level
    return "body"


def classify_paragraphs(section: Section) -> dict[str, list[int]]:
    """Group paragraph indexes by inferred level, for archetype lookup."""
    groups: dict[str, list[int]] = {}
    for p in section.paragraphs:
        if p.kind != "text":
            continue
        level = guess_level(p.text)
        groups.setdefault(level, []).append(p.index)
    return groups
