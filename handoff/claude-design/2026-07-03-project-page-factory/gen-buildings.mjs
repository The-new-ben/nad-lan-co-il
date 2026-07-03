#!/usr/bin/env node
/* ============================================================================
   NadLan 3D FACTORY — anchored-building GLB generator (Node, zero deps)
   ----------------------------------------------------------------------------
   This is the script referenced in docs/showroom-engine-wiring.md ("the build
   script that wrote assets/engine/*.glb and projects.js"). It regenerates the
   concept scene GLBs shipped in this folder (ashira.glb / rainbow.glb /
   dimri.glb) and a manifest with derived per-unit 3D coordinates.

   USAGE
     node generate-buildings.mjs            # all projects in SPECS
     node generate-buildings.mjs ashira     # one project

   OUTPUT (into this directory)
     <slug>.glb                  the anchored concept scene
     projects.generated.json    per-project meta + derived unit coords

   ADDING A NEW PROJECT = add a spec to SPECS below and run. No design request.
   Spec fields:
     floors, floorH (m), podiumFloors, fpX/fpZ (footprint m), twist (deg/floor),
     taperTop (0..1 top scale), seed (context-city layout), ctxCount,
     landmark {x,z,h}  — the red/white banded chimney (Reading Tower cue),
     neighbors [{x,z,floors,rot}] — comparable towers for scale,
     units [{id,floor,bearing,label,rooms,sqm,...}] — bearing in deg
       (270=west/sea, 90=east, 0=north, 180=south).

   SCENE ANCHORING (why buyers trust it): sea plane to the WEST (-X), beach
   strip, street grid, mid-rise context east of the tower, landmark chimney
   south, neighbor towers set back. A lone tower on a void reads fake.

   POSTERS: GLB posters/facades need a WebGL render — capture via model-viewer
   or three.js in a browser (see NOTES.md §1). This script is geometry only.

   HONESTY: output is CONCEPT geometry, labelled "הדמיה להמחשה" by the engine.
   Swap project_model_glb to the developer BIM (contract: 2026-07-02 critical
   report PART 4C) with no other change.
   ============================================================================ */
import { writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
const OUT = dirname(fileURLToPath(import.meta.url));

/* ---------------- mesh helpers ---------------- */
const deg = d => d * Math.PI / 180;
const lerp = (a, b, t) => a + (b - a) * t;
const newG = () => ({ pos: [], nrm: [], idx: [], vc: 0 });

function addBox(g, cx, cy, cz, sx, sy, sz, rot) {
  const a = deg(rot || 0), ca = Math.cos(a), sa = Math.sin(a);
  const hx = sx / 2, hy = sy / 2, hz = sz / 2;
  const F = [
    [0, 0, 1, [[-hx, -hy, hz], [hx, -hy, hz], [hx, hy, hz], [-hx, hy, hz]]],
    [0, 0, -1, [[hx, -hy, -hz], [-hx, -hy, -hz], [-hx, hy, -hz], [hx, hy, -hz]]],
    [1, 0, 0, [[hx, -hy, hz], [hx, -hy, -hz], [hx, hy, -hz], [hx, hy, hz]]],
    [-1, 0, 0, [[-hx, -hy, -hz], [-hx, -hy, hz], [-hx, hy, hz], [-hx, hy, -hz]]],
    [0, 1, 0, [[-hx, hy, hz], [hx, hy, hz], [hx, hy, -hz], [-hx, hy, -hz]]],
    [0, -1, 0, [[-hx, -hy, -hz], [hx, -hy, -hz], [hx, -hy, hz], [-hx, -hy, hz]]],
  ];
  for (const f of F) {
    const nb = g.vc, nx = f[0], ny = f[1], nz = f[2];
    const rnx = nx * ca + nz * sa, rnz = -nx * sa + nz * ca;
    for (const c of f[3]) {
      const rx = c[0] * ca + c[2] * sa, rz = -c[0] * sa + c[2] * ca;
      g.pos.push(rx + cx, c[1] + cy, rz + cz); g.nrm.push(rnx, ny, rnz); g.vc++;
    }
    g.idx.push(nb, nb + 1, nb + 2, nb, nb + 2, nb + 3);
  }
}

function addCyl(g, cx, cy, cz, rb, rt, h, sides = 14) {
  const y0 = cy - h / 2, y1 = cy + h / 2;
  for (let i = 0; i < sides; i++) {
    const a0 = i / sides * Math.PI * 2, a1 = (i + 1) / sides * Math.PI * 2;
    const nb = g.vc, nax = Math.cos((a0 + a1) / 2), naz = Math.sin((a0 + a1) / 2);
    g.pos.push(
      cx + Math.cos(a0) * rb, y0, cz + Math.sin(a0) * rb,
      cx + Math.cos(a1) * rb, y0, cz + Math.sin(a1) * rb,
      cx + Math.cos(a1) * rt, y1, cz + Math.sin(a1) * rt,
      cx + Math.cos(a0) * rt, y1, cz + Math.sin(a0) * rt);
    for (let k = 0; k < 4; k++) g.nrm.push(nax, 0, naz);
    g.vc += 4; g.idx.push(nb, nb + 1, nb + 2, nb, nb + 2, nb + 3);
  }
  const ct = g.vc; g.pos.push(cx, y1, cz); g.nrm.push(0, 1, 0); g.vc++;
  for (let i = 0; i < sides; i++) {
    const a0 = i / sides * Math.PI * 2, a1 = (i + 1) / sides * Math.PI * 2, nb = g.vc;
    g.pos.push(cx + Math.cos(a0) * rt, y1, cz + Math.sin(a0) * rt,
               cx + Math.cos(a1) * rt, y1, cz + Math.sin(a1) * rt);
    g.nrm.push(0, 1, 0, 0, 1, 0); g.vc += 2; g.idx.push(ct, nb, nb + 1);
  }
}

/* ---------------- anchored scene ---------------- */
function genScene(spec) {
  const G = { stone: newG(), glass: newG(), gold: newG(), land: newG(), sea: newG(),
              beach: newG(), ctx: newG(), ctx2: newG(), lmR: newG(), lmW: newG(), road: newG() };
  const fh = spec.floorH, pf = spec.podiumFloors, N = spec.floors, podiumH = pf * fh;
  // ground: sea west (-X), beach strip, city land east; street grid
  addBox(G.sea, -120, -0.5, 0, 220, 1.0, 360, 0);
  addBox(G.beach, -22, -0.32, 0, 26, 0.7, 360, 0);
  addBox(G.land, 95, -0.5, 0, 230, 1.0, 360, 0);
  addBox(G.road, -10, 0.06, 0, 6, 0.12, 360, 0);
  for (let r = 1; r <= 3; r++) addBox(G.road, 20 + r * 40, 0.05, 0, 3.5, 0.1, 360, 0);
  for (let r = -2; r <= 2; r++) addBox(G.road, 55, 0.05, r * 60, 200, 0.1, 4, 0);
  // podium + tower (stone slabs, glass floors, gold ribs every 5 floors)
  addBox(G.stone, 0, podiumH / 2, 0, spec.fpX + 9, podiumH, spec.fpZ + 8, 0);
  addBox(G.glass, 0, podiumH * 0.6, 0, spec.fpX + 7, podiumH * 0.62, spec.fpZ + 6, 0);
  for (let F = pf; F < N; F++) {
    const t = (F - pf) / (N - pf), sc = lerp(1, spec.taperTop, t), rot = spec.twist * F, y = F * fh;
    addBox(G.stone, 0, y + 0.16, 0, spec.fpX * sc + 0.7, 0.34, spec.fpZ * sc + 0.7, rot);
    addBox(G.glass, 0, y + fh * 0.6, 0, spec.fpX * sc, fh * 0.8, spec.fpZ * sc, rot);
    if ((F - pf) % 5 === 0 || F >= N - 2)
      addBox(G.gold, 0, y, 0, spec.fpX * sc + 1.1, 0.18, spec.fpZ * sc + 1.1, rot);
  }
  const yc = N * fh;
  addBox(G.gold, 0, yc + 0.4, 0, spec.fpX * spec.taperTop + 0.7, 0.7, spec.fpZ * spec.taperTop + 0.7, spec.twist * N);
  addBox(G.glass, 0, yc + 1.9, 0, spec.fpX * spec.taperTop * 0.7, 3.0, spec.fpZ * spec.taperTop * 0.7, spec.twist * N);
  addBox(G.gold, 0, yc + 4.4, 0, 0.5, 2.4, 0.5, 0); // mast
  // landmark: red/white banded chimney (Reading cue)
  if (spec.landmark) {
    const { x: lx, z: lz, h: lh } = spec.landmark, bands = 12, bh = lh / bands;
    for (let i = 0; i < bands; i++) {
      const rb = lerp(3.4, 2.1, i / bands), rt = lerp(3.4, 2.1, (i + 1) / bands);
      addCyl(i % 2 ? G.lmW : G.lmR, lx, bh * i + bh / 2, lz, rb, rt, bh + 0.02, 16);
    }
    addCyl(G.lmR, lx, lh + 0.8, lz, 2.1, 1.5, 1.6, 16);
  }
  // context mid-rises (3-8 floors) east of the tower, deterministic by seed
  let s = spec.seed || 7;
  const rng = () => (s = (s * 1103515245 + 12345) & 0x7fffffff) / 0x7fffffff;
  const placed = [[0, 0, 70]];
  const far = (x, z) => placed.every(p => Math.hypot(x - p[0], z - p[1]) >= p[2]);
  for (let n = 0, tr = 0; n < spec.ctxCount && tr < spec.ctxCount * 14; tr++) {
    const x = 34 + rng() * 90, z = (rng() * 2 - 1) * 150;
    const w = 12 + rng() * 16, d = 12 + rng() * 16, h = (3 + Math.floor(rng() * 6)) * 3.1;
    if (!far(x, z)) continue;
    placed.push([x, z, Math.max(w, d) + 18]);
    addBox(rng() > 0.5 ? G.ctx : G.ctx2, x, h / 2, z, w, h, d, (rng() * 2 - 1) * 8);
    addBox(rng() > 0.5 ? G.ctx2 : G.ctx, x, h + 0.2, z, w - 2, 0.5, d - 2, 0); n++;
  }
  for (const nb of (spec.neighbors || [])) {
    const h = nb.floors * 3.1;
    addBox(G.ctx, nb.x, h / 2, nb.z, 16, h, 15, nb.rot || 0);
    addBox(G.glass, nb.x, h * 0.6, nb.z, 13, h * 0.6, 12, nb.rot || 0);
  }
  return { groups: G, modelH: N * fh };
}

/* ---------------- GLB packer (glTF 2.0 binary) ---------------- */
const MATS = [
  ['stone', [0.93, 0.90, 0.83, 1], 0.04, 0.62, null, null],
  ['glass', [0.36, 0.47, 0.50, 0.5], 0.22, 0.09, [0.03, 0.05, 0.06], 'BLEND'],
  ['gold',  [0.62, 0.49, 0.25, 1], 0.90, 0.36, null, null],
  ['land',  [0.87, 0.82, 0.71, 1], 0, 0.97, null, null],
  ['sea',   [0.17, 0.36, 0.42, 1], 0, 0.16, [0.01, 0.04, 0.05], null],
  ['beach', [0.91, 0.86, 0.74, 1], 0, 0.90, null, null],
  ['ctx',   [0.80, 0.76, 0.69, 1], 0.02, 0.78, null, null],
  ['ctx2',  [0.72, 0.70, 0.66, 1], 0.02, 0.80, null, null],
  ['lmR',   [0.74, 0.32, 0.24, 1], 0, 0.55, null, null],
  ['lmW',   [0.94, 0.92, 0.87, 1], 0, 0.55, null, null],
  ['road',  [0.46, 0.44, 0.41, 1], 0, 0.85, null, null],
];
function buildGLB(groups) {
  const buffers = []; let bl = 0;
  const app = (t) => {
    const pad = (4 - (bl % 4)) % 4;
    if (pad) { buffers.push(new Uint8Array(pad)); bl += pad; }
    const o = bl, b = new Uint8Array(t.buffer, t.byteOffset, t.byteLength);
    buffers.push(b); bl += b.byteLength; return o;
  };
  const bv = [], ac = [], prim = [];
  MATS.forEach((m, mi) => {
    const g = groups[m[0]]; if (!g || g.vc === 0) return;
    const pos = new Float32Array(g.pos), nrm = new Float32Array(g.nrm), idx = new Uint16Array(g.idx);
    const mn = [1e9, 1e9, 1e9], mx = [-1e9, -1e9, -1e9];
    for (let i = 0; i < pos.length; i += 3) for (let k = 0; k < 3; k++) {
      const v = pos[i + k]; if (v < mn[k]) mn[k] = v; if (v > mx[k]) mx[k] = v;
    }
    const po = app(pos); bv.push({ buffer: 0, byteOffset: po, byteLength: pos.byteLength, target: 34962 });
    const aP = ac.length; ac.push({ bufferView: bv.length - 1, componentType: 5126, count: g.vc, type: 'VEC3', min: mn, max: mx });
    const no = app(nrm); bv.push({ buffer: 0, byteOffset: no, byteLength: nrm.byteLength, target: 34962 });
    const aN = ac.length; ac.push({ bufferView: bv.length - 1, componentType: 5126, count: g.vc, type: 'VEC3' });
    const io = app(idx); bv.push({ buffer: 0, byteOffset: io, byteLength: idx.byteLength, target: 34963 });
    const aI = ac.length; ac.push({ bufferView: bv.length - 1, componentType: 5123, count: idx.length, type: 'SCALAR' });
    prim.push({ attributes: { POSITION: aP, NORMAL: aN }, indices: aI, material: mi });
  });
  { const pad = (4 - (bl % 4)) % 4; if (pad) { buffers.push(new Uint8Array(pad)); bl += pad; } }
  const gltf = {
    asset: { version: '2.0', generator: 'nadlan-engine-v2' },
    scene: 0, scenes: [{ nodes: [0] }], nodes: [{ mesh: 0, name: 'scene' }],
    meshes: [{ primitives: prim }],
    materials: MATS.map(m => {
      const o = { name: m[0], pbrMetallicRoughness: { baseColorFactor: m[1], metallicFactor: m[2], roughnessFactor: m[3] } };
      if (m[4]) o.emissiveFactor = m[4];
      if (m[5]) { o.alphaMode = m[5]; o.doubleSided = true; }
      return o;
    }),
    bufferViews: bv, accessors: ac, buffers: [{ byteLength: bl }],
  };
  const bin = new Uint8Array(bl); let p = 0;
  for (const b of buffers) { bin.set(b, p); p += b.byteLength; }
  let jb = new TextEncoder().encode(JSON.stringify(gltf));
  const jp = (4 - (jb.byteLength % 4)) % 4;
  if (jp) { const t = new Uint8Array(jb.byteLength + jp); t.set(jb); t.fill(0x20, jb.byteLength); jb = t; }
  const total = 12 + 8 + jb.byteLength + 8 + bin.byteLength;
  const out = new Uint8Array(total), dv = new DataView(out.buffer);
  dv.setUint32(0, 0x46546C67, true); dv.setUint32(4, 2, true); dv.setUint32(8, total, true);
  dv.setUint32(12, jb.byteLength, true); dv.setUint32(16, 0x4E4F534A, true); out.set(jb, 20);
  const bo = 20 + jb.byteLength;
  dv.setUint32(bo, bin.byteLength, true); dv.setUint32(bo + 4, 0x004E4942, true); out.set(bin, bo + 8);
  return out;
}

/* ------------- unit coordinate derivation (hotspots/camera) ------------- */
function deriveUnits(spec) {
  const fh = spec.floorH, pf = spec.podiumFloors, N = spec.floors;
  return (spec.units || []).map(u => {
    const t = (u.floor - pf) / (N - pf), sc = lerp(1, spec.taperTop, t);
    const r = spec.fpX * sc / 2 + 0.6, bb = deg(u.bearing);
    const x = r * Math.sin(bb), z = r * Math.cos(bb), y = u.floor * fh + fh * 0.4;
    const f3 = n => Math.round(n * 1000) / 1000;
    return { ...u,
      hotspot_position: `${f3(x)} ${f3(y)} ${f3(z)}`,
      hotspot_normal: `${f3(Math.sin(bb))} 0 ${f3(Math.cos(bb))}`,
      camera_orbit: `${u.bearing}deg 72deg ${Math.round(N * fh * 1.5 * 0.62)}m` };
  });
}

/* ---------------- project specs (the factory input) ---------------- */
const SPECS = {
  ashira:  { floors: 35, floorH: 3.05, podiumFloors: 3, fpX: 24, fpZ: 19, twist: 0,   taperTop: 0.90, seed: 11, ctxCount: 30,
             landmark: { x: -6,  z: -165, h: 58 }, neighbors: [{ x: 150, z: -170, floors: 24, rot: 8 }, { x: 185, z: 150, floors: 20, rot: -6 }],
             units: [ { id: 'a1', label: 'A-10', floor: 10, bearing: 270 }, { id: 'a2', label: 'B-20', floor: 20, bearing: 225 },
                      { id: 'a3', label: 'B-27', floor: 27, bearing: 270 }, { id: 'a4', label: 'PH-33', floor: 33, bearing: 225 } ] },
  rainbow: { floors: 38, floorH: 3.05, podiumFloors: 3, fpX: 24, fpZ: 20, twist: 0.6, taperTop: 0.85, seed: 23, ctxCount: 28,
             landmark: { x: -10, z: -180, h: 58 }, neighbors: [{ x: 165, z: 160, floors: 26, rot: 0 }, { x: 185, z: -150, floors: 22, rot: 6 }],
             units: [ { id: 'r1', label: 'ק8', floor: 8, bearing: 225 }, { id: 'r2', label: 'ק16', floor: 16, bearing: 270 },
                      { id: 'r3', label: 'ק24', floor: 24, bearing: 180 }, { id: 'r4', label: 'ק31', floor: 31, bearing: 225 },
                      { id: 'r5', label: 'ק36', floor: 36, bearing: 270 } ] },
  dimri:   { floors: 39, floorH: 3.10, podiumFloors: 2, fpX: 28, fpZ: 22, twist: 0,   taperTop: 0.92, seed: 31, ctxCount: 26,
             landmark: { x: -12, z: -175, h: 58 }, neighbors: [{ x: 170, z: 150, floors: 24, rot: 0 }, { x: 185, z: -140, floors: 20, rot: 0 }],
             units: [ { id: 'd1', label: 'A-12', floor: 12, bearing: 270 }, { id: 'd2', label: 'B-24', floor: 24, bearing: 225 },
                      { id: 'd3', label: 'B-30', floor: 30, bearing: 270 }, { id: 'd4', label: 'PH-37', floor: 37, bearing: 225 } ] },
  duo:     { floors: 54, floorH: 3.20, podiumFloors: 4, fpX: 26, fpZ: 24, twist: 0.4, taperTop: 0.82, seed: 41, ctxCount: 32,
             landmark: null, neighbors: [{ x: 170, z: 150, floors: 40, rot: 0 }, { x: 190, z: -150, floors: 34, rot: 4 }],
             units: [ { id: 'u1', label: 'ק14', floor: 14, bearing: 270 }, { id: 'u2', label: 'ק28', floor: 28, bearing: 225 },
                      { id: 'u3', label: 'ק44', floor: 44, bearing: 270 } ] },
};

/* ---------------- main ---------------- */
const only = process.argv[2];
const manifest = {};
for (const slug of Object.keys(SPECS)) {
  if (only && slug !== only) continue;
  const spec = SPECS[slug];
  if(spec.landmark){spec.landmark={...spec.landmark,x:spec.landmark.x*0.7,z:spec.landmark.z*0.62};}
  spec.neighbors=(spec.neighbors||[]).map(n=>({...n,x:n.x*0.5,z:n.z*0.55}));
  const { groups, modelH } = genScene(spec);
  const glb = buildGLB(groups);
  writeFileSync(join(OUT, `${slug}.glb`), glb);
  manifest[slug] = {
    slug, floors: spec.floors, floor_height_m: spec.floorH, height_m: Math.round(modelH),
    default_orbit: `-30deg 73deg ${Math.round(modelH * 1.5 * 1.55)}m`,
    default_target: `0m ${Math.round(modelH * 0.49)}m 0m`,
    frame_radius_m: Math.round(modelH * 1.5 * 1.55),
    units: deriveUnits(spec),
  };
  console.log(`${slug}.glb  ${(glb.byteLength / 1024).toFixed(1)}KB  H=${Math.round(modelH)}m  units=${manifest[slug].units.length}`);
}
writeFileSync(join(OUT, 'projects.generated.json'), JSON.stringify(manifest, null, 1));
console.log('projects.generated.json written. Posters/facades: render in a browser (NOTES.md §1).');
