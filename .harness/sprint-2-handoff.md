# Sprint 2 → Sprint 3 Handoff

Sprint 2 Status: PASS (100%, attempt 1)
Commit: 95cecb3

## Cumulative Changes

| 파일 | 스프린트 | 작업 |
|------|---------|------|
| 사후리포트/data/schema.json | 1 | Created |
| 사후리포트/data/sample-hackathon.json | 1 | Created |
| 사후리포트/data/sample-edu.json | 1 | Created |
| 사후리포트/report-template.html | 2 | Created (1024 lines, placeholder content + A4 print CSS) |

## Current State (Working)

- 데이터 스키마 + 2개 샘플 JSON 완료
- A4 portrait 인쇄 레이아웃 (`@page` 15mm margin)
- `print-color-adjust: exact` `:root` + `body`
- 디자인 토큰 6개 모두 기존 프로젝트와 동일 값
- 섹션 page-break 규칙, 카드 page-break-inside avoid
- `@media screen .a4-page` 카드 미리보기
- 10개 placeholder 섹션 (커버~명단) 하드코딩
- 콘솔 에러 가능성 0 (script 없음, 중복 id 없음)

## Not Yet Implemented

- JS 렌더러 (`사후리포트/js/renderer.js`)
- 동적 데이터 바인딩
- 데모 진입점 + 인라인 데이터 데모

## Next Sprint (Sprint 3): 섹션별 렌더링 컴포넌트 구현

Scope:
- `사후리포트/js/renderer.js` 신규
- `report-template.html` 업데이트하여 JS 통합 + placeholder를 렌더러 타겟 DOM으로 교체
- 9개 섹션 렌더러: renderCover, renderTableOfContents, renderOverview, renderStats, renderTimeline, renderHighlights, renderEvaluation, renderRetrospective, renderTeamCards, renderParticipants
- `async function loadReport(jsonPath)` — fetch → JSON.parse → 렌더 파이프라인
- 점수 합산 + 순위 계산 로직
- 빈 필드 숨김 처리 (`style.display='none'` or `hidden`) 2건 이상
- 금지 문구 0건 유지

## Notes for Sprint 3 Generator

- 데이터 구조는 `사후리포트/data/schema.json` 참조
- 샘플 데이터의 실제 필드명 확인: `event.name`, `event.date`, `teams[].members`, `teams[].output`, `evaluation.criteria[].teamScores[{teamId, score}]`, `retrospective[].category` 등
- 기존 placeholder DOM은 명확한 클래스명을 가짐 (`.cover`, `.report-section`, `.team-card` 등) — 렌더러 타겟으로 활용 가능
- file:// 프로토콜에서 fetch가 막힐 수 있으나 Sprint 3는 fetch 기반으로 충분 (Sprint 4에서 인라인 데이터 데모 작성)
- CR-3.5: `renderer.js`와 `report-template.html`에서 "견적/예산/비용/가격/패키지/스킬 리포트" 문자열 0건 유지
