/* CY-PRUS Instruments: Israel-Cyprus tax map UI. Mounts on <section data-cyx-tool="tax-map">.
   The event chips switch between the sale calculator and the two-country cards; all cards are printed by the server. */
(function () {
  'use strict';
  var E = window.CYXTaxMap;
  if (!E) { return; }

  function fmt(n) { return new Intl.NumberFormat('he-IL', { maximumFractionDigits: 0 }).format(n); }
  function eur(n) { return '⁦€' + fmt(n) + '⁩'; }
  function digits(v) { return parseInt(String(v).replace(/[^0-9]/g, ''), 10) || 0; }

  function mount(root) {
    var R = JSON.parse(root.getAttribute('data-rules'));
    var T = JSON.parse(root.getAttribute('data-text'));
    var a = JSON.parse(root.getAttribute('data-example'));
    var event = 'sale';
    var q = function (s) { return root.querySelector(s); };

    function setChips(name, value) {
      var c = root.querySelectorAll('[data-chip="' + name + '"]'), i;
      for (i = 0; i < c.length; i += 1) { c[i].setAttribute('aria-checked', String(c[i].getAttribute('data-value') === String(value))); }
    }
    function render() {
      var r = E.sale(a, R), cards = root.querySelectorAll('[data-event]'), i;
      for (i = 0; i < cards.length; i += 1) { cards[i].hidden = cards[i].getAttribute('data-event') !== event; }
      q('[data-out="total"]').textContent = eur(r.total);
      q('[data-out="net"]').textContent = T.net_line.replace('{n}', eur(r.net));
      q('[data-out="gain"]').textContent = T.gain_line.replace('{g}', eur(r.gain)).replace('{e}', eur(r.exemption));
      q('[data-row="cy"]').textContent = eur(r.cyTax);
      q('[data-row="fee"]').textContent = eur(r.fee);
      q('[data-row="il"]').textContent = eur(r.ilNet);
      q('[data-row="total"]').textContent = eur(r.total);
    }
    root.addEventListener('click', function (ev) {
      var chip = ev.target.closest('[data-chip]'), n, v;
      if (!chip) { return; }
      n = chip.getAttribute('data-chip'); v = chip.getAttribute('data-value');
      if (n === 'event') { event = v; }
      if (n === 'main' || n === 'used') { a[n] = v === 'yes'; }
      setChips(n, v); render();
    });
    ['buy', 'sell', 'costs'].forEach(function (k) {
      var inp = q('#cyx-tm-' + k);
      inp.addEventListener('input', function (e) { a[k] = digits(e.target.value); render(); });
      inp.addEventListener('change', function (e) { e.target.value = fmt(a[k]); });
    });
    render();
  }

  function boot() {
    var n = document.querySelectorAll('[data-cyx-tool="tax-map"]'), i;
    for (i = 0; i < n.length; i += 1) { try { mount(n[i]); } catch (err) { /* fail open */ } }
  }
  if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', boot); } else { boot(); }
}());
