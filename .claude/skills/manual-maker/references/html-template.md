# HTML 매뉴얼 템플릿 가이드

## 기본 HTML 구조

에이전트 C가 HTML 매뉴얼을 생성할 때 다음 구조를 따른다.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{기능명} 사용자 매뉴얼 - DAKER</title>
<style>
  :root {
    --bg: #0f172a;
    --surface: #1e293b;
    --surface2: #334155;
    --border: #475569;
    --text: #e2e8f0;
    --text-muted: #94a3b8;
    --accent: #3b82f6;
    --accent-glow: rgba(59,130,246,0.15);
    --green: #22c55e;
    --yellow: #eab308;
    --cyan: #06b6d4;
  }
  * { margin:0; padding:0; box-sizing:border-box; }
  body {
    font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.7;
    padding: 2rem;
  }
  .container { max-width: 960px; margin: 0 auto; }

  /* Header */
  .header {
    text-align: center;
    padding: 3rem 0 2rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 3rem;
  }
  .header h1 {
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--accent), var(--cyan));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
  }
  .header .meta {
    color: var(--text-muted);
    font-size: 0.9rem;
  }
  .header .meta span {
    display: inline-block;
    background: var(--surface);
    padding: 0.2rem 0.8rem;
    border-radius: 999px;
    margin: 0.3rem;
    border: 1px solid var(--border);
  }

  /* TOC */
  .toc {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 2rem;
  }
  .toc h2 { font-size: 1.1rem; margin-bottom: 0.8rem; }
  .toc a {
    color: var(--accent);
    text-decoration: none;
    display: block;
    padding: 0.3rem 0;
  }
  .toc a:hover { text-decoration: underline; }

  /* Section */
  section { margin-bottom: 3rem; }
  section h2 {
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 1.2rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid var(--accent);
    display: inline-block;
  }
  section h3 {
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--cyan);
    margin: 1.5rem 0 0.8rem;
  }

  /* Steps */
  .step {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
  }
  .step-number {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    background: var(--accent);
    color: #fff;
    border-radius: 50%;
    font-weight: 700;
    font-size: 0.9rem;
    margin-right: 0.8rem;
    flex-shrink: 0;
  }
  .step-title {
    font-weight: 600;
    font-size: 1.05rem;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
  }
  .step-desc {
    color: var(--text-muted);
    margin-bottom: 1rem;
    padding-left: 2.5rem;
  }

  /* Screenshot */
  .screenshot-wrapper {
    margin: 1rem 0;
    text-align: center;
  }
  .screenshot-wrapper img {
    max-width: 100%;
    border-radius: 8px;
    border: 1px solid var(--border);
    cursor: pointer;
    transition: transform 0.2s;
  }
  .screenshot-wrapper img:hover {
    transform: scale(1.02);
  }
  .screenshot-caption {
    color: var(--text-muted);
    font-size: 0.85rem;
    margin-top: 0.5rem;
  }

  /* Lightbox */
  .lightbox {
    display: none;
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0,0,0,0.9);
    z-index: 1000;
    justify-content: center;
    align-items: center;
    cursor: pointer;
  }
  .lightbox.active { display: flex; }
  .lightbox img {
    max-width: 95vw;
    max-height: 95vh;
    border-radius: 8px;
  }

  /* Tip / Warning */
  .tip {
    background: rgba(34,197,94,0.1);
    border-left: 4px solid var(--green);
    padding: 1rem 1.2rem;
    border-radius: 0 8px 8px 0;
    margin: 1rem 0;
  }
  .warning {
    background: rgba(234,179,8,0.1);
    border-left: 4px solid var(--yellow);
    padding: 1rem 1.2rem;
    border-radius: 0 8px 8px 0;
    margin: 1rem 0;
  }

  /* Footer */
  .footer {
    text-align: center;
    padding: 2rem 0;
    border-top: 1px solid var(--border);
    margin-top: 3rem;
    color: var(--text-muted);
    font-size: 0.85rem;
  }
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>{기능명} 사용자 매뉴얼</h1>
    <div class="meta">
      <span>DAKER</span>
      <span>작성일: {YYYY-MM-DD}</span>
      <span>대상: {사용자/관리자/심사위원}</span>
    </div>
  </div>

  <!-- 목차 -->
  <div class="toc">
    <h2>목차</h2>
    <a href="#overview">1. 개요</a>
    <a href="#getting-started">2. 시작하기</a>
    <a href="#features">3. 주요 기능</a>
    <a href="#faq">4. FAQ</a>
  </div>

  <!-- 본문 섹션들 -->
  <section id="overview">
    <h2>1. 개요</h2>
    <p>기능 설명...</p>
  </section>

  <section id="getting-started">
    <h2>2. 시작하기</h2>
    <div class="step">
      <div class="step-title">
        <span class="step-number">1</span>
        단계 제목
      </div>
      <div class="step-desc">단계 설명</div>
      <div class="screenshot-wrapper">
        <img src="screenshots/manual-{주제}/01-화면명.png"
             alt="화면 설명"
             onclick="openLightbox(this.src)">
        <div class="screenshot-caption">화면 설명 캡션</div>
      </div>
    </div>
  </section>

  <!-- Footer -->
  <div class="footer">
    <p>이 문서는 Claude Code로 자동 생성되었습니다. | {YYYY-MM-DD}</p>
  </div>
</div>

<!-- Lightbox -->
<div class="lightbox" id="lightbox" onclick="closeLightbox()">
  <img id="lightbox-img" src="" alt="확대 이미지">
</div>

<script>
function openLightbox(src) {
  document.getElementById('lightbox-img').src = src;
  document.getElementById('lightbox').classList.add('active');
}
function closeLightbox() {
  document.getElementById('lightbox').classList.remove('active');
}
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') closeLightbox();
});
</script>
</body>
</html>
```

## 이미지 참조 규칙

- 상대 경로 사용: `screenshots/manual-{주제}/파일명.png`
- HTML과 스크린샷 디렉토리가 같은 `docs/plans/` 하위에 있으므로 상대 경로가 동작한다
- alt 텍스트에 화면 설명을 반드시 포함한다
