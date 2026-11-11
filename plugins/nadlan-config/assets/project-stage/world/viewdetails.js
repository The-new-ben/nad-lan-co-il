/* Kikar HaMedina: "View with details" / "נוף עם פירוט" (HAD-712, Ben 11.11.2026 night: "the view with details ... one on top of the
 * other"). The names of the places a window looks at, drawn over the rendered window view itself, each where the place really is.
 *
 * The window views (hamedina/views/*.webp, 16:9) were rendered by scripts/interior/render_kikar_views.py with kikar_interior.py's
 * "view" camera: horizontal field of view 70 degrees, pitched 4 degrees down, the eye 1.6 m over the floor, floor f at (f-1)*4 m.
 * This projects each landmark of world.json (the old 3D stage's window labels) and a few nearby stations, parks and shops of
 * places.json (hamedina/details.json, built by scripts/kikar/build_details_data.py) through that camera, then maps the point
 * onto the picture as the page shows it (object-fit: cover). Distances are straight lines from the tower; walking minutes are the
 * data's own. Nothing loads but one small JSON; the live 3D stays a separate tap.
 *
 *   const d = await viewDetails(imgEl, { data: url, lang: 'he'|'en'|'fr' });  d.set({ tower: 'B', floor: 24, bearing: 37.4 });
 *   d.show(true|false);  d.destroy(); */
const DEG = Math.PI / 180;
const W = {
  he: { km: (v) => `כ-${v} ק״מ`, m: (v) => `כ-${v} מ׳`, walk: (n) => `${n} דק׳ הליכה`, aria: 'שמות המקומות בכיוון הזה, עם המרחק', loc: 'he-IL' },
  en: { km: (v) => `about ${v} km`, m: (v) => `about ${v} m`, walk: (n) => `${n} min walk`, aria: 'Names of the places in this direction, with the distance', loc: 'en-GB' },
  fr: { km: (v) => `environ ${v} km`, m: (v) => `environ ${v} m`, walk: (n) => `${n} min à pied`, aria: 'Les lieux dans cette direction, avec la distance', loc: 'fr-FR' },
};
let CSS_DONE = false;
function css() {
  if (CSS_DONE) return; CSS_DONE = true;
  const s = document.createElement('style'); s.id = 'nlvd-css';
  s.textContent = '.nlvd{position:absolute;inset:0;pointer-events:none;overflow:hidden}'
    + '.nlvd__i{position:absolute;transform:translate(-50%,-100%);display:flex;flex-direction:column;align-items:center}'
    + '.nlvd__b{background:rgba(13,33,41,.88);border:1px solid #7fd3e6;border-radius:9px;padding:3px 8px;color:#fff;font:600 12.5px/1.25 Assistant,Heebo,system-ui,sans-serif;white-space:nowrap;max-width:46vw;overflow:hidden;text-overflow:ellipsis;text-align:center}'
    + '.nlvd__b small{display:block;font-weight:400;font-size:11.5px;color:#cfe3ea}'
    + '.nlvd__s{width:1.5px;background:#7fd3e6}.nlvd__d{width:7px;height:7px;border-radius:50%;background:#7fd3e6;box-shadow:0 0 0 2px rgba(13,33,41,.7)}'
    + '.nlvd--off{display:none}';
  document.head.appendChild(s);
}
const cache = {};
async function load(url) { if (!cache[url]) cache[url] = fetch(url).then((r) => r.json()); return cache[url]; }

export async function viewDetails(img, opt) {
  css();
  const D = await load(opt.data);
  const lang = W[opt.lang] ? opt.lang : 'he';
  const T = W[lang];
  const nf = (v, d) => new Intl.NumberFormat(T.loc, { maximumFractionDigits: d, minimumFractionDigits: d }).format(v);
  const host = img.parentElement;
  if (getComputedStyle(host).position === 'static') host.style.position = 'relative';
  const layer = document.createElement('div'); layer.className = 'nlvd'; layer.setAttribute('role', 'img'); layer.setAttribute('aria-label', T.aria);
  host.appendChild(layer);
  let cur = null, on = true;

  function project() {
    layer.textContent = '';
    if (!cur || !on || !img.naturalWidth) return;
    const t = D.towers[cur.tower]; if (!t) return;
    const nw = img.naturalWidth, nh = img.naturalHeight;
    const bw = img.clientWidth, bh = img.clientHeight; if (!bw || !bh) return;
    const s = Math.max(bw / nw, bh / nh), ox = (bw - nw * s) / 2, oy = (bh - nh * s) / 2;
    const b = cur.bearing * DEG, p = D.cam.pitch * DEG, f = (nw / 2) / Math.tan(D.cam.hfov / 2 * DEG);
    const eye = D.cam.eye0 + (Math.max(1, cur.floor) - 1) * D.cam.storey;
    const camE = t.cx + 15 * Math.sin(b), camN = -t.cz + 15 * Math.cos(b); // the eye stands at the glass, about 15 m from the core
    const F = [Math.sin(b) * Math.cos(p), Math.cos(b) * Math.cos(p), Math.sin(p)], R = [Math.cos(b), -Math.sin(b), 0];
    const U = [-Math.sin(b) * Math.sin(p), -Math.cos(b) * Math.sin(p), Math.cos(p)];
    const dot = (a, c) => a[0] * c[0] + a[1] * c[1] + a[2] * c[2];
    const all = D.marks.map((m) => ({ ...m, mark: 1 })).concat(D.places);
    const pts = [];
    for (const q of all) {
      const name = q[lang] || q.en; if (!name) continue;
      const dE = q.x - camE, dN = -q.z - camN, dist = Math.hypot(dE, dN);
      if (dist < 200) continue;
      const v = [dE, dN, (q.h ? q.h * 0.8 : 0) - eye];
      const zc = dot(v, F); if (zc <= 0) continue;
      const px = nw / 2 + f * dot(v, R) / zc, py = nh / 2 - f * dot(v, U) / zc;
      const x = ox + px * s, y = oy + py * s;
      if (x < 8 || x > bw - 8 || y < 30 || y > bh - 4) continue;
      const meta = q.walk && q.walk <= 15 ? T.walk(nf(q.walk, 0)) : dist >= 1000 ? T.km(nf(Math.round(dist / 100) / 10, 1)) : T.m(nf(Math.round(dist / 50) * 50, 0));
      pts.push({ x, y, name, meta, dist, mark: !!q.mark });
    }
    // landmarks first, then the nearer places; at most six labels, none on top of another (lifted on a longer stem, else left out)
    pts.sort((a, c) => (c.mark - a.mark) || (a.dist - c.dist));
    const placed = [];
    for (const q of pts) {
      if (placed.length >= 6) break;
      let stem = 18, ok = false, box;
      const w = Math.min(bw * 0.46, 9 + 7.2 * Math.max(q.name.length, q.meta.length)), h = 36;
      const cx = Math.min(Math.max(q.x, w / 2 + 4), bw - w / 2 - 4); // the box stays inside the picture; the stem and dot stay on the place
      q.shift = cx - q.x;
      for (let k = 0; k < 4 && !ok; k++, stem += 40) {
        box = { l: cx - w / 2, r: cx + w / 2, t: q.y - stem - h, b: q.y - stem };
        if (box.t < 4) break;
        ok = !placed.some((o) => box.l < o.r + 4 && box.r > o.l - 4 && box.t < o.b + 4 && box.b > o.t - 4);
      }
      if (!ok) continue;
      placed.push(box);
      const el = document.createElement('div'); el.className = 'nlvd__i'; el.style.left = q.x + 'px'; el.style.top = q.y + 'px';
      const bx = document.createElement('div'); bx.className = 'nlvd__b'; bx.dir = lang === 'he' ? 'rtl' : 'ltr';
      if (q.shift) bx.style.transform = 'translateX(' + Math.round(q.shift) + 'px)';
      bx.textContent = q.name; const sm = document.createElement('small'); sm.textContent = q.meta; bx.appendChild(sm);
      const st = document.createElement('div'); st.className = 'nlvd__s'; st.style.height = stem + 'px';
      const dt = document.createElement('div'); dt.className = 'nlvd__d';
      el.append(bx, st, dt); layer.appendChild(el);
    }
  }
  const ro = typeof ResizeObserver !== 'undefined' ? new ResizeObserver(project) : null;
  if (ro) ro.observe(img);
  img.addEventListener('load', project);
  return {
    set(v) { cur = v; project(); },
    show(v) { on = !!v; layer.classList.toggle('nlvd--off', !on); project(); },
    destroy() { if (ro) ro.disconnect(); img.removeEventListener('load', project); layer.remove(); },
  };
}
