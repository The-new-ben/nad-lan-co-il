# -*- coding: utf-8 -*-
"""READ-ONLY diagnosis (15.11.2026, main session: the Dashboard, Profile and Updates screens return 403 for Ben).
A temporary admin bridge scans the LIVE PHP files of every active plugin, the must-use plugins, the active theme(s) and the active
Code Snippets for code that can hide those screens: user_has_cap / map_meta_cap filters, remove_menu_page / remove_submenu_page,
direct $menu / $submenu edits, add_menu_page at position 2, 'index.php' / 'profile.php' / 'update-core.php', remove_cap / add_cap.
It also reports, as the REST admin user: WP version, the administrator role's caps 'read', 'update_core', and which callbacks are
hooked on user_has_cap and map_meta_cap. Writes nothing. Output: docs/qa/had-740/admin-403-scan-<stamp>.json
python scripts/project-stage/scan_admin_caps.py"""
import io, json, os, re, secrets, time
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "scan403"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
req, snip = ns["req"], ns["snip"]
BRIDGE = r'''
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-scan403/v1', '/run', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			global $wpdb, $wp_filter, $wp_version;
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( $b['token'] ?? '' ) ) ) { return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) ); }
			$pat = '~(user_has_cap|map_meta_cap|remove_menu_page|remove_submenu_page|\$menu\s*\[|\$submenu\s*\[|unset\s*\(\s*\$menu|unset\s*\(\s*\$submenu|add_menu_page\s*\([^;]*,\s*[\'"]?2[\'"]?\s*\)|[\'"]index\.php[\'"]|[\'"]profile\.php[\'"]|[\'"]update-core\.php[\'"]|->remove_cap\s*\(|->add_cap\s*\(\s*[\'"]read)~';
			$roots = array();
			foreach ( (array) get_option( 'active_plugins', array() ) as $p ) { $roots[ 'plugin:' . $p ] = WP_PLUGIN_DIR . '/' . dirname( $p ); if ( '.' === dirname( $p ) ) { $roots[ 'plugin:' . $p ] = WP_PLUGIN_DIR . '/' . $p; } }
			if ( is_dir( WPMU_PLUGIN_DIR ) ) { $roots['mu-plugins'] = WPMU_PLUGIN_DIR; }
			$roots['theme:' . get_stylesheet()] = get_stylesheet_directory();
			if ( get_template() !== get_stylesheet() ) { $roots['theme:' . get_template()] = get_template_directory(); }
			$hits = array(); $files = 0;
			foreach ( $roots as $label => $root ) {
				$list = is_file( $root ) ? array( $root ) : array();
				if ( is_dir( $root ) ) {
					$it = new RecursiveIteratorIterator( new RecursiveDirectoryIterator( $root, FilesystemIterator::SKIP_DOTS ) );
					foreach ( $it as $f ) { $n = $f->getPathname(); if ( substr( $n, -4 ) === '.php' && false === strpos( $n, '/vendor/' ) && false === strpos( $n, '/node_modules/' ) && false === strpos( $n, '/languages/' ) && ! preg_match( '~\.bak|/tests?/~', $n ) ) { $list[] = $n; } }
				}
				foreach ( $list as $n ) {
					$files++; $lines = @file( $n ); if ( ! $lines ) { continue; }
					foreach ( $lines as $i => $l ) { if ( preg_match( $pat, $l ) ) { $hits[] = array( $label, str_replace( ABSPATH, '', $n ) . ':' . ( $i + 1 ), trim( substr( $l, 0, 220 ) ) ); } }
				}
			}
			$snip = array();
			$t = $wpdb->prefix . 'snippets';
			if ( $wpdb->get_var( $wpdb->prepare( 'SHOW TABLES LIKE %s', $t ) ) === $t ) {
				foreach ( (array) $wpdb->get_results( "SELECT id, name, scope, code FROM {$t} WHERE active = 1", ARRAY_A ) as $s ) {
					foreach ( preg_split( '~\R~', (string) $s['code'] ) as $i => $l ) { if ( preg_match( $pat, $l ) ) { $snip[] = array( (int) $s['id'], $s['name'], $s['scope'], $i + 1, trim( substr( $l, 0, 220 ) ) ); } }
				}
			}
			$hooks = array();
			foreach ( array( 'user_has_cap', 'map_meta_cap', 'admin_menu', 'admin_init' ) as $h ) {
				$hooks[ $h ] = array();
				if ( empty( $wp_filter[ $h ] ) ) { continue; }
				foreach ( $wp_filter[ $h ]->callbacks as $prio => $cbs ) {
					foreach ( $cbs as $cb ) {
						$f = $cb['function']; $name = is_string( $f ) ? $f : ( is_array( $f ) ? ( is_object( $f[0] ) ? get_class( $f[0] ) : $f[0] ) . '::' . $f[1] : 'closure' );
						$where = '';
						try { $r = is_array( $f ) ? new ReflectionMethod( $f[0], $f[1] ) : new ReflectionFunction( $f ); $where = str_replace( ABSPATH, '', (string) $r->getFileName() ) . ':' . $r->getStartLine(); } catch ( \Throwable $e ) {}
						$hooks[ $h ][] = $prio . ' ' . $name . ' @ ' . $where;
					}
				}
			}
			$role = get_role( 'administrator' );
			$u = wp_get_current_user();
			return array( 'wp' => $wp_version, 'files' => $files, 'hits' => $hits, 'snippets' => $snip, 'hooks' => $hooks,
				'role_admin' => array( 'read' => $role ? $role->has_cap( 'read' ) : null, 'update_core' => $role ? $role->has_cap( 'update_core' ) : null ),
				'me' => array( 'id' => $u->ID, 'roles' => $u->roles, 'can_read' => current_user_can( 'read' ), 'can_update_core' => current_user_can( 'update_core' ), 'allcaps_read' => ! empty( $u->allcaps['read'] ) ),
				'active_plugins' => get_option( 'active_plugins' ) );
		},
	) );
} );
'''
tok = secrets.token_hex(24); nm = "tmp-scan403-%d" % int(time.time())
s, sn = snip("POST", "", {"name": nm, "code": "/* placeholder */", "scope": "global", "active": False}); bid = sn["id"]
try:
    s1, _ = snip("PUT", "/%d" % bid, {"name": nm, "code": BRIDGE.replace("__TOKEN__", tok), "scope": "global", "active": False})
    s2, _ = snip("PUT", "/%d/activate" % bid, {})
    assert s1 == 200 and s2 == 200, (s1, s2)
    time.sleep(2)
    s, res, _ = req("POST", "/wp-json/nadlan-scan403/v1/run", {"token": tok}, timeout=300)
finally:
    a, _ = snip("PUT", "/%d/deactivate" % bid, {}); b, _ = snip("DELETE", "/%d" % bid, None)
    c, _, _ = req("POST", "/wp-json/nadlan-scan403/v1/run", {"token": "x"})
    print("[bridge] deactivate", a, "| delete", b, "| route now", c, "(want 404)")
out = os.path.join(REPO, "docs", "qa", "had-740", "admin-403-scan-%s.json" % time.strftime("%Y%m%dT%H%M%S"))
io.open(out, "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1))
print("http", s, "| saved", os.path.relpath(out, REPO))
if s == 200:
    print("WP", res["wp"], "| files scanned", res["files"], "| hits", len(res["hits"]), "| snippet hits", len(res["snippets"]))
    print("me:", res["me"], "| admin role:", res["role_admin"])
    for h in ("user_has_cap", "map_meta_cap"):
        print(h, ":", res["hooks"][h])
