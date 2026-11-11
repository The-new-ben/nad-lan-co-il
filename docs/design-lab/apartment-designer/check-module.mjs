// node check-module.mjs [--port=47961]
// Presses the PLUGIN module (plugins/nadlan-config/assets/designer/) inside a stand-in project page with hostile site CSS.
// Serve the repo root first:  python -m http.server 47961 --bind 127.0.0.1   (run from the repo root)
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const arg = (k, d) => { const a = process.argv.find((x) => x.startsWith('--' + k + '=')); return a ? a.split('=')[1] : d; };
const URL0 = 'http://127.0.0.1:' + arg('port', '47961') + '/docs/design-lab/apartment-designer/module-harness.html';
const here = path.dirname(fileURLToPath(import.meta.url)), out = path.join(here, 'module-evidence');
fs.mkdirSync(out, { recursive: true });
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe', PORT = 9300 + Math.floor(Math.random() * 500), profile = path.join(os.tmpdir(), 'nd-mod-' + PORT);
const chrome = spawn(CHROME, ['--headless=new', '--remote-debugging-port=' + PORT, '--user-data-dir=' + profile, '--no-first-run', '--disable-extensions', '--ignore-gpu-blocklist', '--enable-gpu', '--use-angle=d3d11', '--lang=he-IL'], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
for (let i = 0; i < 80; i++) { try { if ((await fetch('http://127.0.0.1:' + PORT + '/json/version')).ok) break; } catch {} await sleep(250); }
const receipt = { when: new Date().toISOString(), checks: [] }; let fails = 0;
const check = (name, ok, detail) => { receipt.checks.push({ name, ok: !!ok, detail }); if (!ok) fails++; console.log((ok ? 'ok   ' : 'FAIL ') + name + (detail !== undefined ? '  ' + (typeof detail === 'string' ? detail : JSON.stringify(detail)) : '')); };

async function page(w, h, dpr, mobile, query) {
  const t = await (await fetch('http://127.0.0.1:' + PORT + '/json/new?about:blank', { method: 'PUT' })).json();
  const ws = new WebSocket(t.webSocketDebuggerUrl); let id = 0; const pend = new Map(), errors = [];
  ws.onmessage = (ev) => { const m = JSON.parse(ev.data); if (m.id && pend.has(m.id)) { pend.get(m.id)(m.result || m.error); pend.delete(m.id); } else if (m.method === 'Runtime.exceptionThrown') errors.push(m.params.exceptionDetails.text + ' ' + ((m.params.exceptionDetails.exception || {}).description || '')); else if (m.method === 'Runtime.consoleAPICalled' && m.params.type === 'error') errors.push(m.params.args.map((a) => a.value || a.description).join(' ')); };
  await new Promise((r) => (ws.onopen = r));
  const send = (method, params = {}) => new Promise((res) => { const i = ++id; pend.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); });
  const ev = async (e) => { const r = await send('Runtime.evaluate', { expression: e, awaitPromise: true, returnByValue: true }); if (r.exceptionDetails) throw new Error(JSON.stringify(r.exceptionDetails.exception || r.exceptionDetails.text)); return r.result.value; };
  await send('Page.enable'); await send('Runtime.enable');
  await send('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: dpr, mobile });
  if (mobile) await send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
  await send('Page.navigate', { url: URL0 + '?' + query + '&t=' + Date.now() });
  for (let i = 0; i < 160; i++) { if (await ev('!!window.__ready').catch(() => false)) break; await sleep(250); }
  const touch = (type, x, y) => send('Input.dispatchTouchEvent', { type, touchPoints: type === 'touchEnd' ? [] : [{ x, y, id: 1 }] });
  return {
    ev, errors,
    shot: async (name) => { const d = await send('Page.captureScreenshot', { format: 'png' }); fs.writeFileSync(path.join(out, name + '.png'), Buffer.from(d.data, 'base64')); },
    tap: async (x, y) => { await touch('touchStart', x, y); await sleep(40); await touch('touchEnd'); await sleep(140); },
    drag: async (x0, y0, x1, y1, steps = 12) => { await touch('touchStart', x0, y0); await sleep(30); for (let i = 1; i <= steps; i++) { await touch('touchMove', x0 + ((x1 - x0) * i) / steps, y0 + ((y1 - y0) * i) / steps); await sleep(18); } await touch('touchEnd'); await sleep(140); },
    close: async () => { ws.close(); await fetch('http://127.0.0.1:' + PORT + '/json/close/' + t.id).catch(() => {}); },
  };
}
const R = 'document.getElementById("sheet").shadowRoot';
const mid = (sel) => `(()=>{const r=${R}.querySelector(${JSON.stringify(sel)}).getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]})()`;

try {
  // ---- phone: the full-screen sheet opened from a project page ----
  let p = await page(390, 844, 2.625, true, 'inline=0');
  let c = await p.ev('(()=>{const r=document.getElementById("open").getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]})()');
  await p.tap(c[0], c[1]);
  for (let i = 0; i < 120; i++) { if (await p.ev('!!(window.__d && window.__d.timings.first_3d_frame_ms)').catch(() => false)) break; await sleep(250); }
  await sleep(1300);
  const t = await p.ev('window.__d.timings');
  check('opens from the page button: plan first, then 3D', t.plan_ms < t.space_ms && t.first_3d_frame_ms > 0, { plan_ms: Math.round(t.plan_ms), first_3d_frame_ms: Math.round(t.first_3d_frame_ms) });
  const st = await p.ev(`(()=>{const b=${R}.querySelector('[data-nd="undo"]'),h=${R}.querySelector('header h2'),cs=getComputedStyle(b),hs=getComputedStyle(h);return {radius:cs.borderRadius,bg:cs.backgroundColor,font:hs.fontFamily,h2color:hs.color,h2size:hs.fontSize,spacing:cs.letterSpacing}})()`);
  check('the site CSS does not reach the designer (radius, colours, fonts)', st.radius === '0px' && st.bg !== 'rgb(238, 51, 51)' && st.h2color === 'rgb(15, 34, 51)' && st.h2size === '15px' && /Plex/.test(st.font), st);
  check('fills the phone screen, no horizontal scroll', await p.ev(`(()=>{const r=${R}.querySelector('.nd').getBoundingClientRect();return Math.round(r.width)===innerWidth&&Math.round(r.height)===innerHeight&&document.documentElement.scrollWidth<=innerWidth})()`));
  await p.shot('m1-phone-sheet');
  c = await p.ev(mid('[data-item="i2"] rect'));
  const b0 = await p.ev('(()=>{const i=window.__d.store.item("i2");return [i.x,i.y]})()');
  await p.drag(c[0], c[1], c[0] - 28, c[1] + 36);
  const a0 = await p.ev('(()=>{const i=window.__d.store.item("i2");return {model:[i.x,i.y],three:window.__d.space.placed("i2")}})()');
  check('finger drag on the plan moves the piece in the model and in 3D', a0.model[0] !== b0[0] && a0.three[0] === a0.model[0] && a0.three[1] === a0.model[1], { before: b0, ...a0 });
  c = await p.ev(mid('.hit[data-wall="m4"]'));
  await p.drag(c[0], c[1], c[0] + 14, c[1], 4);
  check('a fixed wall explains itself', (await p.ev(`${R}.querySelector('[data-nd="toast"]').textContent`)).includes('ממ״ד'));
  await sleep(3300);
  const pr = await p.ev(`(()=>{const s=${R}.querySelector('.nd-plan'),m=s.getScreenCTM();const q=new DOMPoint(120,120).matrixTransform(m);return [q.x,q.y]})()`);
  await p.tap(pr[0], pr[1]);
  c = await p.ev(`(()=>{const b=[...${R}.querySelectorAll('.sheet .opt')].find(b=>b.textContent.includes('פרקט'));const r=b.getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]})()`);
  await p.tap(c[0], c[1]);
  const fl = await p.ev('({model:window.__d.store.floorOf("living"),three:window.__d.space.floorKey("living"),boq:window.__d.quantities().floors["oak-plank"]})');
  check('floor choice reaches the model, the 3D material and the quantities', fl.model === 'oak-plank' && fl.three === 'oak-plank' && fl.boq > 20, fl);
  c = await p.ev(mid('[data-nd="send"]')); await p.tap(c[0], c[1]);
  const sent = await p.ev('({n:window.__sent.length,schema:window.__sent[0]&&window.__sent[0].schema,v:window.__sent[0]&&window.__sent[0].v,floor:window.__sent[0]&&window.__sent[0].finishes["floor:living"]})');
  check('"send" hands the host a nadlan-unit-design v2 document', sent.n === 1 && sent.schema === 'nadlan-unit-design' && sent.v === 2 && sent.floor === 'oak-plank', sent);
  await p.shot('m2-phone-floor-sent');
  c = await p.ev(mid('[data-nd="close"]')); await p.tap(c[0], c[1]);
  check('close removes the designer and frees the page', await p.ev('document.getElementById("sheet").hidden && document.getElementById("sheet").shadowRoot.childNodes.length===0 && window.__d===null'));
  // save and return: open again in the same browser, the design is still there, with no personal details in what was stored
  c = await p.ev('(()=>{const r=document.getElementById("open").getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]})()');
  await p.tap(c[0], c[1]);
  for (let i = 0; i < 120; i++) { if (await p.ev('!!(window.__d && window.__d.timings.first_3d_frame_ms)').catch(() => false)) break; await sleep(250); }
  await sleep(600);
  const back = await p.ev(`(()=>{const k=Object.keys(localStorage).filter(k=>k.startsWith('nd-design:'));const raw=localStorage.getItem(k[0])||'';return {restored:window.__d.restored,floor:window.__d.store.floorOf('living'),sofa:window.__d.store.item('i2').x,keys:k.length,bytes:raw.length,personal:/name|phone|email|@/i.test(raw.replace(/"name_he"/g,''))}})()`);
  check('the design is still there on return (saved on the device, no personal details)', back.restored === true && back.floor === 'oak-plank' && back.sofa === a0.model[0] && back.keys === 1 && !back.personal, back);
  await p.ev(`${R}.querySelector('nav button[data-sheet="boq"]').click()`); await sleep(300);
  await p.ev(`${R}.querySelector('[data-nd="reset"]').scrollIntoView({block:'center'})`); await sleep(250); // the button sits at the end of the sheet: scroll to it as a person would
  c = await p.ev(mid('[data-nd="reset"]')); await p.tap(c[0], c[1]); await sleep(500);
  const reset = await p.ev('({floor:window.__d.store.floorOf("living"),sofa:window.__d.store.item("i2").x,three:window.__d.space.placed("i2"),floor3:window.__d.space.floorKey("living")})');
  check('"start over" returns the apartment as it was, in the model and in 3D', reset.floor === 'porcelain-80' && reset.sofa === b0[0] && reset.three[0] === b0[0] && reset.floor3 === 'porcelain-80', reset);
  check('no page errors (phone)', p.errors.length === 0, p.errors);
  await p.close();

  // ---- desktop: embedded inside the page, English strings ----
  p = await page(1366, 900, 1, false, 'lang=en');
  for (let i = 0; i < 120; i++) { if (await p.ev('!!(window.__i && window.__i.timings.first_3d_frame_ms)').catch(() => false)) break; await sleep(250); }
  await sleep(1300);
  const en = await p.ev(`(()=>{const r=document.getElementById("inline").shadowRoot;return {dir:r.querySelector('.nd').dir,title:r.querySelector('header h2').textContent,tool:r.querySelector('nav button').textContent,box:[Math.round(r.querySelector('.nd').getBoundingClientRect().width),Math.round(r.querySelector('.nd').getBoundingClientRect().height)]}})()`);
  check('embeds inside a page block, English strings, left to right', en.dir === 'ltr' && en.title === 'Design the apartment' && en.tool === 'Furniture' && en.box[1] === 640, en);
  await p.ev('document.getElementById("inline").scrollIntoView()'); await sleep(300);
  await p.shot('m3-desktop-inline-en');
  check('no page errors (desktop)', p.errors.length === 0, p.errors);
  await p.close();
} catch (e) { console.error(e); fails++; receipt.error = String(e); }
receipt.passed = receipt.checks.filter((c) => c.ok).length; receipt.failed = fails;
fs.writeFileSync(path.join(out, 'receipt.json'), JSON.stringify(receipt, null, 2));
console.log('\n' + receipt.passed + ' passed, ' + fails + ' failed');
chrome.kill(); await sleep(300); try { fs.rmSync(profile, { recursive: true, force: true }); } catch {}
process.exit(fails ? 1 : 0);
