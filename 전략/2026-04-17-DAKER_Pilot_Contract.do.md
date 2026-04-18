---
created: 2026-04-17
updated: 2026-04-17
author: edgar@dacon.io
status: in_progress
priority: critical
tags: [project, daker, pdca, do, implementation, handoff]
project_name: DAKER B2B 월구독 전환
feature: DAKER-Pilot-Contract
phase: PDCA-Do
pdca_cycle: "2026-Q2-Pilot"
sprint: Sprint-2
sprint_start: 2026-05-10
sprint_end: 2026-06-20
design_doc: [[2026-04-17-DAKER_Pilot_Contract.design]]
decisions_doc: [[2026-04-17-DAKER_Pilot_Design_Decisions]]
---

# DAKER-Pilot-Contract Implementation Guide (Do Phase)

> **Summary**: Sprint 2 (2026-05-10 ~ 2026-06-20) 6주 실행 핸드오프 키트. 개발팀이 복사-붙여넣기로 착수할 수 있는 스켈레톤·스크립트·체크리스트 수록.
>
> **Project**: DAKER (daker.ai)
> **Version**: 0.1
> **Author**: edgar@dacon.io
> **Date**: 2026-04-17
> **Status**: In Progress (Sprint 2 착수 대기)
> **Design Doc**: [[2026-04-17-DAKER_Pilot_Contract.design]]
> **Decisions Doc**: [[2026-04-17-DAKER_Pilot_Design_Decisions]]

---

## 1. Pre-Implementation Checklist

### 1.1 Documents Verified

- [x] 기획서: [[2026-04-17-DAKER_B2B_월구독_서비스_기획서]]
- [x] PDCA Plan: [[2026-04-17-DAKER_B2B_PDCA_Plan]]
- [x] Design: [[2026-04-17-DAKER_Pilot_Contract.design]]
- [x] Open Questions 해소: [[2026-04-17-DAKER_Pilot_Design_Decisions]]
- [x] 계약서 템플릿: `계약서_템플릿/DAKER_Pilot_{Starter,Growth}_계약서.md`
- [ ] 법무 검토 완료 (v0.1 → v1.0) — **블로커, 5/5까지**

### 1.2 Environment Ready

- [ ] **모두싸인 Enterprise 계정** 개설 + API 키 발급 (5/3)
- [ ] **SmartBill B2B 계정** 개설 + API 키 발급 (5/3)
- [ ] **Slack 채널** `#daker-sales`, `#daker-cs` 생성
- [ ] **Gemini API 원가 추적용 대시보드** 설정 (Google Cloud Console)
- [ ] daker.ai 로컬 개발 환경 구동 확인 (`http://localhost:5000`)
- [ ] 스테이징 환경 `test1.daker.ai` 접근 확인
- [ ] MongoDB 스테이징 DB 백업 (변경 전 스냅샷)

### 1.3 Blocker Resolution

| 블로커 | 담당 | 데드라인 | 상태 |
|--------|------|---------|------|
| 법무 계약서 v1.0 | 행정팀 + 외주 변호사 | 2026-05-05 | 🔴 대기 |
| 모두싸인 API 키 | 대표 | 2026-05-03 | 🔴 대기 |
| SmartBill API 키 | 행정팀 | 2026-05-03 | 🔴 대기 |
| DACON SSO 연동 | 개발팀 (별건) | 2026-06-30 | 🟡 진행 중 |

---

## 2. Implementation Order (Sprint 2, 6주)

> Design §11.2 기준. 각 주차 끝에 Slack #daker-dev 에 진척 공유.

### 2.1 Week 1 (5/10~5/16) — Data Layer

| 우선순위 | 작업 | 파일/위치 | 상태 |
|:--------:|------|-----------|:----:|
| 1 | Subscription·Customer Mongoose 스키마 | `src/domain/subscription/schemas.ts` | ☐ |
| 2 | Credit Ledger 스키마 (Append-only 검증) | `src/domain/credit/schemas.ts` | ☐ |
| 3 | MongoDB Index 생성 (migration) | `scripts/migrations/001-subscription-init.ts` | ☐ |
| 4 | Zod validation schemas | `src/domain/subscription/validators.ts` | ☐ |
| 5 | Domain 정책 순수 함수 (할인·상태기계) | `src/domain/subscription/DiscountPolicy.ts` | ☐ |
| 6 | Unit test (할인 계산·상태 전환) | `src/domain/subscription/__tests__/` | ☐ |

### 2.2 Week 2 (5/17~5/23) — Subscription Service & UI

| 우선순위 | 작업 | 파일/위치 | 상태 |
|:--------:|------|-----------|:----:|
| 7 | SubscriptionRepository (Mongo) | `src/infrastructure/mongo/SubscriptionRepository.ts` | ☐ |
| 8 | SubscriptionService (CRUD) | `src/features/subscription/services/SubscriptionService.ts` | ☐ |
| 9 | Admin `/admin/api/subscriptions` REST | `src/features/subscription/routes.ts` | ☐ |
| 10 | Admin 목록 페이지 UI | `src/features/subscription/pages/List.tsx` | ☐ |
| 11 | Admin 상세 페이지 (탭 구조) | `src/features/subscription/pages/Detail.tsx` | ☐ |
| 12 | 계약서 템플릿 MD (2종 확정) | `templates/contracts/*.md` | ☐ |
| 13 | 모두싸인 클라이언트 + 웹훅 | `src/infrastructure/modusign/` | ☐ |

### 2.3 Week 3 (5/24~5/30) — Credit Ledger Core

| 우선순위 | 작업 | 파일/위치 | 상태 |
|:--------:|------|-----------|:----:|
| 14 | CreditLedgerRepository (append-only 강제) | `src/infrastructure/mongo/CreditLedgerRepository.ts` | ☐ |
| 15 | CreditService (grant/consume/purchase) | `src/features/credit/services/CreditService.ts` | ☐ |
| 16 | Idempotency 미들웨어 (Redis) | `src/middleware/idempotency.ts` | ☐ |
| 17 | `POST /api/internal/credits/consume` | `src/features/credit/routes.ts` | ☐ |
| 18 | `GET /api/internal/credits/balance` | `src/features/credit/routes.ts` | ☐ |
| 19 | 기존 AI 기능 3곳 연동 (자동채점·멘토링·코드리뷰) | Each AI feature module | ☐ |
| 20 | Integration test (동시성·중복) | `src/features/credit/__tests__/` | ☐ |

### 2.4 Week 4 (5/31~6/6) — UI & KPI

| 우선순위 | 작업 | 파일/위치 | 상태 |
|:--------:|------|-----------|:----:|
| 21 | Credit Ledger UI + 수동 충전 | `src/features/credit/pages/Ledger.tsx` | ☐ |
| 22 | `usage_events` 집계 Cron (1시간) | `src/jobs/usage-aggregator.ts` | ☐ |
| 23 | KPI Dashboard API | `src/features/dashboard/routes.ts` | ☐ |
| 24 | KPI 카드 컴포넌트 (G/Y/R) | `src/features/dashboard/components/KPICard.tsx` | ☐ |
| 25 | Discount Timeline 컴포넌트 | `src/features/subscription/components/DiscountTimeline.tsx` | ☐ |
| 26 | Subscription Detail 탭 통합 | `src/features/subscription/pages/Detail.tsx` | ☐ |

### 2.5 Week 5 (6/7~6/13) — Billing & Alerts

| 우선순위 | 작업 | 파일/위치 | 상태 |
|:--------:|------|-----------|:----:|
| 27 | SmartBill CSV 생성 도구 | `src/infrastructure/smartbill/Adapter.ts` | ☐ |
| 28 | Invoice draft 자동생성 Cron (월말) | `src/jobs/invoice-draft.ts` | ☐ |
| 29 | Slack Webhook 연동 (sales·cs) | `src/infrastructure/slack/Client.ts` | ☐ |
| 30 | 이벤트 → Slack 알림 연동 | `src/domain/events/` | ☐ |
| 31 | 관리자 수동 세금계산서 발행 UI | `src/features/invoice/pages/Issue.tsx` | ☐ |

### 2.6 Week 6 (6/14~6/20) — E2E & Rehearsal

| 우선순위 | 작업 | 파일/위치 | 상태 |
|:--------:|------|-----------|:----:|
| 32 | E2E 시나리오 (Playwright) | `e2e/subscription.spec.ts` | ☐ |
| 33 | Load test (k6, 1000 TPS consume) | `load-test/credits-consume.js` | ☐ |
| 34 | Feature flag `subscription_v1_enabled` | `src/config/featureFlags.ts` | ☐ |
| 35 | Internal dogfooding (더미 고객 1) | Ops | ☐ |
| 36 | 운영 매뉴얼 작성 (CSM용) | `docs/ops/subscription-handbook.md` | ☐ |
| 37 | Rollback runbook | `docs/ops/rollback.md` | ☐ |

---

## 3. Key Files to Create

### 3.1 신규 파일 (40여개)

> Design §11.1 구조 기준. 아래는 **필수 경로**만 정리.

```
daker.ai/
├── src/
│   ├── domain/
│   │   ├── subscription/
│   │   │   ├── schemas.ts              # Mongoose schemas
│   │   │   ├── validators.ts           # Zod validation
│   │   │   ├── DiscountPolicy.ts       # 순수 함수
│   │   │   ├── SubscriptionStateMachine.ts
│   │   │   └── __tests__/
│   │   └── credit/
│   │       ├── schemas.ts
│   │       └── ConsumePolicy.ts
│   ├── infrastructure/
│   │   ├── mongo/
│   │   │   ├── SubscriptionRepository.ts
│   │   │   ├── CreditLedgerRepository.ts
│   │   │   └── UsageEventRepository.ts
│   │   ├── modusign/Client.ts
│   │   ├── smartbill/Adapter.ts
│   │   └── slack/Client.ts
│   ├── features/
│   │   ├── subscription/
│   │   │   ├── routes.ts
│   │   │   ├── services/SubscriptionService.ts
│   │   │   ├── pages/{List,Detail}.tsx
│   │   │   └── components/
│   │   ├── credit/
│   │   │   ├── routes.ts
│   │   │   ├── services/CreditService.ts
│   │   │   └── pages/Ledger.tsx
│   │   ├── invoice/
│   │   │   ├── routes.ts
│   │   │   └── pages/Issue.tsx
│   │   └── dashboard/
│   │       ├── routes.ts
│   │       └── components/KPICard.tsx
│   ├── middleware/idempotency.ts
│   ├── jobs/
│   │   ├── usage-aggregator.ts
│   │   └── invoice-draft.ts
│   └── config/featureFlags.ts
├── scripts/migrations/001-subscription-init.ts
├── templates/contracts/pilot_{starter,growth}.md
├── e2e/subscription.spec.ts
└── load-test/credits-consume.js
```

### 3.2 수정 파일

| 파일 | 변경 | 사유 |
|------|------|------|
| `src/config/index.ts` | 신규 env 읽기 추가 | API 키·서비스 토큰 |
| `src/features/admin/routes.ts` | Subscription 탭 라우팅 | 어드민 통합 |
| `src/features/grading/AutoGradingService.ts` | 크레딧 consume 호출 | 차감 연동 |
| `src/features/mentoring/AiMentoringService.ts` | 크레딧 consume 호출 | 차감 연동 |
| `src/features/review/CodeReviewService.ts` | 크레딧 consume 호출 | 차감 연동 |
| `package.json` | 의존성 추가 | 아래 §4 참조 |
| `.env.example` | 신규 env 추가 | 아래 §4.3 참조 |

---

## 4. Dependencies

### 4.1 Runtime Packages

```bash
# core
pnpm add mongoose@^8 zod@^3 dayjs@^1 pino@^9

# idempotency · cache
pnpm add ioredis@^5

# HTTP client
pnpm add axios@^1

# scheduled jobs
pnpm add node-cron@^3

# CSV (SmartBill)
pnpm add csv-stringify@^6
```

### 4.2 Dev Dependencies

```bash
# testing
pnpm add -D vitest@^1 @vitest/coverage-v8 supertest@^7

# e2e · load
pnpm add -D @playwright/test@^1.45 k6

# types
pnpm add -D @types/node-cron @types/supertest
```

### 4.3 Environment Variables (`.env.example` 추가분)

```bash
# --- Subscription / Contract ---
DAKER_MODUSIGN_API_KEY=
DAKER_MODUSIGN_WEBHOOK_SECRET=
DAKER_MODUSIGN_SENDER_EMAIL=edgar@dacon.io

# --- Billing ---
DAKER_SMARTBILL_API_KEY=
DAKER_SMARTBILL_BUSINESS_NUMBER=000-00-00000

# --- Credit Economics ---
DAKER_CREDIT_SERVICE_TOKEN=
DAKER_GEMINI_COST_MULTIPLIER=1.8

# --- Notifications ---
DAKER_SLACK_WEBHOOK_SALES=
DAKER_SLACK_WEBHOOK_CS=

# --- Feature Flags ---
FEATURE_SUBSCRIPTION_V1=false

# --- Redis (Idempotency) ---
REDIS_URL=redis://localhost:6379
```

---

## 5. Code Skeletons (복사-붙여넣기용)

### 5.1 MongoDB Migration Script

`scripts/migrations/001-subscription-init.ts`

```typescript
import { MongoClient } from 'mongodb'

const uri = process.env.MONGO_URI!
const client = new MongoClient(uri)

async function run() {
  await client.connect()
  const db = client.db()

  // customers
  await db.createCollection('customers')
  await db.collection('customers').createIndex({ businessNumber: 1 }, { unique: true })

  // subscriptions
  await db.createCollection('subscriptions')
  await db.collection('subscriptions').createIndex({ customerId: 1, status: 1 })
  await db.collection('subscriptions').createIndex({ 'contract.endDate': 1 })

  // credit_ledger (append-only, time-based TTL NOT applied)
  await db.createCollection('credit_ledger')
  await db.collection('credit_ledger').createIndex({ subscriptionId: 1, createdAt: -1 })
  await db.collection('credit_ledger').createIndex({ type: 1, createdAt: -1 })

  // invoices
  await db.createCollection('invoices')
  await db.collection('invoices').createIndex(
    { subscriptionId: 1, 'period.year': 1, 'period.month': 1 },
    { unique: true }
  )

  // usage_events
  await db.createCollection('usage_events')
  await db.collection('usage_events').createIndex({ subscriptionId: 1, date: -1, metric: 1 })

  console.log('Migration 001: subscription-init complete')
  await client.close()
}

run().catch((e) => { console.error(e); process.exit(1) })
```

실행:
```bash
pnpm tsx scripts/migrations/001-subscription-init.ts
```

### 5.2 Domain 순수 함수 — `DiscountPolicy.ts`

`src/domain/subscription/DiscountPolicy.ts`

```typescript
import dayjs from 'dayjs'

export type PilotPhase = '1-3M' | '4-6M' | '7-9M' | '10-12M'
export type Plan = 'starter' | 'growth' | 'enterprise'

const PLAN_MONTHLY_KRW: Record<Plan, number> = {
  starter: 890_000,
  growth: 2_490_000,
  enterprise: 6_990_000, // 최소가
}

const PLAN_ANNUAL_KRW: Record<Plan, number> = {
  starter: 790_000,
  growth: 1_990_000,
  enterprise: 0, // custom
}

/**
 * 파일럿 단계별 월 청구액 계산.
 * Starter: 1-3M 무료 → 4-9M 50% → 10-12M 정가
 * Growth:  1-3M 무료 → 4-6M 50% → 7-12M 정가
 */
export function calculatePilotMonthlyAmount(
  plan: Plan,
  contractStart: Date,
  billingMonth: Date
): number {
  const monthsPassed = dayjs(billingMonth).diff(dayjs(contractStart), 'month')
  const annualPrice = PLAN_ANNUAL_KRW[plan]

  if (monthsPassed < 3) return 0 // 1-3M 무료

  if (plan === 'starter') {
    if (monthsPassed < 9) return Math.round(annualPrice * 0.5) // 4-9M 50%
    if (monthsPassed < 12) return annualPrice
  }
  if (plan === 'growth') {
    if (monthsPassed < 6) return Math.round(annualPrice * 0.5) // 4-6M 50%
    if (monthsPassed < 12) return annualPrice
  }

  throw new Error(`Contract expired: monthsPassed=${monthsPassed}`)
}

export function getPilotPhase(plan: Plan, contractStart: Date, now: Date): PilotPhase {
  const m = dayjs(now).diff(dayjs(contractStart), 'month')
  if (m < 3) return '1-3M'
  if (plan === 'starter') {
    if (m < 9) return '4-6M' // Starter 의 50% 기간 라벨
    return '10-12M'
  }
  if (plan === 'growth') {
    if (m < 6) return '4-6M'
    return '7-9M'
  }
  return '10-12M'
}
```

### 5.3 Credit Consume 엔드포인트

`src/features/credit/routes.ts`

```typescript
import { Router } from 'express'
import { CreditService } from './services/CreditService'
import { idempotency } from '../../middleware/idempotency'
import { serviceAuth } from '../../middleware/serviceAuth'
import { z } from 'zod'

const router = Router()

const consumeSchema = z.object({
  subscriptionId: z.string(),
  amount: z.number().int().positive(),
  reason: z.string().min(1).max(200),
  refId: z.string().optional(),
  costKRW: z.number().int().nonnegative().optional(),
})

router.post(
  '/consume',
  serviceAuth,
  idempotency({ ttlSec: 86_400 }),
  async (req, res, next) => {
    try {
      const parsed = consumeSchema.parse(req.body)
      const result = await CreditService.consume(parsed)
      res.json(result)
    } catch (e) {
      next(e)
    }
  }
)

router.get('/balance/:subscriptionId', serviceAuth, async (req, res, next) => {
  try {
    const balance = await CreditService.getBalance(req.params.subscriptionId)
    res.json({ balance })
  } catch (e) {
    next(e)
  }
})

export default router
```

### 5.4 Idempotency Middleware

`src/middleware/idempotency.ts`

```typescript
import type { Request, Response, NextFunction } from 'express'
import Redis from 'ioredis'

const redis = new Redis(process.env.REDIS_URL!)

export function idempotency(opts: { ttlSec: number }) {
  return async (req: Request, res: Response, next: NextFunction) => {
    const key = req.header('Idempotency-Key') || req.body?.refId
    if (!key) return next()

    const cacheKey = `idemp:${req.path}:${key}`
    const cached = await redis.get(cacheKey)
    if (cached) {
      return res.status(200).json(JSON.parse(cached))
    }

    // Intercept res.json to cache response
    const origJson = res.json.bind(res)
    res.json = ((body: unknown) => {
      redis.set(cacheKey, JSON.stringify(body), 'EX', opts.ttlSec).catch(() => {})
      return origJson(body)
    }) as typeof res.json

    next()
  }
}
```

### 5.5 SubscriptionService Skeleton

`src/features/subscription/services/SubscriptionService.ts`

```typescript
import { SubscriptionRepository } from '../../../infrastructure/mongo/SubscriptionRepository'
import { CustomerRepository } from '../../../infrastructure/mongo/CustomerRepository'
import { ModuSignClient } from '../../../infrastructure/modusign/Client'
import { calculatePilotMonthlyAmount, getPilotPhase } from '../../../domain/subscription/DiscountPolicy'
import { slackSales } from '../../../infrastructure/slack/Client'

export class SubscriptionService {
  static async create(input: CreateSubscriptionInput) {
    // 1. Validate customer exists or create new
    const customer = await CustomerRepository.findOrCreate(input.customer)

    // 2. Generate contract from template
    const contractMd = await renderContractTemplate(input.plan, { customer, ...input })

    // 3. Send to ModuSign
    const signatureRequest = await ModuSignClient.sendContract({
      customerEmail: customer.primaryContactEmail,
      contractMd,
      metadata: { subscriptionId: 'tbd' },
    })

    // 4. Create subscription record (status=pending_signature)
    const sub = await SubscriptionRepository.create({
      customerId: customer._id,
      plan: input.plan,
      status: 'pending_signature',
      contract: {
        startDate: input.contractStartDate,
        endDate: dayjs(input.contractStartDate).add(12, 'month').subtract(1, 'day').toDate(),
        monthlyAmountKRW: 0, // 1-3M 무료
        discountPolicy: buildDiscountSchedule(input.plan, input.contractStartDate),
        documentUrl: signatureRequest.docUrl,
        signedAt: null,
      },
      features: resolveFeatures(input.plan),
      owners: input.owners,
      successCriteria: input.successCriteria,
      metadata: input.metadata,
    })

    // 5. Notify sales team
    await slackSales(`📝 New subscription pending signature: ${customer.name} (${input.plan})`)

    return sub
  }

  static async handleSignatureWebhook(payload: ModuSignWebhookPayload) {
    const subId = payload.metadata.subscriptionId
    const sub = await SubscriptionRepository.findById(subId)
    if (!sub) throw new Error('SUB-404')

    await SubscriptionRepository.update(subId, {
      status: 'pilot_free',
      'contract.signedAt': new Date(),
    })

    // Grant first month credits
    await CreditService.grant({
      subscriptionId: subId,
      amount: sub.features.creditsIncludedPerMonth,
      reason: `monthly_grant_${dayjs().format('YYYYMM')}`,
    })

    await slackSales(`✅ Signature complete: ${subId}`)
  }

  // ... (list/detail/update methods)
}
```

### 5.6 Test Skeleton — `DiscountPolicy.test.ts`

`src/domain/subscription/__tests__/DiscountPolicy.test.ts`

```typescript
import { describe, it, expect } from 'vitest'
import { calculatePilotMonthlyAmount } from '../DiscountPolicy'

describe('calculatePilotMonthlyAmount', () => {
  const start = new Date('2026-05-15')

  it('starter: 1-3M is free', () => {
    expect(calculatePilotMonthlyAmount('starter', start, new Date('2026-06-01'))).toBe(0)
    expect(calculatePilotMonthlyAmount('starter', start, new Date('2026-08-01'))).toBe(0)
  })

  it('starter: 4-9M is 50% of annual', () => {
    expect(calculatePilotMonthlyAmount('starter', start, new Date('2026-09-01'))).toBe(395_000)
  })

  it('starter: 10-12M is annual', () => {
    expect(calculatePilotMonthlyAmount('starter', start, new Date('2027-03-01'))).toBe(790_000)
  })

  it('growth: 4-6M is 50% of annual', () => {
    expect(calculatePilotMonthlyAmount('growth', start, new Date('2026-09-01'))).toBe(1_245_000)
  })

  it('growth: 7-12M is annual', () => {
    expect(calculatePilotMonthlyAmount('growth', start, new Date('2026-12-01'))).toBe(1_990_000)
  })

  it('throws after 12 months', () => {
    expect(() =>
      calculatePilotMonthlyAmount('starter', start, new Date('2027-06-01'))
    ).toThrow('Contract expired')
  })
})
```

---

## 6. Implementation Notes

### 6.1 Design Decisions Reference

| 결정 | 선택 | 근거 |
|-----|------|------|
| 전자서명 | 모두싸인 | Q1 결정 ([[2026-04-17-DAKER_Pilot_Design_Decisions]]) |
| 세금계산서 | SmartBill 수동 CSV → Q3 자동화 | Q2 결정 |
| 크레딧 만료 | 월 리셋 + 구매분 90일 | Q3 결정 |
| 계약서 언어 | 한국어 only | Q4 결정 |
| State Machine | Subscription 상태 순수 함수 | Clean Architecture §9 |
| Idempotency | `refId + reason` 조합 (Redis, 24h TTL) | Design §4.2 |
| 원가 추적 | `credit_ledger.costKRW` 에 Gemini 실비×1.8 | Design §3.3 |

### 6.2 Things to Avoid

- [ ] **credit_ledger UPDATE/DELETE 절대 금지** — append-only, 보정은 역방향 entry만
- [ ] consume 엔드포인트에 일반 사용자 세션 허용 금지 — service token 필수
- [ ] 하드코딩 금액/KRW — `DiscountPolicy` 를 Single Source of Truth로
- [ ] 시간대 혼동 — 모든 date 처리는 `dayjs.tz('Asia/Seoul')` 고정
- [ ] console.log 프로덕션 잔존 — pino logger만 사용
- [ ] 세금계산서 사업자번호 수기 입력 — `customer.businessNumber` 단일 소스

### 6.3 Architecture Checklist

- [ ] Domain(`DiscountPolicy` 등)이 Mongoose/Express 의존 없음 확인
- [ ] Presentation(`pages/*.tsx`)에서 Mongoose 직접 import 금지
- [ ] Infrastructure(모두싸인·SmartBill)는 Domain 인터페이스만 구현
- [ ] Feature 폴더 간 cross-import 금지 (`subscription/` 이 `credit/` 내부 구현 참조 X)

### 6.4 Convention Checklist

- [ ] Mongo 컬렉션: snake_case 복수 (`credit_ledger`, `usage_events`)
- [ ] API 경로: kebab-case, 내부 API는 `/api/internal/` 접두
- [ ] Env 변수: `DAKER_` 접두
- [ ] 오류 코드: `SUB-XXX`, `BILL-XXX`, `CONT-XXX` 형식
- [ ] Currency: 항상 KRW 정수

### 6.5 Security Checklist

- [ ] 모두싸인 웹훅 HMAC-SHA256 검증 (`DAKER_MODUSIGN_WEBHOOK_SECRET`)
- [ ] `/api/internal/credits/*` 는 `DAKER_CREDIT_SERVICE_TOKEN` 검증
- [ ] Admin 엔드포인트는 기존 daker.ai 세션 + role 체크
- [ ] 계약서 PDF S3 저장 시 KMS 암호화 + 접근 로그
- [ ] 사업자번호·주민번호·계좌 등 PII는 로그 마스킹

### 6.6 API Checklist

- [ ] 에러 응답 `{ error: { code, message, details } }` 형식
- [ ] HTTP status: 200/201/400/401/402/403/404/409/500 중 명시된 것만
- [ ] List API 페이지네이션: `{ data, pagination: { page, size, total } }`
- [ ] POST 응답은 생성된 리소스 전체 반환

---

## 7. Testing Checklist

### 7.1 Unit (Vitest)

- [ ] `DiscountPolicy`: 6개 시나리오 (free/50%/full × starter/growth)
- [ ] `SubscriptionStateMachine`: 상태 전환 유효성
- [ ] `ConsumePolicy`: 잔액 검증·status 검증
- [ ] `calculateMonthlyInvoice`: 월말 청구 계산

### 7.2 Integration (Supertest + in-memory Mongo)

- [ ] `/admin/api/subscriptions` CRUD 전체 흐름
- [ ] `/api/internal/credits/consume` — 200·402·409·401
- [ ] Idempotency: 동일 refId 2회 호출 → 1건만 ledger 기록
- [ ] 모두싸인 웹훅 → status 변경 검증

### 7.3 E2E (Playwright)

- [ ] 관리자: 구독 생성 → 모두싸인 전송 (mock) → 상태 pilot_free
- [ ] 관리자: 크레딧 수동 충전 → Ledger 반영 → 잔액 업데이트
- [ ] 관리자: KPI 대시보드 Green/Yellow/Red 색상 검증

### 7.4 Load (k6)

- [ ] `/credits/consume` 1,000 TPS, p99 < 300ms, 에러율 < 0.1%
- [ ] 동시성: 동일 subscriptionId에 병렬 차감 100건 → 잔액 정확

---

## 8. Progress Tracking

### 8.1 Daily Standup Format (매일 09:30, Slack #daker-dev)

```
📅 [YYYY-MM-DD] DAKER Pilot Sprint 2 Day N/42

✅ 어제 완료:
  - 항목 1
  - 항목 2

🚧 오늘 할 일:
  - 항목 1
  - 항목 2

🚨 블로커:
  - (있으면)

📊 Sprint 진척: 12/37 tasks (32%)
```

### 8.2 Weekly Review (매주 금 17:00)

- Sprint burndown (completed/remaining)
- 완료된 작업 데모
- 새로 발견된 위험 요소
- 다음 주 우선순위 조정

### 8.3 Blocker Log

| # | 발생일 | 이슈 | 영향 | 해결 |
|---|--------|------|------|------|
| — | — | — | — | — |

---

## 9. Rollout Plan

### 9.1 Feature Flag

```typescript
// src/config/featureFlags.ts
export const featureFlags = {
  subscription_v1: process.env.FEATURE_SUBSCRIPTION_V1 === 'true',
}
```

Admin UI 진입점은 `featureFlags.subscription_v1 ? <SubscriptionTab /> : null`.

### 9.2 Rollout Steps

1. **Dev**: 로컬에서 flag ON, 자가 검증
2. **Staging (test1.daker.ai)**: flag ON, 내부 5명 dogfooding (2026-06-13~19)
3. **Prod (daker.ai)**: flag OFF 배포 → 대표 계정만 flag ON (2026-06-20)
4. **Pilot 1호 체결일**: flag 전체 ON + Slack 공지
5. **안정화**: 3사 온보딩 완료 후 Q3 초 빌링 자동화 착수

### 9.3 Rollback Runbook

조건 | 조치
---|---
치명적 이슈 발견 | `FEATURE_SUBSCRIPTION_V1=false` 재배포 (5분 내)
데이터 오염 | Mongo 스테이징 스냅샷 복원 + 이벤트 재적용
크레딧 차감 오류 | consume 엔드포인트 503 반환 모드, CSM 수동 대응

---

## 10. Post-Implementation (Do → Check)

### 10.1 Self-Review Checklist

- [ ] 37개 Week 1~6 작업 모두 완료
- [ ] E2E 시나리오 3종 통과
- [ ] Load test p99 < 300ms 확인
- [ ] 문서 2종 작성 완료 (운영 매뉴얼·Rollback Runbook)
- [ ] Design 문서 §8 Test Cases 전부 실행

### 10.2 Ready for Check Phase

위 체크리스트 완료 후:

```bash
/pdca analyze DAKER-Pilot-Contract
```

Gap 분석에서 **Match Rate ≥ 90%** 확보 시 Report 단계 진입.

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 0.1 | 2026-04-17 | Initial Do phase handoff | edgar@dacon.io |
