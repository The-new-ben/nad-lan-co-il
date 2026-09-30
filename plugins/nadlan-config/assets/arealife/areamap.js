/* AreaMap (design system AreaLife v97, 28.9.2026): the project page's area map answers "what is around" at once.
 * The owner, 28.9: "the maps are not rich enough ... people want to know what's around; make them much more functional".
 * Codex (28.9): named places, not anonymous dots; seven daily-life groups; walking time from real routes (where the project
 * has them) and never a circle posing as a walking area; a list in step with the map; every place with its source.
 * It takes over only the places layer of the page's one area map (inc/project-experience.php, window.NLPJX_MAP): prices,
 * plans, 3D and satellite stay as they are. Data: the project's place registry when it has one (data-places, e.g.
 * rainbow/places.json: findplace.co.il = Tel Aviv-Yafo open data + OpenStreetMap, walking minutes by Mapbox, 5/10/15-minute
 * walking areas), else the page's own OpenStreetMap places (window.NLPJX_POIS, distance in a straight line). */
(function () {
  'use strict';
  var host = document.getElementById('nlpjx-unimap');
  if (!host) return;
  var LANG = (host.getAttribute('data-lang') || 'he').slice(0, 2);
  var RTL = LANG === 'he' || LANG === 'ar';
  var T = {
    he: { g: { education: 'חינוך', outdoors: 'פארקים וספורט', transport: 'תחבורה', food: 'קפה ומסעדות', essentials: 'קניות וסידורים', health: 'בריאות', community: 'קהילה ותרבות' },
      walk: 'דק׳ הליכה', min: 'דק׳', all: 'הכל', within: 'בהליכה של', air: 'בקו אווירי', m: 'מ׳', km: 'ק״מ', planned: 'מתוכננת', near: 'הקרובים ביותר', more: 'עוד', page: 'לעמוד המקום ב-findplace',
      sumPre: 'ב־{t}: ', sumAir: 'עד {t} בקו אווירי: ', and: ' ו־', srcReg: 'מקומות: findplace.co.il (עיריית תל אביב-יפו, מידע פתוח) ו-OpenStreetMap. זמני הליכה: מסלול הליכה של Mapbox מהבניין; השטחים הצבועים משוערים.', srcOsm: 'מקומות: OpenStreetMap. המרחקים בקו אווירי מהפרויקט.', none: 'אין מקומות בטווח הזה', groupsLabel: 'מה יש בסביבה', rangeLabel: 'טווח' },
    en: { g: { education: 'Education', outdoors: 'Parks & sport', transport: 'Transport', food: 'Cafés & food', essentials: 'Shops & errands', health: 'Health', community: 'Community & culture' },
      walk: 'min walk', min: 'min', all: 'All', within: 'Within', air: 'straight line', m: 'm', km: 'km', planned: 'planned', near: 'Nearest', more: 'more', page: 'Its page on findplace',
      sumPre: 'Within {t}: ', sumAir: 'Up to {t} in a straight line: ', and: ' and ', srcReg: 'Places: findplace.co.il (Tel Aviv-Yafo open data) and OpenStreetMap. Walking times: Mapbox walking routes from the building; the shaded areas are approximate.', srcOsm: 'Places: OpenStreetMap. Distances in a straight line from the project.', none: 'No places in this range', groupsLabel: "What's around", rangeLabel: 'Range' },
    fr: { g: { education: 'Éducation', outdoors: 'Parcs et sport', transport: 'Transports', food: 'Cafés et restaurants', essentials: 'Commerces', health: 'Santé', community: 'Culture et vie locale' },
      walk: 'min à pied', min: 'min', all: 'Tout', within: 'À', air: 'à vol d’oiseau', m: 'm', km: 'km', planned: 'prévue', near: 'Les plus proches', more: 'de plus', page: 'Sa page sur findplace',
      sumPre: 'À {t} : ', sumAir: 'Jusqu’à {t} à vol d’oiseau : ', and: ' et ', srcReg: 'Lieux : findplace.co.il (données ouvertes de Tel Aviv-Jaffa) et OpenStreetMap. Temps de marche : itinéraires piétons Mapbox depuis l’immeuble ; les zones colorées sont approximatives.', srcOsm: 'Lieux : OpenStreetMap. Distances à vol d’oiseau depuis le projet.', none: 'Aucun lieu dans ce rayon', groupsLabel: 'Autour du projet', rangeLabel: 'Rayon' },
    ru: { g: { education: 'Образование', outdoors: 'Парки и спорт', transport: 'Транспорт', food: 'Кафе и рестораны', essentials: 'Магазины', health: 'Здоровье', community: 'Культура и общество' },
      walk: 'мин пешком', min: 'мин', all: 'Все', within: 'В', air: 'по прямой', m: 'м', km: 'км', planned: 'планируется', near: 'Ближайшие', more: 'ещё', page: 'Страница на findplace',
      sumPre: 'В {t}: ', sumAir: 'До {t} по прямой: ', and: ' и ', srcReg: 'Места: findplace.co.il (открытые данные Тель-Авива-Яффо) и OpenStreetMap. Время пешком: пешеходные маршруты Mapbox от здания; закрашенные зоны приблизительны.', srcOsm: 'Места: OpenStreetMap. Расстояния по прямой от проекта.', none: 'В этом радиусе мест нет', groupsLabel: 'Что вокруг', rangeLabel: 'Радиус' },
    ar: { g: { education: 'التعليم', outdoors: 'حدائق ورياضة', transport: 'المواصلات', food: 'مقاهٍ ومطاعم', essentials: 'تسوق وخدمات', health: 'الصحة', community: 'المجتمع والثقافة' },
      walk: 'دقيقة سيرًا', min: 'د', all: 'الكل', within: 'خلال', air: 'بخط مستقيم', m: 'م', km: 'كم', planned: 'مخطط لها', near: 'الأقرب', more: 'المزيد', page: 'صفحته في findplace',
      sumPre: 'خلال {t}: ', sumAir: 'حتى {t} بخط مستقيم: ', and: ' و', srcReg: 'الأماكن: findplace.co.il (بيانات تل أبيب-يافا المفتوحة) وOpenStreetMap. أوقات السير: مسارات المشي من Mapbox من المبنى؛ المناطق الملونة تقريبية.', srcOsm: 'الأماكن: OpenStreetMap. المسافات بخط مستقيم من المشروع.', none: 'لا أماكن في هذا النطاق', groupsLabel: 'ما حول المشروع', rangeLabel: 'النطاق' },
  }[LANG] || null;
  if (!T) return;
  var COLOR = { education: '#3E5A45', outdoors: '#517048', transport: '#2F6F86', food: '#8A6B3F', essentials: '#9F6F54', health: '#A93F2A', community: '#6B4F7A' };
  var ORDER = ['education', 'outdoors', 'transport', 'food', 'essentials', 'health', 'community'];
  var PATH = {
    education: '<path d="M1.5 6.2 8 3l6.5 3.2L8 9.4z"/><path d="M4 7.6v3.1c1.1 1 2.5 1.6 4 1.6s2.9-.6 4-1.6V7.6"/>',
    outdoors: '<path d="M8 14.5v-4"/><path d="M8 1.8c-2.6 0-4.2 2-4.2 4.3 0 2.3 1.9 4.1 4.2 4.1s4.2-1.8 4.2-4.1C12.2 3.8 10.6 1.8 8 1.8z"/>',
    transport: '<rect x="3.8" y="2.2" width="8.4" height="9.2" rx="2"/><path d="M3.8 7.2h8.4M5.8 14.2l1.2-2.8M10.2 14.2 9 11.4"/>',
    food: '<path d="M2.8 6h8.4v3.4A3.6 3.6 0 0 1 7.6 13h-1.2a3.6 3.6 0 0 1-3.6-3.6z"/><path d="M11.2 7h1.1a1.8 1.8 0 0 1 0 3.6h-1.1M5.4 2.4v1.8M8.6 2.4v1.8"/>',
    essentials: '<path d="M3.3 5.6h9.4l-.9 8.2H4.2z"/><path d="M5.8 5.6V4.7a2.2 2.2 0 0 1 4.4 0v.9"/>',
    health: '<path d="M6.4 2.4h3.2v4h4v3.2h-4v4H6.4v-4h-4V6.4h4z"/>',
    community: '<path d="M2.5 6.2 8 2.8l5.5 3.4M3.6 6.6v6.2M6.5 6.6v6.2M9.5 6.6v6.2M12.4 6.6v6.2M2.2 13.6h11.6"/>',
  };
  var svg = function (g, stroke) { return '<svg viewBox="0 0 16 16" fill="none" stroke="' + (stroke || 'currentColor') + '" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">' + PATH[g] + '</svg>'; };
  /* v104.3 (30.9): a place shows the icon of its KIND (assets/arealife/place-icons.js, loaded before this file): a school is a
     school, a café a cup, a bus stop a bus. The seven group icons above stay for the group chips and as the fallback. */
  var PI = function () { return window.NLPlaceIcons || null; };
  var kindSvg = function (p, stroke) { var I = PI(); return I ? I.svg(p.k, p.g, stroke, 2.2) : svg(p.g, stroke); };
  var hasHe = function (s) { return /[֐-׿]/.test(s || ''); };
  var fmtM = function (m) { return m < 1000 ? (Math.round(m / 10) * 10) + ' ' + T.m : (Math.round(m / 100) / 10) + ' ' + T.km; };
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };

  /* ---------------- the data: the registry, or the page's OSM places ---------------- */
  var REG = null, PLACES = [], ISO = [];
  /* on a language page a place with a Hebrew-only name is shown by its kind in the page's language ("Café", "School"):
     no Hebrew on the page, and the counts stay true */
  var NOUN = {
    en: { school: 'School', kindergarten: 'Kindergarten', daycare: 'Daycare', library: 'Library', park: 'Park', playground: 'Playground', dog_park: 'Dog park', beach: 'Beach', sport: 'Sports ground', gym: 'Gym', pitch: 'Sports ground', tram_stop: 'Light-rail station', bus_stop: 'Bus stop', cafe: 'Café', restaurant: 'Restaurant', bar: 'Bar', bakery: 'Bakery', supermarket: 'Supermarket', shopping: 'Shop', pharmacy: 'Pharmacy', bank: 'Bank', health: 'Clinic', clinic: 'Clinic', community: 'Community centre', culture: 'Culture venue', worship: 'Place of worship' },
    fr: { school: 'École', kindergarten: 'Jardin d’enfants', daycare: 'Crèche', library: 'Bibliothèque', park: 'Parc', playground: 'Aire de jeux', dog_park: 'Parc canin', beach: 'Plage', sport: 'Terrain de sport', gym: 'Salle de sport', pitch: 'Terrain de sport', tram_stop: 'Station de tramway', bus_stop: 'Arrêt de bus', cafe: 'Café', restaurant: 'Restaurant', bar: 'Bar', bakery: 'Boulangerie', supermarket: 'Supermarché', shopping: 'Commerce', pharmacy: 'Pharmacie', bank: 'Banque', health: 'Clinique', clinic: 'Clinique', community: 'Centre communautaire', culture: 'Lieu culturel', worship: 'Lieu de culte' },
    ru: { school: 'Школа', kindergarten: 'Детский сад', daycare: 'Ясли', library: 'Библиотека', park: 'Парк', playground: 'Детская площадка', dog_park: 'Площадка для собак', beach: 'Пляж', sport: 'Спортплощадка', gym: 'Спортзал', pitch: 'Спортплощадка', tram_stop: 'Станция трамвая', bus_stop: 'Остановка', cafe: 'Кафе', restaurant: 'Ресторан', bar: 'Бар', bakery: 'Пекарня', supermarket: 'Супермаркет', shopping: 'Магазин', pharmacy: 'Аптека', bank: 'Банк', health: 'Клиника', clinic: 'Клиника', community: 'Общинный центр', culture: 'Место культуры', worship: 'Место молитвы' },
    ar: { school: 'مدرسة', kindergarten: 'روضة أطفال', daycare: 'حضانة', library: 'مكتبة', park: 'حديقة', playground: 'ملعب أطفال', dog_park: 'حديقة كلاب', beach: 'شاطئ', sport: 'ملعب رياضي', gym: 'نادٍ رياضي', pitch: 'ملعب رياضي', tram_stop: 'محطة قطار خفيف', bus_stop: 'موقف حافلات', cafe: 'مقهى', restaurant: 'مطعم', bar: 'حانة', bakery: 'مخبز', supermarket: 'سوبرماركت', shopping: 'متجر', pharmacy: 'صيدلية', bank: 'بنك', health: 'عيادة', clinic: 'عيادة', community: 'مركز مجتمعي', culture: 'مكان ثقافي', worship: 'مكان عبادة' },
  }[LANG] || {};
  function nameOf(p) {
    if (LANG === 'he') return p.name;
    var n = p.names || {};
    if (n[LANG]) return n[LANG];
    if (n.en) return n.en;
    if (!hasHe(p.name)) return p.name;
    return NOUN[p.k] || T.g[p.g] || null;
  }
  function fromOsm() {
    var P = window.NLPJX_POIS || {}, map = { schools: 'education', kindergartens: 'education', parks: 'outdoors', transit: 'transport', shops: 'essentials', health: 'health', food: 'food' };
    var out = [];
    Object.keys(P).forEach(function (k) {
      (P[k] || []).forEach(function (pt, i) {
        if (!pt.lat || !pt.lng || !map[k]) return;
        var kind = { schools: 'school', kindergartens: 'kindergarten', parks: 'park', transit: 'bus_stop', shops: 'shopping', health: 'clinic', food: 'restaurant' }[k];
        out.push({ id: k + i, g: map[k], k: kind, name: pt.name, lat: +pt.lat, lng: +pt.lng, dist: +pt.d || 0 });
      });
    });
    return out;
  }
  function load() {
    var url = host.getAttribute('data-places');
    if (!url) { PLACES = fromOsm(); return Promise.resolve(); }
    return fetch(url, { credentials: 'omit' }).then(function (r) { return r.ok ? r.json() : null; }).then(function (d) {
      if (d && d.places) { REG = d; PLACES = d.places.filter(function (p) { return !p.generic; }); ISO = d.iso || []; }
      else PLACES = fromOsm();
    }).catch(function () { PLACES = fromOsm(); });
  }

  /* ---------------- the state: which groups, how far ---------------- */
  var on = { education: true, outdoors: true, transport: true, food: true, essentials: false, health: false, community: false };
  var RANGES = null, range = 1; // index into RANGES
  function inRange(p) {
    var R = RANGES[range];
    if (R.all) return true;
    if (REG) return p.walk != null && p.walk <= R.v;
    return p.dist <= R.v;
  }
  function visible() {
    return PLACES.filter(function (p) { return on[p.g] && inRange(p) && nameOf(p); });
  }

  /* ---------------- the section's controls and list ---------------- */
  var sec = document.getElementById('nlpjx-map');
  var bar, rangeBar, listEl, sumEl, srcEl;
  function css() {
    var s = document.createElement('style');
    s.id = 'nlam-css';
    s.textContent = ''
      + ':root body .nlam-bar{display:flex;gap:6px;flex-wrap:wrap;margin:0 0 8px}'
      + ':root body .nlam-bar button{display:inline-flex;align-items:center;gap:7px;min-height:44px;padding:0 14px 0 6px;border-radius:999px;border:1px solid #E2DCD0;background:#fff;color:#3B4753;font:600 13.5px/1 Heebo,Assistant,sans-serif;cursor:pointer}'
      + ':root body .nlam-bar button[dir="ltr"]{padding:0 6px 0 14px}'
      + ':root body .nlam-bar button i{display:grid;place-items:center;width:30px;height:30px;border-radius:50%;background:#F3EEE3;color:#6B6558}'
      + ':root body .nlam-bar button i svg{width:16px;height:16px}'
      + ':root body .nlam-bar button b{font-weight:700;color:#8A6A2E;font-size:12.5px}'
      + ':root body .nlam-bar button[aria-pressed="true"]{background:#14212B;color:#fff;border-color:#14212B}'
      + ':root body .nlam-bar button[aria-pressed="true"] i{color:#fff}'
      + ':root body .nlam-bar button[aria-pressed="true"] b{color:#E8C572}'
      + ':root body .nlam-bar button:disabled{opacity:.45;cursor:default}'
      + ':root body .nlam-range{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:0 0 10px}'
      + ':root body .nlam-range>span{font:600 12.5px/1 Heebo,sans-serif;color:#6B6558}'
      + ':root body .nlam-range div{display:inline-flex;gap:2px;padding:3px;border-radius:999px;background:#F3EEE3}'
      + ':root body .nlam-range button{min-height:40px;min-width:56px;padding:0 12px;border:0;border-radius:999px;background:transparent;color:#3B4753;font:600 13px/1 Heebo,sans-serif;cursor:pointer}'
      + ':root body .nlam-range button[aria-pressed="true"]{background:#1F4B5C;color:#fff}'
      + ':root body .nlam-sum{margin:12px 0 8px!important;font:600 15px/1.55 Heebo,Assistant,sans-serif!important;color:#14212B!important;max-width:none!important}'
      + ':root body .nlam-sum b{color:#1F4B5C}'
      + ':root body .nlam-list{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:6px 18px;margin:6px 0 0!important;padding:0!important;list-style:none}'
      + ':root body .nlam-list li{margin:0!important}'
      + ':root body .nlam-list button{display:grid;grid-template-columns:26px minmax(0,1fr) auto;align-items:center;gap:10px;width:100%;min-height:44px;padding:4px 2px;border:0;border-bottom:1px solid #EFE9DD;background:transparent;text-align:start;cursor:pointer;font:inherit;color:#14212B}'
      + ':root body .nlam-list button:hover b{color:#1F4B5C}'
      + ':root body .nlam-list i{display:grid;place-items:center;width:26px;height:26px;border-radius:50%;color:#fff}.nlam-list i svg{width:14px;height:14px}'
      + ':root body .nlam-list b{font:700 14px/1.3 Heebo,Assistant,sans-serif;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}'
      + ':root body .nlam-list small{display:block;font:500 12px/1.3 Heebo,sans-serif;color:#6B6558}'
      + ':root body .nlam-list em{font:600 12.5px/1 Heebo,sans-serif;font-style:normal;color:#8A6A2E;white-space:nowrap}'
      + ':root body .nlam-more{margin:8px 0 0;min-height:44px;padding:0 16px;border-radius:999px;border:1px solid #E2DCD0;background:#fff;font:600 13px/1 Heebo,sans-serif;color:#1F4B5C;cursor:pointer}'
      + ':root body .nlam-src{margin:10px 0 0!important;font:400 12px/1.5 Heebo,sans-serif!important;color:#6B6558!important;max-width:none!important}'
      + '.nlam-pop b{display:block;font:700 14px/1.3 Heebo,sans-serif;color:#14212B}.nlam-pop span{display:block;font:500 12.5px/1.45 Heebo,sans-serif;color:#6B6558}.nlam-pop a{font:600 12.5px/1.6 Heebo,sans-serif;color:#1F4B5C}'
      + '@media(max-width:600px){:root body .nlam-bar{flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none;padding-bottom:2px}:root body .nlam-bar::-webkit-scrollbar{display:none}:root body .nlam-bar button{flex:none}:root body .nlam-list{grid-template-columns:1fr}}';
    document.head.appendChild(s);
  }
  function counts() {
    var c = {};
    PLACES.forEach(function (p) { if (inRange(p) && nameOf(p)) c[p.g] = (c[p.g] || 0) + 1; });
    return c;
  }
  function buildUi() {
    css();
    // the page's own POI chips give way to these (prices, plans, 3D and satellite stay)
    document.querySelectorAll('.nlpjx-maplayers button').forEach(function (b) {
      if (['schools', 'parks', 'transit', 'shops', 'health', 'food'].indexOf(b.getAttribute('data-layer')) > -1) b.remove();
    });
    bar = document.createElement('div'); bar.className = 'nlam-bar'; bar.setAttribute('role', 'group'); bar.setAttribute('aria-label', T.groupsLabel);
    ORDER.forEach(function (g) {
      var b = document.createElement('button'); b.type = 'button'; b.setAttribute('data-g', g);
      if (!RTL) b.dir = 'ltr';
      b.innerHTML = '<i style="background:' + (on[g] ? COLOR[g] : '') + '">' + svg(g) + '</i><span>' + esc(T.g[g]) + '</span><b></b>';
      b.addEventListener('click', function () { on[g] = !on[g]; refresh(); });
      bar.appendChild(b);
    });
    rangeBar = document.createElement('div'); rangeBar.className = 'nlam-range';
    var lab = document.createElement('span'); lab.textContent = T.rangeLabel + (REG ? '' : ' (' + T.air + ')'); rangeBar.appendChild(lab);
    var seg = document.createElement('div'); seg.setAttribute('role', 'group'); seg.setAttribute('aria-label', T.rangeLabel);
    RANGES.forEach(function (R, i) {
      var b = document.createElement('button'); b.type = 'button'; b.textContent = R.label;
      b.addEventListener('click', function () { range = i; refresh(); });
      seg.appendChild(b);
    });
    rangeBar.appendChild(seg);
    var layers = sec.querySelector('.nlpjx-maplayers');
    var anchor = layers || host;
    anchor.parentNode.insertBefore(bar, anchor);
    anchor.parentNode.insertBefore(rangeBar, anchor);
    sumEl = document.createElement('p'); sumEl.className = 'nlam-sum';
    listEl = document.createElement('ul'); listEl.className = 'nlam-list';
    srcEl = document.createElement('p'); srcEl.className = 'nlam-src'; srcEl.textContent = REG ? T.srcReg : T.srcOsm;
    var after = host.nextSibling;
    host.parentNode.insertBefore(sumEl, after);
    host.parentNode.insertBefore(listEl, after);
    host.parentNode.insertBefore(srcEl, after);
  }
  var shownN = window.innerWidth < 600 ? 6 : 10;
  function refresh() {
    var c = counts();
    bar.querySelectorAll('button').forEach(function (b) {
      var g = b.getAttribute('data-g'), n = c[g] || 0;
      b.setAttribute('aria-pressed', on[g] ? 'true' : 'false');
      b.querySelector('i').style.background = on[g] ? COLOR[g] : '';
      b.querySelector('b').textContent = n;
      b.disabled = !n && !on[g];
    });
    rangeBar.querySelectorAll('div button').forEach(function (b, i) { b.setAttribute('aria-pressed', i === range ? 'true' : 'false'); });
    // the summary: what the range holds, the bigger groups first
    var parts = ORDER.filter(function (g) { return c[g]; }).sort(function (a, b) { return c[b] - c[a]; }).slice(0, 4)
      .map(function (g) { return '<b>' + c[g] + '</b> ' + esc(T.g[g]); });
    var R = RANGES[range];
    var pre = R.all ? '' : (REG ? T.sumPre : T.sumAir).replace('{t}', R.label);
    sumEl.innerHTML = parts.length ? esc(pre) + parts.slice(0, -1).join(', ') + (parts.length > 1 ? esc(T.and) : '') + parts[parts.length - 1] : esc(T.none);
    drawList();
    setData();
  }
  function drawList() {
    var list = visible().sort(function (a, b) { return REG ? ((a.walk || 999) - (b.walk || 999)) : (a.dist - b.dist); });
    listEl.innerHTML = '';
    list.slice(0, shownN).forEach(function (p) {
      var li = document.createElement('li'), b = document.createElement('button'); b.type = 'button';
      var when = p.future ? T.planned : (REG && p.walk ? p.walk + ' ' + T.min : fmtM(p.dist));
      b.innerHTML = '<i style="background:' + COLOR[p.g] + '">' + kindSvg(p) + '</i><span><b><bdi>' + esc(nameOf(p)) + '</bdi></b><small>' + esc(T.g[p.g]) + (p.addr && LANG === 'he' ? ' · ' + esc(p.addr) : '') + '</small></span><em>' + esc(when) + '</em>';
      b.addEventListener('click', function () { focus(p); });
      li.appendChild(b); listEl.appendChild(li);
    });
    var old = sec.querySelector('.nlam-more'); if (old) old.remove();
    if (list.length > shownN) {
      var m = document.createElement('button'); m.type = 'button'; m.className = 'nlam-more';
      m.textContent = '+ ' + (list.length - shownN) + ' ' + T.more;
      m.addEventListener('click', function () { shownN += 20; drawList(); });
      listEl.parentNode.insertBefore(m, srcEl);
    }
  }

  /* ---------------- the map: GL layers, named at street scale ---------------- */
  var MAP = null, popup = null;
  function card(p) {
    var when = p.future ? T.planned : (REG && p.walk ? p.walk + ' ' + T.walk : fmtM(p.dist) + ' ' + T.air);
    return '<div class="nlam-pop"><b><bdi>' + esc(nameOf(p)) + '</bdi></b><span>' + esc(T.g[p.g]) + ' · ' + esc(when) + '</span>'
      + (p.addr && LANG === 'he' ? '<span>' + esc(p.addr) + '</span>' : '')
      + (p.fp ? '<a href="' + esc(p.fp) + '" target="_blank" rel="noopener">' + esc(T.page) + ' ←</a>' : '') + '</div>';
  }
  function focus(p) {
    if (!MAP) return;
    MAP.easeTo({ center: [p.lng, p.lat], zoom: Math.max(MAP.getZoom(), 16), duration: 700 });
    if (popup) popup.remove();
    popup = new window.mapboxgl.Popup({ offset: 16, maxWidth: '280px' }).setLngLat([p.lng, p.lat]).setHTML(card(p)).addTo(MAP);
    try { host.scrollIntoView({ behavior: 'smooth', block: 'center' }); } catch (e) {}
  }
  function fc() {
    return { type: 'FeatureCollection', features: visible().map(function (p, i) {
      return { type: 'Feature', id: i, geometry: { type: 'Point', coordinates: [p.lng, p.lat] }, properties: { i: PLACES.indexOf(p), g: p.g, ic: iconId(p), name: nameOf(p), rank: (REG ? (p.walk || 99) : p.dist / 80) } };
    }) };
  }
  function setData() { if (MAP && MAP.getSource('nlam')) MAP.getSource('nlam').setData(fc()); if (MAP && MAP.getLayer('nlam-iso')) isoFilter(); }
  function isoFilter() {
    var R = RANGES[range];
    MAP.setFilter('nlam-iso', R.all ? ['<=', ['get', 'min'], 0] : ['==', ['get', 'min'], R.v]);
    MAP.setFilter('nlam-iso-line', R.all ? ['<=', ['get', 'min'], 0] : ['==', ['get', 'min'], R.v]);
  }
  /* v104.3: the map pin of a place = the icon of its kind in its group colour. Codex (30.9) found the old pins painted black:
     the regex stripped the <svg> wrapper together with fill="none" stroke="#fff". The <g> below carries them. */
  function iconId(p) { var I = PI(); return 'nlpi-' + (I ? I.glyph(p.k, p.g) : 'g') + '-' + p.g; }
  function pinSrc(p) {
    var I = PI();
    if (I) return I.pinSvg(p.k, p.g, 52);
    return '<svg xmlns="http://www.w3.org/2000/svg" width="52" height="52" viewBox="0 0 52 52"><circle cx="26" cy="26" r="23" fill="' + COLOR[p.g] + '" stroke="#FAF7F1" stroke-width="3"/>'
      + '<g transform="translate(14 14) scale(1.5)" fill="none" stroke="#fff" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">' + PATH[p.g] + '</g></svg>';
  }
  function icons(map) {
    var need = {};
    PLACES.forEach(function (p) { var id = iconId(p); if (!need[id]) need[id] = p; });
    return Promise.all(Object.keys(need).map(function (id) {
      return new Promise(function (res) {
        var img = new Image(52, 52);
        img.onload = function () { try { if (!map.hasImage(id)) map.addImage(id, img, { pixelRatio: 2 }); } catch (e) {} res(); };
        img.onerror = function () { res(); };
        img.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(pinSrc(need[id]));
      });
    }));
  }
  function mount(map) {
    MAP = map;
    icons(map).then(function () {
      if (ISO.length) {
        map.addSource('nlam-iso', { type: 'geojson', data: { type: 'FeatureCollection', features: ISO.map(function (r) { return { type: 'Feature', properties: { min: r.min }, geometry: { type: 'Polygon', coordinates: [r.ring] } }; }) } });
        map.addLayer({ id: 'nlam-iso', type: 'fill', source: 'nlam-iso', paint: { 'fill-color': '#2F6F86', 'fill-opacity': 0.08 } });
        map.addLayer({ id: 'nlam-iso-line', type: 'line', source: 'nlam-iso', paint: { 'line-color': '#1F4B5C', 'line-width': 1.6, 'line-dasharray': [2, 1.5], 'line-opacity': 0.7 } });
      }
      map.addSource('nlam', { type: 'geojson', data: fc() });
      // v104.3: every place that has room shows its icon AND its name, as one unit (Codex: never an orphan icon); the nearest
      // wins a collision (sort key = walking minutes), the far ones step back instead of piling up. At every zoom a
      // place shows with its name or not at all; every place stays in the list under the map.
      map.addLayer({ id: 'nlam-pin', type: 'symbol', source: 'nlam', layout: {
        'icon-image': ['get', 'ic'], 'icon-size': ['interpolate', ['linear'], ['zoom'], 12, 0.72, 14, 0.88, 16, 1],
        'icon-allow-overlap': false, 'icon-padding': 1,
        'symbol-sort-key': ['get', 'rank'],
        // v104.5 (Codex's QA, M15): names from the first frame; the collision thins, never an anonymous icon
        'text-field': ['get', 'name'], 'text-font': ['DIN Pro Medium', 'Arial Unicode MS Regular'],
        'text-size': ['interpolate', ['linear'], ['zoom'], 14, 12, 17, 13.5],
        'text-variable-anchor': RTL ? ['right', 'left', 'top', 'bottom'] : ['left', 'right', 'top', 'bottom'],
        'text-radial-offset': 1.2, 'text-justify': 'auto', 'text-optional': false, 'icon-optional': false, 'text-max-width': 9, 'text-padding': 2 },
        paint: { 'text-color': '#14212B', 'text-halo-color': 'rgba(250,247,241,.96)', 'text-halo-width': 1.8 } });
      if (ISO.length) isoFilter();
      // v104.6: the project is a REQUIRED mark (Google's collision term): its name under the page's own dot, placed before the
      // places (this layer sits above them), and a transparent reserve for the 20 px dot, so the places make room instead of covering it
      var hlat = parseFloat(host.getAttribute('data-lat')), hlng = parseFloat(host.getAttribute('data-lng')), htitle = (host.getAttribute('data-title') || '').split(/\s[-–|]\s/)[0].trim(); // the name before an SEO tail ("מגדלי DUO תל אביב - ...")
      if (isFinite(hlat) && isFinite(hlng) && htitle) {
        try {
          if (!map.hasImage('nlam-reserve')) map.addImage('nlam-reserve', { width: 56, height: 56, data: new Uint8Array(56 * 56 * 4) }, { pixelRatio: 2 });
          map.addSource('nlam-home', { type: 'geojson', data: { type: 'Feature', geometry: { type: 'Point', coordinates: [hlng, hlat] }, properties: { name: htitle } } });
          map.addLayer({ id: 'nlam-home', type: 'symbol', source: 'nlam-home', layout: {
            'icon-image': 'nlam-reserve', 'icon-allow-overlap': true, 'icon-ignore-placement': false,
            'text-field': ['get', 'name'], 'text-font': ['DIN Pro Bold', 'Arial Unicode MS Bold'], 'text-size': 13.5, 'text-anchor': 'top',
            'text-offset': [0, 1.15], 'text-max-width': 12, 'text-allow-overlap': true, 'text-ignore-placement': false },
            paint: { 'text-color': '#1B1A17', 'text-halo-color': 'rgba(250,247,241,.98)', 'text-halo-width': 2.2 } });
          // the page's HTML chips (prices, plans) sit above the map and outside its collision: where one covers the name's box, the
          // name steps back (the dot's own popup still names the project); checked after every move
          var homeCheck = function () {
            if (!map.getLayer('nlam-home')) return;
            var c = map.getContainer(), bx = c.getBoundingClientRect(), p = map.project([hlng, hlat]);
            var w = Math.min(162, htitle.length * 7.6), r = { l: p.x - w / 2, r: p.x + w / 2, t: p.y + 14, b: p.y + 38 }, hit = false;
            c.querySelectorAll('.mapboxgl-marker').forEach(function (m) {
              var q = m.getBoundingClientRect(), x0 = q.left - bx.left, y0 = q.top - bx.top;
              if (q.width && x0 < r.r && x0 + q.width > r.l && y0 < r.b && y0 + q.height > r.t) hit = true;
            });
            map.setLayoutProperty('nlam-home', 'visibility', hit ? 'none' : 'visible');
          };
          map.on('moveend', homeCheck); setTimeout(homeCheck, 900);
        } catch (e) {}
      }
      // v104.5 (Codex's QA, M15): the right-to-left text plugin loads lazily, and the tiles laid out before it lands keep their
      // Hebrew and Arabic labels EMPTY (Latin text showed at zoom 14.4, Hebrew did not). Once it is loaded, the places and the
      // basemap's name labels are laid out again (an equivalent expression: an identical one would be a no-op).
      var tries = 0;
      (function relayout() {
        var st = window.mapboxgl && window.mapboxgl.getRTLTextPluginStatus ? window.mapboxgl.getRTLTextPluginStatus() : 'loaded';
        if (st === 'unavailable' || st === 'error') return;
        if (st !== 'loaded') { if (++tries < 60) setTimeout(relayout, 400); return; }
        try { map.setLayoutProperty('nlam-pin', 'text-field', ['to-string', ['get', 'name']]); } catch (e) {}
        try { if (map.getLayer('nlam-home')) map.setLayoutProperty('nlam-home', 'text-field', ['to-string', ['get', 'name']]); } catch (e) {}
        try {
          (map.getStyle().layers || []).forEach(function (l) {
            var tf = l.type === 'symbol' && l.id !== 'nlam-pin' ? map.getLayoutProperty(l.id, 'text-field') : null;
            if (Array.isArray(tf) && tf[0] === 'coalesce' && JSON.stringify(tf).indexOf('"name') > -1) map.setLayoutProperty(l.id, 'text-field', ['to-string', tf]);
          });
        } catch (e) {}
      })();
      map.on('click', 'nlam-pin', function (e) { var f = e.features && e.features[0]; if (f) focus(PLACES[f.properties.i]); });
      map.on('mouseenter', 'nlam-pin', function () { map.getCanvas().style.cursor = 'pointer'; });
      map.on('mouseleave', 'nlam-pin', function () { map.getCanvas().style.cursor = ''; });
    });
  }
  function start() {
    load().then(function () {
      RANGES = REG
        ? [{ v: 5, label: '5 ' + T.min }, { v: 10, label: '10 ' + T.min }, { v: 15, label: '15 ' + T.min }, { all: 1, label: T.all }]
        : [{ v: 400, label: fmtM(400) }, { v: 800, label: fmtM(800) }, { v: 1200, label: fmtM(1200) }, { all: 1, label: T.all }];
      buildUi(); refresh();
      var go = function (map) { if (map.isStyleLoaded()) mount(map); else map.once('load', function () { mount(map); }); };
      if (window.NLPJX_MAP) go(window.NLPJX_MAP);
      else document.addEventListener('nlpjx:map', function () { go(window.NLPJX_MAP); }, { once: true });
    });
  }
  window.NLPJX_AREALIFE = 1; // the page's inline map leaves its places to this
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
