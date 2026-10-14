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
console.log(bad ? bad + ' FAILED' : 'ALL CHECKS PASS');
process.exit(bad ? 1 : 0);
