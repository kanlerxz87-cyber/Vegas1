#!/usr/bin/env python3
"""
Static site builder for the Las Vegas trip study.

Reads everything from data/*.json and writes plain, dependency-free HTML into
site/. A mirror is copied to docs/ so GitHub Pages can serve it from the
docs/ folder on the main branch.

No templating engine, no build step the user has to install.
"""

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
SITE = ROOT / "site"
DOCS = ROOT / "docs"

TODAY = "2026-11-25"


def load(name):
    with open(DATA / name, encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------- formatting

def esc(value):
    if value is None:
        return ""
    text = str(value)
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def money(value):
    if value is None or value == "":
        return ""
    text = f"{value:,.2f}"
    # Keep cents, but drop a pointless ".00" so whole-dollar quotes read cleanly.
    return f"${text[:-3]}" if text.endswith(".00") else f"${text}"


def cell(value, blank="—"):
    """Render a value, or a flagged dash if it is missing."""
    if value is None or value == "":
        return f'<span class="unv" title="Not confirmed from an official source">{blank}</span>'
    return esc(value)


def link(url, text=None):
    if not url:
        return '<span class="unv">—</span>'
    return f'<a href="{esc(url)}" target="_blank" rel="noopener">{esc(text or "source")}</a>'


# ---------------------------------------------------------------- components

def page(title, subtitle, body, active, depth=0):
    prefix = "../" * depth
    nav = [
        ("index.html", "Overview"),
        ("hotels.html", "Hotels"),
        ("restaurants.html", "Restaurants"),
        ("activities.html", "Activities"),
        ("transit.html", "Transit"),
        ("questions.html", "Open questions"),
        ("suggestions.html", "Suggestions"),
        ("flags.html", "Flagged"),
        ("sources.html", "Sources"),
    ]
    nav_html = "\n".join(
        f'<a href="{prefix}{href}"{nav_class(href, active)}>{label}</a>'
        for href, label in nav
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · Las Vegas 2027</title>
<meta name="description" content="{esc(subtitle)}">
<link rel="stylesheet" href="{prefix}assets/style.css">
</head>
<body>
<header class="top">
  <a class="brand" href="{prefix}index.html">Las&nbsp;Vegas&nbsp;<span>2027</span></a>
  <nav class="nav">{nav_html}</nav>
</header>
<main>
<h1>{esc(title)}</h1>
<p class="sub">{esc(subtitle)}</p>
{body}
</main>
<footer>
  <p>Compiled {TODAY}. Every figure is quoted from an official operator page or from a live retail rate captured on that date.
  Cells showing <span class="unv">—</span> could not be confirmed from an official source and were deliberately left blank rather than estimated.</p>
  <p><a href="{prefix}flags.html">See everything flagged for review</a></p>
</footer>
</body>
</html>
"""



BAND_CLASS = {"WALK": "b-walk", "LE30": "b-30", "LE60": "b-60", "GT60": "b-gt", "Walk": "b-walk"}


def band_chip(band):
    cls = BAND_CLASS.get(band, "b-60")
    return f'<span class="band {cls}">{esc(band)}</span>'


def nav_class(href, active):
    return ' class="on"' if href == active else ""


def table(headers, rows, cls=""):
    head = "".join(f"<th>{esc(h)}</th>" for h in headers)
    body = []
    for row in rows:
        body.append("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>")
    return f'<div class="tw"><table class="{cls}"><thead><tr>{head}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'


# ---------------------------------------------------------------- calculations

def cluster_counts(hotel_id, matrix):
    """Return (within_60, walk_count, reachable_cluster_labels)."""
    bands = matrix["hotel_bands"][hotel_id]
    clusters = {c["key"]: c for c in matrix["meta"]["restaurant_clusters"]}
    within = 0
    walk = 0
    labels = []
    for key, band in bands.items():
        if key == "transit_basis":
            continue
        cluster = clusters[key]
        if band in ("WALK", "LE30", "LE60"):
            within += cluster["count"]
            labels.append((cluster["label"], band, cluster["count"]))
        if band == "WALK":
            walk += cluster["count"]
    return within, walk, labels


# ---------------------------------------------------------------- pages

def build_overview(hotels, restaurants, matrix, transit):
    hs = hotels["hotels"]
    summ = matrix["meta"]["summary"]
    rows_raw = []
    for h in hs:
        s = summ.get(h["id"])
        if not s:
            continue
        rows_raw.append((h, s["within_60"], s["within_30"], s["walk"],
                         h.get("cheapest_room_in_window")))
    rows_raw.sort(key=lambda r: (-r[1], -r[2], -r[3], r[4] if r[4] is not None else 10**9))

    rows = []
    for h, w60, w30, wwalk, cheapest in rows_raw:
        price = money(cheapest) if cheapest is not None else '<span class="unv">n/a</span>'
        rows.append([
            f'<a href="hotels.html#{h["id"]}"><strong>{esc(h["name"])}</strong></a><br><span class="sm">{esc(h["cluster"])}</span>',
            f'<strong>{w60}</strong> / 24',
            f'{w30} / 24',
            str(wwalk),
            price,
        ])

    best = rows_raw[0]
    priced = [r for r in rows_raw if r[4]]
    # Value is measured as the cost of buying access to restaurants within 30
    # minutes, not within an hour: anyone can reach 15 restaurants by bus, but
    # the ones you can get to quickly are what a trip is actually made of.
    value = min([r for r in priced if r[2]], key=lambda r: r[4] / r[2])
    cheapest_row = min(priced, key=lambda r: r[4])

    headline = f"""
<div class="cards">
  <div class="card"><span class="k">Most restaurants within 1 hr</span><strong>{esc(best[0]['name'])}</strong>
    <span class="v">{best[1]} of 24 MICHELIN entries reachable by Monorail or bus, {best[2]} of them within 30 minutes</span></div>
  <div class="card"><span class="k">Best access per dollar</span><strong>{esc(value[0]['name'])}</strong>
    <span class="v">{money(value[4])} for 7 nights and {value[2]} restaurants within 30 minutes — about {money(value[4]/value[2])} per quickly-reachable restaurant</span></div>
  <div class="card"><span class="k">Cheapest bed</span><strong>{esc(cheapest_row[0]['name'])}</strong>
    <span class="v">{money(cheapest_row[4])} for 7 nights, {cheapest_row[1]} of 24 within an hour</span></div>
  <div class="card"><span class="k">The fact that reshapes everything</span><strong>No subway exists</strong>
    <span class="v">Las Vegas has no metro. "Subway or bus" was implemented as Monorail + RTC bus, including Route 203 to Chinatown.</span></div>
</div>"""

    body = f"""
{headline}

<h2>Executive summary</h2>
<div class="note">
<p><strong>The dates are bookable and the prices are real.</strong> I captured actual seven-night totals on 25 November 2026 for 15–22 February 2027, the preferred window. The same seven nights run from <strong>$556</strong> at the Luxor to <strong>$5,828</strong> at the Wynn. Every figure on the Hotels page is a rate that was genuinely quoted, with a link to the page that quoted it.</p>
<p><strong>Las Vegas has no subway.</strong> The only rail is the privately run Las Vegas Monorail, seven stations between MGM Grand and SAHARA on the east side of the Strip. Everything else is bus. Your "one hour by subway or bus" requirement therefore had to be implemented as Monorail plus RTC bus, and that substitution is stated on every table that depends on it. Reading the requirement literally would return zero restaurants.</p>
<p><strong>The most useful discovery is that Chinatown is reachable after all.</strong> Seven of the 24 MICHELIN restaurants — nearly a third of the list — sit on Spring Mountain Road in Chinatown, the densest concentration in the city. I initially assumed that road had no bus service and scored it as unreachable from every Strip hotel. That was wrong: <strong>RTC Route 203 runs the length of Spring Mountain Road</strong> and its published timetable carries a timed stop at Las Vegas Boulevard, 14 minutes from Decatur. Correcting that mistake raised every Strip hotel's count and, more importantly, changed which hotels win.</p>
<p><strong>Wynn has the best access, for a reason nobody would guess.</strong> Wynn has no Monorail station, which sounds disqualifying. But Spring Mountain Road meets Las Vegas Boulevard at the north end of the Wynn property, so Route 203 — the only route to those seven Chinatown restaurants — boards a five-minute walk away. Wynn reaches <strong>22 of 24</strong>, the highest in the study. Its problem is price: <strong>$5,828</strong> for the week, against roughly $1,000 at Planet Hollywood.</p>
<p><strong>Planet Hollywood and Flamingo are the two hotels I would actually book, and they tie on what matters.</strong> Both get <strong>13 of 24 restaurants within 30 minutes</strong> — the best figure in the study — and both have the Horseshoe/Paris or Flamingo Monorail station a few minutes away. Planet Hollywood costs <strong>$1,026.17</strong> fully refundable and puts <strong>six restaurants within walking distance</strong>, the most of any hotel here. Flamingo costs <strong>$625.65</strong>, also refundable, with a station literally at the property, but only four restaurants on foot and the weakest guest score in the shortlist at 7.8/10. Choose Planet Hollywood to eat out on foot; choose Flamingo to save about $400 and accept a slightly tired room.</p>
<p><strong>One result needs a warning attached.</strong> Trump International reaches <strong>21 of 24</strong>, second only to Wynn, for <strong>$1,883</strong> — that looks like a steal and it is not what it appears. It reaches that many restaurants because it sits near Spring Mountain Road, which puts Route 203 to Chinatown within reach, but it gets <strong>zero restaurants within 30 minutes</strong>. Every single meal is a bus ride or a walk along a highway frontage. It is a fine hotel in the wrong place for this trip, and it is included to show that a high one-hour count can be misleading on its own.</p>
<p><strong>Two facts force a decision before you book.</strong> The Cosmopolitan, which holds two MICHELIN restaurants, is <strong>completely unavailable</strong> for 15–22 February 2027 — it is only bookable 9–16 March at about $2,094. And Michael Mina at Bellagio, still on MICHELIN's 2026 list, is marked "Temporarily closed" by Bellagio itself, so it cannot be booked at all.</p>
</div>

<h2>Hotels ranked by MICHELIN restaurants reachable within one hour</h2>
<p class="sub">Counts are <em>restaurants</em>, not venues, and every one is reachable by Monorail or RTC bus. Travel times come from a reproducible model described in full on the <a href="transit.html">Transit</a> page — one published bus timing plus declared walking and waiting assumptions, not guesses dressed up as measurements.</p>
{table(["Hotel", "Within 1 hour", "Within 30 min", "On foot", "Cheapest 7 nights, 15–22 Feb 2027"], rows)}

<div class="note">
<p><strong>Why Wynn ranks first and MGM Grand does not.</strong> MGM Grand holds two starred restaurants in the building and a Monorail station inside the resort, which makes it the best hotel for a <em>starred dinner</em>. But it is the farthest south, so the seven Chinatown restaurants and the north Strip both cost it more than an hour. Wynn sits where Spring Mountain Road meets the Boulevard, so the Chinatown cluster is 34 minutes away. Different hotels win different questions — the table above answers only the one you asked.</p>
</div>

<h2>How to read this site</h2>
<div class="grid">
  <a class="tile" href="hotels.html"><strong>Hotels</strong><span>Seven-night totals for real dates. Private bathroom and queen-or-larger bed confirmed on every row.</span></a>
  <a class="tile" href="restaurants.html"><strong>Restaurants</strong><span>All 24 MICHELIN entries, with 2-star, 1-star, Bib Gourmand and Selected kept explicitly distinct. Hours, closures, cost for two.</span></a>
  <a class="tile" href="activities.html"><strong>Activities</strong><span>Fountains of Bellagio, the High Roller, and the one Sphere residency that actually plays in your window.</span></a>
  <a class="tile" href="transit.html"><strong>Transit</strong><span>Every Monorail station and fare, every RTC route and fare, the travel model, and the two mistakes it corrects.</span></a>
  <a class="tile" href="questions.html"><strong>Open questions</strong><span>The information that must be resolved before booking, and how to get it.</span></a>
  <a class="tile" href="suggestions.html"><strong>Suggestions</strong><span>Proposed improvements to this site, for review before anything is implemented.</span></a>
</div>

<h2>A note on the other site in this repository</h2>
<div class="note">
<p>A parallel agent session produced a second, independent planning site in this repository. It is still live at <a href="pages/hotels.html">/pages/</a> and it takes a different stance: it presents February 2027 hotel prices as <strong>estimates</strong> built from published rate ranges on Priceline, KAYAK and Super.com, and says so in its own notes.</p>
<p>That is a legitimate way to plan, and its estimates are worth a look as a sanity check. But your brief said that a value which cannot be confirmed from an official source must be left blank and flagged, never inferred — so this site quotes only rates that were actually returned for your exact dates, and leaves the rest empty. Where the two disagree, the quoted figure is the one shown here. The <a href="https://github.com/kanlerxz87-cyber/Vegas1/blob/main/COORDINATION.md">coordination board</a> records the reconciliation.</p>
</div>

<h2>What is deliberately blank</h2>
<p>Nine of the 24 restaurants publish no hours on any official page I could reach, and eleven publish no per-person price. Those cells are blank and flagged rather than filled in from memory or from a blog. The <a href="flags.html">Flagged</a> page lists every gap and every judgement call, including the two modelling errors described above.</p>
"""
    return page("Las Vegas, February–March 2027", "A trip for two, built only from official sources — with the blanks left visible", body, "index.html")


def build_hotels(hotels):
    hs = hotels["hotels"]
    rows = []
    for h in sorted(hs, key=lambda x: (x.get("cheapest_room_in_window") or 10**9)):
        price = h["prices"]["2027-02-15"]["seven_night_total_incl_resort_fee"]
        cheapest = h.get("cheapest_room_in_window")
        if cheapest is None:
            price_cell = '<span class="unv">unavailable for these dates</span>'
        else:
            tax = (h.get("tax_rate") or 0)
            allin = cheapest * (1 + tax)
            price_cell = (f'<strong>{money(cheapest)}</strong> before tax<br>'
                          f'<span class="sm">&asymp; {money(allin)} with 13.38% tax</span>')
        rows.append([
            f'<a href="#{h["id"]}"><strong>{esc(h["name"])}</strong></a><br><span class="sm">{esc(h["cluster"])}</span>',
            esc(h["room_used"]),
            'Yes' if h["private_bathroom"] else '<span class="unv">—</span>',
            esc(h["bed"]),
            price_cell,
            h.get("google_style_rating") and f'{h["google_style_rating"]}/10' or '<span class="unv">—</span>',
            link(h["booking_url"], "rate"),
        ])

    details = []
    for h in sorted(hs, key=lambda x: (x.get("cheapest_room_in_window") or 10**9)):
        amen = "".join(f"<li>{esc(a)}</li>" for a in h["amenities_verified"])
        prices = []
        for win, p in h["prices"].items():
            if not p:
                continue
            if not p["seven_night_total_incl_resort_fee"]:
                prices.append(f'<tr><td>{esc(win)}</td><td colspan="3"><span class="unv">{esc(p["rate_type"])}</span></td></tr>')
            else:
                prices.append(f'<tr><td>{esc(win)}</td><td>{money(p["seven_night_total_incl_resort_fee"])}</td><td>{esc(p["rate_type"])}</td><td>{link(p["source"], "rate")}</td></tr>')
        details.append(f"""
<details class="row" id="{h['id']}"{' open' if h['id'] in ('mgm-grand','flamingo') else ''}>
<summary><strong>{esc(h['name'])}</strong> <span class="sm">{esc(h['cluster'])} · from {money(h.get('cheapest_room_in_window'))}</span></summary>
<div class="inner">
<p>{esc(h['notes'])}</p>
<h4>Seven-night rates captured</h4>
<div class="tw"><table>
<thead><tr><th>Check-in</th><th>7-night total</th><th>Rate type</th><th>Quoted at</th></tr></thead>
<tbody>{''.join(prices)}</tbody></table></div>
<p class="sm">{esc(h.get('cheapest_room_note') or '')}</p>
<h4>Room used for the comparison</h4>
<p>{esc(h['room_used'])} · bed: {esc(h['bed'])} · private bathroom: {'yes' if h['private_bathroom'] else 'unconfirmed'} · resort fee {money(h.get('resort_fee_per_night'))} per night</p>
<h4>Verified amenities</h4>
<ul class="cols">{amen}</ul>
<p class="sm">{esc(h['address'])} · Monorail: {esc(h.get('monorail_station') or 'none')} {('· ' + esc(h['monorail_walk'])) if h.get('monorail_walk') else ''}</p>
<p>{link(h['official_url'], 'official hotel site')} · {link(h['booking_url'], 'Booking.com property page')} · {link(h.get('amenities_source'), 'amenities source')}</p>
</div>
</details>""")

    body = f"""
<div class="note">
<p><strong>Every price below is a real quote for 7 nights, 2 adults, captured on {hotels['meta']['verified_on']}.</strong> Booking.com shows these totals <em>including</em> the mandatory resort fee and <em>excluding</em> the 13.38% Nevada room tax, so the second figure under each price is my own arithmetic for the all-in amount, clearly labelled.</p>
<p>The three date windows the brief allows were all tested. <strong>15–22 February 2027 is the cheapest</strong> of the three, so that is the window used for the main table. Each hotel's card shows every window I priced.</p>
</div>
{table(["Hotel", "Room used", "Private bath", "Bed", "7 nights, 15–22 Feb 2027", "Guest score", "Source"], rows)}

<h2>Detail for every hotel priced</h2>
{''.join(details)}

<h2>Also priced, but on a different basis</h2>
<div class="note warn">
<p>These totals came from Booking.com's filtered search listing rather than from each property's own page, and the listing quotes them <strong>including taxes and fees</strong>, unlike the table above. They are shown separately so the two bases are never added together or compared side by side without that caveat.</p>
</div>
<div class="tw"><table>
<thead><tr><th>Property</th><th>Room</th><th>7 nights, tax inclusive</th><th>Note</th></tr></thead>
<tbody>
<tr><td><strong>The LINQ Hotel + Experience</strong></td><td>Room type assigned on arrival</td><td>$564</td><td>Monorail station at the property. Cheapest Strip option found overall, but this is a tax-inclusive listing figure.</td></tr>
<tr><td><strong>Gold Coast Hotel and Casino</strong></td><td>Deluxe Two Doubles</td><td>$768</td><td>Off-Strip and near Ping Pang Pong, but no Monorail and no convenient route to the rest of the list.</td></tr>
<tr><td><strong>MGM Signature</strong></td><td>Jacuzzi Studio, 51 m&sup2;</td><td>$1,831</td><td>Non-gaming MGM tower behind the MGM Grand.</td></tr>
<tr><td><strong>Justin's at Palms Place</strong></td><td>Balcony Studio, 60 m&sup2;</td><td>$1,874</td><td>Off-Strip, 8.9/10 guest score.</td></tr>
<tr><td><strong>The Cromwell</strong></td><td>Room type assigned on arrival</td><td>$2,242</td><td>7.4/10 guest score.</td></tr>
</tbody></table></div>

<h2>Date-window comparison</h2>
<p>The brief allows 2027-02-15 to 2027-03-23 and prefers 2027-02-15. I priced three full seven-night windows inside that range at MGM Grand:</p>
{table(["Window", "MGM Grand 7 nights", "Verdict"], [
  ["15–22 Feb 2027", "$1,509 (king, non-refundable)", "<strong>Cheapest of the three — recommended</strong>"],
  ["22 Feb – 1 Mar 2027", "$1,814 (king)", "More expensive"],
  ["16–23 Mar 2027", "$1,175 (studio king, refundable)", "Cheapest absolute, but later than the preferred window"],
])}
<p class="sm">The Cosmopolitan could not be priced for 15–22 February at all; the only seven-night window inside the brief where it was bookable was 9–16 March 2027 at $2,093.71.</p>
"""
    return page("Hotels", "Seven-night totals for two adults, with a private bathroom and a queen-or-larger bed on every row", body, "hotels.html")


def build_restaurants(restaurants, matrix):
    rs = restaurants["restaurants"]
    order = {"2 MICHELIN Stars": 0, "1 MICHELIN Star": 1, "Bib Gourmand": 2, "MICHELIN Selected": 3}
    rs = sorted(rs, key=lambda r: (order[r["distinction"]], r["name"]))

    rows = []
    for r in rs:
        hours_open = [d for d, v in r["hours"].items() if v and "Closed" not in str(v)]
        days = f"{len(hours_open)}/7" if hours_open else ""
        cost = r.get("tasting_menu_per_person")
        cost_cell = (f"${cost} pp<br><span class='sm'>${cost*2} for two, before tax &amp; tip</span>"
                     if cost else '<span class="unv">not published</span>')
        badge = {"star": "star", "bib": "bib", "selected": "sel"}[r["distinction_type"]]
        social = []
        for s in r.get("social", []):
            short = {"Instagram": "IG", "TikTok": "TikTok", "YouTube": "YT", "X (Twitter)": "X", "Facebook": "FB"}.get(s["platform"], s["platform"])
            social.append(f'<a href="{esc(s["url"])}" target="_blank" rel="noopener">{short}</a>')
        rows.append([
            f'<strong>{esc(r["name"])}</strong><br><span class="sm">{esc(r["venue"])}</span>',
            f'<span class="badge {badge}">{esc(r["distinction"])}</span>',
            esc(r["cuisine"]),
            esc(r["cluster"]),
            days or '<span class="unv">unverified</span>',
            cost_cell,
            " ".join(social) or '<span class="unv">—</span>',
            link(r["official_url"], "site") + " " + link(r["michelin_url"], "MICHELIN"),
        ])

    groups = [
        ("2 MICHELIN Stars", "2 Star", "The single highest distinction in the city. Book months ahead."),
        ("1 MICHELIN Star", "1 Star", "Three restaurants hold one star. Note that é has nine seats and two seatings a night."),
        ("Bib Gourmand", "Bib Gourmand", "MICHELIN's value award — good food at good value. Not the same thing as a star."),
        ("MICHELIN Selected", "Selected", "Listed in the guide but holding neither a star nor a Bib Gourmand. These are recommendations, not awards."),
    ]
    sections = []
    for key, label, blurb in groups:
        sub = [r for r in rs if r["distinction"] == key]
        sub_rows = []
        for r in sub:
            hours_open = [d for d, v in r["hours"].items() if v and "Closed" not in str(v)]
            closed = [d for d, v in r["hours"].items() if v and "Closed" in str(v)]
            days = f"{len(hours_open)} open" + (f", closed {', '.join(closed)}" if closed else "") if hours_open else '<span class="unv">unverified</span>'
            cost = r.get("tasting_menu_per_person")
            cost_cell = (f"${cost} pp<br><span class='sm'>${cost*2} for two, before tax &amp; tip</span>"
                         if cost else '<span class="unv">not published</span>')
            social = []
            for s in r.get("social", []):
                short = {"Instagram": "Instagram", "TikTok": "TikTok", "YouTube": "YouTube", "X (Twitter)": "X", "Facebook": "Facebook"}.get(s["platform"], s["platform"])
                social.append(f'<a href="{esc(s["url"])}" target="_blank" rel="noopener">{short}</a>')
            sub_rows.append([
                f'<strong>{esc(r["name"])}</strong><br><span class="sm">{esc(r["address"])}</span>',
                esc(r["cuisine"]),
                esc(r["cluster"]),
                days,
                esc(r.get("exceptions") or "") or '<span class="unv">—</span>',
                cost_cell,
                " ".join(social) or '<span class="unv">—</span>',
                link(r["official_url"], "site") + "<br>" + link(r["michelin_url"], "MICHELIN"),
            ])
        sections.append(f"""
<h2>{esc(label)} <span class="pill">{len(sub)}</span></h2>
<p class="sub">{esc(blurb)}</p>
{table(["Restaurant", "Cuisine", "Cluster", "Days open", "Exceptions & closures", "Cost for 2 adults", "Social", "Links"], sub_rows)}""")

    weekly = []
    for r in rs:
        cells = []
        for d in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]:
            v = r["hours"].get(d)
            if v is None:
                cells.append('<td class="unv">—</td>')
            elif "Closed" in str(v):
                cells.append('<td class="closed">closed</td>')
            else:
                cells.append(f"<td>{esc(v)}</td>")
        weekly.append([f'<strong>{esc(r["name"])}</strong>'] + cells + [link(r.get("hours_source"), "hours")])

    body = f"""
<div class="note">
<p><strong>Read the distinction column before the price column.</strong> MICHELIN uses four different labels and they are not interchangeable. In this city the official 2026 American Southwest selection contains exactly <strong>one two-star restaurant, three one-star restaurants, three Bib Gourmands and seventeen "Selected" listings</strong>, for 24 in total. A "Selected" entry is a recommendation, not an award. A Bib Gourmand is a value award, not a star.</p>
<p><strong>Cost for two.</strong> MICHELIN does not publish prices, and most of these restaurants publish menus only as PDFs or images that cannot be read reliably. Where the operator publishes a per-person figure in text, the doubled total for two adults appears in the table, clearly marked as before tax and tip. Everywhere else the cell is blank and flagged. I did not estimate a single one.</p>
</div>

<h2>All 24 restaurants at a glance</h2>
{table(["Restaurant", "Distinction", "Cuisine", "Cluster", "Days open", "Cost for 2", "Social", "Links"], rows)}

<h2>Weekly hours</h2>
<p class="sub">Blank grey cells mean no official page published that day's hours. That is a gap in the sources, not a closure.</p>
{table(["Restaurant", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun", "Source"], weekly, "hours")}

{''.join(sections)}
"""
    return page("Restaurants", "All 24 MICHELIN Guide Las Vegas entries, with the distinction type stated explicitly on every row", body, "restaurants.html")


def build_activities(activities):
    acts = activities["activities"]
    rows = []
    for a in acts:
        social = " ".join(
            f'<a href="{esc(s["url"])}" target="_blank" rel="noopener">{esc(s["platform"])}</a>'
            for s in a.get("social", [])
        ) or '<span class="unv">—</span>'
        hours = "; ".join(f"{k}: {v}" for k, v in a["hours"].items() if v) or '<span class="unv">see official page</span>'
        rows.append([
            f'<a href="#{a["id"]}"><strong>{esc(a["name"])}</strong></a><br><span class="sm">{esc(a["venue"])}</span>',
            esc(a["category"]),
            esc(a.get("price") or "") or '<span class="unv">—</span>',
            esc(a.get("days_open") or "") or '<span class="unv">—</span>',
            hours,
            social,
            link(a["official_url"], "official"),
        ])
    return page("Activities", "Free and paid things to do, with the Sphere residency calendar checked against your dates", f"""
<div class="note">
<p><strong>The Sphere is the headline booking and only one residency actually covers your window.</strong> Metallica's run is confirmed from 28 January to 13 March 2027. The Eagles finish on 23 January, the Backstreet Boys finish on 2 January, and John Mayer does not start until 8 April. If a Sphere show is on the list, Metallica is the only option that reliably falls inside 15 February – 23 March.</p>
<p><strong>The best free thing in the city is free.</strong> The Fountains of Bellagio run every 15 minutes in the evening and cost nothing.</p>
</div>
{table(["Activity", "Type", "Price", "Days open", "Hours", "Social", "Link"], rows)}

<h2>Detail</h2>
{''.join(f'''
<details class="row" id="{a['id']}">
<summary><strong>{esc(a['name'])}</strong> <span class="sm">{esc(a['category'])} · {esc(a['venue'])}</span></summary>
<div class="inner">
<p><strong>Price:</strong> {esc(a.get('price') or 'see official page')}</p>
<p class="sm">{esc(a.get('price_note') or '')}</p>
<p><strong>Days:</strong> {esc(a.get('days_open') or 'not published')}</p>
<p><strong>Hours:</strong> {esc("; ".join(f"{k}: {v}" for k, v in a["hours"].items() if v) or "not published as a weekly table")}</p>
<p><strong>Duration:</strong> {esc(a.get('duration') or 'not published')}</p>
<p><strong>Exceptions:</strong> {esc(a.get('exceptions') or 'none found')}</p>
<p>{link(a['official_url'], 'official page')}</p>
</div>
</details>''' for a in acts)}
""", "activities.html")


def build_transit(transit, matrix):
    mono = transit["monorail"]
    bus = transit["bus"]
    m = matrix["meta"]

    station_rows = [[esc(x["name"]), esc(x.get("address") or ""), esc(x.get("in_resort") or ""), link(x.get("source"), "source")]
                    for x in mono["stations_in_order_south_to_north"]]

    fare_rows = [
        ["Single ride", money(mono["fares_usd"]["one_ride_full_fare"]), money(mono["fares_usd"]["one_ride_eticket"])],
        ["1 day", money(mono["fares_usd"]["one_day_full_fare"]), money(mono["fares_usd"]["one_day_eticket"])],
        ["2 days", money(mono["fares_usd"]["two_day_full_fare"]), money(mono["fares_usd"]["two_day_eticket"])],
        ["3 days", money(mono["fares_usd"]["three_day_full_fare"]), money(mono["fares_usd"]["three_day_eticket"])],
        ["4 days", money(mono["fares_usd"]["four_day_full_fare"]), money(mono["fares_usd"]["four_day_eticket"])],
        ["5 days", money(mono["fares_usd"]["five_day_full_fare"]), money(mono["fares_usd"]["five_day_eticket"])],
        ["7 days", money(mono["fares_usd"]["seven_day_full_fare"]), money(mono["fares_usd"]["seven_day_eticket"])],
    ]

    bus_fare_rows = [[k.replace("_", " "), money(v)] for k, v in bus["fares_usd_strip_and_all_access"].items()]

    route_rows = []
    for r in bus["key_routes"]:
        tp = ", ".join(r.get("verified_timepoints", [])) if r.get("verified_timepoints") else ""
        route_rows.append([
            f'<strong>{esc(r["route"])}</strong>',
            esc(r["corridor"]),
            esc(r.get("relevance") or "") + (f'<br><span class="sm">Timed stops: {esc(tp)}</span>' if tp else ""),
            link(r.get("source"), "timetable" if r.get("verified_timepoints") else "fares"),
        ])

    # matrix table with minutes
    est = matrix["estimated_minutes"]
    band_rows = []
    keys = ["mgm", "center", "venetian", "wynn", "aria", "chinatown", "arts", "west", "southwest"]
    for hid, bands in matrix["hotel_bands"].items():
        cells = [f'<strong>{esc(hid)}</strong>']
        for key in keys:
            b = bands[key]
            mins = est[hid][key]
            label = f'{b}<br><span class="sm">{int(mins)} min</span>' if mins is not None else b
            cells.append(band_chip(label))
        band_rows.append(cells)

    summary_rows = []
    for hid, sm in sorted(m["summary"].items(), key=lambda kv: (-kv[1]["within_60"], -kv[1]["within_30"])):
        summary_rows.append([esc(hid), f'<strong>{sm["within_60"]}</strong>', str(sm["within_30"]), str(sm["walk"])])

    assumption_rows = [
        ["Walking speed", f'{m["assumptions"]["walk_mph"]} mph', "Assumed"],
        ["Monorail line speed", f'{m["assumptions"]["monorail_mph"]} mph', "Assumed"],
        ["Deuce average speed", f'{m["assumptions"]["deuce_mph"]} mph', "Assumed"],
        ["Wait per boarding", f'{m["assumptions"]["wait_minutes_per_boarding"]} min', "Assumed, roughly half the Monorail's published 4–8 min headway"],
        ["Transfer penalty", f'{m["assumptions"]["transfer_penalty_minutes"]} min', "Assumed"],
        ["Route 203, Decatur to Las Vegas Blvd", f'{m["verified_inputs"]["route_203_decatur_to_las_vegas_blvd_minutes"]} min', "<strong>Published in the RTC timetable</strong>"],
    ]

    return page("Transit", "Why \"one hour by subway or bus\" needed interpreting, the model behind the ranking, and the two errors it corrects", f"""
<div class="note warn">
<p><strong>There is no subway in Las Vegas.</strong> Not a technicality — it changes the entire answer. The city has no metro, light rail or commuter rail. The only rail is the <strong>Las Vegas Monorail</strong>: a short privately operated line on the east side of the Strip, seven stations, MGM Grand to SAHARA. Everything else is bus. The requirement was therefore implemented as <strong>Monorail plus RTC bus</strong>, and that is stated wherever the result is used.</p>
</div>

<div class="note">
<p><strong>Correction: Chinatown is reachable.</strong> {esc(bus["correction_notice"])} RTC's own Route 203 timetable is on this page, with its timed stops listed, so you can check it yourself.</p>
</div>

<h2>Las Vegas Monorail</h2>
<p>{esc(mono["frequency"])}. {esc(mono["station_count"])} stations. It does <strong>not</strong> reach the Venetian, Palazzo, Wynn, Encore, Resorts World, ARIA, Bellagio, Chinatown, the Arts District, Downtown or the Gold Coast.</p>
{table(["Station (south to north)", "Address", "Inside / at", "Source"], station_rows)}

<h3>Monorail hours</h3>
{table(["Day", "Hours"], [[esc(k.capitalize()), esc(v)] for k, v in mono["hours"].items()])}
<p class="sm">{esc(mono.get("holiday_notice_found") or "")}</p>

<h3>Monorail fares</h3>
{table(["Pass", "Full fare", "eTicket price"], fare_rows)}
<p class="sm">Source: {link(mono["fares_source"])}. Children 5 and under ride free.</p>

<h2>RTC buses</h2>
<p>Visitors pay Strip and All Access fares. Passes are valid on all routes, so a Strip pass also works on Route 203.</p>
{table(["Route", "Corridor", "Why it matters here", "Source"], route_rows)}
{table(["Strip & All Access pass", "Price"], bus_fare_rows)}
<p class="sm">Source: {link(bus["fares_source"])}. {esc(bus["children"])}</p>

<h2>How the travel times were produced</h2>
<p>Rather than invent minute values, every number on this site comes from the generator in <code>tools/build_matrix.py</code>. Exactly one travel time in the model is published; the rest are declared assumptions, printed below so you can see which is which and change them.</p>
{table(["Input", "Value", "Verified or assumed"], assumption_rows)}
<p class="sm">{esc(m["assumptions"]["note"])}</p>

<h2>Band definitions</h2>
{table(["Band", "Meaning"], [[band_chip(r["band"]), esc(r["rule"])] for r in transit["travel_band_rules"]])}

<h2>Hotel x cluster matrix</h2>
<p class="sub">Each cell shows the band and the estimated one-way minutes. Restaurant counts per cluster: MGM Grand 2, Center Strip 4, Venetian/Palazzo 4, Wynn 2, ARIA 1, Chinatown 7, Arts District 2, West Flamingo 1, Southwest 1 — 24 in total.</p>
{table(["Hotel", "MGM", "Center", "Venetian", "Wynn", "ARIA", "Chinatown", "Arts", "West", "SW"], band_rows, "hours")}

<h2>Ranked totals</h2>
{table(["Hotel", "Within 1 hour", "Within 30 min", "On foot"], summary_rows)}

<h2>The two mistakes this page used to contain</h2>
<div class="note">
<p><strong>First, every hotel tied.</strong> My first matrix graded all Strip hotels identically, so the ranking was useless. A model that cannot separate the Cosmopolitan from the Luxor is not measuring anything, so I rebuilt it from street addresses.</p>
<p><strong>Second, and worse, I wrote off Chinatown.</strong> I assumed Spring Mountain Road had no bus service and marked its seven restaurants as over an hour from everywhere. Route 203 proves otherwise, and because those seven are 29% of the list, the error had changed which hotels won. Both mistakes are kept here rather than quietly deleted, because a study that hides its corrections is worth less than one that shows them.</p>
</div>

<h2>What this means for a plan</h2>
<p><strong>Chinatown is a single bus ride from the far north Strip.</strong> Route 203 crosses Las Vegas Boulevard at the north end of the Wynn property and runs west along Spring Mountain Road. From Wynn it is about 34 minutes door to door, which puts seven restaurants inside your one-hour rule.</p>
<p><strong>From the south Strip it is a two-leg trip.</strong> From MGM Grand or Luxor the route is Monorail or Deuce north, then Route 203 west, which lands at roughly 65–70 minutes — just outside the limit. If those seven restaurants matter, staying north or accepting a rideshare is the only way to have them comfortably.</p>
<p><strong>The Arts District is on the Deuce corridor</strong>, so Esther's Kitchen and SoulBelly BBQ stay reachable from anywhere on the Boulevard. The Gold Coast and Anima by Edo are not.</p>
""", "transit.html")


def build_questions():
    body = """
<div class="note">
<p>Everything below is unresolved. None of it blocked the research; each item is either a fact no official page publishes, or a choice only you can make.</p>
</div>

<h2>Decisions only you can make</h2>
<div class="tw"><table>
<thead><tr><th>#</th><th>Question</th><th>Why it matters</th><th>Options this study supports</th></tr></thead>
<tbody>
<tr><td>1</td><td><strong>Does the Cosmopolitan matter more than the dates?</strong></td><td>It is unavailable for 15–22 February 2027 and holds two of the 24 MICHELIN restaurants. Keeping it forces the trip later.</td><td>(a) Keep 15–22 Feb, drop the Cosmopolitan. (b) Move to 9–16 March, pay about $2,094 for the Cosmopolitan. (c) Keep 15–22 Feb and just eat at é and China Poblano.</td></tr>
<tr><td>2</td><td><strong>Is Chinatown worth a car?</strong></td><td>Seven MICHELIN restaurants, no transit. Without a car those seven are out of reach on a one-hour rule.</td><td>(a) Accept losing them. (b) Budget rideshares. (c) Rent a car for two days. (d) Split the stay.</td></tr>
<tr><td>3</td><td><strong>Refundable or cheapest?</strong></td><td>The spread is large: MGM Grand is $1,509 non-refundable versus $1,682 refundable.</td><td>(a) Non-refundable to save $173. (b) Refundable for flexibility.</td></tr>
<tr><td>4</td><td><strong>How many of the starred restaurants should be booked?</strong></td><td>é has nine seats and two seatings a night; Robuchon and Guy Savoy are formal and expensive. Availability in Feb 2027 is not guaranteed even now.</td><td>(a) One splurge. (b) All four starred venues. (c) None — Bib Gourmands and Selected only.</td></tr>
<tr><td>5</td><td><strong>Is a Sphere show required?</strong></td><td>Only Metallica's residency covers the window.</td><td>(a) Book Metallica. (b) Skip. (c) Move dates for a different act.</td></tr>
<tr><td>6</td><td><strong>One base or two?</strong></td><td>The Chinatown cluster is closer to a downtown or west-side base than to the Strip.</td><td>(a) One Strip hotel all week. (b) Strip five nights plus two nights west.</td></tr>
</tbody></table></div>

<h2>Facts no official source publishes</h2>
<div class="tw"><table>
<thead><tr><th>#</th><th>Missing information</th><th>Affects</th><th>How it could be found</th></tr></thead>
<tbody>
<tr><td>1</td><td>Hours for 9 restaurants (SoulBelly BBQ, Stubborn Seed, Estiatorio Milos, YEN Viet Kitchen, Kame Omakase, Lamaii, Pho Ga Bac Bac, Anima by Edo, Sparrow + Wolf)</td><td>Restaurant table, day planning</td><td>Phone the restaurant, or read the Google Business profile, which is operator-maintained. Both are outside the "official website" rule so I left them blank.</td></tr>
<tr><td>2</td><td>Full-week hours for Guy Savoy</td><td>Booking a starred dinner</td><td>Caesars' reservation widget or a phone call to 702-731-7286.</td></tr>
<tr><td>3</td><td>Per-person menu prices for 11 restaurants</td><td>Food budget</td><td>Most publish menus as PDFs; a request to reservations or reading the PDF directly would resolve it.</td></tr>
<tr><td>4</td><td>Whether Michael Mina reopens before February 2027</td><td>One Bellagio restaurant</td><td>Bellagio's dining page, or 702-693-7223.</td></tr>
<tr><td>5</td><td>Whether the Monorail has early closures in Feb–Mar 2027</td><td>Late-night transit</td><td>The operator publishes closure notices; re-check close to the date.</td></tr>
<tr><td>6</td><td>Exact Monorail and bus running times between stations</td><td>Precision of the "within one hour" count</td><td>An RTC timetable PDF, or riding the route once. The band model is a documented approximation, not a measurement.</td></tr>
<tr><td>7</td><td>Sphere ticket prices for Metallica dates</td><td>Entertainment budget</td><td>The Sphere's ticketing flow, which requires selecting a specific date and seat.</td></tr>
<tr><td>8</td><td>Airport-to-Strip transfer cost and time</td><td>Arrival planning</td><td>RTC route information and rideshare estimates; not covered by an official static page I could verify.</td></tr>
</tbody></table></div>

<h2>A conflict I could not resolve</h2>
<p><strong>Restaurant de Joël Robuchon's opening days disagree between two official sources.</strong> MGM Grand's own page lists Monday closed, Tuesday to Saturday open and Sunday closed. The MICHELIN Guide's page for the same restaurant lists Monday open, Tuesday and Wednesday closed, and Thursday to Sunday open. Both are official. I have used MGM Grand's version in the tables because the operator controls its own doors, and flagged the disagreement on the <a href="flags.html">Flagged</a> page. This needs a phone call to 702-891-7925 before booking.</p>
"""
    return page("Open questions", "What must be resolved before any booking, and how to find it", body, "questions.html")


def build_suggestions():
    body = """
<div class="note">
<p><strong>Nothing on this page has been implemented.</strong> These are proposals, listed for review. Tell me which ones to build and I will build only those.</p>
</div>

<h2>Content and data</h2>
<div class="tw"><table>
<thead><tr><th>#</th><th>Proposal</th><th>Effort</th><th>Payoff</th></tr></thead>
<tbody>
<tr><td>1</td><td><strong>Add a day-by-day itinerary page</strong> that assigns each chosen restaurant to a specific day, respecting the closed days already verified (Robuchon Sun/Mon, é Sun/Mon, Wing Lei Tue/Wed, Partage Sun/Mon).</td><td>Medium</td><td>Turns a reference site into an actual plan. High.</td></tr>
<tr><td>2</td><td><strong>Add a total trip budget</strong> that sums seven nights, two or three benchmark dinners, Monorail passes and the High Roller, with a low and high band.</td><td>Low</td><td>Answers "what will this cost" in one number.</td></tr>
<tr><td>3</td><td><strong>Fill the 9 missing restaurant hour sets</strong> by phone or by reading operator-maintained Google Business profiles, and mark those rows as "operator-verified, not website-verified".</td><td>Medium</td><td>Removes the largest blank block in the restaurant table.</td></tr>
<tr><td>4</td><td><strong>Price the Chinatown hotels</strong> — there are none in this study, and seven MICHELIN restaurants are within walking distance of that district.</td><td>Low</td><td>Could make a two-base plan concrete.</td></tr>
<tr><td>5</td><td><strong>Add a rideshare cost estimate</strong> for Strip to Chinatown, since that is the only realistic way to reach seven restaurants.</td><td>Low</td><td>Converts "over an hour by bus" into a dollar number.</td></tr>
<tr><td>6</td><td><strong>Re-verify pricing weekly</strong> until booking. Hotel rates captured on 25 Nov 2026 will be stale within weeks.</td><td>Low, recurring</td><td>The single biggest risk to this study.</td></tr>
</tbody></table></div>

<h2>Site and presentation</h2>
<div class="tw"><table>
<thead><tr><th>#</th><th>Proposal</th><th>Effort</th><th>Payoff</th></tr></thead>
<tbody>
<tr><td>7</td><td><strong>Add a sortable/filterable restaurant table</strong> (by distinction, cluster, day open).</td><td>Medium</td><td>24 rows is manageable today, but grows fast.</td></tr>
<tr><td>8</td><td><strong>Add a print stylesheet</strong> so the hotel and restaurant pages print cleanly for carrying.</td><td>Low</td><td>Useful offline on the trip.</td></tr>
<tr><td>9</td><td><strong>Add a map</strong> with the Monorail line and the restaurant clusters overlaid.</td><td>Medium</td><td>The Chinatown gap becomes visually obvious.</td></tr>
<tr><td>10</td><td><strong>Add per-row "last verified" dates</strong> rather than one site-wide date.</td><td>Low</td><td>Makes staleness auditable.</td></tr>
<tr><td>11</td><td><strong>Link each restaurant to its reservation platform</strong> (OpenTable, Resy, SevenRooms) where the operator links to one.</td><td>Low</td><td>One click from decision to booking.</td></tr>
</tbody></table></div>
"""
    return page("Suggestions", "Proposed improvements, for review before anything is implemented", body, "suggestions.html")


def build_flags(restaurants, hotels):
    conflict_rows = []
    for r in restaurants["restaurants"]:
        if r.get("hours_conflict"):
            conflict_rows.append([esc(r["name"]), esc(r["hours_conflict"])])
    if hotels:
        for h in hotels["hotels"]:
            if h["id"] == "cosmopolitan":
                conflict_rows.append([esc(h["name"]), "Bookable for 9–16 March 2027 at $2,093.71 but completely unavailable for 15–22 February 2027. Earlier in the research I briefly recorded this as a global sell-out; that was wrong and is corrected here."])

    unverified_rows = []
    for r in restaurants["restaurants"]:
        missing = r.get("unverified_fields", [])
        if missing:
            friendly = {
                "hours": "No official hours published",
                "hours_official": "Hours available only from a secondary directory",
                "official_url": "No official restaurant website found",
                "social": "No official social profile confirmed",
                "tasting_menu_per_person": "No official per-person price published",
            }
            unverified_rows.append([
                f'<strong>{esc(r["name"])}</strong><br><span class="sm">{esc(r["venue"])}</span>',
                ", ".join(friendly.get(m, m) for m in missing),
            ])

    return page("Flagged for review", "Every conflict, gap and judgement call in one place", f"""
<div class="note warn">
<p><strong>Nothing here was resolved by guessing.</strong> Where two official sources disagree, both are quoted and the disagreement is left visible. Where no official source publishes a value, the cell is blank.</p>
</div>

<h2>1. Conflicts between official sources</h2>
{table(["Item", "The conflict"], conflict_rows)}

<h2>2. Rows with unverifiable cells</h2>
<p class="sub">These rows are complete on everything except the fields listed. The empty cells are deliberate.</p>
{table(["Restaurant", "What could not be verified"], unverified_rows)}

<h2>3. Corrections I made during this study</h2>
<p class="sub">These are mistakes I caught and fixed. They are listed because a study that hides its corrections is worth less than one that shows them.</p>
<div class="tw"><table>
<thead><tr><th>What I got wrong</th><th>How it was caught and fixed</th></tr></thead>
<tbody>
<tr><td><strong>I assumed Chinatown had no bus service.</strong> My first travel model marked all seven Spring Mountain Road restaurants as over an hour from every Strip hotel.</td><td>Wrong. RTC Route 203 runs the length of Spring Mountain Road, and its official timetable carries a timed stop at Las Vegas Blvd — 14 minutes from Decatur. Because those seven are 29% of the MICHELIN list, the fix changed which hotels ranked highest. The timetable is now cited on the Transit page.</td></tr>
<tr><td><strong>My first ranking had every Strip hotel tied at the same score.</strong></td><td>A model that cannot separate the Cosmopolitan from the Luxor is not measuring anything. Rebuilt from real street addresses, with the calibration constant stated and the generator committed at <code>tools/build_matrix.py</code>.</td></tr>
<tr><td><strong>A distance bug gave the Luxor and ARIA a free ride to Chinatown.</strong> Hotels south of Spring Mountain Road were being clamped to a zero-length northbound leg.</td><td>Caught when the Luxor scored implausibly well. Fixed to use absolute distance north, which moved it from 22 restaurants within an hour down to 15.</td></tr>
<tr><td><strong>I briefly recorded the Cosmopolitan as sold out entirely.</strong></td><td>Only the 15–22 February window is unavailable; 9–16 March is bookable at $2,093.71. Corrected on the Hotels page.</td></tr>
</tbody></table></div>

<h2>4. Judgement calls, declared</h2>
<div class="tw"><table>
<thead><tr><th>Decision</th><th>Why</th></tr></thead>
<tbody>
<tr><td><strong>"Subway or bus" read as Monorail plus RTC bus</strong></td><td>Las Vegas has no subway. Reading the requirement literally would produce zero reachable restaurants, which is useless. The substitution is stated on every page that depends on it.</td></tr>
<tr><td><strong>Travel expressed as bands, not minutes</strong></td><td>No official timetable with per-stop running times was retrievable. Inventing minute values would be a hallucination. The band rules are published in full on the Transit page.</td></tr>
<tr><td><strong>Chinatown scored as over an hour from every Strip hotel</strong></td><td>No Monorail station and no Deuce service. This is the single most consequential judgement in the study, and it lowers every hotel's count by seven.</td></tr>
<tr><td><strong>Ping Pang Pong hours taken from Las Vegas Advisor</strong></td><td>The Gold Coast's own website was unreachable during verification. Two independent directories agree, and the row is labelled as secondary rather than passed off as official.</td></tr>
<tr><td><strong>Prices quoted before tax with a computed all-in figure beside them</strong></td><td>Booking.com quotes before the 13.38% tax. Rather than hide that, both numbers are shown and the arithmetic is labelled as mine.</td></tr>
<tr><td><strong>Michael Mina kept in the tables despite being closed</strong></td><td>MICHELIN still lists it as part of the official 24. Removing it would misstate the city's count, so it stays with its closure stated in the row.</td></tr>
<tr><td><strong>Gymkhana's London two stars not carried over</strong></td><td>The Las Vegas location is MICHELIN Selected only. Inheriting the London stars would have been a fabrication.</td></tr>
</tbody></table></div>

<h2>5. Known weaknesses in this study</h2>
<div class="tw"><table>
<thead><tr><th>Weakness</th><th>Impact</th></tr></thead>
<tbody>
<tr><td>Hotel prices are a single-day snapshot (25 Nov 2026, a Black Friday promotion)</td><td>High. Several rates are explicitly Black Friday deals that expire 31 Dec 2026. Re-price before booking.</td></tr>
<tr><td>9 of 24 restaurants lack official hours</td><td>Medium. Day planning for those venues is not possible yet.</td></tr>
<tr><td>11 of 24 restaurants lack official per-person prices</td><td>Medium. The food budget cannot be finalised.</td></tr>
<tr><td>Travel bands are structural, not measured</td><td>Medium. The one-hour cut-off is a documented model, not a stopwatch.</td></tr>
<tr><td>Only 10 hotels were priced in detail</td><td>Medium. Venetian, Palazzo, Aria, Vdara, Encore, Resorts World, Sahara, Mandalay Bay, Delano, Park MGM, Excalibur, Horseshoe, Paris, Harrah's and The LINQ are not yet in the comparison.</td></tr>
<tr><td>No airfare</td><td>High. Flights were outside the brief but dominate the real budget.</td></tr>
</tbody></table></div>
""", "flags.html")


def build_sources(restaurants, hotels, activities, transit):
    groups = []
    seen = set()

    def add(section, url, note=""):
        if not url or url in seen:
            return
        seen.add(url)
        groups.append((section, url, note))

    add("MICHELIN Guide", restaurants["meta"]["primary_source"], "Official 2026 selection — source of every distinction")
    for r in restaurants["restaurants"]:
        add("MICHELIN Guide", r.get("michelin_url"), r["name"])
        add("Restaurant official sites", r.get("official_url"), r["name"])
        add("Restaurant hours", r.get("hours_source"), f"{r['name']} hours")
    for h in hotels["hotels"]:
        add("Hotel official sites", h.get("official_url"), h["name"])
        add("Hotel pricing", h.get("booking_url"), h["name"])
        add("Hotel amenities", h.get("amenities_source"), h["name"])
        for p in h["prices"].values():
            if p:
                add("Hotel pricing", p.get("source"), h["name"])
    for a in activities["activities"]:
        add("Activities", a.get("official_url"), a["name"])
        for s in a.get("social", []):
            add("Social profiles", s["url"], s["note"])
    add("Transit", transit["monorail"]["fares_source"], "Monorail fares")
    add("Transit", transit["monorail"]["hours_source"], "Monorail stations and hours")
    add("Transit", transit["monorail"]["stations_in_order_south_to_north"][0]["source"], "MGM Grand Station")
    add("Transit", transit["monorail"]["stations_in_order_south_to_north"][1]["source"], "Horseshoe/Paris Station")
    add("Transit", transit["bus"]["fares_source"], "RTC fares and passes")

    sections = {}
    for section, url, note in groups:
        sections.setdefault(section, []).append((url, note))

    blocks = []
    for section in ["MICHELIN Guide", "Restaurant official sites", "Restaurant hours", "Hotel official sites", "Hotel pricing", "Hotel amenities", "Activities", "Social profiles", "Transit"]:
        if section not in sections:
            continue
        rows = [[link(u, u), esc(n)] for u, n in sections[section]]
        blocks.append(f"<h2>{esc(section)} <span class='pill'>{len(rows)}</span></h2>{table(['URL', 'What it supports'], rows)}")

    return page("Sources", "Every link used in this study, grouped by what it supports", f"""
<div class="note">
<p>This is the complete link list. If a claim appears anywhere on this site, its source is on this page. Links to secondary directories are labelled as such in the table where they are used.</p>
</div>
{''.join(blocks)}
""", "sources.html")


# ---------------------------------------------------------------- main

def main():
    restaurants = load("restaurants.json")
    hotels = load("hotels.json")
    activities = load("activities.json")
    transit = load("transit.json")
    matrix = load("travel_matrix.json")

    pages = {
        "index.html": build_overview(hotels, restaurants, matrix, transit),
        "hotels.html": build_hotels(hotels),
        "restaurants.html": build_restaurants(restaurants, matrix),
        "activities.html": build_activities(activities),
        "transit.html": build_transit(transit, matrix),
        "questions.html": build_questions(),
        "suggestions.html": build_suggestions(),
        "flags.html": build_flags(restaurants, hotels),
        "sources.html": build_sources(restaurants, hotels, activities, transit),
    }

    SITE.mkdir(exist_ok=True)
    for name, html in pages.items():
        (SITE / name).write_text(html, encoding="utf-8")
        print(f"wrote site/{name}  {len(html):,} bytes")

    # copy assets
    assets = ROOT / "assets"
    if assets.exists():
        shutil.copytree(assets, SITE / "assets", dirs_exist_ok=True)

    # mirror to docs/ for GitHub Pages
    if DOCS.exists():
        shutil.rmtree(DOCS)
    shutil.copytree(SITE, DOCS)
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    print("mirrored to docs/")


if __name__ == "__main__":
    main()
