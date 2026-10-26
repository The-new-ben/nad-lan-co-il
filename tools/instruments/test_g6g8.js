// G6 G7 G8 (HAD-601 round 2, 26.10.2026): unit checks of the professionals-cluster tools on the built data.
//   node tools/instruments/test_g6g8.js      -> prints every check, exits 1 on any failure
// 1. pure logic (NLBD, NLSH, NLOD) against hand calculations of the law, the regulations and the 2026 official amounts;
// 2. every preset and a grid of inputs run through each tool's compute() with a fake engine: no error, an answer, and the
//    language law on every visible string (no long dash, no banned word, no zero amount, no "0 ימים" claims).
const fs = require('fs'), path = require('path'), vm = require('vm');
const A = path.join(__dirname, '..', '..', 'plugins', 'nadlan-config', 'assets', 'instruments');
const J = f => JSON.parse(fs.readFileSync(path.join(A, 'data', f), 'utf8'));
const BD = J('bedek.json'), SH = J('shamai.json'), OD = J('orechdin.json'), PT = J('ptax.json');
let bad = 0, n = 0;
const ok = (name, cond, extra) => { n++; if (!cond) bad++; console.log((cond ? 'OK  ' : 'BAD ') + name + (extra !== undefined ? ' -> ' + JSON.stringify(extra) : '')); };
const eq = (name, got, want, tol) => ok(name + ' = ' + JSON.stringify(want), typeof want === 'number' ? Math.abs(got - want) <= (tol || 0.01) : JSON.stringify(got) === JSON.stringify(want), got);

// ---------------------------------------------------------------- 1. pure logic
const win = {}; const ctx = vm.createContext({ window: win, Intl, Math, Date, JSON, console, encodeURIComponent });
for (const f of ['bedek', 'shamai', 'orechdin', 'warranty']) vm.runInContext(fs.readFileSync(path.join(A, 'tools', f + '.js'), 'utf8'), ctx);
const L = BD.law, B = win.NLBD, S = win.NLSH, O = win.NLOD;

// the schedule = the law = the live warranty tool
const wSrc = fs.readFileSync(path.join(A, 'tools', 'warranty.js'), 'utf8');
const wYears = [...wSrc.slice(0, wSrc.indexOf('function addY')).matchAll(/\['[^']+', (\d)\]/g)].map(m => +m[1]).sort();
eq('bedek: schedule years = warranty.js', L.items.map(x => x.y).sort(), wYears);
eq('bedek: 10 items, warranty 3, structural 20, notice 1, recurrence 2', [L.items.length, L.warranty_y, L.struct_y, L.visible_notice_y, L.recur_y], [10, 3, 20, 1, 2]);
eq('bedek: years by item', Object.fromEntries(L.items.map(x => [x.id, x.y])), { frames: 2, tiling: 2, machines: 3, yard: 3, insulation: 3, piping: 4, sealing: 4, cracks: 5, cladding: 7, other: 1 });
let r = B.defect('2023-03-15', 'sealing', '2026-10-26', L);
eq('defect: sealing handed 15.3.2023, on 26.10.2026', [r.st, r.bdekEnd, r.warEnd], ['bdek', '2027-03-15', '2030-03-15']);
eq('defect: days left in the inspection period', r.left, 140);
r = B.defect('2023-03-15', 'frames', '2026-10-26', L); eq('defect: frames (2 years) is in warranty', [r.st, r.bdekEnd, r.warEnd], ['warranty', '2025-03-15', '2028-03-15']);
r = B.defect('2023-03-15', 'other', '2026-10-26', L); eq('defect: other (1 year) is in warranty until 15.3.2027', [r.st, r.warEnd], ['warranty', '2027-03-15']);
r = B.defect('2015-01-10', 'piping', '2026-10-26', L); eq('defect: piping from 2015 is over (4+3 years)', [r.st, r.warEnd], ['over', '2022-01-10']);
r = B.defect('2015-01-10', 'struct', '2026-10-26', L); eq('defect: structure from 2015 is inside 20 years', [r.st, r.bdekEnd], ['bdek', '2035-01-10']);
r = B.defect('2004-01-10', 'struct', '2026-10-26', L); eq('defect: structure from 2004 is after 20 years', r.st, 'struct_after');
eq('dates: 29.2.2024 plus a year = 28.2.2025', B.addY('2024-02-29', 1), '2025-02-28');
eq('dates: the last day of the period is still inside', B.defect('2024-01-01', 'other', '2025-01-01', L).st, 'bdek');
eq('dates: the day after is the warranty', B.defect('2024-01-01', 'other', '2025-01-02', L).st, 'warranty');
const cal = B.calendar('2025-06-30', L, BD.book_days);
eq('calendar: 6 inspection ends + 6 warranty ends + notice + structure', cal.length, 14);
eq('calendar: first the one-year notice, then the one-year end', [cal[0].kind, cal[1].kind, cal[1].date], ['notice', 'bdek', '2026-06-30']);
eq('calendar: book 45 days before', cal[1].book, '2026-05-16');
eq('calendar: the last is the structure at 20 years', [cal[13].kind, cal[13].date], ['struct', '2045-06-30']);
eq('calendar: 7-year cladding ends 30.6.2032, warranty 30.6.2035', cal.filter(e => e.years === 7 && e.kind === 'bdek').map(e => e.date).concat(cal.filter(e => e.years === 10).map(e => e.date)), ['2032-06-30', '2035-06-30']);
let p = B.priceRows(BD.prices, 'apt', 4); eq('price: 4 rooms = Midrag 1,200-1,900, BM 1,500-2,500, HB 1,400', [p.rows.length, p.lo, p.hi], [3, 1200, 2500]);
p = B.priceRows(BD.prices, 'apt', 2); eq('price: 2 rooms', [p.rows.length, p.lo, p.hi], [3, 1100, 1900]);
p = B.priceRows(BD.prices, 'apt', 6); eq('price: 6 rooms (Midrag is up to 120 m2, out)', [p.rows.length, p.lo, p.hi], [2, 1600, 3500]);
p = B.priceRows(BD.prices, 'house', 0); eq('price: private house', [p.rows.length, p.lo, p.hi], [3, 1947, 6000]);
p = B.priceRows(BD.prices, 'court', 0); eq('price: court report', [p.lo, p.hi], [2500, 10000]);
let s = B.shared(BD.shared, 24, BD.vat); eq('shared property, 24 apartments: 4,320 + VAT', [s.net, Math.round(s.gross)], [4320, 5098]);
s = B.shared(BD.shared, 10, BD.vat); eq('shared property, 10 apartments: the minimum 3,000', s.net, 3000);
eq('bedek: VAT flags (Midrag incl, others not stated)', BD.prices.map(x => x.src + ':' + x.vat), ['MT:incl', 'PL:incl', 'BM:ns', 'HB:ns']);

// shamai
let d = S.decisiveFee(800000, SH.decisive); eq('decisive: 800,000 = 3% of 500k + 2% of 300k', [d.fee, d.half, d.upfront], [21000, 10500, 5250]);
d = S.decisiveFee(50000, SH.decisive); eq('decisive: 50,000 -> 1,500 by brackets, minimum 2,000', [d.raw, d.fee, d.clamped], [1500, 2000, true]);
d = S.decisiveFee(10000000, SH.decisive); eq('decisive: 10M = 15k + 10k + 10k + 40k', d.fee, 75000);
d = S.decisiveFee(30000000, SH.decisive); eq('decisive: 30M is capped at 100,000', [d.raw, d.fee], [175000, 100000]);
d = S.decisiveFee(2000000, SH.decisive); eq('decisive: exactly 2M = 35,000', d.fee, 35000);
const levy = SH.purposes.find(x => x.id === 'levy'), s197 = SH.purposes.find(x => x.id === 's197');
eq('levy: 45 days from 16.10.2026', S.deadline(levy, '2026-10-16'), '2026-11-30');
eq('section 197: 3 years from 1.3.2024', S.deadline(s197, '2024-03-01'), '2027-03-01');
eq('section 197: 29.2.2024 + 3 years', S.deadline(s197, '2024-02-29'), '2027-02-28');
let pf = S.priceFor(SH, ['house']); eq('appraiser price: private house across 3 sources', [pf.rows.length, pf.lo, pf.hi], [3, 2500, 7000]);
pf = S.priceFor(SH, ['apt']); eq('appraiser price: apartment', [pf.rows.length, pf.lo, pf.hi], [3, 2000, 5400]);
eq('register query: licence number -> exact filter', S.regQuery(' 1096 '), { filters: JSON.stringify({ 'מספר רשיון': 1096 }) });
eq('register query: two words -> prefix full text', S.regQuery('כהן  רמי'), { q: 'כהן:* & רמי:*', plain: 'false' });
eq('register query: markup and one-letter words are stripped', S.regQuery('<b>כהן</b>;--'), { q: 'כהן:*', plain: 'false' });
eq('register query: one letter -> nothing', S.regQuery('כ'), null);
eq('register: 3,182 licensed, 376 with a city, 25.10.2026', [SH.register.count, SH.register.with_city, SH.register.updated], [3182, 376, '2026-10-25']);
eq('exams: pass mark 60, final exam present', [SH.exams.pass, SH.exams.rows.some(x => x[0] === SH.exams.final)], [60, true]);
const fin = SH.exams.rows.find(x => x[0] === SH.exams.final); eq('exams: final exam 2025 = 674 sat, 322 passed', fin[2], [674, 322]);

// orechdin
let t = O.tariff(2400000, OD.tariff); eq('Bar tariff 2026: contract on 2.4M', t.fee, 27029.9, 0.5);
t = O.tariff(50000, OD.tariff); eq('Bar tariff: 50,000 -> 2% = 1,000', t.fee, 1000);
t = O.tariff(30000, OD.tariff); eq('Bar tariff: 30,000 -> the minimum 790', t.fee, 790);
t = O.tariff(4000000, OD.tariff); eq('Bar tariff: above 3,806,082 = by agreement, at least 37,761', [t.open, t.fee], [true, 37761]);
t = O.tariff(3806082, OD.tariff); ok('Bar tariff: continuous at the top (close to 37,761)', Math.abs(t.fee - 37761) < 300, t.fee);
let c = O.devCap(3200000, OD.cap); eq('developer lawyer cap: 3.2M -> 5,915 (fixed)', [c.max, c.by], [5915, 'fixed']);
c = O.devCap(1000000, OD.cap); eq('developer lawyer cap: 1M -> 0.5% = 5,000', [c.max, c.by], [5000, 'pct']);
c = O.devCap(1183000, OD.cap); eq('developer lawyer cap: the crossing 1,183,000', c.max, 5915);
c = O.devCap(4642750, OD.cap); eq('developer lawyer cap: at the ceiling still capped', [c.capped, c.max], [true, 5915]);
c = O.devCap(4642751, OD.cap); eq('developer lawyer cap: above the ceiling, no cap', c.capped, false);
eq('developer lawyer cap history 2024-2026', OD.cap.hist, [[2024, 5575.06], [2025, 5770.77], [2026, 5915]]);
let m = O.market(2400000, OD.market); eq('market: 2.4M = 12,000 to 24,000', [m.lo, m.hi], [12000, 24000]);
m = O.market(800000, OD.market); eq('market: 800k = the minimum 5,000 to 8,000', [m.lo, m.hi], [5000, 8000]);
let lf = O.landFees(OD.land, true); eq('land fees with a mortgage: 188 + 44 + 188 + 188', lf.total, 608);
lf = O.landFees(OD.land, false); eq('land fees without a mortgage: 188 + 44', lf.total, 232);
eq('land fees 2026: extract 18, deletion 127, inheritance 188', [lf.f.extract, lf.f.warn_del, lf.f.inherit], [18, 127, 188]);
const dt = O.dates('2026-10-26', PT.pay); eq('tax dates from 26.10.2026 (ptax.json: 30 and 60 days)', [dt.declare, dt.pay], ['2026-11-25', '2026-12-25']);
eq('cost.json lawyer range = 0.5% to 1% (the site calculator agrees)', J('cost.json').lawyer, { from: 0.5, to: 1 });

// ---------------------------------------------------------------- 2. compute() through a fake engine
const REG = {};
const fmt = { ils: x => '₪' + Math.round(x || 0).toLocaleString('en-US'), num: (x, k) => Number(x || 0).toLocaleString('en-US', { minimumFractionDigits: k || 0, maximumFractionDigits: k || 0 }), pct: (x, k) => (x * 100).toFixed(k == null ? 1 : k) + '%', date: s => s };
const win2 = { NadLanInstruments: { register: (id, spec) => { REG[id] = spec; }, fmt, esc: s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c])) } };
const ctx2 = vm.createContext({ window: win2, Intl, Math, Date, JSON, console, encodeURIComponent });
for (const f of ['bedek', 'shamai', 'orechdin']) vm.runInContext(fs.readFileSync(path.join(A, 'tools', f + '.js'), 'utf8'), ctx2);
const data = { bedek: { bedek: BD }, shamai: { shamai: SH }, orechdin: { orechdin: OD, ptax: PT } };
const BANNED = /ממשק|המערכת|הפלטפורמ|פלטפורמה|סימולצי|אינטראקטיב|בקרוב|בבדיקה|טעון אימות|נדל[״"]?ן חכם|Nadlan|nadlan|מודל|מנגנון|שכבה|שכבות|הדגמה|טכנולוגי|יחסית|כמעט|אטלס|Atlas|פיילוט|לחצו|לחיצה|הקליקו|[–—]/;
const visible = res => [res.answer && res.answer.label, res.answer && res.answer.value, res.answer && res.answer.sub, res.note, res.formula, res.text]
  .concat((res.lines || []).map(l => l.label + ' ' + l.value)).concat(res.table ? [res.table.title].concat(res.table.head, ...res.table.rows) : [])
  .concat(res.figure ? [res.figure.replace(/<[^>]+>/g, ' ') + ' ' + [...res.figure.matchAll(/aria-label="([^"]*)"/g)].map(x => x[1]).join(' ')] : []).filter(Boolean).join(' | ');
function runAll(id, cases) {
  const spec = REG[id]; ok(id + ': registered', !!spec);
  const D = data[id], meta = ['kicker', 'title', 'lede'].map(k => spec[k]).join(' ') + ' ' + spec.fields.map(f => f.label + ' ' + (f.help || '') + ' ' + (f.options || []).map(o => o.label).join(' ')).join(' ') + ' ' + (spec.strip ? spec.strip(D).map(x => x.label + ' ' + x.value).join(' ') : '');
  ok(id + ': labels pass the language law', !BANNED.test(meta), (meta.match(BANNED) || [])[0]);
  const pre = spec.presets ? spec.presets(D) : [];
  const all = pre.map(x => Object.assign(spec.defaults(D), x.set)).concat(cases.map(x => Object.assign(spec.defaults(D), x)));
  all.forEach((v, i) => {
    let res; try { res = spec.compute(v, D); } catch (e) { res = { error: { msg: 'THROW ' + e.message } }; }
    const txt = res.error ? '' : visible(res);
    ok(id + ' case ' + (i + 1) + ' (' + JSON.stringify(v).slice(0, 90) + ')', !res.error && res.answer && res.answer.value && !BANNED.test(txt) && !/(^|[^\d.,])0 (₪|ימים)|₪0(?![\d.,])|NaN|undefined|Infinity/.test(txt),
      res.error ? res.error.msg : (txt.match(BANNED) || txt.match(/(^|[^\d.,])0 (₪|ימים)|₪0(?![\d.,])|NaN|undefined|Infinity/) || [res.answer.value])[0]);
  });
}
const items = BD.law.items.map(x => x.id).concat(['struct']);
runAll('bedek', [].concat(
  items.map(it => ({ view: 'defect', handed: '2022-01-20', item: it, visible: 'yes', who: 'sub', asof: '2026-10-26' })),
  items.map(it => ({ view: 'defect', handed: '2012-05-01', item: it, visible: 'no', who: 'first', asof: '2026-10-26' })),
  [{ view: 'calendar', handed: '2016-02-29', asof: '2026-10-26' }, { view: 'calendar', handed: '2026-10-01', asof: '2026-10-26' }],
  [2, 3, 4, 5, 6, 8].map(k => ({ view: 'cost', ptype: 'apt', rooms: k, roof: 'yes', group: k === 5 ? 12 : 3 })),
  ['roof', 'house', 'villa', 'moist', 'court'].map(k => ({ view: 'cost', ptype: k })), [{ view: 'cost', ptype: 'shared', apts: 8 }, { view: 'cost', ptype: 'shared', apts: 60 }]));
runAll('shamai', [].concat(SH.purposes.map(x => ({ view: 'need', purpose: x.id, levy_date: '2026-10-01', plan_date: '2024-05-01' })),
  ['apt', 'apt_big', 'house', 'invest', 'shop', 'rent', 'inherit', 'plot', 'court_add', 'levy'].map(k => ({ view: 'fee', fkind: k, reduction: 200000 })),
  [10000, 500000, 999999, 2500000, 40000000].map(a => ({ view: 'fee', fkind: 'decisive', amount: a }))));
ok('shamaireg: registered as a custom tool', REG.shamaireg && typeof REG.shamaireg.custom === 'function');
runAll('orechdin', [].concat(['buy2', 'sell2', 'new', 'land', 'gift'].map(k => ({ view: 'fee', deal: k, price: 1500000, mortgage: 'yes', own: 'no' })),
  [600000, 1183000, 4642750, 4642751, 12000000].map(pr => ({ view: 'fee', deal: 'new', price: pr, own: 'yes' })),
  ['buy2', 'sell2', 'new', 'land', 'gift'].map(k => ({ view: 'steps', deal: k, sign: '2026-11-03' }))));
// errors are answered as errors (not thrown)
ok('bedek: a date before the handover is refused', !!REG.bedek.compute(Object.assign(REG.bedek.defaults(), { view: 'defect', handed: '2026-01-01', asof: '2025-01-01' }), data.bedek).error);
ok('orechdin: a price of 10 is refused', !!REG.orechdin.compute(Object.assign(REG.orechdin.defaults(), { price: 10 }), data.orechdin).error);
ok('shamai: a levy without a date is refused', !!REG.shamai.compute(Object.assign(REG.shamai.defaults(), { view: 'need', purpose: 'levy', levy_date: '' }), data.shamai).error);

console.log('\n' + (bad ? bad + ' OF ' + n + ' CHECKS FAILED' : 'ALL ' + n + ' CHECKS PASS'));
process.exit(bad ? 1 : 0);
