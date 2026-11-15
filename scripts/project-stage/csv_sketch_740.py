# -*- coding: utf-8 -*-
"""HAD-740 fix 2 (Ben 15.11.2026): ten compound cards show a photo-like picture (assets/projects/batch-01/NN-...-photo.webp, the only
item of their photos_csv). Each has its own drawing in the same folder (NN-...-sketch.webp, the approved series). The sketch goes FIRST
in photos_csv, the photo stays as the second item (nothing removed): the card shows the sketch; the project page's gallery shows the
sketch, then the photo. update_post_meta through a temporary admin bridge (post_modified untouched), only where photos_csv is still
exactly the expected photo; the catalog cache version is bumped. Restore file docs/qa/project-stage-2026-09-24/photos-csv-restore-2026-11-15.json.
python scripts/project-stage/csv_sketch_740.py --apply | --rollback"""
import io, json, os, secrets, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
RESTORE = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24", "photos-csv-restore-2026-11-15.json")
B = "https://nad-lan.co.il/wp-content/plugins/nadlan-config/assets/projects/batch-01/"
ROWS = {5591: "01-hagana-salvador-haifa", 5590: "02-ehad-haam-nahariya", 5588: "03-maale-gaaton-nahariya", 5586: "04-bialik-shimoni-beer-sheva",
        5585: "05-ben-zvi-ramla", 5583: "06-haatzmaut-kiryat-bialik", 3556: "07-lev-hair-ramat-hasharon", 3551: "08-shvatei-israel-haifa",
        3545: "09-reines-jerusalem", 3543: "10-yerushalayim-ness-ziona"}
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "csv740"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
req, snip = ns["req"], ns["snip"]
BRIDGE = r'''
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-csv740/v1', '/run', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( $b['token'] ?? '' ) ) ) { return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) ); }
			$out = array();
			foreach ( (array) $b['rows'] as $r ) {
				$id = (int) $r['id']; $cur = (string) get_post_meta( $id, 'photos_csv', true ); $mod = get_post_field( 'post_modified_gmt', $id );
				if ( $cur !== (string) $r['expect'] ) { $out[] = array( 'id' => $id, 'skip' => 'current: ' . $cur ); continue; }
				update_post_meta( $id, 'photos_csv', (string) $r['new'] ); clean_post_cache( $id );
				$out[] = array( 'id' => $id, 'done' => true, 'now' => (string) get_post_meta( $id, 'photos_csv', true ), 'modified_same' => $mod === get_post_field( 'post_modified_gmt', $id ) );
			}
			if ( ! empty( $b['bump'] ) ) { update_option( 'nadlan_dir_catalog_cache_ver', (int) get_option( 'nadlan_dir_catalog_cache_ver', 1 ) + 1, true ); }
			return array( 'rows' => $out, 'cache_ver' => (int) get_option( 'nadlan_dir_catalog_cache_ver', 1 ) );
		},
	) );
} );
'''
photo = lambda k: B + ROWS[k] + "-photo.webp"
sketch = lambda k: B + ROWS[k] + "-sketch.webp"
if "--apply" in sys.argv:
    rows = [{"id": k, "expect": photo(k), "new": sketch(k) + "," + photo(k)} for k in ROWS]
    io.open(RESTORE, "w", encoding="utf-8").write(json.dumps({"at": time.strftime("%Y-%m-%d %H:%M:%S"), "rows": [{"id": k, "photos_csv_before": photo(k)} for k in ROWS]}, ensure_ascii=False, indent=1))
elif "--rollback" in sys.argv:
    rows = [{"id": k, "expect": sketch(k) + "," + photo(k), "new": photo(k)} for k in ROWS]
else:
    raise SystemExit(__doc__)
tok = secrets.token_hex(24); nm = "tmp-csv740-%d" % int(time.time())
s, sn = snip("POST", "", {"name": nm, "code": "/* placeholder */", "scope": "global", "active": False}); bid = sn["id"]
try:
    s1, _ = snip("PUT", "/%d" % bid, {"name": nm, "code": BRIDGE.replace("__TOKEN__", tok), "scope": "global", "active": False})
    s2, _ = snip("PUT", "/%d/activate" % bid, {})
    assert s1 == 200 and s2 == 200, (s1, s2)
    time.sleep(2)
    s, res, _ = req("POST", "/wp-json/nadlan-csv740/v1/run", {"token": tok, "rows": rows, "bump": 1})
    print("[run]", s, "| done", sum(1 for r in res["rows"] if r.get("done")), "| skipped", [r for r in res["rows"] if not r.get("done")],
          "| dates unchanged", all(r.get("modified_same") for r in res["rows"] if r.get("done")), "| cache ver", res["cache_ver"])
    print("example now:", res["rows"][0].get("now", "")[-120:])
finally:
    a, _ = snip("PUT", "/%d/deactivate" % bid, {}); b, _ = snip("DELETE", "/%d" % bid, None)
    c, _, _ = req("POST", "/wp-json/nadlan-csv740/v1/run", {"token": "x"})
    print("[bridge] deactivate", a, "| delete", b, "| route now", c, "(want 404)")
