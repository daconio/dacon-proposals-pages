#!/usr/bin/env python3
"""
md_to_slides.py — 제안서 Markdown을 네이티브 Google Slides 프레젠테이션으로 변환

`html_to_slides.py`가 슬라이드 덱 HTML을 다루는 반면, 이 스크립트는 **제안서 .md**
문서(H1/H2/H3 기반 위계)를 그대로 **편집 가능한 Google Slides**로 업로드합니다.

매핑 규칙
  H1         → 커버 슬라이드 (문서 제목 + 서문 첫 단락)
  H2 "I. …"  → 섹션 구분 슬라이드 (로마 숫자 + 섹션 제목)
  H2 기타    → 컨텐츠 슬라이드 (예: "제안 요약")
  H3         → 컨텐츠 슬라이드 (상위 H2의 섹션 헤더를 header_left로 승계)
  H4+        → 현재 슬라이드에 본문으로 포함

각 슬라이드 본문에서 다음을 자동 추출:
  * 첫 문단(리스트·표 전) → subtitle
  * Markdown 표(`|…|…|`) → 네이티브 Slides 표 (편집 가능)
  * 불릿 리스트(`- …` / `* …`) → 네이티브 불릿
  * 나머지 텍스트는 카드 블록으로 묶어 요약

사용법
  python3 scripts/md_to_slides.py 제안/foo.md                       # 업로드
  python3 scripts/md_to_slides.py --title "강원대 제안서" 제안/foo.md
  python3 scripts/md_to_slides.py --brand "KNU 2026" 제안/foo.md    # 우측 헤더 라벨
  python3 scripts/md_to_slides.py --dry-run 제안/foo.md > out.json  # API 호출 없이 구조 확인
  python3 scripts/md_to_slides.py --share user@dacon.io 제안/foo.md

최초 설정 (html_to_slides.py와 동일 — credentials/token 공유)
  `~/.config/dacon-slides/credentials.json` 필요 (Desktop OAuth client JSON).
  최초 실행 시 브라우저 OAuth 창 · 토큰은 자동 캐시.
  의존성: pip install google-api-python-client google-auth-oauthlib google-auth-httplib2
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent

# Reuse upload + request-builder logic from html_to_slides.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from html_to_slides import (  # noqa: E402
    PAGE_SIZES_EMU,
    build_requests_for_slide,
    upload_to_slides,
)


# ─────────────────────────────────────────────────────────────
# Markdown → slide data extractor
# ─────────────────────────────────────────────────────────────

ROMAN_RE = re.compile(r"^([IVXLCDM]+)\.\s+(.+)$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
TABLE_ROW_RE = re.compile(r"^\s*\|(.+)\|\s*$")
TABLE_SEP_RE = re.compile(r"^\s*\|\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|\s*$")
LIST_RE = re.compile(r"^\s*[-*]\s+(.+)$")


def _strip_md(text: str) -> str:
    """Remove common inline Markdown markers for readable plain text."""
    s = text
    s = re.sub(r"`([^`]+)`", r"\1", s)               # inline code
    s = re.sub(r"\*\*([^*]+)\*\*", r"\1", s)         # bold
    s = re.sub(r"__([^_]+)__", r"\1", s)             # bold alt
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"\1", s)  # italic
    s = re.sub(r"(?<!_)_([^_]+)_(?!_)", r"\1", s)      # italic alt
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)    # [text](url) → text
    s = re.sub(r"~~([^~]+)~~", r"\1", s)             # strikethrough
    return s.strip()


def _parse_headings(md: str) -> list[dict]:
    """Split MD text into sequential heading-bounded sections.

    Returns a list of dicts: {"level": int, "title": str, "body_lines": [str]}.
    Lines before the first heading are discarded.
    """
    sections: list[dict] = []
    current: dict | None = None
    for raw in md.split("\n"):
        m = HEADING_RE.match(raw)
        if m:
            if current is not None:
                sections.append(current)
            current = {
                "level": len(m.group(1)),
                "title": _strip_md(m.group(2)),
                "body_lines": [],
            }
        elif current is not None:
            current["body_lines"].append(raw)
    if current is not None:
        sections.append(current)
    return sections


def _extract_tables_from_body(lines: list[str]) -> list[dict[str, Any]]:
    """Find Markdown tables in a block of lines."""
    tables: list[dict[str, Any]] = []
    i = 0
    while i < len(lines):
        if TABLE_ROW_RE.match(lines[i]) and i + 1 < len(lines) and TABLE_SEP_RE.match(lines[i + 1]):
            header_cells = [_strip_md(c.strip()) for c in lines[i].strip().strip("|").split("|")]
            i += 2
            rows: list[list[str]] = []
            while i < len(lines) and TABLE_ROW_RE.match(lines[i]):
                row_cells = [_strip_md(c.strip()) for c in lines[i].strip().strip("|").split("|")]
                rows.append(row_cells)
                i += 1
            tables.append({"header": header_cells, "rows": rows})
            continue
        i += 1
    return tables


def _extract_lists_from_body(lines: list[str]) -> list[list[str]]:
    """Find bullet lists. Consecutive `- …` lines form one list."""
    lists: list[list[str]] = []
    current: list[str] = []
    for line in lines:
        m = LIST_RE.match(line)
        if m:
            current.append(_strip_md(m.group(1)))
        else:
            if line.strip() == "":
                continue  # blank line inside list is tolerated
            if current:
                lists.append(current)
                current = []
    if current:
        lists.append(current)
    return lists


def _first_paragraph(lines: list[str]) -> str:
    """First non-empty text line that isn't a table/list/blockquote/heading."""
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if s.startswith("|") or s.startswith(">") or s.startswith("#"):
            continue
        if LIST_RE.match(s):
            continue
        return _strip_md(s)[:220]
    return ""


def _cards_from_body(lines: list[str]) -> list[dict[str, str]]:
    """Collect residual paragraphs (not table/list) as short 'cards'.

    We grab bold-start paragraphs as card titles with the following text as
    description. Pattern: `**Title**: description` or a bold-only line followed
    by a non-bold line. Keeps output compact so Slides don't overflow.
    """
    cards: list[dict[str, str]] = []
    for raw in lines:
        s = raw.strip()
        if not s:
            continue
        if s.startswith("|") or s.startswith(">") or s.startswith("#") or LIST_RE.match(s):
            continue
        # "**Label**: body" inline pattern
        m = re.match(r"^\s*[-*]?\s*\*\*([^*]+)\*\*\s*[:：]\s*(.+)$", raw)
        if m:
            cards.append({"title": _strip_md(m.group(1)), "description": _strip_md(m.group(2))})
            continue
        # Standalone bold emphasis line → treat as minor card title only.
        m2 = re.match(r"^\s*\*\*([^*]+)\*\*\s*$", raw)
        if m2:
            cards.append({"title": _strip_md(m2.group(1)), "description": ""})
    return cards


def extract_slides_from_md(md_path: Path, brand: str) -> list[dict[str, Any]]:
    """Parse a proposal MD file into html_to_slides-compatible slide dicts."""
    md = md_path.read_text(encoding="utf-8")
    sections = _parse_headings(md)

    slides: list[dict[str, Any]] = []
    current_section_roman: str = ""
    subsection_idx = 0

    def next_page() -> str:
        return str(len(slides) + 1)

    for sec in sections:
        level = sec["level"]
        title = sec["title"]
        body_lines = sec["body_lines"]

        # H1 → cover slide
        if level == 1:
            slides.append({
                "id": f"md_{len(slides)}",
                "type": "cover",
                "header_left": "",
                "header_right": brand,
                "tag": "",
                "section_number": "",
                "title": title,
                "subtitle": _first_paragraph(body_lines),
                "tables": [],
                "lists": [],
                "cards": [],
                "metrics": [],
                "page": next_page(),
            })
            continue

        # H2 with roman numeral prefix → section divider
        roman = ROMAN_RE.match(title)
        if level == 2 and roman:
            current_section_roman = roman.group(1)
            subsection_idx = 0
            slides.append({
                "id": f"md_{len(slides)}",
                "type": "section",
                "header_left": "",
                "header_right": brand,
                "tag": "",
                "section_number": current_section_roman,
                "title": roman.group(2),
                "subtitle": _first_paragraph(body_lines),
                "tables": [],
                "lists": [],
                "cards": [],
                "metrics": [],
                "page": next_page(),
            })
            continue

        # Non-roman H2 (e.g. "제안 요약") → content slide
        # H3/H4 → content slide nested under current section
        if level == 2:
            current_section_roman = ""
            subsection_idx = 0
            header_left = title[:50]
        elif level == 3:
            subsection_idx += 1
            if current_section_roman:
                header_left = f"{current_section_roman}-{subsection_idx}"
            else:
                header_left = title[:50]
        else:
            # H4+ — attach as sub-content to the last slide instead of a new slide.
            if slides:
                last = slides[-1]
                last["lists"] = last["lists"] + _extract_lists_from_body(body_lines)
                last["tables"] = last["tables"] + _extract_tables_from_body(body_lines)
            continue

        clean_title = re.sub(r"^\d+\.\s*", "", title).strip()
        slides.append({
            "id": f"md_{len(slides)}",
            "type": "content",
            "header_left": header_left,
            "header_right": brand,
            "tag": "",
            "section_number": "",
            "title": clean_title,
            "subtitle": _first_paragraph(body_lines),
            "tables": _extract_tables_from_body(body_lines),
            "lists": _extract_lists_from_body(body_lines),
            "cards": _cards_from_body(body_lines),
            "metrics": [],
            "page": next_page(),
        })

    return slides


# ─────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("input", help="제안서 Markdown 파일 경로 (.md)")
    parser.add_argument("--title", help="Google Slides 제목 (기본: MD 파일 stem)")
    parser.add_argument("--brand", default="DACON",
                        help="우측 헤더에 표기할 브랜드/이벤트 라벨 (기본 'DACON')")
    parser.add_argument("--page-size", choices=list(PAGE_SIZES_EMU.keys()), default="16x9",
                        help="슬라이드 페이지 비율 (기본 16x9)")
    parser.add_argument("--share", metavar="EMAIL", help="완성 후 writer 권한 공유할 이메일")
    parser.add_argument("--dry-run", action="store_true",
                        help="Google API 호출 없이 추출 JSON만 stdout에 출력")
    parser.add_argument("--quiet", "-q", action="store_true")
    args = parser.parse_args()

    src = Path(args.input)
    if not src.exists():
        sys.stderr.write(f"❌ Not found: {src}\n")
        return 2
    if src.suffix.lower() != ".md":
        sys.stderr.write(f"⚠️  {src.name} is not .md — continuing anyway.\n")

    log = (lambda *a, **k: None) if args.quiet else print
    log(f"→ Extracting: {src}")
    slides_data = extract_slides_from_md(src, brand=args.brand)
    log(f"  slides extracted: {len(slides_data)}")

    if args.dry_run:
        json.dump(slides_data, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0

    title = args.title or src.stem
    pres_id, url = upload_to_slides(
        slides_data,
        title=title,
        page_size_key=args.page_size,
        share_email=args.share,
        quiet=args.quiet,
    )
    log(f"✓ Slides created: {url}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
