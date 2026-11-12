# -*- coding: utf-8 -*-
"""make deploy668.py from deploy667.py: 1.72.668 = HAD-726, the professionals' forum, round 2 (12.11.2026), still HIDDEN.
  NEW  inc/pro-forum-call.php, assets/proforum/call.js, call.css: one-tap video calls between two people already talking in
       a discussion or a request (LiveKit through the shared project's edge function, rooms nadlan-frm-*, 8 a day per member,
       40 a day for the forum, no recording, no mail to the owner).
  SWAP inc/pro-forum.php (loads the call module), inc/pro-forum-render.php (the forum pages open and close with the theme's
       own header and footer, as the directory does: 1.72.667 printed WordPress's fallback header and a second h1).
  HUNK inc/professional-profile.php (live md5 9bfb9726b6, read 12.11 17:25 UTC; the repo copy was synced to it): once the
       forum is public, a register record's "פנייה בוואטסאפ" ("אשמח לחיבור אל ... דרך האתר", the site's own number) and
       "קבלו הצעת מחיר" (a mail to the site owner) become one "פרסמו בקשה" (owner order 12.11: take me out of the loop; the
       floating site WhatsApp with its "מקור:" line stays). While the forum is hidden the profile is byte-identical."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

A_OLD = ("<?php if ( $wa ) : ?><a class=\"nlpp-btn nlpp-wa\" target=\"_blank\" rel=\"noopener\" href=\"https://wa.me/<?php echo esc_attr( $wa ); ?>?text=<?php echo rawurlencode( 'היי, אשמח לחיבור אל ' . $name . ' דרך האתר' ); ?>\">פנייה בוואטסאפ</a><?php endif; ?>")
A_NEW = ("<?php $nlf_req = function_exists( 'nlf_public' ) && nlf_public(); /* 1.72.668 (HAD-726, owner 12.11.2026): the forum request replaces the site's \"connect me\" WhatsApp */ ?>"
         "<?php if ( $nlf_req ) : ?><a class=\"nlpp-btn nlpp-wa nlpp-req\" href=\"#nlf-card-zone\">פרסמו בקשה</a>"
         "<?php elseif ( $wa ) : ?><a class=\"nlpp-btn nlpp-wa\" target=\"_blank\" rel=\"noopener\" href=\"https://wa.me/<?php echo esc_attr( $wa ); ?>?text=<?php echo rawurlencode( 'היי, אשמח לחיבור אל ' . $name . ' דרך האתר' ); ?>\">פנייה בוואטסאפ</a><?php endif; ?>")
B_OLD = "<?php elseif ( ! $is_broker ) : /* the quote request"
B_NEW = "<?php elseif ( ! $is_broker && empty( $nlf_req ) ) : /* the quote request"
HUNKS = {"inc/professional-profile.php": [(A_OLD, A_NEW), (B_OLD, B_NEW)]}
LIVE = {"inc/professional-profile.php": "9bfb9726b679b5a95464e47faf82ebb5"}

rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-667.json"), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")

FILES = ["inc/pro-forum.php", "inc/pro-forum-render.php", "inc/pro-forum-call.php", "assets/proforum/call.js", "assets/proforum/call.css"]
NEWF = ["inc/pro-forum-call.php", "assets/proforum/call.js", "assets/proforum/call.css"]
MARK = ["nlf-card-zone", "nlf nlf-win", "nlf nlf-neutral", "nlf nlf-claim", "id=\"nlf-compose\"", "assets/proforum/forum.css",
        "assets/proforum/forum.js", "assets/proforum/call.js", "window.NLF=", "/forum/?v=requests", "nlpp-req"]
PRO = "/professionals/%D7%91%D7%99%D7%98%D7%95%D7%9F-%D7%9E%D7%90%D7%99%D7%A8/"
ROWS = ("    ('/wp-json/nadlan/v1/forum/ping?t668f=1', ['\"loaded\":true', '\"public\":false'], [], []),\n"
        "    ('%s?t668f=1', ['nlpp-wa', 'פנייה בוואטסאפ'], ['Fatal error', 'Warning</b>'], %r),\n"  # run 1 asked for the wa text, which the link carries %-encoded
        "    ('/professionals/?t668f=1', [], ['Fatal error', 'Warning</b>'], %r),\n"
        "    ('/?t668f=1', [], ['Fatal error', 'Warning</b>'], %r),\n") % (PRO, MARK, MARK, MARK)
kl_release.build_release(667, 668, FILES, NEWF, HUNKS, LIVE, ROWS,
                         "the forum's video calls and its own site header are on the site, still hidden (?forum=on)",
                         "HAD-726 forum round 2: video calls, the site header, the profile request (when public)")
