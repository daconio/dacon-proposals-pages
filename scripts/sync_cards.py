#!/usr/bin/env python3
"""
sync_cards.py — index.html 랜딩 페이지 카드 그리드 자동 동기화 도구

사용법:
  python3 scripts/sync_cards.py              # index.html을 cards.json 기준으로 재생성
  python3 scripts/sync_cards.py --check      # 변경사항만 확인 (변경 필요 시 exit 1)
  python3 scripts/sync_cards.py --scan       # 매니페스트에 등록되지 않은 HTML 파일 탐색
  python3 scripts/sync_cards.py --all        # sync + scan 둘 다

구조:
  - scripts/cards.json        : 카드 메타데이터 단일 소스(sections → cards)
  - index.html (AUTO 마커 내부) : 이 스크립트가 재생성하는 영역

AUTO 마커:
  <!-- AUTO:cards-start -->
  ... (재생성 영역)
  <!-- AUTO:cards-end -->
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata
from pathlib import Path


def nfc(s: str) -> str:
    """Normalize Korean filenames: macOS stores NFD (decomposed jamo),
    but cards.json and Git typically use NFC (precomposed). Compare in NFC."""
    return unicodedata.normalize("NFC", s)

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "scripts" / "cards.json"
INDEX_PATH = ROOT / "index.html"

MARKER_START = "<!-- AUTO:cards-start -->"
MARKER_END = "<!-- AUTO:cards-end -->"

INDENT = "  "  # 2-space indent inside <div class="container">

VALID_COLORS = {"blue", "warm", "dark"}


def load_manifest() -> dict:
    if not MANIFEST_PATH.exists():
        sys.stderr.write(f"❌ Manifest not found: {MANIFEST_PATH}\n")
        sys.exit(2)
    with MANIFEST_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def html_escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def render_card(card: dict) -> str:
    href = card["href"]
    title = card["title"]
    date = card["date"]
    icon = card.get("icon", "?")
    color = card.get("color", "blue")
    badge = card.get("badge", "")

    if color not in VALID_COLORS:
        sys.stderr.write(
            f"⚠️  Unknown color '{color}' for card {href!r}, defaulting to 'blue'.\n"
        )
        color = "blue"

    badge_class = "badge-new" if badge == "NEW" else "badge-proposal"
    if badge == "슬라이드":
        badge_class = "badge-slide"

    return (
        f'{INDENT}  <a class="card" href="{html_escape(href)}">\n'
        f'{INDENT}    <div class="card-icon {color}">{html_escape(icon)}</div>\n'
        f'{INDENT}    <div class="card-body">\n'
        f'{INDENT}      <div class="card-title">{html_escape(title)}</div>\n'
        f'{INDENT}      <div class="card-date">{html_escape(date)}</div>\n'
        f"{INDENT}    </div>\n"
        f'{INDENT}    <span class="card-badge {badge_class}">{html_escape(badge)}</span>\n'
        f"{INDENT}  </a>"
    )


def render_section(section: dict) -> str:
    title = section["title"]
    cards = section.get("cards", [])
    lines = [
        f'{INDENT}<div class="section-title">{html_escape(title)}</div>',
        f'{INDENT}<div class="card-grid">',
    ]
    lines.extend(render_card(c) for c in cards)
    lines.append(f"{INDENT}</div>")
    return "\n".join(lines)


def render_all(manifest: dict) -> str:
    sections = manifest.get("sections", [])
    blocks = [render_section(s) for s in sections]
    return "\n\n".join(blocks)


def splice_index(generated: str) -> tuple[str, str]:
    """Return (original, new) index.html contents with generated block spliced in."""
    if not INDEX_PATH.exists():
        sys.stderr.write(f"❌ index.html not found: {INDEX_PATH}\n")
        sys.exit(2)
    original = INDEX_PATH.read_text(encoding="utf-8")

    pattern = re.compile(
        re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END),
        re.DOTALL,
    )
    replacement = f"{MARKER_START}\n{generated}\n{INDENT}{MARKER_END}"

    if not pattern.search(original):
        sys.stderr.write(
            f"❌ AUTO markers not found in index.html.\n"
            f"   Expected: {MARKER_START} ... {MARKER_END}\n"
            f"   Add these inside <div class=\"container\">.\n"
        )
        sys.exit(2)

    new = pattern.sub(replacement, original, count=1)
    return original, new


def cmd_sync(manifest: dict, check: bool = False) -> int:
    generated = render_all(manifest)
    original, new = splice_index(generated)
    if original == new:
        print("✓ index.html is already in sync with scripts/cards.json")
        return 0
    if check:
        print("✗ index.html is OUT OF SYNC with scripts/cards.json")
        print("  Run: python3 scripts/sync_cards.py")
        return 1
    INDEX_PATH.write_text(new, encoding="utf-8")
    total = sum(len(s.get("cards", [])) for s in manifest.get("sections", []))
    print(f"✨ index.html synced — {total} cards across {len(manifest.get('sections', []))} sections")
    return 0


def _find_missing(manifest: dict) -> list[str]:
    """Return list of 'dir/file.html' paths present on disk but not in cards.json."""
    scan_cfg = manifest.get("scan", {})
    dirs = scan_cfg.get("directories", [])
    ignore_patterns = scan_cfg.get("ignore_patterns", [])

    registered: set[str] = set()
    for section in manifest.get("sections", []):
        for card in section.get("cards", []):
            href = card["href"].replace("%2B", "+")  # normalize URL-encoded
            registered.add(nfc(href))

    ignore_nfc = [nfc(p) for p in ignore_patterns]

    missing: list[str] = []
    for d in dirs:
        dir_path = ROOT / d
        if not dir_path.exists():
            continue
        for html_file in sorted(dir_path.glob("*.html")):
            name = nfc(html_file.name)
            rel = nfc(f"{d}/{name}")
            if rel in registered:
                continue
            if any(pat in name for pat in ignore_nfc):
                continue
            if not re.match(r"^(\d{4}-\d{2}-\d{2}-|\d{8}_)", name):
                continue
            missing.append(rel)
    return missing


def cmd_scan(manifest: dict) -> int:
    missing = _find_missing(manifest)
    if not missing:
        print("✓ No unregistered proposal HTMLs found")
        return 0

    print("⚠️  Unregistered proposal HTMLs (not in scripts/cards.json):")
    for m in missing:
        print(f"    {m}")
    print()
    print("  If these should appear on the landing page, add entries to")
    print("  scripts/cards.json, then run: python3 scripts/sync_cards.py")
    print("  If they should NOT, add a substring to `scan.ignore_patterns`.")
    print("  Or run: python3 scripts/sync_cards.py --autoregister (auto-add).")
    return 1  # non-zero so pre-commit hook can surface it


# ---------- Autoregister logic ---------------------------------------------
#
# Heuristics translate a filename like "제안/2026-04-17-foo_bar_제안서.html"
# into a card entry. Authors can always edit cards.json afterwards.

# Token in filename → (section title, badge)
# Tested in order; first match wins.
_TOKEN_RULES = [
    ("소개서", "소개서", "소개서"),
    ("전략서", "전략서", "전략서"),
    ("Pilot", "전략서", "전략서"),
    ("전략", "전략서", "전략서"),
    ("리서치", "리서치", "리서치"),
    ("research", "리서치", "리서치"),
    ("리포트", "리서치", "리서치"),
    ("브리핑", "슬라이드", "슬라이드"),
    ("슬라이드", "슬라이드", "슬라이드"),
    ("소개", "슬라이드", "슬라이드"),
    ("제안서", "제안서", "NEW"),
]

# Directory → (color fallback when section doesn't set one)
_DIR_COLOR = {
    "제안": "blue",
    "내부": "blue",
    "전략": "warm",
    "docs/plans": "dark",
}


def _clean_title(stem: str) -> str:
    """Remove date prefix, underscores, trailing descriptors."""
    s = re.sub(r"^(\d{4}-\d{2}-\d{2}-|\d{8}_)", "", stem)
    s = s.replace("_", " ").strip()
    return s


def _first_icon_char(title: str) -> str:
    for ch in title:
        if ch.isalnum() or ("\uac00" <= ch <= "\ud7a3"):
            return ch.upper() if ch.isascii() else ch
    return "?"


def _infer_metadata(rel_path: str) -> tuple[str, dict]:
    """Given 'dir/file.html', return (section_title, card_dict)."""
    p = Path(rel_path)
    directory = "/".join(p.parts[:-1])
    stem = p.stem

    # Date
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})-", stem)
    if m:
        date = f"{m.group(1)}.{m.group(2)}.{m.group(3)}"
    else:
        m2 = re.match(r"^(\d{4})(\d{2})(\d{2})_", stem)
        date = f"{m2.group(1)}.{m2.group(2)}.{m2.group(3)}" if m2 else ""

    title = _clean_title(stem)

    # Section + badge by filename tokens
    section = "제안서"
    badge = "NEW"
    for token, sect, bdg in _TOKEN_RULES:
        if token in stem:
            section = sect
            badge = bdg
            break
    # docs/plans/ defaults to 슬라이드 if no stronger signal
    if directory == "docs/plans" and section == "제안서":
        section = "슬라이드"
        badge = "슬라이드"

    color = _DIR_COLOR.get(directory, "blue")
    icon = _first_icon_char(title)

    card = {
        "href": rel_path,
        "title": title,
        "date": date,
        "icon": icon,
        "color": color,
        "badge": badge,
    }
    return section, card


def cmd_autoregister(manifest: dict) -> int:
    """Append each unregistered HTML to the appropriate section in cards.json.

    New cards are inserted at the TOP of the section so the landing page shows
    newest first. The updated manifest is written back to disk, then
    index.html is re-synced.
    """
    missing = _find_missing(manifest)
    if not missing:
        # Still make sure index.html is in sync.
        return cmd_sync(manifest, check=False)

    # Ensure every known section exists; create if missing.
    existing_titles = [s.get("title") for s in manifest.get("sections", [])]
    added: list[tuple[str, str]] = []
    for rel in missing:
        section_title, card = _infer_metadata(rel)
        target = None
        for sect in manifest["sections"]:
            if sect.get("title") == section_title:
                target = sect
                break
        if target is None:
            target = {"title": section_title, "cards": []}
            manifest["sections"].append(target)
            existing_titles.append(section_title)
        target.setdefault("cards", []).insert(0, card)
        added.append((rel, section_title))

    # Persist manifest (preserve 2-space indent, sort_keys=False to keep order).
    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"✨ Auto-registered {len(added)} HTML(s) to scripts/cards.json:")
    for rel, sect in added:
        print(f"    · [{sect}] {rel}")

    # Re-sync index.html
    return cmd_sync(manifest, check=False)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check only, do not write")
    parser.add_argument("--scan", action="store_true", help="Scan for unregistered files")
    parser.add_argument("--autoregister", action="store_true",
                        help="Auto-add unregistered HTMLs to cards.json with inferred defaults")
    parser.add_argument("--all", action="store_true", help="Sync + Scan")
    args = parser.parse_args()

    manifest = load_manifest()

    if args.autoregister:
        return cmd_autoregister(manifest)

    if args.scan and not args.all:
        return cmd_scan(manifest)

    rc = cmd_sync(manifest, check=args.check)
    if args.all:
        scan_rc = cmd_scan(manifest)
        return rc if rc != 0 else 0 if scan_rc == 0 else 0
    return rc


if __name__ == "__main__":
    sys.exit(main())
