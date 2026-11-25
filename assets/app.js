/* Vegas1 Trip Planner — rendering + helpers
   Reads the global DATA object (assets/data.js) and renders verified tables.
   No external dependencies; works on GitHub Pages (same-origin script tags). */
(function () {
  "use strict";

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }
  function link(url, label) {
    if (!url) return "";
    return '<a href="' + esc(url) + '" target="_blank" rel="noopener noreferrer">' + esc(label || url) + "</a>";
  }
  function srcCell(url, label) {
    if (!url) return '<span class="badge b-unverified">no source</span>';
    return '<span class="src">' + link(url, label || "source") + "</span>";
  }
  function badgeStar(n) {
    if (!n) return '<span class="badge b-listed">Guide listed</span>';
    return '<span class="badge b-star">★ Michelin Star (' + n + ")</span>";
  }
  function mediaCell(media) {
    if (!media || !media.length) return '<span class="note">—</span>';
    return '<div class="pill-row">' + media.map(function (m) {
      return '<a class="badge b-listed" href="' + esc(m.url) + '" target="_blank" rel="noopener noreferrer">' +
        esc(m.type) + "</a>";
    }).join("") + "</div>";
  }
  function verifiedBadge(v) {
    return v ? '<span class="badge b-ok">verified</span>' : '<span class="badge b-unverified">unverified</span>';
  }
  function hoursCell(h) {
    if (!h) return '<span class="note">—</span>';
    var days = h.days ? esc(h.days) : "—";
    var hrs = h.hours ? esc(h.hours) : "—";
    var ex = h.exceptions ? '<div class="note">Exceptions: ' + esc(h.exceptions) + "</div>" : "";
    return days + "<br><span class=\"note\">" + hrs + "</span>" + ex;
  }

  /* generic table renderer */
  function renderTable(container, columns, rows, opts) {
    opts = opts || {};
    var html = '<div class="table-scroll"><table><thead><tr>';
    columns.forEach(function (c) { html += "<th>" + esc(c.label) + "</th>"; });
    html += "</tr></thead><tbody>";
    if (!rows.length) {
      html += '<tr><td colspan="' + columns.length + '"><span class="note">No entries yet — data pending research.</span></td></tr>';
    }
    rows.forEach(function (r) {
      html += "<tr>";
      columns.forEach(function (c) {
        var val = r[c.key];
        var content;
        if (c.render) content = c.render(val, r);
        else if (typeof val === "boolean") content = val ? "Yes" : "No";
        else content = esc(val == null || val === "" ? "—" : val);
        html += "<td" + (c.cls ? ' class="' + c.cls + '"' : "") + ">" + content + "</td>";
      });
      html += "</tr>";
    });
    html += "</tbody></table></div>";
    container.innerHTML = html;
  }

  /* ---- Page renderers ---- */
  function pageRestaurants() {
    var el = document.getElementById("tbl-restaurants");
    if (!el) return;
    renderTable(el, [
      { label: "Restaurant", key: "name" },
      { label: "Michelin status", key: "status", render: function (v, r) { return badgeStar(r.stars); } },
      { label: "Cuisine / Area", key: "cuisine", render: function (v, r) { return esc(v || "—") + '<br><span class="note">' + esc(r.area || "—") + "</span>"; } },
      { label: "Hours / Days", key: "hours", render: hoursCell },
      { label: "Cost (2 adults, total)", key: "priceForTwo" },
      { label: "Media", key: "media", render: mediaCell },
      { label: "Source", key: "source", render: function (v, r) {
          return srcCell(r.michelin, "Michelin Guide") + '<br>' + srcCell(r.source, "Official site"); } },
      { label: "Check", key: "verified", render: verifiedBadge }
    ], DATA.restaurants || []);
  }

  function pageHotels() {
    var el = document.getElementById("tbl-hotels");
    if (!el) return;
    renderTable(el, [
      { label: "Rank", key: "rank", cls: "num" },
      { label: "Hotel", key: "name" },
      { label: "Area", key: "area" },
      { label: "Bed / Bath", key: "bedBath", render: function (v, r) {
          return (r.queenBed ? "Queen+" : "—") + " bed<br>" + (r.privateBath ? "Private bath" : "—"); } },
      { label: "Michelin rest. (on-site / ≤1h)", key: "michelinCount", cls: "num", render: function (v, r) {
          return esc(r.onSiteCount == null ? "—" : r.onSiteCount) + ' on-site<br><span class="note">' + esc(r.within1h == null ? "—" : r.within1h) + " ≤ 1h</span>"; } },
      { label: "Nightly (actual dates)", key: "nightly" },
      { label: "Total 7-night", key: "total7" },
      { label: "Best booking window", key: "bookWindow" },
      { label: "Amenities", key: "amenities", render: function (v) { return (v || []).join(", ") || "—"; } },
      { label: "Source", key: "source", render: function (v) { return srcCell(v); } },
      { label: "Check", key: "verified", render: verifiedBadge }
    ], DATA.hotels || []);
  }

  function pageActivities() {
    var el = document.getElementById("tbl-activities");
    if (!el) return;
    renderTable(el, [
      { label: "Activity", key: "name" },
      { label: "Type", key: "type" },
      { label: "Area", key: "area" },
      { label: "Travel from hotel", key: "travel" },
      { label: "Hours / Days", key: "hours", render: hoursCell },
      { label: "Media", key: "media", render: mediaCell },
      { label: "Source", key: "source", render: function (v) { return srcCell(v); } },
      { label: "Check", key: "verified", render: verifiedBadge }
    ], DATA.activities || []);
  }

  function pagePricing() {
    var el = document.getElementById("tbl-pricing");
    if (!el) return;
    renderTable(el, [
      { label: "Item", key: "item" },
      { label: "Category", key: "category" },
      { label: "Details", key: "details" },
      { label: "Price (total)", key: "price" },
      { label: "Dates / window", key: "window" },
      { label: "Source", key: "source", render: function (v) { return srcCell(v); } },
      { label: "Check", key: "verified", render: verifiedBadge }
    ], DATA.pricing || []);
  }

  function pageVerification() {
    var el = document.getElementById("tbl-verification");
    if (!el) return;
    renderTable(el, [
      { label: "Claim / Value", key: "claim" },
      { label: "Status", key: "status", render: function (v) {
          var map = { verified: '<span class="badge b-ok">verified</span>', unverified: '<span class="badge b-unverified">unverified</span>', flagged: '<span class="badge b-warn">flagged</span>' };
          return map[v] || esc(v); } },
      { label: "Official source", key: "source", render: function (v) { return srcCell(v); } },
      { label: "Notes", key: "notes" }
    ], DATA.verification || []);
  }

  function initNav() {
    var path = location.pathname.split("/").pop() || "index.html";
    document.querySelectorAll("nav.tabs a").forEach(function (a) {
      var href = a.getAttribute("href");
      if (href === path || (path === "" && href === "index.html")) a.classList.add("active");
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    initNav();
    pageRestaurants(); pageHotels(); pageActivities(); pagePricing(); pageVerification();
  });

  // expose for debugging
  window.VegasUI = { renderTable: renderTable, esc: esc };
})();
