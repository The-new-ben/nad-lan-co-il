# -*- coding: utf-8 -*-
"""make deploy672.py from deploy671.py: 1.72.672 = HAD-726, the first round after the forum went PUBLIC (12.11.2026).
  SWAP inc/pro-forum-render.php: while the forum is public, a professional card whose person did not join (a register record)
       gets no "תיאום מועד ביומן" scheduler band or button (its host is the site admin, a dead end); "פרסמו בקשה" is the way in.
  CHECKS: the rows inherited from 667-671 asserted the HIDDEN state ("public":false, no forum markup); the forum is public since
       forum_switch.py on, so they are dropped here and public rows take their place."""
import os, sys, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-671.json"), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
PRO = "/professionals/%D7%91%D7%99%D7%98%D7%95%D7%9F-%D7%9E%D7%90%D7%99%D7%A8/"
ROWS = ("    ('/wp-json/nadlan/v1/forum/ping?t672f=1', ['\"loaded\":true', '\"public\":true'], [], []),\n"
        "    ('/forum/?t672f=1', ['nlf-dir', '/forum/?join=1', 'assets/proforum/forum.js'], ['Fatal error', 'Warning</b>', 'noindex'], []),\n"
        "    ('/forum/?v=requests&t672f=1', ['בקשות פתוחות'], ['Fatal error', 'Warning</b>'], []),\n"
        "    ('%s?t672f=1', ['nlpp-req', 'nlf nlf-neutral', 'id=\"nlf-compose\"'], ['Fatal error', 'Warning</b>', 'id=\"nlsch\"', 'href=\"tel:'], []),\n"
        "    ('/?t672f=1', ['פורום ושיתופי פעולה'], ['Fatal error', 'Warning</b>'], []),\n") % PRO
kl_release.build_release(671, 672, ["inc/pro-forum-render.php"], [], {}, {}, ROWS,
                         "no calendar booking on the cards of people who did not join; the request button is the way in",
                         "HAD-726 forum round: scheduler off on register cards")

# drop the inherited hidden-state rows (they would now fail on a public forum and roll back a good release)
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deploy672.py")
src = open(D, encoding="utf-8").read()
head, rest = src.split("CHECKS = [\n", 1)
body, tail = rest.split("\n]\n", 1)
keep, gone = [], 0
for ln in body.split("\n"):
    if "'\"public\":false'" in ln or ("'nlf-card-zone'" in ln and "t672f=1" in ln and "t672f=1', ['nlpp-req'" not in ln):
        gone += 1
        continue
    keep.append(ln)
assert gone >= 10, "expected the hidden-state rows, found %d" % gone
assert sum(1 for ln in keep if "t672f=1" in ln and "public\":true" in ln) == 1
open(D, "w", encoding="utf-8", newline="\n").write(head + "CHECKS = [\n" + "\n".join(keep) + "\n]\n" + tail)
print("dropped %d hidden-state rows; deploy672.py rewritten" % gone)
