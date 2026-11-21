/* NadLan Instruments · pval v2 (Q2 of the upgrade loop, 26.10.2026; v1 HAD-575, Ben 15.10 + 21.10.2026): what an apartment is worth.
   v1, kept whole: (1) from the official closed deals: the median price for the room count in the neighbourhood (or the city when
   the neighbourhood has no published median in the last four quarters), from the Tax Authority summary files of the government
   real-estate site; (2) area x price per m2 plus balcony, parking and storage. Both take the owner's adjustments (condition,
   floor / view / building), a safety range, and a check of an asking price. Same id, same fields, same numbers.
   v2, the moat of dna.md 7.8 ("שווי היום לפי מחיר הקנייה שלכם, בשלוש בדיקות רשמיות"): property type, rooms 2 to 6 (2 and 6 use the
   nearest official series, 3 or 5, and say so), purchase month, year and price. Three official checks side by side:
     1 = the official median now (neighbourhood, else city) with its quarter;
     2 = purchase price x CBS dwelling price index now / index in the purchase month (the district series, from 10.2017; the
         national series 40010 before that or where the settlement has no district);
     3 = purchase price x official median now / official median in the purchase quarter (same place and rooms; the city when the
         neighbourhood has no median in that quarter).
   Checks 2 and 3 are rounded to 100 ₪ (the official medians are). The adjusted estimate stays the answer. Figures: I1, the 22
   quarters of the place against Israel; I3, the checks on one scale, the shaded range between them and the asking price as a
   stamp-red pin. Palette: survey and land-registry paper (registry blue, graphite grid on white, stamp red only for the pin),
   numbers in IBM Plex Mono. SVG in RTL: text-anchor start = the right end of a label.
   Data: value.json (latest quarter, tools/instruments/build_value_data.py, Yavne added by build_value_series.py) and
   value-series.json (key vseries: 22 quarters, CBS 40010 and 60000 to 60500, settlement -> district; build_value_series.py).
   Without value-series.json the tool runs exactly as v1. Pure logic in NLPV for checks (tools/instruments/test_pval_math.py). */
(function () {
  'use strict';
  var KIND = { apt: 'דירה', garden: 'דירת גן', penthouse: 'פנטהאוז', house: 'בית פרטי' };
  var MONTHS = ['ינואר', 'פברואר', 'מרץ', 'אפריל', 'מאי', 'יוני', 'יולי', 'אוגוסט', 'ספטמבר', 'אוקטובר', 'נובמבר', 'דצמבר'];
  /** The official series exist for 3, 4 and 5 rooms: 2 uses 3, 6 uses 5. */
  function sr(n) { n = Math.round(+n || 4); return n < 3 ? 3 : n > 5 ? 5 : n; }
  function base(v, d) {
    var c = d.cities[v.city]; if (!c) return null;
    var h = null; c.hoods.forEach(function (x) { if (String(x.id) === String(v.hood)) h = x; });
    var n = sr(v.rooms), k = 'r' + n, fb = n !== Math.round(+v.rooms) ? n : 0;
    if (h && h[k]) return { price: h[k][0], q: h[k][1], where: h.n, level: 'hood', rk: k, n: n, fb: fb, id: h.id };
    if (c[k]) return { price: c[k], q: c['q' + n] || c.q, where: v.city, level: 'city', hood: h ? h.n : '', rk: k, n: n, fb: fb, id: h ? h.id : null };
    return null;
  }
  function compute(v, d) {
    var b = v.method === 'sqm' ? { price: (v.sqm || 0) * (v.ppsqm || 0) + (v.balcony || 0) * (v.balconyPrice || 0) + (v.parking || 0) + (v.storage || 0), level: 'sqm' } : base(v, d);
    if (!b || !(b.price > 0)) return null;
    var val = b.price * (1 + ((v.condition || 0) + (v.building || 0)) / 100), r = Math.max(0, v.range || 0) / 100;
    return { b: b, value: val, low: val * (1 - r), high: val * (1 + r), ppsqm: v.sqm > 0 ? val / v.sqm : 0, gap: v.asking > 0 ? (v.asking - val) / val : null };
  }
  // ---- v2: months, quarters, the three checks
  function mIdx(key) { var p = String(key).split('-'); return (+p[0]) * 12 + (+p[1]) - 1; }
  function mKey(i) { var m = i % 12 + 1; return Math.floor(i / 12) + '-' + (m < 10 ? '0' : '') + m; }
  function qOf(y, m) { var e = Math.ceil(m / 3) * 3; return (e - 2) + '-' + e + '.' + y; }   // "1-3.2021", the label of the official files
  function qNum(label) { var p = String(label).split('.'); return (+p[1]) * 4 + (+String(p[0]).split('-')[1]) / 3 - 1; }
  function r100(x) { return Math.round(x / 100) * 100; }
  function cbsAt(s, key) { var i = mIdx(key) - mIdx(s.from); return i >= 0 && i < s.v.length ? s.v[i] : null; }
  function cbsEnd(s) { return mKey(mIdx(s.from) + s.v.length - 1); }
  function bought(v) { return v.bought > 0 && v.buyY && v.buyM ? { key: v.buyY + '-' + ('0' + v.buyM).slice(-2), q: qOf(+v.buyY, +v.buyM) } : null; }
  /** Check 2: purchase price x CBS dwelling price index now / index in the purchase month. */
  function idxCheck(v, S) {
    var p = bought(v); if (!p) return null;
    if (!S || !S.cbs) return { miss: 'nodata' };
    var C = S.cbs.s, meta = (S.city && S.city[v.city]) || {}, ds = meta.cbs ? C[String(meta.cbs)] : null, nat = C['40010'];
    var useD = !!(ds && cbsAt(ds, p.key) != null), s = useD ? ds : nat, end = cbsEnd(s);
    if (mIdx(p.key) > mIdx(end)) return { miss: 'late', key: p.key, end: end };
    var then = cbsAt(s, p.key); if (then == null) return { miss: 'early', key: p.key, from: nat.from };
    var now = s.v[s.v.length - 1], raw = v.bought * now / then;
    return { value: r100(raw), raw: raw, ratio: now / then, sid: useD ? String(meta.cbs) : '40010', name: s.n, from: p.key, to: end, then: then, now: now,
      district: useD, why: useD ? '' : (ds ? 'early' : 'none'), distFrom: ds ? ds.from : null };
  }
  /** Check 3: purchase price x official median now / official median in the purchase quarter (same place and room series). */
  function medCheck(v, d, S, A) {
    var p = bought(v); if (!p) return null;
    if (!S || !S.q) return { miss: 'nodata' };
    if (!A) return { miss: 'noA' };
    var Q = S.q, qi = Q.indexOf(p.q);
    if (qi < 0) return { miss: qNum(p.q) < qNum(Q[0]) ? 'early' : 'late', q: p.q, first: Q[0] };
    var k = A.rk, c = d.cities[v.city], cs = ((S.city || {})[v.city] || {})[k], cityNow = c['q' + A.n] || c.q;
    var hs = A.level === 'hood' ? ((S.hood || {})[String(A.id)] || {})[k] : null, hn = Q.indexOf(A.q);
    var lvl = hs && hs[qi] && hn >= 0 && hs[hn] ? 'hood' : (cs && cs[qi] ? 'city' : null);
    if (!lvl) return { miss: 'noq', q: p.q, n: A.n, where: v.city };
    var s = lvl === 'hood' ? hs : cs, ni = lvl === 'hood' ? hn : Q.indexOf(cityNow);
    if (ni < 0 || !s[ni]) return { miss: 'nonow', q: p.q };
    if (ni < qi) return { miss: 'late', q: p.q, first: Q[0] };
    var raw = v.bought * s[ni] / s[qi];
    return { value: r100(raw), raw: raw, ratio: s[ni] / s[qi], level: lvl, q: p.q, nowQ: Q[ni], then: s[qi], now: s[ni], where: lvl === 'hood' ? A.where : v.city, fell: A.level === 'hood' && lvl === 'city' };
  }
  /** All anchors: 1 (A), 2 (B), 3 (C) official, D the adjusted estimate; the range between the official checks; the asking price on it. */
  function anchors(v, d, S) {
    var A = base(Object.assign({}, v, { method: 'deals' }), d), r = compute(v, d), B = idxCheck(v, S), C = medCheck(v, d, S, A);
    var off = [];
    if (A) off.push(A.price);
    if (B && B.value) off.push(B.value);
    if (C && C.value) off.push(C.value);
    var lo = off.length ? Math.min.apply(null, off) : null, hi = off.length ? Math.max.apply(null, off) : null;
    var ask = null;
    if (v.asking > 0 && off.length > 1) ask = v.asking < lo ? { pos: 'below', d: (v.asking - lo) / lo } : v.asking > hi ? { pos: 'above', d: (v.asking - hi) / hi } : { pos: 'in', d: (v.asking - lo) / lo };
    return { A: A, B: B, C: C, D: r ? r.value : null, r: r, n: off.length, lo: lo, hi: hi, spread: off.length > 1 ? (hi - lo) / lo : null, ask: ask };
  }
  window.NLPV = { base: base, compute: compute, anchors: anchors, idxCheck: idxCheck, medCheck: medCheck, qOf: qOf, sr: sr };
  if (!window.NadLanInstruments) return;
  var NI = window.NadLanInstruments, F = NI.fmt, esc = NI.esc;

  // ---- the drawings: survey and land-registry paper
  var P = { ink: '#16263A', reg: '#1D4E89', regL: '#DCE6F2', grid: '#D7DCE1', graph: '#4A525B', mute: '#5B6570', red: '#C8102E', paper: '#FFFFFF' };
  var MONO = "'IBM Plex Mono',ui-monospace,monospace", SANS = "'IBM Plex Sans Hebrew','IBM Plex Sans',system-ui,sans-serif";
  function T(x, y, s, o) {
    o = o || {};
    return '<text x="' + (+x).toFixed(1) + '" y="' + (+y).toFixed(1) + '" text-anchor="' + (o.a || 'start') + '" style="font:' + (o.w || 400) + ' ' + (o.s || 13) + 'px ' + (o.m ? MONO : SANS)
      + ';fill:' + (o.f || P.ink) + (o.m ? ';font-variant-numeric:tabular-nums' : '') + '">' + esc(s) + '</text>';
  }
  function L(x1, y1, x2, y2, col, w, dash) { return '<line x1="' + x1.toFixed(1) + '" y1="' + y1.toFixed(1) + '" x2="' + x2.toFixed(1) + '" y2="' + y2.toFixed(1) + '" stroke="' + col + '" stroke-width="' + (w || 1) + '"' + (dash ? ' stroke-dasharray="' + dash + '"' : '') + '/>'; }
  function frame(W, H, aria, body) {
    return '<svg viewBox="0 0 ' + W + ' ' + H + '" direction="rtl" role="img" aria-label="' + esc(aria) + '" style="display:block;width:100%;height:auto;max-width:560px;margin:0 0 10px">'
      + '<rect x="0.5" y="0.5" width="' + (W - 1) + '" height="' + (H - 1) + '" fill="' + P.paper + '" stroke="' + P.grid + '"/>' + body + '</svg>';
  }
  function step(span, n) { var raw = span / n, p = Math.pow(10, Math.floor(Math.log(raw) / Math.LN10)), m = raw / p; return (m <= 1 ? 1 : m <= 2 ? 2 : m <= 2.5 ? 2.5 : m <= 5 ? 5 : 10) * p; }
  function mil(v, st) { return F.num(v / 1e6, st >= 1e6 ? 0 : st % 1e5 === 0 ? 1 : 2); }
  function pc(x, d) { return (x > 0 ? '+' : x < 0 ? '−' : '') + F.num(Math.abs(100 * x), d == null ? 1 : d) + '%'; }
  function iso(s) { return '\u2066' + s + '\u2069'; }                         // LRI ... PDI: "+29.5%" keeps its sign on the left inside a Hebrew label
  function nb(q) { return String(q).replace(/-/g, '\u2060-\u2060'); }         // word joiners: "1-3.2026" never breaks at its hyphen

  /** I1: 22 quarters of the official median, the place against Israel, nulls left as gaps; the purchase quarter and price marked. */
  function figLine(o) {
    var W = 420, pl = 42, pr = 14, pt = 54, ph = 150, n = o.q.length, gapC = '#8FA8C8', hasGap = false;
    var vals = o.a.concat(o.b).filter(function (x) { return x > 0; }); if (o.bought > 0 && o.bi >= 0) vals.push(o.bought);
    if (!vals.length || n < 2) return '';
    var lo = Math.min.apply(null, vals), hi = Math.max.apply(null, vals), st = step((hi - lo) || hi * 0.2, 4);
    var y0 = Math.floor(lo / st) * st, y1 = Math.ceil(hi / st) * st; if (y1 <= y0) y1 = y0 + st;
    var X = function (i) { return pl + (W - pl - pr) * i / (n - 1); }, Y = function (v) { return pt + ph - ph * (v - y0) / (y1 - y0); };
    var g = [T(W - 12, 22, o.title, { w: 600, s: 14 }), T(12, 22, 'מיליון ₪', { a: 'end', s: 12, f: P.mute })];
    for (var v = y0; v <= y1 + st / 2; v += st) { var y = Y(v); g.push(L(pl, y, W - pr, y, P.grid, 1)); g.push(T(pl - 6, y + 4, mil(v, st), { m: true, s: 12, f: P.graph })); }
    o.q.forEach(function (q, i) { if (/^1-3\./.test(q)) { g.push(L(X(i), pt + ph, X(i), pt + ph + 5, P.graph, 1)); g.push(T(X(i), pt + ph + 19, q.split('.')[1], { a: 'middle', m: true, s: 12, f: P.graph })); } });
    // a quarter with no published median stays a gap: the real points carry dots, a faint dotted line only bridges the gap
    function path(arr, col, w, dash, bridge) {
      var d = '', on = false, dots = '', gaps = '', prev = -1;
      arr.forEach(function (x, i) {
        if (x > 0) {
          if (bridge && prev >= 0 && prev < i - 1) { gaps += L(X(prev), Y(arr[prev]), X(i), Y(x), gapC, 1.4, '1.5 3.5'); hasGap = true; }
          d += (on ? 'L' : 'M') + X(i).toFixed(1) + ' ' + Y(x).toFixed(1);
          if (bridge || (!(arr[i - 1] > 0) && !(arr[i + 1] > 0))) dots += '<circle cx="' + X(i).toFixed(1) + '" cy="' + Y(x).toFixed(1) + '" r="' + (bridge ? 2.4 : 2.6) + '" fill="' + col + '"/>';
          on = true; prev = i;
        } else on = false;
      });
      return gaps + (d ? '<path d="' + d + '" fill="none" stroke="' + col + '" stroke-width="' + w + '" stroke-linejoin="round" stroke-linecap="round"' + (dash ? ' stroke-dasharray="' + dash + '"' : '') + '/>' : '') + dots;
    }
    g.push(path(o.b, P.graph, 1.6, '5 4'));
    g.push(path(o.a, P.reg, 2.4, '', true));
    var la = -1; o.a.forEach(function (x, i) { if (x > 0) la = i; });
    if (la >= 0) g.push('<circle cx="' + X(la).toFixed(1) + '" cy="' + Y(o.a[la]).toFixed(1) + '" r="4" fill="' + P.reg + '" stroke="#fff" stroke-width="1.5"/>');
    if (o.bi >= 0) {
      g.push(L(X(o.bi), pt - 6, X(o.bi), pt + ph, P.graph, 1, '2 3'));
      g.push(T(X(o.bi) < pl + 30 ? X(o.bi) - 4 : X(o.bi), pt - 10, 'קנייה', { a: X(o.bi) < pl + 30 ? 'end' : 'middle', s: 12, f: P.graph }));
      if (o.bought > 0) g.push('<circle cx="' + X(o.bi).toFixed(1) + '" cy="' + Y(o.bought).toFixed(1) + '" r="5" fill="#fff" stroke="' + P.reg + '" stroke-width="2"/>');
    }
    var ly = pt + ph + 44, rows = [];
    rows.push(['<line x1="' + (W - 38) + '" x2="' + (W - 14) + '" stroke="' + P.reg + '" stroke-width="2.4"/>', o.aName]);
    rows.push(['<line x1="' + (W - 38) + '" x2="' + (W - 14) + '" stroke="' + P.graph + '" stroke-width="1.6" stroke-dasharray="5 4"/>', o.bName]);
    if (o.bi >= 0 && o.bought > 0) rows.push(['<circle cx="' + (W - 26) + '" r="5" fill="#fff" stroke="' + P.reg + '" stroke-width="2"/>', o.buyName]);
    if (hasGap) rows.push(['<line x1="' + (W - 38) + '" x2="' + (W - 14) + '" stroke="' + gapC + '" stroke-width="1.4" stroke-dasharray="1.5 3.5"/>', 'מנוקד: רבעונים שלא פורסם בהם חציון']);
    rows.forEach(function (r, i) { var y = ly + i * 20; g.push('<g transform="translate(0 ' + (y - 4) + ')">' + r[0] + '</g>'); g.push(T(W - 46, y, r[1], { s: 12.5 })); });
    return frame(W, ly + rows.length * 20 - 6, o.aria, g.join(''));
  }

  /** I3: the official checks (numbered, registry blue), the adjusted estimate (graphite diamond), the shaded range between the
      checks and the asking price as a stamp-red pin, on one horizontal scale; a legend with every value and its date. */
  function figScale(o) {
    var W = 420, pl = 26, pr = 26, vals = o.items.map(function (x) { return x.value; }); if (o.ask > 0) vals.push(o.ask);
    var lo = Math.min.apply(null, vals), hi = Math.max.apply(null, vals), span = hi - lo, pad = Math.max(span * 0.12, hi * 0.03);
    var st = step(span + 2 * pad, 4), x0 = Math.floor((lo - pad) / st) * st, x1 = Math.ceil((hi + pad) / st) * st;
    var X = function (v) { return pl + (W - pl - pr) * (v - x0) / (x1 - x0); };
    var placed = [], maxL = 0;  // markers closer than 22 px stack upward, one row each
    o.items.slice().sort(function (a, b) { return a.value - b.value; }).forEach(function (it) {
      var x = X(it.value), lv = 0;
      while (placed.some(function (p) { return p.l === lv && Math.abs(p.x - x) < 22; })) lv++;
      placed.push({ x: x, l: lv, it: it }); maxL = Math.max(maxL, lv);
    });
    var sy = 46 + (o.ask > 0 ? 30 : 0) + maxL * 24;
    var g = [T(W - 12, 22, o.title, { w: 600, s: 14 }), T(12, 22, 'מיליון ₪', { a: 'end', s: 12, f: P.mute })];
    if (o.rlo != null && o.rhi > o.rlo) g.push('<rect x="' + X(o.rlo).toFixed(1) + '" y="' + (sy - 8) + '" width="' + (X(o.rhi) - X(o.rlo)).toFixed(1) + '" height="16" fill="' + P.regL + '" stroke="' + P.reg + '" stroke-width="1"/>');
    g.push(L(pl, sy, W - pr, sy, P.graph, 1.5));
    for (var v = x0; v <= x1 + st / 2; v += st) { g.push(L(X(v), sy, X(v), sy + 6, P.graph, 1)); g.push(T(X(v), sy + 22, mil(v, st), { a: 'middle', m: true, s: 12, f: P.graph })); }
    if (o.ask > 0) {
      var ax = X(o.ask), left = ax > W / 2;
      g.push(L(ax, 46, ax, sy + 10, P.red, 2));
      g.push('<circle cx="' + ax.toFixed(1) + '" cy="44" r="6" fill="' + P.red + '"/>');
      g.push(T(left ? ax - 11 : ax + 11, 48, 'המחיר המבוקש', { a: left ? 'start' : 'end', s: 12.5, w: 600, f: P.red }));
    }
    placed.forEach(function (p) { if (p.l) g.push(L(p.x, sy - p.l * 24, p.x, sy, P.graph, 1)); });
    placed.forEach(function (p) {
      var it = p.it, x = p.x, cy = sy - p.l * 24;
      if (it.est) g.push('<rect x="' + (x - 6.5).toFixed(1) + '" y="' + (cy - 6.5) + '" width="13" height="13" transform="rotate(45 ' + x.toFixed(1) + ' ' + cy + ')" fill="#fff" stroke="' + P.graph + '" stroke-width="2"/>');
      else g.push('<circle cx="' + x.toFixed(1) + '" cy="' + cy + '" r="9.5" fill="' + P.reg + '"/>' + T(x, cy + 4.5, it.k, { a: 'middle', m: true, s: 12, w: 600, f: '#fff' }));
    });
    var ly = sy + 50, rows = o.items.map(function (it) {
      return { sym: it.est ? '<rect x="-6" y="-6" width="12" height="12" transform="rotate(45)" fill="#fff" stroke="' + P.graph + '" stroke-width="2"/>' : '<circle r="9" fill="' + P.reg + '"/>' + T(0, 4.3, it.k, { a: 'middle', m: true, s: 12, w: 600, f: '#fff' }), label: it.label, value: F.ils(it.value) };
    });
    if (o.rlo != null && o.rhi > o.rlo) rows.push({ sym: '<rect x="-9" y="-6" width="18" height="12" fill="' + P.regL + '" stroke="' + P.reg + '"/>', label: o.rangeLabel, value: o.rangeValue });
    if (o.ask > 0) rows.push({ sym: '<circle r="6" fill="' + P.red + '"/>', label: 'המחיר המבוקש', value: F.ils(o.ask), red: true });
    rows.forEach(function (r, i) {
      var y = ly + i * 22;
      g.push('<g transform="translate(' + (W - 22) + ' ' + (y - 4) + ')">' + r.sym + '</g>');
      g.push(T(W - 40, y, r.label, { s: 12.5, f: r.red ? P.red : P.ink }));
      g.push(T(12, y, r.value, { a: 'end', m: true, s: 13, w: 500, f: r.red ? P.red : P.ink }));
    });
    return frame(W, ly + rows.length * 22 - 6, o.aria, g.join(''));
  }

  function presets(dd) {
    var S = dd.vseries; if (!S || !S.city || !S.q) return [];
    var out = [], q21 = S.q.indexOf('1-3.2021');
    var yv = S.city['יבנה'], ta = S.city['תל אביב יפו'];
    if (yv && yv.r4 && yv.r4[q21] && dd.value.cities['יבנה']) out.push({ key: 'yavne21', label: 'יבנה, נקנתה ב־2021', sub: '4 חדרים, במחיר החציוני של ' + nb('1-3.2021'),
      set: { method: 'deals', city: 'יבנה', hood: '', rooms: 4, kind: 'apt', buyY: '2021', buyM: '3', bought: yv.r4[q21], asking: 0, condition: 0, building: 0, range: 5 } });
    var t22 = S.q.indexOf('4-6.2022');
    if (ta && ta.r4 && ta.r4[t22]) out.push({ key: 'tlv22', label: 'תל אביב, עם מחיר מבוקש', sub: '4 חדרים, נקנתה ב־6.2022, מחיר מבוקש לדוגמה',
      set: { method: 'deals', city: 'תל אביב יפו', hood: '', rooms: 4, kind: 'apt', buyY: '2022', buyM: '6', bought: ta.r4[t22], asking: 5900000, condition: 0, building: 0, range: 5 } });
    var bh = (S.hood || {})['65209775'], q22 = S.q.indexOf('1-3.2022');
    if (bh && bh.r4 && bh.r4[q22] && dd.value.cities['ירושלים']) out.push({ key: 'bhk22', label: 'בית הכרם, ירושלים', sub: '4 חדרים, נקנתה ב־2.2022 בחציון השכונה',
      set: { method: 'deals', city: 'ירושלים', hood: '65209775', rooms: 4, kind: 'apt', buyY: '2022', buyM: '2', bought: bh.r4[q22], asking: 0, condition: 0, building: 0, range: 5 } });
    return out;
  }

  NI.register('pval', {
    kicker: 'מחשבון · שווי דירה',
    title: 'כמה שווה הדירה',
    lede: 'עיר, שכונה ומספר חדרים: המחשבון מתחיל מהמחיר החציוני של העסקאות שנסגרו בשכונה לפי רשות המסים, מוסיף את ההתאמות שלכם, ובודק מחיר מבוקש. אפשר לעבור גם לחישוב לפי מחיר למ״ר. מי שמזין גם מתי קנה ובכמה מקבל שלוש בדיקות רשמיות זו לצד זו: החציון היום, מדד מחירי הדירות של הלמ״ס במחוז, והחציון מאז הקנייה.',
    strip: function (dd) {
      var d = dd.value, c = d.cities['תל אביב יפו'], S = dd.vseries;
      var s = [{ label: 'ערים', value: F.num(Object.keys(d.cities).length) }, { label: 'שכונות', value: F.num(Object.keys(d.cities).reduce(function (s, k) { return s + d.cities[k].hoods.length; }, 0)) }, { label: '4 חדרים, תל אביב, ' + (c.q4 || c.q), value: F.ils(c.r4) }];
      if (S && S.cbs && S.cbs.s['40010']) { var n = S.cbs.s['40010'], e = n.v[n.v.length - 1], y = n.v[n.v.length - 13]; if (y) s.push({ label: 'מדד מחירי הדירות, שנה עד ' + F.month(S.cbs.latest), value: pc(e / y - 1) }); }
      return s;
    },
    presets: presets,
    defaults: function () { return { method: 'deals', city: 'תל אביב יפו', hood: '', rooms: 4, sqm: 100, ppsqm: 50000, balcony: 0, balconyPrice: 0, parking: 0, storage: 0, condition: 0, building: 0, range: 5, asking: 0, kind: 'apt', buyY: '', buyM: '', bought: 0 }; },
    fields: [
      { id: 'method', label: 'איך מחשבים', type: 'segmented', options: [{ value: 'deals', label: 'לפי עסקאות בשכונה' }, { value: 'sqm', label: 'לפי מחיר למ״ר' }] },
      { id: 'city', label: 'עיר', type: 'select', optionsFrom: function (v, d) { return Object.keys(d.value.cities).sort().map(function (k) { return { value: k, label: k }; }); } },
      { id: 'hood', label: 'שכונה', type: 'select', optionsFrom: function (v, d) {
          var c = d.value.cities[v.city]; var k = 'r' + sr(v.rooms);
          return [{ value: '', label: 'כל העיר' }].concat((c ? c.hoods : []).map(function (h) { return { value: String(h.id), label: h.n + (h[k] ? '' : ' (חציון העיר)') }; })); } },
      { id: 'kind', label: 'סוג הנכס', type: 'segmented', options: [{ value: 'apt', label: 'דירה' }, { value: 'garden', label: 'דירת גן' }, { value: 'penthouse', label: 'פנטהאוז' }, { value: 'house', label: 'בית פרטי' }],
        help: 'החציון הרשמי מתפרסם לדירות לפי מספר חדרים, בלי הפרדה לפי סוג.' },
      { id: 'rooms', label: 'חדרים', type: 'segmented', options: [{ value: 2, label: '2' }, { value: 3, label: '3' }, { value: 4, label: '4' }, { value: 5, label: '5' }, { value: 6, label: '6' }],
        help: 'ל־2 ול־6 חדרים אין סדרה רשמית; מוצגת הקרובה, 3 או 5.' },
      { id: 'sqm', label: 'שטח הדירה', type: 'number', unit: 'מ״ר' },
      { id: 'ppsqm', label: 'מחיר ממוצע למ״ר באזור', type: 'money', unit: '₪', showIf: function (v) { return v.method === 'sqm'; } },
      { id: 'balcony', label: 'שטח מרפסת', type: 'number', unit: 'מ״ר', showIf: function (v) { return v.method === 'sqm'; } },
      { id: 'balconyPrice', label: 'שווי למ״ר מרפסת', type: 'money', unit: '₪', showIf: function (v) { return v.method === 'sqm'; } },
      { id: 'parking', label: 'שווי חניה', type: 'money', unit: '₪', showIf: function (v) { return v.method === 'sqm'; } },
      { id: 'storage', label: 'שווי מחסן', type: 'money', unit: '₪', showIf: function (v) { return v.method === 'sqm'; } },
      { id: 'condition', label: 'התאמה למצב הדירה', type: 'percent', unit: '%', help: 'למשל +5 לדירה משופצת, −10 לדירה שדורשת שיפוץ. ההחלטה שלכם.' },
      { id: 'building', label: 'התאמה לקומה, נוף ובניין', type: 'percent', unit: '%' },
      { id: 'range', label: 'טווח זהירות', type: 'percent', unit: '±%' },
      { id: 'buyY', label: 'שנת הקנייה', type: 'select', help: 'לא חובה. עם החודש ומחיר הקנייה מקבלים עוד שתי בדיקות רשמיות.', optionsFrom: function (v, d) {
          var S = d.vseries, o = [{ value: '', label: 'בלי בדיקה לפי הקנייה' }]; if (!S || !S.cbs) return o;
          var last = +String(S.cbs.latest).slice(0, 4), first = +String(S.cbs.s['40010'].from).slice(0, 4);
          for (var y = last; y >= first; y--) o.push({ value: String(y), label: String(y) });
          return o; } },
      { id: 'buyM', label: 'חודש הקנייה', type: 'select', showIf: function (v) { return !!v.buyY; }, options: [{ value: '', label: 'בחרו חודש' }].concat(MONTHS.map(function (m, i) { return { value: String(i + 1), label: m }; })) },
      { id: 'bought', label: 'מחיר הקנייה', type: 'money', unit: '₪', showIf: function (v) { return !!v.buyY; }, help: 'המחיר בחוזה הרכישה.' },
      { id: 'asking', label: 'מחיר מבוקש לבדיקה', type: 'money', unit: '₪', help: '0 אם אין מחיר לבדוק.' }
    ],
    compute: function (v, d) {
      var D = d.value, S = d.vseries, r = compute(v, D);
      if (!r) return { error: { field: v.method === 'sqm' ? 'ppsqm' : 'hood', msg: v.method === 'sqm' ? 'הקלידו שטח ומחיר למ״ר.' : 'אין חציון פורסם למספר החדרים הזה. נסו מספר חדרים אחר.' } };
      var X = anchors(v, D, S), A = X.A, B = X.B, C = X.C, b = r.b, lines = [], buy = !!v.buyY, two = buy && (B && B.value || C && C.value);
      var roomsTxt = function (x) { return x.n + ' חדרים' + (x.fb ? ' (במקום ' + Math.round(+v.rooms) + ')' : ''); };
      var aLabel = function (x) { return 'חציון ' + roomsTxt(x) + ', ' + x.where + ', ' + nb(x.q) + (x.level === 'city' && x.hood ? ' (לשכונה אין חציון שפורסם)' : ''); };
      if (b.level === 'hood' || b.level === 'city') lines.push({ label: (two ? 'בדיקה 1 · ' : '') + aLabel(b), value: F.ils(b.price) });
      else {
        lines.push({ label: 'שטח × מחיר למ״ר, מרפסת, חניה ומחסן', value: F.ils(b.price) });
        if (A) lines.push({ label: (two ? 'בדיקה 1 · ' : 'להשוואה: ') + aLabel(A), value: F.ils(A.price) });
      }
      if (B && B.value) lines.push({ label: 'בדיקה 2 · מחיר הקנייה לפי מדד מחירי הדירות, ' + (B.district ? B.name : 'כל הארץ') + ', ' + F.month(B.from) + ' עד ' + F.month(B.to) + ' (' + iso(pc(B.ratio - 1)) + ')', value: F.ils(B.value) });
      if (C && C.value) lines.push({ label: 'בדיקה 3 · מחיר הקנייה לפי חציון ' + roomsTxt(A) + ', ' + C.where + ', ' + nb(C.q) + ' עד ' + nb(C.nowQ) + ' (' + iso(pc(C.ratio - 1)) + ')', value: F.ils(C.value) });
      if (v.condition || v.building) lines.push({ label: 'ההתאמות שלכם', value: ((v.condition || 0) + (v.building || 0) > 0 ? '+' : '') + F.num((v.condition || 0) + (v.building || 0), 1) + '%' });
      if (r.ppsqm) lines.push({ label: 'מחיר למ״ר שיוצא', value: F.ils(r.ppsqm) });
      if (r.gap != null) lines.push({ label: 'המחיר המבוקש מול השווי', value: (r.gap > 0 ? '+' : '−') + F.num(Math.abs(100 * r.gap), 1) + '%' });
      if (X.n > 1) {
        lines.push({ label: 'הבדיקה הנמוכה', value: F.ils(X.lo) }, { label: 'הבדיקה הגבוהה', value: F.ils(X.hi) }, { label: 'פער בין הבדיקות הרשמיות', value: F.num(100 * X.spread, 1) + '%' });
        if (X.ask) lines.push({ label: X.ask.pos === 'above' ? 'המחיר המבוקש מעל הבדיקה הגבוהה' : X.ask.pos === 'below' ? 'המחיר המבוקש מתחת לבדיקה הנמוכה' : 'המחיר המבוקש בתוך הטווח, מעל הנמוכה', value: pc(X.ask.d) });
      }
      var note = r.gap == null ? 'חציון הוא המחיר שחצי מהעסקאות מעליו וחצי מתחתיו. הוא כולל דירות חדשות וישנות, ולא מחליף שמאי.'
        : r.gap > 0.08 ? '<b>המחיר המבוקש גבוה משמעותית מהשווי.</b> כדאי לבדוק מה מצדיק את הפער: קומה, נוף, מצב או חניה.'
        : r.gap < -0.08 ? '<b>המחיר המבוקש נמוך משמעותית מהשווי.</b> כדאי לבדוק למה: מצב הדירה, זכויות, ליקויים או רישום.'
        : 'המחיר המבוקש קרוב לשווי לפי הנתונים.';
      var more = [];
      var fbx = A || (b.level !== 'sqm' ? b : null);
      if (fbx && fbx.fb) more.push('אין סדרה רשמית ל־' + Math.round(+v.rooms) + ' חדרים; מוצג חציון ' + fbx.n + ' חדרים, הסדרה הקרובה.');
      if (v.kind === 'garden') more.push('דירת גן: החציון הרשמי הוא של כל הדירות במספר החדרים הזה, בלי הפרדה לפי סוג. את התוספת של הגינה מזינים בהתאמה לקומה, נוף ובניין.');
      else if (v.kind === 'penthouse') more.push('פנטהאוז: החציון הרשמי הוא של כל הדירות במספר החדרים הזה, בלי הפרדה לפי סוג. מרפסת הגג, הקומה והנוף נכנסים בהתאמות שלכם.');
      else if (v.kind === 'house') more.push('<b>בית פרטי:</b> החציון הרשמי הוא של דירות בלבד, ומדד הלמ״ס הוא מדד מחירי דירות. בבית פרטי המגרש והזכויות בו קובעים חלק גדול מהשווי, ולכן הבדיקות כאן הן נקודת השוואה בלבד. כדאי לחשב גם לפי מחיר למ״ר ולהתייעץ עם שמאי.');
      if (buy) {
        if (!v.buyM) more.push('בחרו את חודש הקנייה כדי לקבל את בדיקות 2 ו־3.');
        else if (!(v.bought > 0)) more.push('הקלידו את מחיר הקנייה כדי לקבל את בדיקות 2 ו־3.');
      }
      if (B && B.miss) more.push(B.miss === 'late' ? 'אין בדיקה 2: חודש הקנייה אחרי ' + esc(F.month(B.end)) + ', החודש האחרון שפרסמה הלמ״ס.' : B.miss === 'early' ? 'אין בדיקה 2: מדד מחירי הדירות מתחיל ב־' + esc(F.month(B.from)) + '.' : 'אין בדיקה 2: נתוני המדד לא נטענו.');
      if (B && B.value && !B.district) more.push(B.why === 'early' ? 'מדד המחוזות של הלמ״ס מתחיל ב־' + esc(F.month(B.distFrom)) + ', ולכן בדיקה 2 לפי מדד כל הארץ.' : 'ליישוב הזה אין מחוז במדד של הלמ״ס, ולכן בדיקה 2 לפי מדד כל הארץ.');
      if (C && C.miss) more.push(C.miss === 'early' ? 'אין בדיקה 3: הסדרה הרשמית של החציונים מתחילה ב־' + esc(C.first) + '.' : C.miss === 'late' ? 'אין בדיקה 3: לרבעון הקנייה עדיין לא פורסם חציון.' : C.miss === 'noq' ? 'אין בדיקה 3: לא פורסם חציון ל־' + esc(C.n) + ' חדרים ב' + esc(C.where) + ' ברבעון ' + esc(C.q) + '.' : C.miss === 'noA' ? 'אין בדיקה 3: אין חציון רשמי היום למספר החדרים הזה.' : 'אין בדיקה 3: נתוני החציונים לא נטענו.');
      if (C && C.fell) more.push('אין חציון לשכונה ברבעון הקנייה, ולכן בדיקה 3 לפי חציון העיר.');
      if (X.spread != null && X.spread > 0.1) more.push('<b>הבדיקות רחוקות זו מזו, פער של ' + esc(F.num(100 * X.spread, 1)) + '%.</b> חציון של רבעון אחד זז עם תמהיל העסקאות באותו רבעון, למשל כשנמכרו בו יותר דירות חדשות, ומדד הלמ״ס מודד את השינוי במחוז כולו ולא בשכונה. כדאי לבדוק עסקאות דומות ברחוב באתר נדל״ן הממשלתי.');
      if (B && B.value) more.push('ערכי המדד של הלמ״ס לחודשים האחרונים זמניים ומתעדכנים מדי חודש.');
      more.push('הערכה ראשונית, לא חוות דעת שמאית.');
      note += ' ' + more.join(' ');  // every data part above went through esc(); the only tags are <b>
      var out = {
        answer: { label: 'שווי משוער', value: F.ils(r.value), tone: 'survey', sub: F.ils(r.low) + ' עד ' + F.ils(r.high) + ' · טווח ±' + F.num(v.range || 0) + '%' },
        breakdown: [{ label: 'מחיר בסיס', value: Math.min(b.price, r.value), kind: 'housing' }, { label: 'תוספת מההתאמות', value: Math.max(0, r.value - b.price), kind: 'open' }],
        lines: lines, note: note,
        formula: (v.method === 'sqm' ? 'שווי = (שטח × מחיר למ״ר + מרפסת × מחיר למ״ר מרפסת + חניה + מחסן) × (1 + ההתאמות). הטווח: ± טווח הזהירות.' : 'שווי = החציון הרשמי לפי מספר החדרים × (1 + ההתאמות). הטווח: ± טווח הזהירות.')
          + (buy ? ' בדיקה 2 = מחיר הקנייה × מדד מחירי הדירות בחודש האחרון ÷ המדד בחודש הקנייה. בדיקה 3 = מחיר הקנייה × החציון ברבעון האחרון ÷ החציון ברבעון הקנייה, באותו מקום ובאותו מספר חדרים. שתיהן מעוגלות ל־100 ₪.' : ''),
        sources: [{ label: D.source + ', קובץ ' + D.file + ', נקרא ' + F.date(D.read), url: D.url }],
        text: 'שווי משוער: ' + F.ils(r.value) + ' (' + F.ils(r.low) + ' עד ' + F.ils(r.high) + ')' + (b.level !== 'sqm' ? ', ' + v.rooms + ' חדרים, ' + b.where : '') + '.'
      };
      if (S && S.q) out.sources.push({ label: 'אותם קבצים, 22 רבעונים (' + S.q[0] + ' עד ' + S.q[S.q.length - 1] + '), נקרא ' + F.date(S.read), url: S.url });
      if (B && B.value) {
        out.sources.push({ label: S.cbs.source + ', סדרה ' + B.sid + ', עד ' + F.month(S.cbs.latest) + ', נקרא ' + F.date(S.cbs.read), url: S.cbs.url });
        if (B.district) out.sources.push({ label: S.loc.source, url: 'https://data.gov.il/' });
      }
      if (two) out.text += (B && B.value ? ' לפי מדד מחירי הדירות (' + F.month(B.from) + ' עד ' + F.month(B.to) + '): ' + F.ils(B.value) + '.' : '') + (C && C.value ? ' לפי החציון מאז הקנייה (' + C.q + ' עד ' + C.nowQ + '): ' + F.ils(C.value) + '.' : '') + ' הערכה ראשונית, לא חוות דעת שמאית.';
      // the drawings
      var figs = [];
      if (A || b.level !== 'sqm') {
        var items = [];
        if (A) items.push({ k: '1', value: A.price, label: 'חציון רשמי היום, ' + A.q });
        if (B && B.value) items.push({ k: '2', value: B.value, label: 'מדד ' + (B.district ? B.name : 'כל הארץ') + ', ' + F.month(B.from) + ' עד ' + F.month(B.to) });
        if (C && C.value) items.push({ k: '3', value: C.value, label: 'חציון מאז הקנייה, ' + C.q + ' עד ' + C.nowQ });
        items.push({ k: 'D', est: true, value: r.value, label: 'השווי המשוער שלכם' });
        var distinct = items.map(function (x) { return x.value; }).concat(v.asking > 0 ? [v.asking] : []).filter(function (x, i, a) { return a.indexOf(x) === i; }).length;
        if (distinct > 1) figs.push(figScale({ items: items, ask: v.asking > 0 ? v.asking : 0, rlo: X.n > 1 ? X.lo : null, rhi: X.n > 1 ? X.hi : null, rangeLabel: 'הטווח בין הבדיקות הרשמיות', rangeValue: X.n > 1 ? 'פער ' + F.num(100 * X.spread, 1) + '%' : '',
          title: X.n > 2 ? 'שלוש הבדיקות על ציר אחד' : X.n > 1 ? 'שתי בדיקות רשמיות על ציר אחד' :v.asking > 0 ? 'החציון, השווי והמחיר המבוקש' : 'החציון הרשמי מול השווי המשוער',
          aria: items.map(function (x) { return x.label + ' ' + F.ils(x.value); }).join(', ') + (v.asking > 0 ? ', המחיר המבוקש ' + F.ils(v.asking) : '') }));
      }
      var ref = A || (b.level !== 'sqm' ? b : null);
      if (S && S.q && ref) {
        var hs = ref.level === 'hood' ? ((S.hood || {})[String(ref.id)] || {})[ref.rk] : null, cs = ((S.city || {})[v.city] || {})[ref.rk], il = (S.il || {})[ref.rk];
        var a = hs || cs, aw = hs ? ref.where : v.city;
        if (a && il) {
          var lastOf = function (arr) { for (var i = arr.length - 1; i >= 0; i--) if (arr[i] > 0) return i; return -1; };
          var ia = lastOf(a), ii = lastOf(il), bq = bought(v), bi = bq ? S.q.indexOf(bq.q) : -1;
          figs.push(figLine({ q: S.q, a: a, b: il, bi: bi, bought: v.bought > 0 ? v.bought : 0, title: 'חציון ' + ref.n + ' חדרים, ' + aw + ' מול ישראל',
            aName: aw + ', ' + ref.n + ' חדרים · ' + S.q[ia] + ': ' + F.ils(a[ia]), bName: 'ישראל, ' + ref.n + ' חדרים · ' + S.q[ii] + ': ' + F.ils(il[ii]),
            buyName: 'מחיר הקנייה · ' + (bq ? F.month(bq.key) : '') + ': ' + F.ils(v.bought),
            aria: 'חציון ' + ref.n + ' חדרים ב' + aw + ' מ־' + S.q[0] + ' עד ' + S.q[ia] + ', ' + F.ils(a[ia]) + ' ברבעון האחרון; ישראל ' + F.ils(il[ii]) + ' ב־' + S.q[ii] }));
        }
      }
      if (figs.length) out.figure = figs.join('');
      if (v.method === 'deals') {
        var c = D.cities[v.city], n = sr(v.rooms), k = 'r' + n;
        out.scenarioLabel = 'באותה שכונה, לפי מספר החדרים';
        out.scenarios = [3, 4, 5].map(function (m) { var x = base(Object.assign({}, v, { rooms: m }), D); return { key: String(m), name: m + ' חדרים' + (x && x.level === 'city' ? ' · העיר' : ''), value: x ? F.ils(x.price) : 'אין נתון' }; });
        var rows = c.hoods.filter(function (h) { return h[k]; }).sort(function (a, b) { return b[k][0] - a[k][0]; });
        out.table = { title: 'חציון ' + n + ' חדרים בשכונות ' + v.city, head: ['שכונה', 'חציון', 'רבעון'], num: [1], rows: rows.map(function (h) { return [h.n, F.ils(h[k][0]), h[k][1]]; }) };
      }
      // 1.72.732: what the row below may carry to the forum's form, on the visitor's tick (never an address: the tool has no street)
      window.NLPV.last = { city: v.city, hood: v.hood ? String(v.hood) : '', rooms: +v.rooms || 0, sqm: +v.sqm || 0, value: Math.round(r.value), level: b.level };
      return out;
    }
  });
})();

/* 1.72.732 (HAD-787, Claude Design board 25; Ben 21.11.2026: "a gentle link, exactly in the right place"): ONE quiet row inside the
   result, right after the note that ends "הערכה ראשונית, לא חוות דעת שמאית", to the forum's form "כמה הדירה שלכם שווה". Hebrew pages
   only, only when the result stands on an official median, and only after the visitor changed a value (the opening values are an
   example). The details travel in sessionStorage (never in the address) and only while the tick stays on. */
(function () {
  if (!/^he/i.test(document.documentElement.lang || 'he')) return;
  var KEY = 'nlfh_from_est', touched = false, told = false, carry = true;
  function track(n, d) { try { if (window.nlTrack) window.nlTrack(n, d || {}); } catch (e) { /* the tracker is optional */ } }
  function css() {
    if (document.getElementById('nlpvf-css')) return;
    var s = document.createElement('style'); s.id = 'nlpvf-css';
    s.textContent = '.nlpvf{margin:14px 0 4px;border:1.5px solid #2F6F86;border-radius:12px;padding:14px;display:flex;flex-direction:column;gap:9px;background:#FFFFFF;text-align:start}'
      + '.nlpvf .nlpvf-h{font-family:inherit!important;font-weight:800!important;font-size:17px;line-height:1.3;color:#101820!important}'
      + '.nlpvf .nlpvf-t{font-size:14.5px;line-height:1.5;color:#3A4650}'
      + '.nlpvf a.nlpvf-a{display:flex;align-items:center;justify-content:center;min-height:46px;padding:0 16px;border-radius:10px;border:2px solid #2F6F86!important;background:#FFFFFF!important;color:#2F6F86!important;font-weight:700;font-size:15.5px;text-decoration:none!important;box-shadow:none!important}'
      + '.nlpvf a.nlpvf-a:hover,.nlpvf a.nlpvf-a:focus-visible{background:#2F6F86!important;color:#FFFFFF!important}'
      + '.nlpvf .nlpvf-c{display:flex;gap:9px;align-items:flex-start;font-size:13px!important;font-weight:400!important;line-height:1.45;color:#3A4650!important;cursor:pointer;min-height:44px;margin:0}.nlpvf .nlpvf-c{flex-wrap:nowrap!important}.nlpvf .nlpvf-c span{font-weight:400!important;flex:1 1 0;min-width:0}'
      + '.nlpvf .nlpvf-c input{width:20px;height:20px;margin:1px 0 0;flex-shrink:0;accent-color:#2F6F86}'
      + '@media (min-width:700px){.nlpvf a.nlpvf-a{align-self:flex-start}}@media print{.nlpvf{display:none}}';
    document.head.appendChild(s);
  }
  function build() {
    var w = document.createElement('div'); w.className = 'nlpvf'; w.setAttribute('role', 'group'); w.setAttribute('aria-label', 'שאלה לפורום על הדירה');
    var h = document.createElement('b'); h.className = 'nlpvf-h'; h.textContent = 'הדירה שלכם לא בדיוק כמו החציון?';
    var t = document.createElement('span'); t.className = 'nlpvf-t'; t.textContent = 'קומה, נוף, שיפוץ ורחוב משנים את המחיר. אפשר לשאול את חברי הפורום מה דעתם.';
    var a = document.createElement('a'); a.className = 'nlpvf-a'; a.href = location.origin + '/forum/#ask-home'; a.textContent = 'שאלו בפורום על הדירה שלכם';
    var l = document.createElement('label'); l.className = 'nlpvf-c';
    var c = document.createElement('input'); c.type = 'checkbox'; c.checked = carry;
    var ls = document.createElement('span'); ls.textContent = 'להעביר לשאלה את מה שמילאתי: עיר, שכונה, חדרים, שטח וההערכה. אפשר לשנות ולמחוק לפני הפרסום.';
    l.appendChild(c); l.appendChild(ls);
    c.addEventListener('change', function () { carry = c.checked; });
    a.addEventListener('click', function () {
      var L = window.NLPV && window.NLPV.last;
      try {
        if (carry && L) sessionStorage.setItem(KEY, JSON.stringify({ t: Date.now(), city: L.city, nbhd: L.hood, rooms: L.rooms, sqm: L.sqm, est: L.value, level: L.level }));
        else sessionStorage.removeItem(KEY);
      } catch (e) { /* private mode: the form opens empty */ }
      track('est_forum_press', { carry: carry && L ? 1 : 0 });
    });
    w.appendChild(h); w.appendChild(t); w.appendChild(a); w.appendChild(l);
    return w;
  }
  function place(root) {
    var ans = root.querySelector('.nli__answer'), out = ans && ans.parentNode, L = window.NLPV && window.NLPV.last;
    if (!out) return;
    var note = null, have = null;
    Array.prototype.forEach.call(out.children, function (e) { if (e.classList.contains('nli__note')) note = e; if (e.classList.contains('nlpvf')) have = e; });
    var ok = touched && note && L && (L.level === 'hood' || L.level === 'city');
    if (!ok) { if (have) have.remove(); return; }
    if (have) return;
    css(); note.parentNode.insertBefore(build(), note.nextSibling);
    if (!told) { told = true; track('est_forum_row', {}); }
  }
  function watch(root) {
    var touch = function (e) {
      var f = e.target && e.target.closest ? e.target.closest('.nli__form') : null;
      if (!f || (e.type === 'click' && !e.target.closest('button'))) return;
      touched = true; setTimeout(function () { place(root); }, 260);
    };
    root.addEventListener('input', touch, true); root.addEventListener('change', touch, true); root.addEventListener('click', touch, true);
    new MutationObserver(function () { place(root); }).observe(root, { childList: true, subtree: true });
  }
  function start() { Array.prototype.forEach.call(document.querySelectorAll('[data-nli="pval"]'), watch); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
