/* NadLan Instruments · urtrack v1 (Q1 moat "יומן המתחמים", 26.10.2026): the complex tracker of /urban-renewal/map/. For every urban
   renewal complex: the stage and track at the authority today (its live map, the freshest source), the stage in the data.gov.il file
   and in our own import, units today and after building with the multiplier, plan number, the plan's approval and deposit dates
   (the authority and XPLAN), "מופיע במאגר מאז" and every change we saw between dated snapshots, each with its check date. A second
   view, "מה זז במאגר", counts and lists all the changes (T8). Honesty: never a start or occupancy year; the 4.0 years from approval
   to a first permit is the authority's average, shown only for an approved plan before implementation, never as a forecast; when two
   sources disagree both are shown with their dates. Search folds spelling (גבעתיים/גבעתים, פתח תקווה/פתח תקוה, ו/וו, י/יי).
   Data: data/renewal-track.json (tools/urban/build_renewal_track.py). Pure logic in NLUR for checks. SVG in RTL: text-anchor start
   = the right end of a label. */
(function () {
  'use strict';
  var SHORT = ['ללא שלב', 'תכנון ראשוני', 'תכנון סטטוטורי', 'תכנית מאושרת', 'במימוש', 'אחרי רישוי'];
  var KIND = { 'new': 'נוסף', up: 'עלה שלב', down: 'ירד שלב', chg: 'השלב השתנה', gone: 'ירד מהרשימה', back: 'חזר לרשימה', trk: 'המסלול השתנה', renum: 'מספר מתחם חדש' };
  var ORDER = { up: 0, 'new': 1, down: 2, chg: 3, trk: 4, renum: 5, back: 6, gone: 7 };
  var ALL = '*';

  /** Search folding: no niqqud, no punctuation, double vav and double yod folded, one space. */
  function norm(s) {
    return String(s == null ? '' : s).replace(/[\u0591-\u05C7]/g, '').replace(/[-\u2010-\u2015,.;:!?"'\u05F3\u05F4()\[\]\/\\+]/g, ' ')
      .replace(/\s+/g, ' ').trim().replace(/יי/g, 'י').replace(/וו/g, 'ו');
  }
  function dd(iso) { var p = String(iso || '').split('-'); return p.length === 3 ? (+p[2]) + '.' + (+p[1]) + '.' + p[0] : String(iso || ''); }
  function n0(x) { return String(Math.round(x || 0)).replace(/\B(?=(\d{3})+(?!\d))/g, ','); }
  function lastOf(D, kind) { for (var i = D.snaps.length - 1; i >= 0; i--) if (D.snaps[i].k === kind) return i; return -1; }
  function snapAt(D, date) { for (var i = D.snaps.length - 1; i >= 0; i--) if (D.snaps[i].d === date) return D.snaps[i]; return null; }
  function station(s) { return String(s || '').replace(/^בבדיקה /, 'בדיקה '); }  // XPLAN's "בבדיקה תכנונית", said without the pending word

  /** Indexes, built once per data object: by key, by city (sorted by name), the folded search text, every change flattened. */
  function ix(D) {
    if (D.__ix) return D.__ix;
    var by = {}, city = {}, all = [];
    D.recs.forEach(function (r) {
      by[r.k] = r; (city[r.c] = city[r.c] || []).push(r);
      r.__h = norm(r.n + ' ' + r.c + ' ' + (r.pl || '')); r.__p = r.pl ? norm(r.pl).replace(/ /g, '') : '';
      (r.ch || []).forEach(function (c) { all.push({ r: r, c: c }); });
    });
    var cities = Object.keys(city).sort(function (a, b) { return a.localeCompare(b, 'he'); });
    cities.forEach(function (c) { city[c].sort(function (a, b) { return a.n.localeCompare(b.n, 'he'); }); });
    all.sort(function (a, b) { return a.c[0] < b.c[0] ? 1 : a.c[0] > b.c[0] ? -1 : (ORDER[a.c[1]] - ORDER[b.c[1]]) || a.r.c.localeCompare(b.r.c, 'he') || a.r.n.localeCompare(b.r.n, 'he'); });
    return (D.__ix = { by: by, city: city, cities: cities, all: all });
  }

  /** Complexes matching a free-text query (every word must appear in the name, the city or the plan number). */
  function search(D, q, max) {
    var t = norm(q); if (t.replace(/ /g, '').length < 2) return [];
    var X = ix(D), toks = t.split(' '), qc = t.replace(/ /g, ''), out = [];
    D.recs.forEach(function (r) {
      var ok = toks.every(function (w) { return r.__h.indexOf(w) > -1 || (r.__p && r.__p.indexOf(w) > -1); }) || (r.__p && qc.length >= 4 && r.__p.indexOf(qc) > -1);
      if (ok) out.push(r);
    });
    var f = toks[0], lm = lastOf(D, 'map');
    var on = function (r) { return lm > -1 && r.s[lm] !== -1 ? 0 : 1; };  // complexes on the authority's map today first
    out.sort(function (a, b) { var sa = norm(a.n).indexOf(f) === 0 ? 0 : 1, sb = norm(b.n).indexOf(f) === 0 ? 0 : 1; return (on(a) - on(b)) || (sa - sb) || a.c.localeCompare(b.c, 'he') || a.n.localeCompare(b.n, 'he'); });
    return out.slice(0, max || 80);
  }

  /** One change as words (RTL, the arrow points from the old value to the new one). */
  function chText(D, c) {
    var k = c[1], sn = snapAt(D, c[0]), where = sn ? (sn.k === 'map' ? 'במפת הרשות' : sn.k === 'file' ? 'בקובץ data.gov.il' : 'בייבוא שלנו') : '';
    if (k === 'new') return 'נוסף לרשימה, ' + (c[3] > 0 ? SHORT[c[3]] : 'ללא שלב');
    if (k === 'gone') return 'לא מופיע ' + where;
    if (k === 'back') return 'חזר לרשימה, ' + (c[3] > 0 ? SHORT[c[3]] : 'ללא שלב');
    if (k === 'trk') return 'המסלול השתנה: ' + D.tracks[c[2]] + ' ← ' + D.tracks[c[3]];
    if (k === 'renum') return 'מספר מתחם חדש: ' + c[2] + ' ← ' + c[3];
    return KIND[k] + ': ' + SHORT[c[2]] + ' ← ' + SHORT[c[3]];
  }
  function fromTo(D, c) {
    var k = c[1];
    if (k === 'new' || k === 'back') return 'נכנס: ' + SHORT[Math.max(0, c[3])];
    if (k === 'gone') return 'אחרון: ' + SHORT[Math.max(0, c[2])];
    if (k === 'trk') return D.tracks[c[2]] + ' ← ' + D.tracks[c[3]];
    if (k === 'renum') return c[2] + ' ← ' + c[3];
    return SHORT[c[2]] + ' ← ' + SHORT[c[3]];
  }
  /** The state of a complex today: on the latest map, in the latest file, where it was seen last. */
  function state(D, r) {
    var lm = lastOf(D, 'map'), lf = lastOf(D, 'file'), last = -1;
    for (var i = r.s.length - 1; i >= 0; i--) if (r.s[i] !== -1) { last = i; break; }
    return { lm: lm, lf: lf, sm: lm > -1 ? r.s[lm] : -1, sf: lf > -1 ? r.s[lf] : -1, last: last };
  }
  function stageCell(D, r) {
    var t = state(D, r);
    if (t.sm === -1) return 'לא במפת הרשות' + (t.last > -1 && r.s[t.last] > 0 ? ' (אחרון: ' + SHORT[r.s[t.last]] + ')' : '');
    if (t.sm === 0) return 'ללא שלב במפה' + (t.sf > 0 ? ' (בקובץ: ' + SHORT[t.sf] + ')' : '');
    return SHORT[t.sm] + (t.sf > 0 && t.sf !== t.sm ? ' (בקובץ: ' + SHORT[t.sf] + ')' : '');
  }
  function counts(D, city) {
    var A = D.agg, lm = lastOf(D, 'map');
    if (!city) return { n: lm > -1 ? D.snaps[lm].n : 0, add: A.added, up: A.up, down: A.down, chg: A.chg, gone: A.gone, renum: A.renum };
    var c = (A.cities || {})[city] || {};
    return { n: c.n || 0, add: c.add || 0, up: c.up || 0, down: c.down || 0, chg: c.chg || 0, gone: c.gone || 0, renum: c.renum || 0 };
  }
  function pl(n, one, many) { return n0(n) + ' ' + (n === 1 ? one : many); }
  /** What else moved, in words that agree with the count: "18 עלו שלב", "1 קיבל מספר מתחם חדש". */
  function moved(c) {
    var p = [pl(c.up, 'עלה שלב', 'עלו שלב')];
    if (c.down) p.push(pl(c.down, 'ירד שלב', 'ירדו שלב'));
    if (c.chg) p.push(pl(c.chg, 'שינה שלב', 'שינו שלב'));
    if (c.gone) p.push(pl(c.gone, 'לא מופיע עוד', 'לא מופיעים עוד'));
    if (c.renum) p.push(pl(c.renum, 'קיבל מספר מתחם חדש', 'קיבלו מספר מתחם חדש'));
    return p;
  }
  /** The count line: "מאז 15.8.2026 נוספו 36 מתחמים ו-18 עלו שלב" (+ what else moved). */
  function countLine(D, city) {
    var c = counts(D, city), A = D.agg, p = [(c.add === 1 ? 'נוסף ' : 'נוספו ') + pl(c.add, 'מתחם', 'מתחמים')].concat(moved(c));
    var s = p.length > 1 ? p.slice(0, -1).join(', ') + ' ו-' + p[p.length - 1] : p[0];
    return 'מאז ' + dd(A.since) + (city ? ' ב' + city : '') + ' ' + s + ' (קובץ data.gov.il מול מפת הרשות של ' + dd(A.to) + ')';
  }
  /** The complex a city opens on: its newest change among complexes on the map today, else its first complex on the map. */
  function pickInCity(D, city) {
    var X = ix(D), lm = lastOf(D, 'map'), list = X.city[city] || [];
    var e = X.all.filter(function (x) { return x.r.c === city && x.r.s[lm] !== -1; })[0];
    if (e) return e.r.k;
    var on = list.filter(function (r) { return r.s[lm] !== -1; })[0] || list[0];
    return on ? on.k : '';
  }
  function slugUrl(s) { return encodeURIComponent(s).replace(/%[0-9A-F]{2}/g, function (x) { return x.toLowerCase(); }); }
  function presetList(D) {
    var X = ix(D), out = [], used = {}, lm = lastOf(D, 'map'), lf = lastOf(D, 'file');
    function add(e, sub) { if (!e || used[e.r.k]) return; used[e.r.k] = 1; out.push({ key: 'p' + out.length, label: e.r.n + ', ' + e.r.c, sub: sub, set: { view: 'cx', city: e.r.c, q: '', cx: e.r.k } }); }
    var ups = X.all.filter(function (e) { return e.c[1] === 'up'; });
    var ks = ups.filter(function (e) { return norm(e.r.n).indexOf('כפר שלם') > -1 && e.r.c.indexOf('תל אביב') > -1; })[0] || ups.filter(function (e) { return e.c[3] >= 3; })[0];
    if (ks) add(ks, 'עלה שלב ב-' + dd(ks.c[0]) + ': ' + SHORT[ks.c[3]]);
    if (ups[0]) add(ups[0], 'עלה שלב ב-' + dd(ups[0].c[0]));
    var nw = X.all.filter(function (e) { return e.c[1] === 'new' && e.r.s[lm] !== -1; })[0];
    if (nw) add(nw, 'נוסף לרשימה ב-' + dd(nw.c[0]));
    var gn = X.all.filter(function (e) { return e.c[1] === 'gone' && lf > -1 && e.r.s[lf] !== -1 && e.r.s[lm] === -1; })[0];
    if (gn) add(gn, 'ירד מהרשימה ב-' + dd(gn.c[0]));
    var g = search(D, 'גבעתיים');
    if (g.length) out.push({ key: 'search', label: 'חיפוש: גבעתיים', sub: g.length + ' תוצאות, האיות לא משנה', set: { view: 'cx', city: g[0].c, q: 'גבעתיים', cx: g[0].k } });
    out.push({ key: 'moves', label: 'מה זז במאגר', sub: pl(D.agg.added, 'נוסף', 'נוספו') + ', ' + pl(D.agg.up, 'עלה שלב', 'עלו שלב'), set: { view: 'chg', city: ALL, q: '' } });
    return out;
  }
  window.NLUR = { norm: norm, search: search, ix: ix, state: state, chText: chText, fromTo: fromTo, countLine: countLine, counts: counts, presets: presetList, pickInCity: pickInCity, stageCell: stageCell, dd: dd, SHORT: SHORT };
  if (!window.NadLanInstruments) return;
  var NI = window.NadLanInstruments, F = NI.fmt, esc = NI.esc;

  /** The timeline: a lane per stage, a column per snapshot (the oldest on the right), the stage at each check, coloured by the move. */
  function svgTimeline(D, r) {
    var N = D.snaps.length, idx = [], i;
    if (N <= 8) { for (i = 0; i < N; i++) idx.push(i); } else { idx.push(0); for (i = N - 7; i < N; i++) idx.push(i); }
    // 16 px in a 420 viewBox stays about 12 px on a phone; dates on three short rows (day.month, year, source) so columns never collide
    var XR = 276, XL = 46, n = idx.length, step = n > 1 ? Math.min(84, (XR - XL) / (n - 1)) : 0;
    var lanes = [5, 4, 3, 2, 1, 0, -1], LY0 = 56, LH = 28, F16 = 'font-size:16px;';
    var ly = function (s) { return LY0 + lanes.indexOf(s) * LH; }, xx = function (k) { return XR - k * step; };
    var chAt = {}; (r.ch || []).forEach(function (c) { (chAt[c[0]] = chAt[c[0]] || []).push(c[1]); });
    var g = [];
    g.push('<text x="410" y="24" class="t" text-anchor="start" style="font-size:17px">' + esc('השלב בכל בדיקה') + '</text>');
    lanes.forEach(function (s) {
      var y = ly(s);
      g.push('<line x1="' + (XL - 26) + '" y1="' + y + '" x2="' + (XR + 12) + '" y2="' + y + '" stroke="#D3DCE2" stroke-width="1"' + (s <= 0 ? ' stroke-dasharray="3 4"' : '') + '/>');
      g.push('<text x="410" y="' + (y + 6) + '" text-anchor="start"' + (s === -1 ? ' class="r" style="' + F16 + '"' : ' style="' + F16 + (s === 0 ? 'fill:#5E6A75' : 'fill:#12202A') + '"') + '>' + esc(s === -1 ? 'לא ברשימה' : SHORT[s]) + '</text>');
    });
    var yb = ly(-1);
    idx.forEach(function (si, k) {
      var X = xx(k), sn = D.snaps[si], p = sn.d.split('-');
      g.push('<line x1="' + X + '" y1="' + (LY0 - 16) + '" x2="' + X + '" y2="' + (yb + 12) + '" stroke="#EDF1F4" stroke-width="1"/>');
      g.push('<text x="' + X + '" y="' + (yb + 36) + '" text-anchor="middle" style="' + F16 + 'fill:#12202A;font-weight:600">' + esc((+p[2]) + '.' + (+p[1])) + '</text>');
      g.push('<text x="' + X + '" y="' + (yb + 54) + '" text-anchor="middle" style="font-size:14px;fill:#5E6A75">' + esc(p[0]) + '</text>');
      g.push('<text x="' + X + '" y="' + (yb + 72) + '" text-anchor="middle" style="font-size:14px;fill:#5E6A75">' + esc(sn.short) + '</text>');
    });
    if (N > 8) g.push('<text x="' + (xx(0) + xx(1)) / 2 + '" y="' + (LY0 - 22) + '" text-anchor="middle" style="' + F16 + 'fill:#5E6A75">…</text>');
    for (var k = 1; k < n; k++) {
      var a = r.s[idx[k - 1]], b = r.s[idx[k]], kinds = chAt[D.snaps[idx[k]].d] || [], col = '#12202A', w = 1.6, dash = '';
      if (kinds.indexOf('up') > -1) { col = '#1F4B5C'; w = 3.4; }
      else if (kinds.indexOf('down') > -1 || kinds.indexOf('gone') > -1) { col = '#C42550'; w = 2.6; }
      else if (a === -1 || b === -1 || a === 0 || b === 0 || a !== b) { col = '#8A97A2'; dash = ' stroke-dasharray="4 4"'; }
      g.push('<line x1="' + xx(k - 1) + '" y1="' + ly(a) + '" x2="' + xx(k) + '" y2="' + ly(b) + '" stroke="' + col + '" stroke-width="' + w + '"' + dash + ' stroke-linecap="round"/>');
    }
    idx.forEach(function (si, k) {
      var s = r.s[si], X = xx(k), Y = ly(s), lastc = k === n - 1;
      if (s > 0) g.push('<circle cx="' + X + '" cy="' + Y + '" r="' + (lastc ? 8 : 6) + '" fill="' + (lastc ? '#1F4B5C' : '#2F6F86') + '" stroke="#fff" stroke-width="2"/>');
      else if (s === 0) g.push('<circle cx="' + X + '" cy="' + Y + '" r="6" fill="#fff" stroke="#5E6A75" stroke-width="1.6"/>');
      else g.push('<circle cx="' + X + '" cy="' + Y + '" r="6" fill="#fff" stroke="#C42550" stroke-width="2"/><path d="M' + (X - 3) + ' ' + (Y - 3) + 'l6 6M' + (X + 3) + ' ' + (Y - 3) + 'l-6 6" stroke="#C42550" stroke-width="1.6"/>');
    });
    var H = yb + 108;
    g.push('<text x="410" y="' + (H - 10) + '" text-anchor="start" style="font-size:14px;fill:#5E6A75">' + esc('כל עמודה היא בדיקה, לפי תאריך הנתונים במקור') + '</text>');
    var aria = 'ציר הבדיקות של ' + r.n + ': ' + idx.map(function (si) { var s = r.s[si]; return dd(D.snaps[si].d) + ' ' + (s === -1 ? 'לא ברשימה' : SHORT[s]); }).join(', ');
    return '<svg class="nli__wall" direction="rtl" viewBox="0 0 420 ' + H + '" role="img" aria-label="' + esc(aria) + '">' + g.join('') + '</svg>';
  }

  /** The moves view: per check, how many complexes were added, moved up, or left the list (the last four checks). */
  function svgSteps(D, city) {
    var X = ix(D), N = D.snaps.length, steps = [];
    for (var i = Math.max(1, N - 4); i < N; i++) {
      var d = D.snaps[i].d, c = { 'new': 0, up: 0, gone: 0, other: 0 };
      X.all.forEach(function (e) { if (e.c[0] === d && (!city || e.r.c === city)) { var k = e.c[1]; if (k === 'new' || k === 'back') c['new']++; else if (k === 'up') c.up++; else if (k === 'gone' || k === 'down') c.gone++; else c.other++; } });
      steps.push({ a: D.snaps[i - 1], b: D.snaps[i], c: c });
    }
    var mx = 1; steps.forEach(function (s) { mx = Math.max(mx, s.c['new'], s.c.up, s.c.gone); });
    var rows = [['new', 'נוספו', '#2F6F86'], ['up', 'עלו שלב', '#1F4B5C'], ['gone', 'ירדו מהרשימה', '#C42550']];
    var g = [], y = 24, XR = 296, WMAX = 228, F16 = 'font-size:16px;';
    g.push('<text x="410" y="' + y + '" class="t" text-anchor="start" style="font-size:17px">' + esc('מה זז בכל בדיקה' + (city ? ' ב' + city : '')) + '</text>');
    y += 14;
    steps.forEach(function (s) {
      y += 28;  // the step in dates only, the sources in short words (no Latin inside the Hebrew line)
      g.push('<text x="410" y="' + y + '" text-anchor="start" style="' + F16 + 'font-weight:600;fill:#12202A">' + esc(dd(s.b.d) + ' מול ' + dd(s.a.d) + ' · ' + s.b.short + ' מול ' + s.a.short) + '</text>');
      rows.forEach(function (rw) {
        y += 27; var v = s.c[rw[0]], w = v ? Math.max(3, Math.round(WMAX * v / mx)) : 0;
        g.push('<text x="410" y="' + (y + 5) + '" text-anchor="start"' + (rw[0] === 'gone' ? ' class="r"' : '') + ' style="' + F16 + '">' + esc(rw[1]) + '</text>');
        g.push('<line x1="' + (XR - WMAX) + '" y1="' + y + '" x2="' + XR + '" y2="' + y + '" stroke="#EDF1F4" stroke-width="16"/>');
        if (w) g.push('<rect x="' + (XR - w) + '" y="' + (y - 8) + '" width="' + w + '" height="16" fill="' + rw[2] + '"/>');
        g.push('<text x="' + (XR - w - 6) + '" y="' + (y + 6) + '" class="m" text-anchor="start" style="font-size:16px">' + v + '</text>');
      });
      if (s.c.other) { y += 26; g.push('<text x="410" y="' + y + '" text-anchor="start" style="font-size:14px;fill:#5E6A75">' + esc('ועוד ' + s.c.other + ': מסלול או מספר מתחם השתנו') + '</text>'); }
      y += 10;
    });
    y += 20;
    g.push('<text x="410" y="' + y + '" text-anchor="start" style="font-size:14px;fill:#5E6A75">' + esc('השוואה לפי מספר המתחם של הרשות, בין כל שתי בדיקות') + '</text>');
    return '<svg class="nli__wall" direction="rtl" viewBox="0 0 420 ' + (y + 12) + '" role="img" aria-label="' + esc('שינויים בכל בדיקה' + (city ? ' ב' + city : '')) + '">' + g.join('') + '</svg>';
  }

  function formula(D) {
    return 'השוואה לפי מספר המתחם של הרשות בין צילומי מצב: ' + D.snaps.map(function (s) { return s.label + ' ' + dd(s.d); }).join(', ')
      + '. כל שינוי מתוארך לצילום המצב הראשון שבו ראינו אותו, ותאריך הבדיקה הוא תאריך הנתונים במקור. מתחם שיצא מהרשימה ונכנס באותו יום במספר אחר, עם אותו שם ואותה עיר, נספר כמספר מתחם חדש. אין כאן שנת התחלת בנייה או אכלוס: המקורות לא מפרסמים אותן, ואנחנו לא מנחשים.';
  }

  function complexView(v, D) {
    var X = ix(D), r = X.by[v.cx];
    if (!r) return { error: { field: norm(v.q) ? 'q' : 'cx', msg: 'לא מצאנו מתחם כזה. נסו שם רחוב, שם מתחם או מספר תכנית.' } };
    var t = state(D, r), mapD = t.lm > -1 ? D.snaps[t.lm].d : '', fileD = t.lf > -1 ? D.snaps[t.lf].d : '', onMap = t.sm !== -1, lines = [], notes = [];
    var answer = onMap
      ? { label: r.n + ', ' + r.c, value: SHORT[t.sm], sub: esc('השלב אצל הרשות ב-' + dd(mapD) + ': ' + (t.sm ? D.stages[t.sm] : 'המפה לא מציינת שלב') + (r.t ? ' · מסלול ' + D.tracks[r.t] : '') + (r.ty ? ' · ' + r.ty : '')) }
      : { label: r.n + ', ' + r.c, value: 'לא במפת הרשות', tone: 'survey', sub: esc('לא מופיע במפת הרשות ב-' + dd(mapD) + (t.last > -1 ? '. בפעם האחרונה שהופיע (' + D.snaps[t.last].label + ', ' + dd(D.snaps[t.last].d) + '): ' + (r.s[t.last] > 0 ? D.stages[r.s[t.last]] : 'ללא שלב') : '') + (r.t ? ' · מסלול ' + D.tracks[r.t] : '')) };
    if (onMap && t.sf > 0 && t.sf !== t.sm) lines.push({ label: 'השלב בקובץ data.gov.il, ' + dd(fileD), value: SHORT[t.sf] });
    if (r.p) {
      var us = D.snaps[r.u];
      if (r.e) {
        lines.push({ label: 'דירות היום ← אחרי הבנייה (' + us.label + ', ' + dd(us.d) + ')', value: F.num(r.e) + ' → ' + F.num(r.p) });
        lines.push({ label: 'מכפיל: דירות אחרי הבנייה חלקי דירות היום (חישוב שלנו)', value: '× ' + F.num(r.p / r.e, 2) });
      } else lines.push({ label: 'דירות אחרי הבנייה (' + us.label + ', ' + dd(us.d) + ')', value: F.num(r.p) });
      if (r.pf) lines.push({ label: 'באותו מתחם בקובץ data.gov.il, ' + dd(fileD), value: (r.ef ? F.num(r.ef) + ' → ' : '') + F.num(r.pf) });
    }
    if (r.pl) lines.push({ label: 'מספר תכנית', value: r.pl });
    var x = r.x;
    if (r.ap && x && x[2] === r.ap) lines.push({ label: 'אישור התכנית (הרשות ו-XPLAN)', value: dd(r.ap) });
    else {
      if (r.ap) lines.push({ label: 'אישור התכנית לפי הרשות', value: dd(r.ap) });
      if (x && x[2]) lines.push({ label: 'פרסום אישור ברשומות (XPLAN)', value: dd(x[2]) });
    }
    if (x && x[1]) lines.push({ label: 'דיון בהפקדה (XPLAN)', value: dd(x[1]) });
    if (x && D.xplan) lines.push({ label: 'השלב ב-XPLAN: ' + station(D.xst[x[0]]), value: 'נבדק ' + dd(D.xplan.d) });
    if (r.dc) lines.push({ label: 'הכרזה (קובץ data.gov.il)', value: dd(r.dc) });
    if (r.pm) lines.push({ label: 'היתרים שנרשמו (קובץ data.gov.il)', value: F.num(r.pm) + ' יח"ד' });
    if (r.bz) lines.push({ label: 'מסומן בביצוע (קובץ data.gov.il)', value: 'כן' });
    lines.push({ label: 'מופיע במאגר מאז', value: dd(D.snaps[r.f].d) + (r.f === 0 ? ' או לפני' : '') });
    var ch = r.ch || [];
    ch.forEach(function (c) { lines.push({ label: chText(D, c), value: dd(c[0]) }); });
    if (!ch.length) lines.push({ label: 'שינויים בין הבדיקות', value: 'לא נמצאו' });
    // notes: disagreements with both dates, the authority's average for an approved plan, renumbering, where to read more
    if (onMap && t.sm === 0 && t.sf > 0) notes.push(esc('במפת הרשות (' + dd(mapD) + ') המתחם מופיע בלי שלב. בקובץ data.gov.il (' + dd(fileD) + ') השלב שלו: ' + D.stages[t.sf] + '.'));
    if (onMap && t.sm > 0 && t.sf > 0 && t.sf !== t.sm) notes.push(esc('שני המקורות שונים: במפת הרשות (' + dd(mapD) + ') ' + D.stages[t.sm] + ', ובקובץ data.gov.il (' + dd(fileD) + ') ' + D.stages[t.sf] + '. לפי הרשות, המפה מתעדכנת מדי יום.'));
    if (r.k.indexOf('s:') === 0) notes.push(esc('המתחם הופיע בייבוא שלנו מ-' + dd(D.snaps[0].d) + ', ולא מופיע מאז בקובץ data.gov.il או במפת הרשות.'));
    ch.filter(function (c) { return c[1] === 'renum'; }).forEach(function (c) { notes.push(esc('מ-' + dd(c[0]) + ' המתחם מופיע במספר מתחם ' + c[3] + ' (קודם: ' + c[2] + '), עם אותו שם ואותה עיר.')); });
    var cur = onMap && t.sm > 0 ? t.sm : t.sf;
    if (cur === 3) notes.push(esc('בממוצע עוברות ' + F.num(D.avg.years, 1) + ' שנים מאישור התכנית עד היתר ראשון (הרשות, ' + D.avg.year + '). זה ממוצע של מתחמים שכבר קיבלו היתר, ולא תחזית למתחם הזה.'));
    var links = [];
    if (r.mv) links.push('<a href="https://mavat.iplan.gov.il/SV4/1/' + esc(r.mv) + '/310" target="_blank" rel="noopener">' + esc('התכנית באתר מינהל התכנון') + '</a>');
    if (r.w) links.push('<a href="/projects/' + esc(slugUrl(r.w)) + '/">' + esc('עמוד המתחם באתר') + '</a>');
    links.push('<a href="https://www.gov.il/he/departments/topics/mapa-renewal" target="_blank" rel="noopener">' + esc('מפת הרשות') + '</a>');
    notes.push(links.join(' · '));
    // the city table
    var list = X.city[r.c] || [], cc = counts(D, r.c), tp = [F.num(cc.n) + ' מתחמים במפת הרשות'];
    if (cc.add) tp.push(pl(cc.add, 'נוסף', 'נוספו')); if (cc.up) tp.push(pl(cc.up, 'עלה שלב', 'עלו שלב')); if (cc.gone) tp.push(pl(cc.gone, 'ירד מהרשימה', 'ירדו מהרשימה'));
    var table = { title: r.c + ': ' + tp.join(', ') + (tp.length > 1 ? ' מאז ' + dd(D.agg.since) : ''), head: ['מתחם', 'השלב אצל הרשות', 'דירות היום ← אחרי', 'שינוי אחרון'], num: [2], phoneHide: [2],
      rows: list.map(function (q) { var lc = q.ch && q.ch[q.ch.length - 1]; return [q.n + (q.k === r.k ? ' (נבחר)' : ''), stageCell(D, q), q.p ? (q.e ? F.num(q.e) + ' → ' : '') + F.num(q.p) : '', lc ? KIND[lc[1]] + ' ' + dd(lc[0]) : '']; }) };
    var txt = 'יומן המתחמים: ' + r.n + ', ' + r.c + '. ' + (onMap ? 'השלב אצל הרשות (' + dd(mapD) + '): ' + (t.sm ? D.stages[t.sm] : 'ללא שלב') : 'לא מופיע במפת הרשות (' + dd(mapD) + ')')
      + (r.t ? ', מסלול ' + D.tracks[r.t] : '') + (r.e && r.p ? '. דירות היום ' + F.num(r.e) + ', אחרי הבנייה ' + F.num(r.p) : '') + (r.pl ? '. תכנית ' + r.pl : '') + '.'
      + (ch.length ? ' שינויים: ' + ch.map(function (c) { return chText(D, c) + ' (' + dd(c[0]) + ')'; }).join('; ') + '.' : '');
    return { answer: answer, figure: svgTimeline(D, r), lines: lines, note: notes.join('<br>'), table: table, formula: formula(D), sources: D.sources, text: txt };
  }

  function changesView(v, D) {
    var X = ix(D), city = v.city && v.city !== ALL ? v.city : '', c = counts(D, city), A = D.agg;
    var rows = X.all.filter(function (e) { return !city || e.r.c === city; });
    var parts = moved(c);
    var lines = [{ label: 'מתחמים במפת הרשות, ' + dd(A.to), value: F.num(c.n) }, { label: 'נוספו לרשימה', value: F.num(c.add) }, { label: 'עלו שלב', value: F.num(c.up) }];
    if (c.down) lines.push({ label: 'ירדו שלב', value: F.num(c.down) });
    if (c.chg) lines.push({ label: 'השלב השתנה', value: F.num(c.chg) });
    lines.push({ label: 'לא מופיעים עוד במפת הרשות', value: F.num(c.gone) });
    if (c.renum) lines.push({ label: 'מספר מתחם חדש', value: F.num(c.renum) });
    if (A.last && !city) { var L = A.last, nl = L['new'] + L.up + L.down + L.chg + L.gone + L.back + L.trk + L.renum; lines.push({ label: 'הבדיקה האחרונה: ' + dd(L.to) + ' מול ' + dd(L.from), value: nl + (nl === 1 ? ' שינוי' : ' שינויים') }); }
    return {
      answer: { label: 'מה זז במאגר' + (city ? ' ב' + city : '') + ' מ-' + dd(A.since) + ' עד ' + dd(A.to), value: pl(c.add, 'נוסף', 'נוספו'), sub: esc('ו-' + parts.join(', ') + '. קובץ data.gov.il מול מפת הרשות.') },
      figure: svgSteps(D, city), lines: lines,
      note: rows.length ? esc('הטבלה מסודרת מהבדיקה החדשה לישנה. לחיצה על מתחם אחד מציגה את כל ההיסטוריה שלו.') : esc('בעיר הזאת לא ראינו שינויים בין הבדיקות.'),
      table: { title: 'כל השינויים' + (city ? ' ב' + city : '') + ' (' + rows.length + ')', head: ['מתחם', 'עיר', 'מה השתנה', 'משלב ← לשלב', 'תאריך הבדיקה'], phoneHide: city ? [1] : [],
        rows: rows.map(function (e) { return [e.r.n, e.r.c, KIND[e.c[1]], fromTo(D, e.c), dd(e.c[0])]; }) },
      formula: formula(D), sources: D.sources, text: countLine(D, city) + '.'
    };
  }

  NI.register('urtrack', {
    kicker: 'יומן · התחדשות עירונית',
    title: 'יומן המתחמים: מה השלב של המתחם שלכם, ומה השתנה בו',
    lede: 'בוחרים עיר ומתחם, או מחפשים לפי שם, רחוב או מספר תכנית, ומקבלים את השלב אצל הרשות היום, את המסלול, כמה דירות יש היום וכמה יהיו אחרי הבנייה, את תאריכי התכנית, ואת כל שינוי שראינו בין הבדיקות, עם תאריך הבדיקה.',
    strip: function (data) { var D = data.urtrack, A = D.agg, lm = lastOf(D, 'map'); return [{ label: 'מתחמים במפת הרשות', value: F.num(lm > -1 ? D.snaps[lm].n : 0) }, { label: 'נוספו מאז ' + dd(A.since), value: F.num(A.added) }, { label: 'עלו שלב', value: F.num(A.up) }, { label: 'הבדיקה האחרונה', value: dd(A.to) }]; },
    presets: function (data) { return presetList(data.urtrack); },
    defaults: function (data) { var p = presetList(data.urtrack)[0]; return p ? JSON.parse(JSON.stringify(Object.assign({ view: 'cx', city: '', q: '', cx: '', keep: '' }, p.set))) : { view: 'cx', city: ix(data.urtrack).cities[0], q: '', cx: '', keep: '' }; },
    fields: [
      { id: 'view', label: 'מה להציג', type: 'segmented', options: [{ value: 'cx', label: 'מתחם אחד' }, { value: 'chg', label: 'מה זז במאגר' }] },
      { id: 'city', label: 'עיר', type: 'select', optionsFrom: function (v, data) {
        var D = data.urtrack, X = ix(D), r = X.by[v.cx];
        // every control keeps city and complex together; a page case that names only a city ([nadlan_tool id="urtrack" city="..."]) wins
        if (v.view === 'cx' && norm(v.q).replace(/ /g, '').length < 2) {
          if (!X.city[v.city]) v.city = r ? r.c : X.cities[0];
          else if (!r || r.c !== v.city) v.cx = pickInCity(D, v.city);
        }
        var o = X.cities.map(function (c) { return { value: c, label: c + ' (' + X.city[c].length + ')' }; });
        return v.view === 'chg' ? [{ value: ALL, label: 'כל הערים (' + D.recs.length + ' מתחמים)' }].concat(o) : o;
      } },
      { id: 'q', label: 'חיפוש לפי שם מתחם, רחוב או מספר תכנית', type: 'text', help: 'לא חובה. האיות לא משנה: גבעתיים או גבעתים, פתח תקווה או פתח תקוה.', showIf: function (v) { return v.view === 'cx'; } },
      { id: 'cx', label: 'מתחם', type: 'select', showIf: function (v) { return v.view === 'cx'; }, optionsFrom: function (v, data) {
        var D = data.urtrack, X = ix(D);
        if (v.view !== 'cx') { var cur = X.by[v.cx]; return (X.city[cur ? cur.c : X.cities[0]] || []).map(function (r) { return { value: r.k, label: r.n }; }); }  // hidden: keep the complex
        if (norm(v.q).replace(/ /g, '').length >= 2) {
          var m = search(D, v.q);
          return m.length ? m.map(function (r) { return { value: r.k, label: r.n + ', ' + r.c }; }) : [{ value: '', label: 'אין תוצאות לחיפוש הזה' }];
        }
        return (X.city[v.city] || []).map(function (r) { return { value: r.k, label: r.n }; });
      } }
    ],
    onField: function (id, v, data, redraw) {
      var D = data.urtrack, X = ix(D);
      if (id === 'view') {
        if (v.view === 'chg') v.city = ALL;
        else { var r = X.by[v.cx]; v.city = r ? r.c : X.cities[0]; if (!r) v.cx = pickInCity(D, v.city); }
      } else if (id === 'city' && v.view === 'cx') {
        v.q = ''; redraw('q'); v.cx = pickInCity(D, v.city);
      } else if (id === 'q') {
        var m = search(D, v.q), typed = norm(v.q).replace(/ /g, '').length >= 2;
        if (m.length && !m.some(function (r) { return r.k === v.cx; })) { v.cx = m[0].k; v.city = m[0].c; }
        else if (!m.length && typed && X.by[v.cx]) v.keep = v.cx;  // a search with no result: come back here when it is cleared
        if (!typed && X.by[v.keep]) { v.cx = v.keep; v.city = X.by[v.keep].c; v.keep = ''; }
      } else if (id === 'cx') {
        var rr = X.by[v.cx]; if (rr) v.city = rr.c;
      }
    },
    compute: function (v, data) {
      var D = data.urtrack;
      if (!D || !D.recs) return { error: { field: null, msg: 'הנתונים לא נטענו.' } };
      return v.view === 'chg' ? changesView(v, D) : complexView(v, D);
    }
  });
})();
