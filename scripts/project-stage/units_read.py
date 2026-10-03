# -*- coding: utf-8 -*-
"""Read-only (HAD-403, Maya 09:00 UTC scope): dump every published project's `project_3d_units`, its average price per m2 and
every size-like meta key, through a temporary admin bridge that only reads post meta, into docs/qa/had-403/units-<stamp>.json.
Writes nothing on the site; the bridge is always deleted. The app password is decrypted in-process (DPAPI) and never printed.

  python scripts/project-stage/units_read.py"""
import base64, hashlib, io, json, os, secrets, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
_src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
_ns = {"__name__": "live_read_helpers"}
exec(compile(_src[:_src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), _ns)
req, must, snip = _ns["req"], _ns["must"], _ns["snip"]
TOKEN = secrets.token_hex(24)
BRIDGE = r"""
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-units-read/v1', '/get', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( isset( $b['token'] ) ? $b['token'] : '' ) ) ) { return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) ); }
			$ids = get_posts( array( 'post_type' => 'nadlan_project', 'post_status' => 'publish', 'posts_per_page' => -1, 'fields' => 'ids' ) );
			$out = array();
			foreach ( $ids as $id ) {
				$meta = get_post_meta( $id );
				$size = array();
				foreach ( $meta as $k => $v ) {
					if ( preg_match( '/sqm|size|area|unit|room|dira|apart/i', $k ) && 'project_3d_units' !== $k ) { $size[ $k ] = mb_substr( (string) $v[0], 0, 600 ); }
				}
				$out[] = array( 'id' => $id, 'slug' => get_post_field( 'post_name', $id ), 'title' => get_the_title( $id ),
					'ppsqm' => (int) get_post_meta( $id, 'project_3d_avg_price_per_sqm', true ),
					'units' => (string) get_post_meta( $id, 'project_3d_units', true ), 'size_meta' => $size );
			}
			return $out;
		},
	) );
} );
""".replace("__TOKEN__", TOKEN)
s, c = snip("POST", "", {"name": f"tmp-units-read-{int(time.time())}", "code": "/* placeholder */", "scope": "global", "active": False})
must(s, c, "bridge create")
BR = c["id"]
try:
    s, u = snip("PUT", f"/{BR}", {"name": c["name"], "code": BRIDGE, "scope": "global", "active": False}); must(s, u, "bridge update")
    s, a = snip("PUT", f"/{BR}/activate", {}); must(s, a, "bridge activate")
    s, r, _ = req("POST", "/wp-json/nadlan-units-read/v1/get", {"token": TOKEN}, timeout=180); must(s, r, "read")
finally:
    s1, _ = snip("PUT", f"/{BR}/deactivate", {}); s2, _ = snip("DELETE", f"/{BR}", None)
    print("[bridge] cleanup", s1, s2)
stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
OUT = os.path.join(REPO, "docs", "qa", "had-403")
os.makedirs(OUT, exist_ok=True)
p = os.path.join(OUT, f"units-{stamp}.json")
io.open(p, "w", encoding="utf-8").write(json.dumps(r, ensure_ascii=False, indent=1))
with_units = [x for x in r if x.get("units")]
print(f"[units] {len(r)} projects, {len(with_units)} with project_3d_units -> {os.path.relpath(p, REPO)}")
