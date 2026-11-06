/* HAD-675 · node test of mhivun ("עמלת היוון"): plugins/nadlan-config/assets/instruments/tools/mhivun.js (window.NLHV) on
   tools/mrates-common.js (NLMR.feeExisting) and tools/mortgage.js (NLMG), with the repo data files. Run from anywhere:
     node docs/research/2026-11-06-mortgage-universe/build/build-mhivun/test_mhivun.js
   "Today" is fixed at 2026-11 (the data's build month), so the numbers are the README's. Hand-worked checks use closed forms
   written here (Spitzer payment, balance, annuity value, effective to nominal), not NLMG. Exit code 1 on any failure. */
'use strict';
var path = require('path'), fs = require('fs'), cp = require('child_process');
var HERE = __dirname, REPO = path.resolve(HERE, '../../../../..');
var INS = path.join(REPO, 'plugins/nadlan-config/assets/instruments');
global.window = {};
require(path.join(INS, 'tools/mortgage.js'));
require(path.join(INS, 'tools/mrates-common.js'));
require(path.join(INS, 'tools/mhivun.js'));
var M = window.NLMG, R = window.NLMR, H = window.NLHV;
var D = require(path.join(INS, 'data/boi-mortgage.json'));
var C = require(path.join(INS, 'data/cbs-120010.json'));
var NOW = '2026-11';
var DASH = new RegExp('[' + String.fromCharCode(0x2013, 0x2014) + ']');  // the two long dashes, built from their codes

var fails = 0, n = 0;
function ok(cond, name, got) { n++; if (cond) console.log('  ok   ' + name + (got != null ? '  [' + got + ']' : '')); else { fails++; console.log('  FAIL ' + name + (got != null ? '  [' + got + ']' : '')); } }
function near(a, b, tol) { return Math.abs(a - b) <= (tol == null ? 0.5 : tol); }
function r0(x) { return Math.round(x); }
/* closed forms, independent of NLMG */
function nom(e) { return 1200 * (Math.pow(1 + e / 100, 1 / 12) - 1); }
function pay(B, a, n) { var r = a / 1200; return r ? B * r / (1 - Math.pow(1 + r, -n)) : B / n; }
function balAfter(B, a, N, k) { var P = pay(B, a, N), r = a / 1200; return r ? P * (1 - Math.pow(1 + r, -(N - k))) / r : B - P * k; }
function ann(P, a, n) { var r = a / 1200; return P * (1 - Math.pow(1 + r, -n)) / r; }
function row(k, amount, date, years, rate, freq, id) { return { id: id || 0, k: k, amount: amount, date: date, n: Math.round(years * 12), rate: rate, freq: H.isVar(k) ? (freq || 60) : null }; }
function same(a, b) { return JSON.stringify(a) === JSON.stringify(b); }

console.log('data: built ' + D.built + ', prepay.nl in force ' + D.prepay.nl.rows[D.prepay.nl.rows.length - 1][0] + ', CPI ' + C.latest + ', today ' + NOW);

/* 1. one loan: mhivun = mexit = NLMR.feeExisting, exactly */
console.log('\n1. one loan: exactly what mexit (NLMR.feeExisting) gives');
var mx = { date: '2024-11', amount: 1e6, years: 25, k: 'fixed_nl', rate: 4.88 };
var fx = R.feeExisting(mx, D, C, NOW), one = H.mortgage([row('fixed_nl', 1e6, '2024-11', 25, 4.88)], D, C, NOW);
ok(one.fee === fx.fee && one.bal === fx.bal, "mexit's worked example: same fee and balance to the last digit", fx.fee + ' / ' + fx.bal);
ok(r0(one.fee) === 15908 && r0(one.bal) === 956994, 'the data headline: 15,908 on 956,994', r0(one.fee) + ' on ' + r0(one.bal));
var hl = D.headlines.filter(function (x) { return x.id === 'prepay_fee'; })[0];
ok(hl && r0(one.fee) === hl.value, 'equals headlines.prepay_fee of boi-mortgage.json', hl && hl.value);
ok(same(H.feeOne(row('fixed_nl', 1e6, '2024-11', 25, 4.88), D, C, NOW), fx), 'NLHV.feeOne returns the feeExisting object itself, field by field');
// a seeded sweep over every track, date, term and rate: the whole-mortgage path with one row = feeExisting
var seed = 7; function rnd() { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }
var months = []; for (var k = '2021-12'; k <= '2026-10'; k = R.mAdd(k, 1)) months.push(k);
var tk = ['fixed_nl', 'fixed_cpi', 'prime', 'var_cpi', 'var_nl_other'], bad1 = 0, bad2 = 0, cases = 0, kinds = {};
for (var i = 0; i < 400; i++) {
  var kk = tk[i % 5], dt = months[Math.floor(rnd() * months.length)], yrs = 5 + Math.floor(rnd() * 26), rt = Math.round((1 + rnd() * 6) * 100) / 100, am = 50000 + Math.floor(rnd() * 950) * 1000;
  if (R.mDiff(dt, NOW) >= yrs * 12) continue;
  cases++; var o = { date: dt, amount: am, years: yrs, k: kk, rate: rt }, ref = R.feeExisting(o, D, C, NOW), mg = H.mortgage([row(kk, am, dt, yrs, rt)], D, C, NOW);
  if (!(mg.fee === ref.fee && mg.bal === ref.bal && mg.notice === ref.notice)) bad1++;
  if (!same(H.feeFreq(o, D, C, NOW, 60), ref)) bad2++;
  kinds[ref.why || (ref.fee > 0.5 ? 'fee' : 'zero')] = (kinds[ref.why || (ref.fee > 0.5 ? 'fee' : 'zero')] || 0) + 1;
}
ok(cases >= 350 && bad1 === 0, cases + ' seeded single loans: mortgage() fee, balance and notice === feeExisting', 'mismatches ' + bad1 + ', ' + JSON.stringify(kinds));
ok(bad2 === 0, 'feeFreq with a 60-month cycle returns exactly the feeExisting object in all ' + cases + ' (the same formula)', 'mismatches ' + bad2);
var fv60 = R.feeExisting({ date: '2021-11', amount: 1e6, years: 25, k: 'var_cpi', rate: 3 }, D, C, NOW);
ok(same(H.feeFreq({ date: '2021-11', amount: 1e6, years: 25, k: 'var_cpi', rate: 3 }, D, C, NOW, 60), fv60) && fv60.why === 'reset', 'variable every 5 years on its change day (month 61): both say reset, no fee', fv60.el);

/* 2. the opening example, by hand */
console.log('\n2. the opening example (7.2023, four tracks), by hand');
var EX = H.EXAMPLE.rows.map(function (r, i) { return row(r.k, r.amount, H.EXAMPLE.date, r.term, r.rate, r.freq, i); });
ok(EX.length === 4 && EX.reduce(function (a, r) { return a + r.amount; }, 0) === 1400000, 'example: 4 tracks, 1,400,000 from 7.2023');
var MG = H.mortgage(EX, D, C, NOW), L0 = MG.loans[0].fx;
var P0 = pay(500000, 5.3, 300), B0 = balAfter(500000, 5.3, 300, 40);
ok(L0.el === 40 && L0.left === 260 && near(L0.bal, B0, 1e-6), 'fixed not linked: 40 paid, 260 left, balance = P(1-(1+r)^-260)/r = 464,966.66', B0.toFixed(2));
var A0 = nom(4.788), C0 = nom(5.022);
ok(L0.colA === '20_25' && L0.Ae === 4.788 && L0.todayFrom === '2026-10-19', "today's average for 21.7 years: column 20_25, 4.788% effective, in force 19.10.2026", L0.Ae);
ok(L0.colC === '20_25' && L0.Ce === 5.022 && L0.origFrom === '2023-07-12', 'loan-day average: 5.022% (file in force 12.7.2023)', L0.origFrom + ' ' + L0.Ce);
ok(near(L0.A, A0, 1e-12) && near(L0.A, 4.68603, 1e-5), '4.788% effective = 4.68603% nominal: 1200((1.04788)^(1/12) - 1)', L0.A.toFixed(5));
var pvA0 = ann(P0, A0, 260), pvC0 = ann(P0, C0, 260);
ok(near(L0.f3, pvA0 - B0, 1e-4) && r0(L0.f3) === 26191, 's.3(3) = annuity at 4.68603% - balance = 26,191', (pvA0 - B0).toFixed(2));
ok(near(L0.f4, pvA0 - pvC0, 1e-4) && r0(L0.f4) === 9799, 's.3(4) = annuity at 4.68603% - annuity at 4.9100% (5.022% effective) = 9,799', (pvA0 - pvC0).toFixed(2));
ok(L0.cut === 0.2 && near(L0.fee, 0.8 * (pvA0 - pvC0), 1e-4) && r0(L0.fee) === 7839, 'the lower one (s.3(4)) x 0.8 (3 years passed in 7.2026) = 7,839', L0.fee.toFixed(2));
var dl0 = H.detail(MG.loans[0]);
ok(near(dl0.pvR, L0.bal, 1e-6) && dl0.which === 4 && dl0.n === 260 && near(dl0.first, P0, 1e-6), 'detail: value at the loan rate = the balance; 260 payments of ' + P0.toFixed(2) + '; lower = s.3(4)', dl0.pvR.toFixed(2));
var L1 = MG.loans[1];
ok(L1.status === 'prime' && L1.fx.fee === 0 && r0(L1.fx.bal) === r0(balAfter(450000, 4.15, 300, 40)), 'prime: no capitalization fee, the reason kept (status prime), balance by hand', r0(L1.fx.bal));
var L2 = MG.loans[2].fx, k0 = H.cpiKey(C, '2023-07'), k1 = H.cpiKey(C, NOW);
ok(k0 === '2023-07' && k1 === '2026-09' && near(L2.ratio, C.months['2026-09'] / C.months['2023-07'], 1e-12), 'linked: CPI 9.2026 / CPI 7.2023 = ' + L2.ratio.toFixed(4), L2.ratio);
var B2r = balAfter(300000, 4.2, 300, 40), B2 = B2r * L2.ratio;
ok(near(L2.bal, B2, 1e-6) && L2.h === 20, 'variable every 5 years: balance x CPI = ' + B2.toFixed(2) + '; 20 payments to the change day 7.2028', L2.h);
var P2 = pay(B2, 4.2, 260), b2h = (function () { var b = B2, r = 4.2 / 1200; for (var q = 0; q < 20; q++) b = b + b * r - P2; return b; })();
var A2 = nom(3.501), C2 = nom(3.921), pv = function (a) { return ann(P2, a, 20) + b2h / Math.pow(1 + a / 1200, 20); };
ok(L2.colA === 'le5' && L2.colC === 'le5' && near(L2.f3, pv(A2) - B2, 1e-4) && near(L2.f4, pv(A2) - pv(C2), 1e-4), 'variable: 20 payments + the balance on the change day, at 3.501% and 3.921% (column le5)', r0(L2.f3) + ' / ' + r0(L2.f4));
ok(r0(L2.fee) === 1537 && H.detail(MG.loans[2]).change === '2028-07', 'variable fee = min x 0.8 = 1,537; next change day 7.2028', L2.fee.toFixed(2));
var L3 = MG.loans[3].fx;
ok(L3.colA === '15_20' && L3.f4 === null && r0(L3.fee) === 4374, 'fixed linked (20 years): column 15_20, the loan-day average 3.995% was above 3.9%, so only s.3(3): 4,374', L3.fee.toFixed(2));
ok(r0(MG.fee) === 13750 && near(MG.fee, L0.fee + L2.fee + L3.fee, 1e-9), 'the whole mortgage: 7,839 + 0 + 1,537 + 4,374 = 13,750', MG.fee.toFixed(2));
ok(r0(MG.bal) === 1319919 && MG.op === 60 && near(MG.notice, MG.bal * 0.001, 1e-6), 'balance 1,319,919; operational fee 60 once; notice 0.1% of the balance = 1,320', r0(MG.notice));
ok(near(MG.cpiFee, (L2.bal + L3.bal) * D.cpi.avg_m12 / 100 / 2, 1e-6) && r0(MG.cpiFee) === 302, 'CPI fee (1st to 15th) only on the two linked tracks: 302', MG.cpiFee.toFixed(2));

/* 3. change cycles other than 5 years */
console.log('\n3. variable tracks every 1, 2, 2.5 and 10 years');
var v30 = row('var_nl_other', 300000, '2024-01', 25, 5.2, 30), f30 = H.feeOne(v30, D, C, NOW);
ok(f30.el === 34 && f30.h === 26 && f30.colA === '1_5' && f30.colC === '1_5', 'every 2.5 years from 1.2024: change days 7.2026 and 1.2029, 26 payments counted, columns 1_5', f30.h);
var s30 = M.stream(f30.bal, 5.2, f30.left, 26, 'spitzer'), A30 = nom(R.avgOf(D, 'nl', D.prepay.nl.rows[D.prepay.nl.rows.length - 1], '1_5'));
ok(near(f30.f3, M.pv(s30, A30) - f30.bal, 1e-6) && f30.fee > 0, 'every 2.5 years: s.3(3) on those 26 payments at the 1_5 average', f30.fee.toFixed(2));
var v12 = row('var_nl_other', 300000, '2024-01', 25, 5.2, 12), f12 = H.feeOne(v12, D, C, NOW);
ok(f12.fee === 0 && f12.why === 'prime' && H.status(f12, 5.2) === 'yearly', 'every year: no capitalization fee (the rate changes at least yearly, s.4)', f12.why);
var f24 = H.feeOne(row('var_cpi', 300000, '2024-11', 25, 4, 24), D, C, NOW);
ok(f24.why === 'reset' && f24.fee === 0 && H.status(f24, 4) === 'reset', 'every 2 years, taken 11.2024, repaid 11.2026: the change day, no fee', f24.el);
var f120 = H.feeOne(row('var_cpi', 300000, '2021-11', 25, 4, 120), D, C, NOW);
ok(f120.h === 60 && f120.colA === 'le5' && f120.colC === '5_10', 'every 10 years from 11.2021: 60 payments to 11.2031, loan-day column 5_10', f120.h + ' ' + f120.colC);

/* 4. the age discount and the reasons for no fee */
console.log('\n4. the 20% and 30% steps, and never a bare zero');
var at = function (m) { return H.feeOne(row('fixed_nl', 500000, '2023-07', 25, 5.3), D, C, R.mAdd('2023-07', m)); };
ok(at(35).cut === 0 && at(36).cut === 0.2, '35 payments: no discount; 36: 20%', at(35).fee.toFixed(0) + ' -> ' + at(36).fee.toFixed(0));
ok(at(59).cut === 0.2 && at(60).cut === 0.3, '59: 20%; 60: 30%', at(59).fee.toFixed(0) + ' -> ' + at(60).fee.toFixed(0));
var low = H.mortgage([row('fixed_nl', 500000, '2022-01', 25, 3)], D, C, NOW).loans[0];
ok(low.fx.fee === 0 && low.status === 'noavg', 'a 3.00% loan from 1.2022: no fee, status "today\'s average not lower than your rate"', low.fx.Ae);
var orig = H.mortgage([row('fixed_nl', 500000, '2021-12', 25, 5)], D, C, NOW).loans[0];
ok(orig.fx.A < 5 && orig.fx.f3 > 10000 && orig.fx.Ce === 3.36 && orig.fx.f4 === 0 && orig.fx.fee === 0 && orig.status === 'orig', 'a 5.00% loan from 12.2021: s.3(3) = ' + r0(orig.fx.f3) + ', but the loan-day average 3.36% is below today\'s, so s.3(4) = 0 and the fee is 0: status orig', r0(orig.fx.f3));
var tie = H.mortgage([row('fixed_nl', 500000, '2024-01', 25, 4.8)], D, C, NOW).loans[0];
ok(tie.fx.f4 === null && tie.fx.Ce === 5.235 && near(tie.fx.fee, tie.fx.f3 * (1 - tie.fx.cut), 1e-9) && r0(tie.fx.fee) === 4931, 'a 4.80% loan from 1.2024: the loan-day average 5.235% was above the rate, so only s.3(3) applies: 4,931', tie.fx.fee.toFixed(2));
var stats = {}; MG.loans.forEach(function (l) { stats[l.status] = 1; });
ok(MG.loans.every(function (l) { return l.status === 'fee' ? l.fx.fee >= 0.5 : ['prime', 'yearly', 'reset', 'noavg', 'orig', 'tiny'].indexOf(l.status) > -1; }), 'every track has a fee or a named reason', Object.keys(stats).join(','));
var ended = H.mortgage([row('fixed_nl', 100000, '2010-01', 10, 5)], D, C, NOW).loans[0];
ok(!ended.active && ended.status === 'ended', 'a track past its term is not counted');

/* 5. partial prepayment */
console.log('\n5. partial prepayment: the least fee');
var A200 = H.allocate(MG, 200000, 'reduce', D);
ok(A200.items.length === 1 && A200.items[0].id === 1 && A200.fee === 0, '200,000: all to prime (no capitalization fee), fee 0', JSON.stringify(A200.items.map(function (x) { return [x.id, r0(x.a)]; })));
ok(near(A200.items[0].drop, pay(200000, 4.15, 260), 1e-6) && r0(A200.items[0].drop) === 1167, 'payment drop = pmt(200,000, 4.15%, 260) = 1,167', A200.items[0].drop.toFixed(2));
ok(near(A200.saved, A200.items[0].drop * 260 - 200000, 1e-6) && r0(A200.saved) === 103537, 'interest saved to the end = 260 x drop - 200,000 = 103,537', A200.saved.toFixed(2));
ok(near(A200.prop, MG.fee * 200000 / MG.bal, 1e-9) && r0(A200.prop) === 2084, 'split by the balances instead: 2,084 of fee', A200.prop.toFixed(2));
var A600 = H.allocate(MG, 600000, 'reduce', D);
ok(same(A600.items.map(function (x) { return x.id; }), [1, 2]) && A600.items[0].full && near(A600.items[1].a, 600000 - MG.loans[1].fx.bal, 1e-6), '600,000: prime closed, the rest to the variable track (lowest fee per shekel 0.52% vs 1.69% and 3.05%)', r0(A600.items[1].a));
ok(near(A600.fee, L2.fee * A600.items[1].a / L2.bal, 1e-9) && r0(A600.fee) === 962, 'fee = 1,537 x 186,673 / 298,378 = 962', A600.fee.toFixed(2));
var Dsyn = { fees: D.fees, cpi: D.cpi, term: { cpi: { buckets: [{ from: 0, to: null, nom: L2.C }] } } };
var pf1 = M.prepayFee({ kind: 'var5', linked: true, method: 'spitzer', freq: 60 }, { month: 40, amount: L2.bal, before: L2.bal, rate: 4.2, share: 1, endBefore: 300 }, Dsyn, L2.C - L2.A);
var sh = A600.items[1].a / L2.bal, pfs = M.prepayFee({ kind: 'var5', linked: true, method: 'spitzer', freq: 60 }, { month: 40, amount: A600.items[1].a, before: L2.bal, rate: 4.2, share: sh, endBefore: 300 }, Dsyn, L2.C - L2.A);
ok(near(pf1.cap, L2.fee, 1e-9) && near(pfs.cap, A600.items[1].fee, 1e-9), 'NLMG.prepayFee with share = a/B gives the same partial fee (the fee is linear in the share)', pfs.cap.toFixed(2));
var best = A600.fee;
ok(best <= A600.prop + 1e-9 && A600.prop - best > 5000, 'the least-fee split beats the split by balances by over 5,000', r0(A600.prop - best));
var S600 = H.allocate(MG, 600000, 'shorten', D);
ok(S600.items[0].months === 260 && S600.items[1].months > 0 && S600.saved > A600.saved, 'shorten: prime closed (260 months), the variable track shorter by ' + S600.items[1].months + ' months, more interest saved than reduce', r0(S600.saved) + ' > ' + r0(A600.saved));
var cut1 = H.cut(100000, 5 / 1200, 120, 0);
ok(near(cut1.saved, 0, 1e-6) && cut1.months === 0, 'shorten with 0 repaid: nothing saved, no month cut');
var big = H.allocate(MG, 5e6, 'reduce', D);
ok(big.capped && near(big.amount, MG.bal, 1e-6) && near(big.fee, MG.fee, 1e-6), 'more than the balance: capped at the balance, the fee = the full payoff fee', r0(big.amount));

/* 6. when to prepay: 24 months */
console.log('\n6. the next 24 months');
var W = H.strip(EX, D, C, NOW, 24);
ok(W.months.length === 25 && W.months[0] === NOW && W.months[24] === '2028-11' && near(W.base[0], MG.fee, 1e-9), '25 months from 11.2026 to 11.2028; month 0 = today\'s total', r0(W.base[0]));
ok(W.cheap === 19 && W.months[19] === '2028-06' && r0(W.base[19]) === 10849 && r0(W.save) === 2901, 'cheapest month 6.2028: 10,849, 2,901 less than today', W.months[W.cheap]);
var e20 = W.ev[20].map(function (e) { return e.t + e.id; }).sort().join(' ');
ok(W.months[20] === '2028-07' && e20 === 'col0 col3 cut300 cut303 reset2', '7.2028: 30% on tracks 1 and 4, change day on track 3, two tracks move to a lower-average column', e20);
ok(W.by[20][2] === 0 && W.base[20] > W.base[19], 'on the change day track 3 pays nothing, yet the total rises (20 years left: the 15-20 average is lower)', r0(W.base[19]) + ' -> ' + r0(W.base[20]));
var mono = true; for (var j = 1; j < 25; j++) if (!(W.down[j] >= W.base[j] - 1e-6 && W.base[j] >= W.up[j] - 1e-6)) mono = false;
ok(mono, 'every month: averages 0.5 lower >= unchanged >= 0.5 higher (the fee falls as the average rises)');
var Dd = H.shiftD(D, -0.5);
ok(D.prepay.nl.rows.length === 60 && Dd.prepay.nl.rows.length === 61 && Dd.prepay.nl.rows[60][4] === Math.round((D.prepay.nl.rows[59][4] - 0.5) * 1e6) / 1e6 && R.avgRow(Dd, 'nl', '2023-07-15')[0] === '2023-07-12', 'scenario data: one moved row appended, the original untouched, the loan-day average unchanged');
var W2 = H.strip([row('var_cpi', 300000, '2024-03', 25, 4.2, 24)], D, C, NOW, 24), rs = [];
W2.ev.forEach(function (l, q) { l.forEach(function (e) { if (e.t === 'reset') rs.push(W2.months[q]); }); });
ok(same(rs, ['2028-03']) && W2.base[W2.months.indexOf('2028-03')] === 0, 'every 2 years from 3.2024: the change day 3.2028 is marked and its fee is 0', rs.join(' '));
var Wf = H.strip([row('fixed_nl', 500000, '2022-01', 25, 3)], D, C, NOW, 24);
ok(Wf.cheap === 0 && Wf.base.every(function (v) { return v === 0; }), 'a loan with no fee all along: no cheaper month is claimed');

/* 7. the bank's number */
console.log('\n7. the bank\'s number');
var c1 = H.compare(13750, 13900), c2 = H.compare(13750, 16000), c3 = H.compare(0, 40);
ok(c1.close && near(c1.d, 150, 1e-9), '13,900 against 13,750: close (within 2%)', c1.pct.toFixed(4));
ok(!c2.close && near(c2.pct, 2250 / 13750, 1e-12), '16,000 against 13,750: a gap of 2,250 (16.4%)', (100 * c2.pct).toFixed(1) + '%');
ok(c3.close && c3.pct === null, 'no fee here, 40 from the bank: within 50, no percentage');

/* 8. the file itself: wording rules, sources, no network */
console.log('\n8. the file: words, dashes, sources');
var SRC = fs.readFileSync(path.join(INS, 'tools/mhivun.js'), 'utf8');
ok(!DASH.test(SRC), 'no long dash (U+2013 or U+2014) anywhere in mhivun.js');
var banned = ['ממשק', 'דמו', 'הדגמה', 'סימולציה', 'מנגנון', 'אינטראקטיבי', 'המערכת', 'הפלטפורמה', 'טכנולוגיה'].filter(function (w) { return SRC.indexOf(w) > -1; });
ok(!banned.length && !/\b(interface|demo)\b/i.test(SRC), 'none of the banned words', banned.join(','));
ok(SRC.indexOf("title: 'עמלת היוון'") > -1 && SRC.indexOf('מה זה היוון משכנתא') > -1 && SRC.indexOf('הפרשי היוון') > -1 && SRC.indexOf('פירעון חלקי') > -1, 'title "עמלת היוון", "מה זה היוון משכנתא", "הפרשי היוון", "פירעון חלקי" present');
ok(['צו הבנקאות (עמלת פירעון מוקדם), התשס"ב-2002', 'https://www.boi.org.il/roles/supervisionregulation/circulars/cir2103/', 'https://www.boi.org.il/information/interestrates/', "D.prepay.nl.src, 'mashfix'"].every(function (s) { return SRC.indexOf(s) > -1; }), 'the source line: the Order, the BoI fee averages file, cir2103, the interest rates page');
ok(!/\b(fetch|XMLHttpRequest|sendBeacon|localStorage)\b/.test(SRC.replace(/\/\*[\s\S]*?\*\//g, '')), 'no request and no storage of its own (the data comes from the shortcode, the case lives in #mhivun=)');

/* 9. the server summary (registry.php.txt) against the same numbers, when php is on the PATH */
console.log('\n9. the server summary');
var php = cp.spawnSync('php', [path.join(HERE, 'render_summary.php')], { encoding: 'utf8' });
if (php.error || php.status !== 0) console.log('  skip: php not available (' + (php.error ? php.error.code : php.stderr) + ')');
else {
  var out = php.stdout, nowD = D.built.slice(0, 7), sx = H.mortgage([row('fixed_nl', 500000, '2023-07', 25, 5.3)], D, C, nowD).loans[0].fx;
  var fmt = function (v) { return Math.round(v).toLocaleString('en-US'); };
  ok(out.indexOf(fmt(sx.bal) + ' ₪') > -1 && out.indexOf(fmt(sx.fee) + ' ₪') > -1, 'PHP worked example = JS at ' + nowD + ': balance ' + fmt(sx.bal) + ', fee ' + fmt(sx.fee));
  var TN = D.prepay.nl.rows[D.prepay.nl.rows.length - 1], TCr = D.prepay.cpi.rows[D.prepay.cpi.rows.length - 1];
  ok(['4.607%', '4.788%', '3.242%', '3.365%', '19.10.2026', '9.2026'].every(function (s) { return out.indexOf(s) > -1; }) && TN[6] === 4.607 && TCr[6] === 3.242, 'PHP summary: the 10-15 and 20-25 averages of both files, in force 19.10.2026, data 9.2026');
  ok(!DASH.test(out) && out.indexOf('עמלת היוון') > -1 && out.indexOf('הפרשי היוון') > -1, 'PHP summary: no long dash; says עמלת היוון and הפרשי היוון');
  fs.writeFileSync(path.join(HERE, 'summary.out.html'), out, 'utf8');
}

console.log('\n' + (n - fails) + ' of ' + n + ' passed' + (fails ? ', ' + fails + ' FAILED' : ''));
process.exit(fails ? 1 : 0);
