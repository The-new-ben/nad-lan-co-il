// NadLan apartment designer: the module every page mounts (HAD-701, architecture in docs/architecture/apartment-designer/).
//
//   import { mount } from '.../assets/designer/designer.js';
//   const d = await mount(host, { planUrl, lang: 'he', title, unitLabel, onSend, onCall, onClose });
//   d.getDesign(); d.getView(); d.setView(v); d.on(fn); d.destroy();
//
// The host decides the size (a full-screen sheet on a project page, the centre block of the design page).
// Everything is drawn inside a shadow root, so the site's CSS cannot reach it and it cannot leak out.
// The plan paints first; the 3D library is requested only after it. three.js comes from the page's import map.
import { createStore, emptyDesign, quantities, WALL_KINDS } from './core.js';
import { mountPlan } from './plan.js';
import * as catalog from './catalog.js';
import { strings } from './strings.js';

const BASE = new URL('.', import.meta.url).href;
const FONTS = 'https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans+Hebrew:wght@400;600;700&display=swap';
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

function ensureFonts() { // a font must be declared in the document itself; a shadow root cannot load one
  if (document.querySelector('link[data-nd-fonts]')) return;
  const l = document.createElement('link'); l.rel = 'stylesheet'; l.href = FONTS; l.setAttribute('data-nd-fonts', ''); document.head.appendChild(l);
}

export async function mount(host, opts = {}) {
  const T = strings(opts.lang || 'he'), t0 = performance.now();
  const apt = opts.plan || (await (await fetch(opts.planUrl || BASE + 'plans/example-4r.json')).json());
  const design = opts.design || emptyDesign(apt);
  if (!opts.design) design.items = (apt.starter || catalog.STARTER).map((i) => ({ ...i }));
  const store = createStore(apt, design);
  ensureFonts();

  const shadow = host.shadowRoot || host.attachShadow({ mode: 'open' });
  shadow.textContent = '';
  const css = document.createElement('link'); css.rel = 'stylesheet'; css.href = BASE + 'designer.css?v=' + (opts.version || '1');
  const root = document.createElement('div'); root.className = 'nd'; root.dir = T.dir; root.lang = opts.lang || 'he';
  root.innerHTML =
    '<header><div><h2>' + esc(opts.title || T.title) + '</h2><p data-nd="sub"></p></div>' +
    '<button class="hb" data-nd="undo" aria-label="' + T.undo + '" title="' + T.undo + '" disabled><svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M9 6l-6 6 6 6M3 12h12a6 6 0 0 1 6 6"/></svg></button>' +
    '<button class="hb" data-nd="redo" aria-label="' + T.redo + '" title="' + T.redo + '" disabled><svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M15 6l6 6-6 6M21 12H9a6 6 0 0 0-6 6"/></svg></button>' +
    (opts.onClose ? '<button class="hb" data-nd="close" aria-label="' + T.close + '" title="' + T.close + '"><svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M6 6l12 12M18 6L6 18"/></svg></button>' : '') + '</header>' +
    '<section class="space" data-nd="space" aria-label="' + T.space + '"><div class="chips" role="group" aria-label="' + T.viewGroup + '">' +
    '<button data-nd="m-doll" aria-pressed="true">' + T.viewTop + '</button><button data-nd="m-walk" aria-pressed="false">' + T.viewWalk + '</button></div>' +
    '<p class="note">' + esc(opts.note || T.note) + '</p></section>' +
    '<div class="bar" data-nd="bar" role="separator" aria-label="' + T.split + '" tabindex="0"><i></i></div>' +
    '<section class="plan" data-nd="plan" aria-label="' + T.plan + '"><p class="hint" data-nd="hint"></p></section>' +
    '<nav aria-label="' + T.tools + '"><button data-sheet="items" aria-expanded="false">' + T.tItems + '</button><button data-sheet="floor" aria-expanded="false">' + T.tFloor + '</button>' +
    '<button data-sheet="boq" aria-expanded="false">' + T.tBoq + '</button>' +
    (opts.onCall ? '<button data-nd="call">' + T.tCall + '</button>' : '') + (opts.onSend ? '<button class="go" data-nd="send">' + T.tSend + '</button>' : '') + '</nav>' +
    '<div class="sheet" data-nd="sheet" hidden></div>' +
    '<div class="selbar" data-nd="selbar" hidden><b data-nd="selname"></b><button data-nd="rot">' + T.rotate + '</button><button data-nd="del">' + T.remove + '</button></div>' +
    '<div class="toast" data-nd="toast" role="alert" hidden></div>';
  shadow.append(css, root);
  const $ = (k) => root.querySelector('[data-nd="' + k + '"]');
  await new Promise((r) => { if (css.sheet) r(); else { css.addEventListener('load', r, { once: true }); css.addEventListener('error', r, { once: true }); } });

  let sel = null, sheet = null, space = null, toastT = 0, alive = true;
  const subs = new Set(), timings = {};
  const toast = (msg, kind) => { $('toast').textContent = msg; $('toast').className = 'toast' + (kind === 'stop' ? ' stop' : ''); $('toast').hidden = false; clearTimeout(toastT); toastT = setTimeout(() => ($('toast').hidden = true), 3200); };
  const select = (s) => { sel = s; plan.setSelection(s); if (space) space.setSelection(s); paintSel(); if (s && s.type === 'room' && sheet !== 'floor') open('floor'); else if (sheet) open(sheet, true); };
  const plan = mountPlan($('plan'), store, catalog, { select, blocked: (r) => toast(r.reason, 'stop'), camMove: (p) => space && space.walkTo(p) });
  timings.plan_ms = performance.now() - t0;

  function paintSel() {
    const it = sel && sel.type === 'item' && store.item(sel.id);
    $('selbar').hidden = !it;
    if (it) $('selname').textContent = catalog.ITEMS[it.sku].he;
    $('hint').textContent = sel && sel.type === 'wall' ? WALL_KINDS[store.derived.wallBy[sel.id].kind].he + (store.slides(sel.id) ? T.wallFree : T.wallFixed) : space && space.mode === 'walk' ? T.hintWalk : T.hintDrag;
  }
  function head() {
    const q = quantities(store);
    $('sub').textContent = (opts.unitLabel ? opts.unitLabel + ' · ' : apt.source && apt.source.label_he ? apt.source.label_he + ' · ' : '') + T.sub(apt.unit.rooms, q.net.toFixed(1), q.balcony ? q.balcony.toFixed(1) : '');
    $('undo').disabled = !store.canUndo(); $('redo').disabled = !store.canRedo();
  }
  function open(name, keep) {
    if (sheet === name && !keep) name = null;
    sheet = name;
    root.querySelectorAll('nav button[data-sheet]').forEach((b) => b.setAttribute('aria-expanded', b.dataset.sheet === name));
    const el = $('sheet'); el.hidden = !name; el.textContent = '';
    if (!name) return;
    const h = document.createElement('h3'); el.appendChild(h);
    const dv = store.derived;
    if (name === 'items') {
      h.textContent = T.itemsHead;
      const g = document.createElement('div'); g.className = 'grid'; el.appendChild(g);
      for (const sku in catalog.ITEMS) {
        const c = catalog.ITEMS[sku], b = document.createElement('button'); b.className = 'opt';
        b.innerHTML = '<span>' + esc(c.he) + '</span><small><span class="mono">' + c.w + '×' + c.d + '</span> ' + T.cm + '</small>';
        b.onclick = () => {
          const id = 'i' + Date.now().toString(36), f = (sel && sel.type === 'room' && dv.faceBy[sel.id]) || dv.faceBy.living || dv.faces[0];
          const r = store.apply({ op: 'item.add', item: { id, sku, x: Math.round((f.bb.x0 + f.bb.x1) / 2), y: Math.round((f.bb.y0 + f.bb.y1) / 2), rot: 0, status: 'decor' } });
          if (r.ok) { open(null); select({ type: 'item', id }); } else toast(r.reason, 'stop');
        };
        g.appendChild(b);
      }
    }
    if (name === 'floor') {
      const room = sel && sel.type === 'room' ? dv.faceBy[sel.id] : null;
      h.textContent = room ? T.floorHead + ': ' + room.room.name_he + ' · ' + room.net.toFixed(1) + ' ' + T.sqm : T.floorPick;
      if (!room) return;
      const g = document.createElement('div'); g.className = 'grid'; el.appendChild(g);
      for (const key of catalog.FLOOR_CHOICES) {
        const f = catalog.FINISHES[key], b = document.createElement('button'); b.className = 'opt'; b.setAttribute('aria-pressed', store.floorOf(room.id) === key);
        b.innerHTML = '<span>' + esc(f.he) + '</span><small><span class="tag ' + f.status + '">' + (f.status === 'base' ? T.base : T.upgrade) + '</span></small>';
        b.onclick = () => store.apply({ op: 'finish.set', key: 'floor:' + room.id, value: key === room.room.floor ? null : key });
        g.appendChild(b);
      }
    }
    if (name === 'boq') {
      const q = quantities(store);
      h.textContent = T.boqHead;
      let html = '<table><thead><tr><th>' + T.boqFloor + '</th><th class="n">' + T.boqArea + '</th></tr></thead><tbody>';
      for (const k in q.floors) html += '<tr><td>' + esc(catalog.FINISHES[k].he) + ' <span class="tag ' + catalog.FINISHES[k].status + '">' + (catalog.FINISHES[k].status === 'base' ? T.base : T.upgrade) + '</span></td><td class="n"><span class="mono">' + q.floors[k].toFixed(1) + '</span> ' + T.sqm + '</td></tr>';
      html += '</tbody></table><table style="margin-top:10px"><thead><tr><th>' + T.boqRoom + '</th><th class="n">' + T.boqSize + '</th><th class="n">' + T.boqArea + '</th></tr></thead><tbody>';
      for (const r of q.rooms) html += '<tr><td>' + esc(r.name) + '</td><td class="n mono">' + r.w + '×' + r.d + '</td><td class="n mono">' + r.net.toFixed(1) + '</td></tr>';
      html += '</tbody></table><table style="margin-top:10px"><thead><tr><th>' + T.boqItems + '</th><th class="n">' + T.boqCount + '</th></tr></thead><tbody>';
      for (const k in q.items) html += '<tr><td>' + esc(catalog.ITEMS[k].he) + '</td><td class="n mono">' + q.items[k] + '</td></tr>';
      el.insertAdjacentHTML('beforeend', html + '</tbody></table><p class="fine">' + T.boqFine + '</p>');
    }
  }
  const setMode = (m) => { if (!space) return; space.setMode(m); $('m-doll').setAttribute('aria-pressed', m === 'doll'); $('m-walk').setAttribute('aria-pressed', m === 'walk'); paintSel(); };

  root.querySelectorAll('nav button[data-sheet]').forEach((b) => (b.onclick = () => open(b.dataset.sheet)));
  $('undo').onclick = () => store.undo(); $('redo').onclick = () => store.redo();
  $('rot').onclick = () => { const it = sel && store.item(sel.id); if (it) store.apply({ op: 'item.rot', id: it.id, rot: it.rot + 90 }); };
  $('del').onclick = () => { if (sel) { store.apply({ op: 'item.remove', id: sel.id }); select(null); } };
  $('m-doll').onclick = () => setMode('doll'); $('m-walk').onclick = () => setMode('walk');
  if (opts.onClose) $('close').onclick = () => opts.onClose(api);
  if (opts.onCall) $('call').onclick = () => opts.onCall(api);
  if (opts.onSend) $('send').onclick = () => opts.onSend(api);
  store.on((e) => { if (e.type !== 'change') return; head(); if (sheet) open(sheet, true); subs.forEach((f) => f(e)); });

  // the divider between the two views: drag it, or use the arrow keys
  const wide = () => root.clientWidth >= 900;
  let barDrag = false, split = 42;
  const setSplit = (pct) => { split = Math.max(25, Math.min(75, pct)); if (wide()) root.style.gridTemplateColumns = 'minmax(0,' + split + 'fr) 14px minmax(0,' + (100 - split) + 'fr)'; else root.style.setProperty('--split', split + '%'); };
  $('bar').addEventListener('pointerdown', (ev) => { barDrag = true; try { $('bar').setPointerCapture(ev.pointerId); } catch (e) { /* synthetic pointer */ } });
  $('bar').addEventListener('pointermove', (ev) => { if (!barDrag) return; const r = root.getBoundingClientRect(); setSplit(wide() ? ((T.dir === 'rtl' ? r.right - ev.clientX : ev.clientX - r.left) / r.width) * 100 : ((ev.clientY - r.top - 60) / (r.height - 120)) * 100); });
  $('bar').addEventListener('pointerup', () => (barDrag = false));
  $('bar').addEventListener('keydown', (ev) => { if (ev.key === 'ArrowUp' || ev.key === 'ArrowRight') setSplit(split - 5); if (ev.key === 'ArrowDown' || ev.key === 'ArrowLeft') setSplit(split + 5); });

  const api = {
    store, plan, timings, version: 1,
    get space() { return space; },
    getDesign: () => JSON.parse(JSON.stringify(store.design)),
    quantities: () => quantities(store),
    getView: () => (space ? space.getView() : null),
    setView: (v) => space && space.setView(v),
    on: (f) => { subs.add(f); return () => subs.delete(f); },
    select, setMode, toast,
    ready3d: null,
    destroy() { alive = false; if (space && space.destroy) space.destroy(); shadow.textContent = ''; subs.clear(); },
  };
  head(); paintSel();

  // the plan is on screen; only now ask for the 3D library
  api.ready3d = import('./space.js').then(({ mountSpace }) => {
    if (!alive) return null;
    space = mountSpace($('space'), store, catalog, { select, camera: (v) => plan.setCamera(v), frame: (dt, rms) => { timings.last_change_ms = store.lastApplyMs + rms; } });
    timings.space_ms = performance.now() - t0;
    requestAnimationFrame(() => requestAnimationFrame(() => { timings.first_3d_frame_ms = performance.now() - t0; }));
    if (sel) space.setSelection(sel);
    return space;
  });
  return api;
}
