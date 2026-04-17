---
name: harness-runner
description: 장시간 자율 개발 하네스. Planner-Generator-Evaluator 3-에이전트 루프로 사용자 요청을 완전 자율 구현한다. harness, 하네스, autonomous, 자율 개발, 자율 구현, long-running, build this, build me, make this, create app, 앱 만들어, 만들어줘, 구현해줘 등의 키워드가 나오면 이 스킬을 사용할 것.
---

# Harness Runner

Short user request in, working software out.

---

## How It Works

```
User Request (1~4 sentences)
        |
        v
  ┌─────────┐
  │ Planner  │  ← product-spec.md + sprints.md 생성
  └────┬─────┘
       |
       v
  ┌──────────────────────────────────┐
  │  Sprint Loop (1 to N)            │
  │                                  │
  │  ┌───────────┐   ┌───────────┐  │
  │  │ Generator  │──▶│ Evaluator │  │  ← 독립 에이전트, 매번 새 컨텍스트
  │  └───────────┘   └─────┬─────┘  │
  │        ▲                │        │
  │        │   RETRY (<90%) │        │
  │        └────────────────┘        │
  │              PASS (>=90%)        │
  │                  │               │
  │                  ▼               │
  │          Handoff → Next Sprint   │
  └──────────────────────────────────┘
        |
        v
  Final Report
```

---

## Execution Protocol

이 문서를 읽는 오케스트레이터(Codex)는 아래 단계를 순서대로 실행한다.

---

### Phase 1: Setup & Planning

#### Step 1 — 사용자 요청 파악

ARGUMENTS에서 사용자의 요청을 읽는다. 이것이 전체 하네스의 입력이다.

#### Step 2 — `.harness/` 디렉토리 생성

```
Bash: mkdir -p .harness
```

#### Step 3 — 프로젝트 컨텍스트 탐색

병렬로 다음을 실행한다:

- `Glob("**/package.json", depth=2)` 또는 동등한 프로젝트 설정 파일 탐색
- `Bash: git log --oneline -10`
- 주요 소스 파일 2~3개 Read (README.md, 진입점 등)

#### Step 4 — Planner 프롬프트 로드

```
Read: .Codex/skills/harness-runner/references/planner-prompt.md
```

파일 전체 내용을 변수 `PLANNER_PROMPT`에 저장한다.

#### Step 5 — Planner 에이전트 실행

```
Agent(
  description: "Planner — 사용자 요청을 스프린트 계획으로 변환",
  model: sonnet,
  prompt: <<EOF
{PLANNER_PROMPT 전체 내용}

---

## User Request

{사용자의 원본 요청}

## Project Context

{Step 3에서 수집한 컨텍스트: package.json 내용, git log, 디렉토리 구조 등}
EOF
)
```

Planner가 완료되면 `.harness/product-spec.md`와 `.harness/sprints.md`가 생성된다.

#### Step 6 — 스프린트 계획 확인

```
Read: .harness/sprints.md
```

`Total Sprints: {N}` 라인에서 총 스프린트 수 N을 추출한다.
각 스프린트의 이름을 파싱한다.

#### Step 7 — 사용자에게 계획 출력

```
━━━ harness-runner ━━━
Plan: {N} Sprints ({Sprint 1 이름}, {Sprint 2 이름}, ...)
━━━━━━━━━━━━━━━━━━━━━
```

---

### Phase 2: Sprint Loop

스프린트 1부터 N까지 순차적으로 실행한다.

각 스프린트 시작 시:
- `attempt = 1`
- `previousScore = -1`

#### RETRY LOOP 시작

##### Step 8 — Generator 프롬프트 로드

```
Read: .Codex/skills/harness-runner/references/generator-prompt.md
```

파일 전체 내용을 변수 `GENERATOR_PROMPT`에 저장한다.

##### Step 9 — Generator 에이전트 실행

매번 새로운 에이전트를 생성한다 (컨텍스트 리셋).

```
Agent(
  description: "Generator — Sprint {currentSprint}/{totalSprints} 구현 (attempt {attempt})",
  model: opus,
  mode: bypassPermissions,
  prompt: <<EOF
{GENERATOR_PROMPT 전체 내용}

---

## Sprint Assignment

Sprint Number: {currentSprint}
Total Sprints: {totalSprints}
Attempt: {attempt}

{attempt > 1인 경우 추가:}
## Retry Context
이전 Evaluator 피드백이 .harness/sprint-{currentSprint}-eval-result.md에 있습니다.
반드시 읽고 피드백에 지적된 항목만 수정하세요.
EOF
)
```

> **bypassPermissions**: Generator는 파일 생성/수정/삭제, 패키지 설치, 빌드/테스트 실행 등 자율적으로 수행한다.

##### Step 10 — Evaluator 프롬프트 로드

```
Read: .Codex/skills/harness-runner/references/evaluator-prompt.md
```

파일 전체 내용을 변수 `EVALUATOR_PROMPT`에 저장한다.

##### Step 11 — Evaluator 에이전트 실행

Generator와 완전히 독립된 새 에이전트를 생성한다.

```
Agent(
  description: "Evaluator — Sprint {currentSprint} 평가 (attempt {attempt})",
  model: opus,
  prompt: <<EOF
{EVALUATOR_PROMPT 전체 내용}

---

## Evaluation Assignment

Sprint Number: {currentSprint}
Attempt: {attempt}

평가 대상: .harness/sprint-{currentSprint}-generator-result.md
계약 기준: .harness/sprints.md의 Sprint {currentSprint} 섹션
EOF
)
```

##### Step 12 — 평가 결과 파싱

```
Read: .harness/sprint-{currentSprint}-eval-result.md
```

다음 두 값을 추출한다:
- **Score**: `Overall: {0~100}%` 라인에서 정수값
- **Verdict**: `PASS` 또는 `RETRY`

##### Step 13 — 판정 로직

**Case A: PASS (Score >= 90%)**

1. Handoff 파일 작성 (아래 "Handoff File Compilation" 참조)
2. 진행 상황 출력:
   ```
   ┃ Sprint {currentSprint}/{totalSprints} ✓ {스프린트 이름} — {score}% (attempt {attempt})
   ```
3. RETRY LOOP 탈출 → 다음 스프린트로 진행

**Case B: RETRY (Score < 90%)**

수렴 여부를 확인한다: `|currentScore - previousScore| <= 2`

- **수렴됨 (converged)**:
  1. `.harness/known-issues.md`에 수렴 실패 항목 추가 (`references/handoff-schema.md` 섹션 6 형식)
  2. Handoff 파일 작성
  3. 진행 상황 출력:
     ```
     ┃ Sprint {currentSprint}/{totalSprints} ◆ {스프린트 이름} — CONVERGED at {score}% (attempt {attempt})
     ```
  4. RETRY LOOP 탈출 → 다음 스프린트로 진행

- **수렴되지 않음 (not converged)**:
  1. `previousScore = currentScore`
  2. `attempt++`
  3. RETRY LOOP 계속 (Step 8로 돌아감)

#### RETRY LOOP 종료

---

### Phase 3: Final Report

##### Step 14 — 최종 리포트 작성

모든 스프린트 완료 후, 다음 파일들을 읽어 `.harness/final-report.md`를 작성한다 (`references/handoff-schema.md` 섹션 7 형식):

- 모든 `sprint-{N}-handoff.md` — 누적 변경사항
- 모든 `sprint-{N}-eval-result.md` — 스프린트별 최종 점수
- `known-issues.md` — 수렴 실패 항목 (존재 시)

##### Step 15 — 최종 요약 출력

```
━━━ harness-runner 완료 ━━━
총 스프린트: {N}
총 시도 횟수: {전체 attempt 합산}
평균 점수: {모든 스프린트 최종 점수 평균}%
Known Issues: {수렴 실패 항목 수}개
변경 파일: {총 파일 수}개
━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Handoff File Compilation

각 스프린트 완료 시 (PASS 또는 CONVERGED) `.harness/sprint-{N}-handoff.md`를 작성한다.

### 구성 방법

1. **이전 Handoff 읽기**: Sprint 2 이상이면 `.harness/sprint-{N-1}-handoff.md`의 `Cumulative Changes` 테이블을 가져온다.
2. **현재 Generator Result 읽기**: `.harness/sprint-{N}-generator-result.md`의 `Implementation Summary` 테이블에서 이번 스프린트 변경사항을 가져온다.
3. **병합**: 이전 누적 변경사항 + 이번 변경사항을 합친다. 동일 파일이 있으면 최신 스프린트 번호로 업데이트한다.
4. **현재 상태 기술**: 동작하는 기능과 미구현 기능을 기술한다.
5. **다음 스프린트 정보**: `.harness/sprints.md`에서 Sprint {N+1}의 Scope를 읽어 `Next Sprint` 섹션에 기재한다.
6. **Eval 피드백 반영**: `.harness/sprint-{N}-eval-result.md`의 Known Limitations이나 주의사항을 다음 스프린트 컨텍스트에 포함한다.

형식은 `references/handoff-schema.md` 섹션 5를 준수한다.

---

## Error Handling

| 상황 | 조치 |
|------|------|
| 에이전트 생성 실패 | 1회 재시도. 재실패 시 사용자에게 에스컬레이션 |
| Generator가 커밋 실패 | Generator를 다시 실행 (Evaluator 건너뜀) |
| Evaluator의 Score 라인 누락 | Score를 0%로 처리, Verdict를 RETRY로 처리 |
| Playwright MCP 사용 불가 | Evaluator가 자동으로 코드 리뷰 전용 모드로 강등 (RV 항목 스킵 명시) |
| `.harness/` 파일 누락 | 해당 스프린트를 attempt 1부터 재실행 |

---

## Key Principles

1. **Generator와 Evaluator는 항상 별도 에이전트다** — 같은 세션에서 두 역할을 수행하지 않는다. 독립성이 평가의 신뢰를 보장한다.

2. **모든 스프린트 = 완전한 컨텍스트 리셋** — 새 에이전트, 파일 기반 핸드오프만 사용. 이전 에이전트의 메모리에 의존하지 않는다.

3. **Evaluator는 설계상 회의적이다** — Generator의 Self-Check를 신뢰하지 않고 직접 코드를 읽고 실행하여 검증한다.

4. **완벽보다 수렴** — 2회 연속 안정된 점수 (차이 2% 이내)는 "충분히 좋다"로 판단한다. 무한 재시도를 방지한다.

5. **우아한 강등 (Graceful Degradation)** — Playwright 없으면 코드 리뷰만으로 진행. 부분적 도구로도 최선의 평가를 수행한다.
