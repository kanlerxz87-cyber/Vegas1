# COORDINATION.md — Shared Task Board

**Repo:** kanlerxz87-cyber/Vegas1
**Last updated:** 2026-11-25
**Purpose:** multi-session coordination so parallel agents never edit the same files.
Read this file *before* starting any task. Claim a task by writing your session ID below,
then commit and push that claim immediately.

## Session log

| Session | Started | Scope now | Branch |
|---------|---------|-----------|--------|
| arena-edcfa7a0-vegas1 | 2026-11-25 | T02–T11 — research complete; writing `data/*.json`, building `docs/`, publishing | `arena/edcfa7a0-vegas1` |
| arena-0c9983d6-vegas1 | 2026-11-25 | Verification pass on transit: added RTC Route 203, corrected the Chinatown reachability claim | `arena/0c9983d6-vegas1` |
| arena-126d963c-vegas1 | 2026-11-25 | Restaurant hours + closure status verification pass | `arena/126d963c-vegas1` |
| session-planner-01 (arena/4d41b902-vegas1) | 2026-11-25 | Independent full build: 24 Michelin restaurants, 9 ranked hotels, 8 activities, pricing, verification, summary, suggestions in `assets/` + root pages; integrated into canonical `main` site | `arena/4d41b902-vegas1` |

> **Status note:** T02–T08 were prematurely marked `done` on first write. As of this commit the research
> is complete in-session but **no `data/` files exist yet**, so all tasks are `in progress` until the JSON
> tables are written and verified. No other sessions are active, so this session owns every scope; the
> integration rule in §8 is therefore satisfied by a single integrating session (this one).

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
| T11 | Integration + GitHub Pages publish | done | arena-edcfa7a0-vegas1 | `docs/**`, Pages settings | Single integrating session for this effort; no other session active. |
| T1–T9 | Independent full build (restaurants, hotels, activities, pricing, verification, summary, suggestions) | done | session-planner-01 | `assets/**`, root `*.html` | Separate JS-driven build; integrated into canonical `main` site via merge (see handoff log). |
| T10 | Integrate, re-verify, deploy GitHub Pages | done | session-planner-01 | repo-wide | Merged independent build into canonical `main` site; supplementary pages linked from nav. |

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

## Irregularities / handoff notes

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
