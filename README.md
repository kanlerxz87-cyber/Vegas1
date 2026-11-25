# Vegas1 — Las Vegas Trip Planner (Feb 15 – Mar 23, 2027)

Mobile-friendly GitHub Pages site planning a 1–2 week Las Vegas trip for 2 adults:
hotels (private bathroom + queen-or-bigger), Michelin restaurants (starred vs listed),
activities ≤1 hour, dates & cheapest booking window, executive summary, open questions,
and site-improvement suggestions.

**Live site:** GitHub Pages from this repo (see `.github/workflows/pages.yml`).
Pages: `index.html` (dashboard) · `executive-summary.html` · `hotels.html` ·
`restaurants.html` · `activities.html` · `dates-pricing.html` · `questions.html` ·
`suggestions.html` · `sources.html` (line-by-line verification).

**Verification rule:** every table row has a source link; values that can't be confirmed
from an official source stay blank and are flagged `UNVERIFIED`. Machine-readable data
in `data/*.json`. Coordination board: `COORDINATION.md`.

**Key irregularity:** Las Vegas has no subway — "within 1 hour by subway/bus" is
implemented as RTC Deuce bus (24h) + Las Vegas Monorail. See `sources.html`.
