# Sprints

Total Sprints: 1

## Sprint 1: hwp-organizer end-to-end 검증 및 버그 수정

### Scope
실제 HWPX 파일(`/Users/kookjinkim/Downloads/[데이콘] 제5회 ETRI 휴먼이해 인공지능 논문경진대회 개최 및 운영 제안서.hwpx`)을 `~/.claude/skills/hwp-organizer/scripts/convert.py` 파이프라인에 넣고 MD/HTML/HWPX 산출물을 만든다. 실패하는 지점이 있으면 스크립트를 직접 수정한 뒤 성공할 때까지 반복한다.

### Deliverables
1. `/Users/kookjinkim/code/제안서/.harness/hwp-organizer-test/output/` 디렉토리에 저장된 산출물:
   - `*.cleaned.md`
   - `*.cleaned.html`
   - `*.cleaned.hwpx` (가능한 경우)
   - `*.assets/` (추출된 이미지, 있는 경우)
   - `*.intermediate.json` (디버깅용, `--keep-intermediate` 사용)
2. 수정된 `~/.claude/skills/hwp-organizer/scripts/*.py` (버그 수정이 있었다면)
3. `.harness/hwp-organizer-test/sprint-1-generator-result.md` — 실행 로그, 수정 내역, 검증 체크리스트

### Contract (Evaluator가 확인할 기준)

**T (Task completion) — 40점**
- [ ] `convert.py` 실행이 최종적으로 성공 exit code 0 또는 "MD/HTML produced" 로 종료
- [ ] 출력 디렉토리에 `.cleaned.md` 파일 존재 및 크기 > 200 bytes
- [ ] 출력 디렉토리에 `.cleaned.html` 파일 존재 및 크기 > 2KB
- [ ] MD 파일에 YAML frontmatter(`---` ... `---`)가 존재
- [ ] MD 파일에 `## 목차` 섹션이 존재하거나, 본문 헤딩이 최소 3개 이상 존재

**C (Code quality) — 30점**
- [ ] 스크립트 수정이 있었다면 python3 -m py_compile 통과
- [ ] 수정 내역이 generator-result.md에 명확히 기록됨
- [ ] 수정이 기존 로직을 완전히 재작성하지 않고 최소 변경 원칙을 따름 (휴리스틱·fallback 추가는 OK)

**Q (Output quality) — 30점**
- [ ] MD 본문에서 원본 제안서의 핵심 키워드(예: "ETRI", "휴먼이해", "논문경진대회", "데이콘")가 최소 2개 이상 등장
- [ ] HTML을 브라우저에서 열 수 있는 형태 (valid DOCTYPE, html/body 태그)
- [ ] HTML에 A4 portrait CSS (`@page`, `A4`) 가 포함됨
- [ ] 이미지가 원본에 있었다면 `*.assets/` 디렉토리에 추출되거나, 최소한 alt 텍스트로 언급됨

### Out of scope
- 완벽한 헤딩 재현 (휴리스틱 한계)
- HWPX 재작성 성공 필수 아님 (실패해도 감점 없음)
- 요약 자동 생성 (`--summary` 플래그는 이번에 사용하지 않음)
