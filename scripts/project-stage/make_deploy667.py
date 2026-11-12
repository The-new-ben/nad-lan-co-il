# -*- coding: utf-8 -*-
"""make deploy667.py from deploy666.py: 1.72.667 = HAD-726, the professionals' forum, first version, HIDDEN (12.11.2026).
  NEW  inc/pro-forum.php (+ pro-forum-render.php, pro-forum-admin.php, pro-forum-trades.php), assets/proforum/forum.css, forum.js
  HUNK inc/pro-network.php (live md5 0d0f76560f, read 12.11 17:25 UTC): one loader line at its end. NO module-list change.
  The forum answers only with ?forum=on (30-day cookie) or to an administrator; closed, /forum/ is the theme's 404 and every
  forum route answers 400, except GET nadlan/v1/forum/ping (200, {"loaded":true,"public":false}) which proves the module loads.
  Register records (people imported from public registers) never get a forum window, a phone or a mail: owner order 12.11."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

OLD = ("\t\twp_schedule_single_event( time() + 30, 'nadlan_pro_trade_backfill' );\n"
       "\t}\n"
       "}, 40 );\n")
NEW = ("\t\twp_schedule_single_event( time() + 30, 'nadlan_pro_trade_backfill' );\n"
       "\t}\n"
       "}, 40 );\n"
       "\n"
       "// 1.72.667 (HAD-726): the professionals' forum, hidden behind ?forum=on until the owner opens it (option nadlan_forum_public)\n"
       "if ( file_exists( __DIR__ . '/pro-forum.php' ) ) { require_once __DIR__ . '/pro-forum.php'; }\n")
# the header's "אנשי מקצוע" panel gains a forum column, printed only once the forum is public (nlf_public(), option
# nadlan_forum_public); while it is closed the menu is byte-identical to today
MOLD = ("\t\t$menus .= nadlan_hp_panel( 'אנשי מקצוע', array(\n"
        "\t\t\tarray( array( 'אנשי מקצוע לנדל״ן', array_slice( $profs, 0, 5 ) ) ),\n"
        "\t\t\tarray( array( ' ', array_slice( $profs, 5 ) ) ),\n"
        "\t\t\tarray( array( 'המאגר', array( array( 'כל המאגר', $u( '/professionals/' ), $fmt( $c['pros'] ) ), array( 'מתווכים', $u( '/brokers/' ) ), array( 'הצטרפות למאגר', $u( '/advertise/' ) ) ) ) ),\n"
        "\t\t) );\n")
MNEW = ("\t\t$menus .= nadlan_hp_panel( 'אנשי מקצוע', array_values( array_filter( array(\n"
        "\t\t\tarray( array( 'אנשי מקצוע לנדל״ן', array_slice( $profs, 0, 5 ) ) ),\n"
        "\t\t\tarray( array( ' ', array_slice( $profs, 5 ) ) ),\n"
        "\t\t\tarray( array( 'המאגר', array( array( 'כל המאגר', $u( '/professionals/' ), $fmt( $c['pros'] ) ), array( 'מתווכים', $u( '/brokers/' ) ), array( 'הצטרפות למאגר', $u( '/advertise/' ) ) ) ) ),\n"
        "\t\t\t// 1.72.667 (HAD-726): the professionals' forum, only when it is public (while closed the panel is unchanged)\n"
        "\t\t\t( function_exists( 'nlf_public' ) && nlf_public() ) ? array( array( 'פורום ושיתופי פעולה', array( array( 'פורום אנשי המקצוע', $u( '/forum/' ) ), array( 'בקשות פתוחות', $u( '/forum/?v=requests' ) ), array( 'הצטרפות לבעלי מקצוע', $u( '/forum/?join=1' ) ) ) ) ) : null,\n"
        "\t\t) ) ) );\n")
HUNKS = {"inc/pro-network.php": [(OLD, NEW)], "inc/home-v3.php": [(MOLD, MNEW)]}
LIVE = {"inc/pro-network.php": "0d0f76560f6da30f8a39ce1c026f66bf",  # live read docs/qa/live-read/20261112T172508Z, equal to the repo
        "inc/home-v3.php": None}  # filled below from the live read 20261112T180256Z (repo SAME)
import hashlib  # noqa: E402
LIVE["inc/home-v3.php"] = hashlib.md5(open(os.path.join(kl_release.REPO, "docs", "qa", "live-read", "20261112T180256Z", "inc", "home-v3.php"), "rb").read()).hexdigest()

rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-666.json"), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")

NEWF = ["inc/pro-forum.php", "inc/pro-forum-render.php", "inc/pro-forum-admin.php", "inc/pro-forum-trades.php",
        "assets/proforum/forum.css", "assets/proforum/forum.js"]
# markers that exist ONLY when the forum prints something; they must be absent from public pages while the gate is closed
MARK = ["nlf-card-zone", "nlf nlf-win", "nlf nlf-neutral", "nlf nlf-claim", "id=\"nlf-compose\"", "assets/proforum/forum.css",
        "assets/proforum/forum.js", "window.NLF=", "/forum/?v=requests"]
PRO = "/professionals/%D7%91%D7%99%D7%98%D7%95%D7%9F-%D7%9E%D7%90%D7%99%D7%A8/"
ROWS = ("    ('/wp-json/nadlan/v1/forum/ping?t667f=1', ['\"loaded\":true', '\"public\":false'], [], []),\n"
        "    ('%s?t667f=1', ['nlpp-wa'], ['Fatal error', 'Warning</b>'], %r),\n"
        "    ('/professionals/?t667f=1', [], ['Fatal error', 'Warning</b>'], %r),\n"
        "    ('/?t667f=1', [], ['Fatal error', 'Warning</b>'], %r),\n") % (PRO, MARK, MARK, MARK)
kl_release.build_release(666, 667, NEWF, NEWF, HUNKS, LIVE, ROWS,
                         "the professionals' forum is on the site, hidden: it answers only with ?forum=on",
                         "HAD-726 the professionals' forum, hidden")
