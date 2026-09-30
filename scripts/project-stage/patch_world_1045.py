# -*- coding: utf-8 -*-
"""v104.5 (30.9.2026 night, HAD-375): Codex's (Maya's) QA of the live 1.72.373/374, docs/coordination/codex-qa-373-2026-09-30.md.
M17  a place in the world is its name AND its icon, one unit (her option a): a unit with no room steps back entirely (it stays in the
     list and the cards), never an icon without its name; on touch screens the name chip's tap area is 44 px and the collision
     keeps those areas apart; the icon itself is aria-hidden (the button with the name is the control).
M24  desktop: after a click on the stage the wheel no longer zooms; the wheel scrolls the page, zoom = Ctrl/⌘ + wheel (a trackpad
     pinch sends the same), in full screen or while walking; a one-time hint says so.
M19  enlarged text: the world's tabs may wrap to two lines instead of clipping; the notes' fold is 44 px tall.
card the focus returns to what opened the card when it closes.
  python patch_world_1045.py"""
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
JS = os.path.join(ROOT, "plugins", "nadlan-config", "assets", "project-stage", "world", "world.js")
CSS = os.path.join(ROOT, "plugins", "nadlan-config", "assets", "project-stage", "world", "world.css")
s = open(JS, encoding="utf-8").read()
if "v104.5" in s:
    raise SystemExit("already patched")


def sub(old, new, name, txt=None):
    global s
    n = s.count(old)
    if n != 1:
        raise SystemExit(f"[{name}] anchor found {n} times")
    s = s.replace(old, new)


# ---- words: the wheel hint, five languages (after each hint)
WH = {"החלקה לצדדים מסובבת · שתי אצבעות לזום · ⤢ למסך מלא',": "זום: Ctrl + גלגלת · ⤢ למסך מלא",
      "Swipe sideways to turn · two fingers to zoom · ⤢ full screen',": "Zoom: Ctrl + scroll · ⤢ full screen",
      "Glissez sur le côté pour tourner · deux doigts pour zoomer · ⤢ plein écran',": "Zoom : Ctrl + molette · ⤢ plein écran",
      "Проведите вбок, чтобы повернуть · двумя пальцами масштаб · ⤢ во весь экран',": "Масштаб: Ctrl + колесо · ⤢ во весь экран",
      "اسحب جانبًا للتدوير · بإصبعين للتكبير · ⤢ ملء الشاشة',": "التكبير: Ctrl + عجلة الفأرة · ⤢ ملء الشاشة"}
for tail, w in WH.items():
    sub(tail, tail + f" wheelHint: '{w}',", "wheel words " + w[:8])

# ---- flags: hints per kind
sub("  let docked = false, autoFull = false, hintShown = false; // v104.3: the phone dock, the walk's own full screen, the hint\n",
    "  let docked = false, autoFull = false, hintShown = {}, hintT = 0; // v104.3: the phone dock, the walk's own full screen; v104.5: a hint per kind\n",
    "flags")
sub("""  function gestureHint() {
    if (hintShown || !ui.hint || !docked) return;
    hintShown = true;
    try { if (sessionStorage.getItem('nlw-hint')) return; sessionStorage.setItem('nlw-hint', '1'); } catch (e) {}
    ui.hint.hidden = false;
    setTimeout(() => { if (ui.hint) ui.hint.hidden = true; }, 3500);
  }
""", """  function gestureHint(kind) {
    const k = kind || 'touch';
    if (!ui.hint || hintShown[k] || (k === 'touch' && !docked)) return;
    hintShown[k] = true;
    try { if (sessionStorage.getItem('nlw-hint-' + k)) return; sessionStorage.setItem('nlw-hint-' + k, '1'); } catch (e) {}
    ui.hint.textContent = k === 'wheel' ? T.wheelHint : T.hint;
    ui.hint.hidden = false;
    clearTimeout(hintT); hintT = setTimeout(() => { if (ui.hint) ui.hint.hidden = true; }, 3500);
  }
""", "gestureHint")

# ---- M24: the wheel belongs to the page unless the visitor asks for zoom
sub("""      controls.enableZoom = true; // engaged: the wheel may zoom now
      if (e.pointerType === 'touch') gestureHint();
""", """      if (e.pointerType === 'touch') gestureHint();
""", "no zoom on press")
sub("""    const gest = new Map();
""", """    // v104.5 (Codex's QA, M24): a click on the stage no longer hands the wheel to the camera. In the page the wheel scrolls the page;
    // zoom = Ctrl/⌘ + wheel (a trackpad pinch sends the same), in full screen or while walking. Decided in the capture phase on the
    // world, before OrbitControls' own wheel listener on the canvas.
    on(root, 'wheel', (e) => {
      const z = root.classList.contains('nlw--full') || e.ctrlKey || e.metaKey || !!(fp && fp.walk);
      controls.enableZoom = z;
      if (!z) gestureHint('wheel');
    }, { capture: true, passive: true });
    const gest = new Map();
""", "wheel policy")

# ---- M17: a name and its icon are one unit
sub("prio: m === 'places' ? 60 : 70, dotOnly: m === 'aerial' && narrow(), click: () => openCard(featureCard(f.key)) });",
    "prio: m === 'places' ? 60 : 70, click: () => openCard(featureCard(f.key)) }); // v104.5: named like every place (no icon-only spot)",
    "features named")
sub("""      e.innerHTML = '<span class="d"></span><span class="s"></span><button class="t" type="button"><span class="n"></span><span class="m"></span></button><span class="i"></span>';""",
    """      e.innerHTML = '<span class="d"></span><span class="s"></span><button class="t" type="button"><span class="n"></span><span class="m"></span></button><span class="i" aria-hidden="true"></span>';""",
    "icon aria-hidden")
sub("""      const tw = e._size[0], th = e._size[1];
""", """      const tw = e._size[0], th = e._size[1];
      const hp = coarse ? 7 : 0; // v104.5: on touch the name chip's tap area is 44 px; the collision keeps those areas apart
""", "hp")
sub("""        if (r.x0 < 4 || r.x1 > w - 4 || r.y0 < 4 || r.y1 > h - 4) continue;
        if (hitAny(r, placed) || hitAny(r, reserved) || (c.kind !== 'tower' && hitAny(r, towerRects))) continue;
        placed.push(r);
""", """        if (r.x0 < 4 || r.x1 > w - 4 || r.y0 < 4 || r.y1 > h - 4) continue;
        const rp = hp ? { x0: r.x0, x1: r.x1, y0: r.y0 - hp, y1: r.y1 + hp } : r;
        if (hitAny(rp, placed) || hitAny(rp, reserved) || (c.kind !== 'tower' && hitAny(r, towerRects))) continue;
        placed.push(rp);
""", "padded collision")
sub("""      if (!ok) { if (c.kind === 'mark' || c.kind === 'tower' || c.kind === 'civic') e.style.display = 'none'; else e.classList.add('is-dot'); }
""", """      // v104.5 (Codex's QA, M17): a place with an icon and no room for its name steps back entirely (it stays in the list and the
      // cards); an icon never stands without its name
      if (!ok) { if (e._ik || c.kind === 'mark' || c.kind === 'tower' || c.kind === 'civic') { e.style.display = 'none'; continue; } e.classList.add('is-dot'); }
""", "no orphan icon")

# ---- the card gives the focus back
sub("""  function openCard(c) {
    if (!c || !ui.card) return;
""", """  let cardOpener = null; // v104.5: the focus returns to what opened the card
  function openCard(c) {
    if (!c || !ui.card) return;
    if (ui.card.hidden) cardOpener = document.activeElement;
""", "openCard focus")
sub("""  function closeCard() { root.classList.remove('has-card'); if (ui.dock) ui.dock.classList.remove('has-card'); if (ui.card && !ui.card.hidden) { ui.card.hidden = true; ui.card.innerHTML = ''; afterSheet(); invalidate(); } }""",
    """  function closeCard() {
    root.classList.remove('has-card'); if (ui.dock) ui.dock.classList.remove('has-card');
    if (ui.card && !ui.card.hidden) {
      const back = cardOpener; cardOpener = null;
      const had = ui.card.contains(document.activeElement);
      ui.card.hidden = true; ui.card.innerHTML = ''; afterSheet(); invalidate();
      if (had && back && back.isConnected && back.offsetParent !== null) { try { back.focus({ preventScroll: true }); } catch (e) {} }
    }
  }""", "closeCard focus")
open(JS, "w", encoding="utf-8", newline="\n").write(s)
print("world.js patched (v104.5)")

css = open(CSS, encoding="utf-8").read()
if "v104.5" in css:
    raise SystemExit("world.css already patched")
css = css.rstrip("\n") + "\n" + """
/* ---------------------------------------------------------------- v104.5 (Codex's QA of 1.72.373/374)
   M19: with enlarged text the tabs wrap to two lines instead of clipping; the notes' fold is a 44 px target.
   M17: on touch screens a place's name chip is a 44 px tap area (the collision in world.js keeps those areas apart). */
.nlw-tabs { align-items: stretch; }
.nlw-tab { white-space: normal; line-height: 1.1; padding-block: 4px; text-wrap: balance; }
.nlw-notes summary { min-height: 44px; }
@media (pointer: coarse) {
  .nlw-pin .t::after { content: ''; position: absolute; inset: -7px -3px; }
}
"""
open(CSS, "w", encoding="utf-8", newline="\n").write(css)
print("world.css patched (v104.5)")
