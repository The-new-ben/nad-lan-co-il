# -*- coding: utf-8 -*-
"""make deploy745.py from deploy744.py: 1.72.745 = film-made-real loop, cycle 1 (coordinator order 22.11.2026, Ben approved
everything in scope): from a project page to the buyers' questions about it, the way the film connects the project and the forum.
World reference: the questions-and-answers block on every Amazon product page (asked and answered by buyers, on the page itself).
  HUNK inc/pro-forum-place.php: eight places in nlfp2_places(), the module's own documented extension point ("TO ADD A PLACE: one
       line"): rainbow, duo, ashira, dimri-yama, h-infinity, first-sde-dov, gindi-vogue, einstein. Each project page then gets the
       forum's own block after the article (heading "שאלות של קונים על <name>", Ben's wording of 21.11), and /forum/?place=<key>.
  SWAP inc/project-shell.php: the project row gets "שאלות של קונים" -> /forum/?place=<key> on the Hebrew page of every project the
       forum lists (the forum speaks Hebrew, so the language pages keep their row as it is).
Live texts read 20261122T194323Z (pro-forum-place.php e98f26a247 = repo; project-shell.php 7384d40519 = 1.72.713)."""
import os, sys, json, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

PREV, NEW = 744, 745
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LR = os.path.join(REPO, "docs", "qa", "live-read", "20261122T194323Z", "inc")
LIVE_PF = open(os.path.join(LR, "pro-forum-place.php"), encoding="utf-8").read()
MD5_PF = hashlib.md5(LIVE_PF.encode("utf-8")).hexdigest()
assert MD5_PF.startswith("e98f26a247"), MD5_PF
OLD = "\t\t'hamedina' => array( 'כיכר המדינה', '/projects/hamedina/' ),\n"
NEWTXT = OLD + "".join("\t\t'%s' => array( '%s', '%s' ),\n" % x for x in (
    ("rainbow", "ריינבו תל אביב", "/projects/rainbow-tel-aviv/"),
    ("duo", "מגדלי DUO", "/projects/duo-tel-aviv/"),
    ("ashira", "אשירה", "/projects/ashira-sde-dov/"),
    ("dimri-yama", "דמרי ימה", "/projects/dimri-yama-sde-dov/"),
    ("h-infinity", "H Infinity", "/projects/h-infinity-somail-tel-aviv/"),
    ("first-sde-dov", "FIRST שדה דב", "/projects/first-sde-dov/"),
    ("gindi-vogue", "גינדי ווג", "/projects/gindi-vogue-sde-dov/"),
    ("einstein", "EINSTEIN TOWER", "/projects/einstein-tower/"),
))
assert LIVE_PF.count(OLD) == 1

BAD = "['Fatal error', 'Warning</b>', 'Notice</b>']"
ROWS = ("    ('/projects/rainbow-tel-aviv/?t745f=1', ['data-nlsh=\"ask\"', 'place=rainbow', 'שאלות של קונים על ריינבו תל אביב', 'id=\"nlps\"'], %s, []),\n"
        "    ('/projects/duo-tel-aviv/?t745f=1', ['place=duo', 'שאלות של קונים על מגדלי DUO'], %s, []),\n"
        "    ('/projects/einstein-tower/?t745f=1', ['place=einstein', 'nadlan-einstein-he-dossier-v1', 'massing/einstein/stage.js'], %s, []),\n"
        "    ('/projects/hamedina/?t745f=1', ['place=hamedina', 'class=\"nlsh\"'], %s, []),\n"
        "    ('/projects/rainbow-tel-aviv-en/?t745f=1', ['class=\"nlsh\"'], ['data-nlsh=\"ask\"', 'Fatal error'], []),\n"
        "    ('/forum/?place=gindi-vogue&t745f=1', ['גינדי ווג'], ['Fatal error'], []),\n") % (BAD, BAD, BAD, BAD)
kl_release.build_release(PREV, NEW, ["inc/project-shell.php"], [], {"inc/pro-forum-place.php": [(OLD, NEWTXT)]}, {"inc/pro-forum-place.php": MD5_PF}, ROWS,
                         "buyers' questions on every flagship project page, and a link to them in the project row",
                         "film loop cycle 1: project to forum questions")

# an INHERITED row asserted that Rainbow has no forum block (Rainbow was not a forum place until this release); trimmed on purpose
_d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deploy%d.py" % NEW)
_t = open(_d, encoding="utf-8").read()
_a = "['nlsh'], ['Fatal error', 'Warning</b>', 'Notice</b>'] + ['data-nlfpl'], [])"
print("trimmed inherited no-forum rows:", _t.count(_a))
_t = _t.replace(_a, "['nlsh'], ['Fatal error', 'Warning</b>', 'Notice</b>'], [])")
open(_d, "w", encoding="utf-8", newline=chr(10)).write(_t)
