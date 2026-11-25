# COORDINATION

Shared task board for parallel agent sessions working in this repository.

## Sessions

| Session | Branch | Scope | Outcome |
|---|---|---|---|
| `arena/d6d3b8f5-vegas1` | `arena/d6d3b8f5-vegas1` | First pass: hotels, restaurants, activities, booking analysis, site at repo root | Merged to `main` as `0d0b1d5`. Its site is what GitHub Pages currently serves from `/` |
| `arena/0c9983d6-vegas1` | `arena/0c9983d6-vegas1` | Verification pass: official-source data, reproducible transit model, `docs/` site | Integrated by this branch (the final integration session) |

## Rules

1. Read this file before starting. Never begin a task another session has claimed.
2. Claim a task by adding your session id before you edit files.
3. Keep file scopes non-overlapping. If you need a file another session owns, request it here.
4. Commit in small increments with specific messages. Run `git pull --rebase` before every push.
5. Shared outputs — table data, nav and the index page — are only changed by the final
   integration session, so parallel edits cannot clobber each other.
6. Log conflicts and handoffs at the bottom.
7. **Verification standard:** every table row carries a link to an official source. A value that
   cannot be confirmed officially is left **blank and flagged**, never estimated.

## Integration decision (this session)

Both sessions produced a full site, and they disagree on a point that matters: **whether
estimated prices are acceptable.**

Session `d6d3b8f5` presents February 2027 hotel prices as estimates drawn from published rate
ranges, sourced from Priceline, KAYAK, Super.com, lasvegaswonders.com and klook.com. That is a
reasonable way to plan, and its `data/booking-analysis.json` carries an explicit "prices are
estimated" note.

Session `0c9983d6` treats estimation as disqualifying, because the brief said a value that
cannot be confirmed officially must be left blank and flagged, and never inferred.

**Resolution:** the verified figures win where the two disagree, and the estimated figures are
kept and labelled rather than deleted, because they are genuinely useful as a cross-check. The
`docs/` site is now the authoritative one, and it states its basis on every row.

### Reconcile, don't overwrite

| Conflict | Resolution |
|---|---|
| `data/hotels.json` | Kept this session's version: live seven-night quotes with a link per row. The first pass's estimated ranges are superseded, and the reason is stated on the site |
| `data/activities.json` | Kept this session's version, which has official pricing for the High Roller and official hours for the Fountains |
| `COORDINATION.md` | Rewritten to record both sessions rather than one claiming everything |
| Site structure | The first pass's site stays at the repository root, where Pages already serves it. This session's site lives in `docs/` and is published from there. Nothing that was live was deleted |

## Published URLs

| URL | Content |
|---|---|
| https://kanlerxz87-cyber.github.io/Vegas1/ | The verified site, served from `docs/` |
| https://kanlerxz87-cyber.github.io/Vegas1/pages/hotels.html | The first pass, still reachable for comparison |

## File scopes

| Session | Files |
|---|---|
| `arena/d6d3b8f5-vegas1` | `index.html`, `pages/`, `assets/css/`, `data/michelin-restaurants.json`, `data/booking-analysis.json`, `executive-summary.md`, `suggestions.md`, `questions-answers.md` |
| `arena/0c9983d6-vegas1` | `data/restaurants.json`, `data/hotels.json`, `data/activities.json`, `data/transit.json`, `data/travel_matrix.json`, `tools/`, `build.py`, `assets/style.css`, `site/`, `docs/`, `README.md`, `REPO_REVIEW.md`, `VERIFICATION.md`, `PUBLISHING.md` |

The two `assets` directories are deliberately separate — `assets/css/style.css` belongs to the
first pass and `assets/style.css` to this one — so neither site can break the other's styling.

## Log

| Date | Entry |
|---|---|
| 2026-11-25 | `d6d3b8f5` claimed all tasks, built the root site, merged to `main` as `0d0b1d5`, and switched Pages on. |
| 2026-11-25 | `0c9983d6` claimed the verification pass, built `docs/`, hit add/add conflicts on three files, and resolved them by keeping the verified data and rewriting this board. Two modelling corrections were documented rather than deleted: Chinatown was wrongly assumed to have no bus service when RTC Route 203 serves Spring Mountain Road, and the first travel model scored every Strip hotel identically. |
| 2026-11-25 | Integration switched Pages from `/` to `/docs` so the verified site is the one at the canonical URL. The first pass remains reachable under `/pages/`. |
