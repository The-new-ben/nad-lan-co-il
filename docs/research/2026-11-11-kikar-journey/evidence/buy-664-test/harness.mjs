// HAD-712 (12.11.2026): waymarks, view with details, floor plan, the card as a sheet (step 0), the basket's way inside.
// Headless Chrome (CDP) on the LIVE Kikar pages with the LOCAL asset files (Fetch interception, as i18n_test.mjs does). The Hebrew
// page's HTML gets the same edits as the local inc/project-stage.php (no world.js / three.js preload, no 3D mount until the tap,
// window.__nlpsMount); French = the English page with lang 'fr' in its configs. GETs only; nothing is submitted.
//   node waymarks_test.mjs [he|en|fr|all]
import { spawn } from 'node:child_process'; import fs from 'node:fs/promises'; import os from 'node:os'; import path from 'node:path';
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const OUT = path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1'));
const REPO = path.resolve(OUT, '../../../../..');
const ASSETS = path.join(REPO, 'plugins/nadlan-config/assets');
const LOCAL = ['project-stage/world/showroom.js', 'project-stage/world/showroom-i18n.js', 'project-stage/world/cockpit.js', 'project-stage/world/journey.js',
  'project-stage/world/viewdetails.js', 'project-stage/world/planfloor.js', 'basket/basket.js', 'project-stage/world/showroom.css', 'project-stage/world/cockpit.css', 'basket/basket.css',
  'project-stage/hamedina/details.json', // details.json: the view-with-details data, new in this release (404 on the live site until then)
  'project-stage/world/kikarbuy.js']; // HAD-712 step 6 (buy-664-test copy): "Build me an offer", new
// HAD-712 step 6 (buy-664-test copy): NO real lead and NO real document. Every POST to nadlan/v1/lead and nadlan/v1/rfp is answered
// here with fake JSON and its body is recorded (b.posts). A GET of a request document is answered with a stub page.
export const FAKE = { lead: { ok: true, lead_id: 123, lead_key: 'k' }, rfp: { ok: true, url: 'https://nad-lan.co.il/wp-json/nadlan/v1/rfp/xxxxxxxxxxxxxxxx', ref: 'RFP-TEST' } };
const URLS = { he: 'https://nad-lan.co.il/projects/hamedina/', en: 'https://nad-lan.co.il/projects/hamedina-en/', fr: 'https://nad-lan.co.il/projects/hamedina-en/' };
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const MODE = process.argv[2] || 'all';

// the same edits as the local inc/project-stage.php (HAD-712), applied to the live HTML
function patchHe(html) {
  const out = { html, applied: [] };
  if (html.includes('heShowroom')) { out.applied.push('live already 1.72.661: no patch'); return out; } // map-663-test copy
  const rep = (a, b, name) => { if (out.html.includes(a)) { out.html = out.html.replace(a, b); out.applied.push(name); } else out.applied.push('MISSING ' + name); };
  const n0 = out.html.length;
  out.html = out.html.replace(/<link rel="modulepreload" href="[^"]*(three\.module\.js|world\/world\.js)[^"]*"[^>]*>\n?/g, '').replace(/<link rel="preload" as="fetch" href="[^"]*hamedina\/world\.json[^"]*"[^>]*>\n?/g, '');
  out.applied.push('preloads removed: ' + (n0 - out.html.length) + ' chars');
  rep("  }).catch((e) => { console.warn('[world]', e); P = null; return null; });\n  return P;\n}", "  }).catch((e) => { console.warn('[world]', e); P = null; return null; });\n  return P;\n}\nwindow.__nlpsMount = mount;\nconst heShowroom = !!(c.next && c.next.journey && c.lang === 'he');", 'mount exposed');
  rep("  if (c.next && c.next.journey && jyPhone()) { /* HAD-699: on phones under the gate the journey replaces the 3D world */ }", "  if (c.next && c.next.journey && jyPhone()) { /* HAD-699: on phones under the gate the journey replaces the 3D world */ }\n  else if (heShowroom) { }", 'no auto mount');
  rep("    if (ev !== 'hero-world') return;", "    if (ev !== 'hero-world') return;\n    if (heShowroom && !document.body.classList.contains('nlsr-3d')) return;", 'tour link');
  return out;
}
function patchFr(html) {
  let n = 0; const h = html.replace(/&quot;lang&quot;:&quot;en&quot;/g, () => { n++; return '&quot;lang&quot;:&quot;fr&quot;'; })
    .replace(/(<script[^>]*id="nadlan-basket-cfg"[^>]*>[^<]*)"lang":"en"/, (m, a) => { n++; return a + '"lang":"fr"'; });
  return { html: h, applied: ['lang en->fr x' + n] };
}

export async function browser({ w, h, L, rfpFailFirst = 0 }) {
  const posts = []; let rfpFails = rfpFailFirst;
  const PORT = 9300 + Math.floor(Math.random() * 500), MOB = w < 900;
  const dir = await fs.mkdtemp(path.join(os.tmpdir(), 'wm-'));
  const ch = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${dir}`, '--no-first-run', '--hide-scrollbars', '--enable-unsafe-swiftshader', '--use-angle=swiftshader', 'about:blank'], { stdio: 'ignore' });
  for (let i = 0; i < 80; i++) { try { await (await fetch(`http://127.0.0.1:${PORT}/json/version`)).json(); break; } catch { await sleep(250); } }
  const tg = await (await fetch(`http://127.0.0.1:${PORT}/json/new?about:blank`, { method: 'PUT' })).json();
  const ws = new WebSocket(tg.webSocketDebuggerUrl); let id = 0; const P = new Map();
  const errs = [], served = new Set(), reqs = [], failed = [], patched = [];
  await new Promise((r) => (ws.onopen = r));
  const send = (m, p = {}) => new Promise((ok, no) => { const i = ++id; P.set(i, { ok, no }); ws.send(JSON.stringify({ id: i, method: m, params: p })); });
  const reqUrl = new Map();
  ws.onmessage = async (e) => {
    const m = JSON.parse(e.data);
    if (m.id && P.has(m.id)) { const q = P.get(m.id); P.delete(m.id); m.error ? q.no(new Error(JSON.stringify(m.error))) : q.ok(m.result); return; }
    if (m.method === 'Runtime.exceptionThrown') { const d = m.params.exceptionDetails; errs.push(((d.exception && d.exception.description) || d.text || '').split('\n')[0].slice(0, 200) + ' @ ' + (d.url || '').split('/').pop()); }
    if (m.method === 'Network.requestWillBeSent') { reqs.push({ url: m.params.request.url, t: Date.now() }); reqUrl.set(m.params.requestId, m.params.request.url); }
    if (m.method === 'Network.loadingFailed' && !m.params.canceled && !/ERR_ABORTED|ERR_BLOCKED_BY_CLIENT/.test(m.params.errorText)) failed.push({ url: reqUrl.get(m.params.requestId), err: m.params.errorText });
    if (m.method === 'Network.responseReceived' && m.params.response.status >= 400) failed.push({ url: m.params.response.url, status: m.params.response.status });
    if (m.method === 'Fetch.requestPaused') {
      const pr = m.params, u = new URL(pr.request.url);
      const api = /\/wp-json\/nadlan\/v1\/(lead|rfp)(\/[a-z0-9]+)?\/?$/i.exec(u.pathname) || (/^\/?$/.test(u.pathname) && /rest_route=\/nadlan\/v1\/(lead|rfp)/.test(u.search) ? [0, /rest_route=\/nadlan\/v1\/(lead|rfp)/.exec(u.search)[1]] : null);
      if (api) { // intercepted: never reaches the site
        let body = pr.request.postData || '';
        if (!body && pr.request.postDataEntries) body = pr.request.postDataEntries.map((x) => Buffer.from(x.bytes || '', 'base64').toString('utf8')).join('');
        const kind = api[1].toLowerCase();
        if (pr.request.method === 'POST') {
          let res = FAKE[kind], code = 200;
          if (kind === 'rfp' && rfpFails > 0) { rfpFails--; res = { code: 'test_fail', message: 'intercepted test failure' }; code = 500; }
          posts.push({ kind, method: 'POST', url: pr.request.url, body, answered: code, t: Date.now() });
          send('Fetch.fulfillRequest', { requestId: pr.requestId, responseCode: code, responseHeaders: [{ name: 'Content-Type', value: 'application/json; charset=utf-8' }], body: Buffer.from(JSON.stringify(res)).toString('base64') }).catch(() => {});
        } else {
          posts.push({ kind, method: pr.request.method, url: pr.request.url, answered: 'stub' });
          send('Fetch.fulfillRequest', { requestId: pr.requestId, responseCode: 200, responseHeaders: [{ name: 'Content-Type', value: 'text/html; charset=utf-8' }], body: Buffer.from('<!doctype html><title>stub</title>intercepted request document').toString('base64') }).catch(() => {});
        }
        return;
      }
      if (pr.responseStatusCode != null) { // a document: patch it
        try {
          const b = await send('Fetch.getResponseBody', { requestId: pr.requestId }); let html = b.base64Encoded ? Buffer.from(b.body, 'base64').toString('utf8') : b.body;
          const r = L === 'he' ? patchHe(html) : L === 'fr' ? patchFr(html) : { html, applied: [] }; patched.push(...r.applied);
          send('Fetch.fulfillRequest', { requestId: pr.requestId, responseCode: 200, responseHeaders: [{ name: 'Content-Type', value: 'text/html; charset=utf-8' }, { name: 'Cache-Control', value: 'no-store' }], body: Buffer.from(r.html, 'utf8').toString('base64') }).catch(() => {});
        } catch (x) { send('Fetch.continueRequest', { requestId: pr.requestId }).catch(() => {}); }
        return;
      }
      const k = '/wp-content/plugins/nadlan-config/assets/', i = u.pathname.indexOf(k), rel = i >= 0 ? u.pathname.slice(i + k.length) : '';
      if (LOCAL.includes(rel)) {
        const body = await fs.readFile(path.join(ASSETS, rel)); served.add(rel);
        send('Fetch.fulfillRequest', { requestId: pr.requestId, responseCode: 200, responseHeaders: [{ name: 'Content-Type', value: rel.endsWith('.css') ? 'text/css; charset=utf-8' : rel.endsWith('.json') ? 'application/json; charset=utf-8' : 'application/javascript; charset=utf-8' }, { name: 'Cache-Control', value: 'no-store' }, { name: 'Access-Control-Allow-Origin', value: '*' }], body: body.toString('base64') }).catch(() => {});
      } else send('Fetch.continueRequest', { requestId: pr.requestId }).catch(() => {});
    }
  };
  await send('Page.enable'); await send('Runtime.enable'); await send('Network.enable', { maxPostDataSize: 0 }); await send('Network.setCacheDisabled', { cacheDisabled: true });
  await send('Fetch.enable', { patterns: [{ urlPattern: '*nadlan/v1/lead*', requestStage: 'Request' }, { urlPattern: '*nadlan/v1/rfp*', requestStage: 'Request' },
    { urlPattern: '*nadlan-config/assets/*', requestStage: 'Request' }, { urlPattern: '*/projects/hamedina*', resourceType: 'Document', requestStage: 'Response' }] });
  await send('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: 1, mobile: MOB });
  if (MOB) await send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
  await send('Page.addScriptToEvaluateOnNewDocument', { source: `window.__ga = []; window.__facing = []; addEventListener('nl:facing', (e) => window.__facing.push(e.detail));
    (() => { let f = null; Object.defineProperty(window, 'nadlanGA', { configurable: true, get() { return (n, p) => { if (window.__gaIn) { if (f) return f(n, p); return; } window.__ga.push([n, p || {}]); window.__gaIn = 1; try { if (f) f(n, p); } catch (e) {} window.__gaIn = 0; }; }, set(v) { f = v; } }); })();` });
  const ev = async (x) => { const r = await send('Runtime.evaluate', { expression: x, awaitPromise: true, returnByValue: true }); if (r.exceptionDetails) return 'EXC ' + JSON.stringify(r.exceptionDetails).slice(0, 300); return r.result.value; };
  const go = async (url) => { await send('Page.navigate', { url }); for (let i = 0; i < 60 && !(await ev("document.readyState==='complete'")); i++) await sleep(1000); };
  const shot = async (name) => { await sleep(500); const s = await send('Page.captureScreenshot', { format: 'jpeg', quality: 72 }); await fs.writeFile(path.join(OUT, name + '.jpg'), Buffer.from(s.data, 'base64')); return name; };
  const until = async (x, ms = 20000) => { for (let t = 0; t < ms; t += 250) { if (await ev(x) === true) return true; await sleep(250); } return false; };
  const tapAt = async (x, y) => {
    x = Math.round(x); y = Math.round(y);
    if (MOB) { await send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x, y }] }); await sleep(50); await send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }); }
    else { await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x, y }); await send('Input.dispatchMouseEvent', { type: 'mousePressed', x, y, button: 'left', clickCount: 1 }); await sleep(50); await send('Input.dispatchMouseEvent', { type: 'mouseReleased', x, y, button: 'left', clickCount: 1 }); }
  };
  const swipe = async (x, y0, y1) => { const n = 8; await send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x, y: y0 }] }); for (let i = 1; i <= n; i++) { await sleep(16); await send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x, y: Math.round(y0 + (y1 - y0) * i / n) }] }); } await send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }); };
  const key = async (k, code) => { await send('Input.dispatchKeyEvent', { type: 'keyDown', key: k, code: k, windowsVirtualKeyCode: code }); await send('Input.dispatchKeyEvent', { type: 'keyUp', key: k, code: k, windowsVirtualKeyCode: code }); };
  const close = async () => { try { ws.close(); } catch { /* none */ } ch.kill(); await sleep(400); await fs.rm(dir, { recursive: true, force: true }).catch(() => {}); };
  return { send, ev, go, shot, until, tapAt, swipe, key, close, errs, served, reqs, failed, patched, MOB, posts };
}
export { patchHe, patchFr };

// page helpers (strings evaluated in the page)
const RECT = (sel) => `(() => { const e = document.querySelector(${JSON.stringify(sel)}); if (!e) return null; const r = e.getBoundingClientRect(); return { x: r.left, y: r.top, w: r.width, h: r.height, b: r.bottom, r: r.right }; })()`;
const PULSE = `(() => { const L = [...document.querySelectorAll('.nlsr-pulse,.nlsr-pulse-b,.nlpf__apt--pulse')].filter((e) => e.isConnected);
  const lab = (e) => { if (e.closest('.nlck')) { const w = document.querySelector('.nlck-wl'); return w && !w.hidden ? w.innerText.trim() : ''; } const h = document.querySelector('.nlsr-hint'); return h && !h.hidden ? h.innerText.trim() : ''; };
  return { n: L.length, what: L.map((e) => (e.className.baseVal != null ? 'svg' : e.tagName.toLowerCase() + '.' + [...e.classList].filter((c) => !/pulse/.test(c)).join('.')) + (e.dataset.open ? '[' + e.dataset.open + ']' : '') + (e.dataset.act ? '[' + e.dataset.act + ']' : '') + (e.dataset.pano ? '[pano ' + e.dataset.pano + ']' : '')), label: L[0] ? lab(L[0]) : '' }; })()`;
const T = (k) => `window.__nlI18n.t(${JSON.stringify(k)})`;
const HEB = `(() => { const H = /[\\u0590-\\u05FF]/, out = []; for (const sel of ['.nlsr', '.nlck', '.nlbk']) { const r = document.querySelector(sel); if (!r) continue;
  const walk = (n) => { if (n.nodeType === 3) { if (H.test(n.nodeValue) && n.parentElement && n.parentElement.offsetParent !== null) out.push(sel + ': ' + n.nodeValue.trim().slice(0, 80)); return; } if (n.nodeType !== 1 || n.tagName === 'STYLE' || n.tagName === 'SCRIPT') return;
    for (const a of ['alt', 'aria-label', 'title', 'placeholder']) { const v = n.getAttribute(a); if (v && H.test(v)) out.push(sel + ' @' + a + ': ' + v.slice(0, 80)); } for (const k of n.childNodes) walk(k); }; walk(r); } return out; })()`;
const HSCROLL = '(document.documentElement.scrollWidth > innerWidth + 1) || (document.body.scrollWidth > innerWidth + 1)';
const SMALL = (root) => `(() => { const out = []; for (const e of document.querySelectorAll(${JSON.stringify(root)})) { if (e.offsetParent === null && getComputedStyle(e).position !== 'fixed') continue; const r = e.getBoundingClientRect(); if (!r.width) continue; if (r.width < 44 - 0.5 || r.height < 44 - 0.5) out.push((e.dataset.fl || e.dataset.act || e.dataset.vdt || e.className || e.tagName) + ' ' + Math.round(r.width) + 'x' + Math.round(r.height)); } return out; })()`;
const BAND = `(() => { const p = document.querySelector('.nlsr-band'); if (!p) return null; const r = p.getBoundingClientRect(), s = document.querySelector('.nlsr-stage').getBoundingClientRect(), c = document.querySelector('.nlsr-card'); const cr = c && !c.hidden && c.parentNode === document.querySelector('.nlsr-stage') ? c.getBoundingClientRect() : null;
  return { top: r.top, bottom: r.bottom, cx: r.left + r.width / 2, stageTop: s.top, stageBottom: s.bottom, cardTop: cr ? cr.top : s.bottom, visible: r.top >= s.top - 1 && r.bottom <= (cr ? cr.top : s.bottom) + 1 }; })()`;
const FLOOR = `(() => { const m = /#dira=([ABC])(\\d+)-(\\d+)/.exec(location.hash); return m ? { tower: m[1], floor: +m[2], bearing: +m[3] } : null; })()`;

async function run(L, w, h) {
  const b = await browser({ w, h, L }); const tag = `${L}-${w}`; const R = { L, w, h, steps: [], checks: {} };
  const step = async (name, expectKey, extra) => { const p = await b.ev(PULSE); const exp = expectKey ? await b.ev(T(expectKey)) : ''; const ok = expectKey ? p.n === 1 && p.label === exp : p.n === 0;
    const s = { name, pulses: p.n, what: p.what, label: p.label, expected: exp, ok, ...(extra || {}) }; R.steps.push(s); return s; };
  await b.go(URLS[L]);
  R.patched = b.patched;
  if (!(await b.until("!!document.querySelector('.nlsr .nlsr-steps li') && !!document.querySelector('.nlsr-h')", 40000))) { R.error = 'showroom did not mount'; await b.close(); return R; }
  await sleep(2500);
  R.checks.worldOnLoad = b.reqs.filter((r) => /world\/world\.js|three\.module\.js|three@/.test(r.url)).map((r) => r.url.split('/').slice(-2).join('/'));
  await b.ev("document.querySelector('.nlsr').scrollIntoView({block:'start',behavior:'instant'}); scrollBy(0,-70); true"); await sleep(600);
  await step('1 tower', 'sr_hint_tower'); await b.shot(`${tag}-01-towers`);
  // tower B by a real tap
  let r = await b.ev(RECT('.nlsr [data-tower="B"]')); await b.tapAt(r.x + r.w / 2, r.y + r.h / 2); await sleep(2200);
  await step('2 floor on the tower', 'sr_hint_floor'); await b.shot(`${tag}-02-tower`);
  // a floor tapped on the tower (the middle first)
  await b.ev("document.querySelector('.nlsr-stage').scrollIntoView({block:'center',behavior:'instant'}); true"); await sleep(700);
  const st = await b.ev(RECT('.nlsr-stage')); let picked = false;
  for (const f of [0.5, 0.45, 0.55, 0.4, 0.6, 0.35]) { await b.tapAt(st.x + st.w / 2, st.y + st.h * f); await sleep(900); if (await b.ev("!document.querySelector('.nlsr-card').hidden")) { picked = true; break; } }
  if (!picked) { R.error = 'no floor picked'; await b.close(); return R; }
  await sleep(1200);
  const s3 = await step('3 after the floor tap: step inside (the side came with the tap, the plan step skipped)', 'way_enter');
  const stg = await b.ev(RECT('.nlsr-stage')), card = await b.ev(RECT('.nlsr-card'));
  R.checks.peek = { stageH: Math.round(stg.h), stageW: Math.round(stg.w), cardH: card ? Math.round(card.h) : null, share: card ? +(card.h / stg.h).toFixed(3) : null, parentIsStage: await b.ev("document.querySelector('.nlsr-card').parentNode.classList.contains('nlsr-stage')"),
    titleOneLine: await b.ev("(() => { const e = document.querySelector('.nlsr-ct'); return e.getBoundingClientRect().height <= 24 ? e.innerText : 'WRAPS ' + e.innerText; })()"), band: await b.ev(BAND), small: await b.ev(SMALL('.nlsr button, .nlsr a')) };
  await b.shot(`${tag}-03-peek`);
  // the basket's Design section on Kikar (item 4): the way inside, never "not available"
  R.checks.basketDesign = await b.ev(`(() => { if (!window.__nlBasket) return 'no basket'; window.__nlBasket.open(); const t = document.querySelector('.nlbk').innerText; window.__nlBasket.close();
    return { goInside: t.includes(${T('bk_go_inside')}), notAvailable: t.includes(${T('bk_inside_na')}) }; })()`);
  if (b.MOB) {
    // the lowest and the highest floor are tappable with the sheet at peek
    const reach = async (from, dirn) => { for (let k = 0; k < 120; k++) { const bd = await b.ev(BAND), y = from() + dirn * k * 3; const s = await b.ev(RECT('.nlsr-stage')), c = await b.ev(RECT('.nlsr-card'));
        if (y < s.y + 2 || y > c.y - 2) break; const before = await b.ev('location.hash'); await b.tapAt(bd.cx, y); await sleep(450); if ((await b.ev('location.hash')) !== before || k === 0) return { y: Math.round(y), ...(await b.ev(FLOOR)) }; } return null; };
    const c0 = await b.ev(RECT('.nlsr-card')), s0 = await b.ev(RECT('.nlsr-stage'));
    const low = await reach(() => c0.y - 3, -1); await sleep(600); const lowShot = await b.shot(`${tag}-04-lowest-floor-peek`);
    const s1 = await b.ev(RECT('.nlsr-stage'));
    const high = await reach(() => s1.y + 3, 1); await sleep(600); await b.shot(`${tag}-04-highest-floor-peek`);
    R.checks.reach = { lowest: low, highest: high, floors: await b.ev("(() => { const m = /#dira=([ABC])/.exec(location.hash); return m ? ({ A: 40, B: 37, C: 40 })[m[1]] : null; })()"), peekShareAfter: await b.ev("(() => { const c = document.querySelector('.nlsr-card').getBoundingClientRect().height, s = document.querySelector('.nlsr-stage').getBoundingClientRect().height; return +(c / s).toFixed(3); })()"), bandAfter: await b.ev(BAND) };
    // back to a middle floor for the rest of the walk
    for (let k = 0; k < 8; k++) { const f = await b.ev(FLOOR); if (f.floor <= 24) break; r = await b.ev(RECT('.nlsr-cstep [data-fl="-1"]')); for (let j = 0; j < 4; j++) { await b.tapAt(r.x + r.w / 2, r.y + r.h / 2); await sleep(250); } }
    await sleep(700);
    // expanded: the handle; then the four ways to fold it
    const sheet = () => b.ev("document.querySelector('.nlsr-card').dataset.sheet");
    const grab = async () => { const g = await b.ev(RECT('.nlsr-grab')); await b.tapAt(g.x + g.w / 2, g.y + g.h / 2); await sleep(700); };
    await grab();
    const ex = await b.ev(RECT('.nlsr-card')), st2 = await b.ev(RECT('.nlsr-stage'));
    R.checks.expanded = { state: await sheet(), cardH: Math.round(ex.h), share: +(ex.h / st2.h).toFixed(3), band: await b.ev(BAND), plan: await b.ev("!!document.querySelector('.nlsr-plan svg')"), small: await b.ev(SMALL('.nlsr-card button, .nlsr-card a')),
      ariaExpanded: await b.ev("document.querySelector('.nlsr-grab').getAttribute('aria-expanded')"), labels: await b.ev("[...document.querySelectorAll('.nlsr-plan text')].map((t) => t.textContent)") };
    await step('3b expanded (the pulse stays on step inside)', 'way_enter'); await b.shot(`${tag}-05-expanded`);
    // the plan: another apartment, as "another direction" does
    const f0 = await b.ev(FLOOR), nf0 = await b.ev('window.__facing.length');
    const ap = await b.ev(`(() => { const a = [...document.querySelectorAll('.nlsr-plan .nlpf__apt')].find((p) => p.getAttribute('aria-pressed') === 'false'); const r = a.getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top + r.height / 2, name: a.getAttribute('aria-label') }; })()`);
    await b.tapAt(ap.x, ap.y); await sleep(1500);
    const f1 = await b.ev(FLOOR);
    R.checks.plan = { tapped: ap.name, before: f0, after: f1, changed: f0.bearing !== f1.bearing, facingEvents: (await b.ev('window.__facing.length')) - nf0, lastFacing: await b.ev('window.__facing[window.__facing.length-1]'),
      pressed: await b.ev("[...document.querySelectorAll('.nlsr-plan .nlpf__apt')].filter((p) => p.getAttribute('aria-pressed') === 'true').map((p) => p.getAttribute('aria-label'))"), mapline: await b.ev("document.querySelector('.nlsr-mapline').innerText"), sheet: await sheet() };
    await step('3c plan apartment tapped', 'way_enter'); await b.shot(`${tag}-06-plan-apartment`);
    if ((await sheet()) !== 'open') await grab();
    // fold 1: the handle
    await grab(); const w1 = await sheet();
    // fold 2: Escape
    await grab(); await b.key('Escape', 27); await sleep(500); const w2 = await sheet();
    // fold 3: a tap on the tower
    await grab(); const s4 = await b.ev(RECT('.nlsr-stage')); const bd = await b.ev(BAND); await b.tapAt(bd.cx, s4.y + 70); await sleep(800); const w3 = await sheet();
    // fold 4: a swipe down on the sheet's row
    await grab(); const pk = await b.ev(RECT('.nlsr-peek .nlsr-ct')); const y0s = await b.ev('scrollY'); await b.swipe(pk.x + pk.w / 2, pk.y + 4, pk.y + 90); await sleep(700); const w4 = await sheet(); const y1s = await b.ev('scrollY');
    // a map tap folds it too
    await grab(); const mp = await b.ev(RECT('.nlsr-map')); await b.ev("document.querySelector('.nlsr-map').scrollIntoView({block:'center',behavior:'instant'}); true"); await sleep(400); const mp2 = await b.ev(RECT('.nlsr-map')); await b.tapAt(mp2.x + mp2.w / 2, mp2.y + mp2.h / 2); await sleep(600); const w5 = await sheet();
    R.checks.fold = { handle: w1, esc: w2, stage: w3, swipe: w4, swipePageScroll: y1s - y0s, map: w5, ga: await b.ev("window.__ga.filter(([n]) => /^sheet_|_after_card$/.test(n)).reduce((o, [n, p]) => { const k = n + (p.how ? ':' + p.how : ''); o[k] = (o[k] || 0) + 1; return o; }, {})") };
    await b.ev("document.querySelector('.nlsr-stage').scrollIntoView({block:'center',behavior:'instant'}); true"); await sleep(500);
  } else {
    const c = await b.ev(RECT('.nlsr-card')), s = await b.ev(RECT('.nlsr-stage')), isHe = L === 'he';
    R.checks.desktop = { cardBesideTower: c.r <= s.x + 1 || c.x >= s.r - 1, side: c.x >= s.r - 1 ? 'right' : (c.r <= s.x + 1 ? 'left' : 'over'), expectSide: isHe ? 'right' : 'left', plan: await b.ev("!!document.querySelector('.nlsr-plan svg')"), small: await b.ev(SMALL('.nlsr-card button, .nlsr-card a')), band: await b.ev(BAND) };
    await b.shot(`${tag}-04-card-beside`);
    const ap = await b.ev(`(() => { const a = [...document.querySelectorAll('.nlsr-plan .nlpf__apt')].find((p) => p.getAttribute('aria-pressed') === 'false'); a.scrollIntoView({block:'center',behavior:'instant'}); const r = a.getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top + r.height / 2, name: a.getAttribute('aria-label') }; })()`);
    const f0 = await b.ev(FLOOR); await b.tapAt(ap.x, ap.y); await sleep(1500); const f1 = await b.ev(FLOOR);
    R.checks.plan = { tapped: ap.name, before: f0, after: f1, changed: f0.bearing !== f1.bearing, mapline: await b.ev("document.querySelector('.nlsr-mapline').innerText") };
    await step('3c plan apartment tapped', 'way_enter'); await b.shot(`${tag}-06-plan-apartment`);
  }
  R.checks.hscrollShowroom = await b.ev(HSCROLL);
  // step inside
  r = await b.ev("(() => { const e = document.querySelector('.nlsr-go'); e.scrollIntoView({block:'center',behavior:'instant'}); const r = e.getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top + r.height / 2 }; })()");
  await b.tapAt(r.x, r.y);
  await b.until("!!document.querySelector('.nlck') && !document.querySelector('.nlck').hidden && !!document.querySelector('.nlck-grid')", 20000); await sleep(2500);
  await step('4 apartment screen: the view', 'way_view', { heroDetails: await b.ev("document.querySelectorAll('.nlck-hero .nlvd__b').length") }); await b.shot(`${tag}-07-apartment-screen`);
  const tapSel = async (sel) => { const q = await b.ev(`(() => { const e = document.querySelector(${JSON.stringify(sel)}); if (!e) return null; e.scrollIntoView({block:'nearest',behavior:'instant'}); const r = e.getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top + r.height / 2 }; })()`); if (!q) return false; await b.tapAt(q.x, q.y); return true; };
  await tapSel('.nlck-tile[data-open="view"]'); await sleep(1500);
  await b.until("document.querySelectorAll('.nlck-pan .nlvd__b').length >= 1", 8000); await sleep(800);
  // a view that faces the city: walk the other directions of the same floor until at least two names are drawn
  let vd = await b.ev("document.querySelectorAll('.nlck-pan .nlvd__b').length"), tries = [];
  tries.push({ cap: await b.ev("document.querySelector('.nlck-cap').innerText"), labels: vd });
  for (let i = 0; i < 4 && vd < 2; i++) { const okk = await b.ev(`(() => { const L = [...document.querySelectorAll('[data-vk="side"]')]; const e = L.find((x) => x.getAttribute('aria-pressed') === 'false' && !x.dataset.tried); if (!e) return false; e.dataset.tried = 1; e.click(); return true; })()`); if (!okk) break; await sleep(1800); vd = await b.ev("document.querySelectorAll('.nlck-pan .nlvd__b').length"); tries.push({ cap: await b.ev("document.querySelector('.nlck-cap').innerText"), labels: vd }); }
  const names = await b.ev("[...document.querySelectorAll('.nlck-pan .nlvd__b')].map((x) => x.innerText.replace(/\\n/g, ' | '))");
  await step('5 view screen (details on): back to the apartment', 'way_back'); await b.shot(`${tag}-08-view-details-on`);
  await tapSel('[data-vdt="0"]'); await sleep(500); const off = await b.ev("({ off: [...document.querySelectorAll('.nlck-pan .nlvd')].every((x) => x.classList.contains('nlvd--off')), pressed: document.querySelector('[data-vdt=\"0\"]').getAttribute('aria-pressed') })");
  await b.shot(`${tag}-09-view-picture`);
  await tapSel('[data-vdt="1"]'); await sleep(500); const on = await b.ev("({ on: document.querySelectorAll('.nlck-pan .nlvd:not(.nlvd--off) .nlvd__b').length })");
  R.checks.viewDetails = { labels: vd, tries, names, toggleOff: off, toggleOn: on, threeDButton: await b.ev("document.querySelector('[data-act=\"3d\"]') ? document.querySelector('[data-act=\"3d\"]').innerText : null"), small: await b.ev(SMALL('.nlck-vdt button, .nlck-3d')) };
  R.checks.worldBefore3d = b.reqs.filter((x) => /world\/world\.js/.test(x.url)).length;
  R.checks.threeBeforeInside = b.reqs.filter((x) => /three\.module\.js|three@/.test(x.url)).length;
  // back, inside
  await tapSel('.nlck-subtop .nlck-back'); await sleep(1200);
  await step('6 apartment screen: inside', 'way_inside');
  await tapSel('.nlck-tile[data-open="inside"]'); await sleep(3500);
  await step('7 inside: a finish', 'way_design'); await b.shot(`${tag}-10-inside-finish`);
  await tapSel('.nlck [data-pano][aria-pressed="false"]'); await sleep(2500);
  await step('8 My selection', 'way_basket'); await b.shot(`${tag}-11-basket-next`);
  await tapSel('.nlck [data-act="basket"]'); await sleep(1500);
  R.checks.basketAfter = await b.ev(`(() => { const t = document.querySelector('.nlbk').innerText; return { open: !document.querySelector('.nlbk').hidden, notAvailable: t.includes(${T('bk_inside_na')}), style: (window.__nlBasket.state || {}).style }; })()`);
  await b.shot(`${tag}-12-basket`);
  await b.key('Escape', 27); await sleep(700);
  const callHref = await b.ev("document.querySelector('.nlck-call').getAttribute('href')");
  await step('9 the video call', 'way_call', { callHref }); await b.shot(`${tag}-13-call-next`);
  R.checks.hscrollCockpit = await b.ev(HSCROLL);
  R.checks.smallCockpit = await b.ev(SMALL('.nlck-bar a, .nlck-bar button, .nlck-tile, .nlck-back'));
  if (callHref === '#nlsch') { await tapSel('.nlck-call'); await sleep(1200); await step('10 all done: no pulse', null); }
  else R.steps.push({ name: '10 call not tapped (a live room would open)', ok: true });
  R.checks.hebrew = L === 'he' ? 'n/a' : await b.ev(HEB);
  // the live 3D on its tap
  const wB = b.reqs.filter((x) => /world\/world\.js/.test(x.url)).length;
  await sleep(1500); // (setup, not under test: open the apartment screen on its view by click)
  if (await b.ev("!!document.querySelector('.nlck') && document.querySelector('.nlck').hidden")) { await b.ev("document.querySelector('.nlsr-go').click(); true"); await b.until("!document.querySelector('.nlck').hidden && !!document.querySelector('.nlck-grid')", 15000); await sleep(1000); }
  await b.ev("(document.querySelector('.nlck-tile[data-open=\"view\"]') || {click(){}}).click(); true"); await b.until("!!document.querySelector('.nlck-pan img[data-vdimg]')", 10000); await sleep(800);
  const want = await b.ev("(() => { const i = document.querySelector('.nlck-pan img[data-vdimg]'); return i ? i.dataset.vdimg : null; })()");
  await tapSel('[data-act="3d"]'); await sleep(1500);
  const okW = await b.until('!!window.__nlpsWorld', 30000); await sleep(9000);
  R.checks.threeD = { wanted: want, worldRequestedBeforeTap: wB, worldRequestedAfterTap: b.reqs.filter((x) => /world\/world\.js/.test(x.url)).length, mounted: okW,
    stagebox: await b.ev("(() => { const s = document.querySelector('.nlps-stagebox'); if (!s) return null; const r = s.getBoundingClientRect(); return { display: getComputedStyle(s).display, top: Math.round(r.top), h: Math.round(r.height) }; })()"),
    state: await b.ev("(() => { try { return window.__nlpsWorld.getState(); } catch (e) { return String(e); } })()"), cockpitHidden: await b.ev("document.querySelector('.nlck').hidden") };
  await b.shot(`${tag}-14-live-3d`);
  R.checks.hscrollEnd = await b.ev(HSCROLL);
  R.errs = b.errs; R.failed = b.failed.filter((f) => f.url); R.served = [...b.served];
  R.ok = R.steps.every((s) => s.ok);
  await b.close();
  return R;
}

if (process.argv[1] && process.argv[1].endsWith('waymarks_test.mjs')) await main();
async function main() {
const report = { started: new Date().toISOString(), runs: [] };
const plan = { he: [[390, 844], [1440, 900]], en: [[390, 844], [1440, 900]], fr: [[390, 844], [1440, 900]] };
for (const L of MODE === 'all' ? ['he', 'en', 'fr'] : [MODE]) for (const [w, h] of plan[L]) {
  const r = await run(L, w, h); report.runs.push(r);
  console.log(L, w, 'steps ok', r.ok, r.error || '', 'errs', (r.errs || []).length, 'failed', (r.failed || []).length);
}
report.finished = new Date().toISOString();
await fs.writeFile(path.join(OUT, `result-${MODE}.json`), JSON.stringify(report, null, 1));
console.log('written', path.join(OUT, `result-${MODE}.json`));
}
