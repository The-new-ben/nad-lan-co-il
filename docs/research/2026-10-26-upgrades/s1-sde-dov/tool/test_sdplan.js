// S1 moat "sdplan" (node test_sdplan.js): independent checks of data/sdplan.json against the official raw facts (s1-facts.json,
// built from the Israel Land Authority tender files), and of tools sdplan.js on a stand-in engine (the real fmt and esc of core.js).
//  1. Totals from the RMI tender files (s1-facts.json) recomputed here: won plot files, units won, open tenders, no-bid plots,
//     and each plot's tender fields equal the file.
//  2. The stage ladder is consistent: s>=1 needs a won tender or a later official record, s>=2 a design plan date, s>=3 a permit
//     request, s>=4 a permit, s=5 works or a "בבניה" record; no request is older than the plot's own plan deposit.
//  3. Every plot and every list combination computes without error; every visible string (answer, lines, note, table, svg text,
//     aria labels, share text) has no long dash and none of the banned words; svg text is 12px or more; line values are short.
//  4. Privacy: a plot record carries only whitelisted keys (no permit holder names); winners are companies from the tender files.
//  5. sdplan.json stays under 120 KB.
const fs = require('fs'), path = require('path'), vm = require('vm');
const H = __dirname, REPO = path.join(H, '..', '..', '..', '..', '..');
const D = JSON.parse(fs.readFileSync(path.join(H, '..', 'data', 'sdplan.json'), 'utf8'));
const FX = JSON.parse(fs.readFileSync(path.join(H, '..', 'data', 's1-facts.json'), 'utf8'));
let bad = 0; const ok = (name, cond, extra) => { if (!cond) bad++; console.log((cond ? 'OK  ' : 'BAD ') + name + (extra ? ': ' + extra : '')); };

// 1. tender totals, recomputed from the raw tender records
const won = FX.tenders.filter(t => t.st === 'won'), open = FX.tenders.filter(t => t.st === 'open'), nob = FX.tenders.filter(t => t.st === 'nobid');
const unitsWon = won.reduce((s, t) => s + t.units, 0);
ok('34 plot files won in the tender records', won.length === 34, won.length);
ok('9,316 units won', unitsWon === 9316, unitsWon);
ok('8 open plot files, 2 with no bids', open.length === 8 && nob.length === 2, open.length + '/' + nob.length);
let mism = 0;
for (const t of won) for (const pid of t.plots) {
  const r = D.plots.find(p => p.id === pid);
  if (!r || !r.t || r.t.tender !== t.tender || r.t.units !== t.units || r.t.bid !== t.bid || r.t.dev !== t.dev || r.t.bids !== t.bids) { mism++; console.log('   mismatch', pid, t.tender); }
  else if (t.units && r.t.perUnit !== Math.round((t.bid + t.dev) / t.units / 1000) * 1000) { mism++; console.log('   perUnit', pid); }
}
ok('every won plot carries its tender exactly', mism === 0, mism + ' mismatches');

// 2. the stage ladder
let lad = 0;
for (const r of D.plots) {
  const why = [];
  if (r.s >= 2 && !(r.design || r.req || r.permit || r.works)) why.push('s>=2 without a record');
  if (r.s >= 3 && !r.req) why.push('s>=3 without a request');
  if (r.s >= 4 && !(r.permit || r.works)) why.push('s>=4 without a permit');
  if (r.s === 5 && !(r.works || r.permit)) why.push('s=5 without works');
  if (r.s === 1 && !r.t) why.push('s=1 without a tender');
  const plan = { eshkol: FX.plans['תמ"ל3001'], merkaz: FX.plans['1/4444'], tzafon: FX.plans['2/4444'] }[r.c];
  if (r.req && plan && plan.deposited && r.req.open < plan.deposited) why.push('request before the plan deposit');
  if (why.length) { lad++; console.log('   ladder', r.id, why.join('; ')); }
}
ok('the stage ladder holds on every plot', lad === 0, lad + ' problems');
const by = D.stages.map((s, i) => D.plots.filter(r => r.s === i).length);
console.log('   stages:', D.stages.map((s, i) => s + ' ' + by[i]).join(' | '));

// 4. privacy: whitelisted keys only
const KEYS = new Set(['id', 'c', 'use', 'yeud', 'area', 's', 'st', 'sea', 'xy', 'poly', 't', 'open', 'nobid', 'design', 'req', 'permit', 'works', 'p', 'price']);
const extra = D.plots.flatMap(r => Object.keys(r).filter(k => !KEYS.has(k)));
ok('plot records carry only whitelisted keys', extra.length === 0, extra.join(','));
const winners = new Set(won.map(t => t.winner));
ok('every winner shown is a winner in the tender records', D.plots.every(r => !r.t || winners.has(r.t.winner)));

// 3. the tool on a stand-in engine (fmt and esc as in core.js)
let spec = null;
const LOC = 'he-IL', nf0 = new Intl.NumberFormat(LOC, { maximumFractionDigits: 0 });
const fmt = { num: (n, d) => new Intl.NumberFormat(LOC, { minimumFractionDigits: d || 0, maximumFractionDigits: d || 0 }).format(n || 0), ils: n => '₪' + nf0.format(Math.round(n || 0)) };
const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const win = { NadLanInstruments: { register: (id, s) => { spec = s; }, fmt, esc } };
const docStub = { addEventListener: () => {} };
const ctx = vm.createContext({ window: win, document: docStub, Intl, Math, Date, JSON, console, Event: function () {} });
vm.runInContext(fs.readFileSync(path.join(H, 'sdplan.js'), 'utf8'), ctx);
ok('the tool registered', !!spec);
const data = { sdplan: D };
const BANNED = /ממשק|מערכת|פלטפורמ|סימולצי|אינטראקטיב|בקרוב|בבדיקה|טעון אימות|מודל|מנגנון|שכב|הדגמה|טכנולוגי|יחסית|כמעט|אטלס|Atlas|פיילוט|פרוטוטייפ|רספונסיבי|מובייל|זיהום|מזוהמ|PFAS|תלת ממד|לחיצ/;
const visible = r => {
  const parts = [r.answer.label, r.answer.value, r.answer.sub || '', r.note || '', r.formula || '', r.text || ''];
  (r.lines || []).forEach(l => parts.push(l.label, l.value));
  if (r.table) { parts.push(r.table.title); r.table.head.forEach(h => parts.push(h)); r.table.rows.forEach(row => row.forEach(c => parts.push(String(c)))); }
  const svg = r.figure || '';
  (svg.match(/<text\b[^>]*>([^<]*)<\/text>/g) || []).forEach(t => parts.push(t.replace(/<[^>]+>/g, '')));
  (svg.match(/aria-label="([^"]*)"/g) || []).forEach(a => parts.push(a));
  return parts.join(' ').replace(/<[^>]+>/g, ' ');
};
let n = 0, errs = 0, dash = 0, ban = 0, small = 0, longv = 0;
const check = (v, tag) => {
  n++; const r = spec.compute(Object.assign(spec.defaults(), v), data);
  if (r.error) { errs++; console.log('   error', tag, r.error.msg); return; }
  const t = visible(r);
  if (/[–—]/.test(t)) { dash++; console.log('   long dash', tag); }
  const m = t.match(BANNED); if (m) { ban++; console.log('   banned word', tag, m[0], t.slice(Math.max(0, m.index - 30), m.index + 30)); }
  const sz = (r.figure.match(/font-size:([\d.]+)px/g) || []).map(s => parseFloat(s.slice(10)));
  if (sz.some(x => x < 12)) { small++; console.log('   small svg text', tag); }
  (r.lines || []).forEach(l => { if (String(l.value).length > 40) { longv++; console.log('   long line value', tag, l.value); } });
  return r;
};
D.plots.forEach(r => check({ view: 'plot', plot: r.id }, 'plot ' + r.id));
for (const c of ['all', 'eshkol', 'merkaz', 'tzafon']) for (const use of ['all', 'sale', 'rent', 'special', 'biz']) for (const sort of ['stage', 'bids', 'land', 'station', 'sea']) check({ view: 'list', c, use, sort }, [c, use, sort].join('/'));
spec.presets(data).forEach(p => check(Object.assign({}, p.set), 'preset ' + p.key));
ok('every plot, list and preset computes', errs === 0, n + ' runs, ' + errs + ' errors');
ok('no long dash in any visible string', dash === 0, dash);
ok('no banned word in any visible string', ban === 0, ban);
ok('svg text is 12px or more', small === 0, small);
ok('line values stay short', longv === 0, longv);

// known answers
const R = id => spec.compute(Object.assign(spec.defaults(), { view: 'plot', plot: id }), data);
const r111 = R('111');
ok('plot 111 (Rainbow): under construction, tender 62/2021 with 11 bids', r111.answer.value === 'בבנייה' && /62\/2021/.test(r111.answer.sub) && /11 הצעות/.test(r111.answer.sub), r111.answer.value + ' | ' + r111.answer.sub);
const r3204 = R('3204');
ok('plot 3204: open tender until 7.12.2026', r3204.lines.some(l => /מכרז פתוח 272\/2024/.test(l.label) && /7\.12\.2026/.test(l.value)));
const r2101 = R('2101');
ok('plot 2101: the tender with no bids is said', r2101.lines.some(l => l.value === 'לא הוגשו הצעות'));
const r2270 = R('2270');
ok('plot 2270 (FIRST): the reported price links to /sde-dov/prices/', /\/sde-dov\/prices\//.test(r2270.note) && r2270.lines.some(l => /המחיר שדווח/.test(l.label)));
const all = spec.compute(spec.defaults(), data);
ok('the district list: 73 plots, 9,316 units, 8 under construction', /73/.test(all.answer.value) && /9,316/.test(all.answer.sub) && /8 בבנייה/.test(all.answer.sub), all.answer.value + ' | ' + all.answer.sub);
const pu = D.plots.filter(r => r.p).map(r => r.p.u);
ok('project links are our project pages', pu.every(u => /^\/projects\/[a-z0-9-]+\/$/.test(u)), [...new Set(pu)].join(' '));

// 5. size
const size = fs.statSync(path.join(H, '..', 'data', 'sdplan.json')).size;
ok('sdplan.json under 120 KB', size < 120000, size + ' bytes');
console.log(bad ? 'FAILED ' + bad : 'ALL OK');
process.exit(bad ? 1 : 0);
