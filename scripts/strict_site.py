"""Primary decision views. Never promote inherited snapshots/model outputs to verified facts.

The original generator functions and raw source datasets are retained for audit;
this renderer deliberately consumes only the field-specific 27 November evidence.
All markup containing source data is escaped. No network calls at build time.
"""
import html
import json
import re
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'data'
REPO = 'https://github.com/kanlerxz87-cyber/Vegas1/blob/main/'


def load(name):
    return json.loads((DATA / name).read_text(encoding='utf-8'))


E = load('verification-2026-11-27.json')
M = E['michelin_source']
RTC = 'https://www.rtcsnv.com/ways-to-travel/fares-passes/'
MONO = 'https://www.lvmonorail.com/ticket-information/'
RES = load('restaurants.json')['restaurants']
NAV = [('index.html', 'Overview'), ('hotels.html', 'Hotels'),
       ('restaurants.html', 'Michelin dining'), ('activities.html', 'Activities'),
       ('transit.html', 'Transport'), ('questions.html', 'Questions'),
       ('suggestions.html', 'Suggestions'), ('flagged.html', 'Flagged for Review'),
       ('sources.html', 'Evidence'), ('repo-review.html', 'Repo review')]
esc = html.escape
BLANK = '<span class="empty" aria-label="Unverified value">—</span>'


def link(url, label='Official source'):
    if not url:
        return BLANK
    if not (url.startswith('https://') or url.startswith('http://')):
        raise ValueError(f'Not an absolute evidence URL: {url}')
    return f'<a href="{esc(url, quote=True)}" rel="noopener">{esc(label)}</a>'


def text(value):
    return esc(str(value)) if value not in (None, '') else BLANK


def panel(title, body, id=None):
    ident = f' id="{esc(id)}"' if id else ''
    return f'<section class="panel"{ident}><h2>{esc(title)}</h2>{body}</section>'


def table(headers, rows, caption, ids=None):
    """Responsive semantic table. Cells are escaped or constructed with link/text helpers."""
    out = []
    for n, row in enumerate(rows):
        ident = f' id="{esc(ids[n])}"' if ids else ''
        cells = ''.join(f'<td data-label="{esc(h)}">{c}</td>' for h, c in zip(headers, row))
        if len(row) != len(headers):
            raise ValueError('Table cell/header mismatch')
        out.append(f'<tr{ident}>{cells}</tr>')
    heads = ''.join(f'<th scope="col">{esc(h)}</th>' for h in headers)
    return (f'<div class="scroll" role="region" aria-label="{esc(caption)}" tabindex="0">'
            f'<table class="data responsive"><caption>{esc(caption)}</caption>'
            f'<thead><tr>{heads}</tr></thead><tbody>{"".join(out)}</tbody></table></div>')


def page(name, title, intro, body):
    nav = ''.join(f'<a href="{h}"' + (' aria-current="page" class="on"' if h == name else '')
                  + f'>{esc(label)}</a>' for h, label in NAV)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} · Las Vegas 2027</title><meta name="description" content="{esc(intro)}">
<link rel="stylesheet" href="style.css"></head><body>
<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap"><a class="brand" href="index.html"><span class="dot"></span>VEGAS / 2027</a>
<nav>{nav}</nav></div></header><main id="main" class="wrap">
<div class="pagehead"><p class="eyebrow">TWO ADULTS · FEBRUARY–MARCH · EVIDENCE CHECKED 27 NOV 2026</p>
<h1>{esc(title)}</h1><p class="sub">{esc(intro)}</p></div>
<p class="notice"><strong>Evidence, not a booking confirmation.</strong> — means unverified; no missing value has been estimated.
Published hours are Las Vegas local time and may change before the trip. <a href="flagged.html">Read the limitations</a>.</p>
{body}</main><footer class="wrap"><p>Two adults · one room · USD · all meal/activity subtotals are for two, not per person.
Subtotals are not all-in checkout totals. No bookings or payments have been made.</p>
<p>Field-specific official evidence checked 27 Nov 2026. Historical captures dated 25–26 Nov remain in the repository;
they are not used to rank hotels. <a href="sources.html">Sources & verification scope</a> · <a href="repo-review.html">Repository audit</a></p></footer></body></html>'''


def social(rec, id=None, category=None):
    fresh = rec.get('social', [])
    output = '<br>'.join(link(x['url'], x['label']) for x in fresh)
    if not output:
        output = BLANK + '<br><small>Not freshly confirmed in this integration</small>'
    else:
        output += '<br><small>Linked by official site; content not independently audited</small>'
    # Preserve other sessions' reviewed accounts, with their actual provenance and
    # uncertainty, rather than replacing their work with this pass's smaller sample.
    prior = next((r for r in load('socials.json').get(category or '', []) if r['id'] == id), None)
    if prior:
        urls = {x['url'] for x in fresh}
        leads = []
        for platform in ['instagram', 'tiktok', 'youtube']:
            url = prior.get(platform)
            if not url or url in urls:
                continue
            # Prior ledger only documents specific YouTube evidence for Sphere and Mob.
            # Its other video fields conflict with its caveats; do not promote them.
            if platform == 'youtube' and id not in {'sphere', 'mob-museum'}:
                continue
            leads.append(link(url, platform.title() + ' — prior-session check'))
        evidence = text(prior.get('evidence')) + '<br>' + text(prior.get('caveat'))
        if leads:
            output += ('<details><summary>Earlier session evidence (27 Nov; not refreshed here)</summary>'
                       + '<br>'.join(leads) + '<p class="tiny">' + evidence + '</p>'
                       + link(REPO+'data/socials.json', 'Original provenance record') + '</details>')
    return output


def prices(rec):
    """Exact arithmetic only, retaining 'from' in option labels. No rounded nightly expansion."""
    parts = []
    for opt in rec.get('price_options', []):
        amount = Decimal(str(opt['per_person'])) * 2
        parts.append(f'<strong>${amount:,.2f}</strong> — {esc(opt["label"])}')
    return '<br>'.join(parts) or BLANK


def index():
    cards = [('24', 'Michelin listings', '4 starred · 3 Bib Gourmand · 17 Recommended'),
             ('7–14', 'Nights allowed', 'Working scenario: 15–22 February 2027'),
             ('0', 'Verified all-in hotel quotes', 'No price winner or cheapest week declared'),
             ('Open', '≤60-minute route test', 'No hotel-level bus ranking is verified')]
    tiles = '<section class="grid4">' + ''.join(f'<div class="card"><div class="big">{v}</div><div class="lbl">{k}</div><p>{d}</p></div>' for v,k,d in cards) + '</section>'
    body = panel('Executive summary', '''<p><strong>Keep 15–22 February 2027 as a planning scenario, not a booked recommendation.</strong>
Your preferred 15–18 February window is only three nights; it cannot also satisfy a one-to-two-week holiday.
Extending the preferred arrival to seven nights avoids inventing a new arrival preference. A 14-night alternative is 15 February–1 March.</p>
<p><strong>There is no defensible “best hotel” or “cheapest time to book” yet.</strong> Official engines did not yield an unambiguous,
all-in seven-night checkout total with confirmed room and party size. Historical OTA prices and zone estimates have been removed from primary decision tables.</p>
<p>Michelin’s 31 August 2026 announcement supports all 24 Las Vegas listings below. Stars belong to restaurants, not hotels;
Bib Gourmand and Recommended do <em>not</em> mean starred. 2027 awards and reservation availability are not established.</p>''' + link(M, 'Read Michelin’s full official selection'))
    body += tiles
    body += panel('Choose a research path — not a winner', table(['Priority', 'Candidate path', 'Why it is relevant', 'Official evidence'], [
        ['Most listings in one connected resort', 'Venetian / Palazzo complex', '4 listings (all Recommended); not 4 stars, and not a timed bus ranking.', link(M)],
        ['Star-focused stay', 'MGM Grand', 'Hosts Joël Robuchon (2 stars) and L’Atelier (1 star); room and total still unverified.', link(M)],
        ['One starred dinner plus a Bib Gourmand', 'The Cosmopolitan', 'é and China Poblano at the same property; named-room total still missing.', link(M)],
        ['Named-bed rate leads', 'Caesars Palace / Flamingo', 'Official engine shows King / Two Queens descriptions; exact totals and error banners unresolved.', link(E['hotels']['caesars-palace']['source'])],
    ], 'Source-backed options without an invented price or transit score'))
    body += panel('What must not be carried forward', '''<ul class="tight"><li>“Every hotel reaches all 24 restaurants in one hour” is withdrawn: no complete door-to-door bus evidence supports it.</li>
<li>“March is cheapest” is unproven. An optimal purchase date is different from the cheapest stay dates; neither is established.</li>
<li>Michael Mina is Guide-listed but its official page says temporarily closed. Do not assume a February reopening.</li>
<li>The Mob Museum’s inherited recurring Thursday early close was wrong. The current official weekly schedule says daily 9 AM–9 PM.</li></ul>
<p><a href="flagged.html">Review flags and evidence</a> · <a href="questions.html">See unanswered decisions</a> · <a href="suggestions.html">Review improvements before adoption</a></p>''')
    body += panel('A flexible seven-night outline', '''<p>This is a proposed pacing template, not a verified or reserved itinerary. It does not claim that any journey is under an hour.
Avoid buying nonrefundable dining/show tickets until a room and feasible routes are confirmed.</p>''' + table(['Dates', 'Proposed focus', 'Condition before scheduling', 'Official reference'], [
        ['Mon 15 Feb', 'Arrival / settle in', 'Confirm check-in, flights and named room. No dinner commitment.', link(E['hotels']['caesars-palace']['source'])],
        ['Tue 16–Wed 17 Feb', 'One star-focused evening, one flexible day', 'MGM Grand or é candidate; secure a real reservation before assigning a night.', link(M)],
        ['Thu 18–Fri 19 Feb', 'One museum / downtown outing; leave an evening open', 'Check exact 2027 ticket, return route and early closures.', link(E['activities']['neon-museum']['source'])],
        ['Sat 20–Sun 21 Feb', 'One additional dining cluster, optional show or rest', 'Show date, total for two, dietary fit and transport remain gates.', link(E['activities']['sphere']['source'])],
        ['Mon 22 Feb', 'Check out / departure', 'Departure flight and transfer unverified.', link(E['hotels']['caesars-palace']['source'])],
    ], 'Suggested pacing only; venue-level details and social links are on category pages'))
    return page('index.html', 'A better-informed week in Las Vegas', 'A simple planning dashboard: what is confirmed, what is missing, and what can reasonably be decided.', body)


def hotels():
    rows=[]
    for id,h in sorted(E['hotels'].items(), key=lambda kv:kv[1]['name']):
        room = text(h.get('room')) + '<br>' + text(h.get('bed'))
        bath = text(h.get('bathroom')) + '<br><small>Exclusive/private-use guarantee for dated room: unverified</small>'
        rows.append([text(h['name']), room, bath, text(h.get('amenities')), BLANK, BLANK,
                     text(h['check']) + '<br><a href="flagged.html#F-65">Unverified decision fields</a>', link(h['source'])])
    body=panel('No price or transit winner is verified', '''<p>The requested ranking needs a qualifying named room, private bathroom, a full seven-night total for two adults, and timed bus journeys for each restaurant.
Those requirements are not met together by any captured quote. Properties below are <strong>alphabetical candidates, not a ranking</strong>.
Missing totals and ≤60-minute counts are blank; historical star classifications, guest scores and zone-model counts are not promoted into this view.</p>
<p>Bathroom descriptions are quoted only where actually read; they do not automatically prove exclusive private use for the requested rate.
MGM Grand is added because Michelin explicitly locates two starred restaurants there; the Signature is a different candidate.</p>''')
    body+=table(['Hotel candidate','Named room / bed','Bathroom evidence','Amenities evidence','7-night total, 2 adults','Verified ≤60-min count','Verification / limitations','Official link'],rows,'33 candidates · total basis: 15–22 February 2027 · USD',ids=list(id for id,h in sorted(E['hotels'].items(),key=lambda kv:kv[1]['name'])))
    body=body.replace('<table class="data responsive">', '<table id="official-hotel-decisions" class="data responsive">', 1)
    body+=panel('A valid location comparison: published host-property clusters', '''<p>Sorted by count within the named host property/complex, from Michelin’s published locations. This is a transparent research aid,
<strong>not a substitute for your bus-within-one-hour ranking</strong>, and no zero-minute walking time is implied.</p>''' + table(['Host property / complex','Guide listings','Starred venues','Listed but not starred','Source'],[
        ['Venetian / Palazzo connected resort','4','0 in this selection','Bouchon, COTE, Estiatorio Milos, Mott 32',link(M)],
        ['MGM Grand','2','Joël Robuchon (2 stars); L’Atelier (1 star)','—',link(M)],
        ['The Cosmopolitan','2','é (1 star)','China Poblano (Bib Gourmand)',link(M)],
        ['Caesars Palace','1','Guy Savoy (1 star)','—',link(M)],
        ['Wynn / ARIA / Resorts World / Bellagio','1 each','0 in this selection','Wing Lei / Gymkhana / Stubborn Seed / Michael Mina respectively; Mina opening unresolved',link(M)],
    ],'Selected clusters, not an exhaustive zero-count hotel ranking'))
    body+=panel('Date and purchase timing', '<p><a href="pricing.html">Compare exact date scenarios and pricing gaps</a>. A live nightly headline, especially a rounded average, is not an exact seven-night total. No taxes or fees have been guessed.</p>')
    return page('hotels.html','Hotel candidates & decision gates','No inferred prices, private-bath guarantees or bus counts. Official links and evidence sit beside each candidate.',body)


def restaurants():
    body=panel('2026 Guide status, not legacy stars', '''<p>All 24 Las Vegas rows were compared individually with Michelin’s official selection: one two-star restaurant, three one-star restaurants,
three Bib Gourmands and 17 Recommended. No three-star Las Vegas entry appears in that selection. These are 2026 distinctions, not a guarantee of a 2027 award.</p>
<p>Menu subtotals below are <strong>for two adults</strong>, calculated as exactly twice a published per-person menu price. They are not estimated à la carte spend or final tax/tip-inclusive totals.
Blank means unverified. Current weekly schedules are not date-specific reservations. Social profiles sourced from a property footer are labelled as property channels, not venue-specific videos.</p>''')
    for cat,title in [('starred','Starred restaurants'),('bib','Bib Gourmand — listed, not starred'),('recommended','Recommended — listed, not starred')]:
        rows=[];ids=[]
        for r in RES:
            v=E['restaurants'][r['id']]
            if v['award_class']!=cat:continue
            source=link(v['source'],'Venue website')+'<br>'+link(M,'Michelin: award & address')
            if v.get('hours_source'):source+='<br>'+link(v['hours_source'],'Official hours')
            if v.get('menu_source'):source+='<br>'+link(v['menu_source'],'Official menu')
            price=prices(v)+'<br><small>All-in total: unverified</small>'
            if v.get('price_note'):price+='<br><small>'+esc(v['price_note'])+'</small>'
            rows.append([text(r['name'])+'<br><span class="badge">'+esc(v['award'])+'</span>',
                         text(v['location'])+'<br><small>'+esc(v['address'])+' (Michelin listing)</small>',
                         text(v['days'])+'<br>'+text(v['hours']),text(v['exceptions']),price,social(v,r['id'],'restaurants'),source])
            ids.append(r['id'])
        body+=panel(title,table(['Restaurant / distinction','Published location','Open days / hours','Exceptions / gaps','Menu subtotal, 2 adults','Watch / social','Official evidence'],rows,title,ids))
    body+=panel('Missing is not nonexistent', '<p>Where hours, prices or social links are blank, no reliable value was extracted from the official page in this pass. The <a href="sources.html">row-level evidence ledger</a> gives the check result for every venue. Expandable prior-session accounts retain upstream provenance without claiming a new check. Older raw creator-video leads remain available for audit but were not verified as primary sources.</p>')
    return page('restaurants.html','Michelin dining, clearly distinguished','24 listings, restaurant-by-restaurant hours, couple subtotals and official evidence.',body)


def activities():
    rows=[]
    for id,a in E['activities'].items():
        sources=link(a['source'])
        if a.get('menu_source'):sources+='<br>'+link(a['menu_source'],'Official tickets')
        rows.append([text(a['name']),text(a['days'])+'<br>'+text(a['hours']),text(a['exceptions']),prices(a)+'<br><small>'+esc(a.get('price_note','Total for requested date unverified.'))+'</small>',social(a,id,'activities'),sources])
    body=panel('Current information versus a 2027 ticket', '<p>Only Neon Museum explicitly labels the quoted admission product “2027”. Other published prices are current starting prices, not a locked 2027 checkout quote. Each displayed amount is a two-adult subtotal; processing fees and taxes are not guessed. No hotel-to-activity journey has been verified under 60 minutes.</p>')
    body+=table(['Activity','Days / hours','Exceptions / limitations','Subtotal, 2 adults','Watch / social','Official source'],rows,'Five activity candidates',list(E['activities']))
    return page('activities.html','Activities without the guesswork','Opening information, exceptions, two-adult subtotals and source-linked social profiles.',body)


def transit():
    body=panel('The requested one-hour bus ranking remains unresolved', '''<p>Use RTC buses for the literal bus constraint. Monorail is a separately ticketed rail alternative, not a subway.
Vegas Loop cars are not buses or subway trains and are <strong>excluded</strong> from a compliant bus-only score.</p>
<p>The inherited zone matrix used zero-minute same-zone trips, fixed times without a departure, and broad zones including Henderson/Summerlin.
It cannot prove all 24 restaurants are within an hour of all hotels. <strong>That conclusion and the 20-minute substitution are withdrawn from primary views.</strong>
A Route 203 scheduled segment alone does not prove an entire journey including hotel walks, waiting, transfers and the last walk.</p>''' + link(RTC,'RTC official fares and trip-planning app'))
    body+=table(['Service / product','Published subtotal, 2 adults','What this confirms','Official source'],[
        ['RTC visitor single / 2-hour / 24-hour / 3-day','$8 / $12 / $16 / $40','Twice current published $4 / $6 / $8 / $20. All passes valid all routes; visitors required to pay Strip & All Access fares. Not a 2027 price guarantee.',link(RTC)],
        ['Monorail one-ride e-ticket / seven-day e-ticket','$11.50 / $119.90','Twice current published $5.75 / $59.95. Separate ticket from RTC. Unlimited duration begins first use.',link(MONO)],
        ['RTC Route 203 timetable',BLANK,'Official PDF retained for route review; full dated door-to-door trip not verified in this pass.',link('https://rtcws.rtcsnv.com/routePDF/203.pdf')],
    ],'Current transit products, not a complete transport budget')
    body+=panel('How to close the route evidence gap', '''<ol class="tight"><li>Fix the hotel entrance, restaurant entrance, dining arrival time and return time.</li><li>Use operator trip planning and dated timetables for outward <em>and</em> return journeys; include every walk, wait and transfer.</li><li>Save the itinerary, route numbers, departure date/time and retrieval timestamp as evidence.</li><li>Count a restaurant only when a qualifying bus journey satisfies the one-hour threshold. Leave unresolved routes blank rather than zero.</li><li>Do not call a proposed fare change enacted without an official effective-date notice.</li></ol>''' + link('https://www.rtcsnv.com/ways-to-travel/how-to-ride/ridertc-app/','Official RideRTC planning app'))
    return page('transit.html','Transport: verify the whole journey','Published fares are source-backed; hotel-to-restaurant door-to-door travel times are not yet verified.',body)


def pricing():
    windows=[('2027-02-15','2027-02-22'),('2027-02-22','2027-03-01'),('2027-03-01','2027-03-08'),('2027-03-08','2027-03-15'),('2027-03-15','2027-03-22'),('2027-03-16','2027-03-23')]
    rows=[]
    for start,end in windows:
        rows.append([start,end,'7',BLANK,'Unverified; no comparable all-in room quote',link(E['hotels']['caesars-palace']['source'],'Official engine (15–22 Feb attempt only)')])
    body=panel('Cheapest stay dates ≠ best purchase date', '''<p>No cheapest week or optimal future booking day has been verified. There are 30 possible seven-night check-in dates from 15 February through 16 March 2027; sampling a few Mondays cannot establish the minimum.</p>
<p>The scenarios below are date arithmetic, not availability or pricing evidence. 15–18 February is a separate three-night preference, outside the stated seven-to-fourteen-night duration. The final 16–23 March scenario uses your end boundary.</p>''')
    body+=table(['Check-in','Check-out','Nights','Official 7-night all-in total','Status','Official rate reference'],rows,'Date scenarios · two adults · one room · USD')
    body+=panel('A real booking deadline, not a forecast', '''<p>Wynn’s official exact-date page publishes the public “Wynn Cyber Exclusive” offer: book <strong>20 November–4 December 2026</strong>, for stays <strong>22 November 2026–30 June 2027</strong>, one to fourteen nights.
It states a one-night room-and-tax deposit and a cancellation deadline 72 hours before arrival. These are the checked offer’s terms, not universal hotel policies.</p>
<p><strong>Suggested action:</strong> evaluate the offer before 4 December only if Wynn fits the budget and a valid checkout quote/occupancy can be obtained.
There is no evidence that this is the lowest price you will ever see. The page exposes rounded average-night rates but not an unambiguous final seven-night total; those averages are not multiplied into a purported exact total.</p>''' + link(E['hotels']['wynn']['source'],'Official dated Wynn offer & terms'))
    body+=panel('Quote acceptance checklist', '''<p>Same named room; two adults/one room; guaranteed queen-or-larger; exclusive bathroom; exact seven nights; currency; base total; mandatory resort fee; all taxes; total due; refundable/nonrefundable terms; deposit; loyalty eligibility; retrieval time.</p>
<p>Neither a property home page, an OTA search list nor “$X/night” without a precise checkout breakdown clears that gate. See <a href="flagged.html#F-65">F-65</a>.</p>''')
    return page('pricing.html','Dates & booking timing','Explicit date scenarios, a verified offer deadline, and no fabricated seven-night totals.',body)


QUESTIONS=[
('Q-01','Can hotels be ranked by restaurants within one hour by bus?','Unresolved','No complete dated door-to-door route evidence. A 20-minute estimate is not an approved replacement.','Run exact outward/return operator itineraries once hotel and dining times are fixed.',RTC),
('Q-02','Which trip length takes precedence?','Conflict','Preferred 15–18 Feb is 3 nights; required duration is 7–14 nights.','Working scenario 15–22 Feb (7 nights); keep 15 Feb–1 Mar (14 nights) as an alternative, not a confirmed preference.',M),
('Q-03','What total budget applies?','Unknown','Hotel, food, flights, activities and transport budget not supplied.','Obtain comparable official checkout totals; publish value tiers rather than invent a spending ceiling.',E['hotels']['caesars-palace']['source']),
('Q-04','Are meal totals known?','Partly answered','Published menu subtotals for two exist for Anima, Partage and Stubborn Seed; no all-in restaurant budget.','Use dated menus, actual choices, beverage plan and fee/tax disclosures. No assumed spend at à la carte venues.',E['restaurants']['partage']['menu_source']),
('Q-05','Are bed and private bathroom guaranteed?','Unresolved','Some named room/bed descriptions verified; exclusive-use promise and dated rate not captured together.','Require the named-room checkout details; reject assigned-on-arrival room as proof of bed size.',E['hotels']['flamingo']['source']),
('Q-06','Which week is cheapest? When should it be booked?','Unresolved','No comparable official all-in seven-night totals. Future best purchase day cannot be established from one snapshot.','Compare 30 possible seven-night starts consistently. Wynn offer deadline is 4 Dec 2026, not proof of a global minimum.',E['hotels']['wynn']['source']),
('Q-07','Dietary restrictions, allergies or alcohol preferences?','Unknown','Not supplied. Partage excludes several diets; Kabuto raw-fish substitutions not accommodated.','Obtain venue dietary policy before a nonrefundable dining commitment. Do not infer suitability.',E['restaurants']['partage']['menu_source']),
('Q-08','Are 2027 dates and hours guaranteed?','No','Current weekly hours do not guarantee a 2027 reservation. Some show calendars need interactive loading.','Capture exact-date confirmation, closure notices and cancellation policy.',E['activities']['sphere']['source']),
('Q-09','How much walking or mobility support is needed?','Unknown','No walking tolerance or accessibility needs provided.','Record entrance-to-stop walks and accessible route/elevator information from operators.',RTC),
('Q-10','Are all social links venue-specific and usable?','Partly answered','Fresh links come from official pages; expandable earlier-session accounts retain their provenance and caveats. Destinations not all rechecked here.','Check identity and content before promoting a video as a recommendation; leave absent handles blank.',E['activities']['neon-museum']['source']),
('Q-11','Can Michael Mina be included?','Unresolved','Michelin Recommended, but official page says temporarily closed. No 2027 reopening confirmed.','Require dated venue reopening/availability; do not count it as a bookable dinner.',E['restaurants']['michael-mina']['source']),
('Q-12','What flights, entry documents and airport transfer apply?','Unknown','Origin airport, passports, flight times and transfer budget not supplied; user location is not treated as departure proof.','Collect official airline/entry information once traveler-specific facts exist; do not assume eligibility.',RTC),
('Q-13','What does an official-link check prove?','Answered','A responding property page does not verify price, bed, bathroom, opening or booking availability.','Use field-specific evidence and leave other fields blank. See the per-row ledger.',M),
]


def questions():
    rows=[[text(id),text(q),text(status),text(answer),text(action),link(src)] for id,q,status,answer,action,src in QUESTIONS]
    body=panel('No questionnaire is required to read this plan', '<p>The register records missing decisions without asking you to fill a form. Working scenarios are explicitly labelled, never passed off as your answers. Unknown personal preferences cannot be verified from a public website; no purchase or irreversible trip choice has been made.</p>')
    body+=table(['ID','Question','Status','What is known / missing','How to discover the missing information','Official context'],rows,'Decision questions, answers and discovery routes',[q[0] for q in QUESTIONS])
    return page('questions.html','Questions before a reasonable decision','Clear answers where evidence exists; explicit gaps and research steps where it does not.',body)


SUGGESTIONS=[
('S-01','Collect comparable checkout totals','High','Capture named room, exact dates, party size, tax, mandatory fees and cancellation. Rank only accepted quotes.','Requires working booking engines; no projected savings promised.',E['hotels']['caesars-palace']['source']),
('S-02','Build a bus-only itinerary matrix','High','Use per-venue outward and return journeys with departure date, all walks/waits/transfers.','More evidence work; do not use Loop or zero-minute zones to fill gaps.',RTC),
('S-03','Choose duration before optimizing','High','Keep seven-night and fourteen-night alternatives separate from the three-night preference.','Changes time off and total budget; not selected for you.',M),
('S-04','Use total trip cost, not headline nightly rates','High','Combine accepted hotel totals, chosen meal subtotals, tickets and transport only after fees are verified.','No all-in trip budget is currently supportable.',E['hotels']['flamingo']['source']),
('S-05','Review Wynn offer by 4 Dec 2026','Time-sensitive','Assess published terms and real checkout quote before its stated purchase deadline.','An offer expiry is not proof that booking now is optimal.',E['hotels']['wynn']['source']),
('S-06','Prioritize on-site dining clusters as a research aid','Medium','Compare Venetian/Palazzo, MGM Grand and Cosmopolitan hosts.','On-site count is not a verified public-transit ranking and must not replace it silently.',M),
('S-07','Add dated closure and price-expiry checks','High','Keep future exceptions separate from current weekly hours and re-fetch before committing.','Official pages can contradict themselves or retain old events.',E['activities']['high-roller']['source']),
('S-08','Expand authentic social coverage','Medium','Read official venue links and label property-wide accounts. Keep reviewed links beside the venue.','A link on an official page verifies provenance, not every claim in a video.',E['restaurants']['gymkhana']['source']),
('S-09','Check dietary and accessibility fit early','High','Apply explicit venue policies before selecting tasting menus or transport.','Personal constraints not supplied; no suitability guessed.',E['restaurants']['partage']['menu_source']),
('S-10','Publish a quote history and evidence expiry','Medium','Preserve retrieval timestamp, source excerpts, room/rate identifiers and changes.','Needs a trustworthy data source; do not silently auto-promote scraped rates.',E['hotels']['wynn']['source']),
]


def suggestions():
    rows=[[text(id),text(title),text(priority),'Proposal — not selected',text(action),text(trade),link(src)] for id,title,priority,action,trade,src in SUGGESTIONS]
    body=panel('Review first, implement later', '''<p>These are options for the next decision/research phase, not changes assumed approved. No preference has been invented and no reservation made.
Evidence corrections and the mobile layout are implemented; ranking substitutions, new budgets, automation services and purchases are not.</p>
<p><strong>Suggested sequence:</strong> establish duration → collect qualifying checkout quotes → test exact bus routes → compare total cost and dining availability → select a refundable option if its actual terms are acceptable.</p>''')
    body+=table(['ID','Improvement','Priority','State','Proposed next step','Trade-off / missing gate','Official context'],rows,'Reviewable suggestions, not auto-approved decisions',[s[0] for s in SUGGESTIONS])
    return page('suggestions.html','Suggestions to review','A decision backlog with explicit benefits, costs and prerequisites; nothing here spends money or invents approval.',body)


def sources():
    rows=[]
    for cat in ['restaurants','activities','hotels']:
        for id,r in E[cat].items():
            name=next((x['name'] for x in RES if x['id']==id),r.get('name',id))
            detail=r.get('check','Only the populated fields were confirmed; blanks remain unverified.')
            if cat=='restaurants':detail+=' Award and address checked against Michelin. Current schedule only where populated.'
            rows.append([text(cat),text(name),text(detail),link(r['source'])+(('<br>'+link(M,'Michelin award/location')) if cat=='restaurants' else '')])
    body=panel('What was actually verified', '''<p>Checked 27 November 2026 with official pages. All 24 award tiers and Michelin-listed addresses were compared individually to the official selection. Venue pages were opened for all 24 restaurants and five activities; only extracted fields enter the primary views.
Five hotel candidates have fresh official room/contact/engine evidence, while other hotel links are inherited and explicitly not claimed rechecked. Fetching a restaurant page at a hotel is not a hotel room/rate check.</p>
<p><strong>Not verified:</strong> complete all-in seven-night hotel totals, a global cheapest stay window, the optimal future purchase day, exact bus routes, 2027 reservation availability, private-use promises for every room and all social destinations.</p>
<p>All check results are published in the field-specific <a href="https://github.com/kanlerxz87-cyber/Vegas1/blob/main/data/verification-2026-11-27.json">machine-readable evidence ledger</a>.
This is a curated record of retrieved page text, not a claim that every website or archived record has been fully verified.</p>''')
    body+=table(['Category','Entry','Check result / limits','Official reference'],rows,'Row-by-row evidence coverage')
    body+=panel('Historical research — audit only', '''<p>Earlier datasets, quote captures and independent subsites remain intact. They contain estimates, conflicting hours, withdrawn rates and older verification labels;
they must not be used as current verified decision tables. They are preserved so parallel-session work is not discarded.</p>''' + ''.join('<p>'+link(REPO+x,x)+'</p>' for x in ['data/hotels.json','data/transit.json','data/price-windows.json','data/restaurants.json','data/activities.json','data/review.json','data/review-flags.json','FLAGS.md','COORDINATION.md']))
    return page('sources.html','Evidence & verification coverage','Field-level confidence, official links, retrieval date and limitations for every candidate.',body)


def flagged():
    rows=[[text(f['id']),text(f['title']),text(f['finding']),'<br>'.join(link(u) for u in f['sources'])] for f in E['checks']]
    body=panel('Current decision-impacting flags', '''<p>These do not block website publication. They <em>do</em> prevent unsupported booking, price and route recommendations. A blank is not zero, sold out or unavailable. Current flags supersede conflicting historical conclusions.</p>'''+table(['ID','Finding','Effect / missing evidence','Official sources'],rows,'27 November strict-evidence review',[f['id'] for f in E['checks']]))
    # Keep every historical ID/row addressable, without treating its claims as current verification.
    historical=[];ids=[]
    for line in (ROOT/'FLAGS.md').read_text().splitlines():
        if line.startswith('| **F-'):
            cells=[c.strip().replace('**','') for c in line.strip().strip('|').split('|')]
            if len(cells)==4 and cells[0] not in ids and cells[0] not in {f['id'] for f in E['checks']}:
                historical.append([text(cells[0]),text(' · '.join(cells[1:])),link(M,'Official selection / location context')+'<br>'+link(REPO+'FLAGS.md','Original record')]);ids.append(cells[0])
    for f in load('review-flags.json')['flags']:
        if f['id'] in ids:continue
        srcs='<br>'.join(link(s['url'],s['label']) for s in f['sources'])
        historical.append([text(f['id']),text(f['title']+' · '+f['what']+' · '+f['effect']),link(M,'Official selection context')+'<br>'+srcs]);ids.append(f['id'])
    body+=panel('Historical flag register — superseded where inconsistent', '''<p>All earlier flag IDs remain available for review. These are historical assertions from 25–26 November, not newly verified facts.
References to showing OTA figures, a 20-minute ranking or universal one-hour coverage no longer describe the current primary views.
The official selection link is location/award context only, not proof of every historical pricing claim; the original record and specific references are retained.</p>'''+table(['ID','Original flag text (historical)','Source / context'],historical,'Historical flags retained for audit',ids))
    return page('flagged.html','Flagged for Review','Missing evidence, contradictions and superseded claims, with sources for manual review.',body)


def repo_review():
    rows=[
        ['Primary renderer','scripts/strict_site.py','Uses only populated field-specific evidence for decision values; old source data and generator functions retained, not silently trusted.',link(M)],
        ['Pricing audit','data/hotels.json / price-windows.json','Historical third-party captures differ in room, fee and total basis. Not used as verified official price comparisons.',link(E['hotels']['caesars-palace']['source'])],
        ['Transit audit','data/transit.json','Zero-minute zones and mode substitution cannot establish requested bus-only routes. Historical computed counts excluded.',link(RTC)],
        ['Restaurant audit','24 evidence rows','Michelin tiers/addresses checked; current venue fields extracted individually. Missing hours/prices left blank. COTE address corrected to Michelin’s 3355 listing.',link(M)],
        ['Activity audit','5 evidence rows','Corrected Mob Museum holiday/weekly-hours confusion; exposed High Roller source conflicts and Neon date-widget anomaly.',link(E['activities']['mob-museum']['source'])],
        ['Room evidence','33 candidates','Five fresh official room/contact checks. Only 4 have extracted room descriptions; private-use/dated booking qualification still incomplete.',link(E['hotels']['desert-rose']['source'])],
        ['Source scope','External URLs','Opening a URL is not field verification. Automated build checks local links; external availability is not comprehensively certified.',link(M)],
        ['Parallel work','COORDINATION.md','T17 integration claimed after completed prior tasks. Assigned Arena branch retained; existing archives and source datasets preserved.',link(REPO+'COORDINATION.md','Coordination record')],
    ]
    body=panel('Review result', '<p>The site is useful as a source-linked research dashboard, not yet a booking-ready optimized vacation. The biggest inherited irregularities were unsupported hotel/transit rankings and headline rates, not HTML build failures. Every source dataset remains available in Git; the new view prevents incomplete evidence being promoted into facts.</p>')
    body+=table(['Area','Files / scope','Review outcome','Official / audit context'],rows,'Code, data and evidence audit')
    body+=panel('Verification commands and their limits', '<pre><code>python3 scripts/build.py\npython3 scripts/gen_site.py\npython3 scripts/validate.py\npython3 -m unittest discover -s tests -v</code></pre><p>Checks cover schema/evidence consistency, local links and anchors, root/docs parity, required sources, blank unsafe decision fields, escaping and responsive markup. They do not certify external websites, future availability or prices. Publication/deployment results are recorded in the coordination board after merge.</p>')
    return page('repo-review.html','Repository review','A review of the inherited data and the code that turns evidence into published decision views.',body)


def render():
    pages={'index.html':index(),'hotels.html':hotels(),'restaurants.html':restaurants(),'activities.html':activities(),
           'transit.html':transit(),'pricing.html':pricing(),'questions.html':questions(),'suggestions.html':suggestions(),
           'flagged.html':flagged(),'sources.html':sources(),'repo-review.html':repo_review()}
    pages['summary.html']=page('summary.html','Executive summary','The concise decision view for two adults, 2027.',panel('Start here','<p>The executive summary is on the <a href="index.html">Overview</a>. No hotel rate winner or bus ranking is verified. Use <a href="hotels.html">hotel candidates</a>, <a href="pricing.html">dated scenarios</a>, and <a href="questions.html">decision gates</a>.</p>'))
    pages['verification.html']=page('verification.html','Verification','Evidence and structural tests are separate.',panel('Verification coverage','<p>Use the <a href="sources.html">field-specific evidence ledger</a>, <a href="repo-review.html">repo review</a> and <a href="flagged.html">Flagged for Review</a> register. No local link test is represented as a complete external availability check.</p>'))
    return pages


CSS_EXTRA='''
/* Strict decision view: keyboard access, readable evidence, stacked mobile tables. */
.brand{color:var(--ink)} .eyebrow{font-size:.7rem;letter-spacing:.13em;color:var(--accent);font-weight:650}
.notice{border-left:3px solid var(--warn);background:var(--panel2);padding:12px 16px;border-radius:4px;font-size:.86rem;color:#cfd7e6}
.empty{color:var(--warn)} small{font-size:.78rem;color:#a9b5ca}
caption{text-align:left;padding:12px;color:var(--ink);font-weight:600;background:var(--panel)}
.badge{border:1px solid var(--line);color:var(--star);margin-top:5px}
.skip{position:absolute;left:10px;top:-90px;background:var(--ink);color:var(--bg);padding:12px;z-index:100}
.skip:focus{top:10px} :focus-visible{outline:3px solid var(--accent);outline-offset:3px}
a{overflow-wrap:anywhere} td{overflow-wrap:anywhere} pre{overflow-x:auto}
[id]{scroll-margin-top:150px}
@media(max-width:700px){
 header.top{position:static} header .wrap{display:block} nav{flex-wrap:nowrap;overflow-x:auto;padding:8px 0;gap:6px} nav a{white-space:nowrap;min-height:44px;display:flex;align-items:center}
 .scroll{border:0;overflow:visible} table.responsive{display:block;min-width:0;width:100%}
 table.responsive caption{display:block;border-radius:8px;margin-bottom:8px;font-size:.85rem}
 table.responsive thead{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}
 table.responsive tbody{display:block} table.responsive tr{display:block;margin-bottom:14px;border:1px solid var(--line);border-radius:12px;padding:8px;background:var(--panel)}
 table.responsive td{display:grid;grid-template-columns:minmax(85px,32%) minmax(0,1fr);gap:10px;white-space:normal}
 table.responsive td::before{content:attr(data-label);font-size:.7rem;letter-spacing:.02em;color:var(--muted);font-weight:650}
 table.responsive td>*{min-width:0} table.responsive td br{display:none}
 table.responsive td{display:block} table.responsive td::before{display:block;margin-bottom:5px}
 [id]{scroll-margin-top:16px} .wrap{padding-left:14px;padding-right:14px}
}
@media print{header.top,.skip{display:none} body{background:white;color:black} section.panel,.notice{background:white;border:1px solid #aaa} a,td,small{color:black!important} .wrap{max-width:none} }
'''
