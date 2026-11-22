# -*- coding: utf-8 -*-
"""HAD-801 read-only probe before the Sde Dov 2036 tour release: free disk on the host, upload limits, ZipArchive, whether a
physical /tour/ folder exists at the site root, and the WordPress rewrite block in .htaccess. Writes nothing on the site; the
temporary bridge is always deleted. The app password is decrypted in-process (DPAPI) and never printed.
  python scripts/had801/probe_host.py"""
import json, os, secrets, time
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
_src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); _ns = {"__name__": "h801probe"}
exec(compile(_src[:_src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), _ns)
req, must, snip = _ns["req"], _ns["must"], _ns["snip"]
TOKEN = secrets.token_hex(24)
BRIDGE = r'''
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-h801-probe/v1', '/get', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( isset( $b['token'] ) ? $b['token'] : '' ) ) ) { return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) ); }
			$ht = @file_get_contents( ABSPATH . '.htaccess' );
			$up = wp_upload_dir();
			return array(
				'php' => PHP_VERSION, 'free' => function_exists( 'disk_free_space' ) ? disk_free_space( ABSPATH ) : null, 'total' => function_exists( 'disk_total_space' ) ? disk_total_space( ABSPATH ) : null, 'disabled' => ini_get( 'disable_functions' ),
				'abspath_writable' => is_writable( ABSPATH ), 'tour_dir' => is_dir( ABSPATH . 'tour' ), 'tour_sde' => file_exists( ABSPATH . 'tour/sde-dov' ), 'tour_list' => is_dir( ABSPATH . 'tour' ) ? array_slice( scandir( ABSPATH . 'tour' ), 0, 40 ) : null,
				'zip' => class_exists( 'ZipArchive' ), 'upload_max' => ini_get( 'upload_max_filesize' ), 'post_max' => ini_get( 'post_max_size' ),
				'mem' => ini_get( 'memory_limit' ), 'max_exec' => ini_get( 'max_execution_time' ), 'uploads' => $up['basedir'],
				'htaccess' => is_string( $ht ) ? substr( $ht, 0, 3000 ) : null, 'server' => isset( $_SERVER['SERVER_SOFTWARE'] ) ? $_SERVER['SERVER_SOFTWARE'] : '',
			);
		},
	) );
} );
'''.replace("__TOKEN__", TOKEN)
s, c = snip("POST", "", {"name": "tmp-h801-probe-%d" % int(time.time()), "code": "/* placeholder */", "scope": "global", "active": False})
must(s, c, "bridge create"); BR = c["id"]
try:
    s, u = snip("PUT", "/%s" % BR, {"name": c["name"], "code": BRIDGE, "scope": "global", "active": False}); must(s, u, "bridge update")
    s, a = snip("PUT", "/%s/activate" % BR, {}); must(s, a, "bridge activate")
    s, r, _ = req("POST", "/wp-json/nadlan-h801-probe/v1/get", {"token": TOKEN}, timeout=60); must(s, r, "probe")
finally:
    s1, _ = snip("PUT", "/%s/deactivate" % BR, {}); s2, _ = snip("DELETE", "/%s" % BR, None)
    print("[bridge] cleanup", s1, s2)
ht = r.pop("htaccess") or ""
r["free_gb"] = round((r.get("free") or 0) / 1024 ** 3, 2); r["total_gb"] = round((r.get("total") or 0) / 1024 ** 3, 2)
print(json.dumps(r, ensure_ascii=False, indent=1))
print("---- .htaccess (WordPress block) ----")
i = ht.find("# BEGIN WordPress"); print(ht[i:i + 700] if i >= 0 else ht[:700])
