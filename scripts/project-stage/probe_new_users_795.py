# -*- coding: utf-8 -*-
"""READ-ONLY (22.11.2026, HAD-795): the site's users registered in the last 48 hours (id, time, masked email, roles, whether they keep
version 1 rental properties) and the three rentals options, to find the test account Ben opened. A temporary admin bridge, deleted at the end.
python scripts/project-stage/probe_new_users_795.py"""
import json, os, secrets, time
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "probe795"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
req, snip = ns["req"], ns["snip"]
BRIDGE = r'''
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-probe795/v1', '/run', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( $b['token'] ?? '' ) ) ) { return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) ); }
			$since = gmdate( 'Y-m-d H:i:s', time() - 48 * 3600 );
			$q = new WP_User_Query( array( 'orderby' => 'registered', 'order' => 'DESC', 'number' => 30, 'date_query' => array( array( 'after' => $since, 'column' => 'user_registered' ) ) ) );
			$out = array( 'now_utc' => gmdate( 'Y-m-d H:i:s' ), 'users' => array() );
			foreach ( $q->get_results() as $u ) {
				$e = (string) $u->user_email; $at = strpos( $e, '@' );
				$mask = false === $at ? '?' : substr( $e, 0, min( 3, $at ) ) . '***' . substr( $e, $at );
				$props = 0;
				$props = count( get_posts( array( 'post_type' => 'nadlan_rentalprop', 'post_status' => 'any', 'posts_per_page' => 5, 'fields' => 'ids', 'meta_query' => array( array( 'key' => 'owner_user_id', 'value' => $u->ID ) ) ) ) );
				global $wpdb; $v2 = 0; $t = $wpdb->prefix . 'nlrm_properties';
				if ( $wpdb->get_var( $wpdb->prepare( 'SHOW TABLES LIKE %s', $t ) ) === $t ) { $v2 = (int) $wpdb->get_var( $wpdb->prepare( "SELECT COUNT(*) FROM $t WHERE owner_id = %d", $u->ID ) ); }
				$out['users'][] = array( 'id' => $u->ID, 'registered_utc' => $u->user_registered, 'email' => $mask, 'roles' => $u->roles, 'v1_props' => $props, 'v2_props' => $v2,
					'rentals_meta' => array_values( array_filter( array_keys( get_user_meta( $u->ID ) ), function ( $k ) { return false !== strpos( $k, 'rent' ) || false !== strpos( $k, 'nlrm' ) || false !== strpos( $k, 'signup' ) || false !== strpos( $k, 'nlau' ); } ) ) );
			}
			foreach ( array( 'nadlan_rentals_v2', 'nadlan_rentals_v2_pilot', 'nadlan_rentals_today2', 'nadlan_rentals_today2_pilot' ) as $o ) { $out['options'][ $o ] = get_option( $o, '(unset)' ); }
			return $out;
		},
	) );
} );
'''
tok = secrets.token_hex(24); nm = "tmp-probe795-%d" % int(time.time())
s, sn = snip("POST", "", {"name": nm, "code": "/* placeholder */", "scope": "global", "active": False}); bid = sn["id"]
try:
    s1, _ = snip("PUT", "/%d" % bid, {"name": nm, "code": BRIDGE.replace("__TOKEN__", tok), "scope": "global", "active": False})
    s2, _ = snip("PUT", "/%d/activate" % bid, {})
    assert s1 == 200 and s2 == 200, (s1, s2)
    time.sleep(2)
    s, res, _ = req("POST", "/wp-json/nadlan-probe795/v1/run", {"token": tok}, timeout=120)
finally:
    a, _ = snip("PUT", "/%d/deactivate" % bid, {}); b, _ = snip("DELETE", "/%d" % bid, None)
    c, _, _ = req("POST", "/wp-json/nadlan-probe795/v1/run", {"token": "x"})
    print("[bridge] deactivate", a, "| delete", b, "| route now", c, "(want 404)")
print("http", s)
print(json.dumps(res, ensure_ascii=False, indent=1)[:4000])
