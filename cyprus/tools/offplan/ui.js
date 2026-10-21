/* CY-PRUS Instruments: off-plan payment schedule UI. Mounts on <section data-cyx-tool="offplan">. */
(function () {
  'use strict';
  var E = window.CYXOffplan;
  if (!E) { return; }

  function fmt(n) { return new Intl.NumberFormat('he-IL', { maximumFractionDigits: 0 }).format(n); }
  function eur(n) { return '⁦€' + fmt(n) + '⁩'; }
  function ils(n) { return '⁦₪' + fmt(n) + '⁩'; }
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) { e.className = cls; } if (text !== undefined) { e.textContent = text; } return e; }
  function digits(v) { return parseInt(String(v).replace(/[^0-9]/g, ''), 10) || 0; }

  function mount(root) {
    var R = JSON.parse(root.getAttribute('data-rules'));
    var T = JSON.parse(root.getAttribute('data-text'));
    var a = JSON.parse(root.getAttribute('data-example'));
    var q = function (s) { return root.querySelector(s); };
    var pctInputs = root.querySelectorAll('[data-pct]');

    function setChips(name, value) {
      var c = root.querySelectorAll('[data-chip="' + name + '"]'), i;
      for (i = 0; i < c.length; i += 1) { c[i].setAttribute('aria-checked', String(c[i].getAttribute('data-value') === String(value))); }
    }
    function render() {
      var r = E.schedule(a, R), tb = q('.cyx-break tbody'), i, x, tr, th, note = q('[data-out="sum"]');
      q('[data-out="total"]').textContent = eur(r.total);
      q('[data-out="ils"]').textContent = T.ils_line.replace('{s}', ils(r.ils)).replace('{d}', R.fx.date);
      q('[data-out="shock"]').textContent = T.shock_line.replace('{s}', ils(r.ilsShock)).replace('{x}', ils(r.ilsShock - r.ils));
      note.hidden = r.ok; note.textContent = T.sum_bad.replace('{p}', r.sum);
      tb.textContent = '';
      for (i = 0; i < r.rows.length; i += 1) {
        x = r.rows[i];
        if (!x.pct) { continue; }
        tr = el('tr', i === r.releaseAt ? 'cyx-row cyx-row--total' : 'cyx-row');
        th = el('th', null, T.stages[x.stage]); th.setAttribute('scope', 'row'); tr.appendChild(th);
        [x.pct + '%', eur(x.eur), ils(x.ils), ils(x.ilsShock)].forEach(function (v) { var td = el('td', 'cyx-num'); td.appendChild(el('bdi', null, v)); tr.appendChild(td); });
        tb.appendChild(tr);
        if (i === r.releaseAt) {
          tr = el('tr', 'cyx-row cyx-row--note'); th = el('td', 'cyx-rule', T.release); th.setAttribute('colspan', '5'); tr.appendChild(th); tb.appendChild(tr);
        }
      }
    }
    function setPlan(v) {
      var i; a.plan = v; a.pcts = R.plans[v].slice();
      for (i = 0; i < pctInputs.length; i += 1) { pctInputs[i].value = a.pcts[i]; }
    }
    root.addEventListener('click', function (ev) {
      var chip = ev.target.closest('[data-chip]'), n, v;
      if (!chip) { return; }
      n = chip.getAttribute('data-chip'); v = chip.getAttribute('data-value');
      if (n === 'plan') { setPlan(v); } else { a[n] = v; }
      setChips(n, v); render();
    });
    Array.prototype.forEach.call(pctInputs, function (inp) {
      inp.addEventListener('input', function (e) { a.pcts[parseInt(e.target.getAttribute('data-pct'), 10)] = digits(e.target.value); render(); });
    });
    q('#cyx-op-price').addEventListener('input', function (e) { a.price = digits(e.target.value); render(); });
    q('#cyx-op-price').addEventListener('change', function (e) { e.target.value = fmt(a.price); });
    render();
  }

  function boot() {
    var n = document.querySelectorAll('[data-cyx-tool="offplan"]'), i;
    for (i = 0; i < n.length; i += 1) { try { mount(n[i]); } catch (err) { /* fail open */ } }
  }
  if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', boot); } else { boot(); }
}());
