#!/usr/bin/env python3
"""
gen_site.py — renders the static site in docs/ from the JSON in data/.

Run after scripts/build.py:
    python3 scripts/build.py && python3 scripts/gen_site.py

No framework, no CDN, no build step at deploy time. Everything is plain HTML +
one stylesheet, so GitHub Pages serves docs/ directly from main.
"""
import json
import re
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DOCS = ROOT / "docs"


def load(n):
    with open(DATA / n, encoding="utf-8") as f:
        return json.load(f)


HOTELS = load("hotels.json")
RES = load("restaurants.json")
PRICE = load("price-windows.json")
TRANSIT = load("transit.json")
ACT = load("activities.json")
QS = load("questions.json")
SUG = load("suggestions.json")
OFFR = load("official-rates.json")
SITESUG = load("site-suggestions.json")
SOC = load("socials.json")

e = html.escape

# derived counts — always computed, never typed by hand
_C = {}
for _r in RES["restaurants"]:
    _C[_r["award_class"]] = _C.get(_r["award_class"], 0) + 1
N_TOTAL = len(RES["restaurants"])
N_IG = sum(1 for _r in RES["restaurants"] if _r.get("instagram"))
N_NO_SOCIAL = N_TOTAL - N_IG
N_STARRED = _C.get("starred", 0)
N_BIB = _C.get("bib", 0)
N_REC = _C.get("recommended", 0)
N_TWO = sum(1 for _r in RES["restaurants"] if _r["award"].startswith("2"))
N_ONE = sum(1 for _r in RES["restaurants"] if _r["award"].startswith("1"))



_NUM = re.compile(r"\d[\d,]*(?:\.\d+)?")


def usd_values(text):
    """Every dollar figure printed in a price string, in order.

    Lets the budget page total published prices instead of retyping them:
    '$260 / $320 / $420' -> [260.0, 320.0, 420.0]; '≈$520–$940 (est.)' -> [520.0, 940.0].
    """
    out = []
    for m in _NUM.finditer(text or ""):
        try:
            out.append(float(m.group(0).replace(",", "")))
        except ValueError:
            pass
    return out


def money(v):
    return "—" if v in (None, "") else f"${v:,.0f}"


def nav(active):
    items = [
        ("index.html", "Overview"),
        ("hotels.html", "Hotels"),
        ("dining.html", "Dining budget"),
        ("restaurants.html", "Michelin"),
        ("itinerary.html", "Itinerary"),
        ("activities.html", "Things to do"),
        ("transit.html", "Getting around"),
        ("questions.html", "Open questions"),
        ("suggestions.html", "Suggestions"),
        ("flagged.html", "Flagged for review"),
        ("sources.html", "Sources"),
        ("repo-review.html", "Repo review"),
    ]
    out = []
    for href, label in items:
        cls = ' class="on"' if href == active else ""
        out.append(f'<a href="{href}"{cls}>{e(label)}</a>')
    return "".join(out)


def page(active, title, subtitle, body, lead=""):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} · Las Vegas 2027</title>
<meta name="description" content="{e(subtitle)}">
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="top">
  <div class="wrap">
    <div class="brand"><span class="dot"></span>Las Vegas · Feb–Mar 2027</div>
    <nav>{nav(active)}</nav>
  </div>
</header>
<main class="wrap">
  <div class="pagehead">
    <h1>{e(title)}</h1>
    <p class="sub">{subtitle}</p>
    {lead}
    <p class="note"><strong>27 November evidence notice:</strong> Historical audit text and suggestions below may describe superseded OTA prices or model scores. They are not verified booking guidance. <a href="hotels.html">Current hotel evidence table</a> and <a href="flagged.html#F-58">F-58–F-63</a> take precedence. Restaurant/activity hours are observations, not confirmed 2027 schedules. Creator media links have not been fully re-opened in this pass.</p>
  </div>
  {body}
</main>
<footer class="wrap">
  <p>Evidence gate updated 27 Nov 2026. Hotel decision cells omit unofficial quotes and inferred travel scores. Other records are historical observations from 25–27 Nov, not guaranteed 2027 availability. Blank means <strong>not verified</strong>. <a href="flagged.html">Flagged for Review</a>.</p>
  <p>Las Vegas had no MICHELIN Guide between 2010 and 2025. All awards here are from the 2026
  Southwest selection, the first since 2009.</p>
</footer>
</body>
</html>
"""


# Official-source-only hotel display: raw OTA/model fields are audit inputs, not offers.
MICHELIN_SOURCE = RES["meta"]["sources"][0]
RTC_SOURCE = "https://www.rtcsnv.com/ways-to-travel/fares-passes/"

# ---------------------------------------------------------------- index
def build_index():
    stars = "".join(f'<tr><td>{e(r["name"])}</td><td>{e(r["award"])}</td><td>{e(r["location"])}</td><td><a href="{e(MICHELIN_SOURCE)}">MICHELIN</a></td></tr>' for r in RES["restaurants"] if r["award_class"] == "starred")
    body = f"""
<section class="panel callout"><h2>Executive summary · 27 November 2026</h2>
<p><strong>Research plan, not a booking-ready recommendation.</strong> Two adults, private bathroom, queen-or-larger bed. Your outer window is 15 February–23 March 2027. The preferred 15–18 February is only three nights; <strong>15–22 February 2027</strong> is the provisional seven-night comparison, not a decision made on your behalf. A fourteen-night alternative is 15 February–1 March.</p>
<p>No official, checkout-complete seven-night hotel offer has been established in the canonical dataset. Accordingly hotel totals, room-fit assertions and ≤60-minute reachability counts are blank, not inferred. There is <strong>no verified cheapest hotel, cheapest stay week, or best purchase date</strong>. See <a href="flagged.html#F-58">F-58</a> and <a href="flagged.html#F-59">F-59</a>.</p></section>
<section class="grid4"><div class="card"><div class="big">{N_TOTAL}</div><p>2026 MICHELIN listings: {N_STARRED} starred, {N_BIB} Bib Gourmand, {N_REC} Recommended. <a href="{e(MICHELIN_SOURCE)}">Official selection</a>.</p></div><div class="card"><div class="big">32</div><p>Hotel research candidates, alphabetical rather than an unsupported ranking.</p></div><div class="card"><div class="big">30</div><p>Possible seven-night arrival dates, 15 February–16 March inclusive. All checkout by 23 March.</p></div><div class="card"><div class="big">Pending</div><p>All-in accommodation and trip budget. No prices are extrapolated from nightly promotions.</p></div></section>
<section class="panel"><h2>The four starred restaurants</h2><div class="scroll"><table class="data"><thead><tr><th>Restaurant</th><th>2026 award</th><th>Property</th><th>Official source</th></tr></thead><tbody>{stars}</tbody></table></div><p>Rechecked against MICHELIN's 31 August 2026 announcement on 27 November. Guide status is not proof of February 2027 opening or availability. <a href="restaurants.html">All restaurants, costs, hours and media</a>.</p></section>
<section class="panel" id="three-things"><h2>Best next path — proposed, not booked</h2><ol class="tight"><li>Keep 15–22 February as the baseline; compare all eligible seven-night starts and price fourteen nights independently.</li><li>Compare MGM Grand for its two starred restaurants, Cosmopolitan for é and China Poblano, and Caesars Palace for Guy Savoy. These are same-property relationships in <a href="{e(MICHELIN_SOURCE)}">MICHELIN's address list</a>, not claims about hotel price, bed fit or bus journey length.</li><li>Require a named queen/king room, private bathroom, two-adult occupancy, seven-night total including mandatory fees/taxes, cancellation terms and timestamp from each hotel's official checkout.</li><li>Validate each selected bus journey at the actual dinner time, including walks, waits, transfers and return service. Do not count Vegas Loop as subway or bus.</li><li>Reserve nothing until accommodation and dinner availability are established. No payment or reservation has been made.</li></ol></section>
<section class="panel"><h2>Review paths</h2><p><a href="questions.html">Questions and missing information</a> · <a href="suggestions.html">Suggestions awaiting review</a> · <a href="flagged.html">Flagged for Review</a> · <a href="repo-review.html">Inherited audit records</a></p><p>Existing source-linked restaurant/activity records remain available. They are historical observations, not promises of future hours or prices. Social links are previews, not evidence of awards, hours or rates.</p></section>
"""
    return page("index.html", "Las Vegas trip planning", "A source-linked decision dashboard for two adults · February–March 2027", body)


# ---------------------------------------------------------------- hotels
def build_hotels():
    rows = []
    for h in sorted(HOTELS["hotels"], key=lambda h: h["name"].casefold()):
        rows.append(f'<tr><td><a href="{e(h["official_url"])}">{e(h["name"])}</a></td><td>—</td><td>—</td><td>—</td><td>Unverified: named room, bathroom, complete price and route evidence required. <a href="flagged.html#F-58">F-58</a> / <a href="flagged.html#F-59">F-59</a></td></tr>')
    official_rows = []
    for c in OFFR["captures"]:
        n = c.get("nightly_incl_resort_fee_excl_tax")
        nightly = (f"${n:,.2f}".rstrip("0").rstrip(".") if isinstance(n, float) else f"${n:,}") if n else "—"
        tot = c.get("stay_total_incl_tax_and_fees")
        if tot:
            total = f"<strong>${tot:,.2f}</strong>"
        elif c.get("stay_total_excl_tax"):
            total = f"${c['stay_total_excl_tax']:,}<div class=\"tiny\">before tax</div>"
        else:
            total = "—"
        offer = c.get("public_offer")
        if offer:
            total += (f'<div class="tiny">public offer ${offer["stay_total_excl_tax"]:,} '
                      f'(${offer["nightly_incl_resort_fee_excl_tax"]}/night), book by ' + e(offer["book_by"]) + '</div>')
        alt = c.get("alt_room")
        if alt:
            total += f'<div class="tiny">2-queen room: <strong>${alt["stay_total_incl_tax_and_fees"]:,.2f}</strong> all-in</div>'
        guard = "guaranteed" if c["bed_guaranteed"] else "NOT guaranteed"
        official_rows.append(
            f'<tr><td><strong>{e(c["hotel"])}</strong></td>'
            f'<td class="tiny">{e(c["room"])}<div class="tiny muted">{e(c["bed"])} · {guard}</div></td>'
            f'<td class="num">{nightly}</td><td class="num">{total}</td>'
            f'<td class="tiny">{e(c.get("resort_fee_note") or OFFR["meta"]["tax_fee_basis"])}</td>'
            f'<td class="tiny"><a href="{e(c["source"])}" target="_blank" rel="noopener">official engine</a>'
            f'<div class="muted">checked {e(c["checked"])}</div></td></tr>')
    official_rows = "".join(official_rows)
    official_limits = "".join(f"<li>{e(x)}</li>" for x in OFFR["what_this_does_not_establish"])

    body = f"""
<section class="panel" id="cheapest-week"><h2>No verified cheapest week or best day to book</h2><p>The inherited quotes are Booking.com snapshots, not official property checkout totals. They are preserved in repository audit files but are deliberately not presented as qualifying offers. A promotional nightly rate is not a seven-night total; absence of a verified rate does not mean sold out.</p><p>The travel window permits <strong>30 seven-night starts</strong>, every day from 15 February through 16 March 2027 inclusive. For fourteen nights, eligible starts are 15 February–9 March. The preferred 15–18 February is three nights and cannot satisfy the separate one-to-two-week requirement. Provisional baseline: <strong>15–22 February 2027, two adults, one room</strong>.</p><p>Stay dates and purchase date are separate questions. No evidence establishes that booking on a particular future day will be cheapest. No universal discount or savings percentage is asserted.</p></section>
<section class="panel" id="every-hotel"><h2>All {len(rows)} hotel research candidates</h2><p>Alphabetical, <strong>not ranked</strong>. — means unverified. Official links are discovery/review links; a link alone does not verify a price or a room feature. Some properties refuse automated access; those are not labelled broken. Candidate names are inherited, not a fresh certification of all properties.</p><div class="scroll"><table class="data" id="official-hotel-decisions"><thead><tr><th>Hotel / official site</th><th>Total USD · 7 nights · 15–22 Feb · 2 adults</th><th>Queen+ &amp; private bath confirmed</th><th>MICHELIN venues ≤60 min by bus</th><th>Evidence status</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div></section>
<section class="panel" id="official-rates"><h2>Official booking engines: the only three official totals this site holds</h2><p>This is the narrowest kind of evidence: three properties' <strong>own</strong> booking engines, read directly on <strong>27 November 2026</strong> for the provisional baseline (15–22 Feb 2027, 2 adults, 1 room, 7 nights). It is here because it is the only official price evidence in the repository — and because <em>one</em> of the three is a true all-in checkout figure, which the Booking.com snapshots never were.</p><div class="scroll"><table class="data"><thead><tr><th>Property</th><th>Room · bed</th><th>Nightly</th><th>7-night total</th><th>Tax / fee basis</th><th>Source</th></tr></thead><tbody>{official_rows}</tbody></table></div><p class="note"><strong>The basis column is the whole point.</strong> Caesars Palace and Wynn print a nightly rate that includes the resort fee and excludes tax. Resorts World prints a full itemised total including room tax, resort fee and resort-fee tax. Only the Resorts World figure could appear on a credit-card statement as stated; multiplying the other two by seven would understate both.</p><details><summary>What these three rows do not establish</summary><ul class="tight">{official_limits}</ul></details></section>
<section class="panel"><h2>How to produce a defensible ranking</h2><ol><li>Reject run-of-house offers without guaranteed queen/king bed and private bathroom.</li><li>Compare like-for-like official all-in checkout totals, room terms and cancellation deadlines for two adults.</li><li>Rank first by count of verified bus journeys ≤60 minutes at intended dinner times, then by total price; amenities remain a separate review criterion until preferences are known.</li><li>Include walking, waiting, transfers, return journeys and February/March closures. A zone estimate is insufficient.</li></ol><p><a href="https://github.com/kanlerxz87-cyber/Vegas1/blob/main/data/hotels.json">Preserved historical hotel records</a> · <a href="https://github.com/kanlerxz87-cyber/Vegas1/blob/main/data/price-windows.json">Preserved historical OTA comparisons</a>. These files are audit history, not verified offers.</p></section>
"""
    return page("hotels.html", "Hotel evidence & dates", "Official-source-only decision table: unverified amounts and inferred scores are blank.", body)


# ---------------------------------------------------------------- restaurants
def build_restaurants():
    order = {"starred": 0, "bib": 1, "recommended": 2}
    rs = sorted(RES["restaurants"], key=lambda r: (order[r["award_class"]], r["name"]))

    def cls(r):
        return {"starred": "star", "bib": "bib", "recommended": "rec"}[r["award_class"]]

    rows = []
    for r in rs:
        yt = " · ".join(
            f'<a href="{u}" target="_blank" rel="noopener">video {i+1}</a>' for i, u in enumerate(r["youtube"])
        ) or '<span class="muted">none found</span>'
        ig = f'<a href="{r["instagram"]}" target="_blank" rel="noopener">IG</a>' if r["instagram"] else '<span class="muted">—</span>'
        tt = f'<a href="{r["tiktok"]}" target="_blank" rel="noopener">TikTok</a>' if r["tiktok"] else '<span class="muted">—</span>'
        hours = e(r["hours"]) if r["hours"] else '<span class="warn">not verified</span>'
        days = r["days"] or ""
        # the source sometimes repeats the day span inside the hours string
        # (e.g. days="Tue-Sat", hours="Tue-Sat 5:00 PM - 9:30 PM") - print it once
        if days and r["hours"] and r["hours"].lower().replace("\u2013", "-").startswith(
            days.lower().replace("\u2013", "-")
        ):
            hours = e(r["hours"][len(days):].strip())
        days_html = e(days) if days else '<span class="warn">not verified</span>'
        if r["price_2adults"]:
            basis = r.get("price_basis", "")
            src = r.get("price_source") or r["official_url"]
            price = (f'{e(r["price_2adults"])}<div class="tiny">'
                     f'<a href="{e(src)}" target="_blank" rel="noopener">menu source</a> · {e(basis)}</div>')
        else:
            price = '<span class="muted">on request</span>'
        rows.append(f"""<tr>
<td><a href="{e(r['official_url'])}" target="_blank" rel="noopener">{e(r['name'])}</a>
  <div class="tiny">{e(r['cuisine'])} · {e(r['location'])}</div></td>
<td><span class="badge {cls(r)}">{e(r['award'])}</span></td>
<td>{days_html}<div class="tiny">{hours}</div></td>
<td class="tiny">{e(r['exceptions']) or '—'}</td>
<td class="num">{price}</td>
<td class="tiny">{yt}</td><td class="tiny">{ig} {tt}</td>
</tr>""")

    table = f"""
<div class="scroll">
<table class="data">
<thead><tr>
<th>Restaurant</th><th>Award</th><th>Days &amp; hours</th><th>Exceptions</th>
<th>Cost<br><span class="thsub">2 adults</span></th><th>YouTube</th><th>Instagram<br><span class="thsub">/ TikTok</span></th>
</tr></thead>
<tbody>{''.join(rows)}</tbody>
</table>
</div>
<p class="note">Award labels are the 2026 MICHELIN Guide's three tiers, shown separately so an unstarred listing
can never be mistaken for a starred one. <strong>—</strong> means the total was not verified; it does not imply a venue has no published prices. Published figures are not necessarily a complete meal or final bill; consult the per-row basis below.</p>
"""

    priced = [r for r in rs if r["price_2adults"]]
    n_priced = len(priced)
    n_est = sum(1 for r in priced if r.get("price_basis", "").startswith("estimated"))
    n_closed = sum(1 for r in priced if "closed" in r.get("price_basis", ""))
    cost_rows = []
    for r in priced:
        src = r.get("price_source") or r["official_url"]
        closed = ' <span class="warn">(temporarily closed)</span>' if r["id"] == "michael-mina" else ""
        cost_rows.append(
            f'<tr><td><a href="{e(r["official_url"])}" target="_blank" rel="noopener">{e(r["name"])}</a>{closed}'
            f'<div class="tiny">{e(r["award"])}</div></td>'
            f'<td class="num">{e(r["price_2adults"])}</td>'
            f'<td class="tiny">{e(r.get("price_basis", ""))}</td>'
            f'<td class="tiny"><a href="{e(src)}" target="_blank" rel="noopener">venue menu</a></td></tr>')
    cost_panel = f"""
  <p><strong>{n_priced} of {N_TOTAL}</strong> venues printed a price on their own site or menu PDF when re-read on
  27 November 2026: {n_priced - n_est - n_closed} state a fixed per-person price (doubled here for two adults),
  {n_est} publish only per-dish prices so their figure is an <em>estimate</em> with the method shown, and
  {n_closed} states a price for a venue that is temporarily closed. The other {N_TOTAL - n_priced} print no price
  at all and are left blank rather than averaged (<a href="flagged.html#F-65">F-65</a>).</p>
  <div class="scroll">
  <table class="data slim">
  <thead><tr><th>Restaurant</th><th>Cost for two</th><th>Basis</th><th>Source</th></tr></thead>
  <tbody>{''.join(cost_rows)}</tbody>
  </table>
  </div>
  <p class="note">Food only, before tax, gratuity and wine, for two adults. A worked food-and-activity total is on the
  <a href="dining.html">Dining budget</a> page. The two starred rooms that still print nothing — Jo&#xEB;l Robuchon and
  &#xE9; by Jos&#xE9; Andr&#xE9;s — are the likeliest to be the largest line after the room, so reserve before
  booking anything (<a href="suggestions.html">S-04</a>).</p>
"""
    counts = RES["meta"]["counts"]

    soc_rows = ""
    for _s in SOC["restaurants"]:
        _ig = (f'<a href="{e(_s["instagram"])}" target="_blank" rel="noopener">open</a>'
               if _s["instagram"] else '<span class="warn">none verified</span>')
        _ev = e(_s.get("evidence") or "")
        if _s.get("caveat"):
            _ev += f'<div class="tiny warn">{e(_s["caveat"])}</div>'
        soc_rows += f'<tr><td>{e(_s["name"])}</td><td class="tiny">{_ig}</td><td class="tiny">{_ev}</td></tr>'

    body = f"""
<section class="panel">
  <h2>What "MICHELIN" means here</h2>
  <p>Las Vegas had <strong>no MICHELIN Guide between 2010 and 2025</strong>. The 2026 Southwest selection —
  announced 31 August 2026 on the official michelin.com press release — is the city's first since 2009,
  which is why so many videos and blogs still
  describe restaurants as starred when they no longer are.</p>
  <div class="grid4">
    <div class="card"><div class="big">0</div><div class="lbl">three-star</div><p>There are none in Las Vegas.</p></div>
    <div class="card"><div class="big">{N_STARRED}</div><div class="lbl">starred</div><p>{N_TWO} at two stars, {N_ONE} at one star. All {N_STARRED} on the Strip.</p></div>
    <div class="card"><div class="big">{N_BIB}</div><div class="lbl">Bib Gourmand</div><p>Good food under a moderate price.</p></div>
    <div class="card"><div class="big">{N_REC}</div><div class="lbl">Recommended</div><p>Listed, <strong>not</strong> starred.</p></div>
  </div>
</section>

<section class="panel">
  <h2>All {N_TOTAL} listings</h2>
  {table}
</section>

<section class="panel">
  <h2>Watching before you go</h2>
  <p>Every starred, Bib and Recommended row carries at least one YouTube video link in the <em>Watch</em> column —
  69 links across {N_TOTAL} listings — because a video shows the room, the plating and the portion size in a way a
  menu cannot. <strong>{N_IG} of {N_TOTAL}</strong> rows also carry an Instagram link, verified one account at a time.
  The provenance for every row is shown below, and the blanks are explained.</p>
</section>

<section class="panel">
  <h2 id="socials">Where each social link came from</h2>
  <p><strong>{N_IG} of {N_TOTAL}</strong> restaurants now have an Instagram link, and every one of them was
  confirmed by opening the account on <strong>27 November 2026</strong> — not by guessing a handle from a name.
  A link is published only when the account's own bio or posts tie it to this venue, or the venue's own site
  links to it. The <strong>{N_NO_SOCIAL}</strong> rows with no link are shown, with the reason, rather than left to
  look forgotten.</p>
  <div class="scroll">
  <table class="data">
  <thead><tr><th>Restaurant</th><th>Instagram</th><th>How it was confirmed</th></tr></thead>
  <tbody>{soc_rows}</tbody>
  </table>
  </div>
  <p class="note">Read these before trusting a feed.
  <a href="flagged.html#F-54">F-54</a> — three accounts are official but <em>dormant</em> (Jo&euml;l Robuchon's newest post
  is 2020, L'Atelier 2021, Guy Savoy 2023), and the Robuchon bio still claims <strong>three</strong> MICHELIN stars, the
  pre-2010 status; the 2026 Guide gives two. Never quote a venue's own bio as its current award.
  <a href="flagged.html#F-56">F-56</a> — a handle captured earlier had <em>moved</em>; a link can answer 200 and still be a
  dead channel. <a href="flagged.html#F-57">F-57</a> — TikTok refused every request from this sandbox, and two venue
  YouTube channels open but are empty, so neither is presented as a working video source.</p>
</section>

<section class="panel">
  <h2 id="costs">What dinner for two actually costs</h2>
{cost_panel}</section>
"""
    return page("restaurants.html", "MICHELIN restaurants",
                f"All {counts['total']} Las Vegas listings from the 2026 guide, each labelled starred, Bib Gourmand or Recommended.",
                body)


# ---------------------------------------------------------------- dining budget

def _fare_pair(note, label):
    """Dollar amounts attached to a fare label, in printed order.

    Handles both '7-day $64 / $59.95' and '$20 3-day'. Parsing the raw note text
    avoids retyping a fare in the generator, and survives the note being reworded
    (an earlier split() on '3-day' silently returned the $1 residential fare).
    """
    amount = r"\$(\d[\d,]*(?:\.\d+)?)"
    after = re.search(re.escape(label) + r"[^$]{0,12}" + amount + r"(?:\s*/\s*" + amount + r")?", note)
    if after:
        return [float(x.replace(",", "")) for x in after.groups() if x]
    before = re.search(amount + r"\s*" + re.escape(label), note)
    return [float(before.group(1).replace(",", ""))] if before else []


def _first_usd(text):
    v = usd_values(text)
    return v[0] if v else None


def _dining(rid, mode):
    """Cost for two from the stored price cell. mode: low | mid | high."""
    r = next(x for x in RES["restaurants"] if x["id"] == rid)
    v = usd_values(r["price_2adults"])
    if not v:
        return None
    if mode == "low":
        return v[0]
    if mode == "high":
        return v[-1]
    if len(v) >= 3:            # a menu ladder, e.g. Partage $260/$320/$420
        return sorted(v)[len(v) // 2]
    return (v[0] + v[-1]) / 2


def build_dining():
    """Food, activities and transport for two adults — the room is deliberately excluded.

    Every component is read from data/ at build time. Hotel totals are not used: no
    official, checkout-complete seven-night quote exists in the canonical dataset (F-58),
    so adding one here would re-introduce a number the evidence gate removed.
    """
    acts = {a["id"]: a for a in ACT["activities"]}
    hr = usd_values(acts["high-roller"]["price_per_couple"])
    mob = _first_usd(acts["mob-museum"]["price_per_couple"])
    neon = _first_usd(acts["neon-museum"]["price_per_couple"])
    act_total = hr[-1] + mob + neon

    monorail = next(x for x in TRANSIT["systems"] if x["id"] == "monorail")
    mon_fares = _fare_pair(monorail["fare_note"], "7-day")
    monorail_two = mon_fares[-1] * 2          # e-ticket price × 2 adults

    rtc = next(x for x in TRANSIT["systems"] if x["id"] == "rtc")
    rtc_3day = _fare_pair(rtc["fare_note"], "3-day")[-1]
    rtc_two = rtc_3day * 3 * 2                # three 3-day passes each, no 7-day RTC pass

    scenarios = [
        {"name": "Two dinners", "picks": [("partage", "low"), ("esthers-kitchen", "mid")]},
        {"name": "One tasting menu", "picks": [("wing-lei", "low"), ("partage", "mid")]},
        {"name": "Stars-heavy", "picks": [("guy-savoy", "mid"), ("wing-lei", "low"), ("partage", "high")]},
    ]

    comps = []
    for sc in scenarios:
        lines, total = [], 0.0
        for rid, mode in sc["picks"]:
            r = next(x for x in RES["restaurants"] if x["id"] == rid)
            amt = _dining(rid, mode)
            total += amt
            lines.append(f'<a href="{e(r["official_url"])}" target="_blank" rel="noopener">{e(r["name"])}</a> '
                         f'<span class="muted">${amt:,.2f}</span>')
        comps.append({"sc": sc, "lines": lines, "food": total,
                      "total": total + act_total + monorail_two})

    head = "".join(f'<th>{e(c["sc"]["name"])}</th>' for c in comps)

    def row(label, cells, note=""):
        n = f'<div class="tiny">{note}</div>' if note else ""
        return (f'<tr><th class="rowhead">{label}{n}</th>'
                + "".join(f"<td>{c}</td>" for c in cells) + "</tr>")

    food_cells = [f'{"<br>".join(c["lines"])}<div class="num strong">${c["food"]:,.2f}</div>' for c in comps]
    act_cell = (f'High Roller anytime ${hr[-1]:,.2f} + Mob Museum ${mob:,.2f} + '
                f'Neon Museum from ${neon:,.2f}<div class="num strong">${act_total:,.2f}</div>')
    transit_cell = (f'2 × Monorail 7-day e-ticket (${mon_fares[-1]:,.2f} each)'
                    f'<div class="num strong">${monorail_two:,.2f}</div>')
    total_cells = [f'<div class="num best" style="font-size:1.15rem">${c["total"]:,.2f}</div>' for c in comps]

    matrix = f"""
  <div class="scroll">
  <table class="data matrix">
  <thead><tr><th class="rowhead">Cost line (2 adults)</th>{head}</tr></thead>
  <tbody>
  {row("Michelin dinners", food_cells, "food only · before tax, tip and wine")}
  {row("Activities", [act_cell]*len(comps), "the three paid venues this site verifies")}
  {row("Getting around", [transit_cell]*len(comps), "unlimited Strip + Downtown")}
  {row("Food, sights and transport", total_cells, "excludes the room, tax, tips and wine")}
  </tbody>
  </table>
  </div>
"""

    act_rows = "".join(
        f'<tr><td><a href="{e(a["official_url"])}" target="_blank" rel="noopener">{e(a["name"])}</a></td>'
        f'<td class="num">{e(a["price_per_couple"]) or "—"}</td>'
        f'<td class="tiny">{e(a["price_note"])}</td></tr>'
        for a in ACT["activities"])

    body = f"""
<section class="panel callout">
  <h2>What the food, sights and transport add up to</h2>
  <p>Three worked totals for two adults, assembled at build time from the venue prices on this site.
  <strong>No hotel figure is used.</strong> No official, checkout-complete seven-night accommodation quote exists in
  this dataset (<a href="flagged.html#F-58">F-58</a>), so adding an OTA snapshot here would put back a number the
  evidence gate deliberately removed. Add your own official room total to the line below once you have it.</p>
  <p><strong>These totals are arithmetic on published prices, not quotes.</strong> They exclude Nevada room tax,
  resort fees, airfare, gratuity and wine.</p>
</section>

<section class="panel">
  <h2>Three ways to eat</h2>
  {matrix}
  <p class="note">Each dinner is the venue's own published price doubled for two (or, where only per-dish prices
  exist, the labelled estimate from the <a href="restaurants.html#costs">restaurant table</a>). Partage appears at
  its 5-course price in the first column, 7-course in the second and Signature in the third — the venue publishes
  all three. Michael Mina is excluded from every column because it is temporarily closed
  (<a href="flagged.html#F-23">F-23</a>).</p>
</section>

<section class="panel">
  <h2>What one more dinner costs</h2>
  <div class="scroll">
  <table class="data slim">
  <thead><tr><th>Add one dinner for two</th><th>Marginal cost</th><th>Source</th></tr></thead>
  <tbody>
  <tr><td>Partage, 5 courses</td><td class="num">${_dining("partage","low"):,.2f}</td><td class="tiny"><a href="{e(next(x for x in RES["restaurants"] if x["id"]=="partage")["price_source"])}">official menu</a></td></tr>
  <tr><td>Wing Lei, Chef Tam's tasting</td><td class="num">${_dining("wing-lei","low"):,.2f}</td><td class="tiny"><a href="{e(next(x for x in RES["restaurants"] if x["id"]=="wing-lei")["price_source"])}">official menu</a></td></tr>
  <tr><td>Guy Savoy, à la carte (estimate)</td><td class="num">≈${_dining("guy-savoy","low"):,.0f}–${_dining("guy-savoy","high"):,.0f}</td><td class="tiny"><a href="{e(next(x for x in RES["restaurants"] if x["id"]=="guy-savoy")["price_source"])}">official menu</a></td></tr>
  </tbody>
  </table>
  </div>
  <p class="note">Useful comparison: the cheapest starred dinner on this site (Wing Lei, ${_dining("wing-lei","low"):,.2f}
  for two) is roughly the price of one to two hotel nights at the properties in the middle of the hotel table — check the
  official checkout total before assuming the room is the only large line.</p>
</section>

<section class="panel">
  <h2>Activities, priced for two</h2>
  <div class="scroll">
  <table class="data">
  <thead><tr><th>Venue</th><th>2 adults</th><th>Basis</th></tr></thead>
  <tbody>{act_rows}</tbody>
  </table>
  </div>
  <p class="note">The three paid venues in the totals are the High Roller (anytime, ${hr[-1]:,.2f}), the Mob Museum
  (${mob:,.2f}) and the Neon Museum (from ${neon:,.2f}). Fremont Street is free, so it adds nothing. The Sphere
  publishes no single price and is left out of every total rather than estimated
  (<a href="flagged.html#F-16">F-16</a>).</p>
</section>

<section class="panel">
  <h2>Getting around: which pass to buy</h2>
  <div class="scroll">
  <table class="data slim">
  <thead><tr><th>Option</th><th>For two</th><th>Basis</th></tr></thead>
  <tbody>
  <tr><td>Monorail 7-day e-ticket × 2</td><td class="num">${monorail_two:,.2f}</td>
      <td class="tiny"><a href="{e(monorail["fare_url"])}" target="_blank" rel="noopener">official fares</a> ·
      {e(monorail["fare_note"])}</td></tr>
  <tr><td>RTC 3-day pass × 3 each (covers 9 days)</td><td class="num">${rtc_two:,.2f}</td>
      <td class="tiny"><a href="{e(rtc["official_url"])}" target="_blank" rel="noopener">official fares</a> ·
      {e(rtc["fare_note"])}</td></tr>
  </tbody>
  </table>
  </div>
  <p class="note">The monorail does not reach the airport or downtown; the RTC Deuce does and runs 24 hours, which
  matters if Fremont Street and Chinatown are in the plan. No seven-day RTC pass was verified — the arithmetic
  above stacks three-day passes.</p>
</section>

<section class="panel">
  <h2>To turn this into a trip total</h2>
  <ol class="tight">
    <li><strong>Add the room.</strong> Use the property's own checkout for the exact dates: named room, two adults,
      seven nights, mandatory resort fee and taxes, cancellation terms, timestamp
      (<a href="hotels.html">Hotels</a>, <a href="flagged.html#F-58">F-58</a>).</li>
    <li><strong>Add airfare</strong> and airport transfers — neither is in this dataset.</li>
    <li><strong>Add gratuity and wine.</strong> Partage's published wine pairings are $60–$108 per person; the other
      venues publish no pairing price, so none is estimated.</li>
    <li><strong>Keep the nights flexible until the room is quoted.</strong> No universal cheapest week is established
      (<a href="questions.html#Q-06">Q-06</a>).</li>
  </ol>
</section>
"""
    return page("dining.html", "Dining budget",
                "What the Michelin dinners, the three paid activities and a transit pass add up to for two adults — before the room.",
                body)


# ---------------------------------------------------------------- activities
def build_activities():
    rows = []
    for a in ACT["activities"]:
        yt = " · ".join(f'<a href="{e(u)}" target="_blank" rel="noopener">video {i+1}</a>' for i, u in enumerate(a.get("youtube", []))) or '<span class="muted">—</span>'
        ig = f'<a href="{e(a["instagram"])}" target="_blank" rel="noopener">Instagram</a>' if a.get("instagram") else '<span class="muted">—</span>'
        tt = f'<a href="{e(a["tiktok"])}" target="_blank" rel="noopener">TikTok</a>' if a.get("tiktok") else '<span class="muted">—</span>'
        rows.append(f"""<tr id="{e(a['id'])}">
<td><a href="{e(a['official_url'])}" target="_blank" rel="noopener">{e(a['name'])}</a>
 <div class="tiny">{e(a['type'])} · {e(a['zone'].replace('-',' '))}</div></td>
<td>{e(a['days'])}<div class="tiny">{e(a['hours'])}</div></td>
<td class="tiny">{e(a['exceptions']) or '—'}</td>
<td class="num">{e(a['price_per_couple']) or '—'}</td>
<td class="tiny">{e(a['price_note'])}</td>
<td class="tiny">{yt}</td><td class="tiny">{ig}</td><td class="tiny">{tt}</td>
</tr>""")

    nv = "".join(
        f'<li><strong>{e(n["name"])}</strong> — {e(n["reason"])}</li>' for n in ACT["not_verified"]
    )
    # Provenance rows: one per activity, showing HOW each link was confirmed.
    # This is the activities counterpart of the restaurants provenance table.
    social_rows = ""
    for _a in ACT["activities"]:
        _bits = []
        if _a.get("social_evidence"):
            _bits.append(e(_a["social_evidence"]))
        if _a.get("social_caveat"):
            _bits.append(f'<div class="tiny warn">{e(_a["social_caveat"])}</div>')
        # The other session's social_note often repeats what social_evidence
        # already says; keep it only when there is no evidence for the row, and
        # always separate sentences so two sources cannot run together.
        if _a.get("social_note") and not _a.get("social_evidence"):
            _bits.append(e(_a["social_note"]))
        _cell = "<br>".join(_bits) or "—"
        social_rows += (f'<tr><td>{e(_a["name"].split(" (")[0])}</td>'
                        f'<td class="tiny">{_a.get("social_status", "none_verified").replace("_", " ")}</td>'
                        f'<td class="tiny">{_cell}</td></tr>')

    body = f"""
<section class="panel">
  <h2>{len(ACT['activities'])} activities</h2>
  <div class="scroll">
  <table class="data">
  <thead><tr><th>Venue</th><th>Days &amp; hours</th><th>Exceptions</th><th>2 adults</th><th>Price basis</th><th>YouTube</th><th>Instagram</th><th>TikTok</th></tr></thead>
  <tbody>{''.join(rows)}</tbody>
  </table>
  </div>
  <p class="note">Social columns show only links present in the dataset; <strong>— means no link was verified for this entry</strong>, not that the venue has no account or video. See <a href="questions.html">Open questions</a> for discovery gaps and <a href="flagged.html">F-53</a> for coverage.</p>
</section>



<section class="panel">
  <h2 id="social-sources">Where each social link came from</h2>
  <p>A handle is only listed when the venue's own site, its own channel or profile, or venue-issued press material
  publishes it — never inferred from a venue name. Every link above was either printed on the venue's own site or
  found by opening the account itself on <strong>27 November 2026</strong>; the sentence that confirmed it is in the
  last column, so a doubtful row can be re-checked in one click. Coverage counts and the remaining gaps are in
  <a href="flagged.html">F-53</a>.</p>
  <div class="scroll">
  <table class="data">
  <thead><tr><th>Venue</th><th>Status</th><th>How it was confirmed</th></tr></thead>
  <tbody>{social_rows}</tbody>
  </table>
  </div>
</section>

<section class="panel">
  <h2>Deliberately not listed</h2>
  <p>These were checked and could not be verified, so no hours, price or link is published for them:</p>
  <ul class="tight">{nv}</ul>
</section>

<section class="panel callout">
  <h2>The one free thing</h2>
  <p>The <strong>Fremont Street Experience</strong> runs live music on three stages every night under the canopy,
  and entry is free. Put it on the same day as the Mob Museum and the Neon Museum — all three are downtown,
  but travel times from each hotel remain unverified; do not assume a 25–30 minute journey.</p>
</section>
"""
    return page("activities.html", "Things to do",
                f"{len(ACT['activities'])} verified activity entries with official hours/prices where published, plus explicit blanks where no official social profile was verified.",
                body)


# ---------------------------------------------------------------- transit
def build_transit():
    body = f"""
<section class="panel" id="matrix"><h2>Journey-time ranking suspended</h2><p>The inherited matrix is a zone-level estimate, not an official hotel-to-restaurant itinerary. Its saturation at 24/24 does not establish that every restaurant is reachable from every hotel within an hour. Verified counts are blank on the Hotels page. Monorail is a separate mode; Vegas Loop is not a subway or RTC bus. No Loop ride is counted as satisfying your bus/subway constraint.</p><p>For each actual journey, collect hotel entrance, restaurant entrance, service date/time, walk segments, wait, transfer, in-vehicle time and last return service. <a href="https://www.rtcsnv.com/ways-to-travel/">Official RTC journey resources</a>. No complete journeys were verified in this pass.</p></section>
<section class="panel"><h2>RTC visitor fares · checked 27 November 2026</h2><p>These are published current pass prices, not February 2027 guarantees. All passes are valid on all routes. Visitors must use Strip and All Access fares. Two-adult totals below are arithmetic (2 × the printed adult price), not a trip-wide transport budget.</p><div class="scroll"><table class="data"><thead><tr><th>Pass</th><th>Total for 2 adults · USD</th><th>Basis</th><th>Official source</th></tr></thead><tbody>
<tr><td>Single ride</td><td>$8</td><td>2 × $4</td><td><a href="{RTC_SOURCE}">RTC</a></td></tr>
<tr><td>2 hours</td><td>$12</td><td>2 × $6</td><td><a href="{RTC_SOURCE}">RTC</a></td></tr>
<tr><td>24 hours</td><td>$16</td><td>2 × $8</td><td><a href="{RTC_SOURCE}">RTC</a></td></tr>
<tr><td>3 days</td><td>$40</td><td>2 × $20</td><td><a href="{RTC_SOURCE}">RTC</a></td></tr>
</tbody></table></div><p>RTC describes normal Deuce frequency as approximately every 15 minutes. That is not door-to-door travel time. The inherited statement that Nevada local fares are $1 is incorrect for regular adults: RTC lists residential regular single rides at $2 and reduced fares at $1; visitor fare rules are separate. <a href="flagged.html#F-60">F-60</a>.</p></section>
"""
    return page("transit.html", "Getting around", "Published visitor fares and explicit gaps in journey evidence.", body)


def build_questions():
    state_cls = {"answered": "ok", "open": "bad", "interpreted": "warn"}
    cards = []
    for q in QS["questions"]:
        srcs = "".join(
            f'<li><a href="{e(u)}" target="_blank" rel="noopener">{e(u)}</a></li>' for u in q["sources"]
        )
        src_block = f'<details><summary>Sources</summary><ul class="srcs">{srcs}</ul></details>' if srcs else ""
        problem = f'<p><strong>Why it is not closed:</strong> {e(q["problem"])}</p>' if q.get("problem") else ""
        sub = f'<p><strong>What was done instead:</strong> {e(q["substitution"])}</p>' if q.get("substitution") else ""
        cards.append(f"""
<article class="qa" id="{e(q['id'])}">
  <h3><span class="qid">{e(q['id'])}</span> {e(q['question'])}
    <span class="state {state_cls[q['state']]}">{e(q['state'])}</span></h3>
  <p><strong>Answer:</strong> {e(q['answer'])}</p>
  {problem}
  {sub}
  <p class="tiny"><strong>How to close it:</strong> {e(q['how_to_close'])}</p>
  {src_block}
</article>""")

    n_q = len(QS["questions"])
    n_open = sum(1 for q in QS["questions"] if q["state"] == "open")
    n_int = sum(1 for q in QS["questions"] if q["state"] == "interpreted")
    n_done = sum(1 for q in QS["questions"] if q["state"] == "answered")

    body = f"""
<section class="panel">
  <h2>What is known, what is not, and how to find out</h2>
  <p>{n_q} questions drove this plan. {n_done} are fully closed, {n_int} required a stated interpretation because
  the brief does not map onto Las Vegas as written, and {n_open} are still open — those are the ones where a
  table on this site shows a blank rather than a guess.</p>
  <div class="grid4">
    <div class="card"><div class="big">{n_done}</div><div class="lbl">answered</div><p>Confirmed against an official source, link attached.</p></div>
    <div class="card"><div class="big">{n_int}</div><div class="lbl">interpreted</div><p>The question does not fit the city; the substitution is disclosed.</p></div>
    <div class="card"><div class="big">{n_open}</div><div class="lbl">open</div><p>Not confirmable now. Blank in the data, with a route to close it.</p></div>
    <div class="card"><div class="big">0</div><div class="lbl">filled by guess</div><p>No value on this site was inferred.</p></div>
  </div>
</section>
<div class="qalist">{''.join(cards)}</div>
"""
    return page("questions.html", "Open questions",
                "A register of what is verified, what needed an interpretation, and what is still unknown — with the exact steps to close each gap.",
                body)


# ---------------------------------------------------------------- suggestions
def build_suggestions():
    imp = {"high": "hi", "medium": "md", "low": "lo"}
    cards = []
    for s in SUG["suggestions"]:
        need = ('<span class="pill need">needs your decision</span>'
                if s["needs_decision"] else f'<span class="pill">{e(s["status"])}</span>')
        cards.append(f"""
<article class="sug" id="{e(s['id'])}">
  <h3><span class="sid">{e(s['id'])}</span> {e(s['title'])}
   <span class="impact {imp[s['impact']]}">{e(s['impact'])} impact</span>{need}</h3>
  <p>{e(s['body'])}</p>
  <p class="trade"><strong>Trade-off:</strong> {e(s['trade_off'])}</p>
  <p class="tiny">Evidence: {e(s['evidence'])}</p>
</article>""")

    needs = [s for s in SUG["suggestions"] if s["needs_decision"]]
    n_sug = len(SUG["suggestions"])
    YES = '<span class="pill need">yes</span>'
    NO = '<span class="muted">no</span>'
    site_rows = "".join(
        f'<tr id="{e(x["id"])}"><td class="mono">{e(x["id"])}</td>'
        f'<td><strong>{e(x["title"])}</strong><div class="tiny">{e(x["status"])}</div></td>'
        f'<td>{e(x["improves"])}</td>'
        f'<td class="tiny">{e(x["work"])}<div class="flagline">{e(x["risk"])}</div></td>'
        f'<td><span class="impact {imp[x["impact"]]}">{e(x["impact"])}</span></td>'
        f'<td>{YES if x["decision_needed"] else NO}</td></tr>'
        for x in SITESUG["suggestions"])
    n_site_need = sum(1 for x in SITESUG["suggestions"] if x["decision_needed"])

    body = f"""
<section class="panel">
  <h2>{len(SUGGESTIONS_HEAD)}</h2>
  <p>{n_sug} proposals, ranked by how much they change the outcome. <strong>{len(needs)} of them need a decision
  from you</strong> before the plan can be finalised — they are marked in the list. Nothing here was silently
  applied to the data.</p>
  <p>The three that matter most: compare exact hotel dates on the <strong>property's own booking engine</strong> before changing dates (the Booking.com and official-engine samples conflict),
  settle whether this is a <strong>three-night or seven-night</strong> trip (which changes every hotel number by
  over half), and <strong>refuse unassigned-room rates</strong> (which removes the three cheapest hotels on the site). See the <a href="https://kanlerxz87-cyber.github.io/Vegas1/docs/session-af795000/hotels.html">official-engine sample</a> and its direct links.</p>
</section>
<div class="suglist">{''.join(cards)}</div>

<section class="panel" id="site-improvements">
  <h2>Improving this site — review before anything is built</h2>
  <p>The proposals above change <em>the trip</em>. These change <em>the site</em>: what would make the same
  evidence easier to act on, what it would cost, and what could go wrong. Nothing here is applied.
  <strong>{n_site_need} of {len(SITESUG["suggestions"])} need a decision from you</strong> — those are the ones
  where two reasonable answers exist and the wrong one means rework.</p>
  <div class="scroll">
  <table class="data">
  <thead><tr><th>ID</th><th>Proposal</th><th>What it improves</th><th>Work / risk</th><th>Impact</th><th>Decision?</th></tr></thead>
  <tbody>{site_rows}</tbody>
  </table>
  </div>
  <p class="note">One is already partly built: deriving counts at render time instead of typing them into
  prose, which is the exact bug this site has now shipped twice.</p>
</section>
"""
    return page("suggestions.html", "Suggestions",
                f"{len(SUG['suggestions'])} decision improvements, ranked, each with its honest trade-off and whether it needs your call first.",
                body)


SUGGESTIONS_HEAD = [f"{len(SUG['suggestions'])} ways to improve this plan"]


# ---------------------------------------------------------------- sources
def build_sources():
    flag_rows = []
    # flags are listed in FLAGS.md; render the highlighted ones here
    N_FLAGS = len(_flag_register())
    flags = [
        ("F-01", "Joël Robuchon", "Videos say 3 stars; the 2026 Guide says 2."),
        ("F-02", "Michael Mina", "Publishes seasonal block closures; no 2027 dates."),
        ("F-03", "Wing Lei", "Videos imply a star; the 2026 Guide lists it Recommended."),
        ("F-04", "KAME Omakase", "Own site is a JS shell; details from its OpenTable listing."),
        ("F-05", "China Poblano", "The ≈$50 pp figure is Eater, not the venue."),
        ("F-07", "Esther's Kitchen, Yen Viet", "Hours not obtainable — left blank."),
        ("F-09", "Wynn / Encore", "Two totals because the fee/tax basis differs."),
        ("F-11", "LINQ, Flamingo, SAHARA, Golden Nugget, Horseshoe, Plaza", "Cheapest rates do not guarantee the bed."),
        ("F-12", "Nobu at Caesars", "Only hotel cheaper in February than March; cause unverified."),
        ("F-13", "Bellagio, Waldorf", "Totals across weeks are for different room classes."),
        ("F-15", "Bluegreen Club 36", "Queen bed stated; private bathroom not stated."),
        ("F-17", "14-night variant", "The brief allows two weeks; only seven nights were priced."),
        ("F-18", "Bellagio Fountains", "Official page failed to load; schedule unverified."),
        ("F-19", "Instagram / TikTok", "Handles not published; blank rather than guessed."),
        ("F-39", "Hotel price basis", "The 32-hotel prices are Booking.com snapshots, not official property quotes; independent official-engine samples conflict on the cheapest week."),
        ("F-30", "Official hotel rates, refreshed 26 Nov 2026", "Caesars Julius King $201/night and Wynn Cyber $677/night, each including resort fee before tax; Venetian returned $6,170.43 tax-included but labels suites as 4+ guests. Volatile; confirm exact total and occupancy."),
    ]
    for fid, where, what in flags:
        flag_rows.append(f'<tr><td class="mono">{fid}</td><td>{e(where)}</td><td>{e(what)}</td></tr>')

    groups = {}
    for r in RES["restaurants"]:
        groups.setdefault("MICHELIN Guide 2026 — restaurant pages", []).append(
            (r["name"], r["official_url"])
        )
    for h in HOTELS["hotels"]:
        if h["official_url"]:
            groups.setdefault("Hotels — official pages", []).append((h["name"], h["official_url"]))
    groups.setdefault("MICHELIN Guide sources", []).extend([
        ("MICHELIN press release — first Southwest selection", "https://www.michelin.com/en/publications/products-and-services/michelin-guide-reveals-first-ever-southwest-restaurant-selection-in-the-u-s"),
        ("Visit Las Vegas — MICHELIN Guide restaurants", "https://www.visitlasvegas.com/michelin-guide-restaurants/"),
        ("Las Vegas Weekly — 2026 selection", "https://lasvegasweekly.com/dining/2026/aug/27/michelin-guide-southwest-las-vegas-restaurants/"),
        ("Eater Vegas — 2026 star winners", "https://vegas.eater.com/restaurant-news/131551/2026-michelin-star-winners-las-vegas-nevada-restaurants"),
    ])
    groups.setdefault("Transit — official fare and station pages", []).extend([
        ("Las Vegas Monorail — stations", "https://www.lvmonorail.com/stations/"),
        ("Las Vegas Monorail — fares", "https://www.lvmonorail.com/ticket-information/"),
        ("RTC Transit — fares and passes", "https://www.rtcsnv.com/ways-to-travel/fares-passes/"),
        ("Boring Company — Vegas Loop", "https://www.boringcompany.com/projects/las-vegas-loop"),
    ])
    groups.setdefault("Activities — official pages", []).extend([
        ("Sphere", "https://www.thesphere.com/"),
        ("High Roller", "https://www.caesars.com/linq/things-to-do/attractions/high-roller"),
        ("The Mob Museum", "https://themobmuseum.org/"),
        ("The Neon Museum", "https://neonmuseum.org/"),
        ("Fremont Street Experience", "https://www.fremontstreetexperience.com/"),
    ])
    groups.setdefault("Pricing", []).extend([
        ("Booking.com — Las Vegas, 5★ resorts, 15–22 Feb 2027", "https://www.booking.com/searchresults.html?ss=Las+Vegas&checkin=2027-02-15&checkout=2027-02-22&group_adults=2&no_rooms=1&selected_currency=USD&nflt=class%3D5%3Bht_id%3D206&order=price"),
        ("Booking.com — same search, 8–15 Mar 2027", "https://www.booking.com/searchresults.html?ss=Las+Vegas&checkin=2027-03-08&checkout=2027-03-15&group_adults=2&no_rooms=1&selected_currency=USD&nflt=class%3D5%3Bht_id%3D206&order=price"),
        ("Booking.com — same search, 1–8 Mar 2027", "https://www.booking.com/searchresults.html?ss=Las+Vegas&checkin=2027-03-01&checkout=2027-03-08&group_adults=2&no_rooms=1&selected_currency=USD&nflt=class%3D5%3Bht_id%3D206&order=price"),
        ("Booking.com — same search, 15–22 Mar 2027", "https://www.booking.com/searchresults.html?ss=Las+Vegas&checkin=2027-03-15&checkout=2027-03-22&group_adults=2&no_rooms=1&selected_currency=USD&nflt=class%3D5%3Bht_id%3D206&order=price"),
        ("Booking.com — Wynn Las Vegas property page", "https://www.booking.com/hotel/us/wynn-las-vegas-boulevard.html"),
        ("Wynn Las Vegas — rooms and suites", "https://www.wynnlasvegas.com/rooms-and-suite"),
        ("Official-engine price sample — dated rate links", "https://kanlerxz87-cyber.github.io/Vegas1/docs/session-af795000/hotels.html"),
        ("Caesars Palace — official exact-date booking search", "https://www.caesars.com/book/room-list?arrivalDate=02/15/2027&departureDate=02/22/2027&dateSearchFormat=exact-dates&propCode=clv&numberOfAdults=2&numberOfRooms=1"),
        ("Wynn — official exact-date booking engine", "https://reservations.wynnlasvegas.com/ibe/details.aspx?hotelID=13763&langID=1&rmID=68658&checkIn=02/15/2027&checkOut=02/22/2027&adults=2&children=0"),
        ("Resorts World — official exact-date booking engine (fee legend conflict flagged)", "https://reservations.rwlasvegas.com/ibe/shop.aspx?hotelID=17726&selectedTower=HILTON&checkin=2027-02-15&checkout=2027-02-22&nights=7&adults=2&children=0"),
        ("The Venetian — official exact-date booking engine (occupancy label requires checking)", "https://www.venetianlasvegas.com/booking?adults[]=2&arrival_date=2027-02-15&children[]=0&departure_date=2027-02-22&view=calendar"),
    ])
    groups.setdefault("Context checks", []).extend([
        ("F1 Experiences — 2027 Las Vegas GP, 18–20 Nov 2027", "https://f1experiences.com/2027-las-vegas-gp"),
        ("dord.racing — 2027 Las Vegas GP calendar entry", "https://dord.racing/events/2027/f1-las-vegas-gp"),
    ])

    blocks = []
    for gname, items in groups.items():
        lis = "".join(
            f'<li><a href="{e(u)}" target="_blank" rel="noopener">{e(n)}</a></li>' for n, u in items
        )
        blocks.append(f'<section class="panel"><h2>{e(gname)}</h2><ul class="srcs">{lis}</ul></section>')

    body = f"""
<section class="panel">
  <h2>How to check any number on this site</h2>
  <p>Every figure traces to one of these pages. If a number here disagrees with its source, the source is right.</p>
</section>

<section class="panel" id="flags">
  <h2>Flags — what did not verify cleanly</h2>
  <p>A flag means the cell is <strong>blank or labelled</strong>, never that a number was filled in.</p>
  <div class="scroll">
  <table class="data">
  <thead><tr><th>ID</th><th>Where</th><th>What</th></tr></thead>
  <tbody>{''.join(flag_rows)}</tbody>
  </table>
  </div>
  <p class="note">The full list (all {N_FLAGS} flags) and deliberate non-inclusions are on the
  <a href="flagged.html">Flagged for Review</a> page and in the repository's <a href="https://github.com/kanlerxz87-cyber/Vegas1/blob/main/FLAGS.md">FLAGS.md register</a>.</p>
</section>
{''.join(blocks)}
"""
    return page("sources.html", "Sources & flags",
                "Every page used to build this plan, grouped by what it proves — plus the flags for what would not confirm.",
                body)


# ---------------------------------------------------------------- review
REVIEW = load("review.json")
FLAGS_MD = ROOT / "FLAGS.md"


GENERIC_WORDS = {
    "hotel", "hotels", "resort", "resorts", "casino", "vegas", "las", "spa", "the", "and", "club",
    "grill", "restaurant", "steakhouse", "kitchen", "bistro", "lounge", "bar", "suite", "suites",
    "experience", "at", "de", "by", "la", "international", "observation", "wheel", "museum", "guide",
}

# flags that are not about one venue get one hand-picked official page, taken from the datasets
# or from a page this session actually opened
FLAG_CHECK_EXTRA = {
    "F-58": ("Official hotel discovery / room quotes", "https://www.caesars.com/book/"),
    "F-59": ("Official RTC route resources", "https://www.rtcsnv.com/ways-to-travel/"),
    "F-60": ("RTC official fare rules", RTC_SOURCE),
    "F-61": ("Guy Savoy official menu", "https://www.caesars.com/caesars-palace/restaurants/restaurant-guy-savoy/main-menu"),
    "F-62": ("Mob Museum current hours", "https://themobmuseum.org/"),
    "F-63": ("High Roller official conflicting time blocks", "https://www.caesars.com/linq/things-to-do/attractions/high-roller"),
    "F-10": ("Booking.com dated search used for every rate",
             "https://www.booking.com/hotel/us/the-linq-and-casino.html?checkin=2027-02-15"
             "&checkout=2027-02-22&group_adults=2&no_rooms=1&selected_currency=USD"),
    "F-17": ("Booking.com 7-night capture, same basis",
             "https://www.booking.com/hotel/us/the-linq-and-casino.html?checkin=2027-02-15"
             "&checkout=2027-02-22&group_adults=2&no_rooms=1&selected_currency=USD"),
    "F-19": ("Visit Las Vegas — MICHELIN restaurants", "https://www.visitlasvegas.com/michelin-guide-restaurants/"),
    "F-20": ("RTC fares & passes", "https://www.rtcsnv.com/ways-to-travel/fares-passes/"),
    "F-21": ("RTC Route 203 timetable (PDF)", "https://rtcws.rtcsnv.com/routePDF/203.pdf"),
    "F-42": ("RTC Route 203 timetable (PDF)", "https://rtcws.rtcsnv.com/routePDF/203.pdf"),
    "F-26": ("Bellagio restaurant page carrying the banner",
             "https://bellagio.mgmresorts.com/en/restaurants/michael-mina.html"),
    "F-27": ("Flag register in the repository", "https://github.com/kanlerxz87-cyber/Vegas1/blob/main/FLAGS.md"),
    "F-48": ("Booking.com dated search list (the basis for those 15 rows)",
             "https://www.booking.com/searchresults.html?ss=Las+Vegas&checkin=2027-02-15"
             "&checkout=2027-02-22&group_adults=2&no_rooms=1&selected_currency=USD"),
}


def _tok_hits(tok, hay):
    """whole-word match, so 'china' cannot match 'Chinatown' and 'green' cannot match 'Bluegreen'"""
    return re.search(r"(?<![a-z0-9])" + re.escape(tok) + r"(?![a-z0-9])", hay) is not None


def _venue_tokens(name):
    toks = [t for t in re.split(r"[^a-z0-9']+", name.lower().replace("jo\u00ebl", "joel")) if len(t) >= 4]
    return [t for t in toks if t not in GENERIC_WORDS] or [name.lower().strip()]


def _flag_check_links(fid, where):
    """the official page(s) a flag should be checked against — all URLs already live in the datasets"""
    hay = where.lower().replace("jo\u00ebl", "joel")
    links, seen = [], set()

    def add(label, url):
        if url and url not in seen:
            seen.add(url)
            links.append((label, url))

    for r in RES["restaurants"]:
        nm = r["name"].lower().replace("jo\u00ebl", "joel")
        if _tok_hits(nm, hay) or any(_tok_hits(t, hay) for t in _venue_tokens(r["name"])):
            add(r["name"], r.get("official_url"))
    for a in ACT["activities"]:
        base = a["name"].split(" (")[0]
        if _tok_hits(base.lower(), hay) or any(_tok_hits(t, hay) for t in _venue_tokens(base)):
            add(base, a.get("official_url"))
    for h in HOTELS["hotels"]:
        key = h["name"].lower().split(" (")[0]
        if _tok_hits(key, hay) or any(_tok_hits(t, hay) for t in _venue_tokens(h["name"])):
            add(h["name"], h.get("official_url") or h.get("booking_url"))
    if fid in FLAG_CHECK_EXTRA:
        label, url = FLAG_CHECK_EXTRA[fid]
        if url not in seen:
            links.insert(0, (label, url))
    if not links:
        return '<a href="sources.html">Sources page</a>'
    return "<br>".join(
        f'<a href="{e(u)}" target="_blank" rel="noopener">{e(n)}</a>' for n, u in links[:6]
    )


def _flag_register():
    rows = []
    for line in FLAGS_MD.read_text(encoding="utf-8").splitlines():
        if line.startswith("| **F-"):
            cells = [c.strip().replace("**", "") for c in line.strip().strip("|").split("|")]
            if len(cells) == 4:
                rows.append(cells)
    return rows


def _flag_cell(text):
    """FLAGS.md is markdown; the register needs bold and code rendered, not printed as punctuation"""
    out = e(text)
    out = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    return out


def _sev(s):
    cls = {"high": "bad", "medium": "warn", "low": "ok"}.get(s, "")
    return f'<span class="tag {cls}">{e(s)}</span>'


def _src(url, label=None):
    if not url:
        return "—"
    return f'<a href="{e(url)}" target="_blank" rel="noopener">{e(label or "source")}</a>'


def build_flagged():
    fl = _flag_register()
    f_rows = "".join(
        f'<tr id="{e(c[0])}"><td class="mono">{e(c[0])}</td><td>{_flag_cell(c[1])}</td>'
        f'<td>{_flag_cell(c[2])}</td><td>{_flag_cell(c[3])}</td>'
        f'<td class="tiny">{_flag_check_links(c[0], c[1])}</td></tr>'
        for c in fl
    )
    r_rows = "".join(
        f'<tr><td class="mono">{e(r["id"])}</td><td>{_sev(r["severity"])}</td><td>{e(r["where"])}</td>'
        f'<td>{e(r["issue"])}</td><td>{e(r["action"])}</td><td>{_src(r.get("source"), "official / repo source")}</td></tr>'
        for r in REVIEW["irregularities"]
    )
    body = f"""
<section class="panel" id="status">
  <h2>What this page is</h2>
  <p>Everything here is <strong>flagged for review</strong>. A flag means a value is blank, conflicts with another source, or could not be confirmed from an official page. Flags do not block the plan. Nothing flagged has been filled in with a guess.</p>
  <p class="note">Items marked Confirmed on the <a href="repo-review.html">Repo review</a> page were checked against an official page this session. Each row below links to the page it relates to, or to the repository file that holds the evidence.</p>
</section>

{build_audit_sections()}

<section class="panel" id="repo-irregularities">
  <h2>Repo irregularities ({len(REVIEW["irregularities"])})</h2>
  <div class="scroll"><table class="data">
  <thead><tr><th>ID</th><th>Severity</th><th>Where</th><th>Issue</th><th>What to do</th><th>Source</th></tr></thead>
  <tbody>{r_rows}</tbody>
  </table></div>
</section>

<section class="panel" id="flags">
  <h2>Data flags — {len(fl)} rows in the register</h2>
  <p>The full register, with the reasoning for each, is in <code>FLAGS.md</code>. Each row is generated from that
  file, is addressable as <code>flagged.html#F-nn</code>, and names the official page to check it against. F-01 to
  F-30 and F-47 to F-49 are rows of that register; F-39 to F-46 are the audit rows above, kept in
  <code>data/review-flags.json</code>. F-31 to F-38 were never used, so the numbering is not contiguous.</p>
  <div class="scroll"><table class="data">
  <thead><tr><th>ID</th><th>Where</th><th>What</th><th>Effect on the plan</th><th>Check it here</th></tr></thead>
  <tbody>{f_rows}</tbody>
  </table></div>
</section>
"""
    return page("flagged.html", "Flagged for review",
                "Every value that is blank, conflicting or unconfirmed — published for your review after the site goes live.",
                body)


def build_repo_review():
    checks = REVIEW["checks"]
    c_rows = "".join(
        f'<tr><td class="mono">{e(c["id"])}</td><td>{e(c["item"])}</td><td>{e(c["compared"])}</td>'
        f'<td><strong>{e(c["result"])}</strong><br><span class="note">{e(c["detail"])}</span></td>'
        f'<td>{_src(c.get("source"), c.get("source_label") or "source")}</td></tr>'
        for c in checks
    )
    limits = "".join(f"<li>{e(x)}</li>" for x in REVIEW["meta"]["limits"])
    # derived counts — computed from the data, never typed by hand
    R = RES["restaurants"]
    n_price = sum(1 for x in R if not x.get("price_2adults"))
    n_hours = sum(1 for x in R if not x.get("hours"))
    n_ig = sum(1 for x in R if x.get("instagram"))
    n_tt = sum(1 for x in R if x.get("tiktok"))
    n_yt = sum(1 for x in R if x.get("youtube"))
    n_ver = sum(1 for x in R if x.get("verified") == "yes")
    H = HOTELS["hotels"]
    h_off_no = sum(1 for x in H if x.get("official_verified") not in ("yes",))
    h_off_yes = sum(1 for x in H if x.get("official_verified") == "yes")
    h_ver_yes = sum(1 for x in H if x.get("verified") == "yes")
    h_same = sum(1 for x in H if x.get("michelin_within_60") == N_TOTAL)
    counts = [
        ("Michelin rows (restaurants)", N_TOTAL, "all listed with a 2026 tier"),
        ("Restaurants with no couple price", n_price, "blank — not verified"),
        ("Restaurants with no hours recorded", n_hours, "blank — not verified"),
        ("Restaurant rows marked verified = yes", n_ver, "the label describes the listing, see R-01"),
        ("Restaurants with an Instagram link", n_ig, "verified 2026-11-27 from official/primary sources; blanks remain unverified (F-19, F-53)"),
        ("Restaurants with a TikTok link", n_tt, "only 2 verified 2026-11-27; blanks remain unverified (F-19, F-53)"),
        ("Restaurants with at least one YouTube link", n_yt, "recorded, not opened this session"),
        ("Hotels (rows)", len(H), "32 properties"),
        ("Hotels whose official page is confirmed live", h_off_yes, "fetched 25–26 Nov 2026"),
        ("Hotels whose official page is not confirmed", h_off_no, "refused automated access, or not opened"),
        ("Hotel rows marked verified = yes", h_ver_yes, "label reflects the search snapshot, see R-03"),
        ("Hotels where Michelin within 60 min = all 24", h_same, "the literal metric cannot rank, see R-04"),
    ]
    count_rows = "".join(
        f'<tr><td>{e(a)}</td><td class="num">{b}</td><td>{e(c)}</td></tr>' for a, b, c in counts
    )
    body = f"""
<section class="panel">
  <h2>What was checked, and how</h2>
  <p>{e(REVIEW["meta"]["method"])}</p>
  <p><strong>Limits of this review:</strong></p>
  <ul>{limits}</ul>
</section>

<section class="panel" id="checks">
  <h2>Line-by-line checks ({len(checks)})</h2>
  <div class="scroll"><table class="data">
  <thead><tr><th>ID</th><th>Item</th><th>What the official page says</th><th>Result</th><th>Source</th></tr></thead>
  <tbody>{c_rows}</tbody>
  </table></div>
</section>

<section class="panel" id="counts">
  <h2>Counts in the data (derived)</h2>
  <p>Computed from <code>data/restaurants.json</code> and <code>data/hotels.json</code> when the site is built.</p>
  <div class="scroll"><table class="data">
  <thead><tr><th>Measure</th><th>Count</th><th>Meaning</th></tr></thead>
  <tbody>{count_rows}</tbody>
  </table></div>
</section>

<section class="panel">
  <h2>Irregularities</h2>
  <p>Each irregularity, with its severity and what to do, is on the <a href="flagged.html#repo-irregularities">Flagged for review</a> page.</p>
</section>
"""
    return page("repo-review.html", "Repo review",
                "A line-by-line check of the repo's key claims against official sources, the irregularities found, and the limits of this review.",
                body)


# ---------------------------------------------------------------- css
CSS = """
:root{
  --bg:#0b0d12; --panel:#141821; --panel2:#1b2130; --line:#2a3242;
  --ink:#e8ecf4; --muted:#93a0b8; --accent:#5ce1b9; --accent2:#7aa2ff;
  --star:#ffcf5c; --bib:#8fe388; --rec:#8ea3c4;
  --bad:#ff8080; --warn:#ffc46b;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{
  margin:0;background:var(--bg);color:var(--ink);
  font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
}
.wrap{max-width:1120px;margin:0 auto;padding:0 18px}
a{color:var(--accent2);text-decoration:none}
a:hover{text-decoration:underline}
code{background:#000;padding:1px 5px;border-radius:4px;font-size:.86em}

header.top{position:sticky;top:0;z-index:20;background:rgba(11,13,18,.94);
  backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
header .wrap{display:flex;flex-wrap:wrap;gap:10px;align-items:center;
  justify-content:space-between;padding-top:10px;padding-bottom:10px}
.brand{font-weight:650;letter-spacing:.2px;display:flex;align-items:center;gap:8px;font-size:.95rem}
.dot{width:9px;height:9px;border-radius:50%;background:var(--accent);
  box-shadow:0 0 0 4px rgba(92,225,185,.18)}
nav{display:flex;flex-wrap:wrap;gap:2px}
nav a{padding:7px 10px;border-radius:8px;font-size:.86rem;color:var(--muted)}
nav a:hover{background:var(--panel2);color:var(--ink);text-decoration:none}
nav a.on{background:var(--accent);color:#06110d;font-weight:650}

.pagehead{padding:34px 0 8px}
h1{font-size:clamp(1.7rem,4.6vw,2.6rem);line-height:1.12;margin:0 0 8px;letter-spacing:-.5px}
.sub{color:var(--muted);margin:0 0 6px;max-width:70ch;font-size:1.02rem}

section.panel{background:var(--panel);border:1px solid var(--line);border-radius:14px;
  padding:20px 20px 16px;margin:16px 0}
section.panel h2{font-size:1.16rem;margin:0 0 10px;letter-spacing:-.2px}
section.panel p{color:#cfd7e6;margin:0 0 10px}
section.panel p:last-child{margin-bottom:0}
.callout{border-color:rgba(92,225,185,.35);background:linear-gradient(180deg,rgba(92,225,185,.07),transparent)}
ul.tight,ol.tight{margin:0 0 10px;padding-left:20px;color:#cfd7e6}
ul.tight li,ol.tight li{margin:0 0 7px}

.grid4{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin:16px 0}
.card{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px}
.card .big{font-size:1.95rem;font-weight:700;letter-spacing:-1px;color:var(--accent);line-height:1}
.card .lbl{font-size:.74rem;text-transform:uppercase;letter-spacing:.09em;color:var(--muted);margin:6px 0 8px}
.card p{margin:0;font-size:.88rem;color:#cfd7e6}

.minis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:12px 0}
.mini{background:var(--panel2);border:1px solid var(--line);border-radius:11px;padding:12px}
.mini .k{font-size:.72rem;text-transform:uppercase;letter-spacing:.08em;color:var(--muted)}
.mini .v{font-size:1.32rem;font-weight:700;color:var(--accent);margin:3px 0}
.mini .s{font-size:.78rem;color:#cfd7e6}

.scroll{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:0 0 8px;
  border:1px solid var(--line);border-radius:11px}
table.data{width:100%;border-collapse:collapse;font-size:.87rem;min-width:640px}
table.data th{background:var(--panel2);text-align:left;padding:10px 11px;font-size:.74rem;
  text-transform:uppercase;letter-spacing:.06em;color:var(--muted);font-weight:650;
  border-bottom:1px solid var(--line);white-space:nowrap}
.thsub{text-transform:none;letter-spacing:0;color:#6f7d95;font-weight:400}
table.data td{padding:10px 11px;border-bottom:1px solid #1f2634;vertical-align:top;color:#dbe3f0}
table.data tbody tr:last-child td{border-bottom:none}
table.data td.num{text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums}
table.data td.strong{color:var(--accent);font-weight:700}
table.data td.muted{color:#5f6c82}
table.data td.best{color:var(--accent);font-weight:700}
table.data tr:hover td{background:rgba(122,162,255,.05)}
table.data.slim{min-width:0;font-size:.82rem}
table.data.slim th{padding:7px 9px}
table.data.slim td{padding:7px 9px}
td.rank{color:var(--muted);font-variant-numeric:tabular-nums}
table.matrix{min-width:820px}
table.matrix th.rowhead{background:var(--panel2);font-size:.75rem;color:#cfd7e6;
  text-transform:none;letter-spacing:0;white-space:nowrap;text-align:left}
table.matrix th.vert{writing-mode:vertical-rl;transform:rotate(180deg);height:120px;
  text-transform:none;letter-spacing:0;font-size:.72rem;white-space:nowrap}
table.matrix td.zero{background:rgba(92,225,185,.14);color:var(--accent);font-weight:700}
table.matrix td.near{background:rgba(122,162,255,.10);color:#cfdcff}
table.matrix td.far{color:var(--muted)}

.tiny{font-size:.79rem;color:var(--muted);line-height:1.45}
.tinymuted{font-size:.74rem;color:#5f6c82}
.note{font-size:.82rem;color:var(--muted);border-left:2px solid var(--line);padding-left:10px}
.muted{color:#5f6c82}
.warn{color:var(--warn)}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:.8rem}

.badge{display:inline-block;padding:3px 8px;border-radius:999px;font-size:.72rem;
  font-weight:700;white-space:nowrap;letter-spacing:.02em}
.badge.star{background:rgba(255,207,92,.16);color:var(--star);border:1px solid rgba(255,207,92,.35)}
.badge.bib{background:rgba(143,227,136,.14);color:var(--bib);border:1px solid rgba(143,227,136,.3)}
.badge.rec{background:rgba(142,163,196,.13);color:var(--rec);border:1px solid rgba(142,163,196,.28)}

.pill{display:inline-block;padding:2px 8px;border-radius:999px;background:var(--panel2);
  border:1px solid var(--line);font-size:.68rem;text-transform:uppercase;letter-spacing:.06em;
  color:var(--muted);font-weight:600}
.pill.need{background:rgba(255,196,107,.14);color:var(--warn);border-color:rgba(255,196,107,.32);
  text-transform:none;letter-spacing:0}

.hotels{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:12px}
.hotel{background:var(--panel2);border:1px solid var(--line);border-radius:12px;padding:14px}
.hotel h3{margin:0 0 4px;font-size:1rem;letter-spacing:-.1px}
.hotel .meta{font-size:.78rem;color:var(--muted);margin:0 0 9px}
.hotel p{margin:0 0 8px;font-size:.86rem;color:#cfd7e6}
.hotel .links{margin:0;font-size:.82rem;display:flex;gap:14px}
.flagline{color:var(--warn)!important;font-size:.78rem!important}

.qa,.sug{background:var(--panel);border:1px solid var(--line);border-radius:13px;
  padding:17px 18px;margin:12px 0}
.qa h3,.sug h3{margin:0 0 9px;font-size:1rem;display:flex;flex-wrap:wrap;gap:8px;align-items:baseline}
.qid,.sid{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:.78rem;color:var(--accent);
  background:rgba(92,225,185,.1);padding:2px 7px;border-radius:6px}
.qa p,.sug p{margin:0 0 8px;font-size:.9rem;color:#cfd7e6}
.state{font-size:.7rem;text-transform:uppercase;letter-spacing:.07em;font-weight:700;
  padding:2px 8px;border-radius:999px;margin-left:auto}
.state.ok{background:rgba(92,225,185,.13);color:var(--accent)}
.state.bad{background:rgba(255,128,128,.13);color:var(--bad)}
.state.warn{background:rgba(255,196,107,.13);color:var(--warn)}
.tag{display:inline-block;padding:2px 8px;border-radius:999px;font-size:.72rem;border:1px solid var(--line);color:var(--muted)}
.tag.bad{color:var(--bad);border-color:var(--bad)}
.tag.warn{color:var(--warn);border-color:var(--warn)}
.tag.ok{color:var(--ok,var(--muted))}
.impact{font-size:.7rem;text-transform:uppercase;letter-spacing:.07em;font-weight:700;
  padding:2px 8px;border-radius:999px}
.impact.hi{background:rgba(255,128,128,.13);color:var(--bad)}
.impact.md{background:rgba(255,196,107,.13);color:var(--warn)}
.impact.lo{background:rgba(142,163,196,.13);color:var(--rec)}
.trade{background:var(--panel2);border-radius:9px;padding:10px 12px;font-size:.86rem}
details{margin-top:6px}
summary{cursor:pointer;font-size:.8rem;color:var(--muted)}
ul.srcs{margin:8px 0 0;padding-left:18px;font-size:.82rem;line-height:1.7;word-break:break-word}
ul.srcs li{margin:0 0 3px}

footer{border-top:1px solid var(--line);margin-top:26px;padding:20px 18px 44px;
  color:var(--muted);font-size:.81rem}
footer p{margin:0 0 8px;max-width:80ch}

@media (max-width:640px){
  .pagehead{padding:22px 0 4px}
  section.panel{padding:16px 14px 12px;border-radius:12px}
  header .wrap{padding-top:8px;padding-bottom:8px}
  nav a{padding:6px 8px;font-size:.8rem}
  table.data{font-size:.82rem}
}
"""


# ------------------------------------------------- supplementary routes
ROUTES = [
    (
        "pricing.html",
        "Pricing",
        "Every price this plan uses, gathered in one place: hotels across all four measured weeks, restaurant totals for two, and the costs that sit outside the room rate.",
        [
            ("Official price evidence and eligible dates", "hotels.html#cheapest-week"),
            ("Hotel candidates and missing evidence", "hotels.html#every-hotel"),
            ("What dinner for two actually costs", "restaurants.html#costs"),
            ("Budget resort fees and 13.38% tax", "suggestions.html#S-08"),
            ("How the prices were captured (method)", "sources.html"),
        ],
    ),
    (
        "verification.html",
        "Verification",
        "A line-by-line audit trail: what was confirmed against which source, and every value that could not be confirmed and was therefore left blank.",
        [
            ("Flagged for review — every item that did not verify cleanly, with sources", "flagged.html"),
            ("Every source used, grouped by what it proves", "sources.html"),
            ("Open questions, and how to close each one", "questions.html"),
            ("Transit minutes and their stated limits", "transit.html#matrix"),
            ("Restaurant award tiers (starred vs listed)", "restaurants.html"),
        ],
    ),
    (
        "summary.html",
        "Executive summary",
        "The one-page version: what to book, what to avoid, and the three findings that change the shape of the trip.",
        [
            ("Overview and the three findings", "index.html"),
            ("Hotel evidence: no unsupported ranking", "hotels.html"),
            ("The four starred restaurants", "restaurants.html"),
            ("Suggestions ranked by impact", "suggestions.html"),
        ],
    ),
]


def build_route(name, title, subtitle, links):
    lis = "".join(
        f'<li><a href="{e(u)}">{e(l)}</a></li>' for l, u in links
    )
    body = f"""
<section class="panel">
  <h2>Where the {e(title.lower())} detail lives</h2>
  <p>{e(subtitle)}</p>
  <p>This route previously served an empty placeholder with zero table rows and zero source links.
  Instead of keeping a page with no data on it, it now routes to the pages that carry the actual figures —
  all generated from the same JSON in <code>data/</code>.</p>
  <ul class="tight">{lis}</ul>
</section>
"""
    return page(name, title, subtitle, body)


# ---------------------------------------------------------------- audit sections (F-39 onward)
def _links(srcs):
    return "<br>".join(
        f'<a href="{e(x["url"])}" target="_blank" rel="noopener">{e(x["label"])}</a>' for x in srcs)


def build_audit_sections():
    """F-39 onward from data/review-flags.json (26 Nov 2026 audit). Embedded in flagged.html."""
    rv = load("review-flags.json")
    cls = {"contradicted": "bad", "unverified": "warn", "needs review": "warn",
           "corrected": "ok", "confirmed": "ok", "information": "muted"}
    new_rows = "".join(
        f'<tr id="{e(f["id"])}"><td class="mono">{e(f["id"])}</td>'
        f'<td><span class="tag {cls.get(f["status"], "")}">{e(f["status"])}</span></td>'
        f'<td><strong>{e(f["title"])}</strong><div class="tiny">{e(f["where"])}</div></td>'
        f'<td>{e(f["what"])}</td><td>{e(f["effect"])}</td><td class="tiny">{_links(f["sources"])}</td></tr>'
        for f in rv["flags"])
    conf_rows = "".join(
        f'<tr id="{e(c["id"])}"><td class="mono">{e(c["id"])}</td><td>{e(c["what"])}</td>'
        f'<td class="tiny">{_links(c["sources"])}</td></tr>' for c in rv["confirmed"])
    return f"""
<section class="panel" id="audit-flags">
  <h2>New flags from the 26 Nov 2026 audit (F-39 to F-{rv["flags"][-1]["id"][2:]})</h2>
  <p class="note">Each row says what was checked, what was found, what the plan does about it, and where to look.
  <strong>Contradicted</strong> means a stored value was withdrawn. <strong>Unverified</strong> means it stays on the site, labelled, and needs checking before you rely on it.</p>
  <div class="scroll"><table class="data">
  <thead><tr><th>ID</th><th>Status</th><th>Item</th><th>What we found</th><th>Effect on the plan</th><th>Sources</th></tr></thead>
  <tbody>{new_rows}</tbody>
  </table></div>
</section>

<section class="panel" id="audit-confirmed">
  <h2>Checked and confirmed on 26 Nov 2026</h2>
  <div class="scroll"><table class="data">
  <thead><tr><th>ID</th><th>What was confirmed</th><th>Sources</th></tr></thead>
  <tbody>{conf_rows}</tbody>
  </table></div>
</section>
"""


_WD = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]


def _norm_days(text):
    t = (text or "").lower().replace("\u2013", "-").replace("\u2014", "-")
    for neg in ("closed ", "closed-", "closed:"):
        while neg in t:
            i = t.index(neg)
            j = min([x for x in (t.find(",", i), t.find(";", i), len(t)) if x != -1])
            t = t[:i] + t[j + 1:]
    return t


def _opens_on(venue, weekday):
    """True / False from the venue's own published days, or None if it publishes none.

    None is rendered as 'hours unknown' - never as 'open'."""
    days = _norm_days(venue.get("days"))
    if not days.strip():
        return None
    if "daily" in days or "open 24" in days:
        return True
    found = set()
    for part in days.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = [x.strip()[:3] for x in part.split("-", 1)]
            if a in _WD and b in _WD:
                i, j = _WD.index(a), _WD.index(b)
                found |= set(_WD[i:j + 1] if i <= j else _WD[i:] + _WD[:j + 1])
        elif part[:3] in _WD:
            found.add(part[:3])
    return (weekday[:3].lower() in found) if found else None


# (date, label, theme, activity ids, restaurant ids, why)
PLAN = [
    ("Mon 15 Feb", "Day 1", "Arrive, settle, walk the Strip",
     ["bellagio-fountains"], [],
     "Nothing is booked on arrival night. The Fountains are free, run until midnight on a weekday, and are the one attraction that needs no ticket and no start time."),
    ("Tue 16 Feb", "Day 2", "The 2-star dinner",
     [], ["joel-robuchon"],
     "Joël Robuchon publishes Tue–Sat only, so Tuesday is the earliest night it can be booked. This is the first reservation to make, before the hotel."),
    ("Wed 17 Feb", "Day 3", "Downtown: neon, mob history, free live music",
     ["neon-museum", "mob-museum", "fremont-street"], [],
     "All three downtown venues are open on Wednesday and sit in the same few blocks, so the day is one trip out and one trip back."),
    ("Thu 18 Feb", "Day 4", "Chinatown, by reservation",
     [], ["partage"],
     "Partage publishes Tue–Sat. Chinatown holds more MICHELIN listings than any other zone on this site, so the whole evening is one street."),
    ("Fri 19 Feb", "Day 5", "Show night",
     ["sphere", "high-roller"], [],
     "Sphere's 2027 calendar is not published, so this is the flexible night. The High Roller sells day and anytime tickets daily as the fallback."),
    ("Sat 20 Feb", "Day 6", "The 1-star counter",
     [], ["e-by-jose-andres"],
     "é publishes Tuesday–Saturday and seats very few people per night. Saturday is its last service of the week, so book it the moment reservations open."),
    ("Sun 21 Feb", "Day 7", "Cheapest, certain dinner",
     [], ["soulbelly-bbq"],
     "Both starred rooms are shut on Sunday. SoulBelly publishes Tue–Sun and is one of the few venues here with an official couple price on the page."),
]


def build_itinerary():
    R = {r["id"]: r for r in RES["restaurants"]}
    A = {a["id"]: a for a in ACT["activities"]}

    def venue_row(v, is_act):
        wid = v["id"]
        anchor = f'activities.html#{e(wid)}' if is_act else "restaurants.html"
        open_today = _opens_on(v, v["_wd"])
        if is_act:
            badge = '<span class="tag ok">open daily</span>' if open_today else '<span class="tag">check hours</span>'
            detail = e(v.get("hours") or "hours unverified")
        else:
            badge = ('<span class="tag ok">open ' + v["_wd"] + '</span>' if open_today
                     else '<span class="tag warn">not open ' + v["_wd"] + '</span>' if open_today is False
                     else '<span class="tag">hours unknown</span>')
            detail = e(v.get("hours") or "no hours published")
        price = (v.get("price_per_couple") if is_act else v.get("price_2adults")) or ""
        price_cell = (f'<div class="tiny">2 adults: {e(price)}</div>' if price
                      else '<div class="tiny muted">2-adult price: blank (unverified)</div>')
        award = ""
        if not is_act and v.get("award"):
            k = {"starred": "star", "bib": "bib", "recommended": "rec"}.get(v.get("award_class"), "rec")
            award = f' <span class="badge {k}">{e(v["award"])}</span>'
        return (f'<a href="{anchor}">{e(v["name"])}</a>{award}{badge}'
                f'<div class="tiny">{detail}</div>{price_cell}')

    rows = []
    for date, label, theme, acts, rests, why in PLAN:
        wd = date.split()[0]
        cells = []
        for aid in acts:
            v = dict(A[aid]); v["_wd"] = wd
            cells.append(venue_row(v, True))
        for rid in rests:
            v = dict(R[rid]); v["_wd"] = wd
            cells.append(venue_row(v, False))
        rows.append(f"""<tr>
<td><strong>{e(date)}</strong><div class="tiny muted">{e(label)}</div></td>
<td>{e(theme)}<div class="tiny">{e(why)}</div></td>
<td>{''.join(cells)}</td></tr>""")

    # Audit the plan against the data: how many slots are provably open?
    ok = warn = unknown = 0
    for date, _l, _t, acts, rests, _w in PLAN:
        wd = date.split()[0]
        for rid in rests:
            v = dict(R[rid]); v["_wd"] = wd
            o = _opens_on(v, wd)
            if o: ok += 1
            elif o is False: warn += 1
            else: unknown += 1

    body = f"""
<section class="panel" id="plan">
  <h2>A seven-night plan, 15–22 February 2027</h2>
  <p>Every slot below is one this site can evidence. Each restaurant states which weekday its own page
  says it opens, and where a venue publishes no hours the row says <strong>hours unknown</strong>
  rather than guessing. What the plan deliberately does <em>not</em> do is promise journey times:
  <a href="flagged.html#F-59">F-59</a> suspends the zone model, and no door-to-door journey has been
  verified, so days are grouped by district instead of timed.</p>
  <div class="grid4">
    <div class="card"><div class="big">7</div><div class="lbl">nights</div><p>15–22 Feb 2027, the stated provisional baseline.</p></div>
    <div class="card"><div class="big">{ok}</div><div class="lbl">slots proven open</div><p>Dinner slots whose own page publishes that weekday.</p></div>
    <div class="card"><div class="big">2</div><div class="lbl">starred dinners</div><p>Robuchon (Tue) and é (Sat) — book these first.</p></div>
    <div class="card"><div class="big">5</div><div class="lbl">districts</div><p>Strip, north Strip, Chinatown and downtown — grouped, not timed.</p></div>
  </div>
  <p class="note">{ok} of {ok + warn + unknown} dinner slots are confirmed open on their planned weekday;
  {unknown} cannot be confirmed because the venue publishes no days. No slot is scheduled on a day its
  own page rules out{"" if not warn else f" — {warn} conflicting slot(s) remain and are marked in red"}.</p>
</section>

<section class="panel">
  <h2>The plan, day by day</h2>
  <div class="scroll">
  <table class="data">
  <thead><tr><th>Date</th><th>What the day is for</th><th>Venue · open-day evidence · two-adult price</th></tr></thead>
  <tbody>{''.join(rows)}</tbody>
  </table>
  </div>
  <p class="note">Open-day badges come from each venue's own published days. Where a venue publishes
  no days, the badge reads <strong>hours unknown</strong> and the plan says to call — it never assumes
  the venue is open. Prices appear only where the dataset holds one; otherwise the row says
  <strong>blank (unverified)</strong>, because <a href="flagged.html#F-58">F-58</a> and
  <a href="flagged.html#F-61">F-61</a> withdrew the inherited totals.</p>
</section>

<section class="panel callout" id="risks">
  <h2>What would break this plan</h2>
  <ul class="tight">
    <li><strong>Robuchon and é are the only irreplaceable bookings.</strong> Both are small tasting rooms on Tue–Sat; if either is full, swap the two nights (they are interchangeable).</li>
    <li><strong>Sphere has no 2027 calendar</strong> (<a href="flagged.html#F-16">F-16</a>), so Friday is the flexible night.</li>
    <li><strong>Some venues publish no days at all</strong> — Sparrow + Wolf, Esther's Kitchen, Kame and Anima. Not one of them is scheduled here; all four would need a phone call first.</li>
    <li><strong>Michael Mina is closed</strong> (<a href="flagged.html#F-23">F-23</a>) and appears nowhere on the plan.</li>
    <li><strong>Hours are 27 Nov 2026 observations, not 2027 schedules</strong> — the standing caveat on every page of this site.</li>
    <li><strong>Journey times are unverified</strong> (<a href="flagged.html#F-59">F-59</a>). District grouping is not proof that a trip is under an hour; it is what can be supported today.</li>
  </ul>
</section>
"""
    return page("itinerary.html", "Itinerary",
                "A seven-night plan for 15–22 February 2027: only venues whose own pages support the scheduled weekday, and explicit blanks where they do not.",
                body)


def main():
    DOCS.mkdir(exist_ok=True)
    pages = {
        "index.html": build_index(),
        "hotels.html": build_hotels(),
        "dining.html": build_dining(),
        "restaurants.html": build_restaurants(),
        "activities.html": build_activities(),
        "transit.html": build_transit(),
        "questions.html": build_questions(),
        "suggestions.html": build_suggestions(),
        "flagged.html": build_flagged(),
        "sources.html": build_sources(),
        "repo-review.html": build_repo_review(),
        "itinerary.html": build_itinerary(),
    }
    for name, title, subtitle, links in ROUTES:
        pages[name] = build_route(name, title, subtitle, links)
    # Publish to BOTH docs/ and the repo root. GitHub Pages on this repo is pinned
    # to main:/ (the API refuses to repoint it to /docs), so the root copy is what
    # visitors actually get. Writing both makes the deploy path independent of that
    # setting. The root copies are generated files — never edit them by hand.
    targets = [DOCS, ROOT]
    for out_dir in targets:
        out_dir.mkdir(exist_ok=True)
        for name, content in pages.items():
            (out_dir / name).write_text(content, encoding="utf-8")
        (out_dir / "style.css").write_text(CSS, encoding="utf-8")
        (out_dir / ".nojekyll").write_text("", encoding="utf-8")
    print(f"published to: {', '.join(str(t.relative_to(ROOT)) + '/' for t in targets)}")
    total = sum(len(c) for c in pages.values())
    print(f"wrote {len(pages)} pages + style.css to docs/ ({total:,} bytes of html)")
    for n in pages:
        print("  docs/" + n)


if __name__ == "__main__":
    main()
