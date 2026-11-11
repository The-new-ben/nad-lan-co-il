// NadLan designer studio (HAD-701, HAD-708): the plan chooser every page puts above the designer.
//
//   import { mountStudio } from '.../assets/designer/studio.js';
//   const st = await mountStudio(host, pickEl, { plans: [{ k, url, label }], planUrl, mk, lang, version, project, helpUrl });
//   st.designer   the designer on screen (null while the visitor is drawing a plan)   st.current   a plan key, 'mine', 'pm' or 'call'
//   cfg.rest      the designer's REST base (/wp-json/nadlan/v1/designer/): with it every designer gets the "video call" button
//                 (HAD-706, call.js on LiveKit); a page opened with ?room=<id> shows the join sheet and receives the apartment
//                 from the people in the call. cfg.call === false turns the call off.
//
// Three sources of a plan, one row of buttons: the visitor's OWN apartment ("my plan", made in planmaker.js and kept in this
// browser only), a project's published plans, and the example apartments. cfg.mk(plan, url, choice) returns the designer's
// options, so each page keeps its own title, labels and send button. The planmaker is requested only when it is asked for.
import { mount } from './designer.js';

const S = {
  he: { mine: 'התוכנית שלי', group: 'על איזו דירה מעצבים', plan: 'דירה לדוגמה',
    scanTitle: 'למדוד במצלמה', scanSub: 'מסתובבים בדירה עם הטלפון ומסמנים את הפינות. התוכנית נבנית במידות אמיתיות', scanBtn: 'מדידה במצלמה' },
  en: { mine: 'My plan', group: 'Which apartment to design', plan: 'Example apartment',
    scanTitle: 'Measure with the camera', scanSub: 'Walk through the apartment with the phone and mark the corners. The plan is built in real sizes', scanBtn: 'Measure with the camera' },
};
const base = (u) => String(u || '').split('?')[0];

export async function mountStudio(host, pick, cfg = {}) {
  const T = S[cfg.lang] || S.he, KEY = 'nl-dsg-plan' + (cfg.scope ? ':' + cfg.scope : '');
  const withMine = cfg.mine !== false;
  // measuring with the camera (roomscan.js) is offered inside "my plan" only where the browser can do it, and only when the
  // page opened it for everyone (cfg.scan) or this visitor turned the trial switch on (?scan=on, kept in this browser)
  const scanOn = (() => {
    let on = cfg.scan === true;
    try {
      const q = new URLSearchParams(location.search).get('scan');
      if (q === 'on') localStorage.setItem('nl-dsg-scan', '1');
      if (q === 'off') localStorage.removeItem('nl-dsg-scan');
      on = on || localStorage.getItem('nl-dsg-scan') === '1';
    } catch (e) { /* storage blocked: only the page's own setting counts */ }
    return on;
  })();
  let scanMod = null; // the module once it is known that this browser can measure; false when it cannot
  let plans = (Array.isArray(cfg.plans) ? cfg.plans : []).filter((x) => x && x.url).map((x) => ({ ...x, k: x.k || base(x.url) }));
  if (!plans.length && cfg.planUrl) plans = [{ k: base(cfg.planUrl), url: cfg.planUrl, label: cfg.planLabel || T.plan }];
  const getPlan = (u) => fetch(u).then((r) => (r.ok ? r.json() : null)).catch(() => null);
  const recall = () => { try { return localStorage.getItem(KEY); } catch (e) { return null; } };
  const remember = (v) => { try { localStorage.setItem(KEY, v); } catch (e) { /* storage blocked: the choice lasts for this visit */ } };

  let inst = null, cur = null, busy = false, pm = null, last = null, first = true;
  let active = null, curPlan = null, curMeta = {}; // the video call on screen, and the apartment it shows to a newcomer
  const st = {
    get designer() { return cur && cur !== 'pm' ? inst : null; },
    get current() { return cur; },
    get call() { return active ? active.call : null; },
    get callRoom() { return active && active.tr ? active.tr.room : null; }, // the LiveKit room (a check reads its state)
    designKept: false,
    openMine: (edit) => go(() => openMine(!!edit)),
    openPlan: (k) => { const x = plans.find((p) => p.k === k); return x ? go(() => openPlan(x)) : Promise.resolve(false); },
  };
  const shown = () => (cur === 'pm' ? 'mine' : cur);
  const paint = () => { if (pick) pick.querySelectorAll('button[data-k]').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.k === shown()))); };
  const drop = () => {
    if (active) { const a = active; active = null; try { a.call.leave(); } catch (e) { /* already gone */ } } // another apartment ends the call
    try { if (inst && inst.destroy) inst.destroy(); } catch (e) { /* already gone */ } inst = null;
  };

  /* ---------------- the video call (HAD-706): LiveKit through call.js, rooms and tokens from the site ---------------- */
  const callOn = cfg.call !== false && !!cfg.rest;
  const ROOM_RE = /^[a-z2-7]{12}$/;
  const hook = () => (typeof window !== 'undefined' && window.__nlCallHook) || null; // a local check may answer the two requests itself
  const ident = (room, v) => { try { const k = 'nl-call-id:' + room; if (v) sessionStorage.setItem(k, v); return sessionStorage.getItem(k) || ''; } catch (e) { return ''; } };
  async function post(path, body) {
    let r = null, j = null;
    try { r = await fetch(cfg.rest + path, { method: 'POST', credentials: 'omit', cache: 'no-store', headers: { 'Content-Type': 'application/json', 'X-NL-Designer': '1' }, body: JSON.stringify(body) }); } catch (e) { r = null; }
    if (r) { try { j = await r.json(); } catch (e) { j = null; } }
    if (!r || !r.ok) { const e = new Error('call'); const c = (j && j.error) || (r && r.status === 429 ? 'rate' : 'fail'); e.code = c === 'room' ? 'gone' : ['off', 'full', 'gone', 'rate'].includes(c) ? c : 'fail'; throw e; }
    return j;
  }
  const openRoom = (name) => (hook() && hook().room ? hook().room({ name }) : post('call', { page: location.pathname, name }));
  async function getToken(room, name, role) {
    const t = hook() && hook().token ? await hook().token({ room, name, role }) : await post('call/token', { room, name, role, identity: ident(room) || undefined });
    if (!t || !t.url || !t.token || !t.identity) { const e = new Error('call'); e.code = 'fail'; throw e; }
    ident(room, t.identity);
    return t;
  }
  const callBox = () => { const sh = host.shadowRoot || host.attachShadow({ mode: 'open' }), b = document.createElement('div'); b.className = 'ndc-host'; sh.appendChild(b); return b; };
  async function enterCall(d, tok, room, name, role, box, tr) {
    const C = await import('./call.js');
    tr = tr || C.livekitTransport({ url: tok.url, token: tok.token });
    const call = await C.joinCall(d, {
      container: box, transport: tr, room, identity: tok.identity, name, role, lang: cfg.lang || 'he', mode: 'open',
      share: () => ({ plan: curPlan, title: curMeta.title || '', unitLabel: curMeta.unitLabel || '', mine: !!curMeta.mine }),
      onLeave: () => { if (active && active.call === call) active = null; box.remove(); if (cfg.onCall) { try { cfg.onCall('left', st); } catch (e) { /* the page's own */ } } },
    });
    active = { call, room, tr };
    if (cfg.onCall) { try { cfg.onCall('joined', st); } catch (e) { /* the page's own */ } }
    return call;
  }
  function startCall(d) { // the designer's "video call" button
    if (active) { try { active.call.openPanel('invite'); } catch (e) { /* none */ } return; }
    if (!callOn || d !== inst) return;
    const box = callBox();
    import('./call.js').then((C) => C.callSheet(box, {
      mode: 'start', lang: cfg.lang,
      onClose: () => box.remove(),
      onGo: async (name, sheet) => {
        const t0 = performance.now();
        const { room } = await openRoom(name);
        const t1 = performance.now();
        if (!ROOM_RE.test(String(room || ''))) { const e = new Error('call'); e.code = 'fail'; throw e; }
        const tok = await getToken(room, name, 'host');
        const t2 = performance.now();
        await enterCall(d, tok, room, name, 'host', box);
        st.callTimes = { room_ms: Math.round(t1 - t0), token_ms: Math.round(t2 - t1), connect_and_media_ms: Math.round(performance.now() - t2) };
        sheet.close();
        st.callStartMs = Math.round(performance.now() - t0);
      },
    })).catch(() => box.remove());
  }
  function joinFromLink(room) { // opened with ?room=: the sheet first, then the apartment of the people in the call
    const box = callBox();
    return import('./call.js').then((C) => C.callSheet(box, {
      mode: 'join', lang: cfg.lang,
      onClose: () => { box.remove(); openDefault(); },
      onGo: async (name, sheet) => {
        const t0 = performance.now();
        const tok = await getToken(room, name, 'guest');
        const tr = C.livekitTransport({ url: tok.url, token: tok.token });
        try {
          await tr.connect();
          sheet.busy(true, sheet.T.waitPlan);
          const got = await C.receivePlan(tr, { onStatus: (s) => sheet.msg(sheet.T[s]) });
          const o = cfg.mk ? cfg.mk(got.plan, null, { k: 'call', call: true, mine: got.mine }) : { plan: got.plan, lang: cfg.lang, version: cfg.version };
          if (got.title) o.title = got.title;
          if (got.unitLabel) o.unitLabel = got.unitLabel;
          if (got.design && got.design.geometry_revision === got.plan.geometry_revision) o.design = got.design;
          o.onCall = (dd) => startCall(dd);
          drop(); cur = 'call'; paint();
          curPlan = got.plan; curMeta = { title: o.title, unitLabel: o.unitLabel, mine: got.mine };
          inst = await mount(host, o); // the sheet goes with the old content of the frame
          const call = await enterCall(inst, tok, room, name, 'guest', callBox(), tr);
          call.stats.planGot = { ms: got.ms, bytes: JSON.stringify(got.plan).length + JSON.stringify(got.design || {}).length, items: (o.design && o.design.items || []).length };
          st.callStartMs = Math.round(performance.now() - t0);
          tell('call');
        } catch (e) { try { await tr.disconnect(); } catch (x) { /* none */ } throw e; }
      },
    }));
  }
  const tell = (kind) => { if (cfg.onChange) { try { cfg.onChange(kind, st, first); } catch (e) { /* the page's own handler */ } } first = false; };
  async function go(fn) {
    if (busy) return false;
    busy = true;
    let ok = false;
    try { ok = (await fn()) !== false; } catch (e) { if (window.console) console.error('[nadlan designer]', e); }
    busy = false;
    return ok;
  }

  async function openPlan(x, design) {
    const pl = await getPlan(x.url);
    if (!pl) return false;
    const o = cfg.mk ? cfg.mk(pl, x.url, x) : { plan: pl, lang: cfg.lang, version: cfg.version };
    st.designKept = !!(design && design.geometry_revision === (o.plan || pl).geometry_revision);
    if (st.designKept) o.design = design;
    if (callOn) o.onCall = (d) => startCall(d);
    drop(); cur = x.k; last = x; paint();
    curPlan = o.plan || pl; curMeta = { title: o.title, unitLabel: o.unitLabel, mine: false };
    inst = await mount(host, o);
    remember(x.k); tell('plan');
    return true;
  }
  async function showMine(plan) { // the designer on the visitor's own plan, with the way back into the drawing
    const o = cfg.mk ? cfg.mk(plan, null, { k: 'mine', mine: true }) : { plan, lang: cfg.lang, version: cfg.version };
    o.onEditPlan = () => go(() => openMine(true));
    if (callOn) o.onCall = (d) => startCall(d);
    drop(); cur = 'mine'; paint();
    curPlan = o.plan || plan; curMeta = { title: o.title, unitLabel: o.unitLabel, mine: true };
    try { inst = await mount(host, o); } catch (e) { // a plan kept in this browser that the engine cannot open any more: back to a plan that works
      inst = null; cur = null; remember('');
      return last ? openPlan(last) : plans[0] ? openPlan(plans[0]) : false;
    }
    remember('mine'); tell('mine');
    return true;
  }
  async function scanWays() {
    if (!scanOn) return [];
    if (scanMod === null) {
      try { const rs = await import('./roomscan.js'); scanMod = (await rs.scanSupported()).ok ? rs : false; } catch (e) { scanMod = false; }
    }
    return scanMod ? [{ title: T.scanTitle, sub: T.scanSub, btn: T.scanBtn, run: () => go(() => openScan()) }] : [];
  }
  async function openScan() { // the camera fills the frame; what it measured comes back as a draft the visitor checks in the drawing
    drop(); cur = 'pm'; paint();
    inst = await scanMod.mountRoomScan(host, {
      lang: cfg.lang || 'he', version: cfg.version,
      onDone: (res) => go(() => openMine(true, res && res.draft ? res.draft : null)),
      onCancel: () => go(() => openMine(true)),
    });
    return true;
  }
  async function openMine(edit, draft) {
    if (!withMine) return false;
    pm = pm || (await import('./planmaker.js'));
    const own = edit ? null : pm.loadMyPlan();
    if (own) return showMine(own);
    const extraWays = await scanWays();
    drop(); cur = 'pm'; paint(); tell('maker');
    inst = await pm.mountPlanMaker(host, {
      lang: cfg.lang || 'he', version: cfg.version, project: cfg.project || null, helpUrl: cfg.helpUrl || '', extraWays, draft: draft || undefined,
      onDone: (plan) => go(() => showMine(plan)),
      onCancel: () => go(() => (last ? openPlan(last) : plans[0] ? openPlan(plans[0]) : false)),
    });
    return true;
  }

  if (pick) {
    pick.textContent = '';
    pick.setAttribute('aria-label', T.group);
    const add = (k, label, fn, cls) => {
      const b = document.createElement('button');
      b.type = 'button'; b.dataset.k = k; b.textContent = label; b.setAttribute('aria-pressed', 'false');
      if (cls) b.className = cls;
      b.addEventListener('click', () => { if (k !== shown()) go(fn); });
      pick.appendChild(b);
    };
    if (withMine) add('mine', cfg.mineLabel || T.mine, () => openMine(false), 'is-mine');
    if (plans.length > 1 || withMine) plans.forEach((x) => add(x.k, x.label || x.k, () => openPlan(x)));
    pick.hidden = !pick.children.length;
  }

  if (typeof window !== 'undefined' && window.__nlCallHook) window.__nlStudio = st; // a local check reads the studio
  // where to open: a shared design's own plan, else what this visitor chose last time, else the page's default
  const want = cfg.design ? null : cfg.start || recall();
  const dflt = plans.find((x) => x.k === base(cfg.planUrl)) || plans[0] || null;
  async function openDefault() {
    let ok = false;
    if (want === 'mine' && withMine) ok = await go(() => openMine(false));
    if (!ok) { const x = plans.find((p) => p.k === want) || dflt; if (x) ok = await go(() => openPlan(x, cfg.design)); }
    if (!ok && dflt) ok = await go(() => openPlan(dflt));
    return ok;
  }
  // an invite link (?room=): the join sheet at once; the apartment arrives from the people in the call, not from this site
  let roomQ = '';
  try { roomQ = String(new URLSearchParams(location.search).get('room') || '').toLowerCase(); } catch (e) { roomQ = ''; }
  if (callOn && ROOM_RE.test(roomQ)) {
    try { await joinFromLink(roomQ); return st; } catch (e) { /* the call module did not load: the designer opens as always */ }
  }
  return (await openDefault()) ? st : null;
}
