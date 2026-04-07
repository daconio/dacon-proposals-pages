# Sprint 1 → Sprint 2 Handoff

Sprint 1 Status: PASS (100%, attempt 1)
Commit: 22f657b

## Cumulative Changes

| 파일 | 스프린트 | 작업 |
|------|---------|------|
| 사후리포트/data/schema.json | 1 | Created |
| 사후리포트/data/sample-hackathon.json | 1 | Created |
| 사후리포트/data/sample-edu.json | 1 | Created |

## Current State (Working)

- 데이터 계약(JSON Schema Draft-07) 정의 완료
- 해커톤 샘플: eventType=hackathon, teams 5, participants 32, timeline 8, evaluation.criteria 4, retrospective 6 (성과/개선/제안 각 2)
- 교육 샘플: eventType=education, teams 4, participants 24, timeline 8, 학습 성취 평가/회고
- 금지 문구(견적/예산/비용/패키지/스킬 리포트) 0건

## Not Yet Implemented

- HTML 템플릿 (`사후리포트/report-template.html`)
- 디자인 토큰/A4 인쇄 CSS
- JS 렌더러
- 데모 진입점 / 인라인 데이터 데모

## Next Sprint (Sprint 2): 리포트 템플릿 시스템 및 디자인 토큰

Scope:
- `사후리포트/report-template.html` 작성
- A4 portrait `@page` 규칙, `print-color-adjust: exact`
- 디자인 토큰: `--primary: #0053db`, `--accent-warm: #c2622d`, `--surface`, `--on-surface`, `--on-surface-variant`, `--outline-variant` (기존 프로젝트와 동일 값)
- `.report-section` page-break-before, `.cover` 예외, `.team-card`/`.participant-row` page-break-inside: avoid
- `@media screen` `.a4-page` 카드 미리보기 (210mm × 297mm)
- placeholder 콘텐츠로 레이아웃 검증

## Notes for Sprint 2 Generator

- 데이터 스키마는 `사후리포트/data/schema.json` 참조 (Sprint 3에서 렌더러 매핑 시 사용)
- placeholder 값은 `sample-hackathon.json`의 실제 값(예: 행사명, 팀명)을 사용해도 무방하나, JS 통합은 Sprint 3 작업이므로 하드코딩으로 유지
- 기존 프로젝트의 슬라이드 HTML 파일들(`제안/2026-04-06-*.html`)에서 디자인 토큰 값 일관성 확인 가능
- 이 스프린트는 placeholder/하드코딩 상태가 정상. JS 없음.
