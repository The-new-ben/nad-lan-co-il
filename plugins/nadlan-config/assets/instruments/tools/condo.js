/* NadLan Instruments · the condo-documents family (HAD-592, /real-estate-lawyer/condo-documents/, the page loop 22.10.2026).
   One file (registry 'file' => 'condo'):
     condo     "which document answers my question": one tap on a buyer's question (parking, storage, roof, yard, balcony, building
               rights, expenses, area, approved drawing, building not registered) lights the matching part of a sample condo drawing
               and opens a card: the document and where in it, what to look for, the red flag, the legal source; under it the
               three-step order path at the government site with the 2026 fee.
     condomaj  "who must agree": an act (registering the condo, agreed bylaws, an attachment, an extension, a safe room) and the
               number of flats give the owners the Land Law requires, drawn as a row of flats.
   Design: DS component CondoDocFinder (https://claude.ai/artifact/L9Nqz7Viv7K3MYeZrBc9s8): the official drawing itself, drafting
   white on a 1:100 grid, navy registry ink, each flat in its own colour with lettered attachments, dashed red for a red flag.
   Data: condo.json (official sources only; the fee is one constant updated each January). We never order on anyone's behalf. */
(function () {
  'use strict';
  /** Owners needed for an act among n flats. basis: flats (a share of the flats), all, area/share (by floor area: with flats of equal
   *  size this is the same share of the flats; the real count follows the order's figures). strict = more than the share. */
  function need(m, n) {
    if (m.basis === 'all') return n;
    var x = m.num ? m.num * n / m.den : m.frac * n;  // two thirds as an exact fraction (0.6667 x 12 would round up to 9)
    return m.strict ? Math.floor(x) + 1 : Math.ceil(x - 1e-9);
  }
  var C = { b: '#3366CC', g: '#2E9E5B', v: '#7F4FC9', c: '#1497B8', ink: '#14213D', red: '#D7263D', grid: '#E6ECF3', com: '#C9D2DD' };
  function hatch(id, col) { return '<pattern id="' + id + '" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="6" height="6" fill="' + col + '" fill-opacity=".14"/><line x1="0" y1="0" x2="0" y2="6" stroke="' + col + '" stroke-width="1.6" stroke-opacity=".75"/></pattern>'; }
  function t(x, y, s, o) { o = o || {}; return '<text x="' + x + '" y="' + y + '" text-anchor="' + (o.a || 'middle') + '" class="' + (o.c || 'tx') + '"' + (o.f ? ' fill="' + o.f + '"' : '') + '>' + s + '</text>'; }
  /** The sample drawing: roof plan, typical floor, ground floor with yards, parking and storage. Items carry data-k for the chips. */
  function sheet() {
    var s = '<svg viewBox="0 0 360 600" role="img" aria-label="תשריט בית משותף לדוגמה: תרשים גג, קומה טיפוסית וקומת קרקע עם חצרות, חניות ומחסנים"><defs>' +
      '<pattern id="cdg" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M10 0H0V10" fill="none" stroke="' + C.grid + '" stroke-width=".6"/></pattern>' +
      hatch('hb', C.b) + hatch('hg', C.g) + hatch('hv', C.v) + hatch('hc', C.c) + hatch('hx', '#7A8798') + '</defs>' +
      '<rect width="360" height="600" fill="#fff"/><rect width="360" height="600" fill="url(#cdg)"/>';
    // title block (the order says: approved drawing or "other drawing")
    s += '<g data-k="approved"><rect x="10" y="8" width="340" height="30" fill="#fff" stroke="' + C.ink + '" stroke-width="1"/>' +
      t(345, 22, 'תשריט בית משותף לדוגמה', { a: 'start', c: 'tb' }) + t(345, 33, 'גוש 0000 · חלקה 00 · 4 תתי־חלקות', { a: 'start', c: 'tm' }) +
      t(16, 22, 'קנ״מ 1:100', { a: 'end', c: 'tm' }) + '<rect x="16" y="25" width="74" height="10" class="stamp"/>' + t(53, 33, 'מאושר בוועדה', { c: 'st' }) + '</g>';
    // roof plan
    s += t(345, 58, 'תרשים גג', { a: 'start', c: 'pn' });
    s += '<g data-k="roof"><rect x="40" y="66" width="170" height="80" fill="url(#hc)" stroke="' + C.c + '" stroke-width="1.6"/>' + t(125, 104, 'ד', { c: 'lt', f: C.c }) + t(125, 120, 'גג מוצמד לתת־חלקה 4', { c: 'sm' }) + '</g>';
    s += '<g data-k="common roof-common"><rect x="210" y="66" width="110" height="80" fill="url(#hx)" stroke="#7A8798" stroke-width="1"/>' +
      '<rect x="222" y="76" width="22" height="12" class="dev"/><rect x="250" y="76" width="22" height="12" class="dev"/><rect x="278" y="76" width="22" height="12" class="dev"/>' +
      t(265, 112, 'גג משותף', { c: 'sm' }) + t(265, 126, 'דודי שמש', { c: 'sm' }) + '</g>';
    s += '<rect x="40" y="66" width="280" height="80" fill="none" stroke="' + C.ink + '" stroke-width="2"/>';
    // typical floor
    s += t(345, 172, 'קומה א׳', { a: 'start', c: 'pn' });
    s += '<g data-k="area"><rect x="40" y="180" width="130" height="100" fill="' + C.v + '" fill-opacity=".08" stroke="' + C.v + '" stroke-width="1.6"/>' + t(105, 222, 'תת־חלקה 3', { c: 'tx', f: C.v }) + t(105, 238, '92 מ״ר', { c: 'tm' }) +
      '<rect x="190" y="180" width="130" height="100" fill="' + C.c + '" fill-opacity=".08" stroke="' + C.c + '" stroke-width="1.6"/>' + t(255, 222, 'תת־חלקה 4', { c: 'tx', f: C.c }) + t(255, 238, '96 מ״ר', { c: 'tm' }) + '</g>';
    s += '<g data-k="common"><rect x="170" y="180" width="20" height="100" fill="url(#hx)" stroke="#7A8798" stroke-width="1"/>' + t(180, 234, 'מדרגות', { c: 'vt' }) + '</g>';
    s += '<g data-k="balc"><rect x="60" y="280" width="80" height="22" fill="url(#hv)" stroke="' + C.v + '" stroke-width="1.6"/>' + t(100, 296, 'ג · מרפסת פתוחה', { c: 'sm', f: C.v }) +
      '<line x1="210" y1="262" x2="300" y2="262" stroke="' + C.c + '" stroke-width="1" stroke-dasharray="2 2"/>' + t(255, 274, 'מרפסת מקורה, בתוך הדירה', { c: 'sm' }) +
      '<rect x="230" y="280" width="70" height="20" class="dev"/>' + t(265, 294, 'סגירה בלי היתר', { c: 'sm', f: C.red }) + '</g>';
    s += '<rect x="40" y="180" width="280" height="100" fill="none" stroke="' + C.ink + '" stroke-width="2"/>';
    // ground floor
    s += t(345, 328, 'קומת קרקע', { a: 'start', c: 'pn' });
    s += '<g data-k="unreg"><rect x="18" y="334" width="324" height="252" fill="none" stroke="' + C.ink + '" stroke-width="1" stroke-dasharray="8 4"/>' + t(180, 582, 'גבול החלקה', { c: 'sm' }) + '</g>';
    s += '<g data-k="area"><rect x="40" y="340" width="130" height="90" fill="' + C.b + '" fill-opacity=".08" stroke="' + C.b + '" stroke-width="1.6"/>' + t(105, 380, 'תת־חלקה 1', { c: 'tx', f: C.b }) + t(105, 396, '88 מ״ר', { c: 'tm' }) +
      '<rect x="190" y="340" width="130" height="90" fill="' + C.g + '" fill-opacity=".08" stroke="' + C.g + '" stroke-width="1.6"/>' + t(255, 380, 'תת־חלקה 2', { c: 'tx', f: C.g }) + t(255, 396, '90 מ״ר', { c: 'tm' }) + '</g>';
    s += '<g data-k="common"><rect x="170" y="340" width="20" height="90" fill="url(#hx)" stroke="#7A8798" stroke-width="1"/>' + t(180, 389, 'לובי', { c: 'vt' }) + '</g>';
    s += '<rect x="40" y="340" width="280" height="90" fill="none" stroke="' + C.ink + '" stroke-width="2"/>';
    s += '<g data-k="yard"><rect x="40" y="432" width="130" height="40" fill="url(#hb)" stroke="' + C.b + '" stroke-width="1.6"/>' + t(105, 457, 'א · חצר 40 מ״ר', { c: 'sm', f: C.b }) +
      '<rect x="190" y="432" width="130" height="40" fill="url(#hg)" stroke="' + C.g + '" stroke-width="1.6"/>' + t(255, 457, 'ב · חצר 38 מ״ר', { c: 'sm', f: C.g }) + '</g>';
    var P = [[C.b, 'hb', 'א1'], [C.g, 'hg', 'ב1'], [C.v, 'hv', 'ג1'], [C.c, 'hc', 'ד1'], ['#7A8798', 'hx', 'משותף']];
    s += '<g data-k="park">' + P.map(function (p, i) { var x = 40 + i * 56; return '<rect x="' + x + '" y="484" width="52" height="40" fill="url(#' + p[1] + ')" stroke="' + p[0] + '" stroke-width="1.6"/>' + t(x + 26, 503, 'P', { c: 'tx', f: p[0] }) + t(x + 26, 517, p[2], { c: 'sm', f: p[0] }); }).join('') + '</g>';
    var M = [[C.b, 'hb', 'א2'], [C.v, 'hv', 'ג2'], ['#7A8798', 'hx', 'משותף']];
    s += '<g data-k="store">' + M.map(function (p, i) { var x = 40 + i * 64; return '<rect x="' + x + '" y="532" width="58" height="36" fill="url(#' + p[1] + ')" stroke="' + p[0] + '" stroke-width="1.6"/>' + t(x + 29, 548, 'מחסן', { c: 'sm', f: p[0] }) + t(x + 29, 561, p[2], { c: 'sm', f: p[0] }); }).join('') +
      '<rect x="236" y="532" width="84" height="36" class="dev"/>' + t(278, 548, 'מחסן שהראו', { c: 'sm', f: C.red }) + t(278, 561, 'ולא בתשריט', { c: 'sm', f: C.red }) + '</g>';
    return s + '</svg>';
  }
  window.NLCD = { need: need, sheet: sheet };
  if (!window.NadLanInstruments) return;
  var NI = window.NadLanInstruments, F = NI.fmt, esc = NI.esc;
  function css() {
    if (document.getElementById('nlcd-css')) return;
    var s = document.createElement('style'); s.id = 'nlcd-css';
    s.textContent = '.nlcd{--cd:#14213D;--cdb:#3366CC;--cdr:#D7263D;--cdl:#E6ECF3}' +
      '.nlcd__chips{display:flex;flex-wrap:wrap;gap:6px;margin:12px 0}.nlcd__chips button{font:500 13.5px/18px var(--nli-sans);min-height:42px;padding:9px 13px;border:1px solid #C9D2DD;border-radius:4px;background:#fff;color:var(--cd);cursor:pointer;margin:0}' +
      '.nlcd__chips button[aria-pressed="true"]{background:var(--cd);border-color:var(--cd);color:#fff}' +
      '.nlcd__wrap{display:grid;grid-template-columns:minmax(0,1fr);gap:14px;align-items:start}@media (min-width:860px){.nlcd__wrap{grid-template-columns:minmax(0,400px) minmax(0,1fr);grid-template-areas:"s c" "s o"}.nlcd__sheet{grid-area:s}.nlcd__card{grid-area:c}.nlcd__order{grid-area:o}}' +
      '.nlcd__sheet{border:1px solid var(--cd);background:#fff;max-width:440px;width:100%;margin:0 auto}.nlcd__sheet svg{display:block;width:100%;height:auto}' +
      '.nlcd__sheet .tx{font:600 12px "IBM Plex Sans Hebrew",sans-serif;fill:#14213D}.nlcd__sheet .sm{font:500 10.5px "IBM Plex Sans Hebrew",sans-serif;fill:#3E4C58}.nlcd__sheet .tm{font:500 10.5px "IBM Plex Mono",monospace;fill:#14213D}' +
      '.nlcd__sheet .tb{font:700 11px "IBM Plex Sans Hebrew",sans-serif;fill:#14213D}.nlcd__sheet .pn{font:700 11px "IBM Plex Sans Hebrew",sans-serif;fill:#14213D}.nlcd__sheet .lt{font:700 22px "IBM Plex Sans Hebrew",sans-serif}' +
      '.nlcd__sheet .vt{font:500 8.5px "IBM Plex Sans Hebrew",sans-serif;fill:#3E4C58;writing-mode:vertical-rl}.nlcd__sheet .st{font:600 8px "IBM Plex Sans Hebrew",sans-serif;fill:#3366CC}' +
      '.nlcd__sheet .stamp{fill:none;stroke:#3366CC;stroke-width:1.2}.nlcd__sheet .dev{fill:none;stroke:#D7263D;stroke-width:1.4;stroke-dasharray:4 3}' +
      '.nlcd__sheet g[data-k]{transition:opacity .25s}.nlcd__sheet.is-focus g[data-k]{opacity:.18}.nlcd__sheet.is-focus g.on{opacity:1}' +
      '.nlcd__card{border:1px solid #C9D2DD;border-inline-start:5px solid var(--cd);background:#fff;padding:14px 16px}.nlcd__card h3{margin:0 0 8px;font:700 19px/24px var(--nli-sans);color:var(--cd)}' +
      '.nlcd__card dl{margin:0;display:grid;gap:10px}.nlcd__card dt{font:600 12px/16px var(--nli-sans);color:#5E6A75;letter-spacing:.02em}.nlcd__card dd{margin:2px 0 0;font:400 15px/23px var(--nli-sans);color:#12202A}' +
      '.nlcd__card .flag{border:1.5px dashed var(--cdr);padding:8px 10px}.nlcd__card .flag dt{color:var(--cdr)}.nlcd__card .src{font:400 12.5px/18px var(--nli-sans);color:#5E6A75}.nlcd__card a{color:var(--cdb)}' +
      '.nlcd__order{margin:14px 0 0;border-top:2px solid var(--cd);padding-top:10px}.nlcd__order h3{margin:0 0 8px;font:700 16px/22px var(--nli-sans);color:var(--cd)}' +
      '.nlcd__order ol{margin:0;padding:0;list-style:none;display:grid;gap:8px;counter-reset:s}.nlcd__order li{counter-increment:s;position:relative;padding-inline-start:36px;font:400 14.5px/22px var(--nli-sans);color:#12202A}' +
      '.nlcd__order li::before{content:counter(s);position:absolute;inset-inline-start:0;top:0;width:26px;height:26px;border:1.5px solid var(--cd);font:600 13px/23px var(--nli-mono);text-align:center;color:var(--cd)}' +
      '.nlcd__order li b{display:block;font-weight:600}.nlcd__order a{color:var(--cdb);font-weight:600}.nlcd__fee{display:inline-block;margin:10px 0 0;font:600 14px var(--nli-mono);color:var(--cd);border:1.5px solid var(--cd);padding:4px 10px}' +
      '.nlcd__note{font:400 12.5px/18px var(--nli-sans);color:#5E6A75;margin:8px 0 0}' +
      '.nlcd__step{display:flex;align-items:center;gap:8px;margin:10px 0}.nlcd__step button{width:44px;height:44px;border:1px solid var(--cd);background:#fff;color:var(--cd);font:600 20px var(--nli-mono);cursor:pointer}' +
      '.nlcd__step output{min-width:64px;text-align:center;font:600 22px var(--nli-mono);color:var(--cd)}.nlcd__step span{font:400 14px var(--nli-sans);color:#3E4C58}' +
      '.nlcd__flats{display:grid;grid-template-columns:repeat(auto-fill,minmax(26px,1fr));gap:4px;margin:12px 0 6px}.nlcd__flats i{display:block;height:30px;border:1.5px solid var(--cd);background:#fff}.nlcd__flats i.on{background:var(--cd)}' +
      '.nlcd__res{font:500 16px/24px var(--nli-sans);color:#12202A;margin:6px 0 0}.nlcd__res b{font-family:var(--nli-mono)}';
    document.head.appendChild(s);
  }

  /* ---------------- condo: which document answers my question ---------------- */
  NI.register('condo', {
    custom: function (root, d) {
      css();
      var D = d.condo, cur = null;
      root.innerHTML = ''; root.classList.add('nli'); root.setAttribute('dir', 'rtl');
      var panel = document.createElement('div'); panel.className = 'nli__panel nlcd';
      panel.innerHTML = '<p class="nli__kicker">תשריט · צו · תקנון</p><h2 class="nli__title">איזה מסמך עונה על השאלה שלכם</h2>' +
        '<p class="nli__lede">בוחרים שאלה, ורואים על התשריט לדוגמה איפה מסומנת התשובה, באיזה מסמך מחפשים אותה, ומה צריך להדליק נורה אדומה.</p>';
      var chips = document.createElement('div'); chips.className = 'nlcd__chips'; chips.setAttribute('role', 'group'); chips.setAttribute('aria-label', 'השאלה שלכם');
      D.chips.forEach(function (c) { var b = document.createElement('button'); b.type = 'button'; b.textContent = c.he; b.setAttribute('aria-pressed', 'false'); b.setAttribute('data-k', c.k); b.onclick = function () { show(c); if (window.innerWidth < 860) card.scrollIntoView({ block: 'nearest', behavior: 'smooth' }); }; chips.appendChild(b); });
      panel.appendChild(chips);
      var wrap = document.createElement('div'); wrap.className = 'nlcd__wrap';
      var sh = document.createElement('div'); sh.className = 'nlcd__sheet'; sh.innerHTML = sheet();
      var card = document.createElement('div'); card.className = 'nlcd__card'; card.setAttribute('aria-live', 'polite');
      var order = document.createElement('div'); order.className = 'nlcd__order';
      var L = D.links, fee = D.fee;
      order.innerHTML = '<h3>איך מזמינים את תיק הבית המשותף</h3><ol>' +
        '<li><b>מוצאים גוש וחלקה</b>באתר המרכז למיפוי ישראל, לפי הכתובת: <a href="' + L.parcel + '" target="_blank" rel="noopener">איתור גוש וחלקה</a>. באתר ההזמנה עצמו אין חיפוש לפי כתובת.</li>' +
        '<li><b>מזמינים באתר הממשלתי</b>לפי גוש וחלקה, משלמים בכרטיס אשראי, ומקבלים בדואר האלקטרוני תוך 24 שעות קישור להורדה של קובץ ZIP עם המסמכים החתומים. מזמינים את כל התיקים של הבניין: הרישום וכל התיקונים. <a href="' + L.service + '" target="_blank" rel="noopener">להזמנת מסמכי בית משותף ב־gov.il</a></li>' +
        '<li><b>לא מצאתם?</b>מחפשים לפי מספר התיק שמופיע בנסח הטאבו (״תיק יוצר״, ומ־1975 ״שטר יוצר״), או מתקשרים למוקד ‎*8653 בשלוחה 7.</li></ol>' +
        '<span class="nlcd__fee">' + fee.order + ' ₪ להזמנה · תעריף ' + fee.year + '</span><p class="nlcd__note">עיון בתיק הנייר בלשכת רישום המקרקעין, עם צילום: ' + fee.physical + ' ₪. התעריפים מתעדכנים ב־1 בינואר. ההזמנה נעשית באתר הממשלתי בלבד; אנחנו לא מזמינים בשמכם.</p>';
      wrap.appendChild(card); wrap.appendChild(sh); wrap.appendChild(order); panel.appendChild(wrap); root.appendChild(panel);  // phones: the answer first, then the drawing; wide screens: the drawing beside them
      function show(c) {
        cur = c;
        [].forEach.call(chips.children, function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-k') === c.k)); });
        sh.classList.add('is-focus');
        [].forEach.call(sh.querySelectorAll('g[data-k]'), function (g) { var ks = g.getAttribute('data-k').split(' '); g.classList.toggle('on', c.hi.some(function (h) { return ks.indexOf(h) > -1; })); });
        var more = c.more === 'roof' ? ' <a href="' + L.roof + '" target="_blank" rel="noopener">על זכויות הבנייה בגג ופסק דין בית הדר</a>' : c.more === 'amend' ? ' <a href="' + L.amend + '" target="_blank" rel="noopener">כך מתקנים צו בית משותף</a>' : '';
        card.innerHTML = '<h3>' + esc(c.he) + '</h3><dl><div><dt>באיזה מסמך ואיפה</dt><dd>' + esc(c.doc) + '</dd></div><div><dt>מה מחפשים</dt><dd>' + esc(c.look) + '</dd></div>' +
          '<div class="flag"><dt>דגל אדום</dt><dd>' + esc(c.flag) + more + '</dd></div><div><dd class="src">המקור: ' + esc(c.src) + '</dd></div></dl>';
      }
      var pre = root.getAttribute('data-nli-set'), first = D.chips[0];
      try { var S = pre ? JSON.parse(pre) : {}; if (S.preset) first = D.chips.filter(function (c) { return c.k === S.preset; })[0] || first; } catch (e) {}
      show(first);
    }
  });

  /* ---------------- condomaj: who must agree ---------------- */
  NI.register('condomaj', {
    custom: function (root, d) {
      css();
      var D = d.condo, n = 12, act = D.maj[2];
      root.innerHTML = ''; root.classList.add('nli'); root.setAttribute('dir', 'rtl');
      var panel = document.createElement('div'); panel.className = 'nli__panel nlcd';
      panel.innerHTML = '<p class="nli__kicker">מחשבון · רוב בבית משותף</p><h2 class="nli__title">כמה בעלי דירות צריכים להסכים</h2>' +
        '<p class="nli__lede">בוחרים את הפעולה ואת מספר הדירות בבניין, ורואים כמה דירות צריכות להסכים לפי חוק המקרקעין.</p>';
      var chips = document.createElement('div'); chips.className = 'nlcd__chips'; chips.setAttribute('role', 'group'); chips.setAttribute('aria-label', 'הפעולה');
      D.maj.forEach(function (m) { var b = document.createElement('button'); b.type = 'button'; b.textContent = m.he; b.setAttribute('data-k', m.k); b.onclick = function () { act = m; draw(); }; chips.appendChild(b); });
      var st = document.createElement('div'); st.className = 'nlcd__step';
      var minus = document.createElement('button'); minus.type = 'button'; minus.textContent = '−'; minus.setAttribute('aria-label', 'פחות דירות');
      var out = document.createElement('output'); out.setAttribute('aria-live', 'polite');
      var plus = document.createElement('button'); plus.type = 'button'; plus.textContent = '+'; plus.setAttribute('aria-label', 'יותר דירות');
      var lab = document.createElement('span'); lab.textContent = 'דירות בבניין';
      minus.onclick = function () { n = Math.max(2, n - 1); draw(); }; plus.onclick = function () { n = Math.min(80, n + 1); draw(); };
      st.appendChild(plus); st.appendChild(out); st.appendChild(minus); st.appendChild(lab);
      var pr = document.createElement('div'); pr.className = 'nlcd__chips'; pr.setAttribute('aria-label', 'גודל הבניין');
      [4, 8, 12, 24, 40].forEach(function (v) { var b = document.createElement('button'); b.type = 'button'; b.textContent = v + ' דירות'; b.setAttribute('data-n', v); b.onclick = function () { n = v; draw(); }; pr.appendChild(b); });
      var flats = document.createElement('div'); flats.className = 'nlcd__flats'; flats.setAttribute('aria-hidden', 'true');
      var res = document.createElement('p'); res.className = 'nlcd__res'; res.setAttribute('aria-live', 'polite');
      var note = document.createElement('p'); note.className = 'nlcd__note';
      panel.appendChild(chips); panel.appendChild(st); panel.appendChild(pr); panel.appendChild(flats); panel.appendChild(res); panel.appendChild(note); root.appendChild(panel);
      function draw() {
        [].forEach.call(chips.children, function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-k') === act.k)); });
        [].forEach.call(pr.children, function (b) { b.setAttribute('aria-pressed', String(+b.getAttribute('data-n') === n)); });
        out.textContent = n;
        var k = need(act, n), cells = '';
        for (var i = 0; i < n; i++) cells += '<i class="' + (i < k ? 'on' : '') + '"></i>';
        flats.innerHTML = cells;
        res.innerHTML = act.he + ' בבניין של ' + n + ' דירות: <b>' + k + '</b> מתוך ' + n + ' דירות צריכות להסכים. הכלל: ' + esc(act.rule) + '.';
        note.textContent = (act.basis === 'area' || act.basis === 'share' ? 'החישוב מניח דירות בגודל שווה. בפועל הרוב נמדד לפי שטח הרצפה או לפי החלק ברכוש המשותף שבצו הרישום. ' : act.basis === 'flats' && act.k === 'extend' ? 'ובנוסף, לדירות שמסכימות צריכים להיות שני שלישים מהרכוש המשותף. ' : '') +
          'המקור: ' + act.src + '. העברת הצמדה קיימת מדירה לדירה באותו בניין אינה דורשת את הסכמת השכנים, ונעשית בתיקון צו הבית המשותף.';
      }
      draw();
    }
  });
})();
