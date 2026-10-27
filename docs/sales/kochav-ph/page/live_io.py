# -*- coding: utf-8 -*-
"""Read or write the raw post_content of the Kochav listing (7634 he, 7812 en) through a temporary admin-only route (code-snippets),
the same way apply_page.py writes. Reading changes nothing.
  python live_io.py --fetch                      -> live-27-7634.html, live-27-7812.html (the live text today)
  python live_io.py --apply after-27-7634.html after-27-7812.html
                                                   -> writes only if the live text still equals live-27-<id>.html (md5 guard),
                                                      keeps nl_dossier=1, purges the cache, reads back
  python live_io.py --rollback                     -> writes live-27-<id>.html back over the round-27 version (same guard)"""
import hashlib, io, json, os, secrets, sys, time
H = os.path.dirname(os.path.abspath(__file__))
REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "kio"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req, snip = ns["req"], ns["snip"]
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
norm = lambda s: s.replace("\r\n", "\n")
md5 = lambda s: hashlib.md5(norm(s).encode("utf-8")).hexdigest()
IDS = (7634, 7812)
MODE = "fetch" if "--fetch" in sys.argv else ("rollback" if "--rollback" in sys.argv else "apply")
jobs = []
if MODE == "apply":
    files = [a for a in sys.argv[1:] if a.endswith(".html")]
    for pid, f in zip(IDS, files):
        old = io.open(os.path.join(H, "live-27-%d.html" % pid), encoding="utf-8").read()
        new = io.open(os.path.join(H, f), encoding="utf-8").read()
        jobs.append({"id": pid, "want": md5(old), "content": norm(new)})
elif MODE == "rollback":
    for pid in IDS:
        cur = io.open(os.path.join(H, "after-27-%d.html" % pid), encoding="utf-8").read()
        old = io.open(os.path.join(H, "live-27-%d.html" % pid), encoding="utf-8").read()
        jobs.append({"id": pid, "want": md5(cur), "content": norm(old)})
tok = secrets.token_hex(24)
code = r"""
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-kochav-io/v1', '/run', array( 'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__T__', (string) ( $b['token'] ?? '' ) ) ) { return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) ); }
			$out = array();
			if ( ! empty( $b['fetch'] ) ) {
				foreach ( (array) $b['fetch'] as $id ) { $p = get_post( (int) $id ); $out[] = array( 'id' => (int) $id, 'content' => $p ? $p->post_content : null, 'modified' => $p ? $p->post_modified : null ); }
				return array( 'ok' => true, 'out' => $out );
			}
			foreach ( (array) $b['jobs'] as $j ) {
				$p = get_post( (int) $j['id'] );
				$cur = $p ? md5( str_replace( "\r\n", "\n", $p->post_content ) ) : '';
				if ( $cur !== $j['want'] ) { $out[] = array( 'id' => $j['id'], 'err' => 'drift', 'cur' => $cur ); }
			}
			if ( $out ) { return array( 'ok' => false, 'out' => $out ); }
			kses_remove_filters();
			foreach ( (array) $b['jobs'] as $j ) {
				$r = wp_update_post( array( 'ID' => (int) $j['id'], 'post_content' => wp_slash( $j['content'] ) ), true );
				if ( 7634 === (int) $j['id'] ) { update_post_meta( 7634, 'nl_dossier', '1' ); }
				clean_post_cache( (int) $j['id'] );
				do_action( 'litespeed_purge_post', (int) $j['id'] );
				$u = get_permalink( (int) $j['id'] ); if ( $u ) { do_action( 'litespeed_purge_url', $u ); }
				$p = get_post( (int) $j['id'] );
				$out[] = array( 'id' => $j['id'], 'ok' => ! is_wp_error( $r ), 'md5' => md5( str_replace( "\r\n", "\n", $p->post_content ) ) );
			}
			kses_init_filters();
			return array( 'ok' => true, 'out' => $out );
		} ) );
} );
""".replace("__T__", tok)
s, c = snip("POST", "", {"name": "tmp-kochav-io-%d" % int(time.time()), "code": "/* placeholder */", "scope": "global", "active": False})
br = c["id"]
try:
    snip("PUT", "/%d" % br, {"name": c["name"], "code": code, "scope": "global", "active": False}); snip("PUT", "/%d/activate" % br, {}); time.sleep(1.5)
    body = {"token": tok, "fetch": list(IDS)} if MODE == "fetch" else {"token": tok, "jobs": jobs}
    s2, out, _ = req("POST", "/wp-json/nadlan-kochav-io/v1/run", body)
    if MODE == "fetch":
        for o in out["out"]:
            p = os.path.join(H, "live-27-%d.html" % o["id"])
            io.open(p, "w", encoding="utf-8", newline="").write(o["content"])
            last = os.path.join(H, "live-%d.html" % o["id"])
            same = os.path.exists(last) and norm(io.open(last, encoding="utf-8").read()) == norm(o["content"])
            print(o["id"], "modified", o["modified"], len(o["content"]), "chars, md5", md5(o["content"])[:10], "| same as live-%d.html (22.10):" % o["id"], same)
    else:
        print("run", s2, json.dumps(out, ensure_ascii=False)[:500])
        if isinstance(out, dict) and out.get("ok"):
            for o, j in zip(out["out"], jobs):
                print(o["id"], "written md5 == wanted:", o["md5"] == hashlib.md5(j["content"].encode("utf-8")).hexdigest())
finally:
    snip("POST", "/%d/deactivate" % br, {}); s3, _ = snip("DELETE", "/%d" % br, None); time.sleep(1)
    s4, _, _ = req("POST", "/wp-json/nadlan-kochav-io/v1/run", {"token": "x"})
    print("[bridge] deleted", s3, "route now", s4, "(want 404)")
