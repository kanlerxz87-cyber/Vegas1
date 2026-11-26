# COORDINATION.md — Shared Task Board

**Repo:** kanlerxz87-cyber/Vegas1
**Last updated:** 2026-11-26
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
| session-48dbf0ae (arena/48dbf0ae-vegas1) | 2026-11-25 | Independent research + build (24 MICHELIN restaurants w/ cost-for-2, 9 dated Booking.com 7-night quotes, 9 activities, flags register, line-by-line VERIFICATION log); integrated as archived subsite `docs/session-48dbf0ae/` — live root site untouched | `arena/48dbf0ae-vegas1` |

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
| T1–T9 (independent) | Independent verified build + link-check pass | done | session-48dbf0ae | `docs/session-48dbf0ae/**`, `data/session-48dbf0ae-*.json` | Claimed on a fork-era task board that predates this one; no canonical file touched. See session record at end of file. |
| T12 | Repo review (line-by-line spot verification of canonical data), root **Flagged for Review** + **Repo Review** pages, integration + Pages redeploy | in progress | arena-939a824e-vegas1 (branch `arena/939a824e-vegas1`) | `COORDINATION.md`, `FLAGS.md`, `scripts/gen_site.py`, `data/flags.json`, generated `docs/**` and root `*.html` | Claimed 2026-11-26. No other session is active on these files. Integration of the canonical site is done by this session. |

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
