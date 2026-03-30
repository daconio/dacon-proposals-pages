# Design System: The Editorial Architect

슬라이드 모드에서 HTML 프레젠테이션 생성 시 반드시 따라야 하는 디자인 시스템.

---

## 1. Creative North Star: "The Digital Curator"

**핵심 원칙**: 해커톤 플랫폼의 인터페이스는 참가자의 혁신과 경쟁하지 않는다. **갤러리급 무대**를 제공한다.

- **Editorial Precision** — "boxed-in" SaaS 대시보드 레이아웃 거부
- **의도적 비대칭(Intentional Asymmetry)**, 스태거드 콘텐츠 블록, 대형 타이포그래피 위계
- 모든 화면을 **하이엔드 건축 저널**처럼 취급 — 엘리트 크래프트를 위한 공간

---

## 2. Colors: Tonal Depth & The "No-Line" Rule

### Color Strategy
- **Primary (`#0053db`)**: 시그니처 블루. 고임팩트 CTA와 "Success" 상태에만 절제하여 사용.
- **Neutral Foundation**: `surface` (#f7f9fb) + `surface_container_lowest` (#ffffff)로 무한한 공간감 창출.
- **3-Color System**: Blue + Slate + White. 추가 색상(green/yellow 등) 사용 최소화.

### Color Tokens

| Token | Value | Use |
|-------|-------|-----|
| `primary` | #0053db | 시그니처 블루, CTA 전용 |
| `primary_dim` | #0048c1 | 그라디언트 페어 |
| `on_primary` | #f8f7ff | primary 위 텍스트 |
| `on_background` | #2a3439 | 메인 텍스트 (**#000000 순검정 금지**) |
| `surface` | #f7f9fb | 페이지 기본 배경 |
| `surface_bright` | #f7f9fb | 네비게이션/모달 (Glass용) |
| `surface_container_lowest` | #ffffff | 인터랙티브 카드 |
| `surface_container_low` | #f0f4f7 | 보조 콘텐츠 영역, 사이드바 |
| `on_surface` | #2a3439 | 본문 텍스트 |
| `on_surface_variant` | #566166 | 보조 메타데이터 |
| `outline_variant` | #a9b4b9 | Ghost Border용 |
| `secondary_container` | #d8e3fb | 칩/태그 배경 |
| `on_secondary_container` | #475266 | 칩/태그 텍스트 |
| `on_primary_fixed_variant` | #0050d4 | 카운트다운 "active" 글로우 |

### "No-Line" 규칙 (필수)

**표준 1px 보더로 영역 구분 절대 금지.** 대신:
1. **배경색 전환(Background Color Shifts)**: 사이드바는 `surface_container_low`, 메인 콘텐츠는 `surface`. 톤 변화로 경계 인식.
2. **톤 전환**: neutral scale의 미묘한 value 차이로 분리 암시.
3. **네거티브 스페이스**: Spacing Scale로 보이지 않는 구분자 역할.

### Surface Hierarchy & Nesting

UI를 겹겹이 쌓인 고급 종이처럼 취급:
- **Base Level**: `surface` (#f7f9fb)
- **Secondary Content**: `surface_container_low` (#f0f4f7)
- **Interactive Cards**: `surface_container_lowest` (#ffffff)
- **Navigation/Modals**: `surface_bright` (#f7f9fb) + Glassmorphism

### Glass & Gradient Rule — "Signature Texture"

- **Hero CTA**: `primary` (#0053db) → `primary_dim` (#0048c1) 135도 리니어 그라디언트
- **Floating Navigation**: `surface_bright` 80% 불투명도 + `24px` backdrop blur — "frosted glass" 효과

---

## 3. Typography: The Plus Jakarta Scale

**Plus Jakarta Sans** 단일 서체. 기하학적 명료함 = "Professional & Clean". 열린 aperture = 소형 스케일 가독성.

### Type Scale

| Token | Size | Weight | Letter Spacing | Use |
|-------|------|--------|---------------|-----|
| `display-lg` | 3.5rem | 800 | -0.02em | 히어로 헤더 |
| `display-md` | 2.75rem | 800 | -0.02em | 서브 히어로 |
| `display-sm` | 2rem | 700 | -0.01em | 카운트다운 숫자 |
| `headline-lg` | 2rem | 700 | -0.01em | 섹션 헤딩 |
| `headline-md` | 1.75rem | 700 | -0.01em | 서브 섹션 |
| `title-lg` | 1.375rem | 600 | 0 | 카드 제목 |
| `title-md` | 1rem | 600 | 0 | 리스트 제목 |
| `body-lg` | 1rem | 400 | 0 | 본문 (워크호스) |
| `body-md` | 0.875rem | 400 | 0 | 설명 텍스트 |
| `body-sm` | 0.75rem | 400 | 0 | 보조 메타데이터 (`on_surface_variant`) |
| `label-lg` | 0.875rem | 600 | 0 | 큰 라벨 |
| `label-md` | 0.75rem | 600 | 0 | 기능 라벨 (Medium/Semi-Bold 필수) |
| `label-sm` | 0.6875rem | 600 | 0 | 캡션, 카운트다운 단위 |

---

## 4. Spacing Scale

| Token | Value | Use |
|-------|-------|-----|
| `spacing-1` | 0.25rem (4px) | 인라인 아이콘 갭 |
| `spacing-2` | 0.5rem (8px) | 칩 내부 패딩 |
| `spacing-3` | 1rem (16px) | 카드 내부 섹션 분리 (디바이더 대체) |
| `spacing-4` | 1.4rem (22px) | 카드 내 header/body/footer 분리 |
| `spacing-6` | 1.5rem (24px) | 섹션 간 기본 |
| `spacing-8` | 2rem (32px) | 컴포넌트 그룹 간격 |
| `spacing-12` | 3rem (48px) | 주요 섹션 간격 |
| `spacing-16` | 5.5rem (88px) | 비대칭 좌측 패딩 |
| `spacing-20` | 7rem (112px) | 비대칭 우측 패딩 |
| `spacing-24` | 6rem (96px) | 히어로 여백 |

---

## 5. Corner Radius

| Token | Value | Use |
|-------|-------|-----|
| `radius-sm` | 0.25rem (4px) | 작은 요소 |
| `radius-md` | 0.375rem (6px) | 버튼, 입력 필드 |
| `radius-lg` | 0.75rem (12px) | 카드 컨테이너 |
| `radius-xl` | 1rem (16px) | 모달, 바텀시트 |
| `radius-full` | 9999px | 칩, 아바타, 원형 뱃지 |

---

## 6. Elevation & Depth: Tonal Layering

**"Drop shadow"는 구시대적이고 무겁다.** Layering Principle 사용.

### Tonal Lift
`surface_container_lowest` 카드가 `surface_container_low` 위에 앉으면 건축적(architectural) 리프트 생성.

### Ambient Shadows (플로팅 요소에만)
- **규격**: `y-8, blur-24`
- **Color**: surface 틴티드 — `rgba(30, 41, 59, 0.04)` (**순검정 금지**)

### Ghost Border (접근성 대체)
`outline_variant` (#a9b4b9) **20% 불투명도** — 흰 배경 위 컨테이너 정의용

---

## 7. Components: Precision Primitives

### Buttons
| Variant | Background | Text | Border | Radius |
|---------|-----------|------|--------|--------|
| Primary | `primary` (#0053db) | `on_primary` (#f8f7ff) | 없음 | `md` (0.375rem) |
| Ghost | 없음 | `primary` | 없음 (hover: `outline_variant` 10%) | `md` |

### Cards (Hackathon Entry)
- **배경**: `surface_container_lowest` (#ffffff)
- **디바이더 금지**: `spacing-3` (1rem) 또는 `spacing-4` (1.4rem)으로 header/body/footer 분리
- **그림자**: Tonal Lift만 (Ambient Shadow 선택적)

### Input Fields
- **배경**: `surface_container_low`
- **Border**: 없음. Focus 시에만 `2px` 하단 보더 (`primary`)
- **Label**: `label-md`, 입력 필드 0.5rem 상단에 위치

### Chips (Project Tags)
- **배경**: `secondary_container` (#d8e3fb)
- **텍스트**: `on_secondary_container` (#475266)
- **Radius**: `full` (9999px) — 소프트 필 형태

### Countdown Timers
- **숫자**: `display-sm`
- **단위** (Days, Hours, Mins): `label-sm`
- **텍스트 색**: `on_primary_fixed_variant` (#0050d4) — "active" 글로우

---

## 8. Do's and Don'ts

### DO
- **비대칭 패딩 사용**: 대형 데스크톱에서 좌 `spacing-16` (5.5rem) / 우 `spacing-20` (7rem) — 에디토리얼 오프센터 리듬
- **"Dead Space" 수용**: 콘텐츠가 적은 섹션은 늘리지 말고 중앙 정렬 + `surface` 여백으로 시선 집중
- **미묘한 트랜지션**: 모든 hover 상태에 `200ms ease-out` transition (background-color/opacity)
- **라인 대신 간격으로 분리**: 리스트 아이템 구분이 필요하면 `spacing-4` (1.4rem) 사용

### DON'T
- **#000000 순검정 절대 금지**: `on_background` (#2a3439)로 대체 — 프리미엄하되 거칠지 않게
- **디바이더/수평선 금지**: 줄 긋고 싶으면 spacing을 `spacing-4`로 늘리기
- **과도한 색상 금지**: 3-Color 시스템 (Blue + Slate + White). 안전 관련 필수 상황 외 green/yellow 추가 지양
- **100% 불투명 검정 그림자 금지**: Ambient shadow만 (`rgba(30, 41, 59, 0.04)`)

---

## 9. 슬라이드 적용 가이드

슬라이드 HTML 생성 시 이 디자인 시스템을 다음과 같이 적용:

### CSS 변수 정의
```css
:root {
  --primary: #0053db;
  --primary-dim: #0048c1;
  --on-primary: #f8f7ff;
  --on-background: #2a3439;
  --surface: #f7f9fb;
  --surface-bright: #f7f9fb;
  --surface-container-lowest: #ffffff;
  --surface-container-low: #f0f4f7;
  --on-surface: #2a3439;
  --on-surface-variant: #566166;
  --outline-variant: #a9b4b9;
  --secondary-container: #d8e3fb;
  --on-secondary-container: #475266;
  --on-primary-fixed-variant: #0050d4;

  --font-display: 'Plus Jakarta Sans', -apple-system, sans-serif;
  --shadow-ambient: 0 8px 24px rgba(30, 41, 59, 0.04);
  --ghost-border: 1px solid rgba(169, 180, 185, 0.2);
}
```

### Font 로딩
```html
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
```

### 슬라이드 배경 계층
- 슬라이드 배경: `surface` (#f7f9fb)
- 카드/박스: `surface-container-lowest` (#ffffff) on `surface-container-low` (#f0f4f7)
- 강조 영역: `secondary-container` (#d8e3fb)
- 영역 분리: 배경색 전환으로만 (보더 금지)

### 타이포그래피 매핑
- 슬라이드 제목: `display-md` (2.75rem, 800, -0.02em)
- 섹션 제목: `headline-lg` (2rem, 700, -0.01em)
- 카드 제목: `title-lg` (1.375rem, 600)
- 본문: `body-md` (0.875rem, 400)
- 라벨/칩: `label-md` (0.75rem, 600)

### 그림자 & 보더 규칙
```css
/* Ambient Shadow — 플로팅 요소에만 */
.floating-element {
  box-shadow: 0 8px 24px rgba(30, 41, 59, 0.04);
}

/* Ghost Border — 흰 배경 위 컨테이너 정의용에만 */
.ghost-border {
  border: 1px solid rgba(169, 180, 185, 0.2);
}

/* Hero CTA Gradient — Signature Texture */
.hero-cta {
  background: linear-gradient(135deg, #0053db, #0048c1);
}

/* Glassmorphism — Floating Navigation */
.glass-nav {
  background: rgba(247, 249, 251, 0.8);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
}
```
