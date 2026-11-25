# COORDINATION.md — Shared task board (Vegas1 trip planning)

**Session ID:** `arena-3860068e`
**Working branch (fixed for this session):** `arena/3860068e-vegas1` (base `9b8bcfa`, `main`)
**Branch note:** The session rules fix the working branch to `arena/3860068e-vegas1`. The `session-<id>/<task>` branch pattern from the brief cannot be used here. Task isolation is handled by file scope below and by this board, not by separate branches. Logged as an irregularity (see Log).

**Status legend:** `unclaimed` · `in progress` · `done` · `needs review` (published on the Flagged for Review page; does not block anything)

## Task board

| ID | Task | Status | Owner (session) | File scope | Claimed (UTC) |
|----|------|--------|-----------------|------------|---------------|
| T1 | Repo review (line-by-line, irregularities, official links) | done (see Flagged) | arena-3860068e | `docs/repo-review.html` (generated), `data/site-data.json#repo_review` | 2026-11-25 |
| T2 | Michelin restaurants in Las Vegas (status, hours, cost, links) | needs review (per-person prices and off-property distances unverified) | arena-3860068e | `data/site-data.json#michelin` | 2026-11-25 |
| T3 | Hotels: queen+/private bath, Michelin proximity ranking, 7-night cost | needs review (no official rates; bathrooms unverified; ranking is same-resort, not 1-hour rule) | arena-3860068e | `data/site-data.json#hotels` | 2026-11-25 |
| T4 | Activities within ~1 hour of Strip hotels | needs review (drive/transit times unverified) | arena-3860068e | `data/site-data.json#activities` | 2026-11-25 |
| T5 | Booking timing + key dates (Feb 15–18 2027 and 7-night window) | needs review (booking windows derived, not verified) | arena-3860068e | `data/site-data.json#booking` | 2026-11-25 |
| T6 | Questions, missing information, suggestions for review, flagged items | done | arena-3860068e | `data/site-data.json#questions`, `#suggestions`, `#flagged` | 2026-11-25 |
| T7 | Site build (GitHub Pages landing + category subpages) | done (built to docs/ on this branch; not yet live) | arena-3860068e | `docs/**`, `scripts/build_site.py`, `README.md` | 2026-11-25 |
| T8 | Integration: combined re-verification, link check, publish | unclaimed | — | all shared outputs (final step) | — |

No other session has claimed any task. `COORDINATION.md` did not exist before this session and was created here.

## Sources used (official / trusted first)

| Source | URL | Used for |
|---|---|---|
| Las Vegas CVA (LVCVA) — Visit Las Vegas | https://www.visitlasvegas.com/michelin-guide-restaurants/ | 2026 Michelin Southwest list for Las Vegas (24 distinctions) |
| OPM Federal Holidays 2027 | https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/ | Washington's Birthday = Mon Feb 15 2027 |
| Red Rock Canyon NCA (BLM) | https://www.blm.gov/programs/national-conservation-lands/nevada/red-rock-canyon | Timed entry, hours, distance |
| Hoover Dam (Bureau of Reclamation) | https://www.usbr.gov/lc/hooverdam/service/directions.html · https://www.usbr.gov/lc/hooverdam/service/index.html | Distance, parking, tour rules |
| Valley of Fire State Park (NV State Parks) | https://parks.nv.gov/parks/valley-of-fire | Hours, entrance fees |
| RTC of Southern Nevada | https://www.rtcsnv.com/ | Bus transit operator |
| MGM Resorts restaurant pages | https://mgmgrand.mgmresorts.com/en/restaurants/joel-robuchon-french-restaurant.html · …/latelier-joel-robuchon-french-restaurant.html · https://cosmopolitanlasvegas.mgmresorts.com/en/restaurants/e-by-jose-andres.html · …/china-poblano.html · https://bellagio.mgmresorts.com/en/restaurants/michael-mina.html · https://aria.mgmresorts.com/en/restaurants/gymkhana.html | Michelin status, hours, price level |
| Caesars (Guy Savoy) | https://www.caesars.com/caesars-palace/restaurants/restaurant-guy-savoy | Michelin star text, address |
| Venetian / Palazzo (LVS) | https://www.venetianlasvegas.com/dining/restaurants/bouchon.html · …/cote.html · …/estiatorio-milos.html · …/mott-32.html | Hours, locations |
| Wynn | https://www.wynnlasvegas.com/dining/fine-dining/wing-lei | Hours |
| Resorts World (Stubborn Seed) | https://www.rwlasvegas.com/dining/stubborn-seed/ | Michelin 2026 selection, hours |
| Others (restaurant-owned sites) | see `data/site-data.json` per row | Hours, Michelin wording |

## Verification rules applied
- A value is written only if it appears on a fetched official page. Otherwise the cell is blank and the row carries an `unverified` flag.
- Prices for Feb 15–22 2027 hotel stays were **not published in any source retrieved** → left blank and flagged.
- The Michelin Guide site (guide.michelin.com) was **not reachable** from the sandbox; Michelin status is taken from the LVCVA official page and restaurant-owned pages that state the award. Manual check required.

## Log
- 2026-11-25 · arena-3860068e · Created `COORDINATION.md`; claimed T1–T7. T8 reserved for final integration.
- 2026-11-25 · Irregularity: brief asks for `session-<id>/<task>` branches; session rules fix the branch to `arena/3860068e-vegas1`. Followed session rules; no other branches created.
- 2026-11-25 · Remote branch `arena/3860068e-vegas1` confirmed at `44ceb50` via `git ls-remote`.
- 2026-11-25 · Built `scripts/build_site.py` → `docs/` (10 pages) from `data/site-data.json`. Blank values render as "Unverified". Re-run after any data change.
- 2026-11-25 · Self-review fixes: MGM Grand corrected to 3 stars (Robuchon 2★ + L'Atelier 1★); removed unverified area counts from the summary; re-checked Cosmopolitan "City Room Queen" and ARIA "Deluxe Two Queen Room" on official pages (2 queen beds, max 4 guests each; neither page states a private bathroom).
- 2026-11-25 · Irregularity: Pages is configured to serve `main /`, so `docs/` on this branch is not live until merged to `main` or the Pages source is changed. Settings were not changed (needs user decision).
- 2026-11-25 · Irregularity: the sandbox cannot reach most official hosts (allowlist), so the link check on the site is not complete. Links are listed for manual review. Michelin's own site (guide.michelin.com) is still unreachable.
- 2026-11-25 · Irregularity: the brief asks for ranking by restaurants within 1 hour by subway or bus. Route-level RTC data was not retrieved, so the ranking uses same-resort counts (labelled on the site).
- 2026-11-25 · Irregularity: brief text contains HTML-escaped placeholders (`&amp;amp;lt;id&amp;amp;gt;`). Interpreted as `session-<id>/<task>`.
