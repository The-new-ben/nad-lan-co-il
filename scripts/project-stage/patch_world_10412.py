# -*- coding: utf-8 -*-
"""v104.12 (1.10.2026, loop turn 21, HAD-375): label tiers, and every place in "מה בסביבה" is its icon, never a bare dot.
Progressive label degradation (the cartographic answer when space runs out; MERL TR94-12; Google Maps search results):
  tier A  the name and its second line (walk time, distance, floors and height), every position tried;
  tier B  the name alone, one line, when A has no room; an honesty line ("planned to open", "illustration") never drops;
  tier C  the icon alone, ONLY in the places tab (a search-results layer: the category is on the panel, the list names every place);
          icons keep 24 px apart centre to centre (WCAG 2.2 SC 2.5.8), never on a name or a control.
The WebGL dot layer stays only as the fallback when the icon set is missing. The aerial view, the walk and the window: A and B only
(the M17 decision with Codex stands there). Patches world.js and world.css.
  python patch_world_10412.py"""
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
D = os.path.join(ROOT, "plugins", "nadlan-config", "assets", "project-stage", "world")
JS, CSS = os.path.join(D, "world.js"), os.path.join(D, "world.css")
s = open(JS, encoding="utf-8").read()
css = open(CSS, encoding="utf-8").read()
if "v104.12" in s or "v104.12" in css:
    raise SystemExit("already patched")


def sub(old, new, name, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"[{name}] anchor found {c} times")
    s = s.replace(old, new)


# ---- the candidates: which second lines may drop (soft); an honesty line never does
sub("name: T.towerN(k), meta: tDesc(k), pos:", "name: T.towerN(k), meta: tDesc(k), soft: true, pos:", "towers", 2)
sub("name: tx(mk), meta: T.km(mk.dist), pos:", "name: tx(mk), meta: T.km(mk.dist), soft: true, pos:", "marks")
sub("TW[S.tower].t.cz : 0))), pos: new THREE.Vector3(x, 1, z), prio: 45,", "TW[S.tower].t.cz : 0))), soft: true, pos: new THREE.Vector3(x, 1, z), prio: 45,", "seaview")
sub("meta: opensOf(p) || T.walkMin(p.walk), pos:", "meta: opensOf(p) || T.walkMin(p.walk), soft: !opensOf(p), pos:", "pins")
sub("name: nm, meta: T.walkMin(p.walk), pos:", "name: nm, meta: T.walkMin(p.walk), soft: true, pos:", "places")
sub("name: placeName(S.place), meta: T.walkMin(S.place.walk), pos:", "name: placeName(S.place), meta: T.walkMin(S.place.walk), soft: true, pos:", "place sel")
# ---- the places tab: with the icon set, every place of the category (within its walk time) is a candidate
sub("""    if (m === 'places' && places) {
      const n = narrow() ? 14 : 26;""",
    """    if (m === 'places' && places) {
      // v104.12 (loop turn 21): with the icon set every place of the category is a candidate (named where a name fits, its icon
      // otherwise); without it, the old count over the WebGL dots
      const n = window.NLPlaceIcons ? 60 : (narrow() ? 14 : 26);""", "places n")
# ---- the WebGL dots: only the fallback when the icon set is missing
sub("    placeDots.visible = m === 'places';", "    placeDots.visible = m === 'places' && !window.NLPlaceIcons; // v104.12: the icons replace the dots", "dots mode")
sub("    placeDots.visible = S.mode === 'places';", "    placeDots.visible = S.mode === 'places' && !window.NLPlaceIcons;", "dots cat")
# ---- the layout: tiers A and B for every name; tier C in the places tab
sub("""      e.classList.remove('is-dot');""", """      e.classList.remove('is-dot', 'is-b', 'is-c');""", "reset")
sub("""    if (e._name !== c.name) { e._n.textContent = c.name; e._name = c.name; e._size = null; }
    if (e._meta !== c.meta) { e._m.textContent = c.meta || ''; e._m.style.display = c.meta ? '' : 'none'; e._meta = c.meta; e._size = null; }""",
    """    if (e._name !== c.name) { e._n.textContent = c.name; e._name = c.name; e._size = e._sizeB = null; }
    if (e._meta !== c.meta) { e._m.textContent = c.meta || ''; e._m.style.display = c.meta ? '' : 'none'; e._meta = c.meta; e._size = e._sizeB = null; }""", "sizes")
sub("""      const tw = e._size[0], th = e._size[1];
      const hp = coarse ? 7 : 0; // v104.5: on touch the name chip's tap area is 44 px; the collision keeps those areas apart
      const stems = c.kind === 'tower' ? [12, 30] : [16, 34, 56, 80];
      const off = Math.max(0, tw / 2 - 12);
      const shifts = c.kind === 'tower' ? [0] : [0, off, -off];
      const opts2 = [];
      for (const s of stems) for (const dx of shifts) opts2.push({ s, dx, below: false });
      // v104.11 (loop turn 20): beside its icon too (the 8-position model: sides as well as above and below), vertically centred
      if (e._ik && c.kind !== 'tower') for (const side of (rtl ? ['l', 'r'] : ['r', 'l'])) opts2.push({ s: 0, dx: 0, below: false, side });
      if (c.kind !== 'tower') for (const s of [14, 32]) for (const dx of shifts) opts2.push({ s, dx, below: true });
      let ok = false;
      const gap = 16;
      for (const { s, dx, below, side } of opts2) {""",
    """      // v104.12 (loop turn 21): label tiers. A = the name and its second line; B = the name alone (one line) when A has no room
      // anywhere and the second line is soft (walk time, distance, floors); an honesty line ("planned", "illustration") never drops
      const tiers = [e._size];
      if (c.soft && c.meta) {
        if (!e._sizeB) { e.classList.add('is-b'); e._sizeB = [e._t.offsetWidth, e._t.offsetHeight]; e.classList.remove('is-b'); }
        tiers.push(e._sizeB);
      }
      const hp = coarse ? 7 : 0; // v104.5: on touch the name chip's tap area is 44 px; the collision keeps those areas apart
      const stems = c.kind === 'tower' ? [12, 30] : [16, 34, 56, 80];
      let ok = false;
      const gap = 16;
      for (let ti = 0; ti < tiers.length && !ok; ti++) {
      const tw = tiers[ti][0], th = tiers[ti][1];
      const off = Math.max(0, tw / 2 - 12);
      const shifts = c.kind === 'tower' ? [0] : [0, off, -off];
      const opts2 = [];
      for (const s of stems) for (const dx of shifts) opts2.push({ s, dx, below: false });
      // v104.11 (loop turn 20): beside its icon too (the 8-position model: sides as well as above and below), vertically centred
      if (e._ik && c.kind !== 'tower') for (const side of (rtl ? ['l', 'r'] : ['r', 'l'])) opts2.push({ s: 0, dx: 0, below: false, side });
      if (c.kind !== 'tower') for (const s of [14, 32]) for (const dx of shifts) opts2.push({ s, dx, below: true });
      for (const { s, dx, below, side } of opts2) {""", "tiers open")
sub("""        placed.push(rp);
        if (side) { // beside the icon: no stem; the chip's near edge `gap` px from the anchor, centred on it""",
    """        placed.push(rp);
        if (ti) e.classList.add('is-b');
        if (side) { // beside the icon: no stem; the chip's near edge `gap` px from the anchor, centred on it""", "tier B class")
sub("""        e._t.style.right = (-dx).toFixed(1) + 'px';
        ok = true; break;
      }
      // v104.5 (Codex's QA, M17): a place with an icon and no room for its name steps back entirely (it stays in the list and the
      // cards); an icon never stands without its name
      if (!ok) { if (e._ik || c.kind === 'mark' || c.kind === 'tower' || c.kind === 'civic') { e.style.display = 'none'; continue; } e.classList.add('is-dot'); }""",
    """        e._t.style.right = (-dx).toFixed(1) + 'px';
        ok = true; break;
      }
      }
      // v104.12: tier C, ONLY in the places tab (a search-results layer: the category is on the panel and the list names every
      // place): the icon alone, a full 24 px target (WCAG 2.2 SC 2.5.8); its box already cleared every name, icon and control above
      if (!ok && e._ik && c.kind === 'place') { e.classList.add('is-c'); ok = true; }
      // v104.5 (Codex's QA, M17): a place with an icon and no room for its name steps back entirely (it stays in the list and the
      // cards); an icon never stands without its name (the aerial view, the walk and the window)
      if (!ok) { if (e._ik || c.kind === 'mark' || c.kind === 'tower' || c.kind === 'civic') { e.style.display = 'none'; continue; } e.classList.add('is-dot'); }""",
    "tiers close")
open(JS, "w", encoding="utf-8", newline="\n").write(s)

anchor = "/* the top bar: the four ways in */"
if css.count(anchor) != 1:
    raise SystemExit("[css] anchor")
css = css.replace(anchor, """/* v104.12 (loop turn 21): label tiers. B = the name alone, one line; C = the icon alone (the places tab only) */
.nlw-pin.is-b .m { display: none !important; }
.nlw-pin.is-c .t, .nlw-pin.is-c .s { display: none; }

""" + anchor)
open(CSS, "w", encoding="utf-8", newline="\n").write(css)
print("world.js + world.css patched (v104.12)")
