/* NadLan Instruments · ptax v3 (HAD-527 v1; v2 HAD-592, 22.10.2026; v3 G4 of the upgrade loop, 26.10.2026, spec:
   docs/research/2026-10-26-upgrades/g4-purchase-tax/dna.md section 8). Purchase tax on an apartment by the Tax Authority's rules.
   v2 (kept, answers unchanged on every v2 case; test: docs/research/2026-10-26-upgrades/g4-purchase-tax/test/test_ptax_v3.js):
   - tracks: an only home, an additional home (and a company), a new immigrant (regulation 12A, capped at 20,183,565 ₪; or
     regulation 12 for an oleh who arrived before 15.8.2024), a foreign resident, a disabled buyer (regulation 11), land or a
     non-residential property (6%, 5% with a permit within 2 years), a gift to a relative (1/3 of the regular tax);
   - each track shows its own end date: the only-home brackets are frozen to 15.1.2028, the additional-home and foreign rate is
     a temporary order to 31.12.2026 (instruction 1/2026), extended to 10.2.2027 (Tax Authority notice 12.10.2026);
   - the upgrader mode: by the purchase date (24 months from 1.6.2025, 18 months from 1.6.2023, 12 months from receiving a
     contractor home, the later of them) and the war extension of instruction 2/2026, the date to sell the previous home by;
   - one-tap presets; a part share; the effective rate; the tax bracket by bracket; every track side by side.
   v3 adds (all from the Tax Authority's 2026 buyer guide pp. 11, 52, 58-59 and instructions 1/2026, 2/2026):
   - the deal date for every track, and the timeline it starts: the declaration (30 days, s.73), the payment date (60 days, s.90a,
     or later under s.51 when possession, over half the price and a registration power of attorney all come later), the sell-by
     date of an upgrader and the resident-by date of a foreign buyer, each with a countdown from today;
   - late payment: 0.2% of the tax for every week (s.94b), plus linkage and interest (named, not computed), the 2026 fines for a late
     declaration (310 ₪ per two weeks, instruction 1/2026), a what-if field for weeks late;
   - olim: the aliyah date checks the window (from a year before aliyah to 7 years after, instruction 1/2026 s.2c), and regulation 12
     against 12A side by side when the oleh arrived before 15.8.2024;
   - a foreign buyer who becomes an Israeli resident within 2 years pays as an only home (s.9(c1)(c4)(b), war extension included);
   - two buyers who are not one family: each pays on the whole value by his own status, times his share (guide p.51);
   - the distance to the next bracket and the tax on every extra 100,000 ₪ of price;
   - a link that reopens the same numbers (#ptax=...), sent with the copied or shared result.
   Data: ptax.json. Pure logic in NLPT for unit checks (tax, trackTax, sellBy, payDue, resBy, olehWin, lateFine, enc, dec). */
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
  function d(iso) { var p = String(iso || '').split('-'); return p.length === 3 && +p[0] > 1900 ? new Date(Date.UTC(+p[0], +p[1] - 1, +p[2])) : null; }
  function iso(dt) { return dt.toISOString().slice(0, 10); }
  function lastDay(y, m) { return new Date(Date.UTC(y, m + 1, 0)).getUTCDate(); }
  function addMonths(dt, n) {  // a period that starts on the last day of a month ends on the last day of the target month (instruction 2/2026 examples)
    var y = dt.getUTCFullYear(), m = dt.getUTCMonth() + n, day = dt.getUTCDate(), isLast = day === lastDay(y, dt.getUTCMonth());
    var ty = y + Math.floor(m / 12), tm = ((m % 12) + 12) % 12, ld = lastDay(ty, tm);
    return new Date(Date.UTC(ty, tm, isLast ? ld : Math.min(day, ld)));
  }
  function addDays(dt, n) { return new Date(dt.getTime() + n * 86400000); }
  /* the war extension of instruction 2/2026: a period that touches 28.2 to 31.5.2026 by one day ends 3 months later, at least on 31.8.2026 */
  function warExt(P, start, end) {
    var W = P.war;
    if (start <= d(W.to) && end >= d(W.from)) { var e3 = addMonths(end, W.plus_months), fl = d(W.floor); return { end: e3 > fl ? e3 : fl, ext: true }; }
    return { end: end, ext: false };
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
  /* v3: the declaration and the payment date (s.73, s.90a, s.51: never before 60 days; later if possession, over half the price and a
     registration power of attorney all come later, then the first of them) */
  function payDue(P, dealIso, deferIso) {
    var b = d(dealIso); if (!b) return null;
    var Y = P.pay, decl = addDays(b, Y.declare_days), pay = addDays(b, Y.pay_days), df = d(deferIso), deferred = false;
    if (df && df > pay) { pay = df; deferred = true; }
    return { declare: iso(decl), pay: iso(pay), deferred: deferred };
  }
  /* v3: a foreign buyer counts as a resident (only-home brackets) if he becomes one within 24 months (s.9(c1)(c4)(b)), war extension */
  function resBy(P, dealIso) { var b = d(dealIso); if (!b) return null; var w = warExt(P, b, addMonths(b, P.resident_months)); return { date: iso(w.end), ext: w.ext }; }
  /* v3: the oleh window: from a year before aliyah to 7 years after (instruction 1/2026 s.2c); regulation 12 for an apartment is open to
     an oleh who arrived before 15.8.2024 */
  function olehWin(P, aliyahIso, dealIso) {
    var a = d(aliyahIso); if (!a) return null; var W = P.oleh_window, from = addMonths(a, -W.before_months), to = addMonths(a, W.after_months), b = d(dealIso);
    return { from: iso(from), to: iso(to), inside: !b || (b >= from && b <= to), reg12: a < d(W.reg12_before) };
  }
  function lateFine(P, taxAmt, weeks) { return Math.max(0, taxAmt) * P.pay.late_week * Math.max(0, weeks || 0); }
  /* v3: the shared link (#ptax=...): only the fields a reader set, base64url of a small JSON (ASCII only) */
  var KEYS = ['price', 'track', 'share', 'upg', 'bdate', 'contractor', 'pdate', 'oleh12', 'disSingle', 'permit', 'giftExtra', 'aliyah', 'becomeRes', 'partner', 'pdefer', 'pdue', 'late'];
  function enc(v) { var o = {}; KEYS.forEach(function (k) { if (v[k] !== '' && v[k] != null && !(typeof v[k] === 'number' && !isFinite(v[k]))) o[k] = v[k]; }); return btoa(JSON.stringify(o)).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, ''); }
  function dec(s) {
    try { var j = JSON.parse(atob(String(s).replace(/-/g, '+').replace(/_/g, '/'))), o = {}; KEYS.forEach(function (k) { if (k in j && (typeof j[k] === 'number' || (typeof j[k] === 'string' && /^[\w\-.]{0,24}$/.test(j[k])))) o[k] = j[k]; }); return o; } catch (e) { return null; }
  }
  window.NLPT = { tax: tax, trackTax: trackTax, sellBy: sellBy, addMonths: addMonths, payDue: payDue, resBy: resBy, olehWin: olehWin, lateFine: lateFine, enc: enc, dec: dec };
  if (!window.NadLanInstruments) return;
  var NI = window.NadLanInstruments, F = NI.fmt, esc = NI.esc;
  var NAMES = { single: 'דירה יחידה', extra: 'דירה נוספת', oleh: 'עולה חדש', foreign: 'תושב חוץ', disabled: 'נכה או נפגע', land: 'קרקע או נכס מסחרי', gift: 'מתנה לקרוב משפחה' };
  var NOTE = {
    single: 'יחיד תושב ישראל שזו הדירה היחידה שלו. מי שיש לו דירה וימכור אותה בזמן נחשב כאן: 24 חודשים לרכישה מ־1.6.2025, 18 חודשים לרכישה מ־1.6.2023 עד 31.5.2025, או 12 חודשים מקבלת דירה מקבלן, המאוחר מביניהם.',
    extra: 'למי שיש כבר דירה ולא ימכור אותה בזמן, ולחברה. השיעור הזה הוא הוראת שעה, שהוארכה לרכישות עד 10.2.2027; מה יחול אחר כך עוד לא פורסם.',
    oleh: 'תקנה 12א: מרכישה שנה לפני העלייה ועד 7 שנים אחריה, בדירה יחידה. מעל 20,183,565 ₪ ההקלה לא חלה ומחשבים כדירה יחידה.',
    foreign: 'מי שאינו תושב ישראל משלם כמו דירה נוספת, גם אם זו הדירה היחידה שלו, אלא אם יהפוך לתושב תוך שנתיים. הוראת שעה, הוארכה לרכישות עד 10.2.2027.',
    disabled: 'תקנה 11: נכה, עיוור, נפגע פעולות איבה ומשפחות שכולות, פעמיים בלבד. בדירה יחידה עד 2,500,000 ₪: פטור עד המדרגה הראשונה ו־0.5% על השאר. טופס 2973.',
    land: 'קרקע ונכס שאינו דירת מגורים: 6%. קרקע שיש עליה תכנית לדירה אחת לפחות, והיתר בנייה בתוך שנתיים: 5%.',
    gift: 'מתנה לקרוב (בן זוג, הורה, צאצא ובן זוגו, נכד, אח): שליש מהמס הרגיל. מתנה לבן זוג שגר עם הנותן בדירה: פטורה. ירושה ומעבר דירה אגב גירושין אינם מכירה, ולכן אין עליהם מס רכישה.'
  };
  function today() { var t = new Date(); return t.toISOString().slice(0, 10); }
  function daysFrom(isoDate) { var a = d(isoDate), b = d(today()); return a && b ? Math.round((a - b) / 86400000) : null; }
  function count(isoDate) { var n = daysFrom(isoDate); if (n == null) return ''; if (n === 0) return 'היום'; return n > 0 ? 'בעוד ' + F.num(n) + ' ימים' : 'עבר לפני ' + F.num(-n) + ' ימים'; }
  function hashState() { var m = /#ptax=([A-Za-z0-9_\-]+)/.exec((typeof location !== 'undefined' && location.hash) || ''); return m ? dec(m[1]) : null; }
  function link(v) { return (typeof location !== 'undefined' ? location.origin + location.pathname : 'https://nad-lan.co.il/purchase-tax-calculator/') + '#ptax=' + enc(v); }
  /* the timeline drawing: HTML (it wraps on a phone), every text escaped; colours from the Instruments tokens */
  var CSS = '#nlpt-css{}.nlpt-tl{list-style:none;margin:0;padding:0;border:1px solid var(--nli-line,#D3DCE2);border-radius:6px;background:#fff;position:relative}'
    + '.nlpt-tl li{display:grid;grid-template-columns:7.2em 1fr auto;gap:4px 12px;align-items:baseline;padding:9px 12px;border-top:1px solid var(--nli-line,#D3DCE2);position:relative}'
    + '.nlpt-tl li:first-child{border-top:0}.nlpt-tl li::before{content:"";position:absolute;inset-inline-start:0;top:0;bottom:0;width:3px;background:var(--nli-sea,#2F6F86);opacity:.35}'
    + '.nlpt-tl li.is-next::before{opacity:1}.nlpt-tl li.is-late::before{background:var(--nli-survey,#C42550);opacity:1}'
    + '.nlpt-tl .d{font-family:var(--nli-mono,"IBM Plex Mono",monospace);font-variant-numeric:tabular-nums;color:var(--nli-ink,#12202A);font-weight:500;white-space:nowrap}'
    + '.nlpt-tl .t{color:var(--nli-ink2,#3E4C58)}.nlpt-tl .c{font-family:var(--nli-sans,"IBM Plex Sans Hebrew",sans-serif);font-variant-numeric:tabular-nums;font-size:.88em;color:var(--nli-mute,#5E6A75);white-space:nowrap}'
    + '.nlpt-tl li.is-late .c{color:var(--nli-survey,#C42550);font-weight:600}.nlpt-tl li.is-next .c{color:var(--nli-sea-deep,#1F4B5C);font-weight:600}'
    + '.nlpt-cap{font:500 13px/18px var(--nli-sans,"IBM Plex Sans Hebrew",sans-serif);color:var(--nli-sea,#2F6F86);margin:14px 0 6px;letter-spacing:.02em}'
    + '@media (max-width:520px){.nlpt-tl li{grid-template-columns:6.4em 1fr}.nlpt-tl .c{grid-column:2}}';
  function css() { if (typeof document === 'undefined' || document.getElementById('nlpt-css')) return; var s = document.createElement('style'); s.id = 'nlpt-css'; s.textContent = CSS; document.head.appendChild(s); }
  function timeline(items) {
    items = items.filter(function (x) { return x && x.date; }).sort(function (a, b) { return a.date < b.date ? -1 : a.date > b.date ? 1 : 0; });
    if (!items.length) return '';
    var next = null; items.forEach(function (x) { var n = daysFrom(x.date); if (next == null && n != null && n >= 0 && x.key !== 'deal') next = x.key; });
    return '<p class="nlpt-cap">ציר הזמנים של העסקה</p><ol class="nlpt-tl" aria-label="ציר הזמנים של העסקה">' + items.map(function (x) {
      var n = daysFrom(x.date), late = x.key !== 'deal' && x.due && n != null && n < 0;
      return '<li class="' + (late ? 'is-late' : x.key === next ? 'is-next' : '') + '"><bdi class="d">' + esc(F.date(x.date)) + '</bdi><span class="t">' + esc(x.label) + '</span><span class="c">' + esc(x.key === 'deal' ? 'יום העסקה' : count(x.date)) + '</span></li>';
    }).join('') + '</ol>';
  }
  NI.register('ptax', {
    kicker: 'מחשבון · מס רכישה',
    title: 'כמה מס רכישה תשלמו על הדירה',
    lede: 'מחיר הדירה ומי הקונה: המחשבון מחשב את המס לפי המדרגות של רשות המסים בכל המסלולים, כולל עולים, נכים, קרקע ומתנה, מראה כמה נופל על כל מדרגה ועד מתי כל שיעור בתוקף, מתי מדווחים ומשלמים ומה עולה כל שבוע של איחור, ולמשפרי דיור גם עד מתי למכור את הדירה הקודמת.',
    strip: function (dd) { var p = dd.ptax; return [{ label: 'פטור בדירה יחידה עד', value: F.ils(p.tracks.single[0][0]) }, { label: 'דירה יחידה: מוקפא עד', value: F.date(p.valid.single) }, { label: 'דירה נוספת ותושב חוץ: הוראת שעה עד', value: F.date(p.valid.extra) }]; },
    presets: [
      { key: 'first', label: 'דירה ראשונה', sub: '₪2,500,000', set: { price: 2500000, track: 'single', share: 100, upg: 'no' } },
      { key: 'upgrader', label: 'משפרי דיור', sub: '₪3,500,000 · מוכרים את הישנה', set: { price: 3500000, track: 'single', share: 100, upg: 'yes', contractor: 'no', bdate: today() } },
      { key: 'investor', label: 'דירה להשקעה', sub: '₪2,000,000', set: { price: 2000000, track: 'extra', share: 100, upg: 'no' } },
      { key: 'oleh', label: 'עולה חדש', sub: '₪4,000,000', set: { price: 4000000, track: 'oleh', share: 100, oleh12: 'no' } },
      { key: 'contractor', label: 'דירה מקבלן', sub: '₪3,000,000 כולל מע״מ', set: { price: 3000000, track: 'single', share: 100, upg: 'yes', contractor: 'yes', bdate: today() } },
      { key: 'half', label: 'חצי דירה', sub: '₪2,000,000 · 50%', set: { price: 2000000, track: 'single', share: 50, upg: 'no' } },
      { key: 'partners', label: 'שני קונים, מעמד שונה', sub: '₪3,000,000 · חצי וחצי', set: { price: 3000000, track: 'single', share: 50, upg: 'no', partner: 'extra' } },
      { key: 'disabled', label: 'נכה, דירה יחידה', sub: '₪2,400,000', set: { price: 2400000, track: 'disabled', share: 100, disSingle: 'yes' } },
      { key: 'gift', label: 'מתנה לבן או לבת', sub: 'דירה בשווי ₪2,800,000', set: { price: 2800000, track: 'gift', share: 100, giftExtra: 'no' } }
    ],
    defaults: function () {
      var v = { price: 3000000, track: 'single', share: 100, upg: 'no', bdate: today(), contractor: 'no', pdate: '', oleh12: 'no', disSingle: 'yes', permit: 'no', giftExtra: 'no',
        aliyah: '', becomeRes: 'no', partner: 'none', pdefer: 'no', pdue: '', late: 0 };
      var h = hashState(); if (h) Object.keys(h).forEach(function (k) { v[k] = h[k]; });  // a shared link opens the same numbers
      css(); return v;
    },
    fields: [
      { id: 'price', label: 'מחיר הדירה', type: 'money', unit: '₪', help: 'המחיר בחוזה. בדירה מקבלן, המחיר כולל מע״מ.' },
      { id: 'track', label: 'מי קונה', type: 'segmented', options: [{ value: 'single', label: 'דירה יחידה' }, { value: 'extra', label: 'דירה נוספת' }, { value: 'oleh', label: 'עולה חדש' }, { value: 'foreign', label: 'תושב חוץ' }, { value: 'disabled', label: 'נכה' }, { value: 'land', label: 'קרקע או מסחרי' }, { value: 'gift', label: 'מתנה' }] },
      { id: 'bdate', label: 'מועד העסקה (חתימת החוזה)', type: 'date', help: 'ממנו נספרים ההצהרה, התשלום ומועד מכירת הדירה הקודמת.' },
      { id: 'upg', label: 'יש לכם דירה שתמכרו?', type: 'segmented', options: [{ value: 'no', label: 'לא' }, { value: 'yes', label: 'כן, משפרי דיור' }], showIf: function (v) { return v.track === 'single'; } },
      { id: 'contractor', label: 'דירה מקבלן?', type: 'segmented', options: [{ value: 'no', label: 'לא' }, { value: 'yes', label: 'כן' }], showIf: function (v) { return v.track === 'single' && v.upg === 'yes'; } },
      { id: 'pdate', label: 'מועד קבלת הדירה מהקבלן (צפוי)', type: 'date', showIf: function (v) { return v.track === 'single' && v.upg === 'yes' && v.contractor === 'yes'; } },
      { id: 'oleh12', label: 'עליתם לפני 15.8.2024 ובוחרים בתקנה 12?', type: 'segmented', options: [{ value: 'no', label: 'לא' }, { value: 'yes', label: 'כן' }], showIf: function (v) { return v.track === 'oleh'; } },
      { id: 'aliyah', label: 'תאריך העלייה (לא חובה)', type: 'date', help: 'בודק שהרכישה בתוך החלון: משנה לפני העלייה ועד 7 שנים אחריה.', showIf: function (v) { return v.track === 'oleh'; } },
      { id: 'becomeRes', label: 'תהפכו לתושבי ישראל תוך שנתיים?', type: 'segmented', options: [{ value: 'no', label: 'לא' }, { value: 'yes', label: 'כן, וזו הדירה היחידה' }], showIf: function (v) { return v.track === 'foreign'; } },
      { id: 'disSingle', label: 'זו הדירה היחידה?', type: 'segmented', options: [{ value: 'yes', label: 'כן' }, { value: 'no', label: 'לא' }], showIf: function (v) { return v.track === 'disabled'; } },
      { id: 'permit', label: 'יש תכנית למגורים והיתר בתוך שנתיים?', type: 'segmented', options: [{ value: 'no', label: 'לא' }, { value: 'yes', label: 'כן' }], showIf: function (v) { return v.track === 'land'; } },
      { id: 'giftExtra', label: 'למקבל המתנה יש דירה אחרת?', type: 'segmented', options: [{ value: 'no', label: 'לא' }, { value: 'yes', label: 'כן' }], showIf: function (v) { return v.track === 'gift'; } },
      { id: 'share', label: 'החלק שאתם קונים', type: 'percent', unit: '%', help: 'קונים חצי דירה? 50. המס מחושב על כל הדירה, וכל קונה משלם לפי החלק שלו.' },
      { id: 'partner', label: 'מי קונה את שאר הדירה? (לא בן או בת זוג)', type: 'segmented', options: [{ value: 'none', label: 'לא רלוונטי' }, { value: 'single', label: 'דירה יחידה' }, { value: 'extra', label: 'דירה נוספת' }, { value: 'oleh', label: 'עולה חדש' }, { value: 'foreign', label: 'תושב חוץ' }], showIf: function (v) { return v.share > 0 && v.share < 100 && ['single', 'extra', 'oleh', 'foreign'].indexOf(v.track) > -1; } },
      { id: 'pdefer', label: 'החזקה ורוב התשלום נדחים מעבר ל־60 יום?', type: 'segmented', options: [{ value: 'no', label: 'לא, עסקה רגילה' }, { value: 'yes', label: 'כן, למשל מקבלן' }], showIf: function (v) { return v.track !== 'gift'; } },
      { id: 'pdue', label: 'המוקדם מבין: קבלת החזקה, תשלום של יותר ממחצית המחיר, ייפוי כוח לרישום', type: 'date', showIf: function (v) { return v.track !== 'gift' && v.pdefer === 'yes'; } },
      { id: 'late', label: 'ואם תשלמו באיחור? שבועות אחרי המועד', type: 'number', unit: 'שבועות', help: '0 = בזמן. קנס של 0.2% מהמס לכל שבוע, ועוד הפרשי הצמדה וריבית.' }
    ],
    compute: function (v, dd) {
      var P = dd.ptax;
      if (!(v.price >= 100000 && v.price <= 500000000)) return { error: { field: 'price', msg: 'הקלידו את מחיר הדירה בשקלים.' } };
      if (!(v.share > 0 && v.share <= 100)) return { error: { field: 'share', msg: 'החלק שאתם קונים: בין 1 ל־100 אחוז.' } };
      var late = +v.late; if (!isFinite(late)) late = 0;  // an empty field = paid on time
      if (!(late >= 0 && late <= 520)) return { error: { field: 'late', msg: 'מספר השבועות: בין 0 ל־520.' } };
      var k = NAMES[v.track] ? v.track : 'single', s = v.share / 100;
      var o = { oleh12: v.oleh12 === 'yes', disSingle: v.disSingle !== 'no', permit: v.permit === 'yes', giftExtra: v.giftExtra === 'yes' };
      /* v3 cases that change the brackets; with their fields at the defaults v2 runs unchanged */
      var ow = k === 'oleh' ? olehWin(P, v.aliyah, v.bdate) : null, v3n = [], full;
      if (ow && o.oleh12 && !ow.reg12) { o.oleh12 = false; v3n.push('תקנה 12 לדירת מגורים פתוחה רק למי שעלה לפני 15.8.2024. לפי תאריך העלייה שהקלדתם המס מחושב לפי תקנה 12א.'); }
      var foreignRes = k === 'foreign' && v.becomeRes === 'yes', rb = foreignRes ? resBy(P, v.bdate) : null;
      if (ow && !ow.inside) full = Object.assign(tax(v.price, P.tracks.single), { used: 'single' });
      else if (foreignRes) full = Object.assign(tax(v.price, P.tracks.single), { used: 'single' });
      else full = trackTax(v.price, k, P, o);
      var t = full.tax * s, part = v.price * s;
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
      if (k === 'oleh' && full.used === 'single' && !(ow && !ow.inside)) notes.push('המחיר מעל 20,183,565 ₪, ולכן ההקלה לעולה לא חלה והמס מחושב כדירה יחידה.');
      var tl = [{ key: 'deal', date: d(v.bdate) ? v.bdate : '', label: 'חתימה על החוזה' }];
      if (k === 'single' && v.upg === 'yes') {
        var sb = sellBy(P, v.bdate, v.contractor === 'yes', v.pdate);
        if (sb && sb.old) notes.push('<b>רכישה לפני 1.6.2023:</b> חלו כללים אחרים והארכות שונות. בדקו את המועד מול רשות המסים או עם עורך הדין.');
        else if (sb) {
          lines.unshift({ label: 'למכור את הדירה הקודמת עד', value: F.date(sb.date) });
          lines.splice(1, 0, { label: 'הזמן שנותר למכירה', value: count(sb.date) });
          notes.push('<b>עד ' + F.date(sb.date) + '</b> (' + sb.how + (sb.ext ? ', כולל הארכת המלחמה לפי הוראה 2/2026' : '') + '). מי שלא ימכור בזמן ישלם את ההפרש לדירה נוספת, כאן ' + F.ils(extra - single) + ', ועוד הצמדה וריבית.');
          tl.push({ key: 'sell', date: sb.date, label: 'מכירת הדירה הקודמת, המועד האחרון', due: true });
        }
      }
      if ((k === 'extra' || k === 'foreign') && v.bdate && d(v.bdate) && d(v.bdate) > d(P.valid.extra)) notes.push('<b>עסקה אחרי 10.2.2027:</b> הוראת השעה של 8% ו־10% מסתיימת, ומה יחול אחריה עוד לא פורסם.');
      /* v3 lines: the next bracket, the oleh window, the resident date, the second buyer, the payment and the late cost */
      var br = { single: P.tracks.single, extra: P.tracks.extra, foreign: P.tracks.extra, oleh: full.used === 'oleh12' ? P.oleh12 : full.used === 'oleh' ? P.tracks.oleh : P.tracks.single, gift: o.giftExtra ? P.tracks.extra : P.tracks.single }[foreignRes || (ow && !ow.inside) ? 'single' : k];
      if (br) {
        var nx = null; for (var i = 0; i < br.length; i++) { if (br[i][0] != null && v.price < br[i][0]) { nx = { at: br[i][0], rate: br[i + 1] ? br[i + 1][1] : null }; break; } }
        if (nx && nx.rate != null) lines.push({ label: 'המרחק עד המדרגה הבאה (' + F.num(100 * nx.rate, nx.rate * 100 % 1 ? 1 : 0) + '%)', value: F.ils(nx.at - v.price) });
        var more = (k === 'gift' ? P.gift : 1) * (tax(v.price + 100000, br).tax - tax(v.price, br).tax) * s;
        lines.push({ label: 'עוד ₪100,000 במחיר מוסיפים למס', value: F.ils(more) });
      }
      if (ow) {
        lines.push({ label: 'חלון ההטבה לעולה', value: F.date(ow.from) + ' עד ' + F.date(ow.to) });
        if (!ow.inside) v3n.push('<b>מחוץ לחלון:</b> ההקלה לעולה חלה על רכישה משנה לפני העלייה ועד 7 שנים אחריה (' + F.date(ow.from) + ' עד ' + F.date(ow.to) + '). העסקה שהקלדתם מחוץ לחלון, ולכן המס מחושב כדירה יחידה.');
        else if (ow.reg12 && v.price <= P.oleh_cap) {
          var t12 = tax(v.price, P.oleh12).tax * s, t12a = tax(v.price, P.tracks.oleh).tax * s;
          lines.push({ label: o.oleh12 ? 'לפי תקנה 12א הייתם משלמים' : 'לפי תקנה 12 הייתם משלמים', value: F.ils(o.oleh12 ? t12a : t12) });
          v3n.push('<b>עליתם לפני 15.8.2024:</b> אפשר לבחור בין תקנה 12א (' + F.ils(t12a) + ') לתקנה 12 (' + F.ils(t12) + '). במחיר הזה ' + (t12 < t12a ? 'תקנה 12 זולה יותר' : t12 > t12a ? 'תקנה 12א זולה יותר' : 'שתיהן שוות') + '. תקנה 12 חלה גם על דירה שאינה יחידה.');
          tl.push({ key: 'oleh', date: ow.to, label: 'סוף חלון ההטבה לעולה (7 שנים מהעלייה)' });
        } else tl.push({ key: 'oleh', date: ow.to, label: 'סוף חלון ההטבה לעולה (7 שנים מהעלייה)' });
      }
      if (rb) {
        lines.push({ label: 'להפוך לתושבי ישראל עד', value: F.date(rb.date) });
        v3n.push('<b>תושב חוץ שיהפוך לתושב ישראל תוך שנתיים</b> נחשב תושב, ואם זו דירתו היחידה הוא משלם לפי מדרגות דירה יחידה' + (rb.ext ? ' (המועד כולל את הארכת המלחמה, הוראה 2/2026)' : '') + '. מי שלא יהפוך לתושב עד ' + F.date(rb.date) + ' ישלים את המס לדירה נוספת: כאן ' + F.ils(extra - t) + ' ועוד הפרשי הצמדה וריבית.');
        tl.push({ key: 'res', date: rb.date, label: 'להפוך לתושבי ישראל, המועד האחרון', due: true });
      }
      var pk = s < 1 && v.partner && v.partner !== 'none' && ['single', 'extra', 'oleh', 'foreign'].indexOf(k) > -1 ? v.partner : null, tp = 0;
      if (pk) {
        tp = trackTax(v.price, pk, P, {}).tax * (1 - s);
        lines.push({ label: 'הקונה השני (' + NAMES[pk] + ', ' + F.num(100 - v.share) + '%) משלם', value: F.ils(tp) });
        lines.push({ label: 'המס של שני הקונים יחד', value: F.ils(t + tp) });
        v3n.push('<b>שני קונים שאינם תא משפחתי אחד:</b> כל אחד מחשב את המס על שווי הדירה כולה לפי המעמד שלו, ומשלם לפי החלק שלו. בני זוג וילדים עד גיל 18 נחשבים קונה אחד.');
      }
      var pd = k !== 'gift' ? payDue(P, v.bdate, v.pdefer === 'yes' ? v.pdue : '') : (d(v.bdate) ? payDue(P, v.bdate, '') : null), Y = P.pay;
      if (pd) {
        lines.push({ label: 'הצהרה לרשות המסים עד', value: F.date(pd.declare) });
        tl.push({ key: 'decl', date: pd.declare, label: 'הצהרה לרשות המסים (טופס 7000, דרך עורך הדין)', due: true });
        if (t > 0) {
          lines.push({ label: 'תשלום המס עד', value: F.date(pd.pay) + (pd.deferred ? ' (נדחה)' : '') });
          lines.push({ label: 'כל שבוע של איחור בתשלום', value: F.ils(lateFine(P, t, 1)) });
          tl.push({ key: 'pay', date: pd.pay, label: pd.deferred ? 'תשלום המס: המועד שנדחה לפי סעיף 51' : 'תשלום המס, 60 יום מהעסקה', due: true });
          if (late > 0) {
            var lf = lateFine(P, t, late);
            lines.push({ label: 'קנס על ' + F.num(late) + ' שבועות איחור', value: F.ils(lf) });
            tl.push({ key: 'late', date: iso(addDays(d(pd.pay), 7 * late)), label: 'התשלום באיחור שבדקתם: קנס ' + F.ils(lf) + ' ועוד הצמדה וריבית' });
          }
          v3n.push('<b>מתי משלמים:</b> הצהרה תוך ' + Y.declare_days + ' יום מהעסקה, והמס תוך ' + Y.pay_days + ' יום. אם עד אז לא קיבלתם חזקה, לא שילמתם יותר ממחצית המחיר ולא קיבלתם ייפוי כוח לרישום, התשלום נדחה למוקדם מביניהם, ועל תקופת הדחייה נוספים הפרשי הצמדה וריבית. איחור בתשלום: קנס של 0.2% מהמס לכל שבוע ועוד הצמדה וריבית. איחור בהצהרה: ' + F.ils(Y.decl_fine) + ' לכל שבועיים (2026); שני הקנסות לא חלים על אותה תקופה.');
        } else v3n.push('<b>גם בלי מס מגישים הצהרה</b> תוך ' + Y.declare_days + ' יום מהעסקה. איחור: ' + F.ils(Y.decl_fine) + ' לכל שבועיים (2026).');
      }
      notes = notes.concat(v3n);
      var SC = ['single', 'extra', 'oleh', 'foreign', 'disabled'];
      var all = lines.map(function (l) { return l.label + ': ' + l.value; }).join('\n');
      return {
        answer: { label: 'מס הרכישה, ' + NAMES[k] + (s < 1 ? ', ' + F.num(v.share) + '% מהדירה' : ''), value: F.ils(t), tone: t > 0 ? 'survey' : 'ink',
          sub: t > 0 ? F.num(100 * t / part, 2) + '% מהמחיר' + (s < 1 ? ' של החלק שלכם' : '') : 'במחיר הזה אין מס רכישה' },
        breakdown: [{ label: 'מחיר', value: part, kind: 'sea' }, { label: 'מס רכישה', value: t, kind: 'survey' }],
        lines: lines,
        figure: timeline(tl),
        note: notes.join('<br>'),
        scenarioLabel: 'אותו מחיר, בכל מסלול',
        scenarios: SC.map(function (x) { return { key: x, name: NAMES[x], value: F.ils(trackTax(v.price, x, P, o).tax * s), on: x === k }; }),
        table: { title: 'המס מדרגה אחרי מדרגה, ' + NAMES[k], head: ['מדרגה', 'שיעור', 'הסכום במדרגה', 'המס'], num: [2, 3],
          rows: full.rows.map(function (r) { return [(r.from ? F.ils(r.from) : '₪0') + ' עד ' + (r.to === Infinity ? 'מעל' : F.ils(r.to)), F.num(100 * r.rate, 1) + '%' + (k === 'gift' ? ' × שליש' : ''), F.ils(r.part * s), F.ils(r.tax * s)]; }) },
        formula: 'מס רכישה = סכום על כל המדרגות של (החלק מהמחיר שנופל במדרגה × שיעור המדרגה), כפול החלק שאתם קונים. המדרגות חלות על שווי הדירה כולה.',
        sources: [{ label: P.instruction.label, url: P.instruction.url }, { label: P.guide.label, url: P.guide.url }, { label: P.source + ', נבדק ' + F.date(P.checked), url: P.url }].concat(k === 'single' && v.upg === 'yes' || rb ? [{ label: P.war.label, url: P.war.url }] : []).concat((k === 'extra' || k === 'foreign') && P.extension ? [{ label: P.extension.label, url: P.extension.url }] : []),
        bare: true,
        text: 'מס רכישה, ' + NAMES[k] + ': דירה ב־' + F.ils(v.price) + (s < 1 ? ', ' + F.num(v.share) + '% מהדירה' : '') + ' = ' + F.ils(t) + ' (' + F.num(part ? 100 * t / part : 0, 2) + '%).\n' + all + '\nלפתיחת אותם מספרים: ' + link(v)
      };
    }
  });
})();
