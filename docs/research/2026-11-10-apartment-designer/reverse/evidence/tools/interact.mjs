// Headless Chrome probe over CDP (node 24, no deps).
// Usage: node probe.mjs <targets.json> <outDir>
// targets.json: [{ "id": "planner5d-home", "url": "https://...", "mode": "desktop"|"mobile", "wait": 8000, "canvasWait": 0 }]
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const [,, targetsFile, outDir] = process.argv;
const targets = JSON.parse(fs.readFileSync(targetsFile, 'utf8'));
fs.mkdirSync(outDir, { recursive: true });
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const PORT = 9300 + Math.floor(Math.random() * 500);
const profile = path.join((await import('node:os')).tmpdir(), 'apt-designer-probe-profile-' + PORT); // throwaway Chrome profile outside the repo

const chrome = spawn(CHROME, [
  '--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`,
  '--no-first-run', '--no-default-browser-check', '--disable-extensions',
  '--enable-unsafe-swiftshader', '--use-angle=swiftshader', '--ignore-gpu-blocklist',
  '--window-size=1366,900', '--lang=en-US', '--disable-features=Translate'
], { stdio: 'ignore' });

const sleep = (ms) => new Promise(r => setTimeout(r, ms));
async function waitForChrome() {
  for (let i = 0; i < 60; i++) {
    try { const r = await fetch(`http://127.0.0.1:${PORT}/json/version`); if (r.ok) return r.json(); } catch {}
    await sleep(250);
  }
  throw new Error('chrome did not start');
}

function connect(wsUrl) {
  const ws = new WebSocket(wsUrl);
  let id = 0; const pending = new Map(); const listeners = [];
  ws.onmessage = (ev) => {
    const msg = JSON.parse(ev.data);
    if (msg.id && pending.has(msg.id)) { const { res, rej } = pending.get(msg.id); pending.delete(msg.id); msg.error ? rej(new Error(JSON.stringify(msg.error))) : res(msg.result); }
    else if (msg.method) listeners.forEach(fn => fn(msg));
  };
  const ready = new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });
  return {
    ready,
    send: (method, params = {}) => new Promise((res, rej) => { const i = ++id; pending.set(i, { res, rej }); ws.send(JSON.stringify({ id: i, method, params })); setTimeout(() => { if (pending.has(i)) { pending.delete(i); rej(new Error('timeout ' + method)); } }, 60000); }),
    on: (fn) => listeners.push(fn),
    close: () => ws.close()
  };
}

const INJECT = `
(() => {
  window.__probe = { ctx: [], lcp: 0, fcp: 0, cls: 0, longTasks: 0 };
  const orig = HTMLCanvasElement.prototype.getContext;
  HTMLCanvasElement.prototype.getContext = function(type, ...a) { try { window.__probe.ctx.push(type); } catch(e){} return orig.call(this, type, ...a); };
  try { new PerformanceObserver(l => { for (const e of l.getEntries()) window.__probe.lcp = e.startTime; }).observe({ type: 'largest-contentful-paint', buffered: true }); } catch(e){}
  try { new PerformanceObserver(l => { for (const e of l.getEntries()) if (e.name === 'first-contentful-paint') window.__probe.fcp = e.startTime; }).observe({ type: 'paint', buffered: true }); } catch(e){}
  try { new PerformanceObserver(l => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__probe.cls += e.value; }).observe({ type: 'layout-shift', buffered: true }); } catch(e){}
  try { new PerformanceObserver(l => { window.__probe.longTasks += l.getEntries().length; }).observe({ type: 'longtask', buffered: true }); } catch(e){}
})();`;


const UA_MOBILE = 'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36';
// steps: {do:'goto',url}, {do:'wait',ms}, {do:'click',text,exact?}, {do:'clickXY',x,y}, {do:'shot',name}, {do:'eval',expr,label}, {do:'waitCanvasChange',ms,label}, {do:'drag',from:[x,y],to:[x,y]}, {do:'key',key}
async function run(job) {
  const r = await fetch(`http://127.0.0.1:${PORT}/json/new?about:blank`, { method: 'PUT' });
  const tgt = await r.json();
  const c = connect(tgt.webSocketDebuggerUrl); await c.ready;
  const net = { bytes: 0, reqs: 0 };
  c.on((m) => { if (m.method === 'Network.loadingFinished') { net.bytes += m.params.encodedDataLength; net.reqs++; } });
  await c.send('Page.enable'); await c.send('Network.enable'); await c.send('Runtime.enable');
  await c.send('Network.setCacheDisabled', { cacheDisabled: true });
  if (job.mode === 'mobile') {
    await c.send('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 2, mobile: true });
    await c.send('Emulation.setUserAgentOverride', { userAgent: UA_MOBILE });
    await c.send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
  } else await c.send('Emulation.setDeviceMetricsOverride', { width: 1366, height: 900, deviceScaleFactor: 1, mobile: false });
  await c.send('Page.addScriptToEvaluateOnNewDocument', { source: INJECT });
  const log = []; const t0 = Date.now();
  const ev = async (expr) => { const res = await c.send('Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise: true }).catch(e => ({ result: { value: 'ERR ' + e } })); if (res.exceptionDetails) return 'EXC ' + JSON.stringify(res.exceptionDetails).slice(0, 300); return res.result ? (res.result.value !== undefined ? res.result.value : 'TYPE ' + res.result.type + ' ' + (res.result.description || '')) : res; };
  for (const s of job.steps) {
    const ts = Date.now() - t0;
    try {
      if (s.do === 'goto') { await c.send('Page.navigate', { url: s.url }); await sleep(s.ms || 8000); log.push({ ts, step: 'goto', url: s.url, kb: Math.round(net.bytes/1024), reqs: net.reqs }); }
      else if (s.do === 'wait') await sleep(s.ms);
      else if (s.do === 'click') {
        const pos = await ev(`(() => { const want = ${JSON.stringify(s.text)}.toLowerCase(); const els = [...document.querySelectorAll('button,a,[role=button],[role=tab],div,span,li,label')].filter(e => { const t = (e.innerText || e.getAttribute('aria-label') || e.title || '').trim().toLowerCase(); return ${s.exact ? 't === want' : 't.includes(want)'} && t.length < 60; }); const vis = els.map(e => [e, e.getBoundingClientRect()]).filter(([e, r]) => r.width > 0 && r.height > 0 && r.top >= 0 && r.top < innerHeight); if (!vis.length) return null; vis.sort((a, b) => (a[1].width * a[1].height) - (b[1].width * b[1].height)); const [e, r] = vis[0]; return { x: r.left + r.width / 2, y: r.top + r.height / 2, t: (e.innerText||'').trim().slice(0,40) }; })()`);
        if (pos && pos.x) { await c.send('Input.dispatchMouseEvent', { type: 'mousePressed', x: pos.x, y: pos.y, button: 'left', clickCount: 1 }); await c.send('Input.dispatchMouseEvent', { type: 'mouseReleased', x: pos.x, y: pos.y, button: 'left', clickCount: 1 }); }
        log.push({ ts, step: 'click', text: s.text, found: pos });
        await sleep(s.ms || 1500);
      }
      else if (s.do === 'clickXY') { await c.send('Input.dispatchMouseEvent', { type: 'mousePressed', x: s.x, y: s.y, button: 'left', clickCount: 1 }); await c.send('Input.dispatchMouseEvent', { type: 'mouseReleased', x: s.x, y: s.y, button: 'left', clickCount: 1 }); log.push({ ts, step: 'clickXY', x: s.x, y: s.y }); await sleep(s.ms || 1500); }
      else if (s.do === 'drag') { const [x1, y1] = s.from, [x2, y2] = s.to; await c.send('Input.dispatchMouseEvent', { type: 'mousePressed', x: x1, y: y1, button: 'left', clickCount: 1 }); for (let i = 1; i <= 10; i++) await c.send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: x1 + (x2 - x1) * i / 10, y: y1 + (y2 - y1) * i / 10, button: 'left', buttons: 1 }); await c.send('Input.dispatchMouseEvent', { type: 'mouseReleased', x: x2, y: y2, button: 'left', clickCount: 1 }); log.push({ ts, step: 'drag' }); await sleep(s.ms || 1500); }
      else if (s.do === 'key') { await c.send('Input.dispatchKeyEvent', { type: 'keyDown', key: s.key, code: s.code || s.key, windowsVirtualKeyCode: s.vk || 0 }); await sleep(s.hold || 50); await c.send('Input.dispatchKeyEvent', { type: 'keyUp', key: s.key, code: s.code || s.key, windowsVirtualKeyCode: s.vk || 0 }); log.push({ ts, step: 'key', key: s.key }); await sleep(s.ms || 500); }
      else if (s.do === 'shot') { const shot = await c.send('Page.captureScreenshot', { format: 'jpeg', quality: 70 }); fs.writeFileSync(path.join(outDir, s.name + '.jpg'), Buffer.from(shot.data, 'base64')); log.push({ ts, step: 'shot', name: s.name, kb: Math.round(net.bytes/1024), reqs: net.reqs }); }
      else if (s.do === 'eval') { const v = await ev(s.expr); log.push({ ts, step: 'eval', label: s.label, value: v }); }
      else if (s.do === 'timeUntil') { const until = Date.now() + (s.ms || 30000); let ok = false; while (Date.now() < until) { if (await ev(s.expr)) { ok = true; break; } await sleep(200); } log.push({ ts, step: 'timeUntil', label: s.label, ok, ms: Date.now() - t0 - ts }); }
    } catch (e) { log.push({ ts, step: s.do, error: String(e) }); }
  }
  c.close(); await fetch(`http://127.0.0.1:${PORT}/json/close/${tgt.id}`).catch(() => {});
  return { id: job.id, mode: job.mode, date: '2026-11-10', totalKB: Math.round(net.bytes / 1024), reqs: net.reqs, log };
}
(async () => {
  await waitForChrome();
  const results = [];
  for (const j of targets) { try { const r = await run(j); results.push(r); console.log(JSON.stringify(r)); } catch (e) { console.log(JSON.stringify({ id: j.id, error: String(e) })); } }
  fs.writeFileSync(path.join(outDir, path.basename(targetsFile).replace('.json', '') + '-results.json'), JSON.stringify(results, null, 2));
  chrome.kill(); process.exit(0);
})();
