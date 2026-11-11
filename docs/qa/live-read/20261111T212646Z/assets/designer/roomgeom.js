// "Measure with the camera" geometry (roomscan.js draws, this file decides). Pure functions: no DOM, no three.js.
// The same file runs in the browser and in node tests (docs/design-lab/apartment-designer/test-roomgeom.mjs).
//
// The person marks corners on the floor INSIDE each room, so every room arrives as the outline of its inner wall faces.
// Between two neighbouring rooms there is a gap the thickness of the wall. Our plan format is wall CENTRE LINES with a
// thickness, so roomsToSegments():
//   1. squares: turns everything so the main axis is horizontal, and makes walls within 7 degrees of it exactly straight;
//   2. pairs: an edge with an opposite, parallel edge of another room 45 cm or closer, overlapping 30 cm or more, is a
//      shared wall: its centre line sits in the middle of the gap and its thickness IS the gap (8 to 40 cm);
//   3. an edge (or the part of one) with no such neighbour is an outside wall: centre line 12.5 cm out, 25 cm, facade
//      (on a balcony: a railing, 8 cm);
//   4. lines that are really one line are made one (measuring noise), every room's centre-line outline is built from them,
//      with a short step where a wall changes thickness, and all outlines are joined into one wall graph: shared corners
//      merged, T junctions split, the same stretch kept once, straight runs joined.
// Frame of the output: centimetres, origin at the top-left, x to the right, y down (the designer's own frame).

const sub = (a, b) => [a[0] - b[0], a[1] - b[1]];
const add = (a, b) => [a[0] + b[0], a[1] + b[1]];
const mul = (a, k) => [a[0] * k, a[1] * k];
const dot = (a, b) => a[0] * b[0] + a[1] * b[1];
const crs = (a, b) => a[0] * b[1] - a[1] * b[0];
const hyp = (a) => Math.hypot(a[0], a[1]);
const dist = (a, b) => Math.hypot(a[0] - b[0], a[1] - b[1]);
const mid = (a, b) => [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2];
const num = (v) => typeof v === 'number' && Number.isFinite(v);
const pt2 = (p) => Array.isArray(p) && p.length >= 2 && num(p[0]) && num(p[1]);
const r1 = (v) => Math.round(v * 10) / 10;
const RAD = Math.PI / 180, Q = Math.PI / 2;
const rot = (p, a) => { const c = Math.cos(a), s = Math.sin(a); return [p[0] * c - p[1] * s, p[0] * s + p[1] * c]; };

/** the names a closed room can take in one tap. key = the plan tool's room key (strings.js pm.rooms), so names carry over */
export const ROOM_CHOICES = [
  { key: 'living', type: 'living', name_he: 'סלון', he: 'סלון', en: 'Living room' },
  { key: 'kitchen', type: 'kitchen', name_he: 'מטבח', he: 'מטבח', en: 'Kitchen' },
  { key: 'bedroom', type: 'bedroom', name_he: 'חדר שינה', he: 'חדר שינה', en: 'Bedroom' },
  { key: 'mamad', type: 'mamad', name_he: 'ממ״ד', he: 'ממ״ד', en: 'Safe room' },
  { key: 'bath', type: 'wet', name_he: 'חדר רחצה', he: 'רחצה', en: 'Bathroom' },
  { key: 'balcony', type: 'balcony', name_he: 'מרפסת', he: 'מרפסת', en: 'Balcony' },
  { key: 'corridor', type: 'hall', name_he: 'מסדרון', he: 'מסדרון', en: 'Corridor' },
];

export const DEFAULTS = {
  snapDeg: 7, square: true, maxGap: 45, minGap: -10, minOverlap: 30, facadeT: 25, railT: 8, minT: 8, maxT: 40,
  absorb: 42, // an uncovered stretch this short between (or beside) shared parts is the end of a crossing wall, not an outside wall
  join: 2.5, // corners closer than this are one corner (cm)
};

// ---------- small polygon tools ----------
export function signedArea(P) {
  let A = 0;
  for (let i = 0; i < P.length; i++) { const p = P[i], q = P[(i + 1) % P.length]; A += p[0] * q[1] - q[0] * p[1]; }
  return A / 2;
}
/** the area of a polygon, in the square of its units (cm in, cm² out) */
export const polygonArea = (P) => Math.abs(signedArea(P || []));

/** WebXR world (metres, y up, x and z on the floor) to plan centimetres. Looking down from above x stays right and z is down. */
export function worldToPlan(p) {
  const x = Array.isArray(p) ? p[0] : p.x, z = Array.isArray(p) ? p[2] : p.z;
  return [x * 100, z * 100];
}

function dedupe(P, tol) {
  const out = [];
  for (const p of P) if (!out.length || dist(out[out.length - 1], p) > tol) out.push([p[0], p[1]]);
  while (out.length > 1 && dist(out[0], out[out.length - 1]) <= tol) out.pop();
  return out;
}
/** drops corners that lie on the straight line between their neighbours (deviation in cm) */
function dropCollinear(P, tol) {
  let p = P.slice();
  for (let changed = true; changed && p.length > 3;) {
    changed = false;
    for (let i = 0; i < p.length && p.length > 3; i++) {
      const a = p[(i + p.length - 1) % p.length], b = p[i], c = p[(i + 1) % p.length], L = dist(a, c);
      const dev = L > 1e-9 ? Math.abs(crs(sub(c, a), sub(b, a))) / L : dist(a, b);
      if (dev <= tol && dot(sub(b, a), sub(c, a)) > 0 && dot(sub(b, c), sub(a, c)) > 0) { p.splice(i, 1); changed = true; i--; }
    }
  }
  return p;
}
function properCross(a0, a1, b0, b1) {
  const r = sub(a1, a0), s = sub(b1, b0), den = crs(r, s);
  if (Math.abs(den) < 1e-12) return null;
  const q = sub(b0, a0), t = crs(q, s) / den, u = crs(q, r) / den;
  return t > 1e-6 && t < 1 - 1e-6 && u > 1e-6 && u < 1 - 1e-6 ? { t, u, p: add(a0, mul(r, t)) } : null;
}
function selfCrossing(P) {
  const n = P.length;
  for (let i = 0; i < n; i++) for (let j = i + 2; j < n; j++) {
    if (i === 0 && j === n - 1) continue;
    if (properCross(P[i], P[(i + 1) % n], P[j], P[(j + 1) % n])) return true;
  }
  return false;
}
/** a point surely inside the polygon, in its wide part (an approximate pole of inaccessibility, two grid passes) */
export function interiorPoint(P) {
  const pip = (p) => { let inside = false; for (let i = 0, j = P.length - 1; i < P.length; j = i++) { const a = P[i], b = P[j]; if ((a[1] > p[1]) !== (b[1] > p[1]) && p[0] < ((b[0] - a[0]) * (p[1] - a[1])) / (b[1] - a[1]) + a[0]) inside = !inside; } return inside; };
  const edge = (q) => { let d = Infinity; for (let i = 0, j = P.length - 1; i < P.length; j = i++) d = Math.min(d, segDist(q, P[j], P[i]).d); return d; };
  const xs = P.map((p) => p[0]), ys = P.map((p) => p[1]);
  let w = Math.max(...xs) - Math.min(...xs), h = Math.max(...ys) - Math.min(...ys), c = [Math.min(...xs) + w / 2, Math.min(...ys) + h / 2], best = null;
  for (const n of [14, 8]) {
    const sx = w / n, sy = h / n;
    for (let i = 0; i <= n; i++) for (let j = 0; j <= n; j++) {
      const q = [c[0] - w / 2 + sx * i, c[1] - h / 2 + sy * j];
      if (!pip(q)) continue;
      const d = edge(q); if (!best || d > best.d + 0.5) best = { q, d };
    }
    if (!best) break;
    c = best.q; w = sx * 2; h = sy * 2;
  }
  return best ? best.q : [xs.reduce((s, v) => s + v, 0) / xs.length, ys.reduce((s, v) => s + v, 0) / ys.length];
}
export function segDist(p, a, b) {
  const v = sub(b, a), L2 = dot(v, v) || 1e-12, t = dot(sub(p, a), v) / L2, c = Math.max(0, Math.min(1, t));
  const q = add(a, mul(v, c));
  return { t, c, d: dist(p, q), q };
}

/**
 * A room the person just closed: the last corner on top of the first one is dropped, repeats and corners on a straight
 * line are dropped. Returns { ok, points, area (cm²), why: 'few' | 'small' | 'cross' }.
 */
export function closeRoom(points, opts = {}) {
  const reach = num(opts.reach) ? opts.reach : 15;
  let P = dedupe((points || []).filter(pt2), 2);
  if (P.length > 3 && dist(P[0], P[P.length - 1]) <= reach) P.pop();
  P = dropCollinear(P, num(opts.straight) ? opts.straight : 3);
  if (P.length < 3) return { ok: false, why: 'few', points: P, area: 0 };
  const area = polygonArea(P);
  if (selfCrossing(P)) return { ok: false, why: 'cross', points: P, area };
  if (area < (num(opts.minArea) ? opts.minArea : 3000)) return { ok: false, why: 'small', points: P, area };
  return { ok: true, points: P, area };
}

/**
 * While measuring: where a new corner really goes. prev = the last corner, candidate = where the phone points,
 * axis = the angle (radians) of the first wall. Order: an existing corner within reach wins (closing a room, a corner
 * shared with a room measured before); then, when the wall from prev is within opts.deg (7) of the axis or square to it,
 * it is made exactly straight, keeping its length; with opts.next (the room's first corner) the closing wall is squared too.
 * opts: { deg, reach, corners:[[x,y]...], next:[x,y], square:true }. Returns { p, snap: 'corner'|'axis'|'square'|null }.
 */
export function snapCorner(prev, candidate, axis, opts = {}) {
  const deg = (num(opts.deg) ? opts.deg : 7) * RAD, reach = num(opts.reach) ? opts.reach : 12;
  let best = null;
  for (const c of opts.corners || []) { const d = dist(c, candidate); if (pt2(c) && d <= reach && (!best || d < best.d)) best = { c, d }; }
  if (best) return { p: [best.c[0], best.c[1]], snap: 'corner' };
  const out = { p: [candidate[0], candidate[1]], snap: null };
  if (!prev || opts.square === false || !num(axis)) return out;
  const dirNear = (v) => {
    const L = hyp(v); if (L < 1e-9) return null;
    const a = Math.atan2(v[1], v[0]), k = Math.round((a - axis) / Q), t = axis + k * Q;
    return Math.abs(a - t) <= deg ? [Math.cos(t), Math.sin(t)] : null;
  };
  const v = sub(candidate, prev), d1 = dirNear(v);
  if (!d1) return out;
  const p = add(prev, mul(d1, dot(v, d1)));
  if (pt2(opts.next)) {
    const d2 = dirNear(sub(opts.next, p));
    if (d2 && Math.abs(dot(d1, d2)) < 1e-6) { // the closing wall square too: the corner where both straight walls meet
      const x = lineX({ p: prev, d: d1 }, { p: opts.next, d: d2 }, 0.5);
      if (x && dist(x, candidate) <= Math.max(reach * 2, 25)) return { p: x, snap: 'square' };
    }
  }
  return { p, snap: 'axis' };
}

// ---------- lines ----------
/** where two lines {p, d} meet; null when they are closer than `minSin` to parallel */
function lineX(L1, L2, minSin) {
  const den = crs(L1.d, L2.d);
  if (Math.abs(den) < (minSin || 1e-9)) return null;
  const t = crs(sub(L2.p, L1.p), L2.d) / den;
  return add(L1.p, mul(L1.d, t));
}
const proj = (p, L) => add(L.p, mul(L.d, dot(sub(p, L.p), L.d)));

/** the angle (mod 90 degrees) the walls agree on, weighted by length, in (-45, 45] degrees */
export function dominantAxis(polys) {
  let sx = 0, sy = 0;
  for (const P of polys) for (let i = 0; i < P.length; i++) {
    const v = sub(P[(i + 1) % P.length], P[i]), L = hyp(v), a = Math.atan2(v[1], v[0]);
    sx += L * Math.cos(4 * a); sy += L * Math.sin(4 * a);
  }
  return sx || sy ? Math.atan2(sy, sx) / 4 : 0;
}

/** each edge becomes a line through its middle (exactly horizontal or vertical when within the snap angle); corners where they meet */
function squarePoly(P, o) {
  const n = P.length, lim = o.square ? o.snapDeg * RAD : -1, lines = [];
  for (let i = 0; i < n; i++) {
    const a = P[i], b = P[(i + 1) % n], v = sub(b, a), L = hyp(v);
    let d = [v[0] / L, v[1] / L];
    const ang = Math.atan2(d[1], d[0]), k = Math.round(ang / Q);
    if (Math.abs(ang - k * Q) <= lim) d = [Math.round(Math.cos(k * Q)), Math.round(Math.sin(k * Q))];
    lines.push({ p: mid(a, b), d });
  }
  const out = [];
  for (let i = 0; i < n; i++) {
    const L1 = lines[(i + n - 1) % n], L2 = lines[i], v = P[i];
    const x = lineX(L1, L2, Math.sin(15 * RAD));
    if (x && dist(x, v) < 80) { out.push(x); continue; }
    const q1 = proj(v, L1), q2 = proj(v, L2);
    out.push(q1); if (dist(q1, q2) > 0.5) out.push(q2);
  }
  return dropCollinear(dedupe(out, 0.5), 0.5);
}

const RANK = { facade: 3, partition: 2, rail: 1, divider: 0 };

/** the wall graph clean-up: corners within tol merged, an end on a wall's inside becomes a T, crossings split, the same stretch kept once */
function cleanSegs(raw, tol) {
  let pts = [], segs = [];
  const nodeAt = (p, t) => {
    let k = -1, bd = t;
    for (let i = 0; i < pts.length; i++) { const d = dist(pts[i].p, p); if (d <= bd) { bd = d; k = i; } }
    if (k >= 0) { const c = pts[k]; c.n++; c.s = add(c.s, p); c.p = mul(c.s, 1 / c.n); return k; }
    pts.push({ p: [p[0], p[1]], s: [p[0], p[1]], n: 1 }); return pts.length - 1;
  };
  for (const s of raw) { const a = nodeAt(s.a, tol), b = nodeAt(s.b, tol); if (a !== b) segs.push({ ...s, a, b }); }
  let P = pts.map((x) => x.p);
  const L = (s) => dist(P[s.a], P[s.b]);
  // T junctions: an end near the inside of another wall moves onto it
  for (let i = 0; i < P.length; i++) {
    let best = null;
    for (const s of segs) {
      if (s.a === i || s.b === i) continue;
      const r = segDist(P[i], P[s.a], P[s.b]), l = L(s);
      if (r.t * l <= tol || (1 - r.t) * l <= tol) continue;
      if (r.d <= tol && (!best || r.d < best.d)) best = r;
    }
    if (best) P[i] = best.q;
  }
  // crossings become corners
  const n0 = segs.length;
  for (let i = 0; i < n0; i++) for (let j = i + 1; j < n0; j++) {
    const A = segs[i], B = segs[j];
    if (A.a === B.a || A.a === B.b || A.b === B.a || A.b === B.b) continue;
    const x = properCross(P[A.a], P[A.b], P[B.a], P[B.b]);
    if (x && x.t * L(A) > 0.5 && (1 - x.t) * L(A) > 0.5 && x.u * L(B) > 0.5 && (1 - x.u) * L(B) > 0.5) P.push(x.p);
  }
  // merge what the moves brought together, then split every wall at the corners on it
  pts = []; const map = P.map((p) => nodeAt(p, 0.5)); P = pts.map((x) => x.p);
  segs = segs.map((s) => ({ ...s, a: map[s.a], b: map[s.b] })).filter((s) => s.a !== s.b);
  const pieces = [];
  for (const s of segs) {
    const a = P[s.a], b = P[s.b], l = dist(a, b), on = [];
    P.forEach((q, k) => { if (k === s.a || k === s.b) return; const r = segDist(q, a, b); if (r.d <= 0.6 && r.t * l > 0.5 && (1 - r.t) * l > 0.5) on.push({ k, t: r.t }); });
    on.sort((x, y) => x.t - y.t);
    let prev = s.a;
    for (const o of on) { if (o.k !== prev) pieces.push({ ...s, a: prev, b: o.k }); prev = o.k; }
    if (prev !== s.b) pieces.push({ ...s, a: prev, b: s.b });
  }
  const by = new Map();
  for (const s of pieces) {
    if (dist(P[s.a], P[s.b]) < 0.5) continue;
    const key = Math.min(s.a, s.b) + ':' + Math.max(s.a, s.b), o = by.get(key);
    if (!o || RANK[s.kind] > RANK[o.kind] || (RANK[s.kind] === RANK[o.kind] && s.t > o.t)) by.set(key, s);
  }
  segs = [...by.values()];
  // straight runs of one kind and thickness through a corner with two walls become one wall
  for (let changed = true; changed;) {
    changed = false;
    const deg = new Map();
    for (const s of segs) for (const k of [s.a, s.b]) (deg.get(k) || deg.set(k, []).get(k)).push(s);
    for (const [k, list] of deg) {
      if (list.length !== 2) continue;
      const [s1, s2] = list;
      if (s1.kind !== s2.kind || s1.t !== s2.t) continue;
      const o1 = s1.a === k ? s1.b : s1.a, o2 = s2.a === k ? s2.b : s2.a;
      if (o1 === o2) continue;
      const v1 = sub(P[o1], P[k]), v2 = sub(P[o2], P[k]);
      if (Math.abs(crs(v1, v2)) / (hyp(v1) * hyp(v2)) > 0.002 || dot(v1, v2) > 0) continue;
      segs = segs.filter((s) => s !== s1 && s !== s2);
      segs.push({ ...s1, a: o1, b: o2 });
      changed = true; break;
    }
  }
  segs = segs.filter((s) => dist(P[s.a], P[s.b]) >= 1);
  // the averaging above can leave a straight wall a millimetre off: walls within half a degree of straight share one x (or y)
  for (const c of [0, 1]) {
    const up = P.map((_, i) => i), f = (i) => (up[i] === i ? i : (up[i] = f(up[i])));
    for (const s of segs) { const v = sub(P[s.b], P[s.a]); if (Math.abs(v[c]) < 1.5 && Math.abs(v[c]) / hyp(v) < 0.009) up[f(s.a)] = f(s.b); }
    const g = new Map();
    P.forEach((p, i) => { const r = f(i); (g.get(r) || g.set(r, []).get(r)).push(i); });
    for (const m of g.values()) if (m.length > 1) { const v = m.reduce((s, i) => s + P[i][c], 0) / m.length; for (const i of m) P[i] = c ? [P[i][0], v] : [v, P[i][1]]; }
  }
  return { P, segs };
}

/**
 * rooms: [{ points:[[x,y]...] (cm, any order, inner wall faces), name_he, type, key }]
 * opts: DEFAULTS plus { axis (radians, else found), openings:[{ a:[x,y], b:[x,y], type:'door'|'window' }] (same frame) }
 * Returns { segments:[{a,b,t,kind}], rooms:[{name_he,type,key,at,area,poly}], openings:[{a,b,type,w}], warnings:[],
 *           axis, draft } in plan cm (origin top-left, y down). draft = the plan tool's own draft (walls, openings, names).
 */
export function roomsToSegments(rooms, opts = {}) {
  const o = { ...DEFAULTS, ...opts }, warnings = [];
  const R = [];
  (rooms || []).forEach((r, i) => {
    const c = closeRoom((r && (r.points || r.poly)) || [], { reach: 15 });
    if (!c.ok) { warnings.push({ code: 'room.' + c.why, room: i, name_he: (r && r.name_he) || null }); return; }
    const P = signedArea(c.points) < 0 ? c.points.slice().reverse() : c.points;
    R.push({ src: i, name_he: r.name_he || null, type: r.type || null, key: r.key || null, P });
  });
  if (!R.length) return { segments: [], rooms: [], openings: [], warnings: warnings.concat({ code: 'no.room' }), axis: 0, draft: null };

  // 1. the main axis horizontal
  const axis = num(o.axis) ? o.axis : dominantAxis(R.map((r) => r.P));
  for (const r of R) r.P = r.P.map((p) => rot(p, -axis));
  const ops = (o.openings || []).filter((x) => x && pt2(x.a) && pt2(x.b)).map((x) => ({ type: x.type === 'window' ? 'window' : 'door', a: rot(x.a, -axis), b: rot(x.b, -axis) }));
  // 2. square every room
  for (const r of R) {
    let P = squarePoly(r.P, o);
    if (signedArea(P) < 0) P = P.reverse();
    if (P.length < 3 || selfCrossing(P)) { P = r.P; warnings.push({ code: 'room.shape', room: r.src, name_he: r.name_he }); }
    r.P = P;
  }
  // 3. edges, and for each one the opposite edges of other rooms
  const E = [];
  R.forEach((r, ri) => {
    r.edges = [];
    for (let i = 0; i < r.P.length; i++) {
      const a = r.P[i], b = r.P[(i + 1) % r.P.length], v = sub(b, a), L = hyp(v);
      if (L < 1e-6) continue;
      const d = [v[0] / L, v[1] / L], e = { ri, a, b, L, d, nout: [d[1], -d[0]], cand: [] };
      r.edges.push(e); E.push(e);
    }
  });
  const par = Math.sin(5 * RAD);
  for (const e of E) for (const f of E) {
    if (f.ri === e.ri || Math.abs(crs(e.d, f.d)) > par || dot(e.d, f.d) > -0.95) continue;
    const gap = dot(sub(mid(f.a, f.b), e.a), e.nout);
    if (gap < o.minGap || gap > o.maxGap) continue;
    const s1 = dot(sub(f.a, e.a), e.d), s2 = dot(sub(f.b, e.a), e.d);
    const lo = Math.max(0, Math.min(s1, s2)), hi = Math.min(e.L, Math.max(s1, s2));
    if (hi - lo >= o.minOverlap) e.cand.push({ lo, hi, gap, rj: f.ri });
  }
  // 4. each edge cut into stretches: shared (nearest neighbour first) and outside
  const isBal = (ri) => R[ri].type === 'balcony';
  for (const e of E) {
    let free = [[0, e.L]]; const parts = [];
    for (const c of e.cand.sort((x, y) => x.gap - y.gap)) {
      const nf = [];
      for (const [u, v] of free) {
        const lo = Math.max(u, c.lo), hi = Math.min(v, c.hi);
        if (hi - lo <= 0) { nf.push([u, v]); continue; }
        if (hi - lo >= 10) parts.push({ s0: lo, s1: hi, c }); else { nf.push([u, v]); continue; }
        if (lo > u) nf.push([u, lo]);
        if (v > hi) nf.push([hi, v]);
      }
      free = nf;
    }
    parts.sort((x, y) => x.s0 - y.s0);
    // the uncovered stretches: short ones are the ends of crossing walls and join the shared stretch next to them
    const all = [];
    let at = 0;
    for (const p of parts) { if (p.s0 > at + 1e-6) all.push({ s0: at, s1: p.s0, c: null }); all.push(p); at = p.s1; }
    if (at < e.L - 1e-6) all.push({ s0: at, s1: e.L, c: null });
    for (let i = 0; i < all.length; i++) {
      const p = all[i];
      if (p.c || p.s1 - p.s0 >= o.absorb) continue;
      const A = all[i - 1] && all[i - 1].c ? all[i - 1] : null, B = all[i + 1] && all[i + 1].c ? all[i + 1] : null;
      if (A && B) { const m = (p.s0 + p.s1) / 2; A.s1 = m; B.s0 = m; p.gone = true; }
      else if (A) { A.s1 = p.s1; p.gone = true; } else if (B) { B.s0 = p.s0; p.gone = true; }
    }
    e.parts = all.filter((p) => !p.gone).map((p) => {
      if (p.c) {
        const bal = isBal(e.ri) || isBal(p.c.rj);
        return { s0: p.s0, s1: p.s1, off: p.c.gap / 2, t: Math.max(o.minT, Math.min(o.maxT, Math.round(p.c.gap))), kind: bal ? 'facade' : 'partition', group: 'in', rj: p.c.rj };
      }
      return isBal(e.ri)
        ? { s0: p.s0, s1: p.s1, off: o.railT / 2, t: o.railT, kind: 'rail', group: 'out' }
        : { s0: p.s0, s1: p.s1, off: o.facadeT / 2, t: o.facadeT, kind: 'facade', group: 'out' };
    });
  }
  // 5. centre lines, and the lines that are one line made one
  const LN = [];
  for (const e of E) for (const p of e.parts) {
    const q0 = add(add(e.a, mul(e.d, p.s0)), mul(e.nout, p.off)), q1 = add(add(e.a, mul(e.d, p.s1)), mul(e.nout, p.off));
    let th = Math.atan2(e.d[1], e.d[0]); th = ((th % Math.PI) + Math.PI) % Math.PI; if (th > Math.PI - 1e-9) th = 0;
    const w = [-Math.sin(th), Math.cos(th)];
    p.line = LN.length;
    LN.push({ th, c: dot(w, q0), len: p.s1 - p.s0, group: p.group, kind: p.kind, t: p.t, q0, q1, up: LN.length });
  }
  const find = (i) => (LN[i].up === i ? i : (LN[i].up = find(LN[i].up)));
  for (let i = 0; i < LN.length; i++) for (let j = i + 1; j < LN.length; j++) {
    const A = LN[i], B = LN[j];
    let dth = Math.abs(A.th - B.th), cB = B.c;
    if (dth > Math.PI / 2) { dth = Math.PI - dth; cB = -cB; }
    if (dth > 1.5 * RAD) continue;
    const tol = A.group === 'out' && B.group === 'out' ? 7 : 3.5;
    if (Math.abs(A.c - cB) <= tol) LN[find(i)].up = find(j);
  }
  const CL = new Map();
  LN.forEach((l, i) => { const k = find(i); (CL.get(k) || CL.set(k, []).get(k)).push(l); });
  const clusters = [];
  for (const list of CL.values()) {
    const lead = list.reduce((m, l) => (l.len > m.len ? l : m), list[0]);
    let sw = 0, sc = 0;
    for (const l of list) { let c = l.c; if (Math.abs(l.th - lead.th) > Math.PI / 2) c = -c; sw += l.len; sc += l.len * c; }
    const c = sc / sw, d = [Math.cos(lead.th), Math.sin(lead.th)], w = [-d[1], d[0]];
    const heavy = list.reduce((m, l) => (l.len > m.len ? l : m), list[0]);
    const cl = { p: mul(w, c), d, th: lead.th, members: list, kind: heavy.kind, t: heavy.t };
    for (const l of list) l.cl = cl;
    clusters.push(cl);
  }
  // 6. every room's centre-line outline
  const raw = [];
  for (const r of R) {
    const seq = [];
    for (const e of r.edges) for (const p of e.parts) {
      const cl = LN[p.line].cl, last = seq[seq.length - 1], P0 = add(e.a, mul(e.d, p.s0));
      if (last && last.cl === cl && last.kind === p.kind && last.t === p.t) continue;
      seq.push({ cl, kind: p.kind, t: p.t, P0 });
    }
    while (seq.length > 1 && seq[0].cl === seq[seq.length - 1].cl && seq[0].kind === seq[seq.length - 1].kind && seq[0].t === seq[seq.length - 1].t) seq.shift();
    if (seq.length < 2) continue;
    const V = [];
    for (let k = 0; k < seq.length; k++) {
      const prev = seq[(k + seq.length - 1) % seq.length], cur = seq[k];
      if (prev.cl === cur.cl) { V.push({ p: proj(cur.P0, cur.cl), kind: cur.kind, t: cur.t }); continue; }
      const x = lineX(prev.cl, cur.cl, Math.sin(10 * RAD));
      if (x && dist(x, cur.P0) < 100) { V.push({ p: x, kind: cur.kind, t: cur.t }); continue; }
      // two parallel lines one after the other: the wall changes thickness. The step goes on the crossing wall nearby, if any.
      let J = null, bj = 30;
      for (const cl of clusters) {
        if (Math.abs(dot(cl.d, cur.cl.d)) > 0.02) continue;
        const dl = Math.abs(dot(sub(cur.P0, cl.p), [-cl.d[1], cl.d[0]]));
        if (dl > bj) continue;
        if (!cl.members.some((m) => segDist(cur.P0, m.q0, m.q1).d <= 40)) continue;
        J = cl; bj = dl;
      }
      const v1 = J ? lineX(prev.cl, J) : proj(cur.P0, prev.cl), v2 = J ? lineX(cur.cl, J) : proj(cur.P0, cur.cl);
      const jog = J ? { kind: J.kind, t: J.t } : RANK[prev.kind] >= RANK[cur.kind] ? { kind: prev.kind, t: Math.max(prev.t, cur.t) } : { kind: cur.kind, t: Math.max(prev.t, cur.t) };
      V.push({ p: v1, ...jog });
      if (dist(v1, v2) > 0.5) V.push({ p: v2, kind: cur.kind, t: cur.t });
    }
    for (let k = 0; k < V.length; k++) raw.push({ a: V[k].p, b: V[(k + 1) % V.length].p, kind: V[k].kind, t: V[k].t });
  }
  // 7. one wall graph
  const g = cleanSegs(raw.filter((s) => dist(s.a, s.b) > 0.5), o.join);
  if (!g.segs.length) return { segments: [], rooms: [], openings: [], warnings: warnings.concat({ code: 'no.room' }), axis, draft: null };
  const used = new Set(); for (const s of g.segs) { used.add(s.a); used.add(s.b); }
  const ox = Math.min(...[...used].map((i) => g.P[i][0])), oy = Math.min(...[...used].map((i) => g.P[i][1]));
  const T = (p) => [r1(p[0] - ox), r1(p[1] - oy)];
  const segments = g.segs.map((s) => ({ a: T(g.P[s.a]), b: T(g.P[s.b]), t: s.t, kind: s.kind }));
  // 8. rooms
  const roomsOut = R.map((r) => {
    const poly = r.P.map(T);
    return { name_he: r.name_he, type: r.type, key: r.key, at: interiorPoint(poly).map(r1), area: Math.round(polygonArea(poly) / 100) / 100, poly };
  });
  // 9. openings on the wall they were measured on
  const openings = [];
  for (const op of ops) {
    const a = T(op.a), b = T(op.b), m = mid(a, b);
    let best = null;
    for (const s of segments) { if (s.kind === 'rail' || s.kind === 'divider') continue; const r = segDist(m, s.a, s.b); if (!best || r.d < best.r.d) best = { s, r }; }
    if (!best || best.r.d > 45) { warnings.push({ code: 'opening.off', type: op.type }); continue; }
    const s = best.s, L = dist(s.a, s.b), d = mul(sub(s.b, s.a), 1 / L);
    let u = dot(sub(a, s.a), d), v = dot(sub(b, s.a), d);
    if (u > v) [u, v] = [v, u];
    u = Math.max(2, u); v = Math.min(L - 2, v);
    if (v - u < 30) { warnings.push({ code: 'opening.narrow', type: op.type }); continue; }
    openings.push({ a: add(s.a, mul(d, u)).map(r1), b: add(s.a, mul(d, v)).map(r1), type: op.type, w: Math.round(v - u) });
  }
  // 10. what the person should know
  if (R.length > 1) R.forEach((r, ri) => { if (!r.edges.some((e) => e.parts.some((p) => p.rj != null))) warnings.push({ code: 'room.alone', room: r.src, name_he: r.name_he }); });
  for (const e of E) for (const c of e.cand) if (c.gap < -3 && e.ri < c.rj) warnings.push({ code: 'room.overlap', room: R[e.ri].src, other: R[c.rj].src });
  return { segments, rooms: roomsOut, openings, warnings, axis, draft: toDraft(segments, openings, roomsOut) };
}

/** the plan tool's own draft (planmaker.js, mode 'measure', 1 cm per unit): walls, doors, windows and room names together */
export function toDraft(segments, openings, rooms) {
  const nodes = {}, keyOf = new Map(), segs = [];
  const node = (p) => { const k = p[0] + ',' + p[1]; if (!keyOf.has(k)) { const id = 'n' + keyOf.size; keyOf.set(k, id); nodes[id] = [p[0], p[1]]; } return keyOf.get(k); };
  const KIND = { facade: 'facade', partition: 'partition', rail: 'rail', divider: 'divider' };
  segments.forEach((s, i) => segs.push({ id: 's' + i, a: node(s.a), b: node(s.b), kind: KIND[s.kind] || 'partition' }));
  return {
    schema: 'nadlan-myplan-draft', v: 1, mode: 'measure', cmPerPx: 1, scale: null, img: null, axis: 0, nodes, segs,
    openings: (openings || []).map((op, i) => ({ id: 'o' + (i + 1), p: mid(op.a, op.b).map(r1), w: op.w, type: op.type === 'window' ? 'window' : 'door' })),
    rooms: (rooms || []).filter((r) => r.key).map((r) => ({ at: r.at, key: r.key })), opacity: 0.6, step: 'walls', source: 'camera',
  };
}
