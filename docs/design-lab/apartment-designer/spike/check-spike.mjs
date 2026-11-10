// node check-spike.mjs [--gl=gpu|soft] [--port=47960]
// Presses the spike like a phone user, in headless Chrome over CDP (node 24, no dependencies), and writes
// evidence/receipt.json + screenshots. The page must be served (python -m http.server 47960 in this folder).
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const arg = (k, d) => { const a = process.argv.find((x) => x.startsWith('--' + k + '=')); return a ? a.split('=')[1] : d; };
const GL = arg('gl', 'gpu'), URL0 = 'http://127.0.0.1:' + arg('port', '47960') + '/index.html';
const here = path.dirname(fileURLToPath(import.meta.url)), out = path.join(here, 'evidence');
fs.mkdirSync(out, { recursive: true });
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe', PORT = 9300 + Math.floor(Math.random() * 500);
const profile = path.join(os.tmpdir(), 'nd-spike-profile-' + PORT);
const chrome = spawn(CHROME, ['--headless=new', '--remote-debugging-port=' + PORT, '--user-data-dir=' + profile, '--no-first-run', '--no-default-browser-check', '--disable-extensions', '--ignore-gpu-blocklist',
  ...(GL === 'gpu' ? ['--enable-gpu', '--use-angle=d3d11'] : ['--enable-unsafe-swiftshader', '--use-angle=swiftshader']), '--window-size=1366,900', '--lang=he-IL'], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
async function up() { for (let i = 0; i < 80; i++) { try { const r = await fetch('http://127.0.0.1:' + PORT + '/json/version'); if (r.ok) return; } catch {} await sleep(250); } throw new Error('chrome did not start'); }
function connect(url) {
  const ws = new WebSocket(url); let id = 0; const pend = new Map(), subs = [];
  ws.onmessage = (ev) => { const m = JSON.parse(ev.data); if (m.id && pend.has(m.id)) { const p = pend.get(m.id); pend.delete(m.id); m.error ? p.rej(new Error(JSON.stringify(m.error))) : p.res(m.result); } else if (m.method) subs.forEach((f) => f(m)); };
  return { ready: new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; }), send: (method, params = {}) => new Promise((res, rej) => { const i = ++id; pend.set(i, { res, rej }); ws.send(JSON.stringify({ id: i, method, params })); }), on: (f) => subs.push(f), close: () => ws.close() };
}
const UA = 'Mozilla/5.0 (Linux; Android 14; SM-A546B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36';
const receipt = { when: new Date().toISOString(), gl_mode: GL, runs: {}, checks: [] };
let fails = 0;
const check = (name, ok, detail) => { receipt.checks.push({ name, ok: !!ok, detail }); if (!ok) fails++; console.log((ok ? 'ok   ' : 'FAIL ') + name + (detail !== undefined ? '  ' + (typeof detail === 'string' ? detail : JSON.stringify(detail)) : '')); };

async function page(opts) {
  const t = await (await fetch('http://127.0.0.1:' + PORT + '/json/new?about:blank', { method: 'PUT' })).json();
  const c = connect(t.webSocketDebuggerUrl); await c.ready;
  const net = { n: 0, bytes: 0, urls: [] }, errors = [];
  c.on((m) => {
    if (m.method === 'Network.requestWillBeSent') { net.n++; net.urls.push(m.params.request.url); }
    if (m.method === 'Network.loadingFinished') net.bytes += m.params.encodedDataLength || 0;
    if (m.method === 'Runtime.exceptionThrown') errors.push(m.params.exceptionDetails.text + ' ' + ((m.params.exceptionDetails.exception || {}).description || ''));
    if (m.method === 'Runtime.consoleAPICalled' && m.params.type === 'error') errors.push(m.params.args.map((a) => a.value || a.description).join(' '));
  });
  await c.send('Page.enable'); await c.send('Runtime.enable'); await c.send('Network.enable');
  await c.send('Emulation.setDeviceMetricsOverride', { width: opts.w, height: opts.h, deviceScaleFactor: opts.dpr, mobile: !!opts.mobile });
  if (opts.mobile) { await c.send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 }); await c.send('Emulation.setUserAgentOverride', { userAgent: UA }); }
  await c.send('Network.setCacheDisabled', { cacheDisabled: !!opts.cold });
  if (opts.slow) await c.send('Network.emulateNetworkConditions', { offline: false, latency: 150, downloadThroughput: (1.6 * 1024 * 1024) / 8, uploadThroughput: (750 * 1024) / 8 });
  const ev = async (expr) => { const r = await c.send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true }); if (r.exceptionDetails) throw new Error(r.exceptionDetails.text + ' ' + JSON.stringify(r.exceptionDetails.exception)); return r.result.value; };
  const shot = async (name) => { const r = await c.send('Page.captureScreenshot', { format: 'png' }); fs.writeFileSync(path.join(out, name + '.png'), Buffer.from(r.data, 'base64')); };
  const touch = (type, x, y) => c.send('Input.dispatchTouchEvent', { type, touchPoints: type === 'touchEnd' ? [] : [{ x, y, id: 1 }] });
  const tap = async (x, y) => { await touch('touchStart', x, y); await sleep(40); await touch('touchEnd'); await sleep(120); };
  const drag = async (x0, y0, x1, y1, steps = 14, hold = false) => { await touch('touchStart', x0, y0); await sleep(30); for (let i = 1; i <= steps; i++) { await touch('touchMove', x0 + ((x1 - x0) * i) / steps, y0 + ((y1 - y0) * i) / steps); await sleep(18); } if (!hold) { await touch('touchEnd'); await sleep(120); } };
  const mouse = async (x0, y0, x1, y1, steps = 14) => { await c.send('Input.dispatchMouseEvent', { type: 'mousePressed', x: x0, y: y0, button: 'left', clickCount: 1 }); for (let i = 1; i <= steps; i++) { await c.send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: x0 + ((x1 - x0) * i) / steps, y: y0 + ((y1 - y0) * i) / steps, button: 'left', buttons: 1 }); await sleep(18); } await c.send('Input.dispatchMouseEvent', { type: 'mouseReleased', x: x1, y: y1, button: 'left', clickCount: 1 }); await sleep(120); };
  await c.send('Page.navigate', { url: URL0 + '?t=' + Date.now() });
  for (let i = 0; i < 240; i++) { if (await ev('!!(window.__nd && window.__nd.timings.first_3d_frame_ms)').catch(() => false)) break; await sleep(250); }
  return { c, ev, shot, tap, drag, mouse, touch, net, errors, close: async () => { c.close(); await fetch('http://127.0.0.1:' + PORT + '/json/close/' + t.id).catch(() => {}); } };
}
const center = (sel) => `(()=>{const r=document.querySelector(${JSON.stringify(sel)}).getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]})()`;
const load = (p) => p.ev(`(()=>{const t=window.__nd.timings,fcp=performance.getEntriesByName('first-contentful-paint')[0];return {fcp_ms:fcp?Math.round(fcp.startTime):null,plan_drawn_ms:Math.round(t.plan_ms),space_mounted_ms:Math.round(t.space_mounted_ms),first_3d_frame_ms:Math.round(t.first_3d_frame_ms)}})()`);

try {
  await up();
  // ---------- phone, cold cache ----------
  let p = await page({ w: 390, h: 844, dpr: 2.625, mobile: true, cold: true });
  await sleep(1500);
  receipt.gl_renderer = await p.ev('window.__nd.space.gl()');
  receipt.runs.phone_cold = { ...(await load(p)), requests: p.net.n, transferred_kb: Math.round(p.net.bytes / 1024), draw: await p.ev('window.__nd.space.stats()') };
  console.log('renderer:', receipt.gl_renderer, JSON.stringify(receipt.runs.phone_cold));
  check('no horizontal scroll at 390', await p.ev('document.documentElement.scrollWidth <= innerWidth'));
  check('plan drawn before the 3D library', receipt.runs.phone_cold.plan_drawn_ms < receipt.runs.phone_cold.space_mounted_ms, receipt.runs.phone_cold);
  await p.shot('01-phone-first');

  // 1. drag the sofa on the PLAN with a finger: the 3D piece must stand exactly where the model says
  let c0 = await p.ev(center('[data-item="i2"] rect')), before = await p.ev('(()=>{const i=window.__nd.store.item("i2");return [i.x,i.y]})()');
  await p.drag(c0[0], c0[1], c0[0] - 30, c0[1] + 40);
  let st = await p.ev('(()=>{const i=window.__nd.store.item("i2");return {model:[i.x,i.y], three:window.__nd.space.placed("i2"), log:window.__nd.store.design.log.length, room:i.room}})()');
  check('plan drag moved the sofa in the model', st.model[0] !== before[0] && st.model[1] !== before[1], { before, after: st.model });
  check('3D piece stands where the model says (plan -> 3D)', st.three[0] === st.model[0] && st.three[1] === st.model[1], st);
  check('one drag is one line in the decision log', st.log === 1, st.log);
  await p.shot('02-phone-sofa-moved');

  // 2. drag the bedroom partition: rooms change in both views, then the rule stops it
  c0 = await p.ev(center('.grip rect[data-wall="p6"]'));
  const m0 = await p.ev('window.__nd.store.derived.faceBy.master.net');
  await p.drag(c0[0], c0[1], c0[0] + 9, c0[1], 6);
  let w = await p.ev('(()=>{const d=window.__nd.store;return {shift:d.design.geometry.walls.p6||0, master:d.derived.faceBy.master.net, bed2:d.derived.faceBy.bed2.net, label:[...document.querySelectorAll(".L-labels .ra")].map(t=>t.textContent).join("|")}})()');
  check('partition moved, master bedroom grew', w.shift > 0 && w.master > m0, w);
  check('plan label shows the new area', w.label.includes(w.master.toFixed(1)), w.label);
  c0 = await p.ev(center('.grip rect[data-wall="p6"]'));
  await p.drag(c0[0], c0[1], c0[0] + 40, c0[1], 10, true);
  await sleep(150);
  let blocked = await p.ev('(()=>{const t=document.getElementById("toast");return {shown:!t.hidden,text:t.textContent,shift:window.__nd.store.design.geometry.walls.p6,clear:window.__nd.store.derived.faceBy.bed2.clearW}})()');
  await p.shot('03-phone-wall-blocked');
  await p.touch('touchEnd'); await sleep(100);
  check('rule stops the partition with a reason in Hebrew', blocked.shown && blocked.text.includes('2.60') && blocked.clear >= 260, blocked);

  // 3. a fixed wall says why it does not move
  c0 = await p.ev(center('.hit[data-wall="m4"]'));
  await p.drag(c0[0], c0[1], c0[0] + 14, c0[1], 4);
  const fixed = await p.ev('document.getElementById("toast").textContent');
  check('mamad wall refuses with its reason', fixed.includes('ממ״ד'), fixed);
  await sleep(3400);

  // 4. tap a room on the plan, choose a floor: 3D material and the bill of quantities follow
  await p.ev('window.__nd.store.derived.faceBy.living.bb').then(async () => { const r = await p.ev(`(()=>{const s=document.querySelector('.nd-plan'),m=s.getScreenCTM();const q=new DOMPoint(120,120).matrixTransform(m);return [q.x,q.y]})()`); await p.tap(r[0], r[1]); });
  check('room tap opens the floor sheet', await p.ev('!document.getElementById("sheet").hidden && document.querySelector("#sheet h2").textContent.includes("סלון")'), await p.ev('document.querySelector("#sheet h2").textContent'));
  c0 = await p.ev('(()=>{const b=[...document.querySelectorAll("#sheet .opt")].find(b=>b.textContent.includes("פרקט"));const r=b.getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]})()');
  await p.tap(c0[0], c0[1]);
  const fl = await p.ev('(()=>{const q=window.__nd.quantities(window.__nd.store);return {model:window.__nd.store.floorOf("living"), three:window.__nd.space.floorKey("living"), boq:q.floors["oak-plank"], living:window.__nd.store.derived.faceBy.living.net}})()');
  check('floor finish: model, 3D material and quantities agree', fl.model === 'oak-plank' && fl.three === 'oak-plank' && fl.boq === fl.living, fl);
  await p.shot('04-phone-floor-oak');
  c0 = await p.ev(center('nav button[data-sheet="boq"]')); await p.tap(c0[0], c0[1]);
  await p.shot('05-phone-quantities');
  await p.tap(c0[0], c0[1]);

  // 5. drag a piece in the 3D view: the plan must follow (3D -> plan)
  await p.ev('window.__nd.plan.el.dispatchEvent(new PointerEvent("pointerdown",{bubbles:true}))'); // clear selection
  const dt = await p.ev('(()=>{const i=window.__nd.store.item("i4");return {from:window.__nd.space.screenOf(i.x,i.y,60), to:window.__nd.space.screenOf(i.x+90,i.y-60,60), xy:[i.x,i.y]}})()');
  await p.drag(dt.from[0], dt.from[1], dt.to[0], dt.to[1]);
  const d3 = await p.ev('(()=>{const i=window.__nd.store.item("i4");return {model:[i.x,i.y], three:window.__nd.space.placed("i4"), plan:document.querySelector(\'[data-item="i4"]\').getAttribute("transform")}})()');
  check('3D drag moved the table in the model', Math.abs(d3.model[0] - dt.xy[0]) > 30, { before: dt.xy, after: d3.model });
  check('plan follows the 3D drag (3D -> plan)', d3.plan.startsWith('translate(' + d3.model[0] + ' ' + d3.model[1] + ')'), d3.plan);
  await p.shot('06-phone-3d-drag');

  // 6. walk inside: tap the chip, tap the floor, the red marker on the plan walks with you
  c0 = await p.ev(center('#m-walk')); await p.tap(c0[0], c0[1]); await sleep(400);
  const v0 = await p.ev('window.__nd.space.getView()');
  await p.shot('07-phone-walk');
  const sp = await p.ev('(()=>{const r=document.getElementById("space").getBoundingClientRect();return [r.left+r.width*0.5,r.top+r.height*0.72]})()');
  await p.tap(sp[0], sp[1]); await sleep(1200);
  const v1 = await p.ev('({v:window.__nd.space.getView(), cam:document.querySelector(".cam").getAttribute("transform")})');
  check('tap on the floor walks there', v1.v.walk && Math.hypot(v1.v.x - v0.x, v1.v.y - v0.y) > 20, { from: [Math.round(v0.x), Math.round(v0.y)], to: [Math.round(v1.v.x), Math.round(v1.v.y)] });
  check('camera marker on the plan is where you stand', v1.cam.startsWith('translate(' + v1.v.x.toFixed(1) + ' ' + v1.v.y.toFixed(1) + ')'), v1.cam);
  await p.shot('07b-phone-walked');
  c0 = await p.ev(center('#m-doll')); await p.tap(c0[0], c0[1]); await sleep(300);

  // 7. undo steps back through everything
  c0 = await p.ev(center('#undo'));
  for (let i = 0; i < 4; i++) await p.tap(c0[0], c0[1]);
  const un = await p.ev('(()=>{const s=window.__nd.store;return {i2:[s.item("i2").x,s.item("i2").y], i2three:window.__nd.space.placed("i2"), wall:s.design.geometry.walls.p6||0, floor:s.floorOf("living"), floor3:window.__nd.space.floorKey("living")}})()');
  check('undo returns sofa, wall and floor in both views', un.i2[0] === before[0] && un.i2three[0] === before[0] && un.wall === 0 && un.floor === 'porcelain-80' && un.floor3 === 'porcelain-80', un);

  // 8. speed: 2D -> 3D latency over 120 moves, and frames while orbiting
  const lat = await p.ev(`(async()=>{const nd=window.__nd;nd.lat.length=0;nd.work_ms.length=0;const f=()=>new Promise(r=>requestAnimationFrame(r));const fr=[];let t=performance.now();for(let i=0;i<120;i++){nd.store.apply({op:'item.move',id:'i2',x:330+(i%40),y:210+(i%25)},{gesture:'bench'});await f();const n=performance.now();fr.push(n-t);t=n;}await f();const q=(a,p)=>{const s=[...a].sort((x,y)=>x-y);return +s[Math.min(s.length-1,Math.floor(s.length*p))].toFixed(2)};return {n:nd.lat.length,work_p50:q(nd.work_ms,.5),work_p95:q(nd.work_ms,.95),work_max:q(nd.work_ms,1),shown_p50:q(nd.lat,.5),shown_p95:q(nd.lat,.95),display_frame_ms:q(fr,.5)}})()`);
  receipt.sync_2d_to_3d_ms = lat;
  check('2D -> 3D: work under 8 ms at p95 (half of a 60 Hz frame)', lat.work_p95 < 8, lat);
  check('2D -> 3D: every change is on screen by the next display frame', lat.shown_p95 <= lat.display_frame_ms * 1.25 && lat.n === 120, lat);
  const wl = await p.ev(`(async()=>{const nd=window.__nd,ts=[];const f=()=>new Promise(r=>requestAnimationFrame(r));for(let i=0;i<40;i++){const t=performance.now();nd.store.apply({op:'wall.shift',id:'p6',d:(i%8)*5},{gesture:'benchw'});ts.push(performance.now()-t);await f();}nd.store.apply({op:'wall.shift',id:'p6',d:0});ts.sort((a,b)=>a-b);return {n:ts.length,p50:+ts[20].toFixed(2),p95:+ts[38].toFixed(2)}})()`);
  receipt.wall_move_rebuild_ms = wl;
  check('a wall move rebuilds rooms, walls and floors under 16.7 ms at p95', wl.p95 < 16.7, wl);
  await p.ev('window.__fr=[];(function f(t){window.__fr.push(t);if(window.__fr.length<600)requestAnimationFrame(f)})(performance.now())');
  await p.drag(sp[0], sp[1] - 60, sp[0] + 160, sp[1] - 100, 60);
  const fps = await p.ev('(()=>{const a=window.__fr,d=[];for(let i=1;i<a.length;i++)d.push(a[i]-a[i-1]);d.sort((x,y)=>x-y);return {frames:a.length,median_ms:+d[Math.floor(d.length/2)].toFixed(1),p95_ms:+d[Math.floor(d.length*0.95)].toFixed(1)}})()');
  fps.render_cpu_ms = await p.ev('(()=>{const s=[...window.__nd.space.renders].sort((a,b)=>a-b);return {n:s.length,p50:+s[Math.floor(s.length/2)].toFixed(2),p95:+s[Math.floor(s.length*0.95)].toFixed(2)}})()');
  fps.draw = await p.ev('window.__nd.space.stats()');
  receipt.orbit_frame_ms = fps;
  check('orbit: render work under 8 ms at p95', fps.render_cpu_ms.p95 < 8, fps);
  check('no page errors on the phone run', p.errors.length === 0, p.errors);
  await p.shot('08-phone-end');
  await p.close();

  // ---------- phone, slow 4G, cold ----------
  p = await page({ w: 390, h: 844, dpr: 2.625, mobile: true, cold: true, slow: true });
  receipt.runs.phone_slow4g_cold = { ...(await load(p)), requests: p.net.n, transferred_kb: Math.round(p.net.bytes / 1024) };
  console.log('slow 4G:', JSON.stringify(receipt.runs.phone_slow4g_cold));
  await p.close();

  // ---------- desktop ----------
  p = await page({ w: 1366, h: 900, dpr: 1, cold: true });
  await sleep(1500);
  receipt.runs.desktop_cold = { ...(await load(p)), requests: p.net.n, transferred_kb: Math.round(p.net.bytes / 1024) };
  c0 = await p.ev(center('[data-item="i8"] rect'));
  await p.mouse(c0[0], c0[1], c0[0] + 40, c0[1] + 20);
  const dk = await p.ev('(()=>{const i=window.__nd.store.item("i8");return {model:[i.x,i.y],three:window.__nd.space.placed("i8")}})()');
  check('desktop: mouse drag on the plan moves the bed in 3D', dk.model[0] === dk.three[0] && dk.model[1] === dk.three[1] && dk.model[0] !== 730, dk);
  check('desktop: side by side, no horizontal scroll', await p.ev('document.documentElement.scrollWidth <= innerWidth && document.getElementById("space").getBoundingClientRect().width > 600'));
  check('no page errors on the desktop run', p.errors.length === 0, p.errors);
  await p.shot('09-desktop');
  await p.close();
} catch (e) { console.error(e); fails++; receipt.error = String(e); }
receipt.passed = receipt.checks.filter((c) => c.ok).length; receipt.failed = fails;
fs.writeFileSync(path.join(out, 'receipt.json'), JSON.stringify(receipt, null, 2));
console.log('\n' + receipt.passed + ' passed, ' + fails + ' failed');
chrome.kill();
await sleep(300);
try { fs.rmSync(profile, { recursive: true, force: true }); } catch {}
process.exit(fails ? 1 : 0);
