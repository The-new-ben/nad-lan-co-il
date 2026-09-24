// LCP / load probe for nad-lan.co.il pages (HAD-247, 24.9.2026).
// Local headless Chrome over the DevTools protocol (Node 22+ built-in WebSocket, no npm packages).
// Cold cache every run. Two profiles: desktop 1440x900, and a Lighthouse-like phone
// (390x844, 150 ms RTT, 1.6 Mbps down, CPU x4). Median of N runs per URL and profile.
//
//   node tools/lcp_probe.mjs <outDir> <label> <runs> <url> [url...]
//
// Writes <outDir>/<label>.json (every run) and one viewport PNG per URL and profile.
// Reports: LCP (ms, element, image), FCP, CLS, load, requests, KB on the wire, and whether
// model-viewer.min.js or any .glb was fetched while the page loaded (nothing is clicked).
import { spawn } from 'node:child_process';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';

const CHROME = process.env.CHROME || 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const [outDir, label, runsArg, ...urls] = process.argv.slice(2);
if (!outDir || !label || !urls.length) {
  console.error('usage: node tools/lcp_probe.mjs <outDir> <label> <runs> <url> [url...]');
  process.exit(2);
}
const RUNS = Math.max(1, Number(runsArg) || 3);
const PORT = 9400 + Math.floor(Math.random() * 400);
const PROFILES = {
  desktop: { width: 1440, height: 900, dpr: 1, mobile: false },
  mobile: {
    width: 390, height: 844, dpr: 3, mobile: true,
    ua: 'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.36',
    net: { latency: 150, down: (1.6 * 1024 * 1024) / 8, up: (750 * 1024) / 8 }, cpu: 4,
  },
};
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const median = (a) => { const s = a.filter((x) => typeof x === 'number').sort((x, y) => x - y); return s.length ? s[Math.floor(s.length / 2)] : null; };

function cdp(wsUrl) {
  return new Promise((resolve, reject) => {
    const ws = new WebSocket(wsUrl);
    let id = 0;
    const pending = new Map();
    const listeners = [];
    ws.onopen = () => resolve({
      send(method, params = {}) {
        return new Promise((res, rej) => { const i = ++id; pending.set(i, { res, rej }); ws.send(JSON.stringify({ id: i, method, params })); });
      },
      on(fn) { listeners.push(fn); },
      close() { try { ws.close(); } catch (e) { /* already closed */ } },
    });
    ws.onmessage = (ev) => {
      const m = JSON.parse(typeof ev.data === 'string' ? ev.data : ev.data.toString());
      if (m.id && pending.has(m.id)) {
        const p = pending.get(m.id); pending.delete(m.id);
        if (m.error) { p.rej(new Error(JSON.stringify(m.error))); } else { p.res(m.result); }
      } else if (m.method) { listeners.forEach((f) => f(m)); }
    };
    ws.onerror = (e) => reject(e);
  });
}

const OBSERVERS = "window.__lcp=null;window.__cls=0;" +
  "try{new PerformanceObserver(function(l){var e=l.getEntries();window.__lcp=e[e.length-1];}).observe({type:'largest-contentful-paint',buffered:true});}catch(e){}" +
  "try{new PerformanceObserver(function(l){l.getEntries().forEach(function(e){if(!e.hadRecentInput){window.__cls+=e.value;}});}).observe({type:'layout-shift',buffered:true});}catch(e){}";

const READ = `JSON.stringify((function(){
  var l=window.__lcp, nav=performance.getEntriesByType('navigation')[0]||{}, res=performance.getEntriesByType('resource');
  var el=l&&l.element; var fcp=(performance.getEntriesByName('first-contentful-paint')[0]||{}).startTime||0;
  return {lcp:l?Math.round(l.startTime):null,
    lcpEl:el?(el.tagName.toLowerCase()+(el.id?'#'+el.id:'')+(el.className&&typeof el.className==='string'?'.'+el.className.trim().split(/\\s+/).slice(0,2).join('.'):'')):null,
    lcpImg:l&&l.url?l.url.split('/').pop().slice(0,90):null,
    fcp:Math.round(fcp), cls:Math.round(window.__cls*1000)/1000,
    load:Math.round(nav.loadEventEnd||0),
    mv:res.filter(function(e){return /model-viewer|\\.glb(\\?|$)/.test(e.name);}).map(function(e){return e.name.split('/').slice(-2).join('/');})};
})())`;

async function measure(url, prof, shot) {
  const t = await (await fetch(`http://127.0.0.1:${PORT}/json/new?about:blank`, { method: 'PUT' })).json();
  const c = await cdp(t.webSocketDebuggerUrl);
  let bytes = 0; let reqs = 0;
  c.on((m) => {
    if (m.method === 'Network.requestWillBeSent') { reqs += 1; }
    if (m.method === 'Network.loadingFinished') { bytes += m.params.encodedDataLength || 0; }
  });
  await c.send('Page.enable');
  await c.send('Network.enable');
  await c.send('Runtime.enable');
  await c.send('Network.setCacheDisabled', { cacheDisabled: true });
  await c.send('Emulation.setDeviceMetricsOverride', { width: prof.width, height: prof.height, deviceScaleFactor: prof.dpr, mobile: prof.mobile });
  if (prof.mobile) {
    await c.send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
    await c.send('Network.setUserAgentOverride', { userAgent: prof.ua });
  }
  if (prof.net) {
    await c.send('Network.emulateNetworkConditions', { offline: false, latency: prof.net.latency, downloadThroughput: prof.net.down, uploadThroughput: prof.net.up });
  }
  if (prof.cpu) { await c.send('Emulation.setCPUThrottlingRate', { rate: prof.cpu }); }
  await c.send('Page.addScriptToEvaluateOnNewDocument', { source: OBSERVERS });
  const loaded = new Promise((r) => c.on((m) => { if (m.method === 'Page.loadEventFired') { r(); } }));
  await c.send('Page.navigate', { url });
  await Promise.race([loaded, sleep(90000)]);
  await sleep(prof.cpu ? 7000 : 4000);
  const r = await c.send('Runtime.evaluate', { expression: READ, returnByValue: true });
  const data = JSON.parse(r.result.value);
  if (shot) {
    const s = await c.send('Page.captureScreenshot', { format: 'png' });
    await fs.writeFile(shot, Buffer.from(s.data, 'base64'));
  }
  c.close();
  await fetch(`http://127.0.0.1:${PORT}/json/close/${t.id}`).catch(() => {});
  return { ...data, reqs, kb: Math.round(bytes / 1024) };
}

function slug(u) {
  const p = decodeURIComponent(new URL(u).pathname).replace(/\/+$/, '').split('/').pop() || 'home';
  return /^[\x20-\x7e]+$/.test(p) ? p.slice(0, 60) : 'id-' + Buffer.from(p).toString('hex').slice(0, 16);
}

await fs.mkdir(outDir, { recursive: true });
const profileDir = await fs.mkdtemp(path.join(os.tmpdir(), 'lcp-probe-'));
const chrome = spawn(CHROME, [
  '--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${profileDir}`,
  '--no-first-run', '--no-default-browser-check', '--disable-extensions', '--hide-scrollbars',
  '--window-size=1440,900', 'about:blank',
], { stdio: 'ignore' });
let ready = false;
for (let i = 0; i < 60 && !ready; i += 1) {
  try { await (await fetch(`http://127.0.0.1:${PORT}/json/version`)).json(); ready = true; } catch (e) { await sleep(250); }
}
if (!ready) { console.error('chrome did not start'); chrome.kill(); process.exit(1); }

const out = { label, at: new Date().toISOString(), runs: RUNS, results: [] };
try {
  for (const url of urls) {
    for (const [pname, prof] of Object.entries(PROFILES)) {
      const runs = [];
      for (let i = 0; i < RUNS; i += 1) {
        const shot = i === RUNS - 1 ? path.join(outDir, `${label}-${slug(url)}-${pname}.png`) : null;
        try { runs.push(await measure(url, prof, shot)); } catch (e) { runs.push({ error: String(e && e.message || e) }); }
      }
      const ok = runs.filter((x) => !x.error);
      const row = {
        url, profile: pname,
        lcp_median: median(ok.map((x) => x.lcp)), fcp_median: median(ok.map((x) => x.fcp)),
        cls_max: ok.length ? Math.max(...ok.map((x) => x.cls || 0)) : null,
        load_median: median(ok.map((x) => x.load)), kb_median: median(ok.map((x) => x.kb)), reqs_median: median(ok.map((x) => x.reqs)),
        lcp_element: ok.length ? ok[ok.length - 1].lcpEl : null, lcp_image: ok.length ? ok[ok.length - 1].lcpImg : null,
        model_viewer_or_glb_fetched: ok.some((x) => x.mv && x.mv.length), fetched: ok.length ? ok[ok.length - 1].mv : [],
        runs,
      };
      out.results.push(row);
      console.log(`${pname.padEnd(7)} LCP ${String(row.lcp_median).padStart(5)} ms  FCP ${String(row.fcp_median).padStart(5)}  CLS ${row.cls_max}  load ${row.load_median}  ${row.kb_median} KB/${row.reqs_median} req  3D-on-load: ${row.model_viewer_or_glb_fetched ? 'YES ' + row.fetched.join(',') : 'no'}  LCP el: ${row.lcp_element} ${row.lcp_image || ''}  | ${decodeURIComponent(url).slice(0, 80)}`);
    }
  }
} finally {
  await fs.writeFile(path.join(outDir, `${label}.json`), JSON.stringify(out, null, 2));
  chrome.kill();
  await sleep(500);
  await fs.rm(profileDir, { recursive: true, force: true }).catch(() => {});
}
