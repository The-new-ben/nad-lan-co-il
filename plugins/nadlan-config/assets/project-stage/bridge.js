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
  try {
    const mod = await import(cfg.stage);
    window.__nlpsStage = mod[cfg.mount](stageEl, {
      preset: 'sunset',
      bearingOffset: Number(cfg.bearingOffset) || 0,
      facingWords: sectors.length ? facingWords : null,
      text: { cta: 'לקבלת תוכניות ומחירים' },
      force3D: /[?&]nlps3d/.test(location.search), // QA only: the scene even on a software renderer
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
  const hasGeo = Number(cfg.lat) && Number(cfg.lng) && cfg.token;
  let last = null;
  const win = { map: null, bearing: 270, vert: 0, alt: 10 };

  const waUrl = (d) => {
    if (!cfg.wa || !d || d.floor == null) return '';
    const words = d.bearing != null ? facingWords(d.bearing) : '';
    const text = 'שלום, אשמח לקבל תוכניות ומחירים לקומה ' + d.floor + ' ב' + cfg.name + (words ? ', ' + words : '') + ' (nad-lan.co.il)';
    return 'https://wa.me/' + cfg.wa + '?text=' + encodeURIComponent(text);
  };
  const setTitle = (d) => {
    if (!title) return;
    title.textContent = 'קומה ' + d.floor;
    const words = d.bearing != null ? facingWords(d.bearing) : '';
    if (words) {
      title.append(' · ');
      const s = document.createElement('span'); s.className = 'nlps-dir'; s.textContent = words; title.append(s);
    }
  };

  window.addEventListener('nl:floor', (e) => {
    const d = e.detail || {};
    if (d.floor == null) return;
    ga('stage_floor', { floor: d.floor, project: cfg.name });
    if (wa) wa.href = waUrl(d);
    if (!last || last.floor !== d.floor) {
      setTitle({ floor: d.floor });
      if (empty && !win.map) empty.textContent = 'עכשיו בחרו נקודה בטבעת הקומה, והנוף לכיוון הזה יופיע כאן.';
    }
    if (cta) cta.hidden = false;
  });

  window.addEventListener('nl:facing', (e) => {
    const d = e.detail || {};
    if (d.floor == null || d.bearing == null) return;
    last = d;
    ga('stage_facing', { floor: d.floor, facing: facingWords(d.bearing), project: cfg.name });
    if (hint) hint.hidden = true;
    setTitle(d);
    const h = Math.max(10, Math.round(Number(d.heightM) || 0));
    if (cap) { cap.textContent = 'הדמיה להמחשה בלבד: מבט משוער מגובה של כ־' + h + ' מ׳, לפי מפה. אינו צילום מהדירה.'; cap.hidden = false; }
    if (wa) wa.href = waUrl(d);
    if (cta) cta.hidden = false;
    if (hasGeo) {
      showView(d).catch(() => {});
      showBeam(d.bearing).catch(() => {});
    }
  });

  window.addEventListener('nl:floor-cta', (e) => {
    const d = Object.assign({}, last || {}, e.detail || {});
    if (d.floor == null) return;
    const url = waUrl(d);
    ga('whatsapp_click', { source: 'project-stage', floor: d.floor });
    if (url) window.open(url, '_blank', 'noopener');
  });
  if (wa) wa.addEventListener('click', () => ga('whatsapp_click', { source: 'project-stage-view', floor: last ? last.floor : null }));

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
  }
  async function showView(d) {
    const gl = await loadMapbox();
    win.bearing = norm(d.bearing);
    win.alt = Math.max(10, (Number(d.heightM) || 0) + 1.6);
    win.vert = 0;
    const host = document.getElementById('nlps-view-map');
    if (!host) return;
    if (win.map) { winCam(); return; }
    host.classList.remove('nlps-stand');
    if (empty) empty.hidden = true;
    gl.accessToken = cfg.token;
    const map = new gl.Map({
      container: host, style: 'mapbox://styles/mapbox/satellite-streets-v12', center: [Number(cfg.lng), Number(cfg.lat)],
      zoom: 16.5, pitch: 70, bearing: win.bearing, maxPitch: 85, interactive: false, attributionControl: true,
    });
    win.map = map;
    map.on('load', () => {
      try { map.addLayer({ id: 'nl-ps-sky', type: 'sky', paint: { 'sky-type': 'atmosphere', 'sky-atmosphere-sun-intensity': 8 } }); } catch (e) {}
      try {
        const layers = map.getStyle().layers; let label;
        for (let i = 0; i < layers.length; i++) { if (layers[i].type === 'symbol' && layers[i].layout && layers[i].layout['text-field']) { label = layers[i].id; break; } }
        map.addLayer({ id: 'nl-ps-3d', source: 'composite', 'source-layer': 'building', filter: ['==', 'extrude', 'true'], type: 'fill-extrusion', minzoom: 13,
          paint: { 'fill-extrusion-color': '#d8d2c4', 'fill-extrusion-height': ['get', 'height'], 'fill-extrusion-base': ['get', 'min_height'], 'fill-extrusion-opacity': 0.85 } }, label);
      } catch (e) {}
      winCam();
    });
    // drag turns the head: sideways the direction, up and down the gaze
    let drag = false, lx = 0, ly = 0;
    const start = (x, y) => { drag = true; lx = x; ly = y; };
    const move = (x, y) => {
      if (!drag) return;
      win.bearing = norm(win.bearing + (x - lx) * 0.35);
      win.vert = Math.max(-45, Math.min(10, win.vert - (y - ly) * 0.22));
      lx = x; ly = y; winCam();
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
      // the map turns so the chosen way is up, the building in the middle and what lies that way ahead of it
      map.easeTo({ center: lngLat, zoom: 14.6, bearing: norm(bearing), duration: 900 }); // 14.6: the coast and the city are in the frame
    } catch (e) {}
  }
}
