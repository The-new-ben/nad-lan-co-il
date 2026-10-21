/* NadLan Instruments · arnona v1 (HAD-575, Kikar HaMedina tools program #4, Ben 15.10 + 21.10.2026): residential arnona in
   Tel Aviv-Yafo for 2026, straight from the city's arnona order: the zone (1-5), the building type by the year it was completed
   (2.1), villa or apartment, the area with balconies (1.3), the rate table (2.3: zones 1-2 split apartments up to 140 m2 and
   above; the order gives ONE rate to the whole area, so 141 m2 costs more than the band would suggest), a personal discount
   (section 6, with its area cap), and the six bi-monthly payments (1.4). Data: arnona-tlv.json
   (docs/research/2026-10-21-kikar-tools/arnona/). Pure logic in NLAR for unit checks. */
(function () {
  'use strict';
  function rowFor(v, A) {
    if (v.kind === 'villa') return A.rows.villa;
    return v.featured ? A.rows.featured : A.rows.plain;
  }
  function column(zone, kind, area, T) {
    if (zone >= 4) return 'z4_5_all';
    if (zone === 3) return 'z3_all';
    var big = kind === 'villa' || area > T;
    return 'z' + zone + (big ? '_villa_any_or_apt_over_140' : '_apt_upto_140');
  }
  function round(a) { return Math.ceil(a - 0.5); }  // 1.3.1.א: to the nearest m2, half a m2 down
  function compute(v, A) {
    var area = round(v.area || 0), letter = rowFor(v, A)[v.built], type = A.typeRow[letter];
    var col = column(+v.zone, v.kind, area, A.threshold), rate = A.rates[type][col];
    var annual = area * rate, disc = null, off = 0;
    A.discounts.forEach(function (x) { if (x.id === v.discount) disc = x; });
    if (disc) off = (disc.cap ? Math.min(area, disc.cap) : area) * rate * disc.pct / 100;
    var alt = null;  // the 140 m2 line: what the same home would cost one band down
    if (+v.zone <= 2 && v.kind !== 'villa' && area > A.threshold) alt = A.threshold * A.rates[type][column(+v.zone, 'apt', A.threshold, A.threshold)];
    return { area: area, letter: letter, type: type, col: col, rate: rate, annual: annual, disc: disc, off: off, net: annual - off, bi: (annual - off) / 6, alt: alt };
  }
  window.NLAR = { compute: compute, round: round };
  if (!window.NadLanInstruments) return;
  var F = window.NadLanInstruments.fmt;
  var BANDS = { '2022+': '2022 ואילך', '2010-2021': '2010 עד 2021', '1992-2009': '1992 עד 2009', '1984-1991': '1984 עד 1991', '1975-1983': '1975 עד 1983', '1970-1974': '1970 עד 1974', '1960-1969': '1960 עד 1969', '1940-1959': '1940 עד 1959', 'up to 1939': 'עד 1939' };
  window.NadLanInstruments.register('arnona', {
    kicker: 'מחשבון · ארנונה',
    title: 'כמה ארנונה תשלמו בתל אביב',
    lede: 'אזור, שנת הבנייה, שטח הדירה עם המרפסות והנחה אם מגיעה לכם: המחשבון מחשב את הארנונה לשנת 2026 לפי צו הארנונה של העירייה, ומראה כמה יוצא כל תשלום דו־חודשי.',
    strip: function (d) { var r = d.arnona.rates['אא']; return [{ label: 'בניין חדש, אזור 1, עד 140 מ״ר', value: F.num(r.z1_apt_upto_140, 2) + ' ₪ למ״ר' }, { label: 'מעל 140 מ״ר', value: F.num(r.z1_villa_any_or_apt_over_140, 2) + ' ₪' }, { label: 'אזורים 4 ו־5', value: F.num(r.z4_5_all, 2) + ' ₪' }]; },
    defaults: function () { return { zone: 1, built: '2022+', kind: 'apt', featured: true, area: 100, discount: '' }; },
    fields: [
      { id: 'zone', label: 'אזור הארנונה', type: 'segmented', options: [1, 2, 3, 4, 5].map(function (z) { return { value: z, label: String(z) }; }), help: 'האזור כתוב בשובר. כיכר המדינה וצפון העיר הוותיק באזור 1.' },
      { id: 'built', label: 'שנת גמר הבנייה', type: 'select', optionsFrom: function (v, d) { return d.arnona.bands.map(function (b) { return { value: b, label: BANDS[b] || b }; }); } },
      { id: 'kind', label: 'סוג הנכס', type: 'segmented', options: [{ value: 'apt', label: 'דירה בבניין' }, { value: 'villa', label: 'וילה או בית בכניסה נפרדת' }] },
      { id: 'featured', label: 'בגמר הבנייה היו בבניין חימום מרכזי או מעלית', type: 'segmented', options: [{ value: true, label: 'כן' }, { value: false, label: 'לא' }],
        showIf: function (v) { return v.kind === 'apt' && ['1975-1983', '1970-1974', '1960-1969', '1940-1959', 'up to 1939'].indexOf(v.built) >= 0; } },
      { id: 'area', label: 'שטח הדירה, כולל מרפסות', type: 'number', unit: 'מ״ר', help: 'מרפסות נכללות במלואן. חניה וקירות לא נכללים. גג צמוד נכלל עד 30% משטח הדירה.' },
      { id: 'discount', label: 'הנחה', type: 'select', optionsFrom: function (v, d) { return [{ value: '', label: 'בלי הנחה' }].concat(d.arnona.discounts.map(function (x) { return { value: x.id, label: x.n + ' · ' + F.num(x.pct, x.pct % 1 ? 2 : 0) + '%' + (x.cap ? ' עד ' + x.cap + ' מ״ר' : '') }; })); } }
    ],
    compute: function (v, d) {
      var A = d.arnona;
      if (!(v.area >= 10 && v.area <= 2000)) return { error: { field: 'area', msg: 'הקלידו את שטח הדירה במ״ר.' } };
      var r = compute(v, A), lines = [
        { label: 'התעריף לשנה', value: F.num(r.rate, 2) + ' ₪ למ״ר' },
        { label: 'סוג הבניין בצו', value: r.letter },
        { label: 'השטח לחיוב', value: F.num(r.area) + ' מ״ר' },
        { label: 'ארנונה לשנה, לפני הנחה', value: F.ils(r.annual) }
      ];
      if (r.disc) lines.push({ label: 'הנחה: ' + r.disc.n, value: '−' + F.ils(r.off) });
      lines.push({ label: 'תשלום דו־חודשי (6 בשנה)', value: F.ils(r.bi) });
      var note = r.alt != null ? '<b>שימו לב לגבול של 140 מ״ר:</b> מעל 140 מ״ר כל הדירה מחויבת בתעריף הגבוה. אותה דירה ב־140 מ״ר הייתה עולה ' + F.ils(r.alt) + ' בשנה, ' + F.ils(r.annual - r.alt) + ' פחות.'
        : (r.disc && r.disc.income ? 'ההנחה הזאת ניתנת לפי מבחן הכנסה. את הזכאות קובעת העירייה.' : 'התשלומים הדו־חודשיים צמודים למדד. מי שמשלם את כל השנה עד 31 בינואר לא משלם הפרשי הצמדה.');
      return {
        answer: { label: 'ארנונה לשנה' + (r.disc ? ', אחרי ההנחה' : ''), value: F.ils(r.net), tone: 'survey', sub: F.ils(r.bi) + ' כל חודשיים · ' + F.num(r.rate, 2) + ' ₪ למ״ר' },
        breakdown: r.disc ? [{ label: 'משלמים', value: r.net, kind: 'housing' }, { label: 'ההנחה', value: r.off, kind: 'open' }] : null,
        lines: lines, note: note,
        scenarioLabel: 'אותה דירה, בכל אזור',
        scenarios: [1, 2, 3, 4, 5].map(function (z) { return { key: String(z), name: 'אזור ' + z, value: F.ils(compute(Object.assign({}, v, { zone: z }), A).net) }; }),
        table: { title: 'תעריפי מגורים 2026 לבניין מסוג ' + r.letter + ' (₪ למ״ר לשנה)', head: ['אזור', 'דירה עד 140 מ״ר', 'מעל 140 מ״ר או וילה'], num: [1, 2],
          rows: [['1', F.num(A.rates[r.type].z1_apt_upto_140, 2), F.num(A.rates[r.type].z1_villa_any_or_apt_over_140, 2)], ['2', F.num(A.rates[r.type].z2_apt_upto_140, 2), F.num(A.rates[r.type].z2_villa_any_or_apt_over_140, 2)],
            ['3', F.num(A.rates[r.type].z3_all, 2), F.num(A.rates[r.type].z3_all, 2)], ['4 ו־5', F.num(A.rates[r.type].z4_5_all, 2), F.num(A.rates[r.type].z4_5_all, 2)]] },
        formula: 'ארנונה לשנה = שטח הדירה (כולל מרפסות, מעוגל למ״ר) × התעריף לפי האזור, סוג הבניין והשטח. הנחה = שיעור ההנחה × התעריף × השטח עד תקרת ההנחה.',
        sources: [{ label: A.source + ', נבדק ' + F.date(A.checked), url: A.url }],
        text: 'ארנונה בתל אביב 2026: אזור ' + v.zone + ', ' + F.num(r.area) + ' מ״ר, בניין מסוג ' + r.letter + ': ' + F.ils(r.net) + ' לשנה, ' + F.ils(r.bi) + ' כל חודשיים.'
      };
    }
  });
})();
