#!/usr/bin/env python3
"""
make_pdf.py — 제안서 슬라이드 HTML을 A4 또는 16:9 PDF로 변환 (2가지 포맷 지원)

`html_to_pdf.py`는 16:9(1280×720 → 960×540pt)만 생성합니다.
이 스크립트는 동일한 슬라이드 HTML에서 **A4 landscape / A4 portrait / 16:9**
PDF를 원클릭으로(또는 한 번에 전부) 생성합니다.

핵심 동작:
  1. Playwright로 슬라이드를 **1회만** 1280×720 PNG로 캡처
  2. 동일 PNG 세트를 여러 포맷의 PDF로 조립 (A4는 흰 배경 레터박스 센터 피팅)

사용법:
  # 기본: 16:9 + A4 landscape 둘 다 생성 (2가지 버전)
  python3 scripts/make_pdf.py 제안/2026-04-17-강원대_부트캠프.html

  # 한 포맷만 원할 때
  python3 scripts/make_pdf.py --format 16x9    제안/foo.html
  python3 scripts/make_pdf.py --format a4      제안/foo.html
  python3 scripts/make_pdf.py --format a4p     제안/foo.html    # A4 portrait

  # 전부 (16:9 + A4 landscape + A4 portrait)
  python3 scripts/make_pdf.py --format all     제안/foo.html

  # 고품질 (scale 3× + 무손실 PNG 임베드)
  python3 scripts/make_pdf.py --hq 제안/foo.html

출력 파일명 규칙 (입력 HTML과 같은 폴더):
  16:9          → <stem>.pdf
  A4 landscape  → <stem>.a4.pdf
  A4 portrait   → <stem>.a4p.pdf

옵션:
  --format  { 16x9 | a4 | a4p | both | all }   기본 both
                 both = 16x9 + a4 (landscape)
                 all  = 16x9 + a4 + a4p
  --scale N      캡처 device_scale_factor (기본 2. 2=Retina, 3=고해상도)
  --lossless     PNG 무손실 임베드 (img2pdf 필요, 파일 크지만 텍스트 선명)
  --hq           --scale 3 + --lossless 일괄 (최종 납품 권장)
  --quiet, -q    진행 메시지 숨김

요구사항:
  - Python 3.8+
  - playwright (pip install playwright)  — 시스템 Chrome 사용
  - Pillow     (pip install Pillow)
  - img2pdf    (pip install img2pdf)     — --lossless / --hq 시 필요
"""

from __future__ import annotations

import argparse
import glob
import io
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Re-use Chrome detection from html_to_pdf.py (same folder)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from html_to_pdf import find_chrome  # noqa: E402

# Default slide capture geometry — matches the slide deck CSS (--sw2 / --sh).
# Current project default is **A4 landscape** (1280 × 905, ratio ≈ 1.414).
# Legacy decks use 16:9 (1280 × 720). Actual size is auto-detected from #stage
# at capture time, so both formats work without manual override.
CAPTURE_W = 1280
CAPTURE_H = 905

# A4 dimensions in millimeters (portrait, width × height).
A4_W_MM = 210
A4_H_MM = 297

# Print-quality DPI for A4 page rasterization (letterbox canvas).
A4_DPI = 300


# ─────────────────────────────────────────────────────────────
# Slide capture (shared across all output formats)
# ─────────────────────────────────────────────────────────────

def capture_slides(src: Path, tmpdir: Path, scale: int, quiet: bool) -> tuple[list[Path], int, int]:
    """Render each .slide to its own PNG.

    Capture dimensions are auto-detected from the #stage bounding box —
    works for both A4-landscape (1280×905) and legacy 16:9 (1280×720) decks.

    Returns (ordered PNG paths, detected_width_px, detected_height_px).
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.stderr.write("❌ playwright not installed. Run: pip install playwright\n")
        sys.exit(2)

    chrome = find_chrome()
    if not chrome:
        sys.stderr.write("❌ Google Chrome not found.\n")
        sys.exit(2)

    log = (lambda *a, **k: None) if quiet else print

    png_paths: list[Path] = []
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=chrome, headless=True)
        # Initial viewport uses project default — will be resized once #stage
        # bounding box is measured from the CSS variables --sw2 / --sh.
        ctx = browser.new_context(
            viewport={"width": CAPTURE_W, "height": CAPTURE_H},
            device_scale_factor=scale,
        )
        page = ctx.new_page()
        page.goto(src.as_uri(), wait_until="networkidle")
        page.wait_for_timeout(500)  # initial layout settle

        # Auto-detect stage dimensions from computed style, then resize viewport
        # to match — prevents scale() transform from distorting the screenshot.
        dims = page.evaluate("""() => {
            const s = document.getElementById('stage');
            if (!s) return null;
            const cs = getComputedStyle(s);
            return { w: parseFloat(cs.width), h: parseFloat(cs.height) };
        }""")
        if dims and dims.get("w") and dims.get("h"):
            det_w = int(round(dims["w"]))
            det_h = int(round(dims["h"]))
        else:
            det_w, det_h = CAPTURE_W, CAPTURE_H
        if (det_w, det_h) != (CAPTURE_W, CAPTURE_H):
            page.set_viewport_size({"width": det_w, "height": det_h})
            page.wait_for_timeout(200)
        log(f"  stage: {det_w}×{det_h}px (auto-detected)")
        page.wait_for_timeout(2000)  # font + JS settle

        # Hide navigation UI in screen-media capture.
        page.add_style_tag(
            content="""
            #key-hint, .nav-btn, #nav-prev, #nav-next, #progress-bar,
            .controls, .presenter-notes, .speaker-notes {
                display: none !important;
                visibility: hidden !important;
            }
            """
        )

        total = page.evaluate("document.querySelectorAll('.slide').length")
        if total == 0:
            browser.close()
            sys.stderr.write(
                f"❌ No `.slide` elements found in {src.name}.\n"
                "   make_pdf.py expects a slide deck with <section class=\"slide\"> elements.\n"
            )
            sys.exit(2)

        log(f"  slides: {total}")

        for i in range(total):
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
            page.wait_for_timeout(180)
            stage = page.query_selector("#stage") or page.query_selector(".slide.active")
            if stage is None:
                browser.close()
                sys.stderr.write("❌ Could not find #stage or .slide.active element.\n")
                sys.exit(2)
            png = tmpdir / f"slide_{i:03d}.png"
            stage.screenshot(path=str(png), omit_background=False)
            png_paths.append(png)
            if not quiet and ((i + 1) % 5 == 0 or i + 1 == total):
                log(f"    captured {i + 1}/{total}")

        browser.close()

    return png_paths, det_w, det_h


# ─────────────────────────────────────────────────────────────
# PDF assemblers — A4 (native) and 16:9 (letterbox)
# ─────────────────────────────────────────────────────────────

def _assemble_pdf(
    images,
    out: Path,
    page_size_pt: tuple[float, float],
    dpi_for_jpeg: int,
    lossless: bool,
) -> None:
    """Assemble a list of PIL RGB images into a PDF.

    * lossless=True uses img2pdf (PNG /FlateDecode, largest, sharpest).
    * lossless=False uses Pillow's PDF backend (JPEG q=95, smaller).
    """
    from PIL import Image  # noqa: F401  (ensure PIL is installed)

    if lossless:
        try:
            import img2pdf
        except ImportError:
            sys.stderr.write(
                "⚠️  img2pdf not installed — falling back to JPEG. "
                "Run: pip install img2pdf for lossless output.\n"
            )
            images[0].save(
                str(out),
                save_all=True,
                append_images=images[1:],
                format="PDF",
                resolution=float(dpi_for_jpeg),
                quality=95,
            )
            return

        layout = img2pdf.get_layout_fun(page_size_pt)
        png_bytes_list = []
        for img in images:
            buf = io.BytesIO()
            img.save(buf, format="PNG", optimize=True, compress_level=9)
            png_bytes_list.append(buf.getvalue())
        out.write_bytes(img2pdf.convert(png_bytes_list, layout_fun=layout))
    else:
        images[0].save(
            str(out),
            save_all=True,
            append_images=images[1:],
            format="PDF",
            resolution=float(dpi_for_jpeg),
            quality=95,
        )


def _page_size_pt(fmt: str) -> tuple[float, float]:
    """Return PDF page size in points for a given output format."""
    if fmt == "16x9":
        # 1280 × 720 px → 960 × 540 pt (13.333 × 7.5 in)
        return (1280 * 72 / 96, 720 * 72 / 96)
    if fmt == "a4":
        return (A4_H_MM * 72 / 25.4, A4_W_MM * 72 / 25.4)  # 297×210 mm
    if fmt == "a4p":
        return (A4_W_MM * 72 / 25.4, A4_H_MM * 72 / 25.4)  # 210×297 mm
    raise ValueError(f"Unknown format: {fmt}")


def make_fit_pdf(
    png_paths: list[Path],
    out: Path,
    fmt: str,
    lossless: bool,
    quiet: bool,
) -> None:
    """Assemble PNGs into a PDF of the target format.

    If captured aspect matches the target page aspect (within tolerance),
    embed PNGs directly (native). Otherwise, center-fit each PNG onto a
    white canvas at 300 DPI and assemble (letterbox).
    """
    from PIL import Image

    log = (lambda *a, **k: None) if quiet else print

    page_size_pt = _page_size_pt(fmt)
    page_aspect = page_size_pt[0] / page_size_pt[1]

    first = Image.open(png_paths[0])
    iw, ih = first.size
    img_aspect = iw / ih

    # Native embed if aspect matches within 0.5% tolerance.
    native = abs(img_aspect - page_aspect) / page_aspect < 0.005

    if native:
        log(f"  assembling {fmt} PDF — native ({len(png_paths)} pages, PNG {iw}×{ih})")
        images = [Image.open(p).convert("RGB") for p in png_paths]
        dpi = int(round(iw * 72 / page_size_pt[0]))
        _assemble_pdf(images, out, page_size_pt, dpi_for_jpeg=dpi, lossless=lossless)
        return

    # Letterbox path — composite onto white canvas at 300 DPI.
    page_w_px = int(round(page_size_pt[0] * A4_DPI / 72))
    page_h_px = int(round(page_size_pt[1] * A4_DPI / 72))
    log(f"  assembling {fmt} PDF — letterbox ({len(png_paths)} pages, canvas {page_w_px}×{page_h_px}px @ {A4_DPI}dpi)")

    pages = []
    for png in png_paths:
        img = Image.open(png).convert("RGB")
        iw2, ih2 = img.size
        fit = min(page_w_px / iw2, page_h_px / ih2)
        new_w = max(1, int(round(iw2 * fit)))
        new_h = max(1, int(round(ih2 * fit)))
        scaled = img.resize((new_w, new_h), Image.LANCZOS)
        page = Image.new("RGB", (page_w_px, page_h_px), (255, 255, 255))
        page.paste(scaled, ((page_w_px - new_w) // 2, (page_h_px - new_h) // 2))
        pages.append(page)

    _assemble_pdf(pages, out, page_size_pt, dpi_for_jpeg=A4_DPI, lossless=lossless)


# ─────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────

FORMAT_CHOICES = ["16x9", "a4", "a4p", "both", "all"]


def expand_inputs(patterns: list[str]) -> list[Path]:
    files: list[Path] = []
    for pat in patterns:
        matched = glob.glob(pat)
        if matched:
            files.extend(Path(m) for m in matched)
        else:
            files.append(Path(pat))
    return files


def resolve_format_list(fmt: str) -> list[str]:
    """Expand format preset to list of concrete formats."""
    if fmt == "both":
        return ["16x9", "a4"]
    if fmt == "all":
        return ["16x9", "a4", "a4p"]
    return [fmt]


def output_path_for(src: Path, fmt: str) -> Path:
    stem = src.stem
    parent = src.parent
    suffix = {"16x9": ".pdf", "a4": ".a4.pdf", "a4p": ".a4p.pdf"}[fmt]
    return parent / f"{stem}{suffix}"


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("inputs", nargs="+", help="HTML 입력 파일 경로 (글롭 지원)")
    parser.add_argument(
        "--format", "-f",
        choices=FORMAT_CHOICES, default="both",
        help="출력 포맷 (기본 both = 16x9 + a4-landscape). all = 16x9 + a4 + a4p",
    )
    parser.add_argument("--scale", type=int, default=2, help="캡처 device_scale_factor (기본 2)")
    parser.add_argument("--lossless", action="store_true", help="PNG 무손실 임베드 (img2pdf 필요)")
    parser.add_argument("--hq", action="store_true", help="--scale 3 + --lossless 일괄 적용")
    parser.add_argument("--quiet", "-q", action="store_true", help="진행 메시지 숨김")
    args = parser.parse_args()

    if args.hq:
        args.scale = max(args.scale, 3)
        args.lossless = True

    files = expand_inputs(args.inputs)
    if not files:
        sys.stderr.write("❌ No input files matched.\n")
        return 2

    fmts = resolve_format_list(args.format)
    log = (lambda *a, **k: None) if args.quiet else print

    rc = 0
    for src in files:
        if not src.exists():
            sys.stderr.write(f"❌ Not found: {src}\n")
            rc = 1
            continue
        src = src.resolve()
        try:
            rel = src.relative_to(ROOT) if src.is_relative_to(ROOT) else src
            log(f"→ Converting: {rel}")
            log(f"  formats: {', '.join(fmts)} · scale ×{args.scale} · {'lossless PNG' if args.lossless else 'JPEG q95'}")

            tmpdir = Path(tempfile.mkdtemp(prefix="make_pdf_"))
            try:
                png_paths, _det_w, _det_h = capture_slides(src, tmpdir, args.scale, args.quiet)

                for fmt in fmts:
                    out = output_path_for(src, fmt)
                    make_fit_pdf(png_paths, out, fmt, args.lossless, args.quiet)
                    rel_out = out.relative_to(ROOT) if out.is_relative_to(ROOT) else out
                    log(f"✓ {fmt:5s} → {rel_out} ({out.stat().st_size:,} bytes)")
            finally:
                shutil.rmtree(tmpdir, ignore_errors=True)
        except SystemExit:
            raise
        except Exception as e:
            sys.stderr.write(f"❌ Failed {src}: {e}\n")
            rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main())
