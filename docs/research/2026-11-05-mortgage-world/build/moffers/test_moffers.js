/* Tests for moffers.js (HAD-675). Run: node test_moffers.js [path/to/boi-mortgage.json]
   Pure logic only (window.NLMO): normalization, the cheapest per basket, the gaps, the bank averages and their place among the
   five large banks, and the negotiation text (only typed or official numbers, no advice wording, no long dash). */
'use strict';
var fs = require('fs'), path = require('path'), assert = require('assert');
global.window = {};
require('./moffers.js');
var M = window.NLMO;
var dataPath = process.argv[2] || path.join(__dirname, '..', '..', 'data', 'boi-mortgage-v2.json');
var D = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
var n = 0, fail = 0;
function t(name, fn) { n++; try { fn(); console.log('ok   ' + name); } catch (e) { fail++; console.log('FAIL ' + name + '\n     ' + e.message); } }
function near(a, b, eps, msg) { assert.ok(Math.abs(a - b) <= (eps || 1e-9), (msg || '') + ' expected ' + b + ' got ' + a); }
function offer(loan, years, b1, b2, b3, bank) {
  var e = function (x) { return x ? { irr: x[0], total: x[1], maxPay: x[2], first: x[3] } : { irr: null, total: null, maxPay: null, first: null }; };
  return { bank: bank || '', loan: loan, years: years, b: { b1: e(b1), b2: e(b2), b3: e(b3) }, mix: [] };
}
function run(offers, target, focus) {
  var cl = M.clean(offers), norm = M.normalize(cl.offers), cmp = M.compare(norm);
  var refs = offers.map(function (o) { return o.bank && o.bank !== 'other' ? M.bankRef(D, o.bank) : null; });
  var ctx = { offers: cl.offers, names: M.names(offers), norm: norm, cmp: cmp, refs: refs, sysRef: M.bankRef(D, 'system'), focus: focus || 'b2', D: D };
  ctx.target = target != null ? target : (cmp[ctx.focus].dearest != null ? cmp[ctx.focus].dearest : 0);
  return ctx;
}

/* ---------------------------------------------------------------------------------------------------------------- data */
t('data: baskets are the directive 451 definitions', function () {
  var L = D.baskets.list;
  assert.deepStrictEqual(L.map(function (b) { return b.k; }), ['b1', 'b2', 'b3']);
  assert.deepStrictEqual(L[0].mix.map(function (x) { return x[0]; }), ['fixed_nl']);
  assert.deepStrictEqual(L[1].mix.map(function (x) { return x[0]; }), ['fixed_nl', 'prime', 'var5_cpi']);
  assert.deepStrictEqual(L[2].mix.map(function (x) { return x[0]; }), ['fixed_nl', 'prime']);
  near(L[1].mix[0][1], 1 / 3, 1e-9); near(L[2].mix[0][1], 0.5, 1e-9);
  assert.strictEqual(M.basketText(D, 'b2'), 'שליש קבועה לא צמודה (קל״צ) · שליש פריים · שליש משתנה כל 5 שנים, צמודה למדד');
});
t('data: by_bank latest month and the five large banks', function () {
  var s = M.bankRef(D, 'system');
  assert.strictEqual(s.month, '2026-09');
  assert.strictEqual(s.rank.length, 5);
  assert.strictEqual(s.min.k, 'fibi'); near(s.min.irr, 4.748, 1e-9);
  assert.strictEqual(s.max.k, 'mizrahi'); near(s.max.irr, 5.1613, 1e-9);
  near(s.irr, 5.0949, 1e-9);
  assert.strictEqual(M.bankRef(D, 'leumi').big5, true);
  assert.strictEqual(M.bankRef(D, 'jerusalem').big5, false);
  assert.strictEqual(M.bankRef(D, 'nope'), null);
});

/* ------------------------------------------------------------------------------------------------------- normalization */
t('normalize: equal loans keep the typed numbers', function () {
  var e = M.example(), cl = M.clean(e.offers), N = M.normalize(cl.offers);
  assert.strictEqual(N.loansEqual, true); assert.strictEqual(N.termsEqual, true); assert.strictEqual(N.base, 1200000);
  near(N.rows[1].b.b2.nTotal, 2084000); near(N.rows[1].b.b2.nMax, 7617); near(N.rows[0].factor, 1);
  near(N.rows[0].b.b1.perShekel, 2073183 / 1200000, 1e-12);
});
t('normalize: a different amount is scaled to the first approval', function () {
  var o = [offer(1000000, 25, [5, 1700000, 6000, 6000]), offer(1250000, 25, [4.9, 2100000, 7400, 7400])];
  var N = M.normalize(M.clean(o).offers);
  assert.strictEqual(N.loansEqual, false); assert.strictEqual(N.base, 1000000);
  near(N.rows[1].factor, 0.8); near(N.rows[1].b.b1.nTotal, 1680000, 1e-6); near(N.rows[1].b.b1.nMax, 5920, 1e-6);
  near(N.rows[1].b.b1.irr, 4.9);  // a rate is not scaled
  var C = M.compare(N);
  assert.deepStrictEqual(C.b1.cheapest, [1]);  // 1,680,000 after scaling beats 1,700,000 although its raw total is higher
  near(C.b1.gapTotal, 20000, 1e-6);
});

/* ------------------------------------------------------------------------------------------------ cheapest and the gaps */
t('compare: the example, cheapest per basket and the gaps', function () {
  var c = run(M.example().offers).cmp;
  ['b1', 'b2', 'b3'].forEach(function (k) { assert.deepStrictEqual(c[k].cheapest, [1], k); assert.strictEqual(c[k].dearest, 0, k); assert.strictEqual(c[k].by, 'total'); });
  near(c.b1.gapTotal, 2073183 - 2042083); near(c.b1.gapMax, 6911 - 6807);
  near(c.b2.gapTotal, 2120212 - 2084000); near(c.b2.gapMax, 7748 - 7617); near(c.b2.gapIrr, 0.17, 1e-9);
  near(c.b3.gapTotal, 2031988 - 1996170);
});
t('compare: three offers, a tie for the cheapest marks both', function () {
  var o = [offer(1e6, 20, [5, 1600000, 6600, 6600]), offer(1e6, 20, [4.9, 1580000, 6500, 6500]), offer(1e6, 20, [4.9, 1580000, 6510, 6510])];
  var c = M.compare(M.normalize(M.clean(o).offers));
  assert.deepStrictEqual(c.b1.cheapest, [1, 2]); assert.strictEqual(c.b1.dearest, 0); near(c.b1.gapTotal, 20000);
});
t('compare: all equal means no dearest and a zero gap', function () {
  var o = [offer(1e6, 20, [5, 1600000, 6600, 6600]), offer(1e6, 20, [5, 1600000, 6600, 6600])];
  var c = M.compare(M.normalize(M.clean(o).offers));
  assert.strictEqual(c.b1.dearest, null); near(c.b1.gapTotal, 0); assert.deepStrictEqual(c.b1.cheapest, [0, 1]);
});
t('compare: different terms are compared by the overall interest', function () {
  var o = [offer(1e6, 20, [5.1, 1600000, 6600, 6600]), offer(1e6, 30, [4.9, 1900000, 5300, 5300])];
  var c = M.compare(M.normalize(M.clean(o).offers));
  assert.strictEqual(c.b1.by, 'irr'); assert.deepStrictEqual(c.b1.cheapest, [1]); near(c.b1.gapIrr, 0.2, 1e-9);
});
t('compare: a basket typed in one offer only marks nothing', function () {
  var o = [offer(1e6, 25, [5, 1700000, 6000, 6000]), offer(1e6, 25, null)];
  var c = M.compare(M.normalize(M.clean(o).offers));
  assert.deepStrictEqual(c.b1.cheapest, []); assert.strictEqual(c.b1.dearest, null); assert.ok(isNaN(c.b1.gapTotal));
});
t('check: impossible numbers are dropped, doubtful ones flagged', function () {
  var o = offer(1e6, 25, [25, 900000, 6000, 6500]);
  var is = M.check(o);
  assert.ok(is.some(function (x) { return x.f === 'irr' && x.drop; }));
  assert.ok(is.some(function (x) { return x.f === 'total' && x.drop; }));
  assert.ok(is.some(function (x) { return x.f === 'maxPay' && !x.drop; }));
  var c = M.clean([o]).offers[0];
  assert.ok(isNaN(c.b.b1.irr)); assert.ok(isNaN(c.b.b1.total)); near(c.b.b1.maxPay, 6000);
  assert.ok(M.check(offer(1e6, 35, null)).some(function (x) { return x.f === 'years'; }));
});

/* ---------------------------------------------------------------------------------------------------- bank averages */
t('place: an overall interest among the five large banks', function () {
  var ref = M.bankRef(D, 'leumi');
  var p = M.place(5.01, ref);
  assert.strictEqual(p.pos, 'between'); assert.strictEqual(p.under.k, 'discount'); assert.strictEqual(p.over.k, 'leumi');
  near(p.gapOwn, -0.02, 1e-9); near(p.own, 5.03, 1e-9);
  assert.strictEqual(M.place(4.57, ref).pos, 'below'); assert.strictEqual(M.place(5.3, ref).pos, 'above');
  assert.strictEqual(M.place(4.75, ref).pos, 'equal');
});
t('trackCmp: the bank average is effective, converted to nominal like tools/mortgage.js', function () {
  var ref = M.bankRef(D, 'hapoalim');
  var r = M.trackCmp({ track: 'fixed_nl', share: 40, rate: 4.85, years: 25 }, ref, 1200000);
  var nom = 1200 * (Math.pow(1 + 4.68 / 100, 1 / 12) - 1);
  near(r.nom, Math.round(nom * 100) / 100, 1e-9); near(r.eff, 4.68); near(r.gap, Math.round((4.85 - r.nom) * 100) / 100, 1e-9);
  near(r.amount, 480000);
  var p = function (B, a, n) { var q = a / 1200; return B * q / (1 - Math.pow(1 + q, -n)); };
  near(r.payGap, p(480000, 4.85, 300) - p(480000, r.nom, 300), 1e-6);
  assert.strictEqual(M.trackCmp({ track: 'zzz', share: 10, rate: 4, years: 10 }, ref, 1e6), null);
});

/* -------------------------------------------------------------------------------------------------- the negotiation text */
var BANNED = ['מומלץ', 'כדאי', 'ממליצים', 'ייעוץ', '—', '–', ' - ', 'סימולציה', 'המערכת', 'הפלטפורמה', 'ממשק'];
function numbersIn(s) { return (s.match(/\d[\d,]*(?:\.\d+)?/g) || []).map(function (x) { return x.replace(/,/g, ''); }); }
function allowed(ctx) {
  var a = {};
  var add = function (s) { a[String(s).replace(/,/g, '')] = 1; };
  ctx.offers.forEach(function (o) {
    if (isFinite(o.loan)) add(M.grp(o.loan)); if (isFinite(o.years)) add(M.yrs(o.years).split(' ')[0]);
    M.BASKETS.forEach(function (k) { var x = o.b[k]; if (isFinite(x.irr)) add(M.pct(x.irr).replace('%', '')); ['total', 'maxPay', 'first'].forEach(function (m) { if (isFinite(x[m])) add(M.grp(x[m])); }); });
  });
  var refs = ctx.refs.concat([ctx.sysRef]).filter(Boolean);
  refs.forEach(function (r) { add(M.pct(r.irr).replace('%', '')); add(M.pct(r.min.irr).replace('%', '')); add(r.month.slice(0, 4)); });
  ['1', '2', '3'].forEach(add);  // the basket numbers
  return a;
}
function checkLetter(ctx, label) {
  var txt = M.letter(ctx), ok = allowed(ctx);
  numbersIn(txt).forEach(function (x) { assert.ok(ok[x], label + ': number ' + x + ' is neither typed nor official'); });
  BANNED.forEach(function (w) { assert.ok(txt.indexOf(w) === -1, label + ': banned "' + w + '"'); });
  assert.ok(/קיבלתי/.test(txt) && /אשמח/.test(txt), label + ': first person singular');
  return txt;
}
t('letter: the example (banks not chosen) uses the all-banks average and only allowed numbers', function () {
  var ctx = run(M.example().offers), txt = checkLetter(ctx, 'example');
  assert.strictEqual(ctx.target, 0);
  assert.ok(txt.indexOf('5.09%') > -1 && txt.indexOf('ספטמבר 2026') > -1, 'official system average with its month');
  assert.ok(txt.indexOf('2,084,000 ₪') > -1 && txt.indexOf('2,120,212 ₪') > -1, 'basket 2 totals');
  assert.ok(txt.indexOf('בסל האחיד 1') > -1 && txt.indexOf('בסל האחיד 3') > -1);
  assert.ok(txt.indexOf('31,100') === -1 && txt.indexOf('36,212') === -1, 'no computed gap in the letter');
});
t('letter: a chosen bank gets its own average and the lowest of the five large', function () {
  var o = M.example().offers; o[0].bank = 'leumi'; o[1].bank = 'discount';
  var ctx = run(o), txt = checkLetter(ctx, 'leumi');
  assert.ok(txt.indexOf('5.03%') > -1, 'Leumi average'); assert.ok(txt.indexOf('4.75%') > -1 && txt.indexOf('הבינלאומי') > -1, 'five-large minimum');
  assert.ok(txt.indexOf('בנק דיסקונט') > -1);
});
t('letter: different amounts and terms, three offers, a target that is cheapest somewhere', function () {
  var o = [offer(1000000, 25, [5, 1700000, 6000, 5900], [5.2, 1760000, 6900, 5600], null, 'mizrahi'), offer(1250000, 30, [4.9, 2300000, 6700, 6700], null, [4.7, 2200000, 6400, 6400], 'fibi'),
    offer(1000000, 25, [5.1, 1720000, 6050, 6050], [5.0, 1740000, 6800, 5550], [4.8, 1690000, 5950, 5950], 'other')];
  [0, 1, 2].forEach(function (tg) { checkLetter(run(o, tg, 'b2'), 'target ' + tg); });
  var txt = M.letter(run(o, 0, 'b2'));
  assert.ok(txt.indexOf('5.16%') > -1, 'Mizrahi average');
});
t('table text: carries the cheapest mark and the official averages', function () {
  var o = M.example().offers; o[1].bank = 'fibi';
  var ctx = run(o), txt = M.tableText(ctx);
  assert.ok(txt.indexOf('(הזולה)') > -1); assert.ok(txt.indexOf('הבינלאומי 4.75%') > -1); assert.ok(txt.indexOf('כל הבנקים 5.09%') > -1);
  assert.ok(txt.indexOf('31,100 ₪') > -1, 'basket 1 gap');
});

/* -------------------------------------------------------------------------------------------------- visible words */
t('source: no long dash, no spaced hyphen and no blacklisted word in any string', function () {
  var src = fs.readFileSync(path.join(__dirname, 'moffers.js'), 'utf8');
  assert.ok(src.indexOf('—') === -1 && src.indexOf('–') === -1, 'long dash');
  var strs = src.match(/'(?:[^'\\\n]|\\.)*'/g) || [];
  var heb = strs.filter(function (s) { return /[֐-׿]/.test(s); });
  var bad = ['ממשק', 'דמו', 'הדגמה', 'מנגנון', 'סימולציה', 'המערכת', 'הפלטפורמה', 'טכנולוגיה', 'בקרוב', 'בבדיקה', 'מומלץ', 'כדאי', 'אינטראקטיבי', 'מובייל'];
  heb.forEach(function (s) { bad.forEach(function (w) { assert.ok(s.indexOf(w) === -1, 'banned "' + w + '" in ' + s); }); assert.ok(s.indexOf(' - ') === -1, 'spaced hyphen in ' + s); });
  assert.ok(src.indexOf('wa.me') === -1 && src.indexOf('וואטסאפ') === -1, 'no WhatsApp element or wording');
});

console.log('\n' + (n - fail) + '/' + n + ' passed');
process.exit(fail ? 1 : 0);
