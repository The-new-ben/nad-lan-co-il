/*!
 * nad-lan.co.il · Rentals manager · rm-3d.js · v1 (1.10.2026)
 * A procedural drawing of the landlord's building (his floors × his apartments, never a fixed model) and a 3D floor
 * plan ("digital twin") of one apartment with asset pins. Both are illustrations, never the real architecture, and
 * both say so on screen.
 * ES module on three.js r170 through the page's import map ("three", "three/addons/").
 * Registers window.NLRM3D = { mountBuilding, mountApartment, version: "1" } and dispatches "nlrm3d:ready".
 * Phone law: a vertical one-finger swipe on the canvas scrolls the page (touch-action: pan-y + a capture-phase
 * gesture split, the world.js pattern); a sideways one turns the model; two fingers zoom; the wheel zooms only with
 * Ctrl/⌘ held.
 */
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

const VERSION = '1';
const FH = 3.05;   // storey height (m)
const GH = 4.1;    // entrance (ground) storey height
const CW = 4.4;    // stair + elevator core width
const WALL_H = 2.7;

const PAL = { paper: '#f7f6f2', ink: '#14212b', sea: '#2f6f86', cream: '#efebe3', glass: '#8fa9b5', wall: '#fbfaf7', edge: '#d9d4ca' };
const STATUS = { ok: '#2e7d5b', due: '#a15c00', late: '#b3261e', vacant: '#6b7680', ending: '#2f6f86' };
const TONE = { living: '#e9e2d3', kitchen: '#e9e2d3', hall: '#e9e2d3', bedroom: '#e6e8e1', storage: '#e6e8e1', mamad: '#e3e0ea', bath: '#dde7ea', toilet: '#dde7ea', laundry: '#dde7ea', balcony: '#e4ddd0' };
const tintOf = (st) => new THREE.Color(STATUS[st] || STATUS.ok).lerp(new THREE.Color(PAL.cream), 0.14);
const ROOM_KINDS = ['living', 'kitchen', 'bedroom', 'mamad', 'bath', 'toilet', 'hall', 'balcony', 'storage', 'laundry'];

const TXT = {
  he: {
    floor: 'קומה {n}', ground: 'קומת כניסה', roof: 'גג',
    empty: 'לחצו כדי להוסיף כאן דירה',
    illus: 'הדמיה להמחשה בלבד', illusGen: 'הדמיה להמחשה בלבד · אפשר להעלות תוכנית',
    wheel: '{k} + גלגלת לזום', north: 'צ', sqm: 'מ״ר',
    bAria: 'הדמיית הבניין: {f} קומות, {u} דירות בקומה', aAria: 'תוכנית הדירה בתלת־ממד',
    noGL: 'הדפדפן הזה לא מציג תלת־ממד', warranty: 'האחריות הסתיימה',
    status: { ok: 'שולם', due: 'לתשלום', late: 'באיחור', vacant: 'פנויה', ending: 'חוזה מסתיים' },
    rooms: { living: 'סלון', kitchen: 'מטבח', bedroom: 'חדר שינה', mamad: 'ממ״ד', bath: 'אמבטיה', toilet: 'שירותי אורחים', hall: 'מבואה', balcony: 'מרפסת', storage: 'מחסן', laundry: 'חדר כביסה', master: 'חדר הורים', study: 'חדר עבודה' },
    assets: { boiler: 'דוד מים', ac: 'מזגן', panel: 'לוח חשמל', water_meter: 'מונה מים', dishwasher: 'מדיח כלים', fridge: 'מקרר', oven: 'תנור', washer: 'מכונת כביסה' },
  },
  en: {
    floor: 'Floor {n}', ground: 'Entrance floor', roof: 'Roof',
    empty: 'Click to add a unit here',
    illus: 'Illustration only', illusGen: 'Illustration only · upload your floor plan',
    wheel: '{k} + wheel to zoom', north: 'N', sqm: 'm²',
    bAria: 'Building illustration: {f} floors, {u} units per floor', aAria: '3D floor plan of the apartment',
    noGL: 'This browser cannot show 3D', warranty: 'Warranty expired',
    status: { ok: 'Paid', due: 'Due', late: 'Late', vacant: 'Vacant', ending: 'Lease ending' },
    rooms: { living: 'Living room', kitchen: 'Kitchen', bedroom: 'Bedroom', mamad: 'Safe room (mamad)', bath: 'Bathroom', toilet: 'Guest toilet', hall: 'Hall', balcony: 'Balcony', storage: 'Storage', laundry: 'Laundry', master: 'Main bedroom', study: 'Study' },
    assets: { boiler: 'Water heater', ac: 'Air conditioner', panel: 'Electric panel', water_meter: 'Water meter', dishwasher: 'Dishwasher', fridge: 'Fridge', oven: 'Oven', washer: 'Washing machine' },
  },
};

const ICONS = {
  boiler: '<rect x="5" y="1.8" width="6" height="12.4" rx="3"/><path d="M8 6v4.2"/>',
  ac: '<rect x="1.8" y="4" width="12.4" height="6" rx="1.5"/><path d="M4.5 12.6h7M4.2 7.4h7.6"/>',
  panel: '<path d="M9.2 1.6 4.4 9h3.7l-1.3 5.4L11.6 7H7.9z"/>',
  water_meter: '<path d="M8 2.1s4.1 4.6 4.1 7.3A4.1 4.1 0 0 1 3.9 9.4C3.9 6.7 8 2.1 8 2.1z"/>',
  dishwasher: '<rect x="2.6" y="2" width="10.8" height="12" rx="1.5"/><path d="M2.6 5.2h10.8"/><circle cx="8" cy="9.6" r="2.3"/>',
  washer: '<rect x="2.6" y="2" width="10.8" height="12" rx="1.5"/><circle cx="8" cy="9" r="3"/><path d="M4.6 4.4h2"/>',
  fridge: '<rect x="4" y="1.6" width="8" height="12.8" rx="1.5"/><path d="M4 6.4h8M6 3.6v1.4M6 8.6v2.2"/>',
  oven: '<rect x="2" y="2.6" width="12" height="10.8" rx="1.5"/><rect x="4.4" y="6.4" width="7.2" height="4.6" rx=".8"/><path d="M4.6 4.4h1M7.4 4.4h1"/>',
  other: '<circle cx="8" cy="8" r="3.4"/>',
};

const CSS = `
.nlrm3d{position:relative;width:100%;height:100%;min-height:300px;overflow:hidden;font-family:Assistant,"Segoe UI",Arial,sans-serif;color:#14212b;-webkit-tap-highlight-color:transparent;-webkit-user-select:none;user-select:none;isolation:isolate}
.nlrm3d-cv{position:absolute;inset:0;width:100%;height:100%;display:block;touch-action:pan-y;outline:0}
.nlrm3d-ov{position:absolute;inset:0;pointer-events:none;overflow:hidden;z-index:1}
.nlrm3d-tag{position:absolute;left:0;top:0;box-sizing:border-box;min-width:44px;min-height:44px;margin:0;padding:0 2px;border:0;background:transparent;display:flex;align-items:center;justify-content:center;pointer-events:auto;cursor:pointer;font:600 13px/1.2 Assistant,"Segoe UI",Arial,sans-serif;color:#14212b;will-change:transform;-webkit-appearance:none;appearance:none}
.nlrm3d-tag.is-off{visibility:hidden;pointer-events:none}
.nlrm3d-pill{display:inline-flex;align-items:center;gap:6px;box-sizing:border-box;height:28px;padding:0 10px;border-radius:14px;background:rgba(255,255,255,.96);border:1px solid #d9d4ca;box-shadow:0 1px 2px rgba(20,33,43,.06),0 6px 14px -8px rgba(20,33,43,.35);white-space:nowrap;transition:border-color .15s,box-shadow .15s}
.nlrm3d-dot{width:10px;height:10px;border-radius:50%;flex:none;box-shadow:0 0 0 2px #fff}
.nlrm3d-tag.is-dot .nlrm3d-txt,.nlrm3d-tag.is-dot .nlrm3d-sub,.nlrm3d-tag.is-compact .nlrm3d-sub{display:none}
.nlrm3d-tag.is-dot .nlrm3d-pill{width:22px;height:22px;padding:0;justify-content:center;border-radius:11px}
.nlrm3d-tag:hover .nlrm3d-pill,.nlrm3d-tag.is-on .nlrm3d-pill{border-color:#2f6f86;box-shadow:0 0 0 1px #2f6f86,0 6px 14px -8px rgba(20,33,43,.35)}
.nlrm3d-tag:focus{outline:0}
.nlrm3d-tag:focus-visible .nlrm3d-pill{box-shadow:0 0 0 2px #fff,0 0 0 4px #2f6f86}
.nlrm3d-room .nlrm3d-pill{flex-direction:column;align-items:center;justify-content:center;gap:0;height:auto;min-height:24px;padding:3px 8px;border-radius:8px;background:rgba(251,250,247,.86);border-color:rgba(217,212,202,.7);box-shadow:none}
.nlrm3d-room .nlrm3d-sub{font-size:12px;font-weight:500;color:#5a6670;line-height:1.15}
.nlrm3d-room.is-dot .nlrm3d-pill{width:10px;height:10px;min-height:10px;padding:0;border:0;border-radius:5px;background:#5a6670;box-shadow:0 0 0 2px #fbfaf7,0 1px 4px rgba(20,33,43,.3)}
.nlrm3d-pin .nlrm3d-ico{width:20px;height:20px;display:grid;place-items:center;border-radius:50%;background:#14212b;color:#fff;flex:none}
.nlrm3d-pin .nlrm3d-ico svg{width:13px;height:13px;fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}
.nlrm3d-pin .nlrm3d-pill{padding:0 10px 0 4px}
.nlrm3d[dir=rtl] .nlrm3d-pin .nlrm3d-pill{padding:0 4px 0 10px}
.nlrm3d-pin.is-warn .nlrm3d-ico{box-shadow:0 0 0 2px #fff,0 0 0 4px #a15c00}
.nlrm3d-pin.is-dot .nlrm3d-pill{width:auto;height:auto;padding:2px;border-radius:50%}
.nlrm3d-floor .nlrm3d-pill{height:26px;padding:0 9px;border-radius:7px;background:#14212b;border-color:#14212b;color:#fff;font-weight:600;font-size:12px}
.nlrm3d-floor.is-on .nlrm3d-pill,.nlrm3d-floor:hover .nlrm3d-pill{background:#2f6f86;border-color:#2f6f86;box-shadow:0 0 0 2px #fff,0 6px 14px -8px rgba(20,33,43,.45)}
.nlrm3d-floor.is-dot .nlrm3d-pill{width:14px;height:14px;padding:0;border-radius:4px}
.nlrm3d-bdg{display:inline-flex;align-items:center;gap:2px;height:18px;padding:0 5px;border-radius:9px;font:700 11px/1 Assistant,"Segoe UI",Arial,sans-serif;color:#fff;background:#a15c00}
.nlrm3d-bdg svg{width:11px;height:11px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.nlrm3d-bdg--late{background:#b3261e}
.nlrm3d-bdg--end{background:#2f6f86}
.nlrm3d-tag.is-dot .nlrm3d-bdg{display:none}
.nlrm3d-pin.is-open .nlrm3d-ico{background:#b3261e;box-shadow:0 0 0 2px #fff,0 0 0 4px #b3261e}
.nlrm3d-cap{position:absolute;bottom:10px;inset-inline-start:10px;z-index:2;max-width:calc(100% - 20px);box-sizing:border-box;padding:3px 10px;border-radius:999px;background:rgba(255,255,255,.9);border:1px solid #e3dfd6;font:600 12px/1.5 Assistant,"Segoe UI",Arial,sans-serif;color:#4c5862;pointer-events:none;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.nlrm3d-tip{position:absolute;left:0;top:0;z-index:3;padding:6px 10px;border-radius:8px;background:#14212b;color:#fff;font:600 13px/1.35 Assistant,"Segoe UI",Arial,sans-serif;pointer-events:none;opacity:0;transition:opacity .12s;white-space:nowrap;box-shadow:0 8px 20px -10px rgba(20,33,43,.6)}
.nlrm3d-tip span{display:block;font-weight:500;font-size:12px;color:#c9d3da}
.nlrm3d-tip.is-on{opacity:1}
.nlrm3d-hint{position:absolute;left:50%;top:12px;z-index:3;transform:translateX(-50%);padding:6px 12px;border-radius:999px;background:rgba(20,33,43,.84);color:#fff;font:600 13px/1.3 Assistant,"Segoe UI",Arial,sans-serif;pointer-events:none;opacity:0;transition:opacity .2s;white-space:nowrap}
.nlrm3d-hint.is-on{opacity:1}
.nlrm3d--nogl{display:grid;place-items:center;background:#f7f6f2;border:1px solid #e3dfd6;border-radius:12px}
@media (prefers-reduced-motion:reduce){.nlrm3d *{transition:none!important}}
`;

/* ------------------------------------------------------------------ small helpers */
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const lerp = (a, b, t) => a + (b - a) * t;
const ease = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
const esc = (s) => String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const fmt = (s, map) => String(s).replace(/\{(\w+)\}/g, (m, k) => (map[k] == null ? m : map[k]));
function hash(a, b, c = 0) {
  let h = Math.imul((a | 0) + 0x9e3779b9, 0x85ebca6b) ^ Math.imul((b | 0) + 0x7f4a7c15, 0xc2b2ae35) ^ Math.imul((c | 0) + 0x165667b1, 0x27d4eb2f);
  h ^= h >>> 15; h = Math.imul(h, 0x2c1b3c6d); h ^= h >>> 12; h = Math.imul(h, 0x297a2d39); h ^= h >>> 15;
  return (h >>> 0) / 4294967296;
}
function injectCss() {
  if (document.getElementById('nlrm3d-css')) return;
  const s = document.createElement('style');
  s.id = 'nlrm3d-css';
  s.textContent = CSS;
  (document.head || document.documentElement).appendChild(s);
}
const std = (c, r = 0.9, m = 0, extra) => new THREE.MeshStandardMaterial(Object.assign({ color: c, roughness: r, metalness: m }, extra || {}));
const _q = new THREE.Quaternion(), _eu = new THREE.Euler(0, 0, 0, 'YXZ'), _p = new THREE.Vector3(), _s = new THREE.Vector3();
function m4(x, y, z, sx, sy, sz, ry = 0, rx = 0, rz = 0) {
  _eu.set(rx, ry, rz, 'YXZ');
  _q.setFromEuler(_eu);
  return new THREE.Matrix4().compose(_p.set(x, y, z), _q, _s.set(sx, sy, sz));
}
function instanced(geo, mat, list, opt = {}) {
  if (!list.length) { geo.dispose(); return null; }
  const m = new THREE.InstancedMesh(geo, mat, list.length);
  for (let i = 0; i < list.length; i++) m.setMatrixAt(i, list[i]);
  m.instanceMatrix.needsUpdate = true;
  m.castShadow = opt.cast !== false;
  m.receiveShadow = opt.receive !== false;
  if (opt.colors) { const c = new THREE.Color(); opt.colors.forEach((hex, i) => m.setColorAt(i, c.set(hex))); m.instanceColor.needsUpdate = true; }
  m.computeBoundingSphere();
  m.computeBoundingBox();
  if (opt.name) m.name = opt.name;
  return m;
}
function colorize(g, hex, capHex) {
  const n = g.attributes.position.count, a = new Float32Array(n * 3);
  const c = new THREE.Color(hex), k = capHex ? new THREE.Color(capHex) : c;
  for (let i = 0; i < n; i++) { const cc = capHex && i >= 8 && i < 12 ? k : c; a[i * 3] = cc.r; a[i * 3 + 1] = cc.g; a[i * 3 + 2] = cc.b; }
  g.setAttribute('color', new THREE.BufferAttribute(a, 3));
  return g;
}
/** Collects geometries by material key and merges each key into one mesh (one draw call per material). */
class Merge {
  constructor() { this.m = new Map(); }
  add(key, g) { let a = this.m.get(key); if (!a) this.m.set(key, (a = [])); a.push(g); return g; }
  box(key, w, h, d, x, y, z, ry = 0) {
    if (w <= 0 || h <= 0 || d <= 0) return null;
    const g = new THREE.BoxGeometry(w, h, d);
    if (ry) g.rotateY(ry);
    g.translate(x, y, z);
    return this.add(key, g);
  }
  meshes(mats, group, noCast = []) {
    for (const [k, list] of this.m) {
      const g = list.length === 1 ? list[0] : mergeGeometries(list, false);
      if (list.length > 1) list.forEach((x) => x.dispose());
      if (!g) continue;
      const mesh = new THREE.Mesh(g, mats[k]);
      mesh.castShadow = !noCast.includes(k);
      mesh.receiveShadow = true;
      mesh.name = k;
      group.add(mesh);
      this[k] = mesh;
    }
    this.m.clear();
  }
}
function disposeTree(root) {
  const seen = new Set();
  root.traverse((o) => {
    if (o.geometry && !seen.has(o.geometry)) { seen.add(o.geometry); o.geometry.dispose(); }
    const mats = o.material ? (Array.isArray(o.material) ? o.material : [o.material]) : [];
    for (const m of mats) {
      if (!m || seen.has(m)) continue;
      seen.add(m);
      for (const k of ['map', 'alphaMap', 'emissiveMap', 'normalMap', 'roughnessMap']) if (m[k] && !seen.has(m[k])) { seen.add(m[k]); m[k].dispose(); }
      m.dispose();
    }
    if (o.isInstancedMesh && o.dispose) o.dispose();
  });
}
function mq(q) { try { return window.matchMedia(q).matches; } catch (e) { return false; } }

/* ------------------------------------------------------------------ the stage (shared by both mounts) */
const LIVE = new WeakMap();
const _v = new THREE.Vector3();

function createStage(el, o, kind) {
  if (!el || !el.appendChild) throw new Error('NLRM3D: a mount element is required');
  const prev = LIVE.get(el);
  if (prev && prev.dispose) { try { prev.dispose(); } catch (e) { /* already gone */ } }
  injectCss();
  const lang = o.lang === 'en' ? 'en' : 'he';
  const base = TXT[lang];
  const T = Object.assign({}, base, o.labels || {});
  T.status = Object.assign({}, base.status, (o.labels && o.labels.status) || {});
  T.rooms = Object.assign({}, base.rooms, (o.labels && o.labels.rooms) || {});
  T.assets = Object.assign({}, base.assets, (o.labels && o.labels.assets) || {});
  const rtl = typeof o.rtl === 'boolean' ? o.rtl : lang === 'he';
  const coarse = mq('(pointer: coarse)');
  const phone = coarse && Math.min(window.innerWidth || 9999, (window.screen && window.screen.width) || 9999) < 820;
  const reduced = mq('(prefers-reduced-motion: reduce)');
  const mac = /Mac|iPhone|iPad/.test(navigator.platform || navigator.userAgent || '');

  const root = document.createElement('div');
  root.className = 'nlrm3d nlrm3d--' + kind;
  root.dir = rtl ? 'rtl' : 'ltr';
  root.lang = lang;
  if (el.clientHeight < 160) root.style.height = kind === 'building' ? 'min(78vh, 620px)' : 'min(70vh, 520px)';
  el.appendChild(root);

  const S = { el, root, kind, lang, T, rtl, phone, reduced, coarse, mac, alive: true, offs: [], hooks: {}, tween: null, userMoved: false, ready: false, W: 1, H: 1, raf: 0 };
  S.on = (t, type, fn, opt) => { t.addEventListener(type, fn, opt); S.offs.push(() => t.removeEventListener(type, fn, opt)); };

  let renderer = null;
  try {
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' });
  } catch (e) { renderer = null; }
  if (!renderer) {
    root.classList.add('nlrm3d--nogl');
    root.textContent = T.noGL;
    root.setAttribute('data-ready', '0');
    const stub = { ok: false, dispose() { root.remove(); if (LIVE.get(el) === stub) LIVE.delete(el); } };
    S.stub = stub;
    return S;
  }
  S.ok = true;
  S.renderer = renderer;
  renderer.setClearColor(0x000000, 0);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.0;
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, phone ? 1.5 : 2));
  S.shadows = !phone && !reduced;
  renderer.shadowMap.enabled = S.shadows;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  const cv = renderer.domElement;
  cv.className = 'nlrm3d-cv';
  cv.setAttribute('role', 'img');
  S.cv = cv;

  const ov = document.createElement('div'); ov.className = 'nlrm3d-ov';
  const tip = document.createElement('div'); tip.className = 'nlrm3d-tip'; tip.setAttribute('aria-hidden', 'true');
  const cap = document.createElement('div'); cap.className = 'nlrm3d-cap';
  const hint = document.createElement('div'); hint.className = 'nlrm3d-hint'; hint.setAttribute('aria-hidden', 'true');
  root.append(cv, ov, cap, tip, hint);
  S.ov = ov; S.cap = cap;

  const scene = new THREE.Scene();
  S.scene = scene;
  const pmrem = new THREE.PMREMGenerator(renderer);
  const env = new RoomEnvironment();
  S.envRT = pmrem.fromScene(env, 0.04);
  if (env.dispose) env.dispose();
  pmrem.dispose();
  scene.environment = S.envRT.texture;
  scene.environmentIntensity = kind === 'building' ? 0.32 : 0.36;
  renderer.toneMappingExposure = kind === 'building' ? 1.0 : 0.92;

  const camera = new THREE.PerspectiveCamera(kind === 'building' ? 30 : 34, 1, 0.3, 2000);
  S.camera = camera;
  const hemi = new THREE.HemisphereLight('#fbfaf6', '#cfc6b4', kind === 'building' ? 1.22 : 1.15);
  const sun = new THREE.DirectionalLight('#fff3e2', kind === 'building' ? 2.75 : 2.1);
  sun.castShadow = S.shadows;
  sun.shadow.mapSize.set(2048, 2048);
  sun.shadow.bias = -0.0004;
  sun.shadow.normalBias = 0.03;
  scene.add(hemi, sun, sun.target);
  S.sun = sun;
  S.placeSun = (box, theta, elev) => {
    const c = box.getCenter(new THREE.Vector3());
    const r = Math.max(4, box.getSize(new THREE.Vector3()).length() / 2);
    const dir = new THREE.Vector3().setFromSphericalCoords(1, Math.PI / 2 - elev, theta);
    sun.position.copy(c).addScaledVector(dir, r * 2.4);
    sun.target.position.copy(c);
    const sc = sun.shadow.camera;
    sc.left = -r; sc.right = r; sc.top = r; sc.bottom = -r; sc.near = r * 0.4; sc.far = r * 4.6;
    sc.updateProjectionMatrix();
  };

  const C = new OrbitControls(camera, cv);
  S.controls = C;
  C.enableDamping = !reduced;
  C.dampingFactor = 0.09;
  C.rotateSpeed = 0.6;
  C.zoomSpeed = 0.9;
  C.enablePan = false;
  C.enableZoom = false; // the wheel zooms only with Ctrl/⌘ (decided per event below); touch turns it on for the pinch
  C.touches.ONE = THREE.TOUCH.ROTATE;
  C.touches.TWO = THREE.TOUCH.DOLLY_PAN;
  // OrbitControls writes touch-action:none inline when it connects; that would trap the page under the canvas on a phone.
  cv.style.removeProperty('touch-action');
  cv.style.touchAction = 'pan-y';

  /* ---------- render on demand */
  S.invalidate = () => { if (!S.raf && S.alive) S.raf = requestAnimationFrame(frame); };
  function stepTween() {
    const tw = S.tween;
    const k = clamp((performance.now() - tw.t0) / tw.ms, 0, 1);
    tw.apply(k);
    if (k >= 1) { S.tween = null; return false; }
    return true;
  }
  function frame() {
    S.raf = 0;
    if (!S.alive) return;
    let more = false;
    if (S.tween) more = stepTween();
    if (C.update()) more = true;
    if (S.hooks.before) S.hooks.before();
    renderer.render(scene, camera);
    if (S.hooks.overlay) S.hooks.overlay();
    if (!S.ready) { S.ready = true; root.setAttribute('data-ready', '1'); }
    if (more) S.invalidate();
  }
  C.addEventListener('change', S.invalidate);
  C.addEventListener('start', () => { S.tween = null; S.userMoved = true; if (S.hooks.hover) S.hooks.hover(null); });

  /* ---------- size */
  function resize() {
    const w = root.clientWidth, h = root.clientHeight;
    if (!w || !h || !S.alive) return;
    if (w === S.W && h === S.H) return;
    S.W = w; S.H = h;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    if (S.hooks.resize) S.hooks.resize();
    S.invalidate();
  }
  S.resize = resize;
  if ('ResizeObserver' in window) { const ro = new ResizeObserver(resize); ro.observe(root); S.offs.push(() => ro.disconnect()); }
  S.on(window, 'resize', resize);

  /* ---------- input: the phone gesture split (world.js pattern), the wheel rule, click + hover picking */
  const gest = new Map();
  let tiltLock = null, tiltT = 0;
  const unlockTilt = () => { if (tiltLock) { if (C.minPolarAngle === C.maxPolarAngle) { C.minPolarAngle = tiltLock[0]; C.maxPolarAngle = tiltLock[1]; } tiltLock = null; } };
  S.on(root, 'pointerdown', (e) => {
    if (e.pointerType !== 'touch') return;
    gest.set(e.pointerId, { x: e.clientX, y: e.clientY, v: null });
    C.enableZoom = true; // two fingers pinch-zoom
    clearTimeout(tiltT);
    // a finger never tilts the camera; the browser takes a vertical pan a few moves late and those moves must not tip the orbit
    if (!tiltLock) { const a = C.getPolarAngle(); tiltLock = [C.minPolarAngle, C.maxPolarAngle]; C.minPolarAngle = a; C.maxPolarAngle = a; }
  }, true);
  S.on(root, 'pointermove', (e) => {
    if (e.pointerType !== 'touch' || gest.size !== 1) return;
    const g = gest.get(e.pointerId);
    if (!g) return;
    if (g.v === null) {
      const dx = Math.abs(e.clientX - g.x), dy = Math.abs(e.clientY - g.y);
      if (dx + dy < 6) { e.stopPropagation(); return; }
      g.v = dy > dx * 0.9;
    }
    // a mostly vertical one-finger move belongs to the page's scroll (touch-action: pan-y), never to the camera
    if (g.v) e.stopPropagation();
  }, true);
  const gEnd = (e) => {
    if (e.pointerType !== 'touch') return;
    gest.delete(e.pointerId);
    if (!gest.size) { clearTimeout(tiltT); tiltT = setTimeout(unlockTilt, 900); }
  };
  S.on(window, 'pointerup', gEnd, true);
  S.on(window, 'pointercancel', gEnd, true);
  S.offs.push(() => clearTimeout(tiltT));

  let hinted = false, hintT = 0;
  S.on(root, 'wheel', (e) => {
    const z = e.ctrlKey || e.metaKey;
    C.enableZoom = z;
    if (z && e.target !== cv && e.isTrusted) {
      // Ctrl/⌘ + wheel over a label still zooms the model (the label sits above the canvas, OrbitControls listens on it)
      e.preventDefault();
      cv.dispatchEvent(new WheelEvent('wheel', { deltaX: e.deltaX, deltaY: e.deltaY, deltaZ: e.deltaZ, deltaMode: e.deltaMode, ctrlKey: e.ctrlKey, metaKey: e.metaKey, clientX: e.clientX, clientY: e.clientY, cancelable: true }));
      return;
    }
    if (!z && !hinted) {
      hinted = true;
      hint.textContent = fmt(T.wheel, { k: mac ? '⌘' : 'Ctrl' });
      hint.classList.add('is-on');
      hintT = setTimeout(() => hint.classList.remove('is-on'), 1900);
    }
  }, { capture: true, passive: false });
  S.offs.push(() => clearTimeout(hintT));

  let down = null;
  S.on(cv, 'pointerdown', (e) => { down = { x: e.clientX, y: e.clientY, t: performance.now(), id: e.pointerId }; });
  S.on(cv, 'pointerup', (e) => {
    if (!down || down.id !== e.pointerId) return;
    const moved = Math.hypot(e.clientX - down.x, e.clientY - down.y), quick = performance.now() - down.t < 650;
    down = null;
    if (moved < 8 && quick && S.hooks.pick) S.hooks.pick(e.clientX, e.clientY, e.pointerType);
  });
  S.on(cv, 'pointercancel', () => { down = null; });
  let hq = null, hraf = 0;
  S.on(cv, 'pointermove', (e) => {
    if (e.pointerType !== 'mouse') return;
    if (e.buttons) { if (S.hooks.hover) S.hooks.hover(null); return; }
    hq = [e.clientX, e.clientY];
    if (!hraf) hraf = requestAnimationFrame(() => { hraf = 0; if (S.alive && hq && S.hooks.hover) S.hooks.hover(hq[0], hq[1]); });
  });
  S.on(cv, 'pointerleave', () => { hq = null; if (S.hooks.hover) S.hooks.hover(null); });
  S.offs.push(() => cancelAnimationFrame(hraf));

  const ray = new THREE.Raycaster();
  const ndc = new THREE.Vector2();
  S.raycast = (cx, cy, objs) => {
    const r = cv.getBoundingClientRect();
    if (!r.width || !r.height) return [];
    ndc.set(((cx - r.left) / r.width) * 2 - 1, -((cy - r.top) / r.height) * 2 + 1);
    ray.setFromCamera(ndc, camera);
    return ray.intersectObjects(objs.filter(Boolean), false);
  };
  S.tip = (html, cx, cy) => {
    if (!html) { tip.classList.remove('is-on'); return; }
    if (tip._h !== html) { tip.innerHTML = html; tip._h = html; }
    const r = root.getBoundingClientRect();
    let x = cx - r.left + 14, y = cy - r.top + 16;
    const tw = tip.offsetWidth, th = tip.offsetHeight;
    if (x + tw > r.width - 6) x = cx - r.left - tw - 14;
    if (y + th > r.height - 6) y = cy - r.top - th - 12;
    tip.style.transform = `translate(${Math.round(Math.max(4, x))}px,${Math.round(Math.max(4, y))}px)`;
    tip.classList.add('is-on');
  };

  /* ---------- camera tools */
  const ptsOf = (box) => {
    if (Array.isArray(box)) return box;
    const pts = [];
    for (let i = 0; i < 8; i++) pts.push(new THREE.Vector3(i & 1 ? box.max.x : box.min.x, i & 2 ? box.max.y : box.min.y, i & 4 ? box.max.z : box.min.z));
    return pts;
  };
  S.fitDistance = (box, dir, target, mx = 0.08, my = 0.1) => {
    const cam = camera.clone();
    const pts = ptsOf(box);
    let lo = 0.5, hi = 4000;
    for (let i = 0; i < 40; i++) {
      const mid = (lo + hi) / 2;
      cam.position.copy(target).addScaledVector(dir, mid);
      cam.lookAt(target);
      cam.updateMatrixWorld(true);
      let ok = true;
      for (const p of pts) {
        _v.copy(p).applyMatrix4(cam.matrixWorldInverse);
        if (_v.z > -cam.near) { ok = false; break; }
        _v.applyMatrix4(cam.projectionMatrix);
        if (Math.abs(_v.x) > 1 - mx || Math.abs(_v.y) > 1 - my) { ok = false; break; }
      }
      if (ok) hi = mid; else lo = mid;
    }
    return hi;
  };
  /** Fit a box at (phi, theta) and centre it on screen: the target slides up/down and sideways until the box's
   *  projection is centred, then the distance is fitted again. Returns { target, dist }. */
  S.frame = (box, phi, theta, target0, mx, my, align = 'center') => {
    const pts = ptsOf(box);
    const target = target0.clone();
    const dir = new THREE.Vector3().setFromSphericalCoords(1, phi, theta);
    const right = new THREE.Vector3(Math.cos(theta), 0, -Math.sin(theta));
    let dist = S.fitDistance(pts, dir, target, mx, my);
    const cam = camera.clone();
    const tanH = Math.tan(THREE.MathUtils.degToRad(camera.fov / 2));
    for (let k = 0; k < 4; k++) {
      cam.position.copy(target).addScaledVector(dir, dist);
      cam.lookAt(target);
      cam.updateMatrixWorld(true);
      let x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity;
      for (const q of pts) {
        _v.copy(q).project(cam);
        x0 = Math.min(x0, _v.x); x1 = Math.max(x1, _v.x); y0 = Math.min(y0, _v.y); y1 = Math.max(y1, _v.y);
      }
      const cx = (x0 + x1) / 2;
      // 'top': on a tall (phone) canvas most of the spare height goes below the model, where the street continues
      const slack = 2 - 2 * my - (y1 - y0);
      const cy = align === 'top' && slack > 0.02 ? y1 - (1 - my - slack * 0.25) : (y0 + y1) / 2;
      if (Math.abs(cx) < 0.01 && Math.abs(cy) < 0.01) break;
      target.y += (cy * dist * tanH) / Math.max(0.3, Math.sin(phi));
      target.addScaledVector(right, cx * dist * tanH * camera.aspect);
      dist = S.fitDistance(pts, dir, target, mx, my);
    }
    return { target, dist };
  };
  S.flyTo = (target, sph, ms = 760) => {
    const fromT = C.target.clone();
    const fromS = new THREE.Spherical().setFromVector3(camera.position.clone().sub(C.target));
    let dT = sph.theta - fromS.theta;
    dT = ((((dT + Math.PI) % (2 * Math.PI)) + 2 * Math.PI) % (2 * Math.PI)) - Math.PI;
    const tS = new THREE.Spherical();
    const apply = (k) => {
      const e = ease(k);
      const t = fromT.clone().lerp(target, e);
      tS.set(lerp(fromS.radius, sph.radius, e), lerp(fromS.phi, sph.phi, e), fromS.theta + dT * e);
      camera.position.setFromSpherical(tS).add(t);
      C.target.copy(t);
    };
    if (S.reduced || ms <= 0) { apply(1); S.tween = null; C.update(); S.invalidate(); return; }
    S.tween = { t0: performance.now(), ms, apply };
    S.invalidate();
  };
  S.place = (target, sph) => { S.tween = null; C.target.copy(target); camera.position.setFromSpherical(sph).add(target); camera.lookAt(target); C.update(); S.invalidate(); };

  /* ---------- overlay layout: project, hide what faces away, never let two labels sit on each other.
     Nearer (and higher-priority) labels are placed first. A later label that would touch a placed one tries, in order:
     a small step aside (room labels only), its compact form (room name without the area), and finally its dot alone. */
  const NUDGE = [[0, 0], [0, -24], [0, 24], [-36, 0], [36, 0]];
  const DOTS = [[0, 0], [0, 26], [26, 0], [-26, 0], [0, -26], [24, 24], [-24, 24]];
  S.layout = (items) => {
    const W = S.W, H = S.H, placed = [];
    const clash = (a) => placed.some((q) => a.x < q.x + q.w + 4 && a.x + a.w + 4 > q.x && a.y < q.y + q.h + 3 && a.y + a.h + 3 > q.y);
    items.sort((a, b) => a.prio - b.prio || a.d - b.d);
    for (const it of items) {
      const t = it.tag;
      let show = !!(it.vis && it.p);
      let x = 0, y = 0;
      if (show) {
        _v.copy(it.p).project(camera);
        if (_v.z > 1 || _v.z < -1 || _v.x < -1.08 || _v.x > 1.08 || _v.y < -1.08 || _v.y > 1.08) show = false;
        else { x = ((_v.x + 1) / 2) * W; y = ((1 - _v.y) / 2) * H; }
      }
      if (!show) { if (!t.off) { t.el.classList.add('is-off'); t.off = true; } continue; }
      if (t.off) { t.el.classList.remove('is-off'); t.off = false; }
      const modes = [['full', t.pw, t.ph]];
      if (t.cw) modes.push(['compact', t.cw, t.ch]);
      const offs = it.nudge ? NUDGE : NUDGE.slice(0, 1);
      let pick = null;
      for (const [m, w, h] of modes) {
        for (const [dx, dy] of offs) {
          // never let a label run off the canvas edge
          const cx = clamp(x + dx, Math.min(w / 2 + 6, W / 2), Math.max(W - w / 2 - 6, W / 2));
          const cy = clamp(y + (it.above ? -(h / 2 + 9) : 0) + dy, Math.min(h / 2 + 6, H / 2), Math.max(H - h / 2 - 6, H / 2));
          const c = { x: cx - w / 2, y: cy - h / 2, w, h, id: t.id };
          if (!clash(c)) { pick = { m, c, px: cx, py: cy }; break; }
        }
        if (pick) break;
      }
      if (!pick) {
        const cy0 = y + (it.above ? -21 : 0);
        pick = { m: 'dot', c: { x: x - 12, y: cy0 - 12, w: 24, h: 24, id: t.id }, px: x, py: cy0 };
        for (const [dx, dy] of DOTS) {
          const c = { x: x + dx - 12, y: cy0 + dy - 12, w: 24, h: 24, id: t.id };
          if (!clash(c)) { pick = { m: 'dot', c, px: x + dx, py: cy0 + dy }; break; }
        }
      }
      if (S.trace) S.trace.push({ id: t.id, mode: pick.m, r: pick.c });
      placed.push(pick.c);
      if (pick.m !== t.mode) {
        t.el.classList.toggle('is-dot', pick.m === 'dot');
        t.el.classList.toggle('is-compact', pick.m === 'compact');
        t.mode = pick.m;
        t.dot = pick.m === 'dot';
      }
      const tx = Math.round(pick.px), ty = Math.round(pick.py);
      if (tx !== t.x || ty !== t.y) { t.el.style.transform = `translate3d(${tx}px,${ty}px,0) translate(-50%,-50%)`; t.x = tx; t.y = ty; }
    }
  };
  S.makeTag = (cls, id, html, aria, onClick) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'nlrm3d-tag ' + cls + ' is-off';
    b.dataset.id = id;
    b.setAttribute('aria-label', aria);
    b.innerHTML = html;
    b.addEventListener('click', (e) => { e.preventDefault(); e.stopPropagation(); onClick(); });
    ov.appendChild(b);
    const t = { el: b, id, off: true, dot: false, mode: 'full', x: NaN, y: NaN, pw: 60, ph: 28, cw: 0, ch: 0 };
    t.measure = () => {
      const p = b.querySelector('.nlrm3d-pill');
      if (!p) return;
      const keep = b.className;
      b.classList.remove('is-dot', 'is-compact');
      t.pw = p.offsetWidth || t.pw; t.ph = p.offsetHeight || t.ph;
      if (b.querySelector('.nlrm3d-sub')) { b.classList.add('is-compact'); t.cw = p.offsetWidth; t.ch = p.offsetHeight; }
      b.className = keep;
    };
    t.measure();
    return t;
  };

  S.dispose = () => {
    if (!S.alive) return;
    S.alive = false;
    if (S.raf) cancelAnimationFrame(S.raf);
    S.raf = 0;
    S.offs.forEach((f) => { try { f(); } catch (e) { /* listener already gone */ } });
    S.offs = [];
    if (S.hooks.dispose) S.hooks.dispose();
    C.dispose();
    disposeTree(scene);
    scene.environment = null;
    S.envRT.dispose();
    renderer.renderLists.dispose();
    renderer.dispose();
    try { renderer.forceContextLoss(); } catch (e) { /* context already lost */ }
    root.remove();
  };
  /** QA: the overlay's collision decisions of the next frame. */
  S.traceOnce = () => new Promise((res) => { S.trace = []; S.invalidate(); requestAnimationFrame(() => requestAnimationFrame(() => { const t = S.trace; S.trace = null; res(t); })); });
  S.mark = (handle) => {
    handle._trace = S.traceOnce; LIVE.set(el, handle); const d = handle.dispose; handle.dispose = () => { d(); if (LIVE.get(el) === handle) LIVE.delete(el); }; };
  S.debug = () => ({
    polar: C.getPolarAngle(), azimuth: C.getAzimuthalAngle(), distance: C.getDistance(),
    tris: renderer.info.render.triangles, calls: renderer.info.render.calls, ready: S.ready, shadows: S.shadows,
  });
  // fonts change label widths: measure again once they are in
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => { if (S.alive && S.hooks.measure) { S.hooks.measure(); S.invalidate(); } });
  resize();
  return S;
}

/* ================================================================== BUILDING */
const BEARING = { north: 0, ne: 45, east: 90, se: 135, south: 180, sw: 225, west: 270, nw: 315 };
const SIDE_N = { front: { x: 0, z: 1 }, back: { x: 0, z: -1 }, left: { x: -1, z: 0 }, right: { x: 1, z: 0 } };
function normDir(d) {
  const k = String(d == null ? '' : d).toLowerCase().trim();
  const map = { n: 'north', s: 'south', e: 'east', w: 'west', north: 'north', south: 'south', east: 'east', west: 'west', ne: 'ne', nw: 'nw', se: 'se', sw: 'sw', northeast: 'ne', northwest: 'nw', southeast: 'se', southwest: 'sw', 'צפון': 'north', 'דרום': 'south', 'מזרח': 'east', 'מערב': 'west' };
  return map[k] || '';
}
/** Building-local unit vector (x, z) of a compass bearing. Local +Z is the building's front; orientation = the front's bearing. */
function localVec(bearing, orient) { const a = ((bearing - orient) * Math.PI) / 180; return { x: -Math.sin(a), z: Math.cos(a) }; }

/** Cells (apartments) around a central core: a front row split by the core and a back row. Units are numbered
 *  front row left to right (as seen from the street), then the back row right to left (a ring). */
function layoutCells(N) {
  const cells = [];
  let W, D, core, zf0;
  if (N === 1) {
    W = 13.6; D = 11.2; zf0 = -D / 2;
    cells.push({ x0: -W / 2, x1: W / 2, z0: -D / 2, z1: D / 2, row: 'f' });
    core = { x0: -CW / 2, x1: CW / 2, z0: D / 2 - 4.2, z1: D / 2 + 1.4 };
  } else {
    let best = null;
    for (let k = 1; 2 * k <= N; k++) {
      const b = N - 2 * k;
      if (N >= 3 && b < 1) continue;
      const Wf = 2 * k * 8.4 + CW, Wb = b * 8.6;
      const diff = b ? Math.abs(Wf - Wb) : 0;
      if (!best || diff < best.diff) best = { k, b, diff, W: Math.max(Wf, Wb) };
    }
    W = best.W;
    const df = best.b ? 7.8 : 11.4, db = 7.8;
    D = df + (best.b ? db : 0);
    zf0 = D / 2 - df;
    const fw = (W / 2 - CW / 2) / best.k;
    for (let i = 0; i < best.k; i++) cells.push({ x0: -W / 2 + i * fw, x1: -W / 2 + (i + 1) * fw, z0: zf0, z1: D / 2, row: 'f' });
    for (let i = 0; i < best.k; i++) cells.push({ x0: CW / 2 + i * fw, x1: CW / 2 + (i + 1) * fw, z0: zf0, z1: D / 2, row: 'f' });
    const bw = W / Math.max(1, best.b);
    for (let i = best.b - 1; i >= 0; i--) cells.push({ x0: -W / 2 + i * bw, x1: -W / 2 + (i + 1) * bw, z0: -D / 2, z1: zf0, row: 'b' });
    core = { x0: -CW / 2, x1: CW / 2, z0: best.b ? zf0 : -D / 2, z1: D / 2 + 0.35 };
  }
  const E = 1e-6;
  cells.forEach((c, i) => {
    c.pos = i + 1;
    c.sides = [];
    if (c.z1 >= D / 2 - E) c.sides.push('front');
    if (c.z0 <= -D / 2 + E) c.sides.push('back');
    if (c.x0 <= -W / 2 + E) c.sides.push('left');
    if (c.x1 >= W / 2 - E) c.sides.push('right');
    c.primary = c.row === 'b' ? 'back' : 'front';
  });
  return { W, D, cells, core, zf0, N };
}
function faceOf(L, c, side) {
  const { W, D } = L;
  if (side === 'front') return { side, cx: (c.x0 + c.x1) / 2, cz: D / 2, nx: 0, nz: 1, tx: 1, tz: 0, len: c.x1 - c.x0 };
  if (side === 'back') return { side, cx: (c.x0 + c.x1) / 2, cz: -D / 2, nx: 0, nz: -1, tx: -1, tz: 0, len: c.x1 - c.x0 };
  if (side === 'left') return { side, cx: -W / 2, cz: (c.z0 + c.z1) / 2, nx: -1, nz: 0, tx: 0, tz: 1, len: c.z1 - c.z0 };
  return { side, cx: W / 2, cz: (c.z0 + c.z1) / 2, nx: 1, nz: 0, tx: 0, tz: -1, len: c.z1 - c.z0 };
}
function cutIv(iv, a, b) {
  const out = [];
  for (const [x, y] of iv) {
    if (b <= x || a >= y) { out.push([x, y]); continue; }
    if (a > x) out.push([x, a]);
    if (b < y) out.push([b, y]);
  }
  return out;
}
function roundedRectShape(x0, z0, x1, z1, r) {
  // shape coordinates (x, y) map to world (x, -y) after rotateX(-PI/2)
  const s = new THREE.Shape();
  const y0 = -z1, y1 = -z0;
  s.moveTo(x0 + r, y0);
  s.lineTo(x1 - r, y0); s.quadraticCurveTo(x1, y0, x1, y0 + r);
  s.lineTo(x1, y1 - r); s.quadraticCurveTo(x1, y1, x1 - r, y1);
  s.lineTo(x0 + r, y1); s.quadraticCurveTo(x0, y1, x0, y1 - r);
  s.lineTo(x0, y0 + r); s.quadraticCurveTo(x0, y0, x0 + r, y0);
  return s;
}
function northTexture(letter) {
  const c = document.createElement('canvas');
  c.width = c.height = 256;
  const g = c.getContext('2d');
  g.clearRect(0, 0, 256, 256);
  g.strokeStyle = 'rgba(20,33,43,.42)';
  g.lineWidth = 5;
  g.beginPath(); g.arc(128, 146, 84, 0, Math.PI * 2); g.stroke();
  g.fillStyle = '#14212b';
  g.beginPath(); g.moveTo(128, 70); g.lineTo(158, 196); g.lineTo(128, 174); g.lineTo(98, 196); g.closePath(); g.fill();
  g.font = '700 58px Assistant, "Segoe UI", Arial, sans-serif';
  g.textAlign = 'center'; g.textBaseline = 'middle';
  g.fillText(letter, 128, 34);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = 4;
  return t;
}

function buildBuildingModel(S, o) {
  const T = S.T;
  const N = clamp(Math.round(+o.unitsPerFloor) || 1, 1, 12);
  const units = (Array.isArray(o.units) ? o.units : []).filter((u) => u && u.id != null && u.id !== '');
  let F = clamp(Math.round(+o.floors) || 1, 1, 40);
  F = Math.max(F, clamp(units.reduce((m, u) => Math.max(m, Math.round(+u.floor) || 0), 0), 0, 40));
  const groundRes = units.some((u) => u.floor !== '' && u.floor != null && Math.round(+u.floor) === 0);
  const meta = o.meta || {};
  const orient = ((((+o.orientation || 0) % 360) + 360) % 360);
  const L = layoutCells(N);
  const { W, D, cells, core } = L;
  const yOf = (f) => (f <= 0 ? 0 : GH + (f - 1) * FH);
  const hOf = (f) => (f <= 0 ? GH : FH);
  const roofY = GH + F * FH;
  const yb = +meta.year_built || 0;
  const glassRail = !yb || yb >= 1995;
  const dv = (dir) => { const k = normDir(dir); return k ? localVec(BEARING[k], orient) : null; };
  const dotS = (sd, v) => SIDE_N[sd].x * v.x + SIDE_N[sd].z * v.z;
  const floorTxt = (f) => (f <= 0 ? T.ground : fmt(T.floor, { n: f }));

  /* ---- which cell is which landlord unit, and which side its balcony faces */
  const info = new Map(), slot = new Map();
  const place = (u, f, c) => {
    const v = dv(u.dir);
    let side = c.primary;
    if (v) { let bs = -9; for (const sd of c.sides) { const s = dotS(sd, v); if (s > bs) { bs = s; side = sd; } } }
    const st = STATUS[u.status] ? u.status : 'ok';
    const rec = { u, id: String(u.id), f, c, side, status: st, s0: 0 };
    info.set(rec.id, rec);
    slot.set(f + ':' + c.pos, rec);
  };
  const byF = new Map();
  for (const u of units) {
    const f = clamp(Math.round(+u.floor) || 0, 0, F);
    if (f === 0 && !groundRes) continue;
    if (!byF.has(f)) byF.set(f, []);
    byF.get(f).push(u);
  }
  for (const [f, list] of byF) {
    const taken = new Set(), rest = [];
    for (const u of list) {
      const p = Math.round(+u.pos);
      if (p >= 1 && p <= N && !taken.has(p)) { taken.add(p); place(u, f, cells[p - 1]); } else rest.push(u);
    }
    for (const u of rest) {
      const v = dv(u.dir);
      let best = null, bs = -9;
      for (const c of cells) {
        if (taken.has(c.pos)) continue;
        const s = v ? Math.max(...c.sides.map((sd) => dotS(sd, v))) : 0;
        if (s > bs) { bs = s; best = c; }
      }
      if (!best) continue;
      taken.add(best.pos);
      place(u, f, best);
    }
  }

  /* ---- materials */
  const mats = {
    facade: std(PAL.cream, 0.92),
    core: std('#e8e3d9', 0.9),
    band: std('#e3ded3', 0.85),
    groove: std('#d3ccbf', 0.9),
    trim: std('#dcd6ca', 0.8),
    stone: std('#e1d9c9', 0.95),
    roof: std('#e2ded5', 0.97),
    coping: std('#d8d2c6', 0.85),
    glass: std(PAL.glass, 0.22, 0.3, { envMapIntensity: 1.25 }),
    lobbyGlass: std('#a9bec7', 0.08, 0.15, { transparent: true, opacity: 0.4, depthWrite: false }),
    railGlass: std('#cfdee4', 0.08, 0.1, { transparent: true, opacity: 0.3, depthWrite: false, side: THREE.DoubleSide }),
    railMetal: std('#58626a', 0.6, 0.4, { transparent: true, opacity: 0.5, depthWrite: false, side: THREE.DoubleSide }),
    rail: std('#7b848b', 0.45, 0.5),
    dark: std('#525c65', 0.6, 0.2),
    lobbyFloor: std('#ece7dd', 0.6),
    balSlab: std('#e6e1d6', 0.9),
    ac: std('#eceae5', 0.6),
    grille: std('#9aa0a4', 0.7),
    solar: std('#4f6170', 0.3, 0.35, { envMapIntensity: 1.3 }),
    tank: std('#efeee9', 0.5, 0.1),
    leg: std('#8d949a', 0.6, 0.4),
    plate: std('#ebe7df', 1),
    path: std('#e4dfd4', 1),
    walk: std('#dfdbd2', 1),
    curb: std('#d2cdc3', 1),
    road: std('#cfcfca', 1),
    line: std('#f9f8f4', 1),
    pwall: std('#dcd3c3', 0.95),
    hedge: std('#b3bca5', 1),
    trunk: std('#8e7f6b', 1),
    leaf: std('#a6b39b', 1, 0, { flatShading: true }),
    car: std('#ffffff', 0.45, 0.15),
    carTop: std('#5d6872', 0.25, 0.3),
    carBase: std('#2f363c', 0.8),
    ink: std(PAL.ink, 0.7),
  };
  const group = new THREE.Group();
  group.name = 'nlrm3d-building';
  const MG = new Merge();
  const I = { pane: [], trim: [], balSlab: [], railP: [], railT: [], ac: [], grille: [], col: [], solar: [], tank: [], leg: [], trunk: [], crown: [], mull: [], line: [], car: [], carTop: [], carBase: [] };
  const carColors = [];
  const balOwner = [];
  const neutral = [], neutralKeys = [];

  const fpt = (fc, s, off) => [fc.cx + fc.tx * s + fc.nx * off, fc.cz + fc.tz * s + fc.nz * off];
  const fb = (list, fc, s, off, y, w, h, d) => { const [x, z] = fpt(fc, s, off); list.push(m4(x, y, z, w, h, d, Math.atan2(fc.nx, fc.nz))); };
  const fcyl = (list, fc, s, off, y, r, h) => { const [x, z] = fpt(fc, s, off); list.push(m4(x, y, z, r, h, r, Math.atan2(fc.nx, fc.nz), Math.PI / 2)); };

  const floorsList = [];
  for (let f = groundRes ? 0 : 1; f <= F; f++) floorsList.push(f);

  for (const f of floorsList) {
    const y0 = yOf(f), h = hOf(f);
    for (const c of cells) {
      const rec = slot.get(f + ':' + c.pos);
      const box = { x: (c.x0 + c.x1) / 2, y: y0 + h / 2, z: (c.z0 + c.z1) / 2, w: c.x1 - c.x0, h, d: c.z1 - c.z0 };
      if (rec) rec.box = box;
      else { neutral.push(m4(box.x, box.y, box.z, box.w, box.h, box.d)); neutralKeys.push({ f, pos: c.pos, box }); }
      const balSide = f > 0 ? (rec ? rec.side : c.primary) : null;
      const owner = rec ? { id: rec.id } : { f, pos: c.pos, idx: neutralKeys.length - 1 };
      for (const sd of c.sides) {
        const fc = faceOf(L, c, sd);
        const half = fc.len / 2;
        let iv = [[-half + 0.6, half - 0.6]];
        if (sd === 'front' && core.z1 > L.D / 2 + 0.01 && core.x1 > c.x0 && core.x0 < c.x1) iv = cutIv(iv, core.x0 - fc.cx - 0.3, core.x1 - fc.cx + 0.3);
        if (sd === balSide) {
          // the balcony takes the widest free stretch of this face
          let big = iv[0];
          for (const q of iv) if (q[1] - q[0] > big[1] - big[0]) big = q;
          const room = big[1] - big[0];
          let bw = clamp(fc.len * 0.56, 2.6, 5.4);
          if (bw > room - 0.4) bw = Math.max(1.8, room - 0.4);
          const s0 = (big[0] + big[1]) / 2, bdp = 1.55;
          if (rec) rec.s0 = s0;
          fb(I.balSlab, fc, s0, bdp / 2, y0 + 0.0, bw, 0.2, bdp);
          balOwner.push(owner);
          const sw = Math.min(bw - 0.6, 2.6);
          fb(I.pane, fc, s0, 0.015, y0 + 0.1 + 1.1, sw, 2.2, 0.05);
          fb(I.trim, fc, s0, 0.045, y0 + 0.1 + 1.1, 0.06, 2.2, 0.03);
          fb(I.trim, fc, s0, 0.08, y0 + 2.48, sw + 0.12, 0.22, 0.16);
          const rh = 1.0, r0 = y0 + 0.1;
          fb(I.railP, fc, s0, bdp - 0.04, r0 + rh / 2, bw - 0.04, rh, 0.025);
          fb(I.railP, fc, s0 - bw / 2 + 0.03, bdp / 2, r0 + rh / 2, 0.025, rh, bdp - 0.06);
          fb(I.railP, fc, s0 + bw / 2 - 0.03, bdp / 2, r0 + rh / 2, 0.025, rh, bdp - 0.06);
          fb(I.railT, fc, s0, bdp - 0.04, r0 + rh + 0.02, bw, 0.05, 0.06);
          fb(I.railT, fc, s0 - bw / 2 + 0.03, bdp / 2, r0 + rh + 0.02, 0.06, 0.05, bdp);
          fb(I.railT, fc, s0 + bw / 2 - 0.03, bdp / 2, r0 + rh + 0.02, 0.06, 0.05, bdp);
          if (hash(f, c.pos, 7) < 0.46 && bw > 2.4) {
            const sA = s0 + (hash(f, c.pos, 9) < 0.5 ? -1 : 1) * (bw / 2 - 0.6);
            fb(I.ac, fc, sA, 0.2, r0 + 0.29, 0.82, 0.58, 0.3);
            fcyl(I.grille, fc, sA - 0.12, 0.36, r0 + 0.29, 0.19, 0.02);
          }
          iv = cutIv(iv, s0 - bw / 2 - 0.3, s0 + bw / 2 + 0.3);
        }
        for (const [a, b] of iv) {
          const len = b - a;
          if (len < 1.5) continue;
          const n = Math.max(1, Math.floor((len + 1.0) / 2.5));
          const ww = Math.min(1.3, len / n - 0.35);
          for (let i = 0; i < n; i++) {
            const s = a + (len * (i + 0.5)) / n;
            const sill = y0 + (f === 0 ? 1.05 : 0.95), wh = 1.45;
            fb(I.pane, fc, s, 0.015, sill + wh / 2, ww, wh, 0.05);
            fb(I.trim, fc, s, 0.045, sill + wh / 2, 0.05, wh, 0.03);
            fb(I.trim, fc, s, 0.08, sill + wh + 0.13, ww + 0.12, 0.22, 0.16);
            fb(I.trim, fc, s, 0.06, sill - 0.03, ww + 0.16, 0.06, 0.14);
            if (f > 0 && sd !== 'front' && hash(f * 31 + c.pos, i, sd.length) < 0.17) {
              fb(I.ac, fc, s, 0.2, y0 + 0.5, 0.8, 0.55, 0.3);
              fcyl(I.grille, fc, s - 0.12, 0.36, y0 + 0.5, 0.18, 0.02);
            }
          }
        }
      }
    }
  }

  /* ---- slab bands (one ring per floor line), grooves between apartments */
  const yStart = groundRes ? 0 : GH;
  const bandYs = [];
  for (let f = 1; f <= F; f++) bandYs.push(yOf(f));
  bandYs.push(roofY);
  for (const y of bandYs) {
    MG.box('band', W + 0.16, 0.26, 0.24, 0, y, D / 2 - 0.04);
    MG.box('band', W + 0.16, 0.26, 0.24, 0, y, -D / 2 + 0.04);
    MG.box('band', 0.24, 0.26, D - 0.1, -W / 2 + 0.04, y, 0);
    MG.box('band', 0.24, 0.26, D - 0.1, W / 2 - 0.04, y, 0);
  }
  const gh = roofY - yStart;
  const fr = cells.filter((c) => c.sides.includes('front')).sort((a, b) => a.x0 - b.x0);
  for (let i = 0; i < fr.length - 1; i++) if (Math.abs(fr[i].x1 - fr[i + 1].x0) < 1e-6) MG.box('groove', 0.07, gh, 0.05, fr[i].x1, yStart + gh / 2, D / 2 + 0.02);
  const bk = cells.filter((c) => c.sides.includes('back')).sort((a, b) => a.x0 - b.x0);
  for (let i = 0; i < bk.length - 1; i++) if (Math.abs(bk[i].x1 - bk[i + 1].x0) < 1e-6) MG.box('groove', 0.07, gh, 0.05, bk[i].x1, yStart + gh / 2, -D / 2 - 0.02);
  if (cells.some((c) => c.row === 'b') && cells.some((c) => c.row === 'f') && N > 1) {
    MG.box('groove', 0.05, gh, 0.07, -W / 2 - 0.02, yStart + gh / 2, L.zf0);
    MG.box('groove', 0.05, gh, 0.07, W / 2 + 0.02, yStart + gh / 2, L.zf0);
  }

  /* ---- the core: stair glass on the street, stair head and machine room on the roof, the lobby below */
  const ccx = (core.x0 + core.x1) / 2, ccz = (core.z0 + core.z1) / 2, cwid = core.x1 - core.x0, cdep = core.z1 - core.z0;
  const headTop = roofY + 2.9;
  MG.box('core', cwid, headTop - GH, cdep, ccx, (GH + headTop) / 2, ccz);
  MG.box('coping', cwid + 0.14, 0.1, cdep + 0.14, ccx, headTop + 0.05, ccz);
  const sgH = roofY - GH - 0.7;
  I.pane.push(m4(ccx, GH + 0.35 + sgH / 2, core.z1 + 0.015, 1.3, sgH, 0.05));
  I.trim.push(m4(ccx - 0.68, GH + 0.35 + sgH / 2, core.z1 + 0.04, 0.07, sgH + 0.07, 0.08));
  I.trim.push(m4(ccx + 0.68, GH + 0.35 + sgH / 2, core.z1 + 0.04, 0.07, sgH + 0.07, 0.08));
  for (let k = 0; k <= F; k++) {
    const y = clamp(GH + 0.35 + k * FH, GH + 0.35, GH + 0.35 + sgH);
    I.trim.push(m4(ccx, y, core.z1 + 0.04, 1.43, 0.07, 0.08));
  }
  // lobby (the core's ground storey): recessed glass front, warm interior, mailboxes, a canopy over the door
  const lz1 = core.z1 - 0.55, lz0 = Math.max(core.z0 + 0.2, lz1 - 6.5), lmid = (lz0 + lz1) / 2;
  MG.box('lobbyFloor', cwid - 0.1, 0.04, lz1 - lz0, ccx, 0.02, lmid);
  MG.box('core', cwid, GH, 0.2, ccx, GH / 2, lz0 - 0.1);
  MG.box('core', 0.22, GH, lz1 - lz0 + 0.2, core.x0 + 0.11, GH / 2, lmid);
  MG.box('core', 0.22, GH, lz1 - lz0 + 0.2, core.x1 - 0.11, GH / 2, lmid);
  MG.box('core', cwid, 0.3, 0.55, ccx, GH - 0.15, core.z1 - 0.275);
  MG.box('lobbyGlass', cwid - 0.44, GH - 0.42, 0.04, ccx, (GH - 0.42) / 2 + 0.03, lz1);
  for (const dx of [-1.55, -0.78, 0.78, 1.55]) I.mull.push(m4(ccx + dx * (cwid / 4.4), (GH - 0.4) / 2, lz1 + 0.03, 0.06, GH - 0.4, 0.07));
  I.mull.push(m4(ccx, 2.55, lz1 + 0.03, cwid - 0.44, 0.06, 0.07));
  MG.box('dark', 0.22, 1.0, 1.5, core.x0 + 0.33, 1.35, lmid - 0.6);
  MG.box('band', cwid + 2.6, 0.18, 2.4, ccx, GH - 0.62, core.z1 + 0.62);
  MG.box('dark', cwid + 2.6, 0.05, 0.05, ccx, GH - 0.73, core.z1 + 1.8);

  /* ---- ground storey: pilotis columns + Jerusalem-stone storage base (or ground apartments) */
  if (!groundRes) {
    const colPts = [];
    const nx = Math.max(2, Math.ceil(W / 5.8) + 1);
    for (let i = 0; i < nx; i++) {
      const x = -W / 2 + 0.3 + ((W - 0.6) * i) / (nx - 1);
      if (!(Math.abs(x - ccx) < cwid / 2 + 0.35)) colPts.push([x, D / 2 - 0.3]);
      colPts.push([x, -D / 2 + 0.3]);
    }
    const nz = Math.max(2, Math.ceil(D / 5.8) + 1);
    for (let j = 1; j < nz - 1; j++) { const z = -D / 2 + 0.3 + ((D - 0.6) * j) / (nz - 1); colPts.push([-W / 2 + 0.3, z], [W / 2 - 0.3, z]); }
    for (const [x, z] of colPts) I.col.push(m4(x, GH / 2, z, 0.44, GH, 0.44));
    const bz1 = meta.parking ? (N > 2 ? L.zf0 : -D / 2 + D * 0.38) : D / 2 - 1.1;
    const bz0 = -D / 2 + 1.1;
    if (bz1 - bz0 > 0.5) {
      const hS = GH - 0.13;
      // left and right of the lobby, then behind it
      MG.box('stone', core.x0 - (-W / 2 + 1.1), hS, bz1 - bz0, (-W / 2 + 1.1 + core.x0) / 2, hS / 2, (bz0 + bz1) / 2);
      MG.box('stone', W / 2 - 1.1 - core.x1, hS, bz1 - bz0, (W / 2 - 1.1 + core.x1) / 2, hS / 2, (bz0 + bz1) / 2);
      if (lz0 - 0.2 - bz0 > 0.3) MG.box('stone', cwid, hS, Math.min(bz1, lz0 - 0.2) - bz0, ccx, hS / 2, (bz0 + Math.min(bz1, lz0 - 0.2)) / 2);
    }
    if (meta.parking) {
      // bays under the building, nose to the street
      const z0 = (N > 2 ? L.zf0 : bz1) + 0.4, z1 = D / 2 - 0.2, zc = (z0 + z1) / 2;
      const spans = [[-W / 2 + 0.7, core.x0 - 0.35], [core.x1 + 0.35, W / 2 - 0.7]];
      let k = 0;
      for (const [a, b] of spans) {
        const n = Math.floor((b - a) / 2.6);
        for (let i = 0; i <= n; i++) I.line.push(m4(a + i * 2.6, 0.012, zc, 0.1, 0.012, Math.min(4.8, z1 - z0)));
        for (let i = 0; i < n; i++) {
          if (hash(i, k, 3) < 0.45) continue;
          const x = a + i * 2.6 + 1.3, cz = zc + 0.1;
          I.carBase.push(m4(x, 0.32, cz, 1.7, 0.46, Math.min(3.9, z1 - z0 - 0.6)));
          I.car.push(m4(x, 0.68, cz, 1.8, 0.56, Math.min(4.3, z1 - z0 - 0.3)));
          I.carTop.push(m4(x, 1.17, cz - 0.15, 1.56, 0.5, Math.min(2.3, z1 - z0 - 1.8)));
          carColors.push(['#d7d9db', '#8f9aa5', '#e9e6df', '#6f7a84'][Math.floor(hash(i, k, 5) * 4)]);
        }
        k++;
      }
    }
  }

  /* ---- roof: parapet with coping, solar water heaters (one per flat), water tank, elevator machine room */
  const rTop = roofY + 0.13;
  MG.box('roof', W - 0.3, 0.06, D - 0.3, 0, rTop + 0.03, 0);
  const ph = 0.95;
  MG.box('facade', W + 0.16, ph, 0.2, 0, rTop + ph / 2, D / 2 - 0.02);
  MG.box('facade', W + 0.16, ph, 0.2, 0, rTop + ph / 2, -D / 2 + 0.02);
  MG.box('facade', 0.2, ph, D - 0.36, -W / 2 + 0.02, rTop + ph / 2, 0);
  MG.box('facade', 0.2, ph, D - 0.36, W / 2 - 0.02, rTop + ph / 2, 0);
  MG.box('coping', W + 0.26, 0.07, 0.3, 0, rTop + ph + 0.035, D / 2 - 0.02);
  MG.box('coping', W + 0.26, 0.07, 0.3, 0, rTop + ph + 0.035, -D / 2 + 0.02);
  MG.box('coping', 0.3, 0.07, D - 0.3, -W / 2 + 0.02, rTop + ph + 0.035, 0);
  MG.box('coping', 0.3, 0.07, D - 0.3, W / 2 - 0.02, rTop + ph + 0.035, 0);
  if (core.z0 > -D / 2 + 0.6) MG.box('dark', 1.0, 2.1, 0.06, ccx, rTop + 1.05, core.z0 - 0.03);
  else MG.box('dark', 0.06, 2.1, 1.0, core.x0 - 0.03, rTop + 1.05, ccz - 1);
  let topY = headTop + 0.1;
  if (meta.elevator) {
    const mw = cwid * 0.56, md = Math.min(2.6, cdep * 0.42), mz = core.z1 - 0.35 - md / 2;
    MG.box('core', mw, 1.55, md, ccx + cwid * 0.18, headTop + 0.1 + 0.775, mz);
    MG.box('coping', mw + 0.12, 0.08, md + 0.12, ccx + cwid * 0.18, headTop + 0.1 + 1.59, mz);
    MG.box('dark', 0.6, 0.5, 0.04, ccx + cwid * 0.18, headTop + 0.95, mz + md / 2 + 0.02);
    topY = headTop + 1.7;
  }
  {
    const tx = ccx - cwid * 0.2, tz = core.z0 + Math.min(1.25, cdep * 0.3);
    MG.box('leg', 1.6, 0.16, 1.6, tx, headTop + 0.18, tz);
    const tg = new THREE.CylinderGeometry(0.72, 0.72, 1.45, 18);
    tg.translate(tx, headTop + 0.26 + 0.725, tz);
    MG.add('tank', tg);
    topY = Math.max(topY, headTop + 1.75);
  }
  const flats = floorsList.length * N;
  if (meta.solar && flats > 0) {
    const alpha = (orient * Math.PI) / 180 + Math.PI; // heaters face south
    const ca = Math.cos(alpha), sa = Math.sin(alpha);
    const spots = [];
    for (let z = -D / 2 + 1.45; z <= D / 2 - 1.45 + 1e-6; z += 2.35) {
      for (let x = -W / 2 + 1.3; x <= W / 2 - 1.3 + 1e-6; x += 1.75) {
        if (x > core.x0 - 1.15 && x < core.x1 + 1.15 && z > core.z0 - 1.6 && z < core.z1 + 1.1) continue;
        spots.push([x, z]);
      }
    }
    spots.sort((p, q) => p[1] - q[1] || Math.abs(p[0]) - Math.abs(q[0]));
    const use = spots.slice(0, Math.min(flats, spots.length));
    for (const [x, z] of use) {
      const at = (lx, ly, lz) => [x + lx * ca + lz * sa, rTop + ly, z - lx * sa + lz * ca];
      let p = at(0, 0.72, 0.12); I.solar.push(m4(p[0], p[1], p[2], 0.98, 0.05, 1.9, alpha, 0.7));
      p = at(0, 1.42, -0.78); I.tank.push(m4(p[0], p[1], p[2], 0.27, 1.45, 0.27, alpha, 0, Math.PI / 2));
      p = at(-0.42, 0.62, -0.72); I.leg.push(m4(p[0], p[1], p[2], 0.06, 1.24, 0.06, alpha));
      p = at(0.42, 0.62, -0.72); I.leg.push(m4(p[0], p[1], p[2], 0.06, 1.24, 0.06, alpha));
    }
  }

  /* ---- the site: a model base, front yard, sidewalk with trees, the street, a low stone wall, the north arrow */
  const yard = 6, walk = 3.2, road = 7.2;
  const PX0 = -W / 2 - 6.5, PX1 = W / 2 + 6.5, PZ0 = -D / 2 - 6, fz = D / 2 + yard;
  const farWalk = 3.4;
  const PZ1 = fz + walk + road + farWalk + 0.2;
  {
    const sh = roundedRectShape(PX0, PZ0, PX1, PZ1, 1.6);
    const g = new THREE.ExtrudeGeometry(sh, { depth: 0.6, bevelEnabled: false, curveSegments: 5 });
    g.rotateX(-Math.PI / 2);
    g.translate(0, -0.6, 0);
    MG.add('plate', g);
  }
  const pw = PX1 - PX0 - 0.02, pcx = (PX0 + PX1) / 2;
  MG.box('walk', pw, 0.12, walk, pcx, 0.06, fz + walk / 2);
  MG.box('curb', pw, 0.16, 0.2, pcx, 0.08, fz + walk - 0.1);
  MG.box('road', pw, 0.03, road, pcx, 0.015, fz + walk + road / 2);
  MG.box('walk', pw, 0.12, farWalk, pcx, 0.06, fz + walk + road + farWalk / 2);
  MG.box('curb', pw, 0.16, 0.2, pcx, 0.08, fz + walk + road + 0.1);
  for (let x = PX0 + 2; x < PX1 - 2; x += 4.6) I.line.push(m4(x, 0.035, fz + walk + road / 2, 2.1, 0.012, 0.14));
  const gate = [-1.45, 1.45];
  const drive = meta.parking ? [W / 2 - 5.2, W / 2 - 1.6] : null;
  let wallIv = [[PX0 + 0.4, PX1 - 0.4]];
  wallIv = cutIv(wallIv, gate[0] + ccx, gate[1] + ccx);
  if (drive) wallIv = cutIv(wallIv, drive[0], drive[1]);
  for (const [a, b] of wallIv) {
    MG.box('pwall', b - a, 0.72, 0.3, (a + b) / 2, 0.36, fz - 0.15);
    if (b - a > 1.6) MG.box('hedge', b - a - 0.6, 0.78, 0.62, (a + b) / 2, 0.39, fz - 0.75);
  }
  MG.box('pwall', 0.3, 0.72, fz - PZ0 - 0.7, PX0 + 0.55, 0.36, (fz + PZ0 + 0.4) / 2);
  MG.box('pwall', 0.3, 0.72, fz - PZ0 - 0.7, PX1 - 0.55, 0.36, (fz + PZ0 + 0.4) / 2);
  MG.box('pwall', PX1 - PX0 - 1.1, 0.72, 0.3, pcx, 0.36, PZ0 + 0.55);
  MG.box('path', 2.6, 0.03, yard + 0.2 + (core.z1 - D / 2), ccx, 0.015, (core.z1 + fz) / 2);
  if (drive) MG.box('path', drive[1] - drive[0], 0.03, yard, (drive[0] + drive[1]) / 2, 0.015, D / 2 + yard / 2);
  const trees = [];
  for (let x = PX0 + 2.6; x < PX1 - 2; x += 6.6) {
    if (Math.abs(x - ccx) < 2.4) continue;
    if (drive && x > drive[0] - 1 && x < drive[1] + 1) continue;
    trees.push([x, fz + walk - 0.85, 0.85]);
  }
  for (let x = PX0 + 5.9; x < PX1 - 2; x += 7.4) trees.push([x, fz + walk + road + 1.3, 0.8]);
  trees.push([PX1 - 2.6, PZ0 + 2.6, 1.15], [PX0 + 2.4, 0.5, 1.05], [PX1 - 2.3, -D / 2 + 1.5, 0.95]);
  if (!meta.shelter) trees.push([PX0 + 2.6, PZ0 + 2.6, 1.1]);
  for (const [x, z, s] of trees) {
    I.trunk.push(m4(x, 0.95 * s, z, 0.13 * s, 1.9 * s, 0.13 * s));
    I.crown.push(m4(x, 2.75 * s + 0.4, z, 1.45 * s, 1.65 * s, 1.45 * s, hash(Math.round(x), Math.round(z)) * 6));
  }
  if (meta.shelter) {
    // the building's shelter entrance: a low concrete head with its door and a vent
    const sx = PX0 + 2.8, sz = PZ0 + 2.4;
    MG.box('stone', 2.6, 1.95, 2.1, sx, 0.975, sz);
    MG.box('coping', 2.74, 0.08, 2.24, sx, 1.99, sz);
    MG.box('dark', 0.95, 1.6, 0.05, sx + 0.4, 0.8, sz + 1.06);
    MG.box('ink', 0.34, 0.22, 0.03, sx - 0.6, 1.45, sz + 1.065);
    const vg = new THREE.CylinderGeometry(0.11, 0.11, 0.9, 10);
    vg.translate(sx - 0.8, 2.4, sz - 0.6);
    MG.add('leg', vg);
  }
  const northM = new THREE.Mesh(new THREE.PlaneGeometry(3.4, 3.4), new THREE.MeshBasicMaterial({ map: northTexture(T.north), transparent: true, depthWrite: false, toneMapped: false }));
  northM.rotation.order = 'YXZ';
  northM.rotation.set(-Math.PI / 2, (orient * Math.PI) / 180 + Math.PI, 0);
  northM.position.set(PX0 + 2.7, 0.02, fz - 2.7);
  northM.renderOrder = 1;
  group.add(northM);
  northM.userData.x = Math.abs(PX0 + 2.7);

  /* ---- assemble */
  MG.meshes(mats, group, ['plate', 'walk', 'road', 'curb', 'path', 'roof', 'lobbyFloor', 'lobbyGlass']);
  const glassRailMat = glassRail ? mats.railGlass : mats.railMetal;
  const box1 = () => new THREE.BoxGeometry(1, 1, 1);
  const add = (m) => { if (m) group.add(m); return m; };
  const nInst = add(instanced(box1(), mats.facade, neutral, { colors: neutral.map(() => '#ffffff'), name: 'apartments' }));
  add(instanced(box1(), mats.glass, I.pane, { cast: false, name: 'windows' }));
  add(instanced(box1(), mats.trim, I.trim, { name: 'trim' }));
  const balInst = add(instanced(box1(), mats.balSlab, I.balSlab, { name: 'balconies' }));
  add(instanced(box1(), glassRailMat, I.railP, { cast: false, name: 'railings' }));
  add(instanced(box1(), mats.rail, I.railT, { name: 'handrails' }));
  add(instanced(box1(), mats.ac, I.ac, { name: 'ac' }));
  add(instanced(new THREE.CylinderGeometry(1, 1, 1, 12), mats.grille, I.grille, { cast: false, name: 'ac-grille' }));
  add(instanced(box1(), mats.facade, I.col, { name: 'columns' }));
  add(instanced(box1(), mats.solar, I.solar, { name: 'solar' }));
  add(instanced(new THREE.CylinderGeometry(1, 1, 1, 12), mats.tank, I.tank, { name: 'solar-tanks' }));
  add(instanced(box1(), mats.leg, I.leg, { name: 'solar-legs' }));
  add(instanced(box1(), mats.dark, I.mull, { name: 'mullions' }));
  add(instanced(box1(), mats.line, I.line, { cast: false, receive: true, name: 'lines' }));
  add(instanced(new THREE.CylinderGeometry(1, 1, 1, 7), mats.trunk, I.trunk, { name: 'trunks' }));
  add(instanced(new THREE.IcosahedronGeometry(1, 1), mats.leaf, I.crown, { name: 'crowns' }));
  add(instanced(box1(), mats.car, I.car, { colors: carColors, name: 'cars' }));
  add(instanced(box1(), mats.carTop, I.carTop, { name: 'car-tops' }));
  add(instanced(box1(), mats.carBase, I.carBase, { name: 'car-bases' }));

  // the landlord's apartments: tinted volumes with a soft glow and a lit edge
  const owned = [];
  for (const rec of info.values()) {
    if (!rec.box) continue;
    const b = rec.box;
    const col = tintOf(rec.status);
    const m = new THREE.Mesh(new THREE.BoxGeometry(b.w, b.h, b.d), new THREE.MeshStandardMaterial({ color: col, roughness: 0.78, metalness: 0, emissive: col, emissiveIntensity: 0.16 }));
    m.position.set(b.x, b.y, b.z);
    m.castShadow = m.receiveShadow = true;
    m.userData.unitId = rec.id;
    const e = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(b.w + 0.04, b.h - 0.02, b.d + 0.04)), new THREE.LineBasicMaterial({ color: col.clone().lerp(new THREE.Color('#ffffff'), 0.35), transparent: true, opacity: 0.95 }));
    m.add(e);
    rec.mesh = m; rec.edge = e;
    group.add(m);
    owned.push(m);
    rec.anchors = rec.c.sides.map((sd) => {
      const fc = faceOf(L, rec.c, sd);
      const bal = sd === rec.side && rec.f > 0;
      const s = bal ? rec.s0 : 0;
      const [x, z] = fpt(fc, s, bal ? 1.7 : 0.3);
      return { p: new THREE.Vector3(x, b.y - b.h * 0.04, z), n: SIDE_N[sd], bal };
    });
  }

  const bounds = new THREE.Box3(new THREE.Vector3(-W / 2 - 1.8, 0, -D / 2 - 1.8), new THREE.Vector3(W / 2 + 1.8, topY, D / 2 + 2.2));
  const sil = [];
  for (const y of [0, rTop + ph + 0.1]) for (const x of [-W / 2 - 1.7, W / 2 + 1.7]) for (const z of [-D / 2 - 1.7, D / 2 + 2.0]) sil.push(new THREE.Vector3(x, y, z));
  for (const x of [core.x0, core.x1]) for (const z of [core.z0, core.z1]) sil.push(new THREE.Vector3(x, topY, z));
  const solid = new THREE.Box3(new THREE.Vector3(-W / 2 - 1.8, -1, -D / 2 - 1.8), new THREE.Vector3(W / 2 + 1.8, topY + 0.5, D / 2 + 1.9));
  const site = new THREE.Box3(new THREE.Vector3(PX0, -0.6, PZ0), new THREE.Vector3(PX1, topY, PZ1));
  return {
    group, sil, north: northM, info, owned, nInst, neutralKeys, balInst, balOwner, coreMesh: MG.core, bounds, solid, site, F, N, W, D, floorTxt, L, yOf, hOf,
    key: F + 'x' + N + 'x' + (groundRes ? 'g' : 'p'),
  };
}

function mountBuilding(el, opts = {}) {
  const S = createStage(el, opts, 'building');
  if (!S.ok) return Object.assign(S.stub, { focusUnit() {}, setStatus() {}, update() {}, _debug: () => ({ ready: false }) });
  const T = S.T, C = S.controls;
  let o = Object.assign({}, opts);
  let M = null, tags = [], hoverKey = null, hoverRec = null, selected = null, floorTags = [], focusF = null;
  const edgesGeo = new THREE.EdgesGeometry(new THREE.BoxGeometry(1, 1, 1));
  const oHover = new THREE.LineSegments(edgesGeo, new THREE.LineBasicMaterial({ color: PAL.sea, transparent: true, opacity: 0.75 }));
  const oSel = new THREE.LineSegments(edgesGeo, new THREE.LineBasicMaterial({ color: PAL.sea }));
  oHover.visible = oSel.visible = false;
  S.scene.add(oHover, oSel);

  const statusTxt = (st) => T.status[st] || st;
  const BDG = { fix: '<svg viewBox="0 0 16 16"><path d="M9.8 4.2a2.7 2.7 0 0 0-3.6 3.6L2.6 11.4l2 2 3.6-3.6a2.7 2.7 0 0 0 3.6-3.6l-1.7 1.7-1.6-.4-.4-1.6z"/></svg>', end: '<svg viewBox="0 0 16 16"><circle cx="8" cy="8.6" r="5.2"/><path d="M8 5.8v3l2 1.2"/></svg>' };
  const badges = (u) => {
    const b = u.badges || {};
    return (b.repairs ? `<i class="nlrm3d-bdg">${BDG.fix}${b.repairs}</i>` : '') + (b.ending ? `<i class="nlrm3d-bdg nlrm3d-bdg--end">${BDG.end}</i>` : '');
  };
  const tagHtml = (rec) => `<span class="nlrm3d-pill"><i class="nlrm3d-dot" style="background:${STATUS[rec.status]}"></i><span class="nlrm3d-txt">${esc(rec.u.label || rec.id)}</span>${badges(rec.u)}</span>`;
  const tagAria = (rec) => [rec.u.label || rec.id, M.floorTxt(rec.f), statusTxt(rec.status), rec.u.tenant, (rec.u.badges || {}).text].filter(Boolean).join(', ');

  function pickUnit(id) {
    const rec = M.info.get(String(id));
    if (!rec) return;
    select(rec);
    if (typeof o.onPick === 'function') o.onPick(rec.id);
  }
  /* a floor: its label on the building's corner that faces the camera; a tap focuses the floor
     (the others fade) and tells the page, which opens the floor's card */
  function pickFloor(f) {
    focusFloor(f);
    if (typeof o.onPickFloor === 'function') o.onPickFloor(f);
  }
  function buildFloorTags() {
    floorTags.forEach((t) => t.el.remove());
    floorTags = [];
    if (typeof o.onPickFloor !== 'function') return;
    const floors = [...new Set([...M.info.values()].filter((r) => r.box).map((r) => r.f))].sort((a, b) => a - b);
    const ax = M.W / 2 + 1.1, az = M.D / 2 + 1.1;
    for (const f of floors) {
      const y = M.yOf(f) + M.hOf(f) * 0.5;
      const anchors = [[1, 1], [1, -1], [-1, 1], [-1, -1]].map(([sx, sz]) => ({ p: new THREE.Vector3(sx * ax, y, sz * az), n: new THREE.Vector3(sx, 0, sz).normalize(), bal: false }));
      const t = S.makeTag('nlrm3d-floor', 'f' + f, `<span class="nlrm3d-pill"><span class="nlrm3d-txt">${esc(M.floorTxt(f))}</span></span>`, M.floorTxt(f), () => pickFloor(f));
      t.rec = { anchors, f, isFloor: true };
      floorTags.push(t);
    }
  }
  function fade(on) {
    /* everything but the focused floor's apartments fades; materials restored exactly after */
    M.group.traverse((ob) => {
      if (!ob.material || ob.userData.unitId) return;
      const mats = Array.isArray(ob.material) ? ob.material : [ob.material];
      for (const m of mats) {
        if (on) {
          if (m.userData.nlrmKeep === undefined) m.userData.nlrmKeep = { t: m.transparent, o: m.opacity, d: m.depthWrite };
          m.transparent = true; m.opacity = Math.min(m.userData.nlrmKeep.o, 0.13); m.depthWrite = false;
        } else if (m.userData.nlrmKeep) {
          m.transparent = m.userData.nlrmKeep.t; m.opacity = m.userData.nlrmKeep.o; m.depthWrite = m.userData.nlrmKeep.d;
          delete m.userData.nlrmKeep;
        }
        m.needsUpdate = true;
      }
    });
    for (const rec of M.info.values()) {
      if (!rec.mesh) continue;
      const keep = !on || rec.f === focusF;
      rec.mesh.material.transparent = !keep; rec.mesh.material.opacity = keep ? 1 : 0.13; rec.mesh.material.depthWrite = keep; rec.mesh.material.needsUpdate = true;
      rec.edge.material.opacity = keep ? 0.95 : 0.12;
    }
  }
  function focusFloor(f) {
    if (!M) return false;
    focusF = +f;
    fade(true);
    floorTags.forEach((t) => t.el.classList.toggle('is-on', t.rec.f === focusF));
    const y = M.yOf(focusF) + M.hOf(focusF) * 0.5;
    const sph = new THREE.Spherical().setFromVector3(S.camera.position.clone().sub(C.target));
    const dist = clamp(S.home.dist * 0.78, C.minDistance, C.maxDistance);
    S.flyTo(new THREE.Vector3(0, y, 0), new THREE.Spherical(dist, clamp(1.05, C.minPolarAngle, C.maxPolarAngle), sph.theta));
    S.userMoved = true;
    S.invalidate();
    return true;
  }
  function clearFloor() {
    if (focusF === null) return;
    focusF = null;
    fade(false);
    floorTags.forEach((t) => t.el.classList.remove('is-on'));
    const h = S.home;
    S.flyTo(h.target, h.sph);
    S.userMoved = false;
    S.invalidate();
  }
  function select(rec) {
    selected = rec || null;
    tags.forEach((t) => t.el.classList.toggle('is-on', !!rec && t.id === rec.id));
    placeOutline(oSel, rec ? rec.box : null, rec && hoverRec === rec ? 0.12 : 0);
    S.invalidate();
  }
  function placeOutline(obj, b, lift) {
    if (!b) { obj.visible = false; return; }
    obj.visible = true;
    obj.position.set(b.x, b.y + (lift || 0), b.z);
    obj.scale.set(b.w + 0.08, b.h + 0.02, b.d + 0.08);
  }

  function build() {
    const prevKey = M ? M.key : null;
    if (M) { S.scene.remove(M.group); disposeTree(M.group); }
    tags.forEach((t) => t.el.remove());
    tags = [];
    hoverKey = null; hoverRec = null;
    M = buildBuildingModel(S, o);
    S.scene.add(M.group);
    for (const rec of M.info.values()) {
      if (!rec.box) continue;
      const t = S.makeTag('nlrm3d-unit', rec.id, tagHtml(rec), tagAria(rec), () => pickUnit(rec.id));
      t.rec = rec;
      rec.tag = t;
      tags.push(t);
    }
    buildFloorTags();
    if (focusF !== null) fade(true);
    S.cv.setAttribute('aria-label', fmt(T.bAria, { f: M.F, u: M.N }));
    S.cap.textContent = T.illus;
    if (selected) { const again = M.info.get(selected.id); selected = again && again.box ? again : null; }
    select(selected);
    return prevKey !== M.key;
  }

  function homeView() {
    // the three-quarter side that shows most of the landlord's balconies
    const cands = [0.62, -0.62, Math.PI - 0.62, -(Math.PI - 0.62)];
    let best = cands[0], bs = -1;
    cands.forEach((th, i) => {
      const dx = Math.sin(th), dz = Math.cos(th);
      let sc = i < 2 ? 2 : 0;
      if (th > 0 && i < 2) sc += 1;
      for (const rec of M.info.values()) {
        if (!rec.box) continue;
        const n = SIDE_N[rec.side];
        if (n.x * dx + n.z * dz > 0.15) sc += 10;
        else if (rec.c.sides.some((sd) => SIDE_N[sd].x * dx + SIDE_N[sd].z * dz > 0.15)) sc += 4;
      }
      if (sc > bs) { bs = sc; best = th; }
    });
    const b = M.bounds;
    const c = b.getCenter(new THREE.Vector3());
    c.y = b.min.y + (b.max.y - b.min.y) * 0.45;
    const phi = 1.2;
    const { target, dist } = S.frame(M.sil, phi, best, c, 0.07, 0.08, 'top');
    return { target, sph: new THREE.Spherical(dist, phi, best), dist, theta: best };
  }
  function fit() {
    const h = homeView();
    S.home = h;
    // the north arrow sits in the yard corner away from the camera, so it is in the picture
    M.north.position.x = (h.theta < 0 ? 1 : -1) * M.north.userData.x;
    const r = M.bounds.getSize(new THREE.Vector3()).length() / 2;
    C.minDistance = Math.max(r * 0.55, h.dist * 0.32);
    C.maxDistance = h.dist * 2.2;
    C.minPolarAngle = 0.12;
    C.maxPolarAngle = 1.5;
    S.place(h.target, h.sph);
    S.placeSun(M.site, h.theta - 0.95, 0.9);
  }

  /* ---- per frame: never inside the building, never under the ground; tags follow the facades */
  const push = new THREE.Vector3();
  S.hooks.before = () => {
    const cam = S.camera.position;
    if (M.solid.containsPoint(cam)) {
      push.copy(cam).sub(C.target).normalize();
      const b = M.solid;
      let tMax = Infinity;
      for (const ax of ['x', 'y', 'z']) {
        const d = push[ax];
        if (Math.abs(d) < 1e-6) continue;
        const t = ((d > 0 ? b.max[ax] : b.min[ax]) - C.target[ax]) / d;
        if (t > 0) tMax = Math.min(tMax, t);
      }
      if (isFinite(tMax)) cam.copy(C.target).addScaledVector(push, tMax + 0.5);
    }
    if (cam.y < 1.2) cam.y = 1.2;
  };
  S.hooks.overlay = () => {
    const cam = S.camera.position, items = [];
    for (const t of tags) {
      const rec = t.rec;
      let best = -2, bp = null;
      for (const a of rec.anchors) {
        const dx = cam.x - a.p.x, dz = cam.z - a.p.z, l = Math.hypot(dx, dz) || 1;
        const d = (a.n.x * dx + a.n.z * dz) / l;
        // the balcony (the unit's own direction) wins whenever it is in view
        const sc = d > 0.06 ? d + (a.bal ? 0.45 : 0) : d;
        if (sc > best) { best = sc; bp = a.p; }
      }
      /* a focused floor shows its own apartments only */
      items.push({ tag: t, p: bp, vis: best > 0.06 && (focusF === null || rec.f === focusF), d: bp ? cam.distanceTo(bp) : 0, prio: 0 });
    }
    for (const t of floorTags) {
      let best = -2, bp = null;
      for (const a of t.rec.anchors) {
        const dx = cam.x - a.p.x, dz = cam.z - a.p.z, l = Math.hypot(dx, dz) || 1;
        const d = (a.n.x * dx + a.n.z * dz) / l;
        if (d > best) { best = d; bp = a.p; }
      }
      items.push({ tag: t, p: bp, vis: best > 0 && (focusF === null || t.rec.f === focusF), d: bp ? cam.distanceTo(bp) : 0, prio: 1 });
    }
    S.layout(items);
  };
  S.hooks.measure = () => { tags.forEach((t) => t.measure()); floorTags.forEach((t) => t.measure()); };
  S.hooks.resize = () => { if (M && !S.userMoved) fit(); };

  /* ---- picking + hover */
  function hitAt(cx, cy) {
    const hits = S.raycast(cx, cy, [M.nInst, M.balInst, M.coreMesh, ...M.owned]);
    for (const h of hits) {
      const ob = h.object;
      if (ob === M.nInst && h.instanceId != null) return { empty: M.neutralKeys[h.instanceId] };
      if (ob.userData && ob.userData.unitId != null) return { rec: M.info.get(ob.userData.unitId) };
      if (ob === M.balInst && h.instanceId != null) {
        const k = M.balOwner[h.instanceId];
        if (k.id != null) return { rec: M.info.get(k.id) };
        return { empty: M.neutralKeys[k.idx] };
      }
      return null; // the core or anything else in front
    }
    return null;
  }
  function liftNeutral(k, on) {
    const i = M.neutralKeys.indexOf(k);
    if (i < 0) return;
    const b = k.box;
    M.nInst.setMatrixAt(i, m4(b.x, b.y + (on ? 0.12 : 0), b.z, b.w, b.h, b.d));
    M.nInst.setColorAt(i, new THREE.Color(on ? '#fffaf1' : '#ffffff'));
    M.nInst.instanceMatrix.needsUpdate = true;
    M.nInst.instanceColor.needsUpdate = true;
  }
  function setHover(h, cx, cy) {
    const key = !h ? null : h.rec ? 'u:' + h.rec.id : 'e:' + h.empty.f + ':' + h.empty.pos;
    if (key !== hoverKey) {
      if (hoverRec) { hoverRec.mesh.position.y = hoverRec.box.y; hoverRec.mesh.material.emissiveIntensity = 0.16; }
      else if (hoverKey && hoverKey[0] === 'e') { const [, f, p] = hoverKey.split(':'); const k = M.neutralKeys.find((q) => q.f === +f && q.pos === +p); if (k) liftNeutral(k, false); }
      hoverKey = key; hoverRec = null;
      if (h && h.rec) { hoverRec = h.rec; h.rec.mesh.position.y = h.rec.box.y + 0.12; h.rec.mesh.material.emissiveIntensity = 0.26; placeOutline(oHover, h.rec.box, 0.12); }
      else if (h && h.empty) { liftNeutral(h.empty, true); placeOutline(oHover, h.empty.box, 0.12); }
      else oHover.visible = false;
      if (selected) placeOutline(oSel, selected.box, hoverRec === selected ? 0.12 : 0);
      S.cv.style.cursor = h ? 'pointer' : '';
      S.invalidate();
    }
    if (!h) { S.tip(null); return; }
    if (h.rec) {
      const r = h.rec;
      S.tip(`<b>${esc(r.u.label || r.id)}</b><span>${esc(M.floorTxt(r.f))} · ${esc(statusTxt(r.status))}${r.u.tenant ? ' · ' + esc(r.u.tenant) : ''}</span>`, cx, cy);
    } else S.tip(`<b>${esc(M.floorTxt(h.empty.f))}</b><span>${esc(T.empty)}</span>`, cx, cy);
  }
  S.hooks.hover = (cx, cy) => {
    if (cx == null) { setHover(null); return; }
    setHover(hitAt(cx, cy), cx, cy);
  };
  S.hooks.pick = (cx, cy) => {
    const h = hitAt(cx, cy);
    if (!h) return;
    if (h.rec) pickUnit(h.rec.id);
    else if (typeof o.onPickEmpty === 'function') o.onPickEmpty(h.empty.f, h.empty.pos);
  };

  build();
  fit();

  const handle = {
    focusUnit(id) {
      const rec = M.info.get(String(id));
      if (!rec || !rec.box) return false;
      select(rec);
      const n = SIDE_N[rec.side];
      const th = Math.atan2(n.x, n.z);
      // aim at the unit's own facade (its balcony side), so the flat sits in the middle of the picture
      const fc = faceOf(M.L, rec.c, rec.side);
      const target = new THREE.Vector3(fc.cx + fc.tx * rec.s0, rec.box.y, fc.cz + fc.tz * rec.s0);
      const dist = clamp(S.home.dist * 0.62, C.minDistance, C.maxDistance);
      S.flyTo(target, new THREE.Spherical(dist, clamp(1.22, C.minPolarAngle, C.maxPolarAngle), th));
      S.userMoved = true;
      return true;
    },
    /* drill-down: a floor in focus (the others fade), and back to the whole building */
    focusFloor(f) { return focusFloor(f); },
    clearFloor() { clearFloor(); },
    focusedFloor() { return focusF; },
    setStatus(id, status) {
      const rec = M.info.get(String(id));
      if (!rec || !STATUS[status]) return false;
      rec.status = status;
      rec.u = Object.assign({}, rec.u, { status });
      if (Array.isArray(o.units)) o.units = o.units.map((u) => (u && String(u.id) === rec.id ? Object.assign({}, u, { status }) : u));
      if (rec.mesh) {
        const col = tintOf(status);
        rec.mesh.material.color.copy(col);
        rec.mesh.material.emissive.copy(col);
        rec.edge.material.color.copy(col.clone().lerp(new THREE.Color('#ffffff'), 0.35));
      }
      if (rec.tag) { const dot = rec.tag.el.querySelector('.nlrm3d-dot'); if (dot) dot.style.background = STATUS[status]; rec.tag.el.setAttribute('aria-label', tagAria(rec)); }
      S.invalidate();
      return true;
    },
    update(next = {}) {
      o = Object.assign({}, o, next);
      const changed = build();
      if (changed || !S.userMoved) fit();
      else S.placeSun(M.site, S.home.theta - 0.95, 0.9);
      S.invalidate();
    },
    dispose() {
      S.dispose();
      edgesGeo.dispose();
    },
    _debug() { return Object.assign(S.debug(), { units: M.info.size, floors: M.F, unitsPerFloor: M.N, tagsShown: tags.filter((t) => !t.off).length, floorTags: floorTags.length, floorTagsShown: floorTags.filter((t) => !t.off).length, focusF }); },
    /** QA probe: page (client) coordinates of an apartment's facade that faces the camera most, or null. */
    _pointOf(floor, pos, strict = true) {
      const f = +floor, p = +pos;
      const rec = [...M.info.values()].find((r) => r.f === f && r.c.pos === p);
      const k = rec ? null : M.neutralKeys.find((q) => q.f === f && q.pos === p);
      const b = rec ? rec.box : k ? k.box : null;
      const c = M.L.cells[p - 1];
      if (!b || !c) return null;
      const cam = S.camera.position, r = S.cv.getBoundingClientRect();
      const cands = [];
      for (const sd of c.sides) {
        const fc = faceOf(M.L, c, sd);
        const dx = cam.x - fc.cx, dz = cam.z - fc.cz, d = (fc.nx * dx + fc.nz * dz) / (Math.hypot(dx, dz) || 1);
        if (d <= 0.05) continue;
        for (const k of [0.3, -0.3, 0.42, -0.42, 0]) for (const dy of [0.2, -0.6, 0.9]) {
          const q = new THREE.Vector3(fc.cx + fc.tx * fc.len * k + fc.nx * 0.02, b.y + dy, fc.cz + fc.tz * fc.len * k + fc.nz * 0.02).project(S.camera);
          cands.push({ d, x: r.left + ((q.x + 1) / 2) * r.width, y: r.top + ((1 - q.y) / 2) * r.height });
        }
      }
      cands.sort((a, q) => q.d - a.d);
      for (const pt of cands) {
        if (!strict) return { x: pt.x, y: pt.y };
        const el = document.elementFromPoint(pt.x, pt.y);
        if (el !== S.cv) continue; // a label is on top there
        const h = hitAt(pt.x, pt.y);
        if (h && ((h.rec && h.rec.f === f && h.rec.c.pos === p) || (h.empty && h.empty.f === f && h.empty.pos === p))) return { x: pt.x, y: pt.y };
      }
      return null;
    },
  };
  S.mark(handle);
  return handle;
}

/* ================================================================== APARTMENT */
const polyArea = (p) => { let a = 0; for (let i = 0; i < p.length; i++) { const q = p[i], r = p[(i + 1) % p.length]; a += q[0] * r[1] - r[0] * q[1]; } return a / 2; };
function polyCentroid(p) {
  const A = polyArea(p);
  if (Math.abs(A) < 1e-9) { const n = p.length; return [p.reduce((s, q) => s + q[0], 0) / n, p.reduce((s, q) => s + q[1], 0) / n]; }
  let x = 0, y = 0;
  for (let i = 0; i < p.length; i++) { const q = p[i], r = p[(i + 1) % p.length], c = q[0] * r[1] - r[0] * q[1]; x += (q[0] + r[0]) * c; y += (q[1] + r[1]) * c; }
  return [x / (6 * A), y / (6 * A)];
}
function inPoly(p, x, y) {
  let ins = false;
  for (let i = 0, j = p.length - 1; i < p.length; j = i++) {
    const xi = p[i][0], yi = p[i][1], xj = p[j][0], yj = p[j][1];
    if (yi > y !== yj > y && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi) ins = !ins;
  }
  return ins;
}
function bbox2(pts) {
  const b = { x0: Infinity, y0: Infinity, x1: -Infinity, y1: -Infinity };
  for (const q of pts) { b.x0 = Math.min(b.x0, q[0]); b.y0 = Math.min(b.y0, q[1]); b.x1 = Math.max(b.x1, q[0]); b.y1 = Math.max(b.y1, q[1]); }
  return b;
}
function validPlan(p) {
  if (!p || typeof p !== 'object' || !Array.isArray(p.rooms) || !p.rooms.length) return false;
  const okPt = (q) => Array.isArray(q) && q.length >= 2 && isFinite(q[0]) && isFinite(q[1]);
  if (p.outline != null && (!Array.isArray(p.outline) || (p.outline.length && (p.outline.length < 3 || !p.outline.every(okPt))))) return false;
  return p.rooms.every((r) => r && r.id != null && Array.isArray(r.poly) && r.poly.length >= 3 && r.poly.every(okPt));
}

/** A plausible Israeli layout from a room count and an area: an open living room + kitchen on the balcony side, the
 *  bedrooms (one a ממ״ד from 3 rooms) on the other side, a bathroom (and a guest toilet from 4 rooms) by the entrance
 *  hall. Built with the balcony to the south, then turned to face `dir`. Rooms (balcony excluded) sum to `sqm`. */
function generatePlan(roomsIn, sqmIn, dirIn, T) {
  const rooms = clamp(Math.round((+roomsIn || 3) * 2) / 2, 1, 8);
  const sqm = clamp(+sqmIn || rooms * 24, 28, 400);
  const nFull = Math.floor(rooms - 1 + 1e-6);
  const half = rooms - Math.floor(rooms) >= 0.5;
  const beds = [];
  for (let i = 0; i < nFull; i++) beds.push({ kind: 'bedroom', a: i === 0 ? 12.5 : 10.5, master: i === 0 && nFull > 1 });
  let mamad = null;
  if (rooms >= 3 && beds.length >= 2) { mamad = beds.pop(); mamad.kind = 'mamad'; mamad.a = 10; }
  if (half) beds.push({ kind: 'bedroom', a: 7.4, study: true });
  if (mamad) beds.push(mamad);
  const toilet = rooms >= 4;
  let aBath = sqm > 115 ? 6 : 4.8;
  const aToil = toilet ? 1.7 : 0;
  let aHall = Math.max(3.4, sqm * 0.05);
  let aKit = clamp(6.5 + sqm * 0.05, 7.5, 14);
  let sumB = beds.reduce((s, b) => s + b.a, 0);
  let aLiv = sqm - sumB - aBath - aToil - aHall - aKit;
  const minLiv = Math.max(16, sqm * 0.27);
  if (aLiv < minLiv) {
    const k = Math.max(0.45, (sqm - minLiv - aBath - aToil) / (sumB + aHall + aKit));
    beds.forEach((b) => { b.a *= k; });
    aHall *= k; aKit *= k; sumB *= k;
    aLiv = sqm - sumB - aBath - aToil - aHall - aKit;
  }
  const W = Math.sqrt(sqm * 1.3), D = sqm / W;
  let Dq = beds.length ? (sumB + aBath + aToil + aHall) / W : Math.max(2.6, (aBath + aHall) / W);
  Dq = clamp(Dq, 2.6, D - 3.2);
  const Dp = D - Dq;
  const sc = Math.sqrt(sqm / 85);
  const ws = beds.length ? clamp((toilet ? 2.9 : 2.2) * sc, toilet ? 2.6 : 1.9, 3.6) : clamp(W * 0.36, 2.0, 3.2);
  const tb = clamp((aBath + aToil) / ws, 1.8, Dq - 1.25);
  const wk = clamp(aKit / Dp, 2.2, W * 0.42);
  const bd = 1.7, y0 = bd, yM = bd + Dp, y1 = bd + D;
  const R = [];
  const rect = (id, kind, label, xa, ya, xb, yb) => R.push({ id, kind, label, poly: [[xa, ya], [xb, ya], [xb, yb], [xa, yb]] });
  const RL = T.rooms;
  rect('kitchen', 'kitchen', RL.kitchen, 0, y0, wk, yM);
  if (beds.length) rect('living', 'living', RL.living, wk, y0, W, yM);
  else R.push({ id: 'living', kind: 'living', label: RL.living, poly: [[wk, y0], [W, y0], [W, y1], [ws, y1], [ws, yM], [wk, yM]] });
  rect('hall', 'hall', RL.hall, 0, yM, ws, y1 - tb);
  if (toilet) { rect('bath', 'bath', RL.bath, 0, y1 - tb, ws - 1.0, y1); rect('toilet', 'toilet', RL.toilet, ws - 1.0, y1 - tb, ws, y1); }
  else rect('bath', 'bath', RL.bath, 0, y1 - tb, ws, y1);
  const doors = [], windows = [];
  if (beds.length) {
    const tot = beds.reduce((s, b) => s + b.a, 0), bw = W - ws;
    let x = ws, n = 0;
    const plainCount = beds.filter((b) => b.kind === 'bedroom' && !b.master && !b.study).length;
    beds.forEach((b) => {
      const w = (bw * b.a) / tot;
      let id, label;
      if (b.kind === 'mamad') { id = 'mamad'; label = RL.mamad; }
      else if (b.study) { id = 'study'; label = RL.study; }
      else if (b.master) { id = 'bed1'; label = RL.master; }
      else { n++; id = 'bed' + (n + 1); label = plainCount > 1 ? RL.bedroom + ' ' + n : RL.bedroom; }
      rect(id, b.kind, label, x, yM, x + w, y1);
      if (Math.abs(x - ws) < 1e-6) doors.push({ at: [x, yM + (y1 - tb - yM) / 2], w: 0.85, between: ['hall', id] });
      else doors.push({ at: [Math.max(x, wk) + 0.6, yM], w: 0.85, between: ['living', id] });
      windows.push({ at: [x + w / 2, y1], w: b.kind === 'mamad' ? 1.0 : Math.min(1.6, w * 0.5), room: id, facing: 'north' });
      x += w;
    });
  }
  const balW = clamp((W - wk) * 0.8, 3, 7.5), bx1 = W - 0.35, bx0 = Math.max(wk + 0.2, bx1 - balW);
  R.push({ id: 'balcony', kind: 'balcony', label: RL.balcony, poly: [[bx0, 0], [bx1, 0], [bx1, y0], [bx0, y0]] });
  doors.push({ at: [0, yM + (y1 - tb - yM) / 2], w: 0.95, between: ['hall', 'exterior'] });
  if (toilet) { doors.push({ at: [(ws - 1.0) / 2, y1 - tb], w: 0.75, between: ['hall', 'bath'] }); doors.push({ at: [ws - 0.5, y1 - tb], w: 0.65, between: ['hall', 'toilet'] }); }
  else doors.push({ at: [ws / 2, y1 - tb], w: 0.75, between: ['hall', 'bath'] });
  doors.push({ at: [(bx0 + bx1) / 2, y0], w: Math.min(2.6, bx1 - bx0 - 0.6), between: ['living', 'balcony'] });
  windows.push({ at: [toilet ? (ws - 1.0) / 2 : ws / 2, y1], w: 0.6, room: 'bath', facing: 'north' });
  if (toilet) windows.push({ at: [ws - 0.5, y1], w: 0.45, room: 'toilet', facing: 'north' });
  windows.push({ at: [0, y0 + Dp / 2], w: 1.2, room: 'kitchen', facing: 'west' });
  windows.push({ at: [W, y0 + Dp / 2], w: 1.6, room: 'living', facing: 'east' });
  const outline = [[0, y0], [bx0, y0], [bx0, 0], [bx1, 0], [bx1, y0], [W, y0], [W, y1], [0, y1]];

  // turn so the balcony faces dir (plan +y = north): south 0, west 1, north 2, east 3 quarter turns clockwise
  const d = normDir(dirIn);
  const q = { south: 0, sw: 0, se: 0, west: 1, north: 2, ne: 2, nw: 2, east: 3 }[d || 'south'];
  const FACE = ['north', 'east', 'south', 'west'];
  const rot = (pt) => { let [x, y] = pt; for (let i = 0; i < q; i++) [x, y] = [y, -x]; return [x, y]; };
  const all = outline.map(rot);
  const mx = Math.min(...all.map((p) => p[0])), my = Math.min(...all.map((p) => p[1]));
  const tr = (pt) => { const r = rot(pt); return [Math.round((r[0] - mx) * 100) / 100, Math.round((r[1] - my) * 100) / 100]; };
  const turnFace = (f) => FACE[(FACE.indexOf(f) + q) % 4];
  return {
    v: 1, unit: 'm',
    outline: outline.map(tr),
    rooms: R.map((r) => ({ id: r.id, kind: r.kind, label: r.label, poly: r.poly.map(tr) })),
    doors: doors.map((x) => ({ at: tr(x.at), w: Math.round(x.w * 100) / 100, between: x.between })),
    windows: windows.map((x) => ({ at: tr(x.at), w: Math.round(x.w * 100) / 100, room: x.room, facing: turnFace(x.facing) })),
    meta: { generated: true, rooms, sqm: Math.round(sqm * 10) / 10, dir: d || 'south' },
  };
}

/** Wall segments: every room edge split at every vertex lying on it, de-duplicated, with the room on each side. */
function planSegments(plan) {
  const rooms = plan.rooms;
  const pts = [];
  rooms.forEach((r) => r.poly.forEach((q) => pts.push(q)));
  (plan.outline || []).forEach((q) => pts.push(q));
  const key = (q) => Math.round(q[0] * 100) + ',' + Math.round(q[1] * 100);
  const segs = new Map();
  const addEdge = (a, b) => {
    const dx = b[0] - a[0], dy = b[1] - a[1], L2 = dx * dx + dy * dy;
    if (L2 < 4e-4) return;
    const ts = [0, 1];
    for (const q of pts) {
      const t = ((q[0] - a[0]) * dx + (q[1] - a[1]) * dy) / L2;
      if (t <= 1e-4 || t >= 1 - 1e-4) continue;
      if (Math.hypot(q[0] - (a[0] + dx * t), q[1] - (a[1] + dy * t)) < 0.005) ts.push(t);
    }
    ts.sort((u, v) => u - v);
    for (let i = 0; i < ts.length - 1; i++) {
      const p0 = [a[0] + dx * ts[i], a[1] + dy * ts[i]], p1 = [a[0] + dx * ts[i + 1], a[1] + dy * ts[i + 1]];
      if (Math.hypot(p1[0] - p0[0], p1[1] - p0[1]) < 0.02) continue;
      const k1 = key(p0), k2 = key(p1), k = k1 < k2 ? k1 + '|' + k2 : k2 + '|' + k1;
      if (!segs.has(k)) segs.set(k, k1 < k2 ? [p0, p1] : [p1, p0]);
    }
  };
  rooms.forEach((r) => { const p = r.poly; for (let i = 0; i < p.length; i++) addEdge(p[i], p[(i + 1) % p.length]); });
  (plan.outline || []).forEach((q, i, arr) => addEdge(q, arr[(i + 1) % arr.length]));
  const roomAt = (x, y) => rooms.find((r) => inPoly(r.poly, x, y)) || null;
  const out = [];
  for (const [a, b] of segs.values()) {
    const dx = b[0] - a[0], dy = b[1] - a[1], L = Math.hypot(dx, dy), ux = dx / L, uy = dy / L, nx = -uy, ny = ux;
    const mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2, e = 0.06;
    const A = roomAt(mx + nx * e, my + ny * e), B = roomAt(mx - nx * e, my - ny * e);
    if ((!A && !B) || A === B) continue;
    out.push({ a, b, L, ux, uy, nx, ny, A, B, ops: [] });
  }
  return out;
}

function buildApartmentModel(S, o) {
  const T = S.T;
  let plan, generated = false;
  if (validPlan(o.plan)) plan = JSON.parse(JSON.stringify(o.plan));
  else { plan = generatePlan(o.rooms, o.sqm, o.dir, T); generated = true; }
  plan.rooms.forEach((r) => { r.id = String(r.id); if (!ROOM_KINDS.includes(r.kind)) r.kind = 'living'; });
  const outline = plan.outline && plan.outline.length >= 3 ? plan.outline : null;
  const bb = bbox2((outline || []).concat(...plan.rooms.map((r) => r.poly)));
  const cx = (bb.x0 + bb.x1) / 2, cy = (bb.y0 + bb.y1) / 2;
  const WP = (x, y, h = 0) => new THREE.Vector3(x - cx, h, -(y - cy));
  const H = WALL_H;
  const group = new THREE.Group();
  group.name = 'nlrm3d-apartment';

  /* ---- base slab */
  const shapeOf = (poly) => new THREE.Shape(poly.map((q) => new THREE.Vector2(q[0] - cx, q[1] - cy)));
  const baseMat = std('#ebe7df', 0.95);
  const basePolys = outline ? [outline] : plan.rooms.map((r) => r.poly);
  for (const poly of basePolys) {
    const g = new THREE.ExtrudeGeometry(shapeOf(poly), { depth: 0.3, bevelEnabled: false });
    g.rotateX(-Math.PI / 2);
    g.translate(0, -0.3, 0);
    const m = new THREE.Mesh(g, baseMat);
    m.receiveShadow = true;
    group.add(m);
    const e = new THREE.LineSegments(new THREE.EdgesGeometry(g, 30), new THREE.LineBasicMaterial({ color: '#d4cec3' }));
    group.add(e);
  }

  /* ---- room floors */
  const rooms = plan.rooms.map((r) => {
    const g = new THREE.ShapeGeometry(shapeOf(r.poly));
    g.rotateX(-Math.PI / 2);
    const mat = std(TONE[r.kind] || TONE.living, 0.94, 0, { emissive: new THREE.Color(PAL.sea), emissiveIntensity: 0, polygonOffset: true, polygonOffsetFactor: -1, polygonOffsetUnits: -2 });
    const m = new THREE.Mesh(g, mat);
    m.position.y = r.kind === 'balcony' ? -0.035 : 0.004;
    m.receiveShadow = true;
    m.userData.roomId = r.id;
    group.add(m);
    const label = r.label || T.rooms[r.kind] || r.kind;
    return { r, id: r.id, kind: r.kind, mesh: m, area: Math.abs(polyArea(r.poly)), c: polyCentroid(r.poly), bb: bbox2(r.poly), label };
  });
  const roomById = new Map(rooms.map((x) => [x.id, x]));

  /* ---- walls with openings */
  const segs = planSegments(plan);
  const OPEN = new Set(['hall|kitchen', 'hall|living', 'kitchen|living']);
  const walls = [], seams = [];
  for (const s of segs) {
    const A = s.A, B = s.B;
    if (A && B) {
      if (OPEN.has([A.kind, B.kind].sort().join('|'))) { seams.push(s); continue; }
      if (A.kind === 'balcony' && B.kind === 'balcony') continue;
      const bal = A.kind === 'balcony' ? A : B.kind === 'balcony' ? B : null;
      if (bal) { s.type = 'facade'; s.t = 0.25; s.shift = (bal === A ? 1 : -1) * 0.125; }
      else { s.type = 'inner'; s.t = A.kind === 'mamad' || B.kind === 'mamad' ? 0.3 : 0.12; s.shift = 0; }
    } else {
      const R = A || B, out = A ? -1 : 1;
      if (R.kind === 'balcony') { s.type = 'rail'; s.t = 0.06; s.shift = out * 0.03; }
      else { s.type = 'outer'; s.t = R.kind === 'mamad' ? 0.32 : 0.25; s.shift = (out * s.t) / 2; }
    }
    walls.push(s);
  }
  const segDist = (s, x, y) => {
    const t = clamp((x - s.a[0]) * s.ux + (y - s.a[1]) * s.uy, 0, s.L);
    return { d: Math.hypot(x - (s.a[0] + s.ux * t), y - (s.a[1] + s.uy * t)), t };
  };
  const has = (s, id) => (s.A && s.A.id === id) || (s.B && s.B.id === id);
  const blockers = new Map(); // room id -> points that must stay free (doors, sliders, open sides)
  const block = (id, x, y) => { if (!id) return; if (!blockers.has(id)) blockers.set(id, []); blockers.get(id).push([x, y]); };
  for (const d of plan.doors || []) {
    if (!d || !Array.isArray(d.at)) continue;
    const ids = Array.isArray(d.between) ? d.between.map(String) : [];
    let best = null;
    for (const s of walls) {
      if (s.type === 'rail') continue;
      const q = segDist(s, +d.at[0], +d.at[1]);
      if (q.d > 0.45) continue;
      const score = q.d - ids.filter((id) => has(s, id)).length * 0.3;
      if (!best || score < best.score) best = { s, q, score };
    }
    if (!best) continue;
    const s = best.s;
    const w = clamp(+d.w || 0.85, 0.55, Math.max(0.55, s.L - 0.1));
    const kind = s.type === 'facade' ? 'slider' : s.type === 'outer' ? 'entry' : 'door';
    s.ops.push({ kind, c: clamp(best.q.t, w / 2, s.L - w / 2), w });
    if (s.A) block(s.A.id, +d.at[0], +d.at[1]);
    if (s.B) block(s.B.id, +d.at[0], +d.at[1]);
  }
  for (const wd of plan.windows || []) {
    if (!wd || !Array.isArray(wd.at)) continue;
    let best = null;
    for (const s of walls) {
      if (s.type !== 'outer' && s.type !== 'facade') continue;
      const q = segDist(s, +wd.at[0], +wd.at[1]);
      if (q.d > 0.45) continue;
      const score = q.d - (wd.room != null && has(s, String(wd.room)) ? 0.3 : 0);
      if (!best || score < best.score) best = { s, q, score };
    }
    if (!best) continue;
    const s = best.s, R = s.A || s.B;
    const w = clamp(+wd.w || 1.2, 0.4, Math.max(0.4, s.L - 0.2));
    const small = ['bath', 'toilet', 'laundry', 'storage'].includes(R.kind);
    s.ops.push({ kind: 'window', c: clamp(best.q.t, w / 2, s.L - w / 2), w, sill: small ? 1.45 : 0.9, head: small ? 2.15 : 2.2 });
  }
  for (const s of seams) { const m = [(s.a[0] + s.b[0]) / 2, (s.a[1] + s.b[1]) / 2]; block(s.A.id, m[0], m[1]); block(s.B.id, m[0], m[1]); }

  const wallParts = [], edgeParts = [], glassParts = [], furn = [], arcPts = [];
  const capFor = (s) => ((s.A && s.A.kind === 'mamad') || (s.B && s.B.kind === 'mamad') ? '#cbc4b6' : PAL.edge);
  // Dollhouse cut-away: the outer walls are grouped by the way they face; the groups facing the camera drop to CUT
  // metres (a separate low version with its own caps), so the near rooms stay readable from any side.
  const CUT = 1.0;
  const cut = new Map();
  const bucketOf = (s) => {
    if (s.type !== 'outer' && s.type !== 'facade') return null;
    const sg = s.shift >= 0 ? 1 : -1; // the shift points outward (or toward the balcony)
    const k = Math.round(Math.atan2(s.ny * sg, s.nx * sg) / (Math.PI / 4)) & 7;
    let b = cut.get(k);
    if (!b) cut.set(k, (b = { k, n: [Math.cos((k * Math.PI) / 4), -Math.sin((k * Math.PI) / 4)], full: [], efull: [], low: [], elow: [], glass: [] }));
    return b;
  };
  const wallBox = (s, a0, a1, y0, y1) => {
    const mid = (a0 + a1) / 2;
    const g = new THREE.BoxGeometry(a1 - a0, y1 - y0, s.t);
    colorize(g, PAL.wall, capFor(s));
    g.rotateY(Math.atan2(s.uy, s.ux));
    const w = WP(s.a[0] + s.ux * mid + s.nx * s.shift, s.a[1] + s.uy * mid + s.ny * s.shift, (y0 + y1) / 2);
    g.translate(w.x, w.y, w.z);
    return g;
  };
  const piece = (s, s0, s1, y0, y1) => {
    if (s1 - s0 < 0.01 || y1 - y0 < 0.01) return;
    let a0 = s0, a1 = s1;
    if (s.type === 'outer') { if (a0 <= 1e-6) a0 -= s.t / 2; if (a1 >= s.L - 1e-6) a1 += s.t / 2; }
    const g = wallBox(s, a0, a1, y0, y1);
    const b = bucketOf(s);
    if (!b) { wallParts.push(g); edgeParts.push(new THREE.EdgesGeometry(g, 25)); return; }
    b.full.push(g); b.efull.push(new THREE.EdgesGeometry(g, 25));
    if (y0 < CUT - 0.01) { const gl = wallBox(s, a0, a1, y0, Math.min(y1, CUT)); b.low.push(gl); b.elow.push(new THREE.EdgesGeometry(gl, 25)); }
  };
  const pane = (s, s0, s1, y0, y1, th = 0.03) => {
    const mid = (s0 + s1) / 2;
    const g = new THREE.BoxGeometry(s1 - s0, y1 - y0, th);
    g.rotateY(Math.atan2(s.uy, s.ux));
    const w = WP(s.a[0] + s.ux * mid + s.nx * s.shift, s.a[1] + s.uy * mid + s.ny * s.shift, (y0 + y1) / 2);
    g.translate(w.x, w.y, w.z);
    const b = bucketOf(s);
    (b ? b.glass : glassParts).push(g);
  };
  // furniture and door leaves share one vertex-coloured mesh
  const fbox = (x, y, ang, w, d, h, y0, color) => {
    const g = new THREE.BoxGeometry(w, h, d);
    colorize(g, color);
    g.rotateY(ang);
    const p = WP(x, y, y0 + h / 2);
    g.translate(p.x, p.y, p.z);
    furn.push(g);
  };
  const fcyl = (x, y, r, h, y0, color) => {
    const g = new THREE.CylinderGeometry(r, r, h, 18);
    colorize(g, color);
    const p = WP(x, y, y0 + h / 2);
    g.translate(p.x, p.y, p.z);
    furn.push(g);
  };
  const rank = (R) => (!R ? -1 : ['hall', 'living', 'kitchen'].includes(R.kind) ? (R.kind === 'hall' ? 0 : 1) : 2);
  const doorLeaf = (s, op, a, b) => {
    let into;
    if (s.A && s.B) into = rank(s.A) >= rank(s.B) ? 1 : -1;
    else into = s.A ? 1 : -1;
    const w = b - a;
    const off = s.shift + (into * s.t) / 2;
    const hx = s.a[0] + s.ux * a + s.nx * off, hy = s.a[1] + s.uy * a + s.ny * off;
    const lw = w - 0.04;
    fbox(hx + s.nx * into * (lw / 2), hy + s.ny * into * (lw / 2), Math.atan2(into * s.ny, into * s.nx), lw, 0.04, 2.04, 0.0, op.kind === 'entry' ? '#c3b49d' : '#f5f3ee');
    const seg = 10;
    for (let i = 0; i < seg; i++) {
      const t0 = (i / seg) * (Math.PI / 2), t1 = ((i + 1) / seg) * (Math.PI / 2);
      const pt = (t) => { const c = Math.cos(t), sn = Math.sin(t); return WP(hx + (s.ux * c + s.nx * into * sn) * lw, hy + (s.uy * c + s.ny * into * sn) * lw, 0.015); };
      arcPts.push(pt(t0), pt(t1));
    }
  };
  const railParts = [], railTop = [];
  for (const s of walls) {
    if (s.type === 'rail') {
      const mid = s.L / 2, ang = Math.atan2(s.uy, s.ux);
      const p = WP(s.a[0] + s.ux * mid + s.nx * s.shift, s.a[1] + s.uy * mid + s.ny * s.shift, 0);
      const g = new THREE.BoxGeometry(s.L, 1.0, 0.03); g.rotateY(ang); g.translate(p.x, 0.5 - 0.03, p.z); railParts.push(g);
      const t = new THREE.BoxGeometry(s.L + 0.04, 0.05, 0.06); colorize(t, '#8a9298'); t.rotateY(ang); t.translate(p.x, 1.0, p.z); railTop.push(t);
      continue;
    }
    const ops = s.ops.sort((p, q) => p.c - q.c);
    let cur = 0;
    for (const op of ops) {
      const a = op.c - op.w / 2, b = op.c + op.w / 2;
      if (a < cur - 1e-3) continue;
      piece(s, cur, a, 0, H);
      if (op.kind === 'window') { piece(s, a, b, 0, op.sill); piece(s, a, b, op.head, H); pane(s, a, b, op.sill, op.head); }
      else if (op.kind === 'slider') { piece(s, a, b, 2.3, H); pane(s, a, b, 0.02, 2.3); }
      else { piece(s, a, b, 2.1, H); doorLeaf(s, op, a, b); }
      cur = b;
    }
    piece(s, cur, s.L, 0, H);
  }
  const wallMat = std('#ffffff', 0.9, 0, { vertexColors: true });
  if (wallParts.length) {
    const g = mergeGeometries(wallParts, false); wallParts.forEach((x) => x.dispose());
    const m = new THREE.Mesh(g, wallMat); m.castShadow = m.receiveShadow = true; m.name = 'walls'; group.add(m);
    const eg = mergeGeometries(edgeParts, false); edgeParts.forEach((x) => x.dispose());
    group.add(new THREE.LineSegments(eg, new THREE.LineBasicMaterial({ color: '#cfc9be' })));
  }
  const glassMat = std(PAL.glass, 0.1, 0.25, { transparent: true, opacity: 0.42, depthWrite: false });
  if (glassParts.length) { const g = mergeGeometries(glassParts, false); glassParts.forEach((x) => x.dispose()); group.add(new THREE.Mesh(g, glassMat)); }
  const edgeMat = new THREE.LineBasicMaterial({ color: '#cfc9be' });
  const merged = (list) => { const g = list.length === 1 ? list[0] : mergeGeometries(list, false); if (list.length > 1) list.forEach((x) => x.dispose()); return g; };
  for (const b of cut.values()) {
    b.fullG = new THREE.Group(); b.lowG = new THREE.Group();
    if (b.full.length) { const m = new THREE.Mesh(merged(b.full), wallMat); m.castShadow = m.receiveShadow = true; b.fullG.add(m, new THREE.LineSegments(merged(b.efull), edgeMat)); }
    if (b.glass.length) b.fullG.add(new THREE.Mesh(merged(b.glass), glassMat));
    if (b.low.length) { const m = new THREE.Mesh(merged(b.low), wallMat); m.castShadow = m.receiveShadow = true; b.lowG.add(m, new THREE.LineSegments(merged(b.elow), edgeMat)); }
    b.lowG.visible = false;
    group.add(b.fullG, b.lowG);
  }
  if (railParts.length) { const g = mergeGeometries(railParts, false); railParts.forEach((x) => x.dispose()); group.add(new THREE.Mesh(g, std('#cfdee4', 0.08, 0.1, { transparent: true, opacity: 0.32, depthWrite: false, side: THREE.DoubleSide }))); }
  if (railTop.length) furn.push(...railTop);
  if (seams.length) {
    const pts = [];
    seams.forEach((s) => pts.push(WP(s.a[0], s.a[1], 0.012), WP(s.b[0], s.b[1], 0.012)));
    group.add(new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints(pts), new THREE.LineBasicMaterial({ color: '#d6d0c5' })));
  }
  if (arcPts.length) group.add(new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints(arcPts), new THREE.LineBasicMaterial({ color: '#c3bcae' })));

  /* ---- furniture (rectangular rooms only): calm, light blocks that make each room read at a glance */
  const isRect = (p) => p.length === 4 && p.every((q, i) => { const r = p[(i + 1) % 4]; return Math.abs(q[0] - r[0]) < 1e-3 || Math.abs(q[1] - r[1]) < 1e-3; });
  const FC = { body: '#f2efe9', soft: '#dfe2e3', linen: '#f7f6f3', blanket: '#cdd6dc', wood: '#cdbfa8', green: '#a9b59d', counter: '#e6e2da', tub: '#ffffff', dark: '#9aa2a8' };
  for (const R of rooms) {
    if (!isRect(R.r.poly)) continue;
    const { x0, y0, x1, y1 } = R.bb;
    const sides = [
      { a: [x0, y0], b: [x1, y0], n: [0, 1] }, { a: [x1, y0], b: [x1, y1], n: [-1, 0] },
      { a: [x1, y1], b: [x0, y1], n: [0, -1] }, { a: [x0, y1], b: [x0, y0], n: [1, 0] },
    ].map((sd) => {
      const L = Math.hypot(sd.b[0] - sd.a[0], sd.b[1] - sd.a[1]);
      const u = [(sd.b[0] - sd.a[0]) / L, (sd.b[1] - sd.a[1]) / L];
      const bl = (blockers.get(R.id) || []).some((q) => {
        const t = clamp((q[0] - sd.a[0]) * u[0] + (q[1] - sd.a[1]) * u[1], 0, L);
        return Math.hypot(q[0] - (sd.a[0] + u[0] * t), q[1] - (sd.a[1] + u[1] * t)) < 0.2;
      });
      return Object.assign(sd, { L, u, blocked: bl, ang: Math.atan2(u[1], u[0]) });
    });
    const free = sides.filter((sd) => !sd.blocked).sort((p, q) => q.L - p.L);
    R.free = free;
    const at = (sd, t, d) => [sd.a[0] + sd.u[0] * t + sd.n[0] * d, sd.a[1] + sd.u[1] * t + sd.n[1] * d];
    const item = (sd, t, w, d, h, y0, color, gap = 0.04) => { const p = at(sd, t, d / 2 + gap); fbox(p[0], p[1], sd.ang, w, d, h, y0, color); };
    const sd = free[0];
    const rw = x1 - x0, rh = y1 - y0;
    if (R.kind === 'bedroom' && sd && Math.min(rw, rh) > 2.1) {
      const study = R.id === 'study' || (R.area < 8.2 && R.id !== 'bed1');
      if (study) {
        item(sd, sd.L / 2, Math.min(1.3, sd.L - 0.4), 0.6, 0.74, 0, FC.wood);
        const p = at(sd, sd.L / 2, 0.95); fbox(p[0], p[1], sd.ang, 0.46, 0.46, 0.46, 0, FC.soft);
      } else {
        const bw = Math.min(rw, rh) >= 3 && sd.L >= 2.8 ? 1.6 : 1.4;
        item(sd, sd.L / 2, bw, 2.0, 0.42, 0, FC.linen);
        item(sd, sd.L / 2, bw, 0.08, 0.95, 0, FC.wood, 0.0);
        const pb = at(sd, sd.L / 2, 0.04 + 1.25); fbox(pb[0], pb[1], sd.ang, bw + 0.02, 1.1, 0.08, 0.4, FC.blanket);
        for (const k of [-1, 1]) { const pp = at(sd, sd.L / 2 + (k * bw) / 4, 0.32); fbox(pp[0], pp[1], sd.ang, bw / 2 - 0.12, 0.34, 0.12, 0.42, '#ffffff'); }
        if (sd.L >= bw + 1.2) for (const k of [-1, 1]) item(sd, sd.L / 2 + k * (bw / 2 + 0.32), 0.44, 0.42, 0.48, 0, FC.wood);
        const opp = free.find((q) => q !== sd && Math.abs(q.ang - sd.ang) > 0.1 && q.L > 1.6);
        if (opp) item(opp, opp.L / 2, Math.min(2.0, opp.L - 0.6), 0.58, 2.1, 0, FC.body);
      }
    } else if (R.kind === 'mamad' && sd) {
      item(sd, Math.min(sd.L - 0.55, 1.05), 0.9, 1.95, 0.42, 0, FC.linen);
      const pb = at(sd, Math.min(sd.L - 0.55, 1.05), 1.25); fbox(pb[0], pb[1], sd.ang, 0.92, 1.1, 0.08, 0.4, FC.blanket);
      if (sd.L > 2.6) item(sd, sd.L - 0.6, 1.0, 0.55, 0.74, 0, FC.wood);
    } else if (R.kind === 'living' && sd) {
      const sw = Math.min(2.3, sd.L - 0.6);
      item(sd, sd.L / 2, sw, 0.9, 0.42, 0, FC.soft);
      item(sd, sd.L / 2, sw, 0.2, 0.82, 0, FC.soft, 0.02);
      for (const k of [-1, 1]) { const p = at(sd, sd.L / 2 + k * (sw / 2 - 0.1), 0.5); fbox(p[0], p[1], sd.ang, 0.2, 0.9, 0.6, 0, FC.soft); }
      const pr = at(sd, sd.L / 2, 2.05); fbox(pr[0], pr[1], sd.ang, Math.min(2.6, sd.L - 0.6), 1.8, 0.012, 0, '#ddd4c4');
      const pt = at(sd, sd.L / 2, 1.75); fbox(pt[0], pt[1], sd.ang, 1.05, 0.6, 0.36, 0.012, FC.wood);
    } else if (R.kind === 'kitchen' && sd) {
      const same = (p, q) => Math.hypot(p[0] - q[0], p[1] - q[1]) < 1e-3;
      const adj = free.find((q) => q !== sd && (same(q.a, sd.b) || same(q.b, sd.a)) && q.L > 1.8);
      const cornerAtEnd = adj ? same(adj.a, sd.b) : true; // the L meets the main run at its end (else at its start)
      const fT = cornerAtEnd ? 0.4 : sd.L - 0.4;
      const r0 = cornerAtEnd ? 0.8 : 0.03, r1 = cornerAtEnd ? sd.L - 0.03 : sd.L - 0.8;
      item(sd, (r0 + r1) / 2, r1 - r0, 0.62, 0.88, 0, FC.body);
      item(sd, (r0 + r1) / 2, r1 - r0, 0.64, 0.04, 0.88, FC.counter, 0.03);
      item(sd, fT, 0.72, 0.66, 1.85, 0, '#e9ebec');
      if (adj) {
        const a0 = cornerAtEnd ? 0.66 : 0.1, a1 = cornerAtEnd ? adj.L - 0.1 : adj.L - 0.66;
        if (a1 - a0 > 0.8) { item(adj, (a0 + a1) / 2, a1 - a0, 0.62, 0.88, 0, FC.body); item(adj, (a0 + a1) / 2, a1 - a0, 0.64, 0.04, 0.88, FC.counter, 0.03); }
      }
    } else if (R.kind === 'bath' && sd) {
      item(sd, Math.min(0.9, sd.L / 2), Math.min(1.7, sd.L - 0.1), 0.75, 0.55, 0, FC.tub);
      const v = free[1];
      if (v) item(v, v.L / 2, 0.8, 0.48, 0.85, 0, FC.body);
    } else if (R.kind === 'toilet' && sd) {
      item(sd, sd.L / 2, 0.38, 0.62, 0.42, 0, FC.tub);
    } else if (R.kind === 'laundry' && sd) {
      item(sd, 0.4, 0.62, 0.62, 0.86, 0, '#f4f4f2');
    } else if (R.kind === 'hall' && sd && sd.L > 1.2) {
      item(sd, sd.L / 2, Math.min(1.1, sd.L - 0.3), 0.34, 0.9, 0, FC.body);
    } else if (R.kind === 'balcony') {
      const alongX = rw >= rh, p = [R.c[0], R.c[1]];
      const ax = alongX ? [1, 0] : [0, 1];
      fcyl(p[0], p[1], 0.34, 0.72, -0.035, FC.body);
      for (const k of [-1, 1]) fbox(p[0] + ax[0] * k * 0.62, p[1] + ax[1] * k * 0.62, 0, 0.46, 0.46, 0.46, -0.035, FC.soft);
      if (Math.max(rw, rh) > 3) {
        const q = alongX ? [x1 - 0.55, (y0 + y1) / 2] : [(x0 + x1) / 2, y1 - 0.55];
        const an = alongX ? Math.PI / 2 : 0;
        fbox(q[0], q[1], an, 0.9, 0.42, 0.36, -0.035, FC.body);
        fbox(q[0], q[1], an, 0.86, 0.38, 0.07, 0.325, FC.green);
      }
    }
  }
  if (furn.length) {
    const g = mergeGeometries(furn, false); furn.forEach((x) => x.dispose());
    const m = new THREE.Mesh(g, std('#ffffff', 0.85, 0, { vertexColors: true }));
    m.castShadow = m.receiveShadow = true; m.name = 'furniture';
    group.add(m);
  }

  /* ---- asset pins */
  const today = new Date(); today.setHours(0, 0, 0, 0);
  const assets = (Array.isArray(o.assets) ? o.assets : []).filter((a) => a && a.id != null);
  const doorsOf = (id) => (plan.doors || []).filter((d) => Array.isArray(d.between) && d.between.map(String).includes(id) && Array.isArray(d.at));
  const inset = (R, q, k) => [clamp(q[0], R.bb.x0 + k, R.bb.x1 - k), clamp(q[1], R.bb.y0 + k, R.bb.y1 - k)];
  const corners = (R) => [[R.bb.x0, R.bb.y0], [R.bb.x1, R.bb.y0], [R.bb.x1, R.bb.y1], [R.bb.x0, R.bb.y1]];
  const farCorner = (R, from, k) => { let best = null, bd = -1; for (const q of corners(R)) { const d = from ? Math.hypot(q[0] - from[0], q[1] - from[1]) : 0; if (d > bd) { bd = d; best = q; } } return inset(R, best, k); };
  const nearCorner = (R, from, k) => { let best = null, bd = Infinity; for (const q of corners(R)) { const d = Math.hypot(q[0] - from[0], q[1] - from[1]); if (d < bd) { bd = d; best = q; } } return inset(R, best, k); };
  const byKind = (...ks) => { for (const k of ks) { const r = rooms.find((x) => x.kind === k); if (r) return r; } return null; };
  const HGT = { boiler: 2.25, ac: 2.2, panel: 1.6, water_meter: 0.85, dishwasher: 0.85, fridge: 1.5, oven: 0.9, washer: 0.85 };
  const spots = [];
  const spotOf = (a) => {
    const kind = String(a.kind || '').toLowerCase();
    const h = HGT[kind] != null ? HGT[kind] : 1.2;
    if (Array.isArray(a.at) && isFinite(a.at[0]) && isFinite(a.at[1])) return { x: +a.at[0], y: +a.at[1], h };
    if (a.room != null) { const R = roomById.get(String(a.room)) || byKind(String(a.room)); if (R) return { x: R.c[0], y: R.c[1], h }; }
    let R = null, pt = null;
    if (kind === 'boiler') { R = byKind('bath', 'laundry', 'toilet'); if (R) { const d = doorsOf(R.id)[0]; pt = farCorner(R, d ? d.at : R.c, 0.4); } }
    else if (kind === 'ac') {
      R = byKind('living');
      if (R && R.free && R.free.length) {
        // on a real wall of the living room (the sofa wall), a quarter of the way along, never on the open kitchen side
        const sd = R.free[0], t = sd.L * 0.26;
        pt = [sd.a[0] + sd.u[0] * t + sd.n[0] * 0.3, sd.a[1] + sd.u[1] * t + sd.n[1] * 0.3];
      } else if (R) pt = inset(R, [R.c[0], R.bb.y1], 0.3);
    }
    else if (kind === 'panel') {
      R = byKind('hall');
      if (R) {
        const d = doorsOf(R.id).find((x) => x.between.includes('exterior')) || doorsOf(R.id)[0];
        if (d) {
          // beside the entrance door, on the same wall
          const onX = Math.abs(d.at[0] - R.bb.x0) < 0.05 || Math.abs(d.at[0] - R.bb.x1) < 0.05;
          const q = onX ? [d.at[0], d.at[1] + (d.at[1] > R.c[1] ? -0.75 : 0.75)] : [d.at[0] + (d.at[0] > R.c[0] ? -0.75 : 0.75), d.at[1]];
          pt = inset(R, q, 0.3);
        } else pt = inset(R, [R.bb.x0, R.bb.y0], 0.4);
      }
    }
    else if (kind === 'water_meter') { R = byKind('hall'); if (R) { const p = spots.find((q) => q.kind === 'panel'); pt = farCorner(R, p ? [p.x, p.y] : [R.bb.x0, R.bb.y0], 0.35); } }
    else if (['dishwasher', 'fridge', 'oven'].includes(kind)) { R = byKind('kitchen'); if (R) { const long = R.bb.x1 - R.bb.x0 >= R.bb.y1 - R.bb.y0; const f = { fridge: 0.18, oven: 0.5, dishwasher: 0.78 }[kind]; pt = long ? [lerp(R.bb.x0, R.bb.x1, f), R.c[1]] : [R.c[0], lerp(R.bb.y0, R.bb.y1, f)]; } }
    else if (kind === 'washer') { R = byKind('laundry', 'bath'); if (R) { const d = doorsOf(R.id)[0]; pt = d ? nearCorner(R, d.at, 0.45) : inset(R, [R.bb.x0, R.bb.y0], 0.45); } }
    if (!R) R = byKind('living') || rooms[0];
    if (!pt) pt = R.c;
    return { x: pt[0], y: pt[1], h };
  };
  const pinMat = { ink: std(PAL.ink, 0.5, 0.1), white: std('#ffffff', 0.4), warn: std('#a15c00', 0.5, 0.1) };
  const stemG = new THREE.CylinderGeometry(0.022, 0.022, 0.48, 6);
  const discG = new THREE.CylinderGeometry(0.2, 0.2, 0.05, 28);
  const innerG = new THREE.CylinderGeometry(0.115, 0.115, 0.056, 24);
  const ringG = new THREE.TorusGeometry(0.29, 0.034, 8, 40).rotateX(Math.PI / 2);
  const pins = [];
  assets.forEach((a) => {
    const sp = spotOf(a);
    for (let k = 0; k < 6 && spots.some((q) => Math.hypot(q.x - sp.x, q.y - sp.y) < 0.55); k++) sp.x += 0.6;
    spots.push(Object.assign({ kind: String(a.kind || '').toLowerCase() }, sp));
    const wu = a.warranty_until ? new Date(a.warranty_until) : null;
    const expired = !!(wu && !isNaN(wu.getTime()) && wu < today);
    const base = WP(sp.x, sp.y, sp.h);
    const stem = new THREE.Mesh(stemG, pinMat.ink); stem.position.set(base.x, base.y + 0.24, base.z);
    const disc = new THREE.Mesh(discG, pinMat.ink); disc.position.set(base.x, base.y + 0.5, base.z);
    const inner = new THREE.Mesh(innerG, pinMat.white); inner.position.copy(disc.position);
    disc.userData.assetId = inner.userData.assetId = String(a.id);
    stem.castShadow = disc.castShadow = true;
    group.add(stem, disc, inner);
    const objs = [disc, inner];
    if (expired) { const ring = new THREE.Mesh(ringG, pinMat.warn); ring.position.copy(disc.position); ring.userData.assetId = String(a.id); group.add(ring); objs.push(ring); }
    pins.push({ a, id: String(a.id), p: disc.position.clone().add(new THREE.Vector3(0, 0.05, 0)), expired, objs, kind: String(a.kind || '').toLowerCase() });
  });

  const box = new THREE.Box3(new THREE.Vector3(bb.x0 - cx, -0.3, -(bb.y1 - cy)), new THREE.Vector3(bb.x1 - cx, H, -(bb.y0 - cy)));
  const exp = box.clone();
  pins.forEach((p) => exp.expandByPoint(p.p));
  return { group, plan, generated, rooms, roomById, pins, box: exp, WP, cut: [...cut.values()] };
}

function mountApartment(el, opts = {}) {
  const S = createStage(el, opts, 'apartment');
  if (!S.ok) return Object.assign(S.stub, { highlightRoom() {}, getPlan: () => null, update() {}, _debug: () => ({ ready: false }) });
  const T = S.T, C = S.controls;
  let o = Object.assign({}, opts);
  let M = null, roomTags = [], pinTags = [], hoverRoom = null, sel = null, outlineObj = null;

  const roomHtml = (R) => `<span class="nlrm3d-pill"><span class="nlrm3d-txt">${esc(R.label)}</span><span class="nlrm3d-sub">${Math.round(R.area)} ${esc(T.sqm)}</span></span>`;
  const pinHtml = (P) => {
    const ico = ICONS[P.kind] || ICONS.other;
    const label = P.a.label || T.assets[P.kind] || P.kind || P.id;
    return `<span class="nlrm3d-pill"><span class="nlrm3d-ico"><svg viewBox="0 0 16 16" aria-hidden="true">${ico}</svg></span><span class="nlrm3d-txt">${esc(label)}</span></span>`;
  };
  function setRoomGlow(R, k) { if (R) { R.mesh.material.emissiveIntensity = k; } }
  function highlightRoom(id) {
    if (sel) setRoomGlow(sel, 0);
    if (outlineObj) { M.group.remove(outlineObj); outlineObj.geometry.dispose(); outlineObj.material.dispose(); outlineObj = null; }
    sel = id != null ? M.roomById.get(String(id)) || null : null;
    roomTags.forEach((t) => t.el.classList.toggle('is-on', !!sel && t.id === sel.id));
    if (sel) {
      setRoomGlow(sel, 0.14);
      const pts = sel.r.poly.map((q) => M.WP(q[0], q[1], (sel.kind === 'balcony' ? -0.035 : 0) + 0.03));
      pts.push(pts[0].clone());
      outlineObj = new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), new THREE.LineBasicMaterial({ color: PAL.sea }));
      M.group.add(outlineObj);
    }
    if (hoverRoom && hoverRoom !== sel) setRoomGlow(hoverRoom, 0.07);
    S.invalidate();
    return !!sel;
  }
  function pickRoom(id) { highlightRoom(id); if (typeof o.onPickRoom === 'function') o.onPickRoom(String(id)); }
  function pickAsset(id) { if (typeof o.onPickAsset === 'function') o.onPickAsset(String(id)); }

  function build() {
    const prevSel = sel ? sel.id : null;
    if (outlineObj) outlineObj = null;
    if (M) { S.scene.remove(M.group); disposeTree(M.group); }
    roomTags.forEach((t) => t.el.remove());
    pinTags.forEach((t) => t.el.remove());
    roomTags = []; pinTags = []; hoverRoom = null; sel = null;
    M = buildApartmentModel(S, o);
    S.scene.add(M.group);
    for (const R of M.rooms) {
      const t = S.makeTag('nlrm3d-room', R.id, roomHtml(R), `${R.label}, ${Math.round(R.area)} ${T.sqm}`, () => pickRoom(R.id));
      t.R = R;
      roomTags.push(t);
    }
    for (const P of M.pins) {
      const label = P.a.label || T.assets[P.kind] || P.kind || P.id;
      const open = !!(P.a && P.a.open);
      const t = S.makeTag('nlrm3d-pin' + (P.expired ? ' is-warn' : '') + (open ? ' is-open' : ''), P.id, pinHtml(P), label + (P.expired ? ', ' + T.warranty : '') + (open ? ', ' + (P.a.openText || '') : ''), () => pickAsset(P.id));
      t.P = P;
      pinTags.push(t);
    }
    S.cv.setAttribute('aria-label', T.aAria);
    S.cap.textContent = M.generated ? T.illusGen : T.illus;
    if (prevSel) highlightRoom(prevSel);
  }
  function fit() {
    const b = M.box;
    const c = b.getCenter(new THREE.Vector3());
    c.y = 0.5;
    const phi = 0.62, theta = -0.32; // about 55° above the floor, a slight three-quarter turn
    const { target, dist } = S.frame(b, phi, theta, c, 0.06, 0.11);
    S.home = { target, dist, theta };
    C.minDistance = dist * 0.42;
    C.maxDistance = dist * 2.1;
    C.minPolarAngle = 0;
    C.maxPolarAngle = 1.2;
    S.place(target, new THREE.Spherical(dist, phi, theta));
    S.placeSun(b, theta - 1.1, 1.0);
  }
  S.hooks.overlay = () => {
    const cam = S.camera.position, items = [];
    for (const t of pinTags) items.push({ tag: t, p: t.P.p, vis: true, d: cam.distanceTo(t.P.p), prio: 0, above: true });
    for (const t of roomTags) { const p = M.WP(t.R.c[0], t.R.c[1], 0.05); items.push({ tag: t, p, vis: true, d: cam.distanceTo(p), prio: 1, nudge: true }); }
    S.layout(items);
  };
  S.hooks.before = () => {
    const cam = S.camera.position;
    if (cam.y < 1.0) cam.y = 1.0;
    // cut away the outer walls that face the camera (none when looking almost straight down)
    const dx = cam.x - C.target.x, dz = cam.z - C.target.z, l = Math.hypot(dx, dz), far = cam.distanceTo(C.target) || 1;
    for (const b of M.cut) {
      const facing = l / far > 0.12 && (b.n[0] * dx + b.n[1] * dz) / l > 0.28;
      b.fullG.visible = !facing;
      b.lowG.visible = facing;
    }
  };
  S.hooks.measure = () => { roomTags.forEach((t) => t.measure()); pinTags.forEach((t) => t.measure()); };
  S.hooks.resize = () => { if (M && !S.userMoved) fit(); };
  const hitAt = (cx, cy) => {
    const objs = [];
    M.pins.forEach((p) => objs.push(...p.objs));
    M.rooms.forEach((R) => objs.push(R.mesh));
    const hits = S.raycast(cx, cy, objs);
    for (const h of hits) {
      if (h.object.userData.assetId != null) return { pin: M.pins.find((p) => p.id === h.object.userData.assetId) };
      if (h.object.userData.roomId != null) return { room: M.roomById.get(h.object.userData.roomId) };
    }
    return null;
  };
  S.hooks.hover = (cx, cy) => {
    const h = cx == null ? null : hitAt(cx, cy);
    const R = h && h.room ? h.room : null;
    if (R !== hoverRoom) {
      if (hoverRoom && hoverRoom !== sel) setRoomGlow(hoverRoom, 0);
      hoverRoom = R;
      if (R && R !== sel) setRoomGlow(R, 0.07);
      S.invalidate();
    }
    S.cv.style.cursor = h ? 'pointer' : '';
    if (!h) { S.tip(null); return; }
    if (h.pin) { const P = h.pin; S.tip(`<b>${esc(P.a.label || T.assets[P.kind] || P.kind)}</b>${P.expired ? `<span>${esc(T.warranty)}</span>` : ''}`, cx, cy); }
    else S.tip(`<b>${esc(R.label)}</b><span>${Math.round(R.area)} ${esc(T.sqm)}</span>`, cx, cy);
  };
  S.hooks.pick = (cx, cy) => {
    const h = hitAt(cx, cy);
    if (!h) return;
    if (h.pin) pickAsset(h.pin.id);
    else if (h.room) pickRoom(h.room.id);
  };

  build();
  fit();

  const handle = {
    getPlan() { return JSON.parse(JSON.stringify(M.plan)); },
    highlightRoom(id) { return highlightRoom(id); },
    update(next = {}) { o = Object.assign({}, o, next); build(); if (!S.userMoved) fit(); S.invalidate(); },
    dispose() { S.dispose(); },
    _debug() {
      return Object.assign(S.debug(), {
        generated: M.generated, rooms: M.rooms.length, pins: M.pins.length,
        area: Math.round(M.rooms.filter((R) => R.kind !== 'balcony').reduce((s, R) => s + R.area, 0) * 10) / 10,
        labelsShown: roomTags.filter((t) => !t.off).length, pinsShown: pinTags.filter((t) => !t.off).length,
      });
    },
  };
  S.mark(handle);
  return handle;
}

/* ------------------------------------------------------------------ register */
window.NLRM3D = Object.freeze({ mountBuilding, mountApartment, version: VERSION });
window.dispatchEvent(new Event('nlrm3d:ready'));
