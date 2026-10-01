# -*- coding: utf-8 -*-
"""v104.12, second step (run after patch_world_10412.py): in the places tab, PINS FIRST, NAMES SECOND, the order of a map's search
results. The names that come before the places in the order (the selected place, the project's mark, the walking rings) are placed
first, as before; then every place's icon that fits (never on another icon, a name or a control); then the place names, which never
cover an icon. Measured before this step (v104.12 first step, he 390): the name chips hid most icons (4 of 25 shown).
  python patch_world_10412b.py"""
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
JS = os.path.join(ROOT, "plugins", "nadlan-config", "assets", "project-stage", "world", "world.js")
s = open(JS, encoding="utf-8").read()
if "v104.12" not in s:
    raise SystemExit("run patch_world_10412.py first")
if "pinsFirst" in s:
    raise SystemExit("already patched")


def sub(old, new, name, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"[{name}] anchor found {c} times")
    s = s.replace(old, new)


sub("""    pts.sort((a, b) => a.c.prio - b.c.prio);
    for (const { c, x, y } of pts) {
      const e = labelEl(c);""",
    """    pts.sort((a, b) => a.c.prio - b.c.prio);
    // v104.12 (loop turn 21): in the places tab, pins first, names second (a map's search results). When the order reaches the
    // second place on the map, every remaining place's icon that fits is placed (never on another icon, a name placed before, or a control); then the
    // place names follow, and they never cover an icon. hitAnyX skips the place's own icon.
    const pinsFirst = S.mode === 'places' && !!window.NLPlaceIcons;
    const hitAnyX = (r, list, skip) => list.some((q) => q !== skip && !(r.x1 < q.x0 || r.x0 > q.x1 || r.y1 < q.y0 || r.y0 > q.y1));
    // the nearest place on the map keeps the old order (its name first: "1 min" is what a buyer reads first), then the icons
    // (measured, he 390: two names first left 5 icons on the map, one name first 11, none 13 with the nearest place unnamed)
    let preDone = false, plRank = 0;
    for (let pi = 0; pi < pts.length; pi++) {
      const { c, x, y } = pts[pi];
      const isPl = pinsFirst && c.kind === 'place' && !c.sel;
      const pre = isPl && plRank >= 1; // counts only places whose icon is on the map (below)
      if (pre && !preDone) {
        preDone = true;
        for (let pj = pi; pj < pts.length; pj++) {
          const q = pts[pj]; if (q.c.kind !== 'place' || q.c.sel) continue;
          const eq = labelEl(q.c);
          const br = { x0: q.x - 13, x1: q.x + 13, y0: q.y - 13, y1: q.y + 13 };
          if (!eq._ik || hitAny(br, placed) || hitAny(br, reserved)) { eq._br = false; continue; }
          placed.push(br); eq._br = br;
        }
      }
      const e = labelEl(c);""", "loop head")
sub("""      if (e._ik) { const br = { x0: x - 13, x1: x + 13, y0: y - 13, y1: y + 13 }; if (hitAny(br, placed) || hitAny(br, reserved)) { e.style.display = 'none'; continue; } }""",
    """      if (pre) { if (!e._br) { e.style.display = 'none'; continue; } } // v104.12: its icon was placed (or not) with the others
      else if (e._ik) { const br = { x0: x - 13, x1: x + 13, y0: y - 13, y1: y + 13 }; if (hitAny(br, placed) || hitAny(br, reserved)) { e.style.display = 'none'; continue; } }
      if (isPl && !pre) plRank++;""",
    "icon check")
sub("""        if (hitAny(rp, placed) || hitAny(rp, reserved) || (c.kind !== 'tower' && hitAny(r, towerRects))) continue;""",
    """        if (hitAnyX(rp, placed, pre ? e._br : null) || hitAny(rp, reserved) || (c.kind !== 'tower' && hitAny(r, towerRects))) continue;""",
    "chip test")
sub("""      const rd = e._ik ? 12 : 6; const dot = { x0: x - rd, x1: x + rd, y0: y - rd, y1: y + rd }; placed.push(dot);
    }
    for (const [id, e] of labelPool) if (!used.has(id)) e.style.display = 'none';""",
    """      if (pre) continue; // its icon is already in the list
      const rd = e._ik ? 12 : 6; const dot = { x0: x - rd, x1: x + rd, y0: y - rd, y1: y + rd }; placed.push(dot);
    }
    for (const [id, e] of labelPool) if (!used.has(id)) e.style.display = 'none';""", "loop tail")
sub("""      if (e._ik && c.kind !== 'tower') for (const side of (rtl ? ['l', 'r'] : ['r', 'l'])) opts2.push({ s: 0, dx: 0, below: false, side });""",
    """      // v104.12: a tower's name may sit beside its top too, after the positions above (he 320: tower B named, it had none)
      if (e._ik || c.kind === 'tower') for (const side of (rtl ? ['l', 'r'] : ['r', 'l'])) opts2.push({ s: 0, dx: 0, below: false, side });""",
    "tower sides")
sub("""      const gap = 16;""", """      const gap = c.kind === 'tower' ? 26 : 16; // v104.12: a tower's name beside its top clears the tower's own width""", "tower gap")
open(JS, "w", encoding="utf-8", newline="\n").write(s)
print("world.js patched (v104.12 pins first)")
