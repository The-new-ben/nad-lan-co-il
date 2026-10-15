/* NadLan Instruments · soilmap v1 (HAD-534, Ben 15.10.2026): the Sde Dov soil map. Every plot of the district (municipal GIS
   layer 837), the plots with a published soil survey coloured by how many times the PFOS value passed the direct-contact
   threshold, every borehole in its place, the plots on the "nine plots" list and the developers' own statements, each with
   its source. A 3D city view (MapLibre GL + OpenFreeMap tiles + OSM buildings), one tap on a plot, a project or a chip opens
   the plot card; any plot number of the district can be checked. Data: data/sde-dov-soil.json, built by
   tools/instruments/build_soil_data.py from docs/research/2026-10-15-sde-dov-soil/. Pure helpers in NLSX for unit checks. */
(function () {
  'use strict';
  var ML = 'https://unpkg.com/maplibre-gl@4.7.1/dist/', RTL = 'https://unpkg.com/@mapbox/mapbox-gl-rtl-text@0.2.3/mapbox-gl-rtl-text.min.js';
  var STYLE = 'https://tiles.openfreemap.org/styles/positron';
  var BIN = [[100, '#8E1238', 'פי 100 ומעלה'], [10, '#C42550', 'פי 10 עד 100'], [1, '#E58CA4', 'עד פי 10'], [0, '#8FA6B2', 'מתחת לסף']];
  var ST = { published_report: 'דו"ח פורסם: נמצאה חריגה', findings_reported_no_report: 'ברשימת המגרשים עם ממצאים · הדו"ח לא פורסם',
    developer_reported_no_exceedance: 'לפי היזם: לא נמצאו חריגות', under_testing_per_developer: 'לפי היזם: בבדיקה' };
  var DEV = { '303': 'מבנה נדל"ן (זכתה במכרז רמ"י, דצמבר 2024)', '301': 'לא אומת', '2255': 'גינדי ישראל (לפי פרסום בפאנדר)', '2270': 'קבוצת חג\'ג\' (לפי פרסום בפאנדר)',
    '2206': 'גינדי ישראל (לפי פרסום בפאנדר)', '106': 'שיכון ובינוי', '2102': 'פרשקובסקי', '2203': 'פרשקובסקי', '2207': 'פרשקובסקי', '107': 'דמרי', '2701': 'שטח ציבורי פתוח', '822': 'דרך' };
  var NOTE = {
    '106': 'לפי דיווח החברה לבורסה (מרץ 2026): סקר מקיף בלי חריגות, והמשרד הודיע שהוא מאמץ את הממצאים. המגרש מופיע ברשימת תשעת המגרשים עם ממצאים כפי שפורסמה ביולי 2026. הדו"ח עצמו לא פורסם במאגר.',
    '2102': 'לפי החברה (יולי 2026): הבדיקות הושלמו, לא נמצא זיהום, והמשרד אישר. המגרש מופיע ברשימת תשעת המגרשים עם ממצאים. הדו"ח עצמו לא פורסם במאגר.',
    '2203': 'לפי החברה (יולי 2026): המגרש בבדיקה אחרי הדיגום.',
    '2207': 'לפי החברה (יולי 2026): בבדיקה אחרי הדיגום. המגרש מופיע ברשימת תשעת המגרשים עם ממצאים. הדו"ח לא פורסם במאגר.',
    '103': 'המגרש מופיע ברשימת תשעת המגרשים עם ממצאים, לפי מכתב המשרד להגנת הסביבה כפי שפורסם ביולי 2026. הדו"ח לא פורסם במאגר.',
    '105': 'המגרש מופיע ברשימת תשעת המגרשים עם ממצאים, לפי מכתב המשרד להגנת הסביבה כפי שפורסם ביולי 2026. הדו"ח לא פורסם במאגר.',
    '107': 'המגרש מופיע ברשימת תשעת המגרשים עם ממצאים. לפי דמרי (יולי 2026): יותר מ־98% מהדגימות תקינות, והקרקע עם החריגות פונתה במלואה. הדו"ח לא פורסם במאגר.',
    '2255': 'לפי שכבת המגרשים של העירייה, 9 מתוך 12 הקידוחים של הדו"ח נמצאים בתחום מגרש 2227 הסמוך. הקידוחים מוצגים במקום שמופיע בדו"ח.'
  };
  var PAGE = { '107': ['דמרי ים', '/projects/dimri-yama-sde-dov/'], '103': ['אוטופיה', '/projects/utopia-sde-dov/'], '2206': ['גינדי ווג', '/projects/gindi-vogue-sde-dov/'], '106': ['שיכון ובינוי שדה דב', '/projects/shikun-binui-sde-dov/'] };
  function bin(x) { for (var i = 0; i < BIN.length; i++) if (x > BIN[i][0] || (BIN[i][0] === 0)) return BIN[i]; return BIN[3]; }
  function dist(a, b) { var R = 6371000, r = Math.PI / 180, dLa = (b[1] - a[1]) * r, dLo = (b[0] - a[0]) * r;
    var h = Math.sin(dLa / 2) * Math.sin(dLa / 2) + Math.cos(a[1] * r) * Math.cos(b[1] * r) * Math.sin(dLo / 2) * Math.sin(dLo / 2); return 2 * R * Math.asin(Math.sqrt(h)); }
  function centroid(g) { var x = 0, y = 0, n = 0; g.forEach(function (ring) { ring.forEach(function (p) { x += p[0]; y += p[1]; n++; }); }); return [x / n, y / n]; }
  function nearest(pt, recs) { var best = null; recs.forEach(function (r) { r.bh.forEach(function (b) { if (!b.pfos || b.pfos <= 0) return; var x = b.pfos / 6321.4; if (x <= 1) return;
    var d = dist(pt, [b.lng, b.lat]); if (!best || d < best.d) best = { d: d, plot: r.plot, x: x }; }); }); return best; }
  function stats(d) { var rep = d.records.filter(function (r) { return r.status === 'published_report'; }), top = rep.slice().sort(function (a, b) { return b.pfosX - a.pfosX; })[0];
    return { reports: rep.length, holes: rep.reduce(function (s, r) { return s + (r.holes || 0); }, 0), over: rep.reduce(function (s, r) { return s + (r.pfosHoles || 0); }, 0), onMap: d.records.reduce(function (s, r) { return s + r.bh.length; }, 0), top: top }; }
  window.NLSX = { bin: bin, dist: dist, centroid: centroid, nearest: nearest, stats: stats };
  if (!window.NadLanInstruments) return;
  var NLI = window.NadLanInstruments, F = NLI.fmt, esc = NLI.esc;
  function xs(x) { return 'פי ' + (x >= 10 ? F.num(Math.round(x)) : F.num(x, 1)); }
  function dt(iso) { return iso ? F.date(String(iso).slice(0, 10)) : ''; }

  function loadML(cb) {
    if (window.maplibregl) return cb();
    var l = document.createElement('link'); l.rel = 'stylesheet'; l.href = ML + 'maplibre-gl.css'; document.head.appendChild(l);
    var s = document.createElement('script'); s.src = ML + 'maplibre-gl.js'; s.async = true;
    s.onload = function () { try { window.maplibregl.setRTLTextPlugin(RTL, true); } catch (e) { /* already set */ } cb(); };
    s.onerror = function () { cb(new Error('map')); }; document.head.appendChild(s);
  }

  NLI.register('soilmap', {
    custom: function (root, data) {
      var d = data.soil, S = stats(d), recs = {}, byOid = {}, phone = window.matchMedia('(max-width: 760px)').matches;
      d.records.forEach(function (r) { recs[r.plot] = r; });
      d.plots.forEach(function (p) { byOid[p.oid] = p; });
      var order = d.records.slice().sort(function (a, b) { var k = ['published_report', 'findings_reported_no_report', 'developer_reported_no_exceedance', 'under_testing_per_developer'];
        return (k.indexOf(a.status) - k.indexOf(b.status)) || ((b.pfosX || 0) - (a.pfosX || 0)); });
      root.innerHTML = '<div class="nli__panel nls">'
        + '<p class="nli__kicker">מפה · שדה דב</p><h2 class="nli__title">מפת זיהום הקרקע בשדה דב</h2>'
        + '<p class="nli__lede">כל מגרש שפורסם עליו סקר קרקע, וכל קידוח במקומו. נוגעים במגרש, בפרויקט או במספר מגרש ורואים פי כמה מעל ערך הסף, באיזה עומק, ואת הדו"ח עצמו.</p>'
        + '<div class="nls__strip"><div><span>דו"חות שפורסמו</span><strong>' + S.reports + '</strong></div><div><span>קידוחים עם חריגה</span><strong>' + S.over + ' מתוך ' + S.holes + '</strong></div>'
        + '<div class="is-top"><span>השיא (מגרש ' + esc(S.top.plot) + ')</span><strong>' + xs(S.top.pfosX) + '</strong></div></div>'
        + '<div class="nls__find"><label class="nls__q"><span>מספר מגרש או פרויקט</span><input type="search" inputmode="search" enterkeyhint="search" placeholder="למשל 303, 2206, דמרי ים" autocomplete="off"></label>'
        + '<div class="nls__chips" role="list">' + order.map(function (r) { return '<button type="button" role="listitem" data-p="' + esc(r.plot) + '" class="is-' + r.status.split('_')[0] + '">' + esc(r.plot)
          + (PAGE[r.plot] ? ' · ' + esc(PAGE[r.plot][0]) : (r.pfosX ? ' · ' + xs(r.pfosX) : '')) + '</button>'; }).join('') + '</div></div>'
        + '<div class="nls__stage"><div class="nls__map" role="region" aria-label="מפת המגרשים והקידוחים בשדה דב"><p class="nls__wait">טוען את המפה…</p></div><div class="nls__card" aria-live="polite"></div></div>'
        + '<div class="nls__bar"><button type="button" class="nls__3d" aria-pressed="true">תלת ממד</button><ul class="nls__legend">' + BIN.map(function (b) { return '<li><b style="background:' + b[1] + '"></b>' + b[2] + '</li>'; }).join('')
        + '<li><b class="is-list"></b>ברשימה, בלי דו"ח</li><li><b class="is-dev"></b>לפי היזם: בלי חריגות</li></ul></div>'
        + '<p class="nli__note">המפה מציגה רק מה שפורסם. מגרש בלי צבע הוא מגרש שלא פורסם עליו דו"ח דיגום במאגר, וזה לא אומר שהקרקע נקייה או מזוהמת. הערכים: הריכוז הגבוה ביותר של PFOS בכל קידוח, מול ' + esc(d.thresholdsLabel) + ': PFOS '
        + F.num(d.thresholds.pfos, 1) + ' ננוגרם לק"ג, PFOA ' + F.num(d.thresholds.pfoa, 1) + '.</p>'
        + '<details class="nli__table" open><summary>כל המגרשים עם מידע שפורסם</summary><div class="nli__tw"><table><thead><tr><th scope="col">מגרש</th><th scope="col" class="ph">יזם</th><th scope="col">המצב</th><th scope="col">שיא PFOS</th></tr></thead><tbody>'
        + order.map(function (r) { return '<tr><td><button type="button" class="nls__row" data-p="' + esc(r.plot) + '">' + esc(r.plot) + '</button></td><td class="ph">' + esc(DEV[r.plot] || '') + '</td><td>' + esc(ST[r.status] || '') + '</td><td class="n">'
          + (r.pfosX ? xs(r.pfosX) : '') + '</td></tr>'; }).join('') + '</tbody></table></div></details>'
        + '<p class="nli__src">מקורות: ' + esc(d.sourcesNote) + '. המפה: © OpenStreetMap, OpenFreeMap. עודכן ' + esc(F.date(d.built)) + '.</p></div>';
      var card = root.querySelector('.nls__card'), mapEl = root.querySelector('.nls__map'), map = null, sel = null;

      function plotCard(p) {
        var r = p.ref ? recs[p.ref] : null;
        if (!r) {
          var nb = nearest(centroid(p.g), d.records);
          return '<p class="nls__ct">מגרש ' + esc(p.n) + '<span> · ' + esc(p.use) + (p.m2 ? ' · ' + F.num(p.m2) + ' מ"ר' : '') + '</span></p><p class="nls__badge">לא פורסם דו"ח דיגום</p>'
            + '<p class="nls__txt">על המגרש הזה לא פורסם דו"ח דיגום במאגר המשרד להגנת הסביבה (נכון ל־' + esc(F.date(d.built)) + '). זה לא אומר שהקרקע נבדקה או שהיא נקייה.</p>'
            + (nb ? '<dl class="nli__lines"><dt>הקידוח הקרוב שבו נמצאה חריגה</dt><dd>' + F.num(Math.round(nb.d / 10) * 10) + ' מ\' · מגרש ' + esc(nb.plot) + '</dd></dl>' : '') + '<p class="nls__plan">תכנית ' + esc(p.plan) + '</p>';
        }
        var h = '<p class="nls__ct">מגרש ' + esc(r.plot) + '<span> · ' + esc(r.use || p.use) + '</span></p><p class="nls__badge is-' + r.status.split('_')[0] + '">' + esc(ST[r.status]) + '</p>';
        if (r.status === 'published_report') {
          h += '<div class="nli__answer"><span class="nli__alab">הריכוז הגבוה ביותר של PFOS, מול ערך הסף</span><output class="nli__fig is-survey">' + xs(r.pfosX) + '</output><span class="nli__asub">'
            + F.num(r.pfosMax) + ' ננוגרם לק"ג' + (r.pfosDepth != null ? ', בעומק ' + F.num(r.pfosDepth, 1) + ' מ\'' : '') + '</span></div>'
            + '<dl class="nli__lines"><dt>קידוחים עם חריגת PFOS</dt><dd>' + F.num(r.pfosHoles) + ' מתוך ' + F.num(r.holes) + '</dd>'
            + (r.pfoaX ? '<dt>PFOA, השיא</dt><dd>' + xs(r.pfoaX) + (r.pfoaHoles ? ' · ' + F.num(r.pfoaHoles) + ' קידוחים' : '') + '</dd>' : '')
            + (r.dates && r.dates.length ? '<dt>הדיגום</dt><dd>' + r.dates.map(dt).join(' עד ') + '</dd>' : '') + (r.report ? '<dt>הדו"ח</dt><dd>' + dt(r.report) + '</dd>' : '')
            + '</dl><p class="nls__txt"><b>יזם או ייעוד:</b> ' + esc(DEV[r.plot] || 'לא ידוע') + '</p>';
          if (r.bh.some(function (b) { return b.approx; })) h += '<p class="nls__plan">מיקומי הקידוחים במגרש הזה שוחזרו מהתרשים שבדו"ח, בדיוק של כ־2 מטרים.</p>';
        } else {
          h += (DEV[r.plot] ? '<p class="nls__txt"><b>יזם:</b> ' + esc(DEV[r.plot]) + '</p>' : '');
        }
        if (NOTE[r.plot]) h += '<p class="nls__txt">' + esc(NOTE[r.plot]) + '</p>';
        h += '<p class="nls__links">' + (r.src ? '<a href="' + esc(r.src) + '" target="_blank" rel="noopener">' + (r.status === 'published_report' ? 'הדו"ח במאגר המשרד להגנת הסביבה' : 'המקור') + '</a>' : '')
          + (PAGE[r.plot] ? '<a href="' + esc(PAGE[r.plot][1]) + '">לעמוד הפרויקט: ' + esc(PAGE[r.plot][0]) + '</a>' : '') + '</p>';
        return h;
      }
      function select(p, fly) {
        sel = p; card.innerHTML = plotCard(p);
        [].forEach.call(root.querySelectorAll('.nls__chips button'), function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-p') === (p.ref || '') ? 'true' : 'false'); });
        if (!map || !map.getSource) return;
        var oids = p.ref && recs[p.ref] ? recs[p.ref].oids : [p.oid];
        map.setFilter('nls-sel', ['in', ['get', 'oid'], ['literal', oids]]);
        if (fly) { var b = new window.maplibregl.LngLatBounds(); oids.forEach(function (o) { var q = byOid[o]; if (q) q.g.forEach(function (ring) { ring.forEach(function (c) { b.extend(c); }); }); });
          if (!b.isEmpty()) map.fitBounds(b, { padding: phone ? 40 : 80, maxZoom: 17.2, duration: 900 }); }
      }
      function byPlot(n) { var r = recs[n]; if (r) return byOid[r.oids[0]] ? Object.assign({}, byOid[r.oids[0]], { ref: n }) : null;
        var all = d.plots.filter(function (p) { return p.n === n; }); return all[0] || null; }
      function find(q) { q = String(q || '').trim(); if (!q) return;
        var hit = Object.keys(PAGE).filter(function (k) { return PAGE[k][0].indexOf(q) > -1 || q.indexOf(PAGE[k][0]) > -1; })[0] || q.replace(/\D/g, '');
        var p = byPlot(hit); if (p) { select(p, true); mapEl.scrollIntoView({ block: 'nearest', behavior: 'smooth' }); }
        else card.innerHTML = '<p class="nls__txt">לא מצאנו מגרש ' + esc(q) + ' בתכניות של רובע שדה דב (תמ"ל 3001, 1/4444, 2/4444).</p>'; }
      root.querySelector('.nls__chips').addEventListener('click', function (e) { var b = e.target.closest('button'); if (b) find(b.getAttribute('data-p')); });
      root.querySelector('tbody').addEventListener('click', function (e) { var b = e.target.closest('.nls__row'); if (b) find(b.getAttribute('data-p')); });
      var inp = root.querySelector('.nls__q input');
      inp.addEventListener('keydown', function (e) { if (e.key === 'Enter') { e.preventDefault(); find(inp.value); } });
      inp.addEventListener('change', function () { find(inp.value); });
      select(byPlot(S.top.plot), false);

      loadML(function (err) {
        if (err || !window.maplibregl) { mapEl.innerHTML = '<p class="nls__wait">המפה לא נטענה. הטבלה והכרטיס למטה עובדים גם בלעדיה.</p>'; return; }
        var gl = window.maplibregl, b0 = new gl.LngLatBounds();
        d.records.forEach(function (r) { r.oids.forEach(function (o) { var q = byOid[o]; if (q) q.g.forEach(function (ring) { ring.forEach(function (c) { b0.extend(c); }); }); }); });
        mapEl.innerHTML = '';
        map = new gl.Map({ container: mapEl, style: STYLE, bounds: b0, fitBoundsOptions: { padding: phone ? 24 : 60 }, pitch: phone ? 40 : 52, bearing: -28, maxPitch: 70,
          attributionControl: { compact: true }, cooperativeGestures: phone,
          locale: { 'CooperativeGesturesHandler.MobileHelpText': 'מזיזים את המפה בשתי אצבעות', 'CooperativeGesturesHandler.WindowsHelpText': 'Ctrl וגלגלת כדי להגדיל', 'CooperativeGesturesHandler.MacHelpText': '⌘ וגלגלת כדי להגדיל' } });
        map.addControl(new gl.NavigationControl({ visualizePitch: true }), 'top-left');
        map.on('load', function () {
          var feats = d.plots.map(function (p) { var r = p.ref ? recs[p.ref] : null;
            return { type: 'Feature', properties: { oid: p.oid, n: p.n, st: r ? r.status : '', x: r && r.pfosX ? r.pfosX : 0, lab: r ? 1 : 0 }, geometry: { type: 'Polygon', coordinates: p.g } }; });
          var holes = []; d.records.forEach(function (r) { r.bh.forEach(function (b) { holes.push({ type: 'Feature', properties: { plot: r.plot, id: b.id, pfos: b.pfos || 0, x: (b.pfos || 0) / d.thresholds.pfos, dep: b.pfosD, pfoa: b.pfoa || 0, approx: b.approx ? 1 : 0 },
            geometry: { type: 'Point', coordinates: [b.lng, b.lat] } }); }); });
          map.addSource('nls-plots', { type: 'geojson', data: { type: 'FeatureCollection', features: feats } });
          map.addSource('nls-holes', { type: 'geojson', data: { type: 'FeatureCollection', features: holes } });
          var xcol = ['step', ['get', 'x'], BIN[3][1], 1, BIN[2][1], 10, BIN[1][1], 100, BIN[0][1]];
          map.addLayer({ id: 'nls-fill', type: 'fill', source: 'nls-plots', paint: { 'fill-color': ['match', ['get', 'st'], 'published_report', xcol, 'findings_reported_no_report', '#F3D3DC',
            'developer_reported_no_exceedance', '#D3E5EC', 'under_testing_per_developer', '#E3E8EB', 'rgba(255,255,255,0)'], 'fill-opacity': ['match', ['get', 'st'], 'published_report', 0.55, '', 0, 0.75] } });
          var dashed = ['in', ['get', 'st'], ['literal', ['findings_reported_no_report', 'under_testing_per_developer']]];
          map.addLayer({ id: 'nls-line', type: 'line', source: 'nls-plots', filter: ['!', dashed], paint: { 'line-color': ['match', ['get', 'st'], 'published_report', '#8E1238',
            'developer_reported_no_exceedance', '#2F6F86', '#9FB0BA'], 'line-width': ['match', ['get', 'st'], '', 0.6, 1.6] } });
          map.addLayer({ id: 'nls-dash', type: 'line', source: 'nls-plots', filter: dashed, paint: { 'line-color': ['match', ['get', 'st'], 'findings_reported_no_report', '#C42550', '#7A8A94'],
            'line-width': 1.8, 'line-dasharray': [2, 1.5] } });
          var lay = map.getStyle().layers, firstSym = (lay.filter(function (l) { return l.type === 'symbol'; })[0] || {}).id;
          if (map.getSource('openmaptiles')) map.addLayer({ id: 'nls-3d', type: 'fill-extrusion', source: 'openmaptiles', 'source-layer': 'building', minzoom: 13.5,
            paint: { 'fill-extrusion-color': '#D9E1E7', 'fill-extrusion-height': ['coalesce', ['get', 'render_height'], 9], 'fill-extrusion-base': ['coalesce', ['get', 'render_min_height'], 0], 'fill-extrusion-opacity': 0.88 } }, firstSym);
          map.addLayer({ id: 'nls-sel', type: 'line', source: 'nls-plots', filter: ['in', ['get', 'oid'], ['literal', []]], paint: { 'line-color': '#12202A', 'line-width': 3.2 } });
          map.addLayer({ id: 'nls-holes', type: 'circle', source: 'nls-holes', paint: { 'circle-color': xcol, 'circle-radius': ['interpolate', ['linear'], ['zoom'], 14, 3, 17, 7, 19, 11],
            'circle-stroke-color': '#FFFFFF', 'circle-stroke-width': 1.4, 'circle-pitch-alignment': 'map' } });
          map.addLayer({ id: 'nls-lab', type: 'symbol', source: 'nls-plots', filter: ['==', ['get', 'lab'], 1], layout: { 'text-field': ['get', 'n'], 'text-font': ['Noto Sans Regular'], 'text-size': 13, 'text-allow-overlap': false },
            paint: { 'text-color': '#12202A', 'text-halo-color': '#FFFFFF', 'text-halo-width': 1.6 } });
          map.on('click', 'nls-holes', function (e) { var f = e.features[0].properties;
            new gl.Popup({ className: 'nls-pop', maxWidth: '260px' }).setLngLat(e.lngLat).setHTML('<p><b>קידוח ' + esc(f.id) + ' · מגרש ' + esc(f.plot) + '</b></p><p>PFOS: ' + (f.x > 0 ? xs(f.x) + ' מהסף · ' + F.num(f.pfos) + ' ננוגרם לק"ג' : 'מתחת לסף הדיווח')
              + (f.dep ? ', בעומק ' + F.num(f.dep, 1) + ' מ\'' : '') + '</p>' + (f.pfoa ? '<p>PFOA: ' + xs(f.pfoa / d.thresholds.pfoa) + ' מהסף</p>' : '') + (f.approx ? '<p class="nls__plan">מיקום משוחזר מהתרשים, כ־2 מ\'.</p>' : '')).addTo(map); e.preventDefault(); });
          map.on('click', 'nls-fill', function (e) { if (e.defaultPrevented) return; var o = e.features[0].properties.oid, p = byOid[o]; if (p) select(p, false); });
          ['nls-holes', 'nls-fill'].forEach(function (l) { map.on('mouseenter', l, function () { map.getCanvas().style.cursor = 'pointer'; }); map.on('mouseleave', l, function () { map.getCanvas().style.cursor = ''; }); });
          var at = mapEl.querySelector('.maplibregl-ctrl-attrib'); if (at) at.classList.remove('maplibregl-compact-show');  // the credit stays one tap away; it is also printed under the map
          if (sel) select(sel, false);
        });
        var b3 = root.querySelector('.nls__3d');
        b3.addEventListener('click', function () { var on = b3.getAttribute('aria-pressed') !== 'true'; b3.setAttribute('aria-pressed', on ? 'true' : 'false');
          map.easeTo({ pitch: on ? (phone ? 40 : 52) : 0, bearing: on ? -28 : 0, duration: 700 }); if (map.getLayer('nls-3d')) map.setLayoutProperty('nls-3d', 'visibility', on ? 'visible' : 'none'); });
      });
    }
  });
})();
