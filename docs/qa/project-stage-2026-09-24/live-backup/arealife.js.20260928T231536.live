/* AreaLife (design system AreaLife v97, 28.9.2026): what is around the building, from one place registry
 * (rainbow/places.json, scripts/project-stage/build_places_rainbow.py), in the view from the floor, the 360 windows and the
 * list under the view. The owner, 28.9: "they don't want to see white buildings, they want to know what's in the
 * neighbourhood". Codex (28.9): one layer for all the surfaces; every place with its source; only what a window can see
 * is named in it (a straight sight line over the city's buildings layer, computed offline per floor band).
 * Places come from findplace.co.il (Tel Aviv-Yafo municipality open data + OpenStreetMap) and OpenStreetMap (ODbL), walking
 * minutes from Mapbox's walking router, all said on the page. A light-rail station findplace marks as future is a planned
 * station, said so, never a running one. On a
 * language page a place shows only with a name in that language (or English); a Hebrew-only name waits for its page. */

export const GROUPS = {
  education: { he: 'חינוך', color: '#3E5A45', w: 3 },
  outdoors: { he: 'פארקים, חוף וספורט', color: '#517048', w: 2.4 },
  transport: { he: 'תחבורה', color: '#2F6F86', w: 3.2 },
  food: { he: 'קפה ומסעדות', color: '#8A6B3F', w: 2.2 },
  essentials: { he: 'קניות וסידורים', color: '#9F6F54', w: 1.9 },
  health: { he: 'בריאות', color: '#A93F2A', w: 2.3 },
  community: { he: 'קהילה ותרבות', color: '#6B4F7A', w: 2 },
};
const P = 'fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"';
export const ICONS = {
  education: '<svg viewBox="0 0 16 16" ' + P + '><path d="M1.5 6.2 8 3l6.5 3.2L8 9.4z"/><path d="M4 7.6v3.1c1.1 1 2.5 1.6 4 1.6s2.9-.6 4-1.6V7.6"/></svg>',
  outdoors: '<svg viewBox="0 0 16 16" ' + P + '><path d="M8 14.5v-4"/><path d="M8 1.8c-2.6 0-4.2 2-4.2 4.3 0 2.3 1.9 4.1 4.2 4.1s4.2-1.8 4.2-4.1C12.2 3.8 10.6 1.8 8 1.8z"/></svg>',
  transport: '<svg viewBox="0 0 16 16" ' + P + '><rect x="3.8" y="2.2" width="8.4" height="9.2" rx="2"/><path d="M3.8 7.2h8.4M5.8 14.2l1.2-2.8M10.2 14.2 9 11.4"/></svg>',
  food: '<svg viewBox="0 0 16 16" ' + P + '><path d="M2.8 6h8.4v3.4A3.6 3.6 0 0 1 7.6 13h-1.2a3.6 3.6 0 0 1-3.6-3.6z"/><path d="M11.2 7h1.1a1.8 1.8 0 0 1 0 3.6h-1.1M5.4 2.4v1.8M8.6 2.4v1.8"/></svg>',
  essentials: '<svg viewBox="0 0 16 16" ' + P + '><path d="M3.3 5.6h9.4l-.9 8.2H4.2z"/><path d="M5.8 5.6V4.7a2.2 2.2 0 0 1 4.4 0v.9"/></svg>',
  health: '<svg viewBox="0 0 16 16" ' + P + '><path d="M6.4 2.4h3.2v4h4v3.2h-4v4H6.4v-4h-4V6.4h4z"/></svg>',
  community: '<svg viewBox="0 0 16 16" ' + P + '><path d="M2.5 6.2 8 2.8l5.5 3.4M3.6 6.6v6.2M6.5 6.6v6.2M9.5 6.6v6.2M12.4 6.6v6.2M2.2 13.6h11.6"/></svg>',
};

const norm = (b) => ((Number(b) % 360) + 360) % 360;
const angOff = (a, b) => { const d = Math.abs(norm(a) - norm(b)); return Math.min(d, 360 - d); };
const signed = (a, b) => { let d = norm(a) - norm(b); if (d > 180) d -= 360; if (d < -180) d += 360; return d; };
export const EYE = { 10: 42.55, 25: 98.8, 36: 140.05 };   // the eye above the street on the registry's floor bands
export const band = (floor) => { const f = Number(floor) || 25; return [10, 25, 36].reduce((b, x) => (Math.abs(x - f) < Math.abs(b - f) ? x : b), 25); };

let PL = null, loading = null;
export function loadPlaces(url) {
  if (PL) return Promise.resolve(PL);
  if (!loading) loading = fetch(url, { credentials: 'omit' }).then((r) => (r.ok ? r.json() : null)).then((d) => (PL = d && Array.isArray(d.places) ? d : null)).catch(() => null);
  return loading;
}
export function pageLang() {
  const L = window.__nlStageI18n; const l = (L && L.lang) || document.documentElement.lang || 'he';
  return String(l).slice(0, 2);
}
/* the name in the page's language: Hebrew pages the Hebrew (OSM's own) name; other pages their language or English */
export function nameOf(p, lang) {
  if (lang === 'he') return p.name;
  const n = p.names || {};
  if (n[lang]) return n[lang];
  if (n.en) return n.en;
  return /[֐-׿]/.test(p.name) ? null : p.name;
}
const isBus = (p) => p.k === 'bus_stop';
/* the places that way (within `half` degrees of the bearing), the named ones, scored: the group's weight, landmarks first,
   the nearer first; `seen` keeps only what the floor band can see */
export function around(bearing, opts) {
  if (!PL) return [];
  const o = opts || {}; const lang = o.lang || pageLang(); const half = o.half == null ? 50 : o.half; const fb = String(band(o.floor));
  const out = [];
  for (const p of PL.places) {
    if (p.generic || (o.noBus && isBus(p))) continue;
    if (angOff(p.bearing, bearing) > half) continue;
    if (o.seen && !(p.sight && p.sight[fb])) continue;
    const nm = nameOf(p, lang); if (!nm) continue;
    const g = GROUPS[p.g]; if (!g) continue;
    // a station first; a name that is only a licence holder's company a little later
    out.push({ p, name: nm, score: g.w + (p.k === 'tram_stop' || p.k === 'station' ? 1.5 : 0) - (p.corp ? 0.6 : 0) - p.dist / 450 });
  }
  return out.sort((a, b) => b.score - a.score);
}

/* ---------------- the view from the floor: labels on the map, the list under it ---------------- */
let css = false;
function ensureCss() {
  if (css) return; css = true;
  const s = document.createElement('style');
  s.id = 'nlal-css';
  s.textContent = '.nlal-pin{display:inline-flex;align-items:center;gap:6px;white-space:nowrap;background:rgba(250,247,241,.95);color:#14212B;font:700 12.5px/1 Assistant,Heebo,Arial,sans-serif;border-radius:999px;padding:4px 10px 4px 4px;box-shadow:0 3px 10px rgba(0,0,0,.24);pointer-events:none;direction:rtl}'
    + '.nlal-pin i{display:grid;place-items:center;width:20px;height:20px;border-radius:50%;color:#fff;flex:none}.nlal-pin i svg{width:13px;height:13px}'
    + '.nlal-pin em{font-style:normal;font-weight:600;color:#6B6558}'
    + '.nlal-pin[dir="ltr"]{direction:ltr;padding:4px 4px 4px 10px}'
    + ':root body .nlds .nlal-groups{display:grid;gap:10px;margin:12px 0 0!important;padding:12px 0 0!important;border-top:1px solid #E2DCD0}'
    + ':root body .nlds .nlal-groups>p{margin:0!important;max-width:none!important;font:600 12.5px/1.4 Assistant,Heebo,sans-serif!important;color:#6B6558!important}'
    + ':root body .nlds .nlal-g{display:grid;grid-template-columns:24px minmax(0,1fr);gap:4px 10px;align-items:start}'
    + ':root body .nlds .nlal-g>i{display:grid;place-items:center;width:24px;height:24px;border-radius:50%;color:#fff;grid-row:span 2}.nlal-g>i svg{width:14px;height:14px}'
    + ':root body .nlds .nlal-g b{font:700 14px/1.3 Assistant,Heebo,sans-serif;color:#14212B}:root body .nlds .nlal-g b span{font-weight:600;color:#8A6A2E;margin-inline-start:6px}'
    + ':root body .nlds .nlal-g ul{display:flex;flex-wrap:wrap;gap:4px 14px;margin:0!important;padding:0!important;list-style:none}'
    + ':root body .nlds .nlal-g li{margin:0!important;font:400 13.5px/1.45 Assistant,Heebo,sans-serif;color:#3B4753}:root body .nlds .nlal-g li em{font-style:normal;color:#8A6A2E;margin-inline-start:4px}'
    + ':root body .nlds .nlal-g li a{color:#1F4B5C!important;text-decoration:underline;text-underline-offset:3px}';
  document.head.appendChild(s);
}
export function pinEl(p, name, lang) {
  ensureCss();
  const g = GROUPS[p.g];
  const el = document.createElement('span');
  el.className = 'nlal-pin nlal-pin--' + p.g;
  if (lang && lang !== 'he' && lang !== 'ar') el.dir = 'ltr';
  const i = document.createElement('i'); i.style.background = g.color; i.innerHTML = ICONS[p.g]; el.append(i);
  const b = document.createElement('b'); b.textContent = name; el.append(b);
  if (p.future) { const e = document.createElement('em'); e.textContent = 'מתוכננת'; el.append(e); }
  else if (p.walk) { const e = document.createElement('em'); e.textContent = p.walk + ' דק׳'; el.append(e); }
  return el;
}
/* the labels in the view: markers for the scored places that way, a few at a time, never on top of each other */
export function viewLayer(gl, map, getView) {
  const pins = new Map(); // id -> { el, mk }
  const lang = pageLang();
  function update() {
    if (!PL || !map) return;
    const v = getView(); // { bearing, floor }
    const W = map.getContainer().clientWidth, H = map.getContainer().clientHeight;
    const max = W < 560 ? 6 : 11;
    const cand = around(v.bearing, { floor: v.floor, seen: true, half: 48, noBus: true, lang });
    const taken = [];
    // the quarter's own labels (bridge.js) are there first: keep clear of them
    for (const q of map.getContainer().querySelectorAll('.nlps-vpin')) {
      if (q.style.visibility === 'hidden') continue;
      const r = q.getBoundingClientRect(), c = map.getContainer().getBoundingClientRect();
      taken.push([r.left - c.left, r.top - c.top, r.width, r.height]);
    }
    const show = new Set();
    for (const c of cand) {
      if (show.size >= max) break;
      let pt; try { pt = map.project([c.p.lng, c.p.lat]); } catch (e) { continue; }
      if (!pt || pt.x < 10 || pt.x > W - 10 || pt.y < 24 || pt.y > H - 8) continue;
      const w = 34 + c.name.length * 6.6 + (c.p.walk ? 34 : 0), h = 28;
      const box = [pt.x - w / 2, pt.y - h, w, h];
      if (box[0] < 4 || box[0] + w > W - 4) continue; // a label is whole in the frame, or it waits for the head to turn
      if (taken.some((t) => box[0] < t[0] + t[2] + 4 && t[0] < box[0] + box[2] + 4 && box[1] < t[1] + t[3] + 2 && t[1] < box[1] + box[3] + 2)) continue;
      taken.push(box); show.add(c.p.id);
      if (!pins.has(c.p.id)) {
        const el = pinEl(c.p, c.name, lang);
        pins.set(c.p.id, { el, mk: new gl.Marker({ element: el, anchor: 'bottom' }).setLngLat([c.p.lng, c.p.lat]).addTo(map) });
      }
    }
    for (const [id, x] of pins) x.el.style.visibility = show.has(id) ? 'visible' : 'hidden';
  }
  return { update };
}
/* under the view: what lies that way, by group: the count and the three nearest by walking minutes */
export function groupsEl(bearing, floor) {
  ensureCss();
  const lang = pageLang();
  const wrap = document.createElement('div'); wrap.className = 'nlal-groups';
  const all = around(bearing, { floor, half: 55, lang });
  let any = false;
  for (const key of Object.keys(GROUPS)) {
    const list = all.filter((c) => c.p.g === key && !(key === 'transport' && isBus(c.p) && all.filter((x) => x.p.g === 'transport').length > 3 && c.p.dist > 500));
    if (!list.length) continue;
    any = true;
    list.sort((a, b) => (a.p.walk || 99) - (b.p.walk || 99));
    const g = GROUPS[key];
    const row = document.createElement('div'); row.className = 'nlal-g';
    const i = document.createElement('i'); i.style.background = g.color; i.innerHTML = ICONS[key]; row.append(i);
    const b = document.createElement('b'); b.textContent = g.he;
    const n = document.createElement('span'); n.textContent = list.length + ' בכיוון הזה'; b.append(n); row.append(b);
    const ul = document.createElement('ul');
    for (const c of list.slice(0, 3)) {
      const li = document.createElement('li');
      // a place with its own findplace page links to it (the owner's sister site)
      if (c.p.fp && lang === 'he') { const a = document.createElement('a'); a.href = c.p.fp; a.target = '_blank'; a.rel = 'noopener'; a.textContent = c.name; li.append(a); }
      else li.textContent = c.name;
      if (c.p.future) { const e = document.createElement('em'); e.textContent = 'מתוכננת'; li.append(e); }
      else if (c.p.walk) { const e = document.createElement('em'); e.textContent = c.p.walk + ' דק׳ הליכה'; li.append(e); }
      ul.append(li);
    }
    row.append(ul); wrap.append(row);
  }
  if (!any) return null;
  const src = document.createElement('p');
  src.textContent = 'מקומות: findplace.co.il (עיריית תל אביב-יפו, מידע פתוח, ו-OpenStreetMap). זמני הליכה לפי מסלול הליכה של Mapbox, מהבניין; מרחק בקו אווירי.';
  wrap.append(src);
  return wrap;
}

/* ---------------- the 360 windows: what a window of the example apartment looks at ---------------- */
const DIR_BEARING = { n: 0, e: 90, s: 180, w: 270 };
/* for a scene { dir, floor }: the named places its window can see, as { at: [yaw, pitch] (degrees, + right / up), label } */
export function looksFor(scene, lang) {
  if (!PL || !scene || DIR_BEARING[scene.dir] == null) return [];
  const centre = DIR_BEARING[scene.dir]; const fb = band(scene.floor); const eye = EYE[fb];
  const cand = around(centre, { floor: fb, seen: true, half: 52, noBus: true, lang: lang || pageLang() });
  const out = [];
  for (const c of cand) {
    const yaw = signed(c.p.bearing, centre);
    const th = c.p.sight[String(fb)] === 'roof' ? 14 : 2;
    const pitch = Math.atan2(th - eye, Math.max(30, c.p.dist)) * 180 / Math.PI;
    if (pitch < -42) continue; // too steep: under the sill
    out.push({ at: [Math.round(yaw * 10) / 10, Math.round(pitch * 10) / 10], g: c.p.g, name: c.name, walk: c.p.future ? null : (c.p.walk || null), future: c.p.future ? 1 : 0, icon: ICONS[c.p.g], color: GROUPS[c.p.g].color, score: c.score });
  }
  return out;
}
