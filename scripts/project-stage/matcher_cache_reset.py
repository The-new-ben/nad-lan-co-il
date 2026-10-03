# -*- coding: utf-8 -*-
"""HAD-396 release housekeeping (Maya 3.10.2026): the matcher's DB transient 'nl_matcher_v3_public' (1 h) can still hold rows built
before 1.72.415, where an urban-renewal compound's plan year fed "y" (delivery). wp_cache_flush does not delete a DB transient.
1. GET /wp-json/nadlan/v1/matcher-data (warm) and save it; 2. a temporary admin-only route deletes exactly that transient and
reports whether it existed; 3. GET again (cold: rebuilt by 1.72.415's code) and save it; 4. compare: the same rows and fields
(the privacy exclusions unchanged), only "y" may lose plan years. No code change, nothing else touched.
  python scripts/project-stage/matcher_cache_reset.py"""
import hashlib, json, os, secrets, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
_src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
_ns = {"__name__": "matcher_reset_helpers"}
exec(compile(_src[:_src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), _ns)
req, must, snip = _ns["req"], _ns["must"], _ns["snip"]
OUT = os.path.join(REPO, "docs", "qa", "had-396", "matcher-cache"); os.makedirs(OUT, exist_ok=True)


def public_get(tag):
    u = "https://nad-lan.co.il/wp-json/nadlan/v1/matcher-data?nlm=" + tag + str(int(time.time() * 1000))
    with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 NadLan-Matcher-Check/1.0"}), timeout=180) as r:
        b = r.read()
    open(os.path.join(OUT, f"matcher-{tag}.json"), "wb").write(b)
    return json.loads(b.decode("utf-8")), hashlib.md5(b).hexdigest()


warm, warm_md5 = public_get("warm")
TOKEN = secrets.token_hex(16)
BRIDGE = r"""
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-mreset/v1', '/go', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__T__', (string) ( $b['token'] ?? '' ) ) ) { return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) ); }
			$before = get_transient( 'nl_matcher_v3_public' );
			$timeout = (int) get_option( '_transient_timeout_nl_matcher_v3_public', 0 );
			$deleted = delete_transient( 'nl_matcher_v3_public' );
			$after = get_transient( 'nl_matcher_v3_public' );
			return array( 'existed' => is_array( $before ), 'rows_before' => is_array( $before ) ? count( (array) ( $before['rows'] ?? array() ) ) : 0,
				'expires_in_s' => $timeout ? $timeout - time() : null, 'deleted' => (bool) $deleted, 'gone' => false === $after );
		},
	) );
} );
""".replace("__T__", TOKEN)
s, c = snip("POST", "", {"name": f"tmp-matcher-reset-{int(time.time())}", "code": "/* placeholder */", "scope": "global", "active": False}); must(s, c, "snippet create")
try:
    s, u = snip("PUT", f"/{c['id']}", {"name": c["name"], "code": BRIDGE, "scope": "global", "active": False}); must(s, u, "snippet update")
    s, a = snip("PUT", f"/{c['id']}/activate", {}); must(s, a, "snippet activate")
    s, r, _ = req("POST", "/wp-json/nadlan-mreset/v1/go", {"token": TOKEN}, timeout=60); must(s, r, "delete transient")
finally:
    s1, _ = snip("PUT", f"/{c['id']}/deactivate", {}); s2, _ = snip("DELETE", f"/{c['id']}", None); print("[bridge] cleanup", s1, s2)
print("[delete]", json.dumps(r))
cold, cold_md5 = public_get("cold")
def stats(d):
    rows = d.get("rows") or []
    return {"rows": len(rows), "with_y": sum(1 for x in rows if x.get("y")), "keys": sorted({k for x in rows for k in x}), "slugs": sorted(x["s"] for x in rows)}
W, C = stats(warm), stats(cold)
yw = {x["s"]: x.get("y") for x in warm.get("rows") or []}; yc = {x["s"]: x.get("y") for x in cold.get("rows") or []}
changed = sorted(s for s in yw if s in yc and yw[s] != yc[s])
res = {"warm_md5": warm_md5, "cold_md5": cold_md5, "warm": {k: v for k, v in W.items() if k != "slugs"}, "cold": {k: v for k, v in C.items() if k != "slugs"},
       "same_rows": W["slugs"] == C["slugs"], "same_keys": W["keys"] == C["keys"], "same_cities": warm.get("cities") == cold.get("cities"),
       "y_changed": len(changed), "y_changed_examples": [(s, yw[s], yc[s]) for s in changed[:8]], "delete": r}
open(os.path.join(OUT, "compare.json"), "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1))
print(json.dumps(res, ensure_ascii=False)[:1500])
