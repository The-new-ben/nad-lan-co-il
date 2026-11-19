// NadLan apartment designer core (HAD-701). First proven as the HAD-703 spike (docs/design-lab/apartment-designer/spike).
// One apartment model (nadlan-apartment v1) + one buyer design (nadlan-unit-design v2), changed ONLY through operations.
// No DOM and no three.js here: the same file runs in the browser, in node tests and, later, on the co-design channel.
// Frame: centimetres, origin at the plan's top-left, x to the right, y down, rotation in degrees clockwise.
import { STRINGS } from './strings.js';

const sub = (a, b) => [a[0] - b[0], a[1] - b[1]];
const dot = (a, b) => a[0] * b[0] + a[1] * b[1];
const crs = (a, b) => a[0] * b[1] - a[1] * b[0];
const hyp = (a) => Math.hypot(a[0], a[1]);
const r1 = (v) => Math.round(v * 10) / 10;
const r2 = (v) => Math.round(v * 100) / 100;
const num = (v) => typeof v === 'number' && Number.isFinite(v);
const pt2 = (p) => Array.isArray(p) && p.length === 2 && num(p[0]) && num(p[1]);
const clone = (o) => JSON.parse(JSON.stringify(o));
const RULE = STRINGS.he.rules;

export const WALL_KINDS = {
  facade: { he: 'קיר חזית', fixed: 'קיר החזית קבוע: החזית והחלונות שייכים לבניין כולו.' },
  structural: { he: 'קיר נושא', fixed: 'קיר נושא, חלק משלד הבניין. הוא לא זז.' },
  mamad: { he: 'קיר ממ״ד', fixed: 'קירות הממ״ד (המרחב המוגן) קבועים.' },
  rail: { he: 'מעקה', fixed: 'מעקה המרפסת קבוע.' },
  divider: { he: 'גבול בין חללים', fixed: 'זה גבול בין שני חללים פתוחים, אין כאן קיר להזיז.' },
  partition: { he: 'מחיצה', fixed: null },
};

// services points. h = the default height above the floor in cm; price = the record in data/price-ranges.json
export const POINT_KINDS = {
  socket: { h: 30, price: 'electric_point' }, switch: { h: 110, price: 'electric_point' }, data: { h: 30, price: 'electric_point' },
  tv: { h: 110, price: 'electric_point' }, ac: { h: 220, price: 'electric_point' }, light: { ceiling: true, price: 'lighting_point' },
};
// the names a new space may take (a short fixed list: the type decides which room rules apply to it)
export const SPACE_NAMES = STRINGS.he.spaceNames.map(([name_he, type]) => ({ name_he, type }));
const END_GAP = 5, OPEN_GAP = 5, MIN_PART = 60, PART_T = 10;

export function emptyDesign(apt) {
  return {
    schema: 'nadlan-unit-design', v: 2,
    project: apt.unit.project, unit_id: apt.unit.unit_id, geometry_revision: apt.geometry_revision,
    frame: { units: 'cm', origin: 'plan-top-left', rot: 'deg-cw' },
    geometry: { walls: {}, added: [], removed: [], rooms: [] }, finishes: {}, items: [], notes: [], log: [], rev: 0,
    points: { added: [], moved: {}, removed: [] },
  };
}

/** a design stored before points and partitions existed still opens: the missing parts start empty */
export function normDesign(d) {
  const g = (d.geometry = d.geometry || {});
  g.walls = g.walls || {}; g.added = g.added || []; g.removed = g.removed || []; g.rooms = g.rooms || [];
  const p = (d.points = d.points || {});
  p.added = p.added || []; p.moved = p.moved || {}; p.removed = p.removed || [];
  for (const k of ['items', 'notes', 'log']) d[k] = d[k] || [];
  d.finishes = d.finishes || {}; d.rev = d.rev || 0;
  return d;
}

function pip(p, poly) { // point in polygon
  let inside = false;
  for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
    const a = poly[i], b = poly[j];
    if ((a[1] > p[1]) !== (b[1] > p[1]) && p[0] < ((b[0] - a[0]) * (p[1] - a[1])) / (b[1] - a[1]) + a[0]) inside = !inside;
  }
  return inside;
}
/** distance from p to a wall's centre line, and where along the wall (s raw, c clamped to the wall) */
function segDist(p, w) {
  const s = dot(sub(p, w.pa), w.dir), c = Math.max(0, Math.min(w.L, s));
  return { s, c, d: Math.hypot(p[0] - w.pa[0] - w.dir[0] * c, p[1] - w.pa[1] - w.dir[1] * c) };
}
/** where segment a meets segment b, as a fraction of a; touching a's own ends does not count */
function cross(a0, a1, b0, b1) {
  const r = sub(a1, a0), s = sub(b1, b0), den = crs(r, s);
  if (Math.abs(den) < 1e-9) return null;
  const q = sub(b0, a0), t = crs(q, s) / den, u = crs(q, r) / den;
  return t > 0.002 && t < 0.998 && u > -0.002 && u < 1.002 ? t : null;
}
/** the room space (a face with a room) that holds p */
export const faceAt = (dv, p) => dv.faces.find((f) => f.room && pip(p, f.poly)) || null;
/** the wall nearest to p (skip(w) leaves walls out), with the place along it and the side of p (+1 along w.n) */
export function nearWall(dv, p, skip) {
  let best = null;
  for (const w of dv.walls) { if (w.L < 1 || (skip && skip(w))) continue; const r = segDist(p, w); if (!best || r.d < best.d) best = { w, s: r.c, d: r.d }; }
  if (best) best.side = dot(sub(p, best.w.pa), best.w.n) >= 0 ? 1 : -1;
  return best;
}
/** a point surely inside a space (for its label or a name): the middle of its box, else the first inside point of a grid */
/** The point of a space farthest from its walls (an approximate pole of inaccessibility): always inside, and in the
 *  wide part of an L-shaped room or a wrap-around balcony, where a label or a name belongs. Two grid passes. */
export function interior(f) {
  const P = f.poly, edge = (q) => { let d = Infinity; for (let i = 0, j = P.length - 1; i < P.length; j = i++) { const a = P[j], b = P[i], v = sub(b, a), L2 = dot(v, v) || 1, t = Math.max(0, Math.min(1, dot(sub(q, a), v) / L2)); d = Math.min(d, Math.hypot(q[0] - a[0] - v[0] * t, q[1] - a[1] - v[1] * t)); } return d; };
  let best = null, w = f.bb.x1 - f.bb.x0, h = f.bb.y1 - f.bb.y0, c = [f.bb.x0 + w / 2, f.bb.y0 + h / 2];
  for (const n of [12, 6]) {
    const sx = w / n, sy = h / n;
    for (let i = 0; i <= n; i++) for (let j = 0; j <= n; j++) {
      const q = [c[0] - w / 2 + sx * i, c[1] - h / 2 + sy * j];
      if (!pip(q, P)) continue;
      const d = edge(q); if (!best || d > best.d + 0.5) best = { q, d };
    }
    if (!best) break;
    c = best.q; w = sx * 2; h = sy * 2; // the second pass looks closer around the best point
  }
  return best ? best.q : [(f.bb.x0 + f.bb.x1) / 2, (f.bb.y0 + f.bb.y1) / 2];
}
/** an axis-aligned rectangle once the corners that lie on a straight line (split points, a free wall end) are dropped */
function rectangular(poly) {
  let p = poly.slice();
  for (let changed = true; changed && p.length > 3;) {
    changed = false;
    for (let i = 0; i < p.length; i++) {
      const a = p[(i + p.length - 1) % p.length], b = p[i], c = p[(i + 1) % p.length];
      if (Math.abs(crs(sub(b, a), sub(c, b))) < 1 || Math.hypot(b[0] - a[0], b[1] - a[1]) < 0.5) { p.splice(i, 1); changed = true; break; }
    }
  }
  if (p.length !== 4) return false;
  for (let i = 0; i < 4; i++) { const a = p[i], b = p[(i + 1) % 4]; if (Math.abs(a[0] - b[0]) > 0.5 && Math.abs(a[1] - b[1]) > 0.5) return false; }
  return true;
}

function findFaces(nodes, walls, rooms) {
  const out = {};
  const push = (u, v, w) => (out[u] = out[u] || []).push({ u, v, w, ang: Math.atan2(nodes[v][1] - nodes[u][1], nodes[v][0] - nodes[u][0]) });
  for (const w of walls) { if (w.L < 0.01) continue; push(w.a, w.b, w); push(w.b, w.a, w); }
  for (const k in out) out[k].sort((p, q) => p.ang - q.ang);
  const seen = new Set(), raw = [];
  const key = (h) => h.u + '>' + h.v + '>' + h.w.id;
  for (const k in out) for (const h0 of out[k]) {
    if (seen.has(key(h0))) continue;
    const ring = []; let h = h0, guard = 0;
    while (!seen.has(key(h)) && guard++ < 2000) {
      seen.add(key(h)); ring.push(h);
      const list = out[h.v], i = list.findIndex((x) => x.v === h.u && x.w === h.w);
      h = list[(i + 1) % list.length]; // the next wall around the corner: walks one face (a free end turns back on itself)
    }
    const poly = ring.map((x) => nodes[x.u]); let A = 0;
    for (let i = 0; i < poly.length; i++) { const p = poly[i], q = poly[(i + 1) % poly.length]; A += p[0] * q[1] - q[0] * p[1]; }
    raw.push({ ring, poly, signed: A / 2 });
  }
  let outer = 0; raw.forEach((f, i) => { if (Math.abs(f.signed) > Math.abs(raw[outer].signed)) outer = i; });
  raw.splice(outer, 1); // the unbounded face is the largest one
  const near = (a, b) => Math.abs(a - b) < 0.5;
  return raw.filter((f) => Math.abs(f.signed) > 1).map((f, i) => {
    const inside = rooms.filter((r) => pip(r.at, f.poly)), room = inside[0] || null;
    const xs = f.poly.map((p) => p[0]), ys = f.poly.map((p) => p[1]);
    const bb = { x0: Math.min(...xs), y0: Math.min(...ys), x1: Math.max(...xs), y1: Math.max(...ys) };
    let half = 0; const side = { l: 0, r: 0, t: 0, b: 0 }, sides = {};
    for (const h of f.ring) {
      const w = h.w, t = w.t || 0, p = nodes[h.u], q = nodes[h.v]; half += (w.L * t) / 2;
      const id = w.parent || w.id; if (!(id in sides)) sides[id] = h.u === w.a ? 'ab' : 'ba';
      if (near(p[0], bb.x0) && near(q[0], bb.x0)) side.l = Math.max(side.l, t);
      if (near(p[0], bb.x1) && near(q[0], bb.x1)) side.r = Math.max(side.r, t);
      if (near(p[1], bb.y0) && near(q[1], bb.y0)) side.t = Math.max(side.t, t);
      if (near(p[1], bb.y1) && near(q[1], bb.y1)) side.b = Math.max(side.b, t);
    }
    const gross = Math.abs(f.signed) / 1e4, rect = rectangular(f.poly);
    return {
      id: room ? room.id : 'void' + i, room, merged: inside.slice(1).map((r) => r.id), poly: f.poly,
      walls: Object.keys(sides), sides, gross: r1(gross), net: r1(gross - half / 1e4), bb,
      // a clear width and depth only where they are true: an axis-aligned rectangle. A turned or L-shaped room shows its area only.
      rect, clearW: rect ? Math.round(bb.x1 - bb.x0 - (side.l + side.r) / 2) : null, clearD: rect ? Math.round(bb.y1 - bb.y0 - (side.t + side.b) / 2) : null,
      perimeter: Math.round(f.ring.reduce((s, h) => s + h.w.L, 0)),
    };
  });
}

/** why a wall point cannot sit at `at` (cm from the wall's current a-end), or null */
function wallPointProblem(w, at) {
  if (w.kind === 'rail' || w.kind === 'divider') return 'point.' + w.kind;
  if (at < END_GAP || at > w.L - END_GAP) return 'point.end';
  for (const o of w.openings || []) if (at > o.at - OPEN_GAP && at < o.at + o.w + OPEN_GAP) return o.type === 'door' ? 'point.door' : 'point.window';
  return null;
}

/** Everything both views draw is derived here, from the base apartment plus the design's geometry changes. */
export function derive(apt, design) {
  const G = design.geometry || {}, shifts = G.walls || {}, gone = new Set(G.removed || []), added = G.added || [];
  const nodes = {}, base = {};
  for (const k in apt.nodes) nodes[k] = [apt.nodes[k][0], apt.nodes[k][1]];
  for (const w of apt.walls) {
    const a = apt.nodes[w.a], v = sub(apt.nodes[w.b], a), L = hyp(v);
    base[w.id] = { dir: [v[0] / L, v[1] / L], n: [v[1] / L, -v[0] / L] };
    const d = gone.has(w.id) ? 0 : +shifts[w.id] || 0; // a removed partition's slide no longer moves anything
    if (d) for (const k of [w.a, w.b]) { nodes[k][0] += base[w.id].n[0] * d; nodes[k][1] += base[w.id].n[1] * d; }
  }
  const walls = [], ghosts = [];
  for (const w of apt.walls) {
    const pa = nodes[w.a], pb = nodes[w.b], v = sub(pb, pa), L = hyp(v), b = base[w.id];
    (gone.has(w.id) ? ghosts : walls).push({
      ...w, pa, pb, L, dir: L ? [v[0] / L, v[1] / L] : b.dir, n: b.n, baseDir: b.dir, shift: gone.has(w.id) ? 0 : +shifts[w.id] || 0,
      slide: dot(sub(pa, apt.nodes[w.a]), b.dir), // how far the a-end slid along the wall's own line
      flipped: dot(v, b.dir) <= 0,
    });
  }
  const wallBy = Object.fromEntries(walls.map((w) => [w.id, w]));

  // added partitions. An end that lies on a wall splits that wall for the room finder only: the wall itself, with its
  // openings and points, stays whole, so nothing on it moves. An end in open space is a free end.
  const mk = (a, pa, pb, na, nb) => { const v = sub(pb, pa), L = hyp(v), dir = L ? [v[0] / L, v[1] / L] : [1, 0]; return { id: a.id, a: na, b: nb, t: a.t || PART_T, kind: 'partition', added: true, pa, pb, L, dir, n: [dir[1], -dir[0]], baseDir: dir, shift: 0, slide: 0, flipped: false, openings: [] }; };
  const hostIn = (list, p, self) => {
    let best = null;
    for (const w of list) {
      if (w.id === self || w.L < 1) continue;
      const r = segDist(p, w);
      if (r.s < -0.6 || r.s > w.L + 0.6 || r.d > Math.max((w.t || 0) / 2, 1) + 1) continue;
      if (!best || r.d < best.d) best = { w, s: r.c, d: r.d };
    }
    return best;
  };
  const onLine = (p, h) => (h ? [h.w.pa[0] + h.w.dir[0] * h.s, h.w.pa[1] + h.w.dir[1] * h.s] : [p[0], p[1]]);
  const raw = added.filter((a) => pt2(a.a) && pt2(a.b)).map((a) => ({ a, ends: [a.a, a.b].map((p) => hostIn(walls, p, a.id)) }));
  const prov = raw.map(({ a, ends }) => mk(a, onLine(a.a, ends[0]), onLine(a.b, ends[1])));
  for (const r of raw) for (const j of [0, 1]) if (!r.ends[j]) r.ends[j] = hostIn(prov, j ? r.a.b : r.a.a, r.a.id); // an end may rest on another new partition
  const splits = {}, hosts = {};
  const nodeAt = (p) => { for (const k in nodes) if (Math.abs(nodes[k][0] - p[0]) < 0.6 && Math.abs(nodes[k][1] - p[1]) < 0.6) return k; return null; };
  for (const { a, ends } of raw) {
    const ids = ends.map((h, j) => {
      const p = onLine(j ? a.b : a.a, h), k = nodeAt(p);
      if (k) return k;
      const id = a.id + (j ? ':b' : ':a'); nodes[id] = p;
      if (h) (splits[h.w.id] = splits[h.w.id] || []).push({ s: h.s, node: id });
      return id;
    });
    hosts[a.id] = ends.map((h) => (h ? h.w.id : null));
    const w = mk(a, nodes[ids[0]], nodes[ids[1]], ids[0], ids[1]);
    walls.push(w); wallBy[w.id] = w;
  }
  const edges = []; // the graph the room finder walks: whole walls, or the pieces of a split wall (parent = the wall)
  for (const w of walls) {
    if (w.L < 0.01) continue;
    const sp = (splits[w.id] || []).sort((p, q) => p.s - q.s);
    if (!sp.length) { edges.push(w); continue; }
    let prev = w.a, ps = 0, k = 0;
    for (const x of sp) { if (x.node === prev) continue; edges.push({ id: w.id + '#' + k++, parent: w.id, a: prev, b: x.node, L: x.s - ps, t: w.t }); prev = x.node; ps = x.s; }
    edges.push({ id: w.id + '#' + k, parent: w.id, a: prev, b: w.b, L: w.L - ps, t: w.t });
  }
  // a window or a door keeps its place in the building when the corner next to it moves; it goes with a removed partition
  const openings = apt.openings.filter((o) => wallBy[o.wall]).map((o) => ({ ...o, at: o.at - wallBy[o.wall].slide }));
  for (const w of walls) w.openings = openings.filter((o) => o.wall === w.id).sort((p, q) => p.at - q.at);

  const rooms = apt.rooms.concat((G.rooms || []).filter((r) => pt2(r.at)).map((r) => ({ ...r, design: true })));
  const faces = findFaces(nodes, edges, rooms);
  // a space cut off by a new partition, with no room point in it, is a new space until the buyer names it
  const addedIds = new Set(added.map((a) => a.id));
  for (const f of faces) {
    if (f.room) continue;
    const mine = f.walls.filter((id) => addedIds.has(id)).sort();
    if (!mine.length) continue;
    f.id = 'sp-' + mine[0] + '-' + f.sides[mine[0]];
    f.room = { id: f.id, type: 'other', name_he: STRINGS.he.newSpace, fresh: true };
  }
  for (const f of faces) if (f.room && (f.room.fresh || f.room.design) && !f.room.floor) { // it keeps the floor of the room it was cut from
    const nb = faces.find((g) => g !== f && g.room && !g.room.fresh && !g.room.design && g.walls.some((id) => addedIds.has(id) && f.walls.includes(id)));
    f.room.floor = nb ? nb.room.floor : (apt.rooms[0] && apt.rooms[0].floor) || null;
  }
  const faceBy = Object.fromEntries(faces.map((f) => [f.id, f]));
  const dv = { nodes, walls, wallBy, openings, faces, faceBy, ghosts, hosts, edges, points: [], pointBy: {} };

  // services points: a wall point keeps its place in the building when a corner next to it slides, exactly like an opening
  const P = design.points || {}, rmP = new Set(P.removed || []), mvP = P.moved || {};
  const place = (p, state) => {
    const k = POINT_KINDS[p.kind]; if (!k) return null;
    const o = { ...p, state, h: num(p.h) ? p.h : k.h || null };
    if (k.ceiling) { const f = faceAt(dv, [p.x, p.y]); o.room = f ? f.id : null; o.bad = f ? null : 'point.outside'; return o; }
    const w = wallBy[p.wall];
    if (!w) { o.lost = true; o.bad = 'point.wall'; return o; }
    const at = p.at - w.slide, t = (w.t || 0) / 2, x = w.pa[0] + w.dir[0] * at, y = w.pa[1] + w.dir[1] * at;
    let side = 0;
    for (const s of [1, -1]) { const f = faceAt(dv, [x + w.n[0] * s * (t + 8), y + w.n[1] * s * (t + 8)]); if (f && (f.id === p.room || f.merged.includes(p.room))) { side = s; break; } }
    if (!side) side = faceAt(dv, [x + w.n[0] * (t + 8), y + w.n[1] * (t + 8)]) ? 1 : -1;
    const ns = [w.n[0] * side, w.n[1] * side];
    return Object.assign(o, { atEff: at, x, y, side, ns, fx: x + ns[0] * t, fy: y + ns[1] * t, bad: wallPointProblem(w, at) });
  };
  for (const b of apt.points || []) { const m = rmP.has(b.id) ? null : mvP[b.id], o = place(m ? { ...b, ...m } : b, rmP.has(b.id) ? 'removed' : m ? 'moved' : 'base'); if (o) dv.points.push(o); }
  for (const a of P.added || []) { const o = place(a, 'added'); if (o) dv.points.push(o); }
  for (const p of dv.points) dv.pointBy[p.id] = p;
  return dv;
}

const rej = (code, reason) => ({ code, reason: reason || RULE[code] || code });

/** A partition can slide only when both of its ends ride along walls that run across it (never out of a corner). */
export function canSlide(apt, id) {
  const w = apt.walls.find((x) => x.id === id);
  if (!w || WALL_KINDS[w.kind].fixed) return false;
  const v = sub(apt.nodes[w.b], apt.nodes[w.a]), n = [v[1], -v[0]];
  for (const k of [w.a, w.b]) for (const o of apt.walls) {
    if (o.id === id || (o.a !== k && o.b !== k)) continue;
    const ov = sub(apt.nodes[o.b], apt.nodes[o.a]);
    if (Math.abs(crs(ov, n)) / (hyp(ov) * hyp(n)) > 1e-6) return false;
  }
  return true;
}

/** the minimum width and area rules of a room, for every room the wall `id` bounds (name = the name the sentence uses) */
function roomRules(apt, dv, id, only) {
  for (const f of dv.faces) {
    if (!f.room || (id && !f.walls.includes(id)) || (only && f !== only.face)) continue;
    const type = only ? only.type : f.room.type, name = only ? only.name_he : f.room.name_he;
    for (const r of apt.rules || []) {
      if (!r.applies.includes(type)) continue;
      // the width rule reads the clear size, which only a rectangle has; a room of any shape still answers to the area rule
      if (r.code === 'room.min_width' && f.clearW != null && Math.min(f.clearW, f.clearD) < r.value) return rej(r.code, name + ': החדר יהיה צר מ-' + (r.value / 100).toFixed(2) + ' מ׳.');
      if (r.code === 'room.min_area' && f.net < r.value) return rej(r.code, name + ': החדר יהיה קטן מ-' + r.value + ' מ״ר.');
    }
  }
  return null;
}
/** the first wall a new partition crosses, or null */
function crossing(dv, w) {
  for (const o of dv.walls) if (o.id !== w.id && o.L >= 1 && cross(w.pa, w.pb, o.pa, o.pb) != null) return o;
  return null;
}
const withGeo = (design, g) => ({ ...design, geometry: { ...design.geometry, ...g } });

function checkShift(apt, design, dv0, id, d) {
  const w0 = apt.walls.find((w) => w.id === id);
  if (!w0) return rej('wall.unknown', 'הקיר הזה לא מוכר.');
  const kind = WALL_KINDS[w0.kind];
  if (!kind || kind.fixed) return rej('wall.fixed.' + w0.kind, kind ? kind.fixed : 'הקיר הזה קבוע.');
  if (design.geometry.removed.includes(id)) return rej('partition.gone');
  const next = withGeo(design, { walls: { ...design.geometry.walls, [id]: d } });
  const dv = derive(apt, next), w = dv.wallBy[id], m = 10 + (w0.t || 0) / 2;
  for (const k of [w0.a, w0.b]) {
    for (const o of dv.walls) {
      if (o.id === id || (o.a !== k && o.b !== k)) continue;
      if (Math.abs(crs(o.baseDir, w.n)) > 1e-6) return rej('wall.corner', 'המחיצה מחוברת לפינה, והיא לא יכולה להחליק לכיוון הזה.');
      if (o.flipped || o.L < 30) return rej('wall.span', 'אין מקום: המחיצה הגיעה לקיר הסמוך.');
      for (const op of o.openings) {
        const hit = o.a === k ? op.at < m : op.at + op.w > o.L - m;
        if (hit) return rej('wall.opening', op.type === 'door' ? 'המחיצה נתקעת בדלת. הדלת נשארת במקומה.' : 'המחיצה נתקעת בחלון. החלונות שייכים לחזית ולא זזים.');
      }
    }
  }
  // what rests on the walls around it stays where it is in the building, so it has to still fit after the slide
  for (const k in dv0.hosts) if (String(dv0.hosts[k]) !== String(dv.hosts[k])) return rej('wall.leans');
  for (const a of dv.walls) if (a.added && crossing(dv, a)) return rej('wall.leans');
  for (const p of dv.points) if (p.state !== 'removed' && p.bad && !(dv0.pointBy[p.id] || {}).bad) return rej('wall.point');
  return roomRules(apt, dv, id);
}

export function createStore(apt, design0) {
  let design = normDesign(clone(design0 || emptyDesign(apt)));
  let dv = derive(apt, design);
  const subs = new Set(), undo = [], redo = [], slideCache = {};
  const placeItems = () => { for (const it of design.items) it.room = roomAt(it.x, it.y); }; // the room of a piece is computed, never typed
  let guard = null; // who may change the design right now (the shared call sets it: only the pen holder edits)
  const emit = (e) => subs.forEach((f) => f(e));
  const item = (id) => design.items.find((i) => i.id === id);
  const note = (id) => design.notes.find((n) => n.id === id);
  // a note to the builder: plain text, one paragraph, at most 400 characters (no markup, no control characters)
  const noteText = (t) => (typeof t === 'string' ? t.replace(/[\u0000-\u001f\u007f<>]/g, ' ').replace(/\s+/g, ' ').trim().slice(0, 400) : '');
  const roomAt = (x, y) => { const f = faceAt(dv, [x, y]) || dv.faces.find((q) => pip([x, y], q.poly)); return f ? f.id : null; };
  const basePt = (id) => (apt.points || []).find((p) => p.id === id);
  const addedPt = (id) => design.points.added.find((p) => p.id === id);
  const addedPart = (id) => design.geometry.added.find((a) => a.id === id);
  const placeOf = (p) => (POINT_KINDS[p.kind].ceiling ? { x: p.x, y: p.y } : { wall: p.wall, at: p.at, room: p.room });
  const samePlace = (b, to) => (POINT_KINDS[b.kind].ceiling ? b.x === to.x && b.y === to.y : b.wall === to.wall && b.at === to.at && (to.room == null || to.room === b.room));

  /** why point p cannot stand where it says (base = its record in the specification, if it has one) */
  function placeProblem(p, base) {
    const k = POINT_KINDS[p.kind];
    if (k.ceiling) {
      if (!num(p.x) || !num(p.y)) return rej('point.kind');
      const f = faceAt(dv, [p.x, p.y]);
      if (!f) return rej('point.outside');
      // the safe room: rule mamad.no_chasing in the apartment data. Its source is TO BE VERIFIED before any public use.
      if (f.room.type === 'mamad' && !(base && samePlace(base, p))) return rej('point.mamad');
      return null;
    }
    if (typeof p.wall !== 'string' || !num(p.at)) return rej('point.kind');
    const w = dv.wallBy[p.wall];
    if (!w) return rej('point.wall');
    const bad = wallPointProblem(w, p.at - w.slide);
    if (bad) return rej(bad);
    if (w.kind === 'mamad' && !(base && samePlace(base, p))) return rej('point.mamad'); // the same placeholder rule, to be verified
    return null;
  }
  function checkPartAdd(a) {
    if (!a || typeof a.id !== 'string' || !/^[a-z0-9_-]{1,40}$/.test(a.id) || !pt2(a.a) || !pt2(a.b) || (a.t != null && !(a.t >= 5 && a.t <= 20))) return rej('partition.bad');
    if (apt.walls.some((w) => w.id === a.id) || addedPart(a.id)) return rej('partition.exists');
    const dv2 = derive(apt, withGeo(design, { added: [...design.geometry.added, { t: PART_T, ...a }] })), w = dv2.wallBy[a.id];
    const hw = dv2.hosts[a.id].map((h) => h && dv2.wallBy[h]);
    if (!hw[0] && !hw[1]) return rej('partition.free');
    for (const h of hw) if (h && h.kind === 'rail') return rej('partition.rail');
    for (const h of hw) if (h && h.kind === 'mamad') return rej('partition.mamad'); // placeholder rule, to be verified
    const start = hw[0] || hw[1], c = Math.abs(crs(w.dir, start.dir)), along = c < 0.0088; // 0.5 degree either way
    if (!along && c < 0.99996) return rej('partition.angle');
    if (w.L < MIN_PART) return rej('partition.short');
    for (let j = 0; j < 2; j++) { // each end stays clear of the doors, windows and points of the wall it meets
      const h = hw[j]; if (!h) continue;
      const s = segDist(j ? w.pb : w.pa, h).c, m = w.t / 2 + OPEN_GAP;
      for (const o of h.openings) if (s > o.at - m && s < o.at + o.w + m) return rej('partition.opening');
      for (const p of dv2.points) if (p.wall === h.id && p.state !== 'removed' && num(p.atEff) && Math.abs(p.atEff - s) < m) return rej('partition.point');
    }
    const o = crossing(dv2, w);
    if (o) return rej(o.added ? 'partition.cross' : 'partition.through');
    const mid = [(w.pa[0] + w.pb[0]) / 2, (w.pa[1] + w.pb[1]) / 2];
    if (along && segDist(mid, start).d < (start.t || 0) / 2 + w.t / 2 + 1) return rej('partition.through');
    const f = faceAt(dv, mid);
    if (!f) return rej('partition.outside');
    if (f.room.type === 'balcony') return rej('partition.balcony');
    if (f.room.type === 'mamad') return rej('partition.mamad');
    return roomRules(apt, dv2, a.id);
  }
  function checkPartRemove(id) {
    if (!addedPart(id)) {
      const w0 = apt.walls.find((w) => w.id === id);
      if (!w0) return rej('wall.unknown', 'הקיר הזה לא מוכר.');
      if (w0.kind !== 'partition') { const k = WALL_KINDS[w0.kind]; return rej('wall.fixed.' + w0.kind, k ? k.fixed : 'הקיר הזה קבוע.'); }
      if (design.geometry.removed.includes(id)) return rej('partition.gone');
    }
    if (dv.points.some((p) => p.wall === id && p.state !== 'removed')) return rej('partition.points');
    for (const k in dv.hosts) if (k !== id && dv.hosts[k].includes(id)) return rej('partition.leans');
    return null;
  }
  function checkPartRestore(id) {
    if (!design.geometry.removed.includes(id)) return rej('partition.notgone');
    const dv2 = derive(apt, withGeo(design, { removed: design.geometry.removed.filter((x) => x !== id) })), w = dv2.wallBy[id];
    for (const a of dv2.walls) if (a.added && cross(a.pa, a.pb, w.pa, w.pb) != null) return rej('partition.blocked');
    return null;
  }
  function checkRoomName(op) {
    if (!pt2(op.at)) return rej('room.name.base');
    const f = faceAt(dv, op.at);
    if (!f || !(f.room.fresh || f.room.design)) return rej('room.name.base');
    if (op.name_he == null) return f.room.design ? null : rej('room.name.same');
    const n = SPACE_NAMES.find((x) => x.name_he === op.name_he && x.type === op.type);
    if (!n) return rej('room.name.list');
    return roomRules(apt, dv, null, { face: f, type: n.type, name_he: n.name_he });
  }

  function check(op) {
    switch (op.op) {
      case 'item.add': return item(op.item.id) ? rej('item.exists', 'הפריט כבר קיים.') : roomAt(op.item.x, op.item.y) ? null : rej('item.outside', 'הפריט מחוץ לדירה.');
      case 'item.move': return !item(op.id) ? rej('item.unknown', 'הפריט לא נמצא.') : roomAt(op.x, op.y) ? null : rej('item.outside', 'הפריט מחוץ לדירה.');
      case 'item.rot': case 'item.remove': return item(op.id) ? null : rej('item.unknown', 'הפריט לא נמצא.');
      case 'finish.set': return /^(floor|wall):[a-z0-9_-]+$/.test(op.key) && (op.value == null || /^[a-z0-9_-]{1,40}$/.test(op.value)) ? null : rej('finish.key', 'משטח לא מוכר.');
      case 'note.add': {
        const n = op.note;
        if (!n || typeof n.id !== 'string' || !/^[a-z0-9_-]{1,40}$/.test(n.id) || !num(n.x) || !num(n.y)) return rej('note.bad', 'הערה לא תקינה.');
        if (note(n.id)) return rej('note.exists', 'ההערה כבר קיימת.');
        if (design.notes.length >= 60) return rej('note.many', 'אפשר עד 60 הערות לדירה.');
        if (!noteText(n.text)) return rej('note.empty', 'כתבו מה לבקש מהקבלן.');
        return roomAt(n.x, n.y) ? null : rej('note.outside', 'ההערה מחוץ לדירה.');
      }
      case 'note.edit': return !note(op.id) ? rej('note.unknown', 'ההערה לא נמצאה.') : noteText(op.text) ? null : rej('note.empty', 'כתבו מה לבקש מהקבלן.');
      case 'note.move': return !note(op.id) ? rej('note.unknown', 'ההערה לא נמצאה.') : num(op.x) && num(op.y) && roomAt(op.x, op.y) ? null : rej('note.outside', 'ההערה מחוץ לדירה.');
      case 'note.remove': return note(op.id) ? null : rej('note.unknown', 'ההערה לא נמצאה.');
      case 'wall.shift': return checkShift(apt, design, dv, op.id, op.d);
      case 'point.add': {
        const p = op.point;
        if (!p || typeof p.id !== 'string' || !/^[a-z0-9_-]{1,40}$/.test(p.id) || !POINT_KINDS[p.kind]) return rej('point.kind');
        return dv.pointBy[p.id] ? rej('point.exists') : placeProblem(p, null);
      }
      case 'point.move': {
        const p = dv.pointBy[op.id];
        if (!p) return rej('point.unknown');
        if (p.state === 'removed') return rej('point.gone');
        const to = POINT_KINDS[p.kind].ceiling ? { kind: p.kind, x: op.x, y: op.y } : { kind: p.kind, wall: op.wall, at: op.at, room: op.room };
        return placeProblem(to, basePt(op.id));
      }
      case 'point.remove': { const p = dv.pointBy[op.id]; return !p ? rej('point.unknown') : p.state === 'removed' ? rej('point.gone') : null; }
      case 'point.restore': return basePt(op.id) ? null : rej('point.restore'); // back to the specification is always allowed
      case 'partition.add': return checkPartAdd(op.wall);
      case 'partition.remove': return checkPartRemove(op.id);
      case 'partition.restore': return checkPartRestore(op.id);
      case 'room.name': return checkRoomName(op);
      default: return rej('op.unknown', 'פעולה לא מוכרת.');
    }
  }
  /** a change that is allowed but must be said out loud */
  function warning(op) {
    if (op.op === 'partition.remove' && dv.faces.some((f) => f.room && f.walls.includes(op.id) && f.room.type === 'wet')) return { code: 'partition.wet', reason: RULE['partition.wet'] };
    return null;
  }
  function inverse(op) {
    const it = op.id && item(op.id), P = design.points, G = design.geometry;
    switch (op.op) {
      case 'item.add': return { op: 'item.remove', id: op.item.id };
      case 'item.remove': return { op: 'item.add', item: { ...it } };
      case 'item.move': return { op: 'item.move', id: op.id, x: it.x, y: it.y };
      case 'item.rot': return { op: 'item.rot', id: op.id, rot: it.rot };
      case 'finish.set': return { op: 'finish.set', key: op.key, value: design.finishes[op.key] || null };
      case 'wall.shift': return { op: 'wall.shift', id: op.id, d: G.walls[op.id] || 0 };
      case 'point.add': return { op: 'point.remove', id: op.point.id };
      case 'point.remove': {
        const a = addedPt(op.id);
        if (a) return { op: 'point.add', point: clone(a) };
        return P.moved[op.id] ? { op: 'point.restore', id: op.id, to: clone(P.moved[op.id]) } : { op: 'point.restore', id: op.id };
      }
      case 'point.move': {
        const a = addedPt(op.id);
        if (a) return { op: 'point.move', id: op.id, ...placeOf(a) };
        return P.moved[op.id] ? { op: 'point.move', id: op.id, ...clone(P.moved[op.id]) } : { op: 'point.restore', id: op.id };
      }
      case 'point.restore':
        if (P.removed.includes(op.id)) return { op: 'point.remove', id: op.id };
        return P.moved[op.id] ? { op: 'point.move', id: op.id, ...clone(P.moved[op.id]) } : { op: 'point.restore', id: op.id };
      case 'partition.add': return { op: 'partition.remove', id: op.wall.id };
      case 'partition.remove': { const a = addedPart(op.id); return a ? { op: 'partition.add', wall: clone(a) } : { op: 'partition.restore', id: op.id }; }
      case 'partition.restore': return { op: 'partition.remove', id: op.id };
      case 'note.add': return { op: 'note.remove', id: op.note.id };
      case 'note.remove': return { op: 'note.add', note: clone(note(op.id)) };
      case 'note.edit': return { op: 'note.edit', id: op.id, text: note(op.id).text };
      case 'note.move': return { op: 'note.move', id: op.id, x: note(op.id).x, y: note(op.id).y };
      case 'room.name': {
        const f = faceAt(dv, op.at), prev = f && G.rooms.find((r) => r.id === f.id);
        return prev ? { op: 'room.name', at: [...prev.at], name_he: prev.name_he, type: prev.type } : { op: 'room.name', at: [...op.at], name_he: null };
      }
    }
  }
  // stored lists are kept in one order (by id), so a change and its undo leave the very same document
  const byId = (p, q) => (p.id < q.id ? -1 : p.id > q.id ? 1 : 0);
  const sortKeys = (o) => Object.fromEntries(Object.keys(o).sort().map((k) => [k, o[k]]));
  function canon() {
    const P = design.points, G = design.geometry;
    P.added.sort(byId); P.removed.sort(); P.moved = sortKeys(P.moved);
    G.added.sort(byId); G.removed.sort(); G.rooms.sort(byId); G.walls = sortKeys(G.walls);
  }
  function mutate(op) {
    const t = { items: [], finishes: [], points: [], notes: [], geometry: false }, P = design.points, G = design.geometry;
    const regeo = () => { canon(); dv = derive(apt, design); t.geometry = true; placeItems(); };
    switch (op.op) {
      case 'item.add': design.items.push({ ...op.item, room: roomAt(op.item.x, op.item.y) }); t.items.push(op.item.id); break;
      case 'item.remove': design.items = design.items.filter((i) => i.id !== op.id); t.items.push(op.id); break;
      case 'item.move': { const it = item(op.id); it.x = op.x; it.y = op.y; it.room = roomAt(op.x, op.y); t.items.push(op.id); break; }
      case 'item.rot': item(op.id).rot = ((op.rot % 360) + 360) % 360; t.items.push(op.id); break;
      case 'finish.set': if (op.value) design.finishes[op.key] = op.value; else delete design.finishes[op.key]; t.finishes.push(op.key); break;
      case 'wall.shift': if (op.d) G.walls[op.id] = op.d; else delete G.walls[op.id]; regeo(); break;
      case 'point.add': {
        const p = op.point, k = POINT_KINDS[p.kind];
        P.added.push(k.ceiling ? { id: p.id, kind: p.kind, x: p.x, y: p.y } : { id: p.id, kind: p.kind, wall: p.wall, at: p.at, room: p.room || null, ...(num(p.h) ? { h: p.h } : {}) });
        t.points.push(p.id); break;
      }
      case 'point.move': {
        const a = addedPt(op.id), kind = (a || basePt(op.id)).kind, to = POINT_KINDS[kind].ceiling ? { x: op.x, y: op.y } : { wall: op.wall, at: op.at, room: op.room || null };
        if (a) Object.assign(a, to);
        else if (samePlace(basePt(op.id), to)) delete P.moved[op.id]; // back on its place in the specification
        else P.moved[op.id] = to;
        t.points.push(op.id); break;
      }
      case 'point.remove':
        if (addedPt(op.id)) P.added = P.added.filter((p) => p.id !== op.id);
        else { P.removed.push(op.id); delete P.moved[op.id]; }
        t.points.push(op.id); break;
      case 'point.restore':
        P.removed = P.removed.filter((x) => x !== op.id);
        if (op.to) P.moved[op.id] = clone(op.to); else delete P.moved[op.id];
        t.points.push(op.id); break;
      case 'partition.add': G.added.push({ id: op.wall.id, a: [op.wall.a[0], op.wall.a[1]], b: [op.wall.b[0], op.wall.b[1]], t: op.wall.t || PART_T }); regeo(); break;
      case 'partition.remove': if (addedPart(op.id)) G.added = G.added.filter((a) => a.id !== op.id); else G.removed.push(op.id); regeo(); break;
      case 'partition.restore': G.removed = G.removed.filter((x) => x !== op.id); regeo(); break;
      case 'note.add': { const n = op.note; design.notes.push({ id: n.id, x: Math.round(n.x), y: Math.round(n.y), text: noteText(n.text), room: roomAt(n.x, n.y), at: n.at || new Date().toISOString() }); design.notes.sort(byId); t.notes.push(n.id); break; }
      case 'note.edit': { const n = note(op.id); n.text = noteText(op.text); t.notes.push(op.id); break; }
      case 'note.move': { const n = note(op.id); n.x = Math.round(op.x); n.y = Math.round(op.y); n.room = roomAt(n.x, n.y); t.notes.push(op.id); break; }
      case 'note.remove': design.notes = design.notes.filter((n) => n.id !== op.id); t.notes.push(op.id); break;
      case 'room.name': {
        const id = faceAt(dv, op.at).id;
        G.rooms = G.rooms.filter((r) => r.id !== id);
        if (op.name_he) G.rooms.push({ id, at: [r1(op.at[0]), r1(op.at[1])], name_he: op.name_he, type: op.type });
        regeo(); break;
      }
    }
    if (t.points.length) { canon(); dv = derive(apt, design); }
    return t;
  }
  /** meta: { by, gesture, replay }. One drag is one gesture: one undo step and one line in the decision log. */
  function apply(op, meta = {}) {
    const t0 = typeof performance !== 'undefined' ? performance.now() : 0;
    // meta.remote: a change that arrived from another person in the call: it is logged with its author, never put on MY undo stack,
    // and never asked of the guard (the sender's side already was). meta.replay: my own undo or redo.
    const err = (guard && !meta.remote ? guard(op, meta) : null) || check(op);
    if (err) { emit({ type: 'reject', op, ...err }); return { ok: false, ...err }; }
    const warn = warning(op), inv = inverse(op), touched = mutate(op);
    design.rev += 1;
    if (!meta.replay && !meta.remote) {
      const top = undo[undo.length - 1];
      if (meta.gesture && top && top.gesture === meta.gesture) top.redo = op;
      else { undo.push({ inv, redo: op, gesture: meta.gesture || null }); redo.length = 0; }
    }
    if (!meta.replay) {
      const last = design.log[design.log.length - 1], entry = { n: design.rev, t: new Date().toISOString(), by: meta.by || 'buyer', op };
      if (meta.gesture && last && last.gesture === meta.gesture) Object.assign(last, entry, { gesture: meta.gesture });
      else design.log.push({ ...entry, gesture: meta.gesture || null });
    }
    emit({ type: 'change', op, touched, t0, by: meta.by || 'buyer', remote: !!meta.remote, replay: !!meta.replay, gesture: meta.gesture || null, warn });
    if (t0) api.lastApplyMs = performance.now() - t0; // the model change plus both views patching themselves
    return warn ? { ok: true, warn } : { ok: true };
  }
  function step(from, to, pick) {
    const e = from.pop(); if (!e) return false;
    const r = apply(e[pick], { replay: true });
    if (r.ok) to.push(e);
    return r.ok;
  }
  placeItems();
  const api = {
    lastApplyMs: 0, apt, apply, check,
    /** fn(op, meta) returns null to allow, or { code, reason } to refuse with one sentence the person reads */
    setGuard(fn) { guard = fn || null; },
    /** replaces the whole design (a saved design opened again, or the full design a late joiner of a call receives) */
    load(next) { design = normDesign(clone(next)); dv = derive(apt, design); placeItems(); undo.length = 0; redo.length = 0; emit({ type: 'change', op: { op: 'design.load' }, touched: { items: design.items.map((i) => i.id), finishes: ['*'], points: ['*'], notes: ['*'], geometry: true, all: true }, t0: 0, by: 'load', remote: true, replay: false, gesture: null }); },
    get design() { return design; }, get derived() { return dv; },
    item, roomAt, note,
    point: (id) => dv.pointBy[id] || null,
    isAdded: (id) => !!addedPart(id), isRemoved: (id) => design.geometry.removed.includes(id),
    slides: (id) => (addedPart(id) || design.geometry.removed.includes(id) ? false : id in slideCache ? slideCache[id] : (slideCache[id] = canSlide(apt, id))),
    on: (f) => { subs.add(f); return () => subs.delete(f); },
    undo: () => step(undo, redo, 'inv'), redo: () => step(redo, undo, 'redo'),
    canUndo: () => undo.length > 0, canRedo: () => redo.length > 0,
    wallOf: (roomId) => design.finishes['wall:' + roomId] || null,
    floorOf: (roomId) => design.finishes['floor:' + roomId] || (dv.faceBy[roomId] && dv.faceBy[roomId].room && dv.faceBy[roomId].room.floor) || null,
  };
  return api;
}

/** The bill of quantities is a pure function of the same model: no second source of truth. */
export function quantities(store) {
  const dv = store.derived, d = store.design, H = (store.apt.levels && store.apt.levels[0] && store.apt.levels[0].height) || 270;
  const rooms = dv.faces.filter((f) => f.room).map((f) => {
    const fin = store.floorOf(f.id);
    return { id: f.id, type: f.room.type, name: f.room.name_he, net: f.net, w: f.clearW, d: f.clearD, finish: fin, base: f.room.floor, changed: fin !== f.room.floor, fresh: !!f.room.fresh, merged: f.merged };
  });
  const floors = {};
  for (const r of rooms) floors[r.finish] = r1((floors[r.finish] || 0) + r.net);
  const items = {};
  for (const it of d.items) items[it.sku] = (items[it.sku] || 0) + 1;
  const points = {};
  for (const k in POINT_KINDS) points[k] = { base: 0, moved: 0, added: 0, removed: 0 };
  for (const p of dv.points) points[p.kind][p.state] += 1;
  const part = (list) => { const m = list.reduce((s, w) => s + w.L, 0) / 100; return { ids: list.map((w) => w.id), m: r2(m), sqm: r1((m * H) / 100) }; };
  const inside = rooms.filter((r) => r.type !== 'balcony');
  return {
    rooms, floors, items, points,
    partitions: { added: part(dv.walls.filter((w) => w.added)), removed: part(dv.ghosts) },
    net: r1(inside.reduce((s, r) => s + r.net, 0)),
    balcony: r1(rooms.filter((r) => r.type === 'balcony').reduce((s, r) => s + r.net, 0)),
    moved: Object.keys(d.geometry.walls).length,
  };
}
