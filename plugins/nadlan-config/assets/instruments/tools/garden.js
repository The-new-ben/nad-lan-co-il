/* NadLan Instruments · garden v1 (HAD-669 R12d, Ben 3.11.2026: "the best garden-apartment page in the world, with tools, prices
   and data"; Claude Design v108.0 GardenHub). Four tools of one family ('file' => 'garden' in inc/garden-tools.php), on the Tax
   Authority closed deals of type 'דירת גן' in Tel Aviv-Yafo (data/garden.json, tools/instruments/build_garden_data.py; the type
   stops at 28.8.2024, so every figure says so):
   gdnworth  what a garden flat is worth: neighbourhood, rooms, built m2 -> the neighbourhood median per m2 (5+ deals, 2015-2024),
             or the citywide median by rooms (2020-2024), said as such;
   gdnmap    every garden deal on a tilted map (MapLibre GL + OpenFreeMap, the soil and asbestos stack), coloured by price per m2,
             labelled by neighbourhood with its median or its deal count;
   gdnstreet the deals on a street;
   gdnground the ground floor against the whole building, per neighbourhood (labelled ground floor, not garden). Hebrew only. */
(function () {
  'use strict';
  if (!window.NadLanInstruments) return;
  var NLI = window.NadLanInstruments, F = NLI.fmt, esc = NLI.esc;
  function f(s, o) { return String(s).replace(/\{(\w+)\}/g, function (m, k) { return o[k] != null ? o[k] : m; }); }
  function rb(r) { return !r ? '' : r < 2.5 ? '1-2' : r < 3.5 ? '3' : r < 4.5 ? '4' : '5+'; }
  function ils(n) { return F.ils(n); }
  function mln(n) { return n >= 1e6 ? F.num(n / 1e6, n % 1e5 ? 2 : 1).replace(/\.?0+$/, '') + ' מיליון ₪' : ils(n); }
  var END = 'עד אוגוסט 2024', SRC = 'לפי עסקאות שדווחו לרשות המסים, ' + 'עד 28.8.2024.';

  /* ---------------------------------------------------------------- gdnworth */
  NLI.register('gdnworth', {
    kicker: 'מחשבון · דירת גן',
    title: 'מה שווה דירת גן בשכונה שלכם',
    lede: 'בוחרים שכונה, חדרים ושטח בנוי, ומקבלים הערכה לפי עסקאות דירות גן שנסגרו בתל אביב. לא לפי מחירים מבוקשים.',
    defaults: function () { return { hood: 'לב תל-אביב', rooms: '3', area: 72 }; },
    fields: [
      { id: 'hood', label: 'השכונה', type: 'select', optionsFrom: function (v, data) {
        var h = data.garden.hoods, k = Object.keys(h).sort(function (a, b) { return (h[b].ppsqm ? 1 : 0) - (h[a].ppsqm ? 1 : 0) || h[b].n - h[a].n; });
        return k.map(function (n) { return { value: n, label: n + (h[n].ppsqm ? '' : ' (מעט עסקאות)') }; }).concat([{ value: '', label: 'שכונה אחרת או כל העיר' }]); } },
      { id: 'rooms', label: 'החדרים', type: 'segmented', options: [{ value: '1-2', label: '1-2' }, { value: '3', label: '3' }, { value: '4', label: '4' }, { value: '5+', label: '5+' }] },
      { id: 'area', label: 'השטח הבנוי', type: 'number', unit: 'מ״ר', help: 'השטח הבנוי של הדירה, בלי הגינה: גודל הגינה לא רשום בדיווח לרשות המסים.' }
    ],
    compute: function (v, data) {
      var d = data.garden, h = d.hoods[v.hood], r = d.rooms[v.rooms];
      if (!(v.area >= 20 && v.area <= 600)) return { error: { field: 'area', msg: 'הקלידו שטח בנוי בין 20 ל־600 מ״ר.' } };
      var byHood = !!(h && h.ppsqm), pp = byHood ? h.ppsqm : (r && r.ppsqm), val = Math.round(v.area * pp / 1000) * 1000;
      var out = {
        answer: { label: byHood ? 'לפי עסקאות דירות הגן בשכונה, 2015 עד 2024' : 'לפי החציון העירוני של דירות גן ' + v.rooms + ' חדרים, 2020 עד 2024', value: ils(val), tone: 'ink',
          sub: F.num(v.area) + ' מ״ר × ' + ils(pp) + ' למ״ר' },
        lines: [{ label: byHood ? 'החציון למ״ר בשכונה' : 'החציון העירוני למ״ר', value: ils(pp) }],
        note: (byHood ? '' : (v.hood ? 'בשכונה ' + v.hood + ' יש פחות מ־5 עסקאות דירות גן, ולכן ההערכה לפי כל העיר. ' : '')) + 'הערכה לפי עסקאות שנסגרו, לא שמאות ולא הצעת מחיר. דירה במצב מיוחד, גינה גדולה במיוחד או ממ״ד משנים את המחיר, והנתונים ' + END + '.',
        formula: 'הערכה = השטח הבנוי × המחיר החציוני למ״ר. חציון מוצג רק כשיש 5 עסקאות ומעלה.',
        sources: [{ label: 'רשות המסים, עסקאות נדל״ן (מאגר פתוח)', url: 'https://www.odata.org.il/dataset/84f2bc2d-87a0-474e-a3ea-63d7bb9b5447' }],
        text: 'הערכת שווי לדירת גן ' + v.rooms + ' חדרים, ' + F.num(v.area) + ' מ״ר' + (v.hood ? ' ב' + v.hood : '') + ': ' + ils(val) + ' (לפי עסקאות שדווחו לרשות המסים, ' + END + ').'
      };
      if (h) out.lines.push({ label: 'עסקאות דירות גן בשכונה (כל השנים)', value: F.num(h.n) });
      if (r) out.lines.push({ label: 'דירות גן ' + v.rooms + ' חדרים בעיר, 2020 עד 2024', value: F.num(r.n) + ' עסקאות, חציון ' + mln(r.price) });
      return out;
    }
  });

  /* ---------------------------------------------------------------- gdnmap */
  var ML = 'https://unpkg.com/maplibre-gl@4.7.1/dist/', RTL = 'https://unpkg.com/@mapbox/mapbox-gl-rtl-text@0.2.3/mapbox-gl-rtl-text.min.js';
  var STYLE = 'https://tiles.openfreemap.org/styles/positron';
  var BIN = [[0, '#a9cdb0', 'עד ₪35,000 למ״ר'], [35000, '#4f8f5e', '₪35,000 עד 50,000'], [50000, '#2f6b3f', '₪50,000 עד 65,000'], [65000, '#1f4a2b', 'מעל ₪65,000 למ״ר']];
  function col(pp) { var c = BIN[0][1]; BIN.forEach(function (b) { if (pp >= b[0]) c = b[1]; }); return c; }
  function loadML(cb) {
    if (window.maplibregl) return cb();
    var l = document.createElement('link'); l.rel = 'stylesheet'; l.href = ML + 'maplibre-gl.css'; document.head.appendChild(l);
    var s = document.createElement('script'); s.src = ML + 'maplibre-gl.js'; s.async = true;
    s.onload = function () { try { window.maplibregl.setRTLTextPlugin(RTL, true); } catch (e) { /* already set */ } cb(); };
    s.onerror = function () { cb(new Error('map')); }; document.head.appendChild(s);
  }
  NLI.register('gdnmap', {
    custom: function (root, data) {
      var d = data.garden, phone = window.matchMedia('(max-width: 760px)').matches, sel = '';
      var names = Object.keys(d.hoods).filter(function (n) { return d.deals.some(function (x) { return x[4] === n; }); }).sort(function (a, b) { return d.hoods[b].n - d.hoods[a].n; });
      root.innerHTML = '<div class="nli__panel gdm"><p class="nli__kicker">מפה · דירות גן בתל אביב</p><h2 class="nli__title">איפה נמכרו דירות גן בתל אביב</h2>'
        + '<p class="nli__lede">כל ' + F.num(d.deals.length) + ' עסקאות דירות הגן שדווחו בתל אביב-יפו, במקומן, בצבע לפי המחיר למ״ר. ליד כל שכונה: המחיר החציוני למ״ר בשנים 2015 עד 2024, או מספר העסקאות כשיש פחות מ־5.</p>'
        + '<div class="nls__chips gdm__chips" role="group"><button type="button" data-p="" aria-pressed="true">כל העיר</button>' + names.map(function (n) { return '<button type="button" data-p="' + esc(n) + '" aria-pressed="false">' + esc(n) + ' · ' + d.hoods[n].n + '</button>'; }).join('') + '</div>'
        + '<div class="gdm__map" role="region" aria-label="מפת עסקאות דירות הגן בתל אביב"><p class="nls__wait">טוען את המפה…</p></div>'
        + '<div class="nls__bar"><button type="button" class="nls__3d gdm__3d" aria-pressed="true">מבט מוטה</button><ul class="nls__legend">' + BIN.map(function (b) { return '<li><b style="background:' + b[1] + '"></b>' + esc(b[2]) + '</li>'; }).join('') + '</ul></div>'
        + '<p class="nli__note">כל נקודה היא עסקה שדווחה לרשות המסים, במיקום החלקה. ' + END + ': אחרי אוגוסט 2024 רשות המסים הפסיקה לסמן עסקאות כ"דירת גן". שכונה בלי נקודות היא שכונה בלי עסקה מסומנת, לא שכונה בלי דירות גן.</p>'
        + '<p class="nli__src">מקור: רשות המסים, עסקאות נדל״ן. המיקום: שכבת הכתובות והשכונות של עיריית תל אביב-יפו. המפה: © OpenStreetMap, OpenFreeMap.</p></div>';
      var mapEl = root.querySelector('.gdm__map'), map = null;
      function fc(only) { return { type: 'FeatureCollection', features: d.deals.filter(function (x) { return !only || x[4] === only; }).map(function (x) {
        var pp = x[6] >= 20 && x[7] ? x[7] / x[6] : 0;
        return { type: 'Feature', properties: { c: pp ? col(pp) : '#8a948d', t: x[2], a: x[3], r: x[5], m: x[6], p: x[7], n: x[8] }, geometry: { type: 'Point', coordinates: [x[0], x[1]] } }; }) }; }
      function labels() { return { type: 'FeatureCollection', features: names.map(function (n) { var xs = d.deals.filter(function (x) { return x[4] === n; }), lo = 0, la = 0;
        xs.forEach(function (x) { lo += x[0]; la += x[1]; }); var h = d.hoods[n];
        return { type: 'Feature', properties: { t: n + '\n' + (h.ppsqm ? ils(h.ppsqm) + ' למ״ר' : h.n + ' עסקאות') }, geometry: { type: 'Point', coordinates: [lo / xs.length, la / xs.length] } }; }) }; }
      function bounds(only) { var b = new window.maplibregl.LngLatBounds(); d.deals.forEach(function (x) { if (!only || x[4] === only) b.extend([x[0], x[1]]); }); return b; }
      function choose(p) { sel = p; [].forEach.call(root.querySelectorAll('.gdm__chips button'), function (x) { x.setAttribute('aria-pressed', String(x.getAttribute('data-p') === p)); });
        if (!map || !map.getSource('gdn')) return; map.getSource('gdn').setData(fc(p)); map.fitBounds(bounds(p), { padding: phone ? 40 : 80, maxZoom: 16, duration: 800 }); }
      root.querySelector('.gdm__chips').addEventListener('click', function (e) { var b = e.target.closest('button[data-p]'); if (b) choose(b.getAttribute('data-p')); });
      loadML(function (err) {
        if (err || !window.maplibregl) { mapEl.innerHTML = '<p class="nls__wait">המפה לא נטענה. הטבלאות בעמוד מציגות את כל הנתונים.</p>'; return; }
        var gl = window.maplibregl;
        map = new gl.Map({ container: mapEl, style: STYLE, bounds: bounds(''), fitBoundsOptions: { padding: phone ? 26 : 50 }, pitch: phone ? 40 : 52, bearing: -20, maxPitch: 65, cooperativeGestures: !NLI.fine, attributionControl: { compact: true } });
        map.addControl(new gl.NavigationControl({ showCompass: true }), 'top-left');
        if (NLI.wheelIntent) NLI.wheelIntent(map, mapEl, false); // HAD-790
        map.on('load', function () {
          var w = mapEl.querySelector('.nls__wait'); if (w) w.remove();
          map.addSource('gdn', { type: 'geojson', data: fc('') });
          map.addLayer({ id: 'gdn-pt', type: 'circle', source: 'gdn', paint: { 'circle-radius': ['interpolate', ['linear'], ['zoom'], 11, 3.5, 16, 8], 'circle-color': ['get', 'c'], 'circle-stroke-color': '#fff', 'circle-stroke-width': 1.2, 'circle-pitch-alignment': 'map' } });
          map.addSource('gdn-l', { type: 'geojson', data: labels() });
          map.addLayer({ id: 'gdn-lab', type: 'symbol', source: 'gdn-l', layout: { 'text-field': ['get', 't'], 'text-size': phone ? 11.5 : 12.5, 'text-font': ['Noto Sans Regular'], 'text-offset': [0, -1.4], 'text-anchor': 'bottom', 'text-padding': 4 },
            paint: { 'text-color': '#14212b', 'text-halo-color': '#fff', 'text-halo-width': 1.6 } });
          var pop = new gl.Popup({ closeButton: false, offset: 8 });
          map.on('click', 'gdn-pt', function (e) { var q = e.features[0].properties;
            pop.setLngLat(e.features[0].geometry.coordinates).setHTML('<b>' + esc(q.a) + '</b><br>' + esc(F.date(q.t)) + ' · ' + (q.r ? q.r + ' חדרים · ' : '') + (q.m ? q.m + ' מ״ר · ' : '') + esc(ils(q.p)) + (q.n ? ' · חדשה מקבלן' : '')).addTo(map); });
          map.on('mouseenter', 'gdn-pt', function () { map.getCanvas().style.cursor = 'pointer'; }); map.on('mouseleave', 'gdn-pt', function () { map.getCanvas().style.cursor = ''; });
          if (sel) choose(sel);
        });
        var b3 = root.querySelector('.gdm__3d');
        b3.addEventListener('click', function () { var on = b3.getAttribute('aria-pressed') !== 'true'; b3.setAttribute('aria-pressed', String(on)); map.easeTo({ pitch: on ? (phone ? 40 : 52) : 0, bearing: on ? -20 : 0, duration: 700 }); });
      });
    }
  });

  /* ---------------------------------------------------------------- gdnstreet */
  NLI.register('gdnstreet', {
    custom: function (root, data) {
      var d = data.garden, by = {};
      d.deals.forEach(function (x) { var s = x[9] || x[3].replace(/\s*\d+[א-ת]?\s*$/, '').trim(); if (s) (by[s] = by[s] || []).push(x); });  // the street column: the display address spells a street several ways
      var streets = Object.keys(by).sort(function (a, b) { return by[b].length - by[a].length || a.localeCompare(b, 'he'); });
      root.innerHTML = '<div class="nli__panel gds"><p class="nli__kicker">איתור · רחוב</p><h2 class="nli__title">דירות גן ברחוב שלכם</h2>'
        + '<p class="nli__lede">מקלידים רחוב בתל אביב-יפו ורואים כל עסקת דירת גן שדווחה בו: התאריך, החדרים, השטח והמחיר.</p>'
        + '<label class="nls__q"><span>רחוב</span><input type="search" list="gds-list" enterkeyhint="search" placeholder="למשל פן אלכסנדר או קהילת ורשה" autocomplete="off"></label>'
        + '<datalist id="gds-list">' + streets.map(function (s) { return '<option value="' + esc(s) + '">'; }).join('') + '</datalist>'
        + '<div class="gds__out" aria-live="polite"></div>'
        + '<p class="nli__note">' + F.num(streets.length) + ' רחובות עם עסקת דירת גן. רחוב שלא מופיע הוא רחוב בלי עסקה מסומנת כ"דירת גן", ' + END + '.</p><p class="nli__src">' + esc(SRC) + '</p></div>';
      var inp = root.querySelector('input'), out = root.querySelector('.gds__out');
      function draw() {
        var q = inp.value.trim(), s = by[q] ? q : streets.filter(function (x) { return q && x.indexOf(q) === 0; })[0];
        if (!s) { out.innerHTML = q ? '<p class="nli__note">לא נמצאה עסקת דירת גן ברחוב הזה.</p>' : ''; return; }
        var L = by[s];
        out.innerHTML = '<p class="gds__h"><b>' + esc(s) + '</b> · ' + L.length + (L.length === 1 ? ' עסקה' : ' עסקאות') + '</p><div class="nli__tw"><table><thead><tr><th>תאריך</th><th>כתובת</th><th class="n">חדרים</th><th class="n">מ״ר</th><th class="n">מחיר</th></tr></thead><tbody>'
          + L.map(function (x) { return '<tr><td>' + esc(F.date(x[2])) + '</td><td>' + esc(x[3]) + (x[8] ? ' <i>חדשה</i>' : '') + '</td><td class="n">' + (x[5] || '') + '</td><td class="n">' + (x[6] || '') + '</td><td class="n">' + esc(ils(x[7])) + '</td></tr>'; }).join('') + '</tbody></table></div>';
      }
      inp.addEventListener('input', draw); inp.addEventListener('change', draw);
      inp.value = streets[0]; draw();
    }
  });

  /* ---------------------------------------------------------------- gdnground */
  NLI.register('gdnground', {
    custom: function (root, data) {
      var d = data.garden, G = d.ground.slice().sort(function (a, b) { return b[4] - a[4]; }), mx = Math.max.apply(null, G.map(function (g) { return Math.abs(g[4]); }));
      root.innerHTML = '<div class="nli__panel gdg"><p class="nli__kicker">השוואה · קומת קרקע</p><h2 class="nli__title">קומת קרקע מול כל הבניין</h2>'
        + '<p class="nli__lede">בכל שכונה: בכמה אחוזים דירה רגילה בקומת הקרקע נמכרה מעל או מתחת לדירות בשאר הבניין, למ״ר, בשנים 2020 עד 2024. זו קומת קרקע, לא בהכרח דירת גן.</p>'
        + '<div class="gdg__rows">' + G.map(function (g) { var w = Math.round(46 * Math.abs(g[4]) / mx), up = g[4] >= 0;
          return '<div class="gdg__row"><span>' + esc(g[0]) + '</span><i class="' + (up ? 'up' : 'dn') + '" style="--w:' + w + '%"></i><b dir="ltr">' + (up ? '+' : '') + F.num(g[4], 1) + '%</b></div>'; }).join('') + '</div>'
        + '<details class="nli__table"><summary>המספרים המלאים</summary><div class="nli__tw"><table><thead><tr><th>שכונה</th><th class="n">כל הבניין, ₪ למ״ר</th><th class="n">קומת קרקע, ₪ למ״ר</th><th class="n">עסקאות קרקע</th></tr></thead><tbody>'
        + G.map(function (g) { return '<tr><td>' + esc(g[0]) + '</td><td class="n">' + esc(ils(g[1])) + '</td><td class="n">' + esc(ils(g[2])) + '</td><td class="n">' + g[3] + '</td></tr>'; }).join('') + '</tbody></table></div></details>'
        + '<p class="nli__src">' + esc(SRC.replace('עד 28.8.2024', '2020 עד 2024')) + ' שכונות עם 5 עסקאות קומת קרקע ומעלה.</p></div>';
    }
  });
})();
