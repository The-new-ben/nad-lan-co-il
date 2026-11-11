// The live 3D view of the apartment designer (HAD-701; first proven as the HAD-703 spike): three.js meshes built from the SAME derived model the plan draws.
// Frame: X = plan x, Z = plan y, Y up, metres. Renders on demand only (a still picture costs no battery).
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const M = 0.01, CUT = 118, EYE = 160;

function rnd(seed) { let s = seed; return () => ((s = (s * 16807) % 2147483647) - 1) / 2147483646; }
function texture(f) {
  const c = document.createElement('canvas'); c.width = c.height = 256; const x = c.getContext('2d'), r = rnd(f.size * 7 + f.tex.length);
  x.fillStyle = f.a; x.fillRect(0, 0, 256, 256);
  if (f.tex === 'tile') { x.strokeStyle = f.b; x.lineWidth = 3; x.strokeRect(0, 0, 256, 256); for (let i = 0; i < 900; i++) { x.fillStyle = 'rgba(255,255,255,' + r() * 0.05 + ')'; x.fillRect(r() * 256, r() * 256, 2, 2); } }
  if (f.tex === 'wood') for (let row = 0; row < 8; row++) {
    let px = -r() * 120;
    while (px < 256) { const len = 90 + r() * 110; x.fillStyle = 'rgba(' + (r() < 0.5 ? '0,0,0,' : '255,235,200,') + r() * 0.12 + ')'; x.fillRect(px, row * 32, len, 32); x.fillStyle = f.b; x.fillRect(px + len - 1, row * 32, 1.5, 32); px += len; }
    x.fillStyle = f.b; x.fillRect(0, row * 32, 256, 1.2);
  }
  if (f.tex === 'terrazzo') for (let i = 0; i < 420; i++) { x.fillStyle = [f.b, '#A9773F', '#F4F1EA', '#3D4A55'][i % 4]; x.beginPath(); x.ellipse(r() * 256, r() * 256, 1 + r() * 4, 1 + r() * 2.5, r() * 3, 0, 7); x.fill(); }
  if (f.tex === 'deck') for (let i = 0; i < 8; i++) { x.fillStyle = f.b; x.fillRect(0, i * 32, 256, 2); }
  const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.colorSpace = THREE.SRGBColorSpace; t.repeat.set(100 / f.size, 100 / f.size); t.anisotropy = 4;
  return t;
}

export function mountSpace(host, store, cat, hooks = {}) {
  const apt = store.apt, H = apt.levels[0].height;
  const xs = Object.values(apt.nodes).map((p) => p[0]), ys = Object.values(apt.nodes).map((p) => p[1]);
  const mid = new THREE.Vector3(((Math.min(...xs) + Math.max(...xs)) / 2) * M, 0, ((Math.min(...ys) + Math.max(...ys)) / 2) * M);
  const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.outputColorSpace = THREE.SRGBColorSpace; renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.08;
  renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap; renderer.shadowMap.autoUpdate = false;
  host.appendChild(renderer.domElement);
  const scene = new THREE.Scene(); scene.background = new THREE.Color(0xE6ECF0);
  const camera = new THREE.PerspectiveCamera(38, 1, 0.1, 200);
  scene.add(new THREE.HemisphereLight(0xffffff, 0xAEBBC6, 1.25));
  const sun = new THREE.DirectionalLight(0xFFF6E8, 2.4); sun.position.set(mid.x - 5, 13, mid.z - 9); sun.target.position.copy(mid); sun.castShadow = true;
  sun.shadow.mapSize.set(1024, 1024); Object.assign(sun.shadow.camera, { left: -11, right: 11, top: 11, bottom: -11, near: 1, far: 40 }); sun.shadow.bias = -0.0004; sun.shadow.normalBias = 0.03;
  scene.add(sun, sun.target);
  const ground = new THREE.Mesh(new THREE.PlaneGeometry(80, 80), new THREE.ShadowMaterial({ opacity: 0.16 })); ground.rotation.x = -Math.PI / 2; ground.position.set(mid.x, -0.02, mid.z); ground.receiveShadow = true; scene.add(ground);
  const gFloor = new THREE.Group(), gWall = new THREE.Group(), gItem = new THREE.Group(); scene.add(gFloor, gWall, gItem);
  const ceiling = new THREE.Mesh(new THREE.PlaneGeometry(40, 40), new THREE.MeshBasicMaterial({ color: 0xF4F5F3 })); ceiling.rotation.x = Math.PI / 2; ceiling.position.set(mid.x, H * M, mid.z); ceiling.visible = false; scene.add(ceiling);

  const mat = {
    wall: new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.93, vertexColors: true }),
    rail: new THREE.MeshStandardMaterial({ color: 0x9FB2C0, roughness: 0.4, transparent: true, opacity: 0.55 }),
    glass: new THREE.MeshStandardMaterial({ color: 0x8FBCE6, roughness: 0.08, transparent: true, opacity: 0.32 }),
    floors: {},
  };
  const floorMat = (key) => mat.floors[key] || (mat.floors[key] = new THREE.MeshStandardMaterial({ map: texture(cat.FINISHES[key]), roughness: cat.FINISHES[key].tex === 'wood' ? 0.62 : 0.42 }));
  const shade = (hex, rough = 0.85) => new THREE.MeshStandardMaterial({ color: hex, roughness: rough });
  const tone = { fabric: shade(0x5E7482), fabric2: shade(0x8FA2AD), wood: shade(0xA9825A, 0.6), white: shade(0xF1F1EE, 0.6), dark: shade(0x24323E, 0.5), linen: shade(0xE4E2DC), rug: shade(0xB9C3CA, 1), leaf: shade(0x4F7A5A), stone: shade(0xD7D9D6, 0.35) };

  let mode = 'doll', sel = null, dirty = true, pending = null, grow = 1, dead = false;
  const clear = (g) => { for (const c of [...g.children]) { g.remove(c); c.traverse((o) => o.geometry && o.geometry.dispose()); } };
  const touch = (shadow = true) => { dirty = true; if (shadow) renderer.shadowMap.needsUpdate = true; };

  const PAINT = new THREE.Color(0xF3F4F1), CAP = { ink: new THREE.Color(0x0F2233), free: new THREE.Color(0x1F5FA8), part: new THREE.Color(0x8799A6) };
  let acc = null; // the walls of one build, gathered into a single mesh: one draw call instead of hundreds
  function box(w, s0, s1, y0, y1, t, m) {
    if (s1 - s0 < 0.5 || y1 - y0 < 0.5) return;
    const g = new THREE.BoxGeometry((s1 - s0) * M, (y1 - y0) * M, t * M), c = (s0 + s1) / 2;
    const mx = new THREE.Matrix4().makeRotationY(-Math.atan2(w.dir[1], w.dir[0])).setPosition((w.pa[0] + w.dir[0] * c) * M, ((y0 + y1) / 2) * M, (w.pa[1] + w.dir[1] * c) * M);
    if (m === mat.glass || m === mat.rail) { const mesh = new THREE.Mesh(g, m); mesh.applyMatrix4(mx); gWall.add(mesh); return; }
    g.applyMatrix4(mx);
    const P = g.attributes.position.array, N = g.attributes.normal.array, I = g.index.array, base = acc.pos.length / 3;
    for (let i = 0; i < P.length; i += 3) { const col = m && i >= 24 && i < 36 ? m : PAINT; acc.pos.push(P[i], P[i + 1], P[i + 2]); acc.nor.push(N[i], N[i + 1], N[i + 2]); acc.col.push(col.r, col.g, col.b); } // vertices 8..11 are the top face
    for (let i = 0; i < I.length; i++) acc.idx.push(I[i] + base);
    g.dispose();
  }
  function buildWalls() {
    clear(gWall); acc = { pos: [], nor: [], col: [], idx: [] };
    const top = mode === 'walk' ? H : CUT;
    for (const w of store.derived.walls) {
      if (w.kind === 'divider' || w.L < 1) continue;
      if (w.kind === 'rail') { box(w, 0, w.L, 0, Math.min(105, top), w.t, mat.rail); continue; }
      const t = Math.max(w.t, 4), e = t / 2;
      const m = mode === 'walk' ? null : store.slides(w.id) ? CAP.free : w.kind === 'partition' ? CAP.part : CAP.ink; // the cut top is drawn like the plan's ink
      let c = -e;
      for (const o of w.openings) {
        box(w, c, o.at, 0, top, t, m);
        if (o.sill > 0) box(w, o.at, o.at + o.w, 0, Math.min(o.sill, top), t, m);
        if (top > o.head) box(w, o.at, o.at + o.w, o.head, top, t, m);
        if (o.type !== 'door' && top > o.sill) box(w, o.at, o.at + o.w, o.sill, Math.min(o.head, top), 3, mat.glass);
        c = o.at + o.w;
      }
      box(w, c, w.L + e, 0, top, t, m);
    }
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(acc.pos, 3)); g.setAttribute('normal', new THREE.Float32BufferAttribute(acc.nor, 3)); g.setAttribute('color', new THREE.Float32BufferAttribute(acc.col, 3)); g.setIndex(acc.idx);
    const all = new THREE.Mesh(g, mat.wall); all.castShadow = all.receiveShadow = true; gWall.add(all);
    gWall.scale.y = grow;
  }
  function buildFloors() {
    clear(gFloor);
    for (const f of store.derived.faces) {
      if (!f.room) continue;
      const g = new THREE.ShapeGeometry(new THREE.Shape(f.poly.map((p) => new THREE.Vector2(p[0] * M, p[1] * M)))); g.rotateX(Math.PI / 2);
      const mesh = new THREE.Mesh(g, floorMat(store.floorOf(f.id))); mesh.material.side = THREE.DoubleSide; mesh.receiveShadow = true; mesh.userData.room = f.id; gFloor.add(mesh);
    }
  }
  const part = (g, w, h, d, x, y, z, m) => { const b = new THREE.Mesh(new THREE.BoxGeometry(w * M, h * M, d * M), m); b.position.set(x * M, (y + h / 2) * M, z * M); b.castShadow = b.receiveShadow = true; g.add(b); return b; };
  function furniture(c) { // real sizes, simple forms: the catalogue task replaces these with real models
    const g = new THREE.Group(), { w, d, h } = c;
    if (c.shape === 'sofa') { part(g, w, 40, d, 0, 0, 0, tone.fabric); part(g, w, h - 40, 22, 0, 40, -d / 2 + 11, tone.fabric); for (const s of [-1, 1]) part(g, 18, 22, d - 22, (s * (w - 18)) / 2, 40, 11, tone.fabric); part(g, w - 44, 12, d - 30, 0, 40, 12, tone.fabric2); }
    else if (c.shape === 'bed') { part(g, w, 28, d, 0, 0, 0, tone.wood); part(g, w - 6, 22, d - 8, 0, 28, 2, tone.white); part(g, w, 95, 8, 0, 0, -d / 2 + 4, tone.wood); part(g, w - 12, 5, d * 0.55, 0, 50, d * 0.2, tone.linen); for (const s of w > 130 ? [-1, 1] : [0]) part(g, 55, 10, 36, s * w * 0.24, 50, -d / 2 + 34, tone.white); }
    else if (c.shape === 'table') { part(g, w, 4, d, 0, h - 4, 0, tone.wood); for (const sx of [-1, 1]) for (const sz of [-1, 1]) part(g, 5, h - 4, 5, sx * (w / 2 - 8), 0, sz * (d / 2 - 8), tone.dark); }
    else if (c.shape === 'counter') { part(g, w, h - 4, d - 4, 0, 0, -2, tone.white); part(g, w + 2, 4, d, 0, h - 4, 0, tone.stone); part(g, w, 8, d - 10, 0, 0, -5, tone.dark); }
    else if (c.shape === 'rug') part(g, w, h, d, 0, 0, 0, tone.rug).castShadow = false;
    else if (c.shape === 'plant') { part(g, 34, 36, 34, 0, 0, 0, tone.stone); const l = new THREE.Mesh(new THREE.IcosahedronGeometry(0.36, 1), tone.leaf); l.position.y = 0.95; l.scale.y = 1.35; l.castShadow = true; g.add(l); }
    else part(g, w, h, d, 0, 0, 0, h > 150 ? tone.white : tone.wood);
    return g;
  }
  // ---- real furniture models: each replaces its true-size box when it arrives; a missing or broken file leaves the box ----
  let models = null; const glb = new Map();
  function loadModel(id) {
    if (!glb.has(id)) glb.set(id, import('three/addons/loaders/GLTFLoader.js').then(({ GLTFLoader }) => new Promise((res) => new GLTFLoader().load(models.base + models.by[id].file, (g) => res(g.scene), undefined, () => res(null)))));
    return glb.get(id);
  }
  function dress(itemId) {
    const it = store.item(itemId), g = itemObj.get(itemId), c = it && cat.ITEMS[it.sku];
    if (!models || !g || !c || !c.model || !models.by[c.model] || g.userData.model) return;
    g.userData.model = 'loading';
    loadModel(c.model).then((scene) => {
      if (dead || !scene || itemObj.get(itemId) !== g) { g.userData.model = scene ? g.userData.model : 'failed'; return; }
      const m = scene.clone(true), mm = models.by[c.model], fit = [c.w / mm.w, c.h / mm.h, c.d / mm.d];
      if (fit.some((f) => f < 0.75 || f > 1.3)) { g.userData.model = 'misfit'; return; } // never stretch a model far from its real shape: the true-size box stays
      m.scale.set(fit[0], fit[1], fit[2]);
      m.traverse((o) => { o.userData.item = itemId; if (o.isMesh) { o.castShadow = o.receiveShadow = true; } });
      for (const ch of [...g.children]) { g.remove(ch); if (ch.geometry) ch.geometry.dispose(); }
      g.add(m); g.userData.model = c.model; if (sel && sel.type === 'item') showSel(); touch();
    });
  }
  function useModels(base, list) { models = { base, by: Object.fromEntries(list.map((x) => [x.id, x])) }; for (const id of itemObj.keys()) dress(id); }
  const itemObj = new Map(), ring = new THREE.Box3Helper(new THREE.Box3(), 0x1F5FA8); ring.visible = false; scene.add(ring);
  function syncItem(id) {
    const it = store.item(id); let g = itemObj.get(id);
    if (!it) { if (g) { gItem.remove(g); itemObj.delete(id); } return; }
    if (!g) { g = furniture(cat.ITEMS[it.sku]); g.userData.item = id; g.traverse((o) => (o.userData.item = id)); gItem.add(g); itemObj.set(id, g); }
    g.position.set(it.x * M, 0, it.y * M); g.rotation.y = (-it.rot * Math.PI) / 180;
    dress(id);
  }
  function showSel() {
    const g = sel && sel.type === 'item' && itemObj.get(sel.id);
    ring.visible = !!g; if (g) ring.box.setFromObject(g).expandByScalar(0.03);
    for (const f of gFloor.children) f.material.emissive && f.material.emissive.setHex(0);
    gFloor.children.forEach((f) => { f.material = floorMat(store.floorOf(f.userData.room)); f.material.side = THREE.DoubleSide; });
    touch(false);
  }

  // ---- cameras: looking from above (orbit) and walking inside ----
  const controls = new OrbitControls(camera, renderer.domElement);
  controls.target.copy(mid); controls.enableDamping = true; controls.dampingFactor = 0.12; controls.maxPolarAngle = 1.28; controls.minDistance = 5; controls.maxDistance = 46; controls.enablePan = false;
  controls.addEventListener('change', () => touch(false));
  const walk = { x: 500, y: 790, yaw: Math.atan2(120 - 790, 250 - 500), pitch: -0.1, to: null }; // from the entrance, looking at the living room and its window
  function place() {
    if (mode !== 'walk') return;
    camera.position.set(walk.x * M, EYE * M, walk.y * M);
    camera.lookAt(camera.position.x + Math.cos(walk.yaw) * Math.cos(walk.pitch), camera.position.y + Math.sin(walk.pitch), camera.position.z + Math.sin(walk.yaw) * Math.cos(walk.pitch));
    touch(false);
  }
  function setMode(m) {
    mode = m; controls.enabled = m === 'doll'; ceiling.visible = m === 'walk'; camera.fov = m === 'walk' ? 72 : 38; camera.updateProjectionMatrix();
    if (m === 'doll') { // fit the whole apartment into the frame, whatever its shape
      const r = (Math.hypot(Math.max(...xs) - Math.min(...xs), Math.max(...ys) - Math.min(...ys)) * M) / 2, hv = (camera.fov * Math.PI) / 360, hh = Math.atan(Math.tan(hv) * camera.aspect), dist = (r / Math.sin(Math.min(hv, hh))) * 0.9;
      camera.position.set(mid.x + dist * 0.05, dist * 0.8, mid.z + dist * 0.6); controls.update();
    }
    buildWalls(); place(); touch();
  }
  function getView() {
    const dir = camera.getWorldDirection(new THREE.Vector3());
    return { mode, x: camera.position.x / M, y: camera.position.z / M, z: camera.position.y / M, yaw: Math.atan2(dir.z, dir.x), pitch: Math.asin(dir.y), fov: camera.fov, walk: mode === 'walk' };
  }
  function setView(v) { // the same handle the 360 tour gives the shared video room
    if (v.mode && v.mode !== mode) setMode(v.mode);
    if (mode === 'walk') { Object.assign(walk, { x: v.x, y: v.y, yaw: v.yaw, pitch: v.pitch || 0 }); place(); }
    else { camera.position.set(v.x * M, v.z * M, v.y * M); controls.update(); touch(false); }
  }

  // ---- pointer: tap selects, drag moves a piece on the floor, in walk mode a tap on the floor walks there ----
  const ray = new THREE.Raycaster(), floorPlane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0), v2 = new THREE.Vector2(), hit3 = new THREE.Vector3();
  const aim = (ev) => { const r = renderer.domElement.getBoundingClientRect(); v2.set(((ev.clientX - r.left) / r.width) * 2 - 1, -((ev.clientY - r.top) / r.height) * 2 + 1); ray.setFromCamera(v2, camera); };
  const onFloor = (ev) => { aim(ev); return ray.ray.intersectPlane(floorPlane, hit3) ? [hit3.x / M, hit3.z / M] : null; };
  let down = null;
  renderer.domElement.addEventListener('pointerdown', (ev) => {
    aim(ev);
    const h = ray.intersectObjects(gItem.children, true)[0], p = onFloor(ev);
    down = { x: ev.clientX, y: ev.clientY, moved: false, item: h ? h.object.userData.item : null, yaw: walk.yaw, pitch: walk.pitch };
    if (down.item && mode === 'doll' && p) {
      const it = store.item(down.item); controls.enabled = false; try { renderer.domElement.setPointerCapture(ev.pointerId); } catch (e) { /* synthetic pointer */ }
      down.off = [it.x - p[0], it.y - p[1]]; down.g = 'g' + Date.now(); hooks.select && hooks.select({ type: 'item', id: it.id });
    }
  });
  renderer.domElement.addEventListener('pointermove', (ev) => {
    if (!down) return;
    if (Math.hypot(ev.clientX - down.x, ev.clientY - down.y) > 6) down.moved = true;
    if (down.off) { const p = onFloor(ev); if (p) store.apply({ op: 'item.move', id: down.item, x: Math.round((p[0] + down.off[0]) / 5) * 5, y: Math.round((p[1] + down.off[1]) / 5) * 5 }, { gesture: down.g }); }
    else if (mode === 'walk' && down.moved) { walk.yaw = down.yaw - (ev.clientX - down.x) * 0.005; walk.pitch = Math.max(-1, Math.min(1, down.pitch + (ev.clientY - down.y) * 0.004)); place(); }
  });
  const up = (ev) => {
    if (!down) return;
    if (!down.moved && !down.off) {
      aim(ev);
      const f = ray.intersectObjects(gFloor.children, false)[0];
      if (down.item) hooks.select && hooks.select({ type: 'item', id: down.item });
      else if (f && mode === 'walk') walk.to = { x: f.point.x / M, y: f.point.z / M };
      else hooks.select && hooks.select(f ? { type: 'room', id: f.object.userData.room } : null);
    }
    if (down.off) controls.enabled = mode === 'doll';
    down = null;
  };
  renderer.domElement.addEventListener('pointerup', up); renderer.domElement.addEventListener('pointercancel', up);

  function size() { const w = host.clientWidth, h = host.clientHeight; if (!w || !h) return; renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix(); touch(false); }
  const ro = new ResizeObserver(size); ro.observe(host);

  // walking stops at a wall and passes only through a door, an opening or the balcony door
  function blockedStep(x0, y0, x1, y1) {
    for (const w of store.derived.walls) {
      if (w.kind === 'divider') continue;
      const rx = x1 - x0, ry = y1 - y0, sx = w.pb[0] - w.pa[0], sy = w.pb[1] - w.pa[1], den = rx * sy - ry * sx;
      if (Math.abs(den) < 1e-9) continue;
      const t = ((w.pa[0] - x0) * sy - (w.pa[1] - y0) * sx) / den, u = ((w.pa[0] - x0) * ry - (w.pa[1] - y0) * rx) / den;
      if (t < 0 || t > 1 || u < 0 || u > 1) continue;
      const at = u * w.L;
      if (!w.openings.some((o) => o.type !== 'window' && at > o.at + 12 && at < o.at + o.w - 12)) return true;
    }
    return false;
  }
  const renders = [];
  let lastCam = '';
  function tick() {
    if (dead) return;
    requestAnimationFrame(tick);
    if (grow < 1) { grow = Math.min(1, grow + 0.035); gWall.scale.y = 1 - Math.pow(1 - grow, 3); touch(); } // the plan stands up
    if (walk.to && mode === 'walk') {
      const dx = walk.to.x - walk.x, dy = walk.to.y - walk.y, l = Math.hypot(dx, dy), nx = walk.x + (dx / (l || 1)) * Math.min(l, 9), ny = walk.y + (dy / (l || 1)) * Math.min(l, 9);
      if (l < 6 || blockedStep(walk.x, walk.y, nx, ny)) walk.to = null; else { walk.x = nx; walk.y = ny; }
      place();
    }
    if (controls.enabled) controls.update();
    if (!dirty) return;
    dirty = false; const r0 = performance.now(); renderer.render(scene, camera); const rms = performance.now() - r0;
    renders.push(rms); if (renders.length > 300) renders.shift();
    if (pending != null) { const dt = performance.now() - pending; pending = null; hooks.frame && hooks.frame(dt, rms); }
    const v = getView(), k = v.x.toFixed(0) + v.y.toFixed(0) + v.yaw.toFixed(2);
    if (k !== lastCam) { lastCam = k; hooks.camera && hooks.camera(v); }
  }

  store.on((e) => {
    if (e.type !== 'change') return;
    if (pending == null) pending = e.t0;
    if (e.touched.geometry) { buildWalls(); buildFloors(); }
    if (e.touched.finishes.length) showSel();
    for (const id of e.touched.items) syncItem(id);
    if (sel && sel.type === 'item') showSel();
    touch();
  });

  size(); buildFloors(); for (const it of store.design.items) syncItem(it.id);
  grow = 0.01; setMode('doll'); tick();
  return {
    el: renderer.domElement, setMode, getView, setView, get mode() { return mode; },
    setSelection(s) { sel = s; showSel(); },
    walkTo(p) { if (mode === 'walk') walk.to = { x: p[0], y: p[1] }; },
    // for checks: where a plan point lands on the screen, and where a piece really stands in the 3D scene
    screenOf(x, y, h = 0) { const v = new THREE.Vector3(x * M, h * M, y * M).project(camera), r = renderer.domElement.getBoundingClientRect(); return [r.left + ((v.x + 1) / 2) * r.width, r.top + ((1 - v.y) / 2) * r.height]; },
    placed(id) { const g = itemObj.get(id); return g ? [Math.round(g.position.x / M), Math.round(g.position.z / M), Math.round((-g.rotation.y * 180) / Math.PI)] : null; },
    floorKey(room) { const f = gFloor.children.find((c) => c.userData.room === room); return f ? Object.keys(mat.floors).find((k) => mat.floors[k] === f.material) : null; },
    renders, useModels,
    modelState: (id) => (itemObj.get(id) ? itemObj.get(id).userData.model || 'box' : null),
    destroy() { dead = true; ro.disconnect(); controls.dispose(); scene.traverse((o) => { if (o.geometry) o.geometry.dispose(); }); renderer.dispose(); renderer.domElement.remove(); },
    /** turns the camera around the apartment for ms and returns the time between frames (the device's real frame rate) */
    spin(ms) {
      return new Promise((done) => {
        const t0 = performance.now(), gaps = []; let last = t0; const r0 = renders.length;
        const step = (now) => {
          gaps.push(now - last); last = now;
          const a = 0.012, dx = camera.position.x - controls.target.x, dz = camera.position.z - controls.target.z;
          camera.position.x = controls.target.x + dx * Math.cos(a) - dz * Math.sin(a); camera.position.z = controls.target.z + dx * Math.sin(a) + dz * Math.cos(a);
          controls.update(); touch(false);
          if (now - t0 < ms) requestAnimationFrame(step); else done({ gaps: gaps.slice(1), renders: renders.slice(-Math.min(300, gaps.length)) });
        };
        requestAnimationFrame(step);
      });
    },
    gl: () => { const g = renderer.getContext(), e = g.getExtension('WEBGL_debug_renderer_info'); return e ? g.getParameter(e.UNMASKED_RENDERER_WEBGL) : 'unknown'; },
    stats: () => ({ calls: renderer.info.render.calls, triangles: renderer.info.render.triangles, geometries: renderer.info.memory.geometries, textures: renderer.info.memory.textures }),
  };
}
