/* NadLan Instruments · hazards v1 (HAD-670 R13e, Ben 3.11.2026 night: "the awesome map: a very extensive page, a 3D map where people
   see where they are, 4-5 complex tools with easy mobile UX, practical for choosing where to live"; Claude Design v109.0 HazardMap).
   Five tools of one family ('file' => 'hazards' in inc/hazards-tools.php), on data/hazards.json + data/hazards-lines.json
   (tools/instruments/build_hazards_data.py, every layer from an official open register or OpenStreetMap, read 3.11.2026):
   hzmap      the scope: an address (Nominatim, on submit only, cached) or "my location" (the browser) or a tap on the map; a radius;
              the layers; a tilted MapLibre map with 3D buildings; the report card of what is within the radius and how far;
   hzant      the antennas near the chosen point with their measured share of the health threshold (MoEP register);
   hzcompare  two addresses side by side, the same rows;
   hzcity     a city's figures: antennas (count, median and highest measured share), reporting plants, fuel stations;
   hzplan     what to check before buying or renting, who checks it, and what it costs where a price was published.
   The map shows distance, never exposure; no company, operator or plant name is shown (the no-names law). Hebrew only. */
(function () {
  'use strict';
  if (!window.NadLanInstruments) return;
  var NLI = window.NadLanInstruments, F = NLI.fmt, esc = NLI.esc;
  var ML = 'https://unpkg.com/maplibre-gl@4.7.1/dist/', RTL = 'https://unpkg.com/@mapbox/mapbox-gl-rtl-text@0.2.3/mapbox-gl-rtl-text.min.js';
  var STYLE = 'https://tiles.openfreemap.org/styles/positron';
  var LAY = [
    { k: 'ant', name: 'אנטנות סלולריות', one: 'אנטנה סלולרית', c: '#6a4fd6', on: true },
    { k: 'line', name: 'קווי מתח עליון', one: 'קו מתח עליון', c: '#0b8fb3', on: true },
    { k: 'sub', name: 'תחנות משנה', one: 'תחנת משנה', c: '#0a5f78', on: true },
    { k: 'prtr', name: 'מפעלים מדווחים', one: 'מפעל מדווח', c: '#c0392b', on: true },
    { k: 'fuel', name: 'תחנות דלק', one: 'תחנת דלק', c: '#e0701b', on: true },
    { k: 'plant', name: 'תחנות כוח', one: 'תחנת כוח', c: '#37474f', on: false },
    { k: 'soil', name: 'קרקע בחשד לזיהום', one: 'אתר קרקע', c: '#7c8a2a', on: false },
    { k: 'air', name: 'תחנות ניטור אוויר', one: 'תחנת ניטור אוויר', c: '#2f86a8', on: false }
  ];
  var SOIL = ['חשד לזיהום (לא אומת)', 'בחקירה או בשיקום', 'סיים שיקום או אין סיכון'];
  var SITE = { ground: 'תורן קרקעי', roof: 'תורן על גג', indoor: 'אתר זעיר בתוך מבנה', small: 'אתר זעיר חיצוני', sting: 'אנטנת עוקץ', wifi: 'מתקן גישה אלחוטי', slope: 'אנטנה משתפלת', other: 'אתר' };
  var HOME = { pt: [34.7818, 32.0809], label: 'כיכר רבין, תל אביב-יפו (נקודת פתיחה לדוגמה)' };
  var S = window.NLHZ = window.NLHZ || { pt: HOME.pt, label: HOME.label, r: 250 };
  function f(s, o) { return String(s).replace(/\{(\w+)\}/g, function (m, k) { return o[k] != null ? o[k] : m; }); }
  function m2(a, b) { var k = Math.cos(a[1] * Math.PI / 180); return Math.hypot((b[0] - a[0]) * 111320 * k, (b[1] - a[1]) * 110574); }
  function seg(p, a, b) { var k = Math.cos(p[1] * Math.PI / 180), ax = (a[0] - p[0]) * 111320 * k, ay = (a[1] - p[1]) * 110574, bx = (b[0] - p[0]) * 111320 * k, by = (b[1] - p[1]) * 110574;
    var dx = bx - ax, dy = by - ay, dd = dx * dx + dy * dy || 1e-9, t = Math.max(0, Math.min(1, -(ax * dx + ay * dy) / dd)); return Math.hypot(ax + t * dx, ay + t * dy); }
  function dist(n) { return n < 1000 ? F.num(Math.round(n / 10) * 10) + ' מ׳' : F.num(n / 1000, 1) + ' ק״מ'; }
  function pct(v) { return v == null ? '' : F.num(v, v < 10 ? 2 : 1) + '%'; }
  function bus() { try { window.dispatchEvent(new CustomEvent('nlhz:pt')); } catch (e) { /* old browser */ } }
  var CACHE = {};
  function geocode(q) {
    q = String(q || '').trim(); if (!q) return Promise.reject(new Error('empty'));
    try { var c = JSON.parse(localStorage.getItem('nlhz-geo') || '{}'); CACHE = c; } catch (e) { /* storage blocked */ }
    if (CACHE[q]) return Promise.resolve(CACHE[q]);
    var u = 'https://nominatim.openstreetmap.org/search?format=jsonv2&countrycodes=il&limit=1&accept-language=he&q=' + encodeURIComponent(q);
    return fetch(u, { headers: { Accept: 'application/json' } }).then(function (r) { return r.json(); }).then(function (j) {
      if (!j || !j[0]) throw new Error('none');
      var v = { pt: [+(+j[0].lon).toFixed(5), +(+j[0].lat).toFixed(5)], label: String(j[0].display_name || q).split(',').slice(0, 3).join(',').replace(/[\u2013\u2014]/g, '-') };  // OSM writes long dashes (תל־אביב\u2013יפו)
      CACHE[q] = v; try { localStorage.setItem('nlhz-geo', JSON.stringify(CACHE)); } catch (e) { /* storage blocked */ }
      return v;
    });
  }
  /** everything within r metres of p, and the nearest item of each layer */
  function report(p, r, d, L) {
    var o = {};
    function pts(k, arr, extra) { var n = 0, best = null, inR = []; arr.forEach(function (a) { var x = m2(p, a); if (x <= r) { n++; inR.push([x, a]); } if (!best || x < best[0]) best = [x, a]; });
      inR.sort(function (u, v) { return u[0] - v[0]; }); o[k] = { n: n, near: best, inR: inR }; if (extra) extra(o[k]); }
    pts('ant', d.ant, function (z) { z.max = z.inR.reduce(function (m, q) { return Math.max(m, q[1][2] || 0); }, 0); });
    pts('pend', d.pend); pts('sub', d.sub); pts('prtr', d.prtr); pts('fuel', d.fuel); pts('plant', d.plant); pts('soil', d.soil); pts('air', d.air);
    var lb = null; (L ? L.lines : []).forEach(function (l) { for (var i = 1; i < l.c.length; i++) { var x = seg(p, l.c[i - 1], l.c[i]); if (!lb || x < lb[0]) lb = [x, l.kv]; } });
    o.line = { n: lb && lb[0] <= r ? 1 : 0, near: lb };
    return o;
  }
  function rows(o, r) {
    function row(k, title, body, val, none) { var l = LAY.filter(function (x) { return x.k === k; })[0];
      return '<div class="hzr' + (none ? ' none' : '') + '"><i style="background:' + l.c + '"></i><div><b>' + esc(title) + '</b><span>' + esc(body) + '</span></div><em>' + esc(val) + '</em></div>'; }
    var a = o.ant, h = '';
    h += a.n ? row('ant', a.n === 1 ? 'אנטנה סלולרית אחת' : F.num(a.n) + ' אנטנות סלולריות', 'הקרובה ' + dist(a.inR[0][0]) + ', ' + (SITE[a.inR[0][1][3]] || 'אתר') + '. הקרינה הגבוהה שנמדדה בה: ' + pct(a.inR[0][1][2]) + ' מסף הבריאות' + (a.n > 1 ? '; הגבוהה ברדיוס: ' + pct(a.max) : '') + '.', dist(a.inR[0][0]))
      : row('ant', 'אנטנות סלולריות', 'אין ברדיוס. הקרובה ' + dist(a.near[0]) + ', ובה נמדדו ' + pct(a.near[1][2]) + ' מסף הבריאות.', 'אין ברדיוס', true);
    if (o.pend.n) h += row('ant', F.num(o.pend.n) + ' בקשות להיתר לאנטנה', 'בקשות שממתינות להיתר הקמה ברדיוס. אפשר לבקש לראות את הבקשה ולהגיש התנגדות.', dist(o.pend.inR[0][0]));
    var L = o.line.near;
    h += L ? row('line', 'קו מתח עליון' + (L[1] ? ' ' + L[1] + ' ק״ו' : ''), o.line.n ? 'עובר ברדיוס, ' + dist(L[0]) + ' מהנקודה.' : 'מחוץ לרדיוס. הקרוב ' + dist(L[0]) + '.', dist(L[0]), !o.line.n) : '';
    [['sub', 'תחנות משנה', 'תחנת משנה'], ['prtr', 'מפעלים שמדווחים על פליטות (מפל״ס)', 'מפעל מדווח'], ['fuel', 'תחנות דלק', 'תחנת דלק'], ['plant', 'תחנות כוח', 'תחנת כוח'], ['soil', 'אתרי קרקע במאגר הלאומי', 'אתר קרקע']].forEach(function (q) {
      var z = o[q[0]], body;
      if (z.n) { body = 'הקרוב ' + dist(z.inR[0][0]) + (q[0] === 'prtr' ? ', ענף: ' + z.inR[0][1][2] : q[0] === 'soil' ? ', ' + SOIL[z.inR[0][1][2]] : '') + '.';
        h += row(q[0], (z.n === 1 ? q[2] + ' אחת' : F.num(z.n) + ' ' + q[1]).replace('מפעל מדווח אחת', 'מפעל מדווח אחד').replace('אתר קרקע אחת', 'אתר קרקע אחד'), body, dist(z.inR[0][0])); }
      else if (z.near) h += row(q[0], q[1], 'אין ברדיוס. הקרוב ' + dist(z.near[0]) + '.', 'אין ברדיוס', true);
    });
    if (o.air.near) h += row('air', 'תחנת ניטור אוויר', 'התחנה הקרובה ' + dist(o.air.near[0]) + '. הערכים העדכניים מתפרסמים באתר המשרד להגנת הסביבה.', dist(o.air.near[0]), true);
    return h;
  }
  var NOTE = 'אין סימון במפה לא אומר שאין מפגע. המפה מציגה מרחק, לא חשיפה, ורק מה שפורסם במאגרים: חדרי שנאים, צנרת דלק, רעש מטוסים וערכי זיהום אוויר בזמן אמת לא פורסמו כנתונים פתוחים. קרינה בתוך דירה מודדים רק במדידה של מודד בעל היתר.';
  function loadML(cb) {
    if (window.maplibregl) return cb();
    var l = document.createElement('link'); l.rel = 'stylesheet'; l.href = ML + 'maplibre-gl.css'; document.head.appendChild(l);
    var s = document.createElement('script'); s.src = ML + 'maplibre-gl.js'; s.async = true;
    s.onload = function () { try { window.maplibregl.setRTLTextPlugin(RTL, true); } catch (e) { /* already set */ } cb(); };
    s.onerror = function () { cb(new Error('map')); }; document.head.appendChild(s);
  }
  function ring(p, r) { var c = [], k = Math.cos(p[1] * Math.PI / 180); for (var i = 0; i <= 64; i++) { var t = i / 64 * 2 * Math.PI; c.push([p[0] + r * Math.cos(t) / (111320 * k), p[1] + r * Math.sin(t) / 110574]); }
    return { type: 'FeatureCollection', features: [{ type: 'Feature', properties: {}, geometry: { type: 'Polygon', coordinates: [c] } }] }; }
  function fcPts(arr, props) { return { type: 'FeatureCollection', features: arr.map(function (a) { return { type: 'Feature', properties: props ? props(a) : {}, geometry: { type: 'Point', coordinates: [a[0], a[1]] } }; }) }; }

  /* ---------------------------------------------------------------- hzmap */
  NLI.register('hzmap', {
    custom: function (root, data) {
      var d = data.hz, Ln = data.hzl, phone = window.matchMedia('(max-width: 760px)').matches, map = null, on = {};
      LAY.forEach(function (l) { on[l.k] = l.on; });
      root.innerHTML = '<div class="nli__panel hzm"><p class="nli__kicker">מפה · מפגעים סביבתיים</p><h2 class="nli__title">מה יש סביב הבית</h2>'
        + '<p class="nli__lede">מקלידים כתובת, או נוגעים ב"המיקום שלי", או במקום כלשהו במפה. בוחרים רדיוס, ורואים כל אנטנה, קו מתח, תחנת משנה, מפעל מדווח ותחנת דלק סביב הנקודה, עם המרחק והערך הרשמי.</p>'
        + '<div class="hzm__scope"><form class="hzm__find" novalidate><input type="search" enterkeyhint="search" placeholder="רחוב, מספר ועיר" aria-label="כתובת" autocomplete="street-address"><button type="submit" class="hzm__go">בדיקה</button>'
        + '<button type="button" class="hzm__loc" aria-label="המיקום שלי"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="8" cy="8" r="4.5"/><path d="M8 0v3M8 13v3M0 8h3M13 8h3"/></svg>המיקום שלי</button></form>'
        + '<p class="hzm__where" aria-live="polite"></p>'
        + '<div class="hzm__rad" role="group" aria-label="רדיוס">' + [100, 250, 500, 1000].map(function (r) { return '<button type="button" data-r="' + r + '" aria-pressed="' + (S.r === r) + '">' + (r < 1000 ? r + ' מ׳' : 'ק״מ') + '</button>'; }).join('') + '</div>'
        + '<div class="hzm__layers" role="group" aria-label="מה להציג">' + LAY.map(function (l) { return '<button type="button" data-l="' + l.k + '" aria-pressed="' + l.on + '"><i style="background:' + l.c + '"></i>' + esc(l.name) + '</button>'; }).join('') + '</div>'
        + '<div class="hzm__map" role="region" aria-label="מפת המפגעים סביב הנקודה"><p class="nls__wait">טוען את המפה…</p></div>'
        + '<div class="hzm__bar"><button type="button" class="hzm__3d" aria-pressed="true">מבט תלת־ממדי</button></div></div>'
        + '<div class="hzm__rep" aria-live="polite"></div><p class="nli__note">' + esc(NOTE) + '</p>'
        + '<p class="nli__src">מקורות: ' + esc([d.sources.ant, d.sources.prtr, d.sources.fuel, d.sources.soil, d.sources.air, d.sources.osm].join('; ')) + '. נקראו ' + esc(F.date(d.read)) + '. הכתובת: OpenStreetMap Nominatim. המפה: © OpenStreetMap, OpenFreeMap.</p></div>';
      var rep = root.querySelector('.hzm__rep'), where = root.querySelector('.hzm__where'), inp = root.querySelector('input'), mapEl = root.querySelector('.hzm__map');
      function draw(fly) {
        var o = report(S.pt, S.r, d, Ln);
        where.textContent = 'הנקודה: ' + S.label + ' · רדיוס ' + (S.r < 1000 ? S.r + ' מ׳' : 'ק״מ');
        rep.innerHTML = '<p class="hzm__k">דוח סביבה · ' + esc(S.label) + '</p>' + rows(o, S.r);
        if (map && map.getSource('hz-ring')) {
          map.getSource('hz-ring').setData(ring(S.pt, S.r)); map.getSource('hz-me').setData(fcPts([S.pt]));
          var lab = [];
          o.ant.inR.slice(0, 4).forEach(function (q) { lab.push([q[1][0], q[1][1], 'אנטנה · ' + dist(q[0]) + ' · ' + pct(q[1][2])]); });
          [['sub', 'תחנת משנה'], ['prtr', 'מפעל מדווח'], ['fuel', 'תחנת דלק'], ['plant', 'תחנת כוח'], ['soil', 'אתר קרקע']].forEach(function (q) { if (on[q[0]]) o[q[0]].inR.slice(0, 2).forEach(function (z) { lab.push([z[1][0], z[1][1], q[1] + ' · ' + dist(z[0])]); }); });
          map.getSource('hz-lab').setData(fcPts(lab, function (a) { return { t: a[2] }; }));
          if (fly) { var k = Math.cos(S.pt[1] * Math.PI / 180), dx = S.r * 1.25 / (111320 * k), dy = S.r * 1.25 / 110574;
            map.fitBounds([[S.pt[0] - dx, S.pt[1] - dy], [S.pt[0] + dx, S.pt[1] + dy]], { padding: phone ? 16 : 40, duration: 900, pitch: map.getPitch() }); }
        }
        bus();
      }
      function set(pt, label, fly) { S.pt = pt; S.label = label; draw(fly !== false); }
      root.querySelector('form').addEventListener('submit', function (e) { e.preventDefault(); var q = inp.value.trim(); if (!q) return;
        where.textContent = 'מחפש את הכתובת…';
        geocode(q).then(function (v) { set(v.pt, v.label); }, function () { where.textContent = 'לא מצאנו את הכתובת. נסו רחוב, מספר ועיר, או געו במפה.'; }); });
      root.querySelector('.hzm__loc').addEventListener('click', function () {
        if (!navigator.geolocation) { where.textContent = 'הדפדפן לא מאפשר מיקום. הקלידו כתובת או געו במפה.'; return; }
        where.textContent = 'מאתר את המיקום שלכם…';
        navigator.geolocation.getCurrentPosition(function (g) { set([+g.coords.longitude.toFixed(5), +g.coords.latitude.toFixed(5)], 'המיקום שלכם'); },
          function () { where.textContent = 'המיקום לא אושר. הקלידו כתובת או געו במפה.'; }, { enableHighAccuracy: true, timeout: 10000 });
      });
      root.querySelector('.hzm__rad').addEventListener('click', function (e) { var b = e.target.closest('button[data-r]'); if (!b) return; S.r = +b.getAttribute('data-r');
        [].forEach.call(this.children, function (x) { x.setAttribute('aria-pressed', String(x === b)); }); draw(true); });
      root.querySelector('.hzm__layers').addEventListener('click', function (e) { var b = e.target.closest('button[data-l]'); if (!b) return; var k = b.getAttribute('data-l'); on[k] = !on[k];
        b.setAttribute('aria-pressed', String(on[k])); if (map && map.getLayer('hz-' + k)) map.setLayoutProperty('hz-' + k, 'visibility', on[k] ? 'visible' : 'none'); draw(false); });
      draw(false);
      loadML(function (err) {
        if (err || !window.maplibregl) { mapEl.innerHTML = '<p class="nls__wait">המפה לא נטענה. הדוח למטה מחושב בכל זאת.</p>'; return; }
        var gl = window.maplibregl, k = Math.cos(S.pt[1] * Math.PI / 180), dx = S.r * 1.25 / (111320 * k), dy = S.r * 1.25 / 110574;
        map = new gl.Map({ container: mapEl, style: STYLE, bounds: [[S.pt[0] - dx, S.pt[1] - dy], [S.pt[0] + dx, S.pt[1] + dy]], pitch: phone ? 45 : 55, bearing: -18, maxPitch: 70, cooperativeGestures: true, attributionControl: { compact: true } });
        map.addControl(new gl.NavigationControl({ showCompass: true }), 'top-left');
        map.on('load', function () {
          var w = mapEl.querySelector('.nls__wait'); if (w) w.remove();
          if (map.getSource('openmaptiles')) map.addLayer({ id: 'hz-3d', type: 'fill-extrusion', source: 'openmaptiles', 'source-layer': 'building', minzoom: 13,
            paint: { 'fill-extrusion-color': '#d9e1e7', 'fill-extrusion-height': ['coalesce', ['get', 'render_height'], 9], 'fill-extrusion-base': ['coalesce', ['get', 'render_min_height'], 0], 'fill-extrusion-opacity': 0.85 } });
          map.addSource('hz-line', { type: 'geojson', data: { type: 'FeatureCollection', features: Ln.lines.map(function (l) { return { type: 'Feature', properties: { kv: l.kv }, geometry: { type: 'LineString', coordinates: l.c } }; }) } });
          map.addLayer({ id: 'hz-line', type: 'line', source: 'hz-line', paint: { 'line-color': '#0b8fb3', 'line-width': ['match', ['get', 'kv'], 400, 3.2, 2.2], 'line-dasharray': [3, 1.6] } });
          [['ant', d.ant, 3.2], ['sub', d.sub, 5], ['prtr', d.prtr, 4.5], ['fuel', d.fuel, 4.5], ['plant', d.plant, 6], ['soil', d.soil.filter(function (s) { return s[2] < 2; }), 3.5], ['air', d.air, 5]].forEach(function (q) {
            var l = LAY.filter(function (x) { return x.k === q[0]; })[0];
            map.addSource('hz-' + q[0], { type: 'geojson', data: fcPts(q[1], function (a) { return q[0] === 'ant' ? { p: a[2] || 0 } : {}; }) });
            map.addLayer({ id: 'hz-' + q[0], type: 'circle', source: 'hz-' + q[0], layout: { visibility: on[q[0]] ? 'visible' : 'none' },
              paint: { 'circle-radius': ['interpolate', ['linear'], ['zoom'], 10, q[2] * 0.55, 16, q[2] * 1.3], 'circle-color': l.c, 'circle-stroke-color': '#fff', 'circle-stroke-width': 1.1, 'circle-pitch-alignment': 'map' } });
          });
          map.addSource('hz-ring', { type: 'geojson', data: ring(S.pt, S.r) });
          map.addLayer({ id: 'hz-ring-f', type: 'fill', source: 'hz-ring', paint: { 'fill-color': '#0f2733', 'fill-opacity': 0.06 } });
          map.addLayer({ id: 'hz-ring-l', type: 'line', source: 'hz-ring', paint: { 'line-color': '#0f2733', 'line-width': 1.6, 'line-dasharray': [2, 2] } });
          map.addSource('hz-me', { type: 'geojson', data: fcPts([S.pt]) });
          map.addLayer({ id: 'hz-me', type: 'circle', source: 'hz-me', paint: { 'circle-radius': 8, 'circle-color': '#0f2733', 'circle-stroke-color': '#fff', 'circle-stroke-width': 3 } });
          map.addSource('hz-lab', { type: 'geojson', data: fcPts([]) });
          map.addLayer({ id: 'hz-lab', type: 'symbol', source: 'hz-lab', layout: { 'text-field': ['get', 't'], 'text-size': phone ? 11 : 12, 'text-font': ['Noto Sans Regular'], 'text-offset': [0, -1.2], 'text-anchor': 'bottom', 'text-padding': 3 },
            paint: { 'text-color': '#101820', 'text-halo-color': '#fff', 'text-halo-width': 1.8 } });
          map.on('click', function (e) { if (e.defaultPrevented) return; set([+e.lngLat.lng.toFixed(5), +e.lngLat.lat.toFixed(5)], 'הנקודה שבחרתם במפה', false); });
          draw(false);
        });
        var b3 = root.querySelector('.hzm__3d');
        b3.addEventListener('click', function () { var o2 = b3.getAttribute('aria-pressed') !== 'true'; b3.setAttribute('aria-pressed', String(o2)); map.easeTo({ pitch: o2 ? (phone ? 45 : 55) : 0, bearing: o2 ? -18 : 0, duration: 700 }); });
      });
    }
  });

  /* ---------------------------------------------------------------- hzant */
  NLI.register('hzant', {
    custom: function (root, data) {
      var d = data.hz;
      root.innerHTML = '<div class="nli__panel hza"><p class="nli__kicker">בדיקה · אנטנות סלולריות</p><h2 class="nli__title">כמה קרינה נמדדה באנטנות ליד הבית</h2>'
        + '<p class="nli__lede">לכל אנטנה פעילה המשרד להגנת הסביבה מפרסם את התוצאה הגבוהה שנמדדה בה, באחוזים מסף הבריאות. כאן עשר האנטנות הקרובות לנקודה שבחרתם במפה.</p><div class="hza__out" aria-live="polite"></div>'
        + '<p class="nli__note">הסף בישראל: 10% מהמגבלה הבינלאומית במקום שבו שוהים זמן רב, ו־30% במקום מעבר. בכל המאגר החציון הוא ' + pct(med(d.ant)) + ' והערך הגבוה ' + pct(maxp(d.ant)) + '. שם החברה המפעילה לא מוצג.</p>'
        + '<p class="nli__src">מקור: ' + esc(d.sources.ant) + ', נקרא ' + esc(F.date(d.read)) + '.</p></div>';
      var out = root.querySelector('.hza__out');
      function draw() { var L = d.ant.map(function (a) { return [m2(S.pt, a), a]; }).sort(function (u, v) { return u[0] - v[0]; }).slice(0, 10);
        out.innerHTML = '<p class="hzm__k">ליד: ' + esc(S.label) + '</p><div class="nli__tw"><table><thead><tr><th>סוג האתר</th><th class="n">מרחק</th><th class="n">מסף הבריאות</th><th class="n">בדיקה אחרונה</th></tr></thead><tbody>'
          + L.map(function (q) { var a = q[1], w = Math.max(2, Math.round((a[2] || 0) / 30 * 100));
            return '<tr><td>' + esc(SITE[a[3]] || 'אתר') + '<i class="hza__bar" style="width:' + w + '%"></i></td><td class="n">' + dist(q[0]) + '</td><td class="n">' + pct(a[2]) + '</td><td class="n">' + (a[4] || '') + '</td></tr>'; }).join('') + '</tbody></table></div>'; }
      window.addEventListener('nlhz:pt', draw); draw();
    }
  });
  function med(a) { var v = a.map(function (x) { return x[2]; }).filter(function (x) { return x != null; }).sort(function (p, q) { return p - q; }); return v[Math.floor(v.length / 2)]; }
  function maxp(a) { return a.reduce(function (m, x) { return Math.max(m, x[2] || 0); }, 0); }

  /* ---------------------------------------------------------------- hzcompare */
  NLI.register('hzcompare', {
    custom: function (root, data) {
      var d = data.hz, Ln = data.hzl, A = null, B = null;
      root.innerHTML = '<div class="nli__panel hzc"><p class="nli__kicker">השוואה · שתי כתובות</p><h2 class="nli__title">איפה לגור: שתי כתובות זו מול זו</h2>'
        + '<p class="nli__lede">מקלידים שתי כתובות ורואים לכל אחת מה יש ברדיוס של 250 מטר והקרוב מכל סוג.</p>'
        + '<form class="hzc__f" novalidate><input type="search" name="a" placeholder="כתובת ראשונה" aria-label="כתובת ראשונה"><input type="search" name="b" placeholder="כתובת שנייה" aria-label="כתובת שנייה"><button type="submit" class="hzm__go">השוואה</button></form>'
        + '<div class="hzc__out" aria-live="polite"></div><p class="nli__note">' + esc(NOTE) + '</p></div>';
      var out = root.querySelector('.hzc__out'), fm = root.querySelector('form');
      function col(v) { return '<div class="hzc__col"><p class="hzm__k">' + esc(v.label) + '</p>' + rows(report(v.pt, 250, d, Ln), 250) + '</div>'; }
      fm.addEventListener('submit', function (e) { e.preventDefault(); var qa = fm.a.value.trim(), qb = fm.b.value.trim(); if (!qa || !qb) { out.innerHTML = '<p class="nli__note">הקלידו שתי כתובות.</p>'; return; }
        out.innerHTML = '<p class="nli__note">מחפש את הכתובות…</p>';
        geocode(qa).then(function (a) { A = a; return new Promise(function (r) { setTimeout(r, 1100); }); }).then(function () { return geocode(qb); }).then(function (b) { B = b; out.innerHTML = '<div class="hzc__grid">' + col(A) + col(B) + '</div>'; },
          function () { out.innerHTML = '<p class="nli__note">אחת הכתובות לא נמצאה. נסו רחוב, מספר ועיר.</p>'; }); });
    }
  });

  /* ---------------------------------------------------------------- hzcity */
  NLI.register('hzcity', {
    custom: function (root, data) {
      var C = data.hz.cities, names = Object.keys(C);
      root.innerHTML = '<div class="nli__panel hzy"><p class="nli__kicker">נתונים · לפי עיר</p><h2 class="nli__title">אנטנות, מפעלים ותחנות דלק בעיר שלכם</h2>'
        + '<p class="nli__lede">בוחרים יישוב ורואים כמה אנטנות סלולריות פעילות רשומות בו, מה הקרינה החציונית והגבוהה שנמדדה בהן, כמה מפעלים מדווחים על פליטות וכמה תחנות דלק.</p>'
        + '<label class="nls__q"><span>יישוב</span><input type="search" list="hzy-list" placeholder="למשל חיפה או רמת גן" autocomplete="off"></label><datalist id="hzy-list">' + names.map(function (n) { return '<option value="' + esc(n) + '">'; }).join('') + '</datalist>'
        + '<div class="hzy__out" aria-live="polite"></div>'
        + '<details class="nli__table"><summary>20 היישובים עם מספר האנטנות הגדול</summary><div class="nli__tw"><table><thead><tr><th>יישוב</th><th class="n">אנטנות</th><th class="n">חציון</th><th class="n">הגבוה</th><th class="n">מפעלים</th><th class="n">דלק</th></tr></thead><tbody>'
        + names.slice(0, 20).map(function (n) { var v = C[n]; return '<tr><td>' + esc(n) + '</td><td class="n">' + F.num(v[0]) + '</td><td class="n">' + pct(v[1]) + '</td><td class="n">' + pct(v[2]) + '</td><td class="n">' + v[3] + '</td><td class="n">' + v[4] + '</td></tr>'; }).join('') + '</tbody></table></div></details>'
        + '<p class="nli__src">לפי היישוב הרשום במאגרים. חציון רק ליישוב עם 5 אנטנות ומעלה. מקורות: ' + esc([data.hz.sources.ant, data.hz.sources.prtr, data.hz.sources.fuel].join('; ')) + '.</p></div>';
      var inp = root.querySelector('input'), out = root.querySelector('.hzy__out');
      function draw() { var q = inp.value.trim(), n = C[q] ? q : names.filter(function (x) { return q && x.indexOf(q) === 0; })[0];
        if (!n) { out.innerHTML = q ? '<p class="nli__note">היישוב לא נמצא ברשימה.</p>' : ''; return; } var v = C[n];
        out.innerHTML = '<div class="hzy__grid"><div><b>' + F.num(v[0]) + '</b><span>אנטנות סלולריות פעילות</span></div><div><b>' + (v[1] != null ? pct(v[1]) : 'לא חושב') + '</b><span>הקרינה החציונית מסף הבריאות</span></div>'
          + '<div><b>' + (v[2] != null ? pct(v[2]) : '') + '</b><span>הערך הגבוה שנמדד</span></div><div><b>' + v[3] + '</b><span>מפעלים מדווחים</span></div><div><b>' + v[4] + '</b><span>תחנות דלק</span></div></div><p class="hzm__k">' + esc(n) + '</p>'; }
      inp.addEventListener('input', draw); inp.addEventListener('change', draw); inp.value = names[0]; draw();
    }
  });

  /* ---------------------------------------------------------------- hzplan */
  var PLAN = [
    { k: 'ant', label: 'אנטנה סלולרית קרובה', who: 'מודד קרינה בעל היתר מהמשרד להגנת הסביבה', what: 'מודד קרינה בתדרי רדיו בתוך הדירה, ליד חלונות ומרפסות, ונותן דוח.', price: 'כ־500 עד 650 ₪ לדירה (מחירון מסחרי שפורסם)' },
    { k: 'elf', label: 'קו מתח, תחנת משנה או חדר שנאים', who: 'מודד קרינה בעל היתר לשדות מגנטיים', what: 'מודד שדה מגנטי בתדר נמוך במילי־גאוס, בשעות צריכה שונות. היעד שהמשרד להגנת הסביבה מציין: 4 מילי־גאוס בממוצע יומי ביום שיא.', price: 'כ־500 עד 650 ₪ לדירה (מחירון מסחרי שפורסם)' },
    { k: 'noise', label: 'רעש מכביש, רכבת או מטוסים', who: 'יועץ אקוסטי', what: 'מודד רעש ביום ובלילה ומציע בידוד: חלונות, איטום, וילונות.', price: 'מחיר לא פורסם' },
    { k: 'air', label: 'מפעל, כביש ראשי או תחנת כוח', who: 'יועץ סביבתי', what: 'בודק דיווחי פליטות, תחנות ניטור ותכניות באזור, ומסביר מה הם אומרים.', price: 'מחיר לא פורסם' },
    { k: 'soil', label: 'תחנת דלק או אתר קרקע במאגר', who: 'יועץ סביבתי, ובקנייה גם עורך דין', what: 'בודק את סטטוס האתר במאגר הלאומי ואת התכניות, ומה זה אומר על הבנייה.', price: 'מחיר לא פורסם' },
    { k: 'home', label: 'מצב הדירה עצמה', who: 'בודק בית', what: 'בודק רטיבות, חשמל, אינסטלציה וליקויי בנייה, ונותן דוח.', price: 'כ־1,700 עד 1,800 ₪ בממוצע (מחירון מסחרי שפורסם)' },
    { k: 'plan', label: 'אנטנה או מתקן שעומדים לקום', who: 'עורך דין לתכנון ובנייה', what: 'בודק בקשות להיתר ותכניות בוועדה המקומית, ומגיש התנגדות בזמן.', price: 'מחיר לא פורסם' }
  ];
  NLI.register('hzplan', {
    custom: function (root) {
      var sel = { ant: true, home: true };
      root.innerHTML = '<div class="nli__panel hzp"><p class="nli__kicker">תכנון · לפני שקונים או שוכרים</p><h2 class="nli__title">מה לבדוק, מי בודק וכמה זה עולה</h2>'
        + '<p class="nli__lede">מסמנים מה יש ליד הדירה ומקבלים תכנית בדיקה: מי עושה כל בדיקה, מה הוא בודק, והמחיר במקום שבו פורסם.</p>'
        + '<div class="nls__chips hzp__chips" role="group">' + PLAN.map(function (p) { return '<button type="button" data-k="' + p.k + '" aria-pressed="' + !!sel[p.k] + '">' + esc(p.label) + '</button>'; }).join('') + '</div>'
        + '<div class="hzp__out" aria-live="polite"></div><p class="nli__note">המחירים לקוחים ממחירונים מסחריים שפורסמו, כדי לתת סדר גודל. בקשו כמה הצעות, ובדקו שלמודד יש היתר בתוקף מהמשרד להגנת הסביבה.</p></div>';
      var out = root.querySelector('.hzp__out');
      function draw() { var L = PLAN.filter(function (p) { return sel[p.k]; });
        out.innerHTML = L.length ? '<ol>' + L.map(function (p) { return '<li><b>' + esc(p.who) + '</b> · ' + esc(p.label) + '<br>' + esc(p.what) + ' <em>' + esc(p.price) + '</em></li>'; }).join('') + '</ol>' : '<p class="nli__note">סמנו לפחות דבר אחד.</p>'; }
      root.querySelector('.hzp__chips').addEventListener('click', function (e) { var b = e.target.closest('button[data-k]'); if (!b) return; var k = b.getAttribute('data-k'); sel[k] = !sel[k]; b.setAttribute('aria-pressed', String(sel[k])); draw(); });
      draw();
    }
  });
})();
