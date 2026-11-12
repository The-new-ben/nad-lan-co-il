# -*- coding: utf-8 -*-
"""make deploy665.py from deploy664.py: 1.72.665 = HAD-712 fix found by the Kikar session's real room test (12.11.2026):
  - On the English Kikar page every tap on video ended in "No connection to the server": POST nadlan/v1/room answered 400
    because nadlan_tr_project_ok() looks the page up in the stage config by its own slug, and the config is keyed by the
    Hebrew slug (hamedina). The English and French Kikar pages (hamedina-en, hamedina-fr) now pass on the Hebrew key; every
    other project and language page is unchanged.
  - The leave-a-time offer counts its minute from the join, not from the end of the video connection (it came late).
  HUNK  inc/together.php (the 664 text, live md5 de0ed3f0c1).   FILE  assets/together/together.js."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

OLD = ("\t\tif ( function_exists( 'nadlan_ps_config' ) ) {\n"
       "\t\t\t$all = nadlan_ps_config();\n"
       "\t\t\treturn isset( $all[ (string) get_post_field( 'post_name', $pid ) ] );\n"
       "\t\t}\n")
NEW = ("\t\tif ( function_exists( 'nadlan_ps_config' ) ) {\n"
       "\t\t\t$all  = nadlan_ps_config();\n"
       "\t\t\t$slug = (string) get_post_field( 'post_name', $pid );\n"
       "\t\t\t// 1.72.665 (HAD-712): the English and French Kikar pages share the Hebrew page's stage config (keyed hamedina)\n"
       "\t\t\tif ( function_exists( 'nadlan_tr_open_always' ) && nadlan_tr_open_always( $pid ) ) { $slug = 'hamedina'; }\n"
       "\t\t\treturn isset( $all[ $slug ] );\n"
       "\t\t}\n")
HUNKS = {"inc/together.php": [(OLD, NEW)]}
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-664.json"), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
LIVE = {"inc/together.php": rp["files"]["inc/together.php"]}  # de0ed3f0c1, the 664 text
ROWS = ("    ('/wp-content/plugins/nadlan-config/assets/together/together.js?t665v=1', ['counted from the join, not from the video connection', 'function waitCheck()'], [], []),\n"
        "    ('/wp-json/nadlan/v1/room/available?post=8114&t665v=1', ['\"now\":true'], [], []),\n"
        "    ('/projects/hamedina-en/?t665v=1', ['room\\\\/available?post=8114'], ['Fatal error', 'Warning</b>'], []),\n")
kl_release.build_release(664, 665, ["assets/together/together.js"], [], HUNKS, LIVE, ROWS,
                         "a tap on video opens a room on the English and French Kikar pages too; the offer counts from the join",
                         "the Kikar room on the English page")
