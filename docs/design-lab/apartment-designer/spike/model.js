// NadLan apartment designer core (HAD-703 spike, 10.11.2026).
// One apartment model (nadlan-apartment v1) + one buyer design (nadlan-unit-design v2), changed ONLY through operations.
// No DOM and no three.js here: the same file runs in the browser, in node tests and, later, on the co-design channel.
// Frame: centimetres, origin at the plan's top-left, x to the right, y down, rotation in degrees clockwise.

const sub = (a, b) => [a[0] - b[0], a[1] - b[1]];
const dot = (a, b) => a[0] * b[0] + a[1] * b[1];
const crs = (a, b) => a[0] * b[1] - a[1] * b[0];
const hyp = (a) => Math.hypot(a[0], a[1]);
const r1 = (v) => Math.round(v * 10) / 10;

export const WALL_KINDS = {
  facade: { he: 'קיר חזית', fixed: 'קיר החזית קבוע: החזית והחלונות שייכים לבניין כולו.' },
  structural: { he: 'קיר נושא', fixed: 'קיר נושא, חלק משלד הבניין. הוא לא זז.' },
  mamad: { he: 'קיר ממ״ד', fixed: 'קירות הממ״ד (המרחב המוגן) קבועים.' },
  rail: { he: 'מעקה', fixed: 'מעקה המרפסת קבוע.' },
  divider: { he: 'גבול בין חללים', fixed: 'זה גבול בין שני חללים פתוחים, אין כאן קיר להזיז.' },
  partition: { he: 'מחיצה', fixed: null },
};

export function emptyDesign(apt) {
  return {
    schema: 'nadlan-unit-design', v: 2,
    project: apt.unit.project, unit_id: apt.unit.unit_id, geometry_revision: apt.geometry_revision,
    frame: { units: 'cm', origin: 'plan-top-left', rot: 'deg-cw' },
    geometry: { walls: {} }, finishes: {}, items: [], notes: [], log: [], rev: 0,
  };
}

function pip(p, poly) { // point in polygon
  let inside = false;
  for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
    const a = poly[i], b = poly[j];
    if ((a[1] > p[1]) !== (b[1] > p[1]) && p[0] < ((b[0] - a[0]) * (p[1] - a[1])) / (b[1] - a[1]) + a[0]) inside = !inside;
  }
  return inside;
}

function findFaces(nodes, walls, rooms) {
  const out = {};
  const push = (u, v, w) => (out[u] = out[u] || []).push({ u, v, w, ang: Math.atan2(nodes[v][1] - nodes[u][1], nodes[v][0] - nodes[u][0]) });
  for (const w of walls) { if (w.L < 0.01) continue; push(w.a, w.b, w); push(w.b, w.a, w); }
  for (const k in out) out[k].sort((p, q) => p.ang - q.ang);
  const seen = new Set(), raw = [];
  const key = (h) => h.u + '>' + h.v + '>' + h.w.id;
  for (const k in out) for (const h0 of out[k]) {
    if (seen.has(key(h0))) continue;
    const ring = []; let h = h0, guard = 0;
    while (!seen.has(key(h)) && guard++ < 2000) {
      seen.add(key(h)); ring.push(h);
      const list = out[h.v], i = list.findIndex((x) => x.v === h.u && x.w === h.w);
      h = list[(i + 1) % list.length]; // the next wall around the corner: walks one face
    }
    const poly = ring.map((x) => nodes[x.u]); let A = 0;
    for (let i = 0; i < poly.length; i++) { const p = poly[i], q = poly[(i + 1) % poly.length]; A += p[0] * q[1] - q[0] * p[1]; }
    raw.push({ ring, poly, signed: A / 2 });
  }
  let outer = 0; raw.forEach((f, i) => { if (Math.abs(f.signed) > Math.abs(raw[outer].signed)) outer = i; });
  raw.splice(outer, 1); // the unbounded face is the largest one
  const near = (a, b) => Math.abs(a - b) < 0.5;
  return raw.filter((f) => Math.abs(f.signed) > 1).map((f, i) => {
    const inside = rooms.filter((r) => pip(r.at, f.poly)), room = inside[0] || null;
    const xs = f.poly.map((p) => p[0]), ys = f.poly.map((p) => p[1]);
    const bb = { x0: Math.min(...xs), y0: Math.min(...ys), x1: Math.max(...xs), y1: Math.max(...ys) };
    let half = 0; const side = { l: 0, r: 0, t: 0, b: 0 };
    for (const h of f.ring) {
      const w = h.w, t = w.t || 0, p = nodes[h.u], q = nodes[h.v]; half += (w.L * t) / 2;
      if (near(p[0], bb.x0) && near(q[0], bb.x0)) side.l = Math.max(side.l, t);
      if (near(p[0], bb.x1) && near(q[0], bb.x1)) side.r = Math.max(side.r, t);
      if (near(p[1], bb.y0) && near(q[1], bb.y0)) side.t = Math.max(side.t, t);
      if (near(p[1], bb.y1) && near(q[1], bb.y1)) side.b = Math.max(side.b, t);
    }
    const gross = Math.abs(f.signed) / 1e4;
    return {
      id: room ? room.id : 'void' + i, room, merged: inside.slice(1).map((r) => r.id), poly: f.poly,
      walls: [...new Set(f.ring.map((h) => h.w.id))], gross: r1(gross), net: r1(gross - half / 1e4), bb,
      clearW: Math.round(bb.x1 - bb.x0 - (side.l + side.r) / 2), clearD: Math.round(bb.y1 - bb.y0 - (side.t + side.b) / 2),
      perimeter: Math.round(f.ring.reduce((s, h) => s + h.w.L, 0)),
    };
  });
}

/** Everything both views draw is derived here, from the base apartment plus the design's geometry changes. */
export function derive(apt, design) {
  const nodes = {}, base = {};
  for (const k in apt.nodes) nodes[k] = [apt.nodes[k][0], apt.nodes[k][1]];
  const shifts = (design.geometry && design.geometry.walls) || {};
  for (const w of apt.walls) {
    const a = apt.nodes[w.a], v = sub(apt.nodes[w.b], a), L = hyp(v);
    base[w.id] = { dir: [v[0] / L, v[1] / L], n: [v[1] / L, -v[0] / L] };
    const d = +shifts[w.id] || 0;
    if (d) for (const k of [w.a, w.b]) { nodes[k][0] += base[w.id].n[0] * d; nodes[k][1] += base[w.id].n[1] * d; }
  }
  const walls = apt.walls.map((w) => {
    const pa = nodes[w.a], pb = nodes[w.b], v = sub(pb, pa), L = hyp(v), b = base[w.id];
    return {
      ...w, pa, pb, L, dir: L ? [v[0] / L, v[1] / L] : b.dir, n: b.n, baseDir: b.dir, shift: +shifts[w.id] || 0,
      slide: dot(sub(pa, apt.nodes[w.a]), b.dir), // how far the a-end slid along the wall's own line
      flipped: dot(v, b.dir) <= 0,
    };
  });
  const wallBy = Object.fromEntries(walls.map((w) => [w.id, w]));
  // a window or a door keeps its place in the building when the corner next to it moves
  const openings = apt.openings.map((o) => ({ ...o, at: o.at - wallBy[o.wall].slide }));
  for (const w of walls) w.openings = openings.filter((o) => o.wall === w.id).sort((p, q) => p.at - q.at);
  const faces = findFaces(nodes, walls, apt.rooms);
  return { nodes, walls, wallBy, openings, faces, faceBy: Object.fromEntries(faces.map((f) => [f.id, f])) };
}

const rej = (code, reason) => ({ code, reason });

/** A partition can slide only when both of its ends ride along walls that run across it (never out of a corner). */
export function canSlide(apt, id) {
  const w = apt.walls.find((x) => x.id === id);
  if (!w || WALL_KINDS[w.kind].fixed) return false;
  const v = sub(apt.nodes[w.b], apt.nodes[w.a]), n = [v[1], -v[0]];
  for (const k of [w.a, w.b]) for (const o of apt.walls) {
    if (o.id === id || (o.a !== k && o.b !== k)) continue;
    const ov = sub(apt.nodes[o.b], apt.nodes[o.a]);
    if (Math.abs(crs(ov, n)) / (hyp(ov) * hyp(n)) > 1e-6) return false;
  }
  return true;
}

function checkShift(apt, design, id, d) {
  const w0 = apt.walls.find((w) => w.id === id);
  if (!w0) return rej('wall.unknown', 'הקיר הזה לא מוכר.');
  const kind = WALL_KINDS[w0.kind];
  if (!kind || kind.fixed) return rej('wall.fixed.' + w0.kind, kind ? kind.fixed : 'הקיר הזה קבוע.');
  const next = { ...design, geometry: { walls: { ...design.geometry.walls, [id]: d } } };
  const dv = derive(apt, next), w = dv.wallBy[id], m = 10 + (w0.t || 0) / 2;
  for (const k of [w0.a, w0.b]) {
    for (const o of dv.walls) {
      if (o.id === id || (o.a !== k && o.b !== k)) continue;
      if (Math.abs(crs(o.baseDir, w.n)) > 1e-6) return rej('wall.corner', 'המחיצה מחוברת לפינה, והיא לא יכולה להחליק לכיוון הזה.');
      if (o.flipped || o.L < 30) return rej('wall.span', 'אין מקום: המחיצה הגיעה לקיר הסמוך.');
      for (const op of o.openings) {
        const hit = o.a === k ? op.at < m : op.at + op.w > o.L - m;
        if (hit) return rej('wall.opening', op.type === 'door' ? 'המחיצה נתקעת בדלת. הדלת נשארת במקומה.' : 'המחיצה נתקעת בחלון. החלונות שייכים לחזית ולא זזים.');
      }
    }
  }
  for (const f of dv.faces) {
    if (!f.room || !f.walls.includes(id)) continue;
    for (const r of apt.rules || []) {
      if (!r.applies.includes(f.room.type)) continue;
      if (r.code === 'room.min_width' && Math.min(f.clearW, f.clearD) < r.value) return rej(r.code, f.room.name_he + ': החדר יהיה צר מ-' + (r.value / 100).toFixed(2) + ' מ׳.');
      if (r.code === 'room.min_area' && f.net < r.value) return rej(r.code, f.room.name_he + ': החדר יהיה קטן מ-' + r.value + ' מ״ר.');
    }
  }
  return null;
}

export function createStore(apt, design0) {
  let design = JSON.parse(JSON.stringify(design0 || emptyDesign(apt)));
  let dv = derive(apt, design);
  const subs = new Set(), undo = [], redo = [], slideCache = {};
  const emit = (e) => subs.forEach((f) => f(e));
  const item = (id) => design.items.find((i) => i.id === id);
  const roomAt = (x, y) => { const f = dv.faces.find((q) => pip([x, y], q.poly)); return f ? f.id : null; };

  function check(op) {
    switch (op.op) {
      case 'item.add': return item(op.item.id) ? rej('item.exists', 'הפריט כבר קיים.') : roomAt(op.item.x, op.item.y) ? null : rej('item.outside', 'הפריט מחוץ לדירה.');
      case 'item.move': return !item(op.id) ? rej('item.unknown', 'הפריט לא נמצא.') : roomAt(op.x, op.y) ? null : rej('item.outside', 'הפריט מחוץ לדירה.');
      case 'item.rot': case 'item.remove': return item(op.id) ? null : rej('item.unknown', 'הפריט לא נמצא.');
      case 'finish.set': return /^floor:[a-z0-9_-]+$/.test(op.key) ? null : rej('finish.key', 'משטח לא מוכר.');
      case 'wall.shift': return checkShift(apt, design, op.id, op.d);
      default: return rej('op.unknown', 'פעולה לא מוכרת.');
    }
  }
  function inverse(op) {
    const it = op.id && item(op.id);
    switch (op.op) {
      case 'item.add': return { op: 'item.remove', id: op.item.id };
      case 'item.remove': return { op: 'item.add', item: { ...it } };
      case 'item.move': return { op: 'item.move', id: op.id, x: it.x, y: it.y };
      case 'item.rot': return { op: 'item.rot', id: op.id, rot: it.rot };
      case 'finish.set': return { op: 'finish.set', key: op.key, value: design.finishes[op.key] || null };
      case 'wall.shift': return { op: 'wall.shift', id: op.id, d: design.geometry.walls[op.id] || 0 };
    }
  }
  function mutate(op) {
    const t = { items: [], finishes: [], geometry: false };
    switch (op.op) {
      case 'item.add': design.items.push({ ...op.item, room: roomAt(op.item.x, op.item.y) }); t.items.push(op.item.id); break;
      case 'item.remove': design.items = design.items.filter((i) => i.id !== op.id); t.items.push(op.id); break;
      case 'item.move': { const it = item(op.id); it.x = op.x; it.y = op.y; it.room = roomAt(op.x, op.y); t.items.push(op.id); break; }
      case 'item.rot': item(op.id).rot = ((op.rot % 360) + 360) % 360; t.items.push(op.id); break;
      case 'finish.set': if (op.value) design.finishes[op.key] = op.value; else delete design.finishes[op.key]; t.finishes.push(op.key); break;
      case 'wall.shift':
        if (op.d) design.geometry.walls[op.id] = op.d; else delete design.geometry.walls[op.id];
        dv = derive(apt, design); t.geometry = true;
        for (const it of design.items) it.room = roomAt(it.x, it.y);
        break;
    }
    return t;
  }
  /** meta: { by, gesture, replay }. One drag is one gesture: one undo step and one line in the decision log. */
  function apply(op, meta = {}) {
    const t0 = typeof performance !== 'undefined' ? performance.now() : 0;
    const err = check(op);
    if (err) { emit({ type: 'reject', op, ...err }); return { ok: false, ...err }; }
    const inv = inverse(op), touched = mutate(op);
    design.rev += 1;
    if (!meta.replay) {
      const top = undo[undo.length - 1];
      if (meta.gesture && top && top.gesture === meta.gesture) top.redo = op;
      else { undo.push({ inv, redo: op, gesture: meta.gesture || null }); redo.length = 0; }
      const last = design.log[design.log.length - 1], entry = { n: design.rev, t: new Date().toISOString(), by: meta.by || 'buyer', op };
      if (meta.gesture && last && last.gesture === meta.gesture) Object.assign(last, entry, { gesture: meta.gesture });
      else design.log.push({ ...entry, gesture: meta.gesture || null });
    }
    emit({ type: 'change', op, touched, t0, by: meta.by || 'buyer' });
    if (t0) api.lastApplyMs = performance.now() - t0; // the model change plus both views patching themselves
    return { ok: true };
  }
  function step(from, to, pick) {
    const e = from.pop(); if (!e) return false;
    const r = apply(e[pick], { replay: true });
    if (r.ok) to.push(e);
    return r.ok;
  }
  const api = {
    lastApplyMs: 0, apt, apply, check,
    get design() { return design; }, get derived() { return dv; },
    item, roomAt,
    slides: (id) => (id in slideCache ? slideCache[id] : (slideCache[id] = canSlide(apt, id))),
    on: (f) => { subs.add(f); return () => subs.delete(f); },
    undo: () => step(undo, redo, 'inv'), redo: () => step(redo, undo, 'redo'),
    canUndo: () => undo.length > 0, canRedo: () => redo.length > 0,
    floorOf: (roomId) => design.finishes['floor:' + roomId] || (dv.faceBy[roomId] && dv.faceBy[roomId].room && dv.faceBy[roomId].room.floor) || null,
  };
  return api;
}

/** The bill of quantities is a pure function of the same model: no second source of truth. */
export function quantities(store) {
  const dv = store.derived, d = store.design;
  const rooms = dv.faces.filter((f) => f.room).map((f) => {
    const fin = store.floorOf(f.id);
    return { id: f.id, type: f.room.type, name: f.room.name_he, net: f.net, w: f.clearW, d: f.clearD, finish: fin, base: f.room.floor, changed: fin !== f.room.floor };
  });
  const floors = {};
  for (const r of rooms) floors[r.finish] = r1((floors[r.finish] || 0) + r.net);
  const items = {};
  for (const it of d.items) items[it.sku] = (items[it.sku] || 0) + 1;
  const inside = rooms.filter((r) => r.type !== 'balcony');
  return {
    rooms, floors, items,
    net: r1(inside.reduce((s, r) => s + r.net, 0)),
    balcony: r1(rooms.filter((r) => r.type === 'balcony').reduce((s, r) => s + r.net, 0)),
    moved: Object.keys(d.geometry.walls).length,
  };
}
