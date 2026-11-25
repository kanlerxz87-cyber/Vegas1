# COORDINATION.md — Shared Task Board

Session ID: `b1ad8e98` (branch `arena/b1ad8e98-vegas1`, base `9b8bcfa6ba9e3d777f9488560ad34c53a0518743`)
Last updated: 2026-11-25

## How to use this board
- Claim a task by writing your session ID + file scope, then commit & push immediately.
- Never start a task another session has claimed. Keep scopes non-overlapping.
- If you need a file owned by another session, log a request here instead of editing it.
- `needs review` = published on Flagged for Review page, does not block.
- Stale claim (>60 min, no commits) may be taken over with a handoff note.
- Shared outputs (table data, index/nav) are changed only by a final integration session.

## Tasks

| ID | Task | Status | Owner session | Files touched | Sources / verification | Irregularities |
|----|------|--------|---------------|---------------|------------------------|----------------|
| T1 | Repo review (line-by-line) | done | b1ad8e98 | README.md, COORDINATION.md | `git log`, `ls -la` — repo was empty except README `# Vegas1` at base commit | None. Empty repo = greenfield build. |
| T2 | Research: Michelin 2026 Southwest (starred vs listed/Bib) | done | b1ad8e98 | restaurants.html, data/restaurants.json | VisitLasVegas Michelin page; Eater Vegas 2026-08-27; MGM Grand official restaurant page (hours) | Michelin Guide site itself failed to fetch (fetch_page error) — starred list cross-checked across 3 secondary sources, flagged for official re-check. |
| T3 | Research: hotels, 7-night pricing, best booking window | done | b1ad8e98 | hotels.html, data/hotels.json | MGM Resorts official (Bellagio Premier Two Queen: 2 queen beds, marble bathroom); LuminaFrontier Feb 2027 price table; LasVegasWonders booking-window guide; TripSignal | Exact Feb-2027 per-hotel rates are NOT published on official sites this far out — left blank + flagged UNVERIFIED per brief, with formula to compute 7-night total. |
| T4 | Research: transit (no subway), activities ≤1 hr, hours/prices | done | b1ad8e98 | activities.html, data/activities.json | RTC/LV Monorail (Deuce 24h); Red Rock Canyon official hours; Hoover Dam guide; Neon Museum / Mob Museum | Brief asks "subway or bus" — Las Vegas has NO subway/metro (verified). Site uses Deuce bus + Monorail instead. Flagged. |
| T5 | Build GitHub Pages site (landing + subpages, mobile-first) | in progress | b1ad8e98 | index.html, *.html, assets/, .github/workflows/pages.yml, _config.yml | Build check: `python3 -m http.server` smoke test + link check script | — |
| T6 | Verification pass (every row has source link or UNVERIFIED flag) | in progress | b1ad8e98 | sources.html, verification log below | Link checker run 2026-11-25 | — |
| T7 | Final integration & publish to GitHub Pages | unclaimed | — | index.html, nav, .github/workflows/pages.yml | — | — |

## Verification log
- 2026-11-25 b1ad8e98: Michelin starred = Joël Robuchon (2★), L'Atelier de Joël Robuchon (1★), Restaurant Guy Savoy (1★), É by José Andrés (1★). Bib Gourmand = China Poblano, Esther's Kitchen, Yen Viet Kitchen. Listed/Selected = 17 names per Eater/VisitLasVegas. Sources linked in restaurants.html.
- 2026-11-25 b1ad8e98: Joël Robuchon hours Tue–Sat 5:00–9:30pm, closed Sun–Mon — MGM Grand official page. Price: official page publishes NO price → cost-for-2 left as UNVERIFIED range from third-party reports, flagged.
- 2026-11-25 b1ad8e98: Feb 2027 cheapest-window guidance (Sun–Thu, book 30–60 days out, avoid Super Bowl Feb 14 2027 + Presidents Day Feb 15) — multiple secondary sources, linked. Exact hotel totals UNVERIFIED until booking window opens.

## Handoff / conflict log
- (none yet)
