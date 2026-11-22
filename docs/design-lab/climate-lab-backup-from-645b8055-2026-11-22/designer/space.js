// The live 3D view of the apartment designer (HAD-701; first proven as the HAD-703 spike): three.js meshes built from the SAME derived model the plan draws.
// Frame: X = plan x, Z = plan y, Y up, metres. Renders on demand only (a still picture costs no battery).
// HAD-792 (19.11.2026, gaps 4, 15, 17): real floors (wood grain, stone, grout in relief), daylight with soft shadows and an
// image-based light, a paint colour per room, window and door frames and door leaves, a sky and a distant city in the window
// (labelled as an illustration), the walls RISE out of the plan, and the walk goes through doors to any room and always
// stops looking at the room, never at a wall (walknav.js).
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { POINT_KINDS } from './core.js';
import { buildNav, route, bestYaw, roomSpot, startFace, tourOrder, nearestFree, ahead } from './walknav.js';

const M = 0.01, CUT = 118, EYE = 160;
const RISE_MS = 2300;

function rnd(seed) { let s = Math.abs(Math.floor(seed)) % 2147483646 || 7; return () => ((s = (s * 16807) % 2147483647) - 1) / 2147483646; }
const hexRGB = (h) => { const n = parseInt(String(h).slice(1), 16); return [(n >> 16) & 255, (n >> 8) & 255, n & 255]; };
const shadeHex = (h, k) => { const [r, g, b] = hexRGB(h); const c = (v) => Math.max(0, Math.min(255, Math.round(v * k))); return 'rgb(' + c(r) + ',' + c(g) + ',' + c(b) + ')'; };

/** a floor finish drawn on a canvas: colour map and a relief map (seams and grout lie lower) */
function texture(f) {
  const N = 512, c = document.createElement('canvas'), b = document.createElement('canvas'); c.width = c.height = b.width = b.height = N;
  const x = c.getContext('2d'), y = b.getContext('2d'), r = rnd(f.size * 7 + f.tex.length * 131 + f.a.length);
  x.fillStyle = f.a; x.fillRect(0, 0, N, N); y.fillStyle = '#c8c8c8'; y.fillRect(0, 0, N, N);
  if (f.tex === 'wood') {
    const rows = 6, rh = N / rows;
    for (let row = 0; row < rows; row++) {
      let px = -r() * N * 0.6;
      while (px < N) {
        const len = N * (0.45 + r() * 0.5), k = 0.86 + r() * 0.24;
        x.fillStyle = shadeHex(f.a, k); x.fillRect(px, row * rh, len, rh);
        for (let g = 0; g < 9; g++) { // the grain: long soft waves along the plank
          x.strokeStyle = 'rgba(' + (r() < 0.5 ? '40,25,10,' : '255,240,220,') + (0.05 + r() * 0.08) + ')'; x.lineWidth = 0.8 + r() * 1.6;
          const y0 = row * rh + r() * rh, amp = 1 + r() * 3, ph = r() * 6;
          x.beginPath(); for (let t = 0; t <= len; t += 8) x.lineTo(px + t, y0 + Math.sin(t / (30 + r() * 4) + ph) * amp); x.stroke();
        }
        if (r() < 0.35) { x.fillStyle = 'rgba(60,35,15,0.18)'; x.beginPath(); x.ellipse(px + r() * len, row * rh + rh / 2, 6 + r() * 6, 2.5 + r() * 2, 0, 0, 7); x.fill(); } // a knot
        x.fillStyle = f.b; x.fillRect(px + len - 1.5, row * rh, 2, rh); y.fillStyle = '#5a5a5a'; y.fillRect(px + len - 1.5, row * rh, 2, rh);
        px += len;
      }
      x.fillStyle = f.b; x.fillRect(0, row * rh, N, 1.6); y.fillStyle = '#5a5a5a'; y.fillRect(0, row * rh, N, 1.6);
    }
  } else if (f.tex === 'tile') {
    const img = x.getImageData(0, 0, N, N), d = img.data; // a quiet stone: grain plus a few soft veins
    for (let i = 0; i < d.length; i += 4) { const n = (r() - 0.5) * 9; d[i] += n; d[i + 1] += n; d[i + 2] += n; }
    x.putImageData(img, 0, 0);
    for (let v = 0; v < 5; v++) {
      x.strokeStyle = 'rgba(255,255,255,' + (0.12 + r() * 0.12) + ')'; x.lineWidth = 1 + r() * 2.5; x.beginPath();
      let px = r() * N, py = 0; x.moveTo(px, py); while (py < N) { px += (r() - 0.5) * 40; py += 20 + r() * 30; x.lineTo(px, py); } x.stroke();
    }
    x.strokeStyle = f.b; x.lineWidth = 5; x.strokeRect(0, 0, N, N); y.strokeStyle = '#505050'; y.lineWidth = 6; y.strokeRect(0, 0, N, N);
  } else if (f.tex === 'terrazzo') {
    for (let i = 0; i < 1600; i++) { x.fillStyle = [f.b, '#8A9AA6', '#F4F5F2', '#3D4A55', '#B7BEC2'][i % 5]; x.beginPath(); x.ellipse(r() * N, r() * N, 1.2 + r() * 6, 1 + r() * 4, r() * 3, 0, 7); x.fill(); }
  } else if (f.tex === 'deck') {
    for (let i = 0; i < 8; i++) {
      x.fillStyle = shadeHex(f.a, 0.9 + r() * 0.16); x.fillRect(0, i * 64 + 4, N, 60);
      x.fillStyle = f.b; x.fillRect(0, i * 64, N, 4); y.fillStyle = '#404040'; y.fillRect(0, i * 64, N, 4);
    }
  }
  const t = new THREE.CanvasTexture(c), bt = new THREE.CanvasTexture(b);
  for (const q of [t, bt]) { q.wrapS = q.wrapT = THREE.RepeatWrapping; q.repeat.set(100 / f.size, 100 / f.size); q.anisotropy = 8; }
  t.colorSpace = THREE.SRGBColorSpace;
  return { map: t, bump: bt };
}
function skyTexture(top, bottom, stops) {
  const c = document.createElement('canvas'); c.width = 4; c.height = 256; const x = c.getContext('2d'), g = x.createLinearGradient(0, 0, 0, 256);
  for (const [k, v] of stops || [[0, top], [1, bottom]]) g.addColorStop(k, v); x.fillStyle = g; x.fillRect(0, 0, 4, 256);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
}
/** the number on a builder's note, drawn as a red tag (the redline colour of a drawing) */
function noteTag(n) {
  const c = document.createElement('canvas'); c.width = c.height = 128; const x = c.getContext('2d');
  x.fillStyle = '#B5302A'; x.fillRect(14, 14, 100, 100); x.strokeStyle = '#ffffff'; x.lineWidth = 8; x.strokeRect(14, 14, 100, 100);
  x.fillStyle = '#ffffff'; x.font = '600 64px "IBM Plex Mono", monospace'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText(String(n), 64, 68);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
}

export function mountSpace(host, store, cat, hooks = {}) {
  const apt = store.apt, H = apt.levels[0].height;
  const xs = Object.values(apt.nodes).map((p) => p[0]), ys = Object.values(apt.nodes).map((p) => p[1]);
  const mid = new THREE.Vector3(((Math.min(...xs) + Math.max(...xs)) / 2) * M, 0, ((Math.min(...ys) + Math.max(...ys)) / 2) * M);
  const R = (Math.hypot(Math.max(...xs) - Math.min(...xs), Math.max(...ys) - Math.min(...ys)) * M) / 2;
  const reduce = typeof matchMedia === 'function' && matchMedia('(prefers-reduced-motion: reduce)').matches;
  const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.outputColorSpace = THREE.SRGBColorSpace; renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.0;
  renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap; renderer.shadowMap.autoUpdate = false;
  renderer.domElement.tabIndex = 0; renderer.domElement.style.outline = 'none';
  host.appendChild(renderer.domElement);
  const scene = new THREE.Scene();
  const bgDoll = skyTexture('#C9DCEA', '#EEF2F5'); let stage = null;
  const camera = new THREE.PerspectiveCamera(38, 1, 0.1, 400);
  const hemi = new THREE.HemisphereLight(0xEAF2FA, 0x9AA6AE, 0.55); scene.add(hemi);
  // the sun comes in from the side the apartment's windows face most (a guess from the plan, never a claim about the real building)
  const sunDir = (() => { let sx = 0, sy = 0; for (const w of store.derived.walls) for (const o of w.openings || []) if (o.type !== 'door') { const n = [-w.dir[1], w.dir[0]], c = [w.pa[0] + w.dir[0] * (o.at + o.w / 2) - mid.x / M, w.pa[1] + w.dir[1] * (o.at + o.w / 2) - mid.z / M]; const s = n[0] * c[0] + n[1] * c[1] > 0 ? 1 : -1; sx += n[0] * s * o.w; sy += n[1] * s * o.w; } const l = Math.hypot(sx, sy) || 1; return [sx / l || -0.5, sy / l || -0.8]; })();
  const sun = new THREE.DirectionalLight(0xFFF8EE, 2.7); sun.position.set(mid.x + sunDir[0] * 9, 11, mid.z + sunDir[1] * 9); sun.target.position.copy(mid); sun.castShadow = true;
  sun.shadow.mapSize.set(2048, 2048); Object.assign(sun.shadow.camera, { left: -R - 2, right: R + 2, top: R + 2, bottom: -R - 2, near: 1, far: 50 }); sun.shadow.bias = -0.0004; sun.shadow.normalBias = 0.03; sun.shadow.radius = 4;
  scene.add(sun, sun.target);
  const ground = new THREE.Mesh(new THREE.PlaneGeometry(80, 80), new THREE.ShadowMaterial({ opacity: 0.18 })); ground.rotation.x = -Math.PI / 2; ground.position.set(mid.x, -0.02, mid.z); ground.receiveShadow = true; scene.add(ground);
  const gFloor = new THREE.Group(), gWall = new THREE.Group(), gGlass = new THREE.Group(), gItem = new THREE.Group(), gPoint = new THREE.Group(), gNote = new THREE.Group();
  scene.add(gFloor, gWall, gGlass, gItem, gPoint, gNote);
  const ceiling = new THREE.Mesh(new THREE.PlaneGeometry(40, 40), new THREE.MeshStandardMaterial({ color: 0xF3F5F4, roughness: 0.95 })); ceiling.rotation.x = Math.PI / 2; ceiling.position.set(mid.x, H * M, mid.z); ceiling.visible = false; scene.add(ceiling);

  // ---- outside the window (walk view only): a sky and a quiet, distant city, an illustration and labelled as one by the page ----
  const outside = new THREE.Group(); outside.visible = false; scene.add(outside);
  {
    const dome = new THREE.Mesh(new THREE.SphereGeometry(180, 32, 16), new THREE.MeshBasicMaterial({ map: skyTexture(0, 0, [[0, '#4F8CC4'], [0.36, '#9CC2E2'], [0.47, '#DCE9F3'], [0.5, '#EEF3F6'], [0.53, '#B9C4CB'], [1, '#8E9AA2']]), side: THREE.BackSide, fog: false, depthWrite: false }));
    dome.position.copy(mid); dome.position.y = -40; outside.add(dome);
    const low = -26, rr = rnd(97), city = new THREE.Group();
    const towerMat = [0xA9B6C0, 0xBCC7CF, 0x9AA8B3, 0xC6CFD5].map((c) => new THREE.MeshStandardMaterial({ color: c, roughness: 0.85, envMapIntensity: 0.4 }));
    const winMat = new THREE.MeshStandardMaterial({ color: 0x7E95A8, roughness: 0.3, envMapIntensity: 0.8 });
    for (let i = 0; i < 90; i++) {
      const a = rr() * Math.PI * 2, d = 45 + rr() * 85, w = 8 + rr() * 16, h = 10 + rr() * (d < 70 ? 40 : 70), dd = 8 + rr() * 14;
      const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, dd), rr() < 0.25 ? winMat : towerMat[i % 4]);
      m.position.set(mid.x + Math.cos(a) * d, low + h / 2, mid.z + Math.sin(a) * d); m.rotation.y = rr() * Math.PI; city.add(m);
    }
    const land = new THREE.Mesh(new THREE.CircleGeometry(170, 48), new THREE.MeshStandardMaterial({ color: 0x9FAAA0, roughness: 1 }));
    land.rotation.x = -Math.PI / 2; land.position.set(mid.x, low, mid.z); outside.add(city, land);
    scene.fog = null;
  }
  // an image-based light (a neutral studio room from three's examples) gives the floors and the glass something to reflect
  import('three/addons/environments/RoomEnvironment.js').then(({ RoomEnvironment }) => {
    if (dead) return;
    const pm = new THREE.PMREMGenerator(renderer); scene.environment = pm.fromScene(new RoomEnvironment(), 0.04).texture; scene.environmentIntensity = 0.5; pm.dispose(); touch();
  }).catch(() => { /* the lights alone still draw a good picture */ });

  const riseU = { value: 1 };
  const riseShader = (sh) => {
    sh.uniforms.uRise = riseU;
    sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\nattribute float aDelay;\nuniform float uRise;')
      .replace('#include <begin_vertex>', '#include <begin_vertex>\nfloat rk = clamp((uRise - aDelay) / 0.42, 0.0, 1.0); rk = 1.0 - pow(1.0 - rk, 3.0); transformed.y *= max(rk, 0.012);');
  };
  const mat = {
    wall: new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.9, vertexColors: true, envMapIntensity: 0.35 }),
    rail: new THREE.MeshStandardMaterial({ color: 0x9FB2C0, roughness: 0.25, metalness: 0.2, transparent: true, opacity: 0.5 }),
    glass: new THREE.MeshStandardMaterial({ color: 0xD8EAF5, roughness: 0.05, metalness: 0, transparent: true, opacity: 0.07, envMapIntensity: 0.35, depthWrite: false }),
    floors: {},
  };
  mat.wall.onBeforeCompile = riseShader;
  const wallDepth = new THREE.MeshDepthMaterial({ depthPacking: THREE.RGBADepthPacking }); wallDepth.onBeforeCompile = riseShader;
  const floorMat = (key) => {
    if (mat.floors[key]) return mat.floors[key];
    const f = cat.FINISHES[key] || cat.FINISHES['porcelain-80'], tx = texture(f);
    return (mat.floors[key] = new THREE.MeshStandardMaterial({ map: tx.map, bumpMap: tx.bump, bumpScale: f.tex === 'wood' ? 1.2 : 2, roughness: f.tex === 'wood' ? 0.55 : f.tex === 'deck' ? 0.8 : 0.24, envMapIntensity: f.tex === 'wood' ? 0.5 : 0.9, side: THREE.DoubleSide }));
  };
  const shade = (hex, rough = 0.85, extra = {}) => new THREE.MeshStandardMaterial({ color: hex, roughness: rough, envMapIntensity: 0.5, ...extra });
  const tone = { fabric: shade(0x55697A, 0.95), fabric2: shade(0x8A9CA8, 0.95), wood: shade(0xA67C52, 0.55), white: shade(0xF1F2F0, 0.5), dark: shade(0x222D36, 0.45, { metalness: 0.3 }), linen: shade(0xE3E6E8, 0.95), rug: shade(0xAEB9C1, 1), leaf: shade(0x3F6E4C, 0.8), stone: shade(0xDADDDB, 0.22) };

  let mode = 'doll', sel = null, dirty = true, pending = null, dead = false;
  const clear = (g) => { for (const c of [...g.children]) { g.remove(c); c.traverse((o) => o.geometry && o.geometry.dispose()); } };
  const touch = (shadow = true) => { dirty = true; if (shadow) renderer.shadowMap.needsUpdate = true; };

  const PAINT = '#EEF0EE', CAP = { ink: new THREE.Color(0x0F2233), free: new THREE.Color(0x1F5FA8), part: new THREE.Color(0x8799A6) };
  const FRAME = new THREE.Color(0x3A444D), JAMB = new THREE.Color(0xDDE2E5), LEAF = new THREE.Color(0xE8EBED);
  const paintOf = (room) => { const k = room && store.wallOf ? store.wallOf(room) : null; return (k && cat.WALLS && cat.WALLS[k] && cat.WALLS[k].hex) || PAINT; };
  const colorCache = new Map(); const col = (hex) => { if (!colorCache.has(hex)) colorCache.set(hex, new THREE.Color(hex)); return colorCache.get(hex); };
  let acc = null; // the walls of one build, gathered into a single mesh: one draw call instead of hundreds
  /** one box along wall w between s0 and s1 (cm along it), from y0 to y1. o.cap = colour of the cut top, o.all = one colour everywhere */
  function box(w, s0, s1, y0, y1, t, o = {}) {
    if (s1 - s0 < 0.5 || y1 - y0 < 0.5) return;
    const g = new THREE.BoxGeometry((s1 - s0) * M, (y1 - y0) * M, t * M), c = (s0 + s1) / 2;
    const cx = w.pa[0] + w.dir[0] * c, cy = w.pa[1] + w.dir[1] * c;
    const mx = new THREE.Matrix4().makeRotationY(-Math.atan2(w.dir[1], w.dir[0])).setPosition(cx * M, ((y0 + y1) / 2) * M, cy * M);
    if (o.mat) { const mesh = new THREE.Mesh(g, o.mat); mesh.applyMatrix4(mx); if (o.mat !== mat.glass) mesh.castShadow = true; gGlass.add(mesh); return; }
    g.applyMatrix4(mx);
    const P = g.attributes.position.array, Nn = g.attributes.normal.array, I = g.index.array, base = acc.pos.length / 3;
    const delay = Math.min(0.55, (Math.hypot(cx * M - mid.x, cy * M - mid.z) / (R || 1)) * 0.55); // the walls rise from the middle outwards
    const faceCol = [];
    for (let f = 0; f < 6; f++) { // per face of the box: the cut top in ink, the two long sides in the paint of the room they face
      let cc = null;
      if (o.all) cc = o.all;
      else if (f === 2) cc = o.cap || null;
      if (!cc && (f === 4 || f === 5 || f === 0 || f === 1)) {
        const v = f * 4 * 3, nx = Nn[v], nz = Nn[v + 2];
        let px = 0, pz = 0; for (let k = 0; k < 4; k++) { px += P[v + k * 3]; pz += P[v + k * 3 + 2]; }
        const room = store.roomAt((px / 4 + nx * 0.14) / M, (pz / 4 + nz * 0.14) / M);
        cc = col(paintOf(room));
      }
      faceCol.push(cc || col(PAINT));
    }
    for (let i = 0; i < P.length; i += 3) {
      const f = Math.floor(i / 12), cc = faceCol[f], yy = P[i + 1] / M;
      const ao = f === 2 || o.all ? 1 : 0.8 + 0.2 * Math.min(1, yy / 90); // darker where the wall meets the floor
      acc.pos.push(P[i], P[i + 1], P[i + 2]); acc.nor.push(Nn[i], Nn[i + 1], Nn[i + 2]); acc.col.push(cc.r * ao, cc.g * ao, cc.b * ao); acc.del.push(delay);
    }
    for (let i = 0; i < I.length; i++) acc.idx.push(I[i] + base);
    g.dispose();
  }
  function buildWalls() {
    clear(gWall); clear(gGlass); acc = { pos: [], nor: [], col: [], idx: [], del: [] };
    const top = mode === 'walk' ? H : CUT;
    for (const w of store.derived.walls) {
      if (w.kind === 'divider' || w.L < 1) continue;
      if (w.kind === 'rail') { box(w, 0, w.L, 0, Math.min(105, top), w.t, { mat: mat.rail }); continue; }
      const t = Math.max(w.t, 4), e = t / 2;
      const cap = mode === 'walk' ? null : store.slides(w.id) || w.added ? CAP.free : w.kind === 'partition' ? CAP.part : CAP.ink; // the cut top is drawn like the plan's ink
      let c = -e;
      for (const o of [...w.openings].sort((a, b) => a.at - b.at)) {
        box(w, c, o.at, 0, top, t, { cap });
        if (o.sill > 0) box(w, o.at, o.at + o.w, 0, Math.min(o.sill, top), t, { cap });
        if (top > o.head) box(w, o.at, o.at + o.w, o.head, top, t, { cap });
        const hd = Math.min(o.head, top);
        if (o.type !== 'door') { // a window or a balcony door: aluminium frame and glass
          if (top > o.sill) box(w, o.at + 4, o.at + o.w - 4, o.sill + 4, hd - 4, 2, { mat: mat.glass });
          box(w, o.at, o.at + 5, o.sill, hd, t * 0.55, { all: FRAME }); box(w, o.at + o.w - 5, o.at + o.w, o.sill, hd, t * 0.55, { all: FRAME });
          if (o.sill > 0) box(w, o.at, o.at + o.w, o.sill, o.sill + 5, t * 0.7, { all: FRAME });
          if (top >= o.head) box(w, o.at, o.at + o.w, o.head - 5, o.head, t * 0.55, { all: FRAME });
          if (o.type === 'slider' && o.w > 140) box(w, o.at + o.w / 2 - 3, o.at + o.w / 2 + 3, o.sill, hd, t * 0.5, { all: FRAME });
        } else { // a door: a light frame, and the leaf standing open the way the plan draws its swing
          box(w, o.at - 2, o.at + 3, 0, hd, t + 2, { all: JAMB }); box(w, o.at + o.w - 3, o.at + o.w + 2, 0, hd, t + 2, { all: JAMB });
          if (top >= o.head) box(w, o.at - 2, o.at + o.w + 2, o.head - 4, o.head, t + 2, { all: JAMB });
          const n = [-w.dir[1], w.dir[0]], s = o.swing || 1, p0 = [w.pa[0] + w.dir[0] * (o.at + 3), w.pa[1] + w.dir[1] * (o.at + 3)];
          box({ pa: [p0[0] + n[0] * s * (t / 2), p0[1] + n[1] * s * (t / 2)], dir: [n[0] * s, n[1] * s] }, 0, o.w - 6, 1, Math.min(hd - 2, top), 4, { all: LEAF });
        }
        c = o.at + o.w;
      }
      box(w, c, w.L + e, 0, top, t, { cap });
    }
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(acc.pos, 3)); g.setAttribute('normal', new THREE.Float32BufferAttribute(acc.nor, 3)); g.setAttribute('color', new THREE.Float32BufferAttribute(acc.col, 3));
    g.setAttribute('aDelay', new THREE.Float32BufferAttribute(acc.del, 1)); g.setIndex(acc.idx);
    const all = new THREE.Mesh(g, mat.wall); all.castShadow = all.receiveShadow = true; all.customDepthMaterial = wallDepth; gWall.add(all);
    gGlass.scale.y = riseEase();
  }
  const riseEase = () => { const k = Math.max(0, Math.min(1, (riseU.value - 0.3) / 0.6)); return Math.max(0.012, 1 - Math.pow(1 - k, 3)); };
  // ---- services points: small plates on the wall face at their height, lights as discs on the ceiling (walk view only).
  const PG = {
    socket: new THREE.BoxGeometry(8 * M, 8 * M, 1.4 * M), switch: new THREE.BoxGeometry(8 * M, 8 * M, 1.4 * M), data: new THREE.BoxGeometry(8 * M, 8 * M, 1.4 * M),
    tv: new THREE.BoxGeometry(12 * M, 8 * M, 1.4 * M), ac: new THREE.BoxGeometry(80 * M, 28 * M, 20 * M), light: new THREE.CylinderGeometry(9 * M, 9 * M, 1.5 * M, 20),
  };
  const PM = { base: new THREE.MeshStandardMaterial({ color: 0x0F2233, roughness: 0.6 }), mine: new THREE.MeshStandardMaterial({ color: 0x1F5FA8, roughness: 0.5 }), on: new THREE.MeshStandardMaterial({ color: 0x1F5FA8, emissive: 0x1F5FA8, emissiveIntensity: 0.7, roughness: 0.4 }), lamp: new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: 0xFFF6E6, emissiveIntensity: 1.2 }) };
  function buildPoints() {
    for (const c of [...gPoint.children]) gPoint.remove(c); // the geometries are shared: nothing to dispose
    for (const p of store.derived.points) {
      if (p.state === 'removed' || p.lost) continue;
      const ceil = POINT_KINDS[p.kind].ceiling, on = sel && sel.type === 'point' && sel.id === p.id;
      if (ceil ? mode !== 'walk' : mode !== 'walk' && p.h >= CUT) continue; // from above the walls are cut at 118 cm
      const m = new THREE.Mesh(PG[p.kind], on ? PM.on : ceil && mode === 'walk' ? PM.lamp : p.state === 'base' ? PM.base : PM.mine);
      if (ceil) m.position.set(p.x * M, (H - 1) * M, p.y * M);
      else { const out = p.kind === 'ac' ? 10.5 : 0.8; m.position.set((p.fx + p.ns[0] * out) * M, p.h * M, (p.fy + p.ns[1] * out) * M); m.rotation.y = Math.atan2(p.ns[0], p.ns[1]); }
      if (on) m.scale.setScalar(1.6);
      m.userData.point = p.id; gPoint.add(m);
    }
    gPoint.scale.y = riseEase();
  }
  function buildFloors() {
    clear(gFloor);
    for (const f of store.derived.faces) {
      if (!f.room) continue;
      const g = new THREE.ShapeGeometry(new THREE.Shape(f.poly.map((p) => new THREE.Vector2(p[0] * M, p[1] * M)))); g.rotateX(Math.PI / 2);
      const mesh = new THREE.Mesh(g, floorMat(store.floorOf(f.id))); mesh.receiveShadow = true; mesh.userData.room = f.id; gFloor.add(mesh);
    }
  }
  // ---- builder's notes: a red numbered tag standing over the place (HAD-792, gap 16) ----
  const tags = new Map();
  function buildNotes() {
    for (const c of [...gNote.children]) gNote.remove(c);
    (store.design.notes || []).forEach((n, i) => {
      let tx = tags.get(i + 1); if (!tx) { tx = noteTag(i + 1); tags.set(i + 1, tx); }
      const on = sel && sel.type === 'note' && sel.id === n.id;
      const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: tx, depthTest: mode !== 'walk', sizeAttenuation: true }));
      const k = mode === 'walk' ? 0.22 : 0.42; s.scale.set(k * (on ? 1.35 : 1), k * (on ? 1.35 : 1), 1);
      s.position.set(n.x * M, mode === 'walk' ? 1.45 : 1.55, n.y * M); s.userData.note = n.id; s.renderOrder = 10; gNote.add(s);
    });
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
    loadModel(c.model).then((sc) => {
      if (dead || !sc || itemObj.get(itemId) !== g) { g.userData.model = sc ? g.userData.model : 'failed'; return; }
      const m = sc.clone(true), mm = models.by[c.model], fit = [c.w / mm.w, c.h / mm.h, c.d / mm.d];
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
    gFloor.children.forEach((f) => { f.material = floorMat(store.floorOf(f.userData.room)); });
    touch(false);
  }
  function applyBg() {
    if (stage != null) { scene.background = new THREE.Color(stage); outside.visible = false; ground.visible = true; }
    else if (mode === 'walk') { scene.background = new THREE.Color(0xDCE8F1); outside.visible = true; ground.visible = false; }
    hemi.intensity = mode === 'walk' && stage == null ? 1.05 : 0.55; // inside, the light bounces off white walls and ceiling: a brighter fill
    if (scene.environment) scene.environmentIntensity = mode === 'walk' ? 0.75 : 0.5;
    else { scene.background = bgDoll; outside.visible = false; ground.visible = true; }
  }

  // ---- cameras: looking from above (orbit) and walking inside ----
  const controls = new OrbitControls(camera, renderer.domElement);
  controls.target.copy(mid); controls.enableDamping = true; controls.dampingFactor = 0.12; controls.maxPolarAngle = 1.28; controls.minDistance = 5; controls.maxDistance = 46; controls.enablePan = false;
  controls.addEventListener('change', () => touch(false));
  const walk = { x: mid.x / M, y: mid.z / M, yaw: 0, pitch: -0.08, path: null, turnTo: null, tour: null, placed: false, last: 0 };
  let nav = null, navRev = -1;
  const getNav = () => { if (!nav || navRev !== store.design.rev) { nav = buildNav(store.derived); navRev = store.design.rev; } return nav; };
  function place() {
    if (mode !== 'walk') return;
    camera.position.set(walk.x * M, EYE * M, walk.y * M);
    camera.lookAt(camera.position.x + Math.cos(walk.yaw) * Math.cos(walk.pitch), camera.position.y + Math.sin(walk.pitch), camera.position.z + Math.sin(walk.yaw) * Math.cos(walk.pitch));
    touch(false);
  }
  /** stand where the walk starts: the living room's open middle, looking at its window */
  function placeStart() {
    const n = getNav(); if (!n) return;
    const sf = startFace(n), p = sf >= 0 ? roomSpot(n, sf) : nearestFree(n, mid.x / M, mid.z / M);
    if (!p) return;
    walk.x = p[0]; walk.y = p[1]; walk.yaw = bestYaw(n, p); walk.pitch = -0.08; walk.placed = true; walk.path = null; walk.turnTo = null;
  }
  const dollPose = () => {
    const hv = (38 * Math.PI) / 360, hh = Math.atan(Math.tan(hv) * camera.aspect), dist = (R / Math.sin(Math.min(hv, hh))) * 0.9;
    return { pos: new THREE.Vector3(mid.x + dist * 0.05, dist * 0.8, mid.z + dist * 0.6), dist };
  };
  let riseAnim = null;
  function setMode(m) {
    stopTour();
    mode = m; controls.enabled = m === 'doll'; ceiling.visible = m === 'walk'; camera.fov = m === 'walk' ? 72 : 38; camera.updateProjectionMatrix();
    if (m === 'doll' && !riseAnim) { camera.position.copy(dollPose().pos); controls.target.copy(mid); controls.update(); } // fit the whole apartment into the frame, whatever its shape
    if (m === 'walk') { riseAnim = null; riseU.value = 1; const n = getNav(); if (!walk.placed || !n || !n.isFree(walk.x, walk.y)) placeStart(); }
    applyBg(); buildWalls(); buildPoints(); buildNotes(); place(); touch();
    hooks.walk && hooks.walk(walkState());
  }
  /** the walls stand up out of the plan, from the middle outwards, while the camera tilts from above the sheet to the doll view */
  function rise() {
    if (reduce) { riseU.value = 1; riseAnim = null; buildWalls(); touch(); return; }
    if (mode !== 'doll') setMode('doll');
    const end = dollPose();
    riseAnim = { t0: performance.now(), from: new THREE.Vector3(mid.x, end.dist * 1.25, mid.z + 0.01), to: end.pos };
    riseU.value = 0; camera.position.copy(riseAnim.from); controls.target.copy(mid); controls.update(); touch();
  }
  controls.addEventListener('start', () => { if (riseAnim) { riseAnim.cam = false; } });
  function getView() {
    const dir = camera.getWorldDirection(new THREE.Vector3());
    return { mode, x: camera.position.x / M, y: camera.position.z / M, z: camera.position.y / M, yaw: Math.atan2(dir.z, dir.x), pitch: Math.asin(dir.y), fov: camera.fov, walk: mode === 'walk' };
  }
  function setView(v) { // the same handle the 360 tour gives the shared video room
    if (v.mode && v.mode !== mode) setMode(v.mode);
    if (mode === 'walk') { Object.assign(walk, { x: v.x, y: v.y, yaw: v.yaw, pitch: v.pitch || 0, path: null, turnTo: null, placed: true }); place(); }
    else { camera.position.set(v.x * M, v.z * M, v.y * M); controls.update(); touch(false); }
  }

  // ---- the walk: a route through doors to any place or room, then a turn to the best view ----
  function walkTo(p) {
    if (mode !== 'walk') return false;
    const n = getNav(), r = n && route(n, [walk.x, walk.y], p);
    if (!r || r.length < 2) { const q = n && nearestFree(n, p[0], p[1]); if (!q) return false; walk.path = [q]; }
    else walk.path = r.slice(1);
    walk.turnTo = null; return true;
  }
  function goRoom(faceId, keepTour) {
    if (mode !== 'walk') setMode('walk');
    if (!keepTour) stopTour();
    const n = getNav(); if (!n) return false;
    const i = n.faces.findIndex((f) => f.id === faceId); if (i < 0) return false;
    const p = roomSpot(n, i); return p ? walkTo(p) : false;
  }
  function stopTour() { if (walk.tour) { walk.tour = null; hooks.walk && hooks.walk(walkState()); } }
  function tour() {
    if (mode !== 'walk') setMode('walk');
    const n = getNav(); if (!n) return false;
    const list = tourOrder(n, [walk.x, walk.y]).map((s) => n.faces[s.i].id);
    if (!list.length) return false;
    walk.tour = { list, i: 0, dwell: 0 }; goRoom(list[0], true); hooks.walk && hooks.walk(walkState());
    return true;
  }
  const walkState = () => ({ mode, touring: !!walk.tour, room: store.roomAt(walk.x, walk.y), moving: !!(walk.path && walk.path.length) });
  const angDiff = (a, b) => Math.atan2(Math.sin(a - b), Math.cos(a - b));
  function stepWalk(dt) {
    let moved = false;
    if (walk.path && walk.path.length) {
      const tgt = walk.path[0], dx = tgt[0] - walk.x, dy = tgt[1] - walk.y, l = Math.hypot(dx, dy), sp = 190 * dt; // cm a second, a calm walk
      const want = Math.atan2(dy, dx);
      walk.yaw += angDiff(want, walk.yaw) * Math.min(1, dt * 6);
      if (l <= sp) { walk.x = tgt[0]; walk.y = tgt[1]; walk.path.shift(); } else { walk.x += (dx / l) * sp; walk.y += (dy / l) * sp; }
      moved = true;
      if (!walk.path.length) { walk.path = null; const n = getNav(); walk.turnTo = n ? bestYaw(n, [walk.x, walk.y], walk.yaw) : null; hooks.walk && hooks.walk(walkState()); }
    } else if (walk.turnTo != null) {
      const d = angDiff(walk.turnTo, walk.yaw);
      if (Math.abs(d) < 0.01) { walk.yaw = walk.turnTo; walk.turnTo = null; if (walk.tour) walk.tour.dwell = 0; } else walk.yaw += d * Math.min(1, dt * 4);
      moved = true;
    } else if (walk.tour) {
      walk.tour.dwell += dt; walk.yaw += dt * 0.12; moved = true; // a slow look around before the next room
      if (walk.tour.dwell > 2.2) { walk.tour.i += 1; if (walk.tour.i >= walk.tour.list.length) stopTour(); else goRoom(walk.tour.list[walk.tour.i], true); }
    }
    if (walk.pitch !== -0.08 && !down) { walk.pitch += (-0.08 - walk.pitch) * Math.min(1, dt * 2); moved = true; }
    if (moved) place();
  }

  // ---- pointer: tap selects, drag moves a piece on the floor, in walk mode a tap on the floor walks there ----
  const ray = new THREE.Raycaster(), floorPlane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0), v2 = new THREE.Vector2(), hit3 = new THREE.Vector3();
  const aim = (ev) => { const r = renderer.domElement.getBoundingClientRect(); v2.set(((ev.clientX - r.left) / r.width) * 2 - 1, -((ev.clientY - r.top) / r.height) * 2 + 1); ray.setFromCamera(v2, camera); };
  const onFloor = (ev) => { aim(ev); return ray.ray.intersectPlane(floorPlane, hit3) ? [hit3.x / M, hit3.z / M] : null; };
  let down = null;
  renderer.domElement.addEventListener('pointerdown', (ev) => {
    stopTour(); if (riseAnim) riseAnim.cam = false;
    aim(ev);
    const hn = ray.intersectObjects(gNote.children, false)[0];
    const h = ray.intersectObjects(gItem.children, true)[0], hp = ray.intersectObjects(gPoint.children, false)[0], p = onFloor(ev);
    down = { x: ev.clientX, y: ev.clientY, moved: false, note: hn ? hn.object.userData.note : null, item: h ? h.object.userData.item : null, point: hp && (!h || hp.distance < h.distance) ? hp.object.userData.point : null, yaw: walk.yaw, pitch: walk.pitch };
    if (down.point || down.note) down.item = null;
    if (down.item && mode === 'doll' && p) {
      const it = store.item(down.item); controls.enabled = false; try { renderer.domElement.setPointerCapture(ev.pointerId); } catch (e) { /* synthetic pointer */ }
      down.off = [it.x - p[0], it.y - p[1]]; down.g = 'g' + Date.now(); hooks.select && hooks.select({ type: 'item', id: it.id });
    }
  });
  renderer.domElement.addEventListener('pointermove', (ev) => {
    if (!down) return;
    if (Math.hypot(ev.clientX - down.x, ev.clientY - down.y) > 6) down.moved = true;
    if (down.off) { const p = onFloor(ev); if (p) store.apply({ op: 'item.move', id: down.item, x: Math.round((p[0] + down.off[0]) / 5) * 5, y: Math.round((p[1] + down.off[1]) / 5) * 5 }, { gesture: down.g }); }
    else if (mode === 'walk' && down.moved) { walk.path = null; walk.turnTo = null; walk.yaw = down.yaw - (ev.clientX - down.x) * 0.005; walk.pitch = Math.max(-1, Math.min(1, down.pitch + (ev.clientY - down.y) * 0.004)); place(); }
  });
  const up = (ev) => {
    if (!down) return;
    if (!down.moved && !down.off) {
      aim(ev);
      const f = ray.intersectObjects(gFloor.children, false)[0];
      if (down.note) hooks.select && hooks.select({ type: 'note', id: down.note });
      else if (down.point) hooks.select && hooks.select({ type: 'point', id: down.point });
      else if (down.item && mode !== 'walk') hooks.select && hooks.select({ type: 'item', id: down.item });
      else if (mode === 'walk') { // walking: a tap anywhere walks there, through the doors; a tap on a wall walks to the room behind the nearest door
        const q = f ? [f.point.x / M, f.point.z / M] : onFloor(ev);
        if (q) { walkTo(q); hooks.walk && hooks.walk(walkState()); }
      } else hooks.select && hooks.select(f ? { type: 'room', id: f.object.userData.room } : null);
    }
    if (down.off) controls.enabled = mode === 'doll';
    down = null;
  };
  renderer.domElement.addEventListener('pointerup', up); renderer.domElement.addEventListener('pointercancel', up);
  renderer.domElement.addEventListener('keydown', (ev) => { // the arrows walk and turn; walls stop you, you slide along them
    if (mode !== 'walk') return;
    const k = ev.key; let used = true;
    stopTour(); walk.path = null; walk.turnTo = null;
    if (k === 'ArrowLeft') walk.yaw -= 0.12; else if (k === 'ArrowRight') walk.yaw += 0.12;
    else if (k === 'ArrowUp' || k === 'ArrowDown') {
      const s = k === 'ArrowUp' ? 18 : -18, n = getNav(), nx = walk.x + Math.cos(walk.yaw) * s, ny = walk.y + Math.sin(walk.yaw) * s;
      if (!n || n.isFree(nx, ny)) { walk.x = nx; walk.y = ny; } else if (n.isFree(nx, walk.y)) walk.x = nx; else if (n.isFree(walk.x, ny)) walk.y = ny;
    } else used = false;
    if (used) { ev.preventDefault(); place(); }
  });

  function size() { const w = host.clientWidth, h = host.clientHeight; if (!w || !h) return; renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix(); touch(false); }
  const ro = new ResizeObserver(size); ro.observe(host);

  const renders = [];
  let lastCam = '', lastT = performance.now();
  function tick(now) {
    if (dead) return;
    requestAnimationFrame(tick);
    now = now || performance.now();
    const dt = Math.min(0.1, (now - lastT) / 1000); lastT = now;
    if (riseAnim) {
      const k = Math.min(1, (now - riseAnim.t0) / RISE_MS);
      riseU.value = Math.min(1, k * 1.0);
      gGlass.scale.y = gPoint.scale.y = riseEase();
      if (riseAnim.cam !== false) { const c = Math.max(0, Math.min(1, (k - 0.15) / 0.8)), e = c < 0.5 ? 4 * c * c * c : 1 - Math.pow(-2 * c + 2, 3) / 2; camera.position.lerpVectors(riseAnim.from, riseAnim.to, e); controls.update(); }
      touch();
      if (k >= 1) { riseAnim = null; riseU.value = 1; gGlass.scale.y = gPoint.scale.y = 1; hooks.risen && hooks.risen(); }
    }
    if (mode === 'walk') stepWalk(dt);
    if (controls.enabled) controls.update();
    if (!dirty) return;
    dirty = false; const r0 = performance.now(); renderer.render(scene, camera); const rms = performance.now() - r0;
    renders.push(rms); if (renders.length > 300) renders.shift();
    if (pending != null) { const d = performance.now() - pending; pending = null; hooks.frame && hooks.frame(d, rms); }
    const v = getView(), key = v.x.toFixed(0) + v.y.toFixed(0) + v.yaw.toFixed(2);
    if (key !== lastCam) { lastCam = key; hooks.camera && hooks.camera(v); }
  }

  const reload = () => { for (const id of [...itemObj.keys()]) { const g = itemObj.get(id); gItem.remove(g); itemObj.delete(id); } buildWalls(); buildFloors(); buildPoints(); buildNotes(); for (const it of store.design.items) syncItem(it.id); showSel(); touch(); };
  store.on((e) => {
    if (e.type !== 'change') return;
    if (e.touched.all) { reload(); return; }
    if (pending == null) pending = e.t0;
    const walls = e.touched.finishes.some((k) => /^wall:|\*/.test(k));
    if (e.touched.geometry || walls) buildWalls();
    if (e.touched.geometry) buildFloors();
    if (e.touched.geometry || (e.touched.points && e.touched.points.length)) buildPoints();
    if (e.touched.notes && e.touched.notes.length) buildNotes();
    if (e.touched.finishes.length) showSel();
    for (const id of e.touched.items) syncItem(id);
    if (sel && sel.type === 'item') showSel();
    touch();
  });

  size(); buildFloors(); for (const it of store.design.items) syncItem(it.id);
  setMode('doll'); if (hooks.rise !== false) rise(); requestAnimationFrame(tick);
  return {
    // CLIMATE LAB ONLY (HAD-803): this copy hands the scene to docs/design-lab/climate-lab/climate.js; the live space.js has no such door
    lab: { THREE, scene, camera, renderer, sun, hemi, ground, ceiling, outside, gWall, gGlass, gFloor, M, H, R, mid, EYE, touch, get walk() { return walk; }, getNav },
    el: renderer.domElement, setMode, getView, setView, get mode() { return mode; },
    setSelection(s) { const pts = (sel && sel.type === 'point') || (s && s.type === 'point'), nts = (sel && sel.type === 'note') || (s && s.type === 'note'); sel = s; showSel(); if (pts) buildPoints(); if (nts) buildNotes(); },
    walkTo(p) { const ok = walkTo(p); hooks.walk && hooks.walk(walkState()); return ok; },
    goRoom(id) { const ok = goRoom(id); hooks.walk && hooks.walk(walkState()); return ok; },
    tour, stopTour, rise, get rising() { return !!riseAnim; }, get riseValue() { return riseU.value; },
    walkState,
    /** the rooms a walk can go to, in plan order (id, Hebrew name, net area) */
    rooms: () => store.derived.faces.filter((f) => f.room && f.net >= 2).map((f) => ({ id: f.id, name_he: f.room.name_he, type: f.room.type, net: f.net, fresh: !!f.room.fresh })),
    /** for checks: how far the wall is straight ahead of the walker (cm) and where the walker stands */
    aheadCm: () => { const n = getNav(); return n ? ahead(n, [walk.x, walk.y], walk.yaw) : null; },
    walker: () => ({ x: walk.x, y: walk.y, yaw: walk.yaw, path: walk.path ? walk.path.length : 0, turning: walk.turnTo != null, touring: !!walk.tour }),
    // for checks: where a plan point lands on the screen, and where a piece really stands in the 3D scene
    screenOf(x, y, h = 0) { const v = new THREE.Vector3(x * M, h * M, y * M).project(camera), r = renderer.domElement.getBoundingClientRect(); return [r.left + ((v.x + 1) / 2) * r.width, r.top + ((1 - v.y) / 2) * r.height]; },
    pointMesh(id) { const m = gPoint.children.find((c) => c.userData.point === id); return m ? { x: Math.round(m.position.x / M), y: Math.round(m.position.z / M), h: Math.round(m.position.y / M), mine: m.material !== PM.base } : null; },
    noteTags: () => gNote.children.map((s) => s.userData.note),
    placed(id) { const g = itemObj.get(id); return g ? [Math.round(g.position.x / M), Math.round(g.position.z / M), Math.round((-g.rotation.y * 180) / Math.PI)] : null; },
    floorKey(room) { const f = gFloor.children.find((c) => c.userData.room === room); return f ? Object.keys(mat.floors).find((k) => mat.floors[k] === f.material) : null; },
    renders, useModels, reload,
    /** the colour behind the apartment: the video call turns it to its ink surface, null returns the designer's own */
    setStage(c) { stage = c == null ? null : c; applyBg(); touch(false); },
    modelState: (id) => (itemObj.get(id) ? itemObj.get(id).userData.model || 'box' : null),
    destroy() { dead = true; ro.disconnect(); controls.dispose(); scene.traverse((o) => { if (o.geometry) o.geometry.dispose(); }); renderer.dispose(); renderer.domElement.remove(); },
    /** turns the camera around the apartment for ms and returns the time between frames (the device's real frame rate) */
    spin(ms) {
      return new Promise((done) => {
        const t0 = performance.now(), gaps = []; let last = t0;
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
