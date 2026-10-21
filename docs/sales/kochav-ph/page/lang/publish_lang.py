# -*- coding: utf-8 -*-
"""Kochav HaTzafon listing in French and Russian (HAD-551, keywords.md: FR and RU demand; Ben 21.10 "don't drop tasks").
Creates (or, with --update, rewrites) the two pages under Meital's French (8375) and Russian (8372) sites, as the site's own
pattern for broker languages: the Hebrew slug, meta nl_lang / nl_broker_id / nl_card_key / nl_twin / nl_status, nl_dossier = 1
(the drop engine and broker-edit never rewrite a dossier page: broker-drop.php 1.72.478 + x-broker-edit 1.1.0), Yoast title and
description, and nl_hreflang on all four pages (7634 he, 7812 en, fr, ru). The pages are NOT added to 7634's nl_twins.
Content with scripts goes through a temporary admin-only bridge (kses off), like apply_page.py; read-back md5 after.
  python docs/sales/kochav-ph/page/lang/publish_lang.py [--dry] [--update]"""
import hashlib, io, json, os, secrets, sys, time
H = os.path.dirname(os.path.abspath(__file__))
REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "kochavlang"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req, snip = ns["req"], ns["snip"]
SEO = json.load(io.open(os.path.join(H, "seo.json"), encoding="utf-8"))
norm = lambda s: s.replace("\r\n", "\n")
md5 = lambda s: hashlib.md5(norm(s).encode("utf-8")).hexdigest()
jobs = []
for l in ("fr", "ru"):
    c = SEO[l]; html = io.open(os.path.join(H, "after-%s.html" % l), encoding="utf-8").read()
    for bad in ("tenant", "locataire", "арендатор", "attico", "cobertura", "Ben ", "commission"):
        assert bad not in html, (l, bad)
    jobs.append({"lang": l, "slug": c["slug"], "parent": c["parent_page_id"], "title": c["post_title"], "content": norm(html),
                 "meta": c["meta"], "seo_title": c["title"], "seo_desc": c["metadesc"]})
HREF = SEO["fr"]["nl_hreflang"]
print("[plan]", [(j["lang"], j["parent"], j["slug"], len(j["content"])) for j in jobs], "| hreflang", list(HREF))
if "--dry" in sys.argv:
    raise SystemExit(0)
tok = secrets.token_hex(24)
code = r"""
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-kochav-lang/v1', '/run', array( 'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__T__', (string) ( $b['token'] ?? '' ) ) ) { return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) ); }
			$out = array(); $ids = array( 'he' => 7634, 'en' => 7812 );
			kses_remove_filters();
			foreach ( (array) $b['jobs'] as $j ) {
				$found = get_posts( array( 'post_type' => 'page', 'name' => $j['slug'], 'post_parent' => (int) $j['parent'], 'post_status' => 'any', 'numberposts' => 1, 'fields' => 'ids' ) );
				if ( $found && empty( $b['update'] ) ) { $out[] = array( 'lang' => $j['lang'], 'err' => 'exists', 'id' => $found[0] ); continue; }
				$arr = array( 'post_type' => 'page', 'post_status' => 'publish', 'post_parent' => (int) $j['parent'], 'post_name' => $j['slug'], 'post_title' => $j['title'], 'post_content' => wp_slash( $j['content'] ), 'post_author' => 1 );
				if ( $found ) { $arr['ID'] = $found[0]; $id = wp_update_post( $arr, true ); } else { $id = wp_insert_post( $arr, true ); }
				if ( is_wp_error( $id ) ) { $out[] = array( 'lang' => $j['lang'], 'err' => $id->get_error_message() ); continue; }
				foreach ( (array) $j['meta'] as $k => $v ) { update_post_meta( $id, $k, wp_slash( (string) $v ) ); }
				update_post_meta( $id, '_yoast_wpseo_title', wp_slash( $j['seo_title'] ) );
				update_post_meta( $id, '_yoast_wpseo_metadesc', wp_slash( $j['seo_desc'] ) );
				$ids[ $j['lang'] ] = $id;
				$p = get_post( $id );
				$out[] = array( 'lang' => $j['lang'], 'id' => $id, 'url' => get_permalink( $id ), 'md5' => md5( str_replace( "\r\n", "\n", $p->post_content ) ) );
			}
			kses_init_filters();
			$map = wp_slash( wp_json_encode( $b['hreflang'], JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) );
			foreach ( $ids as $l => $id ) { update_post_meta( $id, 'nl_hreflang', $map ); clean_post_cache( $id ); do_action( 'litespeed_purge_post', $id ); }
			return array( 'ok' => true, 'out' => $out, 'ids' => $ids );
		} ) );
} );
""".replace("__T__", tok)
s, c = snip("POST", "", {"name": "tmp-kochav-lang-%d" % int(time.time()), "code": "/* placeholder */", "scope": "global", "active": False})
br = c["id"]
try:
    snip("PUT", "/%d" % br, {"name": c["name"], "code": code, "scope": "global", "active": False}); snip("PUT", "/%d/activate" % br, {}); time.sleep(1.5)
    s2, out, _ = req("POST", "/wp-json/nadlan-kochav-lang/v1/run", {"token": tok, "jobs": jobs, "hreflang": HREF, "update": "--update" in sys.argv})
    print("run", s2, json.dumps(out, ensure_ascii=False)[:900])
    if isinstance(out, dict) and out.get("ok"):
        for o in out["out"]:
            j = next(x for x in jobs if x["lang"] == o["lang"])
            if "md5" in o:
                print(o["lang"], o["id"], o["url"], "md5 ok:", o["md5"] == md5(j["content"]))
finally:
    snip("POST", "/%d/deactivate" % br, {}); s3, _ = snip("DELETE", "/%d" % br, None); time.sleep(1)
    s4, _, _ = req("POST", "/wp-json/nadlan-kochav-lang/v1/run", {"token": "x"})
    print("[bridge] deleted", s3, "route now", s4, "(want 404)")
