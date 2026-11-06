/* HAD-675 round H · node test of mkeys ("מהחוזה למפתח"). Run from anywhere:
     node docs/research/2026-11-05-mortgage-world/build/round-h/test_mkeys.js
   Loads the repo files tools/indexation.js (NLIX), tools/mquick.js (NLMQ) and tools/mkeys.js (NLMK) with a fake window and feeds
   the two real data files (data/boi-mortgage.json, data/cbs-200010.json). Every expected number is recomputed here from the data,
   independently of NLMK (the rate from by_bank, the balance from the draws). Exit code 1 on a failure. */
'use strict';
var path = require('path');
var HERE = __dirname, REPO = path.resolve(HERE, '../../../../..');
var INS = path.join(REPO, 'plugins/nadlan-config/assets/instruments');
global.window = {};
require(path.join(INS, 'tools/indexation.js'));
require(path.join(INS, 'tools/mquick.js'));
require(path.join(INS, 'tools/mkeys.js'));
var X = window.NLIX, Q = window.NLMQ, K = window.NLMK;
var D = require(path.join(INS, 'data/boi-mortgage.json'));
var C = require(path.join(INS, 'data/cbs-200010.json'));
var bb = D.by_bank, LAST = bb.months.length - 1;

var fails = 0, n = 0;
function ok(cond, name, got) { n++; if (cond) console.log('  ok   ' + name + (got != null ? '  [' + got + ']' : '')); else { fails++; console.log('  FAIL ' + name + (got != null ? '  [' + got + ']' : '')); } }
function near(a, b, tol) { return Math.abs(a - b) <= (tol == null ? 0.5 : tol); }
function strip(h) { return String(h).replace(/<[^>]+>/g, ''); }
function mDiff(a, b) { return (+b.slice(0, 4) - +a.slice(0, 4)) * 12 + (+b.slice(5, 7) - +a.slice(5, 7)); }
function base(o) { var v = { price: 2000000, equity: 600000, sign: '2026-11-06', delivery: '2029-11-06', plan: 'stages', grace: 'partial', years: 25, annual: null }; Object.keys(o || {}).forEach(function (k) { v[k] = o[k]; }); return v; }
function run(o) { return K.compute(base(o), D, C); }

/* the all-banks mix-weighted monthly rate, straight from the data */
var tot = 0, rm = 0; Q.TR.forEach(function (k) { tot += +bb.mix.system[k][LAST]; });
Q.TR.forEach(function (k) { rm += (+bb.mix.system[k][LAST] / tot) * (Math.pow(1 + bb.rate.system[k][LAST] / 100, 1 / 12) - 1); });
console.log('data: by_bank month ' + bb.months[LAST] + ', CBS 200010 latest ' + C.latest + ', trailing 12 months ' + (X.trailing(C) * 100).toFixed(3) + '%, all-banks monthly rate ' + (rm * 100).toFixed(4) + '%');

console.log('\n0. exposed API');
ok(typeof K.compute === 'function' && typeof K.rowText === 'function' && typeof K.headline === 'function', 'NLMK exposes compute, rowText, headline');
ok(Object.keys(X).join() === 'compute,knownKey,schedule,trailing', 'NLIX exposes compute, knownKey, schedule, trailing', Object.keys(X).join());
var R0 = K.rates(bb, 'system');
ok(near(R0.rm, rm, 1e-12), 'NLMK.rates(system).rm = the mix-weighted monthly rate from the data', (R0.rm * 100).toFixed(5) + '%');
ok(R0.month === bb.months[LAST], 'the rate month is the latest month of by_bank', R0.month);

console.log('\n(a) 20/80 signed after 7.7.2022: the first 20% has no linkage');
var a = run({ plan: 'end', equity: 400000 });
ok(a.newLaw === true, 'contract of 6.11.2026 falls under the new law');
ok(a.rows.length === 2 && a.rows[0].pct === 20 && a.rows[1].pct === 80, 'two payments: 20% at signing, 80% at delivery');
ok(a.rows[0].linked === 0 && a.rows[0].add === 0 && a.rows[0].exempt, 'the 20% at signing: linked part 0, linkage 0');
ok(/בלי הצמדה/.test(strip(K.rowText(a.rows[0], a))), 'its timeline row says "בלי הצמדה"', strip(K.rowText(a.rows[0], a)));
ok(near(a.rows[1].linked, 0.5 * 1600000, 1e-6), 'the 80% payment: half of it linked (800,000)', a.rows[1].linked);
ok(a.rows[1].add > 0 && !a.rows[1].known, 'the 80% payment carries a projected linkage', Math.round(a.rows[1].add));
var ar = X.compute({ price: 2e6, sign: '2026-11-06', delivery: '2029-11-06', share: 50, floor: true, rows: X.schedule('end', '2026-11-06', '2029-11-06') }, C, X.trailing(C));
ok(near(a.linkTotal, ar.total, 1e-9), 'the linkage total is exactly NLIX.compute (no law re-implemented)', Math.round(a.linkTotal));
var a2 = run({ plan: 'end', sign: '2021-05-10', delivery: '2024-05-10' });
ok(a2.newLaw === false && a2.rows[0].linked === a2.rows[0].amt, 'a contract of 10.5.2021 (old law): every payment linked in full, the upper bound', a2.rows[0].linked);

console.log('\n(b) equity covers every payment: no draws, no mortgage, and the headline says so');
var b = run({ equity: 2000000, annual: 0 });  // 6.11.2026: the known index is 9.2026 = the latest; 0% a year for the months ahead
ok(near(b.linkTotal, 0, 1e-9), 'index flat (0% a year, base = the latest index): linkage 0', b.linkTotal);
ok(b.drawn === 0 && b.noMortgage && b.pay === 0 && b.balance === 0, 'no draws, balance 0, payment 0');
var hb = K.headline(b);
ok(hb.value === 'לא צריך משכנתא' && hb.text === true && !/0 ₪/.test(hb.value), 'headline: "לא צריך משכנתא", not "0 ₪"', hb.value);
ok(/בלי משכנתא/.test(strip(K.keysText(b))), 'the keys row: "בלי משכנתא"', strip(K.keysText(b)));
ok(b.rows.every(function (x) { return x.draw === 0 && /מההון העצמי/.test(strip(K.rowText(x, b))); }), 'every row: "מההון העצמי"');
var bp = b.rows.filter(function (x) { return !x.exempt && !x.known; })[0];
ok(bp && /בלי תוספת הצמדה \(לפי השינוי שבחרתם במדד\)/.test(strip(K.rowText(bp, b))), 'a future row with a flat index: "לפי השינוי שבחרתם", not "המדד הידוע"', bp && strip(K.rowText(bp, b)));
var b2 = run({ equity: 2000000 });
ok(b2.drawn > 0 && near(b2.drawn, b2.linkTotal, 1e-6), 'equity = price with the default index change: only the linkage is drawn', Math.round(b2.drawn));

console.log('\n(c) partial grace: the monthly interest = the drawn balance x the monthly rate');
var c = run();
var sumI = 0, okRows = 0, rowsWith = 0;
c.rows.forEach(function (x) { var nn = mDiff(x.date, c.delivery); sumI += x.draw * rm * nn; if (x.cum > 0 && nn > 0) { rowsWith++; if (near(x.monthInt, x.cum * rm, 1e-6)) okRows++; } });
ok(rowsWith > 0 && okRows === rowsWith, 'each row before the keys: monthInt = cumulative draws x rate (' + okRows + '/' + rowsWith + ')');
ok(near(c.interest, sumI, 1e-6), 'interest until delivery = sum of draw x rate x months to the keys', Math.round(c.interest));
var c1 = c.rows.filter(function (x) { return x.cum > 0 && !x.atKeys; })[0];
ok(new RegExp(new Intl.NumberFormat('he-IL').format(Math.round(c1.cum * rm))).test(strip(K.rowText(c1, c))), 'the row prints that interest', strip(K.rowText(c1, c)));
ok(near(c.balance, c.drawn, 1e-9), 'partial: the balance at delivery = the sum of the draws', Math.round(c.balance));
var funded = c.rows.every(function (x) { return near(x.fromEq + x.draw, x.amt + x.add, 1e-6); });
ok(funded, 'every payment: from equity + drawn = amount + its linkage');
ok(near(c.eqUsed, 600000, 1e-6) && near(c.drawn + c.eqUsed, 2000000 + c.linkTotal, 1e-6), 'equity used up, draws + equity = price + linkage');
var fe = c.rows.map(function (x) { return x.fromEq; }), order = true;
for (var i = 1; i < fe.length; i++) if (fe[i] > 0.5 && c.rows[i - 1].draw > 0.5) order = false;
ok(order, 'equity first: no equity is spent after a draw began');

console.log('\n(d) full grace: the balance at delivery is above the sum of the draws');
var d = run({ grace: 'full' });
var bal = 0; d.rows.forEach(function (x) { bal += x.draw * Math.pow(1 + rm, mDiff(x.date, d.delivery)); });
ok(d.balance > d.drawn, 'balance ' + Math.round(d.balance) + ' > draws ' + Math.round(d.drawn));
ok(near(d.balance, bal, 1e-6), 'balance = sum of draw x (1 + rate)^months', Math.round(bal));
ok(near(d.interest, d.balance - d.drawn, 1e-9), 'capitalized interest = balance - draws', Math.round(d.interest));
var prev = d.rows.filter(function (x) { return !x.atKeys; }).pop(), lastRow = d.rows[d.rows.length - 1];
ok(near(prev.bal * Math.pow(1 + rm, mDiff(prev.date, lastRow.date)) + lastRow.draw, d.balance, 1e-6), 'the row balances roll forward to the balance at the keys');

console.log('\n(e) after the keys: balance x payPer1(system, ' + bb.months[LAST] + ', term), within 1 ILS');
[20, 25, 30].forEach(function (y) {
  ['partial', 'full'].forEach(function (g) {
    var r = run({ years: y, grace: g }), want = r.balance * Q.payPer1(bb, 'system', LAST, y);
    ok(near(r.pay, want, 1), g + ', ' + y + ' years: ' + Math.round(r.pay) + ' vs ' + Math.round(want));
  });
});
var im = run({ grace: 'immediate' });
ok(near(im.pay, im.drawn * Q.payPer1(bb, 'system', LAST, 25), 1), 'immediate: the full payment = the draws x payPer1 (each draw on its own schedule)', Math.round(im.pay));
ok(im.balance < im.drawn && near(im.interest, im.paidBefore - (im.drawn - im.balance), 1e-6), 'immediate: balance below the draws, interest = paid - principal repaid', Math.round(im.interest));
var cal = Q.payPer1(bb, 'system', LAST, 25) * 1e6;
ok(Math.round(cal) === 5428, 'calibration: 1,000,000 ILS / 25 years = 5,428 (as mquick)', cal.toFixed(2));

console.log('\n(f) the 75% flag (directive 329)');
var f1 = run({ equity: 400000 }), f2 = run({ equity: 600000 });
ok(f1.over75 === true && f1.share > 0.75, 'equity 400,000: ' + (f1.share * 100).toFixed(1) + '% flagged');
ok(/מעל 75%/.test(strip(K.ltvText(f1))) && /הוראה 329/.test(strip(K.ltvText(f1))), 'its line: "מעל 75% ... הוראה 329"', strip(K.ltvText(f1)));
ok(f2.over75 === false && f2.share <= 0.75, 'equity 600,000, partial: ' + (f2.share * 100).toFixed(1) + '% not flagged');
var f3 = run({ equity: 600000, grace: 'full' });
ok(f3.over75 === true, 'equity 600,000, full grace: the capitalized balance ' + (f3.share * 100).toFixed(1) + '% is flagged');

console.log('\nvalidation');
[[{ price: NaN }, 'price', 'מחיר'], [{ sign: '' }, 'sign', 'חתימת'], [{ delivery: '' }, 'delivery', 'המסירה'], [{ delivery: '2026-10-01' }, 'delivery', 'אחרי תאריך החתימה'],
  [{ equity: 2500000 }, 'equity', 'גבוה ממחיר'], [{ equity: '' }, 'equity', 'ההון העצמי'], [{ annual: NaN }, 'annual', 'שינוי שנתי'], [{ sign: '2009-05-01', delivery: '2012-01-01' }, 'sign', '2010']].forEach(function (t) {
  var r = run(t[0]); ok(r.error && r.error.field === t[1] && r.error.msg.indexOf(t[2]) > -1, JSON.stringify(t[0]) + ' -> ' + t[1], r.error && r.error.msg);
});

console.log('\nwording');
var all = [];
['partial', 'full', 'immediate'].forEach(function (g) { ['end', 'stages', 'thirds'].forEach(function (p) { [400000, 600000, 2000000].forEach(function (e) {
  var r = run({ grace: g, plan: p, equity: e }); all.push(strip(K.summary(r)), strip(K.ltvText(r)), strip(K.keysText(r)), K.copyText(r), K.headline(r).value);
  r.rows.forEach(function (x) { all.push(strip(K.rowText(x, r))); });
}); }); });
K.PLANS.concat(K.GRACE).forEach(function (x) { all.push(x.he); });
var txt = all.join('\n');
ok(!/[–—]/.test(txt), 'no long dashes in any generated text (' + all.length + ' strings)');
ok(!/\bAI\b|סימולציה|דמו|ממשק|אינטראקטיבי/.test(txt), 'no banned words');
ok(!/NaN|undefined|Infinity/.test(txt), 'no NaN, undefined or Infinity');

console.log('\nworked example (the opening values): 2,000,000 ILS, equity 600,000, signed 6.11.2026, delivery 6.11.2029, stages, 25 years');
['partial', 'full', 'immediate'].forEach(function (g) {
  var r = run({ grace: g });
  console.log('  ' + g + ': headline ' + Math.round(r.pay) + ' ILS/month · linkage ' + Math.round(r.linkTotal) + ' · interest until delivery ' + Math.round(r.interest)
    + (g === 'immediate' ? ' (paid ' + Math.round(r.paidBefore) + ')' : '') + ' · mortgage at delivery ' + Math.round(r.balance) + ' · share ' + (r.share * 100).toFixed(1) + '%');
});
console.log('  rows (partial):'); c.rows.forEach(function (x) { console.log('    ' + K.mmyyyy(x.date) + '  ' + strip(K.rowText(x, c))); });
console.log('    ' + K.mmyyyy(c.delivery) + '  ' + strip(K.keysText(c)));

console.log('\n' + (n - fails) + '/' + n + ' passed' + (fails ? ', ' + fails + ' FAILED' : ''));
process.exit(fails ? 1 : 0);
