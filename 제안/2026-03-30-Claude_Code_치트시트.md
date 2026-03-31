# Claude Code 치트시트

명령어, 단축키, 설정 완벽 가이드 — 2026 Edition

---

## 01. 설치 & 시작

### 설치부터 실행까지

플랫폼별 설치 명령어와 기본 실행 방법

#### macOS / Linux

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

#### Homebrew

```bash
brew install --cask claude-code
```

#### Windows

```powershell
irm https://claude.ai/install.ps1 | iex
```

#### npm (Node.js)

```bash
npm install -g @anthropic-ai/claude-code
```

#### 프로젝트 실행

```bash
cd your-project && claude
```

#### 업데이트

```bash
claude update
```

---

## 02. 키보드 단축키

### 글로벌 & 채팅 단축키

#### Global Actions

| 단축키 | 설명 |
|--------|------|
| `Ctrl+C` | 현재 작업 취소 |
| `Ctrl+D` | Claude Code 종료 |
| `Ctrl+T` | 작업 목록 토글 |
| `Ctrl+O` | 상세 트랜스크립트 토글 |

#### Chat Actions

| 단축키 | 설명 |
|--------|------|
| `Escape` | 현재 입력 취소 |
| `Esc` + `Esc` | 되감기 메뉴 (변경사항 실행취소) |
| `Shift+Tab` | 권한 모드 전환 |
| `Cmd+P` | 모델 선택기 |
| `Cmd+T` | 확장 사고 토글 |
| `Enter` | 메시지 전송 |
| `Ctrl+G` | 외부 에디터에서 열기 |
| `Ctrl+S` | 현재 프롬프트 보관 |
| `Ctrl+V` | 이미지 붙여넣기 |

### 히스토리, 자동완성 & 특수 입력

#### History Navigation

| 단축키 | 설명 |
|--------|------|
| `Ctrl+R` | 히스토리 검색 |
| `Up` | 이전 히스토리 |
| `Down` | 다음 히스토리 |

#### Autocomplete

| 단축키 | 설명 |
|--------|------|
| `Tab` | 제안 수락 |
| `Escape` | 메뉴 닫기 |

#### Task Actions

| 단축키 | 설명 |
|--------|------|
| `Ctrl+B` | 현재 작업 백그라운드 전환 |

#### Special Input

| 입력 | 설명 |
|------|------|
| `!` | Bash 모드 접두사 |
| `@` | 파일/폴더 멘션 |
| `\` + `Enter` | 줄바꿈 |

---

## 03. 슬래시 명령어

### 필수 슬래시 명령어

| 명령어 | 설명 |
|--------|------|
| `/help` | 도움말 |
| `/clear` | 대화 기록 초기화 |
| `/compact` | 대화 요약 (선택적 포커스) |
| `/config` | 설정 확인/수정 |
| `/cost` | 토큰 사용량 통계 |
| `/doctor` | 설치 상태 점검 |
| `/exit` | 종료 |
| `/init` | 프로젝트 CLAUDE.md 초기화 |
| `/model` | AI 모델 변경 |
| `/memory` | CLAUDE.md 메모리 편집 |
| `/review` | 코드 리뷰 요청 |
| `/rewind` | 대화/코드 되감기 |
| `/vim` | Vim 모드 진입 |
| `/login` | 로그인 |
| `/permissions` | 권한 관리 |
| `/status` | 시스템 상태 |

### 고급 슬래시 명령어

| 명령어 | 설명 |
|--------|------|
| `/mcp` | MCP 서버 관리 |
| `/agents` | 커스텀 서브에이전트 관리 |
| `/plugin` | 플러그인 관리 |
| `/hooks` | 훅 설정 |
| `/sandbox` | 샌드박스 bash 도구 활성화 |
| `/pr_comments` | PR 코멘트 보기 |
| `/terminal-setup` | Shift+Enter 키 바인딩 설치 |
| `/usage` | 플랜 사용량/제한 |
| `/add-dir` | 추가 작업 디렉토리 |
| `/bug` | 버그 리포트 |

---

## 04. CLI 플래그 & 헤드리스 모드

### CLI 플래그 레퍼런스

| 명령어 | 설명 |
|--------|------|
| `claude` | 인터랙티브 세션 시작 |
| `claude "prompt"` | 초기 프롬프트와 시작 |
| `claude -c` | 최근 세션 이어하기 |
| `claude -r "name"` | 특정 세션 재개 |
| `claude -p "query"` | 비대화형 모드 |

| 플래그 | 설명 |
|--------|------|
| `--output-format json` | JSON 출력 |
| `--output-format stream-json` | 스트리밍 JSON |
| `--max-turns 3` | 에이전트 턴 제한 |
| `--append-system-prompt` | 시스템 프롬프트 추가 |
| `--verbose` | 상세 로깅 |
| `--permission-mode auto` | 자동 권한 모드 |

---

## 05. 설정 & 구조

### 설정 명령어 & 파일 우선순위

#### 설정 명령어

| 명령어 | 설명 |
|--------|------|
| `claude config list` | 설정 목록 |
| `claude config get <key>` | 특정 설정 확인 |
| `claude config set <key> <val>` | 설정 변경 |
| `claude config add <key> <val>` | 배열 설정에 추가 |
| `claude config remove <key> <val>` | 배열에서 제거 |

#### 설정 파일 우선순위 (높은 순)

1. `/etc/claude-code/managed-settings.json` — Enterprise
2. `.claude/settings.local.json` — 프로젝트 로컬 (git-ignored)
3. `.claude/settings.json` — 프로젝트 공유
4. `~/.claude/settings.json` — 유저 글로벌

### 디렉토리 구조 & MCP 서버

#### 디렉토리 구조

| 경로 | 용도 |
|------|------|
| `.claude/commands/` | 프로젝트 슬래시 명령어 |
| `~/.claude/commands/` | 유저 슬래시 명령어 |
| `.claude/skills/` | 프로젝트 에이전트 스킬 |
| `~/.claude/skills/` | 개인 에이전트 스킬 |
| `.claude/agents/` | 프로젝트 서브에이전트 |
| `.claude/hooks/` | 프로젝트 훅 |

#### MCP 서버 관리

서버 추가 (stdio):

```bash
claude mcp add <name> <cmd> [args...]
```

서버 추가 (SSE):

```bash
claude mcp add --transport sse <name> <url>
```

서버 목록:

```bash
claude mcp list
```

서버 제거:

```bash
claude mcp remove <name>
```

### Hook 이벤트 레퍼런스

Claude Code 동작의 각 단계에서 커스텀 스크립트를 실행할 수 있습니다

| 이벤트 | 설명 |
|--------|------|
| `PreToolUse` | 도구 호출 전 (차단 가능) |
| `PostToolUse` | 도구 호출 후 |
| `UserPromptSubmit` | 프롬프트 제출 시 |
| `Notification` | 알림 발생 시 |
| `Stop` | 응답 완료 시 |
| `SubagentStop` | 서브에이전트 완료 시 |
| `PreCompact` | 컴팩트 전 |
| `SessionStart` | 세션 시작/재개 시 |
| `SessionEnd` | 세션 종료 시 |

> **참고:** `PreToolUse` 훅은 `exit 2` 반환으로 도구 실행을 차단할 수 있습니다

---

## References

Sources: awesomeclaude.ai | computingforgeeks.com | claudefa.st
