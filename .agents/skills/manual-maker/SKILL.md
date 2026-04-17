---
name: manual-maker
description: DAKER 프로젝트 사용자 매뉴얼 자동 제작 및 슬라이드 프레젠테이션 생성 스킬. Codex in Chrome 또는 Playwright MCP로 실제 사용자처럼 페이지를 탐색하며 스크린샷을 캡처하고, 병렬 에이전트 팀으로 MD 매뉴얼 문서와 스크린샷 포함 HTML 문서를 동시에 생성한다. SSO 로그인이 필요한 페이지도 지원한다. 또한 순수 HTML/CSS/JavaScript만으로 웹 기반 슬라이드 프레젠테이션을 생성할 수 있다. 매뉴얼, manual, 사용법, 가이드, 사용자 안내, 기능 설명서, 조작법, 운영 매뉴얼, 페이지 설명, 스크린샷 매뉴얼, 캡처 문서, how to use, user guide, documentation, 슬라이드, slide, 프레젠테이션, presentation, 발표 자료, PPT, 발표, 슬라이드쇼, slideshow 등의 키워드가 나오면 반드시 이 스킬을 사용할 것. 특정 기능이나 페이지에 대한 사용법 문서화 요청이나 발표 자료 생성에도 적합하다.
---

# Manual Maker — 매뉴얼 자동 제작 + 슬라이드 프레젠테이션 생성

2가지 모드를 지원한다:

1. **매뉴얼 모드**: 브라우저 캡처 기반 사용자 매뉴얼 자동 제작 (MD + HTML)
2. **슬라이드 모드**: 순수 HTML/CSS/JS 웹 슬라이드 프레젠테이션 생성 (단일 HTML 파일)

사용자 요청에서 "슬라이드", "프레젠테이션", "발표", "PPT", "slide" 키워드가 있으면 → **슬라이드 모드**
그 외 "매뉴얼", "가이드", "사용법" 등이면 → **매뉴얼 모드**

---

## 슬라이드 모드

슬라이드 모드에서는 순수 HTML/CSS/JavaScript만으로 웹 프레젠테이션을 생성한다.
외부 라이브러리 의존 없이 단일 HTML 파일로 동작한다.

**상세 구현 가이드**: `references/slide-guide.md` 참조
**디자인 시스템**: `references/design-system.md` 참조 (The Editorial Architect)
**HTML → PDF 변환**: `references/slide-guide.md` §7-A 참조 — `scripts/html_to_pdf.py` 사용 (스크린샷+Pillow 방식). `page.pdf()`/Chrome `--print-to-pdf`는 `@media print` 강제 활성화로 첫 슬라이드만 캡처되는 함정이 있음.

### 슬라이드 디자인 필수 규칙

1. **Color**: 3-Color 시스템 — Primary(`#0053db`) + Slate(`#2a3439`) + White(`#ffffff`). 과도한 색상 추가 지양.
2. **Font**: `Plus Jakarta Sans` 단일 서체. Display는 letter-spacing `-0.02em`.
3. **No-Line 규칙**: 1px 보더 영역 구분 금지 → 배경색 톤 전환(surface hierarchy)으로 분리
4. **Surface 계층**: surface(#f7f9fb) → surface_container_low(#f0f4f7) → surface_container_lowest(#ffffff)
5. **#000000 금지**: 텍스트 `#2a3439`, 그림자 `rgba(30,41,59,0.04)` Ambient만
6. **Glass**: Hero CTA에 `primary(#0053db) → primary_dim(#0048c1)` 135도 그라디언트
7. **비대칭 패딩**: 에디토리얼 오프센터 리듬 — Dead Space 수용

### 슬라이드 생성 흐름

```
1. 콘텐츠 수집 (사용자 요청 분석 또는 기존 문서 변환)
  ↓
2. 병렬 에이전트로 슬라이드 구성
  ├─ Agent A: 슬라이드 레이아웃 & DOM 구조
  ├─ Agent B: 네비게이션 & 인터랙션
  ├─ Agent C: 전환 애니메이션
  └─ Agent D: 콘텐츠 빌드 효과
  ↓
3. 단일 HTML 파일로 통합 출력
  ↓
4. 브라우저에서 확인 (open 명령)
```

### 슬라이드 핵심 기능

| 기능 | 구현 방법 |
|------|----------|
| 레이아웃 | CSS absolute + transform, 16:9 비율 고정 |
| 전환 | CSS transition + transform (slide, fade, zoom) |
| 키보드 | ←→ Space PageUp/Down Home/End F(풀스크린) |
| 터치 | touchstart/touchend 스와이프 |
| 프로그레스 | 하단 바 + 슬라이드 번호 |
| Fragment | data-step 순차 등장 |
| 해시 라우팅 | #slide-N URL 동기화 |
| 인쇄 | @media print 지원 |
| 발표자 뷰 | BroadcastChannel + 별도 창 |

### 출력 파일

```
docs/plans/YYYY-MM-DD-{주제}_슬라이드.html  (단일 파일, 브라우저에서 바로 실행)
```

---

## 매뉴얼 모드

DAKER 플랫폼의 기능별 사용자 매뉴얼을 실제 브라우저에서 캡처하며 자동으로 만든다. 사용자가 직접 조작하는 것처럼 페이지를 탐색하고, 각 단계를 스크린샷과 설명으로 기록하여 MD 문서와 시각적 HTML 문서를 함께 생성한다.

## 전체 흐름

```
Phase 1: 매뉴얼 범위 & 구조 설계 + 캡처 계획
  ↓
Phase 2: 브라우저 준비 + SSO 인증
  ↓
Phase 3: 순차 캡처 → 캡처 완료 후 병렬 문서 생성
  ├─ Step 1: 메인 에이전트가 직접 캡처 (순차)
  ├─ Step 2: 캡처 완료 후 에이전트 B/C에 파일 목록 전달
  │   ├─ 에이전트 B: MD 매뉴얼 문서 작성
  │   └─ 에이전트 C: HTML 문서 생성
  ↓
Phase 4: 최종 검수 & 출력
```

---

## Phase 1: 매뉴얼 범위 & 구조 설계

### 1-1. 대상 기능 파악

사용자 요청에서 매뉴얼 대상을 파악한다:

| 요청 유형 | 예시 | 범위 |
|-----------|------|------|
| 특정 기능 | "해커톤 참가 매뉴얼 만들어줘" | 해당 기능의 전체 플로우 |
| 특정 포털 | "Admin 포털 매뉴얼" | 포털 내 주요 기능 전체 |
| 특정 페이지 | "학습 페이지 사용법" | 해당 페이지 기능 설명 |
| 전체 | "DAKER 사용자 가이드" | 주요 기능 전체 (목차 기반) |

### 1-2. 캡처 계획 수립

목차와 함께 **캡처 계획표**를 작성한다. 각 스크린샷마다 어떤 영역을 캡처할지 미리 정한다.

```markdown
| # | 파일명 | 페이지/URL | 캡처 대상 | 캡처 방식 |
|---|--------|-----------|-----------|----------|
| 01 | 01-해커톤목록.png | /public/hackathons | 상단 카드 6개 + 필터 | viewport |
| 02 | 02-해커톤상세-상단.png | /public/hackathons/:slug | 배너 + 요약 정보 | viewport (상단) |
| 03 | 03-참가신청-동의.png | 같은 페이지 | 동의사항 영역 | scroll-to → viewport |
| 04 | 04-과제제출.png | ?section=submissions | 제출 폼 전체 | scroll-to → viewport |
```

**캡처 계획을 사용자에게 보여주고 승인받은 후 Phase 2로 진행한다.**

### 1-3. 출력 파일 경로

```
docs/plans/
├── YYYY-MM-DD-{주제}_매뉴얼.md
├── YYYY-MM-DD-{주제}_매뉴얼.html
└── screenshots/manual-{주제}/
    ├── 01-해커톤목록.png
    └── ...
```

---

## Phase 2: 브라우저 준비 + SSO 인증

### 2-1. 브라우저 도구 선택

두 가지 MCP 도구를 순서대로 시도한다:

1. **Codex in Chrome** (`mcp__claude-in-chrome__*`): `tabs_context_mcp`로 연결 확인
2. **Playwright MCP** (`mcp__plugin_playwright_playwright__*`): Chrome 미연결 시 사용
   - Chrome이 실행 중이면 Playwright가 실패한다 → 사용자에게 Chrome 종료 요청
   - `browser_install` 실행 후 `browser_resize(1280, 800)` 설정

### 2-2. SSO 인증 (필요한 경우)

Public 페이지(/public/*)는 로그인 없이 캡처 가능하다.
Admin, Expert, 마이페이지는 로그인 세션이 필요하다.

로그인이 필요하면 사용자에게 안내:
```
매뉴얼 캡처를 위해 SSO 로그인 세션이 필요합니다.
Chrome에서 로그인을 완료해주세요.
```

---

## Phase 3: 캡처 + 문서 생성

### Step 1: 메인 에이전트가 직접 캡처 (순차)

캡처는 서브에이전트에 위임하지 않고 **메인 에이전트가 직접** 수행한다. 브라우저 MCP는 하나의 세션만 사용할 수 있기 때문이다.

#### 스크린샷 캡처 전략 (핵심)

페이지 특성에 따라 3가지 캡처 방식을 사용한다:

| 방식 | 사용 시점 | 설명 |
|------|----------|------|
| **viewport** | 페이지 상단, 목록의 첫 화면 | 현재 보이는 화면만 캡처 (1280x800). 가장 깔끔 |
| **scroll-to → viewport** | 특정 섹션, 폼, 버튼 영역 | 대상 요소로 스크롤 후 viewport 캡처 |
| **fullPage** | 전체 구조를 보여야 할 때만 | 페이지 전체 캡처. 길어질 수 있으므로 신중히 사용 |

**viewport 캡처가 기본이다.** fullPage는 짧은 페이지(스크롤 없이 모든 내용이 보이는 경우)에만 사용한다.

#### 캡처 절차

```
각 캡처 항목에 대해:

1. 페이지 이동 (navigate)
2. 로딩 대기 (snapshot으로 DOM 확인, 또는 wait 2-3초)
3. 팝업/다이얼로그 처리 (있으면 캡처 후 닫기)
4. 대상 영역으로 이동:
   - 상단이면: Home 키 또는 scrollTo(0, 0)
   - 특정 섹션이면: scroll_to(ref) 또는 evaluate(() => element.scrollIntoView())
   - 하단이면: End 키 또는 scrollTo(0, document.body.scrollHeight)
5. viewport 스크린샷 캡처
6. 파일명은 캡처 계획표의 이름 사용
```

#### 팝업/다이얼로그 처리

페이지 이동 시 예상치 못한 팝업(가이드, 모달, 쿠키 동의 등)이 나타날 수 있다:

1. snapshot으로 dialog 요소 확인
2. 팝업이 유용한 내용이면 → **먼저 캡처** (별도 파일로)
3. Escape 키 또는 닫기 버튼으로 팝업 닫기
4. 원래 캡처 계획 진행

#### 특정 섹션 캡처 방법 (Playwright MCP)

```javascript
// 방법 1: evaluate로 스크롤
await page.evaluate(() => {
  document.querySelector('[data-testid="consent-section"]').scrollIntoView({ block: 'start' });
});

// 방법 2: scroll_to ref 사용 (snapshot에서 ref 확인 후)
// browser_click(ref=e1459) → 해당 요소로 이동

// 방법 3: evaluate로 좌표 스크롤
await page.evaluate(() => window.scrollTo(0, 특정높이));
```

스크롤 후 **1-2초 대기** → viewport 캡처. 이렇게 하면 대상 영역이 화면 중앙에 위치하여 잘리지 않는다.

#### 캡처 품질 체크리스트

캡처 후 이미지를 확인하여 다음을 검증한다:
- [ ] 대상 영역이 화면에 완전히 보이는가? (잘리지 않았는가?)
- [ ] 이미지 높이가 적절한가? (viewport 크기 이내인가?)
- [ ] 불필요한 팝업이 가리고 있지 않은가?
- [ ] 데이터가 로딩된 상태인가? ("로딩 중..." 텍스트가 아닌 실제 데이터)

문제가 있으면 스크롤 조정 후 **재캡처**한다.

### Step 2: 캡처 완료 후 병렬 문서 생성

캡처가 모두 끝나면, 캡처 결과(파일 목록 + 각 이미지 설명)를 에이전트 B/C에 전달하여 **동시에** MD와 HTML을 생성한다.

#### 에이전트에 전달할 캡처 목록 형식

```
캡처 완료된 스크린샷 목록:
| # | 파일명 | 페이지 | 설명 |
|---|--------|--------|------|
| 1 | 01-해커톤목록.png | /public/hackathons | 카드 6개 + 사이드바 필터 |
| 2 | 02-해커톤상세-상단.png | /public/hackathons/slug | 배너 + 요약 + 참가 진행 상태 |
| ...
```

이 목록을 에이전트 프롬프트에 포함하면 이미지 파일명이 문서와 정확히 일치한다.

#### 에이전트 B: MD 매뉴얼 문서 작성

```
DAKER 프로젝트의 [대상 기능] 사용자 매뉴얼을 MD 형식으로 작성해줘.

캡처된 스크린샷 목록:
[위 캡처 목록 붙여넣기]

작성 규칙:
1. 코드를 분석하여 기능의 동작 흐름을 파악
2. 스크린샷 참조 시 위 목록의 정확한 파일명을 사용
   예: ![해커톤 목록](screenshots/manual-{주제}/01-해커톤목록.png)
3. 사용자 시점 한국어로 작성
4. 파일 저장: docs/plans/YYYY-MM-DD-{주제}_매뉴얼.md
```

#### 에이전트 C: HTML 문서 생성

```
DAKER 프로젝트의 [대상 기능] 매뉴얼을 HTML 형식으로 제작해줘.

캡처된 스크린샷 목록:
[위 캡처 목록 붙여넣기]

이미지 참조 규칙:
- 위 목록의 정확한 파일명으로 <img src="screenshots/manual-{주제}/파일명"> 사용
- Lightbox 클릭 확대 포함
- 참고: .Codex/skills/manual-maker/references/html-template.md

파일 저장: docs/plans/YYYY-MM-DD-{주제}_매뉴얼.html
```

---

## Phase 4: 최종 검수 & 출력

### 4-1. 이미지 경로 검증

```bash
# MD에서 참조하는 이미지가 모두 존재하는지 확인
grep -oP 'screenshots/manual-\S+\.png' docs/plans/*매뉴얼.md | while read img; do
  [ -f "docs/plans/$img" ] || echo "MISSING: $img"
done
```

### 4-2. 결과 보고

```markdown
매뉴얼 제작이 완료되었습니다.

| 파일 | 경로 |
|------|------|
| MD 매뉴얼 | docs/plans/YYYY-MM-DD-{주제}_매뉴얼.md |
| HTML 매뉴얼 | docs/plans/YYYY-MM-DD-{주제}_매뉴얼.html |
| 스크린샷 | docs/plans/screenshots/manual-{주제}/ (X장) |
```

`open docs/plans/YYYY-MM-DD-{주제}_매뉴얼.html`로 브라우저에서 확인.

---

## 페이지별 캡처 가이드

### Public 포털

| 페이지 | URL | 캡처 포인트 | 방식 |
|--------|-----|------------|------|
| 메인 | `/` | 히어로 영역 | viewport |
| 해커톤 목록 | `/public/hackathons` | 카드 6개 + 필터 | viewport |
| 해커톤 상세 | `/public/hackathons/:slug` | 배너+요약 / 동의사항 / 제출 | viewport × 여러 장 |
| Raids 목록 | `/public/raids` | 카드 + 상태 필터 | viewport |
| 학습 | `/public/learning` | 코스 목록 | viewport |

### Admin 포털

| 페이지 | URL | 캡처 포인트 | 방식 |
|--------|-----|------------|------|
| 대시보드 | `/admin` | KPI 카드 | viewport |
| 해커톤 관리 | `/admin/hackathons` | 테이블 | viewport |

### Expert 포털

| 페이지 | URL | 캡처 포인트 | 방식 |
|--------|-----|------------|------|
| 심사 대시보드 | `/expert` | 할당 목록 | viewport |

---

## 스크린샷 캡처 규칙

### 브라우저 설정
- **해상도**: 1280 × 800 (viewport)
- **도구**: resize_window 또는 browser_resize로 고정

### 파일 네이밍
```
{순번2자리}-{페이지명}-{상태}.png
예: 01-해커톤목록.png, 02-해커톤상세-상단.png, 03-참가신청-동의.png
```

### fullPage 사용 금지 원칙

fullPage 캡처는 페이지가 길면 수천 픽셀짜리 이미지가 되어 매뉴얼에 부적합하다.
대신 **viewport 기반 다중 캡처**로 섹션별 이미지를 따로 찍는다.

예: 해커톤 상세 페이지 → 3장으로 분할
1. `02-해커톤상세-상단.png` (배너 + 요약)
2. `03-참가신청-동의.png` (동의사항 섹션으로 스크롤)
3. `04-과제제출.png` (제출 폼 섹션으로 스크롤)

### 잘림 방지

특정 섹션 캡처 시 대상이 화면 밖에 있을 수 있다. 반드시:
1. **대상 요소로 스크롤** (scrollIntoView, scroll_to ref, evaluate scrollTo)
2. **1-2초 대기** (렌더링 완료)
3. **캡처 후 이미지 확인** (대상이 완전히 보이는지)
4. 잘렸으면 스크롤 조정 후 재캡처

---

## 핵심 원칙

1. **viewport 기본, fullPage는 예외**: 긴 이미지는 매뉴얼 가독성을 해친다. 섹션별로 나눠서 캡처한다.
2. **캡처 먼저, 문서 나중에**: 캡처 파일 목록을 확정한 후 에이전트에 전달해야 이미지 경로 불일치가 없다.
3. **스크롤 후 대기**: 대상 영역으로 스크롤한 뒤 반드시 렌더링 대기를 거쳐야 잘리지 않는다.
4. **팝업은 기회**: 예상치 못한 팝업도 유용한 정보면 별도 캡처 후 문서에 포함한다.
5. **사용자 시점 우선**: 개발 용어 대신 최종 사용자가 이해할 수 있는 언어로 작성한다.
