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
  try {
    const mod = await import(cfg.stage);
    window.__nlpsStage = mod[cfg.mount](stageEl, {
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
  function showNear(bearing) {
    if (!nearEl || !QITEMS.length) return;
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
  }

  const waUrl = (d) => {
    if (!cfg.wa || !d || d.floor == null) return '';
    const words = d.toward ? 'לכיוון ' + d.toward : (d.bearing != null ? facingWords(d.bearing) : '');
    const text = 'שלום, אשמח לקבל תוכניות ומחירים ' + (d.unit ? 'לדירה בקומה ' : 'לקומה ') + d.floor + ' ב' + cfg.name + (words ? ', ' + words : '') + ' (nad-lan.co.il)';
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
      const u = sel && sel.unit ? String(sel.unit).split('-')[1] : null;
      ga('floor_slice', { floor: f, project: cfg.name });
      import(new URL('./slice.js' + new URL(import.meta.url).search, import.meta.url).href).then((m) => m.openSlice({
        stage, floor: f, unit: u, units: cfg.units, words: facingWords, note: cfg.sliceNote || '', tourFloors, opener: sl,
      })).catch((err) => console.warn('[project stage] slice', err));
    });
  }
  const tourFloors = [...new Set(allScenes.map((x) => Number(x.floor) || 25))].sort((a, b) => a - b);
  const nearestFloor = (f) => (tourFloors.length ? tourFloors.reduce((b, x) => (Math.abs(x - f) < Math.abs(b - f) ? x : b), tourFloors[0]) : 25);
  function openTourAt(floor, side, opener) {
    if (!tourBtn) return;
    const fl = nearestFloor(Number(floor) || 25);
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
    import(new URL('./tour.js' + new URL(import.meta.url).search, import.meta.url).href).then((m) => m.openTour({
      src: d.src, srcSmall: d.small || d.src, title: d.title || '', chip: 'מתקן לדוגמה', opener: d.opener || null,
      caption: 'הדמיה להמחשה בלבד: המיקום, החלוקה והריהוט משוערים ואינם לפי תוכנית היזם.' + (d.note ? ' ' + d.note : ''),
    })).catch((err) => console.warn('[project stage] facility tour', err));
  });
  const selSide = () => { try { const sel = stage && stage.getSelection && stage.getSelection(); return sel && sel.unit ? String(sel.unit).split('-')[1] : null; } catch (err) { return null; } };
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
  const toBelow = () => {
    if (!below) return;
    const top = below.getBoundingClientRect().top + window.scrollY - 84; // under the sticky header
    window.scrollTo({ top, behavior: smooth() });
  };
  const DESIGNER = '/tour/designer/';
  /* the floor card's actions (design system ProjectStage version 33) */
  window.addEventListener('nl:floor-action', (e) => {
    const d = e.detail || {};
    ga('floor_action', { action: d.action || '', floor: d.floor, project: cfg.name });
    if (d.action === 'inside') openTourAt(d.floor, d.unit ? String(d.unit).split('-')[1] : 'w', null);
    else if (d.action === 'view') toBelow();
    else if (d.action === 'design') location.href = DESIGNER;
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
    if (k === 'design') { location.href = DESIGNER; return; }
    if (k === 'inside') { openTourAt(selFloor() || 25, selSide() || 'w', b); return; }
    if (k === 'view') {
      // nothing picked yet: floor 25's sea-side example apartment first, so the view and the beam have something to show
      if (!selFloor() && stage && stage.selectUnit) Promise.resolve(stage.ready).then(() => { stage.selectUnit('25-' + seaSide, 'user'); }).catch(() => {});
      toBelow();
    }
  });

  /* the quarter's legend under the stage (design system QuarterPins): a chip shows its group alone; pressed again, all */
  document.addEventListener('click', (e) => {
    const b = e.target && e.target.closest ? e.target.closest('[data-nlps-phase]') : null;
    if (!b || !stage || typeof stage.focusPhase !== 'function') return;
    const on = b.getAttribute('aria-pressed') !== 'true';
    document.querySelectorAll('[data-nlps-phase]').forEach((x) => x.setAttribute('aria-pressed', x === b && on ? 'true' : 'false'));
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
