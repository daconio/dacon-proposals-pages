# Sprint Plan

Total Sprints: 4

---

## Sprint 1: 데이터 스키마 정의 및 샘플 데이터 구축

### Scope

`사후리포트/` 폴더를 신규 생성하고, 리포트 시스템 전체의 데이터 계약(schema)을 JSON으로 정의한다. 해커톤 샘플 데이터(`sample-hackathon.json`)와 교육 프로그램 샘플 데이터(`sample-edu.json`)를 작성하여, 이후 스프린트에서 렌더러와 템플릿이 참조할 실제 데이터를 준비한다. 스키마는 모든 섹션(커버, 개요, 통계, 타임라인, 하이라이트, 평가, 회고, 팀 카드, 참가자 명단)을 커버해야 하며, 샘플 데이터는 실제 DAKER 운영 행사를 모사한 현실적인 내용으로 채운다.

**Deliverables:**
- `사후리포트/data/schema.json` — 전체 스키마 정의 파일 (주석 포함 JSON5 불가, 순수 JSON)
- `사후리포트/data/sample-hackathon.json` — 해커톤 샘플 (팀 5개, 참가자 30명 이상, 타임라인 8항목)
- `사후리포트/data/sample-edu.json` — 교육 프로그램 샘플 (다른 eventType, 학습 성취 데이터 포함)

### Contract

#### Code Review Criteria

| # | 항목 | 설명 |
|---|------|------|
| CR-1.1 | eventType 필드 존재 | 두 샘플 JSON 모두 최상위에 `"eventType"` 필드가 있으며 값은 `"hackathon"` 또는 `"education"` 이다 |
| CR-1.2 | 팀 데이터 필수 필드 | `teams` 배열 각 항목에 `id`, `name`, `rank`, `score`, `highlight`, `members`, `output` 필드가 모두 존재한다 |
| CR-1.3 | 참가자 30명 이상 | `sample-hackathon.json`의 `participants` 배열 항목 수가 30개 이상이다 |
| CR-1.4 | 타임라인 8항목 이상 | `sample-hackathon.json`의 `timeline` 배열 항목 수가 8개 이상이며, 각 항목에 `date`, `time`, `label`, `description` 필드가 있다 |
| CR-1.5 | 평가 데이터 구조 | `evaluation.criteria` 배열 각 항목에 `criterion`, `maxScore`, `teamScores` (팀 ID와 점수 매핑 배열)가 포함된다 |
| CR-1.6 | 회고 데이터 카테고리 | `retrospective` 배열에 `category`가 `"성과"`, `"개선"`, `"제안"` 세 카테고리가 모두 1개 이상 포함된다 |

#### Runtime Verification Criteria

| # | 항목 | 확인 방법 |
|---|------|----------|
| RV-1.1 | JSON 유효성 — 해커톤 샘플 | `python3 -m json.tool 사후리포트/data/sample-hackathon.json > /dev/null && echo OK` 실행 시 `OK` 출력 |
| RV-1.2 | JSON 유효성 — 교육 샘플 | `python3 -m json.tool 사후리포트/data/sample-edu.json > /dev/null && echo OK` 실행 시 `OK` 출력 |
| RV-1.3 | 참가자 수 확인 | `python3 -c "import json; d=json.load(open('사후리포트/data/sample-hackathon.json')); print(len(d['participants']))"` 실행 결과가 30 이상인 숫자 출력 |

### Dependencies

- 없음 (첫 스프린트)

---

## Sprint 2: 리포트 템플릿 시스템 및 디자인 토큰

### Scope

A4 세로 인쇄에 최적화된 CSS 레이아웃 시스템을 구축한다. `@page`, `@media print` 규칙, CSS 커스텀 프로퍼티(디자인 토큰), 섹션별 페이지 분리 규칙, CSS counter 기반 페이지 번호를 포함한 기반 CSS를 작성한다. 이 스프린트의 산출물은 `사후리포트/report-template.html` 파일이며, JS 렌더링 없이 하드코딩된 placeholder 콘텐츠로 레이아웃·인쇄 동작을 검증할 수 있는 상태여야 한다. 화면 미리보기 모드(스크롤 가능한 A4 페이지 목업)도 함께 구현한다.

**Deliverables:**
- `사후리포트/report-template.html` — CSS 레이아웃 + 디자인 토큰 + placeholder 콘텐츠 포함 베이스 파일

### Contract

#### Code Review Criteria

| # | 항목 | 설명 |
|---|------|------|
| CR-2.1 | @page A4 규칙 | CSS에 `@page { size: A4 portrait; margin: 15mm; }` 또는 동등한 규칙이 존재한다 |
| CR-2.2 | print-color-adjust | `body` 또는 `:root`에 `print-color-adjust: exact; -webkit-print-color-adjust: exact;` 가 선언되어 있다 |
| CR-2.3 | 디자인 토큰 일치 | `:root`에 `--primary: #0053db`, `--accent-warm: #c2622d`, `--surface`, `--on-surface`, `--on-surface-variant`, `--outline-variant` 가 기존 프로젝트와 동일한 값으로 정의되어 있다 |
| CR-2.4 | 섹션 페이지 분리 | `.report-section` 클래스에 `page-break-before: always` 가 적용되어 있으며, 커버 섹션(`.cover`)은 예외 처리되어 있다 |
| CR-2.5 | 카드 잘림 방지 | `.team-card`, `.participant-row` 등 반복 단위 요소에 `page-break-inside: avoid` 가 적용되어 있다 |
| CR-2.6 | 화면 미리보기 레이아웃 | `@media screen`에서 `.a4-page` 요소가 `width: 210mm`, `min-height: 297mm`, `margin: 0 auto`, `box-shadow` 스타일로 A4 카드 형태로 표시된다 |

#### Runtime Verification Criteria

| # | 항목 | 확인 방법 |
|---|------|----------|
| RV-2.1 | 브라우저 파일 열기 | `open 사후리포트/report-template.html` 실행 후 Chrome에서 정상 로드 (콘솔 에러 없음). 화면에 A4 비율 흰 카드가 세로 스크롤로 나열되어 표시된다 |
| RV-2.2 | HTML 유효성 | `python3 -c "from html.parser import HTMLParser; p=HTMLParser(); p.feed(open('사후리포트/report-template.html').read()); print('OK')"` 실행 시 `OK` 출력 (파싱 에러 없음) |

### Dependencies

- Sprint 1 완료 (디자인 토큰은 독립적이나, placeholder 예시 값은 sample JSON을 참고한다)

---

## Sprint 3: 섹션별 렌더링 컴포넌트 구현

### Scope

`사후리포트/js/renderer.js`를 작성하고, `report-template.html`에 통합하여 JSON 데이터를 실제 DOM으로 렌더링하는 엔진을 구현한다. 9개 섹션(커버, 목차, 행사 개요, 참가자·팀 통계, 타임라인, 우수 산출물 하이라이트, 평가 결과, 운영 회고, 부록)의 렌더러를 각각 구현하고, 점수 합산·순위 계산 로직을 JS 내에서 처리한다. 빈 필드 처리(숨김)도 구현한다.

**Deliverables:**
- `사후리포트/js/renderer.js` — 전체 렌더링 엔진
- `사후리포트/report-template.html` 업데이트 — JS 통합, placeholder를 렌더러 타겟 DOM으로 교체

### Contract

#### Code Review Criteria

| # | 항목 | 설명 |
|---|------|------|
| CR-3.1 | loadReport 함수 존재 | `renderer.js`에 `async function loadReport(jsonPath)` 함수가 정의되어 있으며, fetch → JSON.parse → 렌더링 파이프라인을 실행한다 |
| CR-3.2 | 9개 섹션 렌더러 | `renderCover`, `renderTableOfContents`, `renderOverview`, `renderStats`, `renderTimeline`, `renderHighlights`, `renderEvaluation`, `renderRetrospective`, `renderTeamCards`, `renderParticipants` 함수가 모두 정의되어 있다 |
| CR-3.3 | 순위 계산 로직 | `renderEvaluation` 또는 별도 헬퍼 함수 내에서 각 팀의 `totalScore`를 계산하고 내림차순 정렬 후 `rank`를 부여하는 코드가 존재한다 |
| CR-3.4 | 빈 필드 숨김 처리 | 데이터 값이 `null`, `undefined`, 또는 빈 문자열인 경우 해당 DOM 요소에 `style.display = 'none'` 또는 `hidden` 속성을 적용하는 조건 분기가 2개 이상 존재한다 |
| CR-3.5 | 견적·비용 문구 부재 | `renderer.js` 및 `report-template.html` 전체에서 "견적", "예산", "비용", "가격", "패키지", "스킬 리포트" 문자열이 존재하지 않는다 |

#### Runtime Verification Criteria

| # | 항목 | 확인 방법 |
|---|------|----------|
| RV-3.1 | 해커톤 샘플 렌더링 | `report-template.html`을 `?data=./data/sample-hackathon.json` 쿼리스트링 또는 직접 경로로 열었을 때, 브라우저 DOM에 팀 이름(샘플 데이터의 `teams[0].name`)이 포함된 요소가 존재한다. 확인: 브라우저 콘솔에서 `document.body.innerHTML.includes('[팀명]')` → `true` |
| RV-3.2 | 교육 샘플 렌더링 | `sample-edu.json`을 로드했을 때 커버 섹션에 교육 프로그램 행사명이 렌더링된다. 확인: 브라우저 콘솔에서 `document.querySelector('.cover-title').textContent` 가 샘플 JSON의 `eventName` 값과 일치 |
| RV-3.3 | 콘솔 에러 없음 | 두 샘플 데이터 로드 시 브라우저 콘솔에 JavaScript 에러(빨간 메시지)가 없다. 확인: DevTools Console에서 에러 0건 |

### Dependencies

- Sprint 1 완료 (JSON 데이터 파일 필요)
- Sprint 2 완료 (렌더러 타겟 DOM 구조 및 CSS 클래스 필요)

---

## Sprint 4: 데모 완성 및 인쇄·PDF 출력 검증

### Scope

`사후리포트/index.html` 데모 진입점과 `demo-hackathon.html`, `demo-edu.html` 두 개의 완성 데모 리포트를 생성한다. 각 데모 파일은 샘플 데이터를 fetch 없이 인라인 JSON으로 직접 포함하여, 파일을 더블클릭만 해도 동작하는 완전한 자급자족 형태여야 한다(file:// 프로토콜 대응). 인쇄 출력 검증 체크리스트를 `index.html` 내 안내문으로 포함하고, 전체 시스템의 완성도를 확인한다.

**Deliverables:**
- `사후리포트/index.html` — 데모 진입점 (사용법 안내 + 두 데모 링크)
- `사후리포트/demo-hackathon.html` — 해커톤 샘플 인라인 데이터 완성 리포트
- `사후리포트/demo-edu.html` — 교육 프로그램 샘플 인라인 데이터 완성 리포트

### Contract

#### Code Review Criteria

| # | 항목 | 설명 |
|---|------|------|
| CR-4.1 | 인라인 JSON 데이터 | `demo-hackathon.html`과 `demo-edu.html` 내부에 `<script type="application/json" id="report-data">` 또는 JS 변수로 샘플 데이터가 인라인 포함되어 있어 외부 fetch 없이 렌더링된다 |
| CR-4.2 | index.html 링크 2개 | `사후리포트/index.html`에 `demo-hackathon.html`과 `demo-edu.html`로의 링크(`<a href="...">`)가 각각 존재한다 |
| CR-4.3 | 인쇄 안내 포함 | `index.html`에 "Ctrl+P 또는 브라우저 인쇄 메뉴 → PDF로 저장" 방법 안내 텍스트가 한국어로 포함되어 있다 |
| CR-4.4 | 파일명 규칙 예시 | `index.html` 또는 각 데모 파일 내에 `YYYY-MM-DD-{고객사}_{행사명}_사후리포트.html` 파일명 규칙이 텍스트로 명시되어 있다 |
| CR-4.5 | 금지 문구 부재 | 모든 산출물 HTML 파일에서 "견적", "예산", "비용", "패키지 가격", "스킬 리포트" 문자열이 존재하지 않는다 |

#### Runtime Verification Criteria

| # | 항목 | 확인 방법 |
|---|------|----------|
| RV-4.1 | 해커톤 데모 자급자족 동작 | `open 사후리포트/demo-hackathon.html` 로 파일 열기 후, 네트워크 연결 없이(DevTools Network throttle → Offline) 페이지가 완전히 렌더링된다. 브라우저 콘솔 에러 0건 |
| RV-4.2 | 교육 데모 자급자족 동작 | `open 사후리포트/demo-edu.html` 로 파일 열기 후, 동일 조건에서 완전 렌더링. 콘솔 에러 0건 |
| RV-4.3 | 인쇄 레이아웃 정상 | Chrome DevTools → 더보기 → 인쇄 미리보기(또는 Ctrl+P)에서 `demo-hackathon.html`을 열었을 때: (1) 커버 페이지가 독립 1페이지, (2) 섹션 제목이 새 페이지 상단에 위치, (3) 팀 카드가 페이지 중간에서 잘리지 않음을 육안 확인 |
| RV-4.4 | index.html 정상 열기 | `open 사후리포트/index.html` 실행 후 브라우저에서 "해커톤 샘플", "교육 프로그램 샘플" 두 링크가 정상 표시되고 클릭 가능하다 |

### Dependencies

- Sprint 1 완료 (샘플 JSON 데이터 — 인라인 포함 시 내용 복사)
- Sprint 2 완료 (CSS 레이아웃 시스템)
- Sprint 3 완료 (렌더링 엔진 — 데모 파일에 통합)
