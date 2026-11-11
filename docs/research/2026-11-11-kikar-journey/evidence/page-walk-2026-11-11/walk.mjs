// Walk the whole live page as a visitor: scroll through (lazy content), then capture clips. GETs only.
import { spawn } from 'node:child_process'; import fs from 'node:fs/promises'; import os from 'node:os'; import path from 'node:path';
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe'; const OUT = process.argv[2]; const W = +(process.argv[3] || 390), H = +(process.argv[4] || 844); const URL_ = process.argv[5]; const MOB = W < 900;
const PORT = 9300 + Math.floor(Math.random() * 400); const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const dir = await fs.mkdtemp(path.join(os.tmpdir(), 'wk-')); const ch = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${dir}`, '--no-first-run', '--hide-scrollbars', '--enable-unsafe-swiftshader', 'about:blank'], { stdio: 'ignore' });
for (let i = 0; i < 80; i++) { try { await (await fetch(`http://127.0.0.1:${PORT}/json/version`)).json(); break; } catch { await sleep(250); } }
await fs.mkdir(OUT, { recursive: true }); const errs = [], bad = [];
const t = await (await fetch(`http://127.0.0.1:${PORT}/json/new?about:blank`, { method: 'PUT' })).json();
const ws = new WebSocket(t.webSocketDebuggerUrl); let id = 0; const P = new Map(); await new Promise((r) => (ws.onopen = r));
const send = (m, p = {}) => new Promise((ok, no) => { const i = ++id; P.set(i, { ok, no }); ws.send(JSON.stringify({ id: i, method: m, params: p })); });
ws.onmessage = (e) => { const m = JSON.parse(e.data);
  if (m.id && P.has(m.id)) { const q = P.get(m.id); P.delete(m.id); if (m.error) q.no(new Error(JSON.stringify(m.error))); else q.ok(m.result); return; }
  if (m.method === 'Runtime.exceptionThrown') errs.push(JSON.stringify(m.params.exceptionDetails).slice(0, 300));
  if (m.method === 'Network.responseReceived' && m.params.response.status >= 400 && !/favicon|google|facebook|hotjar|doubleclick/.test(m.params.response.url)) bad.push(m.params.response.status + ' ' + m.params.response.url.slice(-90)); };
await send('Page.enable'); await send('Runtime.enable'); await send('Network.enable');
await send('Emulation.setDeviceMetricsOverride', { width: W, height: H, deviceScaleFactor: 1, mobile: MOB }); if (MOB) await send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
await send('Page.navigate', { url: URL_ });
const ev = async (x) => { const r = await send('Runtime.evaluate', { expression: x, awaitPromise: true, returnByValue: true }); return r.exceptionDetails ? 'EXC ' + JSON.stringify(r.exceptionDetails).slice(0, 260) : r.result.value; };
await sleep(9000);
let total = await ev('document.documentElement.scrollHeight');
for (let y = 0; y < total; y += H) { await ev(`scrollTo(0,${y})`); await sleep(450); total = await ev('document.documentElement.scrollHeight'); }
await sleep(1500); await ev("(function(){var st=document.createElement('style'); st.textContent='.nlpa,.nlpa-wrap,[class^=nlpa]{display:none!important}'; document.head.appendChild(st); return 1})()"); await sleep(800); total = await ev('document.documentElement.scrollHeight'); console.log('height', total, 'screens', (total / H).toFixed(1));
const CL = +(process.argv[6] || 1688); let n = 0;
for (let y = 0; y < total; y += CL) { await ev(`scrollTo(0,${y})`); await sleep(700); const s = await send('Page.captureScreenshot', { format: 'jpeg', quality: 70, captureBeyondViewport: true, clip: { x: 0, y, width: W, height: Math.min(CL, total - y), scale: 1 } }); await fs.writeFile(path.join(OUT, 'c' + String(n++).padStart(3, '0') + '.jpg'), Buffer.from(s.data, 'base64')); }
console.log(await ev("JSON.stringify([...document.querySelectorAll('h1,h2,video')].map(function(e){var r=e.getBoundingClientRect();return [Math.round(r.top+scrollY), e.tagName, r.width|0, r.height|0, e.tagName==='VIDEO'? ((e.querySelector('source')||{}).src||'').split('/').pop() : e.textContent.trim().replace(/\s+/g,' ').slice(0,60)].join(' | ')}))"));
console.log('errors', errs.length, errs.slice(0, 4)); console.log('http>=400', bad.length, bad.slice(0, 6));
ws.close(); ch.kill(); await sleep(300); await fs.rm(dir, { recursive: true, force: true }).catch(() => {});
