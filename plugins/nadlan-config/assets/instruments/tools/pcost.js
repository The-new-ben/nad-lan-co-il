/* NadLan Instruments · pcost v1 (HAD-575, Kikar HaMedina tools program #3, Ben 15.10 + 21.10.2026): how much money a buyer
   really needs. The purchase tax comes from the ptax brackets by itself (all four tracks), then the lawyer and broker fees with
   VAT, the bank appraiser and inspection, the mortgage file fee, moving, renovation, furniture and a safety margin, and the
   equity left after the mortgage, with the Bank of Israel financing cap for the buyer's track. Every field of the old widget
   stays. Data: ptax.json (Tax Authority) + cost.json (VAT, market fee ranges with source and date, LTV caps).
   Pure logic in NLPC for unit checks. */
(function () {
  'use strict';
  function ptax(price, br) {
    var t = 0, lo = 0;
    for (var i = 0; i < br.length; i++) {
      var hi = br[i][0] == null ? Infinity : br[i][0], top = Math.min(price, hi);
      if (top > lo) t += (top - lo) * br[i][1];
      if (price <= hi) break;
      lo = hi;
    }
    return t;
  }
  function compute(v, P, C) {
    var k = P.tracks[v.track] ? v.track : 'single', vat = 1 + C.vat;
    var tax = ptax(v.price, k === 'oleh' && P.oleh_cap && v.price > P.oleh_cap ? P.tracks.single : P.tracks[k]);  // 1.72.500: above the cap regulation 12A does not apply
    var lawyer = v.price * (v.lawyer || 0) / 100 * vat;
    var broker = v.kind === 'second' ? v.price * (v.broker || 0) / 100 * vat : 0;
    var mfee = v.loan > 0 ? Math.min(v.loan * C.mortgage_fee.rate, C.mortgage_fee.max) : 0;
    var deal = tax + lawyer + broker + mfee + (v.checks || 0);
    var living = (v.moving || 0) + (v.renovation || 0) + (v.furniture || 0);
    var equity = v.price - (v.loan || 0) + deal + living + (v.reserve || 0);
    return { k: k, tax: tax, lawyer: lawyer, broker: broker, mfee: mfee, deal: deal, living: living, equity: equity,
             ltv: v.price ? (v.loan || 0) / v.price : 0, cap: C.ltv[k] };
  }
  window.NLPC = { ptax: ptax, compute: compute };
  if (!window.NadLanInstruments) return;
  var F = window.NadLanInstruments.fmt;
  var NAMES = { single: 'דירה יחידה', extra: 'דירה נוספת', oleh: 'עולה חדש', foreign: 'תושב חוץ' };
  window.NadLanInstruments.register('pcost', {
    kicker: 'מחשבון · קניית דירה',
    title: 'כמה כסף צריך באמת כדי לקנות את הדירה',
    lede: 'מחיר הדירה, מי קונה וכמה משכנתא: המחשבון מוסיף לבד את מס הרכישה לפי המסלול, את עורך הדין והתיווך עם מע״מ, את השמאי, הבדיקות ופתיחת התיק, את המעבר והשיפוץ, ומראה כמה הון עצמי צריך להכין.',
    strip: function (d) { return [{ label: 'מע״מ על שכר טרחה', value: F.num(100 * d.cost.vat) + '%' }, { label: 'מימון מרבי, דירה יחידה', value: F.num(100 * d.cost.ltv.single) + '%' }, { label: 'מימון מרבי, דירה נוספת', value: F.num(100 * d.cost.ltv.extra) + '%' }]; },
    defaults: function () { return { price: 3000000, kind: 'second', track: 'single', loan: 1500000, lawyer: 0.5, broker: 2, checks: 2650, moving: 12000, renovation: 80000, furniture: 40000, reserve: 50000 }; },
    fields: [
      { id: 'price', label: 'מחיר הדירה', type: 'money', unit: '₪' },
      { id: 'kind', label: 'סוג הדירה', type: 'segmented', options: [{ value: 'second', label: 'יד שנייה' }, { value: 'new', label: 'מקבלן' }] },
      { id: 'track', label: 'מי קונה', type: 'segmented', options: [{ value: 'single', label: 'דירה יחידה' }, { value: 'extra', label: 'דירה נוספת' }, { value: 'oleh', label: 'עולה חדש' }, { value: 'foreign', label: 'תושב חוץ' }] },
      { id: 'loan', label: 'משכנתא', type: 'money', unit: '₪', help: '0 אם קונים בלי משכנתא.' },
      { id: 'lawyer', label: 'עורך דין', type: 'percent', unit: '%', help: 'לרוב 0.5% עד 1% מהמחיר, ועוד מע״מ.' },
      { id: 'broker', label: 'תיווך', type: 'percent', unit: '%', help: 'מקובל 2% ועוד מע״מ. 0 אם אין מתווך.', showIf: function (v) { return v.kind === 'second'; } },
      { id: 'checks', label: 'שמאי ובדק בית', type: 'money', unit: '₪', help: 'שמאי לבנק 350 עד 950 ₪, בדק בית 1,500 עד 2,500 ₪.' },
      { id: 'moving', label: 'מעבר והובלה', type: 'money', unit: '₪' },
      { id: 'renovation', label: 'שיפוץ ותיקונים לפני הכניסה', type: 'money', unit: '₪' },
      { id: 'furniture', label: 'ריהוט ומכשירי חשמל', type: 'money', unit: '₪' },
      { id: 'reserve', label: 'מרווח ביטחון אחרי הקנייה', type: 'money', unit: '₪' }
    ],
    compute: function (v, d) {
      var P = d.ptax, C = d.cost;
      if (!(v.price >= 100000 && v.price <= 500000000)) return { error: { field: 'price', msg: 'הקלידו את מחיר הדירה בשקלים.' } };
      if (!(v.loan >= 0 && v.loan < v.price)) return { error: { field: 'loan', msg: 'המשכנתא צריכה להיות קטנה ממחיר הדירה.' } };
      var r = compute(v, P, C), over = r.ltv > r.cap + 1e-9;
      var lines = [
        { label: 'עלויות העסקה, מעבר למחיר', value: F.ils(r.deal) + ' · ' + F.num(100 * r.deal / v.price, 1) + '%' },
        { label: 'מס רכישה, ' + NAMES[r.k], value: F.ils(r.tax) },
        { label: 'עורך דין, כולל מע״מ', value: F.ils(r.lawyer) }
      ];
      if (v.kind === 'second') lines.push({ label: 'תיווך, כולל מע״מ', value: F.ils(r.broker) });
      lines.push({ label: 'שמאי ובדק בית', value: F.ils(v.checks || 0) });
      if (v.loan > 0) lines.push({ label: 'פתיחת תיק משכנתא', value: F.ils(r.mfee) });
      lines.push({ label: 'מעבר, שיפוץ וריהוט', value: F.ils(r.living) });
      lines.push({ label: 'שיעור המימון', value: F.num(100 * r.ltv, 1) + '% · מרבי ' + F.num(100 * r.cap) + '%' });
      return {
        answer: { label: 'ההון העצמי שצריך להכין', value: F.ils(r.equity), tone: 'survey',
          sub: 'מתוכו ' + F.ils(r.deal) + ' עלויות עסקה (' + F.num(100 * r.deal / v.price, 1) + '% מהמחיר)' + (over ? ' · המשכנתא מעל המימון המרבי' : '') },
        breakdown: [{ label: 'הון עצמי לדירה', value: v.price - (v.loan || 0), kind: 'housing' }, { label: 'מס רכישה', value: r.tax, kind: 'survey' },
          { label: 'עורך דין, תיווך ובדיקות', value: r.lawyer + r.broker + r.mfee + (v.checks || 0), kind: 'civic' }, { label: 'מעבר, שיפוץ וריהוט', value: r.living, kind: 'open' },
          { label: 'מרווח ביטחון', value: v.reserve || 0, kind: 'sea' }],
        lines: lines,
        scenarioLabel: 'אותה עסקה, בכל מסלול',
        scenarios: ['single', 'extra', 'oleh', 'foreign'].map(function (x) { return { key: x, name: NAMES[x], value: F.ils(compute(Object.assign({}, v, { track: x }), P, C).equity) }; }),
        note: over ? '<b>המשכנתא גבוהה מהמותר:</b> לפי בנק ישראל, ב' + NAMES[r.k] + ' הבנק יממן עד ' + F.num(100 * r.cap) + '% משווי הדירה, כלומר עד ' + F.ils(v.price * r.cap) + '.'
          : 'עלויות השוק הן טווחים מקובלים, לא הצעת מחיר. את מס הרכישה הסופי קובעת רשות המסים.',
        table: { title: 'כל ההוצאות, שורה אחרי שורה', head: ['הוצאה', 'סכום', 'איך חושב'], num: [1],
          rows: [['מחיר הדירה', F.ils(v.price), 'המחיר בחוזה'], ['מס רכישה', F.ils(r.tax), 'מדרגות רשות המסים, ' + NAMES[r.k]],
            ['עורך דין', F.ils(r.lawyer), F.num(v.lawyer || 0, 2) + '% ועוד מע״מ ' + F.num(100 * C.vat) + '%']]
            .concat(v.kind === 'second' ? [['תיווך', F.ils(r.broker), F.num(v.broker || 0, 2) + '% ועוד מע״מ']] : [])
            .concat([['שמאי ובדק בית', F.ils(v.checks || 0), 'הסכום שהזנתם'], ['פתיחת תיק משכנתא', F.ils(r.mfee), '0.25% מההלוואה, עד ' + F.ils(C.mortgage_fee.max)],
              ['מעבר, שיפוץ וריהוט', F.ils(r.living), 'הסכומים שהזנתם'], ['מרווח ביטחון', F.ils(v.reserve || 0), 'הסכום שהזנתם'], ['משכנתא', '−' + F.ils(v.loan || 0), 'ההלוואה מהבנק'],
              ['הון עצמי', F.ils(r.equity), 'מחיר − משכנתא + כל ההוצאות']]) },
        formula: 'הון עצמי = מחיר הדירה − משכנתא + מס רכישה + (עורך דין + תיווך) × 1.18 + שמאי ובדיקות + פתיחת תיק + מעבר, שיפוץ וריהוט + מרווח ביטחון.',
        sources: [{ label: P.source + ', נבדק ' + F.date(P.checked), url: P.url }].concat(C.sources),
        text: 'קניית דירה ב־' + F.ils(v.price) + ' (' + NAMES[r.k] + ', משכנתא ' + F.ils(v.loan || 0) + '): הון עצמי ' + F.ils(r.equity) + ', מתוכו ' + F.ils(r.deal) + ' עלויות עסקה.'
      };
    }
  });
})();
