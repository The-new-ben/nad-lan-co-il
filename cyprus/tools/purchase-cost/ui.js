/* CY-PRUS Instruments: purchase-cost UI. Mounts on every <section data-cyx-tool="purchase-cost">.
   Reads the rules and texts the server printed into the section (data-rules / data-text, JSON), so the
   server-rendered example stays readable without JavaScript and the script only takes over the controls. */
(function () {
  'use strict';
  var E = window.CYXPurchaseCost;
  if (!E) { return; }

  function fmt(n, lang) { return new Intl.NumberFormat(lang === 'en' ? 'en-GB' : 'he-IL', { maximumFractionDigits: 0 }).format(n); }
  function eur(n, lang) { return '€' + fmt(n, lang); }
  function ils(n, lang) { return '₪' + fmt(n, lang); }
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) { e.className = cls; } if (text !== undefined) { e.textContent = text; } return e; }
  function iso(t) { return '⁦' + t + '⁩'; }
  function range(lo, hi, lang) { return iso(lo === hi ? eur(lo, lang) : eur(lo, lang) + ' – ' + eur(hi, lang)); }

  function mount(root) {
    var rules = JSON.parse(root.getAttribute('data-rules'));
    var T = JSON.parse(root.getAttribute('data-text'));
    var lang = root.getAttribute('data-lang') || 'he';
    var state = JSON.parse(root.getAttribute('data-example'));
    var q = function (sel) { return root.querySelector(sel); };

    function setChips(name, value) {
      var chips = root.querySelectorAll('[data-chip="' + name + '"]'), i;
      for (i = 0; i < chips.length; i += 1) {
        chips[i].setAttribute('aria-checked', String(chips[i].getAttribute('data-value') === String(value)));
      }
    }

    function row(tbody, label, amountText, rule, kind) {
      var tr = el('tr', kind === 'market' ? 'cyx-row cyx-row--market' : 'cyx-row');
      var th = el('th', null, label); th.setAttribute('scope', 'row');
      var td = el('td', 'cyx-num'); td.appendChild(el('bdi', null, amountText));
      var tr2 = el('td', 'cyx-rule', rule);
      tr.appendChild(th); tr.appendChild(td); tr.appendChild(tr2); tbody.appendChild(tr);
    }

    function render() {
      var r = E.purchaseCost(state, rules), tb = q('.cyx-break tbody'), i, m, pct;
      q('[data-out="extra"]').textContent = range(r.extraLow, r.extraHigh, lang);
      pct = Math.round((r.extraLow / r.price) * 1000) / 10;
      q('[data-out="pct"]').textContent = T.pct.replace('{p}', fmt(pct, lang));
      q('[data-out="total"]').textContent = T.total.replace('{t}', range(r.totalLow, r.totalHigh, lang));
      q('[data-out="ils"]').textContent = T.ils.replace('{s}', iso(ils(r.extraLow * rules.fx.eur_ils, lang))).replace('{d}', rules.fx.date);
      tb.textContent = '';
      row(tb, T.rows.vat, eur(r.vat.amount, lang), T.vat_rule[r.vat.mode], 'law');
      row(tb, T.rows.transfer, eur(r.transfer.amount, lang), T.transfer_rule[r.transfer.mode], 'law');
      if (rules.stamp_duty && rules.stamp_duty.active) { row(tb, T.rows.stamp, eur(r.stamp.amount, lang), T.stamp_rule, 'law'); }
      if (state.mortgage) { row(tb, T.rows.mortgage, eur(r.mortgageReg.amount, lang), T.mortgage_rule, 'law'); }
      for (i = 0; i < r.fixedFees.length; i += 1) { row(tb, T.rows[r.fixedFees[i].key], eur(r.fixedFees[i].amount, lang), T.fixed_rule[r.fixedFees[i].key], 'law'); }
      for (i = 0; i < r.market.length; i += 1) {
        m = r.market[i];
        row(tb, T.market[m.key].label, range(m.low, m.high, lang), T.market[m.key].rule, 'market');
      }
      q('[data-field="vat"]').hidden = !state.isNew;
      q('[data-field="area"]').hidden = !(state.isNew && state.reducedVat);
      q('[data-field="mortgage-amount"]').hidden = !state.mortgage;
      q('.cyx-example').hidden = touched;
    }
    var touched = false;
    root.addEventListener('input', function () { touched = true; }, true);
    root.addEventListener('click', function (ev) { if (ev.target.closest('[data-chip]')) { touched = true; } }, true);

    function syncPrice(v) {
      state.price = Math.max(rules.ui.price_min, Math.min(rules.ui.price_max, v || 0));
      q('#cyx-pc-price').value = fmt(state.price, 'en');
      q('#cyx-pc-price-range').value = state.price;
      if (state.mortgage) {
        state.mortgage = Math.round(state.price * state.ltv);
        q('[data-out="mortgage"]').textContent = eur(state.mortgage, lang);
      }
    }

    root.addEventListener('click', function (ev) {
      var chip = ev.target.closest('[data-chip]'), name, val;
      if (!chip) { return; }
      name = chip.getAttribute('data-chip'); val = chip.getAttribute('data-value');
      if (name === 'deal') { state.isNew = val === 'new'; if (!state.isNew) { state.reducedVat = false; setChips('vat', 'standard'); } }
      if (name === 'vat') { state.reducedVat = val === 'reduced'; }
      if (name === 'buyers') { state.buyers = parseInt(val, 10); }
      if (name === 'mortgage') { state.mortgage = val === 'yes' ? Math.round(state.price * state.ltv) : 0; q('[data-out="mortgage"]').textContent = eur(state.mortgage, lang); }
      setChips(name, val);
      render();
    });
    q('#cyx-pc-price').addEventListener('change', function (e) { syncPrice(parseInt(String(e.target.value).replace(/[^0-9]/g, ''), 10)); render(); });
    q('#cyx-pc-price').addEventListener('input', function (e) { var v = parseInt(String(e.target.value).replace(/[^0-9]/g, ''), 10); if (v >= rules.ui.price_min) { state.price = Math.min(rules.ui.price_max, v); q('#cyx-pc-price-range').value = state.price; render(); } });
    q('#cyx-pc-price-range').addEventListener('input', function (e) { syncPrice(parseInt(e.target.value, 10)); render(); });
    q('#cyx-pc-area').addEventListener('input', function (e) { state.area = parseInt(e.target.value, 10) || 0; render(); });
    q('#cyx-pc-ltv').addEventListener('input', function (e) {
      state.ltv = parseInt(e.target.value, 10) / 100;
      state.mortgage = Math.round(state.price * state.ltv);
      q('[data-out="mortgage"]').textContent = eur(state.mortgage, lang);
      q('[data-out="ltv"]').textContent = e.target.value + '%';
      render();
    });
    render();
  }

  function boot() {
    var nodes = document.querySelectorAll('[data-cyx-tool="purchase-cost"]'), i;
    for (i = 0; i < nodes.length; i += 1) {
      try { mount(nodes[i]); } catch (err) { /* fail open: the server-rendered example stays */ }
    }
  }
  if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', boot); } else { boot(); }
}());
