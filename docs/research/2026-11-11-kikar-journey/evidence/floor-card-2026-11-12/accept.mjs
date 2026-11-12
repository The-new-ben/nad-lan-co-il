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

const J = async (x) => JSON.parse(await ev(x));
const CARD = `(()=>{const e=document.querySelector('.nlsr'); const c=e.querySelector('.nlsr-card'); const st=e.querySelector('.nlsr-stage').getBoundingClientRect(); if(!c||c.hidden||!c.offsetParent) return JSON.stringify({card:null});
 const r=c.getBoundingClientRect(); const h=c.querySelector('[aria-expanded]'); const top=Math.max(st.top,r.top), bot=Math.min(st.bottom,r.bottom);
 const band=[...e.querySelectorAll('.nlsr-stage *')].filter(x=>/band|sel|pick|floorline|fl/.test(x.className&&x.className.baseVal!==undefined?x.className.baseVal:String(x.className))&&x.offsetParent!==null).map(x=>{const b=x.getBoundingClientRect(); return [String(x.className.baseVal!==undefined?x.className.baseVal:x.className).slice(0,40),Math.round(b.top),Math.round(b.height)]}).slice(0,6);
 const small=[...c.querySelectorAll('button,a')].filter(b=>b.offsetParent).map(b=>{const q=b.getBoundingClientRect(); return [(b.innerText||b.getAttribute('aria-label')||'').trim().slice(0,28),Math.round(q.width),Math.round(q.height)]});
 return JSON.stringify({top:Math.round(r.top),h:Math.round(r.height),cover:+(Math.max(0,bot-top)/st.height).toFixed(2),exp:h?h.getAttribute('aria-expanded'):null,title:(c.querySelector('h3,h2,[class*=title],[class*=name],b,strong')||c).innerText.trim().split(String.fromCharCode(10))[0].slice(0,60),band,btns:small,cls:c.className,stageBottom:Math.round(st.bottom),stageTop:Math.round(st.top)})})()`;
console.log('PEEK', await ev(CARD));
console.log('classes in stage:', await ev(`[...new Set([...document.querySelectorAll('.nlsr-stage *')].map(x=>String(x.className.baseVal!==undefined?x.className.baseVal:x.className)).filter(Boolean))].join(' | ').slice(0,700)`));
const hrect = async () => J(`(()=>{const h=document.querySelector('.nlsr-card [aria-expanded]'); if(!h) return 'null'; const r=h.getBoundingClientRect(); return JSON.stringify([r.left+r.width/2,r.top+r.height/2])})()`);
const st2 = async () => J(GEO);
// 1 expand by handle
let hp = await hrect(); if (hp) { await tap(hp[0], hp[1]); await sleep(900); } console.log('EXPANDED', await ev(CARD)); await shot('5-expanded');
// 2 collapse by handle
hp = await hrect(); if (hp) { await tap(hp[0], hp[1]); await sleep(900); } console.log('collapse by handle ->', (await J(CARD)).exp, (await J(CARD)).h);
// 3 expand, collapse by Esc
hp = await hrect(); await tap(hp[0], hp[1]); await sleep(700); await send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Escape', code: 'Escape', windowsVirtualKeyCode: 27 }); await send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Escape', code: 'Escape', windowsVirtualKeyCode: 27 }); await sleep(800); console.log('collapse by Esc ->', (await J(CARD)).exp, (await J(CARD)).h);
// 4 expand, collapse by swipe down
hp = await hrect(); await tap(hp[0], hp[1]); await sleep(700); { const c = await J(CARD); const cx = W / 2, cy = c.top + 12; if (W < 900) { await send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: cx, y: cy }] }); for (let i = 1; i <= 10; i++) { await send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: cx, y: cy + i * 14 }] }); await sleep(16); } await send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }); } else { await send('Input.dispatchMouseEvent', { type: 'mousePressed', x: cx, y: cy, button: 'left', clickCount: 1 }); for (let i = 1; i <= 10; i++) await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: cx, y: cy + i * 14, button: 'left' }); await send('Input.dispatchMouseEvent', { type: 'mouseReleased', x: cx, y: cy + 140, button: 'left', clickCount: 1 }); } await sleep(900); console.log('collapse by swipe ->', (await J(CARD)).exp, (await J(CARD)).h, 'scrollY', await ev('Math.round(scrollY)')); }
// 5 expand, collapse by tap on the tower; and does that tap also change the floor?
hp = await hrect(); await tap(hp[0], hp[1]); await sleep(700); { const g = await st2(); const before = (await J(CARD)).title; await tap(g.stage[0] + g.stage[2] / 2, g.stage[1] + g.stage[3] * 0.2); await sleep(1200); const a = await J(CARD); console.log('collapse by stage tap ->', a.exp, a.h, '| title', before, '=>', a.title); }
// 6 lowest and highest floors tappable in peek
{ const g = await st2(); const c = await J(CARD); await tap(g.stage[0] + g.stage[2] / 2, c.top - 14); await sleep(1300); const lo = await J(CARD); await shot('6-lowest'); await tap(g.stage[0] + g.stage[2] / 2, g.stage[1] + 70); await sleep(1300); const hi = await J(CARD); console.log('lowest tap ->', lo.title, lo.band, '| highest tap ->', hi.title, hi.band); await shot('7-highest'); }
console.log('FINAL', await ev(CARD), 'docW', await ev('document.documentElement.scrollWidth'), 'vw', W);
ws.close(); ch.kill(); await sleep(300); await fs.rm(dir, { recursive: true, force: true }).catch(() => {});
