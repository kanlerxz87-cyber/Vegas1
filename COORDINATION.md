# COORDINATION — Multi-session task board

**Repo:** kanlerxz87-cyber/Vegas1
**Branch convention:** `session-<id>/<task>` (this session's branch is fixed by Arena as `arena/f9e78242-vegas1`)
**Rules:** Claim a task by writing your session ID + file scope here, commit + push the claim immediately. Never start a task another session has claimed. Keep scopes non-overlapping. If you need a file owned by another session, log a request here instead of editing it. Run `git pull --rebase` before every push. A claim >60 min old with no commits may be taken over (note the handoff in the log).

---

## Session registry

| Session ID | Branch | Task scope | Status | Started (UTC) |
|---|---|---|---|---|
| `arena-d6d3b8f5-vegas1` | `arena/d6d3b8f5-vegas1` → merged/pushed to `main` (`0d0b1d5`) | Research + site + docs. Files: `index.html`, `pages/`, `assets/`, `data/michelin-restaurants.json`, `data/hotels.json`, `data/activities.json`, `data/booking-analysis.json`, `executive-summary.md`, `suggestions.md`, `questions-answers.md` | **published on `main`** | 2026-11-25 |
| `session-f9e78242` | `arena/f9e78242-vegas1` | Verification-first build. Files: `docs/` (generated site), `plan-data/` (verified JSON), `build.py`, `check.py`, `COORDINATION.md` | in progress | 2026-11-25 |

### ⚠ Overlap that already happened — reconciled, nothing lost

Both sessions were given essentially the same brief. Neither saw the other at claim time:
`session-f9e78242` started from `9b8bcfa` where **no `COORDINATION.md` existed and the only file
was an 8-byte README**, so it claimed the full build. `arena-d6d3b8f5` meanwhile published
directly to `main`.

**Resolution:** no file owned by `arena-d6d3b8f5` was modified or deleted. This session's data
was moved from `data/` to **`plan-data/`** to avoid overwriting their `data/hotels.json`, and its
site lives in **`docs/`**, not the repo root. Both builds coexist.

**Cross-audit performed:** `session-f9e78242` audited every factual claim in the `main` build
against official sources. Result: **the 24 MICHELIN venues and all 24 award levels agree exactly**
— strong two-source confirmation. Conflicts found are in pricing/sourcing, not in the guide data.
Full report: `docs/audit-main.html`, raw data `plan-data/cross-session-audit.json`.

---

## Task board

| # | Task | Status | Owner | File scope |
|---|---|---|---|---|
| T1 | Repo audit + COORDINATION.md bootstrap | done | session-f9e78242 | `COORDINATION.md`, `docs/audit.html` |
| T2 | MICHELIN dataset (stars / Bib / Recommended) | done | session-f9e78242 | `plan-data/michelin.json` |
| T3 | Hotel shortlist (price/location/amenities, bed & bathroom) | done | session-f9e78242 | `plan-data/hotels.json` |
| T4 | 7-night pricing by date window | done (partial sweep) | session-f9e78242 | `plan-data/pricing.json` |
| T5 | Transit-time matrix (hotel → restaurant, ≤60 min) | done (5 of ~360 pairs) — **needs review** | session-f9e78242 | `plan-data/transit.json` |
| T6 | Activities + hours | done (hours unverified) — **needs review** | session-f9e78242 | `plan-data/activities.json` |
| T7 | Social/video links per restaurant & activity | done (partial) | session-f9e78242 | `plan-data/social.json` |
| T8 | Site build (13 pages, mobile-first) | done | session-f9e78242 | `docs/**` |
| T9 | Executive summary, suggestions, open questions | done | session-f9e78242 | `docs/index.html`, `docs/suggestions.html`, `docs/questions.html` |
| T10 | Verification pass + Flagged for Review page | done | session-f9e78242 | `docs/verification.html`, `docs/flagged.html` |
| T11 | **Integration / Pages publish** | **needs review — blocked** | — | see below |
| T12 | Audit of the `main` build | done | session-f9e78242 | `docs/audit-main.html`, `plan-data/cross-session-audit.json` |
| T13 | Complete the 15 × 24 transit matrix | unclaimed | — | `plan-data/transit.json` |
| T14 | Verify resort fees per hotel from hotel sites | unclaimed | — | `plan-data/hotels.json` |
| T15 | Sweep all 7-night windows 15 Feb – 23 Mar 2027 | unclaimed | — | `plan-data/pricing.json` |

---

## Requested changes to files owned by another session

| # | Requesting session | Target file | Request | Status |
|---|---|---|---|---|
| R1 | session-f9e78242 | `main`: `index.html` | Landing page says content is "all verified from official sources"; `data/booking-analysis.json` says Feb 2027 pricing is "estimated". Correct one of the two labels. | **open — awaiting human** |
| R2 | session-f9e78242 | `main`: `data/booking-analysis.json` | Caesars Palace resort fee of $54.95 could not be matched to any current source ($55 / $62.30 / $49.95+tax all appear elsewhere). Re-verify from caesars.com before reuse. | **open — awaiting human** |
| R3 | session-f9e78242 | repo settings | GitHub Pages currently serves `main` / root. This session's site is in `docs/` on `arena/f9e78242-vegas1`. Choose one publish target. | **open — awaiting human** |

---

## Merge-conflict log

| When | What | How resolved |
|---|---|---|
| 2026-11-25 | Both sessions created `data/hotels.json`. This session's version would have overwritten `arena-d6d3b8f5`'s. | This session renamed its data dir `data/` → `plan-data/` via `git mv`, updated `build.py`, rebuilt, re-ran `check.py`. No other session's file touched. |

## Handoff log

_(none yet)_

## Verification summary (this session)

**Method:** distinctions read from the official MICHELIN publication; hours and prices read from
each venue's own website; hotel prices captured live from Booking.com with the capture URL kept
alongside each number; transit times from live Google Maps routing. Unpublished values were left
blank and labelled `unverified` — never inferred.

**Checked:** 13 pages, 311 automated checks (`python3 check.py`) — internal links, nav completeness,
external-link syntax, source-link coverage, leaked null values.

**Not verified, and stated as such on the site:** resort fees, private bathroom for 13 of 15
hotels, TikTok/Instagram for 17 venues, activity hours and ticket prices, prices for 3 of the 4
starred restaurants, and 355 of 360 transit pairs.

**Full page:** `docs/verification.html` · **Irregularities:** `docs/flagged.html`
