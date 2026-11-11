/* HAD-712 (11.11.2026): words from showroom-i18n.js; direction from the page language. */
/* Kikar HaMedina: the showroom stage (HAD-712, Ben 11.11.2026: "each building turns on its own, you choose the apartment on the
 * building, the map under it answers with a beam, and a pulse shows the next thing to tap").
 *
 * What it reuses, by Ben's order (docs/research/2026-11-11-kikar-journey/fairness-statement.md): Ashira's one tap on the tower for a
 * floor, the floor card at the thumb with the apartment's own inquiry, the numbered steps under the model, the beam on the map, the
 * apartment basket (window.__nlBasket) and Kikar's apartment screen (window.__nlCockpit). New here: every tower is a turntable of
 * 24 Blender pictures with the real city around it (hamedina/turn/, scripts/interior/kikar_turntable.py), the map sits right under
 * the model, and the next action pulses until it is taken.
 *
 *   window.__nlJourneyCfg = { js, data, aerial, base, ver }   window.__nlCockpitCfg = { wa, avail, ... }
 *   mountShowroom(beforeEl) -> { open }   (journey.js hands over to it)
 * Every picture is "הדמיה להמחשה". No sun, no fake urgency, no price that was not published. */
const C = window.__nlJourneyCfg || {};
const CK = window.__nlCockpitCfg || {};
const { t, lang, dir } = await import(new URL('showroom-i18n.js' + (C.ver ? '?ver=' + C.ver : ''), import.meta.url).href); // HAD-712: he, en, fr
const A = (p) => (C.base || '') + p + (C.ver ? (p.includes('?') ? '&' : '?') + 'ver=' + C.ver : '');
const WORLD = (C.js || '').replace(/journey\.js.*$/, '');
const esc = (s) => String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const ga = (n, p) => { try { if (window.nadlanGA) window.nadlanGA(n, Object.assign({ project: 'hamedina' }, p || {})); } catch (e) { /* none */ } };
const norm = (b) => ((b % 360) + 360) % 360;
const angDiff = (a, b) => Math.abs(((a - b) % 360 + 540) % 360 - 180);
const DIRS = ['dir_to_n', 'dir_to_ne', 'dir_to_e', 'dir_to_se', 'dir_to_s', 'dir_to_sw', 'dir_to_w', 'dir_to_nw']; // "faces north" (keys of showroom-i18n.js)
const DIRN = ['dir_n', 'dir_ne', 'dir_e', 'dir_se', 'dir_s', 'dir_sw', 'dir_w', 'dir_nw']; // "from the north"
const dirIx = (b) => Math.round(norm(b) / 45) % 8;
const dirTo = (b, L) => t(DIRS[dirIx(b)], null, L), dirFrom = (b, L) => t(DIRN[dirIx(b)], null, L); // L 'he': the analytics keep their Hebrew values
const SECTORS = [[245, 300, 'sec_sea_city'], [300, 345, 'sec_sea_yarkon'], [345, 30, 'sec_yarkon_north'], [30, 75, 'sec_ramat_aviv'], [75, 120, 'sec_ramat_gan'], [120, 200, 'sec_city_towers'], [200, 245, 'sec_old_north']];
const sectorOf = (b) => { b = norm(b); const s = SECTORS.find(([lo, hi]) => (lo < hi ? b >= lo && b < hi : b >= lo || b < hi)); return s ? t(s[2]) : ''; };
const eyeH = (f) => (f - 1) * 4 + 1.6;
const STEPS = [['tower', 'sr_step_tower'], ['view', 'sr_step_view'], ['inside', 'sr_step_inside'], ['design', 'sr_step_design'], ['basket', 'basket_name']];
const START = 270; // each tower first shows the side that looks west, to the sea

let T = null, AER = null, VIEWS = null, el = null, box = null;
const S = { tower: null, frame: 0, floor: null, side: null, done: {}, touched: false };
const pre = {};

const turn = () => (S.tower ? T.towers[S.tower] : null);
const plateAt = (k, f) => T.towers[k].base + T.twist_dir * T.twist * (Math.min(Math.max(f, 1), T.towers[k].floors) - 1);
const sideBearing = (k, f, s) => norm(plateAt(k, f) + s * 90);
const frameUrl = (k, i) => A(`turn/${k}-${String(i).padStart(2, '0')}.webp`);
function nearestFrame(k, bearing) { // the rendered frame whose camera stands nearest to this bearing
  const F = T.towers[k].frames; let best = 0, d = 999;
  F.forEach((f, i) => { if (!f.ok) return; const x = angDiff(f.b, bearing); if (x < d) { d = x; best = i; } });
  return best;
}
function stepFrame(k, i, dir) { const F = T.towers[k].frames, n = F.length; for (let q = 1; q <= n; q++) { const j = ((i + dir * q) % n + n) % n; if (F[j].ok) return j; } return i; }
function preload(k, i) { const u = frameUrl(k, i); if (!pre[u]) { const im = new Image(); im.decoding = 'async'; im.src = u; pre[u] = im; } return pre[u]; }
function preloadAround(k, i) { const n = T.towers[k].frames.length; for (let q = 0; q <= n / 2; q++) { for (const j of [(i + q) % n, (i - q + n) % n]) if (T.towers[k].frames[j].ok) setTimeout(() => preload(k, j), q * 60); } }

function load() {
  if (T) return Promise.resolve();
  return Promise.all([fetch(A('turn/turn.json'), { credentials: 'omit' }).then((r) => r.json()), fetch(C.aerial, { credentials: 'omit' }).then((r) => r.json())]).then(([t, a]) => { T = t; AER = a; });
}
function loadViews() { if (VIEWS || !C.data) return; VIEWS = []; fetch(C.data, { credentials: 'omit' }).then((r) => r.json()).then((j) => { VIEWS = (j.views || []).filter((v) => v.tod === 'day' && v.bearing != null && v.side != null); paintCard(); }).catch(() => {}); }
function viewOf(k, f, b) { const L = (VIEWS || []).filter((v) => v.tower === k && angDiff(v.bearing, b) <= 30).sort((x, y) => Math.abs(x.floor - f) - Math.abs(y.floor - f)); return L[0] || null; }

/* ---------------------------------------------------------------- the picture: placed by hand, so a tap and a floor band agree */
const PIC = { all: [800, 1067, 0.56], tower: [756, 1080, 0.525] }; // width, height, the height share kept at the box's middle
function place() {
  if (!box) return;
  const [pw, ph, mid] = S.tower ? PIC.tower : PIC.all, W = box.clientWidth, H = box.clientHeight, sc = Math.max(W / pw, H / ph), w = pw * sc, h = ph * sc;
  let top = Math.min(0, Math.max(H - h, H / 2 - h * mid)); const left = (W - w) / 2;
  if (S.tower && S.floor) { // the chosen floor stays in sight, in the middle of what the card leaves free
    const card = el.querySelector('.nlsr-card'), free = H - (card.hidden ? 0 : card.offsetHeight), r = turn().frames[S.frame].f[S.floor - 1];
    top = Math.min(0, Math.max(H - h, free * 0.56 - h * ((r[1] + r[3]) / 2000)));
  }
  const im = el.querySelector('.nlsr-img'); im.style.cssText = `left:${left}px;top:${top}px;width:${w}px;height:${h}px`;
}
function paintPic() {
  const img = el.querySelector('.nlsr-pic');
  if (!S.tower) { img.src = A('aerial-tall-800.webp'); img.alt = t('sr_alt_aerial'); }
  else { img.src = frameUrl(S.tower, S.frame); img.alt = t('sr_alt_tower', { tower: S.tower, dir: dirFrom(turn().frames[S.frame].b) }); }
  place(); paintBand(); paintMap();
}
function paintHandles() {
  const hs = el.querySelector('.nlsr-handles');
  if (S.tower) { hs.innerHTML = ''; return; }
  const tw = (AER.tall && AER.tall.towers) || {};
  hs.innerHTML = Object.keys(tw).sort().map((k) => { const p = tw[k][Math.floor(tw[k].length * 0.72)]; return `<button type="button" class="nlsr-h nlsr-pulse" data-tower="${k}" style="left:${(p[0] * 100).toFixed(2)}%;top:${(p[1] * 100).toFixed(2)}%" aria-label="${esc(t('sr_aria_tower_handle', { tower: k }))}">${k}</button>`; }).join('');
}
function bandOf(i, f) { // the floor's band on frame i, as picture thousandths
  const F = turn().frames[i].f, r = F[f - 1], n = F.length, hh = Math.abs(F[0][1] - F[n - 1][1]) / (n - 1) / 2;
  return { r, hh };
}
function paintBand() {
  const g = el.querySelector('.nlsr-ov'), tag = el.querySelector('.nlsr-tag');
  if (!S.tower || !S.floor) { g.innerHTML = ''; tag.hidden = true; return; }
  const { r, hh } = bandOf(S.frame, S.floor);
  g.innerHTML = `<polygon class="nlsr-band" points="${r[0]},${r[1] - hh} ${r[2]},${r[3] - hh} ${r[2]},${r[3] + hh} ${r[0]},${r[1] + hh}"/>`;
  tag.hidden = false; tag.textContent = t('floor_n', { floor: S.floor }); tag.style.left = (r[2] / 10 + 1.5) + '%'; tag.style.top = ((r[1] + r[3]) / 20) + '%';
}

/* ---------------------------------------------------------------- the map under the model: the towers, where you stand, the beam */
function paintMap() {
  const m = T.map, sv = el.querySelector('.nlsr-mapov'), line = el.querySelector('.nlsr-mapline');
  const P = (x, y) => `${x.toFixed(0)},${(-y).toFixed(0)}`;
  let h = '';
  for (const k of Object.keys(m.towers).sort()) { const [x, y] = m.towers[k], on = k === S.tower; h += `<circle class="nlsr-tw${on ? ' is-on' : ''}" cx="${x}" cy="${-y}" r="${on ? 44 : 30}"/>`; }
  if (S.tower) {
    const [x, y] = m.towers[S.tower];
    if (S.side != null && S.floor) {
      const b = sideBearing(S.tower, S.floor, S.side), R = 3200, a1 = (b - 26) * Math.PI / 180, a2 = (b + 26) * Math.PI / 180;
      h = `<path class="nlsr-beam" d="M${P(x, y)} L${P(x + R * Math.sin(a1), y + R * Math.cos(a1))} L${P(x + R * Math.sin(a2), y + R * Math.cos(a2))} Z"/>` + h;
      line.innerHTML = t('sr_map_facing', { dir: esc(dirTo(b)), sector: esc(sectorOf(b)) });
    } else {
      const cb = turn().frames[S.frame].b * Math.PI / 180, ex = x + 210 * Math.sin(cb), ey = y + 210 * Math.cos(cb);
      h += `<path class="nlsr-eyeline" d="M${P(ex, ey)} L${P(x, y)}"/><circle class="nlsr-eye" cx="${ex.toFixed(0)}" cy="${(-ey).toFixed(0)}" r="34"/>`;
      line.innerHTML = t('sr_map_looking', { tower: esc(S.tower), dir: esc(dirFrom(turn().frames[S.frame].b)) });
    }
  } else line.innerHTML = t('sr_map_intro');
  sv.innerHTML = h;
}

/* ---------------------------------------------------------------- the card, the steps, the hint: what to tap next */
function facingText() { const b = sideBearing(S.tower, S.floor, S.side); return t('faces_line', { dir: dirTo(b), sector: sectorOf(b) }); }
function waHref() {
  if (!CK.wa) return '';
  try { const u = new URL(CK.wa, location.href), b = sideBearing(S.tower, S.floor, S.side);
    const w = { floor: S.floor, tower: S.tower, dir: dirFrom(b), dirTo: dirTo(b) }; // en/fr AWAITING BEN: the English page's sentence, the apartment in the page language
    u.searchParams.set('text', t('sr_wa_text', Object.assign(w, { apt: t('sr_wa_apt', w) }))); return u.toString(); } catch (e) { return CK.wa; }
}
function paintCard() {
  const c = el.querySelector('.nlsr-card');
  if (!S.tower || !S.floor) { c.hidden = true; return; }
  const b = sideBearing(S.tower, S.floor, S.side), v = viewOf(S.tower, S.floor, b), wa = waHref();
  c.hidden = false;
  c.innerHTML = `<div class="nlsr-crow">${v ? `<img class="nlsr-cview" src="${esc(A(v.img))}" alt="${esc(t('sr_alt_card_view'))}">` : ''}
      <div class="nlsr-cid"><div class="nlsr-ct">${t('apt_title', { tower: esc(S.tower), floor: S.floor })}</div><div class="nlsr-cf">${esc(facingText())}</div></div>
      <div class="nlsr-cstep"><button type="button" data-fl="-1" aria-label="${esc(t('sr_aria_floor_down'))}">−</button><button type="button" data-fl="1" aria-label="${esc(t('sr_aria_floor_up'))}">+</button></div></div>
    <button type="button" class="nlsr-cside" data-side="next">${esc(t('sr_card_other_side'))}</button>
    <div class="nlsr-cact"><button type="button" class="nlsr-go${S.done.view ? '' : ' nlsr-pulse'}" data-go="home">${esc(t('sr_card_enter'))}</button>
      ${wa ? `<a class="nlsr-ask" href="${esc(wa)}" target="_blank" rel="noopener" data-ev="ask">${esc(t('sr_card_ask'))}</a>` : ''}</div>`;
}
function nextStep() { if (!S.floor) return 'tower'; for (const [k] of STEPS.slice(1)) if (!S.done[k]) return k; return null; }
function paintSteps() {
  const nx = nextStep();
  el.querySelector('.nlsr-steps').innerHTML = STEPS.map(([k, lab], i) => { const done = k === 'tower' ? !!S.floor : !!S.done[k], on = k === nx;
    return `<li><button type="button" class="nlsr-st${done ? ' is-done' : ''}${on ? ' is-on' : ''}" data-step="${k}"${on ? ' aria-current="step"' : ''}><span class="nlsr-sn${on ? ' nlsr-pulse-b' : ''}">${done ? '✓' : i + 1}</span><span class="nlsr-sl">${t(lab)}${k === 'basket' ? `<i class="nlsr-bk" hidden></i>` : ''}</span></button></li>`; }).join('');
  const n = window.__nlBasket && window.__nlBasket.state && window.__nlBasket.state.unit ? 1 : 0, i = el.querySelector('.nlsr-bk'); if (i && n) { i.hidden = false; i.textContent = n; }
}
function paintHint() {
  const hint = el.querySelector('.nlsr-hint'), tn = el.querySelector('.nlsr-turn'), back = el.querySelector('.nlsr-back');
  back.hidden = !S.tower;
  hint.hidden = !!S.floor; hint.querySelector('b').textContent = t(S.tower ? 'sr_hint_floor' : 'sr_hint_tower');
  tn.hidden = !S.tower || !!S.floor || S.touched;
  el.dataset.mode = S.tower ? 'tower' : 'all'; el.dataset.picked = S.floor ? '1' : '0';
  const tt = el.querySelector('.nlsr-t'); tt.textContent = S.tower ? t('sr_title_tower', { tower: S.tower }) : t('sr_title_all');
  el.querySelector('.nlsr-s').textContent = t(S.tower ? (S.floor ? 'sr_sub_picked' : 'sr_sub_tower') : 'sr_sub_all');
}
function paint() { paintHandles(); paintCard(); paintPic(); paintSteps(); paintHint(); }

/* ---------------------------------------------------------------- the moves */
function announce() { // the basket and the page hear the choice; the apartment screen opens only when asked (quiet)
  const b = sideBearing(S.tower, S.floor, S.side);
  // HAD-712: tower, floor, bearing and side are the choice (the basket renders its own words); facing and label stay the Hebrew
  // values the visit trail already records, the same in every language, so the reports do not split
  window.dispatchEvent(new CustomEvent('nl:facing', { detail: { tower: S.tower, floor: S.floor, bearing: Math.round(b), side: S.side, heightM: +eyeH(S.floor).toFixed(1), facing: dirTo(b, 'he'), label: t('tower_n', { tower: S.tower }, 'he'), source: 'showroom', quiet: true } }));
  try { history.replaceState(history.state, '', `${location.pathname}${location.search}#dira=${S.tower}${S.floor}-${Math.round(b)}`); } catch (e) { /* file: */ }
}
function openTower(k, quietly) {
  S.tower = k; S.floor = null; S.side = null; S.touched = false; S.frame = nearestFrame(k, START);
  preload(k, S.frame); preloadAround(k, S.frame); loadViews();
  const im = el.querySelector('.nlsr-img'); im.classList.add('is-in'); setTimeout(() => im.classList.remove('is-in'), 520);
  paint(); if (!quietly) ga('showroom_tower', { tower: k });
}
function toAll() { S.tower = null; S.floor = null; S.side = null; paint(); }
function pick(f, side, how) {
  S.floor = Math.min(Math.max(f, 1), turn().floors);
  if (side != null) S.side = side; else if (S.side == null) S.side = 0;
  S.touched = true; paintCard(); place(); paintBand(); paintMap(); paintSteps(); paintHint(); announce();
  ga('showroom_pick', { tower: S.tower, floor: S.floor, facing: dirFrom(sideBearing(S.tower, S.floor, S.side), 'he'), how: how || 'tap' });
}
function sideFacing(f, normal) { let best = 0, d = 999; for (let s = 0; s < 4; s++) { const x = angDiff(sideBearing(S.tower, f, s), normal); if (x < d) { d = x; best = s; } } return best; }
function tapAt(cx, cy) { // a tap on the picture: the floor under the finger, and the side of the plate that faces out there
  const im = el.querySelector('.nlsr-img').getBoundingClientRect(), x = ((cx - im.left) / im.width) * 1000, y = ((cy - im.top) / im.height) * 1000;
  const F = turn().frames[S.frame].f; let best = -1, d = 1e9;
  F.forEach((r, i) => { const my = (r[1] + r[3]) / 2, dy = Math.abs(my - y); if (dy < d) { d = dy; best = i; } });
  const r = F[best], hh = bandOf(S.frame, best + 1).hh, pad = (r[2] - r[0]) * 0.18;
  if (x < r[0] - pad || x > r[2] + pad || d > hh * 3) return false;
  const u = Math.max(-1, Math.min(1, (x - (r[0] + r[2]) / 2) / ((r[2] - r[0]) / 2)));
  pick(best + 1, sideFacing(best + 1, turn().frames[S.frame].b - Math.asin(u) * 180 / Math.PI), 'tap');
  return true;
}
let spin = null;
function turnTo(target) { // turn the tower, picture by picture, the short way round
  clearInterval(spin);
  const n = turn().frames.length;
  spin = setInterval(() => {
    if (S.frame === target) { clearInterval(spin); return; }
    const fwd = ((target - S.frame) % n + n) % n; S.frame = stepFrame(S.tower, S.frame, fwd <= n / 2 ? 1 : -1); paintPic();
  }, 55);
}
function go(where) {
  if (!S.floor) { nudge(); return; }
  if (where === 'basket') { S.done.basket = 1; paintSteps(); if (window.__nlBasket) window.__nlBasket.open(el.querySelector('[data-step="basket"]')); ga('showroom_step', { step: 'basket' }); return; }
  const b = sideBearing(S.tower, S.floor, S.side), detail = { tower: S.tower, floor: S.floor, bearing: Math.round(b), heightM: +eyeH(S.floor).toFixed(1) };
  if (!window.__nlCockpit) return;
  window.__nlCockpit.open(detail, 'showroom', where === 'home' ? null : (where === 'design' ? 'inside' : where));
  ga('showroom_step', { step: where });
}
function nudge() { const h = el.querySelector('.nlsr-hint'); h.classList.remove('is-nudge'); void h.offsetWidth; h.classList.add('is-nudge'); el.querySelector('.nlsr-stage').scrollIntoView({ behavior: 'smooth', block: 'center' }); }

/* ---------------------------------------------------------------- the hands */
function wire() {
  const st = el.querySelector('.nlsr-stage');
  let p0 = null;
  st.addEventListener('pointerdown', (e) => { if (!S.tower || e.target.closest('button,a,.nlsr-card')) return; clearInterval(spin); p0 = { x: e.clientX, y: e.clientY, t: Date.now(), f: S.frame, moved: false }; });
  st.addEventListener('pointermove', (e) => {
    if (!p0) return; const dx = e.clientX - p0.x, dy = e.clientY - p0.y;
    if (!p0.moved) { if (Math.abs(dx) < 9 || Math.abs(dx) < Math.abs(dy)) return; p0.moved = true; try { st.setPointerCapture(e.pointerId); } catch (x) { /* none */ } if (!S.touched) { S.touched = true; paintHint(); ga('showroom_turn', { tower: S.tower }); } }
    const n = turn().frames.length, want = ((p0.f + Math.round(dx / (st.clientWidth / 9))) % n + n) % n;
    if (want !== S.frame && turn().frames[want].ok) { S.frame = want; paintPic(); }
  });
  const up = (e) => { if (!p0) return; const q = p0; p0 = null; if (!q.moved && Date.now() - q.t < 600 && Math.hypot(e.clientX - q.x, e.clientY - q.y) < 10) { if (!tapAt(e.clientX, e.clientY)) nudge(); } };
  st.addEventListener('pointerup', up); st.addEventListener('pointercancel', () => { p0 = null; });
  el.addEventListener('click', (e) => {
    const t = e.target.closest('[data-tower],[data-fl],[data-side],[data-go],[data-step],[data-act],[data-ev]'); if (!t) return;
    if (t.dataset.tower) return openTower(t.dataset.tower);
    if (t.dataset.fl) return pick(S.floor + +t.dataset.fl, null, 'stepper');
    if (t.dataset.side) { const s = (S.side + 1) % 4; pick(S.floor, s, 'side'); return turnTo(nearestFrame(S.tower, sideBearing(S.tower, S.floor, s))); }
    if (t.dataset.go) return go(t.dataset.go);
    if (t.dataset.step) return t.dataset.step === 'tower' ? (S.floor ? el.querySelector('.nlsr-stage').scrollIntoView({ behavior: 'smooth', block: 'center' }) : nudge()) : go(t.dataset.step);
    if (t.dataset.act === 'all') return toAll();
    if (t.dataset.ev) ga('showroom_' + t.dataset.ev, { tower: S.tower, floor: S.floor });
  });
  st.addEventListener('keydown', (e) => { if (!S.tower) return; if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') { S.frame = stepFrame(S.tower, S.frame, e.key === 'ArrowRight' ? 1 : -1); paintPic(); e.preventDefault(); } if (S.floor && (e.key === 'ArrowUp' || e.key === 'ArrowDown')) { pick(S.floor + (e.key === 'ArrowUp' ? 1 : -1), null, 'keys'); e.preventDefault(); } });
  addEventListener('resize', place);
  addEventListener('nl:cockpit', (e) => { const k = e.detail && e.detail.screen; if (k === 'view' || k === 'home') S.done.view = 1; if (k === 'inside') { S.done.inside = 1; S.done.design = 1; } if (el) { paintSteps(); paintCard(); } });
}
function callRow() {
  const now = !!CK.availNow, room = now ? `${location.pathname}${location.search ? location.search + '&' : '?'}room=new` : '#nlsch';
  return `<a class="nlsr-call" href="${esc(room)}" data-ev="call">${esc(t(now ? 'sr_call_now' : 'sr_call'))}</a>`;
}

export function mountShowroom(at) {
  if (!at || document.querySelector('.nlsr')) return { open };
  const css = document.createElement('link'); css.rel = 'stylesheet'; css.href = WORLD + 'showroom.css' + (C.ver ? '?ver=' + C.ver : ''); document.head.appendChild(css);
  el = document.createElement('section'); el.className = 'nlsr'; el.id = 'nlsr'; el.dir = dir(); el.lang = lang(); el.setAttribute('aria-label', t('sr_aria_section'));
  el.innerHTML = `<div class="nlsr-head"><div class="nlsr-t">${esc(t('sr_title_all'))}</div><div class="nlsr-s"></div></div>
    <ol class="nlsr-steps" aria-label="${esc(t('sr_aria_steps'))}"></ol>
    <div class="nlsr-stage" tabindex="0" aria-label="${esc(t('sr_aria_stage'))}">
      <div class="nlsr-img"><img class="nlsr-pic" alt="" draggable="false" decoding="async"><svg class="nlsr-ov" viewBox="0 0 1000 1000" preserveAspectRatio="none" aria-hidden="true"></svg><div class="nlsr-handles"></div><span class="nlsr-tag" hidden></span></div>
      <span class="nlsr-cap">${esc(t('sim'))}</span>
      <button type="button" class="nlsr-back" data-act="all" hidden>${esc(t('sr_back_all'))}</button>
      <div class="nlsr-hint"><i class="nlsr-pulse-b"></i><b></b></div>
      <div class="nlsr-turn" hidden><span aria-hidden="true">↔</span> ${esc(t('sr_turn_hint'))}</div>
      <div class="nlsr-card" hidden></div>
    </div>
    <div class="nlsr-map"><img src="${esc(A('turn/map.webp'))}" alt="${esc(t('sr_alt_map'))}" loading="lazy" decoding="async">
      <svg class="nlsr-mapov" aria-hidden="true"></svg><span class="nlsr-ml nlsr-ml--sea">${esc(t('sr_map_sea'))}</span><span class="nlsr-ml nlsr-ml--n">${esc(t('sr_map_north'))}</span></div>
    <div class="nlsr-mapline" aria-live="polite"></div>
    <div class="nlsr-row">${callRow()}</div>`;
  at.parentNode.insertBefore(el, at);
  // 1.72.646: the page's own "virtual tour" links pointed at the earlier stage's heading, which the showroom replaces
  document.querySelectorAll('a[href="#nlps-t"]').forEach((x) => x.setAttribute('href', '#nlsr'));
  box = el.querySelector('.nlsr-stage');
  load().then(() => {
    const m = T.map; el.querySelector('.nlsr-mapov').setAttribute('viewBox', `${m.x0} ${-m.y1} ${m.x1 - m.x0} ${m.y1 - m.y0}`);
    wire(); paint(); restore();
    setTimeout(() => Object.keys(T.towers).forEach((k) => preload(k, nearestFrame(k, START))), 1200);
  }).catch((e) => { console.warn('[showroom]', e); el.remove(); });
  if (CK.avail) fetch(CK.avail, { credentials: 'omit', cache: 'no-store' }).then((r) => r.json()).then((j) => { if (j && j.now === true) { CK.availNow = true; const a = el.querySelector('.nlsr-row a.nlsr-call[data-ev="call"]'); if (a) a.outerHTML = callRow(); } }).catch(() => {});
  window.__nlJourney = { open };
  return { open };
}
function restore() { // a shared link (#dira=B24-262) opens on that apartment
  const m = /^#dira=([ABC])(\d+)-(\d+)/.exec(location.hash || ''); if (!m || !T.towers[m[1]]) return;
  openTower(m[1], true); const f = +m[2]; S.side = sideFacing(f, +m[3]); S.floor = Math.min(Math.max(f, 1), turn().floors); S.touched = true;
  S.frame = nearestFrame(m[1], sideBearing(m[1], S.floor, S.side)); paint();
}
function open() { if (!el) return; toAll(); el.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
