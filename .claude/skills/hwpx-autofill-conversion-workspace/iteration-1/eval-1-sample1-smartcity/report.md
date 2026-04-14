# eval-1: 샘플양식1 → 스마트시티 감리용역 제안요청서

## Verification
- XML valid: **True**
- Mimetype first entry, STORED: **True**
- Table count: src=13 / dst=13 (**match**)
- Text nodes (non-empty): 104 (same as template)
- Output size: 63,010 bytes

## What changed
- Title/date block → "2028 회계연도", 스마트시티 통합관제센터 감리용역 제안요청서, 2026.5.12.
- Info box (부서/담당/연락처): labels preserved, dept → 스마트도시본부/도시인프라부, contacts → 박민수 차장·최영희 과장 with new phones
- Chapter markers (Ⅰ~Ⅵ) and chapter titles preserved
- All placeholder heading/body text (□/○/-/※) replaced with smart-city content across 6 chapters
- Schedule table (6x3) cells replaced with actual procurement timeline

## Preserved
- All 11 `<hp:tbl>` tables with layout
- BinData logo, header.xml, secpr master page
- Structural labels (목차, 부서/담당/연락처, 장 번호·제목)

## Notes
- Slot [54] "NT" fragment left as-is (visible in inspect output)
- 견적/예산 섹션 없음 (제안서 규정 준수)
- 반복 머리말 "2027년 회계연도 제안 요청서" 은 secpr 내부 — slot 모드 범위 밖. 필요 시 수동 편집.

## Verdict
**PASS** — 104 slots filled correctly, valid HWPX, all tables preserved.
