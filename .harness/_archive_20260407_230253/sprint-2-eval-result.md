# Sprint 2 — Evaluator Result

## Meta

| 항목 | 값 |
|------|-----|
| Sprint | 2 |
| Attempt | 1 |
| 대상 파일 | `제안/2026-03-29-단국대학교_SW중심대학_사전대회_제안서.html` |
| 평가일 | 2026-03-29 |

---

## Stage 1: Code Review

| ID | 검증 항목 | 점수 | 근거 |
|----|---------|------|------|
| CR-20 | 파일 존재 | 2 | `ls` 명령으로 확인. 파일 존재함 (697줄). |
| CR-21 | 슬라이드 수 | 2 | `<section class="slide` 패턴 15개. 14~16 범위 이내. |
| CR-22 | 표지 제목 | 2 | S1의 `<h1>`에 "SW중심대학" + "사전 연습 대회 제안서" 명확히 포함. |
| CR-23 | 7월 타임라인 | 2 | S11에 "7월 개최 타임라인" 제목, 4월~7월 그리드 구조 존재. "7월" 7회 등장. |
| CR-24 | 예산 슬라이드 | 2 | S12에 Basic/Standard/Premium 패키지 테이블 + "만원" 금액 단위 다수 포함. |
| CR-25 | 성과 지표 테이블 | 2 | `table class="tb"` 6개 존재. S10(ALIGNMENT)에 성과 지표 매핑 테이블 포함. |
| CR-26 | data-step 애니메이션 | 2 | `data-step` 속성 요소 87개. 기준(10개) 대비 대폭 초과. |
| CR-27 | 인쇄 CSS | 2 | `@page { size: landscape; margin: 0; }` + `page-break-after: always` + `break-after: page` 모두 존재. |
| CR-28 | 단일 파일 | 2 | `src=` 속성 검색 결과 0건. 외부 리소스는 Google Fonts `<link href>` 뿐. |
| CR-29 | 페이지 번호 | 2 | `sf-pg` 클래스 요소 15개. 기준(14개) 이상. |
| CR-30 | 네비게이션 JS | 2 | `<script>` 블록에 `show(idx,dir)` 함수 정의 확인. |
| CR-31 | 구 파일명 없음 | 2 | `2026-03-23` 문자열 검색 결과 0건. |

## Stage 2: Runtime Verification (코드 리뷰 대체)

| ID | 검증 항목 | 점수 | 근거 |
|----|---------|------|------|
| RV-01 | 초기 로드 | 2 | S1에 `class="slide active"` 부여. 나머지 14개는 `class="slide"`만. `slide active` 패턴은 파일 전체에서 1회만 등장. |
| RV-02 | 키보드 네비게이션 | 2 | `keydown` 이벤트 리스너에서 `ArrowRight`, `ArrowLeft` 분기 처리. Space, Enter, Backspace도 지원. |
| RV-03 | 프래그먼트 | 2 | `next()` 함수에서 `step` 카운터 증가 후 `data-step <= step` 요소에 `visible` 클래스 추가. `prev()`에서 제거. `pre-visible` 클래스로 뒤로 가기 시 즉시 표시. |
| RV-04 | 진행바 | 2 | `show()` 함수 내 `document.getElementById('progress-bar').style.width=((idx+1)/total*100)+'%'` 로 업데이트. |
| RV-05 | 스케일링 | 2 | `fit()` 함수: `Math.min(vw/1280,vh/720,1)` 계산 후 `stage.style.transform='scale('+s+')'` 적용. `window.addEventListener('resize',fit)` 바인딩. |
| RV-06 | 마지막 슬라이드 | 2 | S15(slide-end)에 "미팅 요청" `<a>` 태그 (daker.ai 설문 링크), daker.ai, dacon.io 링크, contact@daker.ai 연락처 포함. |

---

## Scoring

| 구분 | 항목 수 | 만점 | 획득 |
|------|---------|------|------|
| CR (Code Review) | 12 | 24 | 24 |
| RV (Runtime Verification) | 6 | 12 | 12 |
| **합계** | **18** | **36** | **36** |

```
Sprint Score = 36 / 36 × 100 = 100%
```

## Verdict

**PASS** (100% >= 90%)

---

## Notes

- Generator의 Self-Check와 독립 검증 결과가 완전히 일치한다.
- 모든 CR/RV 항목이 완전 충족(2점)이다.
- HTML 아키텍처는 기존 슬라이드 템플릿(viewport/stage, slide 시스템, data-step, 인쇄 CSS)을 정확히 따르고 있다.
- 슬라이드 15개가 product-spec 구성표와 일치하며, 콘텐츠가 MD 원본을 충실히 반영한다.
