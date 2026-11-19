/* NadLan Instruments · hazards v2 (HAD-670, Ben 3.11.2026 night: "the awesome map: a very extensive page, a 3D map where people
   see where they are, 4-5 complex tools with easy mobile UX, practical for choosing where to live"; Claude Design v109.0 HazardMap).
   Five tools of one family ('file' => 'hazards' in inc/hazards-tools.php), on data/hazards.json + data/hazards-lines.json
   (tools/instruments/build_hazards_data.py, every layer from an official open register or OpenStreetMap, read 3.11.2026):
   hzmap      the scope: an address (Nominatim, on submit only, cached) or "my location" (the browser) or a tap on the map; a radius;
              the layers; a tilted MapLibre map with 3D buildings; the report card of what is within the radius and how far;
   hzant      the antennas near the chosen point with their measured share of the health threshold (MoEP register);
   hzcompare  two addresses side by side, the same rows;
   hzcity     a city's figures: antennas (count, median and highest measured share), reporting plants, fuel stations;
   hzplan     what to check before buying or renting, who checks it, and what it costs where a price was published.
   The map shows distance, never exposure; no company, operator or plant name is shown (the no-names law).
   v2 (R13g): Hebrew and English. The page language comes from the engine (NadLanInstruments.lang); every visible string is L(he, en);
   the Hebrew values inside the data (sectors, city names, sources) are translated by the maps below, city names stay Hebrew. */
(function () {
  'use strict';
  if (!window.NadLanInstruments) return;
  var NLI = window.NadLanInstruments, F = NLI.fmt, esc = NLI.esc, EN = NLI.lang === 'en';
  function L(he, en) { return EN ? en : he; }
  var FINE = !!NLI.fine; // HAD-790: on a mouse the map has no Ctrl lock; NLI.wheelIntent decides scroll or zoom
  var ML = 'https://unpkg.com/maplibre-gl@4.7.1/dist/', RTL = 'https://unpkg.com/@mapbox/mapbox-gl-rtl-text@0.2.3/mapbox-gl-rtl-text.min.js';
  var STYLE = 'https://tiles.openfreemap.org/styles/positron';
  var LAY = [
    { k: 'ant', name: L('אנטנות סלולריות', 'Cellular antennas'), c: '#6a4fd6', on: true },
    { k: 'line', name: L('קווי מתח עליון', 'High-voltage lines'), c: '#0b8fb3', on: true },
    { k: 'sub', name: L('תחנות משנה', 'Substations'), c: '#0a5f78', on: true },
    { k: 'prtr', name: L('מפעלים מדווחים', 'Reporting plants'), c: '#c0392b', on: true },
    { k: 'fuel', name: L('תחנות דלק', 'Fuel stations'), c: '#e0701b', on: true },
    { k: 'plant', name: L('תחנות כוח', 'Power plants'), c: '#37474f', on: false },
    { k: 'soil', name: L('קרקע בחשד לזיהום', 'Suspected soil sites'), c: '#7c8a2a', on: false },
    { k: 'air', name: L('תחנות ניטור אוויר', 'Air monitoring stations'), c: '#2f86a8', on: false }
  ];
  var SOIL = [L('חשד לזיהום (לא אומת)', 'suspected contamination (not confirmed)'), L('בחקירה או בשיקום', 'under investigation or remediation'), L('סיים שיקום או אין סיכון', 'remediated or no risk')];
  var SITE = EN ? { ground: 'Ground mast', roof: 'Rooftop mast', indoor: 'Indoor small cell', small: 'Outdoor small cell', sting: 'Pole-top antenna', wifi: 'Wireless access point', slope: 'Wall-mounted antenna', other: 'Site' }
    : { ground: 'תורן קרקעי', roof: 'תורן על גג', indoor: 'אתר זעיר בתוך מבנה', small: 'אתר זעיר חיצוני', sting: 'אנטנת עוקץ', wifi: 'מתקן גישה אלחוטי', slope: 'אנטנה משתפלת', other: 'אתר' };
  var SECTOR = { 'פסולת ושפכים': 'waste and wastewater', 'חקלאות': 'agriculture', 'תעשייה מינרלית': 'mineral industry', 'תעשיות אנרגיה': 'energy', 'תעשייה כימית': 'chemicals',
    'תעשיית מזון ומשקאות': 'food and drink', 'מתכות': 'metals', 'אחר': 'other', 'גידול מקנה אינטנסיבי': 'intensive livestock' };
  var SRC_EN = { ant: 'Ministry of Environmental Protection, active cellular sites register (data.gov.il)', prtr: 'Ministry of Environmental Protection, Pollutant Release and Transfer Register (PRTR)',
    fuel: 'Ministry of Energy, fuel stations list', air: 'Ministry of Environmental Protection, air-quality monitoring stations (list updated 4.2024)',
    soil: 'Ministry of Environmental Protection, national contaminated-land database', osm: 'OpenStreetMap (community data, not official): power lines, substations, power plants' };
  function src(d, k) { return EN ? SRC_EN[k] : d.sources[k]; }
  function sector(x) { return EN ? (SECTOR[x] || 'other') : x; }
  var HOME = { pt: [34.7818, 32.0809], label: L('כיכר רבין, תל אביב-יפו (נקודת פתיחה לדוגמה)', 'Rabin Square, Tel Aviv-Yafo (a starting example)') };
  var S = window.NLHZ = window.NLHZ || { pt: HOME.pt, label: HOME.label, r: 250 };
  function m2(a, b) { var k = Math.cos(a[1] * Math.PI / 180); return Math.hypot((b[0] - a[0]) * 111320 * k, (b[1] - a[1]) * 110574); }
  function seg(p, a, b) { var k = Math.cos(p[1] * Math.PI / 180), ax = (a[0] - p[0]) * 111320 * k, ay = (a[1] - p[1]) * 110574, bx = (b[0] - p[0]) * 111320 * k, by = (b[1] - p[1]) * 110574;
    var dx = bx - ax, dy = by - ay, dd = dx * dx + dy * dy || 1e-9, t = Math.max(0, Math.min(1, -(ax * dx + ay * dy) / dd)); return Math.hypot(ax + t * dx, ay + t * dy); }
  function dist(n) { return n < 1000 ? F.num(Math.round(n / 10) * 10) + L(' מ׳', ' m') : F.num(n / 1000, 1) + L(' ק״מ', ' km'); }
  function pct(v) { return v == null ? '' : F.num(v, v < 10 ? 2 : 1) + '%'; }
  function rlab(r) { return r < 1000 ? r + L(' מ׳', ' m') : L('ק״מ', '1 km'); }
  function bus() { try { window.dispatchEvent(new CustomEvent('nlhz:pt')); } catch (e) { /* old browser */ } }
  var CACHE = {};
  // 1.72.580: Nominatim finds "Herzl 50, Haifa" but not "50 Herzl Street, Haifa": a second try drops the street word and puts the number after the name
  function tidy(q) {
    var t = q.replace(/(^|[\s,])(street|st\.?|road|rd\.?|avenue|ave\.?|boulevard|blvd\.?|רחוב|רח׳|רח')(?=[\s,]|$)/gi, '$1').replace(/\s+,/g, ',').replace(/\s+/g, ' ').trim();
    var m = t.match(/^(\d+[a-zA-Zא-ת]?)\s+([^,]+)(,.*)?$/);
    return m ? m[2].trim() + ' ' + m[1] + (m[3] || '') : t;
  }
  function look(q) {
    var u = 'https://nominatim.openstreetmap.org/search?format=jsonv2&countrycodes=il&limit=1&accept-language=' + (EN ? 'en' : 'he') + '&q=' + encodeURIComponent(q);
    return fetch(u, { headers: { Accept: 'application/json' } }).then(function (r) { return r.json(); }).then(function (j) { return j && j[0] ? j[0] : null; });
  }
  function geocode(q) {
    q = String(q || '').trim(); if (!q) return Promise.reject(new Error('empty'));
    try { CACHE = JSON.parse(localStorage.getItem('nlhz-geo') || '{}'); } catch (e) { /* storage blocked */ }
    var key = (EN ? 'en:' : '') + q;
    if (CACHE[key]) return Promise.resolve(CACHE[key]);
    var q2 = tidy(q);
    return look(q).then(function (h) { return h || (q2 !== q ? new Promise(function (r) { setTimeout(r, 1100); }).then(function () { return look(q2); }) : null); }).then(function (h) {  // one request a second (the usage policy)
      if (!h) throw new Error('none');
      var j = [h];
      var v = { pt: [+(+j[0].lon).toFixed(5), +(+j[0].lat).toFixed(5)], label: String(j[0].display_name || q).split(',').slice(0, 3).join(',').replace(/[\u2013\u2014]/g, '-') };  // OSM writes long dashes
      CACHE[key] = v; try { localStorage.setItem('nlhz-geo', JSON.stringify(CACHE)); } catch (e) { /* storage blocked */ }
      return v;
    });
  }
  /** everything within r metres of p, and the nearest item of each layer */
  function report(p, r, d, Lns) {
    var o = {};
    function pts(k, arr, extra) { var n = 0, best = null, inR = []; arr.forEach(function (a) { var x = m2(p, a); if (x <= r) { n++; inR.push([x, a]); } if (!best || x < best[0]) best = [x, a]; });
      inR.sort(function (u, v) { return u[0] - v[0]; }); o[k] = { n: n, near: best, inR: inR }; if (extra) extra(o[k]); }
    pts('ant', d.ant, function (z) { z.max = z.inR.reduce(function (m, q) { return Math.max(m, q[1][2] || 0); }, 0); });
    pts('pend', d.pend); pts('sub', d.sub); pts('prtr', d.prtr); pts('fuel', d.fuel); pts('plant', d.plant); pts('soil', d.soil); pts('air', d.air);
    var lb = null; (Lns ? Lns.lines : []).forEach(function (l) { for (var i = 1; i < l.c.length; i++) { var x = seg(p, l.c[i - 1], l.c[i]); if (!lb || x < lb[0]) lb = [x, l.kv]; } });
    o.line = { n: lb && lb[0] <= r ? 1 : 0, near: lb };
    return o;
  }
  var NONE = L('אין ברדיוס', 'None in the radius');
  function rows(o) {
    function row(k, title, body, val, none) { var l = LAY.filter(function (x) { return x.k === k; })[0];
      return '<div class="hzr' + (none ? ' none' : '') + '"><i style="background:' + l.c + '"></i><div><b>' + esc(title) + '</b><span>' + esc(body) + '</span></div><em>' + esc(val) + '</em></div>'; }
    var a = o.ant, h = '', q0;
    if (a.n) { q0 = a.inR[0][1];
      h += row('ant', a.n === 1 ? L('אנטנה סלולרית אחת', 'One cellular antenna') : F.num(a.n) + L(' אנטנות סלולריות', ' cellular antennas'),
        L('הקרובה ', 'The nearest is ') + dist(a.inR[0][0]) + ', ' + (SITE[q0[3]] || SITE.other) + L('. הקרינה הגבוהה שנמדדה בה: ', '. Its highest measured result: ') + pct(q0[2]) + L(' מסף הבריאות', ' of the health threshold')
          + (a.n > 1 ? L('; הגבוהה ברדיוס: ', '; the highest in the radius: ') + pct(a.max) : '') + '.', dist(a.inR[0][0])); }
    else h += row('ant', L('אנטנות סלולריות', 'Cellular antennas'), L('אין ברדיוס. הקרובה ', 'None in the radius. The nearest is ') + dist(a.near[0]) + L(', ובה נמדדו ', ', measured at ') + pct(a.near[1][2]) + L(' מסף הבריאות.', ' of the health threshold.'), NONE, true);
    if (o.pend.n) h += row('ant', F.num(o.pend.n) + L(' בקשות להיתר לאנטנה', ' pending antenna permit requests'), L('בקשות שממתינות להיתר הקמה ברדיוס. אפשר לבקש לראות את הבקשה ולהגיש התנגדות.', 'Requests in the radius waiting for a construction permit. You can ask to see a request and file an objection.'), dist(o.pend.inR[0][0]));
    var ln = o.line.near;
    if (ln) h += row('line', L('קו מתח עליון', 'High-voltage line') + (ln[1] ? ' ' + ln[1] + L(' ק״ו', ' kV') : ''), o.line.n ? L('עובר ברדיוס, ', 'Runs inside the radius, ') + dist(ln[0]) + L(' מהנקודה.', ' from the point.') : L('מחוץ לרדיוס. הקרוב ', 'Outside the radius. The nearest is ') + dist(ln[0]) + '.', dist(ln[0]), !o.line.n);
    [['sub', L('תחנות משנה', 'substations'), L('תחנת משנה אחת', 'One substation')], ['prtr', L('מפעלים שמדווחים על פליטות (מפל״ס)', 'plants that report emissions (PRTR)'), L('מפעל מדווח אחד', 'One reporting plant')],
     ['fuel', L('תחנות דלק', 'fuel stations'), L('תחנת דלק אחת', 'One fuel station')], ['plant', L('תחנות כוח', 'power plants'), L('תחנת כוח אחת', 'One power plant')],
     ['soil', L('אתרי קרקע במאגר הלאומי', 'sites in the national soil database'), L('אתר קרקע אחד', 'One soil site')]].forEach(function (q) {
      var z = o[q[0]], cap = q[1].charAt(0).toUpperCase() + q[1].slice(1);
      if (z.n) {
        var x = z.inR[0][1], body = L('הקרוב ', 'The nearest is ') + dist(z.inR[0][0]) + (q[0] === 'prtr' ? L(', ענף: ', ', sector: ') + sector(x[2]) : q[0] === 'soil' ? ', ' + SOIL[x[2]] : '') + '.';
        h += row(q[0], z.n === 1 ? q[2] : F.num(z.n) + ' ' + q[1], body, dist(z.inR[0][0]));
      } else if (z.near) h += row(q[0], EN ? cap : q[1], L('אין ברדיוס. הקרוב ', 'None in the radius. The nearest is ') + dist(z.near[0]) + '.', NONE, true);
    });
    if (o.air.near) h += row('air', L('תחנת ניטור אוויר', 'Air monitoring station'), L('התחנה הקרובה ', 'The nearest station is ') + dist(o.air.near[0]) + L('. הערכים העדכניים מתפרסמים באתר המשרד להגנת הסביבה.', ' away. Its current values are published by the Ministry of Environmental Protection.'), dist(o.air.near[0]), true);
    return h;
  }
  var NOTE = L('אין סימון במפה לא אומר שאין מפגע. המפה מציגה מרחק, לא חשיפה, ורק מה שפורסם במאגרים: חדרי שנאים, צנרת דלק, רעש מטוסים וערכי זיהום אוויר בזמן אמת לא פורסמו כנתונים פתוחים. קרינה בתוך דירה מודדים רק במדידה של מודד בעל היתר.',
    'No mark on the map does not mean no hazard. The map shows distance, not exposure, and only what the registers publish: transformer rooms, fuel pipelines, aircraft noise and live air-pollution values are not published as open data. Radiation inside a flat is known only from a measurement by a licensed surveyor.');
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
      root.innerHTML = '<div class="nli__panel hzm"><p class="nli__kicker">' + esc(L('מפה · מפגעים סביבתיים', 'Map · Environmental hazards')) + '</p><h2 class="nli__title">' + esc(L('מה יש סביב הבית', 'What is around the home')) + '</h2>'
        + '<p class="nli__lede">' + esc(L('מקלידים כתובת, או נוגעים ב"המיקום שלי", או במקום כלשהו במפה. בוחרים רדיוס, ורואים כל אנטנה, קו מתח, תחנת משנה, מפעל מדווח ותחנת דלק סביב הנקודה, עם המרחק והערך הרשמי.',
          'Type an address, tap "My location", or tap anywhere on the map. Choose a radius and see every antenna, power line, substation, reporting plant and fuel station around the point, with the distance and the official value.')) + '</p>'
        + '<div class="hzm__scope"><form class="hzm__find" novalidate><input type="search" enterkeyhint="search" placeholder="' + esc(L('רחוב, מספר ועיר', 'Street, number and city')) + '" aria-label="' + esc(L('כתובת', 'Address')) + '" autocomplete="street-address"><button type="submit" class="hzm__go">' + esc(L('בדיקה', 'Check')) + '</button>'
        + '<button type="button" class="hzm__loc" aria-label="' + esc(L('המיקום שלי', 'My location')) + '"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="8" cy="8" r="4.5"/><path d="M8 0v3M8 13v3M0 8h3M13 8h3"/></svg>' + esc(L('המיקום שלי', 'My location')) + '</button></form>'
        + '<p class="hzm__where" aria-live="polite"></p>'
        + '<div class="hzm__rad" role="group" aria-label="' + esc(L('רדיוס', 'Radius')) + '">' + [100, 250, 500, 1000].map(function (r) { return '<button type="button" data-r="' + r + '" aria-pressed="' + (S.r === r) + '">' + esc(rlab(r)) + '</button>'; }).join('') + '</div>'
        + '<div class="hzm__layers" role="group" aria-label="' + esc(L('מה להציג', 'What to show')) + '">' + LAY.map(function (l) { return '<button type="button" data-l="' + l.k + '" aria-pressed="' + l.on + '"><i style="background:' + l.c + '"></i>' + esc(l.name) + '</button>'; }).join('') + '</div>'
        + '<div class="hzm__map" role="region" aria-label="' + esc(L('מפת המפגעים סביב הנקודה', 'Map of the hazards around the point')) + '"><p class="nls__wait">' + esc(L('טוען את המפה…', 'Loading the map…')) + '</p></div>'
        + '<div class="hzm__bar"><button type="button" class="hzm__3d" aria-pressed="true">' + esc(L('מבט תלת־ממדי', '3D view')) + '</button></div></div>'
        + '<div class="hzm__rep" aria-live="polite"></div><p class="nli__note">' + esc(NOTE) + '</p>'
        + '<p class="nli__src">' + esc(L('מקורות: ', 'Sources: ') + ['ant', 'prtr', 'fuel', 'soil', 'air', 'osm'].map(function (k) { return src(d, k); }).join('; ') + L('. נקראו ', '. Read ') + F.date(d.read)
          + L('. הכתובת: OpenStreetMap Nominatim. המפה: © OpenStreetMap, OpenFreeMap.', '. Addresses: OpenStreetMap Nominatim. Map: © OpenStreetMap, OpenFreeMap.')) + '</p></div>';
      var rep = root.querySelector('.hzm__rep'), where = root.querySelector('.hzm__where'), inp = root.querySelector('input'), mapEl = root.querySelector('.hzm__map');
      function draw(fly) {
        var o = report(S.pt, S.r, d, Ln);
        where.textContent = L('הנקודה: ', 'The point: ') + S.label + L(' · רדיוס ', ' · radius ') + rlab(S.r);
        rep.innerHTML = '<p class="hzm__k">' + esc(L('דוח סביבה · ', 'Environment report · ') + S.label) + '</p>' + rows(o);
        if (map && map.getSource('hz-ring')) {
          map.getSource('hz-ring').setData(ring(S.pt, S.r)); map.getSource('hz-me').setData(fcPts([S.pt]));
          var lab = [];
          o.ant.inR.slice(0, 4).forEach(function (q) { lab.push([q[1][0], q[1][1], L('אנטנה', 'Antenna') + ' · ' + dist(q[0]) + ' · ' + pct(q[1][2])]); });
          [['sub', L('תחנת משנה', 'Substation')], ['prtr', L('מפעל מדווח', 'Reporting plant')], ['fuel', L('תחנת דלק', 'Fuel station')], ['plant', L('תחנת כוח', 'Power plant')], ['soil', L('אתר קרקע', 'Soil site')]].forEach(function (q) {
            if (on[q[0]]) o[q[0]].inR.slice(0, 2).forEach(function (z) { lab.push([z[1][0], z[1][1], q[1] + ' · ' + dist(z[0])]); }); });
          map.getSource('hz-lab').setData(fcPts(lab, function (a) { return { t: a[2] }; }));
          if (fly) { var k = Math.cos(S.pt[1] * Math.PI / 180), dx = S.r * 1.25 / (111320 * k), dy = S.r * 1.25 / 110574;
            map.fitBounds([[S.pt[0] - dx, S.pt[1] - dy], [S.pt[0] + dx, S.pt[1] + dy]], { padding: phone ? 16 : 40, duration: 900, pitch: map.getPitch() }); }
        }
        bus();
      }
      function set(pt, label, fly) { S.pt = pt; S.label = label; draw(fly !== false); }
      root.querySelector('form').addEventListener('submit', function (e) { e.preventDefault(); var q = inp.value.trim(); if (!q) return;
        where.textContent = L('מחפש את הכתובת…', 'Looking up the address…');
        geocode(q).then(function (v) { set(v.pt, v.label); }, function () { where.textContent = L('לא מצאנו את הכתובת. נסו רחוב, מספר ועיר, או געו במפה.', 'Address not found. Try street, number and city, or tap the map.'); }); });
      root.querySelector('.hzm__loc').addEventListener('click', function () {
        if (!navigator.geolocation) { where.textContent = L('הדפדפן לא מאפשר מיקום. הקלידו כתובת או געו במפה.', 'Your browser does not share location. Type an address or tap the map.'); return; }
        where.textContent = L('מאתר את המיקום שלכם…', 'Finding your location…');
        navigator.geolocation.getCurrentPosition(function (g) { set([+g.coords.longitude.toFixed(5), +g.coords.latitude.toFixed(5)], L('המיקום שלכם', 'Your location')); },
          function () { where.textContent = L('המיקום לא אושר. הקלידו כתובת או געו במפה.', 'Location was not allowed. Type an address or tap the map.'); }, { enableHighAccuracy: true, timeout: 10000 });
      });
      root.querySelector('.hzm__rad').addEventListener('click', function (e) { var b = e.target.closest('button[data-r]'); if (!b) return; S.r = +b.getAttribute('data-r');
        [].forEach.call(this.children, function (x) { x.setAttribute('aria-pressed', String(x === b)); }); draw(true); });
      root.querySelector('.hzm__layers').addEventListener('click', function (e) { var b = e.target.closest('button[data-l]'); if (!b) return; var k = b.getAttribute('data-l'); on[k] = !on[k];
        b.setAttribute('aria-pressed', String(on[k])); if (map && map.getLayer('hz-' + k)) map.setLayoutProperty('hz-' + k, 'visibility', on[k] ? 'visible' : 'none'); draw(false); });
      draw(false);
      loadML(function (err) {
        if (err || !window.maplibregl) { mapEl.innerHTML = '<p class="nls__wait">' + esc(L('המפה לא נטענה. הדוח למטה מחושב בכל זאת.', 'The map did not load. The report below is still calculated.')) + '</p>'; return; }
        var gl = window.maplibregl, k = Math.cos(S.pt[1] * Math.PI / 180), dx = S.r * 1.25 / (111320 * k), dy = S.r * 1.25 / 110574;
        map = new gl.Map({ container: mapEl, style: STYLE, bounds: [[S.pt[0] - dx, S.pt[1] - dy], [S.pt[0] + dx, S.pt[1] + dy]], pitch: phone ? 45 : 55, bearing: -18, maxPitch: 70, cooperativeGestures: !FINE, attributionControl: { compact: true } });
        map.addControl(new gl.NavigationControl({ showCompass: true }), EN ? 'top-right' : 'top-left');
        if (FINE && NLI.wheelIntent) NLI.wheelIntent(map, mapEl, EN);
        map.on('load', function () {
          var w = mapEl.querySelector('.nls__wait'); if (w) w.remove();
          if (map.getSource('openmaptiles')) map.addLayer({ id: 'hz-3d', type: 'fill-extrusion', source: 'openmaptiles', 'source-layer': 'building', minzoom: 13,
            paint: { 'fill-extrusion-color': '#d9e1e7', 'fill-extrusion-height': ['coalesce', ['get', 'render_height'], 9], 'fill-extrusion-base': ['coalesce', ['get', 'render_min_height'], 0], 'fill-extrusion-opacity': 0.85 } });
          map.addSource('hz-line', { type: 'geojson', data: { type: 'FeatureCollection', features: Ln.lines.map(function (l) { return { type: 'Feature', properties: { kv: l.kv }, geometry: { type: 'LineString', coordinates: l.c } }; }) } });
          map.addLayer({ id: 'hz-line', type: 'line', source: 'hz-line', paint: { 'line-color': '#0b8fb3', 'line-width': ['match', ['get', 'kv'], 400, 3.2, 2.2], 'line-dasharray': [3, 1.6] } });
          [['ant', d.ant, 3.2], ['sub', d.sub, 5], ['prtr', d.prtr, 4.5], ['fuel', d.fuel, 4.5], ['plant', d.plant, 6], ['soil', d.soil.filter(function (s) { return s[2] < 2; }), 3.5], ['air', d.air, 5]].forEach(function (q) {
            var l = LAY.filter(function (x) { return x.k === q[0]; })[0];
            map.addSource('hz-' + q[0], { type: 'geojson', data: fcPts(q[1]) });
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
          map.on('click', function (e) { if (e.defaultPrevented) return; set([+e.lngLat.lng.toFixed(5), +e.lngLat.lat.toFixed(5)], L('הנקודה שבחרתם במפה', 'The point you chose on the map'), false); });
          draw(false);
        });
        var b3 = root.querySelector('.hzm__3d');
        b3.addEventListener('click', function () { var o2 = b3.getAttribute('aria-pressed') !== 'true'; b3.setAttribute('aria-pressed', String(o2)); map.easeTo({ pitch: o2 ? (phone ? 45 : 55) : 0, bearing: o2 ? -18 : 0, duration: 700 }); });
      });
    }
  });

  /* ---------------------------------------------------------------- hzant */
  function med(a) { var v = a.map(function (x) { return x[2]; }).filter(function (x) { return x != null; }).sort(function (p, q) { return p - q; }); return v[Math.floor(v.length / 2)]; }
  function maxp(a) { return a.reduce(function (m, x) { return Math.max(m, x[2] || 0); }, 0); }
  NLI.register('hzant', {
    custom: function (root, data) {
      var d = data.hz;
      root.innerHTML = '<div class="nli__panel hza"><p class="nli__kicker">' + esc(L('בדיקה · אנטנות סלולריות', 'Check · Cellular antennas')) + '</p><h2 class="nli__title">' + esc(L('כמה קרינה נמדדה באנטנות ליד הבית', 'How much radiation was measured at the antennas near the home')) + '</h2>'
        + '<p class="nli__lede">' + esc(L('לכל אנטנה פעילה המשרד להגנת הסביבה מפרסם את התוצאה הגבוהה שנמדדה בה, באחוזים מסף הבריאות. כאן עשר האנטנות הקרובות לנקודה שבחרתם במפה.',
          'For every active antenna the Ministry of Environmental Protection publishes its highest measured result, as a percentage of the health threshold. Here are the ten antennas nearest to the point you chose on the map.')) + '</p><div class="hza__out" aria-live="polite"></div>'
        + '<p class="nli__note">' + esc(L('הסף בישראל: 10% מהמגבלה הבינלאומית במקום שבו שוהים זמן רב, ו־30% במקום מעבר. בכל המאגר החציון הוא ', "Israel's threshold: 10% of the international limit where people stay for long periods, and 30% where they only pass. Across the register the median is ")
          + pct(med(d.ant)) + L(' והערך הגבוה ', ' and the highest value is ') + pct(maxp(d.ant)) + L('. שם החברה המפעילה לא מוצג.', '. The operator\'s name is not shown.')) + '</p>'
        + '<p class="nli__src">' + esc(L('מקור: ', 'Source: ') + src(d, 'ant') + L(', נקרא ', ', read ') + F.date(d.read) + '.') + '</p></div>';
      var out = root.querySelector('.hza__out');
      function draw() { var Lx = d.ant.map(function (a) { return [m2(S.pt, a), a]; }).sort(function (u, v) { return u[0] - v[0]; }).slice(0, 10);
        out.innerHTML = '<p class="hzm__k">' + esc(L('ליד: ', 'Near: ') + S.label) + '</p><div class="nli__tw"><table><thead><tr><th>' + esc(L('סוג האתר', 'Site type')) + '</th><th class="n">' + esc(L('מרחק', 'Distance')) + '</th><th class="n">' + esc(L('מסף הבריאות', 'Of the threshold')) + '</th><th class="n">' + esc(L('בדיקה אחרונה', 'Last check')) + '</th></tr></thead><tbody>'
          + Lx.map(function (q) { var a = q[1], w = Math.max(2, Math.round((a[2] || 0) / 30 * 100));
            return '<tr><td>' + esc(SITE[a[3]] || SITE.other) + '<i class="hza__bar" style="width:' + w + '%"></i></td><td class="n">' + dist(q[0]) + '</td><td class="n">' + pct(a[2]) + '</td><td class="n">' + (a[4] || '') + '</td></tr>'; }).join('') + '</tbody></table></div>'; }
      window.addEventListener('nlhz:pt', draw); draw();
    }
  });

  /* ---------------------------------------------------------------- hzcompare */
  NLI.register('hzcompare', {
    custom: function (root, data) {
      var d = data.hz, Ln = data.hzl, A = null;
      root.innerHTML = '<div class="nli__panel hzc"><p class="nli__kicker">' + esc(L('השוואה · שתי כתובות', 'Compare · Two addresses')) + '</p><h2 class="nli__title">' + esc(L('איפה לגור: שתי כתובות זו מול זו', 'Where to live: two addresses side by side')) + '</h2>'
        + '<p class="nli__lede">' + esc(L('מקלידים שתי כתובות ורואים לכל אחת מה יש ברדיוס של 250 מטר והקרוב מכל סוג.', 'Type two addresses to see, for each, what is within 250 metres and the nearest of each kind.')) + '</p>'
        + '<form class="hzc__f" novalidate><input type="search" name="a" placeholder="' + esc(L('כתובת ראשונה', 'First address')) + '" aria-label="' + esc(L('כתובת ראשונה', 'First address')) + '"><input type="search" name="b" placeholder="' + esc(L('כתובת שנייה', 'Second address')) + '" aria-label="' + esc(L('כתובת שנייה', 'Second address')) + '"><button type="submit" class="hzm__go">' + esc(L('השוואה', 'Compare')) + '</button></form>'
        + '<div class="hzc__out" aria-live="polite"></div><p class="nli__note">' + esc(NOTE) + '</p></div>';
      var out = root.querySelector('.hzc__out'), fm = root.querySelector('form');
      function col(v) { return '<div class="hzc__col"><p class="hzm__k">' + esc(v.label) + '</p>' + rows(report(v.pt, 250, d, Ln)) + '</div>'; }
      fm.addEventListener('submit', function (e) { e.preventDefault(); var qa = fm.a.value.trim(), qb = fm.b.value.trim();
        if (!qa || !qb) { out.innerHTML = '<p class="nli__note">' + esc(L('הקלידו שתי כתובות.', 'Type two addresses.')) + '</p>'; return; }
        out.innerHTML = '<p class="nli__note">' + esc(L('מחפש את הכתובות…', 'Looking up the addresses…')) + '</p>';
        geocode(qa).then(function (a) { A = a; return new Promise(function (r) { setTimeout(r, 1100); }); }).then(function () { return geocode(qb); }).then(function (b) { out.innerHTML = '<div class="hzc__grid">' + col(A) + col(b) + '</div>'; },
          function () { out.innerHTML = '<p class="nli__note">' + esc(L('אחת הכתובות לא נמצאה. נסו רחוב, מספר ועיר.', 'One of the addresses was not found. Try street, number and city.')) + '</p>'; }); });
    }
  });

  /* ---------------------------------------------------------------- hzcity */
  NLI.register('hzcity', {
    custom: function (root, data) {
      var C = data.hz.cities, names = Object.keys(C);
      root.innerHTML = '<div class="nli__panel hzy"><p class="nli__kicker">' + esc(L('נתונים · לפי עיר', 'Data · By town')) + '</p><h2 class="nli__title">' + esc(L('אנטנות, מפעלים ותחנות דלק בעיר שלכם', 'Antennas, plants and fuel stations in your town')) + '</h2>'
        + '<p class="nli__lede">' + esc(L('בוחרים יישוב ורואים כמה אנטנות סלולריות פעילות רשומות בו, מה הקרינה החציונית והגבוהה שנמדדה בהן, כמה מפעלים מדווחים על פליטות וכמה תחנות דלק.',
          'Choose a town to see how many active cellular antennas it lists, the median and highest radiation measured at them, how many plants report emissions and how many fuel stations it has.')) + '</p>'
        + '<label class="nls__q"><span>' + esc(L('יישוב', 'Town (its Hebrew name)')) + '</span><input type="search" list="hzy-list" placeholder="' + esc(L('למשל חיפה או רמת גן', 'e.g. חיפה or רמת גן')) + '" autocomplete="off" dir="rtl"></label><datalist id="hzy-list">' + names.map(function (n) { return '<option value="' + esc(n) + '">'; }).join('') + '</datalist>'
        + '<div class="hzy__out" aria-live="polite"></div>'
        + '<details class="nli__table"><summary>' + esc(L('20 היישובים עם מספר האנטנות הגדול', 'The 20 towns with the most antennas')) + '</summary><div class="nli__tw"><table><thead><tr><th>' + esc(L('יישוב', 'Town')) + '</th><th class="n">' + esc(L('אנטנות', 'Antennas')) + '</th><th class="n">' + esc(L('חציון', 'Median')) + '</th><th class="n">' + esc(L('הגבוה', 'Highest')) + '</th><th class="n">' + esc(L('מפעלים', 'Plants')) + '</th><th class="n">' + esc(L('דלק', 'Fuel')) + '</th></tr></thead><tbody>'
        + names.slice(0, 20).map(function (n) { var v = C[n]; return '<tr><td>' + esc(n) + '</td><td class="n">' + F.num(v[0]) + '</td><td class="n">' + pct(v[1]) + '</td><td class="n">' + pct(v[2]) + '</td><td class="n">' + v[3] + '</td><td class="n">' + v[4] + '</td></tr>'; }).join('') + '</tbody></table></div></details>'
        + '<p class="nli__src">' + esc(L('לפי היישוב הרשום במאגרים. חציון רק ליישוב עם 5 אנטנות ומעלה. מקורות: ', 'By the town written in the registers. A median only for a town with 5 antennas or more. Sources: ') + ['ant', 'prtr', 'fuel'].map(function (k) { return src(data.hz, k); }).join('; ') + '.') + '</p></div>';
      var inp = root.querySelector('input'), out = root.querySelector('.hzy__out');
      function draw() { var q = inp.value.trim(), n = C[q] ? q : names.filter(function (x) { return q && x.indexOf(q) === 0; })[0];
        if (!n) { out.innerHTML = q ? '<p class="nli__note">' + esc(L('היישוב לא נמצא ברשימה.', 'That town is not in the list.')) + '</p>' : ''; return; } var v = C[n];
        out.innerHTML = '<div class="hzy__grid"><div><b>' + F.num(v[0]) + '</b><span>' + esc(L('אנטנות סלולריות פעילות', 'Active cellular antennas')) + '</span></div><div><b>' + (v[1] != null ? pct(v[1]) : esc(L('לא חושב', 'n/a'))) + '</b><span>' + esc(L('הקרינה החציונית מסף הבריאות', 'Median radiation, of the threshold')) + '</span></div>'
          + '<div><b>' + (v[2] != null ? pct(v[2]) : '') + '</b><span>' + esc(L('הערך הגבוה שנמדד', 'Highest measured')) + '</span></div><div><b>' + v[3] + '</b><span>' + esc(L('מפעלים מדווחים', 'Reporting plants')) + '</span></div><div><b>' + v[4] + '</b><span>' + esc(L('תחנות דלק', 'Fuel stations')) + '</span></div></div><p class="hzm__k">' + esc(n) + '</p>'; }
      inp.addEventListener('input', draw); inp.addEventListener('change', draw); inp.value = names[0]; draw();
    }
  });

  /* ---------------------------------------------------------------- hzplan */
  var RAD_PRICE = L('כ־500 עד 650 ₪ לדירה (מחירון מסחרי שפורסם)', 'About NIS 500 to 650 per flat (a published commercial price list)'), NOP = L('מחיר לא פורסם', 'Price not published');
  var PLAN = [
    { k: 'ant', label: L('אנטנה סלולרית קרובה', 'A cellular antenna nearby'), who: L('מודד קרינה בעל היתר מהמשרד להגנת הסביבה', 'A radiation surveyor licensed by the Ministry of Environmental Protection'), what: L('מודד קרינה בתדרי רדיו בתוך הדירה, ליד חלונות ומרפסות, ונותן דוח.', 'Measures radio-frequency radiation inside the flat, by windows and balconies, and gives a report.'), price: RAD_PRICE },
    { k: 'elf', label: L('קו מתח, תחנת משנה או חדר שנאים', 'A power line, substation or transformer room'), who: L('מודד קרינה בעל היתר לשדות מגנטיים', 'A radiation surveyor licensed for magnetic fields'), what: L('מודד שדה מגנטי בתדר נמוך במילי־גאוס, בשעות צריכה שונות. היעד שהמשרד להגנת הסביבה מציין: 4 מילי־גאוס בממוצע יומי ביום שיא.', 'Measures the low-frequency magnetic field in milligauss at different hours of demand. The target the Ministry of Environmental Protection cites: 4 mG as a daily average on a peak day.'), price: RAD_PRICE },
    { k: 'noise', label: L('רעש מכביש, רכבת או מטוסים', 'Noise from a road, railway or aircraft'), who: L('יועץ אקוסטי', 'An acoustic consultant'), what: L('מודד רעש ביום ובלילה ומציע בידוד: חלונות, איטום, וילונות.', 'Measures noise by day and night and suggests insulation: windows, sealing, curtains.'), price: NOP },
    { k: 'air', label: L('מפעל, כביש ראשי או תחנת כוח', 'A plant, a main road or a power plant'), who: L('יועץ סביבתי', 'An environmental consultant'), what: L('בודק דיווחי פליטות, תחנות ניטור ותכניות באזור, ומסביר מה הם אומרים.', 'Reads emission reports, monitoring stations and plans for the area, and explains what they mean.'), price: NOP },
    { k: 'soil', label: L('תחנת דלק או אתר קרקע במאגר', 'A fuel station or a site in the soil database'), who: L('יועץ סביבתי, ובקנייה גם עורך דין', 'An environmental consultant, and for a purchase a lawyer too'), what: L('בודק את סטטוס האתר במאגר הלאומי ואת התכניות, ומה זה אומר על הבנייה.', "Checks the site's status in the national database and the plans, and what it means for building."), price: NOP },
    { k: 'home', label: L('מצב הדירה עצמה', 'The state of the flat itself'), who: L('בודק בית', 'A home inspector'), what: L('בודק רטיבות, חשמל, אינסטלציה וליקויי בנייה, ונותן דוח.', 'Checks damp, electrics, plumbing and building defects, and gives a report.'), price: L('כ־1,700 עד 1,800 ₪ בממוצע (מחירון מסחרי שפורסם)', 'About NIS 1,700 to 1,800 on average (a published commercial price list)') },
    { k: 'plan', label: L('אנטנה או מתקן שעומדים לקום', 'An antenna or facility about to be built'), who: L('עורך דין לתכנון ובנייה', 'A planning and building lawyer'), what: L('בודק בקשות להיתר ותכניות בוועדה המקומית, ומגיש התנגדות בזמן.', 'Checks permit requests and plans at the local committee and files an objection in time.'), price: NOP }
  ];
  NLI.register('hzplan', {
    custom: function (root) {
      var sel = { ant: true, home: true };
      root.innerHTML = '<div class="nli__panel hzp"><p class="nli__kicker">' + esc(L('תכנון · לפני שקונים או שוכרים', 'Plan · Before you buy or rent')) + '</p><h2 class="nli__title">' + esc(L('מה לבדוק, מי בודק וכמה זה עולה', 'What to check, who checks it, and what it costs')) + '</h2>'
        + '<p class="nli__lede">' + esc(L('מסמנים מה יש ליד הדירה ומקבלים תכנית בדיקה: מי עושה כל בדיקה, מה הוא בודק, והמחיר במקום שבו פורסם.', 'Mark what is near the flat and get a check plan: who does each check, what they look at, and the price where one was published.')) + '</p>'
        + '<div class="nls__chips hzp__chips" role="group">' + PLAN.map(function (p) { return '<button type="button" data-k="' + p.k + '" aria-pressed="' + !!sel[p.k] + '">' + esc(p.label) + '</button>'; }).join('') + '</div>'
        + '<div class="hzp__out" aria-live="polite"></div><p class="nli__note">' + esc(L('המחירים לקוחים ממחירונים מסחריים שפורסמו, כדי לתת סדר גודל. בקשו כמה הצעות, ובדקו שלמודד יש היתר בתוקף מהמשרד להגנת הסביבה.',
          'The prices come from published commercial price lists, to give an order of magnitude. Ask for several quotes, and check that the surveyor holds a valid licence from the Ministry of Environmental Protection.')) + '</p></div>';
      var out = root.querySelector('.hzp__out');
      function draw() { var Lp = PLAN.filter(function (p) { return sel[p.k]; });
        out.innerHTML = Lp.length ? '<ol>' + Lp.map(function (p) { return '<li><b>' + esc(p.who) + '</b> · ' + esc(p.label) + '<br>' + esc(p.what) + ' <em>' + esc(p.price) + '</em></li>'; }).join('') + '</ol>' : '<p class="nli__note">' + esc(L('סמנו לפחות דבר אחד.', 'Mark at least one thing.')) + '</p>'; }
      root.querySelector('.hzp__chips').addEventListener('click', function (e) { var b = e.target.closest('button[data-k]'); if (!b) return; var k = b.getAttribute('data-k'); sel[k] = !sel[k]; b.setAttribute('aria-pressed', String(sel[k])); draw(); });
      draw();
    }
  });
})();
