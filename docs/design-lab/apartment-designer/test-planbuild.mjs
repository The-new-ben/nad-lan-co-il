// node docs/design-lab/apartment-designer/test-planbuild.mjs
// "My plan" builder without a browser: a traced draft becomes a nadlan-apartment v1 the engine accepts, with the right rooms and areas.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url)), lib = path.join(here, '../../../plugins/nadlan-config/assets/designer/');
const { buildPlan, checkDraft, analyzeDraft, cleanGraph, roomChoices, WALL_T, NOTE_HE } = await import(pathToFileURL(lib + 'planbuild.js'));
const { createStore, emptyDesign, quantities } = await import(pathToFileURL(lib + 'core.js'));
const schema = JSON.parse(fs.readFileSync(path.join(here, '../../architecture/apartment-designer/apartment.schema.json'), 'utf8'));

let pass = 0, fail = 0;
const check = (name, ok, detail) => { if (ok) pass++; else fail++; console.log((ok ? 'ok   ' : 'FAIL ') + name + (detail !== undefined && !ok ? '  ' + (typeof detail === 'string' ? detail : JSON.stringify(detail)) : '')); };
const S = (a, b, kind = 'partition') => ({ a, b, kind });
const F = (a, b) => S(a, b, 'facade');
const rect = (x0, y0, x1, y1, kind = 'facade') => [S([x0, y0], [x1, y0], kind), S([x1, y0], [x1, y1], kind), S([x1, y1], [x0, y1], kind), S([x0, y1], [x0, y0], kind)];
const store = (plan) => createStore(plan, emptyDesign(plan));
const rooms = (st) => st.derived.faces.filter((f) => f.room);
const near = (a, b, pct) => Math.abs(a - b) <= (Math.abs(b) * pct) / 100;
const axisAligned = (plan) => plan.walls.every((w) => { const a = plan.nodes[w.a], b = plan.nodes[w.b]; return a[0] === b[0] || a[1] === b[1]; });
const keyOf = (plan) => plan.walls.map((w) => [w.a, w.b].sort().join('-'));

// a minimal JSON-schema reader for the parts apartment.schema.json uses
function validate(s, v, at = '$', errs = []) {
  if (s.const !== undefined && v !== s.const) errs.push(at + ' const');
  if (s.enum && !s.enum.includes(v)) errs.push(at + ' enum ' + JSON.stringify(v));
  if (s.type) {
    const types = [].concat(s.type), t = v === null ? 'null' : Array.isArray(v) ? 'array' : Number.isInteger(v) ? 'integer' : typeof v;
    if (!types.some((x) => x === t || (x === 'number' && t === 'integer'))) { errs.push(at + ' type ' + t); return errs; }
  }
  if (typeof v === 'string' && s.pattern && !new RegExp(s.pattern).test(v)) errs.push(at + ' pattern');
  if (typeof v === 'string' && s.maxLength && v.length > s.maxLength) errs.push(at + ' maxLength');
  if (typeof v === 'number') { if (s.minimum != null && v < s.minimum) errs.push(at + ' minimum'); if (s.maximum != null && v > s.maximum) errs.push(at + ' maximum'); if (s.exclusiveMinimum != null && v <= s.exclusiveMinimum) errs.push(at + ' exclusiveMinimum'); }
  if (Array.isArray(v)) {
    if (s.minItems != null && v.length < s.minItems) errs.push(at + ' minItems');
    if (s.maxItems != null && v.length > s.maxItems) errs.push(at + ' maxItems');
    if (s.prefixItems) s.prefixItems.forEach((p, i) => validate(p, v[i], at + '[' + i + ']', errs));
    else if (s.items) v.forEach((x, i) => { if (s.items.oneOf) { if (s.items.oneOf.filter((o) => !validate(o, x).length).length !== 1) errs.push(at + '[' + i + '] oneOf'); } else validate(s.items, x, at + '[' + i + ']', errs); });
  } else if (v && typeof v === 'object') {
    for (const r of s.required || []) if (!(r in v)) errs.push(at + ' missing ' + r);
    if (s.minProperties != null && Object.keys(v).length < s.minProperties) errs.push(at + ' minProperties');
    for (const k in v) {
      if (s.properties && s.properties[k]) validate(s.properties[k], v[k], at + '.' + k, errs);
      else if (s.additionalProperties === false) errs.push(at + ' extra ' + k);
      else if (s.additionalProperties && typeof s.additionalProperties === 'object') validate(s.additionalProperties, v[k], at + '.' + k, errs);
    }
  }
  return errs;
}
const schemaErrs = (plan) => validate(schema, plan).filter((e) => e !== '$.source.kind enum "own"');

// ---- 1. a rectangle with inner walls: living room and two bedrooms, T junctions ----
const base = {
  mode: 'measure', cmPerPx: 1,
  segments: [...rect(0, 0, 1000, 800), S([600, 0], [600, 800]), S([600, 400], [1000, 400])],
  openings: [{ id: 'd1', p: [600, 200], w: 80, type: 'door' }, { id: 'd2', p: [600, 600], w: 80, type: 'door' }, { id: 'e', p: [300, 800], w: 100, type: 'entry' }, { id: 'w1', p: [800, 0], w: 120, type: 'window' }, { id: 's', p: [300, 0], w: 240, type: 'slider' }],
  rooms: [{ at: [300, 400], key: 'livkit' }, { at: [800, 200], key: 'master' }, { at: [800, 600], key: 'bedroom' }],
};
{
  const plan = buildPlan(base, { project: 'demo', date: '2026-11-11' });
  check('1 builds a nadlan-apartment v1', plan.schema === 'nadlan-apartment' && plan.v === 1);
  check('1 matches apartment.schema.json (except source.kind "own", which the schema does not list yet)', schemaErrs(plan).length === 0, schemaErrs(plan));
  check('1 T junctions split the walls: 8 corners, 10 walls', Object.keys(plan.nodes).length === 8 && plan.walls.length === 10, { n: Object.keys(plan.nodes).length, w: plan.walls.length });
  check('1 kinds and thicknesses: 7 facade pieces of 25, 3 inner pieces of 10', plan.walls.filter((w) => w.kind === 'facade' && w.t === 25).length === 7 && plan.walls.filter((w) => w.kind === 'partition' && w.t === 10).length === 3);
  check('1 origin at the top-left, whole centimetres', Math.min(...Object.values(plan.nodes).map((p) => p[0])) === 0 && Math.min(...Object.values(plan.nodes).map((p) => p[1])) === 0 && Object.values(plan.nodes).flat().every(Number.isInteger));
  let st, err = null; try { st = store(plan); } catch (e) { err = String(e); }
  check('1 createStore takes it without an exception', !!st && !err, err);
  const r = rooms(st), by = Object.fromEntries(r.map((f) => [f.room.name_he, f]));
  check('1 three rooms, named from the draft', r.length === 3 && by['סלון ומטבח'] && by['חדר שינה הורים'] && by['חדר שינה']);
  check('1 living area within 1% of the hand count (582.5 x 775)', near(by['סלון ומטבח'].net, (582.5 * 775) / 1e4, 1), by['סלון ומטבח'].net);
  check('1 bedroom areas within 1% of the hand count (382.5 x 382.5)', near(by['חדר שינה'].net, (382.5 * 382.5) / 1e4, 1) && near(by['חדר שינה הורים'].net, (382.5 * 382.5) / 1e4, 1));
  check('1 the bedroom is a true rectangle with a clear size', by['חדר שינה'].clearW === 383 || by['חדר שינה'].clearW === 382);
  check('1 the analysis shows the very areas the engine computes', (() => { const a = analyzeDraft(base); return a.faces.every((f) => r.some((g) => g.room.id === f.id && g.net === f.net)); })());
  check('1 five openings, each inside one wall piece', plan.openings.length === 5 && plan.openings.every((o) => { const w = plan.walls.find((x) => x.id === o.wall), a = plan.nodes[w.a], b = plan.nodes[w.b], L = Math.hypot(b[0] - a[0], b[1] - a[1]); return o.at >= 0 && o.at + o.w <= L; }));
  check('1 opening kinds map to the engine: door, door (front, 100), window, slider', plan.openings.filter((o) => o.type === 'door').length === 3 && plan.openings.some((o) => o.type === 'door' && o.w === 100) && plan.openings.some((o) => o.type === 'window' && o.sill === 95) && plan.openings.some((o) => o.type === 'slider' && o.w === 240));
  const top = plan.walls.filter((w) => plan.nodes[w.a][1] === 0 && plan.nodes[w.b][1] === 0);
  const ow = (id) => plan.openings.find((o) => o.wall === id);
  check('1 the top facade was split at the T, and the window and the slider sit on their own pieces', top.length === 2 && ow(top[0].id) && ow(top[1].id) && ow(top[0].id).id !== ow(top[1].id).id);
  const sl = plan.openings.find((o) => o.type === 'slider'), slw = plan.walls.find((w) => w.id === sl.wall), sa = plan.nodes[slw.a];
  check('1 the slider is centred where it was placed (x 300)', Math.abs((sa[0] < plan.nodes[slw.b][0] ? sa[0] + sl.at : sa[0] - sl.at - sl.w) + sl.w / 2 - 300) <= 1, sl);
  check('1 openings carry whole centimetres', plan.openings.every((o) => Number.isInteger(o.at) && Number.isInteger(o.w)));
  check('1 source, unit, levels, empty rules and starter', plan.source.kind === 'own' && plan.source.label_he === 'התוכנית שלי' && plan.source.note === NOTE_HE && plan.source.date === '2026-11-11' && plan.unit.type === 'OWN' && plan.unit.project === 'demo' && plan.unit.unit_id === null && plan.levels[0].height === 270 && plan.levels[0].slab === 25 && plan.rules.length === 0 && plan.starter.length === 0);
  check('1 room count: living + two bedrooms = 3', plan.unit.rooms === 3);
  check('1 every room point is inside exactly one space', plan.rooms.every((rm) => st.derived.faces.filter((f) => f.room && f.room.id === rm.id).length === 1));
  check('1 room ids follow the schema pattern and floors are known finishes', plan.rooms.every((rm) => /^[a-z0-9_-]{1,40}$/.test(rm.id) && ['porcelain-80', 'porcelain-60', 'deck'].includes(rm.floor)));
  const q = quantities(st);
  check('1 the bill of quantities works on it', q.rooms.length === 3 && q.net > 70 && q.net < 76, q.net);
  check('1 nothing to fix in the draft', checkDraft(base).length === 0, checkDraft(base));
  const again = buildPlan(JSON.parse(JSON.stringify(base)), { date: '2027-01-01' });
  check('1 id and revision come from the geometry: the same walls give the same id', again.id === plan.id && again.geometry_revision === plan.geometry_revision && /^own-[a-z0-9]+$/.test(plan.id));
  const moved = buildPlan({ ...base, segments: base.segments.map((s, i) => (i === 4 ? S([620, 0], [620, 800]) : s)) });
  check('1 other walls give another id and revision', moved.id !== plan.id && moved.geometry_revision !== plan.geometry_revision);
}

// ---- 2. the same plan traced off a photo turned by 7 degrees, in pixels (2 px per cm), with shaky ends ----
{
  const th = (7 * Math.PI) / 180, k = 0.5, jit = [[2, -3], [-3, 1], [1, 3], [-2, -2], [3, 2], [0, -3], [-1, 2], [2, 1]];
  let n = 0;
  const tf = (p) => { const j = jit[n++ % jit.length], x = p[0] + j[0], y = p[1] + j[1]; return [((x * Math.cos(th) - y * Math.sin(th)) / k) + 400, ((x * Math.sin(th) + y * Math.cos(th)) / k) + 90]; };
  const d = { mode: 'image', cmPerPx: k, segments: base.segments.map((s) => ({ ...s, a: tf(s.a), b: tf(s.b) })), openings: base.openings.map((o) => ({ ...o, p: tf(o.p) })), rooms: base.rooms.map((r) => ({ ...r, at: tf(r.at) })) };
  const a = analyzeDraft(d), plan = a.plan;
  check('2 the turned photo comes out straight: every wall horizontal or vertical', !!plan && axisAligned(plan));
  check('2 the axis found is 7 degrees', Math.abs((a.frame.th * 180) / Math.PI - 7) < 0.3, (a.frame.th * 180) / Math.PI);
  check('2 shaky ends (up to 3 cm) still close: same 8 corners and 10 walls, no free end', Object.keys(plan.nodes).length === 8 && plan.walls.length === 10 && !a.problems.length, a.problems);
  const st = store(plan), r = rooms(st), b0 = rooms(store(buildPlan(base)));
  check('2 shaky: three rooms, each within 3% of the straight plan (the ends moved up to 3 cm)', r.length === 3 && r.every((f) => { const g = b0.find((x) => x.room.name_he === f.room.name_he); return g && near(f.net, g.net, 3); }), r.map((f) => [f.room.name_he, f.net]));
  check('2 the openings survive the turn', plan.openings.length === 5);
  const back = a.frame.toDraft(a.frame.toPlan(d.rooms[0].at));
  check('2 the frame maps the plan back onto the photo', Math.hypot(back[0] - d.rooms[0].at[0], back[1] - d.rooms[0].at[1]) < 1e-6);
  // the same turn with clean ends: the very sizes of the straight plan
  const tc = (p) => [((p[0] * Math.cos(th) - p[1] * Math.sin(th)) / k) + 400, ((p[0] * Math.sin(th) + p[1] * Math.cos(th)) / k) + 90];
  const dc = { mode: 'image', cmPerPx: k, segments: base.segments.map((s) => ({ ...s, a: tc(s.a), b: tc(s.b) })), openings: base.openings.map((o) => ({ ...o, p: tc(o.p) })), rooms: base.rooms.map((x) => ({ ...x, at: tc(x.at) })) };
  const pc = buildPlan(dc), rc = rooms(store(pc));
  check('2 clean turn: the outer size is 1000 x 800 within 1 cm', (() => { const xs = Object.values(pc.nodes).map((p) => p[0]), ys = Object.values(pc.nodes).map((p) => p[1]); return Math.abs(Math.max(...xs) - 1000) <= 1 && Math.abs(Math.max(...ys) - 800) <= 1; })());
  check('2 clean turn: every room within 1% of the straight plan', rc.length === 3 && rc.every((f) => { const g = b0.find((x) => x.room.name_he === f.room.name_he); return g && near(f.net, g.net, 1); }), rc.map((f) => [f.room.name_he, f.net]));
}

// ---- 3. snapping and overlaps: two rooms drawn side by side, the shared wall drawn twice and longer once ----
{
  const d = { mode: 'measure', cmPerPx: 1, segments: [...rect(0, 0, 400, 300, 'partition'), ...rect(403, -2, 700, 300, 'partition'), S([400, 300], [400, 500]), S([0, 300], [0, 500], 'facade'), S([0, 500], [400, 500], 'facade')], rooms: [{ at: [200, 150], key: 'bedroom' }, { at: [550, 150], key: 'study' }, { at: [200, 400], key: 'bath' }] };
  const a = analyzeDraft(d), plan = a.plan, keys = keyOf(plan);
  check('3 ends within 8 cm snap together (403 -> 400, -2 -> 0)', Object.values(plan.nodes).every((p) => [0, 400, 700].includes(p[0]) && [0, 300, 500].includes(p[1])), plan.nodes);
  check('3 the wall drawn twice is one wall', new Set(keys).size === keys.length && plan.walls.filter((w) => { const A = plan.nodes[w.a], B = plan.nodes[w.b]; return A[0] === 400 && B[0] === 400; }).length === 2);
  check('3 the stronger kind wins where two kinds overlap', plan.walls.filter((w) => { const A = plan.nodes[w.a], B = plan.nodes[w.b]; return A[0] === 0 && B[0] === 0; }).every((w) => w.kind === 'facade' || plan.nodes[w.a][1] < 300 || plan.nodes[w.b][1] < 300));
  const r = rooms(store(plan));
  check('3 three rooms: bedroom, study, bath', r.length === 3 && ['חדר שינה', 'חדר עבודה', 'חדר רחצה'].every((n) => r.some((f) => f.room.name_he === n)));
  check('3 a bathroom gets the wet-room floor', plan.rooms.find((x) => x.type === 'wet').floor === 'porcelain-60');
  check('3 the study counts as a room', plan.unit.rooms === 2);
}

// ---- 4. an L-shaped room against a hand count ----
{
  const L = [[0, 0], [600, 0], [600, 300], [300, 300], [300, 600], [0, 600]];
  const d = { mode: 'measure', cmPerPx: 1, segments: L.map((p, i) => F(p, L[(i + 1) % L.length])), rooms: [{ at: [150, 150], key: 'living' }] };
  const plan = buildPlan(d), f = rooms(store(plan))[0];
  // clear inside: the L inset by 12.5 cm: (600-25)x(300-25) + (300-25)x(300) ... counted as a polygon
  const P = [[12.5, 12.5], [587.5, 12.5], [587.5, 287.5], [287.5, 287.5], [287.5, 587.5], [12.5, 587.5]];
  let A = 0; for (let i = 0; i < P.length; i++) { const p = P[i], q = P[(i + 1) % P.length]; A += p[0] * q[1] - q[0] * p[1]; }
  check('4 L-shaped room: one space within 1% of the hand count', !!f && near(f.net, Math.abs(A) / 2 / 1e4, 1), { net: f && f.net, hand: Math.abs(A) / 2 / 1e4 });
  check('4 an L has no clear width (it is not a rectangle)', f.clearW === null);
  check('4 the label point stands in the wide part, inside the room', f.room.at[0] > 0 && f.room.at[1] > 0 && (f.room.at[0] < 300 || f.room.at[1] < 300));
}

// ---- 5. crossings: two inner walls through each other make four rooms ----
{
  const d = { mode: 'measure', cmPerPx: 1, segments: [...rect(0, 0, 800, 800), S([400, 0], [400, 800]), S([0, 400], [800, 400])], rooms: [] };
  const a = analyzeDraft(d), plan = a.plan;
  check('5 a crossing becomes a corner: 9 corners, 12 walls', Object.keys(plan.nodes).length === 9 && plan.walls.length === 12);
  check('5 four rooms, all unnamed, and the draft says so', rooms(store(plan)).length === 4 && a.problems.some((p) => p.code === 'room.noname' && p.n === 4));
  check('5 an unnamed room still opens, called "חדר" of kind other', plan.rooms.every((r) => r.name_he === 'חדר' && r.type === 'other'));
}

// ---- 6. a doorway with no door, a safe room, an opening wider than its wall ----
{
  const d = {
    mode: 'measure', cmPerPx: 1, segments: [...rect(0, 0, 800, 500), S([500, 0], [500, 500]), S([500, 250], [800, 250])],
    openings: [{ id: 'g', p: [500, 120], w: 90, type: 'open' }, { id: 'd', p: [650, 250], w: 80, type: 'door' }, { id: 'big', p: [650, 500], w: 500, type: 'window' }],
    rooms: [{ at: [250, 250], key: 'living' }, { at: [650, 120], key: 'hall' }, { at: [650, 400], key: 'mamad' }],
  };
  const a = analyzeDraft(d), plan = a.plan, st = store(plan);
  check('6 a doorway with no door is a stretch of open line (divider), not an engine opening', plan.walls.filter((w) => w.kind === 'divider').length === 1 && !plan.openings.some((o) => o.type !== 'door' && o.type !== 'window' && o.type !== 'slider'));
  const dv = plan.walls.find((w) => w.kind === 'divider'), A = plan.nodes[dv.a], B = plan.nodes[dv.b];
  check('6 the open stretch is 90 cm, centred at y 120', Math.hypot(B[0] - A[0], B[1] - A[1]) === 90 && Math.abs((A[1] + B[1]) / 2 - 120) <= 1);
  check('6 the rooms on both sides of the open stretch stay two rooms', rooms(st).length === 3);
  const mm = st.derived.faces.find((f) => f.room && f.room.type === 'mamad');
  check('6 the safe room\'s walls become safe-room walls of 30 cm', mm && mm.walls.every((id) => { const w = plan.walls.find((x) => x.id === id); return w.kind === 'mamad' && w.t === 30; }), mm && mm.walls);
  check('6 a safe-room wall cannot be moved in the designer', mm.walls.every((id) => !st.slides(id)));
  check('6 an opening wider than its wall is shortened and reported', a.problems.some((p) => p.code === 'opening.wide') && plan.openings.every((o) => { const w = plan.walls.find((x) => x.id === o.wall), p = plan.nodes[w.a], q = plan.nodes[w.b]; return o.at + o.w <= Math.hypot(q[0] - p[0], q[1] - p[1]); }));
  check('6 the door on the inner wall stays a door', plan.openings.some((o) => o.type === 'door' && o.swing === 1));
  check('6 the safe room counts as a room', plan.unit.rooms === 2);
}

// ---- 7. what checkDraft reports ----
{
  check('7 an empty draft: no walls', checkDraft({ segments: [] })[0].code === 'no.walls');
  const open = { cmPerPx: 1, segments: [F([0, 0], [500, 0]), F([500, 0], [500, 400]), F([500, 400], [0, 400])] };
  const p1 = checkDraft(open);
  check('7 three sides only: a wall not closed and no room', p1.some((p) => p.code === 'open.end' && p.n === 2) && p1.some((p) => p.code === 'no.room'));
  let threw = null; try { buildPlan(open); } catch (e) { threw = e.code; }
  check('7 buildPlan refuses a draft with no closed room', threw === 'no.room');
  const apart = { cmPerPx: 1, segments: [...rect(0, 0, 500, 400), ...rect(900, 0, 1000, 100)], rooms: [{ at: [250, 200], key: 'living' }] };
  const a = analyzeDraft(apart);
  check('7 a drawing in two separate pieces keeps the big one and says so', a.problems.some((p) => p.code === 'apart') && rooms(store(a.plan)).length === 1);
  const off = { ...base, openings: [{ id: 'x', p: [300, 300], w: 80, type: 'door' }] };
  check('7 an opening away from every wall is left out and reported', analyzeDraft(off).problems.some((p) => p.code === 'opening.off') && analyzeDraft(off).plan.openings.length === 0);
  const clash = { ...base, openings: [{ id: 'a', p: [800, 0], w: 120, type: 'window' }, { id: 'b', p: [850, 0], w: 120, type: 'window' }] };
  check('7 two openings on the same stretch: one kept, reported', analyzeDraft(clash).plan.openings.length === 1 && checkDraft(clash).some((p) => p.code === 'opening.overlap'));
}

// ---- 8. a whole floor: two flats and the stair hall, the hall marked "not part of the apartment" ----
{
  const d = { cmPerPx: 1, segments: [...rect(0, 0, 1600, 900), S([700, 0], [700, 900]), S([900, 0], [900, 900])], rooms: [{ at: [300, 400], key: 'living' }, { at: [800, 400], key: 'out' }, { at: [1200, 400], key: 'bedroom' }] };
  const plan = buildPlan(d), r = rooms(store(plan));
  check('8 the space marked "not part of the apartment" is left out of the rooms', r.length === 2 && plan.rooms.length === 2 && !plan.rooms.some((x) => x.type === 'out'));
}

// ---- 9. the two draft forms (loose segments, or corners and walls) give the same apartment ----
{
  const nodes = { a: [0, 0], b: [500, 0], c: [500, 400], d: [0, 400] };
  const d1 = { cmPerPx: 1, nodes, segs: [{ id: 's1', a: 'a', b: 'b', kind: 'facade' }, { id: 's2', a: 'b', b: 'c', kind: 'facade' }, { id: 's3', a: 'c', b: 'd', kind: 'facade' }, { id: 's4', a: 'd', b: 'a', kind: 'facade' }], rooms: [{ at: [250, 200], key: 'bedroom' }] };
  const d2 = { cmPerPx: 1, segments: rect(0, 0, 500, 400), rooms: [{ at: [250, 200], key: 'bedroom' }] };
  check('9 corners-and-walls form and loose-segments form give the same id', buildPlan(d1).id === buildPlan(d2).id);
  const g = cleanGraph([[0, 0], [10, 0], [5, -5], [5, 5]], [{ a: 0, b: 1, kind: 'partition' }, { a: 2, b: 3, kind: 'partition' }], 0.5);
  check('9 cleanGraph splits two crossing walls into four', g.segs.length === 4 && g.pts.length === 5);
  check('9 the names list holds every engine space name plus the main room kinds', ['חדר שינה', 'חדר עבודה', 'חדר ארונות', 'מחסן', 'פינת משפחה', 'סלון', 'מטבח', 'ממ״ד', 'מרפסת'].every((n) => roomChoices('he').some((c) => c.name_he === n)) && roomChoices('en').every((c) => c.label && !/[֐-׿]/.test(c.label)));
  check('9 wall thicknesses: outer 25, inner 10, rail 8, open line 0', WALL_T.facade === 25 && WALL_T.partition === 10 && WALL_T.rail === 8 && WALL_T.divider === 0);
}

// ---- 10. a balcony with a rail; the 3-room test plan the browser check draws ----
{
  const d = { cmPerPx: 1, segments: [...rect(0, 0, 900, 600), S([500, 0], [500, 600]), S([500, 300], [900, 300]), S([0, 600], [0, 760], 'rail'), S([0, 760], [500, 760], 'rail'), S([500, 760], [500, 600], 'rail')], rooms: [{ at: [250, 300], key: 'living' }, { at: [700, 150], key: 'bedroom' }, { at: [700, 450], key: 'master' }, { at: [250, 680], key: 'balcony' }] };
  const plan = buildPlan(d), st = store(plan), q = quantities(st);
  check('10 a balcony closed by a rail is a balcony space with the deck floor', plan.rooms.some((r) => r.type === 'balcony' && r.floor === 'deck') && q.balcony >= 6.9 && q.balcony <= 7.2, q.balcony);
  check('10 three rooms inside + the balcony; inside area within 1% of 27.74 + 2 x 10.81', near(q.net, 27.74 + 2 * 10.81, 1), q.net);
}

// ---- 11. sizes between the wall faces (what a tape measures and what a sales plan prints) ----
{
  const { innerLengths } = await import(pathToFileURL(lib + 'planbuild.js'));
  const G = (pts, walls) => ({ nodes: Object.fromEntries(pts.map((p, i) => ['n' + i, p])), segs: walls.map(([a, b, kind], i) => ({ id: 's' + i, a: 'n' + a, b: 'n' + b, kind })) });
  // a room typed as 400 x 300 inside, with 10 cm inner walls: its centre lines are 410 x 310
  const one = G([[0, 0], [410, 0], [410, 310], [0, 310]], [[0, 1, 'partition'], [1, 2, 'partition'], [2, 3, 'partition'], [3, 0, 'partition']]);
  const L1 = innerLengths(one.nodes, one.segs, 1);
  check('11 a typed 400 x 300 room reads 400 and 300 on its walls', Math.round(L1.s0.inner) === 400 && Math.round(L1.s1.inner) === 300 && Math.round(L1.s2.inner) === 400 && Math.round(L1.s3.inner) === 300, L1);
  // two typed rooms side by side (300 x 300 to the left), one shared wall
  const two = G([[0, 0], [410, 0], [410, 310], [0, 310], [-310, 0], [-310, 310]], [[0, 1, 'partition'], [1, 2, 'partition'], [2, 3, 'partition'], [3, 0, 'partition'], [4, 0, 'partition'], [5, 4, 'partition'], [3, 5, 'partition']]);
  const L2 = innerLengths(two.nodes, two.segs, 1);
  check('11 two rooms side by side: 400 and 300 for the first, 300 and 300 for the second, 300 on the shared wall', Math.round(L2.s0.inner) === 400 && Math.round(L2.s4.inner) === 300 && Math.round(L2.s5.inner) === 300 && Math.round(L2.s6.inner) === 300 && Math.round(L2.s3.inner) === 300, L2);
  // outer wall 25 against inner wall 10: the 1000 x 800 plan of section 1
  const fp = G([[0, 0], [600, 0], [1000, 0], [1000, 800], [600, 800], [0, 800]], [[0, 1, 'facade'], [1, 2, 'facade'], [2, 3, 'facade'], [3, 4, 'facade'], [4, 5, 'facade'], [5, 0, 'facade'], [1, 4, 'partition']]);
  const L3 = innerLengths(fp.nodes, fp.segs, 1);
  check('11 outer 25 against inner 10: 582.5 along the top, 775 down the side and along the inner wall', Math.abs(L3.s0.inner - 582.5) < 0.01 && Math.abs(L3.s5.inner - 775) < 0.01 && Math.abs(L3.s6.inner - 775) < 0.01 && Math.abs(L3.s1.inner - 382.5) < 0.01, L3);
  check('11 the same sizes in picture units (cm per pixel 0.5)', (() => { const px = G(Object.values(fp.nodes).map((p) => [p[0] * 2, p[1] * 2]), [[0, 1, 'facade'], [1, 2, 'facade'], [2, 3, 'facade'], [3, 4, 'facade'], [4, 5, 'facade'], [5, 0, 'facade'], [1, 4, 'partition']]); return Math.abs(innerLengths(px.nodes, px.segs, 0.5).s0.inner - 582.5) < 0.01; })());
}

// ---- 12. inner walls on the outline become outer walls, without moving or thinning ----
{
  const d = { cmPerPx: 1, segments: [...rect(0, 0, 410, 310, 'partition'), ...rect(-310, 0, 0, 310, 'partition')], rooms: [{ at: [200, 150], key: 'bedroom' }, { at: [-150, 150], key: 'study' }] };
  const plan = buildPlan(d), shared = plan.walls.filter((w) => plan.nodes[w.a][0] === 310 && plan.nodes[w.b][0] === 310);
  check('12 two typed rooms: every outline wall is an outer wall, the shared wall stays an inner wall', shared.length === 1 && shared[0].kind === 'partition' && plan.walls.filter((w) => w !== shared[0]).every((w) => w.kind === 'facade'), plan.walls.map((w) => w.kind));
  check('12 the outline walls keep their 10 cm', plan.walls.every((w) => w.t === 10));
  const r = rooms(store(plan)).map((f) => f.net).sort((a, b) => a - b);
  check('12 the areas do not change: 9.0 and 12.0 m2', Math.abs(r[0] - 9) <= 0.09 && Math.abs(r[1] - 12) <= 0.12, r);
  const st = store(plan);
  check('12 an outline wall cannot be moved in the designer; the shared wall is still an inner wall', plan.walls.filter((w) => w.kind === 'facade').every((w) => !st.slides(w.id)));
  const b = buildPlan({ ...d, segments: [...d.segments, S([0, 310], [0, 420], 'rail'), S([0, 420], [410, 420], 'rail'), S([410, 420], [410, 310], 'rail')], rooms: [...d.rooms, { at: [200, 370], key: 'balcony' }] });
  check('12 rails stay rails; the wall between a room and its balcony stays an inner wall', b.walls.filter((w) => w.kind === 'rail').length === 3 && b.walls.some((w) => w.kind === 'partition' && plan.nodes && b.nodes[w.a][1] === 310 && b.nodes[w.b][1] === 310 && Math.min(b.nodes[w.a][0], b.nodes[w.b][0]) === 310));
}

// ---- 13. counting tiles instead of a tape ----
{
  const { tileLength } = await import(pathToFileURL(lib + 'planbuild.js'));
  check('13 tile 60 with a 0.3 joint: 6.5 tiles = 6.5 x 60.3 = 392 cm', tileLength(6.5, 60) === Math.round(6.5 * 60.3) && tileLength(6.5, 60) === 392);
  check('13 tile 80: 5 tiles = 401.5 -> 402 (rounded); 33 x 12 = 399.6 -> 400', tileLength(5, 80) === 402 && tileLength(12, 33) === 400);
  check('13 half tiles count as halves; nothing counted gives 0', tileLength(0.5, 120) === 60 && tileLength(0, 60) === 0 && tileLength(3, 0) === 0);
}

// ---- 14. the contract area, and setting the scale from it (picture route) ----
{
  const { contractArea, calibrateScale } = await import(pathToFileURL(lib + 'planbuild.js'));
  const plan = buildPlan(base), ca = contractArea(plan);
  check('14 contract area of the 1000 x 800 plan with 25 cm outer walls: 1025 x 825 = 84.56 m2', Math.abs(ca - 84.5625) < 0.01, ca);
  const L = buildPlan({ cmPerPx: 1, segments: [[0, 0], [600, 0], [600, 300], [300, 300], [300, 600], [0, 600]].map((p, i, a) => F(p, a[(i + 1) % a.length])), rooms: [{ at: [150, 150], key: 'living' }] });
  check('14 an L: the outer outline (625 x 325 + 325 x 300) = 30.06 m2', Math.abs(contractArea(L) - (625 * 325 + 325 * 300) / 1e4) < 0.01, contractArea(L));
  const bal = buildPlan({ cmPerPx: 1, segments: [...rect(0, 0, 900, 600), S([0, 600], [0, 760], 'rail'), S([0, 760], [500, 760], 'rail'), S([500, 760], [500, 600], 'rail')], rooms: [{ at: [450, 300], key: 'living' }, { at: [250, 680], key: 'balcony' }] });
  check('14 a balcony is not in the contract area (925 x 625)', Math.abs(contractArea(bal) - 925 * 625 / 1e4) < 0.01, contractArea(bal));
  // the same plan traced off a picture at 2 px per cm, but the scale was marked 4% wrong
  const px = { cmPerPx: 0.52, segments: base.segments.map((s) => ({ ...s, a: [s.a[0] * 2, s.a[1] * 2], b: [s.b[0] * 2, s.b[1] * 2] })), openings: [], rooms: base.rooms.map((r) => ({ ...r, at: [r.at[0] * 2, r.at[1] * 2] })) };
  const c = calibrateScale(px, 84.5625);
  check('14 from the contract area the scale comes back to 0.5 cm per pixel (within 0.3%)', c.ok && Math.abs(c.k - 0.5) / 0.5 < 0.003 && Math.abs(c.after - 84.5625) < 0.05, c);
  check('14 the correction is reported in percent (about -3.8%)', c.pct < -3.5 && c.pct > -4.2, c.pct);
  const far = calibrateScale(px, 50);
  check('14 a correction over 15% is refused and nothing is given to apply', !far.ok && far.code === 'too.big', far);
}

// ---- 15. a page photographed at an angle: its proportions come back ----
{
  const { rectifySize } = await import(pathToFileURL(lib + 'planbuild.js'));
  const shoot = (Wp, Hp, ax, ay, f, cx, cy, D) => { // a pinhole camera looking at a tilted page
    const a = (ax * Math.PI) / 180, b = (ay * Math.PI) / 180;
    return [[-Wp / 2, -Hp / 2], [Wp / 2, -Hp / 2], [Wp / 2, Hp / 2], [-Wp / 2, Hp / 2]].map(([x, y]) => {
      let Y = y * Math.cos(a), Z = y * Math.sin(a), X = x;
      const X2 = X * Math.cos(b) + Z * Math.sin(b), Z2 = -X * Math.sin(b) + Z * Math.cos(b);
      return [cx + (f * X2) / (Z2 + D), cy + (f * Y) / (Z2 + D)];
    });
  };
  for (const [ax, ay] of [[25, 10], [-30, 0], [15, -20]]) {
    const r = rectifySize(shoot(1230, 900, ax, ay, 1400, 800, 600, 2200), 800, 600);
    const tol = r.how === 'camera' ? 0.005 : 0.02; // one-axis tilt: the lens is a usual phone lens, not measured
    check('15 tilted ' + ax + '/' + ay + ' degrees: the proportions 1230:900 come back (' + r.how + ', within ' + tol * 100 + '%)', r.how.startsWith('camera') && Math.abs(r.aspect / (1230 / 900) - 1) < tol, r);
  }
  const flat = rectifySize([[100, 100], [1330, 100], [1330, 1000], [100, 1000]], 700, 550);
  check('15 a page shot straight on keeps its sides', Math.abs(flat.W - 1230) < 1e-6 && Math.abs(flat.H - 900) < 1e-6);
}

console.log('\n' + pass + ' passed, ' + fail + ' failed');
process.exit(fail ? 1 : 0);
