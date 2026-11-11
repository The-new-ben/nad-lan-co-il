// HAD-712 (11.11.2026): the Kikar showroom in Hebrew, English and French, tested on the LIVE pages with the LOCAL asset files.
// Headless Chrome (CDP). Fetch.requestPaused serves the repo's versions of the edited files (matched on the path under
// /wp-content/plugins/nadlan-config/assets/, query ignored); everything else comes from the live site. GETs only: nothing is
// submitted, no WhatsApp link is followed.
//   node i18n_test.mjs [he|en|fr|all]
// he: the Hebrew page twice per size (live files, then local files), the same walk, the visible text and the HTML compared.
// en/fr: the English page; the PHP does not mount the showroom there yet, so the Hebrew page's config is copied in with lang
// en/fr before load, and the showroom, the cockpit and the basket are mounted the way the Hebrew page's inline script does it.
import { spawn } from 'node:child_process'; import fs from 'node:fs/promises'; import os from 'node:os'; import path from 'node:path';
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const OUT = path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1'));
const REPO = path.resolve(OUT, '../../../../..');
const ASSETS = path.join(REPO, 'plugins/nadlan-config/assets');
const LOCAL = ['project-stage/world/showroom.js', 'project-stage/world/showroom-i18n.js', 'project-stage/world/cockpit.js', 'project-stage/world/journey.js',
  'basket/basket.js', 'project-stage/world/showroom.css', 'project-stage/world/cockpit.css', 'basket/basket.css'];
const HE_URL = 'https://nad-lan.co.il/projects/hamedina/', EN_URL = 'https://nad-lan.co.il/projects/hamedina-en/';
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const MODE = process.argv[2] || 'all';
const report = { started: new Date().toISOString(), he: {}, en: {}, fr: {} };

async function browser({ w, h, local, pre }) {
  const PORT = 9300 + Math.floor(Math.random() * 500), MOB = w < 900;
  const dir = await fs.mkdtemp(path.join(os.tmpdir(), 'i18n-'));
  const ch = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${dir}`, '--no-first-run', '--hide-scrollbars', '--enable-unsafe-swiftshader', '--use-angle=swiftshader', 'about:blank'], { stdio: 'ignore' });
  for (let i = 0; i < 80; i++) { try { await (await fetch(`http://127.0.0.1:${PORT}/json/version`)).json(); break; } catch { await sleep(250); } }
  const tg = await (await fetch(`http://127.0.0.1:${PORT}/json/new?about:blank`, { method: 'PUT' })).json();
  const ws = new WebSocket(tg.webSocketDebuggerUrl); let id = 0; const P = new Map(); const errs = [], warns = [], served = new Set();
  await new Promise((r) => (ws.onopen = r));
  const send = (m, p = {}) => new Promise((ok, no) => { const i = ++id; P.set(i, { ok, no }); ws.send(JSON.stringify({ id: i, method: m, params: p })); });
  ws.onmessage = async (e) => {
    const m = JSON.parse(e.data);
    if (m.id && P.has(m.id)) { const q = P.get(m.id); P.delete(m.id); m.error ? q.no(new Error(JSON.stringify(m.error))) : q.ok(m.result); return; }
    if (m.method === 'Runtime.exceptionThrown') { const d = m.params.exceptionDetails; errs.push(((d.exception && d.exception.description) || d.text || '').split('\n')[0].slice(0, 200) + ' @ ' + (d.url || '').split('/').pop()); }
    if (m.method === 'Runtime.consoleAPICalled' && /warning|error/.test(m.params.type)) { const s = m.params.args.map((a) => a.value || a.description || '').join(' '); if (/showroom|cockpit|journey|basket|i18n/i.test(s)) warns.push(s.slice(0, 200)); }
    if (m.method === 'Fetch.requestPaused') {
      const u = new URL(m.params.request.url), k = '/wp-content/plugins/nadlan-config/assets/', i = u.pathname.indexOf(k), rel = i >= 0 ? u.pathname.slice(i + k.length) : '';
      if (LOCAL.includes(rel)) {
        const body = await fs.readFile(path.join(ASSETS, rel)); served.add(rel);
        send('Fetch.fulfillRequest', { requestId: m.params.requestId, responseCode: 200, responseHeaders: [{ name: 'Content-Type', value: rel.endsWith('.css') ? 'text/css; charset=utf-8' : 'application/javascript; charset=utf-8' }, { name: 'Cache-Control', value: 'no-store' }], body: body.toString('base64') }).catch(() => {});
      } else send('Fetch.continueRequest', { requestId: m.params.requestId }).catch(() => {});
    }
  };
  await send('Page.enable'); await send('Runtime.enable'); await send('Network.enable');
  if (local) await send('Fetch.enable', { patterns: [{ urlPattern: '*nadlan-config/assets/*', requestStage: 'Request' }] });
  await send('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: 1, mobile: MOB });
  if (MOB) await send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
  if (pre) await send('Page.addScriptToEvaluateOnNewDocument', { source: pre });
  const ev = async (x) => { const r = await send('Runtime.evaluate', { expression: x, awaitPromise: true, returnByValue: true }); if (r.exceptionDetails) return 'EXC ' + JSON.stringify(r.exceptionDetails).slice(0, 300); return r.result.value; };
  const go = async (url) => { await send('Page.navigate', { url }); for (let i = 0; i < 60 && !(await ev("document.readyState==='complete'")); i++) await sleep(1000); };
  const shot = async (name) => { await sleep(700); const s = await send('Page.captureScreenshot', { format: 'jpeg', quality: 72 }); await fs.writeFile(path.join(OUT, name + '.jpg'), Buffer.from(s.data, 'base64')); return name; };
  const until = async (x, ms = 20000) => { for (let t = 0; t < ms; t += 250) { if (await ev(x) === true) return true; await sleep(250); } return false; };
  const tapAt = async (x, y) => {
    if (MOB) { await send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x, y }] }); await sleep(60); await send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }); }
    else { await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x, y }); await send('Input.dispatchMouseEvent', { type: 'mousePressed', x, y, button: 'left', clickCount: 1 }); await sleep(60); await send('Input.dispatchMouseEvent', { type: 'mouseReleased', x, y, button: 'left', clickCount: 1 }); }
  };
  const close = async () => { try { ws.close(); } catch { /* none */ } ch.kill(); await sleep(400); await fs.rm(dir, { recursive: true, force: true }).catch(() => {}); };
  return { send, ev, go, shot, until, tapAt, close, errs, warns, served, MOB };
}

// the visible state of one root: its text, its HTML (canvases and the 3D viewer's sizes dropped), and every Hebrew letter found in
// text or in alt / aria-label / title / placeholder / href (decoded)
const SNAP = `(sel) => { const r = document.querySelector(sel); if (!r) return null;
  const c = r.cloneNode(true); c.querySelectorAll('canvas').forEach((x) => x.remove());
  const heb = []; const H = /[\\u0590-\\u05FF]/;
  const walk = (n) => { if (n.nodeType === 3) { if (H.test(n.nodeValue)) heb.push('text: ' + n.nodeValue.trim().slice(0, 90)); return; } if (n.nodeType !== 1) return;
    if (n.tagName === 'STYLE' || n.tagName === 'SCRIPT') return;
    for (const a of ['alt', 'aria-label', 'title', 'placeholder', 'href']) { let v = n.getAttribute(a); if (v == null) continue; try { v = decodeURIComponent(v); } catch (e) { /* raw */ } if (H.test(v)) heb.push(a + ': ' + v.slice(0, 120)); }
    for (const k of n.childNodes) walk(k); };
  walk(r);
  return { text: r.innerText, html: c.outerHTML.replace(/ style="[^"]*"/g, ''), heb, dir: r.getAttribute('dir'), lang: r.getAttribute('lang') }; }`;
const snap = (b, sel) => b.ev(`(${SNAP})(${JSON.stringify(sel)})`);
const click = (b, sel) => b.ev(`(() => { const e = document.querySelector(${JSON.stringify(sel)}); if (!e) return 'missing ${sel.replace(/'/g, '')}'; e.click(); return true; })()`);

// the walk: all towers → tower A → a floor tapped on the tower → the card → the apartment screen (tiles) → the basket
async function walk(b, tag, shots) {
  const S = {}, put = async (k, sel) => { S[k] = await snap(b, sel); };
  const okShow = await b.until("!!document.querySelector('.nlsr .nlsr-steps li') && !!document.querySelector('.nlsr-pic') && !!document.querySelector('.nlsr-pic').getAttribute('src')", 40000);
  if (!okShow) return { error: 'showroom did not mount', S };
  await sleep(1500);
  await b.ev("document.querySelector('.nlsr').scrollIntoView({block:'start'}); scrollBy(0,-70); true");
  await put('1-all', '.nlsr'); if (shots) await b.shot(tag + '-01-towers');
  await click(b, '.nlsr [data-tower="A"]'); await sleep(1800);
  await put('2-tower', '.nlsr'); if (shots) await b.shot(tag + '-02-tower');
  // a floor tapped on the picture: the middle of the stage first, then a few heights around it
  await b.ev("document.querySelector('.nlsr-stage').scrollIntoView({block:'center'}); true"); await sleep(600);
  const r = JSON.parse(await b.ev("JSON.stringify(document.querySelector('.nlsr-stage').getBoundingClientRect())"));
  let picked = false;
  for (const f of [0.45, 0.4, 0.5, 0.35, 0.55, 0.3, 0.6]) {
    await b.tapAt(Math.round(r.left + r.width / 2), Math.round(r.top + r.height * f)); await sleep(900);
    if (await b.ev("!document.querySelector('.nlsr-card').hidden")) { picked = true; break; }
  }
  S.picked = picked;
  if (!picked) return { error: 'no floor picked by tap', S };
  await sleep(1200);
  await put('3-floor', '.nlsr'); if (shots) await b.shot(tag + '-03-floor-map');
  await b.ev("document.querySelector('.nlsr-card').scrollIntoView({block:'end'}); true"); if (shots) await b.shot(tag + '-04-card');
  S.cardWa = await b.ev("(() => { const a = document.querySelector('.nlsr-ask'); return a ? decodeURIComponent(new URL(a.href).searchParams.get('text') || '') : null; })()");
  // the apartment screen
  await click(b, '.nlsr [data-go="home"]');
  await b.until("!!document.querySelector('.nlck') && !document.querySelector('.nlck').hidden && !!document.querySelector('.nlck-grid')", 20000); await sleep(1800);
  await put('4-cockpit', '.nlck'); if (shots) await b.shot(tag + '-05-apartment-screen');
  const tiles = ['view', 'inside', 'plan', 'price', 'area', 'save', 'fac'];
  for (const k of tiles) {
    await click(b, `.nlck-tile[data-open="${k}"]`); await sleep(k === 'area' ? 3500 : k === 'inside' || k === 'fac' ? 3000 : 1500);
    if (k === 'area') await b.until("!/טוען|Loading|Chargement/.test(document.querySelector('.nlck-body').innerText)", 15000);
    if (k === 'view') S.pan = await b.ev("(() => { const p = document.querySelector('.nlck [data-pan]'); return p ? { left: Math.round(p.scrollLeft), half: Math.round((p.scrollWidth - p.clientWidth) / 2), dir: getComputedStyle(p).direction } : null; })()");
    await put('5-' + k, '.nlck');
    if (shots && (k === 'inside' || k === 'price' || k === 'view' || k === 'area')) await b.shot(tag + '-06-' + k);
    if (k === 'inside') { await click(b, '.nlck [data-room="bed"]'); await sleep(2500); await put('5-inside-bed', '.nlck'); if (shots) await b.shot(tag + '-06-inside-bedroom'); }
    await click(b, '.nlck .nlck-back'); await sleep(900);
  }
  await b.ev("document.querySelector('.nlck').dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true })); true"); await sleep(800);
  // the basket
  if (await b.ev('!!window.__nlBasket')) {
    await b.ev('window.__nlBasket.open(); true'); await sleep(1200);
    await put('6-basket', '.nlbk'); if (shots) await b.shot(tag + '-07-basket');
    await b.ev("(() => { const i = document.querySelector('.nlbk input[inputmode=numeric]'); i.value = '9580000'; i.dispatchEvent(new Event('change', { bubbles: true })); return true; })()"); await sleep(900);
    await put('7-basket-price', '.nlbk'); if (shots) await b.shot(tag + '-08-basket-price');
    S.basketLinks = await b.ev("[...document.querySelectorAll('.nlbk a[href*=\"wa.me\"]')].map((a) => decodeURIComponent(new URL(a.href).searchParams.get('text') || '')).slice(0, 2)");
  } else S.basket = 'no window.__nlBasket';
  return { S };
}

const cfgOf = async () => {
  const he = await (await fetch(HE_URL)).text(), en = await (await fetch(EN_URL)).text();
  const un = (s) => s.replace(/&quot;/g, '"').replace(/&#039;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
  const c = JSON.parse(un(/id="nlps"[^>]*data-cfg="([^"]*)"/.exec(he)[1]));
  const bk = JSON.parse(/id="nadlan-basket-cfg">([^<]*)</.exec(he)[1]);
  const bjs = /https:[^"']*basket\/basket\.js\?ver=[^"']*/.exec(he)[0], bcss = /https:[^"']*basket\/basket\.css\?ver=[^"']*/.exec(he)[0];
  const enWa = (/https:\/\/wa\.me\/\d+\?text=[^"']*/.exec(en) || [''])[0];
  return { next: c.next, bk, bjs, bcss, enWa };
};

async function hebrew(w, h) {
  const out = {};
  for (const local of [false, true]) {
    const b = await browser({ w, h, local });
    await b.go(HE_URL);
    const r = await walk(b, `he-${w}-${local ? 'local' : 'live'}`, local);
    out[local ? 'local' : 'live'] = { ...r, errs: b.errs, warns: b.warns, served: [...b.served] };
    await b.close();
  }
  const A = out.live.S, B = out.local.S, diffs = [];
  for (const k of Object.keys(A)) {
    if (!A[k] || typeof A[k] !== 'object' || !('text' in A[k])) { if (JSON.stringify(A[k]) !== JSON.stringify(B[k])) diffs.push({ k, live: A[k], local: B[k] }); continue; }
    if (!B[k]) { diffs.push({ k, local: 'missing' }); continue; }
    if (A[k].text !== B[k].text) diffs.push({ k, what: 'text', live: A[k].text, local: B[k].text });
    if (A[k].html !== B[k].html) { let i = 0; while (A[k].html[i] === B[k].html[i]) i++; diffs.push({ k, what: 'html', at: i, live: A[k].html.slice(Math.max(0, i - 120), i + 160), local: B[k].html.slice(Math.max(0, i - 120), i + 160) }); }
    if (A[k].dir !== B[k].dir || A[k].lang !== B[k].lang) diffs.push({ k, what: 'dir/lang', live: [A[k].dir, A[k].lang], local: [B[k].dir, B[k].lang] });
  }
  return { compared: Object.keys(A).length, diffs, live: { error: out.live.error, errs: out.live.errs, warns: out.live.warns }, local: { error: out.local.error, errs: out.local.errs, warns: out.local.warns, served: out.local.served } };
}

async function foreign(L, w, h, shots) {
  const c = await cfgOf();
  const ck = { ...c.next.cockpit, lang: L, wa: c.enWa || c.next.cockpit.wa }, jy = { ...c.next.journey, lang: L };
  const bk = { ...c.bk, lang: L };
  // a choice saved on the Hebrew page by the showroom before this change (its tower as Hebrew words): must show in the page language
  const legacy = { unit: { floor: 24, bearing: 262, unit: null, label: 'מגדל B' }, style: null, team: {}, price: { amount: '', buyer: 'single', lawyer: '' } };
  const pre = `window.__nlCockpitCfg = ${JSON.stringify(ck)}; window.__nlJourneyCfg = ${JSON.stringify(jy)};
    try { if (location.hostname === 'nad-lan.co.il' && !localStorage.getItem('nl-basket:${c.bk.slug}')) localStorage.setItem('nl-basket:${c.bk.slug}', ${JSON.stringify(JSON.stringify(legacy))}); } catch (e) {}`;
  const b = await browser({ w, h, local: true, pre });
  await b.go(EN_URL);
  // mount as the Hebrew page's inline script does (inc/project-stage.php: cockpit styles, cockpit, journey → showroom), plus the basket
  const mounted = await b.ev(`(async () => {
    const ck = window.__nlCockpitCfg, jy = window.__nlJourneyCfg;
    document.body.classList.add('nlck-next'); const l = document.createElement('link'); l.rel = 'stylesheet'; l.href = ck.css; document.head.appendChild(l);
    const s = document.createElement('script'); s.type = 'application/json'; s.id = 'nadlan-basket-cfg'; s.textContent = ${JSON.stringify(JSON.stringify(bk))}; document.body.appendChild(s);
    const bl = document.createElement('link'); bl.rel = 'stylesheet'; bl.href = ${JSON.stringify(c.bcss)}; document.head.appendChild(bl);
    await new Promise((r) => { const sc = document.createElement('script'); sc.src = ${JSON.stringify(c.bjs)}; sc.onload = r; sc.onerror = r; document.body.appendChild(sc); });
    await import(ck.js);
    const m = await import(jy.js); const at = document.querySelector('.nlps-page') || document.querySelector('.nlps-stagebox'); if (!at) return 'no mount point'; m.mountJourney(at); return true; })()`);
  await b.until('!!window.__nlI18n', 10000); await sleep(800);
  const legacyShown = await b.ev("(() => { window.__nlBasket.open(); const t = document.querySelector('.nlbk').innerText; window.__nlBasket.close(); return t.split('\\n').find((x) => /(Floor|Étage|קומה) \\d/.test(x)) || t.slice(0, 200); })()");
  if (shots) { await b.ev('window.__nlBasket.open(); true'); await sleep(900); await b.shot(`${L}-${w}-00-basket-saved-on-hebrew-page`); await b.ev('window.__nlBasket.close(); true'); }
  const stagebox = await b.ev("(() => { const s = document.querySelector('.nlps-stagebox'); return s ? getComputedStyle(s).display : 'none-in-page'; })()");
  const r = await walk(b, `${L}-${w}`, shots);
  const heb = {}; let hebCount = 0, dirs = {};
  for (const [k, v] of Object.entries(r.S || {})) if (v && typeof v === 'object' && 'heb' in v) { if (v.heb.length) { heb[k] = v.heb; hebCount += v.heb.length; } dirs[k] = v.dir + '/' + v.lang; }
  const res = { mounted, legacyShown, stagebox, error: r.error, picked: r.S && r.S.picked, cardWa: r.S && r.S.cardWa, basketLinks: r.S && r.S.basketLinks, pan: r.S && r.S.pan, hebCount, heb, dirs, errs: b.errs, warns: b.warns, served: [...b.served],
    sample: r.S && { floor: r.S['3-floor'] && r.S['3-floor'].text.slice(0, 600), cockpit: r.S['4-cockpit'] && r.S['4-cockpit'].text.slice(0, 500), price: r.S['5-price'] && r.S['5-price'].text.slice(0, 900), area: r.S['5-area'] && r.S['5-area'].text.slice(0, 500), basket: r.S['7-basket-price'] && r.S['7-basket-price'].text.slice(0, 1400) } };
  await b.close();
  return res;
}

if (MODE === 'he' || MODE === 'all') { report.he['390'] = await hebrew(390, 844); console.log('he 390', report.he['390'].diffs.length, 'diffs'); report.he['1440'] = await hebrew(1440, 900); console.log('he 1440', report.he['1440'].diffs.length, 'diffs'); }
if (MODE === 'en' || MODE === 'all') { report.en['390'] = await foreign('en', 390, 844, true); console.log('en 390 hebrew', report.en['390'].hebCount, 'errs', report.en['390'].errs.length); report.en['1440'] = await foreign('en', 1440, 900, true); console.log('en 1440 hebrew', report.en['1440'].hebCount, 'errs', report.en['1440'].errs.length); }
if (MODE === 'fr' || MODE === 'all') { report.fr['390'] = await foreign('fr', 390, 844, true); console.log('fr 390 hebrew', report.fr['390'].hebCount, 'errs', report.fr['390'].errs.length); }
report.finished = new Date().toISOString();
await fs.writeFile(path.join(OUT, `result-${MODE}.json`), JSON.stringify(report, null, 1));
console.log('written', path.join(OUT, `result-${MODE}.json`));
