# -*- coding: utf-8 -*-
"""T1 release: plates render full-frame sitewide (catalog + homepage flagship cards),
capsule plates become the featured images of Bnei Dan (6693) and Stricker (6694).
Live-byte patching via a temporary Code Snippets ops bridge; .bakT1 siblings; md5
verified; server-side lint; version bump 1.72.220 -> 1.72.221."""
import base64, ctypes, ctypes.wintypes, hashlib, io, json, os, re, secrets, sys, time, urllib.request, urllib.error

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = "https://nad-lan.co.il"
HERE = os.path.dirname(os.path.abspath(__file__))
SECRETS_PATH = r"C:\Users\777\Documents\websites\.codex-secrets\wordpress-app-passwords\nad-lan.co.il.json"

class DATA_BLOB(ctypes.Structure):
    _fields_ = [("cbData", ctypes.wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]

def dpapi(b64):
    raw = base64.b64decode(b64)
    bi = DATA_BLOB(len(raw), ctypes.cast(ctypes.create_string_buffer(raw, len(raw)), ctypes.POINTER(ctypes.c_char)))
    bo = DATA_BLOB()
    if not ctypes.windll.crypt32.CryptUnprotectData(ctypes.byref(bi), None, None, None, None, 0, ctypes.byref(bo)):
        raise RuntimeError("dpapi")
    try:
        return ctypes.string_at(bo.pbData, bo.cbData).decode("utf-8")
    finally:
        ctypes.windll.kernel32.LocalFree(bo.pbData)

sec = json.load(open(SECRETS_PATH, encoding="utf-8-sig"))
AUTH = "Basic " + base64.b64encode(f"{sec['username']}:{dpapi(sec['password_dpapi'])}".encode()).decode()

def req(method, path, body=None, ctype="application/json", extra=None, timeout=120, raw=False):
    r = urllib.request.Request(BASE + path, data=None if body is None else (body if isinstance(body, (bytes, bytearray)) else json.dumps(body, ensure_ascii=False).encode()), method=method)
    r.add_header("Authorization", AUTH)
    r.add_header("User-Agent", "NadLan-T1/1.0")
    if body is not None:
        r.add_header("Content-Type", ctype)
    for k, v in (extra or {}).items():
        r.add_header(k, v)
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
        raise SystemExit(f"FATAL {what}: HTTP {s}: {json.dumps(p, ensure_ascii=False)[:400]}")
    return p

s, h = req("GET", "/wp-json/nadlan/v1/health")
must(s, h, "health")
print("[health]", h.get("version"), h.get("status"))
assert h.get("version") == "1.72.220" and h.get("status") == "ok"

# ---- ops bridge ----
TOKEN = secrets.token_hex(24)
BRIDGE = r'''
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-t1-ops/v1', '/apply', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( isset( $b['token'] ) ? $b['token'] : '' ) ) ) {
				return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) );
			}
			$root = WP_PLUGIN_DIR . '/nadlan-config/';
			$safe = function ( $rel ) use ( $root ) {
				$rel = str_replace( array( '..', "\0" ), '', (string) $rel );
				return $root . ltrim( $rel, '/' );
			};
			$out = array();
			if ( ! empty( $b['get'] ) ) {
				$p = $safe( $b['get'] );
				if ( ! is_readable( $p ) ) { return new WP_Error( 'missing', $b['get'], array( 'status' => 404 ) ); }
				$data = file_get_contents( $p );
				$out['get'] = array( 'b64' => base64_encode( $data ), 'md5' => md5( $data ), 'bytes' => strlen( $data ) );
			}
			if ( ! empty( $b['put'] ) && is_array( $b['put'] ) ) {
				$p = $safe( $b['put']['rel'] );
				$data = base64_decode( (string) $b['put']['b64'], true );
				if ( false === $data ) { return new WP_Error( 'b64', 'bad', array( 'status' => 400 ) ); }
				if ( md5( $data ) !== strtolower( (string) $b['put']['md5'] ) ) { return new WP_Error( 'md5', 'mismatch', array( 'status' => 400 ) ); }
				if ( substr( $p, -4 ) === '.php' ) {
					try { token_get_all( $data, TOKEN_PARSE ); } catch ( ParseError $e ) { return new WP_Error( 'lint', $e->getMessage(), array( 'status' => 400 ) ); }
				}
				if ( file_exists( $p ) && ! file_exists( $p . '.bakT1' ) ) { copy( $p, $p . '.bakT1' ); }
				$w = file_put_contents( $p, $data );
				if ( false === $w ) { return new WP_Error( 'write', $p, array( 'status' => 500 ) ); }
				$out['put'] = array( 'rel' => $b['put']['rel'], 'bytes' => $w, 'md5' => md5_file( $p ), 'bak' => file_exists( $p . '.bakT1' ) );
			}
			if ( ! empty( $b['purge'] ) ) { do_action( 'litespeed_purge_all' ); $out['purged'] = 1; }
			return $out;
		},
	) );
} );
'''.replace("__TOKEN__", TOKEN)

def snip(method, path, body=None):
    return req(method, f"/wp-json/code-snippets/v1/snippets{path}", body=body)

s, created = snip("POST", "", {"name": f"tmp-t1-ops-{int(time.time())}", "code": "/* placeholder */", "scope": "global", "active": False})
must(s, created, "bridge create")
BR = created["id"]
must(*snip("PUT", f"/{BR}", {"name": created["name"], "code": BRIDGE, "scope": "global", "active": False}), "bridge code")
must(*snip("PUT", f"/{BR}/activate", {}), "bridge activate")
print("[bridge]", BR)

def ops(payload, what):
    payload["token"] = TOKEN
    s, r = req("POST", "/wp-json/nadlan-t1-ops/v1/apply", body=payload, timeout=180)
    must(s, r, what)
    return r

def patch_file(rel, edits, expect_min=1):
    r = ops({"get": rel}, f"get {rel}")
    data = base64.b64decode(r["get"]["b64"])
    text = data.decode("utf-8")
    orig_md5 = r["get"]["md5"]
    applied = []
    for old, new, required in edits:
        n = text.count(old)
        if n == 0:
            if required:
                raise SystemExit(f"FATAL anchor missing in live {rel}: {old[:80]!r}")
            applied.append((old[:50], 0))
            continue
        text = text.replace(old, new)
        applied.append((old[:50], n))
    out = text.encode("utf-8")
    w = ops({"put": {"rel": rel, "b64": base64.b64encode(out).decode(), "md5": hashlib.md5(out).hexdigest()}}, f"put {rel}")
    print(f"[patch] {rel}: live-md5 {orig_md5[:8]} -> {w['put']['md5'][:8]}, bak={w['put']['bak']}, edits={applied}")

CSS_CAT = "\n/* T1 27.8.2026 (owner order): plates render in full - the capsule row is never cropped */\n.nldc-project .nldc-media.has-real-photo{background:#EFEAE0}\n.nldc-project .nldc-media.has-real-photo img{object-fit:contain}\n"
CSS_HOME = "\n/* T1 27.8.2026 (owner order): flagship plates full-frame 4:3, no crop */\n.nlhv2-shcard-media.nlhv2-shcard-media{aspect-ratio:4/3;background:#EFEAE0}\n.nlhv2-shcard-media.nlhv2-shcard-media img{object-fit:contain}\n"

patch_file("inc/directory-assets.php", [(
    ".nldc-project:hover .nldc-media img{transform:scale(1.03)}",
    ".nldc-project:hover .nldc-media img{transform:scale(1.03)}" + CSS_CAT, True)])
patch_file("inc/directory.php", [(
    "get_the_post_thumbnail_url( $id, 'medium_large' )",
    "get_the_post_thumbnail_url( $id, 'large' )", True)])
patch_file("inc/home-v2.php", [(
    ".nlhv2-shcard-media img{width:100%;height:100%;object-fit:cover;display:block}",
    ".nlhv2-shcard-media img{width:100%;height:100%;object-fit:cover;display:block}" + CSS_HOME, True)])
patch_file("nadlan-config.php", [
    (" * Version: 1.72.220", " * Version: 1.72.221", True),
    ("define( 'NADLAN_CONFIG_VERSION', '1.72.220' )", "define( 'NADLAN_CONFIG_VERSION', '1.72.221' )", True),
])

# ---- capsule plates become featured images ----
PLATES = [
    ("plate-1-stricker.jpg", "bnei-dan-54-56-plate-capsules.jpg", "בני דן 54-56 תל אביב — הדמיה להמחשה בסגנון רישום אדריכלי עם נקודות המכירה", 6693),
    ("plate-0-unknown.jpg", "stricker-13-brandeis-14-plate-capsules.jpg", "שטריקר 13 · ברנדיס 14 תל אביב — הדמיה להמחשה בסגנון רישום אדריכלי עם נקודות המכירה", 6694),
]
for local, name, alt, post_id in PLATES:
    blob = open(os.path.join(HERE, local), "rb").read()
    s, m = req("POST", "/wp-json/wp/v2/media", body=blob, ctype="image/jpeg",
               extra={"Content-Disposition": f'attachment; filename="{name}"'}, timeout=180)
    must(s, m, f"media {name}")
    req("POST", f"/wp-json/wp/v2/media/{m['id']}", body={"alt_text": alt, "title": alt})
    s2, p2 = req("POST", f"/wp-json/wp/v2/nadlan_project/{post_id}", body={"featured_media": m["id"]})
    must(s2, p2, f"featured {post_id}")
    print(f"[plate] {name} -> media {m['id']} ({m['source_url']}) featured on {post_id}")

ops({"purge": 1}, "purge")
s, d = snip("DELETE", f"/{BR}", None)
print("[bridge-delete]", s)

time.sleep(3)
s, h2 = req("GET", "/wp-json/nadlan/v1/health")
print("[health-after]", h2.get("version"), h2.get("status"))
assert h2.get("version") == "1.72.221" and h2.get("status") == "ok", "VERSION/HEALTH FAIL"
s, cat = req("GET", "/projects/", raw=True)
cat_html = cat.decode("utf-8", "replace")
print("[catalog]", s, "contain-rule:", "has-real-photo img{object-fit:contain" in cat_html)
s, home = req("GET", "/", raw=True)
home_html = home.decode("utf-8", "replace")
print("[home]", s, "contain-rule:", ".nlhv2-shcard-media.nlhv2-shcard-media img{object-fit:contain" in home_html)
for probe in ("/projects/rainbow-tel-aviv/", "/projects/h-infinity-somail-tel-aviv/", "/projects/aurelia/"):
    s3, b3 = req("GET", probe, raw=True)
    print("[spot]", probe, s3, len(b3))
print("T1 DONE")
