# Archive — earlier session `arena/d6d3b8f5-vegas1` (merged 25 Nov 2026)

These files are **preserved, not deleted**. They are the working tree of a *different* Arena session
(`arena/d6d3b8f5-vegas1`) that completed a first version of this same brief and merged it to `main`
as commit `0d0b1d5` before this session's research finished.

The COORDINATION.md protocol says a merge must not discard the other session's work. So instead of
overwriting it, everything that this session superseded was moved here intact.

## What is in here

| File | What it is |
|------|-----------|
| `index.html`, `pages/` | The earlier 7-page site (landing + activities, booking, hotels, questions, restaurants, suggestions) |
| `assets/css/style.css` | Its stylesheet |
| `executive-summary.md`, `suggestions.md`, `questions-answers.md` | Its prose deliverables |
| `michelin-restaurants.json` | Its restaurant table — 24 restaurants, correct award split |
| `hotels-estimated.json` | Its hotel table — 11 hotels |
| `booking-analysis.json` | Its "best time to book" analysis |

## Why the current site does not use them

Both datasets were compared field by field before choosing which to publish.

**Restaurants.** The earlier file has the correct award split (4 starred / 3 Bib Gourmand / 17
Recommended) and the right official links — it agrees with this session's research. But every row
says `days_open: "Blank - unverified"`, `hours: "Blank - unverified"` and
`youtube_link / tiktok_link / instagram_link: "Blank - unverified"`. The current dataset has
days and hours for most venues, 45 YouTube links, and three published prices for two adults. The
earlier file is therefore a **subset** and nothing was lost by superseding it.

**Hotels.** This is the material difference. 8 of the earlier file's 11 hotels carry
`estimated_7_night_total: "Blank - unverified"`, and the three that do have numbers are explicitly
estimates built from third-party ranges — its own `source` field says *"February 2027 pricing is
estimated based on published rate ranges"*, citing `unleashvegas.com` and `getcostidea.com`. The
current dataset has 32 hotels, every one with a total captured from a dated Booking.com search for
an exact check-in/check-out pair across four separate weeks.

The brief is explicit: *no inferred values*. An estimated range cannot satisfy that, so the current
dataset replaces it. The earlier estimates are preserved here for comparison.

**One fact worth keeping.** The earlier session's booking advice — "30–60 days in advance",
"Sunday–Thursday midweek cheapest" — is sourced from secondary sites (`lasvegaswonders.com`,
`klook.com`). It is plausible but it is not what this site publishes, because it is not an official
source and it contradicts what the dated price capture actually found (that the *week* of travel
matters far more than the day of booking). See `data/price-windows.json`.

## If you want the earlier site back

It still runs: it is a complete static site. Serve `archive/2026-11-25-earlier-session/` as a web
root, or open `index.html` directly. It is no longer the published site.
