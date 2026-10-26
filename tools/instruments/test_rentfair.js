// G5 (26.10.2026): unit checks of tools/rentfair.js on the built data/rent.json.
//   node tools/instruments/test_rentfair.js
// Expected values are worked by hand from the official sources named in rent.json: the government site's rent files (version
// 20-08-2026), CBS table 4.9 (April to June 2026), the CBS rent index 120460 (to September 2026), the Rental and Loan Law sections
// 25י, 25ח, 25יב, 25טו (Nevo text current to 30.9.2026), and Kol Zchut's worked tax examples (updated 22.2.2026). A data or logic
// drift fails here. The second half runs the tool's own compute() through the engine (core.js with a minimal document) on every
// ready case and on edge cases, and checks the output has no NaN, no "undefined", and one well-formed drawing.
const fs = require('fs'), path = require('path'), vm = require('vm');
const A = path.join(__dirname, '..', '..', 'plugins', 'nadlan-config', 'assets', 'instruments');
const d = JSON.parse(fs.readFileSync(path.join(A, 'data', 'rent.json'), 'utf8'));
let bad = 0;
const eq = (name, got, want, tol) => { const ok = Math.abs(got - want) <= (tol == null ? 0.5 : tol); if (!ok) bad++; console.log((ok ? 'OK  ' : 'BAD ') + name + ': ' + (+got).toFixed(4) + ' (want ' + want + ')'); };
const is = (name, got, want) => { const ok = JSON.stringify(got) === JSON.stringify(want); if (!ok) bad++; console.log((ok ? 'OK  ' : 'BAD ') + name + ': ' + JSON.stringify(got) + (ok ? '' : ' (want ' + JSON.stringify(want) + ')')); };

// 1. pure logic (no engine)
const w1 = {}; vm.runInContext(fs.readFileSync(path.join(A, 'tools', 'rentfair.js'), 'utf8'), vm.createContext({ window: w1, Intl, Math, JSON, console }));
const X = w1.NLRF;
const ta = X.cityOf(d, 'תל אביב-יפו');
eq('data: Tel Aviv 3 rooms median, April to June 2026', ta.r['3'].v, 8250, 0); is('data: its quarter', ta.r['3'].q, '2026-06');
eq('data: Israel 4 rooms median', d.nat.r['4'].v, 4825, 0);
eq('data: CBS Israel all sizes, Q2 2026', d.nat.cbs.total.a, 5085.5, 0.01);
eq('data: CBS Tel Aviv 3.5-4 rooms, Q2 2026', ta.cbs['3.5-4'].a, 8871.6, 0.01);
eq('data: CBS Tel Aviv 3.5-4 sampling error', ta.cbs['3.5-4'].e, 119, 0);
eq('data: cities with a median', d.cities.length, 72, 0);
eq('data: neighbourhoods with a median', d.cities.reduce((s, c) => s + c.nb.length, 0), 945, 0);
eq('data: CBS cities', d.cities.filter(c => c.cbs).length, 18, 0);
is('data: rent index to', d.idx.last, '2026-09'); eq('data: rent index over 12 months', d.idx.yoy, 3.2, 0);
eq('carry June to September 2026 = 1.003 x 1.004 x 1.004', X.carry(d.idx, '2026-06'), 1.003 * 1.004 * 1.004, 1e-9);
const r1 = X.ref(d, 'תל אביב-יפו', '', '3');
is('ref: whole city uses the government median', [r1.baseKind, r1.base], ['gov', 8250]);
const r2 = X.ref(d, 'תל אביב-יפו', 'נופי ים', '3');
eq('ref: Nofei Yam all sizes', r2.hood.v, 12975, 0);
eq('ref: Nofei Yam vs the city, all sizes (12,975 / 8,000)', r2.hoodF, 12975 / 8000, 1e-9);
eq('ref: Nofei Yam 3 rooms, our estimate (8,250 x 1.621875)', r2.est, 8250 * 12975 / 8000, 1e-6);
eq('ref: Nofei Yam rank in Tel Aviv', r2.hood.rank, 3, 0);
const r3 = X.ref(d, 'תל אביב-יפו', '', '2');
is('ref: 2 rooms falls back to the CBS 1-2 average', [r3.baseKind, r3.base], ['cbs', ta.cbs['1-2'].a]);
const L = d.law;
const l1 = X.lease(L, 8600, 12); eq('guarantee cap, 12 months at 8,600 = 3 months', l1.cap, 25800, 0); is('  by', l1.by, 'months');
const l2 = X.lease(L, 8600, 6); eq('guarantee cap, 6 months at 8,600 = a third (17,200)', l2.cap, 17200, 0); is('  by', l2.by, 'third');
eq('Kol Zchut example: 3,000 a month for a year -> 9,000', X.lease(L, 3000, 12).cap, 9000, 0);
is('3 months without an option: the chapter does not apply', X.lease(L, 5000, 3).applies, false);
is('4 months: applies', X.lease(L, 5000, 4).applies, true);
is('rent above 20,000 a month: does not apply', X.lease(L, 25000, 12).applies, false);
is('11 years: does not apply', X.lease(L, 5000, 132).applies, false);
const T = d.tax;
eq('tax: 5,000 a month is fully exempt', X.tax(T, 5000, false, 0).exempt.taxable, 0, 0);
eq('tax: Kol Zchut 7,000 a month -> 2,692 taxable (7,000 - 4,308)', X.tax(T, 7000, false, 0).exempt.taxable, 2692, 0);
eq('tax: 12,000 a month, no exemption', X.tax(T, 12000, false, 0).exempt.taxable, 12000, 0);
eq('tax: 10% track on 9,000 with 7,000 paid elsewhere = 200 a month (Kol Zchut)', X.tax(T, 9000, false, 7000).ten.year / 12, 200, 1e-9);
eq('tax: 10% track on 9,000 with 8,000 paid, capped at 7,500 = 150 a month (Kol Zchut)', X.tax(T, 9000, false, 8000).ten.year / 12, 150, 1e-9);
eq('tax: regular track first bracket under 60 (31%)', X.tax(T, 6000, false, 0).reg.rate, 0.31, 0);
eq('tax: regular track first bracket from 60 (10%)', X.tax(T, 6000, true, 0).reg.rate, 0.10, 0);
eq('position: 8,600 vs 8,250', X.position(8600, 8250).pct, 350 / 8250, 1e-12);

// 2. the tool through the engine (core.js) with a minimal document
const doc = { documentElement: { getAttribute: () => 'he' }, readyState: 'complete', querySelectorAll: () => [], addEventListener() {} };
const w2 = {}; const ctx = vm.createContext({ window: w2, document: doc, Intl, Math, JSON, console, setTimeout, clearTimeout, location: { origin: '', pathname: '' }, navigator: {} });
vm.runInContext(fs.readFileSync(path.join(A, 'core.js'), 'utf8'), ctx);
const SP = {}; const reg = w2.NadLanInstruments.register; w2.NadLanInstruments.register = (id, s) => { SP[id] = s; reg(id, s); };
vm.runInContext(fs.readFileSync(path.join(A, 'tools', 'rentfair.js'), 'utf8'), ctx);
const S = SP.rentfair; const dd = { rent: d, d0: d };
is('engine: rentfair registered', !!S, true);
const cases = S.presets(dd).map(p => [p.key, Object.assign(S.defaults(dd), p.set)]);
cases.push(['hood', Object.assign(S.defaults(dd), { hood: 'נופי ים' })]);
cases.push(['two-rooms', Object.assign(S.defaults(dd), { rooms: '2', rent: 5200, guar: 15600 })]);
cases.push(['over-cap', Object.assign(S.defaults(dd), { months: 6, guar: 25800 })]);
cases.push(['landlord-partial', Object.assign(S.defaults(dd), { role: 'landlord', city: 'חיפה', rooms: '4', rent: 4600, other: 2400 })]);
cases.push(['short', Object.assign(S.defaults(dd), { months: 2 })]);
cases.push(['luxury', Object.assign(S.defaults(dd), { rooms: '5', rent: 27000, guar: 81000 })]);
for (const [k, v] of cases) {
  let r; try { r = S.compute(v, dd, null); } catch (e) { r = { error: { msg: String(e) } }; }
  const s = JSON.stringify(r);
  const ok = !r.error && !/NaN|undefined|Infinity/.test(s) && (r.figure.match(/<svg/g) || []).length === 1 && /<\/svg>$/.test(r.figure) && r.table.rows.length > 0;
  if (!ok) bad++;
  console.log((ok ? 'OK  ' : 'BAD ') + 'compute ' + k + ': ' + (r.error ? r.error.msg : r.answer.value + ' | ' + r.answer.label + ' | lines ' + r.lines.length + ' | rows ' + r.table.rows.length));
  for (const sc of (r.scenarios || [])) { const r2 = S.compute(v, dd, sc.key); const ok2 = !r2.error && !/NaN|undefined/.test(JSON.stringify(r2)); if (!ok2) bad++; if (!ok2) console.log('BAD  scenario ' + k + '/' + sc.key); }
}
const over = S.compute(Object.assign(S.defaults(dd), { months: 6, guar: 25800 }), dd, null);
is('over-cap: survey tone and a red segment', [over.answer.tone, over.breakdown.some(b => b.kind === 'survey')], ['survey', true]);
eq('over-cap: 25,800 asked vs 17,200 allowed', over.breakdown.find(b => b.kind === 'survey').value, 8600, 0);
const lp = S.compute(Object.assign(S.defaults(dd), { role: 'landlord', city: 'חיפה', rooms: '4', rent: 4600, other: 2400 }), dd, null);
is('landlord 4,600 + 2,400 = 7,000: partial exemption line', lp.lines.some(l => /2,692/.test(l.value)), true);
const err = S.compute(Object.assign(S.defaults(dd), { rent: 100 }), dd, null);
is('validation: rent 100 is refused', !!err.error, true);
console.log(bad ? 'FAILED ' + bad : 'ALL OK');
process.exit(bad ? 1 : 0);
