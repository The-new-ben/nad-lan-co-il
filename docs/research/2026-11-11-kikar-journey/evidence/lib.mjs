// A small headless-Chrome driver (CDP): a phone-sized visitor with touch. Read-only towards the site (GETs only).
import { spawn } from 'node:child_process'; import fs from 'node:fs/promises'; import os from 'node:os'; import path from 'node:path';
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
export const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
export async function open(url, { w = 390, h = 844, out = '.' } = {}) {
  const PORT = 9300 + Math.floor(Math.random() * 400); const MOB = w < 900;
  const dir = await fs.mkdtemp(path.join(os.tmpdir(), 'jr-'));
  const ch = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${dir}`, '--no-first-run', '--hide-scrollbars', '--enable-unsafe-swiftshader', '--use-angle=swiftshader', 'about:blank'], { stdio: 'ignore' });
  for (let i = 0; i < 80; i++) { try { await (await fetch(`http://127.0.0.1:${PORT}/json/version`)).json(); break; } catch { await sleep(250); } }
  const t = await (await fetch(`http://127.0.0.1:${PORT}/json/new?about:blank`, { method: 'PUT' })).json();
  const ws = new WebSocket(t.webSocketDebuggerUrl); let id = 0; const P = new Map(); const errs = []; const reqs = [];
  await new Promise((r) => (ws.onopen = r));
  ws.onmessage = (e) => { const m = JSON.parse(e.data); if (m.id && P.has(m.id)) { const q = P.get(m.id); P.delete(m.id); m.error ? q.no(new Error(JSON.stringify(m.error))) : q.ok(m.result); } else if (m.method === 'Runtime.exceptionThrown') errs.push(JSON.stringify(m.params.exceptionDetails).slice(0, 240)); else if (m.method === 'Network.requestWillBeSent') reqs.push(m.params.request.url); };
  const send = (m, p = {}) => new Promise((ok, no) => { const i = ++id; P.set(i, { ok, no }); ws.send(JSON.stringify({ id: i, method: m, params: p })); });
  await send('Page.enable'); await send('Runtime.enable'); await send('Network.enable');
  await send('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: MOB ? 2 : 1, mobile: MOB });
  if (MOB) await send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
  await send('Page.navigate', { url });
  const ev = async (x) => { const r = await send('Runtime.evaluate', { expression: x, awaitPromise: true, returnByValue: true }); if (r.exceptionDetails) return 'EXC ' + JSON.stringify(r.exceptionDetails).slice(0, 200); return r.result.value; };
  for (let i = 0; i < 45 && !(await ev("document.readyState==='complete'")); i++) await sleep(1000);
  await fs.mkdir(out, { recursive: true });
  const shot = async (name, wait = 900) => { await sleep(wait); const s = await send('Page.captureScreenshot', { format: 'jpeg', quality: 70 }); await fs.writeFile(path.join(out, name + '.jpg'), Buffer.from(s.data, 'base64')); return name; };
  const tap = async (x, y) => { await send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x, y }] }); await sleep(60); await send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }); };
  const drag = async (x0, y0, x1, y1, steps = 12) => { await send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: x0, y: y0 }] }); for (let i = 1; i <= steps; i++) { await send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: x0 + ((x1 - x0) * i) / steps, y: y0 + ((y1 - y0) * i) / steps }] }); await sleep(25); } await send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }); };
  const scrollTo = (sel, off = 70) => ev(`(()=>{const e=document.querySelector(${JSON.stringify(sel)}); if(!e) return 'missing'; const y=e.getBoundingClientRect().top+scrollY-${off}; scrollTo(0,y); return Math.round(y)})()`);
  const close = async () => { ws.close(); ch.kill(); await sleep(300); await fs.rm(dir, { recursive: true, force: true }).catch(() => {}); };
  return { ev, shot, tap, drag, scrollTo, send, errs, reqs, close };
}
