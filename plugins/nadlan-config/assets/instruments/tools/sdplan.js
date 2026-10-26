/* NadLan Instruments · sdplan v1 (S1 moat for /sde-dov/, 26.10.2026): "מגרש אחר מגרש ברובע שדה דב". For every plot of the
   three detailed plans (תמ"ל/3001 אשכול, תא/1/4444 מרכז הרובע, תא/2/4444 צפון הרובע): the use in the plan and the registered area
   (Tel Aviv GIS layer 837), the Israel Land Authority tender (winner as recorded, units, bids, winning bid, development cost, and
   our land-plus-development per unit), the architectural design plan and its date (layer 528), the permit request, the permit and
   the start of works (layers 772 and 499), the nearest green line station and the air distance to the waterline, and, where a
   project is in marketing, our project page and the price its developer reported (the figures of /sde-dov/prices/).
   The official stage is the latest official record found: בתכנית → שווק במכרז → תכנית עיצוב אושרה → הוגשה בקשה להיתר → התקבל
   היתר → בבנייה. Honesty: no delivery or occupancy year (no official source publishes one per plot); an open tender shows its
   closing date; a tender with no bids says so; distances are air distances. No names of private permit holders are kept.
   Data: data/sdplan.json (docs/research/2026-10-26-upgrades/s1-sde-dov/build_s1_data.py). Pure logic in NLSD for the node test.
   SVG in RTL: text-anchor start = the right end of a label. */
(function () {
  'use strict';
  var CN = { eshkol: 'מתחם אשכול', merkaz: 'מרכז הרובע', tzafon: 'צפון הרובע' };
  var CORDER = ['eshkol', 'merkaz', 'tzafon'];
  var USE = { res: 'מגורים', special: 'דיור מוגן ודיור מיוחד', hotel: 'מלונאות', biz: 'תעסוקה ומסחר' };
  var FILL = ['#EEF2F5', '#CFE0E7', '#8DB4C3', '#4F8BA0', '#2F6F86', '#1F4B5C'];
  var INK = '#12202A', INK2 = '#3E4C58', MUTE = '#5E6A75', LINE = '#D3DCE2', SEA = '#2F6F86', RED = '#C42550';
  var FONT = "font-family:'IBM Plex Sans Hebrew','IBM Plex Sans',system-ui,sans-serif", MONO = "font-family:'IBM Plex Mono',ui-monospace,monospace";

  function dd(iso) { var p = String(iso || '').split('-'); return p.length === 3 ? (+p[2]) + '.' + (+p[1]) + '.' + p[0] : String(iso || ''); }
  function n0(x) { return String(Math.round(x || 0)).replace(/\B(?=(\d{3})+(?!\d))/g, ','); }
  function ils(x) { return '₪' + n0(x); }
  function mil(x) { var m = x / 1e6; return (m >= 100 ? n0(m) : (Math.round(m * 10) / 10).toFixed(1)) + ' מיליון ₪'; }
  function esc0(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function nkey(id) { return parseInt(String(id).replace(/\D/g, ''), 10) || 0; }

  /** Indexes, built once per data object. */
  function ix(D) {
    if (D.__ix) return D.__ix;
    var by = {}, comp = { eshkol: [], merkaz: [], tzafon: [] }, proj = {};
    D.plots.forEach(function (r) { by[r.id] = r; (comp[r.c] = comp[r.c] || []).push(r); if (r.p && !proj[r.p.n]) proj[r.p.n] = r.id; });
    CORDER.forEach(function (c) { comp[c].sort(function (a, b) { return nkey(a.id) - nkey(b.id); }); });
    // a project on two plots gets its name once, on the larger plot
    var nameAt = {};
    D.plots.forEach(function (r) { if (r.p) { var o = nameAt[r.p.n]; if (!o || by[o].area < r.area) nameAt[r.p.n] = r.id; } });
    return (D.__ix = { by: by, comp: comp, nameAt: nameAt });
  }
  function stageOf(D, r) { return D.stages[r.s]; }
  /** The short words of a plot: number, project or winner, use. */
  function plotName(r) { return 'מגרש ' + r.id + (r.p ? ' · ' + r.p.n : ''); }
  function who(r) { return r.p ? r.p.n : (r.t && r.t.winner ? r.t.winner : (r.open ? 'במכרז פתוח' : (r.nobid ? 'לא הוגשו הצעות' : ''))); }
  function stageCell(D, r) {
    var s = stageOf(D, r);
    if (r.open) return s + ', מכרז פתוח עד ' + dd(r.open.close);
    if (r.nobid && !r.t) return s + ', מכרז בלי הצעות';
    if (r.s === 5 && r.works) return s + ' מ-' + dd(r.works.start);
    if (r.s === 4 && r.permit) return s + ' ' + dd(r.permit.first);
    if (r.s === 3 && r.req) return s + ' ' + dd(r.req.open);
    if (r.s === 2 && r.design) return s + ' ' + dd(r.design);
    if (r.s === 1 && r.t) return s + ' ' + dd(r.t.close);
    return s;
  }
  /** Counts for a compound ('' = the whole district), optionally for one use. */
  function counts(D, c, use) {
    var L = D.plots.filter(function (r) { return (!c || r.c === c) && (!use || use === 'all' || inUse(r, use)); });
    var by = D.stages.map(function () { return 0; }), units = 0, bids = 0, open = 0;
    L.forEach(function (r) { by[r.s]++; if (r.t && !(r.t['with'] && r.t['with'].some(function (w) { return nkey(w) < nkey(r.id); }))) units += r.t.units; if (r.t) bids += r.t.bids; if (r.open) open++; });
    return { n: L.length, by: by, units: units, open: open, list: L };
  }
  function inUse(r, use) {
    if (use === 'sale') return r.use === 'res' && (!r.t || r.t.use === 'בנייה רוויה' || r.t.use === 'מגורים, מסחר ומלונאות') && !(r.p && /להשכרה/.test(r.p.n));
    if (use === 'rent') return r.use === 'res' && ((r.t && r.t.use === 'דיור להשכרה') || (r.p && /להשכרה/.test(r.p.n)));
    if (use === 'special') return r.use === 'special';
    if (use === 'biz') return r.use === 'hotel' || r.use === 'biz';
    return true;
  }
  var SORTS = {
    stage: function (a, b) { return (b.s - a.s) || CORDER.indexOf(a.c) - CORDER.indexOf(b.c) || nkey(a.id) - nkey(b.id); },
    bids: function (a, b) { return ((b.t ? b.t.bids : -1) - (a.t ? a.t.bids : -1)) || nkey(a.id) - nkey(b.id); },
    land: function (a, b) { return ((b.t && b.t.perUnit) || -1) - ((a.t && a.t.perUnit) || -1) || nkey(a.id) - nkey(b.id); },
    station: function (a, b) { return a.st[1] - b.st[1] || nkey(a.id) - nkey(b.id); },
    sea: function (a, b) { return a.sea - b.sea || nkey(a.id) - nkey(b.id); }
  };
  function listRows(D, v) {
    var c = v.c && v.c !== 'all' ? v.c : '';
    var L = D.plots.filter(function (r) { return (!c || r.c === c) && inUse(r, v.use || 'all'); });
    return L.slice().sort(SORTS[v.sort] || SORTS.stage);
  }
  /** What the stage means and what to ask next (no forecasts). */
  function nextStep(D, r) {
    if (r.open) return 'המגרש במכרז פתוח של רשות מקרקעי ישראל, עד ' + dd(r.open.close) + '. אחרי ועדת המכרזים יתפרסם הזוכה, ואז תכנית עיצוב, בקשה להיתר והיתר.';
    if (r.nobid && !r.t) return 'במכרז ' + r.nobid.tender + ' (' + dd(r.nobid.close) + ') לא הוגשו הצעות למגרש הזה. הוא עדיין בתכנית, בלי זוכה.';
    switch (r.s) {
      case 0: return r.use === 'res' ? 'המגרש קבוע בתכנית ולא שווק במכרזי רשות מקרקעי ישראל שמצאנו. מגרש כזה נשאר לבעלי הקרקע או למכרז עתידי.' : 'המגרש קבוע בתכנית, בלי מכרז או תכנית עיצוב שמצאנו.';
      case 1: return 'המגרש שווק, ותכנית העיצוב האדריכלי עוד לא אושרה בעירייה. היא קובעת את הבינוי, הגבהים והפיתוח, והיא התנאי לבקשה להיתר.';
      case 2: return 'תכנית העיצוב אושרה. השלב הרשמי הבא: בקשה להיתר בנייה בעירייה. בקשו מהמוכר את מספר הבקשה להיתר ואת לוח הזמנים בכתב.';
      case 3: return 'הוגשה בקשה להיתר. עד ההיתר אין חפירה. בקשו מהמוכר את מספר הבקשה וממה היא מורכבת (חפירה ודיפון, או הבניין כולו).';
      case 4: return 'יש היתר. בקשו את מספר ההיתר, ובדקו אם הוא לחפירה ודיפון בלבד או לבניין כולו.';
      default: return 'יש היתר והעבודות התחילו לפי רישום אתרי הבנייה של העירייה. את מועד המסירה קובע חוזה המכר, לא השלב הזה.';
    }
  }
  window.NLSD = { ix: ix, counts: counts, listRows: listRows, inUse: inUse, stageCell: stageCell, nextStep: nextStep, who: who, dd: dd, n0: n0, SORTS: SORTS, CN: CN };
  if (!window.NadLanInstruments) return;
  var NI = window.NadLanInstruments, F = NI.fmt, esc = NI.esc;

  // ---------------------------------------------------------------- the map (Tel Aviv GIS plot outlines; the waterline from OpenStreetMap)
  function tx(x, y, s, o) {
    o = o || {}; var size = o.size || 13;
    var st = (o.mono ? MONO : FONT) + ';font-size:' + size + 'px;font-weight:' + (o.w || 400) + (o.halo ? ';paint-order:stroke;stroke:' + (o.haloC || '#fff') + ';stroke-width:3px;stroke-linejoin:round' : '');
    return '<text x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" text-anchor="' + (o.a || 'middle') + '" style="' + st + '" fill="' + (o.fill || INK) + '">' + esc(s) + '</text>';
  }
  function path(rings, P) { return rings.map(function (r) { return 'M' + r.map(function (p) { var q = P(p[0], p[1]); return q[0].toFixed(1) + ' ' + q[1].toFixed(1); }).join('L') + 'Z'; }).join(''); }
  var STYLE = '<style>text{pointer-events:none}.sdp{cursor:pointer;outline:none}.sdp:hover path,.sdp:focus path{stroke:' + INK + ';stroke-width:2}.sdp:focus-visible path{stroke:#2F6F86;stroke-width:3.5}</style>';

  /** A compound map, north up; or, for the whole district, a strip with the sea on top and the north on the right.
      Labels are placed by priority and never overlap: the selected plot, the stations, the project names, then plot numbers
      (biggest plots first); a label that has no free place is left out (its plot still opens on a tap). */
  function mapSVG(D, c, sel) {
    var X = ix(D), W = 420, M = 10, g = [], P, H, plots, rot = !c, top = 34;
    if (c) {
      var b = D.compounds[c].bbox, s = (W - 2 * M) / (b[2] - b[0]);
      H = Math.round((b[3] - b[1]) * s) + top + M; P = function (x, y) { return [M + (x - b[0]) * s, top + (b[3] - y) * s]; };
      plots = X.comp[c];
    } else {
      var xs = [], ys = []; D.plots.forEach(function (r) { r.poly.forEach(function (ring) { ring.forEach(function (p) { xs.push(p[0]); ys.push(p[1]); }); }); });
      var x0 = Math.min.apply(null, xs) - 60, x1 = Math.max.apply(null, xs) + 30, y0 = Math.min.apply(null, ys) - 30, y1 = Math.max.apply(null, ys) + 30, s2 = (W - 2 * M) / (y1 - y0);
      H = Math.round((x1 - x0) * s2) + top + 34; P = function (x, y) { return [M + (y - y0) * s2, top + (x - x0) * s2]; };
      plots = D.plots;
    }
    var legY = H + 6, legH = 92, cid = 'sdclip-' + (c || 'all');
    g.push('<svg viewBox="0 0 ' + W + ' ' + (H + legH) + '" direction="rtl" role="img" aria-label="' + esc((c ? CN[c] : 'רובע שדה דב') + ': כל המגרשים לפי השלב הרשמי היום') + '" style="display:block;width:100%;height:auto;background:#fff">' + STYLE);
    g.push('<defs><clipPath id="' + cid + '"><rect x="0" y="0" width="' + W + '" height="' + H + '"/></clipPath></defs><g clip-path="url(#' + cid + ')">');
    // the sea: the longest waterline closed against the sea-side edge
    var main = D.coast.slice().sort(function (a, b2) { return b2.length - a.length; })[0];
    if (main) {
      var pts = main.map(function (p) { return P(p[0], p[1]); }), f0 = pts[0], fl = pts[pts.length - 1];
      var close = rot ? ['L' + fl[0].toFixed(1) + ' -400', 'L' + f0[0].toFixed(1) + ' -400'] : ['L-400 ' + fl[1].toFixed(1), 'L-400 ' + f0[1].toFixed(1)];
      g.push('<path d="M' + pts.map(function (q) { return q[0].toFixed(1) + ' ' + q[1].toFixed(1); }).join('L') + close.join('') + 'Z" fill="#E4EEF2" stroke="none"/>');
    }
    D.coast.forEach(function (seg) { g.push('<path d="M' + seg.map(function (p) { var q = P(p[0], p[1]); return q[0].toFixed(1) + ' ' + q[1].toFixed(1); }).join('L') + '" fill="none" stroke="' + SEA + '" stroke-width="1.6"/>'); });
    // plots
    plots.forEach(function (r) {
      var on = sel === r.id, dash = r.open ? ' stroke-dasharray="4 3"' : '', stroke = r.open ? SEA : (r.nobid && !r.t ? RED : '#fff');
      g.push('<g class="sdp" data-sdplot="' + esc(r.id) + '" tabindex="0" role="button" aria-label="' + esc(plotName(r) + ', ' + stageOf(D, r)) + '"><path d="' + path(r.poly, P) + '" fill="' + FILL[r.s] + '" stroke="' + (on ? INK : stroke) + '" stroke-width="' + (on ? 3 : (r.open || (r.nobid && !r.t) ? 1.6 : 1)) + '"' + dash + '/></g>');
    });
    g.push('</g>');
    // label placement
    var boxes = [], lab = [];
    function wid(s3, size, mono) { return String(s3).length * size * (mono ? 0.62 : 0.56) + 6; }
    function free(bx) {
      if (bx[0] < 2 || bx[2] > W - 2 || bx[1] < top - 4 || bx[3] > H - 2) return false;
      for (var i = 0; i < boxes.length; i++) { var o = boxes[i]; if (bx[0] < o[2] && bx[2] > o[0] && bx[1] < o[3] && bx[3] > o[1]) return false; }
      return true;
    }
    function place(x, y, s3, o, tries) {
      var w = wid(s3, o.size, o.mono), hh = o.size + 2;
      for (var i = 0; i < tries.length; i++) {
        var a = o.a || 'middle', cx = x + tries[i][0], cy = y + tries[i][1];
        var bx = a === 'middle' ? [cx - w / 2, cy - hh + 3, cx + w / 2, cy + 3] : (a === 'end' ? [cx, cy - hh + 3, cx + w, cy + 3] : [cx - w, cy - hh + 3, cx, cy + 3]);
        if (free(bx)) { boxes.push(bx); lab.push(tx(cx, cy, s3, o)); return true; }
      }
      return false;
    }
    var stn = D.stations.map(function (s4) { return { s: s4, q: P(s4.xy[0], s4.xy[1]) }; }).filter(function (o) { return o.q[0] > 0 && o.q[0] < W && o.q[1] > top && o.q[1] < H; });
    stn.forEach(function (o) { boxes.push([o.q[0] - 6, o.q[1] - 6, o.q[0] + 6, o.q[1] + 6]); });
    var srow = sel ? X.by[sel] : null;
    if (srow && (!c || srow.c === c)) {
      var qs = P(srow.xy[0], srow.xy[1]);
      place(qs[0], qs[1] + 4, srow.id, { mono: true, size: 13, w: 600, fill: srow.s >= 3 ? '#fff' : INK }, [[0, 0]]);
      if (srow.p) place(qs[0], qs[1] + 4, srow.p.n.replace(/,.*$/, ''), { size: 14, w: 700, halo: true }, [[0, 19], [0, -15], [0, 34], [0, -30]]);
    }
    stn.forEach(function (o) { place(o.q[0], o.q[1] + 4, o.s.n, { a: 'end', size: 12, w: 500, halo: true, fill: INK2 }, [[8, 0], [-8 - wid(o.s.n, 12), 0], [-wid(o.s.n, 12) / 2, 17], [-wid(o.s.n, 12) / 2, -12]]); });
    Object.keys(X.nameAt).forEach(function (n) {
      var r = X.by[X.nameAt[n]]; if ((c && r.c !== c) || r.id === sel) return;
      var q = P(r.xy[0], r.xy[1]);
      place(q[0], q[1] + 4, n.replace(/,.*$/, ''), { size: 13, w: 600, halo: true }, rot ? [[0, -12], [0, 18], [0, -26], [0, 32]] : [[0, 18], [0, -14], [0, 32], [0, -28]]);
    });
    if (c) plots.slice().sort(function (a, b2) { return ((b2.use === 'res' || b2.use === 'special') - (a.use === 'res' || a.use === 'special')) || b2.area - a.area; }).forEach(function (r) {
      if (r.id === sel) return; var q = P(r.xy[0], r.xy[1]);
      place(q[0], q[1] + 4, r.id, { mono: true, size: 12, fill: r.s >= 3 ? '#fff' : INK }, [[0, 0]]);
    });
    g.push(lab.join(''));
    stn.forEach(function (o) { g.push('<circle cx="' + o.q[0].toFixed(1) + '" cy="' + o.q[1].toFixed(1) + '" r="5" fill="#fff" stroke="' + INK + '" stroke-width="2.2"/>'); });
    if (rot) {
      g.push(tx(W - M, 22, 'הים התיכון', { a: 'start', size: 13, fill: SEA, w: 600 }));
      g.push(tx(M + 2, 22, 'צפון ←', { a: 'end', size: 12, fill: MUTE }));
      CORDER.forEach(function (k) { var b3 = D.compounds[k].bbox, q = P((b3[0] + b3[2]) / 2, (b3[1] + b3[3]) / 2); g.push(tx(q[0], H - 10, CN[k], { size: 13, w: 600, fill: INK2 })); });
    } else {
      g.push(tx(W - M, 22, 'צפון ↑', { a: 'start', size: 12, fill: MUTE }));
      g.push(tx(M + 2, 22, 'הים התיכון', { a: 'end', size: 13, fill: SEA, w: 600 }));
    }
    // legend
    var lx = [W - M, W / 2 - 6], ly = legY + 14;
    D.stages.forEach(function (s5, i) {
      var x = lx[i % 2], y = ly + Math.floor(i / 2) * 22;
      g.push('<rect x="' + (x - 14) + '" y="' + (y - 11) + '" width="14" height="14" fill="' + FILL[i] + '" stroke="' + LINE + '"/>');
      g.push(tx(x - 20, y, s5, { a: 'start', size: 13 }));
    });
    var y3 = ly + 66;
    g.push('<rect x="' + (W - M - 14) + '" y="' + (y3 - 11) + '" width="14" height="14" fill="#fff" stroke="' + SEA + '" stroke-dasharray="4 3" stroke-width="1.6"/>');
    g.push(tx(W - M - 20, y3, 'מכרז פתוח', { a: 'start', size: 13 }));
    g.push('<circle cx="' + (W / 2 - 13) + '" cy="' + (y3 - 4) + '" r="5" fill="#fff" stroke="' + INK + '" stroke-width="2.2"/>');
    g.push(tx(W / 2 - 26, y3, 'תחנת הקו הירוק', { a: 'start', size: 13 }));
    g.push('</svg>');
    return g.join('');
  }

  // ---------------------------------------------------------------- views
  function sources(D) { return D.sources.map(function (s) { return { label: s.label + ' (' + dd(s.read) + ')', url: s.url }; }); }
  var FORMULA = 'השלב הוא הרישום הרשמי האחרון שמצאנו למגרש: תוצאות המכרז ברשות מקרקעי ישראל, תכנית העיצוב האדריכלי ברישום התכניות של העירייה, בקשה להיתר והיתר ברישום הבקשות וההיתרים, ותחילת עבודות ברישום אתרי הבנייה. קרקע ופיתוח ליחידת דיור = (סכום הזכייה + הוצאות הפיתוח) חלקי יחידות הדיור במכרז, החישוב שלנו. המרחקים בקו אווירי, ממרכז המגרש. אין כאן מועד מסירה או אכלוס: אף מקור רשמי לא מפרסם אותו למגרש.';

  function plotView(v, D) {
    var X = ix(D), r = X.by[v.plot];
    if (!r) return { error: { field: 'plot', msg: 'לא מצאנו את המגרש הזה.' } };
    var C = D.compounds[r.c], lines = [], links = [], t = r.t;
    lines.push({ label: 'יעוד בתכנית ' + C.plan, value: r.yeud });
    lines.push({ label: 'שטח המגרש הרשום', value: F.num(r.area) + ' מ״ר' });
    if (t) {
      lines.push({ label: 'מכרז רשות מקרקעי ישראל ' + t.tender + ', ' + t.use, value: 'נסגר ' + dd(t.close) });
      if (t.units) lines.push({ label: 'יחידות דיור במכרז' + (t['with'] ? ' (יחד עם מגרש ' + t['with'].join(', ') + ')' : ''), value: F.num(t.units) });
      lines.push({ label: 'הזוכה, כפי שנרשם במכרז: ' + t.winner, value: F.num(t.bids) + (t.bids === 1 ? ' הצעה' : ' הצעות') });
      lines.push({ label: 'סכום הזכייה', value: ils(t.bid) });
      lines.push({ label: 'הוצאות פיתוח', value: ils(t.dev) });
      if (t.perUnit) lines.push({ label: 'קרקע ופיתוח ליחידת דיור (החישוב שלנו)', value: 'כ-' + ils(t.perUnit) });
    }
    if (r.open) lines.push({ label: 'מכרז פתוח ' + r.open.tender + ', ' + r.open.use + (r.open.units ? ', ' + F.num(r.open.units) + ' יחידות דיור' : ''), value: 'עד ' + dd(r.open.close) });
    if (r.nobid && !t) lines.push({ label: 'מכרז ' + r.nobid.tender + (r.nobid.units ? ', ' + F.num(r.nobid.units) + ' יחידות דיור' : ''), value: 'לא הוגשו הצעות' });
    if (r.design) lines.push({ label: 'תכנית עיצוב אדריכלי ופיתוח אושרה', value: dd(r.design) });
    if (r.req) lines.push({ label: 'בקשה ראשונה להיתר' + (r.req.units ? ' (' + F.num(r.req.units) + ' יחידות דיור)' : '') + (r.req.n > 1 ? ', ' + r.req.n + ' בקשות' : ''), value: dd(r.req.open) });
    if (r.permit) lines.push({ label: 'היתר ראשון' + (r.permit.kinds.length === 1 && r.permit.kinds[0] === 'dig' ? ' (חפירה ודיפון)' : ''), value: dd(r.permit.first) });
    if (r.works) lines.push({ label: 'תחילת עבודות' + (r.works.stage ? ', ' + r.works.stage : ''), value: dd(r.works.start) });
    lines.push({ label: 'תחנת הקו הירוק הקרובה: ' + r.st[0], value: 'כ-' + F.num(r.st[1]) + ' מ׳' });
    lines.push({ label: 'המרחק מקו המים', value: 'כ-' + F.num(r.sea) + ' מ׳' });
    if (r.price) lines.push({ label: 'המחיר שדווח: ' + r.price.what + ' (' + r.price.date + ')', value: r.price.m2 + ' ₪ למ״ר' });
    if (r.p) links.push('<a href="' + esc(r.p.u) + '">' + esc('עמוד הפרויקט ' + r.p.n.replace(/,.*$/, '')) + '</a>');
    if (r.price) links.push('<a href="/sde-dov/prices/">' + esc('מחירי הדירות בשדה דב') + '</a>');
    if (C.url) links.push('<a href="' + esc(C.url) + '" target="_blank" rel="noopener">' + esc('תכנית ' + C.plan + ' במבא״ת') + '</a>');
    if (t || r.open) links.push('<a href="https://apps.land.gov.il/MichrazimSite/" target="_blank" rel="noopener">' + esc('המכרז באתר רשות מקרקעי ישראל') + '</a>');
    var answer = { label: plotName(r) + ' · ' + CN[r.c], value: stageOf(D, r), tone: r.nobid && !t ? 'survey' : '',
      sub: esc(t ? 'שווק במכרז ' + t.tender + ' (' + dd(t.close) + ')' + (t.units ? ', ' + F.num(t.units) + ' יחידות דיור' : '') + ', ' + F.num(t.bids) + ' הצעות' : (r.open ? 'במכרז פתוח עד ' + dd(r.open.close) : USE[r.use])) };
    var list = X.comp[r.c];
    var table = { title: CN[r.c] + ': כל ' + list.length + ' המגרשים והשלב שלהם', head: ['מגרש', 'פרויקט או זוכה', 'יח״ד', 'השלב היום', 'תחנה קרובה'], num: [2], phoneHide: [4],
      rows: list.map(function (q) { return [q.id + (q.id === r.id ? ' (נבחר)' : ''), who(q) || USE[q.use], q.t && q.t.units ? F.num(q.t.units) : (q.open && q.open.units ? F.num(q.open.units) : ''), stageCell(D, q), q.st[0] + ', ' + F.num(q.st[1]) + ' מ׳']; }) };
    var text = 'רובע שדה דב, ' + plotName(r) + ' (' + CN[r.c] + '): ' + stageCell(D, r) + '.' + (t ? ' מכרז ' + t.tender + ', ' + F.num(t.bids) + ' הצעות, ' + (t.units ? F.num(t.units) + ' יחידות דיור, ' : '') + 'זוכה: ' + t.winner + '.' : '') + ' תחנת ' + r.st[0] + ' כ-' + F.num(r.st[1]) + ' מ׳.';
    return { answer: answer, figure: mapSVG(D, r.c, r.id), lines: lines, note: esc(nextStep(D, r)) + (links.length ? '<br>' + links.join(' · ') : ''), table: table, formula: FORMULA, sources: sources(D), text: text };
  }

  function listView(v, D) {
    var c = v.c && v.c !== 'all' ? v.c : '', k = counts(D, c, v.use), rows = listRows(D, v);
    var lines = D.stages.map(function (s, i) { return { label: s, value: F.num(k.by[i]) + ' מגרשים' }; }).filter(function (l, i) { return k.by[i] || i === 5; });
    if (k.open) lines.push({ label: 'במכרז פתוח עכשיו', value: F.num(k.open) + ' מגרשים' });
    var useLab = { all: '', sale: ' לדירות למכירה', rent: ' לדירות להשכרה', special: ' לדיור מוגן', biz: ' למלונאות ותעסוקה' }[v.use || 'all'];
    var answer = { label: (c ? CN[c] : 'רובע שדה דב') + ': המגרשים' + useLab + ' והשלב שלהם, ' + dd(D.built), value: F.num(k.n) + ' מגרשים',
      sub: esc(F.num(k.units) + ' יחידות דיור שווקו במכרזים · ' + F.num(k.by[5]) + ' בבנייה · ' + F.num(k.by[2] + k.by[3] + k.by[4]) + ' עם תכנית עיצוב או היתר בדרך') };
    var table = { title: 'כל המגרשים (' + rows.length + ')', head: ['מגרש', 'מתחם', 'פרויקט או זוכה', 'יח״ד', 'הצעות', 'קרקע ליחידה', 'השלב היום', 'תחנה', 'ים'], num: [3, 4, 5, 7, 8], phoneHide: c ? [1, 5, 8] : [5, 8],
      rows: rows.map(function (q) { return [q.id, CN[q.c].replace('מתחם ', ''), who(q) || USE[q.use], q.t && q.t.units ? F.num(q.t.units) : (q.open && q.open.units ? F.num(q.open.units) : ''), q.t ? F.num(q.t.bids) : '', q.t && q.t.perUnit ? mil(q.t.perUnit) : '', stageCell(D, q), F.num(q.st[1]) + ' מ׳', F.num(q.sea) + ' מ׳']; }) };
    var text = (c ? CN[c] : 'רובע שדה דב') + ', ' + dd(D.built) + ': ' + F.num(k.n) + ' מגרשים, ' + F.num(k.by[5]) + ' בבנייה, ' + F.num(k.by[2]) + ' עם תכנית עיצוב מאושרת, ' + F.num(k.units) + ' יחידות דיור שווקו במכרזים.';
    return { answer: answer, figure: mapSVG(D, c, null), lines: lines, note: esc('בחרו מגרש במפה או בטבלה: מגרש אחד מציג את המכרז, תכנית העיצוב, ההיתר, התחנה הקרובה והמחיר שדווח.'), table: table, formula: FORMULA, sources: sources(D), text: text };
  }

  function presetList(D) {
    var X = ix(D), out = [];
    function plotP(id, sub) { var r = X.by[id]; if (r) out.push({ key: 'p' + id, label: (r.p ? r.p.n.replace(/,.*$/, '') + ' · ' : '') + 'מגרש ' + id, sub: sub || stageCell(D, r), set: { view: 'plot', plot: id } }); }
    out.push({ key: 'all', label: 'כל הרובע', sub: F.num(D.plots.length) + ' מגרשים לפי השלב', set: { view: 'list', c: 'all', use: 'all', sort: 'stage' } });
    plotP('111'); plotP('2270'); plotP('2206');
    var o = D.plots.filter(function (r) { return r.open && r.open.units; })[0];
    if (o) out.push({ key: 'open', label: 'מכרז פתוח · מגרש ' + o.id, sub: F.num(o.open.units) + ' יח״ד, עד ' + dd(o.open.close), set: { view: 'plot', plot: o.id } });
    out.push({ key: 'near', label: 'הקרובים לתחנה', sub: 'דירות למכירה, לפי המרחק', set: { view: 'list', c: 'all', use: 'sale', sort: 'station' } });
    return out;
  }

  window.NLSD.map = mapSVG;  // the same drawing, rendered once in node for the page's static figure (s1-sde-dov/tool/render_static_map.js)
  NI.register('sdplan', {
    kicker: 'מגרש אחר מגרש · רובע שדה דב',
    title: 'כל מגרש ברובע שדה דב: מי זכה בו, בכמה, ובאיזה שלב הוא היום',
    lede: 'בוחרים מגרש במפה או ברשימה, ומקבלים את המכרז של רשות מקרקעי ישראל (הזוכה, מספר ההצעות, סכום הזכייה והוצאות הפיתוח), את השלב אצל העירייה (תכנית עיצוב, בקשה להיתר, היתר ותחילת עבודות), את תחנת הקו הירוק הקרובה ואת המרחק מהים, ובפרויקט שבשיווק: את המחיר שדווח.',
    strip: function (data) { var D = data.sdplan, k = counts(D, '', 'all'); return [{ label: 'מגרשים בשלוש התכניות', value: F.num(k.n) }, { label: 'יחידות דיור ששווקו', value: F.num(k.units) }, { label: 'מגרשים בבנייה', value: F.num(k.by[5]) }, { label: 'נבדק', value: dd(D.built) }]; },
    presets: function (data) { return presetList(data.sdplan); },
    defaults: function () { return { view: 'list', c: 'all', use: 'all', sort: 'stage', plot: '111' }; },
    fields: [
      { id: 'view', label: 'מה להציג', type: 'segmented', options: [{ value: 'plot', label: 'מגרש אחד' }, { value: 'list', label: 'כל המגרשים' }] },
      { id: 'plot', label: 'מגרש', type: 'select', showIf: function (v) { return v.view === 'plot'; }, optionsFrom: function (v, data) {
        var D = data.sdplan, X = ix(D), o = [];
        CORDER.forEach(function (c) { X.comp[c].forEach(function (r) { o.push({ value: r.id, label: CN[c].replace('מתחם ', '') + ' · ' + r.id + (r.p ? ' · ' + r.p.n.replace(/,.*$/, '') : '') + ' · ' + D.stages[r.s] }); }); });
        return o;
      } },
      { id: 'c', label: 'מתחם', type: 'select', showIf: function (v) { return v.view === 'list'; }, options: [{ value: 'all', label: 'כל הרובע' }, { value: 'eshkol', label: 'מתחם אשכול' }, { value: 'merkaz', label: 'מרכז הרובע' }, { value: 'tzafon', label: 'צפון הרובע' }] },
      { id: 'use', label: 'סוג המגרש', type: 'select', showIf: function (v) { return v.view === 'list'; }, options: [{ value: 'all', label: 'הכול' }, { value: 'sale', label: 'דירות למכירה' }, { value: 'rent', label: 'דירות להשכרה' }, { value: 'special', label: 'דיור מוגן' }, { value: 'biz', label: 'מלונאות ותעסוקה' }] },
      { id: 'sort', label: 'סדר הטבלה', type: 'select', showIf: function (v) { return v.view === 'list'; }, options: [{ value: 'stage', label: 'מהשלב המתקדם' }, { value: 'bids', label: 'לפי מספר ההצעות במכרז' }, { value: 'land', label: 'לפי קרקע ופיתוח ליחידה' }, { value: 'station', label: 'לפי המרחק לתחנה' }, { value: 'sea', label: 'לפי המרחק מהים' }] }
    ],
    compute: function (v, data) {
      var D = data.sdplan;
      if (!D || !D.plots) return { error: { field: null, msg: 'הנתונים לא נטענו.' } };
      return v.view === 'plot' ? plotView(v, D) : listView(v, D);
    }
  });

  // a plot on the map opens that plot (pointer and keyboard)
  function open(g) {
    var host = g.closest('[data-nli="sdplan"]'); if (!host) return;
    var seg = host.querySelector('.nli__seg'); if (seg && seg.children[0] && seg.children[0].getAttribute('aria-pressed') !== 'true') seg.children[0].click();
    var sel = host.querySelector('select[id$="-plot"]'); if (!sel) return;
    sel.value = g.getAttribute('data-sdplot'); sel.dispatchEvent(new Event('change', { bubbles: true }));
  }
  document.addEventListener('click', function (e) { var g = e.target && e.target.closest ? e.target.closest('[data-sdplot]') : null; if (g) { e.preventDefault(); open(g); } });
  document.addEventListener('keydown', function (e) { if (e.key !== 'Enter' && e.key !== ' ') return; var g = e.target && e.target.closest ? e.target.closest('[data-sdplot]') : null; if (g) { e.preventDefault(); open(g); } });
})();
