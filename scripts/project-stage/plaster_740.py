# -*- coding: utf-8 -*-
"""HAD-740 stage 2 (Ben 14.11.2026, released by the main session after its own checks): open the default card picture to everyone
and remove the featured picture from the pages that show one of the 49 "plaster" plates (media 7531-7580, 28.8.2026).
Steps (each logged; nothing deleted from the media library; page dates untouched):
  --plan   read docs/design/project-defaults-2026-11/fable/audit/featured.json, read every page's CURRENT featured id over REST
           (read-only) and write the restore file docs/qa/project-stage-2026-09-24/plaster-thumbs-removed-2026-11-14.json
           (page id, slug, url, the expected old media id, the current id, will_remove).
  --apply  a temporary admin-only bridge (token, manage_options) runs delete_post_meta( $id, '_thumbnail_id' ) ONLY where the
           current value still equals the expected plaster id (skips otherwise), bumps nadlan_dir_catalog_cache_ver, and sets
           nadlan_pd_public = '1'; then the bridge is deleted. No wp_update_post, no REST post update: post_modified stays.
  --rollback put every removed _thumbnail_id back from the restore file (same bridge pattern) and set nadlan_pd_public = ''.
python scripts/project-stage/plaster_740.py --plan | --apply | --rollback"""
import io, json, os, secrets, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
AUD = os.path.join(REPO, "docs", "design", "project-defaults-2026-11", "fable", "audit", "featured.json")
RESTORE = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24", "plaster-thumbs-removed-2026-11-14.json")
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "pl740"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
req, snip = ns["req"], ns["snip"]
ARGS = sys.argv[1:]

BRIDGE = r'''
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-pl740/v1', '/run', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( $b['token'] ?? '' ) ) ) { return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) ); }
			$out = array();
			foreach ( (array) ( $b['rows'] ?? array() ) as $r ) {
				$id = (int) $r['id']; $want = (int) $r['expect']; $put = (int) ( $r['put'] ?? 0 );
				$cur = (int) get_post_meta( $id, '_thumbnail_id', true );
				$mod = get_post_field( 'post_modified_gmt', $id );
				if ( $put ) {
					if ( 0 !== $cur ) { $out[] = array( 'id' => $id, 'skip' => 'has ' . $cur ); continue; }
					update_post_meta( $id, '_thumbnail_id', $put ); clean_post_cache( $id );
				} else {
					if ( $cur !== $want ) { $out[] = array( 'id' => $id, 'skip' => 'current ' . $cur . ' != ' . $want ); continue; }
					delete_post_meta( $id, '_thumbnail_id' ); clean_post_cache( $id );
				}
				$out[] = array( 'id' => $id, 'done' => true, 'now' => (int) get_post_meta( $id, '_thumbnail_id', true ), 'modified_same' => $mod === get_post_field( 'post_modified_gmt', $id ) );
			}
			if ( isset( $b['public'] ) ) { update_option( 'nadlan_pd_public', '1' === (string) $b['public'] ? '1' : '' ); }
			if ( ! empty( $b['bump'] ) ) { update_option( 'nadlan_dir_catalog_cache_ver', (int) get_option( 'nadlan_dir_catalog_cache_ver', 1 ) + 1, true ); }
			return array( 'rows' => $out, 'public' => get_option( 'nadlan_pd_public', '' ), 'cache_ver' => (int) get_option( 'nadlan_dir_catalog_cache_ver', 1 ) );
		},
	) );
} );
'''


def plan():
    d = json.load(io.open(AUD, encoding="utf-8"))
    rows = []
    for mid, pages in d["pages"].items():
        if not (7531 <= int(mid) <= 7580):
            continue
        for pid, slug in pages:
            s, cur, _ = req("GET", "/wp-json/wp/v2/nadlan_project/%d?context=edit&_fields=id,slug,link,featured_media,modified_gmt" % int(pid))
            now = int(cur.get("featured_media") or 0) if s == 200 else None
            rows.append({"id": int(pid), "slug": slug, "url": cur.get("link") if s == 200 else "", "expect": int(mid), "current": now,
                         "modified_gmt": cur.get("modified_gmt") if s == 200 else "", "will_remove": now == int(mid)})
    return rows


if "--plan" in ARGS:
    rows = plan()
    os.makedirs(os.path.dirname(RESTORE), exist_ok=True)
    io.open(RESTORE, "w", encoding="utf-8").write(json.dumps({"at": time.strftime("%Y-%m-%d %H:%M:%S"), "rows": rows}, ensure_ascii=False, indent=1))
    print("pages", len(rows), "| will remove", sum(r["will_remove"] for r in rows), "| skip", [(r["id"], r["slug"], r["current"], r["expect"]) for r in rows if not r["will_remove"]])
    print("restore file:", os.path.relpath(RESTORE, REPO))
    raise SystemExit(0)

if "--apply" in ARGS or "--rollback" in ARGS:
    rec = json.load(io.open(RESTORE, encoding="utf-8"))
    tok = secrets.token_hex(24)
    nm = "tmp-pl740-%d" % int(time.time())
    s, sn = snip("POST", "", {"name": nm, "code": "/* placeholder */", "scope": "global", "active": False})
    if s not in (200, 201):
        raise SystemExit("FATAL bridge: %s %s" % (s, str(sn)[:200]))
    bid = sn["id"]
    try:
        s, u = snip("PUT", "/%d" % bid, {"name": nm, "code": BRIDGE.replace("__TOKEN__", tok), "scope": "global", "active": False})
        s2, a = snip("PUT", "/%d/activate" % bid, {})
        if s != 200 or s2 != 200:
            raise SystemExit("FATAL bridge update/activate: %s %s" % (s, s2))
        print("[bridge] up, snippet", bid)
        time.sleep(2)
        if "--apply" in ARGS:
            body = {"token": tok, "rows": [{"id": r["id"], "expect": r["expect"]} for r in rec["rows"] if r["will_remove"]], "public": "1", "bump": 1}
        else:
            body = {"token": tok, "rows": [{"id": r["id"], "expect": 0, "put": r["expect"]} for r in rec["rows"] if r["will_remove"]], "public": "", "bump": 1}
        s, res, _ = req("POST", "/wp-json/nadlan-pl740/v1/run", body)
        print("[run] http", s)
        if s == 200:
            done = [x for x in res["rows"] if x.get("done")]; skip = [x for x in res["rows"] if not x.get("done")]
            print("done", len(done), "| skipped", skip, "| modified date unchanged on all:", all(x.get("modified_same") for x in done), "| now values", sorted(set(x.get("now") for x in done)))
            print("nadlan_pd_public =", repr(res["public"]), "| catalog cache ver", res["cache_ver"])
            rec.setdefault("runs", []).append({"at": time.strftime("%Y-%m-%d %H:%M:%S"), "mode": "apply" if "--apply" in ARGS else "rollback", "result": res})
            io.open(RESTORE, "w", encoding="utf-8").write(json.dumps(rec, ensure_ascii=False, indent=1))
        else:
            print(str(res)[:400])
    finally:
        s1, _ = snip("PUT", "/%d/deactivate" % bid, {})
        s2, _ = snip("DELETE", "/%d" % bid, None)
        s3, _, _ = req("POST", "/wp-json/nadlan-pl740/v1/run", {"token": "x"})
        print("[bridge] deactivate", s1, "| delete", s2, "| route now", s3, "(want 404)")
