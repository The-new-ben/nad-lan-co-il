// HAD-701: the whole road from "measure with the camera" to the 3D designer, inside the page every project opens
// (/tour/designer/?scan=on), on a computer: the phone's camera session is the stand-in from roomscan-xrmock.js.
// It proves the JOINTS (the switch, the fourth way on the start screen, the handover of the measured draft to the drawing
// tool, the designer opening on it). It does NOT prove a real phone: that is ROOMSCAN-DEVICE-TEST.md.
//   python docs/tools/design-studio/serve_local.py 47962      then
//   node docs/design-lab/apartment-designer/check-scan-studio.mjs [base] [shots folder]
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const BASE = process.argv[2] || 'http://127.0.0.1:47962';
// on the live site the stand-in is handed to the page as text (a secure page may not load a script from this computer)
const LIVE = /^https:/.test(BASE);
const MOCKSRC = fs.readFileSync(new URL('./roomscan-xrmock.js', import.meta.url), 'utf8');
const INSTALL = LIVE
  ? `(async()=>{const u=URL.createObjectURL(new Blob([${JSON.stringify(MOCKSRC)}],{type:'text/javascript'}));const m=await import(u);window.__mock=m.installXrMock();return true})()`
  : `(async()=>{const m=await import('/docs/design-lab/apartment-designer/roomscan-xrmock.js');window.__mock=m.installXrMock();return true})()`;
const SHOTS = process.argv[3] || path.join(os.tmpdir(), 'nd-scan-studio-shots');
fs.mkdirSync(SHOTS, { recursive: true });
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let pass = 0, fail = 0;
const ok = (name, cond, extra) => { if (cond) { pass += 1; console.log('ok   ' + name); } else { fail += 1; console.log('FAIL ' + name + (extra !== undefined ? '  -> ' + JSON.stringify(extra) : '')); } };

const PORT = 9300 + Math.floor(Math.random() * 400), profile = path.join(os.tmpdir(), 'nd-scanstudio-' + PORT);
const chrome = spawn(CHROME, ['--headless=new', '--remote-debugging-port=' + PORT, '--user-data-dir=' + profile, '--no-first-run', '--disable-extensions', '--ignore-gpu-blocklist', '--enable-gpu', '--use-angle=d3d11', '--hide-scrollbars', 'about:blank'], { stdio: 'ignore' });
for (let i = 0; i < 80; i++) { try { if ((await fetch('http://127.0.0.1:' + PORT + '/json/version')).ok) break; } catch (e) { /* not up yet */ } await sleep(250); }
const t = await (await fetch('http://127.0.0.1:' + PORT + '/json/new?about:blank', { method: 'PUT' })).json();
const ws = new WebSocket(t.webSocketDebuggerUrl); let id = 0; const pend = new Map(), errors = [];
ws.onmessage = (ev) => {
  const m = JSON.parse(ev.data);
  if (m.id && pend.has(m.id)) { pend.get(m.id)(m.result || m.error); pend.delete(m.id); }
  else if (m.method === 'Runtime.exceptionThrown') errors.push((m.params.exceptionDetails.exception && m.params.exceptionDetails.exception.description || m.params.exceptionDetails.text || '').slice(0, 300));
  else if (m.method === 'Runtime.consoleAPICalled' && m.params.type === 'error') errors.push('console: ' + m.params.args.map((a) => a.value || a.description || '').join(' ').slice(0, 300));
};
await new Promise((r) => (ws.onopen = r));
const send = (method, params = {}) => new Promise((res) => { const i = ++id; pend.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); });
const ev = async (e) => { const r = await send('Runtime.evaluate', { expression: e, awaitPromise: true, returnByValue: true }); return r.exceptionDetails ? 'EVAL ERROR ' + JSON.stringify(r.exceptionDetails).slice(0, 400) : r.result.value; };
await send('Page.enable'); await send('Runtime.enable');
await send('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 2, mobile: true });
await send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
const go = async (u, wait = 6000) => { await send('Page.navigate', { url: u }); await sleep(wait); };
const shot = async (name) => { const d = await send('Page.captureScreenshot', { format: 'png' }); fs.writeFileSync(path.join(SHOTS, name + '.png'), Buffer.from(d.data, 'base64')); };
const tapXY = async (x, y) => { await send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x, y, id: 1 }] }); await sleep(40); await send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }); await sleep(140); };
const tap = async (expr) => { const c = await ev(`(()=>{const e=${expr};if(!e)return null;const r=e.getBoundingClientRect();return r.width?[r.left+r.width/2,r.top+r.height/2]:null})()`); if (!c || typeof c === 'string') return false; await tapXY(c[0], c[1]); return true; };
const until = async (expr, ms = 5000) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { const v = await ev(expr); if (v === true) return true; await sleep(80); } return false; };
const SR = "document.getElementById('host').shadowRoot";
const OV = 'document.querySelector(".nlscan-root")';
const RS = `(${SR}.querySelector('.nlscan-host')||{}).shadowRoot`; // the camera tool's own screen, inside the designer's frame
const K = (k) => `${OV}.querySelector('[data-k="${k}"]')`;
const btn = (txt) => `[...${SR}.querySelectorAll('button')].find(b=>b.textContent.trim()===${JSON.stringify(txt)})`;

// ---- 1. without the switch nothing changes, even on a phone that can measure ----
await go(BASE + '/tour/designer/?scan=off');
await ev(INSTALL);
await tap(`document.querySelector('#pick button.is-mine')`); await sleep(3500);
let ways = await ev(`${SR}.querySelectorAll('.pm-opt').length`);
ok('switch off: the start screen has its three ways only', ways === 3, ways);

// ---- 2. with the switch, on a browser that cannot measure: still three ways, no error ----
await go(BASE + '/tour/designer/?scan=on');
await ev(`Object.defineProperty(navigator,'xr',{value:undefined,configurable:true});true`);
await tap(`document.querySelector('#pick button.is-mine')`); await sleep(3500);
ways = await ev(`${SR}.querySelectorAll('.pm-opt').length`);
ok('switch on, a browser that cannot measure: three ways, nothing broken', ways === 3, ways);

// ---- 3. with the switch, on a phone that can measure: the fourth way, the walk, the drawing, the 3D ----
await go(BASE + '/tour/designer/?scan=on');
await ev(INSTALL);
await tap(`document.querySelector('#pick button.is-mine')`); await sleep(3500);
const w4 = JSON.parse(await ev(`JSON.stringify({n:${SR}.querySelectorAll('.pm-opt').length,t:[...${SR}.querySelectorAll('.pm-extra h4')].map(h=>h.textContent),b:[...${SR}.querySelectorAll('.pm-extra button')].map(b=>b.textContent.trim())})`));
ok('switch on, a phone that can measure: a fourth way "למדוד במצלמה"', w4.n === 4 && w4.t[0] === 'למדוד במצלמה' && w4.b[0] === 'מדידה במצלמה', w4);
await shot('1-start-four-ways');
ok('a press on the fourth way', await tap(`${SR}.querySelector('.pm-extra button')`));
ok('the explanation screen of the camera measuring opens in the same frame', await until(`!!${RS}&&/מודדים את הדירה במצלמה/.test(${RS}.textContent)`, 6000));
await shot('2-intro');
ok('a press on "להתחיל מדידה"', await tap(`${RS}.querySelector('[data-a="start"]')`));
ok('the measuring layer is on the page', await until(`!!${OV}`, 6000));
// the walk: two rooms side by side, inner faces, world metres = plan cm / 100
const ROOMS = [[[0, 0], [4.8, 0], [4.8, 3.9], [0, 3.9]], [[4.92, 0], [8.0, 0], [8.0, 3.9], [4.92, 3.9]]];
const NAMES = ['living', 'bedroom'];
const sig = `${OV}.querySelector('[data-r="count"]').textContent+'|'+${OV}.querySelector('[data-r="msg"]').textContent`;
async function mark(p) {
  await ev(`__mock.aim=[${p[0]},${p[1]}];true`); await sleep(200);
  for (let i = 0; i < 3; i++) {
    if (!(await until(`!${K('corner')}.disabled`, 5000))) return false;
    await sleep(160); const s0 = await ev(sig);
    await tap(K('corner'));
    if (await until(`(${sig})!==${JSON.stringify(s0)}`, 2500)) return true;
  }
  return false;
}
let walked = true;
for (let r = 0; r < ROOMS.length; r++) {
  for (const p of ROOMS[r]) walked = (await mark(p)) && walked;
  await tap(K('close'));
  walked = (await until(`!${OV}.querySelector('[data-r="names"]').hidden`, 4000)) && walked;
  await tap(`${OV}.querySelector('[data-name="${NAMES[r]}"]')`); await sleep(400);
  if (r === 0) await shot('3-measuring');
}
ok('two rooms walked: eight corners marked, both closed and named', walked);
await tap(K('finish'));
ok('the camera ends and the result screen shows the plan', await until(`!${OV}&&!!${RS}&&!!${RS}.querySelector('[data-a="done"]')`, 6000));
const res = await ev(`${RS}&&${RS}.querySelector('.nlscan-sum')?${RS}.querySelector('.nlscan-sum').textContent:''`);
ok('the result names two rooms', /2 חדרים/.test(String(res)), res);
await shot('4-result');
ok('a press on "להמשיך לתיקון ולתלת ממד"', await tap(`${RS}.querySelector('[data-a="done"]')`));
ok('the drawing tool opens on what was measured, at the rooms step', await until(`!!${SR}.querySelector('.pm')&&!!(${btn('לפתוח בתלת ממד')})`, 8000));
const sum = await ev(`(${SR}.querySelector('[data-pm="sum"]')||{}).textContent||''`);
ok('the drawing tool counts the same two rooms', /2 חדרים/.test(String(sum)), sum);
await shot('5-drawing-rooms');
const dis = await ev(`(${btn('לפתוח בתלת ממד')}).disabled`);
ok('the plan is complete: "לפתוח בתלת ממד" is active', dis === false, dis);
await tap(btn('לפתוח בתלת ממד')); await sleep(5000);
const d = JSON.parse(await ev(`JSON.stringify({h2:(${SR}.querySelector('header h2')||{}).textContent||'',sub:(${SR}.querySelector('[data-nd="sub"]')||{}).textContent||'',pm:!!${SR}.querySelector('.pm'),pick:document.querySelector('#pick button.is-mine').getAttribute('aria-pressed')})`));
ok('the designer opens on MY plan', !d.pm && d.h2 === 'התוכנית שלי' && d.pick === 'true', d);
const area = Number((d.sub.match(/([\d.]+) מ״ר/) || [])[1] || 0), want = 4.8 * 3.9 + 3.08 * 3.9;
ok('the floor area follows the walk within 3% (' + area + ' against ' + want.toFixed(1) + ' מ״ר)', Math.abs(area - want) / want < 0.03, d.sub);
await shot('6-designer-on-measured-plan');
ok('no errors in the console', errors.length === 0, errors.slice(0, 4));

ws.close(); chrome.kill(); await sleep(1200);
try { fs.rmSync(profile, { recursive: true, force: true, maxRetries: 5, retryDelay: 400 }); } catch (e) { /* the folder stays */ }
console.log('\n' + pass + ' passed, ' + fail + ' failed | shots: ' + SHOTS);
process.exit(fail ? 1 : 0);
