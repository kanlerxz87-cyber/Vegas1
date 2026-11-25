# Publishing

The live site is served by **GitHub Pages from the `docs/` folder** on the `main` branch.
No build step runs on the server: the HTML in `docs/` is committed, so Pages serves exactly
what is in the repository.

## How the site is structured

```
data/*.json        source of truth
tools/build_matrix.py   regenerates data/travel_matrix.json from addresses
build.py           reads data/, writes site/, mirrors site/ to docs/
assets/style.css   the only stylesheet
site/              generated HTML (working copy)
docs/              byte-identical mirror — this is what Pages serves
docs/.nojekyll     stops GitHub from running Jekyll over the output
```

`docs/` is a mirror rather than a symlink because GitHub Pages cannot follow symlinks.

## Pages

| Page | File |
|---|---|
| Overview and ranking | `index.html` |
| Hotels | `hotels.html` |
| Restaurants | `restaurants.html` |
| Activities | `activities.html` |
| Transit | `transit.html` |
| Open questions | `questions.html` |
| Suggestions | `suggestions.html` |
| Flagged for review | `flags.html` |
| Sources | `sources.html` |

## Redeploying after a data change

```bash
python3 tools/build_matrix.py   # only if addresses or the model changed
python3 build.py                # regenerates site/ and docs/
git add -A && git commit -m "..." && git push
```

Pages picks up the change on the next push. Allow a minute or two for the CDN.

## First-time enabling

If Pages is not yet switched on for the repository:

```bash
gh api -X POST repos/kanlerxz87-cyber/Vegas1/pages \
  -f source[branch]=main -f source[path]=/docs
```

or through the web UI: **Settings → Pages → Source: Deploy from a branch → `main` / `/docs`**.

## Why the site has no build dependencies

The brief asked for a site that is simple, mobile-friendly and easy to read. A bundler or a
framework would add an install step and a failure mode in exchange for nothing this site
needs. Every page is static HTML plus one 9 KB stylesheet, with no fonts, no scripts and no
third-party requests, so it loads fast on a phone and will still render in ten years.

## Design decisions worth knowing

- **Tables scroll horizontally inside their container** rather than squeezing columns, which
  is what keeps 24-row tables readable on a phone.
- **`details`/`summary` elements hold the per-hotel and per-activity detail**, so the top of
  each page stays scannable.
- **No JavaScript at all**, so nothing can break the reading experience.
- **A print stylesheet expands every `details` block** so a printed copy is complete.
