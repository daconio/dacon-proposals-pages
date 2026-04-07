# Sprint 3 → Sprint 4 Handoff

Sprint 3 Status: PASS (100%, attempt 1)
Commit: cd9f009

## Cumulative Changes

| 파일 | 스프린트 | 작업 |
|------|---------|------|
| 사후리포트/data/schema.json | 1 | Created |
| 사후리포트/data/sample-hackathon.json | 1 | Created |
| 사후리포트/data/sample-edu.json | 1 | Created |
| 사후리포트/report-template.html | 2/3 | Created (S2) + script tag 추가 (S3) |
| 사후리포트/js/renderer.js | 3 | Created (~440 lines) |

## Current State (Working)

- 데이터 + 템플릿 + 동적 렌더러 통합 완료
- `loadReport(jsonPath)` async 파이프라인 (fetch → JSON.parse → renderAll)
- 10개 섹션 렌더러 함수 모두 동작 (Cover/TOC/Overview/Stats/Timeline/Highlights/Evaluation/Retrospective/TeamCards/Participants)
- `computeTeamRanks` — evaluation.criteria.teamScores 합산 → 정렬 → 순위 부여
- 빈 필드 5개 분기 처리 (display=none / hidden)
- 쿼리스트링 `?data=...` 지원, 기본값 `./data/sample-hackathon.json`
- `<script type="application/json" id="report-data">` 인라인 데이터 훅 이미 준비됨 (Sprint 4용)
- python3 http.server + headless chrome 검증: 두 샘플 모두 정상 렌더, `data-report-ready="1"` 설정
- 금지 문구 0건

## Not Yet Implemented

- `사후리포트/index.html` 데모 진입점
- `사후리포트/demo-hackathon.html` (인라인 데이터)
- `사후리포트/demo-edu.html` (인라인 데이터)
- 사용법/인쇄 안내, 파일명 규칙 명시

## Next Sprint (Sprint 4): 데모 완성 및 인쇄·PDF 출력 검증

Scope:
- `사후리포트/index.html` — 사용법 안내 + 두 데모 링크
- `사후리포트/demo-hackathon.html`, `사후리포트/demo-edu.html` — 인라인 JSON 포함 자급자족 리포트
- `<script type="application/json" id="report-data">` 또는 JS 변수로 샘플 데이터 인라인
- index.html에 "Ctrl+P → PDF로 저장" 한국어 안내
- 파일명 규칙 `YYYY-MM-DD-{고객사}_{행사명}_사후리포트.html` 명시
- 모든 산출물에서 금지 문구 0건 유지

## Notes for Sprint 4 Generator

- renderer.js의 inline data hook은 이미 구현됨 — `<script type="application/json" id="report-data">{...JSON...}</script>` 패턴 사용
- 데모 파일은 `report-template.html`을 복제 후 `<script src="./js/renderer.js">` 대신 인라인 데이터+스크립트 방식 또는 동일한 src + 인라인 데이터 hook 모두 가능
- file:// 프로토콜에서도 동작해야 함 (fetch 사용 금지, 인라인 우선)
- 인쇄 미리보기에서 커버 1페이지/섹션 페이지 시작/카드 잘림 없음 확인 필요 (RV-4.3)
- `index.html`은 단순 HTML 페이지 (리포트 UI 아님), 사용법·링크만
