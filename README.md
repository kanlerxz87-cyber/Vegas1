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
| `data/questions.json` | 11-question register: answered, interpreted, still open — each with how to close it |
| `data/suggestions.json` | 13 decision improvements with honest trade-offs |
| `scripts/build.py` | Recomputes the Michelin proximity counts from the transit matrix; runs integrity checks |
| `scripts/gen_site.py` | Renders `docs/` from the JSON. All counts derived, none typed by hand |
| `scripts/validate.py` | Link and structure checks for the built site |
| `FLAGS.md` | The 22 things that did not verify cleanly |
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

## A correction worth knowing about

The first transit model in this repository recorded **Chinatown / Spring Mountain Rd as reachable
only by car or rideshare**. That was wrong. RTC **Route 203** runs the length of Spring Mountain
Road and its [published timetable](https://rtcws.rtcsnv.com/routePDF/203.pdf) carries a timed stop
at **Las Vegas Blvd**, giving Decatur to Las Vegas Blvd in **14 minutes**.

It matters because **seven of the 24 MICHELIN listings sit on that one road** — nearly a third of
the guide. The north Strip therefore reaches Chinatown in about **34 minutes**, not never. This is
the only *published* travel time in the model; every other minute figure remains an estimate built
from station lists and route maps, and is labelled as one. Recorded as F-21 in `FLAGS.md`.

## Ground rules this project followed

- **No inferred values.** Blank means unverified. Every blank is listed in `FLAGS.md` and on the
  Questions page with a route to close it.
- **Every row cites a source.** 280 external links across 8 pages.
- **Estimates are labelled.** Only the transit minutes are estimates, and they say so everywhere.
- **No prior work was discarded.** A parallel session merged a first version to `main` mid-project;
  it is preserved in `archive/` with a written comparison of why each dataset was superseded.

## Session supplement — session-af795000 (verified rates + standalone site)

An independent session built a second complete site with **official-property booking-engine rates** (Caesars/Wynn/Resorts World direct, sampled 2026-11-25) — preserved and readable at **[docs/session-af795000/](docs/session-af795000/)** (exec summary, hotels, Michelin 24, activities, analysis, suggestions, open questions, flagged register). Machine-readable: `data/session-af795000-*.json`; research backup: `notes/research-log.md`.

Headline verified numbers (7 nights, Feb 15–22, 2027, 2 adults, incl. resort fee, excl. tax): **Flamingo $595 · Horseshoe $763 · Planet Hollywood $1,092 · Paris $1,526 · Caesars Palace $1,582 · Resorts World ≈$1,942 · Wynn $4,739 (Cyber $677/nt — book by Dec 4, 2026)**. The preferred week is the cheapest verified 7-night window in the Feb 15 – Mar 23 range. See the subsite's hotels page for source links per row.
