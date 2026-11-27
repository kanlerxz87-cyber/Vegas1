# T17 — Independent line-by-line verification audit — 2026-11-27

Session: `arena/bc27fca6-vegas1` (branch `arena/bc27fca6-vegas1`, base `631e611`).
Scope: this file + `COORDINATION.md` only. No `data/*.json`, generator, or generated site files edited —
PR #27 and PR #38 from other sessions own those files. Findings below are evidence for the owning
session; the one correction needed is logged as a Request in `COORDINATION.md`.

Method: rebuilt locally (`build.py` + `gen_site.py` + `validate.py` → 13 pages, 0 failures,
0 warnings, 394 external links; `git status` clean after rebuild, so committed output is
byte-identical to a fresh generator run), then fetched the live site and the official sources
below and compared them line by line.

## Checks that passed

| # | Claim on the site | Official source checked | Result |
|---|---|---|---|
| V-01 | 24 Las Vegas MICHELIN listings: 4 starred (2★ Joël Robuchon; 1★ L'Atelier, Guy Savoy, é), 3 Bib Gourmand (China Poblano, Esther's, YEN Viet), 17 Recommended | [MICHELIN press release, michelin.com](https://www.michelin.com/en/publications/products-and-services/michelin-guide-reveals-first-ever-southwest-restaurant-selection-in-the-u-s) + [michelinmedia.com](https://michelinmedia.com/pages/blog/detail/article/c0/a1480/) | **Confirmed.** Press release lists exactly these LV tiers. The 5th Southwest star (Monte, Utah) is correctly excluded — the site is LV-only. `data/restaurants.json` tiers match row for row. |
| V-02 | RTC Strip & All Access fares: $4 single / $6 2-hour / $8 24-hour / $20 3-day | [rtcsnv.com fares & passes](https://www.rtcsnv.com/ways-to-travel/fares-passes/) | **Confirmed** exactly, including reduced fares $2/$3/$4/$10. |
| V-03 | Monorail fares: $6.25 paper / $5.75 e-ticket single; 1-day $15.50/$13.95; 2-day $27; 3-day $33; 4-day $40; 5-day $48.25; 7-day $64/$59.95 | [lvmonorail.com ticket information](https://www.lvmonorail.com/ticket-information/) | **Confirmed** exactly. |
| V-04 | Michael Mina is "Temporarily closed", hours "Monday to Sunday: Closed"; tasting menu $295++ pp | [Bellagio official page](https://bellagio.mgmresorts.com/en/restaurants/michael-mina.html) | **Confirmed.** Page shows "Temporarily closed", the Closed hours block, seasonal closure dates 22–30 Nov and 6–8/13–15/20–22 Dec, and "$295++ Per Person" — so the site's $590++ for two is correct arithmetic on a currently-closed venue, and the site says so (F-23). |
| V-05 | The Cromwell → The Vanderpump Hotel rebrand (F-47); 188 rooms, 3595 Las Vegas Blvd South, 702-777-3777 | [caesars.com/vanderpump-hotel](https://www.caesars.com/vanderpump-hotel) | **Confirmed.** Page is live under the Vanderpump name with the same address/phone/room count. |
| V-06 | Live pages render: Overview, Hotels, MICHELIN restaurants, Activities, Open questions | [kanlerxz87-cyber.github.io/Vegas1](https://kanlerxz87-cyber.github.io/Vegas1/) + `/hotels.html`, `/restaurants.html`, `/activities.html`, `/questions.html` | **Confirmed.** All fetched and render with the disclosed caveats (Booking.com snapshot basis, ≤60-min = 24/24 for all 32 hotels, Venetian withdrawn F-39, no market-wide cheapest week). |
| V-07 | Pages API status | `gh api repos/kanlerxz87-cyber/Vegas1/pages` | `built`, source `main:/`, https enforced. Latest Pages runs on `main` are `success`. |

## Irregularity found (not edited — owned by another session)

| # | Issue | Evidence | Suggested fix |
|---|---|---|---|
| V-08 | `data/transit.json` RTC `fare_note` (rendered on `transit.html`) says **"Nevada local fares are $1."** | [RTC official fares page](https://www.rtcsnv.com/ways-to-travel/fares-passes/): Residential Routes single ride is **$2 regular / $1 reduced**. The $1 figure is the **Monorail** Nevada-resident fare ([lvmonorail.com](https://www.lvmonorail.com/ticket-information/): "Local Fare is $1"), not an RTC fare. | Correct the RTC note to "$2 single / $3 2-hour / $5 24-hour residential (regular); $1/$1.50/$2.50 reduced", and move the $1 Nevada-resident fare to the Monorail entry where it belongs. Logged as a Request in `COORDINATION.md` for the PR #38 owner. |

## Known limitations (already published, not new)

- Hotel 7-night totals are dated Booking.com snapshots, not official property rates (F-29/F-30).
  No universal cheapest week is asserted — correct, and the live site says so.
- Transit minutes are labelled estimates everywhere (F-20). The ≤60-minute metric is 24/24 for
  every hotel and cannot rank — disclosed (Q-01); the 20-minute column drives the ranking.
- 15 hotel price links are dated search lists, not room-quote pages (F-48); 8 official hotel
  pages refuse automated access (F-49). All disclosed on `flagged.html`.

## Verdict

The live site's headline claims (MICHELIN tiers, RTC + Monorail fares, Michael Mina closure,
Vanderpump rebrand, rate-basis disclosures) all check out against official sources. One
fare-note error (V-08) needs a one-line fix by the owning session. Nothing here blocks the
site being live.
