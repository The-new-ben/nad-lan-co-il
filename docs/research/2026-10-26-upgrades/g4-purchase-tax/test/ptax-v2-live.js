/* NadLan Instruments · ptax v2 (HAD-527 v1; v2 HAD-592, the page loop, 22.10.2026, after the purchase-tax research:
   docs/research/2026-10-22-purchase-tax/brief.md). Purchase tax on an apartment by the Tax Authority's rules:
   - tracks: an only home, an additional home (and a company), a new immigrant (regulation 12A, capped at 20,183,565 ₪; or
     regulation 12 for an oleh who arrived before 15.8.2024), a foreign resident, a disabled buyer (regulation 11), land or a
     non-residential property (6%, 5% with a permit within 2 years), a gift to a relative (1/3 of the regular tax);
   - each track shows its own end date: the only-home brackets are frozen to 15.1.2028, the additional-home and foreign rate is
     a temporary order to 31.12.2026 (instruction 1/2026), extended to 10.2.2027 (Tax Authority notice 12.10.2026);
   - the upgrader mode: by the purchase date (24 months from 1.6.2025, 18 months from 1.6.2023, 12 months from receiving a
     contractor home, the later of them) and the war extension of instruction 2/2026, the date to sell the previous home by, and
     what missing it costs;
   - one-tap presets for the common cases; a part share; the effective rate; the tax bracket by bracket; every track side by side.
   Data: ptax.json. Pure logic in NLPT for unit checks (tax, trackTax, sellBy). */
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
  /* one track, with its special rules; returns { tax, rows, used } where used names the brackets actually applied */
  function trackTax(price, k, P, o) {
    o = o || {};
    if (k === 'oleh') {
      if (o.oleh12) return Object.assign(tax(price, P.oleh12), { used: 'oleh12' });
      if (price > P.oleh_cap) return Object.assign(tax(price, P.tracks.single), { used: 'single' });  // above the cap 12A does not apply
      return Object.assign(tax(price, P.tracks.oleh), { used: 'oleh' });
    }
    if (k === 'disabled') {
      var D = P.disabled;
      if (o.disSingle && price <= D.single_cap) { var f = P.tracks.single[0][0], part = Math.max(0, price - f); return { tax: part * D.rate, rows: [{ from: 0, to: f, rate: 0, part: Math.min(price, f), tax: 0 }].concat(part > 0 ? [{ from: f, to: Infinity, rate: D.rate, part: part, tax: part * D.rate }] : []), used: 'disabled' }; }
      return { tax: price * D.rate, rows: [{ from: 0, to: Infinity, rate: D.rate, part: price, tax: price * D.rate }], used: 'disabled' };
    }
    if (k === 'land') { var r = o.permit ? P.land_permit : P.land; return { tax: price * r, rows: [{ from: 0, to: Infinity, rate: r, part: price, tax: price * r }], used: 'land' }; }
    if (k === 'gift') { var base = tax(price, o.giftExtra ? P.tracks.extra : P.tracks.single); return { tax: base.tax * P.gift, rows: base.rows.map(function (x) { return Object.assign({}, x, { tax: x.tax * P.gift }); }), used: 'gift' }; }
    return Object.assign(tax(price, P.tracks[k] || P.tracks.single), { used: P.tracks[k] ? k : 'single' });
  }
  function d(iso) { var p = String(iso || '').split('-'); return p.length === 3 ? new Date(Date.UTC(+p[0], +p[1] - 1, +p[2])) : null; }
  function iso(dt) { return dt.toISOString().slice(0, 10); }
  function lastDay(y, m) { return new Date(Date.UTC(y, m + 1, 0)).getUTCDate(); }
  function addMonths(dt, n) {  // a period that starts on the last day of a month ends on the last day of the target month (instruction 2/2026 examples)
    var y = dt.getUTCFullYear(), m = dt.getUTCMonth() + n, day = dt.getUTCDate(), isLast = day === lastDay(y, dt.getUTCMonth());
    var ty = y + Math.floor(m / 12), tm = ((m % 12) + 12) % 12, ld = lastDay(ty, tm);
    return new Date(Date.UTC(ty, tm, isLast ? ld : Math.min(day, ld)));
  }
  function sellBy(P, buyIso, contractor, possIso) {
    var b = d(buyIso); if (!b) return null;
    var rule = P.upgrader.filter(function (r) { return b >= d(r.from); })[0];
    if (!rule) return { old: true };
    var end = addMonths(b, rule.months), how = rule.months + ' חודשים מהרכישה';
    if (contractor && d(possIso)) { var e2 = addMonths(d(possIso), P.contractor_months); if (e2 > end) { end = e2; how = P.contractor_months + ' חודשים מקבלת הדירה מהקבלן'; } }
    var W = P.war, ext = false;
    if (b <= d(W.to) && end >= d(W.from)) { var e3 = addMonths(end, W.plus_months), fl = d(W.floor); end = e3 > fl ? e3 : fl; ext = true; }
    return { date: iso(end), months: rule.months, how: how, ext: ext };
  }
  window.NLPT = { tax: tax, trackTax: trackTax, sellBy: sellBy, addMonths: addMonths };
  if (!window.NadLanInstruments) return;
  var F = window.NadLanInstruments.fmt;
  var NAMES = { single: 'דירה יחידה', extra: 'דירה נוספת', oleh: 'עולה חדש', foreign: 'תושב חוץ', disabled: 'נכה או נפגע', land: 'קרקע או נכס מסחרי', gift: 'מתנה לקרוב משפחה' };
  var NOTE = {
    single: 'יחיד תושב ישראל שזו הדירה היחידה שלו. מי שיש לו דירה וימכור אותה בזמן נחשב כאן: 24 חודשים לרכישה מ־1.6.2025, 18 חודשים לרכישה מ־1.6.2023 עד 31.5.2025, או 12 חודשים מקבלת דירה מקבלן, המאוחר מביניהם.',
    extra: 'למי שיש כבר דירה ולא ימכור אותה בזמן, ולחברה. השיעור הזה הוא הוראת שעה, שהוארכה לרכישות עד 10.2.2027; מה יחול אחר כך עוד לא פורסם.',
    oleh: 'תקנה 12א: מרכישה שנה לפני העלייה ועד 7 שנים אחריה, בדירה יחידה. מעל 20,183,565 ₪ ההקלה לא חלה ומחשבים כדירה יחידה.',
    foreign: 'מי שאינו תושב ישראל משלם כמו דירה נוספת, גם אם זו הדירה היחידה שלו, אלא אם יהפוך לתושב תוך שנתיים. הוראת שעה, הוארכה לרכישות עד 10.2.2027.',
    disabled: 'תקנה 11: נכה, עיוור, נפגע פעולות איבה ומשפחות שכולות, פעמיים בלבד. בדירה יחידה עד 2,500,000 ₪: פטור עד המדרגה הראשונה ו־0.5% על השאר. טופס 2973.',
    land: 'קרקע ונכס שאינו דירת מגורים: 6%. קרקע שיש עליה תכנית לדירה אחת לפחות, והיתר בנייה בתוך שנתיים: 5%.',
    gift: 'מתנה לקרוב (בן זוג, הורה, צאצא ובן זוגו, נכד, אח): שליש מהמס הרגיל. מתנה לבן זוג שגר עם הנותן בדירה: פטורה.'
  };
  function today() { var t = new Date(); return t.toISOString().slice(0, 10); }
  window.NadLanInstruments.register('ptax', {
    kicker: 'מחשבון · מס רכישה',
    title: 'כמה מס רכישה תשלמו על הדירה',
    lede: 'מחיר הדירה ומי הקונה: המחשבון מחשב את המס לפי המדרגות של רשות המסים בכל המסלולים, כולל עולים, נכים, קרקע ומתנה, מראה כמה נופל על כל מדרגה ועד מתי כל שיעור בתוקף, ולמשפרי דיור גם עד מתי למכור את הדירה הקודמת.',
    strip: function (dd) { var p = dd.ptax; return [{ label: 'פטור בדירה יחידה עד', value: F.ils(p.tracks.single[0][0]) }, { label: 'דירה יחידה: מוקפא עד', value: F.date(p.valid.single) }, { label: 'דירה נוספת ותושב חוץ: הוראת שעה עד', value: F.date(p.valid.extra) }]; },
    presets: [
      { key: 'first', label: 'דירה ראשונה', sub: '₪2,500,000', set: { price: 2500000, track: 'single', share: 100, upg: 'no' } },
      { key: 'upgrader', label: 'משפרי דיור', sub: '₪3,500,000 · מוכרים את הישנה', set: { price: 3500000, track: 'single', share: 100, upg: 'yes', contractor: 'no', bdate: today() } },
      { key: 'investor', label: 'דירה להשקעה', sub: '₪2,000,000', set: { price: 2000000, track: 'extra', share: 100, upg: 'no' } },
      { key: 'oleh', label: 'עולה חדש', sub: '₪4,000,000', set: { price: 4000000, track: 'oleh', share: 100, oleh12: 'no' } },
      { key: 'contractor', label: 'דירה מקבלן', sub: '₪3,000,000 כולל מע״מ', set: { price: 3000000, track: 'single', share: 100, upg: 'yes', contractor: 'yes', bdate: today() } },
      { key: 'half', label: 'חצי דירה', sub: '₪2,000,000 · 50%', set: { price: 2000000, track: 'single', share: 50, upg: 'no' } },
      { key: 'disabled', label: 'נכה, דירה יחידה', sub: '₪2,400,000', set: { price: 2400000, track: 'disabled', share: 100, disSingle: 'yes' } },
      { key: 'gift', label: 'מתנה לבן או לבת', sub: 'דירה בשווי ₪2,800,000', set: { price: 2800000, track: 'gift', share: 100, giftExtra: 'no' } }
    ],
    defaults: function () { return { price: 3000000, track: 'single', share: 100, upg: 'no', bdate: today(), contractor: 'no', pdate: '', oleh12: 'no', disSingle: 'yes', permit: 'no', giftExtra: 'no' }; },
    fields: [
      { id: 'price', label: 'מחיר הדירה', type: 'money', unit: '₪', help: 'המחיר בחוזה. בדירה מקבלן, המחיר כולל מע״מ.' },
      { id: 'track', label: 'מי קונה', type: 'segmented', options: [{ value: 'single', label: 'דירה יחידה' }, { value: 'extra', label: 'דירה נוספת' }, { value: 'oleh', label: 'עולה חדש' }, { value: 'foreign', label: 'תושב חוץ' }, { value: 'disabled', label: 'נכה' }, { value: 'land', label: 'קרקע או מסחרי' }, { value: 'gift', label: 'מתנה' }] },
      { id: 'upg', label: 'יש לכם דירה שתמכרו?', type: 'segmented', options: [{ value: 'no', label: 'לא' }, { value: 'yes', label: 'כן, משפרי דיור' }], showIf: function (v) { return v.track === 'single'; } },
      { id: 'bdate', label: 'מועד הרכישה של הדירה החדשה', type: 'date', showIf: function (v) { return v.track === 'single' && v.upg === 'yes'; } },
      { id: 'contractor', label: 'דירה מקבלן?', type: 'segmented', options: [{ value: 'no', label: 'לא' }, { value: 'yes', label: 'כן' }], showIf: function (v) { return v.track === 'single' && v.upg === 'yes'; } },
      { id: 'pdate', label: 'מועד קבלת הדירה מהקבלן (צפוי)', type: 'date', showIf: function (v) { return v.track === 'single' && v.upg === 'yes' && v.contractor === 'yes'; } },
      { id: 'oleh12', label: 'עליתם לפני 15.8.2024 ובוחרים בתקנה 12?', type: 'segmented', options: [{ value: 'no', label: 'לא' }, { value: 'yes', label: 'כן' }], showIf: function (v) { return v.track === 'oleh'; } },
      { id: 'disSingle', label: 'זו הדירה היחידה?', type: 'segmented', options: [{ value: 'yes', label: 'כן' }, { value: 'no', label: 'לא' }], showIf: function (v) { return v.track === 'disabled'; } },
      { id: 'permit', label: 'יש תכנית למגורים והיתר בתוך שנתיים?', type: 'segmented', options: [{ value: 'no', label: 'לא' }, { value: 'yes', label: 'כן' }], showIf: function (v) { return v.track === 'land'; } },
      { id: 'giftExtra', label: 'למקבל המתנה יש דירה אחרת?', type: 'segmented', options: [{ value: 'no', label: 'לא' }, { value: 'yes', label: 'כן' }], showIf: function (v) { return v.track === 'gift'; } },
      { id: 'share', label: 'החלק שאתם קונים', type: 'percent', unit: '%', help: 'קונים חצי דירה? 50. המס מחושב על כל הדירה, וכל קונה משלם לפי החלק שלו.' }
    ],
    compute: function (v, dd) {
      var P = dd.ptax;
      if (!(v.price >= 100000 && v.price <= 500000000)) return { error: { field: 'price', msg: 'הקלידו את מחיר הדירה בשקלים.' } };
      if (!(v.share > 0 && v.share <= 100)) return { error: { field: 'share', msg: 'החלק שאתם קונים: בין 1 ל־100 אחוז.' } };
      var k = NAMES[v.track] ? v.track : 'single', s = v.share / 100;
      var o = { oleh12: v.oleh12 === 'yes', disSingle: v.disSingle !== 'no', permit: v.permit === 'yes', giftExtra: v.giftExtra === 'yes' };
      var full = trackTax(v.price, k, P, o), t = full.tax * s, part = v.price * s;
      var last = full.rows[full.rows.length - 1];
      var single = tax(v.price, P.tracks.single).tax * s, extra = tax(v.price, P.tracks.extra).tax * s;
      var lines = [
        { label: 'שיעור המס האפקטיבי', value: F.num(part ? 100 * t / part : 0, 2) + '%' },
        { label: 'המדרגה של השקל האחרון', value: F.num(100 * (last ? last.rate : 0), 1) + '%' },
        { label: 'המחיר עם המס', value: F.ils(part + t) }
      ];
      if (k !== 'single') lines.push({ label: 'לעומת דירה יחידה באותו מחיר', value: (t >= single ? '+' : '−') + F.ils(Math.abs(t - single)) });
      if (P.valid[full.used]) lines.push({ label: 'השיעור בתוקף עד', value: F.date(P.valid[full.used]) + (full.used === 'extra' || full.used === 'foreign' ? ' (הוראת שעה)' : '') });
      var notes = ['<b>' + NAMES[k] + ':</b> ' + NOTE[k]];
      if (k === 'oleh' && full.used === 'single') notes.push('המחיר מעל 20,183,565 ₪, ולכן ההקלה לעולה לא חלה והמס מחושב כדירה יחידה.');
      if (k === 'single' && v.upg === 'yes') {
        var sb = sellBy(P, v.bdate, v.contractor === 'yes', v.pdate);
        if (sb && sb.old) notes.push('<b>רכישה לפני 1.6.2023:</b> חלו כללים אחרים והארכות שונות. בדקו את המועד מול רשות המסים או עם עורך הדין.');
        else if (sb) {
          lines.unshift({ label: 'למכור את הדירה הקודמת עד', value: F.date(sb.date) });
          notes.push('<b>עד ' + F.date(sb.date) + '</b> (' + sb.how + (sb.ext ? ', כולל הארכת המלחמה לפי הוראה 2/2026' : '') + '). מי שלא ימכור בזמן ישלם את ההפרש לדירה נוספת, כאן ' + F.ils(extra - single) + ', ועוד הצמדה וריבית.');
        }
      }
      if ((k === 'extra' || k === 'foreign') && v.bdate && d(v.bdate) && d(v.bdate) > d(P.valid.extra)) notes.push('<b>עסקה אחרי 10.2.2027:</b> הוראת השעה של 8% ו־10% מסתיימת, ומה יחול אחריה עוד לא פורסם.');
      var SC = ['single', 'extra', 'oleh', 'foreign', 'disabled'];
      return {
        answer: { label: 'מס הרכישה, ' + NAMES[k] + (s < 1 ? ', ' + F.num(v.share) + '% מהדירה' : ''), value: F.ils(t), tone: t > 0 ? 'survey' : 'ink',
          sub: t > 0 ? F.num(100 * t / part, 2) + '% מהמחיר' + (s < 1 ? ' של החלק שלכם' : '') : 'במחיר הזה אין מס רכישה' },
        breakdown: [{ label: 'מחיר', value: part, kind: 'housing' }, { label: 'מס רכישה', value: t, kind: 'survey' }],
        lines: lines,
        note: notes.join('<br>'),
        scenarioLabel: 'אותו מחיר, בכל מסלול',
        scenarios: SC.map(function (x) { return { key: x, name: NAMES[x], value: F.ils(trackTax(v.price, x, P, o).tax * s), on: x === k }; }),
        table: { title: 'המס מדרגה אחרי מדרגה, ' + NAMES[k], head: ['מדרגה', 'שיעור', 'הסכום במדרגה', 'המס'], num: [2, 3],
          rows: full.rows.map(function (r) { return [(r.from ? F.ils(r.from) : '₪0') + ' עד ' + (r.to === Infinity ? 'מעל' : F.ils(r.to)), F.num(100 * r.rate, 1) + '%' + (k === 'gift' ? ' × שליש' : ''), F.ils(r.part * s), F.ils(r.tax * s)]; }) },
        formula: 'מס רכישה = סכום על כל המדרגות של (החלק מהמחיר שנופל במדרגה × שיעור המדרגה), כפול החלק שאתם קונים. המדרגות חלות על שווי הדירה כולה.',
        sources: [{ label: P.instruction.label, url: P.instruction.url }, { label: P.guide.label, url: P.guide.url }, { label: P.source + ', נבדק ' + F.date(P.checked), url: P.url }].concat(k === 'single' && v.upg === 'yes' ? [{ label: P.war.label, url: P.war.url }] : []).concat((k === 'extra' || k === 'foreign') && P.extension ? [{ label: P.extension.label, url: P.extension.url }] : []),
        text: 'מס רכישה, ' + NAMES[k] + ': דירה ב־' + F.ils(v.price) + (s < 1 ? ', ' + F.num(v.share) + '% מהדירה' : '') + ' = ' + F.ils(t) + ' (' + F.num(part ? 100 * t / part : 0, 2) + '%).'
      };
    }
  });
})();
