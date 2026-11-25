# FLAGS.md — everything that did not verify cleanly

Every flag below is referenced from the site. A flag means **the cell is blank or the value is
labelled**, never that a plausible number was filled in.

| ID | Where | What | Effect on the plan |
|----|-------|------|--------------------|
| **F-01** | Joël Robuchon | Creator videos say "3 Michelin stars". The 2026 Guide gives **2**. Two pre-2010-era videos are still circulating. | Do not quote three stars to the couple. |
| **F-02** | Michael Mina | Publishes block closures (e.g. 22–30 Nov, 6–8 Dec, 13–15 Dec, 20–22 Dec 2026) and no 2027 dates. | Check closure calendar before fixing a night. |
| **F-03** | Wing Lei | Forbes Five-Star and a Michelin **star** claim in several videos; the 2026 Guide lists it **Recommended**, not starred. | Counted as unstarred in every total on this site. |
| **F-04** | KAME Omakase | Official site `sushikame.com` is a JavaScript shell that returns no address, hours or price. Address/price taken from its own OpenTable listing instead. | Hours remain blank. |
| **F-05** | China Poblano | The "≈$50 per person" figure is from Eater, a secondary source, not the venue. | Shown as context, not as a price. |
| **F-06** | Fontainebleau | Booking.com `ht_id` filter behaviour places some non-resort properties in the five-star resort list. | Star tier treated as unverified. |
| **F-07** | Esther's Kitchen, Yen Viet Kitchen | Hours not obtainable: `/hours-location` errored, home page has no hours block. | Hours left blank — call first. |
| **F-08** | Anima by EDO | 9205 W Russell Rd is ~8 miles west of the Strip; the 20-minute estimate is optimistic. | Furthest dinner from every hotel. |
| **F-09** | Wynn / Encore | Two totals for the same week: Booking search $4,378 (Wynn) vs Wynn property page $5,828. Different fee/tax basis. | Both shown; property-page figure is the more complete. |
| **F-10** | Booking 5★ list | Booking's own "5-star" filter returns Homewood Suites and Cliffs at Peace Canyon, and the `ht_id` variants omit MGM Grand entirely. | Tier is recorded per property, not trusted from the filter. |
| **F-11** | LINQ, Flamingo, SAHARA, Golden Nugget, Horseshoe, Plaza | Cheapest rates are "Room Type Assigned on Arrival" / "Run of House" — the queen-or-larger bed is **not** guaranteed. | Cannot be the default pick against the stated requirement. |
| **F-12** | Nobu at Caesars | The only property **cheaper** in the February week ($1,125) than in March ($1,750). No cause verified. | Flagged as an anomaly, not explained. |
| **F-13** | Bellagio, Waldorf Astoria | The totals across windows are for **different room classes**, so the percentage comparisons are indicative only. | Stated per row. |
| **F-14** | Cliffs at Peace Canyon, Green Valley Ranch, Red Rock | Off-Strip/Henderson/Summerlin. Correct star ratings, but 11–17 miles from the Michelin corridor. | 0 restaurants inside 20 minutes. |
| **F-15** | Bluegreen Club 36 | The only property with an explicitly stated **queen** bed. Private bathroom is not stated in the rate block. | Bathroom left blank, not inferred. |
| **F-16** | Sphere | No single admission price exists, and the 2027 show calendar is not published. The $131.45 figure is a Booking.com reseller listing. | No venue price quoted. |
| **F-17** | 14-night variant | The brief allows 1–2 weeks; only 7-night blocks were priced. Doubling a 7-night total would ignore weekly rate breaks. | Not priced. Flagged rather than estimated. |
| **F-18** | Bellagio Fountains | Official page fetch failed twice. Show schedule unverified. | No hours listed on the activities page. |
| **F-19** | Instagram / TikTok | Handles are not printed on most official pages. Only the Neon Museum publishes its own. | Blank rather than guessed — see Q-07. |
| **F-20** | Transit minutes | Every minute value is an estimate from official station lists and route maps. No official door-to-door times exist. | Labelled "estimate" everywhere. |
| **F-21** | Chinatown / Route 203 | **Correction.** An earlier version of this dataset recorded Chinatown / Spring Mountain Rd as reachable only by car or rideshare. RTC Route 203 runs the length of that road with a timed stop at Las Vegas Blvd, and its published timetable gives Decatur → Las Vegas Blvd in 14 minutes. | North Strip to Chinatown is ~34 min, not unreachable. Raises the north-Strip short-trip counts. Seven listings are affected. |

## Deliberate non-inclusions

- **No 3-star restaurant exists in Las Vegas.** The guide only returned in 2026 after a 17-year gap, so any source claiming otherwise is out of date.
- **Formula 1 is not in this window.** The 2027 Las Vegas GP is 18–20 November 2027. It was checked precisely because it would otherwise wreck a Strip price.
- **Cirque du Soleil** was listed by a reseller at $158.65 per person with no show name, no venue and no 2027 date — excluded.
- **MGM Grand room price** could not be captured: Booking.com's own property page redirected to a generic Las Vegas search. No price is published for it rather than a guess.
