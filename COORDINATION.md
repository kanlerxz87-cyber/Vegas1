# Coordination Board — Vegas1

Shared task board for parallel agent sessions. Read before starting; claim before working; `git pull --rebase` before every push.

**Branch rule:** sessions work on their assigned branch only (this session: `arena/c515279e-vegas1`). Branch names in the older `session-<id>/<task>` convention are not used here because Arena binds each session to one branch.

**Status values:** unclaimed · in progress · done · needs review (needs review = published on the Flagged for Review page; does not block anything)

## Task board

| ID | Task | Status | Owner (session) | Branch | File scope |
|---|---|---|---|---|---|
| T1 | Repo review: line-by-line check of repo contents and irregularities | needs review | c515279e | arena/c515279e-vegas1 | `README.md`, `COORDINATION.md`, `docs/data/repo-review.json` |
| T2 | Michelin restaurants, Las Vegas (stars, Bib Gourmand, Recommended) | done (hours/prices/social blank: unverified) | c515279e | arena/c515279e-vegas1 | `docs/data/michelin.json` |
| T3 | Hotel candidates: room, bed, bath facts from official hotel sites; price fields left unverified | done (prices unverified) | c515279e | arena/c515279e-vegas1 | `docs/data/hotels.json` |
| T4 | Activities and attractions with official links and hours | done (3 verified; social blank) | c515279e | arena/c515279e-vegas1 | `docs/data/activities.json` |
| T5 | Site build: landing page, category subpages, executive summary, suggestions, questions, flagged-for-review page | done | c515279e | arena/c515279e-vegas1 | `docs/` (site files) |
| T6 | Integration: merge branches, re-verify combined data, check links, publish to GitHub Pages | unclaimed | — | — | `docs/`, `README.md` |

## Activity log

- **2026-11-25 · c515279e** — Claimed T1–T5 on `arena/c515279e-vegas1`. Repo at base commit `9b8bcfa` contained only `README.md`; no `COORDINATION.md` existed, so this file was created.
- **2026-11-25 · c515279e — T2 sources:** Michelin Southwest 2026 press release (michelin.com, 31 Aug 2026). Checked against the Michelin media page, Webwire and Utah Business reprints. Irregularities: Eater article conflicts with the release (see F1); date conflict (see F2). guide.michelin.com not reachable.
- **2026-11-25 · c515279e — T3 sources:** venetianlasvegas.com (Premium Two Queen Suite, Executive Suites); mgmgrand.mgmresorts.com; cosmopolitanlasvegas.mgmresorts.com (Terrace Studio Two Queen); caesars.com (Augustus Premium Room); bellagio.mgmresorts.com (Premier Two Queen); reservations.wynnlasvegas.com (Wynn Two Queens); aria-resort-las-vegas.h-rez.com (Deluxe Two Queen, booking engine, flagged); rwlasvegas.com (Conrad Premium Room). Prices: none verified (no official 15–22 Feb 2027 rate found). Irregularities: F6, F7, F8.
- **2026-11-25 · c515279e — T4 sources:** usbr.gov/lc/hooverdam (official tour hours/fee); parks.nv.gov/parks/valley-of-fire (official, dated 2017 by crawler); blm.gov press releases (Red Rock, 2020 and 2021; old). Irregularities: F9, F10, F11.
- **2026-11-25 · c515279e — T1 repo review:** README and empty repo state confirmed (`git ls-files` at 9b8bcfa); COORDINATION.md created; branch-rule conflict and HTML-escaped task text logged (R3, R4). Findings on the Flagged page. Needs review.
- **2026-11-25 · c515279e — T5:** Static site built with `scripts/build_site.py` into `docs/`. Internal links and table cell counts checked. Not yet merged to main (integration task T6 is unclaimed; it is the only task that changes shared outputs on main).
