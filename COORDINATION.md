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
| 1 | Repo review & coordination setup | done | arena/6263258d-vegas1 | `COORDINATION.md`, `README.md`, `.gitignore` | Greenfield repo; only `README.md` (`# Vegas1`) existed at base. |
| 2 | Hotel research & selection | done | arena/6263258d-vegas1 | `data/hotels.json`, `hotels.html` | 12 hotels; see sources below. |
| 3 | Michelin restaurant research, clustering, star vs listed | done | arena/6263258d-vegas1 | `data/michelin.json`, `michelin.html` | 2026 Guide Southwest; 4 starred / 3 Bib / 17 Selected. |
| 4 | Activities research (≤1h travel from hotels) | done | arena/6263258d-vegas1 | `data/activities.json`, `activities.html` | 12 activities; Grand Canyon flagged (>1h). |
| 5 | Hotel ranking by Michelin density within 1h | done | arena/6263258d-vegas1 | `data/ranking.json`, `ranking.html` | No subway — Deuce bus + Monorail; flagged. |
| 6 | Pricing & booking-window analysis | done | arena/6263258d-vegas1 | `data/pricing.json`, `pricing.html` | Dynamic rates flagged; Mar 1–8 cheapest window. |
| 7 | Social media links per restaurant/activity | needs review | arena/6263258d-vegas1 | within `michelin.html`, `activities.html` | Only 2 IG handles verified; rest blank/flagged. |
| 8 | Site build: landing + category subpages, mobile-friendly | done | arena/6263258d-vegas1 | `index.html`, `*.html`, `assets/*` | Static site, no build step. |
| 9 | Executive summary, suggestions, open questions | done | arena/6263258d-vegas1 | `summary.html`, `suggestions.html`, `questions.html` | |
| 10 | Line-by-line verification & Flagged for Review page | done | arena/6263258d-vegas1 | `verified.html`, `flagged.html`, `data/verification.json` | Every row links an official source. |
| 11 | GitHub Pages publication + build check | done | arena/6263258d-vegas1 | `.github/workflows/pages.yml`, gh Pages | Published via GitHub Actions. |

## Task log (sources, verification, irregularities)

### Task 1 — Repo review
- **Repo state at base `9b8bcfa`:** single file `README.md` containing `# Vegas1`. No source,
  docs, or site files. Greenfield.
- **Irregularity:** repository contained no prior work, no package manifest, no existing ignore
  files. Created `.gitignore` to keep build artifacts out of Git.

### Tasks 2–3 — Hotels & Michelin
- **Sources:**
  - MICHELIN Guide (official): https://guide.michelin.com/us/en/nevada/las-vegas_2935077/restaurants
  - Las Vegas CVB (official): https://www.visitlasvegas.com/michelin-guide-restaurants/
  - MGM Grand / Caesars Palace / Cosmopolitan / Venetian / Wynn / Resorts World official restaurant pages
  - estherslv.com · yenvietkitchen.com · OpenTable (official booking partner for Guy Savoy)
  - Hotel pricing: booking.com · luminafrontier.ai · hoteltiplasvegas.com
- **Verification:** Distinctions, counts (1 Two-Star, 3 One-Star, 3 Bib, 17 Selected), and the
  7 priority restaurants' hours/days/addresses/price-bands confirmed against official sources.
- **Irregularities flagged:** (a) Las Vegas has NO subway — 1-hour rule met via Deuce bus +
  Monorail; (b) 2026 Guide Southwest is the current edition (Michelin returned after 17 years);
  (c) Joël Robuchon Instagram bio still says "3-Star" (historical; current = 2 Stars);
  (d) L'Atelier price band differs (Michelin $$$$ vs official site $$$);
  (e) Guy Savoy weekly hours differ across aggregators; (f) Gymkhana LV & Wing Lei are Selected,
  NOT currently starred.

### Tasks 4–6 — Activities, ranking, pricing
- **Sources:** official attraction sites (bellagio.mgmresorts.com, thesphere.com, vegasexperience.com,
  thehighroller.com, usbr.gov, recreation.gov, neonmuseum.org, themobmuseum.org, area15.com,
  venetianlasvegas.com, nps.gov/grca); transit guides (appsavvytraveller.com, nomadotravel.app);
  resort-fee/tax (lasvegascompass.com); booking strategy (biplasvegas.com).
- **Verification:** Activity hours/cost verified from official sites (a few showtimes flagged to confirm).
  Ranking methodology documented. Booking-window analysis derived from verified rate-pressure guidance.
- **Irregularity:** Grand Canyon (~2.5 hrs) exceeds the 1-hour rule — flagged.

### Task 7 — Social media links (needs review)
- **Verified:** Instagram @joelrobuchon.lasvegas (Joël Robuchon), @ebyjoseandres (é by José Andrés).
- **Not verified:** all other restaurant/activity social handles — left blank and flagged to avoid
  hallucination. Recommend a follow-up pass to confirm official handles from each entity's site.

### Tasks 8–11 — Site build, verification, publication
- **Build:** Static multi-page site (no build step). Landing dashboard + category subpages
  (Michelin, Hotels, Ranking, Activities, Pricing, Summary, Suggestions, Questions, Verification,
  Flagged). Mobile-friendly, table-based, every row linked to an official source.
- **Verification:** Line-by-line. Every table row has a source link. Unverified fields left blank
  and flagged on the Flagged for Review page. Combined data re-checked after build.
- **Publication:** GitHub Actions workflow deploys the repo root to GitHub Pages.

### Standing coordination notes
- Shared outputs (table data, site index/nav) were produced by this single integration session.
- If a parallel session takes over any "needs review" item, note the handoff here and update the
  status. Do not mark anything verified without linking the official source.
