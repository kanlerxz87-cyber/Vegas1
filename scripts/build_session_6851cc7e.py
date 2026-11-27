#!/usr/bin/env python3
"""Build mobile-friendly Las Vegas verification subsite in docs/session-6851cc7e/
from verified structured datasets in data/session-6851cc7e-*.json.
"""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "docs" / "session-6851cc7e"

NAV_ITEMS = [
    ("index.html", "Executive Summary"),
    ("hotels.html", "Hotels (15 Official IBEs)"),
    ("costs.html", "Combined Costs & Calculator"),
    ("michelin.html", "MICHELIN (24)"),
    ("activities-transit.html", "Activities & Transit"),
    ("questions-suggestions.html", "Q&A & Suggestions"),
    ("repo-review.html", "Repo Audit (14)"),
    ("flagged.html", "Flagged (22)"),
]


def esc(val: object) -> str:
    if val is None:
        return ""
    return html.escape(str(val), quote=True)


def money(val: float | None) -> str:
    if val is None:
        return '<span class="blank-cell" title="Unverified / unavailable on official booking engine — left blank per strict evidence rule">— (Blank)</span>'
    return f"${val:,.2f}"


CSS = """\
:root {
  --bg: #f7f6f2;
  --surface: #ffffff;
  --surface-alt: #f0eee8;
  --ink: #16181d;
  --muted: #525866;
  --border: #dcd8ce;
  --accent: #8b1e24;
  --accent-soft: #faeef0;
  --gold: #8a5a00;
  --gold-bg: #fff6db;
  --green: #0f5c3a;
  --green-bg: #e7f6ee;
  --blue: #184980;
  --blue-bg: #eaf2fb;
  --warn: #7c3a00;
  --warn-bg: #fff1e0;
  --radius: 12px;
  --shadow: 0 2px 8px rgba(22, 24, 29, 0.06);
}
* { box-sizing: border-box; }
html { font-size: 16px; -webkit-text-size-adjust: 100%; }
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Inter, Helvetica, Arial, sans-serif;
  background: var(--bg);
  color: var(--ink);
  line-height: 1.55;
}
a { color: var(--blue); text-decoration: underline; text-underline-offset: 2px; }
a:hover { color: var(--accent); }
.skip-link {
  position: absolute; left: -9999px; top: 0;
  background: var(--ink); color: #fff; padding: 8px 14px; z-index: 999;
}
.skip-link:focus { left: 12px; top: 12px; }
.site-header {
  background: #14161b;
  color: #f8f7f4;
  border-bottom: 3px solid var(--accent);
  position: sticky;
  top: 0;
  z-index: 50;
}
.header-inner {
  max-width: 1220px;
  margin: 0 auto;
  padding: 12px 16px 8px;
}
.brand-row {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  justify-content: space-between;
  gap: 8px;
}
.brand-title {
  font-size: 1.05rem;
  font-weight: 700;
  letter-spacing: -0.01em;
  color: #fff;
  text-decoration: none;
}
.brand-meta {
  font-size: 0.78rem;
  color: #c8cbd2;
}
.brand-meta a { color: #ffd9df; }
.nav-scroller {
  display: flex;
  gap: 6px;
  overflow-x: auto;
  padding: 8px 0 4px;
  scrollbar-width: thin;
}
.nav-link {
  flex: 0 0 auto;
  padding: 6px 11px;
  border-radius: 999px;
  font-size: 0.82rem;
  font-weight: 600;
  color: #e2e4e9;
  text-decoration: none;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.12);
}
.nav-link:hover { background: rgba(255, 255, 255, 0.18); color: #fff; }
.nav-link.active {
  background: var(--accent);
  color: #fff;
  border-color: #ff9aa0;
}
main {
  max-width: 1220px;
  margin: 0 auto;
  padding: 20px 16px 56px;
}
.hero {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px;
  box-shadow: var(--shadow);
  margin-bottom: 20px;
}
.eyebrow {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--accent);
  background: var(--accent-soft);
  padding: 3px 9px;
  border-radius: 999px;
  margin-bottom: 8px;
}
h1 { font-size: clamp(1.45rem, 3.2vw, 2.05rem); margin: 4px 0 10px; line-height: 1.22; }
h2 { font-size: clamp(1.2rem, 2.4vw, 1.5rem); margin: 28px 0 10px; line-height: 1.28; }
h3 { font-size: 1.05rem; margin: 0 0 6px; line-height: 1.3; }
p { margin: 0 0 12px; }
.lead { font-size: 1rem; color: var(--muted); max-width: 85ch; }
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
  gap: 12px;
  margin: 16px 0;
}
.kpi {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 14px 16px;
  box-shadow: var(--shadow);
}
.kpi-label { font-size: 0.78rem; color: var(--muted); font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; }
.kpi-val { font-size: 1.35rem; font-weight: 800; margin: 4px 0; color: var(--ink); }
.kpi-sub { font-size: 0.82rem; color: var(--muted); }
.callout {
  border-left: 4px solid var(--accent);
  background: var(--accent-soft);
  padding: 13px 16px;
  border-radius: 8px;
  margin: 14px 0;
  font-size: 0.92rem;
}
.callout.green { border-left-color: var(--green); background: var(--green-bg); }
.callout.gold { border-left-color: var(--gold); background: var(--gold-bg); }
.callout.blue { border-left-color: var(--blue); background: var(--blue-bg); }
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 14px;
  margin-top: 14px;
}
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 16px;
  box-shadow: var(--shadow);
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.card.closed-card {
  opacity: 0.82;
  border-style: dashed;
  background: #fafafa;
}
.badge-row { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }
.badge {
  display: inline-block;
  font-size: 0.73rem;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 999px;
  background: var(--surface-alt);
  color: var(--ink);
}
.badge.star { background: #2b1215; color: #ffd86b; }
.badge.bib { background: var(--accent); color: #fff; }
.badge.rec { background: var(--blue-bg); color: var(--blue); }
.badge.exact { background: var(--green-bg); color: var(--green); }
.badge.est { background: var(--gold-bg); color: var(--gold); }
.badge.blank { background: var(--surface-alt); color: var(--muted); }
.badge.high { background: #fde8e8; color: #9b1c1c; }
.badge.medium { background: var(--warn-bg); color: var(--warn); }
.badge.low { background: var(--blue-bg); color: var(--blue); }
.table-wrap {
  overflow-x: auto;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  margin: 14px 0;
}
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.86rem;
  min-width: 720px;
}
th, td {
  padding: 10px 12px;
  text-align: left;
  border-bottom: 1px solid var(--border);
  vertical-align: top;
}
th {
  background: var(--surface-alt);
  font-weight: 700;
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  color: var(--ink);
}
tr:last-child td { border-bottom: none; }
.blank-cell {
  color: var(--muted);
  font-style: italic;
}
.controls {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
  margin: 12px 0;
}
.btn-chip, select {
  font: inherit;
  font-size: 0.84rem;
  padding: 7px 12px;
  border-radius: 999px;
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--ink);
  cursor: pointer;
}
.btn-chip.active {
  background: var(--ink);
  color: #fff;
  border-color: var(--ink);
}
.meta-list {
  margin: 0;
  padding: 0;
  list-style: none;
  font-size: 0.85rem;
  display: grid;
  gap: 4px;
}
.meta-list strong { color: var(--ink); }
.link-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: auto;
  padding-top: 6px;
}
.pill-link {
  font-size: 0.77rem;
  font-weight: 600;
  padding: 4px 9px;
  border-radius: 6px;
  background: var(--surface-alt);
  color: var(--blue);
  text-decoration: none;
  border: 1px solid var(--border);
}
.pill-link:hover { background: var(--blue-bg); }
.calc-box {
  background: var(--surface);
  border: 2px solid var(--ink);
  border-radius: var(--radius);
  padding: 18px;
  margin: 18px 0;
}
.calc-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 16px;
}
.check-item {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  font-size: 0.85rem;
  margin-bottom: 6px;
}
.site-footer {
  max-width: 1220px;
  margin: 0 auto;
  padding: 20px 16px 40px;
  border-top: 1px solid var(--border);
  font-size: 0.82rem;
  color: var(--muted);
}
@media (max-width: 640px) {
  .hero { padding: 15px; }
  .card-grid { grid-template-columns: 1fr; }
  th, td { padding: 8px 9px; font-size: 0.81rem; }
}
"""


def page_shell(active_file: str, title: str, body_html: str, extra_js: str = "") -> str:
    nav_links = []
    for href, label in NAV_ITEMS:
        cls = "nav-link active" if href == active_file else "nav-link"
        aria = ' aria-current="page"' if href == active_file else ""
        nav_links.append(f'<a class="{cls}" href="{href}"{aria}>{esc(label)}</a>')
    nav_str = "\n        ".join(nav_links)
    js_block = f"<script>\n{extra_js}\n</script>" if extra_js else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)} — Las Vegas Feb–Mar 2027 Official-Source Guide</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to main content</a>
  <header class="site-header">
    <div class="header-inner">
      <div class="brand-row">
        <a class="brand-title" href="index.html">Las Vegas 2027: Official-Source Couple Trip Verification</a>
        <span class="brand-meta">Verified 2026-11-27 · 2 Adults · Feb 15 – Mar 23, 2027 · <a href="../../index.html">Canonical Repo Root ↗</a></span>
      </div>
      <nav class="nav-scroller" aria-label="Primary sections">
        {nav_str}
      </nav>
    </div>
  </header>
  <main id="main-content">
{body_html}
  </main>
  <footer class="site-footer">
    <p><strong>Strict Evidence &amp; Zero-Fabrication Policy:</strong> Every hotel price on this subsite comes directly from a first-party property booking engine captured on <code>2026-11-27</code> for a named Queen-or-larger room with a private bathroom. Every restaurant price comes from an official venue menu, resort menu PDF, or official OpenTable/Resy booking page. All unverified prices, conflicting hours, and bot-blocked engines are left blank and listed on <a href="flagged.html">Flagged for Review</a>.</p>
    <p>Task T20 (<code>arena/6851cc7e-vegas1</code>) · Source JSONs: <code>data/session-6851cc7e-*.json</code> · Audit notes: <code>notes/repo-audit-6851cc7e.md</code>.</p>
  </footer>
  {js_block}
</body>
</html>
"""


def build_index(hotels: dict, michelin: dict, act_tr: dict, audit_qa: dict) -> str:
    body = """
    <section class="hero">
      <span class="eyebrow">Executive Summary · Verified 2026-11-27</span>
      <h1>1–2 Week Las Vegas MICHELIN &amp; Transit Plan for Two Adults (Feb 15 – Mar 23, 2027)</h1>
      <p class="lead">Every figure below was verified directly against official resort booking engines, the 2026 MICHELIN Guide Southwest selection (24 Las Vegas venues), official venue menus, RTC Southern Nevada, and Las Vegas Monorail on <strong>November 27, 2026</strong>. Where an official source omits a price or prints conflicting hours, the cell is left strictly blank and logged on <a href="flagged.html">Flagged for Review</a>.</p>
      <div class="callout gold">
        <strong>BOOKING WINDOW ALERT (Nov 27 – Dec 4, 2026):</strong> Today is Cyber Week — official resort engines are running steep limited-time offers right now:
        <strong>Fontainebleau Bleau Friday (<code>FRBF26</code>)</strong> waives all resort fees + adds a <strong>$350 dining credit</strong> if booked by <strong>Dec 2, 2026</strong>;
        <strong>Wynn &amp; Encore Cyber Exclusive</strong> saves up to 20% + adds a <strong>$300 resort credit</strong> if booked by <strong>Dec 4, 2026</strong> (72h free cancel);
        <strong>Caesars Cyber Monday Early Access</strong> locks in Feb 15–22 rates with <strong>$0 due today and 48h free cancellation</strong>.
      </div>
    </section>

    <div class="kpi-grid">
      <div class="kpi">
        <div class="kpi-label">Official-IBE Hotels Priced</div>
        <div class="kpi-val">15 Resorts × 2 Weeks</div>
        <div class="kpi-sub">Queen+/King + private bath verified; 18 JS/bot-blocked resorts left blank (never OTA)</div>
      </div>
      <div class="kpi">
        <div class="kpi-label">Best Stay Window (Center Strip)</div>
        <div class="kpi-val">Feb 15–22, 2027</div>
        <div class="kpi-sub">3%–28.5% cheaper on all 8 Caesars hotels + Encore &amp; matches preferred Feb 15–18 PTO!</div>
      </div>
      <div class="kpi">
        <div class="kpi-label">Best Stay Window (North Strip)</div>
        <div class="kpi-val">Mar 14–21, 2027</div>
        <div class="kpi-sub">4%–18.8% cheaper at Fontainebleau, Resorts World &amp; Wynn (Feb 16–17 convention spike)</div>
      </div>
      <div class="kpi">
        <div class="kpi-label">2026 MICHELIN Las Vegas</div>
        <div class="kpi-val">4 Starred · 3 Bib · 17 Rec</div>
        <div class="kpi-sub">11/24 official couple prices verified; 13 blank; 1 closed (Michael Mina) excluded</div>
      </div>
    </div>

    <h2>1. Solving the Cheapest-Week Mystery (Feb 15–22 vs Mar 14–21, 2027)</h2>
    <div class="callout green">
      <strong>Key Discovery Across 15 Official First-Party Booking Engines:</strong> Las Vegas does <em>not</em> move as a single price curve between mid-February and mid-March 2027 — it splits cleanly by corridor:
      <ul>
        <li><strong>Center Strip &amp; Downtown (All 8 Caesars Resorts + Downtown Grand + Encore):</strong> <strong>Feb 15–22, 2027 is 3%–28.5% cheaper</strong> than Mar 14–21 because NCAA March Madness First Weekend (Mar 18–21, 2027) surges sportsbook hotels (e.g., <strong>Caesars Palace Julius Deluxe King is $1,407 pre-tax / $1,595.26 all-in in Feb 15–22 vs $1,967 pre-tax / $2,230.18 all-in in Mar 14–21</strong> — saving <strong>$634.92</strong> in your preferred mid-February window!).</li>
        <li><strong>North Strip Convention Corridor (Fontainebleau, Hilton/Conrad/Crockfords at Resorts World, and Wynn Tower):</strong> <strong>Mar 14–21, 2027 is 4%–18.8% cheaper</strong> than Feb 15–22 because an LVCC convention spike on Tue–Wed Feb 16–17 sells out Conrad completely and lifts North-Strip rates (e.g., <strong>Fontainebleau Free-Member Bleau King is $2,186.03 pre-tax / $2,478.52 all-in in Mar 14–21 vs $2,691.01 pre-tax / $3,051.07 all-in in Feb 15–22</strong>).</li>
      </ul>
    </div>

    <h2>2. Top 4 Official-Source Hotel + MICHELIN Recommendations (7 Nights, 2 Adults)</h2>
    <div class="card-grid">
      <article class="card">
        <div class="badge-row"><span class="badge star">#1 Overall Pick</span><span class="badge exact">Feb 15–22 Best</span></div>
        <h3>Caesars Palace — Julius Deluxe 1 King</h3>
        <p><strong>$1,407.00 pre-tax ($201/nt incl. $55 resort fee) · $1,595.26 est. w/ 13.38% tax</strong> (Feb 15–22, 2027).</p>
        <p>Only priced 5-star Strip resort with a <strong>MICHELIN-Starred restaurant in the building</strong> (1★ Restaurant Guy Savoy), walkable to Cosmopolitan (1★ é, Bib China Poblano) &amp; Venetian (4 Recommended), with RTC Deuce at the gate and Route 203 to Chinatown 1 block north.</p>
        <div class="link-pills"><a class="pill-link" href="hotels.html">Compare All 15 Hotels →</a><a class="pill-link" href="costs.html">See $3,496 Full Trip Package →</a></div>
      </article>
      <article class="card">
        <div class="badge-row"><span class="badge exact">#1 Mid-Strip Value</span><span class="badge exact">Clean IBE Render</span></div>
        <h3>Planet Hollywood (Ultra Hip 1K) or Horseshoe (Resort 1K)</h3>
        <p><strong>Planet Hollywood: $875.00 pre-tax ($992.08 w/ tax)</strong> · <strong>Horseshoe: $826.00 pre-tax ($936.52 w/ tax)</strong> (Feb 15–22).</p>
        <p>430–450 sq ft King rooms with private baths. Planet Hollywood bridges directly into Cosmopolitan (1★ é &amp; China Poblano); Horseshoe has an on-site Monorail station 1 stop (~4 min) from MGM Grand's 2★ Joël Robuchon &amp; 1★ L'Atelier.</p>
        <div class="link-pills"><a class="pill-link" href="hotels.html">Hotel Details →</a><a class="pill-link" href="costs.html">See $2,543 Full Trip Package →</a></div>
      </article>
      <article class="card">
        <div class="badge-row"><span class="badge rec">#1 Budget Strip</span><span class="badge exact">$87/nt All-In</span></div>
        <h3>The LINQ ($611.12 w/ tax) or Flamingo ($706.36 w/ tax)</h3>
        <p><strong>LINQ Deluxe 2 Queens: $539.00 pre-tax ($77/nt incl. $50 fee)</strong> · <strong>Flamingo 2 Queens: $623.00 pre-tax ($89/nt)</strong> (Feb 15–22).</p>
        <p>Cheapest verified Queen+ rooms with private baths on the Strip — both have on-site Las Vegas Monorail stations, Center-Strip RTC Deuce stops, and easy walking access to Spring Mountain Rd (RTC Route 203 to Chinatown).</p>
        <div class="link-pills"><a class="pill-link" href="hotels.html">Room &amp; Fee Breakdown →</a><a class="pill-link" href="costs.html">See $1,614 Full Trip Package →</a></div>
      </article>
      <article class="card">
        <div class="badge-row"><span class="badge gold">1 MICHELIN Key</span><span class="badge high">Book by Dec 2</span></div>
        <h3>Fontainebleau Las Vegas — Bleau King (Free Member <code>FRBF26</code>)</h3>
        <p><strong>Mar 14–21: $2,186.03 pre-tax ($2,478.52 w/ tax)</strong> · <strong>Feb 15–22: $2,691.01 pre-tax ($3,051.07 w/ tax)</strong>.</p>
        <p>Las Vegas's only MICHELIN Key resort &amp; casino. Free Fontainebleau Rewards sign-up before <strong>Dec 2, 2026</strong> waives ~$436 in resort fees and includes a <strong>$350 dining credit</strong>.</p>
        <div class="link-pills"><a class="pill-link" href="hotels.html">View Promo Details →</a></div>
      </article>
    </div>

    <h2>3. Repository Audit Highlights (14 Concrete Findings on <code>main@99a3506</code>)</h2>
    <p>Before building this dashboard, we audited every script, JSON file, and HTML page on <code>main@99a3506</code> line by line against primary sources:</p>
    <ul>
      <li><strong><code>RA-01</code> (High):</strong> Live <code>dining.html:72</code> calls <em>Wing Lei</em> "the cheapest starred dinner on this site", violating <code>F-03</code> (Wing Lei is Recommended / unstarred in 2026).</li>
      <li><strong><code>RA-02</code> (High):</strong> Orphan <code>costs.html</code> / <code>docs/costs.html</code> was left deployed with the broken <code>$6.00</code> 9-day RTC pass math (<code>$120.00</code> actual) and withdrawn Booking.com hotel totals.</li>
      <li><strong><code>RA-05</code> (High):</strong> Four restaurants with official published menu prices were still blank in <code>data/restaurants.json</code> — we verified and added all four: <strong>Stubborn Seed ($320.00)</strong>, <strong>Kabuto ($260.00 / $370.00)</strong>, <strong>China Poblano ($120.00)</strong>, and <strong>SoulBelly BBQ ($80.00)</strong>.</li>
      <li><strong><code>RA-06..RA-12</code>:</strong> Fixed L'Atelier's misattributed Service Award / phone / "6 and under" policy, China Poblano's 10:00 PM Sunday close, Milos's 11:00 PM Fri–Sat close, Bouchon's South Tower name, Neon Museum &amp; Fremont Street's contradictory YouTube caveats, RTC's $2 regular local fare, and Vegas Loop's 14 active stations.</li>
    </ul>
    <p><a href="repo-review.html"><strong>Read the full 14-item Line-by-Line Repo Audit →</strong></a></p>
    """
    return page_shell("index.html", "Executive Summary", body)


def build_hotels(hotels: dict) -> str:
    rows_html = []
    cards_html = []
    for h in hotels["verified_hotels"]:
        feb_pre = h["feb_15_22"]["total_7n_incl_fee_pretax"]
        feb_tax = h["feb_15_22"]["total_7n_all_in_est"]
        mar_pre = h["mar_14_21"]["total_7n_incl_fee_pretax"]
        mar_tax = h["mar_14_21"]["total_7n_all_in_est"]
        feb_sort = feb_tax if feb_tax is not None else 999999
        mar_sort = mar_tax if mar_tax is not None else 999999

        feb_cell = (
            f"<strong>{money(feb_tax)}</strong><br><small>{money(feb_pre)} pre-tax (${h['feb_15_22']['nightly_incl_fee_pretax']:,.2f}/nt)</small>"
            if feb_tax is not None
            else f'{money(None)}<br><small>{esc(h["feb_15_22"]["rate_name"])}</small>'
        )
        mar_cell = (
            f"<strong>{money(mar_tax)}</strong><br><small>{money(mar_pre)} pre-tax (${h['mar_14_21']['nightly_incl_fee_pretax']:,.2f}/nt)</small>"
            if mar_tax is not None
            else f'{money(None)}<br><small>{esc(h["mar_14_21"]["rate_name"])}</small>'
        )

        rows_html.append(f"""
        <tr data-zone="{esc(h['zone'])}" data-overall="{h['rank_overall']}" data-feb="{feb_sort}" data-mar="{mar_sort}" data-mich="{h['michelin_35m_est']}">
          <td><strong>#{h['rank_overall']}</strong> <small>(Val #{h['rank_value']})</small></td>
          <td>
            <strong><a href="{esc(h['official_url'])}" target="_blank" rel="noopener">{esc(h['name'])}</a></strong><br>
            <small>{esc(h['room_name'])} ({h['room_sqft']} sq ft)</small>
          </td>
          <td><span class="badge exact">✓ {esc(h['bed'])}</span><br><small>✓ {esc(h['bath_detail'])}</small></td>
          <td>{feb_cell}</td>
          <td>{mar_cell}</td>
          <td><small>{esc(h['resort_fee_display'])}</small></td>
          <td><strong>{esc(h['cheapest_window'])}</strong><br><small>{esc(h['booking_promo'])}</small></td>
          <td>
            <strong>{h['michelin_in_complex']}</strong> in-complex · <strong>{h['michelin_walk_15m']}</strong> walk · <strong>{h['michelin_35m_est']}</strong> ≤35m est.<br>
            <small>{esc(h['transit_access'])}</small>
          </td>
          <td>
            <a class="pill-link" href="{esc(h['official_ibe_feb_url'])}" target="_blank" rel="noopener">Feb IBE ↗</a>
            <a class="pill-link" href="{esc(h['official_ibe_mar_url'])}" target="_blank" rel="noopener">Mar IBE ↗</a>
          </td>
        </tr>""")

    unpriced_rows = []
    for u in hotels["unpriced_official_candidates"]:
        unpriced_rows.append(f"""
        <tr>
          <td><strong><a href="{esc(u['official_url'])}" target="_blank" rel="noopener">{esc(u['name'])}</a></strong></td>
          <td>{esc(u['zone'])}</td>
          <td>{esc(u['room_verified'])}</td>
          <td><span class="blank-cell">— (Blank)</span></td>
          <td><span class="blank-cell">— (Blank)</span></td>
          <td>{esc(u['why_price_blank'])}</td>
        </tr>""")

    js = """
    (function() {
      const tbody = document.getElementById('verified-hotels-tbody');
      const zoneSel = document.getElementById('zone-filter');
      const sortSel = document.getElementById('sort-select');
      function update() {
        const z = zoneSel.value;
        const s = sortSel.value;
        const rows = Array.from(tbody.querySelectorAll('tr'));
        rows.forEach(r => {
          r.style.display = (z === 'all' || r.dataset.zone === z) ? '' : 'none';
        });
        rows.sort((a, b) => {
          if (s === 'overall') return Number(a.dataset.overall) - Number(b.dataset.overall);
          if (s === 'feb') return Number(a.dataset.feb) - Number(b.dataset.feb);
          if (s === 'mar') return Number(a.dataset.mar) - Number(b.dataset.mar);
          if (s === 'mich') return Number(b.dataset.mich) - Number(a.dataset.mich) || Number(a.dataset.feb) - Number(b.dataset.feb);
          return 0;
        });
        rows.forEach(r => tbody.appendChild(r));
      }
      zoneSel.addEventListener('change', update);
      sortSel.addEventListener('change', update);
      update();
    })();
    """

    body = f"""
    <section class="hero">
      <span class="eyebrow">Official First-Party Booking Engines Only · Captured 2026-11-27</span>
      <h1>Ranked Las Vegas Hotels (Queen+ Bed &amp; Private Bathroom Verified)</h1>
      <p class="lead">{esc(hotels['meta']['room_rule'])} {esc(hotels['meta']['transit_rule'])}</p>
      <div class="callout blue">
        <strong>Tax &amp; Resort Fee Transparency:</strong> Every cell shows <strong>both</strong> the <strong>all-in 7-night total incl. resort fees + 13.38% Clark County lodging tax</strong> and the <strong>pre-tax 7-night total incl. resort fee</strong> directly from the property's official booking engine. Zero OTA (Booking.com / Expedia) rates are used anywhere on this page.
      </div>
    </section>

    <div class="controls" aria-label="Filter and sort hotels">
      <label>Zone:
        <select id="zone-filter">
          <option value="all">All Zones (15 Priced)</option>
          <option value="center-strip">Center Strip (8)</option>
          <option value="north-strip">North Strip (6)</option>
          <option value="downtown-arts">Downtown (1)</option>
        </select>
      </label>
      <label>Sort by:
        <select id="sort-select">
          <option value="overall">Overall Rank (MICHELIN Reach + Value)</option>
          <option value="feb">Cheapest Feb 15–22, 2027 (7 Nights)</option>
          <option value="mar">Cheapest Mar 14–21, 2027 (7 Nights)</option>
          <option value="mich">Most MICHELIN Venues ≤35m Public Transit</option>
        </select>
      </label>
    </div>

    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Rank</th>
            <th>Hotel &amp; Verified Qualifying Room</th>
            <th>Bed &amp; Private Bath</th>
            <th>Feb 15–22, 2027 (7n, 2 Adults)</th>
            <th>Mar 14–21, 2027 (7n, 2 Adults)</th>
            <th>Resort Fee</th>
            <th>Cheapest Window &amp; Booking Deadline</th>
            <th>MICHELIN Proximity &amp; Public Transit</th>
            <th>Official Engine</th>
          </tr>
        </thead>
        <tbody id="verified-hotels-tbody">
          {''.join(rows_html)}
        </tbody>
      </table>
    </div>

    <h2>Unpriced Candidate Resorts (18 Official Pages Checked — Left Blank Rather Than Using OTAs)</h2>
    <p>MGM Resorts blocks automated server requests, Venetian/Palazzo renders <code>$XXX</code> client-side placeholders without browser JS execution, and several Downtown/North-Strip engines require interactive JS calendar pagination to reach Feb–Mar 2027. Per our zero-fabrication rule, their 7-night quotes are left blank with direct official links so you can compare in a live browser:</p>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Resort</th>
            <th>Zone</th>
            <th>Verified Room / Property Facts</th>
            <th>Feb 15–22</th>
            <th>Mar 14–21</th>
            <th>Why Official 7-Night Quote Is Left Blank</th>
          </tr>
        </thead>
        <tbody>
          {''.join(unpriced_rows)}
        </tbody>
      </table>
    </div>
    """
    return page_shell("hotels.html", "Ranked Hotels (15 Official IBEs)", body, js)


def build_costs(hotels: dict, michelin: dict, act_tr: dict) -> str:
    pkg_rows = []
    for p in act_tr["combined_packages"]:
        est_badge = '<span class="badge est">Includes Dish-Menu Est.</span>' if p["michelin_includes_estimate"] else '<span class="badge exact">100% Exact Published Prices</span>'
        pkg_rows.append(f"""
        <tr>
          <td>
            <span class="badge star">{esc(p['badge'])}</span><br>
            <strong>{esc(p['title'])}</strong><br>
            <small>{esc(p['hotel_name'])} — {esc(p['room_name'])}</small>
          </td>
          <td><strong>Feb:</strong> {money(p['hotel_7n_feb_all_in'])}<br><strong>Mar:</strong> {money(p['hotel_7n_mar_all_in'])}</td>
          <td><strong>{money(p['michelin_pretax_total'])}</strong> {est_badge}<br><small>{esc(p['michelin_plan_label'])}</small></td>
          <td>{money(p['activities_4_paid_plus_2_free'])}<br><small>Mob + Neon + High Roller Day + 2 Free</small></td>
          <td>{money(p['public_transit_7d_2adults'])}</td>
          <td><strong>{money(p['combined_feb_15_22'])}</strong></td>
          <td><strong>{money(p['combined_mar_14_21'])}</strong></td>
          <td><strong>{esc(p['cheaper_window_savings'])}</strong><br><small>{esc(p['credit_or_caveat_note'])}</small></td>
        </tr>""")

    hotel_opts = []
    for h in hotels["verified_hotels"]:
        feb_v = h["feb_15_22"]["total_7n_all_in_est"]
        mar_v = h["mar_14_21"]["total_7n_all_in_est"]
        hotel_opts.append(
            f'<option value="{esc(h["id"])}" data-feb="{feb_v if feb_v is not None else ""}" data-mar="{mar_v if mar_v is not None else ""}">'
            f'{esc(h["name"])} — {esc(h["room_name"])} (Feb: {f"${feb_v:,.2f}" if feb_v else "N/A"} | Mar: {f"${mar_v:,.2f}" if mar_v else "N/A"})</option>'
        )

    dining_checks = [
        ("guy-savoy", "1★ Restaurant Guy Savoy (~$520.00 min dish est., pre-tax)", 520.00, True, False),
        ("wing-lei", "Recommended: Wing Lei Peking Duck Tasting ($397.76 exact)", 397.76, False, True),
        ("stubborn-seed", "Recommended: Stubborn Seed Tasting Menu ($320.00 exact)", 320.00, False, True),
        ("partage-7", "Recommended: Partage 7-Course Tasting ($320.00 exact; 5-course is $260)", 320.00, False, False),
        ("kabuto", "Recommended: Kabuto Yoroi Omakase ($260.00 exact; Kabuto Course $370)", 260.00, False, True),
        ("anima-by-edo", "Recommended: Anima by EDO Tasting ($170.00 exact)", 170.00, False, False),
        ("anima-mon", "Recommended: Anima by EDO Monday Pasta + Bottle of Wine ($65.00 exact couple)", 65.00, False, False),
        ("esthers-kitchen", "Bib Gourmand: Esther's Kitchen (~$145.00 mid dish est.)", 145.00, True, False),
        ("china-poblano", "Bib Gourmand: China Poblano José's Way Tasting ($120.00 exact)", 120.00, False, True),
        ("soulbelly-bbq", "Recommended: SoulBelly BBQ Chef's Choice for 2 ($80.00 exact)", 80.00, False, True),
    ]
    d_html = []
    for did, label, amt, is_est, checked in dining_checks:
        ck = " checked" if checked else ""
        d_html.append(
            f'<label class="check-item"><input type="checkbox" class="calc-dining" data-amt="{amt}" data-est="{1 if is_est else 0}"{ck}> '
            f'<span>{esc(label)}</span></label>'
        )
    d_html.append('<div class="check-item" style="opacity:0.6;"><input type="checkbox" disabled> <span>Michael Mina ($590++ — Disabled: Temporarily Closed on official Bellagio page)</span></div>')

    js = """
    (function() {
      const hSel = document.getElementById('calc-hotel');
      const wSel = document.getElementById('calc-window');
      const tSel = document.getElementById('calc-transit');
      const dBoxes = Array.from(document.querySelectorAll('.calc-dining'));
      const aBoxes = Array.from(document.querySelectorAll('.calc-act'));
      const outEl = document.getElementById('calc-output');

      function recalc() {
        const opt = hSel.options[hSel.selectedIndex];
        const w = wSel.value;
        const rawH = opt.dataset[w];
        if (!rawH) {
          outEl.innerHTML = '<strong>Selected hotel/window is unavailable or unverified on official booking engine (see Flagged for Review). Pick the alternate month or another hotel.</strong>';
          return;
        }
        const hAmt = parseFloat(rawH);
        let dAmt = 0;
        let hasEst = false;
        dBoxes.forEach(b => {
          if (b.checked) {
            dAmt += parseFloat(b.dataset.amt);
            if (b.dataset.est === '1') hasEst = true;
          }
        });
        let aAmt = 0;
        aBoxes.forEach(b => { if (b.checked) aAmt += parseFloat(b.dataset.amt); });
        const tAmt = parseFloat(tSel.value);
        const total = hAmt + dAmt + aAmt + tAmt;
        outEl.innerHTML =
          '<div style="font-size:1.35rem;font-weight:800;">Combined Verified 2-Adult Total: $' + total.toLocaleString('en-US', {minimumFractionDigits:2, maximumFractionDigits:2}) + '</div>' +
          '<div style="font-size:0.86rem;color:#525866;margin-top:4px;">' +
          'Hotel (7n incl. resort fee &amp; 13.38% tax): <strong>$' + hAmt.toFixed(2) + '</strong> · ' +
          'MICHELIN Dining (pre-tax/tip): <strong>$' + dAmt.toFixed(2) + (hasEst ? ' (incl. dish-level est.)' : ' (exact menus)') + '</strong> · ' +
          'Activities: <strong>$' + aAmt.toFixed(2) + '</strong> · ' +
          'Public Transit: <strong>$' + tAmt.toFixed(2) + '</strong>' +
          '</div>';
      }
      [hSel, wSel, tSel, ...dBoxes, ...aBoxes].forEach(el => el.addEventListener('change', recalc));
      recalc();
    })();
    """

    body = f"""
    <section class="hero">
      <span class="eyebrow">Combined Couple Trip Budgets · 2 Adults · 7 Nights</span>
      <h1>Combined Hotel + MICHELIN Dining + Activities + Public Transit Costs</h1>
      <p class="lead">Every package below combines an <strong>official first-party 7-night hotel quote (including resort fees &amp; 13.38% lodging tax)</strong> with <strong>official published MICHELIN couple menu prices</strong>, <strong>official activity admissions</strong>, and <strong>official RTC / Monorail fares</strong>. Flights, 8.375% restaurant sales tax, 18%–20% dining gratuity, beverages, and the 13 unpriced MICHELIN venues are excluded rather than guessed.</p>
    </section>

    <h2>1. Five Worked 7-Night Couple Packages (Feb 15–22 vs Mar 14–21, 2027)</h2>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Tier &amp; Official-IBE Hotel</th>
            <th>Hotel 7n All-In (w/ Fee &amp; 13.38% Tax)</th>
            <th>Verified MICHELIN Dining Plan (2 Adults, Pre-Tax)</th>
            <th>Activities (2 Adults)</th>
            <th>7-Day Public Transit</th>
            <th>Combined Feb 15–22</th>
            <th>Combined Mar 14–21</th>
            <th>Window Delta &amp; Notes</th>
          </tr>
        </thead>
        <tbody>
          {''.join(pkg_rows)}
        </tbody>
      </table>
    </div>

    <h2>2. Interactive Official-Source Couple Budget Builder</h2>
    <div class="calc-box">
      <div class="calc-grid">
        <div>
          <h3>Step 1: Hotel &amp; Stay Window</h3>
          <p><label>Official-IBE Hotel:<br>
            <select id="calc-hotel" style="width:100%;max-width:100%;border-radius:8px;margin-top:4px;">
              {''.join(hotel_opts)}
            </select>
          </label></p>
          <p><label>7-Night Stay Window:<br>
            <select id="calc-window" style="width:100%;border-radius:8px;margin-top:4px;">
              <option value="feb">Feb 15–22, 2027 (Preferred Mid-Feb Window)</option>
              <option value="mar">Mar 14–21, 2027 (Mid-March Window)</option>
            </select>
          </label></p>
          <p><label>7-Day Public Transit Bundle (2 Adults):<br>
            <select id="calc-transit" style="width:100%;border-radius:8px;margin-top:4px;">
              <option value="118.00">RTC 7d Coverage ($96) + 2 Monorail Round-Trips ($22) = $118.00</option>
              <option value="215.90">RTC 7d Coverage ($96) + 2× 7-Day Unlimited Monorail ($119.90) = $215.90</option>
              <option value="96.00">RTC Strip &amp; All-Access Only (2× 3-Day + 1× 24-Hr each) = $96.00</option>
            </select>
          </label></p>
        </div>
        <div>
          <h3>Step 2: Official-Menu MICHELIN Meals (2 Adults)</h3>
          {''.join(d_html)}
        </div>
        <div>
          <h3>Step 3: Verified Activities ≤1h Transit (2 Adults)</h3>
          <label class="check-item"><input type="checkbox" class="calc-act" data-amt="0" checked> <span>Fountains of Bellagio ($0.00 Free)</span></label>
          <label class="check-item"><input type="checkbox" class="calc-act" data-amt="0" checked> <span>Fremont Street Viva Vision Canopy ($0.00 Free)</span></label>
          <label class="check-item"><input type="checkbox" class="calc-act" data-amt="42.00" checked> <span>The Neon Museum General Admission ($42.00+ couple)</span></label>
          <label class="check-item"><input type="checkbox" class="calc-act" data-amt="47.00" checked> <span>High Roller Daytime ($47.00 couple before fees)</span></label>
          <label class="check-item"><input type="checkbox" class="calc-act" data-amt="75.90" checked> <span>The Mob Museum General Admission ($75.90 couple)</span></label>
          <div class="check-item" style="opacity:0.65;"><input type="checkbox" disabled> <span>Sphere Las Vegas (Blank — dynamic per-show pricing)</span></div>
        </div>
      </div>
      <hr style="border:none;border-top:1px solid var(--border);margin:14px 0;">
      <div id="calc-output" aria-live="polite"></div>
    </div>
    """
    return page_shell("costs.html", "Combined Costs & Calculator", body, js)


def render_restaurant_card(r: dict) -> str:
    if r["distinction"] in ("2-star", "1-star"):
        b_cls = "star"
    elif r["distinction"] == "bib-gourmand":
        b_cls = "bib"
    else:
        b_cls = "rec"

    if r["price_basis"] in ("exact_tasting", "exact_package"):
        p_badge = f'<span class="badge exact">{esc(r["price_2_adults_pretax"])}</span>'
    elif r["price_basis"] == "dish_estimate":
        p_badge = f'<span class="badge est">{esc(r["price_2_adults_pretax"])}</span>'
    else:
        p_badge = '<span class="badge blank">Price Unpublished (Blank)</span>'

    closed_cls = " closed-card" if r["status"] == "temporarily_closed" else ""
    days_disp = esc(r["days"]) if r["days"] else '<span class="blank-cell">— (Blank on official page)</span>'
    hrs_disp = esc(r["hours"]) if r["hours"] else '<span class="blank-cell">— (Blank on official page)</span>'
    phone_disp = esc(r["phone"]) if r["phone"] else '<span class="blank-cell">—</span>'

    links = [
        f'<a class="pill-link" href="{esc(r["official_url"])}" target="_blank" rel="noopener">Official Page ↗</a>',
        f'<a class="pill-link" href="{esc(r["menu_source_url"])}" target="_blank" rel="noopener">Menu / Source ↗</a>',
    ]
    if r["instagram"]:
        links.append(f'<a class="pill-link" href="{esc(r["instagram"])}" target="_blank" rel="noopener">Instagram ↗</a>')
    if r["youtube"]:
        links.append(f'<a class="pill-link" href="{esc(r["youtube"][0])}" target="_blank" rel="noopener">YouTube ({len(r["youtube"])}) ↗</a>')
    if r["tiktok"]:
        links.append(f'<a class="pill-link" href="{esc(r["tiktok"])}" target="_blank" rel="noopener">TikTok ↗</a>')

    return f"""
    <article class="card mich-card{closed_cls}" data-cluster="{esc(r['cluster'])}" data-priced="{1 if r['price_2_adults_pretax'] else 0}">
      <div class="badge-row">
        <span class="badge {b_cls}">{esc(r['distinction_label'])}</span>
        {p_badge}
      </div>
      <h3>{esc(r['name'])}</h3>
      <ul class="meta-list">
        <li><strong>Cuisine &amp; Location:</strong> {esc(r['cuisine'])} · {esc(r['property_or_area'])}</li>
        <li><strong>Address &amp; Phone:</strong> {esc(r['address'])} · {phone_disp}</li>
        <li><strong>Days:</strong> {days_disp}</li>
        <li><strong>Hours:</strong> {hrs_disp}</li>
        <li><strong>2-Adult Pricing Note:</strong> {esc(r['price_detail'])}</li>
        <li><strong>Public Transit:</strong> {esc(r['nearest_public_transit'])} ({esc(r['est_transit_from_center_strip'])})</li>
        <li><strong>Policy / Audit Note:</strong> {esc(r['exceptions'])}</li>
      </ul>
      <div class="link-pills">{''.join(links)}</div>
    </article>"""


def build_michelin(michelin: dict) -> str:
    cluster_rows = []
    for c in michelin["clusters"]:
        cluster_rows.append(f"""
        <tr>
          <td><strong>{esc(c['name'])}</strong></td>
          <td>{c['venue_count']} total ({c['starred_count']} Starred)</td>
          <td>{esc(c['public_transit'])}</td>
        </tr>""")

    starred_cards = "".join(render_restaurant_card(r) for r in michelin["starred"])
    bib_cards = "".join(render_restaurant_card(r) for r in michelin["bib_gourmand"])
    rec_cards = "".join(render_restaurant_card(r) for r in michelin["recommended"])

    js = """
    (function() {
      const cSel = document.getElementById('cluster-filter');
      const pSel = document.getElementById('price-filter');
      const cards = Array.from(document.querySelectorAll('.mich-card'));
      function filter() {
        const c = cSel.value;
        const p = pSel.value;
        cards.forEach(card => {
          const okC = (c === 'all' || card.dataset.cluster === c);
          const okP = (p === 'all' || card.dataset.priced === '1');
          card.style.display = (okC && okP) ? '' : 'none';
        });
      }
      cSel.addEventListener('change', filter);
      pSel.addEventListener('change', filter);
    })();
    """

    body = f"""
    <section class="hero">
      <span class="eyebrow">2026 MICHELIN Guide Southwest · All 24 Las Vegas Selections</span>
      <h1>Las Vegas MICHELIN Restaurants — Starred vs Bib Gourmand vs Recommended</h1>
      <p class="lead">Strictly separated by official 2026 MICHELIN Guide Southwest distinction: <strong>4 MICHELIN-Starred restaurants</strong> (1 Two-Star, 3 One-Star), <strong>3 Bib Gourmand restaurants</strong>, and <strong>17 MICHELIN Recommended (Selected) restaurants</strong>. Unlike canonical <code>dining.html:72</code> (<code>RA-01</code>), <strong>Wing Lei is never counted as starred</strong>, and <strong>4 newly verified official couple prices</strong> (Stubborn Seed $320, Kabuto $260/$370, China Poblano $120, SoulBelly BBQ $80) bring verified menu pricing to <strong>11 of 24 venues</strong>.</p>
    </section>

    <h2>Transit &amp; Geographic Dining Clusters</h2>
    <div class="table-wrap">
      <table>
        <thead>
          <tr><th>Cluster</th><th>MICHELIN Count</th><th>Zero-Car Public Transit Access</th></tr>
        </thead>
        <tbody>{''.join(cluster_rows)}</tbody>
      </table>
    </div>

    <div class="controls">
      <label>Filter by Transit Cluster:
        <select id="cluster-filter">
          <option value="all">All 6 Clusters (24 Venues)</option>
          <option value="south-strip-mgm">South Strip — MGM Grand (2)</option>
          <option value="center-strip">Center Strip &amp; Flamingo Rd (6)</option>
          <option value="north-strip-venetian-wynn-rw">North Strip — Venetian / Wynn / RW (6)</option>
          <option value="chinatown-spring-mountain">Chinatown — Route 203 Spine (6)</option>
          <option value="arts-district-downtown">Downtown Arts District — Deuce (2)</option>
          <option value="west-off-strip">West / Southwest Off-Strip (2)</option>
        </select>
      </label>
      <label>Pricing Status:
        <select id="price-filter">
          <option value="all">Show All 24 Venues (11 Priced + 13 Blank)</option>
          <option value="1">Only Official-Menu Priced Venues (11)</option>
        </select>
      </label>
    </div>

    <h2>Section A — MICHELIN-Starred Restaurants (4 Total: 1× Two-Star, 3× One-Star)</h2>
    <div class="card-grid">{starred_cards}</div>

    <h2>Section B — MICHELIN Bib Gourmand Restaurants (3 Total)</h2>
    <div class="card-grid">{bib_cards}</div>

    <h2>Section C — MICHELIN Recommended / Selected Restaurants (17 Total — Unstarred)</h2>
    <div class="card-grid">{rec_cards}</div>
    """
    return page_shell("michelin.html", "MICHELIN Restaurants (24)", body, js)


def build_activities_transit(act_tr: dict) -> str:
    act_cards = []
    for a in act_tr["activities"]:
        p_disp = f'<span class="badge exact">{esc(a["price_2_adults"])}</span>' if a["price_2_adults"] else '<span class="badge blank">Dynamic Event Pricing (Blank)</span>'
        h_disp = esc(a["hours"]) if a["hours"] else '<span class="blank-cell">— (Blank: conflicting hours on official Caesars page; FL-04)</span>'
        links = [f'<a class="pill-link" href="{esc(a["official_url"])}" target="_blank" rel="noopener">Official Site ↗</a>']
        if a["instagram"]:
            links.append(f'<a class="pill-link" href="{esc(a["instagram"])}" target="_blank" rel="noopener">Instagram ↗</a>')
        if a["youtube"]:
            links.append(f'<a class="pill-link" href="{esc(a["youtube"][0])}" target="_blank" rel="noopener">YouTube ({len(a["youtube"])}) ↗</a>')
        if a["tiktok"]:
            links.append(f'<a class="pill-link" href="{esc(a["tiktok"])}" target="_blank" rel="noopener">TikTok ↗</a>')

        act_cards.append(f"""
        <article class="card">
          <div class="badge-row"><span class="badge rec">{esc(a['category'])}</span>{p_disp}</div>
          <h3>{esc(a['name'])}</h3>
          <ul class="meta-list">
            <li><strong>Zone:</strong> {esc(a['zone'])}</li>
            <li><strong>Days:</strong> {esc(a['days'])}</li>
            <li><strong>Hours:</strong> {h_disp}</li>
            <li><strong>Public Transit (≤1h):</strong> {esc(a['transit_from_center_strip'])}</li>
            <li><strong>Verification Note:</strong> {esc(a['notes'])}</li>
          </ul>
          <div class="link-pills">{''.join(links)}</div>
        </article>""")

    tr_rows = []
    for t in act_tr["transit_systems"]:
        tr_rows.append(f"""
        <tr>
          <td><strong><a href="{esc(t['official_url'])}" target="_blank" rel="noopener">{esc(t['name'])}</a></strong></td>
          <td>{esc(t['mode_type'])}</td>
          <td>{esc(t['corridors'])}</td>
          <td>{esc(t['fares_per_person'])}</td>
          <td><strong>{esc(t['fares_2_adults_7_nights'])}</strong></td>
          <td><small>{esc(t['audit_note'])}</small></td>
        </tr>""")

    body = f"""
    <section class="hero">
      <span class="eyebrow">≤1 Hour by Public Bus &amp; Monorail · Verified 2026-11-27</span>
      <h1>Top Las Vegas Activities &amp; Honest Public Transit Guide</h1>
      <p class="lead">All 6 featured attractions sit within ≤45 minutes of Center Strip via the 24-hour <strong>RTC Deuce</strong>, <strong>Las Vegas Monorail</strong>, or pedestrian walkways. Grand Canyon / Hoover Dam coach excursions exceed the 1-hour public-transit threshold and are excluded.</p>
      <div class="callout blue">
        <strong>Public Bus/Rail vs Vegas Loop Caveat:</strong> Las Vegas has no municipal subway or commuter train. Public transit consists of <strong>RTC Southern Nevada buses</strong> (24/7 Deuce + east-west Route 203 Chinatown &amp; Route 202 Flamingo) and the <strong>7-station Las Vegas Monorail</strong>. The <strong>14-station Vegas Loop</strong> is a point-to-point tunnel Tesla system documented below as an optional North-Strip supplement, never conflated with public bus/rail.
      </div>
    </section>

    <h2>1. Official Las Vegas Activities Reachable Within ≤1 Hour</h2>
    <div class="card-grid">{''.join(act_cards)}</div>

    <h2>2. Official Public Transit Fares &amp; Network Comparison (2 Adults)</h2>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>System</th>
            <th>Mode</th>
            <th>Verified Corridors &amp; Stations</th>
            <th>Official Per-Person Fares</th>
            <th>7-Night Couple Cost</th>
            <th>Audit &amp; Verification Note</th>
          </tr>
        </thead>
        <tbody>{''.join(tr_rows)}</tbody>
      </table>
    </div>
    """
    return page_shell("activities-transit.html", "Activities & Public Transit", body)


def build_qa_suggestions(audit_qa: dict) -> str:
    q_cards = []
    for q in audit_qa["questions"]:
        cls = "exact" if "Answered" in q["status"] or "Resolved" in q["status"] else "est"
        q_cards.append(f"""
        <article class="card">
          <div class="badge-row"><span class="badge">{esc(q['id'])}</span><span class="badge {cls}">{esc(q['status'])}</span></div>
          <h3>{esc(q['question'])}</h3>
          <p><strong>Current Answer:</strong> {esc(q['answer'])}</p>
          <p><strong>Step-by-Step Discovery Plan:</strong> {esc(q['discovery_steps'])}</p>
        </article>""")

    s_cards = []
    for s in audit_qa["suggestions"]:
        p_cls = "high" if s["priority"].startswith("P0") else ("est" if s["priority"].startswith("P1") else "rec")
        s_cards.append(f"""
        <article class="card">
          <div class="badge-row"><span class="badge {p_cls}">{esc(s['priority'])}</span><span class="badge">{esc(s['category'])}</span></div>
          <h3>{esc(s['id'])}: {esc(s['title'])}</h3>
          <p>{esc(s['detail'])}</p>
        </article>""")

    body = f"""
    <section class="hero">
      <span class="eyebrow">Open Questions, Discovery Playbook &amp; Ranked Suggestions</span>
      <h1>Answered Questions, Remaining Gaps &amp; High-Impact Trip Suggestions</h1>
      <p class="lead">Every answered question cites live official-source data from <code>2026-11-27</code>, and every open question includes concrete, zero-guesswork discovery steps.</p>
    </section>

    <h2>1. Ranked Actionable Suggestions (<code>S-01</code> – <code>S-08</code>)</h2>
    <div class="card-grid">{''.join(s_cards)}</div>

    <h2>2. Questions &amp; Discovery Playbooks (<code>Q-01</code> – <code>Q-08</code>)</h2>
    <div class="card-grid">{''.join(q_cards)}</div>
    """
    return page_shell("questions-suggestions.html", "Questions & Suggestions", body)


def build_repo_review(audit_qa: dict) -> str:
    rows = []
    for r in audit_qa["repo_audit"]:
        rows.append(f"""
        <tr>
          <td><strong>{esc(r['id'])}</strong><br><span class="badge {esc(r['severity'])}">{esc(r['severity']).upper()}</span></td>
          <td><code>{esc(r['file_ref'])}</code></td>
          <td><strong>{esc(r['title'])}</strong><br><small>{esc(r['current_state'])}</small></td>
          <td>{esc(r['verified_fact'])}</td>
          <td><a class="pill-link" href="{esc(r['source_url'])}" target="_blank" rel="noopener">Primary Source ↗</a></td>
        </tr>""")

    body = f"""
    <section class="hero">
      <span class="eyebrow">Line-by-Line Code &amp; Data Review of main@99a3506</span>
      <h1>Repository Review — 14 Verified Irregularities &amp; How This Build Resolves Them</h1>
      <p class="lead">Audited commit <code>99a3506</code> across all scripts, JSON files, flags, and generated HTML pages against ~115 primary-source fetches executed on <code>2026-11-27</code>. Full Markdown report saved in <code>notes/repo-audit-6851cc7e.md</code>.</p>
    </section>

    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>ID &amp; Severity</th>
            <th>File &amp; Line Reference</th>
            <th>What Canonical <code>main@99a3506</code> Currently States</th>
            <th>What Official Primary Sources Prove (2026-11-27)</th>
            <th>Source</th>
          </tr>
        </thead>
        <tbody>{''.join(rows)}</tbody>
      </table>
    </div>
    """
    return page_shell("repo-review.html", "Repo Review (14 Findings)", body)


def build_flagged(audit_qa: dict) -> str:
    rows = []
    for f in audit_qa["flags"]:
        rows.append(f"""
        <tr>
          <td><strong>{esc(f['id'])}</strong></td>
          <td><span class="badge medium">{esc(f['category'])}</span></td>
          <td><strong>{esc(f['item'])}</strong></td>
          <td>{esc(f['detail'])}</td>
          <td><a class="pill-link" href="{esc(f['official_url'])}" target="_blank" rel="noopener">Verify Official Page ↗</a></td>
        </tr>""")

    body = f"""
    <section class="hero">
      <span class="eyebrow">Complete Transparency Log · Zero Unverified Claims</span>
      <h1>Flagged for Review (22 Items)</h1>
      <p class="lead">Every blank price, dish-level estimate, schedule contradiction, temporary restaurant closure, expiring Cyber promotion, bot-blocked booking engine, and misleading social/venue star claim is logged below with its official verification link.</p>
    </section>

    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Flag ID</th>
            <th>Category</th>
            <th>Affected Hotel / Restaurant / Activity</th>
            <th>Why Flagged &amp; How Handled</th>
            <th>Official Check URL</th>
          </tr>
        </thead>
        <tbody>{''.join(rows)}</tbody>
      </table>
    </div>
    """
    return page_shell("flagged.html", "Flagged for Review (22)", body)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    hotels = json.loads((DATA / "session-6851cc7e-hotels.json").read_text(encoding="utf-8"))
    michelin = json.loads((DATA / "session-6851cc7e-michelin.json").read_text(encoding="utf-8"))
    act_tr = json.loads((DATA / "session-6851cc7e-activities-transit.json").read_text(encoding="utf-8"))
    audit_qa = json.loads((DATA / "session-6851cc7e-audit-qa.json").read_text(encoding="utf-8"))

    (OUT / "style.css").write_text(CSS, encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")

    pages = {
        "index.html": build_index(hotels, michelin, act_tr, audit_qa),
        "hotels.html": build_hotels(hotels),
        "costs.html": build_costs(hotels, michelin, act_tr),
        "michelin.html": build_michelin(michelin),
        "activities-transit.html": build_activities_transit(act_tr),
        "questions-suggestions.html": build_qa_suggestions(audit_qa),
        "repo-review.html": build_repo_review(audit_qa),
        "flagged.html": build_flagged(audit_qa),
    }
    for fname, content in pages.items():
        (OUT / fname).write_text(content, encoding="utf-8")
    print(f"Built {len(pages)} HTML pages + style.css in {OUT}")


if __name__ == "__main__":
    main()
