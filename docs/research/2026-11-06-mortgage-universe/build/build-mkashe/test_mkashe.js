/* HAD-675 (mortgage universe) · node test of mkashe ("כשקשה לשלם", the mortgage hardship tool).
   Run from anywhere:  node docs/research/2026-11-06-mortgage-universe/build/build-mkashe/test_mkashe.js
   Loads the repo file tools/mkashe.js (NLKS) with a fake window, and the real data files data/kashe.json and data/boi-mortgage.json,
   and gov/banks.json of the research folder. Every expected payment below was worked out by hand with 50-digit decimals
   (Python decimal, the script is in README.md), written as a literal, not recomputed with the tool's own formula:
   pmt = B x i / (1 - (1 + i)^-n), i = annual / 1200; full deferral: B x (1 + i)^d over n - d months; interest only: B x i during,
   then B over n - d; extension: B x (1 + i)^d over n months; extra = all payments to the end minus P0 x n. "Today" is 6.11.2026.
   Exit code 1 on a failure. */
'use strict';
var path = require('path'), fs = require('fs');
var HERE = __dirname, REPO = path.resolve(HERE, '../../../../..');
var INS = path.join(REPO, 'plugins/nadlan-config/assets/instruments');
global.window = {};
require(path.join(INS, 'tools/mkashe.js'));
var L = window.NLKS;
var K = require(path.join(INS, 'data/kashe.json'));
var B = require(path.join(INS, 'data/boi-mortgage.json'));
var BANKS = require(path.join(REPO, 'docs/research/2026-11-06-mortgage-universe/gov/banks.json'));
var TODAY = '2026-11-06';

var fails = 0, n = 0;
function ok(cond, name, got) { n++; if (cond) console.log('  ok   ' + name + (got != null ? '  [' + got + ']' : '')); else { fails++; console.log('  FAIL ' + name + (got != null ? '  [' + got + ']' : '')); } }
function near(a, b, tol) { return Math.abs(a - b) <= (tol == null ? 0.001 : tol); }
function run(o) { var v = L.defaults(B); Object.keys(o || {}).forEach(function (k) { v[k] = o[k]; }); return L.compute(v, K); }
var KS = { full: 'full', io: 'io', ext: 'ext' };

console.log('data: kashe.json checked ' + K.checked + '; boi-mortgage rates.fixed_nl ' + B.rates.fixed_nl.rate + '% (' + B.rates.fixed_nl.hist.slice(-1)[0][0] + ')');

console.log('\n0. the data file');
ok(K.key === 'kashe' && K.checked === '2026-11-06' && /gov\.md/.test(K.src), 'kashe.json: key "kashe", "checked": "2026-11-06", "src" names gov.md', K.checked);
var SRC = Object.keys(K.sources);
ok(SRC.every(function (id) { var s = K.sources[id]; return s.s && s.t && /^https:\/\//.test(s.url) && /^\d{4}-\d{2}-\d{2}$/.test(s.date) && s.read === '2026-11-06'; }), 'every source: short label, title, https URL, a date and the read date 6.11.2026', SRC.length + ' sources');
ok(SRC.filter(function (id) { return K.sources[id].kind === 'kz'; }).every(function (id) { return /^https:\/\/www\.kolzchut\.org\.il\/he\//.test(K.sources[id].url) && K.sources[id].date_kind === 'updated'; }), 'every Kol Zchut source: a kolzchut.org.il/he/ URL and the page update date');
var refs = [];
K.timeline.forEach(function (s) { refs = refs.concat(s.src); });
K.rights.items.forEach(function (s) { refs = refs.concat(s.src); });
K.rights.all.forEach(function (s) { refs = refs.concat(s.src); });
K.programs.items.forEach(function (s) { refs = refs.concat(s.src); });
K.lines.banks.forEach(function (s) { refs.push(s.src); });
K.help.forEach(function (s) { refs.push(s.src); });
Object.keys(K.rules.src).forEach(function (k) { refs.push(K.rules.src[k]); });
var bad = refs.filter(function (r) { return !L.srcOf(r, K); });
ok(bad.length === 0, 'every source reference (timeline, rights, programs, lines, help, rules) resolves', bad.join() || refs.length + ' refs');
ok(K.timeline.every(function (s) { return s.src.length > 0; }) && K.rights.items.every(function (s) { return s.src.length > 0; }) && K.programs.items.every(function (s) { return s.src.length > 0; }), 'every timeline step, right and program carries at least one source');
var Rr = K.rules;
ok(Rr.notice_business_days === 21 && Rr.enforce_months === 6 && Rr.hardship_months === 3 && Rr.hardship_times === 3 && Rr.hardship_every_months === 12 && Rr.rent_months === 18 && Rr.death_months === 12, 'rules: 21 business days, 6 months, 3 months up to 3 times once per 12, 18 months rent, 12 months after death');
ok(Rr.self_sale_notice_days === 20 && Rr.self_sale_stay_days === 90 && Rr.receiver_days === 90 && Rr.immediate_arrears_pct === 10 && Rr.fee_free_cap_ils === 2500000 && Rr.committee_days === 60 && Rr.appeal_file_days === 15 && Rr.appeal_decide_days === 30, 'rules: 20 / 90 days, 90 days after the receiver, 10%, 2.5 million, committee 60 / 15 / 30');
function step(k) { return K.timeline.filter(function (s) { return s.k === k; })[0]; }
function stepText(k) { var s = step(k); return [s.when, s.title, s.what, s.note || ''].concat(s.protect, s.do).join(' '); }
function right(k) { return K.rights.items.filter(function (s) { return s.k === k; })[0]; }
ok(stepText('notice').indexOf(Rr.notice_business_days + ' ימי עסקים') > -1 && stepText('six').indexOf(Rr.enforce_months + ' חודשים') > -1 && stepText('day0').indexOf(Rr.enforce_months + ' חודשים') > -1, 'the texts carry the rule numbers: 21 ימי עסקים (notice), 6 חודשים (day 0, six)');
ok(stepText('office').indexOf(Rr.self_sale_notice_days + ' ימים') > -1 && stepText('office').indexOf(Rr.self_sale_stay_days + ' ימים') > -1 && stepText('receiver').indexOf(Rr.receiver_days + ' ימים') > -1 && stepText('six').indexOf(Rr.immediate_arrears_pct + '%') > -1, 'the texts carry 20 and 90 days (warning), 90 days (receiver), 10% (immediate)');
ok(stepText('sale').indexOf(Rr.rent_months + ' חודשים') > -1 && stepText('sale').indexOf('2.5 מיליון ₪') > -1 && stepText('sale').indexOf('16.5.2009') > -1, 'the sale step carries 18 months, 2.5 million ₪ and the 16.5.2009 deeds');
var hs = right('hardship').text;
ok(hs.indexOf('עד ' + Rr.hardship_months + ' חודשים') > -1 && hs.indexOf(Rr.hardship_every_months + ' חודשים') > -1 && hs.indexOf(Rr.hardship_times + ' פעמים') > -1 && right('death').title.indexOf(Rr.death_months + ' חודשים') > -1, 'rights carry 3 months, once per 12, 3 times (s.9ח1) and 12 months after death (s.9ח2)');
var cm = right('committee').text;
ok(cm.indexOf(Rr.committee_days + ' ימים') > -1 && cm.indexOf(Rr.appeal_file_days + ' ימים') > -1 && cm.indexOf(Rr.appeal_decide_days + ' ימים') > -1 && right('committee').src.indexOf('hll:5א') > -1 && right('committee').src.indexOf('hll:5ב') > -1, 'the committee right: 60, 15 and 30 days, Housing Loans Law s.5א and 5ב');
var el = right('elder').text;
ok(el.indexOf('70') > -1 && el.indexOf('4.11.2007') > -1 && el.indexOf('300 ₪') > -1 && el.indexOf('200 ₪') > -1 && right('elder').tip.indexOf('*2310') > -1, 'the elderly right: 70, until 4.11.2007, 300 ₪ / 200 ₪, the *2310 line');
var cr = K.texts.copy_rules;
ok([Rr.enforce_months + ' חודשים', Rr.notice_business_days + ' ימי עסקים', Rr.self_sale_notice_days + ' ימים', Rr.self_sale_stay_days + ' ימים', Rr.rent_months + ' חודשים', 'עד ' + Rr.hardship_months + ' חודשים', Rr.hardship_every_months + ' חודשים', Rr.hardship_times + ' פעמים', Rr.death_months + ' חודשים'].every(function (x) { return cr.indexOf(x) > -1; }), 'the copy sentence (texts.copy_rules) carries 6 months, 21 business days, 20 / 90 days, 18 months, 3 months / 12 / 3 times, 12 months');

console.log('\n1. hand-worked Spitzer: 1,000,000 ILS, 300 months left, 4.62%, 3 months');
var a = run({ b: 1000000, n: 300, r: 4.62, d: 3 });
ok(near(a.P0, 5626.656114), 'payment before: 5,626.656114', a.P0.toFixed(6));
ok(near(a.base, 1687996.8341, 0.01), 'all payments without a deferral: 1,687,996.83', a.base.toFixed(2));
ok(near(a.by.full.bal, 1011594.524567) && near(a.by.full.acc, 11594.524567), 'full deferral: balance after 3 months 1,011,594.52 (interest 11,594.52 joined it)', a.by.full.bal.toFixed(6));
ok(near(a.by.full.after, 5722.512908) && a.by.full.nAfter === 297 && a.by.full.during === 0, 'full deferral: payment after 5,722.51 over 297 months, nothing paid during', a.by.full.after.toFixed(6));
ok(near(a.by.full.extra, 11589.4995, 0.01), 'full deferral: 11,589.50 more in total', a.by.full.extra.toFixed(4));
ok(near(a.by.io.during, 3850) && near(a.by.io.acc, 11550) && a.by.io.paid === true, 'interest only: 3,850 a month during (11,550 paid)', a.by.io.during);
ok(near(a.by.io.after, 5656.923568) && near(a.by.io.extra, 3659.4657, 0.01), 'interest only: payment after 5,656.92, 3,659.47 more in total', a.by.io.after.toFixed(6) + ' / ' + a.by.io.extra.toFixed(4));
ok(near(a.by.ext.after, 5691.894516) && a.by.ext.nAfter === 300 && a.by.ext.shift === 3, 'extension: payment after 5,691.89 over 300 months, the loan 3 months longer', a.by.ext.after.toFixed(6));
ok(near(a.by.ext.extra, 19571.5208, 0.01), 'extension: 19,571.52 more in total', a.by.ext.extra.toFixed(4));
ok(a.cheapest === 'io' && /^הזולה ביותר בסך הכול: ריבית בלבד, 3,659 ₪ יותר/.test(L.cheapText(a, K)), 'the cheapest in one sentence: ריבית בלבד, 3,659 ₪', L.cheapText(a, K));
ok(near(a.by.ext.after, a.P0 * Math.pow(1.00385, 3), 1e-6) && near(a.by.full.bal, a.by.ext.bal, 1e-9), 'identity: extension payment = P0 x 1.00385^3; full and extension end the deferral on the same balance');
var a6 = run({ b: 1000000, n: 300, r: 4.62, d: 6 });
ok(near(a6.by.full.after, 5820.536146) && near(a6.by.io.after, 5687.875093) && near(a6.by.ext.after, 5757.889327), '6 months: after 5,820.54 / 5,687.88 / 5,757.89', [a6.by.full.after, a6.by.io.after, a6.by.ext.after].map(function (x) { return x.toFixed(2); }).join(' / '));
ok(near(a6.by.full.extra, 23240.7929, 0.01) && near(a6.by.io.extra, 7338.4433, 0.01) && near(a6.by.ext.extra, 39369.9640, 0.01), '6 months: extra 23,240.79 / 7,338.44 / 39,369.96');
var a1 = run({ b: 1000000, n: 300, r: 4.62, d: 1 });
ok(near(a1.by.full.after, 5658.371720) && near(a1.by.io.extra, 1217.6570, 0.01) && near(a1.by.ext.extra, 6498.7878, 0.01), '1 month: full after 5,658.37, interest only +1,217.66, extension +6,498.79');
var b5 = run({ b: 600000, n: 180, r: 5, d: 2 });
ok(near(b5.P0, 4744.761760) && near(b5.by.full.after, 4820.528757) && near(b5.by.io.after, 4780.607366) && near(b5.by.ext.after, 4784.383816), '600,000 / 180 months / 5% / 2 months: 4,744.76 before; after 4,820.53 / 4,780.61 / 4,784.38');
ok(near(b5.by.full.extra, 3997.0019, 0.01) && near(b5.by.io.extra, 1890.9942, 0.01) && near(b5.by.ext.extra, 7131.9700, 0.01) && b5.cheapest === 'io', '600,000 case: extra 3,997.00 / 1,890.99 / 7,131.97, cheapest interest only');
var z = run({ b: 400000, n: 120, r: 0, d: 3 });
ok(near(z.P0, 3333.333333) && near(z.by.full.after, 3418.803419) && near(z.by.ext.after, 3333.333333) && z.cheapest === null && /0%/.test(L.cheapText(z, K)), '0%: no extra cost for any way, said in words (3,333.33 before, 3,418.80 after a full deferral)', L.cheapText(z, K));

console.log('\n2. the payment instead of the rate');
ok(near(L.solveRate(1000000, 300, 5626.656114), 4.62, 1e-5), 'the rate solved from 1,000,000 / 300 / 5,626.66: 4.62%', L.solveRate(1000000, 300, 5626.656114).toFixed(6));
var p = run({ m: 'pay', p: 5626.656114, r: '' });
ok(!p.error && p.derived && near(p.by.full.after, 5722.512908, 0.001), 'payment mode gives the same three ways (full after 5,722.51)', p.error ? p.error.msg : p.by.full.after.toFixed(4));
ok(run({ m: 'pay', p: 3000 }).error.field === 'p' && /בלי ריבית בכלל/.test(run({ m: 'pay', p: 3000 }).error.msg), 'a payment below balance / months: an error on the payment field');
ok(near(L.solveRate(400000, 120, 3333.3333), 0, 1e-9), 'balance / months exactly: rate 0');

console.log('\n3. bad values');
ok(run({ b: 5000 }).error.field === 'b' && run({ n: 300.5 }).error.field === 'n' && run({ n: 6 }).error.field === 'n' && run({ d: 7 }).error.field === 'd' && run({ r: 25 }).error.field === 'r', 'balance 5,000, 300.5 months, 6 months, 7 deferral months, 25%: each an error on its own field');
ok(L.compute({ b: 1e6, n: 300, m: 'rate', r: 4.62, d: 3 }, null).error.msg === 'הנתונים לא נטענו. רעננו את העמוד.', 'no data: the reload message');
ok(L.money('1,000,000 ₪') === 1000000 && L.num('4,62') === 4.62 && L.num('4.62') === 4.62, 'parsers: "1,000,000 ₪" = 1000000; "4,62" and "4.62" = 4.62');

console.log('\n4. the timeline');
var S = L.steps(K, '');
ok(S.map(function (s) { return s.k; }).join() === 'day0,notice,six,office,receiver,sale', 'order: day 0, the notice, 6 months, the execution office, the receiver, the sale', S.map(function (s) { return s.k; }).join(' > '));
ok(K.timeline.every(function (s, i, A) { return i === 0 || A[i - 1].order < s.order; }), 'the data file lists the steps in their order');
var S2 = L.steps(K, '2026-05-10');
ok(S2[0].date === '2026-05-10' && S2[2].date === '2026-11-10' && S2.filter(function (s) { return s.date; }).length === 2, 'first missed payment 10.5.2026: the 6-month line falls on 10.11.2026', S2[2].date);
ok(L.addMonths('2026-08-31', 6) === '2027-02-28' && L.addMonths('2027-08-31', 6) === '2028-02-29' && L.addMonths('2026-12-15', 6) === '2027-06-15', 'six calendar months: 31.8 -> 28.2 (29.2 in 2028), 15.12 -> 15.6');
ok(L.steps(K, 'x')[2].date === null, 'no date (or a bad one): no date on the steps');
ok(step('six').protect.join(' ').indexOf('בלבד') > -1 && step('office').do.join(' ').indexOf('התנגדות') > -1 && step('receiver').protect.join(' ').indexOf('מחצית') > -1, 'arrears only (six), objection (office), half within 90 days (receiver)');

console.log('\n5. the wartime outlines');
var P = K.programs.items;
ok(P.map(function (x) { return x.k + ':' + x.last; }).join() === 'shaagat:2026-05-15,kalavi:2025-07-31', 'two outlines with their last application day: שאגת הארי 15.5.2026, עם כלביא 31.7.2025');
ok(P.every(function (x) { return L.programStatus(x, TODAY) === 'ended' && L.statusText(x, TODAY) === 'הסתיים'; }), 'on 6.11.2026 both are "הסתיים"');
ok(L.programStatus(P[0], '2026-05-01') === 'open' && L.programStatus(P[0], '2026-05-16') === 'ended', 'the status follows the date (open on 1.5.2026, ended on 16.5.2026)');
var progText = P.map(function (x) { return [x.name, x.dates, x.who, x.terms, x.excl || ''].join(' '); }).join(' ') + K.programs.note + K.programs.title;
ok(!/פתוח|אפשר להגיש|הגישו/.test(progText) && /הסתיימו/.test(K.programs.title), 'no outline text invites to apply; the block title says they ended');
ok(K.programs.note === 'בכל מבצע חדש בנק ישראל מפרסם מתווה; בודקים מול הבנק.', 'the one line about a new operation');
ok(P[0].dates.indexOf('2.3.2026') > -1 && P[0].dates.indexOf('15.4.2026') > -1 && P[0].dates.indexOf('15.5.2026') > -1 && P[1].dates.indexOf('17.6.2025') > -1 && P[1].dates.indexOf('31.7.2025') > -1, 'the official dates: 2.3.2026, 15.4.2026, 15.5.2026; 17.6.2025, 1.7 to 31.7.2025');

console.log('\n6. the rights checklist');
function rk(sel) { return L.rightsFor(sel, K).map(function (x) { return x.k; }).join(); }
ok(rk(['jobill']) === 'hardship' && rk(['birth']) === 'hardship', 'פיטורים או מחלה, לידה: the deferral of s.9ח1');
ok(rk(['death']) === 'death,insurance', 'פטירה של לווה: s.9ח2 and the life insurance');
ok(rk(['zakaut']) === 'committee' && rk(['elder']) === 'elder' && rk(['reserve']) === 'reserve', 'הלוואת זכאות: the committee; גיל מבוגר: the elderly share; מילואים: what Kol Zchut says');
ok(rk(K.rights.situations.map(function (s) { return s.k; })).split(',').length === 6 && rk([]) === '', 'all six ticked: six rights, none twice; nothing ticked: none');
ok(right('reserve').text.indexOf('לא נקבעו הסדרים מיוחדים') > -1 && right('reserve').src.join() === 'kz_res', 'מילואים: no special mortgage arrangement in שאגת הארי, per Kol Zchut (26.7.2026)');

console.log('\n7. the bank lines and the free help');
var miz = BANKS.banks.filter(function (b) { return /Mizrahi/.test(b.name_en); })[0];
var mizLine = miz.phones.filter(function (p) { return /איחור/.test(p.purpose); })[0];
var k0 = K.lines.banks[0];
ok(k0.bank === 'מזרחי-טפחות' && k0.tel === '*8860' && k0.ext === 'שלוחה 4 ואז 3' && mizLine.numbers[0] === '*8860 ext. 4 then 3', 'Mizrahi-Tefahot arrears line *8860, extension 4 then 3, as in banks.json', mizLine.numbers[0]);
var allNums = []; BANKS.banks.forEach(function (b) { (b.phones || []).forEach(function (p) { allNums = allNums.concat(p.numbers.map(function (x) { return x.split(' ')[0]; })); }); });
ok(K.lines.banks.every(function (b) { return allNums.indexOf(b.tel) > -1 && (!b.alt || allNums.indexOf(b.alt) > -1); }), 'every bank number shown is in banks.json', K.lines.banks.length + ' lines');
ok(K.help.map(function (h) { return h.tel || '-'; }).join() === '118,*2310,-,*35592' && K.help.every(function (h) { return K.sources[h.src].kind === 'kz'; }), 'free help: שי״ל 118, *2310, legal aid, *35592; each from a Kol Zchut page');

console.log('\n8. the case link and the summary');
var v0 = L.defaults(B); v0.miss = '2026-05-10'; v0.sel = ['death'];
var c = L.caseOf(v0), h = L.enc(c), back = L.dec(h);
ok(back && back.b === 1000000 && back.n === 300 && back.r === 4.62 && back.d === 3 && back.m === 'rate', 'the hash round trip: 1,000,000 / 300 / 4.62% / 3 months', h);
ok(!('miss' in c) && !('sel' in c) && JSON.stringify(c).indexOf('death') < 0, 'the hash holds no date and no ticked situation');
var v1 = { b: 1, n: 1, m: 'rate', r: 1, p: '', d: 1, k: 'full' };
ok(L.fromCase({ b: 'x', n: null, m: 'evil', k: 'zzz', d: 2 }, v1) && v1.b === 1 && v1.n === 1 && v1.m === 'rate' && v1.k === 'full' && v1.d === 2, 'a forged hash: only sane known values are taken');
ok(L.dec('%%%') === null, 'a broken hash: ignored');
var tx = L.copyText(a, K);
ok(tx.indexOf('5,627 ₪') > -1 && tx.indexOf('5,723 ₪') > -1 && tx.indexOf('3,659 ₪') > -1 && tx.indexOf('אינו ייעוץ משפטי') > -1 && tx.indexOf('6.11.2026') > -1, 'the summary: 5,627 before, 5,723 after, 3,659 cheapest, not legal advice, the check date');
ok(K.rights.situations.every(function (s) { return tx.indexOf(s.he) < 0; }) && !/פתוח/.test(tx), 'the summary names no situation and no open outline');

console.log('\n9. the rate starting point');
var br = L.boimRate(B);
ok(br && br.rate === 4.62 && br.month === '2026-08' && L.defaults(B).r === 4.62, 'opens on the BoI average fixed not linked of 8.2026: 4.62% (boi-mortgage.json rates.fixed_nl)', br.rate + ' / ' + br.month);
ok(L.defaults(null).r === '', 'without the BoI file: no rate is made up (the field opens empty)');

console.log('\n10. words and hygiene');
var JS = fs.readFileSync(path.join(INS, 'tools/mkashe.js'), 'utf8'), JSON_TXT = fs.readFileSync(path.join(INS, 'data/kashe.json'), 'utf8');
var LONG = /[\u2013\u2014]/;
ok(!LONG.test(JS) && !LONG.test(JSON_TXT), 'no long dash in mkashe.js or kashe.json');
var BANNED = new RegExp('(\u05de\u05de\u05e9\u05e7|\u05d4\u05d3\u05d2\u05de\u05d4|\u05e1\u05d9\u05de\u05d5\u05dc\u05e6\u05d9\u05d4|\u05de\u05e0\u05d2\u05e0\u05d5\u05df|\u05d0\u05d9\u05e0\u05d8\u05e8\u05d0\u05e7\u05d8\u05d9\u05d1\u05d9|\u05d4\u05de\u05e2\u05e8\u05db\u05ea|\u05d4\u05e4\u05dc\u05d8\u05e4\u05d5\u05e8\u05de\u05d4|\u05d8\u05db\u05e0\u05d5\u05dc\u05d5\u05d2\u05d9\u05d4|(^|[^\u0590-\u05ff])\u05d3\u05de\u05d5([^\u0590-\u05ff]|$))');  // escaped, so this file holds none of them
var visible = JSON.stringify([K.texts, K.calc, K.timeline, K.lines, K.help, K.rights, K.programs]);
ok(!BANNED.test(visible) && !BANNED.test(JS.replace(/\/\*[\s\S]*?\*\//g, '')), 'none of the banned words in the visible texts or the script');
ok(!/חרבות ברזל|תקרה על ריבית|ריבית פיגורים מרבית|החזר עלות ייעוץ/.test(visible), 'the unverified items (Swords of Iron terms, an arrears-interest cap, the reservist advice refund) are not on the page');
ok(!/\bfetch\(|sendBeacon|XMLHttpRequest|<form|localStorage/.test(JS), 'the script sends nothing and stores nothing (no fetch, beacon, XHR, form or localStorage)');
ok(/#mkashe=/.test(JS) && !/location\.hash\s*=|replaceState|pushState/.test(JS), 'the case goes into #mkashe= only when asked: the script never writes the address');

console.log('\n' + (n - fails) + ' of ' + n + ' passed' + (fails ? ', ' + fails + ' FAILED' : ''));
process.exit(fails ? 1 : 0);
