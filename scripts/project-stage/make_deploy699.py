# -*- coding: utf-8 -*-
"""make deploy699.py from deploy698.py: 1.72.699 = HAD-786 (owner 18.11.2026 evening: "I saw no video call anywhere").
An OPEN VIDEO ROOM that every visitor sees, on Claude Design board 19
(docs/design-lab/pro-forum/boards/board-19-video-room-everyone-sees.png):
  SWAP inc/pro-forum-call.php  : NLFC_ROOM_PEOPLE 6, open rooms (topic or the forum home), routes call/room, call/join, call/lock,
                                 status / token / open extended, the band (forum home) and the row (every live discussion, every card)
  SWAP inc/pro-forum-render.php: two one-line HOOK filters (nlf_home_after_start, nlf_card_after_mast)
  SWAP assets/proforum/call.js : the room button, the lobby, the join sheet from a link, "מי מצטרף?" (copy, WhatsApp, share,
                                 discussion members, lock), entry after a guest signs in
  SWAP assets/proforum/call.css: board 19 styles
No new file. Built by an Opus agent from a brief, reviewed by the release session (routes, guards, escaping).
123 + 116 + 91 + 133 local tests pass."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-698.json"), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
PRO = "/professionals/%D7%91%D7%99%D7%98%D7%95%D7%9F-%D7%9E%D7%90%D7%99%D7%A8/"
A = "/wp-content/plugins/nadlan-config/assets/proforum/"
ROWS = ("    ('/forum/?t699f=1', ['nlf-dir', 'nlfc-roomband', 'data-nlf-room=\"0\"', 'פתיחת חדר וידאו'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n"
        "    ('/forum/6/?t699f=1', ['nlf-thread', 'nlfc-roomrow', 'data-nlf-room=\"6\"', 'שיחת וידאו על הדיון הזה'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n"
        "    ('%s?t699f=1', ['nlf nlf-win nlf-emb', 'nlfc-roomrow', 'data-nlf-room=\"0\"'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n"
        "    ('/wp-json/nadlan/v1/forum/ping?t699f=1', ['\"loaded\":true', '\"public\":true'], [], []),\n"
        "    ('%scall.js?t699f=1', ['call/room', 'call/join', 'wa.me'], ['Fatal error'], []),\n"
        "    ('%scall.css?t699f=1', ['nlfc-roomband', 'nlfc-roomrow'], ['Fatal error'], []),\n") % (PRO, A, A)
kl_release.build_release(698, 699, ["inc/pro-forum-call.php", "inc/pro-forum-render.php", "assets/proforum/call.js", "assets/proforum/call.css"],
                         [], {}, {}, ROWS,
                         "an open video room every visitor sees: forum home, every discussion, every card; invite by link and WhatsApp",
                         "HAD-786 forum round: open video room (design board 19)")
