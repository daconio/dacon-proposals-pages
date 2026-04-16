#!/usr/bin/env python3
"""
HTML slide → PDF converter (screenshot per slide, no color loss)

Usage:
  python3 scripts/html2pdf.py                          # all slide HTMLs
  python3 scripts/html2pdf.py 제안/some-file.html      # single file
"""

import asyncio, sys, os, subprocess

# 16:9 PDF page in points
PAGE_W = 960.0
PAGE_H = 540.0

async def convert(html_path):
    from playwright.async_api import async_playwright
    from reportlab.pdfgen import canvas

    pdf_path = html_path.rsplit('.html', 1)[0] + '.pdf'
    basename = os.path.basename(html_path)
    abs_path = os.path.abspath(html_path)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        # 2x retina — high-res for Figma import
        page = await browser.new_page(
            viewport={'width': 1280, 'height': 720},
            device_scale_factor=2
        )

        await page.goto(f'file://{abs_path}', wait_until='networkidle')
        await page.wait_for_timeout(2000)

        n = await page.evaluate('document.querySelectorAll(".slide").length')

        imgs = []
        for i in range(n):
            await page.evaluate(f'''() => {{
                const slides = document.querySelectorAll(".slide");
                slides.forEach((s, idx) => s.classList.toggle("active", idx === {i}));
                const active = slides[{i}];
                active.querySelectorAll("[data-step]").forEach(el => {{
                    el.style.opacity = "1";
                    el.style.transform = "none";
                }});
                document.querySelectorAll(".nav-btn, #progress-bar, #key-hint").forEach(x => x.style.display = "none");
            }}''')
            await page.wait_for_timeout(150)
            img_path = f'/tmp/_pdf_{os.getpid()}_{i:03d}.png'
            await page.screenshot(path=img_path, full_page=False)
            imgs.append(img_path)

        await browser.close()

        c = canvas.Canvas(pdf_path, pagesize=(PAGE_W, PAGE_H))
        for idx, img in enumerate(imgs):
            if idx > 0:
                c.showPage()
            c.drawImage(img, 0, 0, width=PAGE_W, height=PAGE_H)
        c.save()

        for img in imgs:
            os.remove(img)

        print(f'  OK  {basename} → {n} slides ({PAGE_W:.0f}x{PAGE_H:.0f}pt)')

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

    print(f'Converting {len(files)} files\n')

    for f in files:
        try:
            await convert(f)
        except Exception as e:
            print(f'  ERR {os.path.basename(f)}: {e}')

    print(f'\nDone!')

asyncio.run(main())
