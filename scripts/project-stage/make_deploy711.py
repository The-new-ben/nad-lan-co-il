# -*- coding: utf-8 -*-
"""make deploy711.py from deploy710.py: 1.72.711 = HAD-790, package 1 of the long film's gaps (small trust fixes). Whole-file swaps,
each file proven equal to the live one before the edit (docs/qa/had-790/):
  inc/home-v3.php: the desktop language menu has a hover bridge over the 8 px gap and waits 450 ms before closing (gap 20); the four
       language homes (/en/ /fr/ /ru/ /ar/) get the site's header, filled from their own menu, the same links (gaps 27, 38); the
       search icon finds the language home's search field. Option nadlan_home_v3_header_langs = off turns the language header back.
  inc/deals-map.php: the legal line says "אינו צד לעסקה ואינו מייצג אף צד" (he) / "not a party ... does not represent" (en) (gap 40).
  assets/deals/deals.js + deals.css: a deal tag at the map's side edge slides in, its pointer on the place; at the top edge it folds to a
       dot (gap 32); on a mouse a passing wheel scrolls the page, a resting pointer or a click zooms (Ben 21.10, gap 33).
  assets/instruments/core.js + core.css: one shared wheel rule for every tool map (NadLanInstruments.wheelIntent) and its hint; from
       1280 px every tool leaves the 920 px reading column, up to 1320 px (gap 30).
  assets/instruments/tools/hazards.js, asbestos.js, garden.js, soilmap.js: the tool maps use it (no Ctrl lock on a mouse; phones keep
       two fingers) (gap 33).
  assets/nudge/price-alert.js: the test meter shows only with &meter=1; the window is forced in if its entrance did not happen (gap 36).
  assets/project-stage/world/cockpit.js + showroom-i18n.js: the Kikar card says the pictured view is the nearest drawn floor (gap 18).
  assets/project-stage/world/showroom.js (main chat, capture round 4, S02): the tower picture keeps its last frame while the next loads
       (no black stage on south); names in the beam stand beside it and the edge chip leaves the beam's exit (the south beam was covered).
  assets/deals/deals.js (S03/S04): Israel's names only on the base map (country/region names off, place names inside an outline),
       the map never zooms out to the region (minZoom 6.8), a folded tag keeps its full size for the overlap test (it flickered),
       whole tags over dots, a tag whose point is past the bottom or side folds; deals.css: tags 13.5/12.5 px from 768 px.
The buying guide's sentence (gap 40) is post text, changed by scripts/had790/guide_sentence.py with its own backup."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

PREV = 710
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
A = "/wp-content/plugins/nadlan-config/assets/"
FILES = ["inc/home-v3.php", "inc/deals-map.php", "assets/deals/deals.js", "assets/deals/deals.css",
         "assets/instruments/core.js", "assets/instruments/core.css", "assets/instruments/tools/hazards.js",
         "assets/instruments/tools/asbestos.js", "assets/instruments/tools/garden.js", "assets/instruments/tools/soilmap.js",
         "assets/nudge/price-alert.js", "assets/project-stage/world/cockpit.js", "assets/project-stage/world/showroom-i18n.js",
         "assets/project-stage/world/showroom.js", "inc/project-shell.php"]
E = ['Fatal error', 'Warning</b>', 'Notice</b>']
ROWS = ("    ('/fr/?t711a=1', ['nlhp-top--lang', 'nlhp-lang__menu', 'hreflang=\"fr\"'], %r + ['class=\"nlpc-site-header\"'], []),\n"
        "    ('/en/?t711a=1', ['nlhp-top--lang', 'nlhp-lang__menu'], %r + ['class=\"nlpc-site-header\"'], []),\n"
        "    ('/ru/?t711a=1', ['nlhp-top--lang', 'nlhp-lang__menu'], %r + ['class=\"nlpc-site-header\"'], []),\n"
        "    ('/ar/?t711a=1', ['nlhp-top--lang', 'nlhp-lang__menu', 'dir=\"rtl\" lang=\"ar\"'], %r + ['class=\"nlpc-site-header\"'], []),\n"
        "    ('/?t711a=1', ['id=\"nlhp-top\"', 'nlhp-lang__menu::before', '\"nlhp-lang\")?450:220'], %r + ['nlhp-top--lang wp-block-template-part'], []),\n"
        "    ('/developer-deals/?t711a=1', ['אינו צד לעסקה ואינו מייצג אף צד'], %r + ['נדל״ן אינו מתווך'], []),\n"
        "    ('/environmental-hazards/?t711a=1', ['data-nli=\"hzmap\"'], %r, []),\n"
        "    ('/purchase-tax-calculator/?t711a=1', ['class=\"nli\"'], %r, []),\n"
        "    ('/projects/hamedina/?t711a=1', ['hamedina'], %r, []),\n"
        "    ('%sinstruments/core.js?t711a=1', ['wheelIntent: wheelIntent'], [], []),\n"
        "    ('%sinstruments/core.css?t711a=1', ['.nls__whint', '--nli-wide'], [], []),\n"
        "    ('%sdeals/deals.js?t711a=1', ['wheelIntent(map, box)', \"'--nx'\"], [], []),\n"
        "    ('%snudge/price-alert.js?t711a=1', ['var METER = FRESH'], [], []),\n"
        "    ('%sproject-stage/world/showroom-i18n.js?t711a=1', ['הקומה הקרובה שצוירה'], [], []),\n"
        "    ('%sproject-stage/world/showroom.js?t711a=1', ['paintPic.tok', 'side(cw / 2, ch / 2)'], [], []),\n"
        "    ('%sdeals/deals.js?t711b=1', ['function homeNames', 'el._nw', 'minZoom: 6.8'], [], []),\n"
        "    ('/projects/h-infinity-somail-tel-aviv/?t711c=1', ['class=\"nlsh\"', 'id=\"nlpg\"'], %r, []),\n") % (
    E, E, E, E, E, E, E, E, E, A, A, A, A, A, A, A, E)
# Carried for package 3 (HAD-794, its request 19.11): inc/project-shell.php drops a second price guide (id="nlpg") on a page whose
# content already prints one (the Hebrew H Infinity page showed it twice since 1.72.708); the live text must be 1.72.710's.
kl_release.build_release(PREV, 711, FILES, [], {}, {}, ROWS,
                         "trust fixes: language menu, language homes' header, deal tags inside the map, wheel on intent, wide tools, price window, Kikar floor line",
                         "HAD-790 package 1: small trust fixes")

# INHERITED rows that assert what 1.72.711 changes on purpose (first run, 19.11): the deals page's legal line no longer says the site
# is not a broker (it says it is not a party to the deal), and the en/ru language homes now have the site header. Only those tokens go.
_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deploy711.py")
_s = open(_p, encoding="utf-8").read()
_n0 = _s.count("'הלוואה, 8 שנים אחרי', 'נדל״ן אינו מתווך']")
_s = _s.replace("'הלוואה, 8 שנים אחרי', 'נדל״ן אינו מתווך']", "'הלוואה, 8 שנים אחרי', 'אינו צד לעסקה ואינו מייצג אף צד']")
_a = "['#nla11y{position:fixed;bottom:calc(20px + env(safe-area-inset-bottom,0px));right:20px', 'id=\"nlhp-top\"', 'nadlan-hp-css', 'id=\"nlhp-page\"'"
_n1 = _s.count(_a)
_s = _s.replace(_a, "['#nla11y{position:fixed;bottom:calc(20px + env(safe-area-inset-bottom,0px));right:20px', 'id=\"nlhp-page\"'")
_a = "'Найти риелтора', 'class=\"nlcta-wa\"', '#nla11y{position:fixed;bottom:calc(20px + env(safe-area-inset-bottom,0px));left:20px', 'class=\"nlpc-site-header\"'], ['#nla11y{position:fixed;bottom:calc(20px + env(safe-area-inset-bottom,0px));right:20px', 'id=\"nlhp-top\"']"
_n2 = _s.count(_a)
_s = _s.replace(_a, "'Найти риелтора', 'class=\"nlcta-wa\"', '#nla11y{position:fixed;bottom:calc(20px + env(safe-area-inset-bottom,0px));left:20px', 'nlhp-top--lang'], ['#nla11y{position:fixed;bottom:calc(20px + env(safe-area-inset-bottom,0px));right:20px', 'class=\"nlpc-site-header\"']")
assert _n0 == 2 and _n1 == 1 and _n2 == 1, (_n0, _n1, _n2)
open(_p, "w", encoding="utf-8", newline="\n").write(_s)
print("inherited rows: deals x%d, /en/ x%d, /ru/ x%d updated" % (_n0, _n1, _n2))
