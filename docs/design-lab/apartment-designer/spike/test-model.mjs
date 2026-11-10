// node test-model.mjs : checks of the designer core with no browser (HAD-703 spike).
import { readFileSync } from 'node:fs';
import { createStore, emptyDesign, quantities, derive } from './model.js';
import { STARTER, ITEMS } from './catalog.js';

const apt = JSON.parse(readFileSync(new URL('./example-4r.json', import.meta.url), 'utf8'));
let pass = 0, fail = 0;
const ok = (name, cond, extra = '') => { cond ? pass++ : fail++; console.log((cond ? 'ok   ' : 'FAIL ') + name + (extra ? '  ' + extra : '')); };

const d0 = emptyDesign(apt); d0.items = STARTER.map((i) => ({ ...i }));
const s = createStore(apt, d0);
const f = s.derived.faceBy;
ok('11 rooms found from the wall graph', s.derived.faces.length === 11 && s.derived.faces.every((x) => x.room), s.derived.faces.map((x) => x.id + ' ' + x.net).join(', '));
ok('living gross 32.2 m2', f.living.gross === 32.2, String(f.living.gross));
ok('master 380x380 gross 14.4', f.master.gross === 14.4);
ok('no room merged', s.derived.faces.every((x) => x.merged.length === 0));
ok('every starter piece stands inside a room', s.design.items.length === STARTER.length && STARTER.every((i) => s.roomAt(i.x, i.y)), STARTER.filter((i) => !s.roomAt(i.x, i.y)).map((i) => i.sku).join(','));
ok('every piece is in the catalogue', STARTER.every((i) => ITEMS[i.sku]));

// the partition between the two bedrooms
const m0 = f.master.net, b0 = f.bed2.net;
ok('partition moves 20 cm', s.apply({ op: 'wall.shift', id: 'p6', d: 20 }).ok);
ok('master grew, bed2 shrank, sum kept', s.derived.faceBy.master.net > m0 && s.derived.faceBy.bed2.net < b0 && Math.abs(s.derived.faceBy.master.net + s.derived.faceBy.bed2.net - m0 - b0) < 0.11, s.derived.faceBy.master.net + ' + ' + s.derived.faceBy.bed2.net);
const win = s.derived.openings.find((o) => o.id === 'o-win-bed2'), w3 = s.derived.wallBy.f3;
ok('the facade window stayed where it is in the building', Math.abs(w3.pa[0] + win.at - 1090) < 0.01, String(w3.pa[0] + win.at));
let r = s.apply({ op: 'wall.shift', id: 'p6', d: 60 });
ok('blocked: bedroom narrower than 2.60 m', !r.ok && r.code === 'room.min_width', r.reason);
r = s.apply({ op: 'wall.shift', id: 'p6', d: -110 });
ok('blocked: partition would hit the window', !r.ok && r.code === 'wall.opening', r.reason);
for (const [id, code] of [['f1', 'wall.fixed.facade'], ['c1', 'wall.fixed.structural'], ['m4', 'wall.fixed.mamad'], ['v2', 'wall.fixed.divider']]) {
  r = s.apply({ op: 'wall.shift', id, d: 10 });
  ok('blocked: ' + id + ' is fixed', !r.ok && r.code === code, r.reason);
}
r = s.apply({ op: 'wall.shift', id: 'p4', d: 10 });
ok('blocked: a wall tied to a corner cannot slide', !r.ok, r.code + ' ' + r.reason);
ok('undo returns the partition', s.undo() && Math.abs(s.derived.faceBy.master.net - m0) < 0.01);
ok('redo moves it again', s.redo() && s.derived.faceBy.master.net > m0);
s.undo();

// items, finishes, one gesture = one undo step and one log line
const n0 = s.design.log.length;
for (let i = 1; i <= 30; i++) s.apply({ op: 'item.move', id: 'i2', x: 330 + i, y: 210 }, { gesture: 'g1' });
ok('30 drag moves are one log line', s.design.log.length === n0 + 1 && s.item('i2').x === 360);
s.undo();
ok('one undo returns the whole drag', s.item('i2').x === 330);
r = s.apply({ op: 'item.move', id: 'i2', x: 5000, y: 5000 });
ok('blocked: a piece outside the apartment', !r.ok && r.code === 'item.outside');
s.apply({ op: 'finish.set', key: 'floor:living', value: 'oak-plank' });
const q = quantities(s);
ok('bill of quantities follows the finish', q.floors['oak-plank'] === s.derived.faceBy.living.net && q.rooms.find((x) => x.id === 'living').changed);
ok('net interior area is a sum of the rooms', Math.abs(q.net - q.rooms.filter((x) => x.type !== 'balcony').reduce((a, x) => a + x.net, 0)) < 0.11, q.net + ' m2, balcony ' + q.balcony);

// speed of the core alone: derive + rule check for a wall move
const t = performance.now(); for (let i = 0; i < 2000; i++) derive(apt, s.design);
const per = (performance.now() - t) / 2000;
ok('derive under 1 ms', per < 1, per.toFixed(3) + ' ms');
console.log('\n' + pass + ' passed, ' + fail + ' failed');
process.exit(fail ? 1 : 0);
