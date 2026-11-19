# -*- coding: utf-8 -*-
"""make deploy707.py from deploy706.py: 1.72.707 = HAD-792 (package 2 of the long-film gaps, Ben 19.11.2026 "מוצר גמור"):
the apartment designer at /tour/designer/ on every project, as a finished product. ASSETS ONLY: no PHP file, no module-list change.
  SWAP assets/tours/designer-tour.html (five languages from ?lang= / the referring page; ?call=1 opens the call sheet; the design
       order in the WhatsApp text; package 5's lite tracker stub), assets/designer/space.js (floors with grain and grout, daylight,
       an image-based light, wall paint per room, window and door frames and leaves, a sky and a distant city in the window, the
       walls rising out of the plan, the walk through doors that never stops facing a wall), core.js (notes to the builder:
       note.add/edit/move/remove; finish keys wall:<room>), plan.js (red numbered note tags), designer.js + designer.css
       (finishes with wall paint, the notes sheet, the walk's room row and tour, the design order: rooms, finishes, changes,
       notes, services, print, "add to my basket"), catalog.js (wall paints, names in five languages), strings.js (fr, ru, ar),
       studio.js (fr/ru/ar, ?call=1, call tracking), call.js (the call in fr, ru, ar).
  NEW  assets/designer/walknav.js (walkable grid, route, best view), order.js (schema nadlan-design-order v1, the basket hand-off
       to package 4), stringsx.js (the new words in five languages), roomnames.js (Hebrew room names in four languages).
Tests before this release: node docs/design-lab/apartment-designer/test-core.mjs (91/91), pkg2/check-pkg2.mjs local (20/20)."""
import os, sys, json, subprocess
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
import kl_release  # noqa: E402

rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-706.json"), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
REPO = os.path.dirname(os.path.dirname(H))
o = subprocess.run([sys.executable, os.path.join(REPO, "docs", "tools", "design-studio", "build_tour.py"), "1.72.707", "roomscan.js", "roomgeom.js"], capture_output=True, text=True, encoding="utf-8", errors="replace")
assert o.returncode == 0, o.stdout + o.stderr
print("[tour]", o.stdout.strip())
D = "assets/designer/"
SWAP = ["assets/tours/designer-tour.html"] + [D + f for f in ("space.js", "core.js", "plan.js", "designer.js", "designer.css", "catalog.js", "strings.js", "studio.js", "call.js")]
NEW = [D + f for f in ("walknav.js", "order.js", "stringsx.js", "roomnames.js")]
A = "/wp-content/plugins/nadlan-config/" + D
ROWS = ("    ('/tour/designer/?project=ashira&t707d=1', ['walknav.js?v=', 'order.js?v=', 'stringsx.js?v=', 'NL_TRAIL_CFG', 'ru: { dir:'], ['Fatal error'], []),\n"
        "    ('%swalknav.js?t707d=1', ['export function buildNav', 'export function route', 'export function bestYaw'], [], []),\n"
        "    ('%sorder.js?t707d=1', ['nadlan-design-order', 'nl-design-order:v1'], [], []),\n"
        "    ('%sspace.js?t707d=1', ['riseShader', 'goRoom', 'noteTag', 'RoomEnvironment'], [], []),\n"
        "    ('%sdesigner.js?t707d=1', ['renderOrder', 'nadlan:design-order', 'paintWalk'], [], []),\n"
        "    ('%sstringsx.js?t707d=1', ['tFinish', 'ar: {'], [], []),\n"
        "    ('%scall.js?t707d=1', ['pickLang', 'livekitTransport'], [], ['lk_secret']),\n") % (A, A, A, A, A, A)
kl_release.build_release(706, 707, SWAP + NEW, NEW, {}, {}, ROWS,
                         "the apartment designer as a finished product: materials and daylight, walls rising, a walk that never ends at a wall, notes to the builder, the design order, five languages",
                         "HAD-792 package 2: the apartment designer as a finished product")
