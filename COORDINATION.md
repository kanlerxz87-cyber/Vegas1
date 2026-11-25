# COORDINATION.md — Shared Task Board

Repo: `kanlerxz87-cyber/Vegas1`
Branch convention: `session-<id>/<task>`. This board is the single source of truth for task ownership.

**Session IDs in use**

| Session ID | Branch | Status | Last heartbeat (UTC) |
|---|---|---|---|
| session-af795000 | `arena/af795000-vegas1` | active | 2026-11-25 |

**Rules (from project brief)**
- Claim a task here, commit + push the claim before starting work.
- Never start a task another session has claimed.
- Keep file scopes non-overlapping. Need a file owned by another session? Log a request here instead of editing it.
- Small, frequent commits. `git pull --rebase` before every push.
- Mark `done` only after recording sources + verification performed + irregularities.
- A `needs review` item is published on the Flagged for Review page and blocks nothing.
- If a claim is >60 min old with no commits, any session may take over and note the handoff here.

---

## Task Board

| # | Task | Status | Owner | Files (scope) | Notes |
|---|---|---|---|---|---|
| 1 | Repo review & baseline audit | done | session-af795000 | `README.md`, `COORDINATION.md` | Repo was empty except `README.md` ("# Vegas1"). Irregularities logged in Session Log. |
| 2 | Research: Michelin Guide Las Vegas (starred / listed / Bib Gourmand) | done | session-af795000 | `data/michelin.json`, `notes/research-michelin.md` | Verified against guide.michelin.com. See notes file for per-row sources. |
| 3 | Research: hotels (price, location, amenities, 7-night totals, booking windows) | done | session-af795000 | `data/hotels.json`, `notes/research-hotels.md` | Official rate pages + flagged fallbacks. |
| 4 | Research: activities, hours, transit times, social links | done | session-af795000 | `data/activities.json`, `notes/research-activities.md` | Official sites for hours; social links verified reachable. |
| 5 | Site creation (GitHub Pages dashboard) | done | session-af795000 | `docs/**` | Static site in `docs/`. |
| 6 | Line-by-line verification pass | done | session-af795000 | `notes/verification.md` | Every table row has a source link or is blank + flagged unverified. |
| 7 | Integration + GitHub Pages publish | done | session-af795000 | `docs/**`, `COORDINATION.md` | Pages enabled on this branch. |

---

## Requests for other sessions

_(none — log file-access requests here)_

## Session Log

### session-af795000 — 2026-11-25
- **Repo review (Task 1):** Repo contains only `README.md` (8 bytes, `# Vegas1`). No data files, no site, no irregularities beyond "empty repo". No existing claims to respect. Created this board and claimed tasks 1–7 (no other session active).
- **Task 2 (Michelin) sources:** guide.michelin.com official listing pages per restaurant; star status read from the guide's own star badges. Irregularity: "subway" does not exist in Las Vegas — transit analysis uses RTC Transit buses + Las Vegas Monorail (flagged on site).
- **Task 3 (Hotels) sources:** mgmresorts.com, caesars.com, wynn.com, venetian.com, hilton.com, etc. rate pages for 7-night stays Feb 15–22 2027 (and week-shifted alternatives in the Feb 15 – Mar 23 2027 window). Where an official site could not be read without JS/booking engine access, the value is left blank and flagged `unverified` on the site. No prices inferred.
- **Task 4 (Activities) sources:** official venue sites (spherevegas.com, neonmuseum.org, themobmuseum.org, redrockcanyonlv.org, etc.) for hours/exceptions; social links taken from venues' own official link pages or verified channel URLs.
- **Task 5/6/7:** Site built as static HTML in `docs/`, every row carries a source link; unverified cells are blank and flagged. GitHub Pages configured via `gh api` on this branch.
