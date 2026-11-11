// NadLan apartment designer: the module every page mounts (HAD-701, architecture in docs/architecture/apartment-designer/).
//
//   import { mount } from '.../assets/designer/designer.js';
//   const d = await mount(host, { planUrl, lang: 'he', title, unitLabel, onSend, onCall, onClose });
//   d.getDesign(); d.getView(); d.setView(v); d.on(fn); d.destroy();
//
// The host decides the size (a full-screen sheet on a project page, the centre block of the design page).
// Everything is drawn inside a shadow root, so the site's CSS cannot reach it and it cannot leak out.
// The plan paints first; the 3D library is requested only after it. three.js comes from the page's import map.
import { createStore, emptyDesign, quantities, interior, WALL_KINDS, POINT_KINDS, SPACE_NAMES } from './core.js';
import { mountPlan, symbolSvg } from './plan.js';
import * as catalog from './catalog.js';
import { strings } from './strings.js';
import { estimate, itemRange, span, tidy } from './budget.js';

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
  const fresh = () => { const d = emptyDesign(apt); d.items = (apt.starter || catalog.STARTER).filter((i) => catalog.ITEMS[i.sku]).map((i) => ({ ...i })); return d; };
  // the design is kept in THIS browser only, per apartment layout, with no personal details: come back and it is still here
  const saveKey = opts.save === false ? null : 'nd-design:' + (apt.unit.project || '-') + ':' + (apt.unit.unit_id || apt.id) + ':' + apt.geometry_revision;
  let restored = false, design = opts.design || null;
  if (!design && saveKey) try {
    const s = JSON.parse(localStorage.getItem(saveKey) || 'null');
    if (s && s.schema === 'nadlan-unit-design' && s.v === 2 && s.geometry_revision === apt.geometry_revision && Array.isArray(s.items)) { s.items = s.items.filter((i) => catalog.ITEMS[i.sku]); design = s; restored = true; }
  } catch (e) { /* storage blocked or an unreadable draft: start fresh */ }
  let store;
  try { store = createStore(apt, design || fresh()); } catch (e) { restored = false; store = createStore(apt, fresh()); }
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
    '<section class="plan" data-nd="plan" aria-label="' + T.plan + '"><div class="ptools"><p class="hint" data-nd="hint"></p><button class="ptool" data-nd="part" aria-pressed="false">' + T.partNew + '</button></div></section>' +
    '<nav aria-label="' + T.tools + '"><button data-sheet="items" aria-expanded="false">' + T.tItems + '</button><button data-sheet="floor" aria-expanded="false">' + T.tFloor + '</button>' +
    '<button data-sheet="points" aria-expanded="false">' + T.tPoints + '</button>' +
    '<button data-sheet="boq" aria-expanded="false">' + T.tBoq + '</button>' +
    (opts.onCall ? '<button data-nd="call">' + T.tCall + '</button>' : '') + (opts.onSend ? '<button class="go" data-nd="send">' + T.tSend + '</button>' : '') + '</nav>' +
    '<div class="sheet" data-nd="sheet" hidden></div>' +
    '<div class="selbar" data-nd="selbar" hidden><b data-nd="selname"></b><button data-nd="rot">' + T.rotate + '</button><button data-nd="restore">' + T.restore + '</button><button data-nd="del">' + T.remove + '</button></div>' +
    '<div class="toast" data-nd="toast" role="alert" hidden></div>';
  shadow.append(css, root);
  const $ = (k) => root.querySelector('[data-nd="' + k + '"]');
  await new Promise((r) => { if (css.sheet) r(); else { css.addEventListener('load', r, { once: true }); css.addEventListener('error', r, { once: true }); } });

  let sel = null, sheet = null, space = null, toastT = 0, alive = true, prices = null, placing = null;
  const nf = new Intl.NumberFormat('he-IL');
  const money = (r) => (!r ? '' : r.hi == null ? nf.format(r.lo) + ' ' + T.shekel + T.andUp : nf.format(r.lo) + T.to + nf.format(r.hi) + ' ' + T.shekel);
  const subs = new Set(), timings = {};
  const why = (r) => (r && T.rules && T.rules[r.code]) || (r && r.reason) || ''; // a rule's sentence in the page language when it has one
  const toast = (msg, kind) => { $('toast').textContent = msg; $('toast').className = 'toast' + (kind === 'stop' ? ' stop' : ''); $('toast').hidden = false; clearTimeout(toastT); toastT = setTimeout(() => ($('toast').hidden = true), 3200); };
  const select = (s) => { sel = s; plan.setSelection(s); if (space) space.setSelection(s); paintSel(); if (s && s.type === 'room' && sheet !== 'floor') open('floor'); else if (sheet) open(sheet, true); };
  const modeDone = () => { placing = null; $('part').setAttribute('aria-pressed', 'false'); paintSel(); };
  const plan = mountPlan($('plan'), store, catalog, { T, select, blocked: (r) => toast(why(r), 'stop'), camMove: (p) => space && space.walkTo(p), modeDone });
  timings.plan_ms = performance.now() - t0;

  function paintSel() { // the dark bar and the hint line, for every kind of selection and for the two drawing modes
    const dv = store.derived, it = sel && sel.type === 'item' && store.item(sel.id), pt = sel && sel.type === 'point' && store.point(sel.id);
    const w = sel && sel.type === 'wall' && (dv.wallBy[sel.id] || dv.ghosts.find((g) => g.id === sel.id)), gone = !!w && store.isRemoved(w.id);
    const part = w && w.kind === 'partition';
    let name = '', bar = { rot: false, restore: false, del: false };
    if (it) { name = catalog.ITEMS[it.sku].he; bar = { rot: true, del: true }; }
    else if (pt) { name = T.pointName[pt.kind] + (pt.state !== 'base' ? ' · ' + T.pointState[pt.state] : ''); bar = { restore: pt.state === 'moved' || pt.state === 'removed', del: pt.state !== 'removed' }; }
    else if (part) { name = gone ? T.partGoneName : w.added ? T.partAddedName : T.partName; bar = { restore: gone, del: !gone }; }
    $('selbar').hidden = !(it || pt || part);
    $('selname').textContent = name;
    $('rot').hidden = !bar.rot; $('restore').hidden = !bar.restore; $('del').hidden = !bar.del;
    $('restore').textContent = part ? T.partRestore : T.restore; $('del').textContent = part ? T.partRemove : T.remove;
    const m = plan.mode;
    $('hint').textContent = m === 'place' ? (POINT_KINDS[placing].ceiling ? T.placeLight : T.placeWall(T.pointName[placing])) : m === 'part' ? T.partHint
      : w && !gone ? (w.added ? T.partAddedHint : WALL_KINDS[w.kind].he + (store.slides(w.id) ? T.wallFree : T.wallFixed)) : space && space.mode === 'walk' ? T.hintWalk : T.hintDrag;
    $('plan').classList.toggle('busy', !!m);
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
        const pr = tidy(itemRange(c, prices));
        b.innerHTML = '<span>' + esc(c.he) + '</span><small><span class="mono">' + c.w + '×' + c.d + '</span> ' + T.cm + '</small><small class="pr">' + (pr ? money(pr) : prices ? T.noPrice : '') + '</small>';
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
      h.textContent = room ? T.floorHead + ': ' + (room.room.fresh ? T.newSpace : room.room.name_he) + ' · ' + room.net.toFixed(1) + ' ' + T.sqm : T.floorPick;
      if (!room) return;
      if (room.room.fresh || room.room.design) { // a space a new partition made: the buyer says what it is, from a short list
        h.textContent = T.spaceHead + ' · ' + room.net.toFixed(1) + ' ' + T.sqm;
        const ng = document.createElement('div'); ng.className = 'grid names'; el.appendChild(ng);
        SPACE_NAMES.forEach((n, i) => {
          const b = document.createElement('button'); b.className = 'opt'; b.setAttribute('aria-pressed', !room.room.fresh && room.room.name_he === n.name_he); b.textContent = T.spaceNames[i][0];
          b.onclick = () => { const r = store.apply({ op: 'room.name', at: interior(room), name_he: n.name_he, type: n.type }); if (!r.ok) toast(why(r), 'stop'); };
          ng.appendChild(b);
        });
        const fh = document.createElement('h3'); fh.style.marginTop = '12px'; fh.textContent = T.floorHead; el.appendChild(fh);
      }
      const g = document.createElement('div'); g.className = 'grid'; el.appendChild(g);
      for (const key of catalog.FLOOR_CHOICES) {
        const f = catalog.FINISHES[key], b = document.createElement('button'); b.className = 'opt'; b.setAttribute('aria-pressed', store.floorOf(room.id) === key);
        const fp = f.status === 'base' ? null : tidy(span(prices && prices[f.price]));
        b.innerHTML = '<span>' + esc(f.he) + '</span><small><span class="tag ' + f.status + '">' + (f.status === 'base' ? T.base : T.upgrade) + '</span></small>' + (f.status === 'base' ? '' : '<small class="pr">' + (fp ? money(fp) + ' ' + esc(prices[f.price].unit_he) : prices ? T.noPrice : '') + '</small>');
        b.onclick = () => store.apply({ op: 'finish.set', key: 'floor:' + room.id, value: key === room.room.floor ? null : key });
        g.appendChild(b);
      }
    }
    if (name === 'points') {
      h.textContent = T.pointsHead;
      const g = document.createElement('div'); g.className = 'grid kinds'; el.appendChild(g);
      for (const kind of Object.keys(POINT_KINDS)) {
        const b = document.createElement('button'); b.className = 'opt kind'; b.dataset.kind = kind;
        b.appendChild(symbolSvg(kind, 30)); const sp = document.createElement('span'); sp.textContent = T.pk[kind]; b.appendChild(sp);
        b.onclick = () => { open(null); select(null); placing = kind; plan.setPlacing(kind); $('part').setAttribute('aria-pressed', 'false'); paintSel(); };
        g.appendChild(b);
      }
      const c = { base: 0, added: 0, moved: 0, removed: 0 };
      for (const p of dv.points) c[p.state] += 1;
      el.insertAdjacentHTML('beforeend', '<p class="count" data-nd="pcount">' + esc(T.pointsCount(c.base + c.moved + c.removed, c.added, c.moved, c.removed)) + '</p><p class="fine">' + esc(T.pointsFine) + '</p>');
    }
    if (name === 'boq') {
      const q = quantities(store);
      h.textContent = T.budHead;
      const bud = estimate(store, catalog, prices, T);
      let html = bud.ready ? '<p class="total" data-nd="total">' + money({ lo: bud.lo, hi: bud.open ? null : bud.hi }) + '</p><p class="fine" style="margin-top:2px">' + T.budWhat + '</p>' +
        '<table style="margin-top:8px"><thead><tr><th>' + T.budLine + '</th><th class="n">' + T.budQty + '</th><th class="n">' + T.budRange + '</th></tr></thead><tbody>' +
        bud.rows.map((r) => '<tr><td>' + esc(r.label) + (r.where ? ' · ' + esc(r.where) : '') + (r.rough ? ' <span class="tag decor">' + T.rough + '</span>' : '') + '</td><td class="n">' + (r.sqm ? '<span class="mono">' + r.qty.toFixed(1) + '</span> ' + T.sqm : '<span class="mono">' + r.qty + '</span>') + '</td><td class="n">' + money(r) + '</td></tr>').join('') +
        '</tbody></table>' + (bud.missing.length ? '<p class="fine">' + T.budMissing + esc([...new Set(bud.missing)].join(', ')) + '</p>' : '') + '<p class="fine">' + T.budFine + '</p><h3 style="margin-top:14px">' + T.boqHead + '</h3>' : '<p class="fine">' + T.budLoading + '</p><h3 style="margin-top:10px">' + T.boqHead + '</h3>';
      html += '<table><thead><tr><th>' + T.boqFloor + '</th><th class="n">' + T.boqArea + '</th></tr></thead><tbody>';
      for (const k in q.floors) html += '<tr><td>' + esc(catalog.FINISHES[k].he) + ' <span class="tag ' + catalog.FINISHES[k].status + '">' + (catalog.FINISHES[k].status === 'base' ? T.base : T.upgrade) + '</span></td><td class="n"><span class="mono">' + q.floors[k].toFixed(1) + '</span> ' + T.sqm + '</td></tr>';
      html += '</tbody></table><table style="margin-top:10px"><thead><tr><th>' + T.boqRoom + '</th><th class="n">' + T.boqSize + '</th><th class="n">' + T.boqArea + '</th></tr></thead><tbody>';
      for (const r of q.rooms) html += '<tr><td>' + esc(r.fresh ? T.newSpace : r.name) + '</td><td class="n mono">' + (r.w != null ? r.w + '×' + r.d : '') + '</td><td class="n mono">' + r.net.toFixed(1) + '</td></tr>';
      html += '</tbody></table><table style="margin-top:10px"><thead><tr><th>' + T.boqItems + '</th><th class="n">' + T.boqCount + '</th></tr></thead><tbody>';
      for (const k in q.items) html += '<tr><td>' + esc(catalog.ITEMS[k].he) + '</td><td class="n mono">' + q.items[k] + '</td></tr>';
      html += '</tbody></table><table style="margin-top:10px" data-nd="boq-points"><thead><tr><th>' + T.boqPoints + '</th><th class="n">' + T.boqBase + '</th><th class="n">' + T.boqAdded + '</th><th class="n">' + T.boqMoved + '</th><th class="n">' + T.boqGone + '</th></tr></thead><tbody>';
      for (const k in q.points) { const c = q.points[k]; html += '<tr><td>' + esc(T.pointName[k]) + '</td><td class="n mono">' + (c.base + c.moved + c.removed) + '</td><td class="n mono">' + c.added + '</td><td class="n mono">' + c.moved + '</td><td class="n mono">' + c.removed + '</td></tr>'; }
      const pa = q.partitions;
      html += '</tbody></table><table style="margin-top:10px" data-nd="boq-parts"><thead><tr><th></th><th class="n">' + T.boqLen + '</th><th class="n">' + T.boqWallArea + '</th></tr></thead><tbody>' +
        '<tr><td>' + T.boqPartAdded + '</td><td class="n"><span class="mono">' + pa.added.m.toFixed(2) + '</span> ' + T.m + '</td><td class="n"><span class="mono">' + pa.added.sqm.toFixed(1) + '</span> ' + T.sqm + '</td></tr>' +
        '<tr><td>' + T.boqPartGone + '</td><td class="n"><span class="mono">' + pa.removed.m.toFixed(2) + '</span> ' + T.m + '</td><td class="n"><span class="mono">' + pa.removed.sqm.toFixed(1) + '</span> ' + T.sqm + '</td></tr>';
      el.insertAdjacentHTML('beforeend', html + '</tbody></table><p class="fine">' + T.boqFine + '</p>' + (saveKey ? '<p class="fine">' + T.savedHere + '</p><button class="opt" data-nd="reset" style="margin-top:8px;width:100%">' + T.startOver + '</button>' : ''));
      const rb = $('reset'); if (rb) rb.onclick = () => { store.load(fresh()); select(null); open(null); toast(T.startedOver); };
    }
  }
  const setMode = (m) => { if (!space) return; space.setMode(m); $('m-doll').setAttribute('aria-pressed', m === 'doll'); $('m-walk').setAttribute('aria-pressed', m === 'walk'); paintSel(); };

  root.querySelectorAll('nav button[data-sheet]').forEach((b) => (b.onclick = () => { if (plan.mode) { plan.setPlacing(null); modeDone(); } open(b.dataset.sheet); }));
  $('undo').onclick = () => store.undo(); $('redo').onclick = () => store.redo();
  $('rot').onclick = () => { const it = sel && store.item(sel.id); if (it) store.apply({ op: 'item.rot', id: it.id, rot: it.rot + 90 }); };
  $('del').onclick = () => {
    if (!sel) return;
    const op = sel.type === 'item' ? { op: 'item.remove', id: sel.id } : sel.type === 'point' ? { op: 'point.remove', id: sel.id } : { op: 'partition.remove', id: sel.id };
    const r = store.apply(op);
    if (!r.ok) { toast(why(r), 'stop'); return; }
    if (r.warn) toast(why(r.warn)); // allowed, but said out loud (a wet room's partition)
    select(sel.type === 'item' || !(store.point(sel.id) || store.isRemoved(sel.id)) ? null : sel); // a removed base point or partition stays chosen, to be put back
  };
  $('restore').onclick = () => {
    if (!sel) return;
    const r = store.apply(sel.type === 'point' ? { op: 'point.restore', id: sel.id } : { op: 'partition.restore', id: sel.id });
    if (!r.ok) toast(why(r), 'stop'); else select(sel);
  };
  $('part').onclick = () => { const on = plan.mode !== 'part'; plan.setPartMode(on); if (on) { open(null); select(null); } modeDone(); $('part').setAttribute('aria-pressed', on); paintSel(); };
  $('m-doll').onclick = () => setMode('doll'); $('m-walk').onclick = () => setMode('walk');
  if (opts.onClose) $('close').onclick = () => opts.onClose(api);
  if (opts.onCall) $('call').onclick = () => opts.onCall(api);
  if (opts.onSend) $('send').onclick = () => opts.onSend(api);
  let saveT = 0;
  const saveNow = () => { if (!saveKey || !alive) return; try { const d = store.design; localStorage.setItem(saveKey, JSON.stringify({ ...d, log: d.log.slice(-200) })); timings.saved_at = Date.now(); } catch (e) { /* storage full or blocked: the design still works */ } };
  store.on((e) => {
    if (e.type !== 'change') return;
    if (e.touched.all) { sel = null; plan.setPlacing(null); plan.setSelection(null); if (space) space.reload(); modeDone(); }
    else if (sel && sel.type === 'point' && !store.point(sel.id)) select(null); // an undone point is no longer there
    else if (sel) paintSel();
    if (e.warn && (e.remote || e.replay)) toast(why(e.warn));
    head(); if (sheet) open(sheet, true); clearTimeout(saveT); saveT = setTimeout(saveNow, 400); subs.forEach((f) => f(e)); });

  // the divider between the two views: drag it, or use the arrow keys
  const wide = () => root.clientWidth >= 900;
  let barDrag = false, split = 42;
  const setSplit = (pct) => { split = Math.max(25, Math.min(75, pct)); if (wide()) root.style.gridTemplateColumns = 'minmax(0,' + split + 'fr) 14px minmax(0,' + (100 - split) + 'fr)'; else root.style.setProperty('--split', split + '%'); };
  $('bar').addEventListener('pointerdown', (ev) => { barDrag = true; try { $('bar').setPointerCapture(ev.pointerId); } catch (e) { /* synthetic pointer */ } });
  $('bar').addEventListener('pointermove', (ev) => { if (!barDrag) return; const r = root.getBoundingClientRect(); setSplit(wide() ? ((T.dir === 'rtl' ? r.right - ev.clientX : ev.clientX - r.left) / r.width) * 100 : ((ev.clientY - r.top - 60) / (r.height - 120)) * 100); });
  $('bar').addEventListener('pointerup', () => (barDrag = false));
  $('bar').addEventListener('keydown', (ev) => { if (ev.key === 'ArrowUp' || ev.key === 'ArrowRight') setSplit(split - 5); if (ev.key === 'ArrowDown' || ev.key === 'ArrowLeft') setSplit(split + 5); });

  const api = {
    store, plan, timings, version: 1, get selection() { return sel; },
    get space() { return space; },
    getDesign: () => JSON.parse(JSON.stringify(store.design)),
    quantities: () => quantities(store),
    getView: () => (space ? space.getView() : null),
    setView: (v) => space && space.setView(v),
    on: (f) => { subs.add(f); return () => subs.delete(f); },
    select, setMode, toast,
    ready3d: null,
    saveNow, restored,
    destroy() { clearTimeout(saveT); saveNow(); alive = false; if (space && space.destroy) space.destroy(); shadow.textContent = ''; subs.clear(); },
  };
  head(); paintSel();
  if (restored) toast(T.restored);
  // price ranges are a small separate file: the designer works without it and fills the prices in when it arrives
  api.readyPrices = fetch(BASE + 'data/price-ranges.json').then((r) => (r.ok ? r.json() : null)).then((d) => { if (d && alive) { prices = d.items; api.prices = prices; if (sheet) open(sheet, true); } return prices; }).catch(() => null);
  api.budget = () => estimate(store, catalog, prices);

  // the plan is on screen; only now ask for the 3D library
  api.ready3d = import('./space.js').then(({ mountSpace }) => {
    if (!alive) return null;
    space = mountSpace($('space'), store, catalog, { select, camera: (v) => plan.setCamera(v), frame: (dt, rms) => { timings.last_change_ms = store.lastApplyMs + rms; } });
    timings.space_ms = performance.now() - t0;
    requestAnimationFrame(() => requestAnimationFrame(() => { timings.first_3d_frame_ms = performance.now() - t0; }));
    if (sel) space.setSelection(sel);
    // real furniture models stream in after the first picture; without the list the true-size boxes stay
    if (opts.models !== false) fetch(BASE + 'models/models.json').then((r) => (r.ok ? r.json() : null)).then((list) => { if (list && alive && space) space.useModels(BASE + 'models/', list); }).catch(() => {});
    return space;
  });
  return api;
}
