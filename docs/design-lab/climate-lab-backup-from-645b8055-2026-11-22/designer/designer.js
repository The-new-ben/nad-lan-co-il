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
import { roomName } from './roomnames.js';
import { buildOrder, saveOrder, ORDER_KEY } from './order.js';

const BASE = new URL('.', import.meta.url).href;
const FONTS = 'https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans+Hebrew:wght@400;600;700&family=IBM+Plex+Sans:wght@400;600;700&family=IBM+Plex+Sans+Arabic:wght@400;600;700&display=swap';
const track = (name, data) => { try { if (typeof window !== 'undefined' && window.nlTrack) window.nlTrack(name, data); } catch (e) { /* the report is never in the way */ } };
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

function ensureFonts() { // a font must be declared in the document itself; a shadow root cannot load one
  if (document.querySelector('link[data-nd-fonts]')) return;
  const l = document.createElement('link'); l.rel = 'stylesheet'; l.href = FONTS; l.setAttribute('data-nd-fonts', ''); document.head.appendChild(l);
}

export async function mount(host, opts = {}) {
  const T = strings(opts.lang || 'he'), LG = T.lang || 'he', t0 = performance.now();
  const lab = (rec) => catalog.label(rec, LG), rname = (he) => roomName(he, LG);
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
  const root = document.createElement('div'); root.className = 'nd'; root.dir = T.dir; root.lang = LG;
  root.innerHTML =
    '<header><div><h2>' + esc(opts.title || T.title) + '</h2><p data-nd="sub"></p></div>' +
    (opts.onEditPlan ? '<button class="hb" data-nd="editplan" style="width:auto;padding:0 10px;font-size:13px;font-weight:600;white-space:nowrap">' + esc(T.pm.editPlan) + '</button>' : '') +
    '<button class="hb" data-nd="undo" aria-label="' + T.undo + '" title="' + T.undo + '" disabled><svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M9 6l-6 6 6 6M3 12h12a6 6 0 0 1 6 6"/></svg></button>' +
    '<button class="hb" data-nd="redo" aria-label="' + T.redo + '" title="' + T.redo + '" disabled><svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M15 6l6 6-6 6M21 12H9a6 6 0 0 0-6 6"/></svg></button>' +
    (opts.onClose ? '<button class="hb" data-nd="close" aria-label="' + T.close + '" title="' + T.close + '"><svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M6 6l12 12M18 6L6 18"/></svg></button>' : '') + '</header>' +
    '<section class="space" data-nd="space" aria-label="' + T.space + '"><div class="chips" role="group" aria-label="' + T.viewGroup + '">' +
    '<button data-nd="m-doll" aria-pressed="true">' + T.viewTop + '</button><button data-nd="m-walk" aria-pressed="false">' + T.viewWalk + '</button><button class="rise" data-nd="rise">' + esc(T.rise) + '</button></div>' +
    '<div class="walkbar" data-nd="walkbar" role="group" aria-label="' + esc(T.roomsGroup) + '" hidden></div>' +
    '<p class="note" data-nd="vnote">' + esc(opts.note || T.note) + '</p></section>' +
    '<div class="bar" data-nd="bar" role="separator" aria-label="' + T.split + '" tabindex="0"><i></i></div>' +
    '<section class="plan" data-nd="plan" aria-label="' + T.plan + '"><div class="ptools"><p class="hint" data-nd="hint"></p><button class="ptool" data-nd="part" aria-pressed="false">' + T.partNew + '</button></div></section>' +
    '<nav aria-label="' + T.tools + '"><button data-sheet="items" aria-expanded="false">' + T.tItems + '</button><button data-sheet="floor" aria-expanded="false">' + esc(T.tFinish) + '</button>' +
    '<button data-sheet="points" aria-expanded="false">' + T.tPoints + '</button>' +
    '<button data-sheet="notes" aria-expanded="false" class="red">' + esc(T.tNotes) + '</button>' +
    '<button data-sheet="order" aria-expanded="false">' + esc(T.tOrder) + '</button>' +
    (opts.onCall ? '<button data-nd="call">' + T.tCall + '</button>' : '') + (opts.onSend ? '<button class="go" data-nd="send">' + T.tSend + '</button>' : '') + '</nav>' +
    '<div class="sheet" data-nd="sheet" hidden></div>' +
    '<div class="selbar" data-nd="selbar" hidden><b data-nd="selname"></b><button data-nd="rot">' + T.rotate + '</button><button data-nd="restore">' + T.restore + '</button><button data-nd="del">' + T.remove + '</button></div>' +
    '<div class="toast" data-nd="toast" role="alert" hidden></div>';
  shadow.append(css, root);
  const $ = (k) => root.querySelector('[data-nd="' + k + '"]');
  await new Promise((r) => { if (css.sheet) r(); else { css.addEventListener('load', r, { once: true }); css.addEventListener('error', r, { once: true }); } });

  let sel = null, sheet = null, space = null, toastT = 0, alive = true, prices = null, placing = null;
  const nf = new Intl.NumberFormat(LG === 'ar' ? 'ar-u-nu-latn' : LG === 'he' ? 'he-IL' : LG);
  let draftNote = null; // a place on the plan waiting for its text
  const money = (r) => (!r ? '' : r.hi == null ? nf.format(r.lo) + ' ' + T.shekel + T.andUp : nf.format(r.lo) + T.to + nf.format(r.hi) + ' ' + T.shekel);
  const subs = new Set(), timings = {};
  const why = (r) => (r && T.rules && T.rules[r.code]) || (r && r.reason) || ''; // a rule's sentence in the page language when it has one
  const toast = (msg, kind) => { $('toast').textContent = msg; $('toast').className = 'toast' + (kind === 'stop' ? ' stop' : ''); $('toast').hidden = false; clearTimeout(toastT); toastT = setTimeout(() => ($('toast').hidden = true), 3200); };
  const select = (s) => { sel = s; plan.setSelection(s); if (space) space.setSelection(s); paintSel(); if (s && s.type === 'room' && sheet !== 'floor') open('floor'); else if (s && s.type === 'note') { draftNote = null; open('notes', true); } else if (sheet) open(sheet, true); };
  const modeDone = () => { placing = null; $('part').setAttribute('aria-pressed', 'false'); paintSel(); };
  const plan = mountPlan($('plan'), store, catalog, { T, select, blocked: (r) => toast(why(r), 'stop'), camMove: (p) => space && space.walkTo(p), modeDone, roomName: rname,
    notePlace: (p) => { if (!store.roomAt(p[0], p[1])) { toast(why({ code: 'note.outside' }) || T.notePlace, 'stop'); return; } draftNote = p; sel = null; plan.setSelection(null); open('notes', true); } });
  timings.plan_ms = performance.now() - t0;

  function paintSel() { // the dark bar and the hint line, for every kind of selection and for the two drawing modes
    const dv = store.derived, it = sel && sel.type === 'item' && store.item(sel.id), pt = sel && sel.type === 'point' && store.point(sel.id);
    const w = sel && sel.type === 'wall' && (dv.wallBy[sel.id] || dv.ghosts.find((g) => g.id === sel.id)), gone = !!w && store.isRemoved(w.id);
    const part = w && w.kind === 'partition';
    let name = '', bar = { rot: false, restore: false, del: false };
    if (it) { name = lab(catalog.ITEMS[it.sku]); bar = { rot: true, del: true }; }
    else if (pt) { name = T.pointName[pt.kind] + (pt.state !== 'base' ? ' · ' + T.pointState[pt.state] : ''); bar = { restore: pt.state === 'moved' || pt.state === 'removed', del: pt.state !== 'removed' }; }
    else if (part) { name = gone ? T.partGoneName : w.added ? T.partAddedName : T.partName; bar = { restore: gone, del: !gone }; }
    $('selbar').hidden = !(it || pt || part);
    $('selname').textContent = name;
    $('rot').hidden = !bar.rot; $('restore').hidden = !bar.restore; $('del').hidden = !bar.del;
    $('restore').textContent = part ? T.partRestore : T.restore; $('del').textContent = part ? T.partRemove : T.remove;
    const m = plan.mode;
    $('hint').textContent = m === 'note' ? T.notePlace : m === 'place' ? (POINT_KINDS[placing].ceiling ? T.placeLight : T.placeWall(T.pointName[placing])) : m === 'part' ? T.partHint
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
    const el = $('sheet'); el.hidden = !name; el.textContent = ''; el.classList.remove('wide');
    if (!name) return;
    const h = document.createElement('h3'); el.appendChild(h);
    const dv = store.derived;
    if (name === 'items') {
      h.textContent = T.itemsHead;
      const g = document.createElement('div'); g.className = 'grid'; el.appendChild(g);
      for (const sku in catalog.ITEMS) {
        const c = catalog.ITEMS[sku], b = document.createElement('button'); b.className = 'opt';
        const pr = tidy(itemRange(c, prices));
        b.innerHTML = '<span>' + esc(lab(c)) + '</span><small><span class="mono">' + c.w + '×' + c.d + '</span> ' + T.cm + '</small><small class="pr">' + (pr ? money(pr) : prices ? T.noPrice : '') + '</small>';
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
      h.textContent = room ? T.floorHead + ': ' + (room.room.fresh ? T.newSpace : rname(room.room.name_he)) + ' · ' + room.net.toFixed(1) + ' ' + T.sqm : T.finishPick;
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
        b.innerHTML = '<span>' + esc(lab(f)) + '</span><small><span class="tag ' + f.status + '">' + (f.status === 'base' ? T.base : T.upgrade) + '</span></small>' + (f.status === 'base' ? '' : '<small class="pr">' + (fp ? money(fp) + ' ' + esc(prices[f.price].unit_he) : prices ? T.noPrice : '') + '</small>');
        b.onclick = () => store.apply({ op: 'finish.set', key: 'floor:' + room.id, value: key === room.room.floor ? null : key });
        g.appendChild(b);
      }
      if (room.room.type !== 'balcony' && catalog.WALLS) { // the paint of this room's walls (HAD-792)
        const wh = document.createElement('h3'); wh.style.marginTop = '12px'; wh.textContent = T.wallHead; el.appendChild(wh);
        const wg = document.createElement('div'); wg.className = 'grid'; el.appendChild(wg);
        const now = store.wallOf(room.id) || 'w-white';
        for (const key of catalog.WALL_CHOICES) {
          const w = catalog.WALLS[key], b = document.createElement('button'); b.className = 'opt swatch'; b.setAttribute('aria-pressed', now === key); b.dataset.wall = key;
          b.innerHTML = '<i style="background:' + w.hex + '"></i><span>' + esc(lab(w)) + (w.status === 'base' ? '' : '<small style="display:block">' + esc(T.wallReq) + '</small>') + '</span>';
          b.onclick = () => store.apply({ op: 'finish.set', key: 'wall:' + room.id, value: key === 'w-white' ? null : key });
          wg.appendChild(b);
        }
      }
    }
    if (name === 'notes') { // notes to the builder: pinned on the plan, kept on this device, part of the order (HAD-792, gap 16)
      const notes = store.design.notes || [], cur = sel && sel.type === 'note' ? store.note(sel.id) : null;
      if (draftNote || cur) {
        const idx = cur ? notes.findIndex((n) => n.id === cur.id) + 1 : notes.length + 1, at = draftNote || [cur.x, cur.y], rid = store.roomAt(at[0], at[1]), f = rid && dv.faceBy[rid];
        h.innerHTML = '<span class="ntag">' + idx + '</span> ' + esc(T.noteName(idx)) + (f && f.room ? ' · ' + esc(f.room.fresh ? T.newSpace : rname(f.room.name_he)) : '');
        const box = document.createElement('div'); box.className = 'notebox';
        box.innerHTML = '<label for="ndnote" style="font-size:12.5px;color:var(--ink2)">' + esc(T.noteLabel) + '</label><textarea id="ndnote" data-nd="notetext" maxlength="400" rows="3" placeholder="' + esc(T.notePh) + '"></textarea>' +
          '<div class="row"><button class="save" data-nd="notesave">' + esc(T.noteSave) + '</button>' + (cur ? '<button data-nd="notedel">' + esc(T.noteDel) + '</button>' : '') + '</div><p class="fine">' + esc(T.noteFine) + '</p>';
        el.appendChild(box);
        const ta = box.querySelector('textarea'); ta.value = cur ? cur.text : '';
        if (!keep || draftNote) setTimeout(() => { try { ta.focus({ preventScroll: true }); } catch (e) { /* none */ } }, 30);
        box.querySelector('[data-nd="notesave"]').onclick = () => {
          const text = ta.value.trim();
          if (!text) { toast(T.noteNeed, 'stop'); return; }
          if (cur) { const r = store.apply({ op: 'note.edit', id: cur.id, text }); if (!r.ok) { toast(why(r), 'stop'); return; } }
          else { const id = 'n' + Date.now().toString(36), r = store.apply({ op: 'note.add', note: { id, x: at[0], y: at[1], text } }); if (!r.ok) { toast(why(r), 'stop'); return; } track('designer_action', { ...tk(), a: 'note' }); }
          draftNote = null; select(null); open('notes', true); toast(T.noteSaved);
        };
        const del = box.querySelector('[data-nd="notedel"]');
        if (del) del.onclick = () => { store.apply({ op: 'note.remove', id: cur.id }); draftNote = null; select(null); open('notes', true); toast(T.noteGone); };
      } else {
        h.textContent = T.notesHead;
        const add = document.createElement('button'); add.className = 'primary'; add.dataset.nd = 'noteadd'; add.style.background = 'var(--dim)'; add.textContent = T.noteAdd; el.appendChild(add);
        add.onclick = () => { open(null); select(null); plan.setNotePlacing(true); paintSel(); };
        if (!notes.length) el.insertAdjacentHTML('beforeend', '<p class="fine">' + esc(T.noteEmpty) + '</p>');
        else {
          const ul = document.createElement('ul'); ul.className = 'nlist'; el.appendChild(ul);
          notes.forEach((n, i) => {
            const li = document.createElement('li'), b = document.createElement('button'), f = n.room && dv.faceBy[n.room];
            b.innerHTML = '<span class="ntag">' + (i + 1) + '</span><span>' + (f && f.room ? '<b>' + esc(f.room.fresh ? T.newSpace : rname(f.room.name_he)) + ':</b> ' : '') + esc(n.text) + '</span>';
            b.onclick = () => select({ type: 'note', id: n.id }); li.appendChild(b); ul.appendChild(li);
          });
          el.insertAdjacentHTML('beforeend', '<p class="fine">' + esc(T.noteFine) + '</p>');
        }
      }
    }
    if (name === 'order') { el.classList.add('wide'); renderOrder(el, h); }
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
      for (const k in q.floors) html += '<tr><td>' + esc(lab(catalog.FINISHES[k])) + ' <span class="tag ' + catalog.FINISHES[k].status + '">' + (catalog.FINISHES[k].status === 'base' ? T.base : T.upgrade) + '</span></td><td class="n"><span class="mono">' + q.floors[k].toFixed(1) + '</span> ' + T.sqm + '</td></tr>';
      html += '</tbody></table><table style="margin-top:10px"><thead><tr><th>' + T.boqRoom + '</th><th class="n">' + T.boqSize + '</th><th class="n">' + T.boqArea + '</th></tr></thead><tbody>';
      for (const r of q.rooms) html += '<tr><td>' + esc(r.fresh ? T.newSpace : rname(r.name)) + '</td><td class="n mono">' + (r.w != null ? r.w + '×' + r.d : '') + '</td><td class="n mono">' + r.net.toFixed(1) + '</td></tr>';
      html += '</tbody></table><table style="margin-top:10px"><thead><tr><th>' + T.boqItems + '</th><th class="n">' + T.boqCount + '</th></tr></thead><tbody>';
      for (const k in q.items) html += '<tr><td>' + esc(lab(catalog.ITEMS[k])) + '</td><td class="n mono">' + q.items[k] + '</td></tr>';
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
  const setMode = (m) => {
    if (!space) return; space.setMode(m); $('m-doll').setAttribute('aria-pressed', m === 'doll'); $('m-walk').setAttribute('aria-pressed', m === 'walk'); $('rise').hidden = m === 'walk';
    $('vnote').textContent = m === 'walk' ? T.viewNote + ' ' + (opts.note || T.note) : opts.note || T.note;
    if (m === 'walk') track('designer_action', { ...tk(), a: 'walk' });
    paintWalk(); paintSel();
  };
  // the walk's row: a tour of the whole apartment, then one button per room (the room you stand in is marked)
  function paintWalk(st) {
    const bar = $('walkbar'), on = space && space.mode === 'walk';
    bar.hidden = !on; if (!on) return;
    st = st || space.walkState();
    bar.textContent = '';
    const t = document.createElement('button'); t.className = 'tour'; t.dataset.nd = 'tour'; t.textContent = st.touring ? T.tourStop : T.tour;
    t.onclick = () => { if (space.walkState().touring) space.stopTour(); else space.tour(); paintWalk(); };
    bar.appendChild(t);
    for (const r of space.rooms()) {
      const b = document.createElement('button'); b.dataset.room = r.id; b.textContent = r.fresh ? T.newSpace : rname(r.name_he); b.setAttribute('aria-pressed', String(st.room === r.id && !st.moving));
      b.onclick = () => { space.goRoom(r.id); }; bar.appendChild(b);
    }
  }
  // ---- the design order (HAD-792): a structured request for the basket of the buying journey ----
  const services = (() => { try { return new Set(JSON.parse(localStorage.getItem('nl-design-svc:' + (saveKey || '-')) || '[]')); } catch (e) { return new Set(); } })();
  const keepServices = () => { try { localStorage.setItem('nl-design-svc:' + (saveKey || '-'), JSON.stringify([...services])); } catch (e) { /* this visit only */ } };
  const meta = opts.order || {};
  const tk = () => ({ project: (meta.project && meta.project.slug) || (apt.source && apt.source.kind === 'own' ? 'mine' : 'example'), unit: (meta.unit && meta.unit.id) || apt.unit.unit_id || apt.id || '', source: meta.source || 'example' });
  const orderNow = () => buildOrder({ store, apt, catalog, T, lang: LG, meta, services: [...services], budget: estimate(store, catalog, prices, T), roomName: rname, quantities: quantities(store) });
  function renderOrder(el, h) {
    const o = orderNow();
    h.innerHTML = '<span>' + esc(T.orderHead) + '</span>';
    const d = document.createElement('div'); d.className = 'order'; el.appendChild(d);
    const line = (a, b) => '<div class="line"><span>' + esc(a) + '</span><b>' + esc(b) + '</b></div>';
    let html = '<p class="meta">' + esc(o.id) + ' · ' + esc(T.orderVer(o.rev)) + '</p><p style="font-weight:700;margin-top:2px">' + esc((o.project.title ? o.project.title + ' · ' : '') + o.unit.label) + '</p>';
    html += '<h4>' + esc(T.secFinish) + '</h4>' + (o.finishes.length ? o.finishes.map((f) => line(f.roomName + ' · ' + (f.surface === 'floor' ? T.floorW : T.wallW), f.label)).join('') : '<p class="fine" style="margin-top:4px">' + esc(T.none) + '</p>');
    html += '<h4>' + esc(T.secChanges) + '</h4>' + (o.changes.length ? o.changes.map((c) => line(c.label, c.qty || '')).join('') : '<p class="fine" style="margin-top:4px">' + esc(T.none) + '</p>');
    html += '<h4 class="red">' + esc(T.secNotes) + '</h4>' + (o.notes.length ? o.notes.map((n, i) => '<div class="line" style="justify-content:flex-start"><span class="ntag">' + (i + 1) + '</span><span>' + (n.roomName ? '<b>' + esc(n.roomName) + ':</b> ' : '') + esc(n.text) + '</span></div>').join('') : '<p class="fine" style="margin-top:4px">' + esc(T.noteEmpty) + '</p>');
    html += '<h4>' + esc(T.secServices) + '</h4>' + Object.keys(T.services).map((k) => '<label><input type="checkbox" data-svc="' + k + '"' + (services.has(k) ? ' checked' : '') + '> ' + esc(T.services[k]) + '</label>').join('');
    html += '<h4>' + esc(T.secItems) + '</h4><p style="font-size:13.5px">' + esc(T.itemsN(o.items.reduce((s, i) => s + i.count, 0))) + '</p>';
    if (o.budget) html += '<h4>' + esc(T.secBudget) + '</h4><p class="total" style="font-size:18px">' + money({ lo: o.budget.min, hi: o.budget.max == null ? null : o.budget.max }) + '</p>';
    html += '<button class="opt" data-nd="boqopen" style="width:100%;margin-top:10px">' + esc(T.budHead) + ' · ' + esc(String(T.boqHead).split(':')[0]) + '</button>';
    html += '<div class="acts"><button class="go" data-nd="basket">' + esc(T.addBasket) + '</button><button data-nd="print">' + esc(T.print) + '</button></div><p class="fine">' + esc(T.orderFine) + '</p>';
    d.innerHTML = html;
    d.querySelectorAll('[data-svc]').forEach((c) => (c.onchange = () => { if (c.checked) services.add(c.dataset.svc); else services.delete(c.dataset.svc); keepServices(); queueOrder(); }));
    d.querySelector('[data-nd="boqopen"]').onclick = () => open('boq');
    d.querySelector('[data-nd="basket"]').onclick = () => { const x = orderNow(); saveOrder(x); try { window.dispatchEvent(new CustomEvent('nadlan:design-order', { detail: x })); } catch (e) { /* none */ } track('designer_action', { ...tk(), a: 'order' }); toast(T.added); };
    d.querySelector('[data-nd="print"]').onclick = () => printOrder(orderNow());
  }
  function printOrder(o) {
    const w = window.open('', '_blank'); if (!w) return;
    const row = (a, b) => '<tr><td>' + esc(a) + '</td><td>' + esc(b) + '</td></tr>';
    const sec = (t, rows) => '<h2>' + esc(t) + '</h2><table>' + (rows || '<tr><td>' + esc(T.none) + '</td></tr>') + '</table>';
    w.document.write('<!doctype html><html lang="' + LG + '" dir="' + T.dir + '"><head><meta charset="utf-8"><title>' + esc(T.orderHead + ' · ' + o.id) + '</title><style>body{font:14px/1.5 "IBM Plex Sans Hebrew","IBM Plex Sans","IBM Plex Sans Arabic",Arial,sans-serif;color:#0F2233;margin:24px}h1{font-size:20px;margin:0 0 4px}h2{font-size:14px;border-bottom:2px solid #0F2233;margin:18px 0 6px;padding-bottom:3px}table{width:100%;border-collapse:collapse}td{padding:5px 4px;border-bottom:1px solid #B9C6CF;vertical-align:top}td+td{text-align:end;font-weight:600}.m{font-family:monospace;color:#46596A;font-size:12px}.f{font-size:12px;color:#46596A;margin-top:18px}</style></head><body>' +
      '<p class="m">nad-lan.co.il · ' + esc(o.id) + ' · ' + esc(T.orderVer(o.rev)) + ' · ' + esc(o.updated.slice(0, 10)) + '</p><h1>' + esc(T.orderHead) + ': ' + esc((o.project.title ? o.project.title + ' · ' : '') + o.unit.label) + '</h1>' +
      sec(T.secFinish, o.finishes.map((f) => row(f.roomName + ' · ' + (f.surface === 'floor' ? T.floorW : T.wallW), f.label)).join('')) +
      sec(T.secChanges, o.changes.map((c) => row(c.label, c.qty || '')).join('')) +
      sec(T.secNotes, o.notes.map((n, i) => row((i + 1) + '. ' + (n.roomName || ''), n.text)).join('')) +
      sec(T.secServices, o.services.map((s) => row(s.label, '')).join('')) +
      sec(T.secItems, o.items.map((i) => row(i.label + (i.roomName ? ' · ' + i.roomName : ''), String(i.count))).join('')) +
      (o.budget ? sec(T.secBudget, row(T.budWhat, money({ lo: o.budget.min, hi: o.budget.max == null ? null : o.budget.max }))) : '') +
      '<p class="f">' + esc(T.orderFine) + '</p><p class="f">' + esc(o.link || '') + '</p></body></html>');
    w.document.close(); setTimeout(() => { try { w.focus(); w.print(); } catch (e) { /* the page stays open to print by hand */ } }, 300);
  }
  let orderT = 0;
  const queueOrder = () => { clearTimeout(orderT); orderT = setTimeout(() => { if (!alive) return; const x = orderNow(); saveOrder(x, true); try { window.dispatchEvent(new CustomEvent('nadlan:design-order-updated', { detail: x })); } catch (e) { /* none */ } }, 1500); };

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
  $('rise').onclick = () => { if (space) space.rise(); };
  if (opts.onClose) $('close').onclick = () => opts.onClose(api);
  if (opts.onEditPlan) $('editplan').onclick = () => opts.onEditPlan(api);
  if (opts.onCall) $('call').onclick = () => opts.onCall(api);
  if (opts.onSend) $('send').onclick = () => opts.onSend(api);
  let saveT = 0, ownWarned = false;
  const saveNow = () => { if (!saveKey || !alive) return; try { const d = store.design; localStorage.setItem(saveKey, JSON.stringify({ ...d, log: d.log.slice(-200) })); timings.saved_at = Date.now(); } catch (e) { /* storage full or blocked: the design still works */ } };
  store.on((e) => {
    if (e.type !== 'change') return;
    if (e.touched.all) { sel = null; plan.setPlacing(null); plan.setSelection(null); if (space) space.reload(); modeDone(); }
    else if (sel && sel.type === 'point' && !store.point(sel.id)) select(null); // an undone point is no longer there
    else if (sel) paintSel();
    if (e.warn && (e.remote || e.replay)) toast(why(e.warn));
    // a plan the person loaded themselves says nothing about load-bearing walls: said once per opening, at the first wall change
    if (!ownWarned && apt.source && apt.source.kind === 'own' && !e.remote && !e.replay && /^(wall\.shift|partition\.)/.test(e.op.op)) { ownWarned = true; toast(T.pm.ownWalls); }
    head(); if (sheet) open(sheet, true); clearTimeout(saveT); saveT = setTimeout(saveNow, 400); subs.forEach((f) => f(e));
    if (e.touched.geometry && space && space.mode === 'walk') paintWalk();
    if (!e.remote && !e.replay && e.op) { // what the buyer did, for the developer's report (package 5): the kind of action only, never text
      const o = e.op.op, a = o === 'finish.set' ? 'finish' : o === 'partition.add' ? 'partition-add' : o === 'partition.remove' ? 'partition-remove' : o === 'point.add' ? 'point-add' : o === 'point.move' ? 'point-move' : o === 'item.add' ? 'item-add' : null;
      if (a && a !== lastTrack) { lastTrack = a; track('designer_action', { ...tk(), a }); }
    }
    if (saveKey || meta.project) queueOrder(); });
  let lastTrack = null;

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
    order: () => orderNow(), lang: LG,
    quantities: () => quantities(store),
    getView: () => (space ? space.getView() : null),
    setView: (v) => space && space.setView(v),
    on: (f) => { subs.add(f); return () => subs.delete(f); },
    select, setMode, toast,
    ready3d: null,
    saveNow, restored,
    destroy() { clearTimeout(saveT); clearTimeout(orderT); saveNow(); alive = false; if (space && space.destroy) space.destroy(); shadow.textContent = ''; subs.clear(); },
  };
  head(); paintSel();
  if (restored) toast(T.restored);
  track('designer_open', tk());
  // price ranges are a small separate file: the designer works without it and fills the prices in when it arrives
  api.readyPrices = fetch(BASE + 'data/price-ranges.json').then((r) => (r.ok ? r.json() : null)).then((d) => { if (d && alive) { prices = d.items; api.prices = prices; if (sheet) open(sheet, true); } return prices; }).catch(() => null);
  api.budget = () => estimate(store, catalog, prices);

  // the plan is on screen; only now ask for the 3D library
  api.ready3d = import('./space.js').then(({ mountSpace }) => {
    if (!alive) return null;
    space = mountSpace($('space'), store, catalog, { select, camera: (v) => plan.setCamera(v), frame: (dt, rms) => { timings.last_change_ms = store.lastApplyMs + rms; }, walk: (st) => paintWalk(st), rise: opts.rise !== false });
    timings.space_ms = performance.now() - t0;
    requestAnimationFrame(() => requestAnimationFrame(() => { timings.first_3d_frame_ms = performance.now() - t0; }));
    if (sel) space.setSelection(sel);
    // real furniture models stream in after the first picture; without the list the true-size boxes stay
    if (opts.models !== false) fetch(BASE + 'models/models.json').then((r) => (r.ok ? r.json() : null)).then((list) => { if (list && alive && space) space.useModels(BASE + 'models/', list); }).catch(() => {});
    return space;
  });
  return api;
}
