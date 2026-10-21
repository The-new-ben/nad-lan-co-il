/* CY-PRUS Instruments: residency-by-investment check UI. Mounts on <section data-cyx-tool="residency">. */
(function () {
  'use strict';
  var E = window.CYXResidency;
  if (!E) { return; }

  function fmt(n) { return new Intl.NumberFormat('he-IL', { maximumFractionDigits: 0 }).format(n); }
  function eur(n) { return '⁦€' + fmt(n) + '⁩'; }
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
      var r = E.check(a, R), list = q('[data-out="checks"]'), i, c, li, why;
      q('[data-out="answer"]').textContent = r.ok ? T.ok : T.no;
      q('[data-out="need"]').textContent = T.need_line.replace('{n}', eur(r.need)).replace('{v}', r.vatOnTop ? T.vat_suffix : '');
      q('[data-out="income"]').textContent = T.income_line.replace('{i}', eur(r.incomeNeed));
      q('[data-out="fees"]').textContent = T.fees_line.replace('{f}', eur(r.fees)).replace('{p}', r.people);
      q('[data-field="first"]').hidden = a.route !== 'home';
      q('[data-field="abroad"]').hidden = a.route !== 'home';
      list.textContent = '';
      for (i = 0; i < r.checks.length; i += 1) {
        c = r.checks[i];
        li = el('li', 'cyx-check ' + (c.pass ? 'cyx-check--ok' : 'cyx-check--no'));
        li.appendChild(el('span', 'cyx-check__label', T.checks[c.key][0]));
        if (!c.pass) {
          why = T.checks[c.key][1].replace('{g}', eur(c.key === 'amount' ? r.amountGap : r.incomeGap));
          li.appendChild(el('span', 'cyx-check__why', why));
        }
        list.appendChild(li);
      }
    }
    root.addEventListener('click', function (ev) {
      var chip = ev.target.closest('[data-chip]'), n, v;
      if (!chip) { return; }
      n = chip.getAttribute('data-chip'); v = chip.getAttribute('data-value');
      if (n === 'route') { a.route = v; }
      if (n === 'firstSale' || n === 'spouse' || n === 'abroad') { a[n] = v === 'yes'; }
      if (n === 'minors' || n === 'adults') { a[n] = parseInt(v, 10); }
      setChips(n, v); render();
    });
    q('#cyx-rs-amount').addEventListener('input', function (e) { a.amount = digits(e.target.value); render(); });
    q('#cyx-rs-income').addEventListener('input', function (e) { a.income = digits(e.target.value); render(); });
    q('#cyx-rs-amount').addEventListener('change', function (e) { e.target.value = fmt(a.amount); });
    q('#cyx-rs-income').addEventListener('change', function (e) { e.target.value = fmt(a.income); });
    render();
  }

  function boot() {
    var n = document.querySelectorAll('[data-cyx-tool="residency"]'), i;
    for (i = 0; i < n.length; i += 1) { try { mount(n[i]); } catch (err) { /* fail open */ } }
  }
  if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', boot); } else { boot(); }
}());
