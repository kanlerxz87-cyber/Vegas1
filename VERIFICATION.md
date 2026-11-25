# Verification

The rule for this study was: every value traces to an official source, and anything that
cannot be confirmed is left blank and flagged. This file records what that meant in
practice, including where it was uncomfortable.

## Sources by category

| Category | Primary source | Status |
|---|---|---|
| MICHELIN distinctions | `guide.michelin.com` 2026 American Southwest selection | Official. Counts reconcile exactly: 1 two-star, 3 one-star, 3 Bib Gourmand, 17 Selected = 24 |
| Restaurant hours | Each restaurant's own site, or its operating resort's site | Official for 14 of 24. 1 from a secondary directory. 9 unavailable |
| Restaurant prices | Operator pages | Official for 1 of 24 |
| Hotel rates | Booking.com property pages, exact date window, 2 adults | Live retail quotes captured 2026-11-25. Not official hotel rates, but real quoted prices |
| Hotel amenities | Booking.com property pages | Retail listings, corroborated by the operator sites where reachable |
| Monorail | `lvmonorail.com` stations, ticket pages | Official |
| Bus | `rtcsnv.com` fares; `rtcws.rtcsnv.com` Route 203 timetable | Official |
| Activities | `bellagio.mgmresorts.com`, `caesars.com`, `thesphere.com` | Official |
| Social profiles | Only where the operator's own site links to them | 6 confirmed, the rest blank |

## The distinction rule

MICHELIN uses four labels that are routinely conflated. The site keeps them separate on
every row:

- **Two stars** — 1 restaurant. Restaurant de Joël Robuchon.
- **One star** — 3 restaurants. Guy Savoy, é by José Andrés, L'Atelier de Joël Robuchon.
- **Bib Gourmand** — 3 restaurants. A value award, not a star. China Poblano, Esther's
  Kitchen, YEN Viet Kitchen.
- **Selected** — 17 restaurants. A listing, not an award.

One trap worth naming: **Gymkhana's London original holds two MICHELIN stars, but the Las
Vegas location is Selected only.** Carrying the London stars across would have been a
fabrication, so they are not in the table.

## What was deliberately left blank

| Field | Blank count | Why |
|---|---|---|
| Restaurant hours | 9 of 24 | No official page publishes a weekly table |
| Restaurant per-person price | 23 of 24 | MICHELIN does not publish prices, and operators publish menus as PDFs or images |
| Exact transit minutes | 0 | Every band has a computed minute value, but only one input is a published timing — see the assumptions table on the Transit page |
| Sphere ticket prices | 1 | Prices vary by date and seat; the shows page does not give a single figure |
| Airport transfer | 1 | No official static page with a verifiable figure was found |

## Values that were NOT inferred

These are the tempting ones. Each was left blank instead:

- **Menu prices for the starred restaurants.** Secondary outlets quote figures such as a
  $525 degustation at Robuchon. Not used, because none of it came from an official page.
- **Monorail and bus travel times between specific stations.** Not invented. One published
  bus timing anchors the model, and the remaining speeds are declared assumptions printed
  on the page rather than presented as measurements.
- **Restaurant reservation availability in February 2027.** Not checked, so not asserted.
- **Guest scores where Booking.com did not display one.** Left as an em dash.

## Known conflicts, unresolved on purpose

1. **Restaurant de Joël Robuchon's opening days.** MGM Grand says Monday closed, Tuesday to
   Saturday open. The MICHELIN Guide says Monday open, Tuesday and Wednesday closed. Both
   are official. The site uses MGM Grand's version and flags the disagreement.
2. **Michael Mina's existence as a bookable restaurant.** MICHELIN lists it; Bellagio marks
   it temporarily closed with every day closed. Both are stated.
3. **Ping Pang Pong's hours.** The Gold Coast's own site was unreachable. Two independent
   directories agree, so the hours are shown and labelled as secondary rather than passed
   off as official.

## Corrections made during the work

These are recorded because hiding them would make the rest less trustworthy.

| Error | Correction |
|---|---|
| Assumed Chinatown had no bus service, scoring 7 of 24 restaurants as unreachable | RTC Route 203 serves Spring Mountain Road with a timed stop at Las Vegas Blvd, 14 minutes from Decatur. Fixed, and it changed the hotel ranking |
| First travel model gave every Strip hotel the same score | Rebuilt from street addresses with a stated calibration constant |
| A clamping bug gave south-Strip hotels a zero-length trip to Chinatown | Fixed to absolute distance; Luxor fell from 22 to 15 |
| Recorded the Cosmopolitan as globally sold out | Only 15–22 Feb 2027 is unavailable; 9–16 Mar is bookable at $2,093.71 |

## Data-boundary caveats stated on the site

- Hotel prices are a **single-day snapshot during a Black Friday promotion**, and several
  rates are explicitly Black Friday deals expiring 31 Dec 2026. They will be stale.
- Booking.com totals **include resort fees and exclude the 13.38% tax**. Every row states
  this, and a computed all-in figure is shown beside it, labelled as arithmetic rather than
  as a quote.
- Five properties are priced on a **tax-inclusive** basis and are kept in a separate table
  so the two bases are never mixed.
