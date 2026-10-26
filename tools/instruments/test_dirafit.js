// G1 (26.10.2026): unit checks of tools/dirafit.js (dirafit + diracost) on the built data/dira-round.json.
//   node tools/instruments/test_dirafit.js
// Every expected value below is worked by hand from the official sources named in dira-round.json (the ministry's releases of
// 25.5, 23.6 and 2.8.2026, gov.il benefits_in_apartment_funding 24.2.2026, the lottery file) so a data or logic drift fails here.
const fs = require('fs'), path = require('path'), vm = require('vm');
const A = path.join(__dirname, '..', '..', 'plugins', 'nadlan-config', 'assets', 'instruments');
const win = {}; const ctx = vm.createContext({ window: win, Intl, Math, Date, JSON, console });
vm.runInContext(fs.readFileSync(path.join(A, 'tools', 'dirafit.js'), 'utf8'), ctx);
const d = JSON.parse(fs.readFileSync(path.join(A, 'data', 'dira-round.json'), 'utf8'));
const pt = JSON.parse(fs.readFileSync(path.join(A, 'data', 'ptax.json'), 'utf8'));
const X = win.NLDF;
let bad = 0;
const eq = (name, got, want, tol) => { const ok = Math.abs(got - want) <= (tol == null ? 0.5 : tol); if (!ok) bad++; console.log((ok ? 'OK  ' : 'BAD ') + name + ': ' + (+got).toFixed(4) + ' (want ' + want + ')'); };
const is = (name, got, want) => { const ok = JSON.stringify(got) === JSON.stringify(want); if (!ok) bad++; console.log((ok ? 'OK  ' : 'BAD ') + name + ': ' + JSON.stringify(got) + (ok ? '' : ' (want ' + JSON.stringify(want) + ')')); };

// data: the 23.6.2026 table and the 2.8.2026 reserve figures
eq('round 11 flats', d.towns.reduce((s, t) => s + t.units, 0), 7922, 0);
eq('round 11 lotteries', d.towns.reduce((s, t) => s + t.lots, 0), 82, 0);
eq('town registrations (households in up to 3 towns)', d.r11.town_regs, 313415, 0);
eq('Kiryat Gat flats per 100 households (1,433 / 28,514)', d.towns.find(t => t.n === 'קריית גת').per100, 5.03, 0.005);
eq('Rehovot flats per 100 households (30 / 7,623)', d.towns.find(t => t.n === 'רחובות').per100, 0.39, 0.005);
eq('file: lotteries', d.file.n, 2352, 0);
is('file: newest lottery (rounds 10 and 11 are not in it)', d.file.last, '2025-01-27');
eq('file: lotteries in rounds 1 to 9 (3.2022 to 12.2024)', d.file.n22, 635, 0);
eq('round 9 median odds per lottery', d.rounds.find(r => r.n === 9).odds, 0.00287, 0.00001);

// group odds of round 11
const g = X.groups(d.r11);
eq('all households: 7,922 / 114,848', g.all, 0.06898, 0.00001);
eq('reserve: 4,734 / 25,394', g.res, 0.18642, 0.00001);
eq('others: 3,188 / 89,454 (our calculation)', g.rest, 0.03564, 0.00001);
eq('reserve vs others', g.ratio, 5.23, 0.01);
eq('towns per household: 313,415 / 114,848', g.perHH, 2.729, 0.001);

// eligibility (gov.il tenaey_zkaut, 26.5.2026)
const R = d.rules;
is('couple without a home', [X.eligibility(R, 'couple', 'none').ok, X.eligibility(R, 'couple', 'none').first], [true, true]);
is('couple with one home = improver, continuation only', [X.eligibility(R, 'couple', 'one').status, X.eligibility(R, 'couple', 'one').first, X.eligibility(R, 'couple', 'one').cont], ['משפר דיור', false, true]);
is('single under 35 = not eligible', X.eligibility(R, 'single', 'none').ok, false);
is('single from 35 = eligible', X.eligibility(R, 'single35', 'none').ok, true);
is('two homes at once = not eligible', X.eligibility(R, 'couple', 'two').ok, false);
is('bought in a capped-price programme before = not eligible', X.eligibility(R, 'couple', 'past').ok, false);
is('kibbutz member = not eligible', X.eligibility(R, 'couple', 'kibbutz').ok, false);

// town ranking
is('round 11 top three', X.rank(d, 'r11', '').top, ['כפר מנדא', 'מעלה אדומים', 'קריית גת']);
is('local in Kiryat Gat, sorted by local odds: Kiryat Gat first', X.rank(d, 'local', 'קריית גת').top[0], 'קריית גת');
is('local in Rishon LeZion (low round-11 ratio) still first: the file has local results there', X.rank(d, 'r11', 'ראשון לציון').top, ['ראשון לציון', 'כפר מנדא', 'מעלה אדומים']);
is('local in Mazkeret Batya: no lotteries in the file, the top three stay', X.rank(d, 'r11', 'מזכרת בתיה').top, ['כפר מנדא', 'מעלה אדומים', 'קריית גת']);

// diracost: Kiryat Gat, the last price per m2 in the file 11,802 ₪ (11.11.2024), 100 m2, before VAT
const base = { pm: 11802, size: 100, vat: 'plus', equity: 300000, appraisal: 0, grant: 0, rate: 4.62, term: 25 };
const c1 = X.cost(base, R);
eq('price with VAT 11,802 x 100 x 1.18', c1.price, 1392636, 0.5);
eq('financing 75%', c1.cap, 1044477, 0.5);
eq('own money 25%', c1.own, 348159, 0.5);
eq('short of 300,000', c1.short, 48159, 0.5);
eq('payment on 1,044,477 at 4.62% for 25 years', c1.pay, X.pmt(1044477, 4.62, 25), 0.01);
eq('payment check against U2 (563 per 100,000 at 4.62%, 25 years)', c1.pay / 1044477 * 100000, 563, 0.5);
// the appraisal route: value 1,800,000 (under 2.1M), own money at least 100,000
const c2 = X.cost(Object.assign({}, base, { appraisal: 1800000 }), R);
is('appraisal route taken', c2.route, 'app');
eq('appraisal route: financing = price - 100,000', c2.cap, 1292636, 0.5);
eq('appraisal route: own money 100,000', c2.own, 100000, 0.5);
// appraisal above the cap: the value counts as max(2.1M, price)
const c3 = X.cost(Object.assign({}, base, { appraisal: 2600000 }), R);
eq('appraisal 2.6M counts as 2.1M: 75% = 1,575,000, limited to price - 100,000', c3.cap, 1292636, 0.5);
// below 100,000 own money the appraisal route is closed
const c4 = X.cost(Object.assign({}, base, { equity: 90000, appraisal: 1800000 }), R);
is('appraisal route needs 100,000 own money', c4.route, 'std');
// the grant is part of the financing, not on top of it
const c5 = X.cost(Object.assign({}, base, { grant: 60000 }), R);
eq('grant 60,000: bank loan = 1,044,477 - 60,000', c5.loan, 984477, 0.5);
eq('grant 60,000: own money unchanged', c5.own, 348159, 0.5);
// purchase tax on an only home under 1,978,745 = 0
eq('purchase tax, only home, 1,392,636', X.tax(1392636, pt.tracks.single), 0, 0.01);
eq('purchase tax, only home, 2,100,000 (3.5% above 1,978,745)', X.tax(2100000, pt.tracks.single), (2100000 - 1978745) * 0.035, 0.5);

console.log(bad ? '\n' + bad + ' CHECK(S) FAILED' : '\nALL OK');
process.exit(bad ? 1 : 0);
