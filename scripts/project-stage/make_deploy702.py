# -*- coding: utf-8 -*-
"""make deploy702.py from deploy701.py: 1.72.702 = HAD-787 (owner 18.11.2026 night: "תמונות וקבצים בהודעות", the best standard as
our floor, with proof). Claude Design board 21 (docs/design-lab/pro-forum/boards/board-21-images-files-member-picture.png):
  NEW  inc/pro-forum-media.php, assets/proforum/media.js, assets/proforum/media.css: up to 20 pictures/plans on a discussion and 10 on
       an answer (camera, gallery, PDF, drag, paste, reorder, caption), shrunk in the browser and re-encoded on the server (location
       and all metadata removed), gallery + full-screen viewer, "mark a point and ask", a plan opens on the shared board in the video
       room, a member picture that replaces the initials. Tables nadlan_forum_media + nadlan_forum_pins.
  SWAP inc/pro-forum.php, inc/pro-forum-render.php (one-line hooks + the require line), assets/proforum/forum.js (form extras),
       assets/proforum/call.js (board event), assets/proforum/board.js (takeImage entry point).
Built by an Opus agent from a brief, reviewed by the release session. 123 + 116 + 91 + 133 + 95 + 132 local tests pass.
Standard evidence: docs/research/2026-11-18-arena/MEDIA-CHAT-PROOF-HE.md (pages opened by the session)."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-701.json"), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
A = "/wp-content/plugins/nadlan-config/assets/proforum/"
ROWS = ("    ('/forum/?t702f=1', ['nlf-dir', 'assets/proforum/media.js', 'assets/proforum/media.css', 'window.NLFMD=', 'nlfr-leaders'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n"
        "    ('/forum/6/?t702f=1', ['nlf-thread', 'assets/proforum/media.js', '\"topic\":6', 'nlfc-roomrow'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n"
        "    ('/forum/11/?t702f=1', ['nlf-thread', 'assets/proforum/media.js'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n"
        "    ('/wp-json/nadlan/v1/forum/ping?t702f=1', ['\"loaded\":true', '\"public\":true'], [], []),\n"
        "    ('%smedia.js?t702f=1', ['nlfmd-lb', 'nlfExtra'], ['Fatal error'], []),\n"
        "    ('%smedia.css?t702f=1', ['.nlfmd-gal', '.nlfmd-lb'], ['Fatal error'], []),\n"
        "    ('%sforum.js?t702f=1', ['form.nlfExtra ? form.nlfExtra(path)'], ['Fatal error'], []),\n"
        "    ('%sboard.js?t702f=1', ['takeImage', 'nlfsb-svg'], ['Fatal error'], []),\n") % (A, A, A, A)
NEW = ["inc/pro-forum-media.php", "assets/proforum/media.js", "assets/proforum/media.css"]
kl_release.build_release(701, 702, ["inc/pro-forum.php", "inc/pro-forum-render.php", "assets/proforum/forum.js", "assets/proforum/call.js", "assets/proforum/board.js"] + NEW, NEW, {}, {}, ROWS,
                         "pictures, plans and files in forum posts: gallery, full-screen viewer, mark a point and ask, plan on the shared board, member picture",
                         "HAD-787 forum round: images, plans and files in posts (design board 21)")
