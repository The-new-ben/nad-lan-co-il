// Scripted page probe for nad-lan.co.il (HAD-247, 24.9.2026): real clicks and screenshots
// in a local headless Chrome over the DevTools protocol (Node 22+, no npm packages).
//
//   node tools/page_probe.mjs <steps.json>
//
// steps.json: { "outDir": "...", "width": 1440, "height": 900, "mobile": false,
//               "steps": [ {"go": "https://..."}, {"wait": 1500}, {"click": "css selector"},
//                          {"tap": "css selector"}, {"key": "ArrowRight"}, {"swipe": "css selector", "dx": -300},
//                          {"scroll": "css selector"}, {"eval": "js expression", "as": "name"},
//                          {"shot": "file.png"}, {"shotFull": "file.png"} ] }
// Prints one JSON line per eval step; screenshots go to outDir. A click is a real mouse
// press and release at the element's centre (Input.dispatchMouseEvent), a tap is a touch.
import { spawn } from 'node:child_process';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';

const CHROME = process.env.CHROME || 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const cfg = JSON.parse(await fs.readFile(process.argv[2], 'utf8'));
const PORT = 9800 + Math.floor(Math.random() * 150);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
await fs.mkdir(cfg.outDir, { recursive: true });

function cdp(wsUrl) {
  return new Promise((resolve, reject) => {
    const ws = new WebSocket(wsUrl);
    let id = 0; const pending = new Map(); const listeners = [];
    ws.onopen = () => resolve({
      send(method, params = {}) { return new Promise((res, rej) => { const i = ++id; pending.set(i, { res, rej }); ws.send(JSON.stringify({ id: i, method, params })); }); },
      on(fn) { listeners.push(fn); },
      close() { try { ws.close(); } catch (e) { /* closed */ } },
    });
    ws.onmessage = (ev) => {
      const m = JSON.parse(typeof ev.data === 'string' ? ev.data : ev.data.toString());
      if (m.id && pending.has(m.id)) { const p = pending.get(m.id); pending.delete(m.id); if (m.error) { p.rej(new Error(JSON.stringify(m.error))); } else { p.res(m.result); } } else if (m.method) { listeners.forEach((f) => f(m)); }
    };
    ws.onerror = (e) => reject(e);
  });
}

const profileDir = await fs.mkdtemp(path.join(os.tmpdir(), 'page-probe-'));
const chrome = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${profileDir}`, '--no-first-run', '--no-default-browser-check', '--disable-extensions', '--hide-scrollbars', '--enable-unsafe-swiftshader', '--use-angle=swiftshader', `--window-size=${cfg.width || 1440},${cfg.height || 900}`, 'about:blank'], { stdio: 'ignore' });
let ready = false;
for (let i = 0; i < 60 && !ready; i += 1) { try { await (await fetch(`http://127.0.0.1:${PORT}/json/version`)).json(); ready = true; } catch (e) { await sleep(250); } }
if (!ready) { console.error('chrome did not start'); chrome.kill(); process.exit(1); }

const t = await (await fetch(`http://127.0.0.1:${PORT}/json/new?about:blank`, { method: 'PUT' })).json();
const c = await cdp(t.webSocketDebuggerUrl);
const errors = [];
c.on((m) => {
  if (m.method === 'Runtime.exceptionThrown') { errors.push(m.params.exceptionDetails.exception ? m.params.exceptionDetails.exception.description : m.params.exceptionDetails.text); }
  if (m.method === 'Runtime.consoleAPICalled' && m.params.type === 'error') { errors.push('console: ' + m.params.args.map((a) => a.value || a.description || '').join(' ')); }
});
await c.send('Page.enable'); await c.send('Runtime.enable'); await c.send('Network.enable');
await c.send('Emulation.setDeviceMetricsOverride', { width: cfg.width || 1440, height: cfg.height || 900, deviceScaleFactor: cfg.dpr || 1, mobile: !!cfg.mobile });
if (cfg.mobile) {
  await c.send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
  await c.send('Network.setUserAgentOverride', { userAgent: 'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.36' });
}
if (cfg.noCache) { await c.send('Network.setCacheDisabled', { cacheDisabled: true }); }

async function evalv(expr) {
  const r = await c.send('Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise: true });
  if (r.exceptionDetails) { throw new Error('eval failed: ' + (r.exceptionDetails.exception ? r.exceptionDetails.exception.description : r.exceptionDetails.text)); }
  return r.result.value;
}
async function centre(sel) {
  const v = await evalv(`(function(){var e=document.querySelector(${JSON.stringify(sel)});if(!e){return null}e.scrollIntoView({block:"center",inline:"center"});var r=e.getBoundingClientRect();return {x:r.left+r.width/2,y:r.top+r.height/2}})()`);
  if (!v) { throw new Error('no element: ' + sel); }
  await sleep(250);
  const v2 = await evalv(`(function(){var r=document.querySelector(${JSON.stringify(sel)}).getBoundingClientRect();return {x:r.left+r.width/2,y:r.top+r.height/2}})()`);
  return v2;
}

try {
  for (const s of cfg.steps) {
    if (s.go) {
      const loaded = new Promise((r) => c.on((m) => { if (m.method === 'Page.loadEventFired') { r(); } }));
      await c.send('Page.navigate', { url: s.go });
      await Promise.race([loaded, sleep(45000)]);
      await sleep(s.settle || 1500);
    } else if (s.wait) { await sleep(s.wait);
    } else if (s.click) {
      const p = await centre(s.click);
      await c.send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: p.x, y: p.y });
      await c.send('Input.dispatchMouseEvent', { type: 'mousePressed', x: p.x, y: p.y, button: 'left', clickCount: 1 });
      await c.send('Input.dispatchMouseEvent', { type: 'mouseReleased', x: p.x, y: p.y, button: 'left', clickCount: 1 });
      await sleep(s.after || 400);
    } else if (s.tap) {
      const p = await centre(s.tap);
      await c.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: p.x, y: p.y }] });
      await c.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
      await sleep(s.after || 500);
    } else if (s.swipe) {
      const p = await centre(s.swipe); const dx = s.dx || -300; const n = 8;
      await c.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: p.x, y: p.y }] });
      for (let i = 1; i <= n; i += 1) { await c.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: p.x + (dx * i) / n, y: p.y }] }); await sleep(16); }
      await c.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
      await sleep(s.after || 900);
    } else if (s.key) {
      await c.send('Input.dispatchKeyEvent', { type: 'keyDown', key: s.key, code: s.key, windowsVirtualKeyCode: { ArrowRight: 39, ArrowLeft: 37, Escape: 27, Tab: 9, Enter: 13 }[s.key] || 0 });
      await c.send('Input.dispatchKeyEvent', { type: 'keyUp', key: s.key, code: s.key, windowsVirtualKeyCode: { ArrowRight: 39, ArrowLeft: 37, Escape: 27, Tab: 9, Enter: 13 }[s.key] || 0 });
      await sleep(s.after || 600);
    } else if (s.scroll) {
      await evalv(`(function(){var e=document.querySelector(${JSON.stringify(s.scroll)});if(e){e.scrollIntoView({block:${JSON.stringify(s.block || 'start')}});}return 1})()`);
      await sleep(s.after || 700);
    } else if (s.eval) {
      const v = await evalv(s.eval);
      console.log(JSON.stringify({ [s.as || 'eval']: v }));
    } else if (s.shot || s.shotFull) {
      const shot = await c.send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: !!s.shotFull });
      await fs.writeFile(path.join(cfg.outDir, s.shot || s.shotFull), Buffer.from(shot.data, 'base64'));
      console.log(JSON.stringify({ shot: s.shot || s.shotFull }));
    }
  }
} catch (e) {
  console.log(JSON.stringify({ error: String(e && e.message || e) }));
} finally {
  if (errors.length) { console.log(JSON.stringify({ pageErrors: errors.slice(0, 12) })); }
  c.close(); chrome.kill(); await sleep(400);
  await fs.rm(profileDir, { recursive: true, force: true }).catch(() => {});
}
