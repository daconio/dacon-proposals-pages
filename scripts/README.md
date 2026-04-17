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

## HTML → Google Slides 네이티브 업로드 (`html_to_slides.py`)

슬라이드 덱 HTML에서 **제목·부제·표·리스트·카드**를 추출해 **편집 가능한 Google Slides**로 업로드합니다.
시각 요소(그라디언트·아이콘·커스텀 카드 스타일)는 생략 — 텍스트/표 중심의 Tier 1-2 재현.

```bash
# Dry-run: API 호출 없이 추출 JSON만 stdout으로
python3 scripts/html_to_slides.py --dry-run 제안/foo.html > slides.json

# 실제 업로드 (최초 1회 브라우저 OAuth 동의창 뜸)
python3 scripts/html_to_slides.py 제안/foo.html

# 옵션: 제목·공유 이메일·페이지 비율
python3 scripts/html_to_slides.py --title "강원대 제안서" --share edgar@dacon.io \
    --page-size a4 제안/foo.html
```

### 최초 설정 (한 번만)

1. [GCP 콘솔](https://console.cloud.google.com/) 접속 → 프로젝트 생성 (기존 프로젝트 사용 가능)
2. **API 활성화**: `Google Slides API` + `Google Drive API`
3. **OAuth 클라이언트 생성**:
   - `APIs & Services → Credentials → Create Credentials → OAuth client ID`
   - Application type: **Desktop app**
   - 생성된 클라이언트의 **JSON 다운로드**
4. JSON을 `~/.config/dacon-slides/credentials.json` 으로 저장
5. pip 의존성 설치:
   ```bash
   pip3 install google-api-python-client google-auth-oauthlib google-auth-httplib2 beautifulsoup4
   ```
6. 첫 실행 시 브라우저 동의창 → 승인 → 토큰은 `~/.config/dacon-slides/token.json` 에 자동 캐시

`DACON_SLIDES_DIR` 환경변수로 credentials/token 저장 경로 커스터마이징 가능.

### 옵션

| 옵션 | 기본값 | 설명 |
|---|---|---|
| `--title TEXT` | 입력 파일 stem | Google Slides 제목 |
| `--page-size` | `16x9` | `16x9` / `a4` (A4 landscape) |
| `--share EMAIL` |  | 완성 후 writer 권한으로 해당 이메일에 공유 |
| `--dry-run` |  | API 호출 없이 추출 JSON만 stdout |
| `--quiet`, `-q` |  | 진행 메시지 숨김 |

### 추출 대상 (Tier 1-2)

- 슬라이드 타입 자동 분류: `cover` / `section` / `content` / `end`
- 헤더 라벨(`.sh-l`), 태그(`.tag`), 제목(`h2.st`), 부제(`.sub`/`.sd`)
- 표(`<table>`) → 네이티브 Slides 표 (편집 가능)
- 불릿 리스트(`ul.ck`) → 네이티브 불릿 텍스트
- 카드(`.c-t` + `.c-d`) → 압축 텍스트 ("제목 — 설명" 형식)
- 메트릭(`.mx`, `.kpi .k`) → 추출되지만 v1에선 렌더 생략
- 페이지 번호(`.sf-pg`) → 우하단 작은 텍스트

### 한계 및 권장 워크플로우

* 복잡한 CSS 시각 효과(그라디언트, 아이콘, 라운드 카드, 스텝 애니메이션)는 **재현하지 않음**
* 시각 완벽 보존이 필요하면: `make_pdf.py`로 PDF/PNG 추출 → Slides에 이미지로 삽입하는 방식이 더 적합
* 이 스크립트는 **Slides에서 텍스트·표를 직접 편집해야 할 때** 유용 (협업 리뷰·번역·금액 삽입 등)

---

## HTML → PDF 2가지 포맷 변환 (`make_pdf.py`)

**A4(landscape/portrait)와 16:9** 2가지 포맷을 **한 번의 슬라이드 캡처로** 동시 생성하는 래퍼입니다.
대면 배포용 A4 인쇄본과 프레젠테이션용 16:9 파일을 분리 관리할 때 유용합니다.

```bash
# 기본: 16:9 + A4 landscape 둘 다 생성 (2가지 버전)
python3 scripts/make_pdf.py 제안/2026-04-17-강원대_부트캠프.html

# 한 포맷만
python3 scripts/make_pdf.py --format 16x9 제안/foo.html
python3 scripts/make_pdf.py --format a4   제안/foo.html    # A4 landscape
python3 scripts/make_pdf.py --format a4p  제안/foo.html    # A4 portrait

# 전부 (16:9 + A4 landscape + A4 portrait)
python3 scripts/make_pdf.py --format all  제안/foo.html

# 고품질 (scale 3× + 무손실 PNG 임베드 — 최종 납품용)
python3 scripts/make_pdf.py --hq 제안/foo.html
```

### 출력 파일명 규칙 (입력 HTML과 같은 폴더)

| 포맷 | 확장자 | PDF 페이지 크기 |
|---|---|---|
| **16:9** | `<stem>.pdf` | 960 × 540 pt (= 1280 × 720 px @ 96dpi) |
| **A4 landscape** | `<stem>.a4.pdf` | 842 × 595 pt (= 297 × 210 mm) |
| **A4 portrait** | `<stem>.a4p.pdf` | 595 × 842 pt (= 210 × 297 mm) |

### 동작 방식

1. **슬라이드 캡처 1회**: Playwright로 `.slide`를 1280×720 PNG로 한 번만 캡처
2. **포맷별 PDF 조립**:
   - 16:9: PNG를 그대로 임베드 → 960×540pt 페이지
   - A4: 1280×720 PNG를 A4 흰 캔버스(@300dpi)에 **센터 피팅 + 레터박스**로 합성 → img2pdf로 PDF 조립

### 옵션

| 옵션 | 기본값 | 설명 |
|---|---|---|
| `--format` (`-f`) | `both` | `16x9` / `a4` / `a4p` / `both`(16x9+a4) / `all`(16x9+a4+a4p) |
| `--scale N` | 2 | 캡처 device_scale_factor (2=Retina, 3=고해상도) |
| `--lossless` |  | PNG 무손실 임베드 (`img2pdf` 필요) |
| `--hq` |  | `--scale 3 + --lossless` 통합 |
| `--quiet` (`-q`) |  | 진행 메시지 숨김 |

### 의존성 (`html_to_pdf.py`와 동일)

- `playwright`, `Pillow`, `img2pdf`(lossless/hq), `PyPDF2`(선택), Google Chrome

---

## HTML → PDF 변환 (`html_to_pdf.py`) — 16:9 전용

슬라이드 덱(`.slide` 요소 기반) HTML을 정확한 비율의 PDF로 변환합니다.

**방식**: Playwright + Chrome 헤드리스로 슬라이드를 1개씩 **screen 미디어 스크린샷**(2× 해상도)으로 캡처한 뒤, Pillow로 다중 페이지 PDF를 조립합니다. 이 방식이 필요한 이유:
- 슬라이드 덱 HTML은 보통 `@media print { .slide { display:flex !important; opacity:1 !important } }` 같은 인쇄 모드 강제 표시 규칙을 가짐
- Chrome의 `print-to-pdf`는 print 미디어를 강제 활성화 → 모든 슬라이드가 동시에 보이게 되어 inline display:none 우회 불가
- 결과: PDF의 첫 720px 영역(슬라이드 0)만 캡처되고 나머지는 헤더만 렌더되는 현상 발생
- **해결**: `page.pdf()`를 포기하고 `page.screenshot()` (스크린 미디어 사용)으로 슬라이드를 1장씩 PNG로 캡처

```bash
# 단일 파일 변환 (출력은 같은 폴더 .pdf)
python3 scripts/html_to_pdf.py "제안/2026-04-08-강원대학교_X+AI_SW융합프로젝트_제안서.html"

# 여러 파일 / 글롭
python3 scripts/html_to_pdf.py "제안/2026-04-08-강원대_DAKER_*.html"

# 출력 경로 명시
python3 scripts/html_to_pdf.py input.html -o /tmp/out.pdf

# 세로형 슬라이드 (A4 portrait 비율)
python3 scripts/html_to_pdf.py --width 960 --height 1358 portrait.html

# 진행 메시지 숨김
python3 scripts/html_to_pdf.py --quiet input.html
```

### 옵션
| 옵션 | 기본값 | 설명 |
|---|---|---|
| `--width N` | 1280 | 슬라이드 가로 px (HTML 슬라이드 원본 폭과 일치) |
| `--height N` | 720 | 슬라이드 세로 px |
| `--scale N` | 2 | device_scale_factor. 2=Retina, 3=고해상도, 4=초고해상도 |
| `--lossless` |  | PNG 무손실 임베드 (`/FlateDecode`). JPEG 압축 아티팩트 제거, `img2pdf` 필요 |
| `--hq` |  | `--scale 3` + `--lossless` 통합 (가성비 추천 — 텍스트 거의 벡터 수준) |
| `--output PATH` (`-o`) | 입력 파일과 동일 폴더, `.pdf` 확장자 | 출력 경로 |
| `--quiet` (`-q`) |  | 진행 메시지 숨김 |
| `--no-verify` |  | PyPDF2 사후 검증 스킵 |

### 품질 / 파일 크기 트레이드오프 (강원대 22슬라이드 기준)

| 설정 | 해상도 | 파일 크기 | 변환 시간 | 임베드 포맷 | 추천 용도 |
|---|---|---|---|---|---|
| 기본 (`--scale 2`) | 2560×1440 | 3.2 MB | 13s | JPEG q95 | 빠른 검토, 이메일 첨부 |
| `--scale 3` | 3840×2160 | 6.2 MB | 16s | JPEG q95 | 일반 인쇄, 발표용 |
| `--hq` (3× + 무손실) | 3840×2160 | **9.9 MB** | 28s | PNG `/FlateDecode` | **최종 납품·고품질 인쇄** (텍스트 가장자리 픽셀 단위 선명) |

### 의존성
- `playwright` (`pip install playwright`) — 시스템 Chrome 사용하므로 `playwright install` 불필요
- `Pillow` (`pip install Pillow`) — JPEG 모드 PDF 조립
- `img2pdf` (`pip install img2pdf`) — `--lossless` / `--hq` 모드 PNG 무손실 임베드
- `PyPDF2` (`pip install PyPDF2`) — 검증용 (선택)
- Google Chrome.app (macOS 기본 경로 자동 탐지)

### 검증된 출력 특성
- 모든 PDF 뷰어에서 일관된 페이지 수 인식 (`file`, PyPDF2, macOS Spotlight 모두 동일)
- 페이지 크기는 슬라이드 원본 비율을 그대로 보존 (1280×720 → 960×540 pt)
- 2× 해상도(2560×1440 PNG)로 캡처되어 인쇄 시에도 선명
- 각 슬라이드의 `[data-step]` 애니메이션이 모두 펼친 상태로 캡처됨

## MD ↔ HTML 동기화 검증 (`check_md_html_sync.py`)

같은 제안서의 `.md`와 `.html`(슬라이드 덱) 두 파일이 항상 동일한 섹션 구조와 핵심 사실을 유지하는지 검증합니다. pre-commit 훅에서 자동 호출되어 드리프트를 조기에 잡아냅니다.

```bash
# 사전 정의된 모든 페어 검사
python3 scripts/check_md_html_sync.py --all

# 특정 페어 (예: 강원대)
python3 scripts/check_md_html_sync.py --pair 강원대

# 임의 페어 직접 지정
python3 scripts/check_md_html_sync.py path/to/file.md path/to/file.html
```

검증 항목:
- HTML 슬라이드 라벨(`.sh-l`)의 섹션 번호(II-1-라, III, VI 등)와 MD 헤더 정렬
- 핵심 키워드(250명, 65팀, 7.8 본선, 데이콘(주) 등) 양쪽 존재 여부

새 페어 추가는 `scripts/check_md_html_sync.py`의 `PAIRS` 딕셔너리와 `KEY_FACTS`에 항목 추가.

## 구조

```
scripts/
├── cards.json             # 카드 단일 소스
├── sync_cards.py          # index.html 생성기 + 스캐너 (stdlib only)
├── html_to_slides.py      # HTML 슬라이드 → Google Slides 네이티브 업로드 (bs4 + Slides API)
├── make_pdf.py            # HTML 슬라이드 → A4 + 16:9 2가지 포맷 동시 생성 (playwright + Pillow + img2pdf)
├── html_to_pdf.py         # HTML 슬라이드 → 16:9 PDF 단일 변환기 (playwright + Pillow)
├── check_md_html_sync.py  # MD ↔ HTML 동기화 검증
└── README.md              # 이 파일

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
