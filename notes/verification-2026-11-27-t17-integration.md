# T17 — independent line-by-line re-verification and integration — 2026-11-27

**Session:** `arena/41324885-vegas1` (branch `arena/41324885-vegas1`).
**Base:** `main` @ `8f386c5` (the branch started from `631e611`; `main` moved 149 commits while this session
worked — see the collision record at the end).
**Scope actually used:** `FLAGS.md`, `data/activities.json`, `data/questions.json`, `data/suggestions.json`,
`scripts/gen_site.py`, `scripts/validate.py`, `notes/verification-2026-11-27-t17-integration.md` (this file),
`COORDINATION.md`, and the generated site (root `*.html` + `docs/**`).

Every check below was made by opening the official page on **27 November 2026**. "Match" means the value on
the live site equals what the source prints; nothing was inferred, and where an official page prints no value
the cell stays blank.

## A. MICHELIN tiers and counts

| # | Claim on the site | Official source opened | What the source prints | Result |
|---|-------------------|------------------------|------------------------|--------|
| A1 | Joël Robuchon holds **2 stars** | [michelin.com press release](https://www.michelin.com/en/publications/products-and-services/michelin-guide-reveals-first-ever-southwest-restaurant-selection-in-the-u-s) | "Restaurant de Joël Robuchon (Las Vegas, NV) … Two MICHELIN Stars" | match |
| A2 | Three Las Vegas restaurants hold **1 star**: é by José Andrés, Restaurant Guy Savoy, L'Atelier de Joël Robuchon | same release | All three listed; the fourth one-star (**Monte**) is in South Salt Lake, **Utah** and correctly excluded | match |
| A3 | **No three-star restaurant** in Las Vegas | same release | No Three Star section exists in the 2026 Southwest selection | match |
| A4 | **24** listings: 4 starred, 3 Bib Gourmand, 17 Recommended | [visitlasvegas.com/michelin-guide-restaurants](https://www.visitlasvegas.com/michelin-guide-restaurants/) (LVCVA) | "Las Vegas earned 24 distinctions"; 4 starred; Bib = China Poblano, Esther's Kitchen, Yen Viet Kitchen; Recommended list carries 17 names | match |
| A5 | The 17 Recommended names match the guide row for row | same LVCVA page | Anima by Edo, Bouchon, COTE, Estiatorio Milos, Gymkhana, Kabuto, Kame Omakase, Lamaii, Michael Mina, Mott 32, Partage, Pho Ga Bac Bac, Ping Pang Pong, Soulbelly BBQ, Sparrow and Wolf, Stubborn Seed, Wing Lei — identical set | match |
| A6 | Selection announced **31 Aug 2026** | michelin.com press release | Byline "31 Aug 2026" | match |

## B. Starred restaurants

| # | Claim on the site | Official source opened | What the source prints | Result |
|---|-------------------|------------------------|------------------------|--------|
| B1 | Joël Robuchon: Mon & Sun closed, **Tue–Sat 5:00–9:30 PM**, phone 702.891.7925, no under-6s, business formal, "Two Stars, 2026" | [mgmgrand.mgmresorts.com](https://mgmgrand.mgmresorts.com/en/restaurants/joel-robuchon-french-restaurant.html) | Identical hours block, phone, disclaimer, dress code and 2026 award label | match |
| B2 | é by José Andrés: Mon & Sun closed, **Tue–Sat 5:30–8:30 PM**, nine seats, two seatings nightly, reservations up to 3 months ahead, 877.893.2003 | [cosmopolitanlasvegas.mgmresorts.com](https://cosmopolitanlasvegas.mgmresorts.com/en/restaurants/e-by-jose-andres.html) | Identical hours; "seating for nine"; "Only two seatings are available nightly … up to three months in advance"; 877.893.2003 | match |
| B3 | Restaurant Guy Savoy: hours **not published** by the venue (row says see OpenTable) | [caesars.com/caesars-palace/restaurants/restaurant-guy-savoy](https://www.caesars.com/caesars-palace/restaurants/restaurant-guy-savoy) | Page shows "Opens 5:00 PM" and a star mention but **no hours-of-operation block** | stays blank — not inferred |

## C. Activities

| # | Claim on the site | Official source opened | What the source prints | Result |
|---|-------------------|------------------------|------------------------|--------|
| C1 | Mob Museum: **daily 9 AM – 9 PM** | [themobmuseum.org hours](https://themobmuseum.org/plan-your-visit/hours-directions/) | "The Mob Museum: **Daily 9 a.m. to 9 p.m.**" for all seven days | match (the 27 Nov fix, F-52/F-62) |
| C2 | The Underground: Sun–Thu 11–11, Fri–Sat 11–midnight | same page | Identical | match |
| C3 | Mob Museum prices $37.95 / $49.95 / $54.95 per adult; Premier $47.95 in the 9–11 AM and 5–9 PM online windows | [admission.themobmuseum.org](https://admission.themobmuseum.org/) | Identical figures | match |
| C4 | Mob Museum special hours: only December 2026 dates published | hours page | 17 Dec 10–9; 18, 24, 25, 31 Dec 9–4; Starlight Plaza closed for the season | match — none in the 2027 window |
| C5 | Neon Museum "2027 Admission": daily **3–11 PM**, last entry 10 PM, **from $21** adult → $42 for two | [neonmuseum.org/whats-on/all-day-admission](https://neonmuseum.org/whats-on/all-day-admission/) | "Daily 3 – 11 p.m. / Last Admission 10:00 p.m."; Adult "From $21"; processing fee applies | match |
| C6 | 2026 daytime ($25) / evening ($35) tickets expire 31 Dec 2026 | [neonmuseum.org](https://neonmuseum.org/) | "For daytime admission through December 31, 2026 … From $25"; evening "through December 31, 2026 … From $35" | match |
| C7 | High Roller: opens 12:30 PM; adult daytime **$23.50**, anytime **$34.75**, Happy Half Hour **$60**, plus taxes and fees; 30-minute rotation | [caesars.com/linq/…/high-roller](https://www.caesars.com/linq/things-to-do/attractions/high-roller) | Identical FAQ figures; "Closed / Opens 12:30PM"; 30 minutes per revolution | match |
| C8 | High Roller ticket windows | same page | Ticket cards read "Anytime / Daily / 12 PM – Close" while the FAQ reads "anytime ticket (starts 6 PM Daily)" — the page contradicts itself | conflict, published as F-63 |
| C9 | Fremont Street Experience: free entry, live music on three stages nightly | [fremontstreetexperience.com](https://www.fremontstreetexperience.com/) | "free live concerts … across three stages every single night" | match |
| C10 | Sphere: no single admission price, no February 2027 calendar | [thesphere.com](https://www.thesphere.com/) | Show carousel with Ticketmaster links; prices "subject to change"; no Feb 2027 dates | match (row stays partial, F-16) |

## D. Transit

| # | Claim on the site | Official source opened | Result |
|---|-------------------|------------------------|--------|
| D1 | Monorail fares: one ride $6.25 paper / $5.75 e-ticket; 1-day $15.50 / $13.95; 2-day $27; 3-day $33; 4-day $40; 5-day $48.25; 7-day $64 / $59.95 | [lvmonorail.com/ticket-information](https://www.lvmonorail.com/ticket-information/) | match, figure for figure |
| D2 | RTC Strip & All Access fares ($4 single / $6 two-hour / $8 24-hour / $20 three-day) | [rtcsnv.com/ways-to-travel/fares-passes](https://www.rtcsnv.com/ways-to-travel/fares-passes/) | **not re-checked** — the page did not load from this environment on 2026-11-27 (session `arena/bc27fca6-vegas1` did read it the same day and logged the residential-fare correction now published as F-60) |
| D3 | Route 203 Decatur → Las Vegas Blvd ≈ 14 min (published range 8–17) | [RTC 203 timetable PDF](https://rtcws.rtcsnv.com/routePDF/203.pdf) | not re-fetched this session; F-42 stands |

## E. Repository defects found and fixed

| # | Defect | Evidence | Fix |
|---|--------|----------|-----|
| E1 | `FLAGS.md` was **four separate markdown tables**: blank lines before F-27, F-47 and F-50 meant 11 of 43 register rows rendered as loose text on GitHub rather than table rows. | table-block scan of the file: (6–33), (35–38), (40–42), (44–47), (74–81) | blank lines removed; F-01–F-53 are now one 39-line table. The F-58–F-63 audit table keeps its own heading. The non-contiguity of F-31–F-46 is now stated in the file. |
| E2 | `scripts/validate.py` warned on any page containing the letters "nan": it fired on the word *provenance*. | `WARN: flagged.html: contains literal 'nan'` reproduced before the fix | validator now matches standalone `None` / `nan` tokens on word boundaries |
| E3 | Activities carried social links but **no record of where each handle came from**, and Q-07 still described Instagram/TikTok as "almost entirely blank" although F-53 records 19/24 restaurant Instagrams. | `data/questions.json` Q-07 vs F-53; activities table | Q-07 answer, problem, substitution and closure route rewritten to the 27 Nov coverage and the evidence standard; a "Where each social link came from" panel added under the activities table, filled from a new `social_note` field on all five activities; **S-16** added so the remaining 5 Instagram and 22 TikTok gaps are a decision item rather than silent blanks. |

## F. Open irregularity for the owner (not changed by this session)

| # | Observation | Why it matters | Options |
|---|-------------|----------------|---------|
| P-01 | The merged site now presents the **32 hotels alphabetically, "not ranked"**, with official-rate cells blank pending property quotes (F-58/F-59/F-62/F-63). The brief asked for hotels **ranked** by Michelin proximity inside an hour and by price. | The page is now defensible on evidence but no longer answers the ranking question the couple asked. | (a) leave as is; (b) add an explicitly **indicative** ranking built from the dated OTA snapshots, labelled "unverified quote, not a booking offer"; (c) rank only the subset with a confirmed named-room official rate once captured. This session did not choose between them — it is a decision for the couple, logged in `COORDINATION.md`. |

## G. Collision record — two sessions ran "T17" at the same time

This session started from `main` @ `631e611` and wrote, on its own branch: a Mob Museum hours correction
(as F-52), four activity social links with provenance (as F-53), a High Roller ticket-window conflict flag
(as F-54), a `FLAGS.md` table repair, the `validate.py` fix, a Q-07 update and a suggestion. While it worked,
`main` advanced 149 commits and two other sessions published the **same findings under the same IDs**:
F-52 (Mob Museum hours), F-53 (TikTok coverage), F-62 (Mob Museum, strict-evidence re-statement) and F-63
(High Roller conflict).

Resolution: the branch was reset onto `origin/main` and every finding was **re-applied by hand against main's
current structure**, keeping main's wording and IDs and discarding this session's duplicate flag rows
(F-54 is **not** used). What survived from this session is only what was still missing on `main`: the
`FLAGS.md` table repair, the `validate.py` false positive, the social-provenance panel, the Q-07 correction
and S-16. Nothing from another session was overwritten, and the discarded duplicate rows are recorded here
rather than in the live register. The pre-reset commits remain reachable in this clone's reflog
(`858351a`, `9462684`) but are not pushed as a branch.

**Build state:** `python3 scripts/build.py && python3 scripts/gen_site.py && python3 scripts/validate.py`
→ 13 pages · 0 failures · 0 warnings; root and `docs/` byte-identical (`cmp` per page).
