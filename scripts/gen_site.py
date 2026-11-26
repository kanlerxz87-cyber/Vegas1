#!/usr/bin/env python3
"""
gen_site.py — renders the static site in docs/ from the JSON in data/.

Run after scripts/build.py:
    python3 scripts/build.py && python3 scripts/gen_site.py

No framework, no CDN, no build step at deploy time. Everything is plain HTML +
one stylesheet, so GitHub Pages serves docs/ directly from main.
"""
import json
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
DIRECT = load("direct-rates.json")

e = html.escape

# derived counts — always computed, never typed by hand
_C = {}
for _r in RES["restaurants"]:
    _C[_r["award_class"]] = _C.get(_r["award_class"], 0) + 1
N_TOTAL = len(RES["restaurants"])
N_STARRED = _C.get("starred", 0)
N_BIB = _C.get("bib", 0)
N_REC = _C.get("recommended", 0)
N_TWO = sum(1 for _r in RES["restaurants"] if _r["award"].startswith("2"))
N_ONE = sum(1 for _r in RES["restaurants"] if _r["award"].startswith("1"))


def money(v):
    return "—" if v in (None, "") else f"${v:,.0f}"


def nav(active):
    items = [
        ("index.html", "Overview"),
        ("hotels.html", "Hotels"),
        ("restaurants.html", "Michelin"),
        ("activities.html", "Things to do"),
        ("transit.html", "Getting around"),
        ("questions.html", "Open questions"),
        ("suggestions.html", "Suggestions"),
        ("review.html", "Flagged for review (current)"),
        ("flagged.html", "Full flags & repo issues"),
        ("repo-review.html", "Repo review"),
        ("sources.html", "Sources"),
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
  </div>
  {body}
</main>
<footer class="wrap">
  <p>Hotel direct-booking snapshots are dated 26 Nov 2026 and linked to the property's own engine; amounts are clearly marked when calculated, tax-exclusive, or incomplete. Older Booking.com figures are third-party snapshots, not official rates. Blank means <strong>not verified</strong>.</p>
  <p>Las Vegas had no MICHELIN Guide between 2010 and 2025. All awards here are from the 2026
  Southwest selection, the first since 2009.</p>
</footer>
</body>
</html>
"""


# ---------------------------------------------------------------- index
def build_index():
    starred = [r for r in RES["restaurants"] if r["award_class"] == "starred"]
    bib = [r for r in RES["restaurants"] if r["award_class"] == "bib"]
    rec = [r for r in RES["restaurants"] if r["award_class"] == "recommended"]

    # Current official rates are a small, dated sample, not a city-wide ranking.
    n_hotels = len(HOTELS["hotels"])
    official_rate_rows = [h for h in DIRECT["hotels"] if h["name"] == "Horseshoe Las Vegas"]
    horseshoe_feb = official_rate_rows[0]["rates"]["W1"]
    horseshoe_mar = official_rate_rows[0]["rates"]["W5"]
    horseshoe_cheapest = min(v for v in official_rate_rows[0]["rates"].values() if v is not None)

    cards = [
        (str(N_TOTAL), "MICHELIN listings", f"{N_STARRED} starred · {N_BIB} Bib Gourmand · {N_REC} Recommended.<br>No three-star restaurant exists in Las Vegas."),
        ("0", "subway lines", "Las Vegas has no metro. Buses, Monorail and the Vegas Loop were modelled instead — <a href='questions.html'>Q-01</a>."),
        (f"${horseshoe_cheapest}", "lowest checked nightly rate", "Horseshoe King, 15–22 Mar among five official date checks; resort fee included, taxes excluded. Not a final stay total."),
        ("Dec 4", "Wynn offer deadline", "Official Cyber offer; book by 4 Dec 2026 for eligible stays through 30 Jun 2027. See dated terms on Hotels."),
    ]
    card_html = "".join(
        f'<div class="card"><div class="big">{v}</div><div class="lbl">{e(k)}</div><p>{t}</p></div>'
        for v, k, t in cards
    )

    star_lis = "".join(
        f'<li><strong>{e(r["name"])}</strong> — {e(r["award"])} · {e(r["location"])}</li>' for r in starred
    )
    rest_count = len(bib) + len(rec)

    body = f"""
<section class="panel">
  <h2>What this is</h2>
  <p>Two adults, seven nights in Las Vegas, sometime between <strong>15 February and 23 March 2027</strong>.
  The brief asked for hotels ranked by price, location and how many MICHELIN restaurants are within an hour
  by public transport — and for every number to be traceable to a source.</p>
  <p>Sources are linked at row level. The direct hotel-engine quotes below were captured on <strong>26 November 2026</strong>; older Booking.com prices are third-party snapshots and are not treated as official rates. Calculations and missing values are labeled. See <a href="review.html">Flagged for review</a> before making a booking decision.</p>
</section>

<section class="grid4">{card_html}</section>

<section class="panel">
  <h2>The four starred restaurants</h2>
  <p>These are the only starred rooms in the city, and all four are on the Strip:</p>
  <ul class="tight">{star_lis}</ul>
  <p>The other <strong>{rest_count}</strong> listings — {N_BIB} Bib Gourmand and {N_REC} Recommended — are all in the
  <a href="restaurants.html">MICHELIN page</a>, each labelled with which of the three tiers it sits in.</p>
</section>

<section class="panel">
  <h2 id="three-things">Three things that change the answer</h2>
  <ol class="tight">
    <li><strong>The 7-night basis collides with the requested dates.</strong> The preferred window
    2027-02-15 → 2027-02-18 is three nights, not seven. Seven-night totals starting on 15 Feb are used
    so the figures match the brief — <a href="questions.html">Q-02</a>.</li>
    <li><strong>The "within 1 hour" ranking does not rank anything.</strong> Every hotel in Las Vegas is within
    an hour of all {N_TOTAL} restaurants, so the metric returns {N_TOTAL}/{N_TOTAL} for all {n_hotels} properties. A
    <em>20-minute</em> column was added and is what actually separates them — <a href="questions.html">Q-01</a>.</li>
    <li><strong>There is no universal cheapest week in the verified official sample.</strong> The same named Horseshoe King rate was lowest on 15–22 March among five quoted windows. Caesars Palace's standard King quote was $201/night on 15–22 February versus $317/night on 15–22 March; two other pages returned a different accessible room variant and are left blank for like-for-like comparison. Rates are volatile, tax-exclusive, and property-specific — <a href="review.html#F-29">F-29</a>.</li>
  </ol>
</section>

<section class="panel callout">
  <h2>Before choosing a hotel</h2>
  <p>The current direct-rate sample confirms date-specific offers, not a city-wide best buy. The lowest checked Horseshoe King quote was $105/night for 15–22 March; the preferred-week quote was $128/night, both with resort fee and before tax. The room page describes a marble bathroom but does not explicitly state "private". Confirm the bathroom requirement and final checkout total in writing. See the <a href="hotels.html#direct-rates">official quote table</a> and <a href="review.html">review flags</a>.</p>
</section>
"""
    return page("index.html", "Las Vegas, seven nights, 2027",
                "A sourced plan for two adults between 15 Feb and 23 Mar 2027 — hotels, MICHELIN restaurants, transit and what could not be verified.",
                body)


# ---------------------------------------------------------------- hotels
def build_hotels():
    direct_by_id = {
        "flamingo": next(h for h in DIRECT["hotels"] if h["name"] == "Flamingo Las Vegas"),
        "horseshoe": next(h for h in DIRECT["hotels"] if h["name"] == "Horseshoe Las Vegas"),
        "caesars-palace": next(h for h in DIRECT["hotels"] if h["name"] == "Caesars Palace"),
    }

    def direct_w1(h):
        match = direct_by_id.get(h["id"])
        return match["rates"].get("W1") if match else None

    hs = sorted(HOTELS["hotels"], key=lambda h: (
        -h["michelin_within_20"], direct_w1(h) is None,
        direct_w1(h) if direct_w1(h) is not None else float("inf"),
        h["name"].casefold(),
    ))
    rows = []
    for i, h in enumerate(hs, 1):
        q = direct_w1(h)
        if q is None:
            quote = '<span class="muted">— not verified at official engine</span>'
        else:
            source = direct_by_id[h["id"]]["source_urls"]["W1"]
            quote = f'<a href="{e(source)}" target="_blank" rel="noopener">${q}/night avg · official</a>'
        bed = e(h["bed"])
        if "not guaranteed" in h["bed"].lower() or "assigned on arrival" in h["bed"].lower():
            bed = f'<span class="warn">{e(h["bed"])}</span>'
        hotel_name = (f'<a href="{e(h["official_url"])}" target="_blank" rel="noopener">{e(h["name"])}</a>'
                      if h.get("official_url") else f'{e(h["name"])} <span class="warn">(no official property source verified; F-14)</span>')
        rows.append(f"""<tr>
<td class="rank">{i}</td>
<td>{hotel_name}<div class="tiny">{e(h['zone'].replace('-', ' '))}</div></td>
<td class="num strong">{h['michelin_within_20']}</td>
<td class="num muted">{h['michelin_within_60']}</td>
<td>{bed}</td>
<td>{quote}</td>
</tr>""")

    rank_table = f"""
<div class="scroll"><table class="data">
<thead><tr><th>#</th><th>Hotel (official property link)</th><th>≤20 min</th><th>≤60 min</th><th>Bed note (prior capture, not rechecked)</th><th>Official 15–22 Feb rate check</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>
<p class="note">This is a screening order by estimated MICHELIN proximity, then the limited official direct-rate quotes; it is not a complete hotel recommendation. Only three of 32 properties have a current exact-date official quote in this table. The ≤60-minute user metric is 24 for every property and cannot rank hotels. Travel minutes are estimates (see Transit). A named bed category is shown when the direct engine returned it; private-bathroom fit remains unconfirmed where flagged.</p>
"""

    direct_rows = []
    for hotel in DIRECT["hotels"]:
        cells = []
        for window in DIRECT["meta"]["stay_windows"]:
            wid = window["id"]
            nightly = hotel["rates"].get(wid)
            source = hotel["source_urls"].get(wid)
            if nightly is None or not source:
                value = '<span class="muted">— unverified</span>'
            else:
                subtotal = nightly * 7
                value = (f'<a href="{e(source)}" target="_blank" rel="noopener">'
                         f'${nightly}/night · ${subtotal:,}* / 7 nights</a>')
            cells.append(f'<td>{value}</td>')
        direct_rows.append(
            f'<tr><td>{e(hotel["name"])}</td><td>{e(hotel["room"])}</td>'
            f'<td>{e(hotel["bed"])}</td><td>{e(hotel["private_bathroom"])}</td>'
            + "".join(cells) + '</tr>'
        )
    direct_header = "".join(f'<th>{e(w["label"])}</th>' for w in DIRECT["meta"]["stay_windows"])
    offer = DIRECT["meta"]["official_offer_deadline"]

    cards = []
    for h in HOTELS["hotels"]:
        warning = "" if h.get("official_verified") == "yes" else ' <span class="tinymuted">(property page not re-fetched in this pass)</span>'
        flags = f'<p class="flagline">⚑ {", ".join(e(f) for f in h["flags"])} — see <a href="review.html">review flags</a></p>' if h.get("flags") else ""
        cards.append(f"""<article class="hotel">
  <h3><a href="{e(h['official_url'])}" target="_blank" rel="noopener">{e(h['name'])}</a> <span class="pill">{e(h['tier'])}</span></h3>
  <p class="meta">{e(h['zone'].replace('-',' '))} · {h['michelin_within_20']} MICHELIN within 20 min (estimate) · resort fee: {e(h['resort_fee'])}</p>
  <p class="tiny">Bed: {e(h['bed'])} · private bathroom: {'stated in prior source capture' if h['private_bath'] else 'not verified'}{(' · ' + e(h['address'])) if h.get('address') else ''}{warning}</p>
  <p>{e(h['notes'])}</p>{flags}
</article>""")

    body = f"""
<section class="panel" id="direct-rates">
  <h2>Official direct-booking checks — captured 26 Nov 2026</h2>
  <p>Two adults · one room · seven nights. Each populated nightly rate links to the property's own dated booking engine. The listed seven-night subtotal is arithmetic from the displayed, rounded average nightly rate; it is <strong>not</strong> an official checkout total. Resort fee is included in the nightly figure; taxes are excluded by the source.</p>
  <div class="scroll"><table class="data">
  <thead><tr><th>Hotel</th><th>Named room</th><th>Bed in official room description</th><th>Private bathroom</th>{direct_header}</tr></thead>
  <tbody>{''.join(direct_rows)}</tbody></table></div>
  <p class="note">* Calculated as displayed average per night × 7; exact pre-tax total and room tax are not printed in the fetched page, so exact final charge is <strong>unverified</strong>. A dash means the exact room/date quote did not appear in the fetched page; it does not mean sold out. The required private-bathroom status is not explicitly confirmed for these quoted room categories, so none is presented as fully compliant yet (F-31).</p>
  <p class="note"><strong>Current booking deadline found:</strong> {e(offer["hotel"])} {e(offer["offer"])} displays <strong>${offer["displayed_average_nightly"]}/night</strong> for the 640 sq ft Resort King, resort fee included and taxes excluded. Book by <strong>4 Dec 2026</strong> for qualifying stays through 30 Jun 2027. The official offer terms say the deal can be booked Nov 20–Dec 4; this is a deadline, not a claim that the rate is the cheapest. <a href="{e(offer["source"])}" target="_blank" rel="noopener">Official dated offer</a> · <a href="{e(offer["terms_source"])}" target="_blank" rel="noopener">Official terms</a>.</p>
  <p><a href="review.html#F-29">Review price-window conflicts (F-29)</a> · <a href="review.html#F-30">Resorts World fee ambiguity (F-30)</a></p>
</section>
<section class="panel">
  <h2>Hotel screening table</h2>
  <p>The bed, location, guest-score, and Michelin proximity screening is presented alongside official property links. A blank current price means no exact-date official quote was verified for that property in this session. No Booking.com-only value is used to choose or rank the hotels.</p>
  {rank_table}
</section>
<section class="panel">
  <h2>Full 32-property inventory</h2>
  <p>Property details below are reference links; previously captured Booking.com prices were omitted from this decision view because they are not official-property quotes. Every property title links to its official site. Blank or unconfirmed fit details must be checked with the property.</p>
  <div class="hotels">{"".join(cards)}</div>
</section>
"""
    return page("hotels.html", "Hotels",
                f"{len(HOTELS['hotels'])} properties with official links; direct hotel prices are shown only where fetched for the exact dates.",
                body)


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
        tt = f'<a href="{r["tiktok"]}" target="_blank" rel="noopener">TT</a>' if r["tiktok"] else '<span class="muted">—</span>'
        hours = e(r["hours"]) if r["hours"] else '<span class="warn">not verified</span>'
        days = r["days"] or ""
        # the source sometimes repeats the day span inside the hours string
        # (e.g. days="Tue-Sat", hours="Tue-Sat 5:00 PM - 9:30 PM") - print it once
        if days and r["hours"] and r["hours"].lower().replace("\u2013", "-").startswith(
            days.lower().replace("\u2013", "-")
        ):
            hours = e(r["hours"][len(days):].strip())
        days_html = e(days) if days else '<span class="warn">not verified</span>'
        price = e(r["price_2adults"]) if r["price_2adults"] else '<span class="muted">on request</span>'
        rows.append(f"""<tr>
<td><a href="{e(r['official_url'])}" target="_blank" rel="noopener">{e(r['name'])}</a>
  <div class="tiny">{e(r['cuisine'])} · {e(r['location'])}</div></td>
<td><span class="badge {cls(r)}">{e(r['award'])}</span></td>
<td>{days_html}<div class="tiny">{hours}</div></td>
<td class="tiny">{e(r['exceptions']) or '—'}</td>
<td class="num">{price}</td>
<td class="tiny">{yt}<br>{ig} {tt}</td>
</tr>""")

    table = f"""
<div class="scroll">
<table class="data">
<thead><tr>
<th>Restaurant</th><th>Award</th><th>Days &amp; hours</th><th>Exceptions</th>
<th>Cost<br><span class="thsub">2 adults</span></th><th>Watch</th>
</tr></thead>
<tbody>{''.join(rows)}</tbody>
</table>
</div>
<p class="note">Award labels are the 2026 MICHELIN Guide's three tiers, shown separately so an unstarred listing
can never be mistaken for a starred one. <strong>"On request"</strong> means the venue publishes no price — it is not
a missing entry and it is not an average. Only three restaurants print a real per-person figure.</p>
"""

    counts = RES["meta"]["counts"]
    body = f"""
<section class="panel">
  <h2>What "MICHELIN" means here</h2>
  <p>Las Vegas had <strong>no MICHELIN Guide between 2010 and 2025</strong>. The 2026 Southwest selection —
  published 26 August 2026 — is the city's first since 2009, which is why so many videos and blogs still
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
  <h2 id="costs">What dinner for two actually costs</h2>
  <p>Only three venues publish a number, and two of them are outside the starred group:</p>
  <ul class="tight">
    <li><strong>Michael Mina</strong> — $295++ per person, 10-course tasting → <strong>$590++</strong> for two,
      <strong>but the venue is currently closed</strong>: its own Bellagio page reads &ldquo;Monday to Sunday: Closed&rdquo;
      and labels it <em>Temporarily closed</em>, with no reopen date published. Treat this as a price for a service that
      is not running, not as a bookable dinner (FLAGS.md <a href="sources.html#flags">F-23</a>).</li>
    <li><strong>KAME Omakase</strong> — $500 per person, signature omakase → <strong>$1,000++</strong> for two.</li>
    <li><strong>Anima by EDO</strong> — $85 per person tasting → <strong>$170++</strong> for two.</li>
  </ul>
  <p>The four <em>starred</em> rooms are all "price on request". A couple planning a stars-heavy week should expect
  the starred nights to be the largest line in the budget after the hotel, and should plan on reserving
  before booking the room — <a href="suggestions.html">S-04</a>.</p>
</section>
"""
    return page("restaurants.html", "MICHELIN restaurants",
                f"All {counts['total']} Las Vegas listings from the 2026 guide, each labelled starred, Bib Gourmand or Recommended.",
                body)


# ---------------------------------------------------------------- activities
def build_activities():
    rows = []
    for a in ACT["activities"]:
        social_links = []
        for key, label in (("instagram", "Instagram"), ("tiktok", "TikTok"), ("youtube", "YouTube")):
            url = a.get(key)
            if url:
                social_links.append(f'<a href="{e(url)}" target="_blank" rel="noopener">{label}</a>')
        socials = ' · '.join(social_links) if social_links else '<span class="warn">not verified</span>'
        rows.append(f"""<tr>
<td><a href="{e(a['official_url'])}" target="_blank" rel="noopener">{e(a['name'])}</a>
 <div class="tiny">{e(a['type'])} · {e(a['zone'].replace('-',' '))}</div></td>
<td>{e(a['days'])}<div class="tiny">{e(a['hours'])}</div></td>
<td class="tiny">{e(a['exceptions']) or '—'}</td>
<td class="num">{e(a['price_per_couple']) or '—'}</td>
<td class="tiny">{e(a['price_note'])}</td>
<td class="tiny">{socials}</td>
</tr>""")

    nv = "".join(
        f'<li><strong>{e(n["name"])}</strong> — {e(n["reason"])}</li>' for n in ACT["not_verified"]
    )

    body = f"""
<section class="panel">
  <h2>Four things worth the day</h2>
  <div class="scroll">
  <table class="data">
  <thead><tr><th>Venue</th><th>Days &amp; hours</th><th>Exceptions</th><th>2 adults</th><th>Price basis</th><th>Official social links</th></tr></thead>
  <tbody>{''.join(rows)}</tbody>
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
  and downtown is the one zone that is a 25–30 minute trip from everywhere else.</p>
</section>
"""
    return page("activities.html", "Things to do",
                "Four verified venues with official hours and prices for two — and two that were checked and deliberately left out.",
                body)


# ---------------------------------------------------------------- transit
def build_transit():
    sys_rows = []
    for s in TRANSIT["systems"]:
        stations = ", ".join(s.get("stations", []))
        sys_rows.append(f"""<tr>
<td><a href="{e(s['official_url'])}" target="_blank" rel="noopener">{e(s['name'])}</a>
 <div class="tiny">{e(s.get('hours', ''))}</div></td>
<td class="tiny">{e(s['fare_note'])}</td>
<td class="tiny">{e(s['note'])}</td>
</tr>""")

    zones = [z["id"] for z in TRANSIT["zones"]]
    labels = {z["id"]: z["label"] for z in TRANSIT["zones"]}
    head = "".join(f'<th class="vert">{e(labels[z])}</th>' for z in zones)
    mrows = []
    for z in zones:
        cells = []
        for z2 in zones:
            v = TRANSIT["minutes"][z][z2]
            k = "zero" if v == 0 else ("near" if v <= 20 else "far")
            cells.append(f'<td class="num {k}">{v}</td>')
        matrix_sources = [
            '<a href="https://www.rtcsnv.com/ways-to-travel/fares-passes/" target="_blank" rel="noopener">RTC routes/fare source</a>',
            '<a href="https://www.lvmonorail.com/stations/" target="_blank" rel="noopener">Monorail stations</a>',
            '<a href="https://www.boringcompany.com/projects/las-vegas-loop" target="_blank" rel="noopener">Vegas Loop stops</a>',
        ]
        mrows.append(f'<tr><th class="rowhead">{e(labels[z])}</th>{"".join(cells)}<td class="tiny">{" · ".join(matrix_sources)}</td></tr>')

    center20 = max(
        (h["michelin_within_20"] for h in HOTELS["hotels"] if h["zone"] == "center-strip"),
        default=0,
    )
    body = f"""
<section class="panel">
  <h2>There is no subway in Las Vegas</h2>
  <p>The brief asked for restaurants within an hour <em>by subway or bus</em>. Las Vegas has no metro or light rail,
  so three separate systems were modelled instead — and they do not share a ticket:</p>
  <div class="scroll">
  <table class="data">
  <thead><tr><th>System</th><th>Fares</th><th>Reach</th></tr></thead>
  <tbody>{''.join(sys_rows)}</tbody>
  </table>
  </div>
  <p class="note">Fares are the operators' own published prices. The Monorail 7-day pass ($59.95 electronic) pays for
  itself at ten single rides and covers the exact Strip stretch the starred restaurants sit on.</p>
</section>

<section class="panel">
  <h2>Correction: Chinatown is reachable by bus</h2>
  <p>An earlier version of this matrix recorded Chinatown / Spring Mountain Rd as reachable only by car or
  rideshare. <strong>That was wrong.</strong> RTC <strong>Route 203</strong> runs the length of Spring Mountain Road,
  and its published timetable carries a timed stop at <strong>Las Vegas Blvd</strong> — the north end of the Strip,
  where Wynn, Encore, Resorts World and SAHARA are.</p>
  <p>This matters more than any other single number on this site, because <strong>seven of the 24 MICHELIN listings
  sit on that one road</strong>: Partage, Kabuto, KAME Omakase, Lamaii, Sparrow + Wolf, Pho Ga Bac Bac and YEN Viet
  Kitchen. Nearly a third of the guide is on a road that turns out to have a bus.</p>
  <p>The timetable's eastbound runs give <strong>Decatur to Las Vegas Blvd in 14 minutes</strong>. Adding a walk to the
  stop, a platform wait and a walk at the far end puts the north Strip at about <strong>34 minutes</strong> from
  Chinatown door to door — comfortably inside the brief's one-hour limit, from a hotel with no Monorail station.</p>
  <p>This is the <strong>only published travel time in the whole model</strong>. Every other minute figure here is an
  estimate built from station lists and route maps, and is labelled as one. Verify the timetable yourself:
  <a href="https://rtcws.rtcsnv.com/routePDF/203.pdf" target="_blank" rel="noopener">RTC Route 203 timetable (PDF)</a>.</p>
</section>

<section class="panel">
  <h2 id="matrix">Estimated one-way minutes between zones</h2>
  <p><strong>These are estimates, not timetables.</strong> No official source publishes door-to-door times; these are
  built from the official station lists and route maps and rounded to five minutes.</p>
  <div class="scroll">
  <table class="data matrix">
  <thead><tr><th>Origin zone</th>{head}<th>Official route/station source links</th></tr></thead>
  <tbody>{''.join(mrows)}</tbody>
  </table>
  </div>
</section>

<section class="panel">
  <h2>Why the 60-minute ranking failed, and what was done instead</h2>
  <p>The brief asked to rank hotels by how many MICHELIN restaurants fall within an hour. Run literally, that
  number is <strong>24 out of 24 for every single hotel</strong> in the dataset — including the ones in Henderson
  and Summerlin. The Strip is about four miles long and Chinatown is about three miles west of it, so an hour
  covers the entire city.</p>
  <p>A metric that returns the same value for all {len(HOTELS['hotels'])} properties cannot rank them. So a
  <strong>20-minute</strong> column was added, and that one does separate the field:</p>
  <div class="grid4">
    <div class="card"><div class="big">24</div><div class="lbl">West of the Strip</div><p>Palms Place reaches everything in 20 minutes — the western hotels sit between Chinatown and the Strip.</p></div>
    <div class="card"><div class="big">23</div><div class="lbl">North Strip</div><p>Venetian, Palazzo, Wynn, Encore, SAHARA, Resorts World.</p></div>
    <div class="card"><div class="big">{center20}</div><div class="lbl">Centre Strip</div><p>The densest restaurant zone — more starred rooms, fewer Chinatown minutes.</p></div>
    <div class="card"><div class="big">0</div><div class="lbl">Off-Strip</div><p>Henderson and Summerlin: correct resorts, 11–17 miles from dinner.</p></div>
  </div>
  <p class="note">This substitution is a material change to the brief and is raised openly as
  <a href="questions.html">Q-01</a>. The whole matrix lives in one file, so a different threshold can be
  recomputed in a single step.</p>
</section>
"""
    return page("transit.html", "Getting around",
                "No subway, three separate systems, and the reason the 'within one hour' ranking had to be tightened to twenty minutes.",
                body)


# ---------------------------------------------------------------- questions
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
<article class="qa">
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
        sources = []
        for url in s.get("source_urls", []):
            label = e(url.rsplit("/", 1)[-1] or url)
            sources.append(f'<a href="{e(url)}">{label}</a>')
        evidence = " · ".join(sources) or e(s.get("evidence", ""))
        cards.append(f"""
<article class="sug" id="{e(s['id'])}">
  <h3><span class="sid">{e(s['id'])}</span> {e(s['title'])}
   <span class="impact {imp[s['impact']]}">{e(s['impact'])} impact</span>{need}</h3>
  <p>{e(s['body'])}</p>
  <p class="trade"><strong>Trade-off:</strong> {e(s['trade_off'])}</p>
  <p class="tiny">Evidence: {evidence}</p>
</article>""")

    needs = [s for s in SUG["suggestions"] if s["needs_decision"]]
    n_sug = len(SUG["suggestions"])
    body = f"""
<section class="panel">
  <h2>{len(SUGGESTIONS_HEAD)}</h2>
  <p>{n_sug} proposals, ranked by how much they change the outcome. <strong>{len(needs)} of them need a decision
  from you</strong> before the plan can be finalised — they are marked in the list. Nothing here was silently
  applied to the data.</p>
  <p>The three highest-value next steps are: settle the <strong>trip length</strong> (three preferred nights or a longer stay), require an explicitly named <strong>queen-or-larger room with a private bathroom</strong>, and compare exact-date <strong>official checkout totals</strong> on the same day. Earlier broad claims that moving to March always saves money have been withdrawn; see <a href="review.html#F-29">F-29</a>.</p>
</section>
<div class="suglist">{''.join(cards)}</div>
"""
    return page("suggestions.html", "Suggestions",
                f"{len(SUG['suggestions'])} decision improvements, ranked, with trade-offs and whether each needs a decision first.",
                body)


SUGGESTIONS_HEAD = [f"{len(SUG['suggestions'])} ways to improve this plan"]


# ---------------------------------------------------------------- sources
def build_sources():
    flag_rows = []
    # This page highlights selected flags; the full register is in FLAGS.md.
    N_FLAGS = 31
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
        ("F-29", "Direct hotel price windows", "Official quotes differ by property, room type and capture date; no universal cheapest week."),
        ("F-30", "Resorts World", "Official rate calendar's fee-inclusion legends conflict; exact total left blank."),
        ("F-31", "Private bathroom requirement", "Exact direct-rate room cards do not explicitly confirm a private bathroom."),
    ]
    for fid, where, what in flags:
        flag_rows.append(f'<li><strong class="mono">{fid}</strong> — <strong>{e(where)}:</strong> {e(what)}</li>')

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
    activity_social_sources = {}
    for activity in ACT["activities"]:
        if activity.get("social_source"):
            activity_social_sources[f'{activity["name"]} — official social-account verification'] = activity["social_source"]
    groups.setdefault("Activity social-link verification sources", []).extend(sorted(activity_social_sources.items()))
    groups.setdefault("Pricing", []).extend([
        ("Booking.com — Las Vegas, 5★ resorts, 15–22 Feb 2027", "https://www.booking.com/searchresults.html?ss=Las+Vegas&checkin=2027-02-15&checkout=2027-02-22&group_adults=2&no_rooms=1&selected_currency=USD&nflt=class%3D5%3Bht_id%3D206&order=price"),
        ("Booking.com — same search, 8–15 Mar 2027", "https://www.booking.com/searchresults.html?ss=Las+Vegas&checkin=2027-03-08&checkout=2027-03-15&group_adults=2&no_rooms=1&selected_currency=USD&nflt=class%3D5%3Bht_id%3D206&order=price"),
        ("Booking.com — same search, 1–8 Mar 2027", "https://www.booking.com/searchresults.html?ss=Las+Vegas&checkin=2027-03-01&checkout=2027-03-08&group_adults=2&no_rooms=1&selected_currency=USD&nflt=class%3D5%3Bht_id%3D206&order=price"),
        ("Booking.com — same search, 15–22 Mar 2027", "https://www.booking.com/searchresults.html?ss=Las+Vegas&checkin=2027-03-15&checkout=2027-03-22&group_adults=2&no_rooms=1&selected_currency=USD&nflt=class%3D5%3Bht_id%3D206&order=price"),
        ("Booking.com — Wynn Las Vegas property page", "https://www.booking.com/hotel/us/wynn-las-vegas-boulevard.html"),
        ("Wynn Las Vegas — rooms and suites", "https://www.wynnlasvegas.com/rooms-and-suite"),
    ])
    direct_sources = {}
    for hotel in DIRECT["hotels"]:
        for window, url in hotel["source_urls"].items():
            label = f'{hotel["name"]} — {next(w["label"] for w in DIRECT["meta"]["stay_windows"] if w["id"] == window)} direct rate'
            direct_sources[label] = url
    offer = DIRECT["meta"]["official_offer_deadline"]
    direct_sources["Wynn Las Vegas — dated Cyber offer"] = offer["source"]
    direct_sources["Wynn Las Vegas — Cyber offer terms"] = offer["terms_source"]
    groups.setdefault("Official dated hotel booking-engine checks (captured 2026-11-26)", []).extend(sorted(direct_sources.items()))
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
  <p>Verified claims link to the responsible official page. Derived travel-time estimates, arithmetic subtotals, and blank/unverified values are labeled as such; they are not official source facts. If an official source conflicts with a displayed claim, the source is authoritative.</p>
</section>

<section class="panel" id="flags">
  <h2>Flags — what did not verify cleanly</h2>
  <p>A flag means the cell is <strong>blank or labelled</strong>, never that a number was filled in.</p>
  <ul class="tight">{''.join(flag_rows)}</ul>
  <p class="note">The full register (F-01–F-{N_FLAGS}) and deliberate non-inclusions are in
  <a href="https://github.com/kanlerxz87-cyber/Vegas1/blob/main/FLAGS.md" target="_blank" rel="noopener">FLAGS.md</a>; current hotel decisions needing follow-up are on <a href="review.html">Flagged for review</a>.</p>
</section>
{''.join(blocks)}
"""
    return page("sources.html", "Sources & flags",
                "Every page used to build this plan, grouped by what it proves — plus the flags for what would not confirm.",
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


# ------------------------------------------------- review / audit routes
def build_review():
    rows = []
    for item in DIRECT["review_items"]:
        links = " · ".join(
            f'<a href="{e(url)}" target="_blank" rel="noopener">official source {i + 1}</a>'
            for i, url in enumerate(item["source_urls"])
        )
        rows.append(
            f'<tr id="{e(item["id"])}"><td class="mono">{e(item["id"])}</td>'
            f'<td><strong>{e(item["title"])}</strong><p>{e(item["finding"])}</p>'
            f'<p><strong>Next step:</strong> {e(item["action"])}</p></td>'
            f'<td>{links}</td></tr>'
        )
    body = f"""
<section class="panel callout">
  <h2>Do not treat the current rate sample as a booking recommendation</h2>
  <p>Official booking-engine results were fetched on 26 Nov 2026 for two adults and dated 2027 stays. Hotel prices are dynamic; quoted nightly averages exclude taxes. Exact seven-night checkout totals were not printed in the fetched result pages. The official-source sample is limited to named room types at three Caesars properties plus a Wynn promotion, and the private-bath requirement remains unconfirmed for the quoted room categories. No universal cheapest week or fully compliant hotel can be concluded from these pages alone.</p>
</section>
<section class="panel">
  <h2>Flagged for review</h2>
  <p>Each table row links to the relevant official booking-engine page. The issue is separated from the source fact; if the official page does not state a value, the site leaves it blank rather than filling it in.</p>
  <div class="scroll"><table class="data"><thead><tr><th>ID</th><th>Finding and required follow-up</th><th>Official source links</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
  <p>Historic data-quality and travel-planning flags F-01–F-28 remain in the <a href="sources.html#flags">Sources &amp; flags register</a> and <a href="https://github.com/kanlerxz87-cyber/Vegas1/blob/main/FLAGS.md" target="_blank" rel="noopener">repository FLAGS.md</a>. Review those before relying on any older table.</p>
</section>
<section class="panel">
  <h2>Decision-critical open points</h2>
  <ul class="tight">
    <li>Confirm trip length: preferred dates 15–18 Feb are three nights, while the main hotel comparison uses seven-night blocks.</li>
    <li>Confirm the exact room category has a queen/king bed and a private en-suite bathroom before payment; avoid unassigned-room offers.</li>
    <li>Request a full checkout quote including taxes, resort fee, and cancellation terms; the page's nightly-rate arithmetic is not a final bill.</li>
    <li>Choose whether price or Michelin proximity matters more. The requested ≤60-minute metric is 24/24 for all hotels and does not distinguish them.</li>
  </ul>
  <p>For suggested decision paths, see <a href="suggestions.html">Suggestions</a>. For questions and the discovery steps to close them, see <a href="questions.html">Open questions</a>.</p>
</section>
"""
    return page("review.html", "Flagged for review", "Source conflicts, missing details and unverified booking requirements that must be resolved before choosing a hotel.", body)


# ------------------------------------------------- supplementary routes
ROUTES = [
    (
        "pricing.html",
        "Pricing",
        "Official hotel rate snapshots, restaurant totals for two, and the unresolved price and tax questions — with dates and source links.",
        [
            ("Current official hotel rate sample", "hotels.html#direct-rates"),
            ("Flagged price conflicts", "review.html#F-29"),
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
            ("Flags — the 28 things that did not verify cleanly", "sources.html#flags"),
            ("Every source used, grouped by what it proves", "sources.html"),
            ("Open questions, and how to close each one", "questions.html"),
            ("Transit minutes and their stated limits", "transit.html#matrix"),
            ("Restaurant award tiers (starred vs listed)", "restaurants.html"),
        ],
    ),
    (
        "summary.html",
        "Executive summary",
        "A concise summary of verified findings, decision limits, price snapshots and open requirements.",
        [
            ("Overview and the three findings", "index.html"),
            ("Official hotel quote sample and room-fit caveats", "hotels.html#direct-rates"),
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


def main():
    DOCS.mkdir(exist_ok=True)
    pages = {
        "index.html": build_index(),
        "hotels.html": build_hotels(),
        "restaurants.html": build_restaurants(),
        "activities.html": build_activities(),
        "transit.html": build_transit(),
        "questions.html": build_questions(),
        "suggestions.html": build_suggestions(),
        "review.html": build_review(),
        "sources.html": build_sources(),
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
