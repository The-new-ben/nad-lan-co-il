# -*- coding: utf-8 -*-
"""make deploy669.py from deploy668.py: 1.72.669 = HAD-726 fix found in the live check of 1.72.668 (12.11.2026), still HIDDEN.
  SWAP inc/pro-forum-render.php: the forum's sheets (compose, entry, request) print at wp_footer priority 5, before the footer
       scripts; at 20 they came after forum.js, which then found no sheet and no button opened. No PHP hunk, no new file."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-668.json"), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
MARK = ["nlf-card-zone", "nlf nlf-win", "nlf nlf-neutral", "nlf nlf-claim", "id=\"nlf-compose\"", "assets/proforum/forum.css",
        "assets/proforum/forum.js", "assets/proforum/call.js", "window.NLF=", "/forum/?v=requests", "nlpp-req"]
PRO = "/professionals/%D7%91%D7%99%D7%98%D7%95%D7%9F-%D7%9E%D7%90%D7%99%D7%A8/"
ROWS = ("    ('/wp-json/nadlan/v1/forum/ping?t669f=1', ['\"loaded\":true', '\"public\":false'], [], []),\n"
        "    ('%s?t669f=1', ['nlpp-wa', 'פנייה בוואטסאפ'], ['Fatal error', 'Warning</b>'], %r),\n"
        "    ('/?t669f=1', [], ['Fatal error', 'Warning</b>'], %r),\n") % (PRO, MARK, MARK)
kl_release.build_release(668, 669, ["inc/pro-forum-render.php"], [], {}, {}, ROWS,
                         "the forum's buttons open their sheets (still hidden, ?forum=on)",
                         "HAD-726 forum fix: the sheets print before the footer scripts")
