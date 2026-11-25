# COORDINATION.md — Vegas1 Trip Planning (Las Vegas)

Shared task board. One row per task. Statuses: `unclaimed`, `in progress`, `done`, `needs review`.

## Session / branch note
- **Coordinating session ID:** `2d99ac1f`
- **Branch:** `arena/2d99ac1f-vegas1` (fixed by the Arena harness — sessions must not switch or create branches).
  - Coordination convention asks for `session-<id>/<task>` branches. That conflicts with the harness
    requirement to work only on the current branch, so **all tasks were claimed and worked on
    `arena/2d99ac1f-vegas1`**. This session was the sole worker and also performed final integration.
- **Commits:** frequent, on the current branch. Push with `git pull --rebase` before each push.

## Trip parameters (fixed requirements)
- Destination: **Las Vegas, NV, USA**. Duration **1–2 weeks**; window **2027-02-15 → 2027-03-23**.
- **Preferred window: 2027-02-15 → 2027-02-18**. Hotel pricing verified for a **7-night stay 2027-02-15 → 2027-02-22**.
- Travelers: **2 adults (a couple)**. Hotel must have **private bathroom** + **queen bed or larger**.
- Activities **≤ 1 hour travel** from the hotel. Hotels ranked by **# Michelin restaurants within 1 hour (subway/bus)**.
- Hotel cost = **total for 7 nights**; Michelin cost = **total for 2 adults**.

## Task board
| Task | Status | Owner | File scope |
|------|--------|-------|-----------|
| T1 — Requirements capture + executive summary | done | 2d99ac1f | `data/requirements.md`, `index.html` |
| T2 — Hotel research (amenities, price/7-night, booking window) | done | 2d99ac1f | `hotels.html` |
| T3 — Michelin restaurants (starred vs listed, cost, hours, location) | done | 2d99ac1f | `michelin.html` |
| T4 — Activities (≤1h travel, hours, links, social) | done | 2d99ac1f | `activities.html` |
| T5 — Social media links (YouTube/TikTok/Instagram) per entry | done | 2d99ac1f | within `michelin.html`, `activities.html` |
| T6 — Site build (landing + subpages, mobile-friendly dashboard UI) | done | 2d99ac1f | `src/styles.css`, `src/app.js`, all HTML |
| T7 — Verification: sources + flagged-for-review page | done | 2d99ac1f | `data/sources.md`, `review.html` |
| T8 — Suggestions + open-questions section | done | 2d99ac1f | `suggestions.html` |
| T9 — Final integration: merge, re-verify, build check, publish GitHub Pages | done | 2d99ac1f (integrator) | all files |

## Sources (official / verified)
- **Michelin:** official 2026 MICHELIN Guide Southwest — starred list
  (`https://guide.michelin.com/us/en/article/michelin-guide-ceremony/guide-michelin-southwest`) and full
  press release with addresses (`https://www.michelin.com/en/publications/products-and-services/michelin-guide-reveals-first-ever-southwest-restaurant-selection-in-the-u-s`).
  Restaurant hours: `guide.michelin.com` (Joël Robuchon), `ebyjoseandres.com` (é), `mgmgrand.mgmresorts.com` (L'Atelier), `opentable.com` (China Poblano).
- **Hotels:** Booking.com, Las Vegas, **check-in 2027-02-15 / check-out 2027-02-22, 2 adults, 1 room, USD**,
  taxes & fees included (captured 2026-11-25): `https://www.booking.com/searchresults.html?ss=Las+Vegas&checkin=2027-02-15&checkout=2027-02-22&group_adults=2&no_rooms=1&selected_currency=USD`
- **Transit:** `unleashvegas.com`, `lasvegascompass.com`, `lvmonorail.com` (Deuce + Monorail fares/hours).
- **Activities:** `lasvegaswonders.com`, `my-travelmonkey.com`, `viator.com`, `tripadvisor.com`.
- **Restaurant costs:** `stubbornseed.com`, `newsroom.mgmresorts.com`, `lasvegaswonders.com`, `lasvegascompass.com`.
- **Social:** Instagram `@joelrobuchon.lasvegas`, `@guysavoylasvegas`, `@bellagio`, `@spherevegaslv`.

## Verification performed
- **Michelin:** 24 Las Vegas distinctions (1 Two-Star, 3 One-Star, 3 Bib Gourmand, 17 Selected) + addresses
  cross-checked against the two official Michelin sources above. Distinction labels applied from those sources.
- **Hotels:** 5 properties with bed type, amenities, rating and 7-night USD total verified on Booking.com for the exact dates.
- **Transit:** Deuce/Monorail fares and hours verified against operator sources.
- **Build check:** all internal links resolve; all referenced assets exist (`index.html`, `hotels.html`,
  `michelin.html`, `activities.html`, `suggestions.html`, `review.html`, `src/styles.css`, `src/app.js`). No broken internal links.
- **Discipline:** no value inferred. Anything without an official source is blank + flagged `UNVERIFIED` on the tables and on `review.html`.

## Irregularities / flags (also on review.html)
1. **Bed not guaranteed** at Flamingo, Horseshoe, Planet Hollywood ("Room Type Assigned on Arrival"). Only MGM Grand (Studio King) and Luxor (Pyramid King) confirm a king.
2. **Resort fees** may be charged separately at check-in and are not confirmed in the Booking.com totals — `UNVERIFIED`.
3. **Promotional pricing** — all five hotel rates are "Black Friday Deal" rates for 2027-02-15 → 02-22; dynamic, re-check live.
4. **17 "Michelin Selected"** restaurants hold no star (listed, not starred) — labeled to avoid confusion.
5. **No subway in Las Vegas** — "subway or bus" maps to the Deuce bus + Monorail + RTC buses; 1-hour reach measured against this network.
6. **Single-window hotel pricing** — only the preferred 7-night window was priced, not the full 2027-02-15 → 03-23 range (cheapest-across-window comparison is a remaining task on the Suggestions page).
7. **Estimated transit times** — hotel↔restaurant one-way times are estimates; confirm via RTC trip planner / Google Maps.
8. **Unverified restaurant cost/hours** for the 17 Selected + Esther's Kitchen + YEN Viet Kitchen + Guy Savoy hours — left blank/flagged, to confirm on official sites.

## Handoff / irregularity log
- Single session performed all tasks + integration. No other sessions, no merge conflicts.
- Branch constraint reconciled: worked on the fixed `arena/2d99ac1f-vegas1` branch rather than `session-<id>/<task>` branches.
