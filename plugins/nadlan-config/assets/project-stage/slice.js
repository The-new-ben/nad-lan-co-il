/* FloorSlice (design system L9Nqz7Viv7K3MYeZrBc9s8 version 87, 28.9.2026): the picked floor as a plan. The owner: "to see
 * the plans... really able to look at it in various slices, various angles". No plan of the project is published, so the
 * slice draws what the stage knows (stage.floorPlan: the glass line and the balconies of that floor, from the model's own
 * numbers), an illustrative core, and the example apartments by their bearings, each in the page's words for that direction.
 * One floor up or down changes the balconies' wave, as on the model. A tap on an apartment picks it on the stage; the
 * floors that have rooms open the 360 room; the basket takes it. The caption says what is an illustration. */
const NS = 'http://www.w3.org/2000/svg';
let css = false;
function ensureCss() {
  if (css) return;
  css = true;
  const l = document.createElement('link');
  l.rel = 'stylesheet';
  l.href = new URL('./slice.css' + new URL(import.meta.url).search, import.meta.url).href;
  document.head.appendChild(l);
}
const el = (tag, cls, parent, attrs) => {
  const n = document.createElement(tag);
  if (cls) n.className = cls;
  for (const k in attrs || {}) n.setAttribute(k, attrs[k]);
  if (parent) parent.appendChild(n);
  return n;
};
const sv = (tag, attrs, parent) => {
  const n = document.createElementNS(NS, tag);
  for (const k in attrs || {}) n.setAttribute(k, attrs[k]);
  if (parent) parent.appendChild(n);
  return n;
};
const norm = (b) => ((Number(b) % 360) + 360) % 360;

/* o: { stage, floor, unit ('w'), tower ('N' on a two-tower stage, else null), units: [[id, bearing]], words(bearing) -> text,
 *      note, tourFloors: [25, ...], opener } */
export function openSlice(o) {
  ensureCss();
  const stage = o.stage;
  if (!stage || typeof stage.floorPlan !== 'function') return null;
  let floor = Number(o.floor) || 1;
  let unit = o.unit || null;
  const tower = o.tower ? String(o.tower) : null;
  const uid = (side) => (tower ? tower + '-' : '') + floor + '-' + side; // "25-w", or "N-25-w" on DUO
  const units = (o.units || []).map(([id, b]) => ({ id, b: norm(b) }));
  const words = typeof o.words === 'function' ? o.words : () => '';
  const prevFocus = o.opener || document.activeElement;
  // on a language page (HAD-361) the plan's own labels are put in the page's language before they are measured and
  // placed, and the direction words run outward on either side whatever the reading direction (1.72.350)
  const I18N = window.__nlStageI18n || null;
  const T = (s) => (I18N && typeof I18N.tr === 'function' && I18N.tr(s)) || s;
  const LTR = !!(I18N && I18N.lang !== 'he' && I18N.lang !== 'ar');

  const root = el('div', 'nlds nlsl', null, { role: 'dialog', 'aria-modal': 'true', 'aria-labelledby': 'nlsl-t', dir: LTR ? 'ltr' : 'rtl', lang: I18N ? I18N.lang : 'he' });
  const box = el('div', 'nlsl__box', root);
  const head = el('div', 'nlsl__head', box);
  const tt = el('div', 'nlsl__tt', head);
  el('p', 'nlsl__kick', tt).textContent = 'חתך הקומה · להמחשה';
  const title = el('h2', 'nlsl__title', tt, { id: 'nlsl-t' });
  const x = el('button', 'nlsl__x', head, { type: 'button', 'aria-label': 'סגירת החתך' });
  x.textContent = '×';
  const body = el('div', 'nlsl__body', box);
  const plan = el('div', 'nlsl__plan', body);
  const side = el('div', 'nlsl__side', body);
  const step = el('div', 'nlsl__step', side, { role: 'group', 'aria-label': 'קומה' });
  const up = el('button', 'nlsl__btn nlsl__btn--2', step, { type: 'button' });
  up.textContent = 'קומה למעלה';
  const dn = el('button', 'nlsl__btn nlsl__btn--2', step, { type: 'button' });
  dn.textContent = 'קומה למטה';
  const facts = el('p', 'nlsl__facts', side);
  const list = el('div', 'nlsl__units', side, { role: 'radiogroup', 'aria-label': 'דירה לדוגמה' });
  const acts = el('div', 'nlsl__acts', side);
  const inside = el('button', 'nlsl__btn', acts, { type: 'button' });
  inside.textContent = 'להיכנס לדירה · 360°';
  const toBasket = el('button', 'nlsl__btn nlsl__btn--2', acts, { type: 'button' });
  toBasket.textContent = 'לסל הדירה';
  el('p', 'nlsl__note', side).textContent = 'חתך להמחשה: קו החזית והמרפסות לפי הדגם של הבמה; הגרעין והחלוקה לדירות משוערים ואינם תוכנית מכר.' + (o.note ? ' ' + o.note : '');
  document.body.appendChild(root);
  document.documentElement.classList.add('nlsl-open');

  function draw() {
    const p = stage.floorPlan(floor, tower);
    if (!p) return;
    title.textContent = 'קומה ' + p.floor + (p.name ? ' · ' + p.name : '') + (p.penthouse ? ' · קומות הפנטהאוז' : '');
    // true on every stage (Rainbow's balconies wave floor by floor, DUO's sit at the corners and mid-face)
    facts.textContent = 'גובה העין כ־' + p.heightM + ' מ׳ מהרחוב · ' + (p.penthouse ? 'הקומה נסוגה מקו החזית, והמרפסות עמוקות יותר' : 'קו החזית והמרפסות כמו בדגם שעל הבמה');
    up.disabled = p.floor >= p.floors;
    dn.disabled = p.floor <= 1;
    // the plan: metres -> pixels, north up
    const all = p.outer.concat(p.glass);
    const R = Math.max(...all.map(([a, b]) => Math.hypot(a, b))) + 12; // room for the two-line direction words outside
    const S = 520, k = S / (2 * R), c0 = S / 2;
    const P = ([a, b]) => (c0 + a * k).toFixed(1) + ',' + (c0 - b * k).toFixed(1);
    plan.textContent = '';
    const svg = sv('svg', { viewBox: '0 0 ' + S + ' ' + S, role: 'img', 'aria-label': 'תוכנית להמחשה של קומה ' + p.floor }, plan);
    sv('rect', { width: S, height: S, fill: '#F6F2EA' }, svg);
    const cp = sv('clipPath', { id: 'nlsl-g' }, svg);
    sv('polygon', { points: p.glass.map(P).join(' ') }, cp);
    // the example apartments: wedges between the bearings' midpoints, inside the glass line
    const ids = [];
    units.forEach((u, i) => {
      const prev = units[(i - 1 + units.length) % units.length].b, next = units[(i + 1) % units.length].b;
      const a0 = u.b - norm(u.b - prev) / 2, a1 = u.b + norm(next - u.b) / 2;
      const pts = [[0, 0]];
      for (let j = 0; j <= 24; j++) {
        const a = (a0 + (a1 - a0) * j / 24) * Math.PI / 180;
        pts.push([Math.sin(a) * R * 1.5, Math.cos(a) * R * 1.5]);
      }
      const g = sv('g', { class: 'nlsl__u' + (u.id === unit ? ' is-on' : ''), 'data-u': u.id }, svg);
      sv('polygon', { points: pts.map(P).join(' '), 'clip-path': 'url(#nlsl-g)' }, g);
      ids.push(u.id);
    });
    // the balconies: the band between the glass line and its outer edge
    sv('path', { class: 'nlsl__bal', 'fill-rule': 'evenodd', d: 'M' + p.outer.map(P).join(' L') + ' Z M' + p.glass.slice().reverse().map(P).join(' L') + ' Z' }, svg);
    sv('polygon', { class: 'nlsl__glass', points: p.glass.map(P).join(' ') }, svg);
    sv('polygon', { class: 'nlsl__core', points: p.core.map(P).join(' ') }, svg);
    const ct = sv('text', { x: c0, y: c0 + 4, class: 'nlsl__coret', 'text-anchor': 'middle' }, svg);
    ct.textContent = T('גרעין');
    // labels: "דירה לדוגמה" midway between the core and the glass line on the apartment's bearing; the page's words for that
    // direction outside the balconies, facing out, in two lines when long, kept inside the picture
    const ray = (poly, a) => { // distance from the centre to the polygon along bearing a (radians)
      const dx = Math.sin(a), dy = Math.cos(a);
      let best = 0;
      for (let i = 0; i < poly.length; i++) {
        const [x1, y1] = poly[i], [x2, y2] = poly[(i + 1) % poly.length];
        const ex = x2 - x1, ey = y2 - y1, den = dx * ey - dy * ex;
        if (Math.abs(den) < 1e-9) continue;
        const t = (x1 * ey - y1 * ex) / den, u = (x1 * dy - y1 * dx) / den;
        if (t > 0 && u >= 0 && u <= 1) best = Math.max(best, t);
      }
      return best;
    };
    const lines = (w, max = 16) => {
      if (w.length <= max) return [w];
      if (w.startsWith('לכיוון ')) return ['לכיוון', w.slice(7)]; // never split a place's name
      const sp = [...w.matchAll(/ /g)].map((m) => m.index);
      const mid = sp.reduce((m, i) => (Math.abs(i - w.length / 2) < Math.abs(m - w.length / 2) ? i : m), sp[0] || w.length);
      return [w.slice(0, mid), w.slice(mid + 1)];
    };
    for (const u of units) {
      const a = u.b * Math.PI / 180, on = u.id === unit;
      const ri = (ray(p.core, a) + ray(p.glass, a)) / 2;
      const lab = T('דירה לדוגמה'), lls = lab.length > 12 ? lines(lab, 8) : [lab];
      const lx = (c0 + Math.sin(a) * ri * k).toFixed(1), ly = c0 - Math.cos(a) * ri * k + 4 - (lls.length - 1) * 6.5;
      const t1 = sv('text', { x: lx, y: ly.toFixed(1), class: 'nlsl__lab' + (on ? ' is-on' : ''), 'text-anchor': 'middle' }, svg);
      lls.forEach((l, i) => { const ts = sv('tspan', { x: lx, dy: i ? 13 : 0 }, t1); ts.textContent = l; });
      const w = words(u.b) ? T(words(u.b)) : '';
      if (!w) continue;
      const ls = lines(w), ro = ray(p.outer, a) + 2.2, sx = Math.sin(a);
      let x = c0 + sx * ro * k, y = c0 - Math.cos(a) * ro * k + 4;
      const wid = Math.max(...ls.map((l) => l.length)) * 6.4;
      // outward: on the east the text runs right of x, on the west left of it ('end' is the left edge in RTL, the
      // right edge in LTR)
      const east = sx > 0.35, west = sx < -0.35;
      const anchor = east ? (LTR ? 'start' : 'end') : (west ? (LTR ? 'end' : 'start') : 'middle');
      if (east) x = Math.min(x, S - 10 - wid);
      if (west) x = Math.max(x, 10 + wid);
      if (anchor === 'middle') y = Math.cos(a) > 0 ? Math.max(y - (ls.length - 1) * 15, 18) : Math.min(y, S - 44 - (ls.length - 1) * 15);
      const t2 = sv('text', { x: x.toFixed(1), y: y.toFixed(1), class: 'nlsl__dir' + (on ? ' is-on' : ''), 'text-anchor': anchor }, svg);
      ls.forEach((l, i) => { const ts = sv('tspan', { x: x.toFixed(1), dy: i ? 15 : 0 }, t2); ts.textContent = l; });
    }
    // north arrow and a 10 m bar
    const na = sv('g', { transform: 'translate(' + (S - 30) + ',36)' }, svg);
    sv('path', { d: 'M0,-18 L7,6 L0,1 L-7,6 Z', fill: '#14212B' }, na);
    const nt = sv('text', { y: 22, 'text-anchor': 'middle', class: 'nlsl__n' }, na);
    nt.textContent = T('צפון');
    sv('line', { x1: 24, y1: S - 22, x2: (24 + 10 * k).toFixed(1), y2: S - 22, stroke: '#14212B', 'stroke-width': 3 }, svg);
    const st = sv('text', { x: (24 + 5 * k).toFixed(1), y: S - 30, 'text-anchor': 'middle', class: 'nlsl__n' }, svg);
    st.textContent = T('10 מ׳');
    svg.querySelectorAll('.nlsl__u').forEach((g) => g.addEventListener('click', () => pickUnit(g.getAttribute('data-u'))));
    // the side list, the same apartments as buttons
    list.textContent = '';
    for (const u of units) {
      const b = el('button', 'nlsl__ub' + (u.id === unit ? ' is-on' : ''), list, { type: 'button', role: 'radio', 'aria-checked': u.id === unit ? 'true' : 'false' });
      el('b', null, b).textContent = 'דירה לדוגמה';
      el('span', null, b).textContent = words(u.b) || '';
      b.addEventListener('click', () => pickUnit(u.id));
    }
    const hasRoom = (o.tourFloors || []).includes(p.floor) && !!document.querySelector('.nlat__go');
    inside.hidden = !hasRoom || !unit;
    toBasket.hidden = !unit || !window.__nlBasket;
  }
  function pickUnit(id) {
    unit = id;
    try { stage.selectUnit(uid(id), 'user'); } catch (e) { /* the stage moves on its own */ }
    draw();
  }
  function goFloor(d) {
    floor += d;
    try { stage.selectFloor(floor, tower || undefined); window.dispatchEvent(new CustomEvent('nl:floor', { detail: { floor, heightM: stage.floorHeight(floor), tower } })); } catch (e) { /* none */ }
    if (unit) { try { stage.selectUnit(uid(unit), 'user'); } catch (e) { /* none */ } }
    draw();
  }
  up.addEventListener('click', () => goFloor(1));
  dn.addEventListener('click', () => goFloor(-1));
  inside.addEventListener('click', () => {
    const go = document.querySelector('.nlat__go');
    const dir = unit;
    close();
    if (!go) return;
    go.click();
    let n = 0;
    const t = setInterval(() => { // the viewer opens, then turns to this apartment's room
      n++;
      if (window.__nlTour && window.__nlTour.setView) { clearInterval(t); try { window.__nlTour.setView({ scene: dir }, 0); } catch (e) { /* none */ } }
      if (n > 40) clearInterval(t);
    }, 100);
  });
  toBasket.addEventListener('click', () => { close(); if (window.__nlBasket) window.__nlBasket.open(); });
  function close() {
    root.remove();
    document.documentElement.classList.remove('nlsl-open');
    document.removeEventListener('keydown', onKey);
    if (prevFocus && prevFocus.focus) prevFocus.focus();
  }
  const onKey = (e) => { if (e.key === 'Escape') close(); };
  document.addEventListener('keydown', onKey);
  x.addEventListener('click', close);
  root.addEventListener('click', (e) => { if (e.target === root) close(); });
  draw();
  x.focus();
  return { close, get floor() { return floor; }, get unit() { return unit; } };
}
