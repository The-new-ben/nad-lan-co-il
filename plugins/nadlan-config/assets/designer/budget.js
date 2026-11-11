// The budget estimate of the apartment designer (HAD-705). A pure function of the same model the plan and the 3D draw,
// priced with published Israeli price RANGES (data/price-ranges.json; sources stay in the repo's research folder, never on the page).
// It is an estimate from published prices, never a quote, and it says which lines are rough.

/** the range to show for one price record: where most sources sit when known, else the full published span */
export function span(p) {
  if (!p) return null;
  const typical = p.typical_low != null && p.typical_high != null;
  return { lo: typical ? p.typical_low : p.low, hi: typical ? p.typical_high : p.high, rough: !typical || p.confidence === 'low' };
}

/** the price range of one catalogue piece: per unit, or per running metre of its width */
export function itemRange(c, prices) {
  if (!c || !c.price || !prices) return null;
  if (typeof c.price === 'string') return span(prices[c.price]);
  let lo = 0, hi = 0, rough = false;
  for (const id of c.price.per_m) { const s = span(prices[id]); if (!s || s.hi == null) return null; lo += s.lo * (c.w / 100); hi += s.hi * (c.w / 100); rough = rough || s.rough; }
  return { lo, hi, rough };
}

const down = (v, step) => Math.floor(v / step) * step, up = (v, step) => Math.ceil(v / step) * step;
export const tidy = (r) => (r ? { ...r, lo: down(r.lo, 50), hi: r.hi == null ? null : up(r.hi, 50) } : null);

export function estimate(store, cat, prices) {
  const rows = [], missing = [];
  if (!prices) return { rows, missing, lo: 0, hi: 0, open: false, ready: false };
  for (const f of store.derived.faces) { // only floors the buyer changed: the base floor is part of the apartment
    if (!f.room) continue;
    const key = store.floorOf(f.id), fin = cat.FINISHES[key];
    if (!fin || key === f.room.floor) continue;
    const s = span(prices[fin.price]);
    if (!s) { missing.push(fin.he); continue; }
    rows.push({ kind: 'floor', label: fin.he, where: f.room.name_he, qty: f.net, lo: s.lo * f.net, hi: s.hi == null ? null : s.hi * f.net, rough: s.rough });
  }
  const byPiece = {};
  for (const it of store.design.items) (byPiece[it.sku] = byPiece[it.sku] || []).push(it);
  for (const sku in byPiece) {
    const c = cat.ITEMS[sku], n = byPiece[sku].length, s = itemRange(c, prices);
    if (!s) { missing.push(c.he); continue; }
    rows.push({ kind: 'item', label: c.he, qty: n, lo: s.lo * n, hi: s.hi == null ? null : s.hi * n, rough: s.rough });
  }
  const open = rows.some((r) => r.hi == null);
  return {
    rows: rows.map(tidy), missing, open, ready: true,
    lo: down(rows.reduce((a, r) => a + r.lo, 0), 100), hi: up(rows.reduce((a, r) => a + (r.hi == null ? r.lo : r.hi), 0), 100),
    rough: rows.filter((r) => r.rough).length,
  };
}
