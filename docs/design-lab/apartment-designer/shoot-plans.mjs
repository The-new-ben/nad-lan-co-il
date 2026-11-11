// node shoot-plans.mjs [--port=47961] [plan-id ...]
// Opens every plan of plans/index.json in plans-harness.html (headless Chrome over CDP, the same way check-module.mjs does)
// and saves what the designer draws: plans-evidence/<id>.png (the plan view, 2x) and <id>-full.png (plan and 3D together).
// Serve the repo root first:  python -m http.server 47961 --bind 127.0.0.1
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const arg = (k, d) => { const a = process.argv.find((x) => x.startsWith('--' + k + '=')); return a ? a.split('=')[1] : d; };
const only = process.argv.slice(2).filter((x) => !x.startsWith('--'));
const BASE = 'http://127.0.0.1:' + arg('port', '47961') + '/docs/design-lab/apartment-designer/plans-harness.html';
const here = path.dirname(fileURLToPath(import.meta.url)), out = path.join(here, 'plans-evidence');
const index = JSON.parse(fs.readFileSync(path.resolve(here, '../../../plugins/nadlan-config/assets/designer/plans/index.json'), 'utf8'));
fs.mkdirSync(out, { recursive: true });
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe', PORT = 9300 + Math.floor(Math.random() * 500), profile = path.join(os.tmpdir(), 'nd-plans-' + PORT);
const chrome = spawn(CHROME, ['--headless=new', '--remote-debugging-port=' + PORT, '--user-data-dir=' + profile, '--no-first-run', '--disable-extensions', '--ignore-gpu-blocklist', '--enable-gpu', '--use-angle=d3d11', '--lang=he-IL'], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
for (let i = 0; i < 80; i++) { try { if ((await fetch('http://127.0.0.1:' + PORT + '/json/version')).ok) break; } catch {} await sleep(250); }
let fails = 0;
try {
  for (const p of index.plans) {
    if (only.length && !only.includes(p.id)) continue;
    const t = await (await fetch('http://127.0.0.1:' + PORT + '/json/new?about:blank', { method: 'PUT' })).json();
    const ws = new WebSocket(t.webSocketDebuggerUrl); let id = 0; const pend = new Map(), errors = [];
    ws.onmessage = (ev) => { const m = JSON.parse(ev.data); if (m.id && pend.has(m.id)) { pend.get(m.id)(m.result || m.error); pend.delete(m.id); } else if (m.method === 'Runtime.exceptionThrown') errors.push(m.params.exceptionDetails.text + ' ' + ((m.params.exceptionDetails.exception || {}).description || '')); else if (m.method === 'Runtime.consoleAPICalled' && m.params.type === 'error') errors.push(m.params.args.map((a) => a.value || a.description).join(' ')); };
    await new Promise((r) => (ws.onopen = r));
    const send = (method, params = {}) => new Promise((res) => { const i = ++id; pend.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); });
    const ev = async (e) => { const r = await send('Runtime.evaluate', { expression: e, awaitPromise: true, returnByValue: true }); if (r.exceptionDetails) throw new Error(JSON.stringify(r.exceptionDetails.exception || r.exceptionDetails.text)); return r.result.value; };
    await send('Page.enable'); await send('Runtime.enable');
    await send('Emulation.setDeviceMetricsOverride', { width: 1600, height: 1000, deviceScaleFactor: 2, mobile: false });
    await send('Page.navigate', { url: BASE + '?plan=' + encodeURIComponent(p.file) + '&t=' + Date.now() });
    let ok = false;
    for (let i = 0; i < 160; i++) { if (await ev('!!window.__ready').catch(() => false)) { ok = true; break; } await sleep(250); }
    await sleep(2500); // furniture models stream in after the first 3D frame
    const r = await ev('(()=>{const s=document.getElementById("d").shadowRoot.querySelector(".nd-plan").getBoundingClientRect();return {x:s.left,y:s.top,w:s.width,h:s.height,id:window.__d.store.apt.id}})()');
    const shot = async (name, clip) => { const d = await send('Page.captureScreenshot', { format: 'png', ...(clip ? { clip: { ...clip, scale: 1 } } : {}) }); fs.writeFileSync(path.join(out, name + '.png'), Buffer.from(d.data, 'base64')); };
    await shot(p.id, { x: r.x, y: r.y, width: r.w, height: r.h });
    await shot(p.id + '-full');
    const good = ok && r.id === p.id && errors.length === 0;
    if (!good) fails++;
    console.log((good ? 'ok   ' : 'FAIL ') + p.id + (r.id !== p.id ? ' (loaded ' + r.id + ')' : '') + (errors.length ? '  errors: ' + errors.join(' | ') : ''));
    ws.close(); await fetch('http://127.0.0.1:' + PORT + '/json/close/' + t.id).catch(() => {});
  }
} catch (e) { console.error(e); fails++; }
chrome.kill(); await sleep(300); try { fs.rmSync(profile, { recursive: true, force: true }); } catch {}
process.exit(fails ? 1 : 0);
