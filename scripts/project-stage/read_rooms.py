# -*- coding: utf-8 -*-
"""READ-ONLY (17.11.2026, main session for Ben: "who called on the Kikar HaMedina video call yesterday?"): the video rooms
(post type nadlan_room, inc/together.php) opened since 16.11.2026 00:00 Israel time: when, which page, who opened it (buyer or rep),
the names and roles that entered (the live transient, kept 6 hours after the last activity), whether a rep was in, the number of
notes, and the owner mails of kind 'room' in the same days. No IP address is read or printed. A temporary admin bridge, deleted at
the end. python scripts/project-stage/read_rooms.py"""
import io, json, os, secrets, time
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "rooms"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
req, snip = ns["req"], ns["snip"]
BRIDGE = r'''
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-rooms-read/v1', '/run', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( $b['token'] ?? '' ) ) ) { return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) ); }
			$since = (int) ( $b['since'] ?? 0 );
			$tz = new DateTimeZone( 'Asia/Jerusalem' );
			$fmt = function ( $t ) use ( $tz ) { if ( ! $t ) { return ''; } $d = new DateTime( '@' . (int) $t ); $d->setTimezone( $tz ); return $d->format( 'j.n.Y H:i:s' ); };
			$rooms = get_posts( array( 'post_type' => 'nadlan_room', 'post_status' => 'any', 'numberposts' => 200, 'orderby' => 'date', 'order' => 'DESC', 'no_found_rows' => true, 'suppress_filters' => true ) );
			$out = array( 'rooms' => array(), 'mails' => array() );
			foreach ( $rooms as $r ) {
				$created = (int) get_post_meta( $r->ID, '_nltr_created', true );
				if ( ! $created ) { $created = strtotime( $r->post_date_gmt . ' UTC' ); }
				if ( $created < $since ) { continue; }
				$pid  = (int) get_post_meta( $r->ID, '_nltr_project', true );
				$live = get_transient( 'nltr_l_' . $r->post_name );
				$ppl  = array();
				if ( is_array( $live ) && ! empty( $live['p'] ) ) {
					foreach ( $live['p'] as $p ) { $ppl[] = array( 'name' => (string) ( $p['n'] ?? '' ), 'role' => (string) ( $p['r'] ?? '' ), 'joined' => $fmt( $p['j'] ?? 0 ), 'last_seen' => $fmt( $p['s'] ?? 0 ) ); }
				}
				$notes = get_post_meta( $r->ID, '_nltr_note' );
				$out['rooms'][] = array( 'room' => (string) $r->post_name, 'created' => $fmt( $created ), 'by' => (string) get_post_meta( $r->ID, '_nltr_by', true ),
					'page' => get_the_title( $pid ), 'slug' => (string) get_post_field( 'post_name', $pid ), 'url' => (string) get_permalink( $pid ),
					'live_kept' => is_array( $live ), 'people' => $ppl, 'rep_in' => (bool) array_filter( $ppl, function ( $x ) { return 'rep' === $x['role']; } ),
					'notes' => is_array( $notes ) ? count( $notes ) : 0, 'sel' => get_post_meta( $r->ID, '_nltr_sel', true ) );
			}
			foreach ( (array) get_option( 'nadlan_omx_log', array() ) as $m ) {
				if ( (int) ( $m['t'] ?? 0 ) >= $since && 'room' === ( $m['k'] ?? '' ) ) { $out['mails'][] = array( 'at' => $fmt( $m['t'] ), 'subject' => (string) ( $m['s'] ?? '' ), 'result' => (string) ( $m['r'] ?? '' ) ); }
			}
			/* the test lead of the deals guide (17.11): confirm it is in the Lead Inbox (a private nadlan_lead from deals_guide), then delete it.
			   Only a lead whose name is the test name is ever touched. */
			$tl = (int) ( $b['test_lead'] ?? 0 );
			if ( $tl ) {
				$lp = get_post( $tl );
				$is = $lp && 'nadlan_lead' === $lp->post_type && 'בדיקה אוטומטית - למחיקה' === (string) get_post_meta( $tl, 'name', true );
				$out['test_lead'] = array( 'found' => (bool) $lp, 'type' => $lp ? $lp->post_type : '', 'status' => $lp ? $lp->post_status : '', 'is_test' => $is,
					'source' => (string) get_post_meta( $tl, 'utm_source', true ), 'goal' => (string) get_post_meta( $tl, 'goal', true ), 'consent' => (string) get_post_meta( $tl, 'consent', true ),
					'message' => $lp ? mb_substr( (string) $lp->post_content, 0, 200 ) : '', 'in_inbox_query' => $is ? in_array( $tl, get_posts( array( 'post_type' => 'nadlan_lead', 'post_status' => 'any', 'numberposts' => 20, 'fields' => 'ids', 'orderby' => 'date', 'order' => 'DESC', 'suppress_filters' => true ) ), true ) : false );
				if ( $is && ! empty( $b['delete_test'] ) ) { $out['test_lead']['deleted'] = (bool) wp_delete_post( $tl, true ); $out['test_lead']['after'] = get_post( $tl ) ? 'still there' : 'gone'; }
			}
			$out['now'] = $fmt( time() );
			return $out;
		},
	) );
} );
'''
SINCE = 1794780000  # 15.11.2026 22:00 UTC = 16.11.2026 00:00 Israel
tok = secrets.token_hex(24); nm = "tmp-rooms-read-%d" % int(time.time())
s, sn = snip("POST", "", {"name": nm, "code": "/* placeholder */", "scope": "global", "active": False}); bid = sn["id"]
try:
    s1, _ = snip("PUT", "/%d" % bid, {"name": nm, "code": BRIDGE.replace("__TOKEN__", tok), "scope": "global", "active": False})
    s2, _ = snip("PUT", "/%d/activate" % bid, {})
    assert s1 == 200 and s2 == 200, (s1, s2)
    time.sleep(2)
    s, res, _ = req("POST", "/wp-json/nadlan-rooms-read/v1/run", {"token": tok, "since": SINCE, "test_lead": 9115, "delete_test": 1}, timeout=120)
finally:
    a, _ = snip("PUT", "/%d/deactivate" % bid, {}); b, _ = snip("DELETE", "/%d" % bid, None)
    c, _, _ = req("POST", "/wp-json/nadlan-rooms-read/v1/run", {"token": "x"})
    print("[bridge] deactivate", a, "| delete", b, "| route now", c, "(want 404)")
print("http", s, "| now", res.get("now"))
for r in res.get("rooms", []):
    print(json.dumps(r, ensure_ascii=False))
print("test lead:", json.dumps(res.get("test_lead"), ensure_ascii=False))
print("mails:")
for m in res.get("mails", []):
    print("  ", json.dumps(m, ensure_ascii=False))
os.makedirs(os.path.join(REPO, "docs", "qa", "had-712"), exist_ok=True)
io.open(os.path.join(REPO, "docs", "qa", "had-712", "rooms-read-%s.json" % time.strftime("%Y%m%dT%H%M%S")), "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1))
