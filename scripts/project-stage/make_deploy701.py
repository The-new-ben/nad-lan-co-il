# -*- coding: utf-8 -*-
"""make deploy701.py from deploy700.py: 1.72.701 = HAD-786 (owner 18.11.2026 night: "reputation, stars, like the biggest places").
A reputation layer on Claude Design board 20 (docs/design-lab/pro-forum/boards/board-20-stars-and-levels.png):
  NEW  inc/pro-forum-rep.php, assets/proforum/rep.css, assets/proforum/rep.js: points from verified events (the asker marked my
       answer 15, kudos 10, worked together 10, skill confirmed 3, a positive reaction 2 once a day per giver, a post 1 up to 5 a
       day), five star levels named after building stages (10 / 50 / 150 / 400 / 1000, the top one also needs 5 askers and 90
       days), the chip next to every name, the sheet that opens every number, the leaders of the last 30 days on the forum home,
       the public rules, the member's own line and a level-up notice. Fixture members (example.invalid) never count.
  SWAP inc/pro-forum.php (one require line).
A new file goes in BOTH lists. Built by an Opus agent from a brief, reviewed by the release session (SQL, route, escaping).
123 + 116 + 91 + 133 + 95 local tests pass. Rules come from the session's own reading of 20 platforms
(docs/research/2026-11-18-arena/REPUTATION-PROOF-HE.md)."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-700.json"), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
A = "/wp-content/plugins/nadlan-config/assets/proforum/"
ROWS = ("    ('/forum/?t701f=1', ['nlf-dir', 'nlfr-leaders', 'data-nlfr-rules', 'id=\"nlfr-rules\"', 'איך צוברים כוכבים', 'assets/proforum/rep.js'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n"
        "    ('/forum/6/?t701f=1', ['nlf-thread', 'id=\"nlfr-member\"', 'assets/proforum/rep.css', 'nlfc-roomrow'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n"
        "    ('/wp-json/nadlan/v1/forum/ping?t701f=1', ['\"loaded\":true', '\"public\":true'], [], []),\n"
        "    ('%srep.js?t701f=1', ['rep/member', 'data-nlfr-rules'], ['Fatal error'], []),\n"
        "    ('%srep.css?t701f=1', ['.nlfr-chip', '.nlfr-leaders'], ['Fatal error'], []),\n") % (A, A)
NEW = ["inc/pro-forum-rep.php", "assets/proforum/rep.css", "assets/proforum/rep.js"]
kl_release.build_release(700, 701, ["inc/pro-forum.php"] + NEW, NEW, {}, {}, ROWS,
                         "reputation: stars and five levels next to every name, where they came from, the leaders of the last 30 days, public rules",
                         "HAD-786 forum round: stars and levels (design board 20)")
