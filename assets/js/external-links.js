// Make external links open in a new tab, safely.
// External = an http(s) link whose host differs from this site's host.
// Relative links, in-page anchors, mailto:, and same-host links are left alone.
(function () {
  function harden() {
    var here = window.location.host;
    var links = document.querySelectorAll('a[href]');
    for (var i = 0; i < links.length; i++) {
      var a = links[i];
      var href = a.getAttribute('href') || '';
      if (!/^https?:\/\//i.test(href)) continue; // skip relative / anchors / mailto
      if (!a.host || a.host === here) continue;   // skip internal (same-host) links
      a.target = '_blank';
      var rel = (a.getAttribute('rel') || '').split(/\s+/).filter(Boolean);
      if (rel.indexOf('noopener') === -1) rel.push('noopener');
      if (rel.indexOf('noreferrer') === -1) rel.push('noreferrer');
      a.setAttribute('rel', rel.join(' '));
    }
  }
  if (document.readyState !== 'loading') harden();
  else document.addEventListener('DOMContentLoaded', harden);
})();
