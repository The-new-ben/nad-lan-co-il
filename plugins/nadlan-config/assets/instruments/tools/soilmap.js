/* NadLan Instruments · soilmap v1 (HAD-534, Ben 15.10.2026): the Sde Dov soil map. Every plot of the district (municipal GIS
   layer 837), the plots with a published soil survey coloured by how many times the PFOS value passed the direct-contact
   threshold, every borehole in its place, the plots on the "nine plots" list and the developers' own statements, each with
   its source. A 3D city view (MapLibre GL + OpenFreeMap tiles + OSM buildings), one tap on a plot, a project or a chip opens
   the plot card; any plot number of the district can be checked. Data: data/sde-dov-soil.json, built by
   tools/instruments/build_soil_data.py from docs/research/2026-10-15-sde-dov-soil/. Pure helpers in NLSX for unit checks.
   HAD-534 (d), 21.10.2026: Hebrew and English. The page language comes from the engine (NadLanInstruments.lang); the
   strings are TX (he/en, {name} placeholders), the Hebrew values inside the data file are translated by DATA_EN (a value
   without an English entry stays as it is: the release check looks for Hebrew letters in the English render).
   Source table: docs/tools/soil-en/strings-en.json (soilmap + data). */
(function () {
  'use strict';
  var ML = 'https://unpkg.com/maplibre-gl@4.7.1/dist/', RTL = 'https://unpkg.com/@mapbox/mapbox-gl-rtl-text@0.2.3/mapbox-gl-rtl-text.min.js';
  var STYLE = 'https://tiles.openfreemap.org/styles/positron';
  var EN = !!(window.NadLanInstruments && window.NadLanInstruments.lang === 'en'), LG = EN ? 'en' : 'he';
  var TX = {
    bin100: { he: 'פי 100 ומעלה', en: '100× and above' },
    bin10: { he: 'פי 10 עד 100', en: '10× to 100×' },
    bin1: { he: 'עד פי 10', en: 'Up to 10×' },
    bin0: { he: 'מתחת לסף', en: 'Below the threshold' },
    stPublished: { he: 'דו"ח בדיקה פורסם', en: 'Test report published' },
    stFindings: { he: 'ברשימת המגרשים עם ממצאים', en: 'On the list of plots with findings' },
    stDevClear: { he: 'לפי היזם: בלי חריגות', en: 'Per the developer: no exceedances' },
    stDevTesting: { he: 'לפי היזם: בבדיקה', en: 'Per the developer: under review' },
    times: { he: 'פי {n}', en: '{n}×' },
    range: { he: '{a} עד {b}', en: '{a} to {b}' },
    ofN: { he: '{a} מתוך {b}', en: '{a} of {b}' },
    kicker: { he: 'מפה · שדה דב', en: 'Map · Sde Dov' },
    title: { he: 'מפת בדיקות הקרקע בשדה דב', en: 'Sde Dov soil test map' },
    lede: { he: 'כל מגרש שפורסם עליו דו"ח בדיקת קרקע, וכל קידוח במקומו. נוגעים במגרש או מקלידים את מספרו, ורואים את הערכים מול ערך הסף, את שלב הפרויקט במגרש, ואת הדו"ח עצמו.',
      en: 'Every plot with a published soil test report, and every borehole in its place. Tap a plot or type its number to see the values against the threshold, the stage of the project on the plot, and the report itself.' },
    stripReports: { he: 'דו"חות בדיקה שפורסמו', en: 'Published test reports' },
    stripOver: { he: 'קידוחים מעל ערך הסף', en: 'Boreholes above the threshold' },
    stripTop: { he: 'הערך הגבוה (מגרש {plot})', en: 'Highest value (plot {plot})' },
    qLabel: { he: 'מספר מגרש', en: 'Plot number' },
    qPh: { he: 'למשל 303 או 2206', en: 'e.g. 303 or 2206' },
    chipMkt: { he: ' · פרויקט בשיווק', en: ' · project in marketing' },
    mapAria: { he: 'מפת המגרשים והקידוחים בשדה דב', en: 'Map of the Sde Dov plots and boreholes' },
    mapWait: { he: 'טוען את המפה…', en: 'Loading the map…' },
    d3: { he: 'תלת ממד', en: '3D' },
    lgList: { he: 'ברשימה, בלי דו"ח', en: 'On the list, no report' },
    lgDev: { he: 'לפי היזם: בלי חריגות', en: 'Per the developer: no exceedances' },
    lgGreen: { he: 'פרויקט בשיווק (המחשה)', en: 'Project in marketing (illustration)' },
    mapNote: { he: 'המפה מציגה רק מה שפורסם. מגרש בלי צבע הוא מגרש שלא פורסם עליו דו"ח דיגום במאגר, וזה לא אומר דבר על מצב הקרקע בו. הערכים: הריכוז הגבוה ביותר של PFOS בכל קידוח, מול {label}: PFOS {pfos} ננוגרם לק"ג, PFOA {pfoa}.',
      en: 'The map shows only what has been published. A plot without colour has no sampling report in the database, and that says nothing about its soil. The values: the highest PFOS concentration in each borehole, against the {label}: PFOS {pfos} ng/kg, PFOA {pfoa}.' },
    tableSummary: { he: 'כל המגרשים עם מידע שפורסם', en: 'All plots with published information' },
    thPlot: { he: 'מגרש', en: 'Plot' },
    thStatus: { he: 'המצב', en: 'Status' },
    thStage: { he: 'השלב במגרש', en: 'Stage on the plot' },
    thPfos: { he: 'PFOS מול הסף', en: 'PFOS vs the threshold' },
    srcLine: { he: 'מקורות: {src}. המפה: © OpenStreetMap, OpenFreeMap. עודכן {date}.', en: 'Sources: {src}. Map: © OpenStreetMap, OpenFreeMap. Updated {date}.' },
    askMsgProj: { he: 'שלום, אשמח לפרטים על הפרויקט במגרש {n} ברובע שדה דב.', en: 'Hello, I would like details on the project on plot {n} in the Sde Dov district.' },
    askMsgPlot: { he: 'שלום, אשמח לפרטים על מגרש {n} ברובע שדה דב.', en: 'Hello, I would like details on plot {n} in the Sde Dov district.' },
    askBtnProj: { he: 'בקשת פרטים על הפרויקט במגרש {n}', en: 'Ask for details on the project on plot {n}' },
    askBtnPlot: { he: 'בקשת פרטים על מגרש {n}', en: 'Ask for details on plot {n}' },
    plot: { he: 'מגרש {n}', en: 'Plot {n}' },
    badgeProj: { he: 'פרויקט בשיווק', en: 'Project in marketing' },
    greenNote: { he: 'הבניין הירוק במפה הוא המחשה לפי מספר הקומות שפורסם, לא תכנון מדויק.', en: 'The green building on the map is an illustration from the published number of floors, not the exact design.' },
    m2: { he: '{n} מ"ר', en: '{n} m²' },
    badgeNone: { he: 'לא פורסם דו"ח בדיקה', en: 'No test report published' },
    noneTxt: { he: 'על המגרש הזה לא פורסם דו"ח בדיקת קרקע במאגר המשרד להגנת הסביבה (נכון ל־{date}).', en: 'No soil test report for this plot has been published in the Ministry of Environmental Protection database (as of {date}).' },
    plan: { he: 'תכנית {p}', en: 'Plan {p}' },
    peakLab: { he: 'הערך הגבוה של PFOS בדו"ח, מול ערך הסף', en: 'Highest PFOS value in the report, against the threshold' },
    ng: { he: '{n} ננוגרם לק"ג', en: '{n} ng/kg' },
    depth: { he: ', בעומק {m} מ\'', en: ', at a depth of {m} m' },
    holesOver: { he: 'קידוחים מעל ערך הסף (PFOS)', en: 'Boreholes above the threshold (PFOS)' },
    pfoaPeak: { he: 'PFOA, הערך הגבוה', en: 'PFOA, highest value' },
    nHoles: { he: '{n} קידוחים', en: '{n} boreholes' },
    below: { he: 'מתחת לסף', en: 'Below the threshold' },
    sampled: { he: 'הבדיקה', en: 'Sampling' },
    report: { he: 'הדו"ח', en: 'Report' },
    approx: { he: 'מיקומי הקידוחים במגרש הזה שוחזרו מהתרשים שבדו"ח, בדיוק של כ־2 מטרים.', en: 'The borehole positions on this plot were reconstructed from the drawing in the report, to about 2 metres.' },
    phaseMkt: { he: 'יש במגרש פרויקט בשיווק', en: 'A project in marketing on this plot' },
    phaseStage: { he: 'השלב במגרש', en: 'Stage on the plot' },
    inMkt: { he: 'בשיווק', en: 'In marketing' },
    mktPrefix: { he: '^פרויקט בשיווק( · )?', en: '^Project in marketing( · )?' },
    reportLink: { he: 'הדו"ח במאגר המשרד להגנת הסביבה', en: 'The report in the Ministry of Environmental Protection database (Hebrew PDF)' },
    findHint: { he: 'מקלידים מספר מגרש, למשל 303 או 2206.', en: 'Type a plot number, e.g. 303 or 2206.' },
    findNone: { he: 'לא מצאנו מגרש {q} בתכניות של רובע שדה דב (תמ"ל 3001, 1/4444, 2/4444).', en: 'We found no plot {q} in the Sde Dov district plans (TMAL 3001, 1/4444, 2/4444).' },
    mapFail: { he: 'המפה לא נטענה. הטבלה והכרטיס למטה עובדים גם בלעדיה.', en: 'The map did not load. The table and the card below work without it.' },
    gMobile: { he: 'מזיזים את המפה בשתי אצבעות', en: 'Use two fingers to move the map' },
    gWin: { he: 'Ctrl וגלגלת כדי להגדיל', en: 'Use Ctrl + scroll to zoom the map' },
    gMac: { he: '⌘ וגלגלת כדי להגדיל', en: 'Use ⌘ + scroll to zoom the map' },
    popHole: { he: 'קידוח {id} · מגרש {plot}', en: 'Borehole {id} · plot {plot}' },
    popOver: { he: '{x} מהסף · {ng} ננוגרם לק"ג', en: '{x} the threshold · {ng} ng/kg' },
    popBelowRL: { he: 'מתחת לסף הדיווח', en: 'below the reporting limit' },
    popPfoaOver: { he: '{x} מהסף', en: '{x} the threshold' },
    popApprox: { he: 'מיקום משוחזר מהתרשים, כ־2 מ\'.', en: 'Position reconstructed from the drawing, about 2 m.' }
  };
  // Ben 15.10.2026: no project or company names on this surface. Developers' statements stay unnamed ("לפי היזם"); per plot
  // only whether a project is in marketing and its phase, and a button that asks us for details (WhatsApp, the site's number).
  var NOTE = {
    '106': { he: 'לפי היזם (מרץ 2026): בבדיקה לא נמצאו חריגות מערכי הסף, והמשרד להגנת הסביבה אימץ את הממצאים. הדו"ח לא פורסם במאגר.',
      en: 'Per the developer (March 2026): the testing found no exceedance of the threshold values, and the Ministry of Environmental Protection adopted the findings. The report has not been published in the database.' },
    '2102': { he: 'לפי היזם (יולי 2026): הבדיקות הושלמו בלי חריגות, והמשרד אישר. הדו"ח לא פורסם במאגר.',
      en: 'Per the developer (July 2026): the testing was completed with no exceedances, and the Ministry approved. The report has not been published in the database.' },
    '2203': { he: 'לפי היזם (יולי 2026): המגרש בבדיקה אחרי הדיגום.', en: 'Per the developer (July 2026): the plot is under review after sampling.' },
    '2207': { he: 'לפי היזם (יולי 2026): המגרש בבדיקה אחרי הדיגום. הדו"ח לא פורסם במאגר.', en: 'Per the developer (July 2026): the plot is under review after sampling. The report has not been published in the database.' },
    '103': { he: 'המגרש נכלל ברשימת המגרשים שבהם נמסר על ממצאים (יולי 2026). הדו"ח לא פורסם במאגר.', en: 'The plot is on the list of plots where findings were reported (July 2026). The report has not been published in the database.' },
    '105': { he: 'המגרש נכלל ברשימת המגרשים שבהם נמסר על ממצאים (יולי 2026). הדו"ח לא פורסם במאגר.', en: 'The plot is on the list of plots where findings were reported (July 2026). The report has not been published in the database.' },
    '107': { he: 'לפי היזם (יולי 2026): יותר מ־98% מהדגימות תקינות, והקרקע שבה נמצאו חריגות פונתה במלואה. הדו"ח לא פורסם במאגר.',
      en: 'Per the developer (July 2026): more than 98% of the samples are within the values, and the soil where exceedances were found has been fully removed. The report has not been published in the database.' },
    '2255': { he: 'לפי שכבת המגרשים של העירייה, 9 מתוך 12 הקידוחים של הדו"ח נמצאים בתחום מגרש 2227 הסמוך. הקידוחים מוצגים במקום שמופיע בדו"ח.',
      en: 'According to the municipal plot layer, 9 of the 12 boreholes in the report lie within the neighbouring plot 2227. The boreholes are shown where the report places them.' }
  };
  // The Hebrew values inside data/sde-dov-soil.json, in English (used on English pages only).
  var DATA_EN = {
    use: { 'דרך מאושרת': 'Approved road', 'מבנים ומוסדות ציבור': 'Public buildings and institutions', 'שטח ציבורי פתוח': 'Public open space', 'דרך מוצעת': 'Proposed road',
      'מגורים ותעסוקה': 'Residential and employment', 'מגורים ומסחר': 'Residential and retail', 'פארק / גן ציבורי': 'Park / public garden', 'כיכר עירונית': 'Urban plaza', 'דרך קיימת': 'Existing road',
      'מלונאות (אכסון מלונאי)': 'Hotels (hotel accommodation)', 'מסחר, תעסוקה ותיירות': 'Retail, employment and tourism', 'מגורים, מסחר ותיירות': 'Residential, retail and tourism',
      'מסחר ותעסוקה': 'Retail and employment', 'תעסוקה': 'Employment', 'דיור מיוחד': 'Special housing', 'מרכז עסקים ראשי': 'Central business district', 'מגרש מיוחד': 'Special plot',
      'עירוני מעורב': 'Mixed urban use', 'שטחים פתוחים ומתקנים הנדסיים': 'Open space and engineering facilities', 'פתוח חוף הים-מ א': 'Open seashore area', 'בנייני ציבור': 'Public buildings' },
    stage: { 'נמכר במכרז רמ"י (דצמבר 2024)': 'Sold in an Israel Land Authority tender (December 2024)', 'פרויקט בשיווק': 'Project in marketing',
      'פרויקט בשיווק · הוגשה בקשה להיתר חפירה ודיפון (8.10.2026)': 'Project in marketing · an excavation and shoring permit application was filed (8 Oct 2026)' },
    fact: { 'מגדל בן 39 קומות ובנייני בוטיק בני 9 קומות · 459 דירות': 'A 39-storey tower and 9-storey boutique buildings · 459 apartments',
      'מגדל בן 40 קומות, מגדלון בן 16 ושני בניינים בני 9 · 458 דירות': 'A 40-storey tower, a 16-storey mid-rise and two 9-storey buildings · 458 apartments',
      'מגדל בן 35 קומות ועוד 3 בניינים · 406 דירות': 'A 35-storey tower and 3 more buildings · 406 apartments',
      '4 בניינים סביב חצר משותפת · 337 דירות': '4 buildings around a shared courtyard · 337 apartments',
      '230 דירות': '230 apartments',
      '324 דירות להשכרה ארוכת טווח · מגדל בן 38 קומות ושני בניינים בני 8': '324 long-term rental apartments · a 38-storey tower and two 8-storey buildings',
      'מגדל בן 45 קומות ו-3 מגדלים בני 20 · 708 דירות': 'A 45-storey tower and 3 towers of 20 storeys · 708 apartments',
      'מגדל בן 45 קומות ו-3 בנייני בוטיק בני 9 · 350 דירות': 'A 45-storey tower and 3 boutique buildings of 9 storeys · 350 apartments',
      'דיור מוגן · עד 300 יחידות דיור': 'Assisted living · up to 300 housing units' },
    plan: { 'תמ"ל3001': 'TMAL 3001' },
    label: { 'ערכי סף למגע ישיר עבור שדה דב, יוני 2026 (כפי שמצוטטים בדו"חות)': 'direct-contact threshold values for Sde Dov, June 2026 (as quoted in the reports)' },
    sources: { 'דו"חות סקרי הקרקע של פרויקט אבן דרך במאגר המשרד להגנת הסביבה; שכבת המגרשים 837 של עיריית תל אביב': 'the soil survey reports of the Even Derech programme in the Ministry of Environmental Protection database; plot layer 837 of the Tel Aviv municipality' }
  };
  function pick(tx) { var o = {}; Object.keys(tx).forEach(function (k) { o[k] = tx[k][LG] != null ? tx[k][LG] : tx[k].he; }); return o; }
  var T = pick(TX);
  function f(s, o) { return String(s).replace(/\{(\w+)\}/g, function (m, k) { return o[k] != null ? o[k] : m; }); }
  function tr(kind, s) { return EN && s != null && DATA_EN[kind][s] != null ? DATA_EN[kind][s] : s; }
  var BIN = [[100, '#8E1238', T.bin100], [10, '#C42550', T.bin10], [1, '#E58CA4', T.bin1], [0, '#8FA6B2', T.bin0]];
  var ST = { published_report: T.stPublished, findings_reported_no_report: T.stFindings,
    developer_reported_no_exceedance: T.stDevClear, under_testing_per_developer: T.stDevTesting };
  var WA = 'https://wa.me/972525101555?text=';
  function bin(x) { for (var i = 0; i < BIN.length; i++) if (x > BIN[i][0] || (BIN[i][0] === 0)) return BIN[i]; return BIN[3]; }
  function dist(a, b) { var R = 6371000, r = Math.PI / 180, dLa = (b[1] - a[1]) * r, dLo = (b[0] - a[0]) * r;
    var h = Math.sin(dLa / 2) * Math.sin(dLa / 2) + Math.cos(a[1] * r) * Math.cos(b[1] * r) * Math.sin(dLo / 2) * Math.sin(dLo / 2); return 2 * R * Math.asin(Math.sqrt(h)); }
  function centroid(g) { var x = 0, y = 0, n = 0; g.forEach(function (ring) { ring.forEach(function (p) { x += p[0]; y += p[1]; n++; }); }); return [x / n, y / n]; }
  function nearest(pt, recs) { var best = null; recs.forEach(function (r) { r.bh.forEach(function (b) { if (!b.pfos || b.pfos <= 0) return; var x = b.pfos / 6321.4; if (x <= 1) return;
    var d = dist(pt, [b.lng, b.lat]); if (!best || d < best.d) best = { d: d, plot: r.plot, x: x }; }); }); return best; }
  function stats(d) { var rep = d.records.filter(function (r) { return r.status === 'published_report'; }), top = rep.slice().sort(function (a, b) { return b.pfosX - a.pfosX; })[0];
    return { reports: rep.length, holes: rep.reduce(function (s, r) { return s + (r.holes || 0); }, 0), over: rep.reduce(function (s, r) { return s + (r.pfosHoles || 0); }, 0), onMap: d.records.reduce(function (s, r) { return s + r.bh.length; }, 0), top: top }; }
  function inside(pt, g) { var x = pt[0], y = pt[1], c = false, r = g[0]; for (var i = 0, j = r.length - 1; i < r.length; j = i++) { if (((r[i][1] > y) !== (r[j][1] > y)) && (x < (r[j][0] - r[i][0]) * (y - r[i][1]) / (r[j][1] - r[i][1]) + r[i][0])) c = !c; } return c; }
  window.NLSX = { bin: bin, dist: dist, centroid: centroid, nearest: nearest, stats: stats, inside: inside, TX: TX, NOTE: NOTE, DATA_EN: DATA_EN };
  if (!window.NadLanInstruments) return;
  var NLI = window.NadLanInstruments, F = NLI.fmt, esc = NLI.esc;
  function xs(x) { return f(T.times, { n: x >= 10 ? F.num(Math.round(x)) : F.num(x, 1) }); }
  function dt(iso) { return /^\d{4}-\d{2}-\d{2}/.test(String(iso || '')) ? F.date(String(iso).slice(0, 10)) : ''; }  // a partial date ("2026-06/07") is not shown
  function m1(x) { return x % 1 === 0 ? F.num(x) : F.num(x, 1); }
  function span(a) { var v = (a || []).filter(function (x) { return dt(x); }).sort(); return !v.length ? '' : v.length === 1 ? dt(v[0]) : f(T.range, { a: dt(v[0]), b: dt(v[v.length - 1]) }); }

  function loadML(cb) {
    if (window.maplibregl) return cb();
    var l = document.createElement('link'); l.rel = 'stylesheet'; l.href = ML + 'maplibre-gl.css'; document.head.appendChild(l);
    var s = document.createElement('script'); s.src = ML + 'maplibre-gl.js'; s.async = true;
    s.onload = function () { try { window.maplibregl.setRTLTextPlugin(RTL, true); } catch (e) { /* already set */ } cb(); };  // kept on English pages too: the base map labels the streets in Hebrew
    s.onerror = function () { cb(new Error('map')); }; document.head.appendChild(s);
  }

  NLI.register('soilmap', {
    custom: function (root, data) {
      var d = data.soil, S = stats(d), recs = {}, byOid = {}, phone = window.matchMedia('(max-width: 760px)').matches;
      d.records.forEach(function (r) { recs[r.plot] = r; });
      d.plots.forEach(function (p) { byOid[p.oid] = p; });
      var projByOid = {}; (d.projects || []).forEach(function (pr) { pr.oids.forEach(function (o) { projByOid[o] = pr; }); });
      function greens() {  // Mission A (Ben 15.10): every project in marketing as a GREEN schematic building, from the published floor counts
        var out = [];
        (d.projects || []).forEach(function (pr) {
          var lowH = 7;  // a low green base on the lot; only the main tower takes its published height (the rest of the build is in the card text)
          pr.oids.forEach(function (o) { var q = byOid[o]; if (q) out.push({ type: 'Feature', properties: { h: lowH, kind: 'low' }, geometry: { type: 'Polygon', coordinates: q.g } }); });
          if (pr.tower) { var c = pr.c, dy = 14 / 110574, dx = 14 / (111320 * Math.cos(c[1] * Math.PI / 180));
            out.push({ type: 'Feature', properties: { h: pr.tower * 3.4, kind: 'tower' }, geometry: { type: 'Polygon', coordinates: [[[c[0] - dx, c[1] - dy], [c[0] + dx, c[1] - dy], [c[0] + dx, c[1] + dy], [c[0] - dx, c[1] + dy], [c[0] - dx, c[1] - dy]]] } }); }
        });
        return out;
      }
      var order = d.records.slice().sort(function (a, b) { var k = ['published_report', 'findings_reported_no_report', 'developer_reported_no_exceedance', 'under_testing_per_developer'];
        return (k.indexOf(a.status) - k.indexOf(b.status)) || ((b.pfosX || 0) - (a.pfosX || 0)); });
      var extra = []; (d.projects || []).forEach(function (pr) { var q = byOid[pr.oids[0]]; if (q && !q.ref && extra.indexOf(q.n) < 0) extra.push(q.n); });
      root.innerHTML = '<div class="nli__panel nls">'
        + '<p class="nli__kicker">' + esc(T.kicker) + '</p><h2 class="nli__title">' + esc(T.title) + '</h2>'
        + '<p class="nli__lede">' + esc(T.lede) + '</p>'
        + '<div class="nls__strip"><div><span>' + esc(T.stripReports) + '</span><strong>' + S.reports + '</strong></div><div><span>' + esc(T.stripOver) + '</span><strong>' + f(T.ofN, { a: S.over, b: S.holes }) + '</strong></div>'
        + '<div class="is-top"><span>' + f(T.stripTop, { plot: esc(S.top.plot) }) + '</span><strong>' + xs(S.top.pfosX) + '</strong></div></div>'
        + '<div class="nls__find"><label class="nls__q"><span>' + esc(T.qLabel) + '</span><input type="search" inputmode="numeric" enterkeyhint="search" placeholder="' + esc(T.qPh) + '" autocomplete="off"></label>'
        + '<div class="nls__chips" role="list">' + order.map(function (r) { return '<button type="button" role="listitem" data-p="' + esc(r.plot) + '" class="is-' + r.status.split('_')[0] + '">' + esc(r.plot)
          + (r.phase && r.phase.mkt ? T.chipMkt : (r.pfosX ? ' · ' + xs(r.pfosX) : '')) + '</button>'; }).join('') + extra.map(function (n) { return '<button type="button" role="listitem" data-p="' + esc(n) + '" class="is-proj">' + esc(n) + T.chipMkt + '</button>'; }).join('') + '</div></div>'
        + '<div class="nls__stage"><div class="nls__map" role="region" aria-label="' + esc(T.mapAria) + '"><p class="nls__wait">' + esc(T.mapWait) + '</p></div><div class="nls__card" aria-live="polite"></div></div>'
        + '<div class="nls__bar"><button type="button" class="nls__3d" aria-pressed="true">' + esc(T.d3) + '</button><ul class="nls__legend">' + BIN.map(function (b) { return '<li><b style="background:' + b[1] + '"></b>' + b[2] + '</li>'; }).join('')
        + '<li><b class="is-list"></b>' + esc(T.lgList) + '</li><li><b class="is-dev"></b>' + esc(T.lgDev) + '</li><li><b class="is-green"></b>' + esc(T.lgGreen) + '</li></ul></div>'
        + '<p class="nli__note">' + f(esc(T.mapNote), { label: esc(tr('label', d.thresholdsLabel)), pfos: F.num(d.thresholds.pfos, 1), pfoa: F.num(d.thresholds.pfoa, 1) }) + '</p>'
        + '<details class="nli__table" open><summary>' + esc(T.tableSummary) + '</summary><div class="nli__tw"><table><thead><tr><th scope="col">' + esc(T.thPlot) + '</th><th scope="col">' + esc(T.thStatus) + '</th><th scope="col" class="ph">' + esc(T.thStage) + '</th><th scope="col">' + esc(T.thPfos) + '</th></tr></thead><tbody>'
        + order.map(function (r) { return '<tr><td><button type="button" class="nls__row" data-p="' + esc(r.plot) + '">' + esc(r.plot) + '</button></td><td>' + esc(ST[r.status] || '') + '</td><td class="ph">' + esc(r.phase ? tr('stage', r.phase.stage) : '') + '</td><td class="n">'
          + (r.pfosX ? xs(r.pfosX) : '') + '</td></tr>'; }).join('') + '</tbody></table></div></details>'
        + '<p class="nli__src">' + f(esc(T.srcLine), { src: esc(tr('sources', d.sourcesNote)), date: esc(F.date(d.built)) }) + '</p></div>';
      var card = root.querySelector('.nls__card'), mapEl = root.querySelector('.nls__map'), map = null, sel = null;

      function ask(n, mkt) {  // one tap to us on WhatsApp about this plot; nothing is collected on the page
        var t = f(mkt ? T.askMsgProj : T.askMsgPlot, { n: n });
        return '<a class="nls__ask" href="' + WA + encodeURIComponent(t) + '" target="_blank" rel="noopener">' + f(esc(mkt ? T.askBtnProj : T.askBtnPlot), { n: esc(n) }) + '</a>';
      }
      function plotCard(p) {
        var r = p.ref ? recs[p.ref] : null;
        var pj = projByOid[p.oid] || (r ? r.oids.map(function (o) { return projByOid[o]; }).filter(Boolean)[0] : null);
        if (!r && pj) {
          return '<p class="nls__ct">' + f(esc(T.plot), { n: esc(p.n) }) + '<span> · ' + esc(tr('use', p.use)) + '</span></p><p class="nls__badge is-proj">' + esc(T.badgeProj) + '</p>'
            + '<p class="nls__proj">' + esc(tr('fact', pj.fact)) + '</p><p class="nls__plan">' + esc(T.greenNote) + '</p>' + ask(p.n, true);
        }
        if (!r) {
          return '<p class="nls__ct">' + f(esc(T.plot), { n: esc(p.n) }) + '<span> · ' + esc(tr('use', p.use)) + (p.m2 ? ' · ' + f(esc(T.m2), { n: F.num(p.m2) }) : '') + '</span></p><p class="nls__badge">' + esc(T.badgeNone) + '</p>'
            + '<p class="nls__txt">' + f(esc(T.noneTxt), { date: esc(F.date(d.built)) }) + '</p>'
            + '<p class="nls__plan">' + f(esc(T.plan), { p: esc(tr('plan', p.plan)) }) + '</p>' + ask(p.n, false);
        }
        var h = '<p class="nls__ct">' + f(esc(T.plot), { n: esc(r.plot) }) + '<span> · ' + esc(tr('use', r.use || p.use)) + '</span></p><p class="nls__badge is-' + r.status.split('_')[0] + '">' + esc(ST[r.status]) + '</p>';
        if (r.status === 'published_report') {
          h += '<div class="nli__answer"><span class="nli__alab">' + esc(T.peakLab) + '</span><output class="nli__fig is-survey">' + xs(r.pfosX) + '</output><span class="nli__asub">'
            + f(esc(T.ng), { n: F.num(r.pfosMax) }) + (r.pfosDepth != null ? f(esc(T.depth), { m: m1(r.pfosDepth) }) : '') + '</span></div>'
            + '<dl class="nli__lines"><dt>' + esc(T.holesOver) + '</dt><dd>' + f(T.ofN, { a: F.num(r.pfosHoles), b: F.num(r.holes) }) + '</dd>'
            + (r.pfoaX ? '<dt>' + esc(T.pfoaPeak) + '</dt><dd>' + (r.pfoaX > 1 ? xs(r.pfoaX) + (r.pfoaHoles ? ' · ' + f(esc(T.nHoles), { n: F.num(r.pfoaHoles) }) : '') : esc(T.below)) + '</dd>' : '')
            + (span(r.dates) ? '<dt>' + esc(T.sampled) + '</dt><dd>' + span(r.dates) + '</dd>' : '') + (dt(r.report) ? '<dt>' + esc(T.report) + '</dt><dd>' + dt(r.report) + '</dd>' : '')
            + '</dl>';
          if (r.bh.some(function (b) { return b.approx; })) h += '<p class="nls__plan">' + esc(T.approx) + '</p>';
        }
        if (NOTE[r.plot]) h += '<p class="nls__txt">' + esc(NOTE[r.plot][LG]) + '</p>';
        if (r.phase) { var pre = new RegExp(T.mktPrefix), stg = tr('stage', r.phase.stage), fact = pj ? tr('fact', pj.fact) : '';
          h += '<p class="nls__proj"><b>' + esc(r.phase.mkt ? T.phaseMkt : T.phaseStage) + ':</b> ' + esc(r.phase.mkt ? fact + (stg.replace(pre, '') ? (pj ? ' · ' : '') + stg.replace(pre, '') : '') || T.inMkt : stg) + '</p>'; }
        h += (r.src ? '<p class="nls__links"><a href="' + esc(r.src) + '" target="_blank" rel="noopener">' + esc(T.reportLink) + '</a></p>' : '') + ask(r.plot, r.phase && r.phase.mkt);
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
        var hit = q.replace(/\D/g, '');
        if (!hit) { card.innerHTML = '<p class="nls__txt">' + esc(T.findHint) + '</p>'; return; }
        var p = byPlot(hit); if (p) { select(p, true); mapEl.scrollIntoView({ block: 'nearest', behavior: 'smooth' }); }
        else card.innerHTML = '<p class="nls__txt">' + f(esc(T.findNone), { q: esc(q) }) + '</p>'; }
      root.querySelector('.nls__chips').addEventListener('click', function (e) { var b = e.target.closest('button'); if (b) find(b.getAttribute('data-p')); });
      root.querySelector('tbody').addEventListener('click', function (e) { var b = e.target.closest('.nls__row'); if (b) find(b.getAttribute('data-p')); });
      var inp = root.querySelector('.nls__q input');
      inp.addEventListener('keydown', function (e) { if (e.key === 'Enter') { e.preventDefault(); find(inp.value); } });
      inp.addEventListener('change', function () { find(inp.value); });
      select(byPlot(S.top.plot), false);

      loadML(function (err) {
        if (err || !window.maplibregl) { mapEl.innerHTML = '<p class="nls__wait">' + esc(T.mapFail) + '</p>'; return; }
        var gl = window.maplibregl, b0 = new gl.LngLatBounds();
        d.records.forEach(function (r) { r.oids.forEach(function (o) { var q = byOid[o]; if (q) q.g.forEach(function (ring) { ring.forEach(function (c) { b0.extend(c); }); }); }); });
        mapEl.innerHTML = '';
        map = new gl.Map({ container: mapEl, style: STYLE, bounds: b0, fitBoundsOptions: { padding: phone ? 24 : 60 }, pitch: phone ? 40 : 52, bearing: -28, maxPitch: 70,
          attributionControl: { compact: true }, cooperativeGestures: phone,
          locale: { 'CooperativeGesturesHandler.MobileHelpText': T.gMobile, 'CooperativeGesturesHandler.WindowsHelpText': T.gWin, 'CooperativeGesturesHandler.MacHelpText': T.gMac } });
        if (NLI.wheelIntent) NLI.wheelIntent(map, mapEl, EN); // HAD-790: a passing wheel scrolls the page, a resting pointer zooms
        map.addControl(new gl.NavigationControl({ visualizePitch: true }), EN ? 'top-right' : 'top-left');  // the controls sit at the reading start's far side: left in Hebrew, right in English
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
          map.addSource('nls-green', { type: 'geojson', data: { type: 'FeatureCollection', features: greens() } });
          map.addLayer({ id: 'nls-green', type: 'fill-extrusion', source: 'nls-green', paint: { 'fill-extrusion-color': ['match', ['get', 'kind'], 'tower', '#3E8E5A', '#86C298'],
            'fill-extrusion-height': ['get', 'h'], 'fill-extrusion-base': 0, 'fill-extrusion-opacity': 0.88 } });
          map.on('click', 'nls-green', function (e) { var c = e.lngLat, hit = d.plots.filter(function (q) { return projByOid[q.oid] && inside([c.lng, c.lat], q.g); })[0]; if (hit) { select(hit, false); e.preventDefault(); } });
          map.addLayer({ id: 'nls-sel', type: 'line', source: 'nls-plots', filter: ['in', ['get', 'oid'], ['literal', []]], paint: { 'line-color': '#12202A', 'line-width': 3.2 } });
          map.addLayer({ id: 'nls-holes', type: 'circle', source: 'nls-holes', paint: { 'circle-color': xcol, 'circle-radius': ['interpolate', ['linear'], ['zoom'], 14, 3, 17, 7, 19, 11],
            'circle-stroke-color': '#FFFFFF', 'circle-stroke-width': 1.4, 'circle-pitch-alignment': 'map' } });
          map.addLayer({ id: 'nls-lab', type: 'symbol', source: 'nls-plots', filter: ['==', ['get', 'lab'], 1], layout: { 'text-field': ['get', 'n'], 'text-font': ['Noto Sans Regular'], 'text-size': 13, 'text-allow-overlap': false },
            paint: { 'text-color': '#12202A', 'text-halo-color': '#FFFFFF', 'text-halo-width': 1.6 } });
          map.on('click', 'nls-holes', function (e) { var p = e.features[0].properties;
            new gl.Popup({ className: 'nls-pop', maxWidth: '260px' }).setLngLat(e.lngLat).setHTML('<p><b>' + f(esc(T.popHole), { id: esc(p.id), plot: esc(p.plot) }) + '</b></p><p>PFOS: ' + (p.x > 0 ? f(esc(T.popOver), { x: xs(p.x), ng: F.num(p.pfos) }) : esc(T.popBelowRL))
              + (p.dep ? f(esc(T.depth), { m: m1(p.dep) }) : '') + '</p>' + (p.pfoa ? '<p>PFOA: ' + (p.pfoa / d.thresholds.pfoa > 1 ? f(esc(T.popPfoaOver), { x: xs(p.pfoa / d.thresholds.pfoa) }) : esc(T.below)) + '</p>' : '') + (p.approx ? '<p class="nls__plan">' + esc(T.popApprox) + '</p>' : '')).addTo(map); e.preventDefault(); });
          map.on('click', 'nls-fill', function (e) { if (e.defaultPrevented) return; var o = e.features[0].properties.oid, p = byOid[o]; if (p) select(p, false); });
          ['nls-holes', 'nls-fill'].forEach(function (l) { map.on('mouseenter', l, function () { map.getCanvas().style.cursor = 'pointer'; }); map.on('mouseleave', l, function () { map.getCanvas().style.cursor = ''; }); });
          var at = mapEl.querySelector('.maplibregl-ctrl-attrib'); if (at) at.classList.remove('maplibregl-compact-show');  // the credit stays one tap away; it is also printed under the map
          if (sel) select(sel, false);
        });
        var b3 = root.querySelector('.nls__3d');
        b3.addEventListener('click', function () { var on = b3.getAttribute('aria-pressed') !== 'true'; b3.setAttribute('aria-pressed', on ? 'true' : 'false');
          map.easeTo({ pitch: on ? (phone ? 40 : 52) : 0, bearing: on ? -28 : 0, duration: 700 }); ['nls-3d', 'nls-green'].forEach(function (l) { if (map.getLayer(l)) map.setLayoutProperty(l, 'visibility', on ? 'visible' : 'none'); }); });
      });
    }
  });
})();
