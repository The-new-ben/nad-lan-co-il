/*
 * MassingStage (HAD-794, package 3, 19.11.2026): ONE shared 3D stage for every project page that has no stage of its own
 * (H Infinity, FIRST Sde Dov, Gindi Vogue, Einstein Tower, and any project added later as data). Design board:
 * https://claude.ai/artifact/VdA956RZtEthDSgziFSJTW (sea-chart palette: abyss #10262F, sea #2F6F86, foam #E8F1F3,
 * chart magenta #C2185B for the picked floor; Heebo, IBM Plex Mono for numbers).
 *
 * It plugs into the existing project-stage shell (inc/project-stage.php + bridge.js) exactly like a hand-built stage.js:
 * the bridge imports <dir>/stage.js and calls its mount; that tiny file holds only the project's data and calls mount()
 * below. Events are the fleet's: nl:floor {floor, heightM}, nl:facing {floor, heightM, bearing, unit, toward},
 * nl:floor-action {action, floor, unit}, nl:floor-cta {floor, bearing}. So the view from the floor, the beam on the area
 * map, WhatsApp and the designer link all come from the bridge, unchanged. engine.js is never touched.
 *
 * Honesty: floors and building counts come from the project's published facts (the spec's src line); the buildings'
 * footprints and places on the lot are an illustration and the caption says so. The city around is the Tel Aviv-Yafo
 * GIS layers already shipped with a neighbouring stage (city.json), drawn as it stands. Heights for the view: floors x
 * spec.floorH, called "estimated" by the bridge.
 */
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';

const C = { abyss: 0x10262f, deep: 0x1f4b5c, sea: 0x2f6f86, foam: 0xe8f1f3, magenta: 0xc2185b, city: 0xaebcc3, far: 0xa3b2b9, ground: 0xd3dde1, green: 0x9fbcaa };

const WORDS = {
  he: { floor: 'קומה', of: 'מתוך', pick: 'הקישו על קומה במגדל, או בחרו כאן', example: 'דירה לדוגמה', side: 'צד', view: 'הנוף והמפה', design: 'לעצב את הדירה', cta: 'לקבלת תוכניות ומחירים', up: 'קומה למעלה', down: 'קומה למטה', caption: 'הדמיה להמחשה בלבד: מספר הקומות לפי הפרסומים, צורת הבניינים ומקומם במגרש להמחשה. הבניינים סביב לפי עיריית תל אביב-יפו.', aria: 'הדמיה של הפרויקט והבניינים סביבו', dirs: { n: 'לצפון', e: 'למזרח', s: 'לדרום', w: 'למערב' }, faceHint: 'בחרו צד, והנוף ממנו יופיע מתחת', drag: 'גוררים לסובב', tower: 'מגדל', floors: 'קומות במגדל' },
  en: { floor: 'Floor', of: 'of', pick: 'Tap a floor on the tower, or choose here', example: 'Example apartment', side: 'Side', view: 'View and map', design: 'Design the apartment', cta: 'Get plans and prices', up: 'Floor up', down: 'Floor down', caption: 'Illustration only: floor counts as published; building shapes and positions on the lot are illustrative. Surrounding buildings per the Tel Aviv-Yafo municipality.', aria: 'Visualisation of the project and the buildings around it', dirs: { n: 'North', e: 'East', s: 'South', w: 'West' }, faceHint: 'Pick a side and its view appears below', drag: 'Drag to turn', tower: 'Tower', floors: 'floors in the tower' },
  fr: { floor: 'Étage', of: 'sur', pick: 'Touchez un étage de la tour, ou choisissez ici', example: 'Appartement exemple', side: 'Côté', view: 'Vue et carte', design: 'Aménager l’appartement', cta: 'Plans et prix', up: 'Étage au-dessus', down: 'Étage en dessous', caption: 'Illustration uniquement : nombre d’étages selon les publications ; formes et emplacement des bâtiments à titre d’illustration. Environs selon la municipalité de Tel-Aviv-Jaffa.', aria: 'Visualisation du projet et des immeubles alentour', dirs: { n: 'Nord', e: 'Est', s: 'Sud', w: 'Ouest' }, faceHint: 'Choisissez un côté, la vue s’affiche dessous', drag: 'Glissez pour tourner', tower: 'Tour', floors: 'étages dans la tour' },
  ru: { floor: 'Этаж', of: 'из', pick: 'Нажмите на этаж башни или выберите здесь', example: 'Квартира для примера', side: 'Сторона', view: 'Вид и карта', design: 'Обустроить квартиру', cta: 'Планировки и цены', up: 'Этаж выше', down: 'Этаж ниже', caption: 'Только для иллюстрации: число этажей по публикациям; форма и расположение зданий на участке условны. Окрестности по данным муниципалитета Тель-Авива-Яффо.', aria: 'Визуализация проекта и зданий вокруг', dirs: { n: 'Север', e: 'Восток', s: 'Юг', w: 'Запад' }, faceHint: 'Выберите сторону, вид появится ниже', drag: 'Потяните, чтобы повернуть', tower: 'Башня', floors: 'этажей в башне' },
  ar: { floor: 'الطابق', of: 'من', pick: 'اضغطوا على طابق في البرج أو اختاروا هنا', example: 'شقة للمثال', side: 'جهة', view: 'المنظر والخريطة', design: 'تصميم الشقة', cta: 'المخططات والأسعار', up: 'طابق أعلى', down: 'طابق أدنى', caption: 'للتوضيح فقط: عدد الطوابق حسب المنشور؛ أشكال المباني ومواقعها في القسيمة للتوضيح فقط. المحيط حسب بلدية تل أبيب-يافا.', aria: 'تصوير المشروع والمباني المحيطة', dirs: { n: 'شمالاً', e: 'شرقاً', s: 'جنوباً', w: 'غرباً' }, faceHint: 'اختاروا جهة ويظهر المنظر أدناه', drag: 'اسحبوا للتدوير', tower: 'البرج', floors: 'طابقاً في البرج' },
};
const SIDES = { n: 0, e: 90, s: 180, w: 270 };
const norm = (b) => ((Number(b) % 360) + 360) % 360;
const emit = (name, detail) => window.dispatchEvent(new CustomEvent(name, { detail }));
const track = (name, data) => { try { if (window.nlTrack) window.nlTrack(name, data || {}); } catch (e) { /* the tracker is optional */ } };
const el = (tag, cls, parent, attrs) => {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (attrs) for (const k in attrs) e.setAttribute(k, attrs[k]);
  if (parent) parent.appendChild(e);
  return e;
};

function pageLang() {
  const l = String(document.documentElement.lang || 'he').slice(0, 2).toLowerCase();
  return WORDS[l] ? l : 'he';
}

/* metres east / south of the project point from lat/lng (the fleet's local frame, true north) */
function toLocal(lat, lng, o) {
  return { x: (lng - o.lng) * Math.cos((o.lat * Math.PI) / 180) * 111320, z: -(lat - o.lat) * 110574 };
}

let cssDone = false;
function ensureCss() {
  if (cssDone || document.getElementById('nlms-css')) { cssDone = true; return; }
  cssDone = true;
  const st = document.createElement('style');
  st.id = 'nlms-css';
  st.textContent = [
    '.nlms{position:relative;width:100%;height:100%;min-height:340px;overflow:hidden;background:#10262f;border-radius:inherit;font-family:Heebo,system-ui,sans-serif;touch-action:pan-y}',
    '.nlms-poster{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:opacity .5s}',
    '.nlms.is-live .nlms-poster{opacity:0;pointer-events:none}',
    '.nlms-canvas{position:absolute;inset:0}.nlms-canvas canvas{display:block;width:100%!important;height:100%!important;outline:none}',
    '.nlms-chip{position:absolute;top:12px;inset-inline-start:12px;z-index:3;background:rgba(16,38,47,.88);color:#e8f1f3;border:1px solid rgba(232,241,243,.28);border-radius:10px;padding:7px 12px;font:600 14px/1.3 Heebo,system-ui,sans-serif;pointer-events:none}',
    '.nlms-chip b{font-family:"IBM Plex Mono",ui-monospace,monospace;font-weight:500}',
    '.nlms-drag{position:absolute;top:12px;inset-inline-end:12px;z-index:3;color:rgba(232,241,243,.85);font:500 12px Heebo,system-ui,sans-serif;pointer-events:none}',
    '.nlms-cap{position:absolute;bottom:8px;inset-inline:12px;z-index:3;margin:0;color:rgba(232,241,243,.82);font:400 11.5px/1.45 Heebo,system-ui,sans-serif;pointer-events:none;text-shadow:0 1px 2px rgba(16,38,47,.8)}',
    '.nlms-card{margin:12px 0 0;background:#fff;border:1px solid #d6dde1;border-radius:16px;padding:14px;color:#14212b;font-family:Heebo,system-ui,sans-serif}',
    '.nlms-card h3{margin:0 0 4px!important;font:800 20px/1.25 Heebo,system-ui,sans-serif!important;color:#10262f!important}',
    '.nlms-card h3 b{font-family:"IBM Plex Mono",ui-monospace,monospace;font-weight:500}',
    '.nlms-note{margin:0 0 10px;font-size:14px;line-height:1.55;color:#3b4753}',
    '.nlms-row{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin:8px 0}',
    '.nlms-step{width:44px;height:44px;border-radius:12px;border:1.5px solid #10262f;background:#fff;color:#10262f;font:700 20px/1 Heebo,system-ui,sans-serif;cursor:pointer}',
    '.nlms-range{flex:1;min-width:140px;accent-color:#c2185b;height:44px}',
    '.nlms-sides{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;margin:8px 0}',
    '.nlms-side{min-height:48px;border-radius:12px;border:1.5px solid #aeb8bf;background:#eef3f5;color:#10262f;font:600 14px/1.3 Heebo,system-ui,sans-serif;cursor:pointer;padding:6px 10px;text-align:start}',
    '.nlms-side small{display:block;font-weight:400;font-size:11.5px;color:#5f6b75}',
    '.nlms-side[aria-pressed="true"]{border-color:#c2185b;background:#fff;box-shadow:inset 0 0 0 1px #c2185b}',
    '.nlms-acts{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}',
    '.nlms-act{flex:1 1 140px;min-height:48px;border-radius:12px;border:0;background:#10262f;color:#fff;font:700 15px Heebo,system-ui,sans-serif;cursor:pointer;padding:0 14px}',
    '.nlms-act--sec{background:#e8f1f3;color:#10262f}',
    '.nlms-hint{margin:0;font-size:13px;color:#5f6b75}',
    '@media (max-width:700px){.nlms-cap{display:none}.nlms-chip{font-size:13px}}',
    '@media (prefers-reduced-motion:reduce){.nlms-poster{transition:none}}',
  ].join('');
  document.head.appendChild(st);
}

/* the city around, from a neighbouring stage's city.json (its own turned frame), into this project's true-north frame */
function cityToLocal(city, origin) {
  const g = (-(Number(city.origin.grid_deg) || 0) * Math.PI) / 180;
  const c = Math.cos(g), s = Math.sin(g);
  const off = toLocal(city.origin.lat, city.origin.lng, origin);
  return (x, z) => ({ x: x * c + z * s + off.x, z: -x * s + z * c + off.z });
}

function sky() {
  const cv = document.createElement('canvas');
  cv.width = 4; cv.height = 256;
  const g = cv.getContext('2d');
  const gr = g.createLinearGradient(0, 0, 0, 256);
  gr.addColorStop(0, '#0c1f27'); gr.addColorStop(0.45, '#1f4b5c'); gr.addColorStop(0.78, '#5f93a5'); gr.addColorStop(1, '#bcd6de');
  g.fillStyle = gr; g.fillRect(0, 0, 4, 256);
  const t = new THREE.CanvasTexture(cv);
  t.colorSpace = THREE.SRGBColorSpace;
  return t;
}

function webglOk() {
  try { const c = document.createElement('canvas'); return !!(c.getContext('webgl2') || c.getContext('webgl')); } catch (e) { return false; }
}

export function mount(container, options, SPEC, base) {
  if (!container) throw new Error('MassingStage: a container is required');
  ensureCss();
  const opts = options || {};
  const lang = pageLang();
  const W = Object.assign({}, WORDS[lang], (SPEC.words && SPEC.words[lang]) || {});
  const rtl = lang === 'he' || lang === 'ar';
  const origin = { lat: SPEC.lat, lng: SPEC.lng };
  const floorH = Number(SPEC.floorH) || 3.3;
  const main = SPEC.buildings.find((b) => b.main) || SPEC.buildings[0];
  const floors = Number(main.floors);
  const grid = Number(SPEC.grid) || 0;
  const sideBearing = (k) => norm(SIDES[k] + grid);
  const facingWords = typeof opts.facingWords === 'function' ? opts.facingWords : () => '';
  const state = { floor: 0, side: '', live: false };

  /* DOM */
  const root = el('div', 'nlms', null, { dir: rtl ? 'rtl' : 'ltr', lang });
  const ssr = container.querySelector('img.nlps-ssr-poster');
  const poster = ssr || el('img', 'nlms-poster', null, { alt: SPEC.posterAlt || W.aria, decoding: 'async' });
  poster.classList.add('nlms-poster');
  if (!ssr) poster.src = opts.poster || base + 'poster.jpg';
  root.appendChild(poster);
  const wrap = el('div', 'nlms-canvas', root, { role: 'img', 'aria-label': (SPEC.name ? SPEC.name + ': ' : '') + W.aria });
  const chip = el('div', 'nlms-chip', root, { 'aria-live': 'polite' });
  chip.hidden = true;
  const drag = el('div', 'nlms-drag', root);
  drag.textContent = W.drag;
  const cap = el('p', 'nlms-cap rbs-caption', root);
  cap.textContent = W.caption;
  container.textContent = '';
  container.appendChild(root);

  /* the floor card, in the page's flow under the stage (the bridge's host), never on the building */
  const host = opts.cardHost || el('div', '', container.parentNode || container);
  const card = el('div', 'nlms-card', host, { role: 'region', 'aria-label': W.floor, dir: rtl ? 'rtl' : 'ltr', lang });
  const h3 = el('h3', '', card);
  const note = el('p', 'nlms-note', card);
  const row = el('div', 'nlms-row', card);
  const down = el('button', 'nlms-step', row, { type: 'button', 'aria-label': W.down });
  down.textContent = '−';
  const range = el('input', 'nlms-range', row, { type: 'range', min: '1', max: String(floors), step: '1', 'aria-label': W.floor });
  const up = el('button', 'nlms-step', row, { type: 'button', 'aria-label': W.up });
  up.textContent = '+';
  const sidesEl = el('div', 'nlms-sides', card, { role: 'group', 'aria-label': W.side });
  const sideBtns = {};
  for (const k of ['w', 'n', 'e', 's']) {
    const b = el('button', 'nlms-side', sidesEl, { type: 'button', 'aria-pressed': 'false', 'data-side': k });
    sideBtns[k] = b;
    b.addEventListener('click', () => setFacing(k, 'user'));
  }
  const hint = el('p', 'nlms-hint', card);
  hint.textContent = W.pick;
  const acts = el('div', 'nlms-acts', card);
  const actBtn = (id, label, sec) => {
    const b = el('button', 'nlms-act' + (sec ? ' nlms-act--sec' : ''), acts, { type: 'button', 'data-act': id });
    b.textContent = label;
    return b;
  };
  actBtn('cta', W.cta, false).addEventListener('click', () => {
    if (!state.floor) setFloor(Math.round(floors * 0.6), 'auto');
    emit('nl:floor-cta', { floor: state.floor, bearing: state.side ? sideBearing(state.side) : null });
  });
  actBtn('view', W.view, true).addEventListener('click', () => {
    if (!state.side) setFacing('w', 'auto');
    emit('nl:floor-action', { action: 'view', floor: state.floor, unit: state.floor + '-' + state.side });
  });
  actBtn('design', W.design, true).addEventListener('click', () => emit('nl:floor-action', { action: 'design', floor: state.floor, unit: state.floor + '-' + state.side }));
  down.addEventListener('click', () => setFloor(Math.max(1, (state.floor || floors) - 1), 'user'));
  up.addEventListener('click', () => setFloor(Math.min(floors, (state.floor || 0) + 1), 'user'));
  range.addEventListener('input', () => setFloor(Number(range.value), 'user'));

  function paintCard() {
    const f = state.floor;
    h3.innerHTML = '';
    const n = el('b');
    if (f) {
      n.textContent = String(f);
      h3.append(document.createTextNode(W.floor + ' '), n, document.createTextNode(' ' + W.of + ' ' + floors + (SPEC.mainLabel ? ' · ' + SPEC.mainLabel : '')));
    } else {
      n.textContent = String(floors);
      h3.append(n, document.createTextNode(' ' + W.floors));
    }
    const fn = f && typeof opts.floorNote === 'function' ? opts.floorNote(f) : '';
    note.textContent = fn || '';
    note.hidden = !fn;
    range.value = String(f || Math.round(floors / 2));
    for (const k in sideBtns) {
      const b = sideBtns[k];
      const words = facingWords(sideBearing(k)) || '';
      b.innerHTML = '';
      const strong = document.createElement('span');
      strong.textContent = words || W.dirs[k];
      const sm = document.createElement('small');
      sm.textContent = W.example;
      b.append(strong, sm);
      b.setAttribute('aria-pressed', state.side === k ? 'true' : 'false');
      b.disabled = !f;
    }
    hint.textContent = f ? W.faceHint : W.pick;
    chip.hidden = !f;
    if (f) {
      chip.innerHTML = '';
      const cb = el('b'); cb.textContent = String(f);
      chip.append(document.createTextNode(W.floor + ' '), cb, document.createTextNode(' ' + W.of + ' ' + floors + (state.side && facingWords(sideBearing(state.side)) ? ' · ' + facingWords(sideBearing(state.side)) : '')));
    }
  }

  function setFloor(f, src) {
    f = Math.max(1, Math.min(floors, Math.round(Number(f) || 1)));
    const changed = f !== state.floor;
    state.floor = f;
    paintCard();
    if (scene3d) scene3d.mark(f, state.side);
    if (changed) {
      emit('nl:floor', { floor: f, heightM: f * floorH });
      if (src === 'user') track('floor_select', { floor: f, tower: SPEC.mainId || 'main' });
    }
    if (state.side) emitFacing(src);
  }
  function emitFacing(src) {
    const b = sideBearing(state.side);
    const d = { floor: state.floor, heightM: state.floor * floorH, bearing: b, unit: state.floor + '-' + state.side, toward: facingWords(b) };
    emit('nl:facing', d);
    if (src === 'user') track('direction_select', { floor: state.floor, bearing: b, dir: state.side, unit: d.unit });
  }
  function setFacing(k, src) {
    if (!SIDES.hasOwnProperty(k)) return;
    if (!state.floor) state.floor = Math.round(floors * 0.6);
    state.side = k;
    paintCard();
    if (scene3d) scene3d.mark(state.floor, k);
    emit('nl:floor', { floor: state.floor, heightM: state.floor * floorH });
    emitFacing(src);
  }
  paintCard();

  /* 3D */
  let scene3d = null;
  let resolveReady;
  const ready = new Promise((r) => { resolveReady = r; });
  const can3d = webglOk() || opts.force3D;
  const start = () => {
    if (scene3d || !can3d) return;
    scene3d = build3d();
    resolveReady(true);
  };
  if (!can3d) { resolveReady(false); drag.hidden = true; }
  else if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((es) => { if (es.some((e) => e.isIntersecting)) { io.disconnect(); start(); } }, { rootMargin: '200px' });
    io.observe(root);
  } else start();

  function build3d() {
    const phone = Math.min(screen.width, screen.height) < 600 && matchMedia('(pointer: coarse)').matches;
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false, powerPreference: 'high-performance' });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, phone ? 2 : 1.75));
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.05;
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    wrap.appendChild(renderer.domElement);
    const scene = new THREE.Scene();
    scene.background = sky();
    scene.fog = new THREE.Fog(0x9fbfca, 900, 2600);
    const pmrem = new THREE.PMREMGenerator(renderer);
    scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;

    const camera = new THREE.PerspectiveCamera(34, 1, 2, 6000);
    const topY = floors * floorH;
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.08;
    controls.enablePan = false;
    controls.minDistance = Math.max(60, topY * 0.55);
    controls.maxDistance = Math.max(700, topY * 4.2);
    controls.maxPolarAngle = Math.PI * 0.47;
    controls.target.set(0, topY * 0.42, 0);
    controls.autoRotate = !matchMedia('(prefers-reduced-motion: reduce)').matches;
    controls.autoRotateSpeed = 0.45;
    // the first view: from the sea side (west-south-west), a little above the top
    const dist = Math.max(300, topY * 2.8);
    const az = ((Number(SPEC.camAz) || 250) * Math.PI) / 180; // the bearing the camera stands at, seen from the tower
    camera.position.set(Math.sin(az) * dist, topY * 1.05, -Math.cos(az) * dist);

    scene.add(new THREE.HemisphereLight(0xe3f0f4, 0x24363d, 0.95));
    const sun = new THREE.DirectionalLight(0xffffff, 2.1);
    sun.position.set(-420, 520, 260);
    sun.castShadow = true;
    sun.shadow.mapSize.set(phone ? 1024 : 2048, phone ? 1024 : 2048);
    const sc = Math.max(220, topY * 1.4);
    Object.assign(sun.shadow.camera, { left: -sc, right: sc, top: sc, bottom: -sc, near: 50, far: 2200 });
    sun.shadow.bias = -0.0004;
    scene.add(sun);

    const ground = new THREE.Mesh(new THREE.CircleGeometry(2600, 64), new THREE.MeshStandardMaterial({ color: C.ground, roughness: 0.95 }));
    ground.rotation.x = -Math.PI / 2;
    ground.receiveShadow = true;
    scene.add(ground);

    /* the project's buildings: the main tower as stacked floors (pickable), the others as solid volumes */
    const glass = new THREE.MeshPhysicalMaterial({ color: 0xd2e6ee, metalness: 0.15, roughness: 0.18, clearcoat: 0.6, envMapIntensity: 1.1 });
    const solid = new THREE.MeshStandardMaterial({ color: 0xe9eff1, roughness: 0.55, metalness: 0.05 });
    const pickMat = new THREE.MeshStandardMaterial({ color: C.magenta, emissive: C.magenta, emissiveIntensity: 0.55, roughness: 0.4 });
    const hoverMat = new THREE.MeshStandardMaterial({ color: C.sea, emissive: C.sea, emissiveIntensity: 0.35, roughness: 0.35 });
    const edgeMat = new THREE.LineBasicMaterial({ color: C.abyss, transparent: true, opacity: 0.38 });
    const edgeThin = new THREE.LineBasicMaterial({ color: C.deep, transparent: true, opacity: 0.16 });
    const proj = new THREE.Group();
    proj.rotation.y = (-grid * Math.PI) / 180; // the lot's grid, turned from true north
    scene.add(proj);
    const floorMeshes = [];
    for (const b of SPEC.buildings) {
      const bh = Number(b.floors) * floorH + (Number(b.baseM) || 0);
      const g = new THREE.Group();
      g.position.set(Number(b.x) || 0, 0, Number(b.z) || 0);
      g.rotation.y = ((Number(b.rot) || 0) * Math.PI) / 180;
      proj.add(g);
      if (b.baseM) { // a commercial base under the residential floors (published as such)
        const base = new THREE.Mesh(new THREE.BoxGeometry(b.w * 1.12, b.baseM, b.d * 1.12), solid);
        base.position.y = b.baseM / 2; base.castShadow = base.receiveShadow = true; g.add(base);
      }
      if (b === main) {
        const slab = new THREE.BoxGeometry(b.w, floorH * 0.9, b.d);
        const edges = new THREE.EdgesGeometry(slab);
        for (let i = 1; i <= floors; i += 1) {
          const m = new THREE.Mesh(slab, glass);
          m.position.y = (Number(b.baseM) || 0) + (i - 0.5) * floorH;
          m.castShadow = true; m.receiveShadow = true;
          m.userData.floor = i;
          g.add(m);
          floorMeshes.push(m);
          { const ln = new THREE.LineSegments(edges, i % 5 === 0 || i === floors ? edgeMat : edgeThin); ln.position.copy(m.position); g.add(ln); }
        }
        const crown = new THREE.Mesh(new THREE.BoxGeometry(b.w * 0.6, floorH * 1.4, b.d * 0.6), solid);
        crown.position.y = (Number(b.baseM) || 0) + floors * floorH + floorH * 0.7; crown.castShadow = true; g.add(crown);
      } else {
        const hgt = Number(b.floors) * floorH;
        const box = new THREE.BoxGeometry(b.w, hgt, b.d);
        const m = new THREE.Mesh(box, solid);
        m.position.y = (Number(b.baseM) || 0) + hgt / 2; m.castShadow = m.receiveShadow = true; g.add(m);
        const ln = new THREE.LineSegments(new THREE.EdgesGeometry(box), edgeMat); ln.position.copy(m.position); g.add(ln);
        for (let i = 1; i < Number(b.floors); i += 1) { // floor lines, so a low building reads as storeys too
          const fl = new THREE.Mesh(new THREE.BoxGeometry(b.w + 0.25, 0.18, b.d + 0.25), new THREE.MeshBasicMaterial({ color: 0xaab8be }));
          fl.position.y = (Number(b.baseM) || 0) + i * floorH; g.add(fl);
        }
      }
      void bh;
    }
    const mainGroup = floorMeshes.length ? floorMeshes[0].parent : null;

    /* the direction wedge from the picked floor (this stage's own, not the area map's beam) */
    const wedge = new THREE.Mesh(new THREE.CircleGeometry(150, 32, -Math.PI / 7, (2 * Math.PI) / 7), new THREE.MeshBasicMaterial({ color: C.magenta, transparent: true, opacity: 0.22, side: THREE.DoubleSide, depthWrite: false }));
    wedge.rotation.x = -Math.PI / 2;
    wedge.visible = false;
    scene.add(wedge);

    /* the city around (GIS, as it stands) and the sea */
    if (SPEC.city) {
      fetch(new URL(SPEC.city, base).href).then((r) => (r.ok ? r.json() : null)).then((city) => {
        if (!city || !city.origin) return;
        const tf = cityToLocal(city, origin);
        const geos = [];
        for (const row of city.b || []) {
          const hgt = Math.max(3, Number(row[0]) || 6);
          const pts = [];
          for (let i = 3; i + 1 < row.length; i += 2) { const p = tf(row[i], row[i + 1]); pts.push(new THREE.Vector2(p.x, -p.z)); }
          if (pts.length < 3) continue;
          const c0 = pts[0];
          if (Math.hypot(c0.x, c0.y) < 28) continue; // never on the project's own spot
          try {
            const gg = new THREE.ExtrudeGeometry(new THREE.Shape(pts), { depth: hgt, bevelEnabled: false });
            gg.rotateX(-Math.PI / 2);
            geos.push(gg);
          } catch (e) { /* a broken outline is skipped */ }
        }
        const f = city.f || [];
        for (let i = 0; i + 5 < f.length; i += 6) {
          const p = tf(f[i], f[i + 1]);
          if (Math.hypot(p.x, p.z) > 2400) continue;
          const bx = new THREE.BoxGeometry(Number(f[i + 2]) || 10, Number(f[i + 5]) || 10, Number(f[i + 3]) || 10);
          bx.rotateY(-((Number(f[i + 4]) || 0) - (Number(city.origin.grid_deg) || 0)) * Math.PI / 180);
          bx.translate(p.x, (Number(f[i + 5]) || 10) / 2, p.z);
          geos.push(bx);
        }
        if (geos.length) {
          const merged = mergeGeometries(geos.map((g) => g.index ? g.toNonIndexed() : g), false);
          geos.forEach((g) => g.dispose());
          if (merged) {
            const m = new THREE.Mesh(merged, new THREE.MeshStandardMaterial({ color: C.city, roughness: 0.92 }));
            m.castShadow = m.receiveShadow = true;
            scene.add(m);
          }
        }
        for (const gz of city.g || []) {
          const pts = [];
          for (let i = 1; i + 1 < gz.length; i += 2) { const p = tf(gz[i], gz[i + 1]); pts.push(new THREE.Vector2(p.x, -p.z)); }
          if (pts.length < 3) continue;
          const sg = new THREE.ShapeGeometry(new THREE.Shape(pts)); sg.rotateX(-Math.PI / 2);
          const gm = new THREE.Mesh(sg, new THREE.MeshStandardMaterial({ color: C.green, roughness: 1 })); gm.position.y = 0.15; gm.receiveShadow = true; scene.add(gm);
        }
        // the sea: west of the coastline (OSM line where the file has one, else the beaches' straight fit)
        const coast = city.coast || null;
        if (coast) {
          let line = Array.isArray(coast.line) && coast.line.length > 2 ? coast.line : null;
          if (!line && coast.x0 != null) { line = []; for (let z = -3200; z <= 3200; z += 400) line.push([coast.x0 + coast.k * z, z]); }
          if (line) {
            const pts = line.map((q) => { const p = tf(q[0], q[1]); return new THREE.Vector2(p.x, -p.z); });
            const far = -4200;
            pts.push(new THREE.Vector2(far, pts[pts.length - 1].y), new THREE.Vector2(far, pts[0].y));
            const sg = new THREE.ShapeGeometry(new THREE.Shape(pts)); sg.rotateX(-Math.PI / 2);
            const sea = new THREE.Mesh(sg, new THREE.MeshStandardMaterial({ color: C.sea, roughness: 0.25, metalness: 0.2 }));
            sea.position.y = 0.3; scene.add(sea);
          }
        }
        dirty = true;
      }).catch(() => {});
    }

    /* picking: a tap (not a drag) on a floor picks it; a hover shows it */
    const ray = new THREE.Raycaster();
    const ptr = new THREE.Vector2();
    let downAt = null, hovered = null, dirty = true, userMoved = false;
    const hit = (ev) => {
      const r = renderer.domElement.getBoundingClientRect();
      ptr.set(((ev.clientX - r.left) / r.width) * 2 - 1, -((ev.clientY - r.top) / r.height) * 2 + 1);
      ray.setFromCamera(ptr, camera);
      const h = ray.intersectObjects(floorMeshes, false)[0];
      return h ? h.object : null;
    };
    renderer.domElement.addEventListener('pointerdown', (e) => { downAt = { x: e.clientX, y: e.clientY }; controls.autoRotate = false; });
    renderer.domElement.addEventListener('pointerup', (e) => {
      if (!downAt) return;
      const moved = Math.hypot(e.clientX - downAt.x, e.clientY - downAt.y);
      downAt = null;
      if (moved > 7) return;
      const m = hit(e);
      if (m) { setFloor(m.userData.floor, 'user'); if (!state.side) setFacing('w', 'user'); }
    });
    renderer.domElement.addEventListener('pointermove', (e) => {
      if (e.pointerType !== 'mouse' || downAt) return;
      const m = hit(e);
      if (m !== hovered) {
        if (hovered && hovered.userData.floor !== state.floor) hovered.material = glass;
        hovered = m;
        if (m && m.userData.floor !== state.floor) m.material = hoverMat;
        renderer.domElement.style.cursor = m ? 'pointer' : 'grab';
        dirty = true;
      }
    });
    controls.addEventListener('start', () => { userMoved = true; drag.hidden = true; });
    controls.addEventListener('change', () => { dirty = true; });

    function mark(f, side) {
      for (const m of floorMeshes) m.material = m.userData.floor === f ? pickMat : glass;
      if (f && side && mainGroup) {
        const wp = new THREE.Vector3();
        floorMeshes[f - 1].getWorldPosition(wp);
        wedge.position.set(wp.x, wp.y, wp.z);
        wedge.rotation.z = 0;
        // the circle's 0 angle points +x (east); a true bearing b (clockwise from north) is angle (90 - b) on the ground
        wedge.rotation.set(-Math.PI / 2, 0, ((90 - sideBearing(side)) * Math.PI) / 180);
        wedge.visible = true;
      } else wedge.visible = false;
      if (f && !userMoved) controls.target.set(0, f * floorH, 0);
      dirty = true;
    }

    const size = () => {
      const w = Math.max(1, root.clientWidth), h = Math.max(1, root.clientHeight);
      renderer.setSize(w, h, false);
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      dirty = true;
    };
    size();
    if ('ResizeObserver' in window) new ResizeObserver(size).observe(root); else addEventListener('resize', size);

    let visible = true;
    if ('IntersectionObserver' in window) new IntersectionObserver((es) => { visible = es.some((e) => e.isIntersecting); }).observe(root);
    let first = true;
    const loop = () => {
      requestAnimationFrame(loop);
      if (!visible || document.hidden) return;
      const moving = controls.update();
      if (moving || controls.autoRotate || dirty) {
        renderer.render(scene, camera);
        dirty = false;
        if (first) { first = false; root.classList.add('is-live'); state.live = true; }
      }
    };
    loop();
    return { mark, renderer, scene, camera };
  }

  return {
    ready,
    floors,
    selectUnit(id, src) {
      const m = /^(\d+)-([nesw])$/.exec(String(id || ''));
      if (!m) return false;
      setFloor(Number(m[1]), src || 'user');
      setFacing(m[2], src || 'user');
      return true;
    },
    setFloor: (f) => setFloor(f, 'api'),
    setFacing: (k) => setFacing(k, 'api'),
    get floor() { return state.floor; },
  };
}
