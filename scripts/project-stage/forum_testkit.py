# -*- coding: utf-8 -*-
"""HAD-726 live test kit for the professionals' forum: creates (or removes) TWO clearly-named test members so a real
discussion can be opened and answered from two browsers without touching any real person, and prints their session
tokens for the test browser's cookie (nlf_s). Same temporary admin bridge as live_read.py, deleted at the end.
Test members: "בדיקת Claude א" (new member, first post goes to review) and "בדיקת Claude ב" (trusted: 2 approved posts).
Their addresses are on example.invalid (no mail is ever delivered). `clean` removes them and everything they wrote.

  python scripts/project-stage/forum_testkit.py make|clean|approve <topic id>"""
import json, os, secrets, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
MODE = (sys.argv[1] if len(sys.argv) > 1 else "").lower()
ARG = sys.argv[2] if len(sys.argv) > 2 else ""
if MODE not in ("make", "clean", "approve"):
    raise SystemExit("usage: forum_testkit.py make|clean|approve <topic id>")
_src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
_ns = {"__name__": "forum_testkit_helpers"}
exec(compile(_src[:_src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), _ns)
req, must, snip = _ns["req"], _ns["must"], _ns["snip"]
TOKEN = secrets.token_hex(24)
BRIDGE = r'''
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-forum-testkit/v1', '/run', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			global $wpdb;
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( isset( $b['token'] ) ? $b['token'] : '' ) ) ) { return new WP_Error( 'bad', 'token', array( 'status' => 400 ) ); }
			if ( ! function_exists( 'nlf_t' ) ) { return array( 'err' => 'forum module not loaded' ); }
			$mt = nlf_t( 'members' );
			$people = array( array( 'בדיקת Claude א', 'claude-test-a@example.invalid', 0 ), array( 'בדיקת Claude ב', 'claude-test-b@example.invalid', 2 ) );
			$mode = (string) $b['mode'];
			if ( 'make' === $mode ) {
				$out = array();
				foreach ( $people as $p ) {
					$ch  = nlf_contact_hash( $p[1], nlf_key() );
					$id  = (int) $wpdb->get_var( $wpdb->prepare( "SELECT id FROM $mt WHERE contact_hash = %s", $ch ) );
					$tok = bin2hex( random_bytes( 32 ) );
					$row = array( 'display_name' => $p[0], 'contact' => $p[1], 'contact_hash' => $ch, 'role_label' => 'buyer', 'approved_posts' => $p[2], 'status' => 'ok', 'session_hash' => hash( 'sha256', $tok ), 'last_seen' => nlf_now_sql() );
					if ( $id ) { $wpdb->update( $mt, $row, array( 'id' => $id ) ); } else { $row['created_at'] = nlf_now_sql(); $wpdb->insert( $mt, $row ); $id = (int) $wpdb->insert_id; }
					$out[] = array( 'id' => $id, 'name' => $p[0], 'cookie' => $tok );
				}
				return array( 'members' => $out );
			}
			if ( 'approve' === $mode ) { // every pending post of the two test members goes live (as the review screen would)
				$done = array();
				foreach ( $people as $p ) {
					$mid = (int) $wpdb->get_var( $wpdb->prepare( "SELECT id FROM $mt WHERE contact_hash = %s", nlf_contact_hash( $p[1], nlf_key() ) ) );
					if ( ! $mid ) { continue; }
					foreach ( array( 'topic' => 'topics', 'reply' => 'replies' ) as $type => $tb ) {
						foreach ( $wpdb->get_col( $wpdb->prepare( 'SELECT id FROM ' . nlf_t( $tb ) . " WHERE member_id = %d AND status = 'pending'", $mid ) ) as $id ) {
							nlf_moderate( $type, (int) $id, 'live' ); $done[] = $type . (int) $id;
						}
					}
				}
				return array( 'approved' => $done );
			}
			$ids = array();
			foreach ( $people as $p ) { $ids[] = (int) $wpdb->get_var( $wpdb->prepare( "SELECT id FROM $mt WHERE contact_hash = %s", nlf_contact_hash( $p[1], nlf_key() ) ) ); }
			$ids = array_filter( $ids );
			$gone = array();
			if ( $ids ) {
				$in = implode( ',', array_map( 'intval', $ids ) );
				$tids = $wpdb->get_col( 'SELECT id FROM ' . nlf_t( 'topics' ) . " WHERE member_id IN ($in)" );
				foreach ( array( 'replies' => 'member_id', 'thanks' => 'member_id', 'flags' => 'member_id', 'follows' => 'member_id' ) as $tb => $col ) {
					$gone[ $tb ] = (int) $wpdb->query( 'DELETE FROM ' . nlf_t( $tb ) . " WHERE $col IN ($in)" );
				}
				if ( $tids ) { $tin = implode( ',', array_map( 'intval', $tids ) ); $gone['replies_on_their_topics'] = (int) $wpdb->query( 'DELETE FROM ' . nlf_t( 'replies' ) . " WHERE topic_id IN ($tin)" ); }
				$gone['topics'] = (int) $wpdb->query( 'DELETE FROM ' . nlf_t( 'topics' ) . " WHERE member_id IN ($in)" );
				$gone['members'] = (int) $wpdb->query( "DELETE FROM $mt WHERE id IN ($in)" );
			}
			do_action( 'litespeed_purge_all' );
			return array( 'removed' => $gone );
		},
	) );
} );
'''.replace("__TOKEN__", TOKEN)
s, c = snip("POST", "", {"name": f"tmp-forum-testkit-{int(time.time())}", "code": "/* placeholder */", "scope": "global", "active": False})
must(s, c, "bridge create")
BR = c["id"]
try:
    s, u = snip("PUT", f"/{BR}", {"name": c["name"], "code": BRIDGE, "scope": "global", "active": False}); must(s, u, "bridge update")
    s, a = snip("PUT", f"/{BR}/activate", {}); must(s, a, "bridge activate")
    s, r, _ = req("POST", "/wp-json/nadlan-forum-testkit/v1/run", {"token": TOKEN, "mode": MODE, "arg": ARG}, timeout=90); must(s, r, "run")
    if MODE == "make":
        out = os.path.join(os.environ.get("TEMP", "."), "nlf_testkit_cookies.json")
        json.dump(r, open(out, "w", encoding="utf-8"))
        print("[testkit] members:", [(m["id"], m["name"]) for m in r.get("members", [])], "| cookies saved to", out)
    else:
        print("[testkit]", json.dumps(r, ensure_ascii=False))
finally:
    s1, _ = snip("PUT", f"/{BR}/deactivate", {}); s2, _ = snip("DELETE", f"/{BR}", None)
    print("[bridge] cleanup", s1, s2)
