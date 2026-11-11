import { spawn } from 'node:child_process'; import fs from 'node:fs/promises'; import os from 'node:os'; import path from 'node:path';
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe'; const URL_ = process.argv[2]; const OUT = process.argv[3]; const W = +(process.argv[4] || 390), H = +(process.argv[5] || 844);
const PORT = 9300 + Math.floor(Math.random() * 400); const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const dir = await fs.mkdtemp(path.join(os.tmpdir(), 'cd-')); const ch = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${dir}`, '--no-first-run', '--hide-scrollbars', '--enable-unsafe-swiftshader', 'about:blank'], { stdio: 'ignore' });
for (let i = 0; i < 80; i++) { try { await (await fetch(`http://127.0.0.1:${PORT}/json/version`)).json(); break; } catch { await sleep(250); } }
await fs.mkdir(OUT, { recursive: true });
const t = await (await fetch(`http://127.0.0.1:${PORT}/json/new?about:blank`, { method: 'PUT' })).json();
const ws = new WebSocket(t.webSocketDebuggerUrl); let id = 0; const P = new Map(); await new Promise((r) => (ws.onopen = r));
const send = (m, p = {}) => new Promise((ok, no) => { const i = ++id; P.set(i, { ok, no }); ws.send(JSON.stringify({ id: i, method: m, params: p })); });
ws.onmessage = (e) => { const m = JSON.parse(e.data); if (m.id && P.has(m.id)) { const q = P.get(m.id); P.delete(m.id); if (m.error) q.no(new Error(JSON.stringify(m.error))); else q.ok(m.result); } };
await send('Page.enable'); await send('Runtime.enable');
await send('Emulation.setDeviceMetricsOverride', { width: W, height: H, deviceScaleFactor: 2, mobile: W < 900 });
if (W < 900) await send('Emulation.setTouchEmulationEnabled', { enabled: true });
await send('Page.navigate', { url: URL_ });
const ev = async (x) => { const r = await send('Runtime.evaluate', { expression: x, awaitPromise: true, returnByValue: true }); return r.exceptionDetails ? 'EXC ' + JSON.stringify(r.exceptionDetails).slice(0, 400) : r.result.value; };
for (let i = 0; i < 45 && !(await ev("!!document.querySelector('.nlsr .nlsr-h')")); i++) await sleep(1000);
const shot = async (n) => { const r = await send('Page.captureScreenshot', { format: 'jpeg', quality: 72 }); await fs.writeFile(path.join(OUT, n + '.jpg'), Buffer.from(r.data, 'base64')); };
const tap = async (x, y) => { if (W < 900) { await send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x, y }] }); await sleep(60); await send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }); } else { await send('Input.dispatchMouseEvent', { type: 'mousePressed', x, y, button: 'left', clickCount: 1 }); await send('Input.dispatchMouseEvent', { type: 'mouseReleased', x, y, button: 'left', clickCount: 1 }); } };
const GEO = `(()=>{const e=document.querySelector('.nlsr'); if(!e) return 'no showroom'; const R=(s)=>{const x=e.querySelector(s); if(!x||x.hidden||!x.offsetParent) return null; const r=x.getBoundingClientRect(); return [Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)]};
 const st=R('.nlsr-stage'), cd=R('.nlsr-card'); let cover=null; if(st&&cd){const top=Math.max(st[1],cd[1]), bot=Math.min(st[1]+st[3],cd[1]+cd[3]); cover=Math.max(0,bot-top)/st[3];}
 const c=e.querySelector('.nlsr-card'); const btns=c?[...c.querySelectorAll('button,a')].filter(b=>b.offsetParent).map(b=>(b.innerText||b.getAttribute('aria-label')||'').trim().split(String.fromCharCode(10)).join(' ').slice(0,40)+'@'+Math.round(b.getBoundingClientRect().width)+'x'+Math.round(b.getBoundingClientRect().height)):[];
 return JSON.stringify({lang:e.lang,dir:e.dir,vh:innerHeight,stage:st,card:cd,cover:cover==null?null:+cover.toFixed(2),cardPos:c?getComputedStyle(c).position:null,cardBtns:btns,hint:(e.querySelector('.nlsr-hint')||{}).innerText,back:R('.nlsr-back')||R('[data-act=all]'),map:R('.nlsr-map')})})()`;
await ev(`(function(){var s=document.querySelector('.nlsr'); window.scrollTo(0, s.getBoundingClientRect().top+scrollY-60)})()`); await sleep(2500);
console.log('S1', await ev(GEO)); await shot('1-landing');
await ev(`document.querySelector('.nlsr-h[data-tower="B"]').click()`); await sleep(2500);
console.log('S2', await ev(GEO)); await shot('2-tower');
const st = JSON.parse(await ev(GEO)).stage; const x = st[0] + st[2] / 2, y = st[1] + st[3] * 0.42; await tap(x, y); await sleep(2500);
console.log('S3', await ev(GEO)); await shot('3-floor-card');
// try the ways out: Escape, tap on the stage above the card, swipe the card down
await send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Escape', code: 'Escape', windowsVirtualKeyCode: 27 }); await send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Escape', code: 'Escape', windowsVirtualKeyCode: 27 }); await sleep(800);
console.log('after Esc', JSON.parse(await ev(GEO)).card);
const g = JSON.parse(await ev(GEO)); if (g.card) { const cx = g.card[0] + g.card[2] / 2, cy = g.card[1] + 14;
  if (W < 900) { await send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: cx, y: cy }] }); for (let i = 1; i <= 10; i++) { await send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: cx, y: cy + i * 22 }] }); await sleep(16); } await send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }); }
  await sleep(1200); console.log('after swipe down', JSON.parse(await ev(GEO)).card, 'scrollY', await ev('Math.round(scrollY)')); await shot('4-after-swipe'); }
ws.close(); ch.kill(); await sleep(300); await fs.rm(dir, { recursive: true, force: true }).catch(() => {});
