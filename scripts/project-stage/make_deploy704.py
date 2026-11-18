# -*- coding: utf-8 -*-
"""make deploy704.py from deploy703.py: 1.72.704 = HAD-787 (owner 18.11.2026 night: "דירה שמדברים עליה... מאפשרים לאנשים להעלות את
הדירה שלהם"). Claude Design board 23 (docs/design-lab/pro-forum/boards/board-23-apartment-people-talk-about.png):
  NEW  inc/pro-forum-home.php, assets/proforum/home.js, assets/proforum/home.css: a member presents an apartment (city, neighbourhood,
       street WITHOUT a number, rooms, m², floor, asking price, state, intent, photos through the media module); everyone votes
       זול / הוגן / יקר in one tap (guests too, one per browser); members give a price estimate in their answer (median and band,
       "דעות של חברי הפורום, לא שמאות"); beside it the Tax Authority's public average for the same rooms in the city and the
       neighbourhood (data.nadlan.gov.il, cached 7 days); "הדירה שמדברים עליה" card on the forum home; WhatsApp share.
  SWAP inc/pro-forum.php (nlf_kinds filter + require line), inc/pro-forum-render.php (one hook), assets/proforum/media.js (one line:
       the photo uploader in the apartment form).
Built by an Opus agent in its own worktree from a brief, reviewed and merged by the release session.
123 + 116 + 91 + 133 + 95 + 132 + 106 + 84 local tests pass."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-703.json"), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
A = "/wp-content/plugins/nadlan-config/assets/proforum/"
ROWS = ("    ('/forum/?t704f=1', ['nlf-dir', 'assets/proforum/home.js', 'assets/proforum/home.css', 'id=\"nlfh-compose\"', 'כמה הדירה שלכם שווה? תשאלו את הפורום'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n"
        "    ('/forum/6/?t704f=1', ['nlf-thread', 'nlfc-roomrow', 'assets/proforum/media.js'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n"
        "    ('/wp-json/nadlan/v1/forum/ping?t704f=1', ['\"loaded\":true', '\"public\":true'], [], []),\n"
        "    ('/wp-json/nadlan/v1/forum/home/nbhd?code=8600&t704f=1', ['items'], ['Fatal error'], []),  # the route answers; whether the public file was reachable from the host is checked after the release\n"
        "    ('%shome.js?t704f=1', ['home/vote'], ['Fatal error'], []),\n"
        "    ('%shome.css?t704f=1', ['.nlfh-'], ['Fatal error'], []),\n"
        "    ('%smedia.js?t704f=1', ['nlfmd-lb', 'nlfExtra'], ['Fatal error'], []),\n") % (A, A, A)
NEW = ["inc/pro-forum-home.php", "assets/proforum/home.js", "assets/proforum/home.css"]
kl_release.build_release(703, 704, ["inc/pro-forum.php", "inc/pro-forum-render.php", "assets/proforum/media.js"] + NEW, NEW, {}, {}, ROWS,
                         "the apartment people talk about: present an apartment, one-tap price vote, members' estimates, public averages",
                         "HAD-787 forum round: the apartment people talk about (design board 23)")
