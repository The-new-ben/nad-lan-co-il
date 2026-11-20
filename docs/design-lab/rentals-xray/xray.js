// DESIGN-LAB render harness for the rentals board 1b ("the home as an object", x-ray variant). Never deployed, not product code.
// It mounts the designer's own 3D view (a lab copy of space.js that only adds one export) and adds, in this file only:
//   service runs (cold #1565c0, hot #c62828 dashed, gas #f5b800, electricity #6a3fc8), an x-ray mode, eleven white parts, a camera API.
// Plan: example-4r (kitchen, WC, bath, laundry/service room "שירות", safe room "ממ״ד"). Units: plan centimetres, X right, Y down the sheet, Z up.
import * as THREE from 'three';
import { createStore, emptyDesign } from '../../../plugins/nadlan-config/assets/designer/core.js';
import * as cat from '../../../plugins/nadlan-config/assets/designer/catalog.js';
import { mountSpace } from './space.lab.js';

const D = '../../../plugins/nadlan-config/assets/designer/';
const PLAN_FILE = 'plans/example-4r.json';
const q = new URLSearchParams(location.search);
const M = 0.01;
const BG = '#eef2f6';
const INK = 0x0f2233;
const FOV = 20;
const COL = { c: 0x1565c0, h: 0xc62828, g: 0xf5b800, e: 0x6a3fc8 };
const V = (x, y, z) => new THREE.Vector3(x * M, z * M, y * M); // plan (x, y) + height -> three.js (X, Y up, Z)

const apt = await (await fetch(D + PLAN_FILE)).json();
const d0 = emptyDesign(apt); d0.items = cat.STARTER.filter((i) => cat.ITEMS[i.sku]).map((i) => ({ ...i }));
const store = createStore(apt, d0);
const stageEl = document.getElementById('stage');
const space = mountSpace(stageEl, store, cat, { rise: false });
const L = space.lab, { scene, camera, renderer, controls, mat, gWall, gGlass, gItem, gPoint, gFloor, ground, touch } = L;

// ---- timing: first rendered 3D frame (ms from navigation start) ----
const T = { firstRender: null, firstPresented: null, env: null };
{
  const r0 = renderer.render.bind(renderer);
  renderer.render = (s, c) => { r0(s, c); if (T.firstRender == null) { T.firstRender = performance.now(); requestAnimationFrame(() => { T.firstPresented = performance.now(); }); } if (T.env == null && scene.environment) T.env = performance.now(); };
}

// ---- scene setup: the lab look (light, no sky) ----
scene.background = new THREE.Color(BG);
camera.fov = FOV; camera.near = 0.5; camera.far = 200; camera.updateProjectionMatrix();
controls.minDistance = 1; controls.maxDistance = 80; controls.maxPolarAngle = 1.5; controls.enableDamping = false;
scene.fog = null;

// =====================================================================================================================
// small geometry kit
// =====================================================================================================================
const WHITE = () => new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.55, metalness: 0, envMapIntensity: 0.45 });
function merge(geos) { // tiny mergeGeometries for position+normal(+index) so the page needs no extra module
  let nv = 0, ni = 0; const parts = geos.map((g) => (g.index ? g : g.toNonIndexed()));
  for (const g of parts) { nv += g.attributes.position.count; ni += g.index ? g.index.count : g.attributes.position.count; }
  const pos = new Float32Array(nv * 3), nor = new Float32Array(nv * 3), idx = new Uint32Array(ni); let vo = 0, io = 0;
  for (const g of parts) {
    const n = g.attributes.position.count; pos.set(g.attributes.position.array, vo * 3); nor.set(g.attributes.normal.array, vo * 3);
    if (g.index) for (let i = 0; i < g.index.count; i++) idx[io++] = g.index.array[i] + vo; else for (let i = 0; i < n; i++) idx[io++] = vo + i;
    vo += n;
  }
  const out = new THREE.BufferGeometry(); out.setAttribute('position', new THREE.BufferAttribute(pos, 3)); out.setAttribute('normal', new THREE.BufferAttribute(nor, 3)); out.setIndex(new THREE.BufferAttribute(idx, 1));
  return out;
}

/** a path of plan points [x,y,z] (cm), right angles only, with rounded elbows, sampled as a dense 3D polyline */
function filleted(pts, f = 9, step = 5) {
  const P = pts.map((p) => new THREE.Vector3(p[0], p[1], p[2])); const out = [P[0].clone()];
  for (let i = 1; i < P.length - 1; i++) {
    const a = P[i - 1], b = P[i], c = P[i + 1], d1 = b.clone().sub(a), d2 = c.clone().sub(b), l1 = d1.length(), l2 = d2.length(); d1.normalize(); d2.normalize();
    if (d1.distanceTo(d2) < 1e-6) { out.push(b.clone()); continue; }
    const r = Math.min(f, l1 / 2, l2 / 2), p0 = b.clone().addScaledVector(d1, -r), p1 = b.clone().addScaledVector(d2, r);
    for (let k = 0; k <= 6; k++) { const t = k / 6; out.push(new THREE.Vector3().addScaledVector(p0, (1 - t) * (1 - t)).addScaledVector(b, 2 * t * (1 - t)).addScaledVector(p1, t * t)); }
  }
  out.push(P[P.length - 1].clone());
  // resample: dense along straights so the tube stays straight, kept at the elbow points
  const dense = [out[0]];
  for (let i = 1; i < out.length; i++) { const a = out[i - 1], b = out[i], l = a.distanceTo(b), n = Math.max(1, Math.round(l / step)); for (let k = 1; k <= n; k++) dense.push(a.clone().lerp(b, k / n)); }
  return dense;
}
class Poly extends THREE.Curve {
  constructor(pts) { super(); this.pts = pts.map((p) => new THREE.Vector3(p.x * M, p.z * M, p.y * M)); this.cum = [0]; for (let i = 1; i < this.pts.length; i++) this.cum.push(this.cum[i - 1] + this.pts[i].distanceTo(this.pts[i - 1])); this.len = this.cum[this.cum.length - 1]; }
  getPoint(t, o = new THREE.Vector3()) { const s = t * this.len; let i = 1; while (i < this.cum.length - 1 && this.cum[i] < s) i++; const k = (s - this.cum[i - 1]) / Math.max(1e-9, this.cum[i] - this.cum[i - 1]); return o.copy(this.pts[i - 1]).lerp(this.pts[i], Math.min(1, Math.max(0, k))); }
  getLength() { return this.len; }
  getPointAt(u, o) { return this.getPoint(u, o); }
  getTangentAt(u, o = new THREE.Vector3()) { const e = 2e-4, a = this.getPoint(Math.max(0, u - e)), b = this.getPoint(Math.min(1, u + e)); return o.copy(b).sub(a).normalize(); }
}
const tubeGeo = (pts, r, radial = 12) => { const c = new Poly(pts); return new THREE.TubeGeometry(c, Math.max(2, pts.length - 1), r * M, radial, false); };
const ball = (p, r) => { const g = new THREE.SphereGeometry(r * M, 16, 12); g.translate(p.x * M, p.z * M, p.y * M); return g; };
function slicePoly(dense, s0, s1) { // the part of a dense polyline between two arc lengths
  const out = []; let s = 0;
  for (let i = 1; i < dense.length; i++) {
    const a = dense[i - 1], b = dense[i], l = a.distanceTo(b), e = s + l;
    if (e >= s0 && s <= s1) { if (!out.length) out.push(a.clone().lerp(b, Math.max(0, (s0 - s) / l))); const k = Math.min(1, (s1 - s) / l); if (k < 1) { out.push(a.clone().lerp(b, k)); break; } out.push(b.clone()); }
    s = e;
  }
  return out.length >= 2 ? out : null;
}

// =====================================================================================================================
// the eleven parts: white maquette models with thin dark edges
// =====================================================================================================================
const partsRoot = new THREE.Group(); scene.add(partsRoot);
const edgeMat = () => new THREE.LineBasicMaterial({ color: INK, transparent: true, opacity: 1, toneMapped: false });
function newPart(id) {
  const g = new THREE.Group(); g.userData.partId = id; partsRoot.add(g);
  const P = { id, g, mat: WHITE(), edge: edgeMat(), glass: new THREE.MeshStandardMaterial({ color: 0xd6e6f2, roughness: 0.1, transparent: true, opacity: 0.2, depthWrite: false }), meshes: [] };
  const add = (geo, x, y, z, o = {}) => { // x, y = plan centre, z = centre height (cm)
    const m = new THREE.Mesh(geo, o.glass ? P.glass : P.mat); m.position.set(x * M, z * M, y * M); if (o.ry) m.rotation.y = o.ry; if (o.rz) m.rotation.z = o.rz; if (o.sx) m.scale.x = o.sx; if (o.sz) m.scale.z = o.sz;
    m.castShadow = !o.glass; m.receiveShadow = true; g.add(m); P.meshes.push(m);
    if (!o.noedge) { const e = new THREE.LineSegments(new THREE.EdgesGeometry(geo, 25), P.edge); e.position.copy(m.position); e.rotation.copy(m.rotation); e.scale.copy(m.scale); g.add(e); }
    return m;
  };
  // w along X, d along Y (plan), h up; (x, y) the plan centre, z0 the bottom
  P.box = (w, d, h, x, y, z0, o) => add(new THREE.BoxGeometry(w * M, h * M, d * M), x, y, z0 + h / 2, o);
  P.cylZ = (r, h, x, y, z0, o) => add(new THREE.CylinderGeometry(r * M, r * M, h * M, 28), x, y, z0 + h / 2, o); // vertical
  P.cylX = (r, len, x, y, zc, o) => add(new THREE.CylinderGeometry(r * M, r * M, len * M, 32), x, y, zc, { ...o, rz: Math.PI / 2 }); // along X
  return P;
}
const PARTS = {};
function def(id, o) { PARTS[id] = { id, ...o }; return PARTS[id]; }

// 1. living-room AC (wall unit on the north facade, lowered to 91-119 cm so it shows under the 118 cm cut)
{ const P = newPart('acLiving'); const x = 555, y = 23.5;
  P.box(80, 22, 28, x, y, 91); P.box(76, 4, 6, x, y + 12, 88); for (const k of [-24, -8, 8, 24]) P.box(1.2, 1, 22, x + k, y + 11.4, 94, { noedge: true });
  P.box(10, 1, 2.5, x + 28, y + 11.2, 110);
  def('acLiving', { P, anchor: [555, 23, 105], roomPt: [555, 80], sys: { e: 1, ac: 1 }, view: { az: 28, el: 34, d: 8 } }); }
// 2. living-room shutter at the big window: housing, side guides, half-lowered slats
{ const P = newPart('shutter'); const x = 310, y = 0;
  P.box(364, 22, 24, x, y, 234); P.box(4, 8, 234, 128, y, 0); P.box(4, 8, 234, 492, y, 0);
  for (let k = 0; k < 16; k++) P.box(356, 2.4, 6.6, x, y - 3, 226 - k * 8);
  P.box(358, 3.5, 5, x, y - 3, 226 - 16 * 8);
  def('shutter', { P, anchor: [310, 0, 200], roomPt: [310, 80], sys: { e: 1 }, view: { az: 20, el: 34, d: 11 } }); }
// 3. cooktop and oven in the kitchen counter (south wall of the kitchen)
{ const P = newPart('cooktop'); const x = 120, y = 857;
  P.box(60, 52, 3, x, y, 90);
  for (const [dx, dy, r] of [[-14, -12, 8], [14, -12, 6], [-14, 12, 6], [14, 12, 8]]) P.cylZ(r, 1.6, x + dx, y + dy, 93);
  for (const k of [-21, -7, 7, 21]) P.cylZ(2.2, 3.2, x + k, y - 26, 90.5);
  P.box(58, 3, 50, x, 826, 34); P.box(50, 2.4, 2.6, x, 823.4, 76); P.box(42, 1, 28, x, 824.4, 40, { noedge: false });
  def('cooktop', { P, anchor: [120, 850, 94], roomPt: [200, 740], sys: { e: 1, g: 1 }, view: { az: 150, el: 36, d: 7 } }); }
// 4. fridge, north-east corner of the kitchen, back to the wall between kitchen and hall
{ const P = newPart('fridge'); const x = 318, y = 560;
  P.box(70, 66, 118, x, y, 0); P.box(70, 66, 60, x, y, 120); P.box(70, 3, 118, x, y + 34.5, 0); P.box(70, 3, 60, x, y + 34.5, 120);
  P.box(2.6, 4, 40, x - 28, y + 38, 70); P.box(2.6, 4, 22, x - 28, y + 38, 140);
  def('fridge', { P, anchor: [318, 560, 100], roomPt: [250, 580], sys: { e: 1 }, view: { az: 30, el: 30, d: 8 } }); }
// 5. kitchen sink with the main tap
{ const P = newPart('sink'); const x = 270, y = 857;
  P.box(82, 46, 2, x, y, 90); P.box(64, 34, 1.6, x, y + 1, 91.4); P.box(26, 30, 1.6, x + 18, y + 1, 92.6, { noedge: false });
  P.cylZ(2.4, 24, x, 880, 92); P.cylX(1.7, 22, x, 872, 116); P.box(2, 2, 9, x + 6, 880, 116); P.cylZ(3.4, 2, x, 880, 92);
  def('sink', { P, anchor: [270, 868, 100], roomPt: [200, 740], sys: { w: 1 }, view: { az: 150, el: 36, d: 7 } }); }
// 6. electrical panel by the entrance door (hall side of the wall next to the service room)
{ const P = newPart('panel'); const x = 601, y = 860;
  P.box(12, 34, 42, x, y, 139); P.box(1.6, 29, 37, x - 6.6, y, 141.5);
  for (let r = 0; r < 2; r++) for (let c = 0; c < 4; c++) P.box(1.2, 4, 7, x - 7.6, y - 10.5 + c * 7, 146 + r * 14);
  def('panel', { P, anchor: [601, 860, 160], roomPt: [540, 840], sys: { e: 1 }, view: { az: -35, el: 28, d: 6.5 } }); }
// 7. bedroom AC (master, north facade)
{ const P = newPart('acBed'); const x = 920, y = 23.5;
  P.box(80, 22, 28, x, y, 91); P.box(76, 4, 6, x, y + 12, 88); for (const k of [-24, -8, 8, 24]) P.box(1.2, 1, 22, x + k, y + 11.4, 94, { noedge: true });
  P.box(10, 1, 2.5, x + 28, y + 11.2, 110);
  def('acBed', { P, anchor: [920, 23, 105], roomPt: [920, 120], sys: { e: 1, ac: 1 }, view: { az: 28, el: 34, d: 8 } }); }
// 8. safe room (ממ״ד): steel door in the corridor wall and the steel window shutter on the east wall
{ const P = newPart('mamad');
  P.box(80, 12, 205, 1080, 500, 0); P.box(7, 18, 205, 1036.5, 500, 0); P.box(7, 18, 205, 1123.5, 500, 0); P.box(94, 18, 8, 1080, 500, 205);
  P.box(4, 14, 56, 1100, 508, 96); for (const z of [30, 90, 150, 190]) P.cylX(3, 6, 1121, 500, z, { noedge: false });
  P.box(10, 106, 106, 1320, 700, 100); P.box(6, 74, 74, 1314, 700, 116); for (const [a, b] of [[-46, -46], [46, -46], [-46, 46], [46, 46]]) P.cylX(3, 4, 1314, 700 + a, 146 + b, { noedge: false });
  def('mamad', { P, anchor: [1190, 580, 100], roomPt: [1160, 700], sys: {}, view: { az: -45, el: 34, d: 13 } }); }
// 9. shower and toilet (the "רחצה" room, against the wall shared with the service room)
{ const P = newPart('bath');
  P.box(90, 90, 6, 878, 850, 0); P.box(1.4, 90, 195, 923, 850, 0, { glass: true }); P.box(90, 1.4, 195, 878, 805, 0, { glass: true });
  P.box(2, 2, 195, 923, 805, 0); P.cylZ(1.5, 96, 837, 863, 104); P.box(22, 2.2, 2.2, 848, 863, 198); P.cylZ(11, 2, 863, 863, 197);
  P.box(6, 62, 5, 835, 865, 101.5);
  P.box(18, 38, 60, 842, 775, 20); P.cylZ(19, 40, 872, 775, 0, { sx: 1.5 }); P.cylZ(18, 3, 872, 775, 40, { sx: 1.5 }); P.cylZ(3, 2, 842, 775, 80);
  def('bath', { P, anchor: [875, 810, 40], roomPt: [900, 760], sys: { w: 1 }, view: { az: 140, el: 40, d: 10.5 } }); }
// 10. solar water heater tank on a small frame in the service room
{ const P = newPart('boiler'); const x = 720, y = 862;
  P.cylX(24, 120, x, y, 116); P.cylX(24.8, 3, x - 28, y, 116); P.cylX(24.8, 3, x + 28, y, 116);
  for (const lx of [675, 765]) { for (const ly of [842, 882]) P.box(5, 5, 88, lx, ly, 0); P.box(5, 46, 4, lx, y, 88); }
  P.box(60, 4, 4, x, 842, 4);
  def('boiler', { P, anchor: [720, 862, 116], roomPt: [720, 800], sys: { w: 1, e: 1 }, view: { az: 155, el: 34, d: 8.5 } }); }
// 11. washing machine in the service room, back to the wall shared with the bathroom
{ const P = newPart('washer'); const x = 780, y = 722;
  P.box(60, 60, 85, x, y, 0); P.cylX(20, 2.6, x - 30.8, y, 40, { noedge: false }); P.cylX(14, 2.6, x - 31.4, y, 40, { noedge: false }); P.box(1.2, 52, 10, x - 30.6, y, 72); P.cylX(2.6, 2.4, x - 31, y + 20, 77);
  def('washer', { P, anchor: [780, 722, 45], roomPt: [720, 800], sys: { w: 1, e: 1 }, view: { az: -70, el: 36, d: 8 } }); }

// =====================================================================================================================
// service runs (all axis-aligned; installers run along walls, never diagonally)
// Round 2: thin cores (2.2 cm), hot dashed 6 cm beside cold, electricity INSIDE the walls at 90 cm (just under the window sills
// and the 118 cm cut), dipping into the floor slab where a door or an opening interrupts the wall.
// =====================================================================================================================
const RUNS = [
  // cold water (z 28), source in the service room (south-east corner); hot runs 6 cm beside it
  { id: 'c-boiler', sys: 'c', serves: ['boiler'], pts: [[812, 888, 28], [670, 888, 28], [670, 888, 92], [670, 862, 92]] },
  { id: 'c-washer', sys: 'c', serves: ['washer'], pts: [[812, 888, 28], [812, 722, 28], [812, 722, 70]] },
  { id: 'c-toilet', sys: 'c', serves: ['bath'], pts: [[812, 775, 28], [834, 775, 28]] },
  { id: 'c-shower', sys: 'c', serves: ['bath'], pts: [[812, 888, 28], [812, 888, 104], [836, 888, 104]] },
  { id: 'c-sink', sys: 'c', serves: ['sink'], pts: [[812, 888, 28], [548, 888, 28], [548, 888, 8], [432, 888, 8], [432, 888, 28], [286, 888, 28], [286, 888, 92], [286, 880, 92], [273, 880, 92]] },
  { id: 'h-sink', sys: 'h', serves: ['sink'], pts: [[780, 862, 116], [818, 862, 116], [818, 862, 28], [818, 894, 28], [548, 894, 28], [548, 894, 8], [432, 894, 8], [432, 894, 28], [254, 894, 28], [254, 894, 92], [254, 880, 92], [267, 880, 92]] },
  { id: 'h-shower', sys: 'h', serves: ['bath'], pts: [[818, 862, 28], [818, 842, 28], [818, 842, 104], [836, 842, 104]] },
  // gas (z 60), from the west facade to the hob
  { id: 'g-hob', sys: 'g', serves: ['cooktop'], pts: [[-18, 900, 60], [120, 900, 60], [120, 860, 60], [120, 860, 90]] },
  // electricity (z 90) from the panel, in the wall lines; the dips cross the laundry door (x=620), the open gap of the corridor, the entry door
  { id: 'e-trunk', sys: 'e', serves: ['acLiving', 'shutter', 'acBed'], pts: [[601, 860, 139], [601, 860, 90], [620, 860, 90], [620, 830, 90], [620, 830, 8], [620, 730, 8], [620, 730, 90], [620, 500, 90], [620, 500, 8], [620, 380, 8], [620, 380, 90], [620, 0, 90]] },
  { id: 'e-north-w', sys: 'e', serves: ['acLiving', 'shutter'], pts: [[620, 0, 90], [555, 0, 90]] },
  { id: 'e-acl', sys: 'e', serves: ['acLiving'], pts: [[555, 0, 90], [555, 0, 105], [555, 14, 105]] },
  { id: 'e-shutter', sys: 'e', serves: ['shutter'], pts: [[555, 0, 90], [494, 0, 90], [494, 0, 245], [486, 0, 245]] },
  { id: 'e-acb', sys: 'e', serves: ['acBed'], pts: [[620, 0, 90], [920, 0, 90], [920, 0, 105], [920, 14, 105]] },
  { id: 'e-kitchen', sys: 'e', serves: ['cooktop', 'fridge'], pts: [[620, 860, 90], [620, 900, 90], [560, 900, 90], [560, 900, 8], [420, 900, 8], [420, 900, 90], [120, 900, 90], [120, 880, 90]] },
  { id: 'e-fridge', sys: 'e', serves: ['fridge'], pts: [[360, 900, 90], [360, 560, 90], [360, 560, 100], [352, 560, 100]] },
  { id: 'e-laundry', sys: 'e', serves: ['boiler', 'washer'], pts: [[620, 900, 90], [826, 900, 90], [826, 745, 90], [826, 745, 60], [811, 745, 60]] },
  { id: 'e-boiler', sys: 'e', serves: ['boiler'], pts: [[730, 900, 90], [730, 900, 118], [730, 884, 118]] },
];
// ---- the fade-outside-the-room shader (used by walls, caps, floors, ghost furniture and the runs) and the live tube radius ----
const FOCUS = { on: { value: 0 }, box: { value: new THREE.Vector4(0, 0, 0, 0) }, boxRun: { value: new THREE.Vector4(0, 0, 0, 0) }, fade: { value: 0.06 } };
const UR = { core: { value: 0 }, halo: { value: 0 } }; // metres added along the tube normal: the radius follows the camera distance
const RB = { core: 0.022, halo: 0.066 };               // radii the geometry is baked at
function fadeShader(sh, run, dr) {
  sh.uniforms.uOn = FOCUS.on; sh.uniforms.uFade = FOCUS.fade; sh.uniforms.uBox = run ? FOCUS.boxRun : FOCUS.box; if (dr) sh.uniforms.uDR = dr;
  sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\nvarying vec3 vWp;' + (dr ? '\nuniform float uDR;' : ''))
    .replace('#include <begin_vertex>', '#include <begin_vertex>' + (dr ? '\ntransformed += normal * uDR;' : '') + '\nvWp = (modelMatrix * vec4(transformed, 1.0)).xyz;');
  sh.fragmentShader = sh.fragmentShader.replace('#include <common>', '#include <common>\nvarying vec3 vWp;\nuniform float uOn;\nuniform float uFade;\nuniform vec4 uBox;')
    .replace('#include <dithering_fragment>', '#include <dithering_fragment>\n{ float ins = step(uBox.x, vWp.x) * step(vWp.x, uBox.z) * step(uBox.y, vWp.z) * step(vWp.z, uBox.w); gl_FragColor.a = mix(gl_FragColor.a, min(gl_FragColor.a, uFade), uOn * (1.0 - ins)); }');
}
const runsRoot = new THREE.Group(); scene.add(runsRoot);
for (const r of RUNS) {
  const dense = filleted(r.pts, 6), curve = new Poly(dense), col = COL[r.sys];
  r.coreMat = new THREE.MeshBasicMaterial({ color: col, transparent: true, depthTest: false, depthWrite: false, toneMapped: false }); r.coreMat.onBeforeCompile = (sh) => fadeShader(sh, true, UR.core);
  r.haloMat = new THREE.MeshBasicMaterial({ color: col, transparent: true, opacity: 0.14, depthTest: false, depthWrite: false, toneMapped: false }); r.haloMat.onBeforeCompile = (sh) => fadeShader(sh, true, UR.halo);
  const geos = [], rc = RB.core / M; // cm
  if (r.sys === 'h') { // hot: dashes 12 cm long (end to end, caps included) with 8 cm gaps
    const total = curve.getLength() / M;
    for (let s = 0; s + 12 <= total + 0.01; s += 20) { const sub = slicePoly(dense, s + rc, s + 12 - rc); if (!sub) continue; geos.push(tubeGeo(sub, rc, 8), ball(sub[0], rc), ball(sub[sub.length - 1], rc)); }
  } else geos.push(tubeGeo(dense, rc, 8), ball(dense[0], rc), ball(dense[dense.length - 1], rc));
  const core = new THREE.Mesh(merge(geos), r.coreMat); core.renderOrder = 30;
  const halo = new THREE.Mesh(tubeGeo(dense, RB.halo / M, 12), r.haloMat); halo.renderOrder = 25;
  const g = new THREE.Group(); g.add(halo, core); g.userData.run = r; r.g = g; r.len = Math.round(curve.getLength() / M); runsRoot.add(g);
}

// ---- ink caps: the cut tops of the walls, ours in both modes (full ink in normal, 35% in x-ray); movable-wall blue becomes grey ----
let capMesh = null;
{
  const src = gWall.children[0], g0 = src.geometry, nor = g0.attributes.normal.array, I = g0.index.array, keep = [];
  for (let i = 0; i < I.length; i += 3) { if (nor[I[i] * 3 + 1] > 0.9) keep.push(I[i], I[i + 1], I[i + 2]); }
  const col0 = g0.attributes.color, colA = new Float32Array(col0.array);
  for (let i = 0; i < colA.length; i += 3) if (Math.abs(colA[i] - 0.0137) < 0.02 && Math.abs(colA[i + 1] - 0.114) < 0.03 && Math.abs(colA[i + 2] - 0.386) < 0.05) { colA[i] = 0.24; colA[i + 1] = 0.27; colA[i + 2] = 0.31; }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', g0.attributes.position); g.setAttribute('color', new THREE.BufferAttribute(colA, 3)); g.setIndex(keep);
  const cm = new THREE.MeshBasicMaterial({ vertexColors: true, toneMapped: false }); cm.onBeforeCompile = (sh) => fadeShader(sh, false, null);
  capMesh = new THREE.Mesh(g, cm); capMesh.position.y = 0.004; capMesh.renderOrder = 3; scene.add(capMesh);
  const wm = mat.wall, prev = wm.onBeforeCompile; wm.onBeforeCompile = (sh) => { prev(sh); fadeShader(sh, false, null); }; wm.needsUpdate = true;
}

// ---- the white architectural model: furniture in white and cool greys, a white floor with a faint 60 cm drafting grid ----
{
  const map = { 0x55697a: 0xcfd8e0, 0x8a9ca8: 0xe6ebf0, 0xa67c52: 0xffffff, 0xf1f2f0: 0xffffff, 0x222d36: 0xcfd8e0, 0xe3e6e8: 0xffffff, 0xaeb9c1: 0xe6ebf0, 0x3f6e4c: 0xe6ebf0, 0xdadddb: 0xffffff }, seen = new Set();
  const lineMat = new THREE.LineBasicMaterial({ color: 0x8396a8, transparent: true, opacity: 0.6, toneMapped: false });
  gItem.traverse((o) => {
    if (!o.isMesh) return;
    const m = o.material; if (!seen.has(m)) { seen.add(m); const k = map[m.color.getHex()]; if (k != null) { m.color.setHex(k); m.roughness = 0.8; m.metalness = 0; } }
    const e = new THREE.LineSegments(new THREE.EdgesGeometry(o.geometry, 28), lineMat); e.userData.furnEdge = true; o.add(e);
  });
}
const gridTex = (() => { const c = document.createElement('canvas'); c.width = c.height = 256; const x = c.getContext('2d'); x.fillStyle = '#ffffff'; x.fillRect(0, 0, 256, 256); x.strokeStyle = '#e9eef3'; x.lineWidth = 4; x.strokeRect(0, 0, 256, 256);
  const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(1 / 0.6, 1 / 0.6); t.anisotropy = 8; t.colorSpace = THREE.SRGBColorSpace; return t; })();
const floorWhite = new THREE.MeshStandardMaterial({ map: gridTex, color: 0xffffff, emissive: 0xffffff, emissiveIntensity: 0.32, roughness: 0.9, envMapIntensity: 0.3, side: THREE.DoubleSide });
const deckMat = new THREE.MeshStandardMaterial({ map: gridTex, color: 0xd3dbe2, emissive: 0xc9d2da, emissiveIntensity: 0.3, roughness: 0.9, envMapIntensity: 0.3, side: THREE.DoubleSide });
for (const m of [floorWhite, deckMat]) m.onBeforeCompile = (sh) => fadeShader(sh, false, null);
gFloor.children.forEach((f) => { f.material = store.floorOf(f.userData.room) === 'deck' ? deckMat : floorWhite; f.renderOrder = -2; });

// the boiler is the part in trouble: red edges and a flat red disc on the floor (x-ray only)
const RED = 0xa11616, TEAL = 0x2f6f86;
const boilerDisc = new THREE.Mesh(new THREE.CircleGeometry(0.45, 56), new THREE.MeshBasicMaterial({ color: RED, transparent: true, opacity: 0.28, depthWrite: false, toneMapped: false }));
boilerDisc.rotation.x = -Math.PI / 2; boilerDisc.position.set(720 * M, 0.006, 862 * M); boilerDisc.renderOrder = -1; scene.add(boilerDisc);

// =====================================================================================================================
// modes, layers, fade
// =====================================================================================================================
const AC = ['acLiving', 'acBed'];
const S = { mode: 'normal', layer: 'all', layerK: 1, focus: null };
const ghostMat = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 1, metalness: 0, transparent: true, opacity: 0.10, depthWrite: false, envMapIntensity: 0.1 }); ghostMat.onBeforeCompile = (sh) => fadeShader(sh, false, null);
let focusBox = null, focusRun = null; // the room of the last focused part (plan cm) and the same box widened by 60 cm for the runs
const clamp01 = (v) => Math.max(0, Math.min(1, v));
const lerp = (a, b, t) => a + (b - a) * t;

function applyMode() {
  const x = S.mode === 'xray';
  mat.wall.color.set(x ? 0xdfe7ee : 0xffffff); mat.wall.transparent = x; mat.wall.opacity = x ? 0.16 : 1; mat.wall.depthWrite = !x; mat.wall.needsUpdate = true;
  capMesh.material.transparent = x; capMesh.material.opacity = x ? 0.35 : 1; capMesh.material.depthWrite = !x; capMesh.material.needsUpdate = true;
  runsRoot.visible = x; boilerDisc.visible = x;
  gItem.traverse((o) => {
    if (o.userData.furnEdge) { o.visible = !x; return; }
    if (!o.isMesh) return;
    if (!o.userData.orig) o.userData.orig = o.material; o.material = x ? ghostMat : o.userData.orig;
    if (o.userData.cs === undefined) o.userData.cs = o.castShadow; o.castShadow = x ? false : o.userData.cs;
  });
  applyLayer();
}
function onLayer(r) {
  if (S.layer === 'all') return true;
  if (S.layer === 'w') return r.sys === 'c' || r.sys === 'h';
  if (S.layer === 'e') return r.sys === 'e';
  if (S.layer === 'g') return r.sys === 'g';
  if (S.layer === 'ac') return r.sys === 'e' && r.serves.some((s) => AC.includes(s));
  return true;
}
function partOn(p) { if (S.layer === 'all') return true; if (S.layer === 'ac') return AC.includes(p.id); return !!p.sys[S.layer]; }
const inBox = (b, x, y, m = 0) => b && x >= b[0] - m && x <= b[2] + m && y >= b[1] - m && y <= b[3] + m;
function refreshParts() {
  const x = S.mode === 'xray', on = FOCUS.on.value;
  for (const id in PARTS) {
    const p = PARTS[id], P = p.P; let a = 1;
    if (x && S.layer !== 'all' && !partOn(p)) a = 1 - (0.6 + 0.14 * on) * S.layerK;
    if (x && on > 0 && focusBox && !inBox(focusBox, p.anchor[0], p.anchor[1], 20)) a = Math.min(a, lerp(1, 0.06, on));
    P.mat.transparent = a < 0.999; P.mat.opacity = a; P.mat.depthWrite = a > 0.999; P.mat.needsUpdate = true; P.edge.opacity = a;
    const hot = x && (id === 'boiler' || S.focus === id), c = id === 'boiler' && x ? RED : S.focus === id && x ? TEAL : INK; P.edge.color.setHex(c); void hot;
    if (p.halo) p.halo.visible = x && S.layer === 'ac' && partOn(p) && a > 0.5;
  }
}
function applyLayer() {
  const x = S.mode === 'xray', k = S.layer === 'all' ? 0 : S.layerK;
  for (const r of RUNS) { const f = onLayer(r) ? 1 : 1 - k; r.coreMat.opacity = f; r.haloMat.opacity = 0.14 * f; r.g.visible = x && f > 0.003; }
  refreshParts(); touch(true);
}
// accent halos for the highlighted AC units
for (const id of AC) { const p = PARTS[id], b = new THREE.Box3().setFromObject(p.P.g), s = new THREE.Vector3(); b.getSize(s); const c = b.getCenter(new THREE.Vector3());
  const h = new THREE.Mesh(new THREE.BoxGeometry(s.x + 0.2, s.y + 0.2, s.z + 0.2), new THREE.MeshBasicMaterial({ color: COL.e, transparent: true, opacity: 0.16, depthTest: false, depthWrite: false, toneMapped: false })); h.position.copy(c); h.renderOrder = 24; h.visible = false; scene.add(h); p.halo = h; }

// =====================================================================================================================
// camera: overview pose (portrait: the long axis runs up the screen) and focus poses (the part's whole room in view)
// =====================================================================================================================
const mid = L.mid.clone();
const FOV_F = 46; // the focus views use a wider lens so a whole room fits at 3 to 6 m
const bbox = [[-22, -228, 0], [1338, 916, 215]];
const corners = []; for (const x of [0, 1]) for (const y of [0, 1]) for (const z of [0, 1]) corners.push(V(bbox[x][0], bbox[y][1], bbox[z][2]));
function dirOf(az, el) { const a = (az * Math.PI) / 180, e = (el * Math.PI) / 180; return new THREE.Vector3(Math.sin(a) * Math.cos(e), Math.sin(e), Math.cos(a) * Math.cos(e)); }
function aspect() { return stageEl.clientWidth / stageEl.clientHeight; }
function ndcBounds(cam, pts) { let a = 9, b = -9, c = 9, d = -9; for (const p of pts) { const n = p.clone().project(cam); a = Math.min(a, n.x); b = Math.max(b, n.x); c = Math.min(c, n.y); d = Math.max(d, n.y); } return [a, b, c, d]; }
function fitOverview(az, el, margin = 0.037) {
  const cam = new THREE.PerspectiveCamera(FOV, aspect(), 0.5, 200), dir = dirOf(az, el);
  let tgt = new THREE.Vector3(mid.x, 1.0, mid.z), dist = 22;
  for (let it = 0; it < 16; it++) {
    cam.position.copy(tgt).addScaledVector(dir, dist); cam.lookAt(tgt); cam.updateMatrixWorld(); cam.updateProjectionMatrix();
    const [a, b, c, d] = ndcBounds(cam, corners);
    const th = Math.tan((FOV * Math.PI) / 360), right = new THREE.Vector3().setFromMatrixColumn(cam.matrixWorld, 0), up = new THREE.Vector3().setFromMatrixColumn(cam.matrixWorld, 1);
    tgt.addScaledVector(right, ((a + b) / 2) * dist * th * cam.aspect).addScaledVector(up, ((c + d) / 2) * dist * th);
    dist *= Math.max((b - a) / (2 * (1 - margin)), (d - c) / (2 * (1 - margin)));
  }
  return { pos: tgt.clone().addScaledVector(dir, dist), tgt, fov: FOV, fade: 0 };
}
const OV = { az: Number(q.get('az') ?? -84), el: Number(q.get('el') ?? 60) };
let overview = fitOverview(OV.az, OV.el);
const roomOf = (p) => { const f = store.derived.faces.find((fc) => fc.id === store.roomAt(...p.roomPt)); const xs = f.poly.map((v) => v[0]), ys = f.poly.map((v) => v[1]); return [Math.min(...xs), Math.min(...ys), Math.max(...xs), Math.max(...ys)]; };
const focusCache = {};
function focusPose(id) {
  const cacheKey = id + '|' + aspect().toFixed(3); if (focusCache[cacheKey]) return focusCache[cacheKey];
  const p = PARTS[id], a = V(...p.anchor), dir = dirOf(p.view.az, 38), box = roomOf(p), rc = [];
  for (const x of [box[0], box[2]]) for (const y of [box[1], box[3]]) for (const z of [0, 130]) rc.push(V(x, y, z));
  const cam = new THREE.PerspectiveCamera(FOV_F, aspect(), 0.5, 200), th = Math.tan((FOV_F * Math.PI) / 360); let pose = null;
  for (let d = 3.2; d <= 6.0; d += 0.1) {
    const t = a.clone(); // aim so the part sits 40% from the top (ndc y +0.2), the room centred sideways
    for (let it = 0; it < 3; it++) {
      cam.position.copy(t).addScaledVector(dir, d); cam.lookAt(t); cam.updateMatrixWorld(); cam.updateProjectionMatrix();
      const right = new THREE.Vector3().setFromMatrixColumn(cam.matrixWorld, 0), up = new THREE.Vector3().setFromMatrixColumn(cam.matrixWorld, 1), an = a.clone().project(cam), [x0, x1] = ndcBounds(cam, rc);
      let sx = (x0 + x1) / 2; if (an.x - sx > 0.55) sx = an.x - 0.55; if (an.x - sx < -0.55) sx = an.x + 0.55; // the room centred, but the part never nearer the side than 22% of the width
      t.addScaledVector(up, (an.y - 0.2) * d * th).addScaledVector(right, sx * d * th * cam.aspect);
    }
    cam.position.copy(t).addScaledVector(dir, d); cam.lookAt(t); cam.updateMatrixWorld(); cam.updateProjectionMatrix();
    const [x0, x1, y0, y1] = ndcBounds(cam, rc);
    pose = { pos: cam.position.clone(), tgt: t.clone(), fov: FOV_F, fade: 1, distPart: cam.position.distanceTo(a), box };
    if (x0 > -0.96 && x1 < 0.96 && y0 > -0.97 && y1 < 0.97) break;
  }
  return (focusCache[cacheKey] = pose);
}
const posePair = (f) => (f ? focusPose(f) : overview);
function setFocusId(f) {
  S.focus = f || null;
  if (f) { const b = focusPose(f).box; focusBox = b; focusRun = [b[0] - 60, b[1] - 60, b[2] + 60, b[3] + 60]; FOCUS.box.value.set(...[b[0] - 15, b[1] - 15, b[2] + 15, b[3] + 15].map((v) => v * M)); FOCUS.boxRun.value.set(...focusRun.map((v) => v * M)); }
}
let anim = null;
const easeOut = (t) => 1 - Math.pow(1 - t, 2.2);
const lerpPose = (a, b, t) => ({ pos: a.pos.clone().lerp(b.pos, t), tgt: a.tgt.clone().lerp(b.tgt, t), fov: lerp(a.fov, b.fov, t), fade: lerp(a.fade, b.fade, t) });
function applyPose(p) {
  camera.position.copy(p.pos); controls.target.copy(p.tgt); if (camera.fov !== p.fov) { camera.fov = p.fov; camera.updateProjectionMatrix(); } camera.lookAt(p.tgt); controls.update();
  FOCUS.on.value = p.fade;
  const d = camera.position.distanceTo(controls.target), px = (2 * d * Math.tan((camera.fov * Math.PI) / 360)) / stageEl.clientHeight, rc = Math.max(0.004, Math.min(0.03, ((3 + 2 * p.fade) / 2) * px));
  UR.core.value = rc - RB.core; UR.halo.value = 3 * rc - RB.halo;
  const tr = p.fade > 0.001; for (const m of [floorWhite, deckMat]) if (m.transparent !== tr) { m.transparent = tr; m.needsUpdate = true; } // the OPAQUE shader define follows this flag, so the program must be rebuilt
  gPoint.visible = p.fade < 0.5; mat.rail.opacity = lerp(S.mode === 'xray' ? 0.22 : 0.5, 0.06, p.fade);
  refreshParts(); touch(false);
}
const snap = () => ({ pos: camera.position.clone(), tgt: controls.target.clone(), fov: camera.fov, fade: FOCUS.on.value });
function flyTo(to, ms) {
  anim = null; const from = snap();
  if (!ms) { applyPose(to); return Promise.resolve(); }
  return new Promise((res) => { anim = { from, to, t0: performance.now(), ms, res }; });
}
function loop(now) {
  requestAnimationFrame(loop);
  if (!anim) return;
  const k = Math.min(1, (now - anim.t0) / anim.ms); applyPose(lerpPose(anim.from, anim.to, easeOut(k)));
  if (k >= 1) { const r = anim.res; anim = null; r(); }
}
requestAnimationFrame(loop);
controls.addEventListener('start', () => { anim = null; });

// =====================================================================================================================
// public API
// =====================================================================================================================
function set(o = {}, ms = 700) {
  if (o.mode) S.mode = o.mode; if (o.layer) { S.layer = o.layer; S.layerK = 1; }
  if ('focus' in o) setFocusId(o.focus);
  applyMode();
  if ('focus' in o) return flyTo(posePair(S.focus), ms);
  return Promise.resolve();
}
function partsNow() {
  const W = stageEl.clientWidth, H = stageEl.clientHeight; camera.updateMatrixWorld(); camera.updateProjectionMatrix();
  return Object.values(PARTS).map((p) => { const n = V(...p.anchor).project(camera), x = ((n.x + 1) / 2) * W, y = ((1 - n.y) / 2) * H; return { id: p.id, x: Math.round(x * 10) / 10, y: Math.round(y * 10) / 10, onStage: n.z < 1 && x >= 0 && x <= W && y >= 0 && y <= H }; });
}
function rooms() {
  const out = {}; for (const id in PARTS) { const p = PARTS[id], f = store.derived.faces.find((fc) => fc.id === store.roomAt(...p.roomPt)); out[id] = f && f.room ? f.room.name_he : null; }
  return out;
}
function audit() { // closest approach between runs of different ids (cm), a tangle check; junctions of one system are expected
  const segs = []; for (const r of RUNS) for (let i = 1; i < r.pts.length; i++) segs.push({ r, a: r.pts[i - 1], b: r.pts[i] });
  const sd = (s1, s2) => { let best = 1e9; for (let i = 0; i <= 24; i++) for (let j = 0; j <= 24; j++) { const t = i / 24, u = j / 24; const p = s1.a.map((v, k) => v + (s1.b[k] - v) * t), r = s2.a.map((v, k) => v + (s2.b[k] - v) * u); best = Math.min(best, Math.hypot(p[0] - r[0], p[1] - r[1], p[2] - r[2])); } return best; };
  const bad = [];
  for (let i = 0; i < segs.length; i++) for (let j = i + 1; j < segs.length; j++) { if (segs[i].r === segs[j].r) continue; const d = sd(segs[i], segs[j]); if (d < 5 && segs[i].r.sys !== segs[j].r.sys) bad.push([segs[i].r.id, segs[j].r.id, Math.round(d * 10) / 10]); }
  const diag = []; for (const r of RUNS) for (let i = 1; i < r.pts.length; i++) { const dd = r.pts[i].map((v, k) => v - r.pts[i - 1][k]).filter((v) => v !== 0).length; if (dd !== 1) diag.push(r.id + '#' + i); }
  return { closerThan5cmOtherSystem: bad, nonAxis: diag };
}
function fill() { // how much of the stage the model covers (projected corners of the walls), in percent, plus the margins
  camera.updateMatrixWorld(); const c = []; for (const x of [0, 1320]) for (const y of [-220, 900]) for (const z of [0, 130]) c.push(V(x, y, z)); const [a, b, e, d] = ndcBounds(camera, c);
  return { widthPct: Math.round(((b - a) / 2) * 1000) / 10, heightPct: Math.round(((d - e) / 2) * 1000) / 10, marginLeftPct: Math.round(((a + 1) / 2) * 1000) / 10, marginRightPct: Math.round(((1 - b) / 2) * 1000) / 10, marginTopPct: Math.round(((1 - d) / 2) * 1000) / 10, marginBottomPct: Math.round(((e + 1) / 2) * 1000) / 10 };
}
// the film, frame by frame and deterministic: 0.6 s overview (all layers), 0.3 s other layers fade out, 0.3 s water only, 1.2 s ease-out flight to the boiler, 1.1 s hold = 3.5 s
const FILM = { hold0: 0.6, fade: 0.3, pause: 0.3, fly: 1.2, hold1: 1.1 };
function film(t) {
  S.mode = 'xray'; S.layer = 'w'; setFocusId('boiler');
  S.layerK = clamp01((t - FILM.hold0) / FILM.fade); S.layerK = S.layerK * S.layerK * (3 - 2 * S.layerK);
  applyMode();
  const k = clamp01((t - FILM.hold0 - FILM.fade - FILM.pause) / FILM.fly); applyPose(lerpPose(overview, focusPose('boiler'), easeOut(k)));
  return { layerK: S.layerK, flight: k };
}
const api = {
  set, jump: (o) => set(o, 0), parts: partsNow, rooms, audit, fill, film, filmLength: FILM.hold0 + FILM.fade + FILM.pause + FILM.fly + FILM.hold1,
  timings: () => ({ firstRenderMs: T.firstRender, firstPresentedMs: T.firstPresented, envReadyMs: T.env }),
  state: () => ({ ...S }),
  scrub(focus, t) { anim = null; setFocusId(focus); applyPose(lerpPose(overview, posePair(focus), easeOut(t))); },
  ready: () => !!scene.environment && T.firstRender != null,
  gl: () => space.gl(), spin: (ms) => space.spin(ms), stats: () => space.stats(),
  runs: () => RUNS.map((r) => ({ id: r.id, sys: r.sys, serves: r.serves, lengthCm: r.len })),
  focusInfo: (id) => { const p = focusPose(id); return { distToPartM: Math.round(p.distPart * 100) / 100, room: p.box }; },
  plan: PLAN_FILE, overviewPose: () => ({ pos: overview.pos.toArray(), tgt: overview.tgt.toArray(), ...OV }),
  refit: () => { overview = fitOverview(OV.az, OV.el); return flyTo(posePair(S.focus), 0); },
};
window.xray = api;
new ResizeObserver(() => { overview = fitOverview(OV.az, OV.el); if (!anim) applyPose(posePair(S.focus)); }).observe(stageEl);

// first state from the URL: ?mode=xray&layer=w&focus=boiler  (instant)
{
  const m = q.get('mode') || 'normal', l = q.get('layer') || 'all', f = q.get('focus');
  S.mode = m === 'xray' ? 'xray' : 'normal'; S.layer = ['all', 'w', 'e', 'g', 'ac'].includes(l) ? l : 'all'; setFocusId(f && PARTS[f] ? f : null);
  applyMode(); applyPose(posePair(S.focus));
}
window.__xrayReady = true;
