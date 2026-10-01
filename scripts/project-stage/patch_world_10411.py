# -*- coding: utf-8 -*-
"""v104.11 (1.10.2026, loop turn 20, HAD-375): a world place's name may also sit BESIDE its icon (the 8-position model of point-label
placement: corners and sides; Christensen, Marks & Shieber, MERL TR94-12). Tried after the existing positions above, before the ones
below; on he/ar pages the left side first (the icon at the line's start), on LTR pages the right side first, like the area map.
Only places that carry an icon (a name and its icon stay one unit). The tap-area padding and every collision rule are unchanged.
  python patch_world_10411.py"""
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
JS = os.path.join(ROOT, "plugins", "nadlan-config", "assets", "project-stage", "world", "world.js")
s = open(JS, encoding="utf-8").read()
if "v104.11" in s:
    raise SystemExit("already patched")


def sub(old, new, name):
    global s
    n = s.count(old)
    if n != 1:
        raise SystemExit(f"[{name}] anchor found {n} times")
    s = s.replace(old, new)


sub("""      for (const s of stems) for (const dx of shifts) opts2.push({ s, dx, below: false });
      if (c.kind !== 'tower') for (const s of [14, 32]) for (const dx of shifts) opts2.push({ s, dx, below: true });
      let ok = false;
      for (const { s, dx, below } of opts2) {
        const r = below ? { x0: x + dx - tw / 2 - 3, x1: x + dx + tw / 2 + 3, y0: y + s - 2, y1: y + s + th + 3 } : { x0: x + dx - tw / 2 - 3, x1: x + dx + tw / 2 + 3, y0: y - s - th - 3, y1: y - s + 2 };""",
    """      for (const s of stems) for (const dx of shifts) opts2.push({ s, dx, below: false });
      // v104.11 (loop turn 20): beside its icon too (the 8-position model: sides as well as above and below), vertically centred
      if (e._ik && c.kind !== 'tower') for (const side of (rtl ? ['l', 'r'] : ['r', 'l'])) opts2.push({ s: 0, dx: 0, below: false, side });
      if (c.kind !== 'tower') for (const s of [14, 32]) for (const dx of shifts) opts2.push({ s, dx, below: true });
      let ok = false;
      const gap = 16;
      for (const { s, dx, below, side } of opts2) {
        const r = side ? (side === 'r' ? { x0: x + gap - 2, x1: x + gap + tw + 3, y0: y - th / 2 - 2, y1: y + th / 2 + 2 } : { x0: x - gap - tw - 3, x1: x - gap + 2, y0: y - th / 2 - 2, y1: y + th / 2 + 2 })
          : below ? { x0: x + dx - tw / 2 - 3, x1: x + dx + tw / 2 + 3, y0: y + s - 2, y1: y + s + th + 3 } : { x0: x + dx - tw / 2 - 3, x1: x + dx + tw / 2 + 3, y0: y - s - th - 3, y1: y - s + 2 };""",
    "options")
sub("""        placed.push(rp);
        e._s.style.height = s + 'px'; e._s.style.top = below ? '0px' : (-s) + 'px';""",
    """        placed.push(rp);
        if (side) { // beside the icon: no stem; the chip's near edge `gap` px from the anchor, centred on it
          e._s.style.height = '0px'; e._t.style.top = '0px';
          e._t.style.transform = side === 'r' ? 'translate(100%, -50%)' : 'translate(0, -50%)';
          e._t.style.right = (side === 'r' ? -gap : gap) + 'px';
          ok = true; break;
        }
        e._s.style.height = s + 'px'; e._s.style.top = below ? '0px' : (-s) + 'px';""",
    "side style")
open(JS, "w", encoding="utf-8", newline="\n").write(s)
print("world.js patched (v104.11)")
