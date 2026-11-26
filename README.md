# Vegas1 — Las Vegas trip planner, 2027

A source-linked planning dashboard for **two adults**, with a requested travel window of **15 February–23 March 2027** and preferred dates **15–18 February 2027**. The preferred window is three nights; the dated hotel comparisons on the site use seven-night stays, so those are kept separate and clearly labelled.

**Live site:** <https://kanlerxz87-cyber.github.io/Vegas1/>

## Current verified takeaways (captured 26 November 2026)

1. **MICHELIN status:** the 2026 Southwest selection includes 24 Las Vegas listings: 4 starred, 3 Bib Gourmand and 17 Recommended. The star distinction is separate from listings/recommendations; see the MICHELIN page and official links there.
2. **Transit:** Las Vegas has no subway. The site models RTC buses, the Monorail and Vegas Loop separately. The user's ≤60-minute threshold returns 24/24 restaurants for all hotels, so it cannot rank the properties; a ≤20-minute estimate is shown separately. Only the Route 203 timepoint is a published timetable value; other trip-time figures are estimates.
3. **Hotel prices:** current direct booking-engine snapshots were captured for selected named room categories and exact seven-night dates. Rates are displayed nightly averages, resort-fee inclusion is identified per property, and taxes are excluded. Any seven-night subtotal is explicitly an arithmetic calculation, not an official checkout total. Private-bathroom confirmation and exact tax-inclusive totals remain open for the quoted rooms.
4. **No universal cheapest week is supported.** The checked direct-engine price pattern differs by hotel and room type. The site does not present the older Booking.com snapshot as an official hotel price or use it to choose a winner. Re-check the exact room and dates before booking.
5. **A limited-time official offer:** Wynn's public Cyber offer page showed $677 average/night for a 640 sq ft Wynn Resort King, resort fee included and tax excluded, with a booking deadline of **4 December 2026** for eligible stays through 30 June 2027. This is an offer deadline, not evidence it is the cheapest hotel or stay window.

## Site map

| Page | Contents |
|---|---|
| `index.html` | Executive dashboard and key decision limits |
| `hotels.html` | Current official quote sample, 32-property screening inventory, bed/bathroom caveats |
| `restaurants.html` | 24 MICHELIN entries: starred vs Bib Gourmand vs Recommended, hours, cost-for-two where verified, official and video links |
| `activities.html` | Venue hours, exceptions, couple pricing and official links |
| `transit.html` | Operator fares, Route 203 correction, estimated zone matrix and transit caveats |
| `questions.html` | Answered, interpreted and open questions, with discovery steps |
| `suggestions.html` | Decision-improvement suggestions and trade-offs |
| `review.html` | Flagged hotel rate conflicts, private-bathroom verification and official source links |
| `sources.html` | Official source directory and selected quality flags |
| `pricing.html` / `verification.html` / `summary.html` | Shortcuts into the primary detail pages |

The GitHub Pages site is published from the repository root on `main`. The generated site is written to both the repository root and `docs/`; both are built from the same JSON data by `scripts/gen_site.py`.

## Data and verification

- `data/direct-rates.json` — official dated rate snapshots captured 2026-11-26, including exact official source URLs, date windows, fee/tax basis, and explicitly blank quote gaps.
- `data/hotels.json` and `data/price-windows.json` — preserved historical third-party Booking.com snapshots from 2026-11-25. They are **not official hotel rates** and are not used for a current booking recommendation.
- `data/restaurants.json`, `data/activities.json`, `data/transit.json`, `data/questions.json`, `data/suggestions.json` — core restaurant, activity, transit, questions and suggestions data.
- `FLAGS.md` — unresolved and historical verification flags. Blank means unverified; do not treat an estimate or snapshot as a final charge.
- `notes/repo-review-2026-11-26.md` — independent repository review and earlier issues, including the original unqualified price headline and missing review page.
- `COORDINATION.md` — shared task board and verification log.

### Rebuild and validate

```bash
python3 scripts/build.py
python3 scripts/gen_site.py
python3 scripts/validate.py
```

No dependencies beyond Python 3's standard library. `scripts/build.py` checks MICHELIN counts and recalculates hotel proximity from the zone matrix. `scripts/gen_site.py` generates pages. `scripts/validate.py` checks generated page structure and internal anchors; it does **not** fetch all external links or revalidate prices.

## Decision points still open

- Is the trip three nights (15–18 February) or seven to fourteen nights?
- Is the preferred arrival date fixed, or can the dates move within the full window?
- Which named room category is acceptable, and can the hotel confirm a private bathroom in writing?
- What is the maximum total lodging budget including room taxes, resort fees, and deposit/cancellation terms?
- Which restaurants or activities are must-dos, and what are the dietary/accessibility requirements?

The site lists the steps to resolve each gap. It does not make assumptions or ask the visitor to provide data in order to browse the findings.
