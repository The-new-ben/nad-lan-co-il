# -*- coding: utf-8 -*-
"""make deploy674.py from deploy673.py: 1.72.674 = HAD-726, Ben 12.11.2026 night: "תעבוד רק עם Claude Design... אל תעשה לי
דברים שנראים זולים". The forum inside every professional card is rebuilt on Claude Design board 15
(docs/design-lab/pro-forum, https://claude.ai/artifact/6pVfLsFgiNgMWDDWK6XhkC#play-2d348d6ecb35).
  SWAP inc/pro-forum-render.php: nlf_card_embed() on the board: a dark masthead with the people who take part, the leading
       discussion as a conversation (opening message + latest answer), the others as rows with the count in a tinted square,
       open requests, the ask box on ink; the "did not join" line under the forum.
  SWAP assets/proforum/forum.css: the styles of that design (the 673 block replaced).
  NOT in this release: assets/proforum/board.js and the call.js change (the shared board in the call). The owner rejected its
       first look; it is rebuilt on boards 16 and 17 first. The repo copy of call.js differs from live on purpose.
  CHECKS: the 673 profile row named classes of the old markup; it is replaced."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-673.json"), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
PRO = "/professionals/%D7%91%D7%99%D7%98%D7%95%D7%9F-%D7%9E%D7%90%D7%99%D7%A8/"
ROWS = ("    ('%s?t674f=1', ['nlf nlf-win nlf-emb', 'nlf-emb-mast', 'nlf-emb-feat', 'nlf-emb-ask', 'מציע שיתוף פעולה', 'עוד לא הצטרף לפורום', 'nlpp-req'], ['Fatal error', 'Warning</b>', 'id=\"nlsch\"', 'href=\"tel:', 'nlf nlf-neutral'], []),\n"
        "    ('/wp-content/plugins/nadlan-config/assets/proforum/forum.css?t674f=1', ['nlf-emb-mast', 'nlf-emb-bub'], [], []),\n") % PRO
kl_release.build_release(673, 674, ["inc/pro-forum-render.php", "assets/proforum/forum.css"], [], {}, {}, ROWS,
                         "the forum inside every professional card, rebuilt on the Claude Design board",
                         "HAD-726 forum round: the card forum on design board 15")

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deploy674.py")
src = open(D, encoding="utf-8").read()
head, rest = src.split("CHECKS = [\n", 1)
body, tail = rest.split("\n]\n", 1)
keep, gone = [], 0
for ln in body.split("\n"):
    if "'nlf-emb-item'" in ln and "'nlf-emb-people'" in ln:  # the 673 row of the old markup
        gone += 1
        continue
    keep.append(ln)
assert gone == 1, "expected the one 673 old-markup row, found %d" % gone
open(D, "w", encoding="utf-8", newline="\n").write(head + "CHECKS = [\n" + "\n".join(keep) + "\n]\n" + tail)
print("dropped the 673 old-markup row; deploy674.py rewritten")
