/* CY-PRUS Instruments: 5% VAT eligibility UI. Mounts on <section data-cyx-tool="vat5">. */
(function () {
  'use strict';
  var E = window.CYXVat5;
  if (!E) { return; }

  function fmt(n) { return new Intl.NumberFormat('he-IL', { maximumFractionDigits: 0 }).format(n); }
  function eur(n) { return '⁦€' + fmt(n) + '⁩'; }
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) { e.className = cls; } if (text !== undefined) { e.textContent = text; } return e; }
  function digits(v) { return parseInt(String(v).replace(/[^0-9]/g, ''), 10) || 0; }
  var FAMILY = { none: [false, 0], disability: [true, 0], kids4: [false, 1], kids5: [false, 2] };

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
      var r = E.check(a, R), list = q('[data-out="checks"]'), i, c, li;
      q('[data-out="answer"]').textContent = r.eligible ? T.yes : T.no;
      q('[data-out="saving"]').textContent = r.eligible ? T.saving.replace('{s}', eur(r.saving)) : '';
      q('[data-out="saving"]').hidden = !r.eligible;
      q('[data-out="vat"]').textContent = T.vat_line.replace('{v}', eur(r.vat));
      q('[data-out="late"]').hidden = !(r.eligible && r.late);
      q('[data-out="how"]').textContent = T.how.replace('{m}', r.firstM2);
      list.textContent = '';
      for (i = 0; i < r.checks.length; i += 1) {
        c = r.checks[i];
        li = el('li', 'cyx-check ' + (c.pass ? 'cyx-check--ok' : (c.soft ? 'cyx-check--warn' : 'cyx-check--no')));
        li.appendChild(el('span', 'cyx-check__label', T.checks[c.key][0]));
        if (!c.pass || c.soft) { li.appendChild(el('span', 'cyx-check__why', T.checks[c.key][1])); }
        list.appendChild(li);
      }
    }
    root.addEventListener('click', function (ev) {
      var chip = ev.target.closest('[data-chip]'), n, v;
      if (!chip) { return; }
      n = chip.getAttribute('data-chip'); v = chip.getAttribute('data-value');
      if (n === 'family') { a.disability = FAMILY[v][0]; a.children = FAMILY[v][1]; } else { a[n] = v; }
      setChips(n, v); render();
    });
    q('#cyx-v5-price').addEventListener('input', function (e) { a.price = digits(e.target.value); render(); });
    q('#cyx-v5-area').addEventListener('input', function (e) { a.area = digits(e.target.value); render(); });
    q('#cyx-v5-price').addEventListener('change', function (e) { e.target.value = fmt(a.price); });
    render();
  }

  function boot() {
    var n = document.querySelectorAll('[data-cyx-tool="vat5"]'), i;
    for (i = 0; i < n.length; i += 1) { try { mount(n[i]); } catch (err) { /* fail open */ } }
  }
  if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', boot); } else { boot(); }
}());
