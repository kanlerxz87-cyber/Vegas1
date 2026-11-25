# COORDINATION.md — Vegas1 Trip Planning (Las Vegas)

Shared task board. One row per task. Statuses: `unclaimed`, `in progress`, `done`, `needs review`.

## Session / branch note
- **Coordinating session ID:** `2d99ac1f`
- **Branch:** `arena/2d99ac1f-vegas1` (fixed by the Arena harness — sessions must not switch or create branches).
  - Coordination convention asks for `session-<id>/<task>` branches. That conflicts with the harness
    requirement to work only on the current branch, so **all tasks are claimed and worked on
    `arena/2d99ac1f-vegas1`**. No parallel branching is possible in this sandbox; this session is the
    sole worker and also performs final integration. If another session joins, it must claim an
    *unclaimed* task below and note the branch constraint here.
- **Commits:** frequent, on the current branch. Push with `git pull --rebase` before each push.

## Trip parameters (fixed requirements)
- Destination: **Las Vegas, NV, USA**.
- Duration: **1–2 weeks**; travel window **2027-02-15 → 2027-03-23**.
- **Preferred vacation window: 2027-02-15 → 2027-02-18** (shortest option).
- Travelers: **2 adults (a couple)**.
- Hotel must have **private bathroom** and **queen bed or larger**.
- Activities must be **≤ 1 hour travel** from the hotel (subway/bus where applicable).
- Hotels ranked by **number of Michelin restaurants within 1 hour travel (subway/bus)**.
- Hotel cost presented as **total price for a 7-night stay**; cheapest upcoming booking window with real dates.
- Michelin restaurant cost presented as **total for 2 adults** (exact or estimate range).

## Task board
| Task | Status | Owner | File scope (non-overlapping) |
|------|--------|-------|-------------------------------|
| T1 — Requirements capture + executive summary | in progress | 2d99ac1f | `data/requirements.md`, `index.html` |
| T2 — Hotel research (amenities, price/7-night, booking window) | in progress | 2d99ac1f | `data/hotels.md`, `pages/hotels.html` |
| T3 — Michelin restaurants (starred vs listed, cost, hours, location) | in progress | 2d99ac1f | `data/michelin.md`, `pages/michelin.html` |
| T4 — Activities (≤1h travel, hours, links, social) | in progress | 2d99ac1f | `data/activities.md`, `pages/activities.html` |
| T5 — Social media links (YouTube/TikTok/Instagram) per entry | in progress | 2d99ac1f | within each `data/*.md` + subpage table |
| T6 — Site build (landing + subpages, mobile-friendly dashboard UI) | in progress | 2d99ac1f | `src/styles.css`, `src/app.js`, all HTML |
| T7 — Verification: sources + flagged-for-review page | in progress | 2d99ac1f | `data/sources.md`, `pages/review.html` |
| T8 — Suggestions + open-questions section | in progress | 2d99ac1f | `data/suggestions.md`, `pages/suggestions.html` |
| T9 — Final integration: merge, re-verify, build check, publish GitHub Pages | unclaimed | 2d99ac1f (integrator) | all files (integration only) |

## Integration / publication
- Integrator re-verifies combined data line by line, confirms the site builds and has no broken links,
  then enables GitHub Pages. Record sources + verification notes here when done.

## Handoff / irregularity log
- (none yet)
