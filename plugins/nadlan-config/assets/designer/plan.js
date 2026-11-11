// The 2D plan view of the apartment designer (HAD-701; first proven as the HAD-703 spike): an SVG drawn from the store's derived model. It never keeps geometry of its own.
import { WALL_KINDS } from './core.js';

const NS = 'http://www.w3.org/2000/svg';
const E = (tag, attrs, parent) => {
  const n = document.createElementNS(NS, tag);
  for (const k in attrs || {}) n.setAttribute(k, attrs[k]);
  if (parent) parent.appendChild(n);
  return n;
};
const P = (pts) => 'M' + pts.map((p) => p[0].toFixed(1) + ' ' + p[1].toFixed(1)).join('L') + 'Z';
const snap = (v, s) => Math.round(v / s) * s;

export function mountPlan(host, store, cat, hooks = {}) {
  const apt = store.apt;
  const xs = Object.values(apt.nodes).map((p) => p[0]), ys = Object.values(apt.nodes).map((p) => p[1]);
  const vb = [Math.min(...xs) - 60, Math.min(...ys) - 60, Math.max(...xs) - Math.min(...xs) + 120, Math.max(...ys) - Math.min(...ys) + 120];
  const svg = E('svg', { class: 'nd-plan', viewBox: vb.join(' '), role: 'group', 'aria-label': 'תוכנית הדירה' });
  host.appendChild(svg);
  const defs = E('defs', {}, svg);
  const hatch = E('pattern', { id: 'nd-mamad', width: 14, height: 14, patternUnits: 'userSpaceOnUse', patternTransform: 'rotate(45)' }, defs);
  E('rect', { width: 14, height: 14, fill: '#0F2233' }, hatch); E('line', { x1: 0, y1: 0, x2: 0, y2: 14, stroke: '#F2F5F7', 'stroke-width': 3 }, hatch);
  const L = {};
  for (const k of ['rooms', 'items', 'walls', 'open', 'labels', 'grips', 'cam']) L[k] = E('g', { class: 'L-' + k }, svg);
  let sel = null, liveDim = null;

  function drawGeometry() {
    const dv = store.derived;
    for (const k of ['rooms', 'walls', 'open', 'labels', 'grips']) L[k].textContent = '';
    for (const f of dv.faces) {
      if (!f.room) continue;
      const fin = cat.FINISHES[store.floorOf(f.id)] || {};
      E('path', { d: P(f.poly), class: 'room' + (sel && sel.type === 'room' && sel.id === f.id ? ' on' : ''), fill: fin.a || '#fff', 'fill-opacity': 0.5, 'data-room': f.id }, L.rooms);
      const cx = (f.bb.x0 + f.bb.x1) / 2, cy = (f.bb.y0 + f.bb.y1) / 2, small = f.bb.x1 - f.bb.x0 < 260;
      const t = E('text', { x: cx, y: cy - 6, class: 'rl' + (small ? ' s' : '') }, L.labels); t.textContent = f.room.name_he;
      const a = E('text', { x: cx, y: cy + (small ? 30 : 40), class: 'ra' + (small ? ' s' : '') }, L.labels); a.textContent = f.net.toFixed(1) + ' מ״ר';
      if ((sel && sel.type === 'room' && sel.id === f.id) || (liveDim && f.walls.includes(liveDim))) {
        const d = E('text', { x: cx, y: cy + (small ? 62 : 84), class: 'rd' }, L.labels); d.textContent = f.clearW + ' × ' + f.clearD;
      }
    }
    for (const w of dv.walls) {
      const kind = WALL_KINDS[w.kind], n = [-w.dir[1], w.dir[0]];
      if (w.kind === 'divider') { E('line', { x1: w.pa[0], y1: w.pa[1], x2: w.pb[0], y2: w.pb[1], class: 'wall divider' }, L.walls); }
      else {
        const t = Math.max(w.t, 6), e = w.kind === 'rail' ? 0 : t / 2, h = t / 2;
        const a = [w.pa[0] - w.dir[0] * e, w.pa[1] - w.dir[1] * e], b = [w.pb[0] + w.dir[0] * e, w.pb[1] + w.dir[1] * e];
        E('path', { d: P([[a[0] + n[0] * h, a[1] + n[1] * h], [b[0] + n[0] * h, b[1] + n[1] * h], [b[0] - n[0] * h, b[1] - n[1] * h], [a[0] - n[0] * h, a[1] - n[1] * h]]), class: 'wall ' + w.kind + (store.slides(w.id) ? ' free' : '') + (sel && sel.type === 'wall' && sel.id === w.id ? ' on' : '') }, L.walls);
        for (const o of w.openings) {
          const p0 = [w.pa[0] + w.dir[0] * o.at, w.pa[1] + w.dir[1] * o.at], p1 = [p0[0] + w.dir[0] * o.w, p0[1] + w.dir[1] * o.w], g = h + 2;
          E('path', { d: P([[p0[0] + n[0] * g, p0[1] + n[1] * g], [p1[0] + n[0] * g, p1[1] + n[1] * g], [p1[0] - n[0] * g, p1[1] - n[1] * g], [p0[0] - n[0] * g, p0[1] - n[1] * g]]), class: 'gap' }, L.open);
          if (o.type === 'door') {
            const s = o.swing || 1, q = [p0[0] + n[0] * s * o.w, p0[1] + n[1] * s * o.w], sweep = (w.dir[0] * n[1] - w.dir[1] * n[0]) * s > 0 ? 1 : 0;
            E('path', { d: 'M' + p0[0] + ' ' + p0[1] + 'L' + q[0] + ' ' + q[1] + 'M' + p1[0] + ' ' + p1[1] + 'A' + o.w + ' ' + o.w + ' 0 0 ' + sweep + ' ' + q[0] + ' ' + q[1], class: 'door' }, L.open);
          } else {
            E('line', { x1: p0[0], y1: p0[1], x2: p1[0], y2: p1[1], class: 'glass' + (o.type === 'slider' ? ' wide' : '') }, L.open);
            for (const s of [-1, 1]) E('line', { x1: p0[0] + n[0] * h * s, y1: p0[1] + n[1] * h * s, x2: p1[0] + n[0] * h * s, y2: p1[1] + n[1] * h * s, class: 'jamb' }, L.open);
          }
        }
      }
      // every wall answers a touch: a partition moves, a fixed wall says why it cannot
      const free = store.slides(w.id);
      if (w.kind !== 'rail') E('line', { x1: w.pa[0], y1: w.pa[1], x2: w.pb[0], y2: w.pb[1], class: 'hit' + (free ? ' free' : ''), 'data-wall': w.id }, L.grips);
      if (free) {
        const m = [(w.pa[0] + w.pb[0]) / 2, (w.pa[1] + w.pb[1]) / 2], g = E('g', { class: 'grip', transform: 'translate(' + m[0] + ' ' + m[1] + ') rotate(' + (Math.atan2(w.dir[1], w.dir[0]) * 180) / Math.PI + ')' }, L.grips);
        E('rect', { x: -34, y: -13, width: 68, height: 26, rx: 13, 'data-wall': w.id }, g);
        E('path', { d: 'M-12 -5H12M-12 5H12', 'data-wall': w.id }, g);
      }
    }
  }

  const itemEls = new Map();
  function drawItem(id) {
    const it = store.item(id); let g = itemEls.get(id);
    if (!it) { if (g) { g.remove(); itemEls.delete(id); } return; }
    const c = cat.ITEMS[it.sku];
    if (!g) {
      g = E('g', { class: 'item', 'data-item': id }, L.items);
      E('rect', { x: -c.w / 2, y: -c.d / 2, width: c.w, height: c.d, rx: c.shape === 'plant' ? c.w / 2 : 6, 'data-item': id }, g);
      if (c.shape !== 'rug' && c.shape !== 'plant') E('line', { x1: -c.w / 2 + 8, y1: -c.d / 2 + 9, x2: c.w / 2 - 8, y2: -c.d / 2 + 9, class: 'back' }, g);
      itemEls.set(id, g);
    }
    g.setAttribute('transform', 'translate(' + it.x + ' ' + it.y + ') rotate(' + it.rot + ')');
    g.setAttribute('class', 'item ' + c.shape + (sel && sel.type === 'item' && sel.id === id ? ' on' : ''));
  }
  const drawItems = () => { for (const id of [...itemEls.keys()]) drawItem(id); for (const it of store.design.items) drawItem(it.id); };

  // the camera of the 3D view, drawn on the plan: where you stand and what you see
  const cam = E('g', { class: 'cam' }, L.cam), cone = E('path', { class: 'cone' }, cam);
  E('circle', { r: 20, class: 'dot' }, cam); E('circle', { r: 70, class: 'hit', 'data-cam': 1 }, cam);
  function setCamera(v) {
    const x = Math.max(vb[0] + 24, Math.min(vb[0] + vb[2] - 24, v.x)), y = Math.max(vb[1] + 24, Math.min(vb[1] + vb[3] - 24, v.y));
    cam.setAttribute('transform', 'translate(' + x.toFixed(1) + ' ' + y.toFixed(1) + ') rotate(' + ((v.yaw * 180) / Math.PI).toFixed(1) + ')');
    const half = ((v.fov || 60) * Math.PI) / 360, r = v.walk ? 190 : 120;
    cone.setAttribute('d', 'M0 0L' + (r * Math.cos(half)).toFixed(1) + ' ' + (-r * Math.sin(half)).toFixed(1) + 'A' + r + ' ' + r + ' 0 0 1 ' + (r * Math.cos(half)).toFixed(1) + ' ' + (r * Math.sin(half)).toFixed(1) + 'Z');
    cam.classList.toggle('walk', !!v.walk);
  }

  const pt = (ev) => { const p = new DOMPoint(ev.clientX, ev.clientY).matrixTransform(svg.getScreenCTM().inverse()); return [p.x, p.y]; };
  let drag = null;
  svg.addEventListener('pointerdown', (ev) => {
    const t = ev.target.closest('[data-item],[data-wall],[data-cam],[data-room]'), p = pt(ev);
    if (!t) { hooks.select && hooks.select(null); return; }
    try { svg.setPointerCapture(ev.pointerId); } catch (e) { /* a synthetic pointer has nothing to capture */ }
    const g = 'g' + Date.now();
    if (t.dataset.item) {
      const it = store.item(t.dataset.item);
      hooks.select && hooks.select({ type: 'item', id: it.id });
      drag = { kind: 'item', id: it.id, off: [it.x - p[0], it.y - p[1]], g };
    } else if (t.dataset.wall) {
      const w = store.derived.wallBy[t.dataset.wall];
      hooks.select && hooks.select({ type: 'wall', id: w.id });
      drag = { kind: 'wall', id: w.id, p0: p, d0: w.shift, n: w.n, last: w.shift, g, told: false };
      liveDim = w.id; drawGeometry();
    } else if (t.dataset.cam) drag = { kind: 'cam' };
    else if (t.dataset.room) hooks.select && hooks.select({ type: 'room', id: t.dataset.room });
  });
  svg.addEventListener('pointermove', (ev) => {
    if (!drag) return;
    const p = pt(ev);
    if (drag.kind === 'item') store.apply({ op: 'item.move', id: drag.id, x: snap(p[0] + drag.off[0], 5), y: snap(p[1] + drag.off[1], 5) }, { gesture: drag.g });
    else if (drag.kind === 'wall') {
      const d = snap(drag.d0 + (p[0] - drag.p0[0]) * drag.n[0] + (p[1] - drag.p0[1]) * drag.n[1], 5);
      if (d === drag.last) return;
      const r = store.apply({ op: 'wall.shift', id: drag.id, d }, { gesture: drag.g });
      if (r.ok) { drag.last = d; drag.told = false; } else if (!drag.told) { drag.told = true; hooks.blocked && hooks.blocked(r); }
    } else if (drag.kind === 'cam') hooks.camMove && hooks.camMove(p);
  });
  const end = () => { if (drag && drag.kind === 'wall') { liveDim = null; drawGeometry(); } drag = null; };
  svg.addEventListener('pointerup', end); svg.addEventListener('pointercancel', end);

  store.on((e) => {
    if (e.type !== 'change') return;
    if (e.touched.geometry || e.touched.finishes.length) drawGeometry();
    for (const id of e.touched.items) drawItem(id);
  });
  drawGeometry(); drawItems();
  return {
    el: svg, setCamera,
    setSelection(s) { sel = s; drawGeometry(); drawItems(); },
  };
}
