/* ProjectStage bridge (inc/project-stage.php, design system components ProjectStage, BrokerSquare, BrokerSlot).
 *
 * The stage lets the visitor pick a floor and then a direction on that floor. This file shows the view from there
 * (satellite with 3D buildings, the camera at the floor's estimated height, looking that way: the engine's window-view
 * camera, built again here) and turns a beam on the area map next to it. A direction is always said by what lies that
 * way (the project's sectors, measured on the map), never in degrees. The showroom engine (engine.js) is never touched:
 * when it is on the page (#nl-root) this file draws no beam, so a page never has two.
 *
 * Events from the stage: nl:floor {floor, heightM}, nl:facing {floor, heightM, bearing}, nl:floor-cta {floor, bearing}.
 */
const root = document.getElementById('nlps');
const MAPBOX = 'https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl';
const norm = (b) => ((Number(b) % 360) + 360) % 360;
const ga = (name, params) => { try { if (window.nadlanGA) window.nadlanGA(name, params || {}); } catch (e) {} };

/* one copy of Mapbox GL for the whole page: the area map loads the same file; wait for it instead of loading twice */
function loadMapbox() {
  if (window.mapboxgl) return Promise.resolve(window.mapboxgl);
  if (window.__nlMapboxLoading) return window.__nlMapboxLoading;
  window.__nlMapboxLoading = new Promise((resolve, reject) => {
    const done = () => (window.mapboxgl ? resolve(window.mapboxgl) : reject(new Error('mapbox')));
    const existing = document.querySelector('script[src="' + MAPBOX + '.js"]');
    if (existing) { existing.addEventListener('load', done); existing.addEventListener('error', () => reject(new Error('mapbox'))); if (window.mapboxgl) done(); return; }
    if (!document.querySelector('link[href="' + MAPBOX + '.css"]')) {
      const l = document.createElement('link'); l.rel = 'stylesheet'; l.href = MAPBOX + '.css'; document.head.appendChild(l);
    }
    const s = document.createElement('script'); s.src = MAPBOX + '.js'; s.onload = done; s.onerror = () => reject(new Error('mapbox'));
    document.head.appendChild(s);
  });
  return window.__nlMapboxLoading;
}

/* clicks on the rail: the professional's square and the empty square */
document.addEventListener('click', (e) => {
  const a = e.target && e.target.closest ? e.target.closest('[data-nlps-ev]') : null;
  if (!a) return;
  const ev = a.getAttribute('data-nlps-ev');
  if (ev === 'rail') ga(a.hasAttribute('data-nlps-wa') ? 'whatsapp_click' : 'pro_click', { source: 'project-rail', pro: a.getAttribute('data-nlps-pro') });
  else if (ev === 'slot') ga('pro_slot_click', { source: 'project-rail' });
});

/* ApartmentExperience-1 (v101): the docked floor card, the + / − buttons and the wheel hint, for every stage (one place) */
function pickCss() {
  if (document.getElementById('nlps-v101')) return;
  const st = document.createElement('style');
  st.id = 'nlps-v101';
  st.textContent = ''
    + '.rbs-cardhost{--rbs-paper:#F7F6F2;--rbs-ink:#14212B;--rbs-sea:#2F6F86;--rbs-deep:#1F4B5C;--rbs-sand:#EEE9DD;--rbs-line:#E3E1DA;'
    + 'margin:10px 0 0;font-family:Assistant,system-ui,-apple-system,"Segoe UI",Arial,sans-serif;color:var(--rbs-ink)}'
    + '.rbs-cardhost:not(:has(.rbs-label.is-on)){display:none}'
    + ':root body .rbs-cardhost .rbs-label--docked{position:relative;left:auto;top:auto;transform:none!important;width:auto;max-width:none;'
    + 'display:grid;grid-template-columns:repeat(4,minmax(0,1fr));column-gap:8px;row-gap:0;align-items:center;'
    + 'padding:10px 14px 12px;border-radius:14px;box-shadow:0 2px 10px rgba(20,33,43,.07);will-change:auto}'
    // desktop: the floor and its facts on one line, the four actions in one band under it (about 120px, so the card sits
    // inside the first screen under the stage: at 1440x900 the stage ends at ~736px)
    + ':root body .rbs-cardhost .rbs-label--docked>.rbs-label-top{grid-column:1/-1;align-items:center}'
    + ':root body .rbs-cardhost .rbs-label--docked .rbs-label-title{font-size:20px!important;line-height:1.2!important}'
    + ':root body .rbs-cardhost .rbs-label--docked>.rbs-label-line,:root body .rbs-cardhost .rbs-label--docked>.rbs-label-facing,:root body .rbs-cardhost .rbs-label--docked>.rbs-label-more{grid-column:1/-1;margin:2px 0 0!important;font-size:13.5px!important;line-height:1.35!important;max-width:none!important}'
    + ':root body .rbs-cardhost .rbs-label--docked>.rbs-label-line{grid-column:1/3;grid-row:2}:root body .rbs-cardhost .rbs-label--docked>.rbs-label-facing{grid-column:4/5;grid-row:2;text-align:end}:root body .rbs-cardhost .rbs-label--docked>.rbs-label-more{display:none!important}'
    // a project with several towers names the tower on the same line (DUO, Dimri Yama, Ashira)
    + ':root body .rbs-cardhost .rbs-label--docked>.dus-label-kick{grid-column:3/4;grid-row:2;margin:2px 0 0!important;font-size:13.5px!important;line-height:1.35!important;text-align:end}'
    + ':root body .rbs-cardhost .rbs-label--docked>.rbs-label-top{grid-row:1}:root body .rbs-cardhost .rbs-label--docked>.rbs-label-acts{grid-row:3}:root body .rbs-cardhost .rbs-label--docked>.rbs-label-cta{grid-row:3}'
    + ':root body .rbs-cardhost .rbs-label--docked>.rbs-label-acts{grid-column:1/4;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin:10px 0 0}'
    + ':root body .rbs-cardhost .rbs-label--docked .rbs-act{grid-column:auto;min-height:44px;margin:0!important;padding:4px 10px;font-size:14px!important;line-height:1.2!important}'
    + ':root body .rbs-cardhost .rbs-label--docked>.rbs-label-cta{grid-column:4;align-self:end;min-height:44px;margin:10px 0 0!important;padding:6px 12px;line-height:1.2!important}'
    + ':root body .rbs-cardhost .rbs-label--docked.is-min{display:flex;width:auto;max-width:none;padding:8px 14px;cursor:pointer}'
    // v101.1 (Codex QA): the fold and close buttons are 44px targets (the old card measured 22-28px)
    + ':root body .rbs-cardhost .rbs-label--docked .rbs-label-min,:root body .rbs-cardhost .rbs-label--docked .rbs-label-close{width:44px;height:44px;min-width:44px;min-height:44px;margin:-6px 0;display:inline-grid;place-items:center;font-size:20px;line-height:1}'
    // phones: a short block right under the stage (title, one line, three actions in a row, the main button)
    + '@media (max-width:640px){:root body .rbs-cardhost .rbs-label--docked{grid-template-columns:repeat(3,minmax(0,1fr));column-gap:6px;padding:8px 12px 10px}'
    + ':root body .rbs-cardhost .rbs-label--docked .rbs-label-title{font-size:19px!important}'
    + ':root body .rbs-cardhost .rbs-label--docked>.rbs-label-more{display:none!important}'
    + ':root body .rbs-cardhost .rbs-label--docked>.rbs-label-line,:root body .rbs-cardhost .rbs-label--docked>.rbs-label-facing,:root body .rbs-cardhost .rbs-label--docked>.dus-label-kick{grid-column:1/-1;grid-row:auto;text-align:start;font-size:13px!important}'
    + ':root body .rbs-cardhost .rbs-label--docked>.rbs-label-top,:root body .rbs-cardhost .rbs-label--docked>.rbs-label-acts,:root body .rbs-cardhost .rbs-label--docked>.rbs-label-cta{grid-row:auto}'
    + ':root body .rbs-cardhost .rbs-label--docked>.rbs-label-acts{grid-column:1/-1;gap:6px;margin-top:8px}'
    + ':root body .rbs-cardhost .rbs-label--docked .rbs-act{padding:2px 6px;font-size:13px!important}'
    + ':root body .rbs-cardhost .rbs-label--docked>.rbs-label-cta{grid-column:1/-1;margin-top:6px!important;white-space:normal}}'
    + '.rbs-zoom{position:absolute;inset-inline-end:12px;top:50%;transform:translateY(-50%);z-index:4;display:flex;flex-direction:column;gap:6px}'
    + '.rbs-zoom button{width:44px;height:44px;border-radius:12px;border:1px solid rgba(20,33,43,.14);background:rgba(250,247,241,.94);color:#14212B;'
    + 'font:600 22px/1 Assistant,system-ui,sans-serif;cursor:pointer;box-shadow:0 2px 8px rgba(20,33,43,.10);padding:0}'
    + '.rbs-zoom button:hover{background:#fff}.rbs-zoom button:focus-visible{outline:2px solid #2F6F86;outline-offset:2px}'
    + '.rbs-zhint{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);z-index:5;padding:10px 16px;border-radius:12px;background:rgba(20,33,43,.82);'
    + 'color:#fff;font:600 15px/1.3 Assistant,system-ui,sans-serif;white-space:nowrap;opacity:0;transition:opacity .2s;pointer-events:none}'
    + '.rbs-zhint.is-on{opacity:1}'
    // the stage's own stylesheet loads after this one and gives its UI layer's children pointer events: the hint must never take
    // the wheel (it sat over the model's centre and swallowed Ctrl + wheel)
    + '.rbs .rbs-ui .rbs-zhint{pointer-events:none!important}.rbs .rbs-ui .rbs-zoom{pointer-events:auto}'
    + '@media (hover:none){.rbs-zhint{display:none}}'
    // ApartmentMapLanding (v101.2): the unit line over the real map, then the map, then its controls
    + ':root body .nlps-mapsum{display:grid;grid-template-columns:22px minmax(0,1fr) auto;column-gap:10px;row-gap:2px;align-items:center;margin:0 0 10px;'
    + 'padding:8px 10px 8px 12px;background:#F7F2E8;border:1px solid #E2DCD0;border-radius:12px;font-family:Heebo,Assistant,system-ui,sans-serif;color:#14212B}'
    + '.nlps-mapsum[hidden]{display:none!important}'
    + ':root body .nlps-mapsum>i{grid-column:1;grid-row:1/3;line-height:0;align-self:center}'
    + ':root body .nlps-mapsum>.nlps-mapsum-t{grid-column:2;grid-row:1;font:700 15px/1.35 Heebo,system-ui,sans-serif!important;color:#14212B!important}'
    + ':root body .nlps-mapsum em{display:inline-block;margin-inline-start:8px;padding:3px 7px;border-radius:6px;background:#EDE5D6;color:#6B6558;'
    + 'font:600 11.5px/1 Heebo,system-ui,sans-serif;font-style:normal;white-space:nowrap;vertical-align:2px}'
    + ':root body .nlps-mapsum>small{grid-column:2;grid-row:2;display:block;font:500 12.5px/1.4 Heebo,system-ui,sans-serif!important;color:#6B6558!important}'
    + ':root body .nlps-mapsum>button{grid-column:3;grid-row:1/3;min-height:44px;padding:0 16px;border-radius:999px;border:1px solid #CFC7B8;background:#fff;'
    + 'color:#1F4B5C;font:700 13.5px/1 Heebo,system-ui,sans-serif;white-space:nowrap;cursor:pointer}'
    + ':root body .nlps-mapsum>button:hover{background:#FBF8F2}:root body .nlps-mapsum>button:focus-visible{outline:2px solid #2F6F86;outline-offset:2px}'
    // phones: the stage's notice under the open card (the lifted pill sat on it at the stage's foot)
    + '.nlps-pick-cap{display:none}'
    + '@media (max-width:640px){:root body .rbs-cardhost>.nlps-pick-cap{display:block;margin:6px 4px 0!important;font:400 11.5px/1.45 Heebo,Assistant,system-ui,sans-serif!important;color:#6B6558!important;max-width:none!important}'
    + 'body:has(#nlps-pick .rbs-label.is-on) #nlps .rbs-caption{display:none!important}}'
    // the controls now follow the map: a breath between the canvas and the first row
    + ':root body #nlpjx-map>#nlpjx-unimap+.nlam-bar,:root body #nlpjx-map>#nlpjx-unimap+.nlam-range,:root body #nlpjx-map>#nlpjx-unimap+.nlpjx-maplayers{margin-top:12px}'
    + '#nlps-pick .rbs-label[tabindex]:focus{outline:none}#nlps-pick .rbs-label[tabindex]:focus-visible{outline:2px solid #2F6F86;outline-offset:2px}'
    // phones: the floor and direction take the whole first line; the legend and the button share the second
    + '@media (max-width:480px){:root body .nlps-mapsum{grid-template-columns:18px minmax(0,1fr) auto;row-gap:6px;padding:8px 8px 8px 10px}'
    + ':root body .nlps-mapsum>i{grid-row:1}:root body .nlps-mapsum>.nlps-mapsum-t{grid-column:2/4}'
    + ':root body .nlps-mapsum>small{grid-column:1/3;grid-row:2}:root body .nlps-mapsum>button{grid-row:2;padding:0 14px}}'
    + '@media (prefers-reduced-motion:reduce){.rbs-zhint{transition:none}}';
  document.head.appendChild(st);
}

if (root) boot();

async function boot() {
  let cfg = {};
  try { cfg = JSON.parse(root.dataset.cfg || '{}'); } catch (e) { return; }
  const sectors = Array.isArray(cfg.sectors) ? cfg.sectors : [];
  /* what lies that way: the sector the bearing falls in (a sector may wrap past north) */
  const facingWords = (b) => {
    const x = norm(b);
    for (const s of sectors) {
      const from = norm(s[0]), to = norm(s[1]);
      if (from <= to ? (x >= from && x < to) : (x >= from || x < to)) return String(s[2]);
    }
    return '';
  };
  const stageEl = document.getElementById('nlps-stage');
  /* the floor card's sourced line: a sold apartment reported on that floor, else what the developer said about that height */
  const notes = cfg.notes && typeof cfg.notes === 'object' ? cfg.notes : {};
  const floorNote = (f) => notes[String(f)] || (cfg.lowNote && f <= Number(cfg.lowUpTo || 0) ? cfg.lowNote : (cfg.highNote || null));
  /* example apartments (the owner, 25.9.2026: "דירות לדוגמה עם כיוון, ועם תווית ברורה שהן לדוגמה"): one per side of the floor */
  // the sea-side apartment (west) answers first: the side buyers ask about most; else the first side of the list
  const seaSide = Array.isArray(cfg.units) && cfg.units.length ? String((cfg.units.find((u) => String(u[0]) === 'w') || cfg.units[0])[0]) : 'w';
  const units = Array.isArray(cfg.units) && cfg.units.length
    ? { sides: cfg.units.map((u) => ({ id: String(u[0]), bearing: Number(u[1]) })), half: 180 / cfg.units.length, label: 'דירה לדוגמה', chip: 'לדוגמה' }
    : null;
  // ApartmentExperience-1 (design system v101, 29.9.2026): the floor card's place in the page, right under the stage and above
  // the steps: the building stays whole and in place, and the page scrolls on past it to the view and the map
  const pickHost = document.createElement('div');
  pickHost.className = 'rbs-cardhost';
  pickHost.id = 'nlps-pick';
  root.insertAdjacentElement('afterend', pickHost);
  pickCss();
  try {
    const mod = await import(cfg.stage);
    window.__nlpsStage = mod[cfg.mount](stageEl, {
      cardHost: pickHost,
      preset: 'sunset',
      poster: cfg.poster || null, // versioned, so a new poster is never hidden behind a cached one
      bearingOffset: Number(cfg.bearingOffset) || 0,
      facingWords: sectors.length ? facingWords : null,
      floorNote,
      units,
      quarter: cfg.quarter && typeof cfg.quarter === 'object' ? cfg.quarter : null,
      // the project's facilities on the model (design system FacilityHotspots v72) and the site's WhatsApp for their cards
      facilities: Array.isArray(cfg.facilities) && cfg.facilities.length ? cfg.facilities : null,
      wa: String(cfg.wa || ''),
      // one tap, the whole answer (design system ProjectStage version 33): the floor's sea-side example apartment at once,
      // and the card's actions: inside the apartment, the view and the map under the stage, the designer
      autoFacing: units ? seaSide : null,
      actions: units ? [
        { id: 'inside', label: 'להיכנס לדירה · 360°', kind: 'go' },
        { id: 'view', label: 'הנוף והמפה', kind: 'sec' },
        { id: 'design', label: 'לעצב את הדירה', kind: 'sec' },
      ] : null,
      text: units
        ? { cta: 'לקבלת תוכניות ומחירים', more: 'לצד אחר: הקישו על הטבעת', facingHint: 'בחרו דירה לדוגמה בטבעת הקומה', caption: 'הדמיה להמחשה בלבד, על בסיס מקורות פומביים. חלוקת הקומה לדירות היא לדוגמה, ואינה לפי תוכנית מכר.' }
        : { cta: 'לקבלת תוכניות ומחירים' },
      force3D: /[?&]nlps3d\b/.test(location.search), // QA only: the scene even on a software renderer
    });
  } catch (e) {
    console.warn('[project stage]', e);
    return; // the stage module shows its own poster; the page and its map stay as they are
  }
  // ApartmentMapLanding (v101.2): on phones, while the card is open, the stage's notice sits at the card's foot (next to the
  // picked unit), where the lifted pill never goes; the stage keeps it whenever the card is closed. The stage's own words.
  const stageCap = root.querySelector('.rbs-caption');
  if (stageCap && stageCap.textContent.trim()) {
    const pc = document.createElement('p');
    pc.className = 'nlps-pick-cap';
    pc.textContent = stageCap.textContent.trim();
    pickHost.appendChild(pc);
  }
  const title = document.getElementById('nlps-view-t');
  const cap = document.getElementById('nlps-view-cap');
  const cta = document.getElementById('nlps-view-cta');
  const empty = document.getElementById('nlps-view-empty');
  const hint = document.getElementById('nlps-hint');
  const wa = document.getElementById('nlps-wa');
  const kicker = document.getElementById('nlps-view-k');
  const hasGeo = Number(cfg.lat) && Number(cfg.lng) && cfg.token;
  let last = null;
  const win = { map: null, bearing: 270, vert: 0, alt: 10 };
  /* the shared viewing room (inc/together.php, design system TogetherRoom v77): the view from the floor read and set from
     outside ({ bearing, vert } in degrees), and a throttled nl:view while the visitor turns it himself */
  let viewAt = 0, viewT = 0;
  const winView = () => ({ mode: 'view', bearing: Math.round(norm(win.bearing) * 10) / 10, vert: Math.round(win.vert * 10) / 10 });
  const sendWinView = () => { viewT = 0; viewAt = performance.now(); window.dispatchEvent(new CustomEvent('nl:view', { detail: Object.assign(winView(), { source: 'user' }) })); };
  window.__nlpsView = {
    getView: () => (win.map ? winView() : null),
    setView: (v) => {
      if (!v || !win.map) return false;
      if (Number.isFinite(Number(v.bearing))) win.bearing = norm(Number(v.bearing));
      if (Number.isFinite(Number(v.vert))) win.vert = Math.max(-45, Math.min(10, Number(v.vert)));
      winCam();
      return true;
    },
  };

  /* what lies that way (design system ProjectStage version 35): the quarter's places and projects, each with its distance
     and bearing from the tower (quarter.json); labels in the view and a list under it, only what the file holds */
  const Q = cfg.quarter && typeof cfg.quarter === 'object' ? cfg.quarter : null;
  const QITEMS = Q ? [...(Q.places || []), ...(Q.projects || [])].filter((it) => it && it.name && Number.isFinite(Number(it.dist)) && Number.isFinite(Number(it.bearing))) : [];
  const QCOL = { beach: '#C9A96E', park: '#517048', nature: '#517048', school: '#9C7A3C', rail: '#2F6F86', building: '#2F6F86', selling: '#9C7A3C', permit: '#8E8676' };
  const qColor = (it) => QCOL[it.kind === 'project' ? it.phase : it.kind] || '#57534B';
  const angOff = (a, b) => { const d = Math.abs(norm(a) - norm(b)); return Math.min(d, 360 - d); };
  const HALF = 55;
  const fmtDist = (m) => (m < 1000 ? Math.round(m / 10) * 10 + ' מ׳' : (Math.round(m / 100) / 10) + ' ק״מ');
  const nearEl = document.getElementById('nlps-near');
  /* AreaLife v97: the place registry (places.json beside the stage) and its module, loaded when the view first opens */
  const AL_URL = cfg.places && cfg.stage ? (() => { const u = new URL(cfg.stage, location.href); return new URL('./places.json', u).href.split('?')[0] + u.search; })() : null;
  let AL = null, alLayer = null, nearTok = 0;
  const alMod = () => (AL ? Promise.resolve(AL) : import(new URL('./arealife.js' + new URL(import.meta.url).search, import.meta.url).href).then((m) => (AL = m)));
  const alReady = () => (AL_URL ? alMod().then((m) => m.loadPlaces(AL_URL).then((d) => (d ? m : null))).catch(() => null) : Promise.resolve(null));
  function showNear(bearing) {
    if (!nearEl || !QITEMS.length) return;
    const tok = ++nearTok;
    const list = QITEMS.filter((it) => angOff(it.bearing, bearing) <= HALF).sort((a, b) => a.dist - b.dist);
    nearEl.textContent = '';
    const h = document.createElement('p'); h.className = 'nlps-near__h'; h.textContent = 'מה יש לכיוון הזה'; nearEl.append(h);
    if (!list.length) {
      const e = document.createElement('p'); e.className = 'nlps-near__src'; e.textContent = 'אין בכיוון הזה מקומות מסומנים בקובץ הרובע.'; nearEl.append(e);
    } else {
      const ul = document.createElement('ul'); ul.className = 'nlps-near__list';
      for (const it of list) {
        const li = document.createElement('li');
        const dot = document.createElement('i'); dot.className = 'nlps-near__dot'; dot.style.setProperty('background', qColor(it), 'important'); li.append(dot);
        const nm = document.createElement('span'); nm.className = 'nlps-near__name';
        if (it.kind === 'project' && it.url) { const a = document.createElement('a'); a.href = it.url; a.textContent = it.name; nm.append(a); } else nm.textContent = it.name;
        li.append(nm);
        const d = document.createElement('span'); d.className = 'nlps-near__d'; d.textContent = fmtDist(Number(it.dist)); li.append(d);
        const extra = [];
        if (it.kind !== 'project' && it.walk) extra.push('כ־' + it.walk + ' דק׳ הליכה');
        if (it.status && it.status !== 'קיים') extra.push(String(it.status));
        if (extra.length) { const x = document.createElement('span'); x.textContent = extra.join(' · '); li.append(x); }
        ul.append(li);
      }
      nearEl.append(ul);
    }
    const src = document.createElement('p'); src.className = 'nlps-near__src';
    src.textContent = 'מרחק בקו אווירי מהבניין, לפי המפה; זמן ההליכה משוער. מקור: נתוני עיריית תל אביב-יפו ו-OpenStreetMap, 8.2026; הפרויקטים לפי העמודים שלהם באתר.';
    nearEl.append(src);
    nearEl.hidden = false;
    // AreaLife v97: everything else that way, by group, from the registry (a later turn of the head wins)
    alReady().then((m) => {
      if (!m || tok !== nearTok) return;
      const el = m.groupsEl(bearing, last && last.floor);
      if (el) nearEl.append(el);
    });
  }
  const vpins = [];
  function addViewPins(gl, map) {
    if (vpins.length || !QITEMS.length) return;
    const lat0 = Number(cfg.lat), lng0 = Number(cfg.lng);
    for (const it of QITEMS) {
      const r = norm(it.bearing) * Math.PI / 180, dm = Number(it.dist);
      const lat = lat0 + (dm * Math.cos(r)) / 111320;
      const lng = lng0 + (dm * Math.sin(r)) / (111320 * Math.cos(lat0 * Math.PI / 180));
      const el = document.createElement('span');
      el.className = 'nlps-vpin' + (it.kind === 'project' ? ' nlps-vpin--project' : '');
      const dot = document.createElement('i'); dot.style.background = qColor(it); el.append(dot);
      el.append((it.pin || it.name) + ' · ' + fmtDist(dm));
      const mk = new gl.Marker({ element: el, anchor: 'bottom' }).setLngLat([lng, lat]).addTo(map);
      vpins.push({ it, el, mk });
    }
    placeViewPins();
  }
  function placeViewPins() {
    const map = win.map;
    const W = map ? map.getContainer().clientWidth : 0;
    for (const p of vpins) {
      let on = angOff(p.it.bearing, win.bearing) <= HALF - 10;
      // near the edge of the view the label slides inward (its place is still in view); a place outside the view waits
      // until the head turns to it
      let dx = 0;
      if (on && map && W) {
        try {
          const pt = map.project(p.mk.getLngLat()); const w = p.el.offsetWidth || 120;
          if (pt.x < 4 || pt.x > W - 4) on = false;
          else if (pt.x - w / 2 < 6) dx = 6 - (pt.x - w / 2);
          else if (pt.x + w / 2 > W - 6) dx = (W - 6) - (pt.x + w / 2);
        } catch (e) { /* keep it */ }
      }
      p.mk.setOffset([Math.round(dx), 0]);
      p.el.style.visibility = on ? 'visible' : 'hidden';
    }
    if (alLayer) alLayer.update();
  }

  const waUrl = (d) => {
    if (!cfg.wa || !d || d.floor == null) return '';
    const words = d.toward ? 'לכיוון ' + d.toward : (d.bearing != null ? facingWords(d.bearing) : '');
    // on a language page, the message in the page's language (i18n-dom.js, HAD-361)
    const L = window.__nlStageI18n;
    const text = (L && typeof L.wa === 'function' && L.wa(d.unit ? 'unit' : 'floor', { floor: d.floor, project: cfg.name, words })) ||
      'שלום, אשמח לקבל תוכניות ומחירים ' + (d.unit ? 'לדירה בקומה ' : 'לקומה ') + d.floor + ' ב' + cfg.name + (words ? ', ' + words : '') + ' (nad-lan.co.il)';
    return 'https://wa.me/' + cfg.wa + '?text=' + encodeURIComponent(text);
  };
  const setTitle = (d) => {
    if (!title) return;
    title.textContent = 'קומה ' + d.floor;
    // toward a pin in the quarter: the pin's name ("לכיוון דמרי ימה"); otherwise what lies that way
    const words = d.toward ? 'לכיוון ' + d.toward : (d.bearing != null ? facingWords(d.bearing) : '');
    if (words) {
      title.append(' · ');
      const s = document.createElement('span'); s.className = 'nlps-dir'; s.textContent = words; title.append(s);
    }
    // an example apartment says so, here too
    if (d.unit) {
      const c = document.createElement('span'); c.className = 'nlds-sample'; c.textContent = 'דירה לדוגמה'; title.append(' ', c);
    }
    if (kicker) kicker.textContent = d.unit ? 'הנוף מהדירה לדוגמה' : 'הנוף מהקומה';
  };
  /* the address keeps an example apartment, so a link opens the same one */
  const keepUnit = (id) => {
    try {
      const u = new URL(location.href);
      if (id) u.searchParams.set('unit', id); else u.searchParams.delete('unit');
      history.replaceState(history.state, '', u.pathname + (u.search ? u.search : '') + u.hash);
    } catch (e) {}
  };

  window.addEventListener('nl:floor', (e) => {
    const d = e.detail || {};
    if (d.floor == null) return;
    ga('stage_floor', { floor: d.floor, project: cfg.name });
    if (wa) wa.href = waUrl(d);
    if (!last || last.floor !== d.floor) {
      setTitle({ floor: d.floor });
      if (empty && !win.map) empty.textContent = units ? 'עכשיו בחרו דירה לדוגמה בטבעת הקומה, והנוף ממנה יופיע כאן.' : 'עכשיו בחרו נקודה בטבעת הקומה, והנוף לכיוון הזה יופיע כאן.';
    }
    if (cta) cta.hidden = false;
  });

  window.addEventListener('nl:facing', (e) => {
    const d = e.detail || {};
    if (d.floor == null || d.bearing == null) return;
    last = d;
    // ConsultSheet (v101): the site pill's message offers this floor and direction (inc/cta-sheet.php reads it; nothing is sent)
    window.__nlpsPick = { floor: d.floor, facing: facingWords(d.bearing), unit: d.unit || '', example: !!units, name: String(cfg.name || '') };
    ga('stage_facing', { floor: d.floor, facing: facingWords(d.bearing), project: cfg.name, unit: d.unit || '', toward: d.toward || '' });
    if (hint) hint.hidden = true;
    setTitle(d);
    keepUnit(d.unit || '');
    const h = Math.max(10, Math.round(Number(d.heightM) || 0));
    if (cap) { cap.textContent = 'הדמיה להמחשה בלבד: מבט משוער מגובה של כ־' + h + ' מ׳, לפי מפה. אינו צילום מהדירה.'; cap.hidden = false; }
    if (wa) wa.href = waUrl(d);
    if (cta) cta.hidden = false;
    showNear(d.bearing);
    if (hasGeo) {
      showView(d).catch(() => {});
      showBeam(d.bearing).catch(() => {});
    }
  });

  window.addEventListener('nl:quarter', (e) => {
    const d = e.detail || {};
    ga('quarter_pin', { kind: d.kind || '', name: d.name || '', project: cfg.name });
  });

  window.addEventListener('nl:floor-cta', (e) => {
    const d = Object.assign({}, last || {}, e.detail || {});
    if (d.floor == null) return;
    const url = waUrl(d);
    ga('whatsapp_click', { source: 'project-stage', floor: d.floor });
    if (url) window.open(url, '_blank', 'noopener');
  });
  if (wa) wa.addEventListener('click', () => ga('whatsapp_click', { source: 'project-stage-view', floor: last ? last.floor : null }));

  /* ?unit=16-w opens that example apartment once the stage is ready (as a tap would: the view and the map follow) */
  const stage = window.__nlpsStage;
  const wanted = (() => { try { return new URL(location.href).searchParams.get('unit') || ''; } catch (e) { return ''; } })();
  if (wanted && units && stage && stage.ready) {
    Promise.resolve(stage.ready).then(() => { stage.selectUnit(wanted, 'user'); }).catch(() => {});
  }
  /* the example apartment from the inside (design system ApartmentTour): the viewer loads on demand. The pictures exist
     for some floors (10, 25, 36): the viewer takes the floor nearest the pick and says which one it is */
  const tourBtn = document.querySelector('[data-nlps-tour]');
  let allScenes = [];
  try { allScenes = JSON.parse((tourBtn && tourBtn.getAttribute('data-nlps-tour-scenes')) || '[]') || []; } catch (err) { allScenes = []; }
  /* FloorSlice v87: the picked floor as a plan (slice.js, loaded on demand), next to the view's buttons, on a stage that can
     draw it (stage.floorPlan) and has example apartments */
  if (cta && stage && typeof stage.floorPlan === 'function' && units) {
    const sl = document.createElement('button');
    sl.type = 'button';
    sl.className = 'nlds-btn nlds-btn--secondary nlps-slice';
    const sp = document.createElement('span'); sp.textContent = 'חתך הקומה'; sl.appendChild(sp);
    cta.appendChild(sl);
    const tourFloors = [...new Set(allScenes.map((x) => Number(x.floor)).filter(Boolean))];
    sl.addEventListener('click', () => {
      const sel = stage.getSelection ? stage.getSelection() : null;
      const f = (sel && sel.floor) || (last && last.floor) || 25;
      const u = sel && sel.unit ? String(sel.unit).split('-').pop() : null; // "25-w", or "N-25-w" on a two-tower stage
      const tw = sel && sel.tower ? String(sel.tower) : null;
      ga('floor_slice', { floor: f, project: cfg.name });
      import(new URL('./slice.js' + new URL(import.meta.url).search, import.meta.url).href).then((m) => m.openSlice({
        stage, floor: f, unit: u, tower: tw, units: cfg.units, words: facingWords, note: cfg.sliceNote || '', tourFloors, opener: sl,
      })).catch((err) => console.warn('[project stage] slice', err));
    });
  }
  const tourFloors = [...new Set(allScenes.map((x) => Number(x.floor) || 25))].sort((a, b) => a - b);
  const nearestFloor = (f) => (tourFloors.length ? tourFloors.reduce((b, x) => (Math.abs(x - f) < Math.abs(b - f) ? x : b), tourFloors[0]) : 25);
  /* BuildingWalk v96 (design system): one viewer for the whole building when the project's folder has a walk
     (facilities.json 'walk'): the apartment's floors (ids unique per floor), the facilities' 360 rooms with their doors,
     and a where-to list at the lift doors. The apartment's button and each facility's 360 button open it at their own
     room. Every connection is illustrative (Codex consult 28.9), and the viewer says so. */
  const walk = cfg.walk && typeof cfg.walk === 'object' && Array.isArray(cfg.facilities) ? cfg.walk : null;
  const FAC_CAP = 'הדמיה להמחשה בלבד: המיקום, החלוקה והריהוט משוערים ואינם לפי תוכנית היזם.';
  const tourFile = (f) => { const u = new URL(cfg.stage, location.href); return new URL('./tour/' + f, u).href.split('?')[0] + u.search; };
  function walkOpts(startId) {
    const scenes = [];
    const door = walk.aptDoor || {};
    for (const x of allScenes) {
      const fl = Number(x.floor) || 25;
      const sc = Object.assign({}, x, { id: fl + '-' + x.id, floor: fl, group: 'apt' });
      if (x.spot === 'living' && Array.isArray(door[x.dir])) sc.doors = [{ to: 'lift', at: door[x.dir], label: walk.aptDoorLabel || 'יציאה מהדירה', sub: walk.aptDoorSub || '' }];
      scenes.push(sc);
    }
    const facs = cfg.facilities.filter((f) => f && f.tour && f.tour.src);
    for (const f of facs) {
      scenes.push({ id: 'fac-' + f.id, group: 'fac', dir: 'fac-' + f.id, spot: 'fac', title: f.tour.title || f.name, src: tourFile(f.tour.src),
        small: tourFile(f.tour.small || f.tour.src), chip: 'מתקן לדוגמה', caption: FAC_CAP, note: f.note || '',
        doors: (Array.isArray(f.tour.doors) ? f.tour.doors : []).map((d) => Object.assign({}, d, { to: d.to === 'lift' || /^\d+-/.test(d.to) ? d.to : 'fac-' + d.to })) });
    }
    const order = Array.isArray(walk.order) ? walk.order : facs.map((f) => f.id);
    const places = [{ apt: true, label: walk.aptLabel || 'הדירה', floor: 25, dir: 'w' }]; // the buyer's apartment first
    for (const id of order) { const f = facs.find((x) => x.id === id); if (f) places.push({ to: 'fac-' + id, label: f.tour.place || f.pin || f.name, sub: f.tour.stopSub || '' }); }
    // the apartments' stops: the project's own list when it has one (DUO: a tower each), else a floor each
    const aptStops = Array.isArray(walk.aptStops) && walk.aptStops.length
      ? walk.aptStops.filter((q) => q && q.to && scenes.some((sc) => sc.id === q.to)).map((q) => ({ to: q.to, label: q.label || '', sub: q.sub || '' }))
      : tourFloors.slice().sort((a, b) => b - a).map((fl) => ({ floor: fl, label: 'קומה ' + fl, sub: walk.aptStopSub || 'דירה לדוגמה' }));
    const stops = aptStops.concat(places.filter((q) => !q.apt).map((q) => ({ to: q.to, label: q.label, sub: q.sub })));
    return { scenes, start: startId, places, placesLabel: walk.placesLabel || 'בבניין', routeNote: walk.routeNote || '',
      lift: { title: walk.liftTitle || 'לאן?', note: walk.liftNote || 'מעבר להמחשה', stops },
      caption: 'הדמיית פנים להמחשה בלבד: החלוקה, הגמרים והנוף משוערים ואינם לפי תוכנית מכר.',
      onScene: (id) => ga('tour_room', { room: id, project: cfg.name }) };
  }
  async function openWalk(startId, opener) {
    const o = walkOpts(startId);
    // AreaLife v97: the named places each apartment window looks at (a sight line over the city's buildings layer)
    const al = await alReady();
    if (al) {
      for (const sc of o.scenes) if (sc.group === 'apt' && sc.spot === 'living') sc.looks = al.looksFor(sc);
      o.looksNote = 'השמות בחלון: findplace ו-OpenStreetMap, בכיוון ובמרחק האמיתיים מהבניין; מה שבניין מסתיר לא מסומן.';
    }
    import(new URL('./tour.js' + new URL(import.meta.url).search, import.meta.url).href).then((m) => m.openTour(Object.assign(o, { opener: opener || null })))
      .catch((err) => console.warn('[project stage] walk', err));
  }
  function openTourAt(floor, side, opener) {
    if (!tourBtn) return;
    const fl = nearestFloor(Number(floor) || 25);
    if (walk) {
      const sd = side && allScenes.some((x) => (Number(x.floor) || 25) === fl && x.id === side) ? side : 'w';
      ga('tour_open', { room: 'living-' + fl + sd, project: cfg.name });
      openWalk(fl + '-' + sd, opener || tourBtn);
      return;
    }
    const scenes = allScenes.filter((x) => (Number(x.floor) || 25) === fl);
    const start = side && scenes.some((x) => x.id === side) ? side : 'w';
    const first = scenes.find((x) => x.id === start) || scenes[0] || null;
    ga('tour_open', { room: 'living-' + fl + start, project: cfg.name });
    // the viewer keeps this module's version (?ver=), so a new release never meets an old cached viewer
    import(new URL('./tour.js' + new URL(import.meta.url).search, import.meta.url).href).then((m) => m.openTour({
      src: first ? first.src : tourBtn.getAttribute('data-nlps-tour'),
      srcSmall: first ? first.small : tourBtn.getAttribute('data-nlps-tour-small'),
      title: first ? first.title : (tourBtn.getAttribute('data-nlps-tour-title') || ''),
      scenes: scenes.length ? scenes : null,
      start,
      onScene: (id) => ga('tour_direction', { side: id, project: cfg.name, floor: fl }),
      opener: opener || tourBtn,
      caption: 'הדמיית פנים להמחשה בלבד: החלוקה, הגמרים והנוף משוערים ואינם לפי תוכנית מכר.',
    })).catch((err) => console.warn('[project stage] tour', err));
  }
  /* FacilityRooms v83: a facility card's "כניסה ב־360°" (the stage sends nl:facility-tour) opens the same viewer */
  window.addEventListener('nl:facility-tour', (e) => {
    const d = e.detail || {};
    if (!d.src) return;
    ga('facility_tour', { facility: String(d.id || ''), project: cfg.name });
    if (walk && cfg.facilities.some((f) => f && f.id === d.id && f.tour && f.tour.src)) { openWalk('fac-' + d.id, d.opener || null); return; }
    import(new URL('./tour.js' + new URL(import.meta.url).search, import.meta.url).href).then((m) => m.openTour({
      src: d.src, srcSmall: d.small || d.src, title: d.title || '', chip: 'מתקן לדוגמה', opener: d.opener || null,
      caption: 'הדמיה להמחשה בלבד: המיקום, החלוקה והריהוט משוערים ואינם לפי תוכנית היזם.' + (d.note ? ' ' + d.note : ''),
    })).catch((err) => console.warn('[project stage] facility tour', err));
  });
  const selSide = () => { try { const sel = stage && stage.getSelection && stage.getSelection(); return sel && sel.unit ? String(sel.unit).split('-').pop() : null; } catch (err) { return null; } };
  const selFloor = () => { try { const sel = stage && stage.getSelection && stage.getSelection(); return sel ? sel.floor : null; } catch (err) { return null; } };
  document.addEventListener('click', (e) => {
    const b = e.target && e.target.closest ? e.target.closest('[data-nlps-tour]') : null;
    if (!b) return;
    // the section's button: the side and the floor picked on the stage, else floor 25 toward the sea
    openTourAt(selFloor() || 25, selSide() || 'w', b);
  });

  /* the view and the map, right under the stage */
  const below = document.querySelector('.nlps-below');
  const smooth = () => (matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth');
  /* ApartmentMapLanding (design system v101.2, Codex's integrated QA 29.9): on a stage page the map section reads unit line →
     the real map → its controls → the list, and "הנוף והמפה" lands where the whole original cone is in view, clear of the
     wide pill and the accessibility button. The map, the cone (showBeam) and the engine are not touched: only the controls
     move, under the map host, so the WebGL canvas never leaves the page. */
  const mapSec = document.getElementById('nlpjx-map');
  const mapHost = mapSec && (mapSec.querySelector(':scope > #nlpjx-unimap') || mapSec.querySelector(':scope > #nlpjx-leaflet'));
  let mapSum = null;
  if (mapSec && mapHost) {
    mapSum = document.createElement('div');
    mapSum.className = 'nlps-mapsum';
    mapSum.hidden = true;
    mapSum.innerHTML = '<i aria-hidden="true"><svg viewBox="0 0 62 74" width="18" height="22"><path d="M31 74 L0 7 A78 78 0 0 1 62 7 Z" fill="#C2563A" fill-opacity=".38" stroke="#C2563A" stroke-opacity=".7"/></svg></i>'
      + '<b class="nlps-mapsum-t"></b><small>האלומה במפה: הכיוון מהדירה</small>'
      + '<button type="button" data-nlps-back>חזרה לבניין <span aria-hidden="true">↑</span></button>';
    // the same order every time the map's own script adds its bars (idempotent: nothing moves when all is in place)
    const arrange = () => {
      if (mapSum.nextElementSibling !== mapHost) mapHost.before(mapSum);
      let ref = mapHost;
      ['.nlam-bar', '.nlam-range', '.nlpjx-maplayers'].forEach((q) => {
        const el = mapSec.querySelector(':scope > ' + q);
        if (!el) return;
        if (ref.nextElementSibling !== el) ref.after(el);
        ref = el;
      });
    };
    arrange();
    new MutationObserver(arrange).observe(mapSec, { childList: true });
  }
  // the unit line: the card's own floor and direction, the example tag, updated with every pick
  const setMapSum = (d) => {
    if (!mapSum || !d || d.floor == null) return;
    const words = d.toward ? 'לכיוון ' + d.toward : (d.bearing != null ? facingWords(d.bearing) : '');
    const t = mapSum.querySelector('.nlps-mapsum-t');
    t.textContent = 'קומה ' + d.floor + (words ? ' · ' + words : '');
    if (units) { const em = document.createElement('em'); em.textContent = 'דירה לדוגמה'; t.appendChild(em); }
    mapSum.hidden = false;
  };
  window.addEventListener('nl:facing', (e) => setMapSum(e.detail || {}));
  if (last) setMapSum(last);
  // the sticky header's bottom and the top of the fixed controls at the foot of the screen (the pill at rest, the accessibility
  // button), both measured at the moment of the press
  const headBottom = () => {
    let el = document.elementFromPoint(Math.round(innerWidth / 2), 2);
    while (el && el !== document.body) {
      const p = getComputedStyle(el).position;
      if (p === 'fixed' || p === 'sticky') return Math.max(0, el.getBoundingClientRect().bottom);
      el = el.parentElement;
    }
    return 0;
  };
  const shown = (el) => !!el && el.getClientRects().length > 0 && getComputedStyle(el).visibility !== 'hidden'; // fixed elements have no offsetParent
  const footTop = () => {
    let t = innerHeight;
    const box = document.getElementById('nlcta');
    if (shown(box)) {
      const rest = Number(box.getAttribute('data-rest')); // set by inc/conversion-cta.php: the pill's top, from the screen's foot, at rest
      t = Math.min(t, rest > 0 ? innerHeight - rest : box.getBoundingClientRect().top);
    }
    const a11y = document.getElementById('nla11y');
    if (shown(a11y)) t = Math.min(t, a11y.getBoundingClientRect().top);
    return t - 8;
  };
  const toBelow = () => {
    if (!below) return;
    let top = below.getBoundingClientRect().top + window.scrollY - 84; // under the sticky header: the view and the map from their top
    if (mapHost) {
      // the whole map must sit between the header and the controls at the foot; when it does not (phones), the unit line goes
      // right under the header and the real map follows it
      const head = headBottom(), foot = footTop();
      const c = mapHost.getBoundingClientRect(), cTop = c.top + window.scrollY - top, cBot = c.bottom + window.scrollY - top;
      if (cTop < head + 4 || cBot > foot) top = (mapSum && !mapSum.hidden ? mapSum : mapHost).getBoundingClientRect().top + window.scrollY - head - 8;
    }
    window.scrollTo({ top, behavior: smooth() });
  };
  // back to the building: the stage under the header, the same unit still in the card, the focus on the card
  document.addEventListener('click', (e) => {
    const b = e.target && e.target.closest ? e.target.closest('[data-nlps-back]') : null;
    if (!b) return;
    ga('map_back', { project: cfg.name, unit: (window.__nlpsPick && window.__nlpsPick.unit) || '' });
    const lab = document.querySelector('#nlps-pick .rbs-label.is-on');
    if (lab) { if (!lab.hasAttribute('tabindex')) lab.setAttribute('tabindex', '-1'); lab.focus({ preventScroll: true }); }
    window.scrollTo({ top: root.getBoundingClientRect().top + window.scrollY - headBottom() - 8, behavior: smooth() });
  });
  const DESIGNER = '/tour/designer/';
  /* UnitDesignRequest (design system v102): the designer opens for THIS unit (project, unit id and the card's words), so the
     design is kept for it and the request names it; with no unit picked it stays the demonstration */
  const designerUrl = () => {
    const pk = window.__nlpsPick;
    const slug = ((location.pathname.match(/\/projects\/([^/]+)/) || [])[1] || '').replace(/-(en|fr|ru|ar)$/, '');
    if (!pk || !pk.unit || !slug) return DESIGNER;
    const kick = document.querySelector('#nlps-pick .dus-label-kick');
    const ul = 'קומה ' + pk.floor + (pk.facing ? ' · ' + pk.facing : '') + (kick && kick.textContent.trim() ? ' · ' + kick.textContent.trim() : '');
    return DESIGNER + '?project=' + encodeURIComponent(slug) + '&unit=' + encodeURIComponent(pk.unit) + '&pn=' + encodeURIComponent(String(cfg.name || '')) + '&ul=' + encodeURIComponent(ul);
  };
  /* the floor card's actions (design system ProjectStage version 33) */
  window.addEventListener('nl:floor-action', (e) => {
    const d = e.detail || {};
    ga('floor_action', { action: d.action || '', floor: d.floor, project: cfg.name });
    if (d.action === 'inside') openTourAt(d.floor, d.unit ? String(d.unit).split('-').pop() : 'w', null);
    else if (d.action === 'view') toBelow();
    else if (d.action === 'design') location.href = designerUrl();
  });
  /* the button says which floor's pictures open, when they are not the picked floor's */
  const insideLabel = (f) => {
    const b = document.querySelector('.rbs-act[data-act="inside"]');
    if (!b || !tourFloors.length) return;
    const fl = nearestFloor(f);
    b.textContent = fl === f ? 'להיכנס לדירה · 360°' : 'להיכנס לדירה · מקומה ' + fl;
  };
  /* the steps under the stage: what the page can do, each a button; the current one ringed */
  const steps = [...document.querySelectorAll('[data-nlps-step]')];
  const setStep = (k) => steps.forEach((x) => { if (x.getAttribute('data-nlps-step') === k) x.setAttribute('aria-current', 'step'); else x.removeAttribute('aria-current'); });
  window.addEventListener('nl:floor', (e) => { const d = e.detail || {}; if (d.floor != null) { setStep('view'); insideLabel(Number(d.floor)); } });
  document.addEventListener('click', (e) => {
    const b = e.target && e.target.closest ? e.target.closest('[data-nlps-step]') : null;
    if (!b) return;
    const k = b.getAttribute('data-nlps-step');
    ga('stage_step', { step: k, project: cfg.name });
    if (k === 'floor') { root.scrollIntoView({ behavior: smooth(), block: 'center' }); return; }
    if (k === 'design') { location.href = designerUrl(); return; }
    if (k === 'inside') { openTourAt(selFloor() || 25, selSide() || 'w', b); return; }
    if (k === 'view') {
      // nothing picked yet: floor 25's sea-side example apartment first, so the view and the beam have something to show
      // (the landing is measured after that pick, once the unit line above the map has its height)
      if (!selFloor() && stage && stage.selectUnit) Promise.resolve(stage.ready).then(() => { stage.selectUnit('25-' + seaSide, 'user'); requestAnimationFrame(toBelow); }).catch(() => toBelow());
      else toBelow();
    }
  });

  /* the quarter's legend under the stage (design system QuarterPins): a chip shows its group alone; pressed again, all */
  document.addEventListener('click', (e) => {
    const b = e.target && e.target.closest ? e.target.closest('[data-nlps-phase]') : null;
    if (!b || !stage || typeof stage.focusPhase !== 'function') return;
    const on = b.getAttribute('aria-pressed') !== 'true';
    document.querySelectorAll('[data-nlps-phase]').forEach((x) => x.setAttribute('aria-pressed', on && x.getAttribute('data-nlps-phase') === b.getAttribute('data-nlps-phase') ? 'true' : 'false'));
    const ph = on ? b.getAttribute('data-nlps-phase') : null;
    ga('quarter_legend', { phase: ph || 'all', project: cfg.name });
    Promise.resolve(stage.ready).then(() => stage.focusPhase(ph)).catch(() => {});
  });

  /* "לקומה במגדל" in the deals table: that floor on the stage, and the stage into view */
  document.addEventListener('click', (e) => {
    const b = e.target && e.target.closest ? e.target.closest('[data-nlps-floor]') : null;
    if (!b || !stage) return;
    const f = Number(b.getAttribute('data-nlps-floor'));
    if (!(f > 0)) return;
    ga('deal_floor_click', { floor: f, project: cfg.name });
    Promise.resolve(stage.ready).then(() => {
      stage.selectFloor(f);
      window.dispatchEvent(new CustomEvent('nl:floor', { detail: { floor: f, heightM: stage.floorHeight(f) } }));
      // a direction already picked stays (the same side of the new floor): the view and the map follow it
      const sel = stage.getSelection();
      if (sel && sel.bearing != null) window.dispatchEvent(new CustomEvent('nl:facing', { detail: sel }));
      root.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'center' });
    }).catch(() => {});
  });

  /* ---------------- the view from the floor ---------------- */
  function winCam() {
    const gl = window.mapboxgl; const map = win.map;
    if (!gl || !map) return;
    try {
      const cam = map.getFreeCameraOptions();
      cam.position = gl.MercatorCoordinate.fromLngLat({ lng: Number(cfg.lng), lat: Number(cfg.lat) }, win.alt);
      cam.setPitchBearing(Math.max(35, Math.min(90, 86 + win.vert)), win.bearing); // 86: eye level at the horizon
      map.setFreeCameraOptions(cam);
    } catch (e) {}
    placeViewPins();
  }
  async function showView(d) {
    const gl = await loadMapbox();
    win.bearing = norm(d.bearing);
    // heightM is already the eye height above the floor (the stage's floorEyeHeight adds 1.6 m); the view map has no
    // terrain, so its buildings rise from 0 and this is the camera's height above the ground (Codex's finding, 28.9.2026)
    win.alt = Math.max(10, Number(d.heightM) || 0);
    win.vert = 0;
    const host = document.getElementById('nlps-view-map');
    if (!host) return;
    if (win.map) { winCam(); return; }
    host.classList.remove('nlps-stand');
    if (empty) empty.remove(); // the map's container must be empty
    gl.accessToken = cfg.token;
    // Hebrew place names need the right-to-left text plugin (otherwise the letters come out reversed); once per page
    try { if (gl.getRTLTextPluginStatus && gl.getRTLTextPluginStatus() === 'unavailable') gl.setRTLTextPlugin('https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-rtl-text/v0.3.0/mapbox-gl-rtl-text.js', null, true); } catch (e) {}
    const map = new gl.Map({
      container: host, style: 'mapbox://styles/mapbox/satellite-streets-v12', center: [Number(cfg.lng), Number(cfg.lat)],
      zoom: 16.5, pitch: 70, bearing: win.bearing, maxPitch: 85, interactive: false, attributionControl: true,
    });
    win.map = map;
    map.on('load', () => {
      // place names in Hebrew: in Israel the local name is the Hebrew one (the style would show the English one first)
      try {
        const nf = ['coalesce', ['get', 'name'], ['get', 'name_en']];
        for (const l of map.getStyle().layers || []) {
          if (l.type === 'symbol' && l.layout && l.layout['text-field'] && JSON.stringify(l.layout['text-field']).indexOf('name') > -1) {
            try { map.setLayoutProperty(l.id, 'text-field', nf); } catch (e) {}
          }
        }
      } catch (e) {}
      try { map.addLayer({ id: 'nl-ps-sky', type: 'sky', paint: { 'sky-type': 'atmosphere', 'sky-atmosphere-sun-intensity': 8 } }); } catch (e) {}
      try {
        const layers = map.getStyle().layers; let label;
        for (let i = 0; i < layers.length; i++) { if (layers[i].type === 'symbol' && layers[i].layout && layers[i].layout['text-field']) { label = layers[i].id; break; } }
        map.addLayer({ id: 'nl-ps-3d', source: 'composite', 'source-layer': 'building', filter: ['==', 'extrude', 'true'], type: 'fill-extrusion', minzoom: 13,
          paint: { 'fill-extrusion-color': '#d8d2c4', 'fill-extrusion-height': ['get', 'height'], 'fill-extrusion-base': ['get', 'min_height'], 'fill-extrusion-opacity': 0.85 } }, label);
      } catch (e) {}
      winCam();
      addViewPins(gl, map);
      // AreaLife v97: the registry's places the floor can see, named in the view
      alReady().then((m) => {
        if (!m) return;
        alLayer = m.viewLayer(gl, map, () => ({ bearing: win.bearing, floor: last ? last.floor : 25 }));
        alLayer.update();
        map.on('idle', () => alLayer.update());
      });
    });
    // drag turns the head: sideways the direction, up and down the gaze
    let drag = false, lx = 0, ly = 0;
    const start = (x, y) => { drag = true; lx = x; ly = y; };
    const move = (x, y) => {
      if (!drag) return;
      win.bearing = norm(win.bearing + (x - lx) * 0.35);
      win.vert = Math.max(-45, Math.min(10, win.vert - (y - ly) * 0.22));
      lx = x; ly = y; winCam();
      const w = 100 - (performance.now() - viewAt); // the shared viewing room: nl:view, at most ten a second
      if (w <= 0) sendWinView(); else if (!viewT) viewT = setTimeout(sendWinView, w);
    };
    host.addEventListener('mousedown', (e) => { start(e.clientX, e.clientY); e.preventDefault(); });
    window.addEventListener('mousemove', (e) => move(e.clientX, e.clientY));
    window.addEventListener('mouseup', () => { drag = false; });
    host.addEventListener('touchstart', (e) => start(e.touches[0].clientX, e.touches[0].clientY), { passive: true });
    host.addEventListener('touchmove', (e) => { if (!drag) return; move(e.touches[0].clientX, e.touches[0].clientY); }, { passive: true });
    host.addEventListener('touchend', () => { drag = false; });
  }

  /* ---------------- the beam on the area map (only without the engine) ---------------- */
  let cone = null;
  function areaMap() {
    if (window.NLPJX_MAP) return Promise.resolve(window.NLPJX_MAP);
    return new Promise((resolve) => {
      document.addEventListener('nlpjx:map', () => resolve(window.NLPJX_MAP), { once: true });
    });
  }
  async function showBeam(bearing) {
    if (document.getElementById('nl-root')) return; // the engine draws its own beam; never a second one
    const map = await areaMap();
    const gl = window.mapboxgl;
    if (!map || !gl) return;
    const lngLat = [Number(cfg.lng), Number(cfg.lat)];
    try {
      if (!cone) {
        const el = document.createElement('div');
        el.style.pointerEvents = 'none';
        el.className = 'nlps-cone';
        // the engine's wedge (engine.js showViewCone), drawn from outside it
        el.innerHTML = '<svg width="150" height="150" viewBox="0 0 150 150" style="display:block">'
          + '<defs><linearGradient id="nlps-cone-g" x1="0" y1="0" x2="0" y2="1">'
          + '<stop offset="0" stop-color="#C2563A" stop-opacity="0"/>'
          + '<stop offset="1" stop-color="#C2563A" stop-opacity="0.55"/></linearGradient></defs>'
          + '<path d="M75 75 L44 8 A78 78 0 0 1 106 8 Z" fill="url(#nlps-cone-g)" stroke="#C2563A" stroke-opacity="0.35" stroke-width="1"/></svg>';
        cone = new gl.Marker({ element: el, rotationAlignment: 'map', pitchAlignment: 'map', anchor: 'center' }).setLngLat(lngLat);
      }
      cone.setRotation(norm(bearing)).addTo(map);
      // the map turns so the chosen way is up, and centres 450 m ahead: the building low in the frame, what lies that way
      // (the sea, the city) filling the rest, so the beam is read against it
      const r = norm(bearing) * Math.PI / 180, ahead = 450;
      const lat = Number(cfg.lat) + (ahead * Math.cos(r)) / 111320;
      const lng = Number(cfg.lng) + (ahead * Math.sin(r)) / (111320 * Math.cos(Number(cfg.lat) * Math.PI / 180));
      map.easeTo({ center: [lng, lat], zoom: 14.3, bearing: norm(bearing), pitch: 0, duration: 900 });
    } catch (e) {}
  }
}
