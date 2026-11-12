// HAD-712 (12.11.2026): the LOCAL showroom files on the LIVE Kikar pages (waymarks_test.mjs's browser(): Fetch interception) —
// the showroom's small map (the #C2563A beam, names on the map, edge chips, the "in the window's direction" line), the hint after
// the tower is dragged again, and the view-with-details labels kept inside the picture on every side.  node map663.mjs [he|en|fr]
import fs from 'node:fs/promises'; import path from 'node:path';
import { browser } from './waymarks_test.mjs';
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const URLS = { he: 'https://nad-lan.co.il/projects/hamedina/', en: 'https://nad-lan.co.il/projects/hamedina-en/', fr: 'https://nad-lan.co.il/projects/hamedina-en/' };
const OUT = path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1'));
const RECT = (sel) => `(() => { const e = document.querySelector(${JSON.stringify(sel)}); if (!e) return null; const r = e.getBoundingClientRect(); return { x: r.left, y: r.top, w: r.width, h: r.height }; })()`;
const MAP = `(() => { const mb = document.querySelector('.nlsr-map'), o = mb.getBoundingClientRect();
  const R = (e) => { const r = e.getBoundingClientRect(); return { l: r.left - o.left, r: r.right - o.left, t: r.top - o.top, b: r.bottom - o.top, txt: e.textContent }; };
  const L = [...mb.querySelectorAll('.nlsr-pl, .nlsr-pe, .nlsr-ml')].filter((e) => e.style.visibility !== 'hidden').map(R);
  const out = L.filter((a) => a.l < -0.5 || a.t < -0.5 || a.r > o.width + 0.5 || a.b > o.height + 0.5).map((a) => a.txt);
  let over = []; for (let i = 0; i < L.length; i++) for (let j = i + 1; j < L.length; j++) { const a = L[i], c = L[j]; if (a.l < c.r && a.r > c.l && a.t < c.b && a.b > c.t) over.push(a.txt + ' x ' + c.txt); }
  const beam = document.querySelector('.nlsr-beam');
  return { names: [...mb.querySelectorAll('.nlsr-pl')].map((e) => e.textContent + (e.classList.contains('is-beam') ? '*' : '')), chips: [...mb.querySelectorAll('.nlsr-pe')].map((e) => e.textContent),
    outside: out, overlaps: over, beamFill: beam ? getComputedStyle(beam).fill : null, line: document.querySelector('.nlsr-mapline').innerText }; })()`;
const VD = `(() => { const im = document.querySelector('.nlck-pan img[data-vdimg]'); if (!im) return null; const o = im.getBoundingClientRect(), vw = innerWidth;
  const B = [...document.querySelectorAll('.nlck-pan .nlvd:not(.nlvd--off) .nlvd__b')];
  return { n: B.length, cap: (document.querySelector('.nlck-cap') || {}).innerText, names: B.map((b) => b.innerText.replace(/\\n/g, ' | ')),
    cut: B.filter((b) => { const r = b.getBoundingClientRect(); return r.left < Math.max(o.left, 0) - 0.5 || r.right > Math.min(o.right, vw) + 0.5; }).map((b) => b.innerText.split('\\n')[0]),
    clipped: B.filter((b) => b.scrollWidth > b.clientWidth + 1).map((b) => b.innerText.split('\\n')[0]),
    under: (() => { const C = [...document.querySelectorAll('.nlck-subtop > *, .nlck-cap, .nlck-vdt')].map((e) => e.getBoundingClientRect()).filter((r) => r.width);
      return B.filter((b) => { const q = b.getBoundingClientRect(); return C.some((c) => q.left < c.right && q.right > c.left && q.top < c.bottom && q.bottom > c.top); }).map((b) => b.innerText.split('\\n')[0]); })() }; })()`;
const T = (k) => `window.__nlI18n.t(${JSON.stringify(k)})`;
async function run(L, w, h) {
  const b = await browser({ w, h, L }), tag = `${L}-${w}`, R = { L, w };
  await b.go(URLS[L]);
  await b.until("!!document.querySelector('.nlsr .nlsr-steps li') && !!document.querySelector('.nlsr-h')", 40000); await sleep(2500);
  await b.ev("document.querySelector('.nlsr').scrollIntoView({block:'start',behavior:'instant'}); scrollBy(0,-70); true"); await sleep(600);
  R.mapAll = await b.ev(MAP);
  let r = await b.ev(RECT('.nlsr [data-tower="B"]')); await b.tapAt(r.x + r.w / 2, r.y + r.h / 2); await sleep(2200);
  await b.ev("document.querySelector('.nlsr-stage').scrollIntoView({block:'center',behavior:'instant'}); true"); await sleep(700);
  const st = await b.ev(RECT('.nlsr-stage'));
  for (const f of [0.5, 0.45, 0.55, 0.4]) { await b.tapAt(st.x + st.w / 2, st.y + st.h * f); await sleep(900); if (await b.ev("!document.querySelector('.nlsr-card').hidden")) break; }
  await sleep(1500);
  R.mapPicked = await b.ev(MAP);
  await b.ev("document.querySelector('.nlsr-map').scrollIntoView({block:'center',behavior:'instant'}); true"); await sleep(500); await b.shot(`${tag}-map-picked`);
  // the other sides of the same floor: the map follows each
  R.sides = [];
  for (let i = 0; i < 3; i++) {
    const ok = await b.ev("(() => { const e = document.querySelector('.nlsr-card [data-side]:not([aria-pressed=\"true\"]), .nlsr-card .nlsr-other'); if (!e) return false; e.click(); return true; })()");
    if (!ok) break; await sleep(900); R.sides.push(await b.ev(MAP));
  }
  await b.shot(`${tag}-map-other-side`);
  // the tower dragged again: "tap a floor" comes back
  await b.ev("document.querySelector('.nlsr-stage').scrollIntoView({block:'center',behavior:'instant'}); true"); await sleep(500);
  const s2 = await b.ev(RECT('.nlsr-stage'));
  await b.send('Input.dispatchMouseEvent', { type: 'mousePressed', x: s2.x + s2.w * 0.3, y: s2.y + s2.h * 0.3, button: 'left', clickCount: 1 });
  for (let i = 1; i <= 8; i++) { await b.send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: s2.x + s2.w * 0.3 + i * 12, y: s2.y + s2.h * 0.3, button: 'left', buttons: 1 }); await sleep(20); }
  await b.send('Input.dispatchMouseEvent', { type: 'mouseReleased', x: s2.x + s2.w * 0.3 + 96, y: s2.y + s2.h * 0.3, button: 'left', clickCount: 1 }); await sleep(800);
  R.hintAfterDrag = { got: await b.ev("(document.querySelector('.nlsr-hint b') || {}).textContent"), want: await b.ev(T('sr_hint_floor')), way: await b.ev("document.querySelector('.nlsr').dataset.way") };
  await b.shot(`${tag}-after-drag`);
  // a floor again, then inside and the view: every label inside the picture, none cut
  for (const f of [0.5, 0.45, 0.55]) { await b.tapAt(st.x + st.w / 2, st.y + st.h * f); await sleep(900); if (await b.ev("document.querySelector('.nlsr').dataset.way !== 'floor'")) break; }
  R.wayAfterRepick = await b.ev("document.querySelector('.nlsr').dataset.way");
  r = await b.ev("(() => { const e = document.querySelector('.nlsr-go'); e.scrollIntoView({block:'center',behavior:'instant'}); const r = e.getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top + r.height / 2 }; })()");
  await b.tapAt(r.x, r.y);
  await b.until("!!document.querySelector('.nlck') && !document.querySelector('.nlck').hidden && !!document.querySelector('.nlck-grid')", 20000); await sleep(2000);
  await b.ev("(document.querySelector('.nlck-tile[data-open=\"view\"]') || {click(){}}).click(); true");
  await b.until("!!document.querySelector('.nlck-pan img[data-vdimg]')", 10000); await sleep(1500);
  R.views = [await b.ev(VD)]; await b.shot(`${tag}-view-0`);
  await b.ev("(() => { const p = document.querySelector('[data-pan]'); p.scrollLeft = p.scrollLeft + 3; return 1; })()"); await sleep(900); R.viewNudged = await b.ev(VD);
  R.geo = await b.ev("JSON.stringify((() => { const R = (e) => { const r = e.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; }; return { layer: R(document.querySelector('.nlck-pan .nlvd')), ctl: [...document.querySelectorAll('.nlck-subtop > *, .nlck-cap, .nlck-vdt')].map(R), lab: [...document.querySelectorAll('.nlck-pan .nlvd__b')].map(R) }; })())");
  for (let i = 1; i < 4; i++) {
    const ok = await b.ev("(() => { const L = [...document.querySelectorAll('[data-vk=\"side\"]')]; const e = L.find((x) => x.getAttribute('aria-pressed') === 'false' && !x.dataset.tried); if (!e) return false; e.dataset.tried = 1; e.click(); return true; })()");
    if (!ok) break; await sleep(1800); R.views.push(await b.ev(VD)); await b.shot(`${tag}-view-${i}`);
  }
  R.errs = b.errs; R.failed = b.failed; R.served = [...b.served].filter((s) => /showroom|viewdetails|i18n/.test(s));
  await b.close(); return R;
}
const L0 = process.argv[2] || 'all', out = [];
for (const L of L0 === 'all' ? ['he', 'en', 'fr'] : [L0]) for (const [w, h] of (process.env.W1 ? [[390, 844]] : [[390, 844], [1440, 900]])) { const R = await run(L, w, h); out.push(R); console.log(JSON.stringify(R)); }
await fs.writeFile(path.join(OUT, `result-${L0}.json`), JSON.stringify(out, null, 1));
