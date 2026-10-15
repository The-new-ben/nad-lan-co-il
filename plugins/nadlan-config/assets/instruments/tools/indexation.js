/* NadLan Instruments · indexation v1 (HAD-527): the construction-inputs index linkage of a new apartment bought from a
   developer, payment by payment. Law: Sale (Apartments) Law s.5ג for contracts from 7.7.2022 (the first 20% paid at signing
   is never linked; at most half of each later payment; no linkage after the contractual delivery date); contracts before
   that: linkage as the contract says (up to the whole payment). Index: CBS series 200010, the KNOWN index on each date
   (published on the 15th for the previous month). Future months: a chosen annual rate. Pure logic in NLIX for unit checks. */
(function () {
  'use strict';
  var NEW_LAW = '2022-07-07';
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function ym(y, m) { while (m < 1) { m += 12; y--; } while (m > 12) { m -= 12; y++; } return y + '-' + pad(m); }
  function knownKey(iso) { var p = iso.split('-').map(Number); return ym(p[0], p[1] - (p[2] <= 15 ? 2 : 1)); }
  function monthsBetween(a, b) { var x = a.split('-').map(Number), y = b.split('-').map(Number); return (y[0] - x[0]) * 12 + (y[1] - x[1]); }
  function addMonths(iso, n) { var p = iso.split('-').map(Number); var d = new Date(Date.UTC(p[0], p[1] - 1 + n, Math.min(p[2], 28))); return d.toISOString().slice(0, 10); }
  function trailing(data) { var ks = Object.keys(data.months); var last = ks[ks.length - 1]; var prev = ym(+last.slice(0, 4), +last.slice(5) - 12); return data.months[prev] ? data.months[last] / data.months[prev] - 1 : 0.03; }
  function idx(data, key, annual) {
    var v = data.months[key]; if (v != null) return { v: v, known: true };
    var last = data.latest; if (key < Object.keys(data.months)[0]) return null;
    var n = monthsBetween(last, key); return { v: data.months[last] * Math.pow(1 + annual, n / 12), known: false };
  }
  function schedule(kind, sign, delivery) {
    if (kind === 'end') return [{ date: sign, pct: 20 }, { date: delivery, pct: 80 }];
    if (kind === 'thirds') return [{ date: sign, pct: 20 }, { date: addMonths(sign, 12), pct: 30 }, { date: delivery, pct: 50 }];
    var span = Math.max(4, monthsBetween(sign.slice(0, 7), delivery.slice(0, 7))); var rows = [{ date: sign, pct: 20 }];
    for (var i = 1; i <= 4; i++) rows.push({ date: addMonths(sign, Math.round(span * i / 5)), pct: 15 });
    rows.push({ date: delivery, pct: 20 }); return rows;
  }
  function compute(v, data, annual) {
    var P = v.price, s = v.sign, del = v.delivery, share = v.share / 100;
    if (!(P > 50000)) return { error: { field: 'price', msg: 'הקלידו את מחיר הדירה בחוזה.' } };
    if (!/^\d{4}-\d{2}-\d{2}$/.test(s)) return { error: { field: 'sign', msg: 'בחרו את תאריך חתימת החוזה.' } };
    if (!/^\d{4}-\d{2}-\d{2}$/.test(del) || del <= s) return { error: { field: 'delivery', msg: 'מועד המסירה בחוזה צריך להיות אחרי תאריך החתימה.' } };
    var newLaw = s >= NEW_LAW;
    if (!(share >= 0 && share <= 1)) return { error: { field: 'share', msg: 'החלק המוצמד הוא בין 0% ל־100% מכל תשלום.' } };
    if (newLaw && share > 0.5) return { error: { field: 'share', msg: 'בחוזה שנחתם מ־7.7.2022 מותר להצמיד עד מחצית מכל תשלום (סעיף 5ג לחוק המכר).' } };
    var rows = v.rows || [];
    var sumPct = rows.reduce(function (a, r) { return a + (+r.pct || 0); }, 0);
    if (Math.abs(sumPct - 100) > 0.01) return { error: { field: 'rows', msg: 'סך התשלומים צריך להיות 100% (עכשיו ' + Math.round(sumPct * 10) / 10 + '%).' } };
    var bk = knownKey(s), base = idx(data, bk, annual);
    if (!base) return { error: { field: 'sign', msg: 'אין נתוני מדד לתאריך הזה (הנתונים מתחילים ב־2010).' } };
    var free20 = newLaw ? 0.2 * P : 0, out = [], total = 0, known = 0, oldLaw = 0;
    rows.slice().sort(function (a, b) { return a.date < b.date ? -1 : 1; }).forEach(function (r) {
      var amt = P * (+r.pct) / 100;
      var unl = 0; if (newLaw && r.date <= s && free20 > 0) { unl = Math.min(amt, free20); free20 -= unl; }
      var linked = newLaw ? (amt - unl) * share : amt * share;
      var eff = newLaw && r.date > del ? del : r.date;
      var k = knownKey(eff), iv = idx(data, k, annual);
      var add = linked * (iv.v / base.v - 1); if (v.floor && add < 0) add = 0;
      var k2 = knownKey(r.date), iv2 = idx(data, k2, annual); var addOld = amt * (iv2.v / base.v - 1); if (v.floor && addOld < 0) addOld = 0;
      total += add; oldLaw += addOld; if (iv.known) known += add;
      out.push({ date: r.date, pct: +r.pct, amt: amt, linked: linked, key: k, iv: iv.v, known: iv.known, add: add });
    });
    return { newLaw: newLaw, base: base.v, baseKey: bk, total: total, known: known, projected: total - known, oldLaw: oldLaw, rows: out };
  }
  window.NLIX = { compute: compute, knownKey: knownKey, schedule: schedule, trailing: trailing };
  if (!window.NadLanInstruments) return;
  var F = window.NadLanInstruments.fmt;
  window.NadLanInstruments.register('indexation', {
    kicker: 'מחשבון · דירה מקבלן',
    title: 'כמה תוסיף ההצמדה למדד תשומות הבנייה',
    lede: 'מחיר החוזה, תאריך החתימה, מועד המסירה ולוח התשלומים: המחשבון מחיל את כללי חוק המכר על כל תשלום, לפי המדד הרשמי של הלשכה המרכזית לסטטיסטיקה, ומראה כמה כבר ידוע וכמה עוד צפוי.',
    strip: function (d) { var m = d.d0, ks = Object.keys(m.months), l = ks[ks.length - 1], p = ks[ks.length - 2];
      return [{ label: 'המדד האחרון שפורסם', value: F.month(l) }, { label: 'שינוי בחודש', value: F.pct(m.months[l] / m.months[p] - 1) }, { label: 'שינוי ב־12 חודשים', value: F.pct(trailing(m)) }]; },
    defaults: function () { return { price: 2800000, sign: '2024-03-10', delivery: '2027-06-30', plan: 'stages', share: 50, floor: true, rows: schedule('stages', '2024-03-10', '2027-06-30') }; },
    fields: [
      { id: 'price', label: 'מחיר הדירה בחוזה', type: 'money', unit: '₪' },
      { id: 'sign', label: 'תאריך חתימת החוזה', type: 'date', help: 'חוזה מ־7.7.2022 ואילך: חלים כללי תיקון 9.' },
      { id: 'delivery', label: 'מועד המסירה בחוזה', type: 'date' },
      { id: 'plan', label: 'לוח התשלומים', type: 'segmented', options: [{ value: 'stages', label: '20% ותשלומים בבנייה' }, { value: 'end', label: '20/80' }, { value: 'thirds', label: '20/30/50' }] },
      { id: 'rows', label: 'התשלומים (תאריך ואחוז מהמחיר)', type: 'rows', addLabel: 'הוספת תשלום', cols: [{ id: 'date', label: 'תאריך התשלום', type: 'date' }, { id: 'pct', label: 'אחוז', unit: '%' }], blank: function () { return { date: '2026-12-01', pct: 0 }; } },
      { id: 'share', label: 'החלק המוצמד מכל תשלום', type: 'percent', unit: '%', help: 'לפי החוזה. בחוזה חדש: עד 50%.' },
      { id: 'floor', label: 'אם המדד יורד', type: 'segmented', options: [{ value: true, label: 'לא יורד מתחת למדד הבסיס' }, { value: false, label: 'יורד גם המחיר' }] }
    ],
    onField: function (id, v, d, redraw) {
      if ((id === 'plan' || id === 'sign' || id === 'delivery') && (id === 'plan' || !v.__custom)) { v.rows = schedule(v.plan, v.sign, v.delivery); v.__custom = false; redraw('rows'); }
    },
    compute: function (v, d, scen) {
      var m = d.d0, tr = trailing(m);
      var rates = { low: 0.02, trend: tr, high: 0.05 }; var key = scen || 'trend';
      var r = compute(v, m, rates[key]); if (r.error) return r;
      var alt = {}; ['low', 'trend', 'high'].forEach(function (k) { alt[k] = compute(v, m, rates[k]).total; });
      var pct = r.total / v.price;
      var lines = [
        { label: 'מדד הבסיס (הידוע ביום החתימה)', value: F.month(r.baseKey) + ' · ' + F.num(r.base, 2) },
        { label: 'תוספת לפי מדדים שכבר פורסמו', value: F.ils(r.known) },
        { label: 'תוספת צפויה בחודשים הבאים', value: F.ils(r.projected) },
        { label: 'סה״כ לתשלום עם ההצמדה', value: F.ils(v.price + r.total) }
      ];
      if (r.newLaw) lines.push({ label: 'החיסכון מתיקון 9, מול הצמדה מלאה', value: F.ils(r.oldLaw - r.total) });
      return {
        answer: { label: 'תוספת ההצמדה המשוערת', value: F.ils(r.total), tone: 'survey', sub: '<bdi>' + F.pct(pct, 2) + '</bdi> ממחיר הדירה · ' + (r.newLaw ? 'חוזה מ־7.7.2022: 20% הראשונים אינם צמודים, עד מחצית מכל תשלום, ועד מועד המסירה בחוזה.' : 'חוזה לפני 7.7.2022: ההצמדה לפי החוזה, בלי המגבלות של תיקון 9.') },
        breakdown: [{ label: 'לפי מדדים שפורסמו', value: r.known, kind: 'civic' }, { label: 'צפי לחודשים הבאים', value: Math.max(0, r.projected), kind: 'sea' }],
        lines: lines,
        scenarioLabel: 'אם המדד יעלה בשנה הבאה ב...',
        scenarios: [{ key: 'low', name: '2% בשנה', value: F.ils(alt.low), on: key === 'low' }, { key: 'trend', name: F.pct(tr) + ' (12 החודשים האחרונים)', value: F.ils(alt.trend), on: key === 'trend' }, { key: 'high', name: '5% בשנה', value: F.ils(alt.high), on: key === 'high' }],
        table: { title: 'הפירוט לפי תשלום', head: ['תאריך', 'אחוז', 'סכום', 'החלק המוצמד', 'המדד', 'תוספת'], num: [1, 2, 3, 4, 5], phoneHide: [1, 3, 4],
          rows: r.rows.map(function (x) { return [F.date(x.date), F.num(x.pct, 0) + '%', F.ils(x.amt), F.ils(x.linked), F.month(x.key) + ' · ' + F.num(x.iv, 2), F.ils(x.add) + (x.known ? '' : ' (צפי)')]; }) },
        formula: 'תוספת = החלק המוצמד של התשלום × (המדד הידוע ביום התשלום ÷ מדד הבסיס − 1). המדד הידוע: עד ה־15 בחודש, המדד של לפני חודשיים; מה־16, של החודש הקודם.',
        sources: [{ label: 'הלשכה המרכזית לסטטיסטיקה, מדד מחירי תשומה בבנייה למגורים (סדרה 200010), עדכון ' + F.month(m.latest), url: 'https://www.cbs.gov.il/' },
          { label: 'חוק המכר (דירות), סעיף 5ג', url: 'https://he.wikisource.org/wiki/%D7%97%D7%95%D7%A7_%D7%94%D7%9E%D7%9B%D7%A8_(%D7%93%D7%99%D7%A8%D7%95%D7%AA)' }],
        text: 'מחשבון הצמדה למדד תשומות הבנייה: דירה ב־' + F.ils(v.price) + ', חוזה מ־' + F.date(v.sign) + '. תוספת משוערת ' + F.ils(r.total) + ' (' + F.pct(pct, 2) + '), מתוכה ' + F.ils(r.known) + ' כבר לפי מדדים שפורסמו.'
      };
    }
  });
})();
