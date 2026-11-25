# Vegas1 — a Las Vegas trip for two, February–March 2027

A research-backed plan for a 1–2 week Las Vegas trip for two adults, built entirely from
official sources. Every table row links to the page its figures came from. Where a value
could not be confirmed officially, the cell is **blank and flagged** rather than guessed.

## Live site

Published with GitHub Pages from [`docs/`](docs/): every page is static HTML with one
stylesheet and no JavaScript.

| Page | What it answers |
|---|---|
| [Overview](docs/index.html) | Hotels ranked by MICHELIN restaurants reachable within an hour, plus the executive summary |
| [Hotels](docs/hotels.html) | Seven-night totals for real dates; private bathroom and queen-or-larger bed on every row |
| [Restaurants](docs/restaurants.html) | All 24 MICHELIN entries, keeping 2-star, 1-star, Bib Gourmand and Selected explicitly distinct |
| [Activities](docs/activities.html) | Fountains of Bellagio, the High Roller, and the one Sphere residency that plays in the window |
| [Transit](docs/transit.html) | Monorail and RTC fares, the travel model, and the two errors it corrects |
| [Open questions](docs/questions.html) | What must be resolved before booking, and how to find it |
| [Suggestions](docs/suggestions.html) | Proposed improvements, for review before implementation |
| [Flagged](docs/flags.html) | Every conflict, gap, judgement call and correction |
| [Sources](docs/sources.html) | Every link used, grouped by what it supports |

## Headline findings

- **Las Vegas has no subway.** The only rail is the privately run Las Vegas Monorail, seven
  stations from MGM Grand to SAHARA. "One hour by subway or bus" was implemented as
  Monorail plus RTC bus, and that substitution is stated on the site.
- **Chinatown holds 7 of the 24 MICHELIN restaurants** and is served by RTC Route 203, not
  by the Monorail or the Deuce. Catching that changed the hotel ranking.
- **Wynn reaches the most restaurants** (22 of 24) because Spring Mountain Road meets Las
  Vegas Boulevard at its north end — but it costs $5,828 for the week.
- **Planet Hollywood and Flamingo tie on what matters** (13 of 24 within 30 minutes) at
  $1,026 and $626 respectively for the same seven nights.
- **Two constraints force a decision:** the Cosmopolitan is unavailable 15–22 Feb 2027, and
  Michael Mina is marked temporarily closed by Bellagio.

## Repository layout

```
data/                  source of truth (restaurants, hotels, activities, transit, travel matrix)
tools/build_matrix.py  regenerates the travel matrix from real addresses
build.py               generates site/ from data/, then mirrors it to docs/
assets/style.css       the only stylesheet
site/                  generated HTML
docs/                  exact mirror, served by GitHub Pages
REPO_REVIEW.md         line-by-line review of what this repository contained
VERIFICATION.md        what each figure rests on, and what was left blank
PUBLISHING.md          how the site is served and redeployed
COORDINATION.md        task board for parallel agent sessions
```

## Rebuilding

Standard library only — no `pip install`, no `npm install`.

```bash
python3 tools/build_matrix.py   # travel matrix from addresses
python3 build.py                # site/ and docs/
python3 -m http.server -d docs 8080
```

## Verification policy

1. Every figure traces to an official source, linked in the row.
2. A value that no official source publishes is left blank and flagged. It is never inferred,
   interpolated or carried over from a similar venue.
3. Where two official sources disagree, both are quoted and the disagreement is left visible.
4. Corrections are documented rather than quietly deleted — see the Flagged page.
