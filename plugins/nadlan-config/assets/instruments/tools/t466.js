/* NadLan Instruments · t466 v1 (HAD-601, Q5 stage 2, 26.10.2026): "ת"י 466 והדירה שלי" on /glossary/תי-466/. A situation (buying
   new, renovating a concrete wall, building a house, a crack, prestressed or precast or hollow-core slabs; for a new apartment also
   the slab type) becomes: the parts of the concrete code that apply, each with its edition in force and SII price, who is
   responsible, the questions to ask, the related standards, where to read the standard for free, and a section through a residential
   building with the elements of those parts lit in the part's drafting ink. Scope lines from the SII pages only, no clause text.
   Data: data/t466.json (SII standard pages, 25.10.2026). Pure logic in NL466. SVG in RTL: text-anchor start = the right end. */
(function () {
  'use strict';
  /** The parts for a situation (+ the slab type of a new apartment), sorted, without duplicates. */
  function partsFor(d, sit, slab) {
    var s = d.sit[sit]; if (!s) return [];
    var p = s.parts.slice(); if (sit === 'new' && d.slab[slab]) d.slab[slab].forEach(function (x) { if (p.indexOf(x) < 0) p.push(x); });
    return p.sort();
  }
  function list(p) { return p.length === 1 ? 'חלק ' + p[0] : 'חלקים ' + p.slice(0, -1).join(', ') + ' ו-' + p[p.length - 1]; }
  window.NL466 = { partsFor: partsFor, list: list };
  if (!window.NadLanInstruments) return;
  var NI = window.NadLanInstruments, F = NI.fmt, esc = NI.esc;

  function svg(d, on) {
    var W = 420, g = [], ink = function (k) { return on.indexOf(k) > -1 ? d.parts[k].ink : '#C9D1D8'; }, lit = function (k) { return on.indexOf(k) > -1; };
    g.push('<defs><pattern id="t4c" width="9" height="9" patternUnits="userSpaceOnUse"><rect width="9" height="9" fill="#fff"/><circle cx="2" cy="2" r="0.9" fill="#8A97A2"/><path d="M6 5 l1.6 2.6 h-3.2z" fill="none" stroke="#8A97A2" stroke-width="0.7"/></pattern></defs>');
    g.push('<text x="408" y="20" class="t" text-anchor="start">חתך בבניין מגורים: איזה חלק חל על כל אלמנט</text>');
    var x0 = 150, x1 = 360, gy = 262;
    // part 1 frame: applies to the whole structure
    if (lit('1')) g.push('<rect x="' + (x0 - 14) + '" y="34" width="' + (x1 - x0 + 40) + '" height="' + (gy - 34 + 20) + '" fill="none" stroke="' + d.parts['1'].ink + '" stroke-width="1.6" stroke-dasharray="6 4"/><text x="' + (x1 + 22) + '" y="50" class="s" text-anchor="start" style="fill:' + d.parts['1'].ink + '">חלק 1 חל על כל המבנה</text>');
    // ground and foundation
    g.push('<line x1="' + (x0 - 30) + '" y1="' + gy + '" x2="' + (x1 + 30) + '" y2="' + gy + '" stroke="#12202A" stroke-width="1.2"/>');
    g.push('<rect x="' + (x0 - 6) + '" y="' + gy + '" width="' + (x1 - x0 + 12) + '" height="14" fill="url(#t4c)" stroke="' + ink('2') + '" stroke-width="' + (lit('2') ? 2 : 1) + '"/>');
    // columns
    [x0 + 6, (x0 + x1) / 2, x1 - 18].forEach(function (cx) { g.push('<rect x="' + cx + '" y="74" width="12" height="' + (gy - 74) + '" fill="url(#t4c)" stroke="' + ink('2') + '" stroke-width="' + (lit('2') ? 2 : 1) + '"/>'); });
    // slabs: cast (part 2), hollow-core (part 5), post-tensioned roof (part 3)
    g.push('<rect x="' + x0 + '" y="196" width="' + (x1 - x0) + '" height="10" fill="url(#t4c)" stroke="' + ink('2') + '" stroke-width="' + (lit('2') ? 2 : 1) + '"/>');
    g.push('<rect x="' + x0 + '" y="134" width="' + (x1 - x0) + '" height="12" fill="#fff" stroke="' + ink('5') + '" stroke-width="' + (lit('5') ? 2 : 1) + '"/>');
    for (var cx = x0 + 9; cx < x1 - 4; cx += 16) g.push('<circle cx="' + cx + '" cy="140" r="4" fill="none" stroke="' + ink('5') + '" stroke-width="1"/>');
    g.push('<rect x="' + x0 + '" y="70" width="' + (x1 - x0) + '" height="12" fill="url(#t4c)" stroke="' + ink('3') + '" stroke-width="' + (lit('3') ? 2 : 1) + '"/>');
    g.push('<path d="M' + (x0 + 2) + ' 73 Q' + ((x0 + x1) / 2) + ' 84 ' + (x1 - 2) + ' 73" fill="none" stroke="' + ink('3') + '" stroke-width="1.6"/>');
    // precast facade panels (part 4)
    for (var py = 82; py < gy; py += 60) g.push('<rect x="' + (x1 + 2) + '" y="' + py + '" width="12" height="' + Math.min(58, gy - py) + '" fill="url(#t4c)" stroke="' + ink('4') + '" stroke-width="' + (lit('4') ? 2 : 1) + '"/>');
    // labels on the left (rtl anchor start = the right end, at x0 - 22)
    var L = [[76, '3', 'תקרה דרוכה'], [140, '5', 'תקרת לוח"דים'], [201, '2', 'שלד יצוק'], [236, '4', 'חזית טרומית']];
    L.forEach(function (l) {
      var k = l[1], c = ink(k);
      g.push('<circle cx="' + (x0 - 32) + '" cy="' + (l[0] - 4) + '" r="10" fill="' + (lit(k) ? c : '#fff') + '" stroke="' + c + '" stroke-width="1.4"/><text x="' + (x0 - 32) + '" y="' + (l[0] + 1) + '" class="m" text-anchor="middle" style="fill:' + (lit(k) ? '#fff' : '#8A97A2') + '">' + k + '</text>');
      g.push('<text x="' + (x0 - 48) + '" y="' + l[0] + '" class="s" text-anchor="start" style="fill:' + (lit(k) ? '#12202A' : '#8A97A2') + '">' + esc(l[2]) + '</text>');
    });
    if (lit('4')) g.push('<line x1="' + (x0 - 22) + '" y1="232" x2="' + (x1 + 2) + '" y2="232" stroke="' + d.parts['4'].ink + '" stroke-width="0.8" stroke-dasharray="3 3"/>');
    g.push('<text x="408" y="' + (gy + 42) + '" class="s" text-anchor="start">בהיר: חלק שלא נוגע למצב שבחרתם</text>');
    return '<svg class="nli__wall" direction="rtl" viewBox="0 0 ' + W + ' ' + (gy + 52) + '" role="img" aria-label="' + esc('חתך בניין מגורים, מסומנים ' + list(on)) + '">' + g.join('') + '</svg>';
  }

  NI.register('t466', {
    kicker: 'בדיקה · ת"י 466',
    title: 'איזה חלק של ת"י 466 חל אצלכם: בדיקה לפי המצב',
    lede: 'בוחרים את המצב שלכם ומקבלים את חלקי חוקת הבטון שנוגעים לו, את המהדורה שבתוקף בכל חלק, מי אחראי, מה לשאול ואיזה תקן עובד לצידו.',
    presets: [
      { key: 'new', label: 'דירה חדשה מקבלן', sub: 'תקרות יצוקות', set: { sit: 'new', slab: 'cast' } },
      { key: 'newh', label: 'דירה חדשה, תקרות לוח"דים', sub: 'חלקים 1, 2 ו-5', set: { sit: 'new', slab: 'hollow' } },
      { key: 'reno', label: 'פתיחת קיר בשיפוץ', sub: 'קיר בטון', set: { sit: 'reno', slab: 'cast' } },
      { key: 'crack', label: 'סדק או ברזל חשוף', sub: 'בדיקה', set: { sit: 'crack', slab: 'cast' } }
    ],
    defaults: function () { return { sit: 'new', slab: 'cast' }; },
    fields: [
      { id: 'sit', label: 'המצב שלכם', type: 'select', optionsFrom: function (v, data) { var s = data.t466.sit; return Object.keys(s).map(function (k) { return { value: k, label: s[k].label }; }); } },
      { id: 'slab', label: 'התקרות בבניין', type: 'segmented', options: [{ value: 'cast', label: 'יצוקות במקום' }, { value: 'precast', label: 'טרומיות' }, { value: 'hollow', label: 'לוח"דים' }, { value: 'pt', label: 'דרוכות' }, { value: 'unknown', label: 'לא יודעים' }],
        help: 'אם לא יודעים, זו השאלה הראשונה לקבלן: לכל סוג תקרה יש חלק אחר בתקן.', showIf: function (v) { return v.sit === 'new'; } }
    ],
    compute: function (v, data) {
      var d = data.t466, s = d.sit[v.sit];
      if (!s) return { error: { field: 'sit', msg: 'בחרו מצב.' } };
      var on = partsFor(d, v.sit, v.slab), sum = on.reduce(function (a, k) { return a + d.parts[k].price; }, 0);
      var lines = on.map(function (k) { return { label: 'חלק ' + k + ': ' + d.parts[k].name, value: 'מהדורת ' + d.parts[k].ed }; });
      lines.push({ label: 'מחיר ' + (on.length > 1 ? 'החלקים' : 'החלק') + ' במכון התקנים, כולל מע"מ', value: '₪' + F.num(sum, 2) });
      var notes = ['<b>מי אחראי:</b> ' + esc(s.who) + '.', '<b>מה לשאול:</b> ' + s.ask.map(esc).join(' ')];
      if (v.sit === 'new' && v.slab === 'unknown') notes.push('שאלו את הקבלן מה סוג התקרות: לתקרות טרומיות חל גם חלק 4, ללוח"דים חלק 5 ולתקרות דרוכות חלק 3.');
      if (s.rel.length) notes.push('<b>תקן שעובד לצידו:</b> ' + s.rel.map(function (k) { var r = d.related[k]; return esc(r.name) + ' (' + esc(r.ed) + ', ' + esc(r.status) + ')'; }).join('; ') + '.');
      notes.push('<b>לקרוא בלי תשלום:</b> במרכז המידע של מכון התקנים, ' + esc(d.sii.addr) + ', ' + esc(d.sii.hours) + ', בתיאום מראש: ' + esc(d.sii.phone) + '.');
      return {
        answer: { label: 'החלקים של ת"י 466 שנוגעים למצב', value: list(on), sub: esc(s.label + (v.sit === 'new' ? ', תקרות ' + { cast: 'יצוקות במקום', precast: 'טרומיות', hollow: 'מטבלות חלולות', pt: 'דרוכות', unknown: 'מסוג לא ידוע' }[v.slab] : '')) },
        figure: svg(d, on),
        lines: lines,
        note: notes.join('<br>'),
        table: { title: 'מה כל חלק מכסה (לפי מכון התקנים)', head: ['חלק', 'נושא', 'מהדורה', 'החליפה', 'מה הוא מכסה'], phoneHide: [3],
          rows: on.map(function (k) { var p = d.parts[k]; return [k, p.name, p.ed, p.rep || '', p.scope]; }) },
        formula: 'החלקים לפי תחום החלות שמכון התקנים מפרסם לכל חלק. המחיר כפי שמופיע באתר מכון התקנים ב-25.10.2026, כולל מע"מ.',
        sources: d.sources,
        text: 'ת"י 466 (חוקת הבטון), ' + s.label + ': ' + list(on) + ' (' + on.map(function (k) { return 'חלק ' + k + ' מהדורת ' + d.parts[k].ed; }).join(', ') + '). מי אחראי: ' + s.who + '.'
      };
    }
  });
})();
