// HAD-712, the Kikar language pages (11.11.2026): walk the whole LIVE page as a visitor (walk.mjs), then check what the Hebrew round added:
// 7 figures / 18 pictures and none broken, the towers table and the "numbers that differ" table, the FAQ schema against the visible FAQ
// (word for word), the calculator's financing block (it computes, and it updates when the inputs change), script errors, failed requests.
// Saves clips of the added parts. GETs only; the calculator inputs are changed in the page, nothing is sent.
//   node lang_check.mjs <outdir> <width> <height> <url>
import { spawn } from 'node:child_process'; import fs from 'node:fs/promises'; import os from 'node:os'; import path from 'node:path';
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe'; const OUT = process.argv[2]; const W = +(process.argv[3] || 390), H = +(process.argv[4] || 844); const URL_ = process.argv[5]; const MOB = W < 900;
const PORT = 9300 + Math.floor(Math.random() * 400); const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const dir = await fs.mkdtemp(path.join(os.tmpdir(), 'lk-')); const ch = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${dir}`, '--no-first-run', '--hide-scrollbars', '--enable-unsafe-swiftshader', 'about:blank'], { stdio: 'ignore' });
for (let i = 0; i < 80; i++) { try { await (await fetch(`http://127.0.0.1:${PORT}/json/version`)).json(); break; } catch { await sleep(250); } }
await fs.mkdir(OUT, { recursive: true }); const errs = [], bad = [];
const t = await (await fetch(`http://127.0.0.1:${PORT}/json/new?about:blank`, { method: 'PUT' })).json();
const ws = new WebSocket(t.webSocketDebuggerUrl); let id = 0; const P = new Map(); await new Promise((r) => (ws.onopen = r));
const send = (m, p = {}) => new Promise((ok, no) => { const i = ++id; P.set(i, { ok, no }); ws.send(JSON.stringify({ id: i, method: m, params: p })); });
ws.onmessage = (e) => { const m = JSON.parse(e.data);
  if (m.id && P.has(m.id)) { const q = P.get(m.id); P.delete(m.id); if (m.error) q.no(new Error(JSON.stringify(m.error))); else q.ok(m.result); return; }
  if (m.method === 'Runtime.exceptionThrown') errs.push(JSON.stringify(m.params.exceptionDetails).slice(0, 300));
  if (m.method === 'Network.responseReceived' && m.params.response.status >= 400 && !/favicon|google|facebook|hotjar|doubleclick/.test(m.params.response.url)) bad.push(m.params.response.status + ' ' + m.params.response.url.slice(-90));
  if (m.method === 'Network.loadingFailed' && !m.params.canceled && !/net::ERR_ABORTED/.test(m.params.errorText)) bad.push('failed ' + m.params.errorText + ' ' + m.params.requestId); };
await send('Page.enable'); await send('Runtime.enable'); await send('Network.enable');
await send('Emulation.setDeviceMetricsOverride', { width: W, height: H, deviceScaleFactor: 1, mobile: MOB }); if (MOB) await send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
await send('Page.navigate', { url: URL_ });
const ev = async (x) => { const r = await send('Runtime.evaluate', { expression: x, awaitPromise: true, returnByValue: true }); return r.exceptionDetails ? 'EXC ' + JSON.stringify(r.exceptionDetails).slice(0, 260) : r.result.value; };
await sleep(9000);
let total = await ev('document.documentElement.scrollHeight');
for (let y = 0; y < total; y += H) { await ev(`scrollTo(0,${y})`); await sleep(450); total = await ev('document.documentElement.scrollHeight'); }
await sleep(2500); await ev("(function(){var st=document.createElement('style'); st.textContent='.nlpa,.nlpa-wrap,[class^=nlpa]{display:none!important}'; document.head.appendChild(st); return 1})()"); await sleep(800);
total = await ev('document.documentElement.scrollHeight'); console.log('height', total, 'screens', (total / H).toFixed(1));
const R = JSON.parse(await ev(`JSON.stringify((function(){
  var figs=[...document.querySelectorAll('figure.nlws-fig')], imgs=figs.flatMap(function(f){return [...f.querySelectorAll('img')]});
  var broken=imgs.filter(function(i){return !(i.complete&&i.naturalWidth>0)}).map(function(i){return i.src.split('/').pop()});
  var figw=figs.map(function(f){var r=f.getBoundingClientRect();return Math.round(r.width)+'x'+Math.round(r.height)});
  var faqLd=[...document.querySelectorAll('script[type="application/ld+json"]')].map(function(s){try{return JSON.parse(s.textContent)}catch(e){return null}}).filter(function(j){return j&&j['@type']==='FAQPage'});
  var names=faqLd.length?faqLd[0].mainEntity.map(function(q){return q.name}):[];
  var sec=document.querySelector('#nlws-faq'), vis=sec?[...sec.querySelectorAll('h3')].map(function(h){return h.textContent.trim()}):[];
  var ans=faqLd.length?faqLd[0].mainEntity.filter(function(q){var h=[...sec.querySelectorAll('h3')].find(function(x){return x.textContent.trim()===q.name});return !h||!h.nextElementSibling||h.nextElementSibling.textContent.trim()!==q.acceptedAnswer.text}).map(function(q){return q.name}):['no FAQPage'];
  var tables=[...document.querySelectorAll('.nlws table')].length;
  var calc=document.querySelector('#nlpg'), fin=calc&&calc.querySelector('[data-pg=fin]');
  var cells=[...document.querySelectorAll('.nlws table td')].filter(function(td){var r=td.getBoundingClientRect();return r.width>0&&td.scrollWidth>td.clientWidth+2}).length;
  return {figs:figs.length, imgs:imgs.length, broken:broken, figw:figw.slice(0,3), faqLd:faqLd.length, faqN:names.length, faqVis:vis.length,
    notVisible:names.filter(function(n){return vis.indexOf(n)<0}), answerMismatch:ans, tables:tables, overflowCells:cells,
    calc:!!calc, fin:!!fin, mm:!!window.NLPG_MM, docW:document.documentElement.scrollWidth};
})())`));
console.log(JSON.stringify(R));
// the calculator: read, change the purchase type and the floor, read again
const rd = "JSON.stringify(['p','tt','eq','lp','ln','mo','inc','fm'].map(function(k){var e=document.querySelector('#nlpg [data-pg='+k+']');return k+'='+(e?e.textContent.replace(/\\s+/g,' ').trim():'-')}))";
if (R.fin) {
  console.log('calc before', await ev(rd));
  console.log(await ev(`(function(){var r=document.querySelector('#nlpg input[name=nlpg-t][value=more]'); if(!r) return 'no radio'; r.click(); r.dispatchEvent(new Event('change',{bubbles:true})); return 'more clicked'})()`)); await sleep(600);
  console.log('calc more', await ev(rd));
  console.log(await ev(`(function(){var s=document.querySelector('#nlpg input[type=range]'); if(!s) return 'no range'; s.value=s.max; s.dispatchEvent(new Event('input',{bubbles:true})); s.dispatchEvent(new Event('change',{bubbles:true})); return 'range '+s.value})()`)); await sleep(600);
  console.log('calc top floor', await ev(rd));
}
// clips of the added parts
const clip = async (sel, name, idx = 0) => { const r = JSON.parse(await ev(`JSON.stringify((function(){var e=document.querySelectorAll(${JSON.stringify(sel)})[${idx}]; if(!e) return null; e.scrollIntoView({block:'start'}); var b=e.getBoundingClientRect(); return {x:0,y:Math.max(0,b.top+scrollY-12),w:${W},h:Math.min(2400,b.height+24)}})())`)); if (!r) { console.log('no', sel); return; } await sleep(900);
  const s = await send('Page.captureScreenshot', { format: 'jpeg', quality: 72, captureBeyondViewport: true, clip: { x: 0, y: r.y, width: r.w, height: r.h, scale: 1 } }); await fs.writeFile(path.join(OUT, name + '.jpg'), Buffer.from(s.data, 'base64')); };
await clip('figure.nlws-fig', 'fig-aerial', 0); await clip('figure.nlws-fig', 'fig-towers', 1); await clip('figure.nlws-fig', 'fig-dirs', 3); await clip('figure.nlws-fig', 'fig-facilities', 6);
await clip('#nlws-facts table', 'table-diff', 1); await clip('#nlws-choose table', 'table-towers', 0);
await clip('#nlpg [data-pg=fin]', 'calc-fin', 0);
console.log('errors', errs.length, errs.slice(0, 4)); console.log('http>=400 or failed', bad.length, bad.slice(0, 6));
ws.close(); ch.kill(); await sleep(300); await fs.rm(dir, { recursive: true, force: true }).catch(() => {});
