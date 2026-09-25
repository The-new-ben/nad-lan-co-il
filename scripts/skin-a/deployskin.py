# -*- coding: utf-8 -*-
"""Skin A deploy runner (owner GO 2.9.2026). Steps:
1. upload skin-a.css + hero photo (+ LICENSE) to uploads/nadlan-skin/ via a temporary snippet bridge (md5 verified, .bak kept)
2. create or update the PERSISTENT snippet x-skin-a with plugins/nadlan-config/inc/skin-a.php (PHP lint on the server first), activate
3. bump option nadlan_skin_a_ver, purge LiteSpeed
4. verify: GET /?skin=a carries body class nl-skin-a + skin-a.css; plain GET does NOT; health ok
Usage: python deployskin.py [--css-only]"""
import base64, ctypes, ctypes.wintypes, hashlib, io, json, os, secrets, sys, time, urllib.request, urllib.error, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = "https://nad-lan.co.il"
REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
CANVAS = r"C:\Users\777\AppData\Local\Temp\claude\C--Users-777-nad-lan\d91551f7-f7b5-45bf-8a87-c3c8d5bde04f\scratchpad\canvas"
SECRETS_PATH = r"C:\Users\777\Documents\websites\.codex-secrets\wordpress-app-passwords\nad-lan.co.il.json"
CSS_ONLY = "--css-only" in sys.argv
FLIP = "all" if "--flip-all" in sys.argv else ("" if "--flip-off" in sys.argv else None)  # owner-word only: skin for everyone / back to preview

class DATA_BLOB(ctypes.Structure):
    _fields_ = [("cbData", ctypes.wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]
def dpapi_unprotect(b64):
    raw = base64.b64decode(b64)
    bi = DATA_BLOB(len(raw), ctypes.cast(ctypes.create_string_buffer(raw, len(raw)), ctypes.POINTER(ctypes.c_char))); bo = DATA_BLOB()
    if not ctypes.windll.crypt32.CryptUnprotectData(ctypes.byref(bi), None, None, None, None, 0, ctypes.byref(bo)): raise RuntimeError("DPAPI")
    try: return ctypes.string_at(bo.pbData, bo.cbData).decode("utf-8")
    finally: ctypes.windll.kernel32.LocalFree(bo.pbData)
with open(SECRETS_PATH, encoding="utf-8-sig") as f: sec = json.load(f)
AUTH = "Basic " + base64.b64encode(f"{sec['username']}:{dpapi_unprotect(sec['password_dpapi'])}".encode()).decode()
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) NadLan-Skin/1.0"

def req(method, path, body=None, timeout=180, raw=False, auth=True, headers=None):
    r = urllib.request.Request(BASE + path, data=(json.dumps(body, ensure_ascii=False).encode() if body is not None else None), method=method)
    if auth: r.add_header("Authorization", AUTH)
    r.add_header("User-Agent", UA)
    if body is not None: r.add_header("Content-Type", "application/json")
    for k, v in (headers or {}).items(): r.add_header(k, v)
    try:
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            p = resp.read(); return resp.status, (p if raw else json.loads(p.decode() or "null")), dict(resp.headers)
    except urllib.error.HTTPError as e:
        p = e.read()
        try: return e.code, json.loads(p.decode()), dict(e.headers)
        except Exception: return e.code, {"raw": p[:300].decode("utf-8", "replace")}, dict(e.headers)
def must(s, p, what, ok=(200, 201)):
    if s not in ok: raise SystemExit(f"FATAL {what}: HTTP {s}: {json.dumps(p, ensure_ascii=False)[:400]}")
    return p
def snip(method, path, body=None): return req(method, "/wp-json/code-snippets/v1/snippets" + path, body)[:2]

s, h, _ = req("GET", "/wp-json/nadlan/v1/health"); must(s, h, "health"); print("health", h["version"], h["status"])

# ---- 1. bridge: files + option + lint + purge ----
TOKEN = secrets.token_hex(24)
BRIDGE = r'''
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-skin-ops/v1', '/apply', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( isset( $b['token'] ) ? $b['token'] : '' ) ) ) { return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) ); }
			$out = array();
			if ( ! empty( $b['lint'] ) ) {
				try { token_get_all( "<?php\n" . (string) $b['lint'], TOKEN_PARSE ); $out['lint'] = 'ok'; }
				catch ( ParseError $e ) { return new WP_Error( 'lint', $e->getMessage() . ' line ' . $e->getLine(), array( 'status' => 400 ) ); }
			}
			if ( ! empty( $b['files'] ) && is_array( $b['files'] ) ) {
				$up = wp_get_upload_dir(); $dir = trailingslashit( $up['basedir'] ) . 'nadlan-skin';
				if ( ! wp_mkdir_p( $dir ) ) { return new WP_Error( 'mkdir', 'no dir', array( 'status' => 500 ) ); }
				foreach ( $b['files'] as $f ) {
					$name = sanitize_file_name( (string) $f['name'] ); $data = base64_decode( (string) $f['b64'], true );
					if ( false === $data ) { return new WP_Error( 'b64', $name, array( 'status' => 400 ) ); }
					$path = $dir . '/' . $name;
					if ( file_exists( $path ) ) { copy( $path, $path . '.bak' . time() ); }
					file_put_contents( $path, $data );
					$out['files'][ $name ] = array( 'url' => trailingslashit( $up['baseurl'] ) . 'nadlan-skin/' . $name, 'md5' => md5_file( $path ), 'bytes' => filesize( $path ) );
				}
			}
			if ( ! empty( $b['options'] ) && is_array( $b['options'] ) ) {
				foreach ( $b['options'] as $k => $v ) { $k = sanitize_key( $k ); if ( 0 === strpos( $k, 'nadlan_skin_a' ) ) { update_option( $k, sanitize_text_field( (string) $v ), false ); $out['options'][ $k ] = (string) $v; } }
			}
			if ( ! empty( $b['purge'] ) ) { do_action( 'litespeed_purge_all' ); $out['purged'] = 1; }
			return $out;
		},
	) );
} );
'''.replace("__TOKEN__", TOKEN)
s, c = snip("POST", "", {"name": f"tmp-skin-ops-{int(time.time())}", "code": "/* placeholder */", "scope": "global", "active": False}); must(s, c, "bridge create")
BR = c["id"]
try:
    s, u = snip("PUT", f"/{BR}", {"name": c["name"], "code": BRIDGE, "scope": "global", "active": False}); must(s, u, "bridge update")
    s, a = snip("PUT", f"/{BR}/activate", {}); must(s, a, "bridge activate")
    def ops(payload, what):
        payload["token"] = TOKEN
        s, r, _ = req("POST", "/wp-json/nadlan-skin-ops/v1/apply", payload, timeout=240); must(s, r, what); return r

    css = open(os.path.join(REPO, "assets", "skin-a", "skin-a.css"), "rb").read()
    files = [{"name": "skin-a.css", "b64": base64.b64encode(css).decode()}]
    hero = os.path.join(CANVAS, "hero-tel-aviv-coast.jpg")
    if os.path.exists(hero):
        files.append({"name": "hero-tel-aviv-coast.jpg", "b64": base64.b64encode(open(hero, "rb").read()).decode()})
        files.append({"name": "LICENSE-hero-tel-aviv-coast.txt", "b64": base64.b64encode(("Unsplash photo lpQwaLWhw9Q (https://unsplash.com/photos/lpQwaLWhw9Q), Unsplash License: free for commercial use, no permission needed. Downloaded 2026-09-02. Caption on site: צילום אווירה.\n").encode()).decode()})
    r = ops({"files": files}, "files")
    for n, info in r["files"].items():
        local = hashlib.md5(css if n == "skin-a.css" else open(os.path.join(CANVAS, n), "rb").read()).hexdigest() if n != "LICENSE-hero-tel-aviv-coast.txt" else info["md5"]
        print("file", n, info["bytes"], "bytes", "MATCH" if info["md5"] == local else "MISMATCH " + local)
    ver = str(int(time.time()))
    ops({"options": {"nadlan_skin_a_ver": ver}}, "ver")
    if FLIP is not None:
        r = ops({"options": {"nadlan_skin_a": FLIP}}, "flip"); print("FLIP nadlan_skin_a =", repr(FLIP), "->", r.get("options"))
    print("css version", ver)

    if not CSS_ONLY:
        php = open(os.path.join(REPO, "plugins", "nadlan-config", "inc", "skin-a.php"), encoding="utf-8").read()
        code = re.sub(r'^\s*<\?php\s*', '', php, count=1)
        ops({"lint": code}, "lint")
        print("lint ok on server")
        s, lst = snip("GET", ""); must(s, lst, "list")
        existing = [x for x in lst if x["name"] == "x-skin-a"]
        if existing:
            sid = existing[0]["id"]
            s, u2 = snip("PUT", f"/{sid}", {"name": "x-skin-a", "code": code, "scope": "global", "active": False}); must(s, u2, "x-skin-a update")
        else:
            s, c2 = snip("POST", "", {"name": "x-skin-a", "code": code, "scope": "global", "active": False}); must(s, c2, "x-skin-a create"); sid = c2["id"]
        s, a2 = snip("PUT", f"/{sid}/activate", {}); must(s, a2, "x-skin-a activate")
        print("x-skin-a snippet id", sid, "sha256", hashlib.sha256(code.encode()).hexdigest()[:16], "ACTIVE")
    ops({"purge": 1}, "purge")
finally:
    s1, _ = snip("PUT", f"/{BR}/deactivate", {}); s2, _ = snip("DELETE", f"/{BR}", None); print("bridge cleanup", s1, s2)

# ---- verify ----
time.sleep(4)
PUBLIC_SKIN = (FLIP == "all") if FLIP is not None else True  # since 3.9.2026 the skin is on for everyone (owner order); --flip-off returns to preview-only
for path, expect in (("/?skin=a&nocache=" + str(int(time.time())), True), ("/?nl=" + str(int(time.time())), PUBLIC_SKIN), ("/en/?nl=" + str(int(time.time())), PUBLIC_SKIN), ("/projects/rainbow-tel-aviv/?nl=" + str(int(time.time())), PUBLIC_SKIN)):
    s, body, hdrs = req("GET", path, raw=True, auth=False, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/128 Safari/537.36"})
    txt = body.decode("utf-8", "replace") if isinstance(body, (bytes, bytearray)) else json.dumps(body)
    has_class = "nl-skin-a" in re.search(r"<body[^>]*>", txt).group(0) if re.search(r"<body[^>]*>", txt) else False
    has_css = "nadlan-skin/skin-a.css" in txt
    has_hero = "nlsa-hero" in txt
    print(path[:24], "HTTP", s, "| body class:", has_class, "| css:", has_css, "| new hero:", has_hero, "| X-NL-Skin:", hdrs.get("X-NL-Skin"), "| expected skin:", expect, "=>", "OK" if (has_class == expect and has_css == expect) else "PROBLEM")
s, h, _ = req("GET", "/wp-json/nadlan/v1/health"); print("health after", h.get("version"), h.get("status"))
