# Antigravity 치트시트

Google의 에이전트 기반 AI IDE — 단축키, 에이전트 명령어, 설정 완벽 가이드

- macOS Shortcuts
- Agent Commands
- AGENTS.md Config

Powered by Gemini | 2026.03

---

## Antigravity 소개

Google이 만든 에이전트 퍼스트 AI IDE — 코딩의 중력을 없앤다

| 지표 | 값 |
|------|-----|
| SWE-bench Verified | 76.2% |
| 최초 발표 | 2025.11 |
| 기본 엔진 | Gemini 3 |

### 에이전트 퍼스트 IDE

에이전트가 계획 → 실행 → 검증을 자율 수행. Artifacts(작업 목록, 스크린샷, 브라우저 녹화) 자동 생성

### VSCode 포크 기반

기존 VSCode 단축키 대부분 호환. 익숙한 UI, 확장 에코시스템 그대로 활용

- **개인 무료** — Pro 플랜 별도
- **Claude + OpenAI** — Sonnet/Opus 4.6, GPT 모델 지원
- **AGENTS.md / GEMINI.md** — 에이전트 행동 커스터마이즈

---

## 01. Antigravity 전용 단축키

Agent Manager, AI 명령, Git 통합 키바인딩

### View Toggle

| 단축키 | 동작 |
|--------|------|
| `⌘+E` | Agent Manager ↔ Editor View 토글 |
| `⌘+⇧+M` | Editor View ↔ Manager View 토글 (대안) |
| `⌘+L` | 에이전트 패널 포커스 토글 |
| `⌘+B` | 사이드바 토글 |

### AI Commands

| 단축키 | 동작 |
|--------|------|
| `⌘+I` | 인라인 AI 명령 (에디터 + 터미널) |
| `Tab` | AI 코드 완성 수락 |
| `Esc` | AI 제안 닫기 |
| `⌘+⇧+I` | 에이전트 패널 열기/포커스 |
| `⌘+⇧+L` | 새 대화 스레드 시작 |

### Git

| 단축키 | 동작 |
|--------|------|
| `⌘+⏎` | 모든 변경 스테이지 + AI 커밋 메시지 생성 + 동기화 |

---

## 02. 에이전트 컨텍스트 명령어

@ 멘션으로 컨텍스트 전달, MCP 서버 연결

### Built-in Context

| 명령어 | 설명 |
|--------|------|
| **@workspace** | 전체 프로젝트 워크스페이스 포함 |
| **@file** | 특정 파일 참조 (이름/경로) |
| **@terminal** | 현재 터미널 출력 전송 |
| **@problems** | 문제 패널 (오류 & 경고) 첨부 |
| **@selection** | 에디터에서 선택한 텍스트 전달 |
| **@codebase** | 인덱싱된 프로젝트 파일 전체 검색 |

### MCP Server Context

| 명령어 | 설명 |
|--------|------|
| **@Supabase** | Supabase 서버 연결 |
| **@Cloudflare** | Cloudflare 서버 연결 |
| **@Firebase** | Firebase 서버 연결 |
| **@Linear** | Linear 프로젝트 티켓 참조 |
| **@Vercel** | Vercel 배포 로그 가져오기 |

---

## 워크플로우 슬래시 명령어

에이전트에게 특정 작업을 지시하는 빌트인 워크플로우

| 명령어 | 설명 |
|--------|------|
| **/generate-unit-tests** | 현재 파일/선택 영역 테스트 생성 |
| **/fix-errors** | 문제 패널 오류 일괄 수정 |
| **/explain** | 선택한 코드 블록 설명 |
| **/refactor** | 가독성/성능 개선 리팩토링 |
| **/document** | JSDoc/docstring 주석 추가 |
| **/deploy** | 커스텀 배포 트리거 |
| **/<your-workflow>** | 커스텀 워크스페이스 워크플로우 (직접 정의 가능) |

---

## 03. MCP 서버 & 설정

Model Context Protocol 서버 빠른 설치

### MCP 빠른 설치

npx 한 줄로 MCP 서버를 즉시 연결

| 서버 | 설치 명령어 |
|------|------------|
| **Supabase** | `npx @modelcontextprotocol/server-postgres [connection-string]` |
| **Firebase** | `npx firebase-tools@latest mcp --only firestore,auth,storage` |
| **n8n** | `npx n8n-mcp` |
| **Playwright** | `npx @playwright/mcp@latest` |
| **Filesystem** | `npx @modelcontextprotocol/server-filesystem [path]` |
| **GitHub** | `npx @modelcontextprotocol/server-github` |

---

## 04. AGENTS.md 설정

에이전트 행동을 코드로 정의하는 설정 파일

### 파일 위치 & 우선순위

#### Priority Order (높음 → 낮음)

| 순위 | 레이어 | 설명 |
|------|--------|------|
| 1 | **System Rules** | 불변, 오버라이드 불가 |
| 2 | **GEMINI.md** | 최우선 사용자 설정 |
| 3 | **AGENTS.md** | 크로스 도구 공통 |
| 4 | **.agent/rules/** | 보충 워크스페이스 파일 |

#### File Paths

| 범위 | 경로 |
|------|------|
| **글로벌** | `~/.gemini/AGENTS.md` |
| **프로젝트** | `./AGENTS.md` (루트, 모든 도구 공유) |
| **Antigravity 전용** | `./GEMINI.md` |
| **하위 디렉토리** | `./src/api/AGENTS.md` |

### AGENTS.md 핵심 섹션

에이전트에게 프로젝트 맥락을 전달하는 6가지 핵심 블록

1. **Project Overview** — 이름, 유형, 단계 (Prototype / Production / Maintenance)
2. **Tech Stack** — 언어, 프레임워크, 라이브러리, 빌드 도구
3. **Code Quality** — 파일/함수 길이 제한, 복잡도, 타입 시스템
4. **Testing** — 단위/통합/E2E 테스트 요구사항, 최소 커버리지
5. **Safety Guardrails** — DB 쓰기 확인, 배포 승인, 시크릿 관리
6. **Git Conventions** — 커밋 메시지, PR 제목, 브랜치 네이밍

---

## 05. VSCode 호환 단축키

VSCode에서 그대로 이어지는 필수 키바인딩

### Navigation

| 단축키 | 동작 |
|--------|------|
| `⌘+P` | 파일 검색 |
| `⇧⌘+P` | 커맨드 팔레트 |
| `⇧⌘+F` | 전체 검색 |
| `⌃+`` ` | 터미널 토글 |
| `⌃+G` | 줄 번호 이동 |
| `⌘+Click` | 정의로 이동 |
| `⌃+-` | 이전 위치로 돌아가기 |

### Editing

| 단축키 | 동작 |
|--------|------|
| `⌘+D` | 다음 일치 선택 |
| `⇧⌘+L` | 모든 일치 선택 |
| `⌥+↑/↓` | 줄 이동 |
| `⇧⌘+K` | 줄 삭제 |
| `⌘+/` | 주석 토글 |
| `⌘+Z` / `⇧⌘+Z` | 실행취소 / 다시실행 |
| `⇧⌘+[` / `]` | 코드 접기 / 펼치기 |

### 추가 단축키

- `⌘+\` — 에디터 분할
- `⌘+1/2/3` — 분할 에디터 포커스
- `⇧⌘+V` — 마크다운 미리보기

---

## 크로스 도구 호환성

| 도구 | AGENTS.md 지원 | 설정 파일 |
|------|----------------|-----------|
| **Antigravity v1.20.3+** | 네이티브 지원 | AGENTS.md or GEMINI.md |
| **Cursor** | 지원 | .cursor/rules/ |
| **Claude Code** | CLAUDE.md | 심링크 또는 CI 동기화 권장 |
| **Windsurf** | 지원 | .windsurfrules |

### AGENTS.md 작성 베스트 프랙티스

- **300-600줄 유지** (성숙 프로젝트)
- **"왜(Why)" 문서화** — 지시만 하지 말 것
- **자율 실행 안전 규칙 명시**
- **월 1회 업데이트 검토**
- **PR 리뷰처럼 변경사항 관리**

---

## Master Antigravity

Google의 에이전트 퍼스트 AI IDE 완벽 가이드

- [antigravity.codes](https://antigravity.codes)
- [antigravitylab.net](https://antigravitylab.net)
- [codelabs.developers.google.com](https://codelabs.developers.google.com)

2026.03
