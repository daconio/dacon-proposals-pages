# Sprint 1 Evaluator Result

## Verification Log

### Output directory listing
```
[데이콘] ... .assets/        (dir, 24 PNGs)
[데이콘] ... .cleaned.html   48,131 bytes
[데이콘] ... .cleaned.md     38,350 bytes
[데이콘] ... .intermediate.json  55,764 bytes
```
No `.cleaned.hwpx` (acceptable per contract — pyhwpx Windows-only).

### MD inspection
- Size: 38,350 bytes (>> 200)
- First line is `---` (frontmatter open) followed by `title:` / `source:` / `generated_at:` / closing `---`
- `^## ` count: **9**, `^### ` count: **8** (>= 3 headings requirement easily met)
- `## 목차` section present with TOC entries
- Keyword grep on full file:
  - ETRI: **44**
  - 휴먼이해: **32**
  - 논문: **46**
  - 데이콘: **37**
  - All 4 of 4 keywords present (>= 2 required)

### HTML inspection
- Size: 48,131 bytes (>> 2KB)
- Begins with `<!doctype html>` then `<html lang="ko">`, `<head>`, etc.
- `<!doctype`: 1, `<html`: 1, `<body`: 1
- `@page`: 1 occurrence
- `A4`: 2 occurrences (incl. `size: A4 portrait`)

### Assets
- 24 image files extracted (image1.png … image24.png) into `*.assets/`

### Script compile
```
python3 -m py_compile ~/.claude/skills/hwp-organizer/scripts/*.py
→ py_compile OK
```

### Script modification spot-check
`grep extract_hwpx_zip|HP_NS` on `extract_hwp.py`:
- Line 189: `HP_NS = "http://www.hancom.co.kr/hwpml/2011/paragraph"`
- Line 192: `def extract_hwpx_zip(src: Path, images_dir: Path) -> dict | None:`
- Lines 235–239: tag constants for `p/t/tbl/tr/tc`
- Line 413: `doc = extract_hwpx_zip(src, images_dir)` wired into `main()`
Generator's claim of a ~125-line additive change in one file matches reality. No gratuitous refactor visible.

## Score Breakdown

### T — Task completion: 40/40
- [x] convert.py produced MD/HTML (HWPX failure non-fatal as designed) — both files present and well-formed
- [x] MD exists, 38,350 bytes (> 200)
- [x] HTML exists, 48,131 bytes (> 2KB)
- [x] MD has YAML frontmatter (`---` ... `---` with title/source/generated_at)
- [x] MD has `## 목차` AND 9 H2 + 8 H3 (>= 3 headings)

### C — Code quality: 30/30
- [x] All six scripts pass `python3 -m py_compile`
- [x] Generator-result documents fixes clearly: bug table (file/lines/bug/fix), implementation summary, execution log
- [x] Minimal change: 1 file touched, ~125 added lines, 0 deleted, fallback inserted between existing extractor attempts and gated on `.hwpx` suffix

### Q — Output quality: 30/30
- [x] 4/4 target keywords (ETRI, 휴먼이해, 논문, 데이콘) present, each appearing 30+ times (>= 2 required)
- [x] HTML valid: `<!doctype html>` + `<html lang="ko">` + `<body>` all present
- [x] HTML contains `@page` (1) and `A4` (2)
- [x] 24 images extracted to `*.assets/` directory

## Overall: 100%

## Verdict: PASS

## Findings
- Generator's self-reported numbers match disk reality exactly (MD 38,350, HTML 48,131, 24 images, 4/4 keywords, py_compile clean).
- The pure-Python `extract_hwpx_zip` fallback is the right approach: pyhwpx truly is Windows-only (the package's own `setup.py` raises `RuntimeError` on non-Windows), so a stdlib `zipfile` + `lxml` parser of `Contents/section*.xml` is the minimum viable extractor on macOS. Insertion point between `pyhwpx` and `hwp5html` attempts is correct and gated on `.hwpx` suffix so legacy `.hwp` flow is undisturbed.
- MD frontmatter, TOC, headings, and image references all look clean. HTML has DOCTYPE, proper `<html lang="ko">`, `@page A4 portrait`. Browser-openable.
- Heading count of 9 H2 + 8 H3 = 17 total headings, far above the 3 minimum.
- No red flags. The Generator was honest about the HWPX rewrite failure rather than papering over it, which the contract explicitly allows ("HWPX 재작성 성공 필수 아님").

## Known Limitations
- `.cleaned.hwpx` not produced — explicitly out-of-scope per contract; pyhwpx is the only writer and it cannot install on macOS.
- The Generator noted a cosmetic doc/code mismatch (`SKILL.md` references `assets/a4-portrait.html.j2` but `build_html.py` doesn't use Jinja2). Left untouched per minimal-change rule. Acceptable for Sprint 1.
- Heuristic heading recovery is inherent to a zip-only parser without style metadata; contract explicitly excludes "완벽한 헤딩 재현".
- `--summary` flag intentionally not exercised (out of scope).
