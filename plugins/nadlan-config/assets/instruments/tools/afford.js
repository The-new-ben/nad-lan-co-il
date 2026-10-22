/* NadLan Instruments · afford v1 (HAD-575, Kikar tools #7, Ben 15.10 + 21.10.2026): what home a household can buy. Two limits,
   solved together: the monthly payment against the net income (the share the household picks, never above the Bank of Israel
   cap of 50% of disposable income, minus existing loans) and the equity against the down payment by the buyer's LTV cap PLUS the
   purchase tax (ptax brackets by track) and the lawyer with VAT. The highest price that passes both is found by bisection.
   Data: ptax.json, cost.json (VAT, LTV caps), nrm.json (Bank of Israel average rates of new mortgages). Pure logic in NLAF. */
(function () {
  'use strict';
  function pv(pay, annual, months) { var r = annual / 100 / 12; return r === 0 ? pay * months : pay * (1 - Math.pow(1 + r, -months)) / r; }
  function pmt(P, annual, months) { var r = annual / 100 / 12; return r === 0 ? P / months : P * r / (1 - Math.pow(1 + r, -months)); }
  function ptax(price, br) { var t = 0, lo = 0; for (var i = 0; i < br.length; i++) { var hi = br[i][0] == null ? Infinity : br[i][0], top = Math.min(price, hi); if (top > lo) t += (top - lo) * br[i][1]; if (price <= hi) break; lo = hi; } return t; }
  function compute(v, P, C) {
    var k = P.tracks[v.track] ? v.track : 'single', n = Math.round(v.years * 12), ltv = C.ltv[k];
    var payMax = Math.max(0, (v.income || 0) * Math.min(v.ratio, 50) / 100 - (v.loans || 0));
    var loanMax = pv(payMax, v.rate, n), costRate = (v.lawyer || 0) / 100 * (1 + C.vat);
    function trk(price) { return k === 'oleh' && P.oleh_cap && price > P.oleh_cap ? P.tracks.single : P.tracks[k]; }  // 1.72.500: the oleh cap
    function cash(price) { var loan = Math.min(ltv * price, loanMax); return { loan: loan, need: price - loan + ptax(price, trk(price)) + costRate * price }; }
    var lo = 0, hi = 200000000;
    for (var i = 0; i < 80; i++) { var mid = (lo + hi) / 2; if (cash(mid).need <= (v.equity || 0)) lo = mid; else hi = mid; }
    var price = Math.floor(lo / 1000) * 1000, c = cash(price);
    var byPayment = c.loan >= loanMax - 1;  // the payment is the binding limit when the loan is at its payment maximum
    return { k: k, ltv: ltv, payMax: payMax, loanMax: loanMax, price: price, loan: c.loan, tax: ptax(price, trk(price)), lawyer: costRate * price,
             monthly: pmt(c.loan, v.rate, n), limit: byPayment ? 'payment' : 'equity', n: n };
  }
  window.NLAF = { compute: compute, pv: pv };
  if (!window.NadLanInstruments) return;
  var F = window.NadLanInstruments.fmt;
  var NAMES = { single: 'דירה יחידה', extra: 'דירה נוספת', oleh: 'עולה חדש', foreign: 'תושב חוץ' };
  window.NadLanInstruments.register('afford', {
    kicker: 'מחשבון · כושר החזר',
    title: 'איזו דירה אתם יכולים לקנות',
    lede: 'הכנסה, הון עצמי והלוואות קיימות: המחשבון בודק גם את ההחזר החודשי מול ההכנסה וגם את ההון העצמי מול המקדמה, מס הרכישה ועורך הדין, ומוצא את מחיר הדירה הגבוה ביותר שעובר את שתי הבדיקות.',
    strip: function (d) { return [{ label: 'החזר מרבי לפי בנק ישראל', value: '50% מההכנסה הפנויה' }, { label: 'מימון מרבי, דירה יחידה', value: F.num(100 * d.cost.ltv.single) + '%' }, { label: 'ריבית ממוצעת, קבועה לא צמודה', value: F.num(d.nrm.rates[0].rate, 2) + '%' }]; },
    defaults: function (d) { return { income: 25000, loans: 0, equity: 900000, track: 'single', ratio: 35, rate: d.nrm.rates[0].rate, years: 25, lawyer: 0.5 }; },
    fields: [
      { id: 'income', label: 'הכנסה נטו של משק הבית בחודש', type: 'money', unit: '₪' },
      { id: 'loans', label: 'החזרים חודשיים של הלוואות קיימות', type: 'money', unit: '₪', help: 'הלוואות, ליסינג, מינוס קבוע. הבנק מוריד אותם מכושר ההחזר.' },
      { id: 'equity', label: 'הון עצמי', type: 'money', unit: '₪', help: 'כל הכסף שיש לכם לעסקה, כולל למס הרכישה ולעורך הדין.' },
      { id: 'track', label: 'מי קונה', type: 'segmented', options: [{ value: 'single', label: 'דירה יחידה' }, { value: 'extra', label: 'דירה נוספת' }, { value: 'oleh', label: 'עולה חדש' }, { value: 'foreign', label: 'תושב חוץ' }] },
      { id: 'ratio', label: 'כמה מההכנסה ללכת להחזר', type: 'percent', unit: '%', help: 'בנק ישראל לא מתיר יותר מ־50%. רוב הבנקים מעדיפים עד 35% עד 40%.' },
      { id: 'rate', label: 'ריבית', type: 'percent', unit: '%' },
      { id: 'years', label: 'שנים', type: 'number', unit: 'שנים' },
      { id: 'lawyer', label: 'עורך דין, לפני מע״מ', type: 'percent', unit: '%' }
    ],
    compute: function (v, d) {
      var P = d.ptax, C = d.cost, N = d.nrm;
      if (!(v.income > 0)) return { error: { field: 'income', msg: 'הקלידו את ההכנסה החודשית נטו.' } };
      if (!(v.ratio > 0 && v.ratio <= 50)) return { error: { field: 'ratio', msg: 'בין 1% ל־50% מההכנסה.' } };
      if (!(v.years >= 4 && v.years <= 30)) return { error: { field: 'years', msg: 'בין 4 ל־30 שנים.' } };
      var r = compute(v, P, C);
      return {
        answer: { label: 'מחיר הדירה המרבי', value: F.ils(r.price), tone: 'survey',
          sub: 'משכנתא ' + F.ils(r.loan) + ' · החזר ' + F.ils(r.monthly) + ' בחודש · ' + (r.limit === 'payment' ? 'מה שמגביל: ההכנסה' : 'מה שמגביל: ההון העצמי') },
        breakdown: [{ label: 'משכנתא', value: r.loan, kind: 'sea' }, { label: 'הון עצמי לדירה', value: r.price - r.loan, kind: 'housing' }, { label: 'מס רכישה ועורך דין', value: r.tax + r.lawyer, kind: 'survey' }],
        lines: [
          { label: 'החזר מרבי לפי ההכנסה', value: F.ils(r.payMax) + ' בחודש' },
          { label: 'משכנתא מרבית לפי ההחזר', value: F.ils(r.loanMax) },
          { label: 'מימון מרבי, ' + NAMES[r.k], value: F.num(100 * r.ltv) + '% · ' + F.ils(r.ltv * r.price) },
          { label: 'מס רכישה במחיר הזה', value: F.ils(r.tax) },
          { label: 'עורך דין, כולל מע״מ', value: F.ils(r.lawyer) }
        ],
        note: r.limit === 'payment' ? '<b>ההכנסה היא מה שמגביל:</b> עוד הון עצמי לא יגדיל את המחיר. ריבית נמוכה יותר, יותר שנים או הכנסה גבוהה יותר כן.'
          : '<b>ההון העצמי הוא מה שמגביל:</b> הבנק יממן עד ' + F.num(100 * r.ltv) + '% מהשווי, ואת השאר, יחד עם מס הרכישה ועורך הדין, צריך להביא מהבית.',
        scenarioLabel: 'אם ההחזר יהיה ... מההכנסה',
        scenarios: [30, 35, 40, 50].map(function (x) { return { key: String(x), name: x + '%', value: F.ils(compute(Object.assign({}, v, { ratio: x }), P, C).price) }; }),
        formula: 'משכנתא מרבית = הערך הנוכחי של ההחזר המרבי (הכנסה × אחוז ההחזר − הלוואות קיימות) לפי הריבית והשנים. מחיר מרבי = המחיר הגבוה ביותר שבו מחיר − משכנתא + מס רכישה + עורך דין × 1.18 ≤ הון עצמי, כשהמשכנתא עד שיעור המימון המרבי.',
        sources: [{ label: 'בנק ישראל, ריבית ממוצעת במשכנתאות חדשות, אוגוסט 2026', url: N.rates_source.url }, C.sources[2], { label: P.source, url: P.url }],
        text: 'עם הכנסה של ' + F.ils(v.income) + ' והון עצמי של ' + F.ils(v.equity) + ': דירה עד ' + F.ils(r.price) + ', משכנתא ' + F.ils(r.loan) + ', החזר ' + F.ils(r.monthly) + ' בחודש.'
      };
    }
  });
})();
