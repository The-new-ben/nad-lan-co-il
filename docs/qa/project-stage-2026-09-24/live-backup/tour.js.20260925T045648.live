/* The example apartment from the inside (design system ApartmentTour): a full-screen 360° viewer.
   Loaded only when the buyer asks for it (the card's button in the page). A sphere carries the panorama; the small
   picture shows first, the large one replaces it. Drag or arrow keys look around, the wheel or a pinch zooms, Esc closes.
   openTour({ src, srcSmall, title, chip, caption, hint, close, opener }) */
import * as THREE from 'three';

let cssDone = false;
function ensureCss() {
  if (cssDone || document.querySelector('link[data-nlat-css]')) { cssDone = true; return; }
  const l = document.createElement('link');
  l.rel = 'stylesheet';
  l.href = new URL('./tour.css' + new URL(import.meta.url).search, import.meta.url).href;
  l.setAttribute('data-nlat-css', '');
  document.head.appendChild(l);
  cssDone = true;
}

export function openTour(o) {
  ensureCss();
  const prevFocus = o.opener || document.activeElement; // back to the button that opened it (Safari does not focus a clicked button)
  const root = document.createElement('div');
  root.className = 'nlds nlat-viewer';
  root.dir = 'rtl';
  root.lang = 'he';
  root.setAttribute('role', 'dialog');
  root.setAttribute('aria-modal', 'true');
  root.setAttribute('aria-label', o.title || '');
  const top = document.createElement('div');
  top.className = 'nlat-viewer__top';
  const title = document.createElement('p');
  title.className = 'nlat-viewer__title';
  title.textContent = o.title || '';
  const chip = document.createElement('span');
  chip.className = 'nlds-sample';
  chip.textContent = o.chip || 'דירה לדוגמה';
  const x = document.createElement('button');
  x.type = 'button';
  x.className = 'nlat-viewer__x';
  x.setAttribute('aria-label', o.close || 'סגירה');
  x.textContent = '×';
  top.append(title, chip, x);
  const hint = document.createElement('p');
  hint.className = 'nlat-viewer__hint';
  hint.textContent = o.hint || 'גררו כדי להסתכל מסביב';
  const cap = document.createElement('p');
  cap.className = 'nlat-viewer__cap';
  cap.textContent = o.caption || '';
  const stage = document.createElement('div');
  stage.className = 'nlat-viewer__stage';
  root.append(stage, top, hint, cap);
  document.body.appendChild(root);
  document.documentElement.classList.add('nlat-open');

  const renderer = new THREE.WebGLRenderer({ antialias: false, powerPreference: 'high-performance' });
  renderer.setPixelRatio(Math.min(2, window.devicePixelRatio || 1));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  stage.appendChild(renderer.domElement);
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(72, 1, 0.1, 1200);
  const geo = new THREE.SphereGeometry(500, 96, 48);
  geo.scale(-1, 1, 1); // seen from inside
  const mat = new THREE.MeshBasicMaterial({ color: 0xffffff });
  scene.add(new THREE.Mesh(geo, mat));

  // yaw 0 looks at the panorama's centre (the window); the sphere's u = 0.5 lies on -x
  let yaw = 0, pitch = -0.05, fov = 72, vy = 0, vp = 0, raf = 0, alive = true, moved = false, dragging = false;
  const look = new THREE.Vector3();
  function render() {
    raf = 0;
    if (!alive) return;
    if (!dragging && (Math.abs(vy) > 1e-4 || Math.abs(vp) > 1e-4)) { // a little glide after the finger lifts
      yaw += vy; pitch += vp; vy *= 0.86; vp *= 0.86;
      raf = requestAnimationFrame(render);
    }
    pitch = Math.max(-1.45, Math.min(1.45, pitch));
    camera.fov = fov;
    camera.updateProjectionMatrix();
    look.set(-Math.cos(yaw) * Math.cos(pitch), Math.sin(pitch), Math.sin(yaw) * Math.cos(pitch));
    camera.lookAt(look);
    renderer.render(scene, camera);
  }
  const kick = () => { if (!raf) raf = requestAnimationFrame(render); };
  function size() {
    const w = stage.clientWidth || window.innerWidth, h = stage.clientHeight || window.innerHeight;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    kick();
  }
  const ro = new ResizeObserver(size);
  ro.observe(stage);
  size();

  const loader = new THREE.TextureLoader();
  const load = (url) => new Promise((res, rej) => loader.load(url, res, undefined, rej));
  const useTex = (t) => {
    t.colorSpace = THREE.SRGBColorSpace;
    t.anisotropy = Math.min(8, renderer.capabilities.getMaxAnisotropy());
    const old = mat.map;
    mat.map = t;
    mat.needsUpdate = true;
    if (old) old.dispose();
    root.classList.add('is-ready');
    kick();
  };
  load(o.srcSmall || o.src).then((t) => {
    if (!alive) { t.dispose(); return null; }
    useTex(t);
    return o.srcSmall && o.src && o.src !== o.srcSmall ? load(o.src) : null;
  }).then((t) => { if (t) { if (alive) useTex(t); else t.dispose(); } }).catch(() => { root.classList.add('is-error'); });

  // looking around: drag (one pointer), pinch (two), the wheel, the arrow keys
  const pts = new Map();
  let last = null, pinch0 = 0, fov0 = fov;
  // the point under the finger stays under the finger: the vertical field of view over the stage's height
  const k = () => (fov * Math.PI / 180) / Math.max(200, stage.clientHeight || window.innerHeight);
  function onDown(e) {
    pts.set(e.pointerId, { x: e.clientX, y: e.clientY });
    stage.setPointerCapture(e.pointerId);
    vy = vp = 0;
    dragging = true;
    if (pts.size === 1) last = { x: e.clientX, y: e.clientY };
    if (pts.size === 2) { const [a, b] = [...pts.values()]; pinch0 = Math.hypot(a.x - b.x, a.y - b.y); fov0 = fov; }
  }
  function onMove(e) {
    if (!pts.has(e.pointerId)) return;
    pts.set(e.pointerId, { x: e.clientX, y: e.clientY });
    if (pts.size === 2) {
      const [a, b] = [...pts.values()];
      const d = Math.hypot(a.x - b.x, a.y - b.y);
      if (pinch0 > 0) fov = Math.max(35, Math.min(90, fov0 * (pinch0 / d)));
      kick();
      return;
    }
    if (!last) return;
    const dx = e.clientX - last.x, dy = e.clientY - last.y;
    last = { x: e.clientX, y: e.clientY };
    // dragging the picture to the left turns the view to the right (the room follows the finger)
    vy = dx * k(); vp = dy * k();
    yaw += vy; pitch += vp;
    if (!moved && Math.hypot(dx, dy) > 2) { moved = true; root.classList.add('is-moved'); }
    kick();
  }
  function onUp(e) {
    pts.delete(e.pointerId);
    if (pts.size < 2) pinch0 = 0;
    if (pts.size === 0) { last = null; dragging = false; kick(); }
    else { const p = [...pts.values()][0]; last = { x: p.x, y: p.y }; }
  }
  function onWheel(e) {
    e.preventDefault();
    fov = Math.max(35, Math.min(90, fov + e.deltaY * 0.04));
    kick();
  }
  function onKey(e) {
    if (e.key === 'Escape') { e.preventDefault(); close(); return; }
    const step = 0.08;
    if (e.key === 'ArrowLeft') yaw += step;
    else if (e.key === 'ArrowRight') yaw -= step;
    else if (e.key === 'ArrowUp') pitch += step;
    else if (e.key === 'ArrowDown') pitch -= step;
    else if (e.key === 'Tab') { e.preventDefault(); x.focus(); return; } // one control in the dialog
    else return;
    e.preventDefault();
    if (!moved) { moved = true; root.classList.add('is-moved'); }
    kick();
  }
  stage.addEventListener('pointerdown', onDown);
  stage.addEventListener('pointermove', onMove);
  stage.addEventListener('pointerup', onUp);
  stage.addEventListener('pointercancel', onUp);
  stage.addEventListener('wheel', onWheel, { passive: false });
  document.addEventListener('keydown', onKey);
  x.addEventListener('click', () => close());

  function close() {
    if (!alive) return;
    alive = false;
    if (raf) cancelAnimationFrame(raf);
    ro.disconnect();
    document.removeEventListener('keydown', onKey);
    if (mat.map) mat.map.dispose();
    mat.dispose();
    geo.dispose();
    renderer.dispose();
    root.remove();
    document.documentElement.classList.remove('nlat-open');
    if (prevFocus && prevFocus.focus) prevFocus.focus();
    if (typeof o.onClose === 'function') o.onClose();
  }
  x.focus();
  const api = { close, get yaw() { return yaw; }, get pitch() { return pitch; }, get fov() { return fov; } };
  root.nlTour = api; // for the page's checks (scripts/project-stage/pagejourney.py)
  return api;
}
