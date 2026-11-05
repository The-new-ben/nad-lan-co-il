/* test_mbudget.js (HAD-675): node test of the mbudget pure logic and its rendered text. Run from anywhere:
     node docs/research/2026-11-05-mortgage-world/build/mbudget/test_mbudget.js
   Loads the real afford.js (window.NLAF) and mbudget.js, the research data boi-mortgage-v2.json (ships as data/boi-mortgage.json),
   ptax.json, cost.json, and a trimmed snapshot of the public near-finder endpoint (fixtures/). Checks:
   1. the calibration: 1,000,000 over 25 years in the 9.2026 system mix = 5,428 a month (and the equivalent rate fed to NLAF);
   2. both Bank of Israel limits on 4 cases (payment to income, LTV, equity covers tax + lawyer) and that +1,000 fails;
   3. the city filter: every shown city is at or under the max price, none that fits is missing, the payments re-derive;
   4. the listings: only for sale, with a published price, at or under the max, on nad-lan.co.il, no project, at most 6;
   5. no invented number: every ₪ amount, percent and date in the rendered text traces to an input, the data or the model;
      no long dash, no spaced hyphen, no blacklisted word, no "₪0". */
'use strict';
var fs = require('fs'), path = require('path');
var HERE = __dirname, REPO = path.resolve(HERE, '../../../../..');
var INS = path.join(REPO, 'plugins/nadlan-config/assets/instruments');
global.window = global;
require(path.join(INS, 'tools/afford.js'));
require(path.join(HERE, 'mbudget.js'));
var NLMB = global.NLMB, NLAF = global.NLAF;
function J(p) { return JSON.parse(fs.readFileSync(p, 'utf8')); }
var D = { boim: J(path.join(REPO, 'docs/research/2026-11-05-mortgage-world/data/boi-mortgage-v2.json')), ptax: J(path.join(INS, 'data/ptax.json')), cost: J(path.join(INS, 'data/cost.json')) };
var NF = J(path.join(HERE, 'fixtures/near-finder-2026-11-05.json'));

var pass = 0, fail = 0;
function ok(cond, msg) { if (cond) { pass++; } else { fail++; console.log('FAIL ' + msg); } }
function near(a, b, eps) { return Math.abs(a - b) <= (eps == null ? 1e-6 : eps); }

/* ---------------------------------------------------------------------------------------------------- 1. calibration */
var row = NLMB.sysRow(D.boim);
ok(row && row.bank === 'system', 'system row found in by_bank.latest.table');
ok(D.boim.by_bank.latest.month === '2026-09', 'latest month is 2026-09 (got ' + D.boim.by_bank.latest.month + ')');
var pm = NLMB.perMillion(row, 300);
ok(Math.round(pm) === 5428, 'calibration: 1,000,000 over 25 years = 5,428 (got ' + pm.toFixed(2) + ')');
ok(near(pm, D.boim.homes.payments.payment_per_1m, 0.05), 'calibration equals homes.payments.payment_per_1m ' + D.boim.homes.payments.payment_per_1m);
// independent re-derivation, track by track, straight from the brief's formula
var ind = 0, sh = 0; ['fixed_nl', 'prime', 'var_nl_other', 'var_cpi', 'fixed_cpi'].forEach(function (k) { sh += row[k].share; });
['fixed_nl', 'prime', 'var_nl_other', 'var_cpi', 'fixed_cpi'].forEach(function (k) { var r = Math.pow(1 + row[k].rate / 100, 1 / 12) - 1, L = 1e6 * row[k].share / sh; ind += L * r / (1 - Math.pow(1 + r, -300)); });
ok(near(ind, pm, 1e-6), 'perMillion equals the independent track by track sum');
var R = NLMB.eqRate(pm, 300);
ok(near(NLMB.pmt(1e6, R / 1200, 300), pm, 1e-6), 'the equivalent nominal rate reproduces the blended payment (R=' + R.toFixed(4) + '%)');
ok(near(NLAF.pv(pm, R, 300), 1e6, 1e-3), 'NLAF.pv(5,428.30, R, 300) = 1,000,000');

/* ------------------------------------------------------------------------------------------------- 2. the two limits */
var CASES = [
  { name: 'A example: 22,000 net, 600,000 equity, single home, 33%', inp: { income: 22000, equity: 600000, track: 'single', loans: 0, ratio: 33, years: 25 }, expect: 'payment' },
  { name: 'B high income, little equity, single home, 35%', inp: { income: 45000, equity: 450000, track: 'single', loans: 0, ratio: 35, years: 25 }, expect: 'equity' },
  { name: 'C additional home, loans 2,500, 40%, 30 years', inp: { income: 38000, equity: 1500000, track: 'extra', loans: 2500, ratio: 40, years: 30 }, expect: null },
  { name: 'D foreign resident, 50%, 20 years', inp: { income: 30000, equity: 2000000, track: 'foreign', loans: 0, ratio: 50, years: 20 }, expect: null },
  { name: 'E new oleh, 33%', inp: { income: 26000, equity: 700000, track: 'oleh', loans: 1000, ratio: 33, years: 25 }, expect: null }
];
var lawyerRate = D.cost.lawyer.from / 100 * (1 + D.cost.vat);
function cashNeed(price, loan, k) { return price - loan + NLMB.ptax(price, D.ptax, k) + lawyerRate * price; }
var models = {};
CASES.forEach(function (c) {
  var m = NLMB.solve(c.inp, D), k = c.inp.track, ltv = D.cost.ltv[k];
  models[c.name] = m;
  var n = c.inp.years * 12, pmN = NLMB.perMillion(row, n);
  var payMax = c.inp.income * Math.min(c.inp.ratio, 50) / 100 - c.inp.loans;
  ok(near(m.payMax, payMax, 1e-6), c.name + ': payMax = income x ratio - loans (' + payMax + ')');
  ok(near(m.loanMax, payMax / pmN * 1e6, 1e-3), c.name + ': loanMax = payMax / perMillion x 1e6');
  ok(m.monthly <= payMax + 0.01, c.name + ': limit 1, payment ' + m.monthly.toFixed(0) + ' <= ' + payMax);
  ok(m.loan <= ltv * m.price + 0.01, c.name + ': limit 2, loan ' + m.loan.toFixed(0) + ' <= ' + (100 * ltv) + '% of ' + m.price);
  ok(cashNeed(m.price, m.loan, k) <= c.inp.equity + 0.01, c.name + ': equity covers the rest + tax + lawyer');
  ok(near(m.tax, NLMB.ptax(m.price, D.ptax, k), 1e-6), c.name + ': tax equals the bracket sum');
  var p2 = m.price + 1000, loan2 = Math.min(ltv * p2, m.loanMax);
  ok(cashNeed(p2, loan2, k) > c.inp.equity, c.name + ': +1,000 fails (max price ' + m.price + ')');
  ok(near(m.monthly, m.loan * pmN / 1e6, 1e-6), c.name + ': payment = loan x perMillion');
  if (c.expect) ok(m.limit === c.expect, c.name + ': the binding limit is ' + c.expect + ' (got ' + m.limit + ')');
  console.log('  ' + c.name + ' -> max ' + m.price + ', loan ' + Math.round(m.loan) + ', payment ' + Math.round(m.monthly) + ', limit ' + m.limit);
});
var capA = NLMB.solve(Object.assign({}, CASES[0].inp, { ratio: 65 }), D), capB = NLMB.solve(Object.assign({}, CASES[0].inp, { ratio: 50 }), D);
ok(capA.price === capB.price && capA.ratio === 50, 'the share of income is capped at 50% (65% gives the 50% answer)');
var noRoom = NLMB.solve({ income: 10000, equity: 500000, track: 'single', loans: 4000, ratio: 33, years: 25 }, D);
ok(noRoom.loan === 0 && noRoom.payMax <= 0, 'loans above the payment leave no mortgage (price from equity only: ' + noRoom.price + ')');

/* -------------------------------------------------------------------------------------------------- 3. the city filter */
var mA = models[CASES[0].name], csA = NLMB.cities(D.boim, mA, CASES[0].inp, D.ptax);
var rows = D.boim.homes.payments.rows, fitsAll = [];
Object.keys(rows).forEach(function (city) { if (city === 'ישראל') return; ['r3', 'r4', 'r5'].forEach(function (rk) { var x = rows[city][rk]; if (x && x.median <= mA.price) fitsAll.push(city + '|' + rk.slice(1)); }); });
ok(csA.list.every(function (x) { return x.median <= mA.price; }), 'every shown city median is at or under the max price');
ok(csA.list.length === fitsAll.length && fitsAll.every(function (k) { return csA.list.some(function (x) { return x.city + '|' + x.rooms === k; }); }), 'no city that fits is missing (' + fitsAll.length + ' city and room pairs)');
ok(csA.list.every(function (x) { return x.city !== 'ישראל'; }) && csA.natl[4] && csA.natl[4].median === rows['ישראל'].r4.median, 'Israel is the reference line, not a city');
ok(csA.total === 24, 'the list covers 24 cities (got ' + csA.total + ')');
var four = csA.list.filter(function (x) { return x.rooms === 4; }).map(function (x) { return x.city; }).sort();
ok(JSON.stringify(four) === JSON.stringify(['אילת', 'אשקלון', 'באר שבע', 'חיפה'].sort()), 'case A, 4 rooms: Eilat, Ashkelon, Beer Sheva, Haifa (the design board), got ' + four.join(', '));
csA.list.forEach(function (x) {
  var src = rows[x.city]['r' + x.rooms];
  var loan = Math.max(0, x.median + NLMB.ptax(x.median, D.ptax, 'single') + lawyerRate * x.median - CASES[0].inp.equity);
  ok(x.median === src.median && x.quarter === src.quarter, x.city + ' ' + x.rooms + ': median and quarter are the data');
  ok(near(x.loan, loan, 1e-6) && near(x.payment, loan * mA.perM / 1e6, 1e-6), x.city + ' ' + x.rooms + ': the payment re-derives');
  ok(x.loan <= Math.min(0.75 * x.median, mA.loanMax) + 0.01, x.city + ' ' + x.rooms + ': that loan passes both limits');
});
ok(NLMB.bestRooms(csA) === 5 || NLMB.bestRooms(csA) === 4 || NLMB.bestRooms(csA) === 3, 'a default room count is picked');

/* ------------------------------------------------------------------------------------------------------ 4. listings */
var lsA = NLMB.listings(NF, mA.price, 6);
ok(lsA.items.every(function (x) { return x.price > 0 && x.price <= mA.price; }), 'listings: every price is published and at or under the max');
ok(lsA.items.every(function (x) { var s = NF.listings.filter(function (y) { return y.id === x.id; })[0]; return s && s.deal === 'sale' && s.price === x.price && s.url === x.url; }), 'listings: for sale, price and link exactly as the endpoint');
ok(lsA.items.every(function (x) { return !NF.projects.some(function (p) { return p.url === x.url; }); }), 'listings: no project (projects carry no home price)');
ok(lsA.items.length <= 6, 'listings: at most 6');
var big = NLMB.listings(NF, 1e9, 6), priced = NF.listings.filter(function (x) { return x.deal === 'sale' && x.price > 0; }).length;
ok(big.count === priced && big.items.length === Math.min(6, priced), 'listings: all ' + priced + ' priced homes for sale in the snapshot when the budget is huge');
var many = { listings: [] }; for (var q = 1; q <= 9; q++) many.listings.push({ id: q, deal: 'sale', price: q * 100000, title: 't' + q, url: 'https://nad-lan.co.il/properties/t' + q + '/' });
var cut = NLMB.listings(many, 1e9, 6);
ok(cut.items.length === 6 && cut.count === 9 && cut.items[0].price === 900000, 'listings: 6 shown of 9, the closest to the budget first');
ok(big.items.every(function (x, i) { return i === 0 || big.items[i - 1].price >= x.price; }), 'listings: sorted from the closest to the budget');
ok(!big.items.some(function (x) { return x.id === 8424 || x.id === 7633; }), 'listings: a sale listing with no price (8424, 7633) is never shown');
var evil = NLMB.listings({ listings: [{ id: 1, deal: 'sale', price: 100, title: 'x', url: 'https://evil.example/a' }, { id: 2, deal: 'sale', price: 100, title: 'y', url: 'javascript:alert(1)' }] }, 1e6, 6);
ok(evil.count === 0, 'listings: a link off nad-lan.co.il is dropped');
console.log('  case A listings: ' + lsA.items.map(function (x) { return x.id + ' ' + x.price; }).join(', ') + ' (of ' + lsA.count + ')');

/* ----------------------------------------------------------------------------------------- 5. no invented number */
function text(html) { return html.replace(/<[^>]+>/g, ' ').replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>'); }
function attrs(html) { var a = []; html.replace(/aria-label="([^"]*)"/g, function (_, x) { a.push(x); }); return a.join(' '); }
function moneyTokens(s) { var out = []; s.replace(/₪([\d,]+)/g, function (_, x) { out.push(+x.replace(/,/g, '')); }); return out; }
function pctTokens(s) { var out = []; s.replace(/(\d+(?:\.\d+)?)%/g, function (_, x) { out.push(+x); }); return out; }
function dateTokens(s) { var out = []; s.replace(/(?:^|[^\d.\-])((?:\d{1,2}\.)?\d{1,2}\.\d{4})/g, function (_, x) { out.push(x); }); return out; }
function d(iso) { var p = String(iso).slice(0, 10).split('-'); return (+p[2]) + '.' + (+p[1]) + '.' + p[0]; }
function mo(k) { var p = String(k).split('-'); return (+p[1]) + '.' + p[0]; }
var DATES = [mo(D.boim.by_bank.src.as_of), d(D.boim.by_bank.src.file_date), d(D.ptax.effective), d(D.ptax.checked_v3 || D.ptax.checked), d(D.boim.homes.medians.src.retrieved_at), d(NF.updated), mo(D.boim.by_bank.latest.month)];
(D.cost.sources[1].label.match(/\d{1,2}\.\d{1,2}\.\d{4}/g) || []).forEach(function (x) { DATES.push(x); });  // the dated source label in cost.json
Object.keys(rows).forEach(function (c) { ['r3', 'r4', 'r5'].forEach(function (rk) { if (rows[c][rk]) DATES.push(rows[c][rk].quarter.replace(/^\d+-/, '')); }); });
var BLACK = ['ממשק', 'דמו', 'הדגמה', 'מנגנון', 'סימולציה', 'אלגוריתם', 'המערכת', 'הפלטפורמה', 'טכנולוגיה', 'בבדיקה', 'בקרוב', 'פיילוט', 'אינטראקטיבי', ' AI', 'אטלס'];

CASES.forEach(function (c) {
  var m = models[c.name], cs = NLMB.cities(D.boim, m, c.inp, D.ptax), ls = NLMB.listings(NF, m.price, 6);
  var R3 = function (x) { return Math.round(x); };
  var money = [c.inp.income, c.inp.equity, c.inp.loans, m.price, m.loan, m.monthly, m.payMax, m.loanMax, m.tax, m.lawyer, m.ltv * m.price, m.price - m.loan, m.tax + m.lawyer, m.perM, 1e6, m.taxFree || 0].map(R3);
  cs.list.forEach(function (x) { money.push(x.median, R3(x.payment)); });
  [3, 4, 5].forEach(function (r) { if (cs.natl[r]) money.push(cs.natl[r].median); if (cs.cheapest[r]) money.push(cs.cheapest[r].median); });
  ls.items.forEach(function (x) { money.push(x.price); });
  var pcts = [m.ratio, 100 * m.ltv, D.cost.lawyer.from, 50, 35, 40];
  cs.list.forEach(function (x) { pcts.push(Math.round(Math.max(2, Math.min(100, 100 * x.median / m.price)))); });
  var html = NLMB.html.answer(m, c.inp, D, true);
  [3, 4, 5].forEach(function (r) { html += NLMB.html.rooms(cs, r) + NLMB.html.cities(cs, r, m, D.boim); });
  html += NLMB.html.homes(ls, m, 'ok') + NLMB.html.homes(null, m, 'error') + NLMB.html.homes(null, m, 'loading');
  var share = NLMB.shareText(m, c.inp, cs, NLMB.bestRooms(cs));
  var all = text(html) + ' ' + attrs(html) + ' ' + share;
  var bad = moneyTokens(all).filter(function (x) { return money.indexOf(x) < 0; });
  ok(bad.length === 0, c.name + ': every ₪ amount traces to inputs, data or model' + (bad.length ? ' (stray: ' + bad.join(', ') + ')' : ''));
  var badP = pctTokens(all).filter(function (x) { return !pcts.some(function (p) { return near(p, x, 0.051); }); });
  ok(badP.length === 0, c.name + ': every percent traces' + (badP.length ? ' (stray: ' + badP.join(', ') + ')' : ''));
  var badD = dateTokens(text(html)).filter(function (x) { return DATES.indexOf(x) < 0; });
  ok(badD.length === 0, c.name + ': every date is a data date' + (badD.length ? ' (stray: ' + badD.join(', ') + ')' : ''));
  ok(!/[–—]/.test(all) && !/ - /.test(all), c.name + ': no long dash and no spaced hyphen');
  ok(moneyTokens(all).indexOf(0) < 0, c.name + ': no ₪0 on screen');
  var hit = BLACK.filter(function (w) { return all.indexOf(w) > -1; });
  ok(hit.length === 0, c.name + ': no blacklisted word' + (hit.length ? ' (' + hit.join(', ') + ')' : ''));
  ok(text(html).indexOf(NLMB.ils(m.price)) > -1, c.name + ': the max price is on screen');
});
var errHtml = NLMB.html.homes(null, mA, 'error');
ok(errHtml.indexOf(NLMB.ALL) > -1 && moneyTokens(text(errHtml)).length === 0, 'endpoint failure: the see all link stays, no price is shown');
var src = fs.readFileSync(path.join(HERE, 'mbudget.js'), 'utf8');
ok(!/[–—]/.test(src), 'mbudget.js has no long dash anywhere (code, comments, strings)');

console.log((fail ? 'FAILED ' : 'OK ') + pass + ' passed, ' + fail + ' failed');
process.exit(fail ? 1 : 0);
