/* nlbudget build (7.11.2026, HAD-678) · node test of plugins/nadlan-config/assets/instruments/tools/nlbudget.js (window.NLBUDGET) and its
   data file assets/instruments/data/nlbudget.json: every figure carries its source, flag and verbatim evidence, and no number of the data
   is missing from its evidence; the calculations (the source's own example worked through, the bounds and who gives them, per apartment,
   leads only with the developer's own close rate, the budget sheet, the spread by stage), ranges that never invert or claim precision,
   the formatting (Hebrew shekel after the number), the shared text, i18n parity and the copy rules, plus a cross-check with the server
   summary (registry.php.txt through test_nlbudget_summary.php --summary).
   Run from anywhere:  node docs/research/2026-11-07-campaign-network/build/build-nlbudget/test_nlbudget.js
   Exit code 1 on any failure. */
'use strict';
var path = require('path'), fs = require('fs'), cp = require('child_process');
var HERE = __dirname, RES = path.resolve(HERE, '../..'), REPO = path.resolve(HERE, '../../../../..');
var FILE = path.join(REPO, 'plugins/nadlan-config/assets/instruments/tools/nlbudget.js');
var DFILE = path.join(REPO, 'plugins/nadlan-config/assets/instruments/data/nlbudget.json');
global.window = {};
require(FILE);
var N = window.NLBUDGET, SRC = fs.readFileSync(FILE, 'utf8'), D = JSON.parse(fs.readFileSync(DFILE, 'utf8')), F = D.figures;
var DASH = new RegExp('[' + String.fromCharCode(0x2013, 0x2014) + ']');
var fails = 0, n = 0;
function ok(cond, name, got) { n++; if (!cond) fails++; console.log((cond ? '  ok   ' : '  FAIL ') + name + (got !== undefined ? '  [' + (typeof got === 'string' ? got : JSON.stringify(got)) + ']' : '')); }
function same(a, b) { return JSON.stringify(a) === JSON.stringify(b); }
function st(ch) { var s = N.newState(D); Object.keys(ch || {}).forEach(function (k) { s[k] = ch[k]; }); return s; }
var NUMK = ['v', 'lo', 'hi', 'over', 'target', 'units', 'price', 'sales', 'mkt', 'grv', 'total', 'pct', 'brand', 'cgi', 'suite_fit', 'suite_run', 'suite_months', 'media', 'sign',
  'comm_pct', 'comm', 'combined', 'combined_pct', 'of', 'suite', 'creative', 'months', 'leads', 'deals', 'inq', 'often', 'packs', 'n_campaigns', 'angles', 'minutes', 'seconds', 'pages'];
function nums(f) {
  var o = [];
  NUMK.forEach(function (k) { var x = f[k]; if (Array.isArray(x)) o = o.concat(x); else if (typeof x === 'number') o.push(x); });
  (f.list || []).forEach(function (x) { o.push(x.v); }); (f.parts || []).forEach(function (p) { o = o.concat(p); });
  if (f.plans) Object.keys(f.plans).forEach(function (k) { o.push(f.plans[k]); });
  return o;
}
function forms(x) {
  if (x === Math.round(x)) { var s = [x.toLocaleString('en-US'), String(x)]; if (x >= 1e6) s.push(String(x / 1e6) + ' million'); return s; }
  return [String(x), x.toFixed(2)];
}
function inText(x, text) { return forms(x).some(function (fm) { return new RegExp('(?<![\\d.,])' + fm.replace(/[.$]/g, '\\$&') + '(?![\\d]|[.,]\\d)').test(text); }); }

console.log('1. the data file: every figure sourced, flagged, with verbatim evidence');
var FLAGSET = ['cited', 'price list', 'agency claim', 'agency claim, unnamed source', 'example', 'own price', 'not published'];
var ids = Object.keys(F), files = {};
function file(p) { return files[p] || (files[p] = fs.readFileSync(path.join(RES, p), 'utf8')); }
ok(D.key === 'nlbudget' && D.asof === '2026-11-07' && ids.length >= 30, 'key nlbudget, as of 7.11.2026, ' + ids.length + ' figures');
var PJ = JSON.parse(file('teardown/pages.json')), PD = {}; PJ.pages.forEach(function (p) { PD[p.id] = p; });
function dateOf(id) { var p = PD[id]; if (!p) return undefined; if (id === 'A07') return '2004'; var d = [p.published, p.modified].filter(Boolean).filter(function (x, i, a) { return a.indexOf(x) === i; }); return d.length ? d.join(' / ') : null; }
var badDate = ids.filter(function (k) { var f = F[k], want = dateOf(f.src); return want === undefined ? !f.date : f.date !== want; });
ok(!badDate.length, 'every date is the source page own published / modified date (pages.json); an undated page (the Mabatim price list) says so and shows the retrieval date', badDate);
var miss = ids.filter(function (k) { var f = F[k]; return !(f.unit && 'currency' in f && (f.scope === 'il' || f.scope === 'abroad') && f.src && f.src_he && f.src_en && 'url' in f && 'date' in f && f.retrieved === '2026-11-07' && FLAGSET.indexOf(f.flag) > -1 && f.he && f.en && Array.isArray(f.ev) && f.ev.length); });
ok(!miss.length, 'every figure: unit, currency, scope (il / abroad), source name he + en, URL field, date, retrieval date, a union.md flag, he + en words, evidence', miss);
ok(ids.filter(function (k) { return F[k].url; }).every(function (k) { return /^https:\/\//.test(F[k].url); }) && ids.filter(function (k) { return !F[k].url; }).every(function (k) { return ['own price', 'not published'].indexOf(F[k].flag) > -1; }),
  'a URL on every outside source; only NadLan\'s own price and our own checks have none');
var notVerb = []; ids.forEach(function (k) { F[k].ev.forEach(function (e) { var raw = file(e.file); if (raw.indexOf(e.value) < 0 && raw.indexOf(JSON.stringify(e.value).slice(1, -1)) < 0) notVerb.push(k + ' in ' + e.file); }); });
ok(!notVerb.length, 'every evidence string is found verbatim in its file (teardown/pages.json, competitors/services.json, teardown/union.md, PLAN.md)', notVerb);
var notIn = []; ids.forEach(function (k) { var text = F[k].ev.map(function (e) { return e.value; }).join(' || '); nums(F[k]).forEach(function (x) { if (!inText(x, text)) notIn.push(k + ':' + x); }); });
ok(!notIn.length, 'never an invented number: every number of every figure appears in its own evidence string', notIn);
var stray = []; ids.forEach(function (k) {
  var f = F[k], have = nums(f).concat(typeof f.n === 'number' ? [f.n] : []);  // n: the number of records checked (expo_np), tested against ev below
  ['he', 'en'].forEach(function (lg) {
    var tx = f[lg].replace(/\b\d{1,2}\.\d{1,2}\.\d{4}\b/g, '').replace(/\b(19|20)\d{2}\b/g, '').replace(/3D/g, '');
    (tx.match(/\d[\d,]*(\.\d+)?/g) || []).forEach(function (m) { var v = parseFloat(m.replace(/,/g, '')); if (have.indexOf(v) < 0 && have.indexOf(v * 1e6) < 0) stray.push(k + '.' + lg + ':' + m); });
  });
});
ok(!stray.length, 'the words of every figure carry no number its fields do not hold (dates aside)', stray);
ok(ids.every(function (k) { var f = F[k]; return f.lo == null || f.lo <= f.hi; }), 'every published range has lo <= hi');
var LN = D.lines.map(function (l) { return l.id; });
ok(same(LN, ['research', 'brand', 'ext3', 'plan3d', 'film', 'tour', 'photo', 'site', 'crm', 'media', 'outdoor', 'print', 'tv', 'pr', 'events', 'office', 'fee']),
  'the budget sheet: research and pricing, branding, renders (3-angle set, 3D sales plan per unit, film), tour and project page, photography, site, CRM, media, outdoor and fence, print, radio/TV, PR and SEO, events abroad, sales office and model apartment, marketing company fee', LN);
ok(D.lines.every(function (l) { return ['own', 'once', 'unit', 'pct', 'plan', 'fee'].indexOf(l.kind) > -1 && l.stage.length && l.stage.every(function (s) { return N.STAGES.concat('all').indexOf(s) > -1; })
  && (l.fig ? !!F[l.fig] : ['own', 'fee'].indexOf(l.kind) > -1) && l.ctx.every(function (c) { var p = c.split(':'); return F[p[0]] && (!p[1] || typeof F[p[0]][p[1]] === 'number'); }); }), 'every line: a known kind and stage; a priced line points to its figure; context refers to real figures');
var npLines = D.lines.filter(function (l) { return l.kind === 'own'; }).map(function (l) { return l.id; });
ok(same(npLines, ['research', 'brand', 'photo', 'site', 'crm', 'outdoor', 'print', 'tv', 'pr', 'events', 'office']), 'no Israeli price: research, branding, photography, site, CRM, outdoor, print, radio/TV, PR, events, sales office (the developer enters his own)', npLines);

console.log('\n2. the figures, against union.md');
ok(F.wedo_total.v === 1 && F.wedo_online.v === 0.75 && F.wedo_total.flag === 'agency claim' && F.wedo_total.src === 'B08a', 'about 1% of sales, 0.75% online: WE DO MEDIA, agency claim');
ok(F.sp_sm.lo === 2 && F.sp_sm.hi === 4 && F.sp_sm.flag === 'agency claim' && F.sp_sm.src === 'B06', '2% to 4% incl. sales team: Start Point, agency claim');
ok(F.sp_unit.lo === 3000 && F.sp_unit.hi === 23000 && F.sp_unit.flag === 'agency claim, unnamed source', '3,000 to 23,000 per apartment sold: claim, unnamed source');
ok(F.sp_leads.lo === 128 && F.sp_leads.hi === 173 && F.sp_leads.flag === 'price list' && F.sp_leads.vat === 'before', 'exclusive leads 128 to 173 before VAT: price list of 4.11.2026');
ok(F.se_cpl.lo === 300 && F.se_cpl.hi === 800 && F.se_cpl.flag === 'agency claim, unnamed source', 'campaign cost per lead 300 to 800: claim, unnamed source');
ok(F.lq_cpl.lo === 102.51 && F.lq_cpl.hi === 142.59 && F.lq_cpl.currency === 'USD' && F.lq_cpl.flag === 'cited' && F.lq_cpl.country === 'US', 'US search CPL $102.51 (all) to $142.59 (homes for sale): LocaliQ, cited, in dollars');
ok(F.mb_ext3.lo === 4000 && F.mb_ext3.hi === 6000 && F.mb_plan3d.lo === 1000 && F.mb_plan3d.hi === 1500 && F.mb_film.lo === 12000 && F.mb_film.hi === 30000 && ['mb_ext3', 'mb_plan3d', 'mb_film'].every(function (k) { return F[k].flag === 'price list' && F[k].src === 'R01'; }), 'renders: 3 angles 4,000-6,000; 3D sales plan 1,000-1,500 a unit; film 12,000-30,000 (Mabatim price list)');
ok(F.fe_pre.v === 530000 && F.fe_pre.of === 720000 && F.fe_ex.total === 720000 && F.fe_ex.currency === 'AUD' && F.fe_ex.flag === 'example', 'the worked example abroad: 530,000 of 720,000 before launch (Feasly, Australia, example)');
ok(same(F.nl_plans.plans, { one: 36000, three: 72000, flag: 144000 }) && F.nl_plans.flag === 'own price', 'the NadLan plans: 36,000 / 72,000 / 144,000 a year');
ok(F.gl_2025.flag === 'cited' && same(F.gl_2025.list.map(function (x) { return x.v; }), [62, 15, 30.5, 11.5, 6.5]) && F.gl_2025.list[0].approx === 'almost', 'Globes / Ifat 2025: Aura almost 62, Tidhar 15, Israel Canada 30.5, Hagag 11.5, Dimri 6.5 million (cited)');
ok(F.td_np.pages === 50 && F.td_np.flag === 'not published' && F.expo_np.n === F.expo_np.ev.length, 'the "no Israeli price" source: 50 pages read; 4 exhibitions checked, none publishes an exhibitor price');

console.log('\n3. the calculations: the source\'s own example worked through');
var s = st(), r = N.compute(s, D);
ok(s.units === 60 && s.price === 2400000 && s.months === 24 && s.comm === null && s.lpd === null && s.abroad === 0 && N.isExample(s, D), 'opens on the Semerenko example (60 x 2.4 million), a 24-month window (12 to 24, Semerenko); no commission, no close rate');
ok(r.ok && r.V === 144000000, 'sales value 144,000,000 (the source wrote "about 144 million")', r.V);
ok(r.total.lo === 2880000 && r.total.hi === 5760000 && r.total.lowFig === 'sp_sm' && r.total.highFig === 'sp_sm' && !r.total.partial, 'developer team: 2,880,000 to 5,760,000 (2% to 4%), both bounds by Start Point', [r.total.lo, r.total.hi]);
ok(r.mkt.v === 1440000 && Math.abs(r.mkt.v - F.se_ex.mkt) / F.se_ex.mkt < 0.03, 'marketing alone, 1%: 1,440,000, the source\'s "about 1.4 million"', r.mkt.v);
ok(r.total.yearLo === 1440000 && r.total.yearHi === 2880000, 'a year over 24 months: 1,440,000 to 2,880,000');
var c0 = N.compute(st({ seller: 'co' }), D), c1 = N.compute(st({ seller: 'co', comm: 1.5 }), D);
ok(c0.total.lo === 1440000 && c0.total.hi === 2880000 && c0.total.partial && c0.total.lowFig === 'wedo_total' && c0.total.highFig === 'fe_mkt', 'marketing company, no rate yet: marketing alone 1% (WE DO MEDIA) to 2% (Feasly), marked partial', [c0.total.lo, c0.total.hi]);
ok(c1.total.loPct === 2.5 && c1.total.hiPct === 3.5 && c1.total.lo === 3600000 && c1.total.hi === 5040000 && !c1.total.partial, 'with the developer\'s 1.5%: 2.5% to 3.5% = 3,600,000 to 5,040,000', [c1.total.lo, c1.total.hi]);
var fee = c1.lines.filter(function (o) { return o.id === 'fee'; })[0], fee0 = c0.lines.filter(function (o) { return o.id === 'fee'; })[0], feeD = r.lines.filter(function (o) { return o.id === 'fee'; })[0];
ok(fee.lo === 2160000 && fee.hi === 2160000 && fee0.needs && feeD.own && feeD.needs, 'the fee line: 1.5% x 144 million = 2,160,000; without a rate it asks for one; with the developer\'s team it takes his own figure');
ok(r.unit.totLo === 180000 && r.unit.totHi === 1380000 && r.unit.pctLo === 0.125 && Math.abs(r.unit.pctHi - 0.9583) < 0.001, 'advertising: 3,000 to 23,000 a unit = 180,000 to 1,380,000 for 60; 0.13% to 0.96% of the price');
ok(r.leads === null, 'no leads figure until the developer enters his own leads per deal');
var l = N.compute(st({ lpd: 48, abroad: 20 }), D).leads;
ok(l.n === 2880 && l.ab === 576 && l.il === 2304 && l.perMonth === 120, 'leads = 60 deals x 48 = 2,880; 20% abroad = 576, Israel 2,304; 120 a month');
ok(same(l.costs.map(function (x) { return [x.k, x.cur, x.n, x.lo, x.hi]; }), [['list', 'ILS', 2304, 294000, 399000], ['real', 'ILS', 2304, 691000, 1850000], ['us', 'USD', 576, 59000, 82200]]),
  'their cost: price list 294,000 to 399,000; campaigns 691,000 to 1,850,000; abroad $59,000 to $82,200 (three significant figures, outward)', l.costs.map(function (x) { return [x.lo, x.hi]; }));
var l0 = N.compute(st({ lpd: 10, abroad: 0 }), D).leads, l1 = N.compute(st({ lpd: 10, abroad: 100 }), D).leads;
ok(l0.ab === 0 && l0.costs[2].lo === 0 && l1.il === 0 && l1.costs[0].lo === 0 && l1.ab === 600, 'all in Israel: no leads abroad; all abroad: no Israeli leads');
ok(same(N.lpdExamples(D).map(function (x) { return x.lpd; }), [200, 40, 48]), 'the close-rate hint, from the sources\' examples: 200 and 40 (Semerenko), 48 (Mirai); never a default');
var L = {}; r.lines.forEach(function (o) { L[o.id] = o; });
ok(L.ext3.lo === 4000 && L.ext3.hi === 6000 && L.plan3d.lo === 60000 && L.plan3d.hi === 90000 && L.film.lo === 12000 && L.film.hi === 30000, 'sheet: renders 4,000-6,000; sales plans 1,000-1,500 x 60 = 60,000-90,000; film 12,000-30,000');
ok(L.media.approx && L.media.lo === 1080000 && L.tour.kind === 'plan' && L.tour.lo === null, 'sheet: media about 1,080,000 (0.75%); the tour line is included in the plan, not summed');
ok(r.sum.lo === 1156000 && r.sum.hi === 1206000 && r.sum.open === 12, 'total of the priced lines 1,156,000 to 1,206,000; 12 lines open (11 without an Israeli price + the sales team)', [r.sum.lo, r.sum.hi, r.sum.open]);
var so = st(); so.own.research = 50000; so.own.office = 400000; var ro = N.compute(so, D);
ok(ro.sum.lo === 1606000 && ro.sum.hi === 1656000 && ro.sum.open === 10, 'the developer\'s own figures join the total (research 50,000, sales office 400,000)');
ok(same(r.lines.filter(function (o) { return o.now; }).map(function (o) { return o.id; }), ['research', 'brand', 'ext3', 'plan3d', 'tour', 'site', 'outdoor'])
  && same(N.compute(st({ stage: 'launch' }), D).lines.filter(function (o) { return o.now; }).map(function (o) { return o.id; }), ['film', 'outdoor', 'print', 'tv', 'events', 'office'])
  && !N.compute(st({ stage: 'last' }), D).lines.some(function (o) { return o.now; }), 'the stage marks its lines (pre-launch 7, launch 6, last units none)');
ok(same(r.bars.map(function (b) { return [b.k, b.v, Math.round(b.share)]; }), [['pre', 530000, 74], ['post', 190000, 26], ['delay', 160000, 22]]) && N.barNow('pre') === 'pre' && N.barNow('build') === 'post',
  'the spread (Feasly example): 530,000 before launch (74%), 190,000 after (26%), +160,000 if the sale runs 12 more months (+22%)');

console.log('\n4. ranges: never inverted, never more precise than the anchor');
ok(N.nice(1440000, -1) === 1440000 && N.nice(2345678, -1) === 2340000 && N.nice(2345678, 1) === 2350000 && N.nice(4000, 0) === 4000 && N.nice(0, 1) === 0 && N.nice(59045.76, -1) === 59000, 'three significant figures, down for lo, up for hi');
var bad = 0, tried = 0, seed = 7; function rnd() { seed = (seed * 16807) % 2147483647; return seed / 2147483647; }
for (var i = 0; i < 800; i++) {
  var x = st({ units: 1 + Math.floor(rnd() * 3000), price: 100000 + Math.floor(rnd() * 20000) * 1000, seller: rnd() < 0.5 ? 'dev' : 'co', comm: rnd() < 0.5 ? Math.round(rnd() * 50 + 1) / 10 : null,
    abroad: Math.floor(rnd() * 101), months: 1 + Math.floor(rnd() * 120), lpd: rnd() < 0.7 ? 1 + Math.floor(rnd() * 300) : null, stage: N.STAGES[Math.floor(rnd() * 4)] });
  var y = N.compute(x, D); tried++;
  var exactLo = y.V * y.total.loPct / 100, exactHi = y.V * y.total.hiPct / 100;
  var flat = [[y.total.lo, y.total.hi], [y.unit.totLo, y.unit.totHi], [y.sum.lo, y.sum.hi]].concat(y.anchors.map(function (a) { return [a.lo, a.hi]; })).concat(y.lines.filter(function (o) { return o.lo != null; }).map(function (o) { return [o.lo, o.hi]; }))
    .concat(y.leads ? y.leads.costs.map(function (c) { return [c.lo, c.hi]; }) : []);
  if (!y.ok || flat.some(function (p) { return !(p[0] <= p[1]) || p[0] < 0; }) || y.total.lo > exactLo + 1e-6 || y.total.hi < exactHi - 1e-6 || (y.leads && y.leads.il + y.leads.ab !== y.leads.n)) bad++;
}
ok(bad === 0, 'random projects (' + tried + '): every range has lo <= hi, the rounded total holds the exact one, leads add up', bad);

console.log('\n5. inputs and validation');
ok(N.parseNum('2,400,000 ₪') === 2400000 && N.parseNum('1.5%') === 1.5 && N.parseNum('') === null && isNaN(N.parseNum('abc')) && isNaN(N.parseNum('-3')), 'typed numbers: grouping, ₪ and % read; empty is null; text or a minus sign is not a number');
ok(!N.valid('units', 0) && !N.valid('units', 10001) && !N.valid('units', 1.5) && N.valid('units', 1) && !N.valid('price', 99999) && N.valid('price', 200000000) && !N.valid('abroad', 101) && N.valid('abroad', 0)
  && !N.valid('comm', 0) && !N.valid('comm', 10.5) && N.valid('comm', 1.25) && !N.valid('comm', 1.255) && !N.valid('lpd', 0.5) && N.valid('lpd', 12.5) && !N.valid('months', 0) && N.valid('own', 0), 'limits: units 1 to 10,000; price 100,000 to 200 million; share 0 to 100; commission 0.1% to 10%; leads per deal 1 to 2,000; months 1 to 120');
ok(same(N.errors(st({ units: NaN, months: null, lpd: null })), ['units']) && same(N.errors(st({ seller: 'co', comm: 20, lpd: 0 })), ['comm', 'lpd']) && !N.compute(st({ price: null }), D).ok, 'errors name the field; optional fields may stay empty; no units or price, no budget');

console.log('\n6. formatting');
ok(N.rng(4000, 6000, 'ILS', 'he') === '4,000 עד 6,000 ₪' && N.rng(4000, 6000, 'ILS', 'en') === '₪4,000 to ₪6,000' && N.rng(2, 4, '%', 'he') === '2% עד 4%' && N.rng(102.51, 142.59, 'USD', 'he') === '$102.51 עד $142.59', 'ranges: "4,000 עד 6,000 ₪", "₪4,000 to ₪6,000", "2% עד 4%", "$102.51 עד $142.59"');
ok(N.rng(4000, 6000, 'ILS', 'he', true) === '<bdi>4,000</bdi> עד <bdi>6,000</bdi> ₪' && N.curH(1440000, 'ILS', 'he') === '<bdi>1,440,000</bdi> ₪' && N.curH(1440000, 'ILS', 'en') === '<bdi>₪1,440,000</bdi>' && N.curH(530000, 'AUD', 'he') === '<bdi>A$530,000</bdi>',
  'every figure in <bdi>; in Hebrew the shekel sign stays outside the isolate (after the number, as Hebrew reads)');
ok(N.srcText(F.sp_sm, 'he') === 'סטארט פוינט, 5.11.2026 · טענת משרד פרסום' && N.srcText(F.mb_ext3, 'en') === 'Mabatim render price list, no date, read 7.11.2026 · Published price list' && N.srcText(F.sp_leads, 'he').slice(-9) === 'לפני מע״מ', 'the source line: name, date (or "no date, read ..."), flag, and the VAT terms when the source gives them');
ok(N.flagWord(F.mi_funnel, 'en') === 'the source\'s own example' && N.flagWord(F.mi_funnel, 'he') === 'דוגמה של המקור', 'a flag inside a sentence is lower case in English');

console.log('\n7. the shared text (copy and WhatsApp)');
var s7 = st({ lpd: 48, abroad: 20 }); s7.own.research = 50000;
var th = N.summaryText(s7, D, 'he', 'https://nad-lan.co.il/marketing/'), te = N.summaryText(s7, D, 'en', 'https://nad-lan.co.il/en/marketing/');
ok(th.split('\n')[0] === 'תקציב שיווק לפרויקט, לפי נדל״ן' && te.split('\n')[0] === 'Project marketing budget, by NadLan', 'a heading line');
ok(th.indexOf('תקציב שיווק ומכירה, כל הפרויקט: 2,880,000 עד 5,760,000 ₪ (2% עד 4%: סטארט פוינט, 5.11.2026 · טענת משרד פרסום)') > -1 && te.indexOf('₪2,880,000 to ₪5,760,000 (2% to 4%: Start Point, 5.11.2026 · Agency claim)') > -1, 'the total with its bounds, source and flag');
ok(D.lines.every(function (ln) { return th.indexOf('· ' + N.lineName(ln.id, s7, 'he') + ': ') > -1 && te.indexOf('· ' + N.lineName(ln.id, s7, 'en') + ': ') > -1; }), 'every line of the sheet, in both languages');
ok(th.indexOf('הדמיות חוץ (3 זוויות): 4,000 עד 6,000 ₪ (מבטים, מחירון הדמיות, בלי תאריך, נקרא 7.11.2026 · מחירון שפורסם)') > -1 && th.indexOf('מחקר שוק, אסטרטגיה ותמחור: 50,000 ₪ (המחיר שלכם; לא פורסם מחיר ישראלי)') > -1 && te.indexOf('Market research, strategy and pricing: ₪50,000 (your price; no Israeli price published)') > -1, 'a priced line carries its source and flag; an own figure says it is the developer\'s, and the line stays "no Israeli price"');
ok(th.indexOf('פניות שצריך לקמפיין: 2,880') > -1 && th.indexOf('$59,000 עד $82,200') > -1 && th.endsWith(String.fromCharCode(10) + 'https://nad-lan.co.il/marketing/'), 'leads and their cost, the page address last');
ok(!/</.test(th + te) && !DASH.test(th + te) && th.indexOf('‏') > -1 && te.indexOf('‏') < 0, 'text only (no markup), no long dash; right-to-left marks after sources in Hebrew only');
ok(N.waUrl('א ב&') === 'https://wa.me/?text=%D7%90%20%D7%91%26', 'WhatsApp: wa.me with the text only');
ok(N.summaryText(st({ units: null }), D, 'he').split('\n')[1] === STRhe('fix'), 'no units: the text asks for them instead of a budget');
function STRhe(k) { return N.STR.he[k]; }

console.log('\n8. the words: Hebrew and English complete, copy rules');
var he = N.STR.he, en = N.STR.en, hk = Object.keys(he), ek = Object.keys(en);
var noEn = hk.filter(function (k) { return !(k in en); }), noHe = ek.filter(function (k) { return !(k in he); });
ok(!noEn.length && !noHe.length, 'every Hebrew key has an English key and back (' + hk.length + ' keys)', noEn.concat(noHe));
ok(hk.every(function (k) { return String(he[k]).trim() && String(en[k]).trim(); }), 'no empty string');
var ph = hk.filter(function (k) { var a = (he[k].match(/\{\w+\}/g) || []).sort().join(), b = (en[k].match(/\{\w+\}/g) || []).sort().join(); return a !== b; });
ok(!ph.length, 'the same {placeholders} in both languages', ph);
var need = []; LN.forEach(function (id) { need.push('ln_' + id); }); N.STAGES.concat('all').forEach(function (x) { need.push('st_' + x); }); N.SELLERS.forEach(function (x) { need.push('se_' + x); });
Object.keys(N.FLAGS).forEach(function (k) { need.push('fl_' + N.FLAGS[k]); }); ['brand', 'cgi', 'media', 'sign'].forEach(function (p) { need.push('px_' + p); }); ['list', 'real', 'us'].forEach(function (k) { need.push('l_' + k); });
ok(need.every(function (k) { return k in he && k in en; }), 'a name for every line, stage, seller, flag, example part and lead basis (' + need.length + ')', need.filter(function (k) { return !(k in he); }));
var used = hk.filter(function (k) { return SRC.indexOf("t." + k) < 0 && SRC.indexOf("'" + k + "'") < 0 && !/^(ln_|st_|se_|fl_|px_|l_|e_|b_|vat_)/.test(k); });
ok(!used.length, 'no unused string', used);
var all = hk.map(function (k) { return he[k]; }).join('\n') + '\n' + ids.map(function (k) { return F[k].he; }).join('\n'), allE = ek.map(function (k) { return en[k]; }).join('\n') + '\n' + ids.map(function (k) { return F[k].en; }).join('\n');
ok(he.f_lpd && ids.every(function (k) { return F[k].he.trim() && F[k].en.trim(); }), 'every figure has words in both languages');
ok(!DASH.test(all + allE) && !DASH.test(fs.readFileSync(DFILE, 'utf8').replace(/"ev": \[[\s\S]*?\]/g, '')), 'no long dash (– or —) in any string or in the data words');
var BAN_HE = ['ממשק', 'מערכת', 'פלטפורמ', 'אלגוריתם', 'דמו', 'סימולציה', 'הדגמה', 'מנגנון', 'אינטראקטיבי', 'טכנולוגי', 'דיגיטלי'];
var BAN_EN = ['interface', 'system', 'platform', 'algorithm', 'demo', 'simulation', 'interactive', 'technology'];
var hitH = BAN_HE.filter(function (w) { return all.indexOf(w) > -1; }), hitE = BAN_EN.filter(function (w) { return allE.toLowerCase().indexOf(w) > -1; });
ok(!hitH.length && !hitE.length && !/\bAI\b/.test(all + allE) && !/אטלס|Atlas/i.test(all + allE), 'no tech words in Hebrew or English (ממשק, מערכת, פלטפורמה, דיגיטלי, AI, דמו, סימולציה ...), no "אטלס"', hitH.concat(hitE));
var vatOk = ['vat_before', 'vat_plus']; var vatHit = hk.filter(function (k) { return /מע.?"?מ|מע״מ|VAT/i.test(he[k] + en[k]) && vatOk.indexOf(k) < 0; });
ok(!vatHit.length && ids.filter(function (k) { return /מע״מ|VAT/.test(F[k].he + F[k].en); }).every(function (k) { return F[k].vat; }), 'VAT words only where a source states its VAT terms (Start Point, the broker fee); none on NadLan\'s prices', vatHit);
ok(/לשנה/.test(he.plans) && /a year/.test(en.plans) && N.plansText(D, 'he') === 'המנויים: שוק אחד 36,000 ₪ לשנה, שלושה שווקים 72,000 ₪ לשנה, פרויקט דגל 144,000 ₪ לשנה', 'the plans line: "המנויים: שוק אחד 36,000 ₪ לשנה, ..."');
ok(he.noIl === 'לא פורסם מחיר ישראלי' && he.included === 'כלול במנוי נדל״ן' && he.honesty === 'כל טווח מגיע עם המקור שלו ותאריך. טווח שמבוסס על טענה של משרד פרסום מסומן כך.', 'the words of the brief and the design: "לא פורסם מחיר ישראלי", "כלול במנוי נדל״ן", the honesty line');
ok(!/יהוד|Jewish|religio|ethnic|דת[יו]/i.test(all + allE), 'no religion or ethnicity words');
ok(!/ranked|#1|largest spender|הכי גדול|במקום הראשון|מוביל/i.test(he.ctxHead + en.ctxHead + F.gl_2025.he + F.gl_2025.en), 'the ad-spend line makes no ranking claim (source order, not sorted)');
ok(!/[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}]/u.test(SRC), 'no emoji in the file');

console.log('\n9. the file itself');
ok(!/localStorage|sessionStorage|indexedDB|document\.cookie/.test(SRC) && !/location\.hash\s*=|history\.(push|replace)State/.test(SRC), 'no browser storage, nothing written to the address');
ok(!/fetch\(|XMLHttpRequest|sendBeacon/.test(SRC), 'sends nothing anywhere (the data file is fetched by core.js)');
var hex = (SRC.match(/#[0-9A-Fa-f]{6}\b/g) || []).map(function (h) { return h.toUpperCase(); });
var TOK = ['#2F6F86', '#1F4B5C', '#4F9A5C', '#8E7CC3', '#F2D15A', '#C42550', '#12202A', '#3E4C58', '#5E6A75', '#D3DCE2', '#F6F8F9', '#FFFFFF'];
ok(hex.every(function (h) { return TOK.indexOf(h) > -1; }), 'every colour is a NadLan Instruments token (no own hex at all)', hex);
ok(!/gradient/i.test(SRC) && (SRC.match(/box-shadow:(?!none)/g) || []).length === 0, 'no gradient, no shadow (borders only)');
var sv = SRC.match(/is-survey[^"]*" data-o="(\w+)"/g) || [];
ok(sv.length >= 1 && sv.every(function (x) { return /data-o="total"/.test(x); }) && (SRC.match(/var\(--nli-survey\)/g) || []).length === 1, 'survey red on one figure only: the total budget (one colour rule)', sv);
ok(!/Karantina/.test(SRC) && /<bdi>/.test(SRC), 'the title face comes from core.css; figures in <bdi>');
ok(/min-height:44px/.test(SRC) && !/min-height:(3\d|[12]\d)px/.test(SRC.replace(/min-height:42px !important;font-size:15px/, '')), 'controls at least 44 px (the own-price field 44 px with a 42 px input inside its border)');
ok(/NadLanInstruments\.register\('nlbudget', \{ custom:/.test(SRC) && /data\.nlbudget/.test(SRC), 'registers a custom NadLan Instruments tool and reads data.nlbudget');

console.log('\n10. the same numbers on the server (registry.php.txt)');
var php = function (lg) { return cp.spawnSync('php', [path.join(HERE, 'test_nlbudget_summary.php'), '--summary', lg], { encoding: 'utf8' }); };
var ph1 = php('he'), ph2 = php('en');
if (ph1.error || ph1.status !== 0) ok(false, 'php ran', ph1.error ? ph1.error.code : ph1.stderr);
else {
  var sh = ph1.stdout, se = ph2.stdout;
  ok(sh.indexOf(N.rng(r.total.lo, r.total.hi, 'ILS', 'he')) > -1 && se.indexOf(N.rng(r.total.lo, r.total.hi, 'ILS', 'en')) > -1, 'the server summary gives the same example total as the tool', N.rng(r.total.lo, r.total.hi, 'ILS', 'he'));
  ok(sh.indexOf(N.rng(F.sp_unit.lo, F.sp_unit.hi, 'ILS', 'he')) > -1 && sh.indexOf(N.rng(F.sp_leads.lo, F.sp_leads.hi, 'ILS', 'he')) > -1 && sh.indexOf(N.rng(F.mb_film.lo, F.mb_film.hi, 'ILS', 'he')) > -1, 'and the same per-apartment, lead and render ranges');
  ok(sh.indexOf(F.sp_sm.src_he + ', ' + he.fl_claim) > -1 && se.indexOf(F.sp_sm.src_en + ', agency claim') > -1, 'and the same source names and flags');
}

console.log('\n' + (n - fails) + ' of ' + n + ' passed' + (fails ? ', ' + fails + ' FAILED' : ''));
process.exit(fails ? 1 : 0);
