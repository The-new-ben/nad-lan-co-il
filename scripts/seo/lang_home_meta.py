# -*- coding: utf-8 -*-
"""The Arabic language home's search title and description (28.9.2026). The head audit of the 145 language pages that
day: /ar/ was the only language home without a meta description, and its title was Arabic written in Latin letters
("NadLan AR — shaqaq wa-mashari fi Israil", the page's own title, which Yoast printed). /ru/ and /fr/ carry a title and a
description in their own script; /ar/ gets the same, in Arabic, built only from what the site has in Arabic (the
home, the Arabic guides, the 3D tours, the project pages). Same token-gated temporary bridge as project_meta.py; each
field guarded by the value read just before; the app password is decrypted in-process (DPAPI), never printed.
  python scripts/seo/lang_home_meta.py            # read and show the plan
  python scripts/seo/lang_home_meta.py --apply    # write"""
import io, json, os, secrets, sys, time
REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
src = io.open(os.path.join(REPO, "scripts", "project-stage", "rainbow_content4.py"), encoding="utf-8").read()
exec(compile(src[src.index("import base64, ctypes"):src.index("def read():")]
             .replace('QA = os.path.join(REPO, "docs", "qa", "rainbow-content-2026-09-24")', 'QA = os.path.join(REPO, "docs", "qa", "seo-meta-2026-09-28")'), "head", "exec"))

META = {
    "ar": {
        "title": "شقق ومشاريع جديدة في إسرائيل — الأسعار والمشاريع | NadLan",
        "desc": "مشاريع سكنية جديدة في إسرائيل: الأسعار، جولات ثلاثية الأبعاد في المشاريع وأدلة بالعربية للمشتري. افحصوا سعر الشقة ومحيطها قبل الشراء.",
    },
}
for k, v in META.items():
    assert len(v["desc"]) <= 160, (k, len(v["desc"]))
    assert "title" not in v or len(v["title"]) <= 66, (k, len(v["title"]))

PIDS = {}
for slug in META:
    s, d = req("GET", "/wp-json/wp/v2/pages?slug=%s&parent=0&_fields=id" % slug)
    PIDS[slug] = int(d[0]["id"])
TOKEN = secrets.token_hex(24)
NS = "nadlan-lhmeta-" + TOKEN[:8]
BRIDGE = r"""
add_action( 'rest_api_init', function () {
	register_rest_route( '__NS__/v1', '/run', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( $b['token'] ?? '' ) ) ) { return new WP_Error( 'forbidden', 'token', array( 'status' => 400 ) ); }
			$allowed = array( __PIDS__ );
			$out = array();
			foreach ( $allowed as $pid ) {
				$y = array();
				foreach ( get_post_meta( $pid ) as $k => $v ) { if ( 0 === strpos( $k, '_yoast_wpseo_' ) ) { $y[ $k ] = is_array( $v ) ? $v[0] : $v; } }
				$out[ $pid ] = array( 'before' => $y );
			}
			if ( ! empty( $b['do'] ) ) {
				foreach ( (array) ( $b['write'] ?? array() ) as $pid => $w ) {
					$pid = (int) $pid;
					if ( ! in_array( $pid, $allowed, true ) ) { continue; }
					$done = array();
					foreach ( (array) $w as $k => $pair ) {
						if ( 0 !== strpos( $k, '_yoast_wpseo_' ) ) { $done[ $k ] = 'SKIP: not a Yoast field'; continue; }
						$cur = (string) get_post_meta( $pid, $k, true );
						if ( $cur !== (string) $pair[0] ) { $done[ $k ] = 'SKIP: changed since read'; continue; }
						update_post_meta( $pid, $k, wp_slash( (string) $pair[1] ) );
						$done[ $k ] = 'ok';
					}
					if ( function_exists( 'YoastSEO' ) ) {
						try {
							$repo = YoastSEO()->classes->get( \Yoast\WP\SEO\Repositories\Indexable_Repository::class );
							$bld  = YoastSEO()->classes->get( \Yoast\WP\SEO\Builders\Indexable_Builder::class );
							$ix   = $repo->find_by_id_and_type( $pid, 'post', false );
							if ( $ix ) { $bld->build_for_id_and_type( $pid, 'post', $ix ); $done['indexable'] = 'rebuilt'; }
						} catch ( \Throwable $e ) { $done['indexable'] = 'error: ' . $e->getMessage(); }
					}
					clean_post_cache( $pid );
					do_action( 'litespeed_purge_post', $pid );
					$out[ $pid ]['done'] = $done;
					$y = array();
					foreach ( get_post_meta( $pid ) as $k => $v ) { if ( 0 === strpos( $k, '_yoast_wpseo_' ) ) { $y[ $k ] = is_array( $v ) ? $v[0] : $v; } }
					$out[ $pid ]['after'] = $y;
				}
				do_action( 'litespeed_purge_all' );
			}
			return $out;
		},
	) );
} );
""".replace("__TOKEN__", TOKEN).replace("__NS__", NS).replace("__PIDS__", ", ".join(str(p) for p in PIDS.values()))

s, c = req("POST", "/wp-json/code-snippets/v1/snippets", {"name": "x-tmp-lhmeta-%d" % int(time.time()), "code": BRIDGE, "scope": "global", "active": False})
if s not in (200, 201):
    raise SystemExit("FATAL bridge create %s %s" % (s, str(c)[:200]))
BR = c["id"]
try:
    req("PUT", "/wp-json/code-snippets/v1/snippets/%s/activate" % BR, {})
    r = None
    for _ in range(10):
        s, r = req("POST", "/wp-json/" + NS + "/v1/run", {"token": TOKEN})
        if s == 200:
            break
        time.sleep(1.5)
    if s != 200:
        raise SystemExit("FATAL bridge call %s %s" % (s, str(r)[:300]))
    write = {}
    for slug, v in META.items():
        pid = PIDS[slug]
        y = r[str(pid)]["before"]
        y = y if isinstance(y, dict) else {}  # PHP sends an empty array as []
        w = {}
        if "title" in v:
            w["_yoast_wpseo_title"] = [y.get("_yoast_wpseo_title", ""), v["title"]]
        w["_yoast_wpseo_metadesc"] = [y.get("_yoast_wpseo_metadesc", ""), v["desc"]]
        for k in ("_yoast_wpseo_opengraph-description", "_yoast_wpseo_twitter-description"):
            if y.get(k):
                w[k] = [y[k], v["desc"]]
        write[str(pid)] = w
        print("[%s %d] before: title=%r desc=%r" % (slug, pid, y.get("_yoast_wpseo_title", ""), y.get("_yoast_wpseo_metadesc", "")[:80]))
        print("   plan:", json.dumps({k: x[1] for k, x in w.items()}, ensure_ascii=False))
    if "--apply" in sys.argv:
        os.makedirs(QA, exist_ok=True)
        stamp = time.strftime("%Y%m%dT%H%M%S")
        io.open(os.path.join(QA, "lang-home-meta.%s.before.json" % stamp), "w", encoding="utf-8").write(json.dumps(r, ensure_ascii=False, indent=1))
        s, r2 = req("POST", "/wp-json/" + NS + "/v1/run", {"token": TOKEN, "do": 1, "write": write})
        print("[set]", s, json.dumps({k: v.get("done") for k, v in r2.items()} if isinstance(r2, dict) else r2, ensure_ascii=False))
        io.open(os.path.join(QA, "lang-home-meta.%s.after.json" % stamp), "w", encoding="utf-8").write(json.dumps(r2, ensure_ascii=False, indent=1))
finally:
    req("PUT", "/wp-json/code-snippets/v1/snippets/%s/deactivate" % BR, {})
    s, _ = req("DELETE", "/wp-json/code-snippets/v1/snippets/%s" % BR)
    time.sleep(1.5)
    s2, _ = req("POST", "/wp-json/" + NS + "/v1/run", {"token": TOKEN})
    print("[bridge] delete http %s; route now http %s (want 404)" % (s, s2))
