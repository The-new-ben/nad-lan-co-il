# -*- coding: utf-8 -*-
"""Design v104.3 (30.9.2026 evening, HAD-375, with Codex): the phone flow of the shared 3D world.
1. One finger scrolls the page: OrbitControls' inline touch-action:none is removed, world.css decides (pan-y inline).
2. No scroller inside a scroller: on a phone, outside full screen, the panel and the card dock BELOW the world, in the page.
3. Walking on a phone opens full screen by itself; leaving full screen while walking goes back to the aerial view.
4. WhatsApp in full screen: the world's own consult pill in its top bar (the world covers the site's bar there).
5. A one-time gesture hint on the first touch.
6. Place pins carry the icon of their kind (assets/arealife/place-icons.js), never a bare dot.
Idempotent: every hunk asserts its anchor once, and a marker stops a second run.
  python patch_world_1043.py"""
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
JS = os.path.join(ROOT, "plugins", "nadlan-config", "assets", "project-stage", "world", "world.js")
CSS = os.path.join(ROOT, "plugins", "nadlan-config", "assets", "project-stage", "world", "world.css")
MARK = "v104.3 (phones"


def sub(s, old, new, name):
    n = s.count(old)
    if n != 1:
        raise SystemExit(f"[{name}] anchor found {n} times")
    return s.replace(old, new)


js = open(JS, encoding="utf-8").read()
if MARK in js:
    raise SystemExit("world.js already patched")

# ---- words: consult + hint, five languages (after askPlace)
WORDS = {
    "ייעוץ חינם על החיים בכיכר',": ("ייעוץ חינם", "החלקה לצדדים מסובבת · שתי אצבעות לזום · ⤢ למסך מלא"),
    "Free advice on living at the square',": ("Free advice", "Swipe sideways to turn · two fingers to zoom · ⤢ full screen"),
    "Conseil gratuit sur la vie à Kikar Hamedina',": ("Conseil gratuit", "Glissez sur le côté pour tourner · deux doigts pour zoomer · ⤢ plein écran"),
    "Бесплатная консультация о жизни на площади',": ("Бесплатная консультация", "Проведите вбок, чтобы повернуть · двумя пальцами масштаб · ⤢ во весь экран"),
    "استشارة مجانية حول الحياة في الميدان',": ("استشارة مجانية", "اسحب جانبًا للتدوير · بإصبعين للتكبير · ⤢ ملء الشاشة"),
}
for tail, (consult, hint) in WORDS.items():
    js = sub(js, tail, tail + f"\n    consult: '{consult}', hint: '{hint}',", "words " + consult)

# ---- 1. touch-action
js = sub(js,
    "    controls.addEventListener('start', () => { anim = null; });\n",
    "    controls.addEventListener('start', () => { anim = null; });\n"
    "    // v104.3 (phones, 30.9): OrbitControls writes touch-action:none inline when it connects. That beat world.css's pan-y and\n"
    "    // trapped the page under the canvas (a vertical swipe on the world moved the page 0 px). The stylesheet decides again:\n"
    "    // pan-y in the page (one finger scrolls the page, sideways turns, two fingers zoom), none in full screen.\n"
    "    cv.style.removeProperty('touch-action');\n",
    "touch-action")

# state flags declared before buildChrome runs (no temporal dead zone when resize() or toggleFull() fire early)
js = sub(js,
    "  const ui = {};\n  if (o.chrome) buildChrome();\n",
    "  const ui = {};\n  let docked = false, autoFull = false, hintShown = false; // v104.3: the phone dock, the walk's own full screen, the hint\n  if (o.chrome) buildChrome();\n",
    "flags")

# ---- 2/4/5. chrome: the dock, the consult pill, the hint
js = sub(js,
    "    root.append(top, ui.eye, ui.panel, ui.card, ui.joy, ui.compass, ui.scale, ui.cap);\n",
    "    root.append(top, ui.eye, ui.panel, ui.card, ui.joy, ui.compass, ui.scale, ui.cap);\n"
    "    // v104.3 (phones, 30.9): on a phone, outside full screen, the panel and the card move into this dock, right under the\n"
    "    // world in the page: the page's own scroll is the only scroll (no scroller inside a scroller). placeChrome() moves them.\n"
    "    ui.dock = el('div', 'nlw-dock'); ui.dock.dir = root.dir; ui.dock.lang = lang;\n"
    "    // in full screen the world covers the site's WhatsApp bar: its own consult pill stays in the top bar there\n"
    "    if (o.wa) {\n"
    "      ui.waFull = el('a', 'nlw-wafull', `<svg viewBox=\"0 0 24 24\" aria-hidden=\"true\"><path fill=\"currentColor\" d=\"M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.4.1-.7.3-.2.3-.9.9-.9 2.2s.9 2.5 1 2.7c.1.2 1.8 2.8 4.4 3.9 1.6.7 2.3.8 3.1.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.1-1.2l-.6-.3z\"/></svg><span>${esc(T.consult)}</span>`);\n"
    "      ui.waFull.href = o.wa; ui.waFull.target = '_blank'; ui.waFull.rel = 'noopener';\n"
    "      top.insertBefore(ui.waFull, full);\n"
    "    }\n"
    "    ui.hint = el('div', 'nlw-hint', esc(T.hint)); ui.hint.hidden = true; ui.hint.setAttribute('aria-hidden', 'true');\n"
    "    root.appendChild(ui.hint);\n",
    "chrome")

# ---- 2. placeChrome + the hint, placed right before toggleFull
js = sub(js,
    "  function toggleFull(force) {\n"
    "    const onF = force != null ? force : !root.classList.contains('nlw--full');\n"
    "    root.classList.toggle('nlw--full', onF);\n",
    "  // v104.3 (phones, 30.9): where the panel and the card sit. On a phone outside full screen: in the dock under the world, in\n"
    "  // the page's flow, with no height limit and no inner scroll. In full screen and on wider screens: over the canvas, as before.\n"
    "  function placeChrome() {\n"
    "    if (!ui.dock || !o.chrome) return;\n"
    "    const want = root.clientWidth > 0 && root.clientWidth < 720 && !root.classList.contains('nlw--full');\n"
    "    if (want === docked) return;\n"
    "    docked = want;\n"
    "    root.classList.toggle('nlw--docked', want);\n"
    "    if (want) { root.after(ui.dock); ui.dock.append(ui.panel, ui.card); S.collapsed = false; }\n"
    "    else { root.insertBefore(ui.panel, ui.joy); root.insertBefore(ui.card, ui.joy); ui.dock.remove(); }\n"
    "    if (W) renderPanel();\n"
    "    window.requestAnimationFrame(() => window.dispatchEvent(new Event('resize'))); // the site's WhatsApp bar re-measures\n"
    "  }\n"
    "  function gestureHint() {\n"
    "    if (hintShown || !ui.hint || !docked) return;\n"
    "    hintShown = true;\n"
    "    try { if (sessionStorage.getItem('nlw-hint')) return; sessionStorage.setItem('nlw-hint', '1'); } catch (e) {}\n"
    "    ui.hint.hidden = false;\n"
    "    setTimeout(() => { if (ui.hint) ui.hint.hidden = true; }, 3500);\n"
    "  }\n"
    "  function toggleFull(force) {\n"
    "    const onF = force != null ? force : !root.classList.contains('nlw--full');\n"
    "    root.classList.toggle('nlw--full', onF);\n"
    "    placeChrome();\n"
    "    if (!onF) { autoFull = false; if (S.mode === 'walk' && coarse && narrow()) setMode('aerial', 'user'); }\n",
    "toggleFull")

# resize: place the chrome first (also before the renderer exists)
js = sub(js,
    "  function resize() {\n"
    "    if (!renderer) return;\n",
    "  function resize() {\n"
    "    placeChrome();\n"
    "    if (!renderer) return;\n",
    "resize")

# the sheet does not cover the canvas when docked
js = sub(js,
    "  function sheetFrac() {\n"
    "    const h = root.clientHeight || 1;\n",
    "  function sheetFrac() {\n"
    "    if (docked) { sheetCache = 0; return 0; }\n"
    "    const h = root.clientHeight || 1;\n",
    "sheetFrac")

# docked: never auto-collapse, no collapse button
js = sub(js,
    "    const collapseBtn = narrow() ? `<button class=\"nlw-x\" type=\"button\" data-collapse",
    "    if (docked) S.collapsed = false;\n"
    "    const collapseBtn = narrow() && !docked ? `<button class=\"nlw-x\" type=\"button\" data-collapse",
    "collapseBtn")

# the card: the dock hides the panel while a card is open (same as the sheet)
js = sub(js,
    "    root.classList.add('has-card');\n",
    "    root.classList.add('has-card'); if (ui.dock) ui.dock.classList.add('has-card');\n",
    "has-card add")
js = sub(js,
    "  function closeCard() { root.classList.remove('has-card');",
    "  function closeCard() { root.classList.remove('has-card'); if (ui.dock) ui.dock.classList.remove('has-card');",
    "has-card remove")

# ---- 3. walking on a phone opens full screen
js = sub(js,
    "  function enterWalk() { if (narrow()) S.collapsed = true; walkSpot('ring'); }",
    "  function enterWalk() {\n"
    "    if (narrow()) S.collapsed = true;\n"
    "    // v104.3: the joystick and the look-around need every finger, so on a phone the walk never happens inside the page\n"
    "    if (coarse && narrow() && !root.classList.contains('nlw--full')) { autoFull = true; toggleFull(true); }\n"
    "    walkSpot('ring');\n"
    "  }",
    "enterWalk")
js = sub(js,
    "    if (m !== 'walk' && prev === 'walk') S.collapsed = false;\n",
    "    if (m !== 'walk' && prev === 'walk') { S.collapsed = false; if (autoFull) { autoFull = false; toggleFull(false); } }\n",
    "leave walk")

# ---- 5. the hint on the first touch
js = sub(js,
    "      controls.enableZoom = true; // engaged: the wheel may zoom now\n",
    "      controls.enableZoom = true; // engaged: the wheel may zoom now\n"
    "      if (e.pointerType === 'touch') gestureHint();\n",
    "hint on touch")

# ---- 6. pins with the icon of their kind
js = sub(js,
    "        add({ id: 'p' + pn.id, kind: 'pin', name:",
    "        add({ id: 'p' + pn.id, kind: 'pin', k: p.k, g: p.g, name:",
    "pin kind")
js = sub(js,
    "        add({ id: 'q' + p.id, kind: 'place', name: nm,",
    "        add({ id: 'q' + p.id, kind: 'place', k: p.k, g: p.g, name: nm,",
    "place kind")
js = sub(js,
    "      if (S.place) add({ id: 'q' + S.place.id, kind: 'place', name:",
    "      if (S.place) add({ id: 'q' + S.place.id, kind: 'place', k: S.place.k, g: S.place.g, name:",
    "sel place kind")
js = sub(js,
    "      e.innerHTML = '<span class=\"d\"></span><span class=\"s\"></span><button class=\"t\" type=\"button\"><span class=\"n\"></span><span class=\"m\"></span></button>';\n"
    "      e._t = e.querySelector('.t'); e._s = e.querySelector('.s'); e._n = e.querySelector('.n'); e._m = e.querySelector('.m');\n",
    "      e.innerHTML = '<span class=\"d\"></span><span class=\"s\"></span><button class=\"t\" type=\"button\"><span class=\"n\"></span><span class=\"m\"></span></button><span class=\"i\"></span>';\n"
    "      e._t = e.querySelector('.t'); e._s = e.querySelector('.s'); e._n = e.querySelector('.n'); e._m = e.querySelector('.m'); e._i = e.querySelector('.i');\n"
    "      e._i.addEventListener('click', (ev) => { ev.stopPropagation(); if (e._click) e._click(); });\n",
    "labelEl markup")
js = sub(js,
    "    e.className = 'nlw-pin k-' + c.kind + (c.on ? ' is-on' : '') + (c.sel ? ' is-sel' : '');\n",
    "    // v104.3: a place carries the icon of its kind (the owner: \"a school is a school icon\"), the same set as the area map\n"
    "    const ic = (c.k || c.g) && window.NLPlaceIcons ? window.NLPlaceIcons : null;\n"
    "    const ik = ic ? ic.glyph(c.k, c.g) + '|' + c.g : '';\n"
    "    if (e._ik !== ik) { e._ik = ik; e._i.innerHTML = ic ? ic.svg(c.k, c.g, '#fff', 2.3) : ''; e._i.style.background = ic ? (ic.COLOR[c.g] || '#4A4740') : ''; }\n"
    "    e.className = 'nlw-pin k-' + c.kind + (c.on ? ' is-on' : '') + (c.sel ? ' is-sel' : '') + (ic ? ' has-i' : '');\n",
    "labelEl class")
js = sub(js,
    "      const dot = { x0: x - 6, x1: x + 6, y0: y - 6, y1: y + 6 }; placed.push(dot);\n",
    "      const rd = e._ik ? 12 : 6; const dot = { x0: x - rd, x1: x + rd, y0: y - rd, y1: y + rd }; placed.push(dot);\n",
    "dot rect")

# the icon file: loaded once, next to the world (assets/arealife/place-icons.js); the pins redraw when it lands
js = sub(js,
    "  // the featured pins read their names and minutes from places.json (a small separate fetch, after the world paints)\n",
    "  placeChrome(); // v104.3: the phone dock from the first paint (the poster), so the page does not jump when the world loads\n"
    "  // v104.3: the place icons (shared with the area map). A classic script that sets window.NLPlaceIcons; same version query.\n"
    "  if (!window.NLPlaceIcons && o.labels) {\n"
    "    try {\n"
    "      const u = new URL('../../arealife/place-icons.js', import.meta.url); const v = new URL(import.meta.url).searchParams.get('ver');\n"
    "      if (v) u.searchParams.set('ver', v);\n"
    "      const s = document.createElement('script'); s.src = u.href; s.async = true; s.onload = () => invalidate(); document.head.appendChild(s);\n"
    "    } catch (e) {}\n"
    "  }\n"
    "  // the featured pins read their names and minutes from places.json (a small separate fetch, after the world paints)\n",
    "icons load")

open(JS, "w", encoding="utf-8", newline="\n").write(js)
print("world.js patched", len(js))

# ---------------------------------------------------------------- world.css
css = open(CSS, encoding="utf-8").read()
if MARK in css:
    raise SystemExit("world.css already patched")
css = sub(css,
    ".nlw-pin.k-start .d { background: var(--nlw-paper); box-shadow: 0 0 0 2px var(--nlw-ink); }\n",
    ".nlw-pin.k-start .d { background: var(--nlw-paper); box-shadow: 0 0 0 2px var(--nlw-ink); }\n"
    "/* v104.3 (phones, 30.9): a place pin is the icon of its kind (assets/arealife/place-icons.js), never a bare dot */\n"
    ".nlw-pin .i { display: none; }\n"
    ".nlw-pin.has-i .i {\n"
    "  display: grid; place-items: center; position: absolute; width: 24px; height: 24px; margin: -12px 0 0 -12px; border-radius: 50%;\n"
    "  border: 2px solid var(--nlw-paper); box-shadow: 0 1px 4px rgba(27, 26, 23, .3); cursor: pointer; pointer-events: auto;\n"
    "}\n"
    ".nlw-pin.has-i .i svg { width: 13px; height: 13px; }\n"
    ".nlw-pin.has-i .d, .nlw-pin.has-i.k-place.is-sel .d { display: none; }\n"
    ".nlw-pin.has-i.is-sel .i { width: 30px; height: 30px; margin: -15px 0 0 -15px; box-shadow: 0 0 0 2px var(--nlw-ink), 0 2px 8px rgba(27, 26, 23, .35); }\n"
    ".nlw-pin.has-i.is-sel .i svg { width: 16px; height: 16px; }\n",
    "pin css")

# the dock + the pill + the hint: appended at the end (after P9c's block)
css = css.rstrip("\n") + "\n" + """
/* ---------------------------------------------------------------- v104.3 (phones, 30.9): one scroll on the phone
   The panel and the card leave the canvas on a phone (outside full screen) and sit in the dock, in the page, under the world.
   The dock has no height limit and no inner scroll: the page's scroll is the only scroll. The world keeps a calm fixed height. */
.nlw.nlw--docked { height: clamp(360px, 58svh, 540px); min-height: 0; }
.nlw-dock {
  --nlw-paper: #FAF7F1; --nlw-card: #FAF7F1; --nlw-ink: #1B1A17; --nlw-ink-2: #4A4740; --nlw-ink-3: #6E695F; --nlw-gold: #9C7A3C;
  --nlw-terra: #C2563A; --nlw-wa: #0F7A63; --nlw-hair: #E2DCD0; --nlw-shadow: 0 2px 14px rgba(27, 26, 23, .10); --nlw-r: 6px;
  position: relative; color: var(--nlw-ink); font-family: 'Assistant', system-ui, -apple-system, 'Segoe UI', sans-serif; font-size: 15px;
  line-height: 1.4; -webkit-font-smoothing: antialiased; -webkit-tap-highlight-color: transparent;
}
.nlw-dock *, .nlw-dock *::before, .nlw-dock *::after { box-sizing: border-box; }
.nlw-dock .nlw-panel, .nlw-dock .nlw-card {
  position: relative; inset: auto; top: auto; bottom: auto; width: auto; max-height: none; overflow: visible; overscroll-behavior: auto;
  border: 1px solid var(--nlw-hair); border-top: 0; border-radius: 0 0 10px 10px; box-shadow: none; background: var(--nlw-paper);
  padding: 14px 16px 16px; z-index: auto;
}
.nlw-dock .nlw-panel:empty { display: none; }
.nlw-dock .nlw-panel .nlw-intro { display: none; }
.nlw-dock .nlw-panel .nlw-title { font-size: 19px; margin-bottom: 2px; }
.nlw-dock.has-card .nlw-panel { display: none; }
.nlw-dock .nlw-faces { display: flex; overflow-x: auto; scrollbar-width: none; gap: 6px; touch-action: pan-x pan-y; }
.nlw-dock .nlw-faces::-webkit-scrollbar { display: none; }
.nlw-dock .nlw-face { flex: 0 0 76px; }
/* the host section (inc/project-stage.php) grows with the dock instead of holding one fixed height */
:root body .nlps-page--world .nlps-stage--world:has(.nlw-dock) { height: auto; min-height: 0; }
:root body .nlps-stage--world:has(.nlw-dock) .nlps-stage__mount { position: relative; inset: auto; }
:root body .nlps-stage--world:has(.nlw-dock) .nlps-ssr-pic { bottom: auto; height: clamp(360px, 58svh, 540px); }

/* full screen: the world covers the site's WhatsApp bar, so its own consult pill sits in the top bar */
.nlw-wafull { display: none; }
.nlw--full .nlw-wafull {
  display: inline-flex; align-items: center; gap: 7px; min-height: 44px; padding: 0 14px 0 12px; border-radius: 999px;
  background: var(--nlw-wa); color: #fff; font: 700 14px/1 'Assistant', system-ui, sans-serif; text-decoration: none;
  box-shadow: var(--nlw-shadow); pointer-events: auto; white-space: nowrap;
}
.nlw--full .nlw-wafull svg { width: 20px; height: 20px; }
@container nlw (max-width: 720px) {
  .nlw--full .nlw-top .nlw-wafull { position: absolute; top: 58px; inset-inline-end: 54px; }
}

/* the one-time gesture hint (first touch, 3.5 s, once per visit) */
.nlw-hint {
  position: absolute; z-index: 7; inset-inline-start: 50%; bottom: 14px; transform: translateX(50%); max-width: calc(100% - 24px);
  background: rgba(27, 26, 23, .86); color: #FAF7F1; border-radius: 999px; padding: 9px 16px; font-size: 13.5px; font-weight: 600;
  text-align: center; pointer-events: none; box-shadow: var(--nlw-shadow);
}
.nlw[dir='ltr'] .nlw-hint { transform: translateX(-50%); }
.nlw-hint[hidden] { display: none; }
"""
open(CSS, "w", encoding="utf-8", newline="\n").write(css)
print("world.css patched", len(css))
