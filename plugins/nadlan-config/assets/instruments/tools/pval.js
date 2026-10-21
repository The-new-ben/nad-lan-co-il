/* NadLan Instruments · pval v1 (HAD-575, Kikar HaMedina tools program #1, Ben 15.10 + 21.10.2026): what an apartment is worth.
   Two ways, one tool: (1) from the official closed deals: the median price for the room count in the neighbourhood (or the city
   when the neighbourhood has no published median in the last four quarters), from the Tax Authority summary files of the
   government real-estate site; (2) the old page's way, area x price per m2 plus balcony, parking and storage. Both then take the
   owner's adjustments (condition, floor / view / building), a safety range, and a check of an asking price. Every field of the
   old widget stays. Data: value.json (tools/instruments/build_value_data.py). Pure logic in NLPV for unit checks. */
(function () {
  'use strict';
  function base(v, d) {
    var c = d.cities[v.city]; if (!c) return null;
    var h = null; c.hoods.forEach(function (x) { if (String(x.id) === String(v.hood)) h = x; });
    var k = 'r' + v.rooms;
    if (h && h[k]) return { price: h[k][0], q: h[k][1], where: h.n, level: 'hood' };
    if (c[k]) return { price: c[k], q: c['q' + v.rooms] || c.q, where: v.city, level: 'city', hood: h ? h.n : '' };
    return null;
  }
  function compute(v, d) {
    var b = v.method === 'sqm' ? { price: (v.sqm || 0) * (v.ppsqm || 0) + (v.balcony || 0) * (v.balconyPrice || 0) + (v.parking || 0) + (v.storage || 0), level: 'sqm' } : base(v, d);
    if (!b || !(b.price > 0)) return null;
    var val = b.price * (1 + ((v.condition || 0) + (v.building || 0)) / 100), r = Math.max(0, v.range || 0) / 100;
    return { b: b, value: val, low: val * (1 - r), high: val * (1 + r), ppsqm: v.sqm > 0 ? val / v.sqm : 0, gap: v.asking > 0 ? (v.asking - val) / val : null };
  }
  window.NLPV = { base: base, compute: compute };
  if (!window.NadLanInstruments) return;
  var F = window.NadLanInstruments.fmt;
  window.NadLanInstruments.register('pval', {
    kicker: 'מחשבון · שווי דירה',
    title: 'כמה שווה הדירה',
    lede: 'עיר, שכונה ומספר חדרים: המחשבון מתחיל מהמחיר החציוני של העסקאות שנסגרו בשכונה לפי רשות המסים, מוסיף את ההתאמות שלכם, ובודק מחיר מבוקש. אפשר לעבור גם לחישוב לפי מחיר למ״ר.',
    strip: function (dd) { var d = dd.value, c = d.cities['תל אביב יפו']; return [{ label: 'ערים', value: F.num(Object.keys(d.cities).length) }, { label: 'שכונות', value: F.num(Object.keys(d.cities).reduce(function (s, k) { return s + d.cities[k].hoods.length; }, 0)) }, { label: '4 חדרים, תל אביב, ' + (c.q4 || c.q), value: F.ils(c.r4) }]; },
    defaults: function () { return { method: 'deals', city: 'תל אביב יפו', hood: '', rooms: 4, sqm: 100, ppsqm: 50000, balcony: 0, balconyPrice: 0, parking: 0, storage: 0, condition: 0, building: 0, range: 5, asking: 0 }; },
    fields: [
      { id: 'method', label: 'איך מחשבים', type: 'segmented', options: [{ value: 'deals', label: 'לפי עסקאות בשכונה' }, { value: 'sqm', label: 'לפי מחיר למ״ר' }] },
      { id: 'city', label: 'עיר', type: 'select', showIf: function (v) { return v.method === 'deals'; }, optionsFrom: function (v, d) { return Object.keys(d.value.cities).sort().map(function (k) { return { value: k, label: k }; }); } },
      { id: 'hood', label: 'שכונה', type: 'select', showIf: function (v) { return v.method === 'deals'; }, optionsFrom: function (v, d) {
          var c = d.value.cities[v.city]; var k = 'r' + v.rooms;
          return [{ value: '', label: 'כל העיר' }].concat((c ? c.hoods : []).map(function (h) { return { value: String(h.id), label: h.n + (h[k] ? '' : ' (חציון העיר)') }; })); } },
      { id: 'rooms', label: 'חדרים', type: 'segmented', showIf: function (v) { return v.method === 'deals'; }, options: [{ value: 3, label: '3' }, { value: 4, label: '4' }, { value: 5, label: '5' }] },
      { id: 'sqm', label: 'שטח הדירה', type: 'number', unit: 'מ״ר' },
      { id: 'ppsqm', label: 'מחיר ממוצע למ״ר באזור', type: 'money', unit: '₪', showIf: function (v) { return v.method === 'sqm'; } },
      { id: 'balcony', label: 'שטח מרפסת', type: 'number', unit: 'מ״ר', showIf: function (v) { return v.method === 'sqm'; } },
      { id: 'balconyPrice', label: 'שווי למ״ר מרפסת', type: 'money', unit: '₪', showIf: function (v) { return v.method === 'sqm'; } },
      { id: 'parking', label: 'שווי חניה', type: 'money', unit: '₪', showIf: function (v) { return v.method === 'sqm'; } },
      { id: 'storage', label: 'שווי מחסן', type: 'money', unit: '₪', showIf: function (v) { return v.method === 'sqm'; } },
      { id: 'condition', label: 'התאמה למצב הדירה', type: 'percent', unit: '%', help: 'למשל +5 לדירה משופצת, −10 לדירה שדורשת שיפוץ. ההחלטה שלכם.' },
      { id: 'building', label: 'התאמה לקומה, נוף ובניין', type: 'percent', unit: '%' },
      { id: 'range', label: 'טווח זהירות', type: 'percent', unit: '±%' },
      { id: 'asking', label: 'מחיר מבוקש לבדיקה', type: 'money', unit: '₪', help: '0 אם אין מחיר לבדוק.' }
    ],
    compute: function (v, d) {
      var D = d.value, r = compute(v, D);
      if (!r) return { error: { field: v.method === 'sqm' ? 'ppsqm' : 'hood', msg: v.method === 'sqm' ? 'הקלידו שטח ומחיר למ״ר.' : 'אין חציון פורסם למספר החדרים הזה. נסו מספר חדרים אחר.' } };
      var b = r.b, lines = [];
      if (b.level === 'hood') lines.push({ label: 'חציון ' + v.rooms + ' חדרים, ' + b.where + ', ' + b.q, value: F.ils(b.price) });
      else if (b.level === 'city') lines.push({ label: 'חציון ' + v.rooms + ' חדרים, ' + b.where + ', ' + b.q + (b.hood ? ' (לשכונה אין חציון שפורסם)' : ''), value: F.ils(b.price) });
      else lines.push({ label: 'שטח × מחיר למ״ר, מרפסת, חניה ומחסן', value: F.ils(b.price) });
      if (v.condition || v.building) lines.push({ label: 'ההתאמות שלכם', value: ((v.condition || 0) + (v.building || 0) > 0 ? '+' : '') + F.num((v.condition || 0) + (v.building || 0), 1) + '%' });
      if (r.ppsqm) lines.push({ label: 'מחיר למ״ר שיוצא', value: F.ils(r.ppsqm) });
      if (r.gap != null) lines.push({ label: 'המחיר המבוקש מול השווי', value: (r.gap > 0 ? '+' : '−') + F.num(Math.abs(100 * r.gap), 1) + '%' });
      var note = r.gap == null ? 'חציון הוא המחיר שחצי מהעסקאות מעליו וחצי מתחתיו. הוא כולל דירות חדשות וישנות, ולא מחליף שמאי.'
        : r.gap > 0.08 ? '<b>המחיר המבוקש גבוה משמעותית מהשווי.</b> כדאי לבדוק מה מצדיק את הפער: קומה, נוף, מצב או חניה.'
        : r.gap < -0.08 ? '<b>המחיר המבוקש נמוך משמעותית מהשווי.</b> כדאי לבדוק למה: מצב הדירה, זכויות, ליקויים או רישום.'
        : 'המחיר המבוקש קרוב לשווי לפי הנתונים.';
      var out = {
        answer: { label: 'שווי משוער', value: F.ils(r.value), tone: 'survey', sub: F.ils(r.low) + ' עד ' + F.ils(r.high) + ' · טווח ±' + F.num(v.range || 0) + '%' },
        breakdown: [{ label: 'מחיר בסיס', value: Math.min(b.price, r.value), kind: 'housing' }, { label: 'תוספת מההתאמות', value: Math.max(0, r.value - b.price), kind: 'open' }],
        lines: lines, note: note,
        formula: v.method === 'sqm' ? 'שווי = (שטח × מחיר למ״ר + מרפסת × מחיר למ״ר מרפסת + חניה + מחסן) × (1 + ההתאמות). הטווח: ± טווח הזהירות.' : 'שווי = החציון הרשמי לפי מספר החדרים × (1 + ההתאמות). הטווח: ± טווח הזהירות.',
        sources: [{ label: D.source + ', קובץ ' + D.file + ', נקרא ' + F.date(D.read), url: D.url }],
        text: 'שווי משוער: ' + F.ils(r.value) + ' (' + F.ils(r.low) + ' עד ' + F.ils(r.high) + ')' + (b.level !== 'sqm' ? ', ' + v.rooms + ' חדרים, ' + b.where : '') + '.'
      };
      if (v.method === 'deals') {
        var c = D.cities[v.city], k = 'r' + v.rooms;
        out.scenarioLabel = 'באותה שכונה, לפי מספר החדרים';
        out.scenarios = [3, 4, 5].map(function (n) { var x = base(Object.assign({}, v, { rooms: n }), D); return { key: String(n), name: n + ' חדרים' + (x && x.level === 'city' ? ' · העיר' : ''), value: x ? F.ils(x.price) : 'אין נתון' }; });
        var rows = c.hoods.filter(function (h) { return h[k]; }).sort(function (a, b) { return b[k][0] - a[k][0]; });
        out.table = { title: 'חציון ' + v.rooms + ' חדרים בשכונות ' + v.city, head: ['שכונה', 'חציון', 'רבעון'], num: [1], rows: rows.map(function (h) { return [h.n, F.ils(h[k][0]), h[k][1]]; }) };
      }
      return out;
    }
  });
})();
