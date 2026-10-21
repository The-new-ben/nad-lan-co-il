// HAD-527: unit checks of the Instruments logic (node test_tools.js). Loads the tool files with a fake window.
const fs = require('fs'), path = require('path'), vm = require('vm');
const A = path.join(__dirname, '..', '..', 'plugins', 'nadlan-config', 'assets', 'instruments');
const win = {}; const ctx = vm.createContext({ window: win, Intl, Math, Date, JSON, console });
for (const f of ['tools/indexation.js', 'tools/delay.js']) vm.runInContext(fs.readFileSync(path.join(A, f), 'utf8'), ctx);
const cbs = JSON.parse(fs.readFileSync(path.join(A, 'data', 'cbs-200010.json'), 'utf8'));
let bad = 0; const eq = (name, got, want, tol) => { const ok = Math.abs(got - want) <= (tol || 0.5); if (!ok) bad++; console.log((ok ? 'OK  ' : 'BAD ') + name + ': ' + got.toFixed(2) + ' (want ' + want + ')'); };
// known index rule
console.log('known 2023-01-14 ->', win.NLIX.knownKey('2023-01-14'), '| 2023-01-16 ->', win.NLIX.knownKey('2023-01-16'));
// indexation: new law, 20% at signing, 80% a year later, half linked
const v = { price: 1000000, sign: '2023-01-20', delivery: '2025-01-01', share: 50, floor: true, rows: [{ date: '2023-01-20', pct: 20 }, { date: '2024-01-20', pct: 80 }] };
const r = win.NLIX.compute(v, cbs, 0.03);
const ratio = cbs.months['2023-12'] / cbs.months['2022-12'];
eq('new law, 400,000 linked for a year', r.total, 400000 * (ratio - 1), 0.01);
console.log('   CBS check value: 400000 x', ratio.toFixed(5));
// old law: whole payment linked
const r2 = win.NLIX.compute(Object.assign({}, v, { sign: '2022-01-20', rows: [{ date: '2022-01-20', pct: 20 }, { date: '2023-01-20', pct: 80 }], share: 100 }), cbs, 0.03);
eq('old law, 800,000 linked for a year', r2.total, 800000 * (cbs.months['2022-12'] / cbs.months['2021-12'] - 1), 0.01);
// new law: a payment after the contractual delivery is linked only to the delivery date
const r3 = win.NLIX.compute(Object.assign({}, v, { delivery: '2023-07-01', rows: [{ date: '2023-01-20', pct: 20 }, { date: '2024-01-20', pct: 80 }] }), cbs, 0.03);
eq('linkage stops at the contractual delivery', r3.total, 400000 * (cbs.months['2023-05'] / cbs.months['2022-12'] - 1), 0.01);
// share above 50% under the new law is refused
console.log('50% cap:', win.NLIX.compute(Object.assign({}, v, { share: 60 }), cbs, 0.03).error ? 'refused OK' : 'BAD');
// delay: new law
const D = win.NLDX.compute;
eq('new law, 3 weeks late: nothing', D({ signed: '2023-01-01', due: '2025-01-01', state: 'done', handed: '2025-01-21', rent: 8000 }).total, 0);
eq('new law, 3 months late: months 2-3 x1', D({ signed: '2023-01-01', due: '2025-01-01', state: 'done', handed: '2025-04-01', rent: 8000 }).total, 16000);
eq('new law, 12 months late', D({ signed: '2023-01-01', due: '2025-01-01', state: 'done', handed: '2026-01-01', rent: 8000 }).total, 8000 * (3 + 6 * 1.25 + 2 * 1.5));
eq('new law, 4 months and 1 day', D({ signed: '2023-01-01', due: '2025-01-01', state: 'done', handed: '2025-05-02', rent: 8000 }).total, 8000 * (3 + 1.25));
// delay: old law
eq('old law, 50 days: nothing', D({ signed: '2021-01-01', due: '2024-01-01', state: 'done', handed: '2024-02-20', rent: 8000 }).total, 0);
eq('old law, 70 days: 3 months x1.5 from day 1', D({ signed: '2021-01-01', due: '2024-01-01', state: 'done', handed: '2024-03-11', rent: 8000 }).total, 3 * 1.5 * 8000);
eq('old law, 10 months', D({ signed: '2021-01-01', due: '2024-01-01', state: 'done', handed: '2024-11-01', rent: 8000 }).total, 8000 * (8 * 1.5 + 2 * 1.25));
// HAD-534: the soil map and the PFAS calculator, on the built data
for (const f of ['tools/soilmap.js', 'tools/pfas.js']) vm.runInContext(fs.readFileSync(path.join(A, f), 'utf8'), ctx);
const soil = JSON.parse(fs.readFileSync(path.join(A, 'data', 'sde-dov-soil.json'), 'utf8'));
const S = win.NLSX.stats(soil);
eq('soil: published reports', S.reports, 7, 0); eq('soil: boreholes executed in reports', S.holes, 101, 0); eq('soil: boreholes over the PFOS threshold', S.over, 60, 0);
eq('soil: the peak is plot 303, x598', S.top.pfosX, 597.97, 0.01);
eq('pfas: 3,780,000 ng/kg PFOS = x598', win.NLPF.compute(3780000, 'ng', 'pfos', soil.thresholds).x, 597.97, 0.01);
eq('pfas: 3.78 mg/kg = the same', win.NLPF.compute(3.78, 'mg', 'pfos', soil.thresholds).x, 597.97, 0.01);
eq('pfas: 1,896.4 ng/kg PFOA = x1', win.NLPF.compute(1896.4, 'ng', 'pfoa', soil.thresholds).x, 1, 0.0001);
eq('soil: Tel Aviv 1 km check', win.NLSX.dist([34.78, 32.10], [34.78, 32.109]), 1000.8, 2);
// ptax (21.10.2026): the Tax Authority brackets; 18M = the figures on the Kochav listing, checked against the simulator
vm.runInContext(fs.readFileSync(path.join(A, 'tools/ptax.js'), 'utf8'), ctx);
const PT = JSON.parse(fs.readFileSync(path.join(A, 'data', 'ptax.json'), 'utf8')).tracks;
eq('ptax: 18M only home', win.NLPT.tax(18e6, PT.single).tax, 1153886.3, 1);
eq('ptax: 18M additional home', win.NLPT.tax(18e6, PT.extra).tax, 1678899.3, 1);
eq('ptax: 18M new immigrant', win.NLPT.tax(18e6, PT.oleh).tax, 975975.9, 1);
eq('ptax: 18M foreign resident = additional', win.NLPT.tax(18e6, PT.foreign).tax, 1678899.3, 1);
eq('ptax: 3M only home', win.NLPT.tax(3e6, PT.single).tax, 45538.3, 1);
eq('ptax: 1.9M only home is exempt', win.NLPT.tax(1.9e6, PT.single).tax, 0, 0.01);
eq('ptax: 25M only home (10% above 20,183,565)', win.NLPT.tax(25e6, PT.single).tax, 1810214.9, 1);
// pcost (21.10.2026): the equity a buyer needs; tax from the same ptax brackets
vm.runInContext(fs.readFileSync(path.join(A, 'tools/pcost.js'), 'utf8'), ctx);
const PC = { tracks: PT }, CC = JSON.parse(fs.readFileSync(path.join(A, 'data', 'cost.json'), 'utf8'));
const pv = { price: 3e6, kind: 'second', track: 'single', loan: 1.5e6, lawyer: 0.5, broker: 2, checks: 2650, moving: 12000, renovation: 80000, furniture: 40000, reserve: 50000 };
eq('pcost: 3M second-hand, only home: deal costs', win.NLPC.compute(pv, PC, CC).deal, 137048.3, 1);
eq('pcost: 3M second-hand, only home: equity', win.NLPC.compute(pv, PC, CC).equity, 1819048.3, 1);
eq('pcost: new from a developer: no broker', win.NLPC.compute(Object.assign({}, pv, { kind: 'new' }), PC, CC).broker, 0, 0.01);
eq('pcost: mortgage file fee capped at 360', win.NLPC.compute(pv, PC, CC).mfee, 360, 0.01);
eq('pcost: foreign resident LTV cap 50%', win.NLPC.compute(Object.assign({}, pv, { track: 'foreign' }), PC, CC).cap, 0.5, 0.0001);
// pval (21.10.2026): the official neighbourhood median by rooms, the city as a fallback, the old per-m2 way
vm.runInContext(fs.readFileSync(path.join(A, 'tools/pval.js'), 'utf8'), ctx);
const VD = JSON.parse(fs.readFileSync(path.join(A, 'data', 'value.json'), 'utf8'));
const vb = { method: 'deals', city: 'תל אביב יפו', hood: '65210023', rooms: 4, condition: 0, building: 0, range: 5, asking: 0, sqm: 100 };
eq('pval: Bavli 4 rooms = the official median', win.NLPV.compute(vb, VD).value, 6549400, 1);
eq('pval: Kochav HaTzafon (no median) falls back to the city', win.NLPV.compute(Object.assign({}, vb, { hood: '65210017' }), VD).value, 5229800, 1);
eq('pval: +5% condition', win.NLPV.compute(Object.assign({}, vb, { condition: 5 }), VD).value, 6876870, 1);
eq('pval: per-m2 way 100 x 50,000 + parking 150,000', win.NLPV.compute({ method: 'sqm', sqm: 100, ppsqm: 50000, parking: 150000, storage: 0, balcony: 0, balconyPrice: 0, condition: 0, building: 0, range: 5 }, VD).value, 5150000, 1);
console.log(bad ? bad + ' FAILED' : 'ALL CHECKS PASS');
process.exit(bad ? 1 : 0);
