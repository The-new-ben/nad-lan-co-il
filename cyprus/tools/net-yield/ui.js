/* CY-PRUS Instruments: net-yield UI. Mounts on every <section data-cyx-tool="net-yield">; the server already printed
   the worked example, so without JavaScript the page still shows real numbers. */
(function () {
  'use strict';
  var E = window.CYXNetYield;
  if (!E) { return; }

  function fmt(n) { return new Intl.NumberFormat('he-IL', { maximumFractionDigits: 0 }).format(n); }
  function iso(t) { return '⁦' + t + '⁩'; }
  function eur(n) { return iso('€' + fmt(n)); }
  function pct(x) { return (Math.round(x * 1000) / 10).toFixed(1) + '%'; }
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) { e.className = cls; } if (text !== undefined) { e.textContent = text; } return e; }
  function neg(n) { return n ? '−' + eur(n) : eur(0); }
  function digits(v) { return parseInt(String(v).replace(/[^0-9]/g, ''), 10) || 0; }

  function mount(root) {
    var rules = JSON.parse(root.getAttribute('data-rules'));
    var pcRules = JSON.parse(root.getAttribute('data-pc-rules'));
    var T = JSON.parse(root.getAttribute('data-text'));
    var s = JSON.parse(root.getAttribute('data-example'));
    var q = function (sel) { return root.querySelector(sel); };

    function setChips(name, value) {
      var c = root.querySelectorAll('[data-chip="' + name + '"]'), i;
      for (i = 0; i < c.length; i += 1) { c[i].setAttribute('aria-checked', String(c[i].getAttribute('data-value') === String(value))); }
    }
    function row(tb, key, amount, strong) {
      var tr = el('tr', strong ? 'cyx-row cyx-row--total' : 'cyx-row'), th = el('th', null, T.rows[key]), td = el('td', 'cyx-num');
      th.setAttribute('scope', 'row'); td.appendChild(el('bdi', null, amount));
      tr.appendChild(th); tr.appendChild(td); tr.appendChild(el('td', 'cyx-rule', T.rules_text[key])); tb.appendChild(tr);
    }
    function preset() {
      var c = rules.cities[s.city];
      s.price = c.price; s.rent = c.rent[s.beds];
      q('#cyx-ny-price').value = fmt(s.price); q('#cyx-ny-rent').value = fmt(s.rent);
      q('.cyx-example').hidden = false;
    }
    function render() {
      var r = E.netYield(s, rules, pcRules), tb = q('.cyx-break tbody');
      q('[data-out="yield"]').textContent = pct(r.netYieldLow) === pct(r.netYieldHigh) ? pct(r.netYieldLow) : pct(r.netYieldLow) + ' – ' + pct(r.netYieldHigh);
      q('[data-out="monthly"]').textContent = T.net_monthly.replace('{m}', eur(r.netMonthly)).replace('{s}', iso('₪' + fmt(r.netMonthly * rules.fx.eur_ils)));
      q('[data-out="gross"]').textContent = T.gross_line.replace('{g}', pct(r.grossYield));
      tb.textContent = '';
      row(tb, 'gross', eur(r.gross));
      row(tb, 'ghs', neg(r.ghs));
      row(tb, 'cy_tax', neg(r.cyTax));
      row(tb, 'expenses', neg(r.expenses));
      if (s.israelTrack) { row(tb, 'il_tax', neg(r.ilTax)); }
      row(tb, 'net', eur(r.net), true);
      row(tb, 'cost', r.totalLow === r.totalHigh ? eur(r.totalLow) : iso('€' + fmt(r.totalLow) + ' – €' + fmt(r.totalHigh)));
    }

    root.addEventListener('click', function (ev) {
      var chip = ev.target.closest('[data-chip]'), n, v;
      if (!chip) { return; }
      n = chip.getAttribute('data-chip'); v = chip.getAttribute('data-value');
      if (n === 'city') { s.city = v; preset(); }
      if (n === 'beds') { s.beds = v; preset(); }
      if (n === 'deal') { s.isNew = v === 'new'; }
      if (n === 'months') { s.months = parseInt(v, 10); }
      if (n === 'israel') { s.israelTrack = v === '15'; }
      setChips(n, v); render();
    });
    q('#cyx-ny-price').addEventListener('input', function (e) { var v = digits(e.target.value); if (v >= rules.ui.price_min) { s.price = Math.min(v, rules.ui.price_max); q('.cyx-example').hidden = true; render(); } });
    q('#cyx-ny-rent').addEventListener('input', function (e) { var v = digits(e.target.value); if (v >= rules.ui.rent_min) { s.rent = Math.min(v, rules.ui.rent_max); q('.cyx-example').hidden = true; render(); } });
    q('#cyx-ny-expenses').addEventListener('input', function (e) { s.expenses = digits(e.target.value); render(); });
    q('#cyx-ny-price').addEventListener('change', function (e) { e.target.value = fmt(s.price); });
    q('#cyx-ny-rent').addEventListener('change', function (e) { e.target.value = fmt(s.rent); });
    render();
  }

  function boot() {
    var n = document.querySelectorAll('[data-cyx-tool="net-yield"]'), i;
    for (i = 0; i < n.length; i += 1) { try { mount(n[i]); } catch (err) { /* fail open: the printed example stays */ } }
  }
  if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', boot); } else { boot(); }
}());
