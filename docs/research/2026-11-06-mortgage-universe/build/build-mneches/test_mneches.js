/* HAD-675 · node test of mneches ("כמה אפשר לקבל על דירה קיימת"), the loan against a home the reader already owns.
   Run from anywhere:  node docs/research/2026-11-06-mortgage-universe/build/build-mneches/test_mneches.js
   Loads tools/mneches.js (window.NLNC) with a fake window, and the real data files data/boi-mortgage.json and data/mneches.json.
   Every expected number is a literal worked out by hand or by an independent 40-digit Decimal calculation of the same annuity
   formula (P x r / (1 - (1 + r)^-n)), never recomputed from the tool. Rules: directive 329 version 13 (circular 2852, 30.6.2026)
   and the Q&A file of 8.2.2026, as recorded in mneches.json. Exit code 1 on a failure. */
'use strict';
var path = require('path'), fs = require('fs'), crypto = require('crypto');
var HERE = __dirname, REPO = path.resolve(HERE, '../../../../..');
var INS = path.join(REPO, 'plugins/nadlan-config/assets/instruments');
global.window = {};
require(path.join(INS, 'tools/mneches.js'));
var K = window.NLNC;
var D = require(path.join(INS, 'data/boi-mortgage.json'));
var N = require(path.join(INS, 'data/mneches.json'));

var fails = 0, n = 0;
function ok(cond, name, got) { n++; if (cond) console.log('  ok   ' + name + (got != null ? '  [' + got + ']' : '')); else { fails++; console.log('  FAIL ' + name + (got != null ? '  [' + got + ']' : '')); } }
function near(a, b, tol) { return Math.abs(a - b) <= (tol == null ? 0.5 : tol); }
function run(o) { var v = K.defaults(); Object.keys(o || {}).forEach(function (k) { v[k] = o[k]; }); return K.compute(v, D, N); }
function line(r, start) { return K.lines(r).filter(function (l) { return l.label.indexOf(start) === 0; })[0] || null; }
var texts = [];
function allText(r) { var t = K.lines(r).map(function (l) { return l.label + ' ' + l.value + ' ' + l.note + ' ' + l.tag; }).join('\n') + '\n' + K.headline(r).value + '\n' + K.headline(r).label + '\n' + K.sub(r) + '\n' + K.purposeNote(r) + '\n' + K.copyText(r, N); texts.push(t); return t; }
var LONG = /[\u2013\u2014]/;  // the en and em dash, escaped
var BANNED = new RegExp('(^|[^\u05d0-\u05ea])[\u05d5\u05d4\u05d1\u05db\u05dc\u05de\u05e9]?(\u05de\u05de\u05e9\u05e7|\u05d3\u05de\u05d5|\u05d4\u05d3\u05d2\u05de\u05d4|\u05e1\u05d9\u05de\u05d5\u05dc\u05e6\u05d9\u05d4|\u05de\u05e0\u05d2\u05e0\u05d5\u05df|\u05d0\u05d9\u05e0\u05d8\u05e8\u05d0\u05e7\u05d8\u05d9\u05d1\u05d9|\u05d4\u05de\u05e2\u05e8\u05db\u05ea|\u05d4\u05e4\u05dc\u05d8\u05e4\u05d5\u05e8\u05de\u05d4|\u05d8\u05db\u05e0\u05d5\u05dc\u05d5\u05d2\u05d9\u05d4)(?![\u05d0-\u05ea])');  // escaped, so this file holds none of them; whole words, one prefix letter allowed ("הקודמות" is not a hit)
var OWN5 = { src: 'own', rate: '5' };

console.log('data: mneches.json checked ' + N.checked + '; directive 329 v' + N.sources.D329.version + ' (' + N.sources.D329.date + '); any-purpose month ' + N.anyp.month + '; by_bank ' + D.by_bank.latest.month);

console.log('\n0. the rules and the data files');
var R = K.rules(D, N);
ok(R.any === 0.5 && R.upto === 0.7 && R.above === 200000 && R.pti === 0.5 && R.risk === 0.4 && R.termMax === 30 && R.exempt === 120000, 'rules: 50%, 70% with 200,000 above 50%, PTI 50% (40% risk), 30 years, exemption 120,000', JSON.stringify([R.any, R.upto, R.above, R.pti, R.termMax, R.exempt]));
ok(D.rules.any_purpose.ltv === N.rules.any_ltv.value && D.rules.any_purpose.ltv_upto === N.rules.relief.ltv_upto && D.rules.any_purpose.above_cap === N.rules.relief.above_cap && D.rules.pti_max === N.rules.pti_max.value && D.rules.term_max === N.rules.term_max.value,
  'boi-mortgage.json rules and mneches.json (from the directive text) agree');
ok(N.checked === '2026-11-06' && N.sources.D329.version === 13 && N.sources.D329.date === '2026-06-30' && N.sources.D329.circular === 'ח-06-2852' && N.sources.QA329.date === '2026-02-08', 'directive 329 version 13 (circular 2852, 30.6.2026) and the Q&A of 8.2.2026, checked 6.11.2026');
ok(['D329', 'QA329'].every(function (k) { return /^https:\/\/(www\.)?boi\.org\.il\//.test(N.sources[k].url); }) && /^https:\/\/edge\.boi\.gov\.il\//.test(N.sources.SDMX.url), 'every source is a Bank of Israel URL');
var RAW = path.join(REPO, 'docs/research/2026-11-06-mortgage-universe/gov/raw');
function sha(f) { return fs.existsSync(f) ? crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex') : null; }
ok(sha(path.join(RAW, 'boi-h2852-directive329-2026-06-30.pdf')) === N.sources.D329.sha256 && sha(path.join(RAW, 'boi-202601.pdf')) === N.sources.QA329.sha256, 'the recorded SHA-256 of the two boi.org.il files match the copies in gov/raw');
var csv = fs.readFileSync(path.join(REPO, N.sources.SDMX.copy), 'utf8');
ok(N.anyp.tracks.concat([{ id: N.anyp.loans.id, rate: N.anyp.loans.value }, { id: N.anyp.pti.id, rate: N.anyp.pti.value }]).every(function (t) { return new RegExp('^' + t.id + ',.*,2026-08,' + String(t.rate).replace('.', '\\.') + ',', 'm').test(csv); }),
  'the any-purpose rates, count and PTI in mneches.json are the values of the saved SDMX file');
var bsum = N.anyp.ltv_bands.rows.reduce(function (a, x) { return a + x.vol_k; }, 0);
ok(bsum === N.anyp.volume_k.value && near(N.anyp.tracks[0].vol_k + N.anyp.tracks[1].vol_k + 205, N.anyp.volume_k.value, 1), 'LTV bands sum to the volume, 532,545 thousand; the tracks plus 205 foreign currency within 1', bsum);
var csvAll = fs.readFileSync(path.join(REPO, N.sources.SDMX.copy), 'utf8');
ok(/BNK_99034_LR_BIR_MRTG_153,Average payback rate out of income - Consumer loans other than overdrafts-with housing collateral/.test(csvAll), 'the any-purpose series family is "Consumer loans other than overdrafts, with housing collateral" in the official file');

console.log('\n1. the opening example: 2,800,000, balance 350,000, any purpose (hand-worked)');
var a = run({}); allText(a);
ok(a.cap === 1400000 && a.ltvRoom === 1050000, 'LTV: 50% of 2,800,000 = 1,400,000, minus 350,000 = 1,050,000', a.ltvRoom);
ok(a.reliefCap === 1600000 && a.reliefRoom === 1250000, 'section 10a: min(70% = 1,960,000; 50% + 200,000 = 1,600,000) = 1,600,000, minus 350,000 = 1,250,000', a.reliefRoom);
ok(a.disp === 23500 && a.half === 11750 && a.payRoom === 8600, 'PTI: 25,000 - 1,500 = 23,500; 50% = 11,750; minus the existing 3,150 = 8,600 a month', a.payRoom);
ok(a.key === 'anyp' && near(a.per1 * 1e6, 7329.8283, 0.0005), 'rate: the any-purpose average of 8.2026 (6.53% x 79.20%, 5.33% x 20.80%), 7,329.83 a month per 1,000,000 over 20 years', (a.per1 * 1e6).toFixed(4));
ok(a.incMax === 1173288, 'by income: 8,600 / 7,329.83 per million = 1,173,288', a.incMax);
ok(a.binds === 'ltv' && a.best === 1050000 && a.gap === 123288, 'the LTV rule binds, by 123,288; the headline is 1,050,000', a.binds + ' ' + a.gap);
ok(near(a.pay, 7696.32, 0.01) && near(a.total, 1847116.74, 0.02), 'payment 7,696.32, total 1,847,116.74 over 240 months', a.pay.toFixed(2));
ok(near(a.ptiAfter, 0.461546, 1e-6), 'PTI after the loan: (3,150 + 7,696.32) / 23,500 = 46.15%', (100 * a.ptiAfter).toFixed(2));
ok(K.headline(a).value === '1,050,000 ₪', 'headline "1,050,000 ₪"', K.headline(a).value);
ok(line(a, 'לפי כלל המימון').tag === 'קובע' && line(a, 'לפי ההכנסה').tag === '' && /^מרווח של 123,288 ₪/.test(line(a, 'לפי ההכנסה').note), 'the LTV line carries "קובע", the income line the spare 123,288');
ok(line(a, 'ההחזר מההכנסה').note.indexOf('(סעיף 6)') > -1, 'PTI 46.2% > 40%: the section 6 note is shown');
ok(a.table.map(function (x) { return x.years; }).join() === '10,15,20,25,30' && a.table[2].best === a.best && a.table[0].incMax === 764788 && a.table[0].binds === 'income' && a.table[1].incMax === 1000808 && a.table[3].incMax === 1299338 && a.table[4].incMax === 1391471,
  'term table: 10 = 764,788 (income), 15 = 1,000,808, 25 = 1,299,338, 30 = 1,391,471', a.table.map(function (x) { return x.incMax; }).join());
ok(near(a.table[3].pay, 6949.69, 0.01) && near(a.table[4].pay, 6489.53, 0.01) && near(a.table[0].pay, 8600, 0.01), 'term table payments: 10 years 8,600 (the full room), 25 years 6,949.69, 30 years 6,489.53');

console.log('\n2. an income-bound case (own rate 5%, 20 years)');
var b = run(Object.assign({ income: 18000, other: 2000 }, OWN5)); allText(b);
ok(near(b.per1 * 1e6, 6599.5574, 0.0001), '5% / 12 over 240 months: 6,599.5574 a month per 1,000,000', (b.per1 * 1e6).toFixed(4));
ok(b.payRoom === 4850 && b.incMax === 734897, 'room 50% x 16,000 - 3,150 = 4,850; by income 734,897', b.incMax);
ok(b.binds === 'income' && b.best === 734897 && b.gap === 315103, 'income binds, 315,103 below the LTV room of 1,050,000', b.gap);
ok(near(b.pay, 4850, 0.01) && near(b.ptiAfter, 0.5, 1e-6), 'the payment fills the room exactly: 4,850, PTI 50%', b.pay.toFixed(2));
ok(K.sub(b).indexOf('ההכנסה קובעת') === 0 && K.sub(b).indexOf('315,103 ₪ יותר') > -1, 'the sub says the income binds and by how much', K.sub(b).slice(0, 60));

console.log('\n3. zero balance');
var c = run(Object.assign({ value: 2000000, balance: 0, epay: 5000, income: 40000, other: 0 }, OWN5)); allText(c);
ok(c.cap === 1000000 && c.ltvRoom === 1000000 && c.reliefRoom === 1200000, 'no balance: 1,000,000 by LTV; relief min(1,400,000; 1,200,000) = 1,200,000', c.ltvRoom + ' / ' + c.reliefRoom);
ok(c.epay === 0 && c.payRoom === 20000, 'no balance: a typed existing payment is not counted (room 20,000)', c.payRoom);
ok(c.incMax === 3030506 && c.binds === 'ltv' && c.best === 1000000, 'by income 3,030,506; the LTV rule binds at 1,000,000');
ok(near(c.pay, 6599.56, 0.01) && near(c.total, 1583893.77, 0.02) && near(c.interest, 583893.77, 0.02), '1,000,000 at 5% for 20 years: 6,599.56 a month, 1,583,893.77 in all, 583,893.77 interest');
ok(line(c, 'פחות יתרת המשכנתא').value === 'אין משכנתא' && !line(c, 'פחות ההחזר על המשכנתא'), 'the ledger says "אין משכנתא" and has no existing-payment line');

console.log('\n4. a balance above the cap: "no room", never a negative amount');
var d = run({ value: 1500000, balance: 900000 }); allText(d);
ok(d.cap === 750000 && d.ltvRoom === 0 && d.best === 0 && d.kind === 'noroom', '900,000 on 1,500,000 (60%): cap 750,000, no room, kind "noroom"', d.ltvRoom);
ok(K.headline(d).value === 'אין מקום להלוואה נוספת' && line(d, 'לפי כלל המימון').value === 'אין מקום', 'headline "אין מקום להלוואה נוספת", ledger "אין מקום"');
ok(d.reliefRoom === 50000 && K.sub(d).indexOf('עד 50,000 ₪') > -1, 'relief: min(1,050,000; 950,000) - 900,000 = 50,000, said in the sub', d.reliefRoom);
var e = run({ value: 1000000, balance: 800000 }); allText(e);
ok(e.ltvRoom === 0 && e.reliefRoom === 0 && K.sub(e).indexOf('גם בהקלה של סעיף 10א') > -1, '800,000 on 1,000,000: no room, also under the 70% relief');
ok(!/(^|[^\d,.])-[\d]/.test(allText(d) + allText(e)), 'no amount printed with a hyphen minus (negative) anywhere');
ok(d.table.every(function (x) { return x.best === 0; }), 'the term table has no amount when there is no room');

console.log('\n5. the 120,000 exemption (sections 11 and 12.2) and purpose rules');
var f = run(Object.assign({ value: 2000000, balance: 0, income: 3000, other: 2000 }, OWN5)); allText(f);
ok(f.incMax === 75762 && f.exemptOn && f.best === 120000 && f.binds === 'exempt', 'any purpose, income room 500 = 75,762, but up to 120,000 the PTI limit does not apply: 120,000', f.best);
var fb = run(Object.assign({ value: 2000000, balance: 0, income: 3000, other: 2000, purpose: 'buy' }, OWN5));
var fk = run(Object.assign({ value: 2000000, balance: 0, income: 3000, other: 2000, purpose: 'kids' }, OWN5));
var fc = run(Object.assign({ value: 2000000, balance: 0, income: 3000, other: 2000, purpose: 'close' }, OWN5)); allText(fb); allText(fk); allText(fc);
ok(fb.best === 75762 && !fb.exemptOn && fk.best === 75762 && fc.best === 120000, 'buying another home and helping children: no exemption (75,762); closing loans: exemption (120,000)');
ok(fb.reliefRoom === null && fk.reliefRoom === null && fc.reliefRoom === 1200000 && !line(fb, 'בשיקול דעת הבנק'), 'the 70% relief only for any purpose and closing loans');
var g = run({ value: 300000, balance: 100000, income: 3000, other: 2000 });
ok(g.ltvRoom === 50000 && g.exemptAmt === 50000 && g.best === 50000 && g.binds === 'ltv', 'exemption capped by the LTV room: 150,000 - 100,000 = 50,000', g.best);
var h1 = run({ value: 2000000, balance: 300000, epay: 6000, income: 10000, other: 0, purpose: 'buy' }); allText(h1);
var h2 = run({ value: 2000000, balance: 300000, epay: 6000, income: 10000, other: 0, purpose: 'any' });
ok(h1.payRoom === 0 && h1.kind === 'noincome' && K.headline(h1).value === 'אין מקום לפי ההכנסה' && h2.best === 120000, 'existing 6,000 on 10,000: no income room; buying "אין מקום לפי ההכנסה"; any purpose 120,000 (exempt)');
ok(K.purposeNote(fb).indexOf('75% לדירה יחידה, 70% לדירה חלופית ו־50% לדירה להשקעה (סעיף 2)') > -1, 'buying: one line on the new home\'s own caps (section 2)');
ok(K.purposeNote(fk).indexOf('(שו"ת 2.7)') > -1 && K.purposeNote(fk).indexOf('(נספח א, סעיף 1.3)') > -1 && K.purposeNote(fc).indexOf('(שו"ת 7.7)') > -1, 'parents: Q&A 2.7 and Annex A 1.3; closing loans: Q&A 7.7');

console.log('\n6. the rate sources');
ok(K.srcKey({ src: 'auto', purpose: 'any' }) === 'anyp' && K.srcKey({ src: 'auto', purpose: 'buy' }) === 'home' && K.srcKey({ src: 'home', purpose: 'any' }) === 'home', 'auto: any-purpose average, the housing mix when buying; a chosen source sticks');
ok(near(K.per1(K.rateSet('home', D, N), 25) * 1e6, 5428.2967, 0.0005) && D.headlines.filter(function (x) { return x.id === 'pay_1m_25y'; })[0].value === 5428, 'the housing mix of 9.2026: 1,000,000 over 25 years = 5,428.30, the same as the data headline 5,428');
var hm = run({ src: 'home' });
ok(hm.key === 'home' && hm.incMax > a.incMax && hm.best === 1050000, 'the housing mix (lower rates) carries more by income; LTV still binds at 1,050,000', hm.incMax);
ok(run({ src: 'own', rate: '25' }).error.field === 'rate' && run({ src: 'own', rate: '' }).error.field === 'rate' && run({ src: 'own', rate: '6,2' }).rs.rows[0].annual === 6.2, 'own rate: 25% and empty are errors on the field; "6,2" reads 6.2');
ok(K.ownStart(K.PURPOSES[0], N) === 6.61 && K.ownStart(K.PURPOSES[1], N) === 4.62, 'own rate opens at the fixed not linked average of 8.2026: 6.61% any purpose, 4.62% housing');
ok(K.rateHelp('home', K.rateSet('home', D, N), N, K.PURPOSES[0]).indexOf('6.61% מול 4.62%') > -1, 'the housing average is labelled, with the any-purpose price beside it (6.61% vs 4.62%)');

console.log('\n7. errors, the address, words and files');
ok(run({ value: '' }).error.field === 'value' && run({ income: '' }).error.field === 'income' && run({ years: 31 }).error.field === 'years' && run({ balance: 100000, epay: '' }).error.field === 'epay', 'missing value, income, existing payment, or 31 years: an error on its field');
ok(run({ value: '2,800,000', balance: '350,000' }).ltvRoom === 1050000, 'amounts typed with separators are read');
var st = K.dec(K.enc({ value: 1500000, balance: 0, epay: 0, purpose: 'kids', income: 30000, other: 0, years: 25, src: 'own', rate: '5.5' }));
ok(st && st.value === 1500000 && st.purpose === 'kids' && st.years === 25 && st.src === 'own' && st.rate === '5.5', 'the case survives #mneches= (encode, decode)');
ok(K.dec('!!') === null && K.dec(K.enc({ purpose: 'x', years: 17, src: 'y' })).purpose === 'any', 'a broken or foreign hash falls back to the defaults');
texts.push(K.dataLine(N, D));
ok(K.dataLine(N, D).indexOf('1,386 הלוואות') > -1 && K.dataLine(N, D).indexOf('532.5 מיליון ₪') > -1 && K.dataLine(N, D).indexOf('כ־384 אלף ₪') > -1 && K.dataLine(N, D).indexOf('23.97%') > -1, 'the data line: 1,386 loans, 532.5 million, about 384 thousand each (532,545,000 / 1,386 = 384,232), PTI 23.97% (8.2026)');
var joined = texts.join('\n');
ok(!LONG.test(joined), 'no long dash in any generated sentence');
ok(!BANNED.test(joined), 'no banned word in any generated sentence');
ok(!/(^|[^\d,.])0 ₪/.test(joined) && !/NaN|undefined|Infinity/.test(joined), 'no "0 ₪", NaN or undefined in any generated sentence');
var src = fs.readFileSync(path.join(INS, 'tools/mneches.js'), 'utf8'), dat = fs.readFileSync(path.join(INS, 'data/mneches.json'), 'utf8');
ok(!LONG.test(src) && !LONG.test(dat), 'no long dash in mneches.js or mneches.json');
ok(!BANNED.test(src) && !BANNED.test(dat), 'no banned word in mneches.js or mneches.json');
ok(!/fetch\(|XMLHttpRequest|sendBeacon|<form/.test(src), 'the tool sends nothing (no fetch, beacon or form of its own)');
ok(src.indexOf('<a href="https://nad-lan.co.il/mortgage-calculator/mortgage-for-any-purpose/">משכנתא לכל מטרה</a>') > -1 && /<h2 class="nli__title">כמה אפשר לקבל על דירה קיימת<\/h2>/.test(src), 'the guide link with the exact anchor "משכנתא לכל מטרה"; the title is "כמה אפשר לקבל על דירה קיימת"');

console.log('\n' + (n - fails) + ' of ' + n + ' passed' + (fails ? ', ' + fails + ' FAILED' : ''));
process.exit(fails ? 1 : 0);
