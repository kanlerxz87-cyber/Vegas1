# Vegas1 — Las Vegas, seven nights, 2027

A sourced trip plan for **two adults**, seven nights, between **15 February and 23 March 2027**.

**Live site → <https://kanlerxz87-cyber.github.io/Vegas1/>**

## What is here

| Path | What it is |
|------|-----------|
| `docs/` | The site source (15 top-level pages, plain HTML + one stylesheet, no framework, no CDN) |
| `index.html`, `*.html`, `style.css` (repo root) | The **same generated site**, written to the root as well. GitHub Pages on this repo is pinned to `main:/` and the API refuses to repoint it to `/docs`, so the root copy is what visitors actually get. Both are produced by `scripts/gen_site.py` — never edit either by hand. |
| `data/restaurants.json` | 24 MICHELIN listings with award tier, hours, exceptions, cost for two (with basis + menu source), official + YouTube/Instagram links |
| `data/hotels.json` | 32 hotels with dated 7-night totals, bed/bathroom fit, Michelin proximity counts |
| `data/price-windows.json` | Dated Booking.com comparison; read with official-engine snapshots and F-29/F-30 because no universal cheapest week is established |
| `data/transit.json` | Monorail / RTC bus / Vegas Loop fares and the zone-to-restaurant minute matrix |
| `data/activities.json` | Five activity entries with official details/social links when verified; blank social links remain unverified |
| `data/questions.json` | 14-question register: answered, interpreted, still open — each with how to close it |
| `data/suggestions.json` | 15 decision improvements with honest trade-offs |
| `scripts/build.py` | Recomputes the Michelin proximity counts from the transit matrix; runs integrity checks |
| `scripts/gen_site.py` | Renders `docs/` from the JSON. All counts derived, none typed by hand |
| `scripts/validate.py` | Link and structure checks for the built site |
| `scripts/check_evidence.py` | Offline regression gate: no priced restaurant without a basis and menu source, no unofficial hotel number in a decision cell, no root/docs drift |
| `dining.html` | Dining budget: three worked food/activity/transport totals for two adults, built at run time from `data/` (no hotel figure) |
| `FLAGS.md` | 46 register rows (F-01–F-30, F-47–F-53, F-58–F-66), including hotel rate basis/recency limitations and the restaurant price-basis corrections |
| `data/review-flags.json` | The 26 Nov 2026 audit register (F-39 to F-46) and confirmed items C-11 to C-13, each with source links. Rendered on `flagged.html` |
| `executive-summary.md` | The one-page version |
| `data/review.json` | Repo review: 17 line-by-line checks (C-01–C-17), limits, and irregularities |
| `docs/flagged.html`, `docs/repo-review.html` | **Flagged for Review** and **Repo review** pages (generated) |
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

1. **No market-wide cheapest week is established.** Booking.com snapshots show a lower 8–15 March quote for
   some rooms, while an official-engine sample checked 2026-11-25 favored the preferred February dates at some
   properties. A 2026-11-26 direct-engine refresh showed rates changing within one day and an occupancy-label
   mismatch for a Venetian result. These sources/bases are not comparable; verify exact dates directly (Q-06, F-29/F-30).
2. **The requested "within 1 hour by subway or bus" ranking cannot rank anything.** Las Vegas has no
   subway, and every hotel is within an hour of all 24 restaurants. A 20-minute column drives the
   ranking instead; disclosed as Q-01.
3. **The three cheapest hotels fail the brief's bed requirement.** LINQ, Flamingo and Horseshoe are
   all "room type assigned on arrival" — the bed is not guaranteed until check-in.

## A correction worth knowing about

The first transit model in this repository recorded **Chinatown / Spring Mountain Rd as reachable
only by car or rideshare**. That was wrong. RTC **Route 203** runs the length of Spring Mountain
Road and its [published timetable](https://rtcws.rtcsnv.com/routePDF/203.pdf) carries a timed stop
at **Las Vegas Blvd**, giving Decatur to Las Vegas Blvd about **8 to 17 minutes** across the sampled runs (weekday eastbound 10–17; Saturday westbound 8–9). The model uses 14, the midpoint (F-32).

It matters because **seven of the 24 MICHELIN listings sit on that one road** — nearly a third of
the guide. The north Strip therefore reaches Chinatown in about **34 minutes**, not never. This is
the only *published* travel time in the model; every other minute figure remains an estimate built
from station lists and route maps, and is labelled as one. Recorded as F-21 in `FLAGS.md`.

## A rename found while re-checking hotel links

On 26 Nov 2026 every hotel `Official` link was opened where the site would answer. `caesars.com/cromwell`
**301-redirects to `caesars.com/vanderpump-hotel`** — the property is now presented as **The Vanderpump Hotel**
(188 rooms, 3595 Las Vegas Blvd South, 702-777-3777). The row was renamed and logged as F-47: its seven-night
total was captured under the Cromwell name and must be re-quoted before booking. The sweep also settled F-27 —
18 of 32 official pages are now confirmed live, 8 refuse automated access, 5 were not opened and 1 (Nobu at
Caesars) lands on the parent property's page — and it exposed F-48: 15 hotel totals came from a dated
Booking.com **search list** rather than a property quote page, so those cards now say so.

## Session supplement — 27 Nov 2026 (restaurant menus + dining budget)

This pass re-read the venues' own menu pages and turned the results into a worked food budget.
It was merged on top of the 27 Nov **evidence gate** (F-58–F-59) and keeps that gate intact:
**no OTA hotel total is reintroduced anywhere, including on the new page.**

1. **Two "unpublished" prices were actually published.** Partage had been recorded as printing no
   price; its [`/menu` page](https://partage.vegas/menu) prints $130/$160/$210 per person (the
   `/restaurant` page is only a booking widget). Wing Lei had been recorded as unpublished; the
   [Wynn menu PDF](https://cdn.wynnresorts.com/image/upload/v1781902951/visitwynn_pdfs_files/wing-lei-main-menu-new.pdf)
   prints Chef Tam's tasting at $198.88 per person. Both rows now show cost for two — $260/$320/$420
   and $397.76 — with the menu linked (F-65).
2. **Guy Savoy is an estimate, not a resurrected total.** F-61 correctly withdrew the mislabelled
   "$200–$580" range and the unreproducible $3,000 Krug figure. The menu does print per-dish prices
   (starters $100–$120, mains $160–$290, cheese $60), so the cell is now `≈$520–$940 (est.)` with the
   assumption written next to it. The $3,000 figure stays withdrawn (F-64).
3. **Two row corrections.** Anima by EDO's Monday special is $65 **total**, not $65 per person;
   Esther's Kitchen opens for dinner seven days a week, though it publishes no clock times (F-66).
4. **New page:** [dining.html](dining.html) — three worked totals for two adults, all read from `data/`
   at build time: **$712.30** (two dinners), **$1,025.06** (one tasting menu), **$1,855.06**
   (stars-heavy), each including the three paid activities and a Monorail pass each. The room is
   deliberately excluded and the page says why; it also lists what to add once an official
   checkout total exists.

`scripts/check_evidence.py` now enforces the new state: every priced restaurant row must carry a
`price_basis` and an https menu source, the withdrawn Krug figure may not be used as a price, and the
budget page's arithmetic must match. All checks pass (15 pages, 0 failures, 0 warnings).

## Ground rules this project followed

- **No inferred values.** Blank means unverified. Every blank is listed in `FLAGS.md` and on the
  Questions page with a route to close it.
- **Every row cites a source.** 460 external links across 15 pages (counted by `scripts/validate.py` on the current build).
- **Sources and gaps are disclosed.** Hotel prices in the canonical 32-property table are Booking.com snapshots (not official property rates); this does not meet the strict official-rate-only requirement and is flagged as F-29. A dated direct-engine sample and 26 Nov refresh are linked from Sources & Flags; rates must be rechecked on the property's own engine.
- **Estimates are labelled.** Only the transit minutes are estimates, and they say so everywhere.
- **Flags are published.** Everything that did not verify cleanly is on `flagged.html`, with its sources.
- **No prior work was discarded.** A parallel session merged a first version to `main` mid-project;
  it is preserved in `archive/` with a written comparison of why each dataset was superseded.

## Session supplement — session-af795000 (verified rates + standalone site)

An independent session built a second complete site with **official-property booking-engine rates** (Caesars/Wynn/Resorts World direct, sampled 2026-11-25) — preserved and readable at **[docs/session-af795000/](docs/session-af795000/)** (exec summary, hotels, Michelin 24, activities, analysis, suggestions, open questions, flagged register). Machine-readable: `data/session-af795000-*.json`; research backup: `notes/research-log.md`.

Historical official-engine snapshots for seven nights, Feb 15–22, captured 25 Nov, included the amounts shown in the subsite (generally resort fee included, tax excluded; bed guarantee varies). Do not read those as a current quote or a market-wide cheapest week: official engines refreshed 26 Nov, rates moved, and the Venetian result carried a 4+ guest occupancy label. F-29/F-30 and the official-engine page preserve the source URLs and limitations; recheck exact room, dates, fee/tax, occupancy and cancellation conditions before booking.


## Session supplement — session-48dbf0ae (Booking.com dated quotes + independent site)

A third independent session built a parallel site with **Booking.com dated search quotes** (7 nights Feb 15–22, 2027, before 13.38% tax) and a full MICHELIN cost-for-2 table — preserved at **[docs/session-48dbf0ae/](docs/session-48dbf0ae/)** (exec summary, hotels ranking, 24 restaurants Star/Bib/listed, activities, suggestions Q1–Q10, flagged register, line-by-line `VERIFICATION.md`). Machine-readable: `data/session-48dbf0ae-*.json`.

Headline numbers (7 nights Feb 15–22, 2027, 2 adults, before tax, resort fee included): **Flamingo $625.65 · MGM Grand $1,508.50 · Caesars Palace $1,580 · Bellagio $3,072.30 · Venetian $4,573.16**; preferred 3-night window Feb 15–18: **Flamingo $166.65 · MGM $614.10–$887**. Also verified: Partage official menu ($130/$160/$210), é open Tue–Sun (official), RTC Strip fares $4/$6/$8/$20 with a **fare change proposed 2027-01-31**, and that **no $35 7-day Strip pass exists**. Cross-session price differences vs the canonical/af795000 figures follow the same rule: **check the property's own booking engine for your exact dates before deciding.**

## 27 November 2026 — evidence-display correction (T18)

This section supersedes earlier hotel-price/ranking recommendations in this README.
The current canonical hotel decision table leaves all unofficial/unconfirmed seven-night
amounts, room-fit assertions and inferred bus reachability counts blank. Candidate hotels
are alphabetical, not ranked by estimated travel scores. Raw datasets and independent
archives remain historical audit material, not endorsed offers. No official cheapest hotel,
stay week or purchase date has been established. The site is not booking-ready.

Fresh official checks, failures and exact limits: [`notes/audit-2026-11-27.md`](notes/audit-2026-11-27.md).
New review items: F-58–F-63. Corrections cover visitor/residential RTC fares, the incomplete
Guy Savoy dinner total, Mob Museum weekly hours and internally conflicting High Roller hours.
Other source observations and creator links were not comprehensively live reverified.

Reproducible publication check (does not mutate historical travel scores):

```sh
python3 scripts/gen_site.py
python3 scripts/validate.py
python3 scripts/check_evidence.py
```

These checks validate static structure/local links and the evidence-display policy, not
external-link liveness or future availability. `scripts/build.py` is the preserved historical
zone-model calculator; it is no longer a basis for the current hotel's decision table.
