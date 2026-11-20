/* NadLan Instruments · rentfair v1 (G5, Ben 26.10.2026: a winning owner page for "דירות להשכרה" / "דירה להשכרה").
   NEW file, local only until a release. "כמה שכר דירה הוגן לדירה הזאת": the asked rent against the official numbers, and what the
   law and the tax rules say about this lease.
   - The rent: the government site's median rent for the city and the room count (data.nadlan.gov.il, April to June 2026), the
     city's own yearly change, the CBS average of the same size group with its sampling error (table 4.9, 18 cities), the national
     median, and, when a neighbourhood is picked, the neighbourhood's median (all sizes) and our own estimate for the room count
     (city median for the rooms x neighbourhood / city, all sizes). The median carried to the newest month of the CBS rent index is
     our calculation too. Every one of our numbers is labelled "החישוב שלנו".
   - The lease (Rental and Loan Law, sign 6): does the fair-rental chapter apply (3 months to 10 years, rent under the ceiling), the
     largest guarantee the landlord may ask when it costs the tenant money (the lower of 3 months and a third of the lease's rent),
     its return within 60 days, repairs in 3 / 30 days, the 90 / 60 day notices, who pays the broker.
   - The landlord's tax (2026): the monthly exemption (5,654 ₪, partial up to 11,308 ₪), the 10% track with the 7,500 ₪ offset for
     an owner of one home who rents elsewhere, and the regular track's first bracket before expenses (31%, or 10% from age 60).
   Data: rent.json (tools/instruments/build_rent_data.py). Design: NadLan Instruments (ink, sea, deep, line; survey red only for a
   guarantee above the legal cap). Pure logic in NLRF for unit checks (tools/instruments/test_rentfair.js). */
(function () {
  'use strict';
  var GROUP = { '2': '1-2', '3': '2.5-3', '4': '3.5-4', '5': '4.5+' };
  var QM = { '03': 'ינואר עד מרץ', '06': 'אפריל עד יוני', '09': 'יולי עד ספטמבר', '12': 'אוקטובר עד דצמבר' };
  var HM = ['ינואר', 'פברואר', 'מרץ', 'אפריל', 'מאי', 'יוני', 'יולי', 'אוגוסט', 'ספטמבר', 'אוקטובר', 'נובמבר', 'דצמבר'];
  function qlab(q) { var p = String(q).split('-'); return (QM[p[1]] || p[1]) + ' ' + p[0]; }
  function mlab(m) { var p = String(m).split('-'); return (HM[+p[1] - 1] || p[1]) + ' ' + p[0]; }
  function cityOf(d, n) { for (var i = 0; i < d.cities.length; i++) if (d.cities[i].n === n) return d.cities[i]; return null; }
  function hoodOf(c, h) { if (!c || !h) return null; for (var i = 0; i < c.nb.length; i++) if (c.nb[i][0] === h) return { n: c.nb[i][0], v: c.nb[i][1], rank: i + 1, of: c.nb.length }; return null; }
  /** The CBS rent index carried from the end of quarter q to the newest month: product of (1 + monthly change). */
  function carry(idx, q) { var f = 1; idx.s.forEach(function (m) { if (m[0] > q) f *= 1 + m[1] / 100; }); return f; }
  /** The reference numbers for a city, a neighbourhood ('' = the whole city) and a room count. */
  function ref(d, cityName, hood, rooms) {
    var c = cityOf(d, cityName); if (!c) return null;
    var g = c.r[String(rooms)] || null, cb = c.cbs && c.cbs[GROUP[String(rooms)]] || null, nat = d.nat.r[String(rooms)] || null;
    var h = hoodOf(c, hood), all = c.r.all || null;
    var o = { city: c, gov: g, cbs: cb, nat: nat, natCbs: d.nat.cbs[GROUP[String(rooms)]] || null, hood: h, all: all };
    // the file's neighbourhood figure is on the city's last-year basis (all sizes): Tel Aviv 8,000 = settlementPrice = all.ly, not the quarter's 8,300
    if (h && g && all) { o.allLy = all.ly || all.v; o.hoodF = h.v / o.allLy; o.est = g.v * o.hoodF; }
    o.base = o.est || (g ? g.v : (cb ? cb.a : null));
    o.baseKind = o.est ? 'hood' : g ? 'gov' : cb ? 'cbs' : null;
    if (g) { o.carry = carry(d.idx, g.q); o.now = g.v * o.carry; }
    return o;
  }
  /** Fair-rental chapter: does it apply, and the guarantee cap when the guarantee costs the tenant money (section 25י(ב)). */
  function lease(law, rent, months) {
    var s = law.scope, why = [];
    if (!(months > s.minMonths)) why.push('חוזה של עד ' + s.minMonths + ' חודשים בלי אופציה');
    if (months > s.maxYears * 12) why.push('חוזה של יותר מ־' + s.maxYears + ' שנים');
    if (rent > s.ceiling) why.push('שכר דירה מעל ' + s.ceiling.toLocaleString('en-US') + ' ₪ לחודש');
    var cap = Math.min(law.guarantee.months * rent, rent * months * law.guarantee.share);
    return { applies: !why.length, why: why, cap: cap, by: law.guarantee.months * rent <= rent * months * law.guarantee.share ? 'months' : 'third' };
  }
  /** The landlord's tax per year on the total monthly rent T (this flat + the others), three tracks (2026 rules). */
  function tax(t, total, age60, paidOwn) {
    var C = t.ceiling, D = t.double, rate = age60 ? t.first60 : t.first;
    var taxable = total <= C ? 0 : total >= D ? total : total - (D - total);   // exempt part = C - (T - C) = D - T
    var off = paidOwn > 0 ? Math.min(paidOwn, t.offsetCap) : 0;
    var tenBase = Math.max(0, total - off);
    return { exempt: { taxable: taxable, year: 12 * taxable * rate, full: taxable === 0, none: total >= D },
             ten: { base: tenBase, year: 12 * tenBase * t.ten, off: off },
             reg: { year: 12 * total * rate, rate: rate } };
  }
  function position(asked, base) { return base > 0 ? { diff: asked - base, pct: (asked - base) / base } : null; }
  window.NLRF = { ref: ref, lease: lease, tax: tax, position: position, carry: carry, cityOf: cityOf, hoodOf: hoodOf, GROUP: GROUP };
  if (!window.NadLanInstruments) return;
  var NI = window.NadLanInstruments, F = NI.fmt, esc = NI.esc;
  function sp(x, d) { return (x > 0 ? '+' : x < 0 ? '−' : '') + F.num(Math.abs(100 * x), d == null ? 1 : d) + '%'; }
  function roomsLab(r) { return r === '2' ? 'עד 2 חדרים' : r + ' חדרים'; }
  var GL = { '1-2': '1 עד 2 חדרים', '2.5-3': '2.5 עד 3 חדרים', '3.5-4': '3.5 עד 4 חדרים', '4.5+': '4.5 חדרים ומעלה' };
  function pre(p, lab) { return lab.charAt(0) === 'ה' ? p + lab.slice(1) : p + lab; }  // ל + החציון = לחציון

  /* The figure: one ruler (the references and the reader's rent) and the city's 12 quarters for the room count. Escaped parts only.
     360 units wide so the 12 to 13 px text stays readable on a phone; Hebrew labels carry direction="rtl", where text-anchor
     "start" puts the text's right edge at x (tx() takes the visual side and maps it). */
  function tx(x, y, s, side, size, fill, mono, weight) {
    var a = mono ? { right: 'end', left: 'start', middle: 'middle' }[side] : { right: 'start', left: 'end', middle: 'middle' }[side];
    return '<text x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" text-anchor="' + a + '" font-size="' + size + '"' + (weight ? ' font-weight="' + weight + '"' : '') + ' fill="' + fill + '"' +
      (mono ? ' font-family="IBM Plex Mono, ui-monospace, monospace" direction="ltr"' : ' direction="rtl"') + '>' + esc(s) + '</text>';
  }
  function ruler(o, asked, rooms) {
    var W = 360, P = 14, pts = [];
    if (o.gov) pts.push({ v: o.gov.v, t: 'בעיר', c: '#12202A' });
    if (o.est) pts.push({ v: o.est, t: 'בשכונה (שלנו)', c: '#2F6F86' });
    if (o.cbs) pts.push({ v: o.cbs.a, t: 'הלמ״ס', c: '#1F4B5C', e: o.cbs.e });
    if (o.nat) pts.push({ v: o.nat.v, t: 'ארצי', c: '#5E6A75' });
    var vals = pts.map(function (p) { return p.v; }).concat([asked]);
    var lo = Math.min.apply(null, vals), hi = Math.max.apply(null, vals), pad = Math.max(150, (hi - lo) * 0.08); lo -= pad; hi += pad;
    var x = function (v) { return P + (W - 2 * P) * (v - lo) / (hi - lo); };
    var side = function (px) { return px < 90 ? 'left' : px > W - 90 ? 'right' : 'middle'; };
    var H = o.gov && o.gov.s && o.gov.s.length > 3 ? 262 : 168;
    var s = '<svg viewBox="0 0 360 ' + H + '" role="img" aria-label="' + esc('שכר הדירה שלכם מול החציון בעיר, ממוצע הלמ״ס והחציון הארצי, ' + roomsLab(rooms)) + '" font-family="IBM Plex Sans Hebrew, system-ui, sans-serif">';
    s += '<rect x="0" y="0" width="360" height="' + H + '" fill="#F6F8F9"/>';
    for (var gx = 0; gx <= 360; gx += 18) s += '<line x1="' + gx + '" y1="0" x2="' + gx + '" y2="' + H + '" stroke="#D3DCE2" stroke-width="0.5" opacity="0.6"/>';
    var ax = x(asked), AY = 84;
    s += tx(ax, 20, 'שלכם', side(ax), 13, '#12202A', false, 700) + tx(ax, 37, F.ils(asked), side(ax), 13, '#12202A', true, 600);
    s += '<path d="M' + ax.toFixed(1) + ' ' + (AY - 6) + ' l-7 -12 h14 z" fill="#12202A"/>';
    s += '<line x1="' + P + '" y1="' + AY + '" x2="' + (W - P) + '" y2="' + AY + '" stroke="#12202A" stroke-width="1.5"/>';
    pts.sort(function (a, b) { return a.v - b.v; });
    var lastX = -999, row = 0;
    pts.forEach(function (p) {
      var px = x(p.v);
      row = px - lastX < 78 ? (row + 1) % 2 : 0; lastX = px;
      var ty = AY + 26 + row * 34;
      if (p.e) s += '<line x1="' + x(p.v - p.e).toFixed(1) + '" y1="' + AY + '" x2="' + x(p.v + p.e).toFixed(1) + '" y2="' + AY + '" stroke="' + p.c + '" stroke-width="8" opacity="0.35"/>';
      s += '<line x1="' + px.toFixed(1) + '" y1="' + AY + '" x2="' + px.toFixed(1) + '" y2="' + (ty - 12) + '" stroke="' + p.c + '" stroke-width="1" opacity="0.7"/>';
      s += '<circle cx="' + px.toFixed(1) + '" cy="' + AY + '" r="5" fill="' + p.c + '"/>';
      s += tx(px, ty, p.t, side(px), 12.5, p.c) + tx(px, ty + 15, F.ils(p.v), side(px), 12.5, p.c, true);
    });
    var ser = o.gov ? o.gov.s : null;
    if (ser && ser.length > 3) {
      var y0 = 204, y1 = 238, mn = Math.min.apply(null, ser.map(function (a) { return a[1]; })), mx = Math.max.apply(null, ser.map(function (a) { return a[1]; }));
      if (mx === mn) mx = mn + 1;
      var sx = function (i) { return 58 + (W - 58 - P - 52) * i / (ser.length - 1); }, sy = function (v) { return y1 - (y1 - y0) * (v - mn) / (mx - mn); };
      s += '<line x1="' + P + '" y1="172" x2="' + (W - P) + '" y2="172" stroke="#D3DCE2"/>';
      s += tx(W - P, 188, 'החציון ב' + o.city.n + ', ' + roomsLab(rooms) + ', ' + ser.length + ' רבעונים', 'right', 12, '#3E4C58');
      s += '<polyline fill="none" stroke="#2F6F86" stroke-width="2" points="' + ser.map(function (a, i) { return sx(i).toFixed(1) + ',' + sy(a[1]).toFixed(1); }).join(' ') + '"/>';
      var L = ser.length - 1;
      s += '<circle cx="' + sx(L).toFixed(1) + '" cy="' + sy(ser[L][1]).toFixed(1) + '" r="3.5" fill="#1F4B5C"/>';
      s += tx(sx(0) - 6, sy(ser[0][1]) + 4, F.num(ser[0][1]), 'right', 12, '#5E6A75', true) + tx(sx(L) + 6, sy(ser[L][1]) + 4, F.num(ser[L][1]), 'left', 12, '#12202A', true);
      s += tx(sx(0), 254, ser[0][0].slice(5) + '/' + ser[0][0].slice(2, 4), 'middle', 12, '#5E6A75', true) + tx(sx(L), 254, ser[L][0].slice(5) + '/' + ser[L][0].slice(2, 4), 'middle', 12, '#5E6A75', true);
    }
    return s + '</svg>';
  }

  NI.register('rentfair', {
    kicker: 'בדיקה · שכר דירה',
    title: 'כמה שכר דירה הוגן לדירה הזאת',
    lede: 'בוחרים עיר, שכונה ומספר חדרים, וכותבים את שכר הדירה שמבקשים מכם או שאתם מבקשים. רואים איפה הסכום עומד מול החציון הרשמי בעיר, מול הממוצע של הלמ״ס ומול השכונה, כמה ערובה מותר לבקש לפי החוק, ומה המס של המשכיר.',
    strip: function (dd) { var d = dd.rent; return [
      { label: 'חציון ארצי, 4 חדרים, ' + qlab(d.nat.r['4'].q), value: F.ils(d.nat.r['4'].v) },
      { label: 'שכר דירה ב־12 חודשים, מדד הלמ״ס ל' + mlab(d.idx.last), value: sp(d.idx.yoy / 100) },
      { label: 'פטור ממס למשכיר, ' + d.tax.year, value: F.ils(d.tax.ceiling) + ' לחודש' }]; },
    defaults: function () { return { role: 'tenant', city: 'תל אביב-יפו', hood: '', rooms: '3', rent: 8600, months: 12, guar: 25800, broker: 'none', other: 0, age: 'u60', paid: 0 }; },
    presets: function () { return [
      { key: 'ta3', label: 'תל אביב, 3 חדרים', sub: '8,600 ₪ בחודש', set: { role: 'tenant', city: 'תל אביב-יפו', hood: '', rooms: '3', rent: 8600, months: 12, guar: 25800 } },
      { key: 'jlm4', label: 'ירושלים, 4 חדרים', sub: '7,200 ₪ בחודש', set: { role: 'tenant', city: 'ירושלים', hood: '', rooms: '4', rent: 7200, months: 12, guar: 21600 } },
      { key: 'hfa4', label: 'חיפה, 4 חדרים', sub: '4,600 ₪ בחודש', set: { role: 'tenant', city: 'חיפה', hood: '', rooms: '4', rent: 4600, months: 12, guar: 13800 } },
      { key: 'bs3', label: 'באר שבע, 3 חדרים', sub: '2,800 ₪ בחודש', set: { role: 'tenant', city: 'באר שבע', hood: '', rooms: '3', rent: 2800, months: 12, guar: 8400 } },
      { key: 'pt4', label: 'משכירים בפתח תקווה', sub: '4 חדרים, 6,000 ₪', set: { role: 'landlord', city: 'פתח תקווה', hood: '', rooms: '4', rent: 6000, months: 12, guar: 18000, other: 0, age: 'u60', paid: 0 } }]; },
    fields: [
      { id: 'role', label: 'אתם', type: 'segmented', options: [{ value: 'tenant', label: 'שוכרים' }, { value: 'landlord', label: 'משכירים' }] },
      { id: 'city', label: 'עיר', type: 'select', optionsFrom: function (v, dd) { return dd.rent.cities.slice().sort(function (a, b) { return a.n.localeCompare(b.n, 'he'); }).map(function (c) { return { value: c.n, label: c.n }; }); } },
      { id: 'hood', label: 'שכונה', type: 'select', optionsFrom: function (v, dd) { var c = cityOf(dd.rent, v.city); var o = [{ value: '', label: 'כל העיר' }]; if (c) c.nb.slice().sort(function (a, b) { return a[0].localeCompare(b[0], 'he'); }).forEach(function (n) { o.push({ value: n[0], label: n[0] }); }); return o; },
        help: 'השכונות שבקובץ הממשלתי, עם שכר דירה חציוני לכל הגדלים.' },
      { id: 'rooms', label: 'חדרים', type: 'select', optionsFrom: function (v, dd) { var c = cityOf(dd.rent, v.city), o = []; if (!c) return o;
        if (c.cbs && c.cbs['1-2']) o.push({ value: '2', label: 'עד 2 חדרים (ממוצע הלמ״ס)' });
        ['3', '4', '5'].forEach(function (r) { if (c.r[r] || (c.cbs && c.cbs[GROUP[r]])) o.push({ value: r, label: r + ' חדרים' }); }); return o; } },
      { id: 'rent', label: 'שכר הדירה לחודש', type: 'money', unit: '₪' },
      { id: 'months', label: 'תקופת החוזה', type: 'number', unit: 'חודשים' },
      { id: 'guar', label: 'סך הערובות שעולות כסף', type: 'money', unit: '₪', help: 'פיקדון במזומן, ערבות בנקאית או ערבות מחברה בתשלום. ערבים אישיים לא נספרים בתקרה.' },
      { id: 'broker', label: 'מתווך', type: 'segmented', options: [{ value: 'none', label: 'בלי מתווך' }, { value: 'landlord', label: 'מטעם המשכיר' }, { value: 'tenant', label: 'השוכר הזמין' }] },
      { id: 'other', label: 'שכר דירה מדירות נוספות שלכם, לחודש', type: 'money', unit: '₪', showIf: function (v) { return v.role === 'landlord'; }, help: 'הפטור ממס נבדק על סך שכר הדירה מכל הדירות.' },
      { id: 'age', label: 'גיל המשכיר', type: 'segmented', options: [{ value: 'u60', label: 'עד 60' }, { value: 'o60', label: '60 ומעלה' }], showIf: function (v) { return v.role === 'landlord'; } },
      { id: 'paid', label: 'שכר דירה שאתם משלמים על דירה אחרת', type: 'money', unit: '₪', showIf: function (v) { return v.role === 'landlord'; }, help: 'למי שזו דירתו היחידה: מקטין את הבסיס במסלול 10%, עד 7,500 ₪ לחודש.' }
    ],
    onField: function (id, v, dd, redraw) {
      if (id === 'city') { v.hood = ''; var c = cityOf(dd.rent, v.city); if (c && !c.r[v.rooms] && !(c.cbs && c.cbs[GROUP[v.rooms]])) v.rooms = c.r['3'] ? '3' : c.r['4'] ? '4' : '5'; }
      if (id === 'rent' && v.months > 0 && isFinite(v.rent)) { v.guar = Math.round(Math.min(3 * v.rent, v.rent * v.months / 3)); redraw('guar'); }
    },
    compute: function (v, dd, scen) {
      var d = dd.rent, L = d.law;
      if (!(v.rent >= 500 && v.rent <= 100000)) return { error: { field: 'rent', msg: 'שכר דירה בין 500 ל־100,000 ₪ לחודש.' } };
      if (!(v.months >= 1 && v.months <= 240)) return { error: { field: 'months', msg: 'תקופה בין חודש ל־240 חודשים.' } };
      if (!(v.guar >= 0)) return { error: { field: 'guar', msg: 'סכום הערובה בשקלים, 0 אם אין.' } };
      var o = ref(d, v.city, v.hood, v.rooms);
      if (!o || !o.base) return { error: { field: 'rooms', msg: 'אין נתון רשמי לגודל הזה בעיר. בחרו גודל אחר.' } };
      var kind = scen || o.baseKind, base = o.base, baseLab;
      if (kind === 'gov' && o.gov) { base = o.gov.v; baseLab = 'החציון ב' + o.city.n; }
      else if (kind === 'hood' && o.est) { base = o.est; baseLab = 'ההערכה לשכונה ' + o.hood.n + ' (החישוב שלנו)'; }
      else if (kind === 'cbs' && o.cbs) { base = o.cbs.a; baseLab = 'ממוצע הלמ״ס ב' + o.city.n; }
      else if (kind === 'nat' && o.nat) { base = o.nat.v; baseLab = 'החציון הארצי'; }
      else { kind = o.baseKind; baseLab = kind === 'hood' ? 'ההערכה לשכונה ' + o.hood.n + ' (החישוב שלנו)' : kind === 'gov' ? 'החציון ב' + o.city.n : 'ממוצע הלמ״ס ב' + o.city.n; }
      var pos = position(v.rent, base), ls = lease(L, v.rent, v.months), over = v.guar > ls.cap + 0.5 && ls.applies;
      var lines = [];
      if (o.gov) { lines.push({ label: 'החציון הרשמי, ' + roomsLab(v.rooms) + ' ב' + o.city.n + ', ' + qlab(o.gov.q), value: F.ils(o.gov.v) });
        if (o.gov.yoy != null) lines.push({ label: 'השינוי בשנה האחרונה לפי הקובץ', value: sp(o.gov.yoy / 100) });
        lines.push({ label: 'החציון אחרי מדד שכר הדירה עד ' + mlab(d.idx.last) + ' (החישוב שלנו)', value: F.ils(Math.round(o.now / 10) * 10) }); }
      if (o.hood) { lines.push({ label: 'שכר הדירה בשכונה ' + o.hood.n + ', כל הגדלים, השנה האחרונה', value: F.ils(o.hood.v) + ' · ' + o.hood.rank + ' מתוך ' + o.hood.of + ' בעיר' });
        if (o.est) lines.push({ label: 'השכונה מול העיר, כל הגדלים', value: sp(o.hoodF - 1) }); }
      if (o.cbs) { lines.push({ label: 'ממוצע הלמ״ס, ' + GL[GROUP[v.rooms]] + ', אפריל עד יוני 2026, וטעות הדגימה', value: F.ils(o.cbs.a) + ' (±' + F.num(o.cbs.e) + ')' });
        if (o.cbs.p) lines.push({ label: 'ממוצע הלמ״ס מול אפריל עד יוני 2025 (החישוב שלנו)', value: sp(o.cbs.a / o.cbs.p - 1) }); }
      if (o.nat) lines.push({ label: 'החציון הארצי, ' + roomsLab(v.rooms), value: F.ils(o.nat.v) });
      if (ls.applies) {
        lines.push({ label: 'הערובה המרבית לפי החוק (' + (ls.by === 'months' ? '3 חודשי שכירות' : 'שליש מתקופת החוזה') + ')', value: F.ils(ls.cap) });
        lines.push({ label: over ? 'הערובה שביקשו מעל המותר' : 'הערובה בתוך המותר', value: over ? F.ils(v.guar - ls.cap) + ' יותר מהמותר' : F.ils(v.guar) });
        lines.push({ label: 'החזרת הערובה', value: 'עד ' + L.guarantee.returnDays + ' יום מהחזרת הדירה' });
        lines.push({ label: 'תיקון ליקוי שלא מאפשר לגור / ליקוי אחר', value: 'עד ' + L.repairs.urgent + ' ימים / עד ' + L.repairs.other + ' יום' });
        lines.push({ label: 'הודעה על מימוש אופציה: משכיר / שוכר', value: L.notice.landlordOption + ' / ' + L.notice.tenantOption + ' יום לפני הסוף' });
      } else lines.push({ label: 'פרק השכירות ההוגנת לא חל', value: ls.why.join(', ') });
      if (v.broker === 'landlord') lines.push({ label: 'דמי תיווך', value: 'על המשכיר, לא על השוכר' });
      else if (v.broker === 'tenant') lines.push({ label: 'דמי תיווך', value: 'על מי שהזמין את המתווך, לפי ההסכם בכתב' });
      var tx = null;
      if (v.role === 'landlord') {
        tx = tax(d.tax, v.rent + (v.other || 0), v.age === 'o60', v.paid || 0);
        lines.push({ label: 'מסלול פטור, ' + d.tax.year, value: tx.exempt.full ? 'פטור מלא' : tx.exempt.none ? 'אין פטור (מעל ' + F.ils(d.tax.double) + ')' : F.ils(tx.exempt.taxable) + ' בחודש חייבים, עד ' + F.ils(tx.exempt.year) + ' בשנה' });
        lines.push({ label: 'מסלול 10%' + (tx.ten.off ? ', אחרי קיזוז ' + F.ils(tx.ten.off) : ''), value: F.ils(tx.ten.year) + ' בשנה. מדווחים ומשלמים אחרי סוף שנת המס, ואת היום האחרון בודקים באתר רשות המסים' });
        lines.push({ label: 'מסלול רגיל, ' + F.num(100 * tx.reg.rate) + '% לפני הוצאות ופחת', value: 'עד ' + F.ils(tx.reg.year) + ' בשנה' });
      }
      var scen0 = [];
      if (o.est) scen0.push({ key: 'hood', name: 'מול השכונה', value: sp(position(v.rent, o.est).pct), on: kind === 'hood' });
      if (o.gov) scen0.push({ key: 'gov', name: 'מול העיר', value: sp(position(v.rent, o.gov.v).pct), on: kind === 'gov' });
      if (o.cbs) scen0.push({ key: 'cbs', name: 'מול ממוצע הלמ״ס', value: sp(position(v.rent, o.cbs.a).pct), on: kind === 'cbs' });
      if (o.nat) scen0.push({ key: 'nat', name: 'מול כל הארץ', value: sp(position(v.rent, o.nat.v).pct), on: kind === 'nat' });
      var c = o.city, allv = c.r.all ? (c.r.all.ly || c.r.all.v) : null, rr = c.r[v.rooms];
      var rows = c.nb.map(function (n, i) { return [String(i + 1), n[0], F.ils(n[1]), allv ? sp(n[1] / allv - 1) : '', rr && allv ? F.ils(Math.round(rr.v * n[1] / allv / 50) * 50) : '']; });
      var near = Math.abs(pos.pct) < 0.005 ? pre('בדיוק ב', baseLab) : pos.diff > 0 ? F.ils(pos.diff) + ' מעל ' + baseLab : F.ils(-pos.diff) + ' ' + pre('מתחת ל', baseLab);
      var sub = esc(near + ': ' + F.ils(base)) + (kind === 'gov' || kind === 'hood' ? esc(' (' + qlab(o.gov.q) + ')') : kind === 'cbs' ? esc(' (אפריל עד יוני 2026)') : kind === 'nat' ? esc(' (' + qlab(o.nat.q) + ')') : '');
      if (over) sub += '<br>' + esc('הערובה שביקשו גבוהה ב־' + F.ils(v.guar - ls.cap) + ' מהמותר בחוק.');
      if (tx) sub += '<br>' + esc('המס שלכם: ' + (tx.exempt.full ? 'פטור מלא במסלול הפטור' : 'מסלול 10% ' + F.ils(tx.ten.year) + ' בשנה'));
      var bd = [{ label: 'חודש ראשון', value: v.rent, kind: 'sea' }, { label: over ? 'ערובה עד המותר' : 'ערובה', value: Math.min(v.guar, ls.applies ? ls.cap : v.guar), kind: 'open' }];
      if (over) bd.push({ label: 'מעל המותר', value: v.guar - ls.cap, kind: 'survey' });
      return {
        answer: { label: v.role === 'landlord' ? 'שכר הדירה שתבקשו מול ' + (kind === 'nat' ? 'החציון הארצי' : kind === 'cbs' ? 'ממוצע הלמ״ס' : kind === 'hood' ? 'השכונה' : 'החציון בעיר') : 'שכר הדירה שביקשו מכם מול ' + (kind === 'nat' ? 'החציון הארצי' : kind === 'cbs' ? 'ממוצע הלמ״ס' : kind === 'hood' ? 'השכונה' : 'החציון בעיר'),
          value: Math.abs(pos.pct) < 0.005 ? 'בחציון' : sp(pos.pct), sub: sub, tone: over ? 'survey' : '' },
        figure: ruler(o, v.rent, v.rooms),
        breakdown: bd,
        lines: lines,
        scenarios: scen0, scenarioLabel: 'מול מה משווים',
        note: 'החציון והממוצע הם של חוזים שנחתמו, לא של מודעות. דירה חדשה, חניה, מעלית, ממ״ד, ריהוט, קומה גבוהה או נוף מסבירים פער מעל החציון; דירה בלי אלה, מתחת. הממוצע של הלמ״ס והחציון של האתר הממשלתי נמדדים על מדגמים שונים, ולכן הם לא זהים. זה לא ייעוץ משפטי או ייעוץ מס.',
        formula: 'מיקום = (שכר הדירה פחות הנתון שמשווים אליו) חלקי הנתון. השכונה = החציון בעיר לפי חדרים כפול (שכר הדירה בשכונה חלקי שכר הדירה בעיר, כל הגדלים). המדד = מכפלת השינויים החודשיים של מדד שכר הדירה מסוף הרבעון. ערובה מרבית = הנמוך מבין 3 חודשי שכירות ושליש משכר הדירה לכל התקופה. פטור חלקי: הסכום הפטור = ' + F.num(d.tax.double) + ' פחות שכר הדירה החודשי.',
        sources: [{ label: d.src.gov.he, url: d.src.gov.url }, { label: d.src.cbs49.he, url: d.src.cbs49.url }, { label: d.src.cbsIdx.he, url: d.src.cbsIdx.url }, { label: d.src.law.he, url: d.src.law.url }, { label: d.src.tax.he, url: d.src.tax.url }],
        table: { title: 'השכונות של ' + c.n + ': שכר דירה חציוני בשנה האחרונה, כל הגדלים, והערכה ל־' + roomsLab(v.rooms), head: ['#', 'שכונה', 'כל הגדלים', 'מול העיר (' + F.ils(allv) + ')', 'הערכה ל־' + roomsLab(v.rooms) + ' (החישוב שלנו)'], num: [0, 2, 3, 4], phoneHide: [0], rows: rows },
        text: 'שכר דירה ' + F.ils(v.rent) + ' ל' + roomsLab(v.rooms) + ' ב' + c.n + (o.hood ? ', ' + o.hood.n : '') + ': ' + (Math.abs(pos.pct) < 0.005 ? pre('בדיוק ב', baseLab) : sp(pos.pct) + ' מול ' + baseLab) + ' (' + F.ils(base) + ').' + (ls.applies ? ' ערובה מרבית לפי החוק: ' + F.ils(ls.cap) + '.' : '')
      };
    }
  });
})();
