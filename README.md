# Vegas1 — Las Vegas 2027

A sourced planning dashboard for **two adults**, a **one–two week** trip within **15 February–23 March 2027**.

**[Live dashboard](https://kanlerxz87-cyber.github.io/Vegas1/) · [Executive summary](executive-summary.md)**

## Current findings — 27 November 2026

- Preferred **15–18 February is three nights**, inconsistent with the requested length. **15–22 February** is a provisional seven-night comparison, not an approved change.
- **33 hotel candidates** are shown alphabetically. No verified qualifying **all-in seven-night total**, cheapest hotel/week, optimal purchase day, or ≤60-minute bus ranking exists. Unsupported decision fields stay blank.
- MICHELIN categories are separate: **4 starred venues, 3 Bib Gourmands, 17 Recommended**. Guide inclusion does not establish 2027 opening or reservations.
- Fixed-menu food subtotals for **two** are confirmed from official pages/PDFs for **12 of 24** venues: Partage ($260/$320/$420), Anima ($170), Stubborn Seed ($320), Wing Lei ($397.76), China Poblano ($120), Kabuto ($260/$370), SoulBelly ($80), Kame Omakase ($700/$1,000), Sparrow + Wolf ($298), COTE ($190/$450), Estiatorio Milos ($90 daily lunch) and Mott 32 ($76/$136 Mon–Fri lunch). These exclude unverified taxes, gratuities, drinks and future availability. À-la-carte dish prices do not establish a complete meal total.
- No assumed meal counts, OTA hotel amounts, modeled travel scores or constructed full-trip budget are endorsed by the primary decision tables. Historical research is preserved, not silently rewritten.
- Official observations, verification scope and manual-review links accompany each table row. Blank means **unverified**, not free or unavailable. **This is not booking-ready.**

## Repository map

| Path | Purpose |
|---|---|
| `docs/` and root `*.html`, `style.css` | Identical generated 16-page dashboard. Pages publishes `main:/`; both copies are generated together. Do not hand-edit. |
| `data/verification-2026-11-27.json` | Field-level primary evidence overlay: 33 hotels, 24 restaurants, 6 activities; source links, caveats, EC-01–EC-08 flags. |
| `data/{hotels,restaurants,activities,transit,price-windows}.json` | Preserved canonical research, including historical snapshots/estimates. Presence here does not make a value verified for the primary dashboard. |
| `data/socials.json` | Earlier sessions' social-account provenance, shown with attribution and caveats, separate from fresh checks. |
| `data/{questions,suggestions,review,review-flags}.json` | Prior question/suggestion backlogs and review logs, retained for audit. |
| `scripts/build.py` | Validates evidence schema/coverage without recomputing historical scores or rewriting source data. |
| `scripts/strict_site.py` | Primary strict-evidence renderer. Escapes source text; distinguishes current from inherited evidence. |
| `scripts/gen_site.py` | Generates root and docs outputs; earlier rendering functions remain for audit but do not control the primary dashboard. |
| `scripts/validate.py` | Structural, link/anchor and root/docs parity checks. Not external-source verification. |
| `scripts/check_evidence.py`, `tests/test_site.py` | Offline regression suite for evidence-display policy, table-row references, source coverage, arithmetic, markup and parity. |
| `scripts/check_links.py` | Separate inherited external-link probe; automated-access blocks are not proof a venue/link is closed. |
| `dining.html`, `costs.html` | Confirmed fixed-menu subtotals and missing full-budget gates, not assumed meal scenarios. |
| `FLAGS.md`, `COORDINATION.md` | Historical and session-specific flags; task claims, integration conflicts and publication records. |
| `executive-summary.md` | Current decision summary. |
| `archive/`, `docs/session-af795000/`, `docs/session-48dbf0ae/` | Earlier independent builds, preserved as historical research, not current endorsed offers. |

## Reproduce the publication

Python 3 standard library only; no build-time network calls or frontend CDN dependencies.

```sh
python3 scripts/build.py
python3 scripts/gen_site.py
python3 scripts/validate.py
python3 scripts/check_evidence.py
# Equivalent expanded regression entry point:
python3 -m unittest discover -s tests -v
```

`.nojekyll` exists at root and in docs. The latest structural check reports **16 pages, 0 failures, 0 warnings, 564 external link occurrences**. Link occurrences are **not** a claim that remote pages remain live at reading time. Tests check local correctness and evidence-display rules, not source truth or future availability.

## Evidence policy and remaining research

The current overlay/decision pages supersede earlier prose recommending modeled hotel rankings or worked dining budgets. All canonical source datasets, previous menu estimates, social findings and session logs remain available for audit. Complete fixed-menu prices are differentiated from per-dish prices; exact engine observations are differentiated from checkout totals. Earlier social observations retain their original provenance and do not become freshly reverified merely by being rendered.

Manual-review tasks and irregularities are published on **Flagged for Review**. Questions retain known answers, missing preferences and discovery actions. Optional improvements remain a **suggestions backlog**, not automatically implemented decisions. No payments or bookings have been made.

Still required: matched official room checkout quotes with occupancy/bed/bath/fees/taxes/cancellation, a consistent date comparison, dated door-to-door bus journeys, future venue schedules and availability, and personal budget/diet/accessibility preferences. The dashboard exposes those limitations instead of filling them with estimates.

### Latest integration observations

Resorts World Hilton’s official engine was freshly reopened for 15–22 February 2027, two adults. The Deluxe One King display itemises **$2,200.15** including room tax, resort fees and resort-fee tax; the Two Queens display is **$2,434.84**. These are engine observations, not completed checkouts or fully qualified offers: exclusive bathroom, cancellation/deposit and promotion conditions remain unverified. The primary all-conditions decision total therefore stays blank; the observed amount and exact URL appear on `pricing.html`. Bellagio Fountains’ free admission, daily display times and weather exceptions were also freshly reproduced.

Browser smoke check: all 16 pages served HTTP 200 at 375px and 1280px; no page-level horizontal overflow, JavaScript errors or missing H1; expandable provenance worked. Mobile and desktop screenshots were inspected. Browser dependencies and screenshots are temporary, not project runtime dependencies. This is layout testing, not verification of external websites.
