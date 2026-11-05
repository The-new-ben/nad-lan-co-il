/* HAD-675 · node test of the three rate tools' math (mrates-common.js on tools/mortgage.js NLMG). Run from anywhere:
     node docs/research/2026-11-05-mortgage-world/build/mrates/test_mrates.js
   Checks: the 5,428 ILS calibration (1,000,000 ILS / 25 years at the system mix), the Banking Order worked example (15,908 ILS
   on 956,994 ILS), the 2022 to 2023 path and its peak, a decision delta (54 ILS per quarter point on 400,000 ILS / 22 years),
   and the identities the tools print (price = interest + linkage + fee, no fee on prime, the ladder). Exit code 1 on a failure. */
'use strict';
var path = require('path');
var HERE = __dirname, REPO = path.resolve(HERE, '../../../../..');
var INS = path.join(REPO, 'plugins/nadlan-config/assets/instruments');
global.window = {};
require(path.join(INS, 'tools/mortgage.js'));
require(path.join(HERE, 'mrates-common.js'));
var M = window.NLMG, R = window.NLMR;
var D = require(path.join(HERE, '../../data/boi-mortgage-v2.json'));  // ships as data/boi-mortgage.json (same keys)
var RT = require(path.join(INS, 'data/boi-rate.json'));
var C = require(path.join(INS, 'data/cbs-120010.json'));

var fails = 0, n = 0;
function ok(cond, name, got) { n++; if (cond) console.log('  ok   ' + name + (got != null ? '  [' + got + ']' : '')); else { fails++; console.log('  FAIL ' + name + (got != null ? '  [' + got + ']' : '')); } }
function near(a, b, tol) { return Math.abs(a - b) <= (tol == null ? 0.5 : tol); }
function r0(x) { return Math.round(x); }

console.log('data: built ' + D.built + ', by_bank ' + D.by_bank.latest.month + ', prepay in force ' + D.prepay.nl.rows[D.prepay.nl.rows.length - 1][0]);

/* 1. calibration */
console.log('\n1. calibration: 1,000,000 ILS, 25 years, system mix ' + D.by_bank.latest.month);
var sys = R.bankMix(D, 'system');
ok(near(sys.rows.reduce(function (a, r) { return a + r.share; }, 0), 100, 0.01), 'system shares add to 100');
var rows = R.mathRows(sys.rows, 1e6, 25), mx = M.mix(rows, M.scenario({}));
ok(r0(mx.first) === 5428, 'first payment rounds to 5,428', mx.first.toFixed(2));
var hl = D.headlines.filter(function (x) { return x.id === 'pay_1m_25y'; })[0];
ok(hl && r0(mx.first) === hl.value, 'matches headlines.pay_1m_25y', hl && hl.value);
var direct = sys.rows.reduce(function (a, r) { var q = Math.pow(1 + r.eff / 100, 1 / 12) - 1, P = 1e6 * r.share / 100; return a + P * q / (1 - Math.pow(1 + q, -300)); }, 0);
ok(near(mx.first, direct, 1e-6), 'NLMG path equals the plain formula (1+e)^(1/12)-1', direct.toFixed(4));

/* 2. the Banking Order worked example */
console.log('\n2. early-repayment fee: 1,000,000 ILS fixed not linked from 2024-11, 25 years, repaid 2026-11');
var rate0 = R.rateIn(D, 'fixed_nl', '2024-11');
ok(rate0 === 4.88, 'the 2024-11 average fixed not-linked rate is 4.88%', rate0);
var fx = R.feeExisting({ date: '2024-11', amount: 1e6, years: 25, k: 'fixed_nl', rate: rate0 }, D, C, '2026-11');
ok(fx.el === 24 && fx.left === 276, '24 payments made, 276 left', fx.el + '/' + fx.left);
ok(r0(fx.bal) === 956994, 'balance 956,994', fx.bal.toFixed(2));
ok(fx.colA === '20_25' && fx.Ae === 4.788, "today's average for 23 years: 4.788% effective (in force " + fx.todayFrom + ')', fx.Ae);
ok(fx.origFrom === '2024-11-14' && fx.Ce === 4.97, 'average on the loan day: 4.97% (in force 2024-11-14)', fx.origFrom + ' ' + fx.Ce);
ok(r0(fx.fee) === 15908, 'capitalization fee rounds to 15,908', fx.fee.toFixed(2));
var hf = D.headlines.filter(function (x) { return x.id === 'prepay_fee'; })[0];
ok(hf && r0(fx.fee) === hf.value, 'matches headlines.prepay_fee', hf && hf.value);
ok(fx.f4 != null && near(fx.fee, Math.min(fx.f3, fx.f4), 1e-6), 'charged = the lower of s.3(3) and s.3(4)', 's3(3) ' + r0(fx.f3) + ', s3(4) ' + r0(fx.f4));
ok(fx.cut === 0 && fx.op === 60 && r0(fx.notice) === 957, 'no reduction before 3 years, operational 60, short notice 957', fx.cut + ' / ' + fx.op + ' / ' + r0(fx.notice));
var fx3 = R.feeExisting({ date: '2024-11', amount: 1e6, years: 25, k: 'fixed_nl', rate: rate0 }, D, C, '2027-11');
ok(fx3.cut === 0.2, '20% off after 3 years', fx3.cut);
var fp = R.feeExisting({ date: '2024-11', amount: 1e6, years: 25, k: 'prime', rate: 5.5 }, D, C, '2026-11');
ok(fp.fee === 0 && fp.why === 'prime', 'prime: no capitalization fee', fp.why);
var fl = R.feeExisting({ date: '2022-06', amount: 1e6, years: 25, k: 'fixed_nl', rate: 3.0 }, D, C, '2026-11');
ok(fl.fee === 0, 'a 3.0% loan with averages above it: no fee', fl.Ae);
var fc = R.feeExisting({ date: '2024-11', amount: 1e6, years: 25, k: 'fixed_cpi', rate: 3.5 }, D, C, '2026-11');
ok(near(fc.ratio, C.months['2026-09'] / C.months['2024-11'], 1e-12) && fc.bal > fc.real, 'linked: balance indexed by the CPI since the loan month', ((fc.ratio - 1) * 100).toFixed(2) + '%');
var fv = R.feeExisting({ date: '2021-11', amount: 1e6, years: 25, k: 'var_cpi', rate: 3 }, D, C, '2026-11');
ok(fv.why === 'reset' && fv.fee === 0, 'variable every 5 years repaid on its change day (month 61): no fee', fv.el);

/* 3. the 2022 path */
console.log('\n3. the 2022 to 2023 path on the system mix, 1,000,000 ILS, 25 years');
var P = R.replayPath(RT, C);
ok(P.months.length === 15 && P.months[0] === '2022-03' && P.months[14] === '2023-05', '15 months, 3.2022 to 5.2023', P.months[0] + '..' + P.months[14]);
ok(P.boi[0] === 0.1 && P.boi[14] === 4.75 && P.prime[0] === 1.6 && P.prime[14] === 6.25, 'BoI 0.10% to 4.75%, prime 1.60% to 6.25%', P.boi.join(' '));
ok(P.hikes.length === 10, 'ten hikes', P.hikes.map(function (c) { return c.from; }).join(' '));
ok(near(P.ratio[14] - 1, C.months['2023-05'] / C.months['2022-03'] - 1, 1e-12), 'CPI over the path', ((P.ratio[14] - 1) * 100).toFixed(2) + '%');
var rp = R.replay(rows, P);
ok(r0(rp.first) === 5428, 'month 1 = today (5,428)', rp.first.toFixed(2));
ok(rp.peakIdx === 14, 'the peak comes in month 15 (5.2023)', P.months[rp.peakIdx]);
ok(r0(rp.peak) === 6201, 'peak payment 6,201', rp.peak.toFixed(2));
ok(r0(rp.extra) === 772, 'extra at the peak 772 a month', rp.extra.toFixed(2));
ok(near(rp.extra, rp.primeX[14] + rp.cpiX[14], 1e-6), 'extra = prime part + CPI part', r0(rp.primeX[14]) + ' + ' + r0(rp.cpiX[14]));
ok(r0(rp.primeX[14]) === 749, 'prime alone adds 749 (the design board: about 747 to 6,176)', rp.primeX[14].toFixed(2));
var lin = rows.filter(function (t) { return t.linked; })[0], S0 = M.track(Object.assign({}, lin, { linked: true }), M.scenario({ cpi: 0 }));
ok(near(rp.by[rows.indexOf(lin)].pay[0], S0.pay[0], 1e-9), 'linked track month 1 = NLMG.track at CPI 0');
ok(r0(rp.cum) === 5927, 'extra paid over the 15 months 5,927', rp.cum.toFixed(2));

/* 4. decision day */
console.log('\n4. decision day: 400,000 ILS prime, 22 years, the average margin');
var m0 = Math.round((sys.rows[1].rate - D.policy.prime) * 100) / 100;
ok(m0 === -0.68, 'average prime margin on new mortgages: prime -0.68', m0);
var dq = R.quarter(400000, D.policy.prime + m0, 264, 0.25);
ok(r0(dq) === 54, 'every quarter point moves the payment 54 ILS', dq.toFixed(2));
var dc = R.decision([{ k: 'prime', amount: 400000, years: 22, rate: D.policy.prime + m0 }]);
ok(near(dc.q, dq, 1e-9) && r0(dc.now) === 2296, 'payment now 2,296', dc.now.toFixed(2));
var dm = R.decision([{ k: 'prime', amount: 400000, years: 22, rate: 4.07 }, { k: 'fixed_nl', amount: 400000, years: 22, rate: 4.61 }, { k: 'var_cpi', amount: 200000, years: 22, rate: 3.23 }]);
ok(near(dm.q, R.quarter(400000, 4.07, 264, 0.25), 1e-9) && dm.prime === 400000, 'whole mix: only prime moves on decision day', dm.q.toFixed(2));
var up = R.ladderPay(dc.rows.length ? [{ k: 'prime', amount: 400000, years: 22, rate: D.policy.prime + m0 }] : [], 0.25);
ok(near(up - dc.now, dq, 1e-9), 'ladder +0.25 = the quarter delta');
var rm = R.rampMonths(D), pb = R.pathPay(400000, D.policy.prime + m0, 264, D.forecast.rate_q3_2027 - D.policy.rate, rm);
ok(rm === 9 && pb.month === 9, 'the forecast ramp ends in month 9 (8.2027)', rm);
ok(pb.pay < dc.now && near(dc.now - pb.pay, dq, 2), 'BoI forecast (3.0%): the payment falls by about one quarter point', (pb.pay - dc.now).toFixed(2));
ok(D.forecast.next_decision === '2026-11-23', 'next decision 23.11.2026', D.forecast.next_decision);

/* 5. exit costs */
console.log('\n5. exit: system mix vs the baskets, BoI forecast path');
var sc = R.exitScenario(D), drop = D.policy.rate - D.forecast.rate_q3_2027;
[3, 5, 7, 10, 25].forEach(function (y) {
  var e = R.exitAt(rows, D, sc, y, drop);
  ok(near(e.price, e.intr + e.link + e.fee, 0.01), y + ' years: price = interest + linkage + fee', r0(e.price) + ' (fee ' + r0(e.fee) + ')');
});
var e25 = R.exitAt(rows, D, sc, 25, drop);
ok(e25.end && e25.fee === 0 && e25.bal === 0, 'to the end: no fee, no balance');
var e5 = R.exitAt(rows, D, sc, 5, drop);
ok(e5.feeBy.filter(function (f) { return f.k === 'prime'; })[0].why === 'prime', 'prime track: no capitalization fee');
ok(e5.feeBy.filter(function (f) { return f.k === 'var_cpi'; })[0].why === 'reset', 'variable every 5 years at year 5: its change day, no fee');
ok(R.exitAt(rows, D, sc, 5, 0).fee === 0, 'averages unchanged: no capitalization fee on a mix at average rates');
var rateOf = function (k) { return sys.rows.filter(function (r) { return r.k === k; })[0].rate; };
D.baskets.list.forEach(function (b) {
  var br = R.mathRows(R.basketRows(D, b, rateOf), 1e6, 25), e = R.exitAt(br, D, sc, 5, drop);
  ok(near(br.reduce(function (a, t) { return a + t.amount; }, 0), 1e6, 1e-6), b.k + ': 1,000,000 split ' + b.mix.map(function (x) { return x[0] + ' ' + Math.round(100 * x[1]) + '%'; }).join(', '), 'price at 5 years ' + r0(e.price));
});

console.log('\n' + (n - fails) + ' of ' + n + ' passed' + (fails ? ', ' + fails + ' FAILED' : ''));
process.exit(fails ? 1 : 0);
