/* Vegas1 — shared site behavior: mobile nav toggle + active link marking.
   No frameworks, no external calls. Works on static GitHub Pages. */
(function () {
  "use strict";

  // Mark the current page in the nav by matching the filename.
  var path = (location.pathname.split("/").pop() || "index.html").toLowerCase();
  if (path === "" || path === "index.html" || path === "index.htm") path = "index.html";
  document.querySelectorAll("nav.mainnav a").forEach(function (a) {
    var href = (a.getAttribute("href") || "").split("/").pop().toLowerCase();
    if (href === path) a.classList.add("active");
  });

  // Simple mobile nav toggle (collapses to a wrap row already; kept for future use).
  function toggleNav() {
    var nav = document.querySelector("nav.mainnav");
    if (!nav) return;
    nav.classList.toggle("is-open");
  }
  var t = document.getElementById("navToggle");
  if (t) t.addEventListener("click", toggleNav);

  // Ensure every external link opens safely and gets a visible affordance.
  document.querySelectorAll('a[href^="http"]').forEach(function (a) {
    a.setAttribute("target", "_blank");
    a.setAttribute("rel", "noopener noreferrer");
  });

  // Accessibility: skip link target for tables.
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener("click", function (e) {
      var el = document.querySelector(a.getAttribute("href"));
      if (el) { e.preventDefault(); el.scrollIntoView({ behavior: "smooth", block: "start" }); }
    });
  });
})();
