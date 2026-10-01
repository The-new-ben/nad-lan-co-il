# -*- coding: utf-8 -*-
"""v104.15 (1.10.2026, loop turn 24, HAD-375): on a tablet or a computer the aerial city is framed below the floating panel.
A lens shift (the off-axis term the phone's bottom sheet already uses; three.js setViewOffset in effect): the camera, the orbit
and the zoom do not move, the perspective's centre moves down just enough that the roofs under the panel clear it by 24 px,
never pushing the towers' bases off the stage. Computed when the camera arrives in the aerial view and on every resize, never
while the user orbits. Taps (raycasts) and labels use the same projection. The flight's done() now also runs on an instant pose.
  python patch_world_10415.py"""
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
JS = os.path.join(ROOT, "plugins", "nadlan-config", "assets", "project-stage", "world", "world.js")
s = open(JS, encoding="utf-8").read()
if "v104.15" in s:
    raise SystemExit("already patched")


def sub(old, new, name, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"[{name}] anchor found {c} times")
    s = s.replace(old, new)


sub("""  let anim = null;              // camera flight""", """  let anim = null;              // camera flight
  let panelShift = 0;           // v104.15: the lens shift that frames the aerial city below the floating panel (NDC units)""", "decl")
sub("""    if (!fp && narrow()) camera.projectionMatrix.elements[9] -= sheetFrac() * 0.92;
    camera.projectionMatrixInverse.copy(camera.projectionMatrix).invert();""",
    """    if (!fp && narrow()) camera.projectionMatrix.elements[9] -= sheetFrac() * 0.92;
    if (!fp && panelShift) camera.projectionMatrix.elements[9] += panelShift; // v104.15: the city below the floating panel
    camera.projectionMatrixInverse.copy(camera.projectionMatrix).invert();""", "projection")
sub("""  const portrait = () => root.clientWidth / Math.max(1, root.clientHeight) < 0.85;""",
    """  // v104.15 (loop turn 24): on a stage of 720 px or wider the panel floats over the city (top right on he/ar, top left on LTR).
  // In the aerial view the lens shifts down just enough that the roofs under the panel clear it by 30 px, never pushing the towers'
  // bases off the stage (48 px). Computed when the camera arrives and on resize, never while the user orbits (tablet 768: tower
  // C's roof sat under the panel, unnamed). A lens shift: the camera does not move; raycasts and labels use the same matrix.
  // (panelShift is declared beside `anim`, before anything can call applyProjection)
  function fitPanel() {
    const prev = panelShift;
    panelShift = 0;
    if (!fp && !docked && !narrow() && S.mode === 'aerial' && !anim && ui.panel && !ui.panel.hidden && ui.panel.offsetParent) {
      applyProjection(); camera.updateMatrixWorld(); camera.matrixWorldInverse.copy(camera.matrixWorld).invert();
      const w = root.clientWidth, h = root.clientHeight, rr = root.getBoundingClientRect(), pr = ui.panel.getBoundingClientRect();
      const px0 = pr.left - rr.left - 30, px1 = pr.right - rr.left + 30, pyB = pr.bottom - rr.top + 30; // the badge's half + the panel's pad
      let topY = Infinity, baseY = -Infinity;
      const v = new THREE.Vector3();
      for (const k in TW) {
        const X = TW[k];
        v.set(X.t.cx, X.height + 5, X.t.cz).project(camera); // the roof label's own anchor
        const sx = (v.x * 0.5 + 0.5) * w, sy = (-v.y * 0.5 + 0.5) * h;
        if (sx > px0 && sx < px1) topY = Math.min(topY, sy);
        v.set(X.t.cx, 0, X.t.cz).project(camera);
        baseY = Math.max(baseY, (-v.y * 0.5 + 0.5) * h);
      }
      if (topY < pyB) { const dy = Math.min(pyB - topY, Math.max(0, h - 48 - baseY)); if (dy > 1) panelShift = 2 * dy / h; }
    }
    // the measurement above ran on the unshifted lens: always re-apply (a repeat call with the same value used to leave it unshifted)
    if (panelShift !== prev || panelShift) { applyProjection(); invalidate(); }
  }
  const portrait = () => root.clientWidth / Math.max(1, root.clientHeight) < 0.85;""", "fitPanel")
sub("""    if (reduced || !o.motion || ms <= 0 || !isReady || !anim && from.pos.lengthSq() === 0) {
      setPose(pose); anim = null; return;
    }""",
    """    if (reduced || !o.motion || ms <= 0 || !isReady || !anim && from.pos.lengthSq() === 0) {
      setPose(pose); anim = null; if (pose.done) pose.done(); return; // v104.15: done() on an instant pose too
    }""", "flyTo done")
sub("""    if (m === 'aerial') { orbitMode(true); setOrbitLimits('aerial'); flyTo(aerialPose(), prev === m ? 0 : 1300); }""",
    """    if (m !== 'aerial' && panelShift) fitPanel(); // v104.15: other views have no lens shift
    if (m === 'aerial') { orbitMode(true); setOrbitLimits('aerial'); const ap = aerialPose(); ap.done = fitPanel; flyTo(ap, prev === m ? 0 : 1300); }""",
    "setMode")
sub("""    renderer.setSize(w, h, false);
    applyProjection();
    if (fp) applyFp();
    invalidate();
  }""",
    """    renderer.setSize(w, h, false);
    applyProjection();
    if (fp) applyFp();
    fitPanel(); // v104.15
    invalidate();
  }""", "resize")
open(JS, "w", encoding="utf-8", newline="\n").write(s)
print("world.js patched (v104.15)")
