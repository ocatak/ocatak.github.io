#!/usr/bin/env python3
"""Refresh the publication list in site/publications.html from OpenAlex.

Usage:  python3 tools/update_publications.py

It fetches every work linked to the OpenAlex author record for ORCID
0000-0002-2434-9966 and rewrites the block between
<!-- PUBLICATIONS:START --> and <!-- PUBLICATIONS:END --> as static HTML,
so search engines and AI crawlers can read it without running JavaScript.
Standard library only.

To hide an entry, add its DOI or exact title to EXCLUDE below.
"""
import html
import json
import re
import urllib.request
from collections import defaultdict
from datetime import date
from pathlib import Path

AUTHOR_ID = "A5044259885"          # OpenAlex author record (matched to the ORCID)
_ROOT = Path(__file__).resolve().parent.parent
# Works both in the Dropbox project (site/ subfolder) and in the GitHub Pages repo (site files at the root).
PAGE = (_ROOT / "site" / "publications.html") if (_ROOT / "site" / "publications.html").exists() else (_ROOT / "publications.html")
EXCLUDE = {
    # Proceedings volumes and records that are not authored papers
    "2023 IEEE Virtual Conference on Communications (VCC)",
    "Big Data Application in Power Systems 2nd Edition",
}
EXCLUDE_TYPES = {"dataset", "paratext", "erratum", "peer-review", "other"}
# Items OpenAlex does not index (added by hand). Same shape as an OpenAlex work.
EXTRA = [
    {"title": "Trustworthy AI: From Theory to Practice", "publication_year": 2024, "publication_date": "2024-03-01",
     "type": "book", "doi": None,
     "primary_location": {"landing_page_url": "https://digitalcommons.odu.edu/engtech_books/5/",
                          "source": {"display_name": "Old Dominion University Digital Commons"}},
     "authorships": [{"author": {"id": "https://openalex.org/" + "A5044259885", "display_name": "Ferhat Özgür Çatak"}},
                     {"author": {"id": None, "display_name": "Murat Kuzlu"}}]},
]
TYPE_LABEL = {"article": "Journal", "conference-paper": "Conference", "book-chapter": "Chapter",
              "preprint": "Preprint", "review": "Review", "book": "Book"}


def fetch():
    works, cursor = [], "*"
    while cursor:
        url = (f"https://api.openalex.org/works?filter=author.id:{AUTHOR_ID}"
               f"&per-page=200&cursor={cursor}")
        req = urllib.request.Request(url, headers={"User-Agent": "ozgurcatak.net publication updater"})
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.load(r)
        works += data["results"]
        cursor = data["meta"].get("next_cursor") if data["results"] else None
    return works


def norm(t):
    return re.sub(r"[^a-z0-9]", "", (t or "").lower())


def render(works):
    keep, seen = [], {}
    for w in works:
        title = (w.get("title") or "").strip()
        doi = w.get("doi") or ""
        if not title or w.get("type") in EXCLUDE_TYPES or title in EXCLUDE or doi in EXCLUDE:
            continue
        k = norm(title)
        if k in seen:   # same paper twice (e.g. arXiv preprint and published version): keep the published one
            if seen[k].get("type") == "preprint" and w.get("type") != "preprint":
                keep[keep.index(seen[k])] = w
                seen[k] = w
            continue
        seen[k] = w
        keep.append(w)

    keep.sort(key=lambda w: (w.get("publication_year") or 0, w.get("publication_date") or ""), reverse=True)
    by_year = defaultdict(list)
    for w in keep:
        by_year[w.get("publication_year")].append(w)

    out = [f'      <p class="muted">{len(keep)} publications · generated from <a href="https://openalex.org/{AUTHOR_ID}">OpenAlex</a> on {date.today():%d %B %Y}</p>']
    for year in sorted(by_year, reverse=True):
        out.append(f'      <h2 class="year" id="y{year}">{year}</h2>\n      <ol class="pubs" reversed>')
        for w in by_year[year]:
            names = []
            for a in w.get("authorships", []):
                n = html.escape(a["author"].get("display_name") or "")
                names.append(f"<strong>{n}</strong>" if (a["author"].get("id") or "").endswith(AUTHOR_ID) else n)
            if len(names) > 12:
                names = names[:10] + ["et al."]
            src = ((w.get("primary_location") or {}).get("source") or {}).get("display_name") or ""
            doi = w.get("doi") or ""
            m = re.search(r"10\.48550/arxiv\.(.+)$", doi, re.I)
            venue = f"arXiv:{m.group(1)}" if m else src
            link = doi or (w.get("primary_location") or {}).get("landing_page_url") or ""
            label = TYPE_LABEL.get(w.get("type"), "")
            title = html.escape(w["title"].strip())
            title_html = f'<a href="{html.escape(link)}">{title}</a>' if link else title
            doi_txt = f' <span class="muted">doi:{html.escape(doi.split("doi.org/")[-1])}</span>' if doi and not m else ""
            out.append(
                f'        <li>{f"<span class=type>{label}</span>" if label else ""}<span class="t">{title_html}</span><br>'
                f'{", ".join(names)}. <em>{html.escape(venue)}</em>, {year}.{doi_txt}</li>')
        out.append("      </ol>")
    return "\n".join(out)


def main():
    page = PAGE.read_text(encoding="utf-8")
    start, end = "<!-- PUBLICATIONS:START -->", "<!-- PUBLICATIONS:END -->"
    if start not in page or end not in page:
        raise SystemExit("Markers not found in publications.html")
    old_block = page[page.index(start) + len(start): page.index(end)]
    block = render(fetch() + EXTRA)

    def without_date(s):  # ignore the "generated on <date>" line when comparing
        return re.sub(r"generated from .*? on [^<]*</p>", "", s).strip()

    if without_date(old_block) == without_date(block):
        print("No changes in the publication list.")
        return
    page = page[: page.index(start) + len(start)] + "\n" + block + "\n      " + page[page.index(end):]
    PAGE.write_text(page, encoding="utf-8")

    # Keep sitemap.xml freshness honest: bump lastmod for publications.html only.
    sitemap = PAGE.parent / "sitemap.xml"
    if sitemap.exists():
        s = sitemap.read_text(encoding="utf-8")
        s = re.sub(r"(<loc>https://www\.ozgurcatak\.net/publications\.html</loc><lastmod>)[^<]*(</lastmod>)",
                   rf"\g<1>{date.today():%Y-%m-%d}\g<2>", s)
        sitemap.write_text(s, encoding="utf-8")
    print(f"Updated {PAGE} and sitemap lastmod")


if __name__ == "__main__":
    main()
