# Harness Runner — Artifact Schema Definitions

이 문서는 harness-runner 스킬이 `.harness/` 디렉토리에 생성하는 모든 아티팩트의 정확한 형식을 정의한다.
Planner, Generator, Evaluator 에이전트는 반드시 이 스키마를 준수하여 파일을 생성해야 한다.

---

## 1. `product-spec.md`

**생성자**: Planner 에이전트
**목적**: 전체 구현 범위를 정의하는 제품 명세서

```markdown
# Product Specification

## Overview
{구현할 제품/기능에 대한 1~3문장 설명. 목적, 대상 사용자, 핵심 가치를 포함한다.}

## Tech Stack
{사용할 기술 스택 목록. 언어, 프레임워크, 라이브러리, 런타임 버전 등을 명시한다.}

- {기술명}: {버전 및 용도}
- {기술명}: {버전 및 용도}

## Features

### {기능 카테고리 1}
- [ ] {구체적인 기능 항목. 구현 완료 시 체크된다.}
- [ ] {구체적인 기능 항목}

### {기능 카테고리 2}
- [ ] {구체적인 기능 항목}
- [ ] {구체적인 기능 항목}

## Non-Functional Requirements
- {성능 요구사항: 예) API 응답시간 200ms 이하}
- {보안 요구사항: 예) 입력값 검증 필수}
- {품질 요구사항: 예) 테스트 커버리지 80% 이상}
- {기타 제약사항}
```

---

## 2. `sprints.md`

**생성자**: Planner 에이전트
**목적**: 스프린트별 구현 계획 및 평가 기준

```markdown
# Sprint Plan

Total Sprints: {총 스프린트 수 (정수)}

---

## Sprint {N}: {스프린트 이름}

### Scope
{이 스프린트에서 구현할 내용을 서술한다. 구체적인 파일, 컴포넌트, API 엔드포인트 등을 명시한다.}

**Deliverables:**
- {구체적인 산출물 1}
- {구체적인 산출물 2}

### Contract

#### Code Review Criteria
{Generator가 코드 작성 시 반드시 충족해야 하는 정적 기준. Evaluator가 코드를 읽어 확인한다.}

| # | 항목 | 설명 |
|---|------|------|
| CR-{N}.1 | {기준 항목명} | {판단 기준 설명} |
| CR-{N}.2 | {기준 항목명} | {판단 기준 설명} |

#### Runtime Verification Criteria
{Generator가 구현 완료 후 실제 실행하여 확인해야 하는 동적 기준. Evaluator가 실행 결과를 검증한다.}

| # | 항목 | 확인 방법 |
|---|------|----------|
| RV-{N}.1 | {검증 항목명} | {실행 명령 또는 확인 방법} |
| RV-{N}.2 | {검증 항목명} | {실행 명령 또는 확인 방법} |

### Dependencies
- {이 스프린트 시작 전 완료되어야 하는 이전 스프린트 또는 외부 의존성}
- 없음 (첫 스프린트인 경우)

---

## Sprint {N+1}: {스프린트 이름}

{위와 동일한 구조 반복}
```

---

## 3. `sprint-{N}-generator-result.md`

**생성자**: Generator 에이전트
**목적**: 스프린트 구현 결과 보고. `{N}`은 스프린트 번호 (1부터 시작)

```markdown
# Sprint {N} — Generator Result

Attempt: {현재 시도 횟수 (1부터 시작)}
Timestamp: {ISO 8601 형식, 예) 2026-03-28T14:30:00+09:00}

## Implementation Summary

| 파일 경로 | 작업 | 설명 |
|----------|------|------|
| {상대 경로} | {Created \| Modified \| Deleted} | {변경 내용 한 줄 요약} |
| {상대 경로} | {Created \| Modified \| Deleted} | {변경 내용 한 줄 요약} |

## Self-Check

Contract 기준 자가 점검 결과:

| 항목 ID | 항목명 | 결과 | 비고 |
|--------|--------|------|------|
| CR-{N}.1 | {항목명} | {PASS \| FAIL \| PARTIAL} | {근거 또는 미흡 사유} |
| RV-{N}.1 | {항목명} | {PASS \| FAIL \| PARTIAL} | {실행 결과 요약} |

## Known Limitations
{이번 구현에서 의도적으로 제외하거나 완벽하지 않은 부분. 없으면 "없음"으로 표기.}

- {제한사항 1: 이유 포함}
- {제한사항 2: 이유 포함}

## Git Commit

```
{실제 커밋 메시지}
```

Commit Hash: {git commit hash (최소 7자리)}
```

---

## 4. `sprint-{N}-eval-result.md`

**생성자**: Evaluator 에이전트
**목적**: Generator 결과에 대한 독립적 평가. `{N}`은 스프린트 번호

```markdown
# Sprint {N} — Evaluator Result

Attempt: {평가 대상 Generator 시도 횟수}
Timestamp: {ISO 8601 형식}

## Score

Overall: {0~100 정수}%

## Item Scores

| Contract Item | Score | Evidence |
|--------------|-------|----------|
| CR-{N}.1 — {항목명} | {0~100}% | {코드 파일명:줄번호 또는 "확인 불가" 사유} |
| CR-{N}.2 — {항목명} | {0~100}% | {코드 파일명:줄번호 또는 "확인 불가" 사유} |
| RV-{N}.1 — {항목명} | {0~100}% | {실행 명령 및 출력 결과 요약} |
| RV-{N}.2 — {항목명} | {0~100}% | {실행 명령 및 출력 결과 요약} |

## Verdict

{PASS | RETRY}

{PASS인 경우}: 모든 필수 기준을 충족하였습니다.
{RETRY인 경우}: {전체 점수}%로 통과 기준 미달. 아래 피드백을 반영하여 재시도 필요.

## Feedback for Generator

{PASS인 경우 이 섹션 생략 가능}

### 수정 필요 항목

1. **{항목 ID} — {항목명}** ({현재 점수}%)
   - 문제: {구체적인 문제 설명}
   - 요청: {Generator에게 요청하는 구체적인 수정 내용}

2. **{항목 ID} — {항목명}** ({현재 점수}%)
   - 문제: {구체적인 문제 설명}
   - 요청: {Generator에게 요청하는 구체적인 수정 내용}
```

---

## 5. `sprint-{N}-handoff.md`

**생성자**: 하네스 오케스트레이터 (스프린트 완료 시)
**목적**: 다음 스프린트를 위한 컨텍스트 전달. `{N}`은 완료된 스프린트 번호

```markdown
# Sprint {N} — Handoff

## Status

| 항목 | 값 |
|------|-----|
| 완료 스프린트 | {N} / {전체 스프린트 수} |
| 최종 점수 | {0~100}% |
| 시도 횟수 | {총 시도 횟수} |
| 완료 시각 | {ISO 8601 형식} |

## Cumulative Changes

스프린트 1 ~ {N}에서 생성/수정된 모든 파일:

| 파일 경로 | 상태 | 최종 수정 스프린트 |
|----------|------|-----------------|
| {상대 경로} | {Created \| Modified \| Deleted} | Sprint {M} |
| {상대 경로} | {Created \| Modified \| Deleted} | Sprint {M} |

## Current Project State

{현재 프로젝트의 작동 상태를 서술한다. 무엇이 동작하고 무엇이 아직 구현되지 않았는지 명확히 기술.}

**동작하는 기능:**
- {기능 1}
- {기능 2}

**미구현 기능 (향후 스프린트에서 처리):**
- {기능 1}
- {기능 2}

## Next Sprint

Sprint {N+1}: {다음 스프린트 이름}

{다음 스프린트 시작 시 Generator가 참고해야 할 컨텍스트. 이전 스프린트에서 발생한 Known Limitations, 주의사항, 이어서 작업해야 할 부분 등을 기술한다.}
```

---

## 6. `known-issues.md`

**생성자**: 하네스 오케스트레이터 (매 스프린트 완료 후 누적 업데이트)
**목적**: 최대 시도 횟수를 소진하고도 기준을 충족하지 못한 항목의 누적 목록

```markdown
# Known Issues

{이 파일은 하네스 실행 중 수렴에 실패한 항목을 누적 기록한다.
모든 스프린트를 통과한 경우 "없음"으로 표기한다.}

## Convergence Failures

| Sprint | Contract Item | Final Score | Last Attempt Score | Attempts |
|--------|--------------|-------------|-------------------|----------|
| {N} | {항목 ID} — {항목명} | {수렴 완료 점수 또는 "미달"} | {마지막 시도 점수}% | {총 시도 횟수} |
| {N} | {항목 ID} — {항목명} | {수렴 완료 점수 또는 "미달"} | {마지막 시도 점수}% | {총 시도 횟수} |

## Summary

총 {N}개 항목이 최대 시도 횟수({M}회)를 소진하였습니다.
```

---

## 7. `final-report.md`

**생성자**: 하네스 오케스트레이터 (전체 실행 완료 후)
**목적**: 하네스 전체 실행 결과 요약

```markdown
# Harness Run — Final Report

Completed: {ISO 8601 형식}

## Summary

| 항목 | 값 |
|------|-----|
| 총 스프린트 수 | {N} |
| 총 시도 횟수 | {전체 Generator 실행 횟수 합산} |
| 전체 평균 점수 | {모든 스프린트 최종 점수의 평균}% |
| Known Issues 수 | {수렴 실패 항목 총 개수} |
| 변경된 파일 수 | {전체 Created + Modified 파일 수} |

## Sprint Results

| Sprint | Name | Final Score | Attempts | Verdict |
|--------|------|-------------|----------|---------|
| {N} | {스프린트 이름} | {0~100}% | {시도 횟수} | {PASS \| PARTIAL} |
| {N+1} | {스프린트 이름} | {0~100}% | {시도 횟수} | {PASS \| PARTIAL} |

## Known Issues

{known-issues.md에 기록된 수렴 실패 항목이 있으면 항목 수와 간략한 설명을 기재한다.
없으면 "수렴 실패 항목 없음"으로 표기한다.}

## Files Changed

{전체 변경 파일 목록. sprint-{N}-handoff.md의 Cumulative Changes에서 최종 상태를 반영한다.}

| 파일 경로 | 최종 상태 | 최초 생성 스프린트 |
|----------|----------|-----------------|
| {상대 경로} | {Created \| Modified \| Deleted} | Sprint {N} |
| {상대 경로} | {Created \| Modified \| Deleted} | Sprint {N} |
```

---

## 아티팩트 생성 규칙

1. **경로**: 모든 아티팩트는 `.harness/` 디렉토리 아래에 생성한다.
2. **인코딩**: UTF-8, LF 줄바꿈
3. **플레이스홀더**: `{중괄호}` 안의 내용은 실제 값으로 교체한다. 중괄호가 남아있으면 안 된다.
4. **선택 표기**: `{A | B}` 형태는 해당하는 값 하나만 남긴다.
5. **누락 금지**: 각 섹션은 반드시 존재해야 한다. 내용이 없으면 "없음"으로 명시한다.
6. **덮어쓰기**: 재시도 시 동일한 파일명을 덮어쓴다 (버전 관리는 Git으로 한다).
