# -*- coding: utf-8 -*-
"""READ-ONLY (15.11.2026): which filter turns current_user_can('read') to false for the administrator.
In one REST request, as the admin user: the baseline, then the same check with each user_has_cap / map_meta_cap callback removed
in memory one at a time (re-added at once; nothing is saved), the caps array WordPress asks for 'read' (map_meta_cap), and the text of
paid-member-subscriptions/includes/admin/functions-admin-role-permissions.php lines 200-270. A temporary admin bridge, deleted at the end.
python scripts/project-stage/probe_read_cap.py"""
import io, json, os, secrets, time
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "probe403"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
req, snip = ns["req"], ns["snip"]
BRIDGE = r'''
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-probe403/v1', '/run', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			global $wp_filter;
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( $b['token'] ?? '' ) ) ) { return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) ); }
			$u = wp_get_current_user();
			$out = array( 'baseline' => array( 'read' => current_user_can( 'read' ), 'edit_dashboard' => current_user_can( 'edit_dashboard' ), 'update_core' => current_user_can( 'update_core' ) ),
				'map_meta_cap_read' => map_meta_cap( 'read', $u->ID ), 'without' => array() );
			$probe = function ( $cap ) use ( $u ) { $uu = new WP_User( $u->ID ); return $uu->has_cap( $cap ); };
			foreach ( array( 'user_has_cap', 'map_meta_cap' ) as $h ) {
				if ( empty( $wp_filter[ $h ] ) ) { continue; }
				foreach ( $wp_filter[ $h ]->callbacks as $prio => $cbs ) {
					foreach ( $cbs as $id => $cb ) {
						$f = $cb['function']; $name = is_string( $f ) ? $f : ( is_array( $f ) ? ( is_object( $f[0] ) ? get_class( $f[0] ) : $f[0] ) . '::' . $f[1] : 'closure' );
						$where = ''; try { $r = is_array( $f ) ? new ReflectionMethod( $f[0], $f[1] ) : new ReflectionFunction( $f ); $where = basename( (string) $r->getFileName() ) . ':' . $r->getStartLine(); } catch ( \Throwable $e ) {}
						unset( $wp_filter[ $h ]->callbacks[ $prio ][ $id ] );
						$val = $probe( 'read' );
						$wp_filter[ $h ]->callbacks[ $prio ][ $id ] = $cb;
						$out['without'][] = array( $h, $prio, $name . ' @ ' . $where, 'read without it: ' . ( $val ? 'TRUE' : 'false' ) );
					}
				}
			}
			global $post_type_meta_caps;
			$out['meta_caps_read'] = array();
			foreach ( (array) $post_type_meta_caps as $k => $v ) { if ( 'read' === $k || 'read' === $v ) { $out['meta_caps_read'][] = array( $k, $v ); } }
			$out['types_mapping_read'] = array();
			foreach ( get_post_types( array(), 'objects' ) as $pt ) {
				$c = (array) $pt->cap; $hit = array();
				foreach ( array( 'read_post', 'edit_post', 'delete_post' ) as $m ) { if ( isset( $c[ $m ] ) && 'read' === $c[ $m ] ) { $hit[] = $m . '=read'; } }
				if ( $hit ) {
					$where = '';
					$out['types_mapping_read'][] = array( $pt->name, implode( ',', $hit ), 'map_meta_cap=' . ( $pt->map_meta_cap ? '1' : '0' ), 'capability_type=' . ( is_array( $pt->capability_type ) ? implode( '/', $pt->capability_type ) : $pt->capability_type ), 'label=' . $pt->label );
				}
			}
			$f = WP_PLUGIN_DIR . '/paid-member-subscriptions/includes/admin/functions-admin-role-permissions.php';
			$lines = is_file( $f ) ? file( $f ) : array();
			$out['pms_code'] = implode( '', array_slice( $lines, 199, 72 ) );
			$out['pms_version'] = defined( 'PMS_VERSION' ) ? PMS_VERSION : '';
			$out['pms_options'] = array();
			foreach ( array( 'pms_role_permissions', 'pms_role_permissions_settings', 'pms_misc_settings' ) as $o ) { $v = get_option( $o, null ); if ( null !== $v ) { $out['pms_options'][ $o ] = $v; } }
			return $out;
		},
	) );
} );
'''
tok = secrets.token_hex(24); nm = "tmp-probe403-%d" % int(time.time())
s, sn = snip("POST", "", {"name": nm, "code": "/* placeholder */", "scope": "global", "active": False}); bid = sn["id"]
try:
    s1, _ = snip("PUT", "/%d" % bid, {"name": nm, "code": BRIDGE.replace("__TOKEN__", tok), "scope": "global", "active": False})
    s2, _ = snip("PUT", "/%d/activate" % bid, {})
    assert s1 == 200 and s2 == 200, (s1, s2)
    time.sleep(2)
    s, res, _ = req("POST", "/wp-json/nadlan-probe403/v1/run", {"token": tok}, timeout=120)
finally:
    a, _ = snip("PUT", "/%d/deactivate" % bid, {}); b, _ = snip("DELETE", "/%d" % bid, None)
    c, _, _ = req("POST", "/wp-json/nadlan-probe403/v1/run", {"token": "x"})
    print("[bridge] deactivate", a, "| delete", b, "| route now", c, "(want 404)")
out = os.path.join(REPO, "docs", "qa", "had-740", "admin-403-probe-%s.json" % time.strftime("%Y%m%dT%H%M%S"))
io.open(out, "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1))
print("http", s, "| saved", os.path.relpath(out, REPO))
if s == 200:
    print("baseline", res["baseline"], "| map_meta_cap('read') ->", res["map_meta_cap_read"], "| PMS", res.get("pms_version"))
    print("meta caps involving read:", res["meta_caps_read"])
    print("post types mapping a meta cap to read:", res["types_mapping_read"])
