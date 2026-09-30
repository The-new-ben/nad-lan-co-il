# -*- coding: utf-8 -*-
"""v104.4 (30.9.2026 night, HAD-375): Codex's QA of the live 1.72.373 (Maya, in Ben's session).
1. A vertical swipe on the world scrolled the page but ALSO tilted the camera a little (OrbitControls and the window view
   got the first touch moves before the browser took the pan). On a phone in the page (docked), a touch never tilts:
   the orbit's polar angle is held for the gesture, and the window view ignores the vertical part.
2. The world's place icons could still overlap each other and cover names: a badge that would sit on a higher-priority
   badge, name or control now steps back (hidden) instead of piling up.
  python patch_world_1044.py"""
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
JS = os.path.join(ROOT, "plugins", "nadlan-config", "assets", "project-stage", "world", "world.js")
s = open(JS, encoding="utf-8").read()
if "v104.4" in s:
    raise SystemExit("already patched")


def sub(old, new, name):
    global s
    n = s.count(old)
    if n != 1:
        raise SystemExit(f"[{name}] anchor found {n} times")
    s = s.replace(old, new)


sub("""    let down = null;
    on(cv, 'pointerdown', (e) => {
      down = { x: e.clientX, y: e.clientY, t: performance.now(), id: e.pointerId, yaw: fp ? fp.yaw : 0, tilt: fp ? fp.tilt : 0 };
      controls.enableZoom = true; // engaged: the wheel may zoom now
      if (e.pointerType === 'touch') gestureHint();
""", """    let down = null;
    // v104.4 (Codex's QA of 1.72.373): in the page (docked) a touch never tilts the camera. The browser takes the vertical
    // pan a few moves late; those first moves used to tip the orbit. The polar angle is held for the gesture.
    let tiltLock = null;
    const unlockTilt = () => { if (tiltLock) { controls.minPolarAngle = tiltLock[0]; controls.maxPolarAngle = tiltLock[1]; tiltLock = null; } };
    on(window, 'pointerup', unlockTilt); on(window, 'pointercancel', unlockTilt);
    on(cv, 'pointerdown', (e) => {
      down = { x: e.clientX, y: e.clientY, t: performance.now(), id: e.pointerId, yaw: fp ? fp.yaw : 0, tilt: fp ? fp.tilt : 0, touch: e.pointerType === 'touch' };
      controls.enableZoom = true; // engaged: the wheel may zoom now
      if (e.pointerType === 'touch') gestureHint();
      if (e.pointerType === 'touch' && docked && !fp && !tiltLock) { const a = controls.getPolarAngle(); tiltLock = [controls.minPolarAngle, controls.maxPolarAngle]; controls.minPolarAngle = a; controls.maxPolarAngle = a; }
""", "tilt lock")
sub("""      fp.tilt = clamp(down.tilt + dy * k, fp.window ? -25 : -20, fp.window ? 30 : 35);
""", """      if (!(docked && down.touch)) fp.tilt = clamp(down.tilt + dy * k, fp.window ? -25 : -20, fp.window ? 30 : 35); // v104.4
""", "fp tilt")
sub("""      if (c.dotOnly) { e.classList.add('is-dot'); continue; }
""", """      // v104.4 (Codex's QA): an icon never sits on a higher-priority icon, name or control; it steps back instead
      if (e._ik) { const br = { x0: x - 13, x1: x + 13, y0: y - 13, y1: y + 13 }; if (hitAny(br, placed) || hitAny(br, reserved)) { e.style.display = 'none'; continue; } }
      if (c.dotOnly) { e.classList.add('is-dot'); if (e._ik) placed.push({ x0: x - 12, x1: x + 12, y0: y - 12, y1: y + 12 }); continue; }
""", "badge collision")
open(JS, "w", encoding="utf-8", newline="\n").write(s)
print("world.js patched (v104.4)")
