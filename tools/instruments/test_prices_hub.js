/* HAD-681: unit checks of the math of the /apartment-prices/ tools (prices-common.js + panatomy.js), against the data files and
   against values computed here independently from the raw sources (cbs-120010.json, ptax.json, boi-mortgage.json).
     node tools/instruments/test_prices_hub.js      -> "N passed" or the failures, exit 1 on a failure */
'use strict';
const fs = require('fs'), path = require('path'), vm = require('vm');
const ROOT = path.join(__dirname, '..', '..'), INS = path.join(ROOT, 'plugins', 'nadlan-config', 'assets', 'instruments');
const J = f => JSON.parse(fs.readFileSync(path.join(INS, 'data', f), 'utf8'));
// load the browser files in a sandbox with a stub engine (no DOM is touched while loading)
const ctx = { window: {}, document: {}, Intl, Math, JSON, console };
ctx.window.NadLanInstruments = { register() {}, fmt: {}, esc: s => String(s) };
vm.createContext(ctx);
['prices-common.js', 'panatomy.js'].forEach(f => vm.runInContext(fs.readFileSync(path.join(INS, 'tools', f), 'utf8'), ctx, { filename: f }));
const P = ctx.window.NLPH, AN = P.anatomy;
const D = J('prices-hub.json'), CPI10 = J('cbs-120010.json'), PT = J('ptax.json'), CO = J('cost.json'), A = J('anatomy.json'), BM = J('boi-mortgage.json');
let n = 0; const fail = [];
const t = (name, ok, info) => { if (ok) n++; else fail.push(name + (info !== undefined ? ' | ' + JSON.stringify(info) : '')); };
const near = (a, b, e) => a != null && b != null && Math.abs(a - b) <= (e == null ? 1e-9 : e);
const H = { from: D.hpi.from, v: D.hpi.v };

/* ---- the data file ---- */
t('hub: 24 cities, 22 quarters', D.city.length === 24 && D.q.length === 22 && D.q[0] === '1-3.2021');
t('hub: every city series has 22 values', D.city.every(c => ['r3', 'r4', 'r5', 'ra'].every(k => c[k].length === 22)));
t('hub: dwelling index from 1994-01 to the latest month', D.hpi.from === '1994-01' && P.lastKey(H) === D.hpi.latest);
t('hub: CPI continuous from 1994-01', D.cpi.from === '1994-01' && P.lastKey(D.cpi) === D.cpi.latest);
t('hub: CPI from 2010 equals cbs-120010.json', Object.keys(CPI10.months).every(k => near(P.at(D.cpi, k), CPI10.months[k], 1e-3)));
t('hub: CPI chain checked against the CBS calculator (0.1%)', D.cpi.check && Math.abs(D.cpi.check.ours / D.cpi.check.cbs - 1) < 0.001, D.cpi.check);
t('hub: six districts', D.dist.length === 6 && D.dist.every(d => d.from === '2017-10'));
t('hub: every city with a page slug links /<slug>-apartment-prices/ (23 of 24)', D.city.filter(c => c.slug).length === 23);

/* ---- months and labels ---- */
t('addM across the year', P.addM('2026-11', 3) === '2027-02' && P.addM('2026-01', -1) === '2025-12' && P.addM('2026-07', -12) === '2025-07');
t('dealLabel: two months', P.dealLabel('2026-07') === 'יולי ואוגוסט 2026');
t('dealLabel: across the year', P.dealLabel('2025-12') === 'דצמבר 2025 וינואר 2026');
t('pubLabel: about the 15th of M+3', P.pubLabel('2026-07') === 'אמצע אוקטובר 2026');
t('qLabel / qShort', P.qLabel('1-3.2026') === 'ינואר עד מרץ 2026' && P.qShort('10-12.2025') === 'רבעון 4 2025');
t('qMonths', JSON.stringify(P.qMonths('4-6.2026')) === '["2026-04","2026-05","2026-06"]');

/* ---- the dwelling index: change in a year, against the previous period, real, from the peak ---- */
const x = P.hpiAt(H, D.cpi), k = x.k;
const vNow = D.hpi.v[D.hpi.v.length - 1], vYear = D.hpi.v[D.hpi.v.length - 13], vPrev = D.hpi.v[D.hpi.v.length - 2];
t('y/y = index / same month a year earlier - 1', near(x.yoy, vNow / vYear - 1), [x.yoy, vNow, vYear]);
t('m/m = index / previous month - 1', near(x.mom, vNow / vPrev - 1));
t('latest national y/y is -1.8% (CBS 2026-07)', k === '2026-07' && (100 * x.yoy).toFixed(1) === '-1.8');
// the published CBS changes (boi-mortgage.json homes.hpi: the API's own "percentYear"/"percent") against our computation
const hist = BM.homes.hpi.hist, pubLast = hist[hist.length - 1];
t('our y/y and m/m match the CBS published changes for the latest month', pubLast[0] === k && (100 * x.yoy).toFixed(1) === pubLast[3].toFixed(1) && (100 * x.mom).toFixed(1) === pubLast[2].toFixed(1), pubLast);
const agree = hist.filter(r => { const s = P.at(H, r[0]), y = P.at(H, P.addM(r[0], -12)); return s === r[1] && Math.abs(100 * (s / y - 1) - r[3]) <= 0.15; }).length;
t('the published 12-month changes agree within 0.15 points in most months (revisions aside)', agree >= hist.length - 3, agree + '/' + hist.length);
// real: deflated by the CPI of the same two deal months (their average), computed here from cbs-120010.json directly
const cAvg = m => { const a = CPI10.months[m], b = CPI10.months[P.addM(m, 1)]; return b == null ? a : (a + b) / 2; };
t('real y/y = (index ratio) / (CPI ratio of the deal months) - 1', near(x.real, (vNow / vYear) / (cAvg(k) / cAvg(P.addM(k, -12))) - 1, 1e-6), x.real);
t('real is below nominal when prices fall and inflation is positive', x.real < x.yoy);
const peakV = Math.max.apply(null, D.hpi.v.slice(-61, -1));
t('from the peak of the last 5 years', near(x.fromPeak, vNow / peakV - 1) && x.peakK === '2025-01', [x.peakK, x.fromPeak]);
t('cpiDeal falls back to one month when M+1 is not out', near(P.cpiDeal(D.cpi, D.cpi.latest), P.at(D.cpi, D.cpi.latest)));
const W1 = P.window(H, D.cpi, P.addM(k, -60), k, false), W2 = P.window(H, D.cpi, '1994-01', k, true);
t('window: rebased to 100 at its first month, 61 points over 5 years', W1.length === 61 && near(W1[0].x, 100) && near(W1[60].x / 100 - 1, vNow / P.at(H, P.addM(k, -60)) - 1, 1e-9));
t('window real since 1994 equals realChg', near(W2[W2.length - 1].x / 100 - 1, P.realChg(vNow, D.hpi.v[0], P.cpiDeal(D.cpi, k), P.cpiDeal(D.cpi, '1994-01')), 1e-9));
t('chg / realChg return null on a missing value', P.chg(1, null) === null && P.realChg(1, 2, null, 1) === null);

/* ---- the city medians ---- */
const ta = D.city.find(c => c.n === 'תל אביב יפו'), sTA = P.cityStat(ta.r4, D.q, D.cpi);
t('city: latest published quarter (Tel Aviv 4 rooms 1-3.2026)', sTA.q === '1-3.2026' && sTA.v === 5229800, sTA);
t('city: y/y against the same quarter a year earlier', near(sTA.yoy, 5229800 / ta.r4[16] - 1) && D.q[16] === '1-3.2025');
t('city: since 1-3.2021', near(sTA.since, 5229800 / ta.r4[0] - 1));
const cq = q => { const m = P.qMonths(q).map(z => CPI10.months[z]); return (m[0] + m[1] + m[2]) / 3; };
t('city: real since 2021 deflated by the quarter CPI average', near(sTA.real, (5229800 / ta.r4[0]) / (cq('1-3.2026') / cq('1-3.2021')) - 1, 1e-6));
const ks = D.city.find(c => c.n === 'כפר סבא'), sKS = P.cityStat(ks.r4, D.q, D.cpi);
t('city: falls back to the last quarter that was published (Kfar Saba 10-12.2025)', sKS.q === '10-12.2025' && sKS.v === ks.r4[19]);
const bb = D.city.find(c => c.n === 'בני ברק'), sBB = P.cityStat(bb.r4, D.q, D.cpi);
t('city: no 1-3.2021 value -> no change since 2021 (never a substitute quarter)', bb.r4[0] === null && sBB.since === null && sBB.real === null);
const gap = []; D.city.forEach(c => ['r3', 'r4', 'r5', 'ra'].forEach(r => { const s = P.cityStat(c[r], D.q, D.cpi); if (s && c[r][s.i - 4] === null) gap.push([c.n, r, s.yoy]); }));
t('city: a missing year-earlier quarter gives no y/y (' + gap.length + ' cases in the data)', gap.length > 0 && gap.every(g => g[2] === null), gap.slice(0, 3));
t('city: empty series -> null', P.cityStat([null, null], D.q, D.cpi) === null);
const nat = P.cityStat(D.il.r4, D.q, D.cpi);
t('national 4 rooms 4-6.2026 = 2,028,800', nat.q === '4-6.2026' && nat.v === 2028800);

/* ---- rent and yield: same quarter only ---- */
t('rent of the same quarter (Tel Aviv 4 rooms, 1-3.2026 -> 2026-03)', P.rentAt(ta.rent, '4', '1-3.2026') === ta.rent.r4['2026-03'] && ta.rent.r4['2026-03'] > 0);
t('rent: no value for an unpublished quarter', P.rentAt(ta.rent, '4', '1-3.2019') === null && P.rentAt({}, '4', '1-3.2026') === null);
t('gross yield = rent x 12 / price', near(P.grossYield(10000, 5229800), 120000 / 5229800) && P.grossYield(0, 1) === null);

/* ---- mortgage payment ---- */
t('effective -> nominal (Bank of Israel conversion)', near(P.ef2nom(4.62), 1200 * (Math.pow(1.0462, 1 / 12) - 1)));
t('pmt textbook: 1,000,000 at 6% nominal for 30 years = 5,995.51', near(P.pmt(1000000, 6, 360), 5995.505, 0.01));
t('pmt at 0% = P / n', near(P.pmt(1200, 0, 12), 100));
const pay = P.payment(2028800, D.mort.ltv, D.mort.eff, D.mort.years);
t('payment: 75% of the national 4-room median at the BoI average rate for 25 years', D.mort.ltv === 0.75 && D.mort.years === 25 && near(pay.loan, 1521600) && near(pay.pay, P.pmt(1521600, P.ef2nom(D.mort.eff), 300)) && Math.round(pay.pay) === 8479, pay);
t('mortgage rate is the boi-mortgage.json fixed not-linked average of its month', D.mort.eff === BM.rates.fixed_nl.rate && D.mort.month === BM.rates.fixed_nl.hist.slice(-1)[0][0]);
t('a quarter point more costs about 209 ILS a month on that loan', Math.round(P.payment(2028800, 0.75, D.mort.eff + 0.25, 25).pay - pay.pay) === 209);

/* ---- purchase tax by brackets (ptax.json), checked by hand ---- */
const S = PT.tracks.single, E = PT.tracks.extra;
t('ptax single: up to the first bracket = 0', P.ptax(1978745, S).tax === 0 && P.ptax(1500000, S).tax === 0);
t('ptax single 2,000,000 = 3.5% of 21,255', near(P.ptax(2000000, S).tax, (2000000 - 1978745) * 0.035, 1e-6));
t('ptax single 2,500,000 = 20,538.3', near(P.ptax(2500000, S).tax, (2347040 - 1978745) * 0.035 + (2500000 - 2347040) * 0.05, 1e-6) && Math.round(P.ptax(2500000, S).tax) === 20538);
t('ptax single 7,000,000 = 273,886', Math.round(P.ptax(7000000, S).tax) === 273886);
t('ptax single above the top bracket: 10%', near(P.ptax(25000000, S).tax, (2347040 - 1978745) * 0.035 + (6055070 - 2347040) * 0.05 + (20183565 - 6055070) * 0.08 + (25000000 - 20183565) * 0.1, 1e-6));
t('ptax extra home 3,200,000 = 8% = 256,000', near(P.ptax(3200000, E).tax, 256000, 1e-6));
t('ptax parts add up', near(P.ptax(7000000, S).parts.reduce((s, p) => s + p.tax, 0), P.ptax(7000000, S).tax, 1e-6) && P.ptax(7000000, S).parts.length === 4);
t('ptax national 4-room median (single) = 1,751.93', near(P.ptax(2028800, S).tax, 1751.925, 1e-6));

/* ---- the anatomy: VAT, the bar, the buyer's side, honesty of the data ---- */
t('VAT inside a price: 1,180,000 at 18% holds 180,000', near(P.vatIn(1180000, 0.18), 180000, 1e-6) && (100 * 0.18 / 1.18).toFixed(1) === '15.3');
['nat', 'center', 'periph'].forEach(a => { const b = AN.devBar(A, a, CO.vat), s = b.reduce((z, y) => z + y.w, 0); t('devBar ' + a + ': the parts are the whole price', near(s, 1, 1e-9), s); });
const bn = AN.devBar(A, 'nat', CO.vat);
t('devBar national: land 1/3, construction 1/3, VAT exact, the rest of the third without a split', near(bn[0].w, 1 / 3) && near(bn[1].w, 1 / 3) && near(bn[2].w, 0.18 / 1.18) && bn[3].sub === 'בלי חלוקה רשמית');
const bp = AN.devBar(A, 'periph', CO.vat);
t('devBar periphery: land a tenth, VAT, and one hatched part with no number', near(bp[0].w, 0.1) && bp.length === 3 && bp[2].x === true);
const B1 = AN.buyer(A, PT, { price: 2028800, track: 'single', broker: false, ltv: 75 });
t('buyer: purchase tax exact, lawyer 0.5% to 1% plus VAT, file fee capped at 360', near(B1.lines[0].lo, 1751.925, 1e-6) && near(B1.lines[1].lo, 2028800 * 0.005 * 1.18, 1e-6) && near(B1.lines[1].hi, 2028800 * 0.01 * 1.18, 1e-6) && B1.lines.find(l => l.k === 'mf').lo === 360);
t('buyer: no broker line unless asked', !B1.lines.some(l => l.k === 'brk'));
const B2 = AN.buyer(A, PT, { price: 2028800, track: 'extra', broker: true, ltv: 0 });
t('buyer: extra home 8%, broker 2% plus VAT, no file fee without a mortgage', near(B2.lines[0].lo, 2028800 * 0.08, 1e-6) && near(B2.lines.find(l => l.k === 'brk').lo, 2028800 * 0.02 * 1.18, 1e-6) && !B2.lines.some(l => l.k === 'mf'));
t('buyer: totals are the sums of the lines', near(B1.lo, B1.lines.reduce((s, l) => s + l.lo, 0)) && near(B1.hi, B1.lines.reduce((s, l) => s + l.hi, 0)));
// honesty: every number in anatomy.json has a recorded source with a url and a date; claims are flagged
const srcOk = k2 => A.src[k2] && /^https?:\/\//.test(A.src[k2].url) && A.src[k2].date && A.src[k2].read;
let numbered = 0, bad = [];
A.dev.forEach(g => { Object.keys(g.share || {}).forEach(a => { numbered++; if (!srcOk(g.share[a].src)) bad.push(g.id + '.' + a); });
  g.sub.forEach(s => { if (s.rule || s.claim || s.vat) { numbered++; if (!srcOk(s.src)) bad.push(g.id + ':' + s.he); } if (!s.rule && !s.claim && !s.vat && !s.facts && s.src) bad.push('source without a number: ' + s.he); }); });
t('anatomy: every number has a named, dated source with a URL (' + numbered + ' numbers)', !bad.length, bad);
t('anatomy: the marketing range is flagged as a claim', A.src.mkt.kind === 'claim' && A.dev.some(g => g.sub.some(s => s.claim && s.src === 'mkt')));
t('anatomy: the Bank of Israel quotes are kept verbatim', A.src.boi13.q.length === 3 && A.src.boi13.q[0].indexOf('בערך שליש ממחיר הדירה לצרכן') > -1 && A.src.boi13.q[1].indexOf('כשליש ועל כעשירית') > -1);
t('anatomy: developer margin carries no number', A.dev.find(g => g.id === 'rest').sub.find(s => s.he === 'רווח היזם') && !A.dev.find(g => g.id === 'rest').sub.find(s => s.he === 'רווח היזם').rule);
t('anatomy: facts sourced (prime, Reichman)', srcOk(A.facts.prime.src) && srcOk(A.facts.runi.src) && A.facts.prime.v === BM.policy.prime);

/* ---- the server summaries (PHP, inc/instruments.php) print the same numbers as the tools (JS) ---- */
try {
  const os = require('os'), cp = require('child_process'), tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'phub-'));
  const out = path.join(tmp, 'c.html'), ld = path.join(tmp, 'ld.json');
  cp.execFileSync('php', [path.join(__dirname, 'render_prices_page.php'), path.join(ROOT, 'docs', 'research', '2026-11-07-prices-buying', 'page-7151-new.html'), out, ld], { encoding: 'utf8' });
  const html = fs.readFileSync(out, 'utf8'), graph = JSON.parse(fs.readFileSync(ld, 'utf8'))['@graph'];
  const sum = id => { const a = html.indexOf('data-nli="' + id + '"'); return html.slice(a, html.indexOf('</section>', a)); };
  const pm = sum('pmarket'), pc = sum('pcity'), pa = sum('panatomy');
  t('PHP pmarket: the answer with the JS y/y, m/m, period and peak', pm.indexOf('ירדו ב־' + Math.abs(100 * x.yoy).toFixed(1) + '% בשנה') > -1 && pm.indexOf(P.dealLabel(k)) > -1 && pm.indexOf('ב־' + Math.abs(100 * x.mom).toFixed(1) + '%') > -1 && pm.indexOf(Math.abs(100 * x.fromPeak).toFixed(1) + '% מתחת לשיא') > -1);
  const dRows = (pm.match(/<tr>/g) || []).length;
  t('PHP pmarket: district table with the country and 6 districts and a caption', dRows === 8 && pm.indexOf('<caption>') > -1, dRows);
  t('PHP pcity: 25 rows, links to the city pages, the payment of the JS', (pc.match(/<tr>/g) || []).length === 26 && (pc.match(/-apartment-prices\//g) || []).length === 23 && pc.indexOf(Math.round(pay.pay).toLocaleString('en-US') + ' ₪ בחודש') > -1);
  t('PHP pcity: Tel Aviv row with the JS median and change', pc.indexOf('5,229,800') > -1 && pc.indexOf('+' + (100 * sTA.yoy).toFixed(1) + '%') > -1);
  t('PHP panatomy: Bank of Israel thirds, VAT 15.3%, tax on the national median', pa.indexOf('כשליש') > -1 && pa.indexOf('15.3%') > -1 && pa.indexOf(Math.round(P.ptax(2028800, S).tax).toLocaleString('en-US') + ' ₪') > -1);
  const faq = graph.find(g => g['@type'] === 'FAQPage');
  t('FAQPage from the page: 8 questions, answers with numbers', faq && faq.mainEntity.length === 8 && faq.mainEntity[0].acceptedAnswer.text.indexOf('1.8%') > -1);
  t('three SoftwareApplication nodes', graph.filter(g => g['@type'] === 'SoftwareApplication').length === 3);
  const ds = (html.match(/<script type="application\/ld\+json">(.*?)<\/script>/s) || [])[1];
  const dj = ds && JSON.parse(ds);
  t('Dataset JSON-LD parses, names the sources and the period', dj && dj['@type'] === 'Dataset' && dj.temporalCoverage === '2021-01/2026-06' && dj.isBasedOn.indexOf('https://www.nadlan.gov.il/') > -1);
  const vtxt = html.replace(/<style[\s\S]*?<\/style>/g, '').replace(/<script[\s\S]*?<\/script>/g, '');
  t('page: no long dashes, no forbidden words', !/[–—]/.test(vtxt) && !/אטלס|ממשק|דמו |אינטראקטיב|Atlas/.test(vtxt));
  const heads = (vtxt.match(/<h[1-3][^>]*>[\s\S]*?<\/h[1-3]>/g) || []).map(h => h.replace(/<[^>]+>/g, ''));
  t('page: one h1, it leads with מחירי דירות', (vtxt.match(/<h1/g) || []).length === 1 && /^מחירי דירות/.test(heads.find(h => true)), heads[0]);
  t('page: no brand name in any heading', !heads.some(h => /מדלן|יד ?2|ידאטה|madlan|yad2/i.test(h)), heads.filter(h => /מדלן|יד ?2|ידאטה/.test(h)));
} catch (e) { t('PHP render ran', false, String(e.message).slice(0, 300)); }

/* ---- copy rules on every visible string of the three tools ---- */
const vis = ['prices-common.js', 'pmarket.js', 'pcity.js', 'panatomy.js'].map(f => fs.readFileSync(path.join(INS, 'tools', f), 'utf8')).join('\n') + JSON.stringify(A);
t('no long dashes in the tools and anatomy.json', !/[–—]/.test(vis));
t('no forbidden words (אטלס, ממשק, דמו, אינטראקטיבי)', !/אטלס|ממשק|דמו |אינטראקטיב|Atlas/.test(vis));

if (fail.length) { console.log('FAILED (' + fail.length + '):\n - ' + fail.join('\n - ')); console.log(n + ' passed'); process.exit(1); }
console.log(n + ' passed');
