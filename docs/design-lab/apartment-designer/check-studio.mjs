// HAD-708 press check of the page every project opens for "עיצוב הדירה" (/tour/designer/) and of the plan chooser (studio.js).
// Serve the plugin at the live paths first:  python docs/tools/design-studio/serve_local.py 47962
//   node docs/design-lab/apartment-designer/check-studio.mjs [base, default http://127.0.0.1:47962] [shots folder]
// Headless Chrome over CDP with the real GPU; a phone (390x844, touch) and a desktop (1440x900).
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const BASE = process.argv[2] || 'http://127.0.0.1:47962';
const LIVE = /^https:/.test(BASE);
const SHOTS = process.argv[3] || path.join(os.tmpdir(), 'nd-studio-shots');
fs.mkdirSync(SHOTS, { recursive: true });
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let pass = 0, fail = 0;
const ok = (name, cond, extra) => { if (cond) { pass += 1; console.log('ok   ' + name); } else { fail += 1; console.log('FAIL ' + name + (extra !== undefined ? '  -> ' + JSON.stringify(extra) : '')); } };

async function session(w, h, mobile) {
  const PORT = 9300 + Math.floor(Math.random() * 400), profile = path.join(os.tmpdir(), 'nd-studio-' + PORT);
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
  await send('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: mobile ? 2 : 1, mobile });
  if (mobile) await send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
  const go = async (u, wait = 6000) => { await send('Page.navigate', { url: u }); await sleep(wait); };
  const shot = async (name) => { const d = await send('Page.captureScreenshot', { format: 'png' }); fs.writeFileSync(path.join(SHOTS, name + '.png'), Buffer.from(d.data, 'base64')); };
  const tap = async (expr) => { // a real pointer press in the middle of the element the expression returns
    const r = await ev(`(()=>{const e=${expr};if(!e)return null;e.scrollIntoView({block:'center',inline:'center'});const b=e.getBoundingClientRect();return [b.left+b.width/2,b.top+b.height/2]})()`);
    if (!r || typeof r === 'string') return false;
    if (mobile) { await send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: r[0], y: r[1] }] }); await send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }); }
    else { await send('Input.dispatchMouseEvent', { type: 'mousePressed', x: r[0], y: r[1], button: 'left', clickCount: 1 }); await send('Input.dispatchMouseEvent', { type: 'mouseReleased', x: r[0], y: r[1], button: 'left', clickCount: 1 }); }
    return true;
  };
  return { ev, go, shot, tap, errors, close: async () => { ws.close(); chrome.kill(); await sleep(1200); try { fs.rmSync(profile, { recursive: true, force: true, maxRetries: 5, retryDelay: 400 }); } catch (e) { /* the profile folder stays; nothing depends on it */ } } };
}
const SR = "document.getElementById('host').shadowRoot";
const state = `JSON.stringify({pick:[...document.querySelectorAll('#pick button')].map(b=>b.textContent+'|'+b.getAttribute('aria-pressed')),` +
  `h2:(${SR}&&${SR}.querySelector('header h2')||{}).textContent||'',sub:(${SR}&&${SR}.querySelector('[data-nd="sub"]')||{}).textContent||'',` +
  `pm:!!(${SR}&&${SR}.querySelector('.pm')),edit:!!(${SR}&&${SR}.querySelector('[data-nd="editplan"]')),tip:!document.getElementById('tip').hidden,` +
  `host:Math.round(document.getElementById('host').getBoundingClientRect().height),sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth,` +
  `back:document.getElementById('back').getAttribute('href'),ttl:document.getElementById('ttl').textContent})`;
const st = async (s) => JSON.parse(await s.ev(state));
const Q = '?project=rainbow-tel-aviv&unit=S1-5-w&pn=' + encodeURIComponent('פרויקט לבדיקה') + '&ul=' + encodeURIComponent('קומה 5 · מערב · 4 חדרים');

// ------------------------------------------------------------------ the phone
{
  const s = await session(390, 844, true);
  await s.go(BASE + '/tour/designer/' + Q);
  let v = await st(s);
  ok('phone: four choices, "my plan" first', v.pick.length === 4 && v.pick[0].startsWith('התוכנית שלי'), v.pick);
  ok('phone: opens on the unit\'s room count (4)', v.pick.some((x) => x === '4 חדרים|true'), v.pick);
  ok('phone: the designer names the plan as an example, not the project\'s', v.h2 === 'דירה לדוגמה' && v.sub.includes('לא תוכנית הדירה בפרויקט'), [v.h2, v.sub]);
  ok('phone: the page bar names the project and the unit', v.ttl.includes('פרויקט לבדיקה'), v.ttl);
  ok('phone: the way back is the project page', v.back === '/projects/rainbow-tel-aviv/', v.back);
  ok('phone: nothing wider than the screen, the designer has its height', v.sw === v.cw && v.host > 480, [v.sw, v.cw, v.host]);
  ok('phone: the tip about "my plan" shows on a first visit', v.tip === true);
  await s.shot('phone-1-project');
  ok('phone: a press on "3 חדרים"', await s.tap(`[...document.querySelectorAll('#pick button')].find(b=>b.textContent==='3 חדרים')`)); await sleep(4000);
  v = await st(s);
  ok('phone: the designer is now the 3 room example', v.pick.some((x) => x === '3 חדרים|true') && v.sub.includes('3 חדרים'), [v.pick, v.sub]);
  // the request path
  ok('phone: a press on "send"', await s.tap(`document.getElementById('send')`)); await sleep(1500);
  const wa = await s.ev(`(()=>{const d=document.getElementById('dlg');return JSON.stringify({open:d.open,href:decodeURIComponent(document.getElementById('wa').href)})})()`);
  const waj = JSON.parse(wa);
  ok('phone: the dialog opens with the WhatsApp message written from the design', waj.open && waj.href.includes('wa.me/972525101555?text=') && waj.href.includes('פרויקט: פרויקט לבדיקה') && waj.href.includes('שטח:') && waj.href.includes('אשמח שנתקדם'), waj.href.slice(0, 300));
  await s.shot('phone-2-send');
  await s.ev(`document.getElementById('dlg').close()`);
  // my plan: the planmaker
  ok('phone: a press on "my plan"', await s.tap(`document.querySelector('#pick button.is-mine')`)); await sleep(3500);
  v = await st(s);
  const txt = await s.ev(`${SR}.querySelector('.pm').textContent.slice(0,400)`);
  ok('phone: the planmaker opens inside the same frame', v.pm && v.host > 480 && String(txt).includes('מעצבים את הדירה שלכם'), [v.pm, v.host, String(txt).slice(0, 80)]);
  ok('phone: the tip left, nothing wider than the screen', v.tip === false && v.sw === v.cw, [v.tip, v.sw]);
  await s.shot('phone-3-myplan-start');
  // a finished plan, built by the real planbuild.js, as the planmaker stores it
  const made = await s.ev(`(async()=>{const pb=await import('/wp-content/plugins/nadlan-config/assets/designer/planbuild.js');const keys=pb.roomChoices('he');const key=(n)=>(keys.find(k=>k.name_he===n||k.label===n||k.he===n)||keys[0]);` +
    `const R=(x0,y0,x1,y1)=>[[x0,y0,x1,y0],[x1,y0,x1,y1],[x1,y1,x0,y1],[x0,y1,x0,y0]];const segs=[...R(0,0,500,400),...R(500,0,850,400)].map(q=>({a:[q[0],q[1]],b:[q[2],q[3]],kind:'partition'}));` +
    `const draft={schema:'nadlan-myplan-draft',v:1,mode:'measure',cmPerPx:1,segments:segs,openings:[{id:'o1',p:[500,200],w:80,type:'door'}],rooms:[{at:[250,200],key:(key('סלון').key||key('סלון').id)},{at:[675,200],key:(key('חדר שינה').key||key('חדר שינה').id)}]};` +
    `const chk=pb.checkDraft(draft,{});const plan=pb.buildPlan(draft,{});if(!plan)return JSON.stringify({plan:false,chk,keys:keys.slice(0,3)});localStorage.setItem('nd-myplan',JSON.stringify({plan,draft}));return JSON.stringify({plan:true,rooms:plan.rooms.length,src:plan.source.kind,chk})})()`);
  const mj = JSON.parse(made);
  ok('phone: planbuild.js makes a valid apartment from a two room draft', mj.plan === true && mj.rooms === 2 && mj.src === 'own', mj);
  ok('phone: back to an example, then "my plan" again', await s.tap(`[...document.querySelectorAll('#pick button')].find(b=>b.textContent==='4 חדרים')`)); await sleep(3500);
  await s.tap(`document.querySelector('#pick button.is-mine')`); await sleep(4500);
  v = await st(s);
  ok('phone: the designer opens on MY plan, with the way back into the drawing', !v.pm && v.h2 === 'התוכנית שלי' && v.edit && v.pick[0] === 'התוכנית שלי|true', [v.h2, v.edit, v.pick[0], v.sub]);
  ok('phone: my plan reads its own rooms and area', /2 חדרים|חדרים/.test(v.sub) && /\d/.test(v.sub), v.sub);
  await s.shot('phone-4-myplan-3d');
  const wa2 = JSON.parse(await (async () => { await s.tap(`document.getElementById('send')`); await sleep(1500); return s.ev(`JSON.stringify({href:decodeURIComponent(document.getElementById('wa').href)})`); })());
  ok('phone: the message names "my plan"', wa2.href.includes('התוכנית: התוכנית שלי'), wa2.href.slice(0, 260));
  await s.ev(`document.getElementById('dlg').close()`);
  ok('phone: a press on "edit the plan"', await s.tap(`${SR}.querySelector('[data-nd="editplan"]')`)); await sleep(3500);
  v = await st(s);
  ok('phone: the drawing opens again', v.pm === true, v);
  await s.shot('phone-5-edit');
  // a return visit opens on my plan
  await s.go(BASE + '/tour/designer/' + Q, 7000);
  v = await st(s);
  ok('phone: a return visit opens on my plan', v.h2 === 'התוכנית שלי' && v.pick[0] === 'התוכנית שלי|true' && v.tip === false, [v.h2, v.pick[0], v.tip]);
  // from a project page with no parameters: the referrer names the project
  if (LIVE) { await s.go(BASE + '/projects/duo-tel-aviv/', 6000); await s.ev(`location.href='/tour/designer/'`); await sleep(8000); } // the live project page: leave it for the designer, as its own link does
  else { await s.go(BASE + '/projects/duo-tel-aviv/', 1500); await s.tap(`document.getElementById('plain')`); await sleep(7000); }
  v = await st(s);
  ok('phone: opened from a project page, the way back is that page', v.back === '/projects/duo-tel-aviv/', v.back);
  ok('phone: another project starts on an example, not on the first project\'s choice', v.pick.some((x) => x === '4 חדרים|true'), v.pick);
  ok('phone: no errors in the console', s.errors.length === 0, s.errors.slice(0, 4));
  await s.close();
}
// ------------------------------------------------------------------ the desktop, a project whose plans we hold
{
  const s = await session(1440, 900, false);
  await s.go(BASE + '/tour/designer/?project=ashira-sde-dov');
  let v = await st(s);
  ok('desktop: the project\'s four published plan types and "my plan"', v.pick.length === 5 && v.pick.filter((x) => x.includes('E-')).length === 4, v.pick);
  ok('desktop: opens on the default type, named as the published sales plan', v.h2 === 'טיפוס E-4A' && v.sub.includes('לפי תוכנית המכר שפורסמה'), [v.h2, v.sub]);
  await s.shot('desktop-1-project-plans');
  ok('desktop: a press on the 3 room type', await s.tap(`[...document.querySelectorAll('#pick button')].find(b=>b.textContent.includes('E-3B'))`)); await sleep(4500);
  v = await st(s);
  ok('desktop: the designer is now that type', v.h2 === 'טיפוס E-3B', v.h2);
  await s.go(BASE + '/tour/designer/');
  v = await st(s);
  ok('desktop: with no project, the examples and the way back to the design page', v.pick.length === 4 && v.back === '/design-studio/' && v.h2 === 'דירה לדוגמה', [v.pick, v.back, v.h2]);
  ok('desktop: no errors in the console', s.errors.length === 0, s.errors.slice(0, 4));
  await s.close();
}
console.log('\n' + pass + ' passed, ' + fail + ' failed | shots: ' + SHOTS);
process.exit(fail ? 1 : 0);
