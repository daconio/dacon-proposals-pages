# Sprint 2 — Generator Result

## Status

| 항목 | 값 |
|------|-----|
| 스프린트 | 2 / 2 |
| 시도 | 1 |
| 파일 생성 | 제안/2026-03-29-단국대학교_SW중심대학_사전대회_제안서.html |
| 커밋 | 완료 |

## Contract Check (CR)

| ID | 항목 | 결과 |
|----|------|------|
| CR-20 | 파일 존재 | PASS |
| CR-21 | 슬라이드 수 (15개) | PASS |
| CR-22 | 표지에 SW중심대학 + 사전 키워드 | PASS |
| CR-23 | 7월 타임라인 슬라이드 | PASS (7회 등장) |
| CR-24 | 예산 슬라이드 (만원 단위) | PASS (8회 등장) |
| CR-25 | table class="tb" 성과 지표 테이블 | PASS (6개 테이블) |
| CR-26 | data-step 요소 10개 이상 | PASS (87개) |
| CR-27 | @page + break-after: page 인쇄 CSS | PASS |
| CR-28 | 외부 리소스 없음 (Google Fonts만) | PASS |
| CR-29 | sf-pg 페이지 번호 14개 이상 | PASS (15개) |
| CR-30 | show() 함수 존재 | PASS |
| CR-31 | 2026-03-23 문자열 없음 | PASS (0건) |

## RV Notes (Render Verification — manual check needed)

| ID | 항목 | 예상 결과 |
|----|------|----------|
| RV-01 | 초기 로드 시 표지만 보임 | slide.active on s1, 나머지 opacity:0 |
| RV-02 | 키보드 내비게이션 | ArrowRight/Left 바인딩 동일 JS |
| RV-03 | 프래그먼트 순서 | data-step 1~5 per slide |
| RV-04 | 진행바 | progress-bar width 업데이트 |
| RV-05 | 스케일링 | fit() 함수 동일 사용 |
| RV-06 | 마지막 슬라이드 CTA | s15에 미팅 요청 링크 포함 |

## Slide Map (15 slides)

| # | Section | 내용 |
|---|---------|------|
| 1 | COVER | SW중심대학 경진대회 사전 연습, 2026.07, 교수 대상 |
| 2 | CONTEXT | SW중심대학 경진대회 개요 테이블 |
| 3 | PROBLEM | 사전 연습 필요성, 타교 격차 비교표 |
| 4 | LANDSCAPE | 한성대, 조선대, 한국열린사이버대 사례 |
| 5 | DANKOOK | 110억, 3000+, 100+, 19, 4단계 metrics |
| 6 | PROPOSAL | 섹션 구분 (slide-sec) |
| 7 | DUAL TRACK | DAKER vs DACON 비교 |
| 8 | VIBE TRACK | 바이브코딩 대회 구조/과제/플랫폼 |
| 9 | ALGO TRACK | 알고리즘 대회 구조/과제/플랫폼 |
| 10 | ALIGNMENT | 7개 성과 지표 매핑 테이블 |
| 11 | TIMELINE | 4월~7월 그리드 + 역할 분담 |
| 12 | BUDGET | Basic/Standard/Premium 패키지 + 상금 구성 |
| 13 | EXPECTED | KPI 테이블 + 정성적 기대효과 |
| 14 | PLATFORM | 데이콘 25억+, 14만+ 실적 |
| 15 | ENDING | CTA 미팅 요청 링크 |
