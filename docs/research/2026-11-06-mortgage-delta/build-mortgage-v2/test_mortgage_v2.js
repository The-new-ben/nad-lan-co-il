// Round M (HAD-675, 6.11.2026): Mortgage 2.0 v2 checks. node test_mortgage_v2.js
// Loads orig-mortgage.js (v1, byte-identical to live md5 c99f393d...) and the edited tools/mortgage.js into two fake windows, with
// the real data file, and checks: v1 results unchanged for 5 typical mixes and 5 scenarios, then C1, C2, C3, C5, C9, C14, and the
// wording rules on every added line. The C14 cross-check loads tools/mrates-common.js (NLMR, the basket math of mexit) on the new NLMG.
'use strict';
const fs = require('fs'), path = require('path'), vm = require('vm');
const ROOT = path.resolve(__dirname, '..', '..', '..', '..');
const INS = path.join(ROOT, 'plugins', 'nadlan-config', 'assets', 'instruments');
const NEW = path.join(INS, 'tools', 'mortgage.js'), OLD = path.join(__dirname, 'orig-mortgage.js');
const D = JSON.parse(fs.readFileSync(path.join(INS, 'data', 'boi-mortgage.json'), 'utf8'));

function load(files) { const w = {}; const ctx = vm.createContext({ window: w, globalThis: w, Intl, Math, JSON, Date, console }); w.window = w; files.forEach(f => vm.runInContext(fs.readFileSync(f, 'utf8'), ctx, { filename: f })); return w; }
const A = load([OLD]).NLMG, WN = load([NEW, path.join(INS, 'tools', 'mrates-common.js')]), B = WN.NLMG, NLMR = WN.NLMR;

let n = 0, bad = 0;
function ok(name, cond, info) { n++; if (!cond) bad++; console.log((cond ? 'OK   ' : 'FAIL ') + name + (info != null ? '  [' + info + ']' : '')); }
function close(a, b, tol) { return Math.abs(a - b) <= (tol == null ? 1e-9 : tol); }
const same = (x, y) => JSON.stringify(x) === JSON.stringify(y);

/* ------------------------------------------------------------------------------- v1 results unchanged (5 mixes x 5 scenarios) */
const TR = D.tracks, FC = D.forecast, POL = D.policy;
function row(track, amount, years, o) { const T = TR[track]; return Object.assign({ amount, rate: T.rate, years, method: 'spitzer', grace: 0, graceType: 'partial', kind: T.kind, linked: !!T.linked, directed: !!T.directed }, o || {}); }
const MIXES = {
  'default three tracks (1.2M, 25y)': [row('fixed_nl', 600000, 25), row('prime', 400000, 25), row('var5_cpi', 200000, 25)],
  'basket 1 (fixed not linked, 30y)': [row('fixed_nl', 1500000, 30)],
  'basket 2 (thirds, 20y)': [row('fixed_nl', 400000, 20), row('prime', 400000, 20), row('var5_cpi', 400000, 20)],
  'six tracks, grace, equal, balloon, bullet, prepay': [row('fixed_nl', 500000, 25, { prepay: { month: 60, amount: 100000, mode: 'shorten' } }), row('fixed_cpi', 300000, 20, { method: 'equal', grace: 12 }),
    row('prime', 400000, 30, { grace: 6, graceType: 'full' }), row('var5_cpi', 250000, 25, { prepay: { month: 70, amount: 50000, mode: 'reduce' } }), row('var5_nl', 200000, 10, { method: 'bullet' }), row('zakaut', 120000, 15, { method: 'balloon' })],
  'variable heavy (var5 linked and not, 28y)': [row('var5_cpi', 700000, 28), row('var5_nl', 500000, 28), row('prime', 600000, 28), row('fixed_cpi', 400000, 28)]
};
const ramp = Math.max(1, (2027 - 2026) * 12 + (8 - 11));
const SCEN = {
  'BoI CPI, prime unchanged (the page default)': { cpi: 2, prime: 'none' },
  'BoI prime path': { cpi: 2, prime: 'boi', rampTo: FC.rate_q3_2027 - POL.rate, rampMonths: ramp },
  'prime +2% (resets var5)': { cpi: 1.8, prime: 'up2' },
  'custom shock -1 from month 40': { cpi: 2.5, prime: 'custom', shock: -1, shockMonth: 40 },
  'old +2% check on every track': { cpi: 2, prime: 'none', all: 2 }
};
let allSame = true, cnt = 0;
Object.keys(MIXES).forEach(mk => Object.keys(SCEN).forEach(sk => { const a = A.mix(MIXES[mk], A.scenario(SCEN[sk])), b = B.mix(MIXES[mk], B.scenario(SCEN[sk])); cnt++; if (!same(a, b)) { allSame = false; console.log('   differs: ' + mk + ' / ' + sk); } }));
Object.keys(MIXES).forEach(mk => {
  const s = SCEN['prime +2% (resets var5)'], a = A.mix(MIXES[mk], A.scenario(s)), b = B.mix(MIXES[mk], B.scenario(s));
  ok('v1 unchanged, ' + mk + ': every monthly array and total', same(a, b), 'first ' + Math.round(b.first) + ', total ' + Math.round(b.totalPaid));
});
ok('v1 unchanged on all ' + cnt + ' mix x scenario pairs (deep equality of mix())', allSame);
const rows60 = MIXES['variable heavy (var5 linked and not, 28y)'].map(r => Object.assign({}, r, { freq: 60 }));
ok('freq 60 written explicitly gives the v1 result', same(A.mix(MIXES['variable heavy (var5 linked and not, 28y)'], A.scenario(SCEN['prime +2% (resets var5)'])), B.mix(rows60, B.scenario(SCEN['prime +2% (resets var5)']))));
ok('solveLoan unchanged (payment mode)', A.solveLoan(MIXES['default three tracks (1.2M, 25y)'], [50, 33.33, 16.67], A.scenario({ cpi: 2 }), 6000, 'first') === B.solveLoan(MIXES['default three tracks (1.2M, 25y)'], [50, 33.33, 16.67], B.scenario({ cpi: 2 }), 6000, 'first'));
(function () {  // the Banking Order fee on a var5 track at month 30, v1 against v2 (freq missing)
  const t = row('var5_nl', 500000, 25), sc = A.scenario({ cpi: 2 });
  const Sa = A.track(Object.assign({}, t, { prepay: { month: 30, amount: 100000, mode: 'shorten' } }), sc), Sb = B.track(Object.assign({}, t, { prepay: { month: 30, amount: 100000, mode: 'shorten' } }), sc);
  ok('prepayFee unchanged on a 5-year variable track', same(A.prepayFee(t, Sa.prepay, D, 1), B.prepayFee(t, Sb.prepay, D, 1)));
})();

/* ------------------------------------------------------------------------------------------------------------- C1 the band */
const BBMAP = { fixed_nl: 'fixed_nl', fixed_cpi: 'fixed_cpi', prime: 'prime', var5_cpi: 'var_cpi', var5_nl: 'var_nl_other' };
const banks7 = D.by_bank.latest.table.filter(x => x.bank !== 'system');
ok('C1 by_bank latest has 7 banks besides the system row', banks7.length === 7, D.by_bank.latest.month);
Object.keys(BBMAP).forEach(k => {
  const b = B.band(D, k), vals = banks7.map(x => x[BBMAP[k]].rate), lo = Math.min.apply(null, vals), hi = Math.max.apply(null, vals);
  ok('C1 ' + k + ': min and max of the 7 banks (' + BBMAP[k] + ')', b && b.min.eff === lo && b.max.eff === hi && b.n === 7 && b.month === D.by_bank.latest.month && close(b.min.nom, B.ef2nom(lo)) && close(b.max.nom, B.ef2nom(hi)),
    b ? b.min.he + ' ' + lo + ' .. ' + b.max.he + ' ' + hi : 'null');
});
ok('C1 the eligibility loan has no line (not in by_bank)', B.band(D, 'zakaut') === null);
ok('C1 no by_bank in the data: no line', B.band(Object.assign({}, D, { by_bank: undefined }), 'fixed_nl') === null);
ok('C1 the month in Hebrew', B.monthHe('2026-09') === 'ספטמבר 2026' && B.monthHe(D.by_bank.latest.month).indexOf('2026') > 0, B.monthHe(D.by_bank.latest.month));

/* ---------------------------------------------------------------------------------------------------- C2 change frequency */
function rateMonths(S) { const out = []; for (let m = 1; m < S.rate.length; m++) if (Math.abs(S.rate[m] - S.rate[m - 1]) > 1e-12) out.push(m + 1); return out; }
const up2 = B.scenario({ cpi: 2, prime: 'up2' });
[[12, 13], [24, 25], [30, 31], [60, 61], [120, 121]].forEach(([q, first]) => {
  const S = B.track(row('var5_cpi', 500000, 25, { freq: q }), up2);
  ok('C2 every ' + q + ' months: the +2% reaches the track at month ' + first + ' and only there', same(rateMonths(S), [first]) && close(S.rate[first - 1] - S.rate[first - 2], 2), rateMonths(S).join(','));
});
(function () {
  const sh = B.scenario({ cpi: 2, prime: 'custom', shock: 1.5, shockMonth: 40 }), S = B.track(row('var5_nl', 600000, 25, { freq: 12 }), sh);
  ok('C2 a shock from month 40 waits for the next yearly change, month 49', same(rateMonths(S), [49]), rateMonths(S).join(','));
  const S2 = B.track(row('var5_nl', 600000, 25, { freq: 30 }), sh);
  ok('C2 every 2.5 years: the same shock lands at month 61', same(rateMonths(S2), [61]), rateMonths(S2).join(','));
})();
(function () {  // no shock and no forecast reaching the track: the payment is the same on every frequency
  const sc = B.scenario({ cpi: 2, prime: 'boi', rampTo: -0.25, rampMonths: ramp }), base = B.mix([row('var5_cpi', 500000, 25)], sc);
  const allEq = [12, 24, 30, 120].every(q => { const M = B.mix([row('var5_cpi', 500000, 25, { freq: q })], sc); return same(M.pay, base.pay) && M.totalPaid === base.totalPaid; });
  ok('C2 without a shock on the track the payments are identical on all 5 frequencies', allEq, 'first ' + Math.round(base.first));
})();
(function () {
  const t12 = row('var5_nl', 500000, 25, { freq: 12 }), S = B.track(Object.assign({}, t12, { prepay: { month: 30, amount: 100000, mode: 'shorten' } }), B.scenario({ cpi: 2 }));
  const f = B.prepayFee(t12, S.prepay, D, 1);
  ok('C2 Banking Order: a rate that changes every year has no capitalization fee', f.cap === 0 && f.why === 'prime', 'why=' + f.why);
  const t24 = row('var5_nl', 500000, 25, { freq: 24 }), S24 = B.track(Object.assign({}, t24, { prepay: { month: 30, amount: 100000, mode: 'shorten' } }), B.scenario({ cpi: 2 }));
  const f24 = B.prepayFee(t24, S24.prepay, D, 1);
  ok('C2 Banking Order: every 2 years, the period runs to the next change (month 49), bucket up to 5 years', f24.bucket && f24.bucket.from === 1 && f24.bucket.to === 5, f24.bucket ? f24.bucket.label : 'none');
})();

/* ------------------------------------------------------------------------------------------------------------ C3 months */
[48, 250, 301, 360].forEach(mo => {
  const R = B.mix([row('fixed_nl', 1000000, mo / 12)], B.scenario({ cpi: 2 }));
  ok('C3 ' + mo + ' months: schedule of ' + mo + ' rows, ' + Math.ceil(mo / 12) + ' years, paid off', R.N === mo && R.pay.length === mo && R.years.length === Math.ceil(mo / 12) && R.bal[mo - 1] === 0 && close(R.first, B.pmt(1000000, TR.fixed_nl.rate / 1200, mo), 1e-6),
    'first ' + R.first.toFixed(2) + ', last year ' + R.years[R.years.length - 1].mc + ' months');
});

/* --------------------------------------------------------------------------------------------------------------- C5 CSV */
const R0 = B.mix(MIXES['default three tracks (1.2M, 25y)'], B.scenario({ cpi: 2 }));
const CSV = B.csv(R0, ['מסלול 1 קל״צ', 'מסלול 2 פריים', 'מסלול 3 משתנה צמודה']);
const lines = CSV.split('\r\n'); if (lines[lines.length - 1] === '') lines.pop();
const head = lines[0].replace(/^﻿/, '').split(',');
ok('C5 starts with the UTF-8 BOM and ends rows with CRLF', CSV.charCodeAt(0) === 0xFEFF && CSV.indexOf('\r\n') > 0 && Buffer.from(CSV, 'utf8').slice(0, 3).equals(Buffer.from([0xEF, 0xBB, 0xBF])));
ok('C5 one row per month plus the header (300 + 1)', lines.length === R0.N + 1, lines.length);
ok('C5 header: month, then payment, principal, interest, linkage, balance for 3 tracks and the total (21 columns)', head.length === 21 && head[0] === 'חודש' && head[1] === 'מסלול 1 קל״צ: תשלום' && head[5] === 'מסלול 1 קל״צ: יתרה' && head[20] === 'סך הכול: יתרה' && head[17] === 'סך הכול: קרן' && head[18] === 'סך הכול: ריבית' && head[19] === 'סך הכול: הצמדה', head.slice(16).join(' | '));
const r1 = lines[1].split(','), rl = lines[lines.length - 1].split(',');
ok('C5 month 1: total payment and interest match mix()', r1[0] === '1' && r1[16] === R0.pay[0].toFixed(2) && r1[18] === R0.intr[0].toFixed(2), r1[16]);
ok('C5 month 300: the balance is 0.00 and every row has 21 cells', rl[0] === '300' && rl[20] === '0.00' && lines.every(l => l.split(',').length === 21));
ok('C5 a name with a comma is quoted', B.csv(R0, ['משתנה כל 5 שנים, צמודה']).split('\r\n')[0].indexOf('"משתנה כל 5 שנים, צמודה: תשלום"') > 0);
(function () {  // linked track: balance(m) = balance(m-1) + linkage - principal (no prepay)
  const S = R0.T[2]; let okb = true; for (let m = 1; m < 300; m++) if (!close(S.bal[m], S.bal[m - 1] + S.link[m] - S.prin[m], 1e-6)) okb = false;
  ok('C5 the columns add up: balance = previous + linkage - principal, every month', okb);
})();

/* ------------------------------------------------------------------------------------------------------- C9 three scenarios */
const o = { cpi: FC.inflation_4q, prime: 'none', rampTo: 0, rampMonths: ramp, shock: 1, shockMonth: 24 };
const S3 = B.three(MIXES['default three tracks (1.2M, 25y)'], D, o);
ok('C9 three scenarios returned', S3.today && S3.boi && S3.stress && S3.today.N === 300);
ok('C9 "today" = the page default result (prime unchanged, CPI as chosen)', same(S3.today, B.mix(MIXES['default three tracks (1.2M, 25y)'], B.scenario(o))));
const v1st2 = A.mix(MIXES['default three tracks (1.2M, 25y)'], A.scenario(Object.assign({}, o, { all: 2 })));
ok('C9 "stress" = the v1 +2% check (st2), computed by the original file', same(S3.stress, v1st2), 'first ' + Math.round(v1st2.first) + ', total ' + Math.round(v1st2.totalPaid));
const boiRef = B.mix(MIXES['default three tracks (1.2M, 25y)'], B.scenario({ cpi: FC.inflation_4q, prime: 'boi', rampTo: FC.rate_q3_2027 - POL.rate, rampMonths: ramp }));
ok('C9 "BoI forecast" = the prime path to ' + FC.rate_q3_2027 + '% with CPI ' + FC.inflation_4q + '%', same(S3.boi, boiRef) && S3.boi.totalPaid < S3.today.totalPaid && S3.stress.totalPaid > S3.today.totalPaid,
  Math.round(S3.boi.totalPaid) + ' < ' + Math.round(S3.today.totalPaid) + ' < ' + Math.round(S3.stress.totalPaid));
ok('C9 each scenario has first, highest with its month, total', ['today', 'boi', 'stress'].every(k => S3[k].first > 0 && S3[k].highest >= S3[k].first - 1e-9 && S3[k].highestMonth >= 1 && S3[k].totalPaid > 0));
const S3u = B.three(MIXES['default three tracks (1.2M, 25y)'], D, Object.assign({}, o, { prime: 'up2' }));
ok('C9 "today" ignores the chosen prime path (rates unchanged)', same(S3u.today, S3.today));

/* -------------------------------------------------------------------------------------------------- C14 uniform baskets */
const loan = 1234567, yrs = 25, sc = B.scenario({ cpi: 2 });
const mine = { fixed_nl: 4.9, prime: 4.1 };  // a mix with two typed rates; var5_cpi falls back to the average
const rateOf = k => mine[k] != null ? mine[k] : TR[k].rate;
const BK = B.baskets(D, loan, yrs, rateOf, sc);
ok('C14 three baskets of directive 451', BK.length === 3 && BK.map(b => b.k).join() === 'b1,b2,b3', BK.map(b => b.label).join(' / '));
const BACK = { fixed_nl: 'fixed_nl', prime: 'prime', var_cpi: 'var5_cpi', var_nl_other: 'var5_nl', fixed_cpi: 'fixed_cpi' };
BK.forEach(b => {
  const rowsR = NLMR.mathRows(NLMR.basketRows(D, D.baskets.list.filter(x => x.k === b.k)[0], k => rateOf(BACK[k])), loan, yrs), M = B.mix(rowsR, sc);
  ok('C14 ' + b.label + ': first, highest, total equal the mexit basket math (NLMR)', close(M.first, b.R.first, 1e-6) && close(M.highest, b.R.highest, 1e-6) && close(M.totalPaid, b.R.totalPaid, 1e-4),
    Math.round(b.R.first) + ' / ' + Math.round(b.R.highest) + ' / ' + Math.round(b.R.totalPaid));
});
ok('C14 basket 1 is one Spitzer loan at the typed rate', close(BK[0].R.first, B.pmt(loan, 4.9 / 1200, 300), 1e-6));
ok('C14 the amounts add up to the loan in every basket', BK.every(b => close(b.rows.reduce((a, r) => a + r.amount, 0), loan, 1e-6)));

/* ------------------------------------------------------------------------------------------------------------ wording */
const src = fs.readFileSync(NEW, 'utf8'), orig = fs.readFileSync(OLD, 'utf8');
ok('no en or em dash anywhere in the new file', !/[\u2013\u2014]/.test(src));
const origSet = new Set(orig.split(/\r?\n/)), added = src.split(/\r?\n/).filter(l => !origSet.has(l));
const BL = ['סימולציה', 'ממשק', 'מודל', 'המלצה', 'כדאי'];
const hits = added.filter(l => BL.some(w => l.indexOf(w) > -1) || /(^|[^֐-׿])דמו([^֐-׿]|$)/.test(l) || /(^|[^A-Za-z])AI([^A-Za-z]|$)/.test(l));
ok('no blacklisted word in the ' + added.length + ' added or changed lines', hits.length === 0, hits.slice(0, 2).join(' || '));
ok('the one "כדאי" left is the v1 status text kept word for word', (src.match(/כדאי/g) || []).length === 1 && (orig.match(/כדאי/g) || []).length === 1);
ok('the CSV header has no blacklisted word or dash', !BL.some(w => lines[0].indexOf(w) > -1) && !/[\u2013\u2014]/.test(CSV));
ok('version note in the header', /v2 \(round M, HAD-675, 6\.11\.2026\)/.test(src.slice(0, 4000)));

console.log('\n' + (n - bad) + '/' + n + ' passed' + (bad ? ', ' + bad + ' FAILED' : ''));
process.exit(bad ? 1 : 0);
