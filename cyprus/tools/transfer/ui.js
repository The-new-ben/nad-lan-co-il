/* CY-PRUS Instruments: transfer cost comparison UI. Mounts on <section data-cyx-tool="transfer">. */
(function () {
  'use strict';
  var E = window.CYXTransfer;
  if (!E) { return; }

  function fmt(n) { return new Intl.NumberFormat('he-IL', { maximumFractionDigits: 0 }).format(n); }
  function ils(n) { return '⁦₪' + fmt(n) + '⁩'; }
  function pct(x) { return (Math.round(x * 10000) / 100).toFixed(2) + '%'; }
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
      var r = E.compare(a, R), tb = q('.cyx-break tbody'), i, x, tr, th;
      q('[data-out="best"]').textContent = r.cheapest.name;
      q('[data-out="cheap"]').textContent = T.cheap_line.replace('{b}', r.cheapest.name).replace('{t}', ils(r.cheapest.total)).replace('{p}', pct(r.cheapest.pct));
      q('[data-out="spread"]').textContent = T.spread_line.replace('{d}', ils(r.dearest.total - r.cheapest.total));
      q('[data-out="base"]').textContent = T.base_line.replace('{s}', ils(r.ils));
      tb.textContent = '';
      for (i = 0; i < r.rows.length; i += 1) {
        x = r.rows[i]; tr = el('tr', i === 0 ? 'cyx-row cyx-row--total' : 'cyx-row');
        th = el('th', null, x.name); th.setAttribute('scope', 'row'); tr.appendChild(th);
        [x.total, x.transfer, x.conversion, x.incoming].forEach(function (v) { var td = el('td', 'cyx-num'); td.appendChild(el('bdi', null, ils(v))); tr.appendChild(td); });
        tb.appendChild(tr);
      }
    }
    root.addEventListener('click', function (ev) {
      var chip = ev.target.closest('[data-chip]'), n, v;
      if (!chip) { return; }
      n = chip.getAttribute('data-chip'); v = chip.getAttribute('data-value'); a[n] = v; setChips(n, v); render();
    });
    q('#cyx-tr-eur').addEventListener('input', function (e) { var v = digits(e.target.value); if (v >= 100) { a.eur = v; render(); } });
    q('#cyx-tr-eur').addEventListener('change', function (e) { e.target.value = fmt(a.eur); });
    render();
  }

  function boot() {
    var n = document.querySelectorAll('[data-cyx-tool="transfer"]'), i;
    for (i = 0; i < n.length; i += 1) { try { mount(n[i]); } catch (err) { /* fail open */ } }
  }
  if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', boot); } else { boot(); }
}());
