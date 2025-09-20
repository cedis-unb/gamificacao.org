#!/usr/bin/env python3
import os
import sys
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PT_DIR = ROOT / "content" / "pt"
EN_DIR = ROOT / "content" / "en"


def read_file(p: Path):
    try:
        return p.read_text(encoding="utf-8")
    except Exception as e:
        return ""


def parse_front_matter(text: str):
    # Expect YAML delineated by --- at top
    if not text.startswith("---\n"):
        return {}, text
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        return {}, text
    fm_text = parts[0][4:]  # drop initial ---\n
    # Content after first closing ---
    rest = parts[1]
    # Some files might have an extra --- line right after (empty separator)
    # Keep rest as-is; body is everything after first fm closing.

    data = {}
    for line in fm_text.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        # very lightweight YAML key: value parsing (no nested structures)
        m = re.match(r"([A-Za-z0-9_\-]+):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2)
            # strip quotes
            if val.startswith(('"', "'")) and val.endswith(('"', "'")) and len(val) >= 2:
                val = val[1:-1]
            data[key] = val
    return data, rest


def collect(dirpath: Path, lang: str):
    items = {}
    for p in dirpath.rglob("*.md"):
        rel = p.relative_to(dirpath).as_posix()
        text = read_file(p)
        fm, body = parse_front_matter(text)
        key = None
        if fm.get("translationKey"):
            key = f"t:{fm['translationKey']}"
        else:
            # fallback to path key (for identical structure files)
            key = f"p:{rel}"
        items[key] = {
            "path": rel,
            "abs": p,
            "title": fm.get("title", ""),
            "slug": fm.get("slug", ""),
            "body": body.strip(),
        }
    return items


def main():
    if not PT_DIR.exists() or not EN_DIR.exists():
        print("ERROR: content directories not found:", PT_DIR, EN_DIR, file=sys.stderr)
        return 2

    pt = collect(PT_DIR, "pt")
    en = collect(EN_DIR, "en")

    pt_keys = set(pt.keys())
    en_keys = set(en.keys())

    missing_in_en = sorted(pt_keys - en_keys)
    missing_in_pt = sorted(en_keys - pt_keys)

    print("== Missing in EN (present only in PT) ==")
    if not missing_in_en:
        print("OK: none")
    else:
        for k in missing_in_en:
            item = pt[k]
            print(f"- key {k} -> pt:{item['path']}")

    print("\n== Missing in PT (present only in EN) ==")
    if not missing_in_pt:
        print("OK: none")
    else:
        for k in missing_in_pt:
            item = en[k]
            print(f"- key {k} -> en:{item['path']}")

    print("\n== Potential issues in matched pairs ==")
    both = sorted(pt_keys & en_keys)
    identical_bodies = []
    identical_titles = []
    same_slug = []
    for k in both:
        p = pt[k]
        e = en[k]
        if p["body"] and (p["body"] == e["body"]):
            identical_bodies.append((k, p["path"], e["path"]))
        if p["title"] and (p["title"].strip() == e["title"].strip()):
            identical_titles.append((k, p["title"], p["path"], e["path"]))
        if p["slug"] and e["slug"] and (p["slug"] == e["slug"]):
            same_slug.append((k, p["slug"], p["path"], e["path"]))

    if identical_bodies:
        print("- Identical bodies across languages (likely untranslated):")
        for k, pp, ee in identical_bodies:
            print(f"  * {k}: pt:{pp} <> en:{ee}")
    else:
        print("- Bodies: OK (no identical bodies)")

    if identical_titles:
        print("- Identical titles across languages:")
        for k, t, pp, ee in identical_titles:
            print(f"  * {k}: '{t}' at pt:{pp} <> en:{ee}")
    else:
        print("- Titles: OK (differ per language)")

    if same_slug:
        print("- Same slug in both languages (check if intended):")
        for k, s, pp, ee in same_slug:
            print(f"  * {k}: slug='{s}' at pt:{pp} <> en:{ee}")
    else:
        print("- Slugs: OK (distinct or unset)")

    return 0


if __name__ == "__main__":
    sys.exit(main())

