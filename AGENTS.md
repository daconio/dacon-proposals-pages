# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## Repository Purpose

This is a **proposal and presentation document repository** for DAKER (데이커). It contains business proposals, slide presentations, and research documents targeting organizations like 금융보안원, 단국대학교, 대동그룹, and others. Topics focus on AI competitions, vibe coding (바이브코딩), and organizational transformation.

## Document Workflow

Each proposal follows a **Markdown-first workflow**:
1. Write content in `.md` (Markdown source of truth)
2. Generate a standalone `.html` slide presentation from the Markdown
3. Optionally export to `.pdf` for distribution

File naming convention: `YYYY-MM-DD-{대상}_{주제}.{md,html,pdf}`

## HTML Slide Architecture

All HTML presentations are **single-file, self-contained slide decks** (no external dependencies beyond Google Fonts). Key patterns:

- **Viewport scaling**: A `#viewport` + `#stage` container with fixed dimensions (`--slide-w: 1280px; --slide-h: 720px`) scaled via `transform: scale()` to fit the browser window
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
