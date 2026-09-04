#!/usr/bin/env python3
"""Interactively add a news item and rebuild the site."""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NEWS_FILE = ROOT / "data" / "news.json"


def ask(label: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{label}{suffix}: ").strip()
    return value or default


def main() -> None:
    today = date.today().isoformat()
    iso_date = ask("Date (YYYY-MM-DD)", today)
    label = ask("Display date (e.g., Sep 2026)")
    kind = ask("Category", "Update")
    text = ask("News text")
    if not text:
        raise SystemExit("News text is required.")

    items = json.loads(NEWS_FILE.read_text(encoding="utf-8"))
    items.append({"date": iso_date, "label": label, "kind": kind, "text": text})
    items.sort(key=lambda item: item["date"], reverse=True)
    NEWS_FILE.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    subprocess.run([sys.executable, str(ROOT / "scripts" / "build_site.py")], cwd=ROOT, check=True)
    print("News item added and site rebuilt.")


if __name__ == "__main__":
    main()
