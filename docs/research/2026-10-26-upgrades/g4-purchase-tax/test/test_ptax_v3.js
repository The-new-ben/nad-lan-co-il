// G4 (26.10.2026): ptax v3 against ptax v2 as it is live (test/ptax-v2-live.js, md5 df1cac4bd98864312c97866bfe5a1100, fetched
// from nad-lan.co.il 26.10.2026), plus the new rules worked by hand from the Tax Authority's 2026 buyer guide and instructions
// 1/2026 and 2/2026.
//   node docs/research/2026-10-26-upgrades/g4-purchase-tax/test/test_ptax_v3.js
// Part 1: every v2 case (a grid of prices x tracks x options x shares x dates) must give the same answer, label, sub-line, bracket
// table, scenarios and formula, every v2 line (label and value) must still be there, and every v2 note must still be inside the note.
// Part 2: the v3 functions and cases.
const fs = require('fs'), path = require('path'), vm = require('vm');
const REPO = path.join(__dirname, '..', '..', '..', '..', '..');
const A = path.join(REPO, 'plugins', 'nadlan-config', 'assets', 'instruments');
const DATA = { ptax: JSON.parse(fs.readFileSync(path.join(A, 'data', 'ptax.json'), 'utf8')) };
const OLDDATA = { ptax: JSON.parse(fs.readFileSync(path.join(__dirname, 'ptax-live.json'), 'utf8')) };

function load(toolFile) {
  const doc = { documentElement: { getAttribute: () => 'he' }, readyState: 'complete', querySelectorAll: () => [], addEventListener() {}, getElementById: () => null, createElement: () => ({}), head: { appendChild() {} } };
  const win = {};
  const ctx = vm.createContext({ window: win, document: doc, Intl, Math, Date, JSON, console, btoa: (s) => Buffer.from(s, 'binary').toString('base64'), atob: (s) => Buffer.from(s, 'base64').toString('binary') });
  vm.runInContext(fs.readFileSync(path.join(A, 'core.js'), 'utf8'), ctx);
  let spec = null; win.NadLanInstruments.register = (id, s) => { if (id === 'ptax') spec = s; };
  vm.runInContext(fs.readFileSync(toolFile, 'utf8'), ctx);
  return { spec, NLPT: win.NLPT };
}
const OLD = load(path.join(__dirname, 'ptax-v2-live.js'));
const NEW = load(path.join(A, 'tools', 'ptax.js'));
let bad = 0, n = 0;
const fail = (msg) => { bad++; if (bad <= 25) console.log('BAD ' + msg); };

// ------------------------------------------------------------------ part 1: v2 cases unchanged
const prices = [100000, 500000, 1500000, 1978745, 1978746, 2000000, 2347040, 2400000, 2500000, 2500001, 3000000, 3500000, 4000000, 6055070, 6100000, 10000000, 18000000, 20183565, 20183566, 25000000, 100000000];
const shares = [100, 50, 33.3];
const dates = ['2023-01-01', '2023-06-01', '2024-09-01', '2025-04-30', '2025-06-01', '2026-02-28', '2026-10-26', '2027-03-01'];
const cases = [];
for (const price of prices) for (const share of shares) {
  cases.push({ track: 'single', upg: 'no' });
  for (const bdate of dates) { cases.push({ track: 'single', upg: 'yes', contractor: 'no', bdate }); for (const pdate of ['', '2025-12-31', '2027-06-30']) cases.push({ track: 'single', upg: 'yes', contractor: 'yes', bdate, pdate }); }
  for (const bdate of ['2026-10-26', '2027-02-10', '2027-02-11']) { cases.push({ track: 'extra', bdate }); cases.push({ track: 'foreign', bdate }); }
  cases.push({ track: 'oleh', oleh12: 'no' }, { track: 'oleh', oleh12: 'yes' });
  cases.push({ track: 'disabled', disSingle: 'yes' }, { track: 'disabled', disSingle: 'no' });
  cases.push({ track: 'land', permit: 'no' }, { track: 'land', permit: 'yes' });
  cases.push({ track: 'gift', giftExtra: 'no' }, { track: 'gift', giftExtra: 'yes' });
  for (const c of cases.splice(0)) cases2(Object.assign({ price, share }, c));
}
function base(spec) { const v = spec.defaults(); v.bdate = '2026-10-26'; return v; }
function cases2(c) {
  const vo = Object.assign(base(OLD.spec), c), vn = Object.assign(base(NEW.spec), c);
  const ro = OLD.spec.compute(vo, OLDDATA), rn = NEW.spec.compute(vn, DATA);
  n++;
  const tag = JSON.stringify(c);
  if (ro.error || rn.error) { if (JSON.stringify(ro.error) !== JSON.stringify(rn.error)) fail('error differs ' + tag); return; }
  for (const k of ['label', 'value', 'sub', 'tone']) if (ro.answer[k] !== rn.answer[k]) fail('answer.' + k + ' ' + tag + ': ' + ro.answer[k] + ' -> ' + rn.answer[k]);
  if (JSON.stringify(ro.table) !== JSON.stringify(rn.table)) fail('table ' + tag);
  if (JSON.stringify(ro.scenarios) !== JSON.stringify(rn.scenarios)) fail('scenarios ' + tag);
  if (ro.formula !== rn.formula) fail('formula ' + tag);
  for (const l of ro.lines) if (!rn.lines.some((x) => x.label === l.label && x.value === l.value)) fail('line missing ' + tag + ': ' + l.label + ' = ' + l.value);
  for (const seg of ro.note.split('<br>')) if (rn.note.indexOf(seg) < 0) fail('note missing ' + tag + ': ' + seg.slice(0, 60));
  if (ro.breakdown.map((b) => Math.round(b.value)).join() !== rn.breakdown.map((b) => Math.round(b.value)).join()) fail('breakdown values ' + tag);
}
console.log((bad ? 'BAD ' : 'OK  ') + 'part 1: ' + n + ' v2 cases, answer/table/scenarios/formula/lines/notes unchanged (' + bad + ' differences)');
const bad1 = bad;

// ------------------------------------------------------------------ part 2: the v3 rules, by hand
const P = DATA.ptax, X = NEW.NLPT;
const is = (name, got, want) => { const ok = JSON.stringify(got) === JSON.stringify(want); if (!ok) bad++; console.log((ok ? 'OK  ' : 'BAD ') + name + ': ' + JSON.stringify(got) + (ok ? '' : ' (want ' + JSON.stringify(want) + ')')); };
const eq = (name, got, want, tol) => { const ok = Math.abs(got - want) <= (tol == null ? 0.5 : tol); if (!ok) bad++; console.log((ok ? 'OK  ' : 'BAD ') + name + ': ' + (+got).toFixed(2) + ' (want ' + want + ')'); };
const line = (r, label) => { const l = r.lines.find((x) => x.label.indexOf(label) === 0); return l ? l.value : null; };
const run = (c) => NEW.spec.compute(Object.assign(base(NEW.spec), c), DATA);

// brackets (instruction 1/2026), the same figures test_tools.js checks
eq('3M only home', X.tax(3e6, P.tracks.single).tax, 45538.3, 0.1);
eq('3M additional home', X.tax(3e6, P.tracks.extra).tax, 240000, 0.1);
eq('3M oleh 12A: 0.5% x (3,000,000 - 1,978,745)', X.tax(3e6, P.tracks.oleh).tax, 5106.275, 0.01);
eq('10M only home', X.tax(1e7, P.tracks.single).tax, 513886.3, 0.1);

// the official examples of instruction 2/2026 (the sell-by date, unchanged from v2)
is('sell-by: bought 1.9.2024 -> 31.8.2026', X.sellBy(P, '2024-09-01', false, '').date, '2026-08-31');
is('sell-by: bought 30.4.2025 -> 31.1.2027', X.sellBy(P, '2025-04-30', false, '').date, '2027-01-31');
is('sell-by: bought 1.6.2025 -> 1.9.2027', X.sellBy(P, '2025-06-01', false, '').date, '2027-09-01');
is('sell-by: contractor bought 1.6.2024, received 31.12.2025 -> 31.3.2027', X.sellBy(P, '2024-06-01', true, '2025-12-31').date, '2027-03-31');
is('sell-by: bought 26.10.2026 (after the war period) -> 24 months, no extension', [X.sellBy(P, '2026-10-26', false, '').date, X.sellBy(P, '2026-10-26', false, '').ext], ['2028-10-26', false]);

// payment (guide pp. 11, 58: s.73 30 days, s.90a 60 days, s.51 deferral, never before 60 days)
is('declaration and payment of a deal on 26.10.2026', X.payDue(P, '2026-10-26', ''), { declare: '2026-11-25', pay: '2026-12-25', deferred: false });
is('deferred under s.51 to 30.6.2027 (possession and over half the price come later)', X.payDue(P, '2026-10-26', '2027-06-30'), { declare: '2026-11-25', pay: '2027-06-30', deferred: true });
is('an earlier event does not bring the payment before 60 days', X.payDue(P, '2026-10-26', '2026-11-01').pay, '2026-12-25');
eq('late fine: 4 weeks on 45,538.3 at 0.2% a week (s.94b)', X.lateFine(P, 45538.3, 4), 364.31, 0.01);
eq('late fine: 13 weeks on 240,000', X.lateFine(P, 240000, 13), 6240, 0.01);

// becoming a resident within 2 years (s.9(c1)(c4)(b)) and the war extension (instruction 2/2026 2.1.1.3: bought 1.3.24 -> 31.8.26)
is('resident by: bought 1.3.2024 -> 31.8.2026 (the instruction example)', X.resBy(P, '2024-03-01'), { date: '2026-08-31', ext: true });
is('resident by: bought 26.10.2026 -> 26.10.2028', X.resBy(P, '2026-10-26'), { date: '2028-10-26', ext: false });

// the oleh window (instruction 1/2026 s.2c) and regulation 12 for those who arrived before 15.8.2024
is('aliyah 1.3.2025, deal 26.10.2026', X.olehWin(P, '2025-03-01', '2026-10-26'), { from: '2024-03-01', to: '2032-03-01', inside: true, reg12: false });
is('aliyah 10.1.2024, deal 1.2.2031 (after 7 years)', X.olehWin(P, '2024-01-10', '2031-02-01'), { from: '2023-01-10', to: '2031-01-10', inside: false, reg12: true });
is('aliyah 14.8.2024 = before 15.8.2024', X.olehWin(P, '2024-08-14', '2026-10-26').reg12, true);
is('aliyah 15.8.2024 = regulation 12A only', X.olehWin(P, '2024-08-15', '2026-10-26').reg12, false);

// compute: the new cases
let r = run({ price: 3000000, track: 'single', share: 50, partner: 'extra' });
is('partners 50/50, you only home: your tax (45,538.3 / 2)', r.answer.value, '₪22,769');
is('partners: the second buyer (additional home, 8% x 3M / 2)', line(r, 'הקונה השני'), '₪120,000');
is('partners: together', line(r, 'המס של שני הקונים יחד'), '₪142,769');
r = run({ price: 3000000, track: 'foreign', becomeRes: 'yes', bdate: '2026-10-26' });
is('foreign buyer who becomes a resident within 2 years = only-home brackets', r.answer.value, '₪45,538');
is('foreign: resident by', line(r, 'להפוך לתושבי ישראל עד'), '26.10.2028');
r = run({ price: 4000000, track: 'oleh', oleh12: 'no', aliyah: '2023-05-01', bdate: '2026-10-26' });
is('oleh 12A, 4M: 0.5% x 2,021,255', r.answer.value, '₪10,106');
is('oleh arrived before 15.8.2024: regulation 12 alternative (0.5% x 1,988,090 + 5% x 2,011,910)', line(r, 'לפי תקנה 12 הייתם משלמים'), '₪110,536');
r = run({ price: 4000000, track: 'oleh', oleh12: 'yes', aliyah: '2025-01-01', bdate: '2026-10-26' });
is('regulation 12 chosen by an oleh of 2025: not open, 12A applies', r.answer.value, '₪10,106');
r = run({ price: 4000000, track: 'oleh', oleh12: 'no', aliyah: '2015-01-01', bdate: '2026-10-26' });
is('oleh outside the window (aliyah 2015): only-home brackets', r.answer.value, '₪95,538');
r = run({ price: 3000000, track: 'single', late: 4, bdate: '2026-10-26' });
is('payment date in the readout', line(r, 'תשלום המס עד'), '25.12.2026');
is('declaration date in the readout', line(r, 'הצהרה לרשות המסים עד'), '25.11.2026');
is('every week late', line(r, 'כל שבוע של איחור'), '₪91');
is('4 weeks late', line(r, 'קנס על 4 שבועות'), '₪364');
is('next bracket from 3M (8% from 6,055,070)', [line(r, 'המרחק עד המדרגה הבאה'), r.lines.find((x) => x.label.indexOf('המרחק') === 0).label], ['₪3,055,070', 'המרחק עד המדרגה הבאה (8%)']);
is('another 100,000 at 3M costs 5%', line(r, 'עוד ₪100,000'), '₪5,000');
r = run({ price: 1900000, track: 'single', bdate: '2026-10-26' });
is('no tax: no payment line, the declaration is still due', [line(r, 'תשלום המס עד'), line(r, 'הצהרה לרשות המסים עד')], [null, '25.11.2026']);
is('1.9M: 78,745 to the 3.5% bracket', [line(r, 'המרחק עד המדרגה הבאה'), r.lines.find((x) => x.label.indexOf('המרחק') === 0).label], ['₪78,745', 'המרחק עד המדרגה הבאה (3.5%)']);
r = run({ price: 3000000, track: 'single', pdefer: 'yes', pdue: '2027-06-30', bdate: '2026-10-26' });
is('deferred payment in the readout', line(r, 'תשלום המס עד'), '30.6.2027 (נדחה)');
is('the timeline is drawn', /nlpt-tl/.test(r.figure) && (r.figure.match(/<li/g) || []).length, 3);
r = run({ price: 3000000, track: 'gift', giftExtra: 'no', bdate: '2026-10-26' });
is('gift: a third of 45,538.3', r.answer.value, '₪15,179');
is('gift: inheritance is not a sale', /ירושה ומעבר דירה אגב גירושין אינם מכירה/.test(r.note), true);
r = run({ price: 3000000, track: 'single', late: -1 });
is('negative weeks = an error on the field', r.error && r.error.field, 'late');
r = run({ price: 3000000, track: 'single', late: '' });
is('an empty weeks field = paid on time', !r.error && line(r, 'קנס על') === null, true);

// the shared link
const st = Object.assign(base(NEW.spec), { price: 3500000, track: 'single', upg: 'yes', bdate: '2026-10-26', share: 50, partner: 'extra' });
const code = X.enc(st), back = X.dec(code);
is('link round trip', [back.price, back.track, back.upg, back.bdate, back.share, back.partner], [3500000, 'single', 'yes', '2026-10-26', 50, 'extra']);
is('link is URL safe', /^[A-Za-z0-9_\-]+$/.test(code), true);
is('a hostile link is ignored', X.dec('PHNjcmlwdD4'), null);
is('a link value with markup is dropped', X.dec(Buffer.from(JSON.stringify({ track: '<img src=x>', price: 1 })).toString('base64')), { price: 1 });
r = run({ price: 3000000, track: 'single' });
is('the shared text carries the link', /#ptax=[A-Za-z0-9_\-]+$/.test(r.text) && r.bare === true, true);

console.log(bad ? 'FAILED: ' + bad + ' (part 1: ' + bad1 + ')' : 'ALL CHECKS PASS');
process.exit(bad ? 1 : 0);
