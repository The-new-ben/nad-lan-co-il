# -*- coding: utf-8 -*-
"""make deploy708.py from deploy707.py: 1.72.708 = HAD-794 (package 3 of the long-film gaps, Ben 19.11.2026 "מוצר גמור"):
every buyer capability on every project page, in every language, as shared components.
  NEW  inc/project-shell.php: (1) H Infinity, FIRST Sde Dov (5 languages), Gindi Vogue (4) and Einstein Tower join the stage
       shell through the new 'nadlan_ps_config' filter, on ONE shared massing stage; (2) one action row on every developer
       project page in every language (live video call now: package 2's /tour/designer/?project=&call=1&lang=, or the page's
       own live room; the designer for this project; the film where the page has none, Ashira's showroom film; the 360 where the
       page has one; the basket slot package 4 fills); (3) the hero's video-call button opens one sheet: now, or book a time.
  NEW  assets/project-shell/shell.js, shell.css; assets/project-stage/massing/massing.js (the shared stage: the fleet's events
       nl:floor / nl:facing / nl:floor-action / nl:floor-cta, so bridge.js gives the view from the floor and the map beam
       unchanged); massing/<project>/stage.js (data only) + poster.jpg + poster-716.jpg for h-infinity, first, gindi-vogue,
       einstein.
  HUNK inc/project-stage.php: nadlan_ps_config() returns apply_filters('nadlan_ps_config', ...), and requires project-shell.php.
No module-list change. engine.js and bridge.js untouched. Tests: scratchpad t_parts.php (no notices; Rainbow's parts unchanged),
t_shell.php (the row lands after the page's buttons on Rainbow, H Infinity, Ashira, Kikar, FIRST-en), the massing stage in a
headless Chrome (events, card, five languages, phone)."""
import os, sys, json, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

PREV, NEW = 707, 708
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")

# the live text of inc/project-stage.php (scripts/project-stage/live_read.py, read after 1.72.707): the repo copy must equal it
LIVE_PS_MD5 = os.environ.get("NL708_PS_MD5", "")
assert len(LIVE_PS_MD5) == 32, "set NL708_PS_MD5 to the live md5 of inc/project-stage.php (live_read.py)"
H1 = ("\tfunction nadlan_ps_config() {\n\t\treturn array(",
      "\tfunction nadlan_ps_config() {\n\t\treturn apply_filters( 'nadlan_ps_config', array( // HAD-794: inc/project-shell.php adds the massing-stage projects")
H2 = ("\t\t\t),\n\t\t);\n\t}\n}\n\n/* The stage's first picture in the page's own HTML",
      "\t\t\t),\n\t\t) );\n\t}\n}\nrequire_once __DIR__ . '/project-shell.php'; // HAD-794 (1.72.708): every capability on every project page, in every language\n\n/* The stage's first picture in the page's own HTML")

M = "assets/project-stage/massing/"
NEWF = ["inc/project-shell.php", "assets/project-shell/shell.js", "assets/project-shell/shell.css", M + "massing.js"]
for p in ("h-infinity", "first", "gindi-vogue", "einstein"):
    NEWF += [M + p + "/stage.js", M + p + "/poster.jpg", M + p + "/poster-716.jpg"]

A = "/wp-content/plugins/nadlan-config/"
BAD = "['Fatal error', 'Warning</b>', 'Notice</b>']"
ROWS = ("    ('/projects/h-infinity-somail-tel-aviv/?t708a=1', ['massing/h-infinity/stage.js', 'class=\"nlsh\"', 'id=\"nlps\"', 'nlsh-sheet'], %s, []),\n"
        "    ('/projects/first-sde-dov/?t708a=1', ['massing/first/stage.js', 'class=\"nlsh\"'], %s, []),\n"
        "    ('/projects/first-sde-dov-fr/?t708a=1', ['massing/first/stage.js', 'class=\"nlsh\"', 'Appel vid'], %s, []),\n"
        "    ('/projects/gindi-vogue-sde-dov-en/?t708a=1', ['massing/gindi-vogue/stage.js', 'Video call now'], %s, []),\n"
        "    ('/projects/einstein-tower/?t708a=1', ['massing/einstein/stage.js', 'nadlan-einstein-he-dossier-v1', 'class=\"nlsh\"'], %s, []),\n"
        "    ('/projects/rainbow-tel-aviv/?t708a=1', ['rainbow/stage.js', 'class=\"nlsh\"', 'data-nlps-ev=\"hero-pick\"'], %s, []),\n"
        "    ('/projects/ashira-sde-dov/?t708a=1', ['data-nlsh=\"film\"', 'film-showroom-en.mp4', 'ashira/stage.js'], %s, []),\n"
        "    ('/projects/hamedina/?t708a=1', ['class=\"nlsh\"', 'room=new'], %s, []),\n"
        "    ('/projects/zohi-sde-dov-ru/?t708a=1', ['class=\"nlsh\"', 'project=zohi-sde-dov'], %s, []),\n"
        "    ('%s%smassing.js?t708a=1', ['export function mount('], ['Fatal error'], []),\n"
        "    ('%sassets/project-shell/shell.js?t708a=1', ['nadlan:shell-ready'], ['Fatal error'], []),\n") % (BAD, BAD, BAD, BAD, BAD, BAD, BAD, BAD, BAD, A, M, A)
kl_release.build_release(PREV, NEW, NEWF, NEWF, {"inc/project-stage.php": [H1, H2]}, {"inc/project-stage.php": LIVE_PS_MD5}, ROWS,
                         "every project page: the live video call, the designer, the film, the 360 and the basket slot in one row, in every language; a 3D tower for H Infinity, FIRST, Gindi Vogue and Einstein",
                         "HAD-794 package 3: project shell + shared massing stage")

# two INHERITED rows assert what this release changes on purpose: H Infinity now has the stage shell, so it loads the basket
# (as Rainbow does) and the TogetherRoom's hero chooser (inc/together.php prints it on every stage page). Trim those tokens only.
_d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deploy%d.py" % NEW)
_t = open(_d, encoding="utf-8").read()
for _a, _b in [("['nadlan-project-article'], ['nadlan-basket-cfg', 'assets/basket/basket.js']", "['nadlan-project-article'], []"),
               ("['nadlan-project-article'], ['id=\"nadlan-together-chooser-js\"']", "['nadlan-project-article'], []"),
               # the ProjectTitle-layout row (first run of 708 rolled back on it): H Infinity had no stage, now it has the stage
               # shell; the stage tokens move from "forbidden" to "required", the title-layout tokens go, the rest stays
               ("'<h1 id=\"nl-project-page-title\" class=\"nlpt-h1\">', '<style id=\"nadlan-pt-css\">'], ['id=\"nl-project-page-title\" class=\"screen-reader-text\"', 'class=\"nlpc-site-header\"', 'id=\"nlps\"', 'nadlan-ps-importmap', 'nadlan-ps-bridge', 'class=\"nlps-page\"', 'class=\"nlpd\"']",
                "'id=\"nlps\"', 'nadlan-ps-importmap', 'nadlan-ps-bridge', 'class=\"nlps-page\"'], ['id=\"nl-project-page-title\" class=\"screen-reader-text\"', 'class=\"nlpc-site-header\"', 'class=\"nlpd\"']"),
               ("(\"/projects/h-infinity-somail-tel-aviv/\", ['nadlan-project-article', 'class=\"nlcard-facts\"',", "(\"/projects/h-infinity-somail-tel-aviv/\", ['nadlan-project-article',")]:
    _n = _t.count(_a)
    assert _n >= 1, ("inherited row not found", _a)
    _t = _t.replace(_a, _b)
open(_d, "w", encoding="utf-8", newline=chr(10)).write(_t)
print("trimmed the two inherited H Infinity rows (basket, together chooser)")
