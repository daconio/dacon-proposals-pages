# Sprint Plan — daker.ai × dacon.io 단계별 통합

Total Sprints: 6

---

## Sprint 1: 브랜드 진입점 및 가시적 연결 (Cross-linking)

### Scope

두 플랫폼을 코드 수준에서 건드리지 않고 가시적 진입점(메뉴 링크, CTA 버튼, 공지 배너)으로 먼저 연결한다. dacon.io GNB에 "팀 빌딩" 메뉴를, daker.ai 랜딩에 "대회 참가" CTA를 추가하고, 브랜드 토큰(색상·폰트 가이드라인)을 문서화한다. 사용자는 이 단계 이후 두 서비스를 별도 탭 없이 하나의 생태계로 인식할 수 있다.

**Deliverables:**
- dacon.io GNB에 "팀 빌딩 (daker.ai)" 메뉴 링크 추가 (Vue.js 컴포넌트 수정)
- daker.ai 랜딩 페이지에 "대회 참가하기 →" CTA 버튼 (dacon.io 대회 목록 링크)
- 브랜드 통합 가이드라인 문서 (`.harness/brand-guide.md` 또는 내부 노션 페이지)
- dacon.io 공지 배너: "daker.ai 팀 빌딩 서비스 오픈 안내"
- 두 서비스 공통 OG 메타태그 포맷 정의

### Contract

#### Code Review Criteria

| # | 항목 | 설명 |
|---|------|------|
| CR-1.1 | dacon.io GNB 메뉴 항목 추가 | dacon.io GNB Vue 컴포넌트 파일에 `daker.ai` 또는 `팀 빌딩`을 포함하는 `<a>` 또는 `<router-link>` 태그가 존재한다 |
| CR-1.2 | daker.ai 랜딩 CTA 버튼 | daker.ai React 컴포넌트에 `dacon.io` 도메인으로 향하는 링크 버튼이 존재하며 텍스트에 "대회" 또는 "참가"가 포함된다 |
| CR-1.3 | Feature Flag 적용 | dacon.io GNB 신규 메뉴 항목은 환경변수 또는 Feature Flag 조건부로 렌더링된다 (`process.env` 또는 `import.meta.env` 기반) |
| CR-1.4 | 브랜드 가이드 문서 존재 | `--primary`, `--accent` 등 CSS 커스텀 프로퍼티 또는 색상 hex 코드가 정의된 브랜드 통합 문서가 존재한다 |
| CR-1.5 | OG 메타태그 포맷 | 양측 HTML `<head>`에 `og:site_name`, `og:title`, `og:description`, `og:image` 태그가 존재하며 포맷이 통일되어 있다 |

#### Runtime Verification Criteria

| # | 항목 | 확인 방법 |
|---|------|----------|
| RV-1.1 | dacon.io GNB 팀 빌딩 링크 노출 | dacon.io 스테이징 환경 접속 → GNB에 "팀 빌딩" 또는 "daker.ai" 텍스트 메뉴가 보이며 클릭 시 daker.ai 도메인으로 이동한다 |
| RV-1.2 | daker.ai 대회 참가 CTA | daker.ai 랜딩 접속 → "대회 참가" CTA 클릭 시 dacon.io/competitions (또는 대회 목록) 페이지로 이동한다 |
| RV-1.3 | Feature Flag off 시 메뉴 미노출 | Feature Flag를 off로 설정한 환경에서 dacon.io GNB에 daker.ai 메뉴가 노출되지 않는다 |

### Dependencies
- 없음 (첫 스프린트 — 기존 코드베이스 접근권만 필요)

---

## Sprint 2: 계정 통합 — dacon.io OAuth 공급자 구축

### Scope

dacon.io를 OAuth 2.0 인증 공급자로 확장하여 daker.ai 사용자가 "dacon 계정으로 로그인"할 수 있도록 한다. dacon.io 백엔드에 OAuth 인증 서버 엔드포인트(`/oauth/authorize`, `/oauth/token`, `/oauth/userinfo`)를 추가하고, daker.ai React 앱에 소셜 로그인 버튼을 구현한다. 기존 daker.ai 전용 계정은 이메일 기반 계정 연결 플로우로 마이그레이션 옵션을 제공한다.

**Deliverables:**
- dacon.io OAuth 2.0 인증 서버 엔드포인트 3개 (`/oauth/authorize`, `/oauth/token`, `/oauth/userinfo`)
- daker.ai "dacon 계정으로 로그인" 버튼 및 OAuth 클라이언트 구현
- 계정 연결/마이그레이션 UI 플로우 (daker.ai 마이페이지 내)
- JWT 토큰 공유 방식 명세 문서 (만료 시간, 갱신 전략 포함)
- 테스트 계정 세트 (단위 테스트용 Mock OAuth 서버 포함)

### Contract

#### Code Review Criteria

| # | 항목 | 설명 |
|---|------|------|
| CR-2.1 | OAuth 엔드포인트 존재 | dacon.io 백엔드 라우터에 `/oauth/authorize`, `/oauth/token`, `/oauth/userinfo` 경로가 정의되어 있다 |
| CR-2.2 | PKCE 지원 | `/oauth/authorize` 핸들러가 `code_challenge`와 `code_challenge_method` 파라미터를 수신하고 검증하는 로직을 포함한다 |
| CR-2.3 | JWT 만료 설정 | dacon.io가 발급하는 JWT의 `exp` 클레임이 최대 3600(1시간) 이하로 설정된다 |
| CR-2.4 | daker.ai OAuth 클라이언트 | daker.ai React 앱에 OAuth authorization code flow를 처리하는 함수 또는 훅이 존재한다 (state 파라미터 CSRF 방지 포함) |
| CR-2.5 | 계정 연결 UI | daker.ai 마이페이지에 "dacon 계정 연결" 또는 "dacon 계정으로 전환" 버튼 컴포넌트가 존재한다 |
| CR-2.6 | 에러 처리 | OAuth 실패(사용자 거부, 토큰 만료, 서버 오류) 시 사용자에게 한국어 에러 메시지를 표시하는 로직이 존재한다 |

#### Runtime Verification Criteria

| # | 항목 | 확인 방법 |
|---|------|----------|
| RV-2.1 | 로그인 플로우 완료 | daker.ai에서 "dacon 계정으로 로그인" 클릭 → dacon.io 로그인 페이지로 리다이렉트 → dacon 계정 인증 완료 → daker.ai로 리다이렉트되며 로그인 상태가 유지된다 |
| RV-2.2 | userinfo 응답 | `GET /oauth/userinfo` (Authorization: Bearer {token})에 유효한 토큰을 전달하면 HTTP 200과 `{ id, email, nickname }` 이상의 JSON 객체를 반환한다 (curl 또는 테스트로 확인) |
| RV-2.3 | 토큰 만료 처리 | 만료된 JWT로 daker.ai API 호출 시 HTTP 401을 반환하고, 클라이언트가 자동으로 토큰 갱신 또는 재로그인 플로우를 트리거한다 |
| RV-2.4 | 기존 daker.ai 계정 연결 | 기존 daker.ai 계정으로 로그인한 사용자가 마이페이지에서 dacon 계정 연결 버튼을 클릭하여 연결 완료 후, 이후 로그인 시 dacon 계정으로도 동일 프로필에 접근 가능하다 |

### Dependencies
- Sprint 1 완료 (브랜드 진입점 확보 후 인증 통합 진행)
- dacon.io 백엔드 소스코드 접근 권한 및 배포 파이프라인 권한

---

## Sprint 3: 대회 데이터 API 연동 — dacon.io → daker.ai

### Scope

dacon.io의 대회 데이터를 daker.ai 팀 빌딩 기능과 연결하는 API 계층을 구축한다. dacon.io는 현재 진행 중인 대회 목록·상세 정보를 제공하는 공개 API 엔드포인트를 추가하고, daker.ai는 팀 빌딩 생성 시 dacon.io 대회를 선택·연결할 수 있도록 UI를 수정한다. dacon.io 대회 상세 페이지에는 연결된 팀 수가 표시된다.

**Deliverables:**
- dacon.io 대회 목록 API: `GET /api/v1/competitions?status=active` (페이지네이션, 필터 지원)
- dacon.io 대회 상세 API: `GET /api/v1/competitions/{id}` (팀 수 포함)
- daker.ai 팀 빌딩 생성 폼에 "참가 대회 선택" 드롭다운 (dacon.io API 기반)
- dacon.io 대회 상세 페이지 "연결된 팀" 카운트 위젯
- API Rate Limiting 및 Circuit Breaker 설정

### Contract

#### Code Review Criteria

| # | 항목 | 설명 |
|---|------|------|
| CR-3.1 | 대회 목록 API 엔드포인트 존재 | dacon.io 백엔드에 `GET /api/v1/competitions` 라우트가 정의되어 있으며 `status` 쿼리 파라미터를 처리한다 |
| CR-3.2 | 응답 스키마 정의 | 대회 목록 API 응답이 `{ id, title, status, deadline, participantCount }` 이상의 필드를 포함하는 배열을 반환한다 |
| CR-3.3 | daker.ai 대회 선택 컴포넌트 | daker.ai 팀 빌딩 생성 폼에 `competitionId` 필드를 처리하는 컴포넌트 또는 훅이 존재하고, dacon.io API를 호출하여 옵션을 채운다 |
| CR-3.4 | Circuit Breaker 또는 Fallback | daker.ai의 dacon.io API 호출 코드에 타임아웃(최대 5초) 또는 에러 시 Fallback(빈 목록 표시) 처리가 존재한다 |
| CR-3.5 | Rate Limiting 설정 | dacon.io API 라우터 또는 미들웨어에 IP 또는 토큰 기반 Rate Limiting 설정이 존재한다 (분당 60회 이하) |
| CR-3.6 | 팀 수 위젯 | dacon.io 대회 상세 Vue 컴포넌트에 daker.ai 연결 팀 수를 표시하는 UI 요소가 존재한다 |

#### Runtime Verification Criteria

| # | 항목 | 확인 방법 |
|---|------|----------|
| RV-3.1 | 대회 목록 API 응답 | `curl https://dacon.io/api/v1/competitions?status=active` 실행 시 HTTP 200과 대회 배열 JSON을 반환한다 |
| RV-3.2 | daker.ai 팀 빌딩 대회 선택 | daker.ai 팀 빌딩 생성 화면에서 "참가 대회" 드롭다운을 열면 dacon.io 현재 진행 중인 대회 목록이 나타난다 |
| RV-3.3 | 대회 연결 후 dacon.io 반영 | daker.ai에서 특정 dacon.io 대회(ID 기준)와 팀을 연결한 후, dacon.io 해당 대회 상세 페이지에서 "연결된 팀" 카운트가 1 이상으로 증가한다 |
| RV-3.4 | Circuit Breaker 동작 | dacon.io API 서버를 임시 중단했을 때 daker.ai 팀 빌딩 화면이 에러 없이 "대회 정보를 불러올 수 없습니다" 메시지를 표시하고 정상 동작한다 |

### Dependencies
- Sprint 2 완료 (인증된 API 호출을 위해 SSO 토큰 필요)

---

## Sprint 4: UX 통합 — Cross-navigation 및 공통 헤더

### Scope

두 플랫폼 간 사용자 이동 경험을 매끄럽게 만드는 UX 통합을 수행한다. dacon.io 대회 상세 페이지에 "팀 구하기 (daker.ai)" 버튼을, daker.ai 팀 빌딩 완료 후 "대회 제출하기 (dacon.io)" 딥링크를 추가한다. 공통 헤더 스타일 가이드 또는 Web Component를 제작하고, dacon.io 마이페이지에 daker.ai 팀 참여 이력을 노출한다.

**Deliverables:**
- dacon.io 대회 상세 페이지 내 "팀 구하기" 버튼 (daker.ai 팀 빌딩 생성 딥링크)
- daker.ai 팀 빌딩 완료 화면 내 "대회 제출하기" 버튼 (dacon.io 제출 페이지 딥링크)
- 공통 헤더 Web Component 또는 공유 CSS 가이드 (독립 배포 가능)
- dacon.io 마이페이지 "내 팀 (daker.ai)" 섹션 (팀명, 대회명, 참여 날짜 표시)
- 모바일 반응형 Cross-navigation CTA 검증

### Contract

#### Code Review Criteria

| # | 항목 | 설명 |
|---|------|------|
| CR-4.1 | 팀 구하기 버튼 | dacon.io 대회 상세 Vue 컴포넌트에 `daker.ai`로 향하는 "팀 구하기" 버튼이 존재하며, 대회 ID를 쿼리 파라미터로 전달한다 (`?competitionId={id}`) |
| CR-4.2 | 대회 제출하기 딥링크 | daker.ai 팀 빌딩 완료 컴포넌트에 `dacon.io/competitions/{id}/submit`으로 향하는 링크 버튼이 존재한다 |
| CR-4.3 | 공통 헤더 컴포넌트 격리 | 공통 헤더가 Web Component(`<dacon-header>`) 또는 독립 iframe embed 방식으로 구현되어 React와 Vue.js 양쪽에서 사용 가능하다 |
| CR-4.4 | 마이페이지 팀 이력 컴포넌트 | dacon.io 마이페이지에 `dakerTeams` 또는 유사한 데이터를 daker.ai API에서 불러와 렌더링하는 Vue 컴포넌트 또는 섹션이 존재한다 |
| CR-4.5 | 모바일 반응형 | "팀 구하기" 및 "대회 제출하기" 버튼이 max-width 768px 이하에서도 적절한 크기와 터치 타겟(최소 44×44px)을 가진다 |

#### Runtime Verification Criteria

| # | 항목 | 확인 방법 |
|---|------|----------|
| RV-4.1 | 팀 구하기 딥링크 | dacon.io 대회 상세 페이지에서 "팀 구하기" 클릭 → daker.ai 팀 빌딩 생성 페이지로 이동하며 URL에 `?competitionId={id}` 파라미터가 포함된다 |
| RV-4.2 | 대회 제출하기 딥링크 | daker.ai 팀 빌딩 완료 화면에서 "대회 제출하기" 클릭 → dacon.io 해당 대회 제출 페이지로 이동한다 |
| RV-4.3 | 마이페이지 팀 이력 노출 | daker.ai 팀에 참여한 dacon.io 사용자의 마이페이지에서 "내 팀 (daker.ai)" 섹션이 나타나며 팀명과 연결된 대회명이 표시된다 |

### Dependencies
- Sprint 2 완료 (마이페이지 팀 이력을 인증된 API로 가져오기 위해)
- Sprint 3 완료 (대회 ID 기반 딥링크 생성을 위해)

---

## Sprint 5: 데이터 심화 통합 — 통합 프로필 및 알림

### Scope

두 플랫폼의 사용자 데이터를 통합하여 하나의 일관된 프로필과 알림 경험을 제공한다. dacon 티어(Tier) + daker 협업 점수가 통합된 프로필 카드를 구현하고, 대회 수상 시 daker.ai 팀 배지를 자동 부여하는 파이프라인을 구축한다. 통합 알림 시스템(대회 마감, 팀 초대, 리더보드 변동)과 GTM 기반 크로스 플랫폼 Analytics 이벤트 스키마를 완성한다.

**Deliverables:**
- 통합 사용자 프로필 API: `GET /api/v1/users/{id}/profile` (dacon 티어 + daker 활동 점수 통합)
- dacon.io 수상 이벤트 Webhook → daker.ai 팀 배지 자동 부여 파이프라인
- 통합 알림 서비스 (In-app 알림 + 이메일): 대회 마감 D-3, 팀 초대, 리더보드 Top3 진입
- GTM 크로스 플랫폼 이벤트 스키마 정의 및 태그 배포 (양측 공통 `user_id` 기반 추적)
- 통합 검색 결과: dacon.io 검색에 daker.ai 팀 결과 포함 (탭 또는 섹션 분리)

### Contract

#### Code Review Criteria

| # | 항목 | 설명 |
|---|------|------|
| CR-5.1 | 통합 프로필 API | `/api/v1/users/{id}/profile` 엔드포인트가 `{ daconTier, daconPoints, dakerActivityScore, dakerTeamCount }` 이상의 필드를 반환하는 로직이 존재한다 |
| CR-5.2 | 수상 Webhook 핸들러 | dacon.io에 수상 이벤트 Webhook을 발송하는 코드가 존재하고, daker.ai에 해당 Webhook을 수신하여 팀 배지를 부여하는 핸들러가 존재한다 |
| CR-5.3 | 알림 서비스 분리 | 알림 발송 로직이 별도 서비스 모듈 또는 큐(Queue) 기반으로 분리되어 있어 메인 API 응답 지연에 영향을 주지 않는다 |
| CR-5.4 | GTM 이벤트 태그 | 양측 코드베이스에서 GTM `dataLayer.push({ event: '...', user_id: '...' })` 형태의 이벤트 발송 코드가 존재하며 `user_id` 필드가 통일된 포맷을 사용한다 |
| CR-5.5 | 통합 검색 결과 | dacon.io 검색 API 또는 검색 결과 컴포넌트가 daker.ai 팀 검색 결과를 포함하는 로직 또는 UI 섹션을 갖는다 |

#### Runtime Verification Criteria

| # | 항목 | 확인 방법 |
|---|------|----------|
| RV-5.1 | 통합 프로필 API 응답 | `GET /api/v1/users/{id}/profile` 호출 시 HTTP 200과 dacon 티어 + daker 활동 점수가 포함된 JSON을 반환한다 |
| RV-5.2 | 수상 배지 자동 부여 | dacon.io 테스트 환경에서 대회 수상 처리(관리자) 후 해당 사용자의 daker.ai 팀 페이지에 수상 배지가 자동으로 나타난다 (최대 5분 이내) |
| RV-5.3 | 알림 발송 | 대회 마감 D-3 시 등록된 참가자에게 알림(In-app 또는 이메일)이 발송되는 것을 테스트 계정으로 확인한다 |
| RV-5.4 | 크로스 플랫폼 Analytics | GTM Preview 모드에서 dacon.io → daker.ai 이동 시 동일 `user_id`로 이벤트가 양측에서 발생하는 것을 확인한다 |

### Dependencies
- Sprint 3 완료 (대회 데이터 API가 Webhook 발송의 기반)
- Sprint 4 완료 (통합 프로필을 표시할 UX 레이어 완성 후)

---

## Sprint 6: 관리 통합 — 어드민 콘솔 및 운영 프로세스

### Scope

두 플랫폼의 운영 관리를 통합하는 어드민 콘솔과 공통 운영 프로세스를 구축한다. 통합 어드민에서 사용자, 대회, 팀을 단일 뷰로 조회·관리하고, 주최사 대시보드에 팀 빌딩 현황을 통합 표시한다. 공유 어뷰징 대응 시스템, 단일 헬프센터, 공통 SLA 문서를 완성한다.

**Deliverables:**
- 통합 어드민 콘솔 화면: 사용자/대회/팀 통합 검색 및 조회
- 주최사(대회 운영자) 대시보드 — 팀 빌딩 현황 위젯 추가
- 공유 블랙리스트 API (스팸/어뷰징 계정 공동 차단)
- 통합 헬프센터 URL (dacon.io/help 로 일원화) 및 FAQ 콘텐츠 이관
- 통합 SLA 및 장애 대응 RunBook 문서

### Contract

#### Code Review Criteria

| # | 항목 | 설명 |
|---|------|------|
| CR-6.1 | 통합 어드민 사용자 검색 | 어드민 콘솔에서 이메일 또는 닉네임으로 검색 시 dacon.io 계정 정보와 daker.ai 팀 참여 이력을 함께 조회하는 API 또는 뷰가 존재한다 |
| CR-6.2 | 주최사 팀 빌딩 위젯 | 주최사 대시보드 Vue 컴포넌트에 해당 대회에 연결된 daker.ai 팀 수 및 목록을 표시하는 섹션이 존재한다 |
| CR-6.3 | 블랙리스트 API | `POST /api/v1/admin/blacklist` 엔드포인트가 존재하며, 해당 계정을 dacon.io와 daker.ai 양측에서 차단하는 로직이 포함된다 (트랜잭션 또는 이벤트 기반) |
| CR-6.4 | 헬프센터 리다이렉트 | daker.ai `/help` 또는 `/support` 경로가 dacon.io 통합 헬프센터 URL로 301 리다이렉트된다 |
| CR-6.5 | SLA 문서 존재 | 장애 등급 정의, 대응 시간 목표(P0: 30분, P1: 2시간, P2: 24시간), 담당자 에스컬레이션 경로가 명시된 RunBook 문서가 존재한다 |

#### Runtime Verification Criteria

| # | 항목 | 확인 방법 |
|---|------|----------|
| RV-6.1 | 어드민 통합 검색 | 어드민 콘솔에서 테스트 계정 이메일 검색 시 dacon 계정 정보(티어, 대회 참여 이력)와 daker.ai 팀 목록이 단일 화면에 표시된다 |
| RV-6.2 | 블랙리스트 차단 동작 | `POST /api/v1/admin/blacklist { userId: '...' }` 호출 후 해당 사용자로 dacon.io와 daker.ai 양측 로그인 시도 시 모두 접근이 거부된다 |
| RV-6.3 | 헬프센터 리다이렉트 | `curl -I https://daker.ai/help` 실행 시 HTTP 301과 `Location: https://dacon.io/help` 헤더를 반환한다 |
| RV-6.4 | 주최사 팀 현황 표시 | 주최사 계정으로 dacon.io 대시보드 접속 시 운영 중인 대회에 연결된 daker.ai 팀 수가 올바르게 표시된다 |

### Dependencies
- Sprint 5 완료 (통합 사용자 데이터 구조 완성 후 어드민 통합 가능)
- Sprint 2 완료 (SSO 기반 어드민 계정 통합 필요)

---

## 전체 타임라인 요약

| 스프린트 | 내용 | 선행 조건 | 예상 기간 |
|---------|------|----------|---------|
| Sprint 1 | 브랜드 진입점 및 Cross-linking | 없음 | 1~2주 |
| Sprint 2 | OAuth SSO 계정 통합 | Sprint 1 | 3~4주 |
| Sprint 3 | 대회 데이터 API 연동 | Sprint 2 | 2~3주 |
| Sprint 4 | UX Cross-navigation 및 공통 헤더 | Sprint 2, 3 | 2~3주 |
| Sprint 5 | 통합 프로필·알림·Analytics | Sprint 3, 4 | 3~4주 |
| Sprint 6 | 어드민 통합 및 운영 프로세스 | Sprint 2, 5 | 2~3주 |

**총 예상 기간**: 약 13~19주 (병렬 작업 가능 시 단축 가능)

## 통합 원칙 재확인

1. 각 스프린트는 독립적으로 롤백 가능 (Feature Flag 기반)
2. dacon.io가 마스터 데이터 소스, daker.ai는 소비자
3. 사용자 데이터 마이그레이션 시 이중 저장 → 검증 → 구 레코드 삭제 순서 준수
4. 모든 API는 버전 관리 (`/api/v1/`) — 통합 이후에도 하위 호환 유지
