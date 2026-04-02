# Product Specification — daker.ai × dacon.io 단계별 통합 계획

## Overview

daker.ai(클로드 코드 기반 차세대 AI 협업·빌딩 플랫폼)와 dacon.io(기존 인간 개발자 운영 AI·데이터 사이언스 경진대회 플랫폼)를 단계적으로 통합한다. 목표는 두 플랫폼의 사용자 베이스, 기능, 브랜드를 하나의 통합된 에코시스템으로 합쳐 AI 대회 참가자(dacon.io)와 AI 협업 팀 빌더(daker.ai)가 동일한 플랫폼 위에서 활동하도록 하는 것이다. 최종 상태는 dacon.io가 대회 운영의 허브, daker.ai가 협업·바이브코딩 레이어로 역할 분담된 단일 플랫폼이다.

---

## Tech Stack

### daker.ai (신규·클로드 코드 기반)
- **Frontend**: React + Vite — SPA 구조
- **실시간 협업**: y-websocket (CRDT 기반 실시간 공동 편집)
- **Analytics**: Google Analytics 4
- **디자인**: 다크모드 지원, 커스텀 CSS 토큰

### dacon.io (기존·인간 개발자 운영)
- **Frontend**: Vue.js + Vuetify — SPA 구조
- **CSS**: Tailwind CSS
- **UI 컴포넌트**: Swiper (배너·캐러셀)
- **Analytics**: Google Analytics 4, GTM (Google Tag Manager), Hotjar
- **주요 기능**: 경진대회 관리, 리더보드, 뱃지/티어 시스템, 채용 연계, 스폰서 노출
- **콘텐츠 영역**: 메인 배너, 공식 경진대회, 카테고리별 대회, 인터뷰, 스폰서, 채용

### 공통 인프라 (통합 목표)
- **인증**: 통합 SSO (Single Sign-On) — dacon.io 계정으로 daker.ai 로그인
- **API**: RESTful API Gateway — dacon.io 대회 데이터를 daker.ai 팀 빌딩에 공급
- **CDN**: 정적 자산 공유
- **모니터링**: 통합 Analytics 이벤트 스키마

---

## Features

### Phase 1 — 브랜드 및 진입점 통합
- [ ] daker.ai 공식 페이지에 dacon.io 링크 및 "대회 참가하기" CTA 배치
- [ ] dacon.io 메인/GNB에 "팀 빌딩(daker.ai)" 메뉴 항목 추가
- [ ] 두 서비스 공통 로고·색상 가이드라인(브랜드 토큰) 정의
- [ ] 공유 소셜 메타태그(OG, Twitter Card) 포맷 통일
- [ ] 사용자 대상 공개 통합 로드맵 페이지 (dacon.io/roadmap 또는 공지)

### Phase 2 — 계정 및 인증 통합
- [ ] dacon.io 계정 시스템을 daker.ai 로그인 공급자(OAuth 2.0)로 등록
- [ ] daker.ai에서 "dacon 계정으로 로그인" 버튼 구현
- [ ] 기존 daker.ai 전용 계정 → dacon 계정 마이그레이션 플로우
- [ ] JWT 또는 세션 토큰 공유 방식 설계 및 구현
- [ ] 로그인 상태 dacon.io ↔ daker.ai 간 동기화 (SSO)
- [ ] 계정 병합 시 프로필(닉네임, 아바타, 티어) 승계 규칙 정의

### Phase 3 — 대회 데이터 API 연동
- [ ] dacon.io 대회 목록 API 엔드포인트 (공개 or 인증 기반) 설계
- [ ] daker.ai 팀 빌딩 화면에서 dacon.io 현재 진행 중인 대회 리스트 표시
- [ ] 팀 빌딩 생성 시 "참가 대회" 선택 → dacon.io 대회 ID 연결
- [ ] 대회별 팀 현황(팀 수, 참가자 수)을 dacon.io 대회 상세 페이지에 반영
- [ ] Webhook 또는 폴링 방식으로 dacon.io 대회 상태 변경 시 daker.ai 팀에 알림
- [ ] daker.ai 팀 활동 로그(제출 횟수, 협업 시간) → dacon.io 리더보드 보조 지표 연동 (선택)

### Phase 4 — UX 통합 (Cross-navigation)
- [ ] dacon.io 대회 상세 페이지에 "팀 구하기 (daker.ai)" 버튼 삽입
- [ ] daker.ai 팀 빌딩 완료 후 "대회 제출하기 (dacon.io)" 딥링크 버튼
- [ ] 공통 헤더/GNB 컴포넌트 또는 스타일 가이드 (독립 배포 가능한 웹 컴포넌트로 제공)
- [ ] dacon.io 마이페이지에 daker.ai 팀 참여 이력 표시
- [ ] 모바일 반응형 통합 진입점 (dacon.io 모바일 → daker.ai 팀 빌딩)

### Phase 5 — 데이터 및 기능 심화 통합
- [ ] 통합 사용자 프로필 (dacon 티어 + daker 협업 활동 점수 통합 표시)
- [ ] 대회 결과(수상) → daker.ai 팀 배지 자동 부여
- [ ] daker.ai 실시간 협업 코드(y-websocket)를 dacon.io 대회 제출 파이프라인과 연결
- [ ] 통합 알림 시스템 (대회 마감, 팀 초대, 리더보드 변동)
- [ ] 통합 검색: dacon.io 검색창에서 "팀" 검색 시 daker.ai 팀 결과 포함
- [ ] 사용자 행동 통합 Analytics 이벤트 스키마 (GTM 기반 크로스 플랫폼 추적)

### Phase 6 — 관리 및 운영 통합
- [ ] 어드민 콘솔에서 두 플랫폼 사용자/대회/팀 통합 조회
- [ ] 대회 운영자(주최사) 대시보드에 팀 빌딩 현황 통합 표시
- [ ] 스팸·어뷰징 공동 대응 (공유 블랙리스트)
- [ ] 통합 고객 지원 채널 (단일 헬프센터)
- [ ] SLA 및 장애 대응 공통 프로세스 정의

---

## Non-Functional Requirements

- **가용성**: 통합 작업 중 dacon.io 서비스 다운타임 0 — Blue/Green 또는 Feature Flag 방식으로 무중단 배포
- **성능**: API 연동 추가로 인한 dacon.io 메인 페이지 LCP(Largest Contentful Paint) 증가 200ms 이하
- **보안**: SSO 구현 시 OAuth 2.0 + PKCE 표준 준수; JWT 만료 시간 최대 1시간
- **호환성**: React(daker.ai) ↔ Vue.js(dacon.io) 간 공유 컴포넌트는 Web Components 또는 iframe embed 방식으로 격리
- **확장성**: API Gateway 계층을 통해 양측 독립 배포 가능성 유지 — 어느 한쪽 서비스 장애가 다른 쪽으로 전파되지 않도록 Circuit Breaker 패턴 적용
- **데이터 정합성**: 계정 마이그레이션 시 데이터 손실 0 — 이중 저장 후 검증 완료 시 구 레코드 삭제
- **CLAUDE.md 제약**: 제안서·슬라이드 내 견적/비용 섹션 없음; "스킬 리포트" 언급 없음
- **문서 언어**: 모든 산출 문서는 한국어; 커밋 메시지는 영어

---

## 통합 원칙 (Guiding Principles)

1. **Non-disruptive**: dacon.io 기존 사용자 경험을 해치지 않으면서 점진적으로 통합
2. **Feature-flagged**: 모든 통합 기능은 Feature Flag로 on/off 가능하게 구현
3. **API-first**: UI 통합 전 API 계층 통합 선행
4. **Single source of truth**: 계정·대회 데이터는 dacon.io가 마스터, daker.ai는 소비자
5. **Reversible**: 각 통합 단계는 롤백 가능하도록 설계
