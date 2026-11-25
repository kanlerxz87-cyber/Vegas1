# COORDINATION — Vegas1

**Repo:** `kanlerxz87-cyber/Vegas1` · **Purpose:** Plan a Las Vegas vacation (2 adults, Feb 15 – Mar 23, 2027, preferred Feb 15–18) and build a GitHub Pages dashboard.

## Parallel-session rules
1. **Claim before work:** add your session id to the task you take, commit + push that claim **first**.
2. **Pull before push:** `git pull --rebase` before **every** push.
3. **One branch per session:** work only on your session branch; open PRs from it.
4. **Shared files:** append to `notes/research-log.md` (research findings) or `data/*.json` (final datasets) — never rewrite another session's entries. Site files go in `docs/` (final integration builds/rebuilds the site from `data/`).
5. **Small commits.** Verify everything; never infer values — leave blank + flag unverified.
6. **Hand-off:** when done, fill the Session Log below (summary + key answers + source links + flaggable items + timestamp).

## Task list & claims

| # | Task | Claimed by | Status |
|---|------|-----------|--------|
| 1 | Repo review + setup (branch, COORDINATION, file inventory) | session-af795000 | ✅ done 2026-11-25 |
| 2 | Michelin Guide Las Vegas research (listed vs starred vs Bib, addresses, links) | session-af795000 | ✅ done 2026-11-25 (all 24 entries) |
| 3 | Hotel research + total price table (7 nt) + cheapest upcoming booking time | session-af795000 | ✅ done 2026-11-25 (7 properties verified; MGM/Venetian/FB blocked → flagged) |
| 4 | Restaurant research (hours, costs for 2, social links, venue links) | session-af795000 | ✅ done 2026-11-25 (24/24 rows; gaps blank+flagged per rules) |
| 5 | Activities research + transit analysis (no subway in LV → monorail/bus) | session-af795000 | ✅ done 2026-11-25 (10 activities; transit cluster analysis) |
| 6 | GitHub Pages dashboard build (docs/) | session-af795000 | ✅ done 2026-11-25 (8 pages + data/*.json) |
| 7 | Final verification + integration + PR + publish | session-af795000 | ✅ done 2026-11-25 (see Session Log) |

## Session Log (append entries; include summary, key answers, source links, flaggable items, timestamp)

### session-af795000 · 2026-11-25 · FINAL (tasks 1–7 complete)

**Deliverables:** `docs/` GitHub Pages site (index.html = executive summary; hotels.html; michelin.html; activities.html; analysis.html; suggestions.html; open-questions.html; flagged.html; style.css) + machine-readable `data/michelin.json`, `data/hotels.json`, `data/activities.json` + research backup `notes/research-log.md`. Branch `arena/af795000-vegas1`, PR from it.

**Key answers (verified 2026-11-25 from official sources, links below):**
- **Michelin (2026 Southwest, announced Aug 26, 2026):** Las Vegas = 24 distinctions — **4 starred** (2★ Restaurant de Joël Robuchon, MGM Grand; 1★ Guy Savoy Las Vegas, Caesars; 1★ é by José Andrés, Cosmo; 1★ L'Atelier de Joël Robuchon, MGM Grand), **3 Bib Gourmand** (China Poblano, Esther's Kitchen, YEN Viet Kitchen), **17 Recommended/Selected** (Anima by Edo, Bouchon, COTE, Estiatorio Milos, Gymkhana, Kabuto, Kame, Lamaii, Michael Mina, Mott 32, Partage, Pho Ga Bac Bac, Ping Pang Pong, SoulBelly, Sparrow+Wolf, Stubborn Seed, Wing Lei). Source: https://www.michelin.com/en/publications/products-and-services/michelin-guide-reveals-first-ever-southwest-restaurant-selection-in-the-u-s + https://www.visitlasvegas.com/michelin-guide-restaurants/ (all official restaurant links in data/michelin.json).
- **Cheapest 7-night window in Feb 15 – Mar 23, 2027 = the preferred week Feb 15–22, 2027** (verified vs exact-dates searches + official rate calendars at all checked properties). 7-nt totals incl. resort fee, excl. tax (2 adults): Flamingo $595 ($85/nt) · Horseshoe $763 ($109) · Planet Hollywood $1,092 ($156) · Caesars Palace $1,582 ($226) · Paris $1,526 ($218) · Resorts World Hilton ≈$1,942 ($277 avg) · Wynn Resort King $4,739 ($677 Cyber / $833 Flexible). Sources (official booking engines, dated URLs in data/hotels.json): caesars.com/book/room-list (propCodes clv/flv/plv/phv/blv), reservations.wynnlasvegas.com/ibe/details.aspx, reservations.rwlasvegas.com/ibe/shop.aspx.
- **Booking timing:** Wynn Cyber sale must be booked **Nov 20 – Dec 4, 2026** ($677/nt + $75/day credit; 1-nt dep, 72h cancel). Caesars promos auto-apply (book by Dec 20/30, 2027; Caesars Rewards signup −15%). Resorts World Cyber 50% live; check "ALL RESORT, NO FEES" offer. Prices sampled 2026-11-25; re-verify before paying.
- **Verified costs for 2** (exact, from official menus): Wing Lei tasting $397.76 · Michael Mina tasting $590 (++!) · Stubborn Seed tasting $320 · Partage $260–$420 · Kabuto $260–$370 (Resy) · Anima tasting $170 · Guy Savoy à la carte $380–$1,180 (menu eff. 11/5/2026) · Esther's mains $42–$60. Reported-only (flagged): Robuchon ≈$425–$525 pp, é ≈$290–$368 pp.
- **Transit:** Las Vegas has NO subway (brief premise corrected) — RTC buses (Deuce/SDX/202) + Las Vegas Monorail (7 stations Sahara–MGM Grand). All 24 Michelin restaurants ≈≤60 min by bus+walk from all listed hotels (estimates flagged); Chinatown cluster (6) on Spring Mountain; Red Rock & Hoover Dam fail the ≤60-min transit constraint (car only) — flagged.
- **Open hours highlights:** Wing Lei dark Tue–Wed; Robuchon dark Sun+Mon; L'Atelier dark Tue–Wed; Guy Savoy "from 5 PM" (weekly unverified); Pho Ga Bac Bac 24h; SoulBelly dark Mon; Michael Mina seasonal closures Nov–Dec 2026 (Feb'27 unknown — Q2).
- **Socials verified:** @gymkhanalasvegas, @soulbellybbqlv, Kabuto IG posts (official site), @theneonmuseumlasvegas + TikTok @neonmuseumlasvegas, Caesars property IG/YouTube. Others blank+flagged (Q10).

**Flaggable items:** full register in `docs/flagged.html` (10 sections A/B/C): LV Magazine mislabels 17 Selected as Bib; historic≠current stars; name mismatches (MICHELIN vs LVCVA); zola "Vanderpump Hotel" = possible Cromwell rebrand (unconfirmed); Stubborn Seed $145 blog vs $160 official; RW resort-fee legend conflict; MGM/Venetian/Fontainebleau room rates unverifiable by automation (blank+flag); Kame JS-only site; CLV Mar 2 sold out; Caesars calendar drift ±$14.

**For other sessions:** all raw findings also in `notes/research-log.md` (authoritative backup). Do not rewrite `docs/` without re-running the verification rule (every row source-linked; blanks flagged). Suggested follow-ups D1–D6 in `docs/suggestions.html` (map, calculator, price-watch script, .ics export, social sweep, provenance page) await user review before implementation.
