# -*- coding: utf-8 -*-
"""v104.14 (1.10.2026, loop turn 23, HAD-375): when the full tower labels leave a tower without its name, every tower's label
starts at tier B (the name alone, one line) until the view's mode or size changes. Three named towers beat one tower with its
floors and height; those stay in the tower's card. Adaptive, not a width threshold: measured he 320 / 360 / 390 / 412 the
fixed full labels named 2 of 3 towers (430 too); a fixed "< 400 px" rule still missed 430. The tier is tracked by index (bAt),
so the chip shown is the size that was placed. If one line still leaves a tower unnamed (tablet 768), the full labels come back.
Honesty (same release): a tower's name never sits on ANOTHER tower (live 1.72.383 put "מגדל B" on tower C's body); the stems are
longer; a tower with no room for any name shows its letter on its own roof (a 28 px badge; the button keeps the full name).
  python patch_world_10414.py"""
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
JS = os.path.join(ROOT, "plugins", "nadlan-config", "assets", "project-stage", "world", "world.js")
s = open(JS, encoding="utf-8").read()
if "v104.14" in s:
    raise SystemExit("already patched")


def sub(old, new, name, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"[{name}] anchor found {c} times")
    s = s.replace(old, new)


sub("""  function layoutLabels() {
    if (!o.labels) return;
    const w = root.clientWidth, h = root.clientHeight;""",
    """  // v104.14 (loop turn 23): towers' names on one line once the full labels left a tower unnamed, for this mode and size; back
  // to the full labels if one line did not name it either (tablet 768: tower C has no room at all, A and B keep their floors)
  let towersOneLine = false, towersGaveUp = false, towersKey = '';
  function layoutLabels() {
    if (!o.labels) return;
    const w = root.clientWidth, h = root.clientHeight;
    const tKey = S.mode + '|' + w + 'x' + h;
    if (tKey !== towersKey) { towersKey = tKey; towersOneLine = false; towersGaveUp = false; }
    let towerMissed = false;""", "head")
sub("""      const tiers = [e._size];
      if (c.soft && c.meta) {
        if (!e._sizeB) { e.classList.add('is-b'); e._sizeB = [e._t.offsetWidth, e._t.offsetHeight]; e.classList.remove('is-b'); }
        tiers.push(e._sizeB);
      }""",
    """      const tiers = [e._size];
      let bAt = -1; // the index of tier B in this list
      if (c.soft && c.meta) {
        if (!e._sizeB) { e.classList.add('is-b'); e._sizeB = [e._t.offsetWidth, e._t.offsetHeight]; e.classList.remove('is-b'); }
        tiers.push(e._sizeB); bAt = 1;
        // v104.14: three named towers beat one tower with its floors and height (which stay in its card)
        if (c.kind === 'tower' && towersOneLine) { tiers.shift(); bAt = 0; }
      }""", "tiers")
sub("""        if (ti) e.classList.add('is-b');""", """        if (ti === bAt) e.classList.add('is-b');""", "tier class")
sub("""      if (!ok) { if (e._ik || c.kind === 'mark' || c.kind === 'tower' || c.kind === 'civic') { e.style.display = 'none'; continue; } e.classList.add('is-dot'); }""",
    """      if (!ok && c.kind === 'tower') towerMissed = true;
      if (!ok) { if (e._ik || c.kind === 'mark' || c.kind === 'tower' || c.kind === 'civic') { e.style.display = 'none'; continue; } e.classList.add('is-dot'); }""",
    "miss")
sub("""    for (const [id, e] of labelPool) if (!used.has(id)) e.style.display = 'none';
  }""",
    """    for (const [id, e] of labelPool) if (!used.has(id)) e.style.display = 'none';
    if (towerMissed && !towersOneLine && !towersGaveUp) { towersOneLine = true; invalidate(); } // the next frame: towers on one line
    else if (towerMissed && towersOneLine) { towersOneLine = false; towersGaveUp = true; invalidate(); } // it did not help: full again
  }""", "tail")
# ---- honesty: a tower's name never sits on ANOTHER tower (live 1.72.383: "מגדל B" beside its roof covered tower C's body, so
# a buyer could read the wrong tower); longer stems give the names more room above; tier C for a tower = its letter on its own roof
sub("""      if (ok) towerRects.push({ x0: x0 + 2, x1: x1 - 2, y0: y0 + 16, y1 });""",
    """      if (ok) towerRects.push({ x0: x0 + 2, x1: x1 - 2, y0: y0 + 16, y1, k });""", "tower rects")
sub("""    let preDone = false, plRank = 0;""",
    """    // v104.14: every tower's roof is reserved first (the place of its letter, with the touch padding): no other name covers a roof,
    // and a tower without room for its name still shows its letter there (he 390: A's name moved up a step, B shows its letter)
    const roofs = new Map();
    for (const { c, x, y } of pts) {
      if (c.kind !== 'tower' || !TW[c.id.slice(1)]) continue;
      const rb = { x0: x - 15, x1: x + 15, y0: y - 15 - (coarse ? 7 : 0), y1: y + 15 + (coarse ? 7 : 0), cx: x, cy: y };
      // the badge's tap area is the 28 px circle itself (no 44 px extension): two roofs only need their circles apart
      if (hitAny(rb, reserved) || [...roofs.values()].some((q) => Math.hypot(q.cx - x, q.cy - y) < 30)) continue;
      roofs.set(c.id, rb); placed.push(rb);
    }
    let preDone = false, plRank = 0;""", "roofs")
sub("""    const hitAnyX = (r, list, skip) =>""",
    """    // v104.14: a tower's name may not lie on ANOTHER tower. Above its roof (a stem shows whose it is) at most a fifth of the chip
    // may cross another tower's box; beside its roof (no stem) at most 3%, a brush of the outline (he 390: "מגדל B" beside the
    // middle roof crossed tower C's body by 8% and read as C's name; tablet 768: B's name brushed tower A's box by 1 px, fine)
    const onOtherTower = (r, id, f) => towerRects.some((q) => 't' + q.k !== id && Math.max(0, Math.min(r.x1, q.x1) - Math.max(r.x0, q.x0)) * Math.max(0, Math.min(r.y1, q.y1) - Math.max(r.y0, q.y0)) > f * (r.x1 - r.x0) * (r.y1 - r.y0));
    const hitAnyX = (r, list, skip) =>""", "other-tower helper")
sub("""        if (hitAnyX(rp, placed, pre ? e._br : null) || hitAny(rp, reserved) || (c.kind !== 'tower' && hitAny(r, towerRects))) continue;""",
    """        if (hitAnyX(rp, placed, pre ? e._br : (roofs.get(c.id) || null)) || hitAny(rp, reserved) || (c.kind !== 'tower' ? hitAny(r, towerRects) : onOtherTower(r, c.id, side ? 0.03 : 0.2))) continue;""",
    "other towers")
sub("""      const stems = c.kind === 'tower' ? [12, 30] : [16, 34, 56, 80];""",
    """      const stems = c.kind === 'tower' ? [12, 30, 52, 74] : [16, 34, 56, 80];""", "tower stems")
sub("""      e.classList.remove('is-dot', 'is-b', 'is-c');""", """      e.classList.remove('is-dot', 'is-b', 'is-c', 'is-roof');""", "reset")
sub("""      if (!ok && c.kind === 'tower') towerMissed = true;""",
    """      if (!ok && c.kind === 'tower') {
        towerMissed = true;
        // v104.14: tier C for a tower, its letter on its own roof (a 28 px badge; the button keeps the full name for screen readers);
        // the roof was reserved before any name was placed, with the touch padding, so the badge never touches another tap area
        if (roofs.has(c.id)) {
          e.classList.add('is-roof'); e._t.dataset.l = c.id.slice(1);
          e._s.style.height = '0px'; e._t.style.top = '0px'; e._t.style.right = '0px'; e._t.style.transform = 'translate(50%, -50%)';
          ok = true; continue;
        }
      }""", "roof")
open(JS, "w", encoding="utf-8", newline="\n").write(s)

CSS = os.path.join(os.path.dirname(JS), "world.css")
c = open(CSS, encoding="utf-8").read()
if "is-roof" not in c:
    anchor = "/* the top bar: the four ways in */"
    if c.count(anchor) != 1:
        raise SystemExit("[css] anchor")
    c = c.replace(anchor, """/* v104.14 (loop turn 23): a tower with no room for its name shows its letter on its own roof; the name stays in the button */
.nlw-pin.k-tower.is-roof .s { display: none; }
.nlw-pin.k-tower.is-roof .t { width: 28px; height: 28px; padding: 0; border-radius: 50% !important; top: 0 !important; right: 0 !important; transform: translate(50%, -50%) !important; box-shadow: 0 0 0 2px var(--nlw-paper), 0 1px 4px rgba(27, 26, 23, .3); }
.nlw-pin.k-tower.is-roof .n, .nlw-pin.k-tower.is-roof .m { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; margin: 0; }
/* the letter fills the badge exactly (the same ::after is the 44 px tap area elsewhere on touch screens: here it is the badge) */
.nlw-pin.k-tower.is-roof .t::after { content: attr(data-l); position: absolute; inset: 0; display: grid; place-items: center; font: 700 14px/1 'Noto Serif Hebrew', 'Assistant', serif; color: var(--nlw-paper); }

""" + anchor)
    open(CSS, "w", encoding="utf-8", newline="\n").write(c)
print("world.js + world.css patched (v104.14)")
