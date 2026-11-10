/*
 * The apartment cockpit, version 2 (HAD-699, Ben 10.11.2026: "a person presses, he enters the cockpit of his life... from there
 * everything: the view, information, plans, designing the apartment, everything, on the phone"). Design: the canvas
 * https://claude.ai/artifact/FzvFDybiyBoi8bspoPV9Zp, row "הקוקפיט של הדירה".
 * A full-screen app for the chosen apartment: the real view from it at the top, nine tiles below, each opening full screen and
 * coming back to the apartment: the view (every rendered floor and direction), inside in 360 (the example apartment, four
 * styles), the designer (/tour/designer/ opened for THIS unit, as on Ashira, Rainbow and DUO), the plan, the facilities in 360,
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
const $ = (s, r = document) => r.querySelector(s);
const esc = (s) => String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const num = (n, d = 0) => (n == null || !isFinite(n) ? '' : Number(n).toLocaleString('he-IL', { minimumFractionDigits: d, maximumFractionDigits: d }));
const bdi = (s) => `<bdi>${esc(s)}</bdi>`;
const ils = (n, d = 0) => `${bdi(num(n, d))} ₪`;
const A = (p) => (C.base || '') + p + (C.ver ? (p.includes('?') ? '&' : '?') + 'ver=' + C.ver : '');
const ga = (n, p) => { try { if (window.nadlanGA) window.nadlanGA(n, Object.assign({ project: 'hamedina' }, p || {})); } catch (e) { /* none */ } };
const store = { get(k, d) { try { const v = localStorage.getItem(k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } }, set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* private mode */ } } };
const angDiff = (a, b) => Math.abs(((a - b) % 360 + 540) % 360 - 180);
const DIRS = ['צפונה', 'צפון-מזרחה', 'מזרחה', 'דרום-מזרחה', 'דרומה', 'דרום-מערבה', 'מערבה', 'צפון-מערבה'];
const dirWord = (b) => DIRS[Math.round((((b % 360) + 360) % 360) / 45) % 8];
const SECTORS = [[245, 300, 'הים והעיר'], [300, 345, 'הים והירקון'], [345, 30, 'הירקון והצפון'], [30, 75, 'רמת אביב והאוניברסיטה'], [75, 120, 'רמת גן והבורסה'], [120, 200, 'מגדלי העיר'], [200, 245, 'הצפון הישן ומרכז העיר']];
const sectorOf = (b) => { b = ((b % 360) + 360) % 360; const s = SECTORS.find(([lo, hi]) => (lo < hi ? b >= lo && b < hi : b >= lo || b < hi)); return s ? s[2] : ''; };
const eyeH = (f) => (f - 1) * 4 + 1.6;
const GROUPS = { education: 'חינוך', food: 'אוכל וקפה', essentials: 'קניות ושירותים', transport: 'תחבורה', outdoors: 'גנים וספורט', health: 'בריאות', community: 'קהילה ותרבות' };
const KINDS = { school: 'בית ספר', kindergarten: 'גן ילדים', college: 'מכללה', daycare: 'מעון', park: 'גן', dog_park: 'גינת כלבים', gym: 'חדר כושר', bus_stop: 'תחנת אוטובוס', restaurant: 'מסעדה', cafe: 'בית קפה', bakery: 'מאפייה', shopping: 'חנות', supermarket: 'סופרמרקט', bank: 'בנק', pharmacy: 'בית מרקחת', clinic: 'מרפאה', hospital: 'בית חולים', health: 'בריאות', community: 'מרכז קהילתי', worship: 'בית כנסת', culture: 'תרבות', light_rail: 'רכבת קלה', rail: 'רכבת', playground: 'גן שעשועים', library: 'ספרייה' };
const PANOS = [['living360-c30w-sunset', 'העיצוב המקורי'], ['living360-c30w-sunset-warm', 'עץ חם'], ['living360-c30w-sunset-light', 'בהיר'], ['living360-c30w-sunset-stone', 'אבן']];
const FACS = [['fac-pool-c', 'הבריכה'], ['fac-gym-c', 'חדר הכושר'], ['fac-spa-c', 'הספא'], ['fac-lobby-c', 'הלובי'], ['fac-parking-c', 'החניון']];
const ICON = {
  video: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="6" width="13" height="12" rx="2"/><path d="M16 10l5-3v10l-5-3"/></svg>',
  wa: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20l1.3-3.9A8 8 0 1 1 8 19z"/><path d="M9 9.5c.5 2 2.5 4 4.5 4.5l1.2-1.2 2 1-.5 1.7c-3.5.4-8-4-7.6-7.6L10.3 7l1 2z"/></svg>',
  heart: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/></svg>',
};

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
function unitId(c) { const s = ['n', 'e', 's', 'w'][Math.round((((c.bearing % 360) + 360) % 360) / 90) % 4]; return `${c.tower}-${c.floor}-${s}`; }
function label(c) { return `מגדל ${c.tower} · קומה ${c.floor} · פונה ${dirWord(c.bearing)}`; }

/* ---------------------------------------------------------------- the screens */
function home(c) {
  const v = viewOf(c);
  const hero = v ? A(v.big) : A('aerial-1600.webp');
  const t = (k, lab, img, big) => `<button type="button" class="nlck-tile" data-open="${k}">${img ? `<img src="${esc(img)}" alt="" loading="lazy">` : ''}${big ? `<span class="big">${big}</span>` : ''}<span class="lab">${lab}</span></button>`;
  const firstFac = A('tour/' + FACS[0][0] + '-card.jpg');
  return `<div class="nlck-hero"><img src="${esc(hero)}" alt="${esc('הנוף מהדירה: ' + label(c))}">
      <div class="nlck-top"><button type="button" class="nlck-back" data-open="">› חזרה</button><span class="nlck-cap">הדמיה להמחשה${v && v.floor !== c.floor ? ` · הנוף מקומה ${v.floor}` : ''}</span></div>
      <div class="nlck-ht"><h2 class="nlck-title" tabindex="-1">מגדל ${esc(c.tower)} · קומה ${bdi(c.floor)}</h2><p>פונה ${esc(dirWord(c.bearing))} · ${esc(sectorOf(c.bearing))}</p>
      <div class="nlck-chips"><span>גובה העיניים כ-${bdi(eyeH(c.floor).toFixed(0))} מ׳ מעל הרחוב</span></div></div></div>
    <p class="nlck-ask">מה תרצו לראות?</p>
    <div class="nlck-grid">
      ${t('view', 'הנוף', v ? A(v.img) : '')}
      ${t('inside', 'בפנים · 360°', A('tour/living-c30w-day-card.jpg'))}
      ${t('design', 'עצבו את הדירה', A('tour/bedroom-c30nw-day-card.jpg'))}
      ${t('plan', 'התוכנית', D.plan ? A(D.plan) : '')}
      ${t('fac', 'המתקנים · 360°', firstFac)}
      ${t('price', 'מחיר ועלות', '', `${bdi(num(Math.min(...D.deals.map((d) => d.price)) / 1e6, 2) + '–' + num(Math.max(...D.deals.map((d) => d.price)) / 1e6, 2))}<small>מיליון ₪, עסקאות שפורסמו</small>`)}
      ${t('area', 'השכונה', A('aerial-800.webp'))}
      ${film() ? t('film', 'הסרט', film().poster || A('aerial-tall-800.webp')) : ''}
      ${t('save', 'השוואה ושליחה', '', `${bdi(String(cmpList().length))}<small>שמורות</small>`)}
    </div>`;
}
function subTop(title) { return `<div class="nlck-subtop"><button type="button" class="nlck-back" data-open="">› לדירה</button><span>${esc(title)}</span></div>`; }
function scrView(c) {
  const v = sub.view || viewOf(c);
  if (!v) return subTop('הנוף') + '<p class="nlck-pad">אין עדיין תמונה מהקומה הזאת.</p>';
  const fl = floorsOf(c), sd = sidesOf(c);
  return `${subTop(label(c))}<div class="nlck-pan" data-pan><img src="${esc(A(v.big))}" alt="${esc('הנוף מקומה ' + v.floor + ', ' + dirWord(v.bearing))}"></div>
    <span class="nlck-cap" style="top:64px;bottom:auto">הדמיה להמחשה · קומה ${v.floor} · ${esc(dirWord(v.bearing))}</span>
    <div class="nlck-under"><div class="nlck-hint">גררו לצדדים כדי לראות את כל הנוף</div>
      ${fl.length > 1 ? `<div class="nlck-row-t">אותו כיוון, קומות אחרות</div><div class="nlck-strip">${fl.map((x) => `<button type="button" data-v="${esc(x.img)}" data-vk="floor" aria-pressed="${x === v}"><img src="${esc(A(x.img))}" alt=""><b>קומה ${bdi(x.floor)}</b></button>`).join('')}</div>` : ''}
      ${sd.length > 1 ? `<div class="nlck-row-t">אותה קומה, כיוונים אחרים</div><div class="nlck-strip">${sd.map((x) => `<button type="button" data-v="${esc(x.img)}" data-vk="side" aria-pressed="${x === v}"><img src="${esc(A(x.img))}" alt=""><b>${esc(dirWord(x.bearing))}</b></button>`).join('')}</div>` : ''}
    </div>`;
}
function scrInside() {
  return `${subTop('בפנים · 360°')}<div class="nlck-360" data-360="${esc(A('tour/' + PANOS[sub.pano][0] + '-2k.webp'))}" role="img" aria-label="סיור 360 בסלון של הדירה לדוגמה"></div>
    <span class="nlck-cap" style="top:64px;bottom:auto">דירה לדוגמה, מגדל C קומה 30 · גררו כדי להסתכל מסביב</span>
    <div class="nlck-float">${PANOS.map((p, i) => `<button type="button" data-pano="${i}" aria-pressed="${i === sub.pano}">${esc(p[1])}</button>`).join('')}</div>`;
}
function scrFac() {
  return `${subTop('המתקנים · 360°')}<div class="nlck-360" data-360="${esc(A('tour/' + FACS[sub.fac][0] + '-2k.webp'))}" role="img" aria-label="${esc(FACS[sub.fac][1])}, 360"></div>
    <span class="nlck-cap" style="top:64px;bottom:auto">${esc(FACS[sub.fac][1])} · הדמיה להמחשה · גררו כדי להסתכל מסביב</span>
    <div class="nlck-float">${FACS.map((f, i) => `<button type="button" data-fac="${i}" aria-pressed="${i === sub.fac}">${esc(f[1])}</button>`).join('')}</div>`;
}
function scrDesign(c) {
  const u = `/tour/designer/?project=hamedina&unit=${encodeURIComponent(unitId(c))}&pn=${encodeURIComponent('מגדלי כיכר המדינה')}&ul=${encodeURIComponent(label(c))}`;
  return `${subTop('עיצוב הדירה')}<iframe class="nlck-frame" src="${esc(u)}" title="עיצוב הדירה: ${esc(label(c))}" allow="fullscreen; xr-spatial-tracking"></iframe>
    <a class="nlck-ext" href="${esc(u)}" target="_blank" rel="noopener">לפתוח במסך נפרד</a>`;
}
function scrPlan() {
  return `${subTop('התוכנית')}<div class="nlck-white"><div class="nlck-zoom" data-zoom><img src="${esc(A(D.plan))}" alt="תוכנית קומה טיפוסית: ארבע דירות פינתיות סביב גרעין עגול"></div>
    <p class="nlck-note">הקישו על התוכנית כדי להגדיל. תוכנית להמחשה של קומה טיפוסית: ארבע דירות פינתיות, לפי 453 דירות ב-117 קומות ולפי שטח הקומה. אינה תוכנית מכר.</p>
    <p class="nlck-note">תוכניות מכר אמיתיות נשלחות בשיחה עם הנציג.</p></div>`;
}
function scrPrice() {
  const deals = D.deals.map((d) => `<div class="r"><span>קומה ${bdi(d.floor)} · ${esc(d.apt)} · ${bdi(d.date)}</span><b>${bdi(num(d.price / 1e6, 2))} מ׳ ₪</b></div>`).join('');
  const tax = taxOf(calc.price, calc.extra ? D.tax.additional : D.tax.only);
  const arn = (calc.size > 140 ? D.arnona.gt140 : D.arnona.le140) * calc.size;
  const pm = monthly(calc.price * calc.share / 100, calc.rate, calc.years);
  const src = D.deals[0];
  return `${subTop('מחיר ועלות')}<div class="nlck-white" data-calc>
    <div class="nlck-box"><b>עסקאות שפורסמו במגדלים</b>${deals}<small>מקור: <a href="${esc(src.url)}" target="_blank" rel="noopener">${esc(src.src)}</a> · המגדל של כל עסקה לא פורסם</small></div>
    <div class="nlck-box nlck-calc">
      <label>מחיר הדירה לדוגמה (₪)<input type="number" inputmode="numeric" step="10000" name="price" value="${calc.price}"></label>
      <label>דירה נוספת<input type="checkbox" name="extra" ${calc.extra ? 'checked' : ''}></label>
      <label>מימון (%)<input type="number" inputmode="numeric" min="0" max="75" step="5" name="share" value="${calc.share}"></label>
      <label>שנים<input type="number" inputmode="numeric" min="4" max="30" name="years" value="${calc.years}"></label>
      <label>ריבית (%)<input type="number" inputmode="decimal" step="0.05" name="rate" value="${calc.rate}"></label>
      <label>שטח לארנונה (מ״ר)<input type="number" inputmode="numeric" name="size" value="${calc.size}"></label>
      ${D.fee ? `<label>דמי תחזוקה (₪ בחודש)<input type="number" inputmode="numeric" step="100" name="fee" value="${calc.fee}"></label>` : ''}
    </div>
    <div class="nlck-box"><div class="r"><span>מס רכישה</span><b>${ils(tax)}</b></div><div class="r tot"><span>המחיר והמס יחד</span><b>${ils(calc.price + tax)}</b></div>
      <div class="r"><span>משכנתא בחודש, לדוגמה</span><b>${ils(Math.round(pm))}</b></div><div class="r"><span>ארנונה בחודש</span><b>${ils(Math.round(arn / 12))}</b></div>
      ${D.fee ? `<div class="r"><span>תחזוקה בחודש</span><b>${ils(calc.fee)}</b></div>` : ''}<div class="r tot"><span>בחודש, הכול יחד</span><b>${ils(Math.round(pm + arn / 12 + (D.fee ? calc.fee : 0)))}</b></div></div>
    <p class="nlck-note">דוגמה בלבד; ברירת המחדל היא העסקה הנמוכה שפורסמה. מס רכישה: ${esc(D.tax.asof)}. ארנונה: ${esc(D.arnona.asof)}, אזור ${D.arnona.zone}. ריבית: ממוצע ${esc(D.mortgage.src)}, ${esc(D.mortgage.label)}. ${D.fee ? `תחזוקה: לפי <a href="${esc(D.fee.url)}" target="_blank" rel="noopener">${esc(D.fee.src)}</a>, ${esc(D.fee.note)}.` : ''} שכר טרחה ותיווך לא כלולים.</p></div>`;
}
function scrArea() {
  if (!PL) return `${subTop('השכונה')}<p class="nlck-pad">טוען…</p>`;
  const out = [];
  for (const g of Object.keys(GROUPS)) {
    const near = PL.places.filter((p) => p.g === g && !p.generic && p.name).sort((a, b) => a.dist - b.dist).slice(0, 4);
    if (!near.length) continue;
    out.push(`<div class="nlck-grp">${GROUPS[g]}</div>` + near.map((p) => `<a class="nlck-place" href="https://www.google.com/maps/dir/?api=1&amp;destination=${p.lat},${p.lng}&amp;travelmode=walking" target="_blank" rel="noopener"><span>${esc(p.name)} <small>· ${esc(KINDS[p.k] || '')}</small></span><b>${bdi(num(p.dist))} מ׳${p.walk ? ` · ${bdi(p.walk)} דק׳` : ''}</b></a>`).join(''));
  }
  return `${subTop('השכונה')}<div class="nlck-white"><p class="nlck-note">ממרכז הכיכר, ברגל. לחיצה פותחת ניווט. מקור: עיריית תל אביב-יפו ו-OpenStreetMap.</p>${out.join('')}</div>`;
}
function film() { // the page's own Kikar film (ProjectFilm): the tall cut on phones, the wide one on screens
  const src = (v) => { const s = v.querySelector('source'); return (s ? s.getAttribute('src') : v.getAttribute('src')) || ''; };
  const vs = [...document.querySelectorAll('video')].filter((v) => /kikar|hamedina/i.test(src(v)));
  if (!vs.length) return null;
  const v = vs.find((x) => x.classList.contains(innerWidth < 700 ? 'nlws-film__v--tall' : 'nlws-film__v--wide')) || vs[0];
  return { src: src(v), poster: v.getAttribute('data-nlposter') || v.getAttribute('poster') || '' };
}
function scrFilm() { const f = film() || {}; return `${subTop('הסרט')}<video class="nlck-video" src="${esc(f.src)}" poster="${esc(f.poster)}" controls playsinline preload="metadata" autoplay></video>`; }
function cmpList() { return store.get('nlck-cmp', []); }
function isSaved() { if (!cur) return false; const b = Math.round(cur.bearing); return cmpList().some((x) => x.tower === cur.tower && x.floor === cur.floor && x.bearing === b); }
function scrSave(c) {
  const L = cmpList();
  const me = { tower: c.tower, floor: c.floor, bearing: Math.round(c.bearing) };
  const has = L.some((x) => x.tower === me.tower && x.floor === me.floor && x.bearing === me.bearing);
  const card = (x) => { const v = viewOf({ ...x, heightM: eyeH(x.floor) }); return `<div class="nlck-cmp-c">${v ? `<img src="${esc(A(v.img))}" alt="">` : ''}<b>מגדל ${esc(x.tower)} · קומה ${bdi(x.floor)}</b><span>פונה ${esc(dirWord(x.bearing))} · ${esc(sectorOf(x.bearing))}</span><span>גובה העיניים כ-${bdi(eyeH(x.floor).toFixed(0))} מ׳</span></div>`; };
  return `${subTop('השוואה ושליחה')}<div class="nlck-white">
    <div class="nlck-row"><button type="button" class="nlck-btn" data-act="save">${has ? 'הדירה שמורה' : 'שמירת הדירה הזאת'}</button></div>
    ${L.length ? `<div class="nlck-cmp">${[me, ...L.filter((x) => !(x.tower === me.tower && x.floor === me.floor && x.bearing === me.bearing))].slice(0, 3).map(card).join('')}</div>` : '<p class="nlck-note">שמרו את הדירה, בחרו דירה אחרת, והן יופיעו כאן זו לצד זו.</p>'}
    <div class="nlck-box"><b>שלחו למשפחה את מה שבחרתם</b>
      <label class="ck"><input type="checkbox" checked disabled>הדירה, הקומה והכיוון</label>
      <label class="ck"><input type="checkbox" name="sh-view" checked>הנוף וגובה הקומה</label>
      <label class="ck"><input type="checkbox" name="sh-price">המחיר והעלויות לדוגמה</label>
      <small>הקישור לא כולל שם, טלפון או פרטים אישיים.</small></div>
    <div class="nlck-row"><button type="button" class="nlck-btn nlck-btn--solid" data-act="share">שליחת הבחירה</button></div></div>`;
}

/* ---------------------------------------------------------------- the 360 viewer (three.js from the page's import map) */
let PV = null;
async function pano(host, url) {
  if (PV) { PV.destroy(); PV = null; }
  let THREE;
  try { THREE = await import('three'); } catch (e) { host.innerHTML = `<div class="nlck-pan" data-pan><img src="${esc(url)}" alt=""></div>`; return; }
  const W = () => host.clientWidth, H = () => host.clientHeight;
  const r = new THREE.WebGLRenderer({ antialias: true }); r.setPixelRatio(Math.min(2, devicePixelRatio || 1)); r.setSize(W(), H()); host.appendChild(r.domElement);
  const scene = new THREE.Scene(), cam = new THREE.PerspectiveCamera(W() < 600 ? 80 : 70, W() / H(), 0.1, 100);
  const tex = await new THREE.TextureLoader().loadAsync(url); tex.colorSpace = THREE.SRGBColorSpace;
  const geo = new THREE.SphereGeometry(10, 64, 32); geo.scale(-1, 1, 1); scene.add(new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ map: tex })));
  let lon = 180, lat = 0, x0 = null, y0 = 0, l0 = 0, a0 = 0, run = true;
  const draw = () => { if (!run) return; const p = THREE.MathUtils.degToRad(90 - lat), t = THREE.MathUtils.degToRad(lon); cam.lookAt(Math.sin(p) * Math.cos(t), Math.cos(p), Math.sin(p) * Math.sin(t)); r.render(scene, cam); requestAnimationFrame(draw); };
  host.addEventListener('pointerdown', (e) => { x0 = e.clientX; y0 = e.clientY; l0 = lon; a0 = lat; host.setPointerCapture(e.pointerId); });
  host.addEventListener('pointermove', (e) => { if (x0 == null) return; lon = l0 - (e.clientX - x0) * 0.16; lat = Math.max(-75, Math.min(75, a0 + (e.clientY - y0) * 0.16)); });
  host.addEventListener('pointerup', () => { x0 = null; });
  const rs = () => { r.setSize(W(), H()); cam.aspect = W() / H(); cam.updateProjectionMatrix(); }; addEventListener('resize', rs);
  draw();
  PV = { destroy() { run = false; removeEventListener('resize', rs); geo.dispose(); tex.dispose(); r.dispose(); r.domElement.remove(); } };
}

/* ---------------------------------------------------------------- the app */
function render() {
  if (!el || !cur || !D) return;
  if (PV) { PV.destroy(); PV = null; }
  const body = $('.nlck-body', el);
  const c = cur;
  const h = { view: () => scrView(c), inside: scrInside, fac: scrFac, design: () => scrDesign(c), plan: scrPlan, price: scrPrice, area: scrArea, film: scrFilm, save: () => scrSave(c) }[open];
  body.innerHTML = h ? h() : home(c);
  body.dataset.screen = el.dataset.screen = open || 'home';
  body.scrollTop = 0;
  const p3 = $('[data-360]', body); if (p3) pano(p3, p3.dataset['360']);
  const pan = $('[data-pan]', body); if (pan) { const im = $('img', pan); const ctr = () => { pan.scrollLeft = -(pan.scrollWidth - pan.clientWidth) / 2; }; if (im) { if (im.complete) ctr(); else im.addEventListener('load', ctr, { once: true }); } }
  if (open === 'area' && !PL) loadPlaces().then(() => { if (open === 'area') render(); });
  paintBar();
}
function paintBar() {
  const bar = el && $('.nlck-bar', el); if (!bar) return;
  const room = avail ? `${location.pathname}${location.search ? location.search + '&' : '?'}room=new${location.hash}` : '#nlsch';
  bar.innerHTML = `<a class="nlck-call" data-act="call" href="${esc(room)}">${ICON.video}${avail ? 'שיחת וידאו עכשיו, על הדירה' : 'שיחת וידאו על הדירה'}</a>
    ${C.wa ? `<a class="nlck-ic nlck-ic--wa" href="${esc(C.wa)}" target="_blank" rel="noopener" aria-label="וואטסאפ" data-act="wa">${ICON.wa}</a>` : ''}
    <button type="button" class="nlck-ic" data-act="save" aria-label="שמירת הדירה" aria-pressed="${isSaved()}">${ICON.heart}</button>`;
}
function toast(msg) { const t = el && $('.nlck-toast', el); if (!t) return; t.textContent = msg; t.hidden = false; clearTimeout(toast.h); toast.h = setTimeout(() => { t.hidden = true; }, 2600); }
function mount() {
  el = document.createElement('div');
  el.className = 'nlck'; el.id = 'nlck'; el.dir = 'rtl'; el.lang = 'he'; el.hidden = true;
  el.setAttribute('role', 'dialog'); el.setAttribute('aria-modal', 'true'); el.setAttribute('aria-label', 'הדירה שבחרתם');
  el.innerHTML = '<div class="nlck-body"></div><div class="nlck-bar"></div><div class="nlck-toast" role="status" aria-live="polite" hidden></div>';
  document.body.appendChild(el);
  el.addEventListener('click', onClick);
  el.addEventListener('change', onInput);
  el.addEventListener('keydown', (e) => { if (e.key === 'Escape') { if (open) { open = null; render(); } else close(); } });
}
function show(c, from) {
  cur = { tower: c.tower, floor: +c.floor, bearing: +c.bearing, heightM: c.heightM || eyeH(+c.floor) };
  viaJourney = from === 'journey'; open = null; sub.view = null;
  try { history.replaceState(history.state, '', `${location.pathname}${location.search}#dira=${cur.tower}${cur.floor}-${Math.round(cur.bearing)}`); } catch (e) { /* file: */ }
  if (!el) mount();
  load().then(() => {
    el.hidden = false; document.documentElement.style.overflow = 'hidden'; document.body.classList.add('nlck-on');
    render(); askAvail();
    const h = $('.nlck-title', el); if (h) h.focus({ preventScroll: true });
    ga('cockpit_open', { tower: cur.tower, floor: cur.floor, facing: dirWord(cur.bearing) });
  });
}
function close() {
  if (!el) return; if (PV) { PV.destroy(); PV = null; }
  el.hidden = true; document.documentElement.style.overflow = ''; document.body.classList.remove('nlck-on');
  if (viaJourney && window.__nlJourney && window.__nlJourney.open) window.__nlJourney.open(4);
}
function onInput(e) {
  const t = e.target; if (!t.name || !t.closest('[data-calc]')) return;
  if (t.name === 'extra') calc.extra = t.checked; else { const v = parseFloat(t.value); if (isFinite(v)) calc[t.name] = v; }
  render(); const n = $(`[name="${t.name}"]`, el); if (n && t.type !== 'checkbox') n.focus();
}
function onClick(e) {
  const o = e.target.closest('[data-open]');
  if (o && el.contains(o)) { const k = o.dataset.open; if (!k && !open) return close(); open = k || null; if (k !== 'view') sub.view = null; render(); ga('cockpit_tile', { tile: k || 'home' }); return; }
  const v = e.target.closest('[data-v]'); if (v) { sub.view = rendered().find((x) => x.img === v.dataset.v) || null; if (sub.view && v.dataset.vk === 'side') { cur.bearing = sub.view.bearing; } return render(); }
  const p = e.target.closest('[data-pano]'); if (p) { sub.pano = +p.dataset.pano; return render(); }
  const f = e.target.closest('[data-fac]'); if (f) { sub.fac = +f.dataset.fac; return render(); }
  const z = e.target.closest('[data-zoom]'); if (z) { z.classList.toggle('on'); return; }
  const a = e.target.closest('[data-act]'); if (!a) return;
  const act = a.dataset.act;
  if (act === 'save') {
    const me = { tower: cur.tower, floor: cur.floor, bearing: Math.round(cur.bearing) };
    const L = cmpList().filter((x) => !(x.tower === me.tower && x.floor === me.floor && x.bearing === me.bearing)); L.unshift(me); store.set('nlck-cmp', L.slice(0, 4));
    toast('הדירה נשמרה. בחרו דירה אחרת, והן יופיעו זו לצד זו.'); ga('cockpit_save', {}); if (open === 'save' || !open) render(); else paintBar(); return;
  }
  if (act === 'share') {
    const withView = $('[name="sh-view"]', el) && $('[name="sh-view"]', el).checked, withPrice = $('[name="sh-price"]', el) && $('[name="sh-price"]', el).checked;
    const lines = [`מגדלי כיכר המדינה, תל אביב · ${label(cur)}`];
    if (withView) lines.push(`${sectorOf(cur.bearing)} · גובה העיניים כ-${eyeH(cur.floor).toFixed(0)} מ׳`);
    if (withPrice) { const tax = taxOf(calc.price, calc.extra ? D.tax.additional : D.tax.only); lines.push(`דוגמה: מחיר ${num(calc.price)} ₪, מס רכישה ${num(tax)} ₪`); }
    const url = `${location.origin}${location.pathname}#dira=${cur.tower}${cur.floor}-${Math.round(cur.bearing)}`;
    ga('cockpit_share', { view: !!withView, price: !!withPrice });
    if (navigator.share) { navigator.share({ title: 'מגדלי כיכר המדינה', text: lines.join('\n'), url }).catch(() => {}); return; }
    (navigator.clipboard ? navigator.clipboard.writeText(lines.join('\n') + '\n' + url) : Promise.reject()).then(() => toast('הקישור הועתק. אפשר להדביק בכל הודעה.'), () => toast(url));
    return;
  }
  if (act === 'call') { ga('cockpit_call', { now: !!avail }); if (!avail) { e.preventDefault(); close(); const s = document.getElementById('nlsch'); if (s) s.scrollIntoView({ behavior: 'smooth', block: 'start' }); } return; }
  if (act === 'wa') ga('cockpit_wa', {});
}

window.__nlCockpit = { open: (d, from) => show(d, from) };
addEventListener('nl:facing', (e) => { const d = e.detail || {}; if (d.tower && d.floor && d.bearing != null) show(d, d.source); });
function reopen() { // a link that reopens a choice: #dira=A30-262
  const m = /^#dira=([ABC])(\d{1,2})-(\d{1,3})$/.exec(location.hash || '');
  if (m && !(cur && el && !el.hidden && cur.tower === m[1] && cur.floor === +m[2] && Math.round(cur.bearing) === +m[3])) show({ tower: m[1], floor: +m[2], bearing: +m[3] }, 'link');
}
reopen();
addEventListener('hashchange', reopen);
load().catch(() => {});
