/* CY-PRUS Instruments: Cyprus price list UI. Mounts on <section data-cyx-tool="price-list">. */
(function () {
  'use strict';
  var E = window.CYXPriceList;
  if (!E) { return; }

  function fmt(n) { return new Intl.NumberFormat('he-IL', { maximumFractionDigits: 0 }).format(n); }
  function eur(n) { return '⁦€' + fmt(n) + '⁩'; }
  function sgn(y) { return '⁦' + (y > 0 ? '+' : '') + y + '%⁩'; }
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) { e.className = cls; } if (text !== undefined) { e.textContent = text; } return e; }
  function digits(v) { return parseInt(String(v).replace(/[^0-9]/g, ''), 10) || 0; }

  function mount(root) {
    var R = JSON.parse(root.getAttribute('data-rules'));
    var T = JSON.parse(root.getAttribute('data-text'));
    var a = JSON.parse(root.getAttribute('data-example'));
    var q = function (s) { return root.querySelector(s); };

    function setChips(name, value) {
      var c = root.querySelectorAll('[data-chip="' + name + '"]'), i;
      for (i = 0; i < c.length; i += 1) { c[i].setAttribute('aria-checked', String(c[i].getAttribute('data-value') === String(value))); }
    }
    function render() {
      var r = E.lookup(a, R), me = r.me, tb = q('.cyx-break tbody'), i, x, tr, th, cells;
      q('[data-out="median"]').textContent = eur(me.median);
      q('[data-out="m2"]').textContent = me.m2 ? T.m2_line.replace('{m}', eur(me.m2)) : T.m2_none;
      q('[data-out="ask"]').textContent = T.ask_line.replace('{a}', eur(me.asking));
      q('[data-out="yoy"]').textContent = T.yoy_line.replace('{y}', sgn(me.yoy));
      q('[data-out="size"]').textContent = !a.size ? '' : (r.bySizeDeals
        ? T.size_line.replace('{s}', a.size).replace('{d}', eur(r.bySizeDeals)).replace('{k}', eur(r.bySizeAsking))
        : T.size_line_new.replace('{s}', a.size).replace('{k}', eur(r.bySizeAsking)));
      q('[data-out="size"]').hidden = !a.size;
      tb.textContent = '';
      for (i = 0; i < r.table.length; i += 1) {
        x = r.table[i]; tr = el('tr', x.id === a.city ? 'cyx-row cyx-row--total' : 'cyx-row');
        th = el('th', null, T.cities[x.id]); th.setAttribute('scope', 'row'); tr.appendChild(th);
        cells = [eur(x.r.median), x.r.m2 ? eur(x.r.m2) : '—', eur(x.r.asking), sgn(x.r.yoy), fmt(x.r.contracts)];
        cells.forEach(function (v) { var td = el('td', 'cyx-num'); td.appendChild(el('bdi', null, v)); tr.appendChild(td); });
        tb.appendChild(tr);
      }
    }
    root.addEventListener('click', function (ev) {
      var chip = ev.target.closest('[data-chip]'), n, v;
      if (!chip) { return; }
      n = chip.getAttribute('data-chip'); v = chip.getAttribute('data-value'); a[n] = v; setChips(n, v); render();
    });
    q('#cyx-pl-size').addEventListener('input', function (e) { a.size = digits(e.target.value); render(); });
    render();
  }

  function boot() {
    var n = document.querySelectorAll('[data-cyx-tool="price-list"]'), i;
    for (i = 0; i < n.length; i += 1) { try { mount(n[i]); } catch (err) { /* fail open */ } }
  }
  if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', boot); } else { boot(); }
}());
