# -*- coding: utf-8 -*-
"""make deploy661.py from deploy660.py: 1.72.661 = HAD-712, Ben 12.11.2026 (step 0, blocking) and the build order of 11.11 night.
  - The apartment card never traps the tower: a two-height sheet (peek / expanded), collapse by swipe, handle, a tap on the tower or
    the map, Escape; no timer; the handle nudges once; desktop docks the card beside the tower (build-notes.md "Step 0").
  - Waymarks: one pulse at a time on the next step only, with a short line.
  - View with details (world/viewdetails.js, data hamedina/details.json) and the four-apartment plan (world/planfloor.js).
  - The area map attached under the showroom with the beam (world/kikarmap.js; a footer script on the Kikar pages).
  FILES  world/showroom.js, showroom.css, cockpit.js, cockpit.css, showroom-i18n.js, basket/basket.js (+ whatever the build touched)
  NEW    world/viewdetails.js, planfloor.js, kikarmap.js; hamedina/details.json
  HUNK   inc/project-stage.php (live 658 text): the kikarmap footer on the Kikar showroom pages."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

W = "assets/project-stage/world/"
FILES = [W + "showroom.js", W + "showroom.css", W + "cockpit.js", W + "cockpit.css", W + "showroom-i18n.js", "assets/basket/basket.js",
         W + "viewdetails.js", W + "planfloor.js", W + "kikarmap.js", "assets/project-stage/hamedina/details.json"]
NEW = [W + "viewdetails.js", W + "planfloor.js", W + "kikarmap.js"]
# details.json is tracked since the 658 commit but was not part of 658's release: it goes up as a new file if the live copy is missing
_rp658 = json.load(open(os.path.join(kl_release.QA, "deploy-result-658.json"), encoding="utf-8"))
if "assets/project-stage/hamedina/details.json" not in (_rp658.get("files") or {}):
    NEW.append("assets/project-stage/hamedina/details.json")
FOOT_A = "\tnadlan_omx_send( $subj, $html, $text, 'room' );\n}, 10, 3 );\n"
FOOT_B = FOOT_A + (
    "// 1.72.661 (HAD-712): the area map attached under the Kikar showroom, with the beam on the chosen floor and side (world/kikarmap.js)\n"
    "add_action( 'wp_footer', function () {\n"
    "\tif ( is_admin() || ! function_exists( 'nadlan_ps_current' ) || ! function_exists( 'nadlan_ps_kikar_next' ) ) { return; }\n"
    "\t$ps = nadlan_ps_current();\n"
    "\tif ( ! $ps || ! nadlan_ps_kikar_next( $ps ) ) { return; }\n"
    "\t$base = plugins_url( 'assets/project-stage/', dirname( __FILE__ ) );\n"
    "\t$v    = '?ver=' . nadlan_ps_ver();\n"
    "\techo '<script id=\"nlkm-cfg\">window.__nlKikarMap=' . wp_json_encode( array( 'data' => $base . 'hamedina/details.json' . $v ) ) . ';</script>'\n"
    "\t\t. '<script defer id=\"nlkm-js\" src=\"' . esc_url( $base . 'world/kikarmap.js' . $v ) . '\"></script>';\n"
    "}, 60 );\n")
# the Hebrew Kikar page: the earlier 3D stage loads only on "the live 3D of this floor" (no preload, no mount on load; helper 12.11)
WORLD_HUNKS = [
    ("\t\t// the page paints; mount() still runs on intent and finds them in the cache (the same URLs as the stage's data-cfg)\n\t\t$v    = '?ver=' . nadlan_ps_ver();\n\t\t$base = 'assets/project-stage/' . $ps['dir'] . '/';\n\t\t$pw   = (array) $ps['world'];\n",
     '\t\t// the page paints; mount() still runs on intent and finds them in the cache (the same URLs as the stage\'s data-cfg)\n\t\t$v    = \'?ver=\' . nadlan_ps_ver();\n\t\t$base = \'assets/project-stage/\' . $ps[\'dir\'] . \'/\';\n\t\t$pw   = (array) $ps[\'world\'];\n\t\t// HAD-712 (12.11.2026): the Hebrew Kikar page shows the showroom; its earlier 3D stage loads only on "the live 3D of this floor"\n\t\tif ( nadlan_ps_kikar_next( $ps ) && \'he\' === (string) ( $ps[\'lang\'] ?? \'he\' ) ) { return; }\n'),
    ('  return P;\n}\n',
     '  return P;\n}\nwindow.__nlpsMount = mount; // HAD-712 (12.11.2026): the showroom\'s "live 3D of this floor" mounts the world on the tap\nconst heShowroom = !!(c.next && c.next.journey && c.lang === \'he\'); // HAD-712: the Hebrew showroom hides this stage until that tap\n'),
    ('  if (c.next && c.next.journey && jyPhone()) { /* HAD-699: on phones under the gate the journey replaces the 3D world */ }\n',
     '  if (c.next && c.next.journey && jyPhone()) { /* HAD-699: on phones under the gate the journey replaces the 3D world */ }\n  else if (heShowroom) { /* HAD-712 (12.11.2026): the Hebrew showroom; the 3D world mounts only on its tap (window.__nlpsMount) */ }\n'),
    ("    if (ev !== 'hero-world') return;\n",
     "    if (ev !== 'hero-world') return;\n    if (heShowroom && !document.body.classList.contains('nlsr-3d')) return; // HAD-712: the tour link leads to the showroom (#nlsr)\n"),
]
HUNKS = {"inc/project-stage.php": WORLD_HUNKS + [(FOOT_A, FOOT_B)]}
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-660.json"), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
assert "inc/project-stage.php" not in (rp.get("files") or {}), "1.72.660 wrote a file this release hunks"
LIVE = {"inc/project-stage.php": "b272d436f36308f1c38d7f7aaf74b5d6"}  # deploy-result-658.json (RELEASE DONE 1.72.658); 659 and 660 (designer, assets only) did not write it
ROWS = ("    ('/projects/hamedina/?t661s=1', ['id=\"nlkm-cfg\"', 'kikarmap.js?ver=1.72.661', 'journey.js?ver=1.72.661'], ['Fatal error', 'Warning</b>'], []),\n"
        "    ('/projects/hamedina-en/?t661s=1', ['id=\"nlkm-cfg\"', 'kikarmap.js?ver=1.72.661'], ['Fatal error', 'Warning</b>'], []),\n"
        "    ('/projects/rainbow-tel-aviv/?t661s=1', [], ['Fatal error', 'Warning</b>'], ['id=\"nlkm-cfg\"']),\n"
        "    ('/wp-content/plugins/nadlan-config/assets/project-stage/world/kikarmap.js?t661s=1', ['nl:facing', '#C2563A'], [], []),\n"
        "    ('/wp-content/plugins/nadlan-config/assets/project-stage/world/viewdetails.js?t661s=1', ['viewDetails'], [], []),\n"
        "    ('/wp-content/plugins/nadlan-config/assets/project-stage/world/planfloor.js?t661s=1', ['planFloor'], [], []),\n"
        "    ('/wp-content/plugins/nadlan-config/assets/project-stage/hamedina/details.json?t661s=1', ['\"towers\"', '\"origin\"'], [], []),\n")
kl_release.build_release(660, 661, FILES, NEW, HUNKS, LIVE, ROWS,
                         "the Kikar card as a two-height sheet (never over the tower), waymarks, view with details, the floor plan, the area map with the beam",
                         "the Kikar sheet, waymarks, details, plan and map")
# the showroom.css row asked for the line that hid the old stage on the Hebrew page; since 1.72.661 that line lets "the live 3D of
# this floor" show it (body.nlsr-3d): the same check, the new line
_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deploy661.py")
_s = open(_p, encoding="utf-8").read()
_a = "'body:has(.nlsr[lang=\"he\"]) .nlps-stagebox{display:none!important}'"
_b = "'body:has(.nlsr[lang=\"he\"]):not(.nlsr-3d) .nlps-stagebox{display:none!important}'"
assert _s.count(_a) >= 1, "no row with " + _a
open(_p, "w", encoding="utf-8", newline="\n").write(_s.replace(_a, _b))
print("[rows] the showroom.css row follows the rewritten line")
# the HAD-421 step 5 row asked for the world's preloads on every Kikar language page; since 1.72.661 the Hebrew page (the showroom)
# loads the earlier 3D stage only on "the live 3D of this floor": the row keeps en/fr/ru/ar, and the Hebrew page must NOT hint them
_s = open(_p, encoding="utf-8").read()
_L = _s.split("\n")
_i = [i for i, l in enumerate(_L) if l.startswith("# ") and "(HAD-421 step 5)" in l]
assert len(_i) == 1, _i
_j = _i[0] + 4
_old = '           for p in ("/projects/hamedina/", "/projects/hamedina-en/", "/projects/hamedina-fr/", "/projects/hamedina-ru/", "/projects/hamedina-ar/")]'
assert _L[_j] == _old, _L[_j]
_L[_j] = ('           for p in ("/projects/hamedina-en/", "/projects/hamedina-fr/", "/projects/hamedina-ru/", "/projects/hamedina-ar/")]\n'
          "CHECKS += [('/projects/hamedina/?t661w=1', ['id=\"nlps\"', 'world\\/world.js?ver=1.72.661'], ['Fatal error'], "
          "['three@0.170.0/build/three.module.js\" crossorigin fetchpriority=\"low\">', 'world/world.js?ver=1.72.661\" fetchpriority=\"low\">'])]  # 1.72.661 (HAD-712)")
open(_p, "w", encoding="utf-8", newline="\n").write("\n".join(_L))
print("[rows] the Hebrew Kikar page no longer hints the 3D world; the other four languages still do")
