# -*- coding: utf-8 -*-
"""READ-ONLY (15.11.2026, HAD-743 deals map + street plate): how many published projects have each field the map and the street
plate need - lat/lng, address (street), neighbourhood, city, developer, stage, featured image - and the top developers by count.
A temporary admin bridge, deleted at the end. Output: docs/research/2026-11-15-deals-board/project-data-counts.json
python scripts/project-stage/count_project_data.py"""
import io, json, os, secrets, time
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "countpd"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
req, snip = ns["req"], ns["snip"]
BRIDGE = r'''
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-countpd/v1', '/run', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			global $wpdb;
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( $b['token'] ?? '' ) ) ) { return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) ); }
			$ids = $wpdb->get_col( "SELECT ID FROM {$wpdb->posts} WHERE post_type = 'nadlan_project' AND post_status = 'publish'" );
			$keys = array( 'lat', 'lng', 'address', 'neighborhood', 'city', 'developer_name', 'project_status', 'num_units', 'photos_csv', '_thumbnail_id' );
			$have = array_fill_keys( $keys, 0 ); $both = 0; $street = 0; $devs = array(); $cities = array(); $samples = array();
			foreach ( $ids as $id ) {
				$m = array();
				foreach ( $keys as $k ) { $v = trim( (string) get_post_meta( $id, $k, true ) ); $m[ $k ] = $v; if ( '' !== $v && '0' !== $v ) { $have[ $k ]++; } }
				if ( '' !== $m['lat'] && '' !== $m['lng'] && 0.0 !== (float) $m['lat'] ) { $both++; }
				if ( '' !== $m['address'] && preg_match( '~[\x{05D0}-\x{05EA}a-zA-Z]{2,}.*\d|\d.*[\x{05D0}-\x{05EA}]{2,}|רחוב|שדרות|דרך~u', $m['address'] ) ) { $street++; }
				if ( '' !== $m['developer_name'] ) { $devs[ $m['developer_name'] ] = ( $devs[ $m['developer_name'] ] ?? 0 ) + 1; }
				if ( '' !== $m['city'] ) { $cities[ $m['city'] ] = ( $cities[ $m['city'] ] ?? 0 ) + 1; }
				if ( count( $samples ) < 12 && '' === $m['_thumbnail_id'] && '' === $m['photos_csv'] ) { $samples[] = array( $id, get_the_title( $id ), $m['address'], $m['neighborhood'], $m['city'], $m['developer_name'], $m['lat'], $m['lng'] ); }
			}
			arsort( $devs ); arsort( $cities );
			return array( 'projects' => count( $ids ), 'have' => $have, 'latlng_both' => $both, 'address_looks_like_street' => $street,
				'developers' => count( $devs ), 'top_developers' => array_slice( $devs, 0, 25, true ), 'cities' => count( $cities ), 'top_cities' => array_slice( $cities, 0, 15, true ),
				'no_picture_samples' => $samples );
		},
	) );
} );
'''
tok = secrets.token_hex(24); nm = "tmp-countpd-%d" % int(time.time())
s, sn = snip("POST", "", {"name": nm, "code": "/* placeholder */", "scope": "global", "active": False}); bid = sn["id"]
try:
    s1, _ = snip("PUT", "/%d" % bid, {"name": nm, "code": BRIDGE.replace("__TOKEN__", tok), "scope": "global", "active": False})
    s2, _ = snip("PUT", "/%d/activate" % bid, {})
    assert s1 == 200 and s2 == 200, (s1, s2)
    time.sleep(2)
    s, res, _ = req("POST", "/wp-json/nadlan-countpd/v1/run", {"token": tok}, timeout=300)
finally:
    a, _ = snip("PUT", "/%d/deactivate" % bid, {}); b, _ = snip("DELETE", "/%d" % bid, None)
    c, _, _ = req("POST", "/wp-json/nadlan-countpd/v1/run", {"token": "x"})
    print("[bridge] deactivate", a, "| delete", b, "| route now", c, "(want 404)")
out = os.path.join(REPO, "docs", "research", "2026-11-15-deals-board", "project-data-counts.json")
io.open(out, "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1))
print("http", s)
print(json.dumps({k: res[k] for k in ("projects", "have", "latlng_both", "address_looks_like_street", "developers", "cities")}, ensure_ascii=False))
print("top developers:", json.dumps(res["top_developers"], ensure_ascii=False))
print("top cities:", json.dumps(res["top_cities"], ensure_ascii=False))
for r in res["no_picture_samples"]:
    print("  ", r)
