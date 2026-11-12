# -*- coding: utf-8 -*-
"""make deploy673.py from deploy672.py: 1.72.673 = HAD-726, Ben 12.11.2026 evening: "בכל כרטיס שיהיה embedded forum... לא
איזה כפתור בסוף הדף... שיכנסו לפורום ויעזבו אותי".
  SWAP inc/pro-forum-render.php: the forum itself (discussions of the card's field, collaborations, open requests, the people in
       the forum, the ask box) right under the header of EVERY professional card; the small neutral box at the end is gone, the
       "זה הכרטיס שלכם?" box stays at the end; a card whose person did not join says so in one line.
  SWAP inc/pro-forum.php: a fifth kind, "שיתוף פעולה" (collab).
  SWAP assets/proforum/forum.css: the styles of the card's forum.
  CHECKS: the 672 profile row asked for the neutral box; it is replaced by rows for the card's forum."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-672.json"), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
PRO = "/professionals/%D7%91%D7%99%D7%98%D7%95%D7%9F-%D7%9E%D7%90%D7%99%D7%A8/"
ROWS = ("    ('%s?t673f=1', ['nlf nlf-win nlf-emb', 'nlf-emb-item', 'מציע שיתוף פעולה', 'עוד לא הצטרף לפורום', 'nlf-emb-people', 'nlpp-req'], ['Fatal error', 'Warning</b>', 'id=\"nlsch\"', 'href=\"tel:', 'nlf nlf-neutral'], []),\n"
        "    ('/professionals/?t673f=1', [], ['Fatal error', 'Warning</b>'], []),\n"
        "    ('/forum/?t673f=1', ['nlf-dir', 'nlf-card'], ['Fatal error', 'Warning</b>'], []),\n") % PRO
kl_release.build_release(672, 673, ["inc/pro-forum.php", "inc/pro-forum-render.php", "assets/proforum/forum.css"], [], {}, {}, ROWS,
                         "the forum inside every professional card, right under the header; a collaboration kind",
                         "HAD-726 forum round: the forum embedded in every card")

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deploy673.py")
src = open(D, encoding="utf-8").read()
head, rest = src.split("CHECKS = [\n", 1)
body, tail = rest.split("\n]\n", 1)
keep, gone = [], 0
for ln in body.split("\n"):
    if "'nlf nlf-neutral', 'id=\"nlf-compose\"'" in ln:  # the 672 row that required the neutral box
        gone += 1
        continue
    keep.append(ln)
assert gone == 1, "expected the one 672 neutral-box row, found %d" % gone
open(D, "w", encoding="utf-8", newline="\n").write(head + "CHECKS = [\n" + "\n".join(keep) + "\n]\n" + tail)
print("dropped the 672 neutral-box row; deploy673.py rewritten")
