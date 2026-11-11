// node check-roomphoto.mjs [--port=47961] [--out=<folder for screenshots>] [--only=phone|desktop|sample]
// Presses "the floor and paint in your room" (plugins/nadlan-config/assets/designer/roomphoto.js) like a person, in headless
// Chrome with touch at 390x844 and with a mouse at 1440x900, on a synthetic room with known geometry, and checks the pixels.
// Serve the repo root first:  python -m http.server 47961 --bind 127.0.0.1   (from the repo root)
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const arg = (k, d) => { const a = process.argv.find((x) => x.startsWith('--' + k + '=')); return a ? a.slice(k.length + 3) : d; };
const URL0 = 'http://127.0.0.1:' + arg('port', '47961') + '/docs/design-lab/apartment-designer/roomphoto-harness.html';
const OUT = arg('out', path.join(os.tmpdir(), 'nd-roomphoto'));
const ONLY = arg('only', '');
fs.mkdirSync(path.join(OUT, 'downloads'), { recursive: true });
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe', PORT = 9300 + Math.floor(Math.random() * 500), profile = path.join(os.tmpdir(), 'nd-rp-' + PORT);
const chrome = spawn(CHROME, ['--headless=new', '--remote-debugging-port=' + PORT, '--user-data-dir=' + profile, '--no-first-run', '--disable-extensions', '--enable-gpu', '--use-angle=d3d11', '--ignore-gpu-blocklist', '--lang=he-IL'], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
for (let i = 0; i < 80; i++) { try { if ((await fetch('http://127.0.0.1:' + PORT + '/json/version')).ok) break; } catch {} await sleep(250); }
const receipt = { when: new Date().toISOString(), checks: [], timings: {} }; let fails = 0;
const check = (name, ok, detail) => { receipt.checks.push({ name, ok: !!ok, detail }); if (!ok) fails++; console.log((ok ? 'ok   ' : 'FAIL ') + name + (detail !== undefined ? '  ' + (typeof detail === 'string' ? detail : JSON.stringify(detail)) : '')); };

async function page(w, h, dpr, mobile, query = '') {
  const t = await (await fetch('http://127.0.0.1:' + PORT + '/json/new?about:blank', { method: 'PUT' })).json();
  const ws = new WebSocket(t.webSocketDebuggerUrl); let id = 0; const pend = new Map(), errors = [];
  ws.onmessage = (ev) => { const m = JSON.parse(ev.data); if (m.id && pend.has(m.id)) { pend.get(m.id)(m.result || m.error); pend.delete(m.id); } else if (m.method === 'Runtime.exceptionThrown') errors.push(m.params.exceptionDetails.text + ' ' + ((m.params.exceptionDetails.exception || {}).description || '')); else if (m.method === 'Runtime.consoleAPICalled' && (m.params.type === 'error' || m.params.type === 'assert')) errors.push(m.params.args.map((a) => a.value || a.description).join(' ')); else if (m.method === 'Log.entryAdded' && m.params.entry.level === 'error' && !/favicon/.test(m.params.entry.url || '')) errors.push(m.params.entry.text + ' ' + (m.params.entry.url || '')); };
  await new Promise((r) => (ws.onopen = r));
  const send = (method, params = {}) => new Promise((res) => { const i = ++id; pend.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); });
  const ev = async (e) => { const r = await send('Runtime.evaluate', { expression: e, awaitPromise: true, returnByValue: true }); if (r.exceptionDetails) throw new Error(JSON.stringify(r.exceptionDetails.exception || r.exceptionDetails.text)); return r.result.value; };
  await send('Page.enable'); await send('Runtime.enable'); await send('Log.enable');
  await send('Browser.setDownloadBehavior', { behavior: 'allow', downloadPath: path.join(OUT, 'downloads') });
  await send('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: dpr, mobile });
  if (mobile) await send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
  await send('Page.navigate', { url: URL0 + '?t=' + Date.now() + (query ? '&' + query : '') });
  for (let i = 0; i < 160; i++) { if (await ev('!!window.__ready').catch(() => false)) break; await sleep(250); }
  await ev('document.fonts.ready.then(()=>1)');
  const touch = (type, x, y) => send('Input.dispatchTouchEvent', { type, touchPoints: type === 'touchEnd' ? [] : [{ x, y, id: 1 }] });
  const mouse = (type, x, y) => send('Input.dispatchMouseEvent', { type, x, y, button: 'left', buttons: type === 'mouseReleased' ? 0 : 1, clickCount: 1 });
  const p = {
    ev, errors, send, mobile,
    shot: async (name) => { const d = await send('Page.captureScreenshot', { format: 'png' }); fs.writeFileSync(path.join(OUT, name + '.png'), Buffer.from(d.data, 'base64')); },
    tap: async (x, y) => { if (mobile) { await touch('touchStart', x, y); await sleep(40); await touch('touchEnd'); } else { await mouse('mouseMoved', x, y); await mouse('mousePressed', x, y); await sleep(30); await mouse('mouseReleased', x, y); } await sleep(160); },
    /** press, slide to the target (the magnifier shows), optionally photograph, lift */
    place: async (x0, y0, x1, y1, shotName) => {
      const st = mobile ? (x, y) => touch('touchStart', x, y) : (x, y) => mouse('mousePressed', x, y), mv = mobile ? (x, y) => touch('touchMove', x, y) : (x, y) => mouse('mouseMoved', x, y);
      if (!mobile) await mouse('mouseMoved', x0, y0);
      await st(x0, y0); await sleep(30);
      for (let i = 1; i <= 8; i++) { await mv(x0 + ((x1 - x0) * i) / 8, y0 + ((y1 - y0) * i) / 8); await sleep(16); }
      if (shotName) { await sleep(120); await p.shot(shotName); }
      if (mobile) await touch('touchEnd'); else await mouse('mouseReleased', x1, y1);
      await sleep(160);
    },
    close: async () => { ws.close(); await fetch('http://127.0.0.1:' + PORT + '/json/close/' + t.id).catch(() => {}); },
  };
  return p;
}
const S = 'document.getElementById("host").shadowRoot';
const center = (sel) => `(()=>{const b=${S}.querySelector(${JSON.stringify(sel)});if(!b)return null;b.scrollIntoView({block:'nearest'});const r=b.getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]})()`;
const byText = (txt) => `(()=>{const b=[...${S}.querySelectorAll('button')].find(b=>b.offsetParent&&b.textContent.trim()===${JSON.stringify(txt)});if(!b)return null;b.scrollIntoView({block:'nearest'});const r=b.getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]})()`;
async function press(p, what, isSel) { const c = await p.ev(isSel ? center(what) : byText(what)); if (!c) throw new Error('no button: ' + what); await p.tap(c[0], c[1]); }
async function typeInto(p, sel, text) {
  const c = await p.ev(center(sel)); await p.tap(c[0], c[1]);
  await p.ev(`${S}.querySelector(${JSON.stringify(sel)}).focus()`);
  await p.send('Input.insertText', { text });
}
async function idle(p, minRenders = 0, ms = 60000) {
  const t0 = Date.now();
  for (;;) { const s = await p.ev('window.__rp._test.state()'); if (!s.busy && s.renders >= minRenders) { await sleep(120); return s; } if (Date.now() - t0 > ms) throw new Error('timeout waiting, state ' + JSON.stringify(s)); await sleep(100); }
}
const toClient = (p, pt) => p.ev(`window.__rp._test.imgToClient(${pt[0]},${pt[1]})`);

// the geometry of the synthetic room, computed in the page from the same camera that drew it
const GEO = (V) => `(async()=>{
  const room=__paintRoom(${JSON.stringify(V)}), P=room.project, inImg=(q)=>q[0]>8&&q[1]>8&&q[0]<room.w-8&&q[1]<room.h-8;
  const pip=(p,poly)=>{let c=false;for(let i=0,j=poly.length-1;i<poly.length;j=i++){const a=poly[i],b=poly[j];if((a[1]>p[1])!==(b[1]>p[1])&&p[0]<(b[0]-a[0])*(p[1]-a[1])/(b[1]-a[1])+a[0])c=!c}return c};
  const nearF=(X,Y)=>room.footprints.some(f=>X>f[0]-40&&X<f[1]+40&&Y>f[2]-40&&Y<f[3]+40);
  const floor=[];for(let X=30;X<=390;X+=30)for(let Y=room.nearY+15;Y<=505;Y+=25){if(nearF(X,Y))continue;const q=P(X,Y);if(inImg(q)&&!room.furniture.some(h=>pip(q,h)))floor.push(q)}
  const walls=[];for(let X=40;X<=270;X+=40)for(let Z=40;Z<=240;Z+=50){const q=P(X,520,Z);if(inImg(q))walls.push(q)}
  for(let Y=380;Y<=500;Y+=40)for(const Z of [40,80,240]){const q=P(0,Y,Z);if(inImg(q))walls.push(q)}
  const sofa=[P(325,300,20),P(325,380,20),P(360,290,48),P(360,370,48),P(404,300,75)];
  window.__geo={w:room.w,h:room.h,corners:room.corners,furniture:room.furniture,width:room.width,depth:room.depth,sunAt:room.sunAt,shadeAt:room.shadeAt,backWall:room.backWall,
    floor,walls,sofa,gV1:P(270,350),gV2:P(90,460),gH:P(250,400),wallA:P(60,520,150),wallB:P(250,520,150)};
  const blob=await new Promise(r=>room.canvas.toBlob(r,'image/jpeg',0.95));
  const f=new File([blob],'room.jpg',{type:'image/jpeg'}),dt=new DataTransfer();dt.items.add(f);
  const inp=${S}.querySelector('[data-r="file"]');inp.files=dt.files;inp.dispatchEvent(new Event('change',{bubbles:true}));
  return {bytes:blob.size,n:room.furniture.length};
})()`;

/** simplify a hull so that neighbouring taps are at least `minPx` apart on the screen */
async function tapPoints(p, hull, minPx) {
  const cl = []; for (const q of hull) cl.push(await toClient(p, q));
  const keep = [];
  for (const c of cl) if (!keep.length || Math.hypot(c[0] - keep[keep.length - 1][0], c[1] - keep[keep.length - 1][1]) >= minPx) keep.push(c);
  while (keep.length > 3 && Math.hypot(keep[0][0] - keep[keep.length - 1][0], keep[0][1] - keep[keep.length - 1][1]) < minPx) keep.pop();
  return keep;
}
const lumOf = (c) => 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2];

async function pixelChecks(p, tag, label) {
  const r = await p.ev(`(()=>{const T=window.__rp._test,g=window.__geo,d=(a,b)=>Math.max(...a.map((v,i)=>Math.abs(v-b[i])));
    const fl=g.floor.map(q=>{const a=T.read('after',...q),b=T.read('before',...q);return Math.abs(a[0]-b[0])+Math.abs(a[1]-b[1])+Math.abs(a[2]-b[2])});
    const wl=g.walls.map(q=>d(T.read('after',...q),T.read('before',...q)));
    const sf=g.sofa.map(q=>d(T.read('after',...q),T.read('before',...q)));
    const L=(c)=>0.2126*c[0]+0.7152*c[1]+0.0722*c[2];
    const box=(w,q)=>L(T.mean(w,q[0]-6,q[1]-6,q[0]+6,q[1]+6));
    return {floorMean:fl.reduce((a,b)=>a+b,0)/fl.length,floorChanged:fl.filter(v=>v>12).length/fl.length,nFloor:fl.length,wallMax:Math.max(...wl),nWall:wl.length,sofaMax:Math.max(...sf),
      sunAfter:box('after',g.sunAt),shadeAfter:box('after',g.shadeAt),sunBefore:box('before',g.sunAt),shadeBefore:box('before',g.shadeAt)}})()`);
  check(tag + ' ' + label + ': the floor changed', r.floorChanged > 0.9 && r.floorMean > 25, { share: +r.floorChanged.toFixed(3), meanDiff: Math.round(r.floorMean), points: r.nFloor });
  check(tag + ' ' + label + ': the walls did not change', r.wallMax <= 1, { maxDiff: r.wallMax, points: r.nWall });
  check(tag + ' ' + label + ': the sofa did not change', r.sofaMax <= 2, { maxDiff: r.sofaMax });
  check(tag + ' ' + label + ': the patch of sun is still brighter than the floor around it', r.sunAfter > r.shadeAfter * 1.15, { after: +(r.sunAfter / r.shadeAfter).toFixed(2), before: +(r.sunBefore / r.shadeBefore).toFixed(2) });
  return r;
}
/** the darkest column (or row) near where a known joint must be */
async function joint(p, at, vertical) {
  return p.ev(`(()=>{const T=window.__rp._test,q=${JSON.stringify(at)};let best=1e9,bi=0;
    for(let k=-12;k<=12;k++){let s=0;for(let m=-1;m<=1;m++){const c=${vertical ? 'T.read("after",q[0]+m,q[1]+k)' : 'T.read("after",q[0]+k,q[1]+m)'};s+=0.2126*c[0]+0.7152*c[1]+0.0722*c[2]}if(s<best){best=s;bi=k}}return bi})()`);
}

async function fileFlow(tag, w, h, dpr, mobile, V, fins) {
  const p = await page(w, h, dpr, mobile);
  const sh = (n) => p.shot(tag + '-' + n);
  await sh('01-start');
  const st0 = await p.ev(`(()=>{const h=${S}.querySelector('header h2'),b=${S}.querySelector('[data-a="pick"]'),hs=getComputedStyle(h),bs=getComputedStyle(b);return {font:hs.fontFamily,color:hs.color,size:hs.fontSize,radius:bs.borderRadius,bg:bs.backgroundColor,shoot:!!${S}.querySelector('[data-a="shoot"]'),priv:${S}.querySelector('.priv').textContent}})()`);
  check(tag + ' the site CSS does not reach the tool', /Plex/.test(st0.font) && st0.color === 'rgb(15, 34, 51)' && st0.radius === '0px' && st0.bg === 'rgb(31, 95, 168)', st0);
  check(tag + ' the camera button shows only on a touch device', st0.shoot === mobile);
  check(tag + ' the privacy line is word for word', st0.priv === 'הצילום נשאר במכשיר שלכם. הוא לא נשלח לאתר ולא נשמר אצלנו.');
  const fed = await p.ev(GEO(V));
  if (mobile) await p.send('Emulation.setCPUThrottlingRate', { rate: 4 }); // a mid-range phone from here on
  for (let i = 0; i < 300; i++) { const s = await p.ev('window.__rp._test.state()'); if (s.step === 'corners' && !s.busy) break; await sleep(100); }
  const t1 = await p.ev('window.__rp._test.timings');
  receipt.timings[tag + '_load_ms'] = t1.load_ms;
  const s1 = await p.ev('window.__rp._test.state()');
  check(tag + ' the photo opens in the floor step, worked at 2400 px on the long side', s1.step === 'corners' && Math.max(s1.iw, s1.ih) === 2400, { step: s1.step, iw: s1.iw, ih: s1.ih, jpg_bytes: fed.bytes, load_ms: t1.load_ms });
  await sh('02-corners-empty');
  const g = await p.ev('window.__geo');
  // four corners: press a little off, slide onto the corner (the magnifier is photographed on the first), lift
  for (let i = 0; i < 4; i++) {
    const c = await toClient(p, g.corners[i]);
    await p.place(c[0] + 18, c[1] + 22, c[0], c[1], i === 0 ? tag + '-03-magnifier' : null);
  }
  let s2 = await idle(p, 1);
  check(tag + ' four corners make a floor', s2.corners === 4 && !!s2.frame, s2.frame);
  // drag one corner away and back: it follows the finger and lands where lifted
  const c2 = await toClient(p, g.corners[2]);
  await p.place(c2[0], c2[1], c2[0] - 40, c2[1] - 30);
  await p.place(c2[0] - 40, c2[1] - 30, c2[0], c2[1]);
  s2 = await idle(p, 1);
  await sh('04-corners-done');
  await press(p, 'המשך');
  // take the sofa and the table out
  const tapped = [];
  for (const hull of g.furniture) {
    let pts = await tapPoints(p, hull, 30);
    if (tapped.length) { // start the next outline at its point farthest from the outlines already made
      const far = (c) => Math.min(...tapped.map((q) => Math.hypot(c[0] - q[0], c[1] - q[1])));
      let bi = 0; pts.forEach((c, i) => { if (far(c) > far(pts[bi])) bi = i; });
      pts = pts.slice(bi).concat(pts.slice(0, bi));
    }
    tapped.push(...pts);
    for (const c of pts) await p.tap(c[0], c[1]);
    await press(p, 'סיום הרהיט');
  }
  const s3 = await idle(p, 1);
  check(tag + ' the sofa and the table are taken out of the floor', s3.furniture === 2 && s3.draft === 0, { furniture: s3.furniture });
  await sh('05-furniture');
  await press(p, 'המשך');
  if (!mobile) { // first with no measure: the size comes from the photo, and the tool says so
    await press(p, 'בלי מידה');
    const s = await idle(p, 1);
    const warn = await p.ev(`!!${S}.querySelector('.panel .warn')`);
    check(tag + ' no measure: an estimated size, and the tool says so', s.frame && !s.frame.measured && warn && Math.abs(s.frame.W - g.width) / g.width < 0.2, { W: Math.round(s.frame.W), true: g.width, fromPhoto: s.frame.fromPhoto, f: Math.round(s.frame.f) });
    await sh('05b-no-measure');
    await press(p, '[data-step="size"]', true);
  }
  await idle(p, 1);
  await typeInto(p, '[data-r="win"]', String(g.width));
  await typeInto(p, '[data-r="din"]', String(Math.round(g.depth)));
  await sh('06-size');
  await press(p, 'המשך');
  const s4 = await idle(p, 1);
  check(tag + ' the measures reach the floor', s4.step === 'finish' && s4.frame.measured && Math.abs(s4.frame.W - g.width) < 0.01, s4.frame);
  // the floors
  let k = 0;
  for (const f of fins) {
    const before = (await p.ev('window.__rp._test.state()')).renders;
    await press(p, '[data-a="fin"][data-k="' + f.k + '"]', true);
    if (f.rot != null) { await idle(p, before + 1); await press(p, '[data-a="rot"][data-v="' + f.rot + '"]', true); }
    const s = await idle(p, before + 1);
    const tm = await p.ev('window.__rp._test.timings');
    receipt.timings[tag + '_render_' + f.k + '_ms'] = tm.render_ms;
    receipt.timings[tag + '_prep_ms'] = tm.prep_ms;
    check(tag + ' ' + f.k + ' drawn' + (f.rot ? ' at ' + f.rot + '°' : '') + ' (render ' + tm.render_ms + ' ms, light map ' + tm.prep_ms + ' ms)', s.finish === f.k && s.hasAfter && (f.rot == null || s.rot === f.rot));
    if (k === 0) {
      await pixelChecks(p, tag, f.k);
      const a = await joint(p, g.gV1, false), b = await joint(p, g.gV2, false), hh = await joint(p, g.gH, true);
      check(tag + ' the joints fall where the measures say (within 3 px)', Math.abs(a) <= 3 && Math.abs(b) <= 3 && Math.abs(hh) <= 3, { across_at_270cm: a, across_at_90cm: b, along_at_120cm_from_wall: hh });
      const price = await p.ev(`${S}.querySelector('.panel .sum') && ${S}.querySelector('.panel .sum').textContent`);
      check(tag + ' area and price range for this floor', !!price && /מ״ר/.test(price) && /₪/.test(price), price);
      // move the start point: drag on the floor, the joints move with the finger
      await press(p, '[data-a="move"]', true);
      const m0 = await toClient(p, g.gV1), r0 = (await p.ev('window.__rp._test.state()')).renders;
      await p.place(m0[0], m0[1], m0[0] + 25, m0[1]);
      await idle(p, r0 + 1);
      const scale = await p.ev('window.__rp._test.imgToClient(1,0)[0]-window.__rp._test.imgToClient(0,0)[0]');
      const moved = await joint(p, [g.gV1[0] + 25 / scale, g.gV1[1]], false);
      check(tag + ' "move the starting point" drags the pattern with the finger', Math.abs(moved) <= 6, { offFromFinger_px: moved });
      const r1 = (await p.ev('window.__rp._test.state()')).renders;
      await press(p, '[data-a="center"]', true); await idle(p, r1 + 1);
      check(tag + ' back to the centre', Math.abs(await joint(p, g.gV1, false)) <= 3);
      await press(p, '[data-a="move"]', true);
    }
    await sh('07-after-' + ++k + '-' + f.k + (f.rot ? '-' + f.rot : ''));
  }
  // paint the wall in front
  const fl0 = await p.ev(`window.__rp._test.read('after',...window.__geo.floor[3])`);
  await press(p, '[data-step="wall"]', true);
  const bw = g.backWall.map((q) => [Math.max(4, Math.min(g.w - 4, q[0])), Math.max(4, Math.min(g.h - 4, q[1]))]);
  for (const q of bw) { const cc = await toClient(p, q); await p.tap(cc[0], cc[1]); }
  await press(p, 'סיום הקיר');
  const rw = (await idle(p, 1)).renders;
  await press(p, '[data-a="paint"][data-i="9"]', true);
  const s5 = await idle(p, rw + 1);
  const wc = await p.ev(`(()=>{const T=window.__rp._test,g=window.__geo;return {a:T.mean('after',g.wallA[0]-5,g.wallA[1]-5,g.wallA[0]+5,g.wallA[1]+5),b:T.mean('after',g.wallB[0]-5,g.wallB[1]-5,g.wallB[0]+5,g.wallB[1]+5),a0:T.mean('before',g.wallA[0]-5,g.wallA[1]-5,g.wallA[0]+5,g.wallA[1]+5),b0:T.mean('before',g.wallB[0]-5,g.wallB[1]-5,g.wallB[0]+5,g.wallB[1]+5),floor:T.read('after',...g.floor[3])}})()`);
  const ratioAfter = lumOf(wc.a) / lumOf(wc.b), ratioBefore = lumOf(wc.a0) / lumOf(wc.b0);
  check(tag + ' the wall takes the sage green', s5.walls === 1 && s5.paint === 9 && wc.b[1] > wc.b[0] + 4 && wc.b[1] > wc.b[2] + 4, { wall: wc.b.map(Math.round), before: wc.b0.map(Math.round) });
  check(tag + ' the light across the wall is kept (bright side stays brighter)', ratioBefore > 1.03 && Math.abs(ratioAfter - ratioBefore) / ratioBefore < 0.15, { before: +ratioBefore.toFixed(3), after: +ratioAfter.toFixed(3) });
  check(tag + ' painting the wall leaves the floor as it was', fl0.every((v, i) => Math.abs(v - wc.floor[i]) <= 1), { before: fl0, after: wc.floor });
  await sh('08-wall');
  // before and after, then save
  await press(p, '[data-step="result"]', true);
  await idle(p, 1);
  const a0 = await toClient(p, [g.w / 2, g.h / 2]), a1 = await toClient(p, [g.w * 0.3, g.h / 2]);
  await p.place(a0[0], a0[1], a1[0], a1[1]);
  await sh('09-before-after');
  const DL = path.join(OUT, 'downloads');
  for (const f of fs.readdirSync(DL)) fs.rmSync(path.join(DL, f), { force: true });
  const sizes = () => fs.readdirSync(DL).map((f) => ({ f, n: fs.statSync(path.join(DL, f)).size }));
  await press(p, 'שמירת התמונה');
  let saved = null;
  const tSave = Date.now();
  for (let i = 0; i < 300; i++) { saved = await p.ev('window.__rp._test.lastSave'); if (saved) break; await sleep(100); }
  receipt.timings[tag + '_save_ms'] = Date.now() - tSave;
  let onDisk = null;
  for (let i = 0; i < 50 && !onDisk; i++) { await sleep(200); onDisk = sizes().find((x) => saved && x.n === saved.bytes && /\.jpe?g$/i.test(x.f)); }
  check(tag + ' "save the picture" makes a JPG file' + (onDisk ? ' on disk' : ''), saved && saved.type === 'image/jpeg' && saved.bytes > 50000 && (onDisk || mobile), { ...saved, file: onDisk ? onDisk.f : null, folder: sizes() });
  // layout: nothing cut, buttons big enough, the page scrolls outside the photo
  const lay = await p.ev(`(()=>{const R=${S};const bad=[...R.querySelectorAll('button')].filter(b=>b.offsetParent).map(b=>b.getBoundingClientRect()).filter(r=>r.height<44||r.width<44).length;
    const over=[...R.querySelectorAll('.panel *')].filter(e=>e.offsetParent&&e.scrollWidth>e.clientWidth+1&&getComputedStyle(e).overflow!=='hidden').length;
    return {small:bad,overflow:over,docScroll:document.documentElement.scrollWidth>innerWidth,ta:getComputedStyle(R.querySelector('canvas')).touchAction,taPanel:getComputedStyle(R.querySelector('.panel')).touchAction}})()`);
  check(tag + ' every button at least 44 px, nothing cut, no sideways scroll', lay.small === 0 && lay.overflow === 0 && !lay.docScroll, lay);
  check(tag + ' only the photo holds the finger (touch-action none on the photo only)', lay.ta === 'none' && lay.taPanel !== 'none', lay);
  check(tag + ' no errors in the console', p.errors.length === 0, p.errors.slice(0, 5));
  await p.close();
}

async function sampleFlow(tag, w, h, dpr, mobile, lang) {
  const p = await page(w, h, dpr, mobile, lang ? 'lang=' + lang : '');
  if (mobile) await p.send('Emulation.setCPUThrottlingRate', { rate: 4 });
  await press(p, lang === 'en' ? 'Try it on a sample room' : 'לנסות על חדר לדוגמה');
  for (let i = 0; i < 400; i++) { const s = await p.ev('window.__rp._test.state()'); if (s.step === 'finish' && !s.busy && s.renders > 0) break; await sleep(100); }
  if (mobile) await p.send('Emulation.setCPUThrottlingRate', { rate: 1 });
  const s = await p.ev('window.__rp._test.state()'), tm = await p.ev('window.__rp._test.timings');
  await p.ev(`(()=>{const room=__paintRoom({w:1600,h:1200}),P=room.project;window.__geo={floor:[P(60,480),P(150,300),P(250,450),P(300,330)],walls:[P(100,520,150),P(200,520,200)],sofa:[P(325,300,20),P(360,290,48)]}})()`);
  const d = await p.ev(`(()=>{const T=window.__rp._test,g=window.__geo,df=(q)=>{const a=T.read('after',...q),b=T.read('before',...q);return Math.abs(a[0]-b[0])+Math.abs(a[1]-b[1])+Math.abs(a[2]-b[2])};return {floor:g.floor.map(df),walls:g.walls.map(df),sofa:g.sofa.map(df)}})()`);
  check(tag + ' the sample room opens marked, with a new floor drawn (' + tm.sample_ms + ' ms to paint, render ' + tm.render_ms + ' ms)', s.step === 'finish' && s.corners === 4 && s.furniture === 2 && s.frame.measured && d.floor.every((v) => v > 12) && d.walls.every((v) => v === 0) && d.sofa.every((v) => v <= 3), { floor: d.floor, walls: d.walls, sofa: d.sofa });
  receipt.timings[tag + '_sample_ms'] = tm.sample_ms;
  await p.shot(tag + '-10-sample' + (lang ? '-' + lang : ''));
  if (lang === 'en') {
    const txt = await p.ev(`${S}.querySelector('.panel').textContent`);
    check(tag + ' English: the panel is in English', /Choose a floor/.test(txt) && !/[\u0590-\u05FF]/.test(txt), txt.slice(0, 120));
  }
  check(tag + ' no errors in the console', p.errors.length === 0, p.errors.slice(0, 5));
  await p.close();
}

try {
  if (!ONLY || ONLY === 'phone') await fileFlow('m', 390, 844, 2.625, true, {}, [{ k: 'porcelain-60' }, { k: 'oak-plank', rot: 45 }, { k: 'terrazzo' }]);
  if (!ONLY || ONLY === 'desktop') await fileFlow('d', 1440, 900, 1, false, { oldFloor: 'wood', yaw: 7, pitch: -13, lens: 0.66, pos: [200, -30, 155], wall: '#E3E5E6' }, [{ k: 'porcelain-60' }, { k: 'laminate', rot: 90 }, { k: 'concrete' }, { k: 'porcelain-60x120' }]);
  if (!ONLY || ONLY === 'sample') { await sampleFlow('m', 390, 844, 2.625, true); await sampleFlow('d', 1440, 900, 1, false, 'en'); }
} catch (e) { check('the run finished', false, String((e && e.stack) || e)); }
receipt.passed = receipt.checks.filter((c) => c.ok).length; receipt.total = receipt.checks.length;
fs.writeFileSync(path.join(OUT, 'receipt.json'), JSON.stringify(receipt, null, 1));
console.log('\n' + receipt.passed + ' of ' + receipt.total + ' passed; timings ' + JSON.stringify(receipt.timings) + '\nscreenshots in ' + OUT);
chrome.kill();
await sleep(1500);
try { fs.rmSync(profile, { recursive: true, force: true }); } catch {} // the throwaway Chrome profile (about 60 MB)
try { fs.rmSync(path.join(OUT, 'downloads'), { recursive: true, force: true }); } catch {}
process.exit(fails ? 1 : 0);
