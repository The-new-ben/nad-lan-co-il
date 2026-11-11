// node docs/design-lab/apartment-designer/test-core.mjs
// The designer core without a browser: services points, added and removed partitions, room names, their rules, undo, budget, speed.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url)), lib = path.join(here, '../../../plugins/nadlan-config/assets/designer/');
const { createStore, derive, emptyDesign, quantities, faceAt, interior, WALL_KINDS } = await import(pathToFileURL(lib + 'core.js'));
const { estimate } = await import(pathToFileURL(lib + 'budget.js'));
const catalog = await import(pathToFileURL(lib + 'catalog.js'));
const { STRINGS } = await import(pathToFileURL(lib + 'strings.js'));
const apt = JSON.parse(fs.readFileSync(lib + 'plans/example-4r.json', 'utf8'));
const prices = JSON.parse(fs.readFileSync(lib + 'data/price-ranges.json', 'utf8')).items;
const RULE = STRINGS.he.rules;

let pass = 0, fail = 0;
const check = (name, ok, detail) => { if (ok) pass++; else fail++; console.log((ok ? 'ok   ' : 'FAIL ') + name + (detail !== undefined ? '  ' + (typeof detail === 'string' ? detail : JSON.stringify(detail)) : '')); };
const S = () => { const d = emptyDesign(apt); d.items = catalog.STARTER.map((i) => ({ ...i })); return createStore(apt, d); }; // with the starter furniture, as the page opens it
const snap = (s) => JSON.stringify({ g: s.design.geometry, p: s.design.points, i: s.design.items, f: s.design.finishes }); // the design without rev and log
const near = (a, b, e = 0.05) => Math.abs(a - b) <= e;
const area = (s) => Object.fromEntries(s.derived.faces.filter((f) => f.room).map((f) => [f.id, f.net]));
const refused = (r, code) => !r.ok && r.code === code && r.reason === RULE[code];
const LIVING_CUT = { id: 'np1', a: [0, 300], b: [620, 300] }; // across the living room, from the west facade to the structural wall c1

// ---- the base specification ----
{
  const s = S(), dv = s.derived;
  check('29 base points are derived, every one of them valid', dv.points.length === 29 && dv.points.every((p) => p.state === 'base' && !p.bad), dv.points.filter((p) => p.bad).map((p) => p.id));
  const wrong = dv.points.filter((p) => p.kind !== 'light' && (faceAt(dv, [p.fx + p.ns[0] * 6, p.fy + p.ns[1] * 6]) || {}).id !== p.room).map((p) => p.id);
  check('every wall point sits on the face of its own room', wrong.length === 0, wrong);
  check('every light is inside the room it lights', dv.points.filter((p) => p.kind === 'light').every((p) => p.room && dv.faceBy[p.room]));
  const sp = dv.pointBy['sw-hall'];
  check('a wall point gets its height by kind (switch 110, socket 30, ac 220)', sp.h === 110 && dv.pointBy['s-liv-1'].h === 30 && dv.pointBy['ac-liv'].h === 220);
  check('a wall point is placed on its wall: sw-hall at x 425 on s3 (y 900), on the hall side', near(sp.x, 425) && near(sp.y, 900) && sp.fy < 900);
}
// ---- a stored design from before points and partitions ----
{
  const old = emptyDesign(apt); delete old.points; old.geometry = { walls: { p6: 20 } };
  let s, err = null;
  try { s = createStore(apt, old); } catch (e) { err = String(e); }
  check('a stored design without points and partitions still loads', !err && s.design.points.added.length === 0 && Array.isArray(s.design.geometry.added) && s.derived.points.length === 29, err);
  const s2 = S(); s2.load(old);
  check('…and the same through load() (the late joiner of a call)', s2.design.geometry.walls.p6 === 20 && s2.derived.points.length === 29 && s2.design.geometry.removed.length === 0);
}
// ---- point.add and its rules ----
{
  const s = S(), z = snap(s);
  const r = s.apply({ op: 'point.add', point: { id: 'pa1', kind: 'socket', wall: 'w2', at: 300, room: 'living' } });
  const p = s.point('pa1');
  check('point.add: a new socket on the west wall of the living room', r.ok && p.state === 'added' && near(p.x, 0) && near(p.y, 220) && p.side && p.fx > 0, p);
  const z1 = snap(s); s.undo();
  check('point.add undo leaves the design byte-identical', snap(s) === z && !s.point('pa1'));
  s.redo();
  check('point.add redo gives the same design again', snap(s) === z1);
  const add = (pt) => s.apply({ op: 'point.add', point: { id: 'px' + Math.random().toString(36).slice(2, 7), ...pt } });
  check('rule: no point on the balcony rail', refused(add({ kind: 'socket', wall: 'r2', at: 200, room: 'balcony' }), 'point.rail'));
  check('rule: no point on a divider between open spaces', refused(add({ kind: 'socket', wall: 'v2', at: 200, room: 'kitchen' }), 'point.divider'));
  check('rule: no point within 5 cm of a wall end', refused(add({ kind: 'socket', wall: 'w2', at: 3, room: 'living' }), 'point.end') && refused(add({ kind: 'socket', wall: 'w2', at: 517, room: 'living' }), 'point.end'));
  check('rule: no point in a door opening (s3, door 80 to 180)', refused(add({ kind: 'switch', wall: 's3', at: 100, room: 'hall' }), 'point.door') && refused(add({ kind: 'switch', wall: 's3', at: 183, room: 'hall' }), 'point.door'));
  check('rule: no point in a window (f2, window 110 to 270)', refused(add({ kind: 'socket', wall: 'f2', at: 150, room: 'master' }), 'point.window'));
  const m = add({ kind: 'socket', wall: 'm4', at: 100, room: 'bath' });
  check('rule: a NEW point on a safe-room wall is refused with the approved-detail sentence', refused(m, 'point.mamad') && m.reason.includes('ממ״ד') && m.reason.includes('פרט מאושר'), m.reason);
  check('rule: a light must be inside a room', refused(add({ kind: 'light', x: -300, y: 400 }), 'point.outside'));
  check('rule: a new light in the safe room is refused too (its ceiling)', refused(add({ kind: 'light', x: 1100, y: 800 }), 'point.mamad'));
  check('a light inside the living room is placed', add({ kind: 'light', x: 200, y: 400 }).ok);
  check('rule: a point id is used once', refused(s.apply({ op: 'point.add', point: { id: 'pa1', kind: 'socket', wall: 'w2', at: 400, room: 'living' } }), 'point.exists'));
  check('rule: an unknown kind is refused', refused(s.apply({ op: 'point.add', point: { id: 'pz', kind: 'gas', wall: 'w2', at: 400 } }), 'point.kind'));
}
// ---- point.move, point.remove, point.restore ----
{
  const s = S(), z = snap(s);
  let r = s.apply({ op: 'point.move', id: 's-liv-1', wall: 'w2', at: 140, room: 'living' });
  check('point.move: a base socket moves along its wall and is marked moved', r.ok && s.point('s-liv-1').state === 'moved' && near(s.point('s-liv-1').y, 380));
  r = s.apply({ op: 'point.move', id: 's-liv-1', wall: 's4', at: 330, room: 'kitchen' });
  check('point.move: onto another wall', r.ok && s.point('s-liv-1').wall === 's4' && near(s.point('s-liv-1').x, 30));
  s.undo(); s.undo();
  check('point.move undo twice leaves the design byte-identical', snap(s) === z);
  s.apply({ op: 'point.move', id: 's-liv-1', wall: 'w2', at: 140, room: 'living' });
  s.apply({ op: 'point.move', id: 's-liv-1', wall: 'w2', at: 80, room: 'living' });
  check('a point moved back onto its place is base again (nothing stored)', s.point('s-liv-1').state === 'base' && !('s-liv-1' in s.design.points.moved));
  check('rule: a base point on the safe-room wall cannot be moved along it', refused(s.apply({ op: 'point.move', id: 's-mmd', wall: 'm2', at: 100, room: 'mamad' }), 'point.mamad'));
  const s2 = S(), z2 = snap(s2);
  s2.apply({ op: 'point.move', id: 'tv-liv', wall: 'c1', at: 120, room: 'living' });
  const zm = snap(s2);
  r = s2.apply({ op: 'point.remove', id: 'tv-liv' });
  check('point.remove: a base point goes to removed (and its move is forgotten)', r.ok && s2.point('tv-liv').state === 'removed' && s2.design.points.removed.includes('tv-liv') && !s2.design.points.moved['tv-liv']);
  check('rule: a removed point cannot be removed or moved again', refused(s2.apply({ op: 'point.remove', id: 'tv-liv' }), 'point.gone') && refused(s2.apply({ op: 'point.move', id: 'tv-liv', wall: 'c1', at: 150, room: 'living' }), 'point.gone'));
  s2.undo();
  check('point.remove undo brings back the MOVED point exactly', snap(s2) === zm && s2.point('tv-liv').state === 'moved');
  r = s2.apply({ op: 'point.restore', id: 'tv-liv' });
  check('point.restore: a moved base point returns to the specification', r.ok && s2.point('tv-liv').state === 'base');
  s2.undo(); s2.undo();
  check('point.restore and move undone: byte-identical to the start', snap(s2) === z2);
  s2.apply({ op: 'point.add', point: { id: 'pa2', kind: 'data', wall: 'w2', at: 300, room: 'living' } });
  check('rule: only a point of the specification can be restored', refused(s2.apply({ op: 'point.restore', id: 'pa2' }), 'point.restore'));
  r = s2.apply({ op: 'point.remove', id: 'pa2' });
  check('point.remove of an added point deletes it', r.ok && !s2.point('pa2') && s2.design.points.added.length === 0);
}
// ---- quantities and budget for points ----
{
  const s = S();
  s.apply({ op: 'point.add', point: { id: 'pa1', kind: 'socket', wall: 'w2', at: 300, room: 'living' } });
  s.apply({ op: 'point.add', point: { id: 'pa2', kind: 'light', x: 200, y: 420 } });
  s.apply({ op: 'point.move', id: 'tv-liv', wall: 'c1', at: 120, room: 'living' });
  s.apply({ op: 'point.remove', id: 'd-liv' });
  const q = quantities(s).points;
  check('quantities: counts per kind and state', q.socket.added === 1 && q.light.added === 1 && q.tv.moved === 1 && q.data.removed === 1 && q.socket.base === 7, q);
  const b = estimate(s, catalog, prices), row = (l) => b.rows.find((x) => x.label === l);
  const e = prices.electric_point, l = prices.lighting_point;
  check('budget: an added socket is one "נקודת חשמל חדשה" priced as an electrical point', row('נקודת חשמל חדשה') && row('נקודת חשמל חדשה').qty === 1 && row('נקודת חשמל חדשה').lo === Math.floor(e.typical_low / 50) * 50);
  check('budget: an added light is one "נקודת תאורה חדשה" priced as a lighting point', row('נקודת תאורה חדשה') && row('נקודת תאורה חדשה').hi === Math.ceil(l.typical_high / 50) * 50);
  check('budget: a moved point is "הזזת נקודה", marked rough; a removed point costs nothing here', row('הזזת נקודה') && row('הזזת נקודה').rough === true && b.rows.filter((x) => x.kind === 'point').length === 3);
}
// ---- partitions ----
{
  const s = S(), z = snap(s), a0 = area(s);
  const r = s.apply({ op: 'partition.add', wall: LIVING_CUT });
  const dv = s.derived, fresh = dv.faces.find((f) => f.room && f.room.fresh);
  check('partition.add across the living room: a new space appears, named "חלל חדש"', r.ok && fresh && fresh.room.name_he === 'חלל חדש' && fresh.net > 12, fresh && { id: fresh.id, net: fresh.net });
  const foot = (620 * 10) / 1e4;
  check('the two parts plus the partition footprint equal the old living room (to 0.1 m²)', near(dv.faceBy.living.net + fresh.net + foot, a0.living, 0.1), [dv.faceBy.living.net, fresh.net, a0.living]);
  check('the walls it meets are split for the rooms only: w2 and c1 stay whole with their openings and points', dv.wallBy.w2.L === 520 && dv.wallBy.c1.L === 380 && dv.edges.some((e) => e.id === 'w2#0') && dv.edges.some((e) => e.id === 'c1#1') && near(dv.pointBy['tv-liv'].y, 200));
  check('the other rooms did not change', Object.keys(a0).every((k) => k === 'living' || near(a0[k], dv.faceBy[k].net, 0.01)));
  check('the new space keeps the living room floor', s.floorOf(fresh.id) === 'porcelain-80');
  check('items follow: the dining table is now in the new space', s.item('i4').room === fresh.id);
  const q = quantities(s).partitions.added;
  check('quantities: added partitions in running metres and m² at the level height', q.m === 6.2 && q.sqm === 16.7, q);
  const b = estimate(s, catalog, prices).rows.find((x) => x.kind === 'partition'), g = prices.gypsum_partition;
  check('budget: "מחיצת גבס חדשה" priced per m² of plasterboard', b && b.label === 'מחיצת גבס חדשה' && b.sqm && b.lo === Math.floor((g.typical_low * 16.7) / 50) * 50, b);
  const z1 = snap(s); s.undo();
  check('partition.add undo: byte-identical, and every room area back to 0.1 m²', snap(s) === z && Object.keys(a0).every((k) => near(a0[k], area(s)[k], 0.1)) && Object.keys(area(s)).length === Object.keys(a0).length);
  s.redo();
  check('partition.add redo gives the same design', snap(s) === z1);
  // naming the new space
  const at = [300, 420];
  check('rule: the new space cannot be called a bedroom when it is too narrow (220 cm deep)', (() => { const r2 = s.apply({ op: 'room.name', at, name_he: 'חדר שינה', type: 'bedroom' }); return !r2.ok && r2.code === 'room.min_width' && r2.reason.startsWith('חדר שינה'); })());
  const zn = snap(s), rn = s.apply({ op: 'room.name', at, name_he: 'חדר עבודה', type: 'other' });
  const named = faceAt(s.derived, at);
  check('room.name: the new space becomes "חדר עבודה", keeping its id (so its floor choice stays)', rn.ok && named.room.name_he === 'חדר עבודה' && named.id === fresh.id && s.design.geometry.rooms.length === 1);
  check('rule: the name comes from the short list', refused(s.apply({ op: 'room.name', at, name_he: 'חדר כושר', type: 'other' }), 'room.name.list'));
  check('rule: a room of the specification is not renamed', refused(s.apply({ op: 'room.name', at: [760, 190], name_he: 'חדר עבודה', type: 'other' }), 'room.name.base'));
  s.undo();
  check('room.name undo: byte-identical, the space is "חלל חדש" again', snap(s) === zn && faceAt(s.derived, at).room.fresh);
  // remove the added partition
  const rr = s.apply({ op: 'partition.remove', id: 'np1' });
  check('partition.remove of an added partition: the living room is whole again', rr.ok && !s.derived.faces.some((f) => f.room && f.room.fresh) && near(s.derived.faceBy.living.net, a0.living, 0.1));
  s.undo();
  check('…and its undo puts it back exactly', snap(s) === zn);
}
{ // the partition rules
  const s = S(), add = (a, b, id = 'nq') => s.apply({ op: 'partition.add', wall: { id, a, b } });
  check('rule: at least 60 cm long', refused(add([0, 300], [50, 300]), 'partition.short'));
  check('rule: at a right angle to the wall it starts from (or in line with it)', refused(add([0, 300], [300, 500]), 'partition.angle'));
  check('rule: it starts from an existing wall', refused(add([100, 300], [400, 300]), 'partition.free'));
  check('rule: 5 cm clear of a door or a window (an end inside the living-room slider)', refused(add([300, 0], [300, 520]), 'partition.opening'));
  check('rule: its end cannot land on an electrical point (the data point on c1)', refused(add([0, 245], [620, 245]), 'partition.point'));
  check('rule: it cannot cross an existing wall', refused(add([0, 300], [900, 300]), 'partition.through'));
  check('rule: not on the balcony rail', refused(add([300, -220], [300, 0]), 'partition.rail'));
  check('rule: not on the balcony', refused(add([60, 0], [60, -100]), 'partition.balcony'));
  check('rule: not outside the apartment', refused(add([0, 300], [-200, 300]), 'partition.outside'));
  check('rule: not on the safe-room walls (placeholder, to be verified)', refused(add([1100, 380], [1100, 500]), 'partition.mamad'));
  const bed = add([620, 150], [1000, 150]);
  check('rule: it may not leave a bedroom under the minimum width', !bed.ok && bed.code === 'room.min_width' && bed.reason.startsWith('שינה הורים'), bed.reason);
  check('a free end is allowed (a wing wall into the living room)', add([0, 150], [200, 150], 'nfree').ok && !s.derived.faces.some((f) => f.room && f.room.fresh) && s.derived.hosts.nfree[1] === null);
  s.undo();
  check('rule: two new partitions cannot cross', add([0, 300], [620, 300], 'na').ok && refused(add([520, 0], [520, 520], 'nb'), 'partition.cross'));
  check('rule: a non-partition wall is never removed (the existing sentence per kind)', (() => { const r = s.apply({ op: 'partition.remove', id: 'c1' }), m = s.apply({ op: 'partition.remove', id: 'm3' }); return !r.ok && r.reason === WALL_KINDS.structural.fixed && !m.ok && m.reason === WALL_KINDS.mamad.fixed; })());
  check('rule: a partition with electrical points on it is not removed before they are', refused(s.apply({ op: 'partition.remove', id: 'p4' }), 'partition.points'));
  check('rule: a wall a new partition leans on does not slide', refused(s.apply({ op: 'wall.shift', id: 'p6', d: 20 }), 'wall.leans') === false && (() => { const t = S(); t.apply({ op: 'partition.add', wall: { id: 'nm', a: [1000, 300], b: [1320, 300] } }); return refused(t.apply({ op: 'wall.shift', id: 'p6', d: 20 }), 'wall.leans'); })());
}
{ // removing a base partition: p11 between the two wet rooms
  const s = S(), z = snap(s), a0 = area(s);
  const r = s.apply({ op: 'partition.remove', id: 'p11' });
  const wc = s.derived.faceBy.wc;
  check('partition.remove p11 is allowed, with the wet-room warning sentence', r.ok && r.warn && r.warn.code === 'partition.wet' && r.warn.reason === RULE['partition.wet']);
  check('the two wet rooms merge into one space named after the first', wc.merged.includes('laundry') && !s.derived.faceBy.laundry && near(wc.net, a0.wc + a0.laundry + (200 * 10) / 1e4, 0.1), [wc.net, a0.wc, a0.laundry]);
  check('the removed partition becomes a ghost and leaves the bill as "removed"', s.derived.ghosts.some((g) => g.id === 'p11') && !s.derived.wallBy.p11 && quantities(s).partitions.removed.m === 2);
  check('rule: removing it again is refused', refused(s.apply({ op: 'partition.remove', id: 'p11' }), 'partition.gone'));
  s.apply({ op: 'partition.add', wall: { id: 'nw', a: [660, 900], b: [660, 500] } });
  check('rule: a partition cannot come back through a new one', refused(s.apply({ op: 'partition.restore', id: 'p11' }), 'partition.blocked'));
  s.undo();
  check('partition.restore brings p11 back', s.apply({ op: 'partition.restore', id: 'p11' }).ok && s.derived.faceBy.laundry && !s.design.geometry.removed.length);
  check('rule: restoring a partition that is there is refused', refused(s.apply({ op: 'partition.restore', id: 'p11' }), 'partition.notgone'));
  s.undo(); s.undo();
  check('remove, restore, both undone: byte-identical, room areas as before', snap(s) === z && Object.keys(a0).every((k) => near(a0[k], area(s)[k], 0.1)));
}
{ // points keep their place in the building when partition p6 slides
  const s = S(), b = s.derived.pointBy;
  const before = Object.fromEntries(s.derived.points.map((p) => [p.id, [p.x, p.y]]));
  const r = s.apply({ op: 'wall.shift', id: 'p6', d: 40 });
  const moved = s.derived.points.filter((p) => p.wall !== 'p6' && !(near(p.x, before[p.id][0], 0.01) && near(p.y, before[p.id][1], 0.01))).map((p) => p.id);
  check('p6 slides 40 cm: every point not on p6 stays where it is in the building', r.ok && moved.length === 0, moved);
  check('the points on p6 itself ride with it, still on the master bedroom face', near(s.derived.pointBy['tv-mst'].x, before['tv-mst'][0] + 40) && s.derived.pointBy['tv-mst'].room === 'master' && s.derived.pointBy['tv-mst'].fx < s.derived.pointBy['tv-mst'].x);
  check('the bedroom 2 points on p5 kept their place even though p5 lost 40 cm at its a-end', near(s.derived.pointBy['tv-b2'].x, 1080) && near(s.derived.pointBy['tv-b2'].atEff, 40) && !s.derived.pointBy['tv-b2'].bad && b);
  check('rule: a slide that would push a corner into a point is refused', refused(s.apply({ op: 'wall.shift', id: 'p6', d: -80 }), 'wall.point'));
}
{ // labels and clear sizes on the real Ashira plans (turned and L-shaped rooms)
  const load = (f) => JSON.parse(fs.readFileSync(lib + 'plans/' + f, 'utf8'));
  const index = JSON.parse(fs.readFileSync(lib + 'plans/index.json', 'utf8')).plans;
  const edgeDist = (q, P) => { let d = Infinity; for (let i = 0, j = P.length - 1; i < P.length; j = i++) { const a = P[j], b = P[i], v = [b[0] - a[0], b[1] - a[1]], L2 = v[0] * v[0] + v[1] * v[1] || 1, t = Math.max(0, Math.min(1, ((q[0] - a[0]) * v[0] + (q[1] - a[1]) * v[1]) / L2)); d = Math.min(d, Math.hypot(q[0] - a[0] - v[0] * t, q[1] - a[1] - v[1] * t)); } return d; };
  const bad = [], worse = [];
  for (const pl of index) {
    const a = load(pl.file), dv = derive(a, emptyDesign(a));
    for (const f of dv.faces) {
      if (!f.room) continue;
      const q = interior(f), g = faceAt(dv, q), c = [(f.bb.x0 + f.bb.x1) / 2, (f.bb.y0 + f.bb.y1) / 2], gc = faceAt(dv, c);
      if (!g || g.id !== f.id) bad.push(pl.id + ':' + f.id);
      if (gc && gc.id === f.id && edgeDist(q, f.poly) + 1 < edgeDist(c, f.poly)) worse.push(pl.id + ':' + f.id);
    }
  }
  check('the label point of every room of all ' + index.length + ' plans is inside that room', bad.length === 0, bad);
  check('…and never closer to a wall than the middle of the room’s box', worse.length === 0, worse);
  const e3 = load('ashira/E-3B.json'), d3 = derive(e3, emptyDesign(e3)), m = d3.faceBy.master;
  const boxW = Math.round(m.bb.x1 - m.bb.x0), boxD = Math.round(m.bb.y1 - m.bb.y0);
  check('Ashira E-3B: the turned master bedroom reports no clear size (its box would say ' + boxW + '×' + boxD + ')', m.clearW === null && m.clearD === null && !m.rect && m.net > 10, { net: m.net });
  check('Ashira E-3B: an axis-aligned rectangular room keeps its true clear size (kitchen 236×284)', d3.faceBy.kitchen.rect && d3.faceBy.kitchen.clearW === 236 && d3.faceBy.kitchen.clearD === 284);
  const q3 = quantities(createStore(e3));
  check('the bill of quantities shows the area only for a non-rectangular room', q3.rooms.find((r) => r.id === 'master').w === null && q3.rooms.find((r) => r.id === 'kitchen').w === 236);
  check('example-4r: every room is a rectangle, so every room still has its clear size', derive(apt, emptyDesign(apt)).faces.every((f) => !f.room || (f.rect && f.clearW > 0)));
}
{ // the guard of the shared call, and a remote change
  const s = S();
  s.setGuard(() => ({ code: 'call.pen', reason: 'העט אצל מישהו אחר.' }));
  const g = s.apply({ op: 'point.add', point: { id: 'pg', kind: 'socket', wall: 'w2', at: 300, room: 'living' } });
  const rm = s.apply({ op: 'partition.add', wall: LIVING_CUT }, { remote: true, by: 'agent' });
  check('the call guard stops a local point; a remote partition passes and is not on my undo stack', !g.ok && g.code === 'call.pen' && rm.ok && !s.canUndo() && s.design.log[s.design.log.length - 1].by === 'agent');
}
{ // speed: 30+ points and 3 added partitions
  const s = S();
  s.apply({ op: 'partition.add', wall: LIVING_CUT });
  s.apply({ op: 'partition.add', wall: { id: 'np2', a: [1320, 120], b: [1170, 120] } });
  s.apply({ op: 'partition.add', wall: { id: 'np3', a: [0, 150], b: [200, 150] } });
  for (let i = 0; i < 4; i++) s.apply({ op: 'point.add', point: { id: 'pp' + i, kind: 'socket', wall: 's4', at: 30 + i * 50 > 85 && 30 + i * 50 < 95 ? 40 : 30 + i * 50 + (i === 1 ? 5 : 0), room: 'kitchen' } });
  const dvs = s.derived, n = dvs.points.length, parts = dvs.walls.filter((w) => w.added).length;
  const runs = [];
  for (let i = 0; i < 300; i++) { const t0 = performance.now(); derive(apt, s.design); runs.push(performance.now() - t0); }
  runs.sort((a, b) => a - b);
  const med = runs[150];
  check('derive() under 2 ms on example-4r with ' + n + ' points and ' + parts + ' added partitions', n >= 30 && parts === 3 && med < 2, { median_ms: +med.toFixed(3), p95_ms: +runs[285].toFixed(3) });
}
{ // a long session, then undo all and redo all
  const s = S(), z = snap(s);
  const ops = [
    { op: 'point.add', point: { id: 'qa', kind: 'tv', wall: 'w2', at: 300, room: 'living' } },
    { op: 'partition.remove', id: 'p11' },
    { op: 'point.move', id: 's-kit-1', wall: 's4', at: 130, room: 'kitchen' },
    { op: 'partition.add', wall: LIVING_CUT },
    { op: 'room.name', at: [300, 420], name_he: 'פינת משפחה', type: 'living' },
    { op: 'point.remove', id: 'l-hall' },
    { op: 'finish.set', key: 'floor:sp-np1-ba', value: 'oak-plank' },
    { op: 'wall.shift', id: 'p6', d: 30 },
  ];
  const ok = ops.map((op) => s.apply(op).ok);
  const z1 = snap(s);
  while (s.canUndo()) s.undo();
  const back = snap(s) === z;
  while (s.canRedo()) s.redo();
  check('eight mixed changes, all undone then all redone: byte-identical both ways', ok.every(Boolean) && back && snap(s) === z1, ok);
}
console.log('\n' + pass + ' passed, ' + fail + ' failed');
process.exit(fail ? 1 : 0);
