#!/usr/bin/env python3
"""
check_md_html_sync.py — 제안서 MD ↔ HTML 동기화 검증

강원대 제안서(또는 다른 짝지어진 .md/.html 슬라이드 덱)의 섹션 라벨이
일치하는지 검사한다. pre-commit 훅에서 호출하여 드리프트를 조기 발견.

검증 항목:
1. MD 헤더(`### N. ...` / `#### 가. ...`)와 HTML 슬라이드 라벨(`.sh-l` 텍스트)의
   섹션 번호 매핑이 일치하는가
2. 핵심 키워드(예: 250명, 65팀, 11팀, 7.8 본선)가 양쪽에 모두 존재하는가

사용법:
  python3 scripts/check_md_html_sync.py PAIR.md PAIR.html
  python3 scripts/check_md_html_sync.py --pair 강원대   # 사전 정의된 쌍
  python3 scripts/check_md_html_sync.py --all           # 모든 페어 검사

종료 코드:
  0 — 동기화 양호
  1 — 불일치 발견
  2 — 사용 오류 / 파일 없음
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 사전 정의된 검사 페어 (확장 가능)
PAIRS = {
    "강원대": (
        "제안/2026-04-08-강원대학교_X+AI_SW융합프로젝트_제안서.md",
        "제안/2026-04-08-강원대학교_X+AI_SW융합프로젝트_제안서.html",
    ),
}

# 양쪽에 모두 등장해야 하는 핵심 키워드 (페어별로 다를 수 있음)
KEY_FACTS = {
    "강원대": [
        "250명", "65팀", "11팀",
        "5.18", "6.29", "7.6", "7.8",
        "춘천캠퍼스",
        "데이콘(주)",
    ],
}


def extract_md_headers(md_path: Path) -> list[tuple[int, str]]:
    """MD 파일에서 (level, text) 헤더 목록 추출."""
    out = []
    for i, line in enumerate(md_path.read_text(encoding="utf-8").splitlines(), 1):
        m = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if m:
            out.append((len(m.group(1)), m.group(2)))
    return out


def extract_html_slide_labels(html_path: Path) -> list[str]:
    """HTML 파일에서 .sh-l 슬라이드 라벨 텍스트 목록 추출."""
    text = html_path.read_text(encoding="utf-8")
    labels = re.findall(r'class="sh-l"[^>]*>([^<]+)<', text)
    # HTML 엔티티 정리
    return [l.replace("&amp;", "&").replace("&middot;", "·").strip() for l in labels]


def check_pair(md_path: Path, html_path: Path, key_facts: list[str], verbose: bool = True) -> int:
    """단일 페어 검사. 0 = OK, 1 = 불일치."""
    issues: list[str] = []

    if not md_path.exists():
        print(f"❌ MD 파일 없음: {md_path}", file=sys.stderr)
        return 2
    if not html_path.exists():
        print(f"❌ HTML 파일 없음: {html_path}", file=sys.stderr)
        return 2

    md_text = md_path.read_text(encoding="utf-8")
    html_text = html_path.read_text(encoding="utf-8")

    # === 1. 핵심 키워드 존재 여부 ===
    for fact in key_facts:
        in_md = fact in md_text
        in_html = fact in html_text
        if in_md and not in_html:
            issues.append(f"핵심 키워드 '{fact}'가 MD에는 있으나 HTML에 없음")
        elif in_html and not in_md:
            issues.append(f"핵심 키워드 '{fact}'가 HTML에는 있으나 MD에 없음")

    # === 2. 섹션 번호 매핑 (느슨한 검증: HTML 라벨에 등장하는 II-N-X 또는
    #     III/IV/V/VI 번호가 MD 헤더 어딘가에 대응 표현으로 존재하는가) ===
    html_labels = extract_html_slide_labels(html_path)
    md_headers = extract_md_headers(md_path)
    md_header_text = "\n".join(t for _, t in md_headers)

    # HTML 라벨에서 섹션 번호 토큰 추출 (예: "II-1-라", "II-6", "III", "VI")
    section_pattern = re.compile(r"^([IVX]+(?:-\d+(?:-[가-힣])?)?)\.\s")
    for label in html_labels:
        m = section_pattern.match(label)
        if not m:
            continue
        token = m.group(1)
        # MD에서 대응하는 한글 섹션 라벨이 있는지 확인 (가/나/다/라/마/바/사/아 또는 1/2/3/...)
        # 간단 휴리스틱: token의 마지막 부분이 MD 헤더 텍스트 시작에 등장
        last = token.split("-")[-1]
        if not (re.search(rf"(^|\s){re.escape(last)}\.", md_header_text)):
            # 라벨의 키워드가 MD 어딘가에 등장하면 OK
            label_keyword = re.sub(r"^[IVX\-\d가-힣\s]+\.\s*", "", label).strip()
            if label_keyword and label_keyword[:8] not in md_header_text and label_keyword[:8] not in md_text:
                issues.append(
                    f"HTML 슬라이드 '{label}' (섹션 {token})에 대응하는 MD 섹션이 명확치 않음"
                )

    # === 결과 출력 ===
    if not issues:
        if verbose:
            print(f"✓ MD ↔ HTML 동기화 양호")
            print(f"  MD: {md_path.relative_to(ROOT) if md_path.is_relative_to(ROOT) else md_path}")
            print(f"  HTML: {html_path.relative_to(ROOT) if html_path.is_relative_to(ROOT) else html_path}")
            print(f"  HTML 슬라이드: {len(html_labels)}개, MD 헤더: {len(md_headers)}개, 키워드 검증: {len(key_facts)}개")
        return 0

    print(f"⚠️  MD ↔ HTML 동기화 이슈 {len(issues)}건 발견:")
    for issue in issues:
        print(f"   - {issue}")
    print()
    print(f"   MD: {md_path}")
    print(f"   HTML: {html_path}")
    print()
    print("   해결 가이드:")
    print("   1. 한쪽에서 추가/수정/삭제한 내용을 반대편에도 반영하세요")
    print("   2. 섹션 번호·표현·핵심 수치를 일치시키세요")
    print("   3. HTML 수정 후: python3 scripts/html_to_pdf.py <html파일>")
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("md", nargs="?", help="MD 파일 경로")
    parser.add_argument("html", nargs="?", help="HTML 파일 경로")
    parser.add_argument("--pair", help="사전 정의된 페어 이름 (예: 강원대)")
    parser.add_argument("--all", action="store_true", help="모든 사전 정의 페어 검사")
    parser.add_argument("--quiet", "-q", action="store_true", help="성공 메시지 숨김")
    args = parser.parse_args()

    if args.all:
        rc = 0
        for name, (md, html) in PAIRS.items():
            print(f"--- {name} ---")
            r = check_pair(ROOT / md, ROOT / html, KEY_FACTS.get(name, []), verbose=not args.quiet)
            rc = max(rc, r)
        return rc

    if args.pair:
        if args.pair not in PAIRS:
            print(f"❌ Unknown pair: {args.pair}. Known: {list(PAIRS.keys())}", file=sys.stderr)
            return 2
        md, html = PAIRS[args.pair]
        return check_pair(ROOT / md, ROOT / html, KEY_FACTS.get(args.pair, []), verbose=not args.quiet)

    if not args.md or not args.html:
        parser.print_help()
        return 2

    return check_pair(Path(args.md), Path(args.html), [], verbose=not args.quiet)


if __name__ == "__main__":
    sys.exit(main())
