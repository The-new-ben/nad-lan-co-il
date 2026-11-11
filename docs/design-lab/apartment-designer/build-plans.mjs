// node build-plans.mjs
// Writes the designer's plan files (HAD-701 / HAD-708) from the traced specs below:
//   plugins/nadlan-config/assets/designer/plans/ashira/E-4A.json, E-3B.json, E-5E.json, E-5F.json
//   plugins/nadlan-config/assets/designer/plans/example-3r.json, example-5r.json, index.json
//   docs/design-lab/apartment-designer/plans-published.json (the published sizes and where each one is measured)
// example-4r.json is never touched.
//
// How the Ashira plans were traced (details and every assumption: plans-notes.md):
// the four building-E sales plans were LOOKED AT (the private PDFs/PNGs are never copied); walls are written as polylines
// in the sheet's own pixel frame, scaled by a per-plan factor (cm per pixel) and then nudged so that every room size
// printed on the plan comes out as the clear wall-to-wall size. Topology (which wall meets which, where the doors are)
// follows the drawing; the printed numbers win over the drawing where the two disagree.
// The builder splits every wall where another wall meets it (T-junctions), merges shared corners into one node,
// and measures each opening from its wall's a-end.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, '../../..');
const PLANS = path.join(repo, 'plugins/nadlan-config/assets/designer/plans');
const T = { facade: 25, structural: 25, mamad: 30, shaft: 25, partition: 10, divider: 0, rail: 8 };
const PREFIX = { facade: 'f', structural: 's', mamad: 'm', shaft: 'h', partition: 'p', divider: 'v', rail: 'r' };
const FLOOR = { living: 'porcelain-80', kitchen: 'porcelain-80', bedroom: 'porcelain-80', mamad: 'porcelain-80', hall: 'porcelain-80', storage: 'porcelain-80', other: 'porcelain-80', wet: 'porcelain-60', balcony: 'deck' };
const OPEN = { door: { sill: 0, head: 210 }, window: { sill: 95, head: 215 }, slider: { sill: 0, head: 230 }, open: { sill: 0, head: 210 } };
const RULES = [
  { code: 'room.min_width', applies: ['bedroom'], value: 260, source: 'spike value, to be verified against the Planning and Building Regulations before any public use' },
  { code: 'room.min_area', applies: ['bedroom'], value: 8, source: 'spike value, to be verified against the Planning and Building Regulations before any public use' },
];
const TOL = 0.6;
const r1 = (v) => Math.round(v * 10) / 10;
const sub = (a, b) => [a[0] - b[0], a[1] - b[1]];
const dot = (a, b) => a[0] * b[0] + a[1] * b[1];
const crs = (a, b) => a[0] * b[1] - a[1] * b[0];
const len = (a) => Math.hypot(a[0], a[1]);

function build(spec) {
  const tf0 = spec.tf || ((p) => p);
  // pass 1: transform, find the shift that puts the plan's top-left corner at 0,0
  const raw = [];
  for (const w of spec.walls) { const pts = w.pts.map(tf0); for (let i = 0; i < pts.length - 1; i++) raw.push({ a: pts[i], b: pts[i + 1], kind: w.kind, t: w.t ?? T[w.kind] }); }
  const minX = Math.min(...raw.flatMap((s) => [s.a[0], s.b[0]])), minY = Math.min(...raw.flatMap((s) => [s.a[1], s.b[1]]));
  const f = (p) => { const q = tf0(p); return [q[0] - minX, q[1] - minY]; };
  for (const s of raw) { s.a = [s.a[0] - minX, s.a[1] - minY]; s.b = [s.b[0] - minX, s.b[1] - minY]; }
  // every end point, plus any place where two walls cross without a corner (reported: a traced plan should not have one)
  const pts = [];
  for (const s of raw) pts.push(s.a, s.b);
  for (let i = 0; i < raw.length; i++) for (let j = i + 1; j < raw.length; j++) {
    const p = raw[i].a, r = sub(raw[i].b, p), q = raw[j].a, s = sub(raw[j].b, q), d = crs(r, s);
    if (Math.abs(d) < 1e-9) continue;
    const t = crs(sub(q, p), s) / d, u = crs(sub(q, p), r) / d;
    if (t > 1e-3 && t < 1 - 1e-3 && u > 1e-3 && u < 1 - 1e-3) { console.log(spec.id + ': four-way corner added where two walls cross at ' + r1(p[0] + t * r[0]) + ',' + r1(p[1] + t * r[1])); pts.push([p[0] + t * r[0], p[1] + t * r[1]]); }
  }
  // merge into nodes
  const nodes = [];
  const nodeOf = (p) => { for (let i = 0; i < nodes.length; i++) if (Math.hypot(nodes[i][0] - p[0], nodes[i][1] - p[1]) < TOL) return i; nodes.push([p[0], p[1]]); return nodes.length - 1; };
  pts.forEach(nodeOf);
  // split every wall at every node lying on it
  const walls = [], seen = new Set(), cnt = {};
  for (const s of raw) {
    const v = sub(s.b, s.a), L = len(v), dir = [v[0] / L, v[1] / L];
    const on = [];
    nodes.forEach((n, i) => { const w = sub(n, s.a), t = dot(w, dir); if (t > TOL && t < L - TOL && Math.abs(crs(dir, w)) < TOL) on.push([t, i]); });
    on.sort((x, y) => x[0] - y[0]);
    const chain = [nodeOf(s.a), ...on.map((x) => x[1]), nodeOf(s.b)];
    for (let i = 0; i < chain.length - 1; i++) {
      const a = chain[i], b = chain[i + 1], key = Math.min(a, b) + '-' + Math.max(a, b);
      if (a === b) throw new Error(spec.id + ': zero-length wall');
      if (seen.has(key)) throw new Error(spec.id + ': two walls on the same corners ' + key);
      seen.add(key);
      cnt[s.kind] = (cnt[s.kind] || 0) + 1;
      walls.push({ id: PREFIX[s.kind] + cnt[s.kind], a, b, t: s.t, kind: s.kind });
    }
  }
  const nid = (i) => 'n' + (i + 1);
  const N = Object.fromEntries(nodes.map((p, i) => [nid(i), [r1(p[0]), r1(p[1])]]));
  const W = walls.map((w) => ({ id: w.id, a: nid(w.a), b: nid(w.b), t: w.t, kind: w.kind }));
  // openings: placed on the wall whose centre line passes the given point, centred on it, measured from the a-end
  const openings = spec.openings.map((o) => {
    const p = f(o.near);
    let best = null;
    for (const w of W) {
      const A = N[w.a], B = N[w.b], v = sub(B, A), L = len(v), dir = [v[0] / L, v[1] / L], d = sub(p, A), t = dot(d, dir), off = Math.abs(crs(dir, d));
      if (t < 0 || t > L || off > w.t / 2 + 4) continue;
      if (!best || off < best.off) best = { w, t, off, L, dir, A };
    }
    if (!best) throw new Error(spec.id + ': no wall under opening ' + o.id);
    const at = Math.round(best.t - o.w / 2);
    if (at < 0 || at + o.w > best.L + 1e-6) throw new Error(spec.id + ': opening ' + o.id + ' does not fit wall ' + best.w.id + ' (L ' + r1(best.L) + ', at ' + at + ', w ' + o.w + ')');
    const out = { id: o.id, wall: best.w.id, type: o.type, at, w: o.w, sill: o.sill ?? OPEN[o.type].sill, head: o.head ?? OPEN[o.type].head };
    if (o.type === 'door') {
      const n = [-best.dir[1], best.dir[0]], into = sub(f(o.into), [best.A[0] + best.dir[0] * at, best.A[1] + best.dir[1] * at]);
      out.swing = dot(into, n) >= 0 ? 1 : -1;
    }
    return out;
  });
  const rooms = spec.rooms.map((r) => { const at = f(r.at); return { id: r.id, type: r.type, name_he: r.name_he, at: [Math.round(at[0]), Math.round(at[1])], floor: FLOOR[r.type] }; });
  let k = 0;
  const starter = (spec.starter || []).map(([sku, at, rot]) => { const p = f(at); return { id: 's' + ++k, sku, x: Math.round(p[0]), y: Math.round(p[1]), rot: ((rot % 360) + 360) % 360, status: 'decor' }; });
  const apt = {
    schema: 'nadlan-apartment', v: 1, id: spec.id, geometry_revision: spec.rev, source: spec.source, unit: spec.unit, units: 'cm',
    frame: { origin: 'plan-top-left', x: 'right', y: 'down', rot: 'deg-cw' }, north_deg: spec.north_deg,
    levels: [{ id: 'L0', height: spec.height || 270, slab: 25 }], nodes: N, walls: W, openings, rooms, rules: RULES, starter,
  };
  const probes = (spec.probes || []).map((p) => { const at = f(p.at); return { room: p.room, label: p.label, value: p.value, at: [r1(at[0]), r1(at[1])], dir: p.dir === 'x' ? [1, 0] : p.dir === 'y' ? [0, 1] : p.dir.map((x) => Math.round(x * 1e4) / 1e4), through_dividers: !!p.through, extra: !!p.extra, why: p.why } });
  return { apt, probes };
}

// ---------------------------------------------------------------- Ashira building E (sales plans, 2026-10-18 capture)
const ASHIRA_SRC = (type) => ({ kind: 'sales-plan', label_he: 'לפי תוכנית המכר שפורסמה', note: 'Our own redraw of the published building E sales plan ' + type + ' (Ashira, Sde Dov). Room sizes follow the printed dimensions; the drawing is not to scale, so other walls are traced and may differ by a few centimetres. The signed sales plan is binding.', date: '2026-11-11' });
const ashiraUnit = (type, rooms) => ({ project: 'ashira', unit_id: null, tower: 'E', floor: null, type, rooms });
const scale = (kx, ky, ox = 0, oy = 0) => (p) => [(p[0] - ox) * kx, (p[1] - oy) * ky];

// E-4A: 4 rooms, north-west corner. Sheet pixels at ~1.00 cm per pixel (checked on 718, 683, 513, 270, 348, 373).
const E4A = {
  id: 'ashira-e-4a', rev: 'ashira-E-4A:2026-11-11:a', source: ASHIRA_SRC('E-4A'), unit: ashiraUnit('E-4A', 4), north_deg: 11,
  tf: scale(1, 1),
  walls: [
    { kind: 'facade', pts: [[640, 860], [640, 1638]] },                       // the west glazing line
    { kind: 'structural', pts: [[640, 1638], [1475, 1638], [1475, 1300], [1580, 1300], [1580, 1095]] },
    { kind: 'structural', pts: [[1495, 1095], [1821, 1095], [1821, 540]] },
    { kind: 'structural', pts: [[1821, 850], [1748, 850], [1748, 880]] },        // the shaft notch in the second bedroom
    { kind: 'facade', pts: [[1065, 540], [1821, 540]] },                        // the north glazing of both bedrooms
    { kind: 'facade', pts: [[1065, 540], [1065, 860]] },                        // bedroom wall facing the balcony
    { kind: 'facade', pts: [[640, 860], [1065, 860]] },                         // living glazing onto the balcony
    { kind: 'partition', pts: [[1065, 860], [1375, 860]] },
    { kind: 'rail', pts: [[640, 860], [648, 770], [675, 690], [720, 620], [785, 570], [865, 543], [950, 540], [1065, 540]] },
    { kind: 'partition', pts: [[1430.5, 540], [1430.5, 705]] },
    { kind: 'partition', pts: [[1375, 705], [1495, 705]] },
    { kind: 'partition', pts: [[1375, 705], [1375, 1065]] },
    { kind: 'divider', pts: [[1375, 1065], [1375, 1350]] },
    { kind: 'partition', pts: [[1495, 705], [1495, 1095]] },
    { kind: 'partition', pts: [[1495, 880], [1748, 880]] },
    { kind: 'partition', pts: [[640, 1350], [1340, 1350]] },
    { kind: 'divider', pts: [[1340, 1350], [1375, 1350]] },
    { kind: 'partition', pts: [[1340, 1350], [1340, 1638]] },
    { kind: 'partition', pts: [[1165, 1468], [1475, 1468]] },
    { kind: 'partition', pts: [[1165, 1468], [1165, 1638]] },
    { kind: 'divider', pts: [[640, 1180], [1210, 1180], [1210, 1350]] },
    { kind: 'divider', pts: [[1375, 1095], [1495, 1095]] },               // corridor | entrance hall
  ],
  openings: [
    { id: 'o-slider-balcony', type: 'slider', near: [850, 860], w: 300 },
    { id: 'o-win-living', type: 'window', near: [640, 1020], w: 260, sill: 40, head: 230 },
    { id: 'o-win-kitchen', type: 'window', near: [640, 1265], w: 120, sill: 105 },
    { id: 'o-win-master', type: 'window', near: [640, 1494], w: 180 },
    { id: 'o-win-bed1', type: 'window', near: [1230, 540], w: 200 },
    { id: 'o-win-bed2', type: 'window', near: [1640, 540], w: 200 },
    { id: 'o-entry', type: 'door', near: [1580, 1240], w: 100, into: [1530, 1240] },
    { id: 'o-door-bed1', type: 'door', near: [1375, 757], w: 90, into: [1300, 757] },
    { id: 'o-door-bed2', type: 'door', near: [1495, 760], w: 90, into: [1560, 760] },
    { id: 'o-door-bath', type: 'door', near: [1495, 940], w: 80, into: [1560, 940] },
    { id: 'o-door-master', type: 'door', near: [1290, 1350], w: 90, into: [1290, 1400] },
    { id: 'o-door-ens', type: 'door', near: [1215, 1468], w: 80, into: [1215, 1520] },
    { id: 'o-door-wc', type: 'door', near: [1410, 1468], w: 80, into: [1410, 1520] },
  ],
  rooms: [
    { id: 'living', type: 'living', name_he: 'חדר דיור ופינת אוכל', at: [900, 1000] },
    { id: 'kitchen', type: 'kitchen', name_he: 'מטבח', at: [900, 1270] },
    { id: 'balcony', type: 'balcony', name_he: 'מרפסת', at: [850, 700] },
    { id: 'bed1', type: 'bedroom', name_he: 'חדר שינה', at: [1200, 700] },
    { id: 'bed2', type: 'bedroom', name_he: 'חדר שינה', at: [1650, 700] },
    { id: 'bath', type: 'wet', name_he: 'חדר רחצה', at: [1650, 990] },
    { id: 'corridor', type: 'hall', name_he: 'מסדרון', at: [1435, 900] },
    { id: 'hall', type: 'hall', name_he: 'מבואה', at: [1430, 1250] },
    { id: 'master', type: 'bedroom', name_he: 'חדר שינה הורים', at: [900, 1500] },
    { id: 'ens', type: 'wet', name_he: 'חדר רחצה', at: [1250, 1550] },
    { id: 'wc', type: 'wet', name_he: 'שירותי אורחים', at: [1410, 1550] },
  ],
  probes: [
    { room: 'living', label: '718', value: 718, at: [1000, 960], dir: 'x', through: true, why: 'living and dining width, west glazing to the wall beside the hall' },
    { room: 'living', label: '473', value: 473, at: [710, 1000], dir: 'y', through: true, why: 'balcony glazing to the master bedroom wall, across the open kitchen' },
    { room: 'master', label: '683', value: 683, at: [1000, 1400], dir: 'x', why: 'upper width of the L-shaped master bedroom (the studio listed 683 under the kitchen; on the plan it is printed inside the master bedroom)' },
    { room: 'master', label: '513', value: 513, at: [900, 1560], dir: 'x', why: 'lower width beside the en-suite' },
    { room: 'master', label: '270', value: 270, at: [690, 1500], dir: 'y', why: 'depth' },
    { room: 'bed1', label: '348', value: 348, at: [1200, 590], dir: 'x', why: 'width at the window, including the wardrobe niche' },
    { room: 'bed1', label: '288', value: 288, at: [1200, 780], dir: 'x', why: 'width below the niche' },
    { room: 'bed2', label: '373', value: 373, at: [1600, 580], dir: 'x', why: 'width at the window, including the desk niche' },
    { room: 'bed2', label: '313', value: 313, at: [1600, 800], dir: 'x', why: 'width below the niche' },
    { room: 'bed2', label: '283', value: 283, at: [1790, 700], dir: 'y', extra: true, why: 'depth at the east wall, above the shaft notch (printed on the plan, not in the studio list)' },
  ],
  starter: [
    ['gen.sofa3', [1020, 1010], 90], ['gen.rug', [840, 1010], 90], ['gen.tv', [680, 1010], 270],
    ['gen.dining6', [1250, 1000], 0], ['gen.chair', [1205, 926], 0], ['gen.chair', [1295, 926], 0], ['gen.chair', [1205, 1074], 180], ['gen.chair', [1295, 1074], 180],
    ['gen.kitchen', [821, 1313], 180],
    ['gen.bedset', [800, 1523], 180], ['gen.wardrobe2', [1050, 1592], 180],
    ['gen.bed160', [1170, 658], 0], ['gen.wardrobe2', [1150, 822], 180],
    ['gen.bed160', [1718, 658], 0], ['gen.wardrobe2', [1570, 842], 180],
    ['gen.plant', [1000, 600], 0], ['gen.plant', [690, 1145], 0],
  ],
};

// E-3B: 3 rooms, south-east corner. ~0.89 cm per pixel. The bedroom wing is turned 17.5 degrees on the sheet.
const o3 = [209, 245], U3 = [Math.cos((17.5 * Math.PI) / 180), -Math.sin((17.5 * Math.PI) / 180)], V3 = [-U3[1], U3[0]];
const Wg = (u, v) => [o3[0] + u * U3[0] + v * V3[0], o3[1] + u * U3[1] + v * V3[1]];
const atY = (u, Y) => { const b = Wg(u, 0), v = (Y - b[1]) / V3[1]; return [b[0] + v * V3[0], Y]; }; // the wing line u=const at height Y
const UU = 645.5, VM = 295.5, VE = 175, UA = 200, UC = 320, VB = 586, YL = 579.5, XG = 734.5;
const E1 = atY(0, 342), B0 = atY(0, YL), B1 = atY(UA, YL), C1 = atY(UC, YL);
const bedA = Wg(UC, VB), bedB = Wg(UU, VB), G3 = [XG, bedA[1] + ((XG - bedA[0]) / (bedB[0] - bedA[0])) * (bedB[1] - bedA[1])];
const E3B = {
  id: 'ashira-e-3b', rev: 'ashira-E-3B:2026-11-11:a', source: ASHIRA_SRC('E-3B'), unit: ashiraUnit('E-3B', 3), north_deg: 296,
  walls: [
    { kind: 'structural', pts: [Wg(0, 0), Wg(UA, 0), Wg(UU, 0)] },
    { kind: 'facade', pts: [Wg(UU, 0), Wg(UU, VM), Wg(UU, VB)] },
    { kind: 'structural', pts: [Wg(0, 0), E1] },
    { kind: 'partition', pts: [E1, Wg(0, VE), B0] },
    { kind: 'partition', pts: [Wg(UA, 0), Wg(UA, VE), Wg(UA, VM), B1] },
    { kind: 'partition', pts: [Wg(0, VE), Wg(UA, VE)] },
    { kind: 'partition', pts: [Wg(UA, VM), Wg(UC, VM), Wg(UU, VM)] },
    { kind: 'partition', pts: [Wg(UC, VM), C1, bedA] },
    { kind: 'facade', pts: [bedA, G3, bedB] },
    { kind: 'partition', pts: [B0, B1] },
    { kind: 'divider', pts: [B1, C1] },
    { kind: 'facade', pts: [G3, [XG, 970]] },
    { kind: 'facade', pts: [[XG, 970], [293, 970], [44.5, 970]] },
    { kind: 'structural', pts: [[44.5, 970], [44.5, 673.5], [44.5, 400], E1] },
    { kind: 'divider', pts: [[44.5, 673.5], [293, 673.5], [B0[0], 673.5], B0] },
    { kind: 'divider', pts: [[293, 673.5], [293, 970]] },
    { kind: 'rail', pts: [[XG, 970], [830, 975], [925, 960], [1000, 905], [1050, 820], [1060, 720], [1035, 645], bedB] },
  ],
  openings: [
    { id: 'o-entry', type: 'door', near: [151, 368.3], w: 100, into: [151, 450] },
    { id: 'o-door-ens', type: 'door', near: Wg(UA, 90), w: 80, into: Wg(150, 90) },
    { id: 'o-door-bath', type: 'door', near: Wg(UA, 350), w: 80, into: Wg(150, 350) },
    { id: 'o-door-master', type: 'door', near: Wg(260, VM), w: 90, into: Wg(260, 250) },
    { id: 'o-door-bed1', type: 'door', near: Wg(UC, 370), w: 90, into: Wg(380, 370) },
    { id: 'o-win-master', type: 'window', near: Wg(UU, 150), w: 180 },
    { id: 'o-win-bed1', type: 'window', near: Wg(UU, 440), w: 160 },
    { id: 'o-win-bed1-south', type: 'window', near: Wg(480, VB), w: 160 },
    { id: 'o-slider-balcony', type: 'slider', near: [XG, 830], w: 220 },
    { id: 'o-win-living', type: 'window', near: [520, 970], w: 300, sill: 40, head: 230 },
    { id: 'o-win-kitchen', type: 'window', near: [170, 970], w: 120, sill: 105 },
  ],
  rooms: [
    { id: 'living', type: 'living', name_he: 'חדר דיור', at: [450, 800] },
    { id: 'kitchen', type: 'kitchen', name_he: 'מטבח', at: [170, 820] },
    { id: 'dining', type: 'living', name_he: 'פינת אוכל', at: [150, 520] },
    { id: 'hall', type: 'hall', name_he: 'מסדרון', at: Wg(260, 380) },
    { id: 'master', type: 'bedroom', name_he: 'חדר שינה הורים', at: Wg(420, 150) },
    { id: 'bed1', type: 'bedroom', name_he: 'חדר שינה', at: Wg(480, 440) },
    { id: 'ens', type: 'wet', name_he: 'חדר רחצה', at: Wg(100, 90) },
    { id: 'bath', type: 'wet', name_he: 'חדר רחצה', at: Wg(100, 260) },
    { id: 'balcony', type: 'balcony', name_he: 'מרפסת', at: [900, 800] },
  ],
  probes: [
    { room: 'living', label: '665', value: 665, at: [427, 918], dir: 'x', through: true, why: 'west wall to the balcony glazing, across the open kitchen' },
    { room: 'living', label: '373', value: 373, at: [330, 765], dir: 'y', through: true, why: 'bathroom wall to the south glazing' },
    { room: 'kitchen', label: '284', value: 284, at: [138, 805], dir: 'y', why: 'kitchen run, south glazing to the end of the cabinets' },
    { room: 'master', label: '428', value: 428, at: Wg(420, 150), dir: U3, why: 'along the wing' },
    { room: 'master', label: '278', value: 278, at: Wg(420, 150), dir: V3, why: 'across the wing' },
    { room: 'bed1', label: '308', value: 308, at: Wg(480, 440), dir: U3, why: 'along the wing' },
    { room: 'bed1', label: '273', value: 273, at: Wg(480, 440), dir: V3, why: 'across the wing' },
  ],
  starter: [
    ['gen.sofa3', [515, 650], 0], ['gen.rug', [515, 800], 0], ['gen.tv', [515, 934], 180],
    ['gen.dining6', [165, 540], 90], ['gen.chair', [92, 500], 270], ['gen.chair', [92, 580], 270], ['gen.chair', [238, 500], 90], ['gen.chair', [238, 580], 90],
    ['gen.kitchen', [90, 789.5], 270],
    ['gen.bedset', Wg(500, 115.5), 342.5], ['gen.wardrobe2', Wg(290, 46.5), 342.5],
    ['gen.bed160', Wg(520, 468), 162.5], ['gen.wardrobe2', Wg(359, 500), 252.5],
    ['gen.plant', [900, 880], 0],
  ],
};

// E-5E: 5 rooms, north-west, balcony with a jacuzzi. ~1.08 cm per pixel.
const E5E = {
  id: 'ashira-e-5e', rev: 'ashira-E-5E:2026-11-11:a', source: ASHIRA_SRC('E-5E'), unit: ashiraUnit('E-5E', 5), north_deg: 349,
  tf: scale(1.08, 1.08, 600, 340),
  walls: [
    { kind: 'facade', pts: [[667, 660], [1555, 660], [1625, 675], [1680, 725], [1712, 830], [1712, 1767]] },
    { kind: 'structural', pts: [[1712, 1767], [1205, 1767], [1205, 1250], [1140, 1250], [1140, 1310], [1000, 1310], [1000, 1214], [667, 1214], [667, 660]] },
    { kind: 'rail', pts: [[667, 660], [667, 385], [1555, 385], [1660, 410], [1740, 480], [1775, 600], [1775, 830], [1712, 830]] },
    { kind: 'partition', pts: [[1140, 660], [1140, 1135]] },
    { kind: 'divider', pts: [[1140, 1135], [1140, 1214], [1000, 1214]] },
    { kind: 'divider', pts: [[667, 949], [987, 949], [987, 1214]] },
    { kind: 'partition', pts: [[1416, 660], [1416, 880], [1438, 880], [1438, 966]] },
    { kind: 'partition', pts: [[1140, 966], [1438, 966]] },
    { kind: 'partition', pts: [[1305, 966], [1305, 1135], [1140, 1135]] },
    { kind: 'partition', pts: [[1406, 966], [1406, 1595]] },
    { kind: 'partition', pts: [[1406, 1200], [1712, 1200]] },
    { kind: 'partition', pts: [[1530, 1200], [1530, 1035], [1712, 1035]] },
    { kind: 'partition', pts: [[1406, 1480], [1712, 1480]] },
    { kind: 'partition', pts: [[1205, 1595], [1443, 1595], [1443, 1767]] },
    { kind: 'divider', pts: [[1305, 1135], [1305, 1250], [1205, 1250]] }, // entrance hall | corridor
  ],
  openings: [
    { id: 'o-slider-balcony', type: 'slider', near: [900, 660], w: 350 },
    { id: 'o-win-bed1', type: 'window', near: [1280, 660], w: 180 },
    { id: 'o-win-master', type: 'window', near: [1490, 660], w: 120 },
    { id: 'o-win-master-east', type: 'window', near: [1712, 930], w: 160 },
    { id: 'o-win-ens', type: 'window', near: [1712, 1117], w: 60, sill: 150, head: 210 },
    { id: 'o-win-bed2', type: 'window', near: [1712, 1340], w: 160 },
    { id: 'o-win-bed3', type: 'window', near: [1712, 1620], w: 160 },
    { id: 'o-entry', type: 'door', near: [1068, 1310], w: 100, into: [1068, 1260] },
    { id: 'o-door-wc', type: 'door', near: [1230, 1135], w: 80, into: [1230, 1080] },
    { id: 'o-door-bed1', type: 'door', near: [1355, 966], w: 90, into: [1355, 920] },
    { id: 'o-door-master', type: 'door', near: [1406, 1025], w: 90, into: [1450, 1025] },
    { id: 'o-door-ens', type: 'door', near: [1530, 1090], w: 80, into: [1600, 1090] },
    { id: 'o-door-bed2', type: 'door', near: [1406, 1310], w: 90, into: [1460, 1310] },
    { id: 'o-door-bed3', type: 'door', near: [1406, 1537], w: 90, into: [1430, 1537] },
    { id: 'o-door-bath', type: 'door', near: [1340, 1595], w: 80, into: [1340, 1650] },
  ],
  rooms: [
    { id: 'living', type: 'living', name_he: 'חדר דיור ופינת אוכל', at: [800, 800] },
    { id: 'kitchen', type: 'kitchen', name_he: 'מטבח', at: [800, 1100] },
    { id: 'balcony', type: 'balcony', name_he: 'מרפסת', at: [1100, 520] },
    { id: 'bed1', type: 'bedroom', name_he: 'חדר שינה', at: [1280, 800] },
    { id: 'master', type: 'bedroom', name_he: 'חדר שינה הורים', at: [1580, 800] },
    { id: 'ens', type: 'wet', name_he: 'חדר רחצה', at: [1620, 1120] },
    { id: 'wc', type: 'wet', name_he: 'שירותי אורחים', at: [1220, 1050] },
    { id: 'hall', type: 'hall', name_he: 'מבואה', at: [1250, 1200] },
    { id: 'corridor', type: 'hall', name_he: 'מסדרון', at: [1300, 1400] },
    { id: 'bed2', type: 'bedroom', name_he: 'חדר שינה', at: [1560, 1340] },
    { id: 'bed3', type: 'bedroom', name_he: 'חדר שינה', at: [1580, 1620] },
    { id: 'bath', type: 'wet', name_he: 'חדר רחצה', at: [1320, 1690] },
  ],
  probes: [
    { room: 'living', label: '493', value: 493, at: [900, 900], dir: 'x', through: true, why: 'west wall to the bedroom wall' },
    { room: 'living', label: '573', value: 573, at: [888, 900], dir: 'y', through: true, why: 'balcony glazing to the kitchen wall, across the open kitchen' },
    { room: 'kitchen', label: '333', value: 333, at: [800, 1100], dir: 'x', why: 'kitchen run along the south wall' },
    { room: 'kitchen', label: '273', value: 273, at: [745, 1100], dir: 'y', why: 'kitchen run along the west wall' },
    { room: 'bed1', label: '288', value: 288, at: [1300, 705], dir: 'x', why: 'width' },
    { room: 'bed1', label: '313', value: 313, at: [1275, 800], dir: 'y', why: 'depth' },
    { room: 'master', label: '278', value: 278, at: [1580, 940], dir: 'x', why: 'width at the foot of the bed' },
    { room: 'master', label: '558', value: 558, at: [1495, 980], dir: 'y', why: 'depth of the suite, glazing to the second bedroom wall, through the dressing area' },
    { room: 'bed2', label: '313', value: 313, at: [1550, 1300], dir: 'x', why: 'width' },
    { room: 'bed2', label: '283', value: 283, at: [1500, 1340], dir: 'y', why: 'depth' },
    { room: 'bed3', label: '292', value: 292, at: [1515, 1620], dir: 'y', why: 'depth' },
    { room: 'bed3', label: '273', value: 273, at: [1560, 1700], dir: 'x', why: 'width' },
  ],
  starter: [
    ['gen.sofa3', [905, 805], 270], ['gen.rug', [1010, 805], 90], ['gen.tv', [1113, 805], 90],
    ['gen.dining6', [775, 800], 90], ['gen.chair', [707, 760], 270], ['gen.chair', [707, 840], 270],
    ['gen.kitchen', [833, 1172], 180],
    ['gen.bedset', [1590, 905], 90], ['gen.wardrobe2', [1496, 1130], 90],
    ['gen.bed160', [1250, 775], 90], ['gen.wardrobe2', [1215, 924], 180],
    ['gen.bed160', [1600, 1300], 270], ['gen.bed160', [1600, 1600], 270],
    ['gen.plant', [720, 450], 0], ['gen.plant', [1500, 450], 0],
  ],
};

// E-5F: 5-room penthouse, floor 16, wrap-around balcony west and north. ~1.46 cm per pixel across, ~1.52 down.
const E5F = {
  id: 'ashira-e-5f', rev: 'ashira-E-5F:2026-11-11:a', source: ASHIRA_SRC('E-5F'), unit: { ...ashiraUnit('E-5F', 5), floor: 16 }, north_deg: 349,
  tf: scale(1.46, 1.52, 800, 200),
  walls: [
    { kind: 'facade', pts: [[1008, 1739], [1008, 710], [1022, 660], [1055, 625], [1110, 605], [1480, 605]] },
    { kind: 'structural', pts: [[1480, 605], [1480, 753], [1423, 753], [1423, 1107]] },
    { kind: 'partition', pts: [[1375, 1107], [1423, 1107]] },
    { kind: 'structural', pts: [[1423, 1107], [1495, 1107], [1495, 1460], [1580, 1460], [1580, 1826]] },
    { kind: 'facade', pts: [[1580, 1826], [1095, 1826], [1055, 1815], [1025, 1790], [1008, 1739]] },
    { kind: 'divider', pts: [[1008, 990], [1272, 990], [1272, 1173]] },
    { kind: 'partition', pts: [[1008, 1173], [1290, 1173]] },
    { kind: 'divider', pts: [[1290, 1173], [1375, 1173]] },
    { kind: 'partition', pts: [[1375, 1107], [1375, 1619]] },
    { kind: 'partition', pts: [[1375, 1255], [1495, 1255]] },
    { kind: 'partition', pts: [[1375, 1460], [1495, 1460]] },
    { kind: 'partition', pts: [[1375, 1587], [1580, 1587]] },
    { kind: 'partition', pts: [[1290, 1173], [1290, 1619]] },
    { kind: 'partition', pts: [[1008, 1358], [1290, 1358]] },
    { kind: 'partition', pts: [[1008, 1548], [1290, 1548]] },
    { kind: 'partition', pts: [[1250, 1619], [1375, 1619]] },
    { kind: 'partition', pts: [[1250, 1619], [1250, 1826]] },
    { kind: 'rail', pts: [[1448, 605], [1448, 225], [1000, 225], [915, 240], [860, 290], [838, 380], [836, 1700], [855, 1765], [905, 1810], [975, 1830], [1095, 1826]] },
    { kind: 'divider', pts: [[837.5, 710], [1008, 710]] },                 // north part | west part of the one balcony
  ],
  openings: [
    { id: 'o-entry', type: 'door', near: [1480, 700], w: 100, into: [1450, 700] },
    { id: 'o-slider-north', type: 'slider', near: [1280, 605], w: 400 },
    { id: 'o-slider-west', type: 'slider', near: [1008, 850], w: 300 },
    { id: 'o-win-kitchen', type: 'window', near: [1008, 1080], w: 150, sill: 105 },
    { id: 'o-win-bed1', type: 'window', near: [1008, 1265], w: 160 },
    { id: 'o-win-bed2', type: 'window', near: [1008, 1453], w: 160 },
    { id: 'o-win-bed3', type: 'window', near: [1008, 1640], w: 160 },
    { id: 'o-win-master', type: 'window', near: [1430, 1826], w: 200 },
    { id: 'o-door-bed1', type: 'door', near: [1290, 1260], w: 90, into: [1250, 1260] },
    { id: 'o-door-bed2', type: 'door', near: [1290, 1430], w: 90, into: [1250, 1430] },
    { id: 'o-door-bed3', type: 'door', near: [1290, 1583], w: 90, into: [1270, 1583] },
    { id: 'o-door-master', type: 'door', near: [1332, 1619], w: 90, into: [1332, 1680] },
    { id: 'o-door-wc', type: 'door', near: [1375, 1214], w: 80, into: [1420, 1214] },
    { id: 'o-door-bath', type: 'door', near: [1375, 1390], w: 80, into: [1420, 1390] },
    { id: 'o-door-bath2', type: 'door', near: [1375, 1530], w: 80, into: [1420, 1530] },
  ],
  rooms: [
    { id: 'living', type: 'living', name_he: 'חדר דיור ופינת אוכל', at: [1200, 800] },
    { id: 'kitchen', type: 'kitchen', name_he: 'מטבח', at: [1140, 1080] },
    { id: 'balcony', type: 'balcony', name_he: 'מרפסת', at: [930, 500] },
    { id: 'balcony-w', type: 'balcony', name_he: 'מרפסת', at: [920, 1200] },
    { id: 'bed1', type: 'bedroom', name_he: 'חדר שינה', at: [1150, 1265] },
    { id: 'bed2', type: 'bedroom', name_he: 'חדר שינה', at: [1150, 1450] },
    { id: 'bed3', type: 'bedroom', name_he: 'חדר שינה', at: [1130, 1690] },
    { id: 'master', type: 'bedroom', name_he: 'חדר שינה הורים', at: [1450, 1700] },
    { id: 'hall', type: 'hall', name_he: 'מסדרון', at: [1332, 1400] },
    { id: 'wc', type: 'wet', name_he: 'שירותי אורחים', at: [1435, 1180] },
    { id: 'bath', type: 'wet', name_he: 'חדר רחצה', at: [1435, 1360] },
    { id: 'bath2', type: 'wet', name_he: 'חדר רחצה', at: [1480, 1520] },
  ],
  probes: [
    { room: 'living', label: '583', value: 583, at: [1250, 870], dir: 'x', through: true, why: 'west glazing to the entrance wall' },
    { room: 'living', label: '858', value: 858, at: [1255, 920], dir: 'y', through: true, why: 'north glazing to the first bedroom wall, across the open kitchen' },
    { room: 'kitchen', label: '373', value: 373, at: [1160, 1123], dir: 'x', why: 'kitchen run' },
    { room: 'bed1', label: '388', value: 388, at: [1180, 1340], dir: 'x', why: 'width' },
    { room: 'bed1', label: '268', value: 268, at: [1092, 1285], dir: 'y', why: 'depth, wardrobe wall to the next bedroom' },
    { room: 'bed2', label: '388', value: 388, at: [1180, 1408], dir: 'x', why: 'width' },
    { room: 'bed2', label: '278', value: 278, at: [1092, 1440], dir: 'y', why: 'depth' },
    { room: 'bed3', label: '333', value: 333, at: [1160, 1712], dir: 'x', why: 'width' },
    { room: 'bed3', label: '408', value: 408, at: [1110, 1700], dir: 'y', why: 'depth' },
    { room: 'master', label: '478', value: 478, at: [1430, 1810], dir: 'x', why: 'width including the wardrobe wall' },
    { room: 'master', label: '288', value: 288, at: [1350, 1690], dir: 'y', why: 'depth at the label, from the wall of the master door to the south glazing' },
  ],
  starter: [
    ['gen.sofa3', [1110, 720], 270], ['gen.rug', [1220, 720], 90], ['gen.plant', [1400, 640], 0],
    ['gen.dining6', [1140, 900], 0], ['gen.chair', [1100, 862], 0], ['gen.chair', [1180, 862], 0], ['gen.chair', [1100, 938], 180], ['gen.chair', [1180, 938], 180],
    ['gen.kitchen', [1140, 1147], 180], ['gen.island', [1140, 1035], 0],
    ['gen.bed160', [1090, 1265], 90], ['gen.bed160', [1090, 1453], 90], ['gen.bed160', [1100, 1680], 90],
    ['gen.bedset', [1460, 1740], 180], ['gen.wardrobe2', [1530, 1640], 270],
    ['gen.plant', [1300, 300], 0], ['gen.plant', [900, 1200], 0],
  ],
};

// ---------------------------------------------------------------- invented examples (labelled "דירה לדוגמה")
const EX_SRC = (n) => ({ kind: 'example', label_he: 'דירה לדוגמה', note: 'An invented ' + n + '-room layout of a typical Israeli new build, for the designer when a project has no plan. Not a plan of any project and not a sales plan.', date: '2026-11-11' });
const EX3 = {
  id: 'example-3r', rev: 'example-3r:2026-11-11:a', source: EX_SRC(3), unit: { project: null, unit_id: null, tower: null, floor: null, type: '3R', rooms: 3 }, north_deg: 0,
  walls: [
    { kind: 'facade', pts: [[0, 0], [560, 0], [1000, 0]] },
    { kind: 'facade', pts: [[1000, 0], [1000, 380]] },
    { kind: 'mamad', pts: [[1000, 380], [1000, 800], [700, 800], [700, 380], [1000, 380]] },
    { kind: 'structural', pts: [[700, 800], [0, 800]] },
    { kind: 'facade', pts: [[0, 800], [0, 0]] },
    { kind: 'partition', pts: [[560, 0], [560, 380], [700, 380]] },
    { kind: 'divider', pts: [[560, 380], [560, 480], [350, 480], [0, 480]] },
    { kind: 'divider', pts: [[350, 480], [350, 800]] },
    { kind: 'partition', pts: [[700, 520], [560, 520], [560, 800]] },
    { kind: 'rail', pts: [[0, 0], [0, -180], [560, -180], [560, 0]] },
  ],
  openings: [
    { id: 'o-slider', type: 'slider', near: [280, 0], w: 360 },
    { id: 'o-win-master', type: 'window', near: [780, 0], w: 200 },
    { id: 'o-win-living', type: 'window', near: [0, 240], w: 160 },
    { id: 'o-win-kitchen', type: 'window', near: [0, 640], w: 120, sill: 105 },
    { id: 'o-win-mamad', type: 'window', near: [1000, 590], w: 100, sill: 100, head: 200 },
    { id: 'o-entry', type: 'door', near: [430, 800], w: 100, into: [430, 700] },
    { id: 'o-door-master', type: 'door', near: [630, 380], w: 90, into: [630, 300] },
    { id: 'o-door-mamad', type: 'door', near: [700, 460], w: 80, into: [800, 460], head: 205 },
    { id: 'o-door-bath', type: 'door', near: [630, 520], w: 80, into: [630, 620] },
  ],
  rooms: [
    { id: 'living', type: 'living', name_he: 'סלון ופינת אוכל', at: [280, 240] },
    { id: 'kitchen', type: 'kitchen', name_he: 'מטבח', at: [170, 640] },
    { id: 'hall', type: 'hall', name_he: 'כניסה', at: [455, 640] },
    { id: 'master', type: 'bedroom', name_he: 'שינה הורים', at: [780, 190] },
    { id: 'mamad', type: 'mamad', name_he: 'ממ״ד', at: [850, 590] },
    { id: 'bath', type: 'wet', name_he: 'רחצה', at: [630, 660] },
    { id: 'balcony', type: 'balcony', name_he: 'מרפסת', at: [280, -90] },
  ],
  starter: [
    ['gen.tv', [35, 200], 270], ['gen.rug', [170, 200], 90], ['gen.sofa3', [320, 200], 90],
    ['gen.dining6', [480, 240], 90], ['gen.chair', [406, 200], 270], ['gen.chair', [406, 280], 270], ['gen.chair', [480, 121], 0], ['gen.chair', [480, 359], 180],
    ['gen.kitchen', [180.5, 757], 180], ['gen.island', [180, 600], 0],
    ['gen.bedset', [780, 115], 0], ['gen.wardrobe2', [850, 333], 180],
    ['gen.bed160', [880, 690], 270], ['gen.wardrobe2', [900, 428], 0],
    ['gen.plant', [520, -140], 0],
  ],
};
const EX5 = {
  id: 'example-5r', rev: 'example-5r:2026-11-11:a', source: EX_SRC(5), unit: { project: null, unit_id: null, tower: null, floor: null, type: '5R', rooms: 5 }, north_deg: 0,
  walls: [
    { kind: 'facade', pts: [[0, 0], [650, 0], [1050, 0], [1250, 0], [1600, 0]] },
    { kind: 'facade', pts: [[1600, 0], [1600, 430]] },
    { kind: 'structural', pts: [[1600, 430], [1600, 550]] },
    { kind: 'mamad', pts: [[1600, 550], [1600, 920], [1280, 920], [1280, 550], [1600, 550]] },
    { kind: 'structural', pts: [[1280, 920], [1000, 920], [820, 920], [650, 920], [400, 920], [0, 920]] },
    { kind: 'facade', pts: [[0, 920], [0, 0]] },
    { kind: 'partition', pts: [[650, 0], [650, 430]] },
    { kind: 'divider', pts: [[650, 430], [650, 550]] },
    { kind: 'divider', pts: [[0, 550], [650, 550]] },
    { kind: 'partition', pts: [[650, 430], [1250, 430], [1600, 430]] },
    { kind: 'partition', pts: [[1050, 0], [1050, 230], [1250, 230]] },
    { kind: 'partition', pts: [[1250, 0], [1250, 430]] },
    { kind: 'partition', pts: [[650, 550], [650, 920]] },
    { kind: 'partition', pts: [[650, 730], [400, 730], [400, 920]] },
    { kind: 'partition', pts: [[820, 920], [820, 550], [1280, 550]] },
    { kind: 'partition', pts: [[1000, 550], [1000, 920]] },
    { kind: 'divider', pts: [[650, 550], [820, 550]] },                   // entrance | corridor
    { kind: 'rail', pts: [[0, 0], [0, -220], [650, -220], [650, 0]] },
  ],
  openings: [
    { id: 'o-slider', type: 'slider', near: [325, 0], w: 400 },
    { id: 'o-win-master', type: 'window', near: [850, 0], w: 200 },
    { id: 'o-win-ens', type: 'window', near: [1150, 0], w: 60, sill: 150, head: 210 },
    { id: 'o-win-bed2', type: 'window', near: [1425, 0], w: 180 },
    { id: 'o-win-living', type: 'window', near: [0, 270], w: 200 },
    { id: 'o-win-kitchen', type: 'window', near: [0, 760], w: 120, sill: 105 },
    { id: 'o-win-mamad', type: 'window', near: [1600, 760], w: 100, sill: 100, head: 200 },
    { id: 'o-win-bed3', type: 'window', near: [1140, 920], w: 140 },
    { id: 'o-entry', type: 'door', near: [735, 920], w: 100, into: [735, 850] },
    { id: 'o-door-wc', type: 'door', near: [650, 820], w: 80, into: [550, 820] },
    { id: 'o-door-master', type: 'door', near: [725, 430], w: 90, into: [725, 350] },
    { id: 'o-door-ens', type: 'door', near: [1150, 230], w: 80, into: [1150, 120] },
    { id: 'o-door-bed2', type: 'door', near: [1315, 430], w: 90, into: [1315, 350] },
    { id: 'o-door-bath', type: 'door', near: [880, 550], w: 80, into: [880, 650] },
    { id: 'o-door-bed3', type: 'door', near: [1065, 550], w: 90, into: [1065, 650] },
    { id: 'o-door-mamad', type: 'door', near: [1340, 550], w: 80, into: [1340, 650], head: 205 },
  ],
  rooms: [
    { id: 'living', type: 'living', name_he: 'סלון ופינת אוכל', at: [325, 275] },
    { id: 'kitchen', type: 'kitchen', name_he: 'מטבח', at: [200, 740] },
    { id: 'wc', type: 'wet', name_he: 'שירותי אורחים', at: [525, 840] },
    { id: 'hall', type: 'hall', name_he: 'כניסה', at: [735, 750] },
    { id: 'corridor', type: 'hall', name_he: 'מסדרון', at: [1000, 490] },
    { id: 'master', type: 'bedroom', name_he: 'יחידת הורים', at: [850, 215] },
    { id: 'ens', type: 'wet', name_he: 'מקלחת הורים', at: [1150, 115] },
    { id: 'bed2', type: 'bedroom', name_he: 'חדר שינה', at: [1425, 215] },
    { id: 'bath', type: 'wet', name_he: 'רחצה', at: [910, 750] },
    { id: 'bed3', type: 'bedroom', name_he: 'חדר שינה', at: [1140, 750] },
    { id: 'mamad', type: 'mamad', name_he: 'ממ״ד', at: [1440, 750] },
    { id: 'balcony', type: 'balcony', name_he: 'מרפסת', at: [325, -110] },
  ],
  starter: [
    ['gen.sofa3', [330, 110], 0], ['gen.rug', [330, 250], 0], ['gen.tv', [330, 520], 180],
    ['gen.dining6', [130, 330], 90], ['gen.chair', [62, 290], 270], ['gen.chair', [62, 370], 270], ['gen.chair', [198, 290], 90], ['gen.chair', [198, 370], 90],
    ['gen.kitchen', [200, 877], 180], ['gen.island', [200, 700], 0],
    ['gen.bedset', [850, 115], 0], ['gen.wardrobe2', [1150, 383], 180],
    ['gen.bed160', [1425, 120], 0], ['gen.bed160', [1140, 805], 180], ['gen.wardrobe2', [1500, 600], 0],
    ['gen.plant', [600, -170], 0],
  ],
};

const out = [
  ['ashira/E-4A.json', E4A], ['ashira/E-3B.json', E3B], ['ashira/E-5E.json', E5E], ['ashira/E-5F.json', E5F],
  ['example-3r.json', EX3], ['example-5r.json', EX5],
];
const published = { note: 'Room sizes printed on the four published Ashira building E sales plans, and where each is measured on our redraw. studio_d is the size as the Plan Studio (docs/sales/ashira-meeting-2026-10/tour/studio/index.html, TYPES) recorded it. A probe is a dimension line: from the point, along dir both ways, to the first wall face (dividers are skipped when through_dividers is true, because the printed size runs across an open kitchen). Generated by build-plans.mjs.', plans: {} };
const STUDIO = {
  'ashira-e-4a': { living: '718×473', kitchen: '683', master: '513×270', bed1: '348×288', bed2: '373×313' },
  'ashira-e-3b': { living: '665×373', kitchen: '284', master: '428×278', bed1: '308×273' },
  'ashira-e-5e': { living: '573×493', kitchen: '333×273', master: '558×278', bed1: '313×288', bed2: '313×283', bed3: '292×273' },
  'ashira-e-5f': { living: '583×858', kitchen: '373', bed1: '388×268', bed2: '388×278', bed3: '333×408', master: '478×288' },
};
fs.mkdirSync(path.join(PLANS, 'ashira'), { recursive: true });
for (const [file, spec] of out) {
  const { apt, probes } = build(spec);
  fs.writeFileSync(path.join(PLANS, file), JSON.stringify(apt, null, 1) + '\n');
  if (probes.length) published.plans[apt.id] = { type: apt.unit.type, studio_d: STUDIO[apt.id], probes };
  console.log('wrote', file, Object.keys(apt.nodes).length, 'nodes', apt.walls.length, 'walls', apt.openings.length, 'openings', apt.starter.length, 'pieces');
}
fs.writeFileSync(path.join(here, 'plans-published.json'), JSON.stringify(published, null, 1) + '\n');
const index = {
  plans: [
    { id: 'example-3r', file: 'example-3r.json', project: null, type: '3R', rooms: 3, label_he: 'דירה לדוגמה', source_kind: 'example' },
    { id: 'example-4r', file: 'example-4r.json', project: null, type: '4R', rooms: 4, label_he: 'דירה לדוגמה', source_kind: 'example' },
    { id: 'example-5r', file: 'example-5r.json', project: null, type: '5R', rooms: 5, label_he: 'דירה לדוגמה', source_kind: 'example' },
    { id: 'ashira-e-4a', file: 'ashira/E-4A.json', project: 'ashira', type: 'E-4A', rooms: 4, label_he: 'לפי תוכנית המכר שפורסמה', source_kind: 'sales-plan' },
    { id: 'ashira-e-3b', file: 'ashira/E-3B.json', project: 'ashira', type: 'E-3B', rooms: 3, label_he: 'לפי תוכנית המכר שפורסמה', source_kind: 'sales-plan' },
    { id: 'ashira-e-5e', file: 'ashira/E-5E.json', project: 'ashira', type: 'E-5E', rooms: 5, label_he: 'לפי תוכנית המכר שפורסמה', source_kind: 'sales-plan' },
    { id: 'ashira-e-5f', file: 'ashira/E-5F.json', project: 'ashira', type: 'E-5F', rooms: 5, label_he: 'לפי תוכנית המכר שפורסמה', source_kind: 'sales-plan' },
  ],
  projects: { ashira: { types: ['E-4A', 'E-3B', 'E-5E', 'E-5F'], default: 'E-4A' } },
};
fs.writeFileSync(path.join(PLANS, 'index.json'), JSON.stringify(index, null, 1) + '\n');
console.log('wrote index.json and plans-published.json');
