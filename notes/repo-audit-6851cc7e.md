# Line-by-Line Repository Review & Fresh Official-Source Verification (`arena/6851cc7e-vegas1`, Task T20)

- **Audit date:** `2026-11-27` (UTC)
- **Audited commit on `main`:** `99a3506` (after PRs #16–#55)
- **Session branch:** `arena/6851cc7e-vegas1`
- **Live GitHub Pages root:** `https://kanlerxz87-cyber.github.io/Vegas1/`
- **Session verification dashboard:** `https://kanlerxz87-cyber.github.io/Vegas1/docs/session-6851cc7e/`

---

## 1. Executive Assessment of `main@99a3506`

Across 15 parallel live `fetch_page` batches (~115 official primary-source URLs fetched directly on `2026-11-27`) and a line-by-line inspection of `scripts/*.py`, `data/*.json`, `FLAGS.md`, `COORDINATION.md`, and generated HTML pages, we found:

1. **What `main@99a3506` gets right:**
   - All **24 Las Vegas MICHELIN Guide 2026 Southwest distinctions** (`1×2★` Joël Robuchon; `3×1★` é by José Andrés, Restaurant Guy Savoy, L'Atelier de Joël Robuchon; `3 Bib Gourmand` China Poblano, Esther's Kitchen, YEN Viet Kitchen; `17 Recommended`) match MICHELIN's official Aug 31, 2026 press release and LVCVA's directory.
   - `scripts/validate.py` and `scripts/check_evidence.py` pass on `main@99a3506`, and `data/socials.json` documents 21/24 restaurant Instagram links and 5/6 activity Instagram links with per-account provenance.
   - `FLAGS.md` (`F-58`–`F-66`) rightly stopped presenting third-party Booking.com snapshots as verified official hotel quotes and fixed Anima by EDO's `$65` Monday couple special, Kabuto's `(702) 676-1044` phone, Mob Museum's daily `9 AM–9 PM` hours, and Wing Lei / Partage tasting prices.

2. **Critical & medium defects remaining in `main@99a3506` (14 line-by-line irregularities):**
   - **RA-01 (High — False MICHELIN star claim in live `dining.html` & `scripts/gen_site.py`):** `dining.html` line 72 states *"the cheapest starred dinner on this site (Wing Lei, $397.76 for two)"*, directly violating `F-03` (*"the 2026 Guide lists [Wing Lei] Recommended, not starred. Counted as unstarred in every total on this site"*).
   - **RA-02 (High — Orphan `costs.html` / `docs/costs.html` still live on `main`):** When `costs.html` was superseded by `dining.html`, `costs.html` was left committed in both `/` and `/docs/`. It still displays the broken `$6.00` 9-day RTC pass bug (`RTC 3-day pass × 3 each = $6.00` instead of `$120.00`), outdated nav links, and Booking.com OTA hotel totals (`$1,125` Nobu, `$1,580` Caesars, `$3,072` Bellagio) withdrawn under `F-58`.
   - **RA-03 (Medium — Rendering bug `<h2>1</h2>` on `suggestions.html`):** In `scripts/gen_site.py` `build_suggestions()`, `SUGGESTIONS_HEAD` is a 1-element tuple/string structure whose `len()` renders a stray literal `<h2>1</h2>` heading on `suggestions.html`.
   - **RA-04 (Medium — Copy/paste flag typo on `sources.html`):** `scripts/gen_site.py` `build_sources()` pairs `F-39` with `F-29`'s hotel-OTA text instead of `F-39`'s Venetian withdrawal text.
   - **RA-05 (High — Four official restaurant menus with published prices still marked `"Not published officially"` in `data/restaurants.json`):**
     - `stubborn-seed` (`data/restaurants.json:803`): Official Resorts World PDF (`https://www.rwlasvegas.com/pdf/stubborn-seed-tasting-menu-11-25-2026/`) publishes **Tasting Menu `$160/pp` = `$320.00` exact for 2 adults** (Elevated `+$35/pp`; à la carte mains `$44–$92`).
     - `kabuto` (`data/restaurants.json:500`): Official `kabutolv.com/reserve` → Resy venue page (`https://resy.com/cities/las-vegas-nv/venues/kabuto-edomae-sushi`) publishes **Yoroi Course `$130/pp` (`$260.00` for 2) and Kabuto Course `$185/pp` (`$370.00` for 2)**, plus `$100/pp` <24h cancellation policy and holiday-menu-only dates Dec 18–Jan 10.
     - `china-poblano` (`data/restaurants.json:179`): Official venue menu (`https://www.chinapoblano.com/menus/`) publishes **José's Way Tasting Menu at `$60/pp` = `$120.00` exact for 2 adults** (superseding the secondary Eater `≈$50` note in `F-05`).
     - `soulbelly-bbq` (`data/restaurants.json:662`): Official venue menu (`https://soulbellybbq.com/menu`) publishes **Chef's Choice for 2 at `$80.00` exact** (and sandwiches/combos `$16–$30/pp` → `$32–$80` for 2).
   - **RA-06 (Medium — Three factual errors in `latelier-robuchon` row, `data/restaurants.json:84–97`):**
     1. `notes` claims L'Atelier *"Received a 2026 MICHELIN Service Award alongside its star"* — MICHELIN's official Aug 31, 2026 press release awarded the 2026 Service Award to **Sean Christopher at two-star Joël Robuchon**, not L'Atelier.
     2. `notes` states *"Reservations phone per the MGM page: 702.891.7925"* — `702.891.7925` is Joël Robuchon's number; L'Atelier's official MGM page prints **`702.891.7358`** (contradicting `phone` on line 94 of the same object).
     3. `exceptions` states *"No guests under 6"*, whereas the official MGM page states *"does not include children 6 and under"* (excluding 6-year-olds as well).
   - **RA-07 (Medium — `china-poblano` Sunday closing hour off by 30 minutes & missing official phones, `data/restaurants.json:176,189`):** Stored as `Sat–Sun 10:00 AM – 10:30 PM` with blank `phone`; official Cosmopolitan MGM page prints **`Sunday: 10:00 AM to 10:00 PM`** and phones `877.893.2003` / `702.698.7900`.
   - **RA-08 (Low — `estiatorio-milos` Friday–Saturday closing hour omitted, `data/restaurants.json:336`):** Stored as `"11:30 AM – 10:30 PM (Fri–Sat from 11:30 AM)"`; official Venetian page states **Fri–Sat `11:30 AM – 11:00 PM`** (30 min later).
   - **RA-09 (Low — `bouchon` tower name stale, `data/restaurants.json:303`):** Stored as `Venezia Tower`; official Venetian page (`bouchon.html`) specifies **`The Venetian South Tower`, 10th floor**.
   - **RA-10 (Low — `pho-ga-bac-bac` abandoned Instagram handle left in `notes`, `data/restaurants.json:733`):** `instagram` was updated to `@phogabacbac702` (`F-56`), but `notes` still says `Instagram verified 2026-11-27: https://www.instagram.com/bestchickenpho/`.
   - **RA-11 (Medium — Internal self-contradiction in `data/activities.json` for `neon-museum` & `fremont-street`):** Both rows list 3 verified YouTube video URLs in `"youtube"` (including official channel uploads `ewrNfjNa4w4` and `KDARquYGk_M`), yet their `social_caveat` strings on lines 129 and 154 state *"so no YouTube link is published"*.
   - **RA-12 (Medium — `data/transit.json` RTC local fare & Vegas Loop station list):**
     - `rtc` still states *"Nevada local fares are $1"*; official RTC `fares-passes` page lists **`$2.00` Regular Residential single ride** (`$1.00` is Reduced Fare only for seniors/youth/disabled/veterans).
     - `vegas-loop` lists 7 stations, whereas `boringcompany.com/projects/las-vegas-loop` lists **14 active stations** (adding `Fontainebleau`, `Sahara`, `Airport T1`, `Airport T3`, `Turnberry Towers`, `LVCC Central Plaza`) and official `$5` (LVCC→Strip) / `$8` (LVCC→Thomas & Mack) sample fares.
   - **RA-13 (Medium — `FLAGS.md` duplicate IDs `F-52`–`F-57` across merge trains):** Already noted in `COORDINATION.md` line 825; two parallel PR trains used `F-52`/`F-53` and `F-54`–`F-57`.
   - **RA-14 (High — `data/official-rates.json` covers only 3 hotels on 1 date window, leaving `Q-06` & `W-03` open):** Canonical `hotels.html` blanks all 32 decision rows (`F-58`), and `data/official-rates.json` only sampled 3 hotels on `Feb 15–22, 2027` with zero March comparison.

---

## 2. How Task T20 Closes the Official-Source Gap Without Touching Active Claims

In `data/session-6851cc7e-*.json` and `docs/session-6851cc7e/`:
- **15 Las Vegas resorts** are priced directly from **official first-party property booking engines** on `2026-11-27` (`caesars.com/book/room-list`, `reservations.rwlasvegas.com/ibe/shop.aspx`, `reserve.fontainebleaulasvegas.com/ibe/shop.aspx`, `reservations.wynnlasvegas.com/ibe/details.aspx`, and `be.synxis.com` for Downtown Grand) across **both** `Feb 15–22, 2027` and `Mar 14–21, 2027` for **named Queen+/King rooms with private bathrooms** and itemized resort fees + `13.38%` Clark County lodging tax.
- **Empirical resolution of the Feb-vs-March mystery (`Q-06` / `F-29`):**
  - **Center-Strip Caesars resorts (8 properties) + Downtown Grand + Encore** are **3%–28% cheaper in `Feb 15–22, 2027`** (the couple's preferred window!) because NCAA March Madness First Weekend (`Mar 18–21, 2027`) surges Center-Strip sportsbook hotels.
  - **North-Strip LVCC-adjacent luxury towers (Hilton/Conrad/Crockfords at Resorts World, Fontainebleau, and Wynn Tower)** are **4%–19% cheaper in `Mar 14–21, 2027`** (and Conrad is sold out `Feb 16–17, 2027`) due to a mid-week North-Strip convention peak on `Feb 16–17, 2027`.
- **Best booking purchase window (`Nov 27 – Dec 4, 2026`):** Live Cyber Monday / Black Friday promotions are active **right now** (`Fontainebleau Bleau Friday`: book by **Dec 2, 2026** for `$0` resort fee on free member sign-up + `$350` dining credit; `Wynn/Encore Cyber Exclusive`: book **Nov 20 – Dec 4, 2026** for up to 20% off + `$300` resort credit; active Cyber Monday Early Access at `Caesars`, `Resorts World`, and `Downtown Grand`).
- **11 of 24 MICHELIN restaurants** carry official-menu or official-booking-platform 2-adult totals (`9` exact published menu prices + `2` explicitly labelled dish-level estimates; `Michael Mina` flagged **temporarily closed** and excluded from active trip math; `13` unpriced venues left strictly blank).
