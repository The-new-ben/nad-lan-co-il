/* test_mready.js (HAD-675): node test of the mready pure logic (window.NLMRD) and its data. Run from anywhere:
     node docs/research/2026-11-05-mortgage-world/build/mready/test_mready.js
   Loads the real afford.js (window.NLAF), mready.js, mready.json, the research data boi-mortgage-v2.json (ships as
   data/boi-mortgage.json), ptax.json and cost.json. Checks:
   1. the data: every document cites known sources with a URL and a retrieval time; the label rule holds (common = two
      independent groups and at least one bank, Kol Zchut or the Bank of Israel; otherwise "יש בנקים שמבקשים");
   2. the calibration: 1,000,000 over 25 years in the all-banks average mix = 5,428 a month (the same as mbudget);
   3. the three limits on the four ready cases and on edge cases (40% / 50% payment, LTV by buyer type, equity vs tax + lawyer);
   4. agreement with NLAF.compute: the highest price at 40% passes every limit, 5,000 more fails one;
   5. the personal list by profile (salaried, self employed, both, gift, sale, grant, oleh, foreign resident, contractor,
      second hand) and the per-borrower words;
   6. the text: score, ticks, no long dash, no spaced hyphen, no "₪0", no blacklisted or advice word in any visible string. */
'use strict';
var fs = require('fs'), path = require('path');
var HERE = __dirname, REPO = path.resolve(HERE, '../../../../..');
var INS = path.join(REPO, 'plugins/nadlan-config/assets/instruments');
global.window = global;
require(path.join(INS, 'tools/afford.js'));
require(path.join(HERE, 'mready.js'));
var NLMRD = global.NLMRD, NLAF = global.NLAF;
function J(p) { return JSON.parse(fs.readFileSync(p, 'utf8')); }
var M = J(path.join(HERE, 'mready.json'));
var D = { boim: J(path.join(REPO, 'docs/research/2026-11-05-mortgage-world/data/boi-mortgage-v2.json')), ptax: J(path.join(INS, 'data/ptax.json')), cost: J(path.join(INS, 'data/cost.json')), mready: M };
var fails = 0, n = 0;
function ok(c, msg) { n++; if (!c) { fails++; console.log('FAIL ' + msg); } }
function eq(a, b, msg, tol) { ok(Math.abs(a - b) <= (tol == null ? 0.5 : tol), msg + ' (got ' + a + ', want ' + b + ')'); }
function preset(k) { var p = M.presets.filter(function (x) { return x.key === k; })[0]; return Object.assign({ years: 25 }, p.set); }
function ids(list) { return list.map(function (d) { return d.id; }); }
function st(m, id) { return m.checks.filter(function (c) { return c.id === id; })[0].state; }

/* 1. the data */
var S = M.sources;
Object.keys(S).forEach(function (k) { ok(/^https:\/\//.test(S[k].url), 'source ' + k + ' url'); ok(/^2026-11-05T\d\d:\d\d:\d\dZ$/.test(S[k].retrieved), 'source ' + k + ' retrieved'); ok(!!S[k].group && !!S[k].org && !!S[k].title, 'source ' + k + ' fields'); });
var seen = {};
M.docs.forEach(function (d) {
  ok(!seen[d.id], 'unique id ' + d.id); seen[d.id] = 1;
  ok(d.stage === 'aip' || d.stage === 'loan', d.id + ' stage');
  d.src.forEach(function (s) { ok(!!S[s], d.id + ' cites unknown ' + s); });
  var groups = {}, official = false; d.src.forEach(function (s) { groups[S[s].group] = 1; if (S[s].kind !== 'press') official = true; });
  var want = Object.keys(groups).length >= 2 && official ? 'common' : 'some';
  ok(d.level === want, d.id + ' level ' + d.level + ' should be ' + want);
});
['valid_src', 'free_src', 'docs_optional_src', 'based_on_src'].forEach(function (k) { M.aip[k].forEach(function (s) { ok(!!S[s], 'aip ' + k + ' ' + s); }); });
ok(M.aip.valid_days === 24, 'approval valid 24 days');
// the snapshot of the rules equals the research data
var R = D.boim.rules; ok(JSON.stringify(R.ltv) === JSON.stringify(M.rules.ltv) && R.pti_max === M.rules.pti_max && R.pti_risk === M.rules.pti_risk, 'rules snapshot = boi-mortgage-v2.json rules');

/* 2. the calibration */
var pm = NLMRD.perMillion(D.boim, 300);
eq(pm.perM, 5428, 'all-banks mix 1,000,000 / 25 years', 0.5); ok(pm.basis === 'mix' && pm.month === D.boim.by_bank.latest.month, 'mix basis and month');
eq(NLMRD.pmt(1e6, NLMRD.eqRate(pm.perM, 300) / 1200, 300), pm.perM, 'equivalent rate reproduces the payment', 0.01);
var pmFallback = NLMRD.perMillion({ rates: { fixed_nl: { rate: 4.62, hist: [['2026-08', 4.62]] } } }, 300);
ok(pmFallback.basis === 'fixed' && pmFallback.month === '2026-08', 'fallback without by_bank');

/* 3. the limits */
var m1 = NLMRD.model(preset('couple'), D);
eq(m1.equity, 720000, 'couple equity'); eq(m1.ltv, 0.75, 'couple ltv');
eq(m1.tax, (2300000 - 1978745) * 0.035, 'couple purchase tax');
eq(m1.lawyer, 0.005 * 1.18 * 2300000, 'couple lawyer with VAT');
eq(m1.loan, 2300000 + m1.tax + m1.lawyer - 720000, 'couple loan');
eq(m1.payment, m1.loan * pm.perM / 1e6, 'couple first payment');
eq(m1.pti, m1.payment / (24000 - 1200), 'couple payment to disposable income', 1e-9);
ok(st(m1, 'pti') === 'pass' && m1.pti < 0.4, 'couple pti pass under 40% (' + (100 * m1.pti).toFixed(1) + '%)');
ok(st(m1, 'ltv') === 'pass' && st(m1, 'equity') === 'pass', 'couple ltv and equity pass');

var m2 = NLMRD.model(preset('upgrade'), D);
eq(m2.ltv, 0.7, 'replacement home ltv 70%'); ok(m2.k === 'single', 'replacement home pays single-home brackets');
ok(m2.checks.every(function (c) { return c.state === 'pass'; }), 'upgrade all pass');

var m3 = NLMRD.model(preset('oleh'), D);
ok(m3.tax === 0, 'oleh under the first bracket pays no purchase tax'); eq(m3.ltv, 0.75, 'oleh ltv');
ok(st(m3, 'pti') === 'warn' && m3.pti > 0.4 && m3.pti <= 0.5, 'oleh pti between 40% and 50% (' + (100 * m3.pti).toFixed(1) + '%)');

var m4 = NLMRD.model(preset('foreign'), D);
eq(m4.ltv, 0.5, 'foreign ltv 50%'); eq(m4.tax, 0.08 * 3200000, 'foreign tax 8%');
ok(st(m4, 'ltv') === 'pass' && st(m4, 'equity') === 'fail', 'foreign: down payment covered, tax and lawyer not');
eq(m4.checks[2].short, 1600000 + m4.tax + m4.lawyer - 1800000, 'foreign equity gap');
eq(m4.loan, 1600000, 'foreign loan capped at 50%');

var m5 = NLMRD.model(Object.assign(preset('couple'), { income: 15000 }), D);
ok(st(m5, 'pti') === 'fail' && m5.pti > 0.5, 'pti above 50% fails');
var m6 = NLMRD.model(Object.assign(preset('couple'), { savings: 300000, gift: 0 }), D);
ok(st(m6, 'ltv') === 'fail' && st(m6, 'equity') === 'fail', 'equity under the down payment fails ltv and equity');
eq(m6.checks[1].short, 575000 - 300000, 'ltv gap = down payment less equity');
var m7 = NLMRD.model(Object.assign(preset('couple'), { buyer: 'extra' }), D);
eq(m7.ltv, 0.5, 'additional home ltv 50%'); eq(m7.tax, 0.08 * 2300000, 'additional home tax 8%'); ok(st(m7, 'ltv') === 'fail', 'additional home with 720,000 fails the 50% cap');
var m8 = NLMRD.model(Object.assign(preset('couple'), { savings: 3000000, gift: 0 }), D);
ok(m8.loan === 0 && m8.checks[0].none && st(m8, 'pti') === 'pass', 'no mortgage needed');
var m9 = NLMRD.model(Object.assign(preset('couple'), { loans: 30000 }), D);
ok(st(m9, 'pti') === 'fail' && !isFinite(m9.pti), 'loans above income fail');

/* 4. agreement with NLAF.compute */
[preset('couple'), preset('upgrade'), preset('oleh'), Object.assign(preset('foreign'), { savings: 2200000 })].forEach(function (inp, i) {
  var m = NLMRD.model(inp, D); ok(m.max[40] > 0 && m.max[50] >= m.max[40], 'case ' + i + ' max prices');
  var a = NLMRD.model(Object.assign({}, inp, { price: m.max[40] }), D);
  ok(a.checks.every(function (c) { return c.state === 'pass'; }), 'case ' + i + ': the 40% max price ' + m.max[40] + ' passes every limit (' + a.checks.map(function (c) { return c.state; }).join(',') + ')');
  var b = NLMRD.model(Object.assign({}, inp, { price: m.max[40] + 5000 }), D);
  ok(b.checks.some(function (c) { return c.state !== 'pass'; }), 'case ' + i + ': 5,000 above the 40% max fails one limit');
  var c50 = NLMRD.model(Object.assign({}, inp, { price: m.max[50] }), D);
  ok(c50.checks.every(function (c) { return c.state !== 'fail'; }), 'case ' + i + ': the 50% max price is within the cap');
});

/* 5. the personal list */
var L1 = NLMRD.docsFor(preset('couple'), M), I1 = ids(L1);
['id_il', 'app_form', 'bank3', 'pay3', 'f106', 'loans_report', 'savings_proof', 'gift_trail', 'gift_letter', 'elig_opt', 'contract', 'tabu', 'appraisal', 'insurance', 'dev_commit', 'salelaw', 'vouchers'].forEach(function (x) { ok(I1.indexOf(x) > -1, 'couple has ' + x); });
['id_foreign', 'tax_assess', 'cpa', 'sale_contract', 'oleh_cert', 'elig', 'seller_commit', 'warn_notes', 'foreign_income'].forEach(function (x) { ok(I1.indexOf(x) < 0, 'couple has no ' + x); });
ok(L1.filter(function (d) { return d.id === 'pay3'; })[0].per === 'לכל אחד מהלווים', 'two salaried borrowers: per borrower');
ok(L1.filter(function (d) { return d.id === 'gift_letter'; })[0].some, 'gift letter is "some" (no bank list states it)');
var L2 = NLMRD.docsFor(preset('upgrade'), M), I2 = ids(L2);
ok(L2.filter(function (d) { return d.id === 'pay3'; })[0].per === 'ללווה השכיר' && L2.filter(function (d) { return d.id === 'tax_assess'; })[0].per === 'ללווה העצמאי', 'both incomes: per salaried and per self employed');
['sale_contract', 'old_mortgage', 'cpa', 'seller_commit', 'warn_notes', 'pledges_seller', 'seller_lien'].forEach(function (x) { ok(I2.indexOf(x) > -1, 'upgrade has ' + x); });
['dev_commit', 'vouchers', 'loans_report', 'gift_trail', 'elig_opt'].forEach(function (x) { ok(I2.indexOf(x) < 0, 'upgrade has no ' + x); });
var L3 = NLMRD.docsFor(preset('oleh'), M), I3 = ids(L3);
['oleh_cert', 'elig', 'elig_docs', 'id_il'].forEach(function (x) { ok(I3.indexOf(x) > -1, 'oleh has ' + x); });
ok(L3.every(function (d) { return !d.per; }), 'one borrower: no per-borrower words');
var L4 = NLMRD.docsFor(preset('foreign'), M), I4 = ids(L4);
['id_foreign', 'foreign_income', 'foreign_tax', 'foreign_transl', 'foreign_poa', 'foreign_visa'].forEach(function (x) { ok(I4.indexOf(x) > -1, 'foreign has ' + x); });
['id_il', 'elig_opt', 'elig', 'oleh_cert'].forEach(function (x) { ok(I4.indexOf(x) < 0, 'foreign has no ' + x); });
var I5 = ids(NLMRD.docsFor(Object.assign(preset('couple'), { type: 'self', grant: 50000 }), M));
['tax_assess', 'cpa', 'vat', 'elig', 'elig_docs'].forEach(function (x) { ok(I5.indexOf(x) > -1, 'self employed with a grant has ' + x); });
['pay3', 'f106', 'prev_job', 'ctrl', 'elig_opt'].forEach(function (x) { ok(I5.indexOf(x) < 0, 'self employed with a grant has no ' + x); });
var I6 = ids(NLMRD.docsFor(Object.assign(preset('couple'), { loans: 0 }), M));
ok(I6.indexOf('loans_report') < 0, 'no existing loans: no balances report');

/* 6. the text */
var dc0 = NLMRD.docsCheck(L1, {}); ok(dc0.state === 'todo' && dc0.done === 0 && dc0.total === 8, 'couple: 8 core documents, none ticked (' + dc0.total + ')');
ok(NLMRD.score(m1, dc0) === 3, 'couple example scores 3 of 4 (design board)');
var all = {}; L1.forEach(function (d) { if (d.core) all[d.id] = 1; });
var dc1 = NLMRD.docsCheck(L1, all); ok(dc1.state === 'done' && NLMRD.score(m1, dc1) === 4, 'all core documents ticked: 4 of 4');
ok(NLMRD.score(m4, dc0) === 2, 'foreign case scores 2 of 4');
var T = NLMRD.copyText(preset('couple'), m1, L1, { id_il: 1 }, M);
ok(/3 מתוך 4/.test(T) && /\[x\] תעודת זהות עם הספח/.test(T) && /\[ \] דפי חשבון/.test(T), 'copied text: score and ticks');
ok(T.indexOf(NLMRD.STATE.pass) > -1 && T.indexOf('לאישור העקרוני:') > -1 && T.indexOf('למשכנתא עצמה, אחרי האישור:') > -1, 'copied text: both stages');
var LONG = /[\u2013\u2014]/, SPACED = / - /, ZERO = /₪0(?![\d,])/;
var BLACK = ['ממשק', 'דמו', 'הדגמה', 'מנגנון', 'שכבה', 'אינטראקטיב', 'סימולציה', 'טכנולוגיה', 'המערכת', 'הפלטפורמה', 'בקרוב', 'בבדיקה', 'פיילוט', 'פרוטוטייפ', 'אטלס', 'מומלץ', 'כדאי', 'ממליצים', 'עדיף', 'רספונסיבי'];
function clean(s, where) { ok(!LONG.test(s), where + ': long dash'); ok(!SPACED.test(s), where + ': spaced hyphen'); ok(!ZERO.test(s), where + ': ₪0'); BLACK.forEach(function (w) { ok(s.indexOf(w) < 0, where + ': word ' + w); }); }
clean(T, 'copied text');
[m1, m2, m3, m4, m5, m6, m8, m9].forEach(function (m, i) { m.checks.forEach(function (c) { clean(NLMRD.checkText(c, m), 'check text ' + i + ' ' + c.id); }); });
M.docs.forEach(function (d) { clean(d.text + ' ' + (d.cond || ''), 'doc ' + d.id); });
['aip', 'loan'].forEach(function (k) { clean(M.stages[k].label + ' ' + M.stages[k].lede, 'stage ' + k); });
M.presets.forEach(function (p) { clean(p.label + ' ' + p.sub, 'preset ' + p.key); });
// every Hebrew string literal in mready.js
var src = fs.readFileSync(path.join(HERE, 'mready.js'), 'utf8').replace(/\/\*[\s\S]*?\*\//g, '').replace(/\/\/[^\n]*/g, '');
(src.match(/'[^'\n]*[\u0590-\u05FF][^'\n]*'/g) || []).forEach(function (s) { clean(s, 'mready.js ' + s.slice(0, 40)); });

console.log((fails ? 'FAILED ' + fails : 'OK') + ' · ' + n + ' checks · couple pti ' + (100 * m1.pti).toFixed(1) + '%, max at 40% ' + m1.max[40] + ', at 50% ' + m1.max[50] + ' · foreign gap ' + Math.round(m4.checks[2].short));
process.exit(fails ? 1 : 0);
