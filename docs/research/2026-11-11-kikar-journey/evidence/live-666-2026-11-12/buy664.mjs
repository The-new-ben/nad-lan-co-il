// HAD-712 step 6 (12.11.2026): "Build me an offer" on the LIVE Kikar pages with the LOCAL files (harness.mjs, a copy of
// map-663-test/waymarks_test.mjs with world/kikarbuy.js in LOCAL and the two POSTs intercepted: no real lead, no real document).
//   node buy664.mjs [he|en|fr|all|rainbow]
import fs from 'node:fs/promises'; import path from 'node:path';
import { browser, FAKE } from './harness.mjs';
const OUT = path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1'));
const URLS = { he: 'https://nad-lan.co.il/projects/hamedina/', en: 'https://nad-lan.co.il/projects/hamedina-en/', fr: 'https://nad-lan.co.il/projects/hamedina-en/' };
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const MODE = process.argv[2] || 'all';

const RECT = (sel) => `(() => { const e = document.querySelector(${JSON.stringify(sel)}); if (!e) return null; const r = e.getBoundingClientRect(); return { x: r.left, y: r.top, w: r.width, h: r.height, b: r.bottom, r: r.right }; })()`;
// every endless animation that runs on an element a person can see (on screen, on top at its centre)
const PULSES = `(() => { const out = [], all = []; for (const a of document.getAnimations()) { const e = a.effect && a.effect.target; if (!e || a.playState !== 'running') continue;
  if (a.effect.getTiming().iterations !== Infinity) continue; const name = (e.tagName || '').toLowerCase() + '.' + [...(e.classList || [])].join('.') + ' ' + (e.textContent || '').trim().slice(0, 28); all.push(name);
  if (!e.isConnected || (e.checkVisibility && !e.checkVisibility())) continue; const r = e.getBoundingClientRect(); if (!r.width || r.bottom < 0 || r.top > innerHeight) continue;
  const t = document.elementFromPoint(Math.min(innerWidth - 1, Math.max(0, r.left + r.width / 2)), Math.min(innerHeight - 1, Math.max(0, r.top + r.height / 2))); if (!t || !(t === e || e.contains(t))) continue; out.push(name); }
  return { n: out.length, what: out, anyRunning: all }; })()`;
const HEB = `(() => { const H = /[\\u0590-\\u05FF]/, out = []; for (const sel of ['.nlkb', '.nlbk']) { const r = document.querySelector(sel); if (!r || r.hidden) continue;
  const walk = (n) => { if (n.nodeType === 3) { if (H.test(n.nodeValue) && n.parentElement && n.parentElement.offsetParent !== null) out.push(sel + ': ' + n.nodeValue.trim().slice(0, 80)); return; } if (n.nodeType !== 1 || n.tagName === 'STYLE' || n.tagName === 'SCRIPT') return;
    for (const a of ['alt', 'aria-label', 'title', 'placeholder', 'value']) { const v = n.getAttribute(a); if (v && H.test(v)) out.push(sel + ' @' + a + ': ' + v.slice(0, 80)); } for (const k of n.childNodes) walk(k); }; walk(r); } return out; })()`;
const HSCROLL = '(document.documentElement.scrollWidth > innerWidth + 1) || (document.body.scrollWidth > innerWidth + 1)';
// targets: every button, link, choice row and field in the offer (an inline link inside a sentence is listed apart: WCAG 2.5.8 exception)
const SMALL = `(() => { const out = [], inline = []; for (const e of document.querySelectorAll('.nlkb button, .nlkb a, .nlkb label.nlkb__chk, .nlkb .nlkb__f input')) { if (e.offsetParent === null && getComputedStyle(e).position !== 'fixed') continue;
  const r = e.getBoundingClientRect(); if (!r.width) continue; if (r.width < 43.5 || r.height < 43.5) (e.closest('.nlkb__note') ? inline : out).push((e.dataset.kb || e.className || e.tagName) + ' ' + Math.round(r.width) + 'x' + Math.round(r.height)); } return { small: out, inlineLinks: inline }; })()`;
const STATE = `(() => { const k = document.querySelector('.nlkb'); if (!k || k.hidden) return { open: false }; return { open: true, dir: k.dir, lang: k.lang, step: (k.querySelector('.nlkb__cnt') || {}).textContent, title: (k.querySelector('#nlkb-t') || {}).textContent,
  apt: (k.querySelector('.nlkb__apt b') || {}).textContent, aptSub: (k.querySelector('.nlkb__apt span') || {}).textContent, rows: [...k.querySelectorAll('.nlkb__row')].map((r) => r.innerText.replace(/\\n/g, ' = ')),
  checked: [...k.querySelectorAll('[data-x]')].filter((x) => x.checked).map((x) => x.dataset.x), primary: (k.querySelector('.nlkb__foot .nlkb__go') || {}).textContent,
  err: (() => { const e = k.querySelector('.nlkb__err:not([hidden])'); return e ? e.textContent : ''; })(), ref: (k.querySelector('.nlkb__ref b') || {}).textContent || '', doc: (k.querySelector('.nlkb__doc[href]') || { getAttribute() { return ''; } }).getAttribute('href'),
  timeline: [...k.querySelectorAll('.nlkb__tl li')].map((l) => (l.classList.contains('is-on') ? '[x] ' : '[ ] ') + l.innerText.replace(/\\n/g, ' / ')), now: [...k.querySelectorAll('.nlkb__two > *')].map((a) => a.textContent + (a.href ? ' -> ' + a.href.slice(0, 40) : '')),
  bodyScroll: k.querySelector('.nlkb__body').scrollHeight > k.querySelector('.nlkb__body').clientHeight }; })()`;

async function kikar(L, w, h, opt = {}) {
  const b = await browser({ w, h, L, rfpFailFirst: opt.rfpFailFirst || 0 }); const tag = `${L}-${w}`; const R = { L, w, h, steps: [], checks: {} };
  const snap = async (name, extra) => { const s = { name, state: await b.ev(STATE), pulses: await b.ev(PULSES), targets: await b.ev(SMALL), hscroll: await b.ev(HSCROLL), hebrew: L === 'he' ? 'n/a' : await b.ev(HEB), ...(extra || {}) };
    s.ok = s.pulses.n <= 1 && !s.targets.small.length && !s.hscroll && (L === 'he' || !s.hebrew.length); R.steps.push(s); return s; };
  const tapSel = async (sel) => { const q = await b.ev(`(() => { const e = document.querySelector(${JSON.stringify(sel)}); if (!e) return null; e.scrollIntoView({block:'center',behavior:'instant'}); const r = e.getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top + r.height / 2 }; })()`); if (!q) return false; await sleep(200); await b.tapAt(q.x, q.y); return true; };
  const type = async (sel, text) => { await b.ev(`(() => { const e = document.querySelector(${JSON.stringify(sel)}); e.focus(); e.value = ''; return true; })()`); await b.send('Input.insertText', { text }); };
  try {
    await b.go(URLS[L]); R.patched = b.patched;
    if (!(await b.until("!!document.querySelector('.nlsr .nlsr-steps li') && !!document.querySelector('.nlsr-h')", 40000))) throw new Error('showroom did not mount');
    await sleep(2500);
    await b.ev("document.querySelector('.nlsr').scrollIntoView({block:'start',behavior:'instant'}); scrollBy(0,-70); true"); await sleep(600);
    // tower B, a floor on the tower (real taps)
    let r = await b.ev(RECT('.nlsr [data-tower="B"]')); await b.tapAt(r.x + r.w / 2, r.y + r.h / 2); await sleep(2200);
    await b.ev("document.querySelector('.nlsr-stage').scrollIntoView({block:'center',behavior:'instant'}); true"); await sleep(700);
    const st = await b.ev(RECT('.nlsr-stage')); let picked = false;
    for (const f of [0.5, 0.45, 0.55, 0.4, 0.6, 0.35]) { await b.tapAt(st.x + st.w / 2, st.y + st.h * f); await sleep(900); if (await b.ev("!document.querySelector('.nlsr-card').hidden")) { picked = true; break; } }
    if (!picked) throw new Error('no floor picked');
    await sleep(1000);
    R.checks.dira = await b.ev('location.hash');
    // step inside, a finish
    await tapSel('.nlsr-go');
    await b.until("!!document.querySelector('.nlck') && !document.querySelector('.nlck').hidden && !!document.querySelector('.nlck-grid')", 20000); await sleep(2000);
    await tapSel('.nlck-tile[data-open="inside"]'); await sleep(3500);
    await tapSel('.nlck [data-pano][aria-pressed="false"]'); await sleep(2500);
    // My selection, from the apartment screen
    await tapSel('.nlck [data-act="basket"]'); await sleep(1500);
    R.checks.basket = await b.ev(`(() => { const k = document.querySelector('.nlbk'); const o = k && k.querySelector('.nlbk__btn--offer'); return { open: k && !k.hidden, offerButton: o ? o.textContent : null, state: window.__nlBasket.state }; })()`);
    await b.ev("(() => { const o = document.querySelector('.nlbk__btn--offer'); if (o) o.scrollIntoView({block:'center',behavior:'instant'}); return true; })()"); await sleep(400);
    await b.shot(`${tag}-01-basket-offer-button`);
    const leadsBefore = b.posts.length;
    // Build me an offer
    if (!(await tapSel('.nlbk__btn--offer'))) throw new Error('no offer button in My selection');
    if (!(await b.until("!!document.querySelector('.nlkb') && !document.querySelector('.nlkb').hidden", 10000))) throw new Error('offer did not open');
    await sleep(900);
    await snap('step 1 summary'); await b.shot(`${tag}-02-step1`);
    await b.ev("document.querySelector('.nlkb__body').scrollTop = 1e5; true"); await sleep(300); await b.shot(`${tag}-02b-step1-bottom`);
    // a team member: the mortgage advisor
    await tapSel('.nlkb label.nlkb__chk:has([data-x="mortgage"])'); await sleep(300);
    R.checks.afterTick = await b.ev(STATE);
    await tapSel('.nlkb [data-kb="next"]'); await sleep(700);
    await snap('step 2 contact'); await b.shot(`${tag}-03-step2`);
    // send with nothing typed: an error, no request
    await tapSel('.nlkb [data-kb="send"]'); await sleep(500);
    const e1 = await snap('step 2 send empty -> error'); e1.postsAfterEmpty = b.posts.length - leadsBefore; await b.shot(`${tag}-04-step2-error`);
    await type('#nlkb-name', process.env.REAL ? 'בדיקת Claude, לא לטפל' : (L === 'he' ? 'בדיקה' : 'Test'));
    await type('#nlkb-phone', '0500000000');
    await tapSel('.nlkb [data-kb="send"]'); await sleep(500);
    const e2 = await snap('step 2 no consent -> error'); e2.postsAfterNoConsent = b.posts.length - leadsBefore;
    await tapSel('.nlkb label.nlkb__chk--consent'); await sleep(300);
    await b.ev("document.querySelector('.nlkb__body').scrollTop = 0; true"); await sleep(200);
    await b.shot(`${tag}-05-step2-filled`);
    await tapSel('.nlkb [data-kb="send"]');
    await b.until("!!document.querySelector('.nlkb__ref b') || !!document.querySelector('[data-kb=\"docretry\"]')", 12000); await sleep(700);
    if (opt.rfpFailFirst) {
      await snap('step 3 document failed (intercepted 500)'); await b.shot(`${tag}-06a-step3-doc-failed`);
      await tapSel('.nlkb [data-kb="docretry"]'); await b.until("!!document.querySelector('.nlkb__ref b')", 12000); await sleep(600);
    }
    await snap('step 3 confirmation'); await b.shot(`${tag}-06-step3`);
    await b.ev("document.querySelector('.nlkb__body').scrollTop = 1e5; true"); await sleep(300); await b.shot(`${tag}-06b-step3-bottom`);
    // back to the apartment, then My selection > Build me an offer again: the confirmation, never a second lead
    await tapSel('.nlkb [data-kb="home"]'); await sleep(900);
    R.checks.afterHome = { closed: await b.ev("document.querySelector('.nlkb').hidden"), htmlClass: await b.ev("document.documentElement.classList.contains('nlkb-open')"), showroomTop: Math.round(await b.ev("document.getElementById('nlsr').getBoundingClientRect().top")) };
    await b.shot(`${tag}-07-back-to-apartment`);
    await b.ev('window.__nlBasket.open(); true'); await sleep(700); await tapSel('.nlbk__btn--offer'); await sleep(1200);
    R.checks.reopen = { state: await b.ev(STATE), leadPosts: b.posts.filter((p) => p.kind === 'lead').length };
    await b.key('Escape', 27); await sleep(400);
    R.checks.escClosed = await b.ev("document.querySelector('.nlkb').hidden");
    // the payload
    const lead = b.posts.filter((p) => p.kind === 'lead'), rfp = b.posts.filter((p) => p.kind === 'rfp');
    const lb = lead[0] ? JSON.parse(lead[0].body) : null, msg = lb ? JSON.parse(lb.message) : null, rb = rfp.length ? JSON.parse(rfp[rfp.length - 1].body) : null;
    const m = /#dira=([ABC]\d+-\d+)/.exec(R.checks.dira || ''), style = (R.checks.basket.state || {}).style;
    R.payload = { leadCount: lead.length, rfpCount: rfp.length, rfpAnswers: rfp.map((p) => p.answered), lead: lb, leadMessage: msg, rfp: rb };
    R.checks.payload = {
      leadOnce: lead.length === 1,
      source: lb && lb.source === 'rfp-v1', kind: msg && msg.kind === 'rfp-v1',
      project: msg && msg.project === 'hamedina' && rb && rb.project === 'hamedina',
      unit: !!(m && msg && msg.unit === m[1] && rb && rb.unit === m[1]), unitId: msg && msg.unit, dira: m && m[1],
      finish: rb && rb.finish === (style && style !== 'bare' ? style : 'std'), finishSent: rb && rb.finish, basketStyle: style,
      extras: rb && Array.isArray(rb.extras) && rb.extras.includes('mortgage'), extrasSent: rb && rb.extras,
      lang: msg && msg.lang === L && rb && rb.lang === L, leadId: rb && rb.lead_id === FAKE.lead.lead_id, consent: lb && lb.consent === true && !!lb.consent_text,
      noRoomsSqmPrice: msg && msg.rooms === '' && msg.sqm === '' && !('price' in msg),
    };
    const s3 = R.steps.find((s) => s.name === 'step 3 confirmation');
    R.checks.confirmation = { ref: s3 && s3.state.ref === FAKE.rfp.ref, doc: s3 && s3.state.doc === FAKE.rfp.url };
  } catch (x) { R.error = String(x && x.message || x); await b.shot(`${tag}-ERROR`).catch(() => {}); }
  R.errs = b.errs;
  R.failed = b.failed.filter((f) => f.url && !/nadlan\/v1\/(lead|rfp)/.test(f.url));
  R.intercepted = b.posts.map((p) => ({ kind: p.kind, method: p.method, answered: p.answered }));
  R.served = [...b.served];
  R.ok = !R.error && R.steps.length >= 5 && R.steps.every((s) => s.ok) && ['leadOnce', 'source', 'kind', 'project', 'unit', 'finish', 'extras', 'lang', 'leadId', 'consent', 'noRoomsSqmPrice'].every((k) => (R.checks.payload || {})[k] === true) && R.checks.confirmation.ref && R.checks.confirmation.doc && !R.errs.length && !R.failed.length;
  await b.close();
  return R;
}

// Rainbow: the engine's own buy flow (buyflow.js, untouched) with this release's basket.js and showroom-i18n.js served locally
async function rainbow(w, h, slug = 'rainbow-tel-aviv') {
  const b = await browser({ w, h, L: 'rb' }); const R = { page: slug, w, h, checks: {} };
  try {
    await b.go(`https://nad-lan.co.il/projects/${slug}/`); await sleep(6000);
    R.checks.engine = await b.ev("({ showroom: !!window.NADLAN_SHOWROOM, rfpButtons: document.querySelectorAll('[data-act=\"rfp\"]').length, basket: !!window.__nlBasket, buyflowJs: [...document.scripts].map((s) => s.src).filter((s) => /buyflow/.test(s)) })");
    // this release's basket.js on a non-Kikar page: the drawer opens, its actions are the same as before (no Kikar offer button)
    R.checks.basket = await b.ev("(() => { if (!window.__nlBasket) return 'no basket'; window.__nlBasket.open(); const k = document.querySelector('.nlbk'); const r = { open: !k.hidden, kikarOffer: !!k.querySelector('.nlbk__btn--offer'), actions: [...k.querySelectorAll('.nlbk__acts > *')].map((e) => e.className) }; window.__nlBasket.close(); return r; })()");
    if (R.checks.basket && R.checks.basket.open) { await b.ev("window.__nlBasket.open(); document.querySelector('.nlbk__acts').scrollIntoView({block:'center'}); true"); await sleep(500); await b.shot(`${slug}-${w}-00-basket`); await b.ev('window.__nlBasket.close(); true'); }
    if (window_has(R.checks.engine)) {
      // (setup) open the flow from the first unit's "build me an offer" button, as a buyer's tap does
      const id = await b.ev("(() => { const n = document.querySelector('[data-act=\"rfp\"]'); n.scrollIntoView({block:'center',behavior:'instant'}); n.click(); return n.dataset.id; })()"); await sleep(800);
      R.checks.opened = await b.ev("(() => { const e = document.getElementById('nlbuy'); return { open: !!e && e.classList.contains('is-open'), title: e && e.querySelector('h3') ? e.querySelector('h3').textContent : null, step: e && e.querySelector('.nlbuy__step') ? e.querySelector('.nlbuy__step').textContent : null }; })()");
      R.checks.unit = id;
      await b.shot(`rainbow-${w}-01-open`);
      await b.ev("document.querySelector('#nlbuy [data-buy=\"next\"]').click(); true"); await sleep(400);
      await b.ev("document.querySelector('#nlbuy [data-buy=\"extra\"][data-v=\"lawyer\"]').click(); true"); await sleep(300);
      await b.ev("document.querySelector('#nlbuy [data-buy=\"next\"]').click(); true"); await sleep(400);
      await b.ev("document.getElementById('nlbuy-name').value = 'בדיקה'; document.getElementById('nlbuy-phone').value = '0500000000'; true");
      await b.shot(`rainbow-${w}-02-contact`);
      await b.ev("document.getElementById('nlbuy-send').click(); true"); await sleep(6500);
      await b.shot(`rainbow-${w}-03-done`);
      R.checks.done = await b.ev("(() => { const e = document.getElementById('nlbuy'); const a = e.querySelector('.nlbuy__done a'); return { done: !!e.querySelector('.nlbuy__done'), doc: a ? a.getAttribute('href') : null }; })()");
      const lead = b.posts.filter((p) => p.kind === 'lead'), rfp = b.posts.filter((p) => p.kind === 'rfp');
      R.payload = { lead: lead.map((p) => JSON.parse(p.body)), rfp: rfp.map((p) => JSON.parse(p.body)) };
      const lb = R.payload.lead[0] || {}, msg = lb.message ? JSON.parse(lb.message) : {};
      R.checks.shape = { leadKeys: Object.keys(lb), messageKeys: Object.keys(msg), rfpKeys: Object.keys(R.payload.rfp[0] || {}), leadCount: lead.length, rfpCount: rfp.length };
    }
  } catch (x) { R.error = String(x && x.message || x); }
  R.errs = b.errs; R.failed = b.failed.filter((f) => f.url && !/nadlan\/v1\/(lead|rfp)/.test(f.url)); R.served = [...b.served]; R.intercepted = b.posts.map((p) => ({ kind: p.kind, method: p.method, answered: p.answered }));
  await b.close();
  return R;
}
function window_has(e) { return e && e.showroom && e.rfpButtons > 0; }

const report = { started: new Date().toISOString(), runs: [] };
if (MODE === 'rainbow' || MODE === 'all') {
  for (const slug of ['rainbow-tel-aviv', 'duo-tel-aviv']) for (const [w, h] of (process.env.W1 ? [[390, 844]] : [[390, 844], [1440, 900]])) { const r = await rainbow(w, h, slug); report.runs.push(r); console.log(slug, w, JSON.stringify(r.checks.engine), JSON.stringify(r.checks.basket), JSON.stringify(r.checks.shape || {}), r.error || '', 'errs', r.errs.length, 'failed', r.failed.length, 'served', r.served.join(',')); }
}
if (MODE !== 'rainbow') {
  for (const L of MODE === 'all' ? ['he', 'en', 'fr'] : [MODE]) for (const [w, h] of (process.env.W1 ? [[390, 844]] : [[390, 844], [1440, 900]])) {
    const r = await kikar(L, w, h, { rfpFailFirst: L === 'he' && w === 390 ? 1 : 0 }); report.runs.push(r);
    console.log(L, w, 'ok', r.ok, r.error || '', 'steps', r.steps.map((s) => (s.ok ? '+' : '-') + s.pulses.n).join(' '), 'errs', (r.errs || []).length, 'failed', (r.failed || []).length, 'payload', JSON.stringify(r.checks.payload || {}));
  }
}
report.finished = new Date().toISOString();
await fs.writeFile(path.join(OUT, `result-${MODE}.json`), JSON.stringify(report, null, 1));
console.log('written', path.join(OUT, `result-${MODE}.json`));
