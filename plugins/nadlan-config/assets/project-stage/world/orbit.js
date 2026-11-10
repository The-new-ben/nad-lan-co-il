/*
 * "סובבו את הכיכר": the photoreal orbit of Kikar HaMedina (HAD-699, 10.11.2026; design https://claude.ai/artifact/FzvFDybiyBoi8bspoPV9Zp).
 * 24 Blender Cycles frames of the real city (scripts/interior/kikar_aerial.py KA_ORBIT), one every 15°. Drag or swipe to turn,
 * the arrows for keyboard and one-handed use. Each frame carries the projected screen point of every floor of the three towers
 * (orbit.json), so a tower is tapped on the picture and its floors are marked on the picture itself. Choosing a floor hands the
 * choice to the 3D world (pickTower + setFloor), whose facing pick opens the apartment cockpit.
 *
 *   import('.../world/orbit.js').then((m) => m.mountOrbit(host, { json, base, start, onPick: ({ tower, floor }) => {} }))
 *
 * Only the first frame loads with the page; the other 23 load after the first touch (about 2.9 MB in all, WebP).
 * Every picture is an illustration ("הדמיה להמחשה").
 */
const NAMES = { A: 'מגדל A', B: 'מגדל B', C: 'מגדל C' };
const css = `
.nlob{position:relative;overflow:hidden;background:#10262f;touch-action:pan-y;user-select:none;-webkit-user-select:none;direction:rtl;font-family:'Assistant','Segoe UI',Arial,sans-serif}
.nlob img.f{display:block;width:100%;height:100%;object-fit:cover;pointer-events:none}
.nlob .cap{position:absolute;bottom:64px;inset-inline-start:12px;background:rgba(20,33,43,.72);color:#f7f9fa;font-size:12px;padding:4px 8px;border-radius:6px}
.nlob .tw{position:absolute;transform:translate(-50%,-100%);min-height:44px;padding:0 12px;border-radius:999px;border:1px solid rgba(255,255,255,.4);background:rgba(16,38,47,.84);color:#fff;font-size:14px;font-weight:600;cursor:pointer;white-space:nowrap}
.nlob .tw[aria-pressed=true]{background:#7fd3e6;border-color:#7fd3e6;color:#10262f;font-weight:700}
.nlob .band{position:absolute;transform:translate(-50%,-50%);border-radius:4px;background:#7fd3e6;box-shadow:0 0 0 2px rgba(127,211,230,.4),0 0 20px rgba(127,211,230,.95);pointer-events:none}
.nlob .nav{position:absolute;top:50%;transform:translateY(-50%);width:44px;height:44px;border-radius:999px;border:0;background:rgba(16,38,47,.82);color:#fff;cursor:pointer;display:grid;place-items:center}
.nlob .nav.l{left:10px}.nlob .nav.r{right:10px}
.nlob .floors{position:absolute;inset-inline:12px;bottom:12px;display:flex;align-items:center;gap:8px;background:rgba(16,38,47,.84);border-radius:999px;padding:4px 6px 4px 14px;color:#fff;font-size:14px}
.nlob .floors input{flex:1;accent-color:#7fd3e6;min-height:36px}
.nlob .floors button{min-height:40px;padding:0 14px;border-radius:999px;border:0;background:#7fd3e6;color:#10262f;font-weight:700;cursor:pointer;white-space:nowrap}
.nlob .hint{position:absolute;top:12px;inset-inline-end:12px;background:rgba(16,38,47,.82);color:#fff;font-size:13px;padding:6px 10px;border-radius:999px}
.nlob svg{width:20px;height:20px;stroke:currentColor;fill:none;stroke-width:2;stroke-linecap:round}
@media (prefers-reduced-motion:reduce){.nlob *{transition:none!important}}`;

export function mountOrbit(host, opts = {}) {
  if (!document.getElementById('nlob-css')) { const s = document.createElement('style'); s.id = 'nlob-css'; s.textContent = css; document.head.appendChild(s); }
  const st = { i: opts.start || 0, tower: null, floor: null, meta: null, imgs: [], loaded: false };
  const root = document.createElement('div');
  root.className = 'nlob'; root.style.height = '100%';
  root.setAttribute('role', 'group'); root.setAttribute('aria-label', 'כיכר המדינה מכל כיוון, הדמיה');
  root.innerHTML = `<img class="f" alt="מגדלי כיכר המדינה והכיכר, הדמיה מהאוויר" decoding="async">
    <span class="cap">הדמיה להמחשה</span><span class="hint">גררו כדי לסובב</span>
    <button type="button" class="nav l" aria-label="לסובב שמאלה"><svg viewBox="0 0 24 24"><path d="M15 6l-6 6 6 6"/></svg></button>
    <button type="button" class="nav r" aria-label="לסובב ימינה"><svg viewBox="0 0 24 24"><path d="M9 6l6 6-6 6"/></svg></button>
    <div class="tws"></div><div class="band" hidden></div><div class="floors" hidden></div>`;
  host.innerHTML = ''; host.appendChild(root);
  const img = root.querySelector('img.f'), tws = root.querySelector('.tws'), band = root.querySelector('.band'), fl = root.querySelector('.floors');
  const src = (k) => (opts.base || '') + st.meta.frames[k].file.replace(/\.png$/, '.webp') + (opts.ver ? '?ver=' + opts.ver : '');

  function preloadAll() {
    if (st.loaded || !st.meta) return; st.loaded = true;
    st.meta.frames.forEach((f, k) => { const im = new Image(); im.decoding = 'async'; im.src = src(k); st.imgs[k] = im; });
  }
  // the frame is cover-fitted: map a 0..1 point of the frame to the box
  function place(u, v) {
    const W = root.clientWidth, Hh = root.clientHeight, [fw, fh] = st.meta.size;
    const s = Math.max(W / fw, Hh / fh), dw = fw * s, dh = fh * s;
    return { x: (W - dw) / 2 + u * dw, y: (Hh - dh) / 2 + v * dh, s };
  }
  function paint() {
    if (!st.meta) return;
    const f = st.meta.frames[st.i];
    img.src = src(st.i);
    // labels over each tower's top, nearest first; a label that would sit on another one moves up (no overlap on any frame)
    const narrow = root.clientWidth < 600, lw = narrow ? 92 : 150, lh = 48;
    const L = Object.keys(f.towers).map((k) => { const top = f.towers[k][f.towers[k].length - 1], p = place(top[0], top[1]); return { k, x: p.x, y: p.y - 6, n: f.towers[k].length }; })
      .sort((a, b) => b.y - a.y);
    const placed = [];
    for (const l of L) {
      for (let g = 0; g < 4 && placed.some((q) => Math.abs(q.x - l.x) < lw && Math.abs(q.y - l.y) < lh); g++) l.y -= lh;
      l.y = Math.max(lh, l.y); placed.push(l);
    }
    tws.innerHTML = placed.map((l) => `<button type="button" class="tw" data-t="${l.k}" aria-pressed="${st.tower === l.k}" aria-label="${NAMES[l.k]}, ${l.n} קומות" style="left:${l.x}px;top:${l.y}px">${narrow ? `${l.k} · ${l.n}` : `${NAMES[l.k]} · ${l.n} קומות`}</button>`).join('');
    if (st.tower && st.floor) {
      const row = f.towers[st.tower], a = row[st.floor - 1], b = row[Math.min(row.length - 1, st.floor)];
      const pa = place(a[0], a[1]), pb = place(b[0], b[1]);
      const pxm = Math.max(0.6, Math.abs(pa.y - pb.y) / 4 || 1);  // pixels per metre (4 m a floor)
      band.hidden = false; Object.assign(band.style, { left: pa.x + 'px', top: pa.y + 'px', width: Math.max(18, 31 * pxm) + 'px', height: Math.max(5, 3.2 * pxm) + 'px' });
    } else band.hidden = true;
  }
  function turn(d) { if (!st.meta) return; preloadAll(); st.i = (st.i + d + st.meta.frames.length) % st.meta.frames.length; paint(); }
  function floors() {
    if (!st.tower) { fl.hidden = true; return; }
    const n = st.meta.frames[st.i].towers[st.tower].length;
    fl.hidden = false;
    fl.innerHTML = `<label style="display:flex;align-items:center;gap:8px;flex:1">קומה <b class="fn">${st.floor}</b><input type="range" min="1" max="${n}" value="${st.floor}" aria-label="בחירת קומה"></label><button type="button" data-go>לבחור דירה בקומה</button>`;
  }
  root.addEventListener('click', (e) => {
    const t = e.target.closest('.tw'); if (t) { st.tower = t.dataset.t; st.floor = st.floor || Math.min(30, st.meta.frames[st.i].towers[st.tower].length); floors(); paint(); preloadAll(); return; }
    if (e.target.closest('.nav.l')) return turn(-1);
    if (e.target.closest('.nav.r')) return turn(1);
    if (e.target.closest('[data-go]') && opts.onPick) opts.onPick({ tower: st.tower, floor: st.floor });
  });
  root.addEventListener('input', (e) => { if (e.target.type === 'range') { st.floor = +e.target.value; const b = root.querySelector('.fn'); if (b) b.textContent = st.floor; paint(); } });
  root.addEventListener('keydown', (e) => { if (e.key === 'ArrowLeft') turn(-1); if (e.key === 'ArrowRight') turn(1); });
  let x0 = null, i0 = 0;
  root.addEventListener('pointerdown', (e) => { if (e.target.closest('button,input')) return; x0 = e.clientX; i0 = st.i; preloadAll(); });
  addEventListener('pointermove', (e) => { if (x0 == null || !st.meta) return; const step = Math.round((e.clientX - x0) / 28); const n = st.meta.frames.length; const k = ((i0 - step) % n + n) % n; if (k !== st.i) { st.i = k; paint(); } });
  addEventListener('pointerup', () => { x0 = null; });
  addEventListener('resize', paint);
  fetch(opts.json, { credentials: 'omit' }).then((r) => r.json()).then((m) => { st.meta = m; paint(); }).catch((e) => console.warn('[orbit]', e));
  return { turn, destroy() { root.remove(); } };
}
