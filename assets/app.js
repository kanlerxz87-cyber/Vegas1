// Minimal progressive-enhancement helpers (no dependencies).
(function () {
  // Close mobile nav after navigating
  document.addEventListener('click', function (e) {
    var nav = document.getElementById('mainnav');
    if (!nav) return;
    var t = e.target.closest('a');
    if (t && nav.contains(t)) { nav.classList.remove('open'); }
  });

  // Mark active nav link based on current path
  var path = (location.pathname.split('/').pop() || 'index.html').toLowerCase();
  document.querySelectorAll('nav.main a').forEach(function (a) {
    var href = (a.getAttribute('href') || '').toLowerCase();
    if (href === path) a.classList.add('active');
  });
})();
