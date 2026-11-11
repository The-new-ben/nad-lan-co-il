// node docs/design-lab/apartment-designer/check-roomscan.mjs [--port=47961]
// Presses the REAL buttons of roomscan.js in headless Chrome (390 x 844, touch) with a stand-in navigator.xr
// (roomscan-xrmock.js): a scripted walk through a 3-room apartment, then compares the plan with the apartment.
// Serve the repo root first:  python -m http.server 47961 --bind 127.0.0.1   (from the repo root)
// What this does NOT prove: that a real phone's camera tracking, hit tests and anchors behave like the stand-in.
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const arg = (k, d) => { const a = process.argv.find((x) => x.startsWith('--' + k + '=')); return a ? a.split('=')[1] : d; };
const URL0 = 'http://127.0.0.1:' + arg('port', '47961') + '/docs/design-lab/apartment-designer/roomscan-harness.html';
const out = arg('out', 'C:/Users/777/AppData/Local/Temp/claude/231dc6a3026aa599/5993fcd7-ed7e-4647-92f4-08ef43220a4d/scratchpad/scan');
fs.mkdirSync(out, { recursive: true });
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe', PORT = 9300 + Math.floor(Math.random() * 500), profile = path.join(os.tmpdir(), 'nd-scan-' + PORT);
const chrome = spawn(CHROME, ['--headless=new', '--remote-debugging-port=' + PORT, '--user-data-dir=' + profile, '--no-first-run', '--disable-extensions', '--ignore-gpu-blocklist', '--enable-gpu', '--use-angle=d3d11', '--lang=he-IL'], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
for (let i = 0; i < 80; i++) { try { if ((await fetch('http://127.0.0.1:' + PORT + '/json/version')).ok) break; } catch {} await sleep(250); }
let pass = 0, fail = 0;
const check = (name, ok, detail) => { if (ok) pass++; else fail++; console.log((ok ? 'ok   ' : 'FAIL ') + name + (detail !== undefined ? '  ' + (typeof detail === 'string' ? detail : JSON.stringify(detail)) : '')); };

async function page(query) {
  const t = await (await fetch('http://127.0.0.1:' + PORT + '/json/new?about:blank', { method: 'PUT' })).json();
  const ws = new WebSocket(t.webSocketDebuggerUrl); let id = 0; const pend = new Map(), errors = [], warns = [];
  ws.onmessage = (ev) => {
    const m = JSON.parse(ev.data);
    if (m.id && pend.has(m.id)) { pend.get(m.id)(m.result || m.error); pend.delete(m.id); }
    else if (m.method === 'Runtime.exceptionThrown') errors.push(m.params.exceptionDetails.text + ' ' + ((m.params.exceptionDetails.exception || {}).description || ''));
    else if (m.method === 'Runtime.consoleAPICalled' && m.params.type === 'error') errors.push(m.params.args.map((a) => a.value || a.description).join(' '));
    else if (m.method === 'Runtime.consoleAPICalled' && m.params.type === 'warning') warns.push(m.params.args.map((a) => a.value || a.description).join(' '));
    else if (m.method === 'Log.entryAdded' && m.params.entry.level === 'error' && !/favicon/.test(m.params.entry.url || '')) errors.push('log: ' + m.params.entry.text + ' ' + (m.params.entry.url || ''));
  };
  await new Promise((r) => (ws.onopen = r));
  const send = (method, params = {}) => new Promise((res) => { const i = ++id; pend.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); });
  const ev = async (e) => { const r = await send('Runtime.evaluate', { expression: e, awaitPromise: true, returnByValue: true }); if (r.exceptionDetails) throw new Error(JSON.stringify(r.exceptionDetails.exception || r.exceptionDetails.text)); return r.result.value; };
  await send('Page.enable'); await send('Runtime.enable'); await send('Log.enable');
  await send('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 2, mobile: true });
  await send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
  await send('Page.navigate', { url: URL0 + '?' + query + '&t=' + Date.now() });
  for (let i = 0; i < 120; i++) { if (await ev('!!window.__ready').catch(() => false)) break; await sleep(250); }
  const touch = (type, x, y) => send('Input.dispatchTouchEvent', { type, touchPoints: type === 'touchEnd' ? [] : [{ x, y, id: 1 }] });
  return {
    ev, errors, warns,
    shot: async (name, clip) => { const d = await send('Page.captureScreenshot', { format: 'png', ...(clip ? { clip: { ...clip, scale: 2 } } : {}) }); fs.writeFileSync(path.join(out, name + '.png'), Buffer.from(d.data, 'base64')); },
    tap: async (x, y) => { await touch('touchStart', x, y); await sleep(40); await touch('touchEnd'); await sleep(120); },
    close: async () => { ws.close(); await fetch('http://127.0.0.1:' + PORT + '/json/close/' + t.id).catch(() => {}); },
  };
}
const SH = 'document.querySelector(".nlscan-host").shadowRoot';
const centre = (expr) => `(()=>{const e=${expr};if(!e)return null;const r=e.getBoundingClientRect();return r.width?[r.left+r.width/2,r.top+r.height/2]:null})()`;
async function tapEl(p, expr, label) { const c = await p.ev(centre(expr)); if (!c) throw new Error('not on screen: ' + label); await p.tap(c[0], c[1]); }
async function until(p, expr, ms = 4000) { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await p.ev(expr).catch(() => false)) return true; await sleep(60); } return false; }
const OV = 'document.querySelector(".nlscan-root")';
const K = (k) => `${OV}.querySelector('[data-k="${k}"]')`;
const msg = (p) => p.ev(`${OV}.querySelector('[data-r="msg"]').textContent`);

// ---- the apartment the script walks (plan cm, centre lines: walls 25 outside, 12 and 10 inside) and its inner faces ----
const ANG = (23 * Math.PI) / 180, OFF = [-2.1, -3.4];
const W = (p) => { const x = p[0] / 100, y = p[1] / 100; return [x * Math.cos(ANG) - y * Math.sin(ANG) + OFF[0], x * Math.sin(ANG) + y * Math.cos(ANG) + OFF[1]]; };
const ROOMS = [
  { key: 'living', label: 'סלון', pts: [[12.5, 12.5], [494, 12.5], [494, 407.5], [12.5, 407.5]], area: 4.815 * 3.95 },
  { key: 'bedroom', label: 'חדר שינה', pts: [[506, 12.5], [815, 12.5], [815, 407.5], [506, 407.5]], area: 3.09 * 3.95 },
  { key: 'bedroom', label: 'חדר שינה', pts: [[825, 12.5], [1087.5, 12.5], [1087.5, 407.5], [825, 407.5]], area: 2.625 * 3.95 },
];
const jit = (k) => [Math.sin(k * 3.1) * 0.8, Math.cos(k * 1.9) * 0.8]; // a steady hand: under a centimetre
let step = 0;
async function aim(p, pt) { const j = jit(step++), w = W([pt[0] + j[0], pt[1] + j[1]]); await p.ev(`__mock.aim=[${w[0]},${w[1]}]`); }
async function mark(p, pt, label) {
  await aim(p, pt); await sleep(150);
  const sig = `${OV}.querySelector('[data-r="count"]').textContent+'|'+${OV}.querySelector('[data-r="msg"]').textContent`;
  for (let i = 0; i < 3; i++) {
    const ok = await until(p, `!${K('corner')}.disabled`, 4000);
    if (!ok) throw new Error('the main button never became active for ' + label + ' (message: ' + (await msg(p)) + ')');
    await sleep(140); const s0 = await p.ev(sig);
    await tapEl(p, K('corner'), label);
    if (await until(p, `${sig}!==${JSON.stringify(s0)}`, 2000)) return;
  }
  throw new Error('the press did not mark ' + label);
}
const count = (p) => p.ev(`${OV}.querySelector('[data-r="count"]').textContent`);

try {
  // ======== 1. the explanation screen ========
  let p = await page('mode=ok');
  check('the harness loaded and the device reads as supported', await p.ev('window.__supported && window.__supported.ok === true'), await p.ev('window.__supported'));
  const intro = await p.ev(`(()=>{const s=${SH};return {h:s.querySelector('h2').textContent,steps:[...s.querySelectorAll('.nlscan-steps li')].map(l=>l.textContent),fine:[...s.querySelectorAll('.nlscan-fine')].map(x=>x.textContent),go:(s.querySelector('[data-a="start"]')||{}).textContent,svgs:s.querySelectorAll('.nlscan-steps svg').length}})()`);
  check('intro: the title', intro.h === 'מודדים את הדירה במצלמה', intro.h);
  check('intro: the three steps, each with its drawing', intro.steps.length === 3 && intro.svgs === 3 && /לרצפה עד שמופיע סימון/.test(intro.steps[0]) && /ולוחצים פינה/.test(intro.steps[1]) && /והתוכנית נפתחת/.test(intro.steps[2]), intro.steps);
  check('intro: Chrome on Android, good light, the picture stays on the device', intro.fine.includes('עובד בכרום באנדרואיד. צריך אור טוב.') && intro.fine.includes('הצילום נשאר במכשיר. שום תמונה לא נשמרת ולא נשלחת.'), intro.fine);
  check('intro: the start button', intro.go === 'להתחיל מדידה', intro.go);
  const look = await p.ev(`(()=>{const s=${SH},b=s.querySelector('[data-a="start"]'),cs=getComputedStyle(b),h=getComputedStyle(s.querySelector('h2'));return {radius:cs.borderRadius,bg:cs.backgroundColor,h:b.getBoundingClientRect().height,font:h.fontFamily,color:h.color,size:h.fontSize}})()`);
  check('intro: the site CSS does not reach it (square corners, own colours, Plex)', look.radius === '0px' && look.bg === 'rgb(31, 95, 168)' && look.color === 'rgb(15, 34, 51)' && look.size === '19px' && /Plex/.test(look.font) && look.h >= 56, look);
  check('intro: no horizontal scroll at 390 px', await p.ev('document.documentElement.scrollWidth<=innerWidth'));
  await sleep(500); await p.shot('01-intro');

  // ======== 2. measuring ========
  await tapEl(p, `${SH}.querySelector('[data-a="start"]')`, 'start');
  check('the camera opens from the press (an immersive-ar session with hit-test and dom-overlay required, anchors optional)', await until(p, `!!__mock.session && ${OV} && ${OV}.style.display===''`, 8000), await p.ev('__mock.requested'));
  const req = await p.ev('__mock.requested');
  check('session request shape', req && req.mode === 'immersive-ar' && req.init.requiredFeatures.join() === 'hit-test,dom-overlay' && req.init.optionalFeatures.join() === 'anchors' && req.init.domOverlayRoot, req);
  check('the overlay root sits directly under body, not in a shadow root', await p.ev(`${OV}.parentNode===document.body`));
  check('the hit test runs from the viewer (centre of the screen)', await p.ev('__mock.hitSpace==="viewer"'));
  await until(p, `${OV}.querySelector('[data-r="msg"]').textContent.length>0`, 2000);
  check('before the floor is found: point at the floor', /מכוונים את הטלפון לרצפה/.test(await msg(p)), await msg(p));
  const bt = await p.ev(`[...${OV}.querySelectorAll('.nlscan-bar .nlscan-btn')].map(b=>{const r=b.getBoundingClientRect(),cs=getComputedStyle(b);return {t:b.textContent,h:Math.round(r.height),w:Math.round(r.width),rad:cs.borderRadius,bottom:Math.round(r.bottom)}})`);
  check('six big buttons at the bottom: פינה ביטול סגירת חדר דלת חלון סיום, 56 px or more, square', bt.length === 6 && ['פינה', 'ביטול', 'סגירת חדר', 'דלת', 'חלון', 'סיום'].every((t) => bt.some((b) => b.t === t)) && bt.every((b) => b.h >= 56 && b.rad === '0px' && b.bottom <= 844), bt);
  check('the corner button is off while nothing is under the marker', await p.ev(`${K('corner')}.disabled`));
  // room 1, with one wrong corner undone on the way
  const r1 = ROOMS[0];
  await mark(p, r1.pts[0], 'living corner 1');
  check('first corner marked, the floor is locked', (await count(p)).includes('פינה אחת'), await count(p));
  await mark(p, r1.pts[1], 'living corner 2');
  await mark(p, [300, 200], 'a wrong corner');
  await tapEl(p, K('undo'), 'undo');
  check('undo takes the wrong corner back', /2 פינות/.test(await count(p)), await count(p));
  await aim(p, [494, 300]); await until(p, `!${K('corner')}.disabled`); await sleep(450);
  const dist = await p.ev(`${OV}.querySelector('[data-r="dist"]').textContent`);
  check('live distance from the last corner, in metres (2.88 m along the wall)', /^2\.(8[5-9]|9[0-1]) מ׳$/.test(dist), dist);
  await mark(p, r1.pts[2], 'living corner 3');
  await mark(p, r1.pts[3], 'living corner 4');
  // a table top is not the floor
  await p.ev('__mock.table=true'); await aim(p, [250, 200]);
  check('a surface 70 cm up is refused: "not the floor"', await until(p, `/זה לא הרצפה/.test(${OV}.querySelector('[data-r="msg"]').textContent)`, 2500), await msg(p));
  await p.ev('__mock.table=false');
  await aim(p, [14, 15]);
  check('aiming at the first corner says the room can be closed', await until(p, `/הסימון על הפינה הראשונה/.test(${OV}.querySelector('[data-r="msg"]').textContent)`, 2500), await msg(p));
  await tapEl(p, K('close'), 'close room');
  check('closing offers the names in one tap', await until(p, `!${OV}.querySelector('[data-r="names"]').hidden`), await p.ev(`[...${OV}.querySelectorAll('[data-name]')].map(b=>b.textContent)`));
  const names = await p.ev(`[...${OV}.querySelectorAll('[data-name]')].map(b=>b.textContent)`);
  check('the names: סלון מטבח חדר שינה ממ״ד רחצה מרפסת מסדרון דילוג', names.join('|') === 'סלון|מטבח|חדר שינה|ממ״ד|רחצה|מרפסת|מסדרון|דילוג', names);
  await sleep(300); await p.shot('02-names');
  await tapEl(p, `${OV}.querySelector('[data-name="living"]')`, 'name living');
  check('room 2 starts', /חדר 2/.test(await count(p)), await count(p));
  // a door between the living room and bedroom 1, marked from the living room side
  await tapEl(p, K('door'), 'door');
  check('door mode asks for one side, the main button reads סימון', /דלת: מכוונים לצד אחד/.test(await msg(p)) && (await p.ev(`${K('corner')}.textContent`)) === 'סימון', await msg(p));
  await mark(p, [494, 110], 'door side 1');
  check('then the other side', /לצד השני של הפתח/.test(await msg(p)), await msg(p));
  await mark(p, [494, 190], 'door side 2');
  // room 2; one corner with no surface found (the floor plane carries it)
  const r2 = ROOMS[1];
  await mark(p, r2.pts[0], 'bedroom corner 1');
  await p.ev('__mock.noHit=true');
  await mark(p, r2.pts[1], 'bedroom corner 2 (no surface found, the floor plane is used)');
  await p.ev('__mock.noHit=false');
  await mark(p, r2.pts[2], 'bedroom corner 3');
  await mark(p, r2.pts[3], 'bedroom corner 4');
  await tapEl(p, K('close'), 'close room 2');
  await until(p, `!${OV}.querySelector('[data-r="names"]').hidden`);
  await tapEl(p, `${OV}.querySelector('[data-name="bedroom"]')`, 'name bedroom');
  // a window on the outside wall of bedroom 1
  await tapEl(p, K('window'), 'window');
  await mark(p, [590, 12.5], 'window side 1');
  await mark(p, [710, 12.5], 'window side 2');
  // room 3: two corners, then the screenshots, then tracking lost
  const r3 = ROOMS[2];
  await mark(p, r3.pts[0], 'room 3 corner 1');
  await mark(p, r3.pts[1], 'room 3 corner 2');
  await aim(p, [1087.5, 300]); await until(p, `!${K('corner')}.disabled`); await sleep(400);
  await p.shot('03-measuring');
  const mapR = await p.ev(`(()=>{const r=${OV}.querySelector('[data-r="map"]').getBoundingClientRect();return {x:r.left,y:r.top,width:r.width,height:r.height}})()`);
  check('the small map is in a top corner, 132 px', Math.round(mapR.width) === 132 && mapR.y < 300, mapR);
  const ink = await p.ev(`(()=>{const c=${OV}.querySelector('[data-r="map"]'),g=c.getContext('2d'),d=g.getImageData(0,0,c.width,c.height).data;let blue=0,red=0;for(let i=0;i<d.length;i+=4){if(d[i]<60&&d[i+1]>80&&d[i+1]<110&&d[i+2]>150)blue++;if(d[i]>160&&d[i+1]<70&&d[i+2]<70)red++;}return {blue,red}})()`);
  check('the small map draws what was measured (blue rooms) with wall lengths (red)', ink.blue > 200 && ink.red > 30, ink);
  await p.shot('04-minimap', mapR);
  await p.ev('__mock.lost=true');
  check('tracking lost: a plain message, nothing measured is lost', await until(p, `!${OV}.querySelector('[data-r="warn"]').hidden`, 2500) && /חדר 3 · 2 פינות/.test(await count(p)), await p.ev(`${OV}.querySelector('[data-r="warn"]').textContent`));
  check('tracking lost: the corner button is off', await p.ev(`${K('corner')}.disabled`));
  await sleep(200); await p.shot('05-lost');
  await p.ev('__mock.lost=false');
  check('tracking back: the message goes', await until(p, `${OV}.querySelector('[data-r="warn"]').hidden`, 2500));
  await mark(p, r3.pts[2], 'room 3 corner 3');
  await mark(p, r3.pts[3], 'room 3 corner 4');
  // finish with the last room still open: it is closed and named first
  await tapEl(p, K('finish'), 'finish');
  check('finish with an open room asks its name first', await until(p, `!${OV}.querySelector('[data-r="names"]').hidden`));
  await tapEl(p, `${OV}.querySelector('[data-name="bedroom"]')`, 'name room 3');

  // ======== 3. the result ========
  check('the session ends and the overlay is removed from the page', await until(p, `__mock.ended && !document.querySelector('.nlscan-root')`, 4000));
  check('the hit-test source is cancelled and every anchor deleted', await p.ev('__mock.hitCancelled && __mock.anchors.every(a=>a.deleted)'), await p.ev('({c:__mock.hitCancelled,live:__mock.anchors.filter(a=>!a.deleted).length})'));
  await until(p, `!!${SH}.querySelector('.nlscan-plan svg')`, 3000);
  const res = await p.ev(`(()=>{const s=${SH};return {h:s.querySelector('h2').textContent,sum:s.querySelector('.nlscan-sum').textContent,truth:s.querySelector('.nlscan-truth').textContent,go:s.querySelector('[data-a="done"]').textContent,walls:s.querySelectorAll('.p-w').length,names:[...s.querySelectorAll('.p-name')].map(t=>t.textContent)}})()`);
  check('result: heading, 3 rooms and the floor area', res.h === 'התוכנית מוכנה' && /3 חדרים/.test(res.sum) && /שטח רצפה/.test(res.sum), res.sum);
  check('result: the truth line, word for word', res.truth === 'המידות נמדדו במצלמה ויכולות לסטות בכמה סנטימטרים. לפני שמזמינים רהיט או מטבח מודדים שוב את הקיר הקובע.', res.truth);
  check('result: the plan is drawn, rooms named', res.walls >= 8 && res.names.join('|') === 'סלון|חדר שינה|חדר שינה', res);
  check('result: the button to corrections and 3D', res.go === 'להמשיך לתיקון ולתלת ממד', res.go);
  await sleep(400); await p.shot('06-result');
  await tapEl(p, `${SH}.querySelector('[data-a="done"]')`, 'continue');
  check('continue hands the result to onDone', await until(p, '!!window.__result', 2000));
  const R = await p.ev('window.__result');
  const areas = R.rooms.map((r) => r.area).sort((a, b) => a - b), want = ROOMS.map((r) => r.area).sort((a, b) => a - b);
  check('result: 3 rooms, each area within 1% of the apartment', R.rooms.length === 3 && areas.every((a, i) => Math.abs(a - want[i]) / want[i] <= 0.01), { got: areas, want: want.map((x) => +x.toFixed(2)) });
  const inner = R.segments.filter((s) => s.kind === 'partition').map((s) => s.t).sort((a, b) => a - b);
  check('result: the two inside walls, 10 and 12 cm (within 2 cm)', inner.length === 2 && Math.abs(inner[0] - 10) <= 2 && Math.abs(inner[1] - 12) <= 2, inner);
  const opOn = R.openings.map((o) => { const m = [(o.a[0] + o.b[0]) / 2, (o.a[1] + o.b[1]) / 2]; let best = null; for (const s of R.segments) { const v = [s.b[0] - s.a[0], s.b[1] - s.a[1]], L2 = v[0] * v[0] + v[1] * v[1], t = Math.max(0, Math.min(1, ((m[0] - s.a[0]) * v[0] + (m[1] - s.a[1]) * v[1]) / L2)), d = Math.hypot(m[0] - s.a[0] - v[0] * t, m[1] - s.a[1] - v[1] * t); if (!best || d < best.d) best = { d, s }; } return { type: o.type, w: o.w, kind: best.s.kind, t: best.s.t, d: +best.d.toFixed(2) }; });
  check('result: the door on the 12 cm inside wall, 80 cm wide (within 3)', opOn.some((o) => o.type === 'door' && o.kind === 'partition' && Math.abs(o.t - 12) <= 2 && Math.abs(o.w - 80) <= 3 && o.d < 0.5), opOn);
  check('result: the window on an outside wall, 120 cm wide (within 3)', opOn.some((o) => o.type === 'window' && o.kind === 'facade' && Math.abs(o.w - 120) <= 3 && o.d < 0.5), opOn);
  check('result meta: 12 corners, 3 rooms, the time, every corner read from its anchor', R.meta.points === 12 && R.meta.rooms === 3 && R.meta.seconds >= 1 && R.meta.anchored === 12, R.meta);
  check('result: the plan tool draft carries walls, the door, the window and the names', R.draft && R.draft.segs.length === R.segments.length && R.draft.openings.length === 2 && R.draft.rooms.map((r) => r.key).join() === 'living,bedroom,bedroom', R.draft && { segs: R.draft.segs.length, op: R.draft.openings.length, rooms: R.draft.rooms });
  // without the anchors the drift (up to 2.5 cm a corner) would stay in the plan: the same walk with the raw marks
  check('no console errors during the walk', p.errors.length === 0, p.errors);
  await p.close();

  // ======== 3b. the same walk on a device without anchors: it works, corners keep the place they were marked at ========
  p = await page('mode=noanchor');
  await tapEl(p, `${SH}.querySelector('[data-a="start"]')`, 'start');
  await until(p, `!!__mock.session && ${OV} && ${OV}.style.display===''`, 8000);
  check('no anchors on this device: the session still opens without them', await p.ev('!__mock.session.enabledFeatures.includes("anchors")'));
  for (let r = 0; r < 3; r++) {
    for (const pt of ROOMS[r].pts) await mark(p, pt, 'noanchor room ' + (r + 1));
    await tapEl(p, K('close'), 'close'); await until(p, `!${OV}.querySelector('[data-r="names"]').hidden`);
    await tapEl(p, `${OV}.querySelector('[data-name="${ROOMS[r].key}"]')`, 'name');
    if (r === 0) { await tapEl(p, K('door'), 'door'); await mark(p, [494, 110], 'door 1'); await mark(p, [494, 190], 'door 2'); }
  }
  await tapEl(p, K('finish'), 'finish');
  await until(p, `!!${SH}.querySelector('[data-a="done"]')`, 4000);
  await tapEl(p, `${SH}.querySelector('[data-a="done"]')`, 'continue');
  await until(p, '!!window.__result', 2000);
  const N = await p.ev('window.__result');
  const nA = N.rooms.map((r) => r.area).sort((a, b) => a - b), nT = N.segments.filter((s) => s.kind === 'partition').map((s) => s.t).sort((a, b) => a - b);
  check('without anchors: 3 rooms, areas within 2%, no corner read from an anchor', N.rooms.length === 3 && N.meta.anchored === 0 && nA.every((a, i) => Math.abs(a - want[i]) / want[i] <= 0.02), { areas: nA, meta: N.meta });
  console.log('     inside walls without anchors (truth 10, 12): ' + JSON.stringify(nT) + '   with anchors: ' + JSON.stringify(inner));
  check('no console errors (no anchors)', p.errors.length === 0, p.errors);
  await p.close();

  // ======== 4. a device without camera measuring ========
  for (const [mode, re] of [['noxr', /בדפדפן הזה המדידה במצלמה לא זמינה/], ['noar', /המכשיר הזה לא תומך במדידה במצלמה/]]) {
    p = await page('mode=' + mode);
    const u = await p.ev(`(()=>{const s=${SH};return {why:(s.querySelector('.nlscan-why')||{}).textContent||'',start:!!s.querySelector('[data-a="start"]'),back:(s.querySelector('[data-a="back"]')||{}).textContent,sup:window.__supported}})()`);
    check('not supported (' + mode + '): a short reason, no start button, a back button', re.test(u.why) && !u.start && u.back === 'חזרה' && u.sup.why === mode, u);
    if (mode === 'noxr') { await sleep(400); await p.shot('07-unsupported'); await tapEl(p, `${SH}.querySelector('[data-a="back"]')`, 'back'); check('back calls onCancel', await until(p, '!!window.__cancel', 1500)); }
    check('no console errors (' + mode + ')', p.errors.length === 0, p.errors);
    await p.close();
  }
  // the camera permission refused
  p = await page('mode=deny');
  await tapEl(p, `${SH}.querySelector('[data-a="start"]')`, 'start');
  check('permission refused: the reason and a retry button, the overlay removed', await until(p, `/לא התקבל אישור/.test((${SH}.querySelector('.nlscan-why')||{}).textContent||'') && !!${SH}.querySelector('[data-a="start"]') && !document.querySelector('.nlscan-root')`, 3000));
  check('no console errors (deny)', p.errors.length === 0, p.errors);
  await p.close();
  // English
  p = await page('mode=ok&lang=en');
  const en = await p.ev(`(()=>{const s=${SH};return {h:s.querySelector('h2').textContent,dir:s.querySelector('.nlscan-page').dir,go:s.querySelector('[data-a="start"]').textContent}})()`);
  check('English: title, left to right, start', en.h === 'Measure the apartment with the camera' && en.dir === 'ltr' && en.go === 'Start measuring', en);
  await sleep(400); await p.shot('08-intro-en');
  await p.close();
} catch (e) {
  check('the walk finished', false, e.message);
} finally {
  chrome.kill();
  console.log('\n' + pass + ' passed, ' + fail + ' failed. Screenshots: ' + out);
  process.exit(fail ? 1 : 0);
}
