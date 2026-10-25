# mohammedmutaher.github.io

Personal academic website, hosted with GitHub Pages from this repository.

## Where to edit things (no HTML needed)

| What | File |
|------|------|
| Bio paragraph, email, LinkedIn, ORCID, Scholar ID | `_config.yml` |
| Publications, authors, tabs, "featured" cards | `_data/publications.yml` |
| Posters and presentations (+ poster image links) | `_data/posters.yml` |
| News timeline | `_data/news.yml` |
| Publication + citation counts in the title card | automatic (see below); `_data/live_stats.yml` |
| Figures for papers | upload to `images/`, then put the file name in `image:` |
| Poster pictures | upload to `images/posters/`, then set `poster:` to `/images/posters/yourfile.png` |

Layout and look: `index.html` (page structure), `css/index.scss` (styling).

## Preview locally (optional)

```bash
bundle install
bundle exec jekyll serve
```

Then open http://127.0.0.1:4000.

## Title-card numbers update themselves

`.github/workflows/update-stats.yml` runs every Monday (and on demand from the
repo's **Actions** tab -> "Update title-card stats" -> **Run workflow**). It reads:

* Publications: the number of works on your ORCID record
* Citations: the total on your Google Scholar profile

If Google Scholar blocks the request (it sometimes does for automated visitors), the
old citation number is kept and the log says so. You can always edit
`_data/live_stats.yml` by hand.

## When a preprint gets published

In `_data/publications.yml`, keep the `biorxiv_doi:` line and add `doi:` (journal DOI)
and `venue:` (journal name). The paper then shows both a **Paper** and a **bioRxiv** button.
