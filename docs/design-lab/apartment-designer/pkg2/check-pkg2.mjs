// node check-pkg2.mjs [--base=http://127.0.0.1:47962] [--tag=local]
// Presses everything package 2 (HAD-792) added to the apartment designer, in a real headless Chrome with the GPU:
// walls rising, materials, the walk (start view, room to room, tour, never facing a wall), notes to the builder (pin, save,
// survive a reload, show in 3D), wall paint, the design order (basket event + saved object), ?call=1 and the five languages.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { browser, sleep } from './cdp.mjs';
const arg = (k, d) => { const a = process.argv.find((x) => x.startsWith('--' + k + '=')); return a ? a.slice(k.length + 3) : d; };
const BASE = arg('base', 'http://127.0.0.1:47962'), TAG = arg('tag', 'local');
const here = path.dirname(fileURLToPath(import.meta.url)), out = path.join(here, 'evidence-' + TAG);
fs.mkdirSync(out, { recursive: true });
const receipt = { when: new Date().toISOString(), base: BASE, checks: [] }; let fails = 0;
const check = (name, ok, detail) => { receipt.checks.push({ name, ok: !!ok, detail }); if (!ok) fails++; console.log((ok ? 'ok   ' : 'FAIL ') + name + (detail !== undefined ? '  ' + (typeof detail === 'string' ? detail : JSON.stringify(detail)) : '')); };
const S = 'window.__nlStudio', D = S + '.designer', SH = 'document.getElementById("host").shadowRoot';
const b = await browser();
async function open(q, { w = 390, h = 844, mobile = true } = {}) {
  const p = await b.page({ w, h, dpr: mobile ? 2 : 1, mobile });
  await p.send('Page.addScriptToEvaluateOnNewDocument', { source: 'try { localStorage.setItem("nl_vt_off", "1"); } catch (e) {} window.__nlCallHook = {}; window.__events = []; addEventListener("nadlan:design-order", (e) => __events.push(e.detail));' });
  await p.go(BASE + '/tour/designer/' + q);
  const ok = await p.wait(`!!(${D} && ${D}.space && ${D}.space.el)`, 40000);
  return { p, ok };
}
const tapIn = async (p, sel) => { const c = await p.ev(`(()=>{const e=${SH}.querySelector(${JSON.stringify(sel)});if(!e)return null;e.scrollIntoView({block:'nearest'});const r=e.getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]})()`); if (!c) throw new Error('no ' + sel); await p.tap(c[0], c[1]); };
try {
  // ---------------- phone, Hebrew, a project with published plans ----------------
  let { p, ok } = await open('?project=ashira&t=' + Date.now());
  check('phone he: the designer opens on the project plan', ok);
  await p.ev(`localStorage.clear(); localStorage.setItem('nl_vt_off','1')`); // a clean visitor (the test never counts as a buyer in the developer report)
  await p.go(BASE + '/tour/designer/?project=ashira&t=' + Date.now()); await p.wait(`!!(${D} && ${D}.space && ${D}.space.el)`, 40000);
  let r0 = await p.ev(`${D}.space.riseValue`);
  if (r0 >= 1) { await p.ev(`${D}.space.rise()`); await sleep(400); r0 = await p.ev(`${D}.space.riseValue`); } // a slow load can finish the first rise before the check looks
  await p.shot(path.join(out, 'p01-phone-rise-mid.png'));
  await sleep(2600);
  const r1 = await p.ev(`${D}.space.riseValue`);
  check('the walls rise out of the plan (mid-way, then standing)', r0 > 0 && r0 < 1 && r1 === 1, { early: +r0.toFixed(2), after: r1 });
  await p.shot(path.join(out, 'p02-phone-doll.png'));
  const replay = await p.ev(`(()=>{${SH}.querySelector('[data-nd=rise]').click();return ${D}.space.rising})()`);
  check('the rise can be watched again from its button', replay === true);
  await sleep(2600);
  // walk
  await tapIn(p, '[data-nd=m-walk]'); await sleep(900);
  const w0 = await p.ev(`({ahead:${D}.space.aheadCm(),w:${D}.space.walker(),rooms:${SH}.querySelectorAll('.walkbar button[data-room]').length})`);
  check('walk starts in the living room looking at the room, not a wall (>= 3 m free ahead)', w0.ahead >= 300, w0);
  check('walk offers a tour and a button per room', w0.rooms >= 4, w0.rooms);
  await p.shot(path.join(out, 'p03-phone-walk-start.png'));
  const rooms = await p.ev(`${D}.space.rooms().map(r=>r.id)`);
  let worst = Infinity, reached = 0;
  for (const id of rooms) {
    await p.ev(`${SH}.querySelector('.walkbar button[data-room="${id}"]').click()`);
    await p.wait(`(()=>{const w=${D}.space.walker();return !w.path&&!w.turning})()`, 15000); await sleep(200);
    const st = await p.ev(`({a:${D}.space.aheadCm(),r:${D}.space.walkState().room})`);
    if (st.r === id) reached++; worst = Math.min(worst, st.a);
  }
  check('every room is reached through the doors', reached === rooms.length, reached + '/' + rooms.length);
  check('after every walk the view looks into the room (worst free view >= 120 cm)', worst >= 120, worst);
  await p.shot(path.join(out, 'p04-phone-walk-room.png'));
  await p.ev(`${SH}.querySelector('[data-nd=tour]').click()`); await sleep(1500);
  check('the tour runs by itself', await p.ev(`${D}.space.walker().touring`));
  await p.ev(`${SH}.querySelector('[data-nd=tour]').click()`);
  await tapIn(p, '[data-nd=m-doll]'); await sleep(600);
  // note to the builder
  await tapIn(p, 'nav button[data-sheet=notes]'); await sleep(300);
  await tapIn(p, '[data-nd=noteadd]'); await sleep(300);
  const living = await p.ev(`(()=>{const f=${D}.store.derived.faces.filter(f=>f.room).sort((a,b)=>b.net-a.net)[0];return ${D}.plan.screenOf((f.bb.x0+f.bb.x1)/2,(f.bb.y0+f.bb.y1)/2)})()`);
  await p.tap(living[0], living[1]); await sleep(400);
  await p.ev(`(()=>{const t=${SH}.querySelector('[data-nd=notetext]');t.value='להזיז את נקודת הטלוויזיה 40 ס״מ שמאלה';return 1})()`);
  await tapIn(p, '[data-nd=notesave]'); await sleep(500);
  const n1 = await p.ev(`({n:${D}.store.design.notes.length,pins:${D}.plan.el.querySelectorAll('.nt').length,tags:${D}.space.noteTags().length,room:${D}.store.design.notes[0]&&${D}.store.design.notes[0].room})`);
  check('a note is pinned on the plan, saved, and stands in 3D', n1.n === 1 && n1.pins === 1 && n1.tags === 1 && !!n1.room, n1);
  await p.shot(path.join(out, 'p05-phone-note.png'));
  // wall paint
  const fid = await p.ev(`${D}.store.design.notes[0].room`);
  await p.ev(`${D}.select({type:'room',id:${JSON.stringify(fid)}})`); await sleep(300);
  await p.ev(`${SH}.querySelector('[data-wall="w-sage"]').click()`); await sleep(400);
  check('a wall colour is set for the room', await p.ev(`${D}.store.wallOf(${JSON.stringify(fid)})`) === 'w-sage');
  await p.shot(path.join(out, 'p06-phone-finishes.png'));
  // order
  await tapIn(p, 'nav button[data-sheet=order]'); await sleep(400);
  await p.ev(`(()=>{const c=${SH}.querySelector('[data-svc=call]');c.click();return 1})()`);
  await p.shot(path.join(out, 'p07-phone-order.png'));
  await tapIn(p, '[data-nd=basket]'); await sleep(400);
  const ord = await p.ev(`(()=>{const x=JSON.parse(localStorage.getItem('nl-design-order:v1')||'null');const o=x&&x.orders[x.last];return {ev:__events.length,schema:o&&o.schema,proj:o&&o.project.slug,notes:o&&o.notes.length,fin:o&&o.finishes.map(f=>f.surface+':'+f.id),svc:o&&o.services.map(s=>s.id),items:o&&o.items.length,unit:o&&o.unit.id,noPII:!!o&&!/@|972\\d|"(phone|email|mail|fullName|buyer|identity)"/.test(JSON.stringify(o))}})()`);
  check('"add to my basket" fires the event and saves the order object for package 4', ord.ev === 1 && ord.schema === 'nadlan-design-order' && ord.proj === 'ashira' && ord.notes === 1 && ord.fin.includes('wall:w-sage') && ord.svc.includes('call') && ord.noPII, ord);
  // reload: the note survives without any call
  await p.go(BASE + '/tour/designer/?project=ashira&t=' + Date.now()); await p.wait(`!!(${D} && ${D}.space && ${D}.space.el)`, 40000); await sleep(800);
  check('the note survives a reload (kept on this device, no call needed)', await p.ev(`${D}.store.design.notes.length`) === 1);
  await p.close();

  // ---------------- desktop, Hebrew: the materials and the walk, for the eyes ----------------
  ({ p, ok } = await open('?project=ashira&t=' + Date.now(), { w: 1440, h: 900, mobile: false }));
  await sleep(3200); await p.shot(path.join(out, 'd01-desktop-doll.png'));
  await p.ev(`${SH}.querySelector('[data-nd=m-walk]').click()`); await sleep(1500); await p.shot(path.join(out, 'd02-desktop-walk-living.png'));
  const rr = await p.ev(`${D}.space.rooms().filter(r=>/שינה/.test(r.name_he)).map(r=>r.id)`);
  if (rr[0]) { await p.ev(`${SH}.querySelector('.walkbar button[data-room="${rr[0]}"]').click()`); await p.wait(`(()=>{const w=${D}.space.walker();return !w.path&&!w.turning})()`, 15000); await sleep(400); await p.shot(path.join(out, 'd03-desktop-walk-bedroom.png')); }
  const st = await p.ev(`${D}.space.stats()`);
  check('desktop: one draw call for all walls, scene stays light', st.calls < 260, st);
  check('no errors on the page (desktop)', p.errors.filter((e) => !/GLTFLoader|favicon|trail/.test(e)).length === 0, p.errors.slice(0, 3));
  await p.close();

  // ---------------- other languages, and ?call=1 ----------------
  for (const [lg, word] of [['ru', /[а-я]/i], ['ar', /[؀-ۿ]/], ['fr', /[a-zé]/i], ['en', /[a-z]/i]]) {
    ({ p, ok } = await open('?project=ashira&lang=' + lg + '&t=' + Date.now()));
    await sleep(2800);
    const t = await p.ev(`({dir:document.documentElement.dir,lang:document.documentElement.lang,ttl:document.getElementById('ttl').textContent,nav:[...${SH}.querySelectorAll('nav button')].map(b=>b.textContent).join('|'),root:${SH}.querySelector('.nd').lang,label:${D}.plan.el.querySelector('.rl')&&${D}.plan.el.querySelector('.rl').textContent})`);
    const heb = /[֐-׿]/.test(t.nav + t.ttl + t.label);
    check(lg + ': page, tools and room names are in ' + lg + ' (no Hebrew left)', ok && t.lang === lg && t.root === lg && word.test(t.nav) && !heb, t);
    await p.shot(path.join(out, 'l-' + lg + '-phone.png'));
    await p.close();
  }
  ({ p, ok } = await open('?project=rainbow&call=1&lang=en&t=' + Date.now()));
  const sheet = await p.wait(`!!${SH}.querySelector('.ndc-host *')`, 15000);
  check('?call=1 opens the call sheet on arrival (a project with no published plans: example apartment, never a dead page)', ok && sheet);
  await sleep(600); await p.shot(path.join(out, 'c01-call-sheet-en.png'));
  await p.close();
  ({ p, ok } = await open('?project=no-such-project&call=1&t=' + Date.now()));
  check('an unknown project still opens the designer and the call sheet', ok && await p.wait(`!!${SH}.querySelector('.ndc-host *')`, 15000));
  await p.close();
} catch (e) { check('ran to the end', false, String(e && e.stack || e).slice(0, 400)); }
finally { await b.close(); }
receipt.passed = receipt.checks.length - fails; receipt.failed = fails;
fs.writeFileSync(path.join(out, 'receipt.json'), JSON.stringify(receipt, null, 2));
console.log('\n' + receipt.passed + ' passed, ' + fails + ' failed');
process.exit(fails ? 1 : 0);
