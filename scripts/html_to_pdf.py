#!/usr/bin/env python3
"""
html_to_pdf.py — DACON 제안서 슬라이드 HTML을 PDF로 변환

슬라이드 덱(.slide 요소 기반) HTML을 정확한 비율(기본 1280×720)의
표준 PDF로 변환합니다. Chrome 헤드리스의 print-to-pdf Pages tree
버그(Skia/PDF m146)를 우회하기 위해 슬라이드를 1개씩 개별 렌더링
한 뒤 PyPDF2로 병합합니다.

사용법:
  python3 scripts/html_to_pdf.py <input.html> [output.pdf]
  python3 scripts/html_to_pdf.py 제안/2026-04-08-강원대학교_X+AI_SW융합프로젝트_제안서.html
  python3 scripts/html_to_pdf.py "제안/*.html"   # 글롭 지원
  python3 scripts/html_to_pdf.py --width 960 --height 1358 portrait.html
  python3 scripts/html_to_pdf.py --quiet input.html

옵션:
  --width N      슬라이드 가로 px (기본 1280)
  --height N     슬라이드 세로 px (기본 720)
  --quiet        진행 메시지 숨김
  --output PATH  출력 경로 명시 (생략 시 입력과 같은 폴더, .pdf 확장자)
  --no-verify    PyPDF2 검증 스킵

요구사항:
  - Python 3.8+
  - playwright (`pip install playwright` — 브라우저 다운로드 불필요, 시스템 Chrome 사용)
  - PyPDF2  (`pip install PyPDF2`)
  - Google Chrome.app (macOS 기본 경로 또는 PATH 내 chrome)
"""

from __future__ import annotations

import argparse
import glob
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Default Chrome paths to try
CHROME_PATHS = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    shutil.which("google-chrome") or "",
    shutil.which("chromium") or "",
    shutil.which("chrome") or "",
]


def find_chrome() -> str | None:
    for p in CHROME_PATHS:
        if p and Path(p).exists():
            return p
    return None


def convert(
    src: Path,
    out: Path,
    width: int = 1280,
    height: int = 720,
    quiet: bool = False,
    verify: bool = True,
) -> int:
    """Convert a slide-deck HTML to PDF. Returns final page count."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.stderr.write(
            "❌ playwright not installed. Run: pip install playwright\n"
            "   (no need to run `playwright install` — script uses system Chrome)\n"
        )
        sys.exit(2)

    try:
        from PyPDF2 import PdfReader, PdfWriter
    except ImportError:
        sys.stderr.write("❌ PyPDF2 not installed. Run: pip install PyPDF2\n")
        sys.exit(2)

    chrome = find_chrome()
    if not chrome:
        sys.stderr.write(
            "❌ Google Chrome not found. Install Chrome or set CHROME_PATHS.\n"
        )
        sys.exit(2)

    if not src.exists():
        sys.stderr.write(f"❌ Input not found: {src}\n")
        sys.exit(2)

    src = src.resolve()
    out = out.resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    log = (lambda *a, **k: None) if quiet else print

    log(f"→ Converting: {src.relative_to(ROOT) if src.is_relative_to(ROOT) else src}")
    log(f"  size: {width}×{height}px")

    tmpdir = Path(tempfile.mkdtemp(prefix="html2pdf_"))
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=chrome, headless=True)
            ctx = browser.new_context(viewport={"width": width, "height": height})
            page = ctx.new_page()
            page.goto(src.as_uri(), wait_until="networkidle")
            page.wait_for_timeout(2500)  # font + JS settle

            total = page.evaluate("document.querySelectorAll('.slide').length")
            if total == 0:
                browser.close()
                sys.stderr.write(
                    f"❌ No `.slide` elements found in {src.name}.\n"
                    "   This script expects a slide deck with multiple <section class=\"slide\">.\n"
                )
                sys.exit(2)

            log(f"  slides: {total}")

            # Render each slide individually with all data-step elements revealed
            for i in range(total):
                page.evaluate(
                    """({ i, w, h }) => {
                        const slides = document.querySelectorAll('.slide');
                        slides.forEach((s, idx) => {
                            if (idx === i) {
                                s.style.cssText = `position:relative !important; inset:auto !important; opacity:1 !important; pointer-events:auto !important; display:flex !important; flex-direction:column !important; width:${w}px !important; height:${h}px !important; margin:0 !important; overflow:hidden !important; transform:none !important;`;
                                s.querySelectorAll('[data-step]').forEach(e => {
                                    e.classList.add('visible');
                                    e.classList.remove('pre-visible');
                                });
                            } else {
                                s.style.cssText = 'display:none !important;';
                            }
                        });
                        const stage = document.getElementById('stage');
                        if (stage) stage.style.cssText = `position:static !important; width:${w}px !important; height:${h}px !important; transform:none !important; box-shadow:none !important; border-radius:0 !important; overflow:hidden !important;`;
                        const vp = document.getElementById('viewport');
                        if (vp) vp.style.cssText = 'position:static !important; display:block !important; height:auto !important;';
                        document.documentElement.style.cssText = 'background:#fff !important; overflow:visible !important; height:auto !important;';
                        document.body.style.cssText = 'background:#fff !important; overflow:visible !important; height:auto !important; margin:0 !important; padding:0 !important;';
                    }""",
                    {"i": i, "w": width, "h": height},
                )
                page.wait_for_timeout(120)
                pdf_bytes = page.pdf(
                    print_background=True,
                    width=f"{width}px",
                    height=f"{height}px",
                    margin={"top": "0px", "right": "0px", "bottom": "0px", "left": "0px"},
                    scale=1.0,
                )
                (tmpdir / f"page_{i:03d}.pdf").write_bytes(pdf_bytes)
                if not quiet and ((i + 1) % 5 == 0 or i + 1 == total):
                    log(f"    rendered {i + 1}/{total}")

            browser.close()

        # Merge into single PDF with clean Pages tree
        writer = PdfWriter()
        for i in range(total):
            reader = PdfReader(str(tmpdir / f"page_{i:03d}.pdf"))
            for pg in reader.pages:
                writer.add_page(pg)
        with out.open("wb") as f:
            writer.write(f)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

    if verify:
        from PyPDF2 import PdfReader
        final = PdfReader(str(out))
        actual = len(final.pages)
        if actual != total:
            sys.stderr.write(
                f"⚠️  Page count mismatch: rendered {total} but PDF has {actual}\n"
            )
            return actual
        sizes = {(float(p.mediabox.width), float(p.mediabox.height)) for p in final.pages}
        log(f"✓ verified: {actual} pages, sizes {sizes}")

    log(f"✓ output: {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out} ({out.stat().st_size:,} bytes)")
    return total


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("inputs", nargs="+", help="HTML 파일 경로 (글롭 지원)")
    parser.add_argument("--output", "-o", help="출력 PDF 경로 (단일 입력 시에만)")
    parser.add_argument("--width", type=int, default=1280, help="슬라이드 가로 px (기본 1280)")
    parser.add_argument("--height", type=int, default=720, help="슬라이드 세로 px (기본 720)")
    parser.add_argument("--quiet", "-q", action="store_true", help="진행 메시지 숨김")
    parser.add_argument("--no-verify", action="store_true", help="PyPDF2 검증 스킵")
    args = parser.parse_args()

    # Expand globs
    files: list[Path] = []
    for pattern in args.inputs:
        matched = glob.glob(pattern)
        if matched:
            files.extend(Path(m) for m in matched)
        else:
            files.append(Path(pattern))

    if not files:
        sys.stderr.write("❌ No input files matched.\n")
        return 2

    if args.output and len(files) > 1:
        sys.stderr.write("❌ --output is only valid with a single input.\n")
        return 2

    rc = 0
    for src in files:
        if args.output:
            out = Path(args.output)
        else:
            out = src.with_suffix(".pdf")
        try:
            convert(
                src=src,
                out=out,
                width=args.width,
                height=args.height,
                quiet=args.quiet,
                verify=not args.no_verify,
            )
        except SystemExit:
            raise
        except Exception as e:
            sys.stderr.write(f"❌ Failed: {src}: {e}\n")
            rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main())
