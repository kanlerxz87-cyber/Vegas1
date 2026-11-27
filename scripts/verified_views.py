#!/usr/bin/env python3
"""Official-evidence-gated public views.

The old research datasets are retained, but neither an OTA capture nor a row-level
``verified`` label authorizes a public value. Only individual fields in the
verification manifest may populate comparison cells. No network calls at build time.
"""
from collections import Counter
from datetime import date, timedelta
from html import escape as esc
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
CHECKED = "2026-11-27"
GROUPS = ("restaurants", "hotels", "activities", "transit")
LABELS = {
    "award": "2026 award", "address": "address", "location": "location",
    "days": "days", "hours": "hours", "exceptions": "exceptions",
    "price_2adults": "menu/admission subtotal for two", "phone": "phone",
    "youtube": "YouTube", "instagram": "Instagram", "tiktok": "TikTok",
    "room": "named room", "bed": "bed", "bathroom": "suite bathroom",
    "amenities": "amenities", "total_7n": "all-in seven-night total",
    "within_60_bus": "verified ≤60-minute bus count",
    "within_20_bus": "verified ≤20-minute bus count", "fares": "fares",
}
REQUIRED = {
    "restaurants": ("award", "days", "hours", "exceptions", "price_2adults", "youtube", "instagram", "tiktok"),
    "hotels": ("room", "bed", "bathroom", "amenities", "total_7n", "within_60_bus", "within_20_bus"),
    "activities": ("days", "hours", "exceptions", "price_2adults", "youtube", "instagram", "tiktok"),
    "transit": ("fares",),
}


def load_manifest():
    return json.loads((ROOT / "data/verification.json").read_text(encoding="utf-8"))


def validate_manifest(data):
    """Fail closed on missing rows, missing sources and unsupported public fields.

    This validates the evidence *records*, not the truth of a remote web page.
    The checked source excerpts/observations require human/agent verification.
    """
    errors = []
    for group in GROUPS:
        rows = data.get(group, {})
        if group != "transit":
            original = json.loads((ROOT / f"data/{group}.json").read_text(encoding="utf-8"))[group]
            expected = {r["id"] for r in original}
            if set(rows) != expected:
                errors.append(f"{group}: evidence coverage differs from canonical IDs")
        for rid, row in rows.items():
            if not row.get("name") or row.get("source") not in data["sources"]:
                errors.append(f"{group}/{rid}: missing row identity/reference")
            for key in REQUIRED[group]:
                if key not in row.get("fields", {}):
                    errors.append(f"{group}/{rid}: missing explicit verification state for {key}")
            for key, record in row.get("fields", {}).items():
                source = data["sources"].get(record.get("source"))
                if not source:
                    errors.append(f"{group}/{rid}/{key}: source not found")
                    continue
                if record.get("status") == "verified":
                    if record.get("value") in (None, "", []):
                        errors.append(f"{group}/{rid}/{key}: empty verified value")
                    if source.get("authority") != "official" or source.get("result") != "fetched" or not source.get("checked"):
                        errors.append(f"{group}/{rid}/{key}: no checked official evidence")
                elif record.get("status") != "unverified" or record.get("value") is not None:
                    errors.append(f"{group}/{rid}/{key}: unsupported value must be null/unverified")
    for sid, source in data.get("sources", {}).items():
        parsed = urlsplit(source.get("url", ""))
        if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
            errors.append(f"source {sid}: invalid HTTPS URL")
        if source.get("result") == "fetched":
            try:
                date.fromisoformat(source.get("checked", ""))
            except (TypeError, ValueError):
                errors.append(f"source {sid}: invalid checked date")
    return errors


def value(row, key):
    record = row.get("fields", {}).get(key, {})
    return record.get("value") if record.get("status") == "verified" else None


def link(url, text):
    return f'<a href="{esc(url, quote=True)}" target="_blank" rel="noopener">{esc(text)}</a>'


def blank(reason="Not verified from an official source"):
    return f'<span class="unverified" aria-label="Unverified" title="{esc(reason, quote=True)}">—</span>'


def cell(row, key, note=False):
    record = row.get("fields", {}).get(key, {})
    v = value(row, key)
    if v is None:
        return blank(record.get("note", "Not verified"))
    content = esc(str(v))
    out = f'<span data-evidence="{esc(record["source"])}" data-field="{esc(key)}">{content}</span>'
    if note and record.get("note"):
        out += f'<div class="tiny">{esc(record["note"])}</div>'
    return out


def social(row, key, parent=False):
    record = row.get("fields", {}).get(key, {})
    v = value(row, key)
    if v is None:
        return blank("No official cross-link recorded; this does not mean no account exists")
    urls = v if isinstance(v, list) else [v]
    label = {"youtube": "YouTube", "instagram": "Instagram", "tiktok": "TikTok"}[key]
    text = " · ".join(link(u, f"{label}{' ' + str(i + 1) if len(urls) > 1 else ''}") for i, u in enumerate(urls))
    if parent:
        text += '<div class="tiny">The LINQ parent venue account/channel</div>'
    return f'<span data-evidence="{esc(record["source"])}" data-field="{esc(key)}">{text}</span>'


def references(data, row):
    keys = [row["source"]] + [f["source"] for f in row["fields"].values() if f["status"] == "verified"]
    refs = []
    for key in dict.fromkeys(keys):
        s = data["sources"][key]
        label = "MICHELIN list" if key == "michelin" else urlsplit(s["url"]).hostname.replace("www.", "")
        state = "read " + s["checked"] if s["result"] == "fetched" else "reference not rechecked"
        refs.append(link(s["url"], label) + f'<div class="tiny">{esc(state)}</div>')
    return '<div class="source-links">' + "".join(refs) + "</div>"


def missing(row, keys):
    return [LABELS.get(k, k) for k in keys if value(row, k) is None]


def table(headers, rows, caption, table_id=""):
    identity = f' id="{esc(table_id)}"' if table_id else ""
    ths = "".join(f'<th scope="col">{esc(h)}</th>' for h in headers)
    return (f'<div class="scroll" role="region" aria-label="{esc(caption)}" tabindex="0">'
            f'<table class="data"{identity}><caption>{esc(caption)}</caption><thead><tr>{ths}</tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div>')


def panel(title, body, ident="", extra=""):
    identity = f' id="{esc(ident)}"' if ident else ""
    return f'<section class="panel {extra}"{identity}><h2>{esc(title)}</h2>{body}</section>'


def legend():
    return ('<p class="note"><strong>— = unverified, not free, closed or sold out.</strong> '
            'Current published hours and menu subtotals are not promises of 2027 availability. '
            'Social links are official-site cross-links; their target pages were not all opened. '
            'Scroll tables horizontally on a phone. <a href="verification.html">Field-level audit</a>.</p>')


def cards(items):
    return '<section class="grid4">' + "".join(
        f'<div class="card"><div class="big">{esc(str(number))}</div><div class="lbl">{esc(label)}</div><p>{body}</p></div>'
        for number, label, body in items) + '</section>'


def review_link(group, rid):
    return f'<a href="verification.html#{esc(group)}-{esc(rid)}">Evidence &amp; gaps</a>'


def cluster_definitions():
    return [
        ("MGM Grand", ["joel-robuchon", "latelier-robuchon"]),
        ("Caesars Palace", ["guy-savoy"]),
        ("The Cosmopolitan", ["e-by-jose-andres", "china-poblano"]),
        ("The Venetian / Palazzo resort", ["mott-32", "cote", "bouchon", "estiatorio-milos"]),
        ("Wynn", ["wing-lei"]), ("ARIA", ["gymkhana"]),
        ("Bellagio — currently closed listing", ["michael-mina"]),
        ("Resorts World", ["stubborn-seed"]),
        ("Spring Mountain / S. Decatur address corridor (not a timed journey)",
         ["partage", "kabuto", "kame-omakase", "lamaii", "sparrow-and-wolf", "pho-ga-bac-bac", "yen-viet-kitchen"]),
        ("Arts District / S. Main area (not a timed journey)", ["esthers-kitchen", "soulbelly-bbq"]),
        ("W. Russell Road", ["anima-by-edo"]), ("Gold Coast", ["ping-pang-pong"]),
    ]


def build_verified_pages(page, legacy_flagged):
    data = load_manifest()
    errors = validate_manifest(data)
    if errors:
        raise ValueError("Evidence validation failed:\n" + "\n".join(errors))
    R, H, A, T = [data[k] for k in GROUPS]
    awards = Counter(value(r, "award") for r in R.values())
    starred = [r for r in R.values() if value(r, "award") in ("1 star", "2 stars", "3 stars")]
    pages = {}
    guide = link(data["sources"]["michelin"]["url"], "MICHELIN 2026 official selection")
    rtc = link(data["sources"]["rtc-trip"]["url"], "RTC journey planning")
    source_file = link("https://github.com/kanlerxz87-cyber/Vegas1/blob/main/data/verification.json", "field-evidence JSON")

    # Overview: no speculative travel metric or third-party price is a headline.
    body = panel("A plan for two, with a clear evidence boundary", """
<p><strong>Working dates: 15–22 February 2027 (7 nights, 2 adults, 1 room).</strong>
The preferred 15–18 February window is only three nights. Starting the seven-night comparison on 15 February
keeps the preferred arrival date without silently shortening the requested 1–2-week trip.
A possible 14-night version is 15 February–1 March; it has not been priced.</p>
<p><strong>This is a research dashboard, not a booking-ready recommendation.</strong> All entries are retained,
but official all-in hotel totals and dated bus itineraries are still missing. Those cells are blank—not inferred
from rounded nightly averages, third-party quotes, route maps or assumed walking/waiting times.</p>
<p><a href="summary.html">Read the executive summary &amp; draft week</a> ·
<a href="flagged.html">Flagged for Review</a> · <a href="questions.html">What still needs evidence</a></p>
""")
    body += cards([
        (len(R), "MICHELIN listings", f'{len(starred)} starred · {awards["Bib Gourmand"]} Bib Gourmand · {awards["Recommended"]} Recommended. {guide}'),
        (len(H), "hotel candidates", 'All-in seven-night prices and bus-threshold counts remain unverified. <a href="hotels.html">Compare evidence</a>.'),
        (len(A), "activity entries", 'Hours, starting admission for two and official cross-links where confirmed. <a href="activities.html">Things to do</a>.'),
        ("Not established", "cheapest hotel / week", 'No comparable official final totals support a cheapest-date or best-buy claim. <a href="pricing.html">Quote attempts</a>.'),
    ])
    body += panel("The four starred restaurants", '<ul class="tight">' + "".join(
        f'<li>{link(data["sources"][r["source"]]["url"], r["name"])} — {esc(value(r,"award"))} · {esc(value(r,"location"))}</li>'
        for r in starred) + f'</ul><p>{guide}. Bib Gourmand and Recommended are listed separately; neither means a star.</p>')
    body += panel("What changes the decision", """
<ol class="tight">
<li><strong>Bus access is not proved.</strong> The inherited zone model put every hotel at 24/24 inside 60 minutes,
but it used assumptions and non-bus modes. That does not establish any real hotel-to-restaurant journey.
Neither the 60-minute count nor the 20-minute substitute is used as a verified ranking. <a href="flagged.html#F-59">F-59</a>.</li>
<li><strong>Room fit is specific to a named room.</strong> A hotel homepage or an assigned-on-arrival rate is not a
queen/king-bed guarantee. The hotel table distinguishes verified room descriptions from unverified offers.</li>
<li><strong>The Cromwell-era quote cannot price the new brand.</strong> The inherited row now refers to The Vanderpump Hotel;
its old price is not displayed as a current quote. <a href="flagged.html#F-47">F-47</a>.</li>
<li><strong>Current menus are not final trip budgets.</strong> Restaurant and activity subtotals show their arithmetic and
excluded/unknown charges. Michael Mina is currently marked temporarily closed; 2027 reopening is not established.</li>
</ol>""")
    body += panel("How to use this without making a premature purchase", '<p>Start with the restaurant clusters, compare named-room evidence, then use the official quote and route links. '
                  'The <a href="suggestions.html">suggestions backlog</a> separates proposed decision improvements from implemented factual corrections. '
                  'No booking, deposit, account creation or paid transaction was performed.</p>')
    pages["index.html"] = page("index.html", "Las Vegas for two · 2027", "15 February–23 March · 7–14 nights · official-source facts, explicit gaps", body)

    # Hotels: unknown values never fall back to the old model or OTA dataset.
    hrows = []
    for rid, r in sorted(H.items(), key=lambda kv: kv[1]["name"].casefold()):
        state = "room details checked" if value(r, "room") else "room/offer not verified"
        hrows.append(f'<tr data-row="hotels/{esc(rid)}"><th scope="row">{esc(r["name"])}<div class="tiny">{state}</div>{review_link("hotels",rid)}</th>'
                     f'<td>{cell(r,"room")}</td><td>{cell(r,"bed")}</td><td>{cell(r,"bathroom")}</td>'
                     f'<td>{cell(r,"amenities")}</td><td>{cell(r,"within_60_bus")}</td><td>{cell(r,"total_7n")}</td>'
                     f'<td>{references(data,r)}</td></tr>')
    body = panel("No verified price/transit ranking yet", '<p>The requested order needs comparable official all-in totals for the same dates and named room, '
                 'plus timed <strong>bus</strong> journeys including walks, waiting, transfers and the return trip. Those inputs have not been obtained. '
                 'This table is alphabetical, <strong>not a best-hotel ranking</strong>. The prior 24/24 model and its 20-minute tiebreaker have been withdrawn from the verified comparison. '
                 '<a href="flagged.html#F-70">F-70</a>.</p>' + legend())
    body += panel("Every hotel candidate", table(
        ["Candidate (alphabetical)", "Named room", "Bed", "Suite bathroom", "Amenities", "MICHELIN ≤60 min by bus", "Official all-in 7 nights · 15–22 Feb · USD", "Official references"],
        hrows, "32 hotel research candidates; dashes indicate unverified fields", "every-hotel"))
    body += panel("Location-first review shortlist — not a value ranking", f"""
<ul class="tight">
<li><strong>The Venetian / Palazzo:</strong> named King suites and suite bathrooms are described on their operator pages.
Mott 32, COTE, Bouchon and Milos are in the same resort complex in the official guide. No bus time or room price is implied.</li>
<li><strong>Caesars Palace:</strong> the official Julius Deluxe 1 King room has a described in-room bathroom; Guy Savoy is listed at Caesars Palace.
The exact-date booking page returned a technical-error banner and no final taxed total.</li>
<li><strong>Wynn:</strong> the exact-date operator page describes Resort King bedding/bathroom; Wing Lei is listed at Wynn.
Its average nightly Cyber price excludes tax and is not used as a final seven-night quote.</li>
<li><strong>Desert Rose and Cliffs at Peace Canyon:</strong> operator pages describe King-bed suites and kitchen/bath facilities.
Neither has a verified door-to-door one-hour bus itinerary here; Cliffs is not presented as a convenient Strip alternative.</li>
</ul><p>Property co-location comes from {guide}; room evidence is linked in the rows above. A named room description is not a reservation.</p>""")
    body += panel("Dates and booking timing", '<p>Use <a href="pricing.html#cheapest-week">the official quote-attempt log</a>. '
                  'No cheapest week, cheapest purchase day, final resort-fee/tax addition or unassigned-room price is endorsed.</p>')
    pages["hotels.html"] = page("hotels.html", "Hotels", "All 32 candidates retained; only individually supported official fields are populated.", body)

    # Restaurants: all tiers, verified published hours, costs for two and cross-links.
    rrows = []
    order = {"2 stars": 0, "1 star": 1, "Bib Gourmand": 2, "Recommended": 3}
    for rid, r in sorted(R.items(), key=lambda kv: (order[value(kv[1], "award")], kv[1]["name"])):
        tier = "star" if value(r, "award") in ("1 star", "2 stars") else ("bib" if value(r, "award") == "Bib Gourmand" else "rec")
        rrows.append(f'<tr data-row="restaurants/{esc(rid)}"><th scope="row">{link(data["sources"][r["source"]]["url"],r["name"])}'
                     f'<div class="tiny">{cell(r,"location")}</div>{review_link("restaurants",rid)}</th>'
                     f'<td><span class="badge {tier}">{cell(r,"award")}</span></td>'
                     f'<td>{cell(r,"days")}<div class="tiny">{cell(r,"hours")}</div></td>'
                     f'<td class="tiny">{cell(r,"exceptions")}</td><td>{cell(r,"price_2adults",True)}</td>'
                     f'<td>{social(r,"youtube")}</td><td>{social(r,"instagram")}</td><td>{social(r,"tiktok")}</td>'
                     f'<td>{references(data,r)}</td></tr>')
    body = panel("2026 guide status, not historic stars", f'<p>{guide}. The Las Vegas rows contain {len(starred)} starred restaurants '
                 f'({awards["2 stars"]} two-star, {awards["1 star"]} one-star), {awards["Bib Gourmand"]} Bib Gourmand and {awards["Recommended"]} Recommended. '
                 'The two official press pages have different publication dates; no exact ceremony date is inferred (<a href="flagged.html#F-71">F-71</a>).</p>' + legend())
    body += panel("All MICHELIN listings", table(["Restaurant / location", "2026 award", "Published days & hours", "Exceptions", "Menu subtotal · 2 adults · USD", "YouTube", "Instagram", "TikTok", "Official evidence"], rrows, "MICHELIN restaurants: stars, Bib Gourmand and Recommended", "restaurant-list"))
    crows = []
    for label, ids in cluster_definitions():
        names = " · ".join(link(data["sources"][R[i]["source"]]["url"], R[i]["name"]) for i in ids)
        crows.append(f'<tr><th scope="row">{esc(label)}</th><td>{names}</td><td>{guide}</td></tr>')
    body += panel("Dining clusters — co-location, not travel-time estimates", '<p>These groupings use the official property names/addresses. '
                 'They do not establish walking or bus times and are not substituted for the requested one-hour hotel ranking.</p>' + table(
                     ["Property / address group", "Listings", "Address / award source"], crows, "All 24 listings grouped by published location", "clusters"))
    body += panel("How to read the dinner budget", '<p id="costs"><strong>All amounts shown are for two menu orders, not per-person prices.</strong> '
                 'Where the venue prints a menu price, multiplying by two is labelled arithmetic—not an all-in quote. Taxes, tips/service, drinks, '
                 'supplements and trip-date availability must not be silently added or assumed included. Guy Savoy individual dish prices are not complete dinners; its total stays blank. '
                 'KAME’s earlier price was captured on OpenTable without an operator authorization cross-link in this audit, so it is not promoted to an official-only price. '
                 'Michael Mina’s menu is visible but the venue is currently marked temporarily closed. <a href="questions.html#Q-04">Q-04</a>.</p>')
    pages["restaurants.html"] = page("restaurants.html", "MICHELIN restaurants", "24 Las Vegas listings · awards separated clearly · current official facts, not inferred 2027 availability", body)

    arows = []
    for rid, r in A.items():
        parent = rid == "high-roller"
        arows.append(f'<tr data-row="activities/{esc(rid)}"><th scope="row">{link(data["sources"][r["source"]]["url"],r["name"])}<br>{review_link("activities",rid)}</th>'
                     f'<td>{cell(r,"days")}<div class="tiny">{cell(r,"hours")}</div></td><td class="tiny">{cell(r,"exceptions")}</td>'
                     f'<td>{cell(r,"price_2adults",True)}</td><td>{social(r,"youtube",parent)}</td><td>{social(r,"instagram",parent)}</td><td>{social(r,"tiktok")}</td><td>{references(data,r)}</td></tr>')
    body = panel("Five activity options", legend() + table(["Activity", "Published days & hours", "Exceptions / scope", "2 adults · USD", "YouTube", "Instagram", "TikTok", "Official evidence"], arows, "Activities with official opening/admission evidence", "activity-list"))
    body += panel("Scheduling and ticket cautions", '<p>Mob Museum’s current museum hours are <strong>9 AM–9 PM every day</strong>; the previous Thursday 4 PM closing was a dated exception, not a weekly rule. '
                  'Neon’s <strong>2027 Admission</strong> has replaced the earlier 2026 day/evening split. High Roller’s page conflicts internally on opening/ticket eligibility, so its complete hours are blank. '
                  'Fremont’s current Music Reels schedule starts at <strong>6 PM</strong>. These corrections and their sources are in <a href="flagged.html#F-72">F-72</a>.</p>')
    body += panel("Not silently added", '<p>Bellagio Fountains and the Conservatory remain in the historical discovery-gap register, not in the verified activity table: '
                  'a working official schedule was not established for them in this integration. No extra show, paid tour or 2027 Sphere ticket has been invented.</p>')
    pages["activities.html"] = page("activities.html", "Things to do", "Official published schedules, starting costs for two, and explicit social-link gaps.", body)

    # Transit: no zone matrix enters the public table.
    trows = []
    for rid, r in T.items():
        trows.append(f'<tr data-row="transit/{esc(rid)}"><th scope="row">{esc(r["name"])}</th><td>{cell(r,"fares")}</td>'
                     f'<td>{cell(r,"hours")}</td><td>{cell(r,"exceptions")}</td><td>{references(data,r)}</td></tr>')
    body = panel("Bus journeys, not a substituted travel model", f'<p>Las Vegas has no subway. RTC buses are the relevant mode for the requested bus constraint; '
                 'Monorail and Vegas Loop are shown only as optional alternatives, not as proof of compliance. '
                 f'The official planning resource is {rtc}.</p><p><strong>No complete dated hotel-to-restaurant bus itinerary was obtained.</strong> '
                 'A verified route map, fare or in-vehicle segment is insufficient to prove a door-to-door limit. '
                 'Include access walks, waiting, transfers, dinner finishing time and the return journey. '
                 'Neither 24/24 inside 60 minutes nor the derived 20-minute counts are verified.</p>')
    body += panel("Operator fares and published hours", table(["System / product", "Published fares · per person", "Hours", "Restrictions", "Official source"], trows, "Transport information; optional non-bus modes clearly identified"))
    body += panel("Why the old matrix is not a booking decision", '<p id="matrix">The earlier zone matrix is retained in the repository as unvalidated research, '
                  'not rendered as real journey minutes. The former hotel ranking depended on those assumptions and has been withdrawn from the verified comparison '
                  '(<a href="flagged.html#F-59">F-59</a>). There is no claim that every hotel is within an hour of every restaurant.</p>'
                  f'<p>{rtc} supplies the discovery path. Record exact origin/destination, service date, departure/arrival time and each leg before filling any hotel count.</p>')
    body += panel("Do not mix fare products", '<p>RTC residential regular single fare is <strong>$2</strong>; <strong>$1</strong> is reduced fare, not the visitor default. '
                  'The Monorail’s separate $1 local fare requires eligible Nevada ID and has purchase limits. '
                  'For electronic Monorail tickets, 10 singles cost $57.50, below the $59.95 seven-day pass; 11 singles cost $63.25. '
                  'That is fare arithmetic only—not a recommendation that this couple will use 11 rides, or that stations satisfy the restaurant walking/bus constraint.</p>'
                  f'<p>{link(data["sources"]["rtc-fares"]["url"],"RTC fares")} · {link(data["sources"]["monorail-fares"]["url"],"Monorail ticket terms")}</p>')
    pages["transit.html"] = page("transit.html", "Getting around", "Official fares are supported; hotel-to-dinner bus durations remain unverified.", body)

    # Pricing: quote evidence, not nightly-average extrapolation.
    qrows = []
    for key, name in [("quote-caesars", "Caesars Palace · Julius Deluxe 1 King"), ("quote-wynn", "Wynn · Resort King"), ("quote-venetian", "The Venetian")]:
        s = data["sources"][key]
        qrows.append(f'<tr><th scope="row">{esc(name)}</th><td>15–22 February 2027 · 7 nights · 2 adults</td><td>{blank()}</td><td>{esc(s["note"])}</td><td>{link(s["url"],"Official dated engine")}</td></tr>')
    body = panel("Official all-in totals: not obtained", '<p id="cheapest-week">There is no verified cheapest hotel, stay window or future purchase date. '
                 'Historical Booking.com totals are not displayed as official price comparisons. The date range contains <strong>30 possible seven-night start dates</strong> '
                 '(15 February–16 March, checkout by 23 March); the old four-window sample was not exhaustive. No unpriced week is labelled sold out.</p>' + legend())
    body += panel("Exact-date source checks · 27 November 2026", table(["Hotel / named room", "Requested stay", "Final official total · USD", "What the source returned / limitation", "Source"], qrows, "Read-only quote attempts; no checkout or booking submitted"))
    body += panel("A verified booking-offer window, not proof of the best date", '<p>Wynn’s public Cyber offer terms on the exact-date engine say '
                  '<strong>book 20 November–4 December 2026</strong> for eligible stays <strong>22 November 2026–30 June 2027</strong>, one to 14 nights. '
                  'The page describes a 72-hour cancellation rule with a one-night room-and-tax penalty and a one-night deposit at booking. '
                  'Availability, final taxed total and the exact rate’s full terms still need confirmation. An advertised sale deadline does not establish that booking now is cheaper than booking later.</p>'
                  f'<p>{link(data["sources"]["quote-wynn"]["url"],"Wynn official exact-date offer/terms")}</p>')
    body += panel("A couple’s budget should use like-for-like totals", '<ul class="tight"><li>One named queen-or-larger room with an in-room/private bathroom; two adults; seven nights.</li>'
                  '<li>Room + mandatory resort/property fees + taxes in the same currency, with refundable/cancellation terms recorded.</li>'
                  '<li>No multiplication of a rounded average-nightly display into an exact stay total; no blanket tax rate or resort-fee assumption.</li>'
                  '<li>Restaurant and activity <a href="restaurants.html#costs">subtotals for two</a> are separate from final all-in amounts.</li>'
                  '<li>The 14-night extension (15 February–1 March) is still unpriced; do not double a seven-night quote.</li></ul>')
    pages["pricing.html"] = page("pricing.html", "Pricing & booking timing", "Actual official-engine observations; blanks where no reliable final total was returned.", body)

    # Current questions/suggestions are data-driven; no user input is needed to publish.
    Q = json.loads((ROOT / "data/questions.json").read_text())["questions"]
    qcards = []
    for q in Q:
        source_html = " · ".join(link(u, urlsplit(u).hostname or "Source") for u in q.get("sources", []))
        qcards.append(f'<article class="qa" id="{esc(q["id"])}"><h3><span class="qid">{esc(q["id"])}</span> {esc(q["question"])}'
                      f'<span class="state {"ok" if q["state"] == "answered" else "warn"}">{esc(q["state"])}</span></h3>'
                      f'<p><strong>Known:</strong> {esc(q["answer"])}</p><p><strong>Missing / risk:</strong> {esc(q.get("problem", ""))}</p>'
                      f'<p><strong>Next evidence step:</strong> {esc(q["how_to_close"])}</p><p class="tiny">{source_html or "Basis: the trip brief and date arithmetic, not an external price claim."}</p></article>')
    body = panel("Questions do not hold this site for manual input", '<p>This register distinguishes known facts, unknowns and safe working assumptions. '
                 'Publication and factual corrections were completed autonomously; these are evidence gaps for later decision-making, not a request for you to fill out a form. '
                 'No unanswered question is silently converted into a travel-time or cost estimate.</p>') + "".join(qcards)
    pages["questions.html"] = page("questions.html", "Open questions", "What is known, what is still missing, why it matters and how to discover it.", body)

    suggestions = json.loads((ROOT / "data/suggestions.json").read_text())["suggestions"]
    scards = []
    for s in suggestions:
        scards.append(f'<article class="sug" id="{esc(s["id"])}"><h3><span class="sid">{esc(s["id"])}</span> {esc(s["title"])} '
                      f'<span class="pill">{esc(s["status"])}</span></h3><p>{esc(s["body"])}</p><p class="trade"><strong>Trade-off:</strong> {esc(s["trade_off"])}</p>'
                      f'<p class="tiny">Basis: {esc(s["evidence"])}</p><p>{" · ".join(link(u,"Official / evidence source") for u in s.get("sources",[]))}</p></article>')
    body = panel("Review proposals before changing the plan", f'<p>{len(suggestions)} suggestions are kept separate from verified facts. '
                 'Optional trip choices and new decision features have not been silently implemented. Corrections needed to avoid false prices, hours or route claims are already applied and logged in the flag register. '
                 'No purchase or reservation was made, and no manual input is required for this site to remain usable.</p>') + "".join(scards)
    pages["suggestions.html"] = page("suggestions.html", "Suggestions", "A reviewable backlog with decision value, trade-offs and evidence links.", body)

    # Executive summary and proposed week. Dates are arithmetic, not availability claims.
    itinerary = [
        (0, "Arrival and room check", "Confirm named bed/bath; optional High Roller only after opening/ticket conflict is resolved", "a-high-roller"),
        (1, "MGM Grand dining focus", "Joël Robuchon is currently published Tuesday–Saturday; seek a confirmed reservation, not an assumed seat", "r-joel-robuchon"),
        (2, "The Cosmopolitan dining focus", "é is currently published Tuesday–Saturday; only two seatings nightly, availability not obtained", "r-e-by-jose-andres"),
        (3, "Downtown option", "Choose or split Mob Museum, Neon Museum and Fremont; plan each bus leg rather than assuming a 30-minute transfer", "a-mob-museum"),
        (4, "Venetian / Palazzo cluster", "Choose one of Mott 32, COTE, Bouchon or Milos; prices/reservations remain venue-specific", "r-mott-32"),
        (5, "Spring Mountain option", "Partage currently publishes Tuesday–Saturday dinner; check diet constraints and both bus directions", "partage-contact"),
        (6, "Final dinner / flexible day", "L’Atelier currently publishes Sunday dinner; keep the day flexible if bookings do not confirm", "r-latelier-robuchon"),
        (7, "Checkout / departure", "22 February completes seven nights; extension to 1 March is a separate unpriced 14-night option", "h-caesars-palace"),
    ]
    irows = []
    for offset, focus, detail, sid in itinerary:
        day = date(2027, 2, 15) + timedelta(days=offset)
        irows.append(f'<tr><th scope="row">{day.strftime("%a %d %b %Y")}</th><td>{esc(focus)}</td><td>{esc(detail)}</td><td>{link(data["sources"][sid]["url"],"Official reference")}</td></tr>')
    body = panel("Executive summary", f"""
<ul class="tight">
<li><strong>Planning basis:</strong> two adults, 15–22 February 2027, seven nights. This preserves the preferred arrival; the three-night preferred span cannot contain a one-week trip. No flights or room were purchased.</li>
<li><strong>Dining:</strong> {len(R)} Las Vegas MICHELIN listings: {len(starred)} starred, {awards['Bib Gourmand']} Bib Gourmand, {awards['Recommended']} Recommended. {guide}.</li>
<li><strong>Hotels:</strong> {len(H)} research candidates. Venetian/Palazzo, Caesars Palace and Wynn have named-room evidence linked in the hotel table; Desert Rose and Cliffs have suite evidence but no confirmed one-hour bus access. No cheapest or best-value winner is established.</li>
<li><strong>Transport:</strong> no subway; use RTC for the requested bus constraint. Monorail/Loop are optional, separate modes. The old model is not a timed itinerary and does not prove all restaurants are reachable inside an hour.</li>
<li><strong>Budget:</strong> no reliable official all-in seven-night hotel total. Restaurant/activity numbers are explicitly labelled current base subtotals for two, not final trip quotes. Do not book around the current Michael Mina listing: it is temporarily closed.</li>
<li><strong>Booking timing:</strong> Wynn’s published public Cyber booking window ends 4 December 2026; that is a verified offer period, not proof of the cheapest future booking day. No universal cheapest stay week is known.</li>
</ul><p><a href="pricing.html">Read the quote evidence</a> · <a href="flagged.html">Review the flags</a> · <a href="suggestions.html">Compare suggestions</a></p>""")
    body += panel("Draft week — suggestions, not confirmed availability", '<p>The following is an organizational starting point. '
                 'It uses current published weekly hours, not booked 2027 seats, tickets or transport. No transfer time is assumed. '
                 'The downtown entries may be split across days rather than squeezed into a single afternoon.</p>' + table(
                     ["Date", "Proposed focus", "What to confirm before committing", "Official reference"], irows, "Proposed seven-night trip skeleton, 15–22 February 2027"))
    pages["summary.html"] = page("summary.html", "Executive summary", "The practical plan, its unresolved decision blockers and a non-booked draft week.", body)

    # Per-row audit: explicit nulls and source notes make incomplete verification inspectable.
    audit_blocks = []
    gap_rows = []
    approved = Counter()
    for group in GROUPS:
        rows = []
        for rid, r in data[group].items():
            required = REQUIRED[group]
            ok = [LABELS.get(k, k) for k in r["fields"] if value(r, k) is not None]
            gaps = missing(r, required)
            approved[group] += len(ok)
            notes = []
            for k, f in r["fields"].items():
                if f.get("note") and (f["status"] == "verified" or k in ("total_7n", "hours", "price_2adults", "address")):
                    notes.append(f'<li><strong>{esc(LABELS.get(k,k))}:</strong> {esc(f["note"])}</li>')
            rows.append(f'<tr id="{esc(group)}-{esc(rid)}"><th scope="row">{esc(r["name"])}</th><td>{esc(", ".join(ok)) or "No public value approved"}</td>'
                        f'<td>{esc(", ".join(gaps)) or "No missing required fields"}</td><td><details><summary>Evidence limits</summary><ul>{"".join(notes)}</ul></details></td><td>{references(data,r)}</td></tr>')
            if gaps:
                flags = " · ".join(f'<a href="flagged.html#{esc(fid)}">{esc(fid)}</a>' for fid in r.get("flags", []))
                gap_rows.append(f'<tr><th scope="row">{esc(r["name"])}</th><td>{esc(", ".join(gaps))}</td><td>{review_link(group,rid)}<br>{flags}</td><td>{references(data,r)}</td></tr>')
        audit_blocks.append(panel(group.title() + " · field-by-field evidence", table(["Entry", "Approved public fields", "Unverified required fields", "Notes", "References"], rows, group.title() + " verification log"), group))
    body = panel("What verified means here", f'<p>A value is published only when its own record names an official source read on the checked date. '
                 'A source link does not verify every field, and an old row-level badge does not override a null. '
                 'Every canonical restaurant, hotel and activity ID is covered, including incomplete rows. Source observations are recorded in the {source_file}.</p>'
                 '<p>“Read” describes the source-page fetch, not a comprehensive live-link guarantee. Social target pages and every hotel/archived link were not all opened. '
                 'The offline validator checks HTML structure, internal links/anchors, evidence coverage and root/docs parity—not remote availability or truth.</p>') + "".join(audit_blocks)
    pages["verification.html"] = page("verification.html", "Line-by-line verification", "Per-entry, per-field approvals, explicit nulls, checked source dates and limits.", body)

    # Preserve the earlier flag register and audit history, with an explicit current-policy banner.
    old_flags = legacy_flagged()
    banner = panel("Current policy supersedes historical price and model claims", '<p>The 25–26 November audit tables below are retained as historical findings. '
                   'They may quote superseded figures or describe the older UI; those are not current booking offers. '
                   'The live comparisons now use the strict official-field gate (F-70). '
                   'Unverified values are blank even if an older note says they were “shown as captured”. '
                   'Flags are published without blocking deployment of a structurally valid site.</p>')
    banner += panel("Current missing-information register", table(["Entry", "Missing / unverified", "Review / next evidence", "Official reference"], gap_rows, "Every entry with missing required evidence"), "current-gaps")
    old_flags = old_flags.replace('<section class="panel" id="status">', banner + '<section class="panel" id="status">', 1)
    old_flags = old_flags.replace('were checked against an official page this session', 'were checked in the dated historical review, not re-verified by the offline build')
    pages["flagged.html"] = old_flags

    srows = []
    for sid, s in data["sources"].items():
        srows.append(f'<tr id="source-{esc(sid)}"><th scope="row">{esc(sid)}</th><td>{link(s["url"],urlsplit(s["url"]).hostname)}</td>'
                     f'<td>{esc(s["authority"])}</td><td>{esc(s["result"])}<div class="tiny">{esc(s.get("checked") or "Not rechecked")}</div></td><td>{esc(s["note"])}</td></tr>')
    body = panel("Official-source ledger", '<p>Only field records backed by a fetched <strong>official</strong> source can populate the comparison tables. '
                 'A reservation-platform page without a verified operator authorization link is a discovery lead, not official evidence. '
                 'Unchecked hotel reference URLs are explicitly labelled and do not authorize any room, rate or transit assertion.</p>' + legend() + table(
                     ["Evidence key", "Source", "Authority", "Fetch state / date", "What was read / limits"], srows, "All field-evidence sources and their actual check state", "source-ledger"))
    body += panel("Historical evidence is not a current quote", '<p>Earlier snapshots, abandoned claims and independent builds remain in the repository for traceability; '
                  'they have not all been reverified or made compliant with this publication gate. '
                  'Use the <a href="flagged.html">historical flag register</a> for why old numbers were withdrawn, not as a rate sheet. '
                  f'The current authoritative publication manifest is the {source_file}.</p>')
    pages["sources.html"] = page("sources.html", "Sources", "Exact source pages, observation notes and an honest distinction between fetched and unchecked references.", body)

    counts = [("Restaurant rows covered", len(R), "michelin"), ("Hotel candidates covered", len(H), "quote-caesars"),
              ("Activity rows covered", len(A), "a-mob-museum"),
              ("Official all-in hotel totals verified", sum(value(r,"total_7n") is not None for r in H.values()), "quote-wynn"),
              ("Hotel bus-threshold counts verified", sum(value(r,"within_60_bus") is not None for r in H.values()), "rtc-trip"),
              ("Restaurant menu subtotals for two supported", sum(value(r,"price_2adults") is not None for r in R.values()), "michelin"),
              ("Restaurant Instagram cross-links recorded", sum(value(r,"instagram") is not None for r in R.values()), "r-gymkhana")]
    countrows = [f'<tr><th scope="row">{esc(label)}</th><td>{number}</td><td>{link(data["sources"][sid]["url"],"Related official source")} · {source_file}</td></tr>' for label,number,sid in counts]
    body = panel("Integration review · 27 November 2026", '<p>Every current canonical ID is covered by the field manifest. '
                 'This is <strong>not a claim that every requested fact was obtainable</strong>. Unknown facts are explicit nulls; travel rankings and total prices remain unestablished. '
                 'Corrections to Guy Savoy pricing, RTC fares, restaurant/activity hours and unsupported model statements are published with official links.</p>' + table(
                     ["Measure", "Count", "Evidence / reproducibility"], countrows, "Counts derived from current field evidence"))
    body += panel("Checks performed before publishing", '<ul class="tight"><li>Python data integrity and model-research build.</li>'
                  '<li>Field-manifest coverage and fail-closed source checks; regression tests for blank unknowns and suppression of old OTA/model values.</li>'
                  '<li>HTML internal links/anchors, duplicate IDs, table-row references, mobile viewport and identical root/docs output.</li>'
                  '<li>Source-page reads recorded separately; local link validation does not claim every remote URL was fetched.</li></ul>'
                  '<p>Parallel-session records and preserved historical audits remain in '
                  + link("https://github.com/kanlerxz87-cyber/Vegas1/blob/main/COORDINATION.md", "COORDINATION.md") + '.</p>')
    pages["repo-review.html"] = page("repo-review.html", "Repo review", "What the integration actually verified, what tests cover and what remains unresolved.", body)
    return pages
