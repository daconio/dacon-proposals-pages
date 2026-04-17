# 슬라이드 프레젠테이션 구현 가이드

순수 HTML/CSS/JavaScript만으로 웹 슬라이드를 생성하는 상세 구현 가이드.
외부 라이브러리 없이 단일 HTML 파일로 동작한다.

> **디자인 시스템**: `references/design-system.md` 참조 (The Editorial Architect)
> 슬라이드 생성 시 반드시 디자인 시스템의 색상, 타이포그래피, No-Line 규칙, 컴포넌트 가이드를 따른다.

---

## 0. 디자인 시스템 필수 적용 사항

슬라이드 HTML 생성 시 다음을 반드시 준수한다:

1. **Color**: 3-Color 시스템 — Primary(`#0053db`) + Slate(`#2a3439`) + White(`#ffffff`). 과도한 색상 추가 지양.
2. **Font**: `Plus Jakarta Sans` 단일 서체. Display는 -0.02em letter-spacing.
3. **No-Line**: 1px 보더 영역 구분 금지 → 배경색 톤 전환(surface hierarchy)으로 분리
4. **Surface 계층**: surface(#f7f9fb) → surface_container_low(#f0f4f7) → surface_container_lowest(#ffffff) 레이어 네스팅
5. **#000000 금지**: 텍스트는 `on_background`(#2a3439), 그림자는 `rgba(30,41,59,0.04)` Ambient만
6. **Glass**: Hero CTA에 `primary → primary_dim` 135도 그라디언트. 플로팅 네비에 80% 불투명 + `24px` blur
7. **비대칭 패딩**: 에디토리얼 오프센터 리듬 — 좌 5.5rem / 우 7rem (대형 뷰)

상세 토큰, 컴포넌트 스펙은 `references/design-system.md` 참조.

---

## 1. 슬라이드 레이아웃 & DOM 구조

### HTML 기본 구조

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>프레젠테이션 제목</title>
  <style>/* 인라인 CSS */</style>
</head>
<body>
  <div class="presentation" role="application" aria-roledescription="프레젠테이션">
    <div class="slides">
      <section class="slide active" aria-roledescription="슬라이드" aria-label="1/N">
        <div class="slide-content">
          <h1>제목 슬라이드</h1>
          <p class="subtitle">부제목</p>
        </div>
        <aside class="notes">발표자 노트</aside>
      </section>
      <!-- 추가 슬라이드 -->
    </div>

    <div class="controls">
      <button class="prev" aria-label="이전 슬라이드">‹</button>
      <span class="progress-text">1 / N</span>
      <button class="next" aria-label="다음 슬라이드">›</button>
    </div>
    <div class="progress-bar"></div>
  </div>
  <script>/* 인라인 JS */</script>
</body>
</html>
```

### CSS 레이아웃 (16:9 비율 고정, 1280x720)

> **필수**: 슬라이드 뷰포트는 반드시 `1280px x 720px` (16:9)로 고정한다.

```css
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --slide-w: 1280px;
  --slide-h: 720px;
}

html, body {
  width: 100%; height: 100%;
  overflow: hidden;
  font-family: var(--font);
  background: #e2e8f0;
}

#viewport {
  position: fixed; inset: 0;
  display: flex; align-items: center; justify-content: center;
}

#stage {
  position: relative;
  width: var(--slide-w); height: var(--slide-h);
  overflow: hidden; transform-origin: center;
  border-radius: 0.75rem;
  box-shadow: 0 12px 48px rgba(30,41,59,0.15);
  background: #fff;
}

.slide {
  position: absolute; inset: 0;
  background: #fff;
  display: flex; flex-direction: column;
  opacity: 0; pointer-events: none;
  transition: opacity 0s; overflow: hidden;
}
.slide.active { opacity: 1; pointer-events: auto; }

/* 슬라이드 내부 영역: 헤더(.sh) + 콘텐츠(.si) + 푸터(.sf) */
.sh {
  position: absolute; top: 0; left: 0; right: 0;
  height: 44px; padding: 0 32px;
  display: flex; justify-content: space-between; align-items: center;
  z-index: 2;
}
.si {
  flex: 1; display: flex; flex-direction: column;
  padding: 62px 72px 48px;
}
/* 푸터: 페이지 번호만 중앙 정렬 */
.sf {
  position: absolute; bottom: 0; left: 0; right: 0;
  height: 36px; padding: 0 32px;
  display: flex; justify-content: center; align-items: center;
  z-index: 2;
}
.sf .pg {
  font-size: 0.6875rem; font-weight: 600;
  font-family: 'SF Mono', Menlo, monospace;
}
/* 브랜드/섹션명은 숨기고 페이지 번호만 표시 */
.sf .brand { display: none; }
.sf span:last-child { display: none; }
```

### 뷰포트 스케일링 JS (필수)

```javascript
function fit() {
  const s = Math.min(window.innerWidth / 1280, window.innerHeight / 720);
  document.getElementById('stage').style.transform = 'scale(' + s + ')';
}
window.addEventListener('resize', fit);
fit();
```

### 반응형 스케일링

```css
/* 슬라이드 콘텐츠가 뷰포트에 맞게 자동 스케일 */
@media (max-width: 768px) {
  .slide-content { padding: 1rem 1.5rem; }
  .slide-content h1 { font-size: 1.8rem; }
  .slide-content h2 { font-size: 1.4rem; }
}

@media (max-width: 480px) {
  .slide-content h1 { font-size: 1.4rem; }
  .controls { display: none; } /* 모바일에서는 스와이프 사용 */
}
```

### 슬라이드 레이아웃 변형

```css
/* 타이틀 슬라이드 */
.slide--title .slide-content { text-align: center; }

/* 2단 레이아웃 */
.slide--split .slide-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  align-items: center;
}

/* 이미지 전체 배경 */
.slide--image {
  background-size: cover;
  background-position: center;
}
.slide--image .slide-content {
  background: rgba(0,0,0,0.6);
  border-radius: 1rem;
  color: white;
}

/* 코드 슬라이드 */
.slide--code .slide-content { max-width: 1000px; }
.slide--code pre {
  background: #1e293b;
  border-radius: 0.75rem;
  padding: 1.5rem;
  overflow-x: auto;
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
  font-size: 0.95rem;
  line-height: 1.6;
}
```

---

## 2. 키보드 & 마우스 네비게이션

### 네비게이션 엔진

```javascript
class SlideEngine {
  constructor() {
    this.slides = [...document.querySelectorAll('.slide')];
    this.current = 0;
    this.total = this.slides.length;
    this.isAnimating = false;
    this.progressBar = document.querySelector('.progress-bar');
    this.progressText = document.querySelector('.progress-text');

    this.bindKeyboard();
    this.bindTouch();
    this.bindControls();
    this.restoreFromHash();
    this.updateUI();
  }

  goto(index) {
    if (this.isAnimating || index < 0 || index >= this.total || index === this.current) return;

    // Fragment 체크: 현재 슬라이드에 미표시 fragment가 있으면 먼저 처리
    if (index > this.current) {
      const fragments = this.slides[this.current].querySelectorAll('.fragment:not(.visible)');
      if (fragments.length > 0) {
        fragments[0].classList.add('visible');
        return;
      }
    }

    this.isAnimating = true;
    const direction = index > this.current ? 1 : -1;

    // 이전 슬라이드 퇴장
    const prev = this.slides[this.current];
    prev.style.transform = `translateX(${-direction * 100}%)`;
    prev.classList.remove('active');

    // 다음 슬라이드 입장
    const next = this.slides[index];
    next.style.transform = `translateX(${direction * 100}%)`;
    next.classList.add('active');

    // 강제 리플로우 후 애니메이션
    next.offsetHeight;
    next.style.transform = 'translateX(0)';

    // Fragment 초기화 (뒤로 갈 때)
    if (direction < 0) {
      next.querySelectorAll('.fragment').forEach(f => f.classList.remove('visible'));
    }

    setTimeout(() => {
      prev.style.transform = '';
      this.current = index;
      this.isAnimating = false;
      this.updateUI();
    }, 500);
  }

  next() { this.goto(this.current + 1); }
  prev() {
    // 뒤로 갈 때 현재 슬라이드의 visible fragment를 하나씩 제거
    const visibleFragments = this.slides[this.current].querySelectorAll('.fragment.visible');
    if (visibleFragments.length > 0) {
      visibleFragments[visibleFragments.length - 1].classList.remove('visible');
      return;
    }
    this.goto(this.current - 1);
  }

  updateUI() {
    // 프로그레스 바
    const progress = ((this.current + 1) / this.total) * 100;
    if (this.progressBar) this.progressBar.style.width = `${progress}%`;
    if (this.progressText) this.progressText.textContent = `${this.current + 1} / ${this.total}`;

    // ARIA
    this.slides.forEach((s, i) => {
      s.setAttribute('aria-hidden', i !== this.current);
      s.setAttribute('aria-label', `슬라이드 ${i + 1}/${this.total}`);
    });

    // URL 해시
    history.replaceState(null, '', `#slide-${this.current + 1}`);
  }

  restoreFromHash() {
    const match = location.hash.match(/#slide-(\d+)/);
    if (match) {
      const idx = parseInt(match[1]) - 1;
      if (idx >= 0 && idx < this.total) {
        this.slides[this.current].classList.remove('active');
        this.current = idx;
        this.slides[idx].classList.add('active');
      }
    }
  }
}
```

### 키보드 바인딩

```javascript
bindKeyboard() {
  document.addEventListener('keydown', (e) => {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

    switch(e.key) {
      case 'ArrowRight': case 'ArrowDown': case ' ': case 'PageDown': case 'Enter':
        e.preventDefault(); this.next(); break;
      case 'ArrowLeft': case 'ArrowUp': case 'PageUp': case 'Backspace':
        e.preventDefault(); this.prev(); break;
      case 'Home':
        e.preventDefault(); this.goto(0); break;
      case 'End':
        e.preventDefault(); this.goto(this.total - 1); break;
      case 'f': case 'F':
        e.preventDefault(); this.toggleFullscreen(); break;
      case 'Escape':
        if (document.fullscreenElement) document.exitFullscreen();
        break;
      case 'o': case 'O':
        e.preventDefault(); this.toggleOverview(); break;
      case 's': case 'S':
        e.preventDefault(); this.openSpeakerView(); break;
    }
  });
}
```

### 터치/스와이프 지원

```javascript
bindTouch() {
  let startX, startY, startTime;
  const THRESHOLD = 50;
  const RESTRAINT = 100;
  const TIME_LIMIT = 300;

  const container = document.querySelector('.presentation');

  container.addEventListener('touchstart', (e) => {
    startX = e.changedTouches[0].pageX;
    startY = e.changedTouches[0].pageY;
    startTime = Date.now();
  }, { passive: true });

  container.addEventListener('touchend', (e) => {
    const dx = e.changedTouches[0].pageX - startX;
    const dy = e.changedTouches[0].pageY - startY;
    const dt = Date.now() - startTime;

    if (dt <= TIME_LIMIT && Math.abs(dx) >= THRESHOLD && Math.abs(dy) <= RESTRAINT) {
      dx < 0 ? this.next() : this.prev();
    }
  }, { passive: true });
}
```

### 컨트롤 버튼 바인딩

```javascript
bindControls() {
  document.querySelector('.prev')?.addEventListener('click', () => this.prev());
  document.querySelector('.next')?.addEventListener('click', () => this.next());
}
```

### 프로그레스 바 CSS

```css
.progress-bar {
  position: fixed;
  bottom: 0; left: 0;
  height: 4px;
  background: linear-gradient(90deg, #3b82f6, #8b5cf6);
  transition: width 0.3s ease;
  z-index: 100;
}

.controls {
  position: fixed;
  bottom: 1.5rem;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 1rem;
  z-index: 90;
  opacity: 0;
  transition: opacity 0.3s;
}
.presentation:hover .controls { opacity: 1; }
```

---

## 3. 슬라이드 전환 애니메이션

### 전환 효과 모음

```css
/* Fade */
.transition-fade .slide { transition: opacity 0.5s ease; }
.transition-fade .slide.active { opacity: 1; }

/* Slide (기본) */
.transition-slide .slide {
  transition: transform 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94), opacity 0.5s;
}

/* Zoom */
.transition-zoom .slide {
  transition: transform 0.6s ease, opacity 0.6s;
  transform: scale(0.8);
}
.transition-zoom .slide.active { transform: scale(1); opacity: 1; }

/* Flip */
.transition-flip {
  perspective: 1200px;
}
.transition-flip .slide {
  backface-visibility: hidden;
  transition: transform 0.8s;
}

/* Cover (겹침) */
.transition-cover .slide {
  transition: transform 0.5s ease;
  z-index: 0;
}
.transition-cover .slide.active { z-index: 1; }
```

### GPU 가속 최적화

```css
.slide {
  /* GPU 레이어 생성 */
  transform: translateZ(0);
  /* 전환 직전에만 will-change 적용 */
}

.slide.animating {
  will-change: transform, opacity;
}
```

### 이벤트 잠금 (애니메이션 중 입력 차단)

엔진의 `isAnimating` 플래그로 처리. `goto()` 시작 시 `true`, `setTimeout` 콜백에서 `false`.

---

## 4. 콘텐츠 빌드 효과 (Fragment)

### Fragment HTML 마크업

```html
<section class="slide">
  <h2>단계별 등장</h2>
  <ul>
    <li class="fragment" data-step="1">첫 번째 포인트</li>
    <li class="fragment" data-step="2">두 번째 포인트</li>
    <li class="fragment" data-step="3">세 번째 포인트</li>
  </ul>
</section>
```

### Fragment CSS

```css
.fragment {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.4s ease, transform 0.4s ease;
}

.fragment.visible {
  opacity: 1;
  transform: translateY(0);
}

/* 변형: 페이드만 */
.fragment.fade-in { transform: none; }

/* 변형: 왼쪽에서 등장 */
.fragment.slide-in { transform: translateX(-30px); }
.fragment.slide-in.visible { transform: translateX(0); }

/* 변형: 확대 등장 */
.fragment.zoom-in { transform: scale(0.5); }
.fragment.zoom-in.visible { transform: scale(1); }

/* 변형: 강조 (이미 보이지만 색상 변경) */
.fragment.highlight {
  opacity: 1; transform: none;
  transition: color 0.3s, background-color 0.3s;
}
.fragment.highlight.visible {
  color: #fbbf24;
  background: rgba(251, 191, 36, 0.1);
}
```

### 코드 블록 줄 강조

```css
.code-highlight {
  position: relative;
}

.code-highlight .line {
  display: block;
  padding: 0 1rem;
  transition: opacity 0.3s, background-color 0.3s;
}

.code-highlight.has-focus .line { opacity: 0.3; }
.code-highlight.has-focus .line.focus {
  opacity: 1;
  background: rgba(59, 130, 246, 0.15);
  border-left: 3px solid #3b82f6;
}
```

### 발표자 노트

```css
.notes {
  display: none; /* 기본: 숨김 */
}

/* 발표자 뷰에서만 표시 */
@media (display-mode: standalone) {
  .notes { display: block; }
}
```

```javascript
openSpeakerView() {
  const win = window.open('', 'speaker', 'width=900,height=700');
  const channel = new BroadcastChannel('slide-sync');

  // 메인 → 발표자 뷰 동기화
  const updateSpeaker = () => {
    const notes = this.slides[this.current].querySelector('.notes')?.innerHTML || '';
    const nextTitle = this.slides[this.current + 1]?.querySelector('h1,h2')?.textContent || '마지막 슬라이드';
    channel.postMessage({
      type: 'update',
      current: this.current + 1,
      total: this.total,
      notes,
      nextTitle
    });
  };

  // 슬라이드 변경 시 자동 업데이트
  const originalGoto = this.goto.bind(this);
  this.goto = (idx) => { originalGoto(idx); setTimeout(updateSpeaker, 100); };
  updateSpeaker();
}
```

---

## 5. 풀스크린 & 오버뷰

### 풀스크린

```javascript
toggleFullscreen() {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen?.()
      || document.documentElement.webkitRequestFullscreen?.();
  } else {
    document.exitFullscreen?.() || document.webkitExitFullscreen?.();
  }
}
```

### 슬라이드 오버뷰 (O 키)

```css
.presentation.overview .slides {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
  padding: 2rem;
  overflow-y: auto;
  height: 100vh;
}

.presentation.overview .slide {
  position: relative;
  opacity: 1;
  transform: scale(0.9);
  cursor: pointer;
  border: 2px solid transparent;
  border-radius: 8px;
  aspect-ratio: 16/9;
  pointer-events: auto;
}

.presentation.overview .slide.active {
  border-color: #3b82f6;
}

.presentation.overview .controls,
.presentation.overview .progress-bar { display: none; }
```

---

## 6. 테마 시스템 (The Editorial Architect)

> **주의**: 아래 테마 토큰은 `references/design-system.md`의 디자인 시스템에 기반한다.
> **The Digital Curator** 라이트 테마를 기본으로 사용한다. 3-Color 시스템 (Blue + Slate + White).

```css
/* CSS 변수 기반 테마 — The Editorial Architect */
:root {
  /* Core Brand — 3-Color System */
  --primary: #0053db;
  --primary-dim: #0048c1;
  --on-primary: #f8f7ff;
  --on-background: #2a3439; /* #000000 순검정 절대 금지 */

  /* Surface Hierarchy — Tonal Layering */
  --surface: #f7f9fb;
  --surface-bright: #f7f9fb;
  --surface-container-lowest: #ffffff;
  --surface-container-low: #f0f4f7;
  --on-surface: #2a3439;
  --on-surface-variant: #566166;

  /* Outline */
  --outline-variant: #a9b4b9;

  /* Secondary (칩/태그 전용) */
  --secondary-container: #d8e3fb;
  --on-secondary-container: #475266;

  /* Active Glow */
  --on-primary-fixed-variant: #0050d4;

  /* Typography — Plus Jakarta Sans 단일 서체 */
  --font-display: 'Plus Jakarta Sans', -apple-system, sans-serif;

  /* Shadows — Ambient only, 순검정 금지 */
  --shadow-ambient: 0 8px 24px rgba(30, 41, 59, 0.04);
  --ghost-border: 1px solid rgba(169, 180, 185, 0.2);

  /* Corner Radius */
  --radius-sm: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.75rem;
  --radius-xl: 1rem;
  --radius-full: 9999px;
}

/* 적용 */
.slide {
  background: var(--surface);
  color: var(--on-surface);
  font-family: var(--font-display);
}
.slide h1, .slide h2, .slide h3 {
  color: var(--on-surface);
  font-family: var(--font-display);
  letter-spacing: -0.02em;
}
```

### No-Line 규칙 적용

```css
/* 금지: border: 1px solid ... 으로 영역 구분 */

/* 대신: Tonal Lift — 배경색 전환 */
.card { background: var(--surface-container-lowest); } /* #ffffff on #f0f4f7 */
.card-accent { background: var(--secondary-container); } /* #d8e3fb */

/* 대신: Ghost Border (흰 배경 위 컨테이너 정의용에만) */
.card-ghost { border: var(--ghost-border); } /* outline_variant 20% */

/* 대신: Ambient Shadow (플로팅 요소에만) */
.card-float { box-shadow: var(--shadow-ambient); } /* rgba(30,41,59,0.04) */

/* 디바이더 대신 spacing */
.list-item + .list-item { margin-top: 1.4rem; } /* spacing-4 */
```

### Glass & Gradient — Signature Texture

```css
/* Hero CTA — primary → primary_dim 135도 */
.hero-cta {
  background: linear-gradient(135deg, var(--primary), var(--primary-dim));
  color: var(--on-primary);
}

/* Glassmorphism — Floating Navigation */
.glass-nav {
  background: rgba(247, 249, 251, 0.8); /* surface_bright at 80% */
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
}
```

---

## 7. 인쇄 지원 (16:9 PDF)

> **필수**: `@page` 크기는 반드시 16:9 (338.667mm x 190.5mm)으로 설정한다.
> `.slide`는 `width:100%; height:100vh`로 페이지를 채운다.
> `.sf`(푸터)는 `position:static` flex 아이템으로 변환하여 잘림을 방지한다.

```css
@page { size: 338.667mm 190.5mm; margin: 0 !important; }
@media print {
  * { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
  html, body { background: #fff; overflow: visible !important; height: auto !important; width: 100% !important; margin: 0 !important; padding: 0 !important; }
  #viewport { position: static !important; display: block !important; width: 100% !important; height: auto !important; }
  #stage { position: static !important; width: 100% !important; height: auto !important; overflow: visible !important; transform: none !important; box-shadow: none !important; border-radius: 0 !important; }

  .slide {
    position: relative !important; inset: auto !important;
    opacity: 1 !important; pointer-events: auto !important;
    width: 100% !important; height: 100vh !important;
    page-break-after: always !important; break-after: page !important;
    margin: 0 !important; padding: 0 !important;
    overflow: hidden !important;
    display: flex !important; flex-direction: column !important;
  }
  .slide:last-child { page-break-after: auto !important; }

  /* 헤더/푸터를 flex 아이템으로 변환하여 잘림 방지 */
  .sh { position: static !important; flex-shrink: 0 !important; height: 44px !important; display: flex !important; width: 100% !important; order: -1 !important; }
  .si { flex: 1 !important; overflow: hidden !important; }
  .sf { position: static !important; flex-shrink: 0 !important; height: 36px !important; display: flex !important; justify-content: center !important; align-items: center !important; width: 100% !important; order: 99 !important; }

  .nav-btn, #progress-bar, #key-hint { display: none !important; }
  [data-step] { opacity: 1 !important; transform: none !important; }
}
```

---

## 7-A. HTML 슬라이드 → PDF 변환 (실전 노하우)

슬라이드 HTML을 PDF로 안정적으로 변환하려면 **반드시 `scripts/html_to_pdf.py` 패턴**을 사용한다.
이 절은 실제 디버깅으로 확정된 함정과 해결책을 정리한다.

### ⚠️ 함정: Chrome `page.pdf()` 사용 금지

**증상**: Playwright `page.pdf()` 또는 Chrome `--print-to-pdf` 사용 시
첫 페이지와 마지막 페이지만 정상이고 중간 페이지(2~N-1)는 헤더만 보이고 본문이 비어 있음.

**근본 원인**:
1. `page.pdf()`는 Chrome 내부적으로 print 미디어를 강제 활성화
2. 슬라이드 덱 HTML의 `@media print { .slide { display:flex !important; opacity:1 !important } }` 규칙이 발동
3. inline `style="display:none !important"`로 다른 슬라이드를 숨겨도 stylesheet `!important`가 동등 우선순위로 충돌
4. 결국 모든 슬라이드가 동시에 `display:flex`로 펼쳐져 전체 문서가 N×720px 길이로 렌더
5. PDF 페이지 크기가 720px라서 첫 720px(슬라이드 0)만 캡처되고 나머지 슬라이드는 헤더(.sh, top:0 위치)만 잡힘

> 첫 슬라이드는 `.active` 클래스 + 초기화 JS의 `pre-visible` 클래스 덕분에 data-step 콘텐츠가 정상 노출되어 PDF 1페이지에 잡힘. 마지막 슬라이드(.slide-end)는 `.si`의 `justify-content:center` 등 특수 레이아웃 때문에 일부 콘텐츠가 캡처되어 사용자 눈에 "첫 페이지와 마지막만 정상"으로 보임.

### ⚠️ 추가 함정: 화면 도움말이 PDF에 노출됨

스크린 미디어로 캡처하기 때문에 `@media print { #key-hint, .nav-btn { display:none } }`
규칙이 발동하지 않는다. "Arrow keys or click to navigate" 같은 안내 텍스트와
좌우 네비게이션 버튼이 캡처에 그대로 들어간다.

**해결**: 스크린샷 직전에 `add_style_tag`로 해당 요소들을 강제로 숨긴다.

```python
page.add_style_tag(content="""
    #key-hint, .nav-btn, #nav-prev, #nav-next, #progress-bar,
    .controls, .presenter-notes, .speaker-notes {
        display: none !important;
        visibility: hidden !important;
    }
""")
```

### ✅ 해결: `page.screenshot()` (스크린 미디어) + reportlab 조립

> **핵심**: `page.pdf()`가 아닌 슬라이드별 스크린샷 → reportlab PDF 합성.
> 브라우저에서 보이는 그대로 캡처하므로 footer 잘림, 레이아웃 깨짐 없음.
> `device_scale_factor=2`로 Figma 임포트 시에도 선명한 해상도 확보.

```python
# scripts/html2pdf.py 참조
import asyncio, os
from playwright.async_api import async_playwright
from reportlab.pdfgen import canvas

PAGE_W, PAGE_H = 960.0, 540.0  # 16:9 in points

async def convert(html_path):
    pdf_path = html_path.rsplit('.html', 1)[0] + '.pdf'
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(
            viewport={'width': 1280, 'height': 720},
            device_scale_factor=2  # 2x retina for Figma
        )
        await page.goto(f'file://{os.path.abspath(html_path)}', wait_until='networkidle')
        await page.wait_for_timeout(2000)

        n = await page.evaluate('document.querySelectorAll(".slide").length')
        imgs = []
        for i in range(n):
            await page.evaluate(f'''() => {{
                const slides = document.querySelectorAll(".slide");
                slides.forEach((s, idx) => s.classList.toggle("active", idx === {i}));
                slides[{i}].querySelectorAll("[data-step]").forEach(el => {{
                    el.style.opacity = "1"; el.style.transform = "none";
                }});
                document.querySelectorAll(".nav-btn, #progress-bar, #key-hint")
                    .forEach(x => x.style.display = "none");
            }}''')
            await page.wait_for_timeout(150)
            img = f'/tmp/_pdf_{i:03d}.png'
            await page.screenshot(path=img, full_page=False)
            imgs.append(img)
        await browser.close()

        c = canvas.Canvas(pdf_path, pagesize=(PAGE_W, PAGE_H))
        for idx, img in enumerate(imgs):
            if idx > 0: c.showPage()
            c.drawImage(img, 0, 0, width=PAGE_W, height=PAGE_H)
        c.save()
        for img in imgs: os.remove(img)
```

### 검증 체크리스트

PDF 변환 직후 반드시 다음을 확인한다:

1. **페이지 수 일치**: 슬라이드 N개 → PDF N페이지 (`PyPDF2` `len(reader.pages)`)
2. **페이지 크기 균일**: 모든 페이지 MediaBox가 동일 (예: `(960, 540)` for 16:9)
3. **이미지 해시 고유성**: 각 페이지의 임베드 이미지 md5가 모두 다름 (slide 0 복제 방지)
4. **시각 통계**: Pillow `ImageStat`로 각 페이지 mean/stddev 계산 → 모두 0(전백)이 아님
5. **Preview 직접 확인**: `open output.pdf`로 macOS Preview에서 모든 페이지 시각 검증

### Trade-off

- **장점**: 100% 안정적, 모든 PDF 뷰어에서 동일하게 보임, 폰트·이미지·CSS 효과 완벽 보존
- **단점**: 텍스트 선택/복사 불가 (이미지 PDF), 파일 크기 증가 (22슬라이드 ≈ 3MB)
- **텍스트 PDF가 필요하면**: WeasyPrint, 또는 변환 직전에 source HTML에서 `@media print` 블록을 제거(또는 무력화)한 후 `page.pdf()` 사용

### 프로젝트의 기성 유틸리티

DACON 제안서 리포에는 이 패턴을 그대로 구현한 `scripts/html_to_pdf.py`가 있다.
신규 슬라이드 PDF 변환 시 새 코드를 작성하지 말고 다음을 사용한다:

```bash
python3 scripts/html_to_pdf.py 제안/파일명.html              # 단일 변환
python3 scripts/html_to_pdf.py "제안/2026-04-*.html"        # 글롭
python3 scripts/html_to_pdf.py --width 960 --height 1358 portrait.html  # 세로형
```

상세 사용법: `scripts/README.md` 참조.

---

## 8. 슬라이드 생성 시 에이전트 역할 분담

슬라이드 콘텐츠가 많을 경우 병렬 에이전트로 분담:

| 에이전트 | 역할 |
|---------|------|
| **Agent A** | 슬라이드 HTML 마크업 생성 (섹션별 콘텐츠) |
| **Agent B** | CSS 스타일링 (테마, 레이아웃 변형, 전환 효과) |
| **Agent C** | JavaScript 엔진 (네비게이션, fragment, 발표자 뷰) |
| **Agent D** | 콘텐츠 빌드 효과 (fragment 순서, 코드 강조, 애니메이션) |

최종 통합은 메인 에이전트가 단일 HTML 파일로 병합한다.

슬라이드 수가 적으면 (10장 이하) 에이전트 분담 없이 메인 에이전트가 직접 생성해도 충분하다.

---

## 9. DACON / DAKER 공식 수치 (슬라이드 작성 시 참조)

제안서/슬라이드에서 데이콘(DACON) 또는 데이커(DAKER) 관련 수치를 인용할 때 반드시 아래 공식 수치를 사용한다. **임의로 부풀리지 않는다.**

| 항목 | 공식 수치 | 비고 |
|------|----------|------|
| 데이콘 회원 수 | **14만+** | "14만 데이터 사이언티스트" |
| 누적 상금 | **25억 1,072만원** | 총 상금 규모 |
| 누적 제출 수 | **1,030,142** | 모델/결과물 제출 건수 |
| 누적 팀 참여 | **236,666** | 팀 단위 참가 수 |
| 누적 대회 운영 | **500+** | 경진대회/해커톤 합산 |
| 최소 대회 준비 기간 | **1주** | DAKER 플랫폼 세팅 기준 |

**금지 표현**: "30만", "20만" 등 과장된 수치 사용 금지. 위 공식 수치만 사용.

### 제안서 슬라이드에 실제 화면 캡처 포함 규칙

제안서 슬라이드 생성 시 **실제 데이콘/데이커 페이지 스크린샷**을 캡처하여 포함한다:

1. **dacon.io 메인 페이지** — 대회 목록, 통계 지표 (상금/제출/팀 참여)
2. **dacon.io 대회 상세** — 리더보드, 제출 화면, Q&A 게시판
3. **daker.ai 해커톤 페이지** — 팀 빌딩, 쇼케이스, Expert 심사 화면

캡처 방법:
- Claude in Chrome MCP로 실제 페이지 navigate → viewport 캡처
- 캡처 이미지는 제안서 HTML에 `<img>` 태그로 직접 삽입 또는 base64 인코딩
- 캡처 불가 시: 실제 URL을 포함한 **페이지 미리보기 카드** 형태로 대체
