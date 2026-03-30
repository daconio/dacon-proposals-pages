const { execSync } = require('child_process');
const fs = require('fs');

// 1. npx marked로 마크다운을 순수 HTML로 변환합니다.
execSync('npx --yes marked -i "2026-03-30-중앙대_장경석교수_AI대회문의_회신.md" -o "temp.html"');

const htmlContent = fs.readFileSync('temp.html', 'utf-8');

// 2. 이메일에서 예쁘게 보이고, 한글 안 깨지도록 CSS와 meta charset을 씌웁니다.
const finalHtml = `<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif; line-height: 1.6; color: #333; max-width: 800px; padding: 20px; }
  table { border-collapse: collapse; width: 100%; margin: 20px 0; font-size: 14px; background: white; }
  th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
  th { background-color: #f8f9fa; font-weight: bold; border-bottom: 2px solid #ccc; }
  blockquote { border-left: 4px solid #0056b3; margin: 15px 0; padding: 12px 15px; color: #444; background-color: #f4f6f9; border-radius: 0 4px 4px 0; }
  h1, h2, h3 { color: #111; margin-top: 24px; }
  hr { border: 0; border-top: 1px solid #eee; margin: 20px 0; }
  code { background-color: #f1f1f1; padding: 2px 4px; border-radius: 3px; font-family: monospace; }
</style>
</head>
<body>
${htmlContent}
</body>
</html>`;

// 3. 최종 HTML 파일 저장
fs.writeFileSync('2026-03-30-중앙대_장경석교수_AI대회문의_회신.html', finalHtml);
fs.unlinkSync('temp.html'); // 임시 파일 삭제
