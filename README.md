# Vegas1 — Las Vegas for two, 2027

A mobile-friendly, source-linked dashboard for a **7–14-night trip within 15 February–23 March 2027**.

**[Live dashboard](https://kanlerxz87-cyber.github.io/Vegas1/) · [Executive summary](executive-summary.md) · [Flagged for Review](https://kanlerxz87-cyber.github.io/Vegas1/flagged.html)**

## Decision status — 27 November 2026

**Research dashboard, not a booking-ready recommendation.** Unknown facts remain blank and flagged; a working venue homepage does not verify every field.

- **Dates:** preferred 15–18 February is three nights. **15–22 February** is the disclosed seven-night working comparison; **15 February–1 March** is a separate, unpriced 14-night option. No reservation or change to the user's preference is implied.
- **Hotels:** **34 alphabetical candidates**: the original 32, the peer integration's MGM Grand host-hotel candidate, and separately sourced Hilton at Resorts World. Named room/bed/described bathroom/amenity facts are individually supported. No fully qualified final seven-night offer or dated ≤60-minute bus count is established; no verified price/transit ranking, cheapest week or optimal purchase day is claimed.
- **Official engine observation:** Hilton Resorts World, Deluxe One King, 15–22 February, two adults: **$2,200.15**, itemized with room tax, resort fees and fee tax. Eligibility, deposit/cancellation and an exclusive-use guarantee remain incomplete. The amount is reproduced separately on Pricing, not promoted to a qualified offer or attached to Crockfords. Rounded Caesars/Wynn nightly averages are not expanded into exact totals.
- **MICHELIN:** **4 starred restaurants, 3 Bib Gourmands, 17 Recommended**. Award tiers come from the complete official Las Vegas selection, not videos or account bios. The two press pages have different publication dates; no exact ceremony date is inferred.
- **Food for two:** official fixed-menu/set subtotals are supported for Partage, Anima, Stubborn Seed, Wing Lei, China Poblano, Kabuto and SoulBelly. Michael Mina's printed menu is separately supported but its venue is currently temporarily closed. These are not final taxed/tipped bills or 2027 reservations. Guy Savoy's assumed dish-count estimate and KAME's unqualified price are not public meal totals.
- **Activities:** six entries, including newly re-read Bellagio Fountains. Hours, date-specific exceptions and current/from admission for two are distinguished. High Roller's full hours are blank because its own time blocks conflict; é's two official weekly schedules also conflict.
- **Media:** 20 restaurant Instagram profiles are supported by recorded site cross-links or opened venue/brand profiles. Shared brands, parent-property and dormant feeds are labelled. Unapproved account/video discoveries and the parallel oEmbed check are preserved with original attribution on Flagged for Review, not promoted to official operating facts.
- **Remaining decisions/research:** 14 questions, 16 trip suggestions and 10 preserved site-improvement proposals distinguish facts, interpretations, missing personal constraints and safe discovery steps. Missing information does not block publishing a structurally sound, honest site. No bookings, deposits, accounts or purchases were made.

## Repository map

| Path | Purpose |
|---|---|
| Root `*.html` and `docs/*.html`, `style.css` | Identical generated **16-page** dashboard; Pages serves **`main:/`**. Never hand-edit generated files. |
| `data/verification.json` | **Single live publication authority:** per-field value/null, verification state, exact source, observation date and limitations for every current row. |
| `scripts/verified_views.py` | Active evidence-gated views. No fallback from an unsupported field to historical research. Escapes text and checks coverage, sources, itemized arithmetic and qualification boundaries. |
| `scripts/gen_site.py` | Publishes root/docs together, common navigation/styles and retained historical flag rendering. Old comparison helpers are not the active decision renderer. |
| `scripts/build.py` | Non-mutating evidence/schema validation. Does not recompute assumed transit scores or rewrite research. |
| `scripts/validate.py` | Local HTML/link/anchor/duplicate-ID and root/docs-parity checks — **not remote fact or link verification**. |
| `scripts/check_evidence.py`, `tests/test_site.py` | 20 offline regression tests, including negative tests for unsupported prices, sources, model counts and qualification. |
| `data/{hotels,restaurants,activities,transit,price-windows}.json` | Canonical research/history. Historical row-level badges, OTA amounts and zone estimates do not authorize public fields. Original 32 hotel rows and upstream media/provenance are retained. |
| `data/socials.json` | Parallel account/video research and provenance. Approved links need their own field records in the live manifest. |
| `data/verification-2026-11-27.json`, `scripts/strict_site.py` | Preserved peer audit snapshot/previous renderer, **not the active publication input**. EC-01–EC-07 findings remain attributed on Flagged for Review. |
| `data/official-rates.json` | Earlier engine observations, including historical nightly-rate arithmetic. Use the live manifest/Pricing page, not this file as a current final rate sheet. |
| `data/{questions,suggestions,site-suggestions,review,review-flags}.json` | Question/suggestion backlogs and retained reviews. Current question/suggestion records also preserve incoming earlier states. |
| `FLAGS.md`, `COORDINATION.md` | Current/historical flags, task claims, handoffs, merge resolutions and publication records. Reused historical flag IDs get unique rendered `-history-2` anchors. |
| `notes/verification-2026-11-27-integration.md` | This integration's source observations, verification limits and test record. |
| `archive/`, independent `docs/session-*/` builds | Historical independent work; not current endorsed offers or comprehensively reverified subsites. |
| `scripts/check_links.py` | Optional inherited remote probe. A network refusal/bot wall is not proof a venue closed or a URL is broken. |

## Reproduce

Python 3 standard library only. No build-time network, frontend CDN or runtime JavaScript dependency.

```sh
python3 scripts/build.py
python3 scripts/gen_site.py
python3 scripts/validate.py
python3 scripts/check_evidence.py
# Same regression suite directly:
python3 -m unittest discover -s tests -v
```

Current local gates: **16 pages, zero failures/warnings, 20 tests passing**. Every generated table-body row includes an external primary/source-record reference. External-link *occurrences* are counted, not certified live; repeated links are not separate source checks.

Browser smoke testing covered all 16 pages at **375px and 1280px**: HTTP 200, one H1, no page-level horizontal overflow, no page errors, labelled mobile records and functional disclosures. Screenshots were inspected. Browser binaries, dependencies, reports and screenshots stay in ignored scratch storage and are not runtime/project dependencies.

## Evidence boundary

A menu subtotal is not a complete bill; a published room description is not a dated allocation/private-use guarantee; an itemized shop-page observation is not a qualified checkout; an operator fare is not a timed bus journey. Current schedules are not promises of February–March 2027 operation.

Before booking: obtain matched official room offers with bed/bath/occupancy/fees/tax/eligibility/cancellation terms, compare eligible dates consistently, verify dinner-time bus journeys including walks/waits/transfers/return service, and check exact-date venue availability. Budget, diet/allergies, walking/accessibility and rate-flexibility preferences are not invented. These gaps are published, not silently filled or used to delay a safe website release.
