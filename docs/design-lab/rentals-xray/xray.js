// DESIGN-LAB render harness for the rentals board 1b ("the home as an object", x-ray variant). Never deployed, not product code.
// It mounts the designer's own 3D view (a lab copy of space.js that only adds one export) and adds, in this file only:
//   service runs (cold #1565c0, hot #c62828 dashed, gas #f5b800, electricity #6a3fc8), an x-ray mode, eleven white parts, a camera API.
// Plan: example-4r (kitchen, WC, bath, laundry/service room "שירות", safe room "ממ״ד"). Units: plan centimetres, X right, Y down the sheet, Z up.
import * as THREE from 'three';
import { createStore, emptyDesign } from '../../../plugins/nadlan-config/assets/designer/core.js';
import * as cat from '../../../plugins/nadlan-config/assets/designer/catalog.js';
import { mountSpace } from './space.lab.js';
import { RUNS, PART_META, ROOM_SHORT, ICON_PATHS, PART_ICON } from './services.js';

const D = '../../../plugins/nadlan-config/assets/designer/';
const PLAN_FILE = 'plans/example-4r.json';
const q = new URLSearchParams(location.search);
const M = 0.01;
const BG = '#eef2f6';
const INK = 0x0f2233;
const FOV = 20;
const COL = { c: 0x1565c0, h: 0xc62828, g: 0xf5b800, e: 0x6a3fc8 };
const V = (x, y, z) => new THREE.Vector3(x * M, z * M, y * M); // plan (x, y) + height -> three.js (X, Y up, Z)

const AO_ON = q.get('ao') !== '0';
// ambient occlusion: three's GTAOPass through the EffectComposer (same 0.170.0 CDN path); loaded BEFORE the first frame so the first frame already has it
const AO_MODS = AO_ON ? await Promise.all([import('three/addons/postprocessing/EffectComposer.js'), import('three/addons/postprocessing/RenderPass.js'), import('three/addons/postprocessing/GTAOPass.js'), import('three/addons/postprocessing/OutputPass.js')]) : null;
try { await Promise.race([Promise.all([document.fonts.load('600 64px "IBM Plex Sans Hebrew"', 'שלום'), document.fonts.load('700 24px "IBM Plex Sans Hebrew"', '!'), document.fonts.load('500 17px "IBM Plex Mono"', '0123')]), new Promise((r) => setTimeout(r, 4000))]); } catch (e) { /* the system font draws instead */ }
const apt = await (await fetch(D + PLAN_FILE)).json();
const d0 = emptyDesign(apt); d0.items = cat.STARTER.filter((i) => cat.ITEMS[i.sku]).map((i) => ({ ...i }));
const store = createStore(apt, d0);
const stageEl = document.getElementById('stage');
const space = mountSpace(stageEl, store, cat, { rise: false });
const L = space.lab, { scene, camera, renderer, controls, mat, gWall, gGlass, gItem, gPoint, gFloor, ground, touch } = L;

// ---- timing and the render pipeline: first rendered 3D frame (ms from navigation start); GTAO through the composer when ao is on ----
const T = { firstRender: null, firstPresented: null, env: null };
const hideForAO = []; // things that must not take part in the ambient occlusion normal/depth pass (runs, halos, labels, the floor disc)
let composer = null, inPass = false;
{
  const r0 = renderer.render.bind(renderer);
  renderer.render = (s, c) => {
    if (inPass) { if (s.overrideMaterial) { const was = hideForAO.map((o) => o.visible); hideForAO.forEach((o) => { o.visible = false; }); r0(s, c); hideForAO.forEach((o, k) => { o.visible = was[k]; }); } else r0(s, c); return; }
    if (composer) { inPass = true; composer.render(); inPass = false; } else r0(s, c);
    if (T.firstRender == null) { T.firstRender = performance.now(); requestAnimationFrame(() => { T.firstPresented = performance.now(); }); } if (T.env == null && scene.environment) { T.env = performance.now(); scene.environmentIntensity = Number(q.get('env') ?? 0.6); }
  };
}
renderer.toneMapping = THREE.NoToneMapping; // exact colours: the runs, the ink and the background keep their hex values
L.hemi.intensity = Number(q.get('hemi') ?? 2.6); L.sun.intensity = Number(q.get('sun') ?? 1.6); scene.environmentIntensity = Number(q.get('env') ?? 0.6);

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
  const P = { id, g, mat: WHITE(), edge: edgeMat(), glass: new THREE.MeshStandardMaterial({ color: 0xd6e6f2, roughness: 0.1, transparent: true, opacity: 0.2, depthWrite: false }), meshes: [], extra: [] };
  const add = (geo, x, y, z, o = {}) => { // x, y = plan centre, z = centre height (cm)
    const m = new THREE.Mesh(geo, o.m || (o.glass ? P.glass : P.mat)); if (o.m && !P.extra.includes(o.m)) P.extra.push(o.m); m.position.set(x * M, z * M, y * M); if (o.q) m.quaternion.copy(o.q); if (o.rx) m.rotation.x = o.rx; if (o.ry) m.rotation.y = o.ry; if (o.rz) m.rotation.z = o.rz; if (o.sx) m.scale.x = o.sx; if (o.sz) m.scale.z = o.sz;
    m.castShadow = !o.glass; m.receiveShadow = true; g.add(m); P.meshes.push(m);
    if (!o.noedge) { const e = new THREE.LineSegments(new THREE.EdgesGeometry(geo, o.thr || 25), P.edge); e.position.copy(m.position); e.quaternion.copy(m.quaternion); e.scale.copy(m.scale); g.add(e); }
    return m;
  };
  // w along X, d along Y (plan), h up; (x, y) the plan centre, z0 the bottom
  P.box = (w, d, h, x, y, z0, o) => add(new THREE.BoxGeometry(w * M, h * M, d * M), x, y, z0 + h / 2, o);
  P.cylZ = (r, h, x, y, z0, o) => add(new THREE.CylinderGeometry(r * M, r * M, h * M, 28), x, y, z0 + h / 2, o); // vertical
  P.cylX = (r, len, x, y, zc, o) => add(new THREE.CylinderGeometry(r * M, r * M, len * M, 32), x, y, zc, { ...o, rz: Math.PI / 2 }); // along X
  // a round bar between two plan points [x, y, z] (cm)
  P.bar = (a, b, r, o = {}) => { const A = V(...a), B = V(...b), d = B.clone().sub(A), len = d.length(); const q = new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0, 1, 0), d.clone().normalize()); const m = add(new THREE.CylinderGeometry(r * M, r * M, len, o.seg || 14), (a[0] + b[0]) / 2, (a[1] + b[1]) / 2, (a[2] + b[2]) / 2, { ...o, q }); return m; };
  P.sphere = (r, x, y, z, o = {}) => add(new THREE.SphereGeometry(r * M, 20, 14), x, y, z, o);
  return P;
}
const PARTS = {};
function def(id, o) { PARTS[id] = { id, ...o, ...PART_META[id] }; return PARTS[id]; }

// 1. living-room AC (wall unit on the north facade, lowered to 91-119 cm so it shows under the 118 cm cut)
{ const P = newPart('acLiving'); const x = 555, y = 23.5;
  P.box(80, 22, 28, x, y, 91); P.box(76, 4, 6, x, y + 12, 88); for (const k of [-24, -8, 8, 24]) P.box(1.2, 1, 22, x + k, y + 11.4, 94, { noedge: true });
  P.box(10, 1, 2.5, x + 28, y + 11.2, 110);
  def('acLiving', { P, view: { az: 28, el: 34, d: 8 } }); }
// 2. living-room shutter at the big window: housing, side guides, half-lowered slats
{ const P = newPart('shutter'); const x = 310, y = 0;
  P.box(364, 22, 24, x, y, 234); P.box(4, 8, 234, 128, y, 0); P.box(4, 8, 234, 492, y, 0);
  for (let k = 0; k < 16; k++) P.box(356, 2.4, 6.6, x, y - 3, 226 - k * 8);
  P.box(358, 3.5, 5, x, y - 3, 226 - 16 * 8);
  def('shutter', { P, view: { az: 20, el: 34, d: 11 } }); }
// 3. cooktop and oven in the kitchen counter (south wall of the kitchen)
{ const P = newPart('cooktop'); const x = 120, y = 857;
  P.box(60, 52, 3, x, y, 90);
  for (const [dx, dy, r] of [[-14, -12, 8], [14, -12, 6], [-14, 12, 6], [14, 12, 8]]) P.cylZ(r, 1.6, x + dx, y + dy, 93);
  for (const k of [-21, -7, 7, 21]) P.cylZ(2.2, 3.2, x + k, y - 26, 90.5);
  P.box(58, 3, 50, x, 826, 34); P.box(50, 2.4, 2.6, x, 823.4, 76); P.box(42, 1, 28, x, 824.4, 40, { noedge: false });
  def('cooktop', { P, view: { az: 150, el: 36, d: 7 } }); }
// 4. fridge, north-east corner of the kitchen, back to the wall between kitchen and hall
{ const P = newPart('fridge'); const x = 318, y = 560;
  P.box(70, 66, 118, x, y, 0); P.box(70, 66, 60, x, y, 120); P.box(70, 3, 118, x, y + 34.5, 0); P.box(70, 3, 60, x, y + 34.5, 120);
  P.box(2.6, 4, 40, x - 28, y + 38, 70); P.box(2.6, 4, 22, x - 28, y + 38, 140);
  def('fridge', { P, view: { az: 30, el: 30, d: 8 } }); }
// 5. kitchen sink with the main tap
{ const P = newPart('sink'); const x = 270, y = 857;
  P.box(82, 46, 2, x, y, 90); P.box(64, 34, 1.6, x, y + 1, 91.4); P.box(26, 30, 1.6, x + 18, y + 1, 92.6, { noedge: false });
  P.cylZ(2.4, 24, x, 880, 92); P.cylX(1.7, 22, x, 872, 116); P.box(2, 2, 9, x + 6, 880, 116); P.cylZ(3.4, 2, x, 880, 92);
  def('sink', { P, view: { az: 150, el: 36, d: 7 } }); }
// 6. electrical panel by the entrance door (hall side of the wall next to the service room)
{ const P = newPart('panel'); const x = 601, y = 860;
  P.box(12, 34, 42, x, y, 139); P.box(1.6, 29, 37, x - 6.6, y, 141.5);
  for (let r = 0; r < 2; r++) for (let c = 0; c < 4; c++) P.box(1.2, 4, 7, x - 7.6, y - 10.5 + c * 7, 146 + r * 14);
  def('panel', { P, view: { az: -35, el: 28, d: 6.5 } }); }
// 7. bedroom AC (master, north facade)
{ const P = newPart('acBed'); const x = 920, y = 23.5;
  P.box(80, 22, 28, x, y, 91); P.box(76, 4, 6, x, y + 12, 88); for (const k of [-24, -8, 8, 24]) P.box(1.2, 1, 22, x + k, y + 11.4, 94, { noedge: true });
  P.box(10, 1, 2.5, x + 28, y + 11.2, 110);
  def('acBed', { P, view: { az: 28, el: 34, d: 8 } }); }
// 8. safe room (ממ״ד): steel door in the corridor wall and the steel window shutter on the east wall
{ const P = newPart('mamad');
  P.box(80, 12, 205, 1080, 500, 0); P.box(7, 18, 205, 1036.5, 500, 0); P.box(7, 18, 205, 1123.5, 500, 0); P.box(94, 18, 8, 1080, 500, 205);
  P.box(4, 14, 56, 1100, 508, 96); for (const z of [30, 90, 150, 190]) P.cylX(3, 6, 1121, 500, z, { noedge: false });
  P.box(10, 106, 106, 1320, 700, 100); P.box(6, 74, 74, 1314, 700, 116); for (const [a, b] of [[-46, -46], [46, -46], [-46, 46], [46, 46]]) P.cylX(3, 4, 1314, 700 + a, 146 + b, { noedge: false });
  def('mamad', { P, view: { az: -45, el: 34, d: 13 } }); }
// 9. shower and toilet (the "רחצה" room, against the wall shared with the service room)
{ const P = newPart('bath');
  P.box(90, 90, 6, 878, 850, 0); P.box(1.4, 90, 195, 923, 850, 0, { glass: true }); P.box(90, 1.4, 195, 878, 805, 0, { glass: true });
  P.box(2, 2, 195, 923, 805, 0); P.cylZ(1.5, 96, 837, 863, 104); P.box(22, 2.2, 2.2, 848, 863, 198); P.cylZ(11, 2, 863, 863, 197);
  P.box(6, 62, 5, 835, 865, 101.5);
  P.box(18, 38, 60, 842, 775, 20); P.cylZ(19, 40, 872, 775, 0, { sx: 1.5 }); P.cylZ(18, 3, 872, 775, 40, { sx: 1.5 }); P.cylZ(3, 2, 842, 775, 80);
  def('bath', { P, view: { az: 140, el: 40, d: 10.5 } }); }
// 10. solar water heater: horizontal enamel tank with domed caps and two straps, galvanised frame with cross braces, fittings with valves where
//     the cold (underneath, west) and hot (east end) runs connect, an element cover with a cable to the electricity run, a thermostat box
{ const P = newPart('boiler'); const x = 720, y = 862, zc = 116, R = 24;
  const enamel = new THREE.MeshPhysicalMaterial({ color: 0xf6f8fa, roughness: 0.22, metalness: 0, clearcoat: 0.7, clearcoatRoughness: 0.2, envMapIntensity: 0.9 });
  const steel = new THREE.MeshStandardMaterial({ color: 0xa9b3bc, roughness: 0.42, metalness: 0.75, envMapIntensity: 1.0 });
  const dark = new THREE.MeshStandardMaterial({ color: 0x2b3640, roughness: 0.6, metalness: 0.2 });
  const wheelC = new THREE.MeshStandardMaterial({ color: 0x1565c0, roughness: 0.5 }), wheelH = new THREE.MeshStandardMaterial({ color: 0xc62828, roughness: 0.5 });
  // body, domed caps and the weld seams
  const add = (geo, px, py, pz, o) => { const m = new THREE.Mesh(geo, o.m); m.position.set(px * M, pz * M, py * M); if (o.rz) m.rotation.z = o.rz; if (o.sc) m.scale.set(...o.sc); m.castShadow = m.receiveShadow = true; P.g.add(m); if (!P.extra.includes(o.m)) P.extra.push(o.m); if (o.edge !== false) { const e = new THREE.LineSegments(new THREE.EdgesGeometry(geo, o.thr || 28), P.edge); e.position.copy(m.position); e.rotation.copy(m.rotation); e.scale.copy(m.scale); P.g.add(e); } return m; };
  add(new THREE.CylinderGeometry(R * M, R * M, 104 * M, 56), x, y, zc, { m: enamel, rz: Math.PI / 2 });
  const dome = new THREE.SphereGeometry(R * M, 56, 18, 0, Math.PI * 2, 0, Math.PI / 2);
  add(dome, x + 52, y, zc, { m: enamel, rz: -Math.PI / 2, sc: [1, 0.4, 1] }); add(dome, x - 52, y, zc, { m: enamel, rz: Math.PI / 2, sc: [1, 0.4, 1] });
  for (const bx of [x - 28, x + 28]) { P.cylX(R + 0.9, 4, bx, y, zc, { m: steel, noedge: false }); P.box(5, 3, 3, bx, y - R - 1.5, zc - 2, { m: steel, noedge: true }); }
  // frame: four round legs on foot plates, rails under the straps, cross braces
  const legs = [[675, 842], [765, 842], [675, 882], [765, 882]];
  for (const [lx, ly] of legs) { P.bar([lx, ly, 2], [lx, ly, 91], 2.1, { m: steel, noedge: true }); P.cylZ(4.2, 1.6, lx, ly, 0, { m: steel, noedge: true }); }
  for (const bx of [x - 28, x + 28]) { P.bar([bx, 842, 91], [bx, 882, 91], 1.9, { m: steel, noedge: true }); }
  P.bar([675, 842, 91], [765, 842, 91], 1.5, { m: steel, noedge: true }); P.bar([675, 882, 91], [765, 882, 91], 1.5, { m: steel, noedge: true });
  P.bar([675, 842, 24], [765, 842, 24], 1.5, { m: steel, noedge: true }); P.bar([675, 882, 24], [765, 882, 24], 1.5, { m: steel, noedge: true }); P.bar([675, 842, 24], [675, 882, 24], 1.5, { m: steel, noedge: true }); P.bar([765, 842, 24], [765, 882, 24], 1.5, { m: steel, noedge: true });
  P.bar([675, 842, 24], [765, 842, 88], 1.2, { m: steel, noedge: true }); P.bar([765, 842, 24], [675, 842, 88], 1.2, { m: steel, noedge: true });
  P.bar([675, 882, 24], [765, 882, 88], 1.2, { m: steel, noedge: true }); P.bar([765, 882, 24], [675, 882, 88], 1.2, { m: steel, noedge: true });
  P.bar([675, 842, 30], [675, 882, 80], 1.2, { m: steel, noedge: true }); P.bar([675, 882, 30], [675, 842, 80], 1.2, { m: steel, noedge: true });
  P.bar([765, 842, 30], [765, 882, 80], 1.2, { m: steel, noedge: true }); P.bar([765, 882, 30], [765, 842, 80], 1.2, { m: steel, noedge: true });
  // cold inlet, underneath at the west end: nipple, valve body, blue handwheel; the cold run ends at the foot of it
  P.bar([670, 862, 76], [670, 862, 93], 2.2, { m: steel, noedge: true }); P.sphere(4.2, 670, 862, 82, { m: steel, noedge: true }); P.bar([670, 862, 85], [670, 862, 89], 0.8, { m: steel, noedge: true }); P.cylZ(4.6, 1.2, 670, 862, 89, { m: wheelC, noedge: true });
  // hot outlet, at the east end: nipple, valve body, red handwheel; the hot run starts at its tip
  P.bar([781, 862, zc], [794, 862, zc], 2.2, { m: steel, noedge: true }); P.sphere(4.2, 788, 862, zc, { m: steel, noedge: true }); P.bar([788, 862, zc + 3], [788, 862, zc + 8], 0.8, { m: steel, noedge: true }); P.cylZ(4.6, 1.2, 788, 862, zc + 8, { m: wheelH, noedge: true });
  // anode plug on the west cap
  P.cylX(3.4, 3, x - 60.5, y, zc, { m: steel, noedge: false });
  // electric element cover on the front (north) face, a cable over the tank to the electricity run
  { const cv = new THREE.Mesh(new THREE.CylinderGeometry(7.2 * M, 7.2 * M, 3 * M, 32), steel); cv.rotation.x = Math.PI / 2; cv.position.set(748 * M, 112 * M, (y - R - 1.2) * M); cv.castShadow = true; P.g.add(cv);
    const nut = new THREE.Mesh(new THREE.CylinderGeometry(2.6 * M, 2.6 * M, 2.4 * M, 6), dark); nut.rotation.x = Math.PI / 2; nut.position.set(748 * M, 112 * M, (y - R - 3.2) * M); P.g.add(nut);
    const e = new THREE.LineSegments(new THREE.EdgesGeometry(cv.geometry, 28), P.edge); e.position.copy(cv.position); e.rotation.copy(cv.rotation); P.g.add(e);
    const cable = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3([V(748, 835, 112), V(748, 829, 118), V(748, 833, 134), V(748, 850, 147), V(748, 874, 146), V(748, 890, 136), V(748, 899, 124), V(748, 900, 118)], false, 'catmullrom', 0.3), 48, 0.9 * M, 8, false), dark); cable.castShadow = true; P.g.add(cable);
    P.extra.push(steel, dark); }
  // thermostat box on the top, front side, with a dial
  P.box(10, 8, 10, 704, 851, 136, { m: enamel });
  { const dial = new THREE.Mesh(new THREE.CylinderGeometry(2.4 * M, 2.4 * M, 1.4 * M, 20), dark); dial.rotation.x = Math.PI / 2; dial.position.set(704 * M, 141 * M, 846.4 * M); P.g.add(dial); }
  def('boiler', { P, view: { az: -135, el: 36, d: 8.5 } }); }
// 11. washing machine in the service room, back to the wall shared with the bathroom: door ring with dark glass, control strip, detergent drawer
{ const P = newPart('washer'); const x = 780, y = 722, fx = x - 30;
  const enamel = new THREE.MeshPhysicalMaterial({ color: 0xf6f8fa, roughness: 0.3, clearcoat: 0.4, envMapIntensity: 0.8 }), rim = new THREE.MeshStandardMaterial({ color: 0xc3ccd5, roughness: 0.35, metalness: 0.6 });
  const glass = new THREE.MeshPhysicalMaterial({ color: 0x18222d, roughness: 0.06, metalness: 0.1, clearcoat: 1, clearcoatRoughness: 0.05, envMapIntensity: 1.2 }), strip = new THREE.MeshStandardMaterial({ color: 0xdde4ea, roughness: 0.5 }), dk = new THREE.MeshStandardMaterial({ color: 0x1f2933, roughness: 0.5 });
  P.box(60, 60, 84, x, y, 2, { m: enamel }); for (const [dx, dy] of [[-26, -26], [26, -26], [-26, 26], [26, 26]]) P.cylZ(2.2, 2, x + dx, y + dy, 0, { m: dk, noedge: true });
  const facing = new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0, 0, 1), new THREE.Vector3(-1, 0, 0)); // torus in XY plane -> faces west
  const ring = new THREE.Mesh(new THREE.TorusGeometry(19 * M, 2.6 * M, 16, 48), rim); ring.quaternion.copy(facing); ring.position.set((fx - 1) * M, 40 * M, y * M); ring.castShadow = true; P.g.add(ring); P.extra.push(rim);
  const gl = new THREE.Mesh(new THREE.CylinderGeometry(16.6 * M, 16.6 * M, 1.8 * M, 40), glass); gl.rotation.z = Math.PI / 2; gl.position.set((fx - 0.6) * M, 40 * M, y * M); P.g.add(gl); P.extra.push(glass);
  const inner = new THREE.Mesh(new THREE.TorusGeometry(11 * M, 0.9 * M, 10, 36), dk); inner.quaternion.copy(facing); inner.position.set((fx - 1.6) * M, 40 * M, y * M); P.g.add(inner);
  const hinge = new THREE.Mesh(new THREE.BoxGeometry(1.4 * M, 8 * M, 3 * M), rim); hinge.position.set((fx - 1.2) * M, 40 * M, (y + 22.5) * M); P.g.add(hinge);
  P.box(1.6, 56, 10, fx - 0.8, y, 72, { m: strip }); P.box(1.2, 10, 4, fx - 1.6, y + 14, 76, { m: dk, noedge: true }); P.cylX(3.4, 2.2, fx - 1.8, y - 12, 77, { m: dk, noedge: true });
  for (const k of [-6, -2, 2]) P.cylX(1.2, 1.6, fx - 1.6, y + k, 74.4, { m: dk, noedge: true });
  P.box(1.0, 20, 4.2, fx - 0.7, y - 18, 61.5, { m: strip }); P.box(1.2, 9, 1.2, fx - 1.4, y - 18, 63, { m: dk, noedge: true });
  def('washer', { P, view: { az: -135, el: 36, d: 8 } }); }

// =====================================================================================================================
// service runs (all axis-aligned; installers run along walls, never diagonally)
// Round 2: thin cores (2.2 cm), hot dashed 6 cm beside cold, electricity INSIDE the walls at 90 cm (just under the window sills
// and the 118 cm cut), dipping into the floor slab where a door or an opening interrupts the wall.
// =====================================================================================================================
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

// ---- ink caps: the cut tops of the walls, ours in both modes, full ink #14212b ----
let capMesh = null, wallPre = null;
{
  const src = gWall.children[0], g0 = src.geometry, nor = g0.attributes.normal.array, I = g0.index.array, keep = [];
  for (let i = 0; i < I.length; i += 3) { if (nor[I[i] * 3 + 1] > 0.9) keep.push(I[i], I[i + 1], I[i + 2]); }
  const INKC = new THREE.Color('#14212b'), colA = new Float32Array(g0.attributes.color.count * 3); // every cut top in the drawing's ink, whatever the engine's wall kind
  for (let k = 0; k < colA.length; k += 3) { colA[k] = INKC.r; colA[k + 1] = INKC.g; colA[k + 2] = INKC.b; }
  const pos0 = g0.attributes.position, posA = new Float32Array(pos0.array), done = new Set(), CAPK = Number(q.get('capk') ?? 0.55);
  for (const vi of keep) { const b = vi - (vi % 4); if (done.has(b)) continue; done.add(b); let cx = 0, cz = 0, x0 = 9e9, x1 = -9e9, z0 = 9e9, z1 = -9e9;
    for (let k = 0; k < 4; k++) { const x = posA[(b + k) * 3], z = posA[(b + k) * 3 + 2]; cx += x / 4; cz += z / 4; x0 = Math.min(x0, x); x1 = Math.max(x1, x); z0 = Math.min(z0, z); z1 = Math.max(z1, z); }
    const thinX = (x1 - x0) < (z1 - z0) ? 1 : 0; for (let k = 0; k < 4; k++) { const i3 = (b + k) * 3 + (thinX ? 0 : 2), c = thinX ? cx : cz; posA[i3] = c + (posA[i3] - c) * CAPK; } }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(posA, 3)); g.setAttribute('color', new THREE.BufferAttribute(colA, 3)); g.setIndex(keep);
  const cm = new THREE.MeshBasicMaterial({ vertexColors: true, toneMapped: false }); cm.onBeforeCompile = (sh) => fadeShader(sh, false, null);
  capMesh = new THREE.Mesh(g, cm); capMesh.position.y = 0.004; capMesh.renderOrder = 3; scene.add(capMesh);
  wallPre = new THREE.Mesh(src.geometry, new THREE.MeshBasicMaterial({ colorWrite: false, polygonOffset: true, polygonOffsetFactor: 2, polygonOffsetUnits: 2 })); wallPre.renderOrder = 5; scene.add(wallPre); // depth-only copy: the translucent walls then draw ONE layer, the nearest
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
const FLOOR = q.get('floor') || '#d6dfe9', FLOORLINE = q.get('line') || '#bcc9d6', FLOORK = Number(q.get('floork') ?? 0.92);
const mkGrid = (bg, ln) => { const c = document.createElement('canvas'); c.width = c.height = 256; const x = c.getContext('2d'); x.fillStyle = bg; x.fillRect(0, 0, 256, 256); x.strokeStyle = ln; x.lineWidth = 4; x.strokeRect(0, 0, 256, 256);
  const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(1 / 0.6, 1 / 0.6); t.anisotropy = 8; t.colorSpace = THREE.SRGBColorSpace; return t; };
const floorWhite = new THREE.MeshStandardMaterial({ map: mkGrid(FLOOR, FLOORLINE), color: new THREE.Color(FLOORK, FLOORK, FLOORK), roughness: 0.95, envMapIntensity: 0.2, side: THREE.DoubleSide });
const deckMat = new THREE.MeshStandardMaterial({ map: mkGrid('#e3e9ef', '#d2dbe3'), color: new THREE.Color(FLOORK, FLOORK, FLOORK), roughness: 0.95, envMapIntensity: 0.2, side: THREE.DoubleSide });
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
const WALLA = Number(q.get('walla') ?? 0.5);
const S = { mode: 'normal', layer: 'all', layerK: 1, focus: null };
const ghostMat = new THREE.MeshStandardMaterial({ color: 0xcdd6df, roughness: 1, metalness: 0, transparent: true, opacity: 0.6, depthWrite: false, envMapIntensity: 0.1 }); ghostMat.onBeforeCompile = (sh) => fadeShader(sh, false, null);
let focusBox = null, focusRun = null; // the room of the last focused part (plan cm) and the same box widened by 60 cm for the runs
const clamp01 = (v) => Math.max(0, Math.min(1, v));
const lerp = (a, b, t) => a + (b - a) * t;

function applyMode() {
  const x = S.mode === 'xray';
  mat.wall.color.set(x ? Number('0x' + (q.get('wallc') || 'e4e9ee')) : 0xffffff); mat.wall.transparent = x; mat.wall.opacity = x ? WALLA : 1; mat.wall.depthWrite = !x; mat.wall.needsUpdate = true; wallPre.visible = x;
  capMesh.material.transparent = false; capMesh.material.opacity = 1;
  runsRoot.visible = x; boilerDisc.visible = x;
  gGlass.children.forEach((c) => { if (c.material === mat.rail) c.visible = !x || q.get('rail') === '1'; });
  gItem.traverse((o) => {
    if (o.userData.furnEdge) { o.visible = true; o.material.opacity = x ? 0.5 : 0.6; return; }
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
    for (const m of [P.mat, ...P.extra]) { const tr = a < 0.999; if (m.transparent !== tr) { m.transparent = tr; m.needsUpdate = true; } m.opacity = a; m.depthWrite = !tr; } P.edge.opacity = a;
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
// room names written flat on the floor, and the room-cluster markers (HTML over the canvas)
// =====================================================================================================================
const labelsGroup = new THREE.Group(); scene.add(labelsGroup);
const LABEL_AT = { living: [290, 420], kitchen: [120, 600], hall: [495, 600], master: [810, 300], bed2: [1160, 190], corridor: [940, 440], wc: [720, 590], laundry: [700, 745], bath: [910, 560], mamad: [1160, 610], balcony: [565, -118] };
const markersEl = document.createElement('div'); markersEl.id = 'markers'; stageEl.appendChild(markersEl);
function buildLabels(mpp, az, avoid = []) {
  while (labelsGroup.children.length) { const c = labelsGroup.children.pop(); c.geometry.dispose(); c.material.map.dispose(); c.material.dispose(); }
  const a = (az * Math.PI) / 180, right = new THREE.Vector3(Math.cos(a), 0, -Math.sin(a)), fwd = new THREE.Vector3(-Math.sin(a), 0, -Math.cos(a)), up = new THREE.Vector3(0, 1, 0);
  const qn = new THREE.Quaternion().setFromRotationMatrix(new THREE.Matrix4().makeBasis(right, fwd, up));
  const Hp = 34 * mpp * Number(q.get('labelk') ?? 1); // glyphs about 12 CSS px high on screen at this distance
  for (const f of store.derived.faces) {
    if (!f.room) continue; const text = ROOM_SHORT[f.room.id] || ROOM_SHORT[f.id]; let at = LABEL_AT[f.id]; if (!text || !at) continue;
    if (avoid.length) { // the spot of the room farthest from the markers and pills (screen px), near the room's middle
      const xs = f.poly.map((v) => v[0]), ys = f.poly.map((v) => v[1]), x0 = Math.min(...xs), x1 = Math.max(...xs), y0 = Math.min(...ys), y1 = Math.max(...ys), cx = (x0 + x1) / 2, cy = (y0 + y1) / 2; let best = null;
      for (let gx = 0; gx <= 10; gx++) for (let gy = 0; gy <= 10; gy++) { const px = x0 + 50 + ((x1 - x0 - 100) * gx) / 12, py = y0 + 45 + ((y1 - y0 - 160) * gy) / 12, // 130 cm clear of the south wall: the near wall hides the floor behind it
 [sx, sy] = toCss(px, py); const md = Math.min(...avoid.map((a) => Math.hypot(a[0] - sx, a[1] - sy) - (a[2] || 0))); const score = Math.min(md, 60) - 0.03 * Math.hypot(px - cx, py - cy); if (!best || score > best.score) best = { score, px, py }; }
      if (best) at = [best.px, best.py]; }
    const c = document.createElement('canvas'); c.width = 512; c.height = 128; const x = c.getContext('2d'); x.direction = 'rtl'; x.textAlign = 'center'; x.textBaseline = 'middle';
    x.font = '600 64px "IBM Plex Sans Hebrew", Arial, sans-serif'; x.fillStyle = 'rgba(20,33,43,0.72)'; x.fillText(text, 256, 70);
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
    const m = new THREE.Mesh(new THREE.PlaneGeometry(Hp * 4, Hp), new THREE.MeshBasicMaterial({ map: t, transparent: true, depthWrite: false, toneMapped: false }));
    m.quaternion.copy(qn); m.position.set(at[0] * M, 0.012, at[1] * M); m.renderOrder = 2; labelsGroup.add(m);
  }
}
function relayout(markersOn) {
  const dist = overview.pos.distanceTo(overview.tgt), mpp = (2 * dist * Math.tan((FOV * Math.PI) / 360)) / stageEl.clientHeight;
  buildLabels(mpp, OV.az, []); // the floor names exist only behind ?labels=1; the gate frame carries the names in the chips
}
const roomIdOf = (p) => store.roomAt(...p.roomPt);
function clusterDefs() {
  const by = {}; for (const id in PARTS) { const r = roomIdOf(PARTS[id]); (by[r] = by[r] || []).push(id); }
  return Object.entries(by).map(([room, ids]) => { const f = store.derived.faces.find((fc) => fc.id === room); const xs = f.poly.map((v) => v[0]), ys = f.poly.map((v) => v[1]);
    const state = ids.some((i) => PARTS[i].state === 'fault') ? 'fault' : ids.some((i) => PARTS[i].state === 'soon') ? 'soon' : 'ok';
    return { room, roomHe: f.room.name_he, parts: ids, count: ids.length, state, box: [Math.min(...xs), Math.min(...ys), Math.max(...xs), Math.max(...ys)] }; });
}
const toCss = (x, y) => { const n = V(x, y, 0).project(camera); return [((n.x + 1) / 2) * stageEl.clientWidth, ((1 - n.y) / 2) * stageEl.clientHeight]; };
let CLUSTERS = [], PILLS = [], MARKER_SHARE = {};
const svgI = (k, sz = 22) => '<svg width="' + sz + '" height="' + sz + '" viewBox="0 0 24 24" fill="none" stroke="#14212b" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + ICON_PATHS[k] + '</svg>';
const toCss3 = (x, y, z) => { const n = V(x, y, z).project(camera); return [((n.x + 1) / 2) * stageEl.clientWidth, ((1 - n.y) / 2) * stageEl.clientHeight]; };
// markers (round 5): a room with one part and no state = an icon-only 44 px circle; several parts = a narrow pill "name · count"; the living room (due soon) =
// a 44 px clock circle plus a small 20 px tag; the fault = a 44 px red circle with "!" ON the boiler's room plus a 24 px tag over the page background.
// Every marker sits on its own room's floor when the room is at least 48 px on screen (otherwise just outside, with a 1 px leader line to the room's centre),
// 8 px apart, never outside the stage and clear of the water and gas runs.
function placeMarkers() {
  camera.updateMatrixWorld(); camera.updateProjectionMatrix(); markersEl.innerHTML = '';
  const W = stageEl.clientWidth, H = stageEl.clientHeight, NS = 'http://www.w3.org/2000/svg', GAP = 8, EDGE = 6;
  const defs = clusterDefs().sort((a, b) => (b.state === 'fault') - (a.state === 'fault') || b.count - a.count);
  const ov = document.createElementNS(NS, 'svg'); ov.setAttribute('width', W); ov.setAttribute('height', H); ov.style.cssText = 'position:absolute;left:0;top:0'; markersEl.appendChild(ov);
  // the home's outline on screen (convex hull), to tell page background from floor
  const hp = corners.map((c) => { const n = c.clone().project(camera); return [((n.x + 1) / 2) * W, ((1 - n.y) / 2) * H]; }).sort((a, b) => a[0] - b[0] || a[1] - b[1]), cr = (o, a, b) => (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]), lo = [], up = [];
  for (const p of hp) { while (lo.length > 1 && cr(lo[lo.length - 2], lo[lo.length - 1], p) <= 0) lo.pop(); lo.push(p); } for (const p of hp.slice().reverse()) { while (up.length > 1 && cr(up[up.length - 2], up[up.length - 1], p) <= 0) up.pop(); up.push(p); }
  const hull = lo.slice(0, -1).concat(up.slice(0, -1)), inHull = (x, y) => hull.every((a, k) => { const b = hull[(k + 1) % hull.length]; return cr(a, b, [x, y]) >= -1; });
  for (const d of defs) {
    const e = document.createElement('div'), names = d.parts.map((i) => PART_META[i].he).join(', '), name = ROOM_SHORT[d.room] || d.roomHe; e.dataset.room = d.room; e.setAttribute('role', 'img');
    d.aria = d.roomHe + ': ' + names + (d.state === 'fault' ? ' (תקלה פתוחה)' : d.state === 'soon' ? ' (לטיפול בקרוב)' : ''); e.setAttribute('aria-label', d.aria);
    if (d.state === 'fault') { e.className = 'mkc fault'; e.innerHTML = '<span class="bang">!</span>'; d.kind = 'circle-fault'; }
    else if (d.state === 'soon') { e.className = 'mkc soon'; e.innerHTML = svgI('clock', 24); d.kind = 'circle-clock'; }
    else if (d.count > 1) { e.className = 'mkp'; e.innerHTML = '<span>' + name + ' · ' + d.count + '</span>'; d.kind = 'pill-count'; }
    else { e.className = 'mkc'; e.innerHTML = svgI(PART_ICON[d.parts[0]], 24); d.kind = 'circle-icon'; }
    markersEl.appendChild(e); d.el = e; d.w = e.offsetWidth; d.h = e.offsetHeight;
    if (d.state !== 'ok') { const t = document.createElement('div'); t.className = 'tag ' + d.state; t.textContent = d.state === 'fault' ? 'דוד שמש · תקלה' : 'מזגן סלון'; t.setAttribute('aria-hidden', 'true'); markersEl.appendChild(t); d.tagEl = t; d.tw = t.offsetWidth; d.th = t.offsetHeight; }
    const cs = d.box, pr = [[cs[0], cs[1]], [cs[2], cs[1]], [cs[0], cs[3]], [cs[2], cs[3]]].map(([x, y]) => toCss(x, y)); d.roomPx = [Math.max(...pr.map((q) => q[0])) - Math.min(...pr.map((q) => q[0])), Math.max(...pr.map((q) => q[1])) - Math.min(...pr.map((q) => q[1]))];
  }
  const obst = []; for (const r of RUNS) if (r.sys !== 'e') for (let k = 1; k < r.pts.length; k++) { const a = r.pts[k - 1], b = r.pts[k], n = Math.max(1, Math.ceil(Math.hypot(b[0] - a[0], b[1] - a[1], b[2] - a[2]) / 12)); for (let t = 0; t <= n; t++) obst.push(toCss3(a[0] + ((b[0] - a[0]) * t) / n, a[1] + ((b[1] - a[1]) * t) / n, a[2] + ((b[2] - a[2]) * t) / n)); }
  const layout = (forceOut) => {
  while (ov.firstChild) ov.removeChild(ov.firstChild);
  const placed = [], hitsRun = (x0, y0, w, h) => obst.some((o) => o[0] > x0 - 2 && o[0] < x0 + w + 2 && o[1] > y0 - 2 && o[1] < y0 + h + 2);
  const ok = (x0, y0, w, h, own) => x0 >= EDGE && y0 >= EDGE && x0 + w <= W - EDGE && y0 + h <= H - EDGE && !hitsRun(x0, y0, w, h) && placed.every((q) => { const g = q === own ? 3 : GAP; return !(x0 < q.x0 + q.w + g && x0 + w > q.x0 - g && y0 < q.y0 + q.h + g && y0 + h > q.y0 - g); });
  const line = (x1, y1, x2, y2) => { const l = document.createElementNS(NS, 'line'); l.setAttribute('x1', x1); l.setAttribute('y1', y1); l.setAttribute('x2', x2); l.setAttribute('y2', y2); l.setAttribute('stroke', '#14212b'); l.setAttribute('stroke-width', 1); ov.appendChild(l); };
  for (const d of defs) {
    const [bx0, by0, bx1, by1] = d.box, C = toCss((bx0 + bx1) / 2, (by0 + by1) / 2), out = forceOut.includes(d.room), cands = [];
    if (!out) for (let gx = 0; gx <= 12; gx++) for (let gy = 0; gy <= 12; gy++) { const px = bx0 + 18 + ((bx1 - bx0 - 36) * gx) / 12, py = by0 + 18 + ((by1 - by0 - 36) * gy) / 12, [sx, sy] = toCss(px, py); cands.push({ x: sx, y: sy, inside: true, cost: Math.hypot(sx - C[0], sy - C[1]), plan: [px, py] }); }
    for (let r = 40; r <= 340; r += 12) for (let k = 0; k < 28; k++) { const a = (k / 28) * Math.PI * 2; cands.push({ x: C[0] + Math.cos(a) * r * 1.4, y: C[1] + Math.sin(a) * r * 0.9, inside: false, cost: 1000 + r }); }
    cands.sort((a, b) => a.cost - b.cost); let pick = null;
    const bgRect = (c) => [[-1, -1], [1, -1], [-1, 1], [1, 1]].every(([sx, sy]) => !inHull(c.x + (sx * d.w) / 2, c.y + (sy * d.h) / 2));
    for (const c of cands) if (ok(c.x - d.w / 2, c.y - d.h / 2, d.w, d.h) && (!out || bgRect(c))) { pick = c; break; }
    if (!pick) pick = cands.find((c) => c.inside) || cands[0];
    const rect = { x0: pick.x - d.w / 2, y0: pick.y - d.h / 2, w: d.w, h: d.h }; placed.push(rect);
    d.x = Math.round(pick.x * 10) / 10; d.y = Math.round(pick.y * 10) / 10; d.inside = pick.inside; d.anchor = [Math.round(C[0] * 10) / 10, Math.round(C[1] * 10) / 10]; d.plan = pick.plan ? [Math.round(pick.plan[0]), Math.round(pick.plan[1])] : null;
    d.el.style.left = rect.x0 + 'px'; d.el.style.top = rect.y0 + 'px';
    if (!pick.inside) { const dx = C[0] - pick.x, dy = C[1] - pick.y, tx = Math.abs(dx) > 1e-6 ? d.w / 2 / Math.abs(dx) : 1e9, ty = Math.abs(dy) > 1e-6 ? d.h / 2 / Math.abs(dy) : 1e9, t = Math.min(tx, ty, 1); line(pick.x + dx * t, pick.y + dy * t, C[0], C[1]); const dot = document.createElementNS(NS, 'circle'); dot.setAttribute('cx', C[0]); dot.setAttribute('cy', C[1]); dot.setAttribute('r', 3); dot.setAttribute('fill', '#14212b'); ov.appendChild(dot); }
    if (d.tagEl) { // the tag: beside its marker; the fault's tag over the page background (all four corners outside the home), else the nearest free spot
      const tc = [], tw = d.tw, th = d.th, mx = pick.x, my = pick.y;
      for (let r = 0; r <= 230; r += 8) for (let k = 0; k < 32; k++) { const a = (k / 32) * Math.PI * 2, cx = mx + Math.cos(a) * (d.w / 2 + 4 + tw / 2 + r), cy = my + Math.sin(a) * (d.h / 2 + 4 + th / 2 + r * 0.7); tc.push({ x: cx, y: cy, cost: Math.hypot(cx - mx, cy - my) }); }
      tc.sort((a, b) => a.cost - b.cost); let tp = null; const bgOnly = d.state === 'fault';
      const free = (c) => ok(c.x - tw / 2, c.y - th / 2, tw, th, rect), bg = (c) => [[-1, -1], [1, -1], [-1, 1], [1, 1]].every(([sx, sy]) => !inHull(c.x + (sx * tw) / 2, c.y + (sy * th) / 2));
      if (bgOnly) tp = tc.find((c) => free(c) && bg(c)); if (!tp) tp = tc.find(free) || tc[0];
      const tr = { x0: tp.x - tw / 2, y0: tp.y - th / 2, w: tw, h: th }; placed.push(tr); d.tagEl.style.left = tr.x0 + 'px'; d.tagEl.style.top = tr.y0 + 'px';
      d.tag = { x: Math.round(tp.x * 10) / 10, y: Math.round(tp.y * 10) / 10, w: tw, h: th, text: d.tagEl.textContent, onBackground: bg(tp) };
      const gapX = Math.max(tr.x0 - (rect.x0 + rect.w), rect.x0 - (tr.x0 + tr.w), 0), gapY = Math.max(tr.y0 - (rect.y0 + rect.h), rect.y0 - (tr.y0 + tr.h), 0); if (Math.hypot(gapX, gapY) > 10) line(pick.x, pick.y, tp.x, tp.y); // a thin line joins a tag that could not sit right beside its marker
    }
  }
  // how much of the home's floor outline (projected, CSS px) all markers, tags and leader dots hide: sampled every 2 px
  { const fp = [[0, 0], [1320, 0], [1320, 900], [0, 900], [0, -220], [620, -220]].map(([x, y]) => toCss(x, y)).sort((a, b) => a[0] - b[0] || a[1] - b[1]), l2 = [], u2 = [];
    for (const q of fp) { while (l2.length > 1 && cr(l2[l2.length - 2], l2[l2.length - 1], q) <= 0) l2.pop(); l2.push(q); } for (const q of fp.slice().reverse()) { while (u2.length > 1 && cr(u2[u2.length - 2], u2[u2.length - 1], q) <= 0) u2.pop(); u2.push(q); }
    const fh = l2.slice(0, -1).concat(u2.slice(0, -1)), inF = (x, y) => fh.every((a, k) => cr(a, fh[(k + 1) % fh.length], [x, y]) >= 0); let area = 0; for (let k = 0; k < fh.length; k++) { const a = fh[k], b = fh[(k + 1) % fh.length]; area += a[0] * b[1] - b[0] * a[1]; } area = Math.abs(area) / 2;
    const rects = placed.slice(), dots = defs.filter((d) => !d.inside).map((d) => d.anchor); let cov = 0; for (const r of rects) for (let x = r.x0 + 1; x < r.x0 + r.w; x += 2) for (let y = r.y0 + 1; y < r.y0 + r.h; y += 2) if (inF(x, y)) cov += 4;
    for (const d of dots) cov += Math.PI * 9 * (inF(d[0], d[1]) ? 1 : 0); MARKER_SHARE = { markerShareOfHome: Math.round((cov / area) * 1000) / 1000, markersAreaOverHomePx2: Math.round(cov), homeFloorAreaPx2: Math.round(area) }; }
  };
  const force = []; layout(force); const ORDER = ['kitchen', 'mamad', 'bath', 'master', 'hall'];
  while (MARKER_SHARE.markerShareOfHome > 1 / 6 && force.length < ORDER.length) { force.push(ORDER[force.length]); layout(force); }
  MARKER_SHARE.movedOffTheHome = force.slice();
  CLUSTERS = defs;
  return defs;
}
const clusterOut = (defs) => defs.map(({ room, roomHe, x, y, w, h, count, state, kind, aria, parts, plan, inside, anchor, tag, roomPx }) => ({ room, roomHe, kind, aria, x, y, w, h, count, state, parts, partNames: parts.map((i) => PART_META[i].he), plan, leader: !inside, roomCentre: anchor, roomOnScreenPx: roomPx.map((v) => Math.round(v)), tag, ...MARKER_SHARE }));

// =====================================================================================================================
// camera: overview pose (portrait: the long axis runs up the screen) and focus poses (the part's whole room in view)
// =====================================================================================================================
const mid = L.mid.clone();
const FOV_F = 46; // the focus views use a wider lens so a whole room fits at 3 to 6 m
const corners = [];
for (const x of [-22, 1338]) for (const y of [-6, 916]) for (const z of [0, 215]) corners.push(V(x, y, z));
for (const x of [0, 620]) corners.push(V(x, -222, 0)); // the balcony floor
function dirOf(az, el) { const a = (az * Math.PI) / 180, e = (el * Math.PI) / 180; return new THREE.Vector3(Math.sin(a) * Math.cos(e), Math.sin(e), Math.cos(a) * Math.cos(e)); }
function aspect() { return stageEl.clientWidth / stageEl.clientHeight; }
function ndcBounds(cam, pts) { let a = 9, b = -9, c = 9, d = -9; for (const p of pts) { const n = p.clone().project(cam); a = Math.min(a, n.x); b = Math.max(b, n.x); c = Math.min(c, n.y); d = Math.max(d, n.y); } return [a, b, c, d]; }
function fitOverview(az, el, margin = Number(q.get('margin') ?? 0.06)) {
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
const OV = { az: Number(q.get('az') ?? -62), el: Number(q.get('el') ?? 67) };
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
  { const k = 1 - 0.3 * p.fade; L.hemi.intensity = Number(q.get('hemi') ?? 2.6) * k; L.sun.intensity = Number(q.get('sun') ?? 1.6) * (1 - 0.22 * p.fade); // the close-ups are lit a little lower so no wall clips to pure white
    if (S.mode === 'xray') mat.wall.color.setRGB(0.80 - 0.16 * p.fade, 0.84 - 0.15 * p.fade, 0.88 - 0.14 * p.fade); }
  const d = camera.position.distanceTo(controls.target), px = (2 * d * Math.tan((camera.fov * Math.PI) / 360)) / stageEl.clientHeight, rc = Math.max(0.004, Math.min(0.03, ((4.6 + 0.4 * p.fade) / 2) * px));
  UR.core.value = rc - RB.core; UR.halo.value = 3 * rc - RB.halo;
  const tr = p.fade > 0.001; for (const m of [floorWhite, deckMat]) if (m.transparent !== tr) { m.transparent = tr; m.needsUpdate = true; } // the OPAQUE shader define follows this flag, so the program must be rebuilt
  labelsGroup.visible = S.mode === 'xray' && p.fade < 0.5 && q.get('labels') === '1'; markersEl.style.visibility = p.fade < 0.5 && S.mode === 'xray' ? 'visible' : 'hidden';
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
function closeupPose(id, o = {}) {
  const p = PARTS[id], az = o.az ?? p.view.az, el = o.el ?? 36, d = o.d ?? 3.6, fov = o.fov ?? 40, a = V(...p.anchor), dir = dirOf(az, el);
  const cam = new THREE.PerspectiveCamera(fov, aspect(), 0.3, 100), th = Math.tan((fov * Math.PI) / 360), t = a.clone().add(new THREE.Vector3(...(o.aim || [0, 0, 0])).multiplyScalar(M));
  for (let it = 0; it < 3; it++) { cam.position.copy(t).addScaledVector(dir, d); cam.lookAt(t); cam.updateMatrixWorld(); cam.updateProjectionMatrix(); const up = new THREE.Vector3().setFromMatrixColumn(cam.matrixWorld, 1), an = a.clone().project(cam); t.addScaledVector(up, (an.y - (o.ndcY ?? 0.14)) * d * th); }
  return { pos: t.clone().addScaledVector(dir, d), tgt: t, fov, fade: 1 };
}
function bench(n = 120) { // wall time of n frames orbiting, with a one-pixel read-back so the GPU has really finished: render work as this machine sees it
  const gl = renderer.getContext(), px = new Uint8Array(4), cpu = [], all = [], dx0 = camera.position.x - controls.target.x, dz0 = camera.position.z - controls.target.z;
  for (let i = 0; i < n; i++) {
    const a = (i / n) * 0.6; camera.position.x = controls.target.x + dx0 * Math.cos(a) - dz0 * Math.sin(a); camera.position.z = controls.target.z + dx0 * Math.sin(a) + dz0 * Math.cos(a); camera.lookAt(controls.target);
    const t0 = performance.now(); renderer.render(scene, camera); const t1 = performance.now(); gl.readPixels(0, 0, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, px); const t2 = performance.now(); cpu.push(t1 - t0); all.push(t2 - t0);
  }
  const st = (v) => { const w = [...v].sort((x, y) => x - y); return { mean: Math.round((w.reduce((x, y) => x + y, 0) / w.length) * 100) / 100, median: Math.round(w[w.length >> 1] * 100) / 100, p95: Math.round(w[Math.floor(w.length * 0.95)] * 100) / 100, max: Math.round(w[w.length - 1] * 100) / 100 }; };
  return { frames: n, cpuSubmitMs: st(cpu), withGpuSyncMs: st(all), ao: !!composer };
}
const api = {
  set, clusters: () => clusterOut(CLUSTERS), markers: (on = true) => { markersEl.style.display = on ? 'block' : 'none'; const res = on ? clusterOut(placeMarkers()) : []; relayout(on); return res; }, bench,
  closeup(id, o = {}) { anim = null; setFocusId(id); const ps = closeupPose(id, o); applyPose(ps); return { dist: o.d ?? 3.6 }; }, jump: (o) => set(o, 0), parts: partsNow, rooms, audit, fill, film, filmLength: FILM.hold0 + FILM.fade + FILM.pause + FILM.fly + FILM.hold1,
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
new ResizeObserver(() => { overview = fitOverview(OV.az, OV.el); if (composer) composer.setSize(stageEl.clientWidth, stageEl.clientHeight); if (!anim) applyPose(posePair(S.focus)); }).observe(stageEl);

// ---- gate look: labels, ambient occlusion, exclusions ----
{
  hideForAO.push(runsRoot, labelsGroup, boilerDisc, PARTS.acLiving.halo, PARTS.acBed.halo);
  if (AO_ON) {
    const [{ EffectComposer }, { RenderPass }, { GTAOPass }, { OutputPass }] = AO_MODS, W = stageEl.clientWidth, H = stageEl.clientHeight, pr = renderer.getPixelRatio();
    const rt = new THREE.WebGLRenderTarget(W * pr, H * pr, { type: THREE.HalfFloatType, samples: 4 });
    composer = new EffectComposer(renderer, rt); composer.setPixelRatio(pr); composer.setSize(W, H);
    composer.addPass(new RenderPass(scene, camera));
    const gtao = new GTAOPass(scene, camera, W, H);
    gtao.updateGtaoMaterial({ radius: Number(q.get('aor') ?? 0.45), distanceExponent: 1.4, thickness: 1.2, scale: Number(q.get('aos') ?? 1.6), samples: 12, distanceFallOff: 1, screenSpaceRadius: false });
    gtao.updatePdMaterial({ lumaPhi: 10, depthPhi: 2, normalPhi: 3, radius: 6, radiusExponent: 1, rings: 2, samples: 12 }); gtao.blendIntensity = Number(q.get('aoi') ?? 1);
    composer.addPass(gtao); composer.addPass(new OutputPass()); api.gtao = gtao;
  }
}
// first state from the URL: ?mode=xray&layer=w&focus=boiler  (instant)
{
  const m = q.get('mode') || 'normal', l = q.get('layer') || 'all', f = q.get('focus');
  S.mode = m === 'xray' ? 'xray' : 'normal'; S.layer = ['all', 'w', 'e', 'g', 'ac'].includes(l) ? l : 'all'; setFocusId(f && PARTS[f] ? f : null);
  applyMode(); applyPose(posePair(S.focus));
  if (q.get('markers') === '1') api.markers(true); else relayout(false);
}
window.__xrayReady = true;
