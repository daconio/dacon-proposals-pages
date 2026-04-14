# Sprint 1 Generator Result

## Environment
- Python: `/usr/local/bin/python3.13` (Python 3.13.12). Default `python3` is 3.14, which has no working pyhwpx/pyhwp wheels — used 3.13 explicitly.
- pyhwpx: **NOT installable on macOS**. `pip install pyhwpx` fails with `RuntimeError: pyhwpx는 Windows에서만 동작합니다.` (the package's own setup.py refuses to build on non-Windows hosts).
- python-hwp5: not on PyPI under that name; installed `pyhwp 0.1b15` instead which provides `hwp5html`. Useful only for legacy `.hwp`, not `.hwpx`.
- beautifulsoup4 4.14.3 + lxml 6.0.2 installed via `--user --break-system-packages`.
- Platform: macOS (Darwin 25.3.0, arm64).

## Execution Log
1. Read `SKILL.md` and all 6 scripts under `~/.claude/skills/hwp-organizer/scripts/`.
2. Probed Python env — 3.14 default lacked everything; switched to 3.13.
3. `python3.13 -m pip install --user --break-system-packages pyhwpx beautifulsoup4 lxml` → pyhwpx build aborted (Windows only). Installed bs4/lxml only. Also installed `pyhwp` (provides `hwp5html`) but it does not handle `.hwpx`.
4. Inspected the target HWPX with stdlib `zipfile` — confirmed standard layout: `Contents/section0.xml`, `BinData/image*.png`, etc.
5. Added a pure-Python HWPX zip+lxml fallback (`extract_hwpx_zip`) to `extract_hwp.py` and wired it into `main()` after the pyhwpx attempt.
6. Ran `convert.py` end-to-end:
   - `extract_hwp.py`: pyhwpx import failed → hwpx-zip fallback succeeded, dumped 24 images.
   - `organize.py`: produced 141 blocks, 16 headings.
   - `build_md.py`: 38 KB MD with frontmatter, TOC, headings, GFM tables, image refs.
   - `build_html.py`: 48 KB HTML with `@page A4 portrait` and embedded CSS.
   - `build_hwpx.py`: failed cleanly (pyhwpx unavailable) — non-fatal as designed.
7. Verified outputs (sizes, keyword grep, A4/@page markers, asset count).
8. `py_compile` on all six scripts → OK.

## Bugs Found & Fixes Applied
| File | Line(s) | Bug | Fix |
|------|---------|-----|-----|
| `scripts/extract_hwp.py` | (added ~189–305) | No working extractor on macOS — pyhwpx is Windows-only and `hwp5html` cannot read `.hwpx`. Pipeline would fail at step 1 with "all extractors failed". | Added `extract_hwpx_zip()` pure-Python fallback using `zipfile` + `lxml.etree`, parsing `Contents/section*.xml` for `<hp:p>`/`<hp:t>`/`<hp:tbl>` and dumping `BinData/*` images. |
| `scripts/extract_hwp.py` | `main()` extractor chain | Only tried pyhwpx then hwp5html. | Inserted hwpx-zip fallback between them, gated on `.hwpx` suffix. |

No other bugs encountered — `organize.py`, `build_md.py`, `build_html.py`, `convert.py` all worked unchanged once the extractor produced a valid intermediate JSON. `build_hwpx.py` requires pyhwpx and exits non-zero on macOS, but `convert.py` already treats that as non-fatal.

Note: `assets/a4-portrait.html.j2` referenced in `SKILL.md` does not exist in the skill, but `build_html.py` does not actually use Jinja2 — it embeds CSS via `FALLBACK_CSS` or `assets/a4-portrait.css`. The doc/code mismatch is cosmetic; HTML output is fine. Left untouched per "minimal targeted edits" rule.

## Implementation Summary
| File | Change |
|------|--------|
| `scripts/extract_hwp.py` | Added `HP_NS` constant + `extract_hwpx_zip(src, images_dir)` function (pure-Python HWPX parser). Wired into `main()` between the pyhwpx attempt and the `hwp5html` fallback. |

Total diff scope: 1 file, ~125 added lines, 0 deleted, 0 refactored. No other skill files modified.

## Output Verification
- MD file: `/Users/kookjinkim/code/제안서/.harness/hwp-organizer-test/output/[데이콘] 제5회 ETRI 휴먼이해 인공지능 논문경진대회 개최 및 운영 제안서.cleaned.md`
  - size: **38,350 bytes**
  - heading count (`^##`): **17** (incl. `## 목차`)
  - YAML frontmatter present (title/source/generated_at)
  - TOC present (`## 목차` with 16 entries)
- HTML file: `/Users/kookjinkim/code/제안서/.harness/hwp-organizer-test/output/[데이콘] 제5회 ETRI 휴먼이해 인공지능 논문경진대회 개최 및 운영 제안서.cleaned.html`
  - size: **48,131 bytes**
  - contains `@page`: **yes** (1 occurrence)
  - contains `A4`: **yes** (2 occurrences, including `size: A4 portrait`)
- Extracted images: **24** PNGs in `[데이콘] 제5회 ETRI 휴먼이해 인공지능 논문경진대회 개최 및 운영 제안서.assets/` (image1.png … image24.png)
- HWPX rewrite: **failed** — pyhwpx is Windows-only and refuses to install on macOS. Convert.py reports `FAILED (MD/HTML still produced)` as designed.
- Intermediate kept: `[…].intermediate.json` (55,764 bytes, 141 blocks, 16 headings).
- Keywords found in MD: **ETRI, 휴먼이해, 논문, 데이콘** (all 4 of 4 target keywords).

## Self-Check
- [x] convert.py exited 0 (or MD/HTML produced despite HWPX failure) — MD/HTML produced; HWPX failure is non-fatal in convert.py
- [x] MD > 200 bytes (38,350)
- [x] HTML > 2KB (48,131)
- [x] MD has frontmatter
- [x] MD has TOC and ≥3 headings (17)
- [x] At least 2 target keywords in MD (4/4)
- [x] HTML has @page + A4
- [x] All modified Python scripts pass py_compile
