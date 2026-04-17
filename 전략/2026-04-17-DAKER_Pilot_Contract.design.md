---
created: 2026-04-17
updated: 2026-04-17
author: edgar@dacon.io
status: draft
priority: critical
tags: [project, daker, pdca, design, contract, billing, subscription]
project_name: DAKER B2B 월구독 전환
phase: PDCA-Design
feature: DAKER-Pilot-Contract
pdca_cycle: "2026-Q2-Pilot"
version: "0.1"
planning_doc: [[2026-04-17-DAKER_B2B_PDCA_Plan]]
related: [[2026-04-17-DAKER_B2B_월구독_서비스_기획서]], [[2026-04-17-DAKER_B2B_파일럿_실행키트]]
---

# DAKER-Pilot-Contract Design Document

> **Summary**: 파일럿 계약·빌링·구독 상태·AI 크레딧 미터링의 **5개 서브시스템 통합 설계** — 파일럿 6주 내 프로덕션 투입 가능한 최소 완성도 목표.
>
> **Project**: DAKER (daker.ai)
> **Version**: 0.1
> **Author**: edgar@dacon.io
> **Date**: 2026-04-17
> **Status**: Draft
> **Planning Doc**: [[2026-04-17-DAKER_B2B_PDCA_Plan]]

### Pipeline References

| 문서 | 상태 |
|------|------|
| 기획서 (Plan) | ✅ [[2026-04-17-DAKER_B2B_월구독_서비스_기획서]] |
| 실행키트 (Plan) | ✅ [[2026-04-17-DAKER_B2B_파일럿_실행키트]] |
| PDCA Plan | ✅ [[2026-04-17-DAKER_B2B_PDCA_Plan]] |
| 플랫폼 매뉴얼 | ✅ [[2026-03-30-DAKER_플랫폼_매뉴얼]] |
| DACON 통합계획 | 🔄 [[2026-04-01-DAKER_dacon통합계획]] |

---

## 1. Overview

### 1.1 Design Goals

| # | 목표 | 측정 방법 |
|---|------|----------|
| G1 | 파일럿 3~5사 계약을 **2주 내** 체결 가능한 경량 법무 구조 | 계약서 서명 Lead Time ≤ 10일 |
| G2 | 구독 상태를 **단일 진실 소스(.subscription)** 로 통합 | 수동 엑셀 관리 제거 |
| G3 | AI 크레딧 **측정·차감·충전** MVP를 6주 내 배포 | Credit Usage API 실 트래픽 처리 |
| G4 | 세금계산서 발행·수신확인 **월 1회 < 30분** 소요 | 기존 수기 1건 2시간 → 30분 |
| G5 | 파일럿 KPI(MAU·해커톤 건수·NPS) **실시간 대시보드** | Grafana 또는 Metabase 쿼리 ≤ 10s |

### 1.2 Design Principles

1. **Minimum Viable Contract** — 법무는 파일럿 1페이지 계약서 + 기본약관 참조 방식
2. **CMS-first, Billing-later** — Q2는 CMS에 구독 상태, Q3에 결제 자동화
3. **Credit Ledger는 불변** — 차감은 append-only 이벤트로 감사 추적 가능
4. **Re-use daker.ai 어드민** — 신규 CMS 안 만들고 기존 어드민([[2026-03-30-DAKER_플랫폼_매뉴얼]] §7)에 탭 추가
5. **External Tool 위임** — 세금계산서는 SmartBill/Bill36524, 결제는 Q3부터 토스페이먼츠

---

## 2. Architecture

### 2.1 전체 시스템 다이어그램 (Q2 MVP)

```
┌────────────────────────────────────────────────────────────────┐
│                        세일즈 (대표·전략팀)                    │
└────────────────────────┬───────────────────────────────────────┘
                         │ 1. 미팅·제안
                         ▼
                 ┌──────────────┐
                 │ 계약서 템플릿  │ (Google Docs · 전자서명 모두싸인)
                 └──────┬───────┘
                        │ 2. 서명 완료
                        ▼
┌────────────────────────────────────────────────────────────────┐
│                  daker.ai 어드민 (신규 Subscription 탭)         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐ │
│  │ 구독 상태    │  │ AI 크레딧    │  │ KPI 대시보드         │ │
│  │ Subscription │  │ Credit Ledger│  │ MAU / 개최수 / NPS   │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────────────┘ │
└─────────┼──────────────────┼──────────────────┼───────────────┘
          │ 3. 구독 활성     │ 4. 크레딧 차감   │ 5. 통계 조회
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────┐
│                      MongoDB (daker.ai DB)                  │
│   subscriptions · credit_ledger · invoices · usage_events   │
└─────────────────────────────────────────────────────────────┘
          │
          │ 6. 월말 집계
          ▼
┌──────────────────────────────────────────────┐
│  세금계산서 발행 (SmartBill 수동 연동)         │
│  · 사업자번호 · 품목 · 금액 · 비고(크레딧 내역)│
└──────────────────────────────────────────────┘
```

### 2.2 Q3 자동화 다이어그램 (참고)

```
고객 셀프서비스 포털 → 토스페이먼츠 빌링 API → 자동 세금계산서
                   ↓
              daker.ai DB (웹훅 수신)
```

### 2.3 Dependencies

| 컴포넌트 | 의존 | 목적 |
|---------|------|------|
| Subscription CMS 탭 | daker.ai 어드민 (기존) | 기존 권한·레이아웃 재사용 |
| Credit Ledger | daker.ai DB (MongoDB) | 이벤트 저장 |
| AI 기능 호출부 (채점·멘토링) | Credit Ledger | 차감 이벤트 publish |
| 계약서 생성 | Google Docs API + 모두싸인 | 전자서명 |
| 세금계산서 | SmartBill (수동 CSV upload) | 국세청 제출 |
| KPI 대시보드 | MongoDB → Metabase | 시각화 |

---

## 3. Data Model

### 3.1 Entity: `subscriptions`

```typescript
interface Subscription {
  _id: ObjectId;
  customerId: ObjectId;            // 고객 조직 ID (신규 customers 컬렉션 참조)
  plan: 'starter' | 'growth' | 'enterprise';
  status: 'pilot_free' | 'pilot_discount' | 'active' | 'churned' | 'paused';
  pilotPhase?: '1-3M' | '4-6M' | '7-9M' | '10-12M';
  contract: {
    startDate: Date;
    endDate: Date;                 // 12개월 후
    monthlyAmountKRW: number;      // 현재 월 청구액 (단계별 변동)
    discountPolicy: {              // 할인 스케줄
      phase: string;
      percentOff: number;
      effectiveFrom: Date;
      effectiveTo: Date;
    }[];
    documentUrl: string;           // 모두싸인 계약서 PDF URL
    signedAt: Date;
  };
  features: {
    hackathonQuota: number | 'unlimited';
    adminSeats: number;
    whitelabel: boolean;
    ssoEnabled: boolean;
    creditsIncludedPerMonth: number;
  };
  owners: {
    customerPrimaryEmail: string;
    customerBillingEmail: string;
    daconCsm: string;              // 전담 CSM 직원 ID
  };
  successCriteria: {
    targetMauMonthly: number;
    targetHackathonsMonthly: number;
    npsTarget: number;
  };
  metadata: {
    track: 'A_research' | 'B_university' | 'C_enterprise';
    notes: string;
  };
  createdBy: ObjectId;
  createdAt: Date;
  updatedAt: Date;
}
```

### 3.2 Entity: `customers`

```typescript
interface Customer {
  _id: ObjectId;
  name: string;                    // "한국기계연구원"
  type: 'research_institute' | 'university' | 'enterprise' | 'public';
  businessNumber: string;          // 사업자등록번호 (세금계산서용)
  billingAddress: string;
  primaryContactName: string;
  primaryContactEmail: string;
  primaryContactPhone: string;
  billingContactName: string;
  billingContactEmail: string;
  historicalProjects: {            // 데이콘과 기존 프로젝트 이력
    projectName: string;
    year: number;
    amount: number;
  }[];
  createdAt: Date;
  updatedAt: Date;
}
```

### 3.3 Entity: `credit_ledger` (Append-Only)

```typescript
interface CreditLedgerEntry {
  _id: ObjectId;
  subscriptionId: ObjectId;
  type: 'grant' | 'consume' | 'purchase' | 'expire' | 'refund';
  amount: number;                  // 양수: grant/purchase, 음수: consume/expire
  balance: number;                 // 이벤트 후 잔액 (snapshot, 감사 편의)
  reason: string;                  // "monthly_grant_202605" | "auto_grading_submission_<id>"
  refId?: ObjectId;                // 연관된 Submission·Mentoring·Purchase ID
  costKRW?: number;                // 원가 추적 (Gemini API 실비 등)
  createdAt: Date;
}
```

**불변성 규칙**: `credit_ledger` 는 UPDATE/DELETE 금지, 보정은 역방향 entry 추가로만.

### 3.4 Entity: `invoices`

```typescript
interface Invoice {
  _id: ObjectId;
  subscriptionId: ObjectId;
  customerId: ObjectId;
  period: { year: number; month: number };
  items: {
    description: string;           // "DAKER Growth 월구독 (2026-05)" | "AI 크레딧 500"
    quantity: number;
    unitPriceKRW: number;
    amountKRW: number;
  }[];
  subtotalKRW: number;
  vatKRW: number;                  // 부가세 10%
  totalKRW: number;
  status: 'draft' | 'issued' | 'paid' | 'overdue' | 'cancelled';
  taxInvoiceNumber?: string;       // SmartBill 발행번호
  issuedAt?: Date;
  paidAt?: Date;
  createdAt: Date;
}
```

### 3.5 Entity: `usage_events` (집계용)

```typescript
interface UsageEvent {
  _id: ObjectId;
  subscriptionId: ObjectId;
  date: Date;                      // YYYY-MM-DD (day-bucket)
  metric: 'mau' | 'hackathon_started' | 'submission_count' | 'credit_consumed' | 'admin_login';
  value: number;
  createdAt: Date;
}
```

### 3.6 Relationships

```
Customer  1 ──── N  Subscription
Subscription 1 ──── N  CreditLedgerEntry
Subscription 1 ──── N  Invoice
Subscription 1 ──── N  UsageEvent
```

### 3.7 MongoDB Indexes

| Collection | Index | Purpose |
|-----------|-------|---------|
| subscriptions | `{customerId:1, status:1}` | 고객별 활성 구독 조회 |
| subscriptions | `{'contract.endDate':1}` | 갱신 예정 조회 |
| credit_ledger | `{subscriptionId:1, createdAt:-1}` | 최근 이벤트 조회 |
| credit_ledger | `{type:1, createdAt:-1}` | 원가 집계 |
| invoices | `{subscriptionId:1, 'period.year':1, 'period.month':1}` | 월별 청구 |
| usage_events | `{subscriptionId:1, date:-1, metric:1}` | 대시보드 쿼리 |

---

## 4. API Specification

### 4.1 Endpoint List (신규)

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | /admin/api/subscriptions | 구독 목록 | Admin |
| POST | /admin/api/subscriptions | 구독 생성 (수동) | Admin |
| PUT | /admin/api/subscriptions/:id | 구독 상태·계약 업데이트 | Admin |
| POST | /admin/api/subscriptions/:id/grant-credits | 월 정기 충전 | Admin |
| GET | /admin/api/subscriptions/:id/ledger | 크레딧 거래내역 | Admin |
| POST | /api/internal/credits/consume | AI 기능에서 차감 (서버 간) | Service-Token |
| GET | /api/internal/credits/balance | 현재 잔액 조회 | Service-Token |
| GET | /admin/api/invoices | 청구서 목록 | Admin |
| POST | /admin/api/invoices/:id/issue | 세금계산서 발행 표시 | Admin |
| GET | /admin/api/dashboard/kpi | 파일럿 KPI | Admin |

### 4.2 상세 — Credit Consume (Core)

#### `POST /api/internal/credits/consume`

**Request:**
```json
{
  "subscriptionId": "665f...",
  "amount": 2,
  "reason": "auto_grading_submission_665abc",
  "refId": "665abc...",
  "costKRW": 80
}
```

**Response (200 OK):**
```json
{
  "ok": true,
  "newBalance": 998,
  "ledgerId": "665z..."
}
```

**Error Responses:**
- `402 Insufficient Credits`: 잔액 부족 → AI 기능 측에서 Paywall 표시
- `403 Forbidden`: 구독 status != 'active'/'pilot_*'
- `409 Conflict`: 동일 refId 중복 차감 방지 (idempotency)

**Idempotency 키**: `refId + reason` 조합으로 중복 호출 방지 (24시간 TTL)

### 4.3 상세 — KPI Dashboard API

#### `GET /admin/api/dashboard/kpi?subscriptionId=<id>&period=2026-05`

**Response:**
```json
{
  "mau": 72,
  "hackathonsStarted": 2,
  "submissionCount": 340,
  "creditsConsumed": 680,
  "creditsGranted": 1000,
  "creditsBalance": 320,
  "npsScore": 42,
  "adminLoginCount": 18,
  "lastActivity": "2026-05-28T14:30:00Z",
  "greenYellowRed": "green"
}
```

### 4.4 세일즈→계약→온보딩 플로우

```
[1] 대표가 미팅 후 "파일럿 확정" 결정
   │
[2] 어드민에서 customer 신규 생성 (수동 입력)
   │
[3] 어드민에서 subscription 신규 생성
    · plan = 'growth' (예시)
    · status = 'pilot_free'
    · contract.startDate = 계약 시작일
    · discountPolicy 3단계 입력 (1-3M/4-6M/7-12M)
   │
[4] 시스템이 계약서 PDF 자동 생성
    · 템플릿 + subscription 데이터 머지
    · Google Docs API 또는 로컬 MD→PDF 변환
   │
[5] 모두싸인으로 고객에게 전자서명 요청
   │
[6] 서명 완료 웹훅 수신 → subscription.status = 'pilot_free' (공식 활성)
    · contract.documentUrl 저장
    · contract.signedAt 기록
   │
[7] 어드민에서 "킥오프 체크리스트" 페이지 열리며 10일 플로우 시작
    · customer에 admin seat 초대
    · whitelabel 설정 (Growth 이상)
    · 크레딧 grant (첫 월 선 지급)
```

---

## 5. UI/UX Design

### 5.1 Admin — Subscription 탭 화면

```
┌─────────────────────────────────────────────────────────────────┐
│ DAKER Admin                                [ 대표 ▼ ] [ 로그아웃 ]│
├─────────────────────────────────────────────────────────────────┤
│ 대시보드  이벤트  사용자  [✨ 구독]  설문  통계                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [+ 새 구독] [필터: 전체 ▼] [ 검색 ]                            │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ 고객명          | 플랜    | 상태          | MRR    | ... │ │
│  ├───────────────────────────────────────────────────────────┤ │
│  │ 한국기계연구원  | Growth | pilot_free    | ₩0     | 🟢 │ │
│  │ 한양대 SW대학   | Starter| pilot_free    | ₩0     | 🟢 │ │
│  │ ...                                                       │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 Admin — 구독 상세

```
┌─────────────────────────────────────────────────────────────────┐
│ ← 구독 상세 · 한국기계연구원 (Growth)                           │
├─────────────────────────────────────────────────────────────────┤
│ [개요] [크레딧] [청구] [KPI] [킥오프] [설정]                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ 상태: pilot_free (1-3M 단계)          계약: 2026-05-15~2027-05-14 │
│                                                                 │
│ ┌─── 할인 스케줄 ──────────────────────────────────────┐       │
│ │ ✅ 1-3M  무료        ₩0         (05-15 ~ 08-14)     │       │
│ │ ⏳ 4-6M  50% 할인   ₩1,245,000  (08-15 ~ 11-14)     │       │
│ │ ⏳ 7-12M 연계약가   ₩1,990,000  (11-15 ~ 2027-05-14)│       │
│ └─────────────────────────────────────────────────────┘       │
│                                                                 │
│ ┌─── 성공 기준 (Green/Yellow/Red) ─────────────────────┐      │
│ │ MAU:          72 / 목표 80     🟡                    │      │
│ │ 해커톤:         2 / 목표 2     🟢                    │      │
│ │ NPS:          42 / 목표 30     🟢                    │      │
│ │ 관리자 로그인: 18회 / 주3회     🟢                    │      │
│ └──────────────────────────────────────────────────────┘      │
│                                                                 │
│ [할인 전환] [구독 일시정지] [계약서 보기]                       │
└─────────────────────────────────────────────────────────────────┘
```

### 5.3 Admin — Credit Ledger 탭

```
┌─────────────────────────────────────────────────────────────────┐
│ 크레딧 · 한국기계연구원                  잔액: 320 (/1,000 월)  │
├─────────────────────────────────────────────────────────────────┤
│ [+ 수동 충전] [엑셀 내보내기]                                   │
│                                                                 │
│ 날짜        | 타입    | 내역                     | 증감 | 잔액  │
│ 2026-05-01 | grant   | 월 정기 충전             | +1000| 1000 │
│ 2026-05-03 | consume | 제출물 자동채점 (sub 123)| -2   |  998 │
│ ...                                                             │
└─────────────────────────────────────────────────────────────────┘
```

### 5.4 User Flow (관리자 관점)

```
[로그인]
   │
   ▼
[구독 탭 진입] → [구독 상세] → [KPI 확인]
   │                 │              │
   │                 ▼              ▼
   │         [할인 전환 버튼]  [Green/Yellow/Red 판정]
   │                 │              │
   │                 ▼              ▼
   │        [다음 단계로]    [CSM에게 알림]
   ▼
[새 구독 생성] → [고객 정보 입력] → [계약서 생성] → [모두싸인 전송]
```

### 5.5 Component List

| Component | Location | Responsibility |
|-----------|----------|----------------|
| SubscriptionList | src/features/subscription/components/ | 목록 테이블 |
| SubscriptionDetail | src/features/subscription/components/ | 상세 뷰 탭 구조 |
| DiscountTimeline | src/features/subscription/components/ | 할인 단계 UI |
| CreditLedger | src/features/credit/components/ | 크레딧 거래내역 |
| KPICard | src/features/dashboard/components/ | KPI 카드 (G/Y/R) |
| ContractPreview | src/features/contract/components/ | 계약서 PDF 미리보기 |

---

## 6. Error Handling

### 6.1 Error Code Definition

| Code | Scenario | 처리 |
|------|---------|------|
| SUB-001 | 구독 상태가 active/pilot_* 가 아닌데 AI 기능 호출 | 402 반환, 사용자에 "구독 만료 안내" |
| SUB-002 | 잔액 부족 | 402 반환, 관리자에 "크레딧 충전 필요" 알림 |
| SUB-003 | 중복 차감 시도 | 409 반환, idempotency 키로 기존 결과 반환 |
| SUB-004 | 계약 종료 7일 전 | 배너 노출 + CSM 알림 |
| BILL-001 | 세금계산서 발행 실패 | 관리자 수동 재발행 큐 |
| BILL-002 | SmartBill 사업자번호 불일치 | customer 정보 검증 페이지 이동 |
| CONT-001 | 모두싸인 서명 거부 | subscription.status = 'paused' → 재협상 |

### 6.2 Error Response Format

```json
{
  "error": {
    "code": "SUB-002",
    "message": "크레딧 잔액이 부족합니다. 관리자에 충전을 요청하세요.",
    "details": {
      "required": 5,
      "balance": 2,
      "subscriptionId": "665f...",
      "purchaseUrl": "/admin/subscriptions/665f/credits/purchase"
    }
  }
}
```

### 6.3 Monitoring & Alerting

| 이벤트 | 채널 | 수신자 |
|--------|------|--------|
| 신규 구독 생성 | Slack #daker-sales | 대표·전략팀 |
| 계약 서명 완료 | Slack #daker-sales | 대표·CSM |
| 크레딧 잔액 <20% | Slack #daker-cs | CSM |
| 월 KPI Red 판정 | Slack #daker-cs | CSM·대표 |
| 계약 종료 30일전 | 이메일 + Slack | 대표 |

---

## 7. Security Considerations

- [x] **계약서 PDF 암호화 저장** (S3 KMS, 접근 로그 감사)
- [x] **사업자번호·금액 등 PII 접근 제한** (Admin Role만)
- [x] **Credit API는 서비스 토큰 필수** (사용자 세션으로 직접 차감 불가)
- [x] **Idempotency Key** 로 동시성·재시도 안전 처리
- [x] **HTTPS·Helmet·Rate Limit** (기존 daker.ai 인프라 재사용)
- [x] **모두싸인 Webhook 서명 검증** (HMAC-SHA256)
- [ ] **SSO 연동 (Growth+)** — [[2026-04-01-DAKER_dacon통합계획]] Sprint 2 완료 대기
- [ ] **감사 로그 (Enterprise)** — Q4에 별도 설계

---

## 8. Test Plan

### 8.1 Test Scope

| Type | Target | Tool |
|------|--------|------|
| Unit | Credit Ledger 계산·차감 로직 | Vitest |
| Integration | /credits/consume 엔드포인트 | Supertest |
| E2E | 구독 생성 → 계약 → 서명 → 활성 | Playwright |
| Manual | 모두싸인·SmartBill 연동 | 운영 시나리오 |
| Load | 크레딧 차감 동시성 (1000 TPS) | k6 |

### 8.2 Test Cases (Key)

- [ ] Happy: Starter 구독 신규 생성 → 서명 → 활성 → 첫 크레딧 차감까지 성공
- [ ] Happy: 할인 단계 자동 전환 (3개월 후 status 변경)
- [ ] Error: 잔액 0에서 consume 호출 → 402 반환
- [ ] Error: 동일 refId 중복 차감 → 409 반환, ledger 1건만 기록
- [ ] Edge: 월 말(23:59)에 grant 발생 → 다음 달 사용 가능
- [ ] Edge: 계약 종료일 당일 AI 호출 → 정상 처리 / 다음날 차단
- [ ] Security: 비-Admin 사용자가 /admin/subscriptions 접근 → 403
- [ ] Security: 잘못된 서비스 토큰으로 /internal/credits 호출 → 401

---

## 9. Clean Architecture

### 9.1 Layer Structure (DAKER 기준 적용)

| Layer | 책임 | 위치 |
|-------|------|------|
| **Presentation** | Admin UI 구독·크레딧·청구 페이지 | `src/features/subscription/components/` |
| **Application** | 구독 라이프사이클·차감 Use Case | `src/features/subscription/services/` |
| **Domain** | 구독·크레딧·청구 엔티티·정책 | `src/domain/subscription/` |
| **Infrastructure** | MongoDB·모두싸인·SmartBill·Slack | `src/infrastructure/` |

### 9.2 Dependency Rules

```
Admin UI (Presentation)
       ↓ (Use Case 호출)
Subscription Service (Application)
       ↓ (Domain 로직 호출)
Domain Policy (무상태·순수 함수)
       ↑ (Repository 인터페이스만 노출)
MongoDB Adapter / Webhook Handler (Infrastructure)
```

### 9.3 File Import Rules

| From | Can Import | Cannot Import |
|------|-----------|---------------|
| Presentation | Application, Domain | Infrastructure 직접 |
| Application | Domain, Infrastructure Interface | Presentation |
| Domain | (pure) | 외부 라이브러리 |
| Infrastructure | Domain | Application, Presentation |

### 9.4 Feature Layer Assignment

| Component | Layer | Location |
|-----------|-------|----------|
| SubscriptionListPage | Presentation | `src/features/subscription/pages/List.tsx` |
| SubscriptionService | Application | `src/features/subscription/services/SubscriptionService.ts` |
| CreditConsumePolicy | Domain | `src/domain/credit/ConsumePolicy.ts` |
| MongoSubscriptionRepo | Infrastructure | `src/infrastructure/mongo/SubscriptionRepository.ts` |
| ModuSignClient | Infrastructure | `src/infrastructure/modusign/Client.ts` |
| SmartBillAdapter | Infrastructure | `src/infrastructure/smartbill/Adapter.ts` |

---

## 10. Coding Convention

### 10.1 Naming

| 대상 | 규칙 | 예시 |
|------|------|------|
| React 컴포넌트 | PascalCase | `SubscriptionDetail` |
| Service 클래스 | PascalCase | `SubscriptionService` |
| 파일 (컴포넌트) | PascalCase.tsx | `SubscriptionDetail.tsx` |
| 파일 (서비스) | PascalCase.ts | `SubscriptionService.ts` |
| MongoDB 컬렉션 | snake_case 복수 | `subscriptions`, `credit_ledger` |
| API 경로 | kebab-case | `/admin/api/subscriptions/:id` |
| 이벤트 이름 | snake_case | `subscription_created`, `credits_consumed` |

### 10.2 Environment Variables

| Prefix | 용도 | 예시 |
|--------|------|------|
| `DAKER_MODUSIGN_API_KEY` | 전자서명 | 서버만 |
| `DAKER_SMARTBILL_API_KEY` | 세금계산서 | 서버만 |
| `DAKER_SLACK_WEBHOOK_SALES` | 알림 | 서버만 |
| `DAKER_CREDIT_SERVICE_TOKEN` | 내부 API 인증 | 서버만 |
| `DAKER_GEMINI_COST_MULTIPLIER` | 크레딧 원가 승수 (기본 1.8) | 서버만 |

### 10.3 This Feature's Conventions

| 항목 | 규칙 |
|------|------|
| Mongo schema 검증 | Zod schema → Mongoose 연동 |
| Currency | 항상 KRW 정수 (원 단위, 소수점 없음) |
| Date 처리 | dayjs + Asia/Seoul 고정 |
| Error 직렬화 | 오류 코드(`SUB-001`) + 영문 messageKey + 한국어 message |
| 로깅 | pino JSON 로그, `subscriptionId` 필수 필드 |

---

## 11. Implementation Guide

### 11.1 File Structure (신규 추가분만)

```
daker.ai/
├── src/
│   ├── features/
│   │   ├── subscription/
│   │   │   ├── pages/
│   │   │   │   ├── List.tsx
│   │   │   │   └── Detail.tsx
│   │   │   ├── components/
│   │   │   │   ├── DiscountTimeline.tsx
│   │   │   │   ├── KPICard.tsx
│   │   │   │   └── ContractPreview.tsx
│   │   │   ├── services/
│   │   │   │   └── SubscriptionService.ts
│   │   │   └── types/
│   │   │       └── Subscription.ts
│   │   └── credit/
│   │       ├── components/
│   │       │   └── CreditLedger.tsx
│   │       ├── services/
│   │       │   └── CreditService.ts
│   │       └── types/
│   │           └── Credit.ts
│   ├── domain/
│   │   ├── subscription/
│   │   │   ├── DiscountPolicy.ts
│   │   │   └── SubscriptionStateMachine.ts
│   │   └── credit/
│   │       └── ConsumePolicy.ts
│   └── infrastructure/
│       ├── mongo/
│       │   ├── SubscriptionRepository.ts
│       │   └── CreditLedgerRepository.ts
│       ├── modusign/
│       │   └── Client.ts
│       └── smartbill/
│           └── Adapter.ts
└── templates/
    └── contracts/
        ├── pilot_starter.md
        └── pilot_growth.md
```

### 11.2 Implementation Order (Sprint 2, 2026-05-10 ~ 2026-06-20)

**Week 1 (5/10~5/16)**
1. [ ] MongoDB 스키마·인덱스 생성 (`subscriptions`, `customers`)
2. [ ] Domain 타입·정책 순수 함수 (`DiscountPolicy`, `SubscriptionStateMachine`)
3. [ ] Admin 라우팅·권한 확인

**Week 2 (5/17~5/23)**
4. [ ] `SubscriptionService` CRUD 구현
5. [ ] 목록·상세 페이지 UI
6. [ ] 계약서 템플릿 MD (Starter/Growth 2종)
7. [ ] 모두싸인 연동 클라이언트 (전송·웹훅 수신)

**Week 3 (5/24~5/30)**
8. [ ] `credit_ledger` 스키마·인덱스
9. [ ] `/api/internal/credits/consume` + `/balance` 엔드포인트
10. [ ] Idempotency 미들웨어
11. [ ] 기존 AI 기능 호출부 3곳 (자동채점·멘토링·코드리뷰) 크레딧 차감 연동

**Week 4 (5/31~6/6)**
12. [ ] Credit Ledger UI + 수동 충전 기능
13. [ ] `usage_events` 집계 job (Cron, 1시간 간격)
14. [ ] KPI 대시보드 API + UI 카드

**Week 5 (6/7~6/13)**
15. [ ] SmartBill 수동 연동 (CSV 포맷 생성 도구)
16. [ ] 월말 배치 스크립트 (invoices draft 자동 생성)
17. [ ] Slack 알림 연동 (생성·서명·Red 경고)

**Week 6 (6/14~6/20)**
18. [ ] E2E 테스트 시나리오
19. [ ] 부하 테스트 (k6로 1000 TPS 크레딧 차감)
20. [ ] 파일럿 1사 리허설 (internal dogfooding)
21. [ ] 문서화 (운영 매뉴얼·CSM 가이드)

### 11.3 Rollout Plan

1. **Soft launch** — Admin 탭 feature flag `subscription_v1_enabled` 로 배포, 대표 계정만 활성
2. **Internal test** — 더미 고객 1개 생성해 전체 플로우 리허설
3. **Pilot 1호** — 기계연 계약 시점에 Feature flag 전체 활성
4. **Stabilize** — 파일럿 3사 온보딩 후 Q3 초 공개 빌링 자동화 단계로 이관

### 11.4 Out of Scope (이번 파일럿 설계 제외)

- 고객 셀프서비스 포털 (Q3)
- 토스페이먼츠 빌링 자동 결제 (Q3)
- 크레딧 자동충전 구매 (Q3)
- 감사 로그 풀 (Q4, Enterprise 필수)
- 커스텀 도메인·SSO OIDC (Q4, Enterprise 옵션)

---

## 12. Open Questions & Decisions

| # | 질문 | 현재 방향 | 결정 필요 시점 |
|---|------|----------|---------------|
| Q1 | 전자서명 도구: 모두싸인 vs 도큐사인 | 모두싸인 (국내 사업자 편의) | 5/5 이전 |
| Q2 | 세금계산서: SmartBill vs Bill36524 | SmartBill (수동 MVP) | 5/10 이전 |
| Q3 | 크레딧 만료 정책: 롤오버 vs 월별 리셋 | 월별 리셋 + 구매분 90일 유효 | 5/10 이전 |
| Q4 | 계약서 언어: 한국어 only vs 영문 병기 | 한국어 only (파일럿), 영문은 Enterprise | — |
| Q5 | CSM 리소스: 대표 겸임 vs 신규 채용 | 파일럿은 대표·전략팀 겸임, Q3부터 전담 1인 | — |

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 0.1 | 2026-04-17 | Initial draft | edgar@dacon.io |

---

> 본 설계서는 Sprint 2 착수(2026-05-10) 이전 v0.2로 갱신하며, 법무·회계 검토 반영 후 v1.0 확정.
