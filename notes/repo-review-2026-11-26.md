# Repo review — 2026-11-26 (session arena-b54b3346-vegas1, task R01)

Scope: review the existing repo and live site, spot-check claims against official sources, and
record irregularities for the owner's review. **No live page, `data/` file, or root page was
changed by this review.** Items below are flagged, not fixed, because each one needs a decision.

Live site: https://kanlerxz87-cyber.github.io/Vegas1/ · Repo: https://github.com/kanlerxz87-cyber/Vegas1

## What was checked this session

| Check | Result | Evidence |
|---|---|---|
| `python3 scripts/build.py` | Passed. 24 restaurants (4 starred, 3 Bib, 17 Recommended); 32 hotels; no rescoring needed | Local run |
| `python3 scripts/gen_site.py` | Regenerated output is byte-identical to committed files (no git diff) | Local run, `git status` clean |
| `python3 scripts/validate.py` | 11 pages, 0 failures, 0 warnings, 288 external links **counted, not fetched** | Local run |
| Internal link scan, all 46 `*.html` files | 547 internal references, **11 broken**, all in `pages/flagged.html` (see F-02) | Local scan |
| MICHELIN official press release, Southwest 2026 | Matches the site's star split (see V-01) | https://www.michelin.com/en/publications/products-and-services/michelin-guide-reveals-first-ever-southwest-restaurant-selection-in-the-u-s |
| Live homepage fetch | Loads; headline claims checked (see F-01) | https://kanlerxz87-cyber.github.io/Vegas1/ |
| GitHub Pages status | `status: built`, source `main:/`, legacy build | `gh api repos/kanlerxz87-cyber/Vegas1/pages` |
| Workflow runs | `pages build and deployment` on `main`: success. One `Publish site to GitHub Pages` run on `arena/48dbf0ae-vegas1`: **failure** (see F-03) | `gh run list` |
| RTC fares page | **Fetch failed** this session, so RTC fares are *not* re-verified here | https://www.rtcsnv.com/fares/ |

**Not done this session:** fetching all 288 external links, and re-pricing hotels or restaurants.
The earlier sessions' row-level claims are therefore *not re-verified by this review*.

## Verified this session (official source)

- **V-01 — MICHELIN 2026 Southwest, Las Vegas stars.** The official press release lists
  *Restaurant de Joël Robuchon* with **Two** MICHELIN Stars; **é by José Andrés**, **Guy Savoy Las
  Vegas**, and **L'Atelier de Joël Robuchon Las Vegas** with **One** star each. The Bib Gourmand
  table lists **China Poblano, Esther's Kitchen and YEN Viet Kitchen** as the three Las Vegas Bibs.
  The press release also says the full selection is 64 restaurants. The site's "4 starred · 3 Bib ·
  17 Recommended" is consistent with this. Note: the release's *One Star* list also includes
  *Monte* (South Salt Lake, Utah), which is outside Las Vegas and correctly excluded from the Las
  Vegas count.
  Source: https://www.michelin.com/en/publications/products-and-services/michelin-guide-reveals-first-ever-southwest-restaurant-selection-in-the-u-s
  (Page date reads "31 Aug 2026"; the attached PDF filename reads `20260828`. Minor, not material.)
- **V-02 — Presidents' Day 2027 falls on Monday 15 Feb 2027.** Computed (third Monday of February).
  Not fetched from an official source this session. Source to check: https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/

## Irregularities — flagged for review

| ID | Severity | Irregularity | Where | Evidence | Suggested action |
|---|---|---|---|---|---|
| **F-01** | **High** | The live homepage and `README.md` state, without qualification, that **"February is the expensive week… moving to 8–15 March cuts the Venetian by 36%"** and show "$1,350 saved by moving a week". COORDINATION.md's own addendum records that the official-engine checks found **15–22 Feb is the cheapest verified window** at Caesars Palace ($1,582 vs ≈$2,013 Mar 8–15) and Flamingo ($595 vs ≈$804). The addendum asks that neither claim be quoted unqualified. The homepage does not do this. | `index.html` (live), `docs/index.html` l.53, `README.md` "three findings" #1 | COORDINATION.md "Addendum (post-merge cross-session conflict)" | Owner decision: qualify the headline per property, or re-price Venetian/Palazzo on the official engine. |
| **F-02** | **High** | There is **no Flagged-for-Review page on the live root site.** `pages/flagged.html` exists in the repo but is not published (not in `docs/` or the root). It also has **11 broken relative links** (`index.html`, `hotels.html`, …) because it sits one folder down. Flagged pages exist only under `docs/session-48dbf0ae/flagged.html` and `docs/session-af795000/flagged.html`, which are not linked from the main nav. | `pages/flagged.html`, `docs/session-*/flagged.html` | Repo file tree; link scan | Integration step: publish one flagged page at the root with a working nav link, or fix `pages/` paths. Requires a change to shared nav/`gen_site.py`, so it is logged here rather than edited. |
| **F-03** | Medium | A GitHub Actions run `Publish site to GitHub Pages` on branch `arena/48dbf0ae-vegas1` **failed** (conclusion `failure`). Logs could not be downloaded. Pages on `main` is built and healthy. | GitHub Actions | `gh run list`; `gh run view --log-failed` returned an error | Check the run in the Actions tab. If the branch is retired, delete the workflow there. |
| **F-04** | Medium | **RTC fares not re-verified:** the official fares page fetch failed this session. The earlier session's note (Strip & All Access $4/$6/$8, $20 3-day; a fare change proposed from 2027-01-31) is therefore unconfirmed by this review. | `transit.html`, `data/transit.json` | fetch failed: https://www.rtcsnv.com/fares/ | Re-fetch the RTC page before travel, or check its fares page directly. |
| **F-05** | Medium | **Row-level verification is incomplete.** 288 external links are counted by `validate.py` but not fetched by any check in the repo. Booking.com and property rates were captured on 2026-11-25 and are dynamic. | All tables | `validate.py` output; the review did not fetch these links | Run a link-liveness pass and re-capture prices on the day of booking. |
| **F-06** | Low | **Board hygiene:** COORDINATION.md lists two different rows with ID `T10`, and T1–T9 appear twice under different owners. Some session names do not follow the `session-<id>/<task>` branch rule. | `COORDINATION.md` task board | Read of the board | Renumber in the integration session. Historical entries were not edited. |
| **F-07** | Low | `README.md` says the trip-planning rules are "the three findings", but the live site has moved on (see F-01). README and site may drift. | `README.md` | Read | Regenerate README text from the same source as the site, or qualify it. |

## Known open items carried forward (from FLAGS.md and COORDINATION.md, not re-checked here)

- Brief asks for a "within 1 hour by subway or bus" ranking. Las Vegas has no subway; the repo models the
  bus, monorail and Vegas Loop, and the 1-hour metric returns 24/24 for every hotel (Q-01).
- The preferred 15–18 Feb window is 3 nights; the site prices 7-night totals (Q-02).
- Cheapest rates at several hotels (LINQ, Flamingo, Horseshoe, etc.) are "room type assigned on arrival". The queen bed is not guaranteed (F-11).
- 14-night variant not priced (F-17).

## Requests for the integration owner

1. Decide on F-01 before presenting the February-vs-March result as a recommendation.
2. Publish a root-level Flagged-for-Review page with working nav (F-02).
3. Check the failed Actions run (F-03), and re-fetch RTC fares (F-04).
