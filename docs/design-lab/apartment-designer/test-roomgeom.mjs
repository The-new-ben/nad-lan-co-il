// node docs/design-lab/apartment-designer/test-roomgeom.mjs
// "Measure with the camera" geometry without a phone. Synthetic apartments are built from a KNOWN wall graph (centre lines
// with thicknesses); the inner wall faces of every room are derived from it exactly as a person would mark them with the
// phone (corners only), then shaken (up to 3 cm per corner), turned a few degrees, moved, passed through the WebXR world
// frame (metres, x and z on the floor), and fed to roomsToSegments. The result must give back the apartment: the rooms,
// their areas, the thickness of every shared wall, and every door and window on its own wall. Then it goes through the
// plan tool's builder (planbuild.js buildPlan) and the engine (core.js) like a real measurement would.
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url)), lib = path.join(here, '../../../plugins/nadlan-config/assets/designer/');
const G = await import(pathToFileURL(lib + 'roomgeom.js'));
const { derive, emptyDesign, createStore } = await import(pathToFileURL(lib + 'core.js'));
let PB = null;
try { PB = await import(pathToFileURL(lib + 'planbuild.js')); } catch (e) { console.log('note: planbuild.js not loadable (' + e.message + '), checking against core.js only'); }

let pass = 0, fail = 0;
const fails = [];
const check = (name, ok, detail) => { if (ok) pass++; else { fail++; fails.push(name); } if (!ok || process.argv.includes('-v')) console.log((ok ? 'ok   ' : 'FAIL ') + name + (detail !== undefined ? '  ' + (typeof detail === 'string' ? detail : JSON.stringify(detail)) : '')); };
const stats = { area: [], gross: [], net: [], t: [], openPos: [] };

const sub = (a, b) => [a[0] - b[0], a[1] - b[1]];
const add = (a, b) => [a[0] + b[0], a[1] + b[1]];
const mul = (a, k) => [a[0] * k, a[1] * k];
const dot = (a, b) => a[0] * b[0] + a[1] * b[1];
const crs = (a, b) => a[0] * b[1] - a[1] * b[0];
const dist = (a, b) => Math.hypot(a[0] - b[0], a[1] - b[1]);
const rot = (p, a) => [p[0] * Math.cos(a) - p[1] * Math.sin(a), p[0] * Math.sin(a) + p[1] * Math.cos(a)];
const pct = (a, b) => (100 * Math.abs(a - b)) / Math.abs(b);
function rng(seed) { return () => { seed |= 0; seed = (seed + 0x6d2b79f5) | 0; let t = Math.imul(seed ^ (seed >>> 15), 1 | seed); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
function pip(p, poly) { let inside = false; for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) { const a = poly[i], b = poly[j]; if ((a[1] > p[1]) !== (b[1] > p[1]) && p[0] < ((b[0] - a[0]) * (p[1] - a[1])) / (b[1] - a[1]) + a[0]) inside = !inside; } return inside; }

// ---------- the truth: a wall graph ----------
// walls: [x0,y0,x1,y1,t,kind]; rooms: [name_he, key, type, at]; openings: [x,y (a point on the wall centre), w, type, roomKeyIdx]
function truth(def) {
  const nodes = {}, key = new Map();
  const nd = (p) => { const k = p[0] + ',' + p[1]; if (!key.has(k)) { const id = 'n' + key.size; key.set(k, id); nodes[id] = p; } return key.get(k); };
  const all = def.walls.map(([x0, y0, x1, y1, t, kind]) => ({ a: [x0, y0], b: [x1, y1], t, kind }));
  const ends = all.flatMap((w) => [w.a, w.b]);
  const walls = [];
  for (const w of all) { // split every wall at the ends of the others that lie on it (T junctions)
    const L = dist(w.a, w.b), d = mul(sub(w.b, w.a), 1 / L);
    const cuts = [...new Set(ends.filter((p) => Math.abs(crs(sub(p, w.a), d)) < 0.01).map((p) => dot(sub(p, w.a), d)).filter((s) => s > 0.01 && s < L - 0.01))].sort((x, y) => x - y);
    let s0 = 0;
    for (const s of [...cuts, L]) { walls.push({ id: 'w' + walls.length, a: nd(add(w.a, mul(d, s0))), b: nd(add(w.a, mul(d, s))), t: w.t, kind: w.kind }); s0 = s; }
  }
  const rooms = def.rooms.map(([name_he, k, type, at], i) => ({ id: k + i, name_he, key: k, type, at, floor: 'porcelain-80' }));
  const apt = { schema: 'nadlan-apartment', v: 1, id: 'truth', geometry_revision: 't', unit: { project: null, unit_id: null, rooms: 1 }, nodes, walls, openings: [], rooms, rules: [], levels: [{ id: 'L0', height: 270, slab: 25 }] };
  const dv = derive(apt, emptyDesign(apt));
  const wallOf = (p, q) => walls.find((w) => (dist(nodes[w.a], p) < 0.01 && dist(nodes[w.b], q) < 0.01) || (dist(nodes[w.a], q) < 0.01 && dist(nodes[w.b], p) < 0.01));
  const faces = dv.faces.filter((f) => f.room).map((f) => {
    let P = f.poly.slice(); if (G.signedArea(P) < 0) P = P.reverse();
    const n = P.length, lines = [];
    for (let i = 0; i < n; i++) { const p = P[i], q = P[(i + 1) % n], w = wallOf(p, q), d = mul(sub(q, p), 1 / dist(p, q)); lines.push({ p: add(p, mul([-d[1], d[0]], w.t / 2)), d, t: w.t, w }); }
    const inner = [];
    for (let i = 0; i < n; i++) {
      const A = lines[(i + n - 1) % n], B = lines[i], den = crs(A.d, B.d);
      if (Math.abs(den) > 1e-9) { const t = crs(sub(B.p, A.p), B.d) / den; inner.push(add(A.p, mul(A.d, t))); continue; }
      if (A.t === B.t) continue; // a corner on a straight wall: nobody marks it
      const v = P[i]; inner.push(add(A.p, mul(A.d, dot(sub(v, A.p), A.d)))); inner.push(add(B.p, mul(B.d, dot(sub(v, B.p), B.d))));
    }
    return { room: f.room, gross: f.gross, net: f.net, poly: f.poly, inner, area: G.polygonArea(inner) / 1e4, walls: f.walls };
  });
  const shared = walls.filter((w) => faces.filter((f) => f.walls.includes(w.id)).length >= 2);
  const openings = (def.openings || []).map(([x, y, w, type, roomIdx]) => {
    const host = walls.find((h) => { const a = nodes[h.a], b = nodes[h.b], L = dist(a, b), d = mul(sub(b, a), 1 / L), s = dot(sub([x, y], a), d); return Math.abs(crs(sub([x, y], a), d)) < 0.01 && s > 0 && s < L; });
    const a = nodes[host.a], b = nodes[host.b], d = mul(sub(b, a), 1 / dist(a, b)), nrm = [-d[1], d[0]], at = rooms[roomIdx].at;
    const side = dot(sub(at, [x, y]), nrm) > 0 ? 1 : -1, off = mul(nrm, (side * host.t) / 2);
    return { host, c: [x, y], w, type, pa: add(add([x, y], mul(d, -w / 2)), off), pb: add(add([x, y], mul(d, w / 2)), off) };
  });
  return { apt, nodes, walls, rooms, faces, shared, openings };
}

// ---------- a person measuring it ----------
function measure(T, seed, opts = {}) {
  const r = rng(seed), noise = opts.noise == null ? 3 : opts.noise, ang = opts.ang != null ? opts.ang : (r() * 2 - 1) * 8 * (Math.PI / 180);
  const off = [r() * 400 - 200, r() * 400 - 200];
  const shake = (p) => { const a = r() * 2 * Math.PI, m = Math.sqrt(r()) * noise; return [p[0] + Math.cos(a) * m, p[1] + Math.sin(a) * m]; };
  const world = (p) => { const q = add(rot(p, ang), off); return [q[0] / 100, -1.38, q[1] / 100]; }; // what WebXR reports, metres
  const back = (p) => G.worldToPlan(p);
  const rooms = T.faces.map((f) => {
    let pts = f.inner.map((p) => back(world(shake(p))));
    const k = Math.floor(r() * pts.length); pts = pts.slice(k).concat(pts.slice(0, k)); // starts at any corner
    if (r() < 0.5) pts.reverse(); // walks either way round
    if (r() < 0.3) pts.push(add(pts[0], [r() * 4 - 2, r() * 4 - 2])); // ends on the first corner again
    return { points: pts, name_he: f.room.name_he, type: f.room.type, key: f.room.key };
  });
  const openings = T.openings.map((o) => ({ a: back(world(shake(o.pa))), b: back(world(shake(o.pb))), type: o.type }));
  return { rooms, openings, ang };
}

// ---------- the apartments ----------
const F = 'facade', P = 'partition', M = 'mamad', RL = 'rail';
const APTS = {
  row3: {
    walls: [[0, 0, 1100, 0, 25, F], [1100, 0, 1100, 420, 25, F], [1100, 420, 0, 420, 25, F], [0, 420, 0, 0, 25, F], [500, 0, 500, 420, 12, P], [820, 0, 820, 420, 10, P]],
    rooms: [['סלון', 'living', 'living', [250, 210]], ['חדר שינה', 'bedroom', 'bedroom', [660, 210]], ['חדר שינה', 'bedroom', 'bedroom', [960, 210]]],
    openings: [[500, 150, 80, 'door', 0], [650, 0, 120, 'window', 1], [960, 420, 100, 'window', 2]],
  },
  corridor: {
    walls: [[0, 0, 1000, 0, 25, F], [1000, 0, 1000, 800, 25, F], [1000, 800, 0, 800, 25, F], [0, 800, 0, 0, 25, F], [380, 0, 380, 800, 15, P],
      [380, 350, 1000, 350, 10, P], [700, 0, 700, 350, 10, P], [380, 470, 700, 470, 12, P], [700, 470, 1000, 470, 30, M], [700, 470, 700, 800, 30, M]],
    rooms: [['סלון', 'living', 'living', [190, 400]], ['חדר שינה', 'bedroom', 'bedroom', [540, 170]], ['חדר רחצה', 'bath', 'wet', [850, 170]], ['מסדרון', 'corridor', 'hall', [690, 410]], ['חדר שינה', 'bedroom', 'bedroom', [540, 640]], ['ממ״ד', 'mamad', 'mamad', [850, 640]]],
    openings: [[450, 350, 80, 'door', 3], [800, 470, 80, 'door', 3], [540, 800, 140, 'window', 4], [380, 410, 90, 'door', 0]],
  },
  lshape: {
    walls: [[0, 0, 900, 0, 25, F], [900, 0, 900, 700, 25, F], [900, 700, 0, 700, 25, F], [0, 700, 0, 0, 25, F], [550, 0, 550, 700, 12, P], [550, 450, 900, 450, 10, P], [300, 300, 300, 700, 10, P], [300, 300, 550, 300, 10, P]],
    rooms: [['סלון', 'living', 'living', [150, 150]], ['מטבח', 'kitchen', 'kitchen', [425, 500]], ['חדר שינה', 'bedroom', 'bedroom', [725, 225]], ['חדר רחצה', 'bath', 'wet', [725, 575]]],
    openings: [[420, 300, 90, 'door', 0], [550, 150, 80, 'door', 0], [150, 0, 160, 'window', 0], [725, 450, 70, 'door', 2]],
  },
  balcony: {
    walls: [[0, 0, 900, 0, 25, F], [900, 0, 900, 450, 25, F], [900, 450, 0, 450, 25, F], [0, 450, 0, 0, 25, F], [600, 0, 600, 450, 12, P], [0, 450, 0, 630, 8, RL], [0, 630, 600, 630, 8, RL], [600, 630, 600, 450, 8, RL]],
    rooms: [['סלון', 'living', 'living', [300, 225]], ['חדר שינה', 'bedroom', 'bedroom', [750, 225]], ['מרפסת', 'balcony', 'balcony', [300, 540]]],
    openings: [[300, 450, 160, 'door', 0], [600, 300, 80, 'door', 0], [750, 0, 120, 'window', 1]],
  },
  five: {
    walls: [[0, 0, 1200, 0, 25, F], [1200, 0, 1200, 900, 25, F], [1200, 900, 0, 900, 25, F], [0, 900, 0, 0, 25, F], [600, 0, 600, 450, 15, P], [900, 0, 900, 450, 20, P],
      [600, 450, 900, 450, 30, M], [600, 450, 600, 900, 30, M], [900, 450, 900, 900, 30, M], [900, 450, 1200, 450, 10, P]],
    rooms: [['סלון', 'living', 'living', [300, 450]], ['חדר שינה', 'bedroom', 'bedroom', [750, 225]], ['חדר שינה', 'bedroom', 'bedroom', [1050, 225]], ['ממ״ד', 'mamad', 'mamad', [750, 675]], ['חדר רחצה', 'bath', 'wet', [1050, 675]]],
    openings: [[600, 700, 90, 'door', 0], [600, 200, 80, 'door', 0], [1050, 450, 70, 'door', 4], [750, 900, 100, 'window', 3]],
  },
};

/** an engine document straight from the segments, with OUR thicknesses (the plan tool keeps only the kind) */
function ownPlan(res, rooms) {
  const nodes = {}, key = new Map();
  const nd = (p) => { const k = p[0] + ',' + p[1]; if (!key.has(k)) { const id = 'n' + key.size; key.set(k, id); nodes[id] = p; } return key.get(k); };
  const walls = res.segments.map((s, i) => ({ id: 'w' + i, a: nd(s.a), b: nd(s.b), t: s.t, kind: s.kind === 'rail' ? 'rail' : s.kind === 'facade' ? 'facade' : 'partition' }));
  const apt = { schema: 'nadlan-apartment', v: 1, id: 'own', geometry_revision: 'o', unit: { project: null, unit_id: null, rooms: 1 }, nodes, walls, openings: [], rooms, rules: [], levels: [{ id: 'L0', height: 270, slab: 25 }] };
  return { apt, dv: derive(apt, emptyDesign(apt)) };
}

function runApartment(name, def, seed, opts = {}) {
  const T = truth(def), m = measure(T, seed, opts);
  const res = G.roomsToSegments(m.rooms, { openings: m.openings });
  const tag = name + '#' + seed;
  if (process.env.DUMP === tag) console.log(JSON.stringify(res.segments.map((s) => [s.a, s.b, s.t, s.kind])));
  check(tag + ': every room comes back (' + T.faces.length + ')', res.rooms.length === T.faces.length, { got: res.rooms.length, warnings: res.warnings });
  check(tag + ': no warnings', res.warnings.length === 0, res.warnings);
  { const bent = res.segments.filter((s) => !(Math.abs(s.a[0] - s.b[0]) < 0.05 || Math.abs(s.a[1] - s.b[1]) < 0.05)); check(tag + ': walls straight (axis-aligned) after squaring', !bent.length, bent); }
  if (opts.invariantOnly) return { T, res };
  // the frames line up: the turn is undone and the origin is the top-left corner of the outside walls
  const own = ownPlan(res, T.rooms.map((r) => ({ ...r })));
  const ownFaces = own.dv.faces.filter((f) => f.room);
  check(tag + ': the engine finds every room in our walls', ownFaces.length === T.faces.length, { got: ownFaces.length });
  for (const f of T.faces) {
    const rr = res.rooms.find((x) => pip(f.room.at, x.poly) || pip(x.at, f.inner));
    const of = ownFaces.find((x) => x.room.id === f.room.id);
    const nm = tag + ' ' + f.room.key;
    if (!rr || !of) { check(nm + ': room found', false); continue; }
    const ogA = G.polygonArea(of.poly) / 1e4, tgA = G.polygonArea(f.poly) / 1e4;
    if (opts.noise == null) { stats.area.push(pct(rr.area, f.area)); stats.gross.push(pct(ogA, tgA)); stats.net.push(pct(of.net, f.net)); }
    check(nm + ': floor area within 2% (' + f.area.toFixed(2) + ' m²)', pct(rr.area, f.area) <= 2, { got: rr.area, want: +f.area.toFixed(2) });
    check(nm + ': centre-line area within 2%', pct(ogA, tgA) <= 2, { got: +ogA.toFixed(3), want: +tgA.toFixed(3) });
    check(nm + ': engine net area within 2%', pct(of.net, f.net) <= 2, { got: of.net, want: f.net });
  }
  // shared walls: same place, same thickness
  for (const w of T.shared) {
    const a = T.nodes[w.a], b = T.nodes[w.b], L = dist(a, b), d = mul(sub(b, a), 1 / L);
    let best = null;
    for (const s of res.segments) {
      const sd = sub(s.b, s.a), sl = Math.hypot(sd[0], sd[1]); if (Math.abs(crs(sd, d)) / sl > 0.02) continue;
      if (Math.abs(crs(sub(s.a, a), d)) > 5) continue;
      const u = dot(sub(s.a, a), d), v = dot(sub(s.b, a), d), ov = Math.min(L, Math.max(u, v)) - Math.max(0, Math.min(u, v));
      if (ov > 0 && (!best || ov > best.ov)) best = { s, ov };
    }
    const ok = best && best.ov >= 0.5 * L;
    const noise = opts.noise == null ? 3 : opts.noise, lim = noise > 1.5 ? 2 * noise : 3; // two faces, each off by up to the noise
    if (ok && noise === 3) stats.t.push(Math.abs(best.s.t - w.t));
    check(tag + ' shared wall ' + w.t + ' cm at ' + JSON.stringify(a) + ': found, thickness within ' + lim + ' cm', ok && Math.abs(best.s.t - w.t) <= lim, best ? { t: best.s.t, overlap: Math.round(best.ov), L: Math.round(L) } : 'missing');
  }
  // doors and windows on their own wall
  check(tag + ': every opening kept (' + T.openings.length + ')', res.openings.length === T.openings.length, { got: res.openings.length });
  res.openings.forEach((o, i) => {
    const t = T.openings[i]; if (!t) return;
    const c = [(o.a[0] + o.b[0]) / 2, (o.a[1] + o.b[1]) / 2];
    let host = null, hd = Infinity;
    for (const w of T.walls) { const r = G.segDist(c, T.nodes[w.a], T.nodes[w.b]); if (r.d < hd) { hd = r.d; host = w; } }
    const same = host && (host === t.host || (Math.abs(crs(sub(T.nodes[host.b], T.nodes[host.a]), sub(t.c, T.nodes[host.a]))) / dist(T.nodes[host.a], T.nodes[host.b]) < 1 && host.t === t.host.t));
    if (opts.noise == null) stats.openPos.push(dist(c, t.c));
    check(tag + ' ' + t.type + ' ' + i + ': on the right wall, centre within 6 cm, width within 6 cm', same && o.type === t.type && dist(c, t.c) <= 6 && Math.abs(o.w - t.w) <= 6, { off: +dist(c, t.c).toFixed(1), w: o.w, want: t.w });
  });
  // through the plan tool's builder, as the designer will receive it
  if (PB) {
    let plan = null, err = null;
    try { plan = PB.buildPlan(res.draft); } catch (e) { err = e.message; }
    check(tag + ': buildPlan accepts the draft', !!plan, err);
    if (plan) {
      const dv = derive(plan, emptyDesign(plan)), rf = dv.faces.filter((f) => f.room);
      check(tag + ': buildPlan: ' + T.faces.length + ' rooms, named', rf.length === T.faces.length && plan.rooms.every((r) => r.type !== 'other'), { got: rf.length, types: plan.rooms.map((r) => r.type) });
      check(tag + ': buildPlan: every door and window placed', plan.openings.length === T.openings.length, { got: plan.openings.length });
      for (const f of T.faces) { const g = dv.faces.find((x) => pip(f.room.at, x.poly)); const ga = g && G.polygonArea(g.poly) / 1e4, fa = G.polygonArea(f.poly) / 1e4; check(tag + ' ' + f.room.key + ': buildPlan centre-line area within 2%', g && pct(ga, fa) <= 2, g ? { got: +ga.toFixed(3), want: +fa.toFixed(3) } : 'missing'); }
      let st = null; try { st = createStore(plan, emptyDesign(plan)); } catch (e) { err = e.message; }
      check(tag + ': the designer store opens the plan', !!st, err);
    }
  }
  return { T, res };
}

// ---------- 1. the small tools ----------
check('polygonArea: 4 x 3 m', G.polygonArea([[0, 0], [400, 0], [400, 300], [0, 300]]) === 120000);
check('polygonArea: either direction', G.polygonArea([[0, 300], [400, 300], [400, 0], [0, 0]]) === 120000);
check('worldToPlan: metres x,z to cm', JSON.stringify(G.worldToPlan([1.25, -1.4, -2.5])) === '[125,-250]' && JSON.stringify(G.worldToPlan({ x: 0.5, y: 0, z: 0.1 })) === '[50,10]');
{
  const c = G.closeRoom([[0, 0], [400, 2], [401, 300], [0, 299], [3, 4]]);
  check('closeRoom: the last corner on the first one is dropped', c.ok && c.points.length === 4, c);
  check('closeRoom: two corners are not a room', G.closeRoom([[0, 0], [100, 0]]).why === 'few');
  check('closeRoom: a corner on a straight wall is dropped', G.closeRoom([[0, 0], [200, 1], [400, 0], [400, 300], [0, 300]]).points.length === 4);
  check('closeRoom: a crossed outline is refused', G.closeRoom([[0, 0], [400, 300], [400, 0], [0, 300]]).why === 'cross');
  check('closeRoom: a tiny outline is refused', G.closeRoom([[0, 0], [30, 0], [30, 30], [0, 30]]).why === 'small');
}
{
  const s1 = G.snapCorner([0, 0], [300, 20], 0);
  check('snapCorner: 3.8 degrees off becomes straight, length kept', s1.snap === 'axis' && Math.abs(s1.p[1]) < 1e-9 && Math.abs(s1.p[0] - 300) < 1e-9, s1);
  const s2 = G.snapCorner([0, 0], [300, 60], 0);
  check('snapCorner: 11 degrees off stays as measured', s2.snap === null && s2.p[1] === 60, s2);
  const s3 = G.snapCorner([0, 0], [15, 290], 0);
  check('snapCorner: square to the axis', s3.snap === 'axis' && Math.abs(s3.p[0]) < 1e-9, s3);
  const s4 = G.snapCorner([0, 0], [300, 20], 0, { square: false });
  check('snapCorner: switched off keeps the point', s4.snap === null && s4.p[1] === 20);
  const s5 = G.snapCorner([400, 300], [6, 295], 0, { corners: [[0, 300], [0, 0]] });
  check('snapCorner: an existing corner close by wins', s5.snap === 'corner' && s5.p[0] === 0 && s5.p[1] === 300, s5);
  const a = 0.3, s6 = G.snapCorner([0, 0], rot([300, 15], a), a);
  check('snapCorner: a turned axis (17 degrees)', s6.snap === 'axis' && Math.abs(rot(s6.p, -a)[1]) < 1e-6, s6);
  const s7 = G.snapCorner([400, 0], [395, 290], 0, { next: [0, 300] });
  check('snapCorner: the last corner squares both walls', s7.snap === 'square' && Math.abs(s7.p[0] - 400) < 1e-6 && Math.abs(s7.p[1] - 300) < 1e-6, s7);
}
{
  const r = G.roomsToSegments([]);
  check('roomsToSegments: nothing measured says so', r.segments.length === 0 && r.warnings.some((w) => w.code === 'no.room'));
  const one = G.roomsToSegments([{ points: [[0, 0], [400, 0], [400, 300], [0, 300]], name_he: 'סלון', type: 'living', key: 'living' }]);
  const ext = one.segments.every((s) => s.kind === 'facade' && s.t === 25);
  check('one room: 4 outside walls, 25 cm, centre line 12.5 cm out', one.segments.length === 4 && ext && G.polygonArea(one.segments.map((s) => s.a)) === 425 * 325, one.segments);
  check('one room: the floor area is the measured one', one.rooms[0].area === 12, one.rooms[0]);
  check('one room: the draft names it for the plan tool', one.draft.rooms.length === 1 && one.draft.rooms[0].key === 'living' && one.draft.segs.length === 4);
  const far = G.roomsToSegments([{ points: [[0, 0], [400, 0], [400, 300], [0, 300]] }, { points: [[460, 0], [800, 0], [800, 300], [460, 300]] }]);
  const vx = far.segments.filter((s) => s.a[0] === s.b[0] && s.a[0] > 100 && s.a[0] < 700);
  check('a 60 cm gap is two outside walls, not one shared wall', vx.length === 2 && vx.every((s) => s.kind === 'facade' && s.t === 25), vx);
  const tiny = G.roomsToSegments([{ points: [[0, 0], [400, 0], [400, 300], [0, 300]] }, { points: [[412, 280], [700, 280], [700, 500], [412, 500]] }]);
  check('an overlap under 30 cm is not a shared wall', !tiny.segments.some((s) => s.kind === 'partition'), tiny.segments.filter((s) => s.kind === 'partition'));
  const ob = G.roomsToSegments([{ points: [[0, 0], [400, 0], [400, 300], [0, 300]] }], { square: false, axis: 0 });
  check('square:false and a given axis keep the measured frame', ob.axis === 0 && ob.segments.length === 4);
  const tri = G.roomsToSegments([{ points: [[0, 0], [500, 0], [500, 400], [200, 400], [0, 200]] }]);
  check('a 45 degree wall stays at 45 degrees', tri.segments.some((s) => Math.abs(Math.abs(s.a[0] - s.b[0]) - Math.abs(s.a[1] - s.b[1])) < 1 && Math.abs(s.a[0] - s.b[0]) > 50), tri.segments);
  const two = G.roomsToSegments([{ points: [[0, 0], [400, 0], [400, 300], [0, 300]] }, { points: [[414, 0], [700, 0], [700, 300], [414, 300]] }], { openings: [{ a: [407, 100], b: [407, 180], type: 'door' }] });
  const sh = two.segments.find((s) => s.kind === 'partition');
  check('two rooms: the shared wall sits mid-gap with the gap as thickness', sh && sh.t === 14 && sh.a[0] === 419.5, sh);
  check('two rooms: outside walls run straight through the T (one wall each side)', two.segments.filter((s) => s.kind === 'facade').length === 6, two.segments);
  check('two rooms: the door lands on the shared wall', two.openings.length === 1 && two.openings[0].a[0] === 419.5 && two.openings[0].w === 80, two.openings);
  const off = G.roomsToSegments([{ points: [[0, 0], [400, 0], [400, 300], [0, 300]] }], { openings: [{ a: [150, 150], b: [230, 150], type: 'door' }] });
  check('a door measured in the middle of the room is reported, not placed', off.openings.length === 0 && off.warnings.some((w) => w.code === 'opening.off'));
}

// ---------- 2. whole apartments, shaken ----------
const SEEDS = [11, 23, 37];
for (const [name, def] of Object.entries(APTS)) for (const s of SEEDS) runApartment(name, def, s);
const within3 = stats.t.filter((x) => x <= 3).length / stats.t.length;
check('3 cm noise: at least 90% of shared walls within 3 cm of their thickness', within3 >= 0.9, { share: +within3.toFixed(3), n: stats.t.length });
// a careful hand (1.5 cm per corner) and a perfect one: every shared wall within 3 cm, and exact
for (const [name, def] of Object.entries(APTS)) for (const s of [5, 6]) runApartment(name, def, s, { noise: 1.5 });
for (const [name, def] of Object.entries(APTS)) runApartment(name, def, 1, { noise: 0 });
// a measuring session can start facing any way: the plan comes out turned by a quarter turn at most, nothing else changes
for (const [name, def] of Object.entries(APTS)) {
  const T = truth(def), m = measure(T, 99, { ang: 127 * (Math.PI / 180) });
  const res = G.roomsToSegments(m.rooms, { openings: m.openings });
  const want = T.faces.map((f) => f.area).sort((a, b) => a - b), got = res.rooms.map((r) => r.area).sort((a, b) => a - b);
  check(name + ' turned 127 degrees: same rooms and areas (2%)', got.length === want.length && got.every((g, i) => pct(g, want[i]) <= 2), { got, want: want.map((x) => +x.toFixed(2)) });
  const wt = T.shared.map((w) => w.t).sort((a, b) => a - b);
  const gt = res.segments.map((s) => s.t);
  check(name + ' turned 127 degrees: every shared thickness present (3 cm)', wt.every((t) => gt.some((g) => Math.abs(g - t) <= 3)), { want: wt, got: [...new Set(gt)] });
  check(name + ' turned 127 degrees: openings kept', res.openings.length === T.openings.length);
}
// harder hands: 5 cm of noise still gives the rooms back
for (const [name, def] of Object.entries(APTS)) {
  const T = truth(def), m = measure(T, 7, { noise: 5 });
  const res = G.roomsToSegments(m.rooms, { openings: m.openings });
  check(name + ' with 5 cm noise: rooms and openings kept', res.rooms.length === T.faces.length && res.openings.length === T.openings.length, res.warnings);
}

const q = (a) => { const s = a.slice().sort((x, y) => x - y); return { max: +s[s.length - 1].toFixed(2), median: +s[s.length >> 1].toFixed(2), n: s.length }; };
console.log('\naccuracy. Thickness: 3 cm noise only (' + Object.keys(APTS).length + ' apartments x ' + SEEDS.length + ' measurements, turned up to 8 degrees). Areas and openings: the same 3 cm runs:');
console.log('  floor area error %        ', JSON.stringify(q(stats.area)));
console.log('  centre-line area error %  ', JSON.stringify(q(stats.gross)));
console.log('  engine net area error %   ', JSON.stringify(q(stats.net)));
console.log('  shared wall thickness cm  ', JSON.stringify(q(stats.t)));
console.log('  opening centre offset cm  ', JSON.stringify(q(stats.openPos)));
console.log('\n' + pass + ' passed, ' + fail + ' failed' + (fail ? ': ' + fails.slice(0, 12).join(' | ') : ''));
process.exit(fail ? 1 : 0);
