/* NadLan Instruments · bedek v1 (G6 moat, HAD-601 round 2, 26.10.2026): "בדק בית" on /home-inspection/.
   Three views on one set of answers:
   - defect   · הליקוי שלי: for one defect type and the day the apartment was handed to the first buyer, where the defect stands under
                the Sale (Apartments) Law: inside the inspection period (the seller answers unless he proves the buyer caused it, s.4(א)(2)),
                inside the 3-year warranty (the buyer must show the cause is in planning, work or materials, s.4(א)(3)), or over; the
                20 years of a fundamental structural defect (s.4(א)(4)-(5)); the one-year notice for a defect visible at handover
                (s.4א(א)(1)); the repair rule (s.4ב: a fair chance to repair; a defect back within 2 years of the notice, or an urgent one
                not repaired in reasonable time, may be repaired at the seller's cost); a sub-buyer (קונה משנה) keeps the same periods.
   - calendar · לוח הבדיקות: every end of an inspection period from the handover day (1, 2, 3, 4, 5, 7 years), the warranty ends,
                the 20 years, and a suggested day to book an inspector before each end (45 days, our suggestion, said so).
   - cost     · כמה זה עולה: the published price ranges by property type (Midrag 2025, incl. VAT; bedek-mivnim 1.2026 and
                ha-bodkim 6.2026, VAT not stated), shown source by source, with the envelope as the answer; shared property from
                Midrag's per-apartment price with its minimum; group and roof add-ons from Midrag 2022 (dated as such).
   Data: data/bedek.json (tools/instruments/build_pros_data.py; the schedule is checked against warranty.js and the law text).
   Pure logic in NLBD for unit checks. Honesty: no promised outcome, no invented price, every range with its source and date. */
(function () {
  'use strict';
  var STRUCT = 'struct';
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function addY(iso, y) { var p = iso.split('-').map(Number); var d = new Date(Date.UTC(p[0] + y, p[1] - 1, p[2])); if (d.getUTCMonth() !== p[1] - 1) d = new Date(Date.UTC(p[0] + y, p[1], 0)); return d.toISOString().slice(0, 10); }
  function addD(iso, n) { var p = iso.split('-').map(Number); return new Date(Date.UTC(p[0], p[1] - 1, p[2] + n)).toISOString().slice(0, 10); }
  function days(a, b) { return Math.round((Date.parse(b) - Date.parse(a)) / 864e5); }
  function dd(iso) { var p = String(iso).split('-'); return (+p[2]) + '.' + (+p[1]) + '.' + p[0]; }
  function n0(x) { return String(Math.round(x || 0)).replace(/\B(?=(\d{3})+(?!\d))/g, ','); }
  function ils(x) { return '₪' + n0(x); }

  /** One defect: the periods from the handover day and where `asof` falls. L = data.law */
  function defect(handed, itemId, asof, L) {
    if (itemId === STRUCT) {
      var e = addY(handed, L.struct_y);
      return { id: STRUCT, years: L.struct_y, bdekEnd: e, warEnd: e, st: asof <= e ? 'bdek' : 'struct_after', left: asof <= e ? days(asof, e) : 0 };
    }
    var it = L.items.filter(function (x) { return x.id === itemId; })[0];
    if (!it) return null;
    var be = addY(handed, it.y), we = addY(be, L.warranty_y);
    var st = asof <= be ? 'bdek' : asof <= we ? 'warranty' : 'over';
    return { id: it.id, short: it.short, law: it.law, years: it.y, bdekEnd: be, warEnd: we, st: st, left: st === 'bdek' ? days(asof, be) : st === 'warranty' ? days(asof, we) : 0 };
  }

  /** Every date that matters from the handover day, in order. */
  function calendar(handed, L, bookDays) {
    var ev = [], ys = {};
    L.items.forEach(function (it) { (ys[it.y] = ys[it.y] || []).push(it); });
    Object.keys(ys).map(Number).sort(function (a, b) { return a - b; }).forEach(function (y) {
      var end = addY(handed, y), names = ys[y].map(function (x) { return x.short; });
      ev.push({ kind: 'bdek', date: end, book: addD(end, -bookDays), years: y, items: names });
      ev.push({ kind: 'war', date: addY(end, L.warranty_y), years: y + L.warranty_y, items: names });
    });
    ev.push({ kind: 'notice', date: addY(handed, L.visible_notice_y), years: L.visible_notice_y, items: [] });
    ev.push({ kind: 'struct', date: addY(handed, L.struct_y), years: L.struct_y, items: [] });
    ev.sort(function (a, b) { return a.date < b.date ? -1 : a.date > b.date ? 1 : (a.kind === 'notice' ? -1 : 1); });
    return ev;
  }

  /** Published ranges for a property: [{src, date, vat, label, lo, hi}], envelope lo..hi */
  function priceRows(P, kind, rooms) {
    var out = [];
    P.forEach(function (s) {
      s.rows.forEach(function (r) {
        if (r[0] !== kind) return;
        if (r[4] && !(rooms >= r[4][0] && rooms <= r[4][1])) return;
        out.push({ src: s.src, date: s.date, vat: s.vat, label: r[1], lo: r[2], hi: r[3] });
      });
    });
    var lo = Math.min.apply(null, out.map(function (r) { return r.lo; })), hi = Math.max.apply(null, out.map(function (r) { return r.hi; }));
    return { rows: out, lo: out.length ? lo : 0, hi: out.length ? hi : 0 };
  }
  function shared(S, apts, vat) { var net = Math.max(S.min, S.per_apt * apts); return { net: net, gross: net * (1 + vat), per: net * (1 + vat) / Math.max(1, apts) }; }

  window.NLBD = { defect: defect, calendar: calendar, priceRows: priceRows, shared: shared, addY: addY, addD: addD, days: days };
  if (!window.NadLanInstruments) return;
  var NI = window.NadLanInstruments, F = NI.fmt, esc = NI.esc;

  function src(D, keys) { return keys.map(function (k) { return D.sources[k]; }).filter(Boolean); }
  function vatTxt(v) { return v === 'incl' ? 'כולל מע״מ' : v === 'plus' ? 'ועוד מע״מ' : 'מע״מ לא צוין'; }
  function today() { return new Date().toISOString().slice(0, 10); }

  // ------------------------------------------------------------------ drawings (RTL: text-anchor start = the right end)
  function svgDefect(handed, r, asof, visible) {
    var total = Math.max(days(handed, r.warEnd), days(handed, asof)) || 1, XR = 400, XL = 20, y0 = 74, g = [];
    var x = function (iso) { return XR - (XR - XL) * Math.max(0, Math.min(1, days(handed, iso) / total)); };
    g.push('<text x="410" y="24" text-anchor="start" style="font-size:17px;font-weight:600;fill:#12202A">' + esc(r.id === STRUCT ? 'ליקוי בשלד: 20 שנה מהמסירה' : 'בדק ' + (r.years === 1 ? 'שנה' : r.years + ' שנים') + ' ועוד 3 שנות אחריות') + '</text>');
    g.push('<rect x="' + x(r.bdekEnd) + '" y="' + (y0 - 10) + '" width="' + (XR - x(r.bdekEnd)) + '" height="20" fill="#1F4B5C"/>');
    if (r.id !== STRUCT) g.push('<rect x="' + x(r.warEnd) + '" y="' + (y0 - 10) + '" width="' + (x(r.bdekEnd) - x(r.warEnd)) + '" height="20" fill="#2F6F86" fill-opacity=".45"/>');
    g.push('<text x="' + ((XR + x(r.bdekEnd)) / 2) + '" y="' + (y0 + 5) + '" text-anchor="middle" style="font-size:13px;fill:#fff;font-weight:600">' + esc('בדק') + '</text>');
    if (r.id !== STRUCT && x(r.bdekEnd) - x(r.warEnd) > 50) g.push('<text x="' + ((x(r.bdekEnd) + x(r.warEnd)) / 2) + '" y="' + (y0 + 5) + '" text-anchor="middle" style="font-size:13px;fill:#12202A;font-weight:600">' + esc('אחריות') + '</text>');
    if (visible === 'yes') { var nx = x(addY(handed, 1)), nl = 'הודעה עד ' + dd(addY(handed, 1)), nw = nl.length * 6.4; g.push('<line x1="' + nx + '" y1="' + (y0 - 22) + '" x2="' + nx + '" y2="' + (y0 + 14) + '" stroke="#C42550" stroke-width="2"/><text x="' + Math.max(nw / 2 + 4, Math.min(nx, 414 - nw / 2)) + '" y="' + (y0 - 26) + '" text-anchor="middle" style="font-size:12px;fill:#C42550">' + esc(nl) + '</text>'); }
    var tx = x(asof), late = r.st === 'over' || r.st === 'struct_after', tl = ('היום ' + dd(asof)).length * 6.8, tcx = Math.max(tl / 2 + 4, Math.min(tx, 414 - tl / 2));
    g.push('<line x1="' + tx + '" y1="' + (y0 - 18) + '" x2="' + tx + '" y2="' + (y0 + 22) + '" stroke="' + (late ? '#C42550' : '#12202A') + '" stroke-width="2.4"/>');
    g.push('<text x="' + tcx + '" y="' + (y0 + 38) + '" text-anchor="middle" style="font-size:13px;font-weight:600;fill:' + (late ? '#C42550' : '#12202A') + '">' + esc('היום ' + dd(asof)) + '</text>');
    g.push('<text x="410" y="' + (y0 + 58) + '" text-anchor="start" style="font-size:12px;fill:#3E4C58">' + esc('מסירה ' + dd(handed)) + '</text>');
    g.push('<text x="' + XL + '" y="' + (y0 + 58) + '" text-anchor="start" direction="ltr" style="font-size:12px;fill:#3E4C58">' + esc(dd(r.warEnd)) + '</text>');
    return '<svg direction="rtl" viewBox="0 0 420 ' + (y0 + 70) + '" role="img" aria-label="' + esc('ציר הזמן של הליקוי: בדק עד ' + dd(r.bdekEnd) + (r.id !== STRUCT ? ', אחריות עד ' + dd(r.warEnd) : '') + ', היום ' + dd(asof)) + '" style="display:block;width:100%;height:auto;background:#fff">' + g.join('') + '</svg>';
  }

  function svgCalendar(handed, ev, asof) {
    var span = 10, XR = 400, XL = 24, y0 = 70, g = [];
    var x = function (iso) { return XR - (XR - XL) * Math.max(0, Math.min(1, days(handed, iso) / (365.25 * span))); };
    g.push('<text x="410" y="24" text-anchor="start" style="font-size:17px;font-weight:600;fill:#12202A">' + esc('10 השנים הראשונות מהמסירה') + '</text>');
    g.push('<line x1="' + XL + '" y1="' + y0 + '" x2="' + XR + '" y2="' + y0 + '" stroke="#12202A" stroke-width="2"/>');
    for (var yy = 0; yy <= span; yy++) { var tx = x(addY(handed, yy)); g.push('<line x1="' + tx + '" y1="' + (y0 - 4) + '" x2="' + tx + '" y2="' + (y0 + 4) + '" stroke="#12202A"/>'); if (yy % 2 === 0) g.push('<text x="' + tx + '" y="' + (y0 + 20) + '" text-anchor="middle" style="font-size:12px;fill:#3E4C58;font-family:IBM Plex Mono,monospace">' + yy + '</text>'); }
    ev.forEach(function (e) {
      if (e.kind !== 'bdek' && e.kind !== 'war') return;
      var ex = x(e.date), up = e.kind === 'bdek';
      g.push('<circle cx="' + ex + '" cy="' + y0 + '" r="6" fill="' + (up ? '#1F4B5C' : '#fff') + '" stroke="#1F4B5C" stroke-width="2"/>');
      if (up) g.push('<text x="' + ex + '" y="' + (y0 - 14) + '" text-anchor="middle" style="font-size:12px;fill:#1F4B5C;font-weight:600">' + esc(e.years === 1 ? 'שנה' : e.years) + '</text>');
    });
    var t = x(asof); g.push('<line x1="' + t + '" y1="' + (y0 - 30) + '" x2="' + t + '" y2="' + (y0 + 30) + '" stroke="#C42550" stroke-width="2"/><text x="' + t + '" y="' + (y0 + 46) + '" text-anchor="middle" style="font-size:13px;fill:#C42550;font-weight:600">' + esc('היום') + '</text>');
    g.push('<text x="410" y="' + (y0 + 68) + '" text-anchor="start" style="font-size:12px;fill:#3E4C58">' + esc('עיגול מלא: סוף תקופת בדק. עיגול ריק: סוף 3 שנות האחריות שאחריה.') + '</text>');
    return '<svg direction="rtl" viewBox="0 0 420 ' + (y0 + 80) + '" role="img" aria-label="' + esc('לוח התקופות מהמסירה ב-' + dd(handed) + ': סופי תקופות הבדק אחרי שנה, 2, 3, 4, 5 ו-7 שנים, והאחריות 3 שנים אחרי כל אחת') + '" style="display:block;width:100%;height:auto;background:#fff">' + g.join('') + '</svg>';
  }

  function svgRange(rows, lo, hi) {
    var XR = 400, XL = 30, top = 44, rh = 34, H = top + rows.length * rh + 30, g = [], max = hi * 1.08;
    var x = function (v) { return XR - (XR - XL) * v / max; };
    g.push('<text x="410" y="22" text-anchor="start" style="font-size:16px;font-weight:600;fill:#12202A">' + esc('הטווחים שפורסמו, מקור אחר מקור') + '</text>');
    rows.forEach(function (r, i) {
      var y = top + i * rh;
      g.push('<text x="410" y="' + (y + 12) + '" text-anchor="start" style="font-size:12px;fill:#3E4C58">' + esc(r.name + ' · ' + vatTxt(r.vat)) + '</text>');
      if (r.hi > r.lo) g.push('<rect x="' + x(r.hi) + '" y="' + (y + 17) + '" width="' + (x(r.lo) - x(r.hi)) + '" height="10" fill="' + (r.vat === 'incl' ? '#1F4B5C' : '#2F6F86') + '"/>');
      else g.push('<circle cx="' + x(r.lo) + '" cy="' + (y + 22) + '" r="6" fill="#2F6F86"/>');
      var lab = r.hi > r.lo ? n0(r.lo) + '-' + n0(r.hi) : n0(r.lo), lw = lab.length * 7.4;
      if (x(r.hi) - 6 - lw >= 4) g.push('<text x="' + (x(r.hi) - 6) + '" y="' + (y + 27) + '" text-anchor="start" style="font-size:12px;fill:#12202A;font-family:IBM Plex Mono,monospace">' + esc(lab) + '</text>');
      else g.push('<text x="' + Math.min(404 - lw, x(r.lo) + 6) + '" y="' + (y + 27) + '" text-anchor="end" style="font-size:12px;fill:#12202A;font-family:IBM Plex Mono,monospace">' + esc(lab) + '</text>');
    });
    g.push('<line x1="' + x(lo) + '" y1="' + (top - 6) + '" x2="' + x(lo) + '" y2="' + (H - 22) + '" stroke="#12202A" stroke-dasharray="4 3"/><line x1="' + x(hi) + '" y1="' + (top - 6) + '" x2="' + x(hi) + '" y2="' + (H - 22) + '" stroke="#12202A" stroke-dasharray="4 3"/>');
    g.push('<text x="410" y="' + (H - 6) + '" text-anchor="start" style="font-size:12px;fill:#3E4C58">' + esc('הקווים המקווקווים: הנמוך והגבוה מבין המקורות, בשקלים') + '</text>');
    return '<svg direction="rtl" viewBox="0 0 420 ' + H + '" role="img" aria-label="' + esc('טווחי המחירים שפורסמו: מ-' + n0(lo) + ' עד ' + n0(hi) + ' שקלים') + '" style="display:block;width:100%;height:auto;background:#fff">' + g.join('') + '</svg>';
  }

  // ------------------------------------------------------------------ views
  function viewDefect(v, D) {
    var L = D.law, asof = v.asof || today();
    if (!/^\d{4}-\d{2}-\d{2}$/.test(v.handed || '')) return { error: { field: 'handed', msg: 'בחרו את תאריך מסירת הדירה.' } };
    if (!/^\d{4}-\d{2}-\d{2}$/.test(asof) || asof < v.handed) return { error: { field: 'asof', msg: 'התאריך צריך להיות אחרי המסירה.' } };
    var r = defect(v.handed, v.item, asof, L); if (!r) return { error: { field: 'item', msg: 'בחרו את סוג הליקוי.' } };
    var label = r.id === STRUCT ? 'כשל בשלד ויציבות הבניין' : r.short, lines = [], notes = [];
    var notice = addY(v.handed, L.visible_notice_y), lateNotice = v.visible === 'yes' && asof > notice;
    var answer;
    if (r.st === 'bdek') answer = { label: label + ': איפה זה עומד', value: r.id === STRUCT ? 'בתוך 20 השנים' : 'בתקופת הבדק', tone: lateNotice ? 'survey' : 'ink', sub: esc((r.id === STRUCT ? 'עד ' + dd(r.bdekEnd) : 'הבדק עד ' + dd(r.bdekEnd) + ', ועוד 3 שנות אחריות עד ' + dd(r.warEnd)) + ' (' + F.num(r.left) + ' ימים). הקבלן אחראי, אלא אם יוכיח שהליקוי נגרם בגללכם.') };
    else if (r.st === 'warranty') answer = { label: label + ': איפה זה עומד', value: 'בתקופת האחריות', tone: r.left < 120 ? 'survey' : 'ink', sub: esc('הבדק הסתיים ב-' + dd(r.bdekEnd) + '. עד ' + dd(r.warEnd) + ' (' + F.num(r.left) + ' ימים) הקבלן עדיין אחראי, אבל עליכם להראות שמקור הליקוי בתכנון, בעבודה או בחומרים.') };
    else if (r.st === 'over') answer = { label: label + ': איפה זה עומד', value: 'התקופות הסתיימו', tone: 'survey', sub: esc('הבדק הסתיים ב-' + dd(r.bdekEnd) + ' והאחריות ב-' + dd(r.warEnd) + '. כדאי לבדוק עם עורך דין אם הליקוי נובע מאי התאמה למפרט, לתקן או לתקנות הבנייה (סעיף 4(א)(1)), ומה דין ההתיישנות.') };
    else answer = { label: label + ': איפה זה עומד', value: 'אחרי 20 השנים', tone: 'survey', sub: esc('גם אחרי 20 שנה אפשר לטעון לאי התאמה יסודית, אם תוכיחו שמקורה בתכנון, בעבודה או בחומרים (סעיף 4(א)(5)).') };
    lines.push({ label: 'מסירה לקונה הראשון', value: dd(v.handed) });
    if (r.id !== STRUCT) { lines.push({ label: 'תקופת הבדק לפי התוספת', value: r.years === 1 ? 'שנה' : r.years + ' שנים' }); lines.push({ label: 'הבדק עד', value: dd(r.bdekEnd) }); lines.push({ label: 'האחריות עד', value: dd(r.warEnd) }); }
    else lines.push({ label: 'ליקוי יסודי: 20 שנה מהמסירה', value: 'עד ' + dd(r.bdekEnd) });
    lines.push({ label: 'נטל ההוכחה היום', value: r.st === 'bdek' ? 'על הקבלן' : 'עליכם' });
    lines.push({ label: v.visible === 'yes' ? 'הודעה על ליקוי שנראה במסירה' : 'הודעה על ליקוי שהתגלה אחר כך', value: v.visible === 'yes' ? 'עד ' + dd(notice) + (lateNotice ? ' (עבר)' : '') : 'תוך זמן סביר מהגילוי' });
    if (r.st === 'bdek' && r.left > 45) lines.push({ label: 'מועד מומלץ להזמין בדיקה (45 יום לפני סוף הבדק, הצעה שלנו)', value: dd(addD(r.bdekEnd, -45)) });
    if (v.who === 'sub') notes.push(esc('קניתם מקונה קודם: החוק נותן גם לקונה משנה את אותן תקופות, והן נספרות מהיום שבו הדירה נמסרה לקונה הראשון. כלפי המוכר הפרטי חל החוזה שלכם איתו, ולא חוק המכר (דירות).'));
    if (lateNotice) notes.push(esc('ליקוי שאפשר היה לראות ביום המסירה: החוק מאפשר להסתמך עליו אם הודעתם לקבלן בתוך שנה מהמסירה (סעיף 4א(א)(1)). אם הודעתם בזמן, שמרו את ההודעה ואת האישור על קבלתה.'));
    notes.push(esc('מה עושים: מודיעים לקבלן בכתב (דואר רשום או דואר אלקטרוני עם אישור קבלה), עם תמונות ודוח בדק בית. הקבלן חייב לתקן בתוך זמן סביר וצריך לתת לו הזדמנות נאותה לתקן. ליקוי שחזר אחרי תיקון בתוך שנתיים מההודעה, או ליקוי דחוף שלא תוקן בזמן סביר: מותר לתקן בעצמכם על חשבון הקבלן (סעיף 4ב).'));
    var all = L.items.map(function (it) { return defect(v.handed, it.id, asof, L); });
    var table = { title: 'כל סוגי הליקויים בדירה הזאת, לפי התוספת לחוק', head: ['סוג הליקוי', 'בדק', 'המצב ב-' + dd(asof), 'הבדק עד', 'האחריות עד'], num: [3, 4], phoneHide: [3, 4],
      rows: all.map(function (x) { return [x.short, x.years === 1 ? 'שנה' : x.years + ' שנים', x.st === 'bdek' ? 'בבדק · ' + F.num(x.left) + ' ימים' : x.st === 'warranty' ? 'באחריות · ' + F.num(x.left) + ' ימים' : 'הסתיים', dd(x.bdekEnd), dd(x.warEnd)]; })
        .concat([['ליקוי יסודי בשלד', '20 שנה', asof <= addY(v.handed, 20) ? 'בתוקף' : 'הסתיים', dd(addY(v.handed, 20)), '']]) };
    return { answer: answer, figure: svgDefect(v.handed, r, asof, v.visible), lines: lines, note: notes.join('<br>'), table: table,
      formula: 'חוק המכר (דירות): תקופת בדק לפי התוספת מיום העמדת הדירה לרשות הקונה; תקופת אחריות 3 שנים מתום תקופת הבדק; אי התאמה יסודית 20 שנה; הודעה על ליקוי שאפשר היה לגלות במסירה בתוך שנה, ועל ליקוי אחר תוך זמן סביר מהגילוי.',
      sources: src(D, ['SALE']), text: 'בדק בית, ' + label + ': דירה שנמסרה ב-' + dd(v.handed) + '. ' + (r.st === 'bdek' ? 'בתקופת הבדק עד ' + dd(r.bdekEnd) : r.st === 'warranty' ? 'בתקופת האחריות עד ' + dd(r.warEnd) : 'התקופות הסתיימו') + '.' };
  }

  function viewCalendar(v, D) {
    var L = D.law, asof = v.asof || today();
    if (!/^\d{4}-\d{2}-\d{2}$/.test(v.handed || '')) return { error: { field: 'handed', msg: 'בחרו את תאריך מסירת הדירה.' } };
    var ev = calendar(v.handed, L, D.book_days), next = ev.filter(function (e) { return e.date >= asof && e.kind !== 'notice'; })[0], nb = ev.filter(function (e) { return e.kind === 'bdek' && e.date >= asof; })[0];
    var answer = nb ? { label: 'הבדיקה הבאה, לפני סוף הבדק של ' + nb.items.join(', '), value: dd(nb.book <= asof ? asof : nb.book), sub: esc('הבדק מסתיים ב-' + dd(nb.date) + ' (' + F.num(days(asof, nb.date)) + ' ימים). אחר כך הקבלן עדיין אחראי 3 שנים, אבל נטל ההוכחה עובר אליכם.') }
      : { label: 'כל תקופות הבדק הסתיימו', value: next ? 'אחריות עד ' + dd(next.date) : 'הסתיים', tone: 'survey', sub: esc(next ? 'עדיין בתוקף: ' + (next.kind === 'struct' ? 'ליקוי יסודי בשלד' : 'אחריות ל' + next.items.join(', ')) + '.' : 'נשארה רק אחריות לליקוי יסודי, אם תוכיחו שמקורו בתכנון, בעבודה או בחומרים.') };
    var lines = ev.filter(function (e) { return e.date >= asof; }).slice(0, 4).map(function (e) {
      return { label: e.kind === 'bdek' ? 'סוף הבדק: ' + e.items.join(', ') : e.kind === 'war' ? 'סוף האחריות: ' + e.items.join(', ') : e.kind === 'notice' ? 'הודעה על ליקוי שנראה כבר במסירה' : 'ליקוי יסודי בשלד: 20 שנה', value: dd(e.date) };
    });
    var table = { title: 'לוח התאריכים מהמסירה ב-' + dd(v.handed), head: ['תאריך', 'מה מסתיים', 'מה עושים', 'מצב'], num: [0],
      rows: ev.map(function (e) {
        var what = e.kind === 'bdek' ? 'סוף תקופת הבדק (' + (e.years === 1 ? 'שנה' : e.years + ' שנים') + '): ' + e.items.join(', ') : e.kind === 'war' ? 'סוף 3 שנות האחריות: ' + e.items.join(', ') : e.kind === 'notice' ? 'שנה מהמסירה: הודעה על ליקוי שאפשר היה לראות במסירה' : '20 שנה: ליקוי יסודי בשלד';
        var todo = e.kind === 'bdek' ? 'בדק בית עד ' + dd(e.book) + ', מכתב לקבלן לפני ' + dd(e.date) : e.kind === 'war' ? 'ליקוי שהתגלה: מכתב לקבלן עם חוות דעת על מקור הליקוי' : e.kind === 'notice' ? 'מכתב לקבלן על כל מה שנרשם בפרוטוקול ולא תוקן' : 'בדיקת מהנדס קונסטרוקציה בכל סימן לכשל';
        return [dd(e.date), what, todo, e.date < asof ? 'עבר' : 'בעוד ' + F.num(days(asof, e.date)) + ' ימים'];
      }) };
    return { answer: answer, figure: svgCalendar(v.handed, ev, asof), lines: lines, table: table,
      note: esc('ההמלצה להזמין בדיקה 45 יום לפני סוף כל תקופה היא שלנו: כדי שיהיה זמן לקבל דוח ולשלוח מכתב לקבלן לפני התאריך. המועדים עצמם לפי התוספת לחוק המכר (דירות).'),
      formula: 'תקופת בדק מהמסירה: שנה לכל ליקוי שאינו ברשימה; שנתיים למסגרות ונגרות ולריצוף וחיפוי פנים; 3 שנים למכונות ודוודים, לפיתוח החצר ולבידוד תרמי; 4 שנים לצנרת ולאיטום; 5 שנים לסדקים מעל 1.5 מ״מ ברכיבים לא נושאים; 7 שנים לחיפויי חוץ. אחריות: 3 שנים מתום כל תקופת בדק.',
      sources: src(D, ['SALE']), text: 'לוח הבדק והאחריות לדירה שנמסרה ב-' + dd(v.handed) + (nb ? ': הבדיקה הבאה עד ' + dd(nb.book) + ', לפני סוף הבדק של ' + nb.items.join(', ') + ' ב-' + dd(nb.date) + '.' : '.') };
  }

  var KINDS = { apt: 'דירה בבניין', roof: 'פנטהאוז או דירה בשתי קומות', house: 'בית פרטי עד 200 מ״ר', villa: 'בית פרטי גדול או וילה', shared: 'רכוש משותף של בניין', moist: 'רטיבות ותרמוגרפיה בלבד', court: 'חוות דעת לבית משפט' };
  function viewCost(v, D) {
    var P = D.prices, kind = v.ptype, rooms = Math.round(+v.rooms || 0), lines = [], notes = [];
    if (kind === 'shared') {
      var apts = Math.round(+v.apts || 0); if (!(apts >= 2 && apts <= 400)) return { error: { field: 'apts', msg: 'מספר הדירות בבניין: 2 עד 400.' } };
      var s = shared(D.shared, apts, D.vat), MT = D.sources[D.shared.src];
      lines.push({ label: 'לדירה, לפי מידרג (' + dd(D.shared.date) + ')', value: ils(D.shared.per_apt) + ' ועוד מע״מ' });
      lines.push({ label: 'מינימום לבניין', value: ils(D.shared.min) + ' ועוד מע״מ' });
      lines.push({ label: 'לבניין לפני מע״מ', value: ils(s.net) });
      lines.push({ label: 'לכל דירה כולל מע״מ 18%', value: ils(s.per) });
      return { answer: { label: 'בדיקת רכוש משותף ל-' + apts + ' דירות', value: n0(s.gross) + ' ₪', sub: esc('כולל מע״מ 18%: ' + ils(s.net) + ' לפני מע״מ. בבניין של פחות מ-17 דירות המינימום מייקר את החלק של כל דירה.') },
        lines: lines, note: esc('המחיר הוא מה שפרסם מידרג לחוות דעת על הרכוש המשותף. הזמנה דרך נציגות הבית, עם כל הדירות, מורידה את המחיר לדירה.'), formula: 'הגבוה מבין 180 ₪ לדירה ו-3,000 ₪ לבניין, ועוד מע״מ 18%.', sources: [MT],
        text: 'בדק בית לרכוש משותף, ' + apts + ' דירות: ' + ils(s.gross) + ' כולל מע״מ (מידרג, ' + dd(D.shared.date) + ').' };
    }
    if (kind === 'apt' && !(rooms >= 2 && rooms <= 9)) return { error: { field: 'rooms', msg: 'מספר החדרים: 2 עד 9.' } };
    var pr = priceRows(P, kind, kind === 'apt' ? rooms : 0);
    if (!pr.rows.length) return { error: { field: 'ptype', msg: 'אין מחיר שפורסם לסוג הזה.' } };
    var lo = pr.lo, hi = pr.hi, rows = pr.rows.map(function (r) { return { name: D.sources[r.src].label.split(',')[0] + ' ' + r.date.slice(0, 4), vat: r.vat, lo: r.lo, hi: r.hi }; });
    pr.rows.forEach(function (r) { lines.push({ label: D.sources[r.src].label.split(' (')[0] + ': ' + r.label + ' · ' + vatTxt(r.vat), value: r.hi > r.lo ? ils(r.lo) + ' עד ' + ils(r.hi) : ils(r.lo) }); });
    var extra = 0;
    if (kind === 'apt' && v.roof === 'yes') { var a = D.addon_roof; lines.push({ label: 'תוספת לבדיקת גג או גינה בדירה (מידרג, ' + dd(a.date) + ')', value: ils(a.lo) + ' עד ' + ils(a.hi) }); lo += a.lo; hi += a.hi; extra = 1; }
    var grp = Math.round(+v.group || 1);
    if (kind === 'apt' && grp >= D.group.from_apts) { lines.push({ label: grp + ' דירות מזמינות יחד: מחיר לדירה (מידרג, ' + dd(D.group.date) + ')', value: ils(D.group.lo) + ' עד ' + ils(D.group.hi) }); notes.push(esc('קבוצה: מידרג פרסם ב-2022 מחיר של כ-1,000 עד 1,200 ₪ לדירה כשעשר דירות ומעלה מזמינות יחד, והבודקים מציעים עד 15% הנחה לקבוצות רוכשים.')); }
    else if (kind === 'apt' && grp >= 2) notes.push(esc('כמה דירות יחד: הבודקים מציעים עד 15% הנחה לקבוצות רוכשים; מידרג פרסם מחיר לדירה בקבוצה של עשר דירות ומעלה.'));
    var anyIncl = pr.rows.some(function (r) { return r.vat === 'incl'; }), anyNs = pr.rows.some(function (r) { return r.vat === 'ns'; });
    var answer = { label: 'בדק בית ל' + (kind === 'apt' ? 'דירת ' + rooms + ' חדרים' : KINDS[kind]) + (extra ? ' עם גג או גינה' : '') + ', בשקלים', value: lo === hi ? n0(lo) + ' ₪' : n0(lo) + '-' + n0(hi),
      sub: esc('הנמוך והגבוה מבין ' + pr.rows.length + ' מחירים שפורסמו' + (anyIncl ? '; במידרג כולל מע״מ' : '') + (anyNs ? '; אצל השאר מע״מ לא צוין' : '') + '. זה טווח שפורסם, לא הצעת מחיר.') };
    notes.unshift(esc('לפני שמזמינים, שאלו: מי הבודק שמגיע בפועל ואם הוא רשום בפנקס המהנדסים והאדריכלים; האם מצלמה תרמית ובדיקת לחץ מים כלולות; האם המחיר סופי וכולל מע״מ; תוך כמה ימים מגיע הדוח; האם הדוח חתום וכולל אומדן עלות לתיקון; והאם בדיקה חוזרת אחרי התיקונים כלולה.'));
    if (kind === 'roof') notes.push(esc('לפנטהאוז ולדירה בשתי קומות מצאנו מקור אחד שפרסם מחיר; הגג והמרפסות הגדולות מוסיפים זמן בדיקה.'));
    var table = { title: 'כל המחירים שפורסמו לסוג הזה', head: ['מקור', 'מה כלול', 'מחיר', 'מע״מ', 'פורסם'], num: [2],
      rows: pr.rows.map(function (r) { return [D.sources[r.src].label.split(' (')[0].split(',')[0], r.label, r.hi > r.lo ? n0(r.lo) + ' עד ' + n0(r.hi) + ' ₪' : n0(r.lo) + ' ₪', vatTxt(r.vat), dd(r.date)]; }) };
    return { answer: answer, figure: svgRange(rows, pr.lo, pr.hi), lines: lines, note: notes.join('<br>'), table: table,
      formula: 'הטווח: המחיר הנמוך והגבוה מבין המחירים שפורסמו לאותו סוג נכס ב-2025 וב-2026, כפי שפורסמו. תוספת גג או גינה וקבוצות לפי מידרג 2022, מסומנות בשנה.',
      sources: src(D, pr.rows.map(function (r) { return r.src; }).filter(function (k, i, a) { return a.indexOf(k) === i; }).concat(extra || grp >= D.group.from_apts ? ['MP22'] : []).concat(['ENG'])),
      text: 'בדק בית ל' + (kind === 'apt' ? 'דירת ' + rooms + ' חדרים' : KINDS[kind]) + ': ' + ils(lo) + ' עד ' + ils(hi) + ' לפי ' + pr.rows.length + ' מחירים שפורסמו (מידרג כולל מע״מ; בשאר לא צוין).' };
  }

  NI.register('bedek', {
    kicker: 'מחשבון · בדק בית',
    title: 'בדק בית: עד מתי הקבלן אחראי, מתי לבדוק וכמה זה עולה',
    lede: 'בוחרים את סוג הליקוי ואת יום המסירה, ורואים אם אתם בתקופת הבדק, בתקופת האחריות או אחריה, מי צריך להוכיח מה, ועד מתי להודיע לקבלן. בלוח הבדיקות רואים מתי כל תקופה נגמרת ומתי להזמין בודק, ובמחירון את כל המחירים שפורסמו לבדק בית, מקור אחר מקור.',
    strip: function () { return [{ label: 'סוגי ליקויים בתוספת לחוק', value: '10' }, { label: 'תקופת בדק', value: 'שנה עד 7 שנים' }, { label: 'אחריות אחרי כל תקופה', value: '3 שנים' }, { label: 'ליקוי יסודי בשלד', value: '20 שנה' }]; },
    presets: function () {
      return [{ key: 'leak', label: 'רטיבות בקיר', sub: 'דירה שנמסרה במרץ 2023', set: { view: 'defect', handed: '2023-03-15', item: 'sealing', visible: 'no', who: 'first' } },
        { key: 'cal', label: 'לוח הבדיקות', sub: 'דירה שנמסרה ביוני 2025', set: { view: 'calendar', handed: '2025-06-30' } },
        { key: 'apt4', label: 'בדק בית לדירת 4 חדרים', sub: 'כל המחירים שפורסמו', set: { view: 'cost', ptype: 'apt', rooms: 4, roof: 'no', group: 1 } },
        { key: 'house', label: 'בית פרטי', sub: 'עד 200 מ״ר', set: { view: 'cost', ptype: 'house' } },
        { key: 'sub', label: 'קונים דירה בת 3 שנים', sub: 'נזילה בצנרת, קונה משנה', set: { view: 'defect', handed: '2023-09-01', item: 'piping', visible: 'no', who: 'sub' } }];
    },
    defaults: function () { return { view: 'defect', handed: '2023-03-15', item: 'sealing', visible: 'no', who: 'first', asof: today(), ptype: 'apt', rooms: 4, roof: 'no', group: 1, apts: 24 }; },
    fields: [
      { id: 'view', label: 'מה לבדוק', type: 'segmented', options: [{ value: 'defect', label: 'הליקוי שלי' }, { value: 'calendar', label: 'לוח הבדיקות' }, { value: 'cost', label: 'כמה זה עולה' }] },
      { id: 'handed', label: 'תאריך מסירת הדירה לקונה הראשון', type: 'date', showIf: function (v) { return v.view !== 'cost'; } },
      { id: 'who', label: 'ממי קניתם', type: 'segmented', showIf: function (v) { return v.view === 'defect'; }, options: [{ value: 'first', label: 'מהקבלן' }, { value: 'sub', label: 'יד שנייה, מקונה קודם' }] },
      { id: 'item', label: 'סוג הליקוי', type: 'select', showIf: function (v) { return v.view === 'defect'; }, optionsFrom: function (v, data) { return data.bedek.law.items.map(function (x) { return { value: x.id, label: x.short + ' (' + (x.y === 1 ? 'שנה' : x.y + ' שנים') + ')' }; }).concat([{ value: STRUCT, label: 'סדק או כשל בשלד: עמודים, קורות, יסודות (20 שנה)' }]); } },
      { id: 'visible', label: 'אפשר היה לראות את הליקוי ביום המסירה?', type: 'segmented', showIf: function (v) { return v.view === 'defect'; }, options: [{ value: 'no', label: 'התגלה אחר כך' }, { value: 'yes', label: 'נראה כבר במסירה' }] },
      { id: 'asof', label: 'נכון לתאריך', type: 'date', help: 'בדרך כלל היום.', showIf: function (v) { return v.view !== 'cost'; } },
      { id: 'ptype', label: 'סוג הנכס או הבדיקה', type: 'select', showIf: function (v) { return v.view === 'cost'; }, options: Object.keys(KINDS).map(function (k) { return { value: k, label: KINDS[k] }; }) },
      { id: 'rooms', label: 'מספר חדרים', type: 'number', unit: 'חדרים', showIf: function (v) { return v.view === 'cost' && v.ptype === 'apt'; } },
      { id: 'roof', label: 'גם גג או גינה צמודים', type: 'segmented', showIf: function (v) { return v.view === 'cost' && v.ptype === 'apt'; }, options: [{ value: 'no', label: 'לא' }, { value: 'yes', label: 'כן' }] },
      { id: 'group', label: 'כמה דירות מזמינות יחד', type: 'number', unit: 'דירות', showIf: function (v) { return v.view === 'cost' && v.ptype === 'apt'; } },
      { id: 'apts', label: 'דירות בבניין', type: 'number', unit: 'דירות', showIf: function (v) { return v.view === 'cost' && v.ptype === 'shared'; } }
    ],
    compute: function (v, data) {
      var D = data.bedek; if (!D || !D.law) return { error: { field: null, msg: 'הנתונים לא נטענו.' } };
      return v.view === 'cost' ? viewCost(v, D) : v.view === 'calendar' ? viewCalendar(v, D) : viewDefect(v, D);
    }
  });
})();
