# COORDINATION — Multi-session task board

**Repo:** kanlerxz87-cyber/Vegas1
**Branch convention:** `session-<id>/<task>` (this session's branch is fixed by Arena as `arena/f9e78242-vegas1`)
**Rules:** Claim a task by writing your session ID + file scope here, commit + push the claim immediately. Never start a task another session has claimed. Keep scopes non-overlapping. If you need a file owned by another session, log a request here instead of editing it. Run `git pull --rebase` before every push. A claim >60 min old with no commits may be taken over (note the handoff in the log).

---

## Session registry

| Session ID | Branch | Task scope | Status | Started (UTC) |
|---|---|---|---|---|
| `session-f9e78242` | `arena/f9e78242-vegas1` | **FULL BUILD** — repo audit, Michelin dataset, hotel dataset, pricing research, activities, social links, site (all pages), verification log, flag page, integration + Pages publish | in progress | 2026-11-25 |

> At time of writing, COORDINATION.md did not exist and the repository contained only a 1-line `README.md` (commit `9b8bcfa`). No other session has claimed any scope, so `session-f9e78242` claims the whole build to avoid a blocked start. **Any later session must not edit files in this session's scope without logging a request below.**

---

## Task board

| # | Task | Status | Owner | File scope |
|---|---|---|---|---|
| T1 | Repo audit + COORDINATION.md bootstrap | done | session-f9e78242 | `COORDINATION.md`, `docs/audit/repo-audit.md` |
| T2 | Michelin dataset (stars / Bib / Recommended) | in progress | session-f9e78242 | `data/michelin.json`, `docs/verification/michelin.md` |
| T3 | Hotel shortlist (price/location/amenities, bed & bathroom) | in progress | session-f9e78242 | `data/hotels.json`, `docs/verification/hotels.md` |
| T4 | 7-night pricing by date window | in progress | session-f9e78242 | `data/pricing.json`, `docs/verification/pricing.md` |
| T5 | Transit-time matrix (hotel → restaurant, ≤60 min) | in progress | session-f9e78242 | `data/transit.json` |
| T6 | Activities (≤60 min) + hours | in progress | session-f9e78242 | `data/activities.json` |
| T7 | Social/video links per restaurant & activity | in progress | session-f9e78242 | `data/social.json` |
| T8 | Site build (landing + category subpages, mobile-first) | unclaimed → will claim | session-f9e78242 | `docs/**` |
| T9 | Executive summary, suggestions, open-questions sections | unclaimed → will claim | session-f9e78242 | `docs/executive-summary.md`, `docs/suggestions.md`, `docs/open-questions.md` |
| T10 | Verification pass + Flagged for Review page | unclaimed → will claim | session-f9e78242 | `docs/flagged.html`, `data/flags.json` |
| T11 | Integration: build check, broken-link check, Pages publish | unclaimed → will claim | session-f9e78242 | `.github/workflows/pages.yml`, `docs/` |

---

## Requested changes to files owned by another session

_(none yet)_

## Merge-conflict log

_(none yet)_

## Handoff log

_(none yet)_
