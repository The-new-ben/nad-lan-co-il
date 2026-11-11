// node check-call.mjs [--port=47961]
// Presses the designer's CALL (plugins/nadlan-config/assets/designer/call.js) on the MOCK transport: three pages in one headless
// Chrome (buyer on a phone, rep on a desktop, interior designer on a phone), then a late joiner. No server, no LiveKit, nothing
// on the live site. Serve the repo root first:  python -m http.server 47961 --bind 127.0.0.1   (from the repo root)
// What the numbers mean: times are measured INSIDE the pages on one clock (performance.timeOrigin + now), from the moment the
// sender sends to the moment the receiver's store has applied the change (plan and 3D patched). On one machine this is the
// software cost of the protocol; the network adds its own time on real phones (the live test plan in call/spec-had-706.md).
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const arg = (k, d) => { const a = process.argv.find((x) => x.startsWith('--' + k + '=')); return a ? a.split('=')[1] : d; };
const ROOM = 'chk' + Date.now().toString(36);
const URL0 = 'http://127.0.0.1:' + arg('port', '47961') + '/docs/design-lab/apartment-designer/call-harness.html';
const here = path.dirname(fileURLToPath(import.meta.url)), out = path.join(here, 'call-evidence');
fs.mkdirSync(out, { recursive: true });
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe', PORT = 9300 + Math.floor(Math.random() * 500), profile = path.join(os.tmpdir(), 'nd-call-' + PORT);
const chrome = spawn(CHROME, ['--headless=new', '--remote-debugging-port=' + PORT, '--user-data-dir=' + profile, '--no-first-run', '--disable-extensions', '--ignore-gpu-blocklist', '--enable-gpu', '--use-angle=d3d11', '--lang=he-IL',
  '--disable-background-timer-throttling', '--disable-renderer-backgrounding', '--disable-backgrounding-occluded-windows', '--autoplay-policy=no-user-gesture-required'], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
for (let i = 0; i < 80; i++) { try { if ((await fetch('http://127.0.0.1:' + PORT + '/json/version')).ok) break; } catch {} await sleep(250); }
const receipt = { when: new Date().toISOString(), task: 'HAD-706', transport: 'mock (BroadcastChannel, one browser)', room: ROOM, bars: { state_sync_p95_ms: 150, pen_handover_ms: 300 }, checks: [], numbers: {} }; let fails = 0;
const check = (name, ok, detail) => { receipt.checks.push({ name, ok: !!ok, detail }); if (!ok) fails++; console.log((ok ? 'ok   ' : 'FAIL ') + name + (detail !== undefined ? '  ' + (typeof detail === 'string' ? detail : JSON.stringify(detail)) : '')); };
const pct = (a, p) => { if (!a.length) return null; const s = [...a].sort((x, y) => x - y); return Math.round(s[Math.min(s.length - 1, Math.floor((p / 100) * s.length))] * 10) / 10; };

async function page(label, w, h, dpr, mobile, query) {
  const t = await (await fetch('http://127.0.0.1:' + PORT + '/json/new?about:blank', { method: 'PUT' })).json();
  const ws = new WebSocket(t.webSocketDebuggerUrl); let id = 0; const pend = new Map(), errors = [];
  ws.onmessage = (ev) => { const m = JSON.parse(ev.data); if (m.id && pend.has(m.id)) { pend.get(m.id)(m.result || m.error); pend.delete(m.id); } else if (m.method === 'Runtime.exceptionThrown') errors.push(m.params.exceptionDetails.text + ' ' + ((m.params.exceptionDetails.exception || {}).description || '')); else if (m.method === 'Runtime.consoleAPICalled' && m.params.type === 'error') errors.push(m.params.args.map((a) => a.value || a.description).join(' ')); };
  await new Promise((r) => (ws.onopen = r));
  const send = (method, params = {}) => new Promise((res) => { const i = ++id; pend.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); });
  const ev = async (e) => { const r = await send('Runtime.evaluate', { expression: e, awaitPromise: true, returnByValue: true }); if (r.exceptionDetails) throw new Error(label + ': ' + JSON.stringify(r.exceptionDetails.exception || r.exceptionDetails.text)); return r.result.value; };
  await send('Page.enable'); await send('Runtime.enable');
  await send('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: dpr, mobile });
  await send('Emulation.setFocusEmulationEnabled', { enabled: true });
  if (mobile) await send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
  await send('Page.navigate', { url: URL0 + '?room=' + ROOM + '&' + query + '&t=' + Date.now() });
  for (let i = 0; i < 200; i++) { if (await ev('!!window.__ready').catch(() => false)) break; await sleep(200); }
  const touch = (type, x, y) => send('Input.dispatchTouchEvent', { type, touchPoints: type === 'touchEnd' ? [] : [{ x, y, id: 1 }] });
  return {
    label, ev, errors,
    shot: async (name) => { const d = await send('Page.captureScreenshot', { format: 'png' }); fs.writeFileSync(path.join(out, name + '.png'), Buffer.from(d.data, 'base64')); },
    tap: async (x, y) => { await touch('touchStart', x, y); await sleep(40); await touch('touchEnd'); await sleep(140); },
    click: async (x, y) => { for (const type of ['mousePressed', 'mouseReleased']) await send('Input.dispatchMouseEvent', { type, x, y, button: 'left', clickCount: 1 }); await sleep(120); },
    hover: (x, y) => send('Input.dispatchMouseEvent', { type: 'mouseMoved', x, y }),
    drag: async (x0, y0, x1, y1, steps = 12) => { await touch('touchStart', x0, y0); await sleep(30); for (let i = 1; i <= steps; i++) { await touch('touchMove', x0 + ((x1 - x0) * i) / steps, y0 + ((y1 - y0) * i) / steps); await sleep(18); } await touch('touchEnd'); await sleep(140); },
    close: async () => { ws.close(); await fetch('http://127.0.0.1:' + PORT + '/json/close/' + t.id).catch(() => {}); },
  };
}
const R = 'document.getElementById("app").shadowRoot';
const mid = (sel) => `(()=>{const e=${R}.querySelector(${JSON.stringify(sel)});if(!e)return null;const r=e.getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]})()`;
const until = async (p, expr, ms = 3000) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await p.ev(expr).catch(() => false)) return true; await sleep(30); } return false; };
const designOf = (p) => p.ev('(()=>{const d=window.__d.store.design;return JSON.stringify({items:d.items.map(i=>[i.id,i.sku,i.x,i.y,i.rot]),finishes:d.finishes,walls:d.geometry.walls,rev:d.rev})})()');
const REFUSE = (n) => 'העט אצל ' + n + ' כרגע, ורק מי שמחזיק אותו משנה את העיצוב.';

let B, P, D, F;
try {
  // ---- three people join: the buyer first (alone, so she holds the pen), then the rep and the designer ----
  B = await page('buyer', 390, 844, 2.625, true, 'id=b1&name=' + encodeURIComponent('דנה') + '&role=buyer');
  P = await page('rep', 1366, 900, 1, false, 'id=r1&name=' + encodeURIComponent('אבי') + '&role=rep');
  D = await page('designer', 390, 844, 2.625, true, 'id=d1&name=' + encodeURIComponent('נועה') + '&role=designer');
  const all = [B, P, D];
  // three pages decode three.js and the furniture models at once on one machine, so a page can be busy for seconds:
  // wait (up to 15 s) until everyone agrees on the pen holder and the late two hold a design, and report how long it took
  const tj = Date.now();
  for (let k = 0; k < 150; k++) {
    const s = await Promise.all(all.map((p) => p.ev('({pen:window.__call.pen.holder,snap:!!window.__call.stats.snap,v:[...' + R + '.querySelectorAll(".ndc-tile video")].filter(v=>v.srcObject&&v.readyState>=2).length})')));
    if (s.every((x) => x.pen && x.pen === s[0].pen && x.v === 3) && s[1].snap && s[2].snap) break;
    await sleep(100);
  }
  receipt.numbers.join_settle_ms = Date.now() - tj;
  console.log('info all three agree after ' + receipt.numbers.join_settle_ms + ' ms (from the third page being ready)');
  const seen = await Promise.all(all.map((p) => p.ev('({n:window.__call.participants().length,pen:window.__call.pen.holder,vis:document.visibilityState,tiles:' + R + '.querySelectorAll(".ndc-tile").length,videos:[...' + R + '.querySelectorAll(".ndc-tile video")].filter(v=>v.srcObject&&v.readyState>=2).length})')));
  check('three people in the call, each sees three tiles with playing video', seen.every((s) => s.n === 3 && s.tiles === 3 && s.videos === 3), seen);
  check('the first one in holds the pen, and all three agree', seen.every((s) => s.pen === 'b1'), seen.map((s) => s.pen));
  const snaps = await Promise.all([P, D].map((p) => p.ev('window.__call.stats.snap')));
  check('the rep and the designer received the whole design on joining', snaps.every((s) => s && s.items > 0), snaps);

  // ---- layout: the phone strip never covers the 3D or the plan controls; on a desktop the dock sits at the side ----
  const lay = (p) => p.ev(`(()=>{const r=${R};const q=(s)=>{const e=r.querySelector(s);if(!e)return null;const b=e.getBoundingClientRect();return {l:b.left,t:b.top,r:b.right,b:b.bottom,w:b.width,h:b.height}};
    const small=[...r.querySelectorAll('.ndc button')].filter(b=>b.offsetParent).map(b=>{const x=b.getBoundingClientRect();return [b.dataset.ndc||b.textContent.trim().slice(0,12),Math.round(x.width),Math.round(x.height)]}).filter(a=>a[1]<44||a[2]<44);
    return {dock:q('.ndc'),space:q('[data-nd="space"]'),plan:q('[data-nd="plan"]'),nav:q('.nd nav'),chips:q('.chips'),undo:q('[data-nd="undo"]'),side:r.querySelector('.ndc').classList.contains('ndc-side'),vw:innerWidth,vh:innerHeight,small,scrollW:document.documentElement.scrollWidth}})()`);
  const hit = (a, b) => a && b && a.l < b.r - 1 && b.l < a.r - 1 && a.t < b.b - 1 && b.t < a.b - 1;
  const lb = await lay(B);
  check('phone 390: the call strip sits above the designer and covers neither the 3D, the plan, the view chips, undo nor the tool bar', !lb.side && !hit(lb.dock, lb.space) && !hit(lb.dock, lb.plan) && !hit(lb.dock, lb.chips) && !hit(lb.dock, lb.undo) && !hit(lb.dock, lb.nav) && lb.nav.b <= lb.vh + 1 && lb.scrollW <= lb.vw, { dock: lb.dock, space: lb.space, chips: lb.chips, undo: lb.undo, nav: lb.nav, scrollW: lb.scrollW, vw: lb.vw });
  check('phone 390: every call button is at least 44 x 44 px', lb.small.length === 0, lb.small);
  const lp = await lay(P);
  check('desktop 1366: the dock is a column at the side and covers neither view', lp.side && !hit(lp.dock, lp.space) && !hit(lp.dock, lp.plan) && !hit(lp.dock, lp.nav) && lp.small.length === 0, { dock: lp.dock, space: lp.space, plan: lp.plan, small: lp.small });
  await B.shot('c1-buyer-phone'); await P.shot('c2-rep-desktop'); await D.shot('c3-designer-phone');

  // ---- design sync: 100 moves by the pen holder reach the other two stores ----
  const moves = `(async()=>{const s=window.__d.store,i=s.item('i2'),x0=i.x,y0=i.y;for(let k=0;k<100;k++){s.apply({op:'item.move',id:'i2',x:x0+((k%20)-10)*3,y:y0+((k%14)-7)*3},{gesture:'chk'+k});await new Promise(r=>setTimeout(r,25));}return true})()`;
  // first round right after joining, while the furniture models still stream into the 3D views: reported, not the bar
  let w0 = await Promise.all([P, D].map((p) => p.ev('window.__call.stats.op.length')));
  await B.ev(moves); await sleep(600);
  const warm = []; for (const [i, p] of [P, D].entries()) warm.push(...(await p.ev('window.__call.stats.op.slice(' + w0[i] + ')')));
  receipt.numbers.op_while_models_load = { n: warm.length, p50_ms: pct(warm, 50), p95_ms: pct(warm, 95), max_ms: pct(warm, 100), note: 'receivers were still downloading and decoding furniture models (main thread busy)' };
  console.log('info while models load: ' + JSON.stringify(receipt.numbers.op_while_models_load));
  // the bar: every page has finished loading (no new network requests for 1.5 s)
  for (const p of all) { let last = -1, still = 0; for (let k = 0; k < 80 && still < 6; k++) { const n = await p.ev('performance.getEntriesByType("resource").length'); still = n === last ? still + 1 : 0; last = n; await sleep(250); } }
  await sleep(500);
  const n0 = await Promise.all([P, D].map((p) => p.ev('window.__call.stats.op.length')));
  await B.ev(moves);
  await sleep(600);
  const lat = [];
  for (const [i, p] of [P, D].entries()) lat.push(...(await p.ev('window.__call.stats.op.slice(' + n0[i] + ')')));
  const same = [await designOf(B), await designOf(P), await designOf(D)];
  const app = []; for (const [i, p] of [P, D].entries()) app.push(...(await p.ev('window.__call.stats.opApply.slice(' + n0[i] + ')')));
  receipt.numbers.op = { n: lat.length, p50_ms: pct(lat, 50), p95_ms: pct(lat, 95), max_ms: pct(lat, 100), apply_p50_ms: pct(app, 50), apply_p95_ms: pct(app, 95), series_ms: lat.map((x) => Math.round(x)) };
  check('100 moves by the pen holder arrive in both other stores (200 deliveries)', lat.length === 200, receipt.numbers.op);
  check('state sync p95 under the 150 ms bar', receipt.numbers.op.p95_ms !== null && receipt.numbers.op.p95_ms <= 150, receipt.numbers.op);
  check('after the moves the three designs are identical (items, floors, walls, revision)', same[0] === same[1] && same[1] === same[2], JSON.parse(same[0]).rev);
  // the same through a real finger on the buyer's plan
  let c = await B.ev(mid('[data-item="i2"] rect'));
  await B.drag(c[0], c[1], c[0] + 30, c[1] - 26);
  await sleep(400);
  const fd = await Promise.all(all.map((p) => p.ev('(()=>{const i=window.__d.store.item("i2");return [i.x,i.y,window.__d.space.placed("i2")[0]]})()')));
  check('a finger drag on the holder\'s plan moves the piece in all three plans and 3D views', fd.every((x) => x[0] === fd[0][0] && x[1] === fd[0][1] && x[2] === fd[0][0]), fd);
  const logBy = await P.ev('window.__d.store.design.log.slice(-1)[0].by');
  check('the receiver\'s decision log keeps the author\'s role, never a name', logBy === 'buyer', logBy);

  // ---- an edit by someone without the pen is refused with one Hebrew sentence ----
  const before = await designOf(B);
  const rf = await D.ev(`(()=>{const i=window.__d.store.item('i2');return window.__d.store.apply({op:'item.move',id:'i2',x:i.x+40,y:i.y})})()`);
  check('the designer\'s edit is refused while the buyer holds the pen', rf.ok === false && rf.code === 'call.pen' && rf.reason === REFUSE('דנה (קונה)'), rf);
  await sleep(3300);
  c = await D.ev(mid('[data-item="i2"] rect'));
  await D.drag(c[0], c[1], c[0] - 30, c[1] + 30);
  const toastD = await D.ev(`${R}.querySelector('[data-nd="toast"]').textContent`);
  const askBtn = await D.ev(`(()=>{const b=${R}.querySelector('[data-ndc="pen"]');return {text:b.textContent.trim(),visible:!!b.offsetParent}})()`);
  check('a finger drag without the pen shows the sentence and the "ask for the pen" button', toastD === REFUSE('דנה (קונה)') && askBtn.visible && askBtn.text === 'לבקש את העט', { toast: toastD, button: askBtn });
  await D.shot('c4-designer-refused');
  await sleep(200);
  check('the refused edit changed nothing anywhere', (await designOf(B)) === before && (await designOf(D)) === before && (await designOf(P)) === before);

  // ---- asking for the pen through the buttons: the designer asks, the buyer hands it over ----
  c = await D.ev(mid('[data-ndc="pen"]')); await D.tap(c[0], c[1]);
  const askSeen = await until(B, `!${R}.querySelector('[data-ndc="askbar"]').hidden`, 2000);
  const askText = await B.ev(`${R}.querySelector('[data-ndc="asktext"]').textContent`);
  await B.shot('c5-buyer-asked');
  c = await B.ev(mid('[data-ndc="askgive"]')); await B.tap(c[0], c[1]);
  const gotIt = await until(D, 'window.__call.pen.mine', 2000);
  check('ask, then hand over, through the buttons', askSeen && gotIt && askText === 'נועה (מעצב הפנים) מבקש/ת את העט', { askText, gotIt });
  const lb2 = await lay(B);
  check('the ask bar did not push the strip over the 3D', !hit(lb2.dock, lb2.space), { dock: lb2.dock, space: lb2.space });

  // ---- 50 handovers, measured inside the pages ----
  const order = [['d1', D], ['r1', P], ['b1', B]];
  const hand = [], rtt = [];
  let cur = 0; // the designer holds it now
  for (let k = 0; k < 50; k++) {
    const [, from] = order[cur], nx = (cur + 1) % 3, [toId, to] = order[nx];
    const n = await to.ev('window.__call.stats.pen.length');
    await from.ev(`window.__call.give(${JSON.stringify(toId)})`);
    if (!(await until(to, `window.__call.stats.pen.length>${n} && window.__call.pen.mine`, 2000))) { hand.push(NaN); break; }
    hand.push(await to.ev('window.__call.stats.pen.at(-1)'));
    cur = nx;
  }
  await sleep(300);
  for (const p of all) rtt.push(...(await p.ev('window.__call.stats.penRtt')));
  receipt.numbers.pen = { n: hand.length, p50_ms: pct(hand, 50), p95_ms: pct(hand, 95), max_ms: pct(hand, 100), round_trip_p50_ms: pct(rtt, 50), round_trip_p95_ms: pct(rtt, 95) };
  const agree = await Promise.all(all.map((p) => p.ev('window.__call.pen.holder')));
  check('50 handovers, each one message; all three agree on the holder at the end', hand.length === 50 && hand.every((x) => isFinite(x)) && agree.every((h) => h === agree[0]), { ...receipt.numbers.pen, holder: agree[0] });
  check('pen handover p95 under the 300 ms bar', receipt.numbers.pen.p95_ms !== null && receipt.numbers.pen.p95_ms <= 300, receipt.numbers.pen);
  const holderPage = order.find((o) => o[0] === agree[0])[1];
  const wOk = await holderPage.ev(`(()=>{const i=window.__d.store.item('i2');return window.__d.store.apply({op:'item.rot',id:'i2',rot:i.rot+90}).ok})()`);
  await sleep(300);
  check('after the handovers the new holder edits and the others follow', wOk && (await designOf(B)) === (await designOf(P)) && (await designOf(P)) === (await designOf(D)));

  // ---- follow me: the rep presents from the desktop; the phones follow; one looks away and comes back ----
  if (agree[0] !== 'r1') { await holderPage.ev('window.__call.give("r1")'); await until(P, 'window.__call.pen.mine', 2000); }
  const fv = await P.ev(`(()=>{const d=window.__d,f=d.store.derived.faceBy.living||d.store.derived.faces[0];const v={mode:'walk',x:Math.round((f.bb.x0+f.bb.x1)/2),y:Math.round((f.bb.y0+f.bb.y1)/2),yaw:0.7,pitch:0};d.setMode('walk');d.setView(v);return d.getView()})()`);
  await sleep(700);
  const views = await Promise.all([B, D].map((p) => p.ev('window.__d.getView()')));
  const near = (a, b) => a && b && a.mode === b.mode && Math.abs(a.x - b.x) < 3 && Math.abs(a.y - b.y) < 3 && Math.abs(a.yaw - b.yaw) < 0.02;
  check('follow me: both phones walk to where the rep stands, facing the same way', views.every((v) => near(v, fv)), { rep: fv, buyer: views[0], designer: views[1] });
  c = await D.ev(mid('[data-nd="space"] canvas')); await D.tap(c[0], c[1] - 60);
  const away = await D.ev('window.__call.following');
  const fv2 = await P.ev(`(()=>{const d=window.__d,v=d.getView();d.setView({...v,x:v.x+60,yaw:v.yaw+0.5});return d.getView()})()`);
  await sleep(700);
  const vB = await B.ev('window.__d.getView()'), vD = await D.ev('window.__d.getView()');
  const backBtn = await D.ev(`(()=>{const b=${R}.querySelector('[data-ndc="follow"]');return !!b.offsetParent})()`);
  await D.shot('c6-designer-looking-alone');
  c = await D.ev(mid('[data-ndc="follow"]')); if (c) await D.tap(c[0], c[1]);
  await sleep(500);
  const vD2 = await D.ev('window.__d.getView()');
  check('anyone can look away (a touch on the 3D) and come back with one button', away === false && near(vB, fv2) && !near(vD, fv2) && backBtn && near(vD2, fv2), { away, buyerFollows: near(vB, fv2), designerStayed: !near(vD, fv2), backBtn, back: near(vD2, fv2) });
  const vl = []; for (const p of [B, D]) vl.push(...(await p.ev('window.__call.stats.view')));
  receipt.numbers.view = { n: vl.length, p50_ms: pct(vl, 50), p95_ms: pct(vl, 95) };

  // ---- a pointer the others see, on the plan and on the 3D ----
  const pc = await P.ev(`(()=>{const s=${R}.querySelector('.nd-plan'),f=window.__d.store.derived.faceBy.living||window.__d.store.derived.faces[0];const q=new DOMPoint((f.bb.x0+f.bb.x1)/2,(f.bb.y0+f.bb.y1)/2).matrixTransform(s.getScreenCTM());return [q.x,q.y]})()`);
  for (let k = 0; k < 4; k++) { await P.hover(pc[0] + k * 6, pc[1] + k * 4); await sleep(90); }
  const ptrOk = await until(B, `[...${R}.querySelectorAll('.ndc-ptr')].filter(e=>!e.hidden).length>=1`, 1500);
  const ptrInfo = await B.ev(`[...${R}.querySelectorAll('.ndc-ptr')].map(e=>({hidden:e.hidden,label:e.textContent}))`);
  await B.shot('c7-buyer-sees-rep-pointer');
  check('the rep\'s pointer appears on the buyer\'s screen with his name', ptrOk && ptrInfo.some((x) => !x.hidden && x.label === 'אבי'), ptrInfo);

  // ---- raise hand and a short message ----
  await D.ev('window.__call.hand(true)'); await D.ev(`window.__call.chat('אפשר להזיז את הספה לחלון?')`);
  await sleep(300);
  const handOk = await B.ev(`!!${R}.querySelector('.ndc-tile[data-id="d1"] .ndc-m-hand')`);
  c = await B.ev(mid('[data-ndc="more"]')); await B.tap(c[0], c[1]);
  const msgs = await B.ev(`${R}.querySelector('[data-ndc="msgs"]').textContent`);
  const link = await B.ev(`${R}.querySelector('.ndc-link').value`);
  const noRec = await B.ev(`${R}.querySelector('.ndc-norec').textContent`);
  await B.shot('c8-buyer-panel');
  check('raise hand reaches the others', handOk);
  check('a message reaches the others', msgs.includes('אפשר להזיז את הספה לחלון?'), msgs);
  check('the invite link holds the room and no contact details or names', link.includes('room=' + ROOM) && !/[@]|\d{7,}|דנה|אבי|נועה|name=|phone|mail/i.test(link), link);
  check('a clear line says the call is not recorded', noRec === 'השיחה לא מוקלטת.', noRec);
  c = await B.ev(mid('[data-ndc="more"]')); await B.tap(c[0], c[1]);

  // ---- a dropped connection shows, then clears ----
  await B.ev('(async()=>{const p=window.__tr.simulateReconnect(700);await new Promise(r=>setTimeout(r,200));window.__rc=document.getElementById("app").shadowRoot.querySelector("[data-ndc=conn]").textContent;await p;return true})()');
  const rcText = await B.ev('window.__rc'), rcAfter = await B.ev(`${R}.querySelector('[data-ndc="conn"]').textContent`);
  check('reconnecting is shown in plain words and clears when back', rcText === 'החיבור נקטע, מתחברים שוב…' && rcAfter === '', { during: rcText, after: rcAfter });

  // ---- a late joiner receives the whole design ----
  await P.ev(`window.__d.store.apply({op:'finish.set',key:'floor:living',value:'oak-plank'})`);
  await sleep(200);
  F = await page('family', 390, 844, 2.625, true, 'id=f1&name=' + encodeURIComponent('רון') + '&role=family');
  await sleep(1200);
  const fSnap = await F.ev('window.__call.stats.snap'), dF = await designOf(F), dP = await designOf(P);
  receipt.numbers.late_joiner = fSnap;
  check('a late joiner gets the whole design from the pen holder (items, floors, walls, revision)', dF === dP && JSON.parse(dF).finishes['floor:living'] === 'oak-plank' && fSnap && fSnap.ms !== null, { snap: fSnap, rev: JSON.parse(dF).rev });
  check('the late joiner sees who holds the pen and cannot edit', (await F.ev('window.__call.pen.holder')) === 'r1' && (await F.ev(`window.__d.store.apply({op:'item.rot',id:'i2',rot:0}).ok`)) === false);

  // ---- leave cleans up; the pen held by the leaver passes to the rep ----
  await P.ev('window.__call.give("d1")'); await until(D, 'window.__call.pen.mine', 2000);
  c = await D.ev(mid('[data-ndc="leave"]')); await D.tap(c[0], c[1]);
  await until(D, 'window.__left', 2000);
  const dl = await D.ev(`(()=>{const r=${R};return {dock:!!r.querySelector('.ndc'),ptrs:!!r.querySelector('.ndc-ptrs'),top:r.querySelector('.nd').style.top,end:r.querySelector('.nd').style.insetInlineEnd,free:window.__d.store.apply({op:'item.rot',id:'i2',rot:180}).ok}})()`);
  check('leave removes the dock, gives the designer back the full screen and lifts the pen rule', !dl.dock && !dl.ptrs && dl.top === '' && dl.end === '' && dl.free, dl);
  const afterLeave = await until(P, 'window.__call.participants().length===3 && window.__call.pen.mine', 3000);
  const others = await Promise.all([B, P, F].map((p) => p.ev('({n:window.__call.participants().length,pen:window.__call.pen.holder})')));
  check('the others see three people and the pen went to the rep', afterLeave && others.every((o) => o.n === 3 && o.pen === 'r1'), others);
  await P.shot('c9-rep-after-leave');

  for (const p of [B, P, D, F]) check('no page errors (' + p.label + ')', p.errors.length === 0, p.errors);
  receipt.numbers.summaries = {};
  for (const p of [B, P, F]) receipt.numbers.summaries[p.label] = await p.ev('window.__call.summary()');
} catch (e) { console.error(e); fails++; receipt.error = String(e && e.stack || e); for (const p of [B, P, D, F]) if (p && p.errors.length) console.error(p.label + ' page errors:', p.errors.slice(0, 5)); }
receipt.passed = receipt.checks.filter((c) => c.ok).length; receipt.failed = fails;
fs.writeFileSync(path.join(out, 'receipt.json'), JSON.stringify(receipt, null, 2));
console.log('\nnumbers ' + JSON.stringify({ op: receipt.numbers.op, pen: receipt.numbers.pen, view: receipt.numbers.view, late: receipt.numbers.late_joiner }));
console.log(receipt.passed + ' passed, ' + fails + ' failed');
for (const p of [B, P, D, F]) if (p) await p.close().catch(() => {});
chrome.kill(); await sleep(300); try { fs.rmSync(profile, { recursive: true, force: true }); } catch {}
process.exit(fails ? 1 : 0);
