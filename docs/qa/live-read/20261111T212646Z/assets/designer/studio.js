// NadLan designer studio (HAD-701, HAD-708): the plan chooser every page puts above the designer.
//
//   import { mountStudio } from '.../assets/designer/studio.js';
//   const st = await mountStudio(host, pickEl, { plans: [{ k, url, label }], planUrl, mk, lang, version, project, helpUrl });
//   st.designer   the designer on screen (null while the visitor is drawing a plan)   st.current   a plan key, 'mine' or 'pm'
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
  const st = {
    get designer() { return cur && cur !== 'pm' ? inst : null; },
    get current() { return cur; },
    designKept: false,
    openMine: (edit) => go(() => openMine(!!edit)),
    openPlan: (k) => { const x = plans.find((p) => p.k === k); return x ? go(() => openPlan(x)) : Promise.resolve(false); },
  };
  const shown = () => (cur === 'pm' ? 'mine' : cur);
  const paint = () => { if (pick) pick.querySelectorAll('button[data-k]').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.k === shown()))); };
  const drop = () => { try { if (inst && inst.destroy) inst.destroy(); } catch (e) { /* already gone */ } inst = null; };
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
    drop(); cur = x.k; last = x; paint();
    inst = await mount(host, o);
    remember(x.k); tell('plan');
    return true;
  }
  async function showMine(plan) { // the designer on the visitor's own plan, with the way back into the drawing
    const o = cfg.mk ? cfg.mk(plan, null, { k: 'mine', mine: true }) : { plan, lang: cfg.lang, version: cfg.version };
    o.onEditPlan = () => go(() => openMine(true));
    drop(); cur = 'mine'; paint();
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

  // where to open: a shared design's own plan, else what this visitor chose last time, else the page's default
  const want = cfg.design ? null : cfg.start || recall();
  const dflt = plans.find((x) => x.k === base(cfg.planUrl)) || plans[0] || null;
  let ok = false;
  if (want === 'mine' && withMine) ok = await go(() => openMine(false));
  if (!ok) { const x = plans.find((p) => p.k === want) || dflt; if (x) ok = await go(() => openPlan(x, cfg.design)); }
  if (!ok && dflt) ok = await go(() => openPlan(dflt));
  return ok ? st : null;
}
