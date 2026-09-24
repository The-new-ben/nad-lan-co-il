# -*- coding: utf-8 -*-
"""EcoCity takedown, the missed item (24.9.2026): /tour/ecocity/ still served EcoCity's "from the air" tour (a static
file dated 30.8, found by the Rainbow-run research). The owner's 30.8 order is absolute: all their content down, tour
off. This takes it off by RENAMING its folder under the web root (nothing is deleted; it can be renamed back), then
checks the address no longer serves it. Same token-gated temporary bridge as the release runners; the app password is
decrypted in-process (DPAPI), never printed.
  python scripts/ecocity/tour_off.py [--dry]"""
import base64, ctypes, ctypes.wintypes, io, json, secrets, sys, time, urllib.request, urllib.error
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = "https://nad-lan.co.il"
SECRETS_PATH = r"C:\Users\777\Documents\websites\.codex-secrets\wordpress-app-passwords\nad-lan.co.il.json"
DRY = "--dry" in sys.argv


class DB(ctypes.Structure):
    _fields_ = [("cb", ctypes.wintypes.DWORD), ("pb", ctypes.POINTER(ctypes.c_char))]


def dpapi(b64):
    raw = base64.b64decode(b64)
    bi = DB(len(raw), ctypes.cast(ctypes.create_string_buffer(raw, len(raw)), ctypes.POINTER(ctypes.c_char)))
    bo = DB()
    if not ctypes.windll.crypt32.CryptUnprotectData(ctypes.byref(bi), None, None, None, None, 0, ctypes.byref(bo)):
        raise RuntimeError("DPAPI")
    try:
        return ctypes.string_at(bo.pb, bo.cb).decode("utf-8")
    finally:
        ctypes.windll.kernel32.LocalFree(bo.pb)


with open(SECRETS_PATH, encoding="utf-8-sig") as f:
    sec = json.load(f)
AUTH = "Basic " + base64.b64encode((sec["username"] + ":" + dpapi(sec["password_dpapi"])).encode()).decode()
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) NadLan-ECO-OFF/1.0"


def req(method, path, body=None, timeout=60, auth=True, raw=False):
    r = urllib.request.Request(BASE + path, data=None if body is None else json.dumps(body, ensure_ascii=False).encode(), method=method)
    if auth:
        r.add_header("Authorization", AUTH)
    r.add_header("User-Agent", UA)
    if body is not None:
        r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            p = resp.read()
            return resp.status, (p if raw else json.loads(p.decode("utf-8") or "null"))
    except urllib.error.HTTPError as e:
        p = e.read()
        if raw:
            return e.code, p
        try:
            return e.code, json.loads(p.decode("utf-8"))
        except Exception:
            return e.code, {"raw": p[:200].decode("utf-8", "replace")}


TOKEN = secrets.token_hex(24)
NS = "nadlan-ecooff-" + TOKEN[:8]
STAMP = time.strftime("%Y%m%d")
BRIDGE = r'''
add_action( 'rest_api_init', function () {
	register_rest_route( '__NS__/v1', '/run', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( $b['token'] ?? '' ) ) ) { return new WP_Error( 'forbidden', 'token', array( 'status' => 400 ) ); }
			$dir = rtrim( ABSPATH, '/' ) . '/tour/ecocity';
			$off = rtrim( ABSPATH, '/' ) . '/tour/_off-ecocity-__STAMP__';
			$out = array( 'exists' => is_dir( $dir ) ? 1 : 0, 'is_file_index' => file_exists( $dir . '/index.html' ) ? 1 : 0, 'already_off' => is_dir( $off ) ? 1 : 0 );
			if ( is_dir( $dir ) ) { $out['files'] = array_slice( array_values( array_diff( scandir( $dir ), array( '.', '..' ) ) ), 0, 30 ); }
			if ( ! empty( $b['do'] ) && is_dir( $dir ) && ! is_dir( $off ) ) { $out['renamed'] = @rename( $dir, $off ) ? 1 : 0; clearstatcache(); $out['exists_after'] = is_dir( $dir ) ? 1 : 0; }
			// out of the web root altogether: a renamed folder under it is still served at its new address
			$vault = dirname( rtrim( ABSPATH, '/' ) ) . '/nadlan-offline';
			$out['vault_parent_writable'] = is_writable( dirname( rtrim( ABSPATH, '/' ) ) ) ? 1 : 0;
			if ( ! empty( $b['vault'] ) && is_dir( $off ) ) {
				if ( ! is_dir( $vault ) ) { @mkdir( $vault, 0750 ); }
				$dest = $vault . '/ecocity-tour-__STAMP__';
				$out['vault_made'] = is_dir( $vault ) ? 1 : 0;
				$out['moved_out'] = ( is_dir( $vault ) && ! file_exists( $dest ) && @rename( $off, $dest ) ) ? 1 : 0;
				clearstatcache();
				$out['still_under_webroot'] = is_dir( $off ) ? 1 : 0;
				$out['in_vault'] = is_dir( $dest ) ? 1 : 0;
			}
			return $out;
		},
	) );
} );
'''.replace("__TOKEN__", TOKEN).replace("__NS__", NS).replace("__STAMP__", STAMP)

s, h = req("GET", "/wp-json/nadlan/v1/health", auth=False)
print("[health]", s, h.get("version") if isinstance(h, dict) else h)
s, c = req("POST", "/wp-json/code-snippets/v1/snippets", {"name": "x-tmp-ecooff-%d" % int(time.time()), "code": BRIDGE, "scope": "global", "active": False})
if s not in (200, 201):
    raise SystemExit("FATAL bridge create %s" % s)
BR = c["id"]
try:
    req("PUT", "/wp-json/code-snippets/v1/snippets/%s/activate" % BR, {})
    for _ in range(10):
        s, r = req("POST", "/wp-json/" + NS + "/v1/run", {"token": TOKEN})
        if s == 200:
            break
        time.sleep(1.5)
    print("[before]", json.dumps(r, ensure_ascii=False))
    if not DRY and isinstance(r, dict) and r.get("exists"):
        s, r2 = req("POST", "/wp-json/" + NS + "/v1/run", {"token": TOKEN, "do": 1})
        print("[rename]", s, json.dumps(r2, ensure_ascii=False))
    if not DRY and "--vault" in sys.argv:
        s, r3 = req("POST", "/wp-json/" + NS + "/v1/run", {"token": TOKEN, "vault": 1})
        print("[vault]", s, json.dumps(r3, ensure_ascii=False))
finally:
    req("PUT", "/wp-json/code-snippets/v1/snippets/%s/deactivate" % BR, {})
    s, _ = req("DELETE", "/wp-json/code-snippets/v1/snippets/%s" % BR)
    time.sleep(1.5)
    s2, _ = req("POST", "/wp-json/" + NS + "/v1/run", {"token": TOKEN})
    print("[bridge] delete http %s; route now http %s (want 404)" % (s, s2))
s3, body = req("GET", "/tour/ecocity/?c=%d" % int(time.time()), auth=False, raw=True)
print("[public] /tour/ecocity/ ->", s3, "| still EcoCity:", "אקו סיטי" in body.decode("utf-8", "replace"))
s4, _ = req("GET", "/tour/_off-ecocity-%s/?c=%d" % (STAMP, int(time.time())), auth=False, raw=True)
print("[public] renamed address ->", s4)
