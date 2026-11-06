/* HAD-675 (mortgage universe, 6.11.2026) · node test of mrishum ("רישום משכנתה ואגרות").
   Run from anywhere:  node docs/research/2026-11-06-mortgage-universe/build/build-mrishum/test_mrishum.js
   Loads the repo file tools/mrishum.js (window.NLRS) with a fake window and the real data file data/rishum.json. Every expected
   total below was worked out by hand from the 2026 notices as gov/gov.md quotes them (land: 188 registration, additional, increase;
   188 amendment; redemption free when paid straight to the lender, 188 when deposited; 188 warning note, 127 its deletion; extract
   88 at the counter, 18 online; 188 inheritance. Pledges: 45 a year at the counter, 38 online, up to 5 years, free from the 6th;
   cancellation free; change 45 / 38; search 38 / 12) and written as a literal, never recomputed from the tool. Exit code 1 on a
   failure. The output goes to the console; test_mrishum.out.txt keeps the last run. */
'use strict';
var path = require('path'), fs = require('fs');
var HERE = __dirname, REPO = path.resolve(HERE, '../../../../..');
var INS = path.join(REPO, 'plugins/nadlan-config/assets/instruments');
global.window = {};
require(path.join(INS, 'tools/mrishum.js'));
var K = window.NLRS;
var D = JSON.parse(fs.readFileSync(path.join(INS, 'data/rishum.json'), 'utf8'));

var fails = 0, n = 0;
function ok(cond, name, got) { n++; if (cond) console.log('  ok   ' + name + (got != null ? '  [' + got + ']' : '')); else { fails++; console.log('  FAIL ' + name + (got != null ? '  [' + got + ']' : '')); } }
function run(o) { var v = K.defaults(); Object.keys(o || {}).forEach(function (k) { v[k] = o[k]; }); return K.compute(v, D); }
function line(r, k) { return r.lines.filter(function (l) { return l.k === k; })[0] || null; }
function texts(r) {  // every visible or copied word of a path
  var h = K.headline(r, D), w = K.whereText(r, D), dc = K.docs(r, D);
  return [h.label, h.value, h.sub, w.he, dc.note].concat(
    r.lines.map(function (l) { return l.label + ' ' + l.note + ' ' + (l.shown || ''); }),
    K.timeList(r, D).map(function (x) { return x.he; }), K.steps(r, D).map(function (x) { return x.he; }),
    dc.items.map(function (x) { return x.he; }), K.unverified(r, D).map(function (x) { return x.he; }),
    r.ex ? [r.ex.why] : [], [K.copyText(r, D, ''), K.checklistText(r, D), K.sourceLine(D)]).join('\n');
}
var LONG = /[\u2013\u2014]/;
var BANNED = new RegExp('\u05de\u05de\u05e9\u05e7|(^|[^\u0590-\u05ff])\u05d3\u05de\u05d5([^\u0590-\u05ff]|$)|\u05d4\u05d3\u05d2\u05de\u05d4|\u05e1\u05d9\u05de\u05d5\u05dc\u05e6\u05d9\u05d4|\u05de\u05e0\u05d2\u05e0\u05d5\u05df|\u05d0\u05d9\u05e0\u05d8\u05e8\u05d0\u05e7\u05d8\u05d9\u05d1\u05d9|\u05d4\u05de\u05e2\u05e8\u05db\u05ea|\u05d4\u05e4\u05dc\u05d8\u05e4\u05d5\u05e8\u05de\u05d4|\u05d8\u05db\u05e0\u05d5\u05dc\u05d5\u05d2\u05d9\u05d4');
var SIXTY = new RegExp('(^|[^\\d])6' + '0[\\s\\-]*(\u05d9\u05de\u05d9\u05dd|\u05d9\u05d5\u05dd|days?)', 'i');  // built from parts, so this file holds no such string

console.log('data: rishum.json checked ' + D.checked + ', year ' + D.year + ', in force ' + D.in_force);

console.log('\n0. the data file');
ok(D.key === 'rishum' && D.checked === '2026-11-06' && D.year === 2026 && D.in_force === '2026-01-01', 'key "rishum", "checked": "2026-11-06", year 2026 in force 1.1.2026');
var srcKeys = Object.keys(D.src);
ok(srcKeys.every(function (k) { var s = D.src[k]; return s.title && /^https:\/\//.test(s.url); }), 'every src has a title and an https URL', srcKeys.length + ' sources');
ok(srcKeys.filter(function (k) { return !D.src[k].read; }).sort().join() === 'gov_forms,ila_form', 'every src was read on 6.11.2026 except the two official forms (link only)',
  srcKeys.filter(function (k) { return !D.src[k].read; }).join());
ok(D.src.gov_fees.published === '2025-12-23' && D.src.gov_fees.updated === '2025-12-24' && D.src.gov_fees.url === 'https://www.gov.il/he/pages/fees-2026', 'gov.il fees-2026: published 23.12.2025, updated 24.12.2025');
ok(D.src.reshumot_land.where.indexOf('12193') > -1 && D.src.reshumot_pledge.where.indexOf('12123') > -1, 'Reshumot: land notice 12193, pledge notice 12123');
var L = D.land, P = D.pledge;
ok([L.mortgage.amount, L.change.amount, L.redeem_direct.amount, L.redeem_deposit.amount, L.note.amount, L.note_delete.amount, L.nesach_counter.amount, L.nesach_online.amount, L.inherit.amount].join() === '188,188,0,188,188,127,88,18,188',
  'land fees 2026 = gov.md: 188, 188, 0, 188, 188, 127, 88, 18, 188');
ok([P.reg_counter.amount, P.reg_online.amount, P.paid_years_max, P.free_from_year, P.cancel.amount, P.change_counter.amount, P.change_online.amount, P.search_counter.amount, P.search_online.amount].join() === '45,38,5,6,0,45,38,38,12',
  'pledge fees 2026 = gov.md: 45 / 38 a year, 5 paid years, free from year 6, cancel 0, change 45 / 38, search 38 / 12');
ok(D.src.kz_disabled.updated === '2025-03-02' && D.src.kz_terror.updated === '2025-11-10' && D.src.kz_bereaved_idf.updated === '2026-03-16' && D.src.kz_bereaved_terror.updated === '2025-03-02' && D.src.kz_idf_disabled.updated === '2025-03-02',
  'Kol Zchut page dates as read: 2.3.2025, 10.11.2025, 16.3.2026, 2.3.2025, 2.3.2025');
var C = D.contact;
ok(C.phone === '*8653' && C.abroad === '972-8-6831663' && C.ext === 'שלוחה 7 ואז 1' && C.days === 'ראשון עד חמישי' && C.hours === '8:00 עד 16:00' && C.whatsapp === '073-3929983',
  'contact line as read by hand on gov.il: *8653, 7 then 1, Sunday to Thursday 8:00 to 16:00, WhatsApp 073-3929983');
ok(C.deed_days === 'ראשון ורביעי' && C.deed_hours === '8:30 עד 12:30', 'deed authentication by appointment: Sunday and Wednesday 8:30 to 12:30');
ok(D.rules.s9a.days === 30 && D.rules.s9h2.months === 12 && D.rules.deposit.notice_days_min === 15, 'rules: s.9A 30 days, s.9ח2 12 months, reg. 72 at least 15 days');
var I = D.ila;
ok(D.src.ila_guide.read === '2026-11-06' && D.src.ila_guide.url === 'https://www.gov.il/he/service/guide-mortgage' && /בדפדפן של הבעלים/.test(D.src.ila_guide.how), 'ILA service page: read by hand in the owner\'s browser on 6.11.2026');
ok(D.src.ila_form.url === 'https://www.gov.il/BlobFolder/policy/9002b-procedure/he/forms_wform351.pdf' && D.src.ila_form.title === 'טופס בקשה למתן כתב התחייבות לרישום משכנתא והוראה בלתי חוזרת' && !D.src.ila_form.read, 'ILA form: the official PDF, link only');
ok(I.contact.phone === '*5575' && I.contact.phone2 === '03-9533333' && I.contact.days === 'ראשון עד חמישי' && I.contact.hours === '8:00 עד 17:00', 'ILA call centre as read: *5575, 03-9533333, Sunday to Thursday 8:00 to 17:00');
ok(I.area === 'רמ״י שלי' && I.id === 'מערכת ההזדהות הלאומית' && I.procedure.indexOf('90.02B') > -1 && I.fee === 'האגרה של רמ״י לא מופיעה בדף השירות', 'ILA facts: personal area, national identification, procedure 90.02B, no fee stated on the page');
var badSrc = [];
D.exemptions.forEach(function (x) { x.conditions.concat(x.how).forEach(function (c) { if (!D.src[c.src]) badSrc.push(x.k + ':' + c.src); }); });
Object.keys(D.docs).forEach(function (k) { if (!D.src[D.docs[k].src]) badSrc.push('doc:' + k); });
Object.keys(D.rules).forEach(function (k) { if (!D.src[D.rules[k].src]) badSrc.push('rule:' + k); });
ok(!badSrc.length, 'every condition, document and rule names a src that exists', badSrc.join() || 'all');
ok(D.exemptions.map(function (x) { return x.k + x.reg; }).join() === 'disabled12,bereaved_idf12,bereaved_terror12,terror12,olim13', 'five exemption groups: regulation 12 (four) and 13 (olim)');

console.log('\n1. every path, the total "לשלם למדינה" (by hand)');
var CASES = [
  // [overrides, expected total, expected status, what]
  [{}, 206, 'ok', 'tabu, registration, lawyer online, the default online extract: 188 + 18'],
  [{ nesach: 'none' }, 188, 'ok', 'tabu, registration, no extract: 188'],
  [{ who: 'office' }, 206, 'ok', 'tabu, registration, by hand: 188 + 18 (who files does not change the fee)'],
  [{ who: 'office', nesach: 'counter' }, 276, 'ok', 'tabu, registration, counter extract: 188 + 88'],
  [{ act: 'second', nesach: 'none' }, 188, 'ok', 'tabu, additional or second-degree mortgage: 188'],
  [{ act: 'second', who: 'office' }, 206, 'ok', 'tabu, second degree, by hand: 188 + 18'],
  [{ act: 'amend', amend: 'terms', nesach: 'none' }, 188, 'ok', 'tabu, amendment of terms: 188 (item 2(ב))'],
  [{ act: 'amend', amend: 'inc', who: 'office', nesach: 'none' }, 188, 'ok', 'tabu, increase of the loan: 188 (item 2(א))'],
  [{ act: 'cancel' }, 0, 'bank', 'tabu, cancellation after payoff, the bank files: 0'],
  [{ act: 'cancel', nesach: 'online' }, 18, 'bank', 'tabu, cancellation with an online extract to check: 0 + 18'],
  [{ act: 'cancel', who: 'office' }, 188, 'ok', 'tabu, cancellation by deposit at the office (reg. 72): 188'],
  [{ act: 'death' }, 0, 'bank', 'tabu, cancellation after death, insurance repaid: 0 (inheritance 188 apart)'],
  [{ reg: 'ila' }, 0, 'ila', 'ILA, registration: the ILA fee is not stated on the service page; the warning note (if any) is apart'],
  [{ reg: 'ila', who: 'rep' }, 0, 'ila', 'ILA, registration by a representative: the same'],
  [{ reg: 'ila', nesach: 'online' }, 18, 'ila', 'ILA, registration with an online extract: 18'],
  [{ reg: 'ila', act: 'second', who: 'rep', nesach: 'counter' }, 88, 'ila', 'ILA, second mortgage, counter extract: 88'],
  [{ reg: 'ila', act: 'amend' }, 0, 'unknown', 'ILA, amendment: no verified fee'],
  [{ reg: 'ila', act: 'cancel' }, 0, 'bank', 'ILA, cancellation: the bank cancels; 127 note deletion apart'],
  [{ reg: 'ila', act: 'death' }, 0, 'bank', 'ILA, after death: 0'],
  [{ reg: 'company' }, 188, 'ok', 'housing company, registration: warning note 188'],
  [{ reg: 'company', act: 'amend' }, 0, 'unknown', 'housing company, amendment: no verified fee'],
  [{ reg: 'company', act: 'cancel' }, 0, 'bank', 'housing company, cancellation: 0'],
  [{ reg: 'none' }, 190, 'ok', 'not registered, pledge 25 years online: 5 x 38'],
  [{ reg: 'none', who: 'office' }, 225, 'ok', 'not registered, pledge 25 years at the counter: 5 x 45'],
  [{ reg: 'none', years: 5 }, 190, 'ok', 'pledge, 5 years online: 190'],
  [{ reg: 'none', years: 5, who: 'office' }, 225, 'ok', 'pledge, 5 years at the counter: 225'],
  [{ reg: 'none', years: 3 }, 114, 'ok', 'pledge, 3 years online: 3 x 38'],
  [{ reg: 'none', years: 3, who: 'office' }, 135, 'ok', 'pledge, 3 years at the counter: 3 x 45'],
  [{ reg: 'none', years: 1, who: 'office' }, 45, 'ok', 'pledge, 1 year at the counter: 45'],
  [{ reg: 'none', years: 6, who: 'office' }, 225, 'ok', 'pledge, 6 years at the counter: the 6th is free, 225'],
  [{ reg: 'none', years: '30' }, 190, 'ok', 'pledge, 30 years typed as text: 190'],
  [{ reg: 'none', act: 'second' }, 190, 'ok', 'not registered, an additional pledge: 190'],
  [{ reg: 'none', nesach: 'online' }, 202, 'ok', 'pledge online + internet search of the register: 190 + 12'],
  [{ reg: 'none', who: 'office', nesach: 'counter' }, 263, 'ok', 'pledge at the counter + counter search: 225 + 38'],
  [{ reg: 'none', act: 'amend' }, 38, 'ok', 'pledge, change of details online: 38'],
  [{ reg: 'none', act: 'amend', who: 'office' }, 45, 'ok', 'pledge, change of details at the counter: 45'],
  [{ reg: 'none', act: 'cancel' }, 0, 'bank', 'pledge cancellation: free'],
  [{ reg: 'none', act: 'death' }, 0, 'bank', 'pledge after death: free']
];
CASES.forEach(function (c) { var r = run(c[0]); ok(!r.error && r.total === c[1] && r.status === c[2], c[3] + ' = ' + c[1], r.error ? r.error.msg : r.total + ' ' + r.status); });

console.log('\n2. the exemptions (regulations 12 and 13)');
D.exemptions.forEach(function (x) {
  var r = run({ ex: x.k, nesach: 'none' }), m = line(r, 'mortgage');
  ok(r.total === 0 && m.amt === 0 && m.kind === 'ex' && r.ex.applies && r.ex.saved === 188 && m.note.indexOf('תקנה ' + x.reg) > -1, 'tabu registration, ' + x.k + ': 188 becomes 0 with the reason (תקנה ' + x.reg + ')', r.total);
});
var rx = run({ ex: 'disabled' });
ok(rx.total === 18, 'exempt registration with the default online extract: 0 + 18 = 18', rx.total);
rx = run({ act: 'second', ex: 'terror', nesach: 'none' });
ok(rx.total === 0 && rx.ex.applies, 'second-degree mortgage, terror victim: 0', rx.total);
rx = run({ act: 'amend', ex: 'disabled', nesach: 'none' });
ok(rx.total === 188 && !rx.ex.applies && rx.ex.why.indexOf('לא מצאנו כתוב') > -1, 'amendment + exemption: not applied (the regulation says "בעד רישום משכנתה"), 188 stays', rx.total);
ok(K.unverified(rx, D).some(function (u) { return u.k === 'exempt_scope'; }), 'amendment + exemption: the "exempt_scope" caveat is listed');
rx = run({ reg: 'company', ex: 'bereaved_idf' });
ok(rx.total === 188 && !rx.ex.applies && /הערת אזהרה/.test(rx.ex.why) && /יחול כשהמשכנתה תירשם בטאבו/.test(rx.ex.why) && /הפטור שבחרתם יחול על הרישום הזה/.test(line(rx, 'later').note),'housing company + bereaved: the warning note stays 188; the exemption is said to apply to the later tabu registration', rx.total);
rx = run({ reg: 'ila', ex: 'bereaved_idf' });
ok(rx.total === 0 && rx.status === 'ila' && !rx.ex.applies && /כתב ההתחייבות של רמ״י/.test(rx.ex.why) && /הפטור שבחרתם יחול על הרישום הזה/.test(line(rx, 'later').note), 'ILA + bereaved: not on the ILA commitment; said to apply to the later tabu registration');
rx = run({ reg: 'none', who: 'office', ex: 'olim' });
ok(rx.total === 225 && !rx.ex.applies && /הודעת המשכון/.test(rx.ex.why), 'pledge + oleh: not applied to the Registrar of Pledges, 225 stays', rx.total);
ok(K.unverified(rx, D).some(function (u) { return u.k === 'olim'; }), 'oleh picked: the regulation 13 caveat is listed');
ok(run({ act: 'cancel', ex: 'disabled' }).ex === null, 'cancellation: no exemption block (nothing to exempt)');
ok(K.docs(run({ ex: 'bereaved_idf' }), D).items.some(function (d) { return d.k === 'exempt'; }) && !K.docs(run({ ex: 'bereaved_idf' }), D).items.some(function (d) { return d.k === 'fee'; }),
  'exempt path: the checklist asks for the exemption approval instead of the fee receipt');

console.log('\n3. cancellation, the bank and the deadline');
var rc = run({ act: 'cancel' }), red = line(rc, 'redeem');
ok(red.amt === 0 && red.kind === 'free' && red.item === '2(ג)(1)' && red.tot, 'cancellation paid straight to the lender: 0, item 2(ג)(1), counted in the total');
var tl = K.timeList(rc, D).map(function (x) { return x.he; }).join(' ');
ok(tl.indexOf('תוך 30 ימים מיום הפירעון') > -1 && tl.indexOf('והוצאות המחיקה עליו') > -1 && tl.indexOf('מועד אחד לכל תאגיד בנקאי') > -1, 'time: the bank files within 30 days of payoff, at its cost, one deadline for every bank');
ok(K.whereText(rc, D).he.indexOf('לפי בקשת הבנק לבדו') > -1, 'where: regulation 71(ב)(2), the registrar may cancel at the bank\'s request alone');
var rd = run({ act: 'death' });
ok(line(rd, 'inherit').amt === 188 && !line(rd, 'inherit').tot && rd.total === 0, 'after death: inheritance registration 188 shown apart, not in the total');
ok(K.timeList(rd, D).some(function (x) { return x.he.indexOf('עד 12 חודשים מהפטירה') > -1; }) && K.timeList(rd, D).some(function (x) { return x.he.indexOf('בעצמו ולא באמצעות ערב') > -1; }), 'after death: s.9ח2 deferral up to 12 months, and the s.9A "בעצמו ולא באמצעות ערב" caveat');
var ro = run({ act: 'cancel', who: 'office' });
ok(line(ro, 'redeem').item === '2(ג)(2)' && K.steps(ro, D).some(function (s) { return s.he.indexOf('15 ימים לפחות') > -1; }), 'deposit at the office: item 2(ג)(2), the registrar gives the bank at least 15 days');
var ri = run({ reg: 'ila', act: 'cancel' });
ok(line(ri, 'note_delete').amt === 127 && !line(ri, 'note_delete').tot && K.headline(ri, D).value === 'הבנק מבטל את השעבוד', 'ILA cancellation: warning-note deletion 127 shown apart; the headline says the bank cancels');

console.log('\n4. the Registrar of Pledges, five-year totals');
ok(run({ reg: 'none', years: 5, who: 'office' }).total === 225 && run({ reg: 'none', years: 5, who: 'lawyer' }).total === 190, 'five years: 225 at the counter, 190 online');
var rp = run({ reg: 'none', years: 25 });
ok(line(rp, 'pledge').note.indexOf('5 × 38 ₪ לשנה') > -1 && line(rp, 'pledge').note.indexOf('מהשנה השישית אין אגרה') > -1, 'the pledge line explains 5 x 38 and the free sixth year', line(rp, 'pledge').note);
ok(line(rp, 'later').amt === 188 && !line(rp, 'later').tot, 'later tabu registration 188 shown, not in the total');

console.log('\n5. who files, the hash, bad values');
ok(K.whoOpts('ila', 'register').join() === 'owner,rep' && K.whoOpts('ila', 'amend').join() === 'owner,rep' && K.whoOpts('company', 'register').join() === 'lawyer,office' && K.whoOpts('tabu', 'register').join() === 'lawyer,office' && K.whoOpts('tabu', 'cancel').join() === 'bank,office' && K.whoOpts('ila', 'cancel').join() === 'bank' && K.whoOpts('tabu', 'death').join() === 'bank', 'step 3 options follow the path');
ok(run({ reg: 'ila', who: 'lawyer' }).who === 'owner' && run({ reg: 'tabu', who: 'rep' }).who === 'lawyer' && run({ act: 'cancel', who: 'lawyer' }).who === 'bank' && run({ reg: 'ila', act: 'cancel', who: 'office' }).who === 'bank' && run({ act: 'death', who: 'office' }).who === 'bank', 'a who that does not fit the path falls back to the first option');
var hv = { reg: 'none', act: 'second', who: 'office', nesach: 'counter', ex: 'olim', years: 3, amend: 'inc' };
ok(K.enc({ reg: 'ila', act: 'register', who: 'rep', nesach: 'auto', ex: 'none', years: 25, amend: 'terms' }) === 'ila.register.rep.auto.none.25.terms' && K.dec('ila.register.rep.auto.none.25.terms').who === 'rep' && K.enc(hv) === 'none.second.office.counter.olim.3.inc' && JSON.stringify(K.dec(K.enc(hv))) === JSON.stringify(hv), 'hash round trip: none.second.office.counter.olim.3.inc');
ok(JSON.stringify(K.dec('x.y.z.q.w.999.v')) === JSON.stringify(K.defaults()) && K.dec('tabu.register') === null, 'a broken hash falls back to the defaults, a short one is ignored');
ok(/^[a-z0-9_.]+$/.test(K.enc(K.defaults())) && !/[@\d]{6,}/.test(K.enc(hv)), 'the hash holds choices only, no personal data', K.enc(K.defaults()));
ok(run({ reg: 'none', years: 0 }).error.field === 'years' && run({ reg: 'none', years: 41 }).error.field === 'years' && run({ reg: 'none', years: 'x' }).error.field === 'years', 'years 0, 41 or "x": an error on the years field');
ok(run({ reg: 'mars' }).error.field === 'reg' && run({ act: 'sell' }).error.field === 'act' && K.compute(K.defaults(), {}).error, 'an unknown registry, action, or missing data: an error, no figure');

console.log('\n6. the words');
var ALL = [], paths = 0, foreign = [], badSum = [];
var amounts = {}; (function walk(o) { if (o && typeof o === 'object') Object.keys(o).forEach(function (k) { if (k === 'amount') amounts[o[k]] = 1; else walk(o[k]); }); })(D);
[114, 135, 190, 225].forEach(function (x) { amounts[x] = 1; });  // pledge products worked out by hand in section 1 (3 or 5 paid years x 38 / 45)
K.REGS.forEach(function (reg) { K.ACTS.forEach(function (a) { K.whoOpts(reg, a.k).forEach(function (who) { ['auto', 'online', 'counter', 'none'].forEach(function (nes) { ['none', 'disabled', 'olim'].forEach(function (ex) {
  var r = run({ reg: reg, act: a.k, who: who, nesach: nes, ex: ex }); if (r.error) { ALL.push('ERROR ' + r.error.msg); return; } paths++;
  var t = texts(r); ALL.push(t);
  // each line amount is a 2026 amount or a pledge product; the total is their sum; any other shekel figure in the words is one of those
  var parts = r.lines.filter(function (l) { return l.amt != null; }).map(function (l) { return l.amt; });
  parts.forEach(function (x) { if (!amounts[x]) foreign.push(reg + '.' + a.k + ':' + x); });
  var s = 0; r.lines.forEach(function (l) { if (l.tot && l.amt > 0) s += l.amt; }); if (s !== r.total) badSum.push(reg + '.' + a.k);
  (t.match(/[\d,]+ ₪/g) || []).map(function (x) { return +x.replace(/[^\d]/g, ''); }).forEach(function (x) { if (!amounts[x] && x !== r.total) foreign.push(reg + '.' + a.k + '.' + who + '.' + nes + ': ' + x); });
}); }); }); }); });
var TXT = ALL.join('\n');
ok(TXT.indexOf('ERROR') < 0, 'every combination computes', paths + ' combinations');
ok(!LONG.test(TXT), 'no long dash in any text');
ok(!BANNED.test(TXT), 'no banned word in any text', (TXT.match(BANNED) || [''])[0]);
ok(!SIXTY.test(TXT), 'no "sixty days" anywhere in the texts');
ok(!badSum.length, 'in every combination the total is the sum of its counted lines', badSum.slice(0, 3).join() || paths + ' combinations');
ok(!foreign.length, 'every shekel figure in every combination is a 2026 amount of rishum.json, a pledge product, or that path\'s total', foreign.slice(0, 4).join(' | ') || 'all');
var OFFICIAL = [D.ila.doc, D.ila.procedure, D.src.ila_form.title];  // official titles keep their own spelling
function official(t) { OFFICIAL.forEach(function (o) { t = t.split(o).join(''); }); return t; }
var legal = []; K.REGS.forEach(function (reg) { K.ACTS.forEach(function (a) { K.steps(run({ reg: reg, act: a.k }), D).forEach(function (s) { if (/\u05de\u05e9\u05db\u05e0\u05ea\u05d0/.test(official(s.he))) legal.push(s.he); }); }); });
ok(!legal.length, 'the legal steps say "משכנתה", never the everyday spelling', legal[0] || 'all');
ok(K.checklistText(run({}), D).indexOf('טופס רישום משכנתא') === 0 && K.checklistText(run({}), D).indexOf(D.src.gov_forms.url) > -1, 'the checklist is titled "טופס רישום משכנתא" and links the official forms page (no form recreated)');
var dc = K.docs(run({}), D).items.map(function (d) { return d.k; }).join();
ok(dc === 'request,deed,fee,id,capacity,corp,consent,nesach', 'tabu registration checklist: request, deed, fee receipt, ID, capacity, bank documents, consent, extract', dc);
ok(K.docs(run({ act: 'second' }), D).items.some(function (d) { return d.k === 'consent_first'; }), 'second degree: the first bank\'s consent (s.7ח) is on the list');
ok(K.docs(run({ act: 'cancel', who: 'office' }), D).items.map(function (d) { return d.k; }).join() === 'r72_deed,r72_refusal,r72_sum,id', 'deposit: the regulation 72 documents');
ok(K.docs(run({ reg: 'company' }), D).items.map(function (d) { return d.k; }).join() === 'commit,note_req,note_commit,note_owner,note_id', 'housing company: the commitment (unverified) and the regulation 21 warning-note documents (unchanged)');
ok(K.docs(run({ reg: 'ila' }), D).items.map(function (d) { return d.k; }).join() === 'ila_referral,ila_sign,ila_form', 'ILA, the rights holder files: referral letter from the lender, every rights holder signs in the personal area, the official form (link)');
ok(K.docs(run({ reg: 'ila', who: 'rep' }), D).items.map(function (d) { return d.k; }).join() === 'ila_referral,ila_poa,ila_sign,ila_form', 'ILA, a representative files: the power of attorney is added');
ok(K.docs(run({ reg: 'ila', act: 'second' }), D).items.some(function (d) { return d.k === 'consent_first'; }), 'ILA, second mortgage: the first bank\'s consent (s.7ח) is on the list');
ok(!D.unverified.some(function (u) { return u.k === 'ila'; }) && !K.unverified(run({ reg: 'ila' }), D).some(function (u) { return u.k === 'ila_more'; }) && K.unverified(run({ reg: 'ila', act: 'cancel' }), D).some(function (u) { return u.k === 'ila_more'; }) && !K.unverified(run({}), D).some(function (u) { return /^ila/.test(u.k); }),
  'the old ILA caveat is gone; "ila_more" (amendment and cancellation not on the page) shows on ILA cancellation only, nothing ILA on tabu');
var ILA = []; K.ACTS.forEach(function (a) { K.whoOpts('ila', a.k).forEach(function (who) { ILA.push(texts(run({ reg: 'ila', act: a.k, who: who }))); }); });
var ILAT = ILA.join(String.fromCharCode(10));
ok(ILAT.indexOf('לא נקרא') < 0 && ILAT.indexOf('לא ידוע') < 0 && ILAT.indexOf('קטע מתוצאת חיפוש') < 0, 'ILA path: no "לא נקרא", no "לא ידוע", no search-snippet wording left');
ok(['*5575', '03-9533333', '8:00 עד 17:00', 'רמ״י שלי', 'מערכת ההזדהות הלאומית', '90.02B', 'עותק מודפס לא נחשב נסח רשמי', 'מכתב הפנייה', 'לא מופיעה בדף השירות', 'אלא אם באותו מעמד תירשם גם המשכנתה'].every(function (x) { return ILAT.indexOf(x) > -1; }),
  'ILA path carries the facts read: call centre, personal area, national identification, procedure, the digital original, the referral letter, no fee stated, the undertaking');
var rI = run({ reg: 'ila' });
ok(K.headline(rI, D).value === 'לא מופיעה בדף השירות' && line(rI, 'commit').shown === 'לא מופיעה בדף השירות' && !line(rI, 'note').tot && !K.showTotal(rI) && K.showTotal(run({ reg: 'ila', nesach: 'online' })), 'ILA headline: "לא מופיעה בדף השירות"; the warning note is outside the total; no total row unless an extract is picked');
ok(K.whereText(rI, D).ok && K.whereText(rI, D).he.indexOf('שאינם רשומים בטאבו או בחברה משכנת או קבלנית') > -1, 'ILA where: verified, for ILA-managed homes not registered in tabu or a housing or contractor company');
ok(K.checklistText(rI, D).indexOf(D.src.ila_form.url) > -1 && K.checklistText(rI, D).indexOf(D.src.ila_guide.url) > -1, 'ILA checklist copy carries the ILA form and service links');
ok(K.headline(run({ reg: 'company', act: 'amend' }), D).value === 'בודקים מול החברה המשכנת' && K.headline(run({ reg: 'ila', act: 'amend' }), D).value === 'בודקים מול רמ״י', 'unknown paths say "בודקים מול" instead of a number');
ok(K.copyText(run({}), D, 'L').indexOf('23.12.2025') > -1 && K.copyText(run({}), D, 'L').indexOf('24.12.2025') > -1 && K.copyText(run({}), D, 'L').indexOf('נבדק ב־6.11.2026') > -1, 'the copied summary carries the 2026 notice dates and the check date');

console.log('\n7. the files');
var FILES = [path.join(INS, 'tools/mrishum.js'), path.join(INS, 'data/rishum.json')].concat(fs.readdirSync(HERE).filter(function (f) { return /\.(js|py|html|txt|md|json)$/.test(f) && !/\.out\.txt$|verify\.json$/.test(f); }).map(function (f) { return path.join(HERE, f); }));
var bad60 = FILES.filter(function (f) { return SIXTY.test(fs.readFileSync(f, 'utf8')); });
ok(!bad60.length, 'no "sixty days" in any file of the build', bad60.map(function (f) { return path.basename(f); }).join() || FILES.length + ' files');
var badLong = FILES.filter(function (f) { return LONG.test(fs.readFileSync(f, 'utf8')); });
ok(!badLong.length, 'no long dash in any file of the build', badLong.map(function (f) { return path.basename(f); }).join() || 'none');
var JS = fs.readFileSync(path.join(INS, 'tools/mrishum.js'), 'utf8');
var logic = JS.split('the page */')[0].replace(/\/\*[\s\S]*?\*\//g, '').replace(/\/\/.*$/gm, '');
var lit = logic.match(/[^\w.#\-]\b(188|127|88|45|38|18|225|190|30|15|60)\b/g);
ok(!lit, 'the logic of mrishum.js holds no amount or deadline of its own', lit ? lit.join() : 'none');
ok(!/\bfetch\(|sendBeacon|XMLHttpRequest|<form/.test(JS), 'mrishum.js sends nothing: no fetch, sendBeacon, XMLHttpRequest or form');
ok(!BANNED.test(JS) && !BANNED.test(fs.readFileSync(path.join(INS, 'data/rishum.json'), 'utf8')), 'no banned word in mrishum.js or rishum.json');

console.log('\n' + (n - fails) + ' of ' + n + ' passed' + (fails ? ', ' + fails + ' FAILED' : ''));
process.exit(fails ? 1 : 0);
