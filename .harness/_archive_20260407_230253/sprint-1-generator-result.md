# Sprint 1 — Generator Result (GS E&R HTML Slide Sync)

## Status: COMPLETE

## Deliverable

- **File**: `제안/2026-03-27-GS_E&R_AI경진대회_제안서_슬라이드.html`
- **Commit**: `9f93129`

## Tasks Completed

| Task | Description | Status |
|------|-------------|--------|
| 1-1 | s3 Option A table: added 대회 유형, 상금 규모 rows; fixed 참가 대상 to 자격조건 | Done |
| 1-2 | Created new s3b (Option B detail with DACON+DAKER); renamed old s3b to s3c | Done |
| 1-3 | s3c comparison table: fixed Option B duration to 8주 | Done |
| 1-4 | s5 performance table: 10 customers with corrected numbers (SAMSUNG 5,000+, LG 20,000+, TOSS 2,500+, energy sector clients) | Done |
| 1-5 | s6 success factor cards: added 수상인증서/수료증 and 서류 전형 면제 text | Done |
| 1-6 | s8 references: added 4 latest reference cards (토스, Samsung, SW마에스트로, 수원시) | Done |
| 1-7 | s9 simplified; created s9b (Option A/B timeline tables) and s9c (contact + next steps) | Done |
| 1-8 | Slide footers renumbered 2-15 (s1 cover has no footer) | Done |
| 1-9 | JS navigation verified: show() uses querySelectorAll('.slide') dynamically | Done |

## Contract Verification (CR)

| ID | Check | Result |
|----|-------|--------|
| CR-01 | File exists | PASS |
| CR-02 | 15 slide sections | PASS (15) |
| CR-03 | s3 has 대회 유형 and 상금 규모 | PASS |
| CR-04 | s3b exists with "AI Hackathon 2026" | PASS |
| CR-05 | s3b contains "DAKER" in 운영 row | PASS |
| CR-06 | s3c contains "8주" | PASS |
| CR-07 | s5 tbody has 10 tr tags | PASS (10) |
| CR-08 | s5 contains "5,000" | PASS |
| CR-09 | s5 contains "20,000" | PASS |
| CR-10 | s5 contains 한국에너지기술연구원/한국수자원공사 | PASS |
| CR-11 | s8 contains "SW마에스트로" and "수원시" | PASS |
| CR-12 | s9b exists with "W1~W2" | PASS |
| CR-13 | s9c exists with "이근민" and "kmlee@gswind.com" | PASS |
| CR-14 | 14 sf-pg elements, includes "15" | PASS |
| CR-15 | 83 data-step elements (>= 30) | PASS |
| CR-16 | No external resources beyond Google Fonts | PASS |
| CR-17 | @page rule and break-after:page present | PASS |
| CR-18 | show() with querySelectorAll('.slide') | PASS |

## Slide Structure (15 slides)

| # | ID | Title |
|---|-----|-------|
| 1 | s1 | COVER |
| 2 | s2 | 제안 배경 & 핵심 목표 |
| 3 | s3 | Option A 대회 개요 |
| 4 | s3b | Option B 대회 개요 (NEW) |
| 5 | s3c | Option A vs B 비교 |
| 6 | s4 | 대회 주제 후보(안) |
| 7 | s5 | 데이콘 수행 역량 |
| 8 | s6 | 운영 프로세스 타임라인 |
| 9 | s6b | 1박 2일 해커톤 일정 |
| 10 | s7 | 기대 효과 KPI |
| 11 | s8 | 성공 벤치마킹 |
| 12 | s9 | 파트너십 & 역할 분담 |
| 13 | s9b | 추진 일정 상세 (NEW) |
| 14 | s9c | 담당자 & 다음 단계 (NEW) |
| 15 | s10 | ENDING |

## Notes

- s5 table uses smaller font/padding (font-size:.7rem, padding:4px 8px) to fit 10 rows
- PDF regeneration deferred to Sprint 2
