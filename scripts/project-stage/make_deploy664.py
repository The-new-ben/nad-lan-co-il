# -*- coding: utf-8 -*-
"""make deploy664.py from deploy663.py: 1.72.664 = HAD-712, Ben 11.11.2026 night: "a tap on video opens live video" (the small part; the
call module itself is the designer session's, HAD-706, and is wired later through its CALL-CONTRACT.md).
  HUNKS  inc/together.php (the LIVE text, read 11.11.2026 22:40 UTC into docs/qa/live-read/20261111T224003Z; the repo copy was behind):
         - nadlan_tr_open_always(): the Kikar pages (hamedina, hamedina-en, hamedina-fr) open a room at any time;
         - the room route: a visitor on those pages gets a room without the "representative available" box, with two caps
           (8 rooms a day per visitor address, 40 a day on the site); the owner's mail with the join link is the existing listener
           (inc/project-stage.php, nadlan_together_room_created);
         - /room/available?post=<id> answers yes for those pages; the hero button's question carries the page id.
         inc/project-stage.php (the 663 text): the cockpit's availability address carries the page id.
  FILES  assets/together/together.js: a signed-in representative opening the mailed link joins as the representative; after a minute
         without a representative, a card offers a time (#nlsch), WhatsApp, or keep waiting; the English room says "NadLan advisor"."""
import hashlib, json, os, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

PREV, NEWV = 663, 664
REPO = kl_release.REPO; PLUG = kl_release.PLUG
md5 = lambda b: hashlib.md5(b).hexdigest()
LIVE_TP = os.path.join(REPO, "docs", "qa", "live-read", "20261111T224003Z", "inc", "together.php")
assert md5(open(LIVE_TP, "rb").read()).startswith("98399e3d80"), "the live together.php copy is not the one read on 11.11"
dst = os.path.join(PLUG, "inc", "together.php")
if md5(open(dst, "rb").read()) != md5(open(LIVE_TP, "rb").read()):
    shutil.copyfile(LIVE_TP, dst)  # the repo catches up with the live text first; the hunks then apply to exactly what is live
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
LIVE = {"inc/together.php": md5(open(LIVE_TP, "rb").read()),
        "inc/project-stage.php": (rp.get("files") or {}).get("inc/project-stage.php") or md5(open(os.path.join(PLUG, "inc", "project-stage.php"), "rb").read())}
OPEN = ("if ( ! function_exists( 'nadlan_tr_open_always' ) ) {\n"
        "\t/** HAD-712 (Ben, 11.11.2026: \"a tap on video opens live video\"): the Kikar pages open a shared room at any time, without the\n"
        "\t *  \"representative available\" box; the owner gets the join link by mail (inc/project-stage.php, nadlan_together_room_created). */\n"
        "\tfunction nadlan_tr_open_always( $pid ) {\n"
        "\t\treturn in_array( (string) get_post_field( 'post_name', (int) $pid ), array( 'hamedina', 'hamedina-en', 'hamedina-fr' ), true );\n"
        "\t}\n"
        "\t/** the site-wide daily cap for those always-open rooms (40 a day): true while under it, and counts this one */\n"
        "\tfunction nadlan_tr_open_day() {\n"
        "\t\t$k = 'nltr_open_day_' . gmdate( 'Ymd' );\n"
        "\t\t$n = (int) get_transient( $k );\n"
        "\t\tif ( $n >= 40 ) { return false; }\n"
        "\t\tset_transient( $k, $n + 1, DAY_IN_SECONDS );\n"
        "\t\treturn true;\n"
        "\t}\n"
        "}\n")
REPNOW = "\tfunction nadlan_tr_rep_now() { return '1' === (string) nadlan_tr_opt( 'rep_now', '0' ); }\n}\n"
GATE = "\t\t\tif ( ! $rep && ! nadlan_tr_rep_now() ) { return nadlan_tr_err( 'no_rep', 403 ); }\n"
AVAIL = ("\t\t'callback'            => function () {\n"
         "\t\t\t$r = new WP_REST_Response( array( 'ok' => true, 'now' => nadlan_tr_rep_now() ), 200 );\n")
HERO = "esc_url_raw( rest_url( 'nadlan/v1/room/available' ) )"
HUNKS = {
    "inc/together.php": [
        (REPNOW, REPNOW + OPEN),
        (GATE, "\t\t\t$always = ! $rep && ! nadlan_tr_rep_now() && nadlan_tr_open_always( $pid ); // 1.72.664 (HAD-712)\n"
               "\t\t\tif ( ! $rep && ! nadlan_tr_rep_now() && ! $always ) { return nadlan_tr_err( 'no_rep', 403 ); }\n"
               "\t\t\tif ( $always && ( ! nadlan_tr_rl( 'room_day', 8, DAY_IN_SECONDS ) || ! nadlan_tr_open_day() ) ) { return nadlan_tr_err( 'rate', 429 ); }\n"),
        (AVAIL, "\t\t'callback'            => function ( WP_REST_Request $req ) {\n"
                "\t\t\t$r = new WP_REST_Response( array( 'ok' => true, 'now' => nadlan_tr_rep_now() || nadlan_tr_open_always( (int) $req->get_param( 'post' ) ) ), 200 ); // 1.72.664\n"),
        (HERO, "esc_url_raw( add_query_arg( 'post', (int) ( nadlan_ps_current()['id'] ?? 0 ), rest_url( 'nadlan/v1/room/available' ) ) )"),
    ],
    "inc/project-stage.php": [
        ("'avail'  => function_exists( 'rest_url' ) ? rest_url( 'nadlan/v1/room/available' ) : '',",
         "'avail'  => function_exists( 'rest_url' ) ? add_query_arg( 'post', (int) ( $ps['id'] ?? 0 ), rest_url( 'nadlan/v1/room/available' ) ) : '', // 1.72.664 (HAD-712): the page id, so the Kikar pages answer yes"),
    ],
}
FILES = ["assets/together/together.js"]
ROWS = ("    ('/wp-json/nadlan/v1/room/available?post=8113&t664v=1', ['\"now\":true'], [], []),\n"
        "    ('/wp-json/nadlan/v1/room/available?post=8114&t664v=1', ['\"now\":true'], [], []),\n"
        "    ('/wp-content/plugins/nadlan-config/assets/together/together.js?t664v=1', ['function waitCheck()', \"keepWait: 'Keep waiting'\", 'NadLan advisor'], [], []),\n"
        "    ('/projects/hamedina/?t664v=1', ['room\\\\/available?post='], ['Fatal error', 'Warning</b>'], []),\n")
kl_release.build_release(PREV, NEWV, FILES, [], HUNKS, LIVE, ROWS, "a tap on video opens a room on the Kikar pages; the owner gets the link; the wait card after a minute",
                         "Kikar video opens at once")
