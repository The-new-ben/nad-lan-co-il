# -*- coding: utf-8 -*-
"""Reset today's video-room opening counters of THIS computer's connection and of the test kit's members (live checks open
many rooms from one connection and hit the 8-a-day cap). Touches only those counters.
  python scripts/project-stage/forum_call_rl_reset.py"""
import json, os, secrets, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
_src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
_ns = {"__name__": "rl_reset_helpers"}
exec(compile(_src[:_src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), _ns)
req, must, snip = _ns["req"], _ns["must"], _ns["snip"]
MEMS = [m["id"] for m in json.load(open(os.path.join(os.environ.get("TEMP", "."), "nlf_testkit_cookies.json"), encoding="utf-8"))["members"]]
TOKEN = secrets.token_hex(24)
BRIDGE = r'''
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-rl-reset/v1', '/run', array( 'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( $b['token'] ?? '' ) ) ) { return new WP_Error( 'bad', 'token', array( 'status' => 400 ) ); }
			if ( ! function_exists( 'nlfc_rl_key' ) ) { return array( 'err' => 'call module not loaded' ); }
			$who = array( nlf_ip_hash() );
			foreach ( (array) $b['members'] as $m ) { $who[] = 'm' . (int) $m; }
			$n = 0;
			foreach ( array( 'room', 'join', 'tok' ) as $bk ) {
				foreach ( $who as $w ) {
					foreach ( array( DAY_IN_SECONDS, 600 ) as $win ) { if ( delete_transient( nlfc_rl_key( $bk, $w, time(), $win ) ) ) { $n++; } }
				}
			}
			return array( 'deleted' => $n );
		} ) );
} );
'''.replace("__TOKEN__", TOKEN)
s, c = snip("POST", "", {"name": f"tmp-rl-reset-{int(time.time())}", "code": "/* placeholder */", "scope": "global", "active": False})
must(s, c, "bridge create")
BR = c["id"]
try:
    s, u = snip("PUT", f"/{BR}", {"name": c["name"], "code": BRIDGE, "scope": "global", "active": False}); must(s, u, "bridge update")
    s, a = snip("PUT", f"/{BR}/activate", {}); must(s, a, "bridge activate")
    s, r, _ = req("POST", "/wp-json/nadlan-rl-reset/v1/run", {"token": TOKEN, "members": MEMS}, timeout=60); must(s, r, "run")
    print("[rl]", json.dumps(r))
finally:
    s1, _ = snip("PUT", f"/{BR}/deactivate", {}); s2, _ = snip("DELETE", f"/{BR}", None)
    print("[bridge] cleanup", s1, s2)
