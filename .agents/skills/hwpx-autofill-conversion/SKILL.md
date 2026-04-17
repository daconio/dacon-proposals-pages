---
name: hwpx-autofill-conversion
description: HWPX 한글 양식 파일을 주제에 맞춰 자동으로 채워 새 HWPX를 생성한다. 사용자가 .hwpx 양식(템플릿, 보고서 서식, 제안서 양식, 요청서 양식 등)을 건네면서 "이 주제로 작성해줘", "양식에 맞춰 채워줘", "hwpx 자동 채우기", "제안 요청서 양식 그대로 내용만 바꿔줘", "보고서 양식에 내용 넣어줘", "hwpx autofill" 등을 언급하면 반드시 이 스킬을 사용하라. 한글 양식 기반 문서 자동 작성 전반에서 최우선으로 트리거된다. .hwp (바이너리) 파일은 먼저 .hwpx로 변환이 필요하며 이 스킬은 .hwpx 전용이다.
---

# HWPX Autofill Conversion

한글(HWPX) **양식 파일을 주제에 맞춰 자동으로 채워** 새로운 HWPX를 생성하는 스킬입니다. 양식의 서체·여백·표·이미지·스타일은 그대로 유지하고 **텍스트만** 사용자가 지정한 주제에 맞게 교체합니다.

## 언제 사용하는가

- 사용자가 `.hwpx` 양식 파일과 함께 "이 주제로 작성해줘", "양식에 맞춰 채워줘" 등을 요청할 때
- 고정된 보고서/제안서/요청서 양식에 여러 주제별 문서를 만들어야 할 때
- 양식의 레이아웃과 디자인은 건드리지 않고 내용만 갈아 끼우고 싶을 때

이 스킬은 **.hwpx 전용**입니다. 레거시 `.hwp` 바이너리 포맷이면 먼저 hwp-organizer 스킬 등으로 `.hwpx`로 변환한 뒤 사용하세요.

## 핵심 철학

HWPX는 ZIP + XML이고, 양식의 서식 정보는 `Contents/header.xml` 과 `section0.xml` 안의 `paraPrIDRef` / `charPrIDRef` 속성에 박혀 있습니다. 이 속성들을 새로 만들려고 하면 폰트·굵기·들여쓰기가 깨지기 쉽습니다. 그래서 이 스킬은 **"양식을 그대로 두고 텍스트만 바꾼다"** 는 원칙을 따릅니다.

세 가지 동작 모드가 있고, 모두 이 원칙을 지킵니다:

- **slot mode** — 양식에 이미 존재하는 `<hp:t>` 텍스트 노드 중 **비어있지 않은 것**을 문서 순서대로 새 텍스트로 교체. 구조적 편집이 없으므로 **표·이미지·머리말·각주·복잡한 레이아웃이 그대로 살아남습니다.** 대부분의 "양식 채우기" 작업에는 이 모드를 쓰세요.
- **targeted mode** — 특정 `<hp:t>` 노드를 **절대 인덱스**로 지정해 교체. 공백(whitespace)만 있는 텍스트 노드까지 포함하므로, slot mode 가 닿지 못하는 **비어있는 목차 셀·placeholder 셀**을 채울 수 있습니다. `slot mode 와 결합** 가능 — 하나의 content.json에 `slots` 와 `targeted` 를 같이 넣으면 slot 먼저 적용 후 targeted 덮어쓰기.
- **blocks mode** — 본문을 아예 새로 구성하고 싶을 때. 양식의 제목/본문 문단을 "아키타입"으로 복제해 새 내용을 얹습니다. 섹션 속성(페이지 크기·여백)과 필요에 따라 특정 표는 보존됩니다.

### 언제 targeted mode가 꼭 필요한가 — 비어있는 목차 함정

한국 관공서 양식들은 목차(TOC) 를 **미리 그려둔 빈 셀의 격자**로 만든 경우가 많습니다. 예: "목 차" 라벨 뒤에 Ⅰ장~Ⅵ장 제목이 들어갈 10여 개의 빈 `<hp:t>` 공백 노드가 이미 배치되어 있는 식. 이 노드들은 slot mode 의 인덱스에서 **완전히 빠져 있습니다** (non-empty 필터 때문). 결과적으로:

1. slot mode 로 본문 장 제목을 바꾸면 **본문은 새 제목으로 바뀌지만 목차는 공백 그대로** 남는다.
2. HWP 뷰어가 보여주는 목차는 이전 버전에서 캐시된 TOC 텍스트(`Preview/PrvText.txt` 등)라, 한글에서 "목차 업데이트"를 누르기 전까지는 **이전 제목이 그대로 보인다**.
3. 그래서 "목차가 본문과 안 맞는다"는 증상이 생긴다.

해결: `inspect_template.py --all` 로 절대 인덱스를 확인해서, 목차 영역의 공백 노드 인덱스를 찾아 `targeted` 로 장 제목을 주입하세요. 그러면 HWP 에서 목차 업데이트를 누르지 않아도 새 목차가 바로 보입니다.

## 파이프라인

```
template.hwpx
    │
    ▼
[1] inspect_template.py  ──▶  (콘솔 또는 JSON 리포트)
    │                           슬롯 번호 / 레벨 / 원본 텍스트 / 표 목록
    ▼
[2] Codex가 content.json 작성
    │   (slot mode = 문자열 배열, blocks mode = 블록 객체 배열)
    ▼
[3] autofill.py  ──▶  out.hwpx
```

## 실행 방법

### 1. 양식 검사 (항상 먼저)

```bash
python3 scripts/inspect_template.py <template.hwpx> --summary
```

출력 예시:

```
## Contents/section0.xml  (81 paragraphs)
   Text slots: 104,  Tables: 11

   Slots (first 40):
     [  0] body     2027년 회계연도
     [  1] body     회계감사인 선임 제안 요청서
     [  2] body     2026. 2. 14.
     [  3] body     부    서(부)
     ...
```

각 슬롯 번호는 **autofill 이 실제로 교체할 `<hp:t>` 노드의 문서 순서**와 정확히 일치합니다. 표 안의 셀 텍스트도 슬롯에 포함됩니다 — 한국 공식 양식은 "부서/담당/연락처" 같은 정보 상자를 표로 만드는 경우가 많기 때문에, 이 부분까지 채우지 못하면 쓸모가 없습니다.

레벨(`section`/`h1`~`h4`/`body`)은 텍스트 앞글자(`Ⅰ`, `□`, `○`, `-`, `※`)로 추정한 것으로, slot mode 에서는 단순 라벨링일 뿐이고, blocks mode 에서 아키타입 매칭에 사용됩니다.

전체 리포트를 JSON으로 저장하려면:

```bash
python3 scripts/inspect_template.py <template.hwpx> --out template_report.json
```

**`--all` 플래그**: 공백만 있는 `<hp:t>` 노드(=targeted mode 대상)까지 **절대 인덱스**로 함께 출력합니다. 출력 형식:

```
abs[ 14] body     목  차
abs[ 15] empty    <ws len=1>
abs[ 16] empty    <ws len=2>
...
abs[ 25] body     •
abs[ 26] body     별지 제1호~제5호: ...
```

목차 같은 placeholder 영역은 이 출력에서 `empty` 연속 구간으로 쉽게 식별할 수 있습니다. 여기서 찾은 `abs` 번호를 `targeted` 의 키로 사용하세요.

### 2. content.json 작성 (Codex의 역할)

#### Slot mode (권장 — 표·이미지·레이아웃을 그대로 유지)

`content.json` 은 **문자열 배열**입니다. 배열의 N번째 요소가 양식의 슬롯 N을 대체합니다. 슬롯 수보다 적게 넣어도 되며, 그 경우 뒤쪽 슬롯은 원본 텍스트를 유지합니다.

```json
[
  "2027 회계연도",
  "AI 교육 혁신 사업 제안 요청서",
  "2026. 4. 10.",
  "부    서(부)",
  "담  당",
  "연락처",
  "교육혁신실",
  "(AI교육부)",
  "김대리 팀장",
  "(02) 1234-5678"
]
```

**Codex 가 slot mode 에서 해야 할 일:**

1. `inspect_template.py --summary` 로 슬롯 목록과 원본 텍스트를 읽는다.
2. 슬롯별로 "이 위치에는 어떤 값이 들어가야 하는가"를 주제 맥락에 맞춰 정한다. 예: 슬롯 1 의 원본이 "회계감사인 선임 제안 요청서" 라면 같은 위치에 들어갈 새 제목은 "AI 교육 혁신 사업 제안 요청서" 식으로.
3. 원본 슬롯의 줄바꿈·공백 구조는 의미를 가질 수 있으므로(두 줄 제목, 표 셀의 라벨 등) **대응되는 위치에 대응되는 성격의 텍스트**를 넣어라. 한 줄짜리 슬롯에 여러 줄을 우겨 넣으면 레이아웃이 틀어진다.
4. 바꾸고 싶지 않은 슬롯은 원본 문자열을 그대로 복사하거나, 배열을 짧게 만들어서 뒤쪽을 건드리지 않는다.

#### Targeted mode (비어있는 placeholder 셀을 채우거나 slot mode와 결합)

`content.json` 은 **딕셔너리**로, `targeted` 키에 **절대 인덱스 → 새 텍스트** 매핑을 담습니다. 절대 인덱스는 `inspect_template.py --all` 출력의 `abs[N]` 번호를 그대로 사용하세요.

단독 사용 — placeholder만 채우기:

```json
{
  "targeted": {
    "15": "Ⅰ. 행사 개요",
    "16": "1",
    "17": "Ⅱ. 제안 내용",
    "18": "2"
  }
}
```

**slot mode 와 결합** (권장 패턴 — slot 으로 본문 채우고 targeted 로 TOC placeholder 보정):

```json
{
  "slots": [
    "2026 SW마에스트로 부산센터",
    "프롬프톤 개최 제안서",
    "..."
  ],
  "targeted": {
    "15": "Ⅰ. 행사 개요",
    "17": "Ⅱ. 제안 내용"
  }
}
```

이 경우 자동감지 모드는 `slots_targeted` 가 되고, 실행 순서는 **slot → targeted** 입니다. (slot이 먼저 실행되고 나서 targeted가 덮어쓰기 때문에, 동일 노드를 양쪽에서 지정하면 targeted 가 이긴다.)

#### Blocks mode (본문 전체를 새로 짜고 싶을 때)

`content.json` 은 **블록 객체 배열**입니다. 블록은 `type` 또는 `level`, 그리고 `text` 를 갖습니다.

```json
[
  {"type": "title",   "text": "AI 교육 혁신 사업 제안 요청서"},
  {"level": "section","text": "Ⅰ. 사업 개요"},
  {"level": "h1",     "text": "□ 사업 배경 및 목적"},
  {"level": "h2",     "text": "○ 교육 현장의 AI 도입 필요성 증대"},
  {"level": "h3",     "text": "- 전국 초중고 AI 활용 수업 확산 정책"},
  {"level": "h4",     "text": "※ 2025년 AI 디지털교과서 도입 일정 참조"},
  {"type": "keep_table", "template_index": 3},
  {"level": "section","text": "Ⅱ. 요구 사항"}
]
```

레벨은 `section`, `h1`, `h2`, `h3`, `h4`, `body` 를 지원하고, 양식에서 같은 레벨의 문단 아키타입을 자동으로 찾아 복제합니다. 아키타입이 없으면 가까운 레벨로 폴백합니다.

`keep_table` 블록은 양식의 특정 표를 **그대로** 본문에 삽입합니다. `template_index` 는 inspect 출력에 표시되는 `para N` 값입니다. 표 셀 내용을 새 값으로 채우고 싶다면 **blocks mode 말고 slot mode 를** 쓰세요 — 표 재생성은 스크립트 범위 밖입니다.

### 3. 자동 채우기 실행

```bash
python3 scripts/autofill.py <template.hwpx> <content.json> <out.hwpx>
```

스크립트가 content.json 의 형태를 보고 모드를 자동 감지합니다 (문자열 배열 → slot, 객체 배열 → blocks). 출력은 양식의 `mimetype`/`META-INF`/`BinData`/`Preview`/`settings.xml`/`version.xml`/`content.hpf`/`header.xml` 을 바이트 단위로 보존하고, `Contents/section0.xml` 과 `Preview/PrvText.txt` 만 새로 씁니다.

성공하면 다음과 같이 출력됩니다:

```
[autofill] mode=slots  wrote out.hwpx
```

## Codex의 역할 (중요)

### 주제를 슬롯에 매핑하는 것은 스크립트가 아니라 Codex가 한다

스크립트는 **치환만** 합니다. "사용자의 주제가 이 양식의 어느 부분에 어떻게 들어가야 하는가"는 규칙으로 못 박을 수 없고, 양식마다 다르며, 때로는 원본이 예시용 placeholder(예: "헤드라인M 폰트_15 POINT")인지 실제 내용(예: "Ⅰ. 사업 개요")인지도 판단해야 합니다.

이 판단은 다음 순서로 하세요:

1. **inspect 결과를 전부 훑는다.** 슬롯 텍스트가 모두 placeholder 성격이면 양식이 비어 있다는 뜻이고, 실제 내용이 있으면 기존 문서를 바꿔 끼우는 것이다.
2. **원본의 의미 단위를 식별한다.** "제목 → 부제 → 날짜 → 담당자 표 → 목차 → 장 본문" 같은 큰 덩어리를 먼저 파악하고, 주제별로 어느 덩어리가 필요한지 결정한다.
3. **대응 관계를 세운다.** 예: 원본의 "2027년 회계연도" 는 해당 연도 라벨, "회계감사인 선임 제안 요청서"는 문서 제목, "2026. 2. 14."는 작성일. 주제에 맞춰 각 자리에 들어갈 값을 정한다.
4. **원본 텍스트를 보존해야 할 슬롯은 그대로 둔다.** 기호(`Ⅰ.`, `□`, `○`, `-`), 셀 라벨("담당", "연락처"), 고정 안내 문구 등은 바꾸지 마라. 사용자가 분명히 바꿔달라고 한 부분만 손댄다.
5. **길이를 체크한다.** HWPX 양식은 대부분 고정된 공간에 맞춰 레이아웃이 잡혀 있다. 원본이 한 줄 15자면 새 텍스트도 비슷한 길이로 맞추는 것이 좋다. 극단적으로 길어지면 표 셀이 밀려 페이지가 늘어난다.

### 실행 후 반드시 검증하라

autofill 이 `[autofill] mode=... wrote out.hwpx` 를 찍었다고 해서 끝이 아닙니다. 다음을 Codex 가 직접 확인하세요:

- `python3 -c "import zipfile, xml.etree.ElementTree as ET; z=zipfile.ZipFile('out.hwpx'); ET.fromstring(z.read('Contents/section0.xml'))"` 가 오류 없이 통과해야 한다. ParseError 가 나면 양식 XML 에 예상 밖의 구조가 있다는 뜻이므로, 그 양식에서는 slot mode 만 쓰고 blocks mode 는 피하라.
- 원본 양식의 표 개수와 출력물의 표 개수가 동일해야 한다 (slot mode 기준). `grep -c '<hp:tbl ' out.hwpx` 로 간접 확인 가능.
- 치환이 의도대로 됐는지 `Preview/PrvText.txt` 를 열어 맨 앞 몇 줄을 확인하라 — autofill 이 이를 새로 써 주므로 slot mode 결과가 그대로 찍혀 있다.

### 실패 시 솔직하게 보고하라

- 스크립트가 `RuntimeError` 또는 `[autofill] FAILED` 를 남기면 원인을 사용자에게 그대로 전달하라.
- 부분 실패(일부 슬롯만 반영됨) 는 slot mode 에서는 발생하지 않지만, blocks mode 에서 아키타입이 없어서 폴백되는 경우는 경고만 찍고 진행한다. 이런 경고는 사용자에게 꼭 공유해야 레이아웃 차이를 예상할 수 있다.
- "만들어졌습니다" 라고 단정하지 말고, 검증 결과("표 11개 보존 확인, XML valid, 슬롯 0~11 치환 완료") 를 함께 보고하라.

## 제약과 주의

- **암호가 걸린 HWPX** 는 지원하지 않습니다. `zipfile.BadZipFile` 로 실패합니다.
- **레거시 `.hwp` 바이너리** 는 직접 지원하지 않습니다. hwp-organizer 또는 한글 오피스에서 `.hwpx` 로 변환한 뒤 쓰세요.
- **표 셀 수/행 수 변경**, **이미지 교체**, **새 표 생성** 은 지원 범위 밖입니다. 양식에 이미 있는 표를 골라 쓰거나(`keep_table`), 표 셀의 텍스트를 slot mode 로 갈아 끼우는 방식으로 우회하세요.
- **여러 섹션 양식**: `Contents/section0.xml` 만 편집합니다. `section1.xml` 이 있는 양식은 해당 섹션이 그대로 유지되므로, 필요하면 두 번 돌리거나 현재는 지원 범위 밖임을 안내하세요.
- **수식·각주·머리말** 은 slot mode 에서는 원본 위치가 그대로 살아납니다. 각주 본문 텍스트가 슬롯에 포함되므로, 의도치 않은 치환을 피하려면 inspect 결과의 원본 텍스트를 꼼꼼히 확인하세요.

## 번들 리소스

- `scripts/_hwpx_common.py` — ZIP I/O, 섹션 XML 파서(depth-aware paragraph iterator 포함), 텍스트 치환 헬퍼
- `scripts/inspect_template.py` — 양식 검사 + JSON 리포트
- `scripts/autofill.py` — slot/blocks 모드 오케스트레이터
- `assets/(샘플양식1) 보고서 기본 양식.hwpx` — 테스트용 샘플 양식 (감사인 선임 제안 요청서)
- `assets/(샘플양식2) 보고서 기반 양식(요약).hwpx` — 테스트용 요약 양식
