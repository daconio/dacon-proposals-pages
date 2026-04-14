# Product Spec: hwp-organizer End-to-End Test

## Goal
`~/.claude/skills/hwp-organizer/` 스킬이 실제 한글 HWPX 파일을 완전하게 처리할 수 있는지 end-to-end로 검증한다. 발견되는 모든 버그를 수정해 스킬을 production-ready 상태로 만든다.

## Target File
`/Users/kookjinkim/Downloads/[데이콘] 제5회 ETRI 휴먼이해 인공지능 논문경진대회 개최 및 운영 제안서.hwpx` (16MB)

## Success Criteria
1. **환경 준비**: pyhwpx, python-hwp5, beautifulsoup4, lxml 설치 완료 확인
2. **추출 성공**: intermediate JSON 생성 (blocks 수 > 10)
3. **정돈 성공**: 헤딩 계층과 TOC 생성
4. **MD 생성**: `{stem}.cleaned.md` — YAML frontmatter + 본문 포함
5. **HTML 생성**: `{stem}.cleaned.html` — A4 portrait CSS 임베드, 브라우저 렌더 가능
6. **HWPX 재작성**: 시도. 실패는 비치명적 — 성공하면 가점
7. **버그 수정**: 파이프라인 중 실패하는 지점이 발견되면 즉시 스크립트 수정 후 재실행
8. **최종 산출물 검증**: MD/HTML 파일 육안 확인으로 제목·본문·표가 의미 있게 보존되어야 함

## Out of Scope
- 완벽한 헤딩 재현 (휴리스틱 한계 인정)
- 복잡한 수식/각주 완벽 보존
- 자동 테스트 스크립트 작성
