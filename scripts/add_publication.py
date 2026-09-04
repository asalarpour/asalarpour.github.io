#!/usr/bin/env python3
"""Interactively add a publication record and rebuild the site."""
from __future__ import annotations

import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLICATIONS = ROOT / "data" / "publications"


def ask(label: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{label}{suffix}: ").strip()
    return value or default


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")[:110].rstrip("-")


def main() -> None:
    print("Add a publication. Leave optional fields blank.\n")
    title = ask("Title")
    if not title:
        raise SystemExit("Title is required.")
    authors = [x.strip() for x in ask("Authors, separated by commas").split(",") if x.strip()]
    if not authors:
        raise SystemExit("At least one author is required.")
    try:
        year = int(ask("Year"))
    except ValueError as exc:
        raise SystemExit("Year must be a number.") from exc
    venue_short = ask("Short venue name (e.g., CVPR, T-PAMI)")
    venue = ask("Full venue citation")
    publication_type = ask("Type", "Conference paper")
    status = ask("Status", "Published")
    featured = ask("Show on homepage? (y/n)", "n").lower().startswith("y")
    topics = [x.strip() for x in ask("Topics, separated by commas").split(",") if x.strip()]

    links = {}
    for key, label in (
        ("paper", "Paper/page URL"),
        ("pdf", "Direct PDF URL"),
        ("code", "Code URL"),
        ("project", "Project URL"),
        ("doi", "DOI URL"),
        ("bibtex", "BibTeX URL/path"),
    ):
        value = ask(label)
        if value:
            links[key] = value

    pub_id = slugify(title)
    existing = [json.loads(path.read_text(encoding="utf-8")) for path in PUBLICATIONS.glob("*.json") if not path.name.startswith("_")]
    if any(item.get("id") == pub_id for item in existing):
        raise SystemExit(f"A publication with id '{pub_id}' already exists.")

    order = max((int(item.get("order", 0)) for item in existing), default=0) + 1
    record = {
        "id": pub_id,
        "title": title,
        "authors": authors,
        "year": year,
        "venue_short": venue_short,
        "venue": venue,
        "type": publication_type,
        "status": status,
        "featured": featured,
        "order": order,
        "topics": topics,
        "note": "",
        "award": "",
        "image": "",
        "links": links,
    }
    output = PUBLICATIONS / f"{year}-{pub_id}.json"
    output.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\nCreated {output.relative_to(ROOT)}")
    subprocess.run([sys.executable, str(ROOT / "scripts" / "build_site.py")], cwd=ROOT, check=True)
    print("Site rebuilt successfully.")


if __name__ == "__main__":
    main()
