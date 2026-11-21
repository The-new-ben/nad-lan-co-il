# -*- coding: utf-8 -*-
"""RUN ON 21.11.2026 as 1.72.733 after Ben's yes on the heading (through the coordinator). Was: PREPARED, NOT RUN (HAD-787, board 24): the questions block at the end of /sde-dov/ and /projects/hamedina/.
Waits for Ben's word on the heading ("שאלות של קונים על <מקום>"), passed by the coordinator session. Until then: do not run.

  python scripts/project-stage/make_deploy_place.py <PREV> <NEW>      e.g. 731 732 (PREV = the live version, check health first)
  then: deploy<NEW>.py --dry, then the real run, then tools/content_first_check.py and tools/source_audit.py on both pages.

  NEW  inc/pro-forum-place.php, assets/proforum/place.js, assets/proforum/place.css: the block after the article (kicker, heading,
       one-line ask box that opens the forum's own compose sheet, the three latest discussions of the place, the link to all of
       them), the place tag on a discussion, /forum/?place=<key> (canonical stays /forum/), the place chip and the link back on the
       discussion page. No new address, no noindex, no redirect, no JSON-LD on the place page. The video room row is NOT in it.
  SWAP inc/pro-forum.php, inc/pro-forum-render.php (one-line hooks + the require line). No other session touched these two files
       since 1.72.705 (git log, 21.11.2026), so the repo copies are live + this change.
If Ben gives another heading: change it in nlfp2 defaults (inc/pro-forum-place.php) AND in H below before building.
123 + 116 + 91 + 133 + 95 + 132 + 106 + 84 + 45 local tests pass."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

PREV, NEWV = int(sys.argv[1]), int(sys.argv[2])
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
E = ['Fatal error', 'Warning</b>', 'Notice</b>']
H = {"sde-dov": "שאלות של קונים על שדה דב", "hamedina": "שאלות של קונים על כיכר המדינה"}  # the wording Ben approves
A = "/wp-content/plugins/nadlan-config/assets/proforum/"
T = "?t%dp=1" % NEWV
ROWS = ("    ('/sde-dov/%s', ['data-nlfpl=\"sde-dov\"', %r, 'assets/proforum/place.js', 'id=\"nlf-compose\"'], %r, []),\n"
        "    ('/projects/hamedina/%s', ['data-nlfpl=\"hamedina\"', %r, 'assets/proforum/place.js', 'id=\"nlf-compose\"'], %r, []),\n"
        "    ('/forum/?place=sde-dov&t%dp=1', ['nlf-dir', 'nlfpl-fchip', 'rel=\"canonical\" href=\"https://nad-lan.co.il/forum/\"'], %r, []),\n"
        "    ('/forum/%s', ['nlf-dir', 'nlfc-roomband'], %r + ['nlfpl-fchip'], []),\n"
        "    ('/projects/rainbow-tel-aviv/%s', ['nlsh'], %r + ['data-nlfpl'], []),\n"
        "    ('%splace.js%s', ['nlfExtra'], ['Fatal error'], []),\n"
        "    ('%splace.css%s', ['.nlfpl', '.nlfpl-box'], ['Fatal error'], []),\n"
        "    ('/wp-json/nadlan/v1/forum/ping%s', ['\"loaded\":true', '\"public\":true'], [], []),\n") % (
            T, H["sde-dov"], E, T, H["hamedina"], E, NEWV, E, T, E, T, E, A, T, A, T, T)
NEW = ["inc/pro-forum-place.php", "assets/proforum/place.js", "assets/proforum/place.css"]
kl_release.build_release(PREV, NEWV, ["inc/pro-forum.php", "inc/pro-forum-render.php"] + NEW, NEW, {}, {}, ROWS,
                         "buyers' questions at the end of the Sde Dov and Kikar HaMedina pages, from the forum",
                         "HAD-787: the forum block inside two place pages (design board 24)")
