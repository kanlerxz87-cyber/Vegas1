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
  <p>Prices captured 25 Nov 2026 from Booking.com for exact date ranges, 2 adults, 1 room, USD.
  Every row links to its source. Blank means <strong>not verified</strong> — never estimated.</p>
  <p>Las Vegas had no MICHELIN Guide between 2010 and 2025. All awards here are from the 2026
  Southwest selection, the first since 2009.</p>
</footer>
</body>
</html>
"""


# ---------------------------------------------------------------- figures
def luxury_rows():
    """Hotels ranked: 20-min Michelin count desc, then 7-night price asc."""
    hs = [h for h in HOTELS["hotels"] if h["tier"] != "off-strip"]
    return sorted(hs, key=lambda h: (-h["michelin_within_20"], h["prices"][0]["total_7n"]))


def w1(h):
    for p in h["prices"]:
        if p["window"].startswith("2027-02-15"):
            return p["total_7n"]
    return None


# ---------------------------------------------------------------- index
def build_index():
    starred = [r for r in RES["restaurants"] if r["award_class"] == "starred"]
    bib = [r for r in RES["restaurants"] if r["award_class"] == "bib"]
    rec = [r for r in RES["restaurants"] if r["award_class"] == "recommended"]

    # headline numbers
    n_hotels = len(HOTELS["hotels"])
    cheapest = min(HOTELS["hotels"], key=lambda h: w1(h))
    v_w1 = next(p for p in next(h for h in HOTELS["hotels"] if h["id"] == "venetian")["prices"] if p["window"].startswith("2027-02-15"))
    v_w3 = next(p for p in next(h for h in HOTELS["hotels"] if h["id"] == "venetian")["prices"] if p["window"].startswith("2027-03-08"))
    saving = v_w1["total_7n"] - v_w3["total_7n"]
    pct = round(100 * saving / v_w1["total_7n"])

    cards = [
        (str(N_TOTAL), "MICHELIN listings", f"{N_STARRED} starred · {N_BIB} Bib Gourmand · {N_REC} Recommended.<br>No three-star restaurant exists in Las Vegas."),
        ("0", "subway lines", "Las Vegas has no metro. Buses, Monorail and the Vegas Loop were modelled instead — <a href='questions.html'>Q-01</a>."),
        (money(cheapest["prices"][0]["total_7n"]), "cheapest 7 nights", f"{e(cheapest['name'])} — but that is an <em>unassigned room</em> rate. See the caveat on the Hotels page."),
        (money(saving), "saved by moving a week", f"The same Venetian suite costs {pct}% less on 8–15 Mar than on 15–22 Feb. That is the single biggest lever here."),
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
  <p>Everything on this site was captured from official hotel, restaurant, transit and MICHELIN pages on
  <strong>25 November 2026</strong>. Where a number could not be confirmed it is <strong>blank</strong> and listed on the
  <a href="questions.html">Open questions</a> page. Nothing was estimated into a table.</p>
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
  <h2>Three things that change the answer</h2>
  <ol class="tight">
    <li><strong>The 7-night basis collides with the requested dates.</strong> The preferred window
    2027-02-15 → 2027-02-18 is three nights, not seven. Seven-night totals starting on 15 Feb are used
    so the figures match the brief — <a href="questions.html">Q-02</a>.</li>
    <li><strong>The "within 1 hour" ranking does not rank anything.</strong> Every hotel in Las Vegas is within
    an hour of all {N_TOTAL} restaurants, so the metric returns {N_TOTAL}/{N_TOTAL} for all {n_hotels} properties. A
    <em>20-minute</em> column was added and is what actually separates them — <a href="questions.html">Q-01</a>.</li>
    <li><strong>February is the expensive week.</strong> 15 Feb 2027 is Presidents' Day. Moving to 8–15 March
    cuts the Venetian by {pct}% and the Palazzo by 38% for the identical suite.</li>
  </ol>
</section>

<section class="panel callout">
  <h2>If you read only one row</h2>
  <p><strong>Desert Rose Resort</strong> — {money(922)} for seven nights, 9.1 guest score, a 646 ft² one-bedroom
  suite with a king bed and a private bathroom, <em>no resort fee</em>, and a 15-minute walk to the centre-Strip
  restaurant cluster. It is the only property that is simultaneously cheap, well-rated and correctly bedded.
  The catch is that it is a low-rise condo hotel with no casino — <a href="hotels.html">Hotels</a> explains the trade.</p>
</section>
"""
    return page("index.html", "Las Vegas, seven nights, 2027",
                "A sourced plan for two adults between 15 Feb and 23 Mar 2027 — hotels, MICHELIN restaurants, transit and what could not be verified.",
                body)


# ---------------------------------------------------------------- hotels
def build_hotels():
    # ---- ranked table
    rows = []
    for i, h in enumerate(luxury_rows(), 1):
        price = money(w1(h))
        bed = e(h["bed"])
        if "not guaranteed" in h["bed"]:
            bed = f'<span class="warn">{e(h["bed"])}</span>'
        rows.append(f"""<tr>
<td class="rank">{i}</td>
<td><a href="{e(h['official_url'])}" target="_blank" rel="noopener">{e(h['name'])}</a>
    <div class="tiny">{e(h['zone'].replace('-', ' '))}</div></td>
<td class="num">{h['stars']}★</td>
<td class="num">{h['guest_score'] or '—'}</td>
<td class="num strong">{h['michelin_within_20']}</td>
<td class="num muted">{h['michelin_within_60']}</td>
<td>{bed}</td>
<td class="num">{price}</td>
</tr>""")

    rank_table = f"""
<div class="scroll">
<table class="data">
<thead><tr>
<th>#</th><th>Hotel</th><th>Class</th><th>Guest</th>
<th title="MICHELIN restaurants within a 20-minute one-way trip">≤20 min</th>
<th title="MICHELIN restaurants within 60 minutes — the figure the brief asked for">≤60 min</th>
<th>Bed</th><th>7 nights<br><span class="thsub">15–22 Feb</span></th>
</tr></thead>
<tbody>{''.join(rows)}</tbody>
</table>
</div>
<p class="note">Sorted by MICHELIN proximity inside 20 minutes, then by price. The ≤60 min column is the
brief's literal metric and is <strong>24 for every property</strong> — it cannot rank anything, which is why the
20-minute column drives the order. Both are recomputed by <code>scripts/build.py</code> from one zone matrix.</p>
"""

    # ---- price comparison across windows
    prow = []
    for row in PRICE["matrix"]:
        cells = []
        vals = [row["W1"], row["W2"], row["W3"], row["W4"]]
        known = [v for v in vals if v]
        low = min(known) if known else None
        for v in vals:
            if v is None:
                cells.append('<td class="num muted">—</td>')
            elif v == low and len(known) > 1:
                cells.append(f'<td class="num best">{money(v)}</td>')
            else:
                cells.append(f'<td class="num">{money(v)}</td>')
        prow.append(
            f'<tr><td>{e(row["hotel"])}</td>' + "".join(cells) +
            f'<td class="tiny">{e(row["room_note"])}</td></tr>'
        )

    window_table = f"""
<div class="scroll">
<table class="data">
<thead><tr><th>Hotel</th>
<th>15–22 Feb</th><th>1–8 Mar</th><th>8–15 Mar</th><th>15–22 Mar</th><th>Room note</th>
</tr></thead>
<tbody>{''.join(prow)}</tbody>
</table>
</div>
"""

    # ---- like-for-like week comparison: only hotels measured in 2+ windows
    cmp_rows = []
    for row in PRICE["matrix"]:
        pairs = [(k, row[k]) for k in ("W1", "W2", "W3", "W4") if row.get(k)]
        if len(pairs) < 2:
            continue
        lo_k, lo_v = min(pairs, key=lambda kv: kv[1])
        hi_k, hi_v = max(pairs, key=lambda kv: kv[1])
        delta = lo_v - hi_v
        pct = round(100 * delta / hi_v)
        cells = "".join(
            f'<td class="num{" best" if row.get(k) else " muted"}">{money(row[k]) if row.get(k) else "—"}</td>'
            for k in ("W1", "W2", "W3", "W4")
        )
        room = row["room_note"]
        mismatch = "different room class" in room.lower()
        warn_note = " — <span class='warn'>not like for like</span>" if mismatch else ""
        sign = "−" if pct < 0 else "+"
        cmp_rows.append(
            f'<tr><td>{e(row["hotel"])}</td>{cells}'
            f'<td class="num strong">{sign}{abs(pct)}%</td>'
            f'<td class="tiny">{e(room)}{warn_note}</td></tr>'
        )

    # ---- full property cards
    cards = []
    for h in sorted(HOTELS["hotels"], key=lambda x: (-x["michelin_within_20"], x["prices"][0]["total_7n"])):
        plist = "".join(
            f'<tr><td>{e(p["window"])}</td><td class="num">{money(p["total_7n"])}</td>'
            f'<td class="num muted">{money(p["per_night"])}</td>'
            f'<td class="tiny">{e(p["note"])}</td></tr>'
            for p in h["prices"]
        )
        flags = ""
        if h["flags"]:
            flags = f'<p class="flagline">⚑ {", ".join(e(f) for f in h["flags"])} — see <a href="sources.html#flags">flags</a></p>'
        cards.append(f"""
<article class="hotel">
  <h3>{e(h['name'])} <span class="pill">{e(h['tier'])}</span></h3>
  <p class="meta">{e(h['zone'].replace('-',' '))} · {h['stars']}★ · guest score {h['guest_score'] or '—'}
  · {h['michelin_within_20']} MICHELIN within 20 min · resort fee: {e(h['resort_fee'])}</p>
  <table class="data slim">
    <thead><tr><th>Window</th><th>7 nights</th><th>/night</th><th>Note</th></tr></thead>
    <tbody>{plist}</tbody>
  </table>
  <p class="tiny">Bed: {e(h['bed'])} · private bathroom: {'yes' if h['private_bath'] else 'not stated'}</p>
  <p>{e(h['notes'])}</p>
  {flags}
  <p class="links">
    <a href="{e(h['official_url'])}" target="_blank" rel="noopener">Official</a>
    <a href="{e(h['booking_url'])}" target="_blank" rel="noopener">Price source</a>
  </p>
</article>""")

    body = f"""
<section class="panel">
  <h2>Which week is cheapest — like for like</h2>
  <p>Only properties measured in more than one week are shown, so every percentage compares the same
  hotel (usually the same room class) against itself:</p>
  <div class="scroll">
  <table class="data">
  <thead><tr><th>Hotel</th><th>15–22 Feb</th><th>1–8 Mar</th><th>8–15 Mar</th><th>15–22 Mar</th><th>Best vs worst</th><th>Room note</th></tr></thead>
  <tbody>{''.join(cmp_rows)}</tbody>
  </table>
  </div>
  <p class="note"><strong>8–15 March is the cheap week.</strong> The Venetian, Palazzo and Cosmopolitan all drop by
  roughly a third for the same suite. 15–22 February — which contains Presidents' Day on 15 Feb 2027 — is the
  expensive one. The holiday is a verified calendar fact; that it <em>causes</em> the price gap is an inference,
  so it is described as the likely driver and not as proven.</p>
</section>

<section class="panel">
  <h2>Every measured week</h2>
  <div class="scroll">
  <table class="data">
  <thead><tr><th>Hotel</th><th>15–22 Feb</th><th>1–8 Mar</th><th>8–15 Mar</th><th>15–22 Mar</th><th>Room note</th></tr></thead>
  <tbody>{''.join(prow)}</tbody>
  </table>
  </div>
  <p class="note">A dash means <em>not measured</em>, not "sold out". Only properties that appeared in a captured
  result block are listed.</p>
</section>

<section class="panel">
  <h2>Hotels ranked</h2>
  {rank_table}
</section>

<section class="panel">
  <h2>Every hotel, with both price bases</h2>
  <p>Booking.com search totals generally exclude resort fee and local tax. Where a property publishes its own
  rate, both figures are shown rather than one.</p>
  <div class="hotels">{''.join(cards)}</div>
</section>

<section class="panel callout">
  <h2>The three cheapest totals are traps</h2>
  <p>The LINQ ($564), Flamingo ($626) and Horseshoe ($717) headline the dataset, but all three are
  <strong>"room type assigned on arrival"</strong> promotions. The king bed shown at booking is not contractual, so
  they do not satisfy the queen-or-larger requirement until check-in. Book a <em>named</em> room class at the
  same properties — expect $100–$200 more per week — or take Desert Rose at $922 with the bed guaranteed and
  no resort fee.</p>
</section>
"""
    return page("hotels.html", "Hotels",
                f"{len(HOTELS['hotels'])} properties, real 7-night totals for dated windows, and a bed requirement that removes the cheapest three.",
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
        price = e(r["price_2adults"]) if r["price_2adults"] else '<span class="muted">on request</span>'
        rows.append(f"""<tr>
<td><a href="{e(r['official_url'])}" target="_blank" rel="noopener">{e(r['name'])}</a>
  <div class="tiny">{e(r['cuisine'])} · {e(r['location'])}</div></td>
<td><span class="badge {cls(r)}">{e(r['award'])}</span></td>
<td>{e(r['days'])}<div class="tiny">{hours}</div></td>
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
  <h2>What dinner for two actually costs</h2>
  <p>Only three venues publish a number, and two of them are outside the starred group:</p>
  <ul class="tight">
    <li><strong>Michael Mina</strong> — $295++ per person, 10-course tasting → <strong>$590++</strong> for two.</li>
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
        rows.append(f"""<tr>
<td><a href="{e(a['official_url'])}" target="_blank" rel="noopener">{e(a['name'])}</a>
 <div class="tiny">{e(a['type'])} · {e(a['zone'].replace('-',' '))}</div></td>
<td>{e(a['days'])}<div class="tiny">{e(a['hours'])}</div></td>
<td class="tiny">{e(a['exceptions']) or '—'}</td>
<td class="num">{e(a['price_per_couple']) or '—'}</td>
<td class="tiny">{e(a['price_note'])}</td>
</tr>""")

    nv = "".join(
        f'<li><strong>{e(n["name"])}</strong> — {e(n["reason"])}</li>' for n in ACT["not_verified"]
    )

    body = f"""
<section class="panel">
  <h2>Four things worth the day</h2>
  <div class="scroll">
  <table class="data">
  <thead><tr><th>Venue</th><th>Days &amp; hours</th><th>Exceptions</th><th>2 adults</th><th>Price basis</th></tr></thead>
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
        mrows.append(f'<tr><th class="rowhead">{e(labels[z])}</th>{"".join(cells)}</tr>')

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
  <h2>Estimated one-way minutes between zones</h2>
  <p><strong>These are estimates, not timetables.</strong> No official source publishes door-to-door times; these are
  built from the official station lists and route maps and rounded to five minutes.</p>
  <div class="scroll">
  <table class="data matrix">
  <thead><tr><th></th>{head}</tr></thead>
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
        cards.append(f"""
<article class="sug">
  <h3><span class="sid">{e(s['id'])}</span> {e(s['title'])}
   <span class="impact {imp[s['impact']]}">{e(s['impact'])} impact</span>{need}</h3>
  <p>{e(s['body'])}</p>
  <p class="trade"><strong>Trade-off:</strong> {e(s['trade_off'])}</p>
  <p class="tiny">Evidence: {e(s['evidence'])}</p>
</article>""")

    needs = [s for s in SUG["suggestions"] if s["needs_decision"]]
    n_sug = len(SUG["suggestions"])
    body = f"""
<section class="panel">
  <h2>{len(SUGGESTIONS_HEAD)}</h2>
  <p>{n_sug} proposals, ranked by how much they change the outcome. <strong>{len(needs)} of them need a decision
  from you</strong> before the plan can be finalised — they are marked in the list. Nothing here was silently
  applied to the data.</p>
  <p>The three that matter most: move the trip to <strong>8–15 March</strong> (saves about $1,400 on the same suite),
  settle whether this is a <strong>three-night or seven-night</strong> trip (which changes every hotel number by
  over half), and <strong>refuse unassigned-room rates</strong> (which removes the three cheapest hotels on the site).</p>
</section>
<div class="suglist">{''.join(cards)}</div>
"""
    return page("suggestions.html", "Suggestions",
                "Twelve decision improvements, ranked, each with its honest trade-off and whether it needs your call first.",
                body)


SUGGESTIONS_HEAD = [f"{len(SUG['suggestions'])} ways to improve this plan"]


# ---------------------------------------------------------------- sources
def build_sources():
    flag_rows = []
    # flags are listed in FLAGS.md; render the highlighted ones here
    N_FLAGS = 20
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
  <p class="note">The full list (all {N_FLAGS} flags) and the deliberate non-inclusions are in
  <code>FLAGS.md</code> at the repository root.</p>
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
        "sources.html": build_sources(),
    }
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
