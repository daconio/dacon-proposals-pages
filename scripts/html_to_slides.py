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

        # Detect "visual boxes" — elements whose styling can't be recreated
        # faithfully in native Slides. If present and --boxes-as-images is on,
        # the slide body is rasterized to a single PNG.
        box_selectors = ".c, .kpi, .stage-bar, .step-row, .flow-row, .gantt, .mx"
        slide["has_boxes"] = section.select_one(box_selectors) is not None
        # Body image URL — populated later by capture_box_bodies() if enabled.
        slide["body_image_url"] = ""

        slides.append(slide)

    return slides


# ─────────────────────────────────────────────────────────────
# 1b. Box-as-image — Playwright body capture + Drive upload
# ─────────────────────────────────────────────────────────────

def capture_box_bodies(
    html_path: Path,
    slides_data: list[dict[str, Any]],
    tmp_dir: Path,
    quiet: bool,
) -> None:
    """For each slide with has_boxes=True, screenshot its body region to PNG.

    Paths are stored in slide["_body_png_path"] for later Drive upload.
    The body region = the full .slide section minus .sh (header) and .sf (footer),
    i.e. the .si area. This preserves all card/metric/gantt/etc. visuals in a
    single editable-as-image chunk.
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.stderr.write("❌ playwright not installed. Run: pip install playwright\n")
        sys.exit(2)

    # Reuse Chrome detection from html_to_pdf.
    import shutil
    chrome_paths = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary",
        shutil.which("google-chrome") or "", shutil.which("chromium") or "",
    ]
    chrome = next((p for p in chrome_paths if p and Path(p).exists()), None)
    if not chrome:
        sys.stderr.write("❌ Google Chrome not found.\n")
        sys.exit(2)

    log = (lambda *a, **k: None) if quiet else print
    targets = [i for i, s in enumerate(slides_data) if s.get("has_boxes")]
    if not targets:
        log("  no slides with boxes — skipping capture")
        return

    log(f"  capturing box bodies for {len(targets)} slides...")

    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=chrome, headless=True)
        # Use a large-enough viewport; stage size is auto-detected below.
        ctx = browser.new_context(viewport={"width": 1280, "height": 905}, device_scale_factor=2)
        page = ctx.new_page()
        page.goto(html_path.as_uri(), wait_until="networkidle")
        page.wait_for_timeout(500)

        # Hide viewer-only chrome before measuring / capturing boxes too.
        page.add_style_tag(content="""
            #key-hint, #kbd-hint, .kbd-hint,
            .nav, .nav-btn, .nav-prev, .nav-next, .slide-nav, .navigation,
            .bar, #progress-bar, .progress-bar, .progress,
            .controls, .slide-controls, .hotkeys,
            .no-capture, [data-capture="hide"] {
                display: none !important;
                visibility: hidden !important;
            }
        """)

        dims = page.evaluate("""() => {
            const s = document.getElementById('stage');
            if (!s) return null;
            const cs = getComputedStyle(s);
            return { w: parseFloat(cs.width), h: parseFloat(cs.height) };
        }""")
        if dims and dims.get("w") and dims.get("h"):
            page.set_viewport_size({"width": int(dims["w"]), "height": int(dims["h"])})
            page.wait_for_timeout(200)
        page.wait_for_timeout(1500)  # font settle

        # Hide navigation UI.
        page.add_style_tag(content="""
            #key-hint, .nav-btn, #progress-bar { display: none !important; }
        """)

        for i in targets:
            # Activate the target slide via its class manipulation (same as make_pdf.py).
            page.evaluate(
                """({i}) => {
                    const slides = document.querySelectorAll('.slide');
                    slides.forEach((s, idx) => {
                        if (idx === i) {
                            s.classList.add('active');
                            s.querySelectorAll('[data-step]').forEach(e => {
                                e.classList.remove('pre-visible');
                                e.classList.add('visible');
                            });
                        } else {
                            s.classList.remove('active');
                        }
                    });
                }""",
                {"i": i},
            )
            page.wait_for_timeout(200)
            # Screenshot the .si region of the active slide (excludes .sh/.sf).
            si = page.query_selector(".slide.active .si")
            if si is None:
                # Fallback to full stage
                si = page.query_selector("#stage")
            if si is None:
                continue
            png_path = tmp_dir / f"body_{i:03d}.png"
            si.screenshot(path=str(png_path), omit_background=False)
            slides_data[i]["_body_png_path"] = str(png_path)
            if not quiet and ((i + 1) % 5 == 0 or i + 1 == len(slides_data)):
                log(f"    captured body {i + 1}/{len(slides_data)}")

        browser.close()


def capture_full_slides(
    html_path: Path,
    slides_data: list[dict[str, Any]],
    tmp_dir: Path,
    quiet: bool,
    stage_w: int = 1280,
    stage_h: int = 720,
) -> None:
    """Capture ENTIRE #stage (full slide incl. header/footer) for every slide.

    Used by --all-as-images to produce one full PNG per slide for embedding
    as a single fullscreen image in the resulting Google Slides.

    stage_w/stage_h: force the HTML stage to this size before capture so the
    resulting PNG exactly matches the Slides page aspect (Google Slides defaults
    to 16:9 = 1280×720 px and does not accept custom pageSize via API). HTML
    content designed for a different aspect (e.g. A4 landscape 1280×905) may
    clip at the bottom/sides — rendering overflow:hidden.
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.stderr.write("❌ playwright not installed. Run: pip install playwright\n")
        sys.exit(2)

    import shutil
    chrome_paths = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary",
        shutil.which("google-chrome") or "", shutil.which("chromium") or "",
    ]
    chrome = next((p for p in chrome_paths if p and Path(p).exists()), None)
    if not chrome:
        sys.stderr.write("❌ Google Chrome not found.\n")
        sys.exit(2)

    log = (lambda *a, **k: None) if quiet else print
    log(f"  capturing full slides for {len(slides_data)} slides at {stage_w}×{stage_h}px...")

    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=chrome, headless=True)
        ctx = browser.new_context(viewport={"width": stage_w, "height": stage_h}, device_scale_factor=3)
        page = ctx.new_page()
        page.goto(html_path.as_uri(), wait_until="networkidle")
        page.wait_for_timeout(500)

        # Force stage to requested dimensions for Slides aspect match.
        # Hide anything that is viewer-only chrome (nav buttons, progress bars,
        # key hints) so it does not get baked into the captured PNG. Convention:
        # any element with class `.no-capture` or attribute `data-capture="hide"`
        # is also hidden — authors should use these on custom chrome.
        page.add_style_tag(content=f"""
            #key-hint, #kbd-hint, .kbd-hint,
            .nav, .nav-btn, .nav-prev, .nav-next, .slide-nav, .navigation,
            .bar, #progress-bar, .progress-bar, .progress,
            .controls, .slide-controls, .hotkeys,
            .no-capture, [data-capture="hide"] {{
                display: none !important;
                visibility: hidden !important;
            }}
            #stage {{ width: {stage_w}px !important; height: {stage_h}px !important; }}
        """)
        page.set_viewport_size({"width": stage_w, "height": stage_h})
        page.wait_for_timeout(1500)

        # Store stage dims on each slide for aspect-preserving layout.
        for sd in slides_data:
            sd["_stage_w"] = stage_w
            sd["_stage_h"] = stage_h

        for i in range(len(slides_data)):
            page.evaluate(
                """({i}) => {
                    const slides = document.querySelectorAll('.slide');
                    slides.forEach((s, idx) => {
                        if (idx === i) {
                            s.classList.add('active');
                            s.querySelectorAll('[data-step]').forEach(e => {
                                e.classList.remove('pre-visible');
                                e.classList.add('visible');
                            });
                        } else {
                            s.classList.remove('active');
                        }
                    });
                }""",
                {"i": i},
            )
            page.wait_for_timeout(200)
            stage = page.query_selector("#stage")
            if stage is None:
                continue
            png_path = tmp_dir / f"full_{i:03d}.png"
            stage.screenshot(path=str(png_path), omit_background=False)
            slides_data[i]["_body_png_path"] = str(png_path)
            if not quiet and ((i + 1) % 5 == 0 or i + 1 == len(slides_data)):
                log(f"    captured {i + 1}/{len(slides_data)}")

        browser.close()


def build_full_image_slide(
    sd: dict[str, Any],
    idx: int,
    page_w: int,
    page_h: int,
) -> list[dict]:
    """Build a Slides page that contains ONLY one full image (all-as-images mode).

    Image is aspect-preserved and centered; letterbox white bars fill mismatch.
    """
    slide_id = _oid("slide", idx)
    requests: list[dict] = [{
        "createSlide": {
            "objectId": slide_id,
            "insertionIndex": idx,
            "slideLayoutReference": {"predefinedLayout": "BLANK"},
        }
    }]
    if not sd.get("body_image_url"):
        return requests

    stage_w = sd.get("_stage_w") or 1280
    stage_h = sd.get("_stage_h") or 905
    stage_ratio = stage_w / stage_h
    page_ratio = page_w / page_h

    if abs(page_ratio - stage_ratio) < 0.005:
        img_w, img_h, tx, ty = page_w, page_h, 0, 0
    elif page_ratio > stage_ratio:
        img_h = page_h
        img_w = int(round(page_h * stage_ratio))
        tx = (page_w - img_w) // 2
        ty = 0
    else:
        img_w = page_w
        img_h = int(round(page_w / stage_ratio))
        tx = 0
        ty = (page_h - img_h) // 2

    requests.append({
        "createImage": {
            "objectId": _oid("slide", idx, "img"),
            "url": sd["body_image_url"],
            "elementProperties": {
                "pageObjectId": slide_id,
                "size": {"width": {"magnitude": img_w, "unit": "EMU"},
                         "height": {"magnitude": img_h, "unit": "EMU"}},
                "transform": {"scaleX": 1, "scaleY": 1,
                              "translateX": tx, "translateY": ty, "unit": "EMU"},
            },
        }
    })
    return requests


def upload_images_to_drive(
    slides_data: list[dict[str, Any]],
    drive_svc,
    quiet: bool,
) -> list[str]:
    """Upload captured body PNGs to Drive (publicly readable). Sets body_image_url.

    Returns list of uploaded Drive file IDs so caller can clean up later.
    """
    from googleapiclient.http import MediaFileUpload

    log = (lambda *a, **k: None) if quiet else print
    uploaded_ids: list[str] = []

    for i, sd in enumerate(slides_data):
        path = sd.get("_body_png_path", "")
        if not path:
            continue
        media = MediaFileUpload(path, mimetype="image/png", resumable=False)
        file = drive_svc.files().create(
            body={"name": f"slide_{i:03d}_body.png", "mimeType": "image/png"},
            media_body=media,
            fields="id",
        ).execute()
        fid = file["id"]
        # Make publicly readable so Slides API can fetch it.
        drive_svc.permissions().create(
            fileId=fid,
            body={"role": "reader", "type": "anyone"},
        ).execute()
        sd["body_image_url"] = f"https://drive.google.com/uc?id={fid}"
        uploaded_ids.append(fid)
        if not quiet and ((i + 1) % 5 == 0 or i == len(slides_data) - 1):
            log(f"    uploaded image {i + 1}/{len(slides_data)}")

    return uploaded_ids


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

    # If this slide has a body image (rasterized boxes), insert it and
    # skip native rendering of tables/lists/cards — they're inside the image.
    if sd.get("body_image_url"):
        img_id = _oid("slide", idx, "bodyimg")
        # Fill the remaining area down to just above the footer.
        img_h = page_h - cursor_y - margin_bottom - int(0.05 * EMU_PER_INCH)
        if img_h > int(0.5 * EMU_PER_INCH):
            requests.append({
                "createImage": {
                    "objectId": img_id,
                    "url": sd["body_image_url"],
                    "elementProperties": {
                        "pageObjectId": slide_id,
                        "size": {
                            "width": {"magnitude": content_w, "unit": "EMU"},
                            "height": {"magnitude": img_h, "unit": "EMU"},
                        },
                        "transform": {
                            "scaleX": 1, "scaleY": 1,
                            "translateX": content_x, "translateY": cursor_y,
                            "unit": "EMU",
                        },
                    },
                }
            })
        requests.extend(add_header_footer())
        return requests

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
    html_path: Path | None = None,
    boxes_as_images: bool = False,
    all_as_images: bool = False,
) -> tuple[str, str]:
    """Create a Google Slides presentation. Returns (presentation_id, url).

    When boxes_as_images=True and html_path is given, slides containing
    visual box-like elements get their body region rasterized to PNG and
    inserted as an editable-as-image chunk (preserves cards/metrics/Gantt
    styling faithfully).
    """
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

    # Create the presentation FIRST so we know the actual Slides page size
    # (Google Slides API ignores requested pageSize — always creates 16:9).
    log(f"→ Creating presentation: {title!r}")
    page_w_req, page_h_req = PAGE_SIZES_EMU[page_size_key]
    create_body = {
        "title": title,
        "pageSize": {
            "width": {"magnitude": page_w_req, "unit": "EMU"},
            "height": {"magnitude": page_h_req, "unit": "EMU"},
        },
    }
    pres = slides_svc.presentations().create(body=create_body).execute()
    pres_id = pres["presentationId"]
    actual = pres.get("pageSize", {})
    page_w = int(actual.get("width", {}).get("magnitude", page_w_req))
    page_h = int(actual.get("height", {}).get("magnitude", page_h_req))
    if (page_w, page_h) != (page_w_req, page_h_req):
        log(f"  ⚠️  requested {page_w_req}×{page_h_req} EMU but Slides created "
            f"{page_w}×{page_h} — capture & layout will adapt to actual.")
    log(f"  id: {pres_id}  page: {page_w}×{page_h} EMU ({page_w/914400:.2f}×{page_h/914400:.2f} in)")

    # Capture + upload images, using the actual Slides page aspect so the
    # final images fill the slide edge-to-edge (no letterbox).
    drive_cleanup_ids: list[str] = []
    tmp_dir: Path | None = None
    if all_as_images and html_path:
        import tempfile
        tmp_dir = Path(tempfile.mkdtemp(prefix="full_img_"))
        # Pick capture size matching actual page aspect. Keep width=1280,
        # compute height from Slides page ratio → no letterbox.
        capture_w = 1280
        capture_h = int(round(capture_w * page_h / page_w))
        log(f"→ Capturing full-slide images at {capture_w}×{capture_h} (matches Slides aspect)")
        capture_full_slides(html_path.resolve(), slides_data, tmp_dir, quiet,
                            stage_w=capture_w, stage_h=capture_h)
        log("→ Uploading full-slide images to Drive...")
        drive_cleanup_ids = upload_images_to_drive(slides_data, drive_svc, quiet)
    elif boxes_as_images and html_path:
        import tempfile
        tmp_dir = Path(tempfile.mkdtemp(prefix="box_img_"))
        log(f"→ Capturing box-body images (temp: {tmp_dir})")
        capture_box_bodies(html_path.resolve(), slides_data, tmp_dir, quiet)
        log("→ Uploading body images to Drive...")
        drive_cleanup_ids = upload_images_to_drive(slides_data, drive_svc, quiet)

    # Default slide id — will be deleted after our slides are created.
    default_slide_id = pres["slides"][0]["objectId"]

    # Batch requests in reasonable chunks (Slides API limits batch size).
    BATCH_LIMIT = 50  # requests per batch call
    all_requests: list[dict] = []
    for i, sd in enumerate(slides_data):
        if all_as_images:
            all_requests.extend(build_full_image_slide(sd, i, page_w, page_h))
        else:
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

    # Clean up temporary Drive files (Slides already cached the images).
    if drive_cleanup_ids:
        log(f"  cleaning up {len(drive_cleanup_ids)} temp Drive files...")
        for fid in drive_cleanup_ids:
            try:
                drive_svc.files().delete(fileId=fid).execute()
            except Exception as e:
                sys.stderr.write(f"⚠️  cleanup failed for {fid}: {e}\n")
    if tmp_dir and tmp_dir.exists():
        import shutil as _sh
        _sh.rmtree(tmp_dir, ignore_errors=True)

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
    parser.add_argument("--boxes-as-images", action="store_true",
                        help="박스(카드/메트릭/KPI/단계바/Gantt 등)가 있는 슬라이드는 본문을 "
                             "PNG로 캡처해 이미지로 삽입 — 시각 스타일 보존. "
                             "Playwright + Google Chrome 필요.")
    parser.add_argument("--all-as-images", action="store_true",
                        help="전 슬라이드 #stage 전체를 PNG로 캡처해 풀페이지 이미지로 삽입. "
                             "편집 불가이지만 시각 완벽 보존. "
                             "--page-size a4와 함께 쓰면 원본(1280x905) 비율과 정확히 매치.")
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
        html_path=src if (args.boxes_as_images or args.all_as_images) else None,
        boxes_as_images=args.boxes_as_images,
        all_as_images=args.all_as_images,
    )
    log(f"✓ Slides created: {url}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
