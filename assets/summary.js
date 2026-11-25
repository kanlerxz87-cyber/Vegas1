/* Executive summary renderer — filled with verified findings after research. */
(function () {
  "use strict";
  function esc(s){return String(s==null?"":s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");}
  function block(id, html){var el=document.getElementById(id); if(el) el.innerHTML=html;}
  function ul(items){return "<ul>"+items.map(function(i){return "<li>"+esc(i)+"</li>";}).join("")+"</ul>";}

  document.addEventListener("DOMContentLoaded", function () {
    var D = window.DATA;
    var nR = D.restaurants.length, nH = D.hotels.length, nA = D.activities.length;
    var starred = D.restaurants.filter(function(r){return r.status==="Star";}).length;
    var bib = D.restaurants.filter(function(r){return r.status==="Bib Gourmand";}).length;
    var sel = D.restaurants.filter(function(r){return r.status==="Selected";}).length;
    var unv = D.restaurants.filter(function(r){return !r.verified;}).length;

    block("sum-trip", '<div class="callout"><h3>Trip parameters</h3><p>Destination Las Vegas, NV · 2 adults · 7-night base stay (1–2 weeks) · window Feb 15 – Mar 23, 2027 · preferred Feb 15–18, 2027.</p></div>');

    block("sum-hotel", '<h2 class="sec">Recommended stay</h2>'
      + '<p class="sub">Ranked by Michelin density (on-site restaurants first, then ≤1h reach via bus/monorail). All verified with queen bed + private bath.</p>'
      + '<div class="callout"><p>Las Vegas has <b>no subway</b> — transit = RTC bus (Deuce 24/7, SDX, Route 203) + Las Vegas Monorail (7 stations, MGM Grand→SAHARA). All 24 Michelin restaurants are within ~1 hour of any central-Strip hotel.</p>'
      + '<ol>'
      + '<li><b>The Venetian</b> — 4 Michelin on-site (Bouchon, COTE, Estiatorio Milos, Mott 32).</li>'
      + '<li><b>MGM Grand</b> — 2 starred on-site (Joël Robuchon 2★, L\'Atelier 1★); monorail station on-site.</li>'
      + '<li><b>Cosmopolitan</b> — 2 on-site (é by José Andrés 1★, China Poblano Bib).</li>'
      + '<li><b>Caesars Palace</b> — 1 starred on-site (Guy Savoy).</li>'
      + '<b>Wynn / ARIA / Resorts World / Gold Coast / Bellagio</b> follow (1 on-site each; Bellagio\'s Michael Mina currently temporarily closed).</li>'
      + '</ol>'
      + '<p class="note">Exact nightly rates for Feb 15–22, 2027 are dynamic and not statically extractable — confirm live on each official booking page (see <a href="verification.html">verification</a>).</p></div>');

    block("sum-dining", '<h2 class="sec">Michelin dining</h2>'
      + '<p class="sub">'+nR+' restaurants verified against the official Michelin Guide Nevada listing.</p>'
      + '<div class="callout"><p><b>'+starred+' starred</b> (Joël Robuchon 2★; L\'Atelier, Guy Savoy, é by José Andrés 1★) · <b>'+bib+' Bib Gourmand</b> (China Poblano, Esther\'s Kitchen, Yen Viet Kitchen) · <b>'+sel+' Selected</b>. "Listed in the Guide" vs "holds a star" is distinguished throughout.</p>'
      + '<p>Restaurant cost for 2 adults is shown in the <a href="restaurants.html">restaurants</a> table; exact per-person prices only where published (e.g., Anima by EDO $85/person, Michael Mina $295/person). '+unv+' restaurants have unverified hours/location — left blank and flagged.</p>'
      + '<p class="note">Clusters: Strip (Venetian/Palazzo/MGM/Caesars/Cosmopolitan/Bellagio/ARIA/Wynn), Chinatown, Downtown (Arts District).</p></div>');

    block("sum-activities", '<h2 class="sec">Activities</h2>'
      + '<p class="sub">'+nA+' activities, all within ~1 hour of central-Strip hotels (walk, monorail, or RTC bus).</p>'
      + '<div class="callout"><ul>'
      + '<li><b>Cirque du Soleil "O"</b> (Bellagio) — aquatic show, Wed–Sun 6:30 & 9:00 PM.</li>'
      + '<li><b>Sphere</b> at The Venetian — immersive shows/films (event-based).</li>'
      + '<li><b>High Roller</b> (LINQ) — observation wheel, daily 12 PM–12 AM/2 AM.</li>'
      + '<li><b>Bellagio Conservatory + Fountains</b> — free, 24/7.</li>'
      + '<li><b>Fremont Street Experience</b> (Downtown) — free canopy shows + concerts, 6 PM–2 AM.</li>'
      + '<li><b>Neon Museum</b> (Downtown) — 2027 admission daily 3–11 PM, from $21.</li>'
      + '<li><b>"Welcome to Fabulous Las Vegas" sign</b> — free photo spot.</li>'
      + '</ul></div>');

    block("sum-pricing", '<h2 class="sec">Pricing snapshot</h2>'
      + '<p class="sub">Per the no-inference rule, values that could not be confirmed are left blank and flagged.</p>'
      + '<div class="callout"><p><b>Hotels:</b> 7-night total = 7 × nightly + resort fee + tax. Nightly rates are dynamic — exact target-date totals are blank/unverified and must be confirmed live on official booking pages.</p>'
      + '<p><b>Restaurants (2 adults):</b> exact where published (Anima by EDO ~$170, Michael Mina ~$590); otherwise Michelin price bands ($–$$$$).</p>'
      + '<p><b>Activities (2 adults):</b> O ~$324–398 · High Roller ~$80 · Neon Museum ~$42–70 · Conservatory/Fountains/Welcome Sign free · Sphere event-dependent.</p>'
      + '<p>Full breakdown on the <a href="pricing.html">pricing</a> page.</p></div>');

    block("sum-risks", '<h2 class="sec">Key risks &amp; caveats</h2><div class="callout warn"><ul>'
      + '<li><b>Dynamic hotel pricing</b> — exact Feb 15–22, 2027 totals not extractable; confirm live before booking.</li>'
      + '<li><b>Annual Michelin star cycle</b> — distinctions are the 2026 selection; reconfirm the 2027 guide before the trip.</li>'
      + '<li><b>'+unv+' restaurants</b> have unverified hours/location — confirm before planning specific days.</li>'
      + '<li><b>Michael Mina (Bellagio)</b> currently temporarily closed — verify open for trip dates.</li>'
      + '<li><b>Show dark days</b> — "O" runs Wed–Sun only; check calendars.</li>'
      + '<li><b>No subway</b> — all transit is bus/monorail; Downtown/Chinatown are 30–45 min from the Strip.</li>'
      + '</ul></div>');

    block("sum-open", '<h2 class="sec">Open questions</h2><p class="sub">See the <a href="suggestions.html">Suggestions</a> page for the full list of questions, assumptions, and the info needed before finalizing.</p>');
  });
})();
