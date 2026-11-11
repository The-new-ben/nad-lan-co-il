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

const COLLECT = `
(() => {
  const vw = innerWidth, vh = innerHeight;
  const nav = performance.getEntriesByType('navigation')[0] || {};
  const vis = (el) => { const r = el.getBoundingClientRect(); const s = getComputedStyle(el); return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none' && r.top < vh && r.bottom > 0 && r.left < vw && r.right > 0 ? r : null; };
  const name = (el) => (el.getAttribute('aria-label') || el.innerText || el.value || el.title || (el.querySelector('img[alt]') && el.querySelector('img[alt]').alt) || '').trim().replace(/\\s+/g, ' ');
  const inter = [...document.querySelectorAll('a[href],button,[role=button],input:not([type=hidden]),select,textarea')];
  const firstVp = inter.map(el => ({ el, r: vis(el) })).filter(x => x.r);
  const small24 = firstVp.filter(x => Math.min(x.r.width, x.r.height) < 24).length;
  const small44 = firstVp.filter(x => Math.min(x.r.width, x.r.height) < 44).length;
  const ctaRe = /(start|try|get started|design|create|plan|sign up|free|begin|launch|open|התחל|עצב|נסה)/i;
  const ctas = firstVp.filter(x => ctaRe.test(name(x.el)) && name(x.el).length < 40).map(x => ({ text: name(x.el), cx: Math.round(x.r.left + x.r.width/2), cy: Math.round(x.r.top + x.r.height/2), w: Math.round(x.r.width), h: Math.round(x.r.height), area: x.r.width * x.r.height }));
  ctas.sort((a,b) => b.area - a.area);
  const unnamed = inter.filter(el => !name(el) && !el.getAttribute('aria-labelledby')).length;
  const imgs = [...document.images]; const noAlt = imgs.filter(i => !i.hasAttribute('alt')).length;
  const vpMeta = (document.querySelector('meta[name=viewport]') || {}).content || '';
  const hreflang = [...document.querySelectorAll('link[rel=alternate][hreflang]')].map(l => l.hreflang);
  const html = document.documentElement.outerHTML;
  const canvases = [...document.querySelectorAll('canvas')].map(c => { const r = c.getBoundingClientRect(); return [Math.round(r.width), Math.round(r.height)]; }).filter(a => a[0] > 0);
  const bodyText = (document.body ? document.body.innerText : '').replace(/\\s+\\n/g, '\\n');
  let firstVpText = 0; try { const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n; while ((n = walker.nextNode())) { const p = n.parentElement; if (!p) continue; const r = p.getBoundingClientRect(); if (r.top < vh && r.bottom > 0 && r.width > 0) firstVpText += n.textContent.trim().length; } } catch(e){}
  return {
    finalUrl: location.href, title: document.title, lang: document.documentElement.lang || '', dir: document.documentElement.dir || getComputedStyle(document.documentElement).direction,
    metaDesc: (document.querySelector('meta[name=description]') || {}).content || '',
    vw, vh, ttfb: Math.round(nav.responseStart || 0), dcl: Math.round(nav.domContentLoadedEventEnd || 0), load: Math.round(nav.loadEventEnd || 0),
    fcp: Math.round(window.__probe ? window.__probe.fcp : 0), lcp: Math.round(window.__probe ? window.__probe.lcp : 0), cls: window.__probe ? +window.__probe.cls.toFixed(3) : null, longTasks: window.__probe ? window.__probe.longTasks : null,
    ctxTypes: window.__probe ? [...new Set(window.__probe.ctx)] : [], canvases,
    interactiveInFirstViewport: firstVp.length, tapTargetsUnder24: small24, tapTargetsUnder44: small44, ctas: ctas.slice(0, 4).map(({area, ...c}) => c),
    unnamedControls: unnamed, imgs: imgs.length, imgsNoAlt: noAlt, viewport: vpMeta, zoomBlocked: /user-scalable\\s*=\\s*(no|0)|maximum-scale\\s*=\\s*1(\\.0)?\\b/.test(vpMeta),
    hreflang, mentionsHebrew: /עברית|hreflang=\\"he|hreflang=\\"iw|\\/he\\/|lang=\\"he/.test(html), firstViewportTextChars: firstVpText,
    h1: [...document.querySelectorAll('h1')].map(h => h.innerText.trim()).slice(0, 3),
    links: [...new Set([...document.querySelectorAll('a[href]')].map(a => a.href).filter(h => /(editor|\\/app|planner|design|start|demo|try|create|showroom|configurat|tool|live-3d|3d|floorplan|project)/i.test(h)))].slice(0, 40),
    iframes: [...document.querySelectorAll('iframe')].map(f => f.src).filter(Boolean).slice(0, 10),
    textSample: bodyText.slice(0, 2500)
  };
})()`;

const UA_MOBILE = 'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36';

async function probe(t) {
  const r = await fetch(`http://127.0.0.1:${PORT}/json/new?about:blank`, { method: 'PUT' });
  const tgt = await r.json();
  const c = connect(tgt.webSocketDebuggerUrl); await c.ready;
  const net = { bytes: 0, reqs: 0, byType: {}, failed: 0, typeOf: new Map(), hosts: new Set() };
  let loadFired = 0; const t0 = Date.now();
  c.on((m) => {
    if (m.method === 'Network.responseReceived') { net.typeOf.set(m.params.requestId, m.params.type); try { net.hosts.add(new URL(m.params.response.url).host); } catch {} }
    if (m.method === 'Network.loadingFinished') { net.bytes += m.params.encodedDataLength; net.reqs++; const ty = net.typeOf.get(m.params.requestId) || 'Other'; net.byType[ty] = (net.byType[ty] || 0) + m.params.encodedDataLength; }
    if (m.method === 'Network.loadingFailed') net.failed++;
    if (m.method === 'Page.loadEventFired' && !loadFired) loadFired = Date.now() - t0;
  });
  await c.send('Page.enable'); await c.send('Network.enable'); await c.send('Runtime.enable');
  await c.send('Network.setCacheDisabled', { cacheDisabled: true });
  if (t.mode === 'mobile') {
    await c.send('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 2, mobile: true });
    await c.send('Emulation.setUserAgentOverride', { userAgent: UA_MOBILE });
    await c.send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
  } else {
    await c.send('Emulation.setDeviceMetricsOverride', { width: 1366, height: 900, deviceScaleFactor: 1, mobile: false });
  }
  if (t.lang) await c.send('Emulation.setLocaleOverride', { locale: t.lang }).catch(() => {});
  await c.send('Page.addScriptToEvaluateOnNewDocument', { source: INJECT });
  const navStart = Date.now();
  await c.send('Page.navigate', { url: t.url }).catch(e => ({ error: String(e) }));
  // wait for load or timeout
  for (let i = 0; i < 120 && !loadFired; i++) await sleep(250);
  // optional: wait for a sizeable canvas (editor ready)
  let canvasReadyMs = null;
  if (t.canvasWait) {
    const until = Date.now() + t.canvasWait;
    while (Date.now() < until) {
      const res = await c.send('Runtime.evaluate', { expression: `[...document.querySelectorAll('canvas')].some(c => { const r = c.getBoundingClientRect(); return r.width > 300 && r.height > 200; })`, returnByValue: true }).catch(() => null);
      if (res && res.result && res.result.value) { canvasReadyMs = Date.now() - navStart; break; }
      await sleep(500);
    }
  }
  await sleep(t.wait || 6000);
  const ev = await c.send('Runtime.evaluate', { expression: COLLECT, returnByValue: true }).catch(e => ({ result: { value: { error: String(e) } } }));
  const shot = await c.send('Page.captureScreenshot', { format: 'jpeg', quality: 70 }).catch(() => null);
  const file = path.join(outDir, `${t.id}.jpg`);
  if (shot) fs.writeFileSync(file, Buffer.from(shot.data, 'base64'));
  const out = { id: t.id, url: t.url, mode: t.mode, date: '2026-11-10', loadEventMs: loadFired, canvasReadyMs, transferKB: Math.round(net.bytes / 1024), requests: net.reqs, failed: net.failed,
    byTypeKB: Object.fromEntries(Object.entries(net.byType).map(([k, v]) => [k, Math.round(v / 1024)])), hostCount: net.hosts.size, screenshot: shot ? path.basename(file) : null, ...(ev.result ? ev.result.value : {}) };
  c.close();
  await fetch(`http://127.0.0.1:${PORT}/json/close/${tgt.id}`).catch(() => {});
  return out;
}

(async () => {
  await waitForChrome();
  const results = [];
  for (const t of targets) {
    try { const r = await probe(t); results.push(r); console.log(JSON.stringify({ id: r.id, load: r.loadEventMs, kb: r.transferKB, reqs: r.requests, lcp: r.lcp, finalUrl: r.finalUrl, title: r.title, canvasReadyMs: r.canvasReadyMs, ctx: r.ctxTypes })); }
    catch (e) { results.push({ id: t.id, url: t.url, error: String(e) }); console.log(JSON.stringify({ id: t.id, error: String(e) })); }
  }
  const outFile = path.join(outDir, path.basename(targetsFile).replace('.json', '') + '-results.json');
  fs.writeFileSync(outFile, JSON.stringify(results, null, 2));
  chrome.kill();
  process.exit(0);
})();
