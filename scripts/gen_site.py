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
  </div>
  {body}
</main>
<footer class="wrap">
  <p>Prices captured 25 Nov 2026 from Booking.com for exact date ranges, 2 adults, 1 room, USD; spot-checked 26 Nov 2026 (see <a href="flagged.html">Flagged for review</a>).
  Every row links to its source. Blank means <strong>not verified</strong> — never estimated.</p>
  <p>Las Vegas had no MICHELIN Guide between 2010 and 2025. All awards here are from the 2026
  Southwest selection, the first since 2009.</p>
</footer>
</body>
</html>
"""


# ---------------------------------------------------------------- figures
def first_total(h):
    """First captured 7-night total; inf when withdrawn or missing, so it sorts last."""
    for p in h["prices"]:
        if p.get("total_7n") is not None:
            return p["total_7n"]
    return float("inf")


def luxury_rows():
    """Hotels ranked: 20-min Michelin count desc, then 7-night price asc."""
    hs = [h for h in HOTELS["hotels"] if h["tier"] != "off-strip"]
    return sorted(hs, key=lambda h: (-h["michelin_within_20"], first_total(h)))


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
    cheapest = min((h for h in HOTELS["hotels"] if w1(h) is not None), key=lambda h: w1(h))

    cards = [
        (str(N_TOTAL), "MICHELIN listings", f"{N_STARRED} starred · {N_BIB} Bib Gourmand · {N_REC} Recommended.<br>No three-star restaurant exists in Las Vegas."),
        ("0", "subway lines", "Las Vegas has no metro. Buses, Monorail and the Vegas Loop were modelled instead — <a href='questions.html'>Q-01</a>."),
        (money(w1(cheapest)), "lowest OTA quote", f"{e(cheapest['name'])} — a Booking.com snapshot with an <em>unassigned room</em>, not a confirmed official-property rate. See Hotels and Flags."),
        ("Unproven", "saving from moving a week", "The 36% figure was <em>withdrawn</em> after a live check did not reproduce it (F-39). <a href='questions.html#Q-06'>Q-06</a>."),
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
  <p>Hotel, restaurant, transit and MICHELIN venue details were captured from official pages on
  <strong>25 November 2026</strong>. The main hotel-rate comparison is an explicitly labelled <strong>Booking.com snapshot</strong>, not a hotel-issued quote; a separate sample of official property engines conflicts for some date comparisons. Where a value could not be confirmed from its stated source it is blank and flagged on the <a href="sources.html#flags">Sources &amp; flags</a> page. Transit times are labelled estimates, not official running times.</p>
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
  <h2 id="three-things">Four things that change the answer</h2>
  <ol class="tight">
    <li><strong>The 7-night basis collides with the requested dates.</strong> The preferred window
    2027-02-15 → 2027-02-18 is three nights, not seven. Seven-night totals starting on 15 Feb are used
    so the figures match the brief — <a href="questions.html">Q-02</a>.</li>
    <li><strong>The "within 1 hour" ranking does not rank anything.</strong> Every hotel in Las Vegas is within
    an hour of all {N_TOTAL} restaurants, so the metric returns {N_TOTAL}/{N_TOTAL} for all {n_hotels} properties. A
    <em>20-minute</em> column was added and is what actually separates them — <a href="questions.html">Q-01</a>.</li>
    <li><strong>One ranked hotel no longer exists under the name this site priced.</strong> The official page for
    The Cromwell now redirects to <strong>The Vanderpump Hotel</strong>, so that row's $1,978 total is a
    Cromwell-era number and must be re-quoted before it is used — <a href="flagged.html#F-47">F-47</a>.</li>
    <li><strong>The cheapest week is not settled across sources.</strong> The 25 Nov Booking.com snapshots showed lower March quotes for some large resorts, but the Venetian figure was withdrawn on 26 Nov (<a href="flagged.html">F-39</a>). A separate 25 Nov sample of official booking engines found the preferred 15–22 February week cheapest at properties checked. The samples are not like-for-like. Compare exact dates and named-room terms at the hotel's own booking engine before moving dates — <a href="questions.html#Q-06">Q-06</a>.</li>
  </ol>
</section>

<section class="panel callout">
  <h2>If you read only one row</h2>
  <p><strong>Desert Rose Resort is a value candidate, not a confirmed best buy.</strong> The displayed $922 seven-night
  figure is a Booking.com snapshot, not an official property rate. Its room/bed and bathroom fit are described on the
  hotel's official page, but the total must be rechecked with the property before it can support a final decision.
  It is a low-rise condo hotel with no casino, one block off the Strip — see the <a href="hotels.html">hotel page</a>,
  source flags, and the <a href="https://kanlerxz87-cyber.github.io/Vegas1/docs/session-af795000/hotels.html">official-engine sample</a>.</p>
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
<th>Bed</th><th>Booking.com quote<br><span class="thsub">7 nights · 15–22 Feb</span></th>
</tr></thead>
<tbody>{''.join(rows)}</tbody>
</table>
</div>
<p class="note">Sorted by MICHELIN proximity inside 20 minutes, then by the dated Booking.com quote (not an official property rate). The ≤60 min column is the
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
    for h in sorted(HOTELS["hotels"], key=lambda x: (-x["michelin_within_20"], first_total(x))):
        plist = "".join(
            f'<tr><td>{e(p["window"])}</td><td class="num">{money(p["total_7n"])}</td>'
            f'<td class="num muted">{money(p["per_night"])}</td>'
            f'<td class="tiny">{e(p["note"])}</td></tr>'
            for p in h["prices"]
        )
        ov = h.get("official_verified")
        if ov == "yes":
            unverified = ""
        elif ov == "blocked":
            unverified = '&nbsp;<span class="tinymuted">(opened 26 Nov 2026 — the site refuses automated access)</span>'
        elif ov == "sibling":
            unverified = (
                '&nbsp;<span class="tinymuted">(this URL lands on the parent property’s page, '
                "not this property's own)</span>"
            )
        else:
            unverified = '&nbsp;<span class="tinymuted">(not fetched — may have moved)</span>'
        ps_label = (
            "Price source — dated search list, not a room quote"
            if h.get("price_basis") == "search-list"
            else "Price source ✓"
        )
        flags = ""
        if h["flags"]:
            fl = " · ".join(f'<a href="flagged.html#{f}">{f}</a>' for f in h["flags"])
            flags = f'<p class="flagline">⚑ {fl}</p>'
        cards.append(f"""
<article class="hotel">
  <h3>{e(h['name'])} <span class="pill">{e(h['tier'])}</span></h3>
  <p class="meta">{e(h['zone'].replace('-',' '))} · {h['stars']}★ · guest score {h['guest_score'] or '—'}
  · {h['michelin_within_20']} MICHELIN within 20 min · resort fee: {e(h['resort_fee'])}</p>
  <table class="data slim">
    <thead><tr><th>Window</th><th>Booking.com quote · 7 nights</th><th>/night</th><th>Note</th></tr></thead>
    <tbody>{plist}</tbody>
  </table>
  <p class="tiny">Bed: {e(h['bed'])} · private bathroom: {'yes' if h['private_bath'] else 'not stated'}
   {('· ' + e(h['address'])) if h.get('address') else ''}</p>
  <p>{e(h['notes'])}</p>
  {flags}
  <p class="links">
    <a href="{e(h['official_url'])}" target="_blank" rel="noopener">Official</a>{unverified}
    <a href="{e(h['booking_url'])}" target="_blank" rel="noopener">{ps_label}</a>
  </p>
</article>""")

    body = f"""
<section class="panel">
  <h2 id="cheapest-week">Which week had the lower Booking.com quote — selected pairs only</h2>
  <p>Only properties measured in more than one Booking.com date window are shown. Where room classes match, each comparison is within the same hotel; these third-party snapshots do not establish official rates or a market-wide cheapest week:</p>
  <div class="scroll">
  <table class="data">
  <thead><tr><th>Hotel</th><th>15–22 Feb</th><th>1–8 Mar</th><th>8–15 Mar</th><th>15–22 Mar</th><th>Best vs worst</th><th>Room note</th></tr></thead>
  <tbody>{''.join(cmp_rows)}</tbody>
  </table>
  </div>
  <p class="note"><strong>Not settled.</strong> The 25 Nov captures suggested 8–15 March is cheaper for the big resorts.
  On 26 Nov, Booking.com's own Venetian page showed the same 60 m² suite at US$5,185 for 15–22 Feb and €4,472 for
  8–15 Mar, both including taxes and fees, so the stored Venetian figures are withdrawn (F-39). The other rows
  are not reproduced (F-44). Presidents' Day (15 Feb 2027) is a verified calendar fact; whether it moves prices is not
  established. See <a href="questions.html#Q-06">Q-06</a> for how to close it.</p> Compare the exact named room, fees, taxes, cancellation terms and dates on each property's own booking page before booking.</p>
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
  <h2 id="every-hotel">Every hotel — dated Booking.com quote snapshots</h2>
  <p>These are third-party Booking.com search totals, generally excluding resort fees and local tax; they are not official property-engine quotes. The <a href="https://kanlerxz87-cyber.github.io/Vegas1/docs/session-af795000/hotels.html">separate official-engine sample</a> covers only selected properties/dates and has a different fee/tax basis. Do not combine these datasets or read them as a verified market-wide rate ranking.</p>
  <p class="note"><strong>Link honesty, after the 26 Nov 2026 re-check:</strong> <strong>18 of the 32</strong>
  "Official" links were opened and returned the property's own page; <strong>8 refused automated access</strong>
  from this environment (Crockfords returned HTTP 500) and are marked <em>refuses automated access</em> —
  refused, not broken; <strong>5 were not opened</strong> and keep <em>not fetched — may have moved</em>. One link (Nobu at Caesars) opens but lands on the parent property's page.
  A "Price source" link is the Booking.com URL the number came from; where that URL is a dated search-results list
  rather than the property's own quote page, the card says so — the link then proves the search, not the room.</p>
  <div class="hotels">{''.join(cards)}</div>
</section>

<section class="panel callout">
  <h2>Lowest Booking.com quotes: bed and source caveats</h2>
  <p>The LINQ ($564), Flamingo ($626) and Horseshoe ($717) headline the third-party snapshot, but each lowest rate is a
  <strong>"room type assigned on arrival"</strong> promotion. The bed is not guaranteed at booking, so these rates do not
  establish the requested queen-or-larger room fit. Named-room direct rates need to be checked on each property's
  official booking engine; no $100–$200 uplift is assumed. The separate official-engine sample includes some named-room
  alternatives and direct links, but does not establish a universal cheapest hotel.</p>
</section>
"""
    return page("hotels.html", "Hotels",
                f"{len(HOTELS['hotels'])} properties with dated Booking.com 7-night quote snapshots (not official hotel rates), room-fit flags, and a separate official-engine sample.",
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
        yt = " · ".join(f'<a href="{e(u)}" target="_blank" rel="noopener">video {i+1}</a>' for i, u in enumerate(a.get("youtube", []))) or '<span class="muted">—</span>'
        ig = f'<a href="{e(a["instagram"])}" target="_blank" rel="noopener">Instagram</a>' if a.get("instagram") else '<span class="muted">—</span>'
        tt = f'<a href="{e(a["tiktok"])}" target="_blank" rel="noopener">TikTok</a>' if a.get("tiktok") else '<span class="muted">—</span>'
        rows.append(f"""<tr>
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

    body = f"""
<section class="panel">
  <h2>{len(ACT['activities'])} activities</h2>
  <div class="scroll">
  <table class="data">
  <thead><tr><th>Venue</th><th>Days &amp; hours</th><th>Exceptions</th><th>2 adults</th><th>Price basis</th><th>YouTube</th><th>Instagram</th><th>TikTok</th></tr></thead>
  <tbody>{''.join(rows)}</tbody>
  </table>
  </div>
  <p class="note">Social columns show only links present in the dataset; <strong>— means no link was verified for this entry</strong>, not that the venue has no account or video. See <a href="questions.html">Open questions</a> for discovery gaps.</p>
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
                f"{len(ACT['activities'])} verified activity entries with official hours/prices where published, plus explicit blanks where no official social profile was verified.",
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
  <h2>Correction: Chinatown is reachable by bus</h2>
  <p>An earlier version of this matrix recorded Chinatown / Spring Mountain Rd as reachable only by car or
  rideshare. <strong>That was wrong.</strong> RTC <strong>Route 203</strong> runs the length of Spring Mountain Road,
  and its published timetable carries a timed stop at <strong>Las Vegas Blvd</strong> — the north end of the Strip,
  where Wynn, Encore, Resorts World and SAHARA are.</p>
  <p>This matters more than any other single number on this site, because <strong>seven of the 24 MICHELIN listings
  sit within a few blocks of that one corridor</strong>: Partage, Kabuto, KAME Omakase, Lamaii, Sparrow + Wolf
  and Pho Ga Bac Bac on Spring Mountain Road itself, plus Yen Viet Kitchen at 3575 S. Decatur Blvd — a published
  Route 203 timepoint. Nearly a third of the guide is on a road that turns out to have a bus.</p>
  <p>The sampled timetable runs give <strong>Decatur to Las Vegas Blvd in about 8–17 minutes, depending on direction, day and time</strong> (weekday eastbound 10–17; Saturday westbound 8–9) (14 is the model midpoint; F-42). Adding a walk to the
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
"""
    return page("suggestions.html", "Suggestions",
                "Twelve decision improvements, ranked, each with its honest trade-off and whether it needs your call first.",
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
        ("Restaurants with an Instagram link", n_ig, "none recorded in the data (F-19)"),
        ("Restaurants with a TikTok link", n_tt, "none recorded in the data (F-19)"),
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
            ("Selected Booking.com date comparisons (not a market-wide result)", "hotels.html#cheapest-week"),
            ("Every hotel, with both price bases", "hotels.html#every-hotel"),
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
            ("Hotels ranked, and the three cheapest traps", "hotels.html"),
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
        "flagged.html": build_flagged(),
        "sources.html": build_sources(),
        "repo-review.html": build_repo_review(),
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
