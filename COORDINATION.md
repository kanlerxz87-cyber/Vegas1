# COORDINATION

Shared task board for parallel agent sessions working in this repository.

**Session:** `arena/0c9983d6` · branch `arena/0c9983d6-vegas1` · started from `9b8bcfa`

## Rules

1. Read this file before starting. Never begin a task another session has claimed.
2. Claim a task by adding your session id to its row **before** you edit files.
3. Keep file scopes non-overlapping. If you need a file another session owns, request it here
   rather than editing it.
4. Commit in small increments with specific messages. Run `git pull --rebase` before every push.
5. Shared outputs — the table data, the nav and the index page — are only changed by the final
   integration session, so parallel edits cannot clobber each other.
6. Log conflicts and handoffs in the log at the bottom.
7. Verification standard: every table row carries a link to an official source. A value that
   cannot be confirmed officially is left **blank and flagged**, never inferred.

## Status: integration complete

All tasks below are finished on this branch. The board is left in place so a future session
can see what was done and what scopes were touched.

| ID | Task | File scope | Session | Status |
|---|---|---|---|---|
| T1 | MICHELIN restaurant data: 24 entries, distinctions, hours, prices, socials | `data/restaurants.json` | `arena/0c9983d6` | **Done** |
| T2 | Hotel data: 7-night totals for real dates, room and amenity verification | `data/hotels.json` | `arena/0c9983d6` | **Done** |
| T3 | Activities: Fountains, High Roller, Sphere calendar | `data/activities.json` | `arena/0c9983d6` | **Done** |
| T4 | Transit facts: Monorail stations, hours, fares; RTC fares and Route 203 | `data/transit.json` | `arena/0c9983d6` | **Done** |
| T5 | Travel matrix generator — the reproducible model behind the ranking | `tools/build_matrix.py`, `data/travel_matrix.json` | `arena/0c9983d6` | **Done** |
| T6 | Static site builder, no dependencies | `build.py`, `assets/style.css` | `arena/0c9983d6` | **Done** |
| T7 | Generated site and Pages mirror | `site/`, `docs/` | `arena/0c9983d6` | **Done** |
| T8 | Repo review, verification record, publishing notes | `REPO_REVIEW.md`, `VERIFICATION.md`, `PUBLISHING.md`, `README.md` | `arena/0c9983d6` | **Done** |
| T9 | Open questions, suggestions and the flagged-for-review page | `build.py` page functions | `arena/0c9983d6` | **Done** |

## File scopes claimed by this session

`data/`, `tools/`, `build.py`, `assets/`, `site/`, `docs/`, `README.md`, `.gitignore`,
`REPO_REVIEW.md`, `VERIFICATION.md`, `PUBLISHING.md`, `COORDINATION.md`

## Publication

GitHub Pages serves from `docs/` on `main`. See `PUBLISHING.md`.

## Log

| Date | Entry |
|---|---|
| 2026-11-25 | Session `arena/0c9983d6` claimed T1–T9 and completed them. Two modelling corrections were made mid-flight and are documented on the Flagged page rather than deleted: (1) Chinatown was wrongly assumed to have no bus service, when RTC Route 203 serves Spring Mountain Road with a timed stop at Las Vegas Blvd; (2) the first travel model scored every Strip hotel identically. Both fixes changed the hotel ranking. |
