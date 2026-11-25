/* Executive summary renderer — filled with verified findings after research. */
(function () {
  "use strict";
  function esc(s){return String(s==null?"":s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");}
  function block(id, html){var el=document.getElementById(id); if(el) el.innerHTML=html;}
  function ul(items){return "<ul>"+items.map(function(i){return "<li>"+esc(i)+"</li>";}).join("")+"</ul>";}
  document.addEventListener("DOMContentLoaded", function(){
    block("sum-trip", '<div class="callout"><h3>Trip parameters</h3><p>Destination Las Vegas, NV · 2 adults · 7-night base stay (1–2 weeks) · window Feb 15 – Mar 23, 2027 · preferred Feb 15–18, 2027.</p></div>');
    block("sum-hotel", '<h2 class="sec">Recommended stay</h2><p class="sub">Filled after hotel ranking research.</p><div class="callout">Pending research.</div>');
    block("sum-dining", '<h2 class="sec">Michelin dining</h2><p class="sub">Filled after restaurant research.</p><div class="callout">Pending research.</div>');
    block("sum-activities", '<h2 class="sec">Activities</h2><p class="sub">Filled after activity research.</p><div class="callout">Pending research.</div>');
    block("sum-pricing", '<h2 class="sec">Pricing snapshot</h2><p class="sub">Filled after pricing research.</p><div class="callout">Pending research.</div>');
    block("sum-risks", '<h2 class="sec">Key risks &amp; caveats</h2><div class="callout warn"><p>Dynamic pricing; annual Michelin star cycle; show dark days; verify hours before visiting.</p></div>');
    block("sum-open", '<h2 class="sec">Open questions</h2><p class="sub">See the <a href="suggestions.html">Suggestions</a> page for the full list.</p>');
  });
})();
