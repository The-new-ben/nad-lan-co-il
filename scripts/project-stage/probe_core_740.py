# -*- coding: utf-8 -*-
"""READ-ONLY (15.11.2026): the live core map_meta_cap lines that map a post type's meta caps (so 'read' -> 'read_post'), the last
automatic core update record, and the core file dates. A temporary admin bridge, deleted at the end.
python scripts/project-stage/probe_core_740.py"""
import io, json, os, secrets, time
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "probecore"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
req, snip = ns["req"], ns["snip"]
BRIDGE = r'''
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-probecore/v1', '/run', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			global $wp_version;
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( $b['token'] ?? '' ) ) ) { return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) ); }
			$f = ABSPATH . WPINC . '/capabilities.php'; $L = file( $f ); $hits = array();
			foreach ( $L as $i => $l ) { if ( false !== strpos( $l, 'post_type_meta_caps' ) || false !== strpos( $l, "case 'read':" ) || false !== strpos( $l, 'must always check it against a specific post' ) ) { $hits[] = ( $i + 1 ) . ': ' . rtrim( $l ); } }
			$ctx = array(); foreach ( $hits as $h ) { $n = (int) $h; $ctx[] = implode( '', array_slice( $L, max( 0, $n - 4 ), 9 ) ); }
			return array( 'wp' => $wp_version, 'db' => get_option( 'db_version' ), 'auto_update' => get_site_option( 'auto_core_update_notified' ),
				'cap_file_mtime' => gmdate( 'Y-m-d H:i', filemtime( $f ) ), 'version_file_mtime' => gmdate( 'Y-m-d H:i', filemtime( ABSPATH . WPINC . '/version.php' ) ),
				'hits' => $hits, 'ctx' => array_slice( $ctx, 0, 4 ) );
		},
	) );
} );
'''
tok = secrets.token_hex(24); nm = "tmp-probecore-%d" % int(time.time())
s, sn = snip("POST", "", {"name": nm, "code": "/* placeholder */", "scope": "global", "active": False}); bid = sn["id"]
try:
    s1, _ = snip("PUT", "/%d" % bid, {"name": nm, "code": BRIDGE.replace("__TOKEN__", tok), "scope": "global", "active": False})
    s2, _ = snip("PUT", "/%d/activate" % bid, {})
    assert s1 == 200 and s2 == 200, (s1, s2)
    time.sleep(2)
    s, res, _ = req("POST", "/wp-json/nadlan-probecore/v1/run", {"token": tok}, timeout=120)
finally:
    a, _ = snip("PUT", "/%d/deactivate" % bid, {}); b, _ = snip("DELETE", "/%d" % bid, None)
    c, _, _ = req("POST", "/wp-json/nadlan-probecore/v1/run", {"token": "x"})
    print("[bridge] deactivate", a, "| delete", b, "| route now", c, "(want 404)")
io.open(os.path.join(REPO, "docs", "qa", "had-740", "admin-403-core-%s.json" % time.strftime("%Y%m%dT%H%M%S")), "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1))
print("http", s)
print(json.dumps({k: res[k] for k in ("wp", "db", "auto_update", "cap_file_mtime", "version_file_mtime", "hits")}, ensure_ascii=False, indent=1))
for c in res.get("ctx", []):
    print("-----"); print(c)
