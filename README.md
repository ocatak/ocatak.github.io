# ozgurcatak.net

Personal academic website of **Ferhat Ozgur Catak**, Professor of Cyber Security at the University of Stavanger (UiS), Norway. Research areas: penetration testing and malware analysis, quantum technologies for security, and trustworthy AI.

Plain static HTML served by GitHub Pages from the `master` branch (custom domain in `CNAME`). No build step, no frameworks; the only script is Google Analytics.

## Structure

```
index.html                                 Home: intro, research areas, selected work, teaching
penetration-testing-malware-analysis.html  Research area 1 (incl. Mal-API-2019 dataset)
quantum-technologies-for-security.html     Research area 2 (incl. QuantumUQ)
trustworthy-ai.html                        Research area 3 (incl. book)
publications.html                          Full publication list (generated, see below)
software.html                              Research software and datasets
teaching.html                              Courses and supervision
about.html                                 Bio, career, talks, profiles, contact
404.html                                   Not-found page (used automatically by GitHub Pages)
research.html, projects.html,
talks.html, contact.html                   Redirects from the previous site's URLs
llms.txt                                   Plain-text profile for AI assistants (llmstxt.org)
robots.txt, sitemap.xml                    Crawler rules (AI crawlers explicitly allowed) and sitemap
assets/css/style.css                       The only stylesheet (light and dark mode)
assets/img/                                Portrait, book covers, Open Graph image, icons
tools/update_publications.py               Publication-list updater
```

## Updating

- **Publications:** `python3 tools/update_publications.py` fetches all works for OpenAlex author `A5044259885` (ORCID 0000-0002-2434-9966), rewrites the list between the `PUBLICATIONS` markers in `publications.html`, and bumps its `lastmod` in `sitemap.xml`. Hide an item by adding its DOI or title to `EXCLUDE`; add an item OpenAlex lacks to `EXTRA`.
- **Other pages:** edit the HTML directly. Each page carries JSON-LD structured data in its `<head>`; keep facts (title, counts, dates) consistent with the visible text and with `llms.txt`, and update the "Last updated" footer line and `dateModified`.
- **Deploy:** commit and push to `master`.
