# Product Specification

## Overview

DAKER 행사 사후 리포트 자동생성 시스템은 해커톤·학습 프로그램·그룹팀 활동이 종료된 후, 주최측(고객사)에게 제공할 A4 세로 기준 인쇄용 PDF 상세 리포트를 정적 HTML 파일로 자동 생성하는 시스템이다. JSON 형식의 행사 데이터를 입력받아, 행사 개요·참가자/팀 통계·활동 타임라인·우수 산출물 하이라이트·평가 결과·운영 회고·부록(팀 카드/참가자 명단)이 포함된 일관된 디자인의 단일 HTML 파일을 생성하며, 브라우저 인쇄(Ctrl+P) 또는 Print to PDF로 즉시 배포 가능한 산출물을 만든다. 산출물은 `/Users/kookjinkim/code/제안서/사후리포트/` 폴더에 위치하며 샘플 데이터 기반 데모를 포함한다.

## Tech Stack

- HTML5/CSS3: A4 print 레이아웃 (210×297mm), `@media print` + `@page` 규칙 기반 인쇄 최적화
- JavaScript (Vanilla ES6+): 템플릿 렌더링 엔진 — JSON 데이터를 DOM에 주입하는 단순 렌더러
- Google Fonts: 'Plus Jakarta Sans' (기존 프로젝트 표준 폰트)
- CSS Custom Properties (Design Tokens): 기존 리포지토리 팔레트(`--primary: #0053db`, `--accent-warm: #c2622d` 등) 재사용
- JSON: 행사 데이터 스키마 (샘플 파일 포함)
- No build tools, no npm: 순수 정적 파일 — 브라우저에서 직접 열기 가능

## Features

### 데이터 스키마 및 샘플 데이터

- [ ] `사후리포트/data/schema.json` — 행사 데이터 전체 구조 정의 (이벤트 메타, 팀 목록, 참가자 목록, 타임라인, 평가 항목, 회고 항목)
- [ ] `사후리포트/data/sample-hackathon.json` — 해커톤 샘플 데이터 (팀 5개, 참가자 30명 이상, 타임라인 8개 항목, 우수 산출물 3개, 평가 결과 포함)
- [ ] `사후리포트/data/sample-edu.json` — 학습 프로그램 샘플 데이터 (다른 이벤트 유형 커버)
- [ ] JSON 스키마에 `eventType` 필드 포함 (`hackathon` / `education` / `group-activity`)
- [ ] 팀 데이터에 `rank`, `score`, `highlight`, `members`, `output` 필드 포함
- [ ] 참가자 데이터에 `name`, `team`, `role`, `organization` 필드 포함
- [ ] 타임라인 항목에 `date`, `time`, `label`, `description`, `icon` 필드 포함
- [ ] 평가 데이터에 `criterion`, `maxScore`, `teamScores` 배열 포함
- [ ] 회고 데이터에 `category`(성과/개선/제안), `content` 필드 포함

### 리포트 템플릿 시스템 및 디자인 토큰

- [ ] `사후리포트/report-template.html` — 단일 자급자족 HTML 파일, 외부 의존성은 Google Fonts만 허용
- [ ] `@page` 규칙으로 A4 세로(210×297mm), 여백 15mm 설정
- [ ] CSS `@media print` 블록으로 화면 UI 숨김 처리 및 인쇄 색상 최적화
- [ ] `page-break-before: always` / `page-break-inside: avoid` 를 섹션 및 카드에 적용
- [ ] CSS 커스텀 프로퍼티로 디자인 토큰 정의 (`--primary`, `--accent-warm`, `--surface` 등 기존 팔레트 사용)
- [ ] 커버 페이지, 목차, 본문 섹션, 부록 섹션의 4대 레이아웃 구역 구분
- [ ] 각 섹션 상단에 DAKER 로고 텍스트 + 페이지 번호 표시 (CSS counter 활용)
- [ ] 화면 미리보기 모드: A4 비율 페이지가 스크롤 가능한 목업으로 표시

### 섹션별 컴포넌트 구현

- [ ] **커버 페이지**: 행사명, 주최사, 운영사(DAKER), 날짜, 대표 이미지 영역(색상 블록 대체)
- [ ] **목차**: 섹션 번호·제목·페이지 번호 자동 생성 (JS로 렌더링)
- [ ] **행사 개요**: 행사 유형, 일정, 장소, 목표, 주요 수치(참가자 수/팀 수/일수) 카드 형태
- [ ] **참가자·팀 통계**: 총인원, 팀 수, 조직별 분포 막대 그래프(CSS only), 완주율·참여율 지표
- [ ] **활동 타임라인**: 날짜별 세로 타임라인, 아이콘·레이블·설명 포함
- [ ] **우수 산출물 하이라이트**: 상위 3팀 카드 (팀명, 주제, 설명, 수상 등급)
- [ ] **평가 결과**: 평가 항목별 팀 점수 표(table), 총점 기준 순위 자동 계산
- [ ] **운영 회고**: 성과/개선/제안 카테고리별 항목 목록
- [ ] **부록 — 개별 팀 카드**: 각 팀의 팀명·구성원·산출물 요약·점수를 카드 2열 그리드로 표시
- [ ] **부록 — 참가자 명단**: 이름·팀·역할·소속 전체 표(table), 인쇄 시 줄바꿈 최적화

### 렌더링 엔진 (JS 템플릿)

- [ ] `사후리포트/js/renderer.js` — JSON을 받아 각 섹션 DOM을 빌드하는 순수 함수 모음
- [ ] `loadReport(jsonPath)` 함수: fetch + JSON.parse + 전체 렌더링 파이프라인 실행
- [ ] `renderSection(sectionId, data)` 함수: 섹션별 독립 렌더러 호출 디스패처
- [ ] `renderCover`, `renderOverview`, `renderStats`, `renderTimeline`, `renderHighlights`, `renderEvaluation`, `renderRetrospective`, `renderTeamCards`, `renderParticipants` 함수 각각 구현
- [ ] 데이터 없는 선택 필드 처리: 빈 값이면 해당 요소를 `display:none`으로 숨김
- [ ] 점수 합산 및 순위 계산 로직은 JS 내에서 처리 (서버 불필요)

### 데모 및 진입점

- [ ] `사후리포트/index.html` — 데모 진입점: "해커톤 샘플 보기" / "교육 프로그램 샘플 보기" 버튼 2개, 리포트 미리보기 링크
- [ ] `사후리포트/demo-hackathon.html` — 해커톤 샘플 데이터로 렌더링된 완성 리포트 (파일 열기만으로 동작)
- [ ] `사후리포트/demo-edu.html` — 교육 프로그램 샘플 데이터로 렌더링된 완성 리포트
- [ ] `사후리포트/README.md` 금지 — CLAUDE.md 규칙상 문서 파일은 별도 생성 불가. 대신 `index.html`에 사용법 안내 포함

### 인쇄/PDF 출력 검증

- [ ] 브라우저 Ctrl+P 시 A4 페이지 경계가 섹션 사이에서만 끊기는지 확인 (카드 중간 잘림 없음)
- [ ] 커버 페이지가 독립 1페이지로 출력되는지 확인
- [ ] 부록 팀 카드가 카드 단위로 잘리지 않는지 확인
- [ ] CSS 색상이 `print-color-adjust: exact` 적용으로 인쇄 시 보존되는지 확인

## Non-Functional Requirements

- 외부 CDN 또는 서버 의존성 없음: Google Fonts 외 모든 스타일·스크립트는 인라인 또는 동일 폴더 내 파일
- 브라우저 호환성: Chrome 최신 버전에서 화면 렌더링 및 인쇄 정상 동작 보장
- JSON 파일 경로는 상대 경로로만 참조 (`./data/sample-hackathon.json`)
- 인쇄 시 URL·배경색 인쇄 설정과 무관하게 레이아웃 유지
- 한국어 전용: 모든 레이블·안내문은 한국어로 작성
- 견적·예산·비용 섹션 절대 포함 금지 (CLAUDE.md 규칙)
- "스킬 리포트" 문구 사용 금지 (CLAUDE.md 규칙)
- 파일 명명: `YYYY-MM-DD-{고객사}_{행사명}_사후리포트.html` 규칙을 데모에서 예시로 보여줌
- 단일 폴더(`사후리포트/`) 내 모든 산출물 자급자족: 폴더를 압축하여 고객에게 전달 가능
