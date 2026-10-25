/* NadLan Instruments · gwall v1 (HAD-601, Q6 stage 2, 26.10.2026): the gypsum wall calculator of /glossary/לוח-גבס-אדום/.
   A wall (place, fire requirement from the consultant, length, height, sides, layers, board size and thickness, waste, price per
   board) becomes: the board that fits the place, how many boards (by area with the reader's waste, and by layout without reusing
   offcuts), the board weight from the supplier table, the cost, the supplier prices side by side, the tested partition that
   matches the build when a supplier published one, and the documents to ask for. The minutes always belong to the tested wall,
   never to the board. The drawing (SVG in RTL: text-anchor start = the right end of a label): the face of the wall with every board and joint, and the cut through the layers.
   Data: data/gwall.json (manufacturer and supplier sites, 25.10.2026). Pure logic in NLGW for checks. */
(function () {
  'use strict';
  var EPS = 1e-9;
  var PLACE = {
    dry: 'מחיצה או תקרה בחדר יבש', wet: 'חדר רטוב (אמבטיה, מטבח)', esc: 'חדר מדרגות או מסדרון מילוט',
    shaft: 'פיר, צנרת או תעלה', steel: 'עמוד או קיר פלדה', out: 'קיר חוץ'
  };
  var KIND = {
    re: { name: 'לוח לבן רגיל (RE)', short: 'לבן' },
    mr: { name: 'לוח ירוק עמיד מים ולחות (MRWR)', short: 'ירוק' },
    fr: { name: 'לוח גבס ורוד מעכב בעירה (FR)', short: 'ורוד' },
    fm: { name: 'לוח משולב ירוק ורוד (FM)', short: 'משולב' },
    fd: { name: 'לוח מיוחד לאש, פייר דיפנדר 24 מ"מ', short: 'מיוחד לאש' }
  };
  /** The board for a place and a fire requirement (minutes, 0 = none); null = no gypsum fire board fits (outside). */
  function boardFor(place, fire) {
    if (place === 'out') return null;
    if (place === 'shaft' || place === 'steel') return 'fd';
    if (place === 'wet') return fire > 0 ? 'fm' : 'mr';
    if (place === 'esc') return 'fr';
    return fire > 0 ? 'fr' : 're';
  }
  /** Boards two ways, and the order is the larger: by area with the reader's waste, and by a cut plan (columns of 1.20 m; the top
      pieces, the narrow last column and its corner piece are cut from whole boards, several pieces per board, across all layers). */
  function count(L, H, sides, layers, lb, width, waste) {
    var N = sides * layers, area = L * H * N, ba = width * lb;
    var byArea = Math.ceil(area * (1 + waste / 100) / ba - EPS);
    var nf = Math.floor(L / width + EPS), wp = L - nf * width, fh = Math.floor(H / lb + EPS), rh = H - fh * lb;
    if (wp < 0.01) wp = 0; if (rh < 0.01) rh = 0;
    var byCut = N * nf * fh;
    if (rh) byCut += Math.ceil(N * nf / Math.floor(lb / rh + EPS) - EPS);
    if (wp) byCut += Math.ceil(N * fh / Math.floor(width / wp + EPS) - EPS);
    if (wp && rh) byCut += Math.ceil(N / (Math.floor(width / wp + EPS) * Math.floor(lb / rh + EPS)) - EPS);
    return { area: area, boardArea: ba, byArea: byArea, byCut: byCut, order: Math.max(byArea, byCut), cols: nf + (wp ? 1 : 0), perCol: fh + (rh ? 1 : 0) };
  }
  function boardKg(d, kind, thick, size, lb) {
    if (kind === 'fd') return { kg: d.fd.kg, calc: false };
    if (kind !== 'fr') return null;
    var t = d.kgBoard[thick] || {};
    if (t[size]) return { kg: t[size], calc: false };
    return { kg: d.kgm2[thick] * d.width * lb, calc: true };
  }
  function priceFor(d, kind, thick, size) {
    var p = d.price[kind] && d.price[kind][thick] && d.price[kind][thick][size];
    return p ? p : null;
  }
  window.NLGW = { boardFor: boardFor, count: count, boardKg: boardKg, priceFor: priceFor };
  if (!window.NadLanInstruments) return;
  var NI = window.NadLanInstruments, F = NI.fmt, esc = NI.esc;
  function m(n) { var d = Math.abs(n * 10 - Math.round(n * 10)) < EPS ? (n % 1 ? 1 : 0) : 2; return F.num(n, d); }  // 2.6 -> 2.6, 2.65 -> 2.65, 4 -> 4

  /** The drawing: the face of the wall (every board and joint, the cut pieces) and, under it, the cut through the layers. */
  function svg(o) {
    var W = 420, X0 = 60, X1 = 396, maxH = 210;
    var seg = o.L > 12 ? 4.8 : o.L;  // a long wall: a segment of 4 boards, labelled
    var s = Math.min((X1 - X0) / seg, maxH / o.H), w = seg * s, h = o.H * s, x0 = X1 - w, y0 = 54;
    var fill = { re: '#FFFFFF', mr: '#E4F1E6', fr: 'url(#gwFR)', fm: 'url(#gwFM)', fd: 'url(#gwFD)' }[o.kind];
    var g = [];
    g.push('<defs><pattern id="gwFR" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="8" height="8" fill="#FBEAEF"/><line x1="0" y1="0" x2="0" y2="8" stroke="#C42550" stroke-width="1.2"/></pattern>'
      + '<pattern id="gwFM" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="8" height="8" fill="#E4F1E6"/><line x1="0" y1="0" x2="0" y2="8" stroke="#C42550" stroke-width="1.2"/></pattern>'
      + '<pattern id="gwFD" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="5" height="5" fill="#F6D9E1"/><line x1="0" y1="0" x2="0" y2="5" stroke="#C42550" stroke-width="1.6"/></pattern>'
      + '<pattern id="gwWool" width="14" height="10" patternUnits="userSpaceOnUse"><path d="M0 5 Q3.5 0 7 5 T14 5" fill="none" stroke="#8A97A2" stroke-width="1"/></pattern></defs>');
    g.push('<text x="' + X1 + '" y="18" class="t" text-anchor="start">' + esc(o.title) + '</text>');
    if (o.fire > 0) g.push('<rect x="8" y="4" width="112" height="24" fill="#fff" stroke="#C42550" stroke-width="1.5"/><text x="64" y="21" class="m r" text-anchor="middle">' + esc('דרישה ' + o.fire + ' דק\'') + '</text>');
    // boards: columns from the right edge (the drawing reads like the wall, right to left), joints staggered when a column needs two boards
    var cw = o.width * s, ncol = Math.ceil(seg / o.width - EPS);
    for (var i = 0; i < ncol; i++) {
      var xr = X1 - i * cw, xl = Math.max(x0, xr - cw), bw = xr - xl;
      if (o.H <= o.lb + EPS) { g.push('<rect x="' + xl + '" y="' + y0 + '" width="' + bw + '" height="' + h + '" fill="' + fill + '" stroke="#12202A" stroke-width="1"/>'); continue; }
      var full = o.lb * s, rest = h - full * (o.perCol - 1), y = y0 + h;
      var parts = []; for (var k = 0; k < o.perCol - 1; k++) parts.push(full); if (i % 2) parts.unshift(rest); else parts.push(rest);  // stagger
      parts.forEach(function (ph) { y -= ph; g.push('<rect x="' + xl + '" y="' + y + '" width="' + bw + '" height="' + ph + '" fill="' + fill + '" stroke="#12202A" stroke-width="1"/>'); });
    }
    if (o.L > 12) g.push('<text x="' + X1 + '" y="' + (y0 - 8) + '" class="s" text-anchor="start">' + esc('קטע של 4.80 מ\' מתוך ' + m(o.L) + ' מ\'') + '</text>');
    // dimensions
    var yd = y0 + h + 16;
    g.push('<line x1="' + x0 + '" y1="' + yd + '" x2="' + X1 + '" y2="' + yd + '" stroke="#12202A" stroke-width="1"/><line x1="' + x0 + '" y1="' + (yd - 5) + '" x2="' + x0 + '" y2="' + (yd + 5) + '" stroke="#12202A"/><line x1="' + X1 + '" y1="' + (yd - 5) + '" x2="' + X1 + '" y2="' + (yd + 5) + '" stroke="#12202A"/>');
    g.push('<text x="' + ((x0 + X1) / 2) + '" y="' + (yd + 17) + '" class="m" text-anchor="middle">' + esc(m(seg) + ' מ\'') + '</text>');
    g.push('<text x="' + (x0 - 6) + '" y="' + (y0 + h / 2 + 5) + '" class="m" text-anchor="start">' + esc(m(o.H) + ' מ\'') + '</text>');
    // the cut through the layers (plan): side A, the frame cavity, side B
    var yc = yd + 40, t = { '12.5': 7, '16': 9, '24': 12 }[o.thick] || 7, cav = 30, xs0 = 220, xs1 = X1, rows = [];
    function band(n, label) { for (var j = 0; j < n; j++) { rows.push({ h: t, fill: fill, label: j === 0 ? label : '' }); } }
    band(o.layers, 'צד א: ' + o.layers + ' × ' + o.thick + ' מ"מ');
    rows.push({ h: cav, fill: o.wool ? 'url(#gwWool)' : '#F6F8F9', label: o.frame || 'שלד ובידוד לפי היועץ', cav: true });
    if (o.sides > 1) band(o.layers, 'צד ב: ' + o.layers + ' × ' + o.thick + ' מ"מ');
    var yy = yc;
    rows.forEach(function (r) {
      g.push('<rect x="' + xs0 + '" y="' + yy + '" width="' + (xs1 - xs0) + '" height="' + r.h + '" fill="' + r.fill + '" stroke="#12202A" stroke-width="' + (r.cav ? 0.6 : 1) + '"/>');
      if (r.cav) { [xs0 + 10, (xs0 + xs1) / 2 - 6, xs1 - 22].forEach(function (sx) { g.push('<path d="M' + (sx + 12) + ' ' + yy + ' H' + sx + ' V' + (yy + r.h) + ' H' + (sx + 12) + '" fill="none" stroke="#12202A" stroke-width="2"/>'); }); }
      if (r.label) g.push('<text x="' + (xs0 - 8) + '" y="' + (yy + (r.cav ? r.h / 2 + 5 : Math.max(10, r.h) + 3)) + '" class="s" text-anchor="start">' + esc(r.label) + '</text>');
      yy += r.h;
    });
    var H2 = yy + 34;
    g.push('<text x="' + X1 + '" y="' + (yy + 22) + '" class="s" text-anchor="start">' + esc(o.caption) + '</text>');
    return '<svg class="nli__wall" direction="rtl" viewBox="0 0 ' + W + ' ' + H2 + '" role="img" aria-label="' + esc(o.aria) + '">' + g.join('') + '</svg>';
  }

  NI.register('gwall', {
    kicker: 'מחשבון · קיר גבס',
    title: 'כמה לוחות גבס ורודים צריך לקיר, כמה הם שוקלים וכמה הם עולים',
    lede: 'בוחרים איפה הקיר, מה דרישת האש שקבע היועץ, את המידות ואת מספר השכבות, ומקבלים את סוג הלוח, את מספר הלוחות, את המשקל ואת העלות לפי מחירי הספקים, את המחיצה שנבדקה כשיש כזאת, ואת המסמכים לבקש מהקבלן.',
    presets: [
      { key: 'stair120', label: 'חדר מדרגות, 120 דקות', sub: '4 × 2.6 מ\', 2 שכבות מכל צד', set: { place: 'esc', fire: '120', L: 4, H: 2.6, sides: '2', layers: '2', size: '2.60', thick: '12.5', waste: 10, price: 80.8 } },
      { key: 'home', label: 'מחיצה בבית', sub: 'בלי דרישת אש, 3.5 × 2.6 מ\'', set: { place: 'dry', fire: '0', L: 3.5, H: 2.6, sides: '2', layers: '1', size: '2.60', thick: '12.5', waste: 10, price: 61.4 } },
      { key: 'wet60', label: 'חדר רטוב עם דרישת אש', sub: '2.4 × 2.6 מ\', שכבה בכל צד', set: { place: 'wet', fire: '60', L: 2.4, H: 2.6, sides: '2', layers: '1', size: '2.60', thick: '12.5', waste: 10, price: 0 } },
      { key: 'long', label: 'קיר של 100 מטר', sub: 'גובה 3 מ\', צד אחד, שכבה אחת', set: { place: 'dry', fire: '60', L: 100, H: 3, sides: '1', layers: '1', size: '3.00', thick: '12.5', waste: 10, price: 0 } }
    ],
    defaults: function () { return { place: 'esc', fire: '120', L: 4, H: 2.6, sides: '2', layers: '2', size: '2.60', thick: '12.5', waste: 10, price: 80.8 }; },
    fields: [
      { id: 'place', label: 'איפה הקיר', type: 'select', options: Object.keys(PLACE).map(function (k) { return { value: k, label: PLACE[k] }; }) },
      { id: 'fire', label: 'דרישת עמידות האש מהיועץ או מההיתר', type: 'segmented', options: [{ value: '0', label: 'אין' }, { value: '30', label: '30' }, { value: '60', label: '60' }, { value: '90', label: '90' }, { value: '120', label: '120' }],
        help: 'בדקות. את הדרישה קובע יועץ הבטיחות לפי ההיתר, לא הספק ולא הלוח.' },
      { id: 'L', label: 'אורך הקיר (מטר)', type: 'number' },
      { id: 'H', label: 'גובה הקיר (מטר)', type: 'number' },
      { id: 'sides', label: 'צדדים עם לוחות', type: 'segmented', options: [{ value: '1', label: 'צד אחד' }, { value: '2', label: 'שני צדדים' }] },
      { id: 'layers', label: 'שכבות בכל צד', type: 'segmented', options: [{ value: '1', label: 'שכבה אחת' }, { value: '2', label: 'שתי שכבות' }] },
      { id: 'size', label: 'מידת הלוח (מטר)', type: 'segmented', options: [{ value: '2.00', label: '2.00 × 1.20' }, { value: '2.60', label: '2.60 × 1.20' }, { value: '2.80', label: '2.80 × 1.20' }, { value: '3.00', label: '3.00 × 1.20' }],
        showIf: function (v) { return v.place !== 'shaft' && v.place !== 'steel'; } },
      { id: 'thick', label: 'עובי הלוח', type: 'segmented', options: [{ value: '12.5', label: '12.5 מ"מ' }, { value: '16', label: '16 מ"מ' }],
        showIf: function (v) { return v.place !== 'shaft' && v.place !== 'steel'; } },
      { id: 'waste', label: 'פחת (באחוזים, לפי הקיר שלכם)', type: 'percent', help: 'חיתוכים סביב פתחים ופינות. בקיר ישר בלי פתחים הפחת קטן, ובקיר עם הרבה פתחים גדול יותר.' },
      { id: 'price', label: 'מחיר ללוח (₪)', type: 'number', help: 'מתמלא לפי מחיר של ספק כשיש לנו מחיר בדוק למידה הזאת. אפשר להקליד מחיר מהצעה שקיבלתם.' }
    ],
    onField: function (id, v, data, redraw) {
      if (id !== 'size' && id !== 'thick' && id !== 'place' && id !== 'fire') return;
      var kind = boardFor(v.place, +v.fire), p = kind ? priceFor(data.gwall, kind, v.thick, v.size) : null;
      v.price = p ? p.v : 0; redraw('price');
    },
    compute: function (v, data) {
      var d = data.gwall, fire = +v.fire, sides = +v.sides, layers = +v.layers;
      if (!(v.L > 0 && v.L <= 500)) return { error: { field: 'L', msg: 'הקלידו אורך בין 0.1 ל-500 מטר.' } };
      if (!(v.H > 0 && v.H <= 12)) return { error: { field: 'H', msg: 'הקלידו גובה בין 0.1 ל-12 מטר.' } };
      if (!(v.waste >= 0 && v.waste <= 50)) return { error: { field: 'waste', msg: 'פחת בין 0% ל-50%.' } };
      var kind = boardFor(v.place, fire);
      if (!kind) {
        return {
          answer: { label: 'קיר חוץ', value: 'לא לוח ורוד', tone: 'survey', sub: 'לוח גבס ורוד מיועד לשימוש פנימי בלבד' },
          note: 'לקיר חוץ יש לוחות חוץ: כחול (סופרבורד), כתום (אקסטרים בורד) וצהוב (דנסגלאס), ואף אחד מהם אינו לוח אש. לקיר חוץ עם דרישת אש יש לוח חוץ מיוחד שמסווג A1 לפי ת"י 755 (סופרפייר של טמבור). את המערכת קובעים היועץ והיצרן.',
          sources: [d.sources[1]], text: 'קיר חוץ: לוח גבס ורוד מיועד לשימוש פנימי בלבד. לחוץ יש לוחות חוץ, ולקיר חוץ עם דרישת אש לוח חוץ מסווג A1 לפי ת"י 755.'
        };
      }
      var fd = kind === 'fd', thick = fd ? '24' : v.thick, size = fd ? '2.50' : v.size, lb = fd ? d.fd.len : +v.size;
      var c = count(v.L, v.H, sides, layers, lb, d.width, v.waste), kg = boardKg(d, kind, thick, size, lb);
      var price = v.price > 0 ? v.price : 0, p = priceFor(d, kind, thick, size);
      var test = null;
      if (kind === 'fr' && sides === 2 && layers === 2 && thick === '12.5') test = d.tested.fr2x2;
      if (fd && layers === 2) test = d.tested.fd2;
      var lines = [  // the engine prints values in one line (mono, no wrap): numbers on the right, words in the label
        { label: 'הלוח: ' + KIND[kind].name, value: thick + ' מ"מ · ' + size + ' × 1.20' },
        { label: 'לפי שטח, עם ' + F.num(v.waste) + '% פחת', value: F.num(c.byArea) + ' לוחות' },
        { label: 'לפי תוכנית חיתוך: ' + F.num(c.cols) + (c.cols > 1 ? ' עמודות' : ' עמודה') + ' של 1.20 מ\', ' + (c.perCol > 1 ? F.num(c.perCol) + ' חלקים לגובה' : 'לוח אחד לגובה') + ', ' + (sides * layers > 1 ? (sides * layers) + ' שכבות' : 'שכבה אחת'), value: F.num(c.byCut) + ' לוחות' },
        { label: 'שטח הלוחות על הקיר', value: F.num(c.area, 1) + ' מ"ר' }
      ];
      if (kg) lines.push({ label: 'משקל: ' + F.num(kg.kg, kg.calc ? 1 : 0) + ' ק"ג ללוח' + (kg.calc ? ' (חישוב לפי ' + F.num(d.kgm2[thick], 1) + ' ק"ג למ"ר)' : ' (טבלת ספק)'), value: 'כ-' + F.num(Math.round(c.order * kg.kg)) + ' ק"ג' });
      if (price) lines.push({ label: 'עלות: ' + F.num(price, price % 1 ? 2 : 0) + ' ₪ ללוח' + (p && p.v === price ? ' (' + p.src + ', 25.10.2026)' : ''), value: F.ils(c.order * price) });
      var notes = [];
      if (v.place === 'esc' && fire === 0) notes.push('בחדר מדרגות ובמסדרון מילוט דרישת האש נקבעת בהיתר. בחרו את מספר הדקות שקבע היועץ.');
      if (kind === 'mr') notes.push('בלי דרישת אש מתאים לוח ירוק. אם יש דרישת אש, בחרו את מספר הדקות והמחשבון יעבור ללוח המשולב.');
      if (kind === 're') notes.push('בלי דרישת אש מתאים לוח לבן רגיל, זול יותר: אצל רוטנברג הוורוד יקר בכ-32% מהלבן באותה מידה.');
      if (kind === 'fm') notes.push('הלוח המשולב מעכב בעירה ועמיד במים ובלחות, לשימוש פנימי. את המשקל והמחיר שלו בקשו מהספק.');
      if (fd) notes.push('בפירים, בתעלות ובפלדה בונים לפי מערכת מיוחדת שנבדקה, עם לוחות של 22 עד 25 מ"מ. המספרים כאן לפי לוח פייר דיפנדר של 2.50 × 1.20 מ\' (69 ק"ג, טבלת ספק).');
      if (c.perCol > 1 && !fd) notes.push('הקיר גבוה מהלוח, ולכן יש תפרים אופקיים. לוח ארוך יותר חוסך תפרים, ובהזמנה מיוחדת יש לוחות עד 3.60 מ\'.');
      if (fire > 0 && kind !== 're' && kind !== 'mr') {
        if (test && test.min >= fire) notes.push('דוגמה של ספק שמתאימה להרכב הזה: ' + test.what + ', ' + test.frame + (test.wool ? ', ' + test.wool : '') + ': ' + (test.minText || test.min + ' דקות') + ' (' + test.src + '). זו דוגמה, לא אישור לקיר שלכם.');
        else notes.push('לא מצאנו אצל הספקים שבדקנו מחיצה שנבדקה בהרכב הזה. בקשו מהיועץ את המערכת שנבדקה לפי ת"י 931 ובנו בדיוק לפיה.');
        notes.push('מה לבקש מהקבלן: ' + d.docs.join('; ') + '.');
      }
      var o = { L: v.L, H: v.H, lb: lb, width: d.width, perCol: c.perCol, kind: kind, sides: sides, layers: layers, thick: thick, fire: fire,
        wool: test && test.wool, frame: test && test.frame ? test.frame.replace('ניצבי פלדה', 'ניצבים') + (test.wool ? ' + ' + test.wool.replace(/, .*$/, '') : '') : '',
        title: 'חזית הקיר: ' + F.num(c.cols) + (c.cols > 1 ? ' עמודות' : ' עמודה') + ' של 1.20 מ\'',
        caption: 'חתך: ' + (sides > 1 ? 'שני צדדים' : 'צד אחד') + ', ' + (layers > 1 ? 'שתי שכבות' : 'שכבה אחת') + ' בכל צד',
        aria: 'שרטוט הקיר: ' + m(v.L) + ' על ' + m(v.H) + ' מטר, ' + F.num(c.cols) + ' עמודות של לוחות' };
      var out = {
        answer: { label: KIND[kind].name, value: F.num(c.order) + ' לוחות', sub: esc(m(v.L) + ' × ' + m(v.H) + ' מ\' · ' + (sides > 1 ? 'שני צדדים' : 'צד אחד') + ' · ' + (layers > 1 ? 'שתי שכבות' : 'שכבה אחת') + ' בכל צד') },
        figure: svg(o),
        lines: lines,
        note: notes.filter(Boolean).map(esc).join('<br>'),
        formula: 'להזמנה: המספר הגדול מבין שתי הדרכים. לפי שטח = אורך × גובה × צדדים × שכבות × (1 + פחת) ÷ ' + F.num(c.boardArea, 2) + ' מ"ר ללוח, מעוגל למעלה. לפי תוכנית חיתוך: עמודות של 1.20 מ\' לאורך הקיר; החלקים העליונים, העמודה הצרה בקצה והפינה נחתכים מלוחות שלמים, כמה חלקים מכל לוח.',
        sources: d.sources,
        text: 'קיר ' + m(v.L) + ' × ' + m(v.H) + ' מ\', ' + (sides > 1 ? 'שני צדדים' : 'צד אחד') + ', ' + (layers > 1 ? 'שתי שכבות' : 'שכבה אחת') + ' בכל צד: ' + F.num(c.order) + ' לוחות (' + KIND[kind].name + ')'
          + (kg ? ', כ-' + F.num(Math.round(c.order * kg.kg)) + ' ק"ג' : '') + (price ? ', כ-' + F.ils(c.order * price) : '') + '.'
      };
      if (kind === 'fr' && thick === '12.5' && size === '2.60') out.table = { title: 'כמה יעלו ' + F.num(c.order) + ' לוחות אצל כל ספק (25.10.2026)', head: ['ספק', 'מחיר ללוח', 'סך הכול', 'מע"מ'], num: [1, 2], phoneHide: [3],
        rows: d.offers.map(function (x) { return [x.s, F.num(x.v, x.v % 1 ? 2 : 0) + ' ₪', F.ils(x.v * c.order), x.t]; }) };
      return out;
    }
  });
})();
