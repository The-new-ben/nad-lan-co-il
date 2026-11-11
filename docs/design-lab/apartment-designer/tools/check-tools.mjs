// node check-tools.mjs [--port=47961] [--only=dsgsofa]   (HAD-707)
// Presses every design tool in headless Chrome at 390 px with touch, the way a person does with one thumb: every ready case,
// then a typed change in the first number field. Checks: a sensible result after every press (a figure, no NaN), the result
// changes when the case changes, no horizontal scroll, every visible control at least 44 x 44 px, the to-scale drawing where
// the tool has one, no page errors. Saves one screenshot per tool in ./evidence/ and a receipt.json.
// Serve the repo root first:  python -m http.server 47961 --bind 127.0.0.1   (from the repo root)
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const arg = (k, d) => { const a = process.argv.find((x) => x.startsWith('--' + k + '=')); return a ? a.split('=')[1] : d; };
const PORTW = arg('port', '47961'), ONLY = arg('only', '');
const URL0 = 'http://127.0.0.1:' + PORTW + '/docs/design-lab/apartment-designer/tools/harness.html';
const here = path.dirname(fileURLToPath(import.meta.url)), out = path.join(here, 'evidence');
fs.mkdirSync(out, { recursive: true });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
try { await fetch(URL0); } catch { console.error('Serve the repo root first: python -m http.server ' + PORTW + ' --bind 127.0.0.1'); process.exit(2); }
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe', PORT = 9300 + Math.floor(Math.random() * 500), profile = path.join(os.tmpdir(), 'nd-tools-' + PORT);
const chrome = spawn(CHROME, ['--headless=new', '--remote-debugging-port=' + PORT, '--user-data-dir=' + profile, '--no-first-run', '--disable-extensions', '--lang=he-IL'], { stdio: 'ignore' });
for (let i = 0; i < 80; i++) { try { if ((await fetch('http://127.0.0.1:' + PORT + '/json/version')).ok) break; } catch {} await sleep(250); }
const receipt = { when: new Date().toISOString(), width: 390, tools: {} }; let fails = 0, passes = 0;
const check = (tool, name, ok, detail) => { (receipt.tools[tool] = receipt.tools[tool] || []).push({ name, ok: !!ok, detail }); if (ok) passes++; else fails++; console.log((ok ? 'ok   ' : 'FAIL ') + tool + ': ' + name + (detail !== undefined && !ok ? '  ' + JSON.stringify(detail) : '')); };

async function page(w, h, query) {
  const t = await (await fetch('http://127.0.0.1:' + PORT + '/json/new?about:blank', { method: 'PUT' })).json();
  const ws = new WebSocket(t.webSocketDebuggerUrl); let id = 0; const pend = new Map(), errors = [];
  ws.onmessage = (ev) => { const m = JSON.parse(ev.data); if (m.id && pend.has(m.id)) { pend.get(m.id)(m.result || m.error); pend.delete(m.id); } else if (m.method === 'Runtime.exceptionThrown') errors.push(m.params.exceptionDetails.text + ' ' + ((m.params.exceptionDetails.exception || {}).description || '')); else if (m.method === 'Runtime.consoleAPICalled' && m.params.type === 'error') errors.push(m.params.args.map((a) => a.value || a.description).join(' ')); };
  await new Promise((r) => (ws.onopen = r));
  const send = (method, params = {}) => new Promise((res) => { const i = ++id; pend.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); });
  const ev = async (e) => { const r = await send('Runtime.evaluate', { expression: e, awaitPromise: true, returnByValue: true }); if (r.exceptionDetails) throw new Error(JSON.stringify(r.exceptionDetails.exception || r.exceptionDetails.text)); return r.result.value; };
  await send('Page.enable'); await send('Runtime.enable');
  await send('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: 2, mobile: true });
  await send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
  await send('Page.navigate', { url: URL0 + '?' + query + '&t=' + Date.now() });
  for (let i = 0; i < 160; i++) { if (await ev('!!window.__ready').catch(() => false)) break; await sleep(150); }
  await ev('document.fonts ? document.fonts.ready.then(()=>1) : 1').catch(() => 0);
  const touch = (type, x, y) => send('Input.dispatchTouchEvent', { type, touchPoints: type === 'touchEnd' ? [] : [{ x, y, id: 1 }] });
  return {
    ev, errors, send,
    tap: async (x, y) => { await touch('touchStart', x, y); await sleep(40); await touch('touchEnd'); await sleep(260); },
    tapSel: async function (sel) { const c = await ev(`(()=>{const e=document.querySelector(${JSON.stringify(sel)});if(!e)return null;e.scrollIntoView({block:'center'});const r=e.getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]})()`); if (!c) return false; await sleep(120); await this.tap(c[0], c[1]); return true; },
    shotOf: async (sel, name) => {
      const r = await ev(`(()=>{window.scrollTo(0,0);const e=document.querySelector(${JSON.stringify(sel)}).getBoundingClientRect();return {x:0,y:e.top+scrollY,w:innerWidth,h:e.height}})()`);
      const d = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true, clip: { x: r.x, y: Math.max(0, r.y - 8), width: r.w, height: Math.min(r.h + 16, 9000), scale: 1 } });
      fs.writeFileSync(path.join(out, name + '.png'), Buffer.from(d.data, 'base64'));
    },
    close: async () => { ws.close(); await fetch('http://127.0.0.1:' + PORT + '/json/close/' + t.id).catch(() => {}); },
  };
}

const IDS = ['dsgfee', 'dsgquote', 'dsgbudget', 'dsgfurnish', 'dsgkitchen', 'dsgfloor', 'dsgpaint', 'dsgsofa', 'dsgrug', 'dsgdining', 'dsgbed', 'dsglight', 'dsgpoints', 'dsgwho', 'dsgtime', 'dsgstyle', 'dsgcurtain'];
const DRAWN = { dsgsofa: 'svg', dsgrug: 'svg', dsgdining: 'svg', dsgbed: 'svg', dsgstyle: '.nlds-sw', dsgtime: '.nlds-steps' };
const OUT = (id) => `(()=>{const a=document.querySelector('[data-nli="${id}"] .nli__out');return a?a.innerText.replace(/\s+/g,' ').trim():''})()`;
const ANS = (id) => `(()=>{const a=document.querySelector('[data-nli="${id}"] .nli__answer');return a?a.innerText.replace(/\\s+/g,' ').trim():''})()`;
const SMALL = (id) => `(()=>{const out=[];document.querySelectorAll('[data-nli="${id}"] button,[data-nli="${id}"] input,[data-nli="${id}"] select,[data-nli="${id}"] summary,[data-nli="${id}"] a').forEach(e=>{const r=e.getBoundingClientRect();if(!r.width||!r.height)return;const t=e.closest('.nli__in')||e;const q=t.getBoundingClientRect();if(q.height<44-0.5||q.width<44-0.5)out.push((e.tagName+' '+(e.textContent||e.getAttribute('aria-label')||e.type||'').trim()).slice(0,40)+' '+Math.round(q.width)+'x'+Math.round(q.height))});return out})()`;
const HSCROLL = `(()=>({doc:document.documentElement.scrollWidth,win:innerWidth,wide:[...document.querySelectorAll('.nli *')].filter(e=>{const r=e.getBoundingClientRect();return r.width&&r.right>innerWidth+1&&!e.closest('.nli__tw')}).slice(0,4).map(e=>e.tagName+'.'+e.className+' '+Math.round(e.getBoundingClientRect().right))}))()`;

try {
  for (const id of IDS.filter((x) => !ONLY || x === ONLY)) {
    const p = await page(390, 844, 'only=' + id);
    const ready = await p.ev('window.__ready');
    check(id, 'mounts and shows a result', ready && (await p.ev(`!!document.querySelector('[data-nli="${id}"] .nli__answer')`)));
    const first = await p.ev(ANS(id));
    check(id, 'opening result is readable (no NaN, not empty)', first.length > 8 && !/NaN|undefined|Infinity/.test(first), first);
    // every ready case, by touch
    const nPre = await p.ev(`document.querySelectorAll('[data-nli="${id}"] .nli__pre button').length`);
    const seen = new Set([first]);
    for (let i = 0; i < nPre; i++) {
      await p.tapSel(`[data-nli="${id}"] .nli__pre button:nth-child(${i + 1})`); await sleep(220);
      const a = await p.ev(ANS(id)), on = await p.ev(`document.querySelector('[data-nli="${id}"] .nli__pre button:nth-child(${i + 1})').getAttribute('aria-pressed')`);
      check(id, 'ready case ' + (i + 1) + ' pressed and gives a sensible result', on === 'true' && a.length > 8 && !/NaN|undefined|Infinity/.test(a), { on, a });
      seen.add(a);
    }
    if (nPre > 1) check(id, 'the ready cases change the result', seen.size >= 2, [...seen]);
    // a typed change in the first visible number field
    const inp = await p.ev(`(()=>{const e=[...document.querySelectorAll('[data-nli="${id}"] .nli__form input[inputmode="decimal"]')].find(x=>x.offsetParent);if(!e)return null;e.scrollIntoView({block:'center'});const r=e.getBoundingClientRect();return {x:r.left+r.width/2,y:r.top+r.height/2,v:e.value}})()`);
    if (inp) {
      const before = await p.ev(OUT(id));
      await p.tap(inp.x, inp.y);
      await p.ev(`(()=>{const e=document.activeElement;if(e&&e.select)e.select();return 1})()`);
      const nv = String(Math.max(2, Math.round(parseFloat(String(inp.v).replace(/[^\d.]/g, '')) * 1.5) || 3));
      await p.send('Input.insertText', { text: nv }); await sleep(450);
      const after = await p.ev(OUT(id));
      check(id, 'typing ' + inp.v + ' → ' + nv + ' in the first number field updates the result', after !== before && !/NaN|undefined/.test(after), { before: before.slice(0, 200), after: after.slice(0, 200) });
      await p.tapSel(`[data-nli="${id}"] .nli__pre button:nth-child(1)`).catch(() => {}); await sleep(250);
    }
    if (nPre) { await p.tapSel(`[data-nli="${id}"] .nli__pre button:nth-child(${Math.min(2, nPre)})`); await sleep(250); }
    if (DRAWN[id]) check(id, 'the drawing is there', await p.ev(`!!document.querySelector('[data-nli="${id}"] .nli__figure ${DRAWN[id]}')`));
    const hs = await p.ev(HSCROLL);
    check(id, 'no horizontal scroll at 390 px', hs.doc <= hs.win && hs.wide.length === 0, hs);
    const small = await p.ev(SMALL(id));
    check(id, 'every visible control is at least 44 × 44 px', small.length === 0, small);
    // the table opens, still no horizontal page scroll
    await p.tapSel(`[data-nli="${id}"] .nli__table:not([hidden]) summary`); await sleep(200);
    const hs2 = await p.ev(HSCROLL);
    check(id, 'with the table open, still no horizontal page scroll', hs2.doc <= hs2.win, hs2);
    await p.ev('window.scrollTo(0,0)'); await sleep(150);
    await p.shotOf(`#sec-${id}`, id);
    check(id, 'no page errors', p.errors.length === 0, p.errors);
    receipt.tools[id].push({ answers: [...seen] });
    await p.close();
  }
} finally {
  receipt.passes = passes; receipt.fails = fails;
  fs.writeFileSync(path.join(out, 'receipt.json'), JSON.stringify(receipt, null, 1));
  chrome.kill();
}
console.log('\n' + passes + ' passed, ' + fails + ' failed; screenshots in ' + out);
process.exit(fails ? 1 : 0);
