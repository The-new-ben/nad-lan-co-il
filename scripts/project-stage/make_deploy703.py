# -*- coding: utf-8 -*-
"""make deploy703.py from deploy702.py: 1.72.703 = HAD-787 (owner 18.11.2026 night: "צ'אט... בתוך החדר וידאו"). Claude Design board 22
(docs/design-lab/pro-forum/boards/board-22-chat-in-video-room.png):
  NEW  inc/pro-forum-chat.php, assets/proforum/chat.js: chat inside the forum's video room: history per room for whoever is in it
       (late joiners see what was written), pictures and plans through the media module, word reactions, one pinned message,
       report and delete, a toast over the video and an unread counter, and at the end the host attaches "מה סוכם בשיחה" to the
       discussion as one answer (normal moderation and counters). Unattached chat is deleted after 7 days.
  SWAP inc/pro-forum.php (one require line), assets/proforum/call.js (the chat button, the end sheet), assets/proforum/call.css.
Built by an Opus agent in its own worktree from a brief, reviewed and merged by the release session.
123 + 116 + 91 + 133 + 95 + 132 + 106 local tests pass."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-702.json"), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
A = "/wp-content/plugins/nadlan-config/assets/proforum/"
ROWS = ("    ('%schat.js?t703f=1', ['export function createChat(', 'הודעות מלפני שנכנסת'], ['Fatal error'], []),\n"
        "    ('%scall.js?t703f=1', [\"new URL('chat.js' + u.search, u)\", 'bChat'], ['Fatal error'], []),\n"
        "    ('%scall.css?t703f=1', ['.nlfch-panel'], ['Fatal error'], []),\n"
        "    ('/forum/?t703f=1', ['nlf-dir', 'nlfc-roomband', 'assets/proforum/media.js'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n"
        "    ('/forum/6/?t703f=1', ['nlf-thread', 'nlfc-roomrow'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n"
        "    ('/wp-json/nadlan/v1/forum/ping?t703f=1', ['\"loaded\":true', '\"public\":true'], [], []),\n") % (A, A, A)
NEW = ["inc/pro-forum-chat.php", "assets/proforum/chat.js"]
kl_release.build_release(702, 703, ["inc/pro-forum.php", "assets/proforum/call.js", "assets/proforum/call.css"] + NEW, NEW, {}, {}, ROWS,
                         "chat inside the forum video room: history, pictures, reactions, pin, and the summary into the discussion",
                         "HAD-787 forum round: chat in the video room (design board 22)")
