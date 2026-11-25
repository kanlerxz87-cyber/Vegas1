#!/usr/bin/env python3
"""Build the static GitHub Pages site in docs/ from data/site-data.json.

Every table cell that is empty in the data renders as "Unverified" so that
no value is ever filled in by inference. Run:  python3 scripts/build_site.py
"""
import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "data" / "site-data.json").read_text(encoding="utf-8"))
OUT = ROOT / "docs"
OUT.mkdir(exist_ok=True)

NAV = [
    ("index.html", "Home"),
    ("hotels.html", "Hotels"),
    ("michelin.html", "Michelin"),
    ("activities.html", "Activities"),
    ("booking.html", "Booking"),
    ("questions.html", "Questions"),
    ("suggestions.html", "Suggestions"),
    ("flagged.html", "Flagged"),
    ("repo-review.html", "Repo review"),
    ("sources.html", "Sources"),
]

CSS = """
:root{--ink:#1d2430;--mut:#5b6573;--line:#e3e7ee;--bg:#f6f8fb;--card:#fff;--acc:#0b6e4f;--warn:#b26a00;--warnbg:#fff4e0;--bad:#9b1c1c;--badbg:#fdecec;--ok:#0b6e4f;--okbg:#e6f5ef}
*{box-sizing:border-box}
body{margin:0;font:15px/1.5 system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;color:var(--ink);background:var(--bg)}
header{background:#14321f;color:#fff;padding:14px 16px}
header .t{font-weight:700;font-size:18px}
header .s{opacity:.8;font-size:12px}
nav{display:flex;flex-wrap:wrap;gap:6px;padding:10px 16px;background:#fff;border-bottom:1px solid var(--line);position:sticky;top:0;z-index:5}
nav a{padding:6px 10px;border-radius:999px;background:var(--bg);color:var(--ink);text-decoration:none;font-size:13px;border:1px solid var(--line)}
nav a.on{background:var(--acc);color:#fff;border-color:var(--acc)}
main{max-width:1200px;margin:0 auto;padding:16px}
h1{font-size:24px;margin:8px 0 4px}
h2{font-size:18px;margin:22px 0 8px}
p.lead{color:var(--mut);margin:0 0 12px}
.grid{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(170px,1fr))}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px}
.card .n{font-size:26px;font-weight:700}
.card .l{color:var(--mut);font-size:13px}
.card a{color:var(--acc);font-weight:600;text-decoration:none}
.box{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;margin:10px 0}
ul.sum li{margin:6px 0}
.tw{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:12px}
table{border-collapse:collapse;width:100%;min-width:640px;font-size:13.5px}
th{background:#eef3f0;text-align:left;padding:9px;border-bottom:1px solid var(--line);position:sticky;top:0;font-weight:600}
td{padding:9px;border-bottom:1px solid var(--line);vertical-align:top}
tr:last-child td{border-bottom:0}
a{color:#0a5bb5}
.unv{display:inline-block;background:var(--warnbg);color:var(--warn);border:1px solid #f1d29b;border-radius:6px;padding:0 6px;font-size:12px;white-space:nowrap}
.flag{display:block;color:var(--warn);font-size:12px;margin-top:3px}
.badge{display:inline-block;padding:1px 8px;border-radius:999px;font-size:12px;font-weight:600}
.b-star{background:#fff3c4;color:#6b4e00}
.b-bib{background:#e4f0ff;color:#14467a}
.b-rec{background:#eef1f4;color:#33414f}
.b-ok{background:var(--okbg);color:var(--ok)}
.b-bad{background:var(--badbg);color:var(--bad)}
.b-warn{background:var(--warnbg);color:var(--warn)}
.small{font-size:12px;color:var(--mut)}
footer{color:var(--mut);font-size:12px;padding:18px 16px;text-align:center}
/* mobile: stack table rows into cards */
@media (max-width:700px){
  main{padding:10px}
  .tw{overflow:visible;background:none;border:0}
  table{min-width:0}
  thead{display:none}
  tr{display:block;background:var(--card);border:1px solid var(--line);border-radius:12px;margin:10px 0;padding:6px 0}
  td{display:block;border:0;padding:5px 12px}
  td::before{content:attr(data-label);display:block;font-size:11px;text-transform:uppercase;letter-spacing:.04em;color:var(--mut)}
  th{position:static}
}
"""


def esc(s):
    return html.escape("" if s is None else str(s))


def linkify(text):
    """Turn [label](url) and bare https URLs into links; escape everything else."""
    out, pos = [], 0
    for m in re.finditer(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", text):
        out.append(esc(text[pos:m.start()]))
        out.append(f'<a href="{esc(m.group(2))}" target="_blank" rel="noopener">{esc(m.group(1))}</a>')
        pos = m.end()
    out.append(esc(text[pos:]))
    return "".join(out)


def link(url, label=None):
    if not url:
        return unv()
    if label is None:
        label = re.sub(r"^https?://(www\.)?", "", url).rstrip("/").split("/")[0]
    return f'<a href="{esc(url)}" target="_blank" rel="noopener">{esc(label)}</a>'


def unv(extra=None):
    txt = "⚠ Unverified" if not extra else f"⚠ {extra}"
    return f'<span class="unv">{esc(txt)}</span>'


def cell(value, flags=None, empty_label=None):
    if value in (None, ""):
        body = unv(empty_label)
    else:
        body = esc(value)
    if flags:
        body += "".join(f'<span class="flag">⚠ {esc(f)}</span>' for f in flags)
    return body


def table(headers, rows):
    """rows: list of lists of (label, html) tuples; labels become mobile labels."""
    th = "".join(f"<th>{esc(h)}</th>" for h in headers)
    body = []
    for r in rows:
        tds = "".join(f'<td data-label="{esc(lbl)}">{html_}</td>' for lbl, html_ in r)
        body.append(f"<tr>{tds}</tr>")
    return f'<div class="tw"><table><thead><tr>{th}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'


def page(active, title, lead, content):
    nav = "".join(
        f'<a href="{href}" class="{"on" if href == active else ""}">{esc(label)}</a>' for href, label in NAV
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} · Las Vegas Trip Planner</title>
<style>{CSS}</style></head>
<body>
<header><div class="t">Las Vegas Trip Planner</div>
<div class="s">Verified data as of {esc(DATA['meta']['as_of'])} · Branch {esc(DATA['meta']['branch'])}</div></header>
<nav>{nav}</nav>
<main>
<h1>{esc(title)}</h1>
<p class="lead">{esc(lead)}</p>
{content}
</main>
<footer>Blank cells are unverified and flagged. Live site built from data/site-data.json by scripts/build_site.py. Coordination board: COORDINATION.md.</footer>
</body></html>
"""


def michelin_badge(status):
    s = status.lower()
    if "star" in s and "bib" not in s:
        cls = "b-star"
    elif "bib" in s:
        cls = "b-bib"
    else:
        cls = "b-rec"
    return f'<span class="badge {cls}">{esc(status)}</span>'


def michelin_page():
    rows = []
    for r in DATA["michelin"]:
        rows.append([
            ("Restaurant", f"<strong>{esc(r['name'])}</strong>" + (f'<br>{link(r["official_url"], "official site")}' if r["official_url"] else unv())),
            ("Area / address", cell(r["area"])),
            ("Michelin status", michelin_badge(r["michelin"]) + (f'<br>{link(r["michelin_source"], "source")}' if r.get("michelin_source") else "")),
            ("Cuisine", cell(r["cuisine"])),
            ("Price level", cell(r["price_level"])),
            ("Cost for 2 adults", cell(r["est_cost_for_2"], empty_label="not published")),
            ("Days & hours", cell(r["hours"])),
            ("Exceptions", cell(r["exceptions"])),
            ("Social", link(r["social"]) if r.get("social") else unv("not verified")),
            ("Flags", "".join(f'<span class="flag">⚠ {esc(f)}</span>' for f in r["flags"]) or '<span class="small">—</span>'),
        ])
    headers = ["Restaurant", "Area / address", "Michelin status", "Cuisine", "Price level", "Cost for 2 adults",
               "Days & hours", "Exceptions", "Social", "Flags"]
    counts = {"star": 0, "bib": 0, "rec": 0}
    for r in DATA["michelin"]:
        s = r["michelin"].lower()
        if "bib" in s:
            counts["bib"] += 1
        elif "star" in s:
            counts["star"] += 1
        else:
            counts["rec"] += 1
    summary = (
        f'<div class="grid">'
        f'<div class="card"><div class="n">{len(DATA["michelin"])}</div><div class="l">Listings (LVCVA 2026)</div></div>'
        f'<div class="card"><div class="n">{counts["star"]}</div><div class="l">With stars</div></div>'
        f'<div class="card"><div class="n">{counts["bib"]}</div><div class="l">Bib Gourmand</div></div>'
        f'<div class="card"><div class="n">{counts["rec"]}</div><div class="l">Recommended / Selected only</div></div>'
        f'</div>'
    )
    note = (
        '<div class="box"><strong>How to read this table.</strong> Michelin status uses the LVCVA official list plus restaurant-owned pages. '
        'Stars = a current star; Bib = Bib Gourmand; Recommended/Selected = listed but no star. '
        '"Cost for 2" is blank unless the official site publishes a price; where it did, the total is 2 × the per-person price with tax and tip excluded. '
        'Open the restaurant\'s official site to confirm hours before any visit.</div>'
    )
    return summary + note + table(headers, rows)


def hotels_page():
    rows = []
    for h in DATA["hotels"]:
        rows.append([
            ("Rank", f"<strong>{h['rank']}</strong>"),
            ("Hotel", f"<strong>{esc(h['name'])}</strong><br>{link(h['official_url'], 'official site')}"),
            ("Address", cell(h["address"])),
            ("Michelin listed in this resort", cell(h["michelin_listed"])),
            ("Stars in resort", cell(h["stars"])),
            ("Room fit (official)", cell(h["room_fit"])),
            ("Private bathroom", cell(h["private_bath"])),
            ("Total — 3 nights (Feb 15–18)", cell(h["price_3n"], empty_label="no official rate")),
            ("Total — 7 nights (Feb 15–22)", cell(h["price_7n"], empty_label="no official rate")),
            ("Source", link(h["source"], "source")),
            ("Flags", "".join(f'<span class="flag">⚠ {esc(f)}</span>' for f in h["flags"])),
        ])
    headers = ["Rank", "Hotel", "Address", "Michelin listed in this resort", "Stars in resort", "Room fit (official)",
               "Private bathroom", "Total — 3 nights (Feb 15–18)", "Total — 7 nights (Feb 15–22)", "Source", "Flags"]
    intro = (
        '<div class="box"><strong>Ranking rule.</strong> ' + esc(DATA["hotel_rank_rule"]) + '</div>'
        '<div class="box"><strong>Requirements checked.</strong> 2 adults · private bathroom · queen or larger bed. '
        'Queen rooms were confirmed on two official pages (Cosmopolitan, ARIA). Private bathroom is not stated on any retrieved official room page, so it is unverified for every hotel.</div>'
        '<div class="box"><strong>Prices.</strong> No official 2027 rate was retrieved for any hotel. Price cells stay blank until verified. Use the official site links to check rates for the same dates and record the date you checked.</div>'
    )
    return intro + table(headers, rows)


def activities_page():
    rows = []
    for a in DATA["activities"]:
        rows.append([
            ("Activity", f"<strong>{esc(a['name'])}</strong><br>{link(a['official_url'], 'official site')}"),
            ("Operator", cell(a["operator"])),
            ("Distance from Strip", cell(a["distance"])),
            ("Hours", cell(a["hours"])),
            ("Entry / reservations", cell(a["entry"])),
            ("Fees", cell(a["fees"])),
            ("Getting there", cell(a["transit"])),
            ("Booking link", link(a.get("booking_url", ""), "booking") if a.get("booking_url") else unv()),
            ("Social", link(a["social"].split(" ")[0], "account") + (f'<span class="flag">{esc(" ".join(a["social"].split(" ")[1:]))}</span>' if " " in a["social"] else "") if a.get("social") else unv("not verified")),
            ("Flags", "".join(f'<span class="flag">⚠ {esc(f)}</span>' for f in a["flags"])),
        ])
    headers = ["Activity", "Operator", "Distance from Strip", "Hours", "Entry / reservations", "Fees", "Getting there",
               "Booking link", "Social", "Flags"]
    intro = ('<div class="box">Travel-time limit: the brief asks for activities within about one hour of the hotel. '
             'Official pages give Red Rock (about 30 minutes) and Hoover Dam (30 miles). Valley of Fire and Lake Mead distances are not on their official pages. '
             'Drive and transit times from each hotel are not yet verified.</div>')
    return intro + table(headers, rows)


def booking_page():
    b = DATA["booking"]
    dates = table(["Date", "What", "Source"],
                  [[("Date", f"<strong>{esc(d['date'])}</strong>"), ("What", esc(d["what"])), ("Source", link(d["source"], "source") if d["source"].startswith("http") else esc(d["source"]))] for d in b["key_dates"]])
    wins = table(["Item", "Rule (official)", "For Feb 15, 2027", "Source"],
                 [[("Item", f"<strong>{esc(w['item'])}</strong>"), ("Rule", esc(w["rule"])), ("For Feb 15, 2027", esc(w["for_feb_15"])), ("Source", link(w["source"], "source"))] for w in b["windows"]])
    unver = "".join(f"<li>{esc(u)}</li>" for u in b["unverified"])
    return (
        '<h2>Key dates</h2>' + dates +
        '<h2>Booking windows and rules</h2>' + wins +
        '<h2>Cheapest hotel booking time</h2>'
        f'<div class="box">{esc(b["cheapest_hotel_booking_time"])}</div>'
        '<h2>Still unverified</h2><div class="box"><ul class="sum">' + unver + '</ul></div>'
    )


def repo_page():
    rows = []
    for r in DATA["repo_review"]:
        st = r["status"]
        if st.startswith("Verified"):
            badge = '<span class="badge b-ok">' + esc(st) + '</span>'
        elif st.startswith("Unverified"):
            badge = '<span class="badge b-warn">' + esc(st) + '</span>'
        else:
            badge = '<span class="badge b-bad">' + esc(st) + '</span>'
        src = linkify(r["source"]) if "http" in r["source"] else esc(r["source"])
        rows.append([
            ("Item", f"<strong>{esc(r['item'])}</strong>"),
            ("Finding", esc(r["finding"])),
            ("Status", badge),
            ("Source", src),
        ])
    intro = ('<div class="box">Line-by-line review of the repository and the trip brief. Items marked Irregular are listed for manual review. '
             'Source links point to GitHub or the official pages used.</div>')
    return intro + table(["Item", "Finding", "Status", "Source"], rows)


def questions_page():
    q = DATA["questions"]
    ans = table(["Answered", "Answer", "Source"],
                [[("Answered", esc(a["q"])), ("Answer", esc(a["a"])), ("Source", link(a["source"].split(" ")[0], "source"))] for a in q["answered"]])
    miss = table(["Missing information", "Why it matters", "How to find it"],
                 [[("Missing information", f"<strong>{esc(m['q'])}</strong>"), ("Why it matters", esc(m["why"])), ("How to find it", esc(m["how_to_find"]))] for m in q["missing"]])
    return (
        '<h2>Answered from verified sources</h2>' + ans +
        '<h2>Missing before a decision can be made</h2>'
        '<div class="box">Items marked "Your answer" need input from you; the rest can be sourced.</div>' + miss
    )


def suggestions_page():
    rows = []
    for s in DATA["suggestions"]:
        rows.append([
            ("ID", f"<strong>{esc(s['id'])}</strong>"),
            ("Suggestion", esc(s["suggestion"])),
            ("Benefit", esc(s["benefit"])),
            ("Needs", esc(s["needs"])),
            ("Decision", f'<span class="badge b-warn">{esc(s["decision"])}</span>'),
        ])
    intro = ('<div class="box"><strong>Review before any change.</strong> None of these suggestions has been implemented. '
             'Each stays "Pending" until you choose a path.</div>')
    return intro + table(["ID", "Suggestion", "Benefit", "Needs", "Decision"], rows)


def flagged_page():
    rows = [[("Area", esc(f["area"])), ("Item", f"<strong>{esc(f['item'])}</strong>"), ("Reason", esc(f["reason"]))] for f in DATA["flagged"]]
    intro = f'<div class="box"><strong>{len(DATA["flagged"])} items</strong> are flagged for review. Each flagged value is blank or marked on its page.</div>'
    return intro + table(["Area", "Item", "Reason"], rows)


def sources_page():
    rows = [[("Source", esc(s["label"])), ("Link", link(s["url"], s["url"]))] for s in DATA["sources"]]
    return table(["Source", "Link"], rows)


def index_page():
    kpi = (
        '<div class="grid">'
        f'<div class="card"><div class="n">{len(DATA["michelin"])}</div><div class="l">Michelin listings <a href="michelin.html">view →</a></div></div>'
        '<div class="card"><div class="n">4</div><div class="l">Starred restaurants</div></div>'
        f'<div class="card"><div class="n">{len(DATA["hotels"])}</div><div class="l">Hotels ranked <a href="hotels.html">view →</a></div></div>'
        f'<div class="card"><div class="n">{len(DATA["activities"])}</div><div class="l">Activities <a href="activities.html">view →</a></div></div>'
        f'<div class="card"><div class="n">{len(DATA["flagged"])}</div><div class="l">Flagged <a href="flagged.html">view →</a></div></div>'
        '</div>'
    )
    kf = DATA["key_facts"]
    facts = (
        '<div class="box"><strong>Trip window:</strong> ' + esc(kf["trip_window"]) + '<br>'
        '<strong>Preferred:</strong> ' + esc(kf["preferred_dates"]) + '<br>'
        '<strong>7-night scenario:</strong> ' + esc(kf["seven_night_scenario"]) + '<br>'
        '<strong>Party:</strong> ' + esc(kf["party"]) + '</div>'
    )
    summary = '<h2>Executive summary</h2><ul class="sum">' + "".join(f"<li>{linkify(s)}</li>" for s in DATA["executive_summary"]) + "</ul>"
    cats = [
        ("hotels.html", "Hotels", "Ranking by Michelin count, room fit, price status"),
        ("michelin.html", "Michelin restaurants", "24 listings: status, hours, cost, sources"),
        ("activities.html", "Activities", "Within-an-hour options with official hours and fees"),
        ("booking.html", "Booking timing", "Key dates, booking windows, what is unknown"),
        ("questions.html", "Questions", "Answered vs missing information"),
        ("suggestions.html", "Suggestions", "Improvements awaiting your decision"),
        ("flagged.html", "Flagged for review", "Every unverified value"),
        ("repo-review.html", "Repo review", "Irregularities with source links"),
        ("sources.html", "Sources", "All official links used"),
    ]
    tiles = '<div class="grid">' + "".join(
        f'<div class="card"><a href="{h}"><strong>{esc(t)}</strong></a><div class="small">{esc(d)}</div></div>' for h, t, d in cats) + "</div>"
    return kpi + facts + summary + '<h2>Explore</h2>' + tiles


PAGES = {
    "index.html": ("Home", "A simple dashboard for planning the Las Vegas trip. Every value links to an official source, or is marked unverified.", index_page),
    "hotels.html": ("Hotels", "Strip hotels ranked by Michelin restaurants in the same resort. Queen rooms and bathrooms checked against official pages; prices unverified.", hotels_page),
    "michelin.html": ("Michelin restaurants in Las Vegas (2026)", "All 24 Las Vegas listings in the 2026 Michelin Southwest selection, with status, hours and sources.", michelin_page),
    "activities.html": ("Activities within about an hour", "Official facts for the day-trip options we could confirm.", activities_page),
    "booking.html": ("Booking timing", "Key dates and official booking rules. Price timing is not yet verified.", booking_page),
    "questions.html": ("Questions and missing information", "What is answered, what is missing, and how to find it.", questions_page),
    "suggestions.html": ("Suggestions for review", "Choose a path before anything is changed. Every suggestion is Pending.", suggestions_page),
    "flagged.html": ("Flagged for review", "Every value that could not be verified from an official source.", flagged_page),
    "repo-review.html": ("Repo review", "Line-by-line review of the repository and brief, with irregularities flagged.", repo_page),
    "sources.html": ("Sources", "Official and trusted sources used in this site.", sources_page),
}


def main():
    for fname, (title, lead, fn) in PAGES.items():
        (OUT / fname).write_text(page(fname, title, lead, fn()), encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    print(f"Wrote {len(PAGES)} pages to {OUT}")


if __name__ == "__main__":
    main()
