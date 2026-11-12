# -*- coding: utf-8 -*-
"""make deploy675.py from deploy674.py: 1.72.675 = HAD-726, a fix seen with eyes on the live card right after 1.72.674:
  SWAP assets/proforum/forum.css: the theme paints every h2 dark, in its own face, and underlines links with !important, so
       the forum's title on the dark masthead was unreadable and the discussion titles were underlined. Stronger rules for
       the masthead title, the requests heading and the links inside the card's forum. No PHP, no markup change."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-674.json"), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
ROWS = "    ('/wp-content/plugins/nadlan-config/assets/proforum/forum.css?t675f=1', ['nlf-emb-mast h2.nlf-emb-h', 'text-decoration:none !important'], [], []),\n"
kl_release.build_release(674, 675, ["assets/proforum/forum.css"], [], {}, {}, ROWS,
                         "the card forum's title readable on its dark masthead; no underlines on discussion titles",
                         "HAD-726 forum round: live-look fix of the card forum")
