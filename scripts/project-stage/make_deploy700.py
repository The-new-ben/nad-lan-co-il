# -*- coding: utf-8 -*-
"""make deploy700.py from deploy699.py: 1.72.700 = HAD-786, a live defect found by the first real two-browser run of the shared
board (18.11.2026): the board's root class "nlfb" is also the class of the feature bar (inc/feature-bar.php), and the site skin
(assets/skin-a/skin-a.css) paints `body.nl-skin-a .nlfb` with a white surface, a border and a radius, all !important. On the live
site the board therefore opened WHITE with white header text and white buttons (invisible), on phone and desktop. The board was
only ever tested in a local lab without the skin. Fix: the board's own prefix is now "nlfsb" (free in the whole repo).
  SWAP assets/proforum/board.js, assets/proforum/board.css (the prefix only; no logic change)
Second live defect, found by the same run at phone width: /forum/ and /forum/<id>/ printed NO viewport meta (get_header() in this
block theme does not print one), so a real phone laid the forum out as a shrunk 980px desktop page. Public since 12.11.
  SWAP inc/pro-forum.php: one wp_head action prints the viewport meta on the forum's own pages and one-click pages."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-699.json"), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
A = "/wp-content/plugins/nadlan-config/assets/proforum/"
ROWS = ("    ('%sboard.js?t700f=1', ['nlfsb-svg', 'createBoard'], ['Fatal error', \"'nlfb-\"], []),\n"
        "    ('%sboard.css?t700f=1', ['.nlfsb{', '.nlfsb-head'], ['Fatal error', '.nlfb{'], []),\n"
        "    ('/forum/?t700f=1', ['nlf-dir', 'nlfc-roomband', 'name=\"viewport\"'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n"
        "    ('/forum/6/?t700f=1', ['nlf-thread', 'name=\"viewport\"'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n") % (A, A)
kl_release.build_release(699, 700, ["inc/pro-forum.php", "assets/proforum/board.js", "assets/proforum/board.css"], [], {}, {}, ROWS,
                         "the forum pages get the phone viewport tag; the shared board keeps its dark frame (its class no longer collides with the feature bar)",
                         "HAD-786 forum round: phone viewport on forum pages, shared board class collision fixed")

# 18.11.2026, after the first run rolled back: one INHERITED row (from 1.72.676) still asked board.css for the old prefix
# '.nlfb'. The prefix is the very thing this release renames, so that row now asks for the new one.
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deploy700.py")
src = open(D, encoding="utf-8").read()
OLD = "proforum/board.css?t700f=1', ['.nlfb'], ['Fatal error'], []),"
NEW = "proforum/board.css?t700f=1', ['.nlfsb'], ['Fatal error'], []),"
assert src.count(OLD) == 1, src.count(OLD)
open(D, "w", encoding="utf-8", newline="\n").write(src.replace(OLD, NEW))
print("inherited board.css row now asks for the new prefix; deploy700.py rewritten")
