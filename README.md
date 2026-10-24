# mohammedmutaher.github.io

Personal academic website, hosted with GitHub Pages from this repository.

## Where to edit things (no HTML needed)

| What | File |
|------|------|
| Bio paragraph, email, LinkedIn, ORCID, Scholar ID | `_config.yml` |
| Publications, authors, tabs, "featured" cards | `_data/publications.yml` |
| Posters and presentations (+ poster image links) | `_data/posters.yml` |
| News timeline | `_data/news.yml` |
| Publication count in the title card | `_data/live_stats.yml` |
| Figures for papers | upload to `images/`, then put the file name in `image:` |
| Poster pictures | upload to `images/posters/`, then set `poster:` to `/images/posters/yourfile.png` |

Layout and look: `index.html` (page structure), `css/index.scss` (styling).

## Preview locally (optional)

```bash
bundle install
bundle exec jekyll serve
```

Then open http://127.0.0.1:4000.
