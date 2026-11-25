#!/usr/bin/env python3
"""
build.py - generates the static site in docs/ from data/*.json

Design rules enforced here:
  * No value is invented. Every cell in an output table either comes from a JSON
    file (which itself carries a source) or renders as the literal word "unverified".
  * Hotel ranking is computed, not hand-written, so the score is reproducible.
  * Site is a single-page-per-category dashboard; mobile-first CSS; no JS required.
"""
import json, os, html, re, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "plan-data")
DOCS = os.path.join(ROOT, "docs")

def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return json.load(f)

MICHELIN = load("michelin.json")
HOTELS = load("hotels.json")
PRICING = load("pricing.json")
TRANSIT = load("transit.json")
ACTIVITIES = load("activities.json")
DETAILS = load("restaurant-details.json")
SOCIAL = load("social.json")
CROSS = load("cross-session-audit.json")

e = lambda s: html.escape(str(s)) if s is not None else ""

UNV = '<span class="unv">unverified</span>'

def cell(v, unverified_word=False):
    if v is None or v == "" or v == "unverified":
        return UNV
    return e(v)

# ---------------------------------------------------------------- ranking model
def hotel_scores():
    """Score = Michelin reachability * 0.55 + value * 0.20 + guest score * 0.15 + bed fit * 0.10
    Reachability uses ONLY measured transit rows; hotels without measurements score 0 on it
    and are explicitly shown as 'not measured' rather than being silently ranked higher/lower."""
    rows = TRANSIT["rows"]
    measured = {}
    for r in rows:
        measured.setdefault(r["hotel_id"], []).append(r)
    out = []
    for h in HOTELS["hotels"]:
        mr = measured.get(h["id"], [])
        within = [r for r in mr if r["minutes"] <= 60]
        # reach component: proportional to measured venues inside 60 min.
        # A hotel with very few measurements earns a "thin evidence" penalty on the score
        # (see below) so a single lucky route cannot beat a properly measured hotel.
        reach = round(100 * len(within) / len(mr)) if mr else None
        # evidence weight: full credit at >=3 measured routes, scaled down below that
        ev = min(1.0, len(mr) / 3)
        # value component: cheaper is better, normalised across the verified set
        price = h.get("total_usd")
        value = None
        if price:
            lo = min(x["total_usd"] for x in HOTELS["hotels"] if x.get("total_usd"))
            hi = max(x["total_usd"] for x in HOTELS["hotels"] if x.get("total_usd"))
            value = round(100 * (hi - price) / (hi - lo)) if hi > lo else 50
        gs = h.get("guest_score")
        guest = round(gs * 10) if gs else None
        bed = 100 if h.get("bed_meets_req") is True else (50 if h.get("bed_meets_req") == "partial" else None)
        parts, weights = [], []
        if reach is not None: parts.append(reach); weights.append(0.55 * ev)
        if value is not None: parts.append(value); weights.append(0.20)
        if guest is not None: parts.append(guest); weights.append(0.15)
        if bed is not None: parts.append(bed); weights.append(0.10)
        score = round(sum(p * w for p, w in zip(parts, weights)) / sum(weights), 1) if parts else None
        out.append({
            "hotel": h, "reach": reach, "value": value, "guest": guest, "bed": bed,
            "score": score, "measured": mr, "n_measured": len(mr), "n_within": len(within)
        })
    out.sort(key=lambda x: (x["score"] is None, -(x["score"] or 0)))
    return out

SCORES = hotel_scores()

CSS = """
:root{--bg:#0d1117;--card:#161b22;--line:#30363d;--ink:#e6edf3;--dim:#8b949e;
--acc:#f5c518;--good:#2ea043;--bad:#da3633;--warn:#d29922;--link:#58a6ff}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);
font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--link);text-decoration:none}
a:hover{text-decoration:underline}
header.site{position:sticky;top:0;z-index:50;background:rgba(13,17,23,.96);
border-bottom:1px solid var(--line);backdrop-filter:blur(8px)}
.wrap{max-width:1180px;margin:0 auto;padding:0 16px}
.site .wrap{display:flex;align-items:center;gap:14px;flex-wrap:wrap;padding-top:10px;padding-bottom:10px}
.brand{font-weight:700;letter-spacing:.3px;color:var(--ink)}
.brand span{color:var(--acc)}
nav{display:flex;gap:6px;flex-wrap:wrap}
nav a{padding:6px 10px;border-radius:8px;font-size:14px;color:var(--dim);border:1px solid transparent}
nav a:hover{background:var(--card);color:var(--ink);text-decoration:none}
nav a.on{color:var(--acc);border-color:var(--line);background:var(--card)}
main{padding:22px 0 70px}
h1{font-size:clamp(24px,5vw,34px);line-height:1.2;margin:.2em 0 .3em}
h2{font-size:clamp(19px,3.4vw,25px);margin:1.8em 0 .5em;padding-bottom:.3em;border-bottom:1px solid var(--line)}
h3{font-size:17px;margin:1.4em 0 .4em}
p,li{color:#c9d1d9}
.lead{color:var(--dim);max-width:70ch}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px;margin:14px 0}
.grid{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(220px,1fr))}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px}
.kpi b{display:block;font-size:26px;color:var(--acc);line-height:1.1}
.kpi small{color:var(--dim);font-size:12px;text-transform:uppercase;letter-spacing:.5px}
.tblwrap{overflow-x:auto;-webkit-overflow-scrolling:touch;border:1px solid var(--line);
border-radius:12px;margin:12px 0;background:var(--card)}
table{border-collapse:collapse;width:100%;font-size:13.5px;min-width:640px}
th,td{padding:9px 11px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}
th{background:#1c2128;color:var(--ink);font-size:12px;text-transform:uppercase;
letter-spacing:.5px;position:sticky;top:0;white-space:nowrap}
tbody tr:last-child td{border-bottom:none}
tbody tr:hover{background:#1b2028}
td.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.unv{color:var(--warn);font-style:italic;font-size:12px}
.tag{display:inline-block;padding:2px 8px;border-radius:999px;font-size:11px;
font-weight:700;letter-spacing:.4px;white-space:nowrap}
.t2{background:var(--acc);color:#000}
.t1{background:#c9a227;color:#000}
.tb{background:#1f6feb;color:#fff}
.tr{background:#30363d;color:#e6edf3}
.ok{color:var(--good);font-weight:700}
.no{color:var(--bad);font-weight:700}
.warnbox{border-left:4px solid var(--warn);background:#1f1a10;padding:12px 14px;
border-radius:0 10px 10px 0;margin:14px 0}
.errbox{border-left:4px solid var(--bad);background:#1f1213;padding:12px 14px;
border-radius:0 10px 10px 0;margin:14px 0}
.okbox{border-left:4px solid var(--good);background:#0f1f14;padding:12px 14px;
border-radius:0 10px 10px 0;margin:14px 0}
.src{font-size:11.5px;color:var(--dim)}
.src a{color:#7d8590}
footer{border-top:1px solid var(--line);padding:22px 0;color:var(--dim);font-size:13px}
.pill{font-size:11px;border:1px solid var(--line);border-radius:999px;
padding:2px 8px;color:var(--dim);white-space:nowrap;display:inline-block}
.rank{font-weight:800;color:var(--acc);font-size:15px}
details{margin:10px 0}
summary{cursor:pointer;color:var(--acc);font-weight:600;padding:6px 0}
.q{font-weight:600;color:var(--ink)}
.a{color:#c9d1d9;border-left:2px solid var(--line);padding-left:12px;margin:6px 0 16px}
@media(max-width:640px){
 table{min-width:520px;font-size:12.5px}
 th,td{padding:7px 8px}
 h1{font-size:22px}
 .site .wrap{gap:8px}
 nav a{padding:5px 8px;font-size:13px}
}
"""

PAGES = [
    ("index.html", "Overview"),
    ("hotels.html", "Hotels"),
    ("michelin.html", "MICHELIN"),
    ("transit.html", "Transit"),
    ("activities.html", "Activities"),
    ("itinerary.html", "Itinerary"),
    ("budget.html", "Budget"),
    ("questions.html", "Open Questions"),
    ("suggestions.html", "Suggestions"),
    ("verification.html", "Verification"),
    ("flagged.html", "Flagged for Review"),
    ("audit.html", "Repo Audit"),
    ("audit-main.html", "Audit of main"),
]

def nav(cur):
    items = "".join(
        f'<a href="{f}"{" class=on" if f == cur else ""}>{e(t)}</a>' for f, t in PAGES
    )
    return f"""<header class="site"><div class="wrap">
<span class="brand">LAS VEGAS <span>2027</span></span><nav>{items}</nav>
</div></header>"""

def page(fname, title, body):
    doc = f"""<!DOCTYPE html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} | Las Vegas 2027 Trip Planner</title>
<meta name="description" content="Verified, source-linked planning data for a Michelin-focused Las Vegas trip, Feb-Mar 2027.">
<style>{CSS}</style></head><body>
{nav(fname)}
<main><div class="wrap">{body}</div></main>
<footer><div class="wrap">
<p><strong>Data snapshot:</strong> 2026-11-25 (UTC). Prices and hours change — re-verify before booking.</p>
<p>Every figure on this site is either linked to an official source or marked <span class="unv">unverified</span>.
Nothing is estimated silently. <a href="verification.html">Verification log</a> · <a href="flagged.html">Flagged for Review</a></p>
</div></footer></body></html>"""
    with open(os.path.join(DOCS, fname), "w", encoding="utf-8") as f:
        f.write(doc)
    return fname

# ---------------------------------------------------------------- helpers
def distinction_tag(d):
    cls = {"2 Stars": "t2", "1 Star": "t1", "Bib Gourmand": "tb", "Recommended": "tr"}.get(d, "tr")
    return f'<span class="tag {cls}">{e(d)}</span>'

DET = {r["id"]: r for r in DETAILS["restaurants"]}
SOC = {r["venue_id"]: r for r in SOCIAL["links"]}

def hours_cell(rid):
    d = DET.get(rid)
    if not d or not d.get("hours"):
        return UNV, d
    return None, d

def hours_text(d):
    if not d or not d.get("hours"):
        return None
    h = d["hours"]
    bits = []
    for k, v in h.items():
        bits.append(f"{k.replace('_', '–').upper()}: {v}")
    return "<br>".join(e(b) for b in bits)

def price_cell(rid):
    d = DET.get(rid)
    if not d:
        return UNV, None
    if d.get("per_person_usd"):
        parts = [f"{k}: ${v}" for k, v in d["per_person_usd"].items()]
        return "<br>".join(e(p) for p in parts), d
    if d.get("per_person_estimate_usd"):
        note = d.get("per_person_estimate_basis", "")
        return f"≈ ${e(d['per_person_estimate_usd'])} pp<br><span class='src'>{e(note)}</span>", d
    return UNV, d

def couple(x):
    """Turn a per-person range into a 2-adult total, or None."""
    if not x:
        return None
    nums = re.findall(r"\d+", str(x).replace(",", ""))
    if not nums:
        return None
    return (int(nums[0]) * 2, int(nums[-1]) * 2)

# ---------------------------------------------------------------- index
def build_index():
    n_ver = sum(1 for h in HOTELS["hotels"] if h["price_status"] == "verified")
    n_unavail = len(HOTELS["unavailable_for_preferred_window"])
    priced = sorted([h for h in HOTELS["hotels"] if h.get("total_usd")], key=lambda h: h["total_usd"])
    cheapest = priced[0]
    top = SCORES[0]
    star = [r for r in MICHELIN["restaurants"] if r["distinction_class"] in ("two_star", "one_star")]
    bib = [r for r in MICHELIN["restaurants"] if r["distinction_class"] == "bib_gourmand"]
    rec = [r for r in MICHELIN["restaurants"] if r["distinction_class"] == "recommended"]

    body = f"""
<h1>Las Vegas, February–March 2027</h1>
<p class="lead">A Michelin-focused plan for two adults, built line by line from official sources,
with every gap left visibly blank instead of filled in. <strong>Snapshot 2026-11-25.</strong></p>

<div class="grid">
  <div class="kpi"><small>MICHELIN stars in Vegas</small><b>4</b>
    <span class="src">1 two-star + 3 one-star, 2026 Southwest guide</span></div>
  <div class="kpi"><small>Bib Gourmand / Recommended</small><b>3 / 17</b>
    <span class="src">Las Vegas entries only</span></div>
  <div class="kpi"><small>Hotels priced, 7 nights</small><b>{n_ver}</b>
    <span class="src">15–22 Feb 2027, 2 adults</span></div>
  <div class="kpi"><small>Cheapest verified 7-night</small><b>${cheapest['total_usd']:,}</b>
    <span class="src">{e(cheapest['name'])} · excludes resort fees</span></div>
</div>

<div class="errbox">
<strong>Read this first — three findings that change the plan</strong>
<ol>
<li><strong>Las Vegas has no subway.</strong> Your “subway or bus” requirement resolves to
<em>bus + monorail only</em>. Every transit time on this site is a real Google Maps
bus/monorail route, not a metro estimate. See <a href="transit.html">Transit</a>.</li>
<li><strong>One hotel will not cover all 24 restaurants inside 60 minutes.</strong>
The venues split into three clusters — Strip core (12), Chinatown/Spring Mountain Rd (7) and
Downtown/Arts District (2) — and only a few routes have actually been measured. Chinatown is
29–49 minutes by bus from the hotels tested, which is inside the rule; the far-south and far-west
venues are <span class="unv">unmeasured</span>, not assumed to be close. See <a href="transit.html">Transit</a>.</li>
<li><strong>Your preferred dates are only 3 nights.</strong> 15–18 Feb 2027 conflicts with the
1–2 week trip length. This plan prices 15–22 Feb (7 nights) as the working proposal, starting on
your preferred date. See <a href="questions.html">Open Questions</a>.</li>
</ol>
</div>

<h2>What the evidence supports</h2>
<div class="tblwrap"><table>
<thead><tr><th>Question you asked</th><th>Status</th><th>Answer / where it lives</th></tr></thead>
<tbody>
<tr><td>Best hotels by price, location, amenities</td><td class="ok">Answered (partial)</td>
<td><a href="hotels.html">{n_ver} hotels with verified 7-night totals</a> + a transparent ranking formula</td></tr>
<tr><td>Private bathroom, queen bed or bigger</td><td>Partially answered</td>
<td>Only 2 hotels had a private bathroom confirmed in the listing text; the rest are <span class="unv">unverified</span> and flagged</td></tr>
<tr><td>Michelin stars vs. just listed in the guide</td><td class="ok">Answered</td>
<td><a href="michelin.html">24 venues, distinction-labelled</a> from the official Michelin press release</td></tr>
<tr><td>Michelin clusters near each hotel</td><td>Partially answered</td>
<td><a href="transit.html">Measured matrix</a> — 5 hotel→restaurant pairs routed, rest blank</td></tr>
<tr><td>Rank hotels by Michelin reach within 1 hour</td><td>Partially answered</td>
<td><a href="hotels.html">Ranking table</a>, with reach shown only where measured</td></tr>
<tr><td>7-night total price per hotel</td><td class="ok">Answered</td>
<td><a href="hotels.html">Hotels</a> / <a href="budget.html">Budget</a> — Booking.com quotes, resort fees excluded</td></tr>
<tr><td>Cheapest time to book</td><td class="bad">Not verifiable</td>
<td>Two windows compared; no official “best time to book” exists. <a href="questions.html">Open Questions</a> explains</td></tr>
<tr><td>Restaurant cost for 2 adults</td><td>Partially answered</td>
<td>Guy Savoy and Kabuto have exact official prices; the other starred venues publish none → <span class="unv">unverified</span></td></tr>
<tr><td>YouTube / TikTok / Instagram per venue</td><td>Partially answered</td>
<td>6 venues have verified creator links; TikTok/Instagram could not be crawled, so they are blank, not guessed</td></tr>
<tr><td>Official site link per row</td><td class="ok">Answered</td>
<td>Every restaurant and hotel row links its own site</td></tr>
<tr><td>Open days / hours / exceptions</td><td>Partially answered</td>
<td>7 venues have official hours incl. closed days; the rest are <span class="unv">unverified</span></td></tr>
<tr><td>Activities within an hour</td><td>Partially answered</td>
<td><a href="activities.html">7 activities</a>, 2 explicitly outside the rule</td></tr>
</tbody></table></div>

<h2>Recommended starting point</h2>
<div class="okbox">
<p><strong>Top ranked hotel in the measured set:</strong> {e(top['hotel']['name'])}
— score {top['score']}/100, ${top['hotel']['total_usd']:,} for 7 nights.
Reasoning is arithmetic, not opinion: {top['n_within']} of {top['n_measured']} measured
MICHELIN venues reachable within 60 minutes, value {top['value']}/100, guest score {top['guest']}/100.</p>
<p><strong>Honest caveat:</strong> that hotel has only {top['n_measured']} measured route(s).
A hotel with zero measurements cannot win the ranking, and a hotel with one good measurement
can look better than it is. Expanding the matrix is the #1 open task on
<a href="flagged.html">Flagged for Review</a>.</p>
</div>

<h2>How to use this site</h2>
<div class="grid">
<div class="card"><h3><a href="hotels.html">Hotels</a></h3><p class="src">Verified 7-night totals, bed type, bathroom evidence, ranked Michelin reach.</p></div>
<div class="card"><h3><a href="michelin.html">MICHELIN</a></h3><p class="src">Stars vs. Bib vs. listed-only, with official hours and prices where published.</p></div>
<div class="card"><h3><a href="transit.html">Transit</a></h3><p class="src">Which venues sit inside the 60-minute rule, and from which hotel.</p></div>
<div class="card"><h3><a href="itinerary.html">Itinerary</a></h3><p class="src">A 7-night draft that respects opening days.</p></div>
<div class="card"><h3><a href="questions.html">Open Questions</a></h3><p class="src">What must be answered before you can decide, and how to find it.</p></div>
<div class="card"><h3><a href="flagged.html">Flagged for Review</a></h3><p class="src">Every irregularity found, with the source that needs a human eye.</p></div>
</div>
"""
    return page("index.html", "Overview", body)

# ---------------------------------------------------------------- hotels
def build_hotels():
    rows = ""
    for i, s in enumerate(SCORES, 1):
        h = s["hotel"]
        reach = (f"{s['n_within']}/{s['n_measured']} measured ≤60 min" if s["n_measured"]
                 else '<span class="unv">not measured</span>')
        bed = h.get("bed_verified") or None
        bedcell = cell(bed) if bed else UNV
        if h.get("bed_meets_req") is True:
            bedcell += ' <span class="ok">✓</span>'
        elif h.get("bed_meets_req") == "partial":
            bedcell += ' <span class="unv">partial</span>'
        bath = h.get("private_bathroom")
        bathcell = ('<span class="ok">confirmed</span>' if bath and bath.startswith("verified")
                    else UNV)
        score = f"{s['score']}" if s["score"] is not None else UNV
        rows += f"""<tr>
<td class="num"><span class="rank">{i}</span></td>
<td><a href="{e(h['official_site'])}" target="_blank" rel="noopener">{e(h['name'])}</a>
  <div class="src">{e(h['area'])}</div></td>
<td class="num">${h['total_usd']:,}<div class="src">${h['per_night_usd']}/night</div></td>
<td>{e(h.get('room_quoted') or '')}</td>
<td>{bedcell}</td>
<td>{bathcell}</td>
<td class="num">{h.get('guest_score')}<div class="src">{e(h.get('guest_score_label') or '')}</div></td>
<td>{reach}</td>
<td class="num"><strong>{score}</strong></td>
<td class="src"><a href="{e(h['booking_url'])}" target="_blank" rel="noopener">price</a></td>
</tr>"""

    unav = ""
    for u in HOTELS["unavailable_for_preferred_window"]:
        unav += f"""<tr><td><a href="{e(u['official_site'])}" target="_blank" rel="noopener">{e(u['name'])}</a></td>
<td class="no">{e(u['status_2027-02-15_22'])}</td><td>{e(u['alternative_7_nights'])}</td>
<td class="src"><a href="{e(u['booking_url'])}" target="_blank" rel="noopener">check</a></td></tr>"""

    body = f"""
<h1>Hotels</h1>
<p class="lead">7 nights, 2 adults, 1 room, <strong>15–22 February 2027</strong>.
Prices are Booking.com totals captured 2026-11-25 and <strong>exclude Las Vegas resort fees</strong>,
which run roughly $25–$55 per night and are charged at the property.</p>

<div class="warnbox">
<strong>Scoring formula, stated up front so you can disagree with it:</strong>
Reach to MICHELIN venues 55% · price value 20% · guest score 15% · bed fit 10%.
Weights are re-normalised when a component is missing. Hotels with <em>no</em> measured transit
route cannot score on reach and are labelled <span class="unv">not measured</span> — they are not
penalised to zero silently, but they also cannot rank first on reach they never proved.
</div>

<h2>Ranked hotels</h2>
<div class="tblwrap"><table>
<thead><tr><th>#</th><th>Hotel</th><th>7-night total</th><th>Room quoted</th>
<th>Bed</th><th>Private bath</th><th>Guest</th><th>MICHELIN ≤60 min</th><th>Score</th><th>Source</th></tr></thead>
<tbody>{rows}</tbody></table></div>
<p class="src">Bed & bathroom columns come from the room description on the booking listing.
“Confirmed” means the listing text explicitly stated a bathroom inside a private apartment —
nothing weaker was accepted as proof of a <em>private</em> bathroom in a shared-property setting.</p>

<h2>Unavailable for your preferred window</h2>
<div class="tblwrap"><table>
<thead><tr><th>Hotel</th><th>Status 15–22 Feb 2027</th><th>Alternative offered</th><th>Source</th></tr></thead>
<tbody>{unav}</tbody></table></div>
<p class="src">Four flagship Strip properties were already sold out or blocked for that week
15 months out. If any of them is a must-stay, the trip dates have to move — that is a decision
for <a href="questions.html">Open Questions</a>.</p>

<h2>What is still missing here</h2>
<ul>
<li><strong>Resort fees per hotel</strong> — not verified. Without them the true 7-night cost is
understated, and cheap-looking hotels can flip order.</li>
<li><strong>Private bathroom</strong> — only 2 of {len(HOTELS['hotels'])} verified.</li>
<li><strong>Queen-or-bigger guarantee</strong> — several cheap rooms say “Room Type Assigned on
Arrival”, which does <em>not</em> guarantee the bed you asked for.</li>
</ul>
"""
    return page("hotels.html", "Hotels", body)

# ---------------------------------------------------------------- michelin
def build_michelin():
    order = {"2 Stars": 0, "1 Star": 1, "Bib Gourmand": 2, "Recommended": 3}
    rs = sorted(MICHELIN["restaurants"], key=lambda r: (order[r["distinction"]], r["name"]))
    rows = ""
    for r in rs:
        d = DET.get(r["id"], {})
        h = hours_text(d) if d else None
        hcell = h if h else UNV
        if d and d.get("hours_exceptions"):
            exc = e(d["hours_exceptions"])
        else:
            exc = UNV
        p, _ = price_cell(r["id"])
        c = couple(d.get("per_person_estimate_usd")) if d else None
        tot = (f"${c[0]:,}–${c[1]:,} for 2" if c else UNV)
        s = SOC.get(r["id"], {})
        links = []
        for y in s.get("youtube", []):
            links.append(f'<a href="{e(y["url"])}" target="_blank" rel="noopener">YT</a>')
        if s.get("instagram_posts"):
            links.append(f'<a href="{e(s["instagram_posts"][0])}" target="_blank" rel="noopener">IG</a>')
        linkcell = " · ".join(links) if links else UNV
        rows += f"""<tr>
<td>{distinction_tag(r['distinction'])}</td>
<td><a href="{e(r['official_site'])}" target="_blank" rel="noopener">{e(r['name'])}</a>
<div class="src">{e(r['cuisine'])}</div></td>
<td class="src">{e(r['address_official'])}</td>
<td>{hcell}</td>
<td class="src">{exc}</td>
<td>{p}</td>
<td class="num">{tot}</td>
<td>{linkcell}</td>
</tr>"""

    body = f"""
<h1>MICHELIN Guide — Las Vegas</h1>
<p class="lead">Source of record: the official MICHELIN press release for the
<strong>2026 MICHELIN Guide American Southwest</strong> (inaugural edition, revealed 26 Aug 2026,
Las Vegas). Distinctions below are quoted from that release only.</p>

<div class="okbox">
<strong>Star vs. “just listed” — the distinction you asked for:</strong>
A <span class="tag t2">2 Stars</span> / <span class="tag t1">1 Star</span> venue holds an actual
MICHELIN star. A <span class="tag tb">Bib Gourmand</span> has <em>no star</em> — it is a
good-value award. <span class="tag tr">Recommended</span> means <em>listed in the guide with no award
at all</em>. Conflating these three is the most common error in Vegas “Michelin restaurant” lists.
</div>

<div class="grid">
<div class="kpi"><small>Two stars</small><b>1</b><span class="src">Restaurant de Joël Robuchon</span></div>
<div class="kpi"><small>One star</small><b>3</b><span class="src">é by José Andrés · Guy Savoy · L'Atelier</span></div>
<div class="kpi"><small>Bib Gourmand</small><b>3</b><span class="src">no star</span></div>
<div class="kpi"><small>Recommended only</small><b>17</b><span class="src">no star, no Bib</span></div>
</div>

<h2>All 24 Las Vegas selections</h2>
<div class="tblwrap"><table>
<thead><tr><th>Award</th><th>Restaurant</th><th>Address (official)</th>
<th>Open days &amp; hours</th><th>Exceptions</th><th>Cost / person</th>
<th>2 adults</th><th>Video</th></tr></thead>
<tbody>{rows}</tbody></table></div>

<p class="src">Hours and prices are taken from each venue's own website. Where a venue publishes no
price, the cell stays <span class="unv">unverified</span> rather than being estimated. “2 adults”
doubles a published per-person figure and is labelled ≈ where the source is a range.</p>

<h2>The three MICHELIN clusters in this city</h2>
<div class="card">
<h3>1 · The Strip core (12 venues)</h3>
<p class="src">MGM Grand (2 starred), Cosmopolitan (1 starred + 1 Bib), Caesars Palace (1 starred),
Bellagio, ARIA, Wynn, Venetian/Palazzo (4), Resorts World. This is where all four stars live.
A Strip hotel puts most of this cluster inside walking distance — no bus needed.</p>
</div>
<div class="card">
<h3>2 · Chinatown / Spring Mountain Rd (7 venues)</h3>
<p class="src">Kabuto, Kame Omakase, Lamaii, Partage, Pho Ga Bac Bac, Sparrow + Wolf, and the
Bib Gourmand YEN Viet Kitchen. Almost entirely <em>Recommended</em> rather than starred, but this is
the highest density of guide-listed food in the city and it is 29–49 minutes by bus from the
measured hotels.</p>
</div>
<div class="card">
<h3>3 · Downtown / Arts District (2 venues)</h3>
<p class="src">Esther's Kitchen (Bib Gourmand) and SoulBelly BBQ (Recommended), both on S Main St.
Pairs naturally with the Mob Museum and the 18b Arts District on the same day.</p>
</div>

<h2>What is unverified on this page</h2>
<ul>
<li><strong>Prices for the 4 starred restaurants:</strong> only Guy Savoy (à la carte) and
Kabuto (tasting menu PDF) publish numbers. Joël Robuchon, é by José Andrés and L'Atelier publish
none → blank.</li>
<li><strong>Hours for 9 venues:</strong> blank. Their own sites did not render a service-hours
block to a public reader.</li>
<li><strong>TikTok and Instagram:</strong> not crawlable from this environment. Only Instagram
posts embedded in Kabuto's own website are given. Everything else is blank, not invented.</li>
<li><strong>MICHELIN's own guide pages</strong> could not be fetched directly (blocked); the
selection was verified through the official Michelin press release on michelin.com and
cross-checked against the LVCVA (Las Vegas CVA) Michelin page.</li>
</ul>
"""
    return page("michelin.html", "MICHELIN", body)

# ---------------------------------------------------------------- transit
def build_transit():
    hname = {h["id"]: h["name"] for h in HOTELS["hotels"]}
    rname = {r["id"]: r["name"] for r in MICHELIN["restaurants"]}
    rows = ""
    for r in TRANSIT["rows"]:
        cls = "ok" if r["minutes"] <= 60 else "no"
        rows += f"""<tr>
<td>{e(hname.get(r['hotel_id'], r['hotel_id']))}</td>
<td>{e(rname.get(r['restaurant_id'], r['restaurant_id']))}</td>
<td class="num"><span class="{cls}">{r['minutes']} min</span></td>
<td>{e(r['route'])}</td>
<td class="src">{e(r['note'])}</td>
<td class="src"><a href="{e(r['query'])}" target="_blank" rel="noopener">route</a></td>
</tr>"""

    modes = "".join(f"<li><strong>{e(m['mode'])}</strong> — {e(m['operator'])}. {e(m['note'])}</li>"
                    for m in TRANSIT["travel_modes_available"])

    body = f"""
<h1>Transit &amp; the 60-minute rule</h1>
<p class="lead">Your requirement: every restaurant and activity within one hour by
<em>subway or bus</em> of the hotel. Measured with live Google Maps transit routing.</p>

<div class="errbox">
<strong>Correction to a premise: Las Vegas has no subway, metro or light rail.</strong>
There is no underground or surface rapid-transit rail system on the Strip. What exists —
and what Google Maps actually returned for every query — is:
<ul>{modes}</ul>
So “subway or bus” here means <strong>bus + monorail</strong>. Any plan claiming subway travel
inside Las Vegas would be wrong.
</div>

<h2>Measured routes</h2>
<div class="tblwrap"><table>
<thead><tr><th>From hotel</th><th>To restaurant</th><th>Transit time</th><th>Route used</th>
<th>Note</th><th>Source</th></tr></thead>
<tbody>{rows}</tbody></table></div>

<div class="warnbox">
<strong>This table is deliberately partial.</strong> Only the pairs actually routed are shown.
A blank is <em>“not measured”</em>, never <em>“far”</em>. Expanding to the full
{len(HOTELS['hotels'])} × {len(MICHELIN['restaurants'])} grid is the top task on
<a href="flagged.html">Flagged for Review</a>.
</div>

<h2>What the measured routes already tell you</h2>
<div class="grid">
<div class="card"><h3>Chinatown is genuinely reachable by bus</h3>
<p>Gold Coast → Kabuto is <strong>29 minutes</strong>; Flamingo → Kabuto is 46 minutes;
Signature/MGM Grand → Kabuto is 49 minutes. All inside the 60-minute rule, all on
ordinary residential RTC routes (202, 203, 103).</p></div>
<div class="card"><h3>The Strip core needs no bus at all</h3>
<p>MGM Grand → Guy Savoy is a 28-minute transit estimate for a trip that is physically a
walk across the Blvd overpass. Trump International → Wing Lei came back as a 15-minute walk.
For Strip-internal venues, “transit time” overstates the effort.</p></div>
<div class="card"><h3>Hotel location beats hotel quality</h3>
<p>The cheapest hotel measured (Gold Coast, $768/7 nights) beat a hotel nearly twice its price
on Chinatown access. If the Michelin list is the reason for the trip, geography is the lever.</p></div>
</div>

<h2>Caveats that matter for a February trip</h2>
<ul>
<li>Times were captured pre-dawn on a Wednesday. Evening service on a fight-night or convention
week can run longer.</li>
<li>Las Vegas summer heat is irrelevant for February, but late-night frequency is not — check the
last bus before a 9:30 PM dinner at Wing Lei.</li>
<li>The monorail does not serve Chinatown or Downtown. Anything on Spring Mountain Rd is bus-only.</li>
</ul>
"""
    return page("transit.html", "Transit", body)

# ---------------------------------------------------------------- activities
def build_activities():
    rows = ""
    for a in ACTIVITIES["activities"]:
        price = (f"${a['per_person_usd']}" if a.get("per_person_usd") not in (None, "")
                 else UNV)
        rows += f"""<tr>
<td><a href="{e(a['official_site'])}" target="_blank" rel="noopener">{e(a['name'])}</a>
<div class="src">{e(a['category'])}</div></td>
<td class="src">{e(a['location'])}</td>
<td>{cell(a.get('hours'))}</td>
<td>{cell(a.get('open_days'))}</td>
<td class="src">{cell(a.get('exceptions'))}</td>
<td class="num">{price}</td>
<td class="src">{e(a['transit_note'])}</td>
</tr>"""
    body = f"""
<h1>Activities</h1>
<p class="lead">Non-restaurant things to do, each judged against the same 60-minute rule.
Two are explicitly flagged as <em>outside</em> it rather than quietly included.</p>

<div class="tblwrap"><table>
<thead><tr><th>Activity</th><th>Location</th><th>Hours</th><th>Open days</th>
<th>Exceptions</th><th>Price pp</th><th>Transit reality</th></tr></thead>
<tbody>{rows}</tbody></table></div>

<div class="warnbox">
<strong>Hours and prices for most activities are blank on purpose.</strong>
Museum and attraction sites change hours seasonally and many do not publish a machine-readable
schedule. Rather than copy a number from a blog, the cell stays
<span class="unv">unverified</span>. Each row links the official site — that is the
one-click check.
</div>

<h2>Two activities that break your own rule</h2>
<p><strong>Red Rock Canyon</strong> and <strong>Hoover Dam</strong> are not reachable within
60 minutes by public transit. They are listed so the trade-off is visible: choosing them means
renting a car or booking a tour, which adds cost and a day. If they stay in the plan, the
hotel choice stops mattering for those days.</p>

<h2>What would make this page far better</h2>
<ul>
<li>Ticket prices in writing from each official box office.</li>
<li>Seasonal hour tables captured in the same week as the trip.</li>
<li>At least one verified YouTube walkthrough per activity — currently none are attached, because
searching produced mostly promotional reels rather than specific, checkable videos.</li>
</ul>
"""
    return page("activities.html", "Activities", body)

# ---------------------------------------------------------------- itinerary
def build_itinerary():
    open_by = {}
    for rid, d in DET.items():
        h = d.get("hours") or {}
        if h:
            open_by[rid] = "; ".join(f"{k}: {v}" for k, v in h.items())

    def r(rid):
        x = next(y for y in MICHELIN["restaurants"] if y["id"] == rid)
        return x

    days = [
        ("Mon 15 Feb", "Arrival", "Check in. Settle. Evening free — note that <strong>é by José Andrés, "
         "Joël Robuchon and Guy Savoy are all closed on Monday or Sunday</strong>, so day one is a "
         "deliberately light dining day.", None),
        ("Tue 16 Feb", "Star night #1", "é by José Andrés (1★, Tue–Sat 5:30–8:30 PM, only two "
         "seatings, books 3 months ahead) or L'Atelier (closed Tue–Wed). Then Bellagio Fountains.",
         ["e-by-jose-andres"]),
        ("Wed 17 Feb", "Chinatown by bus", "Bus out to Spring Mountain Rd. Kabuto (daily 5:30–9:00 PM, "
         "reservation only; $130 or $185 pp). Walk Spring Mountain for the rest of the cluster.",
         ["kabuto"]),
        ("Thu 18 Feb", "Your preferred end-date", "This is the last day of your stated preferred "
         "window. Keep it free, or fly home. If staying, Wing Lei (Thu open 5:30–9:30 PM) at Wynn.",
         ["wing-lei"]),
        ("Fri 19 Feb", "Downtown day", "Mob Museum + 18b Arts District; Esther's Kitchen (Bib Gourmand) "
         "and SoulBelly BBQ are both on S Main St. Hours unverified — confirm before travelling.",
         ["esthers-kitchen", "soulbelly-bbq"]),
        ("Sat 20 Feb", "Star night #2", "Restaurant de Joël Robuchon (2★, Tue–Sat 5:00–9:30 PM). "
         "Business formal. Book well ahead.", ["joel-robuchon"]),
        ("Sun 21 Feb", "Buffer / repeat", "Joël Robuchon, é and L'Atelier are all closed Sunday. "
         "Use it for Mott 32 (open daily), Ping Pang Pong, or a repeat of a favourite.", ["mott-32"]),
        ("Mon 22 Feb", "Departure", "Checkout. Note L'Atelier is open Monday if you want one last "
         "lunchtime-adjacent dinner before flying.", ["latelier-de-joel-robuchon"]),
    ]
    rows = ""
    for d, title, note, ids in days:
        links = ""
        if ids:
            for i in ids:
                x = r(i)
                hrs = open_by.get(i, "hours unverified")
                links += (f'<div style="margin-top:6px"><a href="{e(x["official_site"])}" '
                          f'target="_blank" rel="noopener">{e(x["name"])}</a> '
                          f'{distinction_tag(x["distinction"])}<div class="src">{e(hrs)}</div></div>')
        else:
            links = '<span class="src">—</span>'
        rows += f"<tr><td><strong>{e(d)}</strong></td><td>{e(title)}</td><td>{note}</td><td>{links}</td></tr>"

    body = f"""
<h1>Draft itinerary — 7 nights</h1>
<p class="lead">Sequenced around <strong>published opening days</strong>, not convenience.
The hardest constraint is real: the two-star restaurant is closed Sun–Mon, é is closed Sun–Mon,
L'Atelier is closed Tue–Wed. A naive plan will hit a locked door.</p>

<div class="tblwrap"><table>
<thead><tr><th>Date</th><th>Theme</th><th>Plan</th><th>Reservation + hours</th></tr></thead>
<tbody>{rows}</tbody></table></div>

<div class="warnbox">
<strong>Open-day collisions worth knowing before you choose dates:</strong>
<ul>
<li>Restaurant de Joël Robuchon — <strong>closed Sun &amp; Mon</strong></li>
<li>é by José Andrés — <strong>closed Sun &amp; Mon</strong>, two seatings only</li>
<li>L'Atelier de Joël Robuchon — <strong>closed Tue &amp; Wed</strong></li>
<li>Wing Lei — <strong>closed Tue &amp; Wed</strong></li>
</ul>
If the trip were only 15–18 Feb (your preferred window), you would land Mon–Thu and could
<em>not</em> eat at Robuchon or é at all. That single fact is the strongest argument for
extending to the full week.
</div>

<h2>Why this order and not another</h2>
<p>Two star-level dinners are spaced out rather than stacked, so neither is wasted on a jet-lagged
evening. Chinatown sits mid-week on a night when the buses run normally and the Strip is busiest.
Downtown is placed on a Friday so the Arts District is awake. Everything else is filler that can
absorb a cancellation.</p>
"""
    return page("itinerary.html", "Itinerary", body)

# ---------------------------------------------------------------- budget
def build_budget():
    priced = sorted([h for h in HOTELS["hotels"] if h.get("total_usd")], key=lambda h: h["total_usd"])
    opts = ""
    for h in priced[:4]:
        opts += f"""<tr><td>{e(h['name'])}</td>
<td class="num">${h['total_usd']:,}</td>
<td class="num">${h['per_night_usd']} × 7</td>
<td class="num"><span class="unv">not verified</span></td>
<td class="num"><span class="unv">add resort fee</span></td></tr>"""

    body = f"""
<h1>Budget</h1>
<p class="lead">What is known, what is knowable, and what nobody has published. This page
deliberately refuses to print a single grand total, because two of its three inputs are
unverified.</p>

<h2>Hotel — verified 7-night totals (15–22 Feb 2027)</h2>
<div class="tblwrap"><table>
<thead><tr><th>Hotel</th><th>7-night total</th><th>Basis</th><th>Resort fees</th><th>True total</th></tr></thead>
<tbody>{opts}</tbody></table></div>
<p class="src">Resort fees are the largest hidden cost in a Las Vegas hotel booking and they are
<strong>not</strong> in these numbers. A $483 headline week can become $700+ at the desk.</p>

<h2>Food — the part with real published numbers</h2>
<div class="tblwrap"><table>
<thead><tr><th>Restaurant</th><th>Award</th><th>Per person (official)</th><th>2 adults</th><th>Basis</th></tr></thead>
<tbody>
<tr><td>Guy Savoy</td><td>{distinction_tag('1 Star')}</td>
<td>$380–$640 est.</td><td class="num">$760–$1,280</td>
<td class="src">3–4 à-la-carte courses at published prices ($100–$290 each), before tax &amp; tip</td></tr>
<tr><td>Kabuto</td><td>{distinction_tag('Recommended')}</td>
<td>$130–$185 exact</td><td class="num">$260–$370</td>
<td class="src">Official 2026 menu PDF; sake pairing $62–$68 pp extra</td></tr>
<tr><td>Restaurant de Joël Robuchon</td><td>{distinction_tag('2 Stars')}</td>
<td>UNVERIFIED</td><td class="num">UNVERIFIED</td>
<td class="src">No price published on the official MGM Grand page</td></tr>
<tr><td>é by José Andrés</td><td>{distinction_tag('1 Star')}</td>
<td>UNVERIFIED</td><td class="num">UNVERIFIED</td>
<td class="src">No price published on the official page; third-party reports ~$290 pp (not official)</td></tr>
<tr><td>L'Atelier de Joël Robuchon</td><td>{distinction_tag('1 Star')}</td>
<td>UNVERIFIED</td><td class="num">UNVERIFIED</td>
<td class="src">No price published on the official page</td></tr>
<tr><td>Bib Gourmand trio</td><td>{distinction_tag('Bib Gourmand')}</td>
<td>UNVERIFIED</td><td class="num">UNVERIFIED</td>
<td class="src">Bib Gourmand promises “good food at moderate price”; no figure is published</td></tr>
</tbody></table></div>

<div class="errbox">
<strong>Why there is no grand total.</strong> A realistic food budget needs the four starred
venues. Two of the four have no published price, and Bib Gourmand has none by design. Any grand
total would be invented. What <em>can</em> be said with evidence:
<em>one Guy Savoy dinner for two is $760–$1,280 before tax and tip</em> — which is 1.6× to 2.6×
the entire cheapest hotel week.
</div>

<h2>Cost-saving levers that are actually evidenced</h2>
<ul>
<li><strong>Hotel choice is a real lever:</strong> $483 (Rio Masquerade) vs $2,493 (W Las Vegas)
for the same 7 nights, same city. A $2,010 swing.</li>
<li><strong>The Bib Gourmand trio is the value play</strong> — that is literally what the award
means. China Poblano, Esther's Kitchen, YEN Viet Kitchen.</li>
<li><strong>Kabuto is the best-value fine-dining on the list:</strong> $130 pp for a
MICHELIN-guide omakase, versus $380+ for a starred French dinner.</li>
<li><strong>Lunch/brunch at Mott 32</strong> ($-modest dishes 11:00–14:30) versus its dinner
service — same kitchen, lower bill.</li>
</ul>

<h2>What to add before committing money</h2>
<ol>
<li>Resort fee per hotel, in writing, from the hotel's own site.</li>
<li>Tax and gratuity assumptions (Clark County room tax; 20% service is normal at this tier).</li>
<li>Airfare — deliberately out of scope here; no source was fetched and none will be guessed.</li>
<li>A published price for Robuchon and é, by phone or OpenTable at booking time.</li>
</ol>
"""
    return page("budget.html", "Budget", body)

# ---------------------------------------------------------------- questions
def build_questions():
    QS = [
        ("Can the trip really be 1–2 weeks when your preferred window is 3 nights?",
         "No — 15–18 Feb 2027 is 3 nights. The plan prices 7 nights (15–22 Feb).",
         "You choose: 7 nights from 15 Feb, or a different length.",
         "Resolved by decision only",
         "You said both '1–2 weeks' and 'preferred 15–18 Feb'. This site assumed 7 nights starting 15 Feb."),
        ("Which dates inside 15 Feb – 23 Mar 2027 are cheapest?",
         "Unknown. Only two windows were swept, and they were not like-for-like (one included taxes).",
         "A full sweep of every 7-night window in the range, all with taxes included.",
         "Partially resolved",
         "Top open item. Needs ~5 Booking.com sweeps and one normalisation rule."),
        ("Is there a convention, rodeo, race or fight in that window?",
         "No official source was checked in this session.",
         "Las Vegas Convention and Visitors Authority calendar + major venue calendars.",
         "Unresolved — highest risk",
         "An event week can double a hotel price and invalidate every number on the Hotels page."),
        ("What are the resort fees per hotel?",
         "Not verified for any hotel.",
         "Each hotel's own 'fees' page — that is the authoritative source.",
         "Unresolved",
         "Without this, the 7-night totals understate true cost by hundreds of dollars."),
        ("Do the cheap rooms actually have a queen/king bed?",
         "No. Rio, Flamingo and Harrah's quote 'assigned on arrival'.",
         "Book a specific named room type and confirm the bed in writing.",
         "Partially resolved",
         "The stated requirement (queen or bigger) is not guaranteed on the cheapest rates."),
        ("Is the bathroom private?",
         "Confirmed for 2 of 15 hotels only.",
         "Filter booking listings on 'private bathroom' and confirm per room, not per property.",
         "Unresolved",
         "A shared-bathroom guesthouse can slip through on price alone."),
        ("Do all 24 restaurants fall inside 60 minutes of one hotel?",
         "Unknown. Only 5 routes were measured.",
         "Complete the 15 × 24 matrix, then count.",
         "Unresolved",
         "This is the core ranking input; today it rests on a small sample."),
        ("What does Robuchon / é / L'Atelier cost per person?",
         "Not published by the venues.",
         "Phone the reservation lines, or take the price OpenTable shows at booking.",
         "Unresolved",
         "The two-star dinner is likely the single largest line in the budget."),
        ("Are the restaurants open on the exact nights you would visit?",
         "Verified for 7 venues; 9 still blank.",
         "Each venue's own site in the week before travel.",
         "Partially resolved",
         "Robuchon and é are closed Sun–Mon; L'Atelier and Wing Lei closed Tue–Wed."),
        ("Which activities are worth the time?",
         "Seven activities listed, no ticket prices or hours verified.",
         "Official box-office pages for dates and prices.",
         "Unresolved",
         "Currently the least evidenced page on the site."),
        ("Can you actually get to Chinatown by bus in under an hour at dinner time?",
         "Yes in the off-peak measurement: 29–49 minutes.",
         "Re-run the route at 6–7 PM on a Friday.",
         "Partially resolved",
         "Pre-dawn timings flatter bus routes."),
        ("Does the private-bathroom + queen-bed filter change the hotel ranking?",
         "Possibly — 13 of 15 hotels do not have that pair confirmed.",
         "Re-query Booking.com with both filters on and re-run the ranking.",
         "Unresolved",
         "The ranking could reshuffle entirely."),
    ]
    rows = ""
    for i, (q, a, action, status, why) in enumerate(QS, 1):
        cls = "ok" if status in ("Resolved",) else ("warn" if "Partial" in status else "no")
        rows += f"""<tr><td class="num">{i}</td>
<td class="q">{e(q)}<div class="src">{e(why)}</div></td>
<td>{e(a)}</td>
<td class="src">{e(action)}</td>
<td><span class="{cls}">{e(status)}</span></td></tr>"""

    body = f"""
<h1>Open Questions</h1>
<p class="lead">A decision cannot be made responsibly on the current evidence. This is the
honest list of what is missing, what it would change, and exactly how to get it.</p>

<div class="tblwrap"><table>
<thead><tr><th>#</th><th>Question</th><th>What we know</th>
<th>How to resolve it</th><th>Status</th></tr></thead>
<tbody>{rows}</tbody></table></div>

<h2>The four that actually block a booking</h2>
<div class="errbox">
<ol>
<li><strong>Trip length.</strong> 3 nights (your preferred window) versus 1–2 weeks is a 2× to 4×
difference in every other number. Nothing else can be costed until this is fixed.</li>
<li><strong>Event calendar.</strong> One convention week can invalidate every price quoted here.</li>
<li><strong>Resort fees.</strong> They are charged to every guest and are missing from all 15 totals.</li>
<li><strong>Robuchon / é tasting-menu prices.</strong> The biggest single expense has no
published figure.</li>
</ol>
</div>

<h2>How to discover the missing information — concretely</h2>
<ul>
<li><strong>Prices:</strong> run the same Booking.com search with every 7-night window from
15 Feb to 23 Mar, with the "includes taxes and fees" toggle on, and record each. Five sweeps,
one spreadsheet.</li>
<li><strong>Events:</strong> the LVCVA publishes a convention calendar; cross-check the
Las Vegas Motor Speedway, T-Mobile Arena, Allegiant Stadium and the rodeo calendar
(PBR / NFR are typically elsewhere in the year but must be confirmed, not assumed).</li>
<li><strong>Resort fees:</strong> search each hotel's site for "resort fee" and record the figure
and its date.</li>
<li><strong>Menus and prices:</strong> OpenTable reservation flows for Robuchon, é and L'Atelier
show the current menu price at the point of booking.</li>
<li><strong>Hours:</strong> the official pages linked from the MICHELIN table; re-check in the
week before travel because all four starred venues post temporary holiday hours.</li>
<li><strong>Transit:</strong> complete the matrix at 6–8 PM local time, since that is when you
would actually be travelling to dinner.</li>
</ul>
"""
    return page("questions.html", "Open Questions", body)

# ---------------------------------------------------------------- suggestions
def build_suggestions():
    body = """
<h1>Suggestions for Review</h1>
<p class="lead">Proposed improvements to this site and to the plan. None have been implemented.
Review each, choose the ones you want, and they can be built next.</p>

<div class="warnbox"><strong>How to use this page.</strong> Every item states the problem it
solves, the effort, and what decision changes if you adopt it. Nothing here is applied yet.</div>

<h2>Tier 1 — changes that would most improve a decision</h2>

<details open><summary>S1 · Complete the 15 × 24 transit matrix (replaces guesswork with a number)</summary>
<p><strong>Problem:</strong> hotel ranking currently rests on 5 measured routes out of 360 possible pairs.</p>
<p><strong>Proposal:</strong> route every hotel→restaurant pair at 6–8 PM local time and rebuild the
ranking from the full grid. Then "restaurants within 60 minutes" becomes a real, defensible count
for every hotel instead of a small-sample estimate.</p>
<p><strong>Effort:</strong> high (automated routing + a manual spot-check).
<strong>Decision it unlocks:</strong> which hotel to book.</p></details>

<details><summary>S2 · Add resort fees and taxes to every hotel total</summary>
<p><strong>Problem:</strong> the headline 7-night figures are understated and can reorder the list.</p>
<p><strong>Proposal:</strong> scrape each hotel's own fee page and show a "true 7-night total"
column next to the booking-site total.</p>
<p><strong>Effort:</strong> medium. <strong>Decision it unlocks:</strong> which hotel is genuinely cheapest.</p></details>

<details><summary>S3 · Sweep every 7-night window in the allowed date range</summary>
<p><strong>Problem:</strong> only two date windows were compared, and they were not like-for-like.</p>
<p><strong>Proposal:</strong> for a fixed shortlist of 4–5 hotels, price every 7-night window from
15 Feb to 23 Mar 2027 with taxes included, then chart the cheapest.</p>
<p><strong>Effort:</strong> medium. <strong>Decision it unlocks:</strong> the dates themselves.</p></details>

<details><summary>S4 · Verify the private-bathroom + queen-bed requirement per room</summary>
<p><strong>Problem:</strong> this was a hard requirement and it is confirmed for 2 of 15 hotels.</p>
<p><strong>Proposal:</strong> re-run the search with both filters on, then keep only rooms whose
description guarantees a specific bed type. Drop "assigned on arrival" rates entirely.</p>
<p><strong>Effort:</strong> low. <strong>Decision it unlocks:</strong> eliminates half the cheap
options honestly instead of optimistically.</p></details>

<h2>Tier 2 — quality of life</h2>
<details><summary>S5 · Event calendar overlay</summary>
<p>Import the LVCVA convention calendar and major-venue schedules into the date picker, so a
traveller can see which weeks are inflated before falling in love with a price.</p></details>

<details><summary>S6 · TikTok / Instagram verification pass</summary>
<p>Only Kabuto has social posts verified (embedded on its own site). A manual pass per venue —
checking the venue's own link-in-bio — would fill the remaining 17 rows without guessing.</p></details>

<details><summary>S7 · Price the starred dinners via OpenTable instead of leaving them blank</summary>
<p>OpenTable shows the current menu price at the reservation step. That is a citable,
time-stamped figure and would complete the food budget.</p></details>

<details><summary>S8 · Add a "walk vs transit" column</summary>
<p>MGM Grand → Guy Savoy took "28 minutes by transit" for a walkable 1.2 miles. For Strip-internal
venues, transit time is the wrong metric and currently makes the Strip look worse than it is.</p></details>

<h2>Tier 3 — for later</h2>
<details><summary>S9 · A single-file PDF export of the final plan</summary>
<p>Useful for travelling without signal, and for handing to a hotel concierge.</p></details>
<details><summary>S10 · Saved-search / re-price alerts</summary>
<p>Because "cheapest time to book" is unverifiable, the honest substitute is a monitored
free-cancellation booking plus an alert when the same dates drop.</p></details>
<details><summary>S11 · Accessibility and dress-code column</summary>
<p>Four venues impose dress codes (business formal at Robuchon, upscale at é) and minor-age
restrictions. That is decision-relevant and currently only appears in notes.</p></details>

<h2>Site changes I would make to the design itself</h2>
<ul>
<li><strong>Per-page "what changed since last snapshot"</strong> — a diff strip so a returning
reader sees movement rather than re-reading everything.</li>
<li><strong>Confidence colour on every cell</strong> — green verified / amber partial / red absent,
so the page can be skimmed at a glance.</li>
<li><strong>A printable one-pager</strong> carrying only the 12 decided facts.</li>
<li><strong>Sticky filter bar</strong> on hotels (max price, min guest score, inside-60-min only).</li>
</ul>
"""
    return page("suggestions.html", "Suggestions", body)

# ---------------------------------------------------------------- verification
def build_verification():
    rows = [
        ("MICHELIN distinctions (4 stars, 3 Bib, 17 Recommended)", "verified",
         "michelin.com official press release",
         "https://www.michelin.com/en/publications/products-and-services/michelin-guide-reveals-first-ever-southwest-restaurant-selection-in-the-u-s",
         "Cross-checked against visitlasvegas.com (LVCVA); both agree. Note the release was published 31 Aug 2026 but the ceremony was 26 Aug 2026."),
        ("MICHELIN restaurant official links", "verified", "visitlasvegas.com Michelin page",
         "https://www.visitlasvegas.com/michelin-guide-restaurants/",
         "LVCVA is the official Las Vegas destination authority and links each venue's own site."),
        ("Restaurant addresses", "verified", "michelin.com press release table",
         "https://www.michelin.com/en/publications/products-and-services/michelin-guide-reveals-first-ever-southwest-restaurant-selection-in-the-u-s", ""),
        ("Joël Robuchon hours (closed Mon & Sun)", "verified", "MGM Grand official restaurant page",
         "https://mgmgrand.mgmresorts.com/en/restaurants/joel-robuchon-french-restaurant.html", ""),
        ("L'Atelier hours (closed Tue & Wed)", "verified", "MGM Grand official restaurant page",
         "https://mgmgrand.mgmresorts.com/en/restaurants/latelier-joel-robuchon-french-restaurant.html", ""),
        ("é by José Andrés hours (closed Sun & Mon; 2 seatings)", "verified",
         "Cosmopolitan official restaurant page",
         "https://cosmopolitanlasvegas.mgmresorts.com/en/restaurants/e-by-jose-andres.html", ""),
        ("Mott 32 hours incl. weekend brunch", "verified", "Venetian official restaurant page",
         "https://www.venetianlasvegas.com/dining/restaurants/mott-32.html",
         "Original URL /restaurants/mott-32.html redirected; the /dining/restaurants/ path is canonical."),
        ("Wing Lei hours (closed Tue & Wed)", "verified", "Wynn official restaurant page",
         "https://www.wynnlasvegas.com/dining/fine-dining/wing-lei", ""),
        ("Kabuto hours + tasting-menu prices", "verified", "Kabuto official site and 2026 menu PDF",
         "https://www.kabutolv.com/s/kabuto-menu2026.pdf",
         "Menu PDF served under filename kabuto-menu2023 in the PDF title metadata; content is the 2026 menu. Flagged."),
        ("Guy Savoy à-la-carte prices (effective 11.5.2026)", "verified",
         "Caesars Palace official menu page",
         "https://www.caesars.com/caesars-palace/restaurants/restaurant-guy-savoy/main-menu", ""),
        ("Hotel 7-night totals, 15–22 Feb 2027", "verified (with caveat)", "Booking.com search results",
         "https://www.booking.com/searchresults.en-us.html?ss=Las+Vegas&checkin=2027-02-15&checkout=2027-02-22&group_adults=2&no_rooms=1&selected_currency=USD&order=class",
         "Booking.com is an intermediary, not an official hotel source. Resort fees excluded. Prices move hourly."),
        ("Hotel unavailability (Park MGM, ARIA, Bellagio, Cosmopolitan, Caesars)", "verified (with caveat)",
         "Booking.com property results", "https://www.booking.com/hotel/us/aria-resort-casino.html",
         "Intermediary evidence of sold-out/blocked status; hotels' own engines were not queried."),
        ("Transit times", "verified (with caveat)", "Google Maps live transit routing",
         "https://www.google.com/maps/dir/?api=1&origin=Flamingo+Las+Vegas&destination=Kabuto+Edomae+Sushi+Las+Vegas&travelmode=transit",
         "Live estimate at query time, pre-dawn. Not a timetable."),
        ("No subway in Las Vegas", "verified", "Google Maps returned bus/monorail only for every query",
         "https://www.rtcsnv.com/", "RTC operates buses + the Strip & Downtown Express; the monorail is private."),
        ("Restaurant prices for Robuchon / é / L'Atelier / Bib Gourmand", "NOT VERIFIED", "no official price published",
         "https://mgmgrand.mgmresorts.com/en/restaurants/joel-robuchon-french-restaurant.html",
         "Left blank on the site. Do not treat as free."),
        ("Resort fees", "NOT VERIFIED", "no hotel fee page fetched", "", "Missing from every total."),
        ("TikTok / Instagram for 17 venues", "NOT VERIFIED", "cannot crawl TikTok or Instagram from this environment", "",
         "Blank rather than guessed."),
        ("Activities hours and ticket prices", "NOT VERIFIED", "official pages list but hours not captured", "",
         "Flagged for review."),
        ("Private bathroom for 13 of 15 hotels", "NOT VERIFIED", "booking listing did not state it", "",
         "Only the two Signature apartment listings explicitly state '1 bathroom'."),
    ]
    rows_html = ""
    for what, status, src, url, note in rows:
        cls = "ok" if status.startswith("verified") else "no"
        link = f'<a href="{e(url)}" target="_blank" rel="noopener">{e(src)}</a>' if url else e(src)
        rows_html += f"""<tr><td>{e(what)}</td><td><span class="{cls}">{e(status)}</span></td>
<td class="src">{link}</td><td class="src">{e(note)}</td></tr>"""

    body = f"""
<h1>Verification log</h1>
<p class="lead">Every claim on this site, the source it came from, and whether it survived checking.
Anything that did not is listed as NOT VERIFIED and renders blank in the tables.</p>

<div class="grid">
<div class="kpi"><small>Claims checked</small><b>{len(rows)}</b></div>
<div class="kpi"><small>Verified</small><b>{sum(1 for r in rows if r[1].startswith('verified'))}</b></div>
<div class="kpi"><small>Not verified</small><b>{sum(1 for r in rows if not r[1].startswith('verified'))}</b></div>
<div class="kpi"><small>Snapshot</small><b style="font-size:17px">25 Nov 2026</b></div>
</div>

<div class="tblwrap"><table>
<thead><tr><th>Claim</th><th>Status</th><th>Source</th><th>Notes / irregularities</th></tr></thead>
<tbody>{rows_html}</tbody></table></div>

<h2>Method, stated plainly</h2>
<ol>
<li>Distinctions were read from the official Michelin publication, not from news summaries.</li>
<li>Hours and prices were read from each venue's own website, not from aggregators.</li>
<li>Prices were captured live with dates and window, and the capture URL is kept with the number.</li>
<li>Where a source could not be reached or a value was not published, the value was left blank
and labelled <span class="unv">unverified</span> — never inferred.</li>
<li>Where a source is an intermediary (Booking.com, Google Maps), the row says so.</li>
</ol>

<div class="warnbox">
<strong>Known limits of this snapshot.</strong> The MICHELIN guide pages themselves
(guide.michelin.com) were blocked to this reader, so the official press release on michelin.com was
used as the source of record. TikTok and Instagram were unreachable, so social links are thin.
Only 5 of 360 possible transit pairs were routed. All three are recorded on
<a href="flagged.html">Flagged for Review</a>.
</div>
"""
    return page("verification.html", "Verification", body)

# ---------------------------------------------------------------- flagged
def build_flagged():
    flags = [
        ("H1", "Hotel", "Four Strip flagships show no availability for the preferred week",
         "Park MGM, ARIA, Bellagio and The Cosmopolitan all returned 'unavailable' for 15–22 Feb 2027.",
         "Medium — likely demand, but could be an inventory-release pattern. Re-check monthly.",
         "https://www.booking.com/hotel/us/hotel-park-mgm.html"),
        ("H2", "Hotel", "Two quotes for the same hotel are not like-for-like",
         "Trump International shows $1,661 for 7 nights (15–22 Feb) and $1,828 for 8 nights (22 Feb–1 Mar); "
         "only the second states 'Includes taxes and fees'.",
         "High — do not compare them as if equal.",
         ""),
        ("H3", "Hotel", "Resort fees absent from every total",
         "No hotel fee page was fetched. Las Vegas resort fees are typically $25–$55/night.",
         "High — the cheapest hotel may not be cheapest.", ""),
        ("H4", "Hotel", "'Room type assigned on arrival' appears on the cheapest rates",
         "Rio ($483), Flamingo ($626) and Harrah's ($961) all quote 'assigned on arrival'. The user "
         "requires a queen bed or bigger.", "High — the requirement is not guaranteed on these rates.", ""),
        ("H5", "Hotel", "Private bathroom confirmed for only 2 of 15",
         "Only the two Signature apartment listings state '1 bathroom'.", "Medium — verify per room.", ""),
        ("M1", "MICHELIN", "Press-release date differs from ceremony date",
         "michelin.com dates the release 31 Aug 2026; the ceremony was 26 Aug 2026.",
         "Low — editorial date, not a data conflict.", ""),
        ("M2", "MICHELIN", "guide.michelin.com could not be read",
         "Direct fetches of Michelin restaurant pages failed. The official michelin.com press release "
         "was used instead and cross-checked against the LVCVA page.",
         "Medium — a second official source was substituted; consider a manual check of the guide.",
         "https://guide.michelin.com/us/en/nevada/las-vegas/restaurants"),
        ("M3", "MICHELIN", "Two-star price exists only in a news article",
         "A third-party publication reports Robuchon's degustation 'from $525 per person'. This is NOT "
         "an official price and is not used anywhere on this site.",
         "High — a tempting number to quote. Deliberately excluded.", ""),
        ("M4", "MICHELIN", "Kabuto menu PDF filename is stale",
         "The 2026 menu is served at kabuto-menu2026.pdf but the embedded PDF title reads "
         "'kabuto-menu2023'.", "Low — content is current; filename metadata is not.", ""),
        ("T1", "Transit", "Transit times measured pre-dawn",
         "All Google Maps routes were queried in the early morning. Evening service differs.",
         "High for planning — dinner travel is what matters.", ""),
        ("T2", "Transit", "Only 5 of ~360 hotel×restaurant pairs routed",
         "The matrix is a small sample. Hotels with no measurements cannot be ranked on reach.",
         "High — the ranking's main weakness.", ""),
        ("T3", "Transit", "The requirement assumed a subway that does not exist",
         "Las Vegas has no subway/metro/light rail. Bus + monorail only.",
         "High — corrected on the Transit page.", ""),
        ("D1", "Dates", "Preferred window (3 nights) conflicts with trip length (1–2 weeks)",
         "15–18 Feb 2027 is 3 nights. Plan prices 7 nights from 15 Feb.",
         "High — needs a human decision.", ""),
        ("D2", "Dates", "No event calendar was checked",
         "Conventions, races and fights could invalidate every price.",
         "Highest — unresolved.", ""),
        ("S1", "Social", "TikTok and Instagram not crawlable",
         "Search engines were reachable but TikTok/Instagram were not. Links exist only where a venue's "
         "own site embeds Instagram (Kabuto), plus YouTube results.",
         "Medium — 17 venues have no social link rather than a guessed one.", ""),
        ("A1", "Activities", "No activity has verified hours or ticket price",
         "All seven activities link their official page; none were captured.",
         "Medium — weakest page on the site.", ""),
        ("R1", "Repo", "No prior content or sources existed to audit",
         "The repository held only a one-line README at commit 9b8bcfa. There was nothing to verify "
         "line by line, so this build starts from the official sources listed above.",
         "Low — recorded for completeness.", ""),
        ("R2", "Repo", "GitHub Pages was pre-configured to serve from main branch root",
         "The Pages API reports source branch 'main', path '/'. Pages cannot serve from /docs on this "
         "branch unless that setting changes.", "Medium — publishing path decision needed.", ""),
    ]
    rows = ""
    for fid, area, title, detail, risk, link in flags:
        l = f'<a href="{e(link)}" target="_blank" rel="noopener">source</a>' if link else "—"
        rows += f"""<tr><td class="src">{e(fid)}</td><td><span class="pill">{e(area)}</span></td>
<td><strong>{e(title)}</strong><div class="src">{e(detail)}</div></td>
<td class="src">{e(risk)}</td><td class="src">{l}</td></tr>"""

    body = f"""
<h1>Flagged for Review</h1>
<p class="lead">Everything irregular, uncertain or blocked, in one place. Nothing on this page
blocks the rest of the site — it is the queue of things a human should look at.</p>

<div class="grid">
<div class="kpi"><small>Items flagged</small><b>{len(flags)}</b></div>
<div class="kpi"><small>High / highest risk</small><b>{sum(1 for f in flags if 'High' in f[4])}</b></div>
<div class="kpi"><small>Medium</small><b>{sum(1 for f in flags if 'Medium' in f[4])}</b></div>
<div class="kpi"><small>Low</small><b>{sum(1 for f in flags if f[4].startswith('Low'))}</b></div>
</div>

<div class="tblwrap"><table>
<thead><tr><th>ID</th><th>Area</th><th>Finding</th><th>Risk</th><th>Source</th></tr></thead>
<tbody>{rows}</tbody></table></div>

<h2>Nothing was silently corrected</h2>
<p>Two things were deliberately <em>not</em> done, and both are recorded above rather than acted on:
the $525 Robuchon price from a news article was not used (M3), and no TikTok or Instagram handle
was inferred from a name (S1). Where the evidence stopped, the table stops.</p>
"""
    return page("flagged.html", "Flagged for Review", body)

# ---------------------------------------------------------------- audit
def build_audit():
    body = """
<h1>Repository audit</h1>
<p class="lead">The “REPO WORK” half of the brief: review the repository line by line and report.</p>

<h2>What was in the repository</h2>
<div class="tblwrap"><table>
<thead><tr><th>Item</th><th>State at start</th><th>Finding</th></tr></thead>
<tbody>
<tr><td>Commits</td><td>1 — <code>9b8bcfa</code> “Initial commit”</td><td>No prior work to audit.</td></tr>
<tr><td><code>README.md</code></td><td>8 bytes</td><td>Content was the single token <code># Vegas1</code> — a title with no body.</td></tr>
<tr><td><code>COORDINATION.md</code></td><td>Did not exist</td><td>Created by this session as required. Claimed the full build to avoid a blocked start, since no other session had any claim.</td></tr>
<tr><td>Source files / data / docs</td><td>absent</td><td>No code, no datasets, no pages.</td></tr>
<tr><td>Licence</td><td>absent</td><td><strong>Irregularity:</strong> a public repository with no licence. Worth adding before publishing.</td></tr>
<tr><td><code>.gitignore</code></td><td>absent</td><td><strong>Irregularity:</strong> absent. Generated artefacts can be committed by accident.</td></tr>
<tr><td>CI / workflows</td><td>absent</td><td>No build or link-check step.</td></tr>
<tr><td>GitHub Pages</td><td>Enabled, source <code>main</code> / root</td><td><strong>Irregularity:</strong> Pages is configured to publish the repository root of <code>main</code>, not <code>/docs</code>. The site built here lives in <code>docs/</code> to keep the repo root clean.</td></tr>
<tr><td>Branch protection</td><td>Unknown — not readable with this token</td><td>Could not be audited.</td></tr>
<tr><td>Git identity / remote</td><td><code>kanlerxz87-cyber/Vegas1</code></td><td>Fine.</td></tr>
</tbody></table></div>

<h2>Honest conclusion on “review line by line”</h2>
<p>There were no lines to review. One 8-byte README is the entire pre-existing content, so the
instruction to “flag irregularities in existing work” resolves to four real findings — no licence,
no .gitignore, no CI, and a Pages source that does not match the build location — plus one thing
that could not be checked at all (branch protection). Those are recorded here and, where relevant,
on <a href="flagged.html">Flagged for Review</a>.</p>

<h2>What this session added</h2>
<div class="tblwrap"><table>
<thead><tr><th>Path</th><th>Purpose</th></tr></thead>
<tbody>
<tr><td><code>data/michelin.json</code></td><td>24 Las Vegas selections with official distinction + official site link</td></tr>
<tr><td><code>data/restaurant-details.json</code></td><td>Official hours and published prices, with the source URL per venue</td></tr>
<tr><td><code>data/hotels.json</code></td><td>15 hotels with verified 7-night quotes + 5 documented unavailabilities</td></tr>
<tr><td><code>data/pricing.json</code></td><td>Date-window comparison and the “cheapest time to book” analysis</td></tr>
<tr><td><code>data/transit.json</code></td><td>Measured routes, the no-subway correction, and explicit coverage limits</td></tr>
<tr><td><code>data/activities.json</code></td><td>Seven activities, two flagged as outside the transit rule</td></tr>
<tr><td><code>data/social.json</code></td><td>Verified video/Instagram links, plus an explicit “not found” list</td></tr>
<tr><td><code>build.py</code></td><td>Generator: renders every page from the JSON, so no number is typed twice</td></tr>
<tr><td><code>docs/</code></td><td>The published site</td></tr>
<tr><td><code>COORDINATION.md</code></td><td>Shared task board</td></tr>
</tbody></table></div>

<div class="okbox"><strong>Design principle worth keeping:</strong> the site is generated, not
hand-written. Every table cell traces to one JSON field, and that field either carries a source
URL or the literal string “unverified”. That makes it structurally hard to introduce a hallucinated
number later — the only way to add one is to add a field, and every field is visible.</div>
"""
    return page("audit.html", "Repo Audit", body)


# ---------------------------------------------------------------- main-branch audit
def build_cross():
    c = CROSS
    meta = c["_meta"]
    sc = c["scorecard"]

    agree = ""
    for a in c["agreements"]:
        src = f'<a href="{e(a["source"])}" target="_blank" rel="noopener">source</a>' if a["source"] else "—"
        agree += f"""<tr><td><span class="ok">{e(a['verdict'])}</span></td>
<td><strong>{e(a['claim'])}</strong><div class="src">{e(a['detail'])}</div>
<div class="src"><em>{e(a['significance'])}</em></div></td>
<td class="src">{src}</td></tr>"""

    conf = ""
    for x in c["conflicts"]:
        cls = {"High": "no", "Medium": "warn", "Low": "src"}.get(x["severity"], "src")
        src = f'<a href="{e(x["source"])}" target="_blank" rel="noopener">source</a>' if x["source"] else "no source exists"
        conf += f"""<tr><td class="src">{e(x['id'])}</td>
<td><span class="{cls}">{e(x['severity'])}</span></td>
<td><strong>{e(x['finding'])}</strong>
 <div class="src">{e(x['detail'])}</div>
 <div style="margin-top:6px"><span class="pill">official / current value</span> {e(x['official_value'])}</div>
 <div class="src" style="margin-top:6px"><strong>Action taken:</strong> {e(x['action_taken'])}</div></td>
<td class="src">{src}</td></tr>"""

    selfcorr = ""
    for sc_ in c.get("auditor_self_corrections", []):
        selfcorr += f'''<div class="card"><span class="pill">self-correction {e(sc_['id'])}</span>
<p style="margin:8px 0 4px"><strong>What I claimed:</strong> {e(sc_['what'])}</p>
<p style="margin:4px 0"><strong>Why it was wrong:</strong> {e(sc_['why_wrong'])}</p>
<p style="margin:4px 0"><strong>Corrected to:</strong> {e(sc_['corrected_to'])}</p>
<p class="src"><a href="{e(sc_['source'])}" target="_blank" rel="noopener">source</a></p></div>'''

    body = f"""
<h1>Audit of the site already published on <code>main</code></h1>
<p class="lead">Another agent session published a Las Vegas site to <code>main</code> at commit
<code>{e(meta['audited_commit'].split(' - ')[0])}</code>. This page is the line-by-line review of it,
done against official sources. <strong>Nothing in that work was edited or deleted.</strong></p>

<div class="warnbox">
<strong>Why this page exists.</strong> Your brief asked for a repo review “line by line, verifying
from official verified trusted sources, flagging irregularities”. At the start of this session the
branch base was an 8-byte README, so there was nothing local to audit. The real prior work was on
<code>main</code>, so that is what got audited.
</div>

<div class="grid">
<div class="kpi"><small>Claims audited</small><b>{sc['claims_audited']}</b></div>
<div class="kpi"><small>Agree</small><b>{sc['agree']}</b></div>
<div class="kpi"><small>High-severity conflicts</small><b>{sc['conflict_high']}</b></div>
<div class="kpi"><small>Unresolvable</small><b>{sc['cannot_be_resolved']}</b></div>
</div>

<div class="okbox"><strong>Verdict in one line.</strong> {e(sc['comment'])}</div>

<h2>Where the two sessions agree (this is the good news)</h2>
<div class="tblwrap"><table>
<thead><tr><th>Verdict</th><th>Claim</th><th>Source</th></tr></thead>
<tbody>{agree}</tbody></table></div>
<p class="src">Two sessions, working independently and reading different source paths, produced
the identical 24-venue MICHELIN list with the identical award split. That is the single most
reassuring result on this site.</p>

<h2>Irregularities found</h2>
<div class="tblwrap"><table>
<thead><tr><th>ID</th><th>Severity</th><th>Finding, current official value, and what was done</th><th>Source</th></tr></thead>
<tbody>{conf}</tbody></table></div>

<h2>The two that would actually cost you money</h2>
<div class="errbox">
<ol>
<li><strong>X3 / X4 — estimated pricing labelled verified.</strong> The landing page says “verified
from official sources”; the project's own data file says the February 2027 prices are estimated.
A budget built on those numbers needs rebuilding on dated quotes. This is the one that affects
a real decision.</li>
<li><strong>X2 — the Caesars Palace resort fee.</strong> $54.95 appears in two files; no current
source matches it. The fee is real and mandatory, so the number matters more than it looks.</li>
</ol>
<p style="margin-top:10px"><strong>And one thing that is <em>not</em> a problem:</strong> the
MICHELIN distinctions. All 24 venues and all 24 award levels are correct.</p>
</div>

<h2>Where I was wrong first, and caught it</h2>
<div class="warnbox">
<p>Publishing a correction is more useful than quietly deleting it.</p>
{selfcorr}
</div>

<h2>How the conflict was handled</h2>
<p>No file written by the other session was modified. The decision was to preserve both builds:</p>
<div class="tblwrap"><table>
<thead><tr><th>Location</th><th>What it holds</th><th>State</th></tr></thead>
<tbody>
<tr><td><code>main</code> branch root</td><td>The other session's site, data and documents</td>
<td class="ok">untouched</td></tr>
<tr><td>this branch, <code>/docs</code></td><td>This session's generated site (12 pages)</td>
<td class="ok">new</td></tr>
<tr><td>this branch, <code>/plan-data</code></td><td>This session's verified JSON</td>
<td class="ok">new, non-colliding names</td></tr>
<tr><td><code>COORDINATION.md</code></td><td>Both sessions recorded, plus the reconciliation</td>
<td class="ok">merged by hand</td></tr>
</tbody></table></div>
<p class="src">One naming collision had to be resolved: this session had created
<code>data/hotels.json</code> and <code>data/michelin.json</code> while the other session had
<code>data/hotels.json</code> and <code>data/michelin-restaurants.json</code>. Merging would have
overwritten eight real hotel files, so this session's data moved to <code>/plan-data</code> instead.</p>

<h2>What a human should decide</h2>
<ol>
<li>Which build becomes the published site — or whether the two should be merged.</li>
<li>Whether to correct the star counts and the “verified” labelling on <code>main</code>.</li>
<li>Whether the pages deployment should serve <code>main</code>/root (current) or
<code>docs/</code> on this branch.</li>
</ol>
"""
    return page("audit-main.html", "Audit of main", body)


# ---------------------------------------------------------------- run
def main():
    os.makedirs(DOCS, exist_ok=True)
    built = []
    built.append(build_index())
    built.append(build_hotels())
    built.append(build_michelin())
    built.append(build_transit())
    built.append(build_activities())
    built.append(build_itinerary())
    built.append(build_budget())
    built.append(build_questions())
    built.append(build_suggestions())
    built.append(build_verification())
    built.append(build_flagged())
    built.append(build_audit())
    built.append(build_cross())
    print(f"built {len(built)} pages -> {DOCS}")
    for p in built:
        print(" ", p, os.path.getsize(os.path.join(DOCS, p)), "bytes")

if __name__ == "__main__":
    main()
