# -*- coding: utf-8 -*-
"""Rainbow's NIS per m² meta (the site loop, R1): project_3d_avg_price_per_sqm 76000 (Madlan, first half of 2023, shown as "לפי היזם") -> 81782, the developer's reported cumulative average through Q1 2026 (Bizportal 29.5.2026). Written only if the value is still 76000. Was: EcoCity takedown, the missed item (24.9.2026): /tour/ecocity/ still served EcoCity's "from the air" tour (a static
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
NS = "nadlan-meta258-" + TOKEN[:8]
BRIDGE = r"""
add_action( 'rest_api_init', function () {
	register_rest_route( '__NS__/v1', '/run', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( $b['token'] ?? '' ) ) ) { return new WP_Error( 'forbidden', 'token', array( 'status' => 400 ) ); }
			$pid = 4464; $key = 'project_3d_avg_price_per_sqm';
			$out = array( 'before' => get_post_meta( $pid, $key, true ) );
			if ( ! empty( $b['do'] ) && '76000' === (string) $out['before'] ) {
				update_post_meta( $pid, $key, 81782 );
				delete_transient( 'nlpjx_comps_v2_' . $pid );
				clean_post_cache( $pid );
				do_action( 'litespeed_purge_post', $pid );
				do_action( 'litespeed_purge_all' );
			}
			$out['after'] = get_post_meta( $pid, $key, true );
			return $out;
		},
	) );
} );
""".replace("__TOKEN__", TOKEN).replace("__NS__", NS)
s, c = req("POST", "/wp-json/code-snippets/v1/snippets", {"name": "x-tmp-meta258-%d" % int(time.time()), "code": BRIDGE, "scope": "global", "active": False})
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
    print("[before]", r)
    if not DRY:
        s, r2 = req("POST", "/wp-json/" + NS + "/v1/run", {"token": TOKEN, "do": 1})
        print("[set]", s, r2)
finally:
    req("PUT", "/wp-json/code-snippets/v1/snippets/%s/deactivate" % BR, {})
    s, _ = req("DELETE", "/wp-json/code-snippets/v1/snippets/%s" % BR)
    time.sleep(1.5)
    s2, _ = req("POST", "/wp-json/" + NS + "/v1/run", {"token": TOKEN})
    print("[bridge] delete http %s; route now http %s (want 404)" % (s, s2))
