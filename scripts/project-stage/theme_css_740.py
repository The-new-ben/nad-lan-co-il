# -*- coding: utf-8 -*-
"""HAD-740 fix 3 (Ben's decision relayed 15.11.2026: "להחליף כמו שהוא"): the theme stylesheet
wp-content/themes/nadlan-revenue/assets/css/nadlan-premium-sitewide.css, two rules only (.nldir-body and .nldir-hero widths
from min(1320px,calc(100vw - 28px)) to min(1320px,100%)). The live text was backed up first:
docs/qa/had-740/theme-css/live-before-2026-11-15.css; the new text is live-after-2026-11-15.css (diff: those two rules).
A temporary admin bridge (token, manage_options) writes the file only when the server file's md5 equals the backup's, keeps a copy
next to it (.bak-had740-20261115), reads the written file back (md5), and returns its mtime. --rollback writes the backup back.
python scripts/project-stage/theme_css_740.py --apply | --rollback"""
import base64, hashlib, io, os, secrets, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
D = os.path.join(REPO, "docs", "qa", "had-740", "theme-css")
BEFORE = open(os.path.join(D, "live-before-2026-11-15.css"), "rb").read()
AFTER = open(os.path.join(D, "live-after-2026-11-15.css"), "rb").read()
md5 = lambda b: hashlib.md5(b).hexdigest()
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "css740"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
req, snip = ns["req"], ns["snip"]
BRIDGE = r'''
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-css740/v1', '/run', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( $b['token'] ?? '' ) ) ) { return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) ); }
			$f = get_theme_root() . '/nadlan-revenue/assets/css/nadlan-premium-sitewide.css';
			if ( ! is_file( $f ) ) { return array( 'ok' => false, 'why' => 'no file ' . $f ); }
			$cur = (string) file_get_contents( $f );
			$out = array( 'path' => str_replace( ABSPATH, '', $f ), 'md5_before' => md5( $cur ) );
			if ( md5( $cur ) !== (string) $b['expect'] ) { $out['ok'] = false; $out['why'] = 'live md5 differs'; return $out; }
			$bak = $f . '.bak-had740-20261115';
			if ( ! file_exists( $bak ) ) { copy( $f, $bak ); }
			$new = base64_decode( (string) $b['b64'] );
			$w = file_put_contents( $f, $new );
			clearstatcache( true, $f );
			$out['written'] = $w; $out['md5_after'] = md5( (string) file_get_contents( $f ) ); $out['mtime'] = filemtime( $f ); $out['bak'] = file_exists( $bak );
			$out['ok'] = $out['md5_after'] === md5( $new );
			if ( function_exists( 'wp_cache_flush' ) ) { wp_cache_flush(); }
			return $out;
		},
	) );
} );
'''
if "--apply" in sys.argv:
    expect, payload = md5(BEFORE), AFTER
elif "--rollback" in sys.argv:
    expect, payload = md5(AFTER), BEFORE
else:
    raise SystemExit(__doc__)
tok = secrets.token_hex(24); nm = "tmp-css740-%d" % int(time.time())
s, sn = snip("POST", "", {"name": nm, "code": "/* placeholder */", "scope": "global", "active": False}); bid = sn["id"]
try:
    s1, _ = snip("PUT", "/%d" % bid, {"name": nm, "code": BRIDGE.replace("__TOKEN__", tok), "scope": "global", "active": False})
    s2, _ = snip("PUT", "/%d/activate" % bid, {})
    assert s1 == 200 and s2 == 200, (s1, s2)
    time.sleep(2)
    s, res, _ = req("POST", "/wp-json/nadlan-css740/v1/run", {"token": tok, "expect": expect, "b64": base64.b64encode(payload).decode()})
    print("[run]", s, res)
finally:
    a, _ = snip("PUT", "/%d/deactivate" % bid, {}); b, _ = snip("DELETE", "/%d" % bid, None)
    c, _, _ = req("POST", "/wp-json/nadlan-css740/v1/run", {"token": "x"})
    print("[bridge] deactivate", a, "| delete", b, "| route now", c, "(want 404)")
