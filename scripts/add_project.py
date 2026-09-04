#!/usr/bin/env python3
"""Interactively add a project and rebuild the site."""
from __future__ import annotations

import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECTS_FILE = ROOT / "data" / "projects.json"


def ask(label: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{label}{suffix}: ").strip()
    return value or default


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")[:90].rstrip("-")


def main() -> None:
    title = ask("Project title")
    if not title:
        raise SystemExit("Project title is required.")
    project = {
        "id": slugify(title),
        "title": title,
        "short_title": ask("Short title", title),
        "status": ask("Status", "Active"),
        "period": ask("Period (e.g., 2027–2030)"),
        "sponsor": ask("Sponsor"),
        "role": ask("Your role"),
        "summary": ask("One-paragraph summary"),
        "topics": [x.strip() for x in ask("Topics, separated by commas").split(",") if x.strip()],
        "featured": ask("Show prominently? (y/n)", "y").lower().startswith("y"),
        "links": [],
    }
    for label in ("Project website", "Code", "Dataset"):
        url = ask(f"{label} URL (optional)")
        if url:
            project["links"].append({"label": label, "url": url})
    projects = json.loads(PROJECTS_FILE.read_text(encoding="utf-8"))
    if any(item.get("id") == project["id"] for item in projects):
        raise SystemExit(f"A project with id '{project['id']}' already exists.")
    projects.append(project)
    PROJECTS_FILE.write_text(json.dumps(projects, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    subprocess.run([sys.executable, str(ROOT / "scripts" / "build_site.py")], cwd=ROOT, check=True)
    print("Project added and site rebuilt.")


if __name__ == "__main__":
    main()
