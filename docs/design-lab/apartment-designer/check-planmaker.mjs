// node check-planmaker.mjs [--port=47961] [--shots=<folder>]
// Presses "my plan" (plugins/nadlan-config/assets/designer/planmaker.js) in headless Chrome, by touch on a 390 x 844 phone
// and by mouse on a 1440 x 900 desktop: a synthetic 3-room plan picture is loaded as a file, the scale is marked, the walls
// are traced, a door and a window added, the rooms named, and the designer must open on THIS plan with the right rooms
// and areas. Also: the "from sizes" route, save to a file and load it back, reload and continue, a one-page PDF.
// Serve the repo root first:  python -m http.server 47961 --bind 127.0.0.1   (run from the repo root)
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const arg = (k, d) => { const a = process.argv.find((x) => x.startsWith('--' + k + '=')); return a ? a.slice(k.length + 3) : d; };
const URL0 = 'http://127.0.0.1:' + arg('port', '47961') + '/docs/design-lab/apartment-designer/planmaker-harness.html';
const here = path.dirname(fileURLToPath(import.meta.url));
const shots = arg('shots', path.join(here, 'planmaker-evidence'));
fs.mkdirSync(shots, { recursive: true });
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe', PORT = 9300 + Math.floor(Math.random() * 500), profile = path.join(os.tmpdir(), 'nd-pm-' + PORT);
const chrome = spawn(CHROME, ['--headless=new', '--remote-debugging-port=' + PORT, '--user-data-dir=' + profile, '--no-first-run', '--disable-extensions', '--ignore-gpu-blocklist', '--enable-gpu', '--use-angle=d3d11', '--lang=he-IL'], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
for (let i = 0; i < 80; i++) { try { if ((await fetch('http://127.0.0.1:' + PORT + '/json/version')).ok) break; } catch {} await sleep(250); }
const receipt = { when: new Date().toISOString(), checks: [] }; let fails = 0;
const check = (name, ok, detail) => { receipt.checks.push({ name, ok: !!ok, detail }); if (!ok) fails++; console.log((ok ? 'ok   ' : 'FAIL ') + name + (detail !== undefined ? '  ' + (typeof detail === 'string' ? detail : JSON.stringify(detail)) : '')); };

// the synthetic plan: 900 x 600 cm, outer walls 25 cm, an inner wall at x 500 and one at y 300 from x 500 to 900.
// Truth (clear inside sizes): living 482.5 x 575, two bedrooms 382.5 x 282.5 = 49.36 m2 in all.
const TRUTH = (482.5 * 575 + 2 * 382.5 * 282.5) / 1e4;
const PXCM = 1.1, M = 120; // picture pixels per cm and the margin of the sheet
const IMG = (x, y) => [M + x * PXCM, M + y * PXCM];

// a one-page PDF of the same plan, drawn with PyMuPDF
const pdfPath = path.join(os.tmpdir(), 'nd-pm-plan-' + PORT + '.pdf');
execFileSync('python', ['-c', `
import fitz, sys
doc = fitz.open(); pg = doc.new_page(width=842, height=595)
s, ox, oy = 0.62, 140, 110
pg.draw_rect(fitz.Rect(ox, oy, ox + 900*s, oy + 600*s), color=(0, 0, 0), width=25*s)
pg.draw_line(fitz.Point(ox + 500*s, oy), fitz.Point(ox + 500*s, oy + 600*s), color=(0, 0, 0), width=10*s)
pg.draw_line(fitz.Point(ox + 500*s, oy + 300*s), fitz.Point(ox + 900*s, oy + 300*s), color=(0, 0, 0), width=10*s)
pg.insert_text(fitz.Point(ox + 400*s, oy - 18), "900", fontsize=14)
doc.save(sys.argv[1])
`, pdfPath]);

async function page(w, h, dpr, mobile) {
  const t = await (await fetch('http://127.0.0.1:' + PORT + '/json/new?about:blank', { method: 'PUT' })).json();
  const ws = new WebSocket(t.webSocketDebuggerUrl); let id = 0; const pend = new Map(), errors = [];
  ws.onmessage = (ev) => { const m = JSON.parse(ev.data); if (m.id && pend.has(m.id)) { pend.get(m.id)(m.result || m.error); pend.delete(m.id); } else if (m.method === 'Runtime.exceptionThrown') errors.push(m.params.exceptionDetails.text + ' ' + ((m.params.exceptionDetails.exception || {}).description || '')); else if (m.method === 'Runtime.consoleAPICalled' && m.params.type === 'error') errors.push(m.params.args.map((a) => a.value || a.description).join(' ')); else if (m.method === 'Log.entryAdded' && m.params.entry.level === 'error' && !/favicon/.test(m.params.entry.url || '')) errors.push('log: ' + m.params.entry.text + ' ' + (m.params.entry.url || '')); };
  await new Promise((r) => (ws.onopen = r));
  const send = (method, params = {}) => new Promise((res) => { const i = ++id; pend.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); });
  const ev = async (e) => { const r = await send('Runtime.evaluate', { expression: e, awaitPromise: true, returnByValue: true }); if (r.exceptionDetails) throw new Error(JSON.stringify(r.exceptionDetails.exception || r.exceptionDetails.text)); return r.result.value; };
  await send('Page.enable'); await send('Runtime.enable'); await send('Log.enable'); await send('DOM.enable');
  await send('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: dpr, mobile });
  if (mobile) await send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
  const go = async (q = '') => { await send('Page.navigate', { url: URL0 + '?t=' + Date.now() + q }); await sleep(300); for (let i = 0; i < 160; i++) { if (await ev('!!window.__ready').catch(() => false)) break; await sleep(200); } await sleep(500); await ev(`window.__see=(e)=>{const sc=e.closest('.pm-panel,.pm-names,.pm-start,.sheet');if(!sc)return;const r=e.getBoundingClientRect(),s=sc.getBoundingClientRect();if(r.bottom>s.bottom)sc.scrollTop+=r.bottom-s.bottom+4;if(r.top<s.top)sc.scrollTop-=s.top-r.top+4;}`); };
  const touch = (type, x, y) => send('Input.dispatchTouchEvent', { type, touchPoints: type === 'touchEnd' ? [] : [{ x, y, id: 1 }] });
  const mouse = (type, x, y) => send('Input.dispatchMouseEvent', { type, x, y, button: 'left', buttons: type === 'mouseReleased' ? 0 : 1, clickCount: 1 });
  return {
    ev, errors, send, go,
    shot: async (name) => { await sleep(120); const d = await send('Page.captureScreenshot', { format: 'png' }); fs.writeFileSync(path.join(shots, name + '.png'), Buffer.from(d.data, 'base64')); },
    tap: mobile ? async (x, y) => { await touch('touchStart', x, y); await sleep(40); await touch('touchEnd'); await sleep(170); } : async (x, y) => { await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x, y }); await mouse('mousePressed', x, y); await sleep(30); await mouse('mouseReleased', x, y); await sleep(170); },
    touch, sleep,
    close: async () => { ws.close(); await fetch('http://127.0.0.1:' + PORT + '/json/close/' + t.id).catch(() => {}); },
  };
}
const R = 'document.getElementById("app").shadowRoot';
const PM = 'window.__pm';

async function flow(p, tag, mobile) {
  const W = mobile ? 390 : 1440;
  const centre = (sel) => p.ev(`(()=>{const e=${R}.querySelector(${JSON.stringify(sel)});if(!e)return null;window.__see(e);const r=e.getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]})()`);
  const press = async (sel) => { const c = await centre(sel); if (!c) throw new Error('no element ' + sel); await p.tap(c[0], c[1]); };
  const byText = (txt) => `[...${R}.querySelectorAll('button')].find(b=>b.textContent.trim()===${JSON.stringify(txt)})`;
  const pressText = async (txt) => { const c = await p.ev(`(()=>{const b=${byText(txt)};if(!b)return null;window.__see(b);const r=b.getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]})()`); if (!c) throw new Error('no button ' + txt); await p.tap(c[0], c[1]); };
  const at = (x, y) => p.ev(`${PM}.screenOf(${x},${y})`);
  const tapImg = async (cx, cy) => { const s = await at(...IMG(cx, cy)); await p.tap(s[0], s[1]); };
  const type = async (sel, text) => { await p.ev(`(()=>{const i=${R}.querySelector(${JSON.stringify(sel)});i.focus();i.select&&i.select();})()`); await p.send('Input.insertText', { text }); await sleep(80); };
  const layout = (label) => p.ev(`(()=>{const r=${R};const bs=[...r.querySelectorAll('button,input,a')].filter(b=>{const q=b.getBoundingClientRect();return q.width>0&&q.height>0&&!b.closest('[hidden]')&&getComputedStyle(b).visibility!=='hidden'});
    const small=bs.filter(b=>b.type!=='range'&&b.getBoundingClientRect().height<43.5).map(b=>(b.textContent||b.getAttribute('aria-label')||b.tagName).trim().slice(0,30));
    const out=bs.filter(b=>{const q=b.getBoundingClientRect();return q.left<-1||q.right>innerWidth+1}).map(b=>b.textContent.trim().slice(0,30));
    const clip=[...r.querySelectorAll('button,h2,h3,h4,p,span,small,b,label')].filter(e=>{const q=e.getBoundingClientRect();return q.width>0&&!e.closest('[hidden]')&&e.scrollWidth>e.clientWidth+1&&getComputedStyle(e).overflow!=='visible'}).map(e=>e.textContent.trim().slice(0,30));
    return {small,out,clip,scroll:document.documentElement.scrollWidth<=innerWidth}})()`).then((l) => { check(tag + ' ' + label + ': nothing cut or off the screen, every control 44 px or more', l.scroll && !l.out.length && !l.clip.length && !l.small.length, l); return l; });

  const helper = `window.__see=(e)=>{const sc=e.closest('.pm-panel,.pm-names,.pm-start,.sheet');if(!sc)return;const r=e.getBoundingClientRect(),s=sc.getBoundingClientRect();if(r.bottom>s.bottom)sc.scrollTop+=r.bottom-s.bottom+4;if(r.top<s.top)sc.scrollTop-=s.top-r.top+4;}`;
  // ---- a clean device ----
  await p.go(); await p.ev(helper);
  await p.ev('localStorage.clear(); new Promise(r=>{const q=indexedDB.deleteDatabase("nd-myplan");q.onsuccess=q.onerror=q.onblocked=()=>r(1)})');
  await p.go();
  const st = await p.ev(`(()=>{const r=${R};return {h:r.querySelector('header h2').textContent,h3:r.querySelector('.pm-h').textContent,lead:r.querySelector('.pm-lead').textContent,opts:[...r.querySelectorAll('.pm-opt h4')].map(e=>e.textContent),priv:r.querySelector('.pm-privacy').textContent,help:(r.querySelector('.pm-help')||{}).textContent,camera:!!${byText('צילום התוכנית')},font:getComputedStyle(r.querySelector('.pm-h')).fontFamily,radius:getComputedStyle(r.querySelector('button')).borderRadius}})()`);
  check(tag + ' opening screen: the owner\'s words, three ways in, the privacy line and the help link', st.h3 === 'מעצבים את הדירה שלכם, לא דירה לדוגמה' && st.lead.includes('אפשר גם קומה שלמה') && st.opts.join('|') === 'יש לי תוכנית|אין לי תוכנית|יש לי קובץ שמור' && st.priv === 'התוכנית נשארת במכשיר שלכם. היא לא נשלחת לאתר ולא נשמרת אצלנו.' && st.help === 'איפה משיגים את תוכנית הדירה?', st);
  check(tag + ' the camera button only on a touch device', st.camera === mobile);
  check(tag + ' the site CSS does not reach the tool (square corners, Plex)', st.radius === '0px' && /Plex/.test(st.font), st);
  await layout('opening screen');
  await p.shot(tag + '-01-start');

  // ---- 1. load the picture as a file ----
  await p.ev(`(async()=>{const c=document.createElement('canvas');c.width=${Math.round(900 * PXCM + 2 * M)};c.height=${Math.round(600 * PXCM + 2 * M)};const x=c.getContext('2d');x.fillStyle='#fbfbf8';x.fillRect(0,0,c.width,c.height);
    const P=(a,b)=>[${M}+a*${PXCM},${M}+b*${PXCM}];x.strokeStyle='#111';x.lineCap='square';
    const L=(a,b,c2,d,w)=>{x.lineWidth=w*${PXCM};x.beginPath();x.moveTo(...P(a,b));x.lineTo(...P(c2,d));x.stroke();};
    L(0,0,900,0,25);L(900,0,900,600,25);L(900,600,0,600,25);L(0,600,0,0,25);L(500,0,500,600,10);L(500,300,900,300,10);
    x.fillStyle='#111';x.font='22px Arial';x.fillText('900',P(430,-60)[0],P(0,-60)[1]);x.fillText('600',P(-90,300)[0],P(0,300)[1]);
    const b=await new Promise(r=>c.toBlob(r,'image/png'));const f=new File([b],'plan.png',{type:'image/png'});const dt=new DataTransfer();dt.items.add(f);
    const i=${R}.querySelector('[data-pm="file"]');i.files=dt.files;i.dispatchEvent(new Event('change',{bubbles:true}));})()`);
  for (let i = 0; i < 40 && (await p.ev(`${PM}.step`)) !== 'scale'; i++) await sleep(150);
  await sleep(400);
  const s1 = await p.ev(`({step:${PM}.step,photo:${PM}.hasPhoto,head:${R}.querySelector('header h2').textContent,steps:[...${R}.querySelectorAll('.pm-steps button span')].map(e=>e.textContent)})`);
  check(tag + ' the picture opens on step 1, the scale, with the four numbered steps', s1.step === 'scale' && s1.photo && s1.head === 'מסמנים קיר אחד שהאורך שלו ידוע' && s1.steps.join('|') === 'קנה מידה|קירות|דלתות וחלונות|חדרים', s1);
  await layout('scale');
  await p.shot(tag + '-02-scale');
  // the photo can be straightened: open the four corners, then cancel (the picture is already straight)
  check(tag + ' the door shortcut: three doors 70, 80, 90 with the less-exact sentence', await p.ev(`(()=>{const r=${R};return ['70','80','90'].every(v=>!!r.querySelector('[data-act="door"][data-v="'+v+'"]'))&&r.querySelector('.pm-door small').textContent==='אין מידות בתוכנית? סמנו דלת פנימית. זה מדויק פחות: דלת היא 70, 80 או 90 ס״מ'})()`));
  await pressText('הצילום עקום? יישרו אותו');
  check(tag + ' "straighten" shows the four corners and the apply button', await p.ev(`!!${byText('יישור הצילום')}`));
  await p.shot(tag + '-03-straighten');
  await pressText('ביטול היישור');
  // mark the top outer wall end to end and type 900
  await tapImg(0, 0); await tapImg(900, 0);
  await type('[data-pm="in-len"]', '900');
  await p.shot(tag + '-04-scale-marked');
  await pressText('אישור קנה המידה'); await sleep(250);
  const sc = await p.ev(`(()=>{const d=${PM}.getDraft();return {step:d.step,k:d.cmPerPx}})()`);
  check(tag + ' the scale: 900 cm over 990 picture pixels', sc.step === 'walls' && Math.abs(sc.k - 900 / 990) < 0.002, sc);

  // ---- 2. walls ----
  await layout('walls');
  await p.shot(tag + '-05-walls-empty');
  await tapImg(0, 0); await tapImg(900, 0);
  if (mobile) { // the third corner by a real finger: down beside it, slide onto it, the magnifier shows, the point lands on lift
    const a = await at(...IMG(900, 600));
    await p.touch('touchStart', a[0] - 26, a[1] - 18); await sleep(60);
    for (let i = 1; i <= 6; i++) { await p.touch('touchMove', a[0] - 26 + (26 * i) / 6, a[1] - 18 + (18 * i) / 6); await sleep(30); }
    await sleep(120);
    const lp = await p.ev(`(()=>{const l=${R}.querySelector('[data-pm="loupe"]'),s=${R}.querySelector('[data-pm="stage"]').getBoundingClientRect(),r=l.getBoundingClientRect();return {shown:${PM}.loupeShown,inside:r.left>=s.left-1&&r.right<=s.right+1&&r.top>=s.top-1&&r.bottom<=s.bottom+1,above:r.bottom<=${a[1]}+2||r.right<=${a[0]}||r.left>=${a[0]},w:Math.round(r.width)}})()`);
    check(tag + ' the magnifier shows while the finger is down, inside the drawing, clear of the finger', lp.shown && lp.inside && lp.above && lp.w === 132, lp);
    await p.shot(tag + '-06-magnifier');
    await p.touch('touchEnd'); await sleep(200);
    check(tag + ' the point is set only when the finger lifts (the magnifier goes)', !(await p.ev(`${PM}.loupeShown`)) && (await p.ev(`${PM}.getDraft().segs.length`)) === 2);
  } else await tapImg(900, 600);
  await tapImg(0, 600); await tapImg(0, 0);
  const closed = await p.ev(`(()=>{const d=${PM}.getDraft();return {segs:d.segs.length,nodes:Object.keys(d.nodes).length,faces:${PM}.analyze().faces.length}})()`);
  check(tag + ' four taps and back to the first corner close the outer walls (one closed space)', closed.segs === 4 && closed.nodes === 4 && closed.faces === 1, closed);
  await press('[data-act="kind"][data-v="partition"]');
  await tapImg(500, 0); await tapImg(500, 600); await pressText('סיום קו');
  await tapImg(500, 300); await tapImg(900, 300); await pressText('סיום קו');
  const walls = await p.ev(`(()=>{const d=${PM}.getDraft(),a=${PM}.analyze();return {segs:d.segs.length,faces:a.faces.length,kinds:d.segs.map(s=>s.kind).sort().join(','),labels:${PM}.labels().length}})()`);
  check(tag + ' inner walls end on the outer walls (T junctions): three closed spaces', walls.faces === 3 && walls.segs === 10, walls);
  check(tag + ' every wall shows its length label', walls.labels >= 8, walls);
  const lab = await p.ev(`(()=>{const L=${PM}.labels();let o=0;for(let i=0;i<L.length;i++)for(let j=i+1;j<L.length;j++)if(Math.abs(L[i].x-L[j].x)<30&&Math.abs(L[i].y-L[j].y)<18)o++;return {o,top:L.filter(l=>l.cm>=482&&l.cm<=483).length,side:L.filter(l=>l.cm===575).length}})()`);
  check(tag + ' no length label sits on another; labels read inside sizes (500 centre to centre reads 483, the 600 side reads 575)', lab.o === 0 && lab.top >= 1 && lab.side >= 1, lab);
  // undo and redo, one step each
  await pressText('ביטול'); const u1 = await p.ev(`${PM}.getDraft().segs.length`);
  await pressText('שחזור'); const u2 = await p.ev(`${PM}.getDraft().segs.length`);
  check(tag + ' undo takes the last wall back, redo returns it', u1 < 10 && u2 === 10, { u1, u2 });
  await layout('walls drawn');
  await p.shot(tag + '-07-walls');

  // ---- 3. a door and a window ----
  await pressText('המשך'); await sleep(200);
  await layout('openings');
  await tapImg(500, 150);
  await press('[data-act="otype"][data-v="window"]');
  await tapImg(250, 0);
  const op = await p.ev(`${PM}.getDraft().openings.map(o=>o.type+':'+o.w)`);
  check(tag + ' a door (80) on the inner wall and a window (120) on the outer wall', op.join(',') === 'door:80,window:120', op);
  await p.shot(tag + '-08-openings');

  // ---- 4. names ----
  await pressText('המשך'); await sleep(200);
  const name = async (cx, cy, label) => { await tapImg(cx, cy); await sleep(150); await pressText(label); await sleep(150); };
  await tapImg(250, 300); await sleep(150);
  check(tag + ' a tap on a room opens the names, with the engine\'s names in the list', await p.ev(`(()=>{const b=[...${R}.querySelectorAll('.pm-names button')].map(e=>e.textContent);return ['סלון','חדר שינה','ממ״ד','חדר עבודה','חדר ארונות','מחסן','פינת משפחה','לא חלק מהדירה'].every(n=>b.includes(n))})()`));
  await layout('room names');
  await p.shot(tag + '-09-names');
  await pressText('סלון'); await sleep(150);
  await name(700, 150, 'חדר שינה'); await name(700, 450, 'חדר שינה הורים');
  const sum = await p.ev(`(()=>{const a=${PM}.analyze();return {sum:${R}.querySelector('[data-pm="sum"]').textContent,net:a.faces.reduce((m,f)=>m+f.net,0),probs:a.problems.map(x=>x.code),note:${R}.querySelector('[data-pm="note"]').textContent}})()`);
  check(tag + ' the summary: 3 rooms and the area, within 2% of the truth (' + TRUTH.toFixed(2) + ' m2)', /^3 חדרים · /.test(sum.sum) && Math.abs(sum.net - TRUTH) / TRUTH <= 0.02 && !sum.probs.length, sum);
  check(tag + ' the honest note about the scale and the engineer', sum.note === 'שרטוט שלכם לפי התוכנית שהעליתם. המידות תלויות בקנה המידה שסימנתם. לפני שינוי קיר מתייעצים עם מהנדס.');
  await layout('rooms');
  await p.shot(tag + '-10-rooms');

  // ---- save as a file (before opening, the draft is the same) ----
  await press('[data-act="save"]'); await sleep(200);
  const file = await p.ev(`(async()=>{const b=window.__blobs[window.__blobs.length-1];return b?await b.text():null})()`);
  const saved = JSON.parse(file || 'null');
  check(tag + ' "save as a file" gives the drawing and the plan, without the picture', saved && saved.schema === 'nadlan-myplan' && saved.draft.segs.length === 10 && saved.plan && saved.plan.rooms.length === 3 && !/data:image|base64/.test(file), saved && { segs: saved.draft.segs.length, rooms: saved.plan && saved.plan.rooms.length, bytes: file.length });

  // ---- open in 3D ----
  await pressText('לפתוח בתלת ממד');
  for (let i = 0; i < 120; i++) { if (await p.ev('!!(window.__d && window.__d.timings.first_3d_frame_ms)').catch(() => false)) break; await sleep(250); }
  await sleep(900);
  const d3 = await p.ev(`(()=>{const d=window.__d,q=d.quantities(),f=d.store.derived.faces.filter(f=>f.room);return {id:d.store.apt.id,done:window.__done.plan.id,rooms:f.length,names:f.map(x=>x.room.name_he).sort(),net:q.net,src:d.store.apt.source.kind,sub:${R}.querySelector('[data-nd="sub"]').textContent,edit:(${R}.querySelector('[data-nd="editplan"]')||{}).textContent,canvas:!!${R}.querySelector('.space canvas')}})()`);
  check(tag + ' the designer opens on THIS plan (same id), not an example', d3.id === d3.done && d3.src === 'own' && /^own-/.test(d3.id) && d3.sub.startsWith('התוכנית שלי'), d3);
  check(tag + ' three rooms in the designer, named as given', d3.rooms === 3 && d3.names.join('|') === ['חדר שינה', 'חדר שינה הורים', 'סלון'].sort().join('|'), d3);
  check(tag + ' the designer\'s area within 2% of the truth', Math.abs(d3.net - TRUTH) / TRUTH <= 0.02, { net: d3.net, truth: +TRUTH.toFixed(2) });
  check(tag + ' 3D is drawn and the header has "עריכת התוכנית"', d3.canvas && d3.edit === 'עריכת התוכנית', d3);
  await p.shot(tag + '-11-designer');
  const own = await p.ev(`(async()=>{const d=window.__d,w=d.store.derived.walls.find(w=>w.kind==='partition');const r=d.store.apply({op:'partition.remove',id:w.id});await new Promise(r=>setTimeout(r,50));const t1=${R}.querySelector('[data-nd="toast"]').textContent;d.store.undo();const r2=d.store.apply({op:'partition.remove',id:w.id});await new Promise(r=>setTimeout(r,50));const t2=${R}.querySelector('[data-nd="toast"]').textContent;d.store.undo();return {ok:r.ok,t1,t2,ok2:r2.ok}})()`);
  check(tag + ' an own plan: the first wall change says once that load-bearing walls are unknown', own.ok && own.t1 === 'בתוכנית שטענתם לבד אין מידע על קירות נושאים. לפני שינוי קיר מתייעצים עם מהנדס.', own);
  await press('[data-nd="editplan"]'); await sleep(600);
  const back = await p.ev(`({step:${PM}&&${PM}.step,segs:${PM}&&${PM}.getDraft().segs.length})`);
  check(tag + ' "עריכת התוכנית" goes back to the drawing, on the rooms step', back.step === 'rooms' && back.segs === 10, back);

  // ---- reload: the same drawing continues ----
  await p.go(); await sleep(400);
  const re = await p.ev(`({step:${PM}.step,segs:${PM}.getDraft().segs.length,photo:${PM}.hasPhoto,toast:${R}.querySelector('[data-pm="toast"]').textContent,mine:!!(window.localStorage.getItem('nd-myplan'))})`);
  check(tag + ' after a reload the same drawing continues, with its picture', re.step === 'rooms' && re.segs === 10 && re.photo && re.toast === 'המשכנו מהשרטוט ששמרתם במכשיר הזה.', re);

  // ---- start over, then load the saved file back ----
  await pressText('התחלה מחדש'); await pressText('לגעת שוב כדי למחוק את השרטוט'); await sleep(200);
  check(tag + ' "start over" (two taps) returns to the opening screen', (await p.ev(`${PM}.step`)) === 'start');
  await p.ev(`(()=>{const f=new File([${JSON.stringify(file)}],'my-plan.json',{type:'application/json'});const dt=new DataTransfer();dt.items.add(f);const i=${R}.querySelector('[data-pm="json"]');i.files=dt.files;i.dispatchEvent(new Event('change',{bubbles:true}));})()`);
  await sleep(500);
  const lo = await p.ev(`(()=>{const a=${PM}.analyze();return {step:${PM}.step,segs:${PM}.getDraft().segs.length,faces:a.faces.length,id:a.plan&&a.plan.id}})()`);
  check(tag + ' the saved file loads back: same walls, same rooms, same plan id', lo.step === 'rooms' && lo.segs === 10 && lo.faces === 3 && lo.id === saved.plan.id, lo);

  // ---- the "from sizes" route, no picture ----
  await pressText('התחלה מחדש'); await pressText('לגעת שוב כדי למחוק את השרטוט'); await sleep(200);
  await pressText('להתחיל לפי מידות'); await sleep(300);
  const m0 = await p.ev(`({step:${PM}.step,steps:[...${R}.querySelectorAll('.pm-steps button span')].map(e=>e.textContent),hint:${R}.querySelector('header p').textContent,rect:${R}.querySelector('[data-act="tool"][data-v="rect"]').getAttribute('aria-pressed')})`);
  check(tag + ' "from sizes": no scale step, the rectangle tool is ready', m0.step === 'walls' && m0.steps.join('|') === 'קירות|דלתות וחלונות|חדרים' && m0.rect === 'true', m0);
  await type('[data-pm="in-w"]', '400'); await type('[data-pm="in-d"]', '300'); await pressText('הוספת חדר'); await sleep(250);
  await type('[data-pm="in-w"]', '300'); await type('[data-pm="in-d"]', '300'); await pressText('הוספת חדר'); await sleep(200);
  { const s = await at(0, 0); await p.tap(s[0], s[1]); } // the second room's top corner on the first room's corner
  const mz = await p.ev(`(()=>{const a=${PM}.analyze();return {faces:a.faces.length,net:a.faces.map(f=>f.net).sort((x,y)=>x-y),segs:${PM}.getDraft().segs.length}})()`);
  const typedL = await p.ev(`${PM}.labels().map(l=>l.cm).sort((a,b)=>a-b)`);
  check(tag + ' a typed 400 x 300 room and a 300 x 300 room read their typed sizes on the walls', typedL.filter((v) => v === 400).length === 2 && typedL.filter((v) => v === 300).length === 5 && typedL.length === 7, typedL);
  check(tag + ' two typed rooms side by side share one wall: 12.0 and 9.0 m2 inside', mz.faces === 2 && Math.abs(mz.net[0] - 9) <= 0.09 && Math.abs(mz.net[1] - 12) <= 0.12 && mz.segs === 7, mz);
  await p.shot(tag + '-12-sizes');
  // an exact length typed on a wall's label: the 400 cm wall becomes 500 (inside)
  await press('[data-act="tool"][data-v="move"]'); await sleep(120);
  const l410 = await p.ev(`${PM}.labels().find(l=>l.cm===400)`);
  if (l410) { await p.tap(l410.x, l410.y); await sleep(150); }
  const edOpen = await p.ev(`!${R}.querySelector('[data-pm="edit"]').hidden`);
  await type('[data-pm="edit"] input', '500'); await press('[data-pm="edit"] button'); await sleep(200);
  const mz2 = await p.ev(`(()=>{const a=${PM}.analyze();return a.faces.map(f=>f.net).sort((x,y)=>x-y)})()`);
  check(tag + ' a tap on a length label opens the box; 500 typed (inside) makes the room 15.0 m2 and leaves the other at 9.0', !!l410 && edOpen && Math.abs(mz2[0] - 9) <= 0.09 && Math.abs(mz2[1] - 15) <= 0.15, { l410, edOpen, mz2 });
  await pressText('המשך'); await pressText('המשך'); await sleep(200);
  { const f = await p.ev(`${PM}.analyze().faces.map(f=>f.at)`); for (const [i, a] of f.entries()) { const s = await at(a[0], a[1]); await p.tap(s[0], s[1]); await sleep(120); await pressText(i ? 'חדר עבודה' : 'חדר שינה'); await sleep(120); } }
  await pressText('לפתוח בתלת ממד');
  for (let i = 0; i < 120; i++) { if (await p.ev('!!(window.__d && window.__d.timings.first_3d_frame_ms)').catch(() => false)) break; await sleep(250); }
  await sleep(600);
  const md = await p.ev(`(()=>{const d=window.__d,f=d.store.derived.faces.filter(f=>f.room);return {rooms:f.length,net:f.map(x=>x.net).sort((a,b)=>a-b),src:d.store.apt.source.kind}})()`);
  check(tag + ' "from sizes" opens in the designer: two rooms, 9.0 and 15.0 m2', md.rooms === 2 && md.src === 'own' && Math.abs(md.net[0] - 9) <= 0.09 && Math.abs(md.net[1] - 15) <= 0.15, md);
  await p.shot(tag + '-13-sizes-designer');

  // ---- a one-page PDF ----
  await press('[data-nd="editplan"]'); await sleep(500);
  await pressText('התחלה מחדש'); await pressText('לגעת שוב כדי למחוק את השרטוט'); await sleep(200);
  const obj = await p.send('Runtime.evaluate', { expression: `${R}.querySelector('[data-pm="file"]')` });
  await p.send('DOM.setFileInputFiles', { files: [pdfPath], objectId: obj.result.objectId });
  for (let i = 0; i < 80 && (await p.ev(`${PM}.step`)) !== 'scale'; i++) await sleep(250);
  await sleep(500);
  const pdf = await p.ev(`(()=>{const c=${R}.querySelector('[data-pm="cv"]'),x=c.getContext('2d'),r=c.getBoundingClientRect();const d=${PM}.getDraft();let dark=0;const im=x.getImageData(0,0,c.width,c.height).data;for(let i=0;i<im.length;i+=16)if(im[i]<80&&im[i+1]<80&&im[i+2]<80)dark++;return {step:${PM}.step,photo:${PM}.hasPhoto,img:d.img,dark}})()`);
  check(tag + ' a one-page PDF opens on the device and its drawing is shown', pdf.step === 'scale' && pdf.photo && pdf.img && pdf.img.w > 1000 && pdf.dark > 200, pdf);
  await p.shot(tag + '-14-pdf');
  check(tag + ' no page errors', p.errors.length === 0, p.errors);
  void W;
}

try {
  let p = await page(390, 844, 2.625, true);
  await flow(p, 'phone', true);
  await p.close();
  p = await page(1440, 900, 1, false);
  await flow(p, 'desktop', false);
  await p.close();
} catch (e) { console.error(e); fails++; receipt.error = String(e && e.stack || e); }
receipt.passed = receipt.checks.filter((c) => c.ok).length; receipt.failed = fails;
fs.writeFileSync(path.join(shots, 'receipt.json'), JSON.stringify(receipt, null, 2));
console.log('\n' + receipt.passed + ' passed, ' + fails + ' failed');
chrome.kill(); await sleep(300); try { fs.rmSync(profile, { recursive: true, force: true }); fs.rmSync(pdfPath, { force: true }); } catch {}
process.exit(fails ? 1 : 0);
