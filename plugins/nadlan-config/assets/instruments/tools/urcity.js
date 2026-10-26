/* NadLan Instruments · urcity v1 (G3 moat, 26.10.2026): "התחדשות עירונית בעיר שלכם" on /urban-renewal/.
   Three views:
   - city  · העיר שלי: the city's complexes on the authority's map today, by stage and track, units today and after building and the
             multiplier, what moved since the data.gov.il file (the tracker's own count), and what the authority's 2025 report says about
             building renewal in the city: the city plan that replaces TAMA 38 and its status, whether TAMA 38 was extended there,
             years from permit request to permit, apartments sold in renewal projects, tax-track declarations.
   - track · המסלול לבניין שלי: for one building (apartments, permit year, in a complex or not) and its city, which tracks stay open
             (pinui binui, TAMA 38, the fast licensing plan of section 145א1), the majority each one needs by law in apartments for
             this building, and the comparison table of annex A of the 2025 report.
   - rank  · השוואת ערים: every city with complexes, sortable in print by complexes, approved, proposed units, multiplier.
   Data: data/urcity.json (tools/urban/build_g2g3_data.py) + data/renewal-track.json. Pure logic in NLUC for checks. Honesty: the
   report's status lines as printed, with the report date; nothing about what happened after May 2026 in a city that the report does
   not say; the multiplier labelled as our calculation. */
(function () {
  'use strict';
  var STG = ['ללא שלב', 'תכנון ראשוני', 'תכנון סטטוטורי', 'תכנית מאושרת', 'במימוש', 'אחרי רישוי'];
  var E = 1e-9;
  function atLeast(n, a, b) { return Math.ceil(n * a / b - E); }
  function n0(x) { return String(Math.round(x || 0)).replace(/\B(?=(\d{3})+(?!\d))/g, ','); }
  function dd(iso) { var p = String(iso || '').split('-'); return p.length === 3 ? (+p[2]) + '.' + (+p[1]) + '.' + p[0] : String(iso || ''); }
  function lastMap(T) { for (var i = T.snaps.length - 1; i >= 0; i--) if (T.snaps[i].k === 'map') return i; return -1; }
  function find(list, c) { for (var i = 0; i < list.length; i++) if (list[i].c === c) return list[i]; return null; }

  /** Per city, from the authority's latest map: complexes, stage and track counts, units with both numbers, multiplier. */
  function stats(T) {
    if (T.__uc) return T.__uc;
    var lm = lastMap(T), by = {}, nat = { n: 0, st: [0, 0, 0, 0, 0, 0], tr: [0, 0, 0, 0], e: 0, p: 0, ea: 0, pa: 0 };
    T.recs.forEach(function (r) {
      var s = r.s[lm]; if (s === -1) return;
      var c = by[r.c] = by[r.c] || { c: r.c, n: 0, st: [0, 0, 0, 0, 0, 0], tr: [0, 0, 0, 0], e: 0, p: 0, ea: 0, pa: 0, list: [] };
      [c, nat].forEach(function (o) { o.n++; o.st[Math.max(0, s)]++; o.tr[r.t || 0]++; o.ea += r.e || 0; o.pa += r.p || 0; if (r.e && r.p) { o.e += r.e; o.p += r.p; } });
      c.list.push(r);
    });
    Object.keys(by).forEach(function (k) { var c = by[k]; c.mult = c.e ? c.p / c.e : 0; c.appr = c.st[3] + c.st[4] + c.st[5]; c.list.sort(function (a, b) { return (b.p || 0) - (a.p || 0) || a.n.localeCompare(b.n, 'he'); }); });
    nat.mult = nat.e ? nat.p / nat.e : 0; nat.appr = nat.st[3] + nat.st[4] + nat.st[5];
    return (T.__uc = { by: by, nat: nat, lm: lm });
  }
  /** Every city the tool knows: on the map, or named by the report (building renewal) without a complex on the map. */
  function cityList(T, U) {
    var S = stats(T), o = {};
    Object.keys(S.by).forEach(function (c) { o[c] = S.by[c].n; });
    [U.replace, U.req2permit, U.sold, U.taxcity].forEach(function (l) { l.forEach(function (x) { if (!(x.c in o)) o[x.c] = 0; }); });
    return Object.keys(o).sort(function (a, b) { return a.localeCompare(b, 'he'); }).map(function (c) { return { c: c, n: o[c] }; });
  }
  /** The report's word on TAMA 38 in a city: the replacement plan and its status, the extension, a plan in force before. */
  function tamaIn(U, c) {
    var r = find(U.replace, c);
    if (r) return { plan: true, st: String(r.st || '').replace(/^בבדיקה /, 'בשלב בדיקה '), ext: r.ext, self: !!r.self, bld: r.bld || 0, e: r.e || 0, p: r.p || 0, approved: /אושרה/.test(r.st) };
    if (U.inforce.indexOf(c) > -1) return { plan: true, st: 'תכנית עירונית הייתה בתוקף ערב פקיעת תמ"א 38', ext: false, inforce: true, approved: true };
    return { plan: false };
  }
  /** Which tracks stay open for one building. */
  function tracks(b, U, c) {
    var L = U.law, out = [], t = tamaIn(U, c), old = b.permit === 'pre80' || b.permit === '80to84';
    var pbOpen = b.complex === 'yes' || b.units >= L.complex_def.min_existing;
    out.push({ id: 'pb', open: b.complex === 'yes' ? 'yes' : b.complex === 'no' && b.units < L.complex_def.min_existing ? 'no' : 'maybe',
      why: b.complex === 'yes' ? 'הבניין במתחם שהרשות מפרסמת' : b.units >= L.complex_def.min_existing ? 'בבניין ' + b.units + ' דירות: מעל הסף של 24 יחידות קיימות למתחם, אבל צריך הכרזה ותכנית' : b.complex === 'no' ? 'מתחם צריך 24 יחידות קיימות לפחות; בניין קטן נכנס רק עם בניינים סמוכים' : 'בדקו ביומן המתחמים אם הבניין בתוך מתחם',
      need: 'שני שלישים מהדירות במקבץ ושלוש חמישיות בכל בניין' });
    var tamaOpen = !old ? 'no' : (t.plan && t.approved) ? 'city' : 'maybe';
    out.push({ id: 'tama', open: tamaOpen,
      why: !old ? 'תמ"א 38 חלה על בניין שההיתר שלו ניתן לפני 1.1.1980, או עד 31.12.1984 באישור מהנדס' : t.plan && t.approved ? 'בעיר ' + t.st + ': זכויות הבנייה לפי התכנית העירונית' : t.plan && t.ext ? 'לפי הדוח, בעיר מקודמת תכנית מחליפה (' + t.st + ') ותוקף תמ"א 38 הוארך עד מאי 2026 או עד אישור התכנית, המוקדם מביניהם' : c === 'תל אביב יפו' ? 'לפי הדוח, בתל אביב לא ניתנה הארכה לתמ"א 38, ותכנית עירונית בהכנה' : 'תמ"א 38 פקעה באוקטובר 2023; בעיר הזאת הדוח לא מציין תכנית מחליפה',
      need: 'חיזוק עם דירות חדשות: שני שלישים מהדירות ומהרכוש המשותף, באישור המפקח; הריסה ובנייה: אותו רוב' });
    out.push({ id: 'fast', open: b.units >= 4 ? 'yes' : 'no',
      why: b.units >= 4 ? 'בניין של 2 קומות לפחות ו-4 דירות לפחות: תכנית בוועדה המקומית, וזכויות עד 400% בהריסה ובנייה' : 'המסלול לבניין עם 4 דירות לפחות',
      need: 'כמו בתמ"א 38: שני שלישים מהדירות ומהרכוש המשותף' });
    return { list: out, tama: t, need23: atLeast(b.units, 2, 3), need60: atLeast(b.units, 3, 5) };
  }
  window.NLUC = { stats: stats, cityList: cityList, tamaIn: tamaIn, tracks: tracks, atLeast: atLeast };
  if (!window.NadLanInstruments) return;
  var NI = window.NadLanInstruments, F = NI.fmt, esc = NI.esc;
  var OPEN = { yes: 'פתוח', maybe: 'צריך לבדוק', city: 'לפי התכנית בעיר', no: 'לא מתאים' };

  function svgCity(c, nat) {
    var g = [], W = 260, XR = 300, y = 56, mx = Math.max.apply(null, c.st.concat([1]));
    g.push('<text x="410" y="24" class="t" text-anchor="start" style="font-size:17px">' + esc(c.c + ': המתחמים לפי השלב אצל הרשות') + '</text>');
    [1, 2, 3, 4, 0].forEach(function (s) {
      var v = c.st[s] + (s === 4 ? c.st[5] : 0), w = v ? Math.max(3, Math.round(W * v / mx)) : 0;
      g.push('<text x="410" y="' + (y + 5) + '" text-anchor="start" style="font-size:15px;fill:' + (s === 0 ? '#5E6A75' : '#12202A') + '">' + esc(STG[s]) + '</text>');
      g.push('<rect x="' + (XR - W) + '" y="' + (y - 9) + '" width="' + W + '" height="18" fill="#EDF1F4"/>');
      if (w) g.push('<rect x="' + (XR - w) + '" y="' + (y - 9) + '" width="' + w + '" height="18" fill="' + (s >= 3 ? '#1F4B5C' : s === 0 ? '#8A97A2' : '#2F6F86') + '"/>');
      g.push('<text x="' + (XR - w - 6) + '" y="' + (y + 6) + '" text-anchor="start" class="m" style="font-size:15px">' + (v || 'אין') + '</text>');
      y += 34;
    });
    y += 10;
    g.push('<text x="410" y="' + y + '" text-anchor="start" style="font-size:14px;fill:#12202A">' + esc('מכפיל הדירות: ' + (c.mult ? '× ' + F.num(c.mult, 2) : 'אין נתון') + ' בעיר, × ' + F.num(nat.mult, 2) + ' בכל הארץ (חישוב שלנו)') + '</text>');
    return '<svg class="nli__wall" direction="rtl" viewBox="0 0 420 ' + (y + 18) + '" role="img" aria-label="' + esc(c.c + ': ' + [1, 2, 3, 4, 0].map(function (s) { return STG[s] + ' ' + (c.st[s] + (s === 4 ? c.st[5] : 0)); }).join(', ')) + '">' + g.join('') + '</svg>';
  }

  function svgRank(S) {
    var top = Object.keys(S.by).map(function (k) { return S.by[k]; }).sort(function (a, b) { return b.n - a.n; }).slice(0, 15), g = [], y = 50, XR = 270, W = 200, mx = top[0] ? top[0].n : 1;
    g.push('<text x="410" y="24" class="t" text-anchor="start" style="font-size:17px">' + esc('15 הערים עם הכי הרבה מתחמים במפת הרשות') + '</text>');
    top.forEach(function (c) {
      var w = Math.max(3, Math.round(W * c.n / mx)), wa = Math.round(W * c.appr / mx);
      g.push('<text x="410" y="' + (y + 5) + '" text-anchor="start" style="font-size:15px;fill:#12202A">' + esc(c.c) + '</text>');
      g.push('<rect x="' + (XR - w) + '" y="' + (y - 8) + '" width="' + w + '" height="16" fill="#2F6F86"/>');
      if (wa) g.push('<rect x="' + (XR - wa) + '" y="' + (y - 8) + '" width="' + wa + '" height="16" fill="#1F4B5C"/>');
      g.push('<text x="' + (XR - w - 6) + '" y="' + (y + 5) + '" text-anchor="start" class="m" style="font-size:14px">' + c.n + (c.mult ? ' · × ' + F.num(c.mult, 1) : '') + '</text>');
      y += 26;
    });
    g.push('<text x="410" y="' + (y + 10) + '" text-anchor="start" style="font-size:13px;fill:#5E6A75">' + esc('כהה: תכנית מאושרת או במימוש. × המכפיל, חישוב שלנו') + '</text>');
    return '<svg class="nli__wall" direction="rtl" viewBox="0 0 420 ' + (y + 24) + '" role="img" aria-label="' + esc(top.map(function (c) { return c.c + ' ' + c.n; }).join(', ')) + '">' + g.join('') + '</svg>';
  }

  function srcs(U, keys) { return keys.map(function (k) { var s = U.sources[k]; return { label: s.label, url: s.url }; }); }

  function viewCity(v, U, T) {
    var S = stats(T), c = S.by[v.city], md = T.snaps[S.lm].d, ag = (T.agg.cities || {})[v.city] || {}, lines = [], notes = [];
    var tm = tamaIn(U, v.city), rq = find(U.req2permit, v.city), so = find(U.sold, v.city), tx = find(U.taxcity, v.city), dist = U.district[v.city];
    var answer = c
      ? { label: v.city + ': מתחמי התחדשות עירונית במפת הרשות, ' + dd(md), value: n0(c.n) + ' מתחמים', sub: esc([[c.appr, STG[3] + ' או במימוש'], [c.st[2], STG[2]], [c.st[1], STG[1]], [c.st[0], 'בלי שלב במפה']].filter(function (x) { return x[0]; }).map(function (x) { return x[1] + ': ' + x[0]; }).join('. ') + (c.pa ? '. דירות היום ' + n0(c.ea) + ', אחרי הבנייה ' + n0(c.pa) : '') + '.') }
      : { label: v.city + ': מתחמי התחדשות עירונית במפת הרשות, ' + dd(md), value: 'אין מתחמים', tone: 'survey', sub: esc('לעיר הזאת אין מתחם במפת הרשות היום. מה שהדוח של הרשות לשנת 2025 אומר על ההתחדשות הבניינית בה מופיע למטה.') };
    if (c) {
      lines.push({ label: 'מסלול מיסוי', value: F.num(c.tr[1]) }); lines.push({ label: 'מסלול רשויות', value: F.num(c.tr[2]) }); if (c.tr[3]) lines.push({ label: 'טרם הוכרז', value: F.num(c.tr[3]) });
      lines.push({ label: 'מכפיל הדירות בעיר (חישוב שלנו)', value: c.mult ? '× ' + F.num(c.mult, 2) : 'אין נתון' });
      lines.push({ label: 'מכפיל הדירות בכל הארץ', value: '× ' + F.num(S.nat.mult, 2) });
      if (ag.add) lines.push({ label: 'נוספו לרשימה מאז ' + dd(T.agg.since), value: F.num(ag.add) }); if (ag.up) lines.push({ label: 'עלו שלב מאז ' + dd(T.agg.since), value: F.num(ag.up) });
    }
    if (dist) lines.push({ label: 'מחוז', value: dist });
    lines.push({ label: 'תכנית עירונית שמחליפה את תמ"א 38', value: tm.plan ? (tm.approved ? 'יש' : 'בתהליך') : 'לא בדוח' });
    if (tm.plan && tm.st) notes.push(esc('תמ"א 38 ב' + v.city + ', לפי דוח הרשות לשנת 2025: ' + tm.st + (tm.bld ? ' (' + n0(tm.bld) + ' מבנים בתכנית, ' + n0(tm.e) + ' דירות היום ו-' + n0(tm.p) + ' מוצעות)' : '') + '. ' + (tm.inforce ? '' : !tm.ext ? 'בעיר הזאת לא ניתנה הארכה לתמ"א 38.' : tm.approved ? 'בערים שקידמו תכנית כזאת, תוקף תמ"א 38 הוארך עד מאי 2026 או עד אישור התכנית, המוקדם מביניהם.' : 'בעיר הזאת תוקף תמ"א 38 הוארך עד מאי 2026 או עד אישור התכנית, המוקדם מביניהם.') + ' מה חל היום בודקים בוועדה המקומית.'));
    else notes.push(esc('תמ"א 38 פקעה באוקטובר 2023. הדוח של הרשות לא מונה את ' + v.city + ' בין הערים שמקדמות תכנית עירונית מחליפה; מה חל היום בבניין שלכם בודקים בוועדה המקומית.'));
    if (rq) lines.push({ label: 'התחדשות בניינית: מבקשה עד היתר, 2025 (' + rq.n + ' היתרים)', value: F.num(rq.y, 1) + ' שנים' });
    if (so) lines.push({ label: 'דירות שנמכרו בפרויקטי התחדשות ב-2025', value: F.num(so.n) });
    if (tx) lines.push({ label: 'הוכרזו במסלול המיסוי עד סוף 2025', value: tx.n + ' מתחמים, ' + n0(tx.p) + ' דירות' });
    notes.push('<a href="/urban-renewal/map/">' + esc('מפת התחדשות עירונית ויומן המתחמים של ' + v.city) + '</a> · <a href="/urban-renewal/pinui-binui/">' + esc('פינוי בינוי: הרוב לפי החוק, דירה אחר דירה') + '</a> · <a href="/urban-renewal/check/">' + esc('בדיקת בניין חינמית') + '</a>');
    var table = c ? { title: v.city + ': ' + c.n + ' מתחמים, מהגדול לקטן לפי דירות אחרי הבנייה', head: ['מתחם', 'השלב אצל הרשות', 'מסלול', 'דירות היום ← אחרי'], num: [3], phoneHide: [2],
      rows: c.list.map(function (r) { var s = r.s[S.lm]; return [r.n, STG[Math.max(0, s)], T.tracks[r.t || 0] || '', r.p ? (r.e ? n0(r.e) + ' → ' : '') + n0(r.p) : '']; }) } : null;
    var txt = 'התחדשות עירונית ב' + v.city + (c ? ': ' + c.n + ' מתחמים במפת הרשות (' + dd(md) + '), ' + c.appr + ' בתכנית מאושרת או במימוש, דירות היום ' + n0(c.ea) + ' ואחרי הבנייה ' + n0(c.pa) + '.' : ': אין מתחם במפת הרשות.') + (tm.plan && tm.st ? ' תמ"א 38: ' + tm.st + ' (דוח הרשות 2025).' : '') + (rq ? ' מבקשה עד היתר בהתחדשות בניינית: ' + F.num(rq.y, 1) + ' שנים (2025).' : '');
    return { answer: answer, figure: c ? svgCity(c, S.nat) : null, lines: lines, note: notes.join('<br>'), table: table,
      formula: 'המתחמים, השלבים, המסלולים והדירות: מפת הרשות הממשלתית להתחדשות עירונית ב-' + dd(md) + ', דרך יומן המתחמים שלנו. המכפיל: דירות אחרי הבנייה חלקי דירות היום במתחמים שיש להם שני המספרים, חישוב שלנו. נוספו ועלו שלב: מאז קובץ data.gov.il של ' + dd(T.agg.since) + '. תמ"א 38, זמני ההיתר, המכירות וההכרזות: דוח הרשות לשנת 2025, כפי שנכתבו בו.',
      sources: srcs(U, ['MAP', 'FILE', 'R25']), text: txt };
  }

  function viewTrack(v, U, T) {
    var u = Math.round(+v.units || 0);
    if (!(u >= 2 && u <= 400)) return { error: { field: 'units', msg: 'מספר הדירות בבניין: בין 2 ל-400.' } };
    var R = tracks({ units: u, permit: v.permit, complex: v.complex }, U, v.city), open = R.list.filter(function (t) { return t.open === 'yes' || t.open === 'city'; });
    var name = {}; U.tracks.forEach(function (t) { name[t.id] = t.name; });
    var answer = { label: 'בניין של ' + u + ' דירות ב' + v.city + ': המסלולים שנשארים פתוחים', value: open.length ? open.length + ' מתוך 3' : 'בדיקה בוועדה', tone: open.length ? '' : 'survey',
      sub: esc(R.list.map(function (t) { return name[t.id] + ': ' + OPEN[t.open]; }).join(' · ')) };
    var lines = [{ label: 'שני שלישים מהדירות בבניין', value: R.need23 + ' דירות' }, { label: 'שלוש חמישיות מהדירות בבניין', value: R.need60 + ' דירות' }];
    R.list.forEach(function (t) { lines.push({ label: name[t.id], value: OPEN[t.open] }); });
    var notes = R.list.map(function (t) { return esc(name[t.id] + ': ' + t.why + '. הרוב: ' + t.need + '.'); });
    notes.push(esc('בהרחבת דירות בתמ"א 38 בלבד, בלי דירות חדשות: 60% מהדירות. הריסה ובנייה של בניין, בתכנית עירונית או לפי סעיף 145א1, מחזקת לפי התקן המלא; חיזוק ועיבוי מתאים אותו ככל האפשר (נספח א לדוח הרשות 2025).'));
    var A = U.tracks, rows = [['מה עושים'].concat(A.map(function (t) { return t.do; })), ['הבניין'].concat(A.map(function (t) { return t.bld; })), ['איך מאשרים'].concat(A.map(function (t) { return t.route; })),
      ['הכרזה על מתחם'].concat(A.map(function (t) { return t.declare; })), ['חובת תכנית'].concat(A.map(function (t) { return t.plan; })), ['היקף במצב הקיים'].concat(A.map(function (t) { return t.scope; })), ['זכויות במצב החדש'].concat(A.map(function (t) { return t.rights; })),
      ['פטור ממס שבח', 'פרק חמישי 4, ללא הגבלה על מספר הדירות', 'פרק חמישי 5, עד סוף 2033; בהריסה 2 דירות בבניין', 'כמו בתמ"א 38'],
      ['תקרת הפטור', '120 מ"ר, 150% מהשווי, או 50% יותר עד 200 מ"ר', 'חיזוק: 25 מ"ר; הריסה: 25 מ"ר או שווי עד 1,777,600 ₪', 'כמו בתמ"א 38'],
      ['היטל השבחה', '25%, או 50% או פטור לפי אזור בעיר', 'פטור לזכויות התמ"א; בהריסה 25% מעבר ל-2.5 קומות', '25% על הזכויות שבחוק, 50% על כל תוספת']];
    var table = { title: 'שלושת המסלולים זה לצד זה (נספח א לדוח הרשות לשנת 2025)', head: ['מאפיין'].concat(A.map(function (t) { return t.name; })), rows: rows };
    var txt = 'בניין של ' + u + ' דירות ב' + v.city + ': ' + R.list.map(function (t) { return name[t.id] + ' ' + OPEN[t.open]; }).join(', ') + '. שני שלישים מהדירות: ' + R.need23 + '.';
    return { answer: answer, lines: lines, note: notes.join('<br>'), table: table,
      formula: 'המסלולים לפי נספח א לדוח הרשות לשנת 2025 (פינוי בינוי, תמ"א 38, תכנית לרישוי מהיר). הרוב בפינוי בינוי לפי סעיף 1 לחוק פינוי ובינוי; בתמ"א 38 ובתכנית לפי סעיף 145א1 לפי חוק החיזוק (סעיפים 4, 5, 5א). המצב בעיר: הרשימה של הדוח (עמודים 92 ו-93), כפי שנכתבה בו.',
      sources: srcs(U, ['R25', 'LAW', 'LTAMA']), text: txt };
  }

  function viewRank(v, U, T) {
    var S = stats(T), md = T.snaps[S.lm].d, all = Object.keys(S.by).map(function (k) { return S.by[k]; }).sort(function (a, b) { return b.n - a.n || a.c.localeCompare(b.c, 'he'); });
    var answer = { label: 'מתחמי התחדשות עירונית במפת הרשות, ' + dd(md), value: n0(S.nat.n) + ' ב-' + all.length + ' ערים', sub: esc(all.slice(0, 3).map(function (c) { return c.c + ' ' + c.n; }).join(', ') + '. בתכנית מאושרת או במימוש: ' + n0(S.nat.appr) + '. מכפיל הדירות בכל הארץ × ' + F.num(S.nat.mult, 2) + ' (חישוב שלנו).') };
    var table = { title: 'כל הערים: מתחמים, תכניות מאושרות, דירות ותמ"א 38', head: ['עיר', 'מחוז', 'מתחמים', 'מאושרת או במימוש', 'דירות אחרי הבנייה', 'מכפיל', 'תכנית מחליפת תמ"א 38'], num: [2, 3, 4, 5], phoneHide: [1, 4, 6],
      rows: all.map(function (c) { var t = tamaIn(U, c.c); return [c.c, U.district[c.c] || '', F.num(c.n), F.num(c.appr), F.num(c.pa), c.mult ? F.num(c.mult, 2) : '', t.plan ? t.st : '']; }) };
    var lines = [{ label: 'ערים עם מתחם במפה', value: F.num(all.length) }, { label: 'מתחמים', value: F.num(S.nat.n) }, { label: 'בתכנית מאושרת או במימוש', value: F.num(S.nat.appr) }, { label: 'מסלול מיסוי', value: F.num(S.nat.tr[1]) }, { label: 'מסלול רשויות', value: F.num(S.nat.tr[2]) }, { label: 'טרם הוכרז', value: F.num(S.nat.tr[3]) },
      { label: 'ערים עם תכנית מחליפת תמ"א 38 בדוח', value: F.num(U.replace.length + U.inforce.length) }];
    return { answer: answer, figure: svgRank(S), lines: lines, note: esc('בחרו "העיר שלי" ועיר אחת, ותראו את כל המתחמים שלה, את המסלולים ואת מה שהדוח אומר על תמ"א 38 בה.'), table: table,
      formula: 'מפת הרשות ב-' + dd(md) + ' דרך יומן המתחמים שלנו; המחוז לפי רשימת היישובים של הלמ"ס ב-data.gov.il; תכניות מחליפות תמ"א 38 לפי דוח הרשות לשנת 2025. המכפיל: חישוב שלנו.',
      sources: srcs(U, ['MAP', 'FILE', 'R25']), text: 'מתחמי התחדשות עירונית במפת הרשות (' + dd(md) + '): ' + S.nat.n + ' ב-' + all.length + ' ערים. ' + all.slice(0, 5).map(function (c) { return c.c + ' ' + c.n; }).join(', ') + '.' };
  }

  function presets(U, T) {
    return [
      { key: 'jlm', label: 'ירושלים', sub: 'הכי הרבה מתחמים, תכנית עירונית בשלב בדיקה מוקדמת', set: { view: 'city', city: 'ירושלים' } },
      { key: 'pt', label: 'פתח תקוה', sub: 'תכנית מחליפת תמ"א 38 אושרה ב-2025', set: { view: 'city', city: 'פתח תקוה' } },
      { key: 'tlv', label: 'תל אביב יפו', sub: 'בלי הארכה לתמ"א 38', set: { view: 'city', city: 'תל אביב יפו' } },
      { key: 'bld', label: 'בניין של 16 דירות משנות ה-70', sub: 'איזה מסלול נשאר פתוח', set: { view: 'track', city: 'רמת גן', units: 16, permit: 'pre80', complex: 'unk' } },
      { key: 'rank', label: 'השוואת ערים', sub: 'כל הערים, מתחמים ומכפיל', set: { view: 'rank' } }
    ];
  }

  NI.register('urcity', {
    kicker: 'מפה · התחדשות עירונית',
    title: 'התחדשות עירונית בעיר שלכם: מתחמים, מסלולים ותמ"א 38',
    lede: 'בוחרים עיר ורואים כמה מתחמים יש בה אצל הרשות ובאיזה שלב, כמה דירות יש בהם היום וכמה יהיו, מה זז מאז הבדיקה הקודמת, ומה הדוח של הרשות אומר על תמ"א 38 בעיר. או רושמים את הבניין שלכם ורואים איזה מסלול נשאר פתוח וכמה חתימות צריך.',
    strip: function (data) { var S = stats(data.urtrack), k = data.urcity.key2025; return [{ label: 'מתחמים במפת הרשות', value: F.num(S.nat.n) }, { label: 'בתכנית מאושרת או במימוש', value: F.num(S.nat.appr) }, { label: 'מכפיל הדירות', value: '× ' + F.num(S.nat.mult, 2) }, { label: 'מינהלות עירוניות', value: F.num(k.minhalot) }]; },
    presets: function (data) { return presets(data.urcity, data.urtrack); },
    defaults: function (data) { return { view: 'city', city: 'ירושלים', units: 16, permit: 'pre80', complex: 'unk' }; },
    fields: [
      { id: 'view', label: 'מה להציג', type: 'segmented', options: [{ value: 'city', label: 'העיר שלי' }, { value: 'track', label: 'המסלול לבניין שלי' }, { value: 'rank', label: 'השוואת ערים' }] },
      { id: 'city', label: 'עיר', type: 'select', showIf: function (v) { return v.view !== 'rank'; }, optionsFrom: function (v, data) { return cityList(data.urtrack, data.urcity).map(function (x) { return { value: x.c, label: x.c + (x.n ? ' (' + x.n + ')' : '') }; }); } },
      { id: 'units', label: 'דירות בבניין', type: 'number', unit: 'דירות', showIf: function (v) { return v.view === 'track'; } },
      { id: 'permit', label: 'מתי ניתן היתר הבנייה של הבניין', type: 'segmented', showIf: function (v) { return v.view === 'track'; }, options: [{ value: 'pre80', label: 'לפני 1980' }, { value: '80to84', label: '1980 עד 1984' }, { value: 'post84', label: 'אחרי 1984' }] },
      { id: 'complex', label: 'הבניין בתוך מתחם התחדשות עירונית?', type: 'segmented', showIf: function (v) { return v.view === 'track'; }, options: [{ value: 'yes', label: 'כן' }, { value: 'no', label: 'לא' }, { value: 'unk', label: 'לא יודעים' }] }
    ],
    compute: function (v, data) {
      var U = data.urcity, T = data.urtrack;
      if (!U || !U.tracks || !T || !T.recs) return { error: { field: null, msg: 'הנתונים לא נטענו.' } };
      return v.view === 'rank' ? viewRank(v, U, T) : v.view === 'track' ? viewTrack(v, U, T) : viewCity(v, U, T);
    }
  });
})();
