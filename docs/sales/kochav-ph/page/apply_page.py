# -*- coding: utf-8 -*-
"""Writes after-7634.html / after-7812.html (build_page.py) into the live posts, through a temporary admin-only bridge.
Guard: the live content must still equal before-<id>.html (line endings aside), or nothing is written. The old content
stays in before-<id>.html and in WordPress's own revisions. --rollback writes the before files back the same way.
  python docs/sales/kochav-ph/page/apply_page.py [--rollback]"""
import hashlib, io, json, os, secrets, sys, time
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "de"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req, snip = ns["req"], ns["snip"]
RB = "--rollback" in sys.argv
norm = lambda s: s.replace("\r\n", "\n")
md5 = lambda s: hashlib.md5(norm(s).encode("utf-8")).hexdigest()
jobs = []
for pid in (7634, 7812):
    before = io.open(os.path.join(H, ("meital-%d.html" if "--over-meital" in sys.argv else "before-%d.html") % pid), encoding="utf-8").read()
    after = io.open(os.path.join(H, "after-%d.html" % pid), encoding="utf-8").read()
    old, new = (after, before) if RB else (before, after)
    jobs.append({"id": pid, "want": md5(old), "content": norm(new)})
tok = secrets.token_hex(24)
code = r"""
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-kochav-ops/v1', '/run', array( 'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__T__', (string) ( $b['token'] ?? '' ) ) ) { return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) ); }
			$out = array();
			foreach ( (array) $b['jobs'] as $j ) {
				$p = get_post( (int) $j['id'] );
				if ( ! $p ) { $out[] = array( 'id' => $j['id'], 'err' => 'no post' ); continue; }
				$cur = md5( str_replace( "\r\n", "\n", $p->post_content ) );
				if ( $cur !== $j['want'] ) { $out[] = array( 'id' => $j['id'], 'err' => 'drift', 'cur' => $cur ); continue; }
			}
			if ( $out ) { return array( 'ok' => false, 'out' => $out ); }
			kses_remove_filters();
			foreach ( (array) $b['jobs'] as $j ) {
				$r = wp_update_post( array( 'ID' => (int) $j['id'], 'post_content' => wp_slash( $j['content'] ) ), true );
				if ( (int) $j['id'] === 7634 ) { update_post_meta( 7634, 'nl_dossier', '1' ); } // x-broker-edit 1.1.0: a broker save no longer rewrites this page
				clean_post_cache( (int) $j['id'] );
				do_action( 'litespeed_purge_post', (int) $j['id'] );
				$u = get_permalink( (int) $j['id'] ); if ( $u ) { do_action( 'litespeed_purge_url', $u ); }
				$p = get_post( (int) $j['id'] );
				$out[] = array( 'id' => $j['id'], 'ok' => ! is_wp_error( $r ), 'len' => strlen( $p->post_content ), 'md5' => md5( str_replace( "\r\n", "\n", $p->post_content ) ) );
			}
			kses_init_filters();
			return array( 'ok' => true, 'out' => $out );
		} ) );
} );
""".replace("__T__", tok)
s, c = snip("POST", "", {"name": "tmp-kochav-page-%d" % int(time.time()), "code": "/* placeholder */", "scope": "global", "active": False})
br = c["id"]
try:
    snip("PUT", "/%d" % br, {"name": c["name"], "code": code, "scope": "global", "active": False}); snip("PUT", "/%d/activate" % br, {}); time.sleep(1.5)
    s2, out, _ = req("POST", "/wp-json/nadlan-kochav-ops/v1/run", {"token": tok, "jobs": jobs})
    print("run", s2, json.dumps(out, ensure_ascii=False)[:600])
    if isinstance(out, dict) and out.get("ok"):
        for o, j in zip(out["out"], jobs):
            print(o["id"], "written md5", o["md5"], "== wanted", hashlib.md5(j["content"].encode("utf-8")).hexdigest(), o["md5"] == hashlib.md5(j["content"].encode("utf-8")).hexdigest())
finally:
    snip("POST", "/%d/deactivate" % br, {}); s3, _ = snip("DELETE", "/%d" % br, None); time.sleep(1)
    s4, _, _ = req("POST", "/wp-json/nadlan-kochav-ops/v1/run", {"token": "x"})
    print("[bridge] deleted", s3, "route now", s4, "(want 404)")
