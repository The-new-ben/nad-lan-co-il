// node dump-design.mjs > design.json : a design document as the store writes it, for schema validation
import { readFileSync } from 'node:fs';
import { createStore, emptyDesign } from './model.js';
import { STARTER } from './catalog.js';
const apt = JSON.parse(readFileSync(new URL('./example-4r.json', import.meta.url), 'utf8'));
const d = emptyDesign(apt); d.items = STARTER.map((i) => ({ ...i }));
const s = createStore(apt, d);
s.apply({ op: 'wall.shift', id: 'p6', d: 20 }, { by: 'buyer' });
s.apply({ op: 'finish.set', key: 'floor:living', value: 'oak-plank' }, { by: 'designer' });
s.apply({ op: 'item.move', id: 'i2', x: 340, y: 220 }, { by: 'rep', gesture: 'g1' });
process.stdout.write(JSON.stringify(s.design, null, 1));
