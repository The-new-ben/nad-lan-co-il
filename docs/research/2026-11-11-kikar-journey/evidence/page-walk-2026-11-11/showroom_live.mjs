// HAD-712: walk the LIVE Kikar showroom as a visitor (no local files): towers -> tap a tower -> tap a floor on it -> the card ->
// the apartment screen -> the basket. Asserts: the showroom is mounted, its direction, no Hebrew on a non-Hebrew page, script errors,
// failed requests. Saves a picture of each step.   node showroom_live.mjs <url> <outdir> <width> <height> <lang>
import { spawn } from 'node:child_process'; import fs from 'node:fs/promises'; import os from 'node:os'; import path from 'node:path';
const [URL_, OUT, W, H, LANG] = process.argv.slice(2); const w = +W, h = +H, MOB = w < 900;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms)); const PORT = 9500 + Math.floor(Math.random() * 400);
const dir = await fs.mkdtemp(path.join(os.tmpdir(), 'sl-'));
const ch = spawn('C:/Program Files/Google/Chrome/Application/chrome.exe', ['--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${dir}`, '--no-first-run', '--hide-scrollbars', '--enable-unsafe-swiftshader', 'about:blank'], { stdio: 'ignore' });
for (let i = 0; i < 80; i++) { try { await (await fetch(`http://127.0.0.1:${PORT}/json/version`)).json(); break; } catch { await sleep(250); } }
await fs.mkdir(OUT, { recursive: true });
const t = await (await fetch(`http://127.0.0.1:${PORT}/json/new?about:blank`, { method: 'PUT' })).json();
const ws = new WebSocket(t.webSocketDebuggerUrl); let id = 0; const P = new Map(); const errs = [], bad = [];
await new Promise((r) => (ws.onopen = r));
const send = (m, p = {}) => new Promise((ok, no) => { const i = ++id; P.set(i, { ok, no }); ws.send(JSON.stringify({ id: i, method: m, params: p })); });
ws.onmessage = (e) => { const m = JSON.parse(e.data); if (m.id && P.has(m.id)) { const q = P.get(m.id); P.delete(m.id); m.error ? q.no(new Error(JSON.stringify(m.error))) : q.ok(m.result); return; }
  if (m.method === 'Runtime.exceptionThrown') errs.push(JSON.stringify(m.params.exceptionDetails).slice(0, 260));
  if (m.method === 'Network.responseReceived' && m.params.response.status >= 400 && !/favicon|google|facebook|hotjar|doubleclick/.test(m.params.response.url)) bad.push(m.params.response.status + ' ' + m.params.response.url.slice(-90)); };
await send('Page.enable'); await send('Runtime.enable'); await send('Network.enable');
await send('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: 1, mobile: MOB }); if (MOB) await send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
await send('Page.navigate', { url: URL_ });
const ev = async (x) => { const r = await send('Runtime.evaluate', { expression: x, awaitPromise: true, returnByValue: true }); return r.exceptionDetails ? 'EXC ' + JSON.stringify(r.exceptionDetails).slice(0, 200) : r.result.value; };
const shot = async (n) => { const s = await send('Page.captureScreenshot', { format: 'jpeg', quality: 72 }); await fs.writeFile(path.join(OUT, n + '.jpg'), Buffer.from(s.data, 'base64')); };
const heb = `(function(s){var m=s.match(/[\\u0590-\\u05FF][^<>]{0,30}/g)||[];return {n:m.length,ex:m.slice(0,4)}})`;
await sleep(10000);
const step = async (name, js, wait = 2500) => { const r = js ? await ev(js) : ''; await sleep(wait);
  const st = await ev(`JSON.stringify((function(){var sr=document.querySelector('.nlsr'),ck=document.querySelector('.nlck,[class*="nlck"]'),bk=document.querySelector('#nlbk,.nlbk,[class*="nlbk"]');
    var txt=(sr?sr.innerText:'')+' '+(ck&&ck.offsetParent?ck.innerText:'')+' '+(bk&&bk.offsetParent?bk.innerText:'');
    return {sr:!!sr, dir:sr&&sr.getAttribute('dir'), lang:sr&&sr.getAttribute('lang'), heb:${heb}(txt), card:!!document.querySelector('.nlsr-card'), scrollW:document.documentElement.scrollWidth}})())`);
  await shot(name); console.log(name, r, st); };
await step('1-towers', `(document.querySelector('.nlsr')||document.body).scrollIntoView({block:'start'}),'scrolled'`);
await step('2-tower', `(function(){var b=document.querySelector('.nlsr [data-tower="B"]')||document.querySelector('.nlsr [data-tower]');if(!b)return 'no tower button';b.click();return 'tower '+b.dataset.tower})()`, 4000);
await step('3-floor', `(function(){var st=document.querySelector('.nlsr-stage');if(!st)return 'no stage';var r=st.getBoundingClientRect();var x=r.left+r.width/2,y=r.top+r.height*0.42;var t=document.elementFromPoint(x,y);['pointerdown','pointerup','click'].forEach(function(n){t.dispatchEvent(new PointerEvent(n,{bubbles:true,clientX:x,clientY:y,pointerType:'touch'}))});return 'tap '+t.className})()`, 3500);
await step('4-apartment', `(function(){var b=document.querySelector('.nlsr [data-go="home"]');if(!b)return 'no enter';b.click();return 'enter'})()`, 4500);
await step('5-basket', `(function(){if(window.__nlBasket&&window.__nlBasket.open){window.__nlBasket.open();return 'basket open'}return 'no basket api'})()`, 3000);
console.log('errors', errs.length, errs.slice(0, 3)); console.log('http>=400', bad.length, bad.slice(0, 5));
ws.close(); ch.kill(); await sleep(300); await fs.rm(dir, { recursive: true, force: true }).catch(() => {});
