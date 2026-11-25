#!/usr/bin/env python3
"""Build the static Las Vegas trip-planning site into docs/ (GitHub Pages).

Reads docs/data/*.json and writes HTML pages. Standard library only.
Blank data values are rendered as 'Unverified' and flagged; nothing is inferred.
Run:  python3 scripts/build_site.py
"""
import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
DATA = DOCS / "data"


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def esc(s):
    return html.escape(str(s or ""), quote=True)


def link(url, label="Source"):
    if not url:
        return ""
    return f'<a href="{esc(url)}" target="_blank" rel="noopener">{esc(label)}</a>'


def cell(value, src=None, label_src="Source"):
    """A table cell: value (or Unverified) plus the source link."""
    if value:
        out = esc(value)
    else:
        out = '<span class="unv">Unverified</span>'
    if src:
        out += f'<div class="src">{link(src, label_src)}</div>'
    return out


def table(headers, rows_html, caption=""):
    th = "".join(f"<th>{esc(h)}</th>" for h in headers)
    cap = f"<caption>{esc(caption)}</caption>" if caption else ""
    return f'<div class="table-wrap"><table>{cap}<thead><tr>{th}</tr></thead><tbody>{"".join(rows_html)}</tbody></table></div>'


def row(cells_html, labels):
    tds = "".join(
        f'<td data-label="{esc(l)}">{c}</td>' for c, l in zip(cells_html, labels)
    )
    return f"<tr>{tds}</tr>"


NAV = [
    ("index.html", "Home"),
    ("summary.html", "Executive summary"),
    ("michelin.html", "Michelin restaurants"),
    ("hotels.html", "Hotels"),
    ("activities.html", "Activities"),
    ("questions.html", "Questions"),
    ("suggestions.html", "Suggestions"),
    ("flagged.html", "Flagged for review"),
]


def page(title, body, active):
    nav = "".join(
        f'<a href="{href}" class="{"active" if href == active else ""}">{esc(label)}</a>'
        for href, label in NAV
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · Las Vegas Trip Planner</title>
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header class="top">
  <div class="brand"><a href="index.html">Las Vegas Trip Planner</a><span>15–22 Feb 2027 · 2 adults</span></div>
  <nav class="nav">{nav}</nav>
</header>
<main class="wrap">
<h1>{esc(title)}</h1>
{body}
</main>
<footer class="foot">
  Verified values link to their official source. Blank cells are unverified and flagged.
  Last built from data in <code>docs/data/</code>. Not financial advice; re-check every value before booking.
</footer>
</body>
</html>
"""


def michelin_page():
    m = load("michelin.json")
    rows_html = []
    counts = {"2 stars": 0, "1 star": 0, "Bib": 0, "Rec": 0}
    for r in m["rows"]:
        d = r["distinction"]
        if "2 MICHELIN" in d:
            counts["2 stars"] += 1
        elif "1 MICHELIN" in d:
            counts["1 star"] += 1
        elif "Bib" in d:
            counts["Bib"] += 1
        else:
            counts["Rec"] += 1
        star = "badge star" if "Michelin star" == r["status"] else ("badge bib" if "Bib" in r["status"] else "badge rec")
        cells = [
            f'<strong>{esc(r["name"])}</strong>',
            f'<span class="{star}">{esc(d)}</span><div class="sub">{esc(r["status"])}</div>',
            cell(r.get("cuisine")),
            esc(r["address"]),
            cell(r.get("hours"), r.get("hours_source"), "Official"),
            cell(r.get("price_couple"), r.get("price_source")),
            cell(r.get("social")),
            link(r["source_url"], "Michelin release"),
            f'<span class="flag">{esc(r.get("flag",""))}</span>' if r.get("flag") else "",
        ]
        labels = ["Restaurant", "Michelin status", "Cuisine", "Address", "Hours & exceptions", "Price for 2 adults (total)", "YouTube / TikTok / Instagram", "Source", "Flag"]
        rows_html.append(row(cells, labels))
    headers = ["Restaurant", "Michelin status", "Cuisine", "Address", "Hours & exceptions", "Price for 2 adults (total)", "YouTube / TikTok / Instagram", "Source", "Flag"]
    stat = (
        f'<div class="stats">'
        f'<div><b>{counts["2 stars"]}</b>2-star</div>'
        f'<div><b>{counts["1 star"]}</b>1-star</div>'
        f'<div><b>{counts["Bib"]}</b>Bib Gourmand</div>'
        f'<div><b>{counts["Rec"]}</b>Recommended (no star)</div>'
        f'<div><b>{len(m["rows"])}</b>Total, Las Vegas</div></div>'
    )
    body = f"""
<p class="lead">2026 MICHELIN Guide Southwest (inaugural Las Vegas selection), per the official Michelin press release.
Stars and Bib Gourmand are listed as such; Recommended restaurants are <b>listed in the guide without a star</b>.</p>
{stat}
<p class="note">Hours, couple's price, and social links are blank because no official source was confirmed for them yet. Restaurants are sorted as published. Michelin's own restaurant pages were not reachable from this session.</p>
{table(headers, rows_html, "Las Vegas Michelin restaurants, 2026")}
"""
    return page("Michelin restaurants", body, "michelin.html")


def hotels_page():
    h = load("hotels.json")
    crit = h["search_criteria"]
    rows_html = []
    headers = ["Rank", "Hotel", "Michelin on property", "Room example", "Beds", "Size", "Bathroom", "7-night total", "Booking window", "Source", "Flag"]
    labels = headers
    for r in h["rows"]:
        cells = [
            str(r["rank_michelin"]),
            f'<strong>{esc(r["hotel"])}</strong><div class="sub">{esc(r["address"])}</div>',
            esc(r["michelin_on_property"]),
            esc(r["room_example"]),
            cell(r["beds"]),
            cell(r["size"]),
            cell(r["bathroom"]),
            cell(r["price_7_nights_total"], r.get("price_source")),
            cell(r["booking_window"]),
            link(r["room_source"], "Room page"),
            f'<span class="flag">{esc(r["flag"])}</span>',
        ]
        rows_html.append(row(cells, labels))
    body = f"""
<p class="lead">Search criteria: <b>{esc(crit['dates_preferred'])}</b> (preferred); {esc(crit['dates_allowed'])}; {esc(crit['guests'])}; {esc(crit['room_requirement'])}.</p>
<div class="callout"><b>Prices are not verified.</b> No official rate for 15–22 Feb 2027 was found, so every price cell is blank. The 7-night totals and the cheapest booking time will be filled in only from official booking pages.</div>
<p class="note">Rank is by number of Michelin-listed restaurants on the same resort property (official addresses). Ties are shown at the same rank. Walking or transit times are not verified.</p>
{table(headers, rows_html, "Hotel candidates (9 rows, 8 properties)")}
"""
    return page("Hotels", body, "hotels.html")


def activities_page():
    a = load("activities.json")
    rows_html = []
    headers = ["Activity", "Type", "Location", "Hours & exceptions", "Fee", "Booking", "YouTube / TikTok / Instagram", "Source", "Flag"]
    for r in a["rows"]:
        cells = [
            f'<strong>{esc(r["name"])}</strong>',
            esc(r["type"]),
            esc(r["location"]),
            cell(r["hours"], r.get("hours_source"), "Official"),
            cell(r["fee"], r.get("fee_source"), "Official"),
            cell(r["booking"]),
            cell(r["social"]),
            link(r["source_url"], "Official"),
            f'<span class="flag">{esc(r["flag"])}</span>' + (f'<div class="sub">Exceptions: {esc(r["day_exceptions"])}</div>' if r.get("day_exceptions") else ""),
        ]
        rows_html.append(row(cells, headers))
    body = f"""
<p class="lead">Activities with official hours or fees. The brief did not list the activities the couple wants, so this list is a starting point.</p>
{table(headers, rows_html, "Verified activities (3)")}
"""
    return page("Activities", body, "activities.html")


def summary_page():
    c = load("content.json")["summary"]
    bullets = "".join(f"<li>{esc(b)}</li>" for b in c["bullets"])
    body = f"""
<div class="callout"><b>{esc(c['headline'])}</b></div>
<ul class="bullets">{bullets}</ul>
<p class="note">Figures are from the sources linked on each page. Nothing here is a price quote.</p>
"""
    return page("Executive summary", body, "summary.html")


def questions_page():
    qs = load("content.json")["questions"]
    rows_html = []
    headers = ["#", "Question", "What we know", "What we need", "How to resolve"]
    for i, q in enumerate(qs, 1):
        cells = [str(i), esc(q["q"]), esc(q["known"]), esc(q["answer_needed"]), esc(q["how_to_resolve"])]
        rows_html.append(row(cells, headers))
    body = f"""
<p class="lead">Open questions that must be answered before a decision is reasonable.</p>
{table(headers, rows_html, "Questions and information gaps")}
"""
    return page("Questions", body, "questions.html")


def suggestions_page():
    ss = load("content.json")["suggestions"]
    rows_html = []
    headers = ["ID", "Suggestion", "Detail", "Impact", "Effort", "Your choice"]
    for s in ss:
        cells = [s["id"], f'<strong>{esc(s["title"])}</strong>', esc(s["detail"]), esc(s["impact"]), esc(s["effort"]), f'<span class="pending">{esc(s["choice"])}</span>']
        rows_html.append(row(cells, headers))
    body = f"""
<div class="callout">Nothing on this page has been implemented. Choose the suggestions to apply (for example: "Apply S1, S2, S4"). Changes are made only after you choose.</div>
{table(headers, rows_html, "Suggestions for improvement")}
"""
    return page("Suggestions", body, "suggestions.html")


def flagged_page():
    c = load("content.json")
    rows_html = []
    headers = ["ID", "Area", "Item", "Action taken", "Source"]
    for f in c["flagged"]:
        cells = [f["id"], esc(f["area"]), esc(f["item"]), esc(f["action"]), link(f.get("source"), "Link") if f.get("source") else '<span class="unv">None</span>']
        rows_html.append(row(cells, headers))
    rrows = []
    rh = ["ID", "Repo review item", "Status", "Source"]
    for r in c["repo_review"]:
        cells = [r["id"], esc(r["item"]), esc(r["status"]), esc(r["source"])]
        rrows.append(row(cells, rh))
    body = f"""
<p class="lead">Items that could not be verified or that conflict between sources. Each needs a manual check before use.</p>
<h2>Data flags</h2>
{table(headers, rows_html, "Flagged data")}
<h2>Repo review</h2>
{table(rh, rrows, "Repo review findings")}
"""
    return page("Flagged for review", body, "flagged.html")


def index_page():
    m = load("michelin.json")["rows"]
    h = load("hotels.json")["rows"]
    a = load("activities.json")["rows"]
    c = load("content.json")
    stars = sum(1 for r in m if "Michelin star" == r["status"])
    cards = [
        ("summary.html", "Executive summary", "The key facts and what is still missing."),
        ("michelin.html", "Michelin restaurants", f"{len(m)} Las Vegas restaurants: {stars} starred, the rest Bib Gourmand or Recommended."),
        ("hotels.html", "Hotels", f"{len(h)} candidates with queen beds and private bathrooms. Prices pending."),
        ("activities.html", "Activities", f"{len(a)} attractions with official hours and fees."),
        ("questions.html", "Questions", f"{len(c['questions'])} open questions and how to answer each."),
        ("suggestions.html", "Suggestions", f"{len(c['suggestions'])} options to choose from before any change."),
        ("flagged.html", "Flagged for review", f"{len(c['flagged'])} data flags and {len(c['repo_review'])} repo review items."),
    ]
    card_html = "".join(
        f'<a class="card" href="{href}"><h3>{esc(t)}</h3><p>{esc(d)}</p></a>' for href, t, d in cards
    )
    kpis = (
        '<div class="stats">'
        f'<div><b>15–22 Feb</b>Preferred trip (3 nights: 15–18 Feb)</div>'
        f'<div><b>{stars}</b>Michelin-starred in Las Vegas</div>'
        f'<div><b>{len(h)}</b>Hotel candidates</div>'
        f'<div><b>0</b>Verified hotel prices</div>'
        '</div>'
    )
    body = f"""
<p class="lead">A simple dashboard for planning the trip. Each table shows its official source. Blank cells are unverified.</p>
{kpis}
<div class="cards">{card_html}</div>
"""
    return page("Las Vegas Trip Planner", body, "index.html")


CSS = """
:root{--ink:#1d2330;--mute:#5b6475;--line:#e3e7ee;--bg:#f7f8fb;--card:#fff;--accent:#7a1f2b;--gold:#b8860b;--ok:#1f7a4d;--warn:#8a5a00;--unv:#b00020}
*{box-sizing:border-box}
body{margin:0;font:16px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:var(--ink);background:var(--bg)}
a{color:#1a4fa0}
.top{background:#fff;border-bottom:1px solid var(--line);position:sticky;top:0;z-index:5}
.brand{display:flex;flex-wrap:wrap;gap:.25rem 1rem;align-items:baseline;padding:.6rem 1rem}
.brand a{font-weight:700;color:var(--accent);text-decoration:none;font-size:1.05rem}
.brand span{color:var(--mute);font-size:.85rem}
.nav{display:flex;gap:.25rem;overflow-x:auto;padding:0 .75rem .6rem;white-space:nowrap}
.nav a{padding:.35rem .65rem;border-radius:999px;background:#eef1f6;color:var(--ink);text-decoration:none;font-size:.9rem}
.nav a.active{background:var(--accent);color:#fff}
.wrap{max-width:1200px;margin:0 auto;padding:1rem}
h1{font-size:1.6rem;margin:.5rem 0 .75rem}
h2{font-size:1.2rem;margin:1.5rem 0 .5rem}
.lead{font-size:1.02rem;color:var(--ink)}
.note{color:var(--mute);font-size:.9rem}
.callout{background:#fff8e6;border:1px solid #f1d58a;border-radius:10px;padding:.75rem 1rem;margin:.75rem 0}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:.6rem;margin:1rem 0}
.stats div{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:.7rem .8rem;color:var(--mute);font-size:.85rem}
.stats b{display:block;font-size:1.35rem;color:var(--accent)}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:.75rem;margin-top:1rem}
.card{display:block;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:1rem;text-decoration:none;color:var(--ink)}
.card:hover{border-color:var(--accent)}
.card h3{margin:0 0 .35rem;color:var(--accent);font-size:1.05rem}
.card p{margin:0;color:var(--mute);font-size:.92rem}
.table-wrap{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:12px;margin:.5rem 0 1rem}
table{border-collapse:collapse;width:100%;min-width:720px;font-size:.9rem}
caption{text-align:left;padding:.6rem .8rem;font-weight:600;color:var(--mute)}
th,td{text-align:left;vertical-align:top;padding:.55rem .6rem;border-top:1px solid var(--line)}
th{background:#f3f5f9;font-size:.8rem;text-transform:uppercase;letter-spacing:.03em;color:var(--mute);position:sticky;top:0}
.src{font-size:.8rem;margin-top:.2rem}
.sub{color:var(--mute);font-size:.8rem;margin-top:.15rem}
.unv{color:var(--unv);font-weight:600;font-size:.82rem}
.flag{color:var(--warn);font-size:.82rem}
.badge{display:inline-block;padding:.12rem .5rem;border-radius:999px;font-size:.8rem;font-weight:600}
.badge.star{background:#fbeccc;color:#6b4a00}
.badge.bib{background:#e5f1ea;color:var(--ok)}
.badge.rec{background:#eef1f6;color:var(--mute)}
.pending{color:var(--warn);font-weight:600}
.foot{max-width:1200px;margin:2rem auto;padding:0 1rem 2rem;color:var(--mute);font-size:.85rem}
@media (max-width:700px){
  table{min-width:0}
  thead{display:none}
  table,tbody,tr,td{display:block;width:100%}
  tr{border-top:1px solid var(--line);padding:.5rem .6rem}
  td{border:0;padding:.25rem 0}
  td::before{content:attr(data-label);display:block;font-size:.72rem;text-transform:uppercase;color:var(--mute);letter-spacing:.03em}
  caption{padding:.6rem}
  h1{font-size:1.35rem}
}
"""


def main():
    (DOCS / "assets").mkdir(parents=True, exist_ok=True)
    (DOCS / "assets" / "style.css").write_text(CSS, encoding="utf-8")
    pages = {
        "index.html": index_page(),
        "summary.html": summary_page(),
        "michelin.html": michelin_page(),
        "hotels.html": hotels_page(),
        "activities.html": activities_page(),
        "questions.html": questions_page(),
        "suggestions.html": suggestions_page(),
        "flagged.html": flagged_page(),
    }
    for name, content in pages.items():
        (DOCS / name).write_text(content, encoding="utf-8")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    print(f"Wrote {len(pages)} pages to {DOCS}")


if __name__ == "__main__":
    main()
