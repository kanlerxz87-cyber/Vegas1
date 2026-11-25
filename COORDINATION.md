# Coordination Board — Vegas1

Shared task board for parallel agent sessions. Read before starting; claim before working; `git pull --rebase` before every push.

**Branch rule:** sessions work on their assigned branch only (this session: `arena/c515279e-vegas1`). Branch names in the older `session-<id>/<task>` convention are not used here because Arena binds each session to one branch.

**Status values:** unclaimed · in progress · done · needs review (needs review = published on the Flagged for Review page; does not block anything)

## Task board

| ID | Task | Status | Owner (session) | Branch | File scope |
|---|---|---|---|---|---|
| T1 | Repo review: line-by-line check of repo contents and irregularities | in progress | c515279e | arena/c515279e-vegas1 | `README.md`, `COORDINATION.md`, `docs/data/repo-review.json` |
| T2 | Michelin restaurants, Las Vegas (stars, Bib Gourmand, Recommended) | in progress | c515279e | arena/c515279e-vegas1 | `docs/data/michelin.json` |
| T3 | Hotel candidates: room, bed, bath facts from official hotel sites; price fields left unverified | in progress | c515279e | arena/c515279e-vegas1 | `docs/data/hotels.json` |
| T4 | Activities and attractions with official links and hours | in progress | c515279e | arena/c515279e-vegas1 | `docs/data/activities.json` |
| T5 | Site build: landing page, category subpages, executive summary, suggestions, questions, flagged-for-review page | in progress | c515279e | arena/c515279e-vegas1 | `docs/` (site files) |
| T6 | Integration: merge branches, re-verify combined data, check links, publish to GitHub Pages | unclaimed | — | — | `docs/`, `README.md` |

## Activity log

- **2026-11-25 · c515279e** — Claimed T1–T5 on `arena/c515279e-vegas1`. Repo at base commit `9b8bcfa` contained only `README.md`; no `COORDINATION.md` existed, so this file was created.
