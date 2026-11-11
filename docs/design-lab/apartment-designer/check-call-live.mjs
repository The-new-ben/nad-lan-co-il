// node check-call-live.mjs --room=<id> [--port=47962] [--out=<folder for screenshots>]
// The designer's video call (HAD-706, designed interface HAD-712 call-design.md) against the REAL LiveKit server, not the mock.
// Round 3 (11.11.2026): the designed call: entry with preview and switches OFF, the bar at the bottom, layouts tour / arrange /
// talk, per-piece holds (two people move two pieces at once; a held piece is refused for the other), follow, "everyone to me",
// pointing, reconnect and weak-connection banners, the leave confirm and the end summary. Screenshots named after the boards.
// Two separate headless Chromes (two profiles, fake camera and microphone): A on a phone 390 x 844 with touch opens the call
// from the designer's own button, B on a desktop 1440 x 900 joins from the invite link. The pages are the repo's /tour/designer/
// served locally (python docs/tools/design-studio/serve_local.py 47962). Everything is the real code; ONLY the two requests to
// the site are answered by the check: the new routes are not on the live site yet, so the room comes from --room (opened by
// the site's own route /wp-json/nadlan/v1/room, see lk_room.py) and each token from the public live route
// /wp-json/nadlan/v1/room/token. Tokens go from this process into the page through a CDP binding; they are never printed,
// never written to a file. Numbers are measured inside the pages or by this process on one clock.
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const arg = (k, d) => { const a = process.argv.find((x) => x.startsWith('--' + k + '=')); return a ? a.slice(k.length + 3) : d; };
const LIVEMODE = process.argv.includes('--live'); // the live site, the real routes, nothing replaced
const PAGE = arg('page', '/tour/designer/');
let ROOM = arg('room', '');
if (!LIVEMODE && !/^[a-z2-7]{12}$/.test(ROOM)) { console.error('usage: node check-call-live.mjs --room=<12 characters from lk_room.py>   or   --live [--page=/design-studio/]'); process.exit(2); }
const BASE = LIVEMODE ? 'https://nad-lan.co.il' : 'http://127.0.0.1:' + arg('port', '47962');
const TOUR = PAGE.startsWith('/tour/designer');
const OUT = arg('out', path.join(os.tmpdir(), 'nd-call-live'));
fs.mkdirSync(OUT, { recursive: true });
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const LIVE = 'https://nad-lan.co.il/wp-json/nadlan/v1/room/token';
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const receipt = { when: new Date().toISOString(), task: 'HAD-706 live', mode: LIVEMODE ? 'live site, real routes' : 'local pages, live token route', base: BASE, page: PAGE, server: 'LiveKit of nad-lan.co.il (real)', checks: [], numbers: {} };
let fails = 0;
const check = (name, ok, detail) => { receipt.checks.push({ name, ok: !!ok, detail }); if (!ok) fails++; console.log((ok ? 'ok   ' : 'FAIL ') + name + (detail !== undefined ? '  ' + (typeof detail === 'string' ? detail : JSON.stringify(detail)) : '')); };
const lkHosts = new Set();

async function token(name, role) { // the live public route; the answer stays in memory
  const r = await fetch(LIVE, { method: 'POST', headers: { 'Content-Type': 'application/json', 'User-Agent': 'nadlan-local-check' }, body: JSON.stringify({ room: ROOM, role, name }) });
  const j = await r.json().catch(() => null);
  if (!r.ok || !j || j.mode !== 'livekit' || !j.token || !j.url) throw new Error('token route answered ' + r.status + ' mode ' + (j && j.mode));
  try { lkHosts.add(new URL(j.url).hostname); } catch (e) { /* none */ }
  return { url: j.url, token: j.token, identity: j.pid };
}

// --live: an EMPTY hook. It answers nothing (studio.js then asks the site's own routes); it only lets the check read the studio.
const HOOK = LIVEMODE ? 'window.__nlCallHook = {};' : `(() => {
  const wait = {};
  window.__nlCallHook = {
    room: async () => ({ room: ${JSON.stringify(ROOM)} }),
    token: (q) => new Promise((res, rej) => { const id = Math.random().toString(36).slice(2); wait[id] = { res, rej }; window.__nlTokReq(JSON.stringify({ id, name: q.name, role: q.role })); }),
  };
  window.__nlTokRes = (id, v) => { const w = wait[id]; delete wait[id]; if (!w) return; if (v && v.token) w.res(v); else w.rej(Object.assign(new Error('token'), { code: 'fail' })); };
})();`;

const browsers = [];
async function browser(label, w, h, mobile) {
  const port = 9600 + Math.floor(Math.random() * 300) + browsers.length * 300, profile = fs.mkdtempSync(path.join(os.tmpdir(), 'nd-live-' + label + '-'));
  const proc = spawn(CHROME, ['--headless=new', '--remote-debugging-port=' + port, '--user-data-dir=' + profile, '--no-first-run', '--no-default-browser-check', '--disable-extensions', '--lang=he-IL',
    '--use-fake-device-for-media-stream', '--use-fake-ui-for-media-stream', '--autoplay-policy=no-user-gesture-required', '--enable-gpu', '--use-angle=d3d11', '--ignore-gpu-blocklist',
    '--disable-background-timer-throttling', '--disable-renderer-backgrounding', '--disable-backgrounding-occluded-windows', '--window-size=' + w + ',' + h], { stdio: 'ignore' });
  const b = { label, proc, profile };
  browsers.push(b);
  for (let i = 0; i < 80; i++) { try { if ((await fetch('http://127.0.0.1:' + port + '/json/version')).ok) break; } catch (e) { /* not yet */ } await sleep(250); }
  const t = await (await fetch('http://127.0.0.1:' + port + '/json/new?about:blank', { method: 'PUT' })).json();
  const ws = new WebSocket(t.webSocketDebuggerUrl); let id = 0; const pend = new Map(), errors = [];
  const send = (method, params = {}) => new Promise((res) => { const i = ++id; pend.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); });
  ws.onmessage = async (ev) => {
    const m = JSON.parse(ev.data);
    if (m.id && pend.has(m.id)) { pend.get(m.id)(m.result || m.error); pend.delete(m.id); return; }
    if (m.method === 'Runtime.exceptionThrown') errors.push(m.params.exceptionDetails.text + ' ' + ((m.params.exceptionDetails.exception || {}).description || ''));
    else if (m.method === 'Runtime.consoleAPICalled' && m.params.type === 'error') errors.push(m.params.args.map((a) => a.value || a.description).join(' '));
    else if (m.method === 'Log.entryAdded' && m.params.entry.level === 'error') errors.push('[log] ' + m.params.entry.text + ' ' + (m.params.entry.url || ''));
    else if (m.method === 'Runtime.consoleAPICalled' && m.params.type === 'warning') (b.warns = b.warns || []).push(m.params.args.map((a) => a.value || a.description || '').join(' ').replace(/access_token=[^&\s"]+/g, 'access_token=<hidden>').slice(0, 300));
    else if (m.method === 'Network.responseReceived' && /\/designer\/call$/.test(new URL(m.params.response.url).pathname) && m.params.response.status === 201) { send('Network.getResponseBody', { requestId: m.params.requestId }).then((r) => { try { b.liveRoom = JSON.parse(r.body).room; } catch (e) { /* none */ } (b.calls = b.calls || []).push('call 201'); }); }
    else if (m.method === 'Network.responseReceived' && /\/designer\/call/.test(m.params.response.url)) (b.calls = b.calls || []).push(new URL(m.params.response.url).pathname.replace(/^.*designer\//, '') + ' ' + m.params.response.status) // the status only, never the body
    else if (m.method === 'Network.webSocketCreated') { try { const u = new URL(m.params.url); if (/^wss?:$/.test(u.protocol) && /livekit/.test(u.hostname)) lkHosts.add(u.hostname); } catch (e) { /* none */ } } // the host only; the address carries the token and is not kept
    else if (m.method === 'Runtime.bindingCalled' && m.params.name === '__nlTokReq') {
      let q = {}; try { q = JSON.parse(m.params.payload); } catch (e) { q = {}; }
      let v = null; try { v = await token(String(q.name || 'בדיקה'), q.role === 'host' ? 'buyer' : 'friend'); } catch (e) { b.tokenError = String(e.message || e); }
      await send('Runtime.evaluate', { expression: 'window.__nlTokRes(' + JSON.stringify(q.id) + ',' + JSON.stringify(v) + ')' }); // the token goes into the page only
    }
  };
  await new Promise((r) => (ws.onopen = r));
  await send('Page.enable'); await send('Runtime.enable'); await send('Log.enable'); await send('Network.enable');
  await send('Runtime.addBinding', { name: '__nlTokReq' });
  await send('Page.addScriptToEvaluateOnNewDocument', { source: HOOK });
  await send('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: mobile ? 2.625 : 1, mobile });
  await send('Emulation.setFocusEmulationEnabled', { enabled: true });
  if (mobile) await send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
  const ev = async (e) => { const r = await send('Runtime.evaluate', { expression: e, awaitPromise: true, returnByValue: true }); if (r.exceptionDetails) throw new Error(label + ': ' + JSON.stringify(r.exceptionDetails.exception ? r.exceptionDetails.exception.description : r.exceptionDetails.text)); return r.result.value; };
  const touch = (type, x, y) => send('Input.dispatchTouchEvent', { type, touchPoints: type === 'touchEnd' ? [] : [{ x, y, id: 1 }] });
  Object.assign(b, {
    ev, errors, send,
    go: (u) => send('Page.navigate', { url: u }),
    shot: async (name) => { const d = await send('Page.captureScreenshot', { format: 'png' }); fs.writeFileSync(path.join(OUT, name + '.png'), Buffer.from(d.data, 'base64')); },
    tap: async (x, y) => { if (mobile) { await touch('touchStart', x, y); await sleep(40); await touch('touchEnd'); } else { for (const type of ['mousePressed', 'mouseReleased']) await send('Input.dispatchMouseEvent', { type, x, y, button: 'left', clickCount: 1 }); } await sleep(120); },
    type: (text) => send('Input.insertText', { text }),
    touch: (type, x, y) => (mobile ? touch(type, x, y) : send('Input.dispatchMouseEvent', { type: type === 'touchStart' ? 'mousePressed' : type === 'touchEnd' ? 'mouseReleased' : 'mouseMoved', x: x || 0, y: y || 0, button: 'left', buttons: type === 'touchEnd' ? 0 : 1, clickCount: 1 })),
    drag: async (x0, y0, x1, y1, steps = 14) => {
      if (mobile) { await touch('touchStart', x0, y0); await sleep(30); for (let i = 1; i <= steps; i++) { await touch('touchMove', x0 + ((x1 - x0) * i) / steps, y0 + ((y1 - y0) * i) / steps); await sleep(20); } await touch('touchEnd'); }
      else { await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: x0, y: y0 }); await send('Input.dispatchMouseEvent', { type: 'mousePressed', x: x0, y: y0, button: 'left', clickCount: 1 }); for (let i = 1; i <= steps; i++) { await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: x0 + ((x1 - x0) * i) / steps, y: y0 + ((y1 - y0) * i) / steps, button: 'left', buttons: 1 }); await sleep(20); } await send('Input.dispatchMouseEvent', { type: 'mouseReleased', x: x1, y: y1, button: 'left', clickCount: 1 }); }
      await sleep(150);
    },
    close: async () => { try { ws.close(); } catch (e) { /* none */ } },
  });
  return b;
}
const R = 'document.querySelector(".nadlan-designer").shadowRoot';
const mid = (sel) => `(()=>{const e=${R}.querySelector(${JSON.stringify(sel)});if(!e)return null;const r=e.getBoundingClientRect();if(!r.width)return null;return [r.left+r.width/2,r.top+r.height/2]})()`;
const until = async (p, expr, ms = 15000, step = 40) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await p.ev(expr).catch(() => false)) return Date.now() - t0; await sleep(step); } return -1; };
const D = 'window.__nlStudio.designer';
const designOf = (p) => p.ev(`(()=>{const d=${D}.store.design;return JSON.stringify({g:d.geometry_revision,items:d.items.map(i=>[i.id,i.sku,i.x,i.y,i.rot]).sort(),finishes:d.finishes,walls:d.geometry.walls})})()`);
const videos = (p) => p.ev(`(()=>{const r=${R};return [...r.querySelectorAll('.ndc-tile')].map(t=>{const v=t.querySelector('video');const q=v&&v.getVideoPlaybackQuality?v.getVideoPlaybackQuality().totalVideoFrames:0;return {me:t.classList.contains('ndc-me'),w:v?v.videoWidth:0,h:v?v.videoHeight:0,frames:q,time:v?v.currentTime:0}})})()`);
const layout = (p) => p.ev(`(()=>{const r=${R};const q=(s)=>{const e=r.querySelector(s);if(!e)return null;const b=e.getBoundingClientRect();return {l:Math.round(b.left),t:Math.round(b.top),r:Math.round(b.right),b:Math.round(b.bottom)}};
  const small=[...r.querySelectorAll('.ndc button,.ndc a.ndc-b')].filter(b=>b.offsetParent).map(b=>{const x=b.getBoundingClientRect();return [b.dataset.ndc||b.textContent.trim().slice(0,14),Math.round(x.width),Math.round(x.height)]}).filter(a=>a[1]<44||a[2]<44);
  return {dock:q('.ndc:not(.ndc-sheet)'),nav:q('.nd nav'),space:q('[data-nd="space"]'),plan:q('[data-nd="plan"]'),vw:innerWidth,vh:innerHeight,small,scrollW:document.documentElement.scrollWidth}})()`);
const tapSel = async (p, sel) => { // scrolls the control into view and presses it; if the site lays something over it, a plain click, counted
  const c = await p.ev(`(async()=>{const r=${R};const k=window.__nlStudio&&window.__nlStudio.call;if(k&&k.wake)k.wake();const e=r.querySelector(${JSON.stringify(sel)});if(!e)return null;e.scrollIntoView({block:"center",inline:"nearest"});await new Promise(q=>setTimeout(q,400));const b=e.getBoundingClientRect();const x=b.left+b.width/2,y=b.top+b.height/2;const t=r.elementFromPoint(x,y);return {x,y,hit:!!t&&(t===e||e.contains(t))}})()`);
  if (!c) throw new Error(p.label + ": nothing at " + sel);
  if (c.hit) await p.tap(c.x, c.y); else { (p.covered = p.covered || []).push(sel); await p.ev(`${R}.querySelector(${JSON.stringify(sel)}).click()`); await sleep(150); }
};
const hit = (a, b) => a && b && a.l < b.r - 1 && b.l < a.r - 1 && a.t < b.b - 1 && b.t < a.b - 1;

const C_ = 'window.__nlStudio.call';
const wake = (p) => p.ev(`(()=>{const c=${C_};if(c&&c.wake)c.wake();return true})()`).catch(() => false);
const shotC = async (p, name) => { await wake(p); await sleep(250); await p.shot(name); };
const txt = (p, sel) => p.ev(`(()=>{const e=${R}.querySelector(${JSON.stringify(sel)});return e?e.textContent.trim():null})()`);
const vis = (p, sel) => p.ev(`(()=>{const e=${R}.querySelector(${JSON.stringify(sel)});if(!e)return false;const r=e.getBoundingClientRect();return !!e.offsetParent&&r.width>0&&r.height>0})()`);

let A, B;
try {
  A = await browser('A-phone', 390, 844, true);
  B = await browser('B-desktop', 1440, 900, false);

  // ---- A opens the designer on the five-room example and fills it with furniture (a big apartment for the data channel) ----
  await A.go(BASE + PAGE + (TOUR ? '?ul=' + encodeURIComponent('5 חדרים') : ''));
  check('A: the designer loads with the video call button', (await until(A, `!!(window.__nlStudio&&${D}&&${R}.querySelector('[data-nd="call"]'))`, 60000)) >= 0);
  if (!(await A.ev('!!window.__nlStudio'))) { // say what the page is instead of dying on the next line
    console.log('debug page', await A.ev(`JSON.stringify({href:location.href,title:document.title,ready:document.readyState,hook:typeof window.__nlCallHook,studio:typeof window.__nlStudio,text:(document.body&&document.body.innerText||'').slice(0,240)})`), JSON.stringify(A.errors.slice(0, 8)).slice(0, 900));
    await A.shot('00-page-did-not-load');
  }
  const five = await A.ev(`(()=>{const b=[...document.querySelectorAll('.nadlan-designer-pick button')].find(x=>/^5/.test(x.textContent.trim()));if(!b)return 'none';if(b.getAttribute('aria-pressed')==='true')return 'already';b.scrollIntoView({block:'center'});b.click();return 'pressed'})()`);
  if (five === 'pressed') await until(A, `${D}&&/5r/.test(${D}.store.design.geometry_revision)`, 20000);
  receipt.numbers.five_room_button = five;
  await A.ev(`${D}.ready3d`);
  const label = await A.ev(`${R}.querySelector('[data-nd="call"]').textContent`);
  check('A: the button says "שיחת וידאו"', label === 'שיחת וידאו', label);
  const added = await A.ev(`(()=>{const s=${D}.store,base=s.design.items.slice();let n=0;for(let k=0;k<3;k++)for(const it of base){const r=s.apply({op:'item.add',item:{id:'x'+k+'_'+it.id,sku:it.sku,x:it.x+(k+1)*7,y:it.y+(k+1)*5,rot:it.rot,status:'decor'}});if(r.ok)n++;}return {n,items:s.design.items.length,geo:s.design.geometry_revision}})()`);
  receipt.numbers.a_design = added;

  // ---- 1. the start sheet: preview, mic meter, camera and mic OFF until switched on ----
  await tapSel(A, '[data-nd="call"]');
  check('A: the start sheet opens', (await until(A, `!!${R}.querySelector('.ndc-sheet [data-ndc="name"]')`, 8000)) >= 0);
  const sheetA = await A.ev(`(()=>{const s=${R}.querySelector('.ndc-sheet');return {h:s.querySelector('h2').textContent,go:s.querySelector('[data-ndc="go"]').textContent.trim(),fine:s.querySelector('.ndo-fine').textContent,label:s.querySelector('.ndo-lbl').textContent,meter:s.querySelectorAll('.ndo-meter i').length,cam:s.querySelector('[data-ndc="cam"]').checked,mic:s.querySelector('[data-ndc="mic"]').checked,sub:s.querySelector('.ndo-shsub').textContent}})()`);
  check('A: the sheet words as designed, a 14-bar mic meter, camera and mic switches OFF', sheetA.h === 'שיחת וידאו על הדירה' && sheetA.go === 'להתחיל שיחה' && sheetA.label === 'איך לקרוא לך?' && sheetA.fine === 'השיחה לא מוקלטת. הדפדפן יבקש רשות למצלמה ולמיקרופון רק כשתלחצו.' && sheetA.meter === 14 && !sheetA.cam && !sheetA.mic && /^מזמינים את מי שצריך ומעצבים יחד את דירת 5 החדרים\./.test(sheetA.sub), sheetA);
  await A.shot('02-entry-start-phone');
  await tapSel(A, '.ndc-sheet [data-ndc="name"]'); await A.ev(`${R}.querySelector('.ndc-sheet [data-ndc="name"]').value=''`); await A.type('דנה');
  await A.ev(`${R}.querySelector('.ndc-sheet [data-ndc="cam"]').click()`);
  await A.ev(`${R}.querySelector('.ndc-sheet [data-ndc="mic"]').click()`);
  const prevOn = await until(A, `(()=>{const v=${R}.querySelector('.ndc-sheet .ndo-pv video');return v&&v.videoWidth>0})()`, 8000);
  let lit = 0; for (let k = 0; k < 30 && !lit; k++) { lit = await A.ev(`${R}.querySelectorAll('.ndc-sheet .ndo-meter i.ndo-lit').length`); await sleep(70); }
  check('A: switching the camera on shows her own preview; the mic meter moves with the (fake) sound', prevOn >= 0 && lit > 0, { preview_ms: prevOn, lit_bars: lit });
  await A.shot('02-entry-start-phone-preview');
  await A.ev(`${R}.querySelector('.ndc-sheet [data-ndc="mic"]').click()`); // mic back off: she enters with the camera only
  const tA = Date.now(); await tapSel(A, '.ndc-sheet [data-ndc="go"]');
  const conA = await until(A, `!!(window.__nlStudio.call&&window.__nlStudio.callRoom&&window.__nlStudio.callRoom.state==='connected')`, 30000, 25);
  const vidA = await until(A, `[...${R}.querySelectorAll('.ndo-face.ndo-me video')].some(v=>v.videoWidth>0)`, 30000, 25);
  receipt.numbers.a_click_to_connected_ms = conA >= 0 ? conA : null;
  receipt.numbers.a_click_to_own_video_ms = vidA >= 0 ? Date.now() - tA : null;
  receipt.numbers.a_breakdown = await A.ev('window.__nlStudio.callTimes||null');
  const roomA = await A.ev(`(()=>{const r=window.__nlStudio.callRoom;return r?{state:r.state,me:!!r.localParticipant.identity}:null})()`);
  check('1. A is connected to LiveKit (room state connected, server host ends with .livekit.cloud)', roomA && roomA.state === 'connected' && lkHosts.size === 1 && [...lkHosts][0].endsWith('.livekit.cloud'), { ...roomA, tokenError: A.tokenError });
  check('1. A sees her own camera in the call (she switched it on)', vidA >= 0, { click_to_own_video_ms: receipt.numbers.a_click_to_own_video_ms });
  const aMedia = await A.ev(`(()=>{const p=${C_}.participants().find(x=>x.local);return {mic:p.mic,cam:p.cam}})()`);
  check('1. A entered with the microphone OFF (she did not switch it on)', aMedia.mic === false && aMedia.cam === true, aMedia);
  const idA = await A.ev('window.__nlStudio.callRoom.localParticipant.identity');
  await sleep(800);
  await shotC(A, '03-tour-phone-alone');

  // ---- 6. invite: WhatsApp first, the link with ?room=, copy turns into "הועתק" ----
  await wake(A); await tapSel(A, '.ndo-bar [data-ndc="invite"]');
  await until(A, `!!${R}.querySelector('.ndo-sheet [data-ndc="wa"]')`, 3000);
  const inv = await A.ev(`(()=>{const p=${R}.querySelector('.ndo-sheet');return {h:p.querySelector('h3').textContent,sub:p.querySelector('.ndo-shsub').textContent,link:p.querySelector('.ndo-link').value,wa:p.querySelector('[data-ndc="wa"]').href,waText:p.querySelector('[data-ndc="wa"]').textContent.trim()}})()`);
  if (LIVEMODE) ROOM = new URL(inv.link).searchParams.get('room') || '';
  const waMsg = inv.wa.startsWith('https://wa.me/?text=') ? decodeURIComponent(inv.wa.slice('https://wa.me/?text='.length)) : '';
  check('6. the invite sheet: "להזמין לשיחה", the page link with ?room=, no name in the link', inv.h === 'להזמין לשיחה' && inv.sub === 'מי שמקבל את הקישור נכנס מהדפדפן, בלי הרשמה. הקישור עובד רק לשיחה הזאת.' && /^[a-z2-7]{12}$/.test(ROOM) && new URL(inv.link).origin === BASE && new URL(inv.link).pathname === PAGE && !/דנה|name=/.test(inv.link), { link: inv.link.replace(ROOM, '<room>') });
  check('6. "הזמנה בוואטסאפ" first: wa.me with the written message and the link', inv.waText === 'הזמנה בוואטסאפ' && waMsg === 'דנה מזמין אותך לשיחת וידאו על דירת 5 חדרים. רואים את הדירה ומעצבים יחד, בדפדפן, בלי הרשמה. ' + inv.link, { text: waMsg.replace(ROOM, '<room>') });
  await A.ev(`${R}.querySelector('.ndo-sheet [data-ndc="copy"]').click()`); await sleep(200);
  const copied = await txt(A, '.ndo-sheet [data-ndc="copy"]');
  check('6. copy turns into "הועתק"', copied === 'הועתק', copied);
  await A.shot('08-invite-phone');
  await tapSel(A, '.ndo-sheet [data-ndc="shx"]');

  // ---- 2. B opens the invite link: the join sheet, joins with both OFF, receives the apartment ----
  await B.go(inv.link);
  check('B: the invite link shows the join sheet at once', (await until(B, `!!(${R}&&${R}.querySelector('.ndc-sheet [data-ndc="name"]'))`, 20000)) >= 0);
  const sheetB = await B.ev(`(()=>{const s=${R}.querySelector('.ndc-sheet');return {h:s.querySelector('h2').textContent,go:s.querySelector('[data-ndc="go"]').textContent.trim(),designer:!!${R}.querySelector('.nd'),cam:s.querySelector('[data-ndc="cam"]').checked,mic:s.querySelector('[data-ndc="mic"]').checked}})()`);
  check('B: "להצטרף לשיחה על הדירה", one name field, "כניסה", both switches off; no designer before the apartment arrives', sheetB.h === 'להצטרף לשיחה על הדירה' && sheetB.go === 'כניסה' && !sheetB.designer && !sheetB.cam && !sheetB.mic, sheetB);
  await B.shot('02-entry-join-desktop');
  await tapSel(B, '.ndc-sheet [data-ndc="name"]'); await B.ev(`${R}.querySelector('.ndc-sheet [data-ndc="name"]').value=''`); await B.type('אבי');
  const tB = Date.now(); await tapSel(B, '.ndc-sheet [data-ndc="go"]');
  const gotB = await until(B, `!!(window.__nlStudio&&window.__nlStudio.call&&window.__nlStudio.callRoom&&window.__nlStudio.callRoom.state==='connected'&&${D})`, 40000, 25);
  receipt.numbers.b_click_to_designer_in_call_ms = gotB >= 0 ? Date.now() - tB : null;
  await B.ev(`${D}.ready3d`).catch(() => null);
  const planB = await B.ev('window.__nlStudio.call.stats.planGot');
  const sent = await A.ev('window.__nlStudio.call.stats.planSent||0');
  const [dA, dB] = [JSON.parse(await designOf(A)), JSON.parse(await designOf(B))];
  check('2. B received the plan and the design on the data channel and opened the SAME apartment', gotB >= 0 && sent >= 1 && JSON.stringify(dA) === JSON.stringify(dB), { items: [dA.items.length, dB.items.length], identical: JSON.stringify(dA) === JSON.stringify(dB), plan_message: planB });
  check('5. the big apartment (over 15 KB) arrived whole, in parts', planB && planB.bytes > 15 * 1024, { bytes: planB && planB.bytes, ms: planB && planB.ms });
  receipt.numbers.plan_message = planB;
  await sleep(500);
  const bMedia = await B.ev(`(()=>{const p=${C_}.participants().find(x=>x.local);return {mic:p.mic,cam:p.cam}})()`);
  check('camera and microphone are OFF on entry (B switched nothing on)', bMedia.mic === false && bMedia.cam === false, bMedia);
  const hostSeen = [await A.ev(`${C_}.host`), await B.ev(`${C_}.host`)];
  check('the host is the one who opened the room (first in), the same on both', hostSeen[0] === idA && hostSeen[1] === idA, hostSeen.map((h) => (h === idA ? 'A' : h)));

  // ---- 3. B turns the camera on from the bar; both see each other's video ----
  await tapSel(B, '.ndo-bar [data-ndc="cam"]');
  const vt0 = Date.now();
  const bothV = await until(A, `[...${R}.querySelectorAll('.ndo-face:not(.ndo-me) video')].some(v=>v.videoWidth>0)`, 20000, 30);
  const bothV2 = await until(B, `[...${R}.querySelectorAll('.ndo-face:not(.ndo-me) video')].some(v=>v.videoWidth>0)`, 20000, 30);
  receipt.numbers.remote_video_ms = { a_sees_b: bothV >= 0 ? Date.now() - vt0 : null, b_sees_a: bothV2 };
  const camLabel = await txt(B, '.ndo-bar [data-ndc="cam"] .ndo-lb');
  check('3. each sees the other\'s video after B pressed "מצלמה" (label reads "מצלמה" when on)', bothV >= 0 && bothV2 >= 0 && camLabel === 'מצלמה', { camLabel, ...receipt.numbers.remote_video_ms });
  await sleep(600);
  await shotC(A, '03-tour-phone'); await shotC(B, '10-desktop');

  // ---- the frame: the bar at the bottom, the designer's tool bar uncovered, every target 44 and up ----
  const frame = (p) => p.ev(`(()=>{const r=${R};const q=(s)=>{const e=r.querySelector(s);if(!e)return null;const b=e.getBoundingClientRect();return {l:Math.round(b.left),t:Math.round(b.top),r:Math.round(b.right),b:Math.round(b.bottom),w:Math.round(b.width),h:Math.round(b.height)}};
    const all=[...r.querySelectorAll('.ndo button,.ndo a,.ndo-sheetwrap button')].filter(b=>b.offsetParent&&b.getBoundingClientRect().width>0);
    const small=all.map(b=>{const x=b.getBoundingClientRect();return [b.dataset.ndc||b.dataset.lay||b.textContent.trim().slice(0,14),Math.round(x.width),Math.round(x.height)]}).filter(a=>a[1]<44||a[2]<44);
    const cells=[...r.querySelectorAll('.ndo-bar .ndo-b:not(.ndo-leave)')].map(b=>{const x=b.getBoundingClientRect();return [b.dataset.ndc,Math.round(x.width),Math.round(x.height)]});
    const order=[...r.querySelectorAll('.ndo-bar .ndo-b')].map(b=>[b.dataset.ndc,Math.round(b.getBoundingClientRect().left)]);
    return {host:q(':host')||(()=>{const b=r.host.getBoundingClientRect();return {t:Math.round(b.top),b:Math.round(b.bottom),l:Math.round(b.left),r:Math.round(b.right)}})(),bar:q('.ndo-bar'),head:q('.ndo-head'),nav:q('.nd > nav'),space:q('[data-nd="space"]'),plan:q('[data-nd="plan"]'),small,cells,order,labels:[...r.querySelectorAll('.ndo-bar .ndo-lb')].map(l=>l.textContent),scrollW:document.documentElement.scrollWidth,vw:innerWidth}})()`);
  await wake(A);
  const fa = await frame(A), fb = await frame(B);
  const hostB = (f) => f.host || {};
  check('phone: the control bar sits at the bottom edge and covers neither the designer\'s tool bar, the 3D nor the header', fa.bar && Math.abs(fa.bar.b - hostB(fa).b) <= 2 && fa.nav && fa.nav.b <= fa.bar.t + 1 && !hit(fa.bar, fa.nav) && !hit(fa.bar, fa.space) && !hit(fa.head, fa.space) && fa.scrollW <= fa.vw, { bar: fa.bar, nav: fa.nav, space: fa.space, head: fa.head, host: fa.host });
  const ord = fa.order.map((o) => o[0]); const rtl = [...fa.order].sort((x, y) => y[1] - x[1]).map((o) => o[0]);
  check('phone: right to left: mic, camera, follow, point, invite, more, then leave apart; a word under every icon', JSON.stringify(rtl) === JSON.stringify(['mic', 'cam', 'follow', 'point', 'invite', 'more', 'leave']) && fa.labels.every((l) => l.trim().length > 0), { rtl, labels: fa.labels });
  check('phone and desktop: every call target at least 44 x 44; bar cells at least 50 x 60', fa.small.length === 0 && fb.small.length === 0 && fa.cells.every((c) => c[1] >= 50 && c[2] >= 60), { phone: fa.small, desktop: fb.small, cells: fa.cells });
  check('desktop: header on top, side panel, the bar under the centre; the designer\'s tool bar uncovered', fb.bar && fb.nav && fb.nav.b <= fb.bar.t + 1 && !hit(fb.bar, fb.nav) && !hit(fb.bar, fb.plan) && !!(await vis(B, '.ndo-side')), { bar: fb.bar, nav: fb.nav, plan: fb.plan });

  // controls hide after 4 s on the phone and come back with one tap
  await wake(A); await sleep(4600);
  const hidden = await A.ev(`${R}.querySelector('.ndo').classList.contains('ndo-barhid')`);
  const hint = (await A.ev(`${C_}.controlsHinted`)) ? 'הקישו על המסך כדי להחזיר את הכפתורים' : await txt(A, '[data-ndc="toast"]'); // the hint is said the first time only (maybe earlier)
  await A.tap(30, 560); await sleep(300); // a tap on an empty corner of the stage
  const back = await A.ev(`!${R}.querySelector('.ndo').classList.contains('ndo-barhid')`);
  check('phone: the controls hide after 4 s and come back with a tap; the first time a hint says how', hidden && back && hint === 'הקישו על המסך כדי להחזיר את הכפתורים', { hidden, back, hint });

  // ---- 4. layouts: A goes to "סידור" (plan fills, 3D in a corner); drags a piece; B has it within 2 s ----
  await wake(A); await tapSel(A, '.ndo-seg-stage [data-lay="b"]');
  await sleep(500);
  const lb = await A.ev(`(()=>{const r=${R};const p=r.querySelector('[data-nd="plan"]').getBoundingClientRect(),s=r.querySelector('[data-nd="space"]').getBoundingClientRect();return {layout:${C_}.layout,plan:[Math.round(p.width),Math.round(p.height)],space:[Math.round(s.width),Math.round(s.height)]}})()`);
  await A.ev(`(()=>{const b=${R}.querySelector('.nd > nav button[aria-expanded="true"]');if(b)b.click();return true})()`); await sleep(200); // a designer sheet a tap may have opened
  check('4. "סידור": the plan fills the stage, the 3D shrinks to a 150 x 128 inset', lb.layout === 'b' && lb.plan[1] > 400 && Math.abs(lb.space[0] - 150) <= 4 && Math.abs(lb.space[1] - 128) <= 4, lb);
  const ids = dA.items.map((i) => i[0]);
  const pickId = async (p, not = []) => p.ev(`(()=>{const r=${R};const pl=r.querySelector('[data-nd="plan"]').getBoundingClientRect();const no=${JSON.stringify(not)};for(const id of ${JSON.stringify(ids)}){if(no.includes(id))continue;const e=r.querySelector('[data-item="'+id+'"] rect');if(!e)continue;const b=e.getBoundingClientRect();const cx=b.left+b.width/2,cy=b.top+b.height/2,top=r.elementFromPoint(cx,cy),own=top&&top.closest&&top.closest('[data-item]');if(b.width>14&&b.height>14&&b.left>pl.left+16&&b.right<pl.right-16&&b.top>pl.top+90&&b.bottom<pl.bottom-16&&own&&own.dataset.item===id)return id}return null})()`);
  const itemOf = (p, id) => p.ev(`JSON.stringify(${D}.store.item(${JSON.stringify(id)}))`).then(JSON.parse);
  const idX = await pickId(A);
  if (!idX) console.log('debug pick', await A.ev(`(()=>{const r=${R};const pl=r.querySelector('[data-nd="plan"]').getBoundingClientRect();const out=[];for(const e of [...r.querySelectorAll('[data-item] rect')].slice(0,12)){const id=e.closest('[data-item]').dataset.item;const b=e.getBoundingClientRect();const t=r.elementFromPoint(b.left+b.width/2,b.top+b.height/2);out.push([id,Math.round(b.left),Math.round(b.top),Math.round(b.width),Math.round(b.height),t&&(t.getAttribute&&t.getAttribute('class'))||t&&t.tagName])}return JSON.stringify({pl:[pl.left,pl.top,pl.width,pl.height],out})})()`));
  const before = await itemOf(A, idX);
  let c = await A.ev(mid(`[data-item="${idX}"] rect`));
  await wake(A); await A.drag(c[0], c[1], c[0] + 26, c[1] + 18);
  const afterA = await itemOf(A, idX);
  const tm = Date.now();
  const arrived = await until(B, `(()=>{const i=${D}.store.item(${JSON.stringify(idX)});return i&&i.x===${afterA.x}&&i.y===${afterA.y}})()`, 2000, 15);
  receipt.numbers.move_a_to_b_ms = arrived >= 0 ? Date.now() - tm : null;
  check('4. A drags a piece with her finger: it moved on A and is in the same place on B within 2 s (the final position goes reliable)', (afterA.x !== before.x || afterA.y !== before.y) && arrived >= 0, { id: idX, from: [before.x, before.y], to: [afterA.x, afterA.y], arrived_ms: receipt.numbers.move_a_to_b_ms });

  // ---- hold: A keeps her finger on the piece; B is refused on that piece only, with the sentence; the hold shows ----
  c = await A.ev(mid(`[data-item="${idX}"] rect`));
  await A.touch('touchStart', c[0], c[1]); for (let i = 1; i <= 6; i++) { await A.touch('touchMove', c[0] + i * 2, c[1] + i); await sleep(30); }
  const heldB = await until(B, `${C_}.holds.some(h=>h.key==='i:${idX}')`, 2000, 15);
  const objHe = await B.ev(`(()=>{const it=${D}.store.item(${JSON.stringify(idX)});return it.sku})()`);
  const refusedApi = await B.ev(`(()=>{const i=${D}.store.item(${JSON.stringify(idX)});const r=${D}.store.apply({op:'item.move',id:${JSON.stringify(idX)},x:i.x+40,y:i.y});return {ok:r.ok,code:r.code,reason:r.reason}})()`);
  await B.ev(`${R}.querySelector('[data-item="${idX}"] rect').scrollIntoView({block:'center'})`).catch(() => {});
  await sleep(300);
  const holdBox = await B.ev(`(()=>{const b=${R}.querySelector('.ndo-hold[data-k="i:${idX}"]');if(!b||b.hidden)return null;return {chip:b.querySelector('.ndo-chip b').textContent,pen:getComputedStyle(b).getPropertyValue('--pen').trim()}})()`);
  const cb = await B.ev(mid(`[data-item="${idX}"] rect`));
  if (cb) await B.drag(cb[0], cb[1], cb[0] - 30, cb[1] + 20);
  const toastHold = await txt(B, '[data-ndc="toast"]');
  check('hold: while A\'s finger is on the piece, B sees it held in her pen colour with "דנה מזיז/ה את …"', heldB >= 0 && holdBox && /^דנה מזיז\/ה את ה/.test(holdBox.chip) && holdBox.pen.toUpperCase() === '#1F5FA8', { held_after_ms: heldB, holdBox, sku: objHe });
  check('hold: B\'s change to that piece is refused (code call.hold) and a drag shows "דנה מחזיק/ה את … נסו שוב בעוד רגע."', refusedApi.ok === false && refusedApi.code === 'call.hold' && /^דנה מחזיק\/ה את ה.+\. נסו שוב בעוד רגע\.$/.test(toastHold || ''), { api: refusedApi, toast: toastHold });
  await shotC(A, '04-arrange-phone-holding'); await B.shot('04-arrange-desktop-sees-hold');
  await A.touch('touchEnd'); await sleep(400);
  const freed = await until(B, `!${C_}.holds.some(h=>h.key==='i:${idX}')`, 2000, 20);
  check('hold: lifting the finger lets go at once', freed >= 0, { freed_ms: freed });

  // ---- two people move two different pieces at the same time; both moves are kept everywhere ----
  const idY = (await pickId(B, [idX])) || ids.find((x) => x !== idX);
  await B.ev(`${R}.querySelector('[data-item="${idY}"] rect').scrollIntoView({block:'center'})`).catch(() => {});
  await sleep(300);
  const bx0 = await itemOf(A, idX), by0 = await itemOf(B, idY);
  const ca = await A.ev(mid(`[data-item="${idX}"] rect`)), cbb = await B.ev(mid(`[data-item="${idY}"] rect`));
  await wake(A);
  await Promise.all([A.drag(ca[0], ca[1], ca[0] - 24, ca[1] - 20, 16), B.drag(cbb[0], cbb[1], cbb[0] + 28, cbb[1] - 18, 16)]);
  await sleep(1200);
  const [xA, yA, xB, yB] = [await itemOf(A, idX), await itemOf(A, idY), await itemOf(B, idX), await itemOf(B, idY)];
  const movedX = xA.x !== bx0.x || xA.y !== bx0.y, movedY = yB.x !== by0.x || yB.y !== by0.y;
  check('two people move two different pieces at the same time: both moved, and both are the same on both screens', movedX && movedY && xA.x === xB.x && xA.y === xB.y && yA.x === yB.x && yA.y === yB.y && (await designOf(A)) === (await designOf(B)), { x: { a: [xA.x, xA.y], b: [xB.x, xB.y], from: [bx0.x, bx0.y] }, y: { a: [yA.x, yA.y], b: [yB.x, yB.y], from: [by0.x, by0.y] } });
  // undo mine: A's last move only
  const undoVis = await vis(A, '[data-ndc="undo"]');
  await wake(A); await tapSel(A, '[data-ndc="undo"]'); await sleep(800);
  const [uX, uY, uXb] = [await itemOf(A, idX), await itemOf(A, idY), await itemOf(B, idX)];
  check('"בטל את שלי" undoes A\'s own last move only; B\'s piece stays; B follows the undo', undoVis && uX.x === bx0.x && uX.y === bx0.y && uY.x === yB.x && uY.y === yB.y && uXb.x === uX.x && uXb.y === uX.y, { undoVis, x: [uX.x, uX.y], y: [uY.x, uY.y] });

  // ---- 5. follow: B taps A's face, follows her view; a touch on the model stops it and offers "חזרה לדנה" ----
  await A.ev(`${C_}.setLayout('a')`); await sleep(300);
  await tapSel(B, `.ndo-face[data-id="${idA}"]`);
  await until(B, `!!${R}.querySelector('.ndo-sheet [data-ndc="fol"]')`, 3000);
  const folText = await txt(B, '.ndo-sheet [data-ndc="fol"]');
  await B.shot('07-face-sheet-desktop');
  await tapSel(B, '.ndo-sheet [data-ndc="fol"]');
  const fv = await A.ev(`(()=>{const d=${D},f=d.store.derived.faceBy.living||d.store.derived.faces[0];const v={mode:'walk',x:Math.round((f.bb.x0+f.bb.x1)/2),y:Math.round((f.bb.y0+f.bb.y1)/2),yaw:0.7,pitch:0};d.setMode('walk');d.setView(v);return d.getView()})()`);
  const near = (a, b) => a && b && a.mode === b.mode && Math.abs(a.x - b.x) < 3 && Math.abs(a.y - b.y) < 3 && Math.abs(a.yaw - b.yaw) < 0.03;
  const folMs = await until(B, `(()=>{const v=${D}.getView(),f=${JSON.stringify(fv)};return v&&v.mode===f.mode&&Math.abs(v.x-f.x)<3&&Math.abs(v.y-f.y)<3&&Math.abs(v.yaw-f.yaw)<0.03})()`, 4000, 20);
  const frameB = await vis(B, '[data-ndc="frame"]'), tabB = await txt(B, '[data-ndc="followtab"]');
  await shotC(B, '07-following-desktop');
  const viewers = await txt(A, `.ndo-face.ndo-me .ndo-tview`);
  check('follow: B taps A\'s face, "לעקוב אחרי דנה", and walks where A walks (frame + tab in her colour)', folText === 'לעקוב אחרי דנה' && folMs >= 0 && frameB && tabB === 'עוקבים אחרי דנה · הקישו לעצור', { folText, follow_ms: folMs, frameB, tabB, viewers });
  c = await B.ev(mid('[data-nd="space"] canvas')); await B.tap(c[0], c[1] - 80);
  await sleep(300);
  const stopped = await B.ev(`${C_}.following`), chipB = await txt(B, '[data-ndc="backchip"]');
  check('follow: one touch on the model stops following and shows "חזרה לדנה"', stopped === false && !!chipB && chipB.endsWith('חזרה לדנה'), { stopped, chipB });
  await tapSel(B, '[data-ndc="backchip"]'); await sleep(300);
  check('follow: "חזרה לדנה" follows again', (await B.ev(`${C_}.followingId`)) === idA);
  await B.ev(`${C_}.follow(false)`);

  // ---- "כולם אליי": the host summons, B says "לא עכשיו", then lets the 3 s run out and follows ----
  await wake(A); await tapSel(A, '.ndo-bar [data-ndc="more"]');
  await until(A, `!!${R}.querySelector('.ndo-sheet [data-more="summon"]')`, 2000);
  await shotC(A, '06-more-sheet-phone');
  await A.ev(`${R}.querySelector('.ndo-sheet [data-more="summon"]').click()`);
  const card = await until(B, `!!${R}.querySelector('.ndo-sheet.ndo-card [data-ndc="sno"]')`, 3000, 20);
  const cardText = await txt(B, '.ndo-sheet.ndo-card .ndo-sumhead b#ndo-sh-t');
  await B.shot('07-summon-desktop');
  await tapSel(B, '.ndo-sheet [data-ndc="sno"]'); await sleep(300);
  const declined = (await B.ev(`${C_}.followingId`)) === null && (await vis(B, '[data-ndc="backchip"]'));
  await A.ev(`${C_}.summon()`);
  await until(B, `!!${R}.querySelector('.ndo-sheet.ndo-card')`, 3000, 20);
  const auto = await until(B, `${C_}.followingId===${JSON.stringify(idA)}`, 5000, 50);
  check('"כולם אליי": B sees "דנה רוצה להראות לכולם את …" with 3 s; "לא עכשיו" stays, and the next time the 3 s run out and B follows', card >= 0 && /^דנה רוצה להראות לכולם את /.test(cardText || '') && declined && auto >= 2500 && auto <= 4500, { card_ms: card, cardText, declined, auto_follow_after_ms: auto });
  await B.ev(`${C_}.follow(false)`);

  // ---- pointing: A presses "הצבעה" and draws on the plan; B sees the line and "דנה: כאן"; it fades ----
  await wake(A); await tapSel(A, '.ndo-bar [data-ndc="point"]'); await sleep(400);
  const pc = await A.ev(`(()=>{const r=${R},pl=r.querySelector('[data-nd="plan"]'),b=pl.getBoundingClientRect();for(let y=b.top+b.height*0.35;y<b.bottom-60;y+=17)for(let x=b.left+b.width*0.3;x<b.right-80;x+=13){const e=r.elementFromPoint(x,y);if(e&&pl.contains(e)&&!e.closest('[data-item],[data-wall],.grip,button'))return [x,y]}return null})()`);
  const before2 = await designOf(A);
  await A.touch('touchStart', pc[0], pc[1]); for (let i = 1; i <= 10; i++) { await A.touch('touchMove', pc[0] + i * 6, pc[1] + i * 3); await sleep(60); }
  const laserA = await A.ev(`${R}.querySelectorAll('.ndo-lchip').length`);
  const laser = await until(B, `[...${R}.querySelectorAll('.ndo-lchip')].some(c=>c.querySelector('b').textContent==='דנה: כאן')`, 2500, 20);
  await shotC(A, '07-point-phone'); await B.shot('07-point-desktop');
  await A.touch('touchEnd'); await sleep(1500);
  const faded = await B.ev(`${R}.querySelectorAll('.ndo-lchip').length===0`);
  check('pointing: B sees A\'s line with "דנה: כאן", it fades by itself, and pointing changes nothing in the design', laser >= 0 && faded && (await designOf(A)) === before2, { laser_ms: laser, faded, own_chip: laserA, at: pc });
  await wake(A); await tapSel(A, '.ndo-bar [data-ndc="point"]');

  // ---- talk layout (phone) and the people sheet ----
  await wake(A); await tapSel(A, '.ndo-seg-stage [data-lay="c"]'); await sleep(600);
  await shotC(A, '05-talk-phone');
  const talk = await A.ev(`(()=>{const r=${R};const f=r.querySelector('.ndo-faces').getBoundingClientRect(),s=r.querySelector('[data-nd="space"]').getBoundingClientRect();return {faces:Math.round(f.height),space:Math.round(s.height),spaceTop:Math.round(s.top),facesBottom:Math.round(f.bottom),btn:!!r.querySelector('[data-ndc="modelback"]').offsetParent}})()`);
  check('"שיחה": faces fill the top, the live model below with "חזרה לדגם"', talk.faces > 250 && talk.space > 150 && talk.spaceTop >= talk.facesBottom - 2 && talk.btn, talk);
  await tapSel(A, '[data-ndc="modelback"]'); await sleep(300);
  await wake(A); await tapSel(A, '.ndo-bar [data-ndc="more"]'); await A.ev(`${R}.querySelector('.ndo-sheet [data-more="people"]').click()`); await sleep(300);
  await shotC(A, '08-people-phone'); await A.ev(`${C_}.openPanel(null)`);
  await B.ev(`${C_}.chat('הספה מול החלון נראית טוב')`); await sleep(600);
  await A.ev(`${C_}.chat('אז נשאיר אותה שם')`); await sleep(600);
  await B.shot('10-desktop-chat');

  // ---- trouble: reconnecting (within 1 s, the model stays), weak connection (voice only, video back) ----
  await A.ev(`(()=>{const r=window.__nlStudio.callRoom;r.emit('reconnecting');return true})()`);
  const banner = await until(A, `!!${R}.querySelector('.ndo-ban-re')`, 1000, 10);
  const stillModel = await A.ev(`!!${R}.querySelector('[data-nd="space"] canvas')&&!!${D}`);
  await shotC(A, '09-reconnecting-phone');
  await A.ev(`(()=>{const r=window.__nlStudio.callRoom;r.emit('reconnected');return true})()`);
  const cleared = await until(A, `!${R}.querySelector('.ndo-ban-re')`, 3000, 20);
  check('reconnecting: the ink banner "מתחברים מחדש…" shows within 1 s, the model stays, and it clears when back', banner >= 0 && banner <= 1000 && stillModel && cleared >= 0, { banner_ms: banner, cleared_ms: cleared });
  await sleep(1500);
  check('after the reconnect A caught up and both designs are the same', (await designOf(A)) === (await designOf(B)));
  const poor = setInterval(() => A.ev(`(()=>{const r=window.__nlStudio.callRoom;r.emit('connectionQualityChanged','poor',r.localParticipant);return true})()`).catch(() => {}), 1500);
  const weak = await until(A, `!!${R}.querySelector('.ndo-ban-weak')`, 14000, 200);
  clearInterval(poor);
  const weakT = await txt(A, '.ndo-ban-weak b');
  await shotC(A, '09-weak-phone');
  await A.ev(`(()=>{const r=window.__nlStudio.callRoom;r.emit('connectionQualityChanged','excellent',r.localParticipant);return true})()`);
  await tapSel(A, '[data-ndc="weakv"]'); await sleep(800);
  const camBack = await A.ev(`${C_}.participants().find(x=>x.local).cam`);
  check('weak connection for 10 s: voice only with "החיבור חלש. עברנו לקול בלבד כדי שהשיחה תמשיך."; "להחזיר וידאו" brings the camera back', weak >= 9000 && weakT === 'החיבור חלש. עברנו לקול בלבד כדי שהשיחה תמשיך.' && camBack === true, { weak_after_ms: weak, weakT, camBack });

  // ---- 7. leaving: A (the host) is asked first; "לצאת, השיחה ממשיכה"; the summary; B keeps the design and becomes host ----
  const keep = await designOf(B);
  await wake(A); await tapSel(A, '.ndo-bar [data-ndc="leave"]');
  await until(A, `!!${R}.querySelector('.ndo-sheet [data-ndc="keep"]')`, 2000);
  const lv = await A.ev(`(()=>{const s=${R}.querySelector('.ndo-sheet');return {t:s.querySelector('h3').textContent,keep:s.querySelector('[data-ndc="keep"] span').textContent,sub:s.querySelector('[data-ndc="keep"] small').textContent,end:s.querySelector('[data-ndc="endall"]').textContent,cancel:s.querySelector('[data-ndc="cancel"]').textContent,still:!!window.__nlStudio.call}})()`);
  await A.shot('06-leave-host-phone');
  check('leave asks first: the host gets "לצאת, השיחה ממשיכה" (who becomes host) / "לסיים לכולם" / "ביטול"; nothing left yet', lv.t === 'לצאת מהשיחה?' && lv.keep === 'לצאת, השיחה ממשיכה' && lv.sub === 'אבי יהיה/תהיה המארח/ת' && lv.end === 'לסיים לכולם' && lv.cancel === 'ביטול' && lv.still, lv);
  await tapSel(A, '.ndo-sheet [data-ndc="keep"]');
  const goneA = await until(A, `!window.__nlStudio.call&&!${R}.querySelector('.ndo')&&!!${R}.querySelector('.ndo-end')`, 5000);
  const endA = await A.ev(`(()=>{const e=${R}.querySelector('.ndo-end');return {h:e.querySelector('h2').textContent,lines:e.querySelectorAll('.ndo-chg li').length,share:e.querySelector('[data-ndc="share"]').textContent.trim(),alone:e.querySelector('[data-ndc="alone"]').textContent.trim(),thumbs:e.querySelectorAll('.ndo-ba svg').length}})()`);
  await A.shot('11-end-phone');
  check('the end: "השיחה הסתיימה. העיצוב שמור אצלכם." with before / after plans and the changes by person', goneA >= 0 && endA.h === 'השיחה הסתיימה. העיצוב שמור אצלכם.' && endA.thumbs === 2 && endA.lines >= 1 && endA.share === 'לשלוח את הסיכום בוואטסאפ' && endA.alone === 'להמשיך לעצב לבד', endA);
  const leftB = await until(B, `${C_}&&${C_}.participants().length===1&&(${C_}.stats.left||0)>=1`, 15000, 50);
  const toastB = await txt(B, '[data-ndc="toast"]');
  check('7. B sees that A left, keeps the same design and is now the host', leftB >= 0 && toastB === 'דנה יצא/ה מהשיחה. העיצוב נשאר אצלך.' && (await designOf(B)) === keep && (await B.ev(`${C_}.host`)) !== idA, { toast: toastB, left_after_ms: leftB });
  await tapSel(A, '.ndo-end [data-ndc="alone"]'); await sleep(300);
  check('7. "להמשיך לעצב לבד" gives A the designer back', !!(await A.ev(`!!${D}&&!${R}.querySelector('.ndo-end')`)));
  await A.shot('11-end-continue-phone');
  await tapSel(B, '.ndo-bar [data-ndc="leave"]'); await until(B, `!!${R}.querySelector('.ndo-sheet [data-ndc="keep"]')`, 2000);
  const lvB = await B.ev(`(()=>{const s=${R}.querySelector('.ndo-sheet');return {keep:s.querySelector('[data-ndc="keep"]').textContent.trim(),endall:!!s.querySelector('[data-ndc="endall"]')}})()`);
  await tapSel(B, '.ndo-sheet [data-ndc="keep"]');
  const goneB = await until(B, `!window.__nlStudio.call`, 5000);
  check('a guest (or the last one) leaves after one short confirm "יציאה"', lvB.keep === 'יציאה' && !lvB.endall && goneB >= 0, lvB);
  await B.shot('11-end-desktop');

  // ---- 8. no errors in the console ----
  for (const p of [A, B]) {
    const errs = p.errors.filter((e) => LIVEMODE || !/favicon\.ico/.test(e));
    const ours = errs.filter((e) => /assets\/designer|livekit|call\.js|studio\.js|designer\.js|core\.js|space\.js|plan\.js|designer\/call/i.test(e));
    if (LIVEMODE) check('8. no console errors from the designer or the call (' + p.label + ')', ours.length === 0, { ours: ours.slice(0, 6), other_page_errors: errs.filter((e) => !ours.includes(e)).map((e) => e.slice(0, 160)).slice(0, 6) });
    else check('8. no console errors (' + p.label + '; the local server has no favicon, that 404 is not counted)', errs.length === 0, errs.slice(0, 6));
    if (p.covered) receipt.numbers['covered_controls_' + p.label] = p.covered;
  }
} catch (e) { console.error(e); fails++; receipt.error = String((e && e.stack) || e); for (const p of [A, B]) if (p && p.errors.length) console.error(p.label + ' page errors:', p.errors.slice(0, 5)); }

receipt.passed = receipt.checks.filter((c) => c.ok).length; receipt.failed = fails;
fs.writeFileSync(path.join(OUT, 'receipt-live.json'), JSON.stringify(receipt, null, 2));
console.log('\nnumbers ' + JSON.stringify(receipt.numbers));
console.log(receipt.passed + ' passed, ' + fails + ' failed  (screenshots and receipt in ' + OUT + ')');
for (const b of browsers) { await b.close?.(); try { b.proc.kill(); } catch (e) { /* none */ } }
await sleep(1200);
for (const b of browsers) { for (let i = 0; i < 5; i++) { try { fs.rmSync(b.profile, { recursive: true, force: true }); break; } catch (e) { await sleep(500); } } }
process.exit(fails ? 1 : 0);
