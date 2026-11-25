# COORDINATION.md — Vegas1 Trip Planning (shared task board)

This is the shared task board. Each task has: a status, an owning session ID, and the
files it touches. Sessions coordinate here to avoid conflicts and duplicate work.

**Current session:** `arena/6263258d-vegas1` (branch `arena/6263258d-vegas1`, base `9b8bcfa`).
This session is the **integration session**: it performs research, builds the site,
re-verifies the combined data line by line, and publishes to GitHub Pages.

> Note on branch naming: the coordination guide suggests per-task branches named
> `session-<id>/<task>`. Because this session is the only active session and the
> Arena runtime pins this session to the current branch, all work is committed to the
> current branch `arena/6263258d-vegas1`. Scopes are still kept non-overlapping by
> file so a future parallel session can take over cleanly.

## Legend
- `unclaimed` — not yet owned by any session
- `in progress` — claimed and being worked
- `needs review` — published on the Flagged for Review page; does not block others
- `done` — finished; sources, verification, irregularities recorded

## Tasks

| # | Task | Status | Session | File scope | Notes |
|---|------|--------|---------|------------|-------|
| 1 | Repo review & coordination setup | done | arena/6263258d-vegas1 | `COORDINATION.md`, `README.md` | Greenfield repo; only `README.md` (`# Vegas1`) existed at base. |
| 2 | Hotel research & selection (price/location/amenities, private bathroom, queen+ bed, 2 adults) | in progress | arena/6263258d-vegas1 | `data/hotels.json`, `data/hotels.csv`, `src/hotels.html` | See sources in task log below. |
| 3 | Michelin restaurant research, clustering, star vs listed | in progress | arena/6263258d-vegas1 | `data/michelin.json`, `data/michelin.csv`, `src/michelin.html` | Las Vegas Michelin Guide editions. |
| 4 | Activities research (≤1h travel from hotels) | in progress | arena/6263258d-vegas1 | `data/activities.json`, `data/activities.csv`, `src/activities.html` | |
| 5 | Hotel ranking by Michelin restaurant density within 1h (bus/subway) | in progress | arena/6263258d-vegas1 | `src/ranking.html`, `data/ranking.json` | Las Vegas has NO subway — uses RTC bus + Monorail; flagged. |
| 6 | Pricing & booking-window analysis (7-night total, cheapest upcoming date) | in progress | arena/6263258d-vegas1 | `src/pricing.html`, `data/pricing.json` | Dynamic pricing; sources cited, dynamic flagged. |
| 7 | Social media links (YouTube/TikTok/Instagram) per restaurant/activity | in progress | arena/6263258d-vegas1 | within `data/*.json`, shown in tables | |
| 8 | Site build: landing + category subpages, mobile-friendly dashboard | in progress | arena/6263258d-vegas1 | `index.html`, `src/*.html`, `assets/*` | Static site, no build step. |
| 9 | Executive summary, suggestions, open questions | in progress | arena/6263258d-vegas1 | `src/summary.html`, `src/suggestions.html`, `src/questions.html` | |
| 10 | Line-by-line verification & Flagged for Review page | pending | arena/6263258d-vegas1 | `src/verified.html`, `src/flagged.html`, `data/verification.json` | Every row needs a source link. |
| 11 | GitHub Pages publication + build check (no broken links) | pending | arena/6263258d-vegas1 | `.github/workflows/*`, `gh` Pages settings | Final integration step. |

## Task log (sources, verification, irregularities)

### Task 1 — Repo review
- **Repo state at base `9b8bcfa`:** single file `README.md` containing `# Vegas1`. No source,
  docs, or site files. Greenfield.
- **Irregularity:** repository contains no prior work, no package manifest, no existing ignore
  files. Created `.gitignore` to keep build artifacts out of Git.

<!-- Each completing session appends a dated entry here with: sources used,
     verification performed (with links), and any irregularities flagged. -->
