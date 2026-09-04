#!/usr/bin/env python3
"""Build Amir Salarpour's zero-dependency academic website.

The source of truth lives in /data. This script validates the data and writes
plain HTML files that can be hosted directly on GitHub Pages.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Could not read {path.relative_to(ROOT)}: {exc}") from exc


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def is_valid_link(value: str) -> bool:
    if not value:
        return True
    if value.startswith(("/", "mailto:", "#")):
        return True
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def type_key(value: str) -> str:
    value = value.lower()
    if "preprint" in value or "arxiv" in value:
        return "preprint"
    if "journal" in value:
        return "journal"
    if "workshop" in value:
        return "workshop"
    if "book" in value:
        return "book"
    if "online" in value:
        return "online"
    return "conference"


def load_data() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    site = load_json(DATA / "site.json")
    profile = load_json(DATA / "profile.json")
    research = load_json(DATA / "research.json")
    projects = load_json(DATA / "projects.json")
    news = load_json(DATA / "news.json")
    teaching = load_json(DATA / "teaching.json")
    service = load_json(DATA / "service.json")
    publications = [load_json(path) for path in sorted((DATA / "publications").glob("*.json")) if not path.name.startswith("_")]
    return site, profile, research, projects, news, teaching, service, publications


def validate(
    site: dict[str, Any],
    profile: dict[str, Any],
    research: dict[str, Any],
    projects: list[dict[str, Any]],
    news: list[dict[str, Any]],
    teaching: dict[str, Any],
    service: dict[str, Any],
    publications: list[dict[str, Any]],
) -> None:
    errors: list[str] = []

    for field in ("site_url", "title", "description"):
        if not site.get(field):
            errors.append(f"site.json is missing '{field}'")

    for field in ("name", "role", "affiliation", "tagline", "intro", "links"):
        if not profile.get(field):
            errors.append(f"profile.json is missing '{field}'")

    social_ids: set[str] = set()
    for link in profile.get("links", []):
        for field in ("id", "label", "url"):
            if not link.get(field):
                errors.append(f"profile link is missing '{field}': {link!r}")
        if link.get("id") in social_ids:
            errors.append(f"duplicate profile link id: {link.get('id')}")
        social_ids.add(link.get("id", ""))
        if not is_valid_link(link.get("url", "")):
            errors.append(f"invalid profile URL: {link.get('url')}")

    required_social = {"scholar", "github", "linkedin", "email", "cv"}
    missing_social = required_social - social_ids
    if missing_social:
        errors.append(f"profile links missing: {', '.join(sorted(missing_social))}")

    pub_ids: set[str] = set()
    for pub in publications:
        pid = pub.get("id", "")
        if not pid:
            errors.append(f"publication missing id: {pub.get('title', '(untitled)')}")
        if pid in pub_ids:
            errors.append(f"duplicate publication id: {pid}")
        pub_ids.add(pid)
        for field in ("title", "authors", "year", "venue_short", "venue", "type", "links"):
            if field not in pub or pub[field] in (None, "", []):
                # Links may legitimately be empty.
                if field != "links":
                    errors.append(f"publication '{pid}' is missing '{field}'")
        if not isinstance(pub.get("year"), int) or not (1900 <= pub.get("year", 0) <= 2100):
            errors.append(f"publication '{pid}' has an invalid year")
        if not isinstance(pub.get("authors"), list) or not pub.get("authors"):
            errors.append(f"publication '{pid}' must have an author list")
        for label, value in pub.get("links", {}).items():
            if value and not is_valid_link(value):
                errors.append(f"publication '{pid}' has invalid {label} URL: {value}")
        image = pub.get("image", "")
        if image and image.startswith("/") and not (ROOT / image.lstrip("/")).exists():
            errors.append(f"publication '{pid}' image does not exist: {image}")

    for field in ("home_publication_limit", "home_news_limit", "home_project_limit"):
        value = site.get(field, 4)
        if type(value) is not int or value < 0:
            errors.append(f"site.json '{field}' must be a nonnegative integer")
    project_ids: set[str] = set()
    for project in projects:
        pid = project.get("id", "")
        if not pid or pid in project_ids:
            errors.append(f"missing or duplicate project id: {pid}")
        project_ids.add(pid)
        for field in ("title", "summary"):
            if not project.get(field):
                errors.append(f"project '{pid}' is missing '{field}'")
        links = project.get("links", [])
        urls = links.values() if isinstance(links, dict) else [x.get("url", "") for x in links]
        for url in urls:
            if url and not is_valid_link(url):
                errors.append(f"project '{pid}' has an invalid URL: {url}")
    for item in news:
        if item.get("publication") and item["publication"] not in pub_ids:
            errors.append(f"news item references unknown publication: {item['publication']}")
        for pid in item.get("publications", []):
            if pid not in pub_ids:
                errors.append(f"news item references unknown publication: {pid}")
        if item.get("project") and item["project"] not in project_ids:
            errors.append(f"news item references unknown project: {item['project']}")

    if not research.get("themes"):
        errors.append("research.json must contain themes")
    if not teaching.get("current"):
        errors.append("teaching.json must contain current courses")
    if not service.get("conference_reviewing"):
        errors.append("service.json must contain conference_reviewing")

    if errors:
        print("Data validation failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        raise SystemExit(1)


ICONS: dict[str, str] = {
    "scholar": '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M3 9.5 12 4l9 5.5-9 5.5L3 9.5Z"/><path d="M6.5 12v4.2c2.8 2.4 8.2 2.4 11 0V12"/><path d="M21 10v6"/></svg>',
    "github": '<svg aria-hidden="true" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.5a9.7 9.7 0 0 0-3.1 18.9c.5.1.7-.2.7-.5v-1.9c-2.8.6-3.4-1.2-3.4-1.2-.5-1.2-1.1-1.5-1.1-1.5-.9-.6.1-.6.1-.6 1 0 1.6 1 1.6 1 .9 1.6 2.4 1.1 3 .9.1-.7.4-1.1.7-1.4-2.3-.3-4.6-1.1-4.6-5 0-1.1.4-2 1-2.7-.1-.3-.4-1.3.1-2.7 0 0 .8-.3 2.7 1a9.3 9.3 0 0 1 4.9 0c1.9-1.3 2.7-1 2.7-1 .5 1.4.2 2.4.1 2.7.6.7 1 1.6 1 2.7 0 3.9-2.4 4.7-4.7 5 .4.3.7 1 .7 1.9v2.9c0 .3.2.6.7.5A9.7 9.7 0 0 0 12 2.5Z"/></svg>',
    "linkedin": '<svg aria-hidden="true" viewBox="0 0 24 24" fill="currentColor"><path d="M5.2 7.7A2.2 2.2 0 1 0 5.2 3.3a2.2 2.2 0 0 0 0 4.4ZM3.4 20.6H7V9H3.4v11.6ZM9.3 9h3.4v1.6h.1c.5-.9 1.6-2 3.4-2 3.7 0 4.4 2.4 4.4 5.6v6.4H17v-5.7c0-1.4 0-3.1-1.9-3.1s-2.2 1.5-2.2 3v5.8H9.3V9Z"/></svg>',
    "email": '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m4.5 7 7.5 6 7.5-6"/></svg>',
    "cv": '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M7 3h7l4 4v14H7V3Z"/><path d="M14 3v5h5M10 12h5M10 16h5"/></svg>',
    "sun": '<svg class="theme-icon theme-icon-sun" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="3.5"/><path d="M12 2v2.2M12 19.8V22M4.9 4.9l1.6 1.6M17.5 17.5l1.6 1.6M2 12h2.2M19.8 12H22M4.9 19.1l1.6-1.6M17.5 6.5l1.6-1.6"/></svg>',
    "moon": '<svg class="theme-icon theme-icon-moon" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M20 15.2A8.2 8.2 0 0 1 8.8 4 8.5 8.5 0 1 0 20 15.2Z"/></svg>',
    "menu": '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
    "arrow": '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "external": '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 5h5v5M19 5l-9 9"/><path d="M19 13v6H5V5h6"/></svg>',
    "award": '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="8" r="5"/><path d="m8.5 12-1 9 4.5-2.5 4.5 2.5-1-9"/></svg>',
}


def icon(name: str) -> str:
    return ICONS.get(name, ICONS["external"])


def link_attrs(url: str) -> str:
    if url.startswith(("http://", "https://")):
        return ' target="_blank" rel="noopener noreferrer"'
    return ""


def best_publication_url(pub: dict[str, Any]) -> str:
    links = pub.get("links", {})
    return links.get("paper") or links.get("doi") or links.get("pdf") or links.get("project") or ""


def render_author_list(authors: list[str]) -> str:
    rendered = []
    for author in authors:
        name = esc(author)
        rendered.append(f"<strong>{name}</strong>" if author.strip() == "Amir Salarpour" else name)
    return ", ".join(rendered)


def render_profile_links(profile: dict[str, Any], *, footer: bool = False) -> str:
    links = []
    for item in profile["links"]:
        url = item["url"]
        label = esc(item["label"])
        if footer:
            footer_label = esc(item.get("display", item["label"]))
            links.append(f'<a href="{esc(url)}"{link_attrs(url)}>{footer_label}</a>')
        else:
            links.append(
                f'<a class="profile-link" href="{esc(url)}"{link_attrs(url)}>'
                f'{icon(item["id"])}<span>{label}</span></a>'
            )
    cls = "footer-links" if footer else "profile-links"
    return f'<div class="{cls}" aria-label="Professional links">{"".join(links)}</div>'


def nav_html(active: str, profile: dict[str, Any]) -> str:
    items = [
        ("research", "/research/", "Research"),
        ("publications", "/publications/", "Publications"),
        ("teaching", "/teaching/", "Teaching"),
        ("service", "/service/", "Service"),
        ("news", "/news/", "News"),
    ]
    links = []
    for key, href, label in items:
        current = ' aria-current="page"' if active == key else ""
        links.append(f'<a href="{href}"{current}>{label}</a>')
    cv = next((x["url"] for x in profile["links"] if x["id"] == "cv"), "")
    if cv:
        links.append(f'<a class="nav-cv" href="{esc(cv)}"{link_attrs(cv)}>CV</a>')
    return "".join(links)


def header_html(active: str, profile: dict[str, Any]) -> str:
    return f"""
<header class="site-header">
  <div class="container header-inner">
    <a class="site-brand" href="/" aria-label="{esc(profile['name'])} home">{esc(profile['name'])}</a>
    <div class="header-actions">
      <nav id="site-navigation" class="site-nav" data-site-nav data-open="false" aria-label="Primary navigation">
        {nav_html(active, profile)}
      </nav>
      <button class="icon-button" type="button" data-theme-toggle aria-label="Use dark theme" title="Use dark theme">
        {icon('sun')}{icon('moon')}
      </button>
      <button class="icon-button nav-toggle" type="button" data-nav-toggle aria-expanded="false" aria-controls="site-navigation" aria-label="Open menu">
        {icon('menu')}
      </button>
    </div>
  </div>
</header>"""


def footer_html(profile: dict[str, Any]) -> str:
    return f"""
<footer class="site-footer">
  <div class="container">
    <div class="footer-main">
      <div>
        <p class="footer-name">{esc(profile['name'])}</p>
        <p class="footer-note">{esc(profile['tagline'])} · {esc(profile['affiliation'])}</p>
      </div>
      {render_profile_links(profile, footer=True)}
    </div>
    <div class="footer-bottom">
      <span>© <span data-current-year>{datetime.now().year}</span> {esc(profile['name'])}</span>
      <span>{esc(profile['location'])}</span>
    </div>
  </div>
</footer>"""


def json_ld(site: dict[str, Any], profile: dict[str, Any]) -> str:
    same_as = [x["url"] for x in profile["links"] if x["id"] in {"scholar", "github", "linkedin"}]
    email = next((x["url"].removeprefix("mailto:") for x in profile["links"] if x["id"] == "email"), "")
    data = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": profile["name"],
        "url": site["site_url"] + "/",
        "image": site["site_url"] + "/assets/images/profile-640.jpg",
        "jobTitle": profile["role"],
        "affiliation": {"@type": "Organization", "name": profile["affiliation"]},
        "email": email,
        "sameAs": same_as,
        "knowsAbout": [
            "Autonomous vehicle perception",
            "Adversarial machine learning",
            "Vision-language models",
            "3D computer vision",
            "Point clouds",
        ],
    }
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def page_shell(
    *,
    site: dict[str, Any],
    profile: dict[str, Any],
    title: str,
    description: str,
    path: str,
    active: str,
    body: str,
    extra_script: str = "",
    preload_profile: bool = False,
) -> str:
    canonical = site["site_url"].rstrip("/") + path
    full_title = site["title"] if title == site["title"] else f"{title} · {site['title']}"
    preload = '<link rel="preload" as="image" href="/assets/images/profile-320.webp" type="image/webp">' if preload_profile else ""
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{esc(description)}">
  <meta name="author" content="{esc(profile['name'])}">
  <meta name="theme-color" media="(prefers-color-scheme: light)" content="#fdfdfc">
  <meta name="theme-color" media="(prefers-color-scheme: dark)" content="#121416">
  <title>{esc(full_title)}</title>
  <link rel="canonical" href="{esc(canonical)}">
  <link rel="icon" href="/assets/images/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/assets/images/favicon-32.png" sizes="32x32">
  <link rel="apple-touch-icon" href="/assets/images/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{esc(full_title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:url" content="{esc(canonical)}">
  <meta property="og:image" content="{esc(site['site_url'])}/assets/images/profile-640.jpg">
  <meta name="twitter:card" content="summary">
  {preload}
  <script>(function(){{document.documentElement.classList.add('js');try{{var t=localStorage.getItem('site-theme');if(t==='dark'||(!t&&window.matchMedia&&window.matchMedia('(prefers-color-scheme: dark)').matches))document.documentElement.dataset.theme='dark';}}catch(e){{}}}})();</script>
  <link rel="stylesheet" href="/assets/css/main.css">
  <script type="application/ld+json">{json_ld(site, profile)}</script>
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to content</a>
  {header_html(active, profile)}
  {body}
  {footer_html(profile)}
  <script src="/assets/js/site.js" defer></script>
  {extra_script}
</body>
</html>
"""


def text_link(href: str, label: str) -> str:
    return f'<a class="text-link" href="{esc(href)}"><span>{esc(label)}</span>{icon("arrow")}</a>'


def picture_html(src: str, alt: str, cls: str, *, width: int | None = None, height: int | None = None, eager: bool = False) -> str:
    if not src:
        return ""
    dimensions = f' width="{width}" height="{height}"' if width and height else ""
    loading = ' loading="eager" fetchpriority="high"' if eager else ' loading="lazy" decoding="async"'
    if src.lower().endswith(".webp"):
        jpg = re.sub(r"\.webp$", ".jpg", src, flags=re.I)
        jpg_exists = (ROOT / jpg.lstrip("/")).exists() if jpg.startswith("/") else False
        fallback = jpg if jpg_exists else src
        return (
            f'<picture><source srcset="{esc(src)}" type="image/webp">'
            f'<img class="{esc(cls)}" src="{esc(fallback)}" alt="{esc(alt)}"{dimensions}{loading}></picture>'
        )
    return f'<img class="{esc(cls)}" src="{esc(src)}" alt="{esc(alt)}"{dimensions}{loading}>'


def publication_links_html(pub: dict[str, Any]) -> str:
    labels = [
        ("paper", "Paper"),
        ("pdf", "PDF"),
        ("code", "Code"),
        ("project", "Project"),
        ("doi", "DOI"),
        ("bibtex", "BibTeX"),
    ]
    links = pub.get("links", {})
    output: list[str] = []
    seen: set[str] = set()
    for key, label in labels:
        url = links.get(key, "")
        if not url or url in seen:
            continue
        seen.add(url)
        download = ' download' if key == "bibtex" and url.startswith("/") else ""
        output.append(
            f'<a class="pub-link" href="{esc(url)}"{link_attrs(url)}{download}>'
            f'<span>{label}</span>{icon("external") if url.startswith("http") else ""}</a>'
        )
    return f'<div class="publication-links">{"".join(output)}</div>' if output else ""


def publication_html(pub: dict[str, Any], *, compact: bool = False) -> str:
    href = best_publication_url(pub)
    title = esc(pub["title"])
    title_html = f'<a href="{esc(href)}"{link_attrs(href)}>{title}</a>' if href else title
    image = "" if compact else pub.get("image", "")
    image_html = ""
    classes = ["publication"]
    if compact:
        classes.append("publication-compact")
    if image:
        classes.append("has-image")
        pic = picture_html(image, f"Representative figure for {pub['title']}", "publication-thumb")
        if href:
            pic = f'<a class="publication-thumb-link" href="{esc(href)}"{link_attrs(href)}>{pic}</a>'
        else:
            pic = f'<div class="publication-thumb-link">{pic}</div>'
        image_html = pic

    status = pub.get("status", "")
    status_html = f'<span class="pub-dot">{esc(status)}</span>' if status == "Accepted" else ""
    award = pub.get("award", "")
    award_html = f'<div class="pub-award">{icon("award")}<span>{esc(award)}</span></div>' if award else ""
    topics = "" if compact else "".join(f'<span class="topic">{esc(topic)}</span>' for topic in pub.get("topics", []))
    topics_html = f'<div class="topic-list" aria-label="Topics">{topics}</div>' if topics else ""
    links_html = publication_links_html(pub)
    search_text = " ".join([pub["title"], " ".join(pub["authors"]), pub["venue"], " ".join(pub.get("topics", []))])
    data_attrs = (
        f' data-publication data-year="{pub["year"]}" data-type="{type_key(pub["type"])}"'
        f' data-search="{esc(search_text)}"'
    )
    return f"""
<article class="{' '.join(classes)}"{data_attrs}>
  {image_html}
  <div class="publication-body">
    <div class="pub-meta"><span class="venue-badge">{esc(pub['venue_short'])}</span><span>{pub['year']}</span><span class="pub-dot">{esc(pub['type'])}</span>{status_html}</div>
    <h3>{title_html}</h3>
    <p class="pub-authors">{render_author_list(pub['authors'])}</p>
    <p class="pub-venue">{esc(pub['venue'])}</p>
    {award_html}{topics_html}{links_html}
  </div>
</article>"""


def project_html(project: dict[str, Any]) -> str:
    topics = " · ".join(project.get("topics", []))
    facts = "".join(
        f"<div><dt>{label}</dt><dd>{esc(project.get(key, ''))}</dd></div>"
        for key, label in (("period", "Period"), ("sponsor", "Sponsor"), ("role", "Role"))
        if project.get(key)
    )
    raw_links = project.get("links", [])
    if isinstance(raw_links, dict):
        raw_links = [{"label": key.title(), "url": value} for key, value in raw_links.items() if value]
    links = "".join(f'<a href="{esc(x["url"])}"{link_attrs(x["url"])}>{esc(x["label"])}</a>' for x in raw_links if x.get("url"))
    links_html = f'<div class="project-links">{links}</div>' if links else ""
    return f"""
<article class="project-card" id="project-{esc(project['id'])}">
  <div>
    <span class="project-status">{esc(project.get('status', ''))}</span>
    <h3>{esc(project['title'])}</h3>
    <p>{esc(project['summary'])}</p>
    <p class="keyword-line">{esc(topics)}</p>
    {links_html}
  </div>
  <dl class="project-facts">{facts}</dl>
</article>"""


def render_news_item(item: dict[str, Any], pub_by_id: dict[str, dict[str, Any]]) -> str:
    text = esc(item["text"])
    related = ""
    if item.get("publication"):
        pub = pub_by_id[item["publication"]]
        title = pub["title"]
        href = best_publication_url(pub)
        link_text = item.get("link_text", title)
        if href and link_text in item["text"]:
            linked = f'<a href="{esc(href)}"{link_attrs(href)}>{esc(link_text)}</a>'
            text = text.replace(esc(link_text), linked, 1)
        elif href:
            related = f'<p class="news-related"><a href="{esc(href)}"{link_attrs(href)}>Paper</a></p>' 
    if item.get("publications"):
        entries = []
        for pid in item["publications"]:
            pub = pub_by_id[pid]
            href = best_publication_url(pub)
            title = esc(pub["title"])
            title_html = f'<a href="{esc(href)}"{link_attrs(href)}>{title}</a>' if href else title
            entries.append(f"<li>{title_html}</li>")
        related = f'<ul class="clean-list news-papers">{"".join(entries)}</ul>'
    return f"""
<article class="news-item">
  <time class="news-date" datetime="{esc(item['date'])}">{esc(item['label'])}</time>
  <div class="news-content"><p>{text}</p>{related}<div class="news-kind">{esc(item['kind'])}</div></div>
</article>"""


def page_hero(title: str, lead: str, eyebrow: str = "") -> str:
    eyebrow_html = f'<p class="eyebrow">{esc(eyebrow)}</p>' if eyebrow else ""
    return f"""
<section class="page-hero">
  <div class="container">
    {eyebrow_html}<h1>{esc(title)}</h1>
    <p class="page-lead">{esc(lead)}</p>
  </div>
</section>"""


def home_page(site: dict[str, Any], profile: dict[str, Any], research: dict[str, Any], projects: list[dict[str, Any]], news: list[dict[str, Any]], publications: list[dict[str, Any]]) -> str:
    featured = sorted([p for p in publications if p.get("featured")], key=lambda p: (-p["year"], p.get("order", 999)))[:site.get("home_publication_limit", 6)]
    pub_by_id = {p["id"]: p for p in publications}
    theme_cards = "".join(
        f"""
<article class="focus-item">
  <h3>{esc(theme['title'])}</h3>
  <p>{esc(theme['description'])}</p>
</article>"""
        for theme in research["themes"]
    )
    pub_items = "".join(publication_html(pub, compact=True) for pub in featured)
    news_items = "".join(render_news_item(item, pub_by_id) for item in sorted(news, key=lambda n: n["date"], reverse=True)[:site.get("home_news_limit", 4)])
    featured_projects = [p for p in projects if p.get("featured", False)][:site.get("home_project_limit", 2)]
    projects_section = ""
    if featured_projects:
        projects_section = f'''<section class="section section-soft" id="projects">
    <div class="container">
      <div class="section-heading"><div><h2>Selected projects</h2></div>{text_link('/research/#projects', 'All projects')}</div>
      {"".join(project_html(p) for p in featured_projects)}
    </div>
  </section>'''
    body = f"""
<main id="main-content">
  <section class="hero">
    <div class="container hero-grid">
      <div class="hero-identity">
        <h1>{esc(profile['name'])}</h1>
        <p class="hero-role">{esc(profile['role'])}</p>
        <p class="hero-affiliation">{esc(profile['affiliation'])} · {esc(profile['lab'])}</p>
      </div>
      <div class="hero-photo">
        <div class="profile-photo-wrap">
          <picture>
            <source srcset="/assets/images/profile-320.webp 320w, /assets/images/profile-640.webp 640w" sizes="(max-width: 680px) 94px, 178px" type="image/webp">
            <img class="profile-photo" src="/assets/images/profile-640.jpg" srcset="/assets/images/profile-320.jpg 320w, /assets/images/profile-640.jpg 640w" sizes="(max-width: 680px) 94px, 178px" width="640" height="640" alt="{esc(profile['photo_alt'])}" loading="eager" fetchpriority="high">
          </picture>
        </div>
      </div>
      <p class="hero-intro">{esc(profile['intro'])}</p>
      {render_profile_links(profile)}
    </div>
  </section>

  <section class="section section-soft" id="research">
    <div class="container">
      <div class="section-heading">
        <div><h2>Research focus</h2></div>
        {text_link('/research/', 'Research overview')}
      </div>
      <div class="focus-grid">{theme_cards}</div>
    </div>
  </section>

  <section class="section" id="selected-publications">
    <div class="container">
      <div class="section-heading">
        <div><h2>Selected publications</h2></div>
        {text_link('/publications/', 'All publications')}
      </div>
      <div class="publication-list">{pub_items}</div>
    </div>
  </section>

  {projects_section}

  <section class="section" id="news">
    <div class="container">
      <div class="section-heading"><div><h2>Recent news</h2></div>{text_link('/news/', 'All news')}</div>
      <div class="news-list home-news">{news_items}</div>
    </div>
  </section>
</main>"""
    return page_shell(site=site, profile=profile, title=site["title"], description=site["description"], path="/", active="home", body=body, preload_profile=True)


def research_page(site: dict[str, Any], profile: dict[str, Any], research: dict[str, Any], projects: list[dict[str, Any]]) -> str:
    cards = "".join(
        f"""
<article class="theme-card" id="{esc(theme['id'])}">
  <span class="theme-number">0{i}</span><h3>{esc(theme['title'])}</h3><p>{esc(theme['description'])}</p>
  <div class="keyword-line">{esc(' · '.join(theme['keywords']))}</div>
</article>"""
        for i, theme in enumerate(research["themes"], 1)
    )
    bios = "".join(f"<p>{esc(paragraph)}</p>" for paragraph in profile["bio"])
    projects_html = "".join(project_html(project) for project in projects)
    sidebar = "".join(f'<a href="#{esc(t["id"])}">{esc(t["title"])}</a>' for t in research["themes"])
    body = f"""
<main id="main-content">
  {page_hero('Research', research['statement'], 'Research agenda')}
  <section class="page-content">
    <div class="container content-grid">
      <div>
        <div class="prose"><h2>Overview</h2>{bios}</div>
        <div class="theme-grid">{cards}</div>
        <section id="projects" class="section" style="padding-bottom:0">
          <div class="section-heading"><div><p class="eyebrow">Projects</p><h2>Active research</h2></div></div>
          {projects_html}
        </section>
      </div>
      <aside class="sidebar-block" aria-label="Research sections"><h2>Research areas</h2><nav class="sidebar-links">{sidebar}<a href="#projects">Projects</a></nav></aside>
    </div>
  </section>
</main>"""
    return page_shell(site=site, profile=profile, title="Research", description=research["statement"], path="/research/", active="research", body=body)


def publications_page(site: dict[str, Any], profile: dict[str, Any], publications: list[dict[str, Any]]) -> str:
    publications = sorted(publications, key=lambda p: (-p["year"], p.get("order", 999)))
    grouped: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for pub in publications:
        grouped[pub["year"]].append(pub)
    groups = []
    for year in sorted(grouped, reverse=True):
        items = "".join(publication_html(pub) for pub in grouped[year])
        groups.append(f'<section class="year-group" data-year-group><h2 class="year-heading">{year}</h2><div class="publication-list">{items}</div></section>')
    years = "".join(f'<option value="{year}">{year}</option>' for year in sorted(grouped, reverse=True))
    body = f"""
<main id="main-content">
  {page_hero('Publications', f"{len(publications)} publications spanning secure autonomous perception, vision-language models, 3D computer vision, and earlier work in signal processing and machine learning.", 'Research record')}
  <section class="page-content">
    <div class="container">
      <form class="filters" data-publication-filters role="search" aria-label="Filter publications">
        <div class="field"><label for="pub-search">Search</label><input id="pub-search" type="search" name="q" placeholder="Title, author, venue, or topic"></div>
        <div class="field"><label for="pub-type">Type</label><select id="pub-type" name="type"><option value="all">All types</option><option value="conference">Conference papers</option><option value="journal">Journal articles</option><option value="workshop">Workshop papers</option><option value="book">Book chapters</option><option value="preprint">Preprints</option><option value="online">Online articles</option></select></div>
        <div class="field"><label for="pub-year">Year</label><select id="pub-year" name="year"><option value="all">All years</option>{years}</select></div>
        <button class="filter-reset" type="button" data-filter-reset>Reset</button>
      </form>
      <p class="results-summary" data-results-summary aria-live="polite">{len(publications)} publications shown</p>
      <div data-publication-results>{''.join(groups)}</div>
      <div class="empty-results" data-empty-results>No publications match these filters.</div>
    </div>
  </section>
</main>"""
    return page_shell(site=site, profile=profile, title="Publications", description="Publications by Amir Salarpour in autonomous perception, adversarial machine learning, vision-language models, and 3D computer vision.", path="/publications/", active="publications", body=body, extra_script='<script src="/assets/js/publications.js" defer></script>')


def teaching_page(site: dict[str, Any], profile: dict[str, Any], teaching: dict[str, Any]) -> str:
    current = "".join(
        f"""
<article class="course-card"><div class="course-code">{esc(c['course'])}</div><div><h3>{esc(c['title'])}</h3><p>{esc(c['role'])} · {esc(c['institution'])} · {esc(c['term'])}</p></div></article>"""
        for c in teaching["current"]
    )
    grad = "".join(f"<li>{esc(x)}</li>" for x in teaching["prior"]["graduate"])
    under = "".join(f"<li>{esc(x)}</li>" for x in teaching["prior"]["undergraduate"])
    areas = "".join(f"<li>{esc(x)}</li>" for x in teaching["areas"])
    body = f"""
<main id="main-content">
  {page_hero('Teaching', teaching['intro'], 'Teaching and mentoring')}
  <section class="page-content"><div class="container">
    <div class="section-heading"><div><p class="eyebrow">Clemson University</p><h2>Courses taught</h2></div></div>
    <div class="course-list">{current}</div>
  </div></section>
  <section class="section section-soft"><div class="container">
    <div class="section-heading"><div><p class="eyebrow">Prior teaching</p><h2>{esc(teaching['prior']['institution'])}</h2><p>{esc(teaching['prior']['role'])}</p></div></div>
    <div class="two-column-list"><div class="list-block"><h3>Graduate courses</h3><ul class="clean-list">{grad}</ul></div><div class="list-block"><h3>Undergraduate courses</h3><ul class="clean-list">{under}</ul></div></div>
  </div></section>
  <section class="section"><div class="container"><div class="section-heading"><div><p class="eyebrow">Teaching areas</p><h2>Subjects</h2></div></div><div class="list-block"><ul class="clean-list">{areas}</ul></div></div></section>
</main>"""
    return page_shell(site=site, profile=profile, title="Teaching", description=teaching["intro"], path="/teaching/", active="teaching", body=body)


def service_page(site: dict[str, Any], profile: dict[str, Any], service: dict[str, Any]) -> str:
    conference_items = "".join(f'<div class="service-row"><div class="service-label">Reviewing</div><div><h3>{esc(item)}</h3></div></div>' for item in service["conference_reviewing"])
    journals = "".join(f"<li>{esc(j)}</li>" for j in service["journal_reviewing"]["journals"])
    leadership = "".join(f'<article class="leadership-row"><div class="service-label">{esc(x["period"])}</div><div><h3>{esc(x["role"])}</h3><p>{esc(x["institution"])}</p></div></article>' for x in service["leadership"])
    memberships = "".join(f"<li>{esc(m)}</li>" for m in service["memberships"])
    body = f"""
<main id="main-content">
  {page_hero('Service', service['intro'], 'Academic service')}
  <section class="page-content"><div class="container">
    <div class="section-heading"><div><p class="eyebrow">Program committees</p><h2>Conference reviewing</h2></div></div>
    <div class="service-list">{conference_items}</div>
  </div></section>
  <section class="section section-soft"><div class="container">
    <div class="section-heading"><div><p class="eyebrow">Peer review</p><h2>Journal reviewing</h2><p>{service['journal_reviewing']['verified_reviews']} verified reviews across leading venues in security, vision, intelligent systems, and signal processing.</p></div></div>
    <div class="list-block"><ul class="clean-list">{journals}</ul></div>
  </div></section>
  <section class="section"><div class="container"><div class="section-heading"><div><p class="eyebrow">Leadership</p><h2>Academic roles</h2></div></div><div class="leadership-list">{leadership}</div></div></section>
  <section class="section section-soft"><div class="container"><div class="section-heading"><div><p class="eyebrow">Professional community</p><h2>Memberships</h2></div></div><div class="list-block"><ul class="clean-list">{memberships}</ul></div></div></section>
</main>"""
    return page_shell(site=site, profile=profile, title="Service", description=service["intro"], path="/service/", active="service", body=body)


def news_page(site: dict[str, Any], profile: dict[str, Any], news: list[dict[str, Any]], publications: list[dict[str, Any]]) -> str:
    pub_by_id = {p["id"]: p for p in publications}
    items = "".join(render_news_item(item, pub_by_id) for item in sorted(news, key=lambda n: n["date"], reverse=True))
    body = f"""
<main id="main-content">
  {page_hero('News', 'Selected publication, award, and project updates.', 'Recent updates')}
  <section class="page-content"><div class="container reading-width"><div class="news-list">{items}</div></div></section>
</main>"""
    return page_shell(site=site, profile=profile, title="News", description="Recent publication, award, and project news from Amir Salarpour.", path="/news/", active="news", body=body)


def error_page(site: dict[str, Any], profile: dict[str, Any]) -> str:
    body = f"""
<main id="main-content" class="error-page"><div class="container"><p class="error-code">404</p><h1>Page not found</h1><p>The page may have moved, or the address may be incorrect.</p><a class="button" href="/">Return home</a></div></main>"""
    return page_shell(site=site, profile=profile, title="Page not found", description="Page not found.", path="/404.html", active="", body=body)


def write_page(output: Path, relative: str, content: str) -> None:
    path = output / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build(output: Path) -> None:
    site, profile, research, projects, news, teaching, service, publications = load_data()
    validate(site, profile, research, projects, news, teaching, service, publications)

    output = output.resolve()
    if output != ROOT.resolve():
        if output in ROOT.resolve().parents or output == DATA.resolve() or output == (ROOT / "assets").resolve():
            raise SystemExit(f"Refusing unsafe output directory: {output}")
        marker = output / ".academic-site-build-output"
        if output.exists() and any(output.iterdir()) and not marker.is_file():
            raise SystemExit(f"Output directory is not a previous site build: {output}. Choose a new empty directory.")
        if output.exists():
            shutil.rmtree(output)
        output.mkdir(parents=True)
        marker.write_text("Generated output; safe for rebuild\n", encoding="utf-8")
        shutil.copytree(ROOT / "assets", output / "assets")
    else:
        output.mkdir(parents=True, exist_ok=True)

    pages = {
        "index.html": home_page(site, profile, research, projects, news, publications),
        "research/index.html": research_page(site, profile, research, projects),
        "publications/index.html": publications_page(site, profile, publications),
        "teaching/index.html": teaching_page(site, profile, teaching),
        "service/index.html": service_page(site, profile, service),
        "news/index.html": news_page(site, profile, news, publications),
        "404.html": error_page(site, profile),
    }
    for path, content in pages.items():
        write_page(output, path, content)

    site_url = site["site_url"].rstrip("/")
    paths = ["/", "/research/", "/publications/", "/teaching/", "/service/", "/news/"]
    now = datetime.now(timezone.utc).date().isoformat()
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f"  <url><loc>{site_url}{path}</loc><lastmod>{now}</lastmod></url>\n" for path in paths
    ) + "</urlset>\n"
    write_page(output, "sitemap.xml", sitemap)
    write_page(output, "robots.txt", f"User-agent: *\nAllow: /\nSitemap: {site_url}/sitemap.xml\n")
    manifest = {
        "name": profile["name"],
        "short_name": profile["name"],
        "start_url": "/",
        "display": "standalone",
        "background_color": "#fdfdfc",
        "theme_color": "#fdfdfc",
        "icons": [
            {"src": "/assets/images/icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "/assets/images/icon-512.png", "sizes": "512x512", "type": "image/png"},
        ],
    }
    write_page(output, "site.webmanifest", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    write_page(output, ".nojekyll", "")

    print(f"Built {len(pages)} pages and {len(publications)} publication records into {output}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT, help="Output directory (default: project root)")
    args = parser.parse_args()
    build(args.output)


if __name__ == "__main__":
    main()
