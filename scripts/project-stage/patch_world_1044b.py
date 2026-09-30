# -*- coding: utf-8 -*-
"""v104.4b: the tilt lock alone did not hold (measured: the camera's height 564 -> 388 after one vertical swipe). OrbitControls
keeps the finger's moves as a damped delta and applies it after the finger lifts, when the lock was already released. So in the
page (docked), a one-finger move that is mostly vertical never reaches the camera: a capture listener on the world stops it before
the canvas (the browser still pans the page: that is decided by touch-action, not by listeners). Sideways moves still turn the
model, with the polar angle held until the damping has settled (1 s after the finger lifts).
  python patch_world_1044b.py"""
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
JS = os.path.join(ROOT, "plugins", "nadlan-config", "assets", "project-stage", "world", "world.js")
s = open(JS, encoding="utf-8").read()
if "v104.4b" in s:
    raise SystemExit("already patched")


def sub(old, new, name):
    global s
    n = s.count(old)
    if n != 1:
        raise SystemExit(f"[{name}] anchor found {n} times")
    s = s.replace(old, new)


sub("""    let tiltLock = null;
    const unlockTilt = () => { if (tiltLock) { controls.minPolarAngle = tiltLock[0]; controls.maxPolarAngle = tiltLock[1]; tiltLock = null; } };
    on(window, 'pointerup', unlockTilt); on(window, 'pointercancel', unlockTilt);
""", """    let tiltLock = null, tiltT = 0;
    // (a mode change in between sets its own limits: then the held ones are simply dropped, never written back)
    const unlockNow = () => { if (tiltLock) { if (controls.minPolarAngle === controls.maxPolarAngle) { controls.minPolarAngle = tiltLock[0]; controls.maxPolarAngle = tiltLock[1]; } tiltLock = null; } };
    // v104.4b: OrbitControls applies the finger's moves with damping after the finger lifts: hold the tilt until that settles
    const unlockTilt = () => { clearTimeout(tiltT); tiltT = setTimeout(unlockNow, 1000); };
    on(window, 'pointerup', unlockTilt); on(window, 'pointercancel', unlockTilt);
    // v104.4b: in the page, a one-finger move that is mostly vertical belongs to the page's scroll, never to the camera. Stopped in
    // the capture phase on the world, before the canvas's own listeners (OrbitControls, the window view); the pan itself is the
    // browser's (touch-action: pan-y), so the page still scrolls.
    const gest = new Map();
    on(root, 'pointerdown', (e) => { if (e.pointerType === 'touch') gest.set(e.pointerId, { x: e.clientX, y: e.clientY, v: null }); }, true);
    on(root, 'pointermove', (e) => {
      if (!docked || e.pointerType !== 'touch' || gest.size !== 1) return;
      const g = gest.get(e.pointerId); if (!g) return;
      if (g.v === null) { const dx = Math.abs(e.clientX - g.x), dy = Math.abs(e.clientY - g.y); if (dx + dy < 4) return; g.v = dy > dx; }
      if (g.v) e.stopPropagation();
    }, true);
    const gEnd = (e) => { gest.delete(e.pointerId); };
    on(window, 'pointerup', gEnd); on(window, 'pointercancel', gEnd);
""", "gesture split")
sub("""      if (e.pointerType === 'touch' && docked && !fp && !tiltLock) { const a = controls.getPolarAngle(); tiltLock = [controls.minPolarAngle, controls.maxPolarAngle]; controls.minPolarAngle = a; controls.maxPolarAngle = a; }
""", """      if (e.pointerType === 'touch' && docked && !fp) { clearTimeout(tiltT); if (!tiltLock) { const a = controls.getPolarAngle(); tiltLock = [controls.minPolarAngle, controls.maxPolarAngle]; controls.minPolarAngle = a; controls.maxPolarAngle = a; } }
""", "lock keep")
open(JS, "w", encoding="utf-8", newline="\n").write(s)
print("world.js patched (v104.4b)")
