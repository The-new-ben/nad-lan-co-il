# -*- coding: utf-8 -*-
"""make deploy721.py from deploy720.py: 1.72.721 = HAD-790 + HAD-712 trust fix, Ben's order (20.11.2026, through the coordinator): on
the Kikar HaMedina page the first paragraph showed, then the showroom jumped in above it (650-800 px, after the first paint) and the
paragraph left the screen. Ben: the first paragraph must always be there, it carries the search phrase.
  SWAP inc/project-stage.php: on the Kikar pages with the showroom (he, en) the page prints the showroom's place right after the
       buttons block (#nlsr.nlsr-ph with the showroom's first picture and a height that follows the showroom's own rules), its own
       grid rows (sr, srmap for the area map that attaches under it, film for the film that had no row), and the rules that hide the
       old stage and widen the text on a Hebrew desktop keyed on #nlsr so they hold from the first paint.
  SWAP assets/project-stage/world/showroom.js: mountShowroom fills that place once its styles are in (it had built its own section and
       put it before the page), one stylesheet link; a shared #dira= link scrolls the showroom into view. Steps, cockpit, basket and the
       small map are unchanged; engine.js and the big map's beam are not touched.
  Measured on the live pages with the new parts routed in (scripts/had790/kikar_first_screen.py, kikar_journey_check.py): order h1,
  paragraph, buttons, showroom on 390 and 1440, he and en; cold-load layout shift 0.78 -> 0 (phone he), 0.76 -> 0 (phone en),
  1.43 -> 0.001 (desktop en), 0.59 -> 0.18 (desktop he: what is left is the site font arriving and rewrapping the paragraph); the
  journey 8/8 on each (tower, floor, apartment, 360, basket, call link, #dira)."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

PREV = 720
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
E = ['Fatal error', 'Warning</b>', 'Notice</b>']
PH = '<section class="nlsr-ph" id="nlsr" dir="%s" lang="%s" aria-hidden="true"><div class="nlsr-ph__stage"><img src="https://nad-lan.co.il/wp-content/plugins/nadlan-config/assets/project-stage/hamedina/aerial-tall-800.webp?ver=1.72.721" alt="" width="800" height="1067" decoding="async"></div></section>'
GRID = ':root body .nlps-page.nlps-page--sr>.nlws-film{grid-area:film}'
SJ = '/wp-content/plugins/nadlan-config/assets/project-stage/world/showroom.js?t721a=1'
ROWS = ("    ('/projects/hamedina/?t721a=1', ['<style id=\"nlsr-place-css\">', %r, 'nlps-page--world nlps-page--sr\"', %r, '<h1 id=\"nl-project-page-title\" class=\"nlps-h1\">'], %r, []),\n"
        "    ('/projects/hamedina-en/?t721a=1', ['<style id=\"nlsr-place-css\">', %r, 'nlps-page--world nlps-page--sr\"', %r], %r, []),\n"
        "    ('/projects/hamedina-fr/?t721a=1', ['nlps-page'], %r + ['nlsr-ph', 'nlps-page--sr'], []),\n"
        "    ('/projects/hamedina-ru/?t721a=1', ['nlps-page'], %r + ['nlsr-ph', 'nlps-page--sr'], []),\n"
        "    ('/projects/hamedina-ar/?t721a=1', ['nlps-page'], %r + ['nlsr-ph', 'nlps-page--sr'], []),\n"
        "    ('/projects/rainbow-tel-aviv/?t721a=1', ['nlps-page'], %r + ['nlsr-ph', 'nlps-page--sr'], []),\n"
        "    ('/projects/h-infinity-somail-tel-aviv/?t721a=1', ['nlps-page'], %r + ['nlsr-ph', 'nlps-page--sr'], []),\n"
        "    (%r, [\"classList.contains('nlsr-ph')\", 'if (!place) at.parentNode.insertBefore(el, at);', \"el.scrollIntoView({ block: 'start' })\", 'link[data-nlsr-css]', \"el.id = 'nlsr'\", 'export function mountShowroom(at)'], [], []),\n") % (
    PH % ("rtl", "he"), GRID, E, PH % ("ltr", "en"), GRID, E, E, E, E, E, E, SJ)
kl_release.build_release(PREV, 721, ["inc/project-stage.php", "assets/project-stage/world/showroom.js"], [], {}, {}, ROWS,
                         "the Kikar showroom sits after the title, the first paragraph and the buttons (it jumped in above them)",
                         "HAD-790 + HAD-712: the Kikar first paragraph stays first")

# INHERITED row that asserts what 1.72.721 changes on purpose (first run, 20.11, rolled back on it): the Kikar page block now carries
# the class nlps-page--sr; only that token changes (the row's other checks stay).
_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deploy721.py")
_s = open(_p, encoding="utf-8").read()
_a = "'<div class=\"nlps-page nlps-page--world\" dir=\"rtl\" lang=\"he\">'"
_n0 = _s.count(_a)
_s = _s.replace(_a, "'<div class=\"nlps-page nlps-page--world nlps-page--sr\" dir=\"rtl\" lang=\"he\">'")
assert _n0 == 1, _n0
open(_p, "w", encoding="utf-8", newline="\n").write(_s)
print("inherited rows: Kikar page block x%d updated" % _n0)
