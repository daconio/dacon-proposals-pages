# Research Report — AI4Sci Korea 2026: Pillars, Benchmarks, Competition Design

- **Topic**: AI4Sci Korea 2026 (ai4scikorea.org) 종합 심층 분석 — 두 Pillar · 조직위 · 벤치마크 · 경진대회 설계 근거
- **Depth**: `deep` (3–4 hop, detailed analysis)
- **Date**: 2026-04-18
- **Analyst**: Claude (Opus 4.7, 1M)
- **Status**: RESEARCH ONLY (implementation deferred per `/sc:research` boundaries)
- **Paired deliverable**: `제안/2026-04-17-AI4Sci_Korea_연구자_경진대회_제안서.md`

---

## Executive Summary

AI4Sci Korea 2026(2026.09.28–10.01, Seoul Dragon City, MSIT 후원)은 두 축 — **AI Agents for Research**, **ML for Domain Science** — 를 국내에서 처음으로 **국제 학술 포럼 + Data Challenge 해커톤** 하이브리드 형식으로 다루는 공식 이벤트다. 본 리서치는 조직위가 공개한 트랙(2개, AI Agent · Scientific ML)을 **6개 연구자 트랙으로 확장하기 위한 근거**를 다음 네 축으로 정리한다.

| 축 | 핵심 발견 (요약) | Confidence |
|---|---|---|
| **P1 · AI Agents for Research SOTA** | AlphaEvolve(2025.05)·AI Co-Scientist(2025.02)·Sakana AI Scientist-v2(2025.04)가 1년 내 **자율 연구 에이전트 상용화** 단계 진입. ScienceAgentBench(32–42% solve rate) 등 **벤치마크가 막 성숙** — 한국 주도 벤치마크 공간 여유 존재 | HIGH |
| **P2 · ML for Domain Science** | Bio(AlphaFold3 CASP16 검증), Materials(GNoME·MatterGen·Matbench Discovery), Weather(GraphCast·Aurora), Math(AlphaProof IMO 2024 은메달)까지 **도메인별 공식 벤치마크 존재**. 한국 Hidden 데이터 결합 시 차별화 가능 | HIGH |
| **Organizers · 한국 네트워크** | 공동위원장(임경태 KAIST, 석차옥 SNU) + Math Chair 김재경 + Chemistry(김우연·손창윤)·AI/ML(안성수)·KAERI 유용균 회장이 **한국 AI for Science 핵심 네트워크 형성** | HIGH |
| **유사 이벤트 경쟁 분석** | KDD 2026(8월, 제주), NeurIPS 2025 AI4Science/ML4PS, AI4Sci EU(2026.10 Mainz), MSIT의 **AI Co-Scientist Challenge Korea**와 부분 중첩 → AI4Sci Korea는 **"온사이트 해커톤 + Proceedings"** 차별화가 관건 | MEDIUM-HIGH |

**결론**: 본 리서치는 제안서의 6개 트랙(T1 Autonomous Research Agent / T2 Protein & Drug / T3 Chemistry / T4 Materials / T5 Earth & Climate / T6 AI for Math) 설계가 **SOTA 벤치마크와 한국 연구진 전공의 교집합**에 정확히 일치함을 확인한다.

---

## 1. 행사 핵심 팩트 (1-hop: 공식 사이트)

| 항목 | 내용 | 출처 |
|---|---|---|
| 공식명 | AI4Sci Korea 2026 — International Conference on AI for Science | ai4scikorea.org |
| 부제 | From Autonomous Research Agents to ML-Driven Scientific Discovery | 동 |
| 일정 | 2026.09.28(월)–10.01(목), 4일 | 동 |
| 장소 | Seoul Dragon City · Grand Ballroom Halla (서울 용산) | 동 |
| 주최 | AI Friends (Korean Society for Practical AI) + Korean Science AI Forum | 동 |
| 후원 | 과학기술정보통신부 (MSIT) | 동 |
| Pillar 1 | **AI Agents for Research** — AlphaEvolve 계열 자율 연구 에이전트 | 동 |
| Pillar 2 | **ML for Domain Science** — AlphaFold 계열 도메인 ML | 동 |
| 부속 | Data Challenge (Kaggle-style), Policy Forum | 동 |
| Competition 원안 | AI Agent Challenge + Scientific ML Challenge (2트랙) | 동 |

---

## 2. Pillar 1 심층: Autonomous Research Agents (2025–2026 SOTA)

### 2.1 대표 시스템 3종

#### (A) DeepMind **AlphaEvolve** (2025.05 공개, arXiv 2506.13131)

- **유형**: 진화 기반 coding agent, Gemini LLM + 자동 Evaluator 루프
- **주요 성과**:
  - 50+ 수학 문제에서 **75% SOTA 재현, 20% SOTA 개선**
  - **4×4 complex matrix multiplication 48 scalar multiplication** 발견 — 56년 만에 Strassen 개선
  - Google 프로덕션에서 **0.7% 전사 컴퓨팅 자원 회수**, Gemini 학습 커널 **23% 가속**
- **시사점**: 에이전트가 "알고리즘 발견"과 "실제 프로덕션 배포"를 모두 증명 → **AI4Sci Korea T1 트랙의 정당성**
- Sources: [arXiv 2506.13131](https://arxiv.org/abs/2506.13131), [DeepMind Blog](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/), [techbytes 프로덕션 분석](https://techbytes.app/posts/deepmind-alphaevolve-production-deployment/)

#### (B) Google **AI Co-Scientist** (2025.02 공개, arXiv 2502.18864)

- **유형**: Gemini 2.0 기반 **multi-agent** (generate-debate-evolve)
- **주요 성과**:
  - 15개 복잡 생의학 목표에서 **신규성 전문가 평가 최고 등급**
  - AML 약물 재창출 후보, 간섬유화 후성유전학 타겟 **웻랩 검증 성공**
  - 가설 생성 주기 "주" → "일" 단축
- **시사점**: 연구 가설 수립 자체가 AI에 의해 단축 → **T1/T6 Hypothesis Generation 서브트랙 설계 근거**
- Sources: [arXiv 2502.18864](https://arxiv.org/abs/2502.18864), [Google Research Blog](https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/), [IEEE Spectrum](https://spectrum.ieee.org/ai-co-scientist)

#### (C) Sakana **AI Scientist-v2** (2025.04 공개, arXiv 2504.08066)

- **유형**: **Agentic Tree Search** + Experiment Manager (human template 불필요)
- **주요 성과**:
  - ICLR 2025 Workshop에 3편 제출, **1편이 인간 블라인드 peer-review 통과** (avg reviewer 6.33)
  - "세계 최초 AI 단독 저자 논문 peer-review 통과"
- **리스크**: 외부 검증에서 **할루시네이션·결과 조작 가능성** 지적
- **시사점**: **재현성·윤리 검증이 없는 자율 연구는 사회적 수용 불가** → 본 제안서의 **Reproducibility Vault + 이중 용도 필터** 필수성 뒷받침
- Sources: [arXiv 2504.08066](https://arxiv.org/abs/2504.08066), [Sakana AI Scientist v2](https://sakana.ai/ai-scientist/), [External evaluation arXiv 2502.14297](https://arxiv.org/abs/2502.14297)

### 2.2 벤치마크: ScienceAgentBench / MLAgentBench / DiscoveryBench

#### **ScienceAgentBench** (ICLR 2025, arXiv 2410.05080)

- 44개 peer-review 논문에서 추출한 **102 태스크**, 4 분야 (Bioinformatics, Computational Chemistry, GIS, Psychology/Cognitive Neuro)
- 평가: self-contained Python program 결과 + 실행 메트릭 + 비용
- **현재 SOTA: o1-preview + self-debug ~42.2%** (그러나 API 비용 10배)
- 일반 agentic framework: **독립 해결률 ~32%**
- Source: [arXiv 2410.05080](https://arxiv.org/abs/2410.05080), [OSU-NLP-Group/ScienceAgentBench](https://github.com/OSU-NLP-Group/ScienceAgentBench), [HAL Leaderboard](https://hal.cs.princeton.edu/scienceagentbench)

#### T1 설계 시사점

1. **벤치마크가 아직 40%대** → 참가 팀이 실질적으로 SOTA를 넘길 수 있는 경쟁 공간
2. 태스크는 **재현 가능한 Python program**으로 통일 → DAKER "코드 제출 + Docker Sandbox" 운영에 적합
3. **비용(API) 상한이 평가 차원** → 에이전트의 "효율성 리더보드" 분리 가능

---

## 3. Pillar 2 심층: ML for Domain Science 벤치마크

### 3.1 Biology — AlphaFold 3 & CASP16

- **CASP16 (2024–2025)**: AF3는 쉬운 타깃에서 AF2 대비 개선, 어려운 타깃에서는 열세. **리간드 binding pose 76% 정확도** (경쟁 방법의 2배)
- **Weight 공개 상태 (2026.04)**: 여전히 **closed weights**, 상업 이용은 Isomorphic Labs 파트너십. 소스코드는 2024.11 공개, 재현 실험 활성화
- **연구자 접근**: AlphaFold Server 하루 10회 제한 — **Hidden Target 기반 T2 경진대회의 현실성 확보** (공개 벤치마크로는 AF3를 직접 넘기 어려움 → 웻랩/신규 타깃 중심이 실효적)
- Sources: [AF3 at CASP16, bioRxiv](https://www.biorxiv.org/content/10.1101/2025.04.10.648174v1), [AF3 benchmarking, PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12661943/), [AF3 in Drug Discovery, bioRxiv](https://www.biorxiv.org/content/10.1101/2025.04.07.647682v1.full.pdf)

### 3.2 Biology — Kaggle BELKA (2024 NeurIPS)

- Leash Bio가 **DEL 기술로 1.33억 분자 x 3 단백질** 이원 결합 라벨 공개
- Kaggle 사상 최대 규모 약물-단백질 데이터, 압도적 참가
- **시사점**: 상업 데이터셋을 공모전에 개방하는 모델이 작동함을 검증 → **T2에 한국 제약사·연구소 Hidden Assay 데이터 유치 가능성**
- Sources: [Kaggle BELKA](https://www.kaggle.com/competitions/leash-BELKA), [Owlposting 분석](https://www.owlposting.com/p/an-ml-drug-discovery-startup-trying)

### 3.3 Materials — GNoME / MatterGen / Matbench Discovery

- **GNoME (DeepMind, 2023→2025)**: 소재 안정성 예측 성공률 50→80%, **220만 신규 결정 구조 발견**, 외부 실험실이 **736개 실제 합성 확인**
- **MatterGen (Microsoft, Azure AI Foundry)**: **Diffusion 기반 Inverse Design** — 극한 물성 영역에서도 강건, Materials Project + Alexandria 학습
- **Matbench Discovery** (Nature MI, 2025): 47개 모델 리더보드. **EquiformerV3+DeNS-OAM F1=0.931, Discovery Acceleration Factor=6.074**
- **시사점**: 순방향 예측은 포화, **Inverse Design + 합성 가능성**이 경쟁 공간 → **T4 설계가 Inverse 중심인 근거**
- Sources: [Matbench Discovery](https://matbench-discovery.materialsproject.org/), [Nature MI 2025](https://www.nature.com/articles/s42256-025-01055-1), [DeepMind GNoME](https://deepmind.google/blog/millions-of-new-materials-discovered-with-deep-learning/), [MatterGen Azure](https://labs.ai.azure.com/projects/mattergen/)

### 3.4 Earth & Climate — GraphCast / Pangu / Aurora / NeuralGCM

- **WeatherBench 2** (AGU 2024, 2025 확장): AI 기상 모델 공식 벤치마크
- **GraphCast** (Science 2023): IFS HRES 대비 medium-range forecast 우위 — 미 동부 60개 폭염에서 Pangu/GEFS 제치고 최고
- **Aurora** (Microsoft 2024): foundation weather 모델, 다양한 변수·해상도 지원
- **NeuralGCM**: 하이브리드(물리+ML), 앙상블 평균에서 HRES 필적
- **한국 차별화**: ECMWF/GFS 기반 모델은 한반도 지역 해상도 부족 → **한반도 AWS 네트워크·기상청 데이터 결합 다운스케일링이 T5의 차별화 포인트**
- Sources: [WeatherBench 2 AGU](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2023MS004019), [GraphCast Science](https://www.science.org/doi/10.1126/science.adi2336), [Scaling Laws arXiv 2602.22962](https://arxiv.org/html/2602.22962), [East Asia Evaluation Nature](https://www.nature.com/articles/s41612-024-00769-0)

### 3.5 Math — miniF2F · ProofNet · AlphaProof

- **miniF2F** (Lean/Isabelle): 488 statement (AMC/AIME/IMO)
- **ProofNet**: 학부 수학, Lean 3 (구버전), Lean 4 버전은 DeepSeek-Prover-V1.5 제공
- **AlphaProof** (Nature 2025): **2024 IMO 6문제 중 4문제 풀이, 은메달급** — RL + Lean 4
- **시사점**: miniF2F·ProofNet은 Lean 기반 자동 검증 가능 → **T6 설계(A. Formal Math, B. Olympiad, C. Scientific Reasoning) 뒷받침**
- Sources: [AlphaProof Nature](https://www.nature.com/articles/s41586-025-09833-y), [miniF2F arXiv 2511.03108](https://arxiv.org/pdf/2511.03108), [openai/miniF2F](https://github.com/openai/miniF2F)

### 3.6 Chemistry — USPTO Retrosynthesis 2025 SOTA

- **RSGPT** (2025 PMC): USPTO-50k **Top-1 77.0%, Top-10 96.7%** — 포화 구간 진입
- **Retro-MTGR** (Nature Comm 2025.01): 단일-step retrosynthesis에서 16개 SOTA 비교 우위
- **시사점**: **순수 Top-K는 포화** → **합성 가능성 평가(SCScore/SA-Score) + 화학자 블라인드 평가** 결합 필수 → **T3 설계가 "Top-K + 합성 가능성 + 화학자 심사"를 모두 포함하는 정당성**
- Sources: [RSGPT PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12314115/), [Retro-MTGR Nature Comm](https://www.nature.com/articles/s41467-025-56062-y)

---

## 4. Organizers · 한국 연구진 네트워크 분석

### 4.1 Co-Chairs & Committee 요약

| 위원 | 소속 | 전공 · 주요 업적 | 연계 트랙 |
|---|---|---|---|
| **Kyungtae Lim** (Co-Chair) | KAIST · Culture Technology, Multimodal Language Processing Lab | 다국어 NLP, CoNLL 2018 57언어 2위, Amazon Alexa Research 경험 | T1 (LLM 에이전트), T6 (Scientific Reasoning) |
| **Chaok Seok** (Co-Chair) | SNU · 화학, SeokLab | **GalaxyWEB** 단백질 구조·도킹 서버, CASP9+ 참가, 100+ 논문 6,400+ citations | T2 (단백질), T3 (화학) |
| **Jae Kyoung Kim** (Math Track Chair) | KAIST · 수리과학 / IBS 생의수학연구단장 | 수리생물학(circadian clock, stochastic QSSA 증명, FDA 약물대사식 수정), **2025 SIAM Annual Meeting 첫 한국인 Keynote** | T6 (AI for Math), T2 (약물대사) |
| **Woo Youn Kim** | KAIST · 화학, Graduate School of Data Science | AI for Science, **BInD 모델**(protein-conditioned 약물 생성), **R-DM** (Riemannian Denoising, Nature Comp Sci 2025) | T2, T3, T4 |
| **Chang Yun Son** | SNU · 화학, Computational Energy/Bio Soft Materials Lab | 전하 계면 시뮬레이션, **ML-보정 force field**, 수처리/에너지 소재 | T4 (Materials) |
| **Sungsoo Ahn** | KAIST · Graduate School of AI, SPML Lab | **분자 생성 GNN**, holistic molecular representation, ICLR 2025 다수 | T2, T3, T4 (분자 생성 공통) |
| **Yonggyun Yu** | KAERI · Applied AI Lab / **AI Friends 회장** / UST 교수 | 원자력 AI, 소셜AI, AI Friends 커뮤니티 운영 | 전 트랙 멘토풀 제공 |
| **Yeji Choi** | DI LAB, Research Director | 산업 AI 연구 | 산학 연계 |

### 4.2 네트워크 해석

1. **전공 커버리지**: NLP/LLM (임경태) · 화학(석차옥·김우연·손창윤) · 분자생성 GNN(안성수) · 수학(김재경) · 산업AI(유용균·최예지) → **6개 트랙 제안을 조직위 교수 1:1 매핑 가능**
2. **심사위원 풀 확보**: AI Friends 커뮤니티 + SeokLab/SPML Lab/BIMAG/Son Lab/Woo Youn Kim Lab 박사과정·포닥 → **트랙당 6명 심사위원 확보 용이**
3. **Data Hidden Set 조달**: 조직위 교수 연구실 공개/비공개 데이터 결합 → **상업 벤치마크 포화 문제를 "한국 Hidden" 결합으로 해소**

### 4.3 MSIT 후원 맥락 · 기존 사업 중첩 관리

- **AI Co-Scientist Challenge Korea 2026** (MSIT 주최, 한국연구재단 주관, 2025.12~2026.01 참가자 모집)
  - **Track 1**: AI 활용 과학기술 연구보고서 작성 (Bio/Materials/Chem/Earth/Semi/Battery/Energy/Math 지정)
  - **Track 2**: 과학기술 AI Agent 개발 (Top-10팀 **A100 GPU 4–8대 + LLM API 3천만원 지원**)
  - 시상: 최대 2.5억원 사업화 지원, NST 출연연 AI agent 배포 검토
  - Source: [co-scientist.kr](https://co-scientist.kr/), [aifactory Track1](https://aifactory.space/task/9235/overview), [aifactory Track2](https://aifactory.space/task/9237/overview)

**AI4Sci Korea 2026 ↔ AI Co-Scientist Challenge Korea 관계 분석**:

| 구분 | AI Co-Scientist Challenge (MSIT) | AI4Sci Korea 2026 (MSIT 후원) |
|---|---|---|
| 주목적 | **R&D 공모형 지원사업** | **국제 학술 컨퍼런스 + 경진대회** |
| 주최자 | 과학기술정보통신부·한국연구재단 | AI Friends + KSAIF |
| 결과물 | 보고서·AI 에이전트·사업화 | 학술 proceedings + 발표 + 시상 |
| 참가 경로 | 국가 R&D 공모 | 국제 오픈 Challenge |
| 시기 | 2025.12 모집 → 2026 진행 | 2026.09 컨퍼런스 (Data Challenge 7월 오픈 예정) |

→ **중첩이 아니라 단계적 파이프라인**: AI Co-Scientist Challenge 참가자/수상팀이 AI4Sci Korea 2026의 **연구 발표자·경진 참가자**로 자연스럽게 연결되는 설계가 합리적. 제안서의 "한국 AI for Science 인재풀 확보" 기대효과의 실질적 근거.

---

## 5. 유사 국제 컨퍼런스/경진대회 비교

### 5.1 시간·지리·범위 포지셔닝

| 이벤트 | 일정 | 장소 | 형식 | 경진대회 유무 | AI4Sci Korea와의 관계 |
|---|---|---|---|---|---|
| **AI4Sci EU** | 2026.10.05–10.09 | Mainz, Germany | 학술 컨퍼런스 | (발표 중심) | 자매 이벤트, 포스트 참가 가능 |
| **KDD 2026** (AI for Sciences Track 신설) | 2026.08.09–08.13 | Jeju, Korea | 메이저 학회 신규 트랙 | 별도 | **같은 주간대 한국 개최** — 상호 홍보·공동 워크숍 기회 |
| **NeurIPS 2025 AI4Science Workshop** | 2025.12 | San Diego | 워크샵 | 데이터셋 제안 대회 | 참고 포맷 |
| **NeurIPS 2025 ML4PS Workshop** | 2025.12 | San Diego | 물리과학 특화 | — | 참고 포맷 |
| **AI Co-Scientist Challenge Korea** | 2025.12–2026 | 한국 | 공모사업 | ✅ Track1/2 | 국내 파이프라인 연결 |
| **Kaggle BELKA (NeurIPS 2024)** | 2024 | 온라인 | 단일 대회 | ✅ | 약물-단백질 Kaggle 성공 사례 |

### 5.2 포지셔닝 전략

**AI4Sci Korea 2026의 차별화 축 (3가지)**:

1. **"해커톤 × 학술" 하이브리드** — AI4Sci EU(학술 only)와 Kaggle BELKA(온라인 only)의 중간
2. **온사이트 4일 결선** — Seoul Dragon City Grand Ballroom 물리 공간을 **학술 트랙·경진 트랙이 공유**
3. **한국 연구진 Hidden Data 결합** — 국제 공개 벤치마크가 포화된 도메인(화학 Top-K, 단백질 구조)에서 **한국 연구실 제공 Hidden Set**이 경쟁의 차별화 축으로 작용

Sources: [AI4Sci EU](https://ai4sci.eu/), [KDD 2026](https://kdd2026.kdd.org/), [KDD AI4Sciences Track](https://kdd2026.kdd.org/ai4sciences-track-call-for-papers/), [NeurIPS AI4Science 2025](https://ai4sciencecommunity.github.io/neurips25), [ML4PS 2025](https://ml4physicalsciences.github.io/)

---

## 6. 6개 트랙 설계 — 리서치 기반 근거 요약

| 트랙 | Pillar | SOTA·벤치마크 근거 | 한국 차별화 |
|---|---|---|---|
| **T1. Autonomous Research Agent Challenge** | P1 | ScienceAgentBench 40%대·AlphaEvolve 75% SOTA 재현 → **경쟁 여지 충분** | Co-Chair 임경태(KAIST)·Yu(KAERI) AI Friends 풀 매칭 |
| **T2. Protein Engineering & Drug Discovery ML** | P2·Bio | AF3 CASP16·Kaggle BELKA 성공 선례 | Seok Lab GalaxyWEB 자산 + Woo Youn Kim BInD · R-DM |
| **T3. Chemistry — Reaction & Retrosynthesis** | P2·Chem | USPTO Top-K 포화 → **합성성·화학자 심사** 결합 | 석차옥·김우연 공동 심사 + Hidden USPTO 확장 |
| **T4. Materials Inverse Design** | P2·Materials | Matbench Discovery 포화 → **Inverse/Synthesis** 중심 | 손창윤 · Ahn · KIST/KRICT 협력 잠재 |
| **T5. Earth & Climate System ML** | P2·Earth | GraphCast/Aurora 전역 우수 → **한반도 다운스케일·극한기상** 차별화 | 기상청·KMA, 한국지질자원연구원 잠재 협력 |
| **T6. AI for Math & Scientific Reasoning** | P1+P2 | AlphaProof 2024 IMO 은메달, miniF2F/ProofNet 공식 벤치마크 | **김재경 Math Track Chair 직접 연계**, KAIST 수리과학 루브릭 |

---

## 7. 운영 설계 관점 — 리서치로부터 도출된 핵심 고려사항

### 7.1 재현성·윤리 (Reproducibility-by-Default)

- **Sakana AI Scientist-v2 paper reveal**: 자율 생성 결과의 **할루시네이션·조작 가능성**이 실제 외부 검증에서 지적됨 → 경진대회 채점 단계에서 **자동 재실행 + 전문가 sanity check** 이중 체계 필수 (confidence: HIGH)
- **AF3 commercial 제약**: AlphaFold Server 하루 10회 → Hidden Target 기반 대회는 API 호출 제한 고려 운영 필요 (confidence: HIGH)

### 7.2 경쟁 포화도 및 차별화

- Chemistry USPTO-50K Top-1 77%, Top-10 96.7% (2025 RSGPT) — **순수 Top-K 지표로는 차별화 어려움** (confidence: HIGH)
- Matbench Discovery F1 0.93 — **순방향 예측 포화**, Inverse/Synthesis Rate 중심 재설계 필요 (confidence: HIGH)
- → 제안서의 트랙별 **"주 지표 + 전문가 심사 + 합성/실험 가능성"** 3중 평가 설계가 정당화됨

### 7.3 운영 규모 예상치 (Evidence-based Estimation)

- Kaggle BELKA (2024): Protein-Drug 단일 대회로 수천 명 참가 (confidence: MEDIUM, 정확 수치 확인 불가)
- 데이콘 Samsung AI Challenge 누적 5,000명+, LG Aimers 20,000명+ — 한국 내 AI 경진 연구자 공급 풍부 (confidence: HIGH, 데이콘 공개 자료)
- AI Co-Scientist Challenge Korea 2026 Track2 "예선 통과 10팀" 규모 → **AI4Sci Korea는 더 큰 규모(트랙당 50팀 이상) 지향 가능** (confidence: HIGH)

### 7.4 시점 충돌 분석

- **KDD 2026 (2026.08.09–13, 제주)**: AI4Sci Korea(9.28–10.01) 7주 전 → **KDD 기간 중 AI4Sci Korea 부스·세션 홍보 최적** (confidence: HIGH)
- **AI4Sci EU (2026.10.05–09, Mainz)**: AI4Sci Korea 직후 → **연사·논문 공유 파트너십 가능** (confidence: MEDIUM)
- **AI Co-Scientist Challenge Korea**: 2026 상반기 진행 → **여름에 수상팀이 AI4Sci Korea로 유입** (confidence: HIGH)

---

## 8. Open Questions · 불확실성

| 질문 | 상태 | 후속 액션 |
|---|---|---|
| 조직위가 정한 데이터 도메인 리스트 | **공개 미확인** | 조직위 1:1 협의 필요 |
| Competition 상금 규모·MSIT 지원 | **미공개 (TBA)** | MSIT 공문·AI Friends 협의 |
| Registration 수수료 (Early/Regular/Student) | **미공개 (TBA)** | 조직위 확정 후 반영 |
| 트랙 수 제한 (조직위 원안 2트랙) | **2트랙 공개** | 6트랙 확장은 협의 대상 |
| 웻랩 검증 가능 파트너 (T2) | **미확인** | Seok Lab · Woo Youn Kim Lab 연계 논의 |
| Hidden 기상 데이터 가용성 (T5) | **미확인** | 기상청·KIGAM 공식 요청 필요 |

---

## 9. Recommendations (사람이 판단할 사항)

1. **조직위 협의 우선순위**
   - (A) 6트랙 vs 2트랙 확장 가부
   - (B) 조직위 소속 연구실의 Hidden Data 제공 의사
   - (C) MSIT 후원 규모 내에서 경진 상금·온사이트 여비 배정 가능성

2. **KDD 2026(8월)과의 공동 마케팅 제안** — 7주 간격이라 제주 → 서울 유도 효과 큼

3. **AI Co-Scientist Challenge Korea 수상팀 fast-track 초청** — MSIT 라인 내 자연스러운 파이프라인

4. **국내 웻랩/계산 파트너 조기 확보** (T2·T4·T5):
   - Bio: Seok Lab · Woo Youn Kim Lab
   - Materials: KRICT · KIST · Son Lab
   - Weather: 기상청 APCC · KIAPS

5. **재현성 Gate를 1차 필터로** — 상위 100팀이 Frozen Container 재실행 통과 시에만 결선 진출. Sakana v2 교훈.

6. **Dual-use 필터**: T2/T3 신약·합성 계열에서 **유해 분자 블랙리스트 + 합성 난이도 상한** 필수 — AI Friends 윤리위 협의.

---

## 10. Confidence Map

| 주장 | Confidence | 근거 |
|---|---|---|
| AI4Sci Korea 2026 일정·장소·주최 | HIGH | 공식 사이트 직접 확인 (Chrome 렌더링) |
| 조직위 구성원 소속·전공 | HIGH | 각 대학 공식 프로필·arXiv·Scholar |
| Pillar 1 SOTA 시스템 3종 현황 | HIGH | arXiv 정식 논문, DeepMind/Sakana 공식 블로그 |
| ScienceAgentBench 32–42% 해결률 | HIGH | ICLR 2025 공식 게재 |
| Matbench Discovery F1 0.931 | HIGH | Nature MI 2025 게재 |
| AlphaProof IMO 은메달 | HIGH | Nature 2025 게재 |
| AI Co-Scientist Challenge Korea 파라미터 | HIGH | 공식 aifactory 공고 |
| KDD 2026 / NeurIPS 2025 / AI4Sci EU 관계 | MEDIUM-HIGH | 공식 사이트 기반, 세부 일정은 일부 TBD |
| 참가 규모 예상 (300+팀, 1,000+명) | MEDIUM | 데이콘 유사 대회 데이터 기반 추정 |
| 웻랩·기상청 Hidden 데이터 조달 | LOW–MEDIUM | 협의 전 단계 |

---

## 11. References (모든 인용)

### 행사·조직
- [AI4Sci Korea 2026](https://ai4scikorea.org/)
- [AI4Sci EU (Mainz 2026)](https://ai4sci.eu/)
- [KDD 2026 Korea](https://kdd2026.kdd.org/)
- [KDD 2026 · AI for Sciences Track CFP](https://kdd2026.kdd.org/ai4sciences-track-call-for-papers/)
- [NeurIPS 2025 AI for Science Workshop](https://ai4sciencecommunity.github.io/neurips25)
- [NeurIPS 2025 ML4PS Workshop](https://ml4physicalsciences.github.io/)
- [AI Co-Scientist Challenge Korea 2026](https://co-scientist.kr/)
- [AI Co-Scientist Challenge Track 1](https://aifactory.space/task/9235/overview)
- [AI Co-Scientist Challenge Track 2](https://aifactory.space/task/9237/overview)

### Pillar 1 — AI Agents
- [AlphaEvolve · arXiv 2506.13131](https://arxiv.org/abs/2506.13131)
- [AlphaEvolve · DeepMind Blog](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/)
- [AlphaEvolve Production · techbytes](https://techbytes.app/posts/deepmind-alphaevolve-production-deployment/)
- [AI Co-Scientist · arXiv 2502.18864](https://arxiv.org/abs/2502.18864)
- [AI Co-Scientist · Google Research Blog](https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/)
- [AI Co-Scientist · IEEE Spectrum](https://spectrum.ieee.org/ai-co-scientist)
- [Sakana AI Scientist v2 · arXiv 2504.08066](https://arxiv.org/abs/2504.08066)
- [Sakana AI Scientist v2 · Project Page](https://sakana.ai/ai-scientist/)
- [Sakana External Evaluation · arXiv 2502.14297](https://arxiv.org/abs/2502.14297)
- [ScienceAgentBench · arXiv 2410.05080](https://arxiv.org/abs/2410.05080)
- [ScienceAgentBench GitHub](https://github.com/OSU-NLP-Group/ScienceAgentBench)
- [ScienceAgentBench HAL Leaderboard](https://hal.cs.princeton.edu/scienceagentbench)

### Pillar 2 — Domain Science
- [AlphaFold3 at CASP16 · bioRxiv](https://www.biorxiv.org/content/10.1101/2025.04.10.648174v1)
- [AF3 Comprehensive Benchmark · PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12661943/)
- [AF3 in Drug Discovery · bioRxiv](https://www.biorxiv.org/content/10.1101/2025.04.07.647682v1.full.pdf)
- [Kaggle BELKA (NeurIPS 2024)](https://www.kaggle.com/competitions/leash-BELKA)
- [BELKA Analysis · Owlposting](https://www.owlposting.com/p/an-ml-drug-discovery-startup-trying)
- [Matbench Discovery · Leaderboard](https://matbench-discovery.materialsproject.org/)
- [Matbench Discovery · Nature MI 2025](https://www.nature.com/articles/s42256-025-01055-1)
- [GNoME · DeepMind](https://deepmind.google/blog/millions-of-new-materials-discovered-with-deep-learning/)
- [MatterGen · Azure AI Foundry](https://labs.ai.azure.com/projects/mattergen/)
- [WeatherBench 2 · AGU](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2023MS004019)
- [GraphCast · Science](https://www.science.org/doi/10.1126/science.adi2336)
- [AI Weather Models East Asia · Nature](https://www.nature.com/articles/s41612-024-00769-0)
- [AlphaProof · Nature 2025](https://www.nature.com/articles/s41586-025-09833-y)
- [miniF2F · arXiv 2511.03108](https://arxiv.org/pdf/2511.03108)
- [miniF2F GitHub](https://github.com/openai/miniF2F)
- [RSGPT Retrosynthesis · PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12314115/)
- [Retro-MTGR · Nature Comm 2025](https://www.nature.com/articles/s41467-025-56062-y)

### 조직위 연구진
- [Kyungtae Lim · KAIST Profile](https://pure.kaist.ac.kr/en/persons/kyungtae-lim/)
- [Chaok Seok · SeokLab GalaxyWEB](https://galaxy.seoklab.org/)
- [Chaok Seok · SNU Chemistry](https://chem.snu.ac.kr/en/research-faculty/faculty/fulltime?mode=view&q=&page=6&useyn=y&profidx=57&mode=view&listheight=10&page=9)
- [Jae Kyoung Kim · KAIST Math](https://mathsci.kaist.ac.kr/~jaekkim/)
- [Jae Kyoung Kim · Wikipedia](https://en.wikipedia.org/wiki/Kim_Jae_Kyoung)
- [Woo Youn Kim · KAIST Profile](https://pure.kaist.ac.kr/en/persons/woo-youn-kim/)
- [Chang Yun Son · Scholar](https://scholar.google.com/citations?user=jxZN0mkAAAAJ&hl=en)
- [Sungsoo Ahn · Homepage](https://sungsoo-ahn.github.io/)
- [Yonggyun Yu · Scholar](https://scholar.google.com/citations?user=tXElczcAAAAJ&hl=en)

---

## Appendix A — 6개 트랙 운영 파라미터 (제안서 연계)

(파라미터는 제안서 본문 `제안/2026-04-17-AI4Sci_Korea_연구자_경진대회_제안서.md` §IV 참조)

| 트랙 | 주 평가 | 보조 평가 | 재현성 | Hidden Data |
|---|---|---|---|---|
| T1 | Auto bench + Expert | ELO Arena (온사이트) | Frozen container + 트레이스 | 조직위 Hidden Problem |
| T2 | RMSE/AUROC Leaderboard | Top-K 웻랩 후보 평가 | Seed + Docker | Seok Lab/Kim Lab Hidden |
| T3 | Top-K + Synthesis Score | Chemist 블라인드 | 자동 채점 + 재실행 | Hidden Reaction Set |
| T4 | MAE + Inverse Match Rate | DFT 검증 + Expert | 3D 뷰어 + 구조 제출 | KRICT/KIST Hidden |
| T5 | RMSE/CRPS | Lead-time Curve | 자동 채점 | 기상청 AWS Hidden |
| T6 | pass@k (Lean) + Rubric | Expert 수학자 심사 | Lean verifier | IMO/KMO 확장 |

---

## Appendix B — 후속 `/sc:design`·`/sc:implement`에 전달할 입력

다음 결정이 `/sc:design`에 전달될 입력값:

1. **트랙 Scope 확정** (6트랙 확장 vs 2트랙 유지)
2. **Hidden Data 조달 범위** (Seok / Woo Youn Kim / Son / Ahn 연구실 · 기상청 · KRICT)
3. **재현성 Gate 임계선** (제출 Top N 중 몇 %를 Frozen Container 재실행 대상으로)
4. **참가 타겟 규모** (트랙당 50팀 × 6 = 300팀 vs 조정)
5. **국제 vs 국내 비중** (40:60 초안)
6. **상금·여비 구조** (MSIT 한도 내, 데이콘 별도 스폰서 유치 여부)

---

> **END OF RESEARCH REPORT**
> 본 리포트는 `/sc:research --depth deep` 범위 내에서 작성되었으며, 다음 단계(`/sc:design`·`/sc:implement`)에 대한 직접적 구현·설계 변경은 포함하지 않습니다.
