# Vegas1 — Las Vegas, seven nights, 2027

A sourced trip plan for **two adults**, seven nights, between **15 February and 23 March 2027**.

**Live site → <https://kanlerxz87-cyber.github.io/Vegas1/>**

## What is here

| Path | What it is |
|------|-----------|
| `docs/` | The site source (8 pages, plain HTML + one stylesheet, no framework, no CDN) |
| `index.html`, `*.html`, `style.css` (repo root) | The **same generated site**, written to the root as well. GitHub Pages on this repo is pinned to `main:/` and the API refuses to repoint it to `/docs`, so the root copy is what visitors actually get. Both are produced by `scripts/gen_site.py` — never edit either by hand. |
| `data/restaurants.json` | 24 MICHELIN listings with award tier, hours, exceptions, prices, official + YouTube links |
| `data/hotels.json` | 32 hotels with dated 7-night totals, bed/bathroom fit, Michelin proximity counts |
| `data/price-windows.json` | The week-by-week price comparison that answers "cheapest time to book" |
| `data/transit.json` | Monorail / RTC bus / Vegas Loop fares and the zone-to-restaurant minute matrix |
| `data/activities.json` | Four verified venues with official hours and prices for two |
| `data/questions.json` | 10-question register: answered, interpreted, still open — each with how to close it |
| `data/suggestions.json` | 12 decision improvements with honest trade-offs |
| `scripts/build.py` | Recomputes the Michelin proximity counts from the transit matrix; runs integrity checks |
| `scripts/gen_site.py` | Renders `docs/` from the JSON. All counts derived, none typed by hand |
| `scripts/validate.py` | Link and structure checks for the built site |
| `FLAGS.md` | The 20 things that did not verify cleanly |
| `executive-summary.md` | The one-page version |
| `COORDINATION.md` | Multi-session task board, merge record and verification log |
| `archive/` | The earlier session's build, preserved intact rather than overwritten |

## Rebuild

```bash
python3 scripts/build.py      # rescore + integrity checks
python3 scripts/gen_site.py   # render docs/
python3 scripts/validate.py   # link + structure checks
```

No dependencies beyond the Python 3 standard library. `gen_site.py` writes the site to **both**
`docs/` and the repo root; `.nojekyll` is present in both so no Jekyll step runs.

## The three findings

1. **8–15 March 2027 is the cheap week.** The same Venetian suite is $2,407 instead of $3,757 — about
   a third less — because the 15 February week contains Presidents' Day.
2. **The requested "within 1 hour by subway or bus" ranking cannot rank anything.** Las Vegas has no
   subway, and every hotel is within an hour of all 24 restaurants. A 20-minute column drives the
   ranking instead; disclosed as Q-01.
3. **The three cheapest hotels fail the brief's bed requirement.** LINQ, Flamingo and Horseshoe are
   all "room type assigned on arrival" — the bed is not guaranteed until check-in.

## Ground rules this project followed

- **No inferred values.** Blank means unverified. Every blank is listed in `FLAGS.md` and on the
  Questions page with a route to close it.
- **Every row cites a source.** 280 external links across 8 pages.
- **Estimates are labelled.** Only the transit minutes are estimates, and they say so everywhere.
- **No prior work was discarded.** A parallel session merged a first version to `main` mid-project;
  it is preserved in `archive/` with a written comparison of why each dataset was superseded.
