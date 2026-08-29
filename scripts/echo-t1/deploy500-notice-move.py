# -*- coding: utf-8 -*-
"""Move the per-project independence notice DOWN (owner order 29.8): from directly
under the lead to the head of the article section, after the engine blocks.
Live-byte patch of inc/legal-notice.php + version bump 1.72.221 -> 1.72.222."""
import base64, ctypes, ctypes.wintypes, hashlib, io, json, re, secrets, sys, time, urllib.request, urllib.error
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = "https://nad-lan.co.il"
SECRETS_PATH = r"C:\Users\777\Documents\websites\.codex-secrets\wordpress-app-passwords\nad-lan.co.il.json"

class DB(ctypes.Structure):
    _fields_ = [("cb", ctypes.wintypes.DWORD), ("pb", ctypes.POINTER(ctypes.c_char))]

def dp(b):
    raw = base64.b64decode(b)
    bi = DB(len(raw), ctypes.cast(ctypes.create_string_buffer(raw, len(raw)), ctypes.POINTER(ctypes.c_char)))
    bo = DB()
    assert ctypes.windll.crypt32.CryptUnprotectData(ctypes.byref(bi), None, None, None, None, 0, ctypes.byref(bo))
    try:
        return ctypes.string_at(bo.pb, bo.cb).decode()
    finally:
        ctypes.windll.kernel32.LocalFree(bo.pb)

sec = json.load(open(SECRETS_PATH, encoding="utf-8-sig"))
AUTH = "Basic " + base64.b64encode((sec["username"] + ":" + dp(sec["password_dpapi"])).encode()).decode()

def req(method, path, body=None, timeout=120, raw=False):
    r = urllib.request.Request(BASE + path, data=None if body is None else json.dumps(body, ensure_ascii=False).encode(), method=method)
    r.add_header("Authorization", AUTH)
    r.add_header("User-Agent", "NadLan-notice-move/1.0")
    if body is not None:
        r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            payload = resp.read()
            return resp.status, payload if raw else json.loads(payload.decode("utf-8") or "null")
    except urllib.error.HTTPError as e:
        p = e.read()
        try:
            return e.code, json.loads(p.decode("utf-8"))
        except Exception:
            return e.code, {"raw": p[:300].decode("utf-8", "replace")}

def must(s, p, what, ok=(200, 201)):
    if s not in ok:
        raise SystemExit(f"FATAL {what}: HTTP {s}: {json.dumps(p, ensure_ascii=False)[:300]}")
    return p

s, h = req("GET", "/wp-json/nadlan/v1/health")
must(s, h, "health")
assert h.get("version") == "1.72.221" and h.get("status") == "ok"
print("[health]", h.get("version"))

TOKEN = secrets.token_hex(24)
BRIDGE = r'''
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-notice-ops/v1', '/apply', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( $b['token'] ?? '' ) ) ) {
				return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) );
			}
			$root = WP_PLUGIN_DIR . '/nadlan-config/';
			$out = array();
			if ( ! empty( $b['get'] ) ) {
				$p = $root . ltrim( str_replace( '..', '', (string) $b['get'] ), '/' );
				if ( ! is_readable( $p ) ) { return new WP_Error( 'missing', $b['get'], array( 'status' => 404 ) ); }
				$d = file_get_contents( $p );
				$out['get'] = array( 'b64' => base64_encode( $d ), 'md5' => md5( $d ) );
			}
			if ( ! empty( $b['put'] ) && is_array( $b['put'] ) ) {
				$p = $root . ltrim( str_replace( '..', '', (string) $b['put']['rel'] ), '/' );
				$d = base64_decode( (string) $b['put']['b64'], true );
				if ( false === $d || md5( $d ) !== strtolower( (string) $b['put']['md5'] ) ) { return new WP_Error( 'md5', 'mismatch', array( 'status' => 400 ) ); }
				try { token_get_all( $d, TOKEN_PARSE ); } catch ( ParseError $e ) { return new WP_Error( 'lint', $e->getMessage(), array( 'status' => 400 ) ); }
				if ( file_exists( $p ) && ! file_exists( $p . '.bakNotice' ) ) { copy( $p, $p . '.bakNotice' ); }
				$w = file_put_contents( $p, $d );
				$out['put'] = array( 'bytes' => $w, 'md5' => md5_file( $p ) );
			}
			if ( ! empty( $b['purge'] ) ) { do_action( 'litespeed_purge_all' ); $out['purged'] = 1; }
			return $out;
		},
	) );
} );
'''.replace("__TOKEN__", TOKEN)

def snip(method, path, body=None):
    return req(method, f"/wp-json/code-snippets/v1/snippets{path}", body=body)

s, c = snip("POST", "", {"name": f"tmp-notice-ops-{int(time.time())}", "code": BRIDGE, "scope": "global", "active": False})
must(s, c, "bridge create")
BR = c["id"]
must(*snip("PUT", f"/{BR}/activate", {}), "bridge activate")

def ops(payload, what):
    payload["token"] = TOKEN
    s, r = req("POST", "/wp-json/nadlan-notice-ops/v1/apply", body=payload, timeout=180)
    must(s, r, what)
    return r

def patch(rel, edits):
    cur = ops({"get": rel}, f"get {rel}")["get"]
    text = base64.b64decode(cur["b64"]).decode("utf-8")
    for old, new in edits:
        n = text.count(old)
        assert n == 1, f"anchor x{n} in {rel}: {old[:70]!r}"
        text = text.replace(old, new)
    out = text.encode("utf-8")
    w = ops({"put": {"rel": rel, "b64": base64.b64encode(out).decode(), "md5": hashlib.md5(out).hexdigest()}}, f"put {rel}")
    print(f"[patch] {rel} {cur['md5'][:8]} -> {w['put']['md5'][:8]}")

OLD_RET = "\t\t$html = '<aside class=\"nl-projnotice\" dir=\"' . ( $rtl ? 'rtl' : 'ltr' ) . '\" role=\"note\">'\n\t\t\t. '<b>' . esc_html( $str[0] ) . '</b><span>' . esc_html( $text ) . '</span></aside>';\n\t\treturn $html . $content;"
NEW_RET = ("\t\t$html = '<aside class=\"nl-projnotice\" dir=\"' . ( $rtl ? 'rtl' : 'ltr' ) . '\" role=\"note\">'\n"
           "\t\t\t. '<b>' . esc_html( $str[0] ) . '</b><span>' . esc_html( $text ) . '</span></aside>';\n"
           "\t\t/* Owner order 29.8.2026: the notice moves DOWN, out of the snippet zone.\n"
           "\t\t * It now opens the article section (still in-body, still next to the\n"
           "\t\t * developer-named content, per the active-disclosure duty); on pages\n"
           "\t\t * without the article wrapper it closes the content instead. */\n"
           "\t\t$nl_article_at = strpos( $content, '<div class=\"nadlan-project-article' );\n"
           "\t\tif ( false !== $nl_article_at ) {\n"
           "\t\t\treturn substr( $content, 0, $nl_article_at ) . $html . substr( $content, $nl_article_at );\n"
           "\t\t}\n"
           "\t\treturn $content . $html;")
patch("inc/legal-notice.php", [(OLD_RET, NEW_RET)])
patch("nadlan-config.php", [
    (" * Version: 1.72.221", " * Version: 1.72.222"),
    ("define( 'NADLAN_CONFIG_VERSION', '1.72.221' )", "define( 'NADLAN_CONFIG_VERSION', '1.72.222' )"),
])

ops({"purge": 1}, "purge")
s, d = snip("DELETE", f"/{BR}", None)
print("[bridge-delete]", s)

time.sleep(10)
s, h2 = req("GET", "/wp-json/nadlan/v1/health")
print("[health-after]", h2.get("version"), h2.get("status"))
assert h2.get("version") == "1.72.222" and h2.get("status") == "ok"
for slug in ("bnei-dan-54-56", "rainbow-tel-aviv", "aurelia", "h-infinity-somail-tel-aviv"):
    s, page = req("GET", f"/projects/{slug}/", raw=True)
    hh = page.decode("utf-8", "replace")
    n = hh.find('<aside class="nl-projnotice"')
    lead = hh.find('nl-lead')
    art = hh.find('nadlan-project-article')
    rel = "none" if n < 0 else ("article-head" if art > 0 and abs(n - art) < 200 and n < art + 200 and n > lead else f"pos {n} (lead {lead}, article {art})")
    ok = (n < 0 and slug == "aurelia") or (n > 0 and art > 0 and lead > 0 and n > lead and n >= art - 10)
    print(f"[verify] {slug}: http {s} | notice@{n} lead@{lead} article@{art} | moved-below: {ok}")
print("NOTICE MOVE DONE")
