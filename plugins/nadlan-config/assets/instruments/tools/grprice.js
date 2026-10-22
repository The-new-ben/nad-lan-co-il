/* NadLan Instruments · the Greece price-list family (HAD-592, Ben 22.10.2026: "the most comprehensive Greece price list ...
   infographics, tools, something new, complex but everything in one tap"). One file (registry 'file' => 'grprice'):
     grmap    a map of Greece (Natural Earth outline) with every priced place as a dot coloured by EUR per m²; filter chips; one
              tap opens the place's card (price in € and ₪, a 70 m² flat, rent, yield, year change, golden-visa tier, border
              permit, Airbnb freeze); up to three places side by side in the compare tray; the full table under the map.
     grbudget what a budget buys in every place after the buying costs (3.09% tax, notary, cadastre, lawyer, agent): m² per place,
              sorted, in € or ₪, with golden-visa eligibility at that budget.
     grisrael "my Israeli flat in Greece": the official median of an Israeli city by rooms (value.json, Tax Authority deals) in
              euros at the Bank of Israel rate, and how many m² it buys in each Greek place after buying costs.
   Data: greece-prices.json (built from docs/research/2026-10-22-greece-prices/prices.json, every figure with its source and
   period), greece-map.json (Natural Earth, public domain), boi-fx.json, value.json. Pure logic in NLGP. */
(function () {
  'use strict';
  var COST = 0.0826;  // buying costs with an agent, as a share of the price (3.09% tax + notary + cadastre + 1% lawyer + 2% agent, with VAT): facts.json worked examples
  function netBudget(b) { return b / (1 + COST); }
  function m2For(b, eurM2) { return eurM2 ? netBudget(b) / eurM2 : 0; }
  function band(v, cuts) { for (var i = 0; i < cuts.length; i++) if (v <= cuts[i]) return i; return cuts.length; }
  window.NLGP = { netBudget: netBudget, m2For: m2For, COST: COST };
  if (!window.NadLanInstruments) return;
  var NI = window.NadLanInstruments, F = NI.fmt, esc = NI.esc;
  var CUTS = [2000, 2600, 3200, 4200], COL = ['#9CC3D1', '#4E93AC', '#2F6F86', '#1F4B5C', '#C42550'];
  var TYPE = { city: 'עיר', area: 'אזור', island: 'אי', region: 'מחוז' };
  function fx(d) { return d.fx.fx.EUR.rate; }
  function ils(e, d) { return '₪' + F.num(Math.round(e * fx(d))); }
  function places(d) { return d.gp.places.filter(function (p) { return p.m2 > 0 && p.z !== 'none'; }); }
  function gvText(g) { return g === 800 ? 'גולדן ויזה מ־€800,000' : g === 400 ? 'גולדן ויזה מ־€400,000' : g === 0 ? 'גולדן ויזה: 800 או 400 אלף, לפי המקום' : 'גולדן ויזה: לבדיקה (סף 3,100 תושבים)'; }
  function gvShort(g) { return g === 800 ? '€800,000' : g === 400 ? '€400,000' : g === 0 ? 'לפי המקום' : 'לבדיקה'; }
  function css() {
    if (document.getElementById('nlgp-css')) return;
    var s = document.createElement('style'); s.id = 'nlgp-css';
    s.textContent = '.nlgp{position:relative}.nlgp__map{position:relative;border:1px solid var(--nli-line);border-radius:6px;background:#E6F0F3;overflow:hidden}' +
      '.nlgp__map svg{display:block;width:100%;height:auto;direction:ltr}.nlgp__gr{fill:#fff;stroke:#1F4B5C;stroke-width:.7}.nlgp__nb{fill:#D3DCE2}' +
      '.nlgp__dot{cursor:pointer;stroke:#fff;stroke-width:1.4}.nlgp__dot:hover,.nlgp__dot[aria-pressed="true"]{stroke:#12202A;stroke-width:2.2}' +
      '.nlgp__dot.is-off{opacity:.12;pointer-events:none}.nlgp__lbl{font:600 11px "IBM Plex Sans Hebrew",sans-serif;fill:#12202A;paint-order:stroke;stroke:#fff;stroke-width:3px;pointer-events:none}' +
      '.nlgp__chips{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 10px}.nlgp__chips button{font:500 13px/18px var(--nli-sans);min-height:40px;padding:8px 12px;border:1px solid var(--nli-line);border-radius:999px;background:#fff;color:var(--nli-ink2);cursor:pointer;margin:0}' +
      '.nlgp__chips button[aria-pressed="true"]{background:var(--nli-sea);border-color:var(--nli-sea);color:#fff}' +
      '.nlgp__legend{display:flex;flex-wrap:wrap;gap:10px;font:400 12px/16px var(--nli-sans);color:var(--nli-mute);margin:8px 0}.nlgp__legend i{display:inline-block;width:12px;height:12px;border-radius:50%;margin-inline-end:4px;vertical-align:-2px}' +
      '.nlgp__card{border:1px solid var(--nli-line);border-radius:6px;background:#fff;padding:14px;margin:10px 0}.nlgp__card h3{margin:0 0 4px;font:700 22px/26px var(--nli-sans);color:var(--nli-ink)}' +
      '.nlgp__card .k{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:8px;margin:10px 0}.nlgp__card .k div{border-top:1px solid var(--nli-line);padding-top:6px}' +
      '.nlgp__card .k span{display:block;font:400 12px/16px var(--nli-sans);color:var(--nli-mute)}.nlgp__card .k b{font:600 17px/22px var(--nli-mono);color:var(--nli-ink);direction:ltr;unicode-bidi:plaintext}' +
      '.nlgp__flags{display:flex;flex-wrap:wrap;gap:6px}.nlgp__flags span{font:500 12px/16px var(--nli-sans);border:1px solid var(--nli-line);border-radius:2px;padding:2px 6px}.nlgp__flags .red{border-color:#C42550;color:#C42550}' +
      '.nlgp__cmp{display:flex;gap:6px;flex-wrap:wrap;align-items:center;margin:8px 0}.nlgp__cmp button{font:500 13px var(--nli-sans);min-height:40px;padding:8px 12px;border:1px solid var(--nli-sea);border-radius:4px;background:#fff;color:var(--nli-sea);cursor:pointer;margin:0}' +
      '.nlgp__src{font:400 12px/16px var(--nli-mono);color:var(--nli-mute);margin:6px 0 0}' +
      '.nlgp .l{display:none}@media (max-width:600px){.nlgp .l{display:inline;font-weight:600;color:var(--nli-mute);font-family:var(--nli-sans)}.nlgp table tr{padding:6px 0}.nlgp table td,.nlgp table th{padding:2px 8px}}' +
      '.nlgp__more{display:block;width:100%;margin:8px 0 0;min-height:44px;border:1px solid var(--nli-sea);border-radius:4px;background:#fff;color:var(--nli-sea);font:600 14px var(--nli-sans);cursor:pointer}';
    document.head.appendChild(s);
  }

  /* ---------------- grmap (custom surface) ---------------- */
  NI.register('grmap', {
    custom: function (root, d) {
      css();
      var M = d.gmap, P = places(d), pr = M.proj, sel = null, cmp = [], filt = 'all', showAll = false, lastW = 0;
      var X = function (lng) { return (lng - pr.lon0) * pr.cos * pr.k; }, Y = function (lat) { return (pr.lat1 - lat) * pr.k; };
      var FIL = [['all', 'כל יוון'], ['attica', 'אתונה ואטיקה, מקרוב'], ['thess', 'סלוניקי, מקרוב'], ['island', 'איים'], ['main', 'יבשה וערים'], ['gv400', 'גולדן ויזה ב־400 אלף'], ['yield5', 'תשואה מעל 5%'], ['open', 'Airbnb פתוח'], ['cheap', 'עד €2,000 למ״ר']];
      function pass(p) {
        if (filt === 'attica') return p.z === 'ath' || p.id === 'ath-centre'; if (filt === 'thess') return p.z === 'thess' || p.id === 'thess-municipality';
        if (p.z !== 'map') return false;
        if (filt === 'island') return p.t === 'island'; if (filt === 'main') return p.t !== 'island';
        if (filt === 'gv400') return p.gv === 400; if (filt === 'yield5') return p.y >= 0.05; if (filt === 'open') return !p.sf; if (filt === 'cheap') return p.m2 <= 2000; return true;
      }
      root.innerHTML = ''; root.classList.add('nli'); root.setAttribute('dir', 'rtl');
      var panel = document.createElement('div'); panel.className = 'nli__panel nlgp';
      panel.innerHTML = '<p class="nli__kicker">מפה · מחירון יוון</p><h2 class="nli__title">מחירי הנדל״ן ביוון על המפה</h2>' +
        '<p class="nli__lede">כל נקודה היא מקום שיש לו מחיר מבוקש מפורסם. לוחצים על נקודה או על שורה בטבלה ומקבלים את כל המספרים, ואפשר להוסיף עד שלושה מקומות להשוואה.</p>';
      var chips = document.createElement('div'); chips.className = 'nlgp__chips'; chips.setAttribute('role', 'group'); chips.setAttribute('aria-label', 'סינון');
      FIL.forEach(function (f) { var b = document.createElement('button'); b.type = 'button'; b.textContent = f[1]; b.setAttribute('aria-pressed', String(f[0] === filt)); b.onclick = function () { filt = f[0]; showAll = false; [].forEach.call(chips.children, function (x) { x.setAttribute('aria-pressed', String(x === b)); }); draw(); }; chips.appendChild(b); });
      panel.appendChild(chips);
      var map = document.createElement('div'); map.className = 'nlgp__map';
      var svg = '<svg viewBox="0 0 ' + M.vb[0] + ' ' + M.vb[1] + '" role="img" aria-label="מפת מחירי הנדל״ן ביוון"><path class="nlgp__nb" d="' + M.nb + '"/><path class="nlgp__gr" d="' + M.gr + '"/>';
      P.slice().sort(function (a, b) { return a.m2 - b.m2; }).forEach(function (p) { var r = p.t === 'region' ? 8 : 6;
        svg += '<circle class="nlgp__dot" data-id="' + esc(p.id) + '" data-r="' + r + '" cx="' + X(p.lng).toFixed(1) + '" cy="' + Y(p.lat).toFixed(1) + '" r="' + r + '" fill="' + COL[band(p.m2, CUTS)] + '" tabindex="0" role="button" aria-label="' + esc(p.he + ', €' + F.num(p.m2) + ' למ״ר') + '"/>'; });
      svg += '<g class="nlgp__labels"></g></svg>';
      map.innerHTML = svg; panel.appendChild(map); var svgEl = map.querySelector('svg');
      var legend = document.createElement('div'); legend.className = 'nlgp__legend';
      legend.innerHTML = ['עד €2,000', '€2,000 עד €2,600', '€2,600 עד €3,200', '€3,200 עד €4,200', 'מעל €4,200'].map(function (t, i) { return '<span><i style="background:' + COL[i] + '"></i>' + t + ' למ״ר</span>'; }).join('');
      panel.appendChild(legend);
      var card = document.createElement('div'); card.className = 'nlgp__card'; card.setAttribute('aria-live', 'polite'); panel.appendChild(card);
      var tray = document.createElement('div'); panel.appendChild(tray);
      var tw = document.createElement('div'); tw.className = 'nli__tw'; panel.appendChild(tw);
      var src = document.createElement('p'); src.className = 'nlgp__src'; src.textContent = 'מקורות: ' + d.gp.sources_line + ' · מפה: Natural Earth · שער: בנק ישראל, ' + F.date(d.fx.fx.EUR.date); panel.appendChild(src);
      root.appendChild(panel);
      function flags(p) { return '<div class="nlgp__flags"><span>' + gvText(p.gv) + '</span>' + (p.bp ? '<span class="red">אזור גבול: היתר מראש לישראלים</span>' : '') + (p.sf ? '<span class="red">Airbnb חדש מוקפא</span>' : '') + '</div>'; }
      function show(p) {
        sel = p; [].forEach.call(map.querySelectorAll('.nlgp__dot'), function (c) { c.setAttribute('aria-pressed', String(c.getAttribute('data-id') === p.id)); });
        var apt = p.m2 * 70;
        card.innerHTML = '<h3>' + esc(p.he) + '</h3><p style="margin:0;color:var(--nli-mute);font-size:13px">' + esc(TYPE[p.t] || '') + (p.rh ? ' · ' + esc(p.rh) : '') + ' · ' + esc(p.per) + ' · ' + esc(p.src) + '</p>' +
          '<div class="k"><div><span>מחיר מבוקש למ״ר</span><b>€' + F.num(p.m2) + '</b></div><div><span>בשקלים למ״ר</span><b>' + ils(p.m2, d) + '</b></div>' +
          '<div><span>דירת 70 מ״ר</span><b>€' + F.num(apt) + '</b></div><div><span>דירת 70 מ״ר בשקלים</span><b>' + ils(apt, d) + '</b></div>' +
          (p.yoy != null ? '<div><span>שינוי בשנה</span><b>' + (p.yoy >= 0 ? '+' : '') + F.num(100 * p.yoy, 1) + '%</b></div>' : '') +
          (p.rent ? '<div><span>שכירות מבוקשת למ״ר לחודש</span><b>€' + F.num(p.rent, 1) + '</b></div>' : '') +
          (p.y ? '<div><span>תשואה ברוטו</span><b>' + F.num(100 * p.y, 1) + '%</b></div>' : '') + '</div>' + flags(p) +
          (p.note ? '<p style="margin:8px 0 0;font-size:13px;color:var(--nli-mute)">' + esc(p.note) + '</p>' : '');
        var add = document.createElement('div'); add.className = 'nlgp__cmp';
        var b = document.createElement('button'); b.type = 'button'; b.textContent = cmp.indexOf(p) > -1 ? 'כבר בהשוואה' : (cmp.length >= 3 ? 'ההשוואה מלאה: הסירו מקום' : '+ להשוואה');
        b.onclick = function () { if (cmp.indexOf(p) < 0 && cmp.length < 3) { cmp.push(p); show(p); drawTray(); } }; add.appendChild(b); card.appendChild(add);
      }
      function drawTray() {
        if (!cmp.length) { tray.innerHTML = ''; return; }
        var rows = [['מחיר למ״ר', function (p) { return '€' + F.num(p.m2); }], ['בשקלים', function (p) { return ils(p.m2, d); }], ['דירת 70 מ״ר', function (p) { return '€' + F.num(p.m2 * 70); }],
          ['שינוי בשנה', function (p) { return p.yoy != null ? F.num(100 * p.yoy, 1) + '%' : 'לא פורסם'; }], ['שכירות למ״ר', function (p) { return p.rent ? '€' + F.num(p.rent, 1) : 'לא פורסם'; }],
          ['תשואה ברוטו', function (p) { return p.y ? F.num(100 * p.y, 1) + '%' : 'לא פורסם'; }], ['גולדן ויזה', function (p) { return gvShort(p.gv); }],
          ['אזור גבול', function (p) { return p.bp ? 'כן' : 'לא'; }], ['Airbnb חדש', function (p) { return p.sf ? 'מוקפא' : 'פתוח'; }]];
        tray.innerHTML = '<h3 style="margin:14px 0 6px;font:600 17px var(--nli-sans);color:var(--nli-ink)">השוואה</h3><div class="nli__tw"><table><thead><tr><th></th>' + cmp.map(function (p, i) { return '<th>' + esc(p.he) + ' <button type="button" data-i="' + i + '" aria-label="הסרה" style="border:0;background:none;color:#C42550;cursor:pointer;font-size:16px">×</button></th>'; }).join('') + '</tr></thead><tbody>' +
          rows.map(function (r) { return '<tr><th>' + r[0] + '</th>' + cmp.map(function (p) { return '<td class="n"><span class="l">' + esc(p.he) + ': </span>' + r[1](p) + '</td>'; }).join('') + '</tr>'; }).join('') + '</tbody></table></div>';
        [].forEach.call(tray.querySelectorAll('button[data-i]'), function (b) { b.onclick = function () { cmp.splice(+b.getAttribute('data-i'), 1); drawTray(); if (sel) show(sel); }; });
      }
      function draw() {
        var vis = P.filter(pass);
        [].forEach.call(map.querySelectorAll('.nlgp__dot'), function (c) { var p = P.filter(function (x) { return x.id === c.getAttribute('data-id'); })[0]; c.classList.toggle('is-off', !pass(p)); });
        var g = map.querySelector('.nlgp__labels'); g.innerHTML = '';
        var zoom = filt === 'attica' || filt === 'thess', fs = 1;
        if (zoom && vis.length) { var xs = vis.map(function (p) { return X(p.lng); }), ys = vis.map(function (p) { return Y(p.lat); }); var x0 = Math.min.apply(0, xs) - 12, x1 = Math.max.apply(0, xs) + 12, y0 = Math.min.apply(0, ys) - 12, y1 = Math.max.apply(0, ys) + 12;
          var asp = map.clientWidth && map.clientWidth < 600 ? 1.1 : M.vb[1] / M.vb[0];  // a phone gets a squarer zoom, so the dots and names have room
          var w = Math.max(x1 - x0, (y1 - y0) / asp), h = w * asp, cx = (x0 + x1) / 2, cy = (y0 + y1) / 2; svgEl.setAttribute('viewBox', (cx - w / 2).toFixed(1) + ' ' + (cy - h / 2).toFixed(1) + ' ' + w.toFixed(1) + ' ' + h.toFixed(1)); fs = w; }
        else { svgEl.setAttribute('viewBox', '0 0 ' + M.vb[0] + ' ' + M.vb[1]); fs = M.vb[0]; }
        var cw = map.clientWidth || M.vb[0]; fs = fs / cw; lastW = cw;  // map units per screen pixel: dots and names keep their size in pixels on every screen and zoom
        var dr = cw < 600 ? 0.85 : 1.05;
        [].forEach.call(map.querySelectorAll('.nlgp__dot'), function (c) { c.setAttribute('r', ((c.getAttribute('data-r') || 6.5) * dr * fs).toFixed(2)); c.style.strokeWidth = (1.4 * fs).toFixed(2); });
        map.querySelector('.nlgp__gr').style.strokeWidth = (0.7 * fs).toFixed(2);
        var boxes = [];  // a name is printed only where it does not cover another one (dense centres); a tap still opens any place
        vis.filter(function (p) { return zoom ? true : p.lb; }).sort(function (a, b) { return (b.lb ? 1 : 0) - (a.lb ? 1 : 0) || b.m2 - a.m2; }).forEach(function (p) {
          var txt = zoom ? p.he.split(' (')[0] : p.lb, bx = { x: X(p.lng) + 9 * fs, y: Y(p.lat) - 9 * fs, w: txt.length * 6.6 * fs, h: 14 * fs };
          if (boxes.some(function (o) { return bx.x < o.x + o.w && o.x < bx.x + bx.w && bx.y < o.y + o.h && o.y < bx.y + bx.h; })) return; boxes.push(bx);
          var t = document.createElementNS('http://www.w3.org/2000/svg', 'text'); t.setAttribute('class', 'nlgp__lbl'); t.setAttribute('x', (X(p.lng) + 9 * fs).toFixed(1)); t.setAttribute('y', (Y(p.lat) + 4 * fs).toFixed(1)); t.style.fontSize = (11.5 * fs).toFixed(2) + 'px'; t.style.strokeWidth = (3 * fs).toFixed(2) + 'px'; t.textContent = txt; g.appendChild(t); });
        var rows = vis.slice().sort(function (a, b) { return b.m2 - a.m2; }), shown = showAll ? rows : rows.slice(0, 12);
        tw.innerHTML = '<table><caption style="text-align:start;padding:8px 0;font-weight:600">' + rows.length + ' מקומות, מהיקר לזול</caption><thead><tr><th>מקום</th><th>€ למ״ר</th><th>₪ למ״ר</th><th>שנה</th><th>תשואה</th></tr></thead><tbody>' +
          shown.map(function (p) { return '<tr data-id="' + esc(p.id) + '" style="cursor:pointer"><td><b>' + esc(p.he) + '</b></td><td class="n"><span class="l">€ למ״ר: </span>€' + F.num(p.m2) + '</td><td class="n"><span class="l">₪ למ״ר: </span>' + ils(p.m2, d) + '</td><td class="n">' + (p.yoy != null ? '<span class="l">שנה: </span>' + F.num(100 * p.yoy, 1) + '%' : '') + '</td><td class="n">' + (p.y ? '<span class="l">תשואה: </span>' + F.num(100 * p.y, 1) + '%' : '') + '</td></tr>'; }).join('') + '</tbody></table>';
        if (rows.length > 12) { var more = document.createElement('button'); more.type = 'button'; more.className = 'nlgp__more'; more.textContent = showAll ? 'פחות שורות' : 'לכל ' + rows.length + ' המקומות';
          more.onclick = function () { showAll = !showAll; draw(); }; tw.appendChild(more); }
        [].forEach.call(tw.querySelectorAll('tr[data-id]'), function (tr) { tr.onclick = function () { show(P.filter(function (x) { return x.id === tr.getAttribute('data-id'); })[0]); card.scrollIntoView({ block: 'nearest', behavior: 'smooth' }); }; });
        if (!sel || !pass(sel)) show(rows[0] || P[0]);
      }
      [].forEach.call(map.querySelectorAll('.nlgp__dot'), function (c) { var go = function () { show(P.filter(function (x) { return x.id === c.getAttribute('data-id'); })[0]); }; c.addEventListener('click', go); c.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); } }); });
      var pre = root.getAttribute('data-nli-set'); try { var S = pre ? JSON.parse(pre) : {}; if (S.region) filt = S.region; } catch (e) {}
      [].forEach.call(chips.children, function (x, i) { x.setAttribute('aria-pressed', String(FIL[i][0] === filt)); });
      draw();
      var rz = 0; window.addEventListener('resize', function () { if (rz) return; rz = requestAnimationFrame(function () { rz = 0; if (map.clientWidth && map.clientWidth !== lastW) draw(); }); });
    }
  });

  /* ---------------- grbudget ---------------- */
  NI.register('grbudget', {
    kicker: 'מחשבון · מה מקבלים בתקציב',
    title: 'כמה מטרים מקבלים ביוון בכל תקציב',
    lede: 'תקציב אחד, כל המקומות: המחשבון מוריד את עלויות הקנייה (כ־8.3% עם מתווך), מחלק במחיר המבוקש למ״ר בכל מקום, וממיין מהגדול לקטן.',
    strip: function (d) { return [{ label: 'מקומות עם מחיר', value: F.num(places(d).length) }, { label: 'עלויות קנייה, עם מתווך', value: F.num(100 * COST, 1) + '%' }, { label: 'יורו בשקלים', value: '₪' + F.num(fx(d), 3) }]; },
    presets: [{ key: 'b100', label: '€100,000', sub: 'דירה קטנה', set: { budget: 100000, cur: 'eur', where: 'all' } }, { key: 'b150', label: '€150,000', sub: 'דירה להשקעה', set: { budget: 150000, cur: 'eur', where: 'all' } },
      { key: 'b250', label: '€250,000', sub: 'דירה משפחתית', set: { budget: 250000, cur: 'eur', where: 'all' } }, { key: 'b400', label: '€400,000', sub: 'גולדן ויזה מחוץ לאטיקה', set: { budget: 400000, cur: 'eur', where: 'all' } },
      { key: 'b800', label: '€800,000', sub: 'גולדן ויזה בכל מקום', set: { budget: 800000, cur: 'eur', where: 'all' } }, { key: 'ils1m', label: '₪1,000,000', sub: 'בשקלים', set: { budget: 1000000, cur: 'ils', where: 'all' } },
      { key: 'isl', label: '€200,000 באיים', sub: 'רק איים', set: { budget: 200000, cur: 'eur', where: 'island' } }],
    defaults: function () { return { budget: 150000, cur: 'eur', where: 'all' }; },
    fields: [
      { id: 'budget', label: 'התקציב, כולל עלויות הקנייה', type: 'money' },
      { id: 'cur', label: 'מטבע', type: 'segmented', options: [{ value: 'eur', label: 'יורו' }, { value: 'ils', label: 'שקלים' }] },
      { id: 'where', label: 'איפה', type: 'segmented', options: [{ value: 'all', label: 'בכל מקום' }, { value: 'island', label: 'איים' }, { value: 'main', label: 'יבשה וערים' }] }
    ],
    compute: function (v, d) {
      if (!(v.budget >= 10000)) return { error: { field: 'budget', msg: 'הקלידו תקציב.' } };
      var eur = v.cur === 'ils' ? v.budget / fx(d) : v.budget;
      var L = places(d).filter(function (p) { return v.where === 'all' || (v.where === 'island' ? p.t === 'island' : p.t !== 'island'); })
        .map(function (p) { return { p: p, m: m2For(eur, p.m2) }; }).sort(function (a, b) { return b.m - a.m; });
      if (!L.length) return { error: { field: 'where', msg: 'אין מקומות בסינון הזה.' } };
      var top = L[0], low = L[L.length - 1], net = netBudget(eur);
      var gv = eur >= 800000 ? 'התקציב עובר את סף הגולדן ויזה בכל יוון (€800,000), בנכס אחד של 120 מ״ר.' : eur >= 400000 ? 'התקציב עובר את סף הגולדן ויזה מחוץ לאטיקה, לסלוניקי, למיקונוס, לסנטוריני ולאיים הגדולים (€400,000), בנכס אחד של 120 מ״ר.' : 'מתחת לסף הגולדן ויזה (€400,000 לפחות).';
      return {
        answer: { label: 'הכי הרבה מטרים: ' + top.p.he, value: F.num(top.m) + ' מ״ר', tone: 'survey', sub: 'לעומת ' + F.num(low.m) + ' מ״ר ב' + low.p.he + ' · נשאר לדירה €' + F.num(net) + ' (' + ils(net, d) + ')' },
        lines: L.slice(0, 5).map(function (x) { return { label: x.p.he + ' · €' + F.num(x.p.m2) + ' למ״ר', value: F.num(x.m) + ' מ״ר' }; }),
        note: gv + ' המחירים הם מחירים מבוקשים; בפועל נסגר לרוב פחות.',
        table: { title: 'כל ' + L.length + ' המקומות', head: ['מקום', '€ למ״ר', 'מ״ר בתקציב', 'גולדן ויזה מ־'], num: [1, 2], rows: L.map(function (x) { return [x.p.he, '€' + F.num(x.p.m2), F.num(x.m), gvShort(x.p.gv)]; }) },
        formula: 'מ״ר = התקציב ÷ (1 + ' + F.num(100 * COST, 2) + '% עלויות קנייה) ÷ המחיר המבוקש למ״ר במקום.',
        sources: [{ label: d.gp.sources_line, url: '' }, { label: 'שער היציג של בנק ישראל, ' + F.date(d.fx.fx.EUR.date), url: d.fx.url }],
        text: 'בתקציב של ' + (v.cur === 'ils' ? '₪' : '€') + F.num(v.budget) + ' ביוון: ' + F.num(top.m) + ' מ״ר ב' + top.p.he + ', ' + F.num(low.m) + ' מ״ר ב' + low.p.he + '.'
      };
    }
  });

  /* ---------------- grisrael ---------------- */
  function ilCities(d) { return Object.keys(d.value.cities).filter(function (c) { var x = d.value.cities[c]; return x.r3 || x.r4 || x.r5; }).sort(); }
  NI.register('grisrael', {
    kicker: 'השוואה · ישראל מול יוון',
    title: 'כמה מטרים שווה הדירה שלכם בישראל, ביוון',
    lede: 'בוחרים עיר בישראל ומספר חדרים: המחשבון לוקח את המחיר החציוני הרשמי של העסקאות בעיר (רשות המסים), ממיר ליורו לפי בנק ישראל, מוריד את עלויות הקנייה ביוון, ומראה כמה מ״ר הוא קונה בכל מקום ביוון.',
    presets: [{ key: 'tlv4', label: '4 חדרים בתל אביב', sub: 'החציון הרשמי', set: { city: 'תל אביב יפו', rooms: 4 } }, { key: 'rg3', label: '3 חדרים ברמת גן', sub: 'החציון הרשמי', set: { city: 'רמת גן', rooms: 3 } },
      { key: 'hfa4', label: '4 חדרים בחיפה', sub: 'החציון הרשמי', set: { city: 'חיפה', rooms: 4 } }, { key: 'bs5', label: '5 חדרים בבאר שבע', sub: 'החציון הרשמי', set: { city: 'באר שבע', rooms: 5 } }],
    defaults: function () { return { city: 'תל אביב יפו', rooms: 4 }; },
    fields: [
      { id: 'city', label: 'העיר בישראל', type: 'select', optionsFrom: function (v, d) { return ilCities(d).map(function (c) { return { value: c, label: c }; }); } },
      { id: 'rooms', label: 'חדרים', type: 'segmented', options: [{ value: 3, label: '3' }, { value: 4, label: '4' }, { value: 5, label: '5' }] }
    ],
    compute: function (v, d) {
      var c = d.value.cities[v.city]; if (!c) return { error: { field: 'city', msg: 'בחרו עיר.' } };
      var med = +c['r' + v.rooms]; if (!med) return { error: { field: 'rooms', msg: 'אין חציון רשמי לדירת ' + v.rooms + ' חדרים בעיר הזאת.' } };
      var eur = med / fx(d), L = places(d).map(function (p) { return { p: p, m: m2For(eur, p.m2) }; }).sort(function (a, b) { return b.m - a.m; });
      var ath = L.filter(function (x) { return x.p.id === 'ath-centre'; })[0];
      return {
        answer: { label: 'דירת ' + v.rooms + ' חדרים ב' + v.city + ' (₪' + F.num(med) + ')', value: '€' + F.num(eur), tone: 'survey', sub: (ath ? 'קונה כ־' + F.num(ath.m) + ' מ״ר במרכז אתונה · ' : '') + F.num(L[0].m) + ' מ״ר ב' + L[0].p.he },
        lines: L.slice(0, 5).map(function (x) { return { label: x.p.he, value: F.num(x.m) + ' מ״ר' }; }),
        note: 'החציון של ' + v.city + ' לפי רשות המסים, רבעון ' + esc(c['q' + v.rooms] || c.q || '') + '. אחרי עלויות קנייה של כ־' + F.num(100 * COST, 1) + '% ביוון. המחירים ביוון מבוקשים, ובפועל נסגר לרוב פחות.',
        table: { title: 'מה הדירה שלכם קונה בכל מקום ביוון', head: ['מקום', '€ למ״ר', 'מ״ר'], num: [1, 2], rows: L.map(function (x) { return [x.p.he, '€' + F.num(x.p.m2), F.num(x.m)]; }) },
        formula: 'מ״ר ביוון = החציון בישראל ÷ שער היורו ÷ (1 + עלויות הקנייה) ÷ המחיר המבוקש למ״ר.',
        sources: [{ label: 'רשות המסים, עסקאות הנדל״ן (data.nadlan.gov.il)', url: 'https://www.nadlan.gov.il/' }, { label: d.gp.sources_line, url: '' }, { label: 'שער היציג של בנק ישראל, ' + F.date(d.fx.fx.EUR.date), url: d.fx.url }],
        text: 'דירת ' + v.rooms + ' חדרים ב' + v.city + ' (₪' + F.num(med) + ') = €' + F.num(eur) + ', כ־' + F.num(L[0].m) + ' מ״ר ב' + L[0].p.he + '.'
      };
    }
  });
})();
