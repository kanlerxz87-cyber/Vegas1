# VERIFICATION.md — line-by-line verification log

Session: 48dbf0ae · Branch: `arena/48dbf0ae-vegas1` · Data date: **2026-11-25**

Policy: every displayed price/hour/address was read from the linked source on 2026-11-25.
Unconfirmable values are **left blank** and listed in `flagged.html` §A — never inferred.
Source conflicts are displayed as conflicts (`flagged.html` §B), not silently resolved.

## Sources used (by page)

### hotels.html
| Row | Source URL | What was read |
|---|---|---|
| Flamingo 7n | booking.com/hotel/us/flamingo-casino.html?checkin=2027-02-15&checkout=2027-02-22&group_adults=2&no_rooms=1&selected_currency=USD | Assigned-on-Arrival 1 king $625.65 total before taxes, −40% BF, resort fee included, free cancel 2027-02-13; Fab 2Q $667.55; search card $709 incl tax |
| Flamingo 3n | same host, checkout=2027-02-18 | 1 king $166.65 before tax (−13%); Fab 2Q $182.05 (−21%); $50/nt resort fee included; free cancel 2027-02-13 |
| Flamingo Mar week | checkout=2027-03-08 | Assigned king $925.85 (−48%); Fab 2Q $1,019.85 (−50%) |
| MGM Grand 7n | booking.com/hotel/us/mgm-grande.html?checkin=2027-02-15&checkout=2027-02-22... | MGM King/2Q $1,508.50 before tax (−31%); refundable $1,682 |
| MGM Grand 3n | checkout=2027-02-18 | King/2Q $614.10 non-ref (−31%); BF+credit $665.91 (−25%, $100 credit); refundable $887; free cancel 2027-02-12 |
| MGM Feb 22 week | checkout=2027-03-01 | Studio King $1,293.60 (−30%) |
| Bellagio 7n | booking.com/hotel/us/bellagio.html?checkin=2027-02-15&checkout=2027-02-22... | Premier King $3,072.30 (−34% BF non-ref); +credit $3,330.65; refundable $4,593 |
| Cosmopolitan 7n | booking.com/hotel/us/the-cosmopolitan-of-las-vegas-las-vegas2.html?... | Terrace Studio $3,432.80 (−34%) |
| ARIA 7n | booking.com/hotel/us/aria-resort-casino.html?... | Deluxe 2Q Accessible $3,797.50 (−35% non-ref, $488/nt); Strip View King $3,936; refundable $5,745 |
| Caesars Palace 7n | booking.com/hotel/us/harrah-s-caesars-palace.html?... | Assigned-on-Arrival king $1,580 ($171/nt avg, $55/nt resort fee); Nobu Deluxe $1,619; Julius $1,622 |
| Venetian 7n | booking.com/hotel/us/the-venetian-resort-casino.html?... | Luxury King Suite BF $4,573.16 ($598/nt, −48%, cancel 2027-02-12); Prestige $6,127.67; non-BF $8,761 |
| LINQ / Horseshoe | booking.com city search (dest_id=20079110) | Search cards: LINQ $640 incl tax (was $1,004); Horseshoe $813 incl tax (was $1,439) |
| Rio / Gold Coast / Orleans | same city search | Masquerade at Rio $483; Gold Coast $768 (2 full beds); Orleans $1,067 — tax inclusion not stated → blank |
| Super Bowl LXI date | news.kalshi.com/p/super-bowl-lxi + trendgoals.com + nflplayoffpass.com | Sun Feb 14, 2027, SoFi Stadium (LA) — multiple sources agree |
| Presidents' Day 2027 | calendar (3rd Monday) | Mon Feb 15, 2027 |
| Tax rate | every Booking.com quote line | "Excluded: 13.38 % TAX" |
| BF promo window | quote banners | "discount on select stays between Nov 19, 2026 and Dec 31, 2027" |

### michelin.html
| Row | Source URL | What was read |
|---|---|---|
| Distinction counts | michelin.com press release (Southwest selection) + Eater/8NewsNow lists | 1×2★ Robuchon, 1★ L'Atelier/Guy Savoy/é; Bib: China Poblano, Esther's, YEN Viet; 17 listed |
| Robuchon hours/price | hotelmenuguide.org/joel-robuchon-menu + smartervegas + LVA | 3 conflicting hour sets → B1 flag; dégustation ~$525 pp (Oct 2026) |
| L'Atelier hours/price | opentable.com/r/latelier-joel-robuchon-mgm-grand... + lasvegaswonders | Mon, Thu–Sun 5–9pm closed Tue–Wed; tasting $225–275 pp |
| Guy Savoy | opentable.com/r/restaurant-guy-savoy-caesars-palace-las-vegas + caesars.com official page | Tue–Sat 5:00–8:45pm; à la carte $100–290; Symphony $1,000 pp w/ pairing; Krug table $1,500 pp; IG @guysavoylasvegas |
| é | lasvegascompass.com + vegasnearme + ebyjoseandres.com | Tue–Sat 5:30/8:30 seatings; Sunday conflict → B2; ~$300s pp 2026 |
| China Poblano | smartervegas + opentable profile 46390 + tripadvisor menu | Hours (weekend conflict → B8); $31–50 pp; José's Way $60 pp; IG @chinapoblano |
| Esther's Kitchen | guide.michelin.com page + menutoeat menu + LVA | Official guide hours; pastas $18–36; LVA "2 under $100"; estherslv.com; IG/TikTok @estherskitchenlv (FSR magazine) |
| YEN Viet | vegasnearme + wanderlog + foodjoyy menu | Mon/Wed–Sun 10–9 closed Tue (Tripadvisor 10–7 → B7); bun mam $14 etc.; yenvietkitchen.com |
| Anima by EDO | animabyedo.com (official) | Dinner 5pm daily last res 8:45; lunch M–F 11–2; tapas $8–28, entrées $36–45, tasting $85 pp; IG @animabyedo |
| Bouchon | thomaskeller.com reservations page | Dinner Sun–Sat 5–10pm; brunch Thu 8–1, Fri–Sun 8–2; LVA $75–125 pp band |
| COTE | cotekoreansteakhouse.com (official) + eater opening + spotlights | Hours (internal conflict → B11); Butcher's Feast $88.88 pp; IG @cotekoreansteakhouse |
| Milos | smartervegas + dimhour + LVA + lasvegaswonders | Hours conflict → B3; dinner $220–380 for 2; lunch $45 pp promo; estiatoriomilos.com |
| Gymkhana | vegas.eater.com/openings/130177 + stocktitan MGM PR + islands.com | Sun–Thu 5–10, Fri–Sat 5–10:30 (conflict → B10); mains $28–75; tasting $165 pp |
| Kabuto | guide.michelin.com page + yelp | Hours daily 5:30–9pm; **no price found → blank (A1)**; kabutolv.com |
| Kame Omakase | guide.michelin.com page + joinpearl | Daily 17:30–22:00; ≈$300 pp; sushikame.com |
| Lamaii | yelp (Nov 2026) | Hours M–W to midnight, Th–Su to 2am; menu prices $9–26; no official site (A6) |
| Michael Mina | opentable + lasvegasmagazine Oct 2026 + bellagio.mgmresorts.com | Hours conflict → B4; tasting $295 (autumn)/$250 (summer) pp; supplements $55/$69 |
| Mott 32 | mott32.com/las-vegas (official) + venetian fact sheet PDF | Lunch M–F 11–2:30, dinner daily 5–10, brunch 10:30–2:30; duck $130–148; dinner 2 $240–380 |
| Partage | opentable profile 1005940 + yelp + inside-las-vegas menu + restaurantjump | Tue–Sat 5:30–9:30 closed Mon/Sun; price conflict → B9; partage.vegas |
| Pho Ga Bac Bac | guide.michelin.com + yelp | Hours conflict → B6; chicken $14.98, rolls $13.73; no official site (A6) |
| Ping Pang Pong | guide.michelin.com + LVA + tripadvisor | Daily 10–3; LVA prices dated → D2; Gold Coast URL not captured (A6) |
| SoulBelly | soulbellybbq.com find-us (official) + menu sources | Tue–Thu 11–9, Fri–Sat 11–10, Sun 11–9; brisket $21, sandwiches $16–23.50 |
| Sparrow + Wolf | opentable + sparrowandwolflv.com + lasvegaswonders | Dinner daily 5–10 (4:30 conflict noted); tasting $142 pp; dinner 2 $140–210 |
| Stubborn Seed | opentable profile 1335541 + stubbornseed.com + timeout | Bar 4–10, dinner 5–10 daily; tasting $145–175 pp, pairing +$70 |
| Wing Lei | smartervegas + joinpearl + LVA | Hours conflict → B5; duck tasting $88 pp; dinner 2 $250–400; Wynn URL not captured (A6) |

### activities.html
| Row | Source URL | What was read |
|---|---|---|
| Transit baseline | rtcsnv.com FAQ + routepdf/203.pdf + transitguide.pdf | Deuce 24h 15/20-min headways; SDX 9–midnight; fares $6/$8/$20/$35; south Strip→downtown 30–60 min; Route 203 Spring Mountain; RED LINE note |
| Fountains of Bellagio | bellagio.mgmresorts.com/en/entertainment/fountains-of-bellagio.html (official) | Full weekly show schedule; free |
| Conservatory | lasvegascompass (3rd party) | 24h claim → flagged (unverified hours) |
| High Roller | caesars.com/linq/things-to-do/attractions + 2026 reseller guides | Hours/prices 2026 only → flagged for 2027 (D4) |
| Fremont Street | fremontstreetexperience.com (official) + usnews | 24/7 free; light shows hourly 6pm–2am; IG @fremontstreet |
| Mob Museum | admission.themobmuseum.org (official) + themobmuseum.org | Daily 9–9; GA from $35; Premier $54.95; Underground hours; IG @themobmuseum |
| Neon Museum | neonmuseum.org/tickets-and-experiences (official) | 2027 admission daily 3–11pm from $21; IG @theneonmuseumlasvegas + TikTok (About page) |
| Sphere | thesphere.com | Event-dependent → blank + flag (A2) |
| Chinatown | rtcsnv.com/routepdf/203.pdf | Route 203 verified; 6 listed restaurants in zone (michelin.html) |
| Arts District | firstfridaylv.com + michelin page | Feb 5 2027 First Friday derived → flagged (D6) |

### Excluded sources (flagged.html §C)
- Las Vegas Magazine Bib list (duplicates recommended list; contradicts guide) — rejected.
- Aggregator/per-diem/monthly-average prices — not date-specific — rejected.
- COTE "Michelin-starred" applied to LV room — star is NYC's; LV = listed — corrected.

## Checks remaining before "final" (T09)
1. Click-test every URL in all HTML files (external + internal).
2. Re-pull COORDINATION.md (`git pull --rebase`) before final push.
3. Enable GitHub Pages on `arena/48dbf0ae-vegas1` and confirm the published URL loads.
4. Resolve or re-verify B1–B12 conflicts if official pages answer them.
