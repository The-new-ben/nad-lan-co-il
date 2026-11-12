# -*- coding: utf-8 -*-
"""make deploy671.py from deploy670.py: 1.72.671 = HAD-726 fix found in the live check of 1.72.668 (12.11.2026), still HIDDEN.
  SWAP inc/pro-forum-render.php: the forum's sheets (compose, entry, request) print at wp_footer priority 5, before the footer
       scripts; at 20 they came after forum.js, which then found no sheet and no button opened. No PHP hunk, no new file."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-670.json"), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
MARK = ["nlf-card-zone", "nlf nlf-win", "nlf nlf-neutral", "nlf nlf-claim", "id=\"nlf-compose\"", "assets/proforum/forum.css",
        "assets/proforum/forum.js", "assets/proforum/call.js", "window.NLF=", "/forum/?v=requests", "nlpp-req"]
PRO = "/professionals/%D7%91%D7%99%D7%98%D7%95%D7%9F-%D7%9E%D7%90%D7%99%D7%A8/"
ROWS = ("    ('/wp-json/nadlan/v1/forum/ping?t671f=1', ['\"loaded\":true', '\"public\":false'], [], []),\n"
        "    ('%s?t671f=1', ['nlpp-wa', 'פנייה בוואטסאפ'], ['Fatal error', 'Warning</b>'], %r),\n"
        "    ('/?t671f=1', [], ['Fatal error', 'Warning</b>'], %r),\n") % (PRO, MARK, MARK)
kl_release.build_release(670, 671, ["inc/pro-forum.php", "inc/pro-forum-call.php", "assets/proforum/forum.css"], [], {}, {}, ROWS,
                         "a clean first message goes live by itself; the call style loads; error messages red (still hidden, ?forum=on)",
                         "HAD-726 forum round: auto-approval, call style handle, error colour")


