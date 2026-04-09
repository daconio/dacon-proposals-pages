# scripts/ — 랜딩 페이지 카드 자동 동기화

`index.html` 카드 그리드를 단일 매니페스트(`scripts/cards.json`)에서 자동 생성합니다.

## 빠른 시작 (한 번만)

```bash
git config core.hooksPath .githooks   # pre-commit 훅 설치
```

이후부터는 커밋할 때 자동 실행됩니다.

## 새 제안서를 랜딩 페이지에 추가하는 방법

1. `제안/` 또는 `내부/`·`전략/` 폴더에 HTML 파일 추가 (예: `2026-04-15-신규고객_제안서.html`)
2. `scripts/cards.json`을 열어 해당 섹션(`제안서` 등)의 `cards` 배열 맨 위에 항목 추가:
   ```json
   {
     "href": "제안/2026-04-15-신규고객_제안서.html",
     "title": "신규고객 AI 경진대회 제안서",
     "date": "2026.04.15",
     "icon": "신",
     "color": "blue",
     "badge": "NEW"
   }
   ```
3. `git add` + `git commit` — 훅이 자동으로 `index.html`을 재생성하고 re-stage합니다.

### 필드 설명

| 필드 | 값 |
|---|---|
| `href` | 파일 상대 경로. `+` 문자는 `%2B`로 URL 인코딩 권장. |
| `title` | 카드 제목 (랜딩 페이지에 표시) |
| `date` | `YYYY.MM.DD` 형식 |
| `icon` | 카드 아이콘에 표시할 1~2자 문자 (한글/영문) |
| `color` | `blue` · `warm` · `dark` 중 택1 |
| `badge` | `NEW` · `제안서` · `소개서` · `전략서` · `리서치` · `슬라이드` |

## 수동 명령어

```bash
# 매니페스트 기준으로 index.html 재생성
python3 scripts/sync_cards.py

# 변경 필요 여부만 체크 (변경 필요 시 exit 1)
python3 scripts/sync_cards.py --check

# 제안/·내부/·전략/ 폴더에 등록 안 된 HTML 파일 탐색
python3 scripts/sync_cards.py --scan

# sync + scan 한 번에
python3 scripts/sync_cards.py --all
```

## 등록 제외하고 싶은 파일

파일을 매니페스트에 등록하지 않되 scan 경고도 띄우지 않으려면
`scripts/cards.json`의 `scan.ignore_patterns`에 파일명 부분 문자열을 추가합니다.

```json
"ignore_patterns": [
  "_치트시트",
  "신규_제외_키워드"
]
```

## 훅 우회

```bash
SKIP_CARD_SYNC=1 git commit -m "..."   # 이번 커밋만 카드 sync 스킵
git commit --no-verify -m "..."        # 모든 pre-commit 훅 스킵
```

## 구조

```
scripts/
├── cards.json       # 단일 소스: 섹션·카드·scan 설정
├── sync_cards.py    # 생성기 + 스캐너 (stdlib only)
└── README.md        # 이 파일

.githooks/
└── pre-commit       # 커밋 시 auto-sync + 미등록 경고

index.html
  └── <!-- AUTO:cards-start --> ... <!-- AUTO:cards-end -->
      ↑ 이 구간만 스크립트가 재생성. 마커 바깥은 수동 편집 안전.
```

## 구현 노트

- **macOS NFD**: Finder/HFS+는 한글 파일명을 NFD(분리형 자모)로 저장하지만 JSON은 보통 NFC. `unicodedata.normalize("NFC", ...)`로 양쪽 정규화 후 비교.
- **URL-encoded `+`**: 일부 Vercel 경로에서 `+`가 공백으로 해석될 수 있어 `%2B`로 인코딩 권장. scan 비교 시엔 `%2B → +`로 정규화.
- **제로 의존성**: `sync_cards.py`는 Python stdlib만 사용 (`json`, `re`, `unicodedata`). PyYAML·PIL 등 외부 패키지 불필요.
