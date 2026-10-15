/* NadLan Instruments · pfas v1 (HAD-534): reading a soil lab result. A concentration from a soil survey, in any unit, becomes
   "how many times the direct-contact threshold" used by the Sde Dov reports (June 2026 values as printed in them), and is set
   against the peaks the published reports found, plot by plot. Data: data/sde-dov-soil.json (the same file as the map).
   Pure logic in NLPF for unit checks. */
(function () {
  'use strict';
  var UNIT = { ng: 1, ug: 1e3, mg: 1e6 };  // to ng/kg
  function compute(val, unit, sub, th) { var ng = val * UNIT[unit]; return { ng: ng, x: ng / th[sub], th: th[sub] }; }
  window.NLPF = { compute: compute, UNIT: UNIT };
  if (!window.NadLanInstruments) return;
  var F = window.NadLanInstruments.fmt;
  function xs(x) { return x >= 1 ? 'פי ' + (x >= 10 ? F.num(Math.round(x)) : F.num(x, 1)) : F.num(x * 100, x < 0.1 ? 1 : 0) + '% מהסף'; }
  function small(n) { return n >= 100 ? F.num(n) : n >= 1 ? F.num(n, 2) : F.num(n, 4); }
  window.NadLanInstruments.register('pfas', {
    kicker: 'מחשבון · קרקע',
    title: 'פי כמה מעל ערך הסף? תוצאת מעבדה של PFAS',
    lede: 'מקלידים ריכוז מתוך דו"ח סקר קרקע, בוחרים חומר ויחידה, ומקבלים פי כמה הוא מעל ערך הסף למגע ישיר שמשמש בדו"חות של שדה דב, ואיך הוא עומד מול השיאים שפורסמו.',
    defaults: function () { return { sub: 'pfos', val: 3780000, unit: 'ng' }; },
    fields: [
      { id: 'sub', label: 'החומר', type: 'segmented', options: [{ value: 'pfos', label: 'PFOS' }, { value: 'pfoa', label: 'PFOA' }, { value: 'pfhxs', label: 'PFHxS' }] },
      { id: 'val', label: 'הריכוז בדו"ח', type: 'number' },
      { id: 'unit', label: 'היחידה בדו"ח', type: 'segmented', options: [{ value: 'ng', label: 'ננוגרם לק"ג' }, { value: 'ug', label: 'מיקרוגרם לק"ג' }, { value: 'mg', label: 'מיליגרם לק"ג' }],
        help: 'בדו"חות מופיע ng/kg, µg/kg או mg/kg. אלף ננוגרם הם מיקרוגרם אחד, ומיליון ננוגרם הם מיליגרם אחד.' }
    ],
    compute: function (v, data) {
      var d = data.soil, th = d.thresholds;
      if (!(v.val > 0)) return { error: { field: 'val', msg: 'הקלידו ריכוז גדול מאפס.' } };
      var r = compute(v.val, v.unit, v.sub, th), name = v.sub.toUpperCase(), over = r.x > 1;
      var rep = d.records.filter(function (x) { return x.status === 'published_report' && x.pfosMax; }).sort(function (a, b) { return b.pfosMax - a.pfosMax; });
      var out = {
        answer: { label: name + ' מול ערך הסף למגע ישיר', value: xs(r.x), tone: over ? 'survey' : 'ink', sub: F.num(r.ng) + ' ננוגרם לק"ג · ערך הסף: ' + F.num(r.th, 1) },
        lines: [{ label: 'בננוגרם לק"ג (ng/kg)', value: F.num(r.ng) }, { label: 'במיקרוגרם לק"ג (µg/kg)', value: small(r.ng / 1e3) }, { label: 'במיליגרם לק"ג (mg/kg)', value: small(r.ng / 1e6) },
          { label: 'ערך הסף ל־' + name, value: F.num(r.th, 1) + ' ננוגרם לק"ג' }],
        note: (over ? 'הריכוז מעל ערך הסף. ' : 'הריכוז מתחת לערך הסף. ') + 'ערך הסף משמש בדו"חות להשוואה: חריגה פירושה שלפי הנחיות המשרד להגנת הסביבה הקרקע דורשת בדיקה נוספת או טיפול לפני בנייה. המחשבון לא מחליף את קריאת הדו"ח המלא ואת חוות הדעת של יועץ סביבתי.',
        formula: 'פי כמה = הריכוז בננוגרם לק"ג ÷ ערך הסף. ' + d.thresholdsLabel + ': PFOS ' + F.num(th.pfos, 1) + ', PFOA ' + F.num(th.pfoa, 1) + ', PFHxS ' + F.num(th.pfhxs, 1) + ' ננוגרם לק"ג.',
        sources: [{ label: 'דו"ח סקר הקרקע של מגרש 303, מאגר המשרד להגנת הסביבה', url: (rep[0] || {}).src || 'https://www.gov.il/' }],
        text: 'תוצאת מעבדה: ' + name + ' ' + F.num(r.ng) + ' ננוגרם לק"ג = ' + xs(r.x) + ' מערך הסף למגע ישיר (שדה דב, יוני 2026).'
      };
      if (v.sub === 'pfos' && rep.length) out.table = { title: 'מול השיאים שפורסמו בשדה דב (PFOS)', head: ['מגרש', 'השיא בדו"ח', 'מול הסף', 'מול הערך שלכם'], num: [1, 2, 3], phoneHide: [1],
        rows: rep.map(function (x) { var k = x.pfosMax / r.ng; return [x.plot, F.num(x.pfosMax), xs(x.pfosX), k >= 1 ? 'פי ' + small(k) + ' יותר' : 'פי ' + small(1 / k) + ' פחות']; }) };
      return out;
    }
  });
})();
