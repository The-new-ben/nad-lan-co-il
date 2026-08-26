const dataFiles = {
  project: 'data/project.json',
  units: 'data/units.json',
  facilities: 'data/facilities.json',
  interiorScenes: 'data/interior-scenes.json',
  studioCatalog: 'data/studio-catalog.json',
  codeEvidence: 'data/code-evidence.json',
  selectionAudit: 'data/unit-selection-audit.json',
  htmlSource: 'data/html-source-audit.json',
  environment: 'data/environment.json',
  drawings: 'data/drawings.json',
  translations: 'data/translations.json',
  bom: 'data/engineering-bom.json',
  checklist: 'data/master-checklist.json',
  matrix: 'data/matrix-test-cases.json',
  testResults: 'data/test-results.json',
  sequence: 'data/page-sequence.json',
  seo: 'data/seo-intent-map.json',
  wordpress: 'data/wordpress-contract.json',
  options: 'data/implementation-options.json'
};

const state = {
  mode: 'buyer',
  scene: 'building',
  language: 'he',
  room: 'all',
  selectedUnitId: 'aur-t-40-a',
  selectedFacilityId: 'sea-pool',
  selectedEnvironmentId: 'beach',
  environmentCategory: 'all',
  lookOffset: 0,
  studioCategory: 'finish',
  selectedStudioItemId: 'fin-stone-120',
  studioItems: [],
  studioHistory: [],
  studioVersion: 1,
  hotspotClickProof: null,
  surfacePickProof: null,
  surfacePickAttempt: null,
  modelPointerStart: null,
  lastSelectionOrigin: 'initial',
  codeEvidenceResults: {},
  selectedCheckId: null,
  selectedBomId: 'S01',
  localChecks: []
};

let data = {};
let unitMap = null;
let unitViewCone = null;
let environmentLayers = [];
let interiorViewer = null;
let facilityViewer = null;
let planZoom = 1;
let projectedHotspotFrame = 0;

const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
const formatPrice = (value) => new Intl.NumberFormat(state.language === 'he' ? 'he-IL' : state.language, { style: 'currency', currency: 'ILS', maximumFractionDigits: 0 }).format(value);
const safe = (value) => String(value ?? '').replace(/[&<>"]/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[char]));

async function loadData() {
  const entries = await Promise.all(Object.entries(dataFiles).map(async ([key, url]) => {
    const response = await fetch(url, { cache: 'no-store' });
    if (!response.ok) throw new Error(`${url}: HTTP ${response.status}`);
    return [key, await response.json()];
  }));
  data = Object.fromEntries(entries);
  const requestedUnit = new URL(window.location.href).searchParams.get('unit_id');
  if (requestedUnit && data.units.some((unit) => unit.id === requestedUnit)) state.selectedUnitId = requestedUnit;
  if (!requestedUnit) {
    const initialUrl = new URL(window.location.href);
    initialUrl.searchParams.set('unit_id', state.selectedUnitId);
    history.replaceState({ unit_id: state.selectedUnitId }, '', `${initialUrl.pathname}${initialUrl.search}${initialUrl.hash}`);
  }
  window.NADLAN_SHOWROOM = {
    version: '1.72.219-aurelia-1.0.0',
    config: {
      active_project: data.project.id,
      lead_endpoint: data.wordpress.runtimeContract.endpoints.find((item) => item.includes('lead')),
      brochure_endpoint: data.wordpress.runtimeContract.endpoints.find((item) => item.includes('brochure')),
      cotour_endpoint: data.wordpress.runtimeContract.endpoints.find((item) => item.includes('cotour')),
      languages: ['he', 'en', 'fr', 'ru', 'ar'],
      studio: true,
      selected_unit_surface: true,
      selected_unit_surface_v2: true
    },
    projects: [{
      wp_id: 7304,
      slug: data.project.identity.slug,
      name: data.project.identity.title,
      lat: data.project.position.lat,
      lng: data.project.position.lng,
      geo: { lat: data.project.position.lat, lng: data.project.position.lng },
      floor_height_m: data.project.architecture.floorHeightM,
      avg_price_per_sqm: data.project.pricing.averagePerSqm,
      model_glb: `assets/${data.project.assets.modelGlb}`,
      model_poster: `assets/${data.project.assets.modelPoster}`,
      units: data.units,
      drawings: data.drawings,
      facilities: data.facilities,
      environment: data.environment,
      interior_scenes: data.interiorScenes,
      studio_catalog: data.studioCatalog
    }]
  };
  window.NADLAN_SELECTION = { project_id: data.project.id, unit_id: state.selectedUnitId, origin: 'initial', timestamp: new Date().toISOString() };
  state.selectedCheckId = data.checklist.definitions[0]?.id;
  initialize();
}

function initialize() {
  bindGlobalControls();
  renderBuyer();
  renderRecipe();
  renderChecklist();
  renderSelectionAudit();
  renderBom();
  renderSeo();
  renderSourceAudit();
  renderWordPress();
  setMode('buyer');
  const upgrade = window.customElements?.whenDefined ? customElements.whenDefined('model-viewer') : Promise.resolve();
  upgrade.then(() => {
    installModelHotspots();
    wireProjectedHotspots();
    $('#building-model')?.addEventListener('load', () => { installModelHotspots(); updateProjectedHotspotPositions(); }, { once: true });
    initializeInteractiveSurfaces();
  });
  verifyCodeEvidence();
}

function bindGlobalControls() {
  $$('.mode-nav button').forEach((button) => button.addEventListener('click', () => setMode(button.dataset.mode)));
  $$('[data-scroll]').forEach((button) => button.addEventListener('click', () => document.getElementById(button.dataset.scroll)?.scrollIntoView({ behavior: 'smooth', block: 'start' })));
  $$('[data-dialog]').forEach((button) => button.addEventListener('click', () => openDialog(button.dataset.dialog)));
  $('.dialog-close').addEventListener('click', closeDialog);
  $('.dialog-done').addEventListener('click', closeDialog);
  $('#dialog').addEventListener('click', (event) => { if (event.target.id === 'dialog') closeDialog(); });
  document.addEventListener('keydown', (event) => { if (event.key === 'Escape' && !$('#dialog').hidden) closeDialog(); });
  $('#decision-form').addEventListener('submit', submitDecision);
  $('#language').addEventListener('change', (event) => setLanguage(event.target.value));
  $$('.scene-tabs [data-scene]').forEach((button) => button.addEventListener('click', () => setScene(button.dataset.scene)));
  $$('[data-scene-jump]').forEach((button) => button.addEventListener('click', () => { setScene(button.dataset.sceneJump); $('#inventory').scrollIntoView({ behavior: 'smooth' }); }));
  $$('.filters [data-room]').forEach((button) => button.addEventListener('click', () => { state.room = button.dataset.room; $$('.filters [data-room]').forEach((item) => item.classList.toggle('active', item === button)); renderInventory(); }));
  $$('.look-controls [data-look]').forEach((button) => button.addEventListener('click', () => { state.lookOffset = Number(button.dataset.look); updateUnitMap(); $('.window-pov img').style.objectPosition = `${50 + state.lookOffset}% center`; $('#window-proof-caption').textContent = `${state.lookOffset < 0 ? 'שמאלה' : state.lookOffset > 0 ? 'ימינה' : 'מרכז'} · ${selectedUnit().view}`; }));
  $$('[data-plan-zoom]').forEach((button) => button.addEventListener('click', () => changePlanZoom(button.dataset.planZoom)));
  $$('.studio-options button').forEach((button) => button.addEventListener('click', () => selectStudioOption(button)));
  $('#studio-canvas').addEventListener('click', addStudioAnnotation);
  $('#studio-undo').addEventListener('click', undoStudioItem);
  $('#studio-clear').addEventListener('click', clearStudioItems);
  $('#studio-notes').addEventListener('input', () => { state.studioVersion += 1; $('#studio-version').textContent = state.studioVersion; });
  const buildingScene = $('[data-scene-panel="building"]');
  buildingScene.addEventListener('pointerdown', (event) => {
    if (!event.isPrimary || event.button !== 0 || event.composedPath().some((node) => node?.dataset?.projectedUnitId)) return;
    state.modelPointerStart = { pointerId: event.pointerId, clientX: event.clientX, clientY: event.clientY, time: performance.now() };
  }, true);
  buildingScene.addEventListener('pointerup', (event) => {
    const start = state.modelPointerStart;
    state.modelPointerStart = null;
    if (!start || start.pointerId !== event.pointerId || event.composedPath().some((node) => node?.dataset?.projectedUnitId)) return;
    const movement = Math.hypot(event.clientX - start.clientX, event.clientY - start.clientY);
    if (movement > 6 || performance.now() - start.time > 900) return;
    selectUnitFromModelSurface(event);
  }, true);
  $('#check-search').addEventListener('input', renderChecklistRows);
  $('#check-domain').addEventListener('change', renderChecklistRows);
  $('#check-mode').addEventListener('change', renderChecklistRows);
  $('#run-local-checks').addEventListener('click', runLocalChecks);
}

function setMode(mode) {
  state.mode = mode;
  $$('.mode-nav button').forEach((button) => button.classList.toggle('active', button.dataset.mode === mode));
  $$('.view').forEach((view) => view.classList.toggle('active', view.dataset.view === mode));
  document.body.classList.toggle('lab-mode', mode !== 'buyer');
  window.scrollTo({ top: 0, behavior: 'instant' });
  $('#app').focus({ preventScroll: true });
}

function setLanguage(language) {
  state.language = language;
  const t = data.translations[language] ?? data.translations.he;
  const languageInfo = data.seo.languages.find((item) => item.code === language);
  document.documentElement.lang = language;
  document.documentElement.dir = languageInfo?.dir ?? 'rtl';
  $('#hero-title').textContent = t.title;
  $('#hero-eyebrow').textContent = t.eyebrow;
  $('#hero-intro').textContent = t.intro;
  $('#hero-select').textContent = t.selectUnit;
  renderUnitCard();
}

function selectedUnit() {
  return data.units.find((unit) => unit.id === state.selectedUnitId) ?? data.units[0];
}

function publicAvailability(value) {
  if (value === 'שמור') return 'שמורה';
  if (value === 'בעדיפות') return 'מבוקשת';
  return 'זמינה';
}

function filteredUnits() {
  const units = state.room === 'all' ? data.units : data.units.filter((unit) => String(unit.rooms) === state.room);
  return units.sort((a, b) => a.floor - b.floor || a.line.localeCompare(b.line));
}

function representativeUnits(units) {
  if (units.length <= 8) return units;
  const indexes = [0, .14, .28, .42, .56, .7, .84, 1].map((ratio) => Math.min(units.length - 1, Math.round((units.length - 1) * ratio)));
  const chosen = indexes.map((index) => units[index]);
  const active = selectedUnit();
  if (!chosen.some((unit) => unit.id === active.id) && units.some((unit) => unit.id === active.id)) {
    const closestIndex = chosen.reduce((best, unit, index) => Math.abs(unit.floor - active.floor) < Math.abs(chosen[best].floor - active.floor) ? index : best, 0);
    chosen.splice(closestIndex, 1, active);
  }
  return [...new Map(chosen.map((unit) => [unit.id, unit])).values()];
}

function renderBuyer() {
  renderInventory();
  renderFacilities();
  renderEnvironment();
  renderInteriorScenes();
  renderStudioCatalog();
  renderStudioState();
  renderUnitCard();
}

function renderInventory() {
  const units = filteredUnits();
  const displayedUnits = units.slice(0, 70);
  const selected = units.find((unit) => unit.id === state.selectedUnitId);
  if (selected && !displayedUnits.some((unit) => unit.id === selected.id)) displayedUnits.splice(displayedUnits.length - 1, 1, selected);
  $('#available-count').textContent = units.length;
  $('#unit-list').innerHTML = displayedUnits.map((unit) => `
    <button class="unit-row ${unit.id === state.selectedUnitId ? 'active' : ''}" data-unit-id="${safe(unit.id)}">
      <b>${safe(unit.label)}</b><em>${publicAvailability(unit.availability)}</em>
      <span>${unit.rooms} חד׳ · ${unit.sqm} מ״ר · קומה ${unit.floor}</span><small>${formatPrice(unit.price)}</small>
    </button>`).join('');
  $$('#unit-list [data-unit-id]').forEach((button) => button.addEventListener('click', () => selectUnit(button.dataset.unitId, 'inventory')));
  requestAnimationFrame(() => $('#unit-list .unit-row.active')?.scrollIntoView({ block: 'nearest' }));

  installModelHotspots(units);
}

function installModelHotspots(units = filteredUnits()) {
  const model = $('#building-model');
  if (!model) return;
  $$('.model-hotspot', model).forEach((button) => button.remove());
  representativeUnits(units).forEach((unit) => {
    const button = document.createElement('button');
    const anchor = unit.selection?.anchor;
    button.className = `hotspot model-hotspot ${unit.id === state.selectedUnitId ? 'active' : ''}`;
    button.slot = `hotspot-${unit.id}`;
    button.dataset.position = (anchor?.position || String(unit.hotspot_position).split(' ')).map((part) => `${part}m`).join(' ');
    button.dataset.normal = (anchor?.normal || String(unit.hotspot_normal || '0 0 1').split(' ')).join(' ');
    button.dataset.visibilityAttribute = 'visible';
    button.dataset.act = 'select';
    button.dataset.id = unit.id;
    button.dataset.unitId = unit.id;
    button.dataset.floor = unit.floor;
    button.textContent = unit.floor;
    button.setAttribute('aria-label', `${unit.label}, קומה ${unit.floor}, ${unit.rooms} חדרים`);
    button.addEventListener('click', (event) => { event.stopPropagation(); selectUnit(unit.id, 'hotspot'); });
    model.append(button);
  });
  renderProjectedHotspots();
}

function renderProjectedHotspots() {
  const overlay = $('#hotspot-overlay');
  const model = $('#building-model');
  if (!overlay || !model) return;
  const unitButtons = $$('.model-hotspot', model);
  overlay.innerHTML = unitButtons.map((button) => {
    const unit = data.units.find((item) => item.id === button.dataset.unitId);
    return `<button class="hotspot projected-hotspot ${button.dataset.unitId === state.selectedUnitId ? 'active' : ''}" data-projected-unit-id="${safe(button.dataset.unitId)}" data-slot="${safe(button.slot)}" data-label="${safe(unit?.label || button.dataset.unitId)}" aria-label="${safe(unit ? `${unit.label}, קומה ${unit.floor}, ${unit.rooms} חדרים` : button.dataset.unitId)}">${safe(unit?.floor ?? '')}</button>`;
  }).join('');
  $$('.projected-hotspot', overlay).forEach((button) => button.addEventListener('click', (event) => {
    event.stopPropagation();
    const requestedUnitId = button.dataset.projectedUnitId;
    selectUnit(requestedUnitId, 'hotspot');
    state.hotspotClickProof = {
      requestedUnitId,
      selectedUnitId: state.selectedUnitId,
      urlUnitId: new URL(location.href).searchParams.get('unit_id')
    };
  }));
  updateProjectedHotspotPositions();
}

function updateProjectedHotspotPositions() {
  cancelAnimationFrame(projectedHotspotFrame);
  projectedHotspotFrame = requestAnimationFrame(() => {
    const model = $('#building-model');
    if (!model?.queryHotspot) return;
    const width = model.clientWidth;
    const height = model.clientHeight;
    const rect = model.getBoundingClientRect();
    $$('.projected-hotspot', $('#hotspot-overlay')).forEach((button) => {
      try {
        const projection = model.queryHotspot(button.dataset.slot);
        const point = projection?.canvasPosition;
        const inside = point && point.x >= 0 && point.y >= 0 && point.x <= width && point.y <= height;
        const surfaceHit = inside && model.positionAndNormalFromPoint ? model.positionAndNormalFromPoint(rect.left + point.x, rect.top + point.y) : null;
        const surfaceDistance = surfaceHit && projection?.position ? Math.hypot(surfaceHit.position.x - projection.position.x, surfaceHit.position.y - projection.position.y, surfaceHit.position.z - projection.position.z) : Infinity;
        button.hidden = !projection || !projection.facingCamera || !inside || surfaceDistance > 4;
        if (!button.hidden) {
          button.style.left = `${point.x}px`;
          button.style.top = `${point.y}px`;
          button.dataset.projectedX = point.x.toFixed(2);
          button.dataset.projectedY = point.y.toFixed(2);
          button.dataset.surfaceDistance = surfaceDistance.toFixed(2);
        }
      } catch (error) {
        button.hidden = true;
      }
    });
  });
}

function vectorDot(a, b) {
  return Number(a.x) * Number(b[0]) + Number(a.y) * Number(b[1]) + Number(a.z) * Number(b[2]);
}

function resolveUnitFromSurfaceHit(hit) {
  if (!hit?.position || !hit?.normal) return null;
  const candidates = filteredUnits().map((unit) => {
    const selection = unit.selection;
    if (!selection?.anchor || !selection.hitRegion) return null;
    const anchor = selection.anchor.position;
    const region = selection.hitRegion;
    if (hit.position.y < region.floorMinY || hit.position.y > region.floorMaxY) return null;
    const normalDot = vectorDot(hit.normal, selection.anchor.normal);
    if (normalDot < region.minNormalDot) return null;
    const distance = Math.hypot(hit.position.x - anchor[0], hit.position.y - anchor[1], hit.position.z - anchor[2]);
    if (distance > region.maxSurfaceDistanceM) return null;
    return { unit, distance, normalDot, score: distance + (1 - normalDot) * 2.4 };
  }).filter(Boolean).sort((a, b) => a.score - b.score);
  return candidates[0] || null;
}

function selectUnitFromModelSurface(event) {
  const model = $('#building-model');
  if (!model?.positionAndNormalFromPoint || event.clientX == null || event.clientY == null) {
    state.surfacePickAttempt = { reason: 'api-or-coordinates-missing' };
    return;
  }
  const hit = model.positionAndNormalFromPoint(event.clientX, event.clientY);
  const match = resolveUnitFromSurfaceHit(hit);
  state.surfacePickAttempt = {
    clientX: event.clientX,
    clientY: event.clientY,
    hit: hit ? { position: [hit.position.x, hit.position.y, hit.position.z], normal: [hit.normal.x, hit.normal.y, hit.normal.z] } : null,
    matchedUnitId: match?.unit?.id || null
  };
  if (!match) return;
  const requestedUnitId = match.unit.id;
  selectUnit(requestedUnitId, 'surface');
  state.surfacePickProof = {
    requestedUnitId,
    selectedUnitId: state.selectedUnitId,
    urlUnitId: new URL(location.href).searchParams.get('unit_id'),
    hitPosition: [hit.position.x, hit.position.y, hit.position.z],
    distanceM: match.distance,
    normalDot: match.normalDot
  };
}

function wireProjectedHotspots() {
  const model = $('#building-model');
  if (!model || model.dataset.projectedHotspots === '1') return;
  model.dataset.projectedHotspots = '1';
  model.addEventListener('camera-change', updateProjectedHotspotPositions);
  model.addEventListener('load', updateProjectedHotspotPositions);
  window.addEventListener('resize', updateProjectedHotspotPositions, { passive: true });
}

function selectUnit(id, origin = 'programmatic') {
  const nextUnit = data.units.find((unit) => unit.id === id);
  if (!nextUnit) return;
  const previousUnitId = state.selectedUnitId;
  state.selectedUnitId = id;
  state.lastSelectionOrigin = origin;
  const url = new URL(window.location.href);
  url.searchParams.set('unit_id', id);
  history.replaceState({ unit_id: id }, '', `${url.pathname}${url.search}${url.hash}`);
  renderInventory();
  renderUnitCard();
  updateScenes();
  const detail = { project_id: data.project.id, unit_id: id, previous_unit_id: previousUnitId, origin, floor: nextUnit.floor, line: nextUnit.line, azimuth: nextUnit.directionAzimuth, timestamp: new Date().toISOString() };
  window.NADLAN_SELECTION = detail;
  document.dispatchEvent(new CustomEvent('nadlan:unit-selected', { detail }));
}

function setScene(scene) {
  state.scene = scene;
  $$('.scene-tabs [data-scene]').forEach((button) => button.classList.toggle('active', button.dataset.scene === scene));
  $$('[data-scene-panel]').forEach((panel) => panel.classList.toggle('active', panel.dataset.scenePanel === scene));
  updateScenes();
  requestAnimationFrame(() => {
    if (scene === 'view') updateUnitMap();
    if (scene === 'interior') ensureInteriorViewer();
    if (scene === 'facilities') ensureFacilityViewer();
  });
}

function updateScenes() {
  const unit = selectedUnit();
  const drawing = data.drawings.find((item) => item.id === unit.plan_id) ?? data.drawings[0];
  $('#plan-image').src = `assets/${drawing.asset}`;
  $('#plan-image').alt = `${drawing.label}, ${unit.rooms} חדרים, קומה ${unit.floor}, כיוון ${unit.dir}`;
  $('#plan-copy').textContent = `${unit.rooms} חדרים · ${unit.sqm} מ״ר · מרפסת ${unit.balcony} מ״ר · ${unit.dir}`;
  $('#view-title').textContent = `הנוף לכיוון ${unit.dir}`;
  $('#view-copy').textContent = `${unit.view} · קומה ${unit.floor} · גובה מבט ${Math.round(data.project.architecture.groundElevationM + unit.floor * data.project.architecture.floorHeightM)} מ׳`;
  $('#interior-room').textContent = `סלון · ${unit.view}`;
  $('#studio-plan').src = `assets/${drawing.asset}`;
  $('#studio-unit').textContent = `${unit.label} · קומה ${unit.floor}`;
  $('#appointment-unit').textContent = `${unit.label}, קומה ${unit.floor}, ${unit.rooms} חדרים — התוכנית, הנוף והמפרט יצורפו לבקשה.`;
  updateUnitMap();
}

function renderUnitCard() {
  const unit = selectedUnit();
  $('#unit-card').innerHTML = `
    <div class="unit-name"><small>הדירה שבחרתם</small><b>${safe(unit.label)} · ${safe(unit.building)}</b><span>${publicAvailability(unit.availability)} · ${safe(unit.view)}</span></div>
    <dl><div><dt>קומה</dt><dd>${unit.floor}</dd></div><div><dt>חדרים</dt><dd>${unit.rooms}</dd></div><div><dt>שטח</dt><dd>${unit.sqm} מ״ר</dd></div><div><dt>מרפסת</dt><dd>${unit.balcony} מ״ר</dd></div><div><dt>כיוון</dt><dd>${safe(unit.dir)}</dd></div><div><dt>קו</dt><dd>${safe(unit.line)}</dd></div></dl>
    <div class="unit-price"><small>מחיר הדירה</small><b>${formatPrice(unit.price)}</b></div>
    <div class="unit-actions"><button data-unit-focus>סובבו לחזית הדירה</button><button data-scene="plan">תוכנית</button><button data-scene="view">נוף</button><button data-scene="interior">סיור פנים</button><button data-scene="facilities">מתקנים</button><button data-dialog="lead">קבלת תוכניות ומחירים</button></div>`;
  $$('#unit-card [data-scene]').forEach((button) => button.addEventListener('click', () => setScene(button.dataset.scene)));
  $$('#unit-card [data-dialog]').forEach((button) => button.addEventListener('click', () => openDialog(button.dataset.dialog)));
  $('#unit-card [data-unit-focus]')?.addEventListener('click', () => {
    const model = $('#building-model');
    if (model && selectedUnit().camera_orbit) model.cameraOrbit = selectedUnit().camera_orbit;
  });
  updateScenes();
}

function renderFacilities() {
  $('#facility-pins').innerHTML = data.facilities.map((facility) => `<button class="${facility.id === state.selectedFacilityId ? 'active' : ''}" style="left:${facility.hotspot[0]}%;top:${facility.hotspot[1]}%" data-facility-id="${safe(facility.id)}">${safe(facility.label)}</button>`).join('');
  $$('#facility-pins [data-facility-id]').forEach((button) => button.addEventListener('click', () => { state.selectedFacilityId = button.dataset.facilityId; renderFacilities(); ensureFacilityViewer(); }));
  const facility = data.facilities.find((item) => item.id === state.selectedFacilityId) ?? data.facilities[0];
  $('#facility-card').innerHTML = `<div><small>FACILITY · ${safe(facility.id)} · מפלס ${facility.level}</small><b>${safe(facility.label)}</b><span>${safe(facility.detail)}</span></div><dl><div><dt>שטח</dt><dd>${facility.areaSqm} מ״ר</dd></div><div><dt>גובה</dt><dd>${facility.ceilingM} מ׳</dd></div><div><dt>קיבולת</dt><dd>${facility.capacity}</dd></div><div><dt>פעילות</dt><dd>${safe(facility.schedule)}</dd></div><div><dt>מהלובי</dt><dd>${facility.routeMin} דק׳</dd></div></dl><section><b>מה יש כאן</b><span>${facility.equipment.map(safe).join(' · ')}</span><b>נגישות ותפעול</b><span>${safe(facility.accessibility)} · ${facility.operations.map(safe).join(' · ')}</span></section>`;
}

function renderEnvironment() {
  const categories = [...new Set(data.environment.map((item) => item.category))];
  $('#environment-filters').innerHTML = `<button class="${state.environmentCategory === 'all' ? 'active' : ''}" data-category="all">הכול</button>` + categories.map((category) => `<button class="${state.environmentCategory === category ? 'active' : ''}" data-category="${safe(category)}">${safe(category)}</button>`).join('');
  $$('#environment-filters [data-category]').forEach((button) => button.addEventListener('click', () => { state.environmentCategory = button.dataset.category; renderEnvironment(); drawEnvironmentLayers(); }));
  const point = data.environment.find((item) => item.id === state.selectedEnvironmentId) ?? data.environment[0];
  $('#environment-card').innerHTML = `<small>${safe(point.category).toUpperCase()} · ${safe(point.id)}</small><b>${safe(point.label)}</b><span>${point.walkMin ? `${point.walkMin} דקות הליכה` : `${point.bikeMin} דקות באופניים`} · מחובר לנקודת הפרויקט ${data.project.position.lat}, ${data.project.position.lng}</span>`;
}

function selectStudioOption(button) {
  $$('.studio-options button').forEach((item) => item.classList.toggle('selected', item === button));
  state.studioCategory = button.dataset.option;
  const first = data.studioCatalog.find((item) => item.category === state.studioCategory);
  if (first) state.selectedStudioItemId = first.id;
  renderStudioCatalog();
}

function initializeInteractiveSurfaces() {
  ensureUnitMap();
  ensureInteriorViewer();
  ensureFacilityViewer();
}

function ensureUnitMap() {
  const mapRuntime = window.mapboxgl || window.maplibregl;
  if (!mapRuntime || unitMap || !$('#unit-map')) return;
  window.mapboxgl = mapRuntime;
  const configuredToken = String(data.project.map.mapboxToken || '');
  const hasRepositorySafeMapboxToken = configuredToken.startsWith('pk.') && !configuredToken.includes('REDACTED');
  if (hasRepositorySafeMapboxToken) mapboxgl.accessToken = configuredToken;
  const repositorySafeMapStyle = hasRepositorySafeMapboxToken
    ? 'mapbox://styles/mapbox/light-v11'
    : {
        version: 8,
        sources: {
          osm: {
            type: 'raster',
            tiles: ['https://tile.openstreetmap.org/{z}/{x}/{y}.png'],
            tileSize: 256,
            attribution: '© OpenStreetMap contributors'
          }
        },
        layers: [{ id: 'osm', type: 'raster', source: 'osm' }]
      };
  unitMap = new mapboxgl.Map({
    container: 'unit-map',
    style: repositorySafeMapStyle,
    center: [data.project.position.lng, data.project.position.lat],
    zoom: 15.5,
    pitch: 45,
    bearing: -17.6,
    cooperativeGestures: true,
    attributionControl: true
  });
  unitMap.addControl(new mapboxgl.NavigationControl({ showCompass: true }), 'top-left');
  new mapboxgl.Marker({ color: '#9C7A3C' }).setLngLat([data.project.position.lng, data.project.position.lat]).setPopup(new mapboxgl.Popup({ offset: 18 }).setText(data.project.identity.title)).addTo(unitMap);
  unitMap.on('style.load', () => {
    try {
      const layers = unitMap.getStyle().layers;
      const labelLayer = layers.find((layer) => layer.type === 'symbol' && layer.layout?.['text-field'])?.id;
      if (unitMap.getSource('composite') && !unitMap.getLayer('aurelia-3d-buildings')) unitMap.addLayer({ id: 'aurelia-3d-buildings', source: 'composite', 'source-layer': 'building', filter: ['==', 'extrude', 'true'], type: 'fill-extrusion', minzoom: 15, paint: { 'fill-extrusion-color': '#aaa', 'fill-extrusion-height': ['interpolate', ['linear'], ['zoom'], 15, 0, 15.05, ['get', 'height']], 'fill-extrusion-base': ['interpolate', ['linear'], ['zoom'], 15, 0, 15.05, ['get', 'min_height']], 'fill-extrusion-opacity': .6 } }, labelLayer);
    } catch (error) {}
  });
  unitMap.on('load', () => {
    window.NLPJX_MAP = unitMap;
    document.dispatchEvent(new CustomEvent('nlpjx:map', { detail: { map: unitMap } }));
    drawEnvironmentLayers();
    updateUnitMap();
  });
  const model = $('#building-model');
  if (model && !model.dataset.mapSync) {
    model.dataset.mapSync = '1';
    model.addEventListener('camera-change', (event) => {
      if (event.detail?.source !== 'user-interaction' || !unitMap || typeof model.getCameraOrbit !== 'function') return;
      try { unitMap.setBearing(-(model.getCameraOrbit().theta * 180 / Math.PI) % 360); } catch (error) {}
    });
  }
}

function updateUnitMap() {
  const unit = selectedUnit();
  $('#map-unit-label').textContent = `${unit.label} · ${unit.rooms} חד׳`;
  $('#map-unit-direction').textContent = `${unit.dir} · ${unit.view} · קומה ${unit.floor}`;
  if (!unitMap || !window.mapboxgl || !data.project) return;
  const bearing = Number(unit.directionAzimuth) + state.lookOffset;
  showViewCone(bearing);
  try { unitMap.easeTo({ center: [data.project.position.lng, data.project.position.lat], zoom: 15.5, pitch: 45, bearing, duration: 900 }); } catch (error) {}
}

function showViewCone(bearing) {
  if (!unitMap || !window.mapboxgl) return;
  try {
    if (!unitViewCone) {
      const element = document.createElement('div');
      element.className = 'unit-view-cone';
      element.innerHTML = '<svg width="150" height="150" viewBox="0 0 150 150" aria-hidden="true"><defs><linearGradient id="aurelia-cone-g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C2563A" stop-opacity="0"/><stop offset="1" stop-color="#C2563A" stop-opacity="0.62"/></linearGradient></defs><path d="M75 75 L44 8 A78 78 0 0 1 106 8 Z" fill="url(#aurelia-cone-g)" stroke="#C2563A" stroke-opacity="0.55" stroke-width="1.5"/></svg>';
      unitViewCone = new mapboxgl.Marker({ element, rotationAlignment: 'map', pitchAlignment: 'map', anchor: 'center' }).setLngLat([data.project.position.lng, data.project.position.lat]);
    }
    unitViewCone.setRotation(bearing).addTo(unitMap);
  } catch (error) {}
}

function drawEnvironmentLayers() {
  if (!unitMap || !window.mapboxgl) return;
  environmentLayers.forEach((marker) => marker.remove());
  environmentLayers = [];
  const visible = data.environment.filter((point) => state.environmentCategory === 'all' || point.category === state.environmentCategory);
  visible.forEach((point) => {
    const popup = new mapboxgl.Popup({ offset: 16 }).setHTML(`<b>${safe(point.label)}</b><br><span>${point.walkMin ? `${point.walkMin} דק׳ הליכה` : `${point.bikeMin} דק׳ אופניים`}</span>`);
    const marker = new mapboxgl.Marker({ color: '#C2563A', scale: .72 }).setLngLat([point.lng, point.lat]).setPopup(popup).addTo(unitMap);
    marker.getElement().addEventListener('click', () => { state.selectedEnvironmentId = point.id; renderEnvironment(); });
    environmentLayers.push(marker);
  });
}

function panoSceneConfig(scene) {
  return {
    type: 'equirectangular',
    panorama: `assets/${scene.asset}`,
    yaw: scene.initialYaw,
    pitch: scene.initialPitch,
    hfov: scene.hfov,
    hotSpots: scene.specs.map((spot) => spot.type === 'scene' ? { pitch: spot.pitch, yaw: spot.yaw, type: 'scene', text: spot.label, sceneId: spot.target, targetYaw: spot.targetYaw } : { pitch: spot.pitch, yaw: spot.yaw, type: 'info', text: `${spot.label} · ${spot.text}` })
  };
}

function renderInteriorScenes() {
  $('#interior-scenes').innerHTML = data.interiorScenes.map((scene) => `<button class="${scene.id === 'living' ? 'active' : ''}" data-interior-scene="${scene.id}">${safe(scene.label)}</button>`).join('');
  $$('#interior-scenes [data-interior-scene]').forEach((button) => button.addEventListener('click', () => { interiorViewer?.loadScene(button.dataset.interiorScene); $$('#interior-scenes button').forEach((item) => item.classList.toggle('active', item === button)); $('#interior-room').textContent = `${button.textContent} · ${selectedUnit().view}`; }));
}

function ensureInteriorViewer() {
  if (!window.pannellum || interiorViewer || !$('#interior-viewer')) return;
  const scenes = Object.fromEntries(data.interiorScenes.map((scene) => [scene.id, panoSceneConfig(scene)]));
  interiorViewer = pannellum.viewer('interior-viewer', { default: { firstScene: 'living', autoLoad: true, sceneFadeDuration: 700 }, scenes });
}

function ensureFacilityViewer() {
  if (!window.pannellum || !$('#facility-viewer')) return;
  const facility = data.facilities.find((item) => item.id === state.selectedFacilityId) ?? data.facilities[0];
  facilityViewer?.destroy();
  facilityViewer = null;
  const container = $('#facility-viewer');
  container.innerHTML = '';
  container.classList.toggle('is-static', !facility.panorama);
  if (facility.panorama) {
    facilityViewer = pannellum.viewer('facility-viewer', { type: 'equirectangular', panorama: `assets/${facility.panorama}`, autoLoad: true, yaw: -12, pitch: -2, hfov: 100, hotSpots: facility.equipment.slice(0, 4).map((item, index) => ({ pitch: -12 + index * 6, yaw: -55 + index * 35, type: 'info', text: item })) });
  } else {
    container.innerHTML = `<div class="facility-static"><img src="assets/${data.project.assets.amenities}" alt="${safe(facility.label)}"><span>בחרו את המתקן בתוכנית כדי לראות את כל הנתונים שלו</span></div>`;
  }
}

function changePlanZoom(action) {
  planZoom = action === 'in' ? Math.min(2.2, planZoom + .2) : action === 'out' ? Math.max(.7, planZoom - .2) : 1;
  $('#plan-image').style.transform = `scale(${planZoom})`;
}

function renderStudioCatalog() {
  const items = data.studioCatalog.filter((item) => item.category === state.studioCategory);
  $('#studio-catalog').innerHTML = items.map((item) => `<button class="${item.id === state.selectedStudioItemId ? 'active' : ''}" data-studio-item="${safe(item.id)}"><b>${safe(item.label)}</b><code>${safe(item.code)}</code><small>${safe(item.spec)}</small></button>`).join('');
  $$('#studio-catalog [data-studio-item]').forEach((button) => button.addEventListener('click', () => { state.selectedStudioItemId = button.dataset.studioItem; renderStudioCatalog(); const item = data.studioCatalog.find((entry) => entry.id === state.selectedStudioItemId); $('#studio-selection').textContent = `${item.code} · ${item.label} · לחצו על התוכנית למיקום`; }));
}

function addStudioAnnotation(event) {
  if (event.target.closest('button') || event.target.closest('#studio-annotations')) return;
  const rect = $('#studio-canvas').getBoundingClientRect();
  const item = data.studioCatalog.find((entry) => entry.id === state.selectedStudioItemId);
  if (!item) return;
  state.studioHistory.push([...state.studioItems]);
  state.studioItems.push({ instanceId: `${item.id}-${Date.now()}`, itemId: item.id, code: item.code, label: item.label, impact: item.impact, unit: item.unit, quantity: item.defaultQuantity, x: Math.max(2, Math.min(98, ((event.clientX - rect.left) / rect.width) * 100)), y: Math.max(2, Math.min(98, ((event.clientY - rect.top) / rect.height) * 100)), unitId: state.selectedUnitId });
  state.studioVersion += 1;
  renderStudioState();
}

function renderStudioState() {
  $('#studio-annotations').innerHTML = state.studioItems.map((item, index) => `<button class="studio-pin" style="left:${item.x}%;top:${item.y}%" title="${safe(item.label)}" data-studio-remove="${item.instanceId}">${index + 1}</button>`).join('');
  $$('#studio-annotations [data-studio-remove]').forEach((button) => button.addEventListener('click', (event) => { event.stopPropagation(); state.studioHistory.push([...state.studioItems]); state.studioItems = state.studioItems.filter((item) => item.instanceId !== button.dataset.studioRemove); state.studioVersion += 1; renderStudioState(); }));
  $('#studio-count').textContent = state.studioItems.length;
  $('#studio-impact-count').textContent = new Set(state.studioItems.map((item) => item.impact)).size;
  $('#studio-version').textContent = state.studioVersion;
  $('#studio-summary').innerHTML = state.studioItems.map((item, index) => `<li><b>${index + 1}. ${safe(item.code)}</b><span>${safe(item.label)} · ${safe(item.unit)}</span></li>`).join('') || '<li>המפרט יתמלא כאן לפי המיקומים בתוכנית.</li>';
}

function undoStudioItem() {
  if (!state.studioHistory.length) return;
  state.studioItems = state.studioHistory.pop();
  state.studioVersion += 1;
  renderStudioState();
}

function clearStudioItems() {
  if (!state.studioItems.length) return;
  state.studioHistory.push([...state.studioItems]);
  state.studioItems = [];
  state.studioVersion += 1;
  renderStudioState();
}

function openDialog(type) {
  const unit = selectedUnit();
  const titles = { lead: 'קבלת תוכניות ומחירים', meeting: 'בחירת מועד לשיחה', cotour: 'צפייה משותפת בפרויקט' };
  $('#dialog-title').textContent = titles[type] ?? titles.lead;
  $('#dialog-kicker').textContent = type === 'cotour' ? 'CO-TOUR' : 'AURELIA SDE DOV';
  $('#dialog-context').innerHTML = `<b>${safe(unit.label)} · קומה ${unit.floor} · ${unit.rooms} חדרים</b><br>${unit.sqm} מ״ר + מרפסת ${unit.balcony} מ״ר · ${safe(unit.dir)} · ${formatPrice(unit.price)}<br><small>התוכנית, הנוף והבחירות שלכם יצורפו לבקשה.</small>`;
  $('#decision-form').hidden = false;
  $('.dialog-success').hidden = true;
  $('#dialog').hidden = false;
  $('.dialog-close').focus();
}

function closeDialog() {
  $('#dialog').hidden = true;
}

function submitDecision(event) {
  event.preventDefault();
  const unit = selectedUnit();
  const payload = {
    project: data.project.id,
    wp_id: 7304,
    unit: unit.id,
    scene: state.scene,
    plan: unit.plan_id,
    language: state.language,
    price: unit.price,
    studio_category: state.studioCategory,
    studio_version: state.studioVersion,
    studio_items: state.studioItems.map((item) => ({ code: item.code, item_id: item.itemId, quantity: item.quantity, unit: item.unit, x: Number(item.x.toFixed(2)), y: Number(item.y.toFixed(2)) })),
    studio_notes: $('#studio-notes').value,
    endpoint: data.wordpress.runtimeContract.endpoints[0]
  };
  $('#decision-form').hidden = true;
  $('.dialog-success').hidden = false;
  window.AURELIA_LAST_DECISION_PAYLOAD = payload;
  $('#payload-preview').textContent = `${unit.label}, קומה ${unit.floor} · ${state.studioItems.length} בחירות מהסטודיו צורפו לבקשה.`;
}

function renderRecipe() {
  const tokenEntries = Object.entries(data.sequence.layoutTokens);
  $('#recipe-summary').innerHTML = `
    <article><small>מקטעים</small><b>${data.sequence.sections.length}</b></article>
    <article><small>רוחב דסקטופ</small><b>${data.sequence.layoutTokens.desktopMaxWidth}px</b></article>
    <article><small>שולי מובייל</small><b>${data.sequence.layoutTokens.mobileGutter}px</b></article>
    <article><small>גובה showroom</small><b>${data.sequence.layoutTokens.showroomDesktopHeight}px</b></article>
    <article><small>יעד מגע</small><b>${data.sequence.layoutTokens.controlHeight}px</b></article>`;
  $('#recipe-list').innerHTML = data.sequence.sections.map((section) => `
    <article class="recipe-item">
      <strong>${String(section.order).padStart(2, '0')}</strong>
      <div><h2>${safe(section.label)}</h2><small>#${safe(section.anchor)} · ${section.required.length} רכיבים</small></div>
      <section><b>מיקום והיגיון</b><span>${safe(section.whyHere)}</span><b>דסקטופ</b><span>${safe(section.desktop)}</span></section>
      <section><b>מובייל</b><span>${safe(section.mobile)}</span><b>SEO / המרה</b><span>${safe(section.seoRole)} ${safe(section.conversionRole)}</span></section>
    </article>`).join('');
}

function baseCheckStatus(check) {
  if (['R01', 'R12', 'R15'].includes(check.domainId)) return 'green';
  if (['R02', 'R17'].includes(check.domainId)) return 'orange';
  return 'yellow';
}

async function sha256(textValue) {
  const bytes = new TextEncoder().encode(textValue);
  const digest = await crypto.subtle.digest('SHA-256', bytes);
  return [...new Uint8Array(digest)].map((byte) => byte.toString(16).padStart(2, '0')).join('').toUpperCase();
}

async function verifyCodeEvidence() {
  const results = {};
  await Promise.all(data.codeEvidence.sources.map(async (source) => {
    try {
      const response = await fetch(source.file, { cache: 'no-store' });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const sourceText = await response.text();
      const hash = await sha256(sourceText);
      results[source.id] = {
        text: sourceText,
        hash,
        status: !source.expectedFileSha256 ? 'yellow' : hash === source.expectedFileSha256 ? 'green' : 'yellow',
        evidence: !source.expectedFileSha256 ? 'baseline טרם נחתם' : hash === source.expectedFileSha256 ? 'SHA-256 תואם' : 'הקובץ השתנה מאז ה-baseline'
      };
    } catch (error) {
      results[source.id] = { text: '', hash: '', status: 'red', evidence: `הקובץ לא נטען: ${error.message}` };
    }
  }));
  state.codeEvidenceResults = results;
  renderChecklistDashboard();
  renderCheckDetail();
}

function bindingStatus(binding) {
  const source = state.codeEvidenceResults[binding.sourceId];
  if (!source) return { status: 'yellow', evidence: 'בדיקת המקור עדיין רצה' };
  if (source.status === 'red') return { status: 'red', evidence: source.evidence };
  if (!source.text.includes(binding.criticalNeedle)) return { status: 'orange', evidence: `הקטע הקריטי נעלם מתוך ${binding.symbol}` };
  if (source.status === 'yellow') return { status: 'yellow', evidence: source.evidence };
  return { status: 'green', evidence: 'הקובץ והקטע הקריטי תואמים ל-baseline' };
}

function architectureFor(binding) {
  const architecture = data.codeEvidence.architecture;
  const keys = binding.id.includes('SOURCE') ? ['sourceFlow', 'changeDetection']
    : binding.id.includes('BUY') ? ['conversionFlow', 'selectionFlow']
      : binding.id.includes('I18N') ? ['languageFlow', 'selectionFlow']
        : binding.id.includes('MAP') ? ['mapFlow', 'selectionFlow']
          : binding.id.includes('3D') || binding.id.includes('MVUX') ? ['modelFlow', 'selectionFlow']
            : binding.id.includes('STUDIO') ? ['studioFlow', 'selectionFlow']
              : ['selectionFlow'];
  return keys.map((key) => `<section class="architecture-note"><b>${safe(key)}</b>${Object.entries(architecture[key]).map(([name, value]) => `<p><code>${safe(name)}</code> ${safe(Array.isArray(value) ? value.join(' → ') : value)}</p>`).join('')}</section>`).join('');
}

function renderCodeEvidenceCard(checkId) {
  const bindings = data.codeEvidence.bindings.filter((binding) => binding.checkIds.includes(checkId));
  if (!bindings.length) return '<section class="code-evidence empty"><b>קוד ו-wiring</b><p>לדרישה זו ייקשר מקור קאנוני בסבב המיפוי הבא.</p></section>';
  return `<section class="code-evidence"><b>קוד, wiring וארכיטקטורה</b>${bindings.map((binding) => {
    const sourceMeta = data.codeEvidence.sources.find((item) => item.id === binding.sourceId);
    const source = state.codeEvidenceResults[binding.sourceId];
    const result = bindingStatus(binding);
    const code = source?.text ? source.text.split(/\r?\n/).slice(binding.lineStart - 1, binding.lineEnd).join('\n') : binding.excerpt;
    return `<article><header><i class="light-dot ${result.status}"></i><div><strong>${safe(binding.title)}</strong><small>${safe(sourceMeta?.file)} → ${safe(binding.symbol)} → L${binding.lineStart}–${binding.lineEnd}</small></div></header><p>${safe(binding.excerpt)}</p><p><b>ראיית משתמש:</b> ${safe(binding.userProof)}</p><p><b>מצב מקור:</b> ${safe(result.evidence)}</p>${architectureFor(binding)}<details><summary>הצגת קטע הקוד הקאנוני</summary><pre><code>${safe(code)}</code></pre></details><a href="${safe(sourceMeta?.file)}" target="_blank" rel="noopener">פתיחת קובץ המקור המקומי</a></article>`;
  }).join('')}</section>`;
}

function renderChecklist() {
  $('#check-domain').innerHTML = '<option value="all">כל התחומים</option>' + data.checklist.domains.map((domain) => `<option value="${domain.id}">${domain.id} · ${safe(domain.name)}</option>`).join('');
  const modes = [...new Set(data.checklist.definitions.map((item) => item.mode))];
  $('#check-mode').innerHTML = '<option value="all">כל שיטות הבדיקה</option>' + modes.map((mode) => `<option>${safe(mode)}</option>`).join('');
  renderChecklistDashboard();
  renderChecklistRows();
}

function renderChecklistDashboard() {
  const statuses = data.checklist.definitions.map(baseCheckStatus);
  const count = (value) => statuses.filter((status) => status === value).length;
  const validationGreen = data.testResults.summary.green ?? 0;
  const evidenceBindings = data.codeEvidence.bindings.map(bindingStatus);
  const evidenceGreen = evidenceBindings.filter((item) => item.status === 'green').length;
  $('#check-dashboard').innerHTML = `
    <article><small>תחומים</small><b>${data.checklist.counts.domains}</b></article>
    <article><small>דרישות בסיס</small><b>${data.checklist.counts.baseDefinitions}</b></article>
    <article><small>מקרי מטריצה</small><b>${data.checklist.counts.expandedCases.toLocaleString('he-IL')}</b></article>
    <article><small>בדיקות נתונים ירוקות</small><b>${validationGreen}/${data.testResults.results.length}</b></article>
    <article><small>מצב דרישות</small><b><i class="light-dot green"></i>${count('green')} <i class="light-dot yellow"></i>${count('yellow')} <i class="light-dot orange"></i>${count('orange')}</b></article>
    <article><small>קוד קאנוני תואם</small><b>${evidenceGreen}/${evidenceBindings.length}</b><span>${evidenceBindings.some((item) => item.status === 'orange' || item.status === 'red') ? 'נדרש diff' : 'fingerprints פעילים'}</span></article>`;
}

function renderChecklistRows() {
  if (!data.checklist) return;
  const query = ($('#check-search')?.value ?? '').toLowerCase();
  const domain = $('#check-domain')?.value ?? 'all';
  const mode = $('#check-mode')?.value ?? 'all';
  const rows = data.checklist.definitions.filter((check) => (domain === 'all' || check.domainId === domain) && (mode === 'all' || check.mode === mode) && (!query || `${check.id} ${check.domain} ${check.title}`.toLowerCase().includes(query)));
  $('#check-list').innerHTML = rows.map((check) => `<button class="check-row ${check.id === state.selectedCheckId ? 'active' : ''}" data-check-id="${check.id}"><i class="${baseCheckStatus(check)}"></i><code>${check.id}</code><b>${safe(check.title)}</b><small>${safe(check.mode)} · ${safe(check.domain)}</small></button>`).join('');
  $$('#check-list [data-check-id]').forEach((button) => button.addEventListener('click', () => { state.selectedCheckId = button.dataset.checkId; renderChecklistRows(); renderCheckDetail(); }));
  if (!rows.some((check) => check.id === state.selectedCheckId)) state.selectedCheckId = rows[0]?.id;
  renderCheckDetail();
}

function renderCheckDetail() {
  const check = data.checklist.definitions.find((item) => item.id === state.selectedCheckId);
  if (!check) { $('#check-detail').innerHTML = '<p>לא נמצאה דרישה.</p>'; return; }
  const matrixCount = data.matrix.filter((item) => item.baseCheckId === check.id).length;
  $('#check-detail').innerHTML = `
    <small>${check.id} · ${safe(check.domain)}</small><h2>${safe(check.title)}</h2><p>מצב נוכחי: <i class="light-dot ${baseCheckStatus(check)}"></i> ${baseCheckStatus(check)} · ${matrixCount} מקרי בדיקה מפורשים.</p>
    <section><b>שיטת בדיקה</b><p>${safe(check.mode)}</p></section>
    <section><b>ראיות נדרשות</b><ul>${check.evidenceRequired.map((item) => `<li>${safe(item)}</li>`).join('')}</ul></section>
    <section><b>חיבורי WordPress</b><ul>${check.wordpressHooks.map((item) => `<li>${safe(item)}</li>`).join('')}</ul></section>
    <section><b>חוק המנגנון</b><p>${safe(check.remediationRule)}</p></section>
    ${renderCodeEvidenceCard(check.id)}`;
}

function runLocalChecks() {
  const buyer = $('[data-view="buyer"]');
  const model = $('#building-model');
  $$('.local-check-row', $('#check-list')).forEach((row) => row.remove());
  const hotspot = $('.model-hotspot.active', model) || $('.model-hotspot', model);
  const projectedHotspot = $('.projected-hotspot.active:not([hidden])') || $('.projected-hotspot:not([hidden])');
  const rect = projectedHotspot?.getBoundingClientRect();
  const hotspotStyle = projectedHotspot ? getComputedStyle(projectedHotspot) : null;
  const hotspotWidth = rect?.width || Number.parseFloat(hotspotStyle?.width || '0');
  const hotspotHeight = rect?.height || Number.parseFloat(hotspotStyle?.height || '0');
  const hotspotQuery = model?.queryHotspot && hotspot ? model.queryHotspot(hotspot.slot) : null;
  const projectedQuery = model?.queryHotspot && projectedHotspot ? model.queryHotspot(projectedHotspot.dataset.slot) : null;
  const projectedX = Number(projectedHotspot?.dataset.projectedX);
  const projectedY = Number(projectedHotspot?.dataset.projectedY);
  const projectionDelta = projectedQuery ? Math.hypot(projectedX - projectedQuery.canvasPosition.x, projectedY - projectedQuery.canvasPosition.y) : Infinity;
  const projectedSurfaceDistance = Number(projectedHotspot?.dataset.surfaceDistance);
  const selectionContracts = data.units.filter((unit) => unit.selection?.anchor?.position?.length === 3 && unit.selection?.anchor?.normal?.length === 3 && unit.selection?.hitRegion && unit.selection?.legacyStageRectangle?.runtimeAllowed === false);
  const banned = ['בהמתנה לחומרי היזם', 'יחליף אותו עם קבלתו', 'בבדיקה מול היזם', 'יוצגו עם קבלת נתונים', 'מחכים ליזם', '0 חדרים'];
  const checks = [
    ['LAB-DOM-001', 'H1 יחיד בעמוד הרוכש', $$('h1', buyer).length === 1, `${$$('h1', buyer).length} H1`],
    ['LAB-DOM-002', 'סדר hero → opening → progress → inventory', ['hero', 'opening', 'progress', 'inventory'].every((id, index, ids) => index === 0 || document.getElementById(ids[index - 1]).compareDocumentPosition(document.getElementById(id)) & Node.DOCUMENT_POSITION_FOLLOWING), 'DOM order'],
    ['LAB-UNIT-003', 'יחידה נבחרת קיימת במלאי', data.units.some((unit) => unit.id === state.selectedUnitId), state.selectedUnitId],
    ['LAB-PLAN-004', 'תוכנית היחידה מחוברת ל-plan_id', data.drawings.some((item) => item.id === selectedUnit().plan_id), selectedUnit().plan_id],
    ['LAB-TOUCH-005', 'hotspot פעיל בגודל 44px לפחות', hotspotWidth >= 44 && hotspotHeight >= 44, `${Math.round(hotspotWidth)}×${Math.round(hotspotHeight)} CSS/rendered`],
    ['LAB-SCENE-006', 'שישה מצבי showroom קיימים', $$('[data-scene-panel]', buyer).length === 6, `${$$('[data-scene-panel]', buyer).length} scenes`],
    ['LAB-COPY-007', 'אין טקסטי המתנה ברשימה השחורה', banned.every((phrase) => !buyer.innerText.includes(phrase)), 'buyer visible text scan'],
    ['LAB-PRICE-008', 'מחיר הדירה מופיע בכרטיס הנבחר', $('#unit-card').innerText.includes(formatPrice(selectedUnit().price)), formatPrice(selectedUnit().price)],
    ['LAB-RUNTIME-009', 'NADLAN_SHOWROOM מחזיק את אותו unit ID', window.NADLAN_SHOWROOM.projects[0].units.some((unit) => unit.id === state.selectedUnitId), state.selectedUnitId],
    ['LAB-MOBILE-010', 'אין גלילה אופקית ברוחב הנוכחי', document.documentElement.scrollWidth <= document.documentElement.clientWidth + 1, `${document.documentElement.scrollWidth}/${document.documentElement.clientWidth}`],
    ['LAB-3D-011', 'מודל GLB נטען וה-hotspot הוא ילד ישיר שלו', Boolean((model?.loaded === true || model?.modelIsVisible === true) && hotspot?.parentElement === model), `${model?.loaded || model?.modelIsVisible ? 'model loaded' : 'model not ready'} · ${hotspot?.slot || 'no slot'}`],
    ['LAB-ANCHOR-012', 'hotspot מחזיק position ו-normal תלת־ממדיים', Boolean(hotspot?.dataset.position && hotspot?.dataset.normal), `${hotspot?.dataset.position || 'missing'} / ${hotspot?.dataset.normal || 'missing'}`],
    ['LAB-ANCHOR-012B', 'model-viewer מזהה את ה-hotspot בתוך מערכת הקואורדינטות', Boolean(hotspotQuery), hotspotQuery ? `canvas ${Math.round(hotspotQuery.canvasPosition.x)},${Math.round(hotspotQuery.canvasPosition.y)} · facing ${hotspotQuery.facingCamera}` : 'queryHotspot returned null'],
    ['LAB-ANCHOR-012C', 'כפתור הבחירה מוקרן מאותה נקודת תלת־ממד ולא ממיקום CSS ידני', projectionDelta <= 1, Number.isFinite(projectionDelta) ? `projection delta ${projectionDelta.toFixed(2)}px` : 'no matching projection'],
    ['LAB-CLICK-012D', 'קליק hotspot אמיתי בחר ושמר את אותה יחידה', Boolean(state.hotspotClickProof && state.hotspotClickProof.requestedUnitId === state.hotspotClickProof.selectedUnitId && state.hotspotClickProof.requestedUnitId === state.hotspotClickProof.urlUnitId), state.hotspotClickProof ? `${state.hotspotClickProof.requestedUnitId} → state + URL` : 'טרם בוצע קליק hotspot בדפדפן'],
    ['LAB-CONTRACT-012E', 'לכל יחידה anchor, normal, hit region ואיסור runtime על stage_x/y', selectionContracts.length === data.units.length, `${selectionContracts.length}/${data.units.length} unit contracts`],
    ['LAB-OCCLUSION-012F', 'hotspot נראה רק כשההקרנה קרובה למשטח הפומבי', Number.isFinite(projectedSurfaceDistance) && projectedSurfaceDistance <= 4, Number.isFinite(projectedSurfaceDistance) ? `${projectedSurfaceDistance.toFixed(2)}m surface delta` : 'no visible surface probe'],
    ['LAB-SURFACE-012G', 'קליק על גוף המודל נפתר ליחידה באותו hit region', Boolean(state.surfacePickProof && state.surfacePickProof.requestedUnitId === state.surfacePickProof.selectedUnitId && state.surfacePickProof.requestedUnitId === state.surfacePickProof.urlUnitId), state.surfacePickProof ? `${state.surfacePickProof.requestedUnitId} · ${state.surfacePickProof.distanceM.toFixed(2)}m · dot ${state.surfacePickProof.normalDot.toFixed(2)}` : 'טרם בוצע קליק surface בדפדפן'],
    ['LAB-SURFACE-012H', 'קליק המשטח מחזיר נקודת פגיעה תלת־ממדית', Boolean(state.surfacePickAttempt?.hit), state.surfacePickAttempt ? `${state.surfacePickAttempt.hit ? state.surfacePickAttempt.hit.position.map((value) => value.toFixed(2)).join(', ') : 'no hit'} · ${state.surfacePickAttempt.matchedUnitId || 'no unit'}` : 'טרם בוצע ניסיון surface בדפדפן'],
    ['LAB-URL-013', 'מזהה היחידה נשמר בכתובת', new URL(location.href).searchParams.get('unit_id') === state.selectedUnitId, new URL(location.href).searchParams.get('unit_id') || 'missing'],
    ['LAB-MAP-014', 'מפת Mapbox החיה ואלומת הכיוון הקאנונית קיימות', Boolean(unitMap && unitViewCone && window.NLPJX_MAP === unitMap), `${unitMap ? 'Mapbox mounted' : 'map missing'} · ${unitViewCone ? 'view cone mounted' : 'cone missing'}`],
    ['LAB-PANO-015', 'סיור פנים 360 עובד עם יותר מחלל אחד', Boolean(interiorViewer && data.interiorScenes.length > 1), `${data.interiorScenes.length} scenes`],
    ['LAB-FAC-016', 'מתקנים מחזיקים מיקום, תפעול, נגישות וציוד', data.facilities.every((item) => item.hotspot?.length === 2 && item.equipment?.length && item.operations?.length && item.accessibility), `${data.facilities.length}/${data.facilities.length} complete`],
    ['LAB-STUDIO-017', 'קטלוג הסטודיו מחזיק קוד BOM ומיקום אינטראקטיבי', data.studioCatalog.every((item) => item.code && item.category && item.impact), `${data.studioCatalog.length} catalog items`]
  ].map(([id, title, pass, evidence]) => ({ id, title, pass, status: pass ? 'green' : 'red', evidence }));
  state.localChecks = checks;
  const green = checks.filter((item) => item.pass).length;
  $('#run-local-checks').textContent = `${green}/${checks.length} ירוקות`;
  const summary = document.createElement('article');
  summary.innerHTML = `<small>בדיקות DOM מקומיות</small><b>${green}/${checks.length}</b>`;
  $('#check-dashboard').append(summary);
  const localMarkup = checks.map((item) => `<button class="check-row local-check-row"><i class="${item.status}"></i><code>${item.id}</code><b>${safe(item.title)}</b><small>${safe(item.evidence)}</small></button>`).join('');
  $('#check-list').insertAdjacentHTML('afterbegin', localMarkup);
}

function renderBom() {
  $('#bom-systems').innerHTML = data.bom.systems.map((system) => {
    const components = system.assemblies.reduce((sum, assembly) => sum + assembly.components.length, 0);
    return `<button class="${system.id === state.selectedBomId ? 'active' : ''}" data-system-id="${system.id}"><b>${system.id}</b><span>${safe(system.name)}</span><small>${system.assemblies.length} מכלולים · ${components} רכיבים</small></button>`;
  }).join('');
  $$('#bom-systems [data-system-id]').forEach((button) => button.addEventListener('click', () => { state.selectedBomId = button.dataset.systemId; renderBom(); }));
  const system = data.bom.systems.find((item) => item.id === state.selectedBomId) ?? data.bom.systems[0];
  $('#bom-detail').innerHTML = `<small>${system.id}</small><h2>${safe(system.name)}</h2><p class="bom-public"><b>${safe(system.publicTitle)}</b><br>${safe(system.publicSummary)}</p>` + system.assemblies.map((assembly) => `
    <section class="assembly"><h3>${assembly.id} · ${safe(assembly.name)}</h3><table class="component-table"><thead><tr><th>קוד / רכיב</th><th>מפרט</th><th>יחידה וכמות</th><th>ביצועים</th><th>בדיקה ותחזוקה</th></tr></thead><tbody>${assembly.components.map((component) => `<tr><td><code>${safe(component.code)}</code><br><b>${safe(component.item)}</b></td><td>${safe(component.spec)}</td><td>${safe(component.unit)}<br>${safe(component.quantityBasis)}</td><td>${safe(component.performance)}</td><td>${safe(component.qa)}<br>${safe(component.maintenance)}</td></tr>`).join('')}</tbody></table></section>`).join('');
}

function renderSeo() {
  const seo = data.seo;
  $('#seo-panel').innerHTML = `
    <section class="serp-card"><small>nad-lan.co.il › projects › aurelia-sde-dov</small><h2>${safe(seo.serp.title)}</h2><p>${safe(seo.serp.metaDescription)}</p></section>
    <div class="seo-grid">
      <section><h3>בעל הבית והביטויים</h3><p><b>${safe(seo.primaryKeyword)}</b></p><ul>${seo.supportingKeywords.map((item) => `<li>${safe(item)}</li>`).join('')}</ul></section>
      <section><h3>H1 ופתיח</h3><code>${safe(seo.serp.h1)}</code><ul>${seo.openingParagraphMustAnswer.map((item) => `<li>${safe(item)}</li>`).join('')}</ul></section>
      <section><h3>מבנה כותרות</h3><ul>${seo.headingPlan.map((item) => `<li><b>${item.level}</b> ${safe(item.text)} — ${safe(item.intent)}</li>`).join('')}</ul></section>
      <section><h3>חלוקת ישויות</h3><ul>${seo.entityOwnership.map((item) => `<li><b>${safe(item.entity)}</b> → ${safe(item.owner)} → ${item.linksTo.map(safe).join(', ')}</li>`).join('')}</ul></section>
      <section class="full"><h3>חמש שפות</h3><ul>${seo.languages.map((item) => `<li><b>${item.code.toUpperCase()} · ${item.dir}</b> — ${safe(item.projectName)} — ${safe(item.keyword)}</li>`).join('')}</ul></section>
    </div>`;
}

function renderSelectionAudit() {
  const audit = data.selectionAudit;
  const groups = [...new Set(audit.checks.map((check) => check.group))];
  const deviceCases = audit.deviceMatrix.reduce((sum, item) => sum + item.orientations.length, 0);
  const replayCases = audit.checks.length * data.units.length * deviceCases * data.seo.languages.length;
  $('#selection-panel').innerHTML = `
    <div class="selection-summary">
      <article><small>בדיקות אטומיות</small><b>${audit.checks.length}</b><span>למנגנון הבחירה בלבד</span></article>
      <article><small>יחידות</small><b>${data.units.length}</b><span>anchor + hit region</span></article>
      <article><small>מסלולי runtime</small><b>${audit.runtimeAdapters.length}</b><span>קיים + סמנטי</span></article>
      <article><small>מקרי replay</small><b>${replayCases.toLocaleString('en-US')}</b><span>יחידה × בדיקה × מכשיר × שפה</span></article>
    </div>
    <section class="selection-chain"><h2>שרשרת הזהות הקאנונית</h2><ol>${audit.authoritativeChain.map((item) => `<li>${safe(item)}</li>`).join('')}</ol></section>
    <div class="selection-adapters">${audit.runtimeAdapters.map((adapter) => `<article><small>${safe(adapter.id)}</small><h2>${safe(adapter.name)}</h2><p>${safe(adapter.use)}</p><code>${safe(adapter.file)}</code></article>`).join('')}</div>
    <div class="selection-groups">${groups.map((group) => `<section><header><h2>${safe(group)}</h2><span>${audit.checks.filter((check) => check.group === group).length} בדיקות</span></header>${audit.checks.filter((check) => check.group === group).map((check) => `<article><i class="light-dot ${safe(check.failLight)}"></i><div><code>${safe(check.id)}</code><b>${safe(check.title)}</b><small>${safe(check.method)} · ראיה: ${safe(check.evidence)}</small><p>${check.code.map((file) => `<code>${safe(file)}</code>`).join(' ')}</p></div></article>`).join('')}</section>`).join('')}</div>`;
}

async function renderSourceAudit() {
  const panel = $('#source-panel');
  const audit = data.htmlSource;
  const snapshot = audit.snapshots[0];
  panel.innerHTML = `<div class="selection-summary"><article><small>detectors</small><b>${audit.detectors.length}</b><span>raw + rendered</span></article><article><small>raw source</small><b>${snapshot.bytes.toLocaleString('en-US')}</b><span>bytes</span></article><article><small>scripts / styles</small><b>${snapshot.parsed.scriptTags}/${snapshot.parsed.styleTags}</b><span>Rainbow snapshot</span></article><article><small>fingerprint</small><b>…${snapshot.fingerprints.fullSourceSha256.slice(-8)}</b><span>SHA-256</span></article></div><div id="source-runtime-proof" class="source-proof"><p>מחשב fingerprint ומפרק את ה־View Source השמור…</p></div><div class="source-findings">${audit.floatingFindings.map((finding) => `<article><i class="light-dot ${safe(finding.light)}"></i><div><small>${safe(finding.scope)} · ${safe(finding.owner)}</small><h2>${safe(finding.title)}</h2><p>${safe(finding.effect)}</p><ul>${finding.evidence.map((item) => `<li>${safe(item)}</li>`).join('')}</ul><b>פעולה:</b> ${safe(finding.nextAction)}</div></article>`).join('')}</div><div class="source-detectors">${audit.detectors.map((detector) => `<article><code>${safe(detector.id)}</code><b>${safe(detector.label)}</b><small>${safe(detector.layer)} · ${safe(detector.scope)}</small><p>${safe(detector.rule)}</p></article>`).join('')}</div>`;
  try {
    const response = await fetch(snapshot.sourceFile, { cache: 'no-store' });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const sourceText = await response.text();
    const sourceHash = await sha256(sourceText);
    const parsed = new DOMParser().parseFromString(sourceText, 'text/html');
    const duplicateIds = [...parsed.querySelectorAll('[id]')].map((node) => node.id).filter((id, index, ids) => ids.indexOf(id) !== index);
    const currentRaw = await (await fetch('index.html', { cache: 'no-store' })).text();
    const currentRawHash = await sha256(currentRaw);
    const renderedHash = await sha256(document.documentElement.outerHTML);
    const pass = sourceHash === snapshot.fingerprints.fullSourceSha256;
    $('#source-runtime-proof').innerHTML = `<h2><i class="light-dot ${pass ? 'green' : 'yellow'}"></i> View Source שמור ${pass ? 'תואם ל־baseline' : 'השתנה'}</h2><dl><div><dt>Rainbow full source</dt><dd><code>${sourceHash}</code></dd></div><div><dt>Lab raw response</dt><dd><code>${currentRawHash}</code></dd></div><div><dt>Lab rendered DOM</dt><dd><code>${renderedHash}</code></dd></div></dl><p>${parsed.title} · canonical ${parsed.querySelectorAll('link[rel="canonical"]').length} · H1 ${parsed.querySelectorAll('h1').length} · favicon ${parsed.querySelectorAll('link[rel~="icon"],link[rel="apple-touch-icon"]').length} · JSON-LD ${parsed.querySelectorAll('script[type="application/ld+json"]').length} · scripts ${parsed.scripts.length} · duplicate IDs ${new Set(duplicateIds).size}</p>`;
  } catch (error) {
    $('#source-runtime-proof').innerHTML = `<h2><i class="light-dot red"></i> לא ניתן לקרוא את snapshot המקור</h2><p>${safe(error.message)}</p>`;
  }
}

function renderWordPress() {
  const runtime = data.wordpress.runtimeContract;
  const metaKeys = Object.keys(data.wordpress.meta).filter((key) => !Array.isArray(data.wordpress.meta[key])).slice(0, 24);
  $('#wordpress-panel').innerHTML = `<div class="wp-grid">
    <section class="wp-card"><h2>Runtime</h2><code>${safe(runtime.global)}\nproject: ${safe(runtime.projectSlug)}\npost type: ${safe(data.wordpress.post_type)}\npost status: ${safe(data.wordpress.post_status)}</code></section>
    <section class="wp-card"><h2>סקריפטים קיימים</h2><ul>${runtime.requiredScripts.map((item) => `<li>${safe(item)}</li>`).join('')}</ul></section>
    <section class="wp-card"><h2>Endpoints קיימים</h2><ul>${runtime.endpoints.map((item) => `<li><code>${safe(item)}</code></li>`).join('')}<li><code>${safe(runtime.cotourQuery)}</code></li></ul></section>
    <section class="wp-card"><h2>חוזה יחידה</h2><code>{ id, floor, rooms, sqm, balcony, dir, directionAzimuth, price, plan_id, tour_url, hotspot_position, camera_orbit }</code><p>${safe(runtime.rule)}</p></section>
    <section class="wp-card full"><h2>שדות WordPress</h2><ul>${metaKeys.map((key) => `<li><code>${safe(key)}</code> → ${safe(typeof data.wordpress.meta[key] === 'object' ? JSON.stringify(data.wordpress.meta[key]) : data.wordpress.meta[key])}</li>`).join('')}</ul></section>
    <section class="wp-card full"><h2>אפשרויות מימוש וה־fallback</h2><ul>${data.options.features.map((feature) => `<li><b>${safe(feature.id)}</b> — ${safe(feature.recommended)}<br><small>Fallback: ${safe(feature.fallback)}</small></li>`).join('')}</ul></section>
  </div>`;
}

loadData().catch((error) => {
  document.body.innerHTML = `<main style="max-width:760px;margin:10vh auto;padding:30px;font-family:Arial"><h1>Recipe Lab could not load its data</h1><p>${safe(error.message)}</p><p>Open the lab through its local server so the JSON contracts can be loaded.</p></main>`;
});
