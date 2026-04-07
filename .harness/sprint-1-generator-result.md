# Sprint 1 — Generator Result

Attempt: 1
Timestamp: 2026-04-07T12:00:00+09:00

## Implementation Summary

| 파일 경로 | 작업 | 설명 |
|----------|------|------|
| 사후리포트/data/schema.json | Created | DAKER 사후리포트 전체 데이터 구조(JSON Schema Draft-07) 정의. eventType, event, overview, stats, timeline, teams, participants, highlights, evaluation, retrospective 9개 루트 필드 명시 |
| 사후리포트/data/sample-hackathon.json | Created | 2026 금융보안원 AI 바이브코딩 해커톤 샘플 데이터. eventType=hackathon, 팀 5개, 참가자 32명, 타임라인 8항목, 평가 4기준, 회고 6항목(성과/개선/제안) |
| 사후리포트/data/sample-edu.json | Created | 2026 단국대학교 바이브코딩 집중 부트캠프 샘플 데이터. eventType=education, 팀 4개, 참가자 24명, 타임라인 8항목, 학습 성취 기반 평가/회고 |

## Self-Check

Contract 기준 자가 점검 결과:

| 항목 ID | 항목명 | 결과 | 비고 |
|--------|--------|------|------|
| CR-1.1 | eventType 필드 존재 | PASS | hackathon 샘플은 "hackathon", edu 샘플은 "education" 값으로 최상위에 존재 |
| CR-1.2 | 팀 데이터 필수 필드 | PASS | 두 샘플의 모든 team 항목이 id/name/rank/score/highlight/members/output 전부 포함. Python 검증 스크립트로 확인 |
| CR-1.3 | 참가자 30명 이상 | PASS | sample-hackathon.json participants 길이 = 32 |
| CR-1.4 | 타임라인 8항목 이상 | PASS | sample-hackathon.json timeline 길이 = 8, 각 항목에 date/time/label/description 포함 |
| CR-1.5 | 평가 데이터 구조 | PASS | evaluation.criteria 각 항목에 criterion/maxScore/teamScores(팀ID-점수 매핑) 포함 |
| CR-1.6 | 회고 데이터 카테고리 | PASS | 두 샘플 모두 성과/개선/제안 세 카테고리가 각 2개씩, 총 6항목 |
| RV-1.1 | JSON 유효성 — 해커톤 샘플 | PASS | `python3 -m json.tool 사후리포트/data/sample-hackathon.json` 정상 실행, "hackathon OK" 출력 |
| RV-1.2 | JSON 유효성 — 교육 샘플 | PASS | `python3 -m json.tool 사후리포트/data/sample-edu.json` 정상 실행, "edu OK" 출력 |
| RV-1.3 | 참가자 수 확인 | PASS | `python3 -c ...len(d['participants'])` 결과 = 32 (30 이상) |

추가: 금지 문구 검사(견적/예산/비용/패키지/스킬 리포트) 3개 파일 전체에서 0건 확인.

## Known Limitations

- 스키마 파일은 JSON Schema Draft-07 형식이며, 이후 스프린트에서 프로그래밍적으로 검증(ajv 등)하지는 않는다. Generator/Evaluator는 이 문서를 데이터 계약의 단일 참조점으로 사용한다.
- `highlights` 배열은 스키마에 정의되어 있으나 Sprint 1 Contract에는 직접 검증 항목이 없어, 실제 렌더러(Sprint 3)에서 사용될 때 재확인이 필요하다.
- 샘플 데이터는 가공된 현실감 있는 가상 사례이며 실제 행사 결과가 아니다.

## Git Commit

```
Sprint 1: add 사후리포트 data schema and sample JSON data

- Define full JSON schema for DAKER post-event report
- Add hackathon sample (32 participants, 5 teams, 8 timeline items)
- Add education bootcamp sample (24 participants, 4 teams, 8 timeline items)
- Cover event metadata, stats, timeline, teams, evaluation, retrospective
```

Commit Hash: 22f657b
