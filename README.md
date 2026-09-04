# Amir Salarpour — Academic Website (v3.1 reviewed)

A custom, zero-dependency academic website designed for long-term use on GitHub Pages.

## Main features

- Responsive layout for mobile, tablet, laptop, and desktop
- Light and dark themes
- Clear Google Scholar, GitHub, LinkedIn, email, and CV links
- Searchable and filterable publication list
- Structured JSON records for publications, news, projects, teaching, and service
- Automatic validation before deployment
- GitHub Pages deployment through GitHub Actions
- No external fonts, JavaScript frameworks, themes, trackers, or CDNs

## Local build

Python 3.10 or newer is sufficient. No package installation is required.

```bash
python3 scripts/build_site.py
python3 -m http.server 8000
```

Then open `http://localhost:8000`.

## Content locations

- Profile and professional links: `data/profile.json`
- Publications: `data/publications/*.json`
- News: `data/news.json`
- Projects: `data/projects.json`
- Research themes: `data/research.json`
- Teaching: `data/teaching.json`
- Service: `data/service.json`

Detailed Persian instructions are available in:

- `DEPLOY_FA.md`
- `HOW_TO_UPDATE_FA.md`
- `AUDIT_FA.md` — measured review results and test limitations
- `REVISION_NOTES_FA.md`
- `DESIGN_BENCHMARK_FA.md`

## License

Website code may be reused and modified for Amir Salarpour's personal academic website. Publication metadata and personal content remain the property of their respective authors and publishers.
