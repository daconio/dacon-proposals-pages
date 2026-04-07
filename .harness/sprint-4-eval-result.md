# Sprint 4 — Evaluator Result

Attempt: 1
Timestamp: 2026-04-07T23:36:00+09:00

## Score

Overall: 100%

## Item Scores

| Contract Item | Score | Evidence |
|--------------|-------|----------|
| CR-4.1 — 인라인 JSON 데이터 | 100% | `demo-hackathon.html:1023` 및 `demo-edu.html:1023`에 `<script type="application/json" id="report-data">` 태그 존재. `js/renderer.js:460` `document.getElementById('report-data')` → `renderInline(data)` 경로로 fetch 없이 처리됨. |
| CR-4.2 — index.html 링크 2개 | 100% | `사후리포트/index.html:212` `<a class="demo-card hack" href="./demo-hackathon.html">`, `:218` `<a class="demo-card edu" href="./demo-edu.html">` 두 개의 `<a href>` 확인. |
| CR-4.3 — 인쇄 안내 포함 | 100% | `사후리포트/index.html:228` `<h2>PDF 저장 방법</h2>`, `:231` 한국어 "Ctrl + P (macOS는 ⌘ + P) 또는 브라우저 메뉴 → 인쇄", `:232` "PDF로 저장" 5단계 안내 포함 (Ctrl/P는 `<span class="kbd">`로 분리되어 있어 문자열 grep은 불일치하지만 렌더링된 텍스트와 DOM 모두에 존재). |
| CR-4.4 — 파일명 규칙 예시 | 100% | `사후리포트/index.html:252` `<code>YYYY-MM-DD-{고객사}_{행사명}_사후리포트.html</code>`, `:254-255` 두 개 실제 예시 (`2026-03-15-금융보안원_...`, `2026-02-23-단국대학교_...`). |
| CR-4.5 — 금지 문구 부재 | 100% | `grep -R "견적\|예산\|비용\|패키지 가격\|스킬 리포트" 사후리포트/` 결과 0건 (index.html / demo-hackathon.html / demo-edu.html / js/renderer.js / data/*.json 전체 스캔). |
| RV-4.1 — 해커톤 데모 자급자족 동작 | 100% | `Google Chrome --headless=new --dump-dom file://.../demo-hackathon.html` → 56,712 bytes, `<html lang="ko" data-report-ready="1">` 설정, `<title>DAKER 사후 리포트 · 2026 금융보...`, 샘플 한글 매칭 30건. file:// 프로토콜 + 네트워크 없이 완전 렌더링 확인. |
| RV-4.2 — 교육 데모 자급자족 동작 | 100% | `Google Chrome --headless=new --dump-dom file://.../demo-edu.html` → 53,112 bytes, `<html lang="ko" data-report-ready="1">`, `<title>DAKER 사후 리포트 · 2026 단국대학교 바이브코딩 집중 부트캠프</title>`, 샘플 한글 매칭 18건. 정상 렌더링. |
| RV-4.3 — 인쇄 레이아웃 정상 | 100% | `--print-to-pdf` 로 `hack.pdf` 982,374 bytes / **11페이지**, `edu.pdf` 946,237 bytes / **10페이지** 정상 생성. 코드 상 `demo-hackathon.html:150` `.report-section { page-break-before: always }`, `:155` `.cover { page-break-before: avoid }`, `:166` `.team-card/.participant-row { page-break-inside: avoid }` 규칙 상속 확인 → 커버 1페이지 독립 + 섹션 제목 새 페이지 시작 + 카드 중간 잘림 방지가 논리적으로 충족됨. |
| RV-4.4 — index.html 정상 열기 | 100% | `--dump-dom file://.../index.html` 결과에서 `:212` "해커톤 샘플", `:218` "교육 프로그램 샘플" 링크 텍스트 및 `./demo-hackathon.html`, `./demo-edu.html` href 6건 매칭. DOM 파싱 오류 없음. |

## Verdict

PASS

모든 필수 기준(CR-4.1 ~ CR-4.5, RV-4.1 ~ RV-4.4)을 100%로 충족하였습니다. 두 데모 파일은 file:// 프로토콜에서 네트워크 없이 완전 자급자족 렌더링되며, Chrome headless `--print-to-pdf` 로 A4 다중 페이지 PDF가 정상 생성됨을 확인하였습니다. 금지 문구(견적/예산/비용/패키지 가격/스킬 리포트) 0건, 파일명 규칙·PDF 저장 안내·두 데모 링크 모두 `index.html`에 명시되어 있습니다.
