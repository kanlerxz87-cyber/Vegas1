# COORDINATION.md — Shared Task Board

**Repo:** kanlerxz87-cyber/Vegas1
**Last updated:** 2026-11-26
**Purpose:** multi-session coordination so parallel agents never edit the same files.
Read this file *before* starting any task. Claim a task by writing your session ID below,
then commit and push that claim immediately.

## Session log

| Session | Started | Scope now | Branch |
|---------|---------|-----------|--------|
| arena/71886f12-vegas1 | 2026-11-26 | T14 — completed activity social-link visibility and executive-summary cleanup after the merged T13 rate audit | `arena/71886f12-vegas1` |
| arena/c419e2da-vegas1 | 2026-11-26 | T13 — post-merge hotel-rate claim audit; reconcile OTA/direct source conflict, refresh official booking engines, preserve PR #22 repo-review pages | `arena/c419e2da-vegas1` |
| arena-edcfa7a0-vegas1 | 2026-11-25 | T02–T11 — research complete; writing `data/*.json`, building `docs/`, publishing | `arena/edcfa7a0-vegas1` |
| arena-0c9983d6-vegas1 | 2026-11-25 | Verification pass on transit: added RTC Route 203, corrected the Chinatown reachability claim | `arena/0c9983d6-vegas1` |
| arena-126d963c-vegas1 | 2026-11-25 | Restaurant hours + closure status verification pass | `arena/126d963c-vegas1` |
| session-planner-01 (arena/4d41b902-vegas1) | 2026-11-25 | Independent full build: 24 Michelin restaurants, 9 ranked hotels, 8 activities, pricing, verification, summary, suggestions in `assets/` + root pages; integrated into canonical `main` site | `arena/4d41b902-vegas1` |
| session-48dbf0ae (arena/48dbf0ae-vegas1) | 2026-11-25 | Independent research + build (24 MICHELIN restaurants w/ cost-for-2, 9 dated Booking.com 7-night quotes, 9 activities, flags register, line-by-line VERIFICATION log); integrated as archived subsite `docs/session-48dbf0ae/` — live root site untouched | `arena/48dbf0ae-vegas1` |
| arena-f527b427-vegas1 | 2026-11-26 | **Repo review + line-by-line audit + Flagged-for-Review page + integration.** Scope: correct the Venetian/“cheapest week” headline, Route 203 timing wording, Michael Mina closure source, per-night reconciliation flags; add a live `flagged.html`; regenerate site; PR to `main`. | `arena/f527b427-vegas1` |
| arena-b54b3346-vegas1 | 2026-11-26 | Repo review + line-by-line verification spot-check; writes `notes/repo-review-2026-11-26.md` only (no change to live site or `data/`) | `arena/b54b3346-vegas1` |

> **Status note:** Original T01–T11 integration is published from `main`. Follow-up T12 (repo review and
> Flagged for Review/Repo Review pages) was merged in PR #22; T13 is the current branch's post-merge rate
> consistency audit. Independent archives remain additive and have not been overwritten.

## Rules (summary)

1. One task per session at a time. Claim it here first, commit + push the claim.
2. Work only inside the file scope you claimed. Need a file owned by someone else? Log a
   **Request** in the table below instead of editing it.
3. Session branches: `session-<id>/<task>`. The Arena session branch for this effort is
   `arena/edcfa7a0-vegas1`; all work from that session stays on that branch only.
4. Small, frequent commits. `git pull --rebase` before every push.
5. Merge conflict → stop, resolve without discarding the other session's work, log it here.
6. Mark **done** only after the verification steps listed for the task have been performed,
   with source links recorded. Anything that cannot be confirmed from an official source is
   marked **unverified**, left blank in the data, and listed on the Flagged for Review page.
7. Claims older than 60 minutes with no commits may be taken over; note the handoff.
8. Shared outputs (`data/*.json` tables, `docs/index.html`, navigation) are only changed by
   the integration session once all other tasks are `done` or `needs review`.

Status values: `unclaimed` · `in progress` · `needs review` · `done` · `blocked`

## Task board

| ID | Task | Status | Owner (session ID) | File scope | Notes |
|----|------|--------|--------------------|-----------|-------|
| T01 | Repo inventory + founding constraints | done | arena-edcfa7a0-vegas1 | `COORDINATION.md`, `docs/` | Repo was empty (README only) at commit `9b8bcfa`. GitHub Pages already enabled from `main` root. Bash sandbox has no general internet; all verification is via `fetch_page` / `web_search`. |
| T02 | Michelin 2026 Southwest selection — star/list status per Las Vegas restaurant | done | arena-edcfa7a0-vegas1 | `data/restaurants.json` | Source: official Michelin press release + LVCVA (visitlasvegas.com). |
| T03 | Restaurant hours, days open, reservations, price per couple | done | arena-edcfa7a0-vegas1 | `data/restaurants.json` | Gaps left blank + flagged. |
| T04 | Hotel shortlist, room-type fit (king/queen + private bathroom) | done | arena-edcfa7a0-vegas1 | `data/hotels.json` | Official hotel room pages. |
| T05 | Verified 7-night pricing per hotel for dated windows | done | arena-edcfa7a0-vegas1 | `data/hotels.json`, `data/price-windows.json` | Booking.com dated search results, captured 2026-11-25. Resort fees handled separately. |
| T06 | Transit model (monorail, Deuce/bus, Vegas Loop) + ≤60-minute scoring | done | arena-edcfa7a0-vegas1 | `data/transit.json`, `data/hotels.json` | Transit times are *estimates* derived from official route maps; never presented as official. |
| T07 | Activities list with official + social links, hours, exceptions | done | arena-edcfa7a0-vegas1 | `data/activities.json` | |
| T08 | Open-questions register + suggestions backlog | done | arena-edcfa7a0-vegas1 | `data/questions.json`, `data/suggestions.json` | |
| T09 | Static site build (mobile-first dashboard) | done | arena-edcfa7a0-vegas1 | `docs/**`, `scripts/**` | No framework, no external CDN calls, no build step at deploy time. |
| T10 | Verification pass + Flagged for Review page | done | arena-edcfa7a0-vegas1 | `docs/verification.html`, `FLAGS.md` | |
| T13 | Post-merge hotel-rate claim audit; revise public date recommendation and disclose source/volatility limitations | done | arena/c419e2da-vegas1 | `COORDINATION.md`, `FLAGS.md`, `README.md`, `executive-summary.md`, `scripts/gen_site.py`, `data/{hotels,price-windows,questions,suggestions}.json`, generated root + `docs/` pages | Replaced market-wide March savings claim with a source-conflict warning; labeled OTA quote basis, recorded 25 Nov sample and 26 Nov direct-engine refresh (F-29/F-30), and retained PR #22 Flagged for Review/Repo Review pages. No universal cheapest date asserted. |
| T14 | Activity social-link visibility and executive-summary cleanup after T13 | done | arena/71886f12-vegas1 | `COORDINATION.md`, `README.md`, `executive-summary.md`, `scripts/gen_site.py`, generated root/docs pages | Completed and merged in PR #25 on 2026-11-26; Pages deployment verified. Details and sources below. |
| T11 | Integration + GitHub Pages publish | done | arena-edcfa7a0-vegas1 | `docs/**`, Pages settings | Single integrating session for this effort; no other session active. |
| T1–T9 | Independent full build (restaurants, hotels, activities, pricing, verification, summary, suggestions) | done | session-planner-01 | `assets/**`, root `*.html` | Separate JS-driven build; integrated into canonical `main` site via merge (see handoff log). |
| T10 | Integrate, re-verify, deploy GitHub Pages | done | session-planner-01 | repo-wide | Merged independent build into canonical `main` site; supplementary pages linked from nav. |
| T1–T9 (independent) | Independent verified build + link-check pass | done | session-48dbf0ae | `docs/session-48dbf0ae/**`, `data/session-48dbf0ae-*.json` | Claimed on a fork-era task board that predates this one; no canonical file touched. See session record at end of file. |
| T12 | Repo review (line-by-line spot verification of canonical data), root **Flagged for Review** + **Repo review** pages, integration + Pages redeploy | done | arena-939a824e-vegas1 (branch `arena/939a824e-vegas1`) | `COORDINATION.md`, `FLAGS.md`, `README.md`, `scripts/gen_site.py`, `data/review.json`, `data/questions.json`, `data/suggestions.json`, `executive-summary.md`, generated `docs/**` and root `*.html` | Done 2026-11-26. 10 line-by-line checks (C-01…C-10), 18 irregularities (R-01…R-18) recorded in `data/review.json` and published on the Flagged for Review page. Hotel prices, social links and hotel official URLs were NOT re-checked (see limits). |
| R01 | Repo review: live-site spot-check, link audit, irregularity register | done | arena-b54b3346-vegas1 | `notes/repo-review-2026-11-26.md`, `COORDINATION.md` | Done 2026-11-26. Live site, `data/`, `docs/`, root pages NOT edited. Irregularities F-01–F-07 flagged for owner review. Sources: michelin.com 2026 Southwest press release; GitHub Pages API; build/validate logs. RTC fares fetch failed (F-04). |
| T14 | Repo review, line-by-line audit of headline claims, Flagged-for-Review page, integration + PR | done | arena-f527b427-vegas1 | `COORDINATION.md`, `FLAGS.md`, `README.md`, `executive-summary.md`, `data/hotels.json`, `data/price-windows.json`, `data/questions.json`, `data/suggestions.json`, `data/transit.json`, `data/travel_matrix.json`, `data/restaurants.json`, `data/review-flags.json` (new), `scripts/gen_site.py`, `docs/**`, root `*.html` | Claimed 2026-11-26 under the ID T12 in commit `3fc6739`; renamed T14 at integration because T12 was already used by arena-939a824e-vegas1 (merged PR #21, #22); T13 is used by arena-c419e2da-vegas1. Overlapping files were integrated by merge, not edited in parallel. Other sessions: please log requests here rather than editing these files. |

## T14 verification / integration record — 2026-11-26

- **Upstream overlap and resolution:** PR #24 (arena/c419e2da, T13) merged while this branch was in progress and updated the same hotel-pricing/summary generator scope. Rebased onto its latest `main`; preserved its `data/hotels.json`, `data/price-windows.json`, `data/questions.json`, `data/suggestions.json`, F-29/F-30, and the PR #22 Flagged for Review/Repo Review pages. T14 only added the missing visible social columns for activities and refreshed the executive summary/README counts and warnings; no T13 rate findings were replaced.
- **Activity rendering:** the five activity rows now display official venue links, days/hours, exceptions, couple-price basis, and YouTube/Instagram/TikTok columns. Only links already in `data/activities.json` render; dashes explicitly mean no profile/video was verified in the dataset.
- **Executive summary:** now resolves the 3-night preferred dates vs 7-night pricing mismatch, distinguishes dated OTA and direct-engine sources, carries forward F-29/F-30 occupancy/rate volatility, and links the Open Questions, Suggestions, Flagged for Review and Repo review pages. README inventory counts reflect 13 pages, five activity rows, 13 questions and 30 F-entries.
- **Build / QA:** `python3 -m json.tool data/suggestions.json`, `python3 -m py_compile scripts/gen_site.py`, `python3 scripts/build.py`, `python3 scripts/gen_site.py`, `python3 scripts/validate.py`, and `git diff --check` passed. Validator: 13 top-level pages, 0 failures, 0 warnings, 361 external links. Root and `docs/` copies are generated from the same source; the Flagged for Review and Repo review pages remain in both.
- **Remaining limitation:** hotel rates in the canonical 32-property table remain dated Booking.com snapshots rather than official property quotes; direct official rate evidence is partial and volatile (F-29/F-30). No universal cheapest week or current 7-night price is asserted.
- **PR and deployment:** [PR #25](https://github.com/kanlerxz87-cyber/Vegas1/pull/25) merged on 2026-11-26 as merge commit `0e9c5299efb91ea9e7bd3383b6305bdc297ebce9`. GitHub Pages build `1406755620` reached **built** with no error; Pages API reports `built` at `https://kanlerxz87-cyber.github.io/Vegas1/`. Fetched the live overview and `activities.html` after deploy; both show the updated source disclosures and five-row social-link table.

## Correction record — RTC Route 203 — 2026-11-25

Session `arena-0c9983d6-vegas1` found that this dataset recorded **Chinatown / Spring Mountain Rd
as reachable only by car or rideshare**. That was wrong, and it was the most consequential error in
the model, because **seven of the 24 MICHELIN listings sit on that road**.

## Merge conflict / handoff log — 2026-11-25

Session `session-planner-01` (branch `arena/4d41b902-vegas1`) built an **independent, complete**
JS-driven site (`assets/data.js`, `assets/app.js`, root pages `pricing.html`, `verification.html`,
`summary.html`) in parallel with `arena-edcfa7a0-vegas1`'s canonical `main` site. When merged into
`main`, both sites' root `index/restaurants/hotels/activities/suggestions.html` collided (add/add).

**Resolution (neither side discarded):**
- The canonical published `main` site (32 hotels, price-windows, transit, sources, questions, FLAGS,
  `docs/`) is kept as the primary experience for the collided root pages.
- The independent build's **unique supplementary pages** — `pricing.html`, `verification.html`,
  `summary.html` — are preserved and **linked from the canonical nav** so their verified content
  (pricing breakdown, line-by-line verification audit, executive summary) stays reachable.
- `assets/` (data.js, app.js, summary.js, suggestions.js, style.css) is retained to power those pages.
- This handoff is logged here per rule §5.

## Verification Log

| Date | Task | Finding | Source | Notes |
|------|------|---------|--------|-------|
| 2026-11-25 | T02 | 2026 MICHELIN Guide Southwest: LV has 4 starred (Joël Robuchon 2★; L'Atelier, Guy Savoy, é by José Andrés 1★), 3 Bib Gourmand, 17 Recommended | https://www.michelin.com/en/publications/products-and-services/michelin-guide-reveals-first-ever-southwest-restaurant-selection-in-the-u-s · https://www.visitlasvegas.com/michelin-guide-restaurants/ | Matched across two independent official sources |
| 2026-11-25 | T01 | GitHub Pages already enabled on `main` (root), build status `built` | `gh api repos/kanlerxz87-cyber/Vegas1/pages` | Confirmed |
| 2026-11-25 | T05 | Four whole weeks inside 15 Feb–23 Mar 2027 priced for 2027 (Venetian, Palazzo, Cosmopolitan, Nobu, ARIA, Bellagio, Waldorf) | Booking.com dated searches, URLs in `data/hotels.json` | 8–15 Mar cheapest for large resorts (−33% to −38% vs the Presidents' Day week); Nobu is the one property that moves the other way |
| 2026-11-25 | T06 | Ran `scripts/build.py` against the zone matrix | `data/transit.json` | The brief's ≤60-minute metric returns **24/24 for all 32 hotels**. Replaced as ranking metric by a ≤20-minute column; disclosed as Q-01 |
| 2026-11-25 | T02/T03 | All 24 award labels re-checked against three independent sources; `meta.counts` now computed from the array, not typed | michelin.com press release · visitlasvegas.com · lasvegasweekly.com | 4 starred (1×2★, 3×1★) · 3 Bib · 17 Recommended · 0 three-star |
| 2026-11-25 | T09/T10 | 8 pages rendered, 0 broken internal links, 0 structural warnings, 280 external source links, all HTML well-formed | `scripts/validate.py` | Pass |
| 2026-11-25 | T11 | F1 2027 Las Vegas GP confirmed 18–20 Nov 2027 — **outside** the 15 Feb–23 Mar window, so it is not a price driver here | f1experiences.com · dord.racing | Confirmed and excluded |
| 2026-11-26 | T12 | MICHELIN 2026 SW tiers confirmed: 1×2★, 3×1★, 3 Bib, 17 Recommended | https://www.michelin.com/en/publications/products-and-services/michelin-guide-reveals-first-ever-southwest-restaurant-selection-in-the-u-s · https://www.visitlasvegas.com/michelin-guide-restaurants/ | Confirmed (C-01) |
| 2026-11-26 | T12 | Joël Robuchon hours Tue–Sat 5:00–9:30 PM, business formal; reservations 702.891.7925 (was blank — filled) | https://mgmgrand.mgmresorts.com/en/restaurants/joel-robuchon-french-restaurant.html | Confirmed (C-03, C-04) |
| 2026-11-26 | T12 | é by José Andrés Tue–Sat 5:30–8:30 PM; archived subsite's Tue–Sun is wrong | https://cosmopolitanlasvegas.mgmresorts.com/en/restaurants/e-by-jose-andres.html | Confirmed (C-05); conflict logged R-06 |
| 2026-11-26 | T12 | Wing Lei Thu, Sun–Mon 5:30–9:30 PM; Fri–Sat to 10 PM; Tue–Wed closed; Forbes Five-Star; no Michelin star claim | https://www.wynnlasvegas.com/dining/fine-dining/wing-lei | Confirmed (C-06) |
| 2026-11-26 | T12 | RTC Strip/Downtown fares: 2-hour $6, 24-hour $8, 3-day $20 | https://rtcws.rtcsnv.com/mobile/geoFares.html | Confirmed (C-07) |
| 2026-11-26 | T12 | Michelin release page dated 31 Aug 2026; data says 26 Aug 2026 | https://www.michelin.com/en/publications/products-and-services/michelin-guide-reveals-first-ever-southwest-restaurant-selection-in-the-u-s | Conflict (C-02, R-05) |
| 2026-11-26 | T13 | Removed any market-wide cheapest-week claim; official and OTA data have different scopes, prices changed in a one-day refresh | https://www.caesars.com/book/room-list?arrivalDate=02/15/2027&departureDate=02/22/2027&dateSearchFormat=exact-dates&propCode=clv&numberOfAdults=2&numberOfRooms=1 · https://reservations.wynnlasvegas.com/ibe/details.aspx?hotelID=13763&langID=1&rmID=68658&checkIn=02/15/2027&checkOut=02/22/2027&adults=2&children=0 · https://www.venetianlasvegas.com/booking?adults[]=2&arrival_date=2027-02-15&children[]=0&departure_date=2027-02-22&view=calendar · https://reservations.rwlasvegas.com/ibe/shop.aspx?hotelID=17726&selectedTower=HILTON&checkin=2027-02-15&checkout=2027-02-22&nights=7&adults=2&children=0 | `fetch_page` refreshed official booking engines; Caesars and Wynn displayed nightly rates; Venetian displayed a tax-included total with a 4+ guest label. Recorded as F-29/F-30; exact rate conditions require confirmation. |
| 2026-11-26 | T13 | PR #24 merged and GitHub Pages deployed successfully; cache-busted re-fetch confirmed updated homepage and Flagged for Review page | https://github.com/kanlerxz87-cyber/Vegas1/pull/24 · https://github.com/kanlerxz87-cyber/Vegas1/actions/runs/45901945140 · https://kanlerxz87-cyber.github.io/Vegas1/?ver=20261126 · https://kanlerxz87-cyber.github.io/Vegas1/flagged.html | Merge commit `768f5aacd704ee3ba06edc6a5e0254a8462ea48e`; Actions build/deploy succeeded; Pages API `built`. |

## Irregularities / handoff notes

- **Hotel price conflict (F-29/F-30):** canonical 32-hotel rate rows are Booking.com snapshots, not official hotel-engine quotes. The 25 Nov direct-engine sample and one-day-later fetch do not provide a comparable market-wide answer; the latter also surfaced a Venetian 4+ guest label mismatch. F-29/F-30 are published on the Flagged for Review page. Do not recommend a universal cheapest week.
- **Rebase conflict (2026-11-26):** PR #22 from `arena/939a824e-vegas1` landed while T13 was being pushed. Rebased onto `origin/main`, preserved its new `data/review.json`, Flagged for Review and Repo Review page generation, and regenerated all 13 pages from the merged generator. No work from PR #22 was discarded.
- **No Michelin Guide existed for Las Vegas 2010–2025.** The 2026 Southwest guide is the
  first since 2009. Any hotel ranking based on Michelin proximity must cite the 2026 guide,
  not older lists (many older "Michelin" claims online are stale).
- **Las Vegas has no subway/metro.** The user's "≤1 hour by subway or bus" constraint is
  therefore modelled on the RTC bus network (The Deuce / SDX) plus the Las Vegas Monorail and
  the Boring Company Vegas Loop, which are separate-fare systems. This is a material
  interpretation and is raised as question Q-01 on the Questions page.

## Verification pass — 2026-11-25 (session arena/126d963c-vegas1)

Scope claimed: **restaurant hours + closure status only.** Files touched: `data/restaurants.json`,
`data/questions.json`, `data/hotels.json` (one notes string), `FLAGS.md`, `scripts/gen_site.py` (two hard-coded
strings), and the regenerated `docs/` pages. No hotel prices, no transit matrix, no Michelin award assignments.

What the pass found, all from the venues' own pages:

| Row | Was | Now |
| --- | --- | --- |
| Joël Robuchon | hours blank, `partial` | **Tue–Sat 5:00–9:30 PM**, closed Sun/Mon, no under-6s, business formal — `yes` |
| Partage | hours blank | **Tue–Sat 5–9 PM** — published on `/contact`, not the Restaurant page |
| Michael Mina | listed as a live option with a $590++ price | **Temporarily closed** — its own page reads "Monday to Sunday: Closed". Price retained but marked as not-running |
| Sparrow + Wolf | hours blank | still blank, deliberately: the official site publishes no hours |
| KAME Omakase | hours blank | still blank: OpenTable shows no weekly service hours |

Flags F-21 to F-25 added to `FLAGS.md`. Questions Q-11 and Q-12 added. Verified hours coverage went from 17/24 to 19/24;
the five remaining blanks all have a stated reason.

Build is clean: `python3 scripts/build.py && python3 scripts/gen_site.py && python3 scripts/validate.py`
→ 8 pages, 0 failures, 0 warnings.

## Verification pass — 2026-11-25 (session session-planner-01)

Scope: independent build. 24 restaurants cross-checked against `guide.michelin.com/us/en/nevada/restaurants`
and each venue's official page; 9 hotels cross-checked for queen bed + private bath on official room pages;
8 activities' hours verified from official attraction pages. 7 restaurant-hour rows left blank and flagged
`verified:false` (Esther's Kitchen, Kame Omakase, Lamaii, Partage, Sparrow & Wolf, Yen Viet Kitchen,
Guy Savoy full weekly schedule). Hotel nightly rates for the target dates are dynamic and not statically
extractable from booking engines — left blank and flagged rather than inferred. See `verification.html`.
## Session record — fd60d57e (branch `arena/fd60d57e-vegas1`)

Joined 2026-11-25 while the integration above was already published. **Additive, non-overlapping scope only** — no file owned by another session was edited.

| Task | Status | Files touched |
|------|--------|---------------|
| S1: Independent verified Michelin dataset (24 restaurants: distinctions, official guide URLs, hours, prices, socials) | done | `data/michelin.json` |
| S2: Line-by-line review pass + supplementary Flagged-for-Review page | done | `data/flags.json`, `pages/flagged.html` |
| S3: Hotel ranking summary by Michelin restaurants within 1 h transit | done | `data/hotel-ranking.json` |

**Verification performed (2026-11-25, official/primary sources):** guide.michelin.com Las Vegas list + michelin.com 2026-08-31 press release (distinctions, addresses, guide slugs); official hotel pages — mgmgrand.mgmresorts.com (Robuchon Tue–Sat 5–9:30 PM; L'Atelier Mon+Thu–Su 5–9:30 PM), caesars.com (Guy Savoy Tue–Sat from 5 PM; official menu prices à la carte $100–$290 eff. 2026-11-05, Krug Chef's Table $1,500/pp), cosmopolitanlasvegas.mgmresorts.com (é Tue–Sat 5:30–8:30 PM; China Poblano hours), venetianlasvegas.com `/dining/restaurants/…` (Bouchon incl. Thanksgiving exception, COTE, Milos, Mott 32), wynnlasvegas.com (Wing Lei Thu/Su/Mo 5:30–9:30, Fr–Sa to 10), mott32.com, partage.vegas, kabutolv.com, soulbellybbq.com, estherslv.com; rtcws.rtcsnv.com official fare page (Deuce $6/$8); tix.lvmonorail.com ($5.75 / $13.95); official Fountains of Bellagio schedule (fills FLAGS.md F-18); Michael Mina officially temporarily closed (fills/corroborates; data/michelin.json corrected); verified Instagram handles (fills FLAGS.md F-19 in part): @ebyjoseandres, @joelrobuchon.lasvegas, @cotekoreansteakhouse, @mott32vegas, @estherskitchenlv, @lamaiilv + Wynn IG/TikTok @wynnlasvegas.

**Irregularities:** `data/flags.json` v2 — S-01/S-02/S-04/S-05 verified fills awaiting integration; S-03 self-correction; F07/F11/F13 remain open and match FLAGS.md items. v1 flags against the archived first site are retained as a record.

**Merge/conflict log (rule 5):** rebased onto `origin/main` repeatedly on 2026-11-25 while PRs #1/#2/#3/#4/#5 landed in parallel; COORDINATION.md conflicts resolved each time by keeping the integration session's board verbatim and appending this record; the superseded bootstrap commit was skipped (nothing discarded — content preserved here and in git history).

## QA pass against the rendered site — session edcfa7a0 — 2026-11-25

This pass read the **live** pages back and compared them to the JSON that generates them, rather than
trusting that a green build meant a correct page. All nine defects below were found that way; none was
caught by any validator.

| # | Defect | How it was found | Fix |
|---|---|---|---|
| 1 | **Desert Rose in the wrong zone.** Tagged `center-strip` and described as "a 15-minute walk to the centre-Strip Michelin cluster"; the address is 5051 Duke Ellington Way, one block east of the Strip at the Tropicana/MGM Grand corner. | Its own note contradicted its own zone. | Zone → `south-strip`; walk claim restated as 15–20 min to the Robuchon rooms at MGM Grand. Price, score and suite size were always right, so the pick survives with the correct reason. |
| 2 | **`desertroseresort.com` returns HTTP 500.** | Fetched it. | Repointed to the real operator page (Shell Vacations Hospitality / Wyndham Extra Holidays). |
| 3 | **28 of 32 hotel `official_url` links were never fetched** — the restaurant links all were. | Comparing how each field was sourced. | Cards now mark them *"not fetched — may have moved"*. Four confirmed: Desert Rose, LINQ, Palms Place, Venetian. The Booking.com "Price source ✓" link on every card is always fetched, so nothing is unreachable. F-27/F-28, Q-13, S-13. |
| 4 | **Day span printed twice** — "Tue–Sat" then "Tue–Sat 5:00 PM – 9:30 PM". | Reading the rendered hours column. | Stripped when `hours` already starts with `days`. Robuchon + Partage. |
| 5 | **Hand-typed counts in the question register**: Q-03 "21 restaurants / fourteen Recommended", Q-07 "45 YouTube links", Q-04 "Twelve of the 21", S-12 "Ten of the 21". | Cross-checking rendered text against `data/restaurants.json`. | Actual: 24 listings, 17 Recommended, 69 links, 15 with a phone number, 12 with fully verified hours. All derived now. Same bug class as PR #5, in files PR #5 did not touch. |
| 6 | **Three nav pages were empty shells.** `pricing.html` 2,258 b, `verification.html` 2,225 b, `summary.html` 1,621 b — each with **0 table rows and 0 source links**; pricing built its whole body from an empty `<div id="tbl-pricing">`. Regenerating would have deleted them and broken every nav bar. | Counting `<tr>` and `href="http` in the committed files. | `gen_site.py` now owns all three and routes them at the sections carrying the figures. Nothing deleted, no nav broken. |
| 7 | **Four cross-page anchors pointed at ids that did not exist.** | Added an anchor check to `validate.py`. | Stable ids added to the five target sections plus one per suggestion. The check is permanent, so it cannot regress. |
| 8 | **Caesars note overstated.** "Two Michelin-starred restaurants in-building-adjacent range" read as if both were inside; only Guy Savoy is. | Reading the rendered note. | Rewritten: Guy Savoy (1★) in the building; Robuchon and L'Atelier a 10-minute ride south. |
| 9 | Missing space before the "not fetched" marker. | Reading the rendered HTML. | `&nbsp;` separator. |

**Final state:** 11 pages published to both the repo root and `docs/`; `validate.py` reports 11 pages,
0 failures, 0 warnings, 0 broken anchors; committed output is byte-identical to a fresh generator run (no
drift); Pages build `built`; confirmed on the live URL.

**Lesson worth keeping:** all nine defects were invisible to `build.py` and `validate.py`. They appeared only
when the rendered text was read and compared back to the data. A green validator proves the generator ran,
not that the page is true.

## Session record — arena-939a824e-vegas1 (T12) — 2026-11-26

Branch `arena/939a824e-vegas1` (base `e4fb98e`). Scope: repo review, Flagged for Review page, Repo review page, integration with the canonical site.

- **Done:** 10 line-by-line checks against official pages (C-01…C-10; 8 confirmed or conflicting, 2 not checked). 18 irregularities recorded (R-01…R-18). R-15…R-18 cover the other session's review (notes/repo-review-2026-11-26.md, F-01…F-07) in `data/review.json`, with severity, action and source link. Published as `flagged.html` and `repo-review.html` on the live root site and `docs/`.
- **Headline corrected:** the 'February is the expensive week' claim (index, README, executive summary) now says the cheapest week depends on the property (R-15).
- **Data changes (kept minimal):** one official gap closed (Robuchon reservation phone, from MGM page). Two overstated labels corrected in text: `data/suggestions.json` (hours count) and `data/questions.json` ("working" video links, not checked). `executive-summary.md` corrected the same way. `README.md` flag count corrected (22 → 28). The Sources page flag count is now derived from `FLAGS.md`.
- **Not changed (by design):** hotel prices, YouTube/TikTok/Instagram links, hotel official URLs, and the archived `docs/session-*` subsites. These are flagged, not altered.
- **Irregularities to review:** see the Flagged for Review page (R-01…R-14). Highest priority: restaurant and hotel `verified` labels overstate what was confirmed (R-01, R-03); no Instagram/TikTok links recorded (R-02); the literal ≤60-minute metric cannot rank hotels (R-04); two sessions give opposite cheapest weeks (R-13).
- **PR and merge:** PR #21 (`arena/939a824e-vegas1` → `main`) https://github.com/kanlerxz87-cyber/Vegas1/pull/21 — merged with `--merge` at 2026-11-26T21:55:54Z, merge commit `f0ab1b6de19f0e62f0b8eae0915268ded05dc24c`. Pages deploy on `main` succeeded (run 45901447883); the live pages `flagged.html` and `repo-review.html` were fetched and render. Flagged irregularities did not block the merge.
- **Follow-up:** a fix to two cross-references (R-03 and R-13 pointed to Q-03; the booking-engine question is Q-06) is in a second small PR, recorded in the PR record below.

## PR and merge record — arena-939a824e-vegas1 (T12) — 2026-11-26

- PR #21: https://github.com/kanlerxz87-cyber/Vegas1/pull/21 — merged `--merge` 2026-11-26T21:55:54Z, merge commit `f0ab1b6`. Pages on `main` built and deployed (run 45901447883, success), Pages API `built`.
- Flagged irregularities R-01…R-18 published on https://kanlerxz87-cyber.github.io/Vegas1/flagged.html and did not block the merge.
- Follow-up cross-reference fix (R-03, R-13: Q-03 → Q-06) in a second PR; see its record below when merged.

## Session record — session-af795000 (arena/af795000-vegas1) — 2026-11-25

Independent full-session build of the same brief (started from base 9b8bcfa before the integrations above). Per rule 5, this merge kept the integration sessions' canonical site and data verbatim; my complete site + datasets are preserved as a self-contained subsite and dated files:

- **Site (self-contained, internal links work):** `docs/session-af795000/` — executive summary, hotels (ranked + verified totals + cheapest week + booking windows), Michelin 24 (cost-for-2 + hours + socials), activities, analysis/transit, suggestions (S1–S8 + D1–D6), open questions (Q1–Q12 + discovery methods), flagged register.
- **Datasets (verified values, source URL per row):** `data/session-af795000-michelin.json`, `data/session-af795000-hotels.json`, `data/session-af795000-activities.json`.
- **Research backup:** `notes/research-log.md` (full transcripts: rate calendars, menu prices, Michelin lists).

**Unique verified findings worth merging into canonical data (official-property booking engines, sampled 2026-11-25, 2 adults, Feb 15–22 2027, 7 nights, incl. resort fee, excl. tax):** Flamingo $85/nt → $595 (caesars.com/book/room-list propCode=flv) · Horseshoe $109 → $763 (blv) · Planet Hollywood $156 → $1,092 (phv) · Paris $218 → $1,526 (plv) · Caesars Palace $226 → $1,582 (clv; Julius King $232/$1,624) · Resorts World Hilton ≈$277 avg → ≈$1,942 (reservations.rwlasvegas.com/ibe/shop.aspx?hotelID=17726&selectedTower=HILTON, daily Feb 15–21 = 214/404/404/284/242/242/152; RF-legend conflict flagged) · Wynn Resort King $677 Cyber / $833 Flexible → $4,739/$5,831 (reservations.wynnlasvegas.com/ibe/details.aspx?hotelID=13763&rmID=68658). **Cheapest 7-night window in Feb 15–Mar 23 2027 = the preferred week Feb 15–22** at every property checked (exact-dates searches + official flexible-date calendars; March spikes incl. Caesars Mar 19–20 $494/$425). **Booking deadlines:** Wynn Cyber must be booked Nov 20–Dec 4 2026 ($677/nt + $75/day credit, 1-nt dep, 72h cancel); Caesars promos auto-apply + Rewards −15%; RW "ALL RESORT, NO FEES" offer worth pricing. Note: canonical `data/hotels.json` prices are Booking.com-OTA derived (`official_verified: 'no'`) — the rates above are the official-engine replacements/confirmations.

**Also verified here:** official menu math for 2 (Wing Lei $198.88 pp → $397.76; Stubborn Seed $160 pp → $320; Partage $130/$160/$210 pp; Kabuto $130/$185 pp via Resy; Michael Mina $295++ pp → $590; Anima $85 pp → $170; Guy Savoy à-la-carte $60–$290 items, menu eff. 11/5/26; Esther's mains $21–$32); hours for 17/24 restaurants incl. exceptions (Wing Lei dark Tue–Wed; Robuchon dark Sun+Mon; Pho Ga Bac Bac 24h; SoulBelly dark Mon; Kabuto holiday-menu-only Dec 18–Jan 10); Neon Museum 2027 admission from $21 daily 3–11 PM; Mob Museum 9–9 + Underground 11–11 (Fri–Sat midnight); socials verified: @gymkhanalasvegas, @soulbellybbqlv, Kabuto IG (official posts), @theneonmuseumlasvegas + TikTok @neonmuseumlasvegas.

**Flaggable items (full register in `docs/session-af795000/flagged.html`):** LV Magazine (2026-08-27) mislabels the 17 Selected as "Bib Gourmand" (official Bib = China Poblano, Esther's, YEN Viet only); historic≠current stars (Robuchon 3★→2★, Guy Savoy 2★→1★, Wing Lei 1★→Selected); name mismatches MICHELIN vs LVCVA ("Restaurant de Joël Robuchon", "Guy Savoy Las Vegas"); zola.com lists "The Vanderpump Hotel" at 3595 S LVB (Cromwell address, possible rebrand — unconfirmed); Stubborn Seed tasting $145 (blog) vs $160 (official PDF — use $160); RW IBE shows BOTH "excludes RF" and "includes $55 RF" legends (promo cross-check suggests inclusive); MGM-family + Venetian/Palazzo + Fontainebleau room rates bot-blocked → blank+flag (Venetian calendar shows $XXX placeholders; FB rooms page 404); Kame site JS-only; CLV Mar 2 sold out (blocks W3 7-night search); Caesars calendars drift ±$14 between same-day fetches (label "sampled 2026-11-25"); COTE NYC / Stubborn Seed Miami / Gymkhana London stars ≠ their LV locations (Recommended only); SoulBelly Michelin = Main St only (not Express counter); Lamaii Michelin = Chinatown only (not Henderson).

**No work discarded in this merge:** canonical site/data/FLAGS/scripts kept from main; my outputs relocated to the paths above (this record's first bullets). PR #16.

**Addendum (post-merge cross-session conflict — flag for users):** The canonical site's headline "February is the expensive week — moving to 8–15 Mar cuts the Venetian by 36%" (from Booking.com OTA snapshots in `data/hotels.json`) **conflicts** with session-af795000's official-engine finding that Feb 15–22 is the *cheapest* verified 7-night window at every property checked (Caesars Palace $1,582 vs Mar 8–15 calendar ≈$2,013; Flamingo $595 vs ≈$804; Wynn/RW Feb sampled). Both may be right for different properties/sources (Venetian March was not machine-verifiable for af795000; OTA snapshots can undercut official BAR). Resolution rule for users: **check the specific property's own booking engine for the specific dates before deciding**; neither claim should be quoted unqualified. Recorded 2026-11-25.


## Session record — arena-b54b3346-vegas1 (R01 repo review) — 2026-11-26

- **Verified (official source):** MICHELIN 2026 Southwest press release — Robuchon 2★; é, Guy Savoy, L'Atelier 1★; Las Vegas Bibs = China Poblano, Esther's Kitchen, YEN Viet. Matches the site's 4 starred / 3 Bib / 17 Recommended. https://www.michelin.com/en/publications/products-and-services/michelin-guide-reveals-first-ever-southwest-restaurant-selection-in-the-u-s
- **Checked locally:** `build.py` integrity passed; `gen_site.py` output identical to committed; `validate.py` 11 pages / 0 failures; internal-link scan of 46 HTML files found 11 broken links, all in unpublished `pages/flagged.html`.
- **Pages:** `main` build status `built`, deploy success. One failed run on `arena/48dbf0ae-vegas1` (F-03).
- **Not verified this session:** RTC fares (fetch failed), the 288 external links, and all dynamic hotel/restaurant prices.
- **Irregularities (full register in `notes/repo-review-2026-11-26.md`):** F-01 live homepage states "February is expensive / −36% in March" unqualified, contradicting the cross-session addendum above. F-02 no root Flagged-for-Review page is published. F-03 failed Actions run. F-04 RTC fares unconfirmed. F-05 row-level link verification incomplete. F-06 duplicate task IDs on the board. F-07 README drift.
- **Changes:** added `notes/repo-review-2026-11-26.md` and this record only. Live site, `data/`, `docs/`, and root pages unchanged.

## Session record — session-48dbf0ae (independent build + link check) — 2026-11-25

Branch `arena/48dbf0ae-vegas1` forked from `9b8bcfa` **before** this board existed, so its early
claims (T01–T09) were made against a now-superseded task board. No work from any other session was
edited or discarded. Integrated additively per the `session-af795000` pattern:

- **Site (7 pages, mobile-first):** `docs/session-48dbf0ae/` — index, executive summary, hotels,
  michelin, activities, suggestions + open questions (Q1–Q10), flagged-for-review, plus
  `VERIFICATION.md` (line-by-line source→value log) and its own stylesheet.
- **Data:** `data/session-48dbf0ae-hotels.json`, `data/session-48dbf0ae-michelin.json`,
  `data/session-48dbf0ae-activities.json` (all rows carry source URLs; blanks = unverified).
- **Live site:** root `index.html` and all canonical `data/*.json` were **not modified** by this
  session's PR; the archived workflow that would have repointed Pages was deleted in this merge.

**Verified findings worth cross-reference (2026-11-25):**
- Booking.com dated quotes, 7 nights Feb 15–22 2027, 2 adults, before 13.38% tax (resort fee in):
  Flamingo **$625.65** (king, −40% BF) · LINQ $640 incl tax · Horseshoe $813 incl tax ·
  MGM Grand $1,508.50 · Caesars Palace $1,580 · Bellagio $3,072.30 · Cosmopolitan $3,432.80 ·
  ARIA $3,797.50 · Venetian $4,573.16. Budget cards: Rio Masquerade $483, Gold Coast $768,
  Orleans $1,067. Preferred window (Feb 15–18, 3 nights): Flamingo $166.65 / MGM $614.10–$887.
- Week lever at MGM Grand: Feb 15–22 $1,508.50 vs **Feb 22–Mar 1 $1,293.60** (post–Super Bowl LXI
  dip; game Sun Feb 14, 2027 + Presidents' Day Mon Feb 15 inflate the target week's first nights).
  Flamingo runs the other way: target week $625.65 < Mar 1–8 $925.85. Consistent with the
  canonical addendum: **per-property check required**.
- Partage official menu fetched live: 5-course **$130** / 7-course **$160** / Signature **$210**
  (supersedes $80–$130 and $120–$198 third-party figures).
- é by José Andrés official site: **open Tue–Sun**, two shows 5:30/8:30 PM, nine seats, tickets
  release 3 months ahead (resolves a Sunday-service source conflict).
- RTC official fares confirmed: Strip & All Access $4 / $6 / $8 / **$20 3-day** — there is **no
  $35 7-day Strip pass** (an error this session caught and corrected in its own draft); a fare
  change is proposed from **2027-01-31** and must be re-checked before travel.
- Link-check pass: all internal links valid; ~20 critical external links re-fetched live
  (MICHELIN guide, Caesars, Bellagio, Mott 32, Esther's, é, Partage, COTE, Sparrow + Wolf,
  Kabuto, SoulBelly, Anima, Stubborn Seed, Neon Museum, YEN Viet). Sandbox curl cannot reach
  external hosts; verification used `fetch_page` + `web_search`.

**No work discarded in this merge:** canonical root site, `docs/` canonical pages, `data/*.json`,
`scripts/`, `FLAGS.md`, `archive/` all kept from `main`.

## Session record — T14 (claimed as T12 in 3fc6739) — arena-f527b427-vegas1 — 2026-11-26

Branch `arena/f527b427-vegas1`, forked from `e4fb98e` (main). Claim committed and pushed first (`3fc6739`).

**What was checked against official or primary sources (fetched 26 Nov 2026):**

| Item | Result | Source |
|---|---|---|
| All 24 Las Vegas MICHELIN names and tiers (4 starred, 3 Bib, 17 Recommended) | **Confirmed.** Names and tiers match the release. The 17 Recommended names match the release's Las Vegas list. | [MICHELIN press release, 31 Aug 2026](https://www.michelin.com/en/publications/products-and-services/michelin-guide-reveals-first-ever-southwest-restaurant-selection-in-the-u-s) · [Visit Las Vegas](https://www.visitlasvegas.com/michelin-guide-restaurants/) |
| Michael Mina (Bellagio) closed | **Confirmed** on Bellagio's dining index ("Temporarily Closed"). Reopen date not published. | [Bellagio dining index](https://bellagio.mgmresorts.com/en/restaurants.html?filter=property,Bellagio_Las_Vegas) |
| RTC Strip and All Access fares: $4 / $6 / $8 / $20 | **Confirmed** (regular fare). | [RTC fares & passes](https://www.rtcsnv.com/ways-to-travel/fares-passes/) |
| Route 203 Decatur → Las Vegas Blvd | **Corrected.** The timetable gives about 8–17 min across sampled rows (weekday eastbound 10–17 from pages 1–2; Saturday westbound 8–9 from page 3; pages 4–6 not read). The model's 14 min is a midpoint, not a published value. | [RTC Route 203 PDF](https://rtcws.rtcsnv.com/routePDF/203.pdf) |
| Venetian 60 m² Luxury King Suite, 15–22 Feb vs 8–15 Mar 2027 | **Contradicted.** Feb US$5,185.05; Mar €4,472.36 (EUR display); both incl. taxes and fees. The stored $2,407 / $3,757 are withdrawn (F-39). | [Booking.com Feb, USD](https://www.booking.com/hotel/us/the-venetian-resort-casino.de.html?aid=356980&checkin=2027-02-15&checkout=2027-02-22&group_adults=2&no_rooms=1&selected_currency=USD&sb_price_type=total&type=total) · [Booking.com Mar](https://www.booking.com/hotel/us/the-venetian-resort-casino.de.html?checkin=2027-03-08&checkout=2027-03-15&group_adults=2&no_rooms=1) |
| Palms Place room (studio, king + sofa bed, bathroom) | **Not confirmed** on palms.com (room specs absent from the fetched text). Kept, flagged (F-41). | [palms.com/palms-place](https://www.palms.com/palms-place/) · [palms.com/stay](https://www.palms.com/stay) |
| Per-night vs 7-night totals | **Inconsistent** on 17 of 42 rows, 16 properties (F-40). Shown as captured. | `data/hotels.json` (computed) |

**Changes made (all reversible from git):**

- `data/hotels.json`: Venetian prices set to null; the captures moved to `prices_withdrawn_2026_11_26`. F-40 added on 16 properties; F-41 on Palms Place.
- `data/price-windows.json`, `data/questions.json` (Q-06 → open), `data/suggestions.json` (S-01 → unproven): the "36% cheaper" headline removed.
- `data/transit.json`, `data/travel_matrix.json`: "14 min" wording changed to "8–17 min across sampled rows; 14 midpoint". Model values unchanged.
- `data/restaurants.json`: Michael Mina re-check note, F-43.
- `data/review-flags.json` (new): F-39 to F-46 plus confirmed items C-11 to C-13, each with source links.
- `scripts/gen_site.py`: `flagged.html` added to navigation and generated; sort and comparison code made safe for withdrawn values; headline cards and notes rewritten; anchors added to question cards.
- `executive-summary.md`, `README.md`, `FLAGS.md`: headline and counts corrected (12 pages, 312 links, 13 questions with 7 open, 19 restaurants with hours, 21 of 24 without a price for two).
- Generated: `docs/*` and root `*.html` (both regenerated by `scripts/gen_site.py`).

**Validation:** `scripts/build.py` passes; `scripts/gen_site.py` writes 12 pages; `scripts/validate.py` → 12 pages, 0 failures, 0 warnings, 312 external links, 0 broken anchors.

**Irregularities for review (F-46, logged, not all fixed):**

1. Task IDs on this board are reused (T10 appears twice; T1–T9 appears in two rows). Left as-is, since other sessions' references point at them.
2. Three Michelin datasets and three hotel datasets overlap. They agree on the 24 award names, but not on every hotel rate. A human should choose the canonical copy.
3. `docs/session-af795000/` and `docs/session-48dbf0ae/` still carry their own price claims, including that February is the cheapest week. Not updated; archived.
4. `pages/flagged.html` was an orphan (not linked, generated by no script). The canonical `flagged.html` replaces it in the nav. The orphan is left in place.
5. `data/flags.json` uses F07-style IDs; FLAGS.md uses F-07.
6. A Pages-related workflow run on `arena/48dbf0ae-vegas1` (run 45643448267) failed. Not on main; main's Pages builds succeed.
7. Instagram and TikTok: **zero** handles recorded for the 24 restaurants (F-19). The YouTube requirement is met for 24 of 24 (69 links). This is the largest gap against the brief.

**Not verified in this session (stay blank or flagged):** the 28 hotel rate rows other than the Venetian were not reproduced on their own engines (F-44); bed and bathroom for 29 of 32 hotels come from Booking.com rate blocks, not official pages; restaurant hours were not re-fetched beyond the Michael Mina check; activities were not re-fetched. A line-by-line check of every row was not possible in one session. This audit covered the headline claims and every stored-value conflict found by the consistency scan.

**Merge / PR:** PR #23 (arena/f527b427-vegas1 → main) merged with `--merge` at 2026-11-26T22:05:26Z, merge commit `b6b486ba1d6094701d618f37c8adeb9b1e4c1f90`. Pages build for that commit: success (run 45902487167); Pages API status `built`. Live check: `flagged.html` serves the audit sections and R-01…R-18. Post-merge fixes and this record go in a follow-up PR (see the PR and merge record for arena-f527b427-vegas1 below).

## PR and merge record — arena-b54b3346-vegas1 (R01) — 2026-11-26

- PR: https://github.com/kanlerxz87-cyber/Vegas1/pull/19 — merged with `--merge` at 2026-11-26T21:53:11Z, merge commit `c466c8b4fa88c58d95eaea23913fcdf1f05b4188`.
- Pages after merge: `pages build and deployment` on `main` completed with success; Pages API status `built`.
- Flagged irregularities F-01–F-07 did not block the merge. They are listed in `notes/repo-review-2026-11-26.md` and in this file.

## Coordination event — 2026-11-26 — arena-f527b427-vegas1

- **Ran into:** `main` moved while this session's PR was open. PRs #21 and #22 (arena-939a824e-vegas1, T12) had merged a Flagged page, Repo review page, and cross-reference fixes over the same files (`scripts/gen_site.py`, README, executive summary, generated `docs/**`).
- **Resolution:** integrated by `git merge origin/main` on `arena/f527b427-vegas1`, not discarded. Their R-01…R-18 register and Repo review page are kept. Our F-39…F-46 audit and `data/review-flags.json` are rendered as sections on the same `flagged.html`. Our headline wording (withdrawn Venetian claim) stays. Their property-specific caveat (Caesars Palace and Flamingo, February cheaper on their own engines) is kept in the README and summary.
- **Duplicate ID:** our T12 is renamed T14 on the board (T13 is taken by arena-c419e2da-vegas1). The R-items and T12 rows from the other session are unchanged.
- **Nothing else from the other session was overwritten.**

## PR and merge record — arena/c419e2da-vegas1 (T13) — 2026-11-26

- PR #24: https://github.com/kanlerxz87-cyber/Vegas1/pull/24 — merged with `--merge` at 2026-11-26T22:00:35Z; merge commit `768f5aacd704ee3ba06edc6a5e0254a8462ea48e`.
- Pages deployment run: https://github.com/kanlerxz87-cyber/Vegas1/actions/runs/45901945140 — success; Pages API status `built`.
- Cache-busted live check: https://kanlerxz87-cyber.github.io/Vegas1/?ver=20261126 showed the revised mixed-source date claim; https://kanlerxz87-cyber.github.io/Vegas1/flagged.html showed the published F-29/F-30 register.
- Local verification: `python3 scripts/build.py`, `python3 scripts/gen_site.py`, `python3 scripts/validate.py` — 13 pages, 0 failures, 0 warnings; `git diff --check` clean.
- Rate-source caveat remains open by design; no universal cheapest-week or official-rate-only comparison is claimed. See F-29/F-30 and Q-06.

## PR and merge record — arena-f527b427-vegas1 (T14) — 2026-11-26

- **PR #23** https://github.com/kanlerxz87-cyber/Vegas1/pull/23 — merged with `--merge` at 2026-11-26T22:05:26Z, merge commit `b6b486ba1d6094701d618f37c8adeb9b1e4c1f90`. Flagged items did not block the merge.
- **Pages:** build for `b6b486b` succeeded (run 45902487167); API status `built`. Live `flagged.html` checked by fetch: serves R-01…R-18 and the F-39…F-46 audit sections.
- **Race with `main`:** `main` moved four times while PR #23 was open (PRs #24, #25, #26, #28 from other sessions). Each time it was integrated with `git merge origin/main`, not rebased. A `git pull --rebase` on a branch that already contained merged `main` history replayed other sessions' commits and stopped with a conflict. It was aborted (`git rebase --abort`); nothing was lost and no force-push was used.
- **Overlap resolved:** T12 ID duplicated (other session's T12 merged first). Our row is T14. Our flag register is F-39…F-46 (main keeps F-29/F-30 for rate basis and rate refresh). Our confirmed items are C-11…C-13 (main uses C-01…C-10).
- **Follow-up PR** (this record and these fixes): removed orphan `pages/flagged.html` (unlinked, 11 broken links; replaced by generated `flagged.html`). Corrected the Venetian room attribution: the US$5,185.05 row's room name was not seen in the chunks read, so it is now marked unverified. Widened the Route 203 range to 8–17 min across sampled rows (weekday eastbound 10–17 from PDF pages 1–2; Saturday westbound 8–9 from page 3); pages 4–6 still unread.
- **Not verified in this session (left blank or flagged):** Route 203 pages 4–6; hotel `official_url` links (F-27/R-08); Instagram and TikTok handles (R-02); hotel rates beyond the Venetian and per-night reconciliation (F-40).

