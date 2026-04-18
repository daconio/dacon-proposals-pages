# AI4Sci Korea 2026 × DAKER — 연구자 대상 AI for Science 경진대회 6개 트랙 운영 제안서

> **작성일:** 2026.04.17
> **제안 대상:** AI4Sci Korea 2026 조직위원회
> **공동위원장:** Prof. 임경태 (KAIST · AI/ML) · Prof. 석차옥 (Seoul National University · Computational Science)
> **주최:** AI Friends (한국실용AI학회) · Korean Science AI Forum
> **후원:** 과학기술정보통신부 (MSIT)
> **행사 일정·장소:** 2026.09.28(월) ~ 10.01(목) · Seoul Dragon City, Grand Ballroom Halla
> **제안사:** 데이콘(DACON) · 데이커(DAKER)
> **담당자:** 김국진 (edgar@dacon.io / 010-4293-1041)

---

## 목차

1. [Executive Summary](#i-executive-summary)
2. [AI4Sci Korea 2026 이해](#ii-ai4sci-korea-2026-이해)
3. [데이콘·데이커 생태계 요약](#iii-데이콘데이커-생태계-요약)
4. [2 Pillars × 3 Tracks — 6개 경진 트랙](#iv-2-pillars--3-tracks--연구자-대상-6개-경진-트랙)
5. [DAKER 플랫폼 완전 활용 매핑](#v-daker-플랫폼-완전-활용-매핑)
6. [운영 로드맵 (2026.07 ~ 2026.10)](#vi-운영-로드맵-202607--202610)
7. [온사이트 해커톤 (9.28–10.01) 운영 방안](#vii-온사이트-해커톤-928--1001-운영-방안)
8. [과학적 재현성·연구윤리 관리](#viii-과학적-재현성연구윤리-관리)
9. [기대 성과 및 후속 활용](#ix-기대-성과-및-후속-활용)
10. [데이콘·데이커 크레덴셜](#x-데이콘데이커-크레덴셜)
11. [마치며 · Contact](#xi-마치며--contact)

---

## I. Executive Summary

### 1. 제안 한 줄 요약

> **AI4Sci Korea 2026의 두 축 — "AI Agents for Research" · "ML for Domain Science" — 을 완전히 커버하는 6개 연구자 경진 트랙을, DAKER 플랫폼 전 기능으로 운영하는 공식 Data Challenge 파트너 제안입니다.**

### 2. 제안 배경

조직위가 공지한 **2 Pillar 구조**를 그대로 유지하면서, 각 Pillar에 **3개 트랙**을 두어
총 **6개 트랙 (2 Pillars × 3 Tracks)**이 모두 **① 온라인 경진대회 + ② 온사이트 해커톤** 을 갖추는 구조로 운영합니다.

| 구분 | 조직위 원안 | 본 제안 구조 |
|---|---|---|
| **Pillar 1 · AI Agents for Research** | AI Agent Challenge (1개) | **P1-A / P1-B / P1-C** — 3개 트랙 |
| **Pillar 2 · ML for Domain Science** | Scientific ML Challenge (1개) | **P2-A / P2-B / P2-C** — 3개 트랙 |
| 운영 포맷 | 단일 Challenge | **온라인 예선(7~9월) + 온사이트 결선 해커톤(9.28–10.01 Seoul Dragon City)** |

### 3. 제안 핵심 가치

1. **조직위 2 Pillar 구조 그대로 계승** — 조직위가 공지한 카테고리·Keynote 주제를 그대로 반영한 트랙 세분화
2. **각 트랙이 "경진대회 + 해커톤" 이중 포맷** — 온라인 리더보드(DACON)와 온사이트 해커톤(DAKER)을 통합 운영
3. **과학 연구 특화 운영** — **재현성 아티팩트 필수 제출**, **도메인 심사위원 풀**, **오픈 사이언스 라이선스 가이드**
4. **한국 대표 AI 연구자 커뮤니티 동원** — 14만+ AI 전문가 커뮤니티 × 국내 최대 AI 경진대회 회원 풀 연계 홍보·모객
5. **MSIT 후원 행사의 격에 맞는 운영** — 500회+ 메이저 AI 대회 운영 경험, 특허 등록된 부정행위 탐지(FDS) 기술 적용

### 4. 트랙 6종 한눈에 보기 (2 Pillars × 3 Tracks)

#### 🟦 Pillar 1 · AI Agents for Research — 3개 트랙

> *"From AI-powered research assistants to fully autonomous scientific agents — exploring how systems like AlphaEvolve are transforming the research process itself."*

| # | 트랙 | 연구 초점 | 대표 참고 시스템 | 온라인 경진 | 온사이트 해커톤 |
|---|------|----------|----------------|-----------|---------------|
| **P1-A** | **Autonomous Research Agent Challenge** | 가설 생성→실험 계획→실행→해석 전 과정 자율 에이전트 | AlphaEvolve, AI Scientist v2 | ScienceAgentBench 유형 리더보드 | Mystery Problem 공개 → 48h 자율 해결 + ELO Arena |
| **P1-B** | **AI Research Copilot Challenge** | 연구자를 보조하는 가설·문헌·실험설계 Copilot | Google AI Co-Scientist, Deep Research | 공개 논문 기반 가설 생성·근거 제시 리더보드 | 조직위 즉석 과제 → 30분 Research Proposal 발표 |
| **P1-C** | **AI for Math & Formal Reasoning Challenge** | 수학 증명·과학 추론 자동화 | AlphaProof (IMO 2024 Silver), miniF2F | Lean verifier 자동 채점 리더보드 | 라이브 증명·미공개 문제 해결 + 수학자 루브릭 |

#### 🟧 Pillar 2 · ML for Domain Science — 3개 트랙

> *"Applying data-driven and machine learning approaches to specific scientific domains — from AlphaFold in biology to materials discovery and beyond."*

| # | 트랙 | 연구 초점 | 대표 참고 시스템 | 온라인 경진 | 온사이트 해커톤 |
|---|------|----------|----------------|-----------|---------------|
| **P2-A** | **AI for Biology Challenge** | 단백질·약물-타겟 상호작용, de novo 분자 설계 | AlphaFold 3, ESM, Kaggle BELKA | 결합 친화도·생성 분자 리더보드 | Hidden Target 공개 → 48h 후보 제안 + 웻랩 검증 후보 선정 |
| **P2-B** | **AI for Chemistry Challenge** | 반응 예측·역합성·촉매 최적화 | USPTO-MIT, RSGPT | Top-K Accuracy + 수율 예측 리더보드 | Hidden Reaction 공개 → 합성 경로 제안 + 화학자 블라인드 심사 |
| **P2-C** | **AI for Materials Science Challenge** | 결정 구조-특성 예측 및 역설계(Inverse Design) | GNoME, MatterGen, Matbench Discovery | Forward MAE + Inverse Match Rate 듀얼 리더보드 | 목표 특성 공개 → 24h 구조 생성 + DFT 검증 + 합성 가능성 발표 |

> **공통 원칙**: 6개 트랙 모두 **온라인 예선 7~9월 + 온사이트 결선 9.28–10.01** 운영. 각 트랙 결선 팀은 Seoul Dragon City Grand Ballroom 현장에서 **24~48시간 해커톤**으로 최종 승부.

---

## II. AI4Sci Korea 2026 이해

### 1. 행사 기본 정보 (조직위 공개 자료 기반)

| 항목 | 내용 |
|------|------|
| 공식명 | AI4Sci Korea 2026 — International Conference on AI for Science |
| 부제 | From Autonomous Research Agents to ML-Driven Scientific Discovery |
| 일정 | 2026년 9월 28일(월) ~ 10월 1일(목), 총 4일 |
| 장소 | Seoul Dragon City · Grand Ballroom Halla (서울시 용산구 한강대로23길 55) |
| 주최 | AI Friends (Korean Society for Practical AI) · Korean Science AI Forum |
| 후원 | 과학기술정보통신부 (MSIT) |
| 공동위원장 | Prof. Kyungtae Lim (KAIST), Prof. Chaok Seok (Seoul National University) |
| Organizing Committee | Dr. Yonggyun Yu (KAERI / AI Friends 회장), Dr. Yeji Choi (DI LAB), Prof. Jae Kyoung Kim (KAIST · AI for Math Track Chair), Prof. Chang Yun Son (SNU 화학), Prof. Woo Youn Kim (KAIST 화학), Prof. Sungsoo Ahn (KAIST Kim Jaechul Graduate School of AI) |

### 2. 두 축 (Pillars) 정확한 해석

| Pillar | 조직위 원문 | 핵심 질문 | 본 제안 3개 트랙 |
|---|---|---|---|
| **Pillar 1 · AI Agents for Research** | *"From AI-powered research assistants to fully autonomous scientific agents — exploring how systems like AlphaEvolve are transforming the research process itself."* | "AI가 직접 연구를 수행·가속할 수 있는가?" | **P1-A** Autonomous Research Agent · **P1-B** AI Research Copilot · **P1-C** AI for Math & Formal Reasoning |
| **Pillar 2 · ML for Domain Science** | *"Applying data-driven and machine learning approaches to specific scientific domains — from AlphaFold in biology to materials discovery and beyond."* | "도메인 과학을 ML이 어떻게 바꾸는가?" | **P2-A** AI for Biology · **P2-B** AI for Chemistry · **P2-C** AI for Materials Science |

### 3. 조직위가 발표한 부속 프로그램

- **Data Challenge** — Kaggle-style scientific data challenge · Hackathon 병행
- **Policy Forum** — AI 정책/공공 담론 확장
- **Keynote 트랙** — AI for Biology, AI Agents for Research, AI for Chemistry, AI for Materials Science

### 4. 조직위 원안 Competition 일정 (공개분)

| 시점 | 단계 |
|---|---|
| 2026.07 (TBD) | Challenge 발표 · 데이터 공개 |
| 2026.08 (TBD) | 온라인 제출 마감 |
| 2026.09.28 (TBD) | 온사이트 해커톤 킥오프 |
| 2026.10.01 (TBD) | 결선·데모·시상 |

**본 제안은 이 타임라인을 완전히 계승하며, 6개 트랙이 동일 캘린더를 공유합니다.**

---

## III. 데이콘·데이커 생태계 요약

### 1. 회사 개요

| 항목 | 내용 |
|------|------|
| 회사명 | 데이콘 주식회사 (DACON Co., Ltd.) |
| 대표이사 | 김국진 |
| 설립 | 2018.08.15 (설립 8년차) |
| 주소 | 서울시 영등포구 은행로 3, 익스콘벤처타워 901호 |
| 비전 | 전세계 누구나 AI를 실제 연구·업무·생활에 자유롭게 활용할 수 있는 경진대회 플랫폼 |

### 2. 3-브랜드 생태계

| 브랜드 | 도메인 | 핵심 역량 | 본 대회 활용 |
|---|---|---|---|
| **DACON (dacon.io)** | AI 알고리즘 경진 | Public/Private 리더보드, 자동 채점, FDS(부정행위 탐지, 특허 등록), Jupyter LAB | **T2·T3·T4·T5** 알고리즘 리더보드 |
| **DAKER (daker.ai)** | 바이브코딩·해커톤·프롬프톤 | 팀 빌딩, 작전실(War Room), 갤러리·쇼케이스, ELO 1v1 Arena, Expert 심사 포털, Q&A 게시판 | **T1·T6** + 전 트랙 온사이트 해커톤 |
| **DASCHOOL** | AI 실무형 교육 | 구독형 온라인 학습, 학습 → 대회 연결 | Pre-Conference 튜토리얼·베이스라인 교재 |

### 3. 플랫폼 팩트 체크 (2026.03 기준)

| 지표 | 수치 |
|---|---|
| AI 전문가 커뮤니티 | **14만+ 명** (연구자·엔지니어 중심) |
| 누적 대회 운영 | **500건+** |
| 누적 코드·결과물 제출 | **103만+ 건** |
| 누적 팀 참여 | **236,666팀** |
| 누적 상금 규모 | **25억+ 원** |
| 월 방문자 | **56만+ 명** |
| 협력 기업·기관 | **150개+** |

### 4. 과학 연구 영역 주요 운영 실적 (발췌)

| 주최 | 대회 | 도메인 | 연구 임팩트 |
|---|---|---|---|
| **한국원자력연구원 (KAERI)** | 태양광 발전량 예측 경진대회 | 에너지·시계열 | 국가연구기관 공동 과제 모델 도출 |
| **ETRI** | AI 분야 다수 경진대회 | 음성·언어·비전 | 출연연 연구성과 확산 |
| **한국전자통신연구원 / KISTI** | 과학 데이터 활용 챌린지 | 과학 빅데이터 | 국가 과학 DB 활용 확대 |
| **삼성전자 SAIT / DS** | Samsung AI Challenge 시리즈 | 반도체·이미지 | 5,000+ 누적 참가 연구자 |
| **LG AI 연구원** | LG Aimers / 오프라인 해커톤 | 제조/언어모델 | 누적 20,000+ 참가자 |
| **한국에너지공단 / 동서발전** | 전력·태양광·풍력 예측 | 재생에너지 | 실제 발전소 모델 발굴 |
| **단국대 / SW중심대학사업단 / 강원대** | 학술 AI 경진대회 | 학계 인재양성 | 학부·대학원 모델 검증 |

### 5. 운영 가능한 8대 대회 유형

| # | 유형 | 플랫폼 | 본 대회 매핑 |
|---|------|--------|------------|
| 1 | AI 알고리즘 대회 (CSV 제출) | DACON | T2·T3·T4·T5 기본 리더보드 |
| 2 | AI 알고리즘 on 코드 제출 | DACON | **T2·T3·T4·T5·T6 본 평가** (재현성 강제) |
| 3 | 프롬프톤 | DAKER | 베이스라인 검증·사전 이벤트 |
| 4 | AI 서비스·아이디어 공모전 | DAKER | T1 에이전트 쇼케이스 갤러리 |
| 5 | 온/오프 하이브리드 해커톤 | DAKER | **온사이트 결선(9.28–10.01)** 전 트랙 |
| 6 | 해커톤 on 코드 제출 | DAKER | P1-A · P1-C 실시간 제출 |
| 7 | 온라인 대회 + 시상식 | DAKER | 시상식 통합 운영 |
| 8 | 비공개 기업 해커톤 | DAKER | 산업계 스폰서 별도 비공개 트랙 시 활용 |

---

## IV. 2 Pillars × 3 Tracks — 연구자 대상 6개 경진 트랙

> **공통 운영 원칙**: 모든 트랙이 **① 온라인 경진대회(예선) + ② 온사이트 해커톤(결선)** 이중 포맷으로 운영됩니다.
> 학술 발표 수준의 **재현성 아티팩트(코드·환경·시드)** 제출 필수, 수상작은 AI4Sci Korea 2026 공식 Proceedings/Tech Report 수록 권고를 전제로 설계했습니다.

---

## 🟦 Pillar 1 · AI Agents for Research (3 Tracks)

> *"From AI-powered research assistants to fully autonomous scientific agents — exploring how systems like AlphaEvolve are transforming the research process itself."* — 조직위 공식 원문

---

### P1-A. Autonomous Research Agent Challenge — 자율 연구 에이전트

#### (1) 배경 · Pillar 정합성

- **Pillar 1의 중심 트랙** — 조직위가 예시로 든 AlphaEvolve 계열 자율 에이전트를 직접 벤치마킹.
- 한국 연구 커뮤니티가 자율 과학 에이전트 SOTA와 정면 경쟁하는 첫 공식 포럼.

#### (2) 과제 정의

참가 팀의 에이전트는 **Mystery Scientific Problem Set**에 대해 다음 전 과정을 자율 수행:

1. **Hypothesis generation** — 문제와 배경 문헌으로부터 가설 N개 도출
2. **Experiment planning** — 시뮬레이션 또는 공개 데이터 재분석 계획 수립
3. **Execution** — Dockerized Sandbox에서 분석 스크립트 실행
4. **Interpretation** — 결과를 과학 논문 단락(IMRaD) 형식으로 자기 서술
5. **Self-critique & iteration** — 최대 N회 자율 재설계

#### (3) 온라인 경진대회 (7월~8월 말)

- 공개 벤치마크: **ScienceAgentBench**, **MLAgentBench**, **DiscoveryBench** 혼합
- Sandbox: Python + 과학 컴퓨팅 스택, 네트워크 격리, 토큰·실행시간 예산 고정
- 자동 채점: 태스크 성공률, 오류 복구율, 비용 효율

#### (4) 온사이트 해커톤 (9.28–10.01)

- **Mystery Problem 공개 (D-Day 15:45)** → 48시간 자율 해결
- 팀당 API 예산·GPU 자원 동일 배분
- **ELO 1v1 Arena** — 팀 간 블라인드 Head-to-Head 데모
- 결선 발표 10분 + Q&A 5분

#### (5) 평가 지표

| 지표 | 비중 | 산정 |
|---|---|---|
| 자동 벤치마크 점수 | 40% | 태스크 성공률, 오류 복구율, 예산 효율 |
| 전문가 심사 (과학적 타당성·창의성) | 30% | 조직위·초청 도메인 연구자 심사 |
| 재현성·로그 품질 | 15% | 에이전트 트레이스 재현 가능 여부 |
| ELO Arena (온사이트 Head-to-Head) | 15% | 결선 블라인드 비교 |

#### (6) DAKER 활용

- **에이전트 트레이스 갤러리** — 전 실행 로그 외부 URL + 스크린샷 프리뷰
- **작전실(War Room)** — 팀별 실시간 협업, AI Friends 멘토 투입
- **ELO 1v1 Arena** + **Expert 심사 포털** (6~7명, 자동 집계)

---

### P1-B. AI Research Copilot Challenge — AI 연구 보조·가설 생성

#### (1) 배경 · Pillar 정합성

- **Pillar 1의 "AI-powered research assistants"** 영역 — Google AI Co-Scientist(2025.02), Deep Research, Consensus 등 **인간 연구자를 보조**하는 Copilot 계열.
- P1-A(완전 자율)와 구분되는 축: **연구자 + AI 협업 성과 측정**.

#### (2) 과제 정의

주어진 연구 문제/연구 자료 코퍼스에 대해 팀의 Copilot 시스템이 아래를 수행:

1. **Literature grounding** — 관련 논문·데이터 수집, 요약, 인용 정합성 확보
2. **Hypothesis ranking** — 가설 N개 생성 + 사전 문헌·증거 점수 산정
3. **Experiment design sketch** — 실험·분석 설계 초안 (통계 검정·표본 크기 포함)
4. **Research proposal draft** — 구조화된 연구 제안서(2–4페이지) 자동 작성

#### (3) 온라인 경진대회 (7월~8월 말)

- 데이터: 공개 논문 코퍼스 + **조직위 Hidden Research Question 세트**
- 자동 평가: 인용 정합성(Citation faithfulness), Novelty score, Coverage 지표
- 부정행위 탐지: 인용 조작·환각 탐지(FDS)

#### (4) 온사이트 해커톤 (9.28–10.01)

- **조직위 도메인 전문가가 즉석 브리핑** — 팀에 미공개 연구 문제를 30분간 설명
- 팀은 **90분 내 Copilot으로 Research Proposal 초안 생성**
- **30분 발표 + 15분 전문가 질의** — 실제 도메인 연구자가 "이 제안서를 받아들일 수 있는가" 관점으로 심사

#### (5) 평가 지표

| 지표 | 비중 | 산정 |
|---|---|---|
| 인용 정합성·환각율 | 25% | 자동 검증 |
| Novelty · Hypothesis 품질 | 25% | 도메인 전문가 루브릭 |
| 연구설계 타당성 | 25% | 통계·방법론 검토 |
| 온사이트 발표·답변 | 25% | 라이브 Q&A 채점 |

#### (6) DAKER 활용

- **Research Proposal 갤러리** — Markdown/PDF 제출, 인용 링크 검증 모듈
- **Hallucination Flag** — FDS 기반 자동 플래그
- **Expert 심사 포털** — 도메인 전문가 루브릭 집계

---

### P1-C. AI for Math & Formal Reasoning Challenge — 수학·형식 추론

#### (1) 배경 · Pillar 정합성

- **조직위 Math Track Chair 김재경 교수(KAIST)와 직접 연계**.
- AlphaProof가 2024 IMO에서 **은메달급 (6문제 중 4문제)** 성과를 낸 직후, 한국 수학·AI 커뮤니티의 독자 벤치마크 무대.

#### (2) 과제 구조 (서브트랙 A/B/C)

| 서브 | 과제 | 검증 방식 |
|---|---|---|
| **A. Formal Math** | miniF2F / ProofNet Lean/Isabelle 증명 | Lean 자동 proof checker |
| **B. Olympiad-Style Problem** | IMO/KMO/Putnam 수준 증명 서술 | KAIST 수리과학과 루브릭 심사 |
| **C. Scientific Reasoning** | GPQA/SciBench 다단계 과학 추론 | Exact Match + 추론 신뢰도 |

#### (3) 온라인 경진대회 (7월~8월 말)

- Lean Verifier 자동 연동: 제출물이 실시간으로 증명기에 투입 → 리더보드 기록
- A/B/C 각 서브에 Public/Private 분할 문제 세트

#### (4) 온사이트 해커톤 (9.28–10.01)

- **Live Proof Battle** — 결선 팀에 미공개 문제 1시간 내 증명 제출
- Math Track Chair 김재경 교수 주재 루브릭 심사
- 수상작 증명본 전체 공개 + Paper-pitch 세션

#### (5) 평가 지표

- **A**: pass@k, 증명 길이·우아함
- **B**: 루브릭(정확성·명료성·우아함) 블라인드 심사
- **C**: 정확도 + Reasoning faithfulness

#### (6) DAKER 활용

- **Lean Verifier 제출 파이프라인 내장** — 자동 채점·리더보드 갱신
- **Expert 심사 포털 — 수학자 루브릭 템플릿**
- **작전실** — 온사이트 Math Track 세션과 동기 운영

---

## 🟧 Pillar 2 · ML for Domain Science (3 Tracks)

> *"Applying data-driven and machine learning approaches to specific scientific domains — from AlphaFold in biology to materials discovery and beyond."* — 조직위 공식 원문

> **조직위 공지 Keynote 주제(AI for Biology / AI for Chemistry / AI for Materials Science)에 1:1 정합**되도록 3개 트랙을 배치했습니다.

---

### P2-A. AI for Biology Challenge — 단백질·신약

#### (1) 배경 · Pillar 정합성

- **조직위 Keynote "AI for Biology"와 1:1 대응**.
- 석차옥 Co-Chair(SeokLab GalaxyWEB)와 김우연 조직위원(BInD, R-DM)의 전공 교차점.
- AlphaFold 3(2024) 이후 **Hidden Target 기반 약물 설계**가 경쟁의 중심.

#### (2) 과제 후보 (조직위 협의 후 1종 또는 복합 확정)

| 과제 | 요약 | 대표 데이터 |
|---|---|---|
| **A. Protein-Ligand Binding Affinity** | 단백질-리간드 쌍 pKd/pKi 예측 | PDBBind, BindingDB, DAVIS, KIBA |
| **B. Antibody Binding Region / CDR Design** | 항체-항원 결합 부위 예측·설계 | SAbDab + 주최 Hidden |
| **C. De novo Small Molecule for Hidden Target** | 미공개 타겟용 신규 분자 생성 | ChEMBL + 주최 Hidden Target |

#### (3) 온라인 경진대회 (7월~8월 말)

- DACON **알고리즘 on 코드 제출** (Public/Private 분할)
- Jupyter LAB 내장 개발 환경
- FDS 기반 데이터 누수·재현성 전수 검증
- 베이스라인 교재 (DASCHOOL, DeepPurpose/TorchDrug/ESM 기반)

#### (4) 온사이트 해커톤 (9.28–10.01)

- **Hidden Target 공개 (D1 오후)** → 48시간 내 후보 분자/모델 제출
- Top-K 후보 분자 → **웻랩 검증 후보 선정 세션** (조직위 지정 연구실 협의 시)
- 온사이트 실시간 리더보드 스크린

#### (5) 평가 지표

- 회귀: RMSE, Pearson, Spearman
- 분류/생성: AUROC, Top-K hit rate, Novelty(Tanimoto <0.4), Synthetic Accessibility
- **전문가 블라인드 심사 (Top-20 합리성)** — Expert 심사 포털
- 웻랩 검증 후보 품질 점수

#### (6) DAKER 활용

- **분자 구조 2D/3D 시각화 갤러리** (RDKit · py3Dmol)
- **Private Score 잠금 → 결선 직후 공개**
- **Hidden Target 보안 관리** — 접근 권한 분리

---

### P2-B. AI for Chemistry Challenge — 반응·합성·촉매

#### (1) 배경 · Pillar 정합성

- **조직위 Keynote "AI for Chemistry"와 1:1 대응**.
- 석차옥·김우연·손창윤 교수 전공 교차점.
- USPTO Top-K 포화 구간 진입(2025 RSGPT Top-1 77%) → **합성 가능성·촉매 최적화** 중심 재설계.

#### (2) 과제 구조 (서브 A/B/C)

| 서브 | 과제 | 데이터 |
|---|---|---|
| **A. Forward Reaction Prediction** | 반응물·조건 → 생성물 분자 예측 | USPTO-MIT, Pistachio 서브셋 |
| **B. Retrosynthesis (Single/Multi-step)** | 타겟 분자 → 합성 경로 역추론 + 합성 가능성 | USPTO-50K·FULL + Hidden |
| **C. Yield & Condition Prediction** | 수율·조건 최적화 (Buchwald/Suzuki 계열) | Reaxys-style 공개 + Hidden |

#### (3) 온라인 경진대회 (7월~8월 말)

- DACON 알고리즘 on 코드 제출
- Round-trip Accuracy (Forward → Retro → Forward) 병행 평가
- SCScore·SA-Score 기반 합성 가능성 부가 지표

#### (4) 온사이트 해커톤 (9.28–10.01)

- **Hidden Reaction Mystery 공개** → 팀별 48시간 합성 경로·조건 제안
- **Blind Chemist Panel** — 유기·무기·촉매 화학자 6~7인이 합리성 블라인드 평가
- 최종 발표 10분 + 화학자 Q&A 10분

#### (5) 평가 지표

- Top-1/5/10 Accuracy
- Round-trip Accuracy
- 합성 가능성 (SCScore, SA-Score)
- 화학자 블라인드 루브릭 점수

#### (6) DAKER 활용

- **RDKit 기반 반응 시각화 갤러리**
- **Chemist Blind Review UI** — 블라인드 모드 기본 ON
- **자동 채점 + 심사 병합** (ELO 없이 가중 평균)

---

### P2-C. AI for Materials Science Challenge — 소재·역설계

#### (1) 배경 · Pillar 정합성

- **조직위 Keynote "AI for Materials Science"와 1:1 대응**.
- 손창윤(SNU Computational Energy/Bio Soft Materials Lab)·Sungsoo Ahn(KAIST SPML, 분자/소재 생성 GNN) 직접 연계.
- Matbench Discovery F1 0.93 포화 → **Forward + Inverse Design 듀얼 트랙** 재설계.

#### (2) 과제 구조 (서브 Forward / Inverse / Synthesis)

| 서브 | 과제 |
|---|---|
| **Forward** | 결정 구조 → 밴드갭/형성에너지/탄성계수 예측 (MAE 경쟁) |
| **Inverse** | 목표 특성(예: 밴드갭 2.0 eV ± 0.2, Ef < 0.05) → 후보 구조 N개 생성 |
| **Synthesis Feasibility** | 생성 후보의 합성 가능성 점수 |

#### (3) 온라인 경진대회 (7월~8월 말)

- 데이터: Materials Project, OQMD, JARVIS-DFT, Alexandria + **Hidden 소재 조성** (KIST/KRICT 협의 시)
- Forward: MAE/R² 리더보드
- Inverse: Property-Matching Accuracy, Stability Rate, Novelty/Uniqueness

#### (4) 온사이트 해커톤 (9.28–10.01)

- **Target Property 공개 (D1 오후)** → 24시간 내 구조 생성·제출
- DFT 검증 (상위 N 샘플, 조직위 전산 파트너)
- 결선 발표 + Synthesis Feasibility 정당화

#### (5) 평가 지표

- Forward: MAE, R²
- Inverse: Property-Matching Accuracy, Stability Rate, Novelty/Uniqueness
- DFT 검증 통과율
- 전문가 심사 (합성 가능성·혁신성)

#### (6) DAKER 활용

- **결정 구조 3D 뷰어 임베드** (crystal-toolkit/py3Dmol CDN)
- **Inverse Candidate ELO Arena** — 온사이트
- **DFT 검증 결과 뱃지** — 갤러리 상단 자동 표시

---

### 📋 6개 트랙 요약표

| Pillar | # | 트랙 | 대표 시스템 | 온라인 | 온사이트 해커톤 | 주요 연계 조직위원 |
|---|---|---|---|---|---|---|
| **P1** | A | Autonomous Research Agent | AlphaEvolve, AI Scientist v2 | ScienceAgentBench 리더보드 | Mystery Problem 48h | 임경태(KAIST), 유용균(KAERI) |
| **P1** | B | AI Research Copilot | AI Co-Scientist, Deep Research | 가설·문헌 정합성 | Research Proposal 90분 | 임경태, 최예지(DI LAB) |
| **P1** | C | AI for Math & Formal Reasoning | AlphaProof, miniF2F | Lean verifier 자동 채점 | Live Proof Battle | **김재경(Math Track Chair)** |
| **P2** | A | AI for Biology | AlphaFold 3, ESM, BELKA | 결합 친화도·분자 생성 | Hidden Target 48h | **석차옥(Co-Chair)**, 김우연 |
| **P2** | B | AI for Chemistry | USPTO / RSGPT SOTA | Top-K + 합성 가능성 | Hidden Reaction 48h | 석차옥, 김우연, 손창윤 |
| **P2** | C | AI for Materials Science | GNoME, MatterGen | Forward + Inverse 듀얼 | Target Property 24h | 손창윤, Sungsoo Ahn |

---

## V. DAKER 플랫폼 완전 활용 매핑

### 1. 조직위 4대 운영 요건 ↔ DAKER 매핑 (100%)

| # | 운영 요건 | DAKER 제공 기능 | 과학 대회 특화 커스터마이즈 |
|---|---|---|---|
| **01** | 공모전 접수·서류 관리 | 개인정보처리동의서 전자 서명, 결과물 활용 동의 다단계, 기획서(PDF) + MVP URL 통합 제출, 제출 현황 실시간 대시보드 | **재현성 아티팩트(코드·requirements·seed) 별도 업로드 슬롯**, **연구윤리·IRB/생명연구심의 확인란** |
| **02** | MVP / 에이전트 리다이렉팅 페이지 | 참가팀 구현물 쇼케이스 갤러리, 외부 URL 리다이렉트 + 스크린샷 프리뷰, 심사위원/일반 공개 접근 권한 분리, 좋아요·댓글 커뮤니티 피드백 | **에이전트 실행 로그 뷰어**, **분자/결정 구조 3D 임베드**, **시계열 예보 맵 프리뷰** |
| **03** | 심사위원 전용 채점 | 6~7명 심사위원 개별 배정·권한 관리, 엑셀 기반 채점표 자동 생성, 가중치·점수 자동 집계, 진행률 실시간 모니터링 | **도메인별 루브릭 템플릿**(Bio/Chem/Materials/Earth/Math 5종), **블라인드 모드** 기본 ON |
| **04** | Q&A 게시판·CS 관리 | 대회 전용 커뮤니티(카테고리별), 운영진 답변·공지 고정, 이미지/파일 첨부·멘션, CS 대시보드 | **English/Korean 이중 언어 지원**, **국제 참가팀 시간대 대응 SLA** |

### 2. DAKER·DACON 공통 고급 기능 (전 트랙 공통)

| 기능 | 설명 | 본 대회 활용 |
|---|---|---|
| **Public/Private 분할 리더보드** | 대회 중 Public(≈30%) 공개, 종료 시 Private(≈70%) 본 순위 확정 | P2-A · P2-B · P2-C · P1-C(A 서브) 과적합 방지 |
| **FDS (특허 등록 2025.12)** | 행동 분석·데이터 누수 탐지·코드 재현성 전수 검증 | 전 트랙 의무 적용 |
| **팀 빌딩 · 원정대 매칭** | 역할·스킬 기반 자동 매칭, 일괄 등록 최대 1,000명 | 국제 참가팀 팀 빌딩 지원 |
| **작전실 (War Room)** | 팀 전용 협업 공간, 관리자 대시보드 | 온사이트 결선 기본 운영 단위 (6트랙 공통) |
| **ELO 1v1 Arena** | MVP/에이전트 블라인드 1:1 비교 | P1-A · P2-C 결선 보조 심사 |
| **AI 멘토링 (Office Hours)** | 24/7 온라인 AI 멘토 + Forcing Question | 학생/신진 연구자 진입 장벽 완화 |
| **인증서 자동 발급** | 수상/참가 수료증 디지털 발급 | 국제 참가자 여권 정보 없이도 발급 |
| **Jupyter LAB 내장** | 참가자 개발 환경 원클릭 제공 | 알고리즘 기반 트랙 공통 환경 |

### 3. 과학 대회 특화 추가 모듈 (본 제안 한정 커스터마이즈)

| 모듈 | 설명 |
|---|---|
| **Reproducibility Vault** | Docker 이미지 해시·시드·requirements 고정 저장, 제출 시점 동결, 검증 재실행 로그 보존 |
| **Domain Reviewer Pool** | AI Friends 회원 풀 + 각 트랙 조직위 추천 연구자를 묶은 심사위원 데이터베이스 (서약서·COI 관리) |
| **Open Science License Wizard** | 제출 코드·모델·데이터의 라이선스(CC-BY/Apache/MIT/OpenRAIL) 선택 가이드 |
| **Pre-registration Slot** | P1-B 연구제안서·P2-C 역설계 등에서 사전등록(hypothesis lock) 지원, NeurIPS Reproducibility Track 관례 적용 |
| **Benchmark Portability** | 종료 후 데이터셋·리더보드를 Papers-with-Code/HuggingFace에 export 지원 |

---

## VI. 운영 로드맵 (2026.07 ~ 2026.10)

### 1. 전체 간트

| 구분 | 07월 | 08월 | 09월 상순 | 09월 중순 | **09.28–10.01** | 10월 |
|---|---|---|---|---|---|---|
| **D-Phase · 설계 확정** | 트랙/평가/데이터 확정, 플랫폼 구축 |  |  |  |  |  |
| **K-Phase · 킥오프** | 대회 오픈, 공식 발표, 데이터 공개 |  |  |  |  |  |
| **O-Phase · 온라인 예선** |  | 제출 폭주기 (일 1,000+ 제출 예상) | 마감(8월 말) |  |  |  |
| **S-Phase · 온사이트 결선** |  |  | 상위 팀 선발·여행 지원 | 오리엔테이션 | **Grand Ballroom 결선** |  |
| **R-Phase · 후속** |  |  |  |  | 수상 발표 | 결과보고서, 논문/공보 지원 |

### 2. 단계별 상세

#### 2.1 설계 확정 (4월 말~6월)

- 본 제안 승인 후 2주 내 **트랙별 Kick-off Workshop** 개최 (조직위·DAKER)
- 트랙별 과제 3안 중 1안 확정, 데이터 사용권·라이선스 검토
- 윤리·법무 검토 (Hidden 데이터·인체유래물·환자 데이터 유무 확인)
- Baseline 모델 개발 착수

#### 2.2 Pre-Launch (7월)

- **7월 1주:** 공식 웹사이트 오픈, 경진대회 Call for Participation 배포
- **7월 2주:** 데이터·베이스라인·튜토리얼 공개
- **7월 4주:** Warm-up Month — 소규모 검증용 Mini Challenge

#### 2.3 온라인 예선 (7월 말~8월 말)

- 일 단위 리더보드 갱신
- **AI 멘토 Office Hours 주 2회** (한/영 각 1회)
- 중간 점검 webinar (AI Friends 공동 운영)
- **Private 마감 48시간 전 커밋 잠금(Freeze)** — 과적합 추가 방지

#### 2.4 결선 팀 선발 (9월 상/중순)

- **Shortlist 기준** — 트랙별 Top 15팀 (Private 점수 + 재현성 검증 통과)
- **Finalists** — Top 6팀 온사이트 초청 (국내선/국제선 이동 지원 규정 조직위 협의)
- 오리엔테이션(온라인) — 온사이트 아젠다, 제출 규정, 발표 포맷

#### 2.5 온사이트 결선 (9.28–10.01)

**→ §VII에서 별도 상세**

#### 2.6 후속 (10월)

- 공식 수상자 발표, 증서 자동 발급
- **결과보고서 (한/영)** 조직위 제출
- 선정된 우수작의 AI4Sci Korea 2026 Tech Report / Workshop Paper 지원
- 데이터셋·리더보드 Paperswithcode/HuggingFace 공개 지원

---

## VII. 온사이트 해커톤 (9.28–10.01) 운영 방안

### 1. 공간 구성 (Seoul Dragon City · Grand Ballroom Halla 기준)

| Zone | 용도 | 규모 |
|---|---|---|
| **Main Arena** | 오프닝·Keynote·Panel 공용, 결선 데모 무대 | Ballroom 메인 홀 |
| **Track Rooms × 6** | Pillar 1(P1-A/B/C) + Pillar 2(P2-A/B/C) 병렬 작전실 | 분반실 각 1실 |
| **Expert Review Booth** | 심사위원 블라인드 심사 공간 | 전용 VIP 룸 |
| **Sponsor & Demo Wall** | DAKER 갤러리 대형 디스플레이 | 복도/로비 |
| **AI Agent Live Demo Stage** | P1-A 자율 에이전트 · P1-C Live Proof Battle 실시간 데모 | Main Arena Sub |

### 2. 일자별 아젠다 (조직위 공개 Day 1 기준 + 본 제안 확장)

#### Day 1 (9.28 Mon)

- 09:00–09:30 **Opening Ceremony** (조직위)
- 09:30–10:30 **Keynote — Autonomous AI Agents for Scientific Discovery** (조직위 · Pillar 1 테마)
- 11:00–12:00 **[본 제안]** 6개 트랙 Finalist Orientation · 작전실 입주
- 14:00–15:30 **Session: AI Research Assistants & Agentic Workflows** (조직위)
- 15:45–17:00 **[본 제안]** Pillar 1 **P1-A Mystery Problem 공개** · Pillar 2 **P2-A/B/C Hidden Target·Reaction·Property 공개** · 해커톤 공식 스타트
- 17:30–19:00 Welcome Reception

#### Day 2 (9.29 Tue)

- 09:00–12:00 Keynote · 병행 세션 (조직위 · AI for Biology / AI for Chemistry 주제)
- 13:00–18:00 **[본 제안]** Pillar 2 (P2-A/B/C) 리더보드 추가 Hidden Test 공개, 실시간 점수 갱신
- 19:00–21:00 Pillar 1 **P1-A 1차 ELO Arena** · **P1-C Live Proof Battle Round 1** (피어 블라인드)

#### Day 3 (9.30 Wed)

- 09:00–12:00 Keynote (조직위 · AI for Materials Science 주제)
- 13:00–17:00 **[본 제안]** 전 트랙 Expert 심사 본격화 · **P1-B Research Proposal 라이브 발표 세션 (90분 + Q&A)**
- 18:00–20:00 **Scientific Storytelling Workshop** — 수상작 논문화 가이드 (AI Friends 공동)

#### Day 4 (10.01 Thu)

- 09:00–12:00 **[본 제안]** 트랙별 Finalist Presentations (10분 발표 + 5분 QnA)
- 13:00–15:00 **[본 제안]** Awards & Keynote Closing — MSIT/조직위 시상
- 15:00–17:00 **Demo Fair & Paper-pitch** — 수상작 부스 운영, 연구자 네트워킹
- 17:00– Closing Reception

### 3. 상주 운영팀 구성

| 역할 | 인원 | 책임 |
|---|---|---|
| Operations Lead | 1 | 전체 일정·위기 대응 |
| Track Lead × 6 | 6 | 트랙별 운영·심사 진행 |
| Tech Support | 3 | 네트워크·노트북·플랫폼 장애 대응 |
| AI/Domain Mentor | 6+ | 트랙별 멘토링 (AI Friends 연구자 공동) |
| Expert Reviewer Pool | 36+ | 트랙당 6명 × 6트랙 |
| CS/Help Desk | 2 | 참가자·국제팀 응대 (한/영) |

### 4. 국제 참가자 대응

- **이중 언어(한/영)** 플랫폼 UI, 공지, Q&A 대응
- **시간대별 Office Hours** — UTC, KST, 미 동부 3개 시간대 멘토 배정
- **초청 여비 지원 안내** (조직위 정책 연동)
- **E-visa Support Letter** 발급 지원

---

## VIII. 과학적 재현성·연구윤리 관리

### 1. 재현성 강제 체계 (Reproducibility-by-Default)

| 단계 | 조치 |
|---|---|
| 참가 등록 | Reproducibility Pledge 서명 |
| 예선 제출 | 코드 + requirements.lock + seed + 환경 해시 업로드 의무 |
| 마감 후 | 상위 팀 수작업 코드 검증 (500+ 대회 운영 경험 적용) |
| 온사이트 결선 | **Frozen container**로 실행, 외부 재현 로그 공개 |
| 수상 발표 | Repo 공개 라이선스 명시 필수 |

### 2. 부정행위 탐지 (FDS)

- **데이콘 FDS 특허 등록** (2025.12) 기술을 전 트랙 적용
- 감지 범주: Label Leakage, Test-time Training 위반, 팀 간 공유 제출, 외부 API 우회 호출
- 위반 시: 단계적 경고 → 실격 → 주최 연구윤리위 이관 옵션 확보

### 3. 연구윤리·데이터 라이선스

| 카테고리 | 체크 |
|---|---|
| 인체유래물·환자 데이터 | 공개 de-identified 데이터만 사용, IRB 면제 근거 명시 |
| 공공 관측 데이터 | 제공 기관(기상청/KIGAM 등) 이용약관 고지·동의 |
| 오픈소스 라이선스 | 제출물 라이선스 선택 Wizard (CC-BY / Apache-2.0 / MIT / OpenRAIL 중 택일) |
| AI 생성물 | 에이전트가 생성한 분자·구조·텍스트의 학술 인용·재사용 가이드 |
| 이중 출판 금지 | 동일 결과의 중복 수상·중복 논문 금지 서약 |

### 4. 안전·이중 용도 (Dual-use) 관리

- **P2-A (Biology) / P2-B (Chemistry)** 일부 서브트랙(신약·유해 분자 생성 관련)에는 **Hazardous Compound Filter** 의무화 (예: 합성 난이도·독성·전구체 필터)
- **P1-A / P1-B** 자율 에이전트·Copilot이 위험 연구(biosecurity·dual-use) 제안을 생성할 경우 자동 플래그 처리
- 조직위 · AI Friends 윤리위원회와 사전 합의된 블랙리스트 체계 적용

---

## IX. 기대 성과 및 후속 활용

### 1. 정량 KPI (제안)

| KPI | 목표치 |
|---|---|
| Pillar 수 | **2 Pillars** (AI Agents for Research · ML for Domain Science) |
| 트랙 수 | **6개** 동시 운영 (각 Pillar 3트랙) |
| 총 참가 팀 | **300+팀** (트랙당 평균 50팀) |
| 총 참가 연구자 | **1,000+ 명** (국내 60%, 해외 40% 목표) |
| 온사이트 결선 팀 | **36팀** (트랙당 6팀) |
| 제출 모델/에이전트 수 | **10,000+ 건** |
| 재현성 검증 통과율 | **Top-30 팀 100%** |
| 수상작 Proceedings/Tech Report 수록 | **전 트랙 Top-3** |

### 2. 학술·정책 성과

- **AI Friends Proceedings / Tech Report 2026** — 수상작 기반 6편 × 3위 = 최소 18편 논문/테크리포트
- **MSIT 후원 실적** — 국가 AI for Science 로드맵 제시 근거 자료 확보
- **국제 학술 연계** — ICML/NeurIPS Workshop, KDD 2026 AI for Sciences Track과 공동 이벤트 가능성

### 3. 생태계 성과

- 참가 연구자 중 Top 10% 인재풀을 **한국 AI for Science 차세대 연구자 DB**로 AI Friends에 이관
- 데이터셋·벤치마크를 공개하여 **지속 가능 벤치마크 인프라** 구축 (Papers-with-Code, HuggingFace)
- **연간 정례화** — AI4Sci Korea의 공식 Data Challenge Track으로 2027년 이후 시리즈화

### 4. 산업 연계

- **AI Friends 산학 스폰서십** 연계 프레임 제공 (스폰서 별도 비공개 트랙·상금 가능, 본 제안과 별도 계약)
- 수상 연구자의 **연구실 출신 창업팀** 발굴 경로로 활용

---

## X. 데이콘·데이커 크레덴셜

### 1. 핵심 수치 재확인

- **설립 8년차 / 500+ 메이저 대회 / 14만+ AI 전문가 / 103만+ 제출물 / 25억+ 누적 상금 / 150+ 협력 기관**

### 2. 특허·인증

- **온라인 경진대회 부정행위 다층적 분석·탐지 시스템 및 그 운용방법** 특허 출원 (2025.12)
- NIA 소셜DNA 협력상, 서울창조경제혁신센터장상
- 기업부설 연구소 설립 (2022)

### 3. 최근 유사 과학·연구 도메인 대회 (2025–2026)

| 대회 | 주최 | 핵심 | 규모 |
|---|---|---|---|
| 2025 Samsung AI Challenge 시리즈 | 삼성전자 SAIT | 반도체·비전·언어 | 5,000+ 누적 |
| LG Aimers / LG AI 오프라인 해커톤 | LG AI 연구원 | LLM/제조 데이터 | 20,000+ 누적 |
| 한국에너지공단 전력사용량 예측 (3회) | 에너지공단 | 시계열 예측 | 2021/2023/2025 3회 연속 |
| 한국원자력연구원 태양광 발전량 예측 | KAERI | 에너지·시계열 | 국가연구기관 |
| NIA 정책수립지원 AI 과제 | NIA | 공공 데이터 | 정책 지원 |
| Samsung Display AI 서비스 개발 | 삼성디스플레이 | AI 서비스 | 진행 중 |
| K-water AI 러닝톤 (2026) | K-water | 학습형 해커톤 | 신규 |
| 법학전문대학원 AI 경진대회 (2026.06) | 법학전문대학원협의회 | 법률 AI | 200명 오프라인 |

### 4. 조직위 인적 네트워크 연계성

- **AI Friends (회장: 유용균 박사, KAERI)** — 데이콘이 KAERI 주최 경진대회 운영 경험 보유, 즉시 시너지
- **KAIST / SNU 화학·수리과학·AI 교수진** — 데이콘이 복수 교수 연구실과 연구 자문·대회 자문 교류
- **MSIT 사업** — 데이콘·데이스쿨이 다수 MSIT 후원 AI 교육·경진 사업 수행

---

## XI. 마치며 · Contact

### 마치며

AI4Sci Korea 2026은 **"AI가 과학의 방식을 바꾸는 현장"을 한국에서 확인하는 첫 국제 학술 이벤트**입니다.
이 행사의 Data Challenge는 단순 부속 행사가 아니라, **Pillar 1·2가 가장 구체적인 스코어로 측정되는 자리**여야 합니다.

- **조직위는 학술 프로그램과 비전 정의에 집중**하시고,
- **대회 운영의 무거운 짐 — 접수·플랫폼·CS·심사·재현성·시상 —은 데이커·데이콘이 책임지는 것**,

이 역할 분담이 본 제안의 본질입니다.

6개 트랙 × DAKER 전 기능 × 500+ 대회 운영 경험을 결합해, AI4Sci Korea 2026이
**"한국이 주도하는 AI for Science 경진의 국제 표준"**이 될 수 있도록 함께 하겠습니다.

### Contact

| 구분 | 내용 |
|---|---|
| 담당자 | 김국진 (DACON · DAKER 대표) |
| 이메일 | edgar@dacon.io |
| 전화 | 010-4293-1041 |
| 주소 | 서울시 영등포구 은행로 3, 익스콘벤처타워 901호 |
| 플랫폼 | dacon.io · daker.ai · daschool.io |

---

> © 2026 DACON · DAKER. All rights reserved.
> 본 제안서는 AI4Sci Korea 2026 조직위원회 검토 목적으로만 사용됩니다.
