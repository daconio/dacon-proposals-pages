#!/usr/bin/env python3
"""
HTML slide → PDF converter (native Chromium PDF, no screenshot)

Usage:
  python3 scripts/html2pdf.py                          # all slide HTMLs
  python3 scripts/html2pdf.py 제안/some-file.html      # single file
"""

import asyncio, sys, os, subprocess

# 16:9 in mm (matches 960x540pt)
PAGE_W_MM = 338.667  # 960pt * 25.4/72
PAGE_H_MM = 190.5    # 540pt * 25.4/72

async def convert(html_path):
    from playwright.async_api import async_playwright

    pdf_path = html_path.rsplit('.html', 1)[0] + '.pdf'
    basename = os.path.basename(html_path)
    abs_path = os.path.abspath(html_path)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1280, 'height': 720})
        await page.goto(f'file://{abs_path}', wait_until='networkidle')
        await page.wait_for_timeout(2000)

        await page.evaluate('''() => {
            // Reset html/body to fill page with no margin
            document.documentElement.style.cssText = "width:100%;height:auto;overflow:visible;background:#fff;margin:0;padding:0";
            document.body.style.cssText = "width:100%;height:auto;overflow:visible;background:#fff;margin:0;padding:0";

            // Reset viewport/stage to flow layout, full width
            const vp = document.getElementById("viewport");
            const st = document.getElementById("stage");
            if (vp) vp.style.cssText = "position:static;display:block;width:100%;height:auto";
            if (st) st.style.cssText = "position:static;width:100%;height:auto;overflow:visible;transform:none;box-shadow:none;border-radius:0";

            // Force all slides visible, full width/height of page
            document.querySelectorAll(".slide").forEach(s => {
                s.style.cssText = "position:relative;inset:auto;opacity:1;pointer-events:auto;width:100%;height:100vh;page-break-after:always;overflow:hidden;display:flex;flex-direction:column";
            });
            const slides = document.querySelectorAll(".slide");
            if (slides.length) slides[slides.length-1].style.pageBreakAfter = "auto";

            // Reveal all data-step fragments
            document.querySelectorAll("[data-step]").forEach(el => {
                el.style.opacity = "1";
                el.style.transform = "none";
            });

            // Hide navigation elements
            document.querySelectorAll(".nav-btn, #progress-bar, #key-hint").forEach(n => {
                n.style.display = "none";
            });
        }''')

        await page.pdf(
            path=pdf_path,
            width=f'{PAGE_W_MM}mm',
            height=f'{PAGE_H_MM}mm',
            margin={'top': '0mm', 'right': '0mm', 'bottom': '0mm', 'left': '0mm'},
            print_background=True,
            prefer_css_page_size=False,
        )

        await browser.close()

        # Verify
        with open(pdf_path, 'rb') as f:
            import re
            content = f.read().decode('latin-1')
            boxes = re.findall(r'/MediaBox\s*\[\s*([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*\]', content)
            if boxes:
                w, h = float(boxes[0][2]), float(boxes[0][3])
                ratio = w / h if h else 0
                print(f'  OK  {basename} → {w:.0f}x{h:.0f}pt (ratio {ratio:.3f})')
            else:
                print(f'  OK  {basename} → done')

async def main():
    if len(sys.argv) > 1:
        files = [sys.argv[1]]
    else:
        result = subprocess.run(
            ['grep', '-rl', 'class="slide"', '--include=*.html', '제안/', '내부/', '전략/'],
            capture_output=True, text=True, cwd=os.getcwd()
        )
        files = [f for f in result.stdout.strip().split('\n')
                 if f and 'NIA' not in f and 'jd-html' not in f]
        files.sort()

    print(f'Converting {len(files)} files (native PDF, 16:9)\n')

    for f in files:
        try:
            await convert(f)
        except Exception as e:
            print(f'  ERR {os.path.basename(f)}: {e}')

    print(f'\nDone!')

asyncio.run(main())
