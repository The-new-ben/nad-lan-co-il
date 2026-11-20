# -*- coding: utf-8 -*-
"""make deploy728.py from deploy727.py: 1.72.728 = HAD-795 package 6, sample people (coordinator's order 20.11.2026: a defect fix).
A sample person carried a phone shaped like a real mobile number (050-000-0xxx) and every stored phone became a wa.me / tel: link,
in the PUBLIC demo of version 1 and in the sample portfolio of version 2. A press could open a chat with a number that may be someone's.
  SWAP assets/rentals/rm-demo.js        the 10 sample people carry no phone and no e-mail; every name wears "(דוגמה)" / "(example)".
  SWAP assets/rentals/rm-core.js        N.isDemo, N.canMsg; N.wa gives no wa.me address inside a sample.
  SWAP assets/rentals/rm-drawers.js     in a sample: the contact card and the message sheet hold buttons, never wa.me / tel: / mailto: links;
                                        the message sheet shows the wording, a copy button and "journal entry"; no stand-in number for the owner.
  SWAP assets/rentals/rm-views.js       the people list: a button in a sample, the real links in a real account (unchanged).
  SWAP assets/rentals/rm-today.js       the reminder button stays for a sample tenant (it used to hang on the phone).
  SWAP assets/rentals/rm-boot.js        the signed-out sample landlord: marked as an example, no phone, no Bit number.
  SWAP assets/rentals/rental-manager.js version 1: in the demo the reminder shows its wording with a copy button and opens no chat.
  HUNK inc/rentals-manager.php          the demo answer carries no tenant phone (payload, the cached answer, the seed); a one-time clean
                                        of the stored sample portfolio; "(example)" as the mark on the English page.
Real accounts keep the real behaviour: every change is behind the sample flag.
Lab: lab_sample_people.py 39/39, lab_sample_people_v1.py --pre 12/12, lab_slice1_short.py, lab_slice1_fixes.py, lab_slice1.py. Headless Edge, not a real phone."""
import os, sys, json, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

PREV = 727
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
E = ['Fatal error', 'Warning</b>', 'Notice</b>']
FILES = ["assets/rentals/rm-demo.js", "assets/rentals/rm-core.js", "assets/rentals/rm-drawers.js", "assets/rentals/rm-views.js",
         "assets/rentals/rm-today.js", "assets/rentals/rm-boot.js", "assets/rentals/rental-manager.js"]
R = "inc/rentals-manager.php"
STRIP = "foreach ( $%s as $nk => $nu ) { if ( is_array( $nu ) ) { $%s[ $nk ]['tenant_phone'] = ''; } }"
H = [
    ("\t\t$units = json_decode( (string) get_post_meta( $id, 'rm_units', true ), true );\n\t\t$city  = (string) get_post_meta( $id, 'city', true );\n",
     "\t\t$units = json_decode( (string) get_post_meta( $id, 'rm_units', true ), true );\n"
     "\t\t/* 20.11.2026: a sample tenant carries no phone (a number shaped like a real one may be someone's); the mark reads in the page language */\n"
     "\t\tif ( is_array( $units ) && '1' === (string) get_post_meta( $id, 'is_demo', true ) ) {\n"
     "\t\t\tforeach ( $units as $nk => $nu ) {\n"
     "\t\t\t\tif ( ! is_array( $nu ) ) { continue; }\n"
     "\t\t\t\t$units[ $nk ]['tenant_phone'] = '';\n"
     "\t\t\t\tif ( 'he' !== $lang && ! empty( $nu['tenant_name'] ) ) { $units[ $nk ]['tenant_name'] = str_replace( '(דוגמה)', '(example)', (string) $nu['tenant_name'] ); }\n"
     "\t\t\t}\n"
     "\t\t}\n"
     "\t\t$city  = (string) get_post_meta( $id, 'city', true );\n"),
    ("\t\t\tforeach ( $p as &$x ) { $x['can_manage'] = false; }\n",
     "\t\t\tforeach ( $p as &$x ) {\n"
     "\t\t\t\t$x['can_manage'] = false;\n"
     "\t\t\t\tif ( isset( $x['units'] ) && is_array( $x['units'] ) ) { foreach ( $x['units'] as $nk => $nu ) { if ( is_array( $nu ) ) { $x['units'][ $nk ]['tenant_phone'] = ''; } } } // an answer cached before 20.11.2026\n"
     "\t\t\t}\n"
     "\t\t\tunset( $x );\n"),
    ("'tenant_phone' => '9725' . '00000001',", "'tenant_phone' => '',"),
    ("'tenant_phone' => '9725' . '00000002',", "'tenant_phone' => '',"),
    ("'tenant_phone' => '9725' . '00000003',", "'tenant_phone' => '',"),
    ("add_action( 'save_post_nadlan_rentalprop', function () { foreach ( array( 'he', 'en' ) as $l ) { delete_transient( 'nlrm_demo_payload_' . $l ); } } );\n",
     "add_action( 'save_post_nadlan_rentalprop', function () { foreach ( array( 'he', 'en' ) as $l ) { delete_transient( 'nlrm_demo_payload_' . $l ); } } );\n"
     "\n"
     "/* 20.11.2026: sample tenants carry no phone. One-time clean of the STORED sample portfolio (the seed no longer writes one). */\n"
     "add_action( 'init', function () {\n"
     "\tif ( '1' === get_option( 'nlrm_demo_nophone_v1' ) ) { return; }\n"
     "\tupdate_option( 'nlrm_demo_nophone_v1', '1', false );\n"
     "\t$demo_ids = get_posts( array( 'post_type' => 'nadlan_rentalprop', 'post_status' => 'any', 'posts_per_page' => 20,\n"
     "\t\t'fields' => 'ids', 'meta_query' => array( array( 'key' => 'is_demo', 'value' => '1' ) ) ) );\n"
     "\tforeach ( $demo_ids as $did ) {\n"
     "\t\t$du = json_decode( (string) get_post_meta( $did, 'rm_units', true ), true );\n"
     "\t\tif ( ! is_array( $du ) ) { continue; }\n"
     "\t\t$changed = false;\n"
     "\t\tforeach ( $du as $nk => $nu ) { if ( is_array( $nu ) && ! empty( $nu['tenant_phone'] ) ) { $du[ $nk ]['tenant_phone'] = ''; $changed = true; } }\n"
     "\t\tif ( $changed ) { update_post_meta( $did, 'rm_units', wp_slash( wp_json_encode( $du, JSON_UNESCAPED_UNICODE ) ) ); }\n"
     "\t}\n"
     "\tforeach ( array( 'he', 'en' ) as $l ) { delete_transient( 'nlrm_demo_payload_' . $l ); }\n"
     "}, 20 );\n"),
]
LIVE_MD5 = {R: hashlib.md5(open(os.path.join(kl_release.PLUG, *R.split("/")), "rb").read()).hexdigest()}
A = "/wp-content/plugins/nadlan-config/assets/rentals/"
T = "?t728a=1"
ROWS = ("    (%r, ['var X = en ? \" (example)\"', ') + X,'], ['9725', '@example'], []),\n"
        "    (%r, ['N.isDemo = function', 'N.canMsg = function'], [], []),\n"
        "    (%r, ['N.canMsg(contact)', 'N.isDemo() ?'], ['972500000999'], []),\n"
        "    (%r, ['N.isDemo() ?'], [], []),\n"
        "    (%r, ['N.canMsg(ten)', 'function probe()'], [], []),\n"
        "    (%r, ['N.mountToday'], ['9725'], []),\n"
        "    (%r, ['nlu-wademo', 'nlu-wacopy'], [], []),\n"
        "    ('/wp-json/nadlan/v1/rental-demo?t728a=1', ['\"props\"', '\"tenant_phone\":\"\"'], ['97250000', 'Fatal error'], []),\n"
        "    ('/wp-json/nadlan/v1/rental-demo?lang=en&t728a=1', ['\"props\"', '(example)'], ['97250000', 'Fatal error'], []),\n"
        "    ('/my-rentals/?t728a=1', ['הנכסים', 'לפי מדריך רשות המסים, התקרה לשנת 2025'], %r, []),\n"
        "    ('/my-rentals/?lang=en&t728a=1', ['check the current ceiling'], %r, []),\n"
        "    ('/wp-json/nadlan/v1/health?t728a=1', ['\"status\":\"ok\"'], %r, []),\n"
        "    ('/projects/rainbow-tel-aviv/?t728a=1', ['nlsh'], %r, []),\n"
        "    ('/projects/h-infinity-somail-tel-aviv/?t728a=1', [], %r, []),\n") % (
    A + "rm-demo.js" + T, A + "rm-core.js" + T, A + "rm-drawers.js" + T, A + "rm-views.js" + T, A + "rm-today.js" + T, A + "rm-boot.js" + T,
    A + "rental-manager.js" + T, E, E, E, E, E)
kl_release.build_release(PREV, 728, FILES, [], {R: H}, LIVE_MD5, ROWS,
                         "rentals: sample people carry no phone and no e-mail, wear an example mark, and nothing in a sample opens a chat or a call",
                         "HAD-795 package 6: sample people")
