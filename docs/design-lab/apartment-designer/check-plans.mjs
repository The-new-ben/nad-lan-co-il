// node check-plans.mjs [plan-id ...]
// Checks every plan listed in plugins/nadlan-config/assets/designer/plans/index.json with the designer's own core (derive)
// and catalogue. No dependencies. Exit code 1 if any plan fails.
//  - the nadlan-apartment v1 fields and enums (a hand-written validator of apartment.schema.json, plus the `starter` list)
//  - the wall graph: no zero-length wall, no two walls on the same corners, no wall crossing another without a corner,
//    no corner lying inside another wall (a T-junction must split the wall it meets), no dangling wall end
//  - rooms: every room point is in a closed space, no two room points share one space, no unnamed space bigger than 0.3 m²
//  - openings: inside their wall, not overlapping another opening on the same wall, never on a divider
//  - starter furniture: every piece stands inside the apartment, its centre in a room, and crosses no wall (dividers excepted)
//  - Ashira: each printed room size (plans-published.json) against the clear wall-to-wall size on our redraw, max 4%
//  - areas: the spaces tile the outline exactly, and the total net area equals the sum of the rooms
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const DES = path.resolve(here, '../../../plugins/nadlan-config/assets/designer');
const { derive, createStore, emptyDesign, quantities, POINT_KINDS } = await import(pathToFileURL(path.join(DES, 'core.js')).href);
const { ITEMS } = await import(pathToFileURL(path.join(DES, 'catalog.js')).href);
const PUB = JSON.parse(fs.readFileSync(path.join(here, 'plans-published.json'), 'utf8'));
const MAX_DEV = 0.04;

const sub = (a, b) => [a[0] - b[0], a[1] - b[1]];
const dot = (a, b) => a[0] * b[0] + a[1] * b[1];
const crs = (a, b) => a[0] * b[1] - a[1] * b[0];
const len = (a) => Math.hypot(a[0], a[1]);
const pip = (p, poly) => { let c = false; for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) { const a = poly[i], b = poly[j]; if ((a[1] > p[1]) !== (b[1] > p[1]) && p[0] < ((b[0] - a[0]) * (p[1] - a[1])) / (b[1] - a[1]) + a[0]) c = !c; } return c; };
const area = (poly) => { let A = 0; for (let i = 0; i < poly.length; i++) { const p = poly[i], q = poly[(i + 1) % poly.length]; A += p[0] * q[1] - q[0] * p[1]; } return A / 2; };
const isNum = (v) => typeof v === 'number' && Number.isFinite(v);
const pad = (s, n) => { s = String(s); return s.length >= n ? s : s + ' '.repeat(n - s.length); };
const lpad = (s, n) => { s = String(s); return s.length >= n ? s : ' '.repeat(n - s.length) + s; };

// ---- 1. the schema, by hand (docs/architecture/apartment-designer/apartment.schema.json)
// Two things core.js already reads that apartment.schema.json (11.11 00:19) does not list yet: the services layer `points`
// (ARCHITECTURE 10b) and the rule code mamad.no_chasing. They are checked here and reported as a NOTE, not silently passed.
const AHEAD = { fields: ['points'], rules: ['mamad.no_chasing'] };
function validate(apt, E, notes = []) {
  const req = ['schema', 'v', 'id', 'geometry_revision', 'source', 'unit', 'units', 'levels', 'nodes', 'walls', 'openings', 'rooms'];
  const allowed = new Set([...req, 'frame', 'north_deg', 'fixed', 'rules', 'view', 'starter', ...AHEAD.fields]);
  for (const k of AHEAD.fields) if (k in apt) notes.push('uses `' + k + '`, which core.js reads but apartment.schema.json does not list yet');
  for (const k of req) if (!(k in apt)) E.push('schema: missing ' + k);
  for (const k in apt) if (!allowed.has(k)) E.push('schema: unknown field ' + k);
  if (apt.schema !== 'nadlan-apartment') E.push('schema: schema must be nadlan-apartment');
  if (apt.v !== 1) E.push('schema: v must be 1');
  if (!/^[a-z0-9][a-z0-9._-]{1,63}$/.test(apt.id || '')) E.push('schema: bad id');
  if (!/^[A-Za-z0-9._:-]{1,80}$/.test(apt.geometry_revision || '')) E.push('schema: bad geometry_revision');
  const s = apt.source || {};
  for (const k in s) if (!['kind', 'label_he', 'note', 'ref', 'date'].includes(k)) E.push('schema: source.' + k + ' unknown');
  if (!['sales-plan', 'derived', 'schematic', 'example'].includes(s.kind)) E.push('schema: source.kind');
  if (typeof s.label_he !== 'string' || s.label_he.length > 80) E.push('schema: source.label_he');
  if (s.note != null && (typeof s.note !== 'string' || s.note.length > 400)) E.push('schema: source.note longer than 400');
  if (s.date != null && !/^\d{4}-\d{2}-\d{2}$/.test(s.date)) E.push('schema: source.date');
  const u = apt.unit || {};
  for (const k of ['project', 'unit_id', 'type', 'rooms']) if (!(k in u)) E.push('schema: unit.' + k + ' missing');
  for (const k in u) if (!['project', 'unit_id', 'tower', 'floor', 'type', 'rooms'].includes(k)) E.push('schema: unit.' + k + ' unknown');
  if (u.project !== null && typeof u.project !== 'string') E.push('schema: unit.project');
  if (u.unit_id !== null && !/^[A-Za-z0-9_-]{1,96}$/.test(u.unit_id || '')) E.push('schema: unit.unit_id');
  if (u.floor != null && !Number.isInteger(u.floor)) E.push('schema: unit.floor');
  if (typeof u.type !== 'string' || u.type.length > 40) E.push('schema: unit.type');
  if (!isNum(u.rooms) || u.rooms < 1 || u.rooms > 12) E.push('schema: unit.rooms');
  if (apt.units !== 'cm') E.push('schema: units must be cm');
  if (apt.frame) { const f = apt.frame; if (f.origin !== 'plan-top-left' || f.x !== 'right' || f.y !== 'down' || f.rot !== 'deg-cw') E.push('schema: frame'); }
  if (apt.north_deg != null && !(isNum(apt.north_deg) && apt.north_deg >= 0 && apt.north_deg < 360)) E.push('schema: north_deg');
  if (!Array.isArray(apt.levels) || !apt.levels.length) E.push('schema: levels');
  else for (const l of apt.levels) if (typeof l.id !== 'string' || !isNum(l.height) || l.height < 200 || l.height > 700) E.push('schema: level ' + l.id);
  const nodes = apt.nodes || {};
  if (Object.keys(nodes).length < 3) E.push('schema: fewer than 3 nodes');
  for (const k in nodes) if (!Array.isArray(nodes[k]) || nodes[k].length !== 2 || !nodes[k].every(isNum)) E.push('schema: node ' + k);
  const KINDS = ['facade', 'structural', 'mamad', 'shaft', 'partition', 'divider', 'rail'];
  const wid = new Set();
  if (!Array.isArray(apt.walls) || apt.walls.length < 3) E.push('schema: walls');
  for (const w of apt.walls || []) {
    for (const k in w) if (!['id', 'a', 'b', 't', 'kind', 'h'].includes(k)) E.push('schema: wall ' + w.id + ' field ' + k);
    if (typeof w.id !== 'string' || wid.has(w.id)) E.push('schema: wall id ' + w.id + ' missing or repeated'); wid.add(w.id);
    if (!(w.a in nodes) || !(w.b in nodes)) E.push('schema: wall ' + w.id + ' names an unknown node');
    if (!isNum(w.t) || w.t < 0 || w.t > 80) E.push('schema: wall ' + w.id + ' thickness');
    if (!KINDS.includes(w.kind)) E.push('schema: wall ' + w.id + ' kind ' + w.kind);
    if (w.h != null && !isNum(w.h)) E.push('schema: wall ' + w.id + ' h');
  }
  const oid = new Set();
  for (const o of apt.openings || []) {
    for (const k in o) if (!['id', 'wall', 'type', 'at', 'w', 'sill', 'head', 'swing'].includes(k)) E.push('schema: opening ' + o.id + ' field ' + k);
    if (typeof o.id !== 'string' || oid.has(o.id)) E.push('schema: opening id ' + o.id); oid.add(o.id);
    if (!wid.has(o.wall)) E.push('schema: opening ' + o.id + ' on unknown wall');
    if (!['door', 'window', 'slider', 'open'].includes(o.type)) E.push('schema: opening ' + o.id + ' type');
    if (!isNum(o.at) || o.at < 0) E.push('schema: opening ' + o.id + ' at');
    if (!isNum(o.w) || o.w <= 0) E.push('schema: opening ' + o.id + ' w');
    if (!isNum(o.sill) || o.sill < 0 || !isNum(o.head) || o.head <= 0 || o.head <= o.sill) E.push('schema: opening ' + o.id + ' sill/head (the 3D view needs both)');
    if (o.swing != null && o.swing !== 1 && o.swing !== -1) E.push('schema: opening ' + o.id + ' swing');
  }
  const RT = ['living', 'kitchen', 'bedroom', 'mamad', 'wet', 'hall', 'balcony', 'storage', 'other'], rid = new Set();
  if (!Array.isArray(apt.rooms) || !apt.rooms.length) E.push('schema: rooms');
  for (const r of apt.rooms || []) {
    for (const k in r) if (!['id', 'type', 'name_he', 'names', 'at', 'floor'].includes(k)) E.push('schema: room ' + r.id + ' field ' + k);
    if (!/^[a-z0-9_-]{1,40}$/.test(r.id || '') || rid.has(r.id)) E.push('schema: room id ' + r.id); rid.add(r.id);
    if (!RT.includes(r.type)) E.push('schema: room ' + r.id + ' type');
    if (typeof r.name_he !== 'string' || !r.name_he || r.name_he.length > 60) E.push('schema: room ' + r.id + ' name_he');
    if (!Array.isArray(r.at) || r.at.length !== 2 || !r.at.every(isNum)) E.push('schema: room ' + r.id + ' at');
  }
  for (const r of apt.rules || []) {
    if (AHEAD.rules.includes(r.code)) notes.push('rule ' + r.code + ' is read by core.js but not yet in the schema enum');
    else if (!['room.min_width', 'room.min_area', 'wet.max_distance_to_drain', 'door.clear_width'].includes(r.code)) E.push('schema: rule code ' + r.code);
    if (!Array.isArray(r.applies) || !isNum(r.value) || typeof r.source !== 'string') E.push('schema: rule ' + r.code);
  }
  const wset = new Set((apt.walls || []).map((w) => w.id)), pid = new Set();
  for (const p of apt.points || []) {
    if (typeof p.id !== 'string' || pid.has(p.id)) E.push('points: id ' + p.id); pid.add(p.id);
    if (!POINT_KINDS[p.kind]) E.push('points: ' + p.id + ' kind ' + p.kind);
    if (!(p.wall ? wset.has(p.wall) && isNum(p.at) : isNum(p.x) && isNum(p.y))) E.push('points: ' + p.id + ' needs a known wall and at, or x and y');
  }
  const sid = new Set();
  for (const it of apt.starter || []) {
    for (const k in it) if (!['id', 'sku', 'x', 'y', 'rot', 'status'].includes(k)) E.push('starter: ' + it.id + ' field ' + k);
    if (typeof it.id !== 'string' || sid.has(it.id)) E.push('starter: id ' + it.id); sid.add(it.id);
    if (!ITEMS[it.sku]) E.push('starter: ' + it.id + ' unknown sku ' + it.sku);
    if (![it.x, it.y, it.rot].every(isNum)) E.push('starter: ' + it.id + ' x/y/rot');
    if (!['base', 'upgrade', 'credit', 'decor', 'ai'].includes(it.status)) E.push('starter: ' + it.id + ' status');
  }
}

// ---- 2. the wall graph
function graph(apt, dv, E) {
  const N = apt.nodes, deg = {};
  const pairs = new Set();
  for (const w of apt.walls) {
    const L = len(sub(N[w.b], N[w.a]));
    if (L < 0.5) E.push('wall ' + w.id + ' has zero length');
    const key = [w.a, w.b].sort().join('|');
    if (pairs.has(key)) E.push('two walls on the corners ' + key); pairs.add(key);
    deg[w.a] = (deg[w.a] || 0) + 1; deg[w.b] = (deg[w.b] || 0) + 1;
    const d = sub(N[w.b], N[w.a]), u = [d[0] / L, d[1] / L];
    for (const k in N) { // a corner inside a wall that does not end there: an unsplit T-junction
      if (k === w.a || k === w.b) continue;
      const v = sub(N[k], N[w.a]), t = dot(v, u);
      if (t > 0.5 && t < L - 0.5 && Math.abs(crs(u, v)) < 0.5) E.push('corner ' + k + ' lies inside wall ' + w.id + ' (the wall must be split there)');
    }
  }
  for (const k in N) if ((deg[k] || 0) < 2) E.push('corner ' + k + ' is a dangling wall end (' + (deg[k] || 0) + ' wall)');
  const W = apt.walls;
  for (let i = 0; i < W.length; i++) for (let j = i + 1; j < W.length; j++) {
    const a = W[i], b = W[j];
    if ([a.a, a.b].some((x) => x === b.a || x === b.b)) continue;
    const p = N[a.a], r = sub(N[a.b], p), q = N[b.a], s = sub(N[b.b], q), d = crs(r, s);
    if (Math.abs(d) < 1e-9) continue;
    const t = crs(sub(q, p), s) / d, u = crs(sub(q, p), r) / d;
    if (t > 1e-4 && t < 1 - 1e-4 && u > 1e-4 && u < 1 - 1e-4) E.push('walls ' + a.id + ' and ' + b.id + ' cross without a corner');
  }
  // every face of the graph, the outer one included (same walk as core.js): the inner faces must tile the outline
  const out = {};
  const push = (u, v, w) => (out[u] = out[u] || []).push({ u, v, w, ang: Math.atan2(N[v][1] - N[u][1], N[v][0] - N[u][0]) });
  for (const w of W) { push(w.a, w.b, w); push(w.b, w.a, w); }
  for (const k in out) out[k].sort((p, q) => p.ang - q.ang);
  const seen = new Set(), faces = [], key = (h) => h.u + '>' + h.v + '>' + h.w.id;
  for (const k in out) for (const h0 of out[k]) {
    if (seen.has(key(h0))) continue;
    const ring = []; let h = h0, g = 0;
    while (!seen.has(key(h)) && g++ < 5000) { seen.add(key(h)); ring.push(h); const list = out[h.v], i = list.findIndex((x) => x.v === h.u && x.w === h.w); h = list[(i + 1) % list.length]; }
    faces.push(Math.abs(area(ring.map((x) => N[x.u]))) / 1e4);
  }
  faces.sort((a, b) => b - a);
  const outline = faces[0], inner = faces.slice(1).reduce((s, a) => s + a, 0);
  if (Math.abs(outline - inner) > 0.01) E.push('the spaces do not tile the outline: outline ' + outline.toFixed(2) + ' m², spaces ' + inner.toFixed(2) + ' m² (a wall crosses or a piece of the graph is loose)');
  return { outline, inner };
}

// ---- 3. rooms, openings, furniture
function rooms(apt, dv, E) {
  const placed = new Set();
  for (const f of dv.faces) {
    if (f.room) placed.add(f.room.id);
    for (const m of f.merged) { E.push('rooms ' + f.room.id + ' and ' + m + ' share one space (no wall or divider between their points)'); placed.add(m); }
    if (!f.room && Math.abs(f.gross) > 0.3) E.push('a closed space of ' + f.gross + ' m² has no room point (at ' + Math.round(f.bb.x0) + ',' + Math.round(f.bb.y0) + ')');
  }
  for (const r of apt.rooms) if (!placed.has(r.id)) E.push('room ' + r.id + ' (' + r.name_he + ') point ' + r.at + ' is in no closed space');
}
function openings(apt, dv, E) {
  for (const w of dv.walls) {
    const os = w.openings;
    for (const o of os) {
      if (o.at < 0 || o.at + o.w > w.L + 0.01) E.push('opening ' + o.id + ' runs past wall ' + w.id + ' (at ' + o.at + ' + ' + o.w + ' > ' + w.L.toFixed(1) + ')');
      if (w.kind === 'divider' || w.kind === 'rail') E.push('opening ' + o.id + ' sits on a ' + w.kind);
    }
    for (let i = 1; i < os.length; i++) if (os[i].at < os[i - 1].at + os[i - 1].w) E.push('openings ' + os[i - 1].id + ' and ' + os[i].id + ' overlap on wall ' + w.id);
  }
}
const rectOf = (it) => {
  const c = ITEMS[it.sku], a = (it.rot * Math.PI) / 180, ux = [Math.cos(a), Math.sin(a)], uy = [-Math.sin(a), Math.cos(a)], hw = c.w / 2, hd = c.d / 2;
  return [[-hw, -hd], [hw, -hd], [hw, hd], [-hw, hd]].map(([x, y]) => [it.x + x * ux[0] + y * uy[0], it.y + x * ux[1] + y * uy[1]]);
};
function overlap(P, Q) { // separating axis test for two convex quads, with 0.5 cm of grace
  for (const poly of [P, Q]) for (let i = 0; i < poly.length; i++) {
    const e = sub(poly[(i + 1) % poly.length], poly[i]), n = [-e[1], e[0]], L = len(n);
    const pa = P.map((p) => dot(p, n) / L), pb = Q.map((p) => dot(p, n) / L);
    if (Math.max(...pa) <= Math.min(...pb) + 0.5 || Math.max(...pb) <= Math.min(...pa) + 0.5) return false;
  }
  return true;
}
function furniture(apt, dv, E) {
  const roomFaces = dv.faces.filter((f) => f.room);
  for (const it of apt.starter || []) {
    if (!ITEMS[it.sku]) continue;
    const R = rectOf(it), home = roomFaces.find((f) => pip([it.x, it.y], f.poly));
    if (!home) { E.push('piece ' + it.id + ' (' + it.sku + ') centre is in no room'); continue; }
    for (const p of R) if (!roomFaces.some((f) => pip(p, f.poly))) { E.push('piece ' + it.id + ' (' + it.sku + ') pokes out of the apartment at ' + p.map(Math.round)); break; }
    for (const w of dv.walls) {
      if (w.kind === 'divider' || w.L < 1) continue;
      const n = [-w.dir[1], w.dir[0]], h = Math.max(w.t, 1) / 2;
      const band = [[w.pa[0] + n[0] * h, w.pa[1] + n[1] * h], [w.pb[0] + n[0] * h, w.pb[1] + n[1] * h], [w.pb[0] - n[0] * h, w.pb[1] - n[1] * h], [w.pa[0] - n[0] * h, w.pa[1] - n[1] * h]];
      if (overlap(R, band)) { E.push('piece ' + it.id + ' (' + it.sku + ' in ' + home.room.id + ') crosses wall ' + w.id + ' (' + w.kind + ')'); break; }
    }
  }
}

// ---- 4. published sizes (Ashira): a dimension line from the probe point, both ways, to the first wall face
function cast(dv, P, d, through) {
  let best = null;
  for (const w of dv.walls) {
    if (w.L < 0.5 || (through && w.kind === 'divider')) continue;
    const s = sub(w.pb, w.pa), den = crs(d, s);
    if (Math.abs(den) < 1e-9) continue;
    const q = sub(w.pa, P), t = crs(q, s) / den, u = crs(q, d) / den;
    if (t > 1e-6 && u >= -1e-6 && u <= 1 + 1e-6 && (!best || t < best.t)) best = { t, w, face: t - (w.t / 2) / (Math.abs(den) / len(s)) };
  }
  return best;
}
function published(apt, dv, E, rows) {
  const pub = PUB.plans[apt.id];
  if (!pub) return;
  for (const p of pub.probes) {
    const f = dv.faceBy[p.room];
    if (!f || !pip(p.at, f.poly)) { E.push('probe ' + p.room + ' ' + p.label + ': the point is not inside that room'); continue; }
    const a = cast(dv, p.at, p.dir, p.through_dividers), b = cast(dv, p.at, [-p.dir[0], -p.dir[1]], p.through_dividers);
    if (!a || !b) { E.push('probe ' + p.room + ' ' + p.label + ': no wall found'); continue; }
    const clear = a.face + b.face, dev = (clear - p.value) / p.value;
    rows.push({ room: p.room, name: f.room.name_he, studio: (pub.studio_d || {})[p.room] || '', label: p.label, value: p.value, clear, dev, extra: p.extra, walls: b.w.id + '..' + a.w.id });
    if (Math.abs(dev) > MAX_DEV) E.push('published size ' + p.room + ' ' + p.label + ': clear ' + clear.toFixed(1) + ' cm is ' + (dev * 100).toFixed(1) + '% off');
  }
}

// ---- run
export function checkPlan(apt) {
  const E = [], rows = [], notes = [];
  validate(apt, E, notes);
  if (E.length) return { E, rows, notes, table: [] };
  const design = emptyDesign(apt);
  design.items = (apt.starter || []).map((i) => ({ ...i }));
  const dv = derive(apt, design);
  const tiles = graph(apt, dv, E);
  rooms(apt, dv, E); openings(apt, dv, E); furniture(apt, dv, E); published(apt, dv, E, rows);
  const store = createStore(apt, design), q = quantities(store);
  const sumIn = Math.round(q.rooms.filter((r) => r.type !== 'balcony').reduce((s, r) => s + r.net, 0) * 10) / 10;
  const sumBal = Math.round(q.rooms.filter((r) => r.type === 'balcony').reduce((s, r) => s + r.net, 0) * 10) / 10;
  if (Math.abs(sumIn - q.net) > 0.05 || Math.abs(sumBal - q.balcony) > 0.05) E.push('total net ' + q.net + ' + balcony ' + q.balcony + ' differs from the sum of the rooms ' + sumIn + ' + ' + sumBal);
  return { E, rows, notes, q, sumIn, sumBal, tiles };
}

const isMain = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) {
  const index = JSON.parse(fs.readFileSync(path.join(DES, 'plans/index.json'), 'utf8'));
  const only = process.argv.slice(2);
  const summary = [];
  for (const entry of index.plans) {
    if (only.length && !only.includes(entry.id)) continue;
    const apt = JSON.parse(fs.readFileSync(path.join(DES, 'plans', entry.file), 'utf8'));
    const E = [];
    if (apt.id !== entry.id) E.push('index id ' + entry.id + ' but the file says ' + apt.id);
    if (apt.unit.type !== entry.type || apt.unit.rooms !== entry.rooms || apt.source.kind !== entry.source_kind || apt.source.label_he !== entry.label_he || apt.unit.project !== entry.project) E.push('index entry does not match the file (type, rooms, project, label or source kind)');
    const r = checkPlan(apt);
    E.push(...r.E);
    console.log('\n== ' + entry.id + '  (' + entry.file + ', ' + apt.source.kind + ': ' + apt.source.label_he + ', ' + apt.unit.rooms + ' rooms)');
    if (r.q) {
      console.log('  ' + pad('room', 22) + pad('type', 9) + lpad('clear W×D cm', 14) + lpad('net m²', 9));
      for (const x of r.q.rooms) console.log('  ' + pad(x.name + ' [' + x.id + ']', 22) + pad(x.type, 9) + lpad(x.w + '×' + x.d, 14) + lpad(x.net.toFixed(1), 9));
      console.log('  ' + pad('total net (inside)', 31) + lpad('', 14) + lpad(r.q.net.toFixed(1), 9) + '   sum of rooms ' + r.sumIn.toFixed(1) + ', balcony ' + r.q.balcony.toFixed(1) + ', outline ' + r.tiles.outline.toFixed(2) + ' = spaces ' + r.tiles.inner.toFixed(2) + ' m² (centre lines)');
    }
    if (r.rows.length) {
      console.log('  published sizes (clear wall face to wall face, along the printed dimension line):');
      console.log('  ' + pad('room', 22) + pad('studio d', 10) + lpad('printed', 8) + lpad('ours', 8) + lpad('dev', 8) + '  walls');
      for (const x of r.rows) console.log('  ' + pad(x.name + ' [' + x.room + ']', 22) + pad(x.studio, 10) + lpad(x.label + (x.extra ? '*' : ''), 8) + lpad(x.clear.toFixed(1), 8) + lpad((x.dev >= 0 ? '+' : '') + (x.dev * 100).toFixed(1) + '%', 8) + '  ' + x.walls);
      if (r.rows.some((x) => x.extra)) console.log('  * printed on the plan but not in the studio list');
    }
    for (const n of r.notes || []) console.log('  NOTE ' + n);
    for (const e of E) console.log('  FAIL ' + e);
    const worst = r.rows.length ? r.rows.reduce((m, x) => (Math.abs(x.dev) > Math.abs(m.dev) ? x : m)) : null;
    console.log('  ' + (E.length ? 'FAIL' : 'PASS') + '  ' + entry.id + (E.length ? '  (' + E.length + ' problems)' : '') + (worst ? '  largest deviation ' + (worst.dev * 100).toFixed(1) + '% (' + worst.room + ' ' + worst.label + ')' : ''));
    summary.push({ id: entry.id, ok: !E.length, worst });
  }
  console.log('\n' + summary.map((s) => pad(s.id, 14) + (s.ok ? 'PASS' : 'FAIL') + (s.worst ? '  max dev ' + (s.worst.dev * 100).toFixed(1) + '% (' + s.worst.room + ' ' + s.worst.label + ')' : '')).join('\n'));
  const bad = summary.filter((s) => !s.ok).length;
  console.log('\n' + (summary.length - bad) + ' of ' + summary.length + ' plans pass');
  process.exit(bad ? 1 : 0);
}
