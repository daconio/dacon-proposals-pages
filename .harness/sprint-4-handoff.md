# Sprint 4 Handoff (Final)

Sprint 4 Status: PASS (100%, attempt 1)
Commit: 4ecb682

## Cumulative Changes

| 파일 | 스프린트 | 작업 |
|------|---------|------|
| 사후리포트/data/schema.json | 1 | Created |
| 사후리포트/data/sample-hackathon.json | 1 | Created |
| 사후리포트/data/sample-edu.json | 1 | Created |
| 사후리포트/report-template.html | 2/3 | Created + script integration |
| 사후리포트/js/renderer.js | 3 | Created (10 renderers + inline data hook) |
| 사후리포트/index.html | 4 | Created (entry, 사용법, 파일명 규칙) |
| 사후리포트/demo-hackathon.html | 4 | Created (inline JSON, file:// safe) |
| 사후리포트/demo-edu.html | 4 | Created (inline JSON, file:// safe) |

## Final Working State

- 단일 폴더 정적 산출물 시스템 (`사후리포트/`) 완성
- 데이터 스키마 + 2개 샘플 + 동적 렌더러 + 자급자족 데모 모두 동작
- file:// 직접 더블클릭 → 두 데모 정상 렌더 (DOM `data-report-ready="1"` 확인)
- Chrome headless print-to-pdf 검증: hack.pdf 982KB/11p, edu.pdf 946KB/10p
- A4 인쇄 레이아웃: 커버 1페이지 / 섹션 page-break-before / 카드 page-break-inside avoid
- 금지 문구 0건 (전체 산출물)

## Known Limitations

- 인쇄 미리보기 시각적 검증은 headless PDF 생성으로 대체. 페이지 수가 합리적이고 page-break CSS 규칙이 적용되어 있으나, 사람 눈으로 카드 잘림을 100% 확신하려면 실제 Chrome 미리보기 확인 권장.
- file://에서 fetch가 막힐 수 있으나 데모 파일은 인라인 데이터를 사용하므로 영향 없음. 새 행사 데이터 추가 시 인라인으로 임베드하거나 http server에서 `?data=` 사용.
