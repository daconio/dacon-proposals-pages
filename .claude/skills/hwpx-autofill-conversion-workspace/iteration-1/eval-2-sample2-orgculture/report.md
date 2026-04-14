# eval-2: 샘플양식2 → 조직문화 진단 결과 보고

## Verification
- XML valid: **True**
- Mimetype first entry, STORED: **True**
- Table count: src=2 / dst=2 (**match**)
- Text nodes: 28 (same as template)
- Output size: 36,675 bytes

## What changed (28 slots)
- Title → "2027년 상반기 조직문화 진단 결과 보고"
- Subtitle → 경영기획실 조직문화팀 · 이지은 팀장
- Date → <소속부서 : 경영기획실 조직문화팀, 2027.07.20.>
- 5개 섹션 (개요/핵심결과/세부해석/개선제안/협조사항) 모두 조직문화 진단 내용으로 재작성
- 사용자가 준 3개 지표(참여도 81/의사소통 72/자율성 75) 정확히 반영
- 제안 2건(리더십 교육, 1:1 미팅) 반영
- 붙임/요약 라벨은 원본 유지

## Preserved
- 양식의 1-page summary layout
- 2 tables (appendix section)
- header.xml 전체 스타일

## Notes
- 원본의 budget slots ("00억원") 을 metric/improvement suggestions로 대체 — 사용자 요청에 예산 언급이 없고 본 저장소는 견적 금지 규칙이 있음
- 슬롯 [2]의 `<` 기호가 XML로 직렬화되며 `&lt;` 로 escape됨 — HWP 뷰어에서는 정상 렌더링

## Verdict
**PASS** — 28 slots filled on-topic, valid HWPX, tables preserved.
