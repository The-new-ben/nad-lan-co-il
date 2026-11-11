// A stand-in navigator.xr for testing roomscan.js on a computer with no phone. It provides ONLY what the module uses:
// isSessionSupported, requestSession (immersive-ar, hit-test, dom-overlay, anchors), reference spaces, a hit-test source,
// a frame loop whose hit results follow a script (mock.aim(x, z) in world metres), anchors, and end().
// The camera picture is a dark screen; the module's 3D marks are drawn on the real WebGL canvas behind the overlay.
// Built against the WebXR Device API, the Hit Test and Anchors modules and DOM Overlays (immersive-web), and what
// three.js r170 WebXRManager calls (makeXRCompatible, XRWebGLLayer path when renderState.layers is undefined).
//
// Faults it can play: mock.lost (tracking lost: emulated position, no hits), mock.table (a surface 70 cm above the floor),
// mock.noHit (no surface found, the viewer still tracked), and DRIFT: the device's world frame creeps as the person walks
// (2 mm and 1.5 mm a second, so 6 to 8 cm over a walk). Hits, the viewer and every anchor are reported in the CURRENT
// frame, as on a phone: corners read back from their anchors stay true to each other; corners kept as first marked do not.
export function installXrMock({ mode = 'ok', floor = -1.4 } = {}) {
  const st = { mode, drift: true, aim: null, lost: false, table: false, noHit: false, frames: 0, anchors: [], session: null, ended: false, hitCancelled: false, requested: null, k: 0 };
  if (mode === 'noxr') { Object.defineProperty(navigator, 'xr', { value: undefined, configurable: true }); return st; }
  for (const G of [window.WebGL2RenderingContext, window.WebGLRenderingContext]) if (G) G.prototype.makeXRCompatible = function () { return Promise.resolve(); };
  const dpr = window.devicePixelRatio || 1;
  window.XRWebGLLayer = class {
    constructor(session, gl) {
      const c = gl.canvas; c.width = Math.round(innerWidth * dpr); c.height = Math.round(innerHeight * dpr);
      c.style.cssText = 'position:fixed;left:0;top:0;width:100vw;height:100vh;z-index:2147482000;background:#1d252c'; // the camera picture, under the overlay
      document.body.prepend(c); st.canvas = c;
      this.framebuffer = null; this.framebufferWidth = c.width; this.framebufferHeight = c.height; this.antialias = true; this.ignoreDepthValues = false;
    }
    getViewport() { return { x: 0, y: 0, width: this.framebufferWidth, height: this.framebufferHeight }; }
  };
  if (typeof window.XRRigidTransform === 'undefined') window.XRRigidTransform = class { constructor(p, o) { this.position = { x: p.x || 0, y: p.y || 0, z: p.z || 0, w: 1 }; this.orientation = o || { x: 0, y: 0, z: 0, w: 1 }; } };

  // ---- the phone: always 1.35 m above the floor and 0.9 m back from the point it aims at, looking at it ----
  const norm = (v) => { const l = Math.hypot(...v); return v.map((x) => x / l); };
  const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
  function quatFromBasis(X, Y, Z) { // columns X, Y, Z of a rotation matrix
    const m00 = X[0], m11 = Y[1], m22 = Z[2], tr = m00 + m11 + m22; let x, y, z, w;
    if (tr > 0) { const s = Math.sqrt(tr + 1) * 2; w = s / 4; x = (Y[2] - Z[1]) / s; y = (Z[0] - X[2]) / s; z = (X[1] - Y[0]) / s; }
    else if (m00 > m11 && m00 > m22) { const s = Math.sqrt(1 + m00 - m11 - m22) * 2; w = (Y[2] - Z[1]) / s; x = s / 4; y = (Y[0] + X[1]) / s; z = (Z[0] + X[2]) / s; }
    else if (m11 > m22) { const s = Math.sqrt(1 + m11 - m00 - m22) * 2; w = (Z[0] - X[2]) / s; x = (Y[0] + X[1]) / s; y = s / 4; z = (Z[1] + Y[2]) / s; }
    else { const s = Math.sqrt(1 + m22 - m00 - m11) * 2; w = (X[1] - Y[0]) / s; x = (Z[0] + X[2]) / s; y = (Z[1] + Y[2]) / s; z = s / 4; }
    return { x, y, z, w };
  }
  const xf = (pos, q, X, Y, Z) => ({ position: { x: pos[0], y: pos[1], z: pos[2], w: 1 }, orientation: q, matrix: new Float32Array([X[0], X[1], X[2], 0, Y[0], Y[1], Y[2], 0, Z[0], Z[1], Z[2], 0, pos[0], pos[1], pos[2], 1]) });
  const flatXf = (p) => xf(p, { x: 0, y: 0, z: 0, w: 1 }, [1, 0, 0], [0, 1, 0], [0, 0, 1]);
  function viewer() {
    const t = st.aim ? [st.aim[0], floor, st.aim[1]] : [0, floor, -1.2];
    const pos = [t[0] + 0.25, floor + 1.35, t[2] + 0.9], f = norm([t[0] - pos[0], t[1] - pos[1], t[2] - pos[2]]);
    const Z = f.map((v) => -v), X = norm(cross([0, 1, 0], Z)), Y = cross(Z, X);
    return xf(moved(pos), quatFromBasis(X, Y, Z), X, Y, Z);
  }
  function proj() {
    const fy = 1 / Math.tan((62 * Math.PI) / 360), a = innerWidth / innerHeight, n = 0.05, f = 60;
    return new Float32Array([fy / a, 0, 0, 0, 0, fy, 0, 0, 0, 0, (f + n) / (n - f), -1, 0, 0, (2 * f * n) / (n - f), 0]);
  }
  const drift = () => { if (st.drift === false || !st.t0) return [0, 0, 0]; const s = (performance.now() - st.t0) / 1000; return [0.002 * s, 0, -0.0015 * s]; };
  const moved = (p) => { const d = drift(); return [p[0] + d[0], p[1] + d[1], p[2] + d[2]]; };

  function frame(session) {
    st.frames++;
    const live = st.anchors.filter((a) => !a.deleted);
    return {
      session,
      trackedAnchors: new Set(live),
      getViewerPose() {
        const transform = viewer();
        return { transform, emulatedPosition: !!st.lost, views: [{ eye: 'none', projectionMatrix: proj(), transform, recommendedViewportScale: null }] };
      },
      getHitTestResults() {
        if (st.lost || st.noHit || !st.aim) return [];
        const truth = st.table ? [st.aim[0], floor + 0.7, st.aim[1]] : [st.aim[0], floor, st.aim[1]], p = moved(truth);
        return [{
          getPose() { return { transform: flatXf(p), emulatedPosition: false }; },
          createAnchor() { const a = { truth, deleted: false, delete() { this.deleted = true; } }; a.anchorSpace = { _a: a }; st.anchors.push(a); return Promise.resolve(a); },
        }];
      },
      getPose(space) {
        const a = space && space._a; if (!a || a.deleted) return null;
        return { transform: flatXf(moved(a.truth)), emulatedPosition: false };
      },
      createAnchor(t) { const d = drift(), a = { truth: [t.position.x - d[0], t.position.y - d[1], t.position.z - d[2]], deleted: false, delete() { this.deleted = true; } }; a.anchorSpace = { _a: a }; st.anchors.push(a); return Promise.resolve(a); },
    };
  }

  class Session extends EventTarget {
    constructor(features) {
      super();
      this.renderState = { baseLayer: null, depthNear: 0.1, depthFar: 1000, inlineVerticalFieldOfView: null };
      this.enabledFeatures = features; this.domOverlayState = { type: 'screen' }; this.inputSources = []; this.environmentBlendMode = 'alpha-blend'; this.visibilityState = 'visible';
      this._raf = new Map(); this._n = 0; this._ended = false;
    }
    updateRenderState(s) { Object.assign(this.renderState, s); }
    async requestReferenceSpace(type) { return { type, getOffsetReferenceSpace() { return this; }, addEventListener() {}, removeEventListener() {} }; }
    async requestHitTestSource(o) { st.hitSpace = o && o.space && o.space.type; return { cancel() { st.hitCancelled = true; } }; }
    requestAnimationFrame(cb) { const id = ++this._n; this._raf.set(id, window.requestAnimationFrame((t) => { this._raf.delete(id); if (!this._ended) cb(t, frame(this)); })); return id; }
    cancelAnimationFrame(id) { window.cancelAnimationFrame(this._raf.get(id)); this._raf.delete(id); }
    async end() { if (this._ended) return; this._ended = true; st.ended = true; this.dispatchEvent(new Event('end')); if (st.canvas) st.canvas.remove(); }
  }
  const SUPPORTED = ['local', 'viewer', 'hit-test', 'dom-overlay', 'anchors'];
  const xr = {
    async isSessionSupported(m) { return mode !== 'noar' && m === 'immersive-ar'; },
    async requestSession(m, init = {}) {
      st.requested = { mode: m, init: { requiredFeatures: init.requiredFeatures, optionalFeatures: init.optionalFeatures, domOverlayRoot: !!(init.domOverlay && init.domOverlay.root) } };
      if (mode === 'deny') throw new DOMException('denied', 'NotAllowedError');
      const avail = mode === 'noanchor' ? SUPPORTED.filter((f) => f !== 'anchors') : SUPPORTED;
      for (const f of init.requiredFeatures || []) if (!avail.includes(f)) throw new DOMException('feature ' + f, 'NotSupportedError');
      if ((init.requiredFeatures || []).includes('dom-overlay') && !(init.domOverlay && init.domOverlay.root && init.domOverlay.root.isConnected)) throw new DOMException('no overlay root', 'NotSupportedError');
      const feats = ['local', 'viewer', ...(init.requiredFeatures || []), ...(init.optionalFeatures || []).filter((f) => avail.includes(f))];
      st.session = new Session([...new Set(feats)]); st.t0 = performance.now();
      return st.session;
    },
  };
  Object.defineProperty(navigator, 'xr', { value: xr, configurable: true });
  return st;
}
