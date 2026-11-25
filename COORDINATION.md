# COORDINATION.md — Vegas1 Trip Planning (Las Vegas)

Shared task board. One row per task. Statuses: `unclaimed`, `in progress`, `done`, `needs review`.

## Session / branch note
- **Coordinating session ID:** `2d99ac1f`
- **Branch:** `arena/2d99ac1f-vegas1` (fixed by the Arena harness — sessions must not switch or create branches).
  - Coordination convention asks for `session-<id>/<task>` branches. That conflicts with the harness
    requirement to work only on the current branch, so all tasks were claimed and worked on
    `arena/2d99ac1f-vegas1`.
- **Commits:** frequent, on the current branch.

## ⚠ RECONCILIATION / FINAL STATUS (read first)
This session (`2d99ac1f`) independently built a complete site on `arena/2d99ac1f-vegas1` and pushed it.
While finalising integration it discovered that **parallel sessions had already produced a more
complete, verified, integrated site that is LIVE on `main`**:

- **Live site:** https://kanlerxz87.github.io/Vegas1/ → https://kanlerxz87-cyber.github.io/Vegas1/
- **Parallel sessions:** `arena-edcfa7a0-vegas1` (T02–T11 research + `data/*.json` + `docs/` + publish),
  `arena-0c9983d6-vegas1` (transit verification / Route 203 correction),
  `arena/126d963c-vegas1` (restaurant-hours verification pass), and others.
- **Their integrated site** covers: 24 MICHELIN listings (4 starred / 3 Bib / 17 Recommended), 32 hotels
  ranked with both a ≤20-min and a ≤60-min Michelin-reach column, a multi-week price comparison
  (finding **8–15 March 2027 is the cheap week**, ~36–57% below the Presidents'-Day week), a
  verification pass correcting hours (Joël Robuchon Tue–Sat; Michael Mina **temporarily closed**),
  `FLAGS.md` with F-01…F-25, and a clean build pipeline (`scripts/build.py`, `gen_site.py`, `validate.py` →
  8 pages, 0 failures, 0 warnings).

**File overlap:** this session's files (`index.html`, `hotels.html`, `activities.html`,
`suggestions.html`, `data/`) share names with the integrated `main` versions. Per coordination rules
(#5 resolve without discarding other sessions' work; #8 shared outputs changed only by the integration
session), **this session did NOT force-push to `main`**, because doing so would clobber the coordinated,
verified, live deliverable. The live site on `main` **satisfies the task**; this branch is retained as
an independent, superseded build for reference.

## Deployment note
The sandbox proxy blocks the GitHub Pages configuration APIs (`PUT /repos/.../pages/source` and
`PUT /repos/.../actions-enabled` both return 404) and the Actions log host, and custom Actions
workflows cannot acquire a runner (jobs fail with 0 steps). The live site is therefore published by the
**built-in "Deploy from a branch" Pages builder on `main`** (the parallel integration session's path),
which builds and serves successfully. This session's `.github/workflows/deploy.yml` is retained on its
branch only and was not used for the live publish.

## Trip parameters (fixed requirements)
- Destination: **Las Vegas, NV, USA**. Duration **1–2 weeks**; window **2027-02-15 → 2027-03-23**.
- **Preferred window: 2027-02-15 → 2027-02-18** (3 nights; hotel pricing verified for a **7-night stay
  2027-02-15 → 2027-02-22**).
- Travelers: **2 adults (a couple)**. Hotel: **private bathroom** + **queen bed or larger**.
- Activities **≤ 1 hour travel**; hotels ranked by **# Michelin restaurants within 1 hour (subway/bus)**.

## Task board (this session's independent build)
| Task | Status | Owner | File scope |
|------|--------|-------|-----------|
| T1 — Requirements capture + executive summary | done | 2d99ac1f | `data/requirements.md`, `index.html` |
| T2 — Hotel research | done | 2d99ac1f | `hotels.html` |
| T3 — Michelin restaurants (starred vs listed, cost, hours) | done | 2d99ac1f | `michelin.html` |
| T4 — Activities | done | 2d99ac1f | `activities.html` |
| T5 — Social media links | done | 2d99ac1f | within `michelin.html`, `activities.html` |
| T6 — Site build (landing + subpages, mobile UI) | done | 2d99ac1f | `src/styles.css`, `src/app.js`, HTML |
| T7 — Verification: sources + flagged-for-review page | done | 2d99ac1f | `data/sources.md`, `review.html` |
| T8 — Suggestions + open questions | done | 2d99ac1f | `suggestions.html` |
| T9 — Integration / publish | **superseded** | 2d99ac1f | live publish handled by parallel session on `main` |

## Sources verified by this session
- **Michelin (official):** 2026 MICHELIN Guide Southwest starred list
  (`guide.michelin.com/.../guide-michelin-southwest`) + full press release with addresses
  (`michelin.com/.../michelin-guide-reveals-first-ever-southwest-restaurant-selection-in-the-u-s`).
  Hours: `guide.michelin.com` (Joël Robuchon), `ebyjoseandres.com` (é), `mgmgrand.mgmresorts.com` (L'Atelier),
  `opentable.com` (China Poblano).
- **Hotels (official, date-specific):** Booking.com Las Vegas, **2027-02-15 → 2027-02-22, 2 adults, USD**,
  taxes & fees included (captured 2026-11-25).
- **Transit:** `unleashvegas.com`, `lasvegascompass.com`, `lvmonorail.com` (Deuce + Monorail fares/hours).
- **Activities:** `lasvegaswonders.com`, `my-travelmonkey.com`, `viator.com`, `tripadvisor.com`.
- **Restaurant costs:** `stubbornseed.com`, `newsroom.mgmresorts.com`, `lasvegaswonders.com`, `lasvegascompass.com`.
- **Social:** Instagram `@joelrobuchon.lasvegas`, `@guysavoylasvegas`, `@bellagio`, `@spherevegaslv`.

## Verification performed by this session
- Michelin: 24 Las Vegas distinctions + addresses cross-checked against the two official Michelin sources.
- Hotels: 5 properties with bed type, amenities, rating, 7-night USD total verified on Booking.com for the exact dates.
- Transit: Deuce/Monorail fares and hours verified against operator sources.
- Build check: all internal links resolve; all referenced assets exist; HTML tag-balance validation PASS.
- Discipline: no value inferred; unconfirmed values left blank + flagged `UNVERIFIED` on `review.html`.

## Irregularities / flags (this session's build)
1. Bed not guaranteed at Flamingo, Horseshoe, Planet Hollywood ("assigned on arrival").
2. Resort fees may be extra (not confirmed in Booking.com totals) — UNVERIFIED.
3. Promotional "Black Friday Deal" rates, dynamic, for 2027-02-15 → 02-22 only.
4. 17 "Michelin Selected" restaurants hold no star (listed, not starred).
5. Las Vegas has no subway — "subway or bus" maps to Deuce + Monorail + RTC buses.
6. The ≤1-hour Michelin-reach metric is effectively tied (≈23/24) for Strip hotels — the parallel session's
   site resolves this with a ≤20-minute ranking column.
7. Estimated transit times — confirm via RTC trip planner / Google Maps.

## Handoff / irregularity log
- Single-session independent build; then discovered parallel sessions' integrated live site on `main`.
- **No merge conflict encountered** because this session deliberately did **not** push to `main`.
- Branch constraint reconciled: worked on the fixed `arena/2d99ac1f-vegas1` branch.
- Live deliverable = the integrated site on `main` (published by the parallel integration session).
