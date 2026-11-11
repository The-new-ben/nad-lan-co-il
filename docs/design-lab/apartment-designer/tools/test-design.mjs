// node test-design.mjs  (HAD-707). Unit checks of every formula in plugins/nadlan-config/assets/instruments/tools/design.js
// against the built data/design.json, edge cases included (zero, very large, missing price data), and a run of every tool's
// page compute on its defaults and on every preset, with the copy gate (no blacklisted word, no site name, no long dash).
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const A = path.join(here, '..', '..', '..', '..', 'plugins', 'nadlan-config', 'assets', 'instruments');
const SRC = fs.readFileSync(path.join(A, 'tools', 'design.js'), 'utf8');
const DATA = JSON.parse(fs.readFileSync(path.join(A, 'data', 'design.json'), 'utf8'));
const clone = (o) => JSON.parse(JSON.stringify(o));

// 1) the pure math, no engine
const win = {};
vm.runInContext(SRC, vm.createContext({ window: win, Intl, Math, Date, JSON, console }));
const N = win.NLDS;

let pass = 0, fail = 0;
const ok = (name, cond, detail) => { if (cond) pass++; else fail++; console.log((cond ? 'ok   ' : 'FAIL ') + name + (detail !== undefined && !cond ? '  ' + JSON.stringify(detail) : '')); };
const near = (name, got, want, tol = 0.5) => ok(name + ' = ' + want, typeof got === 'number' && Math.abs(got - want) <= tol, got);

// ---- ranges and bands ----
const sofa = N.band(DATA.items.sofa_3seat);
ok('band uses the usual band when published', sofa.lo === 1650 && sofa.hi === 6350 && sofa.typical && !sofa.rough);
const f23 = N.band(DATA.items.furnish_2_3r_basic);
ok('band with no top stays open and rough', f23.lo === 30000 && f23.hi === null && f23.rough);
ok('a third of an open band stays open', N.part(f23, 2, 3).hi === null);
const th = N.lvl(sofa, 'mid'); near('mid third of 1,650-6,350 starts at', th.lo, 1650 + 4700 / 3, 0.01); near('mid third ends at', th.hi, 1650 + 2 * 4700 / 3, 0.01);
ok('adding an open range gives an open range', N.radd(N.rg(1, 2), N.rg(3, null)).hi === null);
ok('band of a missing item is null', N.band(undefined) === null && N.rmul(null, 3) === null);
ok('pos: 300/m2 is inside 200-450', N.pos(300, N.band(DATA.fees.fee_m2)) === 'in');
ok('pos: 100/m2 is below all published', N.pos(100, N.band(DATA.fees.fee_m2)) === 'below_all');
ok('pos: 900/m2 is above all published', N.pos(900, N.band(DATA.fees.fee_m2)) === 'above_all');
ok('pos: 160 below the usual band, 500 above it', N.pos(160, N.band(DATA.fees.fee_m2)) === 'below' && N.pos(500, N.band(DATA.fees.fee_m2)) === 'above');

// ---- 1. designer fee ----
let f = N.feeModels({ area: 100, rooms: 4, service: 'full', meetings: 2, works: 150000 }, DATA);
near('fee: per m2, full service, 100 m2, low', f.perM2.lo, 32500); near('fee: per m2 high', f.perM2.hi, 45000);
near('fee: 4 rooms, full = upper half of 16,000-47,500, low', f.byRooms.lo, 31750);
ok('fee: the two methods overlap at 32,500-45,000', f.how === 'overlap' && f.main.lo === 32500 && f.main.hi === 45000, f.main);
near('fee: 7% of 150,000', f.percent.lo, 10500); near('fee: 15% of 150,000', f.percent.hi, 22500);
near('fee: hours that the sum buys, fewest', f.hours.lo, 32500 / 600, 0.01);
f = N.feeModels({ area: 100, rooms: 4, service: 'consult', meetings: 2 }, DATA);
ok('fee: two consultations = 1,600-3,600', f.main.lo === 1600 && f.main.hi === 3600 && f.how === 'meeting');
f = N.feeModels({ area: 60, rooms: 2, service: 'plan' }, DATA);
ok('fee: 2 rooms falls back to the 3-room row and says so', f.rooms.k === 3 && f.rooms.nearest);
ok('fee: no works budget = no percent line', f.percent === null);
f = N.feeModels({ area: 150, rooms: 6, service: 'full' }, DATA);
ok('fee: 6 rooms uses the 5-room row, which is rough', f.rooms.k === 5 && f.rooms.b.rough);
ok('fee: zero area refused', N.feeModels({ area: 0, rooms: 4, service: 'full' }, DATA).error === 'area');
ok('fee: 1,001 m2 refused', N.feeModels({ area: 1001, rooms: 4, service: 'full' }, DATA).error === 'area');
ok('fee: negative works refused', N.feeModels({ area: 100, rooms: 4, service: 'full', works: -1 }, DATA).error === 'works');
const noM2 = clone(DATA); delete noM2.fees.fee_m2;
ok('fee: missing per-m2 data = an error, not a made-up number', N.feeModels({ area: 100, rooms: 4, service: 'full' }, noM2).error === 'data');
f = N.feeModels({ area: 1000, rooms: 10, service: 'full', works: 1e7 }, DATA);
ok('fee: very large flat stays finite', isFinite(f.main.hi) && f.perM2.hi === 450000);

// ---- 2. quote check ----
const allYes = Object.fromEntries(N.QITEMS.map((q) => ['i_' + q.k, 'yes']));
let q = N.quoteCheck(Object.assign({ fee: 30000, area: 100, rooms: 4, vat: 'unk' }, allYes), DATA);
ok('quote: 300/m2 in the usual band, all 10 items written', q.perM2 === 300 && q.posM2 === 'in' && q.yes.length === 10 && q.no.length === 0);
q = N.quoteCheck({ fee: 10000, area: 100, rooms: 3, vat: 'without', i_renders: 'no', i_boq: 'no', i_meet: 'yes' }, DATA);
ok('quote: 100/m2 below all published', q.posM2 === 'below_all');
near('quote: without VAT, with 18% added', q.withVat, 11800, 0.001);
ok('quote: renders and bill of quantities are missing, both priced separately', q.no.length === 2 && q.no.every((x) => x.price && x.price.lo > 0));
ok('quote: unanswered items go to "ask for it in writing"', q.unk.length === 7);
q = N.quoteCheck({ fee: 59000, area: 100, rooms: 4, vat: 'with' }, DATA);
near('quote: with VAT, the sum before VAT', q.without, 59000 / 1.18, 0.01);
ok('quote: zero fee refused', N.quoteCheck({ fee: 0, area: 100 }, DATA).error === 'fee');

// ---- 3/4. furnishing ----
let fu = N.furnish({ rooms: 4, level: 'mid', balcony: 'yes', study: 'no', appliances: 'yes' }, DATA);
ok('furnish 4 rooms: living, dining, master, 2 more bedrooms, balcony, lights, appliances', fu.rooms.map((r) => r.k).join(',') === 'living,dining,master,kid,kid,balcony,lights,appl', fu.rooms.map((r) => r.k));
const fb = N.furnish({ rooms: 4, level: 'basic', balcony: 'yes', study: 'no', appliances: 'yes' }, DATA);
const fh = N.furnish({ rooms: 4, level: 'high', balcony: 'yes', study: 'no', appliances: 'yes' }, DATA);
let sumLo = 0, sumHi = 0; fb.rooms.forEach((r) => r.lines.forEach((l) => { sumLo += l.b.lo * l.qty; sumHi += l.b.hi * l.qty; }));
near('furnish: basic low = the sum of every item\'s low', fb.total.lo, sumLo, 0.01);
near('furnish: high top = the sum of every item\'s top', fh.total.hi, sumHi, 0.01);
ok('furnish: basic < mid < high', fb.total.hi <= fu.total.lo + 1e-6 && fu.total.hi <= fh.total.lo + 1e-6);
ok('furnish: the published whole-flat cross-check is the 4-5 room row', fu.published && /4-5/.test(fu.published.name));
ok('furnish: one room = living and dining, no bedroom', N.furnish({ rooms: 1, level: 'mid' }, DATA).rooms.every((r) => r.k !== 'master'));
ok('furnish: study replaces one bedroom', N.furnish({ rooms: 4, level: 'mid', study: 'yes' }, DATA).rooms.filter((r) => r.k === 'kid').length === 1);
ok('furnish: zero rooms refused', N.furnish({ rooms: 0 }, DATA).error === 'rooms');
const noSofa = clone(DATA); delete noSofa.items.sofa_3seat;
fu = N.furnish({ rooms: 3, level: 'mid' }, noSofa);
ok('furnish: a missing price is left out and named, not invented', fu.missing.includes('sofa_3seat') && fu.total.lo > 0);

// ---- 3. total budget ----
const bud = N.budget({ rooms: 4, area: 100, level: 'mid', designer: 'plan', kitchen: 'yes', kitchenM: 5, parquet: 'yes', parquetM2: 35, ac: 'yes', points: 8, curtains: 'yes', curtM2: 16, paint: 'no', reserve: 10 }, DATA);
const cs = bud.cats.reduce((s, c) => s + c.r.lo, 0);
near('budget: subtotal = sum of the lines', bud.sub.lo, cs, 0.01);
near('budget: total = subtotal + 10%', bud.total.lo, cs * 1.1, 0.01);
ok('budget: names the line that moves the total most', !!bud.swing && bud.cats.includes(bud.swing));
ok('budget: parquet larger than the flat refused', N.budget({ rooms: 4, area: 100, parquet: 'yes', parquetM2: 120 }, DATA).error === 'parquetM2');
ok('budget: 1 room refused', N.budget({ rooms: 1, area: 100 }, DATA).error === 'rooms');
ok('budget: zero reserve allowed', N.budget({ rooms: 3, area: 80, reserve: 0 }, DATA).reserve.lo === 0);

// ---- 5. kitchen ----
let k = N.kitchen({ m: 4, level: 'mid', worktop: 'quartz', island: 'no', sink: 'yes', appl: 'cook' }, DATA);
near('kitchen 4 m mid: cabinets 1,700-2,400 x 4, low', k.parts[0].r.lo, 6800); near('kitchen: cabinets high', k.parts[0].r.hi, 9600);
near('kitchen: quartz mid third x 4, low', k.parts[1].r.lo, (1300 + 1200 / 3) * 4, 0.01);
near('kitchen: total low', k.total.lo, 6800 + (1300 + 400) * 4 + (940 + 2060 / 3) + (709 + 6291 / 3) + (1500 + 5000 / 3) + (487 + 4013 / 3), 0.01);
ok('kitchen: total without appliances is smaller', k.noAppl.hi < k.total.hi);
k = N.kitchen({ m: 6, level: 'high', worktop: 'porcelain', island: 'yes', sink: 'yes', appl: 'full' }, DATA);
ok('kitchen: high level uses the premium cabinet band 3,000-3,050', k.parts[0].r.lo === 18000 && k.parts[0].r.hi === 18300);
ok('kitchen: zero metres refused', N.kitchen({ m: 0, level: 'mid' }, DATA).error === 'm');
ok('kitchen: 25 metres refused', N.kitchen({ m: 25, level: 'mid' }, DATA).error === 'm');
const noCab = clone(DATA); delete noCab.items.kitchen_cab_mid;
k = N.kitchen({ m: 4, level: 'mid', worktop: 'quartz', sink: 'yes', appl: 'none' }, noCab);
ok('kitchen: missing cabinet price is named, the rest still adds up', k.missing.includes('kitchen_cab_mid') && k.parts.every((p) => p.k !== 'cab') && k.total.lo > 0);

// ---- 6. flooring ----
let fl = N.floor({ area: 30, type: 'engineered', pattern: 'straight', box: 2.0 }, DATA);
near('floor: 30 m2 + 8% = 32.4 m2', fl.ordered, 32.4, 1e-9); ok('floor: 17 boxes of 2.0 m2', fl.boxes === 17);
near('floor: engineered 250-510 x 30, low', fl.total.lo, 7500); near('floor: high', fl.total.hi, 15300);
fl = N.floor({ area: 30, type: 'engineered', pattern: 'herringbone', box: 2.0 }, DATA);
ok('floor: herringbone 15% waste = 18 boxes', fl.boxes === 18 && fl.waste === 15);
fl = N.floor({ area: 20, type: 'tile60', pattern: 'straight', box: 1.44 }, DATA);
ok('floor: exactly 15 boxes, no rounding up of a float crumb (21.6 / 1.44)', fl.boxes === 15);
fl = N.floor({ area: 100, type: 'tile80', pattern: 'straight', box: 1.28 }, DATA);
ok('floor: tiles = material on the ordered area + laying on the floor area', fl.parts.length === 2 && fl.parts[1].r.lo === 16000 && Math.abs(fl.parts[0].r.lo - 32 * 85 * 1.28) < 1e-6);
ok('floor: tiles also get the supplied-and-laid cross-check', fl.cross && fl.cross.lo === 16000);
ok('floor: box 0 falls back to the usual pack', N.floor({ area: 30, type: 'engineered', pattern: 'straight', box: 0 }, DATA).box === 2.0);
ok('floor: zero area refused', N.floor({ area: 0, type: 'spc', pattern: 'straight' }, DATA).error === 'area');
ok('floor: unknown pattern refused', N.floor({ area: 10, type: 'spc', pattern: 'zigzag' }, DATA).error === 'pattern');
const noPar = clone(DATA); delete noPar.items.engineered_parquet;
ok('floor: missing price = no total, the boxes still counted', (() => { const r = N.floor({ area: 30, type: 'engineered', pattern: 'straight' }, noPar); return r.total === null && r.boxes === 17 && r.missing[0] === 'engineered_parquet'; })());
ok('floor: skirting adds a line', N.floor({ area: 30, type: 'spc', pattern: 'straight', skirt: 40 }, DATA).parts.length === 2);

// ---- 7. painting ----
let pa = N.paint({ mode: 'rooms', rows: [{ l: 4, w: 3 }], h: 2.5, doors: 1, windows: 1, winM2: 1.5, ceiling: 'no', coats: 2, cover: 10 }, DATA);
near('paint: walls 2 x (4+3) x 2.5', pa.walls, 35, 1e-9); near('paint: minus a door and a window', pa.net, 31.8, 1e-9);
near('paint: litres = 31.8 x 2 / 10', pa.litres, 6.36, 1e-9); ok('paint: cans 5 + 1 + 1', pa.cans.n5 === 1 && pa.cans.n1 === 2 && pa.cans.n18 === 0);
pa = N.paint({ mode: 'rooms', rows: [{ l: 4, w: 3 }], h: 2.5, doors: 0, windows: 0, ceiling: 'yes', coats: 2, cover: 10 }, DATA);
near('paint: ceiling adds the floor area', pa.area, 35 + 12, 1e-9);
pa = N.paint({ mode: 'quick', area: 100, rooms: 4, h: 2.6, doors: 0, windows: 0, ceiling: 'no', coats: 2 }, DATA);
near('paint: quick mode, 6 square-ish spaces', pa.walls, 6 * 4 * Math.sqrt(100 / 6) * 2.6, 1e-6);
ok('paint: openings bigger than the walls give zero, not negative', N.paint({ mode: 'rooms', rows: [{ l: 1, w: 1 }], h: 2.5, doors: 20, windows: 0, coats: 2 }, DATA).net === 0);
ok('paint: cans for 20 l = 18 + 1 + 1', (() => { const c = N.cans(20); return c.n18 === 1 && c.n5 === 0 && c.n1 === 2; })());
ok('paint: cans for 33 l = two of 18', N.cans(33).n18 === 2 && N.cans(33).n5 === 0);
ok('paint: cans for 4 l = one of 5', N.cans(4).n5 === 1 && N.cans(4).n1 === 0);
ok('paint: cans for 0 l = none', N.cans(0).litres === 0);
ok('paint: empty rooms refused', N.paint({ mode: 'rooms', rows: [{ l: 0, w: 0 }], h: 2.6 }, DATA).error === 'rows');
ok('paint: ceiling 1 m refused', N.paint({ mode: 'quick', area: 80, rooms: 3, h: 1 }, DATA).error === 'h');
near('paint: do-it-yourself paint cost at 360 per 18 l can', N.paint({ mode: 'rooms', rows: [{ l: 4, w: 3 }], h: 2.5, doors: 1, windows: 1, winM2: 1.5, coats: 2, cover: 10, can18: 360 }, DATA).diy, 7 * 20, 1e-9);

// ---- 8. sofa ----
near('corner: thin ladder in 100 x 100 corridors = 2√2 x 100', N.cornerMax(100, 100, 0), 200 * Math.SQRT2, 0.05);
near('corner: 90 x 110, the classic (a^2/3 + b^2/3)^3/2', N.cornerMax(90, 110, 0), Math.pow(Math.pow(90, 2 / 3) + Math.pow(110, 2 / 3), 1.5), 0.05);
near('corner: 40 cm thick in 100 x 100 = 2√2 x 100 - 80', N.cornerMax(100, 100, 40), 200 * Math.SQRT2 - 80, 0.05);
ok('corner: thicker than the corridor = 0', N.cornerMax(80, 120, 85) === 0);
let so = N.sofaFit({ W: 420, Dp: 380, L: 240, d: 95, h: 85, table: 60, door: 90, hall: 110, ceil: 260 }, DATA);
ok('sofa: fits the wall', so.c.wall === 'ok'); near('sofa: walkway 380 - 95 - 45 - 60', so.front, 180, 1e-9);
ok('sofa: passes the 90 cm door on its 85 cm side', so.c.door === 'ok');
ok('sofa: does not turn flat into a 110 cm hall, but may on its end under a 2.60 ceiling', so.c.turn === 'maybe' && so.turn < 240, so);
so = N.sofaFit({ W: 420, Dp: 380, L: 240, d: 95, h: 85, table: 60, door: 90, hall: 110, ceil: 230 }, DATA);
ok('sofa: with a 2.30 ceiling it does not turn', so.c.turn === 'no' && so.worst === 'no');
so = N.sofaFit({ W: 230, Dp: 300, L: 240, d: 95, h: 85, table: 0, door: 0, hall: 0 }, DATA);
ok('sofa: longer than the wall = no; no door typed = not checked', so.c.wall === 'no' && so.c.door === 'skip' && so.c.turn === 'skip');
so = N.sofaFit({ W: 400, Dp: 230, L: 200, d: 95, h: 85, table: 50 }, DATA);
ok('sofa: 40 cm left in front = no walkway', so.c.front === 'no');
so = N.sofaFit({ W: 400, Dp: 300, L: 200, d: 90, h: 80, table: 0, lift: 'yes', lw: 110, ld: 210, lh: 220 }, DATA);
ok('sofa: 2 m sofa stands in a stretcher lift', so.c.lift === 'ok');
so = N.sofaFit({ W: 400, Dp: 300, L: 300, d: 100, h: 85, table: 0, lift: 'yes', lw: 100, ld: 125, lh: 210 }, DATA);
ok('sofa: 3 m sofa in a small lift does not fit', so.c.lift === 'no');
ok('sofa: zero length refused', N.sofaFit({ W: 400, Dp: 300, L: 0, d: 90, h: 80 }, DATA).error === 'L');

// ---- 9. rug ----
let ru = N.rugPick({ L: 220, d: 95, f: 230, rw: 400, rd: 400, lay: 'front' }, DATA);
ok('rug: 220 sofa in a 4 x 4 room = 240 x 340', ru.pick && ru.pick[0] === 340 && ru.pick[1] === 240 && ru.status === 'ok', ru);
ru = N.rugPick({ L: 160, d: 85, f: 140, rw: 400, rd: 400, lay: 'front' }, DATA);
ok('rug: 160 sofa, 140 to the console = 160 x 230, priced', ru.pick[0] === 230 && ru.pick[1] === 160 && ru.pid === 'rug_160x230' && ru.price);
ru = N.rugPick({ L: 180, d: 90, f: 170, rw: 320, rd: 350, lay: 'front' }, DATA);
ok('rug: small room = the largest that fits, marked smaller than ideal', ru.status === 'small' && ru.pick[0] === 230);
ru = N.rugPick({ L: 180, d: 90, f: 170, rw: 150, rd: 150, lay: 'front' }, DATA);
ok('rug: a tiny room = no ready size', ru.status === 'none' && ru.pick === null);
ok('rug: 240 x 340 has no published price', N.rugPick({ L: 220, d: 95, f: 230, rw: 400, rd: 400 }, DATA).price === null);

// ---- 10. dining ----
let di = N.dining({ W: 300, Dp: 360, n: 6, shape: 'rect', pass: 'edge' }, DATA);
ok('dining: 6 = table 180 x 90, fits with 91 cm', di.t.l === 180 && di.t.w === 90 && di.status === 'ok');
ok('dining: the most that fit here is 8', di.most === 8); near('dining: 28 cm spare', di.spare, 28, 1e-9);
ok('dining: 6 seats priced as a set', di.price.how === 'set' && di.price.r.lo === 2000);
di = N.dining({ W: 300, Dp: 360, n: 6, shape: 'rect', pass: 'walk' }, DATA);
ok('dining: walking behind needs 112, so only tight', di.status === 'tight');
ok('dining: round for 4 = 90 cm', N.tableFor(4, 'round', DATA).l === 90); ok('dining: round for 6 = 130 cm', N.tableFor(6, 'round', DATA).l === 130);
ok('dining: 10 diners priced as a table and 10 chairs', N.dining({ W: 400, Dp: 600, n: 10, shape: 'rect', pass: 'edge' }, DATA).price.how === 'parts');
ok('dining: 50 cm room refused', N.dining({ W: 50, Dp: 300, n: 4 }, DATA).error === 'W');
ok('dining: 1 diner refused', N.dining({ W: 300, Dp: 300, n: 1 }, DATA).error === 'n');

// ---- 11. bed ----
let be = N.bedFit({ W: 310, Dp: 340, bed: '160', sides: 'both', ward: 'sliding', wardLen: 200 }, DATA);
ok('bed: 160 with sliding wardrobe fits 3.10 x 3.40', be.status === 'ok' && be.need.across === 280 && be.need.along === 330);
be = N.bedFit({ W: 300, Dp: 320, bed: '160', sides: 'both', ward: 'sliding', wardLen: 200 }, DATA);
ok('bed: 3.00 x 3.20 is 10 cm short', be.status === 'no' && be.need.along - 320 === 10);
ok('bed: one side against the wall needs one walkway', N.bedFit({ W: 260, Dp: 300, bed: '90', sides: 'one', ward: 'none' }, DATA).need.across === 150);
ok('bed: the biggest bed that fits a 3.6 x 4 room is 180', N.bedFit({ W: 360, Dp: 400, bed: '160', sides: 'both', ward: 'hinged', wardLen: 240 }, DATA).best[0] === 180);
ok('bed: wardrobe longer than the wall flagged', N.bedFit({ W: 300, Dp: 400, bed: '140', sides: 'both', ward: 'hinged', wardLen: 350 }, DATA).status === 'no');
ok('bed: sliding wardrobe of 2.4 m = two 2 m units', N.bedFit({ W: 300, Dp: 400, bed: '140', sides: 'both', ward: 'sliding', wardLen: 240 }, DATA).wardPrice.units === 2);
ok('bed: kids room 2.6 x 3, bed 90 on the wall, hinged wardrobe at the side = fits', (() => { const r = N.bedFit({ W: 260, Dp: 300, bed: '90', sides: 'one', ward: 'hinged', wardAt: 'side', wardLen: 120 }, DATA); return r.status === 'ok' && r.need.across === 240 && r.need.along === 260; })());
ok('bed: the same wardrobe opposite the bed does not fit (190 + 90 + 60 > 300)', N.bedFit({ W: 260, Dp: 300, bed: '90', sides: 'one', ward: 'hinged', wardAt: 'foot', wardLen: 120 }, DATA).status === 'no');
ok('bed: a side wardrobe longer than the room flagged', N.bedFit({ W: 300, Dp: 300, bed: '90', sides: 'one', ward: 'sliding', wardAt: 'side', wardLen: 320 }, DATA).need.wardOk === false);
ok('bed: unknown bed size refused', N.bedFit({ W: 300, Dp: 400, bed: '200' }, DATA).error === 'bed');

// ---- 12. light ----
let li = N.light({ room: 'living', area: 25, fixture: 'spot' }, DATA);
near('light: living 25 m2 = 150 x 25 x 1.25 lumens', li.lm, 4687.5, 1e-9); ok('light: 8 spots of 600', li.n === 8 && li.points === 8);
ok('light: 8 points at 250-380', li.cost.lo === 2000 && li.cost.hi === 3040);
ok('light: LED profile counted in metres, one point', (() => { const r = N.light({ room: 'living', area: 25, fixture: 'profile' }, DATA); return r.n === 5 && r.points === 1; })());
ok('light: kitchen is 3000-4000 K', N.light({ room: 'kitchen', area: 12, fixture: 'spot' }, DATA).kelvin === '3000 עד 4000');
ok('light: zero area refused', N.light({ room: 'living', area: 0, fixture: 'spot' }, DATA).error === 'area');
ok('light: unknown room refused', N.light({ room: 'garage', area: 10, fixture: 'spot' }, DATA).error === 'room');

// ---- 13. points ----
let pt = N.points({ rows: [{ room: 'סלון', spec: 4, want: 7 }, { room: 'מטבח', spec: 5, want: 3 }] }, DATA);
ok('points: 3 to add, 2 fewer than the specification', pt.add === 3 && pt.less === 2);
ok('points: cost = 3 x 350-700', pt.cost.lo === 1050 && pt.cost.hi === 2100);
ok('points: no rows refused', N.points({ rows: [] }, DATA).error === 'rows');
ok('points: nothing to add costs nothing', N.points({ rows: [{ room: 'x', spec: 5, want: 5 }] }, DATA).cost.hi === 0);

// ---- 14. who ----
ok('who: a permit means an architect', N.who({ permit: 'yes', scope: 'finish', help: 'plan' }, DATA).rec === 'architect');
ok('who: furniture only, full help = home styling', N.who({ permit: 'no', scope: 'furnish', help: 'manage' }, DATA).rec === 'styling');
ok('who: ideas only = a consultation', N.who({ permit: 'no', scope: 'renovate', help: 'ideas' }, DATA).rec === 'consult');
ok('who: plans = design only, priced as the lower half', (() => { const r = N.who({ permit: 'no', scope: 'finish', help: 'plan', rooms: 4 }, DATA); return r.rec === 'plan' && r.opts.plan.r.hi === r.opts.full.r.lo; })());
ok('who: the architect has no invented price', N.who({ permit: 'yes' }, DATA).opts.architect.r === null);

// ---- 15. timeline ----
let tl = N.timeline({ handover: '2028-11', today: '2026-11' }, DATA);
ok('timeline: 24 months left, next = choosing a designer by 3.2027', tl.left === 24 && tl.next.k === 'pro' && tl.next.key === '2027-03');
tl = N.timeline({ handover: '2027-03', today: '2026-11' }, DATA);
ok('timeline: 4 months before handover the next is ordering the kitchen, now', tl.next.k === 'kitchen_order' && tl.next.state === 'now' && tl.late === 7);
tl = N.timeline({ handover: '2028-11', today: '2026-11', signed: '2026-01' }, DATA);
ok('timeline: CBS average from signing = 9.2028 to 3.2029', tl.est.a === '2028-09' && tl.est.b === '2029-03');
ok('timeline: month keys roll over the year', N.ymKey(N.ym('2026-12') + 1) === '2027-01');
ok('timeline: no handover refused', N.timeline({ handover: '', today: '2026-11' }, DATA).error === 'handover');

// ---- 16. style ----
ok('style: calm answers = Japandi', N.style({ q1: 'a', q2: 'b', q3: 'a', q4: 'b', q5: 'a', level: 'mid' }, DATA).top === 'japandi');
ok('style: sea answers = Mediterranean', N.style({ q1: 'd', q2: 'd', q3: 'b', q4: 'd', q5: 'b', level: 'mid' }, DATA).top === 'med');
ok('style: every style has 5 colours', Object.values(N.STYLES).every((s) => s.pal.length === 5 && s.pal.every((p) => /^#[0-9A-F]{6}$/i.test(p[0]))));
ok('style: no answer refused', N.style({}, DATA).error === 'q1');
ok('style: the living-room list is priced', N.style({ q1: 'b', level: 'basic' }, DATA).total.lo > 0);

// ---- 17. curtains ----
let cu = N.curtains({ rows: [{ w: 300, h: 220 }], curtain: 'yes', shutter: 'yes' }, DATA);
near('curtains: 3.00 x 2.20 = 6.6 m2', cu.area, 6.6, 1e-9); ok('curtains: curtain 230-490 per m2', Math.abs(cu.cur.lo - 1518) < 1e-6 && Math.abs(cu.cur.hi - 3234) < 1e-6);
ok('curtains: total = curtain + shutter', Math.abs(cu.total.lo - (1518 + 5280)) < 1e-6);
ok('curtains: no window refused', N.curtains({ rows: [] }, DATA).error === 'rows');

// 2) every tool's page compute, defaults and presets, through a stub engine; the copy gate on everything it writes
const REG = {};
const nf = (d) => new Intl.NumberFormat('he-IL', { minimumFractionDigits: d || 0, maximumFractionDigits: d || 0 });
const NI = { register: (id, spec) => { REG[id] = spec; }, esc: (s) => String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c])),
  fmt: { num: (n, d) => nf(d).format(n || 0), ils: (n) => '₪' + nf(0).format(Math.round(n || 0)), month: (k) => { const p = String(k).split('-'); return (+p[1]) + '.' + p[0]; } } };
const doc = { getElementById: () => ({}), createElement: () => ({}), head: { appendChild() {} } };
vm.runInContext(SRC, vm.createContext({ window: { NadLanInstruments: NI }, document: doc, Intl, Math, Date, JSON, console }));
const BLACK = /ממשק|(?<![֐-׿])דמו(?![֐-׿])|הדגמה|מודל|מנגנון|נקודות חמות|שכבה|אינטראקטיב|רספונסיבי|מובייל|סקיצה|סכמטי|פיילוט|פרוטוטייפ|המערכת|הפלטפורמה|טכנולוגיה|סימולציה|תלת[ -־]?ממד|\b3D\b|אטלס|בקרוב|בבדיקה|—|אריח|https?:|www\.|\.co\.il|\.com\b|Google|גוגל|[\u{1F300}-\u{1FAFF}]/u;
const ids = Object.keys(REG);
ok('17 tools registered', ids.length === 17, ids);
const strings = (o, acc = []) => { if (typeof o === 'string') acc.push(o); else if (o && typeof o === 'object') Object.values(o).forEach((x) => strings(x, acc)); return acc; };
ids.forEach((id) => {
  const spec = REG[id], data = { design: DATA };
  const cases = [['defaults', spec.defaults(data)]].concat((spec.presets || []).map((p) => { const v = spec.defaults(data); Object.assign(v, clone(p.set)); return ['preset ' + p.key, v]; }));
  cases.forEach(([name, v]) => {
    let r; try { r = spec.compute(v, data, null); } catch (e) { r = { crash: String(e && e.stack || e) }; }
    const good = r && !r.crash && !r.error && r.answer && r.answer.value && r.text;
    ok(id + ' ' + name + ': a result a person can read aloud', good, r && (r.crash || r.error));
    if (good) {
      const all = strings([spec.title, spec.lede, spec.kicker, (spec.fields || []).map((f) => [f.label, f.help, (f.options || []).map((o) => o.label)]), (spec.presets || []).map((p) => [p.label, p.sub]), r]).join('\n').replace(/<[^>]+>/g, ' ');
      const m = all.match(BLACK);
      ok(id + ' ' + name + ': copy gate (no blacklisted word, site name or long dash)', !m, m && all.slice(Math.max(0, m.index - 40), m.index + 40));
      ok(id + ' ' + name + ': no NaN or undefined in what it shows', !/NaN|undefined|Infinity/.test(all), (all.match(/.{0,40}(NaN|undefined|Infinity).{0,20}/) || [])[0]);
    }
  });
});
// a missing price must still give a page, never a crash
const thin = clone(DATA); ['sofa_3seat', 'kitchen_cab_mid', 'engineered_parquet', 'wall_paint_m2', 'lighting_point', 'dining_set_6', 'rug_200x300', 'curtain_m2'].forEach((k) => delete thin.items[k]);
ids.forEach((id) => { let r; try { r = REG[id].compute(REG[id].defaults({ design: thin }), { design: thin }, null); } catch (e) { r = { crash: String(e) }; } ok(id + ' with missing prices: no crash', r && !r.crash, r && r.crash); });

console.log('\n' + pass + ' passed, ' + fail + ' failed');
process.exit(fail ? 1 : 0);
