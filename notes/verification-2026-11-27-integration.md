# Official-field integration — 27 November 2026

Session: `arena/3d5d3718-vegas1`. This is an observation/integration record, not a booking confirmation or a claim of complete future-travel verification.

## Publication boundary

- `data/verification.json` is the single live authority. Approved fields require a fetched official source record and checked date. Unsupported values are explicit nulls with notes/flags; no canonical row-level badge authorizes all its fields.
- Canonical coverage: **34 hotels, 24 restaurants, 6 activities**. Original 32 hotel research rows are unchanged. Hilton at Resorts World is a separately sourced addition; MGM Grand, added by the peer integration as a host-hotel candidate, is retained with unknown room/rate facts.
- Historical OTA/model data, all incoming media/profile links and provenance, older register states, the peer `verification-2026-11-27.json`, previous renderer and independent builds are preserved. Prior media is visibly attributed on Flagged for Review, not silently promoted to official operating evidence.
- Fully qualified hotel final totals and bus-threshold counts remain null. Neither the assumed 24/24 model nor its twenty-minute substitute is a real dated bus journey. Build validation is non-mutating; no model outputs are recomputed.
- A verified field is only the stated observation. Current hours, a menu price, an in-room bathroom description and a printed hotel-engine total are not promises of 2027 operation, exclusive use, final qualification or booking availability.

## Key source observations

These observations came from read-only page fetches. The complete per-field ledger, including unchecked inherited references, is in the live manifest.

| Official source | Read observation / limitation |
|---|---|
| [MICHELIN corporate selection](https://www.michelin.com/en/publications/products-and-services/michelin-guide-reveals-first-ever-southwest-restaurant-selection-in-the-u-s) and [North America press page](https://michelinmedia.com/pages/blog/detail/article/c0/a1480/) | Complete Las Vegas subset: four starred venues (one two-star, three one-star), three Bib, 17 Recommended. Corporate publication 31 Aug vs North America Posted 26 Aug does not establish one exact ceremony date. |
| [Caesars exact-date engine](https://www.caesars.com/book/room-list?arrivalDate=02/15/2027&departureDate=02/22/2027&dateSearchFormat=exact-dates&propCode=clv&numberOfAdults=2&numberOfRooms=1) | 15–22 Feb 2027, two adults. Technical-error banner and nightly prices excluding tax; no qualified final total. No multiplication of a rounded nightly figure into an exact stay offer. |
| [Wynn exact-date engine](https://reservations.wynnlasvegas.com/ibe/details.aspx?hotelID=13763&langID=1&rmID=68658&checkIn=02/15/2027&checkOut=02/22/2027&adults=2&children=0) | Tax-exclusive averages include resort fee; occupancy extraction is not fully clear. Cyber booking/stay window and cancellation/deposit wording recorded, not proof of cheapest timing or a qualified offer. |
| [Venetian exact-date engine](https://www.venetianlasvegas.com/booking?adults[]=2&arrival_date=2027-02-15&children[]=0&departure_date=2027-02-22&view=calendar) | Loading/booking shell; no usable quote. |
| [Hilton Resorts World exact-date engine](https://reservations.rwlasvegas.com/ibe/shop.aspx?hotelID=17726&selectedTower=HILTON&checkin=2027-02-15&checkout=2027-02-22&nights=7&adults=2&children=0) | Reproduced Deluxe One King itemization: seven room amounts 159, 348.75, 348.75, 228.75, 186.75, 186.75, 96.75; room tax 208.13; resort fees 385; fee tax 51.52; printed total **2,200.15 USD**. Two Queen alternative 2,434.84. Two guests and exact dates exposed. Selected promotion DBF26; eligibility, cancellation/deposit/private-use guarantee incomplete. Browser-unsupported footer and conflicting calendar fee labels disclosed. Observation, not qualified offer or Crockfords price. |
| [Hilton Deluxe-room page](https://www.rwlasvegas.com/stay/las-vegas-hilton/deluxe-room/) | Describes King or two Queens, 400 ft², in-room bathroom/walk-in shower and LED vanity; amenities listed. Engine separately selects One King. Description is not an exclusive-use/dated-allocation guarantee. |
| [Partage menu](https://partage.vegas/menu) | Five/seven/Signature menus $130/$160/$210 pp → $260/$320/$420 for two. Monthly changes and diet restrictions recorded. Not an all-in future bill. |
| [Wing Lei operator-linked PDF](https://cdn.wynnresorts.com/image/upload/v1781902951/visitwynn_pdfs_files/wing-lei-main-menu-new.pdf) | Literal $198.88 tasting price → $397.76 for two. Wine separate. Do not explain away .88 as formatting or round it silently. |
| [China Poblano menu](https://www.chinapoblano.com/menus/) | José's Way $60 pp → $120 for two. Official operator weekly schedule independently shows Sunday 10 PM closing. |
| [Kabuto menu page](https://www.kabutolv.com/menu), [PDF](https://www.kabutolv.com/s/kabuto-menu2026.pdf), [operator reservation redirect](https://www.kabutolv.com/reserve) | $130 Yoroi / $185 Kabuto → $260/$370 for two. First-party `/reserve` redirects directly to Resy, authorizing that booking source. Thirty-day window, allergies, cancellation policy and separately dated Dec–Jan holiday menu disclosed. PDF title metadata says 2023 despite 2026 filename; current operator link and booking listing corroborate amounts. |
| [SoulBelly menu](https://soulbellybbq.com/menu) | Chef's Choice **for 2** explicitly $80. Do not invent a per-person price. Main Street listing, not Miracle Mile Express. |
| [Stubborn Seed operator PDF](https://www.rwlasvegas.com/pdf/stubborn-seed-tasting-menu-11-25-2026/) | $160 pp → $320 two-person food subtotal; full-table participation/no substitutions. |
| [Michael Mina](https://bellagio.mgmresorts.com/en/restaurants/michael-mina.html) | Printed $295++ pp menu → $590 food subtotal, but current page says temporarily closed/daily closed. No 2027 reopening inferred. |
| [Guy Savoy menu](https://www.caesars.com/caesars-palace/restaurants/restaurant-guy-savoy/main-menu) | Individual dish prices do not establish a complete dinner. Earlier Krug amount not reproduced; assumed 2–3-dish spend not published as a meal total. |
| [é own site](https://www.ebyjoseandres.com/) and [MGM page](https://cosmopolitanlasvegas.mgmresorts.com/en/restaurants/e-by-jose-andres.html) | Tue–Sun vs Tue–Sat weekly conflict. Both describe nine seats/two nightly seatings; own site says 5:30 and 8:30 PM, three-month release and phone 702-698-7950. Weekly days remain null/disputed, not guessed. |
| [Bellagio Fountains](https://bellagio.mgmresorts.com/en/entertainment/fountains-of-bellagio.html) | Free, full current weekday/weekend display schedule, weather/schedule exceptions. Sixth activity retained and re-read, not dropped during integration. |
| [Mob Museum](https://themobmuseum.org/) and [admission engine](https://admission.themobmuseum.org/) | Museum daily 9 AM–9 PM, not a weekly Thursday 4 PM close. Current admission 37.95 pp → 75.90 two-person base, not a 2027 final quote. |
| [Neon 2027 Admission](https://neonmuseum.org/whats-on/all-day-admission/) | 2027 daily 3–11 PM, last entry 10 PM; adults from $21 plus processing fee → from $42 for two plus fee. Outdoor/photo rules and official IG/TikTok cross-links recorded. Stray December widget not treated as dated availability. |
| [Fremont Canopy](https://fremontstreetexperience.com/the-canopy/) | Music Reels at the top of the hour 6 PM–2 AM daily, not old 5 PM. Free ordinary concerts do not make paid attractions/special events free. |
| [High Roller](https://www.caesars.com/linq/things-to-do/attractions/high-roller) | Own blocks conflict on 12:30/noon opening and noon/6 PM anytime eligibility. Full hours null. Published starting two-adult ticket arithmetic has tax/fee and date caveats; The LINQ profiles are labelled parent property. |
| [RTC fares](https://www.rtcsnv.com/ways-to-travel/fares-passes/) and [planner](https://www.rtcsnv.com/ways-to-travel/how-to-ride/ridertc-app/) | Regular vs reduced/residential vs visitor products distinguished. $1 residential is reduced, not visitor default. Operator planning resources are not a hotel-to-restaurant itinerary. |
| [Monorail tickets](https://www.lvmonorail.com/ticket-information/) | Electronic single $5.75 / seven-day $59.95 per adult, $11.50/$119.90 for two. $1 local fare requires eligible Nevada ID; not the visitor fare. |
| [Vegas Loop](https://www.boringcompany.com/projects/las-vegas-loop) | Expanded operator network is not subway/bus-only routing. Example fares are not expanded into a couple total when passenger/vehicle basis is unclear. |

## Social verification scope

Opened venue/brand Instagram profiles are recorded individually with identity basis, rather than promoting the existence of a string in the canonical data. Twenty restaurant profiles are approved. Shared COTE/Bouchon/Stubborn Seed brands and dormant Robuchon/Guy feeds are labelled. Joël Robuchon's stale three-star bio is not used as a current award. L'Atelier's opened dormant profile exposed venue tags but no clear operator-domain/control evidence, so its official field remains null; original discovery survives in the prior-media record.

The Mob Museum YouTube fetch returned a 401 banner **and** usable operator-channel video/playlist content linking the museum; that mixed result is disclosed, not called universally working playback. Neon TikTok is supported by its official-site cross-link; its target was not declared fetched. KAME's official booking subdomain failed; an unqualified bio amount is not made into a two-person priced menu.

All incoming restaurant/activity YouTube/Instagram/TikTok values and provenance strings were programmatically compared with `origin/main` and retained exactly. The parallel oEmbed check and all ten site-improvement proposals remain attributed and visible. No historical creator claim is used as award/price/hour evidence.

## Integration and tests

Main advanced twice during this work, ultimately through PR #65. Both full append-only coordination records and all flags were retained; newer canonical datasets were used as the base, not overwritten by older copies. Generated HTML was regenerated, not hand-resolved. The peer audit/renderer are explicitly historical; the live field manifest is the sole public-value authority. Reused flag identifiers have unique rendered occurrence anchors; F-74 explains the history and withdrawn reasoning.

The first expanded regression run caught missing direct/source-record references on 14 inherited flag rows. Fixed the flag-source lookup to inspect the recorded finding and provide an explicitly labelled repository-record fallback for audit-only claims, not a misleading "official venue verification" label. The original test was retained. Another test expectation was corrected to match the actual TikTok-target caveat; no factual check was weakened.

Final local gates before publication:

- `python3 scripts/build.py`: coverage/schema valid; historical data unchanged.
- `python3 scripts/gen_site.py`: **16 pages**, matching root/docs output.
- `python3 scripts/validate.py`: **0 failures, 0 warnings**. Counts external link occurrences only, not remote success.
- `python3 scripts/check_evidence.py`: **20 tests pass**, including negative/mutation cases for unsupported sources/values, missing coverage, fake model promotion, inconsistent itemization and incomplete offer qualification.
- Browser: all 16 pages at **375px and 1280px** (**32 page checks**), HTTP 200, one H1, no document-width overflow/page errors, labelled cells and working disclosures. Mobile/desktop screenshots inspected. The browser API required its default export and packaged NSS/NSPR libraries; initial harness launch was corrected, not misreported as a site failure. Browser dependencies/binaries/screenshots remain ignored scratch files.

These are website/evidence-record checks, **not** an exhaustive live audit of every external link or a guarantee of 2027 prices, transport or opening. All missing facts remain published. No user review is needed to publish, no foreign branch/PR is changed, and no booking/payment side effect occurred. PR/merge/deployment outcomes are recorded in `COORDINATION.md` after confirmation.
