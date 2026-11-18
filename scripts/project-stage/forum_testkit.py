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
if MODE not in ("make", "clean", "approve", "repdemo"):
    raise SystemExit("usage: forum_testkit.py make|clean|approve <topic id>|repdemo   (add 'rep' after make/clean for members that COUNT in the reputation layer)")
# 18.11.2026: the reputation layer ignores fixture members on example.invalid, so its live check needs members on another
# (still undeliverable) domain. `make rep` / `repdemo` / `clean rep` use it; everything else stays on example.invalid.
DOMAIN = "nadlan-check.invalid" if (ARG == "rep" or MODE == "repdemo") else "example.invalid"
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
			$dom = preg_replace( '/[^a-z0-9.\-]/', '', (string) ( $b['domain'] ?? 'example.invalid' ) );
			if ( ! in_array( $dom, array( 'example.invalid', 'nadlan-check.invalid' ), true ) ) { $dom = 'example.invalid'; }
			$people = array( array( 'בדיקת Claude א', 'claude-test-a@' . $dom, 0 ), array( 'בדיקת Claude ב', 'claude-test-b@' . $dom, 2 ),
				array( 'בדיקת Claude ג', 'claude-test-c@' . $dom, 2 ) ); // 18.11.2026: a third one, for "a locked room refuses a newcomer"
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
			if ( 'repdemo' === $mode ) { // fixture rows for the live check of the reputation layer; `clean rep` removes all of it
				$ids = array();
				foreach ( $people as $p ) { $ids[] = (int) $wpdb->get_var( $wpdb->prepare( "SELECT id FROM $mt WHERE contact_hash = %s", nlf_contact_hash( $p[1], nlf_key() ) ) ); }
				if ( count( array_filter( $ids ) ) < 3 ) { return array( 'err' => 'run make rep first' ); }
				list( $a, $bb, $c ) = $ids;
				$wpdb->update( $mt, array( 'role_label' => 'pro', 'trade' => 'renovation' ), array( 'id' => $bb ) );
				$now = nlf_now_sql();
				$wpdb->insert( nlf_t( 'topics' ), array( 'cat' => 'build', 'kind' => 'question', 'title' => 'בדיקת מערכת: כמה זמן מייבשים טיח לפני צבע?', 'body' => 'דיון בדיקה אוטומטי של האתר. יוסר בעוד כמה דקות.', 'member_id' => $a, 'status' => 'live', 'reply_count' => 1, 'body_hash' => hash( 'sha256', 'repdemo-t' . $now ), 'created_at' => $now, 'last_at' => $now ) );
				$tid = (int) $wpdb->insert_id;
				$wpdb->insert( nlf_t( 'replies' ), array( 'topic_id' => $tid, 'member_id' => $bb, 'body' => 'תשובת בדיקה: בדרך כלל שלושה שבועות, תלוי בעובי ובאוורור.', 'status' => 'live', 'body_hash' => hash( 'sha256', 'repdemo-r' . $now ), 'created_at' => $now ) );
				$rid = (int) $wpdb->insert_id;
				$wpdb->update( nlf_t( 'topics' ), array( 'solved_reply_id' => $rid ), array( 'id' => $tid ) );
				$out = array( 'topic' => $tid, 'reply' => $rid, 'members' => array( 'a' => $a, 'b' => $bb, 'c' => $c ) );
				if ( function_exists( 'nlfs_t' ) ) {
					foreach ( array( array( $a, 'useful' ), array( $c, 'pro' ) ) as $x ) { $wpdb->insert( nlfs_t( 'react' ), array( 'member_id' => $x[0], 'target_type' => 'reply', 'target_id' => $rid, 'kind' => $x[1], 'created_at' => $now ) ); }
					$wpdb->insert( nlfs_t( 'kudos' ), array( 'from_member' => $c, 'to_member' => $bb, 'rel' => 'client', 'body' => 'פרגון בדיקה אוטומטי.', 'status' => 'live', 'created_at' => $now ) );
					$out['react_kinds'] = array_keys( nlfs_kinds() );
				}
				$v = defined( 'NLFR_VER' ) ? NLFR_VER : '1';
				foreach ( $ids as $id ) { delete_transient( 'nlfr_s' . $v . '_' . $id ); }
				delete_transient( 'nlfr_l' . $v . '_30_5' );
				do_action( 'litespeed_purge_all' );
				return $out;
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
				// 18.11.2026: a card a test member opened for himself goes to the trash with him (only a card he made: source forum_member + his id)
				foreach ( $wpdb->get_results( "SELECT id, pro_id FROM $mt WHERE id IN ($in) AND pro_id IS NOT NULL AND pro_id > 0", ARRAY_A ) as $row ) {
					$pid = (int) $row['pro_id'];
					if ( 'forum_member' === (string) get_post_meta( $pid, 'source', true ) && (int) get_post_meta( $pid, 'nl_forum_member', true ) === (int) $row['id'] ) { wp_trash_post( $pid ); $gone['cards_to_trash'][] = $pid; }
				}
				if ( function_exists( 'nlfs_t' ) ) {
					$gone['react'] = (int) $wpdb->query( 'DELETE FROM ' . nlfs_t( 'react' ) . " WHERE member_id IN ($in)" );
					$gone['kudos'] = (int) $wpdb->query( 'DELETE FROM ' . nlfs_t( 'kudos' ) . " WHERE from_member IN ($in) OR to_member IN ($in)" );
				}
				if ( function_exists( 'nlfc_table' ) ) { $gone['callpref'] = (int) $wpdb->query( 'DELETE FROM ' . nlfc_table() . " WHERE member_id IN ($in)" ); }
				$tids = $wpdb->get_col( 'SELECT id FROM ' . nlf_t( 'topics' ) . " WHERE member_id IN ($in)" );
				// 18.11.2026 (media module, inc/pro-forum-media.php): their pictures, plans, profile pictures and points, rows AND files, before the replies go
				if ( function_exists( 'nlfmd_purge_members' ) ) { $gone['media'] = (int) nlfmd_purge_members( $ids, (array) $tids ); }
				// 18.11.2026 (home module, inc/pro-forum-home.php): the apartment rows, votes and estimates of their discussions, and the votes and estimates they gave
				if ( function_exists( 'nlfh_purge_members' ) ) { $gone['homes'] = (int) nlfh_purge_members( $ids, (array) $tids ); }
				foreach ( array( 'replies' => 'member_id', 'thanks' => 'member_id', 'flags' => 'member_id', 'follows' => 'member_id' ) as $tb => $col ) {
					$gone[ $tb ] = (int) $wpdb->query( 'DELETE FROM ' . nlf_t( $tb ) . " WHERE $col IN ($in)" );
				}
				if ( $tids ) { $tin = implode( ',', array_map( 'intval', $tids ) ); $gone['replies_on_their_topics'] = (int) $wpdb->query( 'DELETE FROM ' . nlf_t( 'replies' ) . " WHERE topic_id IN ($tin)" ); }
				$gone['topics'] = (int) $wpdb->query( 'DELETE FROM ' . nlf_t( 'topics' ) . " WHERE member_id IN ($in)" );
				$gone['members'] = (int) $wpdb->query( "DELETE FROM $mt WHERE id IN ($in)" );
			}
			$v = defined( 'NLFR_VER' ) ? NLFR_VER : '1';
			foreach ( $ids as $id ) { delete_transient( 'nlfr_s' . $v . '_' . $id ); }
			delete_transient( 'nlfr_l' . $v . '_30_5' );
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
    s, r, _ = req("POST", "/wp-json/nadlan-forum-testkit/v1/run", {"token": TOKEN, "mode": MODE, "arg": ARG, "domain": DOMAIN}, timeout=90); must(s, r, "run")
    if MODE == "repdemo":
        json.dump(r, open(os.path.join(os.environ.get("TEMP", "."), "nlf_testkit_repdemo.json"), "w", encoding="utf-8"))
        print("[testkit] repdemo:", json.dumps(r, ensure_ascii=False))
    elif MODE == "make":
        out = os.path.join(os.environ.get("TEMP", "."), "nlf_testkit_cookies.json")
        json.dump(r, open(out, "w", encoding="utf-8"))
        print("[testkit] members:", [(m["id"], m["name"]) for m in r.get("members", [])], "| cookies saved to", out)
    else:
        print("[testkit]", json.dumps(r, ensure_ascii=False))
finally:
    s1, _ = snip("PUT", f"/{BR}/deactivate", {}); s2, _ = snip("DELETE", f"/{BR}", None)
    print("[bridge] cleanup", s1, s2)
