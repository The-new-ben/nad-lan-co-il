// The 2D plan view of the apartment designer (HAD-701; first proven as the HAD-703 spike): an SVG drawn from the store's derived model. It never keeps geometry of its own.
import { POINT_KINDS, nearWall, faceAt, interior } from './core.js';

const NS = 'http://www.w3.org/2000/svg';
const E = (tag, attrs, parent) => {
  const n = document.createElementNS(NS, tag);
  for (const k in attrs || {}) n.setAttribute(k, attrs[k]);
  if (parent) parent.appendChild(n);
  return n;
};
const P = (pts) => 'M' + pts.map((p) => p[0].toFixed(1) + ' ' + p[1].toFixed(1)).join('L') + 'Z';
const snap = (v, s) => Math.round(v / s) * s;
const r1 = (v) => Math.round(v * 10) / 10;
const TOUCH = 22, SYM = 7; // half of a 44 px touch target; the radius of a point's symbol, both in screen pixels

/** a services point drawn as a drafting symbol: the SHAPE tells the kind (local +y points into the room, away from the wall face) */
function symbol(g, kind, r) {
  if (kind === 'socket') { E('path', { d: 'M' + -r + ' 0A' + r + ' ' + r + ' 0 0 0 ' + r + ' 0Z' }, g); E('line', { x1: 0, y1: 0, x2: 0, y2: r * 0.62, class: 'in' }, g); }
  else if (kind === 'switch') { E('line', { x1: 0, y1: 0, x2: 0, y2: r * 1.05 }, g); E('circle', { cx: 0, cy: r * 1.5, r: r * 0.48 }, g); }
  else if (kind === 'light') { E('circle', { cx: 0, cy: 0, r }, g); const q = r * 0.7; E('path', { d: 'M' + -q + ' ' + -q + 'L' + q + ' ' + q + 'M' + q + ' ' + -q + 'L' + -q + ' ' + q, class: 'in' }, g); }
  else if (kind === 'data') E('rect', { x: -r * 0.6, y: r * 0.12, width: r * 1.2, height: r * 1.2 }, g);
  else if (kind === 'tv') { E('rect', { x: -r * 0.85, y: r * 0.12, width: r * 1.7, height: r * 1.7 }, g); E('circle', { cx: 0, cy: r * 0.97, r: r * 0.28, class: 'dot' }, g); }
  else if (kind === 'ac') E('rect', { x: -r * 1.7, y: 0, width: r * 3.4, height: r * 0.7 }, g);
}
export const symbolSvg = (kind, px = 30) => { // the same symbol for a button (a small standalone svg)
  const s = E('svg', { viewBox: '-15 -9 30 30', width: px, height: px, 'aria-hidden': 'true', class: 'sym' }), g = E('g', { class: 'pt base ' + kind, transform: kind === 'light' ? 'translate(0 6)' : '' }, s);
  if (kind !== 'light') E('line', { x1: -14, y1: 0, x2: 14, y2: 0, class: 'wl' }, s);
  symbol(g, kind, 8);
  return s;
};

export function mountPlan(host, store, cat, hooks = {}) {
  const apt = store.apt, T = hooks.T || {};
  const xs = Object.values(apt.nodes).map((p) => p[0]), ys = Object.values(apt.nodes).map((p) => p[1]);
  const vb = [Math.min(...xs) - 60, Math.min(...ys) - 60, Math.max(...xs) - Math.min(...xs) + 120, Math.max(...ys) - Math.min(...ys) + 120];
  const svg = E('svg', { class: 'nd-plan', viewBox: vb.join(' '), role: 'group', 'aria-label': T.plan || 'תוכנית הדירה' });
  host.appendChild(svg);
  const defs = E('defs', {}, svg);
  const hatch = E('pattern', { id: 'nd-mamad', width: 14, height: 14, patternUnits: 'userSpaceOnUse', patternTransform: 'rotate(45)' }, defs);
  E('rect', { width: 14, height: 14, fill: '#0F2233' }, hatch); E('line', { x1: 0, y1: 0, x2: 0, y2: 14, stroke: '#F2F5F7', 'stroke-width': 3 }, hatch);
  const L = {};
  for (const k of ['rooms', 'items', 'walls', 'open', 'ghost', 'labels', 'grips', 'points', 'notes', 'draft', 'cam']) L[k] = E('g', { class: 'L-' + k }, svg);
  let sel = null, liveDim = null, placing = null, partMode = false, notePlacing = false, seq = 0;
  const rn = (he) => (hooks.roomName ? hooks.roomName(he) : he); // a room's name in the page language
  const scale = () => { const m = svg.getScreenCTM(); return m && m.a > 0 ? m.a : 0.3; }; // screen pixels per cm
  const labelCache = new Map(); // the label point of a room outline, kept while the outline does not change (a drag redraws often)
  const labelAt = (f) => {
    const k = f.poly.map((p) => p[0].toFixed(0) + ',' + p[1].toFixed(0)).join(' ');
    if (!labelCache.has(k)) { if (labelCache.size > 400) labelCache.clear(); labelCache.set(k, interior(f)); }
    return labelCache.get(k);
  };
  const pip = (p, poly) => { let c = false; for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) { const a = poly[i], b = poly[j]; if ((a[1] > p[1]) !== (b[1] > p[1]) && p[0] < ((b[0] - a[0]) * (p[1] - a[1])) / (b[1] - a[1]) + a[0]) c = !c; } return c; };

  function drawGeometry() {
    const dv = store.derived;
    for (const k of ['rooms', 'walls', 'open', 'ghost', 'labels', 'grips']) L[k].textContent = '';
    const boxes = [], sr = (SYM * 1.8) / scale(); // the label boxes already placed, so two small rooms never print over each other
    for (const f of dv.faces) {
      if (!f.room) continue;
      const fin = cat.FINISHES[store.floorOf(f.id)] || {};
      E('path', { d: P(f.poly), class: 'room' + (f.room.fresh ? ' fresh' : '') + (sel && sel.type === 'room' && sel.id === f.id ? ' on' : ''), fill: fin.a || '#fff', 'fill-opacity': 0.5, 'data-room': f.id }, L.rooms);
      const small = f.bb.x1 - f.bb.x0 < 260, name = f.room.fresh && T.newSpace ? T.newSpace : rn(f.room.name_he);
      const dims = ((sel && sel.type === 'room' && sel.id === f.id) || (liveDim && f.walls.includes(liveDim))) && f.clearW != null; // a size only where it is true
      // the label stands at the point farthest from the walls (inside the room whatever its shape), then steps aside from
      // any point symbol and from the labels already placed
      const c0 = labelAt(f), half = Math.max(70, name.length * (small ? 11 : 12)), lo = small ? 40 : 50, hi = dims ? (small ? 72 : 94) : lo;
      const syms = dv.points.filter((q) => !q.lost).map((q) => centre(q, SYM / scale())); // every symbol: lights and wall points
      const box = (x, y) => ({ x0: x - half, x1: x + half, y0: y - 48, y1: y + hi });
      const free = (x, y, loose) => { // strict: the whole label inside the room; loose (a small room): its middle inside, it may overhang
        const b = box(x, y);
        if (loose ? !pip([x, y], f.poly) : ![[b.x0 + 10, y - 20], [b.x1 - 10, y - 20], [x, b.y1 - 10], [x, y - 40]].every((q) => pip(q, f.poly))) return false;
        if (syms.some((q) => q[0] > b.x0 - sr && q[0] < b.x1 + sr && q[1] > b.y0 - sr && q[1] < b.y1 + sr)) return false;
        return boxes.every((o) => b.x1 < o.x0 || b.x0 > o.x1 || b.y1 < o.y0 || b.y0 > o.y1);
      };
      let at = c0;
      const span = Math.max(120, (f.bb.x1 - f.bb.x0) / 2), dxs = [0];
      for (let x = 40; x <= span; x += 40) dxs.push(-x, x);
      search: for (const loose of [false, true]) for (const dy of [0, 40, -40, 80, -80, 120, -120, 160, -160]) for (const dx of dxs) if (free(c0[0] + dx, c0[1] + dy, loose)) { at = [c0[0] + dx, c0[1] + dy]; break search; }
      const [cx, cy] = at; boxes.push(box(cx, cy));
      const t = E('text', { x: cx, y: cy - 6, class: 'rl' + (small ? ' s' : '') + (f.room.fresh ? ' fresh' : '') }, L.labels); t.textContent = name;
      const a = E('text', { x: cx, y: cy + (small ? 30 : 40), class: 'ra' + (small ? ' s' : '') }, L.labels); a.textContent = f.net.toFixed(1) + ' ' + (T.sqm || 'מ״ר');
      if (dims) { const d = E('text', { x: cx, y: cy + (small ? 62 : 84), class: 'rd' }, L.labels); d.textContent = f.clearW + ' × ' + f.clearD; }
    }
    // a removed partition stays on the sheet as a thin dashed ghost, so the change is visible (and can be taken back)
    for (const w of dv.ghosts) {
      E('line', { x1: w.pa[0], y1: w.pa[1], x2: w.pb[0], y2: w.pb[1], class: 'ghost' + (sel && sel.type === 'wall' && sel.id === w.id ? ' on' : '') }, L.ghost);
      E('line', { x1: w.pa[0], y1: w.pa[1], x2: w.pb[0], y2: w.pb[1], class: 'hit free', 'data-wall': w.id }, L.grips);
    }
    for (const w of dv.walls) {
      const n = [-w.dir[1], w.dir[0]];
      if (w.kind === 'divider') { E('line', { x1: w.pa[0], y1: w.pa[1], x2: w.pb[0], y2: w.pb[1], class: 'wall divider' }, L.walls); }
      else {
        const t = Math.max(w.t, 6), e = w.kind === 'rail' ? 0 : t / 2, h = t / 2;
        const a = [w.pa[0] - w.dir[0] * e, w.pa[1] - w.dir[1] * e], b = [w.pb[0] + w.dir[0] * e, w.pb[1] + w.dir[1] * e];
        E('path', { d: P([[a[0] + n[0] * h, a[1] + n[1] * h], [b[0] + n[0] * h, b[1] + n[1] * h], [b[0] - n[0] * h, b[1] - n[1] * h], [a[0] - n[0] * h, a[1] - n[1] * h]]), class: 'wall ' + w.kind + (w.added ? ' added' : '') + (store.slides(w.id) ? ' free' : '') + (sel && sel.type === 'wall' && sel.id === w.id ? ' on' : '') }, L.walls);
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
      if (w.kind !== 'rail') E('line', { x1: w.pa[0], y1: w.pa[1], x2: w.pb[0], y2: w.pb[1], class: 'hit' + (free || w.added ? ' free' : ''), 'data-wall': w.id }, L.grips);
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
      if (c && c.shape === 'rug') L.items.insertBefore(g, L.items.firstChild); // a rug lies under the furniture: a finger on a sofa takes the sofa, whatever the order in the plan
      E('rect', { x: -c.w / 2, y: -c.d / 2, width: c.w, height: c.d, rx: c.shape === 'plant' ? c.w / 2 : 6, 'data-item': id }, g);
      if (c.shape !== 'rug' && c.shape !== 'plant') E('line', { x1: -c.w / 2 + 8, y1: -c.d / 2 + 9, x2: c.w / 2 - 8, y2: -c.d / 2 + 9, class: 'back' }, g);
      itemEls.set(id, g);
    }
    g.setAttribute('transform', 'translate(' + it.x + ' ' + it.y + ') rotate(' + it.rot + ')');
    g.setAttribute('class', 'item ' + c.shape + (sel && sel.type === 'item' && sel.id === id ? ' on' : ''));
  }
  const drawItems = () => { for (const id of [...itemEls.keys()]) drawItem(id); for (const it of store.design.items) drawItem(it.id); };

  // ---- services points: a symbol per point, sized in screen pixels so it reads the same on a phone and on a desk ----
  const centre = (q, r) => (POINT_KINDS[q.kind].ceiling ? [q.x, q.y] : [q.fx + q.ns[0] * r * 0.9, q.fy + q.ns[1] * r * 0.9]);
  function drawPoints() {
    L.points.textContent = '';
    const r = SYM / scale();
    for (const p of store.derived.points) {
      if (p.lost) continue;
      const wallPt = !POINT_KINDS[p.kind].ceiling, on = sel && sel.type === 'point' && sel.id === p.id;
      const tr = wallPt ? 'translate(' + p.fx.toFixed(1) + ' ' + p.fy.toFixed(1) + ') rotate(' + ((Math.atan2(-p.ns[0], p.ns[1]) * 180) / Math.PI).toFixed(1) + ')' : 'translate(' + p.x + ' ' + p.y + ')';
      const g = E('g', { class: 'pt ' + p.kind + ' ' + p.state + (on ? ' on' : ''), transform: tr, 'data-point': p.id }, L.points);
      if (on) E('circle', { cx: 0, cy: wallPt ? r * 0.9 : 0, r: r * 2.2, class: 'halo' }, g);
      symbol(g, p.kind, r);
    }
  }
  // ---- notes to the builder (HAD-792): a red numbered tag, the redline of a drawing, the same size on any screen ----
  function drawNotes() {
    L.notes.textContent = '';
    const k = scale(), s = 15 / k;
    (store.design.notes || []).forEach((n, i) => {
      const on = sel && sel.type === 'note' && sel.id === n.id, g = E('g', { class: 'nt' + (on ? ' on' : ''), transform: 'translate(' + n.x + ' ' + n.y + ')', 'data-note': n.id }, L.notes);
      if (on) E('circle', { r: s * 2, class: 'halo', 'data-note': n.id }, g);
      E('rect', { x: -s, y: -s, width: s * 2, height: s * 2, 'data-note': n.id }, g);
      const t = E('text', { x: 0, y: s * 0.42, 'font-size': (s * 1.25).toFixed(1), 'data-note': n.id }, g); t.textContent = String(i + 1);
      E('circle', { r: s * 2.4, class: 'nthit', 'data-note': n.id }, g);
    });
  }
  const nearestPoint = (p) => {
    const k = scale(), r = SYM / k; let best = null;
    for (const q of store.derived.points) { if (q.lost) continue; const c = centre(q, r), d = Math.hypot(c[0] - p[0], c[1] - p[1]) * k; if (d <= TOUCH && (!best || d < best.d)) best = { q, d }; }
    return best;
  };
  /** where a point of this kind lands for a finger at p: a light where the finger is, a wall point on the nearest wall face, on the finger's side */
  function pointTarget(kind, p) {
    if (POINT_KINDS[kind].ceiling) return { x: snap(p[0], 5), y: snap(p[1], 5) };
    const dv = store.derived, nw = nearWall(dv, p), w = nw.w, at = Math.max(0, Math.min(w.L, snap(nw.s, 5))), t = (w.t || 0) / 2;
    const f = faceAt(dv, [w.pa[0] + w.dir[0] * at + w.n[0] * nw.side * (t + 8), w.pa[1] + w.dir[1] * at + w.n[1] * nw.side * (t + 8)]);
    return { wall: w.id, at: r1(at + w.slide), room: f ? f.id : null };
  }
  function placeAt(kind, p) {
    const id = 'pt' + Date.now().toString(36) + (++seq);
    const r = store.apply({ op: 'point.add', point: { id, kind, ...pointTarget(kind, p) } });
    placing = null;
    if (r.ok) hooks.select && hooks.select({ type: 'point', id }); else hooks.blocked && hooks.blocked(r);
    hooks.modeDone && hooks.modeDone();
  }

  // ---- a new partition: from a point on a wall, straight out (at a right angle, or in line), to another wall or a free end ----
  const draft = { line: null, text: null };
  function startPart(p) {
    const k = scale(), nw = nearWall(store.derived, p);
    if (!nw || nw.d > (nw.w.t || 0) / 2 + TOUCH / k) { hooks.blocked && hooks.blocked({ code: 'partition.free', reason: (T.rules || {})['partition.free'] || '' }); return null; }
    const w = nw.w, s = Math.max(0, Math.min(w.L, snap(nw.s, 5)));
    return { kind: 'part', w, a: [w.pa[0] + w.dir[0] * s, w.pa[1] + w.dir[1] * s], b: null, len: 0 };
  }
  function movePart(p) {
    const dv = store.derived, k = scale(), w = drag.w, a = drag.a, v = [p[0] - a[0], p[1] - a[1]];
    let d = null, best = -Infinity;
    for (const c of [[-w.dir[1], w.dir[0]], [w.dir[1], -w.dir[0]], w.dir, [-w.dir[0], -w.dir[1]]]) { const x = c[0] * v[0] + c[1] * v[1]; if (x > best) { best = x; d = c; } }
    let len = snap(Math.max(0, best), 5), hit = Infinity;
    for (const o of dv.walls) { // the first wall straight ahead: the partition stops on it
      if (o === w || o.L < 1) continue;
      const den = d[0] * o.dir[1] - d[1] * o.dir[0]; if (Math.abs(den) < 1e-9) continue;
      const q = [o.pa[0] - a[0], o.pa[1] - a[1]], t = (q[0] * o.dir[1] - q[1] * o.dir[0]) / den, u = (q[0] * d[1] - q[1] * d[0]) / den;
      if (u >= -0.5 && u <= o.L + 0.5 && t > 1 && t < hit) hit = t;
    }
    if (len >= hit - TOUCH / k) len = hit; // close to the wall ahead: it lands on it
    len = Math.min(len, hit);
    Object.assign(drag, { d, len, b: [a[0] + d[0] * len, a[1] + d[1] * len] });
    L.draft.textContent = '';
    if (len < 1) return;
    E('line', { x1: a[0], y1: a[1], x2: drag.b[0], y2: drag.b[1], class: 'draft' }, L.draft);
    const nn = [-d[1], d[0]], off = 34 / k, m = [(a[0] + drag.b[0]) / 2 + nn[0] * off, (a[1] + drag.b[1]) / 2 + nn[1] * off];
    const tx = E('text', { x: m[0], y: m[1], class: 'rd live', style: 'font-size:' + (15 / k).toFixed(1) + 'px' }, L.draft); tx.textContent = Math.round(len) + ' ' + (T.cm || 'ס״מ');
  }
  function endPart() {
    L.draft.textContent = '';
    partMode = false;
    if (drag.len >= 1) {
      const id = 'np' + Date.now().toString(36) + (++seq);
      const r = store.apply({ op: 'partition.add', wall: { id, a: [r1(drag.a[0]), r1(drag.a[1])], b: [r1(drag.b[0]), r1(drag.b[1])], t: 10 } });
      if (r.ok) hooks.select && hooks.select({ type: 'wall', id }); else hooks.blocked && hooks.blocked(r);
    }
    hooks.modeDone && hooks.modeDone();
  }

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
  const capture = (ev) => { try { svg.setPointerCapture(ev.pointerId); } catch (e) { /* a synthetic pointer has nothing to capture */ } };
  let drag = null;
  svg.addEventListener('pointerdown', (ev) => {
    const p = pt(ev), g = 'g' + Date.now();
    if (notePlacing) { capture(ev); drag = { kind: 'note-place', at: p }; return; }
    if (placing) { capture(ev); drag = { kind: 'place', at: p }; return; }
    const tn = ev.target.closest('[data-note]');
    if (tn) { capture(ev); const n = store.note(tn.dataset.note); hooks.select && hooks.select({ type: 'note', id: n.id }); drag = { kind: 'note', id: n.id, off: [n.x - p[0], n.y - p[1]], p0: p, g, moved: false }; return; }
    if (partMode) { drag = startPart(p); if (drag) capture(ev); return; }
    const t = ev.target.closest('[data-item],[data-wall],[data-cam],[data-room]'), grip = ev.target.closest('.grip');
    const np = !grip && nearestPoint(p);
    if (np && !(t && t.dataset.item && np.d > 10)) { // a point wins a touch within 22 px; over a piece of furniture only when the finger is right on it
      capture(ev); hooks.select && hooks.select({ type: 'point', id: np.q.id });
      if (np.q.state !== 'removed') drag = { kind: 'point', id: np.q.id, p0: p, g, told: false, moved: false };
      return;
    }
    if (!t) { hooks.select && hooks.select(null); return; }
    capture(ev);
    if (t.dataset.item) {
      const it = store.item(t.dataset.item);
      hooks.select && hooks.select({ type: 'item', id: it.id });
      drag = { kind: 'item', id: it.id, off: [it.x - p[0], it.y - p[1]], g };
    } else if (t.dataset.wall) {
      const id = t.dataset.wall;
      hooks.select && hooks.select({ type: 'wall', id });
      if (store.isAdded(id) || store.isRemoved(id)) return; // a new or a removed partition is chosen, not dragged
      const w = store.derived.wallBy[id];
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
    } else if (drag.kind === 'point') {
      if (!drag.moved && Math.hypot(p[0] - drag.p0[0], p[1] - drag.p0[1]) * scale() < 4) return;
      drag.moved = true;
      const q = store.point(drag.id), to = pointTarget(q.kind, p);
      if (POINT_KINDS[q.kind].ceiling ? to.x === q.x && to.y === q.y : to.wall === q.wall && to.at === q.at && to.room === q.room) return;
      const r = store.apply({ op: 'point.move', id: drag.id, ...to }, { gesture: drag.g });
      if (r.ok) drag.told = false; else if (!drag.told) { drag.told = true; hooks.blocked && hooks.blocked(r); }
    } else if (drag.kind === 'part') movePart(p);
    else if (drag.kind === 'place' || drag.kind === 'note-place') drag.at = p;
    else if (drag.kind === 'note') {
      if (!drag.moved && Math.hypot(p[0] - drag.p0[0], p[1] - drag.p0[1]) * scale() < 6) return;
      drag.moved = true;
      store.apply({ op: 'note.move', id: drag.id, x: snap(p[0] + drag.off[0], 5), y: snap(p[1] + drag.off[1], 5) }, { gesture: drag.g });
    }
    else if (drag.kind === 'cam') hooks.camMove && hooks.camMove(p);
  });
  const end = () => {
    if (!drag) return;
    const d = drag; drag = null;
    if (d.kind === 'wall') { liveDim = null; drawGeometry(); }
    if (d.kind === 'place' && placing) placeAt(placing, d.at);
    if (d.kind === 'note-place' && notePlacing) { notePlacing = false; svg.classList.remove('placing'); hooks.notePlace && hooks.notePlace([snap(d.at[0], 5), snap(d.at[1], 5)]); hooks.modeDone && hooks.modeDone(); }
    if (d.kind === 'part') { drag = d; endPart(); drag = null; }
  };
  svg.addEventListener('pointerup', end); svg.addEventListener('pointercancel', end);

  store.on((e) => {
    if (e.type !== 'change') return;
    if (e.touched.all) { drawGeometry(); drawItems(); drawPoints(); drawNotes(); return; }
    if (e.touched.notes && e.touched.notes.length) drawNotes();
    if (e.touched.geometry || e.touched.finishes.length || (e.touched.points && e.touched.points.length)) drawGeometry(); // labels step aside from lights
    for (const id of e.touched.items) drawItem(id);
    if (e.touched.geometry || (e.touched.points && e.touched.points.length)) drawPoints();
  });
  new ResizeObserver(() => { drawPoints(); drawNotes(); }).observe(svg); // the symbols keep their size on the screen
  drawGeometry(); drawItems(); drawPoints(); drawNotes();
  return {
    el: svg, setCamera, scale,
    setSelection(s) { sel = s; drawGeometry(); drawItems(); drawPoints(); drawNotes(); },
    /** the next tap places a point of this kind (null: stop) */
    setPlacing(kind) { placing = kind || null; partMode = false; notePlacing = false; svg.classList.toggle('placing', !!placing); },
    /** the next drag draws a new partition */
    setPartMode(on) { partMode = !!on; placing = null; notePlacing = false; svg.classList.toggle('placing', partMode); },
    /** the next tap pins a note to the builder there (hooks.notePlace receives the place) */
    setNotePlacing(on) { notePlacing = !!on; placing = null; partMode = false; svg.classList.toggle('placing', notePlacing); },
    get mode() { return placing ? 'place' : partMode ? 'part' : notePlacing ? 'note' : null; },
    noteScreen(id) { const n = store.note(id); return n ? this.screenOf(n.x, n.y) : null; },
    /** for checks: where a plan point is on the screen */
    screenOf(x, y) { const q = new DOMPoint(x, y).matrixTransform(svg.getScreenCTM()); return [q.x, q.y]; },
    pointScreen(id) { const q = store.point(id); if (!q) return null; const c = centre(q, SYM / scale()); return this.screenOf(c[0], c[1]); },
  };
}
