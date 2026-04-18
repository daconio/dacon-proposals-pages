# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a **proposal and presentation document repository** for DAKER (데이커). It contains business proposals, slide presentations, and research documents targeting organizations like 금융보안원, 단국대학교, 대동그룹, and others. Topics focus on AI competitions, vibe coding (바이브코딩), and organizational transformation.

## Document Workflow

Each proposal follows a **Markdown-first workflow**:
1. Write content in `.md` (Markdown source of truth)
2. Generate a standalone `.html` slide presentation from the Markdown
3. Optionally export to `.pdf` for distribution

File naming convention: `YYYY-MM-DD-{대상}_{주제}.{md,html,pdf}`

### Folder structure for `제안/` (2026-04-18 이후)

`제안/` 폴더는 파일 유형별로 분리한다:

```
제안/
├── md/          # 제안서 Markdown 원본
├── html/        # 제안서 슬라이드 HTML (cards.json scan 대상)
├── *.pdf        # (선택) 배포용 PDF — 루트에 그대로 두거나 원본 디렉토리 참고
└── <케이스별 하위폴더>/  # 예: 20260416_법학전문대학원협의회/ 같은 RFP 원본 묶음
```

**생성 규칙 (이 리포에서 제안서를 만들 때 항상 적용)**:
- 새 `.md` 제안서 → **`제안/md/`** 에 저장 (예: `제안/md/2026-05-01-X_제안서.md`)
- 새 `.html` 슬라이드 → **`제안/html/`** 에 저장 (cards.json scan 자동 등록 경로)
- MD와 HTML은 **동일 base name** 유지 (하위폴더만 다름)
- 기존 `scripts/check_md_html_sync.py` 의 PAIRS 딕셔너리는 새 경로로 관리

`docs/plans/` 는 **상황형 브리핑 슬라이드·기획안** (RFP 없는 내부 덱) 용도로 계속 사용한다.

## HTML Slide Architecture

All HTML presentations are **single-file, self-contained slide decks** (no external dependencies beyond Google Fonts). Key patterns:

- **Default stage size = A4 landscape**: `--sw2: 1280px; --sh: 905px` (ratio ≈ 1.414, matches 297×210 mm). New proposals must use this size so the A4 PDF output is native (no letterbox). Legacy decks may use `--sh: 720px` (16:9 = 1.778); `scripts/make_pdf.py` auto-detects stage size and letterboxes as needed.
- **Viewport scaling**: A `#viewport` + `#stage` container with fixed dimensions scaled via `transform: scale()` to fit the browser window. The fit() JS function divisor (`vh/905`) must match `--sh`.
- **Print CSS**: `@page { size: A4 landscape; margin: 0; }` — required for direct browser print to match the stage geometry.
- **Slide transitions**: `.slide` elements positioned absolutely; `.slide.active` controls visibility. Navigation via `show(idx, dir)` or `showSlide(n)` function
- **Fragment animations**: `[data-step]` attributes for incremental reveals within a slide, toggled between `pre-visible` and `visible` classes
- **Navigation**: Arrow keys, touch swipe, and optional on-screen nav buttons (`#nav-prev`, `#nav-next`)
- **Progress bar**: `#progress-bar` element width set as percentage of slides viewed
- **Design tokens**: CSS custom properties on `:root` (`--primary`, `--surface`, `--accent-warm`, etc.) following a Material-inspired tonal palette
- **Utility classes**: Short class names for layout (`g2`-`g5` grids, `tc` two-column, `fr` flow row), cards (`c`, `c-blue`, `c-warm`), metrics (`mx`), tags (`tag`), badges (`bd`), tables (`tb`), checklists (`ck`)

## Proposal Rules

- **견적/예산/비용 섹션 작성 금지**: 제안서(md, html, pdf)에 견적서, 예산 구성, 비용 안내, 패키지 가격 등 금액이 포함된 섹션을 절대 포함하지 않는다. 견적은 별도 문서(스프레드시트 등)로 관리한다.
- **스킬 리포트 언급 금지**: 제안서에 "스킬 리포트", "스킬 리포트 기반 채용 연계" 등의 문구를 포함하지 않는다.

## Language

All document content is in **Korean**. Commit messages are in English.
