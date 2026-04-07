# Sprint 1 — Evaluator Result

Attempt: 1
Timestamp: 2026-04-07T12:20:00+09:00

## Score

Overall: 100%

## Item Scores

| Contract Item | Score | Evidence |
|--------------|-------|----------|
| CR-1.1 — eventType 필드 존재 | 100% | `사후리포트/data/sample-hackathon.json` 최상위 `"eventType": "hackathon"`, `사후리포트/data/sample-edu.json` 최상위 `"eventType": "education"` 직접 확인 (python json.load 결과) |
| CR-1.2 — 팀 데이터 필수 필드 | 100% | 두 샘플 모두 `teams[*]` 키가 `['award','highlight','id','members','name','output','rank','score']` 로 확인됨. 요구 필드 7개(id/name/rank/score/highlight/members/output) 모두 포함 |
| CR-1.3 — 참가자 30명 이상 | 100% | `sample-hackathon.json` `len(participants) == 32` (요구치 30 이상 충족) |
| CR-1.4 — 타임라인 8항목 이상 | 100% | `sample-hackathon.json` `len(timeline) == 8`, 각 항목 키 `['date','description','icon','label','time']` — 요구 필드 date/time/label/description 모두 포함 |
| CR-1.5 — 평가 데이터 구조 | 100% | `evaluation.criteria[0]` 키 `['criterion','maxScore','teamScores','weight']` 포함. `teamScores` 샘플: `[{"teamId":"T1","score":95},...]` 팀ID-점수 매핑 확인 |
| CR-1.6 — 회고 데이터 카테고리 | 100% | `retrospective` 리스트의 `category` Counter — hackathon: {'성과':2,'개선':2,'제안':2}, edu: {'성과':2,'개선':2,'제안':2}. 세 카테고리 모두 1개 이상 충족 |
| RV-1.1 — JSON 유효성 (해커톤) | 100% | `python3 -m json.tool 사후리포트/data/sample-hackathon.json > /dev/null && echo OK` → `hackathon OK` 출력 |
| RV-1.2 — JSON 유효성 (교육) | 100% | `python3 -m json.tool 사후리포트/data/sample-edu.json > /dev/null && echo OK` → `edu OK` 출력 |
| RV-1.3 — 참가자 수 확인 | 100% | `python3 -c "import json; d=json.load(open('사후리포트/data/sample-hackathon.json')); print(len(d['participants']))"` → `32` (30 이상 충족) |

추가 검증: `사후리포트/data/` 전체에서 금지 문구(견적/예산/비용/패키지/가격/스킬 리포트) Grep 결과 0건. schema.json도 `python3 -m json.tool` 로 유효성 확인됨 (Draft-07 JSON Schema).

## Verdict

PASS

모든 필수 기준을 충족하였습니다. 9개 Contract 항목(CR-1.1~1.6, RV-1.1~1.3) 전부 2/2점. Sprint Score = 18/18 = 100% (통과 기준 90% 이상).
