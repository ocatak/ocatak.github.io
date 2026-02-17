# Personal Academic Website — Ferhat Ozgur Catak

Static HTML personal academic website for **Ferhat Ozgur Catak** (Ozgur), Associate Professor of Cyber Security at the University of Stavanger (UiS). Optimized for SEO, fast load, and mobile-first UX.

## Structure

```
/
  index.html          # Homepage (hero, proof strip, research vision, projects, publications, talks, teaching, activity, FAQ)
  about.html
  research.html
  projects.html
  publications.html
  talks.html
  teaching.html
  contact.html
  assets/
    css/styles.css
    js/main.js
    img/
      profile.jpg     # Your professional photo (add your image)
      og.jpg          # Open Graph image 1200×630 (add for social previews)
  data/
    projects.json
    publications.json
    talks.json
    activity.json
    courses.json
    faq.json
  sitemap.xml
  robots.txt
  favicon.ico         # Add your favicon
  README.md
```

## Editing content

### JSON data

- **`data/projects.json`** — Featured projects (QuantumUQ, Trustworthy AI book, Secure 6G, etc.). Each item can have `title`, `meta`, `description`, `tags`, `primary`, `links`.
- **`data/publications.json`** — Publications with `title`, `venue`, `year`, `contribution`, `links`, `bibtex` (for Copy BibTeX).
- **`data/talks.json`** — Talks with `title`, `venue`, `date`, `links`.
- **`data/activity.json`** — Latest activity timeline: `date`, `title`, `description`.
- **`data/courses.json`** — Courses with `code`, `name`, `outcomes` (array of strings).
- **`data/faq.json`** — FAQ with `question` and `answer`.

Each page that uses this data also has an **inline fallback** in a `<script type="application/json" id="inline-...">` block so the site works when opened as `file://` (where `fetch()` is restricted). When deployed on a host, the JS will load from the JSON files.

### Setting the base URL (canonical + SEO)

Before deploying, replace **`https://YOUR-BASE-URL-HERE/`** with your real base URL in:

1. **All HTML files** — in `<link rel="canonical">`, `og:url`, `og:image`, `twitter:image`, and any JSON-LD `url` / `item` fields.
2. **`sitemap.xml`** — every `<loc>`.
3. **`robots.txt`** — the `Sitemap:` line.

Example: if your site is `https://ocatak.github.io/`, set base to `https://ocatak.github.io/` (with trailing slash for consistency).

## Deploying on GitHub Pages

1. Create a repository (e.g. `username.github.io` for a user site).
2. Replace `YOUR-BASE-URL-HERE` with `https://username.github.io` (or your repo URL) in all files above.
3. Push the project to the repo.
4. In **Settings → Pages**, choose source **Deploy from a branch**, branch **main** (or **master**), folder **/ (root)**.
5. After deployment, the site will be at `https://username.github.io/`.

You can also use **GitHub Actions** with a static site action, or any static host (Netlify, Vercel static, etc.).

## Images

- **Hero photo**: The site uses **`assets/img/profile.svg`** as a placeholder. Replace it with your own **`assets/img/profile.jpg`** (e.g. 400×400 or 600×600) and update the `src` in `index.html` from `profile.svg` to `profile.jpg`.
- **`assets/img/og.jpg`** — Add an image **1200×630** for Open Graph / Twitter cards (social previews). Update the `og:image` and `twitter:image` meta tags in each HTML file to point to your full URL (e.g. `https://yoursite.com/assets/img/og.jpg`).
- **Favicon**: **`favicon.svg`** is included (UiS-style “O”). You can add **`favicon.ico`** in the project root for older browsers; the HTML links to both.

## Validating SEO

- **Google Rich Results Test**: [https://search.google.com/test/rich-results](https://search.google.com/test/rich-results) — paste your live URL to check Person, FAQPage, BreadcrumbList.
- **Lighthouse** (Chrome DevTools → Lighthouse): run for Performance, Accessibility, Best Practices, SEO. Aim for high scores on all.
- **Meta and JSON-LD**: Ensure every page has a unique `<title>`, meta description, canonical, and (where applicable) BreadcrumbList and Person schema.

## Dark / light mode

The site defaults to **system preference** and stores the user’s choice in **localStorage** under the key `theme-preference`. The toggle in the navbar switches between `theme-dark` and `theme-light` (class on `<html>`).

## Accessibility

- Keyboard navigation for nav and buttons.
- `aria-label` / `aria-current` where needed.
- Contrast and focus states in CSS.
- `prefers-reduced-motion` respected (no heavy animations when reduced motion is requested).

## Tech stack

- **Static HTML** — no React/Next.js/server.
- **CSS** — one file, variables, Grid/Flex, no build step.
- **JS** — vanilla (nav, theme, data load with fallback, Copy BibTeX, optional scroll reveal).
- **Fonts** — Google Fonts (Inter, Space Grotesk) via `<link>`.
- **Icons** — inline SVGs (no icon library dependency).

## License

Content and design are for the site owner. Replace placeholders (links, ORCID, Scholar, etc.) with your real URLs and data.
