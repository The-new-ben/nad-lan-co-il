/*
 * Rainbow Tel Aviv, 3D stage (illustrative architect's white model at golden hour).
 *
 *   import { mountRainbowStage } from './stage.js';
 *   const stage = mountRainbowStage(document.getElementById('x'), { preset: 'sunset' });
 *   stage.dispose();
 *
 * The page needs an import map for "three" and "three/addons/" (three@0.170.0 on jsDelivr).
 * three.js is loaded lazily, so the poster shows before any 3D code is downloaded.
 * The floor button dispatches: window CustomEvent('nl:floor', { detail: { floor } }).
 */

let THREE = null;
let OrbitControls = null;

const DEG = Math.PI / 180;

const TEXT = {
  sunset: 'שקיעה',
  noon: 'צהריים',
  presets: 'תאורה',
  caption: 'הדמיה להמחשה בלבד, על בסיס מקורות פומביים. אינה תוכנית מכר.',
  floor: (n) => `קומה ${n}`,
  // one project-wide fact for every floor: the marketing gives 2 to 5 rooms for the project, not per floor
  low: 'בפרויקט דירות 2 עד 5 חדרים, לפי פרסומי השיווק',
  high: 'בפרויקט דירות 2 עד 5 חדרים, לפי פרסומי השיווק',
  penthouse: 'קומות הפנטהאוז, לפי פרסומי השיווק',
  cta: 'לקבלת פרטים על הקומה',
  open3d: 'סיור וירטואלי בפרויקט',
  hint: 'בחרו קומה במגדל',
  close: 'סגירה',
  aria: 'הדמיה של פרויקט ריינבו תל אביב, מגדל ובנייני בוטיק סביב גינה',
};

const DEFAULTS = {
  preset: 'sunset',
  poster: null,          // URL of the poster image; defaults to poster.jpg next to stage.js
  injectCss: true,       // adds stage.css (next to stage.js) once per page
  injectFonts: true,     // adds Assistant + Noto Serif Hebrew from Google Fonts if missing
  force3D: false,        // skip the weak-device and software-renderer fallback
  ao: 'auto',            // 'auto' | 'on' | 'off'
  autoOrbit: true,
  intro: true,
  highFloorsFrom: 21,    // floors from this number up use the "high floors" line
  penthouseFloors: 3,    // top N floors are labelled as penthouses
  hint: true,
  adaptive: true,        // lower the pixel ratio automatically when frames get slow
  wheel: 'engaged',      // 'engaged': mouse-wheel zoom only after a click or drag on the stage (page scroll is never hijacked); 'always'
  toneMapping: 'aces',   // 'aces' | 'agx'
  text: null,            // override any of the Hebrew strings
  debug: false,
};

/* Light presets. Colours are sRGB hex, converted to linear at runtime. */
const PRESETS = {
  sunset: {
    sunAz: 250, sunEl: 17, sunColor: '#FFCD9C', sunI: 7.0,
    hemiSky: '#9FB6CC', hemiGround: '#CDB08A', hemiI: 0.2,
    envWhite: 0.5, envGlass: 1.0,
    zenith: '#DEDAD2', horizon: '#E5E3DE', warm: '#F0AE7E', glowCol: '#FFC78A', glow: 1.15, warmPow: 3.0, skyGain: 1.02,
    rose: '#E8D2CB', roseAmt: 0.5,
    envZenith: '#AFC3D6', envHorizon: '#E6DCCF',
    groundEnv: '#BFAE95',
    sea: '#1F5A70', seaShallow: '#5E9FA2',
    exposure: 0.95, fog: 1 / 3300,
  },
  noon: {
    sunAz: 158, sunEl: 60, sunColor: '#FFF4E6', sunI: 3.9,
    hemiSky: '#BFD2E2', hemiGround: '#D8CFC0', hemiI: 0.2,
    envWhite: 0.42, envGlass: 1.0,
    zenith: '#B7CEE0', horizon: '#E2E8EB', warm: '#EFEBE3', glowCol: '#FFFFFF', glow: 0.2, warmPow: 2.0, skyGain: 1.05,
    rose: '#E2E8EB', roseAmt: 0.0,
    envZenith: '#A9C3DA', envHorizon: '#E0E6E8',
    groundEnv: '#CFC6B6',
    sea: '#236D8E', seaShallow: '#6DB4B7',
    exposure: 0.8, fog: 1 / 3600,
  },
};

/* Site-local layout (metres). Local -z points to the quarter's grid north, which is turned
   20 degrees east of true north, like the Tel Aviv coast. The sea is to the local west. */
const GRID_ANGLE = -20 * DEG;
const PLOT = { hx: 52, hz: 40, r: 9, h: 1.2 };
const TOWER = { cx: -30, cz: -4, rot: 98 * DEG, A: 16.5, B: 10.8, y0: 7.2, fh: 3.35, floors: 40 };
TOWER.roof = TOWER.y0 + TOWER.floors * TOWER.fh;
const BLOCK_W = 12.5;
const BLOCKS = [
  { p0: [-13.75, -28.5], p1: [-5, -33.5], p2: [3.75, -28.5], floors: 9, ph: 0.3 },
  { p0: [24.25, -28.5], p1: [33.5, -33.5], p2: [42.75, -28.5], floors: 8, ph: 1.7 },
  { p0: [41, -7.75], p1: [46, 1], p2: [41, 9.75], floors: 9, ph: 2.9 },
  { p0: [27.25, 28.5], p1: [35, 33.5], p2: [42.75, 28.5], floors: 8, ph: 4.1 },
  { p0: [-8.75, 28.5], p1: [-0.5, 33.5], p2: [7.75, 28.5], floors: 9, ph: 5.3 },
  { p0: [-42.75, 28.5], p1: [-35.5, 33.5], p2: [-28.25, 28.5], floors: 8, ph: 0.9 },
];
const COAST_X = -172;          // waterline (local x)
const PITCH_X = 128, PITCH_Z = 104;

let cssInjected = false;
function ensureCss() {
  if (cssInjected || document.querySelector('link[data-rbs-css]')) { cssInjected = true; return; }
  const l = document.createElement('link');
  l.rel = 'stylesheet';
  l.href = new URL('./stage.css', import.meta.url).href;
  l.setAttribute('data-rbs-css', '');
  document.head.appendChild(l);
  cssInjected = true;
}
function ensureFonts() {
  const has = [...document.querySelectorAll('link[href*="fonts.googleapis.com"]')].some((l) => /Assistant/.test(l.href) && /Noto\+Serif\+Hebrew/.test(l.href));
  if (has || document.querySelector('link[data-rbs-fonts]')) return;
  const l = document.createElement('link');
  l.rel = 'stylesheet';
  l.href = 'https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700&family=Noto+Serif+Hebrew:wght@500;600&display=swap';
  l.setAttribute('data-rbs-fonts', '');
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
    // the browser may also flag a major performance caveat (e.g. GPU blocklisted)
    const c2 = document.createElement('canvas');
    const gl2 = c2.getContext('webgl2', { failIfMajorPerformanceCaveat: true });
    out.fast = !!gl2;
    if (gl2) { const e2 = gl2.getExtension('WEBGL_lose_context'); if (e2) e2.loseContext(); }
  } catch (e) { /* keep defaults */ }
  return out;
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

export function mountRainbowStage(container, options = {}) {
  if (!container) throw new Error('mountRainbowStage: a container element is required');
  const opts = { ...DEFAULTS, ...options };
  const T = { ...TEXT, ...(options.text || {}) };
  if (opts.injectCss) ensureCss();
  if (opts.injectFonts) ensureFonts();

  const mq = (q) => (window.matchMedia ? window.matchMedia(q).matches : false);
  const reduced = mq('(prefers-reduced-motion: reduce)');
  const coarse = mq('(pointer: coarse)');
  const smallScreen = Math.min(screen.width, screen.height) < 600;
  const phone = coarse && smallScreen;

  /* DOM */
  const root = el('div', 'rbs', null, { dir: 'rtl', lang: 'he' });
  if (container.clientHeight < 40) root.classList.add('rbs--auto');
  const poster = el('img', 'rbs-poster', root, { alt: T.aria, decoding: 'async', fetchpriority: 'high' });
  poster.addEventListener('error', () => { poster.style.visibility = 'hidden'; }, { once: true });
  poster.src = opts.poster || new URL('./poster.jpg', import.meta.url).href;
  const canvasWrap = el('div', 'rbs-canvas', root);
  const leader = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  leader.setAttribute('class', 'rbs-leader');
  leader.setAttribute('aria-hidden', 'true');
  leader.innerHTML = '<line x1="0" y1="0" x2="0" y2="0" visibility="hidden"/><circle cx="0" cy="0" r="4.5" visibility="hidden"/>';
  root.appendChild(leader);
  const ui = el('div', 'rbs-ui', root);
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
  caption.textContent = T.caption;
  const label = el('div', 'rbs-label', ui, { 'aria-live': 'polite' });
  const labelTop = el('div', 'rbs-label-top', label);
  const labelTitle = el('p', 'rbs-label-title', labelTop);
  const labelClose = el('button', 'rbs-label-close', labelTop, { type: 'button', 'aria-label': T.close });
  labelClose.textContent = '×';
  const labelLine = el('p', 'rbs-label-line', label);
  const labelCta = el('button', 'rbs-label-cta', label, { type: 'button' });
  labelCta.textContent = T.cta;
  const openBtn = el('button', 'rbs-open', ui, { type: 'button' });
  openBtn.textContent = T.open3d;
  container.appendChild(root);
  // layout class for narrow stages (also needed while only the poster is shown)
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

  async function start3D() {
    root.classList.remove('rbs--fallback');
    try {
      if (!THREE) {
        const [three, oc] = await Promise.all([import('three'), import('three/addons/controls/OrbitControls.js')]);
        THREE = three;
        OrbitControls = oc.OrbitControls;
      }
      if (disposed) return;
      engine = createEngine({
        root, canvasWrap, label, labelTitle, labelLine, labelCta, labelClose, leader, hint,
        opts, T, reduced, phone, coarse, preset: currentPreset,
        onReady: markReady,
        onContextLost: () => { root.classList.remove('rbs--live', 'rbs--settled'); },
      });
    } catch (err) {
      console.warn('[rainbow-stage] 3D unavailable, keeping the poster.', err);
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
    selectFloor(n) { if (engine) engine.selectFloor(n, true); },
    clearFloor() { if (engine) engine.clearFloor(); },
    setAutoOrbit(on) { if (engine) engine.setAutoOrbit(on); },
    stats() { return engine ? engine.stats() : null; },
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
  const { root, canvasWrap, label, labelTitle, labelLine, labelCta, labelClose, leader, hint, opts, T, reduced, phone } = ctx;
  const leaderLine = leader.querySelector('line');
  const leaderDot = leader.querySelector('circle');

  const listeners = [];
  const on = (target, type, fn, o) => { target.addEventListener(type, fn, o); listeners.push([target, type, fn, o]); };

  /* renderer */
  const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance', alpha: false, stencil: false });
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
    uHiColor: { value: new THREE.Color('#2F6F86') },
    uFloorY0: { value: TOWER.y0 },
    uFloorH: { value: TOWER.fh },
    uCoast: { value: new THREE.Vector4() },
    uSeaShallow: { value: new THREE.Color() },
    uGhostFade: { value: 0.32 },
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
  const envSkyMat = makeSkyMaterial(skyUniforms, true, envGround, envZen, envHor);
  const envScene = new THREE.Scene();
  envScene.add(new THREE.Mesh(new THREE.SphereGeometry(10, 32, 16), envSkyMat));
  const pmrem = new THREE.PMREMGenerator(renderer);
  let envRT = null;

  /* materials */
  const M = makeMaterials(U);
  const world = buildWorld(site, M, U);
  scene.updateMatrixWorld(true);

  // coast line in world space for the sea shader (point on the waterline + normal towards the sea)
  {
    const p = site.localToWorld(new THREE.Vector3(COAST_X, 0, 0));
    const n = new THREE.Vector3(-1, 0, 0).applyQuaternion(site.quaternion);
    U.uCoast.value.set(p.x, p.z, n.x, n.z);
  }

  /* camera rig */
  const controls = new OrbitControls(camera, canvas);
  controls.enableDamping = true;
  controls.dampingFactor = 0.07;
  controls.enablePan = false;
  controls.rotateSpeed = 0.55;
  controls.zoomSpeed = 0.8;
  controls.minDistance = 120;
  controls.maxDistance = 1150;
  controls.minPolarAngle = 12 * DEG;
  controls.maxPolarAngle = 84 * DEG;
  controls.autoRotate = false;
  controls.autoRotateSpeed = 0;
  controls.touches.TWO = THREE.TOUCH.DOLLY_ROTATE;
  controls.enabled = false;
  canvas.style.touchAction = 'pan-y';

  const tmpV = new THREE.Vector3();
  const tmpV2 = new THREE.Vector3();
  const towerCenterLocal = new THREE.Vector3(TOWER.cx, 0, TOWER.cz);

  function localToWorld(x, y, z, out = new THREE.Vector3()) { return site.localToWorld(out.set(x, y, z)); }
  function viewFromBearing(bearingLocalDeg, elevDeg, dist, target, out) {
    // bearing in the site grid (0 = grid north, clockwise), converted to a world offset
    const b = bearingLocalDeg * DEG, e = elevDeg * DEG;
    const lx = Math.sin(b) * Math.cos(e), lz = -Math.cos(b) * Math.cos(e), ly = Math.sin(e);
    const d = new THREE.Vector3(lx, ly, lz).applyQuaternion(site.quaternion);
    return out.copy(target).addScaledVector(d, dist);
  }

  const heroTarget = new THREE.Vector3();
  const introTarget = localToWorld(6, 14, 4);
  controls.target.copy(heroTarget);
  function heroDistance() {
    const vf = camera.fov * DEG;
    const hf = 2 * Math.atan(Math.tan(vf / 2) * camera.aspect);
    const halfW = camera.aspect < 1 ? 58 : 92;
    return Math.max(118 / Math.tan(vf / 2), halfW / Math.tan(hf / 2));
  }
  function heroTargetFor(aspect, out) {
    // portrait stages centre on the tower itself; landscape keeps the courtyard in frame
    const k = Math.min(1, Math.max(0, (aspect - 0.6) / 0.6));
    return localToWorld(TOWER.cx + 5 + 11 * k, 70 - 6 * k, TOWER.cz + 3 + 5 * k, out);
  }
  const HERO = { bearing: 188, elev: 10 };
  const INTRO = { bearing: 142, elev: 42, distMul: 2.35 };
  heroTargetFor(1.6, heroTarget);

  /* state */
  let phase = 'intro';
  let introT = 0;
  let introHold = 0.35;   // seconds on the aerial view while the canvas fades in
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
  let selected = null;       // { floor, pinned }
  let hover = null;
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
    // world: x east, z south; bearing clockwise from north
    const dir = new THREE.Vector3(Math.sin(az) * Math.cos(elv), Math.sin(elv), -Math.cos(az) * Math.cos(elv)).normalize();
    U.uSunDir.value.copy(dir);
    const focus = localToWorld(0, 0, 0, tmpV);
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
    for (const m of M.all) {
      if (m.isMeshStandardMaterial) {
        m.envMap = rt.texture;
        if (!m.userData.envSet) { m.needsUpdate = true; m.userData.envSet = true; }
      }
    }
    if (envRT) envRT.dispose();
    envRT = rt;
    needsRender = true;
  }
  function fitShadowCamera(dir) {
    // light-space bounds of the region that should carry shadows (site + near quarter + the tower)
    const cam = sun.shadow.camera;
    sun.updateMatrixWorld();
    const view = new THREE.Matrix4().lookAt(sun.position, sun.target.position, new THREE.Vector3(0, 1, 0)).setPosition(sun.position);
    const inv = view.clone().invert();
    const pts = [];
    const R = 230;
    for (let i = 0; i < 16; i++) {
      const a = (i / 16) * Math.PI * 2;
      pts.push(localToWorld(-10 + Math.cos(a) * R, 0, Math.sin(a) * R * 0.85));
      pts.push(localToWorld(-10 + Math.cos(a) * R, 45, Math.sin(a) * R * 0.85));
    }
    pts.push(localToWorld(TOWER.cx, TOWER.roof + 8, TOWER.cz));
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
    if (phase === 'orbit' && !controls.autoRotate && performance.now() - lastInteract > 1500) controls.target.copy(heroTarget);
    renderer.setSize(stageW, stageH, false);
    if (post) post.gtao.setSize(stageW * dpr, stageH * dpr);
    root.classList.toggle('rbs--narrow', stageW < 600);
    labelBox.w = 0;
    leader.setAttribute('viewBox', `0 0 ${stageW} ${stageH}`);
    if (phase !== 'intro') {
      // keep the distance inside the new limits
      controls.maxDistance = Math.max(1150, heroDistance() * 2.2);
    }
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

  // wheel zoom only once the visitor has engaged with the stage (so page scrolling is not hijacked)
  on(root, 'wheel', (e) => {
    if (opts.wheel !== 'always' && performance.now() > engagedUntil) { e.stopPropagation(); return; }
    engagedUntil = performance.now() + 4000;
    lastInteract = performance.now();
  }, { capture: true, passive: true });
  on(root, 'pointerleave', () => { engagedUntil = 0; pointer.inside = false; if (!pointer.down) setHover(null); });

  const raycaster = new THREE.Raycaster();
  raycaster.layers.set(1);
  const ndc = new THREE.Vector2();

  function pickFloor(clientX, clientY) {
    const r = canvas.getBoundingClientRect();
    ndc.set(((clientX - r.left) / r.width) * 2 - 1, -((clientY - r.top) / r.height) * 2 + 1);
    raycaster.setFromCamera(ndc, camera);
    const hit = raycaster.intersectObject(world.towerProxy, false)[0];
    if (!hit) return null;
    const f = Math.floor((hit.point.y - TOWER.y0) / TOWER.fh) + 1;
    if (f < 1 || f > TOWER.floors) return null;
    return f;
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
    if (!pointer.moved && quick && e.target === canvas) {
      const f = pickFloor(e.clientX, e.clientY);
      if (f) selectFloor(f, true);
      else clearFloor();
    }
  });
  on(canvas, 'keydown', (e) => {
    const k = e.key;
    if (k === 'ArrowUp' || k === 'ArrowDown' || k === 'PageUp' || k === 'PageDown') {
      e.preventDefault();
      const base = selected ? selected.floor : 20;
      const step = (k === 'ArrowUp' || k === 'PageUp') ? 1 : -1;
      selectFloor(Math.min(TOWER.floors, Math.max(1, selected ? base + step : base)), true);
    } else if (k === 'Enter' && selected) {
      e.preventDefault();
      emitFloor(selected.floor);
    } else if (k === 'Escape') {
      clearFloor();
    }
  });
  let labelHover = false;
  on(label, 'pointerenter', () => { labelHover = true; });
  on(label, 'pointerleave', () => { labelHover = false; });
  on(labelCta, 'click', () => { if (selected) emitFloor(selected.floor); });
  on(labelClose, 'click', () => clearFloor());

  function emitFloor(floor) {
    window.dispatchEvent(new CustomEvent('nl:floor', { detail: { floor } }));
  }

  let hoverLeaveAt = 0;
  function setHover(f) {
    if (f === hover) return;
    hover = f;
    root.classList.toggle('rbs--pointer', !!f);
    if (!selected || !selected.pinned) {
      if (f) showFloor(f, false);
      else hoverLeaveAt = performance.now();
    }
  }
  function selectFloor(f, pinned) {
    showFloor(f, pinned);
    hint.classList.add('is-gone');
  }
  function showFloor(f, pinned) {
    selected = { floor: f, pinned };
    U.uHiFloor.value = f;
    labelTitle.textContent = T.floor(f);
    const top = TOWER.floors - (opts.penthouseFloors || 3);
    labelLine.textContent = f > top ? T.penthouse : (f >= opts.highFloorsFrom ? T.high : T.low);
    label.classList.add('is-on');
    labelBox.w = 0;
    needsRender = true;
  }
  function clearFloor() {
    selected = null;
    hover = null;
    U.uHiFloor.value = -100;
    label.classList.remove('is-on');
    leaderLine.setAttribute('visibility', 'hidden');
    leaderDot.setAttribute('visibility', 'hidden');
    root.classList.remove('rbs--pointer');
    needsRender = true;
  }

  /* label placement: anchored to the tower silhouette at the selected floor */
  const tAxisU = new THREE.Vector3(), tAxisV = new THREE.Vector3();
  {
    const cu = Math.cos(TOWER.rot), su = Math.sin(TOWER.rot);
    tAxisU.set(cu, 0, su).applyQuaternion(site.quaternion);
    tAxisV.set(-su, 0, cu).applyQuaternion(site.quaternion);
  }
  const towerCenterW = site.localToWorld(towerCenterLocal.clone());
  const camRight = new THREE.Vector3();
  function supportPoint(dir, out) {
    const a = TOWER.A + 2.6, b = TOWER.B + 2.6;
    const du = dir.dot(tAxisU), dv = dir.dot(tAxisV);
    const den = Math.sqrt(a * a * du * du + b * b * dv * dv) || 1;
    return out.copy(tAxisU).multiplyScalar(a * a * du / den).addScaledVector(tAxisV, b * b * dv / den);
  }
  function projectToStage(v) {
    tmpV2.copy(v).project(camera);
    return { x: (tmpV2.x * 0.5 + 0.5) * stageW, y: (-tmpV2.y * 0.5 + 0.5) * stageH, behind: tmpV2.z > 1 };
  }
  function floorAnchor(f, side) {
    camRight.setFromMatrixColumn(camera.matrixWorld, 0);
    camRight.y = 0;
    camRight.normalize().multiplyScalar(side);
    const y = TOWER.y0 + (f - 1) * TOWER.fh + 0.6;
    supportPoint(camRight, tmpV);
    tmpV.add(towerCenterW);
    tmpV.y = y;
    return projectToStage(tmpV);
  }
  function placeLabel() {
    if (!selected) return;
    const narrow = stageW < 600;
    if (!labelBox.w) { labelBox.w = label.offsetWidth || 244; labelBox.h = label.offsetHeight || 140; }
    const lw = labelBox.w, lh = labelBox.h;
    // pick the side with more room, with hysteresis
    const aR = floorAnchor(selected.floor, 1), aL = floorAnchor(selected.floor, -1);
    const roomR = stageW - aR.x, roomL = aL.x;
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
  }

  /* visibility */
  const io = new IntersectionObserver((entries) => {
    for (const en of entries) visible = en.isIntersecting;
    if (visible) kick();
  }, { threshold: 0.01 });
  io.observe(root);
  on(document, 'visibilitychange', () => { if (!document.hidden) kick(); });

  on(canvas, 'webglcontextlost', (e) => { e.preventDefault(); running = false; ctx.onContextLost(); });

  /* ambient occlusion (lazy) */
  async function enableAO() {
    if (aoOn || aoLoading || disposedE) return;
    aoLoading = true;
    try {
      if (!post) {
        // GTAO from the three addons, used without a composer: the scene still renders straight to
        // the multisampled canvas; GTAO computes a half resolution AO buffer (normals, depth, AO,
        // denoise) which one full screen quad multiplies over the finished frame. No full size
        // float targets, no copy or output passes.
        const { GTAOPass } = await import('three/addons/postprocessing/GTAOPass.js');
        if (disposedE) return;
        const gtao = new GTAOPass(scene, camera, 2, 2);
        const fullSetSize = gtao.setSize.bind(gtao);
        gtao.setSize = (w, h) => fullSetSize(Math.max(2, Math.round(w * AO_SCALE)), Math.max(2, Math.round(h * AO_SCALE)));
        gtao.setSize(stageW * dpr, stageH * dpr);
        gtao.output = GTAOPass.OUTPUT.Off;
        gtao.updateGtaoMaterial({ radius: 4.0, distanceExponent: 1.4, thickness: 5.0, scale: 1.6, samples: 16, distanceFallOff: 1.0, screenSpaceRadius: false });
        gtao.updatePdMaterial({ lumaPhi: 10, depthPhi: 2, normalPhi: 3, radius: 7, radiusExponent: 1.5, rings: 3, samples: 16 });
        // AO only on Rainbow's own plot: the context, the far sea and the horizon stay clean
        gtao.setSceneClipBox(new THREE.Box3(new THREE.Vector3(-105, -5, -105), new THREE.Vector3(105, 175, 105)));
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
      // auto mode: an invisible probe first (AO rendered at zero strength), then a soft fade in
      aoProbe = aoMode === 'auto' ? performance.now() : 0;
      aoFade = aoMode === 'auto' ? 0 : 1;
      aoFadeDir = aoMode === 'auto' ? 0 : 1;
      applyAOFade();
      perf.times.length = 0;
      needsRender = true;
    } catch (err) {
      console.warn('[rainbow-stage] AO unavailable', err);
      aoBlocked = true;
    } finally { aoLoading = false; }
  }
  const AO_STRENGTH = 0.85;   // applied on the display-referred frame
  const AO_SCALE = 1.0;       // AO buffer resolution relative to the canvas
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
    const adt = Math.min(1.0, rawDt);      // animation time step: intro and transitions keep wall-clock pace
    lastT = now;
    if (!visible || document.hidden) return; // resumed by observers
    clock += dt;
    const animateWater = !reduced;
    if (animateWater) U.uTime.value = clock;

    // intro move
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

    // preset transition
    if (trans) {
      trans.t = Math.min(1, trans.t + adt / trans.dur);
      const k = ease(trans.t);
      applyPresetState(lerpState(trans.from, trans.to, k));
      if (!trans.midEnv && trans.t > 0.5) { trans.midEnv = true; regenEnv(); }
      if (trans.t >= 1) { Object.assign(cur, trans.to); trans = null; regenEnv(); }
    }

    // idle auto-orbit, resumes after 6 s without interaction
    if (phase === 'orbit') {
      const idle = now - lastInteract > 6000;
      const want = autoOrbit && idle && !(selected && selected.pinned) && !pointer.down;
      orbitRamp = Math.max(0, Math.min(1, orbitRamp + (want ? dt / 2.5 : -dt / 0.4)));
      controls.autoRotate = orbitRamp > 0.001;
      controls.autoRotateSpeed = -0.32 * orbitRamp;
      controls.update(dt);
      if (controls.autoRotate) needsRender = true;
    }

    // hover picking (desktop), at most once per frame
    if (hoverDirty && phase === 'orbit') {
      hoverDirty = false;
      const f = pointer.inside ? pickFloor(pointer.x, pointer.y) : null;
      setHover(f);
      if (f && selected && !selected.pinned && selected.floor !== f) showFloor(f, false);
    }
    if (selected && !selected.pinned && !hover && !labelHover && hoverLeaveAt && now - hoverLeaveAt > 650) {
      hoverLeaveAt = 0;
      clearFloor();
    }

    sky.position.copy(camera.position);
    const continuous = animateWater || controls.autoRotate || phase === 'intro' || !!trans;
    if (needsRender || continuous) {
      render();
      needsRender = false;
      if (selected) placeLabel();
      if (!firstFrameDone) {
        firstFrameDone = true;
        root.classList.add('rbs--live');
        if (!ctx.coarse) root.classList.add('rbs--grab');
        setTimeout(() => root.classList.add('rbs--settled'), 1000);
        ctx.onReady();
      }
    }

    // performance governor
    perf.times.push(rawDt);
    let sum = 0;
    for (let i = perf.times.length - 1; i >= 0; i--) { sum += perf.times[i]; if (sum > 2) { perf.times.splice(0, i); break; } }
    perf.fps = perf.times.length / Math.max(0.001, perf.times.reduce((a, b) => a + b, 0));
    if (phase === 'orbit' && continuous && !trans) {
      // resolution drops only when AO is not the reason (AO has its own probe and governor)
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
          // judge the real cost of AO while it is still invisible; the first 0.6 s (shader
          // compilation for the extra passes) is ignored, then up to 1.4 s are measured
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
      post.gtao.render(renderer, null, null);   // AO buffers only (output off)
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

  // compile shaders before the first visible frame, then start
  const compile = renderer.compileAsync ? renderer.compileAsync(scene, camera) : Promise.resolve();
  compile.catch(() => {}).then(() => { if (!disposedE) { lastT = performance.now(); kick(); } });

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
    selectFloor(n, pinned) {
      const f = Math.round(Number(n));
      if (!(f >= 1 && f <= TOWER.floors)) return;
      if (phase === 'intro') endIntro();
      selectFloor(f, pinned !== false);
      lastInteract = performance.now();
      kick();
    },
    clearFloor() { clearFloor(); },
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
    // dev helpers used by the screenshot script
    _floorScreenPoint(f) {
      const toCam = new THREE.Vector3().subVectors(camera.position, towerCenterW).setY(0).normalize();
      supportPoint(toCam, tmpV).add(towerCenterW);
      tmpV.y = TOWER.y0 + (f - 1) * TOWER.fh + TOWER.fh * 0.5;
      const a = projectToStage(tmpV);
      const r = canvas.getBoundingClientRect();
      return { x: r.left + a.x, y: r.top + a.y };
    },
    _capture(w, h, quality = 0.88) {
      const pw = stageW, ph = stageH, pdpr = dpr;
      renderer.setPixelRatio(1);
      renderer.setSize(w, h, false);
      camera.aspect = w / h; camera.fov = 30; camera.updateProjectionMatrix();
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
      return { l: c.left, r: c.right, t: c.top, b: c.bottom, n: c.near, f: c.far, sunPos: sun.position.toArray().map((v) => +v.toFixed(1)), tgt: sun.target.position.toArray().map((v) => +v.toFixed(1)), dir: U.uSunDir.value.toArray().map((v) => +v.toFixed(3)), map: !!sun.shadow.map, cam: camera.position.toArray().map((v) => +v.toFixed(1)) };
    },
    _setAO(on) { if (on) { aoMode = 'on'; aoFade = 1; aoFadeDir = 0; aoProbe = 0; enableAO(); applyAOFade(); } else { aoMode = 'off'; disableAO(); } },
    _view(bearing, elev, distMul) {
      if (phase === 'intro') endIntro();
      viewFromBearing(bearing, elev, heroDistance() * (distMul || 1), heroTarget, camera.position);
      controls.target.copy(heroTarget);
      controls.update();
      lastInteract = performance.now();
      needsRender = true;
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
      world.towerProxy.geometry.dispose();
      for (const t of M.textures) t.dispose();
      if (envRT) envRT.dispose();
      pmrem.dispose();
      sun.shadow.map && sun.shadow.map.dispose();
      renderer.dispose();
      renderer.forceContextLoss();
      canvas.remove();
      if (statsEl) statsEl.remove();
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
  vec3 hor = mix(uSkyHorizon, uSkyWarm, pow(toward, uWarmPow));
  float h = clamp(d.y, 0.0, 1.0);
  vec3 col = mix(hor, uSkyZenith, 1.0 - exp(-h * 5.0));
  // soft rose band opposite the sun, a few degrees above the horizon (the evening 'belt')
  float anti = pow(1.0 - toward, 1.5);
  float belt = smoothstep(0.0, 0.07, h) * (1.0 - smoothstep(0.1, 0.42, h));
  col = mix(col, uSkyRose, uRoseAmt * anti * belt);
  float sd = max(dot(d, uSunDir), 0.0);
  col += uSkyGlowCol * uSkyGlow * (0.10 * pow(sd, 5.0) + 0.20 * pow(sd, 40.0) + 0.45 * pow(sd, 600.0));
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
        ${envMode ? `
        {
          // lighting environment: a cooler, art-directed fill (the visible sky stays sand coloured)
          float h = clamp(d.y, 0.0, 1.0);
          vec3 fill = mix(uEnvHorizon, uEnvZenith, pow(h, 0.6));
          float sd = max(dot(d, uSunDir), 0.0);
          fill += uSkyGlowCol * uSkyGlow * (0.12 * pow(sd, 5.0) + 0.25 * pow(sd, 40.0));
          c = mix(fill, uGroundEnv, smoothstep(0.02, -0.25, d.y));
        }` : ''}
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
uniform float uHiFloor; uniform vec3 uHiColor; uniform float uFloorY0; uniform float uFloorH;
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
uniform vec4 uCoast; uniform vec3 uSeaShallow;
#endif
#ifdef RBS_GHOST
uniform float uGhostFade;
#endif
${SKY_FN}
`;

const FRAG_COLOR = /* glsl */`
float rbsHi = 0.0;
#ifdef RBS_FLOOR
  if (abs(vRbsF - uHiFloor) < 0.5) rbsHi = 1.0;
#endif
#ifdef RBS_GLASS
  {
    float g = vRbsUv.x / 1.6;
    float w = fwidth(g);
    float d = abs(fract(g) - 0.5);
    float line = smoothstep(0.5 - max(w, 0.018) * 1.3, 0.5, d);
    float fadeL = 1.0 - smoothstep(0.12, 0.4, w);
    diffuseColor.rgb = mix(diffuseColor.rgb, vec3(0.93, 0.92, 0.89), line * fadeL * 0.6);
    if (vRbsF > 0.5) {
      float fl = floor((vRbsW.y - uFloorY0) / uFloorH) + 1.0;
      if (abs(fl - uHiFloor) < 0.5) rbsHi = 0.62;
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
  normal = normalize((viewMatrix * vec4(nW, 0.0)).xyz);
}
#endif
`;

const FRAG_EMISSIVE = /* glsl */`
if (rbsHi > 0.0) totalEmissiveRadiance += uHiColor * (0.22 * rbsHi);
`;

const FRAG_FOG = /* glsl */`
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
  mat.customProgramCacheKey = () => 'rbs-' + key;
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
  const glass = std('#93AAB0', 0.12, { metalness: 0.08 });
  patchMaterial(glass, 'glass', { glass: true }, U);
  const ground = std('#FFFFFF', 0.97, { vertexColors: true });
  patchMaterial(ground, 'ground', {}, U);
  const foliage = std('#FFFFFF', 0.92, { vertexColors: true });
  patchMaterial(foliage, 'foliage', {}, U);
  const ghost = std('#C9C8C2', 0.95);
  patchMaterial(ghost, 'ghost', { ghost: true }, U);
  const pool = std('#5FB9C4', 0.05);
  patchMaterial(pool, 'pool', { water: true, local: { uWater: { value: new THREE.Vector4(2.6, 0.55, 250, 900) } } }, U);
  const sea = std('#245A6E', 0.08);
  patchMaterial(sea, 'sea', { water: true, sea: true, local: { uWater: { value: new THREE.Vector4(1.0, 0.7, 250, 1100) } } }, U);

  // soft contact darkening under buildings (fake AO when GTAO is off)
  const blob = makeBlobTexture();
  const decal = new THREE.MeshBasicMaterial({ color: 0x1b2328, transparent: true, opacity: 0.2, alphaMap: blob, depthWrite: false, polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -2 });

  const all = [white, glass, ground, foliage, ghost, pool, sea, decal];
  return {
    white, glass, ground, foliage, ghost, pool, sea, decal, all,
    envWhiteList: [white, ground, foliage, ghost],
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

function buildWorld(site, M, U) {
  const col = (h) => new THREE.Color(h);
  const C = {
    base: col('#D0CCC4'), plate: col('#DBD7CF'), plinth: col('#EFEBE4'), deck: col('#F1EDE6'), outline: col('#B7AE9F'),
    lawn: col('#BCC6AE'), park: col('#CDD3C3'), sand: col('#EADDC3'), prom: col('#E8E2D6'), path: col('#E9E4DA'),
    tree: col('#BEC6B5'), treeDark: col('#AEB8A6'), planter: col('#4A6651'), trunk: col('#C8C0B2'), roofGarden: col('#A9B597'),
  };
  const rnd = mulberry32(20260924);

  const white = newAcc({ fl: true });
  const glass = newAcc({ uv: true, fl: true });
  const ground = newAcc({ col: true });
  const foliage = newAcc({ col: true });
  const trunks = newAcc({ col: true });
  const ghosts = newAcc();
  const water = newAcc();
  const sea = newAcc();
  const decals = newAcc({ uv: true });

  /* ---------- ground: base board, sea, beach, promenade, park ---------- */
  setCol(ground, C.base);
  {
    const x0 = COAST_X, x1 = 7000, z0 = -7000, z1 = 7000, b = ground.n;
    V(ground, x0, 0, z0, 0, 1, 0); V(ground, x1, 0, z0, 0, 1, 0); V(ground, x1, 0, z1, 0, 1, 0); V(ground, x0, 0, z1, 0, 1, 0);
    quad(ground, b, b + 1, b + 2, b + 3);
  }
  const strip = (x0, x1, y, c) => {
    setCol(ground, c);
    const b = ground.n;
    V(ground, x0, y, -7000, 0, 1, 0); V(ground, x1, y, -7000, 0, 1, 0); V(ground, x1, y, 7000, 0, 1, 0); V(ground, x0, y, 7000, 0, 1, 0);
    quad(ground, b, b + 1, b + 2, b + 3);
    // small step face towards the sea side
    const b2 = ground.n;
    V(ground, x0, 0, -7000, -1, 0, 0); V(ground, x0, y, -7000, -1, 0, 0); V(ground, x0, y, 7000, -1, 0, 0); V(ground, x0, 0, 7000, -1, 0, 0);
    quad(ground, b2, b2 + 1, b2 + 2, b2 + 3);
  };
  strip(COAST_X, COAST_X + 40, 0.12, C.sand);
  strip(COAST_X + 40, COAST_X + 54, 0.45, C.prom);
  // coastal park plate (the column west of the site)
  setCol(ground, C.park);
  addBox(ground, -97, 0, 42, 14000, 0, 0.16, 0);
  // park paths
  setCol(ground, C.path);
  for (const [x0, amp, ph] of [[-104, 3, 0], [-88, 2.5, 1.7]]) {
    const P = [];
    for (let i = 0; i <= 120; i++) {
      const z = -1400 + i * (2800 / 120);
      P.push([x0 + Math.sin(z / 90 + ph) * amp, z]);
    }
    addRibbon(ground, P, 2.6, 0.18);
  }
  // sea plane
  {
    const b = sea.n;
    V(sea, -12000, -0.3, -12000, 0, 1, 0); V(sea, COAST_X + 6, -0.3, -12000, 0, 1, 0); V(sea, COAST_X + 6, -0.3, 12000, 0, 1, 0); V(sea, -12000, -0.3, 12000, 0, 1, 0);
    quad(sea, b, b + 1, b + 2, b + 3);
  }

  /* ---------- quarter: block plates + ghost volumes ---------- */
  const parkCells = [];
  for (let i = 0; i <= 4; i++) {
    for (let j = -4; j <= 4; j++) {
      if (i === 0 && j === 0) continue;
      const cx = i * PITCH_X, cz = j * PITCH_Z;
      if (i === 0 && j === 1) {
        setCol(ground, C.park);
        addSlab(ground, roundRectPoly(cx, cz, 104, 80, 8, 6), 0, 0.3);
        setCol(ground, C.path);
        addRibbon(ground, [[cx - 50, cz - 30], [cx - 10, cz - 6], [cx + 18, cz + 10], [cx + 50, cz + 34]], 3, 0.32);
        addRibbon(ground, [[cx - 48, cz + 30], [cx - 14, cz + 14], [cx + 16, cz - 12], [cx + 48, cz - 32]], 3, 0.32);
        parkCells.push([cx, cz]);
        continue;
      }
      setCol(ground, C.plate);
      addSlab(ground, roundRectPoly(cx, cz, 104, 80, 8, 6), 0, 0.3);
      ghostCell(ghosts, cx, cz, i, j, rnd);
    }
  }
  // blocks behind the park to the north/south along the coast are left open (parkland)

  /* ---------- the plot ---------- */
  setCol(ground, C.plinth);
  const plotLoop = addSlab(ground, roundRectPoly(0, 0, PLOT.hx * 2, PLOT.hz * 2, PLOT.r, 10), 0, PLOT.h);
  // plot outline: a fine engraved line just inside the plinth edge
  setCol(ground, C.outline);
  addLoopRibbon(ground, offsetLoop(plotLoop, -0.9), 0.28, PLOT.h + 0.012);

  // courtyard lawns
  setCol(ground, C.lawn);
  const Y = PLOT.h;
  addSlab(ground, roundRectPoly(22, 11, 21, 12, 5.5, 8), Y, Y + 0.18);
  addSlab(ground, roundRectPoly(-1, -14, 16, 7, 3.5, 8), Y, Y + 0.18);
  addSlab(ground, roundRectPoly(-44, -31, 12, 12, 5, 8), Y, Y + 0.18);
  addSlab(ground, roundRectPoly(46, -36.5, 9, 5, 2.4, 6), Y, Y + 0.18);
  addSlab(ground, roundRectPoly(-47, 8, 6, 22, 3, 8), Y, Y + 0.18);
  addSlab(ground, rotatePoly(roundRectPoly(10, -4, 14, 5, 2.5, 6), 10, -4, 18 * DEG), Y, Y + 0.18);

  /* ---------- pools ---------- */
  // amenity pavilion with the infinity pool on its roof
  const pav = { cx: 0, cz: 6, w: 21, d: 11, h: 3.6 };
  setCol(ground, C.deck);
  const pavLoop = addSlab(ground, roundRectPoly(pav.cx, pav.cz, pav.w, pav.d, 2.2, 8), Y, Y + pav.h);
  // glazed recess around the pavilion (a thin glass band under the roof edge)
  addWallFlat(glass, offsetLoop(pavLoop, 0.03), Y + 0.4, Y + pav.h - 0.55);
  const poolTop = Y + pav.h;
  addPool(water, white, pav.cx, pav.cz + 1.4, 17, 5.2, 1.4, poolTop, true);
  // adults-only pool at courtyard level, framed by a deck and trees
  setCol(ground, C.deck);
  addSlab(ground, roundRectPoly(24, -10, 19, 10, 3, 8), Y, Y + 0.1);
  addPool(water, white, 24, -10, 12, 4.6, 1.6, Y + 0.1, false);
  // loungers
  for (let k = 0; k < 6; k++) addBox(white, -6.5 + k * 2.6, pav.cz - 2.9, 0.8, 2.0, poolTop, poolTop + 0.35, 0);
  for (let k = 0; k < 4; k++) addBox(white, 19.5 + k * 3.0, -13.6, 0.8, 2.0, Y + 0.1, Y + 0.45, 0);

  /* ---------- tower ---------- */
  const towerPoly = ellipsePoly(TOWER.A, TOWER.B, TOWER.cx, TOWER.cz, TOWER.rot, 720);
  const tLoop = resampleLoop(towerPoly, 84, 7);
  const tLobby = offsetLoop(tLoop, -2.2);
  const tPent = offsetLoop(tLoop, -1.3);
  const top = TOWER.floors - 3;
  const bandProf = { Hp: 1.05, Ts: 0.4, tp: 0.24, rb: 0.12 };
  glass.f = 1;
  addWall(glass, tLobby, Y, TOWER.y0);
  addWall(glass, tLoop, TOWER.y0 - 0.5, TOWER.y0 + top * TOWER.fh);
  addWall(glass, tPent, TOWER.y0 + top * TOWER.fh - 0.5, TOWER.roof);
  glass.f = 0;
  const K = 3, dphi = 0.16;
  const planterSpots = [];
  for (let f = 1; f <= TOWER.floors; f++) {
    const y = TOWER.y0 + (f - 1) * TOWER.fh;
    const ph = 0.4 + f * dphi;
    const pent = f > top;
    const lp = pent ? tPent : tLoop;
    const dmin = pent ? 2.4 : 0.7, dmax = pent ? 4.8 : 3.6;
    white.f = f;
    const depth = (s) => dmin + (dmax - dmin) * (0.5 + 0.5 * Math.sin(2 * Math.PI * K * s + ph));
    const out = addBand(white, lp, y, depth, bandProf);
    // planters at a few wave crests
    if (pent) {
      for (let c = 0; c < K; c++) {
        const sCrest = (((0.25 - ph / (2 * Math.PI)) + c) / K + 10) % 1;
        let best = 0, bd = 9;
        for (let i = 0; i < out.length; i++) { const dd = Math.abs(out[i].s - sCrest); if (dd < bd) { bd = dd; best = i; } }
        const o = out[best];
        planterSpots.push({ x: o.x - o.nx * 0.75, z: o.z - o.nz * 0.75, y, nx: o.nx, nz: o.nz, big: pent });
      }
    }
  }
  // roof: parapet band, cap and a light crown ring on slender posts
  white.f = TOWER.floors + 1;
  addBand(white, tPent, TOWER.roof, () => 0.55, { Hp: 1.2, Ts: 0.5, tp: 0.3, rb: 0.14 });
  white.f = -1;
  addCap(white, tPent, TOWER.roof + 0.02, true);
  const crownLoop = offsetLoop(tLoop, 0.6);
  white.f = TOWER.floors + 2;
  addBand(white, crownLoop, TOWER.roof + 5.4, () => 2.1, { Hp: 0.3, Ts: 0.6, tp: 0.3, rb: 0.14, inset: 0 });
  white.f = -1;
  {
    const post = new THREE.CylinderGeometry(0.32, 0.32, 5.2, 8, 1, true);
    for (let k = 0; k < 8; k++) {
      const p = crownLoop.pts[Math.floor((k / 8) * crownLoop.pts.length)];
      addGeometry(white, post, new THREE.Matrix4().makeTranslation(p.x + p.nx * 0.9, TOWER.roof + 2.6, p.z + p.nz * 0.9));
    }
    post.dispose();
  }
  // lobby canopy detail: the first band already overhangs the recessed lobby glass

  /* ---------- boutique blocks ---------- */
  const blockFootprints = [];
  BLOCKS.forEach((bk, bi) => {
    const poly = capsulePoly(bk.p0, bk.p1, bk.p2, BLOCK_W, 40);
    const loop = resampleLoop(poly, 52, 5);
    const ground0 = offsetLoop(loop, -1.0);
    const topInset = offsetLoop(loop, -2.4);
    const gh = 4.4, fh = 3.2;
    const nF = bk.floors;
    const yTopFloor = Y + gh + (nF - 2) * fh;   // level of the top floor
    const roofY = Y + gh + (nF - 1) * fh;
    addWall(glass, ground0, Y, Y + gh);
    addWall(glass, loop, Y + gh - 0.4, yTopFloor);
    addWall(glass, topInset, yTopFloor - 0.4, roofY);
    const bprof = { Hp: 1.0, Ts: 0.38, tp: 0.22, rb: 0.11 };
    white.f = -1;
    for (let f = 2; f <= nF; f++) {
      const y = Y + gh + (f - 2) * fh;
      const isTop = f === nF;
      const ph = bk.ph + f * 0.42;
      const depth = (s) => 0.75 + 1.55 * (0.5 + 0.5 * Math.sin(2 * Math.PI * 5 * s + ph));
      if (isTop) addBand(white, topInset, y, (s) => 2.4 + depth(s), bprof);
      else addBand(white, loop, y, depth, bprof);
    }
    // roof: low parapet, cap, garden and pergola
    addBand(white, topInset, roofY, () => 0.4, { Hp: 0.9, Ts: 0.45, tp: 0.26, rb: 0.12 });
    addCap(white, topInset, roofY + 0.02, true);
    const gardenLoop = offsetLoop(topInset, -1.6);
    setCol(ground, C.roofGarden);
    // roof garden as a low planted slab (ground material carries vertex colours)
    addWall(ground, gardenLoop, roofY, roofY + 0.32);
    addCap(ground, gardenLoop, roofY + 0.32, true);
    // pergola slats over part of the roof
    const mid = gardenLoop.pts[Math.floor(gardenLoop.pts.length * 0.25)];
    const tan = Math.atan2(bk.p2[1] - bk.p0[1], bk.p2[0] - bk.p0[0]);
    const cx = (bk.p0[0] + bk.p2[0]) / 2 * 0.5 + mid.x * 0.5, cz = (bk.p0[1] + bk.p2[1]) / 2 * 0.5 + mid.z * 0.5;
    for (let k = -3; k <= 3; k++) {
      const ox = Math.cos(tan) * k * 0.9, oz = Math.sin(tan) * k * 0.9;
      addBox(white, cx + ox, cz + oz, 0.18, 4.2, roofY + 2.5, roofY + 2.7, tan);
    }
    for (const sx of [-3, 3]) for (const sz of [-1.9, 1.9]) {
      const px = cx + Math.cos(tan) * sx * 0.9 - Math.sin(tan) * sz, pz = cz + Math.sin(tan) * sx * 0.9 + Math.cos(tan) * sz;
      addBox(white, px, pz, 0.2, 0.2, roofY + 0.3, roofY + 2.5, tan);
    }
    // a few planters on the roof garden edge
    for (let k = 0; k < 5; k++) {
      const p = gardenLoop.pts[Math.floor(((k + 0.5) / 5) * gardenLoop.pts.length)];
      planterSpots.push({ x: p.x, z: p.z, y: roofY + 0.3, nx: p.nx, nz: p.nz, big: false, roof: true });
    }
    blockFootprints.push(loop);
  });

  /* ---------- planters ---------- */
  {
    const bush = new THREE.IcosahedronGeometry(1, 1);
    const m = new THREE.Matrix4(), q = new THREE.Quaternion(), s = new THREE.Vector3(), p = new THREE.Vector3();
    for (const sp of planterSpots) {
      setCol(foliage, C.planter);
      const ang = Math.atan2(sp.nx, sp.nz);
      q.setFromAxisAngle(new THREE.Vector3(0, 1, 0), ang);
      s.set(sp.big ? 1.8 : 1.35, sp.big ? 0.75 : 0.6, sp.big ? 1.1 : 0.85);
      p.set(sp.x, sp.y + (sp.roof ? 0.5 : 0.62), sp.z);
      m.compose(p, q, s);
      addGeometry(foliage, bush, m);
    }
    bush.dispose();
  }

  /* ---------- trees ---------- */
  const trees = [];
  // courtyard
  [[15, -14], [18, -5.5], [30.5, -5], [31, -14.5], [12, 16], [33, 16], [27, 3], [15.5, 3.5], [-8, -20], [6, -20.5],
    [-12, 14.5], [-9, 20], [10, 21], [-44, -21], [-46, -12], [-45, 18], [-19, -34], [47, 22], [48, -20], [-50, 35]].forEach(([x, z]) => trees.push({ x, z, y: Y + 0.18, r: 2.1 + rnd() * 0.7, dark: false }));
  // street trees around the plot and the neighbouring plates
  const streetRows = [];
  streetRows.push([0, 0]);   // street trees only around Rainbow's own plot; the quarter stays clean
  for (const [cx, cz] of streetRows) {
    const hx = 52 - 2.4, hz = 40 - 2.4;
    const onSite = cx === 0 && cz === 0;
    const yy = onSite ? 0.0 : 0.3;
    const edgeOffset = onSite ? 5 : 0; // around the plot, trees stand on the street verge outside the plinth
    for (let x = -hx + 6; x <= hx - 6; x += 14) {
      trees.push({ x: cx + x, z: cz - hz - edgeOffset, y: yy, r: 1.7 + rnd() * 0.4, dark: rnd() < 0.3 });
      trees.push({ x: cx + x, z: cz + hz + edgeOffset, y: yy, r: 1.7 + rnd() * 0.4, dark: rnd() < 0.3 });
    }
    for (let z = -hz + 8; z <= hz - 8; z += 14) {
      trees.push({ x: cx - hx - edgeOffset, z: cz + z, y: yy, r: 1.7 + rnd() * 0.4, dark: rnd() < 0.3 });
      trees.push({ x: cx + hx + edgeOffset, z: cz + z, y: yy, r: 1.7 + rnd() * 0.4, dark: rnd() < 0.3 });
    }
  }
  // pocket park south of the plot
  for (const [px, pz] of parkCells) {
    for (let k = 0; k < 16; k++) trees.push({ x: px - 44 + rnd() * 88, z: pz - 32 + rnd() * 64, y: 0.3, r: 2.2 + rnd() * 1.0, dark: rnd() < 0.5 });
  }
  // coastal park groves
  for (let k = 0; k < 40; k++) {
    const x = -114 + rnd() * 34, z = -300 + rnd() * 600;
    trees.push({ x, z, y: 0.35, r: 2.3 + rnd() * 1.1, dark: rnd() < 0.5 });
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

  /* ---------- contact decals (fake AO) ---------- */
  const decal = (cx, cz, w, d, rot, y) => {
    const c = Math.cos(rot), s = Math.sin(rot), b = decals.n;
    const pts = [[-1, -1], [1, -1], [1, 1], [-1, 1]];
    for (const [u, v] of pts) {
      const x = u * w / 2, z = v * d / 2;
      decals.u = (u + 1) / 2; decals.v = (v + 1) / 2;
      V(decals, cx + x * c - z * s, y, cz + x * s + z * c, 0, 1, 0);
    }
    quad(decals, b, b + 1, b + 2, b + 3);
  };
  decal(TOWER.cx, TOWER.cz, (TOWER.A + 5.5) * 2, (TOWER.B + 5.5) * 2, TOWER.rot, Y + 0.02);
  BLOCKS.forEach((bk) => {
    const cx = (bk.p0[0] + 2 * bk.p1[0] + bk.p2[0]) / 4, cz = (bk.p0[1] + 2 * bk.p1[1] + bk.p2[1]) / 4;
    const len = Math.hypot(bk.p2[0] - bk.p0[0], bk.p2[1] - bk.p0[1]) + BLOCK_W;
    const rot = Math.atan2(bk.p2[1] - bk.p0[1], bk.p2[0] - bk.p0[0]);
    decal(cx, cz, len + 8, BLOCK_W + 9, rot, Y + 0.02);
  });
  decal(pav.cx, pav.cz, pav.w + 6, pav.d + 6, 0, Y + 0.02);

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
  add(white, M.white, true, true, 'white');
  add(glass, M.glass, true, true, 'glass');
  add(foliage, M.foliage, true, true, 'foliage');
  add(trunks, M.foliage, false, true, 'trunks');
  add(water, M.pool, false, true, 'pools');
  const dm = add(decals, M.decal, false, false, 'decals');
  if (dm) dm.renderOrder = 2;
  site.updateMatrixWorld(true);
  meshes.forEach((m) => m.updateMatrix());

  // picking proxy (layer 1 only, never rendered)
  const proxyGeo = new THREE.CylinderGeometry(1, 1, TOWER.roof - TOWER.y0 + 1.2, 40, 1, false);
  proxyGeo.translate(0, (TOWER.roof + TOWER.y0) / 2, 0);
  const towerProxy = new THREE.Mesh(proxyGeo, new THREE.MeshBasicMaterial());
  towerProxy.scale.set(TOWER.A + 2.2, 1, TOWER.B + 2.2);
  towerProxy.position.set(TOWER.cx, -0.4, TOWER.cz);
  towerProxy.rotation.y = -TOWER.rot;
  towerProxy.layers.set(1);
  site.add(towerProxy);
  towerProxy.updateMatrixWorld(true);

  let triangles = 0;
  for (const m of meshes) triangles += m.geometry.index.count / 3;
  return { towerProxy, triangles, meshCount: meshes.length };
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

/* future buildings of the quarter: pale volumes, kept low on the side facing the default camera */
function ghostCell(a, cx, cz, i, j, rnd) {
  const ring = Math.max(Math.abs(i), Math.abs(j));
  const foreground = j >= 1 && i <= 2;   // local south, between the default camera and the site
  const hmax = ring === 1 ? (foreground ? 12 : 16) : (ring === 2 ? 22 : 28);
  const hmin = ring === 1 ? 8 : 13;
  const H = () => hmin + rnd() * (hmax - hmin);
  const type = rnd();
  const tall = ring >= 3 && !foreground && rnd() < 0.2;
  if (tall) {
    // podium + tower
    addBox(a, cx - 14, cz + 8, 60, 34, 0.3, 0.3 + 10 + rnd() * 4, 0);
    const th = 40 + rnd() * 22;
    addBox(a, cx + 22, cz - 12, 24, 24, 0.3, th, 0);
    addGhost(a, cx - 24, cz - 26, 44, 14, 0.3, H(), rnd);
  } else if (type < 0.5) {
    // perimeter bars
    for (const [ox, oz, w] of [[-26, -27, 34], [14, -27, 38], [-18, 27, 40], [24, 27, 30]]) addGhost(a, cx + ox, cz + oz, w, 14, 0.3, H(), rnd);
    if (rnd() < 0.6) addGhost(a, cx + 38, cz, 14, 30, 0.3, H() * 0.85, rnd);
  } else {
    // cluster of mid-rise blocks
    const n = 3 + Math.floor(rnd() * 2);
    for (let k = 0; k < n; k++) {
      const ox = (k % 2 ? 1 : -1) * (14 + rnd() * 12), oz = (k < 2 ? -1 : 1) * (12 + rnd() * 8);
      addGhost(a, cx + ox, cz + oz, 26 + rnd() * 10, 16 + rnd() * 6, 0.3, H(), rnd);
    }
  }
}
