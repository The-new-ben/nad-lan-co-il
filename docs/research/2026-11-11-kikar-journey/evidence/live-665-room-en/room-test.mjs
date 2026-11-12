import { spawn } from 'node:child_process'; import fs from 'node:fs/promises'; import os from 'node:os'; import path from 'node:path';
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe'; const URL_ = process.argv[2]; const OUT = process.argv[3]; const W = 390, H = 844;
const PORT = 9300 + Math.floor(Math.random() * 400); const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const dir = await fs.mkdtemp(path.join(os.tmpdir(), 'rm-')); const ch = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${dir}`, '--no-first-run', '--hide-scrollbars', '--enable-unsafe-swiftshader', '--use-fake-ui-for-media-stream', '--use-fake-device-for-media-stream', '--autoplay-policy=no-user-gesture-required', 'about:blank'], { stdio: 'ignore' });
for (let i = 0; i < 80; i++) { try { await (await fetch(`http://127.0.0.1:${PORT}/json/version`)).json(); break; } catch { await sleep(250); } }
await fs.mkdir(OUT, { recursive: true });
const t = await (await fetch(`http://127.0.0.1:${PORT}/json/new?about:blank`, { method: 'PUT' })).json();
const ws = new WebSocket(t.webSocketDebuggerUrl); let id = 0; const P = new Map(); await new Promise((r) => (ws.onopen = r));
const send = (m, p = {}) => new Promise((ok, no) => { const i = ++id; P.set(i, { ok, no }); ws.send(JSON.stringify({ id: i, method: m, params: p })); });
const net = []; const errs = [];
ws.onmessage = (e) => { const m = JSON.parse(e.data); if (m.id && P.has(m.id)) { const q = P.get(m.id); P.delete(m.id); if (m.error) q.no(new Error(JSON.stringify(m.error))); else q.ok(m.result); return; }
  if (m.method === 'Network.responseReceived') { const u = m.params.response.url; if (/\/room|livekit|wss:/.test(u)) net.push(m.params.response.status + ' ' + u.replace(/\?.*$/, '').slice(0, 110)); }
  if (m.method === 'Network.webSocketCreated') net.push('WS ' + m.params.url.replace(/\?.*$/, '').replace(/[a-z0-9-]+\.livekit\.cloud/, '<livekit-host>').slice(0, 80));
  if (m.method === 'Runtime.exceptionThrown') errs.push(JSON.stringify(m.params.exceptionDetails).slice(0, 200)); };
await send('Page.enable'); await send('Runtime.enable'); await send('Network.enable');
await send('Emulation.setDeviceMetricsOverride', { width: W, height: H, deviceScaleFactor: 2, mobile: true });
await send('Page.navigate', { url: URL_ });
const ev = async (x) => { const r = await send('Runtime.evaluate', { expression: x, awaitPromise: true, returnByValue: true, userGesture: true }); return r.exceptionDetails ? 'EXC ' + JSON.stringify(r.exceptionDetails).slice(0, 300) : r.result.value; };
const shot = async (n) => { const r = await send('Page.captureScreenshot', { format: 'jpeg', quality: 70 }); await fs.writeFile(path.join(OUT, n + '.jpg'), Buffer.from(r.data, 'base64')); };
const ROOM = `(()=>{const r=document.body; const vis=!!document.querySelector('[class*=nltg],[class*=nltr]'); const txt=((document.querySelector('[class*=nltg],[class*=nltr]')||{}).innerText||'').split(String.fromCharCode(10)).map(s=>s.trim()).filter(Boolean).slice(0,24);
 return JSON.stringify({vis,url:location.search.replace(/room=([a-z0-9]{4})[a-z0-9]*/,'room=$1...'),inputs:[...r.querySelectorAll('input,select,textarea')].filter(x=>x.offsetParent).map(x=>x.type+':'+(x.placeholder||x.name||x.id)),btns:[...r.querySelectorAll('[class*=nltg] button,[class*=nltr] button,[class*=nltg] a,[class*=nltr] a')].filter(b=>b.offsetParent).map(b=>(b.innerText||b.getAttribute('aria-label')||'').trim().slice(0,30)),videos:[...r.querySelectorAll('video')].map(v=>[v.readyState,v.videoWidth,v.videoHeight,v.paused]),txt})})()`;
await sleep(9000); console.log('T+9s', await ev(ROOM)); await shot('1-open');
// enter a name if asked, then press the first primary button
console.log('fill:', await ev(`(()=>{const r=document.body; const i=[...r.querySelectorAll('input[type=text],input:not([type])')].find(x=>x.offsetParent); if(!i) return 'no name field'; const set=Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set; set.call(i,'Claude test, please ignore'); i.dispatchEvent(new Event('input',{bubbles:true})); const f=i.closest('form')||i.closest('[class*=nltg],[class*=nltr]')||r; const bs=[...f.querySelectorAll('button')].filter(b=>b.offsetParent); const b=bs.find(b=>b.type==='submit')||bs.reduce((a,c)=>(!a||c.getBoundingClientRect().width>a.getBoundingClientRect().width)?c:a,null); if(b){b.click(); return 'clicked '+(b.innerText||'').trim().slice(0,30)} return 'no button'})()`));
await sleep(12000); console.log('T+21s', await ev(ROOM)); await shot('2-joined');
await sleep(Number(process.env.WAITMS||55000)); console.log('T+76s', await ev(ROOM)); await shot('3-after-a-minute');
console.log('NET', JSON.stringify([...new Set(net)].slice(0, 30))); console.log('ERR', errs.slice(0, 5));
// leave politely if there is a leave/end control
console.log('leave:', await ev(`(()=>{const r=document.body; const b=[...r.querySelectorAll('[class*=nltg] button,[class*=nltr] button,[class*=nltg] a')].filter(b=>b.offsetParent).find(x=>/leave|end|סיום|יציאה|לצאת/i.test((x.innerText||x.getAttribute('aria-label')||''))); if(b){b.click(); return 'clicked '+(b.innerText||b.getAttribute('aria-label')||'').trim().slice(0,30)} return 'no leave control found'})()`));
await sleep(2500); await shot('4-left');
ws.close(); ch.kill(); await sleep(300); await fs.rm(dir, { recursive: true, force: true }).catch(() => {});
