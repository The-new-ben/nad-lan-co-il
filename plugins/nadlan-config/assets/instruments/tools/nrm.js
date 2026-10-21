/* NadLan Instruments · nrm v1 (HAD-575, Kikar HaMedina tools program #5, Ben 15.10 + 21.10.2026): an Israeli mortgage for a
   buyer who lives abroad, in English. The loan is capped at 50% of the value (Bank of Israel directive 329 for non-residents);
   the monthly payment (equal payments, Spitzer) at the average rate of new mortgages by track; the purchase tax on the
   foreign-resident brackets (ptax.json); lawyer with VAT, appraiser and the file fee; the cash to close and the payment in
   dollars, euros or pounds at the Bank of Israel representative rate (boi-fx.json), with the last 30 days' range.
   English only: the registry entry carries only => en. Pure logic in NLNR for unit checks. */
(function () {
  'use strict';
  function pay(P, annual, months) { var r = annual / 100 / 12; return r === 0 ? P / months : P * r / (1 - Math.pow(1 + r, -months)); }
  function ptax(price, br) { var t = 0, lo = 0; for (var i = 0; i < br.length; i++) { var hi = br[i][0] == null ? Infinity : br[i][0], top = Math.min(price, hi); if (top > lo) t += (top - lo) * br[i][1]; if (price <= hi) break; lo = hi; } return t; }
  function compute(v, P, N) {
    var loan = v.price * Math.min(v.ltv, 100) / 100, n = Math.round(v.years * 12), m = pay(loan, v.rate, n);
    var tax = ptax(v.price, P.tracks.foreign), lawyer = v.price * (v.lawyer || 0) / 100 * (1 + N.vat);
    var fee = loan > 0 ? Math.min(loan * N.mortgage_fee.rate, N.mortgage_fee.max) : 0, appr = loan > 0 ? N.appraiser : 0;
    var cash = v.price - loan + tax + lawyer + fee + appr;
    return { loan: loan, n: n, monthly: m, interest: m * n - loan, tax: tax, lawyer: lawyer, fee: fee, appr: appr, cash: cash, over: v.ltv / 100 > N.ltv_max + 1e-9 };
  }
  window.NLNR = { pay: pay, ptax: ptax, compute: compute };
  if (!window.NadLanInstruments) return;
  var SYM = { USD: '$', EUR: '€', GBP: '£' };
  var nf = new Intl.NumberFormat('en-US', { maximumFractionDigits: 0 });
  function ils(x) { return '₪' + nf.format(Math.round(x)); }
  function fc(x, cur, fx) { return SYM[cur] + nf.format(Math.round(x / fx.fx[cur].rate)); }
  window.NadLanInstruments.register('nrm', {
    kicker: 'Calculator · Israeli mortgage',
    title: 'What an Israeli mortgage costs you from abroad',
    lede: 'The price of the home, your currency and the loan: the calculator caps the loan at 50% of the value as Israeli banks must for non-residents, works out the monthly payment, adds the purchase tax a foreign resident pays and the closing costs, and shows it all in your currency at the Bank of Israel rate.',
    strip: function (d) { var f = d.fx.fx; return [{ label: 'USD/ILS, ' + f.USD.date, value: String(f.USD.rate) }, { label: 'EUR/ILS', value: String(f.EUR.rate) }, { label: 'GBP/ILS', value: String(f.GBP.rate) }, { label: 'Max loan, non-resident', value: Math.round(100 * d.nrm.ltv_max) + '%' }]; },
    exampleNote: 'The calculator opens with an example. Change any number and the result updates.',
    defaults: function (d) { return { price: 4000000, cur: 'USD', ltv: 50, years: 25, track: 'fixed', rate: d.nrm.rates[0].rate, lawyer: 0.5 }; },
    fields: [
      { id: 'price', label: 'Price of the home', type: 'money', unit: '₪' },
      { id: 'cur', label: 'Your currency', type: 'segmented', options: [{ value: 'USD', label: 'US dollar' }, { value: 'EUR', label: 'Euro' }, { value: 'GBP', label: 'Pound' }] },
      { id: 'ltv', label: 'Loan as a share of the price', type: 'percent', unit: '%', help: 'Israeli banks lend a non-resident up to 50% of the value.' },
      { id: 'years', label: 'Years', type: 'number', unit: 'years' },
      { id: 'track', label: 'Mortgage track', type: 'select', optionsFrom: function (v, d) { return d.nrm.rates.map(function (r) { return { value: r.id, label: r.label + ' · avg ' + r.rate + '%' }; }); } },
      { id: 'rate', label: 'Interest rate', type: 'percent', unit: '%', help: 'Opens at the average for the track you pick. Your bank\'s offer may differ.' },
      { id: 'lawyer', label: 'Lawyer, before VAT', type: 'percent', unit: '%', help: 'Usually 0.5% to 1% of the price, plus 18% VAT.' }
    ],
    onField: function (id, v, d, redraw) { if (id === 'track') { d.nrm.rates.forEach(function (r) { if (r.id === v.track) v.rate = r.rate; }); redraw('rate'); } },
    compute: function (v, d) {
      var P = d.ptax, N = d.nrm, FX = d.fx, cur = FX.fx[v.cur] ? v.cur : 'USD';
      if (!(v.price >= 300000 && v.price <= 500000000)) return { error: { field: 'price', msg: 'Type the price in shekels.' } };
      if (!(v.ltv >= 0 && v.ltv < 100)) return { error: { field: 'ltv', msg: 'Between 0% and 50% for a non-resident.' } };
      if (!(v.years >= 1 && v.years <= 30)) return { error: { field: 'years', msg: 'Between 1 and 30 years.' } };
      if (!(v.rate >= 0 && v.rate <= 15)) return { error: { field: 'rate', msg: 'An annual rate, e.g. 4.6.' } };
      var r = compute(v, P, N), f = FX.fx[cur];
      return {
        answer: { label: 'Cash to close, in ' + cur, value: fc(r.cash, cur, FX), tone: 'survey',
          sub: ils(r.cash) + ' · monthly payment ' + fc(r.monthly, cur, FX) + ' (' + ils(r.monthly) + ')' + (r.over ? ' · above the 50% cap' : '') },
        breakdown: [{ label: 'Down payment', value: v.price - r.loan, kind: 'housing' }, { label: 'Purchase tax', value: r.tax, kind: 'survey' }, { label: 'Lawyer, appraiser, file fee', value: r.lawyer + r.appr + r.fee, kind: 'civic' }],
        lines: [
          { label: 'Loan', value: ils(r.loan) + ' · ' + fc(r.loan, cur, FX) },
          { label: 'Monthly payment, ' + r.n + ' payments', value: ils(r.monthly) + ' · ' + fc(r.monthly, cur, FX) },
          { label: 'Total interest if the rate holds', value: ils(r.interest) },
          { label: 'Purchase tax, foreign resident', value: ils(r.tax) + ' · ' + (100 * r.tax / v.price).toFixed(2) + '%' },
          { label: 'Lawyer incl. VAT, appraiser, file fee', value: ils(r.lawyer + r.appr + r.fee) },
          { label: '1 ' + cur + ' = ₪' + f.rate + ' (' + f.date + ')', value: '30 days: ' + f.min30 + ' to ' + f.max30 }
        ],
        note: r.over ? '<b>Above the cap:</b> an Israeli bank can lend a non-resident up to 50% of the value, ' + ils(v.price * N.ltv_max) + ' here.'
          : 'A foreign resident pays purchase tax on the additional-home brackets: 8% up to ₪6,055,070 and 10% above. The payment in your currency moves with the exchange rate.',
        scenarioLabel: 'The same loan at another rate',
        scenarios: [-1, -0.5, 0.5, 1].map(function (s) { return { key: String(s), name: (s > 0 ? '+' : '−') + Math.abs(s) + '% rate', value: fc(pay(r.loan, v.rate + s, r.n), cur, FX) + ' / month' }; }),
        table: { title: 'Cash to close, line by line', head: ['Item', 'ILS', cur], num: [1, 2],
          rows: [['Price', ils(v.price), fc(v.price, cur, FX)], ['Mortgage', '−' + ils(r.loan), '−' + fc(r.loan, cur, FX)], ['Purchase tax (foreign resident)', ils(r.tax), fc(r.tax, cur, FX)],
                 ['Lawyer incl. VAT', ils(r.lawyer), fc(r.lawyer, cur, FX)], ['Bank appraiser', ils(r.appr), fc(r.appr, cur, FX)], ['Mortgage file fee', ils(r.fee), fc(r.fee, cur, FX)], ['Cash to close', ils(r.cash), fc(r.cash, cur, FX)]] },
        formula: 'Monthly payment = loan × r ÷ (1 − (1 + r)^−n), r = annual rate ÷ 12, n = months. Cash to close = price − loan + purchase tax + lawyer × 1.18 + appraiser + file fee.',
        sources: [{ label: FX.source + ', ' + f.date, url: FX.url }, { label: N.rates_source.label, url: N.rates_source.url }, { label: N.ltv_source.label, url: N.ltv_source.url }, { label: 'Israel Tax Authority, purchase tax brackets from 16 Jan 2025', url: P.url }],
        text: 'Israeli mortgage from abroad: home ' + ils(v.price) + ', loan ' + ils(r.loan) + ' over ' + v.years + ' years at ' + v.rate + '%: ' + fc(r.monthly, cur, FX) + ' a month; cash to close ' + fc(r.cash, cur, FX) + '.'
      };
    }
  });
})();
