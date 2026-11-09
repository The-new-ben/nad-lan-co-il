/* HAD-683: unit checks of the /buying-apartment/ hub tools (buying.js on prices-common.js), against the data files, against values
   computed here independently, and against the PHP server summaries of inc/buying-hub.php (the same numbers on both sides).
     node tools/instruments/test_buying_hub.js [--facts]   -> "N passed" or the failures, exit 1 on a failure
   --facts prints the worked numbers the page text quotes (docs/research/2026-11-07-prices-buying/page-9-new.html). */
'use strict';
const fs = require('fs'), path = require('path'), vm = require('vm'), cp = require('child_process');
const ROOT = path.join(__dirname, '..', '..'), INS = path.join(ROOT, 'plugins', 'nadlan-config', 'assets', 'instruments');
const J = f => JSON.parse(fs.readFileSync(path.join(INS, 'data', f), 'utf8'));
const ctx = { window: {}, document: {}, Intl, Math, JSON, console };
ctx.window.NadLanInstruments = { register() {}, fmt: {}, esc: s => String(s) };
vm.createContext(ctx);
['prices-common.js', 'buying.js', 'buying2.js', 'buying3.js'].forEach(f => vm.runInContext(fs.readFileSync(path.join(INS, 'tools', f), 'utf8'), ctx, { filename: f }));
const B = ctx.window.NLBH, X = ctx.window.NLBH2;
const BU = J('buying.json'), PT = J('ptax.json'), NR = J('nrm.json'), Z = J('zakaut.json'), O = J('orechdin.json'), BM = J('boi-mortgage.json'), CO = J('cost.json'), C = J('cbs-200010.json'), PH = J('prices-hub.json'), V = J('value.json');
const M = B.model({ buying: BU, ptax: PT, nrm: NR, zakaut: Z, orechdin: O, boim: BM, cost: CO, phub: PH, value: V, d9: C });
let n = 0; const fail = [];
const t = (name, ok, info) => { if (ok) n++; else fail.push(name + (info !== undefined ? ' | ' + JSON.stringify(info) : '')); };
const near = (a, b, e) => a != null && b != null && Math.abs(a - b) <= (e == null ? 1e-6 : e);

/* ---- the content file ---- */
const nodate = s => s.replace(/\d{1,2}\.\d{1,2}\.\d{4}/g, '').replace(/20\d\d/g, '');
const ids = BU.statuses.map(s => s.id);
t('12 buyer statuses, unique ids', ids.length === 12 && new Set(ids).size === 12, ids);
t('every status names a purchase-tax track that exists', BU.statuses.every(s => PT.tracks[s.ptax]), BU.statuses.map(s => s.ptax));
t('every status names an LTV key of nrm.json', BU.statuses.every(s => NR.ltv_by_status[s.ltv] > 0));
const FLAGS = ['zakaut', 'marriage', 'service', 'career', 'reserve', 'olim', 'disability', 'ptax_disabled', 'upgrader', 'invest', 'foreign'];
t('every flag is one the rules know', BU.statuses.every(s => s.flags.every(f => FLAGS.includes(f))));
t('7 stages and every step in one of them', BU.stages.length === 7 && BU.steps.every(x => x.st >= 0 && x.st <= 6));
t('step ids unique', new Set(BU.steps.map(x => x.id)).size === BU.steps.length);
t('no number written into the content file (numbers come from the data files)', BU.steps.every(x => !/\d{3}/.test(nodate(x.t + x.d))), BU.steps.filter(x => /\d{3}/.test(nodate(x.t + x.d))).map(x => x.id));
// every placeholder fills, for every status and type
let unfilled = [];
BU.statuses.forEach(s => ['used', 'new', 'any'].forEach(ty => B.steps(BU, s, ty, M).forEach(x => { if (/[{}]/.test(x.t + x.d)) unfilled.push(s.id + ':' + x.id); })));
t('every {placeholder} fills from the data files', !unfilled.length, unfilled.slice(0, 5));
// links: an anchor on the page, an official gov.il page, or a path that exists in the live sitemap (read 7.11.2026)
const SM = path.join(process.env.NLBH_SITEMAP || '', '');
let paths = null; try { paths = new Set(JSON.parse(fs.readFileSync(SM, 'utf8'))); } catch (e) {}
const ANCH = ['#equity', '#ladder', '#offer', '#my-plan'];
const hrefs = new Set(); BU.steps.forEach(x => { hrefs.add(x.href); Object.values(x.alt || {}).forEach(h => hrefs.add(h)); });
const badLinks = [...hrefs].filter(h => !(ANCH.includes(h) || /^https:\/\/www\.gov\.il\//.test(h) || (paths ? paths.has(h) : /^\/[a-z0-9\-\/]+\/$/.test(h))));
t('every step link is a page anchor, gov.il, or a live URL' + (paths ? ' (sitemap checked)' : ' (shape only: set NLBH_SITEMAP)'), !badLinks.length, badLinks);

/* ---- purchase tax ---- */
const f1 = PT.tracks.single[0][0];
t('single: nothing up to the first bracket', B.tax(f1, 'single', PT) === 0);
t('single: 3.5% just above it', near(B.tax(f1 + 100000, 'single', PT), 100000 * 0.035));
t('single: across three brackets', near(B.tax(3000000, 'single', PT), (2347040 - 1978745) * 0.035 + (3000000 - 2347040) * 0.05));
t('extra and foreign: 8% from the first shekel', B.tax(1000000, 'extra', PT) === 80000 && B.tax(1000000, 'foreign', PT) === 80000);
t('oleh: 0.5% above the exempt part', near(B.tax(3000000, 'oleh', PT), (3000000 - 1978745) * 0.005));
t('disabled: 0.5% above the exempt part up to the cap, the normal brackets above it', near(B.tax(2400000, 'single', PT, true), (2400000 - f1) * 0.005) && near(B.tax(2600000, 'single', PT, true), B.tax(2600000, 'single', PT)));
t('bracket text', B.brackets('single', PT).indexOf('3.5% עד 2,347,040 ₪') > 0 && / ו־10% מעל 20,183,565 ₪$/.test(B.brackets('single', PT)), B.brackets('single', PT));

/* ---- the rules per status ---- */
const R = id => B.rules(B.status(BU, id), M);
const ltvTxt = id => R(id).filter(r => r.k === 'ltv')[0].t;
t('LTV 75% first home, 70% replacement, 50% second, 50% foreign', /75%/.test(ltvTxt('first')) && /70%/.test(ltvTxt('replace')) && /50%/.test(ltvTxt('extra')) && /50%/.test(ltvTxt('foreign')));
t('every rule has a dated source, except the honest "no number" line', BU.statuses.every(s => B.rules(s, M).every(r => r.k === 'career' ? r.src === null : r.src && r.src.label && r.src.date)));
t('career line carries no number', !/\d/.test(R('career').filter(r => r.k === 'career')[0].t));
t('reserve line from zakaut.json', R('reserve').some(r => r.k === 'reserve' && r.t.indexOf(Z.reserve.min_pct + '% ועד ' + Z.reserve.max_pct_person + '%') > 0));
t('zakaut band from the official table', R('first').some(r => r.k === 'zakaut' && r.t.indexOf('54,240') > 0 && r.t.indexOf('161,665') > 0));
t('foreign: no eligibility loan, investment LTV', !R('foreign').some(r => r.k === 'zakaut'));
t('oleh: the 7-year window', R('oleh').some(r => r.k === 'ptax' && r.t.indexOf('7 שנים') > 0));

/* ---- steps ---- */
const S = (id, ty) => B.steps(BU, B.status(BU, id), ty, M).map(x => x.id);
t('sell-the-old-flat step only for a replacement home', S('replace', 'any').includes('sellplan') && !S('first', 'any').includes('sellplan'));
t('eligibility steps only where an eligibility loan applies', S('young', 'any').includes('zakaut') && !S('foreign', 'any').includes('zakaut') && !S('extra', 'any').includes('zakautuse'));
t('developer steps hidden for second-hand, and the other way round', !S('first', 'used').includes('salelaw') && !S('first', 'new').includes('tabu') && S('first', 'any').includes('salelaw') && S('first', 'any').includes('tabu'));
t('purchase-tax step links the status page', B.steps(BU, B.status(BU, 'foreign'), 'any', M).filter(x => x.id === 'ptax')[0].href === '/israel-purchase-tax-foreign-residents/');
const fl = B.steps(BU, B.status(BU, 'first'), 'any', M);
t('deadline steps carry the Tax Authority days', fl.some(x => x.t.indexOf('בתוך ' + PT.pay.declare_days + ' יום') > 0) && fl.some(x => x.t.indexOf('בתוך ' + PT.pay.pay_days + ' יום') > 0));
t('next step: first undone at or after the stage', B.next(fl, {}, 3).st === 3 && B.next(fl, { goal: 1 }, 0).id === 'equity');

/* ---- money ---- */
const rr = B.rate(BM);
t('BoI rate: fixed not linked, its month', rr.rate === BM.rates.fixed_nl.rate && /^\d{4}-\d{2}$/.test(rr.month));
const nomI = 1200 * (Math.pow(1 + rr.rate / 100, 1 / 12) - 1), rI = nomI / 1200, payI = 1e6 * rI / (1 - Math.pow(1 + rI, -300));
t('Spitzer payment on the effective rate', near(B.pmt(1e6, rr.rate, 25), payI, 1e-6));
t('present value is the inverse of the payment', near(B.pv(B.pmt(1234567, rr.rate, 30), rr.rate, 30), 1234567, 1e-3));
const o1 = { ltv: 0.75, track: 'single', PT: PT, dis: false, lawyerPct: CO.lawyer.from, vat: CO.vat, loanCap: Infinity };
[100000, 300000, 500000, 1000000].forEach(E => { const x = B.maxPrice(E, o1); t('max price for ' + E + ': fits, and 1,000 more does not', x.cash <= E + 1e-6 && B.need(x.P + 1000, o1).cash > E, [x.P, x.cash]); });
const capd = B.maxPrice(500000, Object.assign({}, o1, { loanCap: B.loanCap(15000, 0.3, rr.rate, 25) }));
t('an income cap lowers the price and is flagged', capd.capped && capd.P < B.maxPrice(500000, o1).P && near(capd.loan, B.loanCap(15000, 0.3, rr.rate, 25), 1));
const x3 = B.maxPrice(300000, o1), lad = B.ladder(PH, x3.P);
t('ladder: 24 cities, every marked cell at or under the price', lad.length === 24 && lad.every(c => [3, 4, 5].every(r => !c['f' + r] || c['r' + r].v <= x3.P)));
t('ladder: the latest published quarter per city', lad.every(c => !c.r4 || c.r4.v === PH.city.filter(z => z.n === c.n)[0].r4[c.r4.i]));
const src = B.sources({ price: 2e6, ltv: 0.75, tax: 1000, law: 11800, rate: rr.rate, years: 25, items: [{ id: 'own', kind: 'cash', amt: 400000 }, { id: 'fund', kind: 'loan', amt: 50000, rate: 0, years: 5 }, { id: 'loan', kind: 'loan', amt: 60000, rate: 6, years: 5 }] });
t('sources: need = the unfinanced part + tax + lawyer', near(src.need, 500000 + 1000 + 11800));
t('sources: a loan with no rate shows no number', src.rows[1].missing && src.rows[1].pay === null);
t('sources: a loan with a rate adds its payment', near(src.rows[2].pay, B.pmt(60000, 6, 5)) && near(src.total, src.mpay + src.rows[2].pay));
t('sources: the mortgage stops at the LTV', src.mort === 1.5e6);
const CB = B.cbsYoY(C);
t('construction index over 12 months from the CBS file', near(CB.g, C.months[CB.to] / C.months[CB.from] - 1) && CB.to === C.latest);
const sx = B.stress({ price: 2e6, paidPct: 0.1, months: 30, share: 0.5, g: CB.g, ltv: 0.75, rate: rr.rate, years: 25, appr: 1 });
t('stress: the linked balance', near(sx.add, 1.8e6 * 0.5 * (Math.pow(1 + CB.g, 2.5) - 1)) && near(sx.due, 1.8e6 + sx.add));
t('stress: the cash at handover = balance - LTV x value', near(sx.cash, sx.due - 0.75 * (2e6 + sx.add)) && sx.rows.length === 3 && sx.rows[2].pay > sx.rows[0].pay);
t('stress: a lower appraisal asks for more cash', B.stress(Object.assign({ price: 2e6, paidPct: 0.1, months: 30, share: 0.5, g: CB.g, ltv: 0.75, rate: rr.rate, years: 25 }, { appr: 0.9 })).cash > sx.cash);

/* ---- the offer helper ---- */
const rg = PH.city.filter(c => c.n === 'רמת גן')[0], L = B.lastQ(rg.r4, PH.q);
const of = B.offer(PH, V, { code: rg.code, rooms: 4, ask: Math.round(L.v * 1.08), hood: '' });
t('offer: the city median of the latest published quarter', of.med === L.v && of.q === PH.q[L.i]);
const vc = Object.values(V.cities).filter(c => c.code === rg.code)[0], hm = vc.hoods.filter(h => h.r4).map(h => h.r4[0]);
t('offer: neighbourhoods with a lower median, counted from value.json', of.hoods.length === hm.length && of.lower === hm.filter(v => v < of.ask).length, [of.lower, of.hoods.length]);
t('offer: the range starts at the lowest of the last 4 quarters and ends at the median', near(of.lo, Math.min(...of.four.map(f => f.v))) && of.hi === of.med && of.lo <= of.hi);
t('offer: an asking price under the range has no market range', B.offer(PH, V, { code: rg.code, rooms: 4, ask: of.lo * 0.9, hood: '' }).range === false);
const h0 = of.hoods[0], ofh = B.offer(PH, V, { code: rg.code, rooms: 4, ask: Math.round(h0.v * 1.05), hood: h0.id });
t('offer: a neighbourhood becomes the basis', ofh.hood && ofh.basis === h0.v && near(ofh.vs, Math.round(h0.v * 1.05) / h0.v - 1));
t('offer: the district index of the city', of.dist && /^[֐-׿ ]+$/.test(of.dist.n));
t('offer: the whole country works', B.offer(PH, V, { code: 0, rooms: 4, ask: 2.2e6, hood: '' }).med === B.lastQ(PH.il.r4, PH.q).v);

/* ---- Phase 2 (buying2.js) ---- */
t('dates: +30 and +60 days, month ends clamp', X.addDays('2026-11-08', 30) === '2026-12-08' && X.addDays('2026-11-08', 60) === '2027-01-07' && X.addMonths('2026-01-31', 1) === '2026-02-28' && X.addMonths('2026-11-08', 24) === '2028-11-08');
const D1 = X.dates(M, '2026-11-08', 'used', B.status(BU, 'first')), ids1 = D1.map(x => x.id);
t('deadlines, first home second-hand: declare, pay, eligibility loan 12 months, then the undated', JSON.stringify(ids1) === JSON.stringify(['declare', 'paytax', 'zakaut', 'objection', 'cgt']) && D1[0].d === '2026-12-08' && D1[1].d === '2027-01-07' && D1[2].d === '2027-11-08', ids1);
const D2 = X.dates(M, '2026-11-08', 'new', B.status(BU, 'replace'));
t('deadlines, replacement from a developer: sell within 24 months, no eligibility loan, no capital-gains advance', D2.some(x => x.id === 'sellby' && x.d === '2028-11-08') && !D2.some(x => x.id === 'zakaut' || x.id === 'cgt'));
t('deadlines: eligibility loan 36 months from a developer', X.dates(M, '2026-11-08', 'new', B.status(BU, 'young')).some(x => x.id === 'zakaut' && x.d === '2029-11-08'));
t('deadlines: every row has an official source', D1.concat(D2).every(x => x.src && x.src.label && x.src.url));
const ics = X.ics(D1, '2026-11-08T10:00:00.000Z'), lines = ics.split('\r\n');
t('ics: a calendar, one event per dated row, CRLF, 75-octet lines', ics.startsWith('BEGIN:VCALENDAR\r\n') && ics.trim().endsWith('END:VCALENDAR') && (ics.match(/BEGIN:VEVENT/g) || []).length === 3 && lines.every(l => Buffer.byteLength(l, 'utf8') <= 75) && ics.indexOf('DTSTART;VALUE=DATE:20261208') > 0 && ics.indexOf('TRIGGER:-P3D') > 0);
const pr = { PT, NRM: NR, CO, rate: rr.rate, years: 25 };
const sl = X.sell(Object.assign({ newP: 3e6, saleP: 2e6, oldLoan: 5e5, oldPay: 4000, cash: 15e4, months: 6, bridgeRate: 6 }, pr));
t('sell: replacement LTV 70%, need = 30% + single-home tax + lawyer, bridge = need - cash', sl.ltv === 0.7 && near(sl.need, 9e5 + B.tax(3e6, 'single', PT) + 3e6 * CO.lawyer.from / 100 * (1 + CO.vat)) && near(sl.bridge, sl.need - 15e4));
t('sell: the tax risk is the additional-home brackets', near(sl.taxExtra - sl.taxRep, B.tax(3e6, 'extra', PT) - B.tax(3e6, 'single', PT)) && sl.taxExtra > sl.taxRep);
t('sell: double months = old payment + bridge interest', near(sl.bi, sl.bridge * 0.06 / 12) && near(sl.double, 6 * (4000 + sl.bi)) && near(sl.late.extra, 3 * (4000 + sl.bi)) && sl.late.taxJump === 0);
t('sell: 3 months late past the window costs the tax jump', X.sell(Object.assign({ newP: 3e6, saleP: 2e6, oldLoan: 5e5, oldPay: 4000, cash: 15e4, months: 22, bridgeRate: null }, pr)).late.taxJump > 0);
t('sell: no bridge rate, no interest number', X.sell(Object.assign({ newP: 3e6, saleP: 2e6, oldLoan: 5e5, oldPay: 0, cash: 15e4, months: 6, bridgeRate: null }, pr)).bi === null);
const cmp = X.compare([{ name: 'א', price: 2e6, type: 'used' }, { name: 'ב', price: 2.5e6, type: 'new' }], { ltv: 0.75, track: 'single', dis: false, PT, CO, rate: rr.rate, years: 25 });
t('compare: equity = the need of the equity tool, payment = Spitzer, a range for the all-in cost', near(cmp[0].eq, B.need(2e6, o1).cash) && near(cmp[1].pay, B.pmt(2.5e6 * 0.75, rr.rate, 25)) && cmp.every(r => r.lo < r.hi));
const who = X.who(BU, M);
t('who pays: 8 rows, each with an official source, numbers filled', who.length === 8 && who.every(r => r.src && r.src.label && r.src.url && !/[{}]/.test(r.d)) && who[3].d.indexOf('7.5%') === 0);
t('who pays: the contract line fills the 2026 fees', B.fill(BU.who_contract, M).indexOf('188 ₪') > 0 && !/[{}]/.test(B.fill(BU.who_contract, M)));
const hp = (id, tg) => X.help(BU, B.status(BU, id), tg || {}, M).map(h => h.id);
t('benefits: first home without toggles', JSON.stringify(hp('first')) === JSON.stringify(['base', 'service', 'dira']), hp('first'));
t('benefits: toggles add priority zone and Negev', hp('first', { zoneA: 1, negev: 1 }).includes('zoneA') && hp('first', { zoneA: 1, negev: 1 }).includes('negev'));
t('benefits: none for a foreign resident or a second home', !hp('foreign').length && !hp('extra').length);
t('benefits: olim, disability, reserve', hp('oleh').includes('olimtax') && hp('disabled').includes('distax') && hp('reserve').includes('reserve'));
const all = X.help(BU, B.status(BU, 'disabled'), { zoneA: 1, zoneB: 1, negev: 1, parent: 1, ten: 1 }, M).concat(X.help(BU, B.status(BU, 'oleh'), {}, M));
t('benefits: every number filled, every card has a link, a year stays a year', all.every(h => !/[{}]/.test(h.d) && h.href) && all.filter(h => h.id === 'ten')[0].d.indexOf('2025') > 0 && all.filter(h => h.id === 'ten')[0].d.indexOf('2,025') < 0);
t('benefits: the unverified grant is named as left out', /50,000/.test(BU.help_out) && !BU.help.some(h => /50,000|50 אלף/.test(h.d)));
t('visit sheet: 5 groups, 31 questions', BU.visit.length === 5 && BU.visit.reduce((a, g) => a + g.q.length, 0) === 31);
t('visit count', JSON.stringify(X.visitCount({ a: { '0.0': 'y', '0.1': 'n', '1.0': 'q', '1.1': 'y' } })) === '{"y":2,"n":1,"q":1}');
const related = (fs.readFileSync(path.join(ROOT, 'plugins', 'nadlan-config', 'inc', 'buying-hub.php'), 'utf8').match(/'(\/[a-z0-9\-\/]+\/)' =>/g) || []).map(x => x.slice(1, -4));
t('every related link of the registry is a live URL' + (paths ? '' : ' (shape only)'), related.length >= 30 && related.every(h => paths ? paths.has(h) : true), related.filter(h => paths && !paths.has(h)));

/* ---- Phase 3 (buying3.js, HAD-686): bpay, bsign, bkeys, breg, bmemo and the reading layer ---- */
const X3 = ctx.window.NLBH3, G3 = ctx.window.NLBG, OA = O.cgt_advance, PY = BU.pay;
t('buying3: pure logic loaded (NLBH3, NLBG)', !!X3 && typeof X3.pay === 'function' && typeof X3.memo === 'function' && !!G3 && typeof G3.norm === 'function');
const noNum = s => !/\d{3}/.test(String(s).replace(/סעיף \d+|m324/g, '').replace(/\d{1,2}\.\d{1,2}\.\d{4}/g, ''));
t('pay: five payments in order, each with when, to and a protection (the advance carries the law)', JSON.stringify(PY.items.map(x => x.id)) === '["first","seller","loan","adv","last"]' && PY.items.every(x => x.t && x.when && x.to && (x.id === 'adv' || x.safe)));
const advRow = BU.who.filter(r => r.src === PY.adv_src);
t('pay: the advance rule is the bwho row with the same source (tax15)', advRow.length === 1 && B.fill(advRow[0].d, M).indexOf('7.5%') === 0 && B.fill(advRow[0].d, M).indexOf('15%') > 0 && B.fill(advRow[0].d, M).indexOf('40%') > 0);
t('pay, sign, keys, reg, memo: no number written into the content (placeholders, sections and dates only)', [PY, BU.sign, BU.keys.transfers, BU.reg, BU.memo.q, BU.memo.levels].every(o => noNum(JSON.stringify(o))));
t('sign: 5 to bring, 4 to sign, 3 to leave with; every placeholder fills', BU.sign.bring.length === 5 && BU.sign.sign.length === 4 && BU.sign.leave.length === 3 && !/\{[a-z]/.test(B.fill(JSON.stringify(BU.sign), M)) && B.fill(BU.sign.leave[2].d, M).indexOf('30 יום') > 0 && B.fill(BU.sign.leave[2].d, M).indexOf('60 יום') > 0);
t('sign: a src names a law that exists', ['bring', 'sign', 'leave'].every(g => BU.sign[g].every(x => !x.src || BU.laws[x.src])));
t('keys: 3 meters, 2 counts, 5 transfers; how and src are strings or a dated source (never a phone number)', BU.keys.meters.length === 3 && BU.keys.counts.length === 2 && BU.keys.transfers.length === 5 && BU.keys.transfers.every(x => typeof x.how === 'string' && (x.src === '' || (typeof x.src === 'string' && BU.laws[x.src]) || (x.src && x.src.label && x.src.url && /^\d{4}-\d{2}-\d{2}$/.test(x.src.date))) && !/\d{3}/.test(x.how)));
t('reg: 10 steps, unique ids, each with who and the proof; the dated ones are the declaration and the tax payment', BU.reg.length === 10 && new Set(BU.reg.map(x => x.id)).size === 10 && BU.reg.every(x => x.t && x.who && x.doc) && JSON.stringify(BU.reg.filter(x => x.due).map(x => x.due)) === '["declare","pay"]' && BU.reg.every(x => !x.src || BU.laws[x.src]));
t('memo: six questions with the ids the scoring reads, three levels, the section 8 source dated', JSON.stringify(BU.memo.q.map(q => q.id)) === JSON.stringify(X3.MEMO) && ['low', 'mid', 'high'].every(k => BU.memo.levels[k].t && BU.memo.levels[k].d && BU.memo.levels[k].next) && BU.laws[BU.memo.law].label.indexOf('סעיף 8') > 0 && /^\d{4}-\d{2}-\d{2}$/.test(BU.laws[BU.memo.law].date));
/* bpay arithmetic */
const LT = NR.ltv_by_status, payo = o => X3.pay(Object.assign({ O: OA, PT: PT.pay, ltv: LT }, o));
const sum = r => r.rows.reduce((a, x) => a + x.amt, 0);
let sums = [], cnt = 0;
[1200000, 2028800, 2450000, 3333333, 7654321].forEach(P => [0, 0.4, 0.6, 0.75].forEach(lr => [0, 0.05, 0.2, 0.45].forEach(sr => [0, 5, 10, 20, 30].forEach(pct => ['std', 'old', 'none'].forEach(adv => {
  const r = payo({ P, L: Math.round(P * lr), S: Math.round(P * sr), pct, adv });
  if (!r.ok) return; cnt++;
  const own = r.rows.reduce((a, x) => a + x.own, 0), loan = r.rows.reduce((a, x) => a + x.loan, 0);
  if (sum(r) !== P || own !== P - Math.round(P * lr) || loan !== Math.round(P * lr) || r.rows.some(x => x.amt < 0 || x.own < 0 || x.loan < 0 || x.own + x.loan !== x.amt) || r.rows.length !== 5) sums.push([P, lr, sr, pct, adv]);
})))));
t('pay: in every valid case (' + cnt + ') the five payments add up to the price, own money + mortgage split exactly, nothing negative', cnt > 600 && !sums.length, sums.slice(0, 3));
const pv = payo({ P: 2450000, L: 1500000, S: 420000, pct: 10, adv: 'std' });
t('pay: the design case 2,450,000 / 1,500,000 / 420,000 / 10%: 245,000, 420,000, 1,500,000, 183,750, 101,250', pv.ok && JSON.stringify(pv.rows.map(x => x.amt)) === '[245000,420000,1500000,183750,101250]' && pv.own === 950000, pv.rows && pv.rows.map(x => x.amt));
t('pay: the advance is 7.5% of the price, 15% before 7.11.2001, none with a certificate', payo({ P: 2e6, L: 1e6, S: 0, pct: 10, adv: 'std' }).A === 150000 && payo({ P: 2e6, L: 1e6, S: 0, pct: 10, adv: 'old' }).A === 300000 && payo({ P: 2e6, L: 1e6, S: 0, pct: 10, adv: 'none' }).A === 0 && OA.old_before === '2001-11-07');
t('pay: the 40% point is crossed by the mortgage payment in the design case', pv.cross === 2 && payo({ P: 2e6, L: 0, S: 0, pct: 50, adv: 'std' }).cross === 0 && payo({ P: 2e6, L: 0, S: 0, pct: 50, adv: 'std' }).warns.some(w => w.k === 'cross1'));
const sp = payo({ P: 2000000, L: 1400000, S: 900000, pct: 10, adv: 'std' });
t('pay: a seller balance larger than your money left: the mortgage pays the rest of it to his bank, nothing is left for the handover', sp.ok && JSON.stringify(sp.rows.map(x => x.amt)) === '[200000,900000,750000,150000,0]' && sp.rows[1].loan === 500000 && sp.rows[3].loan === 150000 && sp.warns.some(w => w.k === 'split') && sp.warns.some(w => w.k === 'nolast') && sum(sp) === 2000000, sp.rows && sp.rows.map(x => x.amt));
const ek = o => payo(o).errs.map(e => e.k).join(',');
t('pay validation: no price', ek({ P: 0, L: 0, S: 0, pct: 10, adv: 'std' }) === 'price');
t('pay validation: a mortgage above the price', ek({ P: 1e6, L: 1.2e6, S: 0, pct: 10, adv: 'std' }) === 'loan' && /גדולה ממחיר הדירה/.test(payo({ P: 1e6, L: 1.2e6, S: 0, pct: 10, adv: 'std' }).errs[0].t));
t('pay validation: a first payment above 100% or above your own money', ek({ P: 1e6, L: 0, S: 0, pct: 120, adv: 'std' }) === 'pct' && ek({ P: 1e6, L: 950000, S: 0, pct: 10, adv: 'std' }) === 'first');
t('pay validation: the seller balance larger than what is left of the price after the first payment and the advance', ek({ P: 1e6, L: 7e5, S: 830000, pct: 10, adv: 'std' }) === 'seller' && payo({ P: 1e6, L: 7e5, S: 825000, pct: 10, adv: 'std' }).ok);
t('pay validation: the first payment and the advance together above the price', ek({ P: 1e6, L: 0, S: 0, pct: 95, adv: 'std' }) === 'over');
t('pay validation: a handover before the signing', ek({ P: 1e6, L: 5e5, S: 0, pct: 10, adv: 'std', sign: '2026-11-08', hand: '2026-10-01' }) === 'dates');
const pd = payo({ P: 2e6, L: 1e6, S: 0, pct: 10, adv: 'std', sign: '2026-11-08', hand: '2027-02-01' }), bd = X.dates(M, '2026-11-08', 'used', B.status(BU, 'first'));
t('pay dates: the 30 and 60 day deadlines as bdates gives them, the days to the handover', pd.dates.declare === '2026-12-08' && pd.dates.pay === '2027-01-07' && pd.dates.declare === bd.filter(x => x.id === 'declare')[0].d && pd.dates.pay === bd.filter(x => x.id === 'paytax')[0].d && pd.dates.handDays === 85 && X3.addDays('2026-11-08', 30) === X.addDays('2026-11-08', 30));
t('pay: an LTV above the single-home rule is flagged, at the rule it is not', payo({ P: 2e6, L: 1.6e6, S: 0, pct: 10, adv: 'std' }).warns.some(w => w.k === 'ltv') && !payo({ P: 2e6, L: 1.5e6, S: 0, pct: 10, adv: 'std' }).warns.some(w => w.k === 'ltv'));
/* bmemo scoring */
const yes = { price: true, flat: true, dates: true, paid: true, subj: true, both: true }, mm = o => X3.memo(Object.assign({}, yes, o)).level;
t('memo: unanswered questions give no level, and say how many are left', X3.memo({ price: true }).level === null && X3.memo({ price: true }).left === 5 && X3.memo({}).left === 6);
t('memo: essentials + both signed + no "subject to contract" = high', mm({ subj: false, paid: false }) === 'high' && mm({ subj: false, paid: false, dates: false }) === 'high');
t('memo: essentials + money paid = high, even with "subject to contract"', mm({ both: false }) === 'high' && mm({}) === 'high');
t('memo: essentials + both signed + "subject to contract", no money = mid', mm({ paid: false }) === 'mid');
t('memo: signed or paid without the essentials = mid; essentials alone = mid', mm({ price: false, paid: false }) === 'mid' && mm({ flat: false, both: false }) === 'mid' && mm({ paid: false, both: false }) === 'mid');
t('memo: no essentials, nothing signed by both, nothing paid = low', mm({ price: false, flat: false, paid: false, both: false }) === 'low' && X3.memo({ price: false, flat: false, dates: false, paid: false, subj: false, both: false }).level === 'low');
/* breg and bsign helpers */
t('reg: the due dates come from the signing date (declaration 30 days, tax 60 days), none without it', X3.regDue(BU.reg[1], '2026-11-08', PT.pay) === '2026-12-08' && X3.regDue(BU.reg[2], '2026-11-08', PT.pay) === '2027-01-07' && X3.regDue(BU.reg[0], '2026-11-08', PT.pay) === null && X3.regDue(BU.reg[1], '', PT.pay) === null);
t('reg: status count', JSON.stringify(X3.regCount(BU.reg, { warn: 2, declare: 1, ptax: 2 })) === '[7,1,2]');
t('sign: tick count across the three lists', JSON.stringify(X3.ticks({ b: BU.sign.bring, s: BU.sign.sign, l: BU.sign.leave }, { b: { 0: 1, 2: 1 }, l: { 1: 1 } })) === '{"n":3,"all":12}');
/* the reading layer */
t('glossary search key: niqqud, gershayim and maqaf do not matter', G3.norm('רמ״י') === G3.norm('רמ"י') && G3.norm('הַלְוָאָה') === 'הלואה' && G3.norm('ל־30') === 'ל 30' && G3.norm('  נסח   טאבו ') === 'נסח טאבו');
t('glossary count wording', G3.count(1) === 'מונח אחד' && G3.count(60) === '60 מונחים');
t('map: a chapter is read at 60% past the middle of the screen', G3.READ === 0.6 && G3.passed(0, 1000, 600) === 0.6 && G3.passed(500, 1000, 400) === 0 && G3.passed(-2000, 1000, 400) === 1 && G3.passed(0, 0, 400) === 0);

/* ---- the PHP summaries: same numbers ---- */
let php = null;
try {
  const stub = path.join(require('os').tmpdir(), 'nlbh_php_' + process.pid + '.php');
  fs.writeFileSync(stub, "<?php define('ABSPATH','/');function esc_html($s){return htmlspecialchars((string)$s,ENT_QUOTES,'UTF-8');}function esc_attr($s){return esc_html($s);}function add_filter(){}function add_action(){}function wp_strip_all_tags($s){return strip_tags((string)$s);}" +
    "require " + JSON.stringify(path.join(ROOT, 'plugins', 'nadlan-config', 'inc', 'buying-hub.php')) + ";$d=" + JSON.stringify(path.join(INS, 'data') + path.sep) + ";$o=array();foreach(nadlan_bhub_tool_ids() as $i){$o[$i]=nadlan_bhub_summary($i,$d);}" +
    "$f=nadlan_bhub_faq('<h2>קניית דירה: השאלות שלא שואלים את עורך הדין</h2><h3>ש1?</h3><p>ת1</p><h3>ש2?</h3><p>ת2</p><p>עוד</p><h2>אחר</h2><h3>x</h3><p>y</p>');$o['faq']=$f;echo json_encode($o,JSON_UNESCAPED_UNICODE);");
  php = JSON.parse(cp.execFileSync('php', [stub], { encoding: 'utf8' })); fs.unlinkSync(stub);
} catch (e) { fail.push('php summaries did not run | ' + String(e.message).slice(0, 200)); }
if (php) {
  t('PHP: ten summaries, each with its marker', ['bplan', 'bequity', 'bladder', 'boffer', 'bsell', 'bdates', 'bcompare', 'bvisit', 'bwho', 'bhelp'].every(i => php[i] && php[i].indexOf('data-bhub-sum="' + i + '"') > 0));
  t('PHP bwho: 8 rows; bhelp: 13 rows; bvisit: 31 questions', (php.bwho.match(/<tr><td>/g) || []).length === 8 && (php.bhelp.match(/<tr><td>/g) || []).length === 13 && (php.bvisit.match(/<li>/g) || []).length === 31);
  const s5 = X.sell(Object.assign({ newP: B.lastQ(PH.il.r5, PH.q).v, saleP: B.lastQ(PH.il.r4, PH.q).v, oldLoan: 5e5, oldPay: 0, cash: 15e4, months: 6, bridgeRate: null }, pr));
  t('PHP bsell bridge = JS', php.bsell.indexOf('הלוואת גישור של כ־' + B.n0(s5.bridge) + ' ₪') > 0, B.n0(s5.bridge));
  t('PHP: no unfilled placeholder anywhere', !/\{[a-z_.0-9]+\}/.test(Object.values(php).filter(v => typeof v === 'string').join('')));
  t('PHP bplan: a row per status', (php.bplan.match(/<tr><td>/g) || []).length === 12);
  [100000, 300000, 500000, 1000000].forEach(E => t('PHP bladder max price = JS for ' + E, php.bladder.indexOf('<td>' + B.n0(E) + ' ₪</td><td>' + B.n0(B.maxPrice(E, o1).P) + ' ₪</td>') >= 0));
  const P4 = B.lastQ(PH.il.r4, PH.q).v, need4 = P4 * 0.25 + B.tax(P4, 'single', PT) + P4 * CO.lawyer.from / 100 * (1 + CO.vat);
  t('PHP bequity need = JS', php.bequity.indexOf(B.n0(need4) + ' ₪ מכספו') > 0, B.n0(need4));
  const s4 = B.stress({ price: P4, paidPct: 0.1, months: 30, share: 0.5, g: CB.g, ltv: 0.75, rate: rr.rate, years: 25, appr: 1 });
  t('PHP bequity handover cash = JS', php.bequity.indexOf('עוד ' + B.n0(s4.cash) + ' ₪ מכספכם') > 0, B.n0(s4.cash));
  t('PHP FAQ parser: questions and multi-paragraph answers of that section only', php.faq.length === 2 && php.faq[1].acceptedAnswer.text === 'ת2עוד');
  t('PHP: no unfilled placeholder', !/\{[a-z_.]+\}/.test(php.bplan));
  /* Phase 3 */
  t('PHP: fifteen summaries, each with its marker', ['bplan', 'bequity', 'bladder', 'boffer', 'bsell', 'bdates', 'bcompare', 'bvisit', 'bwho', 'bhelp', 'bpay', 'bsign', 'bkeys', 'breg', 'bmemo'].every(i => php[i] && php[i].indexOf('data-bhub-sum="' + i + '"') > 0));
  t('PHP bpay: the five payments with their protections, the advance rule with its source, the 30 and 60 days', (php.bpay.match(/<li>/g) || []).length === 5 && (php.bpay.match(/מה מגן עליכם:/g) || []).length === 4 && php.bpay.indexOf('7.5% מהמחיר') > 0 && php.bpay.indexOf('סעיף 15') > 0 && php.bpay.indexOf('בתוך 30 יום') > 0 && php.bpay.indexOf('בתוך 60 יום') > 0);
  t('PHP bsign: the three lists in full (12 items), the dates filled', (php.bsign.match(/<li>/g) || []).length === 12 && php.bsign.indexOf('בתוך 30 יום') > 0);
  t('PHP bkeys: the five transfers, an empty how or src is not printed', (php.bkeys.match(/<li>/g) || []).length === 5 && !/: <\/li>|\(מקור: \)/.test(php.bkeys));
  t('PHP breg: the steps table, 10 rows with column labels', (php.breg.match(/<tr><td data-l=/g) || []).length === 10);
  t('PHP bmemo: the six questions and the dated section 8', (php.bmemo.match(/<li>/g) || []).length === 6 && php.bmemo.indexOf('סעיף 8') > 0 && php.bmemo.indexOf('9.11.2026') > 0);
}

if (process.argv.includes('--facts')) {
  const P4 = B.lastQ(PH.il.r4, PH.q).v, l4 = B.lastQ(PH.il.r4, PH.q);
  console.log(JSON.stringify({ il4: l4, P4, tax4: B.tax(P4, 'single', PT), law4: P4 * CO.lawyer.from / 100 * (1 + CO.vat), need4: P4 * 0.25 + B.tax(P4, 'single', PT) + P4 * CO.lawyer.from / 100 * (1 + CO.vat), pay4: B.pmt(P4 * 0.75, rr.rate, 25), rate: rr,
    ladder: [100000, 300000, 500000, 1000000].map(E => { const x = B.maxPrice(E, o1), Ld = B.ladder(PH, x.P); return [E, x.P, Ld.filter(c => c.f3).length, Ld.filter(c => c.f4).length, Ld.filter(c => c.f5).length, Ld.filter(c => c.f4).map(c => c.n).slice(0, 6).join('/')]; }),
    stress: B.stress({ price: P4, paidPct: 0.1, months: 30, share: 0.5, g: CB.g, ltv: 0.75, rate: rr.rate, years: 25, appr: 1 }), cb: CB, pti: BM.market.pti_avg, ptim: BM.market.month }, null, 1));
}
console.log(fail.length ? 'FAILED ' + fail.length + ':\n  ' + fail.join('\n  ') + '\n' + n + ' passed' : n + ' passed');
process.exit(fail.length ? 1 : 0);
