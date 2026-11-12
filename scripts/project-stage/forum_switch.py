# -*- coding: utf-8 -*-
"""HAD-726: open or close the professionals' forum to the public (option nadlan_forum_public), owner order 12.11.2026
("upload it and show me with a link, put it in the menu"). Same temporary admin bridge as live_read.py: a one-run Code
Snippet with a random token, deleted at the end; it writes ONE option and purges the page cache so the menu column and the
forum appear (or disappear) at once. The app password is decrypted in-process (DPAPI) and never printed.

  python scripts/project-stage/forum_switch.py on|off|status"""
import json, os, secrets, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
MODE = (sys.argv[1] if len(sys.argv) > 1 else "status").lower()
if MODE not in ("on", "off", "status"):
    raise SystemExit("usage: forum_switch.py on|off|status")
_src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
_ns = {"__name__": "forum_switch_helpers"}
exec(compile(_src[:_src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), _ns)
req, must, snip = _ns["req"], _ns["must"], _ns["snip"]
TOKEN = secrets.token_hex(24)
BRIDGE = r'''
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-forum-switch/v1', '/set', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( isset( $b['token'] ) ? $b['token'] : '' ) ) ) { return new WP_Error( 'bad', 'token', array( 'status' => 400 ) ); }
			$before = (string) get_option( 'nadlan_forum_public', '0' );
			$mode = (string) ( isset( $b['mode'] ) ? $b['mode'] : 'status' );
			if ( 'on' === $mode || 'off' === $mode ) {
				update_option( 'nadlan_forum_public', 'on' === $mode ? '1' : '0', true );
				do_action( 'litespeed_purge_all' );
				if ( function_exists( 'wp_cache_flush' ) ) { wp_cache_flush(); }
			}
			return array( 'before' => $before, 'after' => (string) get_option( 'nadlan_forum_public', '0' ), 'module' => function_exists( 'nlf_public' ) ? 1 : 0 );
		},
	) );
} );
'''.replace("__TOKEN__", TOKEN)
s, c = snip("POST", "", {"name": f"tmp-forum-switch-{int(time.time())}", "code": "/* placeholder */", "scope": "global", "active": False})
must(s, c, "bridge create")
BR = c["id"]
try:
    s, u = snip("PUT", f"/{BR}", {"name": c["name"], "code": BRIDGE, "scope": "global", "active": False}); must(s, u, "bridge update")
    s, a = snip("PUT", f"/{BR}/activate", {}); must(s, a, "bridge activate")
    s, r, _ = req("POST", "/wp-json/nadlan-forum-switch/v1/set", {"token": TOKEN, "mode": MODE}, timeout=90); must(s, r, "set")
    print("[forum] nadlan_forum_public", r.get("before"), "->", r.get("after"), "| module loaded:", r.get("module"))
finally:
    s1, _ = snip("PUT", f"/{BR}/deactivate", {}); s2, _ = snip("DELETE", f"/{BR}", None)
    print("[bridge] cleanup", s1, s2)
