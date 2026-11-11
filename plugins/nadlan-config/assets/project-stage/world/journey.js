/* HAD-712 (11.11.2026): words from showroom-i18n.js; direction from the page language. */
/*
 * The Kikar HaMedina journey (HAD-699, 10.11.2026; design: https://claude.ai/artifact/FzvFDybiyBoi8bspoPV9Zp, row "המסלול").
 * Ben, 10.11: "instead of all this, take him into the experience". One full-screen path made only of real renders of the city
 * (Blender, scripts/interior): the square at sunset → choose a tower on the picture → choose a floor on the picture (the floor is
 * marked from the render's own projection) → choose by VIEW (the four real window views of that floor) → the apartment cockpit (cockpit.js) opens for that
 * apartment: the view, inside in 360, the designer, the plan, the facilities, price and cost, the neighbourhood, the video call
 * (Ben 10.11: "a person presses and enters the cockpit of his life"). No 3D engine on this path.
 *
 *   window.__nlJourneyCfg = { data, aerial, base, ver, wa, avail }  (printed by inc/project-stage.php under ?kikar=next)
 *   import('.../world/journey.js').then((m) => m.mountJourney(document.getElementById('nlps')))
 *
 * Every picture says "הדמיה להמחשה" (t('sim')); the inside is the example apartment (tower C, floor 30) and says so.
 */
const C = window.__nlJourneyCfg || {};
const { t, lang, dir, nf } = await import(new URL('showroom-i18n.js' + (C.ver ? '?ver=' + C.ver : ''), import.meta.url).href); // HAD-712: he, en, fr
const SHOWROOM = new URLSearchParams(location.search).get('kikar') !== 'journey'; // HAD-712 (1.72.644): the showroom is the page for every visitor, on Ben's word (11.11.2026); ?kikar=journey keeps the earlier path for comparison
const esc = (s) => String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const bdi = (s) => `<bdi>${esc(s)}</bdi>`;
const A = (p) => (C.base || '') + p + (C.ver ? (p.includes('?') ? '&' : '?') + 'ver=' + C.ver : '');
const ga = (n, p) => { try { if (window.nadlanGA) window.nadlanGA(n, Object.assign({ project: 'hamedina' }, p || {})); } catch (e) { /* none */ } };
const angDiff = (a, b) => Math.abs(((a - b) % 360 + 540) % 360 - 180);
const eyeH = (f) => (f - 1) * 4 + 1.6;
const DIRS = ['dir_to_n', 'dir_to_ne', 'dir_to_e', 'dir_to_se', 'dir_to_s', 'dir_to_sw', 'dir_to_w', 'dir_to_nw']; // keys of showroom-i18n.js
const dirWord = (b, L) => t(DIRS[Math.round((((b % 360) + 360) % 360) / 45) % 8], null, L); // L 'he': the event keeps its Hebrew value
// what lies that way from the square (true bearings; OpenStreetMap and the city's map): words for the view cards
const SECTORS = [[245, 300, 'sec_sea_city'], [300, 345, 'sec_sea_yarkon'], [345, 30, 'sec_yarkon_north'], [30, 75, 'sec_ramat_aviv'], [75, 120, 'sec_ramat_gan'], [120, 200, 'sec_city_towers'], [200, 245, 'sec_old_north']];
const sectorOf = (b) => { b = ((b % 360) + 360) % 360; const s = SECTORS.find(([lo, hi]) => (lo < hi ? b >= lo && b < hi : b >= lo || b < hi)); return s ? t(s[2]) : ''; };

const css = `
.nljy{position:fixed;inset:0;z-index:99995;background:#10262f;color:#fff;font-family:'Assistant','Segoe UI',Arial,sans-serif;overflow:hidden;-webkit-tap-highlight-color:transparent;overscroll-behavior:contain}
.nljy[hidden]{display:none}
.nljy *{box-sizing:border-box}
.nljy bdi{unicode-bidi:isolate;direction:ltr;font-variant-numeric:tabular-nums}
.nljy .bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.nljy .top{position:absolute;top:0;inset-inline:0;z-index:5;display:flex;align-items:center;gap:10px;padding:12px;background:linear-gradient(rgba(16,38,47,.75),rgba(16,38,47,0))}
.nljy .top button{width:44px;height:44px;border-radius:999px!important;border:0;background:rgba(16,38,47,.82);color:#fff;font-size:20px;cursor:pointer;flex:none}
.nljy .bars{flex:1;display:flex;gap:4px}
.nljy .bars i{flex:1;height:4px;border-radius:2px;background:rgba(255,255,255,.35)}
.nljy .bars i.on{background:#7fd3e6}
.nljy .ttl{position:absolute;top:68px;inset-inline:16px;z-index:4;text-shadow:0 2px 12px rgba(0,0,0,.55)}
.nljy .ttl b{display:block;font:600 25px/1.2 'Noto Serif Hebrew',Georgia,serif}
.nljy .ttl span{display:block;font-size:14.5px;color:#e6f2f6;margin-top:2px}
.nljy .cap{position:absolute;z-index:4;bottom:96px;inset-inline-end:12px;font-size:12px;background:rgba(20,33,43,.72);padding:3px 8px;border-radius:6px}
.nljy .cta{position:absolute;z-index:4;bottom:max(18px,env(safe-area-inset-bottom));inset-inline:16px;display:flex;flex-direction:column;gap:8px}
.nljy .go{min-height:56px;border-radius:999px!important;border:0;background:#7fd3e6;color:#10262f;font-size:18px;font-weight:700;cursor:pointer;width:100%}
.nljy .alt{min-height:46px;border-radius:999px!important;border:1px solid rgba(255,255,255,.6);background:rgba(16,38,47,.6);color:#fff;font-size:15px;font-weight:600;cursor:pointer;width:100%}
.nljy .tw{position:absolute;z-index:4;transform:translate(-50%,-100%);min-height:48px;padding:0 14px;border-radius:999px!important;border:1px solid rgba(255,255,255,.5);background:rgba(16,38,47,.86);color:#fff;font-size:16px;font-weight:700;cursor:pointer;white-space:nowrap}
.nljy .band{position:absolute;z-index:3;transform:translate(-50%,-50%);border-radius:6px;background:#7fd3e6;box-shadow:0 0 0 3px rgba(127,211,230,.45),0 0 28px #7fd3e6;pointer-events:none;transition:top .12s}
.nljy .ladder{position:absolute;z-index:4;top:150px;bottom:236px;inset-inline-start:10px;width:64px;border-radius:999px;background:rgba(16,38,47,.84);display:flex;flex-direction:column;align-items:center;padding:10px 0}
.nljy .ladder b{font-size:20px;color:#7fd3e6;font-variant-numeric:tabular-nums}
.nljy .ladder input{flex:1;width:44px;writing-mode:vertical-lr;direction:rtl;accent-color:#7fd3e6;cursor:pointer;margin:8px 0}
.nljy .peek{position:absolute;z-index:4;bottom:92px;inset-inline:16px;display:flex;gap:10px;align-items:center;background:rgba(16,38,47,.9);border-radius:16px;padding:8px}
.nljy .peek img{width:112px;height:63px;object-fit:cover;border-radius:10px;flex:none}
.nljy .peek b{display:block;font-size:16px}.nljy .peek span{font-size:13px;color:#cfe3ea}
.nljy .views{position:absolute;inset:0;overflow-y:auto;padding:68px 16px 24px;display:flex;flex-direction:column;gap:10px}
.nljy .views h2{margin:0;font:600 25px/1.2 'Noto Serif Hebrew',Georgia,serif!important;color:#fff!important}
.nljy .views p{margin:0;font-size:14px;color:#cfe3ea}
.nljy .vc{position:relative;flex:none;height:156px;border-radius:16px!important;overflow:hidden;border:0;padding:0;background:#0b1c23;cursor:pointer;text-align:start}
.nljy .vc img{width:100%;height:100%;object-fit:cover;display:block}
.nljy .vc span{position:absolute;bottom:0;inset-inline:0;padding:28px 12px 10px;background:linear-gradient(rgba(16,38,47,0),rgba(16,38,47,.92));display:flex;justify-content:space-between;align-items:flex-end;color:#fff}
.nljy .vc b{font-size:18px}.nljy .vc small{font-size:12.5px;color:#cfe3ea;text-align:end}
.nljy .pan{position:absolute;inset:0;overflow-x:auto;overflow-y:hidden;scrollbar-width:none;-webkit-overflow-scrolling:touch}
.nljy .pan::-webkit-scrollbar{display:none}
.nljy .pan img{height:100%;width:auto;max-width:none;display:block}
.nljy .hint{position:absolute;z-index:4;top:46%;inset-inline:16px;text-align:center;font-size:14px;text-shadow:0 1px 8px rgba(0,0,0,.7);pointer-events:none}
.nljy .chips{position:absolute;z-index:4;bottom:92px;inset-inline:16px;display:flex;gap:6px;overflow-x:auto;scrollbar-width:none}
.nljy .chips button{flex:none;min-height:44px;padding:0 14px;border-radius:999px!important;border:0;background:rgba(16,38,47,.84);color:#fff;font-size:14px;cursor:pointer}
.nljy .chips button[aria-pressed=true]{background:#fff;color:#10262f;font-weight:700}
.nljy .story{position:absolute;inset:0}
.nljy .story .tapl,.nljy .story .tapr{position:absolute;top:0;bottom:0;width:35%;z-index:2;border:0;background:transparent;cursor:pointer}
.nljy .story .tapl{left:0}.nljy .story .tapr{right:0}
@media (min-width:900px){.nljy .bg,.nljy .pan img{object-position:center}.nljy .views{max-width:720px;margin:0 auto;inset-inline:0}}
@media (prefers-reduced-motion:reduce){.nljy *{transition:none!important}}`;

let D = null, AER = null, el = null;
const S = { step: 1, tower: null, floor: 30, view: null };

function load() {
  if (D && AER) return Promise.resolve();
  return Promise.all([fetch(C.data).then((r) => r.json()), fetch(C.aerial).then((r) => r.json())]).then(([d, a]) => { D = d; AER = a; });
}
// the tall sunset picture is cover-fitted into the screen: a 0..1 point of the picture to the screen
function fit(zoom, cx, cy) {
  const W = el.clientWidth, H = el.clientHeight, fw = 800, fh = 1067;
  const s = Math.max(W / fw, H / fh) * (zoom || 1), dw = fw * s, dh = fh * s;
  let ox = (W - dw) / 2, oy = (H - dh) / 2;
  if (cx != null) ox = Math.min(0, Math.max(W - dw, W / 2 - cx * dw));
  if (cy != null) oy = Math.min(0, Math.max(H - dh, H * 0.45 - cy * dh));
  return { s, dw, dh, ox, oy, at: (u, v) => ({ x: ox + u * dw, y: oy + v * dh }) };
}
function viewsOf(t, f) {
  const all = (D.views || []).filter((v) => v.tower === t && v.tod === 'day' && v.side != null && v.big);
  if (!all.length) return { floor: f, list: [270, 0, 90, 180].map((b) => ({ bearing: b, img: '' })) };
  const fl = all.map((v) => v.floor).sort((a, b) => Math.abs(a - f) - Math.abs(b - f))[0];
  const list = all.filter((v) => v.floor === fl).sort((a, b) => (angDiff(a.bearing, 262) - angDiff(b.bearing, 262)));
  return { floor: fl, list };
}
function bars(n) { return `<div class="bars">${[2, 3, 4].map((k) => `<i class="${k <= n ? 'on' : ''}"></i>`).join('')}</div>`; }
function top() { return `<div class="top"><button type="button" data-a="back" aria-label="${esc(t('aria_back'))}">${t('jy_back_glyph')}</button>${bars(S.step)}<button type="button" data-a="close" aria-label="${esc(t('aria_close'))}">✕</button></div>`; }

// the floor's view preview: the title and the line under it (HAD-712: words by language, the eye height in its number format)
function peekTitle(vv, f) { return t('jy_view_from', { floor: bdi(vv.floor) }) + (vv.floor !== f ? t('jy_nearest') : ''); }
function peekSub(vv, f) { return t('jy_peek_sub', { m: bdi(nf(eyeH(f), 1)), n: vv.list.length }); }
function render() {
  if (!el) return;
  const st = S.step;
  let h = '';
  if (st === 2) {
    const z = fit(1); const tw = AER.tall.towers;
    h = `<img class="bg" src="${esc(A('aerial-tall-800.webp'))}" alt="${esc(t('jy_alt_square'))}" style="object-position:50% 50%">
      <div class="ttl"><b>${esc(t('jy_choose_tower'))}</b><span>${esc(t('jy_choose_tower_sub'))}</span></div>
      ${Object.keys(tw).map((k) => { const p = z.at(tw[k][tw[k].length - 1][0], tw[k][tw[k].length - 1][1]); return `<button type="button" class="tw" data-a="tower" data-v="${k}" style="left:${Math.max(48, Math.min(el.clientWidth - 48, p.x))}px;top:${p.y - 4}px" aria-label="${esc(t('jy_aria_tower', { tower: k, n: tw[k].length }))}">${k} · ${tw[k].length}</button>`; }).join('')}
      <span class="cap">${esc(t('sim'))}</span>`;
  } else if (st === 3) {
    const row = AER.tall.towers[S.tower], n = row.length, f = Math.min(S.floor, n);
    const cx = row[Math.floor(n / 2)][0], cy = row[Math.floor(n / 2)][1];
    const z = fit(1.65, cx, cy), p = z.at(row[f - 1][0], row[f - 1][1]), q = z.at(row[Math.max(0, f - 2)][0], row[Math.max(0, f - 2)][1]);
    const pxf = Math.max(6, Math.abs(p.y - q.y) || 8), wpx = Math.max(60, pxf * 7.6);
    const vv = viewsOf(S.tower, f), peek = vv.list[0] && vv.list[0].img ? vv.list[0] : null;
    h = `<img class="bg" src="${esc(A('aerial-tall-800.webp'))}" alt="${esc(t('jy_alt_tower_close', { tower: S.tower }))}" style="width:${z.dw}px;height:${z.dh}px;left:${z.ox}px;top:${z.oy}px;right:auto;bottom:auto;max-width:none;object-fit:fill">
      <div class="band" style="left:${p.x}px;top:${p.y}px;width:${wpx}px;height:${Math.max(8, pxf * 0.8)}px"></div>
      <div class="ttl" style="inset-inline-start:88px"><b>${esc(t('jy_choose_floor', { tower: S.tower }))}</b><span>${esc(t('jy_choose_floor_sub'))}</span></div>
      <div class="ladder"><b>${bdi(f)}</b><input type="range" min="1" max="${n}" value="${f}" aria-label="${esc(t('jy_aria_floor', { tower: S.tower }))}" data-a="floor"><small style="font-size:12px;color:#cfe3ea">${esc(t('floor_word'))}</small></div>
      ${peek ? `<div class="peek"><img src="${esc(A(peek.img))}" alt=""><div><b>${peekTitle(vv, f)}</b><span>${peekSub(vv, f)}</span></div></div>` : ''}
      <div class="cta"><button type="button" class="go" data-a="next">${t('jy_next_view', { floor: bdi(f) })}</button></div>`;
  } else if (st === 4) {
    const vv = viewsOf(S.tower, S.floor);
    h = `<div class="views"><h2>${esc(t('jy_views_title'))}</h2><p>${t('jy_views_sub', { tower: esc(S.tower), floor: bdi(S.floor) })}${vv.floor !== S.floor ? t('jy_views_nearest', { floor: bdi(vv.floor) }) : ''}</p>
      ${vv.list.map((v, i) => { return `<button type="button" class="vc" data-a="view" data-v="${i}">${v.img ? `<img src="${esc(A(v.img))}" alt="${t('jy_alt_view', { dir: esc(dirWord(v.bearing)) })}" loading="lazy">` : ''}<span><b>${esc(dirWord(v.bearing))} · ${esc(sectorOf(v.bearing))}</b><small>${bdi(Math.round(v.bearing) + '°')}</small></span></button>`; }).join('')}
      </div>`;
  }
  el.innerHTML = top() + h;
}
function toCockpit() {
  const vv = viewsOf(S.tower, S.floor), v = vv.list[S.view || 0];
  close(true);
  const detail = { tower: S.tower, floor: S.floor, heightM: +eyeH(S.floor).toFixed(1), bearing: Math.round(v ? v.bearing : 262), facing: dirWord(v ? v.bearing : 262, 'he'), source: 'journey' };
  window.dispatchEvent(new CustomEvent('nl:facing', { detail }));
  ga('journey_cockpit', { tower: S.tower, floor: S.floor });
}
function onClick(e) {
  const b = e.target.closest('[data-a]'); if (!b) return;
  const a = b.dataset.a, v = b.dataset.v;
  if (a === 'close') return close();
  if (a === 'back') { S.step = Math.max(1, S.step - 1); if (S.step === 1) return close(); return render(); }
  if (a === 'tower') { S.tower = v; S.floor = Math.min(30, AER.tall.towers[v].length); S.step = 3; ga('journey_tower', { tower: v }); return render(); }
  if (a === 'view') { S.view = +v; ga('journey_view', { tower: S.tower, floor: S.floor, view: +v }); return toCockpit(); }
  if (a === 'next') { S.step += 1; ga('journey_step', { step: S.step }); return render(); }
}
function onInput(e) {
  if (e.target.dataset.a !== 'floor') return;
  S.floor = +e.target.value;
  // repaint the band, the number and the view preview without rebuilding the slider (keeps the drag)
  const row = AER.tall.towers[S.tower], n = row.length, f = Math.min(S.floor, n);
  const cx = row[Math.floor(n / 2)][0], cy = row[Math.floor(n / 2)][1];
  const z = fit(1.65, cx, cy), p = z.at(row[f - 1][0], row[f - 1][1]);
  const band = el.querySelector('.band'); if (band) band.style.top = p.y + 'px';
  const num = el.querySelector('.ladder b'); if (num) num.textContent = f;
  const go = el.querySelector('.cta .go'); if (go) go.innerHTML = t('jy_next_view', { floor: bdi(f) });
  clearTimeout(onInput.t); onInput.t = setTimeout(() => { const vv = viewsOf(S.tower, f), pk = vv.list[0], pe = el.querySelector('.peek'); if (pe && pk && pk.img) { pe.querySelector('img').src = A(pk.img); pe.querySelector('b').innerHTML = peekTitle(vv, f); pe.querySelector('span').innerHTML = peekSub(vv, f); } }, 120);
}
function open(step) {
  if (!document.getElementById('nljy-css')) { const s = document.createElement('style'); s.id = 'nljy-css'; s.textContent = css; document.head.appendChild(s); }
  if (!el) {
    el = document.createElement('div'); el.className = 'nljy'; el.dir = dir(); el.lang = lang(); el.setAttribute('role', 'dialog'); el.setAttribute('aria-modal', 'true'); el.setAttribute('aria-label', t('jy_aria_dialog'));
    document.body.appendChild(el);
    el.addEventListener('click', onClick); el.addEventListener('input', onInput);
    el.addEventListener('keydown', (e) => { if (e.key === 'Escape') close(); });
    addEventListener('resize', () => { if (el && !el.hidden) render(); });
  }
  return load().then(() => { S.step = step || 2; el.hidden = false; document.documentElement.style.overflow = 'hidden'; render(); const f = el.querySelector('button'); if (f) f.focus({ preventScroll: true }); ga('journey_open', {}); });
}
function close(toCockpitNext) { if (!el) return; el.hidden = true; document.documentElement.style.overflow = ''; if (!toCockpitNext) ga('journey_close', { step: S.step }); }

// the entry: the square at sunset fills the first screen of the stage, with one button
export function mountJourney(stage) {
  if (SHOWROOM) { // HAD-712: the showroom stage (each tower a turntable, the floor chosen on the tower, the map with the beam)
    document.body.classList.add('nljy-on');
    import(new URL('showroom.js' + (C.ver ? '?ver=' + C.ver : ''), import.meta.url).href).then((m) => m.mountShowroom(stage)).catch((e) => console.warn('[showroom]', e));
    return { open };
  }
  if (!stage || stage.querySelector('.nljy-entry')) return { open };
  const entry = document.createElement('div');
  entry.className = 'nljy-entry'; entry.dir = dir(); entry.lang = lang();
  entry.innerHTML = `<style>.nljy-entry{position:relative;height:clamp(420px,calc(100svh - 270px),640px);border-radius:0;overflow:hidden;background:#10262f;color:#fff;font-family:'Assistant','Segoe UI',Arial,sans-serif;margin:0 0 12px}
    .nljy-entry img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:45% 40%}
    .nljy-entry .in{position:absolute;bottom:0;inset-inline:0;padding:110px 16px 18px;background:linear-gradient(rgba(16,38,47,0),rgba(16,38,47,.92) 40%);display:flex;flex-direction:column;gap:10px}
    .nljy-entry .t{font:600 28px/1.18 'Noto Serif Hebrew',Georgia,serif}
    .nljy-entry .f{font-size:15px;color:#cfe3ea}
    .nljy-entry button{min-height:56px;border-radius:999px!important;border:0;background:#7fd3e6;color:#10262f;font-size:18px;font-weight:700;cursor:pointer}
    .nljy-entry .c{position:absolute;top:12px;inset-inline-end:12px;font-size:12px;background:rgba(20,33,43,.72);padding:3px 8px;border-radius:6px}
    @media (min-width:900px){.nljy-entry{height:clamp(420px,calc(100vh - 290px),640px);border-radius:22px}.nljy-entry .in{max-width:620px}}</style>
    <img src="${esc(A('aerial-tall-800.webp'))}" srcset="${esc(A('aerial-tall-800.webp'))} 800w, ${esc(A('aerial-1600.webp'))} 1600w" sizes="(max-width:899px) 100vw, 1200px" alt="${esc(t('jy_alt_entry'))}" fetchpriority="high">
    <span class="c">${esc(t('sim'))}</span>
    <div class="in"><div class="t">${esc(t('jy_entry_title'))}</div><div class="f">${esc(t('jy_entry_sub'))}</div><button type="button" data-jy="open">${esc(t('jy_entry_cta'))}</button></div>`;
  stage.parentNode.insertBefore(entry, stage);
  document.body.classList.add('nljy-on');
  window.__nlJourney = { open };
  entry.addEventListener('click', (e) => { if (e.target.closest('[data-jy="open"]')) open(2); });
  return { open };
}
export { open as openJourney };
