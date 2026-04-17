#!/usr/bin/env python3
"""
html_to_slides.py — 슬라이드 덱 HTML을 네이티브 Google Slides 프레젠테이션으로 변환

`make_pdf.py`가 PDF를 만드는 반면, 이 스크립트는 HTML 슬라이드 덱의
**텍스트·표·리스트·카드**를 추출해서 **편집 가능한 Google Slides**로 업로드합니다.

방식
  1. BeautifulSoup으로 HTML에서 각 .slide 섹션별 구조화 데이터 추출
     (제목, 부제, 태그, 표[2D], 불릿 리스트, 카드[제목+설명])
  2. Google Slides API v1 `batchUpdate`로 새 프레젠테이션 생성 + 슬라이드 단위로 요청 전송
  3. 완성된 Slides URL 출력

사용법
  python3 scripts/html_to_slides.py 제안/foo.html                         # 업로드
  python3 scripts/html_to_slides.py --title "강원대 제안서" 제안/foo.html
  python3 scripts/html_to_slides.py --dry-run 제안/foo.html > slides.json # API 호출 없이 JSON만
  python3 scripts/html_to_slides.py --share user@dacon.io 제안/foo.html   # 공유 이메일 부여

최초 인증 (한 번만)
  1. GCP 프로젝트에서 Google Slides API + Google Drive API **활성화**
  2. OAuth 2.0 클라이언트 ID (유형: 데스크톱 앱) 생성 → JSON 다운로드
  3. JSON을 `~/.config/dacon-slides/credentials.json` 으로 저장
  4. pip install google-api-python-client google-auth-oauthlib google-auth-httplib2 beautifulsoup4
  5. 첫 실행 시 브라우저 OAuth 동의 창 → 토큰은 `~/.config/dacon-slides/token.json` 에 자동 캐시

커스텀 설정
  환경변수 `DACON_SLIDES_DIR`로 credentials/token 저장 경로 변경 가능.

주의
  * 복잡한 CSS(카드, 그라디언트, 아이콘) 100% 재현은 아님. 편집 가능한 텍스트+표 중심.
  * 시각 보존이 목표라면 `make_pdf.py`로 PDF + PNG 추출 후 Slides에 이미지로 삽입하는 워크플로우 별도.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent

# EMU (English Metric Units) constants — Slides API uses EMU for positions/sizes.
# 1 inch = 914,400 EMU. 1 cm = 360,000 EMU. 1 pt = 12,700 EMU.
EMU_PER_INCH = 914_400
EMU_PER_PT = 12_700

# Default slide page size: 16:9 widescreen (Google Slides default).
# 10 × 5.625 in = 9,144,000 × 5,143,500 EMU.
# Switching to A4 landscape would mean 11.69 × 8.27 in, which would be closer to
# our HTML source's 1.414 ratio — but 16:9 is more compatible with Slides presenter
# tooling. Configurable via --page-size.
PAGE_SIZES_EMU = {
    "16x9": (9_144_000, 5_143_500),
    "a4": (int(297 / 25.4 * EMU_PER_INCH), int(210 / 25.4 * EMU_PER_INCH)),  # landscape
}

# Brand colors (RGB, 0–1 scale for Slides API)
BRAND_PRIMARY = {"red": 0.118, "green": 0.227, "blue": 0.541}  # #1E3A8A
BRAND_WARM = {"red": 0.761, "green": 0.384, "blue": 0.176}  # #c2622d
TEXT_DARK = {"red": 0.059, "green": 0.090, "blue": 0.165}  # #0f172a
TEXT_MUTED = {"red": 0.278, "green": 0.337, "blue": 0.412}  # #475569


# ─────────────────────────────────────────────────────────────
# 1. Extractor — HTML → structured slide data (pure, no Google API)
# ─────────────────────────────────────────────────────────────

def _text(el) -> str:
    """Collapsed, trimmed text content of a BeautifulSoup element."""
    if el is None:
        return ""
    s = el.get_text(" ", strip=True)
    return re.sub(r"\s+", " ", s).strip()


def _classify_slide(section) -> str:
    """Identify slide type from CSS classes."""
    classes = section.get("class", [])
    if "slide-end" in classes:
        return "end"
    if "slide-sec" in classes:
        return "section"
    if section.get("id") == "s1":
        return "cover"
    return "content"


def _extract_table(tbl) -> dict[str, Any]:
    """Extract a <table> into {header: [str], rows: [[str]]}."""
    header: list[str] = []
    thead_tr = tbl.select_one("thead tr")
    if thead_tr:
        header = [_text(th) for th in thead_tr.select("th")]

    rows: list[list[str]] = []
    for tr in tbl.select("tbody tr"):
        cells = [_text(td) for td in tr.select("td")]
        if cells:
            rows.append(cells)
    # Fallback: some tables have no thead/tbody.
    if not header and not rows:
        trs = tbl.select("tr")
        if trs:
            header_candidate = [_text(th) for th in trs[0].select("th")]
            if header_candidate:
                header = header_candidate
                for tr in trs[1:]:
                    rows.append([_text(td) for td in tr.select("td,th")])
            else:
                for tr in trs:
                    rows.append([_text(td) for td in tr.select("td,th")])
    return {"header": header, "rows": rows}


def extract_slides(html_path: Path) -> list[dict[str, Any]]:
    """Parse the HTML deck and return a list of slide data dicts."""
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        sys.stderr.write("❌ beautifulsoup4 not installed. Run: pip install beautifulsoup4\n")
        sys.exit(2)

    html = html_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    slides: list[dict[str, Any]] = []
    for section in soup.select("section.slide"):
        slide: dict[str, Any] = {
            "id": section.get("id", f"slide_{len(slides)}"),
            "type": _classify_slide(section),
            "header_left": _text(section.select_one(".sh .sh-l")),
            "header_right": _text(section.select_one(".sh .sh-r")),
            "tag": _text(section.select_one(".tag")),
            "section_number": _text(section.select_one(".sn")) if "slide-sec" in section.get("class", []) else "",
            "title": _text(section.select_one("h2.st") or section.select_one("h2") or section.select_one("h1")),
            "subtitle": _text(section.select_one(".sub") or section.select_one(".sd") or section.select_one(".end-sub")),
            "page": _text(section.select_one(".sf .sf-pg")),
        }

        # Tables
        slide["tables"] = [_extract_table(t) for t in section.select("table.tb, table.tb-xs, table")]

        # Bullet lists (.ck is the project's canonical bullet style; also grab <ul> as fallback).
        lists = []
        for ul in section.select("ul.ck, ul"):
            items: list[str] = []
            for li in ul.select("li"):
                # Project pattern: <li><span class="i">●</span><div>actual text</div></li>
                content_div = li.select_one("div")
                if content_div:
                    items.append(_text(content_div))
                else:
                    items.append(_text(li))
            if items:
                lists.append(items)
        slide["lists"] = lists

        # Cards: .c-t (title) + .c-d (description) inside a .c container
        cards = []
        for c in section.select(".c, .c-b, .c-w, .c-s, .c-g"):
            if c.name == "table":
                continue
            t_el = c.select_one(".c-t")
            d_el = c.select_one(".c-d")
            if t_el or d_el:
                cards.append({"title": _text(t_el), "description": _text(d_el)})
        slide["cards"] = cards

        # Metric boxes (.mx with .v value + .l label)
        metrics = []
        for m in section.select(".mx, .kpi .k"):
            v = m.select_one(".v")
            l = m.select_one(".l")
            if v or l:
                metrics.append({"value": _text(v), "label": _text(l)})
        slide["metrics"] = metrics

        slides.append(slide)

    return slides


# ─────────────────────────────────────────────────────────────
# 2. Slides API request builder — structured data → batchUpdate requests
# ─────────────────────────────────────────────────────────────

def _oid(prefix: str, i: int, *suffixes: str) -> str:
    parts = [prefix, f"{i:03d}", *suffixes]
    return "_".join(parts)


def _textbox(object_id: str, page_id: str, x: int, y: int, w: int, h: int) -> dict:
    return {
        "createShape": {
            "objectId": object_id,
            "shapeType": "TEXT_BOX",
            "elementProperties": {
                "pageObjectId": page_id,
                "size": {
                    "width": {"magnitude": w, "unit": "EMU"},
                    "height": {"magnitude": h, "unit": "EMU"},
                },
                "transform": {
                    "scaleX": 1, "scaleY": 1,
                    "translateX": x, "translateY": y,
                    "unit": "EMU",
                },
            },
        }
    }


def _insert_text(object_id: str, text: str) -> dict:
    return {"insertText": {"objectId": object_id, "text": text}}


def _style_text(object_id: str, start: int, end: int, style: dict) -> dict:
    fields = ",".join(style.keys())
    return {
        "updateTextStyle": {
            "objectId": object_id,
            "textRange": {"type": "FIXED_RANGE", "startIndex": start, "endIndex": end},
            "style": style,
            "fields": fields,
        }
    }


def _style_all(object_id: str, style: dict) -> dict:
    fields = ",".join(style.keys())
    return {
        "updateTextStyle": {
            "objectId": object_id,
            "textRange": {"type": "ALL"},
            "style": style,
            "fields": fields,
        }
    }


def _paragraph_style_all(object_id: str, style: dict) -> dict:
    fields = ",".join(style.keys())
    return {
        "updateParagraphStyle": {
            "objectId": object_id,
            "textRange": {"type": "ALL"},
            "style": style,
            "fields": fields,
        }
    }


def _bullets(object_id: str, preset: str = "BULLET_DISC_CIRCLE_SQUARE") -> dict:
    return {
        "createParagraphBullets": {
            "objectId": object_id,
            "textRange": {"type": "ALL"},
            "bulletPreset": preset,
        }
    }


def build_requests_for_slide(
    sd: dict[str, Any],
    idx: int,
    page_w: int,
    page_h: int,
) -> list[dict]:
    """Return batchUpdate requests creating one slide from extracted data."""
    requests: list[dict] = []
    slide_id = _oid("slide", idx)

    # 1) Create blank slide.
    requests.append({
        "createSlide": {
            "objectId": slide_id,
            "insertionIndex": idx,
            "slideLayoutReference": {"predefinedLayout": "BLANK"},
        }
    })

    # Layout margins (EMU). Compact for 16:9 widescreen readability.
    margin_x = int(0.5 * EMU_PER_INCH)
    margin_top = int(0.25 * EMU_PER_INCH)
    margin_bottom = int(0.3 * EMU_PER_INCH)
    content_x = margin_x
    content_w = page_w - 2 * margin_x

    # Common helper: add header/footer (page number, section label) to any slide.
    def add_header_footer():
        reqs = []
        # Left header label (e.g., "II-1 13개 세부 업무 1/2")
        if sd["header_left"]:
            hdr_l_id = _oid("slide", idx, "hdrL")
            reqs.append(_textbox(
                hdr_l_id, slide_id,
                margin_x, int(0.1 * EMU_PER_INCH),
                int(content_w * 0.6), int(0.18 * EMU_PER_INCH),
            ))
            reqs.append(_insert_text(hdr_l_id, sd["header_left"].upper()))
            reqs.append(_style_all(hdr_l_id, {
                "fontFamily": "Noto Sans KR",
                "fontSize": {"magnitude": 8, "unit": "PT"},
                "bold": True,
                "foregroundColor": {"opaqueColor": {"rgbColor": BRAND_PRIMARY}},
            }))
        # Right header label (e.g., "KNU AI BOOTCAMP 2026")
        if sd["header_right"]:
            hdr_r_id = _oid("slide", idx, "hdrR")
            right_x = page_w - margin_x - int(content_w * 0.35)
            reqs.append(_textbox(
                hdr_r_id, slide_id,
                right_x, int(0.1 * EMU_PER_INCH),
                int(content_w * 0.35), int(0.18 * EMU_PER_INCH),
            ))
            reqs.append(_insert_text(hdr_r_id, sd["header_right"].upper()))
            reqs.append(_style_all(hdr_r_id, {
                "fontFamily": "Noto Sans KR",
                "fontSize": {"magnitude": 7, "unit": "PT"},
                "bold": True,
                "foregroundColor": {"opaqueColor": {"rgbColor": TEXT_MUTED}},
            }))
            reqs.append(_paragraph_style_all(hdr_r_id, {"alignment": "END"}))
        # Footer logo + page number + copyright
        foot_logo_id = _oid("slide", idx, "ftL")
        reqs.append(_textbox(
            foot_logo_id, slide_id,
            margin_x, page_h - int(0.25 * EMU_PER_INCH),
            int(content_w * 0.3), int(0.18 * EMU_PER_INCH),
        ))
        reqs.append(_insert_text(foot_logo_id, "DACON"))
        reqs.append(_style_all(foot_logo_id, {
            "fontFamily": "Noto Sans KR",
            "fontSize": {"magnitude": 7, "unit": "PT"},
            "bold": True,
            "foregroundColor": {"opaqueColor": {"rgbColor": BRAND_PRIMARY}},
        }))
        if sd["page"]:
            pg_id = _oid("slide", idx, "pg")
            reqs.append(_textbox(
                pg_id, slide_id,
                (page_w - int(0.3 * EMU_PER_INCH)) // 2, page_h - int(0.25 * EMU_PER_INCH),
                int(0.3 * EMU_PER_INCH), int(0.18 * EMU_PER_INCH),
            ))
            reqs.append(_insert_text(pg_id, sd["page"]))
            reqs.append(_style_all(pg_id, {
                "fontSize": {"magnitude": 7, "unit": "PT"},
                "bold": True,
                "foregroundColor": {"opaqueColor": {"rgbColor": TEXT_MUTED}},
            }))
            reqs.append(_paragraph_style_all(pg_id, {"alignment": "CENTER"}))
        foot_cr_id = _oid("slide", idx, "ftR")
        reqs.append(_textbox(
            foot_cr_id, slide_id,
            page_w - margin_x - int(content_w * 0.3), page_h - int(0.25 * EMU_PER_INCH),
            int(content_w * 0.3), int(0.18 * EMU_PER_INCH),
        ))
        reqs.append(_insert_text(foot_cr_id, "COPYRIGHT 2026"))
        reqs.append(_style_all(foot_cr_id, {
            "fontSize": {"magnitude": 6, "unit": "PT"},
            "foregroundColor": {"opaqueColor": {"rgbColor": TEXT_MUTED}},
        }))
        reqs.append(_paragraph_style_all(foot_cr_id, {"alignment": "END"}))
        return reqs

    # Cover / End slide: centered title + subtitle.
    if sd["type"] in ("cover", "end"):
        title_text = sd["title"] or sd["header_right"]
        subtitle_text = sd["subtitle"]

        title_id = _oid("slide", idx, "title")
        title_h = int(1.2 * EMU_PER_INCH)
        title_y = (page_h - title_h) // 2 - int(0.3 * EMU_PER_INCH)
        requests.append(_textbox(title_id, slide_id, content_x, title_y, content_w, title_h))
        if title_text:
            requests.append(_insert_text(title_id, title_text))
            requests.append(_style_all(title_id, {
                "fontFamily": "Noto Sans KR",
                "fontSize": {"magnitude": 24, "unit": "PT"},
                "bold": True,
                "foregroundColor": {"opaqueColor": {"rgbColor": TEXT_DARK}},
            }))
            requests.append(_paragraph_style_all(title_id, {"alignment": "CENTER"}))

        if subtitle_text:
            sub_id = _oid("slide", idx, "subtitle")
            sub_y = title_y + title_h + int(0.1 * EMU_PER_INCH)
            requests.append(_textbox(sub_id, slide_id, content_x, sub_y, content_w, int(0.8 * EMU_PER_INCH)))
            requests.append(_insert_text(sub_id, subtitle_text))
            requests.append(_style_all(sub_id, {
                "fontFamily": "Noto Sans KR",
                "fontSize": {"magnitude": 11, "unit": "PT"},
                "foregroundColor": {"opaqueColor": {"rgbColor": TEXT_MUTED}},
            }))
            requests.append(_paragraph_style_all(sub_id, {"alignment": "CENTER"}))

        requests.extend(add_header_footer())
        return requests

    # Section divider: large roman numeral + title below.
    if sd["type"] == "section":
        if sd["section_number"]:
            num_id = _oid("slide", idx, "num")
            num_y = int(1.2 * EMU_PER_INCH)
            requests.append(_textbox(num_id, slide_id, content_x, num_y, content_w, int(1.3 * EMU_PER_INCH)))
            requests.append(_insert_text(num_id, sd["section_number"]))
            requests.append(_style_all(num_id, {
                "fontFamily": "Noto Sans KR",
                "fontSize": {"magnitude": 54, "unit": "PT"},
                "bold": True,
                "foregroundColor": {"opaqueColor": {"rgbColor": BRAND_PRIMARY}},
            }))
            requests.append(_paragraph_style_all(num_id, {"alignment": "CENTER"}))

        title_id = _oid("slide", idx, "title")
        title_y = int(2.8 * EMU_PER_INCH)
        requests.append(_textbox(title_id, slide_id, content_x, title_y, content_w, int(0.7 * EMU_PER_INCH)))
        requests.append(_insert_text(title_id, sd["title"] or ""))
        requests.append(_style_all(title_id, {
            "fontFamily": "Noto Sans KR",
            "fontSize": {"magnitude": 22, "unit": "PT"},
            "bold": True,
            "foregroundColor": {"opaqueColor": {"rgbColor": TEXT_DARK}},
        }))
        requests.append(_paragraph_style_all(title_id, {"alignment": "CENTER"}))

        if sd["subtitle"]:
            sub_id = _oid("slide", idx, "subtitle")
            requests.append(_textbox(sub_id, slide_id, content_x, title_y + int(0.7 * EMU_PER_INCH),
                                    content_w, int(0.6 * EMU_PER_INCH)))
            requests.append(_insert_text(sub_id, sd["subtitle"]))
            requests.append(_style_all(sub_id, {
                "fontFamily": "Noto Sans KR",
                "fontSize": {"magnitude": 10, "unit": "PT"},
                "foregroundColor": {"opaqueColor": {"rgbColor": TEXT_MUTED}},
            }))
            requests.append(_paragraph_style_all(sub_id, {"alignment": "CENTER"}))

        requests.extend(add_header_footer())
        return requests

    # Content slide — vertical stack of: tag, title, subtitle, body (tables+lists+cards).
    # Header/footer handled by add_header_footer at the end.
    # Leave room at top for header bar (~0.28in) and bottom for footer (~0.28in).
    cursor_y = int(0.35 * EMU_PER_INCH)

    if sd["tag"]:
        tag_id = _oid("slide", idx, "tag")
        requests.append(_textbox(tag_id, slide_id, content_x, cursor_y, content_w, int(0.2 * EMU_PER_INCH)))
        requests.append(_insert_text(tag_id, sd["tag"]))
        requests.append(_style_all(tag_id, {
            "fontFamily": "Noto Sans KR",
            "fontSize": {"magnitude": 8, "unit": "PT"},
            "bold": True,
            "foregroundColor": {"opaqueColor": {"rgbColor": BRAND_WARM}},
        }))
        cursor_y += int(0.22 * EMU_PER_INCH)

    if sd["title"]:
        t_id = _oid("slide", idx, "title")
        requests.append(_textbox(t_id, slide_id, content_x, cursor_y, content_w, int(0.55 * EMU_PER_INCH)))
        requests.append(_insert_text(t_id, sd["title"]))
        requests.append(_style_all(t_id, {
            "fontFamily": "Noto Sans KR",
            "fontSize": {"magnitude": 18, "unit": "PT"},
            "bold": True,
            "foregroundColor": {"opaqueColor": {"rgbColor": TEXT_DARK}},
        }))
        cursor_y += int(0.55 * EMU_PER_INCH)

    if sd["subtitle"]:
        s_id = _oid("slide", idx, "subtitle")
        requests.append(_textbox(s_id, slide_id, content_x, cursor_y, content_w, int(0.35 * EMU_PER_INCH)))
        requests.append(_insert_text(s_id, sd["subtitle"]))
        requests.append(_style_all(s_id, {
            "fontFamily": "Noto Sans KR",
            "fontSize": {"magnitude": 10, "unit": "PT"},
            "foregroundColor": {"opaqueColor": {"rgbColor": TEXT_MUTED}},
        }))
        cursor_y += int(0.4 * EMU_PER_INCH)

    # Tables
    for ti, tbl in enumerate(sd["tables"]):
        header = tbl["header"]
        rows = tbl["rows"]
        n_cols = max(len(header), *(len(r) for r in rows), 1) if (header or rows) else 0
        n_rows = (1 if header else 0) + len(rows)
        if n_cols == 0 or n_rows == 0:
            continue
        tbl_id = _oid("slide", idx, f"tbl{ti}")
        row_h = int(0.25 * EMU_PER_INCH)
        tbl_h = row_h * n_rows
        # Clamp so we don't overflow — leave footer room.
        available = page_h - cursor_y - margin_bottom - int(0.15 * EMU_PER_INCH)
        if tbl_h > available:
            tbl_h = available
        requests.append({
            "createTable": {
                "objectId": tbl_id,
                "elementProperties": {
                    "pageObjectId": slide_id,
                    "size": {"width": {"magnitude": content_w, "unit": "EMU"},
                             "height": {"magnitude": tbl_h, "unit": "EMU"}},
                    "transform": {"scaleX": 1, "scaleY": 1,
                                  "translateX": content_x, "translateY": cursor_y,
                                  "unit": "EMU"},
                },
                "rows": n_rows,
                "columns": n_cols,
            }
        })
        # Fill cells. Rows are 0-indexed; header is row 0 if present.
        def fill_cell(r: int, c: int, text: str, bold: bool = False):
            if not text:
                return
            requests.append({
                "insertText": {
                    "objectId": tbl_id,
                    "cellLocation": {"rowIndex": r, "columnIndex": c},
                    "text": text,
                }
            })
            style_req = {
                "updateTextStyle": {
                    "objectId": tbl_id,
                    "cellLocation": {"rowIndex": r, "columnIndex": c},
                    "textRange": {"type": "ALL"},
                    "style": {
                        "fontFamily": "Noto Sans KR",
                        "fontSize": {"magnitude": 8, "unit": "PT"},
                        "bold": bold,
                        "foregroundColor": {"opaqueColor": {"rgbColor": TEXT_DARK if bold else TEXT_MUTED}},
                    },
                    "fields": "fontFamily,fontSize,bold,foregroundColor",
                }
            }
            requests.append(style_req)

        if header:
            for ci, cell in enumerate(header[:n_cols]):
                fill_cell(0, ci, cell, bold=True)
        row_offset = 1 if header else 0
        for ri, row in enumerate(rows):
            for ci, cell in enumerate(row[:n_cols]):
                fill_cell(ri + row_offset, ci, cell)
        cursor_y += tbl_h + int(0.2 * EMU_PER_INCH)

    # Bullet lists
    for li_idx, items in enumerate(sd["lists"]):
        if not items:
            continue
        list_id = _oid("slide", idx, f"list{li_idx}")
        list_h = int(max(0.4, 0.22 * len(items)) * EMU_PER_INCH)
        if cursor_y + list_h > page_h - margin_bottom - int(0.1 * EMU_PER_INCH):
            break  # skip if overflow
        requests.append(_textbox(list_id, slide_id, content_x, cursor_y, content_w, list_h))
        requests.append(_insert_text(list_id, "\n".join(items)))
        requests.append(_style_all(list_id, {
            "fontFamily": "Noto Sans KR",
            "fontSize": {"magnitude": 9, "unit": "PT"},
            "foregroundColor": {"opaqueColor": {"rgbColor": TEXT_MUTED}},
        }))
        requests.append(_bullets(list_id))
        cursor_y += list_h + int(0.1 * EMU_PER_INCH)

    # Cards as compact text (title — description per line)
    card_lines = [f"{c['title']} — {c['description']}".strip(" —") for c in sd["cards"] if c.get("title") or c.get("description")]
    if card_lines and cursor_y < page_h - margin_bottom - int(0.2 * EMU_PER_INCH):
        card_id = _oid("slide", idx, "cards")
        card_h = int(max(0.4, 0.22 * len(card_lines)) * EMU_PER_INCH)
        if cursor_y + card_h > page_h - margin_bottom - int(0.1 * EMU_PER_INCH):
            card_h = page_h - cursor_y - margin_bottom - int(0.1 * EMU_PER_INCH)
        if card_h > int(0.2 * EMU_PER_INCH):
            requests.append(_textbox(card_id, slide_id, content_x, cursor_y, content_w, card_h))
            requests.append(_insert_text(card_id, "\n".join(card_lines)))
            requests.append(_style_all(card_id, {
                "fontFamily": "Noto Sans KR",
                "fontSize": {"magnitude": 8, "unit": "PT"},
                "foregroundColor": {"opaqueColor": {"rgbColor": TEXT_DARK}},
            }))

    requests.extend(add_header_footer())
    return requests


# ─────────────────────────────────────────────────────────────
# 3. Google Slides uploader
# ─────────────────────────────────────────────────────────────

SCOPES = [
    "https://www.googleapis.com/auth/presentations",
    "https://www.googleapis.com/auth/drive.file",
]


def _config_dir() -> Path:
    override = os.environ.get("DACON_SLIDES_DIR")
    if override:
        return Path(override).expanduser()
    return Path.home() / ".config" / "dacon-slides"


def get_credentials():
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError:
        sys.stderr.write(
            "❌ Google auth libs not installed. Run:\n"
            "   pip install google-api-python-client google-auth-oauthlib google-auth-httplib2\n"
        )
        sys.exit(2)

    cfg_dir = _config_dir()
    cfg_dir.mkdir(parents=True, exist_ok=True)
    creds_path = cfg_dir / "credentials.json"
    token_path = cfg_dir / "token.json"

    if not creds_path.exists():
        sys.stderr.write(
            f"❌ OAuth client JSON missing: {creds_path}\n"
            "   Create a Desktop OAuth client in GCP → download JSON → save to that path.\n"
            "   https://console.cloud.google.com/apis/credentials\n"
        )
        sys.exit(2)

    creds = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(creds_path), SCOPES)
            creds = flow.run_local_server(port=0)
        token_path.write_text(creds.to_json())
    return creds


def upload_to_slides(
    slides_data: list[dict[str, Any]],
    title: str,
    page_size_key: str,
    share_email: str | None,
    quiet: bool,
) -> tuple[str, str]:
    """Create a Google Slides presentation. Returns (presentation_id, url)."""
    try:
        from googleapiclient.discovery import build
        from googleapiclient.errors import HttpError
    except ImportError:
        sys.stderr.write("❌ google-api-python-client not installed.\n")
        sys.exit(2)

    log = (lambda *a, **k: None) if quiet else print
    creds = get_credentials()

    slides_svc = build("slides", "v1", credentials=creds)
    drive_svc = build("drive", "v3", credentials=creds)

    log(f"→ Creating presentation: {title!r}")
    pres = slides_svc.presentations().create(body={"title": title}).execute()
    pres_id = pres["presentationId"]
    log(f"  id: {pres_id}")

    page_w, page_h = PAGE_SIZES_EMU[page_size_key]

    # Default slide id — will be deleted after our slides are created.
    default_slide_id = pres["slides"][0]["objectId"]

    # Batch requests in reasonable chunks (Slides API limits batch size).
    BATCH_LIMIT = 50  # requests per batch call
    all_requests: list[dict] = []
    for i, sd in enumerate(slides_data):
        all_requests.extend(build_requests_for_slide(sd, i, page_w, page_h))

    # Drop default slide after all new slides exist (index 0 created slides have insertionIndex 0..N)
    all_requests.append({"deleteObject": {"objectId": default_slide_id}})

    log(f"  total requests: {len(all_requests)}")
    for chunk_start in range(0, len(all_requests), BATCH_LIMIT):
        chunk = all_requests[chunk_start: chunk_start + BATCH_LIMIT]
        try:
            slides_svc.presentations().batchUpdate(
                presentationId=pres_id, body={"requests": chunk}
            ).execute()
            log(f"  sent batch {chunk_start}..{chunk_start + len(chunk) - 1}")
        except HttpError as e:
            sys.stderr.write(f"❌ batchUpdate failed at {chunk_start}: {e}\n")
            raise

    # Optional share
    if share_email:
        try:
            drive_svc.permissions().create(
                fileId=pres_id,
                body={"type": "user", "role": "writer", "emailAddress": share_email},
                sendNotificationEmail=False,
            ).execute()
            log(f"  shared with: {share_email}")
        except HttpError as e:
            sys.stderr.write(f"⚠️  share failed: {e}\n")

    url = f"https://docs.google.com/presentation/d/{pres_id}/edit"
    return pres_id, url


# ─────────────────────────────────────────────────────────────
# 4. CLI
# ─────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("input", help="슬라이드 덱 HTML 경로")
    parser.add_argument("--title", help="Google Slides 제목 (기본: 파일명)")
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

    log = (lambda *a, **k: None) if args.quiet else print
    log(f"→ Extracting: {src}")
    slides_data = extract_slides(src)
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
