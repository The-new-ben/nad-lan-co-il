/* NadLan Instruments · ptax v1 (HAD-527, Kikar HaMedina tools program, Ben 15.10 + 21.10.2026): purchase tax on an apartment,
   all four tracks in one (an only home, an additional home, a new immigrant, a foreign resident), a part share, the effective
   rate, the tax bracket by bracket, and the same price on every track side by side. Data: ptax.json (the Tax Authority brackets
   in force from 16.1.2025, frozen to 15.1.2028; checked against the Tax Authority simulator 21.10.2026). The brackets apply to
   the value of the whole apartment and a buyer of a part pays his share of it. Pure logic in NLPT for unit checks. */
(function () {
  'use strict';
  function tax(price, br) {
    var t = 0, lo = 0, rows = [];
    for (var i = 0; i < br.length; i++) {
      var hi = br[i][0] == null ? Infinity : br[i][0], r = br[i][1];
      var top = Math.min(price, hi);
      if (top > lo) { t += (top - lo) * r; rows.push({ from: lo, to: hi, rate: r, part: top - lo, tax: (top - lo) * r }); }
      if (price <= hi) break;
      lo = hi;
    }
    return { tax: t, rows: rows };
  }
  window.NLPT = { tax: tax };
  if (!window.NadLanInstruments) return;
  var F = window.NadLanInstruments.fmt;
  var NAMES = { single: 'דירה יחידה', extra: 'דירה נוספת', oleh: 'עולה חדש', foreign: 'תושב חוץ' };
  var NOTE = {
    single: 'יחיד תושב ישראל שזו הדירה היחידה שלו, או שימכור את הדירה הקודמת תוך 18 חודשים (דירה חלופית).',
    extra: 'למי שיש כבר דירה ולא ימכור אותה, ולחברה.',
    oleh: 'הטבה לעולה חדש לפי תקנות מיסוי מקרקעין. את הזכאות קובעת רשות המסים לפי תעודת העולה ומועד הרכישה.',
    foreign: 'מי שאינו תושב ישראל משלם לפי מדרגות דירה נוספת, גם אם זו הדירה היחידה שלו.'
  };
  window.NadLanInstruments.register('ptax', {
    kicker: 'מחשבון · מס רכישה',
    title: 'כמה מס רכישה תשלמו על הדירה',
    lede: 'מחיר הדירה, מי הקונה וכמה מהדירה הוא קונה: המחשבון מחשב את המס לפי המדרגות של רשות המסים, מראה כמה נופל על כל מדרגה, ומשווה את אותו מחיר בכל ארבעת המסלולים.',
    strip: function (d) { var p = d.ptax; return [{ label: 'פטור בדירה יחידה עד', value: F.ils(p.tracks.single[0][0]) }, { label: 'דירה נוספת ותושב חוץ', value: '8% עד ' + F.ils(p.tracks.extra[0][0]) }, { label: 'המדרגות מוקפאות עד', value: F.date(p.frozen_until) }]; },
    defaults: function () { return { price: 3000000, track: 'single', share: 100 }; },
    fields: [
      { id: 'price', label: 'מחיר הדירה', type: 'money', unit: '₪', help: 'המחיר בחוזה. בדירה מקבלן, המחיר כולל מע״מ.' },
      { id: 'track', label: 'מי קונה', type: 'segmented', options: [{ value: 'single', label: 'דירה יחידה' }, { value: 'extra', label: 'דירה נוספת' }, { value: 'oleh', label: 'עולה חדש' }, { value: 'foreign', label: 'תושב חוץ' }] },
      { id: 'share', label: 'החלק שאתם קונים', type: 'percent', unit: '%', help: 'קונים חצי דירה? 50. המס מחושב על כל הדירה, וכל קונה משלם לפי החלק שלו.' }
    ],
    compute: function (v, d) {
      var P = d.ptax;
      if (!(v.price >= 100000 && v.price <= 500000000)) return { error: { field: 'price', msg: 'הקלידו את מחיר הדירה בשקלים.' } };
      if (!(v.share > 0 && v.share <= 100)) return { error: { field: 'share', msg: 'החלק שאתם קונים: בין 1 ל־100 אחוז.' } };
      var k = P.tracks[v.track] ? v.track : 'single', s = v.share / 100;
      var full = tax(v.price, P.tracks[k]), t = full.tax * s, part = v.price * s;
      var last = full.rows[full.rows.length - 1];
      var single = tax(v.price, P.tracks.single).tax * s;
      var lines = [
        { label: 'שיעור המס האפקטיבי', value: F.num(part ? 100 * t / part : 0, 2) + '%' },
        { label: 'המדרגה של השקל האחרון', value: F.num(100 * (last ? last.rate : 0), 1) + '%' },
        { label: 'המחיר של החלק שאתם קונים', value: F.ils(part) }
      ];
      if (k !== 'single') lines.push({ label: 'לעומת דירה יחידה באותו מחיר', value: (t >= single ? '+' : '−') + F.ils(Math.abs(t - single)) });
      return {
        answer: { label: 'מס הרכישה, ' + NAMES[k] + (s < 1 ? ', ' + F.num(v.share) + '% מהדירה' : ''), value: F.ils(t), tone: t > 0 ? 'survey' : 'ink',
          sub: t > 0 ? F.num(100 * t / part, 2) + '% מהמחיר' + (s < 1 ? ' של החלק שלכם' : '') : 'במחיר הזה אין מס רכישה בדירה יחידה' },
        breakdown: [{ label: 'מחיר', value: part, kind: 'housing' }, { label: 'מס רכישה', value: t, kind: 'survey' }],
        lines: lines,
        note: '<b>' + NAMES[k] + ':</b> ' + NOTE[k],
        scenarioLabel: 'אותו מחיר, בכל מסלול',
        scenarios: ['single', 'extra', 'oleh', 'foreign'].map(function (x) { return { key: x, name: NAMES[x], value: F.ils(tax(v.price, P.tracks[x]).tax * s) }; }),
        table: { title: 'המס מדרגה אחרי מדרגה, ' + NAMES[k], head: ['מדרגה', 'שיעור', 'הסכום במדרגה', 'המס'], num: [2, 3],
          rows: full.rows.map(function (r) { return [(r.from ? F.ils(r.from) : '₪0') + ' עד ' + (r.to === Infinity ? 'מעל' : F.ils(r.to)), F.num(100 * r.rate, 1) + '%', F.ils(r.part * s), F.ils(r.tax * s)]; }) },
        formula: 'מס רכישה = סכום על כל המדרגות של (החלק מהמחיר שנופל במדרגה × שיעור המדרגה), כפול החלק שאתם קונים. המדרגות חלות על שווי הדירה כולה.',
        sources: [{ label: P.source + ', מדרגות מ־' + F.date(P.effective) + ', מוקפאות עד ' + F.date(P.frozen_until) + ', נבדק ' + F.date(P.checked), url: P.url }],
        text: 'מס רכישה, ' + NAMES[k] + ': דירה ב־' + F.ils(v.price) + (s < 1 ? ', ' + F.num(v.share) + '% מהדירה' : '') + ' = ' + F.ils(t) + ' (' + F.num(part ? 100 * t / part : 0, 2) + '%).'
      };
    }
  });
})();
