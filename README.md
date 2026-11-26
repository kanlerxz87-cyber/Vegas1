# Vegas1 — Las Vegas, seven nights, 2027

A sourced trip plan for **two adults**, seven nights, between **15 February and 23 March 2027**.

**Live site → <https://kanlerxz87-cyber.github.io/Vegas1/>**

## What is here

| Path | What it is |
|------|-----------|
| `docs/` | The site source (12 pages, plain HTML + one stylesheet, no framework, no CDN) |
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
| `FLAGS.md` | The 28 earlier flags that did not verify cleanly (F-01 to F-28) |
| `data/review-flags.json` | The 26 Nov 2026 audit register (F-29 onward) and confirmed items, each with source links. Rendered on `flagged.html` |
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

1. **The cheaper-week claim is withdrawn.** The 25 Nov captures showed 8–15 March as about a third cheaper
   for the Venetian ($2,407 vs $3,757). On 26 Nov, Booking.com's own Venetian page did not reproduce it
   (US$5,185 for 15–22 Feb vs €4,472 for 8–15 Mar, both incl. taxes and fees). Withdrawn — F-29, Q-06.
2. **The requested "within 1 hour by subway or bus" ranking cannot rank anything.** Las Vegas has no
   subway, and every hotel is within an hour of all 24 restaurants. A 20-minute column drives the
   ranking instead; disclosed as Q-01.
3. **The three cheapest hotels fail the brief's bed requirement.** LINQ, Flamingo and Horseshoe are
   all "room type assigned on arrival" — the bed is not guaranteed until check-in.

## A correction worth knowing about

The first transit model in this repository recorded **Chinatown / Spring Mountain Rd as reachable
only by car or rideshare**. That was wrong. RTC **Route 203** runs the length of Spring Mountain
Road and its [published timetable](https://rtcws.rtcsnv.com/routePDF/203.pdf) carries a timed stop
at **Las Vegas Blvd**, giving Decatur to Las Vegas Blvd about **10 to 17 minutes**, depending on the time of day. The model uses 14, the midpoint (F-32).

It matters because **seven of the 24 MICHELIN listings sit on that one road** — nearly a third of
the guide. The north Strip therefore reaches Chinatown in about **34 minutes**, not never. This is
the only *published* travel time in the model; every other minute figure remains an estimate built
from station lists and route maps, and is labelled as one. Recorded as F-21 in `FLAGS.md`.

## Ground rules this project followed

- **No inferred values.** Blank means unverified. Every blank is listed in `FLAGS.md` and on the
  Questions page with a route to close it.
- **Every row cites a source.** 312 external links across 12 pages.
- **Estimates are labelled.** Only the transit minutes are estimates, and they say so everywhere.
- **Flags are published.** Everything that did not verify cleanly is on `flagged.html`, with its sources.
- **No prior work was discarded.** A parallel session merged a first version to `main` mid-project;
  it is preserved in `archive/` with a written comparison of why each dataset was superseded.

## Session supplement — session-af795000 (verified rates + standalone site)

An independent session built a second complete site with **official-property booking-engine rates** (Caesars/Wynn/Resorts World direct, sampled 2026-11-25) — preserved and readable at **[docs/session-af795000/](docs/session-af795000/)** (exec summary, hotels, Michelin 24, activities, analysis, suggestions, open questions, flagged register). Machine-readable: `data/session-af795000-*.json`; research backup: `notes/research-log.md`.

Headline verified numbers (7 nights, Feb 15–22, 2027, 2 adults, incl. resort fee, excl. tax): **Flamingo $595 · Horseshoe $763 · Planet Hollywood $1,092 · Paris $1,526 · Caesars Palace $1,582 · Resorts World ≈$1,942 · Wynn $4,739 (Cyber $677/nt — book by Dec 4, 2026)**. The preferred week is the cheapest verified 7-night window in the Feb 15 – Mar 23 range. See the subsite's hotels page for source links per row.


## Session supplement — session-48dbf0ae (Booking.com dated quotes + independent site)

A third independent session built a parallel site with **Booking.com dated search quotes** (7 nights Feb 15–22, 2027, before 13.38% tax) and a full MICHELIN cost-for-2 table — preserved at **[docs/session-48dbf0ae/](docs/session-48dbf0ae/)** (exec summary, hotels ranking, 24 restaurants Star/Bib/listed, activities, suggestions Q1–Q10, flagged register, line-by-line `VERIFICATION.md`). Machine-readable: `data/session-48dbf0ae-*.json`.

Headline numbers (7 nights Feb 15–22, 2027, 2 adults, before tax, resort fee included): **Flamingo $625.65 · MGM Grand $1,508.50 · Caesars Palace $1,580 · Bellagio $3,072.30 · Venetian $4,573.16**; preferred 3-night window Feb 15–18: **Flamingo $166.65 · MGM $614.10–$887**. Also verified: Partage official menu ($130/$160/$210), é open Tue–Sun (official), RTC Strip fares $4/$6/$8/$20 with a **fare change proposed 2027-01-31**, and that **no $35 7-day Strip pass exists**. Cross-session price differences vs the canonical/af795000 figures follow the same rule: **check the property's own booking engine for your exact dates before deciding.**
