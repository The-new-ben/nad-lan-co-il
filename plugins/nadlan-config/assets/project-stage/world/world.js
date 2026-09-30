/*
 * The shared 3D WORLD module (design system v104 "KikarHamedinaWorld", HAD-375, phase P5).
 * One scene, four ways in: aerial, walk, tower (floor, facing, window view, sun clock) and places.
 *
 *   import { mountWorld } from '/wp-content/plugins/nadlan-config/assets/project-stage/world/world.js';
 *   const w = mountWorld(document.getElementById('x'), {
 *     dataUrl: '.../hamedina/world.json', placesUrl: '.../hamedina/places.json', lang: 'he',
 *     i18n: { he: { ... } }, onPick: (p) => {}, poster: { src, srcset }, intent: 'visible' });
 *   await w.ready;
 *   w.setMode('tower'); w.pickTower('A'); w.setFloor(30); w.setFacing(270); w.setSun({ season: 6, hour: 17 });
 *   w.destroy();
 *
 * The handle: ready (a promise), setMode('aerial'|'walk'|'tower'|'places'), pickTower('A'|'B'|'C'), setFloor(n),
 * setFacing(bearing | { index }), setSun({ season: 3|6|9|12, hour: 5-20 }), setView('out'|'window'), setCategory(group),
 * pickPlace(id), walkTo('ring'|'park'|'towers'|'school'), show(kind, id) (opens a card: tower, civic, feature, park, pond,
 * road, ring, square, block, place, mark), closeCard(), collapse(bool), project(x, y, z), getState(), sunHours(tower, floor,
 * bearing, season), stats(), bench(ms), destroy(). Methods called before the world is ready wait for it.
 * Options: see DEFAULTS below (poster, intent, mode, season, hour, wa, motion, maxDpr, shadows, labels, chrome, adaptive).
 *
 * The page needs the import map for "three" and "three/addons/" (three@0.170.0 on jsDelivr), the same one the project
 * stages use (inc/project-stage.php). three.js and the world data load only on intent, after the poster has painted.
 *
 * Events on window (detail.source is 'user' or 'api'):
 *   nl:floor   { tower, floor, heightM, source }                    a tower floor was chosen
 *   nl:facing  { tower, floor, heightM, bearing, facing, source }   a facing was chosen (bearing: degrees clockwise from true north)
 * window.__nlpsPick = { tower, floor, facing, ... } after a pick, so the site's WhatsApp line names them (inc/wa-source.php
 * prints `floor`, inc/cta-sheet.php prints `floor` and `facing`): `floor` is the floor number followed by the tower's name.
 *
 * Honesty: every fact line in a card comes from the world data with its source; the towers are an illustration (the municipal
 * footprint + the published 1.25° turn); what is provisional is labelled in the card and in the data (model.notes).
 */

let THREE = null;
let OrbitControls = null;
let mergeGeometries = null;

const DEG = Math.PI / 180;
const MODES = ['aerial', 'walk', 'tower', 'places'];

const I18N = {
  he: {
    region: 'מגדלי כיכר המדינה והשכונה סביבם, בהדמיה',
    eyebrow: 'מגדלי כיכר המדינה · תל אביב',
    modes: { aerial: 'מבט על', walk: 'סיור ברגל', tower: 'קומה ונוף', places: 'מה בסביבה' },
    enter: 'לסיור בכיכר',
    loading: 'טוענים את הכיכר',
    full: 'מסך מלא', unfull: 'יציאה ממסך מלא', close: 'סגירה', north: 'צפון למעלה',
    aerialTitle: 'הכיכר, הפארק והשכונה',
    aerialIntro: 'בחרו מגדל, גן, בניין או מקום כדי לראות את הפרטים.',
    goTower: 'בחרו מגדל',
    walkTitle: 'סיור ברגל בכיכר',
    walkIntro: 'בגובה העיניים, על טבעת ה׳ באייר ובשבילי הפארק.',
    walkKeysDesk: 'גררו כדי להסתכל · <kbd>W</kbd><kbd>A</kbd><kbd>S</kbd><kbd>D</kbd> או החצים כדי ללכת · <kbd>Shift</kbd> מהר יותר',
    walkKeysTouch: 'גררו כדי להסתכל · הכפתור העגול כדי ללכת',
    spots: { ring: 'טבעת ה׳ באייר', park: 'לב הפארק', towers: 'בין המגדלים', school: 'ליד בית הספר' },
    towerTitle: (k, f) => (f ? `מגדל ${k} · קומה ${f}` : `מגדל ${k}`),
    tower: 'מגדל', towerN: (k) => `מגדל ${k}`,
    floor: 'קומה', floorN: (f) => `קומה ${f}`,
    floorsN: (n) => `${n} קומות`,
    meters: (m) => `${m} מ׳`,
    eye: (h) => `גובה העיניים כ-${h} מ׳`,
    facingLbl: 'כיוון המבט',
    dirs: ['צפונה', 'צפון-מזרחה', 'מזרחה', 'דרום-מזרחה', 'דרומה', 'דרום-מערבה', 'מערבה', 'צפון-מערבה'],
    dirsShort: ['צפון', 'צפון-מזרח', 'מזרח', 'דרום-מזרח', 'דרום', 'דרום-מערב', 'מערב', 'צפון-מערב'],
    sunOpen: 'שעון השמש',
    illusSpot: 'מיקום להמחשה',
    notesSum: 'מה בתמונה להמחשה',
    towersHere: 'מגדלי כיכר המדינה',
    floorTag: (f) => `קומה ${f}`,
    srcNames: { osm: 'OpenStreetMap', tlv: 'עיריית תל אביב-יפו, מידע פתוח', gis: 'עיריית תל אביב-יפו, מידע גאוגרפי פתוח', 'tlv-gis': 'עיריית תל אביב-יפו, מידע גאוגרפי פתוח', gtfs: 'משרד התחבורה', fp: 'findplace.co.il', walk: 'Mapbox, זמן הליכה', lines: 'Open Bus Stride, משרד התחבורה' },
    faces: (w) => `פונה ${w}`,
    viewOut: 'המגדל מבחוץ', viewWin: 'הנוף מהחלון',
    pickFacing: 'בחרו כיוון כדי לראות את הנוף מהחלון',
    sun: 'שמש וצל',
    seasons: { 3: '21.3', 6: '21.6', 9: '21.9', 12: '21.12' },
    seasonsLong: { 3: '21 במרץ', 6: '21 ביוני', 9: '21 בספטמבר', 12: '21 בדצמבר' },
    hour: 'שעה',
    sunNow: (alt, az) => `השמש בגובה ${alt}° מכיוון ${az}°`,
    sunDown: 'השמש מתחת לאופק',
    riseSet: (r, s) => `זריחה ${r} · שקיעה ${s}`,
    sunHours: (h, d) => `כ-${h} שעות שמש ישירה בחלון הזה ב-${d}`,
    sunNone: (d) => `בכיוון הזה אין שמש ישירה ב-${d}`,
    sunOnNow: 'השמש על החלון בשעה הזו', sunOffNow: 'החלון בצל בשעה הזו',
    sunNote: 'לפי מסלול השמש בתל אביב וגובה הבניינים מסביב; בלי עצים, מרפסות ותריסים.',
    hoursShort: (h) => `${h} ש׳`,
    placesTitle: 'מה בסביבה',
    placesIntro: 'זמני ההליכה נמדדו מטבעת הכיכר, מהצד שפונה אל המקום.',
    cats: { transport: 'תחבורה', education: 'חינוך', outdoors: 'פארקים וספורט', food: 'קפה ומסעדות', essentials: 'קניות ושירותים', health: 'בריאות', community: 'קהילה ותרבות' },
    catCount: (n, m) => `${n} מקומות במרחק של עד ${m} דק׳ הליכה`,
    walkMin: (m) => `${m} דק׳ הליכה`,
    fromRing: 'מטבעת הכיכר',
    km: (m) => (m >= 1000 ? `${(m / 1000).toFixed(1)} ק״מ` : `${Math.round(m / 10) * 10} מ׳`),
    fromTowers: (d) => `כ-${d} ממרכז המתחם`,
    routeNote: 'המסלול המסומן: הערכה על צירי הרחובות של העירייה. זמן ההליכה: Mapbox.',
    routeAir: 'קו ישר אל המקום; זמן ההליכה: Mapbox.',
    lines: 'קווים',
    source: 'מקור',
    illus: 'הדמיה להמחשה בלבד',
    caption: 'הדמיה להמחשה בלבד · בניינים, גבהים, רחובות, גנים ועצים: עיריית תל אביב-יפו · המגדלים: קונטור הבניין במאגר העירייה וסיבוב של 1.25° בכל קומה',
    block: 'בניין', blockPublic: 'מבנה ציבור', blockBuilding: 'בבנייה',
    hSrc: ['גובה לפי מדידת העירייה, 2019', 'גובה לפי מאגר העירייה', 'גובה לפי מדידת פני השטח של העירייה', 'גובה משוער לפי מספר הקומות'],
    heightAbout: (h) => `גובה כ-${h} מ׳`,
    built: (y) => `נבנה ב-${y}`,
    street: 'רחוב', green: 'שטח ירוק ציבורי', water: 'מים', tree: 'עץ',
    treeLine: 'עצי העיר לפי חופות העצים שמיפתה העירייה ב-2024; גובה העץ בתמונה להמחשה.',
    park: 'הפארק בכיכר', pond: 'האגם האקולוגי', road: 'טבעת ה׳ באייר', ringBld: 'בנייני הטבעת של הכיכר', square: 'כיכר המדינה',
    towersAll: 'מגדלי כיכר המדינה',
    mark: 'נקודת ציון', markDist: (d) => `${d} מהמגדלים`,
    askWa: (k, f) => (f ? `ייעוץ חינם על קומה ${f} במגדל ${k}` : `ייעוץ חינם על מגדל ${k}`),
    askPlace: 'ייעוץ חינם על החיים בכיכר',
    pickLabel: (f, k) => `${f} · מגדל ${k}`,
    notes: 'מה להמחשה',
    collapse: 'הקטנה', expand: 'הגדלה',
    kinds: {
      bus_stop: 'תחנת אוטובוס', station: 'תחנת רכבת', subway_entrance: 'כניסה לתחנת רכבת קלה', tram_stop: 'תחנת רכבת קלה',
      school: 'בית ספר', kindergarten: 'גן ילדים', daycare: 'מעון יום', library: 'ספרייה', college: 'מכללה',
      park: 'גן ציבורי', garden: 'גינה', playground: 'גן משחקים', dog_park: 'גינת כלבים', sport: 'מתקן ספורט', gym: 'חדר כושר',
      fitness_centre: 'מכון כושר', pitch: 'מגרש ספורט', sports_centre: 'מרכז ספורט', swimming_pool: 'בריכת שחייה',
      cafe: 'בית קפה', restaurant: 'מסעדה', bar: 'בר', pub: 'פאב', fast_food: 'אוכל מהיר', ice_cream: 'גלידרייה', bakery: 'מאפייה',
      supermarket: 'סופרמרקט', convenience: 'מכולת', shopping: 'חנות', mall: 'מרכז קניות', pharmacy: 'בית מרקחת', chemist: 'פארם',
      bank: 'בנק', atm: 'כספומט', post_office: 'סניף דואר', greengrocer: 'ירקן', clinic: 'מרפאה', hospital: 'בית חולים',
      health: 'שירותי בריאות', dentist: 'רופא שיניים', doctors: 'רופאים', community: 'מרכז קהילתי', culture: 'תרבות', worship: 'בית כנסת',
    },
  },
  en: {
    region: 'Kikar Hamedina Towers and the neighbourhood around them, illustrated',
    eyebrow: 'Kikar Hamedina Towers · Tel Aviv',
    modes: { aerial: 'Aerial', walk: 'Walk', tower: 'Floor view', places: 'Nearby' },
    enter: 'Explore the square',
    loading: 'Loading the square',
    full: 'Full screen', unfull: 'Exit full screen', close: 'Close', north: 'North up',
    aerialTitle: 'The square, the park and the neighbourhood',
    aerialIntro: 'Choose a tower, a garden, a building or a place to see its details.',
    goTower: 'Choose a tower',
    walkTitle: 'Walk around the square',
    walkIntro: 'At eye level, on the ה\' באייר ring and the park paths.',
    walkKeysDesk: 'Drag to look · <kbd>W</kbd><kbd>A</kbd><kbd>S</kbd><kbd>D</kbd> or the arrows to walk · <kbd>Shift</kbd> faster',
    walkKeysTouch: 'Drag to look · the round pad to walk',
    spots: { ring: 'The ring road', park: 'The park', towers: 'Between the towers', school: 'By the school' },
    towerTitle: (k, f) => (f ? `Tower ${k} · floor ${f}` : `Tower ${k}`),
    tower: 'Tower', towerN: (k) => `Tower ${k}`,
    floor: 'Floor', floorN: (f) => `Floor ${f}`,
    floorsN: (n) => `${n} floors`,
    meters: (m) => `${m} m`,
    eye: (h) => `Eye height about ${h} m`,
    facingLbl: 'Facing',
    dirs: ['north', 'north-east', 'east', 'south-east', 'south', 'south-west', 'west', 'north-west'],
    dirsShort: ['North', 'NE', 'East', 'SE', 'South', 'SW', 'West', 'NW'],
    sunOpen: 'Sun clock',
    illusSpot: 'Location for illustration',
    notesSum: 'What is illustrated',
    towersHere: 'Kikar Hamedina Towers',
    floorTag: (f) => `Floor ${f}`,
    srcNames: { osm: 'OpenStreetMap', tlv: 'Tel Aviv-Yafo municipality open data', gis: 'Tel Aviv-Yafo municipality open GIS', 'tlv-gis': 'Tel Aviv-Yafo municipality open GIS', gtfs: 'Ministry of Transport', fp: 'findplace.co.il', walk: 'Mapbox walking time', lines: 'Open Bus Stride, Ministry of Transport' },
    faces: (w) => `Facing ${w}`,
    viewOut: 'The tower', viewWin: 'The window view',
    pickFacing: 'Choose a facing to see the view from the window',
    sun: 'Sun & shade',
    seasons: { 3: '21 Mar', 6: '21 Jun', 9: '21 Sep', 12: '21 Dec' },
    seasonsLong: { 3: '21 March', 6: '21 June', 9: '21 September', 12: '21 December' },
    hour: 'Time',
    sunNow: (alt, az) => `Sun ${alt}° high, from ${az}°`,
    sunDown: 'The sun is below the horizon',
    riseSet: (r, s) => `Sunrise ${r} · sunset ${s}`,
    sunHours: (h, d) => `About ${h} hours of direct sun on this window on ${d}`,
    sunNone: (d) => `No direct sun on this facing on ${d}`,
    sunOnNow: 'Sun on the window at this time', sunOffNow: 'The window is in shade at this time',
    sunNote: 'From the sun\'s path over Tel Aviv and the heights of the buildings around; trees, balconies and shades not counted.',
    hoursShort: (h) => `${h} h`,
    placesTitle: 'Nearby',
    placesIntro: 'Walking times are measured from the square\'s ring road, on the side facing the place.',
    cats: { transport: 'Transport', education: 'Education', outdoors: 'Parks & sport', food: 'Cafés & dining', essentials: 'Shops & services', health: 'Health', community: 'Community & culture' },
    catCount: (n, m) => `${n} places within a ${m}-minute walk`,
    walkMin: (m) => `${m} min walk`,
    fromRing: 'from the ring road',
    km: (m) => (m >= 1000 ? `${(m / 1000).toFixed(1)} km` : `${Math.round(m / 10) * 10} m`),
    fromTowers: (d) => `About ${d} from the compound's centre`,
    routeNote: 'The route drawn is an estimate on the city\'s street axes. Walking time: Mapbox.',
    routeAir: 'A straight line to the place; walking time: Mapbox.',
    lines: 'Lines',
    source: 'Source',
    illus: 'Illustration only',
    caption: 'Illustration only · buildings, heights, streets, gardens and trees: Tel Aviv-Yafo municipality · the towers: the municipal footprint turned 1.25° every floor',
    block: 'Building', blockPublic: 'Public building', blockBuilding: 'Under construction',
    hSrc: ['Height from the city\'s 2019 survey', 'Height from the city\'s data', 'Height from the city\'s surface model', 'Height estimated from the floor count'],
    heightAbout: (h) => `About ${h} m high`,
    built: (y) => `Built in ${y}`,
    street: 'Street', green: 'Public green space', water: 'Water', tree: 'Tree',
    treeLine: 'Trees from the tree canopies mapped by the city in 2024; the tree height shown is an illustration.',
    park: 'The park in the square', pond: 'The ecological pond', road: 'The ה\' באייר ring', ringBld: 'The square\'s ring of buildings', square: 'Kikar Hamedina',
    towersAll: 'Kikar Hamedina Towers',
    mark: 'Landmark', markDist: (d) => `${d} from the towers`,
    askWa: (k, f) => (f ? `Free advice on floor ${f} of tower ${k}` : `Free advice on tower ${k}`),
    askPlace: 'Free advice on living at the square',
    pickLabel: (f, k) => `${f} · tower ${k}`,
    notes: 'What is illustrated',
    collapse: 'Collapse', expand: 'Expand',
    kinds: {
      bus_stop: 'Bus stop', station: 'Railway station', subway_entrance: 'Light-rail station entrance', tram_stop: 'Light-rail stop',
      school: 'School', kindergarten: 'Kindergarten', daycare: 'Daycare', library: 'Library', college: 'College',
      park: 'Public garden', garden: 'Garden', playground: 'Playground', dog_park: 'Dog park', sport: 'Sports facility', gym: 'Gym',
      fitness_centre: 'Fitness centre', pitch: 'Sports pitch', sports_centre: 'Sports centre', swimming_pool: 'Swimming pool',
      cafe: 'Café', restaurant: 'Restaurant', bar: 'Bar', pub: 'Pub', fast_food: 'Fast food', ice_cream: 'Ice cream', bakery: 'Bakery',
      supermarket: 'Supermarket', convenience: 'Grocery', shopping: 'Shop', mall: 'Shopping centre', pharmacy: 'Pharmacy', chemist: 'Drugstore',
      bank: 'Bank', atm: 'ATM', post_office: 'Post office', greengrocer: 'Greengrocer', clinic: 'Clinic', hospital: 'Hospital',
      health: 'Health services', dentist: 'Dentist', doctors: 'Doctors', community: 'Community centre', culture: 'Culture', worship: 'Synagogue',
    },
  },
};

const DEFAULTS = {
  dataUrl: null,
  placesUrl: null,
  lang: 'he',
  i18n: null,
  onPick: null,
  poster: null,          // { src, srcset, sizes } or a URL: painted at once, before any 3D
  intent: 'visible',     // 'now' | 'visible' (loads when scrolled into view) | 'tap' (loads on the button)
  mode: 'aerial',
  season: 9,             // 3 | 6 | 9 | 12 (21st of the month)
  hour: 10,              // local time, 5-20
  wa: null,              // the site's WhatsApp link for the card's button (the site's interceptor adds the source line)
  motion: true,          // false: every camera move is a cut (QA screenshots; reduced motion does the same)
  name: '',              // the project's name for window.__nlpsPick.name
  injectCss: true,
  injectFonts: true,
  maxDpr: null,          // default: 2 on desktop, 1.5 on phones
  shadows: true,
  labels: true,
  ui: true,
  chrome: true,          // false: canvas + labels only (the poster generator)
  adaptive: true,        // lower the pixel ratio (to 75% at most) when frames get slow
  logDepth: false,       // a logarithmic depth buffer (off: tighter far planes and per-layer offsets keep the ground clean)
  softShadows: true,
  pond: true,            // false: the park's pond is not drawn (its outline and place are an illustration, not published)
};

const C = {
  paper: '#FAF7F1', ink: '#1B1A17', gold: '#9C7A3C', hair: '#E2DCD0',
  sky0: '#F0EBE1', sky1: '#FAF8F3',
  ground: '#EEEAE1', street: '#E2DCD0', block: '#FCFAF6', blockPublic: '#F4EBD9', blockRing: '#FBF6EC', blockSite: '#EDE8DF',
  green: '#CFD5BF', park: '#C2CBAD', water: '#C3D5DA', lot: '#F2EEE5', lotSoft: '#D5DAC4',
  tree: '#B5BE9F', slab: '#FFFFFF', edge: '#1B1A17',
};

// ------------------------------------------------------------------------------------------------ sun (suncalc, V. Agafonkin, BSD)
const J1970 = 2440588, J2000 = 2451545, OBL = DEG * 23.4397;
function sunPos(date, lat, lng) {
  const lw = DEG * -lng, phi = DEG * lat, d = date.valueOf() / 864e5 - 0.5 + J1970 - J2000;
  const M = DEG * (357.5291 + 0.98560028 * d);
  const Cc = DEG * (1.9148 * Math.sin(M) + 0.02 * Math.sin(2 * M) + 0.0003 * Math.sin(3 * M));
  const L = M + Cc + DEG * 102.9372 + Math.PI;
  const dec = Math.asin(Math.sin(OBL) * Math.sin(L));
  const ra = Math.atan2(Math.sin(L) * Math.cos(OBL), Math.cos(L));
  const H = DEG * (280.16 + 360.9856235 * d) - lw - ra;
  const az = Math.atan2(Math.sin(H), Math.cos(H) * Math.sin(phi) - Math.tan(dec) * Math.cos(phi));
  const alt = Math.asin(Math.sin(phi) * Math.sin(dec) + Math.cos(phi) * Math.cos(dec) * Math.cos(H));
  return { bearing: ((az / DEG) + 180 + 360) % 360, alt: alt / DEG };
}
// Israel: standard time UTC+2 on 21.3 and 21.12, daylight time UTC+3 on 21.6 and 21.9 (2026)
const SEASONS = { 3: { m: 2, d: 21, off: 2 }, 6: { m: 5, d: 21, off: 3 }, 9: { m: 8, d: 21, off: 3 }, 12: { m: 11, d: 21, off: 2 } };
function sunAt(season, hour, lat, lng) {
  const s = SEASONS[season] || SEASONS[9];
  return sunPos(new Date(Date.UTC(2026, s.m, s.d, 0, Math.round(hour * 60) - s.off * 60)), lat, lng);
}
function riseSet(season, lat, lng) {
  let rise = null, set = null, prev = null;
  for (let mi = 3 * 60; mi <= 22 * 60; mi += 2) {
    const up = sunAt(season, mi / 60, lat, lng).alt > -0.833;
    if (prev !== null && up && !prev) rise = mi;
    if (prev !== null && !up && prev) set = mi;
    prev = up;
  }
  return { rise, set };
}
const hhmm = (mi) => (mi == null ? '' : `${String(Math.floor(mi / 60)).padStart(2, '0')}:${String(Math.round(mi % 60)).padStart(2, '0')}`);
const dirOf = (b, out) => (out || new THREE.Vector3()).set(Math.sin(b * DEG), 0, -Math.cos(b * DEG));

// ------------------------------------------------------------------------------------------------ small helpers
const el = (tag, cls, html) => { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; };
const esc = (s) => String(s == null ? '' : s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const ease = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
const norm360 = (a) => ((a % 360) + 360) % 360;
const angDiff = (a, b) => { const d = Math.abs(norm360(a) - norm360(b)); return d > 180 ? 360 - d : d; };
function deepMerge(a, b) {
  if (!b) return a;
  const out = Array.isArray(a) ? a.slice() : { ...a };
  for (const k of Object.keys(b)) {
    const v = b[k];
    out[k] = v && typeof v === 'object' && !Array.isArray(v) && a && typeof a[k] === 'object' && !Array.isArray(a[k]) ? deepMerge(a[k], v) : v;
  }
  return out;
}
function i16(b64) {
  const bin = atob(b64);
  const n = bin.length >> 1;
  const out = new Int16Array(n);
  for (let i = 0; i < n; i++) out[i] = ((bin.charCodeAt(2 * i) | (bin.charCodeAt(2 * i + 1) << 8)) << 16) >> 16;
  return out;
}
// first vertex absolute, the rest deltas; returns a flat Float64Array [x0, z0, x1, z1, ...] in metres
function unpack(arr, off, n, q) {
  const P = new Float64Array(n * 2);
  let x = 0, z = 0;
  for (let i = 0; i < n; i++) { x += arr[off + 2 * i]; z += arr[off + 2 * i + 1]; P[2 * i] = x * q; P[2 * i + 1] = z * q; }
  return P;
}
function signedArea(P) { let A = 0; const n = P.length / 2; for (let i = 0; i < n; i++) { const j = (i + 1) % n; A += P[2 * i] * P[2 * j + 1] - P[2 * j] * P[2 * i + 1]; } return A / 2; }
function pip(P, x, z) {
  let c = false; const n = P.length / 2;
  for (let i = 0, j = n - 1; i < n; j = i++) {
    const xi = P[2 * i], zi = P[2 * i + 1], xj = P[2 * j], zj = P[2 * j + 1];
    if ((zi > z) !== (zj > z) && x < (xj - xi) * (z - zi) / (zj - zi + 1e-12) + xi) c = !c;
  }
  return c;
}
function bboxOf(P) { let x0 = 1e9, x1 = -1e9, z0 = 1e9, z1 = -1e9; for (let i = 0; i < P.length; i += 2) { x0 = Math.min(x0, P[i]); x1 = Math.max(x1, P[i]); z0 = Math.min(z0, P[i + 1]); z1 = Math.max(z1, P[i + 1]); } return [x0, z0, x1, z1]; }
function segDist(px, pz, ax, az, bx, bz) {
  const ex = bx - ax, ez = bz - az, L = ex * ex + ez * ez;
  const t = L ? clamp(((px - ax) * ex + (pz - az) * ez) / L, 0, 1) : 0;
  return Math.hypot(px - ax - t * ex, pz - az - t * ez);
}

// a uniform grid over the ground, for picking, the sun's rays and the walk's collisions
class Grid {
  constructor(half, cell) { this.half = half; this.cell = cell; this.n = Math.ceil(2 * half / cell); this.cells = new Map(); }
  key(i, j) { return i * 100000 + j; }
  ij(x) { return Math.floor((x + this.half) / this.cell); }
  add(id, bb) {
    const i0 = clamp(this.ij(bb[0]), 0, this.n - 1), i1 = clamp(this.ij(bb[2]), 0, this.n - 1);
    const j0 = clamp(this.ij(bb[1]), 0, this.n - 1), j1 = clamp(this.ij(bb[3]), 0, this.n - 1);
    for (let i = i0; i <= i1; i++) for (let j = j0; j <= j1; j++) { const k = this.key(i, j); let a = this.cells.get(k); if (!a) this.cells.set(k, (a = [])); a.push(id); }
  }
  at(x, z) { return this.cells.get(this.key(this.ij(x), this.ij(z))) || null; }
  // Amanatides-Woo walk along the ray's ground projection; cb(list, tEnter) returns true to stop
  walk(ox, oz, dx, dz, tMax, cb) {
    const cs = this.cell;
    let i = this.ij(ox), j = this.ij(oz);
    const si = dx > 0 ? 1 : -1, sj = dz > 0 ? 1 : -1;
    const bx = (i + (si > 0 ? 1 : 0)) * cs - this.half, bz = (j + (sj > 0 ? 1 : 0)) * cs - this.half;
    let tx = Math.abs(dx) < 1e-12 ? Infinity : (bx - ox) / dx, tz = Math.abs(dz) < 1e-12 ? Infinity : (bz - oz) / dz;
    const ddx = Math.abs(dx) < 1e-12 ? Infinity : cs / Math.abs(dx), ddz = Math.abs(dz) < 1e-12 ? Infinity : cs / Math.abs(dz);
    let t = 0;
    for (let guard = 0; guard < 4000; guard++) {
      if (i >= 0 && j >= 0 && i < this.n && j < this.n) {
        const a = this.cells.get(this.key(i, j));
        if (a && cb(a, t)) return;
      }
      if (tx < tz) { t = tx; tx += ddx; i += si; } else { t = tz; tz += ddz; j += sj; }
      if (t > tMax) return;
    }
  }
}

// the ray against a vertical prism (a footprint P extruded 0..h); returns the ray parameter of the first hit or Infinity
function rayPrism(ox, oy, oz, dx, dy, dz, P, h) {
  let best = Infinity;
  const n = P.length / 2;
  for (let i = 0; i < n; i++) {
    const j = (i + 1) % n;
    const ax = P[2 * i], az = P[2 * i + 1], ex = P[2 * j] - ax, ez = P[2 * j + 1] - az;
    const den = dx * ez - dz * ex;
    if (Math.abs(den) < 1e-12) continue;
    const t = ((ax - ox) * ez - (az - oz) * ex) / den;
    const s = ((ax - ox) * dz - (az - oz) * dx) / den;
    if (t > 1e-3 && s >= 0 && s <= 1 && t < best) { const y = oy + dy * t; if (y >= 0 && y <= h) best = t; }
  }
  if (Math.abs(dy) > 1e-9) { const t = (h - oy) / dy; if (t > 1e-3 && t < best && pip(P, ox + dx * t, oz + dz * t)) best = t; }
  return best;
}
function rayCylinder(ox, oy, oz, dx, dy, dz, cx, cz, r, h) {
  const fx = ox - cx, fz = oz - cz;
  const a = dx * dx + dz * dz, b = 2 * (fx * dx + fz * dz), c = fx * fx + fz * fz - r * r;
  let best = Infinity;
  if (a > 1e-12) {
    const disc = b * b - 4 * a * c;
    if (disc >= 0) {
      const sq = Math.sqrt(disc);
      for (const t of [(-b - sq) / (2 * a), (-b + sq) / (2 * a)]) { if (t > 1e-3) { const y = oy + dy * t; if (y >= 0 && y <= h && t < best) best = t; } }
    }
  }
  if (Math.abs(dy) > 1e-9) { const t = (h - oy) / dy; if (t > 1e-3 && t < best) { const x = ox + dx * t - cx, z = oz + dz * t - cz; if (x * x + z * z <= r * r) best = t; } }
  return best;
}

// the floor plate: a superellipse ("circle-inspired", sized to the municipal footprint); local u along the plate's bearing
function plateOutline(half, n, M = 72) {
  const pts = [];
  for (let k = 0; k < M; k++) {
    const t = (k / M) * Math.PI * 2;
    const c = Math.cos(t), s = Math.sin(t);
    pts.push([half * Math.sign(c) * Math.pow(Math.abs(c), 2 / n), half * Math.sign(s) * Math.pow(Math.abs(s), 2 / n)]);
  }
  return pts;
}
const plateRadius = (half, n, phi) => half / Math.pow(Math.pow(Math.abs(Math.cos(phi)), n) + Math.pow(Math.abs(Math.sin(phi)), n), 1 / n);

// ================================================================================================= mountWorld
export function mountWorld(host, opts = {}) {
  const o = { ...DEFAULTS, ...opts };
  const lang = String(o.lang || 'he').slice(0, 2) === 'en' ? 'en' : 'he';
  const T = deepMerge(I18N[lang], o.i18n ? (o.i18n[lang] || o.i18n) : null);
  const rtl = lang === 'he';
  const reduced = typeof matchMedia === 'function' && matchMedia('(prefers-reduced-motion: reduce)').matches;
  const coarse = typeof matchMedia === 'function' && matchMedia('(pointer: coarse)').matches;

  // ---------------------------------------------------------------- DOM
  if (o.injectCss && !document.querySelector('link[data-nlw-css]')) {
    const l = document.createElement('link');
    l.rel = 'stylesheet'; l.href = new URL('./world.css', import.meta.url).href; l.setAttribute('data-nlw-css', '1');
    document.head.appendChild(l);
  }
  if (o.injectFonts && !document.querySelector('link[href*="family=Assistant"]')) {
    const f = document.createElement('link');
    f.rel = 'stylesheet';
    f.href = 'https://fonts.googleapis.com/css2?family=Assistant:wght@400;500;600;700&family=Noto+Serif+Hebrew:wght@500;600;700&display=swap';
    document.head.appendChild(f);
  }
  const root = el('div', 'nlw');
  root.dir = rtl ? 'rtl' : 'ltr';
  root.lang = lang;
  root.setAttribute('role', 'region');
  root.setAttribute('aria-label', T.region);
  root.dataset.mode = o.mode;
  host.appendChild(root);
  const canvasHost = el('div', 'nlw-canvas');
  const frame = el('div', 'nlw-frame'); frame.hidden = true;
  const labelsEl = el('div', 'nlw-labels');
  root.append(canvasHost, frame, labelsEl);
  let posterImg = null;
  if (o.poster) {
    posterImg = el('img', 'nlw-poster');
    const p = typeof o.poster === 'string' ? { src: o.poster } : o.poster;
    if (p.srcset) posterImg.srcset = p.srcset;
    if (p.sizes) posterImg.sizes = p.sizes;
    posterImg.src = p.src;
    posterImg.alt = p.alt || T.region;
    posterImg.decoding = 'async';
    root.appendChild(posterImg);
  }
  const enterBtn = el('button', 'nlw-enter', esc(T.enter)); enterBtn.type = 'button'; enterBtn.hidden = true;
  const loadEl = el('div', 'nlw-load', `${esc(T.loading)}<span class="nlw-bar"><i></i></span>`); loadEl.hidden = true;
  root.append(enterBtn, loadEl);

  const ui = {};
  if (o.chrome) buildChrome();

  function buildChrome() {
    const top = el('div', 'nlw-top');
    const tabs = el('div', 'nlw-tabs'); tabs.setAttribute('role', 'toolbar');
    ui.tabs = {};
    for (const m of MODES) {
      const b = el('button', 'nlw-tab', esc(T.modes[m])); b.type = 'button'; b.dataset.mode = m; b.setAttribute('aria-pressed', 'false');
      b.addEventListener('click', () => api.setMode(m, 'user'));
      tabs.appendChild(b); ui.tabs[m] = b;
    }
    const full = el('button', 'nlw-sq nlw-fullbtn', '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M3 8V3h5M17 8V3h-5M3 12v5h5M17 12v5h-5"/></svg>');
    full.type = 'button'; full.setAttribute('aria-label', T.full); full.title = T.full;
    full.addEventListener('click', () => toggleFull());
    top.append(tabs, el('span', 'nlw-spacer'), full);
    ui.top = top; ui.full = full;
    ui.panel = el('div', 'nlw-panel');
    ui.card = el('div', 'nlw-card'); ui.card.hidden = true; ui.card.setAttribute('role', 'dialog'); ui.card.setAttribute('aria-live', 'polite');
    ui.joy = el('div', 'nlw-joy', '<i></i>'); ui.joy.hidden = true; ui.joy.setAttribute('aria-hidden', 'true');
    ui.compass = el('div', 'nlw-compass');
    const cb = el('button', 'nlw-sq', `<svg viewBox="-12 -12 24 24"><path d="M0,-9 L4,3 L0,1 L-4,3 Z" fill="#1B1A17"/><path d="M0,9 L4,3 L0,1 L-4,3 Z" fill="none" stroke="#1B1A17" stroke-width=".8"/></svg>`);
    cb.type = 'button'; cb.setAttribute('aria-label', T.north); cb.title = T.north;
    cb.addEventListener('click', () => northUp());
    ui.compass.appendChild(cb); ui.needle = cb.querySelector('svg');
    ui.scale = el('div', 'nlw-scale', '<span></span><i></i>');
    ui.cap = el('div', 'nlw-cap', esc(T.caption));
    ui.eye = el('div', 'nlw-eye'); ui.eye.hidden = true;
    root.append(top, ui.eye, ui.panel, ui.card, ui.joy, ui.compass, ui.scale, ui.cap);
  }

  // ---------------------------------------------------------------- state
  const S = {
    mode: MODES.includes(o.mode) ? o.mode : 'aerial',
    tower: null, floor: null, facing: null, view: 'out',
    season: SEASONS[o.season] ? o.season : 9, hour: clamp(+o.hour || 10, 5, 20),
    cat: 'transport', place: null, sunOpen: false, collapsed: false,
  };
  let W = null;                 // decoded world
  let places = null;            // places.json (on intent)
  let renderer, scene, camera, controls, sunLight, hemi, fog, sky;
  let TW = {};                  // towers
  let dirty = true, raf = 0, destroyed = false, visible = true;
  let anim = null;              // camera flight
  let fp = null;                // first-person rig { x, y, z, yaw, tilt, top, bottom }
  let proj = { top: 20, bottom: -20 };
  const curTarget = { v: null };
  let frameTimes = [];
  let dpr = 1;
  const readyCbs = [];
  let isReady = false;
  const ready = new Promise((res) => readyCbs.push(res));
  const queue = [];
  const disposables = [];
  const listeners = [];
  const on = (t, ev, fn, opt) => { t.addEventListener(ev, fn, opt); listeners.push([t, ev, fn, opt]); };

  // ---------------------------------------------------------------- the API (methods wait for the world)
  const whenReady = (fn) => (...args) => { if (isReady) return fn(...args); queue.push(() => fn(...args)); return undefined; };
  const api = {
    ready,
    setMode: whenReady((m, source = 'api') => setMode(m, source)),
    pickTower: whenReady((k, source = 'api') => pickTower(k, source)),
    setFloor: whenReady((n, source = 'api') => setFloor(n, source)),
    setFacing: whenReady((b, source = 'api') => setFacing(b, source)),
    setSun: whenReady((s) => setSun(s)),
    setView: whenReady((v) => setTowerView(v)),
    setCategory: whenReady((c) => setCategory(c)),
    pickPlace: whenReady((id) => ensurePlaces().then(() => { const p = places && places.byId[id]; if (p) selectPlace(p); })),
    walkTo: whenReady((k) => walkSpot(k)),
    collapse: whenReady((v) => { S.collapsed = !!v; renderPanel(); }),
    // open the info card of a thing: 'tower' A|B|C, 'civic' school|centre, 'park', 'pond', 'road', 'ring', 'square', 'block' index, 'place' id
    show: whenReady((kind, id) => showThing(kind, id)),
    closeCard: whenReady(() => closeCard()),
    project: (x, y, z) => { if (!camera) return null; const v = new THREE.Vector3(x, y, z).project(camera); return { x: (v.x * 0.5 + 0.5) * root.clientWidth, y: (-v.y * 0.5 + 0.5) * root.clientHeight, front: v.z < 1 }; },
    getState: () => ({ mode: S.mode, tower: S.tower, floor: S.floor, facing: S.facing != null ? facingBearing(S.tower, S.floor, S.facing) : null, season: S.season, hour: S.hour, view: S.view, cat: S.cat }),
    stats: () => stats(),
    bench: (ms) => bench(ms),
    _debug: () => ({ scene, renderer, camera, W, TW, route: (sx, sz, tx, tz) => { const r = route(sx, sz, tx, tz); return r ? { len: r.len, n: r.path.length, nodes: graph.adj.length } : { none: true }; } }),
    sunHours: (k, f, b, season) => sunHoursFor(k, f, b, season || S.season),
    destroy,
    el: root,
  };

  // ---------------------------------------------------------------- start on intent
  function start() {
    if (start.done) return; start.done = true;
    enterBtn.hidden = true;
    boot().catch((e) => { console.error('[nlw] boot failed', e); loadEl.textContent = String(e && e.message || e); loadEl.hidden = false; });
  }
  if (o.intent === 'now') start();
  else if (o.intent === 'tap') { enterBtn.hidden = false; on(enterBtn, 'click', start); }
  else {
    if (posterImg) { enterBtn.hidden = false; on(enterBtn, 'click', start); }
    if ('IntersectionObserver' in window) {
      const io = new IntersectionObserver((es) => { if (es.some((e) => e.isIntersecting)) { io.disconnect(); start(); } }, { rootMargin: '120px' });
      io.observe(root);
      disposables.push(() => io.disconnect());
    } else start();
  }

  async function boot() {
    loadEl.hidden = false;
    const bar = loadEl.querySelector('.nlw-bar i');
    const dataP = fetchWithProgress(o.dataUrl, (f) => { if (bar) bar.style.width = Math.round(f * 80) + '%'; });
    const [three, oc, bgu, data] = await Promise.all([
      import('three'), import('three/addons/controls/OrbitControls.js'), import('three/addons/utils/BufferGeometryUtils.js'), dataP]);
    if (destroyed) return;
    THREE = three; OrbitControls = oc.OrbitControls; mergeGeometries = bgu.mergeGeometries;
    if (bar) bar.style.width = '88%';
    await new Promise((r) => requestAnimationFrame(r));
    W = decode(data);
    buildScene();
    if (bar) bar.style.width = '100%';
    isReady = true;
    setMode(S.mode, 'init');
    applySun();
    if (document.fonts && document.fonts.ready) await Promise.race([document.fonts.ready, new Promise((r) => setTimeout(r, 1500))]);
    renderNow();
    loadEl.hidden = true;
    if (posterImg) posterImg.classList.add('is-gone');
    while (queue.length) queue.shift()();
    renderNow();
    loop();
    readyCbs.forEach((f) => f(api));
  }

  async function fetchWithProgress(url, cb) {
    const r = await fetch(url, { credentials: 'same-origin' });
    if (!r.ok) throw new Error('world data ' + r.status);
    const len = +r.headers.get('content-length') || 0;
    if (!r.body || !len) return r.json();
    const reader = r.body.getReader();
    const chunks = []; let got = 0;
    for (;;) { const { done, value } = await reader.read(); if (done) break; chunks.push(value); got += value.length; cb(Math.min(1, got / len)); }
    const buf = new Uint8Array(got); let off = 0;
    for (const c of chunks) { buf.set(c, off); off += c.length; }
    return JSON.parse(new TextDecoder().decode(buf));
  }

  // ---------------------------------------------------------------- decode the compact world
  function decode(d) {
    const out = { raw: d, names: d.names || [], model: d.model, facts: d.facts || {}, sources: d.sources || {}, origin: d.origin };
    // buildings
    const ints = (x) => (typeof x === 'string' ? i16(x) : x);
    const bA = ints(d.blocks.data), bq = d.blocks.q, bqFar = d.blocks.q_far || bq;
    const blocks = [];
    for (let o2 = 0, idx = 0; o2 < bA.length; idx++) {
      const n = bA[o2], h = bA[o2 + 1] * bq, floors = bA[o2 + 2], year = bA[o2 + 3], flags = bA[o2 + 4] & 0xffff;
      const P = unpack(bA, o2 + 5, n, flags & 256 ? bqFar : bq);
      o2 += 5 + 2 * n;
      const bb = bboxOf(P);
      blocks.push({ i: idx, h, floors, year, flags, P, bb, cx: (bb[0] + bb[2]) / 2, cz: (bb[1] + bb[3]) / 2, name: d.blocks.names ? d.blocks.names[idx] : null });
    }
    out.blocks = blocks; out.nNear = d.blocks.near;
    // streets
    const sA = ints(d.streets.data), sq = d.streets.q;
    const streets = [];
    for (let o2 = 0; o2 < sA.length;) { const n = sA[o2], w = sA[o2 + 1], fl = sA[o2 + 2], ni = sA[o2 + 3]; streets.push({ w, ring: !!(fl & 1), name: ni >= 0 ? out.names[ni] : '', P: unpack(sA, o2 + 4, n, sq) }); o2 += 4 + 2 * n; }
    out.streets = streets;
    // greens
    const gA = ints(d.greens.data), gq = d.greens.q;
    const greens = [];
    for (let o2 = 0; o2 < gA.length;) { const n = gA[o2], ni = gA[o2 + 1], fl = gA[o2 + 2]; const P = unpack(gA, o2 + 3, n, gq); greens.push({ name: ni >= 0 ? out.names[ni] : '', square: !!(fl & 1), P, bb: bboxOf(P) }); o2 += 3 + 2 * n; }
    out.greens = greens;
    out.water = (d.water.rings || []).map((w) => ({ name: w.n >= 0 ? out.names[w.n] : '', outer: !!w.o, P: unpack(w.p, 0, w.p.length / 2, d.water.q) }));
    out.water.forEach((w) => { w.bb = bboxOf(w.P); w.area = Math.abs(signedArea(w.P)); });
    out.sea = out.water.filter((w) => w.outer).sort((a, b) => b.area - a.area)[0] || null;
    const tA = ints(d.trees.data), tq = d.trees.q;
    out.trees = new Float32Array(tA.length); for (let i = 0; i < tA.length; i++) out.trees[i] = tA[i] * tq;
    out.ring = (d.ring.parts || []).map((p) => unpack(p, 0, p.length / 2, d.ring.q));
    out.park = d.park && d.park.p ? unpack(d.park.p, 0, d.park.p.length / 2, d.park.q) : null;
    out.pond = o.pond !== false && d.pond && d.pond.p ? unpack(d.pond.p, 0, d.pond.p.length / 2, d.pond.q) : null; // an illustration (no published outline)
    if (out.pond) { const bb = bboxOf(out.pond); out.pondC = [(bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2]; }
    if (out.park) out.parkBB = bboxOf(out.park);
    out.lots = (d.lots.list || []).map((l) => ({ lot: l.lot, use: l.use, P: unpack(l.p, 0, l.p.length / 2, d.lots.q) }));
    out.towers = d.towers.map((t) => ({ ...t, fpP: unpack(t.fp, 0, t.fp.length / 2, 0.1) }));
    out.civic = d.civic || [];
    out.features = d.park_features || [];
    out.pins = d.pins || [];
    out.marks = d.marks || [];
    // grids: buildings (for picking, the sun's rays and the walk), greens and streets (for picking the ground)
    out.bgrid = new Grid(3400, 25);
    blocks.forEach((b) => out.bgrid.add(b.i, b.bb));
    out.ggrid = new Grid(3400, 50);
    greens.forEach((g, i) => out.ggrid.add(i, g.bb));
    out.sgrid = new Grid(3400, 25);
    streets.forEach((s, i) => { for (let k = 0; k + 3 < s.P.length; k += 2) out.sgrid.add(i, [Math.min(s.P[k], s.P[k + 2]) - s.w, Math.min(s.P[k + 1], s.P[k + 3]) - s.w, Math.max(s.P[k], s.P[k + 2]) + s.w, Math.max(s.P[k + 1], s.P[k + 3]) + s.w]); });
    out.stamp = new Uint32Array(blocks.length); out.stampN = 1;
    return out;
  }

  // ================================================================================================ the scene
  function buildScene() {
    const m = W.model;
    const small = Math.min(root.clientWidth, root.clientHeight) < 700 || coarse;
    dpr = Math.min(window.devicePixelRatio || 1, o.maxDpr || (small ? 1.5 : 2));
    renderer = new THREE.WebGLRenderer({ antialias: true, logarithmicDepthBuffer: o.logDepth === true, preserveDrawingBuffer: !!o.preserve, powerPreference: 'high-performance' });
    renderer.setPixelRatio(dpr);
    renderer.setSize(root.clientWidth, root.clientHeight, false);
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.NeutralToneMapping;
    renderer.toneMappingExposure = 1.0;
    renderer.shadowMap.enabled = !!o.shadows;
    renderer.shadowMap.type = o.softShadows === false ? THREE.PCFShadowMap : THREE.PCFSoftShadowMap;
    renderer.shadowMap.autoUpdate = false;
    const cv = renderer.domElement;
    cv.tabIndex = 0;
    cv.setAttribute('aria-label', T.region);
    canvasHost.appendChild(cv);

    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(40, 1, 0.3, 60000);
    fog = new THREE.Fog(C.sky0, 1600, 9000);
    scene.fog = fog;

    // sky: a quiet gradient, paper at the horizon
    const skyMat = new THREE.ShaderMaterial({
      uniforms: { c0: { value: new THREE.Color(C.sky0) }, c1: { value: new THREE.Color(C.sky1) }, c2: { value: new THREE.Color('#E8E2D6') } },
      vertexShader: 'varying vec3 vP; void main(){ vP = normalize(position); gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }',
      fragmentShader: 'uniform vec3 c0; uniform vec3 c1; uniform vec3 c2; varying vec3 vP; void main(){ float y = vP.y; vec3 c = y > 0.0 ? mix(c0, c1, smoothstep(0.0, 0.5, y)) : mix(c0, c2, smoothstep(0.0, -0.2, y)); gl_FragColor = vec4(c, 1.0);\n#include <colorspace_fragment>\n}',
      side: THREE.BackSide, depthWrite: false, depthTest: false, fog: false,
    });
    sky = new THREE.Mesh(new THREE.SphereGeometry(10000, 32, 16), skyMat); // follows the camera (inside every far plane)
    sky.renderOrder = -10; sky.frustumCulled = false;
    scene.add(sky);

    // the glass reflects the same paper sky
    const pmrem = new THREE.PMREMGenerator(renderer);
    const envScene = new THREE.Scene();
    envScene.add(new THREE.Mesh(new THREE.SphereGeometry(10, 32, 16), new THREE.ShaderMaterial({
      vertexShader: 'varying vec3 vP; void main(){ vP = normalize(position); gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }',
      fragmentShader: 'varying vec3 vP; void main(){ float y = vP.y; vec3 top = vec3(0.80,0.86,0.90); vec3 hor = vec3(0.97,0.96,0.93); vec3 gnd = vec3(0.55,0.53,0.48); vec3 c = y > 0.0 ? mix(hor, top, pow(y,0.55)) : mix(hor, gnd, smoothstep(0.0,-0.25,y)); gl_FragColor = vec4(c,1.0); }',
      side: THREE.BackSide,
    })));
    const envTex = pmrem.fromScene(envScene, 0.02).texture;
    pmrem.dispose();

    hemi = new THREE.HemisphereLight('#FFFBF3', '#E4DCCB', 1.9);
    scene.add(hemi);
    sunLight = new THREE.DirectionalLight('#FFF1D8', 2.4);
    sunLight.castShadow = !!o.shadows;
    const sm = small ? 2048 : 4096;
    sunLight.shadow.mapSize.set(sm, sm);
    sunLight.shadow.bias = -0.0003;
    sunLight.shadow.normalBias = 0.4;
    scene.add(sunLight, sunLight.target);

    buildGround();
    buildBlocks();
    buildTrees(small);
    buildTowers(m, envTex);
    buildSelection();
    buildPlacesLayer();

    controls = new OrbitControls(camera, cv);
    controls.enableDamping = true;
    controls.dampingFactor = 0.08;
    controls.rotateSpeed = 0.55;
    controls.zoomSpeed = 0.9;
    controls.panSpeed = 0.8;
    controls.screenSpacePanning = false;
    controls.touches.ONE = THREE.TOUCH.ROTATE;
    controls.touches.TWO = THREE.TOUCH.DOLLY_PAN;
    controls.enableZoom = false; // the wheel zooms only after the visitor engages the world (the page's scroll is never trapped)
    controls.addEventListener('change', () => { if (!anim) invalidate(); });
    controls.addEventListener('start', () => { anim = null; });

    bindInput(cv);
    resize();
    on(window, 'resize', resize);
    if ('ResizeObserver' in window) { const ro = new ResizeObserver(() => resize()); ro.observe(root); disposables.push(() => ro.disconnect()); }
    on(document, 'visibilitychange', () => { visible = !document.hidden; if (visible) loop(); });
  }

  // ground layers lie a few centimetres apart: each one also gets its own depth offset, so they never flicker far away
  const groundMat = (color, extra = {}, level = 1) => new THREE.MeshStandardMaterial({ color, roughness: 1, metalness: 0, polygonOffset: true, polygonOffsetFactor: -level, polygonOffsetUnits: -2 * level, ...extra });
  function shapeFromP(P) { const pts = []; for (let i = 0; i < P.length; i += 2) pts.push(new THREE.Vector2(P[i], -P[i + 1])); return new THREE.Shape(pts); }
  function flatMesh(shapes, color, y, extra, level = 1) {
    if (!shapes.length) return null;
    const g = mergeGeometries(shapes.map((s) => new THREE.ShapeGeometry(s, 2)));
    g.rotateX(-Math.PI / 2);
    const mesh = new THREE.Mesh(g, groundMat(color, extra, level));
    mesh.position.y = y; mesh.receiveShadow = true;
    scene.add(mesh);
    return mesh;
  }

  function buildGround() {
    const g = new THREE.Mesh(new THREE.PlaneGeometry(120000, 120000, 200, 200).rotateX(-Math.PI / 2), new THREE.MeshStandardMaterial({ color: C.ground, roughness: 1 }));
    g.receiveShadow = true;
    scene.add(g);
    // water: the sea, the Yarkon, the Yarkon park lake (GIS 504), holes kept
    {
      const shapes = []; let cur = null;
      for (const w of W.water) {
        if (w.outer) { cur = shapeFromP(w.P); shapes.push(cur); }
        else if (cur) { const pts = []; for (let i = 0; i < w.P.length; i += 2) pts.push(new THREE.Vector2(w.P[i], -w.P[i + 1])); cur.holes.push(new THREE.Path(pts)); }
      }
      flatMesh(shapes, C.water, 0.3, { roughness: 0.5 }, 1);
    }
    // streets: ribbons of the width class (GIS 507)
    {
      const pos = [];
      const tri = (ax, az, bx, bz, cx, cz) => {
        const ny = (bz - az) * (cx - ax) - (bx - ax) * (cz - az);
        if (ny < 0) pos.push(ax, 0, az, cx, 0, cz, bx, 0, bz); else pos.push(ax, 0, az, bx, 0, bz, cx, 0, cz);
      };
      for (const s of W.streets) {
        const w = s.w * 0.5 * 0.92, P = s.P, n = P.length / 2;
        for (let i = 0; i + 1 < n; i++) {
          const x0 = P[2 * i], z0 = P[2 * i + 1], x1 = P[2 * i + 2], z1 = P[2 * i + 3];
          const dx = x1 - x0, dz = z1 - z0, L = Math.hypot(dx, dz);
          if (L < 0.01) continue;
          const nx = -dz / L * w, nz = dx / L * w;
          tri(x0 + nx, z0 + nz, x1 - nx, z1 - nz, x1 + nx, z1 + nz);
          tri(x0 + nx, z0 + nz, x0 - nx, z0 - nz, x1 - nx, z1 - nz);
        }
        for (let i = 1; i + 1 < n; i++) {
          const x = P[2 * i], z = P[2 * i + 1];
          for (let k = 0; k < 8; k++) { const a0 = k / 8 * Math.PI * 2, a1 = (k + 1) / 8 * Math.PI * 2; tri(x, z, x + Math.cos(a0) * w, z + Math.sin(a0) * w, x + Math.cos(a1) * w, z + Math.sin(a1) * w); }
        }
      }
      const g2 = new THREE.BufferGeometry();
      g2.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
      g2.computeVertexNormals();
      const mesh = new THREE.Mesh(g2, groundMat(C.street, {}, 2));
      mesh.position.y = 0.06; mesh.receiveShadow = true;
      scene.add(mesh);
    }
    // the plot of plan 2500ב: the residential lot as pale stone, the private open space as a light green wash
    {
      const stone = [], soft = [];
      for (const l of W.lots) { if (/^מגורים/.test(l.use)) stone.push(shapeFromP(l.P)); else if (/^פרטי/.test(l.use)) soft.push(shapeFromP(l.P)); }
      flatMesh(stone, C.lot, 0.09, {}, 3);
      flatMesh(soft, C.lotSoft, 0.1, {}, 4);
    }
    flatMesh(W.greens.filter((g) => !g.square).map((g) => shapeFromP(g.P)), C.green, 0.12, {}, 5);
    if (W.park) flatMesh([shapeFromP(W.park)], C.park, 0.14, {}, 6);
    // the pond: ILLUSTRATION (no published outline), a dashed outline says so
    if (W.pond) {
      flatMesh([shapeFromP(W.pond)], C.water, 0.17, { roughness: 0.35 }, 7);
      const lp = []; for (let i = 0; i <= W.pond.length / 2; i++) { const k = i % (W.pond.length / 2); lp.push(new THREE.Vector3(W.pond[2 * k], 0.25, W.pond[2 * k + 1])); }
      const line = new THREE.Line(new THREE.BufferGeometry().setFromPoints(lp), new THREE.LineDashedMaterial({ color: C.ink, dashSize: 1.6, gapSize: 1.4, transparent: true, opacity: 0.5 }));
      line.computeLineDistances();
      scene.add(line);
    }
    // the ring road ה' באייר: an ink hairline on its axis
    {
      const pos = [];
      for (const P of W.ring) for (let i = 0; i + 3 < P.length; i += 2) pos.push(P[i], 0.3, P[i + 1], P[i + 2], 0.3, P[i + 3]);
      const g2 = new THREE.BufferGeometry(); g2.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
      scene.add(new THREE.LineSegments(g2, new THREE.LineBasicMaterial({ color: C.ink, transparent: true, opacity: 0.35 })));
    }
  }

  // city blocks: real footprints x real heights, tiled by bearing so the far ones are culled when out of view
  function buildBlocks() {
    const tiles = new Map();
    const cBlock = new THREE.Color(C.block), cPub = new THREE.Color(C.blockPublic), cRing = new THREE.Color(C.blockRing), cSite = new THREE.Color(C.blockSite);
    for (const b of W.blocks) {
      const near = !!(b.flags & 2);
      const r = Math.hypot(b.cx, b.cz);
      const sec = Math.floor(norm360(Math.atan2(b.cx, -b.cz) / DEG) / (near ? 90 : 45));
      const key = (near ? (r < 330 ? 'c' : 'n') : 'f') + sec;
      let t = tiles.get(key);
      if (!t) tiles.set(key, (t = { near, pos: [], nor: [], col: [], lin: [], tri2b: [] }));
      const col = (b.flags & 24) ? cPub : (b.flags & 32) ? cSite : (b.flags & 4) ? cRing : (b.flags & 1) ? cPub : cBlock;
      const P = b.P, n = P.length / 2, h = b.h;
      const v = (x, y, z, nx, ny, nz) => { t.pos.push(x, y, z); t.nor.push(nx, ny, nz); t.col.push(col.r, col.g, col.b); };
      for (let i = 0; i < n; i++) {
        const j = (i + 1) % n;
        const x0 = P[2 * i], z0 = P[2 * i + 1], x1 = P[2 * j], z1 = P[2 * j + 1];
        const dx = x1 - x0, dz = z1 - z0, L = Math.hypot(dx, dz);
        if (L < 0.02) continue;
        const nx = dz / L, nz = -dx / L;
        v(x0, 0, z0, nx, 0, nz); v(x1, h, z1, nx, 0, nz); v(x1, 0, z1, nx, 0, nz);
        v(x0, 0, z0, nx, 0, nz); v(x0, h, z0, nx, 0, nz); v(x1, h, z1, nx, 0, nz);
        t.tri2b.push(b.i, b.i);
        t.lin.push(x0, h, z0, x1, h, z1);
        if (near) t.lin.push(x0, 0.25, z0, x1, 0.25, z1);
      }
      for (let i = 0; i < n; i++) {
        const p = (i - 1 + n) % n, q = (i + 1) % n;
        const a1 = Math.atan2(P[2 * i + 1] - P[2 * p + 1], P[2 * i] - P[2 * p]), a2 = Math.atan2(P[2 * q + 1] - P[2 * i + 1], P[2 * q] - P[2 * i]);
        let da = Math.abs(a2 - a1); if (da > Math.PI) da = 2 * Math.PI - da;
        if (da > 28 * DEG) t.lin.push(P[2 * i], 0, P[2 * i + 1], P[2 * i], h, P[2 * i + 1]);
      }
      const contour = []; for (let i = 0; i < n; i++) contour.push(new THREE.Vector2(P[2 * i], P[2 * i + 1]));
      const tris = THREE.ShapeUtils.triangulateShape(contour, []);
      for (const [ia, ib, ic] of tris) {
        let a = ia, bb = ib, c = ic;
        const ny = (P[2 * bb + 1] - P[2 * a + 1]) * (P[2 * c] - P[2 * a]) - (P[2 * bb] - P[2 * a]) * (P[2 * c + 1] - P[2 * a + 1]);
        if (ny < 0) { const tt = bb; bb = c; c = tt; }
        v(P[2 * a], h, P[2 * a + 1], 0, 1, 0); v(P[2 * bb], h, P[2 * bb + 1], 0, 1, 0); v(P[2 * c], h, P[2 * c + 1], 0, 1, 0);
        t.tri2b.push(b.i);
      }
    }
    const blockMat = new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.92, metalness: 0 });
    blockMat.onBeforeCompile = (sh) => {
      sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\nvarying float vWY; varying float vWall;')
        .replace('#include <begin_vertex>', '#include <begin_vertex>\nvWY = (modelMatrix * vec4(transformed, 1.0)).y; vWall = 1.0 - abs(normal.y);');
      sh.fragmentShader = sh.fragmentShader.replace('#include <common>', '#include <common>\nvarying float vWY; varying float vWall;')
        .replace('#include <color_fragment>', `#include <color_fragment>
          { float fl = vWY / 3.2; float fw = fwidth(fl); float d = abs(fract(fl + 0.5) - 0.5);
            float band = (1.0 - smoothstep(0.0, max(fw * 1.2, 0.012), d)) * (1.0 - smoothstep(0.08, 0.3, fw));
            diffuseColor.rgb *= 1.0 - 0.09 * band * step(0.5, vWall) * step(0.6, vWY); }`);
    };
    const nearLine = new THREE.LineBasicMaterial({ color: C.edge, transparent: true, opacity: 0.34 });
    const farLine = new THREE.LineBasicMaterial({ color: C.edge, transparent: true, opacity: 0.15 });
    W.blockMeshes = [];
    for (const [key, t] of tiles) {
      const g = new THREE.BufferGeometry();
      g.setAttribute('position', new THREE.Float32BufferAttribute(t.pos, 3));
      g.setAttribute('normal', new THREE.Float32BufferAttribute(t.nor, 3));
      g.setAttribute('color', new THREE.Float32BufferAttribute(t.col, 3));
      g.computeBoundingSphere();
      const mesh = new THREE.Mesh(g, blockMat);
      mesh.castShadow = true; mesh.receiveShadow = true;
      mesh.userData.tile = key;
      scene.add(mesh);
      const lg = new THREE.BufferGeometry(); lg.setAttribute('position', new THREE.Float32BufferAttribute(t.lin, 3)); lg.computeBoundingSphere();
      const lines = new THREE.LineSegments(lg, t.near ? nearLine : farLine);
      scene.add(lines);
      W.blockMeshes.push(mesh);
    }
  }

  // trees: the city's 2024 canopy footprints (crown size and height are an illustration)
  function buildTrees(small) {
    const A = W.trees, n = A.length / 3;
    const NEAR_R = 330;
    const nearIdx = [], farIdx = [];
    for (let i = 0; i < n; i++) (Math.hypot(A[3 * i], A[3 * i + 1]) < NEAR_R ? nearIdx : farIdx).push(i);
    const cm = new THREE.MeshStandardMaterial({ color: '#FFFFFF', roughness: 0.95 });
    const tm = new THREE.MeshStandardMaterial({ color: '#8E8676', roughness: 1 });
    const M = new THREE.Matrix4(), q = new THREE.Quaternion(), s = new THREE.Vector3(), p = new THREE.Vector3(), up = new THREE.Vector3(0, 1, 0);
    const base = new THREE.Color(C.tree), tmp = new THREE.Color();
    let seed = 7; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
    const make = (idx, crownGeo, withTrunks) => {
      const crowns = new THREE.InstancedMesh(crownGeo, cm, idx.length);
      const trunks = withTrunks ? new THREE.InstancedMesh(new THREE.CylinderGeometry(0.16, 0.22, 1, 5, 1, true).translate(0, 0.5, 0), tm, idx.length) : null;
      idx.forEach((i, k) => {
        const x = A[3 * i], z = A[3 * i + 1], r = Math.max(1.2, A[3 * i + 2]);
        const h0 = 2.0 + r * 0.35;
        q.setFromAxisAngle(up, rnd() * 6.28);
        p.set(x, h0 + r * 0.86, z); s.set(r, r * 0.86, r);
        M.compose(p, q, s); crowns.setMatrixAt(k, M);
        tmp.copy(base).offsetHSL((rnd() - 0.5) * 0.02, (rnd() - 0.5) * 0.05, (rnd() - 0.5) * 0.05);
        crowns.setColorAt(k, tmp);
        if (trunks) { p.set(x, 0, z); s.set(1, h0 + r * 0.3, 1); q.identity(); M.compose(p, q, s); trunks.setMatrixAt(k, M); }
      });
      crowns.castShadow = !small; crowns.receiveShadow = true;
      crowns.computeBoundingSphere(); scene.add(crowns);
      if (trunks) { trunks.castShadow = false; trunks.computeBoundingSphere(); scene.add(trunks); }
      return crowns;
    };
    W.treeMesh = make(nearIdx, new THREE.IcosahedronGeometry(1, 1), true);
    make(farIdx, new THREE.IcosahedronGeometry(1, 0).scale(1.08, 1.08, 1.08), true);
  }

  // ---------------------------------------------------------------- the three towers, floor by floor
  function glassTexture() {
    const cv = document.createElement('canvas'); cv.width = 64; cv.height = 128;
    const g = cv.getContext('2d');
    const grd = g.createLinearGradient(0, 0, 0, 128);
    grd.addColorStop(0, '#CFDCDF'); grd.addColorStop(0.55, '#B3C5CA'); grd.addColorStop(1, '#A2B6BC');
    g.fillStyle = grd; g.fillRect(0, 0, 64, 128);
    g.fillStyle = '#FFFFFF'; g.fillRect(0, 0, 3, 128);                // the white aluminium fin (300 mm deep, Alum Eshet)
    g.fillStyle = 'rgba(120,130,132,0.28)'; g.fillRect(3, 0, 2, 128);  // its thin shadow
    g.fillStyle = 'rgba(255,255,255,0.55)'; g.fillRect(0, 120, 64, 8);  // the spandrel line under the slab
    const t = new THREE.CanvasTexture(cv);
    t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping;
    t.anisotropy = Math.min(8, renderer.capabilities.getMaxAnisotropy());
    return t;
  }
  function buildTowers(m, envTex) {
    const FH = m.fh, TWIST = m.twist, DIR = m.twist_dir, SLAB_T = m.slab_t, SLAB_OUT = m.slab_out, NEXP = m.plate_n || 3.2;
    const gTex = glassTexture();
    const slabMat = new THREE.MeshStandardMaterial({ color: C.slab, roughness: 0.62, metalness: 0 });
    const glassMat = new THREE.MeshStandardMaterial({ color: '#FFFFFF', map: gTex, metalness: 0.45, roughness: 0.1, envMap: envTex, envMapIntensity: 1.1 });
    const lineMat = new THREE.LineBasicMaterial({ color: C.edge, transparent: true, opacity: 0.2 });
    const helixMat = new THREE.LineBasicMaterial({ color: C.edge, transparent: true, opacity: 0.32 });
    W.towerMats = { lineMat, helixMat };
    for (const t of W.towers) {
      const N = t.floors, half = t.side / 2, gHalf = half - SLAB_OUT;
      const plateAt = (f) => t.base_bearing + DIR * TWIST * (clamp(f, 1, N) - 1);
      const slabOut = plateOutline(half, NEXP), glassOut = plateOutline(gHalf, NEXP);
      const contour = slabOut.map(([u, v]) => new THREE.Vector2(u, v));
      const capTris = THREE.ShapeUtils.triangulateShape(contour, []);
      const toW = (th, u, v, y, out) => {
        const eu = dirOf(th), ev = dirOf(th + 90);
        return out.set(t.cx + u * eu.x + v * ev.x, y, t.cz + u * eu.z + v * ev.z);
      };
      const sPos = [], sNor = [], gPos = [], gNor = [], gUv = [], lin = [], hel = [];
      const V = new THREE.Vector3(), V2 = new THREE.Vector3();
      const M = slabOut.length;
      // arc length of the glass outline (for the fin rhythm: one fin every 1.5 m, an illustration)
      const gLen = [0]; for (let k = 1; k <= M; k++) { const a = glassOut[k - 1], b = glassOut[k % M]; gLen.push(gLen[k - 1] + Math.hypot(b[0] - a[0], b[1] - a[1])); }
      const normalAt = (out, k) => { const a = out[(k - 1 + M) % M], b = out[(k + 1) % M]; const tu = b[0] - a[0], tv = b[1] - a[1], L = Math.hypot(tu, tv); return [tv / L, -tu / L]; };
      const nrmS = slabOut.map((_, k) => normalAt(slabOut, k)), nrmG = glassOut.map((_, k) => normalAt(glassOut, k));
      const pushN = (arr, th, nu, nv) => { const eu = dirOf(th), ev = dirOf(th + 90); arr.push(nu * eu.x + nv * ev.x, 0, nu * eu.z + nv * ev.z); };
      for (let i = 1; i <= N + 1; i++) {
        const th = plateAt(Math.min(i, N));
        const y0 = (i - 1) * FH, y1 = y0 + SLAB_T;
        // slab caps
        for (const [a, b, c] of capTris) {
          const pa = toW(th, slabOut[a][0], slabOut[a][1], 0, new THREE.Vector3()), pb = toW(th, slabOut[b][0], slabOut[b][1], 0, new THREE.Vector3()), pc = toW(th, slabOut[c][0], slabOut[c][1], 0, new THREE.Vector3());
          const upw = (pb.z - pa.z) * (pc.x - pa.x) - (pb.x - pa.x) * (pc.z - pa.z) > 0;
          for (const [yy, ny] of [[y1, 1], [y0, -1]]) {
            const order = (ny > 0) === upw ? [a, b, c] : [a, c, b];
            for (const k of order) { toW(th, slabOut[k][0], slabOut[k][1], yy, V); sPos.push(V.x, V.y, V.z); sNor.push(0, ny, 0); }
          }
        }
        // slab edge
        for (let k = 0; k < M; k++) {
          const k2 = (k + 1) % M;
          const A0 = toW(th, slabOut[k][0], slabOut[k][1], y0, new THREE.Vector3()), A1 = toW(th, slabOut[k][0], slabOut[k][1], y1, new THREE.Vector3());
          const B0 = toW(th, slabOut[k2][0], slabOut[k2][1], y0, new THREE.Vector3()), B1 = toW(th, slabOut[k2][0], slabOut[k2][1], y1, new THREE.Vector3());
          for (const P of [A0, B1, B0, A0, A1, B1]) sPos.push(P.x, P.y, P.z);
          for (const kk of [k, k2, k2, k, k, k2]) pushN(sNor, th, nrmS[kk][0], nrmS[kk][1]);
          lin.push(A1.x, A1.y, A1.z, B1.x, B1.y, B1.z);
        }
        // the glass band of the floor (sides only)
        if (i <= N) {
          const g0 = y1, g1 = y0 + FH;
          for (let k = 0; k < M; k++) {
            const k2 = (k + 1) % M;
            const A0 = toW(th, glassOut[k][0], glassOut[k][1], g0, new THREE.Vector3()), A1 = toW(th, glassOut[k][0], glassOut[k][1], g1, new THREE.Vector3());
            const B0 = toW(th, glassOut[k2][0], glassOut[k2][1], g0, new THREE.Vector3()), B1 = toW(th, glassOut[k2][0], glassOut[k2][1], g1, new THREE.Vector3());
            for (const P of [A0, B1, B0, A0, A1, B1]) gPos.push(P.x, P.y, P.z);
            for (const kk of [k, k2, k2, k, k, k2]) pushN(gNor, th, nrmG[kk][0], nrmG[kk][1]);
            const u0 = gLen[k] / 1.5, u1 = gLen[k + 1] / 1.5;
            gUv.push(u0, 0, u1, 1, u1, 0, u0, 0, u0, 1, u1, 1);
          }
        }
      }
      // the four "corners" floor to floor: the spiral the turn draws on the façade
      for (const phi of [45, 135, 225, 315]) {
        let prev = null;
        for (let i = 1; i <= N + 1; i++) {
          const th = plateAt(Math.min(i, N));
          const r = plateRadius(half, NEXP, phi * DEG);
          const p = toW(th, r * Math.cos(phi * DEG), r * Math.sin(phi * DEG), (i - 1) * FH + SLAB_T * 0.5, new THREE.Vector3());
          if (prev) hel.push(prev.x, prev.y, prev.z, p.x, p.y, p.z);
          prev = p;
        }
      }
      const group = new THREE.Group();
      const sg = new THREE.BufferGeometry(); sg.setAttribute('position', new THREE.Float32BufferAttribute(sPos, 3)); sg.setAttribute('normal', new THREE.Float32BufferAttribute(sNor, 3));
      const gg = new THREE.BufferGeometry(); gg.setAttribute('position', new THREE.Float32BufferAttribute(gPos, 3)); gg.setAttribute('normal', new THREE.Float32BufferAttribute(gNor, 3)); gg.setAttribute('uv', new THREE.Float32BufferAttribute(gUv, 2));
      const slabMesh = new THREE.Mesh(sg, slabMat), glassMesh = new THREE.Mesh(gg, glassMat);
      for (const mm of [slabMesh, glassMesh]) { mm.castShadow = true; mm.receiveShadow = true; group.add(mm); }
      const lg = new THREE.BufferGeometry(); lg.setAttribute('position', new THREE.Float32BufferAttribute(lin, 3));
      const lines = new THREE.LineSegments(lg, lineMat); group.add(lines);
      const hg = new THREE.BufferGeometry(); hg.setAttribute('position', new THREE.Float32BufferAttribute(hel, 3));
      const helix = new THREE.LineSegments(hg, helixMat); group.add(helix);
      const top = N * FH + SLAB_T;
      // tower B: 37 floors x 4.0 m = 148 m; the published 157 m is reached by a roof crown (its form is an illustration)
      if (t.h > top + 1) {
        const ch = t.h - top, th = plateAt(N);
        const outer = plateOutline(gHalf - 1.2, NEXP), inner = plateOutline(gHalf - 2.0, NEXP);
        const shape = new THREE.Shape(outer.map(([u, v]) => new THREE.Vector2(u, v)));
        shape.holes.push(new THREE.Path(inner.slice().reverse().map(([u, v]) => new THREE.Vector2(u, v))));
        const cg = new THREE.ExtrudeGeometry(shape, { depth: ch, bevelEnabled: false, curveSegments: 4 });
        // shape (u, v) with extrusion along +z -> plate frame (u along th, v along th + 90), up = y
        const eu = dirOf(th), ev = dirOf(th + 90);
        cg.applyMatrix4(new THREE.Matrix4().set(eu.x, ev.x, 0, t.cx, 0, 0, 1, top, eu.z, ev.z, 0, t.cz, 0, 0, 0, 1));
        cg.computeVertexNormals();
        const cm = new THREE.Mesh(cg, new THREE.MeshStandardMaterial({ color: C.slab, roughness: 0.62, side: THREE.DoubleSide })); cm.castShadow = true; cm.receiveShadow = true; group.add(cm);
      }
      scene.add(group);
      TW[t.key] = { t, N, half, gHalf, plateAt, top, height: Math.max(top, t.h), group, lines, helix, FH, SLAB_T, NEXP };
    }
  }

  // the chosen tower / floor / facing in gold (the only gold in the world)
  let sel = null;
  function buildSelection() {
    const gold = new THREE.Color(C.gold);
    const ringMat = new THREE.MeshStandardMaterial({ color: gold, roughness: 0.4, metalness: 0.3, emissive: gold, emissiveIntensity: 0.45 });
    const bandMat = new THREE.MeshBasicMaterial({ color: gold, transparent: true, opacity: 0.42, depthWrite: false, side: THREE.DoubleSide });
    const wedgeMat = new THREE.MeshBasicMaterial({ color: gold, transparent: true, opacity: 0.35, depthWrite: false, side: THREE.DoubleSide });
    const goldLine = new THREE.LineBasicMaterial({ color: gold, transparent: true, opacity: 0.95 });
    const goldHelix = new THREE.LineBasicMaterial({ color: gold, transparent: true, opacity: 0.9 });
    const ring = new THREE.Mesh(new THREE.BufferGeometry(), ringMat);
    const band = new THREE.Mesh(new THREE.BufferGeometry(), bandMat);
    const wedge = new THREE.Mesh(new THREE.BufferGeometry(), wedgeMat);
    ring.renderOrder = 2; band.renderOrder = 3; wedge.renderOrder = 3;
    const eyeDot = new THREE.Mesh(new THREE.SphereGeometry(0.9, 16, 10), new THREE.MeshBasicMaterial({ color: gold }));
    for (const x of [ring, band, wedge, eyeDot]) { x.visible = false; scene.add(x); }
    sel = { ring, band, wedge, eyeDot, goldLine, goldHelix };
  }
  function updateSelection() {
    for (const k in TW) { const X = TW[k]; X.helix.material = k === S.tower && S.mode === 'tower' ? sel.goldHelix : W.towerMats.helixMat; }
    const X = TW[S.tower];
    const showFloor = !!(X && S.floor && S.mode === 'tower');
    sel.ring.visible = sel.band.visible = showFloor && S.view === 'out';
    sel.wedge.visible = sel.eyeDot.visible = showFloor && S.view === 'out' && S.facing != null;
    if (!showFloor) return;
    const f = S.floor, th = X.plateAt(f), y0 = (f - 1) * X.FH;
    const outer = plateOutline(X.half + 0.25, X.NEXP, 96), inner = plateOutline(X.gHalf - 0.1, X.NEXP, 96);
    const eu = dirOf(th), ev = dirOf(th + 90);
    const w = (u, v, y) => [X.t.cx + u * eu.x + v * ev.x, y, X.t.cz + u * eu.z + v * ev.z];
    // a gold ring on the slab edge, top and side
    const rp = [];
    const M = outer.length;
    for (let k = 0; k < M; k++) {
      const k2 = (k + 1) % M;
      const a = w(outer[k][0], outer[k][1], y0 + X.SLAB_T + 0.06), b = w(outer[k2][0], outer[k2][1], y0 + X.SLAB_T + 0.06);
      const c = w(inner[k][0], inner[k][1], y0 + X.SLAB_T + 0.06), d = w(inner[k2][0], inner[k2][1], y0 + X.SLAB_T + 0.06);
      rp.push(...a, ...c, ...b, ...b, ...c, ...d);
      const a0 = w(outer[k][0], outer[k][1], y0 - 0.06), b0 = w(outer[k2][0], outer[k2][1], y0 - 0.06);
      rp.push(...a0, ...b, ...a, ...a0, ...b0, ...b);
    }
    sel.ring.geometry.dispose();
    sel.ring.geometry = new THREE.BufferGeometry(); sel.ring.geometry.setAttribute('position', new THREE.Float32BufferAttribute(rp, 3)); sel.ring.geometry.computeVertexNormals();
    // a gold veil over the floor's glass
    const gp = [], gi = plateOutline(X.gHalf + 0.08, X.NEXP, 96);
    for (let k = 0; k < gi.length; k++) {
      const k2 = (k + 1) % gi.length;
      const a = w(gi[k][0], gi[k][1], y0 + X.SLAB_T), b = w(gi[k2][0], gi[k2][1], y0 + X.SLAB_T), c = w(gi[k][0], gi[k][1], y0 + X.FH), d = w(gi[k2][0], gi[k2][1], y0 + X.FH);
      gp.push(...a, ...b, ...d, ...a, ...d, ...c);
    }
    sel.band.geometry.dispose();
    sel.band.geometry = new THREE.BufferGeometry(); sel.band.geometry.setAttribute('position', new THREE.Float32BufferAttribute(gp, 3));
    if (S.facing != null) {
      const b = facingBearing(S.tower, S.floor, S.facing);
      const eye = towerEye(S.tower, S.floor, b, -0.6);
      const yy = y0 + X.SLAB_T + 0.1;
      const wp = [eye.x, yy, eye.z];
      for (let a = -22.5; a <= 22.5; a += 3.75) { const dd = dirOf(b + a); wp.push(eye.x + dd.x * 70, yy, eye.z + dd.z * 70); }
      const tris = []; for (let i = 1; i + 1 < wp.length / 3; i++) tris.push(wp[0], wp[1], wp[2], wp[3 * i], wp[3 * i + 1], wp[3 * i + 2], wp[3 * i + 3], wp[3 * i + 4], wp[3 * i + 5]);
      sel.wedge.geometry.dispose();
      sel.wedge.geometry = new THREE.BufferGeometry(); sel.wedge.geometry.setAttribute('position', new THREE.Float32BufferAttribute(tris, 3));
      sel.eyeDot.position.set(eye.x, (f - 1) * X.FH + 1.6, eye.z);
    }
  }

  // ---------------------------------------------------------------- places layer (dots in one draw call + the route)
  let placeDots = null, routeMesh = null, isoLines = null;
  function buildPlacesLayer() {
    const cv = document.createElement('canvas'); cv.width = cv.height = 64;
    const g = cv.getContext('2d');
    g.fillStyle = '#FAF7F1'; g.beginPath(); g.arc(32, 32, 30, 0, Math.PI * 2); g.fill();
    g.fillStyle = '#1B1A17'; g.beginPath(); g.arc(32, 32, 22, 0, Math.PI * 2); g.fill();
    const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace;
    placeDots = new THREE.Points(new THREE.BufferGeometry(), new THREE.PointsMaterial({ map: tex, size: 13, sizeAttenuation: false, transparent: true, alphaTest: 0.4, depthTest: false }));
    placeDots.renderOrder = 8; placeDots.visible = false; placeDots.frustumCulled = false;
    scene.add(placeDots);
    routeMesh = new THREE.Mesh(new THREE.BufferGeometry(), new THREE.MeshBasicMaterial({ color: C.ink, transparent: true, opacity: 0.82, depthWrite: false, side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: -4, polygonOffsetUnits: -4 }));
    routeMesh.renderOrder = 6; routeMesh.visible = false; routeMesh.frustumCulled = false;
    scene.add(routeMesh);
    isoLines = new THREE.Group(); isoLines.visible = false; scene.add(isoLines);
  }

  // ================================================================================================ geometry queries
  const eyeH = (f) => (f - 1) * W.model.fh + 1.6;
  function facingBearings(k, f) {
    const X = TW[k]; const th = X.plateAt(f);
    const list = []; for (let i = 0; i < 8; i++) list.push(norm360(th + i * 45));
    // start from the bearing nearest north, clockwise
    list.sort((a, b) => a - b);
    let s = 0, best = 999; list.forEach((b, i) => { const d = Math.min(b, 360 - b); if (d < best) { best = d; s = i; } });
    return list.slice(s).concat(list.slice(0, s));
  }
  const facingBearing = (k, f, idx) => facingBearings(k, f)[idx];
  const dirWord = (b) => T.dirs[Math.round(norm360(b) / 45) % 8];
  // the eye at floor f looking along bearing b, `inset` metres inside the glass line
  function towerEye(k, f, b, inset = 0.35) {
    const X = TW[k];
    const th = X.plateAt(f);
    const phi = (b - th) * DEG;
    const r = plateRadius(X.gHalf, X.NEXP, phi) - inset;
    const d = dirOf(b);
    return new THREE.Vector3(X.t.cx + d.x * r, eyeH(f), X.t.cz + d.z * r);
  }
  // is the point lit by the sun (a ray to the sun against every building and the other towers)?
  function sunBlocked(px, py, pz, dx, dy, dz, skipTower) {
    if (dy <= 0) return true;
    const tMax = Math.min((260 - py) / dy, 6000);
    let hit = false;
    const stamp = ++W.stampN; if (stamp > 4e9) { W.stamp.fill(0); W.stampN = 1; }
    W.bgrid.walk(px, pz, dx, dz, tMax, (list) => {
      for (const id of list) {
        if (W.stamp[id] === stamp) continue; W.stamp[id] = stamp;
        const b = W.blocks[id];
        if (b.h <= py + 0.01 && true) { /* the roof is below the eye; the ray only climbs */ continue; }
        if (rayPrism(px, py, pz, dx, dy, dz, b.P, b.h) < Infinity) { hit = true; return true; }
      }
      return false;
    });
    if (hit) return true;
    for (const k in TW) {
      if (k === skipTower) continue;
      const X = TW[k];
      if (rayCylinder(px, py, pz, dx, dy, dz, X.t.cx, X.t.cz, X.half * 0.97, X.height) < Infinity) return true;
    }
    return false;
  }
  function sunHoursFor(k, f, b, season) {
    if (!TW[k]) return null;
    const p = towerEye(k, f, b, -0.8);
    const n = dirOf(b);
    const step = 10;
    let lit = 0;
    const lat = W.origin.lat, lng = W.origin.lng;
    for (let mi = 4 * 60; mi <= 21 * 60; mi += step) {
      const s = sunAt(season, mi / 60, lat, lng);
      if (s.alt <= 0.5) continue;
      const d = dirOf(s.bearing); const ca = Math.cos(s.alt * DEG);
      const dx = d.x * ca, dz = d.z * ca, dy = Math.sin(s.alt * DEG);
      if (dx * n.x + dz * n.z < 0.05) continue; // the sun is behind this façade
      if (!sunBlocked(p.x, p.y, p.z, dx, dy, dz, k)) lit += step;
    }
    return Math.round(lit / 30) / 2;
  }
  function sunOnWindowNow(k, f, b) {
    const s = sunAt(S.season, S.hour, W.origin.lat, W.origin.lng);
    if (s.alt <= 0.5) return false;
    const p = towerEye(k, f, b, -0.8), n = dirOf(b), d = dirOf(s.bearing), ca = Math.cos(s.alt * DEG);
    if (d.x * ca * n.x + d.z * ca * n.z < 0.05) return false;
    return !sunBlocked(p.x, p.y, p.z, d.x * ca, Math.sin(s.alt * DEG), d.z * ca, k);
  }

  // what is under the pointer: labels are DOM; then the towers, the buildings, the ground
  const ray = { o: null, d: null };
  function pickAt(clientX, clientY) {
    const r = renderer.domElement.getBoundingClientRect();
    const ndc = new THREE.Vector2(((clientX - r.left) / r.width) * 2 - 1, -((clientY - r.top) / r.height) * 2 + 1);
    const rc = new THREE.Raycaster(); rc.setFromCamera(ndc, camera);
    const o2 = rc.ray.origin, d = rc.ray.direction;
    ray.o = o2; ray.d = d;
    let best = { t: Infinity, hit: null };
    // places dots (screen distance)
    if (S.mode === 'places' && places && placeDots.visible) {
      let bd = 22, bp = null;
      const v = new THREE.Vector3();
      for (const p of places.shown) {
        v.set(p.x, 1, p.z).project(camera);
        if (v.z > 1) continue;
        const sx = (v.x * 0.5 + 0.5) * r.width, sy = (-v.y * 0.5 + 0.5) * r.height;
        const dd = Math.hypot(sx - (clientX - r.left), sy - (clientY - r.top));
        if (dd < bd) { bd = dd; bp = p; }
      }
      if (bp) return { kind: 'place', place: bp };
    }
    for (const k in TW) {
      const X = TW[k];
      const t = rayCylinder(o2.x, o2.y, o2.z, d.x, d.y, d.z, X.t.cx, X.t.cz, X.half * 0.98, X.height);
      if (t < best.t) best = { t, hit: { kind: 'tower', key: k, y: o2.y + d.y * t } };
    }
    // buildings (grid walk along the ray's ground projection, until the ray is under ground)
    const tGround = d.y < -1e-6 ? -o2.y / d.y : 8000;
    const stamp = ++W.stampN;
    W.bgrid.walk(o2.x, o2.z, d.x, d.z, Math.min(tGround, 8000), (list, tEnter) => {
      if (tEnter > best.t) return true;
      for (const id of list) {
        if (W.stamp[id] === stamp) continue; W.stamp[id] = stamp;
        const b = W.blocks[id];
        const t = rayPrism(o2.x, o2.y, o2.z, d.x, d.y, d.z, b.P, b.h);
        if (t < best.t) best = { t, hit: { kind: 'block', block: b } };
      }
      return false;
    });
    if (best.hit) return best.hit;
    if (d.y < -1e-6) {
      const x = o2.x + d.x * tGround, z = o2.z + d.z * tGround;
      return groundAt(x, z);
    }
    return null;
  }
  function groundAt(x, z) {
    // trees (within 3 m of a crown's centre)
    if (W.pond && pip(W.pond, x, z)) return { kind: 'pond', x, z };
    if (W.park && pip(W.park, x, z)) return { kind: 'park', x, z };
    const sl = W.sgrid.at(x, z);
    if (sl) {
      let bs = null, bd = 1e9;
      for (const i of sl) { const s = W.streets[i]; for (let k = 0; k + 3 < s.P.length; k += 2) { const dd = segDist(x, z, s.P[k], s.P[k + 1], s.P[k + 2], s.P[k + 3]); if (dd < s.w * 0.5 && dd < bd) { bd = dd; bs = s; } } }
      if (bs) return bs.ring ? { kind: 'road', x, z } : { kind: 'street', street: bs, x, z };
    }
    const gl = W.ggrid.at(x, z);
    if (gl) for (const i of gl) { const g = W.greens[i]; if (pip(g.P, x, z)) return { kind: 'green', green: g, x, z }; }
    for (const w of W.water) if (w.outer && x >= w.bb[0] && x <= w.bb[2] && z >= w.bb[1] && z <= w.bb[3] && pip(w.P, x, z)) return { kind: 'water', water: w, x, z };
    for (const l of W.lots) if (pip(l.P, x, z)) return { kind: 'lot', lot: l, x, z };
    return null;
  }

  // ================================================================================================ camera
  function applyProjection() {
    const w = root.clientWidth || 1, h = root.clientHeight || 1;
    camera.aspect = w / h;
    const n = camera.near, t = n * Math.tan(proj.top * DEG), b = n * Math.tan(proj.bottom * DEG);
    const hw = (t - b) * camera.aspect / 2;
    camera.projectionMatrix.makePerspective(-hw, hw, t, b, n, camera.far, THREE.WebGLCoordinateSystem);
    if (!fp && narrow()) camera.projectionMatrix.elements[9] -= sheetFrac() * 0.92;
    camera.projectionMatrixInverse.copy(camera.projectionMatrix).invert();
    camera.fov = proj.top - proj.bottom;
  }
  const portrait = () => root.clientWidth / Math.max(1, root.clientHeight) < 0.85;
  let sheetCache = 0;
  function sheetFrac() {
    const h = root.clientHeight || 1;
    let px = 0;
    if (ui.card && !ui.card.hidden) px = ui.card.offsetHeight;
    else if (ui.panel && !ui.panel.hidden) px = ui.panel.offsetHeight;
    sheetCache = clamp(px / h, 0, 0.6);
    return sheetCache;
  }
  const narrow = () => root.clientWidth < 720;
  function lookFrom(target, bearingFromTarget, elevDeg, dist) {
    const d = dirOf(bearingFromTarget), c = Math.cos(elevDeg * DEG);
    return new THREE.Vector3(target.x + d.x * c * dist, target.y + Math.sin(elevDeg * DEG) * dist, target.z + d.z * c * dist);
  }
  // fly the camera; pose = { pos, target, top, bottom, near, far }
  function flyTo(pose, ms = 1100) {
    const from = { pos: camera.position.clone(), target: curTarget.v ? curTarget.v.clone() : pose.target.clone(), top: proj.top, bottom: proj.bottom };
    if (reduced || !o.motion || ms <= 0 || !isReady || !anim && from.pos.lengthSq() === 0) {
      setPose(pose); anim = null; return;
    }
    anim = { from, to: pose, t0: performance.now(), ms };
    invalidate();
  }
  function setPose(p) {
    camera.near = p.near || camera.near; camera.far = p.far || camera.far;
    proj.top = p.top; proj.bottom = p.bottom;
    camera.position.copy(p.pos);
    camera.up.set(0, 1, 0);
    camera.lookAt(p.target);
    curTarget.v = p.target.clone();
    applyProjection();
    if (!fp) { controls.target.copy(p.target); controls.update(); }
    invalidate();
  }
  function stepAnim(now) {
    if (!anim) return;
    const k = clamp((now - anim.t0) / anim.ms, 0, 1), e = ease(k);
    const a = anim.from, b = anim.to;
    const pos = a.pos.clone().lerp(b.pos, e), tg = a.target.clone().lerp(b.target, e);
    // the flight arcs a little upwards between two far poses
    const lift = Math.sin(Math.PI * e) * Math.min(260, a.pos.distanceTo(b.pos) * 0.18);
    if (!b.noLift) pos.y += lift;
    setPose({ pos, target: tg, top: a.top + (b.top - a.top) * e, bottom: a.bottom + (b.bottom - a.bottom) * e, near: b.near, far: b.far });
    if (k >= 1) { anim = null; if (b.done) b.done(); }
  }
  // first-person (walk and window): a level camera with a shifted lens, so verticals stay vertical
  function fpTarget() { const d = dirOf(fp.yaw); return new THREE.Vector3(fp.x + d.x * 100, fp.y, fp.z + d.z * 100); }
  function fpPose() { return { pos: new THREE.Vector3(fp.x, fp.y, fp.z), target: fpTarget(), top: fp.top + fp.tilt, bottom: fp.bottom + fp.tilt, near: fp.near, far: fp.walk ? 12000 : 24000, noLift: fp.noLift }; }
  function applyFp() { setPose(fpPose()); }

  function orbitMode(enable) {
    controls.enabled = enable;
    if (enable) { fp = null; }
  }

  // ================================================================================================ modes
  function setMode(m, source = 'api') {
    if (!MODES.includes(m)) return;
    const prev = S.mode;
    S.mode = m;
    root.dataset.mode = m;
    if (ui.tabs) for (const k in ui.tabs) ui.tabs[k].setAttribute('aria-pressed', k === m ? 'true' : 'false');
    closeCard();
    placeDots.visible = m === 'places';
    routeMesh.visible = m === 'places' && !!S.place;
    isoLines.visible = m === 'places';
    if (ui.joy) ui.joy.hidden = m !== 'walk' || !coarse && !o.forceJoystick;
    frame.hidden = true;
    if (ui.eye) ui.eye.hidden = true;
    if (m !== 'walk' && prev === 'walk') S.collapsed = false;
    if (m === 'aerial') { orbitMode(true); setOrbitLimits('aerial'); flyTo(aerialPose(), prev === m ? 0 : 1300); }
    if (m === 'walk') { enterWalk(); }
    if (m === 'tower') {
      if (!S.tower) S.tower = 'C';
      if (!S.floor) S.floor = Math.min(30, TW[S.tower].N);
      S.view = S.facing != null && S.view === 'window' ? 'window' : 'out';
      towerCamera(true);
      emitFloor(source === 'init' ? 'api' : source);
    }
    if (m === 'places') { orbitMode(true); setOrbitLimits('places'); flyTo(placesPose(), 1300); ensurePlaces(); }
    updateSelection();
    renderPanel();
    if (W) applySun();
    invalidate();
  }
  function setOrbitLimits(kind) {
    controls.enablePan = kind !== 'tower';
    controls.minDistance = kind === 'tower' ? 90 : 160;
    controls.maxDistance = kind === 'tower' ? 900 : 4200;
    controls.minPolarAngle = 5 * DEG;
    controls.maxPolarAngle = kind === 'tower' ? 96 * DEG : 82 * DEG;
  }
  function aerialPose() {
    const ph = portrait();
    const target = new THREE.Vector3(ph ? 5 : -10, ph ? 70 : 42, ph ? 20 : -20);
    const pos = lookFrom(target, 142, ph ? 29 : 26, ph ? 1020 : 930);
    const half = ph ? 24 : 18;
    return { pos, target, top: half, bottom: -half, near: 3, far: 24000 };
  }
  function placesPose() {
    const ph = portrait();
    const target = new THREE.Vector3(ph ? 0 : 60, 0, ph ? -60 : -80);
    const pos = lookFrom(target, 180, ph ? 70 : 62, ph ? 3600 : 2500);
    const half = ph ? 24 : 20;
    return { pos, target, top: half, bottom: -half, near: 5, far: 24000 };
  }
  function towerOutPose() {
    const X = TW[S.tower];
    const y = (S.floor - 1) * X.FH;
    const target = new THREE.Vector3(X.t.cx, (clamp(y, 20, X.height - 20) + X.height * 0.5) / 2, X.t.cz);
    let b = 312;
    if (S.facing != null) b = facingBearing(S.tower, S.floor, S.facing) + 32;
    const ph = portrait();
    const pos = lookFrom(target, b, ph ? 9 : 7, ph ? 640 : 470);
    pos.y = Math.max(pos.y, 24);
    const half = ph ? 24 : 18;
    return { pos, target, top: half, bottom: -half, near: 1, far: 24000 };
  }
  function towerCamera(fly, ms) {
    if (S.view === 'window' && S.facing != null) {
      const b = facingBearing(S.tower, S.floor, S.facing);
      const e = towerEye(S.tower, S.floor, b, 0.35);
      const ph = portrait();
      fp = { x: e.x, y: e.y, z: e.z, yaw: b, tilt: 0, top: ph ? 15 : 19, bottom: ph ? -44 : -29, near: 2.7, noLift: true, window: true, yaw0: b };
      controls.enabled = false;
      frame.hidden = false;
      flyTo(fpPose(), fly ? (ms || 900) : 0);
    } else {
      orbitMode(true); setOrbitLimits('tower');
      frame.hidden = true;
      flyTo(towerOutPose(), fly ? (ms || 1100) : 0);
    }
    if (ui.eye) {
      ui.eye.hidden = !(S.view === 'window' && S.facing != null);
      if (!ui.eye.hidden) ui.eye.textContent = `${T.towerN(S.tower)} · ${T.floorN(S.floor)} · ${T.eye(eyeH(S.floor).toFixed(1))}`;
    }
  }
  function pickTower(k, source = 'api') {
    k = String(k || '').toUpperCase();
    if (!TW[k]) return;
    const keepFloor = S.floor;
    const keepB = S.facing != null && S.tower && S.floor ? facingBearing(S.tower, S.floor, S.facing) : null;
    S.tower = k;
    S.floor = clamp(keepFloor || 30, 1, TW[k].N);
    if (keepB != null) { const list = facingBearings(k, S.floor); let bi = 0; list.forEach((b, i) => { if (angDiff(b, keepB) < angDiff(list[bi], keepB)) bi = i; }); S.facing = bi; }
    if (S.mode !== 'tower') { setMode('tower', source); return; }
    towerCamera(true);
    applySun();
    updateSelection();
    renderPanel();
    emitFloor(source);
    if (S.facing != null) emitFacing(source);
  }
  function setFloor(n, source = 'api') {
    if (!S.tower) S.tower = 'C';
    const X = TW[S.tower];
    const f = clamp(Math.round(+n || 1), 1, X.N);
    let keepB = S.facing != null && S.floor ? facingBearing(S.tower, S.floor, S.facing) : null;
    S.floor = f;
    if (keepB != null) { const list = facingBearings(S.tower, f); let bi = 0; list.forEach((b, i) => { if (angDiff(b, keepB) < angDiff(list[bi], keepB)) bi = i; }); S.facing = bi; }
    if (S.mode !== 'tower') { setMode('tower', source); return; }
    towerCamera(S.view === 'out', 450);
    updateSelection();
    renderPanel(true);
    if (source === 'drag') return; // the slider tells the page once, when it is let go
    emitFloor(source);
    if (S.facing != null) emitFacing(source);
  }
  function setFacing(b, source = 'api') {
    if (!S.tower) S.tower = 'C';
    if (!S.floor) S.floor = Math.min(30, TW[S.tower].N);
    const list = facingBearings(S.tower, S.floor);
    let idx;
    if (b && typeof b === 'object' && b.index != null) idx = clamp(b.index | 0, 0, 7);
    else { const bb = norm360(+b || 0); idx = 0; list.forEach((x, i) => { if (angDiff(x, bb) < angDiff(list[idx], bb)) idx = i; }); }
    S.facing = idx;
    S.view = 'window';
    if (narrow()) S.collapsed = true;
    if (S.mode !== 'tower') setMode('tower', source);
    else { towerCamera(true); updateSelection(); renderPanel(); }
    applySun();
    emitFacing(source);
  }
  function setTowerView(v) {
    S.view = v === 'window' && S.facing != null ? 'window' : 'out';
    if (S.mode === 'tower') { towerCamera(true); updateSelection(); renderPanel(); }
  }
  function setSun(s = {}) {
    if (s.season && SEASONS[s.season]) S.season = +s.season;
    if (s.hour != null) S.hour = clamp(+s.hour, 5, 20);
    applySun();
    renderPanel(true);
  }
  function emitFloor(source) {
    if (!S.tower || !S.floor) return;
    const detail = { tower: S.tower, floor: S.floor, heightM: +eyeH(S.floor).toFixed(1), source };
    setPick();
    window.dispatchEvent(new CustomEvent('nl:floor', { detail }));
    if (o.onPick) o.onPick({ kind: 'floor', ...detail });
  }
  function emitFacing(source) {
    if (!S.tower || !S.floor || S.facing == null) return;
    const b = facingBearing(S.tower, S.floor, S.facing);
    const detail = { tower: S.tower, floor: S.floor, heightM: +eyeH(S.floor).toFixed(1), bearing: Math.round(b), facing: dirWord(b), source };
    setPick();
    window.dispatchEvent(new CustomEvent('nl:facing', { detail }));
    if (o.onPick) o.onPick({ kind: 'facing', ...detail });
  }
  function setPick() {
    const b = S.facing != null ? facingBearing(S.tower, S.floor, S.facing) : null;
    window.__nlpsPick = {
      tower: S.tower, floor: T.pickLabel(S.floor, S.tower), facing: b != null ? dirWord(b) : '',
      floorNum: S.floor, towerKey: S.tower, bearing: b != null ? Math.round(b) : null, unit: '', example: false, name: o.name || '',
    };
  }

  // ---------------------------------------------------------------- walk
  const SPOTS = {
    ring: { r: 108, b: 350, look: 158, lookP: 148 },
    park: { x: -62, z: 48, look: 62 },
    towers: { x: 10, z: 12, look: 330 },
    school: { x: -128, z: -18, look: 96 },
  };
  function walkSpot(k) {
    const s = SPOTS[k] || SPOTS.ring;
    let x = s.x, z = s.z;
    if (s.r) { x = Math.sin(s.b * DEG) * s.r; z = -Math.cos(s.b * DEG) * s.r; }
    const ph = portrait();
    fp = { x, y: 1.6, z, yaw: ph && s.lookP != null ? s.lookP : s.look, tilt: 0, top: ph ? 58 : 52, bottom: ph ? -22 : -12, near: 0.3, walk: true };
    controls.enabled = false;
    flyTo(fpPose(), 1200);
    applySun();
  }
  function enterWalk() { if (narrow()) S.collapsed = true; walkSpot('ring'); }
  const keys = new Set();
  let joyV = { x: 0, y: 0 };
  function walkStep(dt) {
    if (!fp || !fp.walk || anim) return false;
    let fw = 0, st = 0, turn = 0;
    if (keys.has('KeyW') || keys.has('ArrowUp')) fw += 1;
    if (keys.has('KeyS') || keys.has('ArrowDown')) fw -= 1;
    if (keys.has('KeyA')) st -= 1;
    if (keys.has('KeyD')) st += 1;
    if (keys.has('ArrowLeft')) turn -= 1;
    if (keys.has('ArrowRight')) turn += 1;
    fw += -joyV.y; st += joyV.x;
    if (!fw && !st && !turn) return false;
    const speed = (keys.has('ShiftLeft') || keys.has('ShiftRight') ? 9 : 3.6) * dt;
    fp.yaw = norm360(fp.yaw + turn * 70 * dt);
    const f = dirOf(fp.yaw), r = dirOf(fp.yaw + 90);
    const nx = fp.x + (f.x * fw + r.x * st) * speed, nz = fp.z + (f.z * fw + r.z * st) * speed;
    if (free(nx, nz)) { fp.x = nx; fp.z = nz; }
    else if (free(nx, fp.z)) fp.x = nx;
    else if (free(fp.x, nz)) fp.z = nz;
    applyFp();
    return true;
  }
  function free(x, z) {
    if (Math.hypot(x, z) > 690) return false;
    const R = 0.45;
    for (const k in TW) { const X = TW[k]; if (Math.hypot(x - X.t.cx, z - X.t.cz) < X.half + R) return false; }
    if (W.pond && pip(W.pond, x, z)) return false;
    const list = W.bgrid.at(x, z);
    if (list) for (const id of list) {
      const b = W.blocks[id];
      if (x < b.bb[0] - R || x > b.bb[2] + R || z < b.bb[1] - R || z > b.bb[3] + R) continue;
      if (pip(b.P, x, z)) return false;
      const P = b.P, n = P.length / 2;
      for (let i = 0; i < n; i++) { const j = (i + 1) % n; if (segDist(x, z, P[2 * i], P[2 * i + 1], P[2 * j], P[2 * j + 1]) < R) return false; }
    }
    return true;
  }

  function northUp() {
    if (fp) { if (fp.walk) { fp.yaw = 0; applyFp(); } return; }
    const tg = controls.target.clone(), dist = camera.position.distanceTo(tg);
    const elev = Math.asin(clamp((camera.position.y - tg.y) / dist, -1, 1)) / DEG;
    flyTo({ pos: lookFrom(tg, 180, elev, dist), target: tg, top: proj.top, bottom: proj.bottom, near: camera.near, far: camera.far, noLift: true }, 700);
  }

  // ================================================================================================ sun and light
  function applySun() {
    const s = sunAt(S.season, S.hour, W.origin.lat, W.origin.lng);
    const up = s.alt > 0;
    const d = dirOf(s.bearing), ca = Math.cos(Math.max(s.alt, 0.5) * DEG);
    const dir = new THREE.Vector3(d.x * ca, Math.sin(Math.max(s.alt, 0.5) * DEG), d.z * ca).normalize();
    const focus = shadowFocus();
    sunLight.position.copy(focus.c).addScaledVector(dir, 3000);
    sunLight.target.position.copy(focus.c); sunLight.target.updateMatrixWorld();
    const cam = sunLight.shadow.camera;
    cam.left = -focus.half; cam.right = focus.half; cam.top = focus.half; cam.bottom = -focus.half; cam.near = 100; cam.far = 6500; cam.updateProjectionMatrix();
    sunLight.castShadow = up && !!o.shadows;
    const low = clamp(1 - s.alt / 45, 0, 1);
    sunLight.intensity = up ? 1.75 + 0.55 * (1 - low) : 0;
    sunLight.color.set(up ? new THREE.Color('#FFF6E8').lerp(new THREE.Color('#FFD7A0'), low * 0.6) : '#000000');
    hemi.intensity = up ? 1.75 : 1.15;
    hemi.color.set(up ? '#FFFBF3' : '#D7DCE6');
    renderer.toneMappingExposure = up ? 1.0 : 1.08;
    S.sun = s;
    renderer.shadowMap.needsUpdate = true;
    invalidate();
  }
  function shadowFocus() {
    if (fp && fp.window) { const dd = dirOf(fp.yaw); return { c: new THREE.Vector3(fp.x + dd.x * 380, 0, fp.z + dd.z * 380), half: 700 }; }
    if (fp && fp.walk) return { c: new THREE.Vector3(fp.x, 0, fp.z), half: 360 };
    if (S.mode === 'tower') { const X = TW[S.tower || 'C']; return { c: new THREE.Vector3(X.t.cx, 0, X.t.cz), half: 480 }; }
    if (S.mode === 'places') return { c: new THREE.Vector3(0, 0, -100), half: 1500 };
    return { c: new THREE.Vector3(-60, 0, -120), half: 950 };
  }

  // ================================================================================================ places
  let placesP = null;
  function loadPlaces() {
    if (!placesP) placesP = o.placesUrl ? fetch(o.placesUrl, { credentials: 'same-origin' }).then((r) => r.json()) : Promise.resolve({ places: [] });
    return placesP;
  }
  async function ensurePlaces() {
    if (places || !o.placesUrl) { if (places && S.mode === 'places') showCategory(); return; }
    try {
      const d = await loadPlaces();
      if (places) return;
      const list = (d.places || []).filter((p) => p.walk != null && !p.generic);
      const byId = {}; list.forEach((p) => { byId[p.id] = p; });
      places = { doc: d, list, byId, shown: [] };
      // the 5 / 10 / 15 minute areas (Mapbox walking, from the ring road; places.json "iso")
      const KX = Math.cos(W.origin.lat * DEG) * 111320;
      for (const iso of d.iso || []) {
        const pts = iso.ring.map(([lng, lat]) => new THREE.Vector3((lng - W.origin.lng) * KX, 0.6, -(lat - W.origin.lat) * 111320));
        pts.push(pts[0].clone());
        const line = new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), new THREE.LineDashedMaterial({ color: C.ink, dashSize: 9, gapSize: 7, transparent: true, opacity: 0.55, depthTest: false }));
        line.computeLineDistances(); line.renderOrder = 5;
        line.userData = { min: iso.min, top: pts.reduce((a, p) => (p.z < a.z ? p : a), pts[0]) };
        isoLines.add(line);
      }
      if (S.mode === 'places') { showCategory(); renderPanel(); }
    } catch (e) { console.warn('[nlw] places', e); }
  }
  function setCategory(c) { if (!T.cats[c]) return; S.cat = c; S.place = null; routeMesh.visible = false; closeCard(); showCategory(); renderPanel(); }
  function showCategory() {
    if (!places) return;
    const maxWalk = S.cat === 'transport' || S.cat === 'health' ? 15 : 12;
    places.shown = places.list.filter((p) => p.g === S.cat && p.walk <= maxWalk).sort((a, b) => a.walk - b.walk || a.dist - b.dist);
    const pos = []; places.shown.forEach((p) => pos.push(p.x, 1.2, p.z));
    placeDots.geometry.dispose();
    placeDots.geometry = new THREE.BufferGeometry(); placeDots.geometry.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    placeDots.visible = S.mode === 'places';
    places.maxWalk = maxWalk;
    invalidate();
  }
  // the walking route on the city's street axes (an estimate; the minutes are Mapbox's)
  let graph = null;
  function buildGraph() {
    const nodes = new Map(), adj = [];
    const key = (x, z) => Math.round(x) + ':' + Math.round(z);
    const id = (x, z) => { const k = key(x, z); let i = nodes.get(k); if (i == null) { i = adj.length; nodes.set(k, i); adj.push([]); xy.push(x, z); } return i; };
    const xy = [];
    for (const s of W.streets) {
      let prev = -1;
      for (let k = 0; k < s.P.length; k += 2) {
        const i = id(s.P[k], s.P[k + 1]);
        if (prev >= 0 && prev !== i) { const L = Math.hypot(xy[2 * i] - xy[2 * prev], xy[2 * i + 1] - xy[2 * prev + 1]); adj[prev].push(i, L); adj[i].push(prev, L); }
        prev = i;
      }
    }
    // join ends that the city's axes leave a few metres apart, and ends that meet another street between two of its vertices
    const g = new Grid(3400, 12);
    for (let i = 0; i < adj.length; i++) g.add(i, [xy[2 * i], xy[2 * i + 1], xy[2 * i], xy[2 * i + 1]]);
    const segs = [], sg = new Grid(3400, 20);
    for (let i = 0; i < adj.length; i++) for (let k = 0; k < adj[i].length; k += 2) { const j = adj[i][k]; if (j > i) { sg.add(segs.length, [Math.min(xy[2 * i], xy[2 * j]) - 8, Math.min(xy[2 * i + 1], xy[2 * j + 1]) - 8, Math.max(xy[2 * i], xy[2 * j]) + 8, Math.max(xy[2 * i + 1], xy[2 * j + 1]) + 8]); segs.push([i, j]); } }
    for (let i = 0; i < adj.length; i++) {
      if (adj[i].length > 2) continue;
      const x = xy[2 * i], z = xy[2 * i + 1];
      for (const j of g.at(x, z) || []) { if (j === i) continue; const L = Math.hypot(x - xy[2 * j], z - xy[2 * j + 1]); if (L < 6) { adj[i].push(j, L); adj[j].push(i, L); } }
      let best = null, bd = 9;
      for (const si of sg.at(x, z) || []) {
        const [a, b] = segs[si]; if (a === i || b === i) continue;
        const d = segDist(x, z, xy[2 * a], xy[2 * a + 1], xy[2 * b], xy[2 * b + 1]);
        if (d < bd) { bd = d; best = [a, b]; }
      }
      if (best) for (const e of best) { const L = Math.hypot(x - xy[2 * e], z - xy[2 * e + 1]); adj[i].push(e, L); adj[e].push(i, L); }
    }
    graph = { adj, xy, g, segs, sg };
  }
  // a point joins the street network through the nearest street segment (its two ends, with the walk along the segment)
  function attach(x, z) {
    let best = null, bd = 160;
    const { xy, segs } = graph;
    for (let r = 0; r <= 8 && !best; r++) {
      const c = graph.sg.cell;
      for (let i = -r; i <= r; i++) for (let j = -r; j <= r; j++) {
        if (Math.max(Math.abs(i), Math.abs(j)) !== r) continue;
        for (const si of graph.sg.at(x + i * c, z + j * c) || []) {
          const [a, b] = segs[si];
          const d = segDist(x, z, xy[2 * a], xy[2 * a + 1], xy[2 * b], xy[2 * b + 1]);
          if (d < bd) { bd = d; best = [a, b]; }
        }
      }
    }
    if (!best) return [];
    const [a, b] = best;
    const ax = xy[2 * a], az = xy[2 * a + 1], bx = xy[2 * b], bz = xy[2 * b + 1];
    const ex = bx - ax, ez = bz - az, L2 = ex * ex + ez * ez;
    const t = L2 ? clamp(((x - ax) * ex + (z - az) * ez) / L2, 0, 1) : 0;
    const px = ax + ex * t, pz = az + ez * t, L = Math.sqrt(L2);
    return [{ node: a, cost: bd + t * L, via: [px, pz] }, { node: b, cost: bd + (1 - t) * L, via: [px, pz] }];
  }
  function route(sx, sz, tx, tz) {
    if (!graph) buildGraph();
    const A = attach(sx, sz), B = attach(tx, tz);
    if (!A.length || !B.length) return null;
    const n = graph.adj.length, dist = new Float64Array(n).fill(Infinity), prev = new Int32Array(n).fill(-1);
    const heap = [];
    const endCost = new Map(B.map((e) => [e.node, e]));
    const push = (d, i) => { heap.push([d, i]); let k = heap.length - 1; while (k > 0) { const p = (k - 1) >> 1; if (heap[p][0] <= heap[k][0]) break; [heap[p], heap[k]] = [heap[k], heap[p]]; k = p; } };
    const pop = () => { const top = heap[0], last = heap.pop(); if (heap.length) { heap[0] = last; let k = 0; for (;;) { const l = 2 * k + 1, r = l + 1; let m = k; if (l < heap.length && heap[l][0] < heap[m][0]) m = l; if (r < heap.length && heap[r][0] < heap[m][0]) m = r; if (m === k) break; [heap[m], heap[k]] = [heap[k], heap[m]]; k = m; } } return top; };
    for (const e of A) if (e.cost < dist[e.node]) { dist[e.node] = e.cost; push(e.cost, e.node); }
    let guard = 0, bestEnd = null, bestLen = Infinity;
    while (heap.length && guard++ < 200000) {
      const [d, i] = pop();
      if (d > dist[i]) continue;
      if (d >= bestLen) break;
      const ec = endCost.get(i);
      if (ec && d + ec.cost < bestLen) { bestLen = d + ec.cost; bestEnd = ec; }
      const e = graph.adj[i];
      for (let k = 0; k < e.length; k += 2) { const j = e[k], nd = d + e[k + 1]; if (nd < dist[j]) { dist[j] = nd; prev[j] = i; push(nd, j); } }
    }
    if (!bestEnd) return null;
    const path = [];
    for (let i = bestEnd.node; i >= 0; i = prev[i]) path.push([graph.xy[2 * i], graph.xy[2 * i + 1]]);
    path.reverse();
    return { path: [A[0].via, ...path, bestEnd.via], len: bestLen };
  }
  function drawRoute(p) {
    const br = Math.atan2(p.x, -p.z) / DEG;
    const sx = Math.sin(br * DEG) * 138, sz = -Math.cos(br * DEG) * 138;
    let r = route(sx, sz, p.x, p.z);
    const straight = Math.hypot(p.x - sx, p.z - sz);
    let air = false;
    let pts;
    if (r && r.len < straight * 2.4 + 80) pts = [[sx, sz], ...r.path, [p.x, p.z]];
    else { pts = [[sx, sz], [p.x, p.z]]; air = true; }
    const w = 2.6, pos = [];
    for (let i = 0; i + 1 < pts.length; i++) {
      const [x0, z0] = pts[i], [x1, z1] = pts[i + 1];
      const dx = x1 - x0, dz = z1 - z0, L = Math.hypot(dx, dz); if (L < 0.05) continue;
      const nx = -dz / L * w / 2, nz = dx / L * w / 2;
      if (air) {
        // a dashed ribbon for the straight line
        for (let s = 0; s < L; s += 12) { const s1 = Math.min(L, s + 7); const ax = x0 + dx * s / L, az = z0 + dz * s / L, bx = x0 + dx * s1 / L, bz = z0 + dz * s1 / L; pos.push(ax + nx, 0.5, az + nz, bx + nx, 0.5, bz + nz, bx - nx, 0.5, bz - nz, ax + nx, 0.5, az + nz, bx - nx, 0.5, bz - nz, ax - nx, 0.5, az - nz); }
      } else {
        pos.push(x0 + nx, 0.5, z0 + nz, x1 + nx, 0.5, z1 + nz, x1 - nx, 0.5, z1 - nz, x0 + nx, 0.5, z0 + nz, x1 - nx, 0.5, z1 - nz, x0 - nx, 0.5, z0 - nz);
        for (let k = 0; k < 8; k++) { const a0 = k / 8 * Math.PI * 2, a1 = (k + 1) / 8 * Math.PI * 2; pos.push(x1, 0.5, z1, x1 + Math.cos(a0) * w / 2, 0.5, z1 + Math.sin(a0) * w / 2, x1 + Math.cos(a1) * w / 2, 0.5, z1 + Math.sin(a1) * w / 2); }
      }
    }
    routeMesh.geometry.dispose();
    routeMesh.geometry = new THREE.BufferGeometry(); routeMesh.geometry.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    routeMesh.visible = S.mode === 'places';
    S.routeStart = [sx, sz];
    return air;
  }
  function selectPlace(p) {
    S.place = p;
    const air = drawRoute(p);
    openCard(placeCard(p, air));
    // frame the start and the place
    const tg = new THREE.Vector3((p.x + S.routeStart[0]) / 2, 0, (p.z + S.routeStart[1]) / 2);
    const span = Math.max(260, Math.hypot(p.x - S.routeStart[0], p.z - S.routeStart[1]) * 1.9);
    const ph = portrait();
    flyTo({ pos: lookFrom(tg, 180, 64, span * (ph ? 1.75 : 1.35)), target: tg, top: proj.top, bottom: proj.bottom, near: 5, far: 24000, noLift: true }, 900);
    if (o.onPick) o.onPick({ kind: 'place', id: p.id, name: p.name, walk: p.walk });
    invalidate();
  }

  // ================================================================================================ labels
  const labelPool = new Map();
  const _v = () => new THREE.Vector3();
  function labelCandidates() {
    const L = [];
    const m = S.mode;
    const add = (o2) => L.push(o2);
    const lang2 = lang;
    const tDesc = (k) => { const X = TW[k]; return `${T.floorsN(X.N)} · ${T.meters(Math.round(X.t.h))}`; };
    if (m === 'places') {
      add({ id: 'twall', kind: 'tower', name: T.towersHere, meta: '', pos: new THREE.Vector3(0, 170, 0), prio: 40, click: () => openCard(simpleCard('square')) });
    } else if (!(fp && fp.window)) {
      if (m === 'tower' && S.tower && S.floor && S.view === 'out') {
        const X = TW[S.tower];
        add({ id: 'floor', kind: 'floor', name: T.floorTag(S.floor), meta: '', pos: new THREE.Vector3(X.t.cx, (S.floor - 1) * X.FH + 2, X.t.cz), prio: 0.5, side: X.half + 3 });
      }
      for (const k in TW) {
        const X = TW[k];
        add({ id: 't' + k, kind: 'tower', name: T.towerN(k), meta: tDesc(k), pos: new THREE.Vector3(X.t.cx, X.height + 5, X.t.cz), prio: 1, on: k === S.tower && m === 'tower', click: () => (m === 'tower' ? pickTower(k, 'user') : openCard(towerCard(k))) });
      }
    } else {
      for (const k in TW) { if (k === S.tower) continue; const X = TW[k]; add({ id: 't' + k, kind: 'tower', name: T.towerN(k), meta: tDesc(k), pos: new THREE.Vector3(X.t.cx, X.height + 5, X.t.cz), prio: 3, click: () => openCard(towerCard(k)) }); }
    }
    if (m === 'aerial' || m === 'walk' || m === 'tower') {
      for (const c of W.civic) add({ id: 'c' + c.key, kind: 'civic', name: lang2 === 'en' ? c.en : c.he, meta: '', pos: new THREE.Vector3(c.x, 22, c.z), prio: 20, click: () => openCard(civicCard(c.key)) });
      if (W.pond) add({ id: 'pond', kind: 'water', name: T.pond, meta: T.illus, pos: new THREE.Vector3(W.pondC[0], 0.5, W.pondC[1]), prio: 25, click: () => openCard(simpleCard('pond')) });
      if (W.park && m !== 'walk') add({ id: 'park', kind: 'green', name: T.park, meta: '', pos: new THREE.Vector3(-30, 0.5, 40), prio: 30, click: () => openCard(simpleCard('park')) });
    }
    if (m === 'aerial' || m === 'walk' || (m === 'places' && S.cat === 'outdoors')) {
      for (const f of W.features) add({ id: 'f' + f.key, kind: 'feature', name: lang === 'en' ? f.en : f.he, meta: m === 'walk' || m === 'places' ? T.illusSpot : '', pos: new THREE.Vector3(f.x, 0.6, f.z), prio: m === 'places' ? 60 : 70, dotOnly: m === 'aerial' && narrow(), click: () => openCard(featureCard(f.key)) });
    }
    if (m === 'aerial' || (fp && fp.window)) {
      const keysA = ['sea', 'port', 'reading_lighthouse', 'sportek', 'azrieli_center', 'ramat_aviv', 'tau', 'reading', 'city_hall', 'habima', 'azrieli_sarona', 'moshe_aviv', 'savidor', 'ichilov'];
      for (const mk of W.marks) {
        if (m === 'aerial' && !['sea', 'port', 'reading_lighthouse', 'sportek'].includes(mk.key)) continue;
        if (!keysA.includes(mk.key)) continue;
        add({ id: 'm' + mk.key, kind: 'mark', name: lang2 === 'en' ? mk.en : mk.he, meta: T.km(mk.dist), pos: new THREE.Vector3(mk.x, mk.key === 'sea' ? 1 : Math.max(20, mk.h || 30), mk.z), prio: 60 + mk.dist / 100, click: () => openCard(markCard(mk)) });
      }
    }
    if (fp && fp.window && W.sea) {
      const d = dirOf(fp.yaw);
      for (let r = 300; r < 7000; r += 40) {
        const x = fp.x + d.x * r, z = fp.z + d.z * r;
        if (x >= W.sea.bb[0] && x <= W.sea.bb[2] && z >= W.sea.bb[1] && z <= W.sea.bb[3] && pip(W.sea.P, x, z)) {
          const tw = W.marks.find((mk) => mk.key === 'sea');
          add({ id: 'seaview', kind: 'mark', name: tw ? (lang === 'en' ? tw.en : tw.he) : T.water, meta: T.km(Math.hypot(x - (TW[S.tower] ? TW[S.tower].t.cx : 0), z - (TW[S.tower] ? TW[S.tower].t.cz : 0))), pos: new THREE.Vector3(x, 1, z), prio: 45, click: () => tw && openCard(markCard(tw)) });
          break;
        }
      }
    }
    if ((m === 'aerial' || (fp && fp.window)) && placesIndex) {
      for (const pn of W.pins) {
        const p = placesIndex[pn.id]; if (!p) continue;
        if (m === 'aerial' && pn.tier !== 1) continue;
        add({ id: 'p' + pn.id, kind: 'pin', name: lang2 === 'en' ? pn.en : p.name, meta: p.opens ? p.opens : T.walkMin(p.walk), pos: new THREE.Vector3(p.x, 1.5, p.z), prio: 100 + pn.tier * 50 + p.dist / 20, click: () => openCard(placeCard(p)) });
      }
    }
    if (m === 'places' && places) {
      const n = narrow() ? 14 : 26;
      const seen = [];
      let k2 = 0;
      for (const p of places.shown.slice(0, 80)) {
        if (p === S.place) continue;
        const nm = placeName(p);
        if (seen.some((q) => q.nm === nm && Math.hypot(q.x - p.x, q.z - p.z) < 160)) continue;
        seen.push({ nm, x: p.x, z: p.z });
        if (k2++ >= n) break;
        add({ id: 'q' + p.id, kind: 'place', name: nm, meta: T.walkMin(p.walk), pos: new THREE.Vector3(p.x, 1.2, p.z), prio: 100 + k2, click: () => selectPlace(p) });
      }
      if (S.place) add({ id: 'q' + S.place.id, kind: 'place', name: placeName(S.place), meta: T.walkMin(S.place.walk), pos: new THREE.Vector3(S.place.x, 1.2, S.place.z), prio: 0, sel: true, click: () => selectPlace(S.place) });
      for (const l of isoLines.children) add({ id: 'iso' + l.userData.min, kind: 'iso', name: T.walkMin(l.userData.min), meta: '', pos: l.userData.top.clone(), prio: 50 });
    }
    if (m === 'walk' && fp) {
      // in the walk: only what is near enough to read
      return L.filter((x) => x.kind === 'tower' || x.pos.distanceTo(camera.position) < 520);
    }
    return L;
  }
  // first person: a label behind a building is not shown
  function occluded(pos) {
    const tgt = pos.clone(); tgt.y = Math.max(tgt.y, fp && fp.window ? 14 : 3);
    const o2 = camera.position, d = tgt.sub(o2); const len = d.length(); d.divideScalar(len);
    const slack = fp && fp.window ? 45 : 6;
    const stamp = ++W.stampN;
    let hit = false;
    W.bgrid.walk(o2.x, o2.z, d.x, d.z, len - slack, (list) => {
      for (const id of list) {
        if (W.stamp[id] === stamp) continue; W.stamp[id] = stamp;
        const b = W.blocks[id];
        const t = rayPrism(o2.x, o2.y, o2.z, d.x, d.y, d.z, b.P, b.h);
        if (t < len - slack) { hit = true; return true; }
      }
      return false;
    });
    if (hit) return true;
    for (const k in TW) { const X = TW[k]; if (fp && fp.window && k === S.tower) continue; const t = rayCylinder(o2.x, o2.y, o2.z, d.x, d.y, d.z, X.t.cx, X.t.cz, X.half * 0.9, X.height); if (t < len - 4) return true; }
    return false;
  }
  let placesIndex = null;
  const placeName = (p) => (lang === 'en' && p.names && p.names.en ? p.names.en : p.name);
  function labelEl(c) {
    let e = labelPool.get(c.id);
    if (!e) {
      e = el('div', 'nlw-pin');
      e.innerHTML = '<span class="d"></span><span class="s"></span><button class="t" type="button"><span class="n"></span><span class="m"></span></button>';
      e._t = e.querySelector('.t'); e._s = e.querySelector('.s'); e._n = e.querySelector('.n'); e._m = e.querySelector('.m');
      e._t.addEventListener('click', (ev) => { ev.stopPropagation(); if (e._click) e._click(); });
      labelsEl.appendChild(e);
      labelPool.set(c.id, e);
    }
    e.className = 'nlw-pin k-' + c.kind + (c.on ? ' is-on' : '') + (c.sel ? ' is-sel' : '');
    if (e._name !== c.name) { e._n.textContent = c.name; e._name = c.name; e._size = null; }
    if (e._meta !== c.meta) { e._m.textContent = c.meta || ''; e._m.style.display = c.meta ? '' : 'none'; e._meta = c.meta; e._size = null; }
    e._click = c.click;
    return e;
  }
  function layoutLabels() {
    if (!o.labels) return;
    const w = root.clientWidth, h = root.clientHeight;
    const cands = labelCandidates();
    const used = new Set();
    const camDir = _v(); camera.getWorldDirection(camDir);
    const reserved = [];
    const rr = root.getBoundingClientRect();
    for (const e of [ui.top, ui.panel, ui.card, ui.joy, ui.compass, ui.eye, ui.cap]) {
      if (!e || e.hidden || e.offsetParent === null) continue;
      const r = e.getBoundingClientRect();
      if (!r.width) continue;
      reserved.push({ x0: r.left - rr.left - 6, x1: r.right - rr.left + 6, y0: r.top - rr.top - 6, y1: r.bottom - rr.top + 6 });
    }
    const towerRects = [];
    for (const k in TW) {
      if (fp && fp.window && k === S.tower) continue;
      const X = TW[k];
      let x0 = 1e9, x1 = -1e9, y0 = 1e9, y1 = -1e9, ok = true;
      for (const dx of [-1, 1]) for (const dz of [-1, 1]) for (const yy of [0, X.height]) {
        const v = new THREE.Vector3(X.t.cx + dx * X.half, yy, X.t.cz + dz * X.half);
        if (v.clone().sub(camera.position).dot(camDir) <= 0) { ok = false; continue; }
        v.project(camera);
        const sx = (v.x * 0.5 + 0.5) * w, sy = (-v.y * 0.5 + 0.5) * h;
        x0 = Math.min(x0, sx); x1 = Math.max(x1, sx); y0 = Math.min(y0, sy); y1 = Math.max(y1, sy);
      }
      if (ok) towerRects.push({ x0: x0 + 2, x1: x1 - 2, y0: y0 + 16, y1 });
    }
    const placed = [];
    const hitAny = (r, list) => list.some((q) => !(r.x1 < q.x0 || r.x0 > q.x1 || r.y1 < q.y0 || r.y0 > q.y1));
    const pts = [];
    const firstPerson = !!fp;
    for (const c of cands) {
      if (c.kind === 'floor') { const right = new THREE.Vector3().crossVectors(camDir, new THREE.Vector3(0, 1, 0)).normalize(); c.pos.addScaledVector(right, rtl ? -c.side : c.side); }
      const p = c.pos.clone();
      const toP = p.clone().sub(camera.position);
      if (toP.dot(camDir) <= 0) continue;
      if (firstPerson && (c.kind === 'pin' || c.kind === 'civic' || c.kind === 'water' || c.kind === 'green' || c.kind === 'feature') && occluded(c.pos)) continue;
      p.project(camera);
      const x = (p.x * 0.5 + 0.5) * w, y = (-p.y * 0.5 + 0.5) * h;
      if (x < -30 || x > w + 30 || y < -30 || y > h + 30) continue;
      pts.push({ c, x, y });
    }
    pts.sort((a, b) => a.c.prio - b.c.prio);
    for (const { c, x, y } of pts) {
      const e = labelEl(c);
      used.add(c.id);
      e.style.display = 'block';
      e.style.transform = `translate(${x.toFixed(1)}px, ${y.toFixed(1)}px)`;
      e.classList.remove('is-dot');
      if (c.kind === 'iso') { const r = { x0: x - 30, x1: x + 30, y0: y - 10, y1: y + 10 }; if (hitAny(r, reserved) || hitAny(r, placed)) e.style.display = 'none'; else placed.push(r); continue; }
      if (!e._size) e._size = [e._t.offsetWidth, e._t.offsetHeight];
      if (c.kind === 'floor') { const tw0 = e._size[0]; const r = rtl ? { x0: x - tw0 - 8, x1: x, y0: y - 12, y1: y + 12 } : { x0: x, x1: x + tw0 + 8, y0: y - 12, y1: y + 12 }; if (hitAny(r, reserved)) e.style.display = 'none'; else placed.push(r); continue; }
      if (c.dotOnly) { e.classList.add('is-dot'); continue; }
      const tw = e._size[0], th = e._size[1];
      const stems = c.kind === 'tower' ? [12, 30] : [16, 34, 56, 80];
      const off = Math.max(0, tw / 2 - 12);
      const shifts = c.kind === 'tower' ? [0] : [0, off, -off];
      const opts2 = [];
      for (const s of stems) for (const dx of shifts) opts2.push({ s, dx, below: false });
      if (c.kind !== 'tower') for (const s of [14, 32]) for (const dx of shifts) opts2.push({ s, dx, below: true });
      let ok = false;
      for (const { s, dx, below } of opts2) {
        const r = below ? { x0: x + dx - tw / 2 - 3, x1: x + dx + tw / 2 + 3, y0: y + s - 2, y1: y + s + th + 3 } : { x0: x + dx - tw / 2 - 3, x1: x + dx + tw / 2 + 3, y0: y - s - th - 3, y1: y - s + 2 };
        if (r.x0 < 4 || r.x1 > w - 4 || r.y0 < 4 || r.y1 > h - 4) continue;
        if (hitAny(r, placed) || hitAny(r, reserved) || (c.kind !== 'tower' && hitAny(r, towerRects))) continue;
        placed.push(r);
        e._s.style.height = s + 'px'; e._s.style.top = below ? '0px' : (-s) + 'px';
        e._t.style.top = below ? s + 'px' : (-s) + 'px';
        e._t.style.transform = below ? (rtl ? 'translate(50%, 0)' : 'translate(50%, 0)') : '';
        e._t.style.right = (-dx).toFixed(1) + 'px';
        ok = true; break;
      }
      if (!ok) { if (c.kind === 'mark' || c.kind === 'tower' || c.kind === 'civic') e.style.display = 'none'; else e.classList.add('is-dot'); }
      const dot = { x0: x - 6, x1: x + 6, y0: y - 6, y1: y + 6 }; placed.push(dot);
    }
    for (const [id, e] of labelPool) if (!used.has(id)) e.style.display = 'none';
  }

  // ================================================================================================ cards
  const srcHtml = (keys) => {
    if (!keys || !keys.length) return '';
    const parts = keys.map((k) => { const s = W.sources[k]; if (!s) return esc(k); const t = esc(s[lang] || s.he); return s.url ? `<a href="${esc(s.url)}" target="_blank" rel="noopener nofollow">${t}</a>` : t; });
    return `<span class="nlw-src">${esc(T.source)}: ${parts.join(' · ')}</span>`;
  };
  const factList = (lines) => `<ul class="nlw-facts">${(lines || []).map((l) => `<li>${esc(l[lang] || l.he)}${srcHtml(l.src)}</li>`).join('')}</ul>`;
  const notesHtml = () => `<details class="nlw-notes"><summary>${esc(T.notesSum)}</summary><ul>${(W.model.notes || []).map((n) => `<li>${esc(n[lang] || n.he)}</li>`).join('')}</ul></details>`;
  function openCard(c) {
    if (!c || !ui.card) return;
    root.classList.add('has-card');
    ui.card.innerHTML = `<button class="nlw-x" type="button" aria-label="${esc(T.close)}"><svg viewBox="0 0 20 20" stroke="currentColor" stroke-width="1.8"><path d="M4 4l12 12M16 4L4 16"/></svg></button>` + c.html;
    ui.card.hidden = false;
    ui.card.querySelector('.nlw-x').addEventListener('click', closeCard);
    for (const b of ui.card.querySelectorAll('[data-act]')) b.addEventListener('click', () => { const f = c.acts && c.acts[b.dataset.act]; if (f) f(); });
    if (o.onPick && c.pick) o.onPick(c.pick);
    afterSheet();
    invalidate();
  }
  function closeCard() { root.classList.remove('has-card'); if (ui.card && !ui.card.hidden) { ui.card.hidden = true; ui.card.innerHTML = ''; afterSheet(); invalidate(); } }
  function afterSheet() {
    if (!camera || !narrow()) return;
    if (!fp) applyProjection();
    if (ui.joy) ui.joy.style.bottom = ((ui.panel && !ui.panel.hidden ? ui.panel.offsetHeight : 0) + 16) + 'px';
    invalidate();
  }
  const eyebrow = (s) => `<div class="nlw-eyebrow">${esc(s)}</div>`;
  const title = (s) => `<div class="nlw-title">${esc(s)}</div>`;
  const waBtn = (label) => (o.wa ? `<a class="nlw-btn nlw-btn--wa" href="${esc(o.wa)}" target="_blank" rel="noopener">${esc(label)}</a>` : '');
  function towerCard(k) {
    const X = TW[k];
    const html = eyebrow(T.towersAll) + title(T.towerN(k)) + factList(W.facts.tower[k]) +
      `<button class="nlw-btn nlw-btn--go" type="button" data-act="go">${esc(T.goTower)} ${esc(k)}</button>` + waBtn(T.askWa(k)) +
      `<div class="nlw-sec">${factList(W.facts.towers)}</div>` + notesHtml();
    return { html, acts: { go: () => { closeCard(); pickTower(k, 'user'); } }, pick: { kind: 'tower', tower: k, floors: X.N, height: X.t.h } };
  }
  function featureCard(key) {
    const f = W.features.find((x) => x.key === key);
    if (!f) return null;
    const html = eyebrow(T.park) + title(lang === 'en' ? f.en : f.he) + factList(f.lines) + `<div class="nlw-note">${esc(T.illusSpot)}</div>`;
    return { html, pick: { kind: 'feature', key } };
  }
  function civicCard(key) {
    const c = W.civic.find((x) => x.key === key);
    const html = eyebrow(T.square) + title(lang === 'en' ? c.en : c.he) + factList(W.facts[key]);
    return { html, pick: { kind: 'civic', key } };
  }
  function simpleCard(kind) {
    const titles = { park: T.park, pond: T.pond, road: T.road, ring: T.ringBld, square: T.square };
    let html = eyebrow(T.square) + title(titles[kind] || T.square) + factList(W.facts[kind]);
    if (kind === 'pond') html += `<div class="nlw-note">${esc(T.illus)}</div>`;
    return { html, pick: { kind } };
  }
  function blockCard(b) {
    const hs = (b.flags >> 6) & 3;
    const kindName = (b.flags & 32) ? T.blockBuilding : (b.flags & 1) ? T.blockPublic : T.block;
    if (b.flags & 8) return civicCard('school');
    if (b.flags & 16) return civicCard('centre');
    const ttl = b.name || kindName;
    const kv = [];
    if (b.floors > 0) kv.push(`<b>${esc(T.floorsN(b.floors))}</b>`);
    kv.push(`<span>${esc(T.heightAbout(Math.round(b.h)))}</span>`);
    if (b.year > 1800) kv.push(`<span>${esc(T.built(b.year))}</span>`);
    const where = T.fromTowers(T.km(Math.hypot(b.cx, b.cz)));
    let html = eyebrow(b.flags & 4 ? T.ringBld : b.name ? kindName : where) + title(ttl) + `<div class="nlw-kv">${kv.join('')}</div>` +
      `<div class="nlw-note">${esc(T.hSrc[hs])}${b.flags & 4 || b.name ? ' · ' + esc(where) : ''}</div>` + srcHtml(['tlv_513']);
    if (b.flags & 4) html += `<div class="nlw-sec">${factList(W.facts.ring)}</div>`;
    return { html, pick: { kind: 'block', index: b.i, h: b.h, floors: b.floors } };
  }
  function groundCard(hit) {
    if (hit.kind === 'park' || hit.kind === 'pond' || hit.kind === 'road') return simpleCard(hit.kind);
    if (hit.kind === 'street') return { html: eyebrow(T.street) + title(hit.street.name || T.street) + `<div class="nlw-note">${esc(T.fromTowers(T.km(Math.hypot(hit.x, hit.z))))}</div>` + srcHtml(['tlv_507']), pick: { kind: 'street', name: hit.street.name } };
    if (hit.kind === 'green') return { html: eyebrow(T.green) + title(hit.green.name || T.green) + `<div class="nlw-note">${esc(T.fromTowers(T.km(Math.hypot(hit.x, hit.z))))}</div>` + srcHtml(['tlv_503']), pick: { kind: 'green', name: hit.green.name } };
    if (hit.kind === 'water') return { html: eyebrow(T.water) + title(hit.water.name || T.water) + srcHtml(['tlv_504']), pick: { kind: 'water', name: hit.water.name } };
    if (hit.kind === 'lot') return simpleCard('square');
    return null;
  }
  function markCard(mk) {
    return { html: eyebrow(T.mark) + title(lang === 'en' ? mk.en : mk.he) + `<div class="nlw-kv"><b>${esc(T.markDist(T.km(mk.dist)))}</b></div>` + `<span class="nlw-src">${esc(T.source)}: OpenStreetMap</span>`, pick: { kind: 'mark', key: mk.key } };
  }
  function placeCard(p, air) {
    const kind = T.kinds[p.k] || T.cats[p.g] || '';
    const kv = [`<b>${esc(T.walkMin(p.walk))}</b>`, `<span>${esc(T.fromRing)}</span>`, `<span>${esc(T.km(p.dist))}</span>`];
    let html = eyebrow(`${T.cats[p.g] || ''}${kind && kind !== T.cats[p.g] ? ' · ' + kind : ''}`) + title(placeName(p)) + `<div class="nlw-kv">${kv.join('')}</div>`;
    const lines = [];
    if (p.addr) lines.push(esc(p.addr));
    if (p.info && p.info !== kind) lines.push(esc(p.info));
    if (p.opens) lines.push(esc(p.opens));
    if (p.lines && p.lines.length) lines.push(`${esc(T.lines)}: <bdi>${esc(p.lines.slice(0, 16).join(', '))}</bdi>`);
    if (lines.length) html += `<ul class="nlw-facts">${lines.map((l) => `<li>${l}</li>`).join('')}</ul>`;
    const srcMap = T.srcNames;
    const srcs = [];
    for (const k of String(p.src || '').split('+')) { const v = srcMap[k]; if (v && !srcs.includes(v)) srcs.push(v); }
    srcs.push(srcMap.walk);
    if (p.lines && p.lines.length && !srcs.includes(srcMap.lines)) srcs.push(srcMap.lines);
    html += `<span class="nlw-src">${esc(T.source)}: ${srcs.filter(Boolean).map(esc).join(' · ')}</span>`;
    if (S.mode === 'places') html += `<div class="nlw-note">${esc(air ? T.routeAir : T.routeNote)}</div>`;
    html += waBtn(T.askPlace);
    return { html, pick: { kind: 'place', id: p.id } };
  }

  // ================================================================================================ the panel (per mode)
  const chip = (label, pressed, data, cls = '') => `<button class="nlw-chip ${cls}" type="button" aria-pressed="${pressed ? 'true' : 'false'}" ${data}>${esc(label)}</button>`;
  function sunSection(open, withHours) {
    const rs = riseSet(S.season, W.origin.lat, W.origin.lng);
    const s = S.sun || sunAt(S.season, S.hour, W.origin.lat, W.origin.lng);
    const seasons = [3, 6, 9, 12].map((k) => chip(T.seasons[k], S.season === k, `data-season="${k}"`)).join('');
    let hoursLine = '';
    if (withHours && S.tower && S.floor && S.facing != null) {
      const b = facingBearing(S.tower, S.floor, S.facing);
      const h = sunHoursFor(S.tower, S.floor, b, S.season);
      const now = sunOnWindowNow(S.tower, S.floor, b);
      hoursLine = `<div class="nlw-line nlw-sun-line ${h ? '' : 'is-none'}">${esc(h ? T.sunHours(h.toString(), T.seasonsLong[S.season]) : T.sunNone(T.seasonsLong[S.season]))}</div>` +
        `<div class="nlw-note">${esc(now ? T.sunOnNow : T.sunOffNow)} · ${esc(T.sunNote)}</div>`;
    }
    return `<div class="nlw-sec nlw-sun">
      <div class="nlw-sechead"><span class="nlw-eyebrow">${esc(T.sun)}</span>${open ? '' : chip(T.sunOpen, false, 'data-sunopen="1"')}</div>
      ${open ? `<div class="nlw-row" role="group" aria-label="${esc(T.sun)}">${seasons}</div>
      <label class="nlw-lbl"><span>${esc(T.hour)}</span><b>${hhmm(S.hour * 60)}</b></label>
      <input class="nlw-range" type="range" min="5" max="20" step="0.25" value="${S.hour}" data-hour aria-label="${esc(T.hour)}">
      <div class="nlw-note">${esc(s.alt > 0 ? T.sunNow(s.alt.toFixed(0), s.bearing.toFixed(0)) : T.sunDown)} · ${esc(T.riseSet(hhmm(rs.rise), hhmm(rs.set)))}</div>
      ${hoursLine}` : (withHours && hoursLine ? hoursLine : '')}
    </div>`;
  }
  let panelLight = false;
  function renderPanel(light) {
    if (!ui.panel || !W) return;
    const p = ui.panel;
    // light updates keep the sliders under the finger: only the texts change
    if (light && panelLight === S.mode && p.querySelector('[data-hour]')) {
      const hv = p.querySelector('.nlw-sun .nlw-lbl b'); if (hv) hv.textContent = hhmm(S.hour * 60);
      if (S.mode === 'tower') {
        const fl = p.querySelector('[data-floorlbl]'); if (fl) fl.textContent = T.floorN(S.floor);
        const tt = p.querySelector('.nlw-title'); if (tt) tt.textContent = T.towerTitle(S.tower, S.floor);
        const ey = p.querySelector('[data-eye]'); if (ey) ey.textContent = T.eye(eyeH(S.floor).toFixed(1));
        const fr = p.querySelector('.nlw-faces'); if (fr) fr.outerHTML = facesHtml();
        bindFaces();
      }
      const sun = p.querySelector('.nlw-sun');
      if (sun) {
        const s = S.sun; const rs = riseSet(S.season, W.origin.lat, W.origin.lng);
        const notes = sun.querySelectorAll('.nlw-note');
        if (notes[0]) notes[0].textContent = `${s.alt > 0 ? T.sunNow(s.alt.toFixed(0), s.bearing.toFixed(0)) : T.sunDown} · ${T.riseSet(hhmm(rs.rise), hhmm(rs.set))}`;
        if (S.mode === 'tower' && S.facing != null) {
          const b = facingBearing(S.tower, S.floor, S.facing);
          const h = sunHoursFor(S.tower, S.floor, b, S.season);
          const line = sun.querySelector('.nlw-sun-line');
          if (line) { line.textContent = h ? T.sunHours(h.toString(), T.seasonsLong[S.season]) : T.sunNone(T.seasonsLong[S.season]); line.classList.toggle('is-none', !h); }
          if (notes[1]) notes[1].textContent = `${sunOnWindowNow(S.tower, S.floor, b) ? T.sunOnNow : T.sunOffNow} · ${T.sunNote}`;
        }
        sun.querySelectorAll('[data-season]').forEach((x) => x.setAttribute('aria-pressed', +x.dataset.season === S.season ? 'true' : 'false'));
      }
      return;
    }
    panelLight = S.mode;
    let html = '';
    const collapseBtn = narrow() ? `<button class="nlw-x" type="button" data-collapse aria-label="${esc(S.collapsed ? T.expand : T.collapse)}"><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.8"><path d="${S.collapsed ? 'M5 12l5-5 5 5' : 'M5 8l5 5 5-5'}"/></svg></button>` : '';
    const nar = narrow();
    if (S.mode === 'aerial') {
      html = eyebrow(T.eyebrow) + title(T.aerialTitle) + `<div class="nlw-sub nlw-intro">${esc(T.aerialIntro)}</div>` +
        `<div class="nlw-row">${['A', 'B', 'C'].map((k) => chip(T.towerN(k), false, `data-tower="${k}"`, 'nlw-tw')).join('')}</div>` +
        (S.collapsed ? '' : sunSection(S.sunOpen, false));
    } else if (S.mode === 'walk') {
      html = eyebrow(T.eyebrow) + title(T.walkTitle) + (S.collapsed ? '' : `<div class="nlw-sub nlw-intro">${esc(T.walkIntro)}</div>`) +
        `<div class="nlw-row nlw-scroll">${Object.keys(SPOTS).map((k) => chip(T.spots[k], false, `data-spot="${k}"`)).join('')}</div>` +
        (S.collapsed ? '' : `<div class="nlw-kbd">${coarse ? esc(T.walkKeysTouch) : T.walkKeysDesk}</div>` + sunSection(S.sunOpen, false));
    } else if (S.mode === 'tower') {
      const X = TW[S.tower];
      html = eyebrow(T.eyebrow) + title(T.towerTitle(S.tower, S.floor)) +
        (S.collapsed ? collapsedTowerLine() : (
          `<div class="nlw-row">${['A', 'B', 'C'].map((k) => chip(T.towerN(k), k === S.tower, `data-tower="${k}"`, 'nlw-tw')).join('')}</div>` +
          `<label class="nlw-lbl"><span data-floorlbl>${esc(T.floorN(S.floor))}</span><b data-eye>${esc(T.eye(eyeH(S.floor).toFixed(1)))}</b></label>` +
          `<input class="nlw-range" type="range" min="1" max="${X.N}" step="1" value="${S.floor}" data-floor aria-label="${esc(T.floor)}">` +
          `<div class="nlw-lbl"><span>${esc(T.facingLbl)}</span>${S.facing != null ? `<span class="nlw-seg">${chip(T.viewOut, S.view === 'out', 'data-view="out"')}${chip(T.viewWin, S.view === 'window', 'data-view="window"')}</span>` : ''}</div>` +
          facesHtml() + (S.facing == null && !nar ? `<div class="nlw-note">${esc(T.pickFacing)}</div>` : '') +
          sunSection(!nar || S.sunOpen, true) + notesHtml()));
    } else if (S.mode === 'places') {
      html = eyebrow(T.eyebrow) + title(T.placesTitle) +
        `<div class="nlw-row nlw-scroll" role="group">${Object.keys(T.cats).map((c) => chip(T.cats[c], c === S.cat, `data-cat="${c}"`)).join('')}</div>` +
        (places ? `<div class="nlw-line">${esc(T.catCount(places.shown.length, places.maxWalk))}</div>` : '') +
        (S.collapsed ? '' : `<div class="nlw-note">${esc(T.placesIntro)}</div>`);
    }
    p.innerHTML = collapseBtn + html;
    p.hidden = false;
    bindPanel();
    afterSheet();
  }
  function collapsedTowerLine() {
    if (S.facing == null) return '';
    const b = facingBearing(S.tower, S.floor, S.facing);
    const h = sunHoursFor(S.tower, S.floor, b, S.season);
    return `<div class="nlw-sub">${esc(T.faces(dirWord(b)))} · ${Math.round(b)}° · ${esc(T.eye(eyeH(S.floor).toFixed(1)))}</div>` +
      `<div class="nlw-line nlw-sun-line ${h ? '' : 'is-none'}">${esc(h ? T.sunHours(h.toString(), T.seasonsLong[S.season]) : T.sunNone(T.seasonsLong[S.season]))}</div>`;
  }
  function facesHtml() {
    const list = facingBearings(S.tower, S.floor);
    const hours = list.map((b) => sunHoursFor(S.tower, S.floor, b, S.season));
    const maxH = Math.max(1, ...hours);
    return `<div class="nlw-faces" role="group" aria-label="${esc(T.facingLbl)}">${list.map((b, i) => `<button class="nlw-face" type="button" data-face="${i}" aria-pressed="${S.facing === i ? 'true' : 'false'}" aria-label="${esc(T.faces(dirWord(b)))} ${Math.round(b)}°, ${esc(T.hoursShort(hours[i]))}">
      <span class="nlw-fw">${esc(T.dirsShort[Math.round(norm360(b) / 45) % 8])}</span><small><bdi>${Math.round(b)}°</bdi></small><span class="nlw-sunb"><i style="width:${Math.round(100 * hours[i] / maxH)}%"></i></span><small class="nlw-fh">${esc(T.hoursShort(hours[i]))}</small></button>`).join('')}</div>`;
  }
  function bindFaces() {
    ui.panel.querySelectorAll('[data-face]').forEach((b) => b.addEventListener('click', () => setFacing({ index: +b.dataset.face }, 'user')));
  }
  function bindPanel() {
    const p = ui.panel;
    p.querySelectorAll('[data-tower]').forEach((b) => b.addEventListener('click', () => pickTower(b.dataset.tower, 'user')));
    p.querySelectorAll('[data-spot]').forEach((b) => b.addEventListener('click', () => walkSpot(b.dataset.spot)));
    p.querySelectorAll('[data-cat]').forEach((b) => b.addEventListener('click', () => setCategory(b.dataset.cat)));
    p.querySelectorAll('[data-view]').forEach((b) => b.addEventListener('click', () => setTowerView(b.dataset.view)));
    p.querySelectorAll('[data-season]').forEach((b) => b.addEventListener('click', () => { S.season = +b.dataset.season; applySun(); renderPanel(true); }));
    p.querySelectorAll('[data-sunopen]').forEach((b) => b.addEventListener('click', () => { S.sunOpen = true; renderPanel(); }));
    const col = p.querySelector('[data-collapse]'); if (col) col.addEventListener('click', () => { S.collapsed = !S.collapsed; renderPanel(); invalidate(); });
    const hr = p.querySelector('[data-hour]'); if (hr) hr.addEventListener('input', () => { S.hour = +hr.value; applySun(); renderPanel(true); });
    const fl = p.querySelector('[data-floor]');
    if (fl) {
      fl.addEventListener('input', () => setFloor(+fl.value, 'drag'));
      fl.addEventListener('change', () => { emitFloor('user'); if (S.facing != null) emitFacing('user'); });
    }
    bindFaces();
  }

  // ================================================================================================ input
  function bindInput(cv) {
    let down = null;
    on(cv, 'pointerdown', (e) => {
      down = { x: e.clientX, y: e.clientY, t: performance.now(), id: e.pointerId, yaw: fp ? fp.yaw : 0, tilt: fp ? fp.tilt : 0 };
      controls.enableZoom = true; // engaged: the wheel may zoom now
      if (fp) { cv.setPointerCapture(e.pointerId); }
    });
    on(cv, 'pointermove', (e) => {
      if (!down || !fp || down.id !== e.pointerId) return;
      const dx = e.clientX - down.x, dy = e.clientY - down.y;
      const k = (fp.top - fp.bottom) / Math.max(200, root.clientHeight);
      fp.yaw = norm360(down.yaw - dx * k * (rtl ? 1 : 1));
      if (fp.window) { const d0 = ((fp.yaw - fp.yaw0 + 540) % 360) - 180; fp.yaw = norm360(fp.yaw0 + clamp(d0, -80, 80)); }
      fp.tilt = clamp(down.tilt + dy * k, fp.window ? -25 : -20, fp.window ? 30 : 35);
      anim = null;
      applyFp();
      if (fp.window) applySunFocusLazy();
    });
    const end = (e) => {
      if (!down) return;
      const moved = Math.hypot(e.clientX - down.x, e.clientY - down.y);
      const quick = performance.now() - down.t < 450;
      down = null;
      if (moved < 7 && quick) handleClick(e.clientX, e.clientY);
    };
    on(cv, 'pointerup', end);
    on(cv, 'pointercancel', () => { down = null; });
    on(cv, 'pointerleave', () => { if (!fp) setTimeout(() => { controls.enableZoom = false; }, 2500); });
    on(cv, 'wheel', (e) => { if (fp && fp.walk && controls.enableZoom) { e.preventDefault(); const d = dirOf(fp.yaw); const s = -Math.sign(e.deltaY) * 4; if (free(fp.x + d.x * s, fp.z + d.z * s)) { fp.x += d.x * s; fp.z += d.z * s; applyFp(); } } }, { passive: false });
    on(cv, 'keydown', (e) => {
      if (S.mode !== 'walk') return;
      if (['KeyW', 'KeyA', 'KeyS', 'KeyD', 'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ShiftLeft', 'ShiftRight'].includes(e.code)) { keys.add(e.code); e.preventDefault(); invalidate(); }
    });
    on(cv, 'keyup', (e) => keys.delete(e.code));
    on(cv, 'blur', () => keys.clear());
    if (ui.joy) {
      const knob = ui.joy.querySelector('i');
      let jid = null;
      const upd = (e) => {
        const r = ui.joy.getBoundingClientRect();
        const cx = r.left + r.width / 2, cy = r.top + r.height / 2, R = r.width / 2 - 14;
        let x = (e.clientX - cx) / R, y = (e.clientY - cy) / R; const L = Math.hypot(x, y); if (L > 1) { x /= L; y /= L; }
        joyV = { x, y };
        knob.style.transform = `translate(${x * R}px, ${y * R}px)`;
        invalidate();
      };
      on(ui.joy, 'pointerdown', (e) => { jid = e.pointerId; ui.joy.setPointerCapture(jid); upd(e); e.preventDefault(); });
      on(ui.joy, 'pointermove', (e) => { if (e.pointerId === jid) upd(e); });
      const stop = () => { jid = null; joyV = { x: 0, y: 0 }; knob.style.transform = ''; };
      on(ui.joy, 'pointerup', stop); on(ui.joy, 'pointercancel', stop);
    }
    on(root, 'keydown', (e) => { if (e.key === 'Escape') { if (ui.card && !ui.card.hidden) closeCard(); else if (root.classList.contains('nlw--full')) toggleFull(false); } });
  }
  let sunFocusT = 0;
  function applySunFocusLazy() { clearTimeout(sunFocusT); sunFocusT = setTimeout(applySun, 160); }
  function handleClick(x, y) {
    const hit = pickAt(x, y);
    if (!hit) { closeCard(); return; }
    if (hit.kind === 'place') { selectPlace(hit.place); return; }
    if (hit.kind === 'tower') {
      if (S.mode === 'tower' && !(fp && fp.window)) {
        const X = TW[hit.key];
        const f = clamp(Math.floor(hit.y / X.FH) + 1, 1, X.N);
        if (hit.key !== S.tower) { S.tower = hit.key; }
        setFloor(f, 'user');
        return;
      }
      openCard(towerCard(hit.key));
      return;
    }
    if (hit.kind === 'block') { openCard(blockCard(hit.block)); return; }
    const c = groundCard(hit);
    if (c) openCard(c); else closeCard();
  }
  function showThing(kind, id) {
    if (kind === 'tower') return openCard(towerCard(String(id).toUpperCase()));
    if (kind === 'civic') return openCard(civicCard(id));
    if (kind === 'feature') return openCard(featureCard(id));
    if (kind === 'block') { const b = id === 'ring' ? W.blocks.find((x) => x.flags & 4) : W.blocks[+id]; return b ? openCard(blockCard(b)) : null; }
    if (kind === 'place') { return ensurePlaces().then(() => loadPlaces()).then((d) => { const p = (places && places.byId[id]) || (d.places || []).find((x) => x.id === id); if (!p) return; if (S.mode === 'places') selectPlace(p); else openCard(placeCard(p)); }); }
    if (kind === 'mark') { const mk = W.marks.find((m) => m.key === id); return mk ? openCard(markCard(mk)) : null; }
    return openCard(simpleCard(kind));
  }
  function toggleFull(force) {
    const onF = force != null ? force : !root.classList.contains('nlw--full');
    root.classList.toggle('nlw--full', onF);
    if (ui.full) { ui.full.setAttribute('aria-label', onF ? T.unfull : T.full); ui.full.title = onF ? T.unfull : T.full; }
    setTimeout(resize, 30);
  }

  // ================================================================================================ render loop
  function invalidate() { dirty = true; }
  function resize() {
    if (!renderer) return;
    const w = root.clientWidth, h = root.clientHeight;
    if (!w || !h) return;
    renderer.setSize(w, h, false);
    applyProjection();
    if (fp) applyFp();
    invalidate();
  }
  let lastT = 0;
  // adaptive resolution: when frames in a row come slower than ~33 fps, the canvas renders a little smaller (labels are HTML
  // and stay sharp); it never goes under 75% of the starting ratio
  const adapt = { dts: [], base: 0 };
  function adaptDpr(dt) {
    if (o.adaptive === false) return;
    if (!adapt.base) adapt.base = dpr;
    adapt.dts.push(dt);
    if (adapt.dts.length < 45) return;
    const m = adapt.dts.slice().sort((a, b) => a - b)[22];
    adapt.dts.length = 0;
    const min = Math.max(0.75, adapt.base * 0.75);
    if (m > 0.03 && dpr > min + 0.01) { dpr = Math.max(min, +(dpr * 0.85).toFixed(3)); renderer.setPixelRatio(dpr); resize(); }
  }
  function loop() {
    if (destroyed || !visible) { raf = 0; return; }
    if (raf) return;
    raf = requestAnimationFrame(tick);
  }
  function tick(now) {
    raf = 0;
    if (destroyed) return;
    const dt = Math.min(0.05, (now - (lastT || now)) / 1000); lastT = now;
    if (anim) stepAnim(now);
    if (!fp && controls.enabled) controls.update();
    if (walkStep(dt)) { if (Math.random() < 0.08) applySun(); }
    if (dirty) { renderNow(); if (lastRendered && now - lastRendered < 120) adaptDpr((now - lastRendered) / 1000); lastRendered = now; }
    loop();
  }
  let lastRendered = 0;
  function renderNow() {
    dirty = false;
    sky.position.copy(camera.position);
    const t0 = performance.now();
    renderer.render(scene, camera);
    const dtR = performance.now() - t0;
    frameTimes.push(dtR); if (frameTimes.length > 60) frameTimes.shift();
    layoutLabels();
    updateChrome();
  }
  function updateChrome() {
    if (!ui.needle) return;
    const d = new THREE.Vector3(); camera.getWorldDirection(d);
    let yaw = Math.atan2(d.x, -d.z) / DEG;
    if (fp) yaw = fp.yaw;
    ui.needle.style.transform = `rotate(${(-yaw).toFixed(1)}deg)`;
    if (ui.scale) {
      const show = !fp && (S.mode === 'aerial' || S.mode === 'places');
      ui.scale.hidden = !show;
      ui.scale.style.display = show ? '' : 'none';
      if (show) {
        const dist = camera.position.distanceTo(controls.target);
        const mpp = 2 * dist * Math.tan((proj.top - proj.bottom) / 2 * DEG) / Math.max(1, root.clientHeight);
        const nice = [20, 50, 100, 200, 250, 500, 1000].find((m) => m / mpp > 70) || 1000;
        ui.scale.querySelector('i').style.width = (nice / mpp).toFixed(0) + 'px';
        ui.scale.querySelector('span').textContent = T.km(nice);
      }
    }
  }

  // ================================================================================================ measurement (QA)
  function stats() {
    const info = renderer ? renderer.info : null;
    if (renderer) renderNow();
    return {
      drawCalls: info ? info.render.calls : null, triangles: info ? info.render.triangles : null, lines: info ? info.render.lines : null, points: info ? info.render.points : null,
      geometries: info ? info.memory.geometries : null, textures: info ? info.memory.textures : null, dpr, size: [root.clientWidth, root.clientHeight],
      renderMs: frameTimes.length ? +(frameTimes.reduce((a, b) => a + b, 0) / frameTimes.length).toFixed(2) : null,
      blocks: W ? W.blocks.length : 0, trees: W ? W.trees.length / 3 : 0, mode: S.mode,
    };
  }
  function bench(ms = 3000) {
    return new Promise((res) => {
      const t0 = performance.now(); let n = 0; const times = [];
      const target = controls.target.clone(); const r0 = camera.position.clone().sub(target);
      const f = (now) => {
        n++; times.push(now);
        if (!fp) { const a = (now - t0) / 1000 * 0.25; const r = r0.clone().applyAxisAngle(new THREE.Vector3(0, 1, 0), a); camera.position.copy(target).add(r); camera.lookAt(target); }
        else { fp.yaw = norm360(fp.yaw + 0.3); applyFp(); }
        sky.position.copy(camera.position); renderer.render(scene, camera); layoutLabels();
        if (now - t0 < ms) requestAnimationFrame(f);
        else {
          const dts = []; for (let i = 1; i < times.length; i++) dts.push(times[i] - times[i - 1]);
          dts.sort((a, b) => a - b);
          res({ frames: n, fps: +(1000 * (n - 1) / (times[times.length - 1] - times[0])).toFixed(1), p95ms: +dts[Math.floor(dts.length * 0.95)].toFixed(1), drawCalls: renderer.info.render.calls, triangles: renderer.info.render.triangles });
          camera.position.copy(target).add(r0); camera.lookAt(target); invalidate();
        }
      };
      requestAnimationFrame(f);
    });
  }

  function destroy() {
    destroyed = true;
    if (raf) cancelAnimationFrame(raf);
    for (const [t, ev, fn, opt] of listeners) t.removeEventListener(ev, fn, opt);
    for (const f of disposables) try { f(); } catch (e) { /* ignore */ }
    if (scene) scene.traverse((x) => { if (x.geometry) x.geometry.dispose(); if (x.material) { const ms = Array.isArray(x.material) ? x.material : [x.material]; ms.forEach((m) => { if (m.map) m.map.dispose(); m.dispose(); }); } });
    if (controls) controls.dispose();
    if (renderer) { renderer.dispose(); renderer.forceContextLoss(); }
    root.remove();
  }

  // the featured pins read their names and minutes from places.json (a small separate fetch, after the world paints)
  ready.then(() => {
    if (!o.placesUrl) return;
    loadPlaces().then((d) => {
      placesIndex = {}; for (const p of d.places || []) placesIndex[p.id] = p;
      invalidate();
    }).catch(() => {});
  });

  return api;
}

export { I18N as WORLD_I18N, sunPos, sunAt };
