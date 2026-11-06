/* HAD-675 (mortgage delta A1, A2, A8) · node test of mzakaut ("מחשבון זכאות משכנתא") and mnomeff ("ריבית נומינלית וריבית אפקטיבית").
   Run from anywhere:  node docs/research/2026-11-06-mortgage-delta/build-mzakaut/test_mzakaut.js
   Loads the repo files tools/mzakaut.js (NLZK) and tools/mnomeff.js (NLNE) with a fake window, and the real data files
   data/zakaut.json and data/boi-mortgage.json. Every expected number below was worked out by hand from the official tables as
   eligibility.md quotes them (S3 points and amounts, S4 ages, S5, S7 per-month amounts, S8, S9, S10, S11, S12), written as a
   literal, not recomputed from the tool. The converter's literals come from a 40-digit decimal calculation. "Today" is fixed at
   6.11.2026. Exit code 1 on a failure. */
'use strict';
var path = require('path'), fs = require('fs');
var HERE = __dirname, REPO = path.resolve(HERE, '../../../..');
var INS = path.join(REPO, 'plugins/nadlan-config/assets/instruments');
global.window = {};
require(path.join(INS, 'tools/mzakaut.js'));
require(path.join(INS, 'tools/mnomeff.js'));
var K = window.NLZK, N = window.NLNE;
var Z = require(path.join(INS, 'data/zakaut.json'));
var D = require(path.join(INS, 'data/boi-mortgage.json'));
var TODAY = '2026-11-06';

var fails = 0, n = 0;
function ok(cond, name, got) { n++; if (cond) console.log('  ok   ' + name + (got != null ? '  [' + got + ']' : '')); else { fails++; console.log('  FAIL ' + name + (got != null ? '  [' + got + ']' : '')); } }
function near(a, b, tol) { return Math.abs(a - b) <= (tol == null ? 0.5 : tol); }
function run(o) { var v = K.defaults(); Object.keys(o || {}).forEach(function (k) { v[k] = o[k]; }); return K.compute(v, Z, TODAY); }
function pts(r, k) { var p = r.parts.filter(function (x) { return x.k === k; })[0]; return p ? p.pts : null; }
function allText(r) { return K.lines(r, Z).map(function (l) { return l.label + ' ' + l.value + ' ' + l.note; }).join('\n') + '\n' + K.headline(r, Z).value + '\n' + K.sub(r, Z) + '\n' + K.statusText(r, Z) + '\n' + K.copyText(r, Z) + '\n' + K.payText(r); }
var LONG = /[\u2013\u2014]/, BANNED = new RegExp("(\\bAI\\b|\u05e1\u05d9\u05de\u05d5\u05dc\u05e6\u05d9\u05d4|\u05de\u05de\u05e9\u05e7|\u05de\u05d5\u05d3\u05dc|\u05d3\u05de\u05d5)");  // escaped, so this file holds none of them
var texts = [];
var FAM = { profile: 'family', years: 3, children: 2, sib1: 2, sib2: 4, svc1: 24, svc2: 20 };

console.log('data: zakaut.json checked ' + Z.checked + ', S3 updated ' + Z.sources.S3.updated + '; boi-mortgage by_bank ' + D.by_bank.months[D.by_bank.months.length - 1]);

console.log('\n0. the data file');
ok(Z.checked === '2026-11-06', 'zakaut.json carries "checked": "2026-11-06"', Z.checked);
ok(['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'S11', 'S12', 'S13', 'S14'].every(function (k) { return /^https:\/\/www\.gov\.il\//.test(Z.sources[k].url) && (Z.sources[k].updated || Z.sources[k].published); }), 'S1 to S14: a gov.il URL and a page date each');
ok(Z.bands.rows.length === 11 && Z.bands.rows[0][2] === 54240 && Z.bands.rows[10][2] === 161665 && Z.bands.rows[10][3] === 1617, 'S3 / S7 band table: 11 rows, 54,240 to 161,665, top service 1,617 a month');
var BLOCKS = ['vet_family', 'bands', 'vet_single', 'single_parent', 'olim_family', 'olim_single', 'disability', 'service', 'reserve', 'priority', 'ten_plus', 'negev', 'frontline', 'terms', 'prepay', 'process', 'banks', 'binding'];
var noSrc = BLOCKS.filter(function (k) { return !Z[k] || !/^S\d+$/.test(Z[k].src) || !Z.sources[Z[k].src]; });
ok(noSrc.length === 0, 'every table block names a source id that exists in sources', noSrc.join() || BLOCKS.length + ' blocks');

console.log('\n1. a family married 3 years, 2 children, siblings 2 and 4, service 24 and 20 months');
var a = run(FAM); texts.push(allText(a));
ok(pts(a, 'marriage') === 350, 'marriage, 3 full years: 350 (S3)', pts(a, 'marriage'));
ok(pts(a, 'children') === 500, 'children, 2: 500 (S3)', pts(a, 'children'));
ok(pts(a, 'sib1') === 100 && pts(a, 'sib2') === 400, 'siblings counted per spouse: 2 = 100, 4 = 400 (S3)', pts(a, 'sib1') + ' + ' + pts(a, 'sib2'));
ok(a.points === 1350, 'total 1,350 points', a.points);
ok(a.points !== 1500 && a.basic !== 85250, 'not the zakaut.com error (6 siblings summed = 650 points, 1,500 total, 85,250)', a.points);
ok(a.band.from === 1000 && a.band.to === 1399 && a.basic === 62400, 'band 1,000 to 1,399: basic loan 62,400 (S3)', a.basic);
ok(a.months === 44 && a.svcAmt === 27456, 'service supplement 44 months x 624 = 27,456 (S7)', a.svcAmt);
ok(a.total === 89856 && a.amountVerified === true, 'total 89,856 ILS, a veteran family: the S3 amount, no unverified label', a.total);
ok(K.headline(a, Z).value === '89,856 ₪', 'headline "89,856 ₪"', K.headline(a, Z).value);
var aL = K.lines(a, Z);
ok(aL.filter(function (l) { return l.kind === 'amt' || l.kind === 'pts'; }).every(function (l) { return l.src.length > 0; }), 'every points and amount line carries a source id');
ok(aL.some(function (l) { return l.src.indexOf('S7') > -1; }) && K.srcTag(Z, 'S3') === 'gov.il · עודכן 30.3.2026' && K.srcTag(Z, 'S4') === 'gov.il · פורסם 29.9.2021', 'source tags carry the page date (S3 updated 30.3.2026, S4 published 29.9.2021)', K.srcTag(Z, 'S3'));
var a2 = run(Object.assign({}, FAM, { zone: 'a' })); texts.push(allText(a2));
ok(a2.basic === 85250 && a2.zoneLift, 'zone א: a family gets the 1,500-point amount, 85,250 (S3, S8)', a2.basic);
ok(a2.svcAmt === 37488 && a2.zoneAmt === 100000 && a2.zoneFirst === 633 && a2.total === 222738, 'zone א: service 44 x 852 = 37,488, plus 100,000 at 4.5% (first payment 633): 222,738', a2.total);
var a3 = run(Object.assign({}, FAM, { zone: 'b' }));
ok(a3.basic === 62400 && a3.zoneAmt === 70000 && a3.zoneFirst === 443 && a3.total === 159856, 'zone ב: 70,000 (first payment 443), basic unchanged: 159,856', a3.total);
ok(near(K.pmt(100000, 0.045 / 12, 240), 633) && near(K.pmt(70000, 0.045 / 12, 240), 443), 'S8 first payments 633 / 443 = Spitzer of 100,000 / 70,000 at 4.5% for 20 years', K.pmt(100000, 0.045 / 12, 240).toFixed(2));
var a4 = run(Object.assign({}, FAM, { res1: true, res1d: 90 }));
ok(a4.resPct === 3 && a4.resAmt === 1872 && a4.total === 91728, 'reserve 90 full days: 0.5% per 15 days (S2) = 3% of 62,400 = 1,872; total 91,728', a4.resAmt);
ok(run(Object.assign({}, FAM, { res1: true, res1d: 30 })).resAmt === 1248, 'reserve 30 days: the 2% minimum (S7) = 1,248');
ok(run(Object.assign({}, FAM, { res1: true, res1d: 400 })).resAmt === 6240, 'reserve 400 days: the 10% maximum a person (S7) = 6,240');
var a5 = run(Object.assign({}, FAM, { svc1: 36, svc2: 36, res1: true, res1d: 300, res2: true, res2d: 300 }));
ok(a5.capCut === 16848 && a5.svcRes === 40560, 'service 72% + reserve 20% > 65%: capped at 65% of 62,400 = 40,560 (S7)', a5.svcRes);
var a6 = run(Object.assign({}, FAM, { svc1: 40, svc2: 20, svc2t: 'civic' }));
ok(a6.svc[0].c === 36 && a6.svc[1].c === 12 && a6.svcAmt === 48 * 624, 'service counted at most 36 months (S16), civic service 12 (S7)', a6.svc[0].c + ' + ' + a6.svc[1].c);
ok(run(Object.assign({}, FAM, { married: '2023-11-05' })).years === 3 && pts(run(Object.assign({}, FAM, { married: '2023-11-07' })), 'marriage') === 300, 'marriage date 5.11.2023: 3 full years; 7.11.2023: 2 years, 300 points');
var a7 = run(Object.assign({}, FAM, { rate: '2.5', term: 30 }));
ok(near(a7.pay, 355.04, 0.01), 'rate typed from the certificate, 2.5% for 30 years on 89,856: first payment 355.04', a7.pay.toFixed(2));
ok(run(FAM).pay === null && !/\d/.test(K.payText(run(FAM))), 'no rate typed: no payment and no rate number anywhere');

console.log('\n2. a veteran single aged 35 (S4)');
var s0 = run({ profile: 'single', age: 35, sib1: 0, svc1: 24 }); texts.push(allText(s0));
ok(pts(s0, 'age') === 450 && s0.points === 450, 'age 35: 300 at 32 + 3 x 50 = 450 points', s0.points);
ok(s0.status === 'noband' && s0.basic === 0 && s0.total === 0 && K.headline(s0, Z).value === '450 נקודות', 'below the S3 table (599): the points, no shekel figure', K.headline(s0, Z).value);
var s4 = run({ profile: 'single', age: 35, sib1: 4, svc1: 24 }); texts.push(allText(s4));
ok(s4.points === 850 && s4.basic === 54240 && s4.amountVerified === false, 'with 4 siblings: 450 + 400 = 850, band 599 to 999, 54,240 (unverified mapping)', s4.points);
ok(K.sub(s4, Z).indexOf('לפי טבלת הסכומים למשפחות ותיקות (S3); לבדוק בתעודת הזכאות') > -1 && K.headline(s4, Z).value === '850 נקודות', 'the headline is the points; the shekel figure carries the label of eligibility.md section 4', K.sub(s4, Z));
ok([[31, 250], [45, 950], [46, 1200], [47, 1250], [48, 1300]].every(function (x) { return pts(run({ profile: 'single', age: x[0], sib1: 0 }), 'age') === x[1]; }), 'S4 ladder: 31 = 250, 45 = 950, 46 = 1,200, 47 = 1,250, 48 = 1,300');
ok(run({ profile: 'single', age: 60, sib1: 6 }).points === 1690, 'age 60 with 6 siblings: capped at 1,690 (S4)');
ok(run({ profile: 'single', age: 25, sib1: 0, svc1: 24 }).status === 'young' && run({ profile: 'single', age: 25, sib1: 5, svc1: 24, zone: 'a' }).points === 630 && run({ profile: 'single', age: 25, sib1: 5, svc1: 24, zone: 'a' }).status === 'ok' && run({ profile: 'single', age: 25, sib1: 5, svc1: 0, zone: 'a' }).status === 'young', 'age 25: not eligible outside a priority zone or without service; in zone א after service: 30 + 600 = 630 points (S4)');
ok(run({ profile: 'single', age: 19 }).status === 'age', 'age 19: not eligible (from 21)');

console.log('\n3. an olim family in its second year (S11)');
var o1 = run({ profile: 'olim_family', israel: 1, children: 2, svc1: 0, svc2: 0 }); texts.push(allText(o1));
ok(pts(o1, 'seniority') === 250 && pts(o1, 'fixed') === 730, '1 full year in Israel: seniority 250, fixed 730', pts(o1, 'seniority'));
ok(pts(o1, 'floor') === 320 && o1.points === 1800, '250 + 500 + 730 = 1,480, floor from the second year 1,800', o1.points);
ok(o1.basic === 117985 && o1.amountVerified === false && K.headline(o1, Z).value === '1,800 נקודות', 'band 1,800 to 1,899: 117,985, labelled; headline = points', o1.basic);
ok(run({ profile: 'olim_family', israel: 0, children: 2, svc1: 0, svc2: 0 }).points === 1700, 'first year: 30 + 500 + 730 = 1,260, floor 1,700');
var o7 = run({ profile: 'olim_family', israel: 7, children: 3, svc1: 0, svc2: 0 });
ok(o7.points === 1930 && o7.basic === 128930 && o7.olimSupp === 28370 && o7.total === 157300, '7 years, 3 children: 550 + 650 + 730 = 1,930, 128,930 + 28,370 at 3% for 28 years = 157,300', o7.total);
ok(run({ profile: 'olim_family', israel: 5, children: 1, svc1: 0, svc2: 0 }).olimSupp === 19630 && run({ profile: 'olim_family', israel: 8, children: 1, svc1: 0, svc2: 0 }).olimSupp === 43630, 'olim supplement: 5 years 19,630; 8 years 43,630');
var o4 = run({ profile: 'olim_family', israel: 4, children: 1, svc1: 0, svc2: 0 });
ok(o4.olimSupp === 0 && !K.lines(o4, Z).some(function (l) { return /תוספת למשפחת עולים/.test(l.label); }), '4 years: no supplement, and no "0 ₪" supplement line');

console.log('\n4. a family under 599 points (S3)');
var u = run({ profile: 'family', years: 1, children: 0, sib1: 1, sib2: 1, svc1: 24, svc2: 0 }); texts.push(allText(u));
ok(u.points === 350 && u.status === 'nopoints', '250 + 0 + 50 + 50 = 350 points: no loan by points', u.points);
ok(u.basic === 0 && u.svcAmt === 0 && u.total === 0 && K.headline(u, Z).value === 'אין הלוואה לפי הניקוד', 'no basic, no service supplement; the headline says so in words, not "0 ₪"', K.headline(u, Z).value);
ok(/רק לתוספות סיוע/.test(K.statusText(u, Z)), 'the S3 sentence about locality supplements is shown');
var uz = run({ profile: 'family', years: 1, children: 0, sib1: 1, sib2: 1, svc1: 0, svc2: 0, zone: 'a' });
ok(uz.total === 100000 && uz.basic === 0, 'the same family in zone א: only the 100,000 locality supplement', uz.total);

console.log('\n5. the other profiles');
var sp = run({ profile: 'single_parent', children: 2, svc1: 0 });
ok(sp.points === 2200 && sp.basic === Z.single_parent.amount && sp.basic === 161665, 'single parent: 2,200 points = 161,665, as S5 prints it', sp.basic);
ok(run(Object.assign({}, FAM, { profile: 'dis_family', disF: '75one' })).basic === 96190, 'disabled family 75%: 1,350 + 200 = 1,550, floor 1,600: 96,190 (S10)');
ok(run(Object.assign({}, FAM, { profile: 'wheelchair' })).points === 2200, 'wheelchair-bound family: floor 2,200 (S10)');
var dsa = run({ profile: 'dis_single', disS: 'a', age: 35, sib1: 0, svc1: 0 }), dsb = run({ profile: 'dis_single', disS: 'b', age: 35, sib1: 0, svc1: 0 });
ok(dsa.points === 1500 && dsa.basic === 85250 && dsb.points === 2000 && dsb.basic === 139825, "disabled single age 35: degree א' 450 + 200 = 650 -> 1,500; degree ב' 2,000 (S10)", dsa.points + ' / ' + dsb.points);
var t1 = run({ profile: 'family', years: 12, children: 3, sib1: 0, sib2: 0, svc1: 0, svc2: 0, tp_stay: true, tp_fam: true, tp_income: true });
ok(t1.points === 1450 && t1.basic === 74350 && t1.tp === 132000 && t1.total === 206350, '10 פלוס: 12 years (800) + 3 children (650) = 1,450, 74,350 + 132,000 = 206,350 (S9)', t1.total);
var t2 = run({ profile: 'family', years: 12, children: 3, sib1: 0, sib2: 0, svc1: 0, svc2: 0, tp_stay: true, tp_fam: true, tp_income: true, zone: 'a' });
ok(t2.tp === 0 && t2.tenplus.why.join().indexOf('4 ילדים') > -1, 'the same family in a priority zone: 10 פלוס needs 4 children (S9)', t2.tenplus.why.join(' | '));
var ol = run({ profile: 'oleh', age: 50, israel: 8, svc1: 0 }); texts.push(allText(ol));
ok(ol.points === 1000 && ol.olehSupp === 10895 && ol.total === 73295, 'oleh single, 50, 8 years: 600 (S11 ladder, labelled) + 400 = 1,000; 62,400 + 10,895 = 73,295', ol.total);
ok(ol.parts.filter(function (p) { return p.k === 'seniority'; })[0].warn.length > 0, "the olim singles' seniority ladder is labelled unverified");
var ng = run(Object.assign({}, FAM, { negev: true })); texts.push(allText(ng));
ok(ng.total === 89856 && K.lines(ng, Z).some(function (l) { return l.value === '48,000 עד 84,000 ₪ לפי היישוב'; }), 'Negev: the 48,000 to 84,000 range in words only, never added to the total');
ok(!/ריבית[^\n]*\d%/.test(allText(run(FAM))), 'no eligible-loan rate number is printed (the rule stays in words)');
ok(K.compute(Object.assign(K.defaults(), { children: 'x' }), Z, TODAY).error.field === 'children', 'a bad children value is an error on its field');

console.log('\n6. nominal and effective (mnomeff)');
ok(near(N.toEff(4.5), 4.5939825, 1e-6), '4.5% nominal (monthly) = 4.5940% effective', N.toEff(4.5).toFixed(4));
ok(near(N.toNom(4.5), 4.4097713, 1e-6), '4.5% effective = 4.4098% nominal', N.toNom(4.5).toFixed(4));
ok(near(N.toNom(N.toEff(4.5)), 4.5, 1e-9) && near(N.toEff(N.toNom(4.5)), 4.5, 1e-9), 'both ways round trip at 4.5%');
var SY = N.system(D);
ok(SY && SY.month === D.by_bank.months[D.by_bank.months.length - 1] && SY.tracks[0].k === 'fixed_nl' && SY.tracks[0].e === D.by_bank.rate.system.fixed_nl[D.by_bank.months.length - 1], 'the example is the all-banks fixed not linked effective rate of the latest month', SY.month + ' ' + SY.tracks[0].e);
ok(SY.tracks[0].e === 4.7162 ? near(SY.tracks[0].n, 4.6172249, 1e-6) : near(SY.tracks[0].n, N.toNom(SY.tracks[0].e), 1e-12), 'system average 4.7162% effective (9.2026) = 4.6172% nominal', SY.tracks[0].n.toFixed(4));
ok(near(N.toEff(SY.tracks[0].n), SY.tracks[0].e, 1e-9), 'system average: back to effective');
ok(/^דוגמה: בספטמבר 2026 /.test(N.exampleText(SY)) && N.exampleText(SY).indexOf('4.72%') > -1 && N.exampleText(SY).indexOf('4.62%') > -1, 'the example names its month: ' + N.exampleText(SY));
ok(N.sentence(N.convert('n', '4.5')) === '4.50% נומינלית בשנה = 0.375% בחודש = 4.59% אפקטיבית בשנה', 'the result sentence at 4.5% nominal', N.sentence(N.convert('n', '4.5')));
ok(N.convert('e', '4,5').n.toFixed(4) === '4.4098' && N.convert('n', '').error && N.convert('n', '45').error, 'a comma decimal is read; empty or over 30% is an error');
texts.push(N.exampleText(SY), N.sentence(N.convert('e', '4.7162')));

console.log('\n7. words and files');
var joined = texts.join('\n');
ok(!LONG.test(joined), 'no long dash in any generated sentence');
ok(!BANNED.test(joined), 'no banned word in any generated sentence');
ok(!/(^|[^\d,])0 ₪/.test(joined), 'no "0 ₪" in any generated sentence (no fake zero)');
var files = ['tools/mzakaut.js', 'tools/mnomeff.js', 'data/zakaut.json'].map(function (f) { return fs.readFileSync(path.join(INS, f), 'utf8'); });
ok(files.every(function (s) { return !LONG.test(s); }), 'no long dash in mzakaut.js, mnomeff.js or zakaut.json');
ok(files.slice(0, 2).every(function (s) { return !BANNED.test(s); }), 'no banned word in the two tool files');
ok(!/fetch\(|XMLHttpRequest|sendBeacon|<form/.test(files[0] + files[1]), 'neither tool sends anything (no fetch, beacon or form of its own)');

console.log('\n' + (n - fails) + ' of ' + n + ' passed' + (fails ? ', ' + fails + ' FAILED' : ''));
process.exit(fails ? 1 : 0);
