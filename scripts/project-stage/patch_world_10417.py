# -*- coding: utf-8 -*-
"""v104.17 (1.10.2026, the V2 loop turn 1, item V1; HAD-380): the page opens on choosing an apartment, and nothing scrolls inside
the 3D. Measured on live 1.72.387: on the PC the floating panel (803 px in 638) and the card (933 in 638) scrolled inside the stage;
on the phone the eight directions were a sideways strip; half the floor panel was "sun and shade"; the direction cards carried sun
hours; the floor view labelled the school, the lake and the park.
  1. the panel and cards never float over the 3D (except full screen): beside it on a stage >= 900 px (a 340 px column in the
     page's own scroll, the 3D sticky), under it below 900 px (the phone dock as before);
  2. a world with apartments to show (o.examples) opens in the floor view, in numbered steps: 1 tower, 2 floor, 3 apartment by
     direction;
  3. the directions are a 4 x 2 grid at every width, the direction and its bearing (no sun hours);
  4. the sun is a closed fold at the end of the panel, never opened by itself;
  5. the floor view labels only the towers and the floor;
  6. in full screen a card that floats over the 3D closes after 8 s without a touch, hover or keyboard inside it.
  python patch_world_10417.py"""
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
D = os.path.join(ROOT, "plugins", "nadlan-config", "assets", "project-stage", "world")
JS, CSS = os.path.join(D, "world.js"), os.path.join(D, "world.css")
s = open(JS, encoding="utf-8").read()
css = open(CSS, encoding="utf-8").read()
if "v104.17" in s or "v104.17" in css:
    raise SystemExit("already patched")


def sub(old, new, name, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"[{name}] anchor found {c} times")
    s = s.replace(old, new)


# 1. the dock at every width (not in full screen); beside the 3D on a wide stage
sub("""    const want = root.clientWidth > 0 && root.clientWidth < 720 && !root.classList.contains('nlw--full');
    if (want === docked) return;
    docked = want;
    root.classList.toggle('nlw--docked', want);""",
    """    // v104.17 (V1): the panel and the cards never float over the 3D: under it below 900 px, BESIDE it from 900 px (the stage's own
    // width, read on the mount so the side column does not feed back), in the page's own scroll; only full screen floats them
    const hostW = (root.parentElement && root.parentElement.clientWidth) || root.clientWidth;
    const want = hostW > 0 && !root.classList.contains('nlw--full');
    const side = want && hostW >= 900;
    if (ui.dock) ui.dock.classList.toggle('nlw-dock--side', side);
    root.classList.toggle('nlw--side', side);
    if (want === docked) return;
    docked = want;
    root.classList.toggle('nlw--docked', want);""", "placeChrome")
# 2. open on choosing an apartment
sub("""    mode: MODES.includes(o.mode) ? o.mode : 'aerial',""",
    """    // v104.17 (V1): a world with apartments to show opens on choosing one (the floor view), unless the page asks for another view
    mode: o.mode === 'aerial' && o.examples && o.examples.url ? 'tower' : (MODES.includes(o.mode) ? o.mode : 'aerial'),""", "start mode")
# 3. the directions without sun hours
sub("""      <span class="nlw-fw">${esc(T.dirsShort[Math.round(norm360(b) / 45) % 8])}</span><small><bdi dir="ltr">${Math.round(b)}°</bdi></small><span class="nlw-sunb"><i style="width:${Math.round(100 * hours[i] / maxH)}%"></i></span><small class="nlw-fh">${esc(T.hoursShort(hours[i]))}</small></button>`).join('')}</div>`;""",
    """      <span class="nlw-fw">${esc(T.dirsShort[Math.round(norm360(b) / 45) % 8])}</span><small><bdi dir="ltr">${Math.round(b)}°</bdi></small></button>`).join('')}</div>`; // v104.17: the sun hours went to the sun's fold""",
    "faces")
sub("""aria-label="${esc(T.faces(dirWord(b)))} ${Math.round(b)}°, ${esc(T.hoursShort(hours[i]))}">""",
    """aria-label="${esc(T.faces(dirWord(b)))} ${Math.round(b)}°">""", "faces aria")
sub("""    const hours = list.map((b) => sunHoursFor(S.tower, S.floor, b, S.season));
    const maxH = Math.max(1, ...hours);
    return `<div class="nlw-faces\"""",
    """    return `<div class="nlw-faces\"""", "faces hours")
# 4. the floor view in numbered steps; the sun a closed fold at the end
sub("""          `<div class="nlw-row">${['A', 'B', 'C'].map((k) => chip(T.towerN(k), k === S.tower, `data-tower="${k}"`, 'nlw-tw')).join('')}</div>` +
          `<label class="nlw-lbl"><span data-floorlbl>${esc(T.floorN(S.floor))}</span><b data-eye>${esc(T.eye(eyeH(S.floor).toFixed(1)))}</b></label>` +""",
    """          `<div class="nlw-step"><b>1</b>${esc(T.steps[0])}</div>` +
          `<div class="nlw-row">${['A', 'B', 'C'].map((k) => chip(T.towerN(k), k === S.tower, `data-tower="${k}"`, 'nlw-tw')).join('')}</div>` +
          `<div class="nlw-step"><b>2</b>${esc(T.steps[1])}</div>` +
          `<label class="nlw-lbl"><span data-floorlbl>${esc(T.floorN(S.floor))}</span><b data-eye>${esc(T.eye(eyeH(S.floor).toFixed(1)))}</b></label>` +""",
    "steps 1-2")
sub("""          `<div class="nlw-lbl"><span>${esc(T.facingLbl)}</span>${S.facing != null ?""",
    """          `<div class="nlw-lbl"><span class="nlw-step"><b>3</b>${esc(T.steps[2])}</span>${S.facing != null ?""", "step 3")
sub("""          sunSection(!nar || S.sunOpen, true) + notesHtml()));""",
    """          sunSection(S.sunOpen, S.sunOpen) + notesHtml())); // v104.17: the sun is a closed fold, never opened by itself""", "sun fold")
for a, b, nm in (("    facingLbl: 'כיוון המבט',", "    facingLbl: 'כיוון המבט',\n    steps: ['בחרו מגדל', 'בחרו קומה', 'בחרו דירה לפי כיוון'], // v104.17", "he"),
                 ("    facingLbl: 'Facing',", "    facingLbl: 'Facing',\n    steps: ['Choose a tower', 'Choose a floor', 'Choose an apartment by its direction'], // v104.17", "en"),
                 ("    facingLbl: 'Orientation',", "    facingLbl: 'Orientation',\n    steps: ['Choisissez une tour', 'Choisissez un étage', 'Choisissez un appartement selon son orientation'], // v104.17", "fr"),
                 ("    facingLbl: 'Сторона света',", "    facingLbl: 'Сторона света',\n    steps: ['Выберите башню', 'Выберите этаж', 'Выберите квартиру по стороне света'], // v104.17", "ru"),
                 ("    facingLbl: 'الاتجاه',", "    facingLbl: 'الاتجاه',\n    steps: ['اختاروا البرج', 'اختاروا الطابق', 'اختاروا الشقة حسب اتجاهها'], // v104.17", "ar")):
    sub(a, b, "steps " + nm)
# 5. the floor view labels only the towers and the floor
sub("""    if (m === 'aerial' || m === 'walk' || m === 'tower') {
      for (const c of W.civic)""",
    """    if (m === 'aerial' || m === 'walk') { // v104.17: the floor view labels only the towers and the floor
      for (const c of W.civic)""", "floor labels")
# 6. in full screen a floating card closes after 8 s without a touch, hover or keyboard inside it
sub("""    if (o.onPick && c.pick) o.onPick(c.pick);
    afterSheet();
    invalidate();
  }
  function closeCard() {""",
    """    if (o.onPick && c.pick) o.onPick(c.pick);
    afterSheet();
    invalidate();
    armCardFade();
  }
  // v104.17 (V1): a card that floats over the 3D (full screen only) fades after 8 s unless a finger, the mouse or the keyboard is in it
  let cardFadeT = 0;
  function armCardFade() {
    clearTimeout(cardFadeT);
    if (docked || !ui.card || ui.card.hidden) return;
    cardFadeT = setTimeout(() => { if (ui.card && !ui.card.hidden && !ui.card.matches(':hover') && !ui.card.contains(document.activeElement)) closeCard(); }, 8000);
  }
  function closeCard() {
    clearTimeout(cardFadeT);""", "card fade")
open(JS, "w", encoding="utf-8", newline="\n").write(s)

# the rules go at the END of the file: earlier phone-dock rules (.nlw-dock .nlw-faces as a sideways strip) must not win
css = css.rstrip("\n") + "\n\n" + """/* v104.17 (V1): the panel and the cards beside the 3D on a wide stage (in the page's own scroll, the 3D sticky), never inside it */
:root body .nlps-stage--world:has(.nlw-dock--side) .nlps-stage__mount { display: grid; grid-template-columns: minmax(0, 1fr) 340px; gap: 14px; align-items: start; }
.nlw.nlw--docked.nlw--side { position: sticky; top: 72px; height: clamp(540px, calc(100svh - 96px), 760px); }
.nlw-dock.nlw-dock--side { margin: 0; padding-top: 0; }
.nlw-dock.nlw-dock--side .nlw-panel .nlw-intro { display: block; }
/* the directions: a 4 x 2 grid at every width, never a sideways strip */
.nlw-dock .nlw-panel .nlw-faces { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); overflow: visible; }
.nlw-dock .nlw-panel .nlw-face { flex: none; min-width: 0; }
/* the numbered steps of the floor view */
.nlw-step { display: flex; align-items: center; gap: 8px; margin: 12px 0 6px; font-weight: 700; font-size: 14px; color: var(--nlw-ink); }
.nlw-step b { display: inline-grid; place-items: center; width: 22px; height: 22px; border-radius: 50%; background: var(--nlw-ink); color: var(--nlw-paper); font-size: 12.5px; }
.nlw-lbl .nlw-step { margin: 0; }
.nlw-lbl .nlw-step b { color: var(--nlw-paper); font-size: 12.5px; }
"""
open(CSS, "w", encoding="utf-8", newline="\n").write(css)
print("world.js + world.css patched (v104.17)")
