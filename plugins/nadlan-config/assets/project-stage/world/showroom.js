/* HAD-712 (12.11.2026): waymarks, view with details, floor plan; the card is a sheet (peek / expanded), docked beside the tower on desktops. */
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
const { planFloor } = await import(new URL('planfloor.js' + (C.ver ? '?ver=' + C.ver : ''), import.meta.url).href); // HAD-712 (12.11): the floor's four apartments
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
const reduced = () => { try { return matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) { return false; } };
const wide = () => innerWidth >= 900; // the card docks beside the tower (desktop), else it is a sheet over the stage's foot
const cap1 = (s) => (lang() === 'he' ? s : s.charAt(0).toUpperCase() + s.slice(1));
const shortDir = (b) => (lang() === 'fr' ? dirTo(b) : dirFrom(b)); // the noun: "מערב", "west", "ouest" (fr's nouns carry an article)
/* HAD-712 (12.11.2026): the waymarks' progress, per page, in this tab only (shared with cockpit.js under the same key) */
const WK = 'nlsr-way:' + location.pathname;
const way = {
  get() { try { return JSON.parse(sessionStorage.getItem(WK) || '{}') || {}; } catch (e) { return {}; } },
  set(k) { const o = way.get(); if (o[k]) return; o[k] = 1; try { sessionStorage.setItem(WK, JSON.stringify(o)); } catch (e) { /* private mode */ } },
};
const CK_WAY = ['ck_view', 'ck_inside', 'ck_design', 'ck_basket', 'ck_call']; // the apartment screen's order (cockpit.js paints them)

let T = null, AER = null, VIEWS = null, el = null, box = null, plan = null, DET = null;
const S = { tower: null, frame: 0, floor: null, side: null, touched: false, sideChosen: false, sheet: 'peek', rechoose: false }; // sheet: 'peek' | 'open'
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
function loadDetails() { if (DET) return; DET = { marks: [], places: [] }; fetch(A('details.json'), { credentials: 'omit' }).then((r) => r.json()).then((j) => { DET = j; if (el) paintMap(); }).catch(() => {}); }
function loadViews() { if (VIEWS || !C.data) return; VIEWS = []; fetch(C.data, { credentials: 'omit' }).then((r) => r.json()).then((j) => { VIEWS = (j.views || []).filter((v) => v.tod === 'day' && v.bearing != null && v.side != null); paintCard(); }).catch(() => {}); }
function viewOf(k, f, b) { const L = (VIEWS || []).filter((v) => v.tower === k && angDiff(v.bearing, b) <= 30).sort((x, y) => Math.abs(x.floor - f) - Math.abs(y.floor - f)); return L[0] || null; }

/* ---------------------------------------------------------------- the picture: placed by hand, so a tap and a floor band agree */
const PIC = { all: [800, 1067, 0.56], tower: [756, 1080, 0.525] }; // width, height, the height share kept at the box's middle
function place() {
  if (!box) return;
  const [pw, ph, mid] = S.tower ? PIC.tower : PIC.all, W = box.clientWidth, H = box.clientHeight;
  let sc = Math.max(W / pw, H / ph), w = pw * sc, h = ph * sc;
  let top = Math.min(0, Math.max(H - h, H / 2 - h * mid));
  if (S.tower && S.floor) {
    // HAD-712 (12.11, Ben: "the card hides the model"): the chosen floor's band is never under the sheet, and with the sheet at
    // peek the whole tower (lowest to highest floor) stays above it, the picture a little smaller when it must be
    const card = el.querySelector('.nlsr-card'), over = card && !card.hidden && card.parentNode === box, free = H - (over ? card.offsetHeight : 0);
    const F = turn().frames[S.frame].f, n = F.length, hb = bandOf(S.frame, S.floor).hh / 1000, r = F[S.floor - 1];
    const lo1 = Math.max(F[0][1], F[0][3]) / 1000 + hb, hiN = Math.min(F[n - 1][1], F[n - 1][3]) / 1000 - hb, yb = (r[1] + r[3]) / 2000;
    const pad = 8, hint = el.querySelector('.nlsr-hint'), pt = hint && !hint.hidden ? hint.offsetTop + hint.offsetHeight + 4 : pad;
    if (over && S.sheet !== 'open') { const fit = (free - 2 * pad) / ((lo1 - hiN) * ph); if (fit < sc) { sc = Math.max(fit, sc * 0.78); w = pw * sc; h = ph * sc; } }
    top = free * 0.56 - yb * h;
    const a = pad - hiN * h, b = free - pad - lo1 * h; // the whole tower inside the free part, when it fits
    if (a <= b + 1) top = Math.min(Math.max(a, b), Math.max(a, top));
    top = Math.min(top, 0); top = Math.max(top, Math.min(0, free - h)); // no gap above the picture, none above the sheet
    top = Math.min(free - pad - (yb + hb) * h, Math.max(pt - (yb - hb) * h, top)); // the chosen band wins: always in sight
  }
  const left = (W - w) / 2;
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
  hs.innerHTML = Object.keys(tw).sort().map((k) => { const p = tw[k][Math.floor(tw[k].length * 0.72)]; return `<button type="button" class="nlsr-h" data-tower="${k}" style="left:${(p[0] * 100).toFixed(2)}%;top:${(p[1] * 100).toFixed(2)}%" aria-label="${esc(t('sr_aria_tower_handle', { tower: k }))}">${k}</button>`; }).join('');
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
  if (!DET) loadDetails();
  let h = '', beamB = null, from = null;
  for (const k of Object.keys(m.towers).sort()) { const [x, y] = m.towers[k], on = k === S.tower; h += `<circle class="nlsr-tw${on ? ' is-on' : ''}" cx="${x}" cy="${-y}" r="${on ? 44 : 30}"/>`; }
  if (S.tower) {
    const [x, y] = m.towers[S.tower]; from = [x, y];
    if (S.side != null && S.floor) {
      const b = sideBearing(S.tower, S.floor, S.side), R = 3200, a1 = (b - 26) * Math.PI / 180, a2 = (b + 26) * Math.PI / 180;
      beamB = b;
      h = `<path class="nlsr-beam${sv.querySelector('.nlsr-beam') ? ' is-still' : ''}" d="M${P(x, y)} L${P(x + R * Math.sin(a1), y + R * Math.cos(a1))} L${P(x + R * Math.sin(a2), y + R * Math.cos(a2))} Z"/>` + h;
      const win = windowNames(from, b);
      line.innerHTML = t('sr_map_facing', { dir: esc(dirTo(b)), sector: esc(sectorOf(b)) }) + (win ? '<br>' + t('sr_map_window', { names: esc(win) }) : '');
    } else {
      const cb = turn().frames[S.frame].b * Math.PI / 180, ex = x + 210 * Math.sin(cb), ey = y + 210 * Math.cos(cb);
      h += `<path class="nlsr-eyeline" d="M${P(ex, ey)} L${P(x, y)}"/><circle class="nlsr-eye" cx="${ex.toFixed(0)}" cy="${(-ey).toFixed(0)}" r="34"/>`;
      line.innerHTML = t('sr_map_looking', { tower: esc(S.tower), dir: esc(dirFrom(turn().frames[S.frame].b)) });
    }
  } else line.innerHTML = t('sr_map_intro');
  sv.innerHTML = h;
  mapLabels(from, beamB);
}
/* HAD-712 (12.11.2026, Ben: "many details on the map"; boards P3/Q3): the places and landmarks of hamedina/details.json (the same
   positions view-with-details projects) named on the small map; those in the beam stand out, the beam's landmarks beyond the map's
   edge get a chip at the edge on their true bearing, and the line under the map names them ("in the window's direction", never a
   promise of the view itself) */
const brg = (f, x, y) => ((Math.atan2(x - f[0], y - f[1]) * 180 / Math.PI) + 360) % 360;
const nameOf = (q) => { const L = lang(); return q[L] || (L === 'fr' && q.fr_name) || q.en || ''; };
function detailRows(f) {
  if (!DET || !DET.places) return [];
  return DET.marks.map((q) => ({ ...q, mark: 1 })).concat(DET.places).map((q) => ({ q, name: nameOf(q), X: q.x, Y: -q.z, d: Math.hypot(q.x - f[0], -q.z - f[1]) })).filter((r) => r.name && r.d > 60);
}
function windowNames(f, b) {
  const rows = detailRows(f).filter((r) => angDiff(brg(f, r.X, r.Y), b) <= 26 && r.d <= (r.q.mark ? 4500 : 1500));
  const pick = rows.filter((r) => r.q.mark).sort((a, c) => a.d - c.d).slice(0, 3);
  for (const r of rows.filter((x) => !x.q.mark).sort((a, c) => a.d - c.d)) { if (pick.length >= 3) break; pick.push(r); }
  if (!pick.length) return '';
  const names = pick.sort((a, c) => a.d - c.d).map((r) => r.name);
  try { return new Intl.ListFormat(lang(), { style: 'long', type: 'conjunction' }).format(names); } catch (e) { return names.join(', '); }
}
function mapLabels(from, b) {
  const mb = el.querySelector('.nlsr-map'); if (!mb) return;
  let lay = mb.querySelector('.nlsr-mlx'); if (!lay) { lay = document.createElement('div'); lay.className = 'nlsr-mlx'; lay.setAttribute('aria-hidden', 'true'); mb.appendChild(lay); }
  lay.textContent = '';
  const m = T.map, cw = mb.clientWidth, ch = mb.clientHeight; if (!cw || !ch || !DET || !DET.places) return;
  const W = m.x1 - m.x0, H = m.y1 - m.y0, f = from || [0, 0];
  const px = (x) => (x - m.x0) / W * cw, py = (y) => (m.y1 - y) / H * ch;
  const o = mb.getBoundingClientRect();
  const taken = [...mb.querySelectorAll('.nlsr-ml')].map((e) => { const r = e.getBoundingClientRect(); return { l: r.left - o.left, r: r.right - o.left, t: r.top - o.top, b: r.bottom - o.top }; });
  const hit = (a) => taken.some((q) => a.l < q.r + 3 && a.r > q.l - 3 && a.t < q.b + 2 && a.b > q.t - 2);
  const rows = detailRows(f).map((r) => ({ ...r, beam: b != null && angDiff(brg(f, r.X, r.Y), b) <= 26 }));
  const inside = rows.filter((r) => r.X > m.x0 + W * 0.02 && r.X < m.x1 - W * 0.02 && r.Y > m.y0 + H * 0.05 && r.Y < m.y1 - H * 0.05)
    .sort((a, c) => (c.beam - a.beam) || ((c.q.mark || 0) - (a.q.mark || 0)) || (a.d - c.d));
  const cap = cw < 520 ? 4 : 7; let n = 0;
  for (const r of inside) {
    if (n >= cap) break;
    const x = px(r.X), y = py(r.Y);
    const s = document.createElement('span'); s.className = 'nlsr-pl' + (r.beam ? ' is-beam' : ''); s.textContent = r.name; s.style.visibility = 'hidden'; lay.appendChild(s);
    const w = s.offsetWidth, hh = s.offsetHeight; if (!w || w > cw - 6) { s.remove(); continue; }
    const l = Math.min(Math.max(x - w / 2, 3), cw - w - 3); let tp = y - hh - 5; if (tp < 2) tp = y + 5;
    const a = { l, r: l + w, t: tp, b: tp + hh };
    if (hit(a) || a.b > ch - 2) { s.remove(); continue; }
    taken.push(a); n++;
    s.style.left = (l / cw * 100).toFixed(2) + '%'; s.style.top = (tp / ch * 100).toFixed(2) + '%'; s.style.visibility = '';
    const d = document.createElement('i'); d.className = 'nlsr-pd' + (r.beam ? ' is-beam' : ''); d.style.left = (x / cw * 100).toFixed(2) + '%'; d.style.top = (y / ch * 100).toFixed(2) + '%'; lay.appendChild(d);
  }
  if (b == null || !from) return;
  const ARW = ['↑', '↗', '→', '↘', '↓', '↙', '←', '↖'];
  const far = rows.filter((r) => r.beam && r.q.mark && r.d <= 4500 && !inside.includes(r)).sort((a, c) => a.d - c.d).slice(0, 2);
  for (const r of far) {
    const br = brg(f, r.X, r.Y), dx = Math.sin(br * Math.PI / 180), dy = Math.cos(br * Math.PI / 180);
    const xi = [m.x0 + W * 0.03, m.x1 - W * 0.03], yi = [m.y0 + H * 0.08, m.y1 - H * 0.08];
    let k = Infinity;
    if (Math.abs(dx) > 1e-6) k = Math.min(k, ((dx > 0 ? xi[1] : xi[0]) - f[0]) / dx);
    if (Math.abs(dy) > 1e-6) k = Math.min(k, ((dy > 0 ? yi[1] : yi[0]) - f[1]) / dy);
    const x = px(f[0] + dx * k), y = py(f[1] + dy * k);
    const s = document.createElement('span'); s.className = 'nlsr-pe'; s.textContent = r.name + ' ' + ARW[Math.round(br / 45) % 8]; s.style.visibility = 'hidden'; lay.appendChild(s);
    const w = s.offsetWidth, hh = s.offsetHeight; if (!w || w > cw - 6) { s.remove(); continue; }
    const l = Math.min(Math.max(x - w / 2, 3), cw - w - 3), tp = Math.min(Math.max(y - hh / 2, 2), ch - hh - 2);
    const a = { l, r: l + w, t: tp, b: tp + hh }; if (hit(a)) { s.remove(); continue; }
    taken.push(a); s.style.left = (l / cw * 100).toFixed(2) + '%'; s.style.top = (tp / ch * 100).toFixed(2) + '%'; s.style.visibility = '';
  }
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
  if (plan) { plan.destroy(); plan = null; }
  if (!S.tower || !S.floor) { c.hidden = true; return; }
  dock(c);
  const b = sideBearing(S.tower, S.floor, S.side), v = viewOf(S.tower, S.floor, b), wa = waHref(), open = wide() || S.sheet === 'open';
  const first = c.hidden; c.hidden = false; c.dataset.sheet = open ? 'open' : 'peek';
  // HAD-712 (12.11.2026, Ben: "the card hides the model, it cannot be dismissed"): one row at the stage's foot (peek), the rest on
  // the handle, the row or a swipe up; the same markup docks beside the tower on a desktop, always open there
  const title = t('sr_peek_title', { tower: esc(S.tower), floor: S.floor, dir: esc(shortDir(b)) });
  c.innerHTML = `<div class="nlsr-peek">${v ? `<img class="nlsr-cview" src="${esc(A(v.img))}" alt="${esc(t('sr_alt_card_view'))}">` : ''}
      <div class="nlsr-ct" title="${esc(title.replace(/<\/?bdi>/g, ''))}">${title}</div>
      <div class="nlsr-pctl"><div class="nlsr-cstep"><button type="button" data-fl="-1" aria-label="${esc(t('sr_aria_floor_down'))}">−</button><button type="button" data-fl="1" aria-label="${esc(t('sr_aria_floor_up'))}">+</button></div>
        <button type="button" class="nlsr-go" data-go="home">${esc(t('sr_card_enter'))}</button></div>
      <button type="button" class="nlsr-grab" data-sheet-t aria-expanded="${open}" aria-controls="nlsr-more" aria-label="${esc(t(open ? 'sr_sheet_less' : 'sr_sheet_more'))}"><i aria-hidden="true"></i><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 14l6-6 6 6"/></svg></button></div>
    <div class="nlsr-more" id="nlsr-more"${open ? '' : ' hidden'}><div class="nlsr-plan"></div>
      <div class="nlsr-mcol"><div class="nlsr-cf">${esc(facingText())}</div><small class="nlsr-pill">${esc(t('sr_plan_ill'))}</small>
        <button type="button" class="nlsr-cside" data-side="next">${esc(t('sr_card_other_side'))}</button>
        ${wa ? `<a class="nlsr-ask" href="${esc(wa)}" target="_blank" rel="noopener" data-ev="ask">${esc(t('sr_card_ask'))}</a>` : ''}</div></div>`;
  if (open) { // the floor plan: the four apartments, the chosen one lit; a tap there moves the side as the old control does
    plan = planFloor(c.querySelector('.nlsr-plan'), { lang: lang(), plate: plateAt(S.tower, S.floor), names: (bb) => cap1(shortDir(bb)),
      pick: (s) => { S.sideChosen = true; way.set('plan'); if (s === S.side) { paintWay(); return; } pick(S.floor, s, 'plan'); turnTo(nearestFrame(S.tower, sideBearing(S.tower, S.floor, s))); } });
    plan.set({ side: S.side, pulse: false });
  }
  if (first && !wide()) { // the handle nudges once a visit (down and back), never with reduced motion
    let seen = false; try { seen = !!sessionStorage.getItem('nlsr-sheet-nudge'); sessionStorage.setItem('nlsr-sheet-nudge', '1'); } catch (e) { /* none */ }
    if (!seen && !reduced()) { const g = c.querySelector('.nlsr-grab'); g.classList.add('is-nudge'); setTimeout(() => { const x = el.querySelector('.nlsr-grab'); if (x) x.classList.remove('is-nudge'); }, 1300); }
  }
  paintWay();
}
function dock(c) { // a desktop: the card sits in the reading column beside the tower; a phone: over the stage's foot
  const want = wide() ? el : box, before = wide() ? el.querySelector('.nlsr-map') : null;
  if (c.parentNode !== want) want.insertBefore(c, before);
}
function setSheet(v, how) { // 'open' | 'peek'; how: handle, row, swipe, stage, esc
  if (wide() || !S.floor || S.sheet === v) return;
  S.sheet = v; paintCard(); place(); paintBand();
  ga(v === 'open' ? 'sheet_expand' : 'sheet_collapse', { how, tower: S.tower, floor: S.floor });
}
/* ---------------------------------------------------------------- the waymarks (HAD-712, Ben 11.11.2026: "every next step blinks
   so people understand where to tap; a short line beside it says what to do; it stops on the tap"): exactly one element pulses,
   the next step; the label is the hint pill; the step bar shows the state without pulsing; the apartment screen paints its own */
function nextWay() {
  if (!S.tower) return 'tower';
  if (!S.floor || S.rechoose) return 'floor'; // HAD-712 (12.11): the tower dragged again after a pick: "tap a floor" comes back
  const d = way.get();
  if (!S.sideChosen && !d.plan) return 'plan'; // a floor tapped on the tower already chose its side: skipped then
  if (!d.enter || CK_WAY.some((k) => !d[k])) return 'enter'; // the rest happens in the apartment screen
  return null;
}
const cockpitOpen = () => { const c = document.getElementById('nlck'); return !!(c && !c.hidden); };
let cyc = null;
function paintWay() {
  if (!el) return;
  clearInterval(cyc); cyc = null;
  el.querySelectorAll('.nlsr-pulse,.nlsr-pulse-b').forEach((x) => x.classList.remove('nlsr-pulse', 'nlsr-pulse-b'));
  const hint = el.querySelector('.nlsr-hint'), k = cockpitOpen() ? null : nextWay();
  el.dataset.way = k || '';
  hint.hidden = !k;
  const cap = el.querySelector('.nlsr-cap'), back = el.querySelector('.nlsr-back');
  if (k) {
    hint.querySelector('b').textContent = t({ tower: 'sr_hint_tower', floor: 'sr_hint_floor', plan: 'way_plan', enter: 'way_enter' }[k]);
    if (box && box.clientWidth) hint.style.maxWidth = Math.max(170, box.clientWidth - cap.offsetWidth - 34) + 'px'; // beside the caption, never over it
  }
  back.style.top = Math.max(58, k ? hint.offsetTop + hint.offsetHeight + 8 : 0) + 'px'; // "‹ All three towers" stays under the line
  if (!k) return;
  let tg = null;
  if (k === 'tower') {
    const hs = [...el.querySelectorAll('.nlsr-h')]; tg = hs[0] || null;
    if (hs.length > 1 && !reduced()) { let i = 0; cyc = setInterval(() => { if (!hs[i].isConnected) { clearInterval(cyc); return; } hs[i].classList.remove('nlsr-pulse'); i = (i + 1) % hs.length; hs[i].classList.add('nlsr-pulse'); }, 1600); }
  } else if (k === 'floor') tg = hint.querySelector('i'); // the target is the picture itself: the pill's dot marks it, the line says it
  else if (k === 'plan') tg = el.querySelector('.nlsr-more:not([hidden]) .nlsr-plan') || el.querySelector('.nlsr-grab');
  else tg = el.querySelector('.nlsr-go');
  if (tg) tg.classList.add(k === 'floor' ? 'nlsr-pulse-b' : 'nlsr-pulse');
}
function paintSteps() {
  const d = way.get(), done = { tower: !!S.floor, view: !!d.ck_view, inside: !!d.ck_inside, design: !!d.ck_design, basket: !!d.ck_basket };
  const nx = !S.floor ? 'tower' : (STEPS.slice(1).find(([k]) => !done[k]) || [null])[0];
  el.querySelector('.nlsr-steps').innerHTML = STEPS.map(([k, lab], i) => { const on = k === nx; // the bar shows the state; only the next target pulses
    return `<li><button type="button" class="nlsr-st${done[k] ? ' is-done' : ''}${on ? ' is-on' : ''}" data-step="${k}"${on ? ' aria-current="step"' : ''}><span class="nlsr-sn">${done[k] ? '✓' : i + 1}</span><span class="nlsr-sl">${t(lab)}${k === 'basket' ? `<i class="nlsr-bk" hidden></i>` : ''}</span></button></li>`; }).join('');
  const n = window.__nlBasket && window.__nlBasket.state && window.__nlBasket.state.unit ? 1 : 0, i = el.querySelector('.nlsr-bk'); if (i && n) { i.hidden = false; i.textContent = n; }
}
function paintHint() {
  const tn = el.querySelector('.nlsr-turn'), back = el.querySelector('.nlsr-back');
  back.hidden = !S.tower;
  tn.hidden = !S.tower || !!S.floor || S.touched;
  el.dataset.mode = S.tower ? 'tower' : 'all'; el.dataset.picked = S.floor ? '1' : '0';
  const tt = el.querySelector('.nlsr-t'); tt.textContent = S.tower ? t('sr_title_tower', { tower: S.tower }) : t('sr_title_all');
  el.querySelector('.nlsr-s').textContent = t(S.tower ? (S.floor ? 'sr_sub_picked' : 'sr_sub_tower') : 'sr_sub_all');
  paintWay();
}
function paint() { paintHandles(); paintHint(); paintCard(); paintPic(); paintSteps(); }

/* ---------------------------------------------------------------- the moves */
function announce() { // the basket and the page hear the choice; the apartment screen opens only when asked (quiet)
  const b = sideBearing(S.tower, S.floor, S.side);
  // HAD-712: tower, floor, bearing and side are the choice (the basket renders its own words); facing and label stay the Hebrew
  // values the visit trail already records, the same in every language, so the reports do not split
  window.dispatchEvent(new CustomEvent('nl:facing', { detail: { tower: S.tower, floor: S.floor, bearing: Math.round(b), side: S.side, heightM: +eyeH(S.floor).toFixed(1), facing: dirTo(b, 'he'), label: t('tower_n', { tower: S.tower }, 'he'), source: 'showroom', quiet: true } }));
  try { history.replaceState(history.state, '', `${location.pathname}${location.search}#dira=${S.tower}${S.floor}-${Math.round(b)}`); } catch (e) { /* file: */ }
}
function openTower(k, quietly) {
  if (S.floor && !quietly) ga('tower_change_after_card', { from: S.tower, to: k }); // HAD-712 (12.11): another tower with the card up
  S.tower = k; S.floor = null; S.side = null; S.touched = false; S.sideChosen = false; S.sheet = 'peek'; S.rechoose = false; S.frame = nearestFrame(k, START);
  preload(k, S.frame); preloadAround(k, S.frame); loadViews(); loadDetails();
  const im = el.querySelector('.nlsr-img'); im.classList.add('is-in'); setTimeout(() => im.classList.remove('is-in'), 520);
  paint(); if (!quietly) ga('showroom_tower', { tower: k });
}
function toAll() { if (S.floor) ga('tower_change_after_card', { from: S.tower, to: 'all' }); S.tower = null; S.floor = null; S.side = null; S.sideChosen = false; S.sheet = 'peek'; paint(); }
function pick(f, side, how) {
  const had = S.floor;
  S.rechoose = false;
  S.floor = Math.min(Math.max(f, 1), turn().floors);
  if (side != null) S.side = side; else if (S.side == null) S.side = 0;
  if (how === 'tap' || how === 'side' || how === 'plan') S.sideChosen = true; // a floor tapped on the tower names its side too
  if (had && had !== S.floor) ga('floor_change_after_card', { tower: S.tower, from: had, to: S.floor, how: how || 'tap' });
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
  if (where === 'basket') { way.set('ck_basket'); paintSteps(); paintWay(); if (window.__nlBasket) window.__nlBasket.open(el.querySelector('[data-step="basket"]')); ga('showroom_step', { step: 'basket' }); return; }
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
  // HAD-712 (12.11): touching or dragging the tower (or the map) drops an open sheet to peek: by intent, never by a clock
  st.addEventListener('pointerdown', (e) => { if (!S.tower || e.target.closest('button,a,.nlsr-card')) return; clearInterval(spin); if (S.sheet === 'open') setSheet('peek', 'stage'); p0 = { x: e.clientX, y: e.clientY, t: Date.now(), f: S.frame, moved: false }; });
  el.querySelector('.nlsr-map').addEventListener('pointerdown', () => { if (S.sheet === 'open') setSheet('peek', 'stage'); });
  st.addEventListener('pointermove', (e) => {
    if (!p0) return; const dx = e.clientX - p0.x, dy = e.clientY - p0.y;
    if (!p0.moved) { if (Math.abs(dx) < 9 || Math.abs(dx) < Math.abs(dy)) return; p0.moved = true; try { st.setPointerCapture(e.pointerId); } catch (x) { /* none */ } if (!S.touched) { S.touched = true; paintHint(); ga('showroom_turn', { tower: S.tower }); } if (S.floor && !S.rechoose) { S.rechoose = true; paintWay(); } }
    const n = turn().frames.length, want = ((p0.f + Math.round(dx / (st.clientWidth / 9))) % n + n) % n;
    if (want !== S.frame && turn().frames[want].ok) { S.frame = want; paintPic(); }
  });
  const up = (e) => { if (!p0) return; const q = p0; p0 = null; if (!q.moved && Date.now() - q.t < 600 && Math.hypot(e.clientX - q.x, e.clientY - q.y) < 10) { if (!tapAt(e.clientX, e.clientY)) nudge(); } };
  st.addEventListener('pointerup', up); st.addEventListener('pointercancel', () => { p0 = null; });
  // the sheet: a swipe up opens it, a swipe down folds it (the row and the handle; the page does not scroll under that drag)
  let g0 = null, swiped = 0;
  el.addEventListener('pointerdown', (e) => { const c = e.target.closest('.nlsr-card'); if (!c || wide() || c.parentNode !== box || e.target.closest('.nlsr-more')) return; g0 = { y: e.clientY, x: e.clientX, id: e.pointerId }; });
  el.addEventListener('pointermove', (e) => { if (!g0 || e.pointerId !== g0.id) return; const dy = e.clientY - g0.y; if (Math.abs(dy) > 10 && Math.abs(dy) > Math.abs(e.clientX - g0.x)) e.preventDefault(); });
  const gUp = (e) => { if (!g0 || e.pointerId !== g0.id) return; const dy = e.clientY - g0.y, dx = e.clientX - g0.x; g0 = null;
    if (Math.abs(dy) > 30 && Math.abs(dy) > Math.abs(dx)) { swiped = Date.now(); setSheet(dy < 0 ? 'open' : 'peek', 'swipe'); } };
  el.addEventListener('pointerup', gUp); el.addEventListener('pointercancel', () => { g0 = null; });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && S.sheet === 'open' && !wide() && !cockpitOpen()) setSheet('peek', 'esc'); });
  el.addEventListener('click', (e) => {
    if (Date.now() - swiped < 400) return; // the click that ends a swipe
    const g = e.target.closest('[data-sheet-t]'); if (g) return setSheet(S.sheet === 'open' ? 'peek' : 'open', 'handle');
    const t = e.target.closest('[data-tower],[data-fl],[data-side],[data-go],[data-step],[data-act],[data-ev]');
    if (!t) { if (e.target.closest('.nlsr-peek') && S.sheet !== 'open') setSheet('open', 'row'); return; }
    if (t.dataset.tower) return openTower(t.dataset.tower);
    if (t.dataset.fl) return pick(S.floor + +t.dataset.fl, null, 'stepper');
    if (t.dataset.side) { const s = (S.side + 1) % 4; pick(S.floor, s, 'side'); return turnTo(nearestFrame(S.tower, sideBearing(S.tower, S.floor, s))); }
    if (t.dataset.go) return go(t.dataset.go);
    if (t.dataset.step) return t.dataset.step === 'tower' ? (S.floor ? el.querySelector('.nlsr-stage').scrollIntoView({ behavior: 'smooth', block: 'center' }) : nudge()) : go(t.dataset.step);
    if (t.dataset.act === 'all') return toAll();
    if (t.dataset.ev) ga('showroom_' + t.dataset.ev, { tower: S.tower, floor: S.floor });
  });
  st.addEventListener('keydown', (e) => { if (!S.tower) return; if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') { S.frame = stepFrame(S.tower, S.frame, e.key === 'ArrowRight' ? 1 : -1); paintPic(); e.preventDefault(); } if (S.floor && (e.key === 'ArrowUp' || e.key === 'ArrowDown')) { pick(S.floor + (e.key === 'ArrowUp' ? 1 : -1), null, 'keys'); e.preventDefault(); } });
  let wasWide = wide();
  addEventListener('resize', () => { if (wide() !== wasWide) { wasWide = wide(); paintCard(); } place(); paintBand(); });
  // the apartment screen opened (the step "inside" is taken) or closed: the waymarks move on
  addEventListener('nl:cockpit', (e) => { if (e.detail && e.detail.screen) way.set('enter'); if (el) { paintSteps(); paintWay(); } });
  // HAD-712 (12.11): the basket's "Step inside and choose a style" opens this apartment's inside in the apartment screen (basket.js reads
  // this before world.js's own __nlInsideGo, which the earlier 3D stage sets for its example apartment once it loads)
  window.__nlShowroomInside = () => go('inside');
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
      <div class="nlsr-hint" role="status"><i></i><b></b></div>
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
  S.sideChosen = true; S.frame = nearestFrame(m[1], sideBearing(m[1], S.floor, S.side)); paint();
}
function open() { if (!el) return; toAll(); el.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
