/* NadLan Instruments · the apartment-design family (HAD-707, 11.11.2026; Ben: "tools on top of tools ... every page must be
   the best on the web for its phrase"). One file (registry 'file' => 'design'), 17 tools for /design-studio/, the designer price
   page and the designers page:
     dsgfee      מחשבון עיצוב פנים: every pricing method side by side (hour, meeting, m², percent of the works, apartment size)
     dsgquote    בדיקת הצעת מחיר של מעצבת פנים: the quote against the published ranges, and the usual items it leaves out
     dsgbudget   תקציב לעיצוב דירה חדשה: room by room, three levels, a share bar and what moves the total most
     dsgfurnish  כמה עולה לרהט דירה: the furniture basket of every room
     dsgkitchen  כמה עולה מטבח: running metres, level, worktop, island, appliances
     dsgfloor    מחשבון ריצוף ופרקט: waste by laying pattern, boxes, cost
     dsgpaint    מחשבון צביעת דירה: wall area net of openings, litres and cans, painter or yourself
     dsgsofa     האם הספה תיכנס: the wall, the walkway, the door, the turn in the corridor and the lift, drawn to scale
     dsgrug      איזה גודל שטיח לסלון: the ready size that fits the seating group, drawn to scale
     dsgdining   פינת אוכל: the table for the diners and the space around the chairs, drawn to scale
     dsgbed      חדר שינה: which bed fits with walkways and a wardrobe, drawn to scale
     dsglight    תכנון תאורה: lumens by room and area, fittings, colour of the light, cost of the points
     dsgpoints   נקודות חשמל: the specification against what you want, and the cost of the additions
     dsgwho      מי מתאים לכם: interior designer, home styling, architect or one consultation, with the costs side by side
     dsgtime     לוח זמנים לדירה חדשה: from the handover month back, the latest sensible month of every decision
     dsgstyle    סגנונות עיצוב פנים: five questions, a style, its colours and the living-room list priced as a range
     dsgcurtain  וילונות ותריסים: the windows and what covering them costs
   Data: data/design.json (tools/instruments/build_design_data.py from the research price files; never a site name). Every price
   is a published range with its unit, the month it was read (November 2026), the VAT status and the number of sources; a range
   from one source or with low confidence is marked rough. Physical and ergonomic numbers live in design.json "rules", each
   with its basis and kind (standard / rule of thumb / our assumption).
   The engine cannot draw a plan, so the to-scale drawings are built here as SVG strings in r.figure (the engine's own slot,
   1.72.521), and recomputed on every change: the drawing follows the numbers live. Pure math in window.NLDS for node tests. */
(function () {
  'use strict';
  var EPS = 1e-9;
  /* ---------------- ranges ---------------- */
  function rg(lo, hi) { return { lo: lo, hi: hi == null ? null : hi }; }
  function radd(a, b) { if (!a) return b; if (!b) return a; return rg(a.lo + b.lo, a.hi == null || b.hi == null ? null : a.hi + b.hi); }
  function rmul(a, k) { return a ? rg(a.lo * k, a.hi == null ? null : a.hi * k) : null; }
  function rsum(list) { return list.reduce(function (s, x) { return x ? radd(s, x) : s; }, null) || rg(0, 0); }
  function rgb(b) { return b ? rg(b.lo, b.hi) : null; }
  function mid(r) { return r.hi == null ? r.lo : (r.lo + r.hi) / 2; }
  /** The published band of an item: the usual band when the research found one, else the full range. hi null = "and up". */
  function band(it) {
    if (!it) return null;
    var typ = it.tlo != null && it.thi != null && it.thi >= it.tlo;
    return { lo: typ ? it.tlo : it.low, hi: typ ? it.thi : it.high, full: rg(it.low, it.high), typical: typ,
      rough: it.conf === 'low' || it.n < 2 || !typ, vat: it.vat, n: it.n, unit: it.unit, name: it.name };
  }
  /** Part i of k equal parts of a band (the level split: thirds; the service split: halves). An open band stays open. */
  function part(b, i, k) { if (!b) return null; if (b.hi == null) return rg(b.lo, null); var w = (b.hi - b.lo) / k; return rg(b.lo + w * i, b.lo + w * (i + 1)); }
  var LV = { basic: 0, mid: 1, high: 2 };
  function lvl(b, level) { return level in LV ? part(b, LV[level], 3) : (b ? rg(b.lo, b.hi) : null); }
  function it(D, id) { return (D.items && D.items[id]) || (D.fees && D.fees[id]) || null; }
  function rule(D, k) { return D.rules && D.rules[k] ? D.rules[k].v : null; }
  function clamp(x, a, b) { return Math.max(a, Math.min(b, x)); }
  function isNum(x) { return typeof x === 'number' && isFinite(x); }
  /** Where a figure sits against a band: below_all, below, in, above, above_all (full range and usual band). */
  function pos(x, b) {
    if (!b) return 'none';
    if (x < b.full.lo - EPS) return 'below_all';
    if (b.full.hi != null && x > b.full.hi + EPS) return 'above_all';
    if (!b.typical) return 'in';
    if (x < b.lo - EPS) return 'below'; if (x > b.hi + EPS) return 'above'; return 'in';
  }

  /* ---------------- 1. designer fee: every method side by side ---------------- */
  function roomsRow(D, rooms) { var k = clamp(Math.round(rooms), 3, 5); return { k: k, nearest: k !== Math.round(rooms), b: band(it(D, 'fee_' + k + 'rooms')) }; }
  function feeModels(v, D) {
    if (!(v.area >= 10 && v.area <= 1000)) return { error: 'area' };
    if (!(v.rooms >= 1 && v.rooms <= 10)) return { error: 'rooms' };
    var meetings = isNum(v.meetings) ? v.meetings : 1; if (!(meetings >= 1 && meetings <= 20)) return { error: 'meetings' };
    var works = isNum(v.works) ? v.works : 0; if (works < 0) return { error: 'works' };
    var svc = v.service, half = svc === 'plan' ? 0 : svc === 'full' ? 1 : -1;
    var m2b = band(it(D, 'fee_m2')), rr = roomsRow(D, v.rooms), pb = it(D, 'fee_percent'), hour = band(it(D, 'fee_hour')), meet = band(it(D, 'fee_meeting'));
    if (!m2b || !rr.b || !pb || !hour || !meet) return { error: 'data' };
    var perM2 = rmul(half < 0 ? rg(m2b.lo, m2b.hi) : part(m2b, half, 2), v.area);
    var byRooms = half < 0 ? rg(rr.b.lo, rr.b.hi) : part(rr.b, half, 2);
    var percent = works > 0 ? rg(works * pb.low / 100, works * pb.high / 100) : null;
    var meeting = rmul(rg(meet.lo, meet.hi), meetings);
    var main, how;
    if (svc === 'consult') { main = meeting; how = 'meeting'; }
    else {
      var lo = Math.max(perM2.lo, byRooms.lo), hi = Math.min(perM2.hi, byRooms.hi);
      if (lo <= hi) { main = rg(lo, hi); how = 'overlap'; } else { main = rg(Math.min(perM2.lo, byRooms.lo), Math.max(perM2.hi, byRooms.hi)); how = 'apart'; }
    }
    var hours = rg(main.lo / hour.hi, main.hi / hour.lo);
    return { main: main, how: how, perM2: perM2, m2band: m2b, byRooms: byRooms, rooms: rr, percent: percent, pctBand: [pb.low, pb.high], hour: rg(hour.lo, hour.hi), hours: hours, meeting: meeting, meetings: meetings };
  }

  /* ---------------- 2. quote check ---------------- */
  var QITEMS = [
    { k: 'meet', he: 'פגישת היכרות ומדידה בדירה', p: 'fee_meeting' },
    { k: 'layout', he: 'תכנית העמדת רהיטים' },
    { k: 'plans', he: 'תכניות עבודה לבעלי המקצוע: חשמל, אינסטלציה, נגרות' },
    { k: 'renders', he: 'הדמיות של החדרים', p: 'render_view' },
    { k: 'boq', he: 'כתב כמויות', p: 'bill_of_quantities' },
    { k: 'kitchen', he: 'תכנון מטבח', p: 'fee_kitchen_plan' },
    { k: 'light', he: 'תכנית תאורה', p: 'fee_lighting_plan' },
    { k: 'shop', he: 'ליווי בבחירות ויום קניות', p: 'shopping_day' },
    { k: 'visits', he: 'ביקורי פיקוח בדירה בזמן העבודות' },
    { k: 'pay', he: 'תשלום לפי שלבים, לא הכול מראש' }
  ];
  function quoteCheck(v, D) {
    if (!(v.fee > 0 && v.fee < 5e6)) return { error: 'fee' };
    if (!(v.area >= 10 && v.area <= 1000)) return { error: 'area' };
    var vat = rule(D, 'vat_rate'), withVat = v.vat === 'without' ? v.fee * (1 + vat) : v.fee, without = v.vat === 'with' ? v.fee / (1 + vat) : v.fee;
    var m2b = band(it(D, 'fee_m2')), rr = roomsRow(D, v.rooms || 4);
    if (!m2b || !rr.b) return { error: 'data' };
    var perM2 = v.fee / v.area;
    var yes = [], no = [], unk = [];
    QITEMS.forEach(function (q) { var s = v['i_' + q.k]; var o = { k: q.k, he: q.he, price: q.p ? band(it(D, q.p)) : null }; (s === 'yes' ? yes : s === 'no' ? no : unk).push(o); });
    return { perM2: perM2, posM2: pos(perM2, m2b), posRooms: pos(v.fee, rr.b), m2band: m2b, rooms: rr, withVat: withVat, without: without, yes: yes, no: no, unk: unk, total: QITEMS.length };
  }

  /* ---------------- 3/4. furnishing basket by rooms ---------------- */
  var BASKET = {
    living: { he: 'סלון', items: [['sofa_3seat', 1], ['armchair', 1], ['coffee_table', 1], ['tv_console', 1], ['rug_200x300', 1], ['floor_lamp', 1]] },
    dining: { he: 'פינת אוכל', items: [['dining_set_6', 1]] },
    master: { he: 'חדר שינה הורים', items: [['bed_double_with_mattress', 1], ['wardrobe_sliding_2m', 1]] },
    kid: { he: 'חדר שינה נוסף', items: [['bed_single', 1], ['desk', 1], ['office_chair', 1], ['wardrobe_sliding_2m', 1]] },
    study: { he: 'חדר עבודה', items: [['desk', 1], ['office_chair', 1], ['bookcase', 1]] },
    balcony: { he: 'מרפסת', items: [['balcony_set', 1]] },
    lights: { he: 'גופי תאורה בכל הדירה', items: [['lighting_fixtures_apartment', 1]] },
    appl: { he: 'מוצרי חשמל', items: [['fridge', 1], ['dishwasher', 1]] }
  };
  function furnish(v, D) {
    var rooms = Math.round(v.rooms);
    if (!(rooms >= 1 && rooms <= 8)) return { error: 'rooms' };
    var level = v.level in LV ? v.level : 'mid', list = ['living', 'dining'];
    if (rooms >= 2) list.push('master');
    var extra = Math.max(0, rooms - 2);
    if (v.study === 'yes' && extra > 0) { list.push('study'); extra--; }
    for (var i = 0; i < extra; i++) list.push('kid');
    if (v.balcony === 'yes') list.push('balcony');
    list.push('lights');
    if (v.appliances === 'yes') list.push('appl');
    var out = [], total = null, swing = null, n = 0, miss = [];
    list.forEach(function (k, idx) {
      var B = BASKET[k], lines = [], sum = null;
      B.items.forEach(function (x) {
        var b = band(it(D, x[0])); if (!b) { if (miss.indexOf(x[0]) < 0) miss.push(x[0]); return; }
        var r = rmul(lvl(b, level), x[1]); lines.push({ id: x[0], qty: x[1], r: r, b: b }); sum = radd(sum, r);
        var w = r.hi == null ? 0 : r.hi - r.lo; if (!swing || w > swing.w) swing = { id: x[0], name: b.name, w: w };
      });
      if (k === 'kid') n++;
      out.push({ k: k, he: k === 'kid' ? B.he + (extra > 1 ? ' ' + n : '') : B.he, lines: lines, r: sum || rg(0, 0) });
      total = radd(total, sum);
    });
    var pubKey = rooms <= 3 ? 'furnish_2_3r_' : 'furnish_4_5r_';
    var pub = it(D, pubKey + level);
    return { rooms: out, total: total || rg(0, 0), level: level, missing: miss, published: pub ? { r: rg(pub.low, pub.high), name: pub.name, n: pub.n } : null, swing: swing };
  }

  /* ---------------- 5. kitchen ---------------- */
  var CAB = { basic: 'kitchen_cab_basic', mid: 'kitchen_cab_mid', high: 'kitchen_cab_premium' };
  var APPL = { none: [], cook: ['oven_builtin', 'hob', 'hood'], full: ['oven_builtin', 'hob', 'hood', 'dishwasher', 'fridge'] };
  function kitchen(v, D) {
    if (!(v.m > 0.5 && v.m <= 20)) return { error: 'm' };
    var level = v.level in LV ? v.level : 'mid', parts = [], miss = [];
    function P(k, he, id, r, q, ap) { var b = band(it(D, id)); if (!b) { miss.push(id); return; } parts.push({ k: k, he: he || b.name, r: r(b), b: b, q: q, appl: !!ap }); }
    P('cab', 'ארונות', CAB[level], function (b) { return rmul(rgb(b), v.m); }, v.m);
    if (v.worktop === 'quartz' || v.worktop === 'porcelain') P('top', 'משטח', v.worktop === 'quartz' ? 'worktop_quartz' : 'worktop_porcelain', function (b) { return rmul(lvl(b, level), v.m); }, v.m);
    if (v.island === 'yes') P('island', 'אי', 'kitchen_island', function (b) { return lvl(b, level); }, 1);
    if (v.sink === 'yes') P('sink', 'כיור', 'kitchen_sink', function (b) { return lvl(b, level); }, 1);
    (APPL[v.appl] || []).forEach(function (id) { P(id, null, id, function (b) { return lvl(b, level); }, 1, true); });
    var total = rsum(parts.map(function (p) { return p.r; }));
    var noAppl = rsum(parts.filter(function (p) { return !p.appl; }).map(function (p) { return p.r; }));
    var full = it(D, 'kitchen_full'), plan = band(it(D, 'fee_kitchen_plan'));
    if (!parts.length) return { error: 'data' };
    var swing = parts.slice().sort(function (a, b) { return (b.r.hi == null ? 0 : b.r.hi - b.r.lo) - (a.r.hi == null ? 0 : a.r.hi - a.r.lo); })[0];
    return { parts: parts, total: total, noAppl: noAppl, published: full ? rg(full.low, full.high) : null, plan: rgb(plan), level: level, swing: swing, missing: miss };
  }

  /* ---------------- 6. flooring ---------------- */
  var FLOOR = {
    tile60: { he: 'פורצלן 60×60', mat: 'tile_material_60', lay: 'tile_laying' }, tile80: { he: 'פורצלן 80×80', mat: 'tile_material_80', lay: 'tile_laying' },
    tile120: { he: 'פורצלן 120×120', mat: 'tile_material_120', lay: 'tile_laying' }, laminate: { he: 'פרקט למינציה', inst: 'laminate' },
    engineered: { he: 'פרקט עץ תלת שכבתי', inst: 'engineered_parquet' }, spc: { he: 'פרקט SPC או ויניל', inst: 'spc_vinyl' }
  };
  function boxes(area, box) { return Math.ceil(area / box - EPS); }
  function floor(v, D) {
    if (!(v.area > 0 && v.area <= 2000)) return { error: 'area' };
    var T = FLOOR[v.type]; if (!T) return { error: 'type' };
    var wp = (rule(D, 'waste_pct') || {})[v.pattern]; if (!isNum(wp)) return { error: 'pattern' };
    var box = isNum(v.box) && v.box > 0 ? v.box : (rule(D, 'box_m2') || {})[v.type];
    if (!(box > 0 && box <= 10)) return { error: 'box' };
    var ordered = v.area * (1 + wp / 100), nb = boxes(ordered, box), parts = [], miss = [], cross = null;
    function P(k, he, id, q) { var b = band(it(D, id)); if (!b) { miss.push(id); return; } parts.push({ k: k, he: he, r: rmul(rgb(b), q), b: b }); }
    if (T.mat) {
      P('mat', 'החומר, עם הפחת (' + (Math.round(nb * box * 100) / 100) + ' מ"ר)', T.mat, nb * box);
      P('lay', 'עבודת הריצוף', T.lay, v.area);
      cross = rmul(rgb(band(it(D, 'tile_supplied_laid'))), v.area);
    } else P('inst', T.he + ' כולל התקנה', T.inst, v.area);
    if (v.skirt > 0) P('skirt', 'פנלים, ' + v.skirt + ' מטר', 'skirting', v.skirt);
    return { missing: miss, waste: wp, ordered: ordered, box: box, boxes: nb, boxArea: nb * box, parts: parts, total: parts.length ? rsum(parts.map(function (p) { return p.r; })) : null, cross: cross, he: T.he, tiles: !!T.mat };
  }

  /* ---------------- 7. painting ---------------- */
  function cans(L) {
    var S = [18, 5, 1], n18 = Math.floor(L / 18 + EPS), r = L - 18 * n18;
    if (r > 14 + EPS) { n18++; r = 0; }
    var n5 = Math.floor(r / 5 + EPS); r -= 5 * n5; if (r > 3 + EPS) { n5++; r = 0; }
    var n1 = Math.ceil(r - EPS); if (n1 < 0) n1 = 0;
    return { n18: n18, n5: n5, n1: n1, litres: n18 * S[0] + n5 * S[1] + n1 };
  }
  function paint(v, D) {
    var h = v.h; if (!(h >= 2 && h <= 6)) return { error: 'h' };
    var walls = 0, floorA = 0, spaces = 0;
    if (v.mode === 'rooms') {
      (v.rows || []).forEach(function (r) { if (r.l > 0 && r.w > 0 && r.l < 50 && r.w < 50) { walls += 2 * (r.l + r.w) * h; floorA += r.l * r.w; spaces++; } });
      if (!spaces) return { error: 'rows' };
    } else {
      if (!(v.area >= 10 && v.area <= 1000)) return { error: 'area' };
      if (!(v.rooms >= 1 && v.rooms <= 10)) return { error: 'rooms' };
      spaces = Math.round(v.rooms) + 2;  // the rooms plus the kitchen and a bathroom or hall: our assumption, rooms close to square
      var a = v.area / spaces; walls = spaces * 4 * Math.sqrt(a) * h; floorA = v.area;
    }
    var doors = Math.max(0, v.doors || 0), wins = Math.max(0, v.windows || 0), wm2 = Math.max(0, v.winM2 || 0);
    var openings = doors * rule(D, 'door_m2') + wins * wm2, net = Math.max(0, walls - openings);
    var ceil = v.ceiling === 'yes' ? floorA : 0, area = net + ceil;
    var coats = clamp(Math.round(v.coats || 2), 1, 4), cover = v.cover > 0 ? v.cover : rule(D, 'paint_cover_m2l');
    var litres = area * coats / cover, c = cans(litres);
    var pb = band(it(D, 'wall_paint_m2')), painter = rmul(rgb(pb), area);
    var p4 = band(it(D, 'paint_4rooms')), diy = v.can18 > 0 ? c.litres * v.can18 / 18 : null;
    return { walls: walls, floorA: floorA, openings: openings, net: net, ceil: ceil, area: area, coats: coats, cover: cover, litres: litres, cans: c, painter: painter, pb: pb, flat4: rgb(p4), p4: p4, diy: diy, spaces: spaces };
  }

  /* ---------------- 8. does the sofa fit ---------------- */
  /** The longest rectangle of thickness w that turns a right-angle corner between corridors of widths a and b, kept flat
   *  (no tilting): L = min over θ of (a·sinθ + b·cosθ − w) / (sinθ·cosθ). With w = 0 it is the classic (a^⅔ + b^⅔)^{3/2}. */
  function cornerMax(a, b, w) {
    if (!(a > 0 && b > 0) || w >= Math.min(a, b)) return 0;
    var best = Infinity;
    for (var i = 1; i < 4000; i++) { var t = (Math.PI / 2) * i / 4000, s = Math.sin(t), c = Math.cos(t), L = (a * s + b * c - w) / (s * c); if (L < best) best = L; }
    return Math.max(0, best);
  }
  var RANK = { ok: 0, tight: 1, maybe: 1, no: 2, skip: -1 };
  function sofaFit(v, D) {
    var f = ['W', 'Dp', 'L', 'd', 'h'];
    for (var i = 0; i < f.length; i++) if (!(v[f[i]] > 0 && v[f[i]] <= 2000)) return { error: f[i] };
    var M = rule(D, 'wall_margin_cm'), gap = rule(D, 'sofa_table_gap_cm'), wMain = rule(D, 'walk_main_cm'), wMin = rule(D, 'walk_min_cm'), dm = rule(D, 'door_margin_cm');
    var table = v.table > 0 ? v.table : 0;
    var c = {};
    c.wall = v.L + 2 * M <= v.W + EPS ? 'ok' : v.L <= v.W + EPS ? 'tight' : 'no';
    var front = v.Dp - v.d - (table ? gap + table : 0);
    c.front = front >= wMain - EPS ? 'ok' : front >= wMin - EPS ? 'tight' : 'no';
    var thin = Math.min(v.d, v.h);
    c.door = v.door > 0 ? (thin <= v.door - dm + EPS ? 'ok' : 'no') : 'skip';
    var turn = v.door > 0 && v.hall > 0 ? cornerMax(v.door - dm, v.hall - dm, thin) : null;
    var ceil = v.ceil > 0 ? v.ceil : 0;
    c.turn = turn == null ? 'skip' : v.L <= turn + EPS ? 'ok' : ceil && v.L <= ceil - dm + EPS && Math.max(v.d, v.h) <= v.hall - dm + EPS ? 'maybe' : 'no';
    if (v.lift === 'yes' && v.lw > 0 && v.ld > 0 && v.lh > 0) {
      var lw = v.lw - dm, ld = v.ld - dm, lh = v.lh - dm, big = Math.max(v.d, v.h);
      var upright = v.L <= lh + EPS && thin <= Math.min(lw, ld) + EPS && big <= Math.max(lw, ld) + EPS;
      var flat = v.L <= Math.sqrt(lw * lw + ld * ld) - thin + EPS && Math.max(v.d, v.h) <= lh + EPS;
      var diag = v.L <= Math.sqrt(lw * lw + ld * ld + lh * lh) - thin + EPS;
      c.lift = upright || flat ? 'ok' : diag ? 'maybe' : 'no';
    } else c.lift = 'skip';
    var worst = 'ok'; Object.keys(c).forEach(function (k) { if (RANK[c[k]] > RANK[worst]) worst = c[k]; });
    return { c: c, worst: worst, front: front, turn: turn, thin: thin, gap: gap, table: table, wMain: wMain, wMin: wMin, margin: M };
  }

  /* ---------------- 9. rug size ---------------- */
  function rugPick(v, D) {
    var f = ['L', 'd', 'f', 'rw', 'rd'];
    for (var i = 0; i < f.length; i++) if (!(v[f[i]] > 0 && v[f[i]] <= 3000)) return { error: f[i] };
    var over = rule(D, 'rug_side_overhang_cm'), under = rule(D, 'rug_under_sofa_cm'), wall = rule(D, 'rug_wall_margin_cm');
    var needW = v.L + 2 * over, needD = v.lay === 'all' ? v.d + v.f - 15 + 10 : under + v.f - 15;
    var maxW = v.rw - 2 * wall, maxD = v.rd - 2 * wall;
    var sizes = (rule(D, 'rug_sizes_cm') || []).map(function (s) { return [Math.max(s[0], s[1]), Math.min(s[0], s[1])]; }).sort(function (a, b) { return a[0] * a[1] - b[0] * b[1]; });  // [along the sofa, depth]
    var fitsRoom = sizes.filter(function (s) { return s[0] <= maxW + EPS && s[1] <= maxD + EPS; });
    var good = fitsRoom.filter(function (s) { return s[0] >= needW - EPS && s[1] >= needD - EPS; });
    var pick = good[0] || null, status = 'ok';
    if (!pick) { if (fitsRoom.length) { pick = fitsRoom[fitsRoom.length - 1]; status = 'small'; } else status = 'none'; }
    var pid = pick ? (pick[0] === 230 && pick[1] === 160 ? 'rug_160x230' : pick[0] === 290 && pick[1] === 200 ? 'rug_200x300' : null) : null;
    var pb = pid ? band(it(D, pid)) : null;
    return { needW: needW, needD: needD, maxW: maxW, maxD: maxD, pick: pick, status: status, price: pb, pid: pid };
  }

  /* ---------------- 10. dining ---------------- */
  function tableFor(n, shape, D) {
    if (shape === 'round') { var dia = Math.ceil(Math.max(80, n * rule(D, 'seat_round_cm') / Math.PI) / 10 - EPS) * 10; return { l: dia, w: dia, round: true }; }
    return { l: Math.max(80, Math.ceil(n / 2) * rule(D, 'seat_width_cm')), w: rule(D, 'table_depth_cm'), round: false };
  }
  function diningFits(W, Dp, n, shape, c, D) {
    var t = tableFor(n, shape, D), A = Math.max(W, Dp), B = Math.min(W, Dp), end = rule(D, 'table_end_cm');
    if (t.round) return t.l + 2 * c <= B + EPS;
    return t.l + 2 * end <= A + EPS && t.w + 2 * c <= B + EPS;
  }
  function dining(v, D) {
    if (!(v.W >= 100 && v.W <= 3000)) return { error: 'W' };
    if (!(v.Dp >= 100 && v.Dp <= 3000)) return { error: 'Dp' };
    var n = Math.round(v.n); if (!(n >= 2 && n <= 16)) return { error: 'n' };
    var c = rule(D, v.pass === 'walk' ? 'chair_walk_cm' : v.pass === 'edge' ? 'chair_edge_cm' : 'chair_wall_cm'), cMin = rule(D, 'chair_wall_cm');
    var t = tableFor(n, v.shape, D), fit = diningFits(v.W, v.Dp, n, v.shape, c, D), fitMin = diningFits(v.W, v.Dp, n, v.shape, cMin, D);
    var most = 0; for (var k = 2; k <= 16; k++) if (diningFits(v.W, v.Dp, k, v.shape, c, D)) most = k;
    var A = Math.max(v.W, v.Dp), B = Math.min(v.W, v.Dp), end = rule(D, 'table_end_cm');
    var spare = t.round ? B - t.l - 2 * c : Math.min(B - t.w - 2 * c, A - t.l - 2 * end);
    var price;
    var s = band(it(D, 'dining_set_6')), tb = band(it(D, 'dining_table_6')), ch = band(it(D, 'dining_chair'));
    if (n >= 4 && n <= 6 && s) price = { r: rgb(s), b: s, how: 'set' };
    else if (tb && ch) price = { r: radd(rgb(tb), rmul(rgb(ch), n)), b: tb, ch: ch, how: 'parts' };
    else price = { r: null, b: null, how: 'none' };
    return { t: t, c: c, cMin: cMin, status: fit ? 'ok' : fitMin ? 'tight' : 'no', most: most, spare: spare, price: price, end: end };
  }

  /* ---------------- 11. bedroom ---------------- */
  function bedNeed(W, Dp, bw, bl, v, D) {
    var side = rule(D, 'bed_side_cm'), foot = rule(D, 'bed_foot_cm'), wd = rule(D, 'wardrobe_depth_cm');
    var front = v.ward === 'hinged' ? rule(D, 'wardrobe_front_hinged_cm') : rule(D, 'wardrobe_front_sliding_cm');
    var one = v.sides === 'one', atSide = v.ward !== 'none' && v.wardAt === 'side', across, along;
    if (atSide) {  // wardrobe along the long wall, beside the bed: the walkway on that side is the larger of the bed side and the wardrobe front
      across = (one ? 0 : side) + bw + Math.max(side, front) + wd;
      along = Math.max(bl + foot, v.wardLen || 0);
    } else {
      across = bw + (one ? side : 2 * side);
      along = bl + (v.ward === 'none' ? foot : Math.max(foot, front) + wd);
    }
    return { across: across, along: along, okA: across <= W + EPS, okL: along <= Dp + EPS, atSide: atSide,
      wardOk: v.ward === 'none' || (v.wardLen > 0 && v.wardLen <= (atSide ? Dp : W) + EPS) };
  }
  function bedFit(v, D) {
    if (!(v.W >= 150 && v.W <= 2000)) return { error: 'W' };
    if (!(v.Dp >= 150 && v.Dp <= 2000)) return { error: 'Dp' };
    var beds = rule(D, 'beds_cm'), b = beds.filter(function (x) { return String(x[0]) === String(v.bed); })[0];
    if (!b) return { error: 'bed' };
    if (v.ward !== 'none' && !(v.wardLen > 0 && v.wardLen <= 2000)) return { error: 'wardLen' };
    var n = bedNeed(v.W, v.Dp, b[0], b[1], v, D), best = null;
    beds.forEach(function (x) { var m = bedNeed(v.W, v.Dp, x[0], x[1], v, D); if (m.okA && m.okL) best = x; });
    var status = n.okA && n.okL && n.wardOk ? 'ok' : 'no';
    var bp = band(it(D, b[0] >= 140 ? 'bed_double_with_mattress' : 'bed_single')), wp = null;
    if (v.ward === 'hinged') { var wb = band(it(D, 'wardrobe_per_m')); wp = { r: rmul(rgb(wb), v.wardLen / 100), b: wb }; }
    else if (v.ward === 'sliding') { var sb = band(it(D, 'wardrobe_sliding_2m')), units = Math.ceil(v.wardLen / 200 - EPS); wp = { r: rmul(rgb(sb), units), b: sb, units: units }; }
    return { bed: b, need: n, best: best, status: status, bedPrice: bp, wardPrice: wp };
  }

  /* ---------------- 12. lighting ---------------- */
  var ROOMS = { living: 'סלון', dining: 'פינת אוכל', kitchen: 'מטבח', bedroom: 'חדר שינה', kids: 'חדר ילדים או חדר עבודה', bath: 'חדר רחצה', hall: 'מסדרון או כניסה' };
  function light(v, D) {
    if (!(v.area > 0 && v.area <= 200)) return { error: 'area' };
    var lux = (rule(D, 'lux') || {})[v.room === 'kids' ? 'kids' : v.room]; if (!isNum(lux)) return { error: 'room' };
    var lm = lux * v.area * rule(D, 'lumen_factor'), per = (rule(D, 'fixtures_lm') || {})[v.fixture]; if (!(per > 0)) return { error: 'fixture' };
    var n = Math.ceil(lm / per - EPS), points = v.fixture === 'profile' ? 1 : n;
    var pb = band(it(D, 'lighting_point')), cost = rmul(rgb(pb), points);
    var plan = v.plan === 'yes' ? band(it(D, 'fee_lighting_plan')) : null;
    return { lux: lux, lm: lm, per: per, n: n, points: points, cost: cost, pb: pb, plan: plan, kelvin: (rule(D, 'kelvin') || {})[v.room] };
  }

  /* ---------------- 13. electrical points ---------------- */
  function points(v, D) {
    var rows = (v.rows || []).filter(function (r) { return r && (isNum(r.spec) || isNum(r.want)); });
    if (!rows.length) return { error: 'rows' };
    var add = 0, less = 0, per = [];
    rows.forEach(function (r) { var s = isNum(r.spec) && r.spec >= 0 ? r.spec : 0, w = isNum(r.want) && r.want >= 0 ? r.want : 0; var d = w - s; if (d > 0) add += d; if (d < 0) less -= d; per.push({ room: r.room || '', spec: s, want: w, d: d }); });
    var eb = band(it(D, 'electric_point'));
    return { add: add, less: less, per: per, cost: rmul(rgb(eb), add), eb: eb, specTotal: per.reduce(function (s, r) { return s + r.spec; }, 0), wantTotal: per.reduce(function (s, r) { return s + r.want; }, 0) };
  }

  /* ---------------- 14. which professional ---------------- */
  function who(v, D) {
    var rooms = isNum(v.rooms) ? clamp(Math.round(v.rooms), 1, 8) : 4, rr = roomsRow(D, rooms);
    var mt = band(it(D, 'fee_meeting')), st = band(it(D, 'styling_apartment'));
    var opts = {
      consult: { he: 'פגישת ייעוץ אחת או שתיים', r: rmul(rgb(mt), 2), b: mt },
      styling: { he: 'הום סטיילינג: הלבשת הדירה בלי עבודות', r: rgb(st), b: st },
      plan: { he: 'מעצב פנים: תכנון בלבד', r: part(rr.b, 0, 2), b: rr.b },
      full: { he: 'מעצב פנים: תכנון וליווי עד הכניסה', r: part(rr.b, 1, 2), b: rr.b },
      architect: { he: 'אדריכל, ואיתו מעצב לפי הצורך', r: null }
    };
    var rec;
    if (v.permit === 'yes') rec = 'architect';
    else if (v.scope === 'furnish') rec = v.help === 'ideas' ? 'consult' : 'styling';
    else if (v.help === 'ideas') rec = 'consult';
    else if (v.help === 'plan') rec = 'plan';
    else rec = 'full';
    var why = { architect: 'שינוי שדורש היתר, תוספת בנייה או נגיעה בקיר נושא הוא עבודה של אדריכל או מהנדס, לא של מעצב.',
      consult: 'אתם רוצים כיוון ורעיונות, ואת הביצוע עושים לבד.',
      styling: 'אין עבודות בנייה; צריך לבחור רהיטים, צבעים, וילונות ואביזרים ולהלביש את הדירה.',
      plan: 'צריך תכניות מסודרות לבעלי המקצוע, ואת הקבלנים והספקים אתם מנהלים בעצמכם.',
      full: 'אתם רוצים מישהו שילווה את הבחירות, את בעלי המקצוע ואת העבודות עד הכניסה.' }[rec];
    return { rec: rec, why: why, opts: opts, rooms: rr };
  }

  /* ---------------- 15. timeline from the handover month ---------------- */
  function ym(s) { var m = /^(\d{4})-(\d{2})/.exec(String(s || '')); return m ? +m[1] * 12 + (+m[2] - 1) : null; }
  function ymKey(n) { var y = Math.floor(n / 12), m = n - y * 12 + 1; return y + '-' + (m < 10 ? '0' : '') + m; }
  function timeline(v, D) {
    var h = ym(v.handover), now = ym(v.today);
    if (h == null) return { error: 'handover' };
    if (now == null) return { error: 'today' };
    var steps = (D.steps || []).map(function (s) { var at = h + s.m; return { k: s.k, he: s.he, why: s.why, at: at, key: ymKey(at), state: at < now ? 'late' : at <= now + 1 ? 'now' : 'later' }; });
    var next = steps.filter(function (s) { return s.state !== 'late'; })[0] || null;
    var cbs = rule(D, 'build_months_cbs'), sign = ym(v.signed), est = sign != null && cbs ? { a: ymKey(sign + Math.round(cbs[0])), b: ymKey(sign + Math.round(cbs[1])) } : null;
    return { steps: steps, next: next, left: h - now, late: steps.filter(function (s) { return s.state === 'late'; }).length, est: est, handover: ymKey(h) };
  }

  /* ---------------- 16. style quiz ---------------- */
  var STYLES = {
    modern: { he: 'מודרני נקי', pal: [['#F4F4F2', 'לבן שבור'], ['#C9CCCF', 'אפור בטון'], ['#2B2F33', 'גרפיט'], ['#8A6E58', 'אגוז'], ['#3E6B8A', 'כחול פלדה']], mat: 'משטחים חלקים, זכוכית, מתכת מוברשת, פורצלן גדול', look: 'קווים ישרים, מעט חפצים ובלי עיטורים' },
    nordic: { he: 'סקנדינבי', pal: [['#FAFAF7', 'לבן'], ['#D9D4CB', 'אפור אבן בהיר'], ['#B8A387', 'אלון בהיר'], ['#6E8B74', 'ירוק מרווה'], ['#2E3A46', 'כחול לילה']], mat: 'עץ אלון בהיר, צמר, פשתן, קרמיקה מט', look: 'הרבה אור, עץ בהיר ובדים רכים' },
    industrial: { he: 'תעשייתי', pal: [['#E6E3DE', 'בטון בהיר'], ['#8E8B86', 'מלט'], ['#2A2724', 'פחם'], ['#7A4B32', 'עור קוניאק'], ['#4F5D63', 'פלדה כהה']], mat: 'בטון, ברזל שחור, עור, לבנים חשופות', look: 'חומרים גולמיים, תקרה גבוהה וגופי תאורה חשופים' },
    rustic: { he: 'כפרי', pal: [['#F3EFE8', 'לבן גיר'], ['#CBB89D', 'קש'], ['#8C6A4F', 'עץ מלא'], ['#5F7355', 'ירוק זית'], ['#2F3B4C', 'כחול דיו']], mat: 'עץ מלא, אבן, קרמיקה בעבודת יד, פשתן', look: 'חומים, רהיטים כבדים וחפצים עם היסטוריה' },
    boho: { he: 'בוהו', pal: [['#F5EEE6', 'שמנת'], ['#D9A47C', 'חימר'], ['#B5543C', 'אדמה אדומה'], ['#6F8F5E', 'ירוק עלה'], ['#2F4858', 'פטרול']], mat: 'קש, במבוק, מקרמה, שטיחים ארוגים, צמחים', look: 'שכבות של טקסטיל, צבעים חמים והרבה צמחים' },
    japandi: { he: 'יפני־סקנדינבי', pal: [['#F2EFEA', 'נייר אורז'], ['#CFC6B8', 'חול'], ['#9C8B76', 'אלון מעושן'], ['#4B4A45', 'אפר'], ['#1F2522', 'שחור דיו']], mat: 'עץ מט, נייר, טיח חלק, אבן אפורה', look: 'מעט מאוד חפצים, רהיטים נמוכים ושקט' },
    med: { he: 'ים תיכוני', pal: [['#FBF8F2', 'לבן סיד'], ['#E3D3B4', 'חול חוף'], ['#2F6F9F', 'כחול ים'], ['#C8693F', 'טרקוטה'], ['#6D7F4E', 'זית']], mat: 'טיח, אבן, קרמיקה מצוירת, ראטן, פשתן', look: 'אור חזק, קירות לבנים ונגיעות של כחול' }
  };
  var QUIZ = [
    { id: 'q1', he: 'איזה בוקר נראה לכם הכי טוב בבית?', o: [['a', 'הכול מסודר, משטח ריק ואור לבן', { modern: 2, japandi: 1 }], ['b', 'שמש על עץ בהיר ושמיכה רכה', { nordic: 2, japandi: 1 }], ['c', 'קפה ליד ספרייה מלאה וצמחים', { boho: 2, rustic: 1 }], ['d', 'ארוחת בוקר במרפסת עם ריח של ים', { med: 2, rustic: 1 }]] },
    { id: 'q2', he: 'איזה רצפה הייתם בוחרים?', o: [['a', 'פורצלן גדול וחלק', { modern: 2, industrial: 1 }], ['b', 'פרקט עץ בהיר', { nordic: 2, japandi: 1 }], ['c', 'בטון מוחלק או אבן', { industrial: 2, japandi: 1 }], ['d', 'קרמיקה מצוירת או טרקוטה', { med: 2, boho: 1, rustic: 1 }]] },
    { id: 'q3', he: 'כמה חפצים על המדפים?', o: [['a', 'כמעט כלום', { japandi: 2, modern: 2 }], ['b', 'מעט, נבחרים', { nordic: 2, med: 1 }], ['c', 'הרבה, כל אחד עם סיפור', { boho: 2, rustic: 2 }]] },
    { id: 'q4', he: 'איזה צבע מושך אתכם?', o: [['a', 'אפור וגרפיט', { modern: 2, industrial: 2 }], ['b', 'לבן ועץ', { nordic: 2, japandi: 2 }], ['c', 'חימר וירוק עלה', { boho: 2, rustic: 1 }], ['d', 'לבן וכחול ים', { med: 3 }]] },
    { id: 'q5', he: 'איזו ספה?', o: [['a', 'ספה נמוכה בקווים ישרים', { modern: 2, japandi: 2 }], ['b', 'ספה בבד בהיר על רגלי עץ', { nordic: 3 }], ['c', 'ספת עור עם ברזל', { industrial: 3 }], ['d', 'ספה עמוקה עם הרבה כריות', { boho: 2, rustic: 1, med: 1 }]] }
  ];
  function style(v, D) {
    var score = {}; Object.keys(STYLES).forEach(function (k) { score[k] = 0; });
    var answered = 0;
    QUIZ.forEach(function (q) { var a = v[q.id]; q.o.forEach(function (o) { if (o[0] === a) { answered++; Object.keys(o[2]).forEach(function (k) { score[k] += o[2][k]; }); } }); });
    if (!answered) return { error: 'q1' };
    var order = Object.keys(score).sort(function (a, b) { return score[b] - score[a] || (a < b ? -1 : 1); });
    var f = furnish({ rooms: 1, level: v.level, balcony: 'no', study: 'no', appliances: 'no' }, D);
    var living = f.rooms.filter(function (r) { return r.k === 'living'; })[0];
    return { top: order[0], second: score[order[1]] > 0 ? order[1] : null, score: score, S: STYLES[order[0]], list: living.lines, total: living.r, level: f.level };
  }

  /* ---------------- 17. curtains and shutters ---------------- */
  function curtains(v, D) {
    var area = 0, n = 0;
    (v.rows || []).forEach(function (r) { if (r.w > 0 && r.h > 0 && r.w <= 1000 && r.h <= 600) { area += r.w * r.h / 10000; n++; } });
    if (!n) return { error: 'rows' };
    var cb = band(it(D, 'curtain_m2')), sb = band(it(D, 'shutter_electric_m2'));
    var cur = v.curtain === 'yes' ? rmul(rgb(cb), area) : null, sh = v.shutter === 'yes' ? rmul(rgb(sb), area) : null;
    return { area: area, n: n, cur: cur, sh: sh, cb: cb, sb: sb, total: rsum([cur, sh]) };
  }

  /* ---------------- 3. total design budget for a new apartment ---------------- */
  function budget(v, D) {
    var rooms = Math.round(v.rooms); if (!(rooms >= 2 && rooms <= 6)) return { error: 'rooms' };
    if (!(v.area >= 30 && v.area <= 400)) return { error: 'area' };
    var level = v.level in LV ? v.level : 'mid', cats = [];
    var fu = furnish({ rooms: rooms, level: level, balcony: 'yes', study: 'no', appliances: 'yes' }, D);
    cats.push({ k: 'furn', he: 'רהיטים, תאורה ומוצרי חשמל', r: fu.total, kind: 'sea' });
    if (v.designer && v.designer !== 'none') {
      var fm = feeModels({ area: v.area, rooms: rooms, service: v.designer, meetings: 2, works: 0 }, D);
      if (!fm.error) cats.push({ k: 'design', he: v.designer === 'consult' ? 'שתי פגישות ייעוץ' : 'מעצב פנים', r: fm.main, kind: 'civic' });
    }
    if (v.kitchen === 'yes') { if (!(v.kitchenM > 0.5 && v.kitchenM <= 20)) return { error: 'kitchenM' }; var k = kitchen({ m: v.kitchenM, level: level, worktop: 'quartz', island: 'no', sink: 'yes', appl: 'cook' }, D); if (!k.error) cats.push({ k: 'kitchen', he: 'מטבח, ' + v.kitchenM + ' מטר', r: k.total, kind: 'housing' }); }
    if (v.parquet === 'yes') { if (!(v.parquetM2 > 0 && v.parquetM2 <= v.area)) return { error: 'parquetM2' }; var pq = band(it(D, 'engineered_parquet')); if (pq) cats.push({ k: 'floor', he: 'פרקט עץ, ' + v.parquetM2 + ' מ"ר', r: rmul(lvl(pq, level), v.parquetM2), kind: 'open' }); }
    if (v.ac === 'yes') { var ac = band(it(D, 'ac_minicentral_4rooms_total')); if (ac) cats.push({ k: 'ac', he: 'מיזוג מיני מרכזי', r: rgb(ac), kind: 'survey', rough: true }); }
    if (v.points > 0) { var ep = band(it(D, 'electric_point')); if (ep) cats.push({ k: 'points', he: v.points + ' נקודות חשמל נוספות', r: rmul(rgb(ep), v.points), kind: 'civic' }); }
    if (v.curtains === 'yes') { if (!(v.curtM2 > 0 && v.curtM2 <= 300)) return { error: 'curtM2' }; var cb = band(it(D, 'curtain_m2')); if (cb) cats.push({ k: 'curt', he: 'וילונות, ' + v.curtM2 + ' מ"ר', r: rmul(lvl(cb, level), v.curtM2), kind: 'open' }); }
    if (v.paint === 'yes') { var p4 = band(it(D, 'paint_4rooms')); if (p4) cats.push({ k: 'paint', he: 'צביעת הדירה', r: rmul(rgb(p4), v.area / rule(D, 'rooms_m2')['4']), kind: 'housing', rough: true }); }
    var sub = rsum(cats.map(function (c) { return c.r; })), pct = isNum(v.reserve) ? v.reserve : rule(D, 'contingency_pct');
    if (!(pct >= 0 && pct <= 50)) return { error: 'reserve' };
    var reserve = rmul(sub, pct / 100), total = radd(sub, reserve);
    var swing = cats.slice().sort(function (a, b) { return (b.r.hi == null ? 0 : b.r.hi - b.r.lo) - (a.r.hi == null ? 0 : a.r.hi - a.r.lo); })[0];
    return { cats: cats, sub: sub, reserve: reserve, pct: pct, total: total, swing: swing, furnish: fu, level: level };
  }

  var NLDS = { rg: rg, radd: radd, rmul: rmul, rsum: rsum, band: band, part: part, lvl: lvl, pos: pos, feeModels: feeModels, quoteCheck: quoteCheck, QITEMS: QITEMS,
    furnish: furnish, budget: budget, kitchen: kitchen, floor: floor, cans: cans, paint: paint, cornerMax: cornerMax, sofaFit: sofaFit, rugPick: rugPick,
    tableFor: tableFor, dining: dining, bedFit: bedFit, light: light, points: points, who: who, ym: ym, ymKey: ymKey, timeline: timeline, style: style,
    STYLES: STYLES, QUIZ: QUIZ, curtains: curtains, ROOMS: ROOMS, FLOOR: FLOOR };
  window.NLDS = NLDS;
  if (!window.NadLanInstruments) return;

  /* ======================================================================================================================
     The pages. Plain everyday Hebrew; every range says its unit, the month read, the VAT status and whether it is rough.
     ====================================================================================================================== */
  var NI = window.NadLanInstruments, F = NI.fmt, esc = NI.esc;
  var READ = 'נובמבר 2026';
  function css() {
    if (document.getElementById('nlds-css')) return;
    var s = document.createElement('style'); s.id = 'nlds-css';
    s.textContent = 'html body .nli [data-nli^="dsg"] .nli__fig{font:600 32px/38px var(--nli-sans);direction:rtl;unicode-bidi:isolate;text-align:right;white-space:normal;overflow-wrap:anywhere}' +
      '@media (max-width:520px){html body .nli [data-nli^="dsg"] .nli__fig{font-size:26px;line-height:32px}}' +
      'html body .nli [data-nli^="dsg"] .nli__lines div{flex-wrap:wrap;gap:2px 12px}html body .nli [data-nli^="dsg"] .nli__lines dd{font:600 14px/20px var(--nli-sans);direction:rtl;unicode-bidi:isolate;text-align:left;white-space:normal;margin-inline-start:auto}' +
      'html body .nli [data-nli^="dsg"] .nli__table td.n{font-family:var(--nli-sans) !important;direction:rtl;unicode-bidi:isolate;text-align:right;white-space:normal;min-width:118px}' +
      'html body .nli [data-nli^="dsg"] .nli__table td:first-child{min-width:110px}' +
      '[data-nli^="dsg"] .nli__figure svg{display:block;width:100%;height:auto;max-width:560px;margin:0 auto;background:#fff;border:1px solid var(--nli-line)}' +
      '[data-nli^="dsg"] .nli__figure .t{font:500 11px "IBM Plex Sans Hebrew",sans-serif;fill:#12202A}[data-nli^="dsg"] .nli__figure .m{font:500 10.5px "IBM Plex Sans Hebrew",sans-serif;fill:#3E4C58;font-variant-numeric:tabular-nums}' +
      '[data-nli^="dsg"] .nli__seg button{min-width:48px;justify-content:center;text-align:center}' +
      '[data-nli^="dsg"] .nli__figure .bad{fill:#C42550}' +
      '[data-nli="dsgpoints"] .nli__row{grid-template-columns:minmax(0,1.3fr) minmax(0,.7fr) minmax(0,.7fr) 44px}html body .nli [data-nli="dsgpoints"] .nli__row .nli__in:first-child input{font-family:var(--nli-sans);direction:rtl;font-size:15px}' +
      '[data-nli="dsgpaint"] .nli__row,[data-nli="dsgcurtain"] .nli__row{grid-template-columns:minmax(0,1fr) minmax(0,1fr) 44px}' +
      '[data-nli^="dsg"] .nlds-sw{display:flex;gap:6px;margin:4px 0 0}[data-nli^="dsg"] .nlds-sw span{flex:1;min-height:56px;border:1px solid var(--nli-line);display:flex;align-items:flex-end;padding:4px;font:500 11px/14px var(--nli-sans);color:#12202A;background-clip:padding-box}' +
      '[data-nli^="dsg"] .nlds-sw span.dk{color:#fff}' +
      '[data-nli^="dsg"] .nlds-steps{list-style:none;margin:0;padding:0;display:grid;gap:0;border-top:1px solid var(--nli-line)}' +
      '[data-nli^="dsg"] .nlds-steps li{display:grid;grid-template-columns:72px minmax(0,1fr);gap:10px;padding:9px 0;border-bottom:1px solid var(--nli-line);font:400 14px/20px var(--nli-sans);color:#12202A}' +
      '[data-nli^="dsg"] .nlds-steps b{font:500 14px/20px var(--nli-mono);color:#12202A}[data-nli^="dsg"] .nlds-steps small{display:block;color:#5E6A75;font-size:12.5px;line-height:18px}' +
      '[data-nli^="dsg"] .nlds-steps li.late b{color:#C42550}[data-nli^="dsg"] .nlds-steps li.now{background:#EEF4F6}[data-nli^="dsg"] .nlds-steps li.now b{color:#1F4B5C}';
    document.head.appendChild(s);
  }
  css();
  /** Rounded for reading: the low end down, the high end up, so the shown range never shrinks the published one. */
  function step(n) { return n < 1000 ? 10 : n < 10000 ? 100 : n < 100000 ? 500 : 1000; }
  function dn(n) { var s = step(Math.abs(n)); return Math.floor(n / s + EPS) * s; }
  function up(n) { var s = step(Math.abs(n)); return Math.ceil(n / s - EPS) * s; }
  function num(n) { return F.num(n); }
  /** "15,000 עד 40,000 ₪"; an open top "מ־15,000 ₪ ומעלה"; exact = round false (per m² prices, small numbers). */
  function R(r, exact) {
    if (!r) return 'אין לנו מחיר שפורסם';
    var lo = exact ? Math.round(r.lo) : dn(r.lo), hi = r.hi == null ? null : exact ? Math.round(r.hi) : up(r.hi);
    if (hi == null) return 'מ־' + num(lo) + ' ₪ ומעלה';
    if (lo === hi) return num(lo) + ' ₪';
    return num(lo) + ' עד ' + num(hi) + ' ₪';
  }
  var VAT = { included: 'כולל מע"מ', mixed: 'מע"מ: יש מקורות עם ויש בלי', unknown: 'לא צוין אם כולל מע"מ' };
  var VATS = { included: 'כולל', mixed: 'מעורב', unknown: 'לא צוין' };
  function rough(b) { return b && b.rough ? ' (גס)' : ''; }
  function itemRow(b, r, label) { return [label || b.name, R(r || b, true) + ' ' + b.unit + rough(b), VATS[b.vat] || 'לא צוין', String(b.n)]; }
  var PHEAD = ['פריט', 'טווח שפורסם', 'מע"מ', 'מקורות'];
  function srcLine(bs) {
    var n = 0, r = 0, v = {}; bs.forEach(function (b) { if (!b) return; n = Math.max(n, b.n); if (b.rough) r++; v[b.vat] = 1; });
    var vat = Object.keys(v).length === 1 ? VAT[Object.keys(v)[0]] : 'מע"מ: משתנה בין הפריטים, ראו בטבלה';
    return [{ label: 'טווחי מחירים שפורסמו בישראל, נקראו ב' + READ + ' · ' + vat + (r ? ' · ' + r + ' מהטווחים גסים: מקור אחד או ביטחון נמוך' : '') }];
  }
  function sum(list) { return list.reduce(function (s, x) { return s + (x || 0); }, 0); }
  function share(cats) { return cats.map(function (c) { return { label: c.he, value: mid(c.r), kind: c.kind || 'sea', shown: R(c.r) }; }); }
  function pickErr(e, map) { return { error: { field: e, msg: map[e] || (e === 'data' ? 'חסר מחיר שפורסם לחישוב הזה. רעננו את העמוד.' : 'בדקו את הערך הזה.') } }; }
  var LEVELS = [{ value: 'basic', label: 'בסיסי' }, { value: 'mid', label: 'בינוני' }, { value: 'high', label: 'גבוה' }];
  var LEVELHE = { basic: 'רמה בסיסית', mid: 'רמה בינונית', high: 'רמה גבוהה' };
  var YN = [{ value: 'yes', label: 'כן' }, { value: 'no', label: 'לא' }];
  var ROOMSEG = [{ value: 2, label: '2' }, { value: 3, label: '3' }, { value: 4, label: '4' }, { value: 5, label: '5' }, { value: 6, label: '6' }];
  function segNum(id, label, opts, help) { return { id: id, label: label, type: 'segmented', options: opts, help: help }; }
  var LEVELNOTE = 'בסיסי, בינוני וגבוה הם שלושה חלקים שווים של הטווח הנפוץ של כל פריט (או של כל הטווח שפורסם, כשאין טווח נפוץ). זו חלוקה שלנו, לא מחירון של חנות.';

  /* ---------------- SVG plan helpers (to scale) ---------------- */
  function plan(Wcm, Dcm, draw, aria) {
    var pad = 26, maxW = 340, sc = Math.min(maxW / Wcm, 300 / Dcm), w = Wcm * sc, h = Dcm * sc, W = w + 2 * pad, H = h + 2 * pad + 6;
    var g = ['<svg direction="rtl" viewBox="0 0 ' + W.toFixed(1) + ' ' + H.toFixed(1) + '" role="img" aria-label="' + esc(aria) + '">',
      '<defs><pattern id="nldsg" width="' + (50 * sc).toFixed(2) + '" height="' + (50 * sc).toFixed(2) + '" patternUnits="userSpaceOnUse"><path d="M' + (50 * sc).toFixed(2) + ' 0H0V' + (50 * sc).toFixed(2) + '" fill="none" stroke="#E3E9ED" stroke-width=".6"/></pattern>',
      '<pattern id="nldsh" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" stroke="#C42550" stroke-width="1.4" stroke-opacity=".55"/></pattern></defs>',
      '<rect x="' + pad + '" y="' + pad + '" width="' + w.toFixed(1) + '" height="' + h.toFixed(1) + '" fill="url(#nldsg)"/>'];
    var P = { x: function (cm) { return (pad + cm * sc).toFixed(1); }, y: function (cm) { return (pad + cm * sc).toFixed(1); }, s: function (cm) { return (cm * sc).toFixed(1); }, sc: sc };
    draw(g, P);
    g.push('<rect x="' + pad + '" y="' + pad + '" width="' + w.toFixed(1) + '" height="' + h.toFixed(1) + '" fill="none" stroke="#12202A" stroke-width="4"/>');
    g.push('<text x="' + (pad + w / 2).toFixed(1) + '" y="' + (pad - 8) + '" text-anchor="middle" class="m">' + (Wcm / 100).toFixed(2) + ' מטר</text>');
    g.push('<text x="' + (pad - 8) + '" y="' + (pad + h / 2).toFixed(1) + '" text-anchor="middle" class="m" transform="rotate(-90 ' + (pad - 8) + ' ' + (pad + h / 2).toFixed(1) + ')">' + (Dcm / 100).toFixed(2) + ' מטר</text>');
    g.push('<g transform="translate(' + (W - pad - 50 * sc - 2).toFixed(1) + ' ' + (H - 9).toFixed(1) + ')"><line x1="0" y1="0" x2="' + (50 * sc).toFixed(1) + '" y2="0" stroke="#12202A" stroke-width="1.5"/><text x="' + (25 * sc).toFixed(1) + '" y="-3" text-anchor="middle" class="m">50 ס"מ</text></g>');
    return g.join('') + '</svg>';
  }
  function box(P, x, y, w, h, fill, stroke, label, cls) {
    return '<rect x="' + P.x(x) + '" y="' + P.y(y) + '" width="' + P.s(w) + '" height="' + P.s(h) + '" fill="' + fill + '" stroke="' + (stroke || '#12202A') + '" stroke-width="1.4"' + (cls ? ' class="' + cls + '"' : '') + '/>' +
      (label ? '<text x="' + (+P.x(x + w / 2)).toFixed(1) + '" y="' + (+P.y(y + h / 2) + 4).toFixed(1) + '" text-anchor="middle" class="t">' + esc(label) + '</text>' : '');
  }
  var C = { sofa: '#2F6F86', sofaF: '#D6E6EC', wood: '#E9DFC9', rug: '#F2D15A', ok: '#4F9A5C', bad: '#C42550', bed: '#D6E6EC', ward: '#E6E1F2' };

  /* ---------------- dsgfee ---------------- */
  NI.register('dsgfee', {
    kicker: 'מחשבון · עיצוב פנים',
    title: 'כמה עולה מעצב פנים לדירה',
    lede: 'בוחרים את גודל הדירה ואת סוג השירות, ורואים את כל שיטות התמחור של מעצבי פנים זו לצד זו: לפי מטר, לפי גודל הדירה, לפי שעה, לפי פגישה ואחוז מתקציב העבודות. הכול בטווחים שפורסמו בישראל.',
    presets: [
      { key: 'r3', label: 'דירת 3 חדרים', sub: '80 מ"ר, ליווי מלא', set: { area: 80, rooms: 3, service: 'full' } },
      { key: 'r4', label: 'דירת 4 חדרים', sub: '100 מ"ר, ליווי מלא', set: { area: 100, rooms: 4, service: 'full' } },
      { key: 'r5', label: 'דירת 5 חדרים', sub: '130 מ"ר, ליווי מלא', set: { area: 130, rooms: 5, service: 'full' } },
      { key: 'new', label: 'דירה חדשה מקבלן', sub: '4 חדרים, תכנון בלבד', set: { area: 100, rooms: 4, service: 'plan', works: 150000 } },
      { key: 'consult', label: 'רק ייעוץ', sub: 'שתי פגישות בבית', set: { service: 'consult', meetings: 2 } }
    ],
    defaults: function () { return { area: 100, rooms: 4, service: 'full', meetings: 2, works: 0 }; },
    fields: [
      { id: 'area', label: 'שטח הדירה', type: 'number', unit: 'מ"ר' },
      segNum('rooms', 'מספר חדרים', ROOMSEG),
      { id: 'service', label: 'מה אתם צריכים', type: 'segmented', options: [{ value: 'consult', label: 'פגישות ייעוץ' }, { value: 'plan', label: 'תכנון בלבד' }, { value: 'full', label: 'תכנון וליווי עד הכניסה' }] },
      { id: 'meetings', label: 'כמה פגישות ייעוץ', type: 'number', showIf: function (v) { return v.service === 'consult'; } },
      { id: 'works', label: 'תקציב העבודות, אם ידוע (לא חובה)', type: 'money', unit: '₪', help: 'יש מעצבים שמתמחרים באחוז מתקציב העבודות. השאירו 0 אם אין עדיין תקציב.', showIf: function (v) { return v.service !== 'consult'; } }
    ],
    compute: function (v, data) {
      var D = data.design, r = feeModels(v, D);
      if (r.error) return pickErr(r.error, { area: 'הקלידו שטח בין 10 ל־1,000 מ"ר.', rooms: 'בחרו מספר חדרים.', meetings: 'בין פגישה אחת ל־20.', works: 'תקציב לא יכול להיות שלילי.' });
      var F2 = D.fees, svcHe = { consult: 'פגישות ייעוץ', plan: 'תכנון בלבד', full: 'תכנון וליווי עד הכניסה' }[v.service];
      var lines = [
        { label: 'לפי מטר: ' + R(v.service === 'consult' ? r.m2band : (v.service === 'plan' ? part(r.m2band, 0, 2) : part(r.m2band, 1, 2)), true) + ' למ"ר × ' + num(v.area) + ' מ"ר', value: R(r.perM2) },
        { label: 'לפי גודל הדירה (' + r.rooms.k + ' חדרים' + (r.rooms.nearest ? ', הקרוב ביותר שפורסם' : '') + ')', value: R(r.byRooms) },
        { label: 'לפי פגישה: ' + r.meetings + (r.meetings > 1 ? ' פגישות' : ' פגישה'), value: R(r.meeting) },
        { label: 'לפי שעה: ' + R(r.hour, true) + ' לשעה. הסכום למעלה שווה ל־', value: num(Math.floor(r.hours.lo)) + ' עד ' + num(Math.ceil(r.hours.hi)) + ' שעות' }
      ];
      if (r.percent) lines.push({ label: 'אחוז מתקציב העבודות: ' + r.pctBand[0] + '% עד ' + r.pctBand[1] + '%', value: R(r.percent) });
      var mainLab = v.service === 'consult' ? 'פגישות ייעוץ בבית' : r.how === 'overlap' ? 'הטווח שבו נפגשים המחיר למטר והמחיר לפי גודל הדירה' : 'בין המחיר למטר למחיר לפי גודל הדירה';
      var b = [band(F2.fee_m2), band(F2['fee_' + r.rooms.k + 'rooms']), band(F2.fee_hour), band(F2.fee_meeting), band(F2.fee_percent)];
      var notes = ['לכל שיטה טווח משלה, ולכן הן לא תמיד נפגשות. כשמשווים הצעות, מחלקים את הסכום בשטח הדירה ומשווים לשורה "לפי מטר".'];
      if (r.rooms.b.rough) notes.push('הטווח לדירת ' + r.rooms.k + ' חדרים גס: ' + r.rooms.b.n + ' מקורות בלבד.');
      notes.push('חלק מהמחירים פורסמו כבר ב־2021; כולם נקראו ב' + READ + '.');
      return {
        answer: { label: mainLab + ' · ' + svcHe, value: R(r.main), sub: esc('דירת ' + r.rooms.k + ' חדרים, ' + num(v.area) + ' מ"ר · ' + (VAT[F2.fee_m2.vat] || '')) },
        lines: lines,
        breakdown: v.service === 'consult' ? null : [{ label: 'לפי מטר', value: mid(r.perM2), kind: 'sea', shown: R(r.perM2) }, { label: 'לפי גודל הדירה', value: mid(r.byRooms), kind: 'civic', shown: R(r.byRooms) }],
        note: notes.map(esc).join('<br>'),
        table: { title: 'המחירים שפורסמו, לכל שיטה', head: PHEAD, num: [1], phoneHide: [3], rows: b.map(function (x, i) { var row = itemRow(x); if (i === 4) row[1] = x.full.lo + '% עד ' + x.full.hi + '% מהתקציב' + rough(x); return row; })
          .concat(['fee_3rooms', 'fee_4rooms', 'fee_5rooms'].filter(function (k) { return k !== 'fee_' + r.rooms.k + 'rooms'; }).map(function (k) { return itemRow(band(F2[k])); })) },
        formula: 'לפי מטר = שטח × המחיר למ"ר. תכנון בלבד = החצי התחתון של הטווח הנפוץ, ליווי מלא = החצי העליון (חלוקה שלנו: המקורות מתארים טווח "מתכנון בלבד ועד ליווי מלא"). לפי שעה: הסכום הראשי חלקי המחיר לשעה. אחוז: תקציב העבודות × 7% עד 15%.',
        sources: srcLine(b),
        text: 'מעצב פנים לדירת ' + r.rooms.k + ' חדרים (' + num(v.area) + ' מ"ר), ' + svcHe + ': ' + R(r.main) + ' לפי טווחים שפורסמו (' + READ + ').'
      };
    }
  });

  /* ---------------- dsgquote ---------------- */
  var POSHE = { below_all: 'נמוך מכל הטווח שפורסם', below: 'מתחת לטווח הנפוץ', in: 'בתוך הטווח הנפוץ', above: 'מעל הטווח הנפוץ, בתוך מה שפורסם', above_all: 'מעל כל הטווח שפורסם', none: 'אין טווח להשוואה' };
  var Q3 = [{ value: 'yes', label: 'כלול' }, { value: 'no', label: 'לא כלול' }, { value: 'unk', label: 'לא כתוב' }];
  NI.register('dsgquote', {
    kicker: 'בדיקה · הצעת מחיר',
    title: 'בדיקת הצעת מחיר של מעצבת פנים',
    lede: 'מקלידים את הסכום ואת השטח מההצעה שקיבלתם ומסמנים מה כתוב בה. רואים איפה הסכום עומד מול המחירים שפורסמו בישראל, ומה בדרך כלל נמצא בהצעה מלאה וחסר אצלכם.',
    presets: [
      { key: 'full4', label: 'הצעה מלאה, 4 חדרים', sub: '38,000 ₪, 100 מ"ר', set: { fee: 38000, area: 100, rooms: 4, vat: 'unk', i_meet: 'yes', i_layout: 'yes', i_plans: 'yes', i_renders: 'yes', i_boq: 'yes', i_kitchen: 'yes', i_light: 'yes', i_shop: 'yes', i_visits: 'yes', i_pay: 'yes' } },
      { key: 'thin3', label: 'הצעה קצרה, 3 חדרים', sub: '12,000 ₪, 80 מ"ר', set: { fee: 12000, area: 80, rooms: 3, vat: 'without', i_meet: 'yes', i_layout: 'yes', i_plans: 'unk', i_renders: 'no', i_boq: 'no', i_kitchen: 'unk', i_light: 'no', i_shop: 'no', i_visits: 'no', i_pay: 'unk' } },
      { key: 'big5', label: 'הצעה גבוהה, 5 חדרים', sub: '95,000 ₪, 130 מ"ר', set: { fee: 95000, area: 130, rooms: 5, vat: 'with', i_meet: 'yes', i_layout: 'yes', i_plans: 'yes', i_renders: 'yes', i_boq: 'unk', i_kitchen: 'yes', i_light: 'yes', i_shop: 'yes', i_visits: 'yes', i_pay: 'unk' } }
    ],
    defaults: function () { return { fee: 30000, area: 100, rooms: 4, vat: 'unk', i_meet: 'yes', i_layout: 'yes', i_plans: 'yes', i_renders: 'no', i_boq: 'unk', i_kitchen: 'yes', i_light: 'unk', i_shop: 'no', i_visits: 'yes', i_pay: 'unk' }; },
    fields: [
      { id: 'fee', label: 'הסכום בהצעה', type: 'money', unit: '₪' },
      { id: 'vat', label: 'המע"מ', type: 'segmented', options: [{ value: 'with', label: 'כולל מע"מ' }, { value: 'without', label: 'לא כולל' }, { value: 'unk', label: 'לא כתוב' }] },
      { id: 'area', label: 'שטח הדירה', type: 'number', unit: 'מ"ר' },
      segNum('rooms', 'מספר חדרים', ROOMSEG)
    ].concat(QITEMS.map(function (q) { return { id: 'i_' + q.k, label: q.he, type: 'segmented', options: Q3 }; })),
    compute: function (v, data) {
      var D = data.design, r = quoteCheck(v, D);
      if (r.error) return pickErr(r.error, { fee: 'הקלידו את הסכום שבהצעה.', area: 'הקלידו שטח בין 10 ל־1,000 מ"ר.' });
      var bad = r.posM2 === 'above_all' || r.posM2 === 'below_all';
      var lines = [
        { label: 'המחיר למטר בהצעה', value: num(Math.round(r.perM2)) + ' ₪ למ"ר' },
        { label: 'מול המחיר למטר שפורסם (' + R(r.m2band, true) + ')', value: POSHE[r.posM2] },
        { label: 'מול דירת ' + r.rooms.k + ' חדרים (' + R(r.rooms.b) + ')', value: POSHE[r.posRooms] },
        { label: 'מה כתוב בהצעה', value: r.yes.length + ' מתוך ' + r.total }
      ];
      if (v.vat === 'without') lines.splice(1, 0, { label: 'עם מע"מ 18%', value: R(rg(r.withVat, r.withVat), true) });
      if (v.vat === 'with') lines.splice(1, 0, { label: 'בלי מע"מ', value: R(rg(r.without, r.without), true) });
      var miss = r.no.map(function (x) { return x.he + (x.price ? ': אם תצטרכו את זה בנפרד, ' + R(x.price, true) + ' ' + x.price.unit + rough(x.price) : ''); });
      var notes = [];
      if (miss.length) notes.push('<b>לא כלול בהצעה:</b> ' + miss.map(esc).join(' · '));
      if (r.unk.length) notes.push('<b>לבקש שיהיה כתוב:</b> ' + r.unk.map(function (x) { return esc(x.he); }).join(' · '));
      if (v.vat === 'unk') notes.push(esc('בהצעה לא כתוב אם המחיר כולל מע"מ. בקשו שיהיה כתוב: ההפרש הוא 18%.'));
      notes.push(esc('המקורות שפרסמו את הטווחים לא תמיד ציינו אם הם כוללים מע"מ, ולכן ההשוואה היא לסכום כמו שהוא כתוב.'));
      var verdict = r.posM2 === 'in' ? 'המחיר בטווח הנפוץ' : r.posM2 === 'below' || r.posM2 === 'below_all' ? 'המחיר נמוך מהנפוץ' : 'המחיר גבוה מהנפוץ';
      return {
        answer: { label: verdict + ', ' + r.yes.length + ' מתוך ' + r.total + ' הפריטים כתובים בהצעה', value: num(Math.round(r.perM2)) + ' ₪ למ"ר', tone: bad ? 'survey' : '', sub: esc(R(rg(v.fee, v.fee), true) + ' ל־' + num(v.area) + ' מ"ר · הטווח הנפוץ ' + R(r.m2band, true) + ' למ"ר') },
        lines: lines,
        breakdown: [{ label: 'כתוב בהצעה', value: r.yes.length, kind: 'open', shown: String(r.yes.length) }, { label: 'לא כתוב', value: r.unk.length, kind: 'housing', shown: String(r.unk.length) }, { label: 'לא כלול', value: r.no.length, kind: 'survey', shown: String(r.no.length) }],
        note: notes.join('<br>'),
        table: { title: 'מה בודקים בהצעה, ומה עולים הפריטים כשמזמינים אותם בנפרד', head: ['פריט', 'בהצעה שלכם', 'בנפרד'], phoneHide: [],
          rows: QITEMS.map(function (q) { var s = v['i_' + q.k]; var b = q.p ? band(D.fees[q.p]) : null; return [q.he, s === 'yes' ? 'כלול' : s === 'no' ? 'לא כלול' : 'לא כתוב', b ? R(b, true) + ' ' + b.unit + rough(b) : 'אין מחיר נפרד שפורסם']; }) },
        formula: 'מחיר למטר = הסכום בהצעה ÷ שטח הדירה. "בתוך הטווח הנפוץ" = בין הקצה התחתון לעליון של הטווח שרוב המקורות נתנו; "מעל כל הטווח" = יותר מהמחיר הגבוה ביותר שמצאנו.',
        sources: srcLine([r.m2band, r.rooms.b]),
        text: 'הצעת מעצבת פנים: ' + num(Math.round(r.perM2)) + ' ₪ למ"ר, ' + POSHE[r.posM2] + ' (' + R(r.m2band, true) + ' למ"ר, ' + READ + '). כתוב בהצעה ' + r.yes.length + ' מתוך ' + r.total + ' פריטים.' + (r.no.length ? ' לא כלול: ' + r.no.map(function (x) { return x.he; }).join(', ') + '.' : '')
      };
    }
  });

  /* ---------------- dsgfurnish ---------------- */
  function furnishOut(r, v, title) {
    var rows = [];
    r.rooms.forEach(function (room) { room.lines.forEach(function (l) { rows.push([room.he + ': ' + l.b.name, R(l.r) + rough(l.b), VATS[l.b.vat] || 'לא צוין', String(l.b.n)]); }); });
    return rows;
  }
  NI.register('dsgfurnish', {
    kicker: 'מחשבון · ריהוט דירה',
    title: 'כמה עולה לרהט דירה',
    lede: 'בוחרים את מספר החדרים ואת הרמה, ורואים כמה עולה לרהט כל חדר: ספה, פינת אוכל, מיטות, ארונות, תאורה ומוצרי חשמל, לפי טווחי מחירים שפורסמו בישראל.',
    presets: [
      { key: 'r2', label: 'דירת 2 חדרים', sub: 'בסיסי', set: { rooms: 2, level: 'basic', balcony: 'no', study: 'no', appliances: 'yes' } },
      { key: 'r3', label: 'דירת 3 חדרים', sub: 'בינוני', set: { rooms: 3, level: 'mid', balcony: 'yes', study: 'no', appliances: 'yes' } },
      { key: 'r4', label: 'דירת 4 חדרים', sub: 'בינוני, עם מרפסת', set: { rooms: 4, level: 'mid', balcony: 'yes', study: 'no', appliances: 'yes' } },
      { key: 'r5', label: 'דירת 5 חדרים', sub: 'גבוה, עם חדר עבודה', set: { rooms: 5, level: 'high', balcony: 'yes', study: 'yes', appliances: 'yes' } }
    ],
    defaults: function () { return { rooms: 4, level: 'mid', balcony: 'yes', study: 'no', appliances: 'yes' }; },
    fields: [segNum('rooms', 'מספר חדרים (כולל הסלון)', ROOMSEG), { id: 'level', label: 'רמה', type: 'segmented', options: LEVELS },
      { id: 'balcony', label: 'פינת ישיבה במרפסת', type: 'segmented', options: YN }, { id: 'study', label: 'אחד החדרים הוא חדר עבודה', type: 'segmented', options: YN },
      { id: 'appliances', label: 'כולל מקרר ומדיח', type: 'segmented', options: YN }],
    compute: function (v, data) {
      var D = data.design, r = furnish(v, D);
      if (r.error) return pickErr(r.error, { rooms: 'בחרו מספר חדרים.' });
      var bs = []; r.rooms.forEach(function (x) { x.lines.forEach(function (l) { bs.push(l.b); }); });
      var kinds = ['sea', 'civic', 'housing', 'open', 'survey'];
      var notes = ['הכי משנה את הסכום: ' + r.swing.name + '. שם ההפרש בין זול ליקר הוא הגדול ביותר.'];
      if (r.published) notes.push('לבדיקה: ריהוט ' + r.published.name.replace(/^ריהוט /, '') + ' פורסם כסכום אחד לכל הדירה: ' + R(r.published.r) + (r.published.n < 2 ? ' (מקור אחד)' : ' (' + r.published.n + ' מקורות)') + '.');
      notes.push(LEVELNOTE);
      return {
        answer: { label: 'לרהט דירת ' + Math.round(v.rooms) + ' חדרים, ' + LEVELHE[r.level], value: R(r.total), sub: esc('מוצרים בלבד, בלי הובלה והרכבה · מחירים שנקראו ב' + READ) },
        breakdown: r.rooms.map(function (x, i) { return { label: x.he, value: mid(x.r), kind: kinds[i % kinds.length], shown: R(x.r) }; }),
        note: notes.map(esc).join('<br>'),
        table: { title: 'כל פריט וטווח המחיר שלו', head: PHEAD, num: [1], phoneHide: [3], rows: furnishOut(r) },
        formula: 'לכל חדר רשימה קבועה של רהיטים; לכל פריט החלק של הרמה שבחרתם מתוך הטווח שפורסם; הסכומים מתחברים. הסכום התחתון הוא כשכל פריט בקצה הזול, והעליון כשכולם בקצה היקר.',
        sources: srcLine(bs),
        text: 'ריהוט דירת ' + Math.round(v.rooms) + ' חדרים, ' + LEVELHE[r.level] + ': ' + R(r.total) + ' (טווחים שפורסמו, ' + READ + ').'
      };
    }
  });

  /* ---------------- dsgbudget ---------------- */
  NI.register('dsgbudget', {
    kicker: 'מחשבון · תקציב לעיצוב דירה',
    title: 'תקציב לעיצוב דירה חדשה',
    lede: 'כל מה שנכנס לתקציב של דירה חדשה מקבלן, אחרי המפתח: רהיטים, מעצב, מטבח, פרקט, מיזוג, נקודות חשמל, וילונות וצביעה, עם רזרבה. רואים כמה כל חלק לוקח מהסכום ומה הכי משנה אותו.',
    presets: [
      { key: 'r3', label: 'דירת 3 חדרים', sub: '80 מ"ר, בסיסי', set: { rooms: 3, area: 80, level: 'basic', designer: 'consult', kitchen: 'no', parquet: 'no', ac: 'yes', points: 4, curtains: 'yes', curtM2: 12, paint: 'no' } },
      { key: 'r4', label: 'דירת 4 חדרים', sub: '100 מ"ר, בינוני', set: { rooms: 4, area: 100, level: 'mid', designer: 'plan', kitchen: 'yes', kitchenM: 5, parquet: 'yes', parquetM2: 35, ac: 'yes', points: 8, curtains: 'yes', curtM2: 16, paint: 'no' } },
      { key: 'r5', label: 'דירת 5 חדרים', sub: '130 מ"ר, גבוה', set: { rooms: 5, area: 130, level: 'high', designer: 'full', kitchen: 'yes', kitchenM: 6, parquet: 'yes', parquetM2: 50, ac: 'yes', points: 12, curtains: 'yes', curtM2: 20, paint: 'no' } }
    ],
    defaults: function () { return { rooms: 4, area: 100, level: 'mid', designer: 'plan', kitchen: 'yes', kitchenM: 5, parquet: 'yes', parquetM2: 35, ac: 'yes', points: 8, curtains: 'yes', curtM2: 16, paint: 'no', reserve: 10 }; },
    fields: [
      segNum('rooms', 'מספר חדרים', ROOMSEG), { id: 'area', label: 'שטח הדירה', type: 'number', unit: 'מ"ר' },
      { id: 'level', label: 'רמה', type: 'segmented', options: LEVELS },
      { id: 'designer', label: 'מעצב פנים', type: 'segmented', options: [{ value: 'none', label: 'בלי' }, { value: 'consult', label: 'ייעוץ' }, { value: 'plan', label: 'תכנון' }, { value: 'full', label: 'ליווי מלא' }] },
      { id: 'kitchen', label: 'מטבח חדש במקום מטבח הקבלן', type: 'segmented', options: YN },
      { id: 'kitchenM', label: 'אורך המטבח', type: 'number', unit: 'מטר', showIf: function (v) { return v.kitchen === 'yes'; } },
      { id: 'parquet', label: 'פרקט עץ בחדרי השינה', type: 'segmented', options: YN },
      { id: 'parquetM2', label: 'שטח הפרקט', type: 'number', unit: 'מ"ר', showIf: function (v) { return v.parquet === 'yes'; } },
      { id: 'ac', label: 'מיזוג מיני מרכזי', type: 'segmented', options: YN },
      { id: 'points', label: 'נקודות חשמל נוספות', type: 'number', unit: 'נקודות' },
      { id: 'curtains', label: 'וילונות', type: 'segmented', options: YN },
      { id: 'curtM2', label: 'שטח החלונות לווילונות', type: 'number', unit: 'מ"ר', showIf: function (v) { return v.curtains === 'yes'; } },
      { id: 'paint', label: 'צביעה מחדש', type: 'segmented', options: YN },
      { id: 'reserve', label: 'רזרבה לבלתי צפוי', type: 'percent', unit: '%', help: 'כלל אצבע מקובל: 10% עד 15% מהסכום.' }
    ],
    compute: function (v, data) {
      var D = data.design, r = budget(v, D);
      if (r.error) return pickErr(r.error, { rooms: 'בחרו 2 עד 6 חדרים.', area: 'הקלידו שטח בין 30 ל־400 מ"ר.', kitchenM: 'הקלידו אורך מטבח במטרים.', parquetM2: 'שטח הפרקט לא יכול להיות גדול מהדירה.', curtM2: 'הקלידו את שטח החלונות.', reserve: 'רזרבה בין 0% ל־50%.' });
      var rows = r.cats.map(function (c) { return [c.he, R(c.r) + (c.rough ? ' (גס)' : '')]; });
      rows.push(['רזרבה ' + r.pct + '%', R(r.reserve)]);
      var room = [];
      r.furnish.rooms.forEach(function (x) { room.push([x.he, R(x.r)]); });
      var notes = ['הכי משנה את הסכום: ' + r.swing.he + ' (' + R(r.swing.r) + '). שם כדאי לקבל שתי הצעות או שלוש לפני שמחליטים.'];
      if (r.cats.some(function (c) { return c.k === 'ac'; })) notes.push('מיזוג: המקורות פרסמו מחיר לדירת 4 חדרים הכול כלול, והם סותרים זה את זה. בדירה אחרת המחיר שונה; זה טווח גס.');
      if (r.cats.some(function (c) { return c.k === 'paint'; })) notes.push('צביעה: המחיר שפורסם לדירת 4 חדרים, מותאם לשטח שלכם לפי 100 מ"ר לדירת 4 חדרים. טווח גס.');
      notes.push('מה שבדרך כלל כבר כלול בדירה מקבלן (ריצוף, חדרי רחצה, מטבח בסיסי) לא נספר כאן. ' + LEVELNOTE);
      return {
        answer: { label: 'התקציב לדירת ' + Math.round(v.rooms) + ' חדרים, ' + LEVELHE[r.level] + ', עם רזרבה', value: R(r.total), sub: esc('בלי הרזרבה: ' + R(r.sub) + ' · מחירים שנקראו ב' + READ) },
        breakdown: share(r.cats),
        lines: [{ label: 'רזרבה ' + r.pct + '%', value: R(r.reserve) }, { label: 'בלי הרזרבה', value: R(r.sub) }],
        note: notes.map(esc).join('<br>'),
        table: { title: 'הריהוט חדר אחרי חדר', head: ['חדר', 'טווח'], num: [1], rows: room },
        formula: 'כל שורה מחושבת כמו בכלי שלה (ריהוט, מעצב, מטבח), לפי אותם טווחים. סך הכול = סכום השורות + רזרבה באחוזים. הקצה התחתון כשהכול זול, העליון כשהכול יקר; בפועל רוב התקציבים באמצע.',
        sources: srcLine([band(D.items.sofa_3seat), band(D.items.engineered_parquet), band(D.items.ac_minicentral_4rooms_total), band(D.fees.fee_m2)]),
        text: 'תקציב לעיצוב דירה חדשה, ' + Math.round(v.rooms) + ' חדרים, ' + LEVELHE[r.level] + ': ' + R(r.total) + ' כולל רזרבה ' + r.pct + '% (' + READ + ').'
      };
    }
  });

  /* ---------------- dsgkitchen ---------------- */
  NI.register('dsgkitchen', {
    kicker: 'מחשבון · מטבח',
    title: 'כמה עולה מטבח: מחשבון לפי מטר',
    lede: 'מקלידים את אורך המטבח ובוחרים רמה, משטח, אי ומכשירים. רואים את המחיר של הארונות למטר, של המשטח ושל כל השאר, ומה הכי משנה את הסכום.',
    presets: [
      { key: 'm3', label: 'מטבח 3 מטר', sub: 'בסיסי, משטח קוורץ', set: { m: 3, level: 'basic', worktop: 'quartz', island: 'no', sink: 'yes', appl: 'none' } },
      { key: 'm4', label: 'מטבח 4 מטר', sub: 'בינוני, עם מכשירים לבישול', set: { m: 4, level: 'mid', worktop: 'quartz', island: 'no', sink: 'yes', appl: 'cook' } },
      { key: 'm6', label: 'מטבח 6 מטר עם אי', sub: 'גבוה, כל המכשירים', set: { m: 6, level: 'high', worktop: 'porcelain', island: 'yes', sink: 'yes', appl: 'full' } }
    ],
    defaults: function () { return { m: 4, level: 'mid', worktop: 'quartz', island: 'no', sink: 'yes', appl: 'cook' }; },
    fields: [
      { id: 'm', label: 'אורך המטבח (ארונות תחתונים)', type: 'number', unit: 'מטר' },
      { id: 'level', label: 'רמת הארונות', type: 'segmented', options: [{ value: 'basic', label: 'בסיסי' }, { value: 'mid', label: 'בינוני' }, { value: 'high', label: 'גבוה' }], help: 'בסיסי: פורמייקה או סנדוויץ\'. בינוני: פולימר, פורניר או צבע בתנור. גבוה: ננו או עץ מלא.' },
      { id: 'worktop', label: 'משטח עבודה', type: 'segmented', options: [{ value: 'quartz', label: 'קוורץ' }, { value: 'porcelain', label: 'גרניט פורצלן' }, { value: 'none', label: 'בלי' }] },
      { id: 'island', label: 'אי', type: 'segmented', options: YN }, { id: 'sink', label: 'כיור', type: 'segmented', options: YN },
      { id: 'appl', label: 'מכשירים', type: 'segmented', options: [{ value: 'none', label: 'בלי' }, { value: 'cook', label: 'תנור, כיריים וקולט' }, { value: 'full', label: 'הכול, כולל מקרר ומדיח' }] }
    ],
    compute: function (v, data) {
      var D = data.design, r = kitchen(v, D);
      if (r.error) return pickErr(r.error, { m: 'הקלידו אורך בין 1 ל־20 מטר.' });
      var kinds = { cab: 'sea', top: 'housing', island: 'civic', sink: 'open', oven_builtin: 'survey', hob: 'civic', hood: 'open', dishwasher: 'housing', fridge: 'sea' };
      var rows = r.parts.map(function (p) { return [p.he + (p.q > 1 ? ' × ' + p.q + ' מ\'' : ''), R(p.r) + rough(p.b), VATS[p.b.vat] || 'לא צוין', String(p.b.n)]; });
      var cab = (r.parts.filter(function (p) { return p.k === 'cab'; })[0] || {}).b;
      var notes = ['הכי משנה את הסכום: ' + r.swing.he + '.', 'לבדיקה: מטבח שלם בלי מכשירים פורסם בטווח ' + R(r.published) + '. אצלכם בלי מכשירים: ' + R(r.noAppl) + '.' + (r.missing.length ? ' חסר מחיר שפורסם ל־' + r.missing.length + ' פריטים, והם לא בסכום.' : ''),
        'המקורות לא מסכימים מה כלול ב"מחיר למטר": יש שכוללים ארונות עליונים ויש שלא. בקשו שיהיה כתוב.', 'תכנון מטבח אצל מעצב: ' + R(r.plan) + ' (גס, שני מקורות).'];
      if (r.parts.some(function (p) { return p.appl; })) notes.push('למכשירים אין טווח נפוץ, רק מהזול ליקר; זה טווח גס.');
      return {
        answer: { label: 'מטבח ' + num(v.m) + ' מטר, ' + LEVELHE[r.level], value: R(r.total), sub: esc((cab ? 'ארונות ' + R(cab, true) + ' למטר · ' : '') + 'מחירים שנקראו ב' + READ) },
        breakdown: r.parts.map(function (p) { return { label: p.he, value: mid(p.r), kind: kinds[p.k] || 'survey', shown: R(p.r) }; }),
        note: notes.map(esc).join('<br>'),
        table: { title: 'כל חלק וטווח המחיר שלו', head: PHEAD, num: [1], phoneHide: [3], rows: rows },
        formula: 'ארונות = אורך × המחיר למטר של הרמה. משטח = אורך × המחיר למטר. אי, כיור ומכשירים: החלק של הרמה מתוך הטווח שפורסם (שלישים שווים).',
        sources: srcLine(r.parts.map(function (p) { return p.b; })),
        text: 'מטבח ' + num(v.m) + ' מטר, ' + LEVELHE[r.level] + ': ' + R(r.total) + ' (טווחים שפורסמו, ' + READ + ').'
      };
    }
  });

  /* ---------------- dsgfloor ---------------- */
  NI.register('dsgfloor', {
    kicker: 'מחשבון · ריצוף ופרקט',
    title: 'מחשבון ריצוף ופרקט: כמה להזמין וכמה זה עולה',
    lede: 'מקלידים את השטח ובוחרים חומר וצורת הנחה. מקבלים כמה מטר להזמין עם הפחת, כמה קרטונים ומה המחיר כולל עבודה.',
    presets: [
      { key: 'p30', label: 'פרקט בחדרי שינה', sub: '30 מ"ר, עץ תלת שכבתי', set: { area: 30, type: 'engineered', pattern: 'straight', box: 2.0, skirt: 0 } },
      { key: 'spc', label: 'SPC לכל הדירה', sub: '90 מ"ר', set: { area: 90, type: 'spc', pattern: 'straight', box: 2.2, skirt: 0 } },
      { key: 'herr', label: 'פרקט פישבון', sub: '35 מ"ר', set: { area: 35, type: 'engineered', pattern: 'herringbone', box: 2.0, skirt: 0 } },
      { key: 't80', label: 'ריצוף 80×80', sub: '100 מ"ר', set: { area: 100, type: 'tile80', pattern: 'straight', box: 1.28, skirt: 0 } }
    ],
    defaults: function () { return { area: 30, type: 'engineered', pattern: 'straight', box: 2.0, skirt: 0 }; },
    fields: [
      { id: 'area', label: 'שטח הרצפה', type: 'number', unit: 'מ"ר' },
      { id: 'type', label: 'חומר', type: 'select', options: Object.keys(FLOOR).map(function (k) { return { value: k, label: FLOOR[k].he }; }) },
      { id: 'pattern', label: 'צורת ההנחה', type: 'segmented', options: [{ value: 'straight', label: 'ישר' }, { value: 'diagonal', label: 'באלכסון' }, { value: 'herringbone', label: 'פישבון' }] },
      { id: 'box', label: 'כמה מ"ר בקרטון', type: 'number', unit: 'מ"ר', help: 'כתוב על הקרטון. מתמלא לפי הנפוץ לכל חומר.' },
      { id: 'skirt', label: 'פנלים (לא חובה)', type: 'number', unit: 'מטר' }
    ],
    onField: function (id, v, data, redraw) { if (id === 'type') { v.box = (data.design.rules.box_m2.v || {})[v.type] || v.box; redraw('box'); } },
    compute: function (v, data) {
      var D = data.design, r = floor(v, D);
      if (r.error) return pickErr(r.error, { area: 'הקלידו שטח בין 1 ל־2,000 מ"ר.', box: 'הקלידו כמה מ"ר יש בקרטון.' });
      var notes = [];
      if (r.tiles) notes.push('לבדיקה: ריצוף פורצלן כולל חומר ועבודה פורסם גם כמחיר אחד, ' + R(band(D.items.tile_supplied_laid), true) + ' למ"ר, כלומר ' + R(r.cross) + ' לשטח שלכם.');
      else notes.push('המחיר כולל התקנה ונמדד על שטח הרצפה. הפחת כבר בתוך מחיר המתקין; את מספר הקרטונים צריך אם קונים את החומר לבד.');
      if (v.pattern !== 'straight') notes.push('הנחה באלכסון או בפישבון לוקחת יותר עבודה. לא מצאנו מחיר עבודה נפרד שפורסם, אז בקשו הצעה.');
      notes.push('הפחת לפי כלל אצבע של מתקינים: ישר 5% עד 10%, אלכסון ופישבון 15% ויותר.');
      return {
        answer: { label: r.he + ', ' + num(v.area) + ' מ"ר', value: R(r.total), sub: esc('להזמין ' + num(r.boxes) + ' קרטונים (' + F.num(r.boxArea, 2) + ' מ"ר, ' + r.waste + '% פחת) · מחירים שנקראו ב' + READ) },
        lines: [{ label: 'שטח עם פחת ' + r.waste + '%', value: F.num(r.ordered, 1) + ' מ"ר' }, { label: 'קרטונים של ' + F.num(r.box, 2) + ' מ"ר', value: num(r.boxes) + ' קרטונים' }]
          .concat(r.parts.map(function (p) { return { label: p.he, value: R(p.r) }; })),
        breakdown: r.parts.map(function (p, i) { return { label: p.he, value: mid(p.r), kind: ['sea', 'housing', 'civic'][i % 3], shown: R(p.r) }; }),
        note: notes.map(esc).join('<br>'),
        table: { title: 'המחירים למ"ר שפורסמו לכל חומר', head: PHEAD, num: [1], phoneHide: [3], rows: ['tile_material_60', 'tile_material_80', 'tile_material_120', 'tile_laying', 'tile_supplied_laid', 'laminate', 'engineered_parquet', 'spc_vinyl', 'skirting']
          .map(function (id) { return band(D.items[id]); }).filter(Boolean).map(function (b) { return itemRow(b, null, b.name.replace(/^אריח /, '')); }) },
        formula: 'להזמין = שטח × (1 + פחת), ואז חלקי מ"ר בקרטון, מעוגל למעלה. פורצלן: החומר על השטח עם הפחת, העבודה על שטח הרצפה. פרקט: מחיר כולל התקנה × שטח הרצפה.',
        sources: srcLine(r.parts.map(function (p) { return p.b; })),
        text: r.he + ', ' + num(v.area) + ' מ"ר: ' + num(r.boxes) + ' קרטונים, ' + R(r.total) + ' (טווחים שפורסמו, ' + READ + ').'
      };
    }
  });

  /* ---------------- dsgpaint ---------------- */
  NI.register('dsgpaint', {
    kicker: 'מחשבון · צביעת דירה',
    title: 'מחשבון צביעת דירה: כמה צבע וכמה זה עולה',
    lede: 'לפי מידות החדרים או לפי שטח הדירה: שטח הקירות בלי הדלתות והחלונות, כמה ליטר צבע ואילו פחים לקנות, ומה המחיר אצל צבעי מול צביעה לבד.',
    presets: [
      { key: 'r3', label: 'דירת 3 חדרים', sub: '80 מ"ר, קירות בלבד', set: { mode: 'quick', area: 80, rooms: 3, ceiling: 'no', doors: 5, windows: 5 } },
      { key: 'r4', label: 'דירת 4 חדרים', sub: '100 מ"ר, עם תקרות', set: { mode: 'quick', area: 100, rooms: 4, ceiling: 'yes', doors: 6, windows: 6 } },
      { key: 'r5', label: 'דירת 5 חדרים', sub: '130 מ"ר, קירות בלבד', set: { mode: 'quick', area: 130, rooms: 5, ceiling: 'no', doors: 7, windows: 8 } },
      { key: 'room', label: 'חדר אחד', sub: '3 × 3.5 מ\'', set: { mode: 'rooms', rows: [{ l: 3.5, w: 3 }], ceiling: 'yes', doors: 1, windows: 1 } }
    ],
    defaults: function () { return { mode: 'quick', area: 100, rooms: 4, rows: [{ l: 5, w: 4 }, { l: 3.5, w: 3 }, { l: 3, w: 3 }], h: 2.6, doors: 6, windows: 6, winM2: 1.5, ceiling: 'no', coats: 2, cover: 10, can18: 0 }; },
    fields: [
      { id: 'mode', label: 'איך מודדים', type: 'segmented', options: [{ value: 'quick', label: 'לפי שטח הדירה' }, { value: 'rooms', label: 'חדר אחרי חדר' }] },
      { id: 'area', label: 'שטח הדירה', type: 'number', unit: 'מ"ר', showIf: function (v) { return v.mode === 'quick'; } },
      { id: 'rooms', label: 'מספר חדרים', type: 'number', showIf: function (v) { return v.mode === 'quick'; } },
      { id: 'rows', label: 'אורך ורוחב של כל חדר (מטר)', type: 'rows', addLabel: 'הוספת חדר', cols: [{ id: 'l', label: 'אורך', unit: 'מ\'' }, { id: 'w', label: 'רוחב', unit: 'מ\'' }], blank: function () { return { l: 3, w: 3 }; }, showIf: function (v) { return v.mode === 'rooms'; } },
      { id: 'h', label: 'גובה התקרה', type: 'number', unit: 'מטר' },
      { id: 'doors', label: 'דלתות', type: 'number' },
      { id: 'windows', label: 'חלונות', type: 'number' },
      { id: 'winM2', label: 'גודל חלון ממוצע', type: 'number', unit: 'מ"ר' },
      { id: 'ceiling', label: 'גם תקרות', type: 'segmented', options: YN },
      { id: 'coats', label: 'כמה פעמים צובעים', type: 'segmented', options: [{ value: 1, label: 'פעם אחת' }, { value: 2, label: 'פעמיים' }, { value: 3, label: 'שלוש' }] },
      { id: 'cover', label: 'כמה מ"ר צובע ליטר', type: 'number', unit: 'מ"ר', help: 'כתוב על הפח. כלל אצבע לצבע אקרילי לפנים: 8 עד 12.' },
      { id: 'can18', label: 'מחיר פח של 18 ליטר, אם בדקתם (לא חובה)', type: 'money', unit: '₪', help: 'אין לנו מחיר צבע שפורסם; עם המחיר שלכם נחשב כמה תעלה צביעה לבד.' }
    ],
    compute: function (v, data) {
      var D = data.design, r = paint(v, D);
      if (r.error) return pickErr(r.error, { h: 'גובה בין 2 ל־6 מטר.', rows: 'הקלידו אורך ורוחב של חדר אחד לפחות.', area: 'הקלידו שטח בין 10 ל־1,000 מ"ר.', rooms: 'הקלידו מספר חדרים.' });
      var c = r.cans, canTxt = [c.n18 ? c.n18 + ' × 18 ליטר' : '', c.n5 ? c.n5 + ' × 5 ליטר' : '', c.n1 ? c.n1 + ' × ליטר' : ''].filter(Boolean).join(' + ') || 'אין צורך';
      var ratio = r.painter && r.flat4 ? mid(r.painter) / mid(r.flat4) * (100 / Math.max(1, r.floorA)) : 1;
      var notes = ['שני סוגי מחירים פורסמו: לפי מ"ר קיר (' + R(r.pb, true) + ') ולדירת 4 חדרים שלמה (' + R(r.p4) + '). '
        + (ratio > 1.5 ? 'לפי מ"ר קיר יוצא יותר בבירור מהמחיר לדירה שלמה: יש צבעים שמתמחרים לפי מ"ר רצפה ולא קיר. שאלו את הצבע לפי מה הוא מודד.' : 'שתי הדרכים קרובות.')];
      if (r.diy != null) notes.push('צביעה לבד: הצבע כ־' + R(rg(r.diy, r.diy)) + ', בלי מברשות, גלילים, ניילון ושפכטל.');
      else notes.push('צביעה לבד חוסכת את העבודה, ומוסיפה את הצבע: ' + F.num(c.litres) + ' ליטר. הקלידו מחיר של פח 18 ליטר כדי לראות את הסכום.');
      if (v.mode === 'quick') notes.push('לפי שטח הדירה מניחים חדרים קרובים לריבוע: ' + r.spaces + ' חללים (החדרים, המטבח וחדר רחצה או מסדרון). למדידה מדויקת עברו ל"חדר אחרי חדר".');
      return {
        answer: { label: 'צבעי, ' + F.num(r.area, 0) + ' מ"ר ' + (r.ceil ? 'קירות ותקרות' : 'קירות'), value: R(r.painter), sub: esc(F.num(r.litres, 0) + ' ליטר צבע: ' + canTxt + ' · ' + (r.pb ? VAT[r.pb.vat] + ' · ' : '') + READ) },
        lines: [{ label: 'שטח הקירות', value: F.num(r.walls, 0) + ' מ"ר' }, { label: 'פחות דלתות וחלונות', value: F.num(r.openings, 0) + ' מ"ר' }, { label: 'תקרות', value: F.num(r.ceil, 0) + ' מ"ר' },
          { label: 'שטח לצביעה × ' + r.coats + ' ÷ ' + r.cover + ' מ"ר לליטר', value: F.num(r.litres, 1) + ' ליטר' }, { label: 'פחים', value: canTxt },
          { label: 'צבעי, לפי מ"ר', value: R(r.painter) }, { label: 'צבעי, דירת 4 חדרים שלמה (לבדיקה)', value: R(r.p4) }],
        breakdown: [{ label: 'קירות', value: r.net, kind: 'sea', shown: F.num(r.net, 0) + ' מ"ר' }, { label: 'תקרות', value: r.ceil, kind: 'housing', shown: F.num(r.ceil, 0) + ' מ"ר' }],
        note: notes.map(esc).join('<br>'),
        formula: 'קירות = היקף החדר × הגובה; פחות דלת של 1.7 מ"ר וכל חלון לפי הגודל שהקלדתם. ליטרים = שטח × מספר הפעמים ÷ מ"ר לליטר. פחים: קודם 18 ליטר, אחר כך 5, ואז ליטר.',
        sources: srcLine([r.pb, r.p4]),
        text: 'צביעת ' + F.num(r.area, 0) + ' מ"ר: ' + F.num(r.litres, 0) + ' ליטר (' + canTxt + '), צבעי ' + R(r.painter) + ' (' + READ + ').'
      };
    }
  });

  /* ---------------- dsgsofa ---------------- */
  var CHK = { ok: 'עובר', tight: 'צפוף', maybe: 'אולי, תלוי בזווית', no: 'לא עובר', skip: 'לא נבדק' };
  var SHORT = { wall: 'הקיר', front: 'המעבר', door: 'הפתח', turn: 'הפנייה', lift: 'המעלית' };
  NI.register('dsgsofa', {
    kicker: 'בדיקה · מידות ספה לסלון',
    title: 'האם הספה תיכנס',
    lede: 'מידות הקיר, הסלון והספה, ואם צריך גם הדלת, המסדרון והמעלית. רואים בשרטוט בקנה מידה אם יש מקום למעבר, ואם הספה תעבור בפתח ובפנייה.',
    presets: [
      { key: 's3', label: 'ספה תלת מושבית', sub: '220 × 95 ס"מ', set: { L: 220, d: 95, h: 85, path: 'no' } },
      { key: 's2', label: 'ספה דו מושבית', sub: '170 × 90 ס"מ', set: { L: 170, d: 90, h: 85, path: 'no' } },
      { key: 'corner', label: 'ספה פינתית ארוכה', sub: '300 × 100 ס"מ', set: { L: 300, d: 100, h: 85, path: 'no' } },
      { key: 'way', label: 'הדרך פנימה', sub: 'פתח 90, מסדרון 110', set: { path: 'yes', door: 90, hall: 110, ceil: 260, lift: 'no' } },
      { key: 'lift', label: 'עם מעלית אלונקה', sub: 'תא 110 × 210', set: { path: 'yes', lift: 'yes', lw: 110, ld: 210, lh: 220 } }
    ],
    defaults: function () { return { W: 420, Dp: 380, L: 240, d: 95, h: 85, table: 60, path: 'no', door: 90, hall: 110, ceil: 260, lift: 'no', lw: 110, ld: 210, lh: 220 }; },
    fields: [
      { id: 'W', label: 'אורך הקיר של הספה', type: 'number', unit: 'ס"מ' }, { id: 'Dp', label: 'עומק הסלון, מהקיר עד הטלוויזיה', type: 'number', unit: 'ס"מ' },
      { id: 'L', label: 'אורך הספה', type: 'number', unit: 'ס"מ' }, { id: 'd', label: 'עומק הספה', type: 'number', unit: 'ס"מ' }, { id: 'h', label: 'גובה הספה', type: 'number', unit: 'ס"מ' },
      { id: 'table', label: 'עומק שולחן הסלון (0 = בלי)', type: 'number', unit: 'ס"מ' },
      { id: 'path', label: 'לבדוק גם את הדרך פנימה: הפתח, המסדרון והמעלית', type: 'segmented', options: YN },
      { id: 'door', showIf: function (v) { return v.path === 'yes'; }, label: 'רוחב פתח הכניסה, נטו', type: 'number', unit: 'ס"מ', help: 'מהמשקוף למשקוף, כשהדלת פתוחה עד הסוף.' },
      { id: 'hall', showIf: function (v) { return v.path === 'yes'; }, label: 'רוחב המסדרון אחרי הפתח (0 = אין פנייה)', type: 'number', unit: 'ס"מ' },
      { id: 'ceil', label: 'גובה התקרה במסדרון', type: 'number', unit: 'ס"מ', showIf: function (v) { return v.path === 'yes' && v.hall > 0; }, help: 'כשהספה לא עוברת שטוחה, מובילים מעבירים אותה עומדת על הצד. לכך צריך תקרה גבוהה מאורך הספה.' },
      { id: 'lift', label: 'עולים במעלית', type: 'segmented', options: YN, showIf: function (v) { return v.path === 'yes'; } },
      { id: 'lw', label: 'רוחב תא המעלית', type: 'number', unit: 'ס"מ', showIf: function (v) { return v.path === 'yes' && v.lift === 'yes'; } },
      { id: 'ld', label: 'עומק תא המעלית', type: 'number', unit: 'ס"מ', showIf: function (v) { return v.path === 'yes' && v.lift === 'yes'; } },
      { id: 'lh', label: 'גובה תא המעלית', type: 'number', unit: 'ס"מ', showIf: function (v) { return v.path === 'yes' && v.lift === 'yes'; } }
    ],
    compute: function (v, data) {
      var D = data.design, r = sofaFit(v.path === 'yes' ? v : Object.assign({}, v, { door: 0, hall: 0, lift: 'no' }), D);
      if (r.error) return pickErr(r.error, { W: 'הקלידו את אורך הקיר בס"מ.', Dp: 'הקלידו את עומק הסלון בס"מ.', L: 'הקלידו את אורך הספה.', d: 'הקלידו את עומק הספה.', h: 'הקלידו את גובה הספה.' });
      var wall = v.W, sx = Math.max(0, (wall - v.L) / 2), front = r.front;
      var fig = plan(Math.max(wall, v.L), v.Dp, function (g, P) {
        var tY = v.d + r.gap, wY = tY + r.table;
        if (r.table) g.push(box(P, sx + v.L * 0.2, tY, v.L * 0.6, r.table, C.wood, '#8A6E58', 'שולחן'));
        if (front > 0) g.push('<rect x="' + P.x(0) + '" y="' + P.y(wY) + '" width="' + P.s(Math.max(wall, v.L)) + '" height="' + P.s(Math.max(0, v.Dp - wY)) + '" fill="' + (r.c.front === 'no' ? 'url(#nldsh)' : (r.c.front === 'tight' ? '#FBEFC4' : '#E3F1E5')) + '"/>');
        g.push('<text x="' + P.x(Math.max(wall, v.L) / 2) + '" y="' + (+P.y(wY + Math.max(0, v.Dp - wY) / 2) + 4).toFixed(1) + '" text-anchor="middle" class="m' + (r.c.front === 'no' ? ' bad' : '') + '">מעבר ' + Math.round(front) + ' ס"מ</text>');
        g.push(box(P, sx, 0, v.L, v.d, C.sofaF, r.c.wall === 'no' ? C.bad : C.sofa, 'ספה ' + v.L + ' ס"מ'));
        g.push('<line x1="' + P.x(0) + '" y1="' + P.y(v.Dp) + '" x2="' + P.x(Math.max(wall, v.L)) + '" y2="' + P.y(v.Dp) + '" stroke="#12202A" stroke-width="6"/>');
        g.push('<text x="' + P.x(Math.max(wall, v.L) / 2) + '" y="' + (+P.y(v.Dp) - 6).toFixed(1) + '" text-anchor="middle" class="t">קיר הטלוויזיה</text>');
      }, 'שרטוט הסלון בקנה מידה: ספה של ' + v.L + ' ס"מ על קיר של ' + v.W + ' ס"מ, מעבר של ' + Math.round(front) + ' ס"מ');
      var lines = [
        { label: 'על הקיר (' + v.L + ' מול ' + v.W + ' ס"מ)', value: CHK[r.c.wall] },
        { label: 'מעבר מול הספה: ' + Math.round(front) + ' ס"מ (נוח 90, אפשרי 60)', value: CHK[r.c.front] },
        { label: 'בפתח הכניסה: הצד הצר של הספה ' + r.thin + ' ס"מ', value: CHK[r.c.door] },
        { label: r.turn == null ? 'פנייה במסדרון' : 'פנייה במסדרון: עוברת ספה עד ' + Math.floor(r.turn) + ' ס"מ', value: CHK[r.c.turn] },
        { label: 'מעלית', value: CHK[r.c.lift] }
      ];
      var notes = [];
      if (r.c.turn === 'no' || r.c.turn === 'maybe') notes.push('בפנייה החישוב מניח שמובילים את הספה שטוחה. מובילים מנוסים מטים אותה לגובה ולפעמים מפרקים רגליים או משענות, וזה מוסיף כמה סנטימטרים. לפני הזמנה, שאלו את החנות.');
      if (r.c.lift === 'maybe') notes.push('במעלית הספה נכנסת רק באלכסון ובהטיה. שווה למדוד את התא באמת ולשאול את המובילים.');
      if (r.c.front !== 'ok') notes.push('אפשר שולחן סלון צר יותר, ספה פחות עמוקה, או מזנון צר מול הספה.');
      notes.push('מעבר נוח 90 ס"מ ומעבר אפשרי 60 ס"מ הם כללי אצבע מקובלים בתכנון פנים; בין הספה לשולחן משאירים 40 עד 50 ס"מ.');
      var verdict = r.worst === 'ok' ? 'הספה נכנסת' : r.worst === 'no' ? 'הספה לא נכנסת כמו שהיא' : 'נכנסת, אבל צפוף';
      return {
        answer: { label: 'ספה ' + v.L + ' × ' + v.d + ' ס"מ', value: verdict, tone: r.worst === 'no' ? 'survey' : '', sub: esc(['wall', 'front', 'door', 'turn', 'lift'].filter(function (k) { return RANK[r.c[k]] > 0; }).map(function (k) { return SHORT[k] + ': ' + CHK[r.c[k]]; }).join(' · ') || 'כל הבדיקות עברו') },
        figure: fig, lines: lines, note: notes.map(esc).join('<br>'),
        formula: 'מעבר = עומק הסלון − עומק הספה − 45 ס"מ − עומק השולחן. פתח: הצד הצר של הספה (עומק או גובה) + 2 ס"מ. פנייה: האורך הגדול ביותר של מלבן בעובי הספה שמסתובב בפינה ישרה בין הפתח למסדרון, כשהוא שטוח; אם לא עובר שטוח אבל התקרה גבוהה מאורך הספה, "אולי" (עומדת על הצד). מעלית: הספה עומדת על הצד, או שוכבת באלכסון התא.',
        sources: [{ label: 'כללי אצבע מקובלים בתכנון פנים; חישוב הפנייה הוא גאומטריה' }],
        text: 'ספה ' + v.L + ' × ' + v.d + ' ס"מ בסלון ' + v.W + ' × ' + v.Dp + ' ס"מ: ' + verdict + '. ' + lines.map(function (l) { return l.label + ': ' + l.value; }).join('; ') + '.'
      };
    }
  });

  /* ---------------- dsgrug ---------------- */
  NI.register('dsgrug', {
    kicker: 'בחירה · גודל שטיח לסלון',
    title: 'איזה גודל שטיח לסלון',
    lede: 'מידות הספה והסלון, והמרחק עד המזנון. רואים איזו מידה מוכנה מתאימה לפינת הישיבה, בשרטוט בקנה מידה, ומה המחיר שלה.',
    presets: [
      { key: 'small', label: 'סלון קטן', sub: 'ספה 180, סלון 3.2 × 3.5', set: { L: 180, d: 90, f: 170, rw: 320, rd: 350, lay: 'front' } },
      { key: 'mid', label: 'סלון בינוני', sub: 'ספה 220, סלון 4 × 4', set: { L: 220, d: 95, f: 230, rw: 400, rd: 400, lay: 'front' } },
      { key: 'big', label: 'סלון גדול', sub: 'ספה 280, כל הרגליים על השטיח', set: { L: 280, d: 100, f: 260, rw: 520, rd: 480, lay: 'all' } }
    ],
    defaults: function () { return { L: 220, d: 95, f: 230, rw: 400, rd: 400, lay: 'front' }; },
    fields: [
      { id: 'L', label: 'אורך הספה', type: 'number', unit: 'ס"מ' }, { id: 'd', label: 'עומק הספה', type: 'number', unit: 'ס"מ' },
      { id: 'f', label: 'מקדמת הספה עד המזנון', type: 'number', unit: 'ס"מ' },
      { id: 'rw', label: 'רוחב הסלון (לאורך הספה)', type: 'number', unit: 'ס"מ' }, { id: 'rd', label: 'עומק הסלון', type: 'number', unit: 'ס"מ' },
      { id: 'lay', label: 'איך השטיח מונח', type: 'segmented', options: [{ value: 'front', label: 'רגליים קדמיות על השטיח' }, { value: 'all', label: 'כל הספה על השטיח' }] }
    ],
    compute: function (v, data) {
      var D = data.design, r = rugPick(v, D);
      if (r.error) return pickErr(r.error, { L: 'הקלידו את אורך הספה.', d: 'הקלידו את עומק הספה.', f: 'הקלידו את המרחק עד המזנון.', rw: 'הקלידו את רוחב הסלון.', rd: 'הקלידו את עומק הסלון.' });
      var p = r.pick, label = p ? p[1] + ' × ' + p[0] + ' ס"מ' : 'אין מידה מוכנה שנכנסת';
      var fig = plan(v.rw, v.rd, function (g, P) {
        var sx = Math.max(0, (v.rw - v.L) / 2), wall = 30, sy = wall;
        if (p) { var rx = (v.rw - p[0]) / 2, ry = v.lay === 'all' ? sy - 10 : sy + v.d - 20; g.push(box(P, rx, ry, p[0], p[1], C.rug, '#B8962A', '')); g.push('<text x="' + P.x(rx + p[0] / 2) + '" y="' + (+P.y(ry + p[1]) - 6).toFixed(1) + '" text-anchor="middle" class="m">שטיח ' + p[1] + ' על ' + p[0] + '</text>'); }
        g.push(box(P, sx, sy, v.L, v.d, C.sofaF, C.sofa, 'ספה'));
        var cy = Math.min(v.rd - 45, sy + v.d + v.f); g.push(box(P, Math.max(0, (v.rw - 160) / 2), cy, Math.min(160, v.rw), 40, C.wood, '#8A6E58', 'מזנון'));
      }, 'שרטוט בקנה מידה: ' + label + ' מול ספה של ' + v.L + ' ס"מ בסלון של ' + v.rw + ' על ' + v.rd + ' ס"מ');
      var msg = r.status === 'ok' ? 'מתאים לפינת הישיבה ומשאיר רצפה גלויה ליד הקירות' : r.status === 'small' ? 'הגדול ביותר שנכנס לסלון; קטן מהאידיאלי' : 'הסלון קטן מכל המידות המוכנות; שקלו שטיח בהזמנה';
      return {
        answer: { label: 'המידה שמתאימה', value: label, tone: r.status === 'ok' ? '' : 'survey', sub: esc(msg) },
        figure: fig,
        lines: [{ label: 'רוחב שצריך: הספה + 15 ס"מ מכל צד', value: Math.round(r.needW) + ' ס"מ' }, { label: 'עומק שצריך', value: Math.round(r.needD) + ' ס"מ' },
          { label: 'הכי גדול שנכנס (30 ס"מ מכל קיר)', value: Math.round(r.maxD) + ' × ' + Math.round(r.maxW) + ' ס"מ' },
          { label: 'מחיר', value: r.price ? R(r.price, true) + rough(r.price) : 'אין מחיר שפורסם למידה הזאת' }],
        note: esc('כללי סטיילינג מקובלים: השטיח בולט 15 עד 20 ס"מ מכל צד של הספה, הרגליים הקדמיות עומדות עליו, ונשארת רצפה גלויה ליד הקירות (מקובל 15 עד 50 ס"מ; כאן 30). ' + (r.price ? 'מחיר: ' + VAT[r.price.vat] + ', ' + r.price.n + ' מקורות. שטיח סינתטי בתחתית הטווח, צמר ועבודת יד בראשו.' : '')),
        formula: 'רוחב = אורך הספה + 30. עומק, רגליים קדמיות: 20 ס"מ מתחת לספה ועד 15 ס"מ לפני המזנון. כל הספה: עומק הספה + המרחק עד המזנון − 5. בוחרים את המידה המוכנה הקטנה ביותר שגדולה מהצורך ונכנסת לסלון.',
        sources: r.price ? srcLine([r.price]) : [{ label: 'כללי סטיילינג מקובלים' }],
        text: 'שטיח לסלון עם ספה של ' + v.L + ' ס"מ: ' + label + (r.price ? ', ' + R(r.price, true) : '') + '.'
      };
    }
  });

  /* ---------------- dsgdining ---------------- */
  var PASS = [{ value: 'wall', label: 'צמוד לקיר, בלי מעבר' }, { value: 'edge', label: 'עוברים בצד' }, { value: 'walk', label: 'עוברים מאחורי הכיסאות' }];
  NI.register('dsgdining', {
    kicker: 'בדיקה · פינת אוכל',
    title: 'פינת אוכל: כמה מקום צריך לשולחן ולכסאות',
    lede: 'מידות פינת האוכל ומספר הסועדים. מקבלים את גודל השולחן, את המרווח מאחורי הכיסאות, שרטוט בקנה מידה, ואת מספר הסועדים הגדול ביותר שנכנס.',
    presets: [
      { key: 'n4', label: '4 סועדים', sub: 'פינה 2.6 × 2.8', set: { W: 260, Dp: 280, n: 4, shape: 'rect', pass: 'edge' } },
      { key: 'n6', label: '6 סועדים', sub: 'פינה 3 × 3.6', set: { W: 300, Dp: 360, n: 6, shape: 'rect', pass: 'edge' } },
      { key: 'n8', label: '8 סועדים', sub: 'פינה 3.4 × 4.4', set: { W: 340, Dp: 440, n: 8, shape: 'rect', pass: 'walk' } },
      { key: 'round', label: 'שולחן עגול', sub: '4 סועדים, 2.8 × 2.8', set: { W: 280, Dp: 280, n: 4, shape: 'round', pass: 'edge' } }
    ],
    defaults: function () { return { W: 300, Dp: 360, n: 6, shape: 'rect', pass: 'edge' }; },
    fields: [
      { id: 'W', label: 'רוחב פינת האוכל', type: 'number', unit: 'ס"מ' }, { id: 'Dp', label: 'אורך פינת האוכל', type: 'number', unit: 'ס"מ' },
      { id: 'n', label: 'כמה סועדים', type: 'number' },
      { id: 'shape', label: 'שולחן', type: 'segmented', options: [{ value: 'rect', label: 'מלבני' }, { value: 'round', label: 'עגול' }] },
      { id: 'pass', label: 'מאחורי הכיסאות', type: 'segmented', options: PASS }
    ],
    compute: function (v, data) {
      var D = data.design, r = dining(v, D);
      if (r.error) return pickErr(r.error, { W: 'רוחב בין 100 ל־3,000 ס"מ.', Dp: 'אורך בין 100 ל־3,000 ס"מ.', n: 'בין 2 ל־16 סועדים.' });
      var t = r.t, A = Math.max(v.W, v.Dp), B = Math.min(v.W, v.Dp), rot = v.W >= v.Dp;
      var fig = plan(v.W, v.Dp, function (g, P) {
        var cx = v.W / 2, cy = v.Dp / 2, tl = rot ? t.l : t.w, tw = rot ? t.w : t.l;  // tl, tw: the table along x and along y
        if (!t.round) g.push('<rect x="' + P.x(Math.max(0, cx - tl / 2 - (rot ? r.end : r.c))) + '" y="' + P.y(Math.max(0, cy - tw / 2 - (rot ? r.c : r.end))) + '" width="' + P.s(Math.min(v.W, tl + 2 * (rot ? r.end : r.c))) + '" height="' + P.s(Math.min(v.Dp, tw + 2 * (rot ? r.c : r.end))) + '" fill="' + (r.status === 'no' ? 'url(#nldsh)' : '#E3F1E5') + '" stroke="' + (r.status === 'no' ? C.bad : C.ok) + '" stroke-dasharray="4 3"/>');
        else g.push('<circle cx="' + P.x(cx) + '" cy="' + P.y(cy) + '" r="' + P.s(t.l / 2 + r.c) + '" fill="' + (r.status === 'no' ? 'url(#nldsh)' : '#E3F1E5') + '" stroke="' + (r.status === 'no' ? C.bad : C.ok) + '" stroke-dasharray="4 3"/>');
        if (t.round) g.push('<circle cx="' + P.x(cx) + '" cy="' + P.y(cy) + '" r="' + P.s(t.l / 2) + '" fill="' + C.wood + '" stroke="#8A6E58" stroke-width="1.4"/>');
        else g.push(box(P, cx - tl / 2, cy - tw / 2, tl, tw, C.wood, '#8A6E58', ''));
        // chairs, 45 cm squares, half under the table edge
        var n = Math.round(v.n), cs = 45;
        if (t.round) { for (var i = 0; i < n; i++) { var a = 2 * Math.PI * i / n, rr = t.l / 2 + 8; g.push('<rect x="' + P.x(cx + Math.cos(a) * rr - cs / 2) + '" y="' + P.y(cy + Math.sin(a) * rr - cs / 2) + '" width="' + P.s(cs) + '" height="' + P.s(cs) + '" fill="' + C.sofaF + '" stroke="' + C.sofa + '"/>'); } }
        else {
          var side = Math.ceil(n / 2);
          [side, n - side].forEach(function (k, s) {
            for (var j = 0; j < k; j++) {
              var p = -t.l / 2 + (t.l / k) * (j + 0.5) - cs / 2, off = s ? t.w / 2 - 15 : -t.w / 2 - cs + 15;  // along the long side; half a chair under the edge
              var x = rot ? cx + p : cx + off, y = rot ? cy + off : cy + p;
              g.push('<rect x="' + P.x(x) + '" y="' + P.y(y) + '" width="' + P.s(cs) + '" height="' + P.s(cs) + '" fill="' + C.sofaF + '" stroke="' + C.sofa + '"/>');
            }
          });
        }
        g.push('<text x="' + P.x(cx) + '" y="' + (+P.y(cy) + 4).toFixed(1) + '" text-anchor="middle" class="m">' + (t.round ? 'קוטר ' + t.l : t.l + ' על ' + t.w) + '</text>');
      }, 'שרטוט פינת האוכל בקנה מידה: שולחן ' + (t.round ? 'עגול בקוטר ' + t.l : t.l + ' על ' + t.w) + ' ס"מ ל־' + Math.round(v.n) + ' סועדים');
      var verdict = r.status === 'ok' ? 'נכנס, עם המרווח שבחרתם' : r.status === 'tight' ? 'נכנס רק בלי מעבר מאחור' : 'לא נכנס';
      return {
        answer: { label: 'שולחן ' + (t.round ? 'עגול בקוטר ' + t.l : t.l + ' × ' + t.w) + ' ס"מ ל־' + Math.round(v.n), value: verdict, tone: r.status === 'ok' ? '' : 'survey', sub: esc('הכי הרבה סועדים שנכנסים כאן עם המרווח הזה: ' + (r.most || 'אף שולחן')) },
        figure: fig,
        lines: [{ label: 'מרווח מקצה השולחן, ' + PASS.filter(function (p) { return p.value === v.pass; })[0].label, value: r.c + ' ס"מ' },
          { label: r.spare >= 0 ? 'נשאר מקום פנוי' : 'חסר מקום', value: Math.abs(Math.round(r.spare)) + ' ס"מ' },
          { label: r.price.how === 'set' ? 'פינת אוכל עם 6 כסאות' : 'שולחן ו־' + Math.round(v.n) + ' כסאות', value: R(r.price.r) + rough(r.price.b) }],
        note: esc('המרווחים לפי הנחיות תכנון מקובלות למטבח ולפינת ישיבה: 81 ס"מ מקצה השולחן כשאין מעבר, 91 כשעוברים בצד, 112 כשעוברים מאחורי סועד. 60 ס"מ לכל סועד בשולחן מלבני. ' + (r.price.b ? 'מחיר: ' + VAT[r.price.b.vat] + (r.price.how === 'parts' ? '; השולחן לפי מחיר שולחן ל־6, לגדול יותר זה גס.' : '.') : 'אין מחיר שפורסם.')),
        formula: 'שולחן מלבני: אורך = מספר הסועדים בצד הארוך × 60 ס"מ, עומק 90. שולחן עגול: קוטר = סועדים × 65 ÷ π, מעוגל ל־10. צריך: שולחן + מרווח מכל צד שיש בו כיסאות, ו־60 ס"מ בקצוות.',
        sources: srcLine([r.price.b]),
        text: 'פינת אוכל ' + v.W + ' × ' + v.Dp + ' ס"מ, ' + Math.round(v.n) + ' סועדים: ' + verdict + '. שולחן ' + (t.round ? 'עגול ' + t.l : t.l + ' × ' + t.w) + ' ס"מ.'
      };
    }
  });

  /* ---------------- dsgbed ---------------- */
  NI.register('dsgbed', {
    kicker: 'בדיקה · חדר שינה',
    title: 'חדר שינה קטן: איזו מיטה נכנסת',
    lede: 'מידות החדר, גודל המיטה והארון. רואים בשרטוט בקנה מידה אם נשאר מעבר בצדי המיטה ומול הארון, ומה המיטה הגדולה ביותר שנכנסת.',
    presets: [
      { key: 'small', label: 'חדר הורים קטן', sub: '3 × 3.2, מיטה 160', set: { W: 300, Dp: 320, bed: '160', sides: 'both', ward: 'sliding', wardAt: 'foot', wardLen: 200 } },
      { key: 'kid', label: 'חדר ילדים', sub: '2.6 × 3, מיטה 90', set: { W: 260, Dp: 300, bed: '90', sides: 'one', ward: 'hinged', wardAt: 'side', wardLen: 120 } },
      { key: 'big', label: 'חדר הורים', sub: '3.6 × 4, מיטה 180', set: { W: 360, Dp: 400, bed: '180', sides: 'both', ward: 'hinged', wardAt: 'foot', wardLen: 240 } }
    ],
    defaults: function () { return { W: 310, Dp: 340, bed: '160', sides: 'both', ward: 'sliding', wardAt: 'foot', wardLen: 200 }; },
    fields: [
      { id: 'W', label: 'רוחב החדר (קיר הראש של המיטה)', type: 'number', unit: 'ס"מ' }, { id: 'Dp', label: 'אורך החדר', type: 'number', unit: 'ס"מ' },
      { id: 'bed', label: 'רוחב המיטה', type: 'segmented', options: [{ value: '90', label: '90' }, { value: '120', label: '120' }, { value: '140', label: '140' }, { value: '160', label: '160' }, { value: '180', label: '180' }] },
      { id: 'sides', label: 'נכנסים למיטה', type: 'segmented', options: [{ value: 'both', label: 'משני הצדדים' }, { value: 'one', label: 'מצד אחד' }] },
      { id: 'ward', label: 'ארון בגדים', type: 'segmented', options: [{ value: 'none', label: 'בלי' }, { value: 'hinged', label: 'דלתות' }, { value: 'sliding', label: 'הזזה' }] },
      { id: 'wardAt', label: 'איפה הארון', type: 'segmented', options: [{ value: 'foot', label: 'מול המיטה' }, { value: 'side', label: 'בצד המיטה' }], showIf: function (v) { return v.ward !== 'none'; } },
      { id: 'wardLen', label: 'אורך הארון', type: 'number', unit: 'ס"מ', showIf: function (v) { return v.ward !== 'none'; } }
    ],
    compute: function (v, data) {
      var D = data.design, r = bedFit(v, D);
      if (r.error) return pickErr(r.error, { W: 'רוחב בין 150 ל־2,000 ס"מ.', Dp: 'אורך בין 150 ל־2,000 ס"מ.', wardLen: 'הקלידו את אורך הארון.' });
      var b = r.bed, side = D.rules.bed_side_cm.v, wd = D.rules.wardrobe_depth_cm.v;
      var fig = plan(v.W, v.Dp, function (g, P) {
        var okA = r.need.okA, okL = r.need.okL, atSide = r.need.atSide, hasW = v.ward !== 'none';
        var free = function (ok) { return ok ? '#E3F1E5' : 'url(#nldsh)'; };
        var right = atSide ? v.W - wd : v.W;  // the free width to the wardrobe or the wall
        var bx = v.sides === 'one' ? 0 : atSide ? side : (v.W - b[0]) / 2;
        if (bx > 0) g.push('<rect x="' + P.x(0) + '" y="' + P.y(0) + '" width="' + P.s(bx) + '" height="' + P.s(Math.min(b[1], v.Dp)) + '" fill="' + free(okA) + '"/>');
        g.push('<rect x="' + P.x(bx + b[0]) + '" y="' + P.y(0) + '" width="' + P.s(Math.max(0, right - bx - b[0])) + '" height="' + P.s(Math.min(b[1], v.Dp)) + '" fill="' + free(okA) + '"/>');
        g.push('<text x="' + P.x(bx + b[0] + Math.max(0, right - bx - b[0]) / 2) + '" y="' + (+P.y(Math.min(b[1], v.Dp) / 2) + 4).toFixed(1) + '" text-anchor="middle" class="m' + (okA ? '' : ' bad') + '">' + Math.round(right - bx - b[0]) + '</text>');
        g.push(box(P, bx, 0, b[0], Math.min(b[1], v.Dp), C.bed, C.sofa, 'מיטה ' + b[0]));
        g.push(box(P, bx + 8, 6, Math.max(10, b[0] - 16), 30, '#fff', C.sofa, ''));
        if (hasW && atSide) { var wl = Math.min(v.wardLen, v.Dp); g.push(box(P, v.W - wd, 0, wd, wl, C.ward, r.need.wardOk && okA ? '#8E7CC3' : C.bad, 'ארון')); }
        if (hasW && !atSide) { var wl2 = Math.min(v.wardLen, v.W); g.push(box(P, (v.W - wl2) / 2, v.Dp - wd, wl2, wd, C.ward, r.need.wardOk && okL ? '#8E7CC3' : C.bad, 'ארון')); }
        var gapH = v.Dp - b[1] - (hasW && !atSide ? wd : 0);
        g.push('<text x="' + P.x(bx + b[0] / 2) + '" y="' + (+P.y(b[1] + Math.max(0, gapH) / 2) + 4).toFixed(1) + '" text-anchor="middle" class="m' + (okL ? '' : ' bad') + '">' + Math.round(gapH) + ' ס"מ</text>');
      },'שרטוט חדר השינה בקנה מידה: מיטה ' + b[0] + ' על ' + b[1] + ' בחדר ' + v.W + ' על ' + v.Dp + ' ס"מ');
      var verdict = r.status === 'ok' ? 'המיטה נכנסת עם מעברים' : 'צפוף מדי';
      var lines = [{ label: 'לרוחב צריך ' + Math.round(r.need.across) + ' ס"מ', value: r.need.okA ? 'יש' : 'חסר ' + Math.round(r.need.across - v.W) + ' ס"מ' },
        { label: 'לאורך צריך ' + Math.round(r.need.along) + ' ס"מ', value: r.need.okL ? 'יש' : 'חסר ' + Math.round(r.need.along - v.Dp) + ' ס"מ' },
        { label: 'המיטה הגדולה ביותר שנכנסת', value: r.best ? r.best[0] + ' × ' + r.best[1] : 'אף מיטה עם מעברים' },
        { label: b[0] >= 140 ? 'מיטה זוגית עם מזרן' : 'מיטת יחיד או נוער', value: R(r.bedPrice) + rough(r.bedPrice) }];
      if (r.wardPrice) lines.push({ label: v.ward === 'sliding' ? 'ארון הזזה, ' + r.wardPrice.units + ' × 2 מטר' : 'ארון בהתאמה, ' + v.wardLen / 100 + ' מטר', value: R(r.wardPrice.r) + rough(r.wardPrice.b) });
      if (!r.need.wardOk) lines.push({ label: 'הארון ארוך מהקיר', value: 'קצרו אותו' });
      return {
        answer: { label: 'מיטה ' + b[0] + ' × ' + b[1] + ' בחדר ' + v.W + ' × ' + v.Dp + ' ס"מ', value: verdict, tone: r.status === 'ok' ? '' : 'survey', sub: esc('מעבר ' + side + ' ס"מ בצד המיטה ו־' + D.rules.bed_foot_cm.v + ' למרגלותיה · מחירים מ' + READ) },
        figure: fig, lines: lines,
        note: esc('כללי אצבע מקובלים: 60 ס"מ בצד שנכנסים ממנו (50 לכל הפחות), 60 עד 90 למרגלות המיטה, ארון בעומק 60 עם 90 ס"מ מולו לדלתות או 60 להזזה.'),
        formula: 'רוחב נדרש = רוחב המיטה + מעבר בכל צד שנכנסים ממנו. אורך נדרש = אורך המיטה + מעבר למרגלות. ארון מול המיטה: אורך המיטה + המקום מול הארון + עומק הארון. ארון בצד: רוחב המיטה + המקום מול הארון + עומק הארון.',
        sources: srcLine([r.bedPrice, r.wardPrice && r.wardPrice.b]),
        text: 'מיטה ' + b[0] + ' בחדר ' + v.W + ' × ' + v.Dp + ' ס"מ: ' + verdict + '. הגדולה שנכנסת: ' + (r.best ? r.best[0] : 'אין') + '.'
      };
    }
  });

  /* ---------------- dsglight ---------------- */
  var FIX = { spot: 'ספוטים שקועים', ceiling: 'גוף תאורה תקרתי', pendant: 'מנורות תלויות', profile: 'פס לד (מטר)' };
  NI.register('dsglight', {
    kicker: 'מחשבון · תכנון תאורה לבית',
    title: 'תכנון תאורה לבית: כמה אור צריך בכל חדר',
    lede: 'בוחרים חדר, שטח וסוג גוף תאורה. מקבלים כמה לומן צריך, כמה גופים, איזה גוון אור מתאים, וכמה עולות נקודות התאורה.',
    presets: [
      { key: 'living', label: 'סלון 25 מ"ר', sub: 'ספוטים', set: { room: 'living', area: 25, fixture: 'spot' } },
      { key: 'kitchen', label: 'מטבח 12 מ"ר', sub: 'ספוטים', set: { room: 'kitchen', area: 12, fixture: 'spot' } },
      { key: 'bedroom', label: 'חדר שינה 12 מ"ר', sub: 'גוף תקרתי', set: { room: 'bedroom', area: 12, fixture: 'ceiling' } },
      { key: 'bath', label: 'חדר רחצה 5 מ"ר', sub: 'ספוטים', set: { room: 'bath', area: 5, fixture: 'spot' } }
    ],
    defaults: function () { return { room: 'living', area: 25, fixture: 'spot', plan: 'no' }; },
    fields: [
      { id: 'room', label: 'החדר', type: 'select', options: Object.keys(ROOMS).map(function (k) { return { value: k, label: ROOMS[k] }; }) },
      { id: 'area', label: 'שטח החדר', type: 'number', unit: 'מ"ר' },
      { id: 'fixture', label: 'סוג התאורה', type: 'segmented', options: Object.keys(FIX).map(function (k) { return { value: k, label: FIX[k] }; }) },
      { id: 'plan', label: 'עם תכנית תאורה של מעצב', type: 'segmented', options: YN }
    ],
    compute: function (v, data) {
      var D = data.design, r = light(v, D);
      if (r.error) return pickErr(r.error, { area: 'הקלידו שטח בין 1 ל־200 מ"ר.' });
      var many = v.fixture === 'profile' ? num(r.n) + ' מטר פס לד' : num(r.n) + ' ' + (v.fixture === 'spot' ? 'ספוטים' : v.fixture === 'pendant' ? 'מנורות תלויות' : 'גופי תאורה');
      var lines = [{ label: 'עוצמת אור כללית (' + ROOMS[v.room] + ')', value: r.lux + ' לוקס' }, { label: 'לומן לכל החדר', value: num(Math.round(r.lm)) + ' לומן' },
        { label: 'אור מגוף אחד, בערך', value: num(r.per) + ' לומן' + (v.fixture === 'profile' ? ' למטר' : '') }, { label: 'גוון האור', value: r.kelvin + ' קלווין' },
        { label: 'נקודות תאורה: ' + r.points, value: R(r.cost) }];
      if (r.plan) lines.push({ label: 'תכנית תאורה לכל הדירה', value: R(r.plan, true) + rough(r.plan) });
      return {
        answer: { label: ROOMS[v.room] + ' של ' + num(v.area) + ' מ"ר', value: many, sub: esc(num(Math.round(r.lm)) + ' לומן · ' + r.kelvin + ' קלווין · נקודות ' + R(r.cost)) },
        lines: lines,
        note: esc('זו התאורה הכללית. מעליה מוסיפים תאורת משימה (מעל משטח העבודה, ליד המיטה, מעל השולחן) ותאורה דקורטיבית. ' + (v.fixture === 'profile' ? 'לפס לד סופרים נקודה אחת לכל פס. ' : 'כל גוף נספר כנקודת תאורה; חשמלאי יכול לחבר כמה ספוטים לנקודה אחת, וזה זול יותר. ') + 'נקודה שמתכננים לפני הצביעה זולה יותר. ' + (r.pb ? 'מחיר: ' + VAT[r.pb.vat] + '.' : '')),
        formula: 'לומן = לוקס × מ"ר × 1.25 (תוספת לאור שנבלע בקירות ובאהילים). גופים = לומן ÷ האור של גוף אחד, מעוגל למעלה. עוצמות האור הן כלל אצבע בתוך הטווחים המקובלים לבית (סלון 100 עד 300 לוקס, מטבח ופינת עבודה 300 עד 500).',
        sources: srcLine([r.pb].concat(r.plan ? [r.plan] : [])),
        text: ROOMS[v.room] + ' ' + num(v.area) + ' מ"ר: ' + many + ', ' + num(Math.round(r.lm)) + ' לומן, ' + r.kelvin + ' קלווין, נקודות ' + R(r.cost) + '.'
      };
    }
  });

  /* ---------------- dsgpoints ---------------- */
  function ptRows(n) {
    var base = [{ room: 'סלון', spec: 4, want: 7 }, { room: 'מטבח', spec: 5, want: 7 }, { room: 'חדר שינה הורים', spec: 3, want: 5 }];
    for (var i = 0; i < n - 2; i++) base.push({ room: 'חדר שינה ' + (i + 2), spec: 3, want: 4 });
    base.push({ room: 'מרפסת', spec: 0, want: 1 });
    return base;
  }
  NI.register('dsgpoints', {
    kicker: 'מחשבון · נקודות חשמל',
    title: 'נקודות חשמל בדירה חדשה: מה במפרט ומה להוסיף',
    lede: 'מעתיקים מהמפרט של הדירה כמה שקעים יש בכל חדר, ומקלידים כמה אתם רוצים. מקבלים כמה נקודות להוסיף, כמה זה עולה, ולמה לסגור את זה לפני הטיח.',
    presets: [
      { key: 'r3', label: 'דוגמה: 3 חדרים', set: { rows: ptRows(2) } },
      { key: 'r4', label: 'דוגמה: 4 חדרים', set: { rows: ptRows(3) } },
      { key: 'r5', label: 'דוגמה: 5 חדרים', set: { rows: ptRows(4) } }
    ],
    defaults: function () { return { rows: ptRows(3) }; },
    exampleNote: 'המספרים בפתיחה הם דוגמה ולא מפרט של פרויקט. העתיקו את המספרים מהמפרט שלכם.',
    fields: [{ id: 'rows', label: 'חדר · במפרט · רוצים', type: 'rows', addLabel: 'הוספת חדר', cols: [{ id: 'room', label: 'חדר', type: 'text', ph: 'חדר' }, { id: 'spec', label: 'במפרט' }, { id: 'want', label: 'רוצים' }], blank: function () { return { room: '', spec: 0, want: 0 }; } }],
    compute: function (v, data) {
      var D = data.design, r = points(v, D);
      if (r.error) return pickErr(r.error, { rows: 'הוסיפו חדר אחד לפחות.' });
      var notes = ['מה בדרך כלל חסר: שקע לכל צד של המיטה, ארבעה שקעים בקיר הטלוויזיה, שקע לכל מכשיר קבוע במטבח ועוד שניים מעל המשטח, שקע במרפסת, ושקע ליד שולחן העבודה. זה כלל אצבע, לא תקן.',
        'נקודה שמוסיפים לפני הטיח, דרך השינויים אצל היזם, זולה בהרבה מנקודה שחוצבים אחרי המסירה. את המחיר אצל היזם קובע מחירון השינויים שלו.'];
      if (r.less) notes.push('ביקשתם פחות נקודות מהמפרט בחלק מהחדרים (' + r.less + '). אפשר לבקש זיכוי מהיזם.');
      return {
        answer: { label: 'נקודות להוסיף מעבר למפרט', value: num(r.add) + ' נקודות', sub: esc('עלות ההוספה: ' + R(r.cost) + ' · ' + R(r.eb, true) + ' לנקודה · ' + READ) },
        breakdown: [{ label: 'במפרט', value: r.specTotal, kind: 'sea', shown: String(r.specTotal) }, { label: 'תוספת', value: r.add, kind: 'housing', shown: String(r.add) }],
        lines: r.per.map(function (x) { return { label: (x.room || 'חדר') + ': ' + x.spec + ' במפרט, ' + x.want + ' רוצים', value: x.d > 0 ? 'עוד ' + x.d : x.d < 0 ? Math.abs(x.d) + ' פחות' : 'מספיק' }; }),
        note: notes.map(esc).join('<br>'),
        formula: 'תוספת = סכום ההפרשים החיוביים בין מה שרוצים למה שבמפרט. עלות = תוספת × המחיר לנקודה שפורסם (' + R(r.eb, true) + ', עם חציבה יקר יותר).',
        sources: srcLine([r.eb]),
        text: 'נקודות חשמל: ' + r.specTotal + ' במפרט, ' + r.wantTotal + ' רוצים, להוסיף ' + r.add + ': ' + R(r.cost) + ' (' + READ + ').'
      };
    }
  });

  /* ---------------- dsgwho ---------------- */
  NI.register('dsgwho', {
    kicker: 'בחירה · איש המקצוע',
    title: 'מעצב פנים, הום סטיילינג או אדריכל: מי מתאים לכם',
    lede: 'ארבע שאלות קצרות, ותשובה: איזה איש מקצוע מתאים למה שאתם עושים, ומה עולה כל אפשרות, זו לצד זו.',
    presets: [
      { key: 'new', label: 'דירה חדשה מקבלן', sub: 'שינויים ומטבח', set: { permit: 'no', scope: 'finish', help: 'plan', rooms: 4 } },
      { key: 'furnish', label: 'רק לרהט', sub: 'בלי עבודות', set: { permit: 'no', scope: 'furnish', help: 'manage', rooms: 4 } },
      { key: 'reno', label: 'שיפוץ גדול', sub: 'הזזת קירות ותוספת', set: { permit: 'yes', scope: 'renovate', help: 'manage', rooms: 5 } }
    ],
    defaults: function () { return { permit: 'no', scope: 'finish', help: 'plan', rooms: 4 }; },
    fields: [
      { id: 'permit', label: 'יש תוספת בנייה, קיר נושא או משהו שדורש היתר?', type: 'segmented', options: YN },
      { id: 'scope', label: 'מה עושים בדירה', type: 'segmented', options: [{ value: 'furnish', label: 'רק ריהוט ועיצוב' }, { value: 'finish', label: 'גימורים, מטבח ושינויים' }, { value: 'renovate', label: 'שיפוץ מלא' }] },
      { id: 'help', label: 'כמה עזרה אתם רוצים', type: 'segmented', options: [{ value: 'ideas', label: 'רעיונות וכיוון' }, { value: 'plan', label: 'תכניות לבעלי המקצוע' }, { value: 'manage', label: 'ליווי עד הכניסה' }] },
      segNum('rooms', 'מספר חדרים', ROOMSEG)
    ],
    compute: function (v, data) {
      var D = data.design, r = who(v, D), o = r.opts[r.rec];
      var order = ['consult', 'styling', 'plan', 'full', 'architect'];
      var bs = [o.b, r.opts.consult.b, r.opts.styling.b, r.rooms.b].filter(Boolean);
      return {
        answer: { label: 'מה שמתאים לכם', value: o.he, sub: esc(r.why + (o.r ? ' בערך ' + R(o.r) + '.' : '')) },
        lines: order.map(function (k) { var x = r.opts[k]; return { label: (k === r.rec ? '● ' : '') + x.he, value: x.r ? R(x.r) : 'אין טווח שפורסם' }; }),
        note: esc('הום סטיילינג: לפי מחיר שפורסם להלבשת דירה שלמה. מעצב פנים: לפי דירת ' + r.rooms.k + ' חדרים; תכנון בלבד הוא החצי התחתון של הטווח הנפוץ וליווי מלא העליון. לאדריכל לא מצאנו טווח מחירים שפורסם לדירה, ולכן אין כאן מספר. שינוי שדורש היתר עובר דרך אדריכל או מהנדס.'),
        formula: 'ההמלצה: היתר או קיר נושא → אדריכל; רק ריהוט → ייעוץ או הום סטיילינג; אחרת לפי כמות העזרה: רעיונות → ייעוץ, תכניות → תכנון בלבד, ליווי → ליווי מלא.',
        sources: srcLine(bs),
        text: 'מי מתאים: ' + o.he + (o.r ? ', ' + R(o.r) : '') + '. ' + r.why
      };
    }
  });

  /* ---------------- dsgtime ---------------- */
  function monthHe(k) { var p = String(k).split('-'); var M = ['ינואר', 'פברואר', 'מרץ', 'אפריל', 'מאי', 'יוני', 'יולי', 'אוגוסט', 'ספטמבר', 'אוקטובר', 'נובמבר', 'דצמבר']; return p.length > 1 ? M[+p[1] - 1] + ' ' + p[0] : k; }
  function thisMonth() { var d = new Date(); return d.getFullYear() + '-' + (d.getMonth() < 9 ? '0' : '') + (d.getMonth() + 1); }
  function plusMonths(n) { return NLDS.ymKey(NLDS.ym(thisMonth()) + n); }
  NI.register('dsgtime', {
    kicker: 'לוח זמנים · דירה חדשה',
    title: 'לוח זמנים לדירה חדשה: מהחתימה ועד המעבר',
    lede: 'מקלידים את חודש המסירה שבחוזה, ומקבלים את סדר ההחלטות, מהמעצב והשינויים ועד הרהיטים והמעבר, עם החודש האחרון שהגיוני לסגור כל אחת.',
    presets: [
      { key: 'y3', label: 'מסירה בעוד 3 שנים', set: { handover: plusMonths(36) } },
      { key: 'y2', label: 'מסירה בעוד שנתיים', set: { handover: plusMonths(24) } },
      { key: 'y1', label: 'מסירה בעוד שנה', set: { handover: plusMonths(12) } },
      { key: 'm4', label: 'מסירה בעוד 4 חודשים', set: { handover: plusMonths(4) } }
    ],
    defaults: function () { return { handover: plusMonths(24), signed: '' }; },
    fields: [
      { id: 'handover', label: 'חודש המסירה בחוזה', type: 'month' },
      { id: 'signed', label: 'חודש החתימה (לא חובה)', type: 'month', help: 'אם אין עדיין מועד בחוזה, נראה כמה זמן בנייה נמשכת בממוצע.' }
    ],
    compute: function (v, data) {
      var D = data.design, r = timeline({ handover: v.handover, signed: v.signed, today: thisMonth() }, D);
      if (r.error) return pickErr(r.error, { handover: 'בחרו את חודש המסירה.' });
      var items = r.steps.map(function (s) { return '<li class="' + s.state + '"><b>' + esc(NI.fmt.month(s.key)) + '</b><span>' + esc(s.he) + (s.state === 'late' ? ' · החודש הזה עבר' : s.state === 'now' ? ' · עכשיו' : '') + '<small>' + esc(s.why) + '</small></span></li>'; }).join('');
      var cbs = D.rules.build_months_cbs.v;
      var notes = ['הסדר והחודשים הם מה שמקובל, לא כלל. המועדים בחוזה עם היזם, ובמיוחד המועד האחרון לשינויים, קובעים.',
        'משך בנייה ממוצע של בניין שהסתיים ב־2025: ' + cbs[0] + ' חודשים, ו־' + cbs[1] + ' בממוצע לפי מספר הדירות (הלשכה המרכזית לסטטיסטיקה, מרץ 2026).'];
      if (r.est) notes.push('מחודש החתימה, לפי הממוצע: מסירה בין ' + monthHe(r.est.a) + ' ל־' + monthHe(r.est.b) + '. התאריך בחוזה גובר.');
      if (r.late) notes.push(r.late + ' מהשלבים כבר מאחוריכם בלוח הזה. בדקו מול היזם מה עוד אפשר לשנות.');
      var left = r.left;
      return {
        answer: { label: r.next ? 'ההחלטה הבאה' : 'כל השלבים בלוח עברו', value: r.next ? r.next.he : 'לפני המעבר', tone: r.late ? 'survey' : '', sub: esc(r.next ? 'עד ' + monthHe(r.next.key) + ' · ' + (left > 0 ? left + ' חודשים עד המסירה' : left === 0 ? 'המסירה החודש' : 'המסירה עברה') : '') },
        figure: '<ol class="nlds-steps" aria-label="סדר ההחלטות">' + items + '</ol>',
        note: notes.map(esc).join('<br>'),
        formula: 'לכל שלב קבענו כמה חודשים לפני המסירה או אחריה הוא נסגר בדרך כלל, ומחשבים מחודש המסירה שהקלדתם. השלבים שחודשם עבר מסומנים.',
        sources: [{ label: 'הלשכה המרכזית לסטטיסטיקה, הודעה 089/2026, 19.3.2026 (משך בנייה)' }, { label: 'סדר השלבים: מה שמקובל בשוק, לא מקור רשמי' }],
        text: 'דירה במסירה ב' + monthHe(r.handover) + ': ' + r.steps.map(function (s) { return monthHe(s.key) + ' ' + s.he; }).join('; ') + '.'
      };
    }
  });

  /* ---------------- dsgstyle ---------------- */
  NI.register('dsgstyle', {
    kicker: 'שאלון · סגנונות עיצוב פנים',
    title: 'סגנונות עיצוב פנים: איזה סגנון שלכם',
    lede: 'חמש שאלות על מה שאתם אוהבים. מקבלים סגנון, חמישה צבעים לקירות ולבדים, החומרים שלו, ורשימת רהיטים לסלון עם טווח מחיר.',
    presets: [
      { key: 'calm', label: 'שקט ומעט חפצים', set: { q1: 'a', q2: 'b', q3: 'a', q4: 'b', q5: 'a' } },
      { key: 'warm', label: 'חם ומלא חיים', set: { q1: 'c', q2: 'd', q3: 'c', q4: 'c', q5: 'd' } },
      { key: 'sea', label: 'ליד הים', set: { q1: 'd', q2: 'd', q3: 'b', q4: 'd', q5: 'b' } }
    ],
    defaults: function () { return { q1: 'b', q2: 'b', q3: 'b', q4: 'b', q5: 'b', level: 'mid' }; },
    fields: QUIZ.map(function (q) { return { id: q.id, label: q.he, type: 'segmented', options: q.o.map(function (o) { return { value: o[0], label: o[1] }; }) }; }).concat([{ id: 'level', label: 'רמת המחיר של הרהיטים', type: 'segmented', options: LEVELS }]),
    compute: function (v, data) {
      var D = data.design, r = style(v, D);
      if (r.error) return pickErr(r.error, {});
      var S = r.S;
      var sw = '<div class="nlds-sw" role="img" aria-label="הצבעים של הסגנון: ' + esc(S.pal.map(function (p) { return p[1]; }).join(', ')) + '">' + S.pal.map(function (p) {
        var c = parseInt(p[0].slice(1), 16), l = 0.299 * (c >> 16) + 0.587 * (c >> 8 & 255) + 0.114 * (c & 255);
        return '<span class="' + (l < 120 ? 'dk' : '') + '" style="background:' + p[0] + '">' + esc(p[1]) + '</span>'; }).join('') + '</div>';
      return {
        answer: { label: 'הסגנון שלכם', value: S.he, sub: esc(S.look + (r.second ? ' · קרוב גם ל' + STYLES[r.second].he : '')) },
        figure: sw,
        lines: [{ label: 'חומרים', value: S.mat }].concat(r.list.map(function (l) { return { label: l.b.name, value: R(l.r) }; })).concat([{ label: 'כל הסלון, ' + LEVELHE[r.level], value: R(r.total) }]),
        note: esc('המחיר תלוי ברמה, לא בסגנון: ספה סקנדינבית יכולה להיות זולה או יקרה. הצבעים הם הצעה לנקודת פתיחה; לפני שצובעים, בודקים דוגמה על הקיר באור של הבוקר ושל הערב.'),
        table: { title: 'הניקוד של כל סגנון', head: ['סגנון', 'נקודות'], num: [1], rows: Object.keys(r.score).sort(function (a, b) { return r.score[b] - r.score[a]; }).map(function (k) { return [STYLES[k].he, String(r.score[k])]; }) },
        formula: 'כל תשובה נותנת נקודות לסגנון אחד או שניים; הסגנון עם הכי הרבה נקודות מנצח. המחירים: רהיטי סלון לפי הרמה שבחרתם, מתוך הטווחים שפורסמו.',
        sources: srcLine(r.list.map(function (l) { return l.b; })),
        text: 'הסגנון שלי: ' + S.he + '. צבעים: ' + S.pal.map(function (p) { return p[1]; }).join(', ') + '. סלון ' + LEVELHE[r.level] + ': ' + R(r.total) + '.'
      };
    }
  });

  /* ---------------- dsgcurtain ---------------- */
  NI.register('dsgcurtain', {
    kicker: 'מחשבון · וילונות ותריסים',
    title: 'כמה עולים וילונות ותריסים לכל החלונות',
    lede: 'מקלידים את רוחב וגובה החלונות, ובוחרים וילון, תריס חשמלי או שניהם. מקבלים את השטח ואת הטווח שפורסם.',
    presets: [
      { key: 'r3', label: 'דירת 3 חדרים', sub: 'ויטרינה ו־3 חלונות', set: { rows: [{ w: 240, h: 220 }, { w: 120, h: 120 }, { w: 120, h: 120 }, { w: 100, h: 120 }], curtain: 'yes', shutter: 'no' } },
      { key: 'r4', label: 'דירת 4 חדרים', sub: 'ויטרינה ו־4 חלונות', set: { rows: [{ w: 300, h: 220 }, { w: 140, h: 130 }, { w: 120, h: 120 }, { w: 120, h: 120 }, { w: 100, h: 120 }], curtain: 'yes', shutter: 'no' } },
      { key: 'vit', label: 'ויטרינה בסלון', sub: 'וילון ותריס חשמלי', set: { rows: [{ w: 300, h: 230 }], curtain: 'yes', shutter: 'yes' } }
    ],
    defaults: function () { return { rows: [{ w: 300, h: 220 }, { w: 140, h: 130 }, { w: 120, h: 120 }, { w: 120, h: 120 }], curtain: 'yes', shutter: 'no' }; },
    fields: [
      { id: 'rows', label: 'רוחב וגובה של כל חלון (ס"מ)', type: 'rows', addLabel: 'הוספת חלון', cols: [{ id: 'w', label: 'רוחב', unit: 'ס"מ' }, { id: 'h', label: 'גובה', unit: 'ס"מ' }], blank: function () { return { w: 120, h: 120 }; } },
      { id: 'curtain', label: 'וילון בהזמנה', type: 'segmented', options: YN }, { id: 'shutter', label: 'תריס גלילה חשמלי', type: 'segmented', options: YN }
    ],
    compute: function (v, data) {
      var D = data.design, r = curtains(v, D);
      if (r.error) return pickErr(r.error, { rows: 'הקלידו רוחב וגובה של חלון אחד לפחות.' });
      var parts = []; if (r.cur) parts.push({ he: 'וילונות', r: r.cur, b: r.cb, kind: 'sea' }); if (r.sh) parts.push({ he: 'תריסים חשמליים', r: r.sh, b: r.sb, kind: 'housing' });
      if (!parts.length) return { error: { field: 'curtain', msg: 'בחרו וילון, תריס או שניהם.' } };
      return {
        answer: { label: r.n + ' חלונות, ' + F.num(r.area, 1) + ' מ"ר', value: R(r.total), sub: esc(parts.map(function (p) { return p.he + ' ' + R(p.r); }).join(' · ') + ' · ' + READ) },
        breakdown: parts.map(function (p) { return { label: p.he, value: mid(p.r), kind: p.kind, shown: R(p.r) }; }),
        lines: parts.map(function (p) { return { label: p.he + ': ' + R(p.b, true) + ' למ"ר', value: R(p.r) }; }),
        note: esc('וילון: המקורות לא תמיד כוללים את הבד, התפירה וההתקנה; שאלו מה כלול. תריס: יש מחיר מינימום לחלון קטן, כך שבחלונות קטנים המחיר יוצא גבוה מהחישוב. שטח הווילון מחושב לפי שטח החלון.'),
        formula: 'שטח = רוחב × גובה של כל חלון, במטרים. עלות = שטח × המחיר למ"ר שפורסם.',
        sources: srcLine(parts.map(function (p) { return p.b; })),
        text: r.n + ' חלונות (' + F.num(r.area, 1) + ' מ"ר): ' + parts.map(function (p) { return p.he + ' ' + R(p.r); }).join(', ') + ' (' + READ + ').'
      };
    }
  });
})();
