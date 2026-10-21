/* NadLan Instruments · pfas v1 (HAD-534): reading a soil lab result. A concentration from a soil survey, in any unit, becomes
   "how many times the direct-contact threshold" used by the Sde Dov reports (June 2026 values as printed in them), and is set
   against the peaks the published reports found, plot by plot. Data: data/sde-dov-soil.json (the same file as the map).
   Pure logic in NLPF for unit checks. HAD-534 (d), 21.10.2026: Hebrew and English (TX, picked by NadLanInstruments.lang;
   source table docs/tools/soil-en/strings-en.json, pfas). */
(function () {
  'use strict';
  var UNIT = { ng: 1, ug: 1e3, mg: 1e6 };  // to ng/kg
  function compute(val, unit, sub, th) { var ng = val * UNIT[unit]; return { ng: ng, x: ng / th[sub], th: th[sub] }; }
  var TX = {
    times: { he: 'פי {n}', en: '{n}×' },
    pctOf: { he: '{n}% מהסף', en: '{n}% of the threshold' },
    kicker: { he: 'מחשבון · קרקע', en: 'Calculator · Soil' },
    title: { he: 'פי כמה מעל ערך הסף? תוצאת מעבדה של PFAS', en: 'How many times the threshold? Reading a PFAS lab result' },
    lede: { he: 'מקלידים ריכוז מתוך דו"ח סקר קרקע, בוחרים חומר ויחידה, ומקבלים פי כמה הוא מעל ערך הסף למגע ישיר שמשמש בדו"חות של שדה דב, ואיך הוא עומד מול השיאים שפורסמו.',
      en: 'Type a concentration from a soil survey report, choose the compound and the unit, and see how many times it is above the direct-contact threshold used in the Sde Dov reports, and how it compares with the published peaks.' },
    fSub: { he: 'החומר', en: 'Compound' },
    fVal: { he: 'הריכוז בדו"ח', en: 'Concentration in the report' },
    fUnit: { he: 'היחידה בדו"ח', en: 'Unit in the report' },
    uNg: { he: 'ננוגרם לק"ג', en: 'ng/kg' },
    uUg: { he: 'מיקרוגרם לק"ג', en: 'µg/kg' },
    uMg: { he: 'מיליגרם לק"ג', en: 'mg/kg' },
    help: { he: 'בדו"חות מופיע ng/kg, µg/kg או mg/kg. אלף ננוגרם הם מיקרוגרם אחד, ומיליון ננוגרם הם מיליגרם אחד.', en: 'Reports print ng/kg, µg/kg or mg/kg. A thousand nanograms make one microgram, and a million nanograms make one milligram.' },
    errVal: { he: 'הקלידו ריכוז גדול מאפס.', en: 'Enter a concentration greater than zero.' },
    ansLab: { he: '{name} מול ערך הסף למגע ישיר', en: '{name} against the direct-contact threshold' },
    ansSub: { he: '{ng} ננוגרם לק"ג · ערך הסף: {th}', en: '{ng} ng/kg · threshold: {th}' },
    lNg: { he: 'בננוגרם לק"ג (ng/kg)', en: 'In nanograms per kg (ng/kg)' },
    lUg: { he: 'במיקרוגרם לק"ג (µg/kg)', en: 'In micrograms per kg (µg/kg)' },
    lMg: { he: 'במיליגרם לק"ג (mg/kg)', en: 'In milligrams per kg (mg/kg)' },
    lTh: { he: 'ערך הסף ל־{name}', en: 'Threshold for {name}' },
    ngVal: { he: '{n} ננוגרם לק"ג', en: '{n} ng/kg' },
    over: { he: 'הריכוז מעל ערך הסף. ', en: 'The concentration is above the threshold. ' },
    under: { he: 'הריכוז מתחת לערך הסף. ', en: 'The concentration is below the threshold. ' },
    note: { he: 'ערך הסף משמש בדו"חות להשוואה: חריגה פירושה שלפי הנחיות המשרד להגנת הסביבה הקרקע דורשת בדיקה נוספת או טיפול לפני בנייה. המחשבון לא מחליף את קריאת הדו"ח המלא ואת חוות הדעת של יועץ סביבתי.',
      en: 'The reports use the threshold for comparison: an exceedance means that, under the Ministry of Environmental Protection guidelines, the soil needs further testing or treatment before construction. The calculator does not replace reading the full report or the opinion of an environmental consultant.' },
    formula: { he: 'פי כמה = הריכוז בננוגרם לק"ג ÷ ערך הסף. {label}: PFOS {pfos}, PFOA {pfoa}, PFHxS {pfhxs} ננוגרם לק"ג.',
      en: 'Times the threshold = the concentration in ng/kg ÷ the threshold. The {label}: PFOS {pfos}, PFOA {pfoa}, PFHxS {pfhxs} ng/kg.' },
    srcLabel: { he: 'דו"ח סקר הקרקע של מגרש 303, מאגר המשרד להגנת הסביבה', en: 'Soil survey report of plot 303, Ministry of Environmental Protection database (Hebrew PDF)' },
    share: { he: 'תוצאת מעבדה: {name} {ng} ננוגרם לק"ג = {x} מערך הסף למגע ישיר (שדה דב, יוני 2026).', en: 'Lab result: {name} {ng} ng/kg = {x} the direct-contact threshold (Sde Dov threshold values, June 2026).' },
    tTitle: { he: 'מול השיאים שפורסמו בשדה דב (PFOS)', en: 'Against the published Sde Dov peaks (PFOS)' },
    tPlot: { he: 'מגרש', en: 'Plot' },
    tPeak: { he: 'השיא בדו"ח', en: 'Report peak' },
    tVsTh: { he: 'מול הסף', en: 'Vs the threshold' },
    tVsYou: { he: 'מול הערך שלכם', en: 'Vs your value' },
    more: { he: 'פי {n} יותר', en: '{n}× higher' },
    less: { he: 'פי {n} פחות', en: '{n}× lower' }
  };
  var LABEL_EN = { 'ערכי סף למגע ישיר עבור שדה דב, יוני 2026 (כפי שמצוטטים בדו"חות)': 'direct-contact threshold values for Sde Dov, June 2026 (as quoted in the reports)' };
  window.NLPF = { compute: compute, UNIT: UNIT, TX: TX };
  if (!window.NadLanInstruments) return;
  var F = window.NadLanInstruments.fmt, EN = window.NadLanInstruments.lang === 'en';
  var T = window.NadLanInstruments.pick(TX, EN ? 'en' : 'he');
  function f(s, o) { return String(s).replace(/\{(\w+)\}/g, function (m, k) { return o[k] != null ? o[k] : m; }); }
  function label(d) { return EN && LABEL_EN[d.thresholdsLabel] ? LABEL_EN[d.thresholdsLabel] : d.thresholdsLabel; }
  function xs(x) { return x >= 1 ? f(T.times, { n: x >= 10 ? F.num(Math.round(x)) : F.num(x, 1) }) : f(T.pctOf, { n: F.num(x * 100, x < 0.1 ? 1 : 0) }); }
  function small(n) { return n >= 100 ? F.num(n) : n >= 1 ? F.num(n, 2) : F.num(n, 4); }
  window.NadLanInstruments.register('pfas', {
    kicker: T.kicker,
    title: T.title,
    lede: T.lede,
    defaults: function () { return { sub: 'pfos', val: 3780000, unit: 'ng' }; },
    fields: [
      { id: 'sub', label: T.fSub, type: 'segmented', options: [{ value: 'pfos', label: 'PFOS' }, { value: 'pfoa', label: 'PFOA' }, { value: 'pfhxs', label: 'PFHxS' }] },
      { id: 'val', label: T.fVal, type: 'number' },
      { id: 'unit', label: T.fUnit, type: 'segmented', options: [{ value: 'ng', label: T.uNg }, { value: 'ug', label: T.uUg }, { value: 'mg', label: T.uMg }],
        help: T.help }
    ],
    compute: function (v, data) {
      var d = data.soil, th = d.thresholds;
      if (!(v.val > 0)) return { error: { field: 'val', msg: T.errVal } };
      var r = compute(v.val, v.unit, v.sub, th), name = v.sub.toUpperCase(), over = r.x > 1;
      var rep = d.records.filter(function (x) { return x.status === 'published_report' && x.pfosMax; }).sort(function (a, b) { return b.pfosMax - a.pfosMax; });
      var out = {
        answer: { label: f(T.ansLab, { name: name }), value: xs(r.x), tone: over ? 'survey' : 'ink', sub: f(T.ansSub, { ng: F.num(r.ng), th: F.num(r.th, 1) }) },
        lines: [{ label: T.lNg, value: F.num(r.ng) }, { label: T.lUg, value: small(r.ng / 1e3) }, { label: T.lMg, value: small(r.ng / 1e6) },
          { label: f(T.lTh, { name: name }), value: f(T.ngVal, { n: F.num(r.th, 1) }) }],
        note: (over ? T.over : T.under) + T.note,
        formula: f(T.formula, { label: label(d), pfos: F.num(th.pfos, 1), pfoa: F.num(th.pfoa, 1), pfhxs: F.num(th.pfhxs, 1) }),
        sources: [{ label: T.srcLabel, url: (rep[0] || {}).src || 'https://www.gov.il/' }],
        text: f(T.share, { name: name, ng: F.num(r.ng), x: xs(r.x) })
      };
      if (v.sub === 'pfos' && rep.length) out.table = { title: T.tTitle, head: [T.tPlot, T.tPeak, T.tVsTh, T.tVsYou], num: [1, 2, 3], phoneHide: [1],
        rows: rep.map(function (x) { var k = x.pfosMax / r.ng; return [x.plot, F.num(x.pfosMax), xs(x.pfosX), k >= 1 ? f(T.more, { n: small(k) }) : f(T.less, { n: small(1 / k) })]; }) };
      return out;
    }
  });
})();
