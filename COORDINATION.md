# COORDINATION.md — Shared Task Board

**Project:** Trip Planning — Las Vegas (Feb 15 2027 – Mar 23 2027 window; preferred Feb 15–18, 2027)
**Repo:** `kanlerxz87-cyber/Vegas1`
**Current branch:** `arena/4d41b902-vegas1`
**This session ID:** `session-planner-01`

This file is the single source of truth for task ownership. Statuses:
`unclaimed` · `in progress` · `needs review` · `done`

A task marked `needs review` is published on the Flagged for Review page and does not block anything.
Sessions claim a task by writing their session ID + file scope here, then committing and pushing the claim
immediately. Scopes must be non-overlapping. Shared outputs (index/navigation, combined table data) are
changed only by the final integration session once all tasks are done.

---

## Task Board

| ID | Task | Status | Owner | File scope | Notes |
|----|------|--------|-------|-----------|-------|
| T1 | Repo setup: coordination board, site skeleton, Git Pages config | done | session-planner-01 | `COORDINATION.md`, `.gitignore`, `.nojekyll`, `assets/`, `index.html` | Skeleton committed; data filled in later tasks |
| T2 | Research Michelin Las Vegas restaurants (stars + guide-listed) | in progress | session-planner-01 | `data/restaurants.json`, `restaurants.html` | Verify each on guide.michelin.com |
| T3 | Research + rank hotels (price, location, amenities, Michelin density) | in progress | session-planner-01 | `data/hotels.json`, `hotels.html` | Private bath, queen+ bed, 2 adults |
| T4 | Research activities within 1 hour of hotel (transit) | in progress | session-planner-01 | `data/activities.json`, `activities.html` | Bus/monorail travel ≤ 1h |
| T5 | Pricing research (hotel 7-night total; restaurant total for 2) | in progress | session-planner-01 | `data/pricing.json`, `pricing.html` | Real verified pricing, actual dates |
| T6 | Media links (YT/TikTok/IG) + days/hours/exceptions for restaurants & activities | in progress | session-planner-01 | `data/*.json` (media fields), `*.html` | Every row needs a source link |
| T7 | Build site pages (landing + category subpages, dashboard UI) | in progress | session-planner-01 | all `*.html`, `assets/` | Mobile-first, clean tables |
| T8 | Verification pass (line-by-line, source links, flag unverified) | in progress | session-planner-01 | `verification.html`, `data/*.json` | Blank + flag if not confirmable |
| T9 | Executive summary + suggestions + open questions | in progress | session-planner-01 | `summary.html`, `suggestions.html` | Decision-support section |
| T10 | Integrate, re-verify, deploy GitHub Pages, confirm live | pending | session-planner-01 | repo-wide | Final integration |

---

## Handoff / Conflict Log

(none yet)

## Verification Log

(filled per task as tasks complete)

## Irregularities / Flags for Review

(filled as discovered)
