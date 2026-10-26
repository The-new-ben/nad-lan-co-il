/* NadLan Instruments · pinui v1 (G2 moat, 26.10.2026): "הבניין שלכם בפינוי בינוי" on /urban-renewal/pinui-binui/.
   Three views on one set of answers:
   - maj  · הרוב והחתימות: the special majority of section 1 of the Pinui Binui law, building by building (two thirds of the
            apartments in the cluster and three fifths in every building; 4 or 5 apartments: 3), what is missing, the more-than-two-fifths
            that lets owners ask the authority for its free appraiser (s.2א), the 40% line of s.1ג, and the complex at the authority today.
   - mine · מה מגיע לי: the tax-free ceiling of the new apartment for the reader's own size (the authority's 2025 report, annex A),
            the units multiplier of the complex or the city, what the law fixes and what is negotiated, the options for 70+ and 75+.
   - time · השעון של החוק: the dates of section 1ד from the first signed deal (half in 2 years, three fifths in 4, a plan in 4.5,
            one more year in a complex of 120 units or more), the years since the plan was approved, and the authority's 4.0-year
            average from approval to a first permit, shown as an average of complexes that got one, never as a forecast.
   Data: data/pinui.json (tools/urban/build_g2g3_data.py) + data/renewal-track.json (the tracker's file). Pure logic in NLPB for
   checks. Honesty: no promised area, price or date; the law's numbers with their section; the averages labelled as averages. */
(function () {
  'use strict';
  var STG = ['ללא שלב', 'תכנון ראשוני', 'תכנון סטטוטורי', 'תכנית מאושרת', 'במימוש', 'אחרי רישוי'];
  var OTHER = '*';
  var E = 1e-9;

  function atLeast(n, a, b) { return Math.ceil(n * a / b - E); }          // at least a/b of n
  function moreThan(n, a, b) { return Math.floor(n * a / b + E) + 1; }    // more than a/b of n
  function n0(x) { return String(Math.round(x || 0)).replace(/\B(?=(\d{3})+(?!\d))/g, ','); }
  function dd(iso) { var p = String(iso || '').split('-'); return p.length === 3 ? (+p[2]) + '.' + (+p[1]) + '.' + p[0] : p.length === 2 ? (+p[1]) + '.' + p[0] : String(iso || ''); }
  function addMonths(ym, m) { var p = String(ym).split('-'), y = +p[0], mo = +p[1] - 1 + m; return (y + Math.floor(mo / 12)) + '-' + ('0' + (((mo % 12) + 12) % 12 + 1)).slice(-2); }
  function ymOf(iso) { return String(iso || '').slice(0, 7); }
  function months(a, b) { var p = a.split('-'), q = b.split('-'); return (+q[0] - +p[0]) * 12 + (+q[1] - +p[1]); }  // b - a in months
  function lastMap(T) { for (var i = T.snaps.length - 1; i >= 0; i--) if (T.snaps[i].k === 'map') return i; return -1; }

  /** The special majority of s.1, per building and for the cluster. rows: [{u: apartments, s: signed}] */
  function majority(rows, L) {
    var out = { b: [], N: 0, S: 0, ok: true, missing: 0, small: [], tiny: [] };
    rows.forEach(function (r, i) {
      var u = Math.max(0, Math.round(r.u || 0)), s = Math.max(0, Math.min(u, Math.round(r.s || 0)));
      if (!u) return;
      var need = atLeast(u, L.building_share[0], L.building_share[1]);
      if (u >= L.small_building.apts[0] && u <= L.small_building.apts[1]) { need = L.small_building.min_yes; out.small.push(i + 1); }
      if (u < L.building_min_apts) out.tiny.push(i + 1);
      var ap = moreThan(u, L.appraiser_share[0], L.appraiser_share[1]);
      var b = { i: i + 1, u: u, s: s, need: need, miss: Math.max(0, need - s), ap: ap, apOk: s >= ap, half: atLeast(u, 1, 2), tf: atLeast(u, 3, 5) };
      out.b.push(b); out.N += u; out.S += s;
    });
    out.cneed = atLeast(out.N, L.complex_share[0], L.complex_share[1]);
    out.cmiss = Math.max(0, out.cneed - out.S);
    var bmiss = out.b.reduce(function (t, b) { return t + b.miss; }, 0);
    // the fewest extra signatures that satisfy both tests: a signature that closes a building gap also counts for the cluster
    out.missing = Math.max(bmiss, out.cneed - out.S, 0);
    out.ok = out.missing === 0 && out.b.length > 0;
    out.apAll = out.b.length > 0 && out.b.every(function (b) { return b.apOk; });
    out.pct = out.N ? out.S / out.N : 0;
    return out;
  }

  /** The tax-free ceiling of the new apartment (pinui binui, R25 annex A): the highest of 120 m², 150% of the value (not computed here)
      and the old area grown by 50% up to 200 m². */
  function taxCap(area, T) {
    var grow = Math.min(area * (1 + T.cap_grow_pct / 100), T.cap_grow_max_sqm);
    return { cap: Math.max(T.cap_sqm, grow), grow: grow, floor: T.cap_sqm, by: grow > T.cap_sqm ? 'grow' : 'floor' };
  }

  /** Section 1ד dates from the month of the first signed deal. */
  function clock(first, L, bigComplex) {
    var c = L.clock, x = bigComplex ? c.big_complex_extra_months : 0;
    return { half: addMonths(first, c.half_months + x), tf: addMonths(first, c.three_fifths_months + x), plan: addMonths(first, c.plan_months + x), extra: x };
  }

  /** The city's complexes on the authority's latest map: count and the units multiplier (after ÷ today), our calculation. */
  function cityStats(T, c) {
    var lm = lastMap(T), n = 0, e = 0, p = 0;
    T.recs.forEach(function (r) { if (r.s[lm] === -1) return; if (c && r.c !== c) return; n++; if (r.e && r.p) { e += r.e; p += r.p; } });
    return { n: n, mult: e ? p / e : 0 };
  }

  function cities(T) { var o = {}; T.recs.forEach(function (r) { o[r.c] = (o[r.c] || 0) + 1; }); return Object.keys(o).sort(function (a, b) { return a.localeCompare(b, 'he'); }).map(function (c) { return { c: c, n: o[c] }; }); }
  function inCity(T, c) { var lm = lastMap(T); return T.recs.filter(function (r) { return r.c === c && r.s[lm] !== -1; }).sort(function (a, b) { return a.n.localeCompare(b.n, 'he'); }); }
  function byKey(T, k) { for (var i = 0; i < T.recs.length; i++) if (T.recs[i].k === k) return T.recs[i]; return null; }

  window.NLPB = { majority: majority, taxCap: taxCap, clock: clock, cityStats: cityStats, atLeast: atLeast, moreThan: moreThan, addMonths: addMonths, months: months, dd: dd };
  if (!window.NadLanInstruments) return;
  var NI = window.NadLanInstruments, F = NI.fmt, esc = NI.esc;

  // ------------------------------------------------------------------ drawings (RTL: text-anchor start = the right end of the label)
  function svgMajority(m, L) {
    // 16 px in a 420 viewBox stays readable in the engine's narrow desktop column and on a phone
    var rows = m.b.length + 1, H = 44 + rows * 66, XR = 300, W = 200, g = [];
    g.push('<text x="410" y="24" class="t" text-anchor="start" style="font-size:18px">' + esc('חתימות מול הרוב שבחוק') + '</text>');
    function bar(y, label, s, u, need, ok, extra) {
      var w = u ? Math.round(W * s / u) : 0, xn = XR - Math.round(W * need / Math.max(1, u));
      g.push('<text x="410" y="' + (y + 6) + '" text-anchor="start" style="font-size:16px;fill:#12202A;font-weight:600">' + esc(label) + '</text>');
      g.push('<rect x="' + (XR - W) + '" y="' + (y - 10) + '" width="' + W + '" height="20" fill="#EDF1F4"/>');
      if (w) g.push('<rect x="' + (XR - w) + '" y="' + (y - 10) + '" width="' + w + '" height="20" fill="' + (ok ? '#1F4B5C' : '#2F6F86') + '"/>');
      g.push('<line x1="' + xn + '" y1="' + (y - 16) + '" x2="' + xn + '" y2="' + (y + 16) + '" stroke="' + (ok ? '#12202A' : '#C42550') + '" stroke-width="2.5"/>');
      g.push('<text x="' + (XR - W - 8) + '" y="' + (y + 6) + '" text-anchor="start" class="m" style="font-size:16px">' + esc(n0(s) + '/' + n0(u)) + '</text>');
      g.push('<text x="410" y="' + (y + 30) + '" text-anchor="start"' + (ok ? '' : ' class="r"') + ' style="font-size:15px' + (ok ? ';fill:#3E4C58' : '') + '">' + esc('צריך ' + n0(need) + (ok ? ' ✓' : ', חסרות ' + n0(extra))) + '</text>');
    }
    var y = 64;
    m.b.forEach(function (b) { bar(y, 'בניין ' + b.i, b.s, b.u, b.need, b.miss === 0, b.miss); y += 66; });
    bar(y, 'המקבץ', m.S, m.N, m.cneed, m.cmiss === 0, m.cmiss);
    var aria = 'רוב מיוחס: ' + m.b.map(function (b) { return 'בניין ' + b.i + ' ' + b.s + ' מתוך ' + b.u + ', צריך ' + b.need; }).join('; ') + '; מקבץ ' + m.S + ' מתוך ' + m.N + ', צריך ' + m.cneed + '. הקו האנכי: שלוש חמישיות בבניין, שני שלישים במקבץ';
    return '<svg class="nli__wall" direction="rtl" viewBox="0 0 420 ' + H + '" role="img" aria-label="' + esc(aria) + '">' + g.join('') + '</svg>';
  }

  function svgArea(area, cap, old) {
    var mx = Math.max(cap.cap, area + old, 130), XR = 404, W = 300, g = [], y = 62;
    var rows = [['הדירה היום', area, '#8A97A2'], ['ועוד ' + old + ' מ״ר, כמו בתקן עד 2022', area + old, '#2F6F86'], ['תקרת הפטור ממס', cap.cap, '#1F4B5C']];
    g.push('<text x="410" y="24" class="t" text-anchor="start" style="font-size:18px">' + esc('השטח שלכם מול התקרה שבחוק') + '</text>');
    rows.forEach(function (r) {
      var w = Math.round(W * r[1] / mx);
      g.push('<text x="410" y="' + (y - 10) + '" text-anchor="start" style="font-size:16px;fill:#12202A">' + esc(r[0]) + '</text>');
      g.push('<rect x="' + (XR - w) + '" y="' + (y - 2) + '" width="' + w + '" height="20" fill="' + r[2] + '"/>');
      g.push('<text x="' + (XR - w - 8) + '" y="' + (y + 14) + '" text-anchor="start" class="m" style="font-size:16px">' + esc(n0(r[1])) + '</text>');
      y += 58;
    });
    return '<svg class="nli__wall" direction="rtl" viewBox="0 0 420 ' + (y - 10) + '" role="img" aria-label="' + esc('הדירה היום ' + area + ' מ״ר; עם ' + old + ' מ״ר נוספים ' + (area + old) + ' מ״ר; תקרת הפטור ' + Math.round(cap.cap) + ' מ״ר') + '">' + g.join('') + '</svg>';
  }

  function svgClock(first, ck, now, ap, avgY) {
    var pts = [[0, 'עסקה ראשונה', dd(first), 'k', 1], [months(first, ck.half), 'חצי', dd(ck.half), 'law', 1], [months(first, ck.tf), '3/5', dd(ck.tf), 'law', 1], [months(first, ck.plan), 'תכנית', dd(ck.plan), 'law', 0]];
    var span = Math.max(pts[3][0] + 6, months(first, now) + 3), XR = 380, XL = 30, g = [], y0 = 100;
    var x = function (m) { return XR - (XR - XL) * Math.max(0, Math.min(1, m / span)); };
    g.push('<text x="410" y="24" class="t" text-anchor="start" style="font-size:18px">' + esc('השעון של סעיף 1ד') + '</text>');
    g.push('<line x1="' + XL + '" y1="' + y0 + '" x2="' + XR + '" y2="' + y0 + '" stroke="#12202A" stroke-width="2"/>');
    var nm = months(first, now);
    if (nm >= 0 && nm <= span) { g.push('<line x1="' + x(nm) + '" y1="' + (y0 - 12) + '" x2="' + x(nm) + '" y2="' + (y0 + 12) + '" stroke="#C42550" stroke-width="3"/>'); g.push('<text x="' + x(nm) + '" y="' + (y0 + 76) + '" text-anchor="middle" class="r" style="font-size:15px">' + esc('היום') + '</text>'); }
    pts.forEach(function (p) {
      var X = x(p[0]), up = p[4];
      g.push('<circle cx="' + X + '" cy="' + y0 + '" r="7" fill="' + (p[3] === 'law' ? '#1F4B5C' : '#fff') + '" stroke="#1F4B5C" stroke-width="2"/>');
      g.push('<text x="' + X + '" y="' + (up ? y0 - 34 : y0 + 30) + '" text-anchor="middle" style="font-size:16px;fill:#12202A;font-weight:600">' + esc(p[1]) + '</text>');
      g.push('<text x="' + X + '" y="' + (up ? y0 - 14 : y0 + 50) + '" text-anchor="middle" class="m" style="font-size:15px">' + esc(p[2]) + '</text>');
    });
    var H = y0 + 104;
    g.push('<text x="410" y="' + H + '" text-anchor="start" style="font-size:15px;fill:#3E4C58">' + esc('אחר כך: ' + F.num(avgY, 1) + ' שנים בממוצע מאישור עד היתר') + '</text>');
    return '<svg class="nli__wall" direction="rtl" viewBox="0 0 420 ' + (H + 14) + '" role="img" aria-label="' + esc('עסקה ראשונה ' + dd(first) + '; חצי מבעלי הדירות עד ' + dd(ck.half) + '; שלוש חמישיות עד ' + dd(ck.tf) + '; הגשת תכנית עד ' + dd(ck.plan) + (ap ? '; התכנית אושרה ב-' + dd(ap) : '') + '; אחר כך ' + F.num(avgY, 1) + ' שנים בממוצע מאישור עד היתר, ממוצע ולא תחזית') + '">' + g.join('') + '</svg>';
  }

  // ------------------------------------------------------------------ views
  function srcs(D, keys) { return keys.map(function (k) { var s = D.sources[k]; return { label: s.label, url: s.url }; }); }

  function complexLines(T, v, lines, notes, P) {
    var r = v.cx && v.cx !== OTHER ? byKey(T, v.cx) : null, lm = lastMap(T);
    if (!r) return null;
    var md = T.snaps[lm].d, st = r.s[lm];
    lines.push({ label: 'השלב אצל הרשות, ' + dd(md), value: st === -1 ? 'לא במפה' : STG[Math.max(0, st)] });
    if (r.t) lines.push({ label: 'מסלול ההכרזה', value: T.tracks[r.t] });
    if (r.e && r.p) lines.push({ label: 'דירות במתחם היום ← אחרי הבנייה', value: F.num(r.e) + ' → ' + F.num(r.p) });
    if (r.ap) lines.push({ label: 'אישור התכנית לפי הרשות', value: dd(r.ap) });
    if (r.pl) lines.push({ label: 'מספר תכנית', value: r.pl });
    return r;
  }

  function viewMaj(v, D, T) {
    var L = D.law, m = majority(v.rows || [], L), lines = [], notes = [];
    if (!m.b.length) return { error: { field: 'rows', msg: 'הוסיפו לפחות בניין אחד עם מספר הדירות.' } };
    var short = m.b.filter(function (b) { return b.miss; });
    var answer = m.ok
      ? { label: 'הרוב המיוחס בדירות (סעיף 1 לחוק)', value: 'מתקיים', sub: esc('במקבץ ' + n0(m.S) + ' מתוך ' + n0(m.N) + ' דירות (' + F.pct(m.pct, 1) + '), צריך ' + n0(m.cneed) + '. בכל בניין יש שלוש חמישיות לפחות. נשאר לבדוק את הרכוש המשותף: יותר ממחציתו בכל בניין.') }
      : { label: 'הרוב המיוחס בדירות (סעיף 1 לחוק)', value: 'חסרות ' + n0(m.missing), tone: 'survey', sub: esc((m.cmiss ? 'במקבץ ' + n0(m.S) + ' מתוך ' + n0(m.N) + ', צריך ' + n0(m.cneed) + '. ' : 'במקבץ יש שני שלישים (' + n0(m.S) + ' מתוך ' + n0(m.N) + '). ') + (short.length ? short.map(function (b) { return 'בבניין ' + b.i + ' ' + n0(b.s) + ' מתוך ' + n0(b.u) + ', צריך ' + n0(b.need); }).join('. ') + '.' : '')) };
    lines.push({ label: 'דירות במקבץ', value: F.num(m.N) });
    lines.push({ label: 'חתמו (' + F.pct(m.pct, 1) + ')', value: F.num(m.S) });
    lines.push({ label: 'צריך במקבץ: שני שלישים', value: F.num(m.cneed) });
    m.b.forEach(function (b) { lines.push({ label: 'בניין ' + b.i + ' (' + b.u + ' דירות), צריך ' + (L.small_building.apts.indexOf(b.u) > -1 ? '3 דירות' : 'שלוש חמישיות'), value: 'חתמו ' + F.num(b.s) + ', צריך ' + F.num(b.need) }); });
    lines.push({ label: 'שמאי מטעם הרשות, בחינם: יותר משתי חמישיות בכל בניין', value: m.apAll ? 'אפשר לבקש' : 'עדיין לא' });
    lines.push({ label: 'נחתם בלי כינוס או בלי מסמך עיקרי הצעה: רוב יכול לבטל כל עוד חתמו פחות מ-40%', value: m.b.every(function (b) { return b.s < b.u * L.convention_cancel_below; }) ? 'עדיין פתוח' : 'עבר 40%' });
    var r = complexLines(T, v, lines, notes);
    if (m.tiny.length) notes.push(esc('בניין ' + m.tiny.join(', ') + ': פחות מ-4 דירות. החוק מגדיר בית משותף מ-4 דירות, ולכן בניין כזה נספר רק כחלק ממקבץ עם בניינים אחרים; כדאי לבדוק עם עורך הדין.'));
    if (m.small.length) notes.push(esc('בבניין של 4 או 5 דירות החוק דורש 3 דירות לפחות, וגם יותר משני בעלי דירות.'));
    notes.push(esc('החוק סופר דירות שבבעלות המסכימים, לא אנשים. בבניין של 6 דירות ומעלה, בעלים של יותר מ-30% מהדירות נספר כ-30% ועוד שליש מההפרש (סעיף 4). את הרכוש המשותף, יותר ממחציתו בכל בניין, המחשבון לא בודק.'));
    if (r && r.e) notes.push(esc('במתחם ' + r.n + ' יש לפי הרשות ' + n0(r.e) + ' דירות היום. הרוב נספר במקבץ: הבניינים שצריך לפנות כדי להקים בניין חדש לפי התכנית, ולכן רשמו כאן את הבניינים של המקבץ שלכם.'));
    var table = { title: 'בניין אחר בניין: הרוב, השמאי והשעון של סעיף 1ד', head: ['בניין', 'דירות', 'חתמו', 'צריך לרוב', 'חסרות', 'לשמאי של הרשות', 'חצי (שנתיים)', 'שלוש חמישיות (4 שנים)'], num: [1, 2, 3, 4, 5, 6, 7], phoneHide: [5, 6, 7],
      rows: m.b.map(function (b) { return ['בניין ' + b.i, F.num(b.u), F.num(b.s), F.num(b.need), b.miss ? F.num(b.miss) : '0', F.num(b.ap), F.num(b.half), F.num(b.tf)]; }).concat([['כל המקבץ', F.num(m.N), F.num(m.S), F.num(m.cneed), m.cmiss ? F.num(m.cmiss) : '0', '', '', '']]) };
    var txt = 'פינוי בינוי, הרוב המיוחס לפי סעיף 1 לחוק: במקבץ ' + m.S + ' מתוך ' + m.N + ' דירות, צריך ' + m.cneed + '. ' + m.b.map(function (b) { return 'בניין ' + b.i + ': ' + b.s + ' מתוך ' + b.u + ', צריך ' + b.need; }).join('; ') + '. ' + (m.ok ? 'הרוב בדירות מתקיים.' : 'חסרות ' + m.missing + ' חתימות.');
    return { answer: answer, figure: svgMajority(m, L), lines: lines, note: notes.join('<br>'), table: table,
      formula: 'רוב מיוחס (סעיף 1 לחוק פינוי ובינוי): בעלי שני שלישים לפחות מהדירות במקבץ, שלוש חמישיות לפחות מהדירות בכל בית משותף שבמקבץ (בבית של 4 או 5 דירות: 3 דירות ויותר משני בעלי דירות), ויותר ממחצית הרכוש המשותף בכל בית. שמאי פינוי ובינוי מטעם הרשות: יותר משתי חמישיות מהדירות ומהרכוש המשותף בכל בית (סעיפים 1 ו-2א). המספרים מעוגלים כלפי מעלה לדירה שלמה.',
      sources: srcs(D, ['LAW', 'FAQ', 'SHM', 'MAP']), text: txt };
  }

  function viewMine(v, D, T) {
    var X = D.tax, area = +v.area;
    if (!(area >= 20 && area <= 400)) return { error: { field: 'area', msg: 'שטח הדירה בין 20 ל-400 מ״ר.' } };
    var cap = taxCap(area, X), lines = [], notes = [], old = D.s21.old_sqm;
    var r = v.cx && v.cx !== OTHER ? byKey(T, v.cx) : null;
    var ns = cityStats(T, ''), cs = v.city && v.city !== OTHER ? cityStats(T, v.city) : null;
    var mult = r && r.e && r.p ? { v: r.p / r.e, of: 'במתחם ' + r.n } : cs && cs.mult ? { v: cs.mult, of: 'בממוצע ב' + v.city } : { v: ns.mult, of: 'בממוצע בכל המתחמים' };
    var answer = { label: 'תקרת השטח לפטור ממס בדירת התמורה', value: 'עד ' + n0(cap.cap) + ' מ״ר', sub: esc('לדירה של ' + n0(area) + ' מ״ר: ' + (cap.by === 'grow' ? 'הדירה ועוד 50%' + (cap.grow >= X.cap_grow_max_sqm ? ', עד 200 מ״ר' : '') : 'הרף של 120 מ״ר גבוה מהדירה ועוד 50%') + '. או דירה בשווי 150% מהדירה הקיימת בניכוי שווי הזכויות שעוברות ליזם, הגבוה מביניהם. ' + X.rent_note + ' (דוח הרשות 2025, נספח א).') };
    lines.push({ label: 'מכפיל הדירות ' + mult.of + ' (חישוב שלנו)', value: '× ' + F.num(mult.v, 2) });
    if (mult.of !== 'בממוצע בכל המתחמים') lines.push({ label: 'מכפיל הדירות בכל המתחמים במפת הרשות', value: '× ' + F.num(ns.mult, 2) });
    lines.push({ label: 'מס שבח על הדירה הישנה', value: 'פטור' });
    lines.push({ label: 'מס רכישה על דירת התמורה', value: 'פטור' });
    lines.push({ label: 'מע״מ על שירותי הבנייה', value: '0%' });
    lines.push({ label: 'מספר הדירות של אותו בעלים במתחם', value: 'ללא הגבלה' });
    lines.push({ label: 'היטל השבחה במתחם מוכרז (ככלל)', value: '25%' });
    lines.push({ label: 'שמאי פינוי ובינוי מטעם הרשות', value: 'בחינם' });
    lines.push({ label: 'התקן הקודם ציין כמקובלת תוספת של', value: old + ' מ״ר' });
    lines.push({ label: 'פינוי בממוצע בהנחות המחשבון הממשלתי', value: D.model.evac_months + ' חודשים' });
    var age = v.age, L = D.law;
    if (age === '70' || age === '75') {
      var opts = age === '75' ? L.elderly_options.slice(0, L.elderly_out) : L.elderly_options;
      notes.push(esc((age === '75' ? 'מגיל 75 במועד העסקה הראשונה, וגם חולה הנוטה למות או זכאי לגמלת סיעוד ברמה 5 או 6: אם לא הוצעה לכם אחת משלוש החלופות מחוץ לפרויקט, הסירוב שלכם לא ייחשב בלתי סביר. ' : 'מגיל 70 במועד העסקה הראשונה, אם גרתם בדירה שנתיים לפחות: היזם צריך להציע לכם לפחות אחת מהחלופות שבחוק, לצד דירת התמורה, אחרת הסירוב שלכם לא ייחשב בלתי סביר. ') + 'החלופות: ' + opts.join('; ') + '.'));
      notes.push(esc('קשיש שמקבל הבטחת הכנסה, שזו דירתו היחידה: היזם מממן 5 שנים את ההפרש בוועד הבית (שאלות ותשובות של הרשות).'));
    }
    notes.push(esc('אין תעריף חוקי לתמורה. החוק קובע מה חייב להיות בעסקה: עקרונות התמורה, מועדים מרביים לתכנית, להיתר ולמסירה, מי בונה, וערבויות של היזם לטובתכם. הגודל, המרפסת, החניה והמחסן נקבעים במשא ומתן, לפי תקן 21 והשמאות.'));
    notes.push(esc('הנחה בארנונה על השטח שנוסף לדירה החדשה ניתנת לזמן מוגבל ובאופן מדורג (שאלות ותשובות של הרשות).'));
    var table = { title: 'מה קובע החוק, ומה נקבע אצלכם בהסכם', head: ['נושא', 'מה קבוע', 'מקור'],
      rows: [['רוב מיוחס', 'שני שלישים במקבץ, שלוש חמישיות בכל בניין, יותר ממחצית הרכוש המשותף', 'סעיף 1 לחוק'],
             ['מה חייב להיות בעסקה', 'עקרונות התמורה, מועדים מרביים, הבונה, ערבויות', 'סעיף 1 לחוק'],
             ['מגורים בתקופת הבנייה', 'בלי מגורים חלופיים הסירוב סביר', 'סעיף 2(ב)(2)'],
             ['ערבויות', 'בלי בטוחות הולמות הסירוב סביר', 'סעיף 2(ב)(3)'],
             ['גודל הדירה החדשה', 'נקבע בהסכם ובשמאות; התקרה לפטור ממס: ' + n0(cap.cap) + ' מ״ר לדירה שלכם', 'נספח א לדוח הרשות'],
             ['קשישים', 'חלופות מגיל 70, וחלופה מחוץ לפרויקט מגיל 75', 'סעיף 2(ב)(6), (7)'],
             ['מסים', 'פטור ממס שבח וממס רכישה, מע״מ אפס, בלי הגבלה על מספר הדירות', 'נספח א לדוח הרשות'],
             ['היטל השבחה', '25%, או לפי החלטת העירייה 50% או פטור, לתכניות שייקלטו עד מאי 2027', 'נספח א לדוח הרשות'],
             ['מי משלם לאנשי המקצוע', 'היזם, במבנה עסקה מקובל', 'שאלות ותשובות של הרשות']] };
    var txt = 'פינוי בינוי, דירה של ' + area + ' מ״ר: תקרת הפטור ממס לדירת התמורה ' + Math.round(cap.cap) + ' מ״ר (או 150% מהשווי). מכפיל הדירות ' + mult.of + ': ' + F.num(mult.v, 2) + '. פטור ממס שבח וממס רכישה, מע״מ אפס.';
    return { answer: answer, figure: svgArea(area, cap, old), lines: lines, note: notes.join('<br>'), table: table,
      formula: 'תקרת השטח לפטור (דוח הרשות 2025, נספח א): הגבוה מבין 120 מ״ר, ושטח הדירה כפול 1.5 ולא יותר מ-200 מ״ר; האפשרות של 150% מהשווי תלויה בשמאות ולא מחושבת כאן. המכפיל: דירות אחרי הבנייה חלקי דירות היום, לפי מפת הרשות, חישוב שלנו. ' + old + ' מ״ר: מה שהתקן ציין כמקובל לפני העדכון של 13.6.2022, שקבע במקומו טבלת רגישות.',
      sources: srcs(D, ['R25', 'LAW', 'FAQ', 'S21', 'MDL', 'MAP']), text: txt };
  }

  function svgApproval(rc, now, avg) {
    var ap = ymOf(rc.ap), el = months(ap, now), avgM = Math.round(avg[1] * 12), span = Math.max(el, avgM) + 12, XR = 396, XL = 30, y0 = 70, g = [];
    var x = function (m) { return XR - (XR - XL) * Math.max(0, Math.min(1, m / span)); };
    g.push('<text x="410" y="24" class="t" text-anchor="start" style="font-size:18px">' + esc('מאז אישור התכנית, בשנים') + '</text>');
    g.push('<line x1="' + XL + '" y1="' + y0 + '" x2="' + XR + '" y2="' + y0 + '" stroke="#12202A" stroke-width="2"/>');
    g.push('<rect x="' + x(el) + '" y="' + (y0 - 7) + '" width="' + (XR - x(el)) + '" height="14" fill="#2F6F86" opacity=".85"/>');
    g.push('<line x1="' + x(avgM) + '" y1="' + (y0 - 24) + '" x2="' + x(avgM) + '" y2="' + (y0 + 24) + '" stroke="#12202A" stroke-width="2" stroke-dasharray="5 4"/>');
    g.push('<text x="' + x(avgM) + '" y="' + (y0 - 30) + '" text-anchor="middle" style="font-size:15px;fill:#12202A">' + esc('ממוצע ' + F.num(avg[1], 1)) + '</text>');
    g.push('<circle cx="' + XR + '" cy="' + y0 + '" r="6" fill="#1F4B5C"/><text x="' + XR + '" y="' + (y0 + 32) + '" text-anchor="end" style="font-size:15px;fill:#12202A;font-weight:600">' + esc('אישור ' + dd(rc.ap)) + '</text>');
    g.push('<text x="' + x(el) + '" y="' + (y0 + 32) + '" text-anchor="middle" class="r" style="font-size:15px">' + esc('היום: ' + F.num(el / 12, 1)) + '</text>');
    g.push('<text x="410" y="' + (y0 + 66) + '" text-anchor="start" style="font-size:15px;fill:#3E4C58">' + esc('ממוצע של ' + avg[2] + ' מתחמים, ' + avg[0] + '. לא תחזית') + '</text>');
    return '<svg class="nli__wall" direction="rtl" viewBox="0 0 420 ' + (y0 + 80) + '" role="img" aria-label="' + esc('התכנית אושרה ב-' + dd(rc.ap) + ', עברו ' + F.num(el / 12, 1) + ' שנים; ממוצע הרשות ' + F.num(avg[1], 1) + ' שנים עד היתר ראשון') + '">' + g.join('') + '</svg>';
  }

  function viewTime(v, D, T) {
    var L = D.law, lm = lastMap(T), now = ymOf(T.snaps[lm].d), first = String(v.first || '');
    var rc = v.cx && v.cx !== OTHER ? byKey(T, v.cx) : null, rcs = rc ? rc.s[lm] : -1, approved = !!(rc && rc.ap && rcs >= 3);
    var hasFirst = /^\d{4}-\d{2}$/.test(first);
    if (!hasFirst && !approved) return { error: { field: 'first', msg: 'בחרו את החודש שבו נחתמה העסקה הראשונה בבניין.' } };
    if (hasFirst && months(first, now) < 0) return { error: { field: 'first', msg: 'החודש אחרי תאריך הבדיקה (' + dd(T.snaps[lm].d) + ').' } };
    var N = (v.rows || []).reduce(function (t, x) { return t + (+x.u || 0); }, 0);
    var big = (rc && rc.e >= L.clock.big_complex_units) || N >= L.clock.big_complex_units;
    var avg = D.series.approval_to_permit[D.series.approval_to_permit.length - 1], lines = [], notes = [];
    var ck = hasFirst ? clock(first, L, big) : null;
    var next = ck ? [[ck.half, 'חצי מבעלי הדירות בכל בניין'], [ck.tf, 'שלוש חמישיות בכל בניין'], [ck.plan, 'הגשת תכנית מפורטת']].filter(function (p) { return months(now, p[0]) >= 0; })[0] : null;
    var yrs = approved ? months(ymOf(rc.ap), now) / 12 : 0;
    var answer = approved
      ? { label: 'מאז אישור התכנית של ' + rc.n, value: F.num(yrs, 1) + ' שנים', sub: esc('התכנית אושרה ב-' + dd(rc.ap) + ' לפי הרשות. ' + (rcs === 3 ? 'בממוצע עוברות ' + F.num(avg[1], 1) + ' שנים מאישור תכנית עד היתר ראשון (' + avg[2] + ' מתחמים שקיבלו היתר ב-' + avg[0] + '). ממוצע, לא תחזית למתחם הזה.' : 'המתחם כבר ' + STG[rcs] + ' לפי מפת הרשות.')) }
      : next
      ? { label: 'המועד הבא בסעיף 1ד, מהעסקה הראשונה ב-' + dd(first), value: dd(next[0]), sub: esc(next[1] + '. אם עד אז היזם לא הגיע לזה, רוב בעלי הדירות באסיפה כללית יכול להחליט שמי שחתם רשאי לבטל את העסקה.' + (big ? ' במתחם של 120 יחידות ומעלה כל המועדים ארוכים בשנה.' : '')) }
      : { label: 'כל המועדים של סעיף 1ד עברו', value: dd(ck.plan), tone: 'survey', sub: esc('מהעסקה הראשונה ב-' + dd(first) + ' עברו ' + F.num(months(first, now) / 12, 1) + ' שנים. אם היזם לא עמד בהם, רוב בעלי הדירות באסיפה כללית יכול להחליט שמי שחתם רשאי לבטל.') };
    var past = function (ym) { return months(now, ym) < 0 ? ' (עבר)' : ''; };
    if (ck) {
      lines.push({ label: 'חצי מבעלי הדירות בכל בניין' + past(ck.half), value: dd(ck.half) });
      lines.push({ label: 'שלוש חמישיות בכל בניין' + past(ck.tf), value: dd(ck.tf) });
      lines.push({ label: 'הגשת תכנית מפורטת למוסד התכנון' + past(ck.plan), value: dd(ck.plan) });
      if (big) lines.push({ label: 'מתחם של 120 יחידות ומעלה: תוספת', value: '12 חודשים' });
    }
    complexLines(T, v, lines, notes);
    if (approved) lines.push({ label: 'עברו מאז אישור התכנית', value: F.num(yrs, 1) + ' שנים' });
    lines.push({ label: 'מאישור תכנית עד היתר ראשון, ממוצע ' + avg[0] + ' (' + avg[2] + ' מתחמים)', value: F.num(avg[1], 1) + ' שנים' });
    lines.push({ label: 'פינוי עד דירת התמורה, בהנחות המחשבון הממשלתי', value: D.model.evac_months + ' חודשים' });
    if (!ck) notes.push(esc('בחרו את החודש שבו נחתמה העסקה הראשונה בבניין, ותראו גם את המועדים שסעיף 1ד נותן ליזם.'));
    notes.push(esc('הכלל של 4 שנים ו-6 חודשים להגשת התכנית לא חל על מתחם שהוכרז לפי סעיף 14(א)(1) לחוק הרשות הממשלתית להתחדשות עירונית. כשעד 40% מהדירות בבניין הן דירות ציבוריות, סופרים את החצי ואת שלוש החמישיות רק מהדירות שאינן ציבוריות.'));
    var table = { title: 'שלבי פינוי בינוי: מה החוק דורש בכל שלב, וכמה זמן לפי מקור רשמי', head: ['שלב', 'מה החוק או הרשות קובעים', 'זמן'],
      rows: [['לפני העסקה הראשונה', 'כינוס של בעלי הדירות, ומסמך עיקרי הצעה לכולם שבועיים לפחות לפני החתימה (סעיף 1א)', 'שבועיים'],
             ['העסקה הראשונה נחתמה', 'הודעה לכל בעלי הדירות, ומסמכי העסקה לחותם (סעיף 1ב)', ck ? dd(first) : 'החודש שתבחרו'],
             ['חצי מבעלי הדירות', 'אחרת רוב יכול לאפשר ביטול (סעיף 1ד)', ck ? dd(ck.half) : 'שנתיים'],
             ['שלוש חמישיות', 'אותו כלל (סעיף 1ד)', ck ? dd(ck.tf) : '4 שנים'],
             ['הגשת תכנית מפורטת', 'אותו כלל, למעט מתחם לפי סעיף 14(א)(1) (סעיף 1ד)', ck ? dd(ck.plan) : '4.5 שנים'],
             ['רוב מיוחס', 'שני שלישים במקבץ ושלוש חמישיות בכל בניין; מכאן אפשר לתבוע דייר שמסרב סירוב בלתי סביר (סעיף 2)', 'לפי ההחתמות'],
             ['אישור התכנית', 'במוסד התכנון', approved ? dd(rc.ap) : 'לפי התכנון'],
             ['היתר בנייה ראשון', 'ממוצע הרשות ל-' + avg[0], F.num(avg[1], 1) + ' שנים מהאישור'],
             ['פינוי, הריסה ובנייה', 'שכירות וערבויות לפי ההסכם', D.model.evac_months + ' חודשים בהנחות המחשבון הממשלתי'],
             ['מסירה ורישום', 'לפי המועדים המרביים שבהסכם', 'לפי ההסכם']] };
    var txt = 'פינוי בינוי' + (approved ? ', ' + rc.n + ': התכנית אושרה ב-' + dd(rc.ap) + ', עברו ' + F.num(yrs, 1) + ' שנים.' : '') + (ck ? ' השעון של סעיף 1ד מהעסקה הראשונה ב-' + dd(first) + ': חצי מהדירות עד ' + dd(ck.half) + ', שלוש חמישיות עד ' + dd(ck.tf) + ', הגשת תכנית עד ' + dd(ck.plan) + '.' : '') + ' מאישור תכנית עד היתר ראשון: ' + F.num(avg[1], 1) + ' שנים בממוצע (הרשות, ' + avg[0] + ').';
    return { answer: answer, figure: ck ? svgClock(first, ck, now, approved && rc.ap, avg[1]) : svgApproval(rc, now, avg), lines: lines, note: notes.join('<br>'), table: table,
      formula: 'סעיף 1ד לחוק פינוי ובינוי: מהיום שבו נחתמה העסקה הראשונה, אם היזם לא התקשר עם מחצית מבעלי הדירות בבית המשותף בתוך שנתיים או עם שלוש חמישיות בתוך ארבע שנים, או לא הגיש תכנית מפורטת בתוך ארבע שנים ושישה חודשים, רוב בעלי הדירות באסיפה כללית רשאי להחליט שהחותמים רשאים לבטל. במתחם של 120 יחידות ומעלה: שנה נוספת. החודשים כאן לפי החודש שבחרתם; היום המדויק לפי תאריך העסקה.',
      sources: srcs(D, ['LAW', 'R25', 'MDL', 'MAP']), text: txt };
  }

  function presets(D, T) {
    var lm = lastMap(T), out = [];
    out.push({ key: 'maj', label: 'שלושה בניינים, 48 דירות', sub: 'שני שלישים במקבץ, וחסרה חתימה בבניין אחד', set: { view: 'maj', city: OTHER, cx: OTHER, rows: [{ u: 24, s: 17 }, { u: 16, s: 9 }, { u: 8, s: 6 }] } });
    out.push({ key: 'ok', label: 'אותם בניינים, הרוב מתקיים', sub: 'שלוש חמישיות בכל בניין', set: { view: 'maj', city: OTHER, cx: OTHER, rows: [{ u: 24, s: 17 }, { u: 16, s: 10 }, { u: 8, s: 5 }] } });
    out.push({ key: 'mine', label: 'דירה של 68 מ״ר, בעלת דירה בת 76', sub: 'התקרה לפטור ממס וחלופות מגיל 75', set: { view: 'mine', area: 68, age: '75' } });
    out.push({ key: 'clock', label: 'העסקה הראשונה נחתמה ב-6.2024', sub: 'המועדים של סעיף 1ד', set: { view: 'time', first: '2024-06' } });
    var ap = T.recs.filter(function (r) { return r.s[lm] === 3 && r.ap && r.e && r.p && !r.pm; }).sort(function (a, b) { return b.p - a.p; })[0];
    if (ap) out.push({ key: 'approved', label: ap.n + ', ' + ap.c, sub: 'תכנית מאושרת מ-' + dd(ap.ap), set: { view: 'time', city: ap.c, cx: ap.k, first: '' } });
    return out;
  }

  NI.register('pinui', {
    kicker: 'מחשבון · פינוי בינוי',
    title: 'הבניין שלכם בפינוי בינוי: הרוב לפי החוק, מה מגיע לכם וכמה זמן',
    lede: 'רושמים כמה דירות יש בכל בניין וכמה חתמו, ורואים מה חסר לרוב המיוחס לפי החוק, בניין אחר בניין. בוחרים עיר ומתחם כדי לראות את השלב אצל הרשות ואת המכפיל, את השטח שפטור ממס לדירה שלכם, ואת המועדים שהחוק נותן ליזם.',
    strip: function (data) { var D = data.pinui, k = D.key2025; return [{ label: 'תכניות פינוי בינוי שאושרו ב-2025', value: F.num(k.pb_plans) }, { label: 'דירות בתכניות האלה', value: F.num(k.pb_units) }, { label: 'מאישור עד היתר, ממוצע 2025', value: F.num(D.series.approval_to_permit[D.series.approval_to_permit.length - 1][1], 1) + ' שנים' }, { label: 'רוב מיוחס במקבץ', value: 'שני שלישים' }]; },
    presets: function (data) { return presets(data.pinui, data.urtrack); },
    defaults: function (data) { var p = presets(data.pinui, data.urtrack)[0]; return Object.assign({ view: 'maj', city: OTHER, cx: OTHER, rows: [{ u: 24, s: 17 }], area: 68, age: 'u70', first: '2024-06' }, JSON.parse(JSON.stringify(p.set))); },
    fields: [
      { id: 'view', label: 'מה לבדוק', type: 'segmented', options: [{ value: 'maj', label: 'הרוב והחתימות' }, { value: 'mine', label: 'מה מגיע לי' }, { value: 'time', label: 'השעון של החוק' }] },
      { id: 'city', label: 'עיר', type: 'select', optionsFrom: function (v, data) { return [{ value: OTHER, label: 'לא לבחור עיר' }].concat(cities(data.urtrack).map(function (x) { return { value: x.c, label: x.c + ' (' + x.n + ')' }; })); } },
      { id: 'cx', label: 'מתחם, לפי מפת הרשות', type: 'select', showIf: function (v) { return v.city !== OTHER; }, optionsFrom: function (v, data) { if (v.city === OTHER) return [{ value: OTHER, label: 'הבניין שלנו לא ברשימה' }]; return [{ value: OTHER, label: 'הבניין שלנו לא ברשימה' }].concat(inCity(data.urtrack, v.city).map(function (r) { return { value: r.k, label: r.n }; })); } },
      { id: 'rows', label: 'הבניינים במקבץ: דירות וחתימות', type: 'rows', addLabel: 'הוספת בניין', showIf: function (v) { return v.view !== 'mine'; }, cols: [{ id: 'u', label: 'דירות בבניין', unit: 'דירות' }, { id: 's', label: 'חתמו', unit: 'חתמו' }], blank: function () { return { u: 12, s: 0 }; } },
      { id: 'area', label: 'שטח הדירה שלכם היום', type: 'number', unit: 'מ״ר', showIf: function (v) { return v.view === 'mine'; } },
      { id: 'age', label: 'גיל בעל הדירה במועד העסקה הראשונה', type: 'segmented', showIf: function (v) { return v.view === 'mine'; }, options: [{ value: 'u70', label: 'עד 69' }, { value: '70', label: '70 עד 74' }, { value: '75', label: '75 ומעלה' }] },
      { id: 'first', label: 'החודש שבו נחתמה העסקה הראשונה בבניין', type: 'month', showIf: function (v) { return v.view === 'time'; } }
    ],
    onField: function (id, v) { if (id === 'city') v.cx = OTHER; },
    compute: function (v, data) {
      var D = data.pinui, T = data.urtrack;
      if (!D || !D.law || !T || !T.recs) return { error: { field: null, msg: 'הנתונים לא נטענו.' } };
      return v.view === 'mine' ? viewMine(v, D, T) : v.view === 'time' ? viewTime(v, D, T) : viewMaj(v, D, T);
    }
  });
})();
