# -*- coding: utf-8 -*-
"""HAD-726 read-only look at the live forum for the release session: the real (non-sample) members and what they wrote,
with every status, so a report like "the site does not let me enter my details" can be traced to its cause.
Same temporary admin bridge as forum_testkit.py, deleted at the end. Nothing is written. Mail addresses are masked.

  python scripts/project-stage/forum_peek.py [days]"""
import json, os, secrets, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
DAYS = int(sys.argv[1]) if len(sys.argv) > 1 else 14
_src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
_ns = {"__name__": "forum_peek_helpers"}
exec(compile(_src[:_src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), _ns)
req, must, snip = _ns["req"], _ns["must"], _ns["snip"]
TOKEN = secrets.token_hex(24)
BRIDGE = r'''
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-forum-peek/v1', '/run', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			global $wpdb;
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( isset( $b['token'] ) ? $b['token'] : '' ) ) ) { return new WP_Error( 'bad', 'token', array( 'status' => 400 ) ); }
			if ( ! function_exists( 'nlf_t' ) ) { return array( 'err' => 'forum module not loaded' ); }
			$since = gmdate( 'Y-m-d H:i:s', time() - (int) $b['days'] * DAY_IN_SECONDS );
			$mt = nlf_t( 'members' ); $tt = nlf_t( 'topics' ); $rt = nlf_t( 'replies' );
			$mask = function ( $c ) { $p = explode( '@', (string) $c ); return ( isset( $p[1] ) ? mb_substr( $p[0], 0, 2 ) . '***@' . $p[1] : '' ); };
			$mem = $wpdb->get_results( "SELECT id, display_name, contact, pro_id, role_label, trade, trade_other, approved_posts, status, show_phone, created_at, last_seen FROM $mt WHERE contact NOT LIKE 'seed-%@example.invalid' ORDER BY id", ARRAY_A );
			foreach ( $mem as &$m ) { $m['contact'] = $mask( $m['contact'] ); } unset( $m );
			$ids = array_map( 'intval', wp_list_pluck( $mem, 'id' ) );
			$in  = $ids ? implode( ',', $ids ) : '0';
			$out = array( 'members' => $mem,
				'topics'  => $wpdb->get_results( "SELECT id, cat, kind, title, body, member_id, pro_id, city, status, reply_count, created_at FROM $tt WHERE member_id IN ($in) OR created_at >= '$since' AND member_id NOT IN (SELECT id FROM $mt WHERE contact LIKE 'seed-%@example.invalid') ORDER BY id", ARRAY_A ),
				'replies' => $wpdb->get_results( "SELECT id, topic_id, member_id, body, status, created_at FROM $rt WHERE member_id IN ($in) ORDER BY id", ARRAY_A ),
				'requests' => $wpdb->get_results( 'SELECT id, kind, pro_id, member_id, body, status, created_at FROM ' . nlf_t( 'requests' ) . ' ORDER BY id DESC LIMIT 20', ARRAY_A ),
				'flags' => $wpdb->get_results( 'SELECT target_type, target_id, reason, created_at FROM ' . nlf_t( 'flags' ) . ' ORDER BY id DESC LIMIT 20', ARRAY_A ),
				'options' => array( 'public' => get_option( 'nadlan_forum_public' ), 'autoapprove' => get_option( 'nadlan_forum_autoapprove', '1' ), 'social_db' => get_option( 'nadlan_forum_social_db' ), 'call_db' => get_option( 'nadlan_forum_call_db' ) ),
			);
			if ( function_exists( 'nlfs_t' ) && get_option( 'nadlan_forum_social_db' ) ) {
				$out['kudos']  = $wpdb->get_results( 'SELECT id, from_member, to_member, rel, body, status, created_at FROM ' . nlfs_t( 'kudos' ) . ' ORDER BY id DESC LIMIT 20', ARRAY_A );
				$out['skills'] = $wpdb->get_results( 'SELECT id, member_id, label, status, created_at FROM ' . nlfs_t( 'skills' ) . ' ORDER BY id DESC LIMIT 20', ARRAY_A );
			}
			return $out;
		},
	) );
} );
'''.replace("__TOKEN__", TOKEN)
s, c = snip("POST", "", {"name": f"tmp-forum-peek-{int(time.time())}", "code": "/* placeholder */", "scope": "global", "active": False})
must(s, c, "bridge create")
BR = c["id"]
try:
    s, u = snip("PUT", f"/{BR}", {"name": c["name"], "code": BRIDGE, "scope": "global", "active": False}); must(s, u, "bridge update")
    s, a = snip("PUT", f"/{BR}/activate", {}); must(s, a, "bridge activate")
    s, r, _ = req("POST", "/wp-json/nadlan-forum-peek/v1/run", {"token": TOKEN, "days": DAYS}, timeout=90); must(s, r, "run")
    out = os.path.join(os.environ.get("TEMP", "."), "nlf_peek.json")
    json.dump(r, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("[peek] members %d, topics %d, replies %d, requests %d -> %s" % (len(r.get("members", [])), len(r.get("topics", [])), len(r.get("replies", [])), len(r.get("requests", [])), out))
finally:
    s1, _ = snip("PUT", f"/{BR}/deactivate", {}); s2, _ = snip("DELETE", f"/{BR}", None)
    print("[bridge] cleanup", s1, s2)
