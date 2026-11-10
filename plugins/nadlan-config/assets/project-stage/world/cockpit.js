/*
 * The apartment cockpit (HAD-699, 10.11.2026; design: https://claude.ai/artifact/FzvFDybiyBoi8bspoPV9Zp).
 * When the visitor chooses an apartment in the world (tower → floor → direction: the world fires nl:facing), one panel opens
 * with everything about that apartment, in stacked sections that open and close: the view, price and cost, the plan, inside,
 * around, decide. The video call is the site's own shared room (inc/together.php: /room/available, ?room=new), else the
 * booking band (#nlsch). The choice lives in the address (#dira=C30-266), so a link reopens it.
 *
 *   window.__nlCockpitCfg = { data, places, base, wa, avail, lang }   (printed by inc/project-stage.php under the gate)
 *   import('.../world/cockpit.js')
 *
 * Honesty (the site's language law): every number comes from cockpit.json with its source; examples say "דוגמה"; pictures say
 * "הדמיה להמחשה"; an unknown is left out, never announced. No new WhatsApp wording: the WhatsApp button is the page's own link
 * (the site's interceptor adds the chosen floor from window.__nlpsPick).
 */
const C = window.__nlCockpitCfg || {};
const $ = (s, r = document) => r.querySelector(s);
const esc = (s) => String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const num = (n, d = 0) => (n == null || !isFinite(n) ? '' : Number(n).toLocaleString('he-IL', { minimumFractionDigits: d, maximumFractionDigits: d }));
const bdi = (s) => `<bdi>${esc(s)}</bdi>`;
const ils = (n, d = 0) => `${bdi(num(n, d))} ₪`;
const ga = (n, p) => { try { if (window.nadlanGA) window.nadlanGA(n, Object.assign({ project: 'hamedina' }, p || {})); } catch (e) { /* none */ } };
const store = { get(k, d) { try { const v = localStorage.getItem(k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } }, set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* private mode */ } } };
const SEASONS = { 12: 'בחורף', 3: 'באביב', 6: 'בקיץ' };
const ICON = {
  x: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>',
  chev: '<svg viewBox="0 0 24 24" aria-hidden="true" style="color:#2f6f86"><path d="M6 9l6 6 6-6"/></svg>',
  video: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="6" width="13" height="12" rx="2"/><path d="M16 10l5-3v10l-5-3"/></svg>',
  wa: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20l1.3-3.9A8 8 0 1 1 8 19z"/><path d="M9 9.5c.5 2 2.5 4 4.5 4.5l1.2-1.2 2 1-.5 1.7c-3.5.4-8-4-7.6-7.6L10.3 7l1 2z"/></svg>',
  save: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 4h12v16l-6-4-6 4z"/></svg>',
};
const GROUPS = { education: 'חינוך', food: 'אוכל וקפה', essentials: 'קניות ושירותים', transport: 'תחבורה', outdoors: 'גנים וספורט', health: 'בריאות', community: 'קהילה ותרבות' };
const KINDS = { school: 'בית ספר', kindergarten: 'גן ילדים', college: 'מכללה', daycare: 'מעון', park: 'גן', dog_park: 'גינת כלבים', gym: 'חדר כושר', bus_stop: 'תחנת אוטובוס', restaurant: 'מסעדה', cafe: 'בית קפה', bakery: 'מאפייה', shopping: 'חנות', supermarket: 'סופרמרקט', bank: 'בנק', pharmacy: 'בית מרקחת', clinic: 'מרפאה', hospital: 'בית חולים', health: 'בריאות', community: 'מרכז קהילתי', worship: 'בית כנסת', culture: 'תרבות', light_rail: 'רכבת קלה', rail: 'רכבת', playground: 'גן שעשועים', library: 'ספרייה', post: 'דואר', sport: 'ספורט', pitch: 'מגרש ספורט', fuel: 'תחנת דלק', marketplace: 'שוק' };
const SECS = [['view', 'הנוף'], ['price', 'מחיר ועלות'], ['plan', 'תוכנית'], ['inside', 'בפנים'], ['around', 'מה מסביב'], ['decide', 'החלטה']];

let D = null, PL = null, el = null, cur = null, avail = null;
const open = { view: true };
const calc = { price: null, extra: false, size: null, share: null, years: null, rate: null, fee: null };
let tod = 'day', viewPick = null;

const world = () => window.__nlpsWorld || null;
const asset = (p) => (C.base || '') + p + (C.ver ? (p.includes('?') ? '&' : '?') + 'ver=' + C.ver : '');
const angDiff = (a, b) => { const d = Math.abs(((a - b) % 360 + 540) % 360 - 180); return d; };

function load() {
  if (D) return Promise.resolve(D);
  return fetch(C.data, { credentials: 'omit' }).then((r) => r.json()).then((j) => {
    D = j;
    calc.price = D.defaults.price; calc.size = D.defaults.size; calc.share = D.defaults.share; calc.years = D.defaults.years; calc.rate = D.mortgage.rate;
    calc.fee = D.fee ? D.defaults.fee : 0;
    return D;
  });
}
function loadPlaces() {
  if (PL || !C.places) return Promise.resolve(PL);
  return fetch(C.places, { credentials: 'omit' }).then((r) => r.json()).then((j) => (PL = j)).catch(() => null);
}
function askAvail() {
  if (avail !== null || !C.avail) return;
  avail = false;
  fetch(C.avail, { credentials: 'omit', cache: 'no-store' }).then((r) => r.json()).then((j) => { avail = !!(j && j.now === true); paintBar(); }).catch(() => {});
}

/* ---------------------------------------------------------------- the money */
function taxOf(p, brackets) {
  let t = 0, lo = 0;
  for (const [hi, r] of brackets) { const top = hi == null ? Infinity : hi; if (p > lo) t += (Math.min(p, top) - lo) * r; lo = top; }
  return Math.round(t);
}
function monthly(P, ratePct, years) {
  const r = ratePct / 100 / 12, n = years * 12;
  if (!(P > 0) || !(n > 0)) return 0;
  return r ? (P * r) / (1 - Math.pow(1 + r, -n)) : P / n;
}

/* ---------------------------------------------------------------- the sections */
function viewsFor(c) {
  const list = (D.views || []).filter((v) => v.tower === c.tower && v.tod === 'day' && v.bearing != null && angDiff(v.bearing, c.bearing) <= 30);
  list.sort((a, b) => Math.abs(a.floor - c.floor) - Math.abs(b.floor - c.floor));
  return list;
}
function secView(c) {
  const vs = viewsFor(c);
  const sun = [12, 3, 6].map((s) => { let h = null; try { const w = world(); h = w && w.sunHours ? w.sunHours(c.tower, c.floor, c.bearing, s) : null; } catch (e) { h = null; } return h == null ? '' : `<div><small>שמש ישירה בחלון ${SEASONS[s]}</small><b>כ-${bdi(num(h, h % 1 ? 1 : 0))} שעות</b></div>`; }).join('');
  let pic = '';
  if (vs.length) {
    const pick = viewPick && vs.find((v) => v.floor === viewPick) ? vs.find((v) => v.floor === viewPick) : vs[0];
    const exact = pick.floor === c.floor;
    const alt = (D.views || []).filter((v) => v.tower === pick.tower && v.floor === pick.floor && angDiff(v.bearing, pick.bearing) < 1 && v.tod !== 'day');
    const shown = tod !== 'day' ? alt.find((v) => v.tod === tod) || pick : pick;
    const tods = alt.length ? `<div class="tods">${[['day', 'יום'], ...alt.map((v) => [v.tod, v.tod === 'sunset' ? 'שקיעה' : 'ערב'])].map(([k, l]) => `<button type="button" data-act="tod" data-v="${k}" aria-pressed="${(tod === k || (k === 'day' && !alt.find((v) => v.tod === tod))) ? 'true' : 'false'}">${l}</button>`).join('')}</div>` : '';
    const floors = vs.length > 1 ? `<div class="nlck-note">אותו כיוון בקומות אחרות. המגדל מסתובב, והנוף מסתובב איתו:</div><div class="nlck-floors">${vs.slice(0, 3).sort((a, b) => a.floor - b.floor).map((v) => `<button type="button" data-act="vfloor" data-v="${v.floor}" aria-pressed="${v === pick ? 'true' : 'false'}"><img src="${esc(asset(v.img))}" alt="" loading="lazy">קומה ${bdi(v.floor)}</button>`).join('')}</div>` : '';
    pic = `<div class="nlck-pic"><img src="${esc(asset(shown.img))}" alt="${esc(`הנוף מקומה ${pick.floor} במגדל ${pick.tower}`)}" loading="lazy"><span class="cap">הדמיה להמחשה${exact ? '' : ` · מקומה ${pick.floor}, הקרובה שצוירה`}</span>${tods}</div>${floors}`;
  }
  return `${pic}<div class="nlck-facts">${sun}</div>
    <p class="nlck-note">גובה העיניים כ-${bdi(num(c.heightM, 1))} מ׳ · החלון פונה ל-${bdi(Math.round(c.bearing) + '°')} (${esc(c.facing || '')}). השעות מחושבות מול הבניינים של העיר, ב-21 לחודש.</p>
    <div class="nlck-row"><button type="button" class="nlck-btn" data-act="window">לראות את הנוף מהחלון בעולם</button></div>`;
}
function secPrice() {
  const deals = D.deals.map((d) => `<tr><td><b>${bdi(d.floor)}</b></td><td>${esc(d.apt)}</td><td>${bdi(num(d.price / 1e6, 2))} מ׳ ₪</td><td>${bdi(d.date)}</td></tr>`).join('');
  const src = D.deals[0];
  const tax = taxOf(calc.price, calc.extra ? D.tax.additional : D.tax.only);
  const arn = (calc.size > 140 ? D.arnona.gt140 : D.arnona.le140) * calc.size;
  const loan = calc.price * calc.share / 100;
  const pm = monthly(loan, calc.rate, calc.years);
  return `<table><caption>עסקאות שפורסמו במגדלים</caption><thead><tr><th>קומה</th><th>הדירה</th><th>מחיר</th><th>מועד</th></tr></thead><tbody>${deals}</tbody></table>
    <p class="nlck-note">מקור: <a href="${esc(src.url)}" target="_blank" rel="noopener">${esc(src.src)}</a>. המגדל של כל עסקה לא פורסם.</p>
    <div class="nlck-facts"><div><small>למ״ר בעסקאות</small><b>כ-${ils(Math.round(D.deals.reduce((s, d) => s + d.price, 0) / D.deals.length / 140 / 1000) * 1000)}</b></div><div><small>ממוצע המגדלים</small><b>${esc(D.sums.towers_psqm)}</b></div><div><small>סביב הכיכר</small><b>${esc(D.sums.area_psqm)}</b></div></div>
    <div class="nlck-calc" data-calc>
      <label>מחיר הדירה לדוגמה (₪)<input type="number" inputmode="numeric" min="0" step="10000" name="price" value="${calc.price}"></label>
      <label><span>דירה נוספת</span><input type="checkbox" name="extra" ${calc.extra ? 'checked' : ''}></label>
      <label>שטח לארנונה (מ״ר)<input type="number" inputmode="numeric" min="20" step="1" name="size" value="${calc.size}"></label>
      <label>מימון (%)<input type="number" inputmode="numeric" min="0" max="75" step="5" name="share" value="${calc.share}"></label>
      <label>שנים<input type="number" inputmode="numeric" min="4" max="30" step="1" name="years" value="${calc.years}"></label>
      <label>ריבית (%)<input type="number" inputmode="decimal" min="0" max="12" step="0.05" name="rate" value="${calc.rate}"></label>
      ${D.fee ? `<label>דמי תחזוקה (₪ בחודש)<input type="number" inputmode="numeric" min="0" step="100" name="fee" value="${calc.fee}"></label>` : ''}
      <div class="nlck-out">
        <div><span>מס רכישה</span><b>${ils(tax)}</b></div>
        <div class="tot"><span>המחיר ומס הרכישה יחד</span><b>${ils(calc.price + tax)}</b></div>
        <div><span>החזר משכנתא בחודש, לדוגמה</span><b>${ils(Math.round(pm))}</b></div>
        <div><span>ארנונה בחודש</span><b>${ils(Math.round(arn / 12))}</b></div>
        ${D.fee ? `<div><span>דמי תחזוקה בחודש</span><b>${ils(calc.fee)}</b></div>` : ''}
        <div class="tot"><span>בחודש, הכול יחד</span><b>${ils(Math.round(pm + arn / 12 + (D.fee ? calc.fee : 0)))}</b></div>
      </div>
    </div>
    ${D.fee ? `<p class="nlck-note">דמי התחזוקה: לפי <a href="${esc(D.fee.url)}" target="_blank" rel="noopener">${esc(D.fee.src)}</a>, ${esc(D.fee.note)}. ברירת המחדל היא האמצע.</p>` : ''}
    <p class="nlck-note">דוגמה בלבד. מחיר ברירת המחדל הוא העסקה הנמוכה שפורסמה. מס רכישה: ${esc(D.tax.asof)}. ארנונה: ${esc(D.arnona.asof)}, אזור ${D.arnona.zone}, סוג ${esc(D.arnona.type)}${calc.size > 140 ? '; מעל 140 מ״ר כל השטח בתעריף הגבוה' : ''}. ריבית: ממוצע ${esc(D.mortgage.src)}, ${esc(D.mortgage.label)}, ${esc(D.mortgage.month.split('-').reverse().join('.'))}. שכר טרחה ודמי תיווך לא כלולים.</p>`;
}
function secPlan(c) {
  const img = D.plan ? `<div class="nlck-pic" style="background:#fff;border:1px solid #e3e7ea"><img src="${esc(asset(D.plan))}" alt="תוכנית קומה טיפוסית: ארבע דירות פינתיות סביב גרעין עגול" loading="lazy" style="aspect-ratio:1/1;object-fit:contain"><span class="cap">תוכנית להמחשה</span></div>` : '';
  const dirs = [[0, 'צפונה'], [90, 'מזרחה'], [180, 'דרומה'], [270, 'מערבה']];
  return `${img}<div class="nlck-row">${dirs.map(([b, l]) => `<button type="button" class="nlck-chip" data-act="face" data-v="${b}" aria-pressed="${angDiff(b, c.bearing) <= 45 ? 'true' : 'false'}">פונה ${l}</button>`).join('')}</div>
    <p class="nlck-note">ארבע דירות פינתיות בקומה טיפוסית, לפי 453 דירות ב-117 קומות ולפי שטח הקומה. אינה תוכנית מכר; הקומות העליונות שונות.</p>`;
}
function secInside() {
  const fac = [['fac-pool-c', 'הבריכה'], ['fac-gym-c', 'חדר הכושר'], ['fac-spa-c', 'הספא'], ['fac-lobby-c', 'הלובי'], ['fac-parking-c', 'החניון']];
  return `<div class="nlck-pic"><img src="${esc(asset('tour/living360-c30w-sunset-card.jpg'))}" alt="הסלון של הדירה לדוגמה בשקיעה" loading="lazy"><span class="cap">הדמיה להמחשה · דירה לדוגמה, מגדל C, קומה 30</span></div>
    <div class="nlck-row"><button type="button" class="nlck-btn nlck-btn--solid" data-act="inside">סיור 360 בדירה לדוגמה</button></div>
    <p class="nlck-note">בסיור: ארבעה סגנונות עיצוב (העיצוב המקורי, עץ חם, בהיר, אבן), חדר השינה, המרפסת, ומשם במעלית לבריכה, לחדר הכושר, לספא ולחניון.</p>
    <div class="nlck-floors">${fac.slice(0, 3).map(([f, l]) => `<button type="button" data-act="inside"><img src="${esc(asset('tour/' + f + '-card.jpg'))}" alt="" loading="lazy">${l}</button>`).join('')}</div>`;
}
function secAround() {
  if (!PL) return '<p class="nlck-note">טוען את המקומות…</p>';
  const out = [];
  for (const g of Object.keys(GROUPS)) {
    const near = PL.places.filter((p) => p.g === g && !p.generic && p.name).sort((a, b) => a.dist - b.dist).slice(0, 3);
    if (!near.length) continue;
    out.push(`<div class="grp">${GROUPS[g]}</div>` + near.map((p) => `<button type="button" data-act="place" data-v="${esc(p.id)}"><span>${esc(p.name)} <small>· ${esc(KINDS[p.k] || '')}</small></span><b>${bdi(num(p.dist))} מ׳${p.walk ? ` · ${bdi(p.walk)} דק׳` : ''}</b></button>`).join(''));
  }
  return `<div class="nlck-places">${out.join('')}</div><p class="nlck-note">מרחק ממרכז הכיכר וזמן הליכה. לחיצה מראה את המקום בעולם. מקור: עיריית תל אביב-יפו ו-OpenStreetMap.</p>`;
}
function cmpList() { return store.get('nlck-cmp', []); }
function secDecide(c) {
  const L = cmpList().filter((x) => !(x.tower === c.tower && x.floor === c.floor && x.bearing === Math.round(c.bearing)));
  const me = { tower: c.tower, floor: c.floor, bearing: Math.round(c.bearing), facing: c.facing, h: c.heightM };
  const card = (x, on) => {
    let w = '', s = '';
    try { const ww = world(); if (ww && ww.sunHours) { w = ww.sunHours(x.tower, x.floor, x.bearing, 12); s = ww.sunHours(x.tower, x.floor, x.bearing, 6); } } catch (e) { /* none */ }
    return `<div class="${on ? 'on' : ''}"><b>מגדל ${esc(x.tower)} · קומה ${bdi(x.floor)}</b><br>פונה ${esc(x.facing || '')} (${bdi(x.bearing + '°')})<br>גובה העיניים כ-${bdi(num(x.h, 1))} מ׳${w !== '' ? `<br>שמש בחורף כ-${bdi(w)} ש׳, בקיץ כ-${bdi(s)} ש׳` : ''}</div>`;
  };
  const cmp = L.length ? `<div class="nlck-note"><b>השוואה לדירות ששמרתם</b></div><div class="nlck-cmp">${card(me, true)}${L.slice(-1).map((x) => card(x, false)).join('')}</div>` : '<p class="nlck-note">שמרו את הדירה (הכפתור בתחתית) ובחרו דירה אחרת: כאן יופיעו שתיהן זו לצד זו.</p>';
  return `${cmp}
    <div class="nlck-share"><b>שלחו למשפחה את מה שבחרתם</b>
      <label><input type="checkbox" name="sh-apt" checked disabled>הדירה, הקומה והכיוון</label>
      <label><input type="checkbox" name="sh-view" checked>הנוף ושעות השמש</label>
      <label><input type="checkbox" name="sh-price">המחיר והעלויות לדוגמה</label>
      <span class="nlck-note">הקישור לא כולל שם, טלפון או פרטים אישיים.</span>
    </div>
    <div class="nlck-row"><button type="button" class="nlck-btn" data-act="share">שליחת הבחירה</button></div>`;
}

/* ---------------------------------------------------------------- the panel */
function isExample(c) { return c.tower === 'C' && c.floor >= 27 && c.floor <= 33 && angDiff(c.bearing, 265.61) <= 30; }
function summary(c) {
  let w = null; try { const ww = world(); w = ww && ww.sunHours ? ww.sunHours(c.tower, c.floor, c.bearing, 12) : null; } catch (e) { w = null; }
  return [`גובה העיניים כ-${bdi(num(c.heightM, 1))} מ׳`, w != null ? `כ-${bdi(w)} שעות שמש בחורף` : '', `עסקאות במגדלים ${bdi('9.58–10.63')} מ׳ ₪`].filter(Boolean).join(' · ');
}
const SUMS = {
  view: (c) => `פונה ${esc(c.facing || '')} · שעות השמש בכל עונה`,
  price: () => `עסקאות ${bdi('9.58–10.63')} מ׳ ₪ · מס רכישה · ארנונה · החזר חודשי`,
  plan: () => 'ארבע דירות פינתיות בקומה טיפוסית',
  inside: () => 'סיור 360 · ארבעה סגנונות · בריכה, חדר כושר וספא',
  around: () => 'בתי ספר, בתי קפה, תחבורה ובריאות, במטרים ובדקות',
  decide: () => 'השוואה · שליחה למשפחה בלי פרטים אישיים',
};
function body(id, c) { return { view: secView, price: secPrice, plan: secPlan, inside: secInside, around: secAround, decide: secDecide }[id](c); }
function render() {
  if (!el || !cur || !D) return;
  const c = cur;
  const keep = $('.nlck__body', el) ? $('.nlck__body', el).scrollTop : 0;
  el.innerHTML = `<button type="button" class="nlck__grab" data-act="grab" aria-label="${el.dataset.size === 'full' ? 'הקטנה' : 'הגדלה'}"></button>
    <div class="nlck__head"><div class="nlck__titles"><h2 class="nlck__title" tabindex="-1">מגדל ${esc(c.tower)} · קומה ${bdi(c.floor)} · פונה ${esc(c.facing || '')}</h2><p class="nlck__sum">${summary(c)}</p></div>
      ${isExample(c) ? '<span class="nlck__tag">דירה לדוגמה</span>' : ''}<button type="button" class="nlck__x" data-act="close" aria-label="סגירה">${ICON.x}</button></div>
    <nav class="nlck__nav" aria-label="קפיצה לחלק בדירה">${SECS.map(([id, l]) => `<a href="#nlck-${id}" data-act="jump" data-v="${id}" aria-current="${open[id] ? 'true' : 'false'}">${l}</a>`).join('')}</nav>
    <div class="nlck__body">${SECS.map(([id, l]) => `<section class="nlck-sec" id="nlck-${id}"><button type="button" class="nlck-sec__h" data-act="toggle" data-v="${id}" aria-expanded="${open[id] ? 'true' : 'false'}" aria-controls="nlck-b-${id}"><span><b>${l}</b><span class="s">${SUMS[id](c)}</span></span>${ICON.chev}</button><div class="nlck-sec__b" id="nlck-b-${id}" ${open[id] ? '' : 'hidden'}>${open[id] ? body(id, c) : ''}</div></section>`).join('')}</div>
    <div class="nlck__bar" data-bar></div><div class="nlck__toast" role="status" aria-live="polite" hidden></div>`;
  $('.nlck__body', el).scrollTop = keep;
  paintBar();
}
function paintBar() {
  const bar = el && $('[data-bar]', el);
  if (!bar) return;
  const room = avail ? `${location.pathname}?room=new${location.hash}` : '#nlsch';
  bar.innerHTML = `<a class="nlck-btn nlck-btn--solid" data-act="call" href="${esc(room)}">${ICON.video}${avail ? 'שיחת וידאו עכשיו, על הדירה הזאת' : 'תיאום שיחת וידאו על הדירה'}</a>
    ${C.wa ? `<a class="nlck__icon nlck__icon--wa" href="${esc(C.wa)}" target="_blank" rel="noopener" aria-label="וואטסאפ עם הבחירה" data-act="wa">${ICON.wa}</a>` : ''}
    <button type="button" class="nlck__icon" data-act="save" aria-label="שמירה להשוואה">${ICON.save}</button>`;
}
function toast(msg) {
  const t = el && $('.nlck__toast', el); if (!t) return;
  t.textContent = msg; t.hidden = false; clearTimeout(toast.h); toast.h = setTimeout(() => { t.hidden = true; }, 2600);
}
function setSize(s) { if (!el) return; el.dataset.size = s; const g = $('.nlck__grab', el); if (g) g.setAttribute('aria-label', s === 'full' ? 'הקטנה' : 'הגדלה'); }
function show(c) {
  cur = c; viewPick = null; tod = 'day';
  try { history.replaceState(history.state, '', `${location.pathname}${location.search}#dira=${c.tower}${c.floor}-${Math.round(c.bearing)}`); } catch (e) { /* file: */ }
  if (!el) mount();
  load().then(() => {
    const was = el.hidden;
    el.hidden = false; document.body.classList.add('nlck-on');
    if (was) setSize(innerWidth >= 1024 ? 'full' : 'half');
    render(); askAvail();
    if (was) { const h = $('.nlck__title', el); if (h) h.focus({ preventScroll: true }); }
    ga('cockpit_open', { tower: c.tower, floor: c.floor, facing: c.facing });
  });
}
function close() { if (!el) return; el.hidden = true; document.body.classList.remove('nlck-on'); ga('cockpit_close', {}); }
function mount() {
  el = document.createElement('aside');
  el.className = 'nlck'; el.id = 'nlck'; el.dir = 'rtl'; el.lang = 'he'; el.hidden = true; el.dataset.size = 'half';
  el.setAttribute('aria-label', 'הדירה שבחרתם');
  document.body.appendChild(el);
  el.addEventListener('click', onClick);
  el.addEventListener('input', onInput);
  el.addEventListener('change', onInput);
  el.addEventListener('keydown', (e) => { if (e.key === 'Escape') close(); });
  // the grab handle: drag up or down between peek, half and full (pointer events on the handle only: no gesture trap in the body)
  let y0 = null, h0 = 0;
  el.addEventListener('pointerdown', (e) => { if (!e.target.closest('.nlck__grab')) return; y0 = e.clientY; h0 = el.getBoundingClientRect().height; e.target.setPointerCapture(e.pointerId); });
  el.addEventListener('pointermove', (e) => { if (y0 == null) return; el.style.transition = 'none'; el.style.height = Math.max(150, Math.min(innerHeight * 0.92, h0 + (y0 - e.clientY))) + 'px'; });
  el.addEventListener('pointerup', (e) => {
    if (y0 == null) return;
    const dy = y0 - e.clientY; y0 = null; el.style.transition = ''; el.style.height = '';
    const s = el.dataset.size;
    if (Math.abs(dy) < 8) setSize(s === 'full' ? 'half' : s === 'half' ? 'full' : 'half');
    else if (dy > 0) setSize(s === 'peek' ? 'half' : 'full');
    else setSize(s === 'full' ? 'half' : 'peek');
  });
}
function onInput(e) {
  const t = e.target; if (!t.name || !t.closest('[data-calc]')) return;
  if (t.name === 'extra') calc.extra = t.checked; else { const v = parseFloat(t.value); if (isFinite(v)) calc[t.name] = v; }
  if (e.type === 'change' || t.type === 'checkbox') { const sec = $('#nlck-b-price', el); if (sec) { const f = document.activeElement && document.activeElement.name; sec.innerHTML = secPrice(); if (f) { const n = sec.querySelector(`[name="${f}"]`); if (n) n.focus(); } } }
}
function onClick(e) {
  const a = e.target.closest('[data-act]'); if (!a || !el.contains(a)) return;
  const act = a.dataset.act, v = a.dataset.v, w = world();
  if (act === 'close') return close();
  if (act === 'grab') return;
  if (act === 'toggle' || act === 'jump') {
    if (act === 'jump') { e.preventDefault(); open[v] = true; } else open[v] = !open[v];
    if (open[v] && v === 'around') loadPlaces().then(() => { if (open.around) { const b = $('#nlck-b-around', el); if (b) b.innerHTML = secAround(); } });
    render();
    if (act === 'jump') { const s = $('#nlck-' + v, el); if (s) s.scrollIntoView({ block: 'start', behavior: 'smooth' }); if (el.dataset.size === 'peek') setSize('half'); }
    ga('cockpit_section', { section: v, open: !!open[v] });
    return;
  }
  if (act === 'tod') { tod = v; return render(); }
  if (act === 'vfloor') { viewPick = +v; return render(); }
  if (act === 'window' && w) { w.setView('window'); setSize('peek'); return; }
  if (act === 'face' && w) { w.setFacing(+v, 'user'); return; }
  if (act === 'inside') { if (typeof window.__nlInsideGo === 'function') window.__nlInsideGo(); ga('cockpit_inside', {}); return; }
  if (act === 'place' && w) { w.setMode('places', 'user'); w.pickPlace(v); setSize('peek'); return; }
  if (act === 'save') {
    const L = cmpList().filter((x) => !(x.tower === cur.tower && x.floor === cur.floor && x.bearing === Math.round(cur.bearing)));
    L.push({ tower: cur.tower, floor: cur.floor, bearing: Math.round(cur.bearing), facing: cur.facing, h: cur.heightM });
    store.set('nlck-cmp', L.slice(-3)); toast('נשמר. בחרו דירה אחרת, והן יופיעו זו לצד זו תחת "החלטה".'); ga('cockpit_save', {}); return;
  }
  if (act === 'share') {
    const withView = $('[name="sh-view"]', el) && $('[name="sh-view"]', el).checked, withPrice = $('[name="sh-price"]', el) && $('[name="sh-price"]', el).checked;
    const lines = [`מגדלי כיכר המדינה, תל אביב · מגדל ${cur.tower} · קומה ${cur.floor} · פונה ${cur.facing || ''}`];
    if (withView) { let wn = null; try { wn = w && w.sunHours ? w.sunHours(cur.tower, cur.floor, cur.bearing, 12) : null; } catch (er) { wn = null; } lines.push(`גובה העיניים כ-${num(cur.heightM, 1)} מ׳${wn != null ? `, כ-${wn} שעות שמש בחורף` : ''}`); }
    if (withPrice) { const tax = taxOf(calc.price, calc.extra ? D.tax.additional : D.tax.only); lines.push(`דוגמה: מחיר ${num(calc.price)} ₪, מס רכישה ${num(tax)} ₪`); }
    const url = `${location.origin}${location.pathname}#dira=${cur.tower}${cur.floor}-${Math.round(cur.bearing)}`;
    const text = lines.join('\n');
    ga('cockpit_share', { view: !!withView, price: !!withPrice });
    if (navigator.share) { navigator.share({ title: 'מגדלי כיכר המדינה', text, url }).catch(() => {}); return; }
    const all = text + '\n' + url;
    (navigator.clipboard ? navigator.clipboard.writeText(all) : Promise.reject()).then(() => toast('הקישור הועתק. אפשר להדביק בכל הודעה.'), () => toast(url));
    return;
  }
  if (act === 'call') { ga('cockpit_call', { now: !!avail }); if (!avail) { e.preventDefault(); setSize('peek'); const s = document.getElementById('nlsch'); if (s) s.scrollIntoView({ behavior: 'smooth', block: 'start' }); } return; }
  if (act === 'wa') { ga('cockpit_wa', {}); }
}

/* ---------------------------------------------------------------- wiring */
addEventListener('nl:facing', (e) => { const d = e.detail || {}; if (d.tower && d.floor && d.bearing != null) show(d); });
// a link that reopens a choice: #dira=C30-266
(function reopen() {
  const m = /^#dira=([ABC])(\d{1,2})-(\d{1,3})$/.exec(location.hash || '');
  if (!m) return;
  let tries = 0;
  const go = () => {
    const w = world();
    if (!w) { if (++tries < 120) setTimeout(go, 250); return; }
    w.ready.then(() => { w.pickTower(m[1], 'api'); w.setFloor(+m[2], 'api'); w.setFacing(+m[3], 'api'); }).catch(() => {});
  };
  go();
}());
load().catch(() => {});
