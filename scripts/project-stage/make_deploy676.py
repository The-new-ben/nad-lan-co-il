# -*- coding: utf-8 -*-
"""make deploy676.py from deploy675.py: 1.72.676 = HAD-726, the social layer of the forum on Claude Design board 11
(owner 12.11.2026: "תרים את זה עד הסוף... עם כל הפיצ'רים של ה-reverse engineering"; loop rows 5 to 8).
  NEW  inc/pro-forum-social.php, assets/proforum/social.js, assets/proforum/social.css: five positive reactions (מפרגן, מועיל,
       מקצועי, יפה, תודה; old thanks rows keep counting as תודה), a private "לא עזר לי", kudos between members (one per pair,
       positive only, the receiver can hide), skill confirmations in one tap, "עבדו יחד" tags on a finished work, and the
       computed badge "עונה בדרך כלל תוך יום". Own tables through nlfs_install() (option nadlan_forum_social_db).
  SWAP inc/pro-forum.php: one require line at the end. inc/pro-forum-render.php: six filters marked HOOK (social module).
  SWAP assets/proforum/forum.css: the card forum's send button in raspberry and a white field (seen on the live 675).
  NEW  assets/proforum/board.js + board.css, SWAP assets/proforum/call.js: the shared board inside a forum video call, rebuilt
       on Claude Design boards 16 and 17 (video tiles on the sheet, a colour per person, pen, marker, arrow, shapes, numbered
       notes, measure with a stated scale, laser, eraser of own marks, follow mode, a photo or a plan from the phone, save as
       an image; only through the call's LiveKit data, nothing stored on the site). 44 two-person lab checks by its builder.
  Built by Opus agents, reviewed by the release session (routes go through nlf_guard: session, nonce, proof of work,
  rate limits; prepared SQL; POST confirm on the signed mail links). 91 + 123 + 85 local tests pass."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-675.json"), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
PRO = "/professionals/%D7%91%D7%99%D7%98%D7%95%D7%9F-%D7%9E%D7%90%D7%99%D7%A8/"
ROWS = ("    ('/forum/2/?t676f=1', ['nlf-thread', 'assets/proforum/social.js', 'assets/proforum/social.css', 'מפרגן'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n"
        "    ('/forum/?t676f=1', ['nlf-dir', 'nlf-card'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n"
        "    ('%s?t676f=1', ['nlf nlf-win nlf-emb', 'nlf-emb-ask'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n"
        "    ('/wp-json/nadlan/v1/forum/ping?t676f=1', ['\"loaded\":true', '\"public\":true'], [], []),\n"
        "    ('/wp-content/plugins/nadlan-config/assets/proforum/social.js?t676f=1', ['social/member', 'social/find'], ['Fatal error'], []),\n") % PRO
ROWS += ("    ('/wp-content/plugins/nadlan-config/assets/proforum/board.js?t676f=1', ['export function createBoard', 'board.css'], ['Fatal error'], []),\n"
         "    ('/wp-content/plugins/nadlan-config/assets/proforum/board.css?t676f=1', ['.nlfb'], ['Fatal error'], []),\n"
         "    ('/wp-content/plugins/nadlan-config/assets/proforum/call.js?t676f=1', ['BOARD_URL', 'createBoard'], ['Fatal error'], []),\n")
# a new file goes in BOTH lists (the first run of 676 passed them only as "new": nothing wrote them, the rows caught it, rolled back)
NEW = ["inc/pro-forum-social.php", "assets/proforum/social.js", "assets/proforum/social.css", "assets/proforum/board.js", "assets/proforum/board.css"]
kl_release.build_release(675, 676, ["inc/pro-forum.php", "inc/pro-forum-render.php", "assets/proforum/forum.css", "assets/proforum/call.js"] + NEW,
                         NEW, {}, {}, ROWS,
                         "reactions, kudos, skills and the response badge in the forum; a shared board in every forum video call",
                         "HAD-726 forum round: the social layer (board 11) and the shared board in the call (boards 16, 17)")
