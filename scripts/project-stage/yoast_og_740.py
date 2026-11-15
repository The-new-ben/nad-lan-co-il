# -*- coding: utf-8 -*-
"""HAD-740 fix 1 (Ben 15.11.2026 "כן, תתקן אותם"): the share image of the 48 former plaster pages.
  --read   read-only: for each of the 49 pages in plaster-thumbs-removed-2026-11-14.json, the Yoast share-image fields of the page
           (_yoast_wpseo_opengraph-image / -id, _yoast_wpseo_twitter-image / -id) and its stored Yoast record (wp_yoast_indexable:
           open_graph_image, _id, _source, twitter_image, _source). Writes docs/qa/project-stage-2026-09-24/yoast-og-before-2026-11-15.json.
  --apply  for the pages whose share image still names a plaster file: set the page's own Yoast share image (the fields Ben sees in
           the edit screen) to media 8914 and rebuild that page's Yoast record (Indexable_Builder), post_modified untouched.
           Restore file: docs/qa/project-stage-2026-09-24/yoast-og-restore-2026-11-15.json (the old field values).
  --rollback put the old field values back and rebuild the records.
A temporary admin-only bridge (token, manage_options), deleted at the end."""
import io, json, os, secrets, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
SRC = os.path.join(QA, "plaster-thumbs-removed-2026-11-14.json")
BEFORE = os.path.join(QA, "yoast-og-before-2026-11-15.json")
RESTORE = os.path.join(QA, "yoast-og-restore-2026-11-15.json")
MEDIA = 8914
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "yog740"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
req, snip = ns["req"], ns["snip"]
KEYS = ["_yoast_wpseo_opengraph-image", "_yoast_wpseo_opengraph-image-id", "_yoast_wpseo_twitter-image", "_yoast_wpseo_twitter-image-id"]
BRIDGE = r'''
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-yog740/v1', '/run', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			global $wpdb;
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( $b['token'] ?? '' ) ) ) { return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) ); }
			$keys = (array) $b['keys']; $t = $wpdb->prefix . 'yoast_indexable';
			$read = function ( $id ) use ( $keys, $wpdb, $t ) {
				$m = array(); foreach ( $keys as $k ) { $m[ $k ] = get_post_meta( $id, $k, true ); }
				$ix = $wpdb->get_row( $wpdb->prepare( "SELECT id, open_graph_image, open_graph_image_id, open_graph_image_source, twitter_image, twitter_image_id, twitter_image_source, object_last_modified FROM {$t} WHERE object_id = %d AND object_type = 'post' LIMIT 1", $id ), ARRAY_A );
				return array( 'meta' => $m, 'ix' => $ix, 'modified' => get_post_field( 'post_modified_gmt', $id ) );
			};
			$out = array();
			foreach ( (array) $b['rows'] as $r ) {
				$id = (int) $r['id']; $before = $read( $id ); $row = array( 'id' => $id, 'before' => $before );
				if ( ! empty( $r['set'] ) ) {
					foreach ( (array) $r['set'] as $k => $v ) {
						if ( ! in_array( $k, $keys, true ) ) { continue; }
						if ( '' === (string) $v ) { delete_post_meta( $id, $k ); } else { update_post_meta( $id, $k, $v ); }
					}
					clean_post_cache( $id );
					$built = 'no-builder';
					if ( function_exists( 'YoastSEO' ) && class_exists( '\Yoast\WP\SEO\Builders\Indexable_Builder' ) ) {
						try {
							$repo = YoastSEO()->classes->get( 'Yoast\WP\SEO\Repositories\Indexable_Repository' );
							$ixo  = $repo->find_by_id_and_type( $id, 'post', false );
							$bld  = YoastSEO()->classes->get( 'Yoast\WP\SEO\Builders\Indexable_Builder' );
							$bld->build_for_id_and_type( $id, 'post', $ixo ? $ixo : false );
							$built = 'rebuilt';
						} catch ( \Throwable $e ) { $built = 'error: ' . $e->getMessage(); }
					}
					$row['built'] = $built; $row['after'] = $read( $id );
					$row['modified_same'] = $before['modified'] === $row['after']['modified'];
				}
				$out[] = $row;
			}
			$src = wp_get_attachment_image_src( (int) $b['media'], 'full' );
			return array( 'rows' => $out, 'media_url' => $src ? $src[0] : '' );
		},
	) );
} );
'''


def run(rows):
    tok = secrets.token_hex(24); nm = "tmp-yog740-%d" % int(time.time())
    s, sn = snip("POST", "", {"name": nm, "code": "/* placeholder */", "scope": "global", "active": False})
    if s not in (200, 201):
        raise SystemExit("FATAL bridge %s" % s)
    bid = sn["id"]
    try:
        s1, _ = snip("PUT", "/%d" % bid, {"name": nm, "code": BRIDGE.replace("__TOKEN__", tok), "scope": "global", "active": False})
        s2, _ = snip("PUT", "/%d/activate" % bid, {})
        if s1 != 200 or s2 != 200:
            raise SystemExit("FATAL bridge update/activate %s %s" % (s1, s2))
        time.sleep(2)
        s, res, _ = req("POST", "/wp-json/nadlan-yog740/v1/run", {"token": tok, "keys": KEYS, "rows": rows, "media": MEDIA})
        if s != 200:
            raise SystemExit("FATAL run %s %s" % (s, str(res)[:300]))
        return res
    finally:
        a, _ = snip("PUT", "/%d/deactivate" % bid, {}); b, _ = snip("DELETE", "/%d" % bid, None)
        c, _, _ = req("POST", "/wp-json/nadlan-yog740/v1/run", {"token": "x"})
        print("[bridge] deactivate", a, "| delete", b, "| route now", c, "(want 404)")


rec = json.load(io.open(SRC, encoding="utf-8"))
plaster = json.load(io.open(os.path.join(REPO, "docs", "design", "project-defaults-2026-11", "fable", "audit", "featured.json"), encoding="utf-8"))
names = sorted({plaster["media"][k]["slug"] for k in plaster["media"] if 7531 <= int(k) <= 7580})
has_pl = lambda v: any(n in str(v or "") for n in names)
if "--read" in sys.argv:
    res = run([{"id": r["id"]} for r in rec["rows"]])
    io.open(BEFORE, "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1))
    rows = res["rows"]
    print("pages", len(rows), "| media 8914 url", res["media_url"])
    print("own Yoast share field set:", sum(1 for r in rows if r["before"]["meta"]["_yoast_wpseo_opengraph-image"]), "| own field names plaster:", sum(1 for r in rows if has_pl(r["before"]["meta"]["_yoast_wpseo_opengraph-image"])))
    print("stored record names plaster in og:", sum(1 for r in rows if r["before"]["ix"] and has_pl(r["before"]["ix"]["open_graph_image"])),
          "| sources:", sorted({(r["before"]["ix"] or {}).get("open_graph_image_source") for r in rows}),
          "| twitter plaster:", sum(1 for r in rows if r["before"]["ix"] and has_pl(r["before"]["ix"]["twitter_image"])), "| no record:", sum(1 for r in rows if not r["before"]["ix"]))
    print("example:", json.dumps(rows[0]["before"], ensure_ascii=False)[:500])
elif "--apply" in sys.argv or "--rollback" in sys.argv:
    before = json.load(io.open(BEFORE, encoding="utf-8"))
    url = before["media_url"]; assert url.endswith(".webp"), url
    if "--apply" in sys.argv:
        targets = [r for r in before["rows"] if r["before"]["ix"] and has_pl(r["before"]["ix"]["open_graph_image"])]
        io.open(RESTORE, "w", encoding="utf-8").write(json.dumps({"at": time.strftime("%Y-%m-%d %H:%M:%S"), "rows": [{"id": r["id"], "meta": r["before"]["meta"], "ix": r["before"]["ix"]} for r in targets]}, ensure_ascii=False, indent=1))
        rows = [{"id": r["id"], "set": {"_yoast_wpseo_opengraph-image": url, "_yoast_wpseo_opengraph-image-id": str(MEDIA)}} for r in targets]
    else:
        rs = json.load(io.open(RESTORE, encoding="utf-8"))
        rows = [{"id": r["id"], "set": {k: (r["meta"].get(k) or "") for k in KEYS[:2]}} for r in rs["rows"]]
    res = run(rows)
    out = res["rows"]
    ok = [r for r in out if r.get("built") == "rebuilt" and r["after"]["ix"] and not has_pl(r["after"]["ix"]["open_graph_image"]) and r["modified_same"]]
    print("pages changed", len(out), "| rebuilt + no plaster + date unchanged:", len(ok), "| problems:", [(r["id"], r.get("built"), (r["after"]["ix"] or {}).get("open_graph_image", "")[-50:], r["modified_same"]) for r in out if r not in ok][:6])
    print("example after:", json.dumps(out[0]["after"]["ix"], ensure_ascii=False)[:300] if out else "")
    io.open(RESTORE.replace("restore", "result"), "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1))
