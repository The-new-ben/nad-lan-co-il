/*
 * DUO Tel Aviv, 3D stage (prototype, 28.9.2026): the two towers of Africa Israel Residences on the official lots 111 + 112
 * of plan 2988א (Somail South), in the city as it stands today. Built on the Rainbow stage's engine (rainbow/stage.js:
 * the same light, sky, water, glide, card, quarter pins and facility pins), with a scene of its own.
 *
 *   import { mountDuoStage } from './stage.js';
 *   const stage = mountDuoStage(document.getElementById('x'), { preset: 'sunset' });
 *   stage.dispose();
 *
 * The page needs an import map for "three" and "three/addons/" (three@0.170.0 on jsDelivr), like Rainbow's.
 * What is official and what is an illustration (docs/research/2026-09-28-stages/stage-geometry.md, section 3):
 *   OFFICIAL  the lot outline (GIS 837, lots 111 + 112 = 8,338 m², the permit's site), both tower footprints (GIS 513
 *             oids 44499 and 42941: 1,082 and 918 m²), the towers in the east half and the three commercial buildings and
 *             the sunken courtyard in the west half (licensing decision 1-25-0172, 21.9.2025), 50 residential floors with
 *             penthouses on 48-50 and private pools on 49-50, technical floors 51-52, 5 basements; the city around it (GIS).
 *   DEVELOPER the lobby of about 7 m joining the towers, the infinity pool on the lobby building's roof, the wellness
 *             complex, the gym and the residents' club.
 *   ILLUSTRATION every height (no official height or floor-to-floor height exists: 3.3 m a floor), the lobby building's
 *             and the commercial buildings' shapes and places inside their halves, the pools' shapes, the facade.
 *             The caption says so on the stage itself.
 * Events on window (user actions only, never for API calls), the same as Rainbow's so bridge.js works unchanged:
 *   nl:floor        { floor, heightM, tower, towerName }
 *   nl:facing       { floor, heightM, bearing, unit: 'N-25-w', toward, tower }
 *   nl:floor-action { action, floor, heightM, bearing, unit, tower }
 *   nl:floor-cta    { floor, bearing, tower }
 *   nl:quarter      { kind, name, id }
 */

let THREE = null;
let OrbitControls = null;

const DEG = Math.PI / 180;

const TEXT = {
  sunset: 'שקיעה',
  noon: 'צהריים',
  presets: 'תאורה',
  caption: 'הדמיה להמחשה בלבד, על בסיס מקורות פומביים. אינה תוכנית מכר.',
  // always printed after the caption (the page may replace the caption; never this line): what is official, what is not
  geo: 'המגרש וקווי המגדלים לפי עיריית תל אביב-יפו; הגבהים (3.3 מ׳ לקומה), הלובי והמסחר להמחשה.',
  floor: (n) => `קומה ${n}`,
  // one project-wide line for every floor: the developer's site gives 2 to 5 rooms and penthouses for the project
  low: 'דירות 2 עד 5 חדרים ופנטהאוזים, לפי אתר הפרויקט',
  high: 'דירות 2 עד 5 חדרים ופנטהאוזים, לפי אתר הפרויקט',
  penthouse: 'קומות הפנטהאוזים (48 עד 50), עם בריכות פרטיות בקומות 49 ו־50, לפי החלטת רשות הרישוי (9.2025)',
  cta: 'לקבלת פרטים על הקומה',
  open3d: 'סיור וירטואלי בפרויקט',
  hint: 'בחרו מגדל וקומה',
  facingHint: 'בחרו כיוון סביב הקומה',
  faces: 'פונה',
  dirs: ['צפונה', 'צפון מזרחה', 'מזרחה', 'דרום מזרחה', 'דרומה', 'דרום מערבה', 'מערבה', 'צפון מערבה'],
  close: 'סגירה',
  heroName: 'DUO',
  from: 'מ־DUO',                 // "180 מ׳ מ־DUO"
  in: 'ב־DUO',                   // "שאלה על הבריכה ב־DUO"
  towers: { N: 'מגדל צפוני', S: 'מגדל דרומי' },
  towerShort: { N: 'צפוני', S: 'דרומי' },
  aria: 'הדמיה של פרויקט DUO תל אביב: שני מגדלי מגורים ומתחם מסחר, בין אבן גבירול, ארלוזורוב ובן סרוק',
};

const DEFAULTS = {
  preset: 'sunset',
  poster: null,          // URL of the poster image; defaults to poster.jpg next to stage.js
  injectCss: true,       // adds stage.css (next to stage.js) once per page
  injectFonts: true,     // adds Assistant, Heebo, Frank Ruhl Libre and Noto Serif Hebrew from Google Fonts if missing
  force3D: false,        // skip the weak-device and software-renderer fallback
  ao: 'auto',            // 'auto' | 'on' | 'off'
  autoOrbit: true,
  intro: true,
  highFloorsFrom: 21,
  penthouseFloors: 3,    // floors 48-50 are the penthouse floors (licensing decision 1-25-0172, 21.9.2025)
  hint: true,
  adaptive: true,
  bearingOffset: 0,      // degrees added to every reported bearing (the scene's north is true north already)
  glide: true,
  wheel: 'engaged',
  toneMapping: 'aces',
  text: null,
  facingWords: null,     // (bearing) => words for that direction from the page ("לכיוון הים")
  floorNote: null,       // (floor, tower) => the page's sourced line for that floor, or null for the project-wide line
  quarter: null,         // quarter.json: { projects, places, note }
  autoFacing: null,      // a side id ('w'): the first tap on a floor also picks that side's example apartment
  actions: null,         // the floor card's actions: [{ id, label, kind: 'go' | 'sec' }]; each emits nl:floor-action
  units: null,           // example apartments: { sides: [{ id: 'w', bearing: 280 }, ...], label: 'דירה לדוגמה', chip: 'לדוגמה' }
  facilities: null,      // facilities.json's list (design system FacilityHotspots v72)
  wa: '',
  tower: 'N',            // the tower a floor opens on when none is named ("25-w" from the page's steps)
  debug: false,
};

/* Light presets (Rainbow's). Colours are sRGB hex, converted to linear at runtime. */
const PRESETS = {
  sunset: {
    sunAz: 208, sunEl: 16, sunColor: '#FFC690', sunI: 6.6,
    hemiSky: '#9FB6CC', hemiGround: '#CDB08A', hemiI: 0.22,
    envWhite: 0.5, envGlass: 1.0,
    zenith: '#AFBDCA', horizon: '#EFD3B8', warm: '#F3AE7A', glowCol: '#FFCB93', glow: 1.35, warmPow: 1.5, skyGain: 1.0,
    rose: '#E9C8C0', roseAmt: 0.45,
    envZenith: '#AFC3D6', envHorizon: '#E6DCCF',
    groundEnv: '#BFAE95',
    sea: '#1F5A70', seaShallow: '#5E9FA2', sparkle: 1.0,
    exposure: 0.95, fog: 1 / 5200,
  },
  noon: {
    sunAz: 158, sunEl: 60, sunColor: '#FFF4E6', sunI: 3.9,
    hemiSky: '#BFD2E2', hemiGround: '#D8CFC0', hemiI: 0.2,
    envWhite: 0.42, envGlass: 1.15,
    zenith: '#A3BED6', horizon: '#E3E9EC', warm: '#EEEBE4', glowCol: '#FFFFFF', glow: 0.25, warmPow: 2.0, skyGain: 1.03,
    rose: '#E3E9EC', roseAmt: 0.0,
    envZenith: '#A9C3DA', envHorizon: '#E0E6E8',
    groundEnv: '#CFC6B6',
    sea: '#236D8E', seaShallow: '#6DB4B7', sparkle: 0.55,
    exposure: 0.8, fog: 1 / 5600,
  },
};

/* ------------------------------------------------------------------------------------------ */
/* The site (metres). Frame of the research file, section 0.2: origin = the area-weighted centroid of lots 111 + 112     */
/* (32.085698, 34.782856); x = grid east, z = grid south; the grid is turned 10° east of true north, like the lots.      */
/* ------------------------------------------------------------------------------------------ */
const GRID_ANGLE = -10 * DEG;
const PLOT = { h: 1.2 };
/* lots 111 + 112 together (GIS 837, plan 2988א; 4,379 + 3,959 = 8,338 m², the permit's site 6213/1468), clockwise from the
   north-west corner; the rounded south-east corner is Arlozorov at Ben Saruk */
const LOT_OUTLINE = [[-42.3, -48.5], [44.5, -49.0], [44.6, -5.8], [40.0, -5.7], [40.0, 1.7], [39.7, 37.2], [39.3, 41.0], [37.9, 44.5],
  [34.6, 48.4], [32.6, 50.0], [28.1, 51.8], [25.7, 52.1], [-41.9, 48.6], [-42.1, 2.2]];
/* heights: no official height or floor-to-floor height was found (research 3.3): a typical 3.3 m a floor over a lobby of
   about 7 m (the developer), every height labelled an illustration */
const FH = 3.3;
const LOBBY_H = 7.0;
const Y0 = PLOT.h + LOBBY_H + 0.4;   // floor 1's level; the lobby building's roof (the pool deck) is at PLOT.h + LOBBY_H
const FLOORS = 50;                   // residential floors 1-50 (above them the technical floors 51-52)
const PH_FROM = 48;                  // penthouse floors 48-50
const TECH_H = 4.4;                  // each technical floor (illustration)
/* the two towers' footprints, the city's building layer (GIS 513): north oid 44499 (1,082 m²), south oid 42941 (918 m²),
   corners from the research's latitude and longitude, in the stage frame; both in the east half, 28 m apart */
const TOWERS = [
  { id: 'N', k: 1, poly: [[1.13, -45.65], [31.64, -45.96], [31.46, -10.86], [-0.11, -11.01]] },
  { id: 'S', k: 2, poly: [[1.55, 17.28], [33.94, 17.11], [32.78, 46.12], [1.48, 45.9]] },
];
for (const T of TOWERS) {
  T.cx = T.poly.reduce((s, p) => s + p[0], 0) / 4;
  T.cz = T.poly.reduce((s, p) => s + p[1], 0) / 4;
  T.floors = FLOORS;
  T.roof = Y0 + FLOORS * FH;            // the roof of floor 50
  T.top = T.roof + 2 * TECH_H + 3.4;    // the technical floors and the crown's screen
}
const TOWER_BY = { N: TOWERS[0], S: TOWERS[1] };
const MID = { x: (TOWERS[0].cx + TOWERS[1].cx) / 2, z: (TOWERS[0].cz + TOWERS[1].cz) / 2 };
const TOP = Math.max(TOWERS[0].top, TOWERS[1].top);
/* the lobby building between the towers (the developer: the main lobby joins both towers; the pool on its roof); the gap
   is the towers' own 28 m. Its outline is not public: the towers' width, as an illustration */
const LOBBY = [[2.2, -11.0], [31.0, -10.9], [31.6, 17.1], [2.2, 17.2]];
const DECK_Y = PLOT.h + LOBBY_H;
const POOL = { cx: 8.6, cz: 3.0, w: 8.0, d: 21.0 };            // the infinity pool along the deck's west edge (illustration)
const KIDPOOL = { cx: 16.4, cz: -6.2, w: 4.6, d: 3.6 };       // the toddler pool (the developer; illustration of its place)
/* the west half (licensing decision 21.9.2025: "3 מבני מסחר, פיתוח שטח וחצר שקועה"): their places are not public; these
   stand inside the west half as an illustration, and the caption says so */
const RETAIL = [
  { id: 'w', name: 'מסחר מערבי', poly: [[-40.6, -33.0], [-31.0, -33.0], [-31.0, 31.0], [-40.2, 31.0]], floors: 4, roof: true },
  { id: 'n', name: 'מסחר צפוני', poly: [[-28.4, -47.0], [-5.0, -47.2], [-5.0, -30.6], [-28.4, -30.6]], floors: 3 },
  { id: 's', name: 'מסחר דרומי', poly: [[-28.4, 30.0], [-5.0, 30.0], [-5.0, 47.4], [-28.4, 47.0]], floors: 3 },
];
const RETAIL_FH = 4.6;
const COURT = { x0: -27.0, x1: -6.4, z0: -24.0, z1: 24.0, floor: -4.6 };   // the sunken courtyard
const EYE_M = 1.6;
const RING_OFF = 3.8;          // the floor ring: this far outside the glass line (clears the deepest balcony)
function floorLevel(n) { return Y0 + (n - 1) * FH; }
function floorEyeHeight(n) { return Math.round((floorLevel(n) + EYE_M) * 10) / 10; }
/* FloorSlice v87 (28.9.2026): floor n of a tower ('N' | 'S') as a plan, north up, in metres from that tower's centre
   (x east, y north), from the very numbers the towers are built from: the footprint with eased corners, the balconies
   (deep around the corners, a sun balcony in the middle of the west and east faces, a slab edge elsewhere), the penthouse
   floors 48-50 set back 2.2 m with deeper terraces; a core drawn along the grid. The core and any division into
   apartments are illustrations; the plan says so. */
function floorPlan(n, tower, offset) {
  const f = Math.round(Number(n));
  const TW = TOWER_BY[String(tower || 'N').toUpperCase()];
  if (!TW || !(f >= 1 && f <= FLOORS)) return null;
  const ph = f >= PH_FROM;
  const loop = resampleLoop(easeCorners(TW.poly, 1.4, 5), 136, 4);
  // the setback line: the model offsets the eased loop by 2.2 m, more than the corners' 1.4 m radius, which folds tiny spikes
  // into the corners (hidden in 3D, visible in a plan); here the corners are eased wider first, so the line stays clean
  const lp = ph ? offsetLoop(resampleLoop(easeCorners(TW.poly, 4.1, 5), 136, 4), -2.2) : loop;
  const xs = TW.poly.map((p) => p[0]).slice().sort((a, b) => a - b);
  const wMid = { x: (xs[0] + xs[1]) / 2, z: TW.cz }, eMid = { x: (xs[2] + xs[3]) / 2, z: TW.cz };
  const D = loop.pts.map((p) => {
    let dc = 1e9;
    for (const c of TW.poly) dc = Math.min(dc, Math.hypot(p.x - c[0], p.z - c[1]));
    const corner = 1 - smooth(5.8, 8.6, dc);
    const onWE = Math.abs(p.nx) > 0.85;
    const dm = onWE ? Math.min(Math.hypot(p.x - wMid.x, p.z - wMid.z), Math.hypot(p.x - eMid.x, p.z - eMid.z)) : 1e9;
    const mid = 1 - smooth(4.2, 5.6, dm);
    return 0.42 + 1.95 * Math.max(corner, mid * 0.82) + (ph ? 2.2 : 0);
  });
  const cg = Math.cos(GRID_ANGLE), sg = Math.sin(GRID_ANGLE); // site.rotation.y = GRID_ANGLE
  const r2 = (v) => Math.round(v * 100) / 100;
  const toPlan = (x, z) => {
    const dx = x - TW.cx, dz = z - TW.cz;
    const wx = dx * cg + dz * sg, wz = -dx * sg + dz * cg;
    const b = (Math.atan2(wx, -wz) / DEG + (Number(offset) || 0)) * DEG, r = Math.hypot(wx, wz);
    return [r2(r * Math.sin(b)), r2(r * Math.cos(b))];
  };
  const glass = lp.pts.map((p) => toPlan(p.x, p.z));
  const outer = lp.pts.map((p, i) => toPlan(p.x + p.nx * D[i], p.z + p.nz * D[i]));
  const core = [[-6, -4.5], [6, -4.5], [6, 4.5], [-6, 4.5]].map(([x, z]) => toPlan(TW.cx + x, TW.cz + z));
  return { floor: f, floors: FLOORS, tower: TW.id, name: (TEXT.towers || {})[TW.id] || '', penthouse: ph, heightM: floorEyeHeight(f), glass, outer, core };
}
function normDeg(b) { return ((b % 360) + 360) % 360; }

let cssInjected = false;
function ensureCss() {
  if (cssInjected || document.querySelector('link[data-dus-css]')) { cssInjected = true; return; }
  const l = document.createElement('link');
  l.rel = 'stylesheet';
  l.href = new URL('./stage.css', import.meta.url).href + (new URL(import.meta.url).search || '');
  l.setAttribute('data-dus-css', '');
  document.head.appendChild(l);
  cssInjected = true;
}
function ensureFonts() {
  const has = [...document.querySelectorAll('link[href*="fonts.googleapis.com"]')].some((l) => /Heebo/.test(l.href) && /Frank\+Ruhl/.test(l.href));
  if (has || document.querySelector('link[data-dus-fonts]')) return;
  const l = document.createElement('link');
  l.rel = 'stylesheet';
  l.href = 'https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700&family=Heebo:wght@400;500;700&family=Frank+Ruhl+Libre:wght@500;700&family=Noto+Serif+Hebrew:wght@500;600&display=swap';
  l.setAttribute('data-dus-fonts', '');
  document.head.appendChild(l);
}

/* returns { ok, fast }: WebGL2 available, and not a software rasteriser */
function probeWebGL2() {
  const out = { ok: false, fast: false };
  try {
    const c = document.createElement('canvas');
    const gl = c.getContext('webgl2', { failIfMajorPerformanceCaveat: false });
    if (!gl) return out;
    out.ok = true;
    let name = '';
    const dbg = gl.getExtension('WEBGL_debug_renderer_info');
    try { name = String(gl.getParameter(dbg ? dbg.UNMASKED_RENDERER_WEBGL : gl.RENDERER) || ''); } catch (e) { /* ignore */ }
    const software = /swiftshader|llvmpipe|softpipe|software|basic render/i.test(name);
    const ext = gl.getExtension('WEBGL_lose_context');
    if (ext) ext.loseContext();
    if (software) return out;
    const c2 = document.createElement('canvas');
    const gl2 = c2.getContext('webgl2', { failIfMajorPerformanceCaveat: true });
    out.fast = !!gl2;
    if (gl2) { const e2 = gl2.getExtension('WEBGL_lose_context'); if (e2) e2.loseContext(); }
  } catch (e) { /* keep defaults */ }
  return out;
}

function staticNorth(offset) {
  const a = -offset * DEG;
  return { bearingOffset: offset, north: { x: +Math.sin(a).toFixed(4), z: +(-Math.cos(a)).toFixed(4) }, cameraBearing: null, seaBearing: null };
}

function el(tag, cls, parent, attrs) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (attrs) for (const k in attrs) e.setAttribute(k, attrs[k]);
  if (parent) parent.appendChild(e);
  return e;
}

/* ------------------------------------------------------------------------------------------ */
/* Public API                                                                                  */
/* ------------------------------------------------------------------------------------------ */

export function mountDuoStage(container, options = {}) {
  if (!container) throw new Error('mountDuoStage: a container element is required');
  const opts = { ...DEFAULTS, ...options };
  const T = { ...TEXT, ...(options.text || {}) };
  if (opts.injectCss) ensureCss();
  if (opts.injectFonts) ensureFonts();
  // the page's "inside the apartment" action needs interior pictures; DUO has none yet: that action is left out, so no
  // button on the card does nothing (the other actions stay as the page gives them)
  if (Array.isArray(opts.actions) && !document.querySelector('[data-nlps-tour]')) opts.actions = opts.actions.filter((a) => a.id !== 'inside');

  const mq = (q) => (window.matchMedia ? window.matchMedia(q).matches : false);
  const reduced = mq('(prefers-reduced-motion: reduce)');
  const coarse = mq('(pointer: coarse)');
  const smallScreen = Math.min(screen.width, screen.height) < 600;
  const phone = coarse && smallScreen;

  /* DOM (Rainbow's classes, rbs-; DUO's own additions are dus-) */
  const root = el('div', 'rbs dus', null, { dir: 'rtl', lang: 'he' });
  if (container.clientHeight < 40) root.classList.add('rbs--auto');
  const ssr = container.querySelector('img.nlps-ssr-poster');
  const poster = ssr || el('img', 'rbs-poster', root, { alt: T.aria, decoding: 'async', fetchpriority: 'high' });
  if (ssr) { ssr.classList.add('rbs-poster'); root.appendChild(ssr); }
  poster.addEventListener('error', () => { poster.style.visibility = 'hidden'; }, { once: true });
  if (!ssr) poster.src = opts.poster || new URL('./poster.jpg', import.meta.url).href;
  const canvasWrap = el('div', 'rbs-canvas', root);
  const leader = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  leader.setAttribute('class', 'rbs-leader');
  leader.setAttribute('aria-hidden', 'true');
  leader.innerHTML = '<line x1="0" y1="0" x2="0" y2="0" visibility="hidden"/><circle cx="0" cy="0" r="4.5" visibility="hidden"/>';
  root.appendChild(leader);
  const ui = el('div', 'rbs-ui', root);
  // the streets and the towers' names over the model (never buttons): drawn first, so every control stays above them
  const marks = el('div', 'dus-marks', ui, { 'aria-hidden': 'true' });
  const hint = el('div', 'rbs-hint', ui);
  hint.textContent = T.hint;
  if (!opts.hint) hint.style.display = 'none';
  const presetsEl = el('div', 'rbs-presets', ui, { role: 'radiogroup', 'aria-label': T.presets });
  const presetBtns = {};
  for (const key of ['sunset', 'noon']) {
    const b = el('button', '', presetsEl, { type: 'button', role: 'radio', 'aria-checked': 'false', 'data-preset': key });
    b.textContent = T[key];
    presetBtns[key] = b;
  }
  const caption = el('p', 'rbs-caption', ui);
  caption.textContent = T.caption + ' ' + T.geo;
  const label = el('div', 'rbs-label', ui, { 'aria-live': 'polite' });
  const labelKick = el('p', 'dus-label-kick', label);
  const labelTop = el('div', 'rbs-label-top', label);
  const labelTitle = el('p', 'rbs-label-title', labelTop);
  const labelClose = el('button', 'rbs-label-close', labelTop, { type: 'button', 'aria-label': T.close });
  labelClose.textContent = '×';
  const labelLine = el('p', 'rbs-label-line', label);
  const labelFacing = el('p', 'rbs-label-facing', label);
  const labelMore = el('p', 'rbs-label-more', label);
  labelMore.hidden = true;
  const actBtns = {};
  if (Array.isArray(opts.actions) && opts.actions.length) {
    const acts = el('div', 'rbs-label-acts', label);
    for (const a of opts.actions) {
      const b = el('button', 'rbs-act rbs-act--' + (a.kind === 'go' ? 'go' : 'sec'), acts, { type: 'button', 'data-act': String(a.id) });
      b.textContent = String(a.label);
      actBtns[a.id] = b;
    }
  }
  const labelCta = el('button', 'rbs-label-cta', label, { type: 'button' });
  labelCta.textContent = T.cta;
  const facingChip = el('div', 'rbs-facing', ui, { 'aria-hidden': 'true' });
  /* the quarter (design system QuarterPins): a pin per project and place, and one card */
  const Q = opts.quarter && (Array.isArray(opts.quarter.projects) || Array.isArray(opts.quarter.places)) ? opts.quarter : null;
  const qpins = [];
  let qcard = null;
  if (Q) {
    const pinsEl = el('div', 'rbs-qpins', ui);
    for (const it of [...(Q.projects || []), ...(Q.places || [])]) {
      const isP = it.kind === 'project';
      const b = el('button', 'rbs-qpin ' + (isP ? 'rbs-qpin--project' : 'rbs-qpin--place rbs-qpin--' + it.kind), pinsEl, { type: 'button', 'aria-label': it.name });
      if (!isP) el('i', 'rbs-qdot', b);
      else if (it.phase) el('i', 'rbs-qdot rbs-qdot--' + it.phase, b);
      b.append(it.pin || it.name);
      const h = isP ? Math.max(12, (Number(it.floors) || 10) * 3.3 + 4) : (it.kind === 'civic' ? 84 : 10);
      qpins.push({ el: b, it, x: Number(it.x) || 0, y: h + (isP ? 7 : 3), z: Number(it.z) || 0, w: 0 });
    }
    const heroEl = el('div', 'rbs-qpin rbs-qpin--hero', pinsEl, { 'aria-hidden': 'true' });
    heroEl.textContent = T.heroName;
    const G = GRID_ANGLE;
    qpins.push({ el: heroEl, it: { kind: 'hero', name: T.heroName }, hero: true,
      x: MID.x * Math.cos(G) + MID.z * Math.sin(G), y: TOP + 10, z: -MID.x * Math.sin(G) + MID.z * Math.cos(G), w: 0 });
    qcard = el('div', 'rbs-qcard', ui, { role: 'dialog', 'aria-live': 'polite' });
  }
  /* the project's facilities (design system FacilityHotspots v72): a pin per facility on the model, each with a card that
     names its source; shown by the legend's "מתקנים בפרויקט" chip */
  const fpins = [];
  if (Array.isArray(opts.facilities) && opts.facilities.length) {
    const fEl = el('div', 'rbs-qpins rbs-fpins', ui);
    for (const it of opts.facilities) {
      for (const an of (Array.isArray(it.anchors) ? it.anchors : [])) {
        const b = el('button', 'rbs-qpin rbs-qpin--facility', fEl, { type: 'button', 'aria-label': it.name });
        el('i', 'rbs-fic rbs-fic--' + String(it.icon || 'dot'), b, { 'aria-hidden': 'true' });
        b.append(it.pin || it.name);
        b.style.visibility = 'hidden';
        fpins.push({ el: b, it, an: String(an), fac: true, off: true, w: 0 });
      }
    }
    if (!qcard) qcard = el('div', 'rbs-qcard', ui, { role: 'dialog', 'aria-live': 'polite' });
  }
  const openBtn = el('button', 'rbs-open', ui, { type: 'button' });
  openBtn.textContent = T.open3d;
  container.appendChild(root);
  const layoutRO = new ResizeObserver(() => root.classList.toggle('rbs--narrow', root.clientWidth < 600));
  layoutRO.observe(root);
  root.classList.toggle('rbs--narrow', root.clientWidth < 600);

  let engine = null;
  let disposed = false;
  let currentPreset = PRESETS[opts.preset] ? opts.preset : 'sunset';
  const setPresetButtons = (k) => {
    for (const key in presetBtns) presetBtns[key].setAttribute('aria-checked', key === k ? 'true' : 'false');
  };
  setPresetButtons(currentPreset);

  const probe = probeWebGL2();
  const hasGL = probe.ok;
  const fastGL = probe.fast;
  const weak = ((navigator.hardwareConcurrency || 8) <= 4 && smallScreen) || !fastGL;

  const readyCallbacks = [];
  let readyResolved = false;
  const ready = new Promise((res) => readyCallbacks.push(res));
  const markReady = () => { if (!readyResolved) { readyResolved = true; readyCallbacks.forEach((f) => f()); } };

  // the real city around the building (design system StageCity): its file sits next to this module
  let cityData;
  function loadCity() {
    if (cityData !== undefined || opts.city === false) return Promise.resolve(cityData || null);
    return fetch(new URL('./city.json', import.meta.url).href + (new URL(import.meta.url).search || ''))
      .then((r) => (r.ok ? r.json() : null))
      .catch(() => null)
      .then((d) => { cityData = d && (Array.isArray(d.b) || Array.isArray(d.lots)) ? d : null; return cityData; });
  }
  async function start3D() {
    root.classList.remove('rbs--fallback');
    try {
      if (!THREE) {
        const [three, oc] = await Promise.all([import('three'), import('three/addons/controls/OrbitControls.js'), loadCity()]);
        THREE = three;
        OrbitControls = oc.OrbitControls;
      } else await loadCity();
      opts.cityData = cityData || null;
      if (disposed) return;
      engine = createEngine({
        root, ui, marks, canvasWrap, label, labelKick, labelTitle, labelLine, labelFacing, labelMore, actBtns, labelCta, labelClose, leader, hint, facingChip, qpins, qcard, fpins,
        opts, T, reduced, phone, coarse, preset: currentPreset,
        onReady: markReady,
        onContextLost: () => { root.classList.remove('rbs--live', 'rbs--settled'); },
      });
    } catch (err) {
      console.warn('[duo-stage] 3D unavailable, keeping the poster.', err);
      root.classList.add('rbs--fallback', 'rbs--nogl');
    }
  }

  const onPresetClick = (e) => {
    const b = e.target.closest('button[data-preset]');
    if (!b) return;
    handle.setPreset(b.getAttribute('data-preset'));
  };
  presetsEl.addEventListener('click', onPresetClick);
  const onPresetKey = (e) => {
    if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
    e.preventDefault();
    const next = currentPreset === 'sunset' ? 'noon' : 'sunset';
    handle.setPreset(next);
    presetBtns[next].focus();
  };
  presetsEl.addEventListener('keydown', onPresetKey);
  const onOpen = () => { openBtn.disabled = true; start3D(); };
  openBtn.addEventListener('click', onOpen);

  if (!hasGL) {
    root.classList.add('rbs--fallback', 'rbs--nogl');
  } else if (weak && !opts.force3D) {
    root.classList.add('rbs--fallback');
  } else {
    start3D();
  }

  const handle = {
    ready,
    get preset() { return currentPreset; },
    setPreset(k) {
      if (!PRESETS[k]) return;
      currentPreset = k;
      setPresetButtons(k);
      if (engine) engine.setPreset(k);
    },
    /* pick a floor (the camera glides to it) on a tower ('N' | 'S'; default: the tower picked last, else opts.tower) */
    selectFloor(n, tower) { if (engine) engine.selectFloor(n, tower); },
    clearFloor() { if (engine) engine.clearFloor(); },
    setFacing(bearing) { return engine ? engine.setFacing(bearing) : null; },
    clearFacing() { if (engine) engine.clearFacing(); },
    /* an example apartment by its id: "N-25-w" (tower, floor, side), or "25-w" on the current tower */
    selectUnit(id, source) { return engine ? engine.selectUnit(id, source) : null; },
    openQuarter(name) { return engine ? engine.openQuarter(name) : false; },
    /* the legend: 'facilities' | 'today' | 'building' | 'selling' | 'permit' shows that group alone; null shows all */
    focusPhase(ph) { return engine ? engine.focusPhase(ph) : null; },
    lookToward(name) { return engine ? engine.lookToward(name) : false; },
    /* { tower, floor, heightM, bearing, unit } of the current pick, or null */
    getSelection() { return engine ? engine.getSelection() : null; },
    floorHeight(n) { const f = Math.round(Number(n)); return f >= 1 && f <= FLOORS ? floorEyeHeight(f) : null; },
    /* FloorSlice v87: floor n of a tower as a plan (see floorPlan), for assets/project-stage/slice.js */
    floorPlan(n, tower) { return floorPlan(n, tower, Number(opts.bearingOffset) || 0); },
    getNorth() { return engine ? engine.getNorth() : staticNorth(Number(opts.bearingOffset) || 0); },
    setAutoOrbit(on) { if (engine) engine.setAutoOrbit(on); },
    stats() { return engine ? engine.stats() : null; },
    /* the shared viewing room (inc/together.php, design system TogetherRoom v77, being added to Rainbow's stage on
       28.9.2026): the same calls, so a room can drive DUO too. The camera as data ({ target: [x, y, z], r, phi, theta }),
       a glide to it; a screen point as a scene point ({ x, y, z, floor, tower, on }) and back ({ x, y, behind }). */
    getView() { return engine ? engine.getView() : null; },
    setView(v, dur) { return engine ? engine.setView(v, dur) : false; },
    home(dur) { return engine ? engine.home(dur) : false; },
    pickPoint(clientX, clientY) { return engine ? engine.pickPoint(clientX, clientY) : null; },
    project(point) { return engine ? engine.project(point) : null; },
    get phase() { return engine ? engine.phase() : 'poster'; },
    _engine() { return engine; },
    dispose() {
      if (disposed) return;
      disposed = true;
      layoutRO.disconnect();
      presetsEl.removeEventListener('click', onPresetClick);
      presetsEl.removeEventListener('keydown', onPresetKey);
      openBtn.removeEventListener('click', onOpen);
      if (engine) engine.dispose();
      engine = null;
      root.remove();
    },
  };
  return handle;
}

/* ------------------------------------------------------------------------------------------ */
/* Engine                                                                                      */
/* ------------------------------------------------------------------------------------------ */

function createEngine(ctx) {
  const { root, marks, canvasWrap, label, labelKick, labelTitle, labelLine, labelFacing, labelMore, actBtns, labelCta, labelClose, leader, hint, facingChip, opts, T: TX, reduced, phone } = ctx;
  const T = TX;
  const qpins = ctx.qpins || [], qcard = ctx.qcard || null, fpins = ctx.fpins || [];
  let facMode = false; // the legend's "מתקנים בפרויקט" chip: the facility pins on, the quarter's pins off
  const leaderLine = leader.querySelector('line');
  const leaderDot = leader.querySelector('circle');

  const listeners = [];
  const on = (target, type, fn, o) => { target.addEventListener(type, fn, o); listeners.push([target, type, fn, o]); };

  /* renderer */
  const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance', alpha: false, stencil: false, preserveDrawingBuffer: !!opts.debug });
  const dprCap = phone ? 1.5 : 1.75;
  let dpr = Math.min(window.devicePixelRatio || 1, dprCap);
  renderer.setPixelRatio(dpr);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = opts.toneMapping === 'agx' ? THREE.AgXToneMapping : THREE.ACESFilmicToneMapping;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.shadowMap.autoUpdate = false;
  renderer.info.autoReset = false;
  const canvas = renderer.domElement;
  canvas.setAttribute('role', 'img');
  canvas.setAttribute('aria-label', T.aria);
  canvas.tabIndex = 0;
  canvasWrap.appendChild(canvas);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(30, 1.6, 2, 16000);
  const site = new THREE.Group();
  site.rotation.y = GRID_ANGLE;
  scene.add(site);

  /* shared uniforms */
  const U = {
    uTime: { value: 0 },
    uSkyZenith: { value: new THREE.Color() },
    uSkyHorizon: { value: new THREE.Color() },
    uSkyWarm: { value: new THREE.Color() },
    uSkyGlowCol: { value: new THREE.Color() },
    uSkyRose: { value: new THREE.Color() },
    uRoseAmt: { value: 0 },
    uSunDir: { value: new THREE.Vector3(0, 1, 0) },
    uSkyGlow: { value: 1 },
    uWarmPow: { value: 2 },
    uFogDensity: { value: 1 / 2400 },
    uHiFloor: { value: -100 },
    uHiTower: { value: 0 },        // 1 = the north tower, 2 = the south tower
    uHiColor: { value: new THREE.Color('#2F6F86') },
    uFloorY0: { value: Y0 },
    uFloorH: { value: FH },
    uCoast: { value: new THREE.Vector4() },
    uSeaShallow: { value: new THREE.Color() },
    uGhostFade: { value: 0.14 },
    uDim: { value: 0 },
    uHiGlow: { value: 0.22 },
    uSunTint: { value: new THREE.Color() },
    uSparkle: { value: 1 },
  };

  /* lights */
  const sun = new THREE.DirectionalLight(0xffffff, 3);
  sun.castShadow = true;
  const bigShadow = !phone && renderer.capabilities.maxTextureSize >= 8192;
  sun.shadow.mapSize.set(bigShadow ? 4096 : 2048, bigShadow ? 4096 : 2048);
  sun.shadow.bias = -0.00015;
  sun.shadow.normalBias = bigShadow ? 0.06 : 0.1;
  scene.add(sun, sun.target);
  const hemi = new THREE.HemisphereLight(0xffffff, 0xffffff, 0.4);
  scene.add(hemi);

  /* sky dome + environment */
  const skyUniforms = {
    uSkyZenith: U.uSkyZenith, uSkyHorizon: U.uSkyHorizon, uSkyWarm: U.uSkyWarm, uSkyGlowCol: U.uSkyGlowCol,
    uSkyRose: U.uSkyRose, uRoseAmt: U.uRoseAmt,
    uSunDir: U.uSunDir, uSkyGlow: U.uSkyGlow, uWarmPow: U.uWarmPow,
  };
  const skyMat = makeSkyMaterial(skyUniforms, false, null);
  const sky = new THREE.Mesh(new THREE.SphereGeometry(100, 32, 16), skyMat);
  sky.frustumCulled = false;
  sky.renderOrder = 1000;
  scene.add(sky);
  const envGround = { value: new THREE.Color() };
  const envZen = { value: new THREE.Color() };
  const envHor = { value: new THREE.Color() };
  const envScene = new THREE.Scene();
  envScene.add(new THREE.Mesh(new THREE.SphereGeometry(10, 32, 16), makeSkyMaterial(skyUniforms, 'fill', envGround, envZen, envHor)));
  const envSkyScene = new THREE.Scene();
  envSkyScene.add(new THREE.Mesh(new THREE.SphereGeometry(10, 32, 16), makeSkyMaterial(skyUniforms, 'sky', envGround, envZen, envHor)));
  const pmrem = new THREE.PMREMGenerator(renderer);
  let envRT = null, envSkyRT = null;

  /* materials and the world */
  const M = makeMaterials(U);
  const world = buildWorld(site, M, U, opts.quarter, opts.cityData);
  scene.updateMatrixWorld(true);

  // the coast line in world space for the sea shader (a point on the waterline + the normal towards the sea)
  {
    const cst = world.coast;
    const p = site.localToWorld(new THREE.Vector3(cst.x0, 0, 0));
    const n = new THREE.Vector3(-1, 0, cst.k).normalize().applyQuaternion(site.quaternion);
    U.uCoast.value.set(p.x, p.z, n.x, n.z);
  }

  /* camera rig */
  const controls = new OrbitControls(camera, canvas);
  controls.enableDamping = true;
  controls.dampingFactor = 0.07;
  controls.enablePan = false;
  controls.rotateSpeed = 0.55;
  controls.zoomSpeed = 0.8;
  controls.minDistance = 140;
  controls.maxDistance = 1400;
  controls.minPolarAngle = 12 * DEG;
  controls.maxPolarAngle = 84 * DEG;
  controls.autoRotate = false;
  controls.autoRotateSpeed = 0;
  controls.touches.TWO = THREE.TOUCH.DOLLY_ROTATE;
  controls.enabled = false;
  canvas.style.touchAction = 'pan-y';

  const tmpV = new THREE.Vector3();
  const tmpV2 = new THREE.Vector3();

  function localToWorld(x, y, z, out = new THREE.Vector3()) { return site.localToWorld(out.set(x, y, z)); }
  function viewFromBearing(bearingLocalDeg, elevDeg, dist, target, out) {
    // bearing in the site grid (0 = grid north, clockwise), converted to a world offset
    const b = bearingLocalDeg * DEG, e = elevDeg * DEG;
    const lx = Math.sin(b) * Math.cos(e), lz = -Math.cos(b) * Math.cos(e), ly = Math.sin(e);
    const d = new THREE.Vector3(lx, ly, lz).applyQuaternion(site.quaternion);
    return out.copy(target).addScaledVector(d, dist);
  }

  const heroTarget = new THREE.Vector3();
  const introTarget = localToWorld(MID.x - 6, 40, MID.z);
  controls.target.copy(heroTarget);
  function heroDistance() {
    const vf = camera.fov * DEG;
    const hf = 2 * Math.atan(Math.tan(vf / 2) * camera.aspect);
    const halfW = camera.aspect < 1 ? 66 : 96;
    return (HERO.dist || 1) * Math.max((camera.aspect < 1 ? 124 : 112) / Math.tan(vf / 2), halfW / Math.tan(hf / 2));
  }
  function heroTargetFor(aspect, out) {
    // portrait stages centre on the towers themselves; landscape keeps the west half's retail and the courtyard in frame
    const k = Math.min(1, Math.max(0, (aspect - 0.6) / 0.6));
    return localToWorld(MID.x - 2 - 10 * k, 86 - 6 * k, MID.z + 2, out);
  }
  // from the south-west (Ibn Gabirol at Arlozorov), the low sun behind the camera: both towers side by side, lit warm
  const HERO = { bearing: 250, elev: 18, dist: 1.1 };
  const INTRO = { bearing: 214, elev: 40, distMul: 2.3 };
  heroTargetFor(1.6, heroTarget);

  /* state */
  let phase = 'intro';
  let introT = 0;
  let introHold = 0.35;
  const INTRO_DUR = 3.6;
  let lastInteract = -1e9;
  let orbitRamp = 0;
  let autoOrbit = opts.autoOrbit && !reduced;
  let running = true;
  let visible = true;
  let rafId = 0;
  let lastT = performance.now();
  let clock = 0;
  let needsRender = true;
  let firstFrameDone = false;
  let presetKey = ctx.preset;
  let trans = null;
  let aoMode = opts.ao;
  let aoOn = false;
  let aoBlocked = false;
  let post = null;
  let aoLoading = false;
  let aoProbe = 0, aoFade = 0, aoFadeDir = 0;
  const perf = { times: [], fps: 0, goodFor: 0, badFor: 0, dprLowFor: 0 };
  let selected = null;       // { tower, floor, pinned }
  let lastTower = TOWER_BY[opts.tower] || TOWERS[0];
  let glide = null;
  let hover = null;          // { tower, floor }
  let labelSide = 1;
  const labelBox = { w: 0, h: 0 };
  let stageW = 1, stageH = 1;
  let disposedE = false;

  /* presets */
  const cur = presetState(PRESETS[presetKey]);
  applyPresetState(cur);
  regenEnv();

  function presetState(p) {
    const c = (h) => new THREE.Color(h);
    return {
      sunAz: p.sunAz, sunEl: p.sunEl, sunColor: c(p.sunColor), sunI: p.sunI,
      hemiSky: c(p.hemiSky), hemiGround: c(p.hemiGround), hemiI: p.hemiI,
      envWhite: p.envWhite, envGlass: p.envGlass,
      zenith: c(p.zenith).multiplyScalar(p.skyGain), horizon: c(p.horizon).multiplyScalar(p.skyGain),
      envZenith: c(p.envZenith), envHorizon: c(p.envHorizon),
      rose: c(p.rose).multiplyScalar(p.skyGain), roseAmt: p.roseAmt,
      warm: c(p.warm).multiplyScalar(p.skyGain), glowCol: c(p.glowCol), glow: p.glow, warmPow: p.warmPow,
      groundEnv: c(p.groundEnv), sea: c(p.sea), seaShallow: c(p.seaShallow), exposure: p.exposure, fog: p.fog,
      sparkle: p.sparkle,
    };
  }
  function lerpState(a, b, t) {
    const o = {};
    for (const k in a) {
      if (a[k] && a[k].isColor) o[k] = a[k].clone().lerp(b[k], t);
      else o[k] = a[k] + (b[k] - a[k]) * t;
    }
    return o;
  }
  function applyPresetState(s) {
    const az = s.sunAz * DEG, elv = s.sunEl * DEG;
    const dir = new THREE.Vector3(Math.sin(az) * Math.cos(elv), Math.sin(elv), -Math.cos(az) * Math.cos(elv)).normalize();
    U.uSunDir.value.copy(dir);
    const focus = localToWorld(MID.x, 0, MID.z, tmpV);
    sun.target.position.copy(focus);
    sun.position.copy(focus).addScaledVector(dir, 1500);
    sun.color.copy(s.sunColor);
    sun.intensity = s.sunI;
    hemi.color.copy(s.hemiSky);
    hemi.groundColor.copy(s.hemiGround);
    hemi.intensity = s.hemiI;
    U.uSkyZenith.value.copy(s.zenith);
    U.uSkyHorizon.value.copy(s.horizon);
    U.uSkyWarm.value.copy(s.warm);
    U.uSkyGlowCol.value.copy(s.glowCol);
    U.uSkyRose.value.copy(s.rose);
    U.uRoseAmt.value = s.roseAmt;
    U.uSkyGlow.value = s.glow;
    U.uWarmPow.value = s.warmPow;
    U.uFogDensity.value = s.fog;
    U.uSeaShallow.value.copy(s.seaShallow);
    U.uSunTint.value.copy(s.sunColor).multiplyScalar(s.sunI * 0.9);
    U.uSparkle.value = s.sparkle;
    envGround.value.copy(s.groundEnv);
    envZen.value.copy(s.envZenith);
    envHor.value.copy(s.envHorizon);
    M.sea.color.copy(s.sea);
    renderer.toneMappingExposure = s.exposure;
    for (const m of M.envWhiteList) m.envMapIntensity = s.envWhite;
    for (const m of M.envGlassList) m.envMapIntensity = s.envGlass;
    fitShadowCamera(dir);
    renderer.shadowMap.needsUpdate = true;
    needsRender = true;
  }
  function regenEnv() {
    const rt = pmrem.fromScene(envScene, 0, 0.1, 100);
    const rts = pmrem.fromScene(envSkyScene, 0, 0.1, 100);
    for (const m of M.all) {
      if (m.isMeshStandardMaterial) {
        m.envMap = M.envGlassList.includes(m) ? rts.texture : rt.texture;
        if (!m.userData.envSet) { m.needsUpdate = true; m.userData.envSet = true; }
      }
    }
    if (envRT) envRT.dispose();
    if (envSkyRT) envSkyRT.dispose();
    envRT = rt; envSkyRT = rts;
    needsRender = true;
  }
  function fitShadowCamera(dir) {
    // light-space bounds of the region that carries shadows: the site, the near city and both towers' tops
    const cam = sun.shadow.camera;
    sun.updateMatrixWorld();
    const view = new THREE.Matrix4().lookAt(sun.position, sun.target.position, new THREE.Vector3(0, 1, 0)).setPosition(sun.position);
    const inv = view.clone().invert();
    const pts = [];
    const R = 250;
    for (let i = 0; i < 16; i++) {
      const a = (i / 16) * Math.PI * 2;
      pts.push(localToWorld(MID.x + Math.cos(a) * R, 0, MID.z + Math.sin(a) * R));
      pts.push(localToWorld(MID.x + Math.cos(a) * R, 40, MID.z + Math.sin(a) * R));
    }
    for (const TW of TOWERS) pts.push(localToWorld(TW.cx, TW.top + 6, TW.cz));
    let minX = 1e9, maxX = -1e9, minY = 1e9, maxY = -1e9, minZ = 1e9, maxZ = -1e9;
    for (const p of pts) {
      p.applyMatrix4(inv);
      minX = Math.min(minX, p.x); maxX = Math.max(maxX, p.x);
      minY = Math.min(minY, p.y); maxY = Math.max(maxY, p.y);
      minZ = Math.min(minZ, p.z); maxZ = Math.max(maxZ, p.z);
    }
    cam.left = minX - 4; cam.right = maxX + 4; cam.bottom = minY - 4; cam.top = maxY + 4;
    cam.near = Math.max(1, -maxZ - 60); cam.far = -minZ + 700;
    cam.updateProjectionMatrix();
  }

  /* resize */
  function resize() {
    const r = root.getBoundingClientRect();
    stageW = Math.max(1, Math.round(r.width));
    stageH = Math.max(1, Math.round(r.height));
    const aspect = stageW / stageH;
    camera.aspect = aspect;
    camera.fov = aspect < 1 ? Math.min(52, Math.max(30, 2 * Math.atan(Math.tan(11.5 * DEG) / aspect) / DEG)) : 30;
    camera.updateProjectionMatrix();
    heroTargetFor(aspect, heroTarget);
    if (phase === 'orbit' && !glide && !(selected && selected.pinned) && !controls.autoRotate && !facMode && performance.now() - lastInteract > 1500) controls.target.copy(heroTarget);
    renderer.setSize(stageW, stageH, false);
    if (post) post.gtao.setSize(stageW * dpr, stageH * dpr);
    root.classList.toggle('rbs--narrow', stageW < 600);
    labelBox.w = 0;
    leader.setAttribute('viewBox', `0 0 ${stageW} ${stageH}`);
    if (phase !== 'intro') controls.maxDistance = Math.max(1400, heroDistance() * 2.2);
    needsRender = true;
  }
  const ro = new ResizeObserver(resize);
  ro.observe(root);
  resize();

  /* initial camera */
  const hd = heroDistance();
  if (!opts.intro || reduced) {
    phase = 'orbit';
    viewFromBearing(HERO.bearing, HERO.elev, hd, heroTarget, camera.position);
    controls.target.copy(heroTarget);
    controls.enabled = true;
    controls.update();
  } else {
    viewFromBearing(INTRO.bearing, INTRO.elev, hd * INTRO.distMul, introTarget, camera.position);
    camera.lookAt(introTarget);
    root.classList.add('rbs--intro');
  }

  /* interaction */
  const pointer = { x: 0, y: 0, down: false, downX: 0, downY: 0, downT: 0, moved: false, type: 'mouse', inside: false };
  let hoverDirty = false;
  let engagedUntil = 0;
  on(controls, 'start', () => {
    lastInteract = performance.now();
    if (phase === 'intro') endIntro();
    root.classList.add('rbs--grabbing');
  });
  on(controls, 'end', () => { lastInteract = performance.now(); root.classList.remove('rbs--grabbing'); });
  on(controls, 'change', () => { needsRender = true; });

  on(root, 'wheel', (e) => {
    if (opts.wheel !== 'always' && performance.now() > engagedUntil) { e.stopPropagation(); return; }
    engagedUntil = performance.now() + 4000;
    lastInteract = performance.now();
  }, { capture: true, passive: true });
  on(root, 'pointerleave', () => {
    engagedUntil = 0; pointer.inside = false;
    if (!pointer.down) { setHover(null); setPreview(-1); }
  });

  const raycaster = new THREE.Raycaster();
  raycaster.layers.set(1);
  const ndc = new THREE.Vector2();
  function setRay(clientX, clientY) {
    const r = canvas.getBoundingClientRect();
    ndc.set(((clientX - r.left) / r.width) * 2 - 1, -((clientY - r.top) / r.height) * 2 + 1);
    raycaster.setFromCamera(ndc, camera);
  }
  /* the tower and the floor under a screen point (either tower; the nearer one wins) */
  function hitTower(clientX, clientY) {
    setRay(clientX, clientY);
    const hit = raycaster.intersectObjects(world.towerProxies, false)[0];
    if (!hit) return null;
    const TW = hit.object.userData.tower;
    const f = Math.floor((hit.point.y - Y0) / FH) + 1;
    if (f < 1 || f > TW.floors) return null;
    return { tower: TW, floor: f, point: hit.point };
  }
  function emit(name, detail) { window.dispatchEvent(new CustomEvent(name, { detail })); }

  /* the shared viewing room (Rainbow's TogetherRoom calls): a throttled nl:view while the visitor moves the camera
     himself; a camera set from outside or a glide to a picked floor never sends one */
  let camUser = false, camUserAt = 0, viewEmitAt = 0, viewTimer = 0;
  const sendView = () => { viewTimer = 0; if (disposedE) return; viewEmitAt = performance.now(); emit('nl:view', Object.assign(viewNow(), { source: 'user' })); };
  on(controls, 'start', () => { camUser = true; camUserAt = performance.now(); });
  on(controls, 'end', () => { camUser = false; camUserAt = performance.now(); });
  on(controls, 'change', () => {
    if (glide || !(camUser || performance.now() - camUserAt < 900)) return;
    const wait = 100 - (performance.now() - viewEmitAt);
    if (wait <= 0) sendView(); else if (!viewTimer) viewTimer = setTimeout(sendView, wait);
  });
  function viewNow() {
    const cs = camSpherical(), t = controls.target;
    return { mode: 'building', target: [+t.x.toFixed(2), +t.y.toFixed(2), +t.z.toFixed(2)], r: +cs.r.toFixed(2), phi: +cs.phi.toFixed(4), theta: +cs.theta.toFixed(4) };
  }
  function setViewFrom(v, dur) {
    if (!v || !Array.isArray(v.target) || v.target.length !== 3) return false;
    const t = v.target.map(Number), r = Number(v.r), phi = Number(v.phi), theta = Number(v.theta);
    if (!t.every(Number.isFinite) || !(r > 0) || !Number.isFinite(phi) || !Number.isFinite(theta)) return false;
    if (phase === 'intro') endIntro();
    camUser = false; camUserAt = 0;
    lastInteract = performance.now();
    const d = Number(dur);
    glideTo(new THREE.Vector3(t[0], t[1], t[2]), r, phi, theta, Number.isFinite(d) ? Math.max(0, d) : 0.6);
    kick();
    return true;
  }
  const pickPlane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0);
  const pickHit = new THREE.Vector3();
  function pickPoint(clientX, clientY) {
    const rc = canvas.getBoundingClientRect();
    if (!rc.width || clientX < rc.left || clientX > rc.right || clientY < rc.top || clientY > rc.bottom) return null;
    const h = hitTower(clientX, clientY); // sets the ray
    if (h) return { x: +h.point.x.toFixed(2), y: +h.point.y.toFixed(2), z: +h.point.z.toFixed(2), floor: h.floor, tower: h.tower.id, on: 'tower' };
    if (raycaster.ray.intersectPlane(pickPlane, pickHit) && pickHit.distanceTo(camera.position) < 4000) {
      return { x: +pickHit.x.toFixed(2), y: 0, z: +pickHit.z.toFixed(2), floor: null, tower: null, on: 'ground' };
    }
    return null;
  }
  function projectPoint(p) {
    if (!p) return null;
    const x = Number(p.x), y = Number(p.y), z = Number(p.z);
    if (!Number.isFinite(x) || !Number.isFinite(y) || !Number.isFinite(z)) return null;
    const a = projectToStage(tmpV.set(x, y, z));
    const rc = canvas.getBoundingClientRect();
    return { x: rc.left + a.x, y: rc.top + a.y, behind: a.behind };
  }

  /* compass: the scene's north is world -z; bearingOffset aligns it with the real site */
  const offset = Number(opts.bearingOffset) || 0;
  const sceneBearing = (dx, dz) => normDeg(Math.atan2(dx, -dz) / DEG);
  const trueBearing = (sb) => normDeg(sb + offset);
  const round1 = (b) => { const v = Math.round(normDeg(b) * 10) / 10; return v >= 360 ? 0 : v; };
  const dirWord = (b) => T.dirs[Math.round(normDeg(b) / 45) % 8];
  const heightOf = (f) => floorEyeHeight(f);
  const nameOf = (TW) => (T.towers && T.towers[TW.id]) || TW.id;

  /* example apartments (the owner, 25.9.2026): one per side of each tower floor, labelled examples everywhere */
  const UNITS = opts.units && Array.isArray(opts.units.sides) && opts.units.sides.length ? opts.units : null;
  const unitHalf = UNITS ? Math.max(10, Math.min(90, Number(UNITS.half) || 180 / UNITS.sides.length)) : 0;
  function unitFor(b) {
    if (!UNITS) return null;
    let best = null, bd = 1e9;
    for (const s of UNITS.sides) {
      let d = Math.abs(normDeg(b) - normDeg(s.bearing));
      if (d > 180) d = 360 - d;
      if (d < bd) { bd = d; best = s; }
    }
    return bd <= unitHalf + 0.001 ? best : null;
  }

  /* the floor ring of each tower: the footprint grown by RING_OFF with round corners (a Minkowski sum), sampled by arc
     length; every sample carries its facade point, its outward normal, the normal's bearing and the side it belongs to */
  const RING_N = 960;
  for (const TW of TOWERS) {
    const P = TW.poly.slice();
    let ar = 0;
    for (let i = 0; i < P.length; i++) { const a = P[i], b = P[(i + 1) % P.length]; ar += a[0] * b[1] - b[0] * a[1]; }
    const sg = ar > 0 ? 1 : -1;
    const segs = [];
    let total = 0;
    for (let i = 0; i < P.length; i++) {
      const a = P[i], b = P[(i + 1) % P.length], c = P[(i + 2) % P.length];
      let tx = b[0] - a[0], tz = b[1] - a[1];
      const L = Math.hypot(tx, tz); tx /= L; tz /= L;
      const n0 = [sg * tz, -sg * tx];
      let ux = c[0] - b[0], uz = c[1] - b[1];
      const L2 = Math.hypot(ux, uz); ux /= L2; uz /= L2;
      const n1 = [sg * uz, -sg * ux];
      let ang = Math.atan2(n0[0] * n1[1] - n0[1] * n1[0], n0[0] * n1[0] + n0[1] * n1[1]);
      segs.push({ kind: 'edge', a, b, n: n0, len: L });
      segs.push({ kind: 'arc', c: b, n0, ang, len: Math.abs(ang) * RING_OFF });
      total += L + Math.abs(ang) * RING_OFF;
    }
    const ring = [];
    const q = site.quaternion;
    const v = new THREE.Vector3(), w = new THREE.Vector3(), nn = new THREE.Vector3();
    const cW = localToWorld(TW.cx, 0, TW.cz);
    let si = 0, acc = 0;
    for (let i = 0; i < RING_N; i++) {
      const s = (i / RING_N) * total;
      while (si < segs.length - 1 && acc + segs[si].len < s) { acc += segs[si].len; si++; }
      const sgm = segs[si], t = sgm.len > 0 ? (s - acc) / sgm.len : 0;
      let fx, fz, nx, nz;
      if (sgm.kind === 'edge') {
        fx = sgm.a[0] + (sgm.b[0] - sgm.a[0]) * t; fz = sgm.a[1] + (sgm.b[1] - sgm.a[1]) * t;
        nx = sgm.n[0]; nz = sgm.n[1];
      } else {
        const th = sgm.ang * t, cth = Math.cos(th), sth = Math.sin(th);
        nx = sgm.n0[0] * cth - sgm.n0[1] * sth; nz = sgm.n0[0] * sth + sgm.n0[1] * cth;
        fx = sgm.c[0]; fz = sgm.c[1];
      }
      v.set(fx + nx * RING_OFF, 0, fz + nz * RING_OFF).applyQuaternion(q);
      w.set(fx, 0, fz).applyQuaternion(q);
      nn.set(nx, 0, nz).applyQuaternion(q);
      ring.push({ x: v.x, z: v.z, fx: w.x, fz: w.z, nx: nn.x, nz: nn.z, sb: sceneBearing(nn.x, nn.z), ab: sceneBearing(v.x - cW.x, v.z - cW.z), side: null });
    }
    TW.ring = ring;
    TW.centerW = cW;
    TW.name = nameOf(TW);
    // each side's run of samples and its middle (a flat face: all its samples share one bearing)
    TW.sideRuns = {}; TW.sideMid = {};
    if (UNITS) {
      for (const r of ring) { const sd = unitFor(trueBearing(r.sb)); r.side = sd ? sd.id : null; }
      for (const sd of UNITS.sides) {
        let start = -1;
        for (let i = 0; i < RING_N; i++) if (ring[i].side === sd.id && ring[(i - 1 + RING_N) % RING_N].side !== sd.id) { start = i; break; }
        if (start < 0) continue;
        const run = [];
        for (let k = 0; k < RING_N && ring[(start + k) % RING_N].side === sd.id; k++) run.push((start + k) % RING_N);
        TW.sideRuns[sd.id] = run;
        TW.sideMid[sd.id] = run[Math.floor(run.length / 2)];
      }
    }
    // the picked floor's label is anchored to the tower's outline: its corners, a little outside the balconies
    TW.cornersW = TW.poly.map(([x, z]) => {
      const dx = x - TW.cx, dz = z - TW.cz, l = Math.hypot(dx, dz) || 1;
      return localToWorld(x + (dx / l) * 2.8, 0, z + (dz / l) * 2.8);
    });
  }
  const ringY = (f) => floorLevel(f) + 0.5;
  /* the ring sample of a tower that lies in a scene direction from the tower's centre */
  function idxByAngle(TW, sb) {
    let best = 0, bd = 1e9;
    const R = TW.ring;
    for (let i = 0; i < RING_N; i++) {
      let d = Math.abs(R[i].ab - sb);
      if (d > 180) d = 360 - d;
      if (d < bd) { bd = d; best = i; }
    }
    return best;
  }
  function nearestIdx(TW, px, pz, facade) {
    let best = 0, bd = 1e18;
    const R = TW.ring;
    for (let i = 0; i < RING_N; i++) {
      const r = R[i];
      const dx = (facade ? r.fx : r.x) - px, dz = (facade ? r.fz : r.z) - pz;
      const d = dx * dx + dz * dz;
      if (d < bd) { bd = d; best = i; }
    }
    return { idx: best, dist: Math.sqrt(bd) };
  }
  /* where a facing lands on the ring: an example apartment's side at its middle, else the point in that direction */
  function idxForFacing(TW, b, sideId) {
    if (sideId && TW.sideMid[sideId] != null) return TW.sideMid[sideId];
    return idxByAngle(TW, normDeg(b - offset));
  }

  /* one ring group per tower (a tube and eight small compass ticks; the north tick a little longer) */
  const ringMat = new THREE.MeshBasicMaterial({ color: '#1F4B5C', toneMapped: false });
  for (const TW of TOWERS) {
    const g = new THREE.Group();
    g.visible = false;
    scene.add(g);
    const pts = [];
    for (let i = 0; i < RING_N; i += 4) pts.push(new THREE.Vector3(TW.ring[i].x, 0, TW.ring[i].z));
    const curve = new THREE.CatmullRomCurve3(pts, true, 'centripetal');
    g.add(new THREE.Mesh(new THREE.TubeGeometry(curve, 320, 0.15, 6, true), ringMat));
    const acc = newAcc();
    const box = new THREE.BoxGeometry(0.26, 0.26, 1);
    const m = new THREE.Matrix4(), qq = new THREE.Quaternion(), sc = new THREE.Vector3(), pp = new THREE.Vector3(), up = new THREE.Vector3(0, 1, 0);
    for (let k = 0; k < 8; k++) {
      const sb = normDeg(k * 45 - offset);
      const r = TW.ring[idxByAngle(TW, sb)];
      const dx = Math.sin(sb * DEG), dz = -Math.cos(sb * DEG);
      const len = k === 0 ? 2.8 : 1.4;
      qq.setFromAxisAngle(up, Math.atan2(dx, dz));
      pp.set(r.x + dx * (len / 2 + 0.05), 0, r.z + dz * (len / 2 + 0.05));
      m.compose(pp, qq, sc.set(1, 1, len));
      addGeometry(acc, box, m);
    }
    box.dispose();
    g.add(new THREE.Mesh(toGeom(acc), ringMat));
    TW.ringGroup = g;
  }

  /* example apartments: a stretch of the ring per side; the picked one (and the hovered one) drawn thicker */
  const arcMat = new THREE.MeshBasicMaterial({ color: '#2F6F86', toneMapped: false });
  const arcPrevMat = new THREE.MeshBasicMaterial({ color: '#2F6F86', toneMapped: false, transparent: true, opacity: 0.35, depthWrite: false });
  function makeArc(mat) { const m = new THREE.Mesh(new THREE.BufferGeometry(), mat); m.visible = false; m.renderOrder = 4; scene.add(m); return m; }
  const unitArc = makeArc(arcMat), unitArcPrev = makeArc(arcPrevMat);
  function placeArc(mesh, TW, side, f) {
    const run = side && TW ? TW.sideRuns[side.id] : null;
    if (!run || run.length < 8) { mesh.visible = false; return; }
    const cut = Math.max(4, Math.round(run.length * 0.07)); // a little left open at each end, so four stretches read as four apartments
    const pts = [];
    for (let k = cut; k <= run.length - 1 - cut; k += 3) { const r = TW.ring[run[k]]; pts.push(new THREE.Vector3(r.x, 0, r.z)); }
    if (pts.length < 2) { mesh.visible = false; return; }
    mesh.geometry.dispose();
    mesh.geometry = new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts, false, 'centripetal'), Math.max(8, pts.length * 2), 0.36, 8, false);
    mesh.position.set(0, ringY(f), 0);
    mesh.visible = true;
  }

  /* facing arrow (and a lighter preview that follows the pointer) */
  const ARROW_LEN = 9.7;
  function makeArrow(mat) {
    const acc = newAcc();
    const shaft = new THREE.CylinderGeometry(0.2, 0.2, 6.6, 10, 1);
    const head = new THREE.ConeGeometry(1.0, 2.6, 20, 1);
    const rx = new THREE.Matrix4().makeRotationX(Math.PI / 2);
    addGeometry(acc, shaft, new THREE.Matrix4().makeTranslation(0, 0, 0.5 + 3.3).multiply(rx));
    addGeometry(acc, head, new THREE.Matrix4().makeTranslation(0, 0, 0.5 + 6.6 + 1.3).multiply(rx));
    shaft.dispose(); head.dispose();
    const mesh = new THREE.Mesh(toGeom(acc), mat);
    mesh.visible = false;
    mesh.renderOrder = 5;
    scene.add(mesh);
    return mesh;
  }
  const arrow = makeArrow(new THREE.MeshBasicMaterial({ color: '#2F6F86', toneMapped: false }));
  const arrowPrev = makeArrow(new THREE.MeshBasicMaterial({ color: '#2F6F86', toneMapped: false, transparent: true, opacity: 0.4, depthWrite: false }));
  function placeArrow(mesh, TW, idx, f, sb) {
    const r = TW.ring[idx];
    const b = sb != null ? sb : r.sb;
    mesh.position.set(r.x, ringY(f), r.z);
    mesh.rotation.set(0, Math.atan2(Math.sin(b * DEG), -Math.cos(b * DEG)), 0);
    mesh.visible = true;
  }

  /* facing state and its words: "פונה מערבה · 280°" */
  let facing = null;          // { idx, bearing, sb, unit, toward, auto }
  let skipAuto = false;
  let previewIdx = -1;
  const chipBox = { w: 0, h: 0 };
  function renderFacing(elm, b) {
    elm.textContent = '';
    const words = typeof opts.facingWords === 'function' ? String(opts.facingWords(b) || '') : '';
    if (words) { elm.textContent = words; return; }
    elm.append(`${T.faces} ${dirWord(b)} · `);
    const n = document.createElement('span');
    n.dir = 'ltr';
    n.textContent = `${Math.round(normDeg(b)) % 360}°`;
    elm.append(n);
  }
  function updateFacingUI() {
    if (facing) {
      renderFacing(labelFacing, facing.bearing);
      labelFacing.classList.add('is-set');
      renderFacing(facingChip, facing.bearing);
      if (facing.toward) { labelFacing.textContent = 'לכיוון ' + facing.toward; facingChip.textContent = 'לכיוון ' + facing.toward; }
      labelMore.textContent = T.more || '';
      labelMore.hidden = !(facing.auto && T.more);
    } else {
      labelFacing.textContent = T.facingHint;
      labelFacing.classList.remove('is-set');
      labelMore.hidden = true;
      facingChip.classList.remove('is-on');
    }
    if (selected) {
      labelKick.textContent = selected.tower.name;
      labelTitle.textContent = T.floor(selected.floor);
      if (facing && facing.unit) {
        const chip = document.createElement('span');
        chip.className = 'rbs-sample';
        chip.textContent = UNITS.label || 'דירה לדוגמה';
        labelTitle.append(' ', chip);
      }
    }
    labelBox.w = 0; chipBox.w = 0;
  }
  function setFacingIdx(idx, source, exact, toward) {
    if (!selected || !selected.pinned || idx < 0) return null;
    const TW = selected.tower;
    let b = exact != null ? round1(exact) : round1(trueBearing(TW.ring[idx].sb));
    const side = toward ? null : unitFor(b);
    if (side) { b = round1(side.bearing); idx = idxForFacing(TW, b, side.id); }
    facing = { idx, bearing: b, sb: normDeg(b - offset), unit: side ? `${TW.id}-${selected.floor}-${side.id}` : null, toward: toward || null };
    placeArrow(arrow, TW, idx, selected.floor, facing.sb);
    placeArc(unitArc, TW, side, selected.floor);
    setPreview(-1);
    updateFacingUI();
    needsRender = true;
    lastInteract = performance.now();
    if (source === 'user') emit('nl:facing', { floor: selected.floor, heightM: heightOf(selected.floor), bearing: b, unit: facing.unit, toward: facing.toward, tower: TW.id });
    return b;
  }
  function setFacingBearing(b, source, toward) {
    if (!selected || !selected.pinned) return null;
    const side = toward ? null : unitFor(b);
    return setFacingIdx(idxForFacing(selected.tower, b, side ? side.id : null), source, b, toward);
  }
  function clearFacing() { facing = null; arrow.visible = false; unitArc.visible = false; setPreview(-1); updateFacingUI(); needsRender = true; }
  function setPreview(idx) {
    const TW = selected && selected.pinned ? selected.tower : null;
    let side = null;
    if (idx >= 0 && UNITS && TW) {
      side = unitFor(trueBearing(TW.ring[idx].sb));
      if (side) idx = idxForFacing(TW, side.bearing, side.id);
    }
    if (idx >= 0 && facing) {
      let d = Math.abs(idx - facing.idx); d = Math.min(d, RING_N - d);
      if (d < 10) { idx = -1; side = null; }
    }
    if (idx === previewIdx) return;
    previewIdx = idx;
    if (idx >= 0 && TW) {
      placeArrow(arrowPrev, TW, idx, selected.floor, side ? normDeg(side.bearing - offset) : null);
      placeArc(unitArcPrev, TW, side, selected.floor);
    } else { arrowPrev.visible = false; unitArcPrev.visible = false; }
    needsRender = true;
  }
  function bearingTowardCamera() {
    const c = selected ? selected.tower.centerW : TOWERS[0].centerW;
    return trueBearing(sceneBearing(camera.position.x - c.x, camera.position.z - c.z));
  }

  /* which facing sits under a screen point: the picked floor itself, or close to its ring */
  const ringPlane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0);
  const planeHit = new THREE.Vector3();
  function pickFacing(clientX, clientY, towerHit) {
    if (!selected || !selected.pinned) return -1;
    const TW = selected.tower, f = selected.floor;
    if (towerHit && towerHit.tower === TW && Math.abs(towerHit.point.y - (floorLevel(f) + FH / 2)) < FH * 0.75) {
      return nearestIdx(TW, towerHit.point.x, towerHit.point.z, true).idx;
    }
    setRay(clientX, clientY);
    ringPlane.constant = -ringY(f);
    if (!raycaster.ray.intersectPlane(ringPlane, planeHit)) return -1;
    const near = nearestIdx(TW, planeHit.x, planeHit.z, false);
    const r = TW.ring[near.idx];
    const a = projectToStage(tmpV.set(r.x, ringY(f), r.z));
    const rect = canvas.getBoundingClientRect();
    const tol = pointer.type === 'touch' ? 34 : 22;
    if (Math.hypot(rect.left + a.x - clientX, rect.top + a.y - clientY) > tol && near.dist > 3) return -1;
    return near.idx;
  }

  on(canvas, 'pointerdown', (e) => {
    pointer.down = true; pointer.moved = false; pointer.type = e.pointerType;
    pointer.downX = e.clientX; pointer.downY = e.clientY; pointer.downT = performance.now();
    engagedUntil = performance.now() + 4000;
    lastInteract = performance.now();
  });
  on(canvas, 'pointermove', (e) => {
    pointer.x = e.clientX; pointer.y = e.clientY; pointer.inside = true; pointer.type = e.pointerType;
    if (pointer.down && Math.hypot(e.clientX - pointer.downX, e.clientY - pointer.downY) > 6) pointer.moved = true;
    if (e.pointerType === 'mouse' && !pointer.down) hoverDirty = true;
  });
  on(window, 'pointerup', (e) => {
    if (!pointer.down) return;
    pointer.down = false;
    const quick = performance.now() - pointer.downT < 600;
    if (!pointer.moved && quick && e.target === canvas) handleTap(e.clientX, e.clientY);
  });
  function handleTap(x, y) {
    if (glide) return;
    const th = hitTower(x, y);
    if (selected && selected.pinned) {
      const idx = pickFacing(x, y, th);
      if (idx >= 0) { setFacingIdx(idx, 'user'); return; }
      if (th && (th.tower !== selected.tower || th.floor !== selected.floor)) { selectFloor(th.floor, 'user', th.tower); return; }
      if (th) return;
      clearFloor();
      return;
    }
    if (th) selectFloor(th.floor, 'user', th.tower);
    else clearFloor();
  }
  on(canvas, 'keydown', (e) => {
    const k = e.key;
    const pinned = !!(selected && selected.pinned);
    if (k === 'ArrowUp' || k === 'ArrowDown' || k === 'PageUp' || k === 'PageDown') {
      e.preventDefault();
      const step = (k === 'ArrowUp' || k === 'PageUp') ? 1 : -1;
      const next = pinned ? Math.min(FLOORS, Math.max(1, selected.floor + step)) : 25;
      if (!pinned || next !== selected.floor) selectFloor(next, 'user', pinned ? selected.tower : lastTower);
    } else if ((k === 'ArrowLeft' || k === 'ArrowRight') && pinned) {
      e.preventDefault();
      const step = UNITS ? 360 / UNITS.sides.length : 45;
      if (facing) setFacingBearing(Math.round(facing.bearing / step) * step + (k === 'ArrowRight' ? step : -step), 'user');
      else setFacingBearing(Math.round(bearingTowardCamera() / step) * step, 'user');
    } else if ((k === 't' || k === 'T') && pinned) {
      // the other tower, the same floor
      e.preventDefault();
      selectFloor(selected.floor, 'user', selected.tower === TOWERS[0] ? TOWERS[1] : TOWERS[0]);
    } else if (k === 'Enter' && selected) {
      e.preventDefault();
      emitCta();
    } else if (k === 'Escape') {
      if (facing) clearFacing(); else clearFloor();
    }
  });
  let labelHover = false;
  on(label, 'pointerenter', () => { labelHover = true; });
  on(label, 'pointerleave', () => { labelHover = false; });
  let cardAt = 0;
  const fresh = () => performance.now() - cardAt < 500;
  on(labelCta, 'click', () => { if (!fresh()) emitCta(); });
  for (const id of Object.keys(actBtns || {})) {
    on(actBtns[id], 'click', () => {
      if (!selected || fresh()) return;
      emit('nl:floor-action', { action: id, floor: selected.floor, heightM: heightOf(selected.floor), bearing: facing ? facing.bearing : null, unit: facing ? facing.unit : null, tower: selected.tower.id });
    });
  }
  on(labelClose, 'click', () => clearFloor());
  function emitCta() {
    if (!selected) return;
    emit('nl:floor-cta', { floor: selected.floor, bearing: facing ? facing.bearing : null, tower: selected.tower.id });
  }

  let hoverLeaveAt = 0;
  function setHover(h) {
    const same = (h && hover && h.tower === hover.tower && h.floor === hover.floor) || (!h && !hover);
    if (same) return;
    hover = h;
    root.classList.toggle('rbs--pointer', !!h);
    if (!selected || !selected.pinned) {
      if (h) showFloor(h.tower, h.floor, false);
      else hoverLeaveAt = performance.now();
    }
  }
  /* a pinned pick: ring, dimming, glide, events for user picks */
  let dimTarget = 0;
  function selectFloor(f, source, TW) {
    const prevT = selected && selected.pinned ? selected.tower : null;
    const prev = prevT ? selected.floor : null;
    TW = TW || prevT || lastTower;
    lastTower = TW;
    showFloor(TW, f, true);
    hint.classList.add('is-gone');
    const auto = !facing && !skipAuto && UNITS && opts.autoFacing ? UNITS.sides.find((x) => x.id === opts.autoFacing) : null;
    if (auto) facing = { idx: idxForFacing(TW, auto.bearing, auto.id), bearing: round1(auto.bearing), sb: normDeg(auto.bearing - offset), unit: `${TW.id}-${f}-${auto.id}`, toward: null, auto: true };
    for (const X of TOWERS) X.ringGroup.visible = X === TW;
    TW.ringGroup.position.y = ringY(f);
    dimTarget = 1;
    if (reduced) U.uDim.value = 1;
    U.uHiGlow.value = 0.5;
    controls.minDistance = 55;
    if (facing) {
      // the same side of the new floor (or the other tower): its example apartment
      const side = facing.unit ? unitFor(facing.bearing) : null;
      facing.idx = idxForFacing(TW, facing.bearing, side ? side.id : null);
      facing.unit = side ? `${TW.id}-${f}-${side.id}` : null;
      placeArrow(arrow, TW, facing.idx, f, facing.sb);
      placeArc(unitArc, TW, side, f);
    }
    if (previewIdx >= 0) { arrowPrev.visible = false; unitArcPrev.visible = false; previewIdx = -1; }
    updateFacingUI();
    frameFloor(TW, f, prev, prevT);
    lastInteract = performance.now();
    if (source === 'user') {
      emit('nl:floor', { floor: f, heightM: heightOf(f), tower: TW.id, towerName: TW.name });
      if (facing) emit('nl:facing', { floor: f, heightM: heightOf(f), bearing: facing.bearing, unit: facing.unit, tower: TW.id });
    }
  }
  function showFloor(TW, f, pinned) {
    if (!label.classList.contains('is-on')) cardAt = performance.now();
    selected = { tower: TW, floor: f, pinned };
    U.uHiFloor.value = f;
    U.uHiTower.value = TW.k;
    labelKick.textContent = TW.name;
    labelTitle.textContent = T.floor(f);
    const note = typeof opts.floorNote === 'function' ? opts.floorNote(f, TW.id) : null;
    const top = FLOORS - (opts.penthouseFloors || 0);
    labelLine.textContent = note ? String(note) : (opts.penthouseFloors && f > top ? T.penthouse : (f >= opts.highFloorsFrom ? T.high : T.low));
    labelFacing.hidden = !pinned;
    label.classList.add('is-on');
    labelBox.w = 0;
    needsRender = true;
  }
  function clearFloor() {
    const wasPinned = !!(selected && selected.pinned);
    selected = null;
    hover = null;
    facing = null;
    previewIdx = -1;
    arrow.visible = false; arrowPrev.visible = false; unitArc.visible = false; unitArcPrev.visible = false;
    for (const X of TOWERS) X.ringGroup.visible = false;
    U.uHiFloor.value = -100;
    U.uHiTower.value = 0;
    U.uHiGlow.value = 0.22;
    dimTarget = 0;
    if (reduced) U.uDim.value = 0;
    label.classList.remove('is-on');
    facingChip.classList.remove('is-on');
    leaderLine.setAttribute('visibility', 'hidden');
    leaderDot.setAttribute('visibility', 'hidden');
    root.classList.remove('rbs--pointer');
    updateFacingUI();
    if (wasPinned) frameOverview();
    needsRender = true;
  }

  /* camera glides (a cut under reduced motion) */
  const sph = new THREE.Spherical();
  const glideT = new THREE.Vector3();
  function camSpherical() {
    sph.setFromVector3(tmpV.subVectors(camera.position, controls.target));
    return { r: sph.radius, phi: sph.phi, theta: sph.theta };
  }
  function setCamSpherical(target, r, phi, theta) {
    sph.set(r, phi, theta);
    camera.position.setFromSpherical(sph).add(target);
    camera.lookAt(target);
  }
  function syncControls() {
    if (controls._sphericalDelta) controls._sphericalDelta.set(0, 0, 0);
    controls.update();
  }
  function glideTo(target, r, phi, theta, dur, after) {
    if (phase === 'intro') endIntro();
    const from = camSpherical();
    let dth = theta - from.theta;
    dth = Math.atan2(Math.sin(dth), Math.cos(dth));
    const to = { r, phi: Math.min(controls.maxPolarAngle, Math.max(controls.minPolarAngle, phi)), theta: from.theta + dth };
    if (reduced || !opts.glide || dur <= 0) {
      glide = null;
      controls.target.copy(target);
      setCamSpherical(controls.target, to.r, to.phi, to.theta);
      controls.enabled = true;
      syncControls();
      if (after) after();
      needsRender = true;
      return;
    }
    glide = { fromT: controls.target.clone(), toT: target.clone(), from, to, t: 0, dur, after };
    controls.enabled = false;
    kick();
  }
  function stepGlide(adt) {
    const g = glide;
    g.t = Math.min(1, g.t + adt / g.dur);
    const k = ease(g.t);
    glideT.copy(g.fromT).lerp(g.toT, k);
    const r = Math.exp(Math.log(g.from.r) + (Math.log(g.to.r) - Math.log(g.from.r)) * k);
    const phi = g.from.phi + (g.to.phi - g.from.phi) * k;
    const theta = g.from.theta + (g.to.theta - g.from.theta) * k;
    controls.target.copy(glideT);
    setCamSpherical(controls.target, r, phi, theta);
    if (g.t >= 1) {
      glide = null;
      controls.enabled = true;
      syncControls();
      if (g.after) g.after();
    }
    needsRender = true;
  }
  function floorFrame(TW, f) {
    const vf = camera.fov * DEG, hf = 2 * Math.atan(Math.tan(vf / 2) * camera.aspect);
    const r = Math.max(28 / Math.tan(vf / 2), 42 / Math.tan(hf / 2));
    const y = floorLevel(f) + EYE_M;
    // low floors are seen from a little higher, so the retail buildings and the lobby do not hide them
    const elev = y < 40 ? Math.min(40, Math.max(9, Math.atan2(40 - y, 30) / DEG)) : 9;
    // a phone: the card docks at the bottom of the stage, so the picked floor is framed in the upper third
    const lift = stageW < 600 ? 0.44 * r * Math.tan(vf / 2) : 0;
    return { target: new THREE.Vector3(TW.centerW.x, Math.max(2, y - lift), TW.centerW.z), r, phi: (90 - elev) * DEG };
  }
  function frameFloor(TW, f, prev, prevT) {
    const fr = floorFrame(TW, f);
    const cur = camSpherical();
    if (prev == null || prevT !== TW) glideTo(fr.target, prev == null ? fr.r : Math.min(cur.r, fr.r * 1.6), fr.phi, cur.theta, 1.15);
    else glideTo(fr.target, Math.min(cur.r, fr.r * 1.8), Math.min(cur.phi, fr.phi), cur.theta, 0.7);
  }
  function frameOverview() {
    const cur = camSpherical();
    glideTo(heroTarget, heroDistance(), (90 - HERO.elev) * DEG, cur.theta, 1.0, () => { controls.minDistance = 140; });
  }

  /* label placement: anchored to the picked tower's outline at the selected floor */
  const camRight = new THREE.Vector3();
  function supportPoint(TW, dir, out) {
    let best = null, bd = -1e9;
    for (const c of TW.cornersW) { const d = (c.x - TW.centerW.x) * dir.x + (c.z - TW.centerW.z) * dir.z; if (d > bd) { bd = d; best = c; } }
    return out.set(best.x, 0, best.z);
  }
  function projectToStage(v) {
    tmpV2.copy(v).project(camera);
    return { x: (tmpV2.x * 0.5 + 0.5) * stageW, y: (-tmpV2.y * 0.5 + 0.5) * stageH, behind: tmpV2.z > 1 };
  }
  function floorAnchor(TW, f, side) {
    camRight.setFromMatrixColumn(camera.matrixWorld, 0);
    camRight.y = 0;
    camRight.normalize().multiplyScalar(side);
    supportPoint(TW, camRight, tmpV);
    tmpV.y = floorLevel(f) + 0.6;
    return projectToStage(tmpV);
  }
  function arrowTip() {
    if (!facing || !selected) return null;
    const r = selected.tower.ring[facing.idx], L = ARROW_LEN + 1.4;
    const dx = Math.sin(facing.sb * DEG), dz = -Math.cos(facing.sb * DEG);
    return projectToStage(tmpV.set(r.x + dx * L, ringY(selected.floor), r.z + dz * L));
  }
  function placeLabel() {
    if (!selected) return;
    const TW = selected.tower;
    const narrow = stageW < 600;
    if (!labelBox.w) { labelBox.w = label.offsetWidth || 244; labelBox.h = label.offsetHeight || 140; }
    const lw = labelBox.w, lh = labelBox.h;
    const aR = floorAnchor(TW, selected.floor, 1), aL = floorAnchor(TW, selected.floor, -1);
    const roomR = stageW - aR.x, roomL = aL.x;
    const tip = arrowTip();
    if (tip && !tip.behind && !narrow) {
      const tipSide = tip.x > (aR.x + aL.x) / 2 ? 1 : -1;
      const roomOther = tipSide === 1 ? roomL : roomR;
      if (tipSide === labelSide && roomOther > lw + 70) labelSide = -tipSide;
    }
    if (labelSide === 1 && roomR < lw + 60 && roomL > roomR + 40) labelSide = -1;
    else if (labelSide === -1 && roomL < lw + 60 && roomR > roomL + 40) labelSide = 1;
    const a = labelSide === 1 ? aR : aL;
    if (a.behind) { label.classList.remove('is-on'); return; }
    let x, y, lx, ly;
    if (narrow) {
      x = Math.round((stageW - lw) / 2);
      y = Math.round(stageH - lh - 64);
      if (a.y > y - 30) y = Math.max(56, Math.round(a.y - lh - 48));
      lx = Math.min(Math.max(a.x, x + 24), x + lw - 24);
      ly = a.y < y ? y : y + lh;
    } else {
      const gap = 64;
      x = labelSide === 1 ? a.x + gap : a.x - gap - lw;
      y = a.y - lh / 2;
      x = Math.min(Math.max(12, x), stageW - lw - 12);
      y = Math.min(Math.max(12, y), stageH - lh - 64);
      lx = labelSide === 1 ? x : x + lw;
      ly = Math.min(Math.max(a.y, y + 18), y + lh - 18);
    }
    label.style.transform = `translate3d(${Math.round(x)}px, ${Math.round(y)}px, 0)`;
    if (!label.classList.contains('is-on')) label.classList.add('is-on');
    leaderLine.setAttribute('x1', a.x.toFixed(1));
    leaderLine.setAttribute('y1', a.y.toFixed(1));
    leaderLine.setAttribute('x2', lx.toFixed(1));
    leaderLine.setAttribute('y2', ly.toFixed(1));
    leaderDot.setAttribute('cx', a.x.toFixed(1));
    leaderDot.setAttribute('cy', a.y.toFixed(1));
    leaderLine.setAttribute('visibility', 'visible');
    leaderDot.setAttribute('visibility', 'visible');
    placeChip(tip);
  }

  /* the streets' and the towers' names over the model (not buttons): the city's labels (city.json) and one per tower */
  const qNames = new Set(qpins.map((p) => p.it && p.it.name));
  const smarks = [];
  for (const lb of (world.labels || [])) {
    if (qNames.has(lb[0])) continue; // a quarter pin already names it
    const e = el('span', 'dus-street', marks);
    e.textContent = lb[0];
    smarks.push({ el: e, x: lb[1], z: lb[2], y: 0.6, w: 0, h: 0, kind: 'street' });
  }
  for (const TW of TOWERS) {
    const e = el('span', 'dus-tname', marks);
    e.textContent = TW.name;
    smarks.push({ el: e, x: TW.cx, z: TW.cz, y: TW.top + 7, w: 0, h: 0, kind: 'tower', tw: TW });
  }

  /* the quarter's pins: over each mass and place; hidden behind the camera or off the stage, fainter far away */
  const qv = new THREE.Vector3(), qdir = new THREE.Vector3();
  let framedPhase = false;
  const frameCam = camera.clone();
  function frameGroup(k) {
    const tw = localToWorld(MID.x, 0, MID.z);
    const pts = [];
    for (const TW of TOWERS) for (const c of TW.cornersW) pts.push(new THREE.Vector3(c.x, 0, c.z), new THREE.Vector3(c.x, TW.top, c.z));
    const centres = [];
    for (const p of qpins) {
      if (p.it.kind !== 'project' || p.it.phase !== k) continue;
      pts.push(new THREE.Vector3(p.x, 0, p.z), new THREE.Vector3(p.x, p.y, p.z));
      centres.push(new THREE.Vector3(p.x, 0, p.z));
    }
    if (!centres.length) return;
    const gc = centres.reduce((acc, v) => acc.add(v), new THREE.Vector3()).multiplyScalar(1 / centres.length);
    const c = gc.clone().add(tw).multiplyScalar(0.5).setY(TOP * 0.3);
    const ax = gc.x - tw.x, az = gc.z - tw.z;
    const cur = camSpherical();
    const near = (t) => Math.abs(Math.atan2(Math.sin(t - cur.theta), Math.cos(t - cur.theta)));
    let th = Math.atan2(-az, ax);
    if (near(th + Math.PI) < near(th)) th += Math.PI;
    const phi = 58 * DEG;
    frameCam.aspect = camera.aspect; frameCam.fov = camera.fov; frameCam.updateProjectionMatrix();
    let lo = 60, hi = 3200;
    for (let i = 0; i < 18; i++) {
      const d = (lo + hi) / 2;
      sph.set(d, phi, th);
      frameCam.position.setFromSpherical(sph).add(c);
      frameCam.lookAt(c);
      frameCam.updateMatrixWorld(true);
      const ok = pts.every((v) => { const q = v.clone().project(frameCam); return q.z < 1 && Math.abs(q.x) < 0.8 && q.y > -0.74 && q.y < 0.66; });
      if (ok) hi = d; else lo = d;
    }
    if (hi * 1.05 > controls.maxDistance) controls.maxDistance = hi * 1.05;
    glideTo(c, hi, phi, th, 1.2);
  }
  function facilityPoint(an, out) {
    const ph = /^ph:([NS])$/.exec(an);
    if (ph && TOWER_BY[ph[1]]) {
      const pp = phPools(TOWER_BY[ph[1]])[0]; // floor 49's pool on its terrace (illustration)
      return localToWorld(pp.cx + pp.nx * 1.2, floorLevel(pp.f) + 2.2, pp.cz + pp.nz * 1.2, out);
    }
    const zMid = (LOBBY[0][1] + LOBBY[3][1]) / 2;
    if (an === 'deck:pool') return localToWorld(POOL.cx, DECK_Y + 1.6, POOL.cz + 6, out);
    if (an === 'lobby') return localToWorld(LOBBY[0][0] - 1.0, PLOT.h + 2.4, zMid - 7, out);
    // the wellness complex, the gym and the club: the floor is not published; at the north tower's base (illustration)
    if (an === 'club') { const TW = TOWERS[0]; return localToWorld(TW.poly[0][0] - 1.5, PLOT.h + 3.2, TW.cz - 4, out); }
    if (an === 'court') return localToWorld((COURT.x0 + COURT.x1) / 2, PLOT.h + 1.6, (COURT.z0 + COURT.z1) / 2, out);
    if (an === 'parking') return localToWorld(-2.0, PLOT.h + 1.2, 40, out);
    return null;
  }
  function towerRects() {
    // each tower on screen (and a band above its crown): no quarter pin may sit on it, in front of it or behind it
    const rects = [];
    for (const TW of TOWERS) {
      let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9, any = false;
      for (const c of TW.cornersW) {
        for (const y of [0, TW.top + 4]) {
          qv.set(c.x, y, c.z);
          const s = projectToStage(qv);
          if (s.behind) continue;
          any = true;
          x0 = Math.min(x0, s.x); x1 = Math.max(x1, s.x); y0 = Math.min(y0, s.y); y1 = Math.max(y1, s.y);
        }
      }
      if (any) rects.push({ x: x0 - 8, y: y0 - 44, w: x1 - x0 + 16, h: y1 - y0 + 44 });
    }
    return rects;
  }
  function placeQuarter() {
    const pinned = !!(selected && selected.pinned);
    const shown = [];
    const heroes = towerRects();
    const onTower = (s) => heroes.some((hr) => s.x < hr.x + hr.w + 4 && hr.x < s.x + s.w + 4 && s.y < hr.y + hr.h + 2 && hr.y < s.y + s.h + 2);
    for (const p of qpins) {
      if (p.off || (p.hero && !framedPhase)) { p.el.style.visibility = 'hidden'; continue; }
      qv.set(p.x, p.y, p.z);
      const a = projectToStage(qv);
      if (a.behind || a.x < -40 || a.x > stageW + 40 || a.y < 20 || a.y > stageH - 40) { p.el.style.visibility = 'hidden'; continue; }
      qdir.subVectors(qv, camera.position);
      const d = qdir.length();
      raycaster.set(camera.position, qdir.normalize());
      raycaster.far = d;
      const hidden = !p.hero && raycaster.intersectObjects(world.towerProxies, false).length > 0;
      raycaster.far = Infinity;
      if (hidden) { p.el.style.visibility = 'hidden'; continue; }
      if (!p.w && p.el.offsetWidth) { p.w = p.el.offsetWidth; p.h = p.el.offsetHeight; }
      const w = p.w || 80, h = p.h || 30;
      const x = Math.min(Math.max(6, a.x - w / 2), stageW - w - 6);
      shown.push({ p, x, y: a.y - 34, w, h, d });
    }
    for (const p of fpins) {
      if (p.off || !facilityPoint(p.an, qv)) { p.el.style.visibility = 'hidden'; continue; }
      const a = projectToStage(qv);
      if (a.behind || a.x < -40 || a.x > stageW + 40 || a.y < 20 || a.y > stageH - 40) { p.el.style.visibility = 'hidden'; continue; }
      if (!p.w && p.el.offsetWidth) { p.w = p.el.offsetWidth; p.h = p.el.offsetHeight; }
      const w = p.w || 90, h = p.h || 30;
      const x = Math.min(Math.max(6, a.x - w / 2), stageW - w - 6);
      shown.push({ p, x, y: a.y - 34, w, h, d: qv.distanceTo(camera.position) });
    }
    shown.sort((u, v) => (v.p.hero ? 1 : 0) - (u.p.hero ? 1 : 0) || (v.p.fac ? 1 : 0) - (u.p.fac ? 1 : 0) || u.d - v.d);
    const kept = [];
    {
      const rr = root.getBoundingClientRect();
      for (const u of [hint, root.querySelector('.rbs-presets'), root.querySelector('.rbs-caption'), label.classList.contains('is-on') ? label : null, qcard && qcard.classList.contains('is-on') ? qcard : null]) {
        if (!u || (u === hint && u.classList.contains('is-gone'))) continue;
        const b = u.getBoundingClientRect();
        if (b.width > 0 && b.height > 0) kept.push({ x: b.left - rr.left - 4, y: b.top - rr.top - 4, w: b.width + 8, h: b.height + 8, chrome: true });
      }
    }
    const hits = (s) => kept.some((k) => s.x < k.x + k.w + 4 && k.x < s.x + s.w + 4 && s.y < k.y + k.h + 2 && k.y < s.y + s.h + 2);
    for (const s of shown) {
      if (!s.p.hero && !s.p.fac && onTower(s)) { s.p.el.style.visibility = 'hidden'; continue; }
      if (s.p.fac) { for (let t = 0; t < 4 && hits(s); t++) s.y -= s.h + 6; }
      if (hits(s) || s.y < 4) { s.p.el.style.visibility = 'hidden'; continue; }
      kept.push(s);
      const fade = framedPhase || s.p.fac ? 1 : Math.min(1, Math.max(0.35, 1.25 - s.d / 2600)) * (pinned ? 0.6 : 1);
      s.p.el.style.visibility = 'visible';
      s.p.el.style.opacity = fade.toFixed(2);
      s.p.el.style.transform = `translate3d(${Math.round(s.x)}px, ${Math.round(s.y)}px, 0)`;
    }
    // the names last: they never cover a pin, a card or the stage's own controls
    for (const m of smarks) {
      const hide = (m.kind === 'tower' && (pinned || framedPhase)) || (m.kind === 'street' && (framedPhase || (pinned && stageW < 600)));
      if (hide) { m.el.style.visibility = 'hidden'; continue; }
      localToWorld(m.x, m.y, m.z, qv);
      const a = projectToStage(qv);
      if (a.behind || a.x < 10 || a.x > stageW - 10 || a.y < 14 || a.y > stageH - 30) { m.el.style.visibility = 'hidden'; continue; }
      if (m.kind === 'street') {
        // a street behind a tower is not named on the tower
        qdir.subVectors(qv, camera.position);
        const dd = qdir.length();
        raycaster.set(camera.position, qdir.normalize());
        raycaster.far = dd;
        const behindTower = raycaster.intersectObjects(world.towerProxies, false).length > 0;
        raycaster.far = Infinity;
        if (behindTower) { m.el.style.visibility = 'hidden'; continue; }
      }
      if (!m.w && m.el.offsetWidth) { m.w = m.el.offsetWidth; m.h = m.el.offsetHeight; }
      const w = m.w || 70, h = m.h || 20;
      const s = { x: Math.min(Math.max(6, a.x - w / 2), stageW - w - 6), y: a.y - h / 2, w, h };
      if (m.kind === 'tower') {
        // above the crown; under the light switch or the hint (a phone's top edge): on the crown's screen instead
        s.y = a.y - h;
        if (hits(s) || s.y < 6) { localToWorld(m.x, m.tw.roof + 5, m.z, qv); const b2 = projectToStage(qv); s.y = b2.y - h / 2; }
        if (hits(s) || s.y < 6) { m.el.style.visibility = 'hidden'; continue; }
      } else if (hits(s)) { m.el.style.visibility = 'hidden'; continue; }
      kept.push(s);
      m.el.style.visibility = 'visible';
      m.el.style.transform = `translate3d(${Math.round(s.x)}px, ${Math.round(s.y)}px, 0)`;
    }
  }
  function openFacilityCard(it) {
    if (!qcard) return;
    qcard.textContent = '';
    const x = el('button', 'rbs-qcard-x', qcard, { type: 'button', 'aria-label': T.close });
    x.textContent = '×';
    x.addEventListener('click', () => { qcard.classList.remove('is-on'); needsRender = true; kick(); });
    el('p', 'rbs-qcard-kick', qcard).textContent = 'מתקן בפרויקט';
    el('p', 'rbs-qcard-title', qcard).textContent = it.name;
    for (const line of (Array.isArray(it.lines) ? it.lines : [])) el('p', 'rbs-qcard-line', qcard).textContent = line;
    if (it.note) el('p', 'rbs-qcard-note', qcard).textContent = it.note;
    if (it.tour && it.tour.src) { // FacilityRooms v83: walk into the facility, a 360 room (illustration), in the page's viewer
      const go = el('button', 'rbs-qcard-page rbs-qcard-360', qcard, { type: 'button' });
      el('b', 'rbs-qcard-360b', go).textContent = '360°';
      go.appendChild(document.createTextNode(it.tour.label || 'כניסה ב־360°'));
      const q = new URL(import.meta.url).search || '';
      const abs = (f) => new URL('./tour/' + f, import.meta.url).href.split('?')[0] + q;
      go.addEventListener('click', () => window.dispatchEvent(new CustomEvent('nl:facility-tour', { detail: {
        id: it.id, src: abs(it.tour.src), small: abs(it.tour.small || it.tour.src), title: it.tour.title || it.name, note: it.note || '', opener: go } })));
    }
    const wa = String(opts.wa || '').replace(/[^0-9]/g, '');
    if (wa) {
      const cta = el('div', 'rbs-qcard-cta', qcard);
      const a = el('a', 'rbs-qcard-page rbs-qcard-wa', cta, { href: 'https://wa.me/' + wa + '?text=' + encodeURIComponent((window.__nlStageI18n && typeof window.__nlStageI18n.wa === 'function' && window.__nlStageI18n.wa('ask', { what: it.ask || it.name, project: T.heroName })) || ('שלום, יש לי שאלה על ' + (it.ask || it.name) + ' ' + T.in + '.')), target: '_blank', rel: 'noopener' });
      a.textContent = 'שאלה על המתקן בוואטסאפ';
    }
    qcard.dataset.phase = '';
    qcard.setAttribute('aria-label', it.name);
    qcard.classList.add('is-on');
    emit('nl:facility', { id: it.id || null, name: it.name });
    needsRender = true; kick();
  }
  function openQuarterCard(it) {
    if (!qcard) return;
    const isP = it.kind === 'project';
    const words = typeof opts.facingWords === 'function' ? String(opts.facingWords(Number(it.bearing)) || '') : '';
    const where = Math.round(Number(it.dist) || 0) + ' מ׳ ' + T.from + (!isP && it.walk ? ', כ-' + it.walk + ' דקות הליכה' : '') + (words ? ', ' + words : '');
    qcard.textContent = '';
    const x = el('button', 'rbs-qcard-x', qcard, { type: 'button', 'aria-label': T.close });
    x.textContent = '×';
    x.addEventListener('click', () => { qcard.classList.remove('is-on'); needsRender = true; kick(); });
    el('p', 'rbs-qcard-kick', qcard).textContent = isP ? 'פרויקט בסביבה' : 'מקום בסביבה';
    el('p', 'rbs-qcard-title', qcard).textContent = it.name;
    if (isP && it.brand) el('p', 'rbs-qcard-brand', qcard).textContent = it.brand;
    const line = isP ? [it.developer, it.status].filter(Boolean).join(' · ') : String(it.status || '');
    if (line) el('p', 'rbs-qcard-line', qcard).textContent = line;
    qcard.dataset.phase = isP ? String(it.phase || '') : '';
    if (isP) {
      const facts = [it.floors ? it.floors + ' קומות' : '', it.units ? it.units + ' דירות' : ''].filter(Boolean).join(' · ');
      if (facts) el('p', 'rbs-qcard-facts', qcard).textContent = facts;
      if (Number(it.occupancy) > 2000) el('p', 'rbs-qcard-facts', qcard).textContent = 'אכלוס צפוי ' + it.occupancy + ', לפי עמוד הפרויקט';
    }
    el('p', 'rbs-qcard-dist', qcard).textContent = where;
    el('p', 'rbs-qcard-note', qcard).textContent = isP ? (Q_NOTE || '') : String(it.source || '');
    const cta = el('div', 'rbs-qcard-cta', qcard);
    const go = el('button', 'rbs-qcard-go', cta, { type: 'button' });
    go.textContent = 'מה רואים ' + T.from + ' לכיוונו';
    go.addEventListener('click', () => { lookToward(it); qcard.classList.remove('is-on'); });
    if (isP && it.url) {
      const a = el('a', 'rbs-qcard-page', cta, { href: String(it.url) });
      a.textContent = 'לעמוד הפרויקט';
    }
    qcard.setAttribute('aria-label', it.name);
    qcard.classList.add('is-on');
    emit('nl:quarter', { kind: it.kind, name: it.name, id: it.id || null });
    needsRender = true; kick();
  }
  function lookToward(it) {
    const TW = selected && selected.pinned ? selected.tower : lastTower;
    const f = selected && selected.pinned ? selected.floor : 25;
    if (!(selected && selected.pinned && selected.floor === f && selected.tower === TW)) selectFloor(f, 'user', TW);
    setFacingBearing(Number(it.bearing) || 0, 'user', it.name);
    kick();
  }
  const Q_NOTE = opts.quarter && opts.quarter.note ? String(opts.quarter.note) : '';
  for (const p of qpins) if (!p.hero) on(p.el, 'click', (e) => { e.stopPropagation(); openQuarterCard(p.it); });
  for (const p of fpins) on(p.el, 'click', (e) => { e.stopPropagation(); openFacilityCard(p.it); });
  function placeChip(tip) {
    if (!tip || tip.behind || !(selected && selected.pinned)) { facingChip.classList.remove('is-on'); return; }
    if (!chipBox.w) { facingChip.classList.add('is-on'); chipBox.w = facingChip.offsetWidth || 120; chipBox.h = facingChip.offsetHeight || 30; }
    const x = Math.min(Math.max(8, tip.x - chipBox.w / 2), stageW - chipBox.w - 8);
    const y = Math.min(Math.max(8, tip.y - chipBox.h - 10), stageH - chipBox.h - 8);
    // never over the floor card (the card says the same direction)
    const lr = label.getBoundingClientRect(), rr = root.getBoundingClientRect();
    const lx = lr.left - rr.left, ly = lr.top - rr.top;
    if (label.classList.contains('is-on') && x < lx + lr.width + 6 && lx < x + chipBox.w + 6 && y < ly + lr.height + 6 && ly < y + chipBox.h + 6) { facingChip.classList.remove('is-on'); return; }
    facingChip.style.transform = `translate3d(${Math.round(x)}px, ${Math.round(y)}px, 0)`;
    facingChip.classList.add('is-on');
  }

  /* visibility */
  const io = new IntersectionObserver((entries) => {
    for (const en of entries) visible = en.isIntersecting;
    if (visible) kick();
  }, { threshold: 0.01 });
  io.observe(root);
  on(document, 'visibilitychange', () => { if (!document.hidden) kick(); });

  on(canvas, 'webglcontextlost', (e) => { e.preventDefault(); running = false; ctx.onContextLost(); });

  /* ambient occlusion (lazy): Rainbow's GTAO without a composer */
  async function enableAO() {
    if (aoOn || aoLoading || disposedE) return;
    aoLoading = true;
    try {
      if (!post) {
        const { GTAOPass } = await import('three/addons/postprocessing/GTAOPass.js');
        if (disposedE) return;
        const gtao = new GTAOPass(scene, camera, 2, 2);
        const fullSetSize = gtao.setSize.bind(gtao);
        gtao.setSize = (w, h) => fullSetSize(Math.max(2, Math.round(w * AO_SCALE)), Math.max(2, Math.round(h * AO_SCALE)));
        gtao.setSize(stageW * dpr, stageH * dpr);
        gtao.output = GTAOPass.OUTPUT.Off;
        gtao.updateGtaoMaterial({ radius: 4.0, distanceExponent: 1.4, thickness: 5.0, scale: 1.6, samples: 16, distanceFallOff: 1.0, screenSpaceRadius: false });
        gtao.updatePdMaterial({ lumaPhi: 10, depthPhi: 2, normalPhi: 3, radius: 7, radiusExponent: 1.5, rings: 3, samples: 16 });
        // AO only on DUO's own lot and its street edges: the city, the far sea and the horizon stay clean
        gtao.setSceneClipBox(new THREE.Box3(new THREE.Vector3(-120, -8, -120), new THREE.Vector3(120, TOP + 12, 120)));
        const blendMat = new THREE.ShaderMaterial({
          uniforms: { tAO: { value: gtao.gtaoMap }, uStrength: { value: 0 } },
          vertexShader: 'varying vec2 vUv; void main() { vUv = uv; gl_Position = vec4(position.xy, 0.0, 1.0); }',
          fragmentShader: 'uniform sampler2D tAO; uniform float uStrength; varying vec2 vUv; void main() { float ao = texture2D(tAO, vUv).r; gl_FragColor = vec4(vec3(mix(1.0, ao, uStrength)), 1.0); }',
          blending: THREE.CustomBlending, blendSrc: THREE.DstColorFactor, blendDst: THREE.ZeroFactor, blendEquation: THREE.AddEquation,
          depthTest: false, depthWrite: false, transparent: true, toneMapped: false,
        });
        const quad = new THREE.Mesh(new THREE.PlaneGeometry(2, 2), blendMat);
        quad.frustumCulled = false;
        const quadScene = new THREE.Scene();
        quadScene.add(quad);
        post = { gtao, blendMat, quad, quadScene, quadCam: new THREE.Camera() };
      }
      aoOn = true;
      aoProbe = aoMode === 'auto' ? performance.now() : 0;
      aoFade = aoMode === 'auto' ? 0 : 1;
      aoFadeDir = aoMode === 'auto' ? 0 : 1;
      applyAOFade();
      perf.times.length = 0;
      needsRender = true;
    } catch (err) {
      console.warn('[duo-stage] AO unavailable', err);
      aoBlocked = true;
    } finally { aoLoading = false; }
  }
  const AO_STRENGTH = 0.85;
  const AO_SCALE = 1.0;
  function applyAOFade() {
    if (post) post.blendMat.uniforms.uStrength.value = aoFade * AO_STRENGTH;
    M.decal.opacity = 0.2 - 0.1 * aoFade;
  }
  function disableAO() { aoOn = false; aoProbe = 0; aoFade = 0; aoFadeDir = 0; applyAOFade(); needsRender = true; }
  if (aoMode === 'on') enableAO();

  /* frame loop */
  function kick() { if (!rafId && running && !disposedE) { lastT = performance.now(); rafId = requestAnimationFrame(frame); } }
  function endIntro() {
    if (phase !== 'intro') return;
    phase = 'orbit';
    controls.target.copy(heroTarget);
    controls.enabled = true;
    controls.update();
    lastInteract = performance.now() - (autoOrbit ? 6000 : 0);
  }
  const ease = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);

  function frame(now) {
    rafId = 0;
    if (disposedE || !running) return;
    const rawDt = Math.max(0.0005, (now - lastT) / 1000);
    const dt = Math.min(0.1, rawDt);
    const adt = Math.min(1.0, rawDt);
    lastT = now;
    if (!visible || document.hidden) return;
    clock += dt;
    const animateWater = !reduced;
    if (animateWater) U.uTime.value = clock;

    if (phase === 'intro') {
      if (introHold > 0) introHold -= adt; else introT += adt / INTRO_DUR;
      const t = ease(Math.min(1, introT));
      const hdist = heroDistance();
      const b = INTRO.bearing + (HERO.bearing - INTRO.bearing) * t;
      const e = INTRO.elev + (HERO.elev - INTRO.elev) * t;
      const d = hdist * (INTRO.distMul + (1 - INTRO.distMul) * t);
      const tgt = tmpV.copy(introTarget).lerp(heroTarget, t);
      viewFromBearing(b, e, d, tgt, camera.position);
      camera.lookAt(tgt);
      if (introT >= 1) { endIntro(); lastInteract = now - 6000; }
      needsRender = true;
    }

    if (trans) {
      trans.t = Math.min(1, trans.t + adt / trans.dur);
      const k = ease(trans.t);
      applyPresetState(lerpState(trans.from, trans.to, k));
      if (!trans.midEnv && trans.t > 0.5) { trans.midEnv = true; regenEnv(); }
      if (trans.t >= 1) { Object.assign(cur, trans.to); trans = null; regenEnv(); }
    }

    if (glide) stepGlide(adt);
    if (U.uDim.value !== dimTarget) {
      const d = dimTarget - U.uDim.value;
      U.uDim.value = Math.abs(d) < 0.01 ? dimTarget : U.uDim.value + d * Math.min(1, adt * 7);
      needsRender = true;
    }

    if (phase === 'orbit' && !glide) {
      const idle = now - lastInteract > 6000;
      const want = autoOrbit && idle && !(selected && selected.pinned) && !pointer.down && !facMode && !(qcard && qcard.classList.contains('is-on'));
      orbitRamp = Math.max(0, Math.min(1, orbitRamp + (want ? dt / 2.5 : -dt / 0.4)));
      controls.autoRotate = orbitRamp > 0.001;
      controls.autoRotateSpeed = -0.32 * orbitRamp;
      controls.update(dt);
      if (controls.autoRotate) needsRender = true;
    }

    if (hoverDirty && phase === 'orbit' && !glide) {
      hoverDirty = false;
      if (selected && selected.pinned) {
        const th = pointer.inside ? hitTower(pointer.x, pointer.y) : null;
        const idx = pointer.inside ? pickFacing(pointer.x, pointer.y, th) : -1;
        setPreview(idx);
        root.classList.toggle('rbs--pointer', idx >= 0 || !!th);
      } else {
        const h = pointer.inside ? hitTower(pointer.x, pointer.y) : null;
        setHover(h ? { tower: h.tower, floor: h.floor } : null);
      }
    }
    if (selected && !selected.pinned && !hover && !labelHover && hoverLeaveAt && now - hoverLeaveAt > 650) {
      hoverLeaveAt = 0;
      clearFloor();
    }

    sky.position.copy(camera.position);
    const continuous = animateWater || controls.autoRotate || phase === 'intro' || !!trans || !!glide;
    if (needsRender || continuous) {
      render();
      needsRender = false;
      if (selected) placeLabel();
      placeQuarter();
      if (!firstFrameDone) {
        firstFrameDone = true;
        root.classList.add('rbs--live');
        if (!ctx.coarse) root.classList.add('rbs--grab');
        setTimeout(() => root.classList.add('rbs--settled'), 1000);
        ctx.onReady();
      }
    }

    perf.times.push(rawDt);
    let sum = 0;
    for (let i = perf.times.length - 1; i >= 0; i--) { sum += perf.times[i]; if (sum > 2) { perf.times.splice(0, i); break; } }
    perf.fps = perf.times.length / Math.max(0.001, perf.times.reduce((a, b) => a + b, 0));
    if (phase === 'orbit' && continuous && !trans) {
      if (perf.fps < 45 && !aoOn) perf.dprLowFor += dt; else perf.dprLowFor = 0;
      if (opts.adaptive && perf.dprLowFor > 2 && dpr > 1.0) {
        dpr = Math.max(1, Math.round((dpr - 0.25) * 100) / 100);
        renderer.setPixelRatio(dpr);
        resize();
        perf.dprLowFor = 0; perf.times.length = 0;
      }
      if (aoMode === 'auto' && !phone && !aoBlocked) {
        if (!aoOn) {
          perf.goodFor = perf.fps > 50 ? perf.goodFor + dt : 0;
          if (perf.goodFor > 2) { perf.goodFor = 0; perf.times.length = 0; enableAO(); }
        } else if (aoProbe) {
          const age = now - aoProbe;
          if (age < 600) perf.times.length = 0;
          else if (age > 2000 || (age > 1000 && perf.fps < 36)) {
            aoProbe = 0;
            if (perf.fps >= 50) aoFadeDir = 1;
            else { aoBlocked = true; disableAO(); perf.times.length = 0; }
          }
        } else {
          perf.badFor = perf.fps < 48 ? perf.badFor + dt : 0;
          if (perf.badFor > 1.5) { perf.badFor = 0; aoBlocked = true; aoFadeDir = -1; }
        }
      }
    }
    if (aoOn && aoFadeDir) {
      aoFade = Math.min(1, Math.max(0, aoFade + aoFadeDir * dt / 1.2));
      applyAOFade();
      if (aoFade >= 1 && aoFadeDir > 0) aoFadeDir = 0;
      if (aoFade <= 0 && aoFadeDir < 0) disableAO();
      needsRender = true;
    }
    if (opts.debug && statsEl) statsEl.textContent = statsText();

    rafId = requestAnimationFrame(frame);
  }

  function render() {
    renderer.info.reset();
    renderer.render(scene, camera);
    if (aoOn && post) {
      post.gtao.render(renderer, null, null);
      renderer.setRenderTarget(null);
      if (aoFade > 0) {
        const ac = renderer.autoClear;
        renderer.autoClear = false;
        renderer.render(post.quadScene, post.quadCam);
        renderer.autoClear = ac;
      }
    }
  }

  let statsEl = null;
  if (opts.debug) statsEl = el('div', 'rbs-stats', root);
  function statsText() {
    const s = api.stats();
    return `fps ${s.fps.toFixed(0)}  dpr ${s.dpr}\ncalls ${s.drawCalls}  tris ${s.trianglesDrawn}\nscene tris ${s.sceneTriangles}  ao ${s.ao ? 'on' : 'off'}`;
  }

  const compile = renderer.compileAsync ? renderer.compileAsync(scene, camera) : Promise.resolve();
  compile.catch(() => {}).then(() => { if (!disposedE) { lastT = performance.now(); kick(); } });

  const towerOf = (id) => TOWER_BY[String(id || '').toUpperCase()] || null;
  const api = {
    phase: () => phase,
    setPreset(k) {
      if (!PRESETS[k]) return;
      presetKey = k;
      const to = presetState(PRESETS[k]);
      if (reduced) { Object.assign(cur, to); applyPresetState(cur); regenEnv(); return; }
      const from = trans ? lerpState(trans.from, trans.to, ease(trans.t)) : lerpState(cur, cur, 0);
      trans = { from, to, t: 0, dur: 1.2, midEnv: false };
      kick();
    },
    selectFloor(n, tower) {
      const f = Math.round(Number(n));
      if (!(f >= 1 && f <= FLOORS)) return;
      if (phase === 'intro') endIntro();
      selectFloor(f, 'api', towerOf(tower));
      kick();
    },
    clearFloor() { clearFloor(); kick(); },
    setFacing(b) {
      const v = Number(b);
      if (!(selected && selected.pinned) || !Number.isFinite(v)) return null;
      const r = setFacingBearing(v, 'api');
      kick();
      return r;
    },
    clearFacing() { clearFacing(); kick(); },
    openQuarter(name) { const p = qpins.find((q) => q.it.name === name); if (p) openQuarterCard(p.it); return !!p; },
    focusPhase(ph) {
      const wasFac = facMode;
      facMode = ph === 'facilities' && fpins.length > 0;
      for (const p of fpins) p.off = !facMode;
      if (facMode) {
        for (const p of qpins) if (!p.hero) p.off = true;
        if (qcard) qcard.classList.remove('is-on');
        framedPhase = false;
        if (selected && selected.pinned) clearFloor();
        // the whole project in view from a little higher, from the south-west (the pool deck faces west): the deck, the
        // courtyard, the lobby and the penthouse terraces at once
        // the whole project, the towers' tops (the penthouses' pools) to the courtyard, from the south-west and a little higher
        const narrow = camera.aspect < 1;
        const tgt = localToWorld(MID.x - 10, TOP * 0.5, MID.z + 2, new THREE.Vector3());
        const vf = camera.fov * DEG, hf = 2 * Math.atan(Math.tan(vf / 2) * camera.aspect);
        const r = Math.max((TOP * 0.5 + 38) / Math.tan(vf / 2), (narrow ? 58 : 112) / Math.tan(hf / 2));
        const dir = new THREE.Vector3();
        viewFromBearing(236, 22, 1, new THREE.Vector3(), dir);
        const theta = Math.atan2(dir.x, dir.z);
        glideTo(tgt, r, (90 - 22) * DEG, theta, 1.1);
        placeQuarter();
        kick();
        return 'facilities';
      }
      if (wasFac) {
        for (const p of qpins) p.off = false;
        if (qcard) qcard.classList.remove('is-on');
        if (!ph) glideTo(heroTarget, heroDistance(), (90 - HERO.elev) * DEG, camSpherical().theta, 1.0);
      }
      const k = ['today', 'building', 'selling', 'permit'].includes(ph) ? ph : null;
      const groups = world.qGroups || {};
      for (const g in groups) for (const m of groups[g]) m.visible = !k || (k !== 'today' && g === k);
      for (const p of qpins) p.off = !!k && p.it.kind === 'project' && (k === 'today' || p.it.phase !== k);
      if (qcard && qcard.classList.contains('is-on') && qcard.dataset.phase && k && qcard.dataset.phase !== k) qcard.classList.remove('is-on');
      if (k && k !== 'today' && world.qGroups && world.qGroups[k]) {
        frameGroup(k);
        framedPhase = true;
      } else if (!k && framedPhase) {
        framedPhase = false;
        glideTo(heroTarget, heroDistance(), (90 - HERO.elev) * DEG, camSpherical().theta, 1.0, () => {
          controls.maxDistance = Math.max(1400, heroDistance() * 2.2);
        });
      }
      placeQuarter();
      kick();
      return k;
    },
    lookToward(name) { const p = qpins.find((q) => q.it.name === name); if (p) lookToward(p.it); return !!p; },
    /* the shared viewing room */
    getView: () => viewNow(),
    setView: (v, dur) => setViewFrom(v, dur),
    home: (dur) => {
      if (phase === 'intro') endIntro();
      lastInteract = performance.now();
      if (selected && selected.pinned) frameFloor(selected.tower, selected.floor, selected.floor, selected.tower);
      else glideTo(heroTarget, heroDistance(), (90 - HERO.elev) * DEG, camSpherical().theta, Number(dur) > 0 ? Number(dur) : 0);
      kick();
      return true;
    },
    pickPoint: (x, y) => pickPoint(Number(x), Number(y)),
    project: (p) => projectPoint(p),
    /* an example apartment: "N-25-w" (tower, floor, side) or "25-w" (the current tower); returns its id or null */
    selectUnit(id, source) {
      const m = /^(?:([NSns])-)?(\d+)-([a-z]+)$/.exec(String(id || ''));
      if (!m || !UNITS) return null;
      const TW = m[1] ? towerOf(m[1]) : (selected && selected.pinned ? selected.tower : lastTower);
      const f = Number(m[2]); const side = UNITS.sides.find((x) => x.id === m[3]);
      if (!TW || !side || !(f >= 1 && f <= FLOORS)) return null;
      if (phase === 'intro') endIntro();
      skipAuto = true;
      try { selectFloor(f, source === 'user' ? 'user' : 'api', TW); } finally { skipAuto = false; }
      setFacingBearing(side.bearing, source === 'user' ? 'user' : 'api');
      kick();
      return facing ? facing.unit : null;
    },
    getSelection() {
      if (!(selected && selected.pinned)) return null;
      return { tower: selected.tower.id, floor: selected.floor, heightM: heightOf(selected.floor), bearing: facing ? facing.bearing : null, unit: facing ? facing.unit : null };
    },
    getNorth() {
      const n = staticNorth(offset);
      n.cameraBearing = round1(trueBearing(sceneBearing(controls.target.x - camera.position.x, controls.target.z - camera.position.z)));
      return n;
    },
    setAutoOrbit(v) { autoOrbit = !!v && !reduced; },
    stats() {
      return {
        fps: perf.fps,
        dpr,
        ao: aoOn && !aoProbe && aoFade > 0,
        aoFade,
        aoState: aoBlocked ? 'blocked' : (aoLoading ? 'loading' : aoMode),
        drawCalls: renderer.info.render.calls,
        trianglesDrawn: renderer.info.render.triangles,
        sceneTriangles: world.triangles,
        meshes: world.meshCount,
        shadowMap: sun.shadow.mapSize.x,
      };
    },
    // dev helpers used by the checks
    _ringScreenPoint(bearing, f, tower) {
      const TW = towerOf(tower) || (selected ? selected.tower : TOWERS[0]);
      const fl = f || (selected ? selected.floor : 20);
      const side = unitFor(bearing);
      const r = TW.ring[idxForFacing(TW, bearing, side ? side.id : null)];
      const a = projectToStage(tmpV.set(r.x, ringY(fl), r.z));
      const rect = canvas.getBoundingClientRect();
      return { x: rect.left + a.x, y: rect.top + a.y, behind: a.behind };
    },
    _floorScreenPoint(f, tower) {
      const TW = towerOf(tower) || TOWERS[0];
      // the facade point of the tower facing the camera, at the floor's middle
      const toCam = new THREE.Vector3().subVectors(camera.position, TW.centerW).setY(0).normalize();
      const idx = idxByAngle(TW, sceneBearing(toCam.x, toCam.z));
      const r = TW.ring[idx];
      tmpV.set(r.fx + (r.x - r.fx) * 0.15, floorLevel(f) + FH * 0.5, r.fz + (r.z - r.fz) * 0.15);
      const a = projectToStage(tmpV);
      const rc = canvas.getBoundingClientRect();
      return { x: rc.left + a.x, y: rc.top + a.y, behind: a.behind };
    },
    _state() {
      const cs = camSpherical();
      return {
        gliding: !!glide, targetY: +controls.target.y.toFixed(2), dist: +cs.r.toFixed(1),
        tower: selected ? selected.tower.id : null, floor: selected ? selected.floor : null, pinned: !!(selected && selected.pinned),
        facing: facing ? { bearing: facing.bearing, unit: facing.unit } : null,
        dim: +U.uDim.value.toFixed(2), ring: TOWERS.map((X) => X.ringGroup.visible), arrow: arrow.visible, preview: arrowPrev.visible,
        facMode, framedPhase,
      };
    },
    _capture(w, h, quality = 0.9) {
      const pw = stageW, ph = stageH, pdpr = dpr;
      renderer.setPixelRatio(1);
      renderer.setSize(w, h, false);
      camera.aspect = w / h; camera.updateProjectionMatrix();
      if (post) post.gtao.setSize(w, h);
      render();
      const url = canvas.toDataURL('image/jpeg', quality);
      dpr = pdpr;
      renderer.setPixelRatio(dpr);
      resize();
      stageW = pw; stageH = ph;
      render();
      return url;
    },
    _debug() {
      const c = sun.shadow.camera;
      return { l: c.left, r: c.right, t: c.top, b: c.bottom, n: c.near, f: c.far, cam: camera.position.toArray().map((v) => +v.toFixed(1)), tgt: controls.target.toArray().map((v) => +v.toFixed(1)) };
    },
    _setAO(v) { if (v) { aoMode = 'on'; aoFade = 1; aoFadeDir = 0; aoProbe = 0; enableAO(); applyAOFade(); } else { aoMode = 'off'; disableAO(); } },
    /* a dev helper for the checks: look at a site-local point from a grid bearing, an elevation and a distance */
    _look(tx, ty, tz, bearing, elev, dist) {
      if (phase === 'intro') endIntro();
      const tgt = localToWorld(tx, ty, tz, new THREE.Vector3());
      viewFromBearing(bearing, elev, dist, tgt, camera.position);
      controls.target.copy(tgt);
      const md = controls.minDistance; controls.minDistance = Math.min(md, dist * 0.9);
      controls.update();
      lastInteract = performance.now();
      needsRender = true;
      kick();
    },
    _view(bearing, elev, distMul, ty) {
      if (phase === 'intro') endIntro();
      const tgt = heroTarget.clone();
      if (ty != null) tgt.y = ty;
      viewFromBearing(bearing, elev, heroDistance() * (distMul || 1), tgt, camera.position);
      controls.target.copy(tgt);
      controls.update();
      lastInteract = performance.now();
      needsRender = true;
      kick();
    },
    dispose() {
      disposedE = true;
      running = false;
      if (rafId) cancelAnimationFrame(rafId);
      rafId = 0;
      ro.disconnect();
      io.disconnect();
      for (const [t, type, fn, o] of listeners) t.removeEventListener(type, fn, o);
      controls.dispose();
      if (post) {
        post.gtao.dispose();
        post.blendMat.dispose();
        post.quad.geometry.dispose();
      }
      scene.traverse((o) => {
        if (o.geometry) o.geometry.dispose();
        if (o.material) (Array.isArray(o.material) ? o.material : [o.material]).forEach((m) => m.dispose());
      });
      envScene.traverse((o) => { if (o.geometry) o.geometry.dispose(); if (o.material) o.material.dispose(); });
      for (const p of world.towerProxies) p.geometry.dispose();
      for (const t of M.textures) t.dispose();
      envSkyScene.traverse((o) => { if (o.geometry) o.geometry.dispose(); if (o.material) o.material.dispose(); });
      if (envRT) envRT.dispose();
      if (envSkyRT) envSkyRT.dispose();
      pmrem.dispose();
      sun.shadow.map && sun.shadow.map.dispose();
      renderer.dispose();
      renderer.forceContextLoss();
      canvas.remove();
      if (statsEl) statsEl.remove();
      marks.textContent = '';
      leaderLine.setAttribute('visibility', 'hidden');
      leaderDot.setAttribute('visibility', 'hidden');
    },
  };
  return api;
}

/* ------------------------------------------------------------------------------------------ */
/* Shaders                                                                                     */
/* ------------------------------------------------------------------------------------------ */

const SKY_FN = /* glsl */`
vec3 rbsSky(vec3 d) {
  // guarded normalisation and clamping: no NaN where the view azimuth meets the sun azimuth
  vec2 az = d.xz; float al = length(az); az = al > 1e-5 ? az / al : vec2(1.0, 0.0);
  vec2 saz = uSunDir.xz; float sl = length(saz); saz = sl > 1e-5 ? saz / sl : vec2(1.0, 0.0);
  float toward = clamp(dot(az, saz) * 0.5 + 0.5, 0.0, 1.0);
  float h = clamp(d.y, 0.0, 1.0);
  // warm horizon all round, warmest under the sun, rising into a cooler zenith
  vec3 hor = mix(uSkyHorizon, uSkyWarm, pow(toward, uWarmPow));
  float k = smoothstep(0.0, 1.0, 1.0 - exp(-h * 3.6));
  vec3 col = mix(hor, uSkyZenith, k);
  // soft rose band opposite the sun, a few degrees above the horizon (the evening belt)
  float anti = pow(1.0 - toward, 1.3);
  float belt = smoothstep(0.0, 0.06, h) * (1.0 - smoothstep(0.12, 0.45, h));
  col = mix(col, uSkyRose, uRoseAmt * anti * belt);
  // the low sun: a wide warm halo, a softer inner glow and a small bright core (no hard disc)
  float sd = max(dot(d, uSunDir), 0.0);
  col += uSkyGlowCol * uSkyGlow * (0.14 * pow(sd, 6.0) + 0.32 * pow(sd, 48.0) + 1.1 * pow(sd, 1100.0));
  return col;
}
`;
const SKY_PARS = /* glsl */`
uniform vec3 uSkyZenith; uniform vec3 uSkyHorizon; uniform vec3 uSkyWarm; uniform vec3 uSkyGlowCol;
uniform vec3 uSkyRose; uniform float uRoseAmt;
uniform vec3 uSunDir; uniform float uSkyGlow; uniform float uWarmPow;
`;

function makeSkyMaterial(uniforms, envMode, groundU, zenU, horU) {
  const u = { ...uniforms };
  if (envMode) { u.uGroundEnv = groundU; u.uEnvZenith = zenU; u.uEnvHorizon = horU; }
  return new THREE.ShaderMaterial({
    uniforms: u,
    vertexShader: /* glsl */`
      varying vec3 vDir;
      void main() {
        vDir = (modelMatrix * vec4(position, 0.0)).xyz;
        vec4 p = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        gl_Position = p.xyww;
      }`,
    fragmentShader: /* glsl */`
      ${SKY_PARS}
      ${envMode ? 'uniform vec3 uGroundEnv; uniform vec3 uEnvZenith; uniform vec3 uEnvHorizon;' : ''}
      ${SKY_FN}
      varying vec3 vDir;
      void main() {
        vec3 d = normalize(vDir);
        vec3 c = rbsSky(d);
        ${envMode === 'fill' ? `
        {
          // lighting fill for the white model: cooler than the visible sky, warm towards the sun
          float h = clamp(d.y, 0.0, 1.0);
          vec3 fill = mix(uEnvHorizon, uEnvZenith, pow(h, 0.6));
          float sd = max(dot(d, uSunDir), 0.0);
          fill += uSkyGlowCol * uSkyGlow * (0.12 * pow(sd, 5.0) + 0.25 * pow(sd, 40.0));
          c = mix(fill, uGroundEnv, smoothstep(0.02, -0.25, d.y));
        }` : ''}
        ${envMode === 'sky' ? `
          // the visible sky itself, for reflections; the ground below the horizon
          c = mix(c, uGroundEnv, smoothstep(0.0, -0.2, d.y));
        ` : ''}
        gl_FragColor = vec4(c, 1.0);
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
      }`,
    side: THREE.BackSide,
    depthWrite: false,
  });
}

const FRAG_PARS = /* glsl */`
varying vec3 vRbsW;
#if defined(RBS_FLOOR) || defined(RBS_GLASS)
varying float vRbsF;
#endif
#ifdef RBS_GLASS
varying vec2 vRbsUv;
#endif
uniform float uTime;
${SKY_PARS}
uniform float uFogDensity;
uniform float uHiFloor; uniform float uHiTower; uniform vec3 uHiColor; uniform float uFloorY0; uniform float uFloorH;
uniform float uDim; uniform float uHiGlow;
#ifdef RBS_WATER
uniform vec4 uWater;
vec2 rbsW1(vec2 p, vec2 dir, float wl, float a, float t) {
  float k = 6.2831853 / wl;
  float ph = k * dot(dir, p) - sqrt(9.81 * k) * t;
  return dir * (a * k * cos(ph));
}
vec2 rbsWaveGrad(vec2 p, float t) {
  vec2 g = vec2(0.0);
  g += rbsW1(p, vec2(0.894, 0.447), 23.0, 0.10, t);
  g += rbsW1(p, vec2(0.600, -0.800), 13.0, 0.050, t);
  g += rbsW1(p, vec2(-0.316, 0.949), 7.5, 0.028, t);
  g += rbsW1(p, vec2(0.981, -0.196), 4.1, 0.010, t);
  return g;
}
#endif
#ifdef RBS_SEA
uniform vec4 uCoast; uniform vec3 uSeaShallow; uniform vec3 uSunTint; uniform float uSparkle;
float rbsHash(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
#endif
#ifdef RBS_GHOST
uniform float uGhostFade;
#endif
${SKY_FN}
`;

const FRAG_COLOR = /* glsl */`
float rbsHi = 0.0;
vec3 rbsNW = vec3(0.0, 1.0, 0.0);
#ifdef RBS_FLOOR
  {
    // DUO: a band's aFloor is tower * 100 + floor (the north tower 101-154, the south 201-254); -1 elsewhere
    float rbsTw = floor(vRbsF / 100.0 + 0.001);
    float rbsFl = vRbsF - rbsTw * 100.0;
    if (rbsTw > 0.5 && abs(rbsTw - uHiTower) < 0.5 && abs(rbsFl - uHiFloor) < 0.5) rbsHi = 1.0;
    else if (rbsTw > 0.5) diffuseColor.rgb *= 1.0 - 0.3 * uDim;
  }
#endif
#ifdef RBS_GLASS
  {
    float g = vRbsUv.x / 1.5;
    float w = fwidth(g);
    float d = abs(fract(g) - 0.5);
    float line = smoothstep(0.5 - max(w, 0.018) * 1.3, 0.5, d);
    float fadeL = 1.0 - smoothstep(0.12, 0.4, w);
    // a curtain wall: slim mullions, and a slightly deeper tone on every third pane (the facade's rhythm)
    float pane = mod(floor(g), 3.0);
    diffuseColor.rgb *= pane < 0.5 ? 0.9 : 1.0;
    diffuseColor.rgb = mix(diffuseColor.rgb, vec3(0.93, 0.92, 0.89), line * fadeL * 0.55);
    if (vRbsF > 0.5) {
      // DUO: a tower's glass carries its tower (1 north, 2 south); the floor comes from the height
      float fl = floor((vRbsW.y - uFloorY0) / uFloorH) + 1.0;
      if (abs(vRbsF - uHiTower) < 0.5 && abs(fl - uHiFloor) < 0.5) rbsHi = 0.62;
      else diffuseColor.rgb *= 1.0 - 0.35 * uDim;
    }
  }
#endif
if (rbsHi > 0.0) diffuseColor.rgb = mix(diffuseColor.rgb, uHiColor, rbsHi);
#ifdef RBS_SEA
  {
    float dc = dot(vRbsW.xz - uCoast.xy, uCoast.zw);
    diffuseColor.rgb = mix(uSeaShallow, diffuseColor.rgb, smoothstep(2.0, 150.0, dc));
  }
#endif
`;

const FRAG_NORMAL = /* glsl */`
#ifdef RBS_WATER
{
  vec2 g = rbsWaveGrad(vRbsW.xz * uWater.x, uTime) * uWater.y;
  float dist = length(vRbsW - cameraPosition);
  g *= 1.0 - smoothstep(uWater.z, uWater.w, dist);
  vec3 nW = normalize(vec3(-g.x, 1.0, -g.y));
  rbsNW = nW;
  normal = normalize((viewMatrix * vec4(nW, 0.0)).xyz);
}
#endif
`;

const FRAG_EMISSIVE = /* glsl */`
if (rbsHi > 0.0) totalEmissiveRadiance += uHiColor * (uHiGlow * rbsHi);
`;

const FRAG_FOG = /* glsl */`
#ifdef RBS_SEA
{
  // gentle sparkle towards the sun: every small water cell gets a slightly different facet,
  // only the facets that mirror the sun light up, and they twinkle a few times a second
  vec3 V = normalize(cameraPosition - vRbsW);
  vec2 cell = floor(vRbsW.xz * 0.6);
  float tick = floor(uTime * 2.2);
  vec3 jit = vec3(rbsHash(cell + tick * 0.37) - 0.5, 0.0, rbsHash(cell.yx + 11.3 + tick * 0.53) - 0.5) * 0.16;
  vec3 R = reflect(-V, normalize(rbsNW + jit));
  float s = max(dot(R, uSunDir), 0.0);
  float dist = length(vRbsW - cameraPosition);
  float fade = 1.0 - smoothstep(1400.0, 5200.0, dist);
  float path = pow(max(dot(reflect(-V, rbsNW), uSunDir), 0.0), 60.0);
  outgoingLight += uSunTint * uSparkle * fade * (pow(s, 1600.0) * 1.6 + path * 0.035);
}
#endif
{
  vec3 rv = vRbsW - cameraPosition;
  float rd = length(rv);
  vec3 rdir = rv / max(rd, 1e-3);
  // aerial haze: none on the site itself, growing with distance, full at the horizon
  float ff = 1.0 - exp(-max(0.0, rd - 650.0) * uFogDensity);
  ff *= mix(1.0, 0.55, clamp(vRbsW.y / 250.0, 0.0, 1.0));
  ff = max(ff, smoothstep(3800.0, 6800.0, rd));
  #ifdef RBS_GHOST
    ff = 1.0 - (1.0 - ff) * (1.0 - uGhostFade);
  #endif
  outgoingLight = mix(outgoingLight, rbsSky(rdir), clamp(ff, 0.0, 1.0));
}
`;

function patchMaterial(mat, key, flags, U) {
  mat.customProgramCacheKey = () => 'dus-' + key;
  mat.onBeforeCompile = (sh) => {
    for (const k in U) sh.uniforms[k] = U[k];
    if (flags.local) for (const k in flags.local) sh.uniforms[k] = flags.local[k];
    let defs = '';
    if (flags.floor) defs += '#define RBS_FLOOR\n';
    if (flags.glass) defs += '#define RBS_GLASS\n';
    if (flags.water) defs += '#define RBS_WATER\n';
    if (flags.sea) defs += '#define RBS_SEA\n';
    if (flags.ghost) defs += '#define RBS_GHOST\n';
    sh.vertexShader = defs + sh.vertexShader
      .replace('#include <common>', `#include <common>
varying vec3 vRbsW;
#if defined(RBS_FLOOR) || defined(RBS_GLASS)
attribute float aFloor;
varying float vRbsF;
#endif
#ifdef RBS_GLASS
varying vec2 vRbsUv;
#endif`)
      .replace('#include <project_vertex>', `#include <project_vertex>
{
  vec4 rbsWp = vec4(transformed, 1.0);
  #ifdef USE_INSTANCING
    rbsWp = instanceMatrix * rbsWp;
  #endif
  vRbsW = (modelMatrix * rbsWp).xyz;
}
#if defined(RBS_FLOOR) || defined(RBS_GLASS)
  vRbsF = aFloor;
#endif
#ifdef RBS_GLASS
  vRbsUv = uv;
#endif`);
    sh.fragmentShader = defs + sh.fragmentShader
      .replace('#include <common>', '#include <common>\n' + FRAG_PARS)
      .replace('#include <color_fragment>', '#include <color_fragment>\n' + FRAG_COLOR)
      .replace('#include <normal_fragment_maps>', '#include <normal_fragment_maps>\n' + FRAG_NORMAL)
      .replace('#include <emissivemap_fragment>', '#include <emissivemap_fragment>\n' + FRAG_EMISSIVE)
      .replace('#include <opaque_fragment>', FRAG_FOG + '\n#include <opaque_fragment>');
  };
}

function makeMaterials(U) {
  const std = (color, rough, extra = {}) => new THREE.MeshStandardMaterial({ color, roughness: rough, metalness: 0, ...extra });
  const white = std('#F2EEE6', 0.9);
  patchMaterial(white, 'white', { floor: true }, U);
  const glass = std('#4E6978', 0.05, { metalness: 0.28 });
  patchMaterial(glass, 'glass', { glass: true }, U);
  const ground = std('#FFFFFF', 0.97, { vertexColors: true });
  patchMaterial(ground, 'ground', {}, U);
  const foliage = std('#FFFFFF', 0.92, { vertexColors: true });
  patchMaterial(foliage, 'foliage', {}, U);
  const ghost = std('#BDC0BF', 0.95);
  patchMaterial(ghost, 'ghost', { ghost: true }, U);
  const pool = std('#5FB9C4', 0.05);
  patchMaterial(pool, 'pool', { water: true, local: { uWater: { value: new THREE.Vector4(2.6, 0.55, 250, 900) } } }, U);
  const sea = std('#245A6E', 0.06);
  patchMaterial(sea, 'sea', { water: true, sea: true, local: { uWater: { value: new THREE.Vector4(1.0, 0.7, 250, 1100) } } }, U);
  // DUO: the crown's screen and the facade's pilasters, a warm champagne bronze (the site's gold-brown, #8A6A2E, lifted)
  const bronze = std('#C2B292', 0.42, { metalness: 0.28 });
  patchMaterial(bronze, 'bronze', {}, U);

  // soft contact darkening under buildings (fake AO when GTAO is off)
  const blob = makeBlobTexture();
  const decal = new THREE.MeshBasicMaterial({ color: 0x1b2328, transparent: true, opacity: 0.2, alphaMap: blob, depthWrite: false, polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -2 });

  const all = [white, glass, ground, foliage, ghost, pool, sea, decal, bronze];
  return {
    white, glass, ground, foliage, ghost, pool, sea, decal, bronze, all,
    envWhiteList: [white, ground, foliage, ghost, bronze],
    envGlassList: [glass, pool, sea],
    textures: [blob],
  };
}

function makeBlobTexture() {
  const s = 128;
  const c = document.createElement('canvas');
  c.width = c.height = s;
  const g = c.getContext('2d');
  const img = g.createImageData(s, s);
  for (let y = 0; y < s; y++) {
    for (let x = 0; x < s; x++) {
      const u = (x + 0.5) / s * 2 - 1, v = (y + 0.5) / s * 2 - 1;
      // superellipse distance so the blob hugs rounded rectangles and capsules
      const d = Math.pow(Math.pow(Math.abs(u), 3) + Math.pow(Math.abs(v), 3), 1 / 3);
      const a = 1 - smooth(0.55, 1.0, d);
      const i = (y * s + x) * 4;
      img.data[i] = img.data[i + 1] = img.data[i + 2] = Math.round(a * a * 255);
      img.data[i + 3] = 255;
    }
  }
  g.putImageData(img, 0, 0);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.NoColorSpace;
  return t;
}
function smooth(a, b, x) { const t = Math.min(1, Math.max(0, (x - a) / (b - a))); return t * t * (3 - 2 * t); }

/* ------------------------------------------------------------------------------------------ */
/* Geometry helpers                                                                            */
/* ------------------------------------------------------------------------------------------ */

function newAcc(o = {}) {
  return { pos: [], nor: [], uv: o.uv ? [] : null, col: o.col ? [] : null, fl: o.fl ? [] : null, idx: [], n: 0, u: 0, v: 0, r: 1, g: 1, b: 1, f: -1 };
}
function V(a, x, y, z, nx, ny, nz) {
  a.pos.push(x, y, z);
  a.nor.push(nx, ny, nz);
  if (a.uv) a.uv.push(a.u, a.v);
  if (a.col) a.col.push(a.r, a.g, a.b);
  if (a.fl) a.fl.push(a.f);
  return a.n++;
}
function setCol(a, c) { a.r = c.r; a.g = c.g; a.b = c.b; }
function tri(a, i, j, k) {
  // orient so the geometric normal agrees with the vertex normals
  const P = a.pos, N = a.nor;
  const ex = P[j * 3] - P[i * 3], ey = P[j * 3 + 1] - P[i * 3 + 1], ez = P[j * 3 + 2] - P[i * 3 + 2];
  const fx = P[k * 3] - P[i * 3], fy = P[k * 3 + 1] - P[i * 3 + 1], fz = P[k * 3 + 2] - P[i * 3 + 2];
  const gx = ey * fz - ez * fy, gy = ez * fx - ex * fz, gz = ex * fy - ey * fx;
  const sx = N[i * 3] + N[j * 3] + N[k * 3], sy = N[i * 3 + 1] + N[j * 3 + 1] + N[k * 3 + 1], sz = N[i * 3 + 2] + N[j * 3 + 2] + N[k * 3 + 2];
  if (gx * sx + gy * sy + gz * sz >= 0) a.idx.push(i, j, k); else a.idx.push(i, k, j);
}
function quad(a, i, j, k, l) {
  const P = a.pos;
  // skip fully degenerate quads
  const d1 = Math.abs(P[i * 3] - P[k * 3]) + Math.abs(P[i * 3 + 1] - P[k * 3 + 1]) + Math.abs(P[i * 3 + 2] - P[k * 3 + 2]);
  const d2 = Math.abs(P[j * 3] - P[l * 3]) + Math.abs(P[j * 3 + 1] - P[l * 3 + 1]) + Math.abs(P[j * 3 + 2] - P[l * 3 + 2]);
  if (d1 < 1e-5 && d2 < 1e-5) return;
  tri(a, i, j, k);
  tri(a, i, k, l);
}
function toGeom(a) {
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(a.pos, 3));
  g.setAttribute('normal', new THREE.Float32BufferAttribute(a.nor, 3));
  if (a.uv) g.setAttribute('uv', new THREE.Float32BufferAttribute(a.uv, 2));
  if (a.col) g.setAttribute('color', new THREE.Float32BufferAttribute(a.col, 3));
  if (a.fl) g.setAttribute('aFloor', new THREE.Float32BufferAttribute(a.fl, 1));
  g.setIndex(a.n > 65535 ? new THREE.Uint32BufferAttribute(a.idx, 1) : new THREE.Uint16BufferAttribute(a.idx, 1));
  g.computeBoundingSphere();
  g.computeBoundingBox();
  return g;
}

function setNormals(pts) {
  const n = pts.length;
  let area = 0;
  for (let i = 0; i < n; i++) { const p = pts[i], q = pts[(i + 1) % n]; area += p.x * q.z - q.x * p.z; }
  const sgn = area > 0 ? 1 : -1;
  for (let i = 0; i < n; i++) {
    const a = pts[(i - 1 + n) % n], b = pts[(i + 1) % n];
    let tx = b.x - a.x, tz = b.z - a.z;
    const l = Math.hypot(tx, tz) || 1;
    tx /= l; tz /= l;
    pts[i].nx = sgn * tz;
    pts[i].nz = -sgn * tx;
  }
}
function perimeterOf(pts) {
  let L = 0;
  for (let i = 0; i < pts.length; i++) { const p = pts[i], q = pts[(i + 1) % pts.length]; L += Math.hypot(q.x - p.x, q.z - p.z); }
  return L;
}
/* resample a dense closed polyline to n points, spaced by arc length plus extra weight on turns */
function resampleLoop(P, n, curveWeight = 0) {
  const M = P.length;
  const len = new Float64Array(M), turn = new Float64Array(M);
  for (let i = 0; i < M; i++) { const a = P[i], b = P[(i + 1) % M]; len[i] = Math.hypot(b[0] - a[0], b[1] - a[1]); }
  for (let i = 0; i < M; i++) {
    const a = P[(i - 1 + M) % M], b = P[i], c = P[(i + 1) % M];
    let d = Math.atan2(c[1] - b[1], c[0] - b[0]) - Math.atan2(b[1] - a[1], b[0] - a[0]);
    d = Math.atan2(Math.sin(d), Math.cos(d));
    turn[i] = Math.abs(d);
  }
  const cumL = new Float64Array(M + 1), cumW = new Float64Array(M + 1);
  for (let i = 0; i < M; i++) {
    cumL[i + 1] = cumL[i] + len[i];
    cumW[i + 1] = cumW[i] + len[i] + curveWeight * 0.5 * (turn[i] + turn[(i + 1) % M]);
  }
  const L = cumL[M], W = cumW[M];
  const pts = [];
  let j = 0;
  for (let k = 0; k < n; k++) {
    const target = (k / n) * W;
    while (j < M - 1 && cumW[j + 1] < target) j++;
    const seg = cumW[j + 1] - cumW[j];
    const f = seg > 0 ? (target - cumW[j]) / seg : 0;
    const a = P[j], b = P[(j + 1) % M];
    pts.push({ x: a[0] + (b[0] - a[0]) * f, z: a[1] + (b[1] - a[1]) * f, s: (cumL[j] + len[j] * f) / L, nx: 0, nz: 0 });
  }
  setNormals(pts);
  return { pts, perimeter: L };
}
function offsetLoop(loop, d) {
  const pts = loop.pts.map((p) => ({ x: p.x + p.nx * d, z: p.z + p.nz * d, s: p.s, nx: p.nx, nz: p.nz }));
  return { pts, perimeter: perimeterOf(pts) };
}
function ellipsePoly(A, B, cx, cz, rot, M = 720) {
  const c = Math.cos(rot), s = Math.sin(rot), P = [];
  for (let i = 0; i < M; i++) {
    const t = (i / M) * Math.PI * 2;
    const x = A * Math.cos(t), z = B * Math.sin(t);
    P.push([cx + x * c - z * s, cz + x * s + z * c]);
  }
  return P;
}
function roundRectPoly(cx, cz, w, d, r, seg = 10) {
  const P = [];
  const hx = w / 2 - r, hz = d / 2 - r;
  const corners = [[hx, hz, 0], [-hx, hz, 90], [-hx, -hz, 180], [hx, -hz, 270]];
  for (const [ox, oz, a0] of corners) {
    for (let k = 0; k <= seg; k++) {
      const a = (a0 + (k / seg) * 90) * DEG;
      P.push([cx + ox + Math.cos(a) * r, cz + oz + Math.sin(a) * r]);
    }
  }
  return P;
}
/* a polygon with its corners eased by a short curve (d metres back along each side); the line is otherwise exact */
function easeCorners(P, d, seg = 6) {
  const out = [];
  for (let i = 0; i < P.length; i++) {
    const a = P[(i + P.length - 1) % P.length], b = P[i], c = P[(i + 1) % P.length];
    const la = Math.hypot(a[0] - b[0], a[1] - b[1]), lc = Math.hypot(c[0] - b[0], c[1] - b[1]);
    const ka = Math.min(d, la * 0.4) / la, kc = Math.min(d, lc * 0.4) / lc;
    const p0 = [b[0] + (a[0] - b[0]) * ka, b[1] + (a[1] - b[1]) * ka], p2 = [b[0] + (c[0] - b[0]) * kc, b[1] + (c[1] - b[1]) * kc];
    for (let k = 0; k <= seg; k++) {
      const t = k / seg, u = 1 - t;
      out.push([u * u * p0[0] + 2 * u * t * b[0] + t * t * p2[0], u * u * p0[1] + 2 * u * t * b[1] + t * t * p2[1]]);
    }
  }
  return out;
}
function rotatePoly(P, cx, cz, rot) {
  const c = Math.cos(rot), s = Math.sin(rot);
  return P.map(([x, z]) => [cx + (x - cx) * c - (z - cz) * s, cz + (x - cx) * s + (z - cz) * c]);
}
/* curved capsule: a quadratic Bezier centreline offset by w/2 with round ends */
function capsulePoly(p0, p1, p2, w, M = 48) {
  const C = [], Tn = [];
  for (let i = 0; i <= M; i++) {
    const t = i / M, u = 1 - t;
    C.push([u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0], u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1]]);
    const tx = 2 * u * (p1[0] - p0[0]) + 2 * t * (p2[0] - p1[0]), tz = 2 * u * (p1[1] - p0[1]) + 2 * t * (p2[1] - p1[1]);
    const l = Math.hypot(tx, tz) || 1;
    Tn.push([tx / l, tz / l]);
  }
  const h = w / 2, P = [];
  for (let i = 0; i <= M; i++) P.push([C[i][0] - Tn[i][1] * h, C[i][1] + Tn[i][0] * h]);
  const capSeg = 18;
  {
    const e = C[M], t = Tn[M];
    const a0 = Math.atan2(t[0], -t[1]);
    for (let k = 1; k < capSeg; k++) { const a = a0 - (k / capSeg) * Math.PI; P.push([e[0] + Math.cos(a) * h, e[1] + Math.sin(a) * h]); }
  }
  for (let i = M; i >= 0; i--) P.push([C[i][0] + Tn[i][1] * h, C[i][1] - Tn[i][0] * h]);
  {
    const e = C[0], t = Tn[0];
    const b0 = Math.atan2(-t[0], t[1]);
    for (let k = 1; k < capSeg; k++) { const a = b0 - (k / capSeg) * Math.PI; P.push([e[0] + Math.cos(a) * h, e[1] + Math.sin(a) * h]); }
  }
  return P;
}

const C45 = Math.SQRT1_2;
/* A floor band: balcony floor, rounded parapet, rounded slab edge and soffit, swept along the
   outer edge. depthFn(s) gives the balcony depth from the glass line at arc position s. */
function addBand(a, loop, y, depthFn, prof) {
  const n = loop.pts.length;
  const out = new Array(n);
  for (let i = 0; i < n; i++) {
    const p = loop.pts[i];
    const D = depthFn(p.s, i);
    out[i] = { x: p.x + p.nx * D, z: p.z + p.nz * D, s: p.s, nx: 0, nz: 0 };
  }
  setNormals(out);
  const { Hp, Ts, tp, rb } = prof;
  const inset = prof.inset ?? 0.3;
  const rt = tp / 2;
  const strips = [];
  if (!prof.noFloor) strips.push([['i', 0, 0, 0, 1], ['o', -tp, 0, 0, 1]]);
  strips.push([
    ['o', -tp, 0, -1, 0], ['o', -tp, Hp - rt, -1, 0], ['o', -rt, Hp, 0, 1], ['o', 0, Hp - rt, 1, 0],
    ['o', 0, -Ts + rb, 1, 0], ['o', -rb * (1 - C45), -Ts + rb * (1 - C45), C45, -C45], ['o', -rb, -Ts, 0, -1],
    ['i', 0, -Ts, 0, -1],
  ]);
  for (const strip of strips) {
    const m = strip.length, base = a.n;
    for (let i = 0; i < n; i++) {
      const p = loop.pts[i], o = out[i];
      for (const [k, u, v, nu, nv] of strip) {
        let px, pz, Nx, Nz;
        if (k === 'i') { px = p.x - p.nx * inset; pz = p.z - p.nz * inset; Nx = p.nx; Nz = p.nz; }
        else { px = o.x + o.nx * u; pz = o.z + o.nz * u; Nx = o.nx; Nz = o.nz; }
        const nl = Math.hypot(Nx * nu, nv, Nz * nu) || 1;
        V(a, px, y + v, pz, (Nx * nu) / nl, nv / nl, (Nz * nu) / nl);
      }
    }
    for (let i = 0; i < n; i++) {
      const i2 = (i + 1) % n;
      for (let j = 0; j < m - 1; j++) quad(a, base + i * m + j, base + i2 * m + j, base + i2 * m + j + 1, base + i * m + j + 1);
    }
  }
  return out;
}
/* vertical wall along a loop (glass cores, plinths) */
function addWall(a, loop, y0, y1) {
  const n = loop.pts.length, base = a.n;
  for (let i = 0; i <= n; i++) {
    const p = loop.pts[i % n];
    const s = (i === n ? 1 : p.s) * loop.perimeter;
    a.u = s; a.v = y0; V(a, p.x, y0, p.z, p.nx, 0, p.nz);
    a.u = s; a.v = y1; V(a, p.x, y1, p.z, p.nx, 0, p.nz);
  }
  for (let i = 0; i < n; i++) quad(a, base + 2 * i, base + 2 * i + 2, base + 2 * i + 3, base + 2 * i + 1);
}
/* flat cap filling a loop */
function addCap(a, loop, y, up = true) {
  const contour = loop.pts.map((p) => new THREE.Vector2(p.x, p.z));
  const tris = THREE.ShapeUtils.triangulateShape(contour, []);
  const base = a.n;
  for (const p of loop.pts) V(a, p.x, y, p.z, 0, up ? 1 : -1, 0);
  for (const t of tris) tri(a, base + t[0], base + t[1], base + t[2]);
}
/* loop object straight from a polygon (no resampling) */
function loopFromPoly(P) {
  const pts = P.map(([x, z]) => ({ x, z, s: 0, nx: 0, nz: 0 }));
  const L = perimeterOf(pts);
  let acc = 0;
  for (let i = 0; i < pts.length; i++) {
    pts[i].s = acc / L;
    const q = pts[(i + 1) % pts.length];
    acc += Math.hypot(q.x - pts[i].x, q.z - pts[i].z);
  }
  setNormals(pts);
  return { pts, perimeter: L };
}
/* wall with one flat normal per segment (crisp on straight sides) */
function addWallFlat(a, loop, y0, y1) {
  const n = loop.pts.length;
  let s = 0;
  for (let i = 0; i < n; i++) {
    const p = loop.pts[i], q = loop.pts[(i + 1) % n];
    let nx = q.z - p.z, nz = -(q.x - p.x);
    const l = Math.hypot(nx, nz) || 1;
    nx /= l; nz /= l;
    if (nx * (p.nx + q.nx) + nz * (p.nz + q.nz) < 0) { nx = -nx; nz = -nz; }
    const b = a.n;
    a.u = s; a.v = y0; V(a, p.x, y0, p.z, nx, 0, nz);
    a.u = s + l; a.v = y0; V(a, q.x, y0, q.z, nx, 0, nz);
    a.u = s + l; a.v = y1; V(a, q.x, y1, q.z, nx, 0, nz);
    a.u = s; a.v = y1; V(a, p.x, y1, p.z, nx, 0, nz);
    quad(a, b, b + 1, b + 2, b + 3);
    s += l;
  }
}
/* slab: flat walls + top cap (plates, plinth, decks, lawns) */
function addSlab(a, poly, y0, y1) {
  const loop = loopFromPoly(poly);
  addWallFlat(a, loop, y0, y1);
  addCap(a, loop, y1, true);
  return loop;
}
/* ghost volume: a box, sometimes with a set-back top storey */
function addGhost(a, cx, cz, w, d, y0, y1, rnd) {
  const h = y1 - y0;
  if (h > 14 && rnd() < 0.55) {
    const top = 3.4;
    addBox(a, cx, cz, w, d, y0, y1 - top, 0);
    const sx = w > d ? 0.7 : 0.82, sz = w > d ? 0.82 : 0.7;
    addBox(a, cx + (rnd() - 0.5) * w * 0.12, cz + (rnd() - 0.5) * d * 0.12, w * sx, d * sz, y1 - top, y1, 0);
  } else addBox(a, cx, cz, w, d, y0, y1, 0);
}
/* box prism rotated around its centre */
function addBox(a, cx, cz, w, d, y0, y1, rot = 0) {
  const P = rotatePoly([[cx - w / 2, cz - d / 2], [cx + w / 2, cz - d / 2], [cx + w / 2, cz + d / 2], [cx - w / 2, cz + d / 2]], cx, cz, rot);
  const corners = P.map(([x, z]) => ({ x, z }));
  // walls with hard edges
  for (let i = 0; i < 4; i++) {
    const p = corners[i], q = corners[(i + 1) % 4];
    let nx = q.z - p.z, nz = -(q.x - p.x);
    const l = Math.hypot(nx, nz); nx /= l; nz /= l;
    // make sure the normal points away from the centre
    const mx = (p.x + q.x) / 2 - cx, mz = (p.z + q.z) / 2 - cz;
    if (nx * mx + nz * mz < 0) { nx = -nx; nz = -nz; }
    const b = a.n;
    V(a, p.x, y0, p.z, nx, 0, nz); V(a, q.x, y0, q.z, nx, 0, nz); V(a, q.x, y1, q.z, nx, 0, nz); V(a, p.x, y1, p.z, nx, 0, nz);
    quad(a, b, b + 1, b + 2, b + 3);
  }
  const b = a.n;
  for (const p of corners) V(a, p.x, y1, p.z, 0, 1, 0);
  quad(a, b, b + 1, b + 2, b + 3);
}
/* append a three.js geometry transformed by a matrix */
function addGeometry(a, geom, matrix) {
  const nm = new THREE.Matrix3().getNormalMatrix(matrix);
  const pos = geom.attributes.position, nor = geom.attributes.normal;
  const base = a.n;
  const v = new THREE.Vector3(), nn = new THREE.Vector3();
  for (let i = 0; i < pos.count; i++) {
    v.fromBufferAttribute(pos, i).applyMatrix4(matrix);
    nn.fromBufferAttribute(nor, i).applyMatrix3(nm).normalize();
    V(a, v.x, v.y, v.z, nn.x, nn.y, nn.z);
  }
  if (geom.index) { const ix = geom.index.array; for (let i = 0; i < ix.length; i += 3) a.idx.push(base + ix[i], base + ix[i + 1], base + ix[i + 2]); }
  else for (let i = 0; i < pos.count; i += 3) a.idx.push(base + i, base + i + 1, base + i + 2);
}

function mulberry32(seed) {
  let s = seed >>> 0;
  return function () {
    s = (s + 0x6D2B79F5) >>> 0;
    let t = s;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/* ------------------------------------------------------------------------------------------ */
/* World                                                                                       */
/* ------------------------------------------------------------------------------------------ */

/* the penthouse terraces' private pools (licensing decision 21.9.2025: "the private pools moved on 49-50"): which terrace
   is not public; here floor 49 at the north-west corner and floor 50 at the south-west corner of each tower (illustration) */
function phPools(TW) {
  const P = TW.poly.slice().sort((a, b) => a[0] - b[0]);
  const w2 = [P[0], P[1]].sort((a, b) => a[1] - b[1]);
  const NW = w2[0], SW = w2[1];
  const L = Math.hypot(SW[0] - NW[0], SW[1] - NW[1]);
  const tx = (SW[0] - NW[0]) / L, tz = (SW[1] - NW[1]) / L;
  let nx = tz, nz = -tx;
  if (nx > 0) { nx = -nx; nz = -nz; } // the west face's outward normal
  return [
    { f: 49, cx: NW[0] + tx * 4.0, cz: NW[1] + tz * 4.0, ux: tx, uz: tz, nx, nz },
    { f: 50, cx: SW[0] - tx * 4.0, cz: SW[1] - tz * 4.0, ux: tx, uz: tz, nx, nz },
  ];
}

function buildWorld(site, M, U, quarter, city) {
  const col = (h) => new THREE.Color(h);
  const C = {
    base: col('#D3CFC7'), road: col('#BDB8AF'), plate: col('#DDD9D1'), plinth: col('#EEEAE3'), paving: col('#E2DDD3'),
    outline: col('#B7AE9F'), lawn: col('#BCC6AE'), park: col('#C5CDB7'), green: col('#C0C9AF'), sand: col('#EADDC3'),
    prom: col('#E8E2D6'), tree: col('#BEC6B5'), treeDark: col('#AEB8A6'), planter: col('#4A6651'), trunk: col('#C8C0B2'),
    roofGarden: col('#A9B597'), deck: col('#E6DAC6'), court: col('#E4DED3'), step: col('#EBE6DD'), stone: col('#E9E4DA'),
    lounger: col('#F4F0E8'),
  };
  const rnd = mulberry32(20260928);

  const white = newAcc({ fl: true });
  const glass = newAcc({ uv: true, fl: true });
  const bronze = newAcc();
  const ground = newAcc({ col: true });
  const foliage = newAcc({ col: true });
  const trunks = newAcc({ col: true });
  const ghosts = newAcc();
  const farAcc = newAcc();
  const qmassBy = { building: newAcc(), selling: newAcc(), permit: newAcc() };
  const water = newAcc();
  const sea = newAcc();
  const decals = newAcc({ uv: true });
  white.f = -1; glass.f = 0;
  const Y = PLOT.h;
  const planterSpots = [];
  const trees0 = [];

  /* ---------- the coast (city.json: a straight fit through the city's beach polygons' sea edge) ---------- */
  const cst = city && city.coast && Number.isFinite(Number(city.coast.x0)) ? { x0: Number(city.coast.x0), k: Number(city.coast.k) || 0 } : { x0: -1422, k: -0.053 };
  const xc = (z) => cst.x0 + cst.k * z;
  const ZA = -7000, ZB = 7000;

  /* ---------- ground: the land (with the sunken courtyard cut out), the beach, the promenade and the sea ---------- */
  setCol(ground, C.base);
  const courtHole = [[COURT.x0, COURT.z0], [COURT.x1, COURT.z0], [COURT.x1, COURT.z1], [COURT.x0, COURT.z1]];
  addPolyCap(ground, [[xc(ZA), ZA], [7000, ZA], [7000, ZB], [xc(ZB), ZB]], [courtHole], 0);
  const strip = (d0, d1, y, c) => {
    setCol(ground, c);
    addPolyCap(ground, [[xc(ZA) + d0, ZA], [xc(ZA) + d1, ZA], [xc(ZB) + d1, ZB], [xc(ZB) + d0, ZB]], [], y);
    const b2 = ground.n;
    V(ground, xc(ZA) + d0, 0, ZA, -1, 0, 0); V(ground, xc(ZA) + d0, y, ZA, -1, 0, 0); V(ground, xc(ZB) + d0, y, ZB, -1, 0, 0); V(ground, xc(ZB) + d0, 0, ZB, -1, 0, 0);
    quad(ground, b2, b2 + 1, b2 + 2, b2 + 3);
  };
  strip(0, 42, 0.12, C.sand);
  strip(42, 56, 0.45, C.prom);
  {
    const b = sea.n;
    V(sea, -12000, -0.3, -12000, 0, 1, 0); V(sea, xc(-12000) + 6, -0.3, -12000, 0, 1, 0); V(sea, xc(12000) + 6, -0.3, 12000, 0, 1, 0); V(sea, -12000, -0.3, 12000, 0, 1, 0);
    quad(sea, b, b + 1, b + 2, b + 3);
  }

  /* ---------- the city as it stands (city.json): plan lots, green areas, streets, buildings, trees ---------- */
  const ptsOf = (a, k) => { const P = []; for (let i = k; i + 1 < a.length; i += 2) P.push([a[i], a[i + 1]]); return P; };
  const inPoly = (x, z, L) => {
    let c = false;
    for (let i = 0, j = L.length - 1; i < L.length; j = i++) {
      const [xi, zi] = L[i], [xj, zj] = L[j];
      if ((zi > z) !== (zj > z) && x < ((xj - xi) * (z - zi)) / (zj - zi) + xi) c = !c;
    }
    return c;
  };
  const planLots = [];
  if (city) {
    for (const s of city.s || []) {                       // streets: the city's axes, a drawing width by road class
      const P = ptsOf(s, 2);
      if (P.length < 2) continue;
      setCol(ground, C.road);
      addRibbon(ground, P, Number(s[0]) || 10, 0.05);
    }
    for (const l of city.lots || []) {                    // the Somail plans' lots (GIS 837)
      const poly = ptsOf(l, 2);
      if (poly.length < 3) continue;
      setCol(ground, l[0] === 'park' ? C.park : C.plate);
      addSlab(ground, poly, 0, l[0] === 'park' ? 0.22 : 0.3);
      planLots.push(poly);
    }
    for (const g of city.g || []) {                       // green areas (GIS 503)
      const poly = ptsOf(g, 1);
      if (poly.length < 3) continue;
      setCol(ground, C.green);
      addSlab(ground, poly, 0, 0.26);
    }
    for (const b of city.b || []) {                       // the buildings standing today (GIS 513), at their heights
      const poly = ptsOf(b, 3);
      if (poly.length >= 3 && b[0] > 0) addSlab(ghosts, poly, 0, b[0]);
    }
    const f = city.f || [];                               // the far city, each building as its box, to the sea
    for (let i = 0; i + 5 < f.length; i += 6) addBox(farAcc, f[i], f[i + 1], Math.max(2, f[i + 2]), Math.max(2, f[i + 3]), 0, f[i + 5], f[i + 4] * DEG);
  }
  // our other projects nearby (quarter.json): pale schematic masses at their floors' height (the card says so)
  const qProj = [];
  if (quarter && Array.isArray(quarter.projects)) {
    const cg = Math.cos(GRID_ANGLE), sg = Math.sin(GRID_ANGLE);
    for (const p of quarter.projects) {
      const X = Number(p.x) || 0, Z = Number(p.z) || 0;
      qProj.push({ lx: X * cg - Z * sg, lz: X * sg + Z * cg, floors: Number(p.floors) || 10, phase: String(p.phase || 'permit') });
    }
  }
  for (const q of qProj) {
    const h = Math.max(12, q.floors * 3.3 + 4);
    if (!planLots.some((L) => inPoly(q.lx, q.lz, L))) { setCol(ground, C.plate); addSlab(ground, roundRectPoly(q.lx, q.lz, 64, 52, 8, 6), 0, 0.55); }
    const qa = qmassBy[q.phase] || qmassBy.permit;
    if (q.floors >= 20) { addBox(qa, q.lx, q.lz, 25, 25, 0.55, h, 0); addBox(qa, q.lx - 6, q.lz + 16, 40, 13, 0.55, 20, 0); }
    else addBox(qa, q.lx, q.lz, 44, 26, 0.55, h, 0);
  }

  /* ---------- DUO's lot: the plinth (the courtyard cut out), its engraved line, the paving ---------- */
  const lotPoly = easeCorners(LOT_OUTLINE, 1.6, 6);
  setCol(ground, C.plinth);
  {
    const loop = loopFromPoly(lotPoly);
    addWallFlat(ground, loop, 0, Y);
    addPolyCap(ground, lotPoly, [courtHole], Y);
    setCol(ground, C.outline);
    addLoopRibbon(ground, offsetLoop(loop, -0.9), 0.26, Y + 0.012);
  }
  // paving joints every 6 m across the plaza (clipped to the lot, left off over the courtyard)
  setCol(ground, C.paving);
  {
    const inCourt = (x, z) => x > COURT.x0 - 0.2 && x < COURT.x1 + 0.2 && z > COURT.z0 - 0.2 && z < COURT.z1 + 0.2;
    const segs = (fixed, along) => { // a line x = fixed (along z) or z = fixed (along x), split into inside runs
      const out = []; let cur = null;
      for (let t = -60; t <= 60; t += 0.5) {
        const x = along === 'z' ? fixed : t, z = along === 'z' ? t : fixed;
        const ok = inPoly(x, z, LOT_OUTLINE) && !inCourt(x, z);
        if (ok && !cur) cur = [t, t];
        else if (ok) cur[1] = t;
        else if (cur) { out.push(cur); cur = null; }
      }
      if (cur) out.push(cur);
      return out;
    };
    for (let x = -39; x <= 42; x += 6) for (const [a, b] of segs(x, 'z')) if (b - a > 1) addRibbon(ground, [[x, a + 0.6], [x, b - 0.6]], 0.09, Y + 0.011);
    for (let z = -45; z <= 48; z += 6) for (const [a, b] of segs(z, 'x')) if (b - a > 1) addRibbon(ground, [[a + 0.6, z], [b - 0.6, z]], 0.09, Y + 0.011);
  }

  /* ---------- the sunken courtyard (west half; its shape and place an illustration) ---------- */
  {
    const F = COURT.floor;
    setCol(ground, C.court);
    addPolyCap(ground, courtHole, [], F);
    // the stone walls, facing into the courtyard
    const inward = loopFromPoly(courtHole);
    for (const p of inward.pts) { p.nx = -p.nx; p.nz = -p.nz; }
    white.f = -1;
    addWallFlat(white, inward, F, Y);
    // the lower level's shop fronts (glass), on the long sides, just in front of the stone
    const g0 = loopFromPoly([[COURT.x0 + 0.12, COURT.z0 + 0.12], [COURT.x1 - 0.12, COURT.z0 + 0.12], [COURT.x1 - 0.12, COURT.z1 - 0.12], [COURT.x0 + 0.12, COURT.z1 - 0.12]]);
    for (const p of g0.pts) { p.nx = -p.nx; p.nz = -p.nz; }
    glass.f = 0;
    addWallFlat(glass, g0, F + 0.3, Y - 1.1);
    // a canopy ledge over the shop fronts, and a glass balustrade around the edge up top
    addBox(white, COURT.x0 + 0.55, (COURT.z0 + COURT.z1) / 2, 1.1, COURT.z1 - COURT.z0, Y - 1.25, Y - 0.95, 0);
    addBox(white, COURT.x1 - 0.55, (COURT.z0 + COURT.z1) / 2, 1.1, COURT.z1 - COURT.z0, Y - 1.25, Y - 0.95, 0);
    const rail = offsetLoop(loopFromPoly(courtHole), 0.3);
    glass.f = 0;
    addWall(glass, rail, Y, Y + 1.05);
    addBand(white, rail, Y + 1.0, () => 0.02, { Hp: 0.06, Ts: 0.06, tp: 0.08, rb: 0.02, noFloor: true, inset: 0 });
    // wide steps down at the south end, and two escalators beside them (the plan names escalators around the patio)
    const n = 26, rise = (Y - F) / n, run = 0.34, sx0 = COURT.x0 + 1.5, sw = 7.5;
    setCol(ground, C.step);
    for (let i = 0; i < n; i++) {
      const zz = COURT.z1 - (n - i) * run;
      addBox(ground, sx0 + sw / 2, (zz + COURT.z1) / 2, sw, COURT.z1 - zz, F, F + (i + 1) * rise, 0);
    }
    const len = Math.hypot(n * run, Y - F), ang = Math.atan2(Y - F, n * run);
    const esc = new THREE.BoxGeometry(1.25, 0.55, len);
    for (const ex of [sx0 + sw + 1.1, sx0 + sw + 2.8]) {
      const m = new THREE.Matrix4().makeTranslation(ex, (F + Y) / 2 + 0.25, COURT.z1 - (n * run) / 2).multiply(new THREE.Matrix4().makeRotationX(-ang));
      addGeometry(white, esc, m);
    }
    esc.dispose();
    // planters with trees on the courtyard floor
    for (const [px, pz] of [[-13, -15], [-20, -3], [-11, 5], [-19, 12]]) {
      addBox(white, px, pz, 2.6, 2.6, F, F + 0.55, 0);
      setCol(ground, C.roofGarden); addBox(ground, px, pz, 2.2, 2.2, F + 0.55, F + 0.6, 0);
      trees0.push({ x: px, z: pz, y: F + 0.6, r: 1.9 + rnd() * 0.5, dark: rnd() < 0.4 });
    }
  }

  /* ---------- the two towers ---------- */
  const bandProf = { Ts: 0.46, rb: 0.1 };
  for (const TW of TOWERS) {
    const fp = easeCorners(TW.poly, 1.4, 5);
    const loop = resampleLoop(fp, 136, 4);
    const lobbyL = offsetLoop(loop, -1.7);
    const pentL = offsetLoop(loop, -2.2);
    const techL = offsetLoop(loop, -3.2);
    // balconies (the marketing's "wide sun balconies"; their layout is not public): deep around the corners, a sun balcony in
    // the middle of the west and east faces, a slab edge elsewhere
    const xs = TW.poly.map((p) => p[0]).slice().sort((a, b) => a - b);
    const wMid = { x: (xs[0] + xs[1]) / 2, z: TW.cz }, eMid = { x: (xs[2] + xs[3]) / 2, z: TW.cz };
    const D = loop.pts.map((p) => {
      let dc = 1e9;
      for (const c of TW.poly) dc = Math.min(dc, Math.hypot(p.x - c[0], p.z - c[1]));
      const corner = 1 - smooth(5.8, 8.6, dc);
      const onWE = Math.abs(p.nx) > 0.85;
      const dm = onWE ? Math.min(Math.hypot(p.x - wMid.x, p.z - wMid.z), Math.hypot(p.x - eMid.x, p.z - eMid.z)) : 1e9;
      const mid = 1 - smooth(4.2, 5.6, dm);
      return 0.42 + 1.95 * Math.max(corner, mid * 0.82);
    });
    const Dp = D.map((d) => d + 2.2);
    // the ground floor: tall recessed glass (the lobby, about 7 m) behind slim columns
    glass.f = 0;
    addWall(glass, lobbyL, Y, Y0);
    {
      const colG = new THREE.CylinderGeometry(0.42, 0.42, Y0 - Y - 0.45, 12, 1, true);
      const step = Math.max(1, Math.round(loop.pts.length / 18));
      for (let i = 0; i < loop.pts.length; i += step) {
        const p = loop.pts[i];
        addGeometry(white, colG, new THREE.Matrix4().makeTranslation(p.x - p.nx * 0.2, (Y + Y0 - 0.45) / 2, p.z - p.nz * 0.2));
      }
      colG.dispose();
    }
    // the residential floors: a curtain wall with glass balustrades on every floor plate
    glass.f = TW.k;
    addWall(glass, loop, Y0 - 0.5, floorLevel(PH_FROM));
    addWall(glass, pentL, floorLevel(PH_FROM) - 0.5, TW.roof);
    for (let f = 1; f <= FLOORS; f++) {
      const ph = f >= PH_FROM;
      white.f = TW.k * 100 + f;
      addPlate(white, glass, ph ? pentL : loop, floorLevel(f), ph ? Dp : D, bandProf, 1.05);
    }
    // the roof of floor 50, the technical floors 51-52 set back, and a crown screen of bronze fins at the glass line
    white.f = TW.k * 100 + 51;
    addPlate(white, glass, pentL, TW.roof, Dp.map((d) => d * 0.35 + 0.4), { Ts: 0.6, rb: 0.12 }, 0);
    white.f = -1;
    addWall(white, techL, TW.roof, TW.roof + 2 * TECH_H);
    addCap(white, techL, TW.roof + 2 * TECH_H, true);
    {
      const finG = new THREE.BoxGeometry(0.16, TW.top - TW.roof - 0.4, 0.95);
      const per = loop.perimeter, nF = Math.round(per / 1.25);
      for (let k = 0; k < nF; k++) {
        const p = loop.pts[Math.floor((k / nF) * loop.pts.length)];
        const m = new THREE.Matrix4().makeRotationY(Math.atan2(p.nx, p.nz));
        m.setPosition(p.x + p.nx * 0.2, (TW.roof + TW.top) / 2 + 0.2, p.z + p.nz * 0.2);
        addGeometry(bronze, finG, m);
      }
      finG.dispose();
      addBand(white, offsetLoop(loop, 0.35), TW.top - 0.5, () => 0.3, { Hp: 0.5, Ts: 0.4, tp: 0.26, rb: 0.1, inset: 0, noFloor: true });
    }
    // the private pools on the penthouse terraces (floors 49 and 50)
    for (const pp of phPools(TW)) {
      const y = floorLevel(pp.f) + 0.02;
      const rot = Math.atan2(pp.uz, pp.ux);
      addPoolRot(water, white, pp.cx, pp.cz, 4.0, 2.2, 0.4, y, rot);
    }
    // a soft contact shadow under the tower
    decal(TW.cx, TW.cz, 44, 46, 0, Y + 0.02);
  }

  /* ---------- the lobby building between the towers and the pool deck on its roof ---------- */
  {
    const L = LOBBY;
    const xW = Math.min(L[0][0], L[3][0]), xE = Math.max(L[1][0], L[2][0]), zN = Math.max(L[0][1], L[1][1]), zS = Math.min(L[2][1], L[3][1]);
    glass.f = 0;
    const gl = loopFromPoly([[xW + 0.8, zN], [xE - 0.8, zN], [xE - 0.8, zS], [xW + 0.8, zS]]);
    addWallFlat(glass, gl, Y, DECK_Y - 1.0);
    // the roof slab with a thin overhang, the deck on top
    white.f = -1;
    addSlab(white, [[xW - 0.6, zN], [xE + 0.6, zN], [xE + 0.6, zS], [xW - 0.6, zS]], DECK_Y - 1.0, DECK_Y);
    setCol(ground, C.deck);
    addSlab(ground, [[xW - 0.4, zN + 0.2], [xE + 0.4, zN + 0.2], [xE + 0.4, zS - 0.2], [xW - 0.4, zS - 0.2]], DECK_Y, DECK_Y + 0.06);
    // glass balustrades along the open west and east edges
    for (const x of [xW - 0.45, xE + 0.45]) {
      const bl = { pts: [{ x, z: zN + 0.3, s: 0, nx: x < 10 ? -1 : 1, nz: 0 }, { x, z: zS - 0.3, s: 1, nx: x < 10 ? -1 : 1, nz: 0 }], perimeter: zS - zN };
      addWallOpen(glass, bl, DECK_Y + 0.06, DECK_Y + 1.15);
      addBox(white, x, (zN + zS) / 2, 0.12, zS - zN - 0.6, DECK_Y + 1.1, DECK_Y + 1.2, 0);
    }
    // the infinity pool along the west edge (its edge open to the west), the toddler pool, loungers, a shade pergola
    addPoolEdge(water, white, POOL.cx, POOL.cz, POOL.w, POOL.d, 0.5, DECK_Y + 0.07, 'w');
    addPoolEdge(water, white, KIDPOOL.cx, KIDPOOL.cz, KIDPOOL.w, KIDPOOL.d, 0.8, DECK_Y + 0.07, '');
    setCol(ground, C.lounger);
    for (let z = POOL.cz - POOL.d / 2 + 1.5; z <= POOL.cz + POOL.d / 2 - 1.2; z += 2.35) {
      addBox(ground, POOL.cx + POOL.w / 2 + 2.3, z, 1.9, 0.78, DECK_Y + 0.06, DECK_Y + 0.42, 0);
    }
    {
      const px0 = 21.5, px1 = 29.8, pz0 = -3.5, pz1 = 12.5, top = DECK_Y + 3.3;
      white.f = -1;
      for (let x = px0; x <= px1 + 0.01; x += 0.75) addBox(white, x, (pz0 + pz1) / 2, 0.14, pz1 - pz0, top - 0.3, top, 0);
      for (const [x, z] of [[px0, pz0], [px1, pz0], [px0, pz1], [px1, pz1], [px0, (pz0 + pz1) / 2], [px1, (pz0 + pz1) / 2]]) addBox(white, x, z, 0.26, 0.26, DECK_Y + 0.06, top - 0.3, 0);
      addBox(white, (px0 + px1) / 2, pz0, px1 - px0 + 0.3, 0.2, top - 0.5, top - 0.3, 0);
      addBox(white, (px0 + px1) / 2, pz1, px1 - px0 + 0.3, 0.2, top - 0.5, top - 0.3, 0);
      setCol(ground, C.lounger);
      for (let z = pz0 + 2; z < pz1 - 1; z += 3.2) { addBox(ground, 24.2, z, 1.6, 1.6, DECK_Y + 0.06, DECK_Y + 0.8, 0); addBox(ground, 27.4, z, 1.6, 1.6, DECK_Y + 0.06, DECK_Y + 0.8, 0); }
    }
    // planters on the deck's north and south ends, by the towers
    for (const z of [zN + 1.6, zS - 1.6]) for (let x = xW + 3; x < xE - 2; x += 3.2) planterSpots.push({ x, z, y: DECK_Y + 0.06, nx: 0, nz: z < 0 ? -1 : 1, big: false, roof: true });
    decal((xW + xE) / 2, (zN + zS) / 2, xE - xW + 8, zS - zN + 6, 0, Y + 0.02);
  }

  /* ---------- the three commercial buildings in the west half (their shapes and places an illustration) ---------- */
  for (const R of RETAIL) {
    const fp = easeCorners(R.poly, 1.2, 4);
    const loop = resampleLoop(fp, 64, 3);
    const hTop = Y + R.floors * RETAIL_FH;
    glass.f = 0;
    addWall(glass, offsetLoop(loop, -1.4), Y, Y + RETAIL_FH);          // shop fronts under the first floor's overhang
    addWall(glass, loop, Y + RETAIL_FH - 0.3, hTop - 0.2);
    white.f = -1;
    for (let f = 2; f <= R.floors; f++) addBand(white, loop, Y + (f - 1) * RETAIL_FH, () => 0.55, { Hp: 0.95, Ts: 0.55, tp: 0.2, rb: 0.1 });
    // vertical fins on the upper floors (a commercial rhythm)
    {
      const finG = new THREE.BoxGeometry(0.14, hTop - Y - RETAIL_FH - 0.6, 0.6);
      const nF = Math.round(loop.perimeter / 2.4);
      for (let k = 0; k < nF; k++) {
        const p = loop.pts[Math.floor((k / nF) * loop.pts.length)];
        const m = new THREE.Matrix4().makeRotationY(Math.atan2(p.nx, p.nz));
        m.setPosition(p.x + p.nx * 0.2, (Y + RETAIL_FH + hTop) / 2 + 0.3, p.z + p.nz * 0.2);
        addGeometry(white, finG, m);
      }
      finG.dispose();
    }
    addBand(white, loop, hTop, () => 0.35, { Hp: 0.9, Ts: 0.6, tp: 0.26, rb: 0.12 });
    addCap(white, loop, hTop + 0.02, true);
    const garden = offsetLoop(loop, -2.2);
    setCol(ground, C.roofGarden);
    addWall(ground, garden, hTop, hTop + 0.3);
    addCap(ground, garden, hTop + 0.3, true);
    if (R.roof) { addBox(white, (R.poly[0][0] + R.poly[1][0]) / 2, 0, 5.2, 16, hTop, hTop + 3.2, 0); }
    for (let k = 0; k < 6; k++) {
      const p = garden.pts[Math.floor(((k + 0.5) / 6) * garden.pts.length)];
      planterSpots.push({ x: p.x, z: p.z, y: hTop + 0.3, nx: p.nx, nz: p.nz, big: false, roof: true });
    }
    const cx = R.poly.reduce((s, p) => s + p[0], 0) / 4, cz = R.poly.reduce((s, p) => s + p[1], 0) / 4;
    const w = Math.abs(R.poly[1][0] - R.poly[0][0]), d = Math.abs(R.poly[2][1] - R.poly[1][1]);
    decal(cx, cz, w + 8, d + 8, 0, Y + 0.02);
  }

  /* ---------- planters ---------- */
  {
    const bush = new THREE.IcosahedronGeometry(1, 1);
    const m = new THREE.Matrix4(), q = new THREE.Quaternion(), s = new THREE.Vector3(), p = new THREE.Vector3();
    for (const sp of planterSpots) {
      setCol(foliage, C.planter);
      q.setFromAxisAngle(new THREE.Vector3(0, 1, 0), Math.atan2(sp.nx, sp.nz));
      s.set(sp.big ? 1.8 : 1.3, sp.big ? 0.75 : 0.6, sp.big ? 1.1 : 0.85);
      p.set(sp.x, sp.y + 0.5, sp.z);
      m.compose(p, q, s);
      addGeometry(foliage, bush, m);
    }
    bush.dispose();
  }

  /* ---------- trees: the city's own (GIS 628, real positions) and a few on the plaza (illustration) ---------- */
  const trees = trees0;
  for (let z = -22; z <= 22; z += 7.3) trees.push({ x: -3.2, z, y: Y, r: 2.0 + rnd() * 0.5, dark: rnd() < 0.3 });
  for (let z = -40; z <= 44; z += 9.4) trees.push({ x: 40.6, z, y: Y, r: 1.9 + rnd() * 0.5, dark: rnd() < 0.3 });
  if (city && Array.isArray(city.t)) {
    for (let i = 0; i + 1 < city.t.length; i += 2) trees.push({ x: city.t[i], z: city.t[i + 1], y: 0.05, r: 2.0 + rnd() * 1.3, dark: rnd() < 0.45 });
  }
  {
    const canopy = new THREE.SphereGeometry(1, 7, 5);
    const trunk = new THREE.CylinderGeometry(0.13, 0.18, 1, 5, 1, true);
    const m = new THREE.Matrix4(), q = new THREE.Quaternion(), s = new THREE.Vector3(), p = new THREE.Vector3();
    for (const t of trees) {
      const h = t.r * 1.25;
      setCol(trunks, C.trunk);
      m.compose(p.set(t.x, t.y + h * 0.5, t.z), q.identity(), s.set(1, h, 1));
      addGeometry(trunks, trunk, m);
      setCol(foliage, t.dark ? C.treeDark : C.tree);
      q.setFromAxisAngle(new THREE.Vector3(0, 1, 0), rnd() * 6.28);
      m.compose(p.set(t.x, t.y + h + t.r * 0.75, t.z), q, s.set(t.r, t.r * 0.86, t.r));
      addGeometry(foliage, canopy, m);
    }
    canopy.dispose(); trunk.dispose();
  }

  /* ---------- meshes ---------- */
  const meshes = [];
  const add = (acc, mat, cast, receive, name) => {
    if (!acc.n) return null;
    const mesh = new THREE.Mesh(toGeom(acc), mat);
    mesh.castShadow = cast; mesh.receiveShadow = receive; mesh.name = name;
    mesh.matrixAutoUpdate = false;
    site.add(mesh); meshes.push(mesh);
    return mesh;
  };
  add(ground, M.ground, true, true, 'ground');
  add(sea, M.sea, false, false, 'sea');
  add(ghosts, M.ghost, true, true, 'ghosts');
  add(farAcc, M.ghost, false, true, 'far-city');
  add(white, M.white, true, true, 'white');
  add(glass, M.glass, true, true, 'glass');
  add(bronze, M.bronze, true, true, 'bronze');
  add(foliage, M.foliage, true, true, 'foliage');
  add(trunks, M.foliage, false, true, 'trunks');
  add(water, M.pool, false, true, 'pools');
  const dm = add(decals, M.decal, false, false, 'decals');
  if (dm) dm.renderOrder = 2;
  const QTINT = { building: ['#D6E3E7', 0.34, '#1F4B5C', 0.55], selling: ['#F4EAD4', 0.32, '#9C7A3C', 0.7], permit: ['#F1ECE2', 0.28, '#8E8676', 0.62] };
  const qGroups = {};
  for (const k in qmassBy) {
    if (!qmassBy[k].n) continue;
    const [fc, fo, ec, eo] = QTINT[k];
    const qg = toGeom(qmassBy[k]);
    const qm = new THREE.Mesh(qg, new THREE.MeshBasicMaterial({ color: fc, transparent: true, opacity: fo, depthWrite: false }));
    qm.name = 'quarter-masses-' + k; qm.renderOrder = 3; qm.matrixAutoUpdate = false;
    const qe = new THREE.LineSegments(new THREE.EdgesGeometry(qg, 30), new THREE.LineBasicMaterial({ color: ec, transparent: true, opacity: eo }));
    qe.name = 'quarter-edges-' + k; qe.renderOrder = 3; qe.matrixAutoUpdate = false;
    site.add(qm); site.add(qe); meshes.push(qm);
    qGroups[k] = [qm, qe];
  }
  site.updateMatrixWorld(true);
  meshes.forEach((m) => m.updateMatrix());

  // picking proxies, one per tower (layer 1 only, never rendered): the residential floors, a little outside the balconies
  const towerProxies = [];
  for (const TW of TOWERS) {
    const acc = newAcc();
    const P = TW.poly.map(([x, z]) => { const dx = x - TW.cx, dz = z - TW.cz, l = Math.hypot(dx, dz) || 1; return [x + (dx / l) * 3.2, z + (dz / l) * 3.2]; });
    addSlab(acc, P, Y0 - 0.6, TW.roof + 0.4);
    const mesh = new THREE.Mesh(toGeom(acc), new THREE.MeshBasicMaterial({ side: THREE.DoubleSide }));
    mesh.layers.set(1);
    mesh.userData.tower = TW;
    site.add(mesh);
    mesh.updateMatrixWorld(true);
    towerProxies.push(mesh);
  }

  let triangles = 0;
  for (const m of meshes) triangles += m.geometry.index.count / 3;
  return { towerProxies, triangles, meshCount: meshes.length, qGroups, coast: cst, labels: city && Array.isArray(city.labels) ? city.labels : [] };

  /* local helpers (hoisted) */
  function decal(cx, cz, w, d, rot, y) {
    const c = Math.cos(rot), s = Math.sin(rot), b = decals.n;
    for (const [u, v] of [[-1, -1], [1, -1], [1, 1], [-1, 1]]) {
      const x = u * w / 2, z = v * d / 2;
      decals.u = (u + 1) / 2; decals.v = (v + 1) / 2;
      V(decals, cx + x * c - z * s, y, cz + x * s + z * c, 0, 1, 0);
    }
    quad(decals, b, b + 1, b + 2, b + 3);
  }
}

/* a flat cap over a polygon, with holes (the land around the courtyard, the plinth) */
function addPolyCap(a, P, holes, y) {
  const contour = P.map(([x, z]) => new THREE.Vector2(x, z));
  const hs = (holes || []).map((H) => H.map(([x, z]) => new THREE.Vector2(x, z)));
  const tris = THREE.ShapeUtils.triangulateShape(contour, hs);
  const base = a.n;
  for (const v of contour) V(a, v.x, y, v.y, 0, 1, 0);
  for (const H of hs) for (const v of H) V(a, v.x, y, v.y, 0, 1, 0);
  for (const t of tris) tri(a, base + t[0], base + t[1], base + t[2]);
}
/* an open wall along a polyline (one normal per point) */
function addWallOpen(a, loop, y0, y1) {
  const n = loop.pts.length, base = a.n;
  let s = 0;
  for (let i = 0; i < n; i++) {
    const p = loop.pts[i];
    if (i) s += Math.hypot(p.x - loop.pts[i - 1].x, p.z - loop.pts[i - 1].z);
    a.u = s; a.v = y0; V(a, p.x, y0, p.z, p.nx, 0, p.nz);
    a.u = s; a.v = y1; V(a, p.x, y1, p.z, p.nx, 0, p.nz);
  }
  for (let i = 0; i < n - 1; i++) quad(a, base + 2 * i, base + 2 * i + 2, base + 2 * i + 3, base + 2 * i + 1);
}
/* a floor plate with a glass balustrade: the slab (its floor, its rounded edge and its soffit) in white, grown out by the
   balcony depth D[i] at each point of the loop; the balustrade (hb metres, 0 for none) on the plate's outer line in glass */
function addPlate(white, glassAcc, loop, y, D, prof, hb) {
  const n = loop.pts.length;
  const out = new Array(n);
  for (let i = 0; i < n; i++) {
    const p = loop.pts[i], d = D[i];
    out[i] = { x: p.x + p.nx * d, z: p.z + p.nz * d, s: p.s, nx: 0, nz: 0 };
  }
  setNormals(out);
  const Ts = prof.Ts, rb = prof.rb, inset = 0.3;
  const strip = [['i', 0, 0, 0, 1], ['o', -0.02, 0, 0, 1], ['o', 0, -rb * 0.5, 1, 0], ['o', 0, -Ts + rb, 1, 0], ['o', -rb * (1 - C45), -Ts + rb * (1 - C45), C45, -C45], ['o', -rb, -Ts, 0, -1], ['i', 0, -Ts, 0, -1]];
  const m = strip.length, base = white.n;
  for (let i = 0; i < n; i++) {
    const p = loop.pts[i], o = out[i];
    for (const [k, u, v, nu, nv] of strip) {
      let px, pz, Nx, Nz;
      if (k === 'i') { px = p.x - p.nx * inset; pz = p.z - p.nz * inset; Nx = p.nx; Nz = p.nz; }
      else { px = o.x + o.nx * u; pz = o.z + o.nz * u; Nx = o.nx; Nz = o.nz; }
      const nl = Math.hypot(Nx * nu, nv, Nz * nu) || 1;
      V(white, px, y + v, pz, (Nx * nu) / nl, nv / nl, (Nz * nu) / nl);
    }
  }
  for (let i = 0; i < n; i++) {
    const i2 = (i + 1) % n;
    for (let j = 0; j < m - 1; j++) quad(white, base + i * m + j, base + i2 * m + j, base + i2 * m + j + 1, base + i * m + j + 1);
  }
  if (hb > 0) {
    const gb = glassAcc.n;
    let s = 0;
    for (let i = 0; i <= n; i++) {
      const o = out[i % n];
      if (i) { const q = out[(i - 1) % n]; s += Math.hypot(o.x - q.x, o.z - q.z); }
      glassAcc.u = s; glassAcc.v = y; V(glassAcc, o.x - o.nx * 0.06, y, o.z - o.nz * 0.06, o.nx, 0, o.nz);
      glassAcc.u = s; glassAcc.v = y + hb; V(glassAcc, o.x - o.nx * 0.06, y + hb, o.z - o.nz * 0.06, o.nx, 0, o.nz);
    }
    for (let i = 0; i < n; i++) quad(glassAcc, gb + 2 * i, gb + 2 * i + 2, gb + 2 * i + 3, gb + 2 * i + 1);
  }
  return out;
}
/* a pool whose coping is left off along one side (the infinity edge): 'w' leaves the west side open */
function addPoolEdge(water, white, cx, cz, w, d, r, y, edge) {
  const poly = roundRectPoly(cx, cz, w, d, r, 8);
  const loop = loopFromPoly(poly);
  addCap(water, loop, y + 0.03, true);
  const outer = offsetLoop(loop, 0.45);
  const n = loop.pts.length, base = white.n;
  white.f = -1;
  for (let i = 0; i < n; i++) {
    const p = loop.pts[i], o = outer.pts[i];
    V(white, p.x, y + 0.09, p.z, 0, 1, 0);
    V(white, o.x, y + 0.09, o.z, 0, 1, 0);
  }
  for (let i = 0; i < n; i++) {
    const j = (i + 1) % n;
    if (edge === 'w' && loop.pts[i].x < cx - w / 2 + 0.35 && loop.pts[j].x < cx - w / 2 + 0.35) continue;
    quad(white, base + 2 * i, base + 2 * j, base + 2 * j + 1, base + 2 * i + 1);
  }
  const wallBase = white.n;
  for (let i = 0; i < n; i++) {
    const p = loop.pts[i];
    V(white, p.x, y + 0.0, p.z, -p.nx, 0, -p.nz);
    V(white, p.x, y + 0.09, p.z, -p.nx, 0, -p.nz);
  }
  for (let i = 0; i < n; i++) { const j = (i + 1) % n; quad(white, wallBase + 2 * i, wallBase + 2 * j, wallBase + 2 * j + 1, wallBase + 2 * i + 1); }
}
/* a small pool turned with its terrace (the penthouses' private pools) */
function addPoolRot(water, white, cx, cz, len, wid, r, y, rot) {
  const P = rotatePoly(roundRectPoly(cx, cz, wid, len, r, 6), cx, cz, rot + Math.PI / 2);
  const loop = loopFromPoly(P);
  addCap(water, loop, y + 0.05, true);
  const outer = offsetLoop(loop, 0.3);
  const n = loop.pts.length, base = white.n;
  white.f = -1;
  for (let i = 0; i < n; i++) { const p = loop.pts[i], o = outer.pts[i]; V(white, p.x, y + 0.1, p.z, 0, 1, 0); V(white, o.x, y + 0.1, o.z, 0, 1, 0); }
  for (let i = 0; i < n; i++) { const j = (i + 1) % n; quad(white, base + 2 * i, base + 2 * j, base + 2 * j + 1, base + 2 * i + 1); }
}

/* ribbon along an open polyline (paths) */
function addRibbon(a, P, w, y) {
  const n = P.length, base = a.n;
  for (let i = 0; i < n; i++) {
    const p = P[Math.max(0, i - 1)], q = P[Math.min(n - 1, i + 1)];
    let tx = q[0] - p[0], tz = q[1] - p[1];
    const l = Math.hypot(tx, tz) || 1; tx /= l; tz /= l;
    V(a, P[i][0] - tz * w / 2, y, P[i][1] + tx * w / 2, 0, 1, 0);
    V(a, P[i][0] + tz * w / 2, y, P[i][1] - tx * w / 2, 0, 1, 0);
  }
  for (let i = 0; i < n - 1; i++) quad(a, base + 2 * i, base + 2 * i + 2, base + 2 * i + 3, base + 2 * i + 1);
}
/* ribbon along a closed loop */
function addLoopRibbon(a, loop, w, y) {
  const n = loop.pts.length, base = a.n;
  for (const p of loop.pts) {
    V(a, p.x - p.nx * w / 2, y, p.z - p.nz * w / 2, 0, 1, 0);
    V(a, p.x + p.nx * w / 2, y, p.z + p.nz * w / 2, 0, 1, 0);
  }
  for (let i = 0; i < n; i++) { const j = (i + 1) % n; quad(a, base + 2 * i, base + 2 * j, base + 2 * j + 1, base + 2 * i + 1); }
}
/* pool: water surface slightly below the deck, with a white coping ring */
function addPool(water, white, cx, cz, w, d, r, y, infinity) {
  const poly = roundRectPoly(cx, cz, w, d, r, 8);
  const loop = loopFromPoly(poly);
  // water sits flush with the deck (the deck slab below stays closed), framed by a thin coping
  addCap(water, loop, y + 0.03, true);
  const outer = offsetLoop(loop, 0.45);
  const n = loop.pts.length, base = white.n;
  white.f = -1;
  for (let i = 0; i < n; i++) {
    const p = loop.pts[i], o = outer.pts[i];
    V(white, p.x, y + 0.09, p.z, 0, 1, 0);
    V(white, o.x, y + 0.09, o.z, 0, 1, 0);
  }
  for (let i = 0; i < n; i++) {
    const j = (i + 1) % n;
    // leave the coping off along the infinity edge (the side facing +z, towards the courtyard's open south-west)
    if (infinity) {
      const pz = loop.pts[i].z;
      if (pz > cz + d / 2 - 0.35) continue;
    }
    quad(white, base + 2 * i, base + 2 * j, base + 2 * j + 1, base + 2 * i + 1);
  }
  // inner edge wall of the coping (catches light, frames the water)
  const wallBase = white.n;
  for (let i = 0; i < n; i++) {
    const p = loop.pts[i];
    V(white, p.x, y + 0.0, p.z, -p.nx, 0, -p.nz);
    V(white, p.x, y + 0.09, p.z, -p.nx, 0, -p.nz);
  }
  for (let i = 0; i < n; i++) { const j = (i + 1) % n; quad(white, wallBase + 2 * i, wallBase + 2 * j, wallBase + 2 * j + 1, wallBase + 2 * i + 1); }
}
