# -*- coding: utf-8 -*-
"""Fill the nearby-places cache for project points that moved (28.9.2026, after somail_locations.py).
A project map reads nearby places (OpenStreetMap Overpass) from a cache keyed by the point; a new point queues a WP-Cron
fetch, and the map shows the layer empty until it lands. This asks the server, through a temporary admin-only route
(created, called once, deleted), for the breaker state and the cron state, then runs the fetch for each point and reports
the counts per group. Same auth as the release runners (DPAPI in-process, never printed).
  python scripts/project-stage/poi_warm.py 32.087284,34.78272 32.085698,34.782856 [--radius 1200] [--reset-breaker]"""
import base64, ctypes, ctypes.wintypes, hashlib, io, json, os, re, secrets, subprocess, sys, tempfile, time, urllib.request, urllib.error, zlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = "https://nad-lan.co.il"
REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
SECRETS_PATH = r"C:\Users\777\Documents\websites\.codex-secrets\wordpress-app-passwords\nad-lan.co.il.json"
ARGS = sys.argv[1:]
DRY = "--dry" in ARGS
BAK = ".bak330"
CRLF, LF = bytes([13, 10]), bytes([10])


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
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) NadLan-PS330/1.0"


def req(method, path, body=None, timeout=120, raw=False, auth=True):
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
            return e.code, {"raw": p[:300].decode("utf-8", "replace")}


def must(s, p, what, ok=(200, 201)):
    if s not in ok:
        raise SystemExit(f"FATAL {what}: HTTP {s}: {json.dumps(p, ensure_ascii=False)[:400]}")
    return p


def md5(b):
    return hashlib.md5(b).hexdigest()


def php_lint(data, label):
    with tempfile.NamedTemporaryFile("wb", suffix=".php", delete=False) as t:
        t.write(data)
        tmp = t.name
    try:
        out = subprocess.run(["php", "-l", tmp], capture_output=True, text=True)
    finally:
        os.unlink(tmp)
    if out.returncode != 0:
        raise SystemExit(f"FATAL local lint {label}: {out.stdout.strip()} {out.stderr.strip()}")
    print(f"[lint] {label}: ok")


def git_head(rel):
    out = subprocess.run(["git", "-C", REPO, "show", "HEAD:" + rel.replace(os.sep, "/")], capture_output=True)
    if out.returncode != 0:
        return None
    return out.stdout



PTS = [tuple(float(x) for x in a.split(",")) for a in ARGS if "," in a and not a.startswith("--")]
RADIUS = int(ARGS[ARGS.index("--radius") + 1]) if "--radius" in ARGS else 1200
RESET = "--reset-breaker" in ARGS
TOKEN = secrets.token_hex(24)
NS = "nadlan-poiw-" + TOKEN[:8]
BRIDGE = r"""
add_action( 'rest_api_init', function () {
	register_rest_route( '__NS__/v1', '/run', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( $b['token'] ?? '' ) ) ) { return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) ); }
			$out = array( 'down' => get_transient( 'nadlan_poi_down' ) ? 1 : 0, 'rate' => (int) get_transient( 'nadlan_poi_rate' ),
				'wp_cron_disabled' => ( defined( 'DISABLE_WP_CRON' ) && DISABLE_WP_CRON ) ? 1 : 0, 'fn' => function_exists( 'nadlan_poi_fetch_remote' ) ? 1 : 0 );
			if ( ! empty( $b['reset'] ) ) { delete_transient( 'nadlan_poi_down' ); $out['reset'] = 1; }
			$out['pts'] = array();
			foreach ( (array) ( $b['pts'] ?? array() ) as $p ) {
				$la = round( (float) $p[0], 4 ); $ln = round( (float) $p[1], 4 ); $r = (int) $p[2];
				$key = function_exists( 'nadlan_poi_key' ) ? nadlan_poi_key( $la, $ln, $r ) : '';
				$row = array( 'lat' => $la, 'lng' => $ln, 'cached_before' => is_array( get_transient( $key ) ) ? 1 : 0,
					'scheduled' => wp_next_scheduled( 'nadlan_poi_refresh', array( $la, $ln, $r ) ) ?: 0 );
				if ( ! get_transient( 'nadlan_poi_down' ) && $out['fn'] ) {
					$t0 = microtime( true );
					$g = nadlan_poi_fetch_remote( $la, $ln, $r );
					$row['secs'] = round( microtime( true ) - $t0, 2 );
					$row['counts'] = array_map( 'count', (array) $g );
				}
				$row['down_after'] = get_transient( 'nadlan_poi_down' ) ? 1 : 0;
				$out['pts'][] = $row;
			}
			return $out;
		},
	) );
} );
""".replace("__TOKEN__", TOKEN).replace("__NS__", NS)


def snip(method, path, body=None):
    return req(method, "/wp-json/code-snippets/v1/snippets" + path, body=body)


s, c = snip("POST", "", {"name": "x-tmp-poiw-%d" % int(time.time()), "code": BRIDGE, "scope": "global", "active": False})
must(s, c, "bridge create")
BR = c["id"]
try:
    must(*snip("PUT", "/%s/activate" % BR, {}), "bridge activate")
    time.sleep(1.5)
    s, r = req("POST", "/wp-json/" + NS + "/v1/run", body={"token": TOKEN, "reset": RESET, "pts": [[a, b, RADIUS] for a, b in PTS]}, timeout=180)
    print("[run]", s, json.dumps(r, ensure_ascii=False))
finally:
    snip("PUT", "/%s/deactivate" % BR, {})
    s, _ = snip("DELETE", "/%s" % BR, None)
    time.sleep(1.5)
    s2, _ = req("POST", "/wp-json/" + NS + "/v1/run", body={"token": TOKEN})
    print("[bridge] delete http %s; route now http %s (want 404)" % (s, s2))
