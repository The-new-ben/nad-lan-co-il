/* HAD-675 · node test of mcheck ("בדיקת משכנתא לפני חתימה"). Run from anywhere:
     node docs/research/2026-11-06-mortgage-delta/build-mcheck/test_mcheck.js
   Loads the REAL data files (plugins/nadlan-config/assets/instruments/data/boi-mortgage.json, boi-rate.json, cbs-120010.json) and
   the real tool scripts with a fake window: tools/mortgage.js (NLMG), mrates-common.js (NLMR), moffers.js (NLMO), mquick.js (NLMQ)
   and the new tools/mcheck.js (NLMC). "Today" is fixed at 6.11.2026 so the dates are stable. One section per check of presign.md
   section 3 (1 to 28), then the wording rules: the summary has 5 to 8 sentences and no recommendation word, no long dash in any
   string, no "0 ₪" shown for a value nobody typed. Exit code 1 on a failure. */
'use strict';
var path = require('path'), fs = require('fs');
var REPO = path.resolve(__dirname, '../../../..');
var INS = path.join(REPO, 'plugins/nadlan-config/assets/instruments');
global.window = {};
['mortgage', 'mrates-common', 'moffers', 'mquick', 'mcheck'].forEach(function (f) { require(path.join(INS, 'tools', f + '.js')); });
var C = window.NLMC, G = window.NLMG, R = window.NLMR, O = window.NLMO, Q = window.NLMQ;
var D = require(path.join(INS, 'data/boi-mortgage.json')), RT = require(path.join(INS, 'data/boi-rate.json')), CPI = require(path.join(INS, 'data/cbs-120010.json'));
var XR = { rt: RT, cpi: CPI }, TODAY = '2026-11-06';

var fails = 0, n = 0;
function ok(cond, name, got) { n++; if (cond) console.log('  ok   ' + name + (got != null ? '  [' + got + ']' : '')); else { fails++; console.log('  FAIL ' + name + (got != null ? '  [' + got + ']' : '')); } }
function near(a, b, tol) { return Math.abs(a - b) <= (tol == null ? 0.5 : tol); }
function run(st) { return C.run(st, D, XR, TODAY); }
function F(res, id, level) { return res.flags.filter(function (f) { return f.id === id && (!level || f.level === level); }); }
function one(res, id, level) { return F(res, id, level)[0] || null; }
function isNa(res, id) { return res.na.some(function (x) { return x.id === id; }); }
function ex() { return C.example(D, TODAY); }
function allText(res) { return [].concat(res.sum, res.qs, res.flags.map(function (f) { return f.title + ' ' + f.you + ' ' + f.rule + ' ' + f.src.map(function (s) { return s.label; }).join(' '); }), res.na.map(function (x) { return x.title + ' ' + x.why; })).join('\n'); }

console.log('data: built ' + D.built + ', by_bank ' + D.by_bank.latest.month + ', forecast ' + D.forecast.published + ', today ' + TODAY);

/* 0. the example, built from the 9.2026 averages (by_bank, all banks) */
console.log('\n0. the example: 1,200,000 ILS, 25 years, the all-banks mix and rates of ' + D.by_bank.latest.month);
var E = ex(), RE = run(E);
var sys = R.bankMix(D, 'system');
ok(C.bmodel(E, 'offer').sum === 1200000 && C.bmodel(E, 'b2').sum === 1200000, 'every basket\'s tracks add up to 1,200,000');
ok(E.b.offer.irr === Math.round(sys.irr * 100) / 100, 'row 7 of the proposed basket = the all-banks overall rate the Bank of Israel published', E.b.offer.irr);
var flat = G.mix(C.bmodel(E, 'offer').tr.map(function (t) { return C.eng(t); }), G.scenario({})).first;
var per1 = Q.payPer1(D.by_bank, 'system', D.by_bank.months.length - 1, 25) * 1200000;
ok(near(flat, per1, 60), 'first payment at flat rates matches NLMQ.payPer1 on the system mix (rounded track amounts)', flat.toFixed(0) + ' vs ' + per1.toFixed(0));
ok(near(1.2 * 5428, flat, 60), 'and the page calibration 5,428 per 1,000,000 x 1.2', flat.toFixed(0));
var b1x = G.mix(C.bmodel(E, 'b1').tr.map(function (t) { return C.eng(t); }), R.exitScenario(D));
ok(near(C.irrOf(b1x.pay, 1200000), sys.rows[0].eff, 0.01), 'NLMC.irrOf on basket 1 (all fixed, no forecast in it) = its effective rate ' + sys.rows[0].eff, C.irrOf(b1x.pay, 1200000).toFixed(3));
var sysx = G.mix(C.bmodel(E, 'offer').tr.map(function (t) { return C.eng(t); }), R.exitScenario(D)), ourIrr = C.irrOf(sysx.pay, 1200000);
ok(ourIrr < sys.irr - 0.3, 'our IRR of the system mix on the Research forecast (' + ourIrr.toFixed(2) + '%) is far below the published ' + sys.irr.toFixed(2) + '%: so row 7 is never recomputed');
ok(E.b.b1.irr === null && E.b.offer.fees === null, 'no invented figures: row 7 of the uniform baskets and row 11 stay empty');
ok(RE.counts.red === 0 && RE.counts.amber === 2, 'the example: no red flag, two to check (row 6 margin missing, eligibility not checked)', JSON.stringify(RE.counts));

/* 1. validity */
console.log('\n1. validity (451 s.4c: 24 days, 12 without a new lien)');
var s1 = ex(); s1.h.date = '7.10.2026'; var r1 = run(s1);
ok(one(r1, 1, 'red') && /31\.10\.2026/.test(one(r1, 1).you), 'approval of 7.10.2026: expired on 31.10.2026, red', one(r1, 1).you);
s1.h.date = '15.10.2026'; r1 = run(s1);
ok(one(r1, 1, 'amber') && r1.valid.left === 2, '15.10.2026: 2 days left, amber', r1.valid.left);
ok(one(RE, 1, 'info') && RE.valid.left === 19 && RE.valid.exp === '2026-11-25', 'the example (1.11.2026): 19 days left, until 25.11.2026, info', RE.valid.exp);
s1.h.date = '1.11.2026'; s1.h.lien = 'no'; r1 = run(s1);
ok(r1.valid.days === 12 && r1.valid.left === 7, 'no new lien: 12 days, 7 left', r1.valid.left);
s1.h.date = '20.11.2026'; r1 = run(s1);
ok(isNa(r1, 1), 'a date after today is not checked');
s1.h.date = '31.2.2026'; r1 = run(s1);
ok(r1.err['h.date'] && isNa(r1, 1), 'an impossible date (31.2) is a field error, and the check does not run');

/* 2. completeness */
console.log('\n2. the four baskets');
var s2 = C.blank(); s2.h.loan = 1000000; s2.b.offer.first = 6000; var r2 = run(s2);
ok(one(r2, 2, 'red') && /סל אחיד 1, סל אחיד 2, סל אחיד 3/.test(one(r2, 2).you), 'only the proposed basket typed: red, the three uniform baskets named');
ok(one(RE, 2, 'info'), 'the example: all four, info');

/* 3. the uniform basket form */
console.log('\n3. the uniform baskets against their definition');
var s3 = ex(); s3.b.b1.term = 270; s3.b.b1.tracks.forEach(function (t) { t.months = 270; }); var r3 = run(s3);
ok(one(r3, 3, 'amber') && /270/.test(one(r3, 3).you), 'basket 1 for 270 months (not 10/15/20/25/30 years): amber');
s3 = ex(); s3.b.b2.tracks[0].amount = 600000; s3.b.b2.tracks[1].amount = 200000; r3 = run(s3);
ok(one(r3, 3, 'amber') && /סל אחיד 2/.test(one(r3, 3).you), 'basket 2 not in thirds: amber');
ok(one(RE, 3, 'info'), 'the example: info');

/* 4. totals */
console.log('\n4. the totals');
var s4 = ex(); s4.b.offer.tracks[0].amount += 50000; var r4 = run(s4);
ok(one(r4, 4, 'red') && /1,250,000/.test(one(r4, 4, 'red').you), 'tracks of the proposed basket add up to 1,250,000 against 1,200,000: red');
s4 = ex(); s4.c.equity = 350000; r4 = run(s4);
ok(F(r4, 4, 'red').some(function (f) { return /50,000/.test(f.you); }), 'loan 1,200,000 + equity 350,000 < price 1,600,000: red, 50,000 missing');
ok(F(RE, 4, 'info').some(function (f) { return /נשארים 50,000/.test(f.you); }), 'the example: 50,000 left over for tax and lawyer, info');

/* 5. LTV */
console.log('\n5. financing share (329)');
var s5 = ex(); s5.h.loan = 1300000; var r5 = run(s5);
ok(one(r5, 5, 'red') && /81\.3%/.test(one(r5, 5).you), '1,300,000 on 1,600,000 for a single home: 81.3%, red', one(r5, 5).you);
s5 = ex(); s5.h.buyer = 'replace'; s5.h.loan = 1150000; r5 = run(s5);
ok(one(r5, 5, 'red') && /70%/.test(one(r5, 5).you), 'replacement home, 71.9% over 70%: red');
ok(one(RE, 5, 'info') && /בדיוק במגבלה/.test(one(RE, 5).you), 'the example: exactly at 75%, info');
s5 = ex(); s5.h.buyer = 'reduced'; s5.c.equity = 80000; r5 = run(s5);
ok(F(r5, 5, 'amber').length === 1, 'reduced price, equity 80,000 (between 60,000 and 100,000): amber');
s5.c.equity = 50000; r5 = run(s5);
ok(F(r5, 5, 'red').some(function (f) { return /50,000/.test(f.you); }), 'reduced price, equity 50,000: red');

/* 6. payment to income */
console.log('\n6. payment to income (329: 40% / 50%)');
var s6 = ex(); s6.c.income = 15000; var r6 = run(s6);
ok(one(r6, 6, 'red') && near(r6.pti, (6511 + 1200) / 15000, 0.001), '(6,511 + 1,200) / 15,000 = 51.4%: red', (100 * r6.pti).toFixed(1));
s6.c.income = 18000; r6 = run(s6);
ok(one(r6, 6, 'amber'), '42.8%: amber');
ok(one(RE, 6, 'info') && /32\.1%/.test(one(RE, 6).you), 'the example: 32.1%, info');
s6.c.income = null; r6 = run(s6);
ok(isNa(r6, 6), 'no income typed: not checked, never assumed');

/* 7. variable share */
console.log('\n7. at least one third fixed (329)');
var s7 = ex(); var o7 = s7.b.offer.tracks; o7[0].amount = 200000; o7[1].amount = 500000; o7[2].amount = 420000; o7[3].amount = 41000; o7[4].amount = 39000; var r7 = run(s7);
ok(one(r7, 7, 'red') && /הסל המוצע 80\.1%/.test(one(r7, 7).you), 'proposed basket 80.1% variable: red', one(r7, 7).you);
ok(!F(RE, 7, 'red').length && /סל אחיד 2 66\.7%/.test(one(RE, 7).you), 'basket 2 at exactly two thirds is not red');

/* 8. term */
console.log('\n8. term up to 30 years (329)');
var s8 = ex(); s8.b.offer.tracks[0].months = 372; var r8 = run(s8);
ok(one(r8, 8, 'red') && /372/.test(one(r8, 8).you), 'a 372-month track: red');
ok(one(RE, 8, 'info'), 'the example: 300 months, info');

/* 9. the overall rate against the bank's own average (קו המשווה) */
console.log('\n9. row 7 against the bank in קו המשווה');
var s9 = ex(); s9.h.bank = 'leumi'; s9.b.offer.irr = 5.2; var r9 = run(s9), lref = O.bankRef(D, 'leumi');
ok(one(r9, 9, 'info') && /גבוהה ב־0\.17% מהממוצע של בנק לאומי/.test(one(r9, 9).you), 'Leumi 5.20% vs its own ' + lref.irr.toFixed(2) + '%: 0.17% higher, info (never good or bad)', one(r9, 9).you);
ok(one(r9, 9).q.some(function (q) { return /אפשר לקבל הצעה מעודכנת/.test(q); }), 'and a question for the bank');

/* 10. rate per track against the averages */
console.log('\n10. each track against the Bank of Israel averages');
var s10 = ex(); s10.h.bank = 'leumi'; s10.b.offer.tracks[0].rate = 5.2; var r10 = run(s10), t10 = r10.t10.rows[0];
var nomL = O.ef2nom(lref.row.fixed_nl.rate), gap = G.pmt(368000, 5.2 / 1200, 300) - G.pmt(368000, Math.round(nomL * 100) / 100 / 1200, 300);
ok(one(r10, 10, 'amber') && near(t10.c.payGap, gap, 0.01), 'fixed not linked 5.20% at Leumi: amber, the monthly gap = Spitzer difference (' + gap.toFixed(0) + ' ILS)', t10.c.payGap.toFixed(2));
ok(t10.tb && t10.tb.nom === D.term.nl.buckets.filter(function (b) { return b.from === 20; })[0].nom, 'the term-file average for 25 years is shown beside it', t10.tb && t10.tb.nom);

/* 11. across banks (NLMO.normalize / compare) */
console.log('\n11. the same basket in another approval');
var s11 = ex(); s11.o = [C.blankOther()]; s11.o[0].bank = 'discount'; s11.o[0].loan = 1200000;
['b1', 'b2', 'b3'].forEach(function (k) { var b = s11.b[k]; s11.o[0].b[k] = { term: 300, irr: null, first: b.first - 40, max: b.max - 40, maxM: null, total: b.total - 12000, fees: null, tracks: [] }; });
var r11 = run(s11);
ok(one(r11, 11, 'info') && /בנק דיסקונט זול יותר, 12,000 ₪ פחות/.test(one(r11, 11).you), 'Discount 12,000 ILS cheaper over the loan in each basket: named, with the gap', one(r11, 11).you.slice(0, 70));
ok(isNa(RE, 11), 'the example (no other approval): not checked');

/* 12. recompute rows 8 to 10 */
console.log('\n12. recompute of rows 8 to 10');
ok(one(RE, 12, 'info') && /זהה/.test(one(RE, 12).you), 'the example: our numbers equal the typed ones');
var s12 = ex(); s12.b.offer.first = 7000; var r12 = run(s12);
ok(one(r12, 12, 'amber'), 'row 8 typed 7,000 against 6,511 computed (+7.5%): amber');

/* 13. highest payment, +1% and the 2022 replay */
console.log('\n13. the highest payment and the stress tests');
var bm = C.bmodel(E, 'offer'), st13 = C.stressMix(bm, D), rp = C.replayMix(bm, XR);
ok(st13.max > E.b.offer.max, '+1% on the variable tracks lifts the highest payment', st13.max.toFixed(0) + ' > ' + E.b.offer.max);
ok(rp && rp.peak > rp.first && rp.m >= 1 && rp.m <= 15, 'the 2022 path: a peak inside the 15 months', rp && rp.peak.toFixed(0) + ' in month ' + rp.m);
var s13 = ex(); s13.c.income = 16000; var r13 = run(s13);
ok(one(r13, 13, 'amber'), 'income 16,000: a stress peak passes 50%, amber');

/* 14. fees and a reservation fee */
console.log('\n14. charges and fees (row 11; 451 s.8)');
var s14 = ex(); s14.h.resv = 'yes'; var r14 = run(s14);
ok(one(r14, 14, 'red'), 'a reservation or option fee: red');
s14 = ex(); s14.b.offer.fees = 9000; s14.b.b1.fees = 3000; r14 = run(s14);
ok(one(r14, 14, 'info') && r14.qs.some(function (q) { return /גבוהים ב־6,000 ₪ מהסלים האחידים/.test(q); }), 'proposed basket fees 6,000 above the uniform ones: a question');
ok(isNa(RE, 14), 'the example (row 11 empty): not checked');

/* 15. file opening fee */
console.log('\n15. file opening fee');
ok(one(RE, 15, 'info') && /360/.test(one(RE, 15).rule) && /כל זכות/.test(one(RE, 15).rule), 'info, the 360 ILS figure attributed to Kol Zchut and called unsourced');

/* 16. early repayment */
console.log('\n16. early repayment (the Banking Order)');
var f16 = C.feeAt(bm, D, 84), drop = Math.round((D.policy.rate - D.forecast.rate_q3_2027) * 100) / 100;
var ex16 = R.exitAt(bm.tr.map(function (t) { return C.eng(t); }), D, R.exitScenario(D), 7, drop);
ok(near(f16.cap, ex16.fee, 0.01), 'fee in 7 years equals NLMR.exitAt (mexit) on the same rows', f16.cap.toFixed(2) + ' = ' + ex16.fee.toFixed(2));
ok(one(RE, 16) && /עמלת היוון צפויה של כ־5,153/.test(one(RE, 16).you), 'the example: about 5,153 ILS at year 7', one(RE, 16).you.slice(0, 60));
var tY = { k: 'var_nl', kind: 'var5', linked: false, method: 'spitzer', freq: 12 };
ok(C.capFee(tY, 30, 500000, 6, 300, D, 0).why === 'yearly', 'a variable track changing every year: no capitalization fee');
var t24 = { k: 'var_nl', kind: 'var5', linked: false, method: 'spitzer', freq: 24 }, f24 = C.capFee(t24, 30, 500000, 6, 300, D, 0.5), f60 = C.capFee({ k: 'var_nl', kind: 'var5', linked: false, method: 'spitzer', freq: 60 }, 30, 500000, 6, 300, D, 0.5);
ok(f24.cap > 0 && f24.cap < f60.cap, 'every 2 years: a fee to the change in month 49 only, smaller than every 5 years (month 61); averages 0.5% lower on the day', f24.cap.toFixed(0) + ' < ' + f60.cap.toFixed(0));
var s16 = ex(); s16.b.offer.tracks[1].pp = 'yes'; var r16 = run(s16);
ok(one(r16, 16, 'amber') && /בפריים/.test(one(r16, 16).you), 'row 12 says "yes" on prime: amber');
s16 = ex(); s16.c.hz = 30; r16 = run(s16);
ok(/כבר נפרעה/.test(one(r16, 16).you), 'exit after the end: no fee');

/* 17. balloon, bullet, grace */
console.log('\n17. balloon, bullet, grace');
var s17 = ex(); s17.b.offer.tracks[0].method = 'balloon'; s17.b.offer.tracks[1].grace = 24; var r17 = run(s17);
var lump = r17.RC.offer.X.T[0].lump;
ok(one(r17, 17, 'amber') && lump > 368000 && new RegExp(O.grp(lump)).test(one(r17, 17).you), 'balloon: the lump sum and its month shown (' + O.grp(lump) + ')');
ok(/גרייס חלקי ל־24 חודשים/.test(one(r17, 17).you), 'grace of 24 months shown');

/* 18. CPI linkage */
console.log('\n18. linkage');
ok(one(RE, 18) && /7\.8%/.test(one(RE, 18).you) && /94,000/.test(one(RE, 18).you), 'the example: 7.8% linked, 94,000 ILS');

/* 19. the variable mechanism */
console.log('\n19. the variable rate mechanism (row 6)');
ok(one(RE, 19, 'amber') && /משתנה לא צמודה: חסר המרווח/.test(one(RE, 19).you), 'the example: margin missing on variable not linked, amber');
var s19 = ex(); s19.b.offer.tracks[2].margin = 0.9; s19.b.offer.tracks[1].rate = 4.5; var r19 = run(s19);
ok(one(r19, 19, 'amber') && /פריים: הריבית 4\.50%/.test(one(r19, 19).you), 'prime 4.50% while prime minus 0.68 is 4.07%: amber');

/* 20. guarantors */
console.log('\n20. guarantors');
var s20 = ex(); s20.h.guar = 'yes'; var r20 = run(s20);
ok(one(r20, 20, 'amber') && one(r20, 20).q.length === 2, 'guarantors required: amber with two questions');
s20.h.guar = ''; r20 = run(s20); ok(isNa(r20, 20), 'not marked: not checked');

/* 21. insurance */
console.log('\n21. insurance rights (451 s.11)');
var s21 = ex(); s21.h.newb = 'new'; s21.h.delivery = '6.2028'; var r21 = run(s21);
ok(/14 ימים/.test(one(r21, 21).rule) && /לפני מועד המסירה שבחוזה, 6\.2028/.test(one(r21, 21).rule), 'external insurance in 14 days; a new home: not before delivery 6.2028');

/* 22. full monthly cost (NLMQ.fullCost) */
console.log('\n22. the full monthly cost');
ok(/לא הוקלדו/.test(one(RE, 22).you), 'no quotes typed: says so, no number invented');
var s22 = ex(); s22.c.life = 150; s22.c.struct = 40; var r22 = run(s22), fc = Q.fullCost(6511, 190, 0);
ok(new RegExp(O.grp(fc.total) + ' ₪ בחודש').test(one(r22, 22).you), 'payment 6,511 + 190 insurance = ' + O.grp(fc.total) + ' (NLMQ.fullCost)');

/* 23, 27, 28. general information */
console.log('\n23, 27, 28. appraisal, before paying, credit report');
ok(one(RE, 23) && /90/.test(one(RE, 23).rule), 'appraisal: reuse within 90 days');
ok(one(RE, 27) && /למספר שנשמר מראש/.test(one(RE, 27).rule), 'payment instructions: confirm by phone to a saved number');
ok(one(RE, 28) && /בחינם/.test(one(RE, 28).rule), 'one free credit data report a year');

/* 24. eligibility */
console.log('\n24. eligibility');
ok(one(RE, 24, 'amber'), 'not checked: amber');
var s24 = ex(); s24.c.elig = 'yes'; var r24 = run(s24);
ok(one(r24, 24, 'amber') && /אין מסלול של הלוואת זכאות/.test(one(r24, 24).you), 'eligible, but no eligibility track in the proposed basket: amber');
s24.c.elig = ''; r24 = run(s24); ok(isNa(r24, 24), 'not answered: not checked');

/* 25. a new home from a developer */
console.log('\n25. new home timeline');
var s25 = ex(); s25.h.newb = 'new'; s25.h.delivery = '6.2028'; s25.b.offer.tracks.forEach(function (t) { t.grace = 12; }); var r25 = run(s25);
ok(one(r25, 25) && /בעוד 19 חודשים/.test(one(r25, 25).you) && /שנגמר 7 חודשים לפני המסירה/.test(one(r25, 25).you), 'delivery 6.2028 is 19 months after 11.2026; a 12-month grace ends 7 months before', one(r25, 25).you);

/* 26. mode 2: the final documents against the approval */
console.log('\n26. the final documents against the approval');
var s26 = ex(); s26.mode = 'fin'; s26.f = { date: '20.11.2026', loan: 1200000, guar: 'no', fees: null, ins: 'no', tracks: JSON.parse(JSON.stringify(s26.b.offer.tracks)) };
var r26 = run(s26);
ok(one(r26, 26, 'info') && r26.counts.red === 0, 'the same tracks: no change found');
s26.f.tracks[0].rate = 4.9; s26.f.tracks[2].amount = 400000; s26.f.loan = 1180000; s26.f.ins = 'yes'; s26.f.tracks.push(C.blankTrack('prime', { amount: 20000, months: 300, rate: 4.2 }));
r26 = run(s26);
ok(F(r26, 26, 'red').some(function (f) { return /הריבית עלתה/.test(f.title) && /4\.90%/.test(f.you); }), 'rate 4.62% -> 4.90%: red');
ok(F(r26, 26, 'amber').some(function (f) { return /הסכום במסלול השתנה/.test(f.title); }), 'a smaller track amount: amber');
ok(F(r26, 26, 'red').some(function (f) { return /דרישת ביטוח חדשה/.test(f.title); }), 'a new insurance requirement: red');
ok(F(r26, 26, 'red').some(function (f) { return /מסלול חדש/.test(f.title); }), 'a second prime track not in the approval: red');
s26.f.tracks.splice(4, 1); s26.f.date = '28.11.2026'; r26 = run(s26);
ok(F(r26, 26, 'red').some(function (f) { return /מסלול חסר/.test(f.title); }) && F(r26, 26, 'amber').some(function (f) { return /אחרי תקופת השמירה/.test(f.title); }), 'a track left out: red; documents of 28.11 after the hold (25.11): amber');
ok(r26.sum.length >= 4 && /שינויים/.test(r26.sum.join(' ')), 'mode 2 has its own summary', r26.sum.length + ' sentences');

/* the wording rules */
console.log('\nwording: the summary, recommendation words, long dashes, fake zeros');
ok(RE.sum.length >= 5 && RE.sum.length <= 8, 'the example summary has 5 to 8 sentences', RE.sum.length);
var states = [RE, r1, r2, r4, r5, r6, r7, r9, r10, r11, r12, r13, r14, r16, r17, r19, r20, r21, r22, r24, r25, r26, run(C.blank())];
var bad = states.filter(function (r) { return /כדאי|המלצה|מומלץ|ממליצ|עדיף|כדאי לבחור/.test(allText(r)); });
ok(bad.length === 0, 'no recommendation word in any flag, summary or question (' + states.length + ' cases)');
ok(states.every(function (r) { return !/[–—]/.test(allText(r) + C.text(r, r.st, TODAY)); }), 'no long dash in any string or copied text');
var src = fs.readFileSync(path.join(INS, 'tools/mcheck.js'), 'utf8');
ok(!/[–—]/.test(src) && !/כדאי|המלצה|מומלץ|ממליצ|סימולציה|ממשק|מודל|דמו\b/.test(src) && !/\bAI\b/.test(src), 'and none in the source file, nor the banned words');
var zero = /(^|[^\d.,])0 ₪|₪\s?0(?![\d.,])/;
var s0 = C.blank(); s0.h.date = '2.11.2026'; s0.h.loan = 900000; var r0 = run(s0);
ok(!zero.test(allText(r0)) && !zero.test(allText(RE)) && !zero.test(C.text(RE, RE.st, TODAY)), 'no "0 ₪" shown for a value nobody typed (a bare approval, the example, the copied text)');
ok(r0.na.length >= 10, 'a bare approval lists what cannot be checked yet', r0.na.length + ' checks');
var rb = run(C.blank());
ok(rb.empty && rb.flags.length === 0 && rb.sum.length === 0, 'the empty state: no flag, no summary');
var txt = C.text(RE, RE.st, TODAY);
ok(/מה לשאול את הבנק:/.test(txt) && /אינה ייעוץ/.test(txt) && RE.qs.length >= 8, 'the copied text carries the summary, the flags and ' + RE.qs.length + ' questions');

/* the case link (#mcheck=...) */
console.log('\nthe case link');
var back = C.restore(JSON.parse(JSON.stringify(E))), rr = run(back);
ok(JSON.stringify(rr.counts) === JSON.stringify(RE.counts) && rr.sum.join() === RE.sum.join(), 'a restored case gives the same result');
var junk = C.restore({ h: { loan: 'abc', bank: 5 }, b: { offer: { tracks: [{ k: 'evil', amount: 100000 }] } }, mode: 'x' });
ok(junk.h.loan === null && junk.h.bank === '' && junk.b.offer.tracks[0].k === 'fixed_nl' && junk.mode === 'ap', 'a broken hash is cleaned, unknown values dropped');
var sv = ex(); sv.b.offer.irr = 25; var rv = run(sv);
ok(rv.err['b.offer.irr'] && !/25\.00%/.test(allText(rv)), 'an out-of-range rate (25%) is a field error and is not used in any check');

console.log('\n' + (n - fails) + '/' + n + ' passed' + (fails ? ', ' + fails + ' FAILED' : ''));
process.exit(fails ? 1 : 0);
