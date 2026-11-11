// "My plan" (התוכנית שלי): turns a traced draft into a nadlan-apartment v1 document. Pure functions, no DOM.
// The same file runs in the browser (planmaker.js) and in node tests (docs/design-lab/apartment-designer/test-planbuild.mjs).
//
// A draft is what a person traces over their own plan, in the units of that plan's picture (pixels) or straight in cm:
//   { schema:'nadlan-myplan-draft', v:1, mode:'image'|'measure', cmPerPx, axis (radians, optional),
//     nodes:{id:[x,y]}, segs:[{id,a,b,kind}]   or   segments:[{a:[x,y],b:[x,y],kind}],
//     openings:[{id,p:[x,y],w (cm),type:'door'|'entry'|'window'|'slider'|'open'}], rooms:[{at:[x,y],key}] }
// buildPlan(draft, meta) returns the apartment: snapped ends, walls split at T junctions and crossings, overlapping walls
// joined, the sheet turned so the plan's own axis is horizontal, origin at the top-left, whole centimetres.
import { derive, emptyDesign, interior } from './core.js';
import { STRINGS } from './strings.js';

export const WALL_T = { facade: 25, partition: 10, rail: 8, divider: 0, mamad: 30, structural: 25 };
export const DRAW_KINDS = ['facade', 'partition', 'rail', 'divider'];
const RANK = { mamad: 6, facade: 5, structural: 4, partition: 3, rail: 2, divider: 1 };
// the opening kinds a person picks, mapped to the kinds the engine draws. A doorway with no door is NOT an engine opening
// (the plan and the 3D view would draw glass in it): it is a piece of the wall turned into a divider, the engine's own
// "open line between two spaces", so the wall really stops there and the rooms stay apart.
export const OPEN_TYPES = {
  door: { type: 'door', w: 80, sill: 0, head: 210 },
  entry: { type: 'door', w: 100, sill: 0, head: 210 },
  window: { type: 'window', w: 120, sill: 95, head: 215 },
  slider: { type: 'slider', w: 240, sill: 0, head: 230 },
  open: { type: 'gap', w: 90 },
};
export const NOTE_HE = 'שרטוט שלכם לפי התוכנית שהעליתם. המידות תלויות בקנה המידה שסימנתם. לפני שינוי קיר מתייעצים עם מהנדס.';
const FLOOR = { wet: 'porcelain-60', balcony: 'deck' };

const sub = (a, b) => [a[0] - b[0], a[1] - b[1]];
const dot = (a, b) => a[0] * b[0] + a[1] * b[1];
const crs = (a, b) => a[0] * b[1] - a[1] * b[0];
const hyp = (a) => Math.hypot(a[0], a[1]);
const r1 = (v) => Math.round(v * 10) / 10;
const num = (v) => typeof v === 'number' && Number.isFinite(v);
const pt2 = (p) => Array.isArray(p) && p.length === 2 && num(p[0]) && num(p[1]);

export function pip(p, poly) {
  let inside = false;
  for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
    const a = poly[i], b = poly[j];
    if ((a[1] > p[1]) !== (b[1] > p[1]) && p[0] < ((b[0] - a[0]) * (p[1] - a[1])) / (b[1] - a[1]) + a[0]) inside = !inside;
  }
  return inside;
}
export const polyArea = (poly) => { let A = 0; for (let i = 0; i < poly.length; i++) { const p = poly[i], q = poly[(i + 1) % poly.length]; A += p[0] * q[1] - q[0] * p[1]; } return A / 2; };
/** distance from p to segment a-b, with the place along it (t in 0..1) */
export function segDist(p, a, b) {
  const v = sub(b, a), L2 = dot(v, v) || 1e-12, t = dot(sub(p, a), v) / L2, c = Math.max(0, Math.min(1, t));
  return { t, c, d: Math.hypot(p[0] - a[0] - v[0] * c, p[1] - a[1] - v[1] * c), q: [a[0] + v[0] * c, a[1] + v[1] * c] };
}

/** the room names a person can pick: the list in strings (pm.rooms), then any engine space name not in it */
export function roomChoices(lang) {
  const he = STRINGS.he.pm.rooms, loc = (STRINGS[lang] && STRINGS[lang].pm && STRINGS[lang].pm.rooms) || he;
  const out = he.map(([key, name_he, type], i) => ({ key, name_he, type, label: (loc.find((r) => r[0] === key) || loc[i] || [])[1] || name_he }));
  STRINGS.he.spaceNames.forEach(([name_he, type], i) => {
    if (out.some((c) => c.name_he === name_he)) return;
    const l = (STRINGS[lang] && STRINGS[lang].spaceNames && STRINGS[lang].spaceNames[i]) || STRINGS.he.spaceNames[i];
    out.push({ key: 'sn' + i, name_he, type, label: l[0] });
  });
  return out;
}
const choiceBy = (key) => roomChoices('he').find((c) => c.key === key) || null;

/** a draft in either form becomes one list of points and one list of segments (indices into the points) */
function readDraft(d) {
  const pts = [], segs = [];
  if (d && d.nodes && Array.isArray(d.segs)) {
    const idx = {};
    for (const k in d.nodes) if (pt2(d.nodes[k])) { idx[k] = pts.length; pts.push([d.nodes[k][0], d.nodes[k][1]]); }
    for (const s of d.segs) if (s && s.a in idx && s.b in idx && s.a !== s.b) segs.push({ a: idx[s.a], b: idx[s.b], kind: WALL_T[s.kind] != null ? s.kind : 'partition' });
  } else if (d && Array.isArray(d.segments)) {
    for (const s of d.segments) {
      if (!s || !pt2(s.a) || !pt2(s.b)) continue;
      pts.push([s.a[0], s.a[1]], [s.b[0], s.b[1]]);
      segs.push({ a: pts.length - 2, b: pts.length - 1, kind: WALL_T[s.kind] != null ? s.kind : 'partition' });
    }
  }
  return { pts, segs };
}

/** The graph clean-up both the tool and the builder use. tol: ends closer than this are one corner, and an end this close
 *  to a wall lands on it (a T junction). Then every wall is split where another ends on it or crosses it, and two walls
 *  on the same stretch become one (the stronger kind wins). Returns fresh { pts, segs }. */
export function cleanGraph(pts0, segs0, tol, eps) {
  eps = eps || Math.max(1e-6, tol * 1e-3);
  let pts = pts0.map((p) => [p[0], p[1]]), segs = segs0.map((s) => ({ ...s }));
  const merge = (t) => { // greedy clusters: every point joins the first cluster centre within t
    const cent = [], map = [];
    pts.forEach((p, i) => {
      let k = cent.findIndex((c) => Math.hypot(c.x - p[0], c.y - p[1]) <= t);
      if (k < 0) { k = cent.length; cent.push({ x: p[0], y: p[1], n: 1, sx: p[0], sy: p[1] }); }
      else { const c = cent[k]; c.n++; c.sx += p[0]; c.sy += p[1]; }
      map[i] = k;
    });
    // a corner where three walls meet keeps the place of the first point (the one the person set first); others average
    pts = cent.map((c) => [c.x, c.y]);
    segs = segs.map((s) => ({ ...s, a: map[s.a], b: map[s.b] })).filter((s) => s.a !== s.b);
  };
  const used = () => { const u = new Set(); for (const s of segs) { u.add(s.a); u.add(s.b); } return u; };
  merge(tol);
  // T junctions: an end near the inside of another wall moves onto it
  for (const i of used()) {
    let best = null;
    for (const s of segs) {
      if (s.a === i || s.b === i) continue;
      const r = segDist(pts[i], pts[s.a], pts[s.b]), L = hyp(sub(pts[s.b], pts[s.a]));
      if (r.t * L <= tol || (1 - r.t) * L <= tol) continue; // near an end: that is a corner, not a T
      if (r.d <= tol && (!best || r.d < best.d)) best = { d: r.d, q: r.q };
    }
    if (best) pts[i] = best.q;
  }
  merge(Math.min(tol, eps * 10));
  // crossings: two walls that pass through each other meet at a new corner
  const n0 = segs.length;
  for (let i = 0; i < n0; i++) for (let j = i + 1; j < n0; j++) {
    const A = segs[i], B = segs[j];
    if (A.a === B.a || A.a === B.b || A.b === B.a || A.b === B.b) continue;
    const p0 = pts[A.a], r = sub(pts[A.b], p0), q0 = pts[B.a], s = sub(pts[B.b], q0), den = crs(r, s);
    if (Math.abs(den) < 1e-12) continue;
    const q = sub(q0, p0), t = crs(q, s) / den, u = crs(q, r) / den;
    const la = hyp(r), lb = hyp(s);
    if (t * la > eps && (1 - t) * la > eps && u * lb > eps && (1 - u) * lb > eps) pts.push([p0[0] + r[0] * t, p0[1] + r[1] * t]);
  }
  merge(Math.min(tol, eps * 10));
  // split every wall at the corners that lie on it (a crossing point is not an end of any wall yet, so every point counts)
  const all = pts.map((_, i) => i), pieces = [];
  for (const s of segs) {
    const a = pts[s.a], b = pts[s.b], L = hyp(sub(b, a)), on = [];
    for (const k of all) {
      if (k === s.a || k === s.b) continue;
      const r = segDist(pts[k], a, b);
      if (r.d <= eps * 4 && r.t * L > eps && (1 - r.t) * L > eps) on.push({ k, t: r.t });
    }
    on.sort((x, y) => x.t - y.t);
    let prev = s.a;
    for (const o of on) { if (o.k !== prev) pieces.push({ ...s, a: prev, b: o.k }); prev = o.k; }
    if (prev !== s.b) pieces.push({ ...s, a: prev, b: s.b });
  }
  // the same stretch twice (two rooms drawn side by side): keep one, the stronger kind
  const by = new Map();
  for (const s of pieces) {
    if (hyp(sub(pts[s.b], pts[s.a])) <= eps) continue;
    const key = Math.min(s.a, s.b) + ':' + Math.max(s.a, s.b), o = by.get(key);
    if (!o || (RANK[s.kind] || 0) > (RANK[o.kind] || 0)) by.set(key, s);
  }
  segs = [...by.values()];
  // drop the points no wall uses, renumber
  const keep = [...used()].sort((x, y) => x - y), re = new Map(keep.map((k, i) => [k, i]));
  return { pts: keep.map((k) => pts[k]), segs: segs.map((s) => ({ ...s, a: re.get(s.a), b: re.get(s.b) })) };
}

/** The length a person measures with a tape: between the faces of the walls that meet each end, not centre to centre.
 *  For each wall: centre length minus half the thickness of the thickest wall square to it at each end (an end where
 *  nothing meets it square, or the wall just runs on, takes nothing off). nodes in draft units, k = cm per unit;
 *  returns { segId: { centre, inner, ta, tb } } in cm, where ta/tb are what was taken off at the a and b ends. */
export function innerLengths(nodes, segs, k = 1) {
  const out = {}, at = {};
  for (const s of segs) for (const n of [s.a, s.b]) (at[n] = at[n] || []).push(s);
  const dirOf = (s, from) => { const A = nodes[from], B = nodes[from === s.a ? s.b : s.a], L = hyp(sub(B, A)) || 1; return [(B[0] - A[0]) / L, (B[1] - A[1]) / L]; };
  for (const s of segs) {
    const A = nodes[s.a], B = nodes[s.b]; if (!A || !B) continue;
    const centre = hyp(sub(B, A)) * k, d = dirOf(s, s.a);
    const off = (n) => { let t = 0; for (const o of at[n] || []) { if (o === s) continue; if (Math.abs(crs(d, dirOf(o, n))) > 0.7) t = Math.max(t, WALL_T[o.kind] || 0); } return t / 2; };
    const ta = off(s.a), tb = off(s.b);
    out[s.id] = { centre, inner: Math.max(0, centre - ta - tb), ta, tb };
  }
  return out;
}

/** the plan's own axis: the angle (mod 90 degrees) the walls agree on, weighted by length; or the draft's axis */
export function planAxis(pts, segs, given) {
  if (num(given)) return wrap90(given);
  let sx = 0, sy = 0;
  for (const s of segs) { const v = sub(pts[s.b], pts[s.a]), L = hyp(v), a = Math.atan2(v[1], v[0]); sx += L * Math.cos(4 * a); sy += L * Math.sin(4 * a); }
  return sx || sy ? Math.atan2(sy, sx) / 4 : 0;
}
const wrap90 = (a) => { const q = Math.PI / 2; let r = a % q; if (r > q / 2) r -= q; if (r <= -q / 2) r += q; return r; };

/** walls within 4 degrees of the axis become exactly straight: their two ends share one x (or one y) */
function straighten(pts, segs) {
  const lim = Math.sin((4 * Math.PI) / 180), px = pts.map((_, i) => i), py = pts.map((_, i) => i);
  const find = (p, i) => (p[i] === i ? i : (p[i] = find(p, p[i])));
  for (const s of segs) {
    const v = sub(pts[s.b], pts[s.a]), L = hyp(v); if (!L) continue;
    if (Math.abs(v[1]) / L < lim) py[find(py, s.a)] = find(py, s.b);
    else if (Math.abs(v[0]) / L < lim) px[find(px, s.a)] = find(px, s.b);
  }
  for (const [par, c] of [[px, 0], [py, 1]]) { // the median, so one shaky corner does not pull a whole line
    const g = new Map();
    pts.forEach((p, i) => { const r = find(par, i); (g.get(r) || g.set(r, []).get(r)).push(i); });
    for (const m of g.values()) if (m.length > 1) { const v = m.map((i) => pts[i][c]).sort((a, b) => a - b), med = v[(v.length - 1) >> 1]; for (const i of m) pts[i][c] = med; }
  }
}

/** the connected pieces of the wall graph, as lists of segment indices */
function components(n, segs) {
  const par = Array.from({ length: n }, (_, i) => i), find = (i) => (par[i] === i ? i : (par[i] = find(par[i])));
  for (const s of segs) par[find(s.a)] = find(s.b);
  const g = new Map();
  segs.forEach((s, i) => { const r = find(s.a); (g.get(r) || g.set(r, []).get(r)).push(i); });
  return [...g.values()];
}

function hash(str, seed) {
  let h = seed >>> 0;
  for (let i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = Math.imul(h, 16777619) >>> 0; }
  return h.toString(36).padStart(7, '0');
}

/** faces of a wall graph through the engine itself, so the tool shows exactly the rooms and areas the designer will */
function facesOf(nodes, walls, openings) {
  const apt = { schema: 'nadlan-apartment', v: 1, id: 'tmp', geometry_revision: 'tmp', unit: { project: null, unit_id: null, rooms: 1 }, nodes, walls, openings: openings || [], rooms: [], rules: [] };
  return derive(apt, emptyDesign(apt)).faces;
}

/**
 * Everything the tool needs from a draft in one pass: the apartment (or null when nothing is closed yet), the spaces
 * found (outline in DRAFT units, net area, name), the problems, and the frame between the draft and the plan.
 */
export function analyzeDraft(draft, meta = {}) {
  const k = num(draft && draft.cmPerPx) && draft.cmPerPx > 0 ? draft.cmPerPx : 1;
  const raw = readDraft(draft);
  const problems = [];
  if (!raw.segs.length) return { plan: null, faces: [], problems: [{ code: 'no.walls' }], frame: null, free: [] };
  // 1. centimetres, turned so the plan's axis is horizontal
  const th = planAxis(raw.pts, raw.segs, draft.axis), c = Math.cos(-th), s = Math.sin(-th);
  const rot = (p) => [(p[0] * c - p[1] * s) * k, (p[0] * s + p[1] * c) * k];
  let g = cleanGraph(raw.pts.map(rot), raw.segs, num(meta.snapCm) ? meta.snapCm : 8);
  straighten(g.pts, g.segs);
  g.pts = g.pts.map((p) => [Math.round(p[0]), Math.round(p[1])]);
  g = cleanGraph(g.pts, g.segs, 0.6, 0.3);
  g.pts = g.pts.map((p) => [Math.round(p[0]), Math.round(p[1])]);
  g.segs = g.segs.filter((q) => hyp(sub(g.pts[q.b], g.pts[q.a])) >= 1);
  // 2. one connected drawing: the piece with the most enclosed area (else the longest) is the apartment
  const comps = components(g.pts.length, g.segs);
  if (comps.length > 1) {
    const score = comps.map((list) => {
      const nodes = {}, walls = [];
      for (const i of list) { const q = g.segs[i]; nodes['p' + q.a] = g.pts[q.a]; nodes['p' + q.b] = g.pts[q.b]; walls.push({ id: 'x' + i, a: 'p' + q.a, b: 'p' + q.b, t: 0, kind: 'divider' }); }
      let area = 0; try { area = facesOf(nodes, walls).reduce((m, f) => m + f.gross, 0); } catch (e) { /* a piece with no space */ }
      return area * 1e6 + list.reduce((m, i) => m + hyp(sub(g.pts[g.segs[i].b], g.pts[g.segs[i].a])), 0);
    });
    const best = score.indexOf(Math.max(...score));
    problems.push({ code: 'apart', n: comps.length - 1 });
    const keep = new Set(comps[best]); g.segs = g.segs.filter((_, i) => keep.has(i));
  }
  // 3. origin at the top-left
  const usedP = new Set(); for (const q of g.segs) { usedP.add(q.a); usedP.add(q.b); }
  const ox = Math.min(...[...usedP].map((i) => g.pts[i][0])), oy = Math.min(...[...usedP].map((i) => g.pts[i][1]));
  const toPlan = (p) => { const r = rot(p); return [r[0] - ox, r[1] - oy]; };
  const toDraft = (p) => { const x = (p[0] + ox) / k, y = (p[1] + oy) / k, c2 = Math.cos(th), s2 = Math.sin(th); return [x * c2 - y * s2, x * s2 + y * c2]; };
  const order = [...usedP].sort((a, b) => g.pts[a][1] - g.pts[b][1] || g.pts[a][0] - g.pts[b][0]);
  const nid = new Map(order.map((i, j) => [i, 'n' + (j + 1)]));
  const nodes = {}; for (const i of order) nodes[nid.get(i)] = [g.pts[i][0] - ox, g.pts[i][1] - oy];
  let walls = g.segs.map((q, j) => ({ id: 'w' + (j + 1), a: nid.get(q.a), b: nid.get(q.b), t: WALL_T[q.kind], kind: q.kind }));
  // free ends: a corner with one wall is a wall that was not closed
  const deg = {}; for (const w of walls) { deg[w.a] = (deg[w.a] || 0) + 1; deg[w.b] = (deg[w.b] || 0) + 1; }
  const free = Object.keys(deg).filter((n) => deg[n] === 1);
  if (free.length) problems.push({ code: 'open.end', n: free.length });
  // 4. openings: each one on the wall piece nearest to its middle, inside that piece
  const wl = (w) => { const a = nodes[w.a], b = nodes[w.b]; return { a, b, L: hyp(sub(b, a)) }; };
  const host = (p) => { let best = null; for (const w of walls) { if (w.kind === 'divider' || w.kind === 'rail') continue; const g2 = wl(w), r = segDist(p, g2.a, g2.b); if (!best || r.d < best.d) best = { w, d: r.d, s: r.c * g2.L, L: g2.L }; } return best; };
  const ops = (draft.openings || []).filter((o) => o && pt2(o.p) && OPEN_TYPES[o.type]).map((o) => ({ ...o, q: toPlan(o.p) }));
  let seq = walls.length;
  for (const o of ops.filter((x) => x.type === 'open')) { // a doorway with no door: that stretch of the wall becomes a divider
    const h = host(o.q);
    if (!h || h.d > Math.max(WALL_T[h.w.kind], 20)) { problems.push({ code: 'opening.off' }); continue; }
    let w = Math.round(num(o.w) ? o.w : OPEN_TYPES.open.w);
    if (w > h.L - 2) { problems.push({ code: 'opening.wide' }); w = Math.max(10, Math.round(h.L - 2)); }
    const at0 = Math.max(1, Math.min(h.L - 1 - w, Math.round(h.s - w / 2))), A = wl(h.w), dir = [(A.b[0] - A.a[0]) / A.L, (A.b[1] - A.a[1]) / A.L];
    const m1 = 'n' + (Object.keys(nodes).length + 1), m2 = 'n' + (Object.keys(nodes).length + 2);
    nodes[m1] = [Math.round(A.a[0] + dir[0] * at0), Math.round(A.a[1] + dir[1] * at0)];
    nodes[m2] = [Math.round(A.a[0] + dir[0] * (at0 + w)), Math.round(A.a[1] + dir[1] * (at0 + w))];
    const i = walls.indexOf(h.w), base = h.w;
    walls.splice(i, 1, { ...base, b: m1 }, { id: 'w' + ++seq, a: m1, b: m2, t: 0, kind: 'divider' }, { ...base, id: 'w' + ++seq, a: m2 });
  }
  const openings = [];
  let on = 0;
  for (const o of ops.filter((x) => x.type !== 'open')) {
    const h = host(o.q), spec = OPEN_TYPES[o.type];
    if (!h || h.d > Math.max(WALL_T[h.w.kind], 20)) { problems.push({ code: 'opening.off' }); continue; }
    let w = Math.round(num(o.w) && o.w > 0 ? o.w : spec.w);
    if (w > h.L - 10) { problems.push({ code: 'opening.wide' }); w = Math.round(h.L - 10); if (w < 30) continue; }
    const at = Math.max(5, Math.min(Math.round(h.L - 5 - w), Math.round(h.s - w / 2)));
    const clash = openings.find((x) => x.wall === h.w.id && at < x.at + x.w + 5 && x.at < at + w + 5);
    if (clash) { problems.push({ code: 'opening.overlap' }); continue; }
    const rec = { id: 'o' + ++on, wall: h.w.id, type: spec.type, at, w, sill: spec.sill, head: spec.head };
    if (spec.type === 'door') rec.swing = 1;
    openings.push(rec);
  }
  // 5. spaces, through the engine; names from the draft's name points
  let faces = facesOf(nodes, walls, openings);
  const names = (draft.rooms || []).filter((r) => r && pt2(r.at)).map((r) => ({ ...r, q: toPlan(r.at), choice: r.key === 'out' ? { key: 'out', type: null } : choiceBy(r.key) })).filter((r) => r.choice);
  const nameOf = (f) => { const hit = names.filter((r) => pip(r.q, f.poly)); return hit.length ? hit[hit.length - 1].choice : null; };
  // the safe room's walls are the safe room's: 30 cm, kind mamad (its open line, if any, stays an open line)
  const mm = new Set();
  for (const f of faces) { const ch = nameOf(f); if (ch && ch.type === 'mamad') for (const id of f.walls) mm.add(id); }
  if (mm.size) { walls = walls.map((w) => (mm.has(w.id) && w.kind !== 'divider' && w.kind !== 'rail' ? { ...w, kind: 'mamad', t: WALL_T.mamad } : w)); faces = facesOf(nodes, walls, openings); }
  // an inner wall with a space on one side only is on the outline of the apartment: it is an outer wall (it keeps its
  // thickness and place, so no size changes, but the designer will not let it move). Rails and open lines stay as they are.
  if (faces.length) walls = walls.map((w) => {
    if (w.kind !== 'partition') return w;
    const a = nodes[w.a], b = nodes[w.b], L = hyp(sub(b, a)); if (!L) return w;
    const m = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2], n = [-(b[1] - a[1]) / L, (b[0] - a[0]) / L], e = w.t / 2 + 2;
    const inside = (p) => faces.some((f) => pip(p, f.poly));
    return inside([m[0] + n[0] * e, m[1] + n[1] * e]) !== inside([m[0] - n[0] * e, m[1] - n[1] * e]) ? { ...w, kind: 'facade' } : w;
  });
  if (!faces.length) { problems.push({ code: 'no.room' }); return { plan: null, faces: [], problems, frame: { toDraft, toPlan, th, k }, free: free.map((n) => toDraft(nodes[n])) }; }
  const rooms = [], out = [], counter = {};
  let unnamed = 0;
  for (const f of faces) {
    const ch = nameOf(f), at = interior(f).map(r1), area = Math.abs(polyArea(f.poly)) / 1e4;
    const rec = { poly: f.poly.map(toDraft), net: f.net, gross: f.gross, at: toDraft(at), key: ch ? ch.key : null };
    out.push(rec);
    if (ch && ch.key === 'out') continue;
    if (!ch) unnamed++;
    const type = ch ? ch.type : 'other', name_he = ch ? ch.name_he : STRINGS.he.pm.unnamedRoom;
    counter[type] = (counter[type] || 0) + 1;
    const id = type + '-' + counter[type];
    rec.id = id; rec.type = type; rec.name_he = name_he; rec.area = area;
    rooms.push({ id, type, name_he, at, floor: FLOOR[type] || 'porcelain-80' });
  }
  if (unnamed) problems.push({ code: 'room.noname', n: unnamed });
  if (!rooms.length) { problems.push({ code: 'no.room' }); return { plan: null, faces: out, problems, frame: { toDraft, toPlan, th, k }, free: free.map((n) => toDraft(nodes[n])) }; }
  // 6. the document
  const geo = JSON.stringify({ nodes, walls, openings });
  const h = hash(geo, 2166136261) + hash(geo, 33554467);
  const count = (t) => rooms.filter((r) => r.type === t).length;
  const roomN = Math.max(1, Math.min(12, (count('living') ? 1 : 0) + count('bedroom') + count('mamad') + rooms.filter((r) => r.name_he === 'חדר עבודה').length));
  const date = meta.date || new Date().toISOString().slice(0, 10);
  const plan = {
    schema: 'nadlan-apartment', v: 1, id: 'own-' + h, geometry_revision: 'own:' + h,
    source: { kind: 'own', label_he: STRINGS.he.pm.sourceLabel, note: NOTE_HE, date },
    unit: { project: meta.project || null, unit_id: null, tower: null, floor: null, type: 'OWN', rooms: roomN },
    units: 'cm', frame: { origin: 'plan-top-left', x: 'right', y: 'down', rot: 'deg-cw' }, north_deg: 0,
    levels: [{ id: 'L0', height: 270, slab: 25 }],
    nodes, walls, openings, rooms, rules: [], starter: [],
  };
  return { plan, faces: out, problems, frame: { toDraft, toPlan, th, k }, free: free.map((n) => toDraft(nodes[n])) };
}

/** The apartment document from a draft. Throws when the walls close no room at all. */
export function buildPlan(draft, meta = {}) {
  const r = analyzeDraft(draft, meta);
  if (!r.plan) { const e = new Error('no closed room'); e.code = 'no.room'; throw e; }
  return r.plan;
}

/** What still needs the person's attention, as codes (the sentences are in strings.js, pm.problems) */
export function checkDraft(draft, meta = {}) {
  return analyzeDraft(draft, meta).problems;
}
