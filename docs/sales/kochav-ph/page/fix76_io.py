# -*- coding: utf-8 -*-
"""Ben 27.10.2026: the terraces are 76 sqm, not 80, and the building has a gym and a residents' room. Reads and writes the four
Kochav listing pages (7634 he, 7812 en, fr, ru) with title and Yoast meta, through a temporary admin-only route (code-snippets),
the same way live_io.py does. Reading changes nothing.
  python fix76_io.py --fetch        -> live76/<lang>.json (id, title, content, meta) for he, en, fr, ru
  python fix76_io.py --apply        -> writes live76/<lang>.new.json where the live content still matches live76/<lang>.json (md5
                                       guard), keeps nl_dossier, purges the cache, reads back"""
import hashlib, io, json, os, secrets, sys, time
H = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(H, "live76"); os.makedirs(D, exist_ok=True)
REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "k76"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req, snip = ns["req"], ns["snip"]
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
norm = lambda s: s.replace("\r\n", "\n")
md5 = lambda s: hashlib.md5(norm(s).encode("utf-8")).hexdigest()
URLS = {"he": "https://nad-lan.co.il/properties/kochav-hatzafon-new-mini-penthouse-for-sale/",
        "en": "https://nad-lan.co.il/en/brokers/meital-katzir/kochav-hatzafon-new-mini-penthouse-for-sale/",
        "fr": "https://nad-lan.co.il/fr/brokers/meital-katzir/kochav-hatzafon-new-mini-penthouse-for-sale/",
        "ru": "https://nad-lan.co.il/ru/brokers/meital-katzir/kochav-hatzafon-new-mini-penthouse-for-sale/"}
META = ["_yoast_wpseo_title", "_yoast_wpseo_metadesc", "_yoast_wpseo_opengraph-title", "_yoast_wpseo_opengraph-description",
        "_yoast_wpseo_twitter-title", "_yoast_wpseo_twitter-description"]
MODE = "fetch" if "--fetch" in sys.argv else "apply"
body = {"meta": META}
if MODE == "fetch":
    body["urls"] = URLS
else:
    jobs = []
    for lang in URLS:
        f = os.path.join(D, "%s.new.json" % lang)
        if not os.path.exists(f): continue
        old = json.load(io.open(os.path.join(D, "%s.json" % lang), encoding="utf-8"))
        new = json.load(io.open(f, encoding="utf-8"))
        jobs.append({"lang": lang, "id": old["id"], "want": md5(old["content"]), "content": norm(new["content"]),
                     "title": new["title"], "meta": {k: v for k, v in new["meta"].items() if v != old["meta"].get(k)}})
    body["jobs"] = jobs
tok = secrets.token_hex(24); body["token"] = tok
code = r"""
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-kochav76/v1', '/run', array( 'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__T__', (string) ( $b['token'] ?? '' ) ) ) { return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) ); }
			$read = function ( $id ) use ( $b ) {
				$p = get_post( (int) $id ); $m = array();
				foreach ( (array) $b['meta'] as $k ) { $m[ $k ] = (string) get_post_meta( (int) $id, $k, true ); }
				return array( 'id' => (int) $id, 'title' => $p ? $p->post_title : null, 'content' => $p ? $p->post_content : null, 'meta' => $m, 'type' => $p ? $p->post_type : null );
			};
			$out = array();
			if ( ! empty( $b['urls'] ) ) {
				foreach ( (array) $b['urls'] as $lang => $u ) { $id = url_to_postid( $u ); $out[ $lang ] = $id ? $read( $id ) : array( 'id' => 0, 'url' => $u ); }
				return array( 'ok' => true, 'out' => $out );
			}
			foreach ( (array) $b['jobs'] as $j ) {
				$p = get_post( (int) $j['id'] );
				$cur = $p ? md5( str_replace( "\r\n", "\n", $p->post_content ) ) : '';
				if ( $cur !== $j['want'] ) { $out[] = array( 'lang' => $j['lang'], 'err' => 'drift', 'cur' => $cur ); }
			}
			if ( $out ) { return array( 'ok' => false, 'out' => $out ); }
			kses_remove_filters();
			foreach ( (array) $b['jobs'] as $j ) {
				$id = (int) $j['id'];
				$r = wp_update_post( array( 'ID' => $id, 'post_content' => wp_slash( $j['content'] ), 'post_title' => wp_slash( $j['title'] ) ), true );
				foreach ( (array) $j['meta'] as $k => $v ) { update_post_meta( $id, $k, wp_slash( $v ) ); }
				if ( 7634 === $id ) { update_post_meta( 7634, 'nl_dossier', '1' ); }
				clean_post_cache( $id );
				do_action( 'litespeed_purge_post', $id );
				$u = get_permalink( $id ); if ( $u ) { do_action( 'litespeed_purge_url', $u ); }
				$x = $read( $id );
				$out[] = array( 'lang' => $j['lang'], 'id' => $id, 'ok' => ! is_wp_error( $r ), 'md5' => md5( str_replace( "\r\n", "\n", $x['content'] ) ), 'title' => $x['title'], 'meta' => $x['meta'] );
			}
			kses_init_filters();
			return array( 'ok' => true, 'out' => $out );
		} ) );
} );
""".replace("__T__", tok)
s, c = snip("POST", "", {"name": "tmp-kochav76-%d" % int(time.time()), "code": "/* placeholder */", "scope": "global", "active": False})
br = c["id"]
try:
    snip("PUT", "/%d" % br, {"name": c["name"], "code": code, "scope": "global", "active": False}); snip("PUT", "/%d/activate" % br, {}); time.sleep(1.5)
    s2, out, _ = req("POST", "/wp-json/nadlan-kochav76/v1/run", body)
    if MODE == "fetch":
        for lang, o in out["out"].items():
            io.open(os.path.join(D, "%s.json" % lang), "w", encoding="utf-8").write(json.dumps(o, ensure_ascii=False, indent=1))
            print(lang, o["id"], o.get("type"), (o.get("title") or "")[:70], len(o.get("content") or ""), "chars, md5", md5(o.get("content") or "")[:10])
    else:
        print("run", s2, "ok" if isinstance(out, dict) and out.get("ok") else json.dumps(out, ensure_ascii=False)[:600])
        if isinstance(out, dict) and out.get("ok"):
            for o, j in zip(out["out"], jobs):
                print(o["lang"], o["id"], "content md5 == wanted:", o["md5"] == hashlib.md5(j["content"].encode("utf-8")).hexdigest(),
                      "| title ok:", o["title"] == j["title"], "| meta ok:", all(o["meta"].get(k) == v for k, v in j["meta"].items()))
finally:
    snip("POST", "/%d/deactivate" % br, {}); s3, _ = snip("DELETE", "/%d" % br, None); time.sleep(1)
    s4, _, _ = req("POST", "/wp-json/nadlan-kochav76/v1/run", {"token": "x"})
    print("[bridge] deleted", s3, "route now", s4, "(want 404)")
