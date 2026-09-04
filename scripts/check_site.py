#!/usr/bin/env python3
"""Run structural checks on the generated static website."""
from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.links: list[tuple[str, str]] = []
        self.images: list[dict[str, str]] = []
        self.has_title = False
        self.h1_count = 0
        self.has_viewport = False
        self.html_lang = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {key: value or "" for key, value in attrs}
        if "id" in data:
            self.ids.add(data["id"])
        if tag == "html":
            self.html_lang = data.get("lang", "")
        elif tag == "title":
            self.has_title = True
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "meta" and data.get("name") == "viewport":
            self.has_viewport = True
        elif tag in {"a", "link"} and data.get("href"):
            self.links.append(("href", data["href"]))
        elif tag in {"script", "img"} and data.get("src"):
            self.links.append(("src", data["src"]))
        if tag == "img":
            self.images.append(data)
        if data.get("srcset"):
            for part in data["srcset"].split(","):
                url = part.strip().split()[0] if part.strip() else ""
                if url:
                    self.links.append(("srcset", url))


def target_for(site: Path, current: Path, url: str) -> tuple[Path | None, str]:
    parsed = urlparse(url)
    if parsed.scheme or url.startswith(("mailto:", "tel:", "data:")):
        return None, parsed.fragment
    path_text = unquote(parsed.path)
    if not path_text:
        return current, parsed.fragment
    if path_text.startswith("/"):
        target = site / path_text.lstrip("/")
    else:
        target = current.parent / path_text
    if path_text.endswith("/"):
        target = target / "index.html"
    elif target.is_dir():
        target = target / "index.html"
    return target.resolve(), parsed.fragment


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    site = args.site.resolve()
    errors: list[str] = []
    parsed_pages: dict[Path, PageParser] = {}

    html_files = sorted(site.rglob("*.html"))
    if not html_files:
        raise SystemExit(f"No HTML files found in {site}")

    for page in html_files:
        p = PageParser()
        p.feed(page.read_text(encoding="utf-8"))
        parsed_pages[page.resolve()] = p
        rel = page.relative_to(site)
        if not p.html_lang:
            errors.append(f"{rel}: missing html lang attribute")
        if not p.has_title:
            errors.append(f"{rel}: missing title")
        if p.h1_count != 1:
            errors.append(f"{rel}: expected exactly one h1, found {p.h1_count}")
        if not p.has_viewport:
            errors.append(f"{rel}: missing viewport meta tag")
        for image in p.images:
            if not image.get("alt"):
                errors.append(f"{rel}: image missing alt text ({image.get('src', '')})")
            if image.get("loading") == "lazy" and not image.get("decoding"):
                errors.append(f"{rel}: lazy image missing decoding attribute ({image.get('src', '')})")

    for page, p in parsed_pages.items():
        rel = page.relative_to(site)
        for kind, url in p.links:
            target, fragment = target_for(site, page, url)
            if target is None:
                continue
            if not target.exists():
                errors.append(f"{rel}: broken local {kind} '{url}'")
                continue
            if fragment and target.suffix.lower() == ".html":
                target_parser = parsed_pages.get(target)
                if target_parser is None:
                    target_parser = PageParser()
                    target_parser.feed(target.read_text(encoding="utf-8"))
                    parsed_pages[target] = target_parser
                if fragment not in target_parser.ids:
                    errors.append(f"{rel}: missing fragment '#{fragment}' in '{url}'")

    # Lightweight checks for accidental placeholders and unsafe blank tabs.
    for page in html_files:
        text = page.read_text(encoding="utf-8")
        rel = page.relative_to(site)
        if re.search(r'href=["\']\s*["\']', text):
            errors.append(f"{rel}: empty href found")
        if 'target="_blank"' in text and 'rel="noopener noreferrer"' not in text:
            errors.append(f"{rel}: target=_blank found without expected rel protection")

    if errors:
        print(f"Site checks failed with {len(errors)} issue(s):", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        raise SystemExit(1)

    print(f"Site checks passed: {len(html_files)} HTML pages, no broken local links, and all images have alt text.")


if __name__ == "__main__":
    main()
