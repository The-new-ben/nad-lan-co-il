/* NadLan Instruments · cpi v1 (HAD-527 turn 2): linkage to the consumer price index (CBS series 120010, chained to the latest
   base). Three jobs: (1) link any amount between two dates, by the KNOWN index (published on the 15th) or by the index FOR a
   month; (2) a CPI-linked rent: the base is the index known at signing, updates every 12, 6 or 3 months or every payment,
   optional floor (never below the contract rent); (3) linkage plus a yearly interest rate. Future months: the last 12 months'
   pace. Pure logic in NLCX for unit checks. */
(function () {
  'use strict';
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function ym(y, m) { while (m < 1) { m += 12; y--; } while (m > 12) { m -= 12; y++; } return y + '-' + pad(m); }
  function knownKey(iso) { var p = iso.split('-').map(Number); return ym(p[0], p[1] - (p[2] <= 15 ? 2 : 1)); }
  function forKey(iso) { return iso.slice(0, 7); }
  function addM(iso, n) { var p = iso.split('-').map(Number); var d = new Date(Date.UTC(p[0], p[1] - 1 + n, Math.min(p[2], 28))); return d.toISOString().slice(0, 10); }
  function trailing(m) { var ks = Object.keys(m.months), l = ks[ks.length - 1], p = ym(+l.slice(0, 4), +l.slice(5) - 12); return m.months[p] ? m.months[l] / m.months[p] - 1 : 0.025; }
  function mdiff(a, b) { return (+b.slice(0, 4) - +a.slice(0, 4)) * 12 + (+b.slice(5, 7) - +a.slice(5, 7)); }
  function val(m, key, rate) { var v = m.months[key]; if (v != null) return { v: v, known: true }; var ks = Object.keys(m.months); if (key < ks[0]) return null; return { v: m.months[m.latest] * Math.pow(1 + rate, mdiff(m.latest, key) / 12), known: false }; }
  function today() { return new Date().toISOString().slice(0, 10); }
  function link(m, amount, from, to, how, rate) {
    var ka = how === 'for' ? forKey(from) : knownKey(from), kb = how === 'for' ? forKey(to) : knownKey(to);
    var a = val(m, ka, rate), b = val(m, kb, rate); if (!a || !b) return null;
    return { ka: ka, kb: kb, a: a.v, b: b.v, projected: !b.known, out: amount * b.v / a.v, chg: b.v / a.v - 1 };
  }
  function rent(m, base, sign, upto, every, floor, rate) {
    var bk = knownKey(sign), b0 = val(m, bk, rate); if (!b0) return null;
    var rows = [], cur = base, step = every === 'pay' ? 1 : +every, d = sign, n = 0, paid = 0;
    while (d <= upto && n < 240) {
      if (n > 0 && n % step === 0) { var k = knownKey(d), iv = val(m, k, rate); var nr = base * iv.v / b0.v; if (floor && nr < base) nr = base; rows.push({ date: d, key: k, iv: iv.v, rent: nr, known: iv.known }); cur = nr; }
      paid += cur; n++; d = addM(sign, n);
    }
    return { bk: bk, b0: b0.v, rows: rows, cur: cur, months: n, paid: paid, extra: paid - base * n };
  }
  window.NLCX = { link: link, rent: rent, knownKey: knownKey, trailing: trailing };
  if (!window.NadLanInstruments) return;
  var F = window.NadLanInstruments.fmt;
  window.NadLanInstruments.register('cpi', {
    kicker: 'מחשבון · מדד המחירים לצרכן',
    title: 'מחשבון הצמדה למדד המחירים לצרכן',
    lede: 'סכום, שכר דירה או חוב: בחרו מה להצמיד, מאיזה תאריך ועד איזה תאריך. המחשבון משתמש במדד הרשמי של הלשכה המרכזית לסטטיסטיקה, לפי "המדד הידוע" או "המדד בגין", ומראה את החישוב.',
    strip: function (d) { var m = d.d0, ks = Object.keys(m.months), l = ks[ks.length - 1], p = ks[ks.length - 2];
      return [{ label: 'המדד האחרון שפורסם', value: F.month(l) }, { label: 'שינוי בחודש', value: F.pct(m.months[l] / m.months[p] - 1) }, { label: 'שינוי ב־12 חודשים', value: F.pct(trailing(m)) }]; },
    defaults: function () { return { mode: 'sum', amount: 100000, from: '2021-01-20', to: today(), how: 'known', rent: 6500, sign: '2024-09-01', every: '12', floor: true, rate: 4 }; },
    fields: [
      { id: 'mode', label: 'מה מצמידים', type: 'segmented', options: [{ value: 'sum', label: 'סכום' }, { value: 'rent', label: 'שכר דירה' }, { value: 'interest', label: 'ריבית והצמדה' }] },
      { id: 'amount', label: 'הסכום', type: 'money', unit: '₪', showIf: function (v) { return v.mode !== 'rent'; } },
      { id: 'from', label: 'מתאריך', type: 'date', showIf: function (v) { return v.mode !== 'rent'; } },
      { id: 'rent', label: 'שכר הדירה בחוזה', type: 'money', unit: '₪', showIf: function (v) { return v.mode === 'rent'; } },
      { id: 'sign', label: 'תאריך חתימת חוזה השכירות', type: 'date', showIf: function (v) { return v.mode === 'rent'; } },
      { id: 'every', label: 'עדכון לפי המדד', type: 'segmented', showIf: function (v) { return v.mode === 'rent'; }, options: [{ value: '12', label: 'פעם בשנה' }, { value: '6', label: 'כל חצי שנה' }, { value: '3', label: 'כל רבעון' }, { value: 'pay', label: 'בכל תשלום' }] },
      { id: 'floor', label: 'אם המדד יורד', type: 'segmented', showIf: function (v) { return v.mode === 'rent'; }, options: [{ value: true, label: 'לא פחות משכר הדירה בחוזה' }, { value: false, label: 'יורד גם שכר הדירה' }] },
      { id: 'to', label: 'עד תאריך', type: 'date' },
      { id: 'how', label: 'איזה מדד', type: 'segmented', showIf: function (v) { return v.mode !== 'rent'; }, options: [{ value: 'known', label: 'המדד הידוע ביום' }, { value: 'for', label: 'המדד בגין החודש' }] },
      { id: 'rate', label: 'ריבית שנתית', type: 'percent', unit: '%', showIf: function (v) { return v.mode === 'interest'; }, help: 'ריבית פשוטה על הסכום המוצמד, לפי מספר הימים.' }
    ],
    compute: function (v, d) {
      var m = d.d0, tr = trailing(m);
      if (!/^\d{4}-\d{2}-\d{2}$/.test(v.to || '')) return { error: { field: 'to', msg: 'בחרו תאריך סיום.' } };
      var srcs = [{ label: 'הלשכה המרכזית לסטטיסטיקה, מדד המחירים לצרכן, כללי (סדרה 120010), עדכון ' + F.month(m.latest), url: 'https://www.cbs.gov.il/' }];
      if (v.mode === 'rent') {
        if (!(v.rent > 100)) return { error: { field: 'rent', msg: 'הקלידו את שכר הדירה בחוזה.' } };
        if (!/^\d{4}-\d{2}-\d{2}$/.test(v.sign || '') || v.sign >= v.to) return { error: { field: 'sign', msg: 'תאריך החתימה צריך להיות לפני תאריך הסיום.' } };
        var r = window.NLCX.rent(m, v.rent, v.sign, v.to, v.every, v.floor, tr); if (!r) return { error: { field: 'sign', msg: 'אין נתוני מדד לתאריך הזה (מ־2010).' } };
        return {
          answer: { label: 'שכר הדירה המעודכן', value: F.ils(r.cur), tone: 'ink', sub: '<bdi>' + F.pct(r.cur / v.rent - 1) + '</bdi> מול החוזה · מדד הבסיס ' + F.month(r.bk) },
          breakdown: [{ label: 'שכר הדירה בחוזה', value: v.rent * r.months, kind: 'housing' }, { label: 'תוספת ההצמדה עד היום', value: Math.max(0, r.extra), kind: 'civic' }],
          lines: [{ label: 'מדד הבסיס (הידוע בחתימה)', value: F.month(r.bk) + ' · ' + F.num(r.b0, 2) }, { label: 'חודשי שכירות עד ' + F.date(v.to), value: F.num(r.months) }, { label: 'סה״כ ששולם עם ההצמדה', value: F.ils(r.paid) }, { label: 'מתוכו תוספת ההצמדה', value: F.ils(r.extra) }],
          table: { title: 'העדכונים לפי המדד', head: ['תאריך', 'המדד', 'שכר הדירה'], num: [1, 2], rows: r.rows.map(function (x) { return [F.date(x.date), F.month(x.key) + ' · ' + F.num(x.iv, 2) + (x.known ? '' : ' (צפי)'), F.ils(x.rent)]; }) },
          formula: 'שכר דירה מעודכן = שכר הדירה בחוזה × (המדד הידוע ביום העדכון ÷ המדד הידוע ביום החתימה)' + (v.floor ? ', ולא פחות משכר הדירה בחוזה.' : '.'),
          sources: srcs, text: 'שכר דירה ' + F.ils(v.rent) + ' צמוד למדד מ־' + F.date(v.sign) + ': היום ' + F.ils(r.cur) + ' (' + F.pct(r.cur / v.rent - 1) + ').'
        };
      }
      if (!(v.amount > 0)) return { error: { field: 'amount', msg: 'הקלידו סכום.' } };
      if (!/^\d{4}-\d{2}-\d{2}$/.test(v.from || '') || v.from >= v.to) return { error: { field: 'from', msg: 'תאריך ההתחלה צריך להיות לפני תאריך הסיום.' } };
      var L = window.NLCX.link(m, v.amount, v.from, v.to, v.how, tr); if (!L) return { error: { field: 'from', msg: 'אין נתוני מדד לתאריך הזה (מ־2010).' } };
      var days = Math.round((Date.parse(v.to) - Date.parse(v.from)) / 864e5), interest = v.mode === 'interest' ? L.out * (v.rate / 100) * days / 365 : 0;
      var total = L.out + interest;
      var lines = [{ label: 'המדד בתחילה', value: F.month(L.ka) + ' · ' + F.num(L.a, 2) }, { label: 'המדד בסוף', value: F.month(L.kb) + ' · ' + F.num(L.b, 2) + (L.projected ? ' (צפי)' : '') }, { label: 'שינוי המדד', value: F.pct(L.chg, 2) }, { label: 'הפרשי הצמדה', value: F.ils(L.out - v.amount) }];
      if (interest) lines.push({ label: 'ריבית (' + F.num(v.rate, 2) + '% לשנה, ' + F.num(days) + ' ימים)', value: F.ils(interest) });
      return {
        answer: { label: v.mode === 'interest' ? 'הסכום עם ריבית והצמדה' : 'הסכום המוצמד', value: F.ils(total), tone: 'ink', sub: '<bdi>' + F.pct(total / v.amount - 1, 2) + '</bdi> מעל הסכום המקורי' + (L.projected ? ' · המדד בסוף התקופה עוד לא פורסם, והוא לפי קצב 12 החודשים האחרונים' : '') },
        breakdown: [{ label: 'הסכום המקורי', value: v.amount, kind: 'housing' }, { label: 'הפרשי הצמדה', value: Math.max(0, L.out - v.amount), kind: 'civic' }].concat(interest ? [{ label: 'ריבית', value: interest, kind: 'sea' }] : []),
        lines: lines,
        formula: 'סכום מוצמד = הסכום × (המדד בסוף ÷ המדד בתחילה). ' + (v.how === 'known' ? 'המדד הידוע: עד ה־15 בחודש, המדד של לפני חודשיים; מה־16, של החודש הקודם.' : 'המדד בגין: המדד של החודש עצמו, גם אם פורסם אחריו.'),
        sources: srcs, text: F.ils(v.amount) + ' מ־' + F.date(v.from) + ' צמוד למדד המחירים לצרכן עד ' + F.date(v.to) + ': ' + F.ils(total) + ' (' + F.pct(total / v.amount - 1, 2) + ').'
      };
    }
  });
})();
