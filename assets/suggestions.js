/* Suggestions & open questions renderer — decision-support content. */
(function () {
  "use strict";
  function esc(s){return String(s==null?"":s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");}
  function block(id, html){var el=document.getElementById(id); if(el) el.innerHTML=html;}

  document.addEventListener("DOMContentLoaded", function () {
    var questions = [
      { q: "Final travel dates?", why: "Rates and show schedules are date-specific; the 1–2 week window has a big impact on price.", how: "Confirm the exact 7-night check-in/check-out dates, then re-pull live hotel + show pricing for those dates." },
      { q: "Budget ceiling for lodging?", why: "Hotel ranking is density-first; a hard budget can override the top-ranked hotel.", how: "Set a max 7-night total; filter the Hotel page to stays under it." },
      { q: "Dining priority — starred vs. guide-listed?", why: "Starred restaurants are pricier and book out early; guide-listed options are more flexible.", how: "Decide whether to anchor the trip on starred tasting menus or mix in guide-listed spots." },
      { q: "Confirm Michelin star cycle timing?", why: "Stars are reassigned annually; a restaurant's status near Feb–Mar 2027 may differ from the latest listing.", how: "Check guide.michelin.com for the current Las Vegas selection and any announcement timing before booking." },
      { q: "Transit assumptions valid?", why: "The 1-hour rule uses bus/monorail; rideshare/walking changes the reachable set.", how: "Confirm the traveler will use public transit; if using rideshare, recompute the 1-hour radius." },
      { q: "Resort/destination fees included?", why: "Many Strip hotels add mandatory nightly fees not in the base room rate.", how: "Verify each hotel's mandatory fee schedule on its official booking page and add to the 7-night total." },
      { q: "Show/activity bookings needed?", why: "Popular shows sell out; dark days affect scheduling.", how: "List must-see shows and check availability + dark days on official ticketing pages." }
    ];
    var qHtml = "<div class='table-scroll'><table><thead><tr><th>Question</th><th>Why it matters</th><th>How to resolve</th></tr></thead><tbody>" +
      questions.map(function (o) {
        return "<tr><td><b>" + esc(o.q) + "</b></td><td>" + esc(o.why) + "</td><td>" + esc(o.how) + "</td></tr>";
      }).join("") + "</tbody></table></div>";
    block("q-list", qHtml);

    block("have-dont",
      '<div class="card"><div class="k">What we have</div><p>Verified Michelin restaurant list (starred + listed), hotel ranking method, activity shortlist with hours, and a line-by-line source audit.</p></div>' +
      '<div class="card"><div class="k">What we don\'t have</div><p>Live booking-engine rates for the exact 2027 dates (dynamic), confirmed 2027 Michelin star assignments, and show-date availability for the full window.</p></div>' +
      '<div class="card"><div class="k">Assumptions</div><p>Public transit (bus/monorail) for the 1-hour rule; 2 adults; one shared queen+ room with private bath; base 7-night stay.</p></div>' +
      '<div class="card"><div class="k">Dependencies</div><p>Annual Michelin cycle, dynamic pricing, and show calendars — all change over time and need re-verification.</p></div>');

    var sug = [
      { t: "Add a live price-check button", d: "Link each hotel/restaurant row to its official booking/menu page with a one-tap 'check live price' so decision-makers see current rates without leaving the dashboard.", pri: "High" },
      { t: "Interactive 1-hour transit map", d: "A map overlay showing Michelin restaurants and activities reachable within 1 hour from a chosen hotel, so the density ranking is visual and intuitive.", pri: "High" },
      { t: "Filter & sort controls", d: "Let users sort hotels by price, Michelin count, or star rating and filter by area/budget — improves decision-making vs. a static ranked list.", pri: "High" },
      { t: "Saved shortlist / compare", d: "Let a reviewer pin a few hotels/restaurants and compare them side-by-side before choosing.", pri: "Medium" },
      { t: "Trip itinerary builder", d: "Auto-generate a day-by-day plan grouping activities and restaurants by area and travel time.", pri: "Medium" },
      { t: "Cost calculator", d: "Sum 7-night lodging + planned dining + activities for the couple with a per-day breakdown.", pri: "Medium" },
      { t: "Source-confidence badges", d: "Keep the verified/unverified badges and add 'last-checked' dates so reviewers know freshness.", pri: "Low" }
    ];
    var sugHtml = "<div class='table-scroll'><table><thead><tr><th>Priority</th><th>Suggestion</th><th>Why it helps</th></tr></thead><tbody>" +
      sug.map(function (o) {
        return "<tr><td><span class='badge " + (o.pri === "High" ? "b-star" : (o.pri === "Medium" ? "b-listed" : "b-ok")) + "'>" + esc(o.pri) + "</span></td><td><b>" + esc(o.t) + "</b><br><span class='note'>" + esc(o.d) + "</span></td></tr>";
      }).join("") + "</tbody></table></div>";
    block("sug-list", sugHtml);

    var discover = [
      { t: "Pull exact-date hotel rates", d: "Use each hotel's official booking engine for the chosen 2027 dates to capture the true 7-night total including mandatory fees." },
      { t: "Confirm the Michelin Las Vegas selection", d: "Re-check guide.michelin.com for the current Las Vegas starred/listed set and note the inspection-cycle announcement date." },
      { t: "Capture restaurant menu prices", d: "Open each restaurant's official menu/tasting-menu page to get per-person pricing and compute the two-adult total." },
      { t: "Verify show calendars", d: "Check each show's official ticketing page for the Feb–Mar 2027 calendar, dark days, and any blackout dates." },
      { t: "Record transit trip times", d: "Use the RTC trip planner / monorail schedule to document actual one-way travel times used for the 1-hour rule." }
    ];
    var dHtml = "<div class='table-scroll'><table><thead><tr><th>Missing info</th><th>How to discover it (official source)</th></tr></thead><tbody>" +
      discover.map(function (o) {
        return "<tr><td><b>" + esc(o.t) + "</b></td><td>" + esc(o.d) + "</td></tr>";
      }).join("") + "</tbody></table></div>";
    block("discover-list", dHtml);
  });
})();
