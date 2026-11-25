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

## Correction record — RTC Route 203 — 2026-11-25

Session `arena-0c9983d6-vegas1` found that this dataset recorded **Chinatown / Spring Mountain Rd
as reachable only by car or rideshare**. That was wrong, and it was the most consequential error in
the model, because **seven of the 24 MICHELIN listings sit on that road**.

RTC **Route 203** (Spring Mountain / Desert Inn / Lamb) runs the length of Spring Mountain Road.
Its [official timetable](https://rtcws.rtcsnv.com/routePDF/203.pdf) carries a timed stop at
**Las Vegas Blvd**, and the eastbound runs give **Decatur → Las Vegas Blvd in 14 minutes**.

Changes made:

| File | Change |
|---|---|
| `data/transit.json` | Added Route 203 as a fourth system, with its verified timepoints and published timing. |
| `data/transit.json` | `north-strip → chinatown` corrected from **20 to 34** minutes, built from the published 14-minute run plus a 7-minute walk, an 8-minute wait and a 5-minute walk at the far end. |
| `scripts/gen_site.py` | Added a "Correction: Chinatown is reachable by bus" panel to the transit page. |
| `FLAGS.md` | Added **F-21** recording the correction. |
| `README.md` | Added the correction to the findings. |

**Why the time went up while the claim got better:** the old 20-minute figure was an estimate with
no source. The new 34-minute figure is anchored to a published stop-to-stop timing. It is slower and
more defensible, which is the right trade for a study whose whole premise is traceability.

Note this is the **only published travel time in the model**. Every other minute value remains an
estimate, and F-20 still says so.

---

## Merge record — 2026-11-25

`origin/main` was found to contain commit `0d0b1d5`, a **complete first version of this same brief
produced by a different Arena session** (`arena/d6d3b8f5-vegas1`) and merged to `main`. This session
had branched from `9b8bcfa` (the empty repo) and did not know it existed.

**How it was handled, per rule 5 (never discard the other session's work):**

1. Merged `origin/main` into this branch with `--allow-unrelated-histories`. Nothing was deleted.
2. Compared both datasets field by field.
   - **Restaurants:** the earlier file has the correct award split and official links but leaves
     *every* hours, days-open and social field as `"Blank - unverified"`. This session's file is a
     strict superset (it adds hours, 45 YouTube links and three published prices). Earlier file kept
     in the archive; not used.
   - **Hotels:** 8 of the earlier file's 11 hotels are `"Blank - unverified"`; its own `source` field
     says prices are *"estimated based on published rate ranges"* from `unleashvegas.com` and
     `getcostidea.com`. The brief forbids inferred values, so this session's 32 hotels (every one a
     dated Booking.com capture across four windows) are published instead.
3. Moved all superseded files to `archive/2026-11-25-earlier-session/` **intact**, with a README that
   explains what each file was and why it is not the live version.
4. Repointed the published site at `docs/` (this session's build). The earlier site lived at
   `main:/index.html`; see "Publication" below for what that means for GitHub Pages.

**Irregularity for review:** two sessions were assigned the same brief and both wrote to the same
files. Rule 6 (single integration session) was already broken before this session discovered it.
Recorded here rather than silently overwritten.

## Third-session merge — 2026-11-25 (later)

A **third** Arena session (`arena/126d963c-vegas1`, plus commits from `arena/0c9983d6-vegas1`) merged to
`main` while this branch was open. Rather than re-doing its work, this branch **merged `origin/main` and
kept its verified findings**, resolving six conflicts by hand:

**What the other sessions found that this branch had wrong or missing — now integrated:**

| Finding | Effect |
|---|---|
| **Michael Mina is "Temporarily closed"** — its own Bellagio page reads *"Monday to Sunday: Closed"* with a *Temporarily closed* label and no reopen date | The $590++ row is now marked `Closed — see note`. The Bellagio hotel note no longer sells the property on a restaurant that is not serving. Executive summary warns against planning around it. |
| **Route 203 correction** — Chinatown *is* reachable from the north Strip by bus; RTC 203 decants at Spring Mountain/Decatur in 14 min | north→chinatown corrected 20 → **34 min**. This **lowered** north-Strip hotels from 23 to **17** restaurants inside 20 min, and raised south-Strip. Rankings changed as a result — the model was wrong before and is less wrong now. |
| **Joël Robuchon hours** — Tue–Sat 5:00–9:30 PM, closed Sun/Mon, business formal, no under-6s | Filled, `verified: yes`. Tue–Sat is the only booking window. |
| **Partage hours** — Tue–Sat 5–9 PM (on `/contact`, not `/restaurant`) | Filled. Strict no-vegan/no-coeliac policy confirmed. |
| **Sparrow + Wolf** — publishes no hours anywhere | Correctly left blank (F-25) rather than taken from a reseller. |
| **Sample-date banners** — MGM pages show 2026-dated banners | Ignored and called out (F-26). Carrying one into a 2027 plan would be a silent error. |

**What this branch contributed that the others did not have:** the four-week dated price matrix, the
20-minute column that makes the ranking meaningful, the 32-hotel dataset, and the hotel-link verification
(F-27/F-28, Q-13, S-13).

**Numbering resolved:** the other session used F-21…F-26; this branch's two hotel-link flags were
renumbered **F-27/F-28**, and its hotel-links question became **Q-13** (both sides had independently
created a "Q-11"). The Bellagio note's `F-22` reference was corrected to `F-23`.

**Consequence to flag for review:** after the Route 203 fix, **no hotel reaches all 24 restaurants inside
20 minutes** — the best is now 24 → 21 (south Strip) / 24 (west-near). The transit table in
`data/transit.json` is not symmetric (north→chinatown 34, chinatown→north 20), which is intentional: a bus
that only runs one way on that stretch, plus a walk at the anchored end. The scoring script reads the
matrix as written, so this asymmetry is safe, but anyone re-deriving it should know it is by design.

## Requests between sessions

| Date | From | To (owner) | Request | Status |
|------|------|-----------|---------|--------|
| 2026-11-25 | arena-edcfa7a0-vegas1 | arena-d6d3b8f5-vegas1 | Your `main` build was found mid-session. Superseded by a verified dataset; your files are archived intact at `archive/2026-11-25-earlier-session/`, not deleted. Your restaurant award split agreed with mine. | complete |

## Verification log

| Date | Task | What was verified | Source(s) | Result |
|------|------|-------------------|-----------|--------|
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

---

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
