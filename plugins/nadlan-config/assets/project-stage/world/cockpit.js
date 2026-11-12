/* HAD-712 (12.11.2026): waymarks, view with details, floor plan (the apartment screen's waymarks, the view with details, the live 3D on a tap, My selection in the bar). */
/* HAD-712 (11.11.2026): words from showroom-i18n.js; direction from the page language. */
/*
 * The apartment cockpit, version 2 (HAD-699, Ben 10.11.2026: "a person presses, he enters the cockpit of his life... from there
 * everything: the view, information, plans, designing the apartment, everything, on the phone"). Design: the canvas
 * https://claude.ai/artifact/FzvFDybiyBoi8bspoPV9Zp, row "הקוקפיט של הדירה".
 * A full-screen app for the chosen apartment: the real view from it at the top, nine tiles below, each opening full screen and
 * coming back to the apartment: the view (every rendered floor and direction), inside in 360 (the example apartment, four
 * styles), another apartment (back to the journey; the old designer left on Ben's word, 10.11 night), the plan, the facilities in 360,
 * price and cost, the neighbourhood, the film, compare and send. The video call is always at the bottom (the site's shared room
 * when a representative is available, else the booking band). The choice lives in the address (#dira=A30-262).
 *
 *   window.__nlCockpitCfg = { data, places, base, ver, wa, avail }; import('.../world/cockpit.js')
 *   opens on the world's nl:facing event (the journey fires it too); window.__nlCockpit.open(detail) does the same.
 *
 * Honesty (the site's language law): numbers from cockpit.json with their sources; examples say "דוגמה"; every picture says
 * "הדמיה להמחשה"; the inside is the example apartment and says so; no new WhatsApp wording (the page's own link).
 */
const C = window.__nlCockpitCfg || {};
const { t, lang, dir, isRtl, nf, dw, placeName } = await import(new URL('showroom-i18n.js' + (C.ver ? '?ver=' + C.ver : ''), import.meta.url).href); // HAD-712: he, en, fr
const $ = (s, r = document) => r.querySelector(s);
const esc = (s) => String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const num = (n, d = 0) => nf(n, d); // he-IL, en-GB or fr-FR by the page language
const bdi = (s) => `<bdi>${esc(s)}</bdi>`;
const ils = (n, d = 0) => t('money', { n: bdi(num(n, d)) });
const A = (p) => (C.base || '') + p + (C.ver ? (p.includes('?') ? '&' : '?') + 'ver=' + C.ver : '');
const ga = (n, p) => { try { if (window.nadlanGA) window.nadlanGA(n, Object.assign({ project: 'hamedina' }, p || {})); } catch (e) { /* none */ } };
const store = { get(k, d) { try { const v = localStorage.getItem(k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } }, set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* private mode */ } } };
const angDiff = (a, b) => Math.abs(((a - b) % 360 + 540) % 360 - 180);
const DIRS = ['dir_to_n', 'dir_to_ne', 'dir_to_e', 'dir_to_se', 'dir_to_s', 'dir_to_sw', 'dir_to_w', 'dir_to_nw']; // keys of showroom-i18n.js
const dirWord = (b, L) => t(DIRS[Math.round((((b % 360) + 360) % 360) / 45) % 8], null, L); // L 'he': the analytics keep their Hebrew value
const SECTORS = [[245, 300, 'sec_sea_city'], [300, 345, 'sec_sea_yarkon'], [345, 30, 'sec_yarkon_north'], [30, 75, 'sec_ramat_aviv'], [75, 120, 'sec_ramat_gan'], [120, 200, 'sec_city_towers'], [200, 245, 'sec_old_north']];
const sectorOf = (b) => { b = ((b % 360) + 360) % 360; const s = SECTORS.find(([lo, hi]) => (lo < hi ? b >= lo && b < hi : b >= lo || b < hi)); return s ? t(s[2]) : ''; };
const eyeH = (f) => (f - 1) * 4 + 1.6;
const GROUPS = ['education', 'food', 'essentials', 'transport', 'outdoors', 'health', 'community']; // words: ck_grp_<group>; place kinds: ck_kind_<kind>
const PANOS = [['living360-c30w-sunset', 'ck_pano_original'], ['living360-c30w-sunset-warm', 'style_warm'], ['living360-c30w-sunset-light', 'style_light'], ['living360-c30w-sunset-stone', 'style_stone']];
const FACS = [['fac-pool-c', 'ck_fac_pool'], ['fac-gym-c', 'ck_fac_gym'], ['fac-spa-c', 'ck_fac_spa'], ['fac-lobby-c', 'ck_fac_lobby'], ['fac-parking-c', 'ck_fac_parking']];
const ICON = {
  video: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="6" width="13" height="12" rx="2"/><path d="M16 10l5-3v10l-5-3"/></svg>',
  wa: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20l1.3-3.9A8 8 0 1 1 8 19z"/><path d="M9 9.5c.5 2 2.5 4 4.5 4.5l1.2-1.2 2 1-.5 1.7c-3.5.4-8-4-7.6-7.6L10.3 7l1 2z"/></svg>',
  heart: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/></svg>',
  bag: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 8h14l-1.2 12H6.2z"/><path d="M9 8V6.5a3 3 0 0 1 6 0V8"/></svg>',
};
/* HAD-712 (12.11.2026): the waymarks of the apartment screen, in the order Ben gave: the view (with details), inside 360, a finish,
   My selection, the video call. Exactly one element pulses (showroom.css .nlsr-pulse), a line above the bar says what to do; the
   progress is shared with showroom.js (sessionStorage, this page, this tab) */
const WK = 'nlsr-way:' + location.pathname;
const way = {
  get() { try { return JSON.parse(sessionStorage.getItem(WK) || '{}') || {}; } catch (e) { return {}; } },
  set(k) { const o = way.get(); if (o[k]) return; o[k] = 1; try { sessionStorage.setItem(WK, JSON.stringify(o)); } catch (e) { /* private mode */ } },
};
const WAY = ['ck_view', 'ck_inside', 'ck_design', 'ck_basket', 'ck_call'];
const PSTYLE = ['bare', 'warm', 'light', 'stone']; // PANOS index -> the basket's style key (nl:view)
let vdOn = true, VD = null, from3d = false; const vds = []; // the view with details: on when the view first opens

let D = null, PL = null, el = null, cur = null, avail = null, open = null, viaJourney = false;
const calc = { price: null, extra: false, size: null, share: null, years: null, rate: null, fee: null };
const sub = { pano: 0, fac: 0, view: null };

function load() {
  if (D) return Promise.resolve(D);
  return fetch(C.data, { credentials: 'omit' }).then((r) => r.json()).then((j) => {
    D = j;
    calc.price = D.defaults.price; calc.size = D.defaults.size; calc.share = D.defaults.share; calc.years = D.defaults.years; calc.rate = D.mortgage.rate;
    calc.fee = D.fee ? D.defaults.fee : 0;
    return D;
  });
}
function loadPlaces() { if (PL || !C.places) return Promise.resolve(PL); return fetch(C.places, { credentials: 'omit' }).then((r) => r.json()).then((j) => (PL = j)).catch(() => null); }
function askAvail() {
  if (avail !== null || !C.avail) return;
  avail = false;
  fetch(C.avail, { credentials: 'omit', cache: 'no-store' }).then((r) => r.json()).then((j) => { avail = !!(j && j.now === true); paintBar(); }).catch(() => {});
}
function taxOf(p, brackets) { let t = 0, lo = 0; for (const [hi, r] of brackets) { const top = hi == null ? Infinity : hi; if (p > lo) t += (Math.min(p, top) - lo) * r; lo = top; } return Math.round(t); }
function monthly(P, ratePct, years) { const r = ratePct / 100 / 12, n = years * 12; if (!(P > 0) || !(n > 0)) return 0; return r ? (P * r) / (1 - Math.pow(1 + r, -n)) : P / n; }

/* ---------------------------------------------------------------- the views of this apartment */
function rendered() { return (D.views || []).filter((v) => v.tod === 'day' && v.bearing != null && v.big); }
function viewOf(c) { // the rendered window nearest to this apartment: same tower and direction, nearest floor
  const L = rendered().filter((v) => v.tower === c.tower && angDiff(v.bearing, c.bearing) <= 30).sort((a, b) => Math.abs(a.floor - c.floor) - Math.abs(b.floor - c.floor));
  return L[0] || null;
}
function sidesOf(c) { // the other directions on the nearest rendered floor of this tower
  const f = rendered().filter((v) => v.tower === c.tower && v.side != null).map((v) => v.floor).sort((a, b) => Math.abs(a - c.floor) - Math.abs(b - c.floor))[0];
  return rendered().filter((v) => v.tower === c.tower && v.side != null && v.floor === f);
}
function floorsOf(c) { // the same direction on the other rendered floors
  return rendered().filter((v) => v.tower === c.tower && angDiff(v.bearing, c.bearing) <= 30).sort((a, b) => a.floor - b.floor);
}
function insideOf(c) { // the living room 360 nearest to this apartment (HAD-710): same tower and direction, nearest rendered floor
  const L = (D.inside || []).filter((v) => v.tower === c.tower && angDiff(v.bearing, c.bearing) <= 45).sort((a, b) => Math.abs(a.floor - c.floor) - Math.abs(b.floor - c.floor));
  return L[0] || null;
}
function unitId(c) { const s = ['n', 'e', 's', 'w'][Math.round((((c.bearing % 360) + 360) % 360) / 90) % 4]; return `${c.tower}-${c.floor}-${s}`; }
function label(c) { return t('ck_label', { tower: c.tower, floor: c.floor, dir: dirWord(c.bearing) }); }

/* ---------------------------------------------------------------- the screens */
function home(c) {
  const v = viewOf(c);
  const hero = v ? A(v.big) : A('aerial-1600.webp');
  const tile = (k, lab, img, big) => `<button type="button" class="nlck-tile" data-open="${k}">${img ? `<img src="${esc(img)}" alt="" loading="lazy">` : ''}${big ? `<span class="big">${big}</span>` : ''}<span class="lab">${lab}</span></button>`;
  const firstFac = A('tour/' + FACS[0][0] + '-card.jpg');
  // HAD-712 (12.11): the names are drawn on the view screen (the tile "the view"), not on this small hero, where they covered the title
  return `<div class="nlck-hero"><img src="${esc(hero)}" alt="${esc(t('ck_alt_hero', { label: label(c) }))}">
      <div class="nlck-top"><button type="button" class="nlck-back" data-open="">${esc(t('ck_back'))}</button><span class="nlck-cap">${esc(t('sim'))}${v && v.floor !== c.floor ? t('ck_cap_view_from', { floor: v.floor }) : ''}</span></div>
      <div class="nlck-ht"><h2 class="nlck-title" tabindex="-1">${t('apt_title', { tower: esc(c.tower), floor: esc(c.floor) })}</h2><p>${t('faces_line', { dir: esc(dirWord(c.bearing)), sector: esc(sectorOf(c.bearing)) })}</p>
      <div class="nlck-chips"><span>${t('ck_eye_street', { m: bdi(nf(eyeH(c.floor), 0)) })}</span></div></div></div>
    <p class="nlck-ask">${esc(t('ck_ask'))}</p>
    <div class="nlck-grid">
      ${tile('view', t('ck_tile_view'), v ? A(v.img) : '')}
      ${tile('inside', t('ck_tile_inside'), insideOf(c) ? A(insideOf(c).card) : A('tour/living-c30w-day-card.jpg'))}
      ${tile('other', t('ck_tile_other'), A('aerial-tall-800.webp'))}
      ${tile('plan', t('ck_tile_plan'), D.plan ? A(D.plan) : '')}
      ${tile('fac', t('ck_tile_fac'), firstFac)}
      ${tile('price', t('ck_tile_price'), '', `${bdi(t('ck_price_range', { lo: num(Math.min(...D.deals.map((d) => d.price)) / 1e6, 2), hi: num(Math.max(...D.deals.map((d) => d.price)) / 1e6, 2) }))}<small>${esc(t('ck_tile_price_sub'))}</small>`)}
      ${tile('area', t('ck_tile_area'), A('aerial-800.webp'))}
      ${film() ? tile('film', t('ck_tile_film'), film().poster || A('aerial-tall-800.webp')) : ''}
      ${tile('save', t('ck_tile_save'), '', `${bdi(String(cmpList().length))}<small>${esc(t('ck_tile_saved'))}</small>`)}
    </div>`;
}
function vdAttr(v) { return ` data-vdimg="${esc(v.tower)}|${esc(v.floor)}|${esc(v.bearing)}"`; } // the picture's own tower, floor, bearing
function vdToggle() { // "Picture" / "View with details" (never "the names"): two states, on by default
  return `<div class="nlck-vdt" role="group" aria-label="${esc(t('vd_aria'))}"><button type="button" data-vdt="0" aria-pressed="${!vdOn}">${esc(t('vd_pic'))}</button><button type="button" data-vdt="1" aria-pressed="${vdOn}">${esc(t('vd_details'))}</button></div>`;
}
function subTop(title) { return `<div class="nlck-subtop"><button type="button" class="nlck-back" data-open="">${esc(t('ck_back_apt'))}</button><span>${esc(title)}</span></div>`; }
function scrView(c) {
  const v = sub.view || viewOf(c);
  if (!v) return subTop(t('ck_tile_view')) + `<p class="nlck-pad">${esc(t('ck_view_none'))}</p>`;
  const fl = floorsOf(c), sd = sidesOf(c);
  return `${subTop(label(c))}<div class="nlck-pan" data-pan><div class="nlck-vdh"><img src="${esc(A(v.big))}" alt="${esc(t('ck_alt_view', { floor: v.floor, dir: dirWord(v.bearing) }))}"${vdAttr(v)}></div></div>
    <span class="nlck-cap" style="top:112px;bottom:auto">${t('ck_cap_view', { floor: v.floor, dir: esc(dirWord(v.bearing)) })}</span>${vdToggle()}
    <div class="nlck-under"><div class="nlck-hint">${esc(t('ck_view_drag'))}</div><p class="nlck-vdnote" data-vdn${vdOn ? '' : ' hidden'}>${esc(t('vd_note'))}</p>
      <button type="button" class="nlck-3d" data-act="3d">${esc(t('vd_3d'))}</button><p class="nlck-vdnote">${esc(t('vd_3d_note'))}</p>
      ${fl.length > 1 ? `<div class="nlck-row-t">${esc(t('ck_row_floors'))}</div><div class="nlck-strip">${fl.map((x) => `<button type="button" data-v="${esc(x.img)}" data-vk="floor" aria-pressed="${x === v}"><img src="${esc(A(x.img))}" alt=""><b>${t('floor_n', { floor: bdi(x.floor) })}</b></button>`).join('')}</div>` : ''}
      ${sd.length > 1 ? `<div class="nlck-row-t">${esc(t('ck_row_sides'))}</div><div class="nlck-strip">${sd.map((x) => `<button type="button" data-v="${esc(x.img)}" data-vk="side" aria-pressed="${x === v}"><img src="${esc(A(x.img))}" alt=""><b>${esc(dirWord(x.bearing))}</b></button>`).join('')}</div>` : ''}
    </div>`;
}
/* room to room (HAD-712, Ben: "there is a door, you want to pass from room to room"): the living room's doors carry a button each;
   the bedroom and the balcony are the C30 example apartment's own pictures, and say so */
const ROOMS = { bed: ['tour/bedroom-c30nw-day-2k.webp', 'ck_room_bed'], balcony: ['tour/balcony-c30w-sunset-2k.webp', 'ck_room_balcony'] }; // [picture, word key]
const DOORS = [{ lon: 69, lat: -3, to: 'bed', label: 'ck_door_bed_go' }, { lon: 197, lat: -6, to: 'balcony', label: 'ck_door_balcony_go' }]; // the label carries the language's forward arrow
function roomsRow(room) { return `<div class="nlck-rooms" role="group" aria-label="${esc(t('ck_aria_rooms'))}">${[['living', 'ck_room_living'], ['bed', ROOMS.bed[1]], ['balcony', ROOMS.balcony[1]]].map(([k, l]) => `<button type="button" data-room="${k}" aria-pressed="${k === room}">${esc(t(l))}</button>`).join('')}</div>`; }
function scrInside(c) { // this apartment's living room with its own window view first (HAD-710); the finishes of the C30 example after it
  if (sub.room && ROOMS[sub.room]) { const R = ROOMS[sub.room];
    return `${subTop(t('ck_tile_inside'))}<div class="nlck-360" data-360="${esc(A(R[0]))}" role="img" aria-label="${esc(t('ck_aria_room_tour', { room: t(R[1]) }))}"></div>
    <span class="nlck-cap" style="top:64px;bottom:auto">${t('ck_cap_room', { room: esc(t(R[1])) })}</span>${roomsRow(sub.room)}`; }
  const io = insideOf(c), own = !!io && sub.pano === 0, P = PANOS[io ? Math.max(1, sub.pano) : sub.pano];
  const url = own ? A(io.img) : A('tour/' + P[0] + '-2k.webp');
  const chips = io ? [[t('ck_pano_this'), 0]].concat(PANOS.slice(1).map((p, i) => [t(p[1]), i + 1])) : PANOS.map((p, i) => [t(p[1]), i]);
  const cap = own ? t('ck_cap_own', { floor: io.floor, near: io.floor !== c.floor ? t('ck_cap_own_near', { floor: c.floor }) : '', dir: dirWord(io.bearing) }) : `${io ? t('ck_cap_finish', { finish: t(P[1]) }) : ''}${t('ck_cap_example')}`;
  return `${subTop(t('ck_tile_inside'))}<div class="nlck-360" data-360="${esc(url)}" data-doors="1" role="img" aria-label="${esc(t(own ? 'ck_aria_own_tour' : 'ck_aria_example_tour'))}"></div>
    <span class="nlck-cap" style="top:64px;bottom:auto">${t('ck_cap_drag', { cap })}</span>
    <div class="nlck-float">${chips.map(([lab, i]) => `<button type="button" data-pano="${i}" aria-pressed="${i === (io ? (own ? 0 : Math.max(1, sub.pano)) : sub.pano)}">${esc(lab)}</button>`).join('')}</div>${roomsRow('living')}`;
}
function scrFac() {
  return `${subTop(t('ck_tile_fac'))}<div class="nlck-360" data-360="${esc(A('tour/' + FACS[sub.fac][0] + '-2k.webp'))}" role="img" aria-label="${esc(t(FACS[sub.fac][1]))}, 360"></div>
    <span class="nlck-cap" style="top:64px;bottom:auto">${t('ck_cap_fac', { facility: esc(t(FACS[sub.fac][1])) })}</span>
    <div class="nlck-float">${FACS.map((f, i) => `<button type="button" data-fac="${i}" aria-pressed="${i === sub.fac}">${esc(t(f[1]))}</button>`).join('')}</div>`;
}
function scrPlan() {
  return `${subTop(t('ck_tile_plan'))}<div class="nlck-white"><div class="nlck-zoom" data-zoom><img src="${esc(A(D.plan))}" alt="${esc(t('ck_alt_plan'))}"></div>
    <p class="nlck-note">${esc(t('ck_plan_note'))}</p>
    <p class="nlck-note">${esc(t('ck_plan_note2'))}</p></div>`;
}
function scrPrice() {
  const deals = D.deals.map((d) => `<div class="r"><span>${t('ck_deal_row', { floor: bdi(d.floor), apt: esc(dw(d.apt)), date: bdi(d.date) })}</span><b>${t('ck_deal_price', { m: bdi(num(d.price / 1e6, 2)) })}</b></div>`).join('');
  const tax = taxOf(calc.price, calc.extra ? D.tax.additional : D.tax.only);
  const arn = (calc.size > 140 ? D.arnona.gt140 : D.arnona.le140) * calc.size;
  const pm = monthly(calc.price * calc.share / 100, calc.rate, calc.years);
  const src = D.deals[0];
  const feeClause = D.fee ? t('ck_price_note_fee', { url: esc(D.fee.url), feeSrc: esc(dw(D.fee.src)), feeNote: esc(dw(D.fee.note)) }) : ''; // dw: cockpit.json's Hebrew labels in the page language
  return `${subTop(t('ck_tile_price'))}<div class="nlck-white" data-calc>
    <div class="nlck-box"><b>${esc(t('ck_deals_title'))}</b>${deals}<small>${esc(t('source_prefix'))} <a href="${esc(src.url)}" target="_blank" rel="noopener">${esc(dw(src.src))}</a> · ${esc(t('ck_deals_tower_unknown'))}</small></div>
    <div class="nlck-box nlck-calc">
      <label>${esc(t('ck_calc_price'))}<input type="number" inputmode="numeric" step="10000" name="price" value="${calc.price}"></label>
      <label>${esc(t('tax_additional_home'))}<input type="checkbox" name="extra" ${calc.extra ? 'checked' : ''}></label>
      <label>${esc(t('ck_calc_share'))}<input type="number" inputmode="numeric" min="0" max="75" step="5" name="share" value="${calc.share}"></label>
      <label>${esc(t('ck_calc_years'))}<input type="number" inputmode="numeric" min="4" max="30" name="years" value="${calc.years}"></label>
      <label>${esc(t('ck_calc_rate'))}<input type="number" inputmode="decimal" step="0.05" name="rate" value="${calc.rate}"></label>
      <label>${esc(t('ck_calc_size'))}<input type="number" inputmode="numeric" name="size" value="${calc.size}"></label>
      ${D.fee ? `<label>${esc(t('ck_calc_fee'))}<input type="number" inputmode="numeric" step="100" name="fee" value="${calc.fee}"></label>` : ''}
    </div>
    <div class="nlck-box"><div class="r"><span>${esc(t('purchase_tax'))}</span><b>${ils(tax)}</b></div><div class="r tot"><span>${esc(t('ck_price_tax_total'))}</span><b>${ils(calc.price + tax)}</b></div>
      <div class="r"><span>${esc(t('ck_mortgage_month'))}</span><b>${ils(Math.round(pm))}</b></div><div class="r"><span>${esc(t('ck_arnona_month'))}</span><b>${ils(Math.round(arn / 12))}</b></div>
      ${D.fee ? `<div class="r"><span>${esc(t('ck_fee_month'))}</span><b>${ils(calc.fee)}</b></div>` : ''}<div class="r tot"><span>${esc(t('ck_month_total'))}</span><b>${ils(Math.round(pm + arn / 12 + (D.fee ? calc.fee : 0)))}</b></div></div>
    <p class="nlck-note">${t('ck_price_note', { taxAsof: esc(dw(D.tax.asof)), arnonaAsof: esc(dw(D.arnona.asof)), zone: D.arnona.zone, mortgageSrc: esc(dw(D.mortgage.src)), mortgageLabel: esc(dw(D.mortgage.label)), feeClause })}</p></div>`;
}
function scrArea() {
  if (!PL) return `${subTop(t('ck_tile_area'))}<p class="nlck-pad">${esc(t('loading'))}</p>`;
  const out = [];
  for (const g of GROUPS) { // HAD-712: on the en/fr page a place shows only with a name in that language or English (placeName), never in Hebrew
    const near = PL.places.filter((p) => p.g === g && !p.generic && placeName(p)).sort((a, b) => a.dist - b.dist).slice(0, 4);
    if (!near.length) continue;
    out.push(`<div class="nlck-grp">${esc(t('ck_grp_' + g))}</div>` + near.map((p) => `<a class="nlck-place" href="https://www.google.com/maps/dir/?api=1&amp;destination=${p.lat},${p.lng}&amp;travelmode=walking" target="_blank" rel="noopener"><span>${esc(placeName(p))} <small>· ${esc(t('ck_kind_' + p.k))}</small></span><b>${t('ck_dist_m', { dist: bdi(num(p.dist)) })}${p.walk ? t('ck_walk_min', { min: bdi(p.walk) }) : ''}</b></a>`).join(''));
  }
  return `${subTop(t('ck_tile_area'))}<div class="nlck-white"><p class="nlck-note">${esc(t('ck_area_note'))}</p>${out.join('')}</div>`;
}
function film() { // the page's own Kikar film (ProjectFilm): the tall cut on phones, the wide one on screens
  const src = (v) => { const s = v.querySelector('source'); return (s ? s.getAttribute('src') : v.getAttribute('src')) || ''; };
  const vs = [...document.querySelectorAll('video')].filter((v) => /kikar|hamedina/i.test(src(v)));
  if (!vs.length) return null;
  const v = vs.find((x) => x.classList.contains(innerWidth < 700 ? 'nlws-film__v--tall' : 'nlws-film__v--wide')) || vs[0];
  return { src: src(v), poster: v.getAttribute('data-nlposter') || v.getAttribute('poster') || '' };
}
function scrFilm() { const f = film() || {}; return `${subTop(t('ck_tile_film'))}<video class="nlck-video" src="${esc(f.src)}" poster="${esc(f.poster)}" controls playsinline preload="metadata" autoplay></video>`; }
function cmpList() { return store.get('nlck-cmp', []); }
function isSaved() { if (!cur) return false; const b = Math.round(cur.bearing); return cmpList().some((x) => x.tower === cur.tower && x.floor === cur.floor && x.bearing === b); }
function scrSave(c) {
  const L = cmpList();
  const me = { tower: c.tower, floor: c.floor, bearing: Math.round(c.bearing) };
  const has = L.some((x) => x.tower === me.tower && x.floor === me.floor && x.bearing === me.bearing);
  const card = (x) => { const v = viewOf({ ...x, heightM: eyeH(x.floor) }); return `<div class="nlck-cmp-c">${v ? `<img src="${esc(A(v.img))}" alt="">` : ''}<b>${t('apt_title', { tower: esc(x.tower), floor: esc(x.floor) })}</b><span>${t('faces_line', { dir: esc(dirWord(x.bearing)), sector: esc(sectorOf(x.bearing)) })}</span><span>${t('eye_height', { m: bdi(nf(eyeH(x.floor), 0)) })}</span></div>`; };
  return `${subTop(t('ck_tile_save'))}<div class="nlck-white">
    <div class="nlck-row"><button type="button" class="nlck-btn" data-act="save">${esc(t(has ? 'ck_saved' : 'ck_save_this'))}</button></div>
    ${L.length ? `<div class="nlck-cmp">${[me, ...L.filter((x) => !(x.tower === me.tower && x.floor === me.floor && x.bearing === me.bearing))].slice(0, 3).map(card).join('')}</div>` : `<p class="nlck-note">${esc(t('ck_cmp_empty'))}</p>`}
    <div class="nlck-box"><b>${esc(t('ck_share_title'))}</b>
      <label class="ck"><input type="checkbox" checked disabled>${esc(t('ck_share_unit'))}</label>
      <label class="ck"><input type="checkbox" name="sh-view" checked>${esc(t('ck_share_view'))}</label>
      <label class="ck"><input type="checkbox" name="sh-price">${esc(t('ck_share_price'))}</label>
      <small>${esc(t('ck_share_privacy'))}</small></div>
    <div class="nlck-row"><button type="button" class="nlck-btn nlck-btn--solid" data-act="share">${esc(t('ck_share_btn'))}</button></div></div>`;
}

/* ---------------------------------------------------------------- the 360 viewer (three.js from the page's import map) */
let PV = null;
async function pano(host, url, doors) {
  if (PV) { PV.destroy(); PV = null; }
  let THREE;
  try { THREE = await import('three'); } catch (e) { host.innerHTML = `<div class="nlck-pan" data-pan><img src="${esc(url)}" alt=""></div>`; return; }
  const W = () => host.clientWidth, H = () => host.clientHeight;
  const r = new THREE.WebGLRenderer({ antialias: true }); r.setPixelRatio(Math.min(2, devicePixelRatio || 1)); r.setSize(W(), H()); host.appendChild(r.domElement);
  const scene = new THREE.Scene(), cam = new THREE.PerspectiveCamera(W() < 600 ? 80 : 70, W() / H(), 0.1, 100);
  const tex = await new THREE.TextureLoader().loadAsync(url); tex.colorSpace = THREE.SRGBColorSpace;
  const geo = new THREE.SphereGeometry(10, 64, 32); geo.scale(-1, 1, 1); scene.add(new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ map: tex })));
  let lon = 180, lat = 0, x0 = null, y0 = 0, l0 = 0, a0 = 0, run = true;
  const dir = (lo, la) => { const p = THREE.MathUtils.degToRad(90 - la), t = THREE.MathUtils.degToRad(lo); return new THREE.Vector3(Math.sin(p) * Math.cos(t), Math.cos(p), Math.sin(p) * Math.sin(t)); };
  const hot = (doors || []).map((d) => { const b = document.createElement('button'); b.type = 'button'; b.className = 'nlck-door'; b.dataset.room = d.to; b.textContent = t(d.label); b.hidden = true; host.appendChild(b); return { b, v: dir(d.lon, d.lat).multiplyScalar(9) }; });
  const draw = () => { if (!run) return; cam.lookAt(dir(lon, lat)); cam.updateMatrixWorld(); r.render(scene, cam);
    for (const h of hot) { const q = h.v.clone().project(cam), on = q.z < 1 && Math.abs(q.x) < 0.9 && Math.abs(q.y) < 0.8; h.b.hidden = !on; if (on) { h.b.style.left = ((q.x * 0.5 + 0.5) * 100).toFixed(1) + '%'; h.b.style.top = ((-q.y * 0.5 + 0.5) * 100).toFixed(1) + '%'; } }
    requestAnimationFrame(draw); };
  host.addEventListener('pointerdown', (e) => { if (e.target.closest('button')) return; x0 = e.clientX; y0 = e.clientY; l0 = lon; a0 = lat; host.setPointerCapture(e.pointerId); });
  host.addEventListener('pointermove', (e) => { if (x0 == null) return; lon = l0 - (e.clientX - x0) * 0.16; lat = Math.max(-75, Math.min(75, a0 + (e.clientY - y0) * 0.16)); });
  host.addEventListener('pointerup', () => { x0 = null; });
  const rs = () => { r.setSize(W(), H()); cam.aspect = W() / H(); cam.updateProjectionMatrix(); }; addEventListener('resize', rs);
  draw();
  PV = { destroy() { run = false; removeEventListener('resize', rs); hot.forEach((h) => h.b.remove()); geo.dispose(); tex.dispose(); r.dispose(); r.domElement.remove(); } };
}

/* ---------------------------------------------------------------- the app */
function render() {
  if (!el || !cur || !D) return;
  if (PV) { PV.destroy(); PV = null; }
  const body = $('.nlck-body', el);
  const c = cur;
  const h = { view: () => scrView(c), inside: () => scrInside(c), fac: scrFac, plan: scrPlan, price: scrPrice, area: scrArea, film: scrFilm, save: () => scrSave(c) }[open];
  vds.splice(0).forEach((d) => d.destroy());
  body.innerHTML = h ? h() : home(c);
  body.dataset.screen = el.dataset.screen = open || 'home';
  if (open === 'view') way.set('ck_view'); if (open === 'inside') way.set('ck_inside');
  body.querySelectorAll('img[data-vdimg]').forEach(mountVd);
  try { dispatchEvent(new CustomEvent('nl:cockpit', { detail: { screen: open || 'home' } })); } catch (e) { /* none */ } // HAD-712: the showroom's steps follow
  body.scrollTop = 0;
  const p3 = $('[data-360]', body); if (p3) pano(p3, p3.dataset['360'], p3.dataset.doors ? DOORS : null);
  const pan = $('[data-pan]', body); if (pan) { const im = $('img', pan); const ctr = () => { pan.scrollLeft = (isRtl() ? -1 : 1) * (pan.scrollWidth - pan.clientWidth) / 2; }; /* HAD-712: RTL scrolls with negative values */ if (im) { if (im.complete) ctr(); else im.addEventListener('load', ctr, { once: true }); } }
  if (open === 'area' && !PL) loadPlaces().then(() => { if (open === 'area') render(); });
  paintBar();
}
function mountVd(img) { // HAD-712 (12.11): the names of the places over the rendered window view (world/viewdetails.js, loaded on first use)
  const [tw, fl, br] = img.dataset.vdimg.split('|');
  if (!VD) VD = import(new URL('viewdetails.js' + (C.ver ? '?ver=' + C.ver : ''), import.meta.url).href);
  VD.then((m) => m.viewDetails(img, { data: A('details.json'), lang: lang(), avoid: '.nlck-subtop > *, .nlck-cap, .nlck-vdt' })).then((d) => {
    if (!img.isConnected) { d.destroy(); return; }
    d.set({ tower: tw, floor: +fl, bearing: +br }); d.show(vdOn); vds.push(d);
  }).catch((e) => console.warn('[cockpit] view details', e));
}
function setVd(on) {
  vdOn = !!on; vds.forEach((d) => d.show(vdOn));
  el.querySelectorAll('[data-vdt]').forEach((b) => b.setAttribute('aria-pressed', String((b.dataset.vdt === '1') === vdOn)));
  el.querySelectorAll('[data-vdn]').forEach((p) => { p.hidden = !vdOn; });
  ga('cockpit_view_details', { on: vdOn });
}
function paintWay() { // exactly one pulse: the next step of the apartment screen, with its line above the bar
  if (!el) return;
  el.querySelectorAll('.nlsr-pulse').forEach((x) => x.classList.remove('nlsr-pulse'));
  const wl = $('.nlck-wl', el);
  const d = way.get(), k = el.hidden ? null : WAY.find((x) => !d[x] && !(x === 'ck_basket' && !window.__nlBasket));
  if (!k) { delete el.dataset.way; if (wl) wl.hidden = true; return; }
  const scr = open || 'home', tile = (x) => $(`.nlck-tile[data-open="${x}"]`, el), back = () => $('.nlck-subtop .nlck-back', el);
  let tg = null, lab = '';
  if (k === 'ck_view') { if (scr === 'home') { tg = tile('view'); lab = 'way_view'; } else { tg = back(); lab = 'way_back'; } }
  else if (k === 'ck_inside') { if (scr === 'home') { tg = tile('inside'); lab = 'way_inside'; } else { tg = back(); lab = 'way_back'; } }
  else if (k === 'ck_design') {
    if (scr === 'inside') { tg = sub.room ? $('[data-room="living"]', el) : $('[data-pano][aria-pressed="false"]', el); lab = 'way_design'; }
    else if (scr === 'home') { tg = tile('inside'); lab = 'way_design_home'; } else { tg = back(); lab = 'way_back'; }
  } else if (k === 'ck_basket') { tg = $('[data-act="basket"]', el); lab = 'way_basket'; }
  else { tg = $('.nlck-call', el); lab = 'way_call'; }
  el.dataset.way = k;
  if (tg) tg.classList.add('nlsr-pulse');
  if (wl) { wl.hidden = !tg; $('b', wl).textContent = t(lab); }
}
function paintBar() {
  const bar = el && $('.nlck-bar', el); if (!bar) return;
  const room = avail ? `${location.pathname}${location.search ? location.search + '&' : '?'}room=new${location.hash}` : '#nlsch';
  bar.innerHTML = `<a class="nlck-call" data-act="call" href="${esc(room)}">${ICON.video}${esc(t(avail ? 'ck_call_now' : 'ck_call'))}</a>
    ${C.wa ? `<a class="nlck-ic nlck-ic--wa" href="${esc(C.wa)}" target="_blank" rel="noopener" aria-label="${esc(t('ck_aria_wa'))}" data-act="wa">${ICON.wa}</a>` : ''}
    <button type="button" class="nlck-ic" data-act="save" aria-label="${esc(t('ck_aria_save'))}" aria-pressed="${isSaved()}">${ICON.heart}</button>
    ${window.__nlBasket ? `<button type="button" class="nlck-ic nlck-ic--bk" data-act="basket" aria-label="${esc(t('basket_name'))}">${ICON.bag}</button>` : ''}`; // HAD-712 (12.11): My selection
  paintWay();
}
function toast(msg) { const t = el && $('.nlck-toast', el); if (!t) return; t.textContent = msg; t.hidden = false; clearTimeout(toast.h); toast.h = setTimeout(() => { t.hidden = true; }, 2600); }
function mount() {
  el = document.createElement('div');
  el.className = 'nlck'; el.id = 'nlck'; el.dir = dir(); el.lang = lang(); el.hidden = true;
  el.setAttribute('role', 'dialog'); el.setAttribute('aria-modal', 'true'); el.setAttribute('aria-label', t('ck_aria_dialog'));
  el.innerHTML = '<div class="nlck-body"></div><div class="nlck-wl" role="status" hidden><i aria-hidden="true"></i><b></b></div><div class="nlck-bar"></div><div class="nlck-toast" role="status" aria-live="polite" hidden></div>';
  document.body.appendChild(el);
  el.addEventListener('click', onClick);
  el.addEventListener('change', onInput);
  el.addEventListener('keydown', (e) => { if (e.key === 'Escape') { if (open) { open = null; render(); } else close(); } });
}
function show(c, from, screen) { // screen (HAD-712): open straight on one of the screens, e.g. 'view' or 'inside'
  cur = { tower: c.tower, floor: +c.floor, bearing: +c.bearing, heightM: c.heightM || eyeH(+c.floor) };
  viaJourney = from === 'journey'; open = ['view', 'inside', 'fac', 'plan', 'price', 'area', 'film', 'save'].includes(screen) ? screen : null; sub.view = null; sub.pano = 0; sub.room = null;
  try { history.replaceState(history.state, '', `${location.pathname}${location.search}#dira=${cur.tower}${cur.floor}-${Math.round(cur.bearing)}`); } catch (e) { /* file: */ }
  if (!el) mount();
  load().then(() => {
    el.hidden = false; document.documentElement.style.overflow = 'hidden'; document.body.classList.add('nlck-on');
    render(); askAvail();
    const h = $('.nlck-title', el); if (h) h.focus({ preventScroll: true });
    ga('cockpit_open', { tower: cur.tower, floor: cur.floor, facing: dirWord(cur.bearing, 'he') });
  });
}
function close() {
  if (!el) return; if (PV) { PV.destroy(); PV = null; }
  el.hidden = true; document.documentElement.style.overflow = ''; document.body.classList.remove('nlck-on');
  vds.splice(0).forEach((d) => d.destroy()); paintWay(); // no pulse left behind a closed screen
  try { dispatchEvent(new CustomEvent('nl:cockpit', { detail: { screen: null, closed: true } })); } catch (e) { /* none */ } // HAD-712: the showroom's waymarks move on
  if (viaJourney && window.__nlJourney && window.__nlJourney.open) window.__nlJourney.open(4);
}
function onInput(e) {
  const t = e.target; if (!t.name || !t.closest('[data-calc]')) return;
  if (t.name === 'extra') calc.extra = t.checked; else { const v = parseFloat(t.value); if (isFinite(v)) calc[t.name] = v; }
  render(); const n = $(`[name="${t.name}"]`, el); if (n && t.type !== 'checkbox') n.focus();
}
function onClick(e) {
  const vt = e.target.closest('[data-vdt]'); if (vt) { setVd(vt.dataset.vdt === '1'); return; }
  const o = e.target.closest('[data-open]');
  if (o && o.dataset.open === 'other') { ga('cockpit_tile', { tile: 'other' }); viaJourney = false; close(); if (window.__nlJourney && window.__nlJourney.open) window.__nlJourney.open(2); else { const s = document.getElementById('nlps'); if (s) s.scrollIntoView({ behavior: 'smooth', block: 'center' }); } return; }
  if (o && el.contains(o)) { const k = o.dataset.open; if (!k && !open) return close(); open = k || null; if (k !== 'view') sub.view = null; render(); ga('cockpit_tile', { tile: k || 'home' }); return; }
  const v = e.target.closest('[data-v]'); if (v) { sub.view = rendered().find((x) => x.img === v.dataset.v) || null; if (sub.view && v.dataset.vk === 'side') { cur.bearing = sub.view.bearing; } return render(); }
  const rm = e.target.closest('[data-room]'); if (rm) { sub.room = rm.dataset.room === 'living' ? null : rm.dataset.room; ga('cockpit_room', { room: rm.dataset.room }); return render(); }
  const p = e.target.closest('[data-pano]'); if (p) {
    sub.pano = +p.dataset.pano; way.set('ck_design');
    try { dispatchEvent(new CustomEvent('nl:view', { detail: { mode: 'inside', style: PSTYLE[sub.pano] || 'bare', source: 'cockpit' } })); } catch (x) { /* none */ } // the basket records the finish
    return render();
  }
  const f = e.target.closest('[data-fac]'); if (f) { sub.fac = +f.dataset.fac; return render(); }
  const z = e.target.closest('[data-zoom]'); if (z) { z.classList.toggle('on'); return; }
  const a = e.target.closest('[data-act]'); if (!a) return;
  const act = a.dataset.act;
  if (act === 'save') {
    const me = { tower: cur.tower, floor: cur.floor, bearing: Math.round(cur.bearing) };
    const L = cmpList().filter((x) => !(x.tower === me.tower && x.floor === me.floor && x.bearing === me.bearing)); L.unshift(me); store.set('nlck-cmp', L.slice(0, 4));
    toast(t('ck_toast_saved')); ga('cockpit_save', {}); if (open === 'save' || !open) render(); else paintBar(); return;
  }
  if (act === 'share') {
    const withView = $('[name="sh-view"]', el) && $('[name="sh-view"]', el).checked, withPrice = $('[name="sh-price"]', el) && $('[name="sh-price"]', el).checked;
    const lines = [t('ck_share_line1', { label: label(cur) })];
    if (withView) lines.push(t('ck_share_line2', { sector: sectorOf(cur.bearing), m: nf(eyeH(cur.floor), 0) }));
    if (withPrice) { const tax = taxOf(calc.price, calc.extra ? D.tax.additional : D.tax.only); lines.push(t('ck_share_line3', { price: num(calc.price), tax: num(tax) })); }
    const q = new URLSearchParams(location.search); q.delete('room'); const qs = q.toString(); // keeps ?kikar=next while the cockpit is gated
    const url = `${location.origin}${location.pathname}${qs ? '?' + qs : ''}#dira=${cur.tower}${cur.floor}-${Math.round(cur.bearing)}`;
    ga('cockpit_share', { view: !!withView, price: !!withPrice });
    if (navigator.share) { navigator.share({ title: t('project_title'), text: lines.join('\n'), url }).catch(() => {}); return; }
    (navigator.clipboard ? navigator.clipboard.writeText(lines.join('\n') + '\n' + url) : Promise.reject()).then(() => toast(t('ck_toast_copied')), () => toast(url));
    return;
  }
  if (act === 'basket') { way.set('ck_basket'); paintWay(); ga('cockpit_basket', {}); if (window.__nlBasket) window.__nlBasket.open(a); return; }
  if (act === '3d') { ga('cockpit_3d', { tower: cur.tower, floor: cur.floor }); return world3d(sub.view || viewOf(cur) || cur); }
  if (act === 'call') { way.set('ck_call'); paintWay(); ga('cockpit_call', { now: !!avail }); if (!avail) { e.preventDefault(); close(); const s = document.getElementById('nlsch'); if (s) s.scrollIntoView({ behavior: 'smooth', block: 'start' }); } return; }
  if (act === 'wa') ga('cockpit_wa', {});
}

window.__nlCockpit = { open: (d, from, screen) => show(d, from, screen) };
addEventListener('nl:facing', (e) => { const d = e.detail || {}; if (from3d && d.source === 'api') return; if (!d.quiet && d.tower && d.floor && d.bearing != null) show(d, d.source); }); // HAD-712: the 3D set by our tap reports back as 'api'
/* HAD-712 (12.11.2026): "the live 3D of this floor": the page's earlier 3D stage (world.js) loads only on this tap. On the Hebrew page
   the stage is hidden (showroom.css) until body.nlsr-3d; the world is set to the picture's tower, floor and facing through its
   handle (setMode, pickTower, setFloor, setFacing, setView: world.js's documented API) */
function world3d(v) {
  from3d = true; viaJourney = false; close();
  document.body.classList.add('nlsr-3d');
  const root = document.getElementById('nlps'), host = document.getElementById('nlps-stage'), box = document.getElementById('nlps-t') || document.querySelector('.nlps-stagebox') || root; // the heading keeps the site header's margin
  if (!root || !host) return;
  requestAnimationFrame(() => box.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'start' }));
  const go = (w) => { if (!w) return; try { w.setMode('tower'); w.pickTower(v.tower); w.setFloor(+v.floor); w.setFacing(+v.bearing); w.setView('window'); } catch (e) { console.warn('[cockpit] 3d', e); }
    Promise.resolve(w.ready).then(() => setTimeout(() => box.scrollIntoView({ block: 'start' }), 400)).catch(() => {}); }; // the stage's top in sight once the world has laid out
  if (window.__nlpsWorld) return go(window.__nlpsWorld);
  if (typeof window.__nlpsMount === 'function') return Promise.resolve(window.__nlpsMount()).then(go); // inc/project-stage.php (HAD-712)
  let c = {}; try { c = JSON.parse(root.dataset.cfg || '{}'); } catch (e) { c = {}; }
  if (!c.world) return;
  import(c.world).then((m) => { // the page's own mount, the same options (inc/project-stage.php nadlan_ps_world_script)
    if (window.__nlpsWorld) return go(window.__nlpsWorld);
    const w = m.mountWorld(host, { dataUrl: c.data, placesUrl: c.places || null, lang: c.lang, name: c.name, wa: c.wa || null, poster: c.poster,
      intent: 'visible', mode: c.mode, season: c.season, hour: c.hour, pond: c.pond !== false, examples: c.examples || null, colors: (c.next && c.next.colors) || null });
    window.__nlpsWorld = w;
    const own = host.querySelector('.nlps-ssr-pic'); if (own) setTimeout(() => own.remove(), 1500);
    go(w);
  }).catch((e) => console.warn('[cockpit] 3d', e));
} // quiet (HAD-712): the showroom reports a choice without opening this screen
function reopen() { // a link that reopens a choice: #dira=A30-262
  const m = /^#dira=([ABC])(\d{1,2})-(\d{1,3})$/.exec(location.hash || '');
  if (m && !(cur && el && !el.hidden && cur.tower === m[1] && cur.floor === +m[2] && Math.round(cur.bearing) === +m[3])) show({ tower: m[1], floor: +m[2], bearing: +m[3] }, 'link');
}
reopen();
addEventListener('hashchange', reopen);
load().catch(() => {});
