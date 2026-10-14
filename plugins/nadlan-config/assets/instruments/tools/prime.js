/* NadLan Instruments · prime v1 (HAD-527 turn 3): what the Bank of Israel rate means in shekels for a prime-linked mortgage
   track. Data: boi-rate.json (official daily series MNT_RIB_BOI_D reduced to decisions; prime = rate + 1.5). The payment is a
   Spitzer (equal monthly payment) on the remaining balance and term; scenarios move the rate by quarter points.
   Pure logic in NLPX for unit checks. */
(function () {
  'use strict';
  function pay(P, annual, months) { var r = annual / 100 / 12; return r === 0 ? P / months : P * r / (1 - Math.pow(1 + r, -months)); }
  window.NLPX = { pay: pay };
  if (!window.NadLanInstruments) return;
  var F = window.NadLanInstruments.fmt;
  window.NadLanInstruments.register('prime', {
    kicker: 'מחשבון · משכנתא',
    title: 'כמה הריבית של בנק ישראל עולה לכם בחודש',
    lede: 'יתרת המשכנתא במסלול הפריים, השנים שנותרו והמרווח מהפריים: המחשבון מראה את ההחזר החודשי לפי הפריים של היום, וכמה הוא משתנה בכל שינוי של רבע אחוז בריבית בנק ישראל.',
    strip: function (d) { var b = d.d0, c = b.changes, l = c[c.length - 1], p = c[c.length - 2];
      return [{ label: 'ריבית בנק ישראל', value: F.num(b.rate, 2) + '%' }, { label: 'ריבית הפריים', value: F.num(b.prime, 2) + '%' }, { label: 'השינוי האחרון', value: F.date(l.from) + ' · ' + (l.rate > p.rate ? '+' : '−') + F.num(Math.abs(l.rate - p.rate), 2) + '%' }]; },
    defaults: function () { return { balance: 600000, years: 22, margin: -0.5 }; },
    fields: [
      { id: 'balance', label: 'יתרת ההלוואה במסלול הפריים', type: 'money', unit: '₪' },
      { id: 'years', label: 'שנים שנותרו', type: 'number', unit: 'שנים' },
      { id: 'margin', label: 'המרווח מהפריים', type: 'percent', unit: '%', help: 'למשל −0.5 לפריים מינוס חצי. כתוב בדוח השנתי מהבנק.' }
    ],
    compute: function (v, d) {
      var b = d.d0;
      if (!(v.balance > 1000)) return { error: { field: 'balance', msg: 'הקלידו את יתרת ההלוואה במסלול הפריים.' } };
      if (!(v.years > 0 && v.years <= 35)) return { error: { field: 'years', msg: 'מספר השנים שנותרו: בין 1 ל־35.' } };
      if (!(v.margin >= -3 && v.margin <= 3)) return { error: { field: 'margin', msg: 'המרווח מהפריים הוא בדרך כלל בין −1% ל־+1%.' } };
      var n = Math.round(v.years * 12), rate = b.prime + v.margin, now = pay(v.balance, rate, n);
      var q = pay(v.balance, rate + 0.25, n) - now;
      var sc = [-0.5, -0.25, 0.25, 0.5].map(function (s) { return { key: String(s), name: (s > 0 ? '+' : '−') + F.num(Math.abs(s), 2) + '% בריבית', value: F.ils(pay(v.balance, rate + s, n)) + ' · ' + (s > 0 ? '+' : '−') + F.ils(Math.abs(pay(v.balance, rate + s, n) - now)) }; });
      var total = now * n, interest = total - v.balance;
      var hist = b.changes.slice(-8).reverse();
      return {
        answer: { label: 'ההחזר החודשי במסלול הפריים היום', value: F.ils(now), tone: 'ink', sub: 'ריבית ' + F.num(rate, 2) + '% (פריים ' + F.num(b.prime, 2) + '% ' + (v.margin < 0 ? '−' : '+') + ' ' + F.num(Math.abs(v.margin), 2) + '%) · כל רבע אחוז: <bdi>' + F.ils(q) + '</bdi> בחודש' },
        breakdown: [{ label: 'קרן', value: v.balance, kind: 'housing' }, { label: 'ריבית עד הסוף, אם הריבית לא תשתנה', value: interest, kind: 'civic' }],
        lines: [{ label: 'כל שינוי של 0.25% בריבית בנק ישראל', value: F.ils(q) + ' בחודש' }, { label: 'ריבית שנתית במסלול', value: F.num(rate, 2) + '%' }, { label: 'מספר התשלומים שנותרו', value: F.num(n) }, { label: 'סה״כ ריבית עד הסוף', value: F.ils(interest) }],
        scenarioLabel: 'אם בנק ישראל ישנה את הריבית ב...',
        scenarios: sc,
        table: { title: 'החלטות הריבית האחרונות של בנק ישראל', head: ['בתוקף מ', 'ריבית בנק ישראל', 'פריים'], num: [1, 2], rows: hist.map(function (c) { return [F.date(c.from), F.num(c.rate, 2) + '%', F.num(c.prime, 2) + '%']; }) },
        formula: 'החזר חודשי (שפיצר) = יתרה × ר ÷ (1 − (1 + ר)^−מ), כש־ר = הריבית השנתית ÷ 12 ומ = מספר התשלומים. פריים = ריבית בנק ישראל + 1.5%.',
        sources: [{ label: b.source + ', עדכון ' + F.date(b.asof), url: 'https://www.boi.org.il/' }],
        text: 'מסלול פריים: יתרה ' + F.ils(v.balance) + ', ' + F.num(v.years) + ' שנים, פריים ' + F.num(b.prime, 2) + '% ' + (v.margin < 0 ? '−' : '+') + F.num(Math.abs(v.margin), 2) + '%: החזר ' + F.ils(now) + ' בחודש. כל רבע אחוז: ' + F.ils(q) + '.'
      };
    }
  });
})();
