// Small headless-Chrome helper for package 2 checks (HAD-792). Real GPU (ANGLE d3d11), touch on phone sizes.
//   const b = await browser(); const p = await b.page({ w, h, dpr, mobile, url, lang }); await p.shot(file); await b.close();
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

export const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';

export async function browser(opts = {}) {
  const PORT = 9300 + Math.floor(Math.random() * 600), profile = path.join(os.tmpdir(), 'nd-pkg2-' + PORT);
  const chrome = spawn(CHROME, ['--headless=new', '--remote-debugging-port=' + PORT, '--user-data-dir=' + profile, '--no-first-run', '--disable-extensions',
    '--ignore-gpu-blocklist', '--enable-gpu', '--use-angle=d3d11', '--lang=' + (opts.lang || 'he-IL'), '--hide-scrollbars', '--mute-audio'], { stdio: 'ignore' });
  for (let i = 0; i < 80; i++) { try { if ((await fetch('http://127.0.0.1:' + PORT + '/json/version')).ok) break; } catch {} await sleep(250); }
  async function page({ w = 390, h = 844, dpr = 2, mobile = true, url = 'about:blank', ua } = {}) {
    const t = await (await fetch('http://127.0.0.1:' + PORT + '/json/new?about:blank', { method: 'PUT' })).json();
    const ws = new WebSocket(t.webSocketDebuggerUrl); let id = 0; const pend = new Map(), errors = [], logs = [];
    ws.onmessage = (ev) => {
      const m = JSON.parse(ev.data);
      if (m.id && pend.has(m.id)) { pend.get(m.id)(m.result || m.error); pend.delete(m.id); }
      else if (m.method === 'Runtime.exceptionThrown') errors.push(m.params.exceptionDetails.text + ' ' + ((m.params.exceptionDetails.exception || {}).description || ''));
      else if (m.method === 'Runtime.consoleAPICalled') { const s = m.params.args.map((a) => a.value || a.description).join(' '); (m.params.type === 'error' ? errors : logs).push(s); }
    };
    await new Promise((r) => (ws.onopen = r));
    const send = (method, params = {}) => new Promise((res) => { const i = ++id; pend.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); });
    const ev = async (e) => { const r = await send('Runtime.evaluate', { expression: e, awaitPromise: true, returnByValue: true }); if (r.exceptionDetails) throw new Error(JSON.stringify(r.exceptionDetails.exception || r.exceptionDetails.text)); return r.result.value; };
    await send('Page.enable'); await send('Runtime.enable');
    await send('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: dpr, mobile });
    if (mobile) await send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
    if (ua) await send('Emulation.setUserAgentOverride', { userAgent: ua });
    const touch = (type, x, y) => send('Input.dispatchTouchEvent', { type, touchPoints: type === 'touchEnd' ? [] : [{ x, y, id: 1 }] });
    const mouse = (type, x, y) => send('Input.dispatchMouseEvent', { type, x, y, button: 'left', clickCount: 1 });
    const p = {
      ev, errors, logs, send,
      go: async (u) => { await send('Page.navigate', { url: u }); await sleep(400); },
      wait: async (expr, ms = 30000) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await ev(expr).catch(() => false)) return true; await sleep(200); } return false; },
      shot: async (file) => { const d = await send('Page.captureScreenshot', { format: 'png' }); fs.mkdirSync(path.dirname(file), { recursive: true }); fs.writeFileSync(file, Buffer.from(d.data, 'base64')); return file; },
      tap: async (x, y) => { if (mobile) { await touch('touchStart', x, y); await sleep(40); await touch('touchEnd'); } else { await mouse('mouseMoved', x, y); await mouse('mousePressed', x, y); await sleep(40); await mouse('mouseReleased', x, y); } await sleep(160); },
      drag: async (x0, y0, x1, y1, steps = 12) => {
        if (mobile) { await touch('touchStart', x0, y0); for (let i = 1; i <= steps; i++) { await touch('touchMove', x0 + ((x1 - x0) * i) / steps, y0 + ((y1 - y0) * i) / steps); await sleep(18); } await touch('touchEnd'); }
        else { await mouse('mousePressed', x0, y0); for (let i = 1; i <= steps; i++) { await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: x0 + ((x1 - x0) * i) / steps, y: y0 + ((y1 - y0) * i) / steps, button: 'left', buttons: 1 }); await sleep(18); } await mouse('mouseReleased', x1, y1); }
        await sleep(160);
      },
      type: async (text) => { await send('Input.insertText', { text }); },
      close: async () => { ws.close(); await fetch('http://127.0.0.1:' + PORT + '/json/close/' + t.id).catch(() => {}); },
    };
    if (url !== 'about:blank') await p.go(url);
    return p;
  }
  return {
    page,
    close: async () => { try { chrome.kill(); } catch {} await sleep(600); try { fs.rmSync(profile, { recursive: true, force: true }); } catch {} },
  };
}
