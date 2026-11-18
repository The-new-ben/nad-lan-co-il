# -*- coding: utf-8 -*-
"""make deploy705.py from deploy704.py: 1.72.705 = HAD-787 follow-up, two fixes found by the release session:
  SWAP inc/pro-forum-home.php: the Tax Authority's public files (data.nadlan.gov.il) refuse WordPress's default user agent, so the
       city/neighbourhood averages and the neighbourhood list came back empty; the request now names the site honestly
       ("NadLanForum/1.0 (+https://nad-lan.co.il/forum/)"), a failure is remembered 10 minutes (was an hour), new cache keys.
  SWAP inc/pro-forum-media.php, assets/proforum/media.css: a plan card whose first page the host cannot draw showed a blank white
       box; it now shows the grid with a "PDF" label."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-704.json"), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
A = "/wp-content/plugins/nadlan-config/assets/proforum/"
ROWS = ("    ('/wp-json/nadlan/v1/forum/home/nbhd?code=8600&t705f=1', ['65210661'], ['Fatal error'], []),\n"
        "    ('%smedia.css?t705f=1', ['.nlfmd-pdf-lbl'], ['Fatal error'], []),\n"
        "    ('/forum/?t705f=1', ['nlf-dir', 'assets/proforum/home.js'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n") % (A,)
kl_release.build_release(704, 705, ["inc/pro-forum-home.php", "inc/pro-forum-media.php", "assets/proforum/media.css"], [], {}, {}, ROWS,
                         "the apartment page reads the Tax Authority's public averages; plan cards show a PDF label",
                         "HAD-787 follow-up: public averages user agent, PDF card label")
