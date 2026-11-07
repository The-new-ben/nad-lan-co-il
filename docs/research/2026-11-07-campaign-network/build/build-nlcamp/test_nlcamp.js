/* nlcamp build (7.11.2026) · node test of the pure part of plugins/nadlan-config/assets/instruments/tools/nlcamp.js (window.NLCAMP):
   the plan recommendation, totals, the split, validation, the payload, the shared text, the payment link, i18n completeness and
   the copy rules, plus a cross-check against the server side (inc/campaign-brief.php through test_campaign_brief.php --json).
   Run from anywhere:  node docs/research/2026-11-07-campaign-network/build/build-nlcamp/test_nlcamp.js
   Exit code 1 on any failure. */
'use strict';
var path = require('path'), fs = require('fs'), cp = require('child_process');
var HERE = __dirname, REPO = path.resolve(HERE, '../../../../..');
var FILE = path.join(REPO, 'plugins/nadlan-config/assets/instruments/tools/nlcamp.js');
global.window = {};
require(FILE);
var N = window.NLCAMP, SRC = fs.readFileSync(FILE, 'utf8');
var DASH = new RegExp('[' + String.fromCharCode(0x2013, 0x2014) + ']');
var fails = 0, n = 0;
function ok(cond, name, got) { n++; if (!cond) fails++; console.log((cond ? '  ok   ' : '  FAIL ') + name + (got !== undefined ? '  [' + (typeof got === 'string' ? got : JSON.stringify(got)) + ']' : '')); }
function same(a, b) { return JSON.stringify(a) === JSON.stringify(b); }
function full(ch) {  // a complete state: two markets, everything filled
  var s = N.newState(); ['fr', 'ca'].forEach(function (m) { N.toggleMarket(s, m); });
  Object.assign(s, { buyer: 'invest', budget: 25000, kind: 'existing', ref: '  מגדלי הים, בת ים ', plan: 'three', name: 'דנה לוי', company: 'לוי יזמות', phone: '050-123 4567', email: 'dana@example.test', consent: true }, ch || {});
  return s;
}

console.log('1. the offer');
ok(N.benchmarks === null, 'NLCAMP.benchmarks is the named hook and stays null (no reach, lead or cost-per-lead figure)');
ok(N.plans.one.price === 36000 && N.plans.three.price === 72000 && N.plans.flag.price === 144000, 'the approved annual plans: 36,000 / 72,000 / 144,000');
ok(N.PLAN_ORDER.every(function (k) { return N.plans[k].productUrl === null && N.plans[k].firstPay === null; }), 'in the file every productUrl and firstPay is null (the server config sets them)');
ok(same(N.MARKETS.map(function (m) { return m.id + ':' + m.langs.join('+'); }), ['fr:fr', 'us:en', 'uk:en', 'ca:en+fr', 'be:fr', 'ch:fr', 'za:en', 'au:en', 'ru:ru', 'olim:en+fr+ru']), 'ten markets with the languages of the brief', N.MARKETS.length);
ok(same(N.BUDGET, { min: 3000, max: 60000, step: 1000, start: 10000 }), 'budget 3,000 to 60,000, step 1,000, opens at 10,000');
ok(same(N.SPLIT.map(function (c) { return c.k + c.pct; }), ['meta55', 'google25', 'press15', 'boards5']) && N.splitSum(N.SPLIT.map(function (c) { return c.pct; })) === 100, 'the suggested split: Meta 55, Google 25, press 15, portals 5');

console.log('\n2. the plan follows the number of markets');
var rec = []; for (var k = 0; k <= 10; k++) rec.push(N.recommend(k));
ok(same(rec, [null, 'one', 'three', 'three', 'flag', 'flag', 'flag', 'flag', 'flag', 'flag', 'flag']), '0 none, 1 one market, 2-3 three markets, 4+ flagship', rec);
ok(N.covers('one', 1) && !N.covers('one', 2) && N.covers('three', 3) && !N.covers('three', 4) && N.covers('flag', 10) && !N.covers('gold', 1), 'covers: one carries 1, three carries 3, flagship any');
var s = N.newState(); N.toggleMarket(s, 'olim'); N.toggleMarket(s, 'fr'); N.toggleMarket(s, 'zz'); N.toggleMarket(s, 'ca');
ok(same(s.markets, ['fr', 'ca', 'olim']), 'chips keep the list order; an unknown id is ignored', s.markets);
N.toggleMarket(s, 'olim'); ok(same(s.markets, ['fr', 'ca']), 'a second press removes the market');
ok(same(N.langsOf(['fr']), ['fr']) && same(N.langsOf(['fr', 'ca']), ['en', 'fr']) && same(N.langsOf(['ru', 'us']), ['en', 'ru']) && same(N.langsOf(['olim']), ['en', 'fr', 'ru']) && same(N.langsOf([]), []), 'languages implied: France fr; France + Canada en, fr; olim en, fr, ru');

console.log('\n3. budget and totals');
ok(N.budgetOk(3000) && N.budgetOk(60000) && N.budgetOk(25000) && !N.budgetOk(2000) && !N.budgetOk(61000) && !N.budgetOk(25500) && !N.budgetOk(NaN) && !N.budgetOk('25000'), 'in range and on the step only');
ok(N.clampBudget(2500) === 3000 && N.clampBudget(99999) === 60000 && N.clampBudget(12400) === 12000 && N.clampBudget(NaN) === 10000, 'clamp: 2,500 -> 3,000; 99,999 -> 60,000; 12,400 -> 12,000; empty -> 10,000');
s = N.newState(); s.budget = 3000; N.stepBudget(s, -1); var lo = s.budget; s.budget = 60000; N.stepBudget(s, 1); var hi = s.budget; s.budget = 10000; N.stepBudget(s, 1); N.stepBudget(s, 1); N.stepBudget(s, -1);
ok(lo === 3000 && hi === 60000 && s.budget === 11000, 'the -/+ buttons stop at 3,000 and 60,000; 10,000 +2 -1 = 11,000', [lo, hi, s.budget]);
s.budget = 2500; N.stepBudget(s, 1); ok(s.budget === 3000, 'a typed value off the range: the first press only brings it into range', s.budget);
ok(N.yearly(10000) === 120000 && N.yearly(60000) === 720000 && N.yearly(3000) === 36000, 'yearly total = 12 months: 120,000 / 720,000 / 36,000');

console.log('\n4. the split');
var bad = 0, tried = 0;
[[55, 25, 15, 5], [50, 25, 20, 5], [100, 0, 0, 0], [35, 35, 15, 15], [5, 5, 5, 85]].forEach(function (sh) {
  for (var b = 3000; b <= 60000; b += 1000) { tried++; var A = N.splitAmounts(b, sh); var sum = A.reduce(function (x, a) { return x + a.amount; }, 0); if (sum !== b || A.some(function (a) { return a.amount !== Math.round(a.amount) || a.amount < 0; })) bad++; }
});
ok(bad === 0, 'whole shekels that add up to the budget exactly, ' + tried + ' cases (5 splits x every budget step)', bad);
ok(same(N.splitAmounts(25000, [55, 25, 15, 5]).map(function (a) { return a.amount; }), [13750, 6250, 3750, 1250]), '25,000 by the suggested split: 13,750 / 6,250 / 3,750 / 1,250');
ok(same(N.splitAmounts(3000, [55, 25, 15, 5]).map(function (a) { return a.amount; }), [1650, 750, 450, 150]), '3,000: 1,650 / 750 / 450 / 150');
s = N.newState(); N.stepShare(s, 0, -1); N.stepShare(s, 2, 1); ok(same(s.shares, [50, 25, 20, 5]) && N.splitSum(s.shares) === 100, 'Meta -5, press +5: 50 / 25 / 20 / 5, still 100');
s.shares = [0, 25, 15, 5]; N.stepShare(s, 0, -1); s.shares[1] = 100; N.stepShare(s, 1, 1); ok(s.shares[0] === 0 && s.shares[1] === 100, 'a share stays between 0 and 100');

console.log('\n5. validation, step by step');
s = N.newState();
ok(same(N.validate(s, 1), [{ f: 'markets' }]) && same(N.validate(s, 2), [{ f: 'buyer' }]) && same(N.validate(s, 4), [{ f: 'kind' }]), 'empty: step 1 markets, step 2 buyer, step 4 kind');
ok(N.validate(s, 3).length === 0, 'step 3 opens valid (10,000, the suggested split)');
s.budget = 2500; s.shares = [55, 25, 20, 5]; ok(same(N.validate(s, 3), [{ f: 'budget' }, { f: 'split', sum: 105 }]), 'step 3: budget off range and a split of 105', N.validate(s, 3));
s = N.newState(); s.kind = 'existing'; s.ref = ' x '; ok(same(N.validate(s, 4), [{ f: 'ref' }]), 'an existing page needs its address or name (2 letters at least)');
s.kind = 'new'; s.ref = ''; ok(N.validate(s, 4).length === 0, 'a new project needs no name');
s = full(); ok(N.validateAll(s).length === 0, 'a full state passes all five steps', N.validateAll(s));
ok(same(N.validate(full({ plan: 'one' }), 5), [{ f: 'plan', code: 'cover' }]), 'one market chosen for two markets: the plan error "cover"');
ok(same(N.validate(full({ plan: null }), 5), [{ f: 'plan' }]) && N.validate(full({ plan: 'flag' }), 5).length === 0, 'no plan: error; a bigger plan than needed: fine');
var e5 = N.validate(full({ name: ' ', company: 'x', phone: '12345', email: 'a@b', consent: 'yes' }), 5).map(function (x) { return x.f; });
ok(same(e5, ['name', 'company', 'phone', 'email', 'consent']), 'contact errors in screen order; consent must be true itself', e5);
ok(N.phoneOk('050-1234567') && N.phoneOk('03 123 4567') && N.phoneOk('+33 6 12 34 56 78') && N.phoneOk('(212) 555-0199 1') && !N.phoneOk('1234') && !N.phoneOk('050-123-4567 ext 9') && !N.phoneOk(''), 'phones: Israeli mobile and landline, French, US; short or with words refused');
ok(N.emailOk('dana@example.test') && N.emailOk(' a.b+c@d.co.il ') && !N.emailOk('dana@') && !N.emailOk('dana example.test') && !N.emailOk('a@b.c'), 'emails');
var va = N.validateAll(N.newState()); ok(va[0].step === 1 && va[0].f === 'markets', 'validateAll names the step of the first error');

console.log('\n6. the brief sent to the server');
var P = N.payload(full(), 'he', 41234.6, '/international-campaigns/', '');
ok(same(Object.keys(P).sort(), ['budget', 'buyer', 'company', 'consent', 'consent_text', 'email', 'hp', 'kind', 'lang', 'markets', 'name', 'page', 'phone', 'plan', 'project', 'shares', 't', 'v'].sort()), 'the keys inc/campaign-brief.php reads, nothing else', Object.keys(P).length);
ok(!/card|cvv|iban|account|passw/i.test(JSON.stringify(Object.keys(P))), 'no card or bank field');
ok(P.consent === true && P.project === 'מגדלי הים, בת ים' && P.t === 41235 && P.lang === 'he' && P.consent_text === N.STR.he.consent && same(P.markets, ['fr', 'ca']) && P.budget === 25000, 'consent true, project trimmed, time in whole ms, the consent wording sent with it');
var p2 = N.payload(full(), 'en', 1, '/x/', 'bot'); ok(p2.lang === 'en' && p2.hp === 'bot' && p2.consent_text === N.STR.en.consent, 'English brief, the honeypot passed through as typed');
var st2 = full(); var p3 = N.payload(st2, 'he', 1, '/', ''); p3.markets.push('us'); p3.shares[0] = 0; ok(same(st2.markets, ['fr', 'ca']) && st2.shares[0] === 55, 'the payload is a copy (the state is not changed by it)');

console.log('\n7. the shared text (copy and WhatsApp)');
var tx = N.summaryText(full(), 'he', null, 'https://nad-lan.co.il/international-campaigns/');
ok(tx.split('\n')[0] === 'תוכנית קמפיין בינלאומי בנדלן' && tx.indexOf('שווקים וקהילות: צרפת, קנדה') > -1 && tx.indexOf('שפות: אנגלית, צרפתית') > -1 && tx.indexOf('הקונים: משקיעים, להשכרה') > -1, 'Hebrew: markets, languages, buyers');
var RLM = String.fromCharCode(0x200F);
ok((tx.match(new RegExp(RLM, 'g')) || []).length === 4 && N.summaryText(full(), 'en', null, '').indexOf(RLM) < 0, 'Hebrew text: a right-to-left mark after each of the 4 split items (keeps "Meta 55%" together in WhatsApp); none in English');
ok(tx.indexOf('תקציב פרסום: ₪25,000 בחודש, ₪300,000 בשנה') > -1 && tx.split(RLM).join('').indexOf('חלוקת התקציב: Meta 55%, Google 25%, עיתונות קהילתית 15%, אתרי נדלן 5%') > -1 && tx.indexOf('התוכנית: שלושה שווקים, ₪72,000 לשנה') > -1, 'budget a month and a year, the split, the plan a year', tx.split('\n')[4]);
ok(tx.indexOf(N.STR.he.leads) > -1 && tx.indexOf(N.STR.he.t_paid) > -1 && /\/international-campaigns\/$/.test(tx), 'the WhatsApp lead line, the ad budget paid directly, the page link');
ok(tx.indexOf('דנה') < 0 && tx.indexOf('050') < 0 && tx.indexOf('@') < 0 && tx.indexOf('לוי יזמות') < 0, 'no name, company, phone or email in the shared text');
ok(tx.indexOf('NLC-') < 0 && N.summaryText(full(), 'he', 'NLC-261107-AB12', '').indexOf('מספר התוכנית: NLC-261107-AB12') > -1, 'the reference only after the brief is saved');
var te = N.summaryText(full(), 'en', 'NLC-261107-AB12', '');
ok(te.indexOf('Markets and communities: France, Canada') > -1 && te.indexOf('Ad budget: ₪25,000 a month, ₪300,000 a year') > -1 && te.indexOf('The plan: Three markets, ₪72,000 a year') > -1 && te.indexOf('Plan number: NLC-261107-AB12') > -1, 'English text');
ok(!DASH.test(tx + te) && !/מע.?"?מ|VAT/.test(tx + te), 'no long dash, no VAT wording');
ok(N.waUrl('a b') === 'https://wa.me/?text=a%20b', 'WhatsApp: wa.me with text only, no phone number');

console.log('\n8. the payment link');
ok(N.payUrl('three', 'NLC-1') === null, 'no product: no link (the page says a link is sent today)');
N.plans.three.productUrl = 'https://nad-lan.co.il/checkout/?add-to-cart=9101';
ok(N.payUrl('three', 'NLC-261107-AB12') === 'https://nad-lan.co.il/checkout/?add-to-cart=9101&nlc_ref=NLC-261107-AB12', 'with a product: the checkout link plus the reference');
N.plans.three.productUrl = 'javascript:alert(1)'; ok(N.payUrl('three', 'x') === null, 'a javascript: link is refused');
N.plans.three.productUrl = 'http://nad-lan.co.il/x'; ok(N.payUrl('three', 'x') === null, 'a plain http link is refused');
N.plans.three.productUrl = '/checkout/?add-to-cart=7'; ok(N.payUrl('three', 'R') === '/checkout/?add-to-cart=7&nlc_ref=R', 'a site path is fine');
N.plans.three.productUrl = null;
N.configure({ endpoint: 'https://nad-lan.co.il/wp-json/nadlan/v1/campaign-brief', privacy: '/privacy/', plans: { one: { productUrl: 'https://nad-lan.co.il/checkout/?add-to-cart=1' }, flag: { productUrl: '"><script>' }, gold: { productUrl: '/x' } } });
ok(N.endpoint === 'https://nad-lan.co.il/wp-json/nadlan/v1/campaign-brief' && N.privacy === '/privacy/' && N.plans.one.productUrl === 'https://nad-lan.co.il/checkout/?add-to-cart=1' && N.plans.flag.productUrl === null && !N.plans.gold, 'window.NLCAMP_CONFIG: endpoint, privacy, product links; a bad link becomes null, an unknown plan is ignored');
N.plans.one.productUrl = null; N.endpoint = null; N.privacy = null;
ok(N.REF_RE.test('NLC-261107-AB12') && !N.REF_RE.test('NLC-261107-ab12') && !N.REF_RE.test('<b>NLC-261107-AB12'), 'only a well formed reference is shown');

console.log('\n8b. first-payment mode (Morning takes one charge of up to about 20,000, 7.11.2026)');
ok(N.firstPay('three') === null && N.restOf('three') === 0, 'no firstPay: the full plan in one charge, no rest');
N.configure({ plans: { one: { productUrl: '/checkout/?add-to-cart=8822', firstPay: 18000 }, three: { productUrl: '/checkout/?add-to-cart=8823', firstPay: 18000 }, flag: { productUrl: '/checkout/?add-to-cart=8824', firstPay: 18000 } } });
ok(N.firstPay('one') === 18000 && N.restOf('one') === 18000 && N.restOf('three') === 54000 && N.restOf('flag') === 126000, 'firstPay 18,000: the rest 18,000 / 54,000 / 126,000');
ok(N.payUrl('three', 'NLC-261107-AB12') === '/checkout/?add-to-cart=8823&nlc_ref=NLC-261107-AB12', 'the button goes to the first-payment product with the reference');
var badFp = [0, -18000, 36000, 50000, 18000.5, '18000', null, NaN].map(function (v) { N.configure({ plans: { one: { firstPay: v } } }); return N.plans.one.firstPay; });
ok(badFp.every(function (v) { return v === null; }), 'firstPay refused when 0, negative, not below the price, not whole, a string, null or NaN', badFp);
N.configure({ plans: { three: { firstPay: 18000 } } }); N.configure({ plans: { three: { productUrl: '/x' } } });
ok(N.plans.three.firstPay === 18000, 'a config without firstPay leaves it as it was');
var he1 = N.STR.he, en1 = N.STR.en;
ok(he1.payFirst === 'לתשלום ראשון: {first} ({plan}, {price} לשנה)' && en1.payFirst === 'Pay the first part: {first} ({plan}, {price} a year)', 'the button wording, as the coordinator wrote it');
ok(he1.payRest === 'את היתרה, {rest}, משלמים בתשלומים של עד {part}, בקישורים שנשלחים אליכם.' && en1.payRest === 'The rest, {rest}, is paid in parts of up to {part} through links we send you.', 'the rest line, as the coordinator wrote it (the part amount filled from firstPay, 18,000)');
ok(N.tpl(he1.payFirst, { first: N.money(18000, 'he'), plan: he1.p_three, price: N.money(72000, 'he') }) === 'לתשלום ראשון: ₪18,000 (שלושה שווקים, ₪72,000 לשנה)'
  && N.tpl(en1.payRest, { rest: N.money(54000, 'en'), part: N.money(18000, 'en') }) === 'The rest, ₪54,000, is paid in parts of up to ₪18,000 through links we send you.', 'filled: "לתשלום ראשון: ₪18,000 (שלושה שווקים, ₪72,000 לשנה)" and the English rest line');
N.PLAN_ORDER.forEach(function (k) { N.plans[k].productUrl = null; N.plans[k].firstPay = null; });

console.log('\n9. the words: Hebrew and English complete, copy rules');
var he = N.STR.he, en = N.STR.en, hk = Object.keys(he), ek = Object.keys(en);
var noEn = hk.filter(function (k) { return !(k in en); }), noHe = ek.filter(function (k) { return !(k in he); });
ok(!noEn.length && !noHe.length, 'every Hebrew key has an English key and back (' + hk.length + ' keys)', noEn.concat(noHe));
ok(hk.every(function (k) { return String(he[k]).trim() && String(en[k]).trim(); }), 'no empty string');
var ph = hk.filter(function (k) { var a = (he[k].match(/\{\w+\}/g) || []).sort().join(), b = (en[k].match(/\{\w+\}/g) || []).sort().join(); return a !== b; });
ok(!ph.length, 'the same {placeholders} in both languages', ph);
var used = ['m_', 'l_', 'b_', 'k_', 'p_', 'ch_', 'chs_'], need = [];
N.MARKETS.forEach(function (m) { need.push('m_' + m.id); }); N.LANGS.forEach(function (l) { need.push('l_' + l); });
N.BUYERS.forEach(function (b) { need.push('b_' + b, 'b_' + b + '_d'); }); N.KINDS.forEach(function (x) { need.push('k_' + x, 'k_' + x + '_d'); });
N.PLAN_ORDER.forEach(function (p) { need.push('p_' + p, 'p_' + p + '_d'); }); N.SPLIT.forEach(function (c) { need.push('ch_' + c.k, 'chs_' + c.k); });
ok(need.every(function (k) { return k in he && k in en; }), 'a name for every market, language, buyer, project kind, plan and channel (' + need.length + ')', need.filter(function (k) { return !(k in he); }));
var all = hk.map(function (k) { return he[k]; }).join('\n'), allE = ek.map(function (k) { return en[k]; }).join('\n');
ok(!DASH.test(all + allE), 'no long dash (– or —) in any string');
var BAN_HE = ['ממשק', 'מערכת', 'פלטפורמ', 'אלגוריתם', 'דמו', 'סימולציה', 'הדגמה', 'מנגנון', 'אינטראקטיבי', 'טכנולוגי', 'דיגיטלי'];
var BAN_EN = ['interface', 'system', 'platform', 'algorithm', 'demo', 'simulation', 'interactive', 'technology'];
var hitH = BAN_HE.filter(function (w) { return all.indexOf(w) > -1; }), hitE = BAN_EN.filter(function (w) { return allE.toLowerCase().indexOf(w) > -1; });
ok(!hitH.length && !hitE.length && !/\bAI\b/.test(all + allE), 'no tech words in Hebrew or English (ממשק, מערכת, פלטפורמה, אלגוריתם, AI, דמו, סימולציה ...)', hitH.concat(hitE));
ok(!/מע.?"?מ|מע״מ|VAT/i.test(all + allE) && he.perYearShort === 'לשנה' && en.perYearShort === 'a year', 'no VAT wording; prices say "לשנה" / "a year"');
ok(!/יהוד|Jewish|religio|ethnic|דת[יו]/i.test(all + allE), 'no religion or ethnicity targeting words (Meta and Google housing rules)');
ok(he.s1aim === 'הפרסום מכוון לפי מדינה, עיר ושפה, ובעיתונות ובניוזלטרים של הקהילות.' && en.s1aim === 'Ads are aimed by country, city and language, plus community press and newsletters.', 'step 1 targeting line, as the coordinator wrote it');
ok(he.leads === 'כל פנייה מגיעה אליכם בוואטסאפ, עם מה שהקונה פתח בפרויקט.' && en.leads === 'Every lead reaches you on WhatsApp with what the buyer opened in the project.' && !/שגוי|מוחלפ|replace|guarant|מובטח/i.test(all + allE), 'step 5 lead line: WhatsApp with what the buyer opened, and no guarantee anywhere (coordinator, 7.11)');
ok(he.payLater === 'קישור לתשלום יישלח אליכם עוד היום.' && en.payLater === 'A payment link will be sent to you today.', 'the honest payment line while there is no product');
ok(/^(בנו|המשיכו|שלחו)/.test(he.next) && /^שלחו/.test(he.send) && he.back === 'חזרה', 'buttons in the plural ("המשיכו", "שלחו")');
var emoji = /[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}]/u; ok(!emoji.test(SRC), 'no emoji in the file');

console.log('\n10. the file itself');
ok(!/localStorage|sessionStorage|indexedDB|document\.cookie/.test(SRC), 'no browser storage, no cookies');
ok(!/location\.hash\s*=|history\.(push|replace)State/.test(SRC), 'nothing written to the address (the state stays in memory)');
ok(/method: 'POST'/.test(SRC) && /\/wp-json\/nadlan\/v1\/campaign-brief/.test(SRC) && /credentials: 'omit'/.test(SRC), 'the brief goes by POST to /wp-json/nadlan/v1/campaign-brief, no cookies');
var hex = (SRC.match(/#[0-9A-Fa-f]{6}\b/g) || []).map(function (h) { return h.toUpperCase(); });
var TOK = ['#2F6F86', '#1F4B5C', '#4F9A5C', '#8E7CC3', '#F2D15A', '#C42550', '#12202A', '#3E4C58', '#5E6A75', '#D3DCE2', '#F6F8F9', '#FFFFFF'];
ok(hex.every(function (h) { return TOK.indexOf(h) > -1; }), 'every colour is a NadLan Instruments token', hex.filter(function (h) { return TOK.indexOf(h) < 0; }));
ok(!/gradient/i.test(SRC) && (SRC.match(/box-shadow:(?!none)/g) || []).length === 0, 'no gradient, no shadow (borders only)');
ok((SRC.match(/class="is-survey"/g) || []).length === 1 && (SRC.match(/var\(--nli-survey\)/g) || []).length === 1, 'survey red on one figure only: the yearly total (one use in the markup, one colour rule)');
ok(!/Karantina/.test(SRC), 'the title face comes from core.css (Karantina on Hebrew pages, 32 px and more), not set again here');

console.log('\n11. the same offer on the server (inc/campaign-brief.php)');
var php = cp.spawnSync('php', [path.join(HERE, 'test_campaign_brief.php'), '--json'], { encoding: 'utf8' });
if (php.error || php.status !== 0) { ok(false, 'php ran', php.error ? php.error.code : php.stderr); }
else {
  var S = JSON.parse(php.stdout);
  ok(N.PLAN_ORDER.every(function (k) { return S.plans[k].price === N.plans[k].price && (S.plans[k].markets || null) === N.plans[k].markets; }), 'plan prices and market limits equal');
  ok(N.PLAN_ORDER.every(function (k) { return S.plans[k].he === N.STR.he['p_' + k] && S.plans[k].en === N.STR.en['p_' + k]; }), 'plan names equal in both languages');
  ok(same(Object.keys(S.markets), N.MARKETS.map(function (m) { return m.id; })) && N.MARKETS.every(function (m) { return same(S.markets[m.id].langs, m.langs) && S.markets[m.id].he === N.STR.he['m_' + m.id] && S.markets[m.id].en === N.STR.en['m_' + m.id]; }), 'markets: ids, order, languages and names equal');
  ok(same(S.langs, N.LANGS) && same(S.buyers, N.BUYERS) && same(S.kinds, N.KINDS) && same(S.channels, N.SPLIT.map(function (c) { return c.k; })), 'languages, buyers, project kinds and channels equal');
  ok(S.budget.min === N.BUDGET.min && S.budget.max === N.BUDGET.max && S.budget.step === N.BUDGET.step, 'budget range and step equal');
  ok(same(S.rec.map(function (x) { return x || null; }), rec), 'the recommendation table equal for 0 to 10 markets');
  ok(S.first === 18000 && N.PLAN_ORDER.every(function (k) { return S.firstPay[k] === 18000 && S.plans[k].product === { one: 8822, three: 8823, flag: 8824 }[k]; }), 'server defaults: first amount 18,000 on every plan, products 8822 / 8823 / 8824 with no option set', [S.first, S.firstPay]);
  N.configure({ plans: { one: { firstPay: S.firstPay.one }, three: { firstPay: S.firstPay.three }, flag: { firstPay: S.firstPay.flag } } });
  ok(N.PLAN_ORDER.every(function (k) { return N.firstPay(k) === S.firstPay[k]; }), 'the server firstPay values are accepted by the planner as printed');
  N.PLAN_ORDER.forEach(function (k) { N.plans[k].firstPay = null; });
}

console.log('\n' + (n - fails) + ' of ' + n + ' passed' + (fails ? ', ' + fails + ' FAILED' : ''));
process.exit(fails ? 1 : 0);
