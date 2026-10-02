# -*- coding: utf-8 -*-
"""Read-only: fetch the LIVE text of one or more nadlan-config plugin files (the server copy, which can differ from the repo:
local batches run ahead of production) through a temporary admin bridge that only reads files under the plugin folder, and save
them under docs/qa/live-read/<stamp>/. Writes nothing on the site; the bridge is always deleted. The app password is decrypted
in-process (DPAPI) and never printed.

  python scripts/project-stage/live_read.py inc/project-stage.php [inc/other.php ...]"""
import base64, hashlib, io, json, os, secrets, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
RELS = [r for r in sys.argv[1:] if not r.startswith("--")]
if not RELS:
    raise SystemExit("usage: live_read.py <rel> [<rel> ...]")
_src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
_ns = {"__name__": "live_read_helpers"}
exec(compile(_src[:_src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), _ns)
req, must, snip = _ns["req"], _ns["must"], _ns["snip"]
TOKEN = secrets.token_hex(24)
BRIDGE = r'''
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-live-read/v1', '/get', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( isset( $b['token'] ) ? $b['token'] : '' ) ) ) { return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) ); }
			$root = realpath( WP_PLUGIN_DIR . '/nadlan-config' );
			$out = array();
			foreach ( (array) $b['rels'] as $rel ) {
				$path = realpath( $root . '/' . ltrim( (string) $rel, '/' ) );
				if ( ! $path || 0 !== strpos( $path, $root . DIRECTORY_SEPARATOR ) || ! is_file( $path ) ) { $out[ $rel ] = array( 'missing' => true ); continue; }
				$data = file_get_contents( $path );
				$out[ $rel ] = array( 'b64' => base64_encode( $data ), 'md5' => md5( $data ), 'bytes' => strlen( $data ) );
			}
			return $out;
		},
	) );
} );
'''.replace("__TOKEN__", TOKEN)
s, c = snip("POST", "", {"name": f"tmp-live-read-{int(time.time())}", "code": "/* placeholder */", "scope": "global", "active": False})
must(s, c, "bridge create")
BR = c["id"]
try:
    s, u = snip("PUT", f"/{BR}", {"name": c["name"], "code": BRIDGE, "scope": "global", "active": False}); must(s, u, "bridge update")
    s, a = snip("PUT", f"/{BR}/activate", {}); must(s, a, "bridge activate")
    s, r, _ = req("POST", "/wp-json/nadlan-live-read/v1/get", {"token": TOKEN, "rels": RELS}, timeout=120); must(s, r, "read")
finally:
    s1, _ = snip("PUT", f"/{BR}/deactivate", {}); s2, _ = snip("DELETE", f"/{BR}", None)
    print("[bridge] cleanup", s1, s2)
stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
OUT = os.path.join(REPO, "docs", "qa", "live-read", stamp)
for rel, v in r.items():
    if v.get("missing"):
        print("[missing]", rel); continue
    data = base64.b64decode(v["b64"])
    assert hashlib.md5(data).hexdigest() == v["md5"]
    p = os.path.join(OUT, *rel.split("/"))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "wb").write(data)
    repo_p = os.path.join(REPO, "plugins", "nadlan-config", *rel.split("/"))
    same = os.path.exists(repo_p) and open(repo_p, "rb").read().replace(b"\r\n", b"\n") == data.replace(b"\r\n", b"\n")
    print(f"[live] {rel} {v['bytes']} B md5 {v['md5'][:10]} -> {os.path.relpath(p, REPO)} | repo working copy {'SAME' if same else 'DIFFERENT'}")
