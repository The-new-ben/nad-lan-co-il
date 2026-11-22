// The design order (HAD-792): one structured object per apartment, readable like a product order, that the buying journey's
// basket (package 4) takes in. Contract: side-session-notes/<group>/pkg2-contracts-designer-order-and-call.md
//   schema 'nadlan-design-order' v 1; saved under localStorage[ORDER_KEY] = { orders: { '<project|source>|<unit>': order }, last }
//   events on window: 'nadlan:design-order' (the buyer pressed "add to my basket"), 'nadlan:design-order-updated' (autosave)
// Nothing personal is inside: no name, phone or mail. A number that is not known is left out, never written as 0.
export const ORDER_KEY = 'nl-design-order:v1';
const clean = (s, n) => String(s == null ? '' : s).replace(/[<>"'`\\]/g, '').replace(/\s+/g, ' ').trim().slice(0, n);
const r1 = (v) => Math.round(v * 10) / 10;

export function orderKey(o) { return (o.project.slug || o.source) + '|' + (o.unit.id || '-'); }

export function buildOrder({ store, apt, catalog, T, lang, meta = {}, services = [], budget, roomName, quantities: q }) {
  const dv = store.derived, d = store.design, L = (rec) => catalog.label(rec, lang);
  const faceName = (id) => { const f = id && dv.faceBy[id]; return f && f.room ? (f.room.fresh ? T.newSpace : roomName(f.room.name_he)) : ''; };
  const slug = clean(meta.project && meta.project.slug, 60).toLowerCase().replace(/[^a-z0-9-]/g, '');
  const source = meta.source || (apt.source && apt.source.kind === 'own' ? 'mine' : slug ? 'project' : 'example');
  const unitId = clean((meta.unit && meta.unit.id) || apt.unit.unit_id || apt.id || '', 40).replace(/[^A-Za-z0-9_.-]/g, '');
  const rooms = q.rooms.map((r) => ({ id: r.id, name: r.fresh ? T.newSpace : roomName(r.name), type: r.type, ...(r.net ? { area_m2: r1(r.net) } : {}) }));
  const finishes = [];
  for (const r of q.rooms) {
    if (r.changed && r.finish && catalog.FINISHES[r.finish]) finishes.push({ room: r.id, roomName: faceName(r.id), surface: 'floor', id: r.finish, label: L(catalog.FINISHES[r.finish]) });
    const wk = store.wallOf ? store.wallOf(r.id) : null;
    if (wk && catalog.WALLS && catalog.WALLS[wk]) finishes.push({ room: r.id, roomName: faceName(r.id), surface: 'wall', id: wk, label: L(catalog.WALLS[wk]) });
  }
  const changes = [];
  const pa = q.partitions;
  if (pa.added.ids.length) changes.push({ kind: 'partition-add', label: T.chPartAdd + (pa.added.ids.length > 1 ? ' ×' + pa.added.ids.length : ''), qty: pa.added.m.toFixed(2) + ' ' + T.m, length_m: pa.added.m });
  if (pa.removed.ids.length) changes.push({ kind: 'partition-remove', label: T.chPartGone + (pa.removed.ids.length > 1 ? ' ×' + pa.removed.ids.length : ''), qty: pa.removed.m.toFixed(2) + ' ' + T.m, length_m: pa.removed.m });
  if (q.moved) changes.push({ kind: 'wall-move', label: T.chWall, qty: '×' + q.moved, count: q.moved });
  for (const k in q.points) for (const st of ['added', 'moved', 'removed']) {
    const n = q.points[k][st]; if (!n) continue;
    changes.push({ kind: st === 'added' ? 'point-add' : st === 'moved' ? 'point-move' : 'point-remove', point: k, label: T.pointName[k] + ' · ' + T.chPt[st], qty: '×' + n, count: n });
  }
  const items = Object.keys(q.items).map((sku) => {
    const c = catalog.ITEMS[sku]; if (!c) return null;
    const rooms_ = [...new Set(d.items.filter((i) => i.sku === sku).map((i) => i.room).filter(Boolean))].map(faceName).filter(Boolean);
    return { id: sku, label: L(c), count: q.items[sku], ...(rooms_.length ? { roomName: rooms_.join(', ') } : {}) };
  }).filter(Boolean);
  const notes = (d.notes || []).map((n) => ({ id: n.id, room: n.room || null, roomName: faceName(n.room), x: n.x, y: n.y, text: n.text, at: n.at }));
  const svc = services.filter((k) => T.services && T.services[k]).map((k) => ({ id: k, label: T.services[k] }));
  const now = new Date().toISOString();
  const o = {
    schema: 'nadlan-design-order', v: 1,
    id: 'do-' + (slug || source) + '-' + (unitId || 'apt').toLowerCase(), rev: d.rev || 0, created: now, updated: now, lang,
    project: { slug, title: clean(meta.project && meta.project.title, 80) },
    unit: { id: unitId, label: clean((meta.unit && meta.unit.label) || T.sub(apt.unit.rooms, q.net.toFixed(1), q.balcony ? q.balcony.toFixed(1) : ''), 120), ...(apt.unit.rooms ? { rooms: apt.unit.rooms } : {}), ...(q.net ? { area_m2: q.net } : {}) },
    source, rooms, finishes, changes, items, notes, services: svc,
  };
  if (budget && budget.ready && budget.lo) o.budget = { min: budget.lo, max: budget.open || budget.hi == null ? null : budget.hi, currency: 'ILS' };
  try {
    const base = location.origin + '/tour/designer/';
    o.link = meta.link || (slug ? base + '?project=' + encodeURIComponent(slug) + (unitId ? '&unit=' + encodeURIComponent(unitId) : '') + (lang !== 'he' ? '&lang=' + lang : '') : base + (lang !== 'he' ? '?lang=' + lang : ''));
  } catch (e) { /* no address outside a page */ }
  return o;
}

function readAll() {
  try { const x = JSON.parse(localStorage.getItem(ORDER_KEY) || 'null'); if (x && typeof x === 'object' && x.orders) return x; } catch (e) { /* unreadable: start a new list */ }
  return { orders: {}, last: null };
}
/** keeps the order (one per apartment, the newest wins). quiet: an autosave, which only refreshes an order already in the basket */
export function saveOrder(o, quiet) {
  try {
    const all = readAll(), k = orderKey(o), prev = all.orders[k];
    if (quiet && !prev) return false;
    if (prev && prev.created) o.created = prev.created;
    all.orders[k] = o; all.last = k;
    const keys = Object.keys(all.orders); if (keys.length > 20) delete all.orders[keys[0]]; // a basket, not an archive
    localStorage.setItem(ORDER_KEY, JSON.stringify(all));
    return true;
  } catch (e) { return false; }
}
export function readOrders() { return readAll(); }
