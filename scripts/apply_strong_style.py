#!/usr/bin/env python3
"""
apply_strong_style.py — 강원대 HTML 스타일을 전 DACON 슬라이드 덱에 일괄 적용

기준 스타일 (2026-04-17-강원대_AI첨단산업인재양성부트캠프_비공개_알고리즘_경진대회_제안서.html):
  1. #stage 크기 16:9 통일 (--sh:720px)         — 세로형 덱(--sh > 1200)은 제외
  2. 모서리 라운딩 전량 제거 (--rs~--rf 모두 0)
  3. 본문 폰트 144% 확대 (html{font-size:144%})
  4. 헤더/푸터 폰트 px 절대값 고정:
        .sh-l 13px, .sh-r 11px, .sf-logo 12px, .sf-pg 11px, .sf-cr 9px
  5. .tag::before hardcoded border-radius:2px 제거
  6. fit() JS divisor vh/N → vh/720
  7. @page size A4 landscape → landscape

사용법
  python3 scripts/apply_strong_style.py --dry-run      # 변경 대상·diff 미리보기
  python3 scripts/apply_strong_style.py                # 실제 적용
  python3 scripts/apply_strong_style.py --path 제안/foo.html  # 단일 파일만

안전
  * 대상은 `--sw2:1280px` + `.slide` 패턴을 가진 파일만 (DACON 템플릿)
  * 이미 적용된 변경은 idempotent — 여러 번 실행해도 안전
  * --dry-run으로 미리 확인 가능
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def transform(text: str) -> tuple[str, list[str]]:
    """Apply all migrations. Returns (new_text, list_of_applied_changes).

    Supports two DACON slide-deck CSS conventions:
      * COMPACT: `--sw2` / `--sh` / `--rs..--rf` / `.sh-l` / `.sf-cr` (current).
      * VERBOSE: `--slide-w` / `--slide-h` / `--radius-sm..--radius-xl` (older).
    Detection is permissive — it only skips if neither pattern is present.
    """
    changes: list[str] = []
    out = text

    is_compact = "--sw2:1280px" in out or "--sw2: 1280px" in out
    is_verbose = re.search(r"--slide-w\s*:\s*1280px", out) is not None
    if not (is_compact or is_verbose):
        return out, ["SKIP: not a DACON slide deck template"]

    # 1a) COMPACT stage height → 720
    if is_compact:
        m = re.search(r"--sh\s*:\s*(\d+)px", out)
        if m:
            cur_h = int(m.group(1))
            if cur_h > 1200:
                changes.append(f"SKIP: portrait deck (--sh:{cur_h}px)")
                return out, changes
            if cur_h != 720:
                out = re.sub(r"--sh\s*:\s*\d+px", "--sh:720px", out, count=1)
                changes.append(f"stage height: {cur_h} → 720")
    # 1b) VERBOSE stage height → 720
    if is_verbose:
        m = re.search(r"--slide-h\s*:\s*(\d+)px", out)
        if m:
            cur_h = int(m.group(1))
            if cur_h > 1200:
                changes.append(f"SKIP: portrait deck (--slide-h:{cur_h}px)")
                return out, changes
            if cur_h != 720:
                out = re.sub(r"(--slide-h\s*:\s*)\d+px", r"\g<1>720px", out)
                changes.append(f"slide-h: {cur_h} → 720")

    # 2a) COMPACT radius vars → 0
    old_rad_re = re.compile(
        r"--rs:[\d.]+(?:rem|px)?;\s*"
        r"--rm:[\d.]+(?:rem|px)?;\s*"
        r"--rl:[\d.]+(?:rem|px)?;\s*"
        r"--rx:[\d.]+(?:rem|px)?;\s*"
        r"--rf:[\d.]+(?:rem|px)?;?"
    )
    if old_rad_re.search(out):
        out = old_rad_re.sub("--rs:0;--rm:0;--rl:0;--rx:0;--rf:0;", out, count=1)
        changes.append("radius vars (compact) → 0")

    # 2b) VERBOSE radius vars → 0
    # Matches --radius-sm/md/lg/xl/full/2xl ... any name starting with --radius-
    verbose_rad_count = 0
    for m in list(re.finditer(r"(--radius-[a-z0-9]+)\s*:\s*[\d.]+(?:rem|px)", out)):
        pass
    new_out, n = re.subn(r"(--radius-[a-z0-9]+)\s*:\s*[\d.]+(?:rem|px)", r"\g<1>: 0", out)
    if n:
        out = new_out
        changes.append(f"radius vars (verbose) → 0 ({n} vars)")
    # Also handle --r-xx style (even shorter)
    new_out, n = re.subn(r"(--r-[a-z0-9]+)\s*:\s*[\d.]+(?:rem|px)", r"\g<1>: 0", out)
    if n:
        out = new_out
        changes.append(f"radius vars (r-*) → 0 ({n} vars)")

    # 3) html{font-size:144%} insertion
    if "font-size:144%" not in out:
        # Insert before the first `html,body{` rule.
        m_hb = re.search(r"(html,body\s*\{)", out)
        if m_hb:
            out = out[:m_hb.start()] + "html{font-size:144%}\n" + out[m_hb.start():]
            changes.append("inserted html{font-size:144%}")
    else:
        pass  # already present

    # 4) Header/footer rem → px (surgical per-selector)
    rem_px_map = [
        (r"\.sh-l\{font-size:\.8125rem", ".sh-l{font-size:13px", ".sh-l 13px"),
        (r"\.sh-r\{font-size:\.6875rem", ".sh-r{font-size:11px", ".sh-r 11px"),
        (r"(\.sf-logo\{[^}]*?)font-size:\.75rem", r"\g<1>font-size:12px", ".sf-logo 12px"),
        (r"\.sf-pg\{font-size:\.6875rem", ".sf-pg{font-size:11px", ".sf-pg 11px"),
        (r"\.sf-cr\{font-size:\.5625rem", ".sf-cr{font-size:9px", ".sf-cr 9px"),
    ]
    for pat, repl, label in rem_px_map:
        new_out, n = re.subn(pat, repl, out, count=1)
        if n:
            out = new_out
            changes.append(label)

    # 5) .tag::before border-radius:2px removal
    new_out, n = re.subn(
        r"(\.tag::before\{[^}]*?);?\s*border-radius:2px",
        r"\g<1>",
        out,
        count=1,
    )
    if n:
        out = new_out
        changes.append(".tag::before radius removed")

    # 6) fit() JS divisor — handles both `Math.min(vw/1280,vh/905,...)` and
    # variants with spaces `Math.min(vw / 1280, vh / 905, ...)`.
    for pat in [
        r"(Math\.min\(vw/1280,\s*vh/)\d+",
        r"(Math\.min\(\s*vw\s*/\s*1280\s*,\s*vh\s*/\s*)\d+",
    ]:
        new_out, n = re.subn(pat, r"\g<1>720", out, count=1)
        if n:
            # Only report if something actually changed
            if new_out != out:
                out = new_out
                changes.append("fit() JS divisor → 720")
            break

    # 7) @page size A4 landscape → landscape
    new_out, n = re.subn(
        r"@page\s*\{\s*size:\s*A4\s+landscape",
        "@page { size: landscape",
        out,
        count=1,
    )
    if n:
        out = new_out
        changes.append("@page: A4 landscape → landscape")

    if not changes:
        changes.append("(no changes needed — already migrated)")

    return out, changes


def find_targets(explicit: list[Path] | None = None) -> list[Path]:
    if explicit:
        return explicit
    out: list[Path] = []
    for folder in ("제안", "내부", "전략"):
        p = ROOT / folder
        if p.exists():
            out.extend(p.rglob("*.html"))
    return sorted(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--path", action="append", help="특정 파일만 (여러 번 지정 가능)")
    ap.add_argument("--dry-run", action="store_true", help="적용 없이 변경 예정만 출력")
    ap.add_argument("--quiet", "-q", action="store_true")
    args = ap.parse_args()

    targets: list[Path] = []
    if args.path:
        targets = [Path(p) for p in args.path]
    else:
        targets = find_targets()

    log = (lambda *a, **k: None) if args.quiet else print

    touched = 0
    skipped = 0
    for src in targets:
        if not src.exists():
            continue
        try:
            original = src.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        new_text, changes = transform(original)
        rel = src.relative_to(ROOT) if src.is_relative_to(ROOT) else src
        if any(c.startswith("SKIP") for c in changes):
            skipped += 1
            log(f"⏭  {rel} — {changes[0]}")
            continue
        if original == new_text:
            skipped += 1
            log(f"✓  {rel} — already migrated")
            continue
        if args.dry_run:
            log(f"🧪 {rel} — would change:")
            for c in changes:
                log(f"    • {c}")
        else:
            src.write_text(new_text, encoding="utf-8")
            log(f"✅ {rel} — applied:")
            for c in changes:
                log(f"    • {c}")
        touched += 1

    log()
    log(f"Summary: {touched} {'would change' if args.dry_run else 'changed'}, {skipped} skipped, {len(targets)} total")
    return 0


if __name__ == "__main__":
    sys.exit(main())
