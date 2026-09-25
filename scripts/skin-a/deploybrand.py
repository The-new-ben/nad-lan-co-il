# -*- coding: utf-8 -*-
"""Brand kit deploy (owner: "logo, favicon, everything has to comply", 2.9.2026).
1. upload site-icon-512.png + og-default-1200x630.jpg via media REST (alt text set)
2. bridge: site_icon option -> new attachment; Yoast org logo + default OG image; physical /favicon.ico; plugin favicon.svg (with .bak)
3. purge, verify: /favicon.ico 200 image, <link rel=icon> points to new files, og:image default on a page without its own image.
Reads: wpseo_titles.company_logo(_id), wpseo_social.og_default_image(_id) before/after (printed, not secret)."""
import base64, ctypes, ctypes.wintypes, hashlib, io, json, os, re, secrets, sys, time, urllib.request, urllib.error
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = "https://nad-lan.co.il"
OUT = r"C:\Users\777\nad-lan\nad-lan-co-il\assets\skin-a\brand\out"
SECRETS_PATH = r"C:\Users\777\Documents\websites\.codex-secrets\wordpress-app-passwords\nad-lan.co.il.json"
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
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) NadLan-Brand/1.0"
def req(method, path, body=None, ctype="application/json", extra=None, timeout=180, raw=False, auth=True):
    data = None
    if body is not None: data = body if isinstance(body, (bytes, bytearray)) else json.dumps(body, ensure_ascii=False).encode()
    r = urllib.request.Request(BASE + path, data=data, method=method)
    if auth: r.add_header("Authorization", AUTH)
    r.add_header("User-Agent", UA)
    if body is not None: r.add_header("Content-Type", ctype)
    for k, v in (extra or {}).items(): r.add_header(k, v)
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

# 1. media uploads
def upload(name, mime, alt):
    blob = open(os.path.join(OUT, name), "rb").read()
    s, m, _ = req("POST", "/wp-json/wp/v2/media", body=blob, ctype=mime, extra={"Content-Disposition": f'attachment; filename="{name}"'}, timeout=180)
    must(s, m, "upload " + name)
    req("POST", f"/wp-json/wp/v2/media/{m['id']}", body={"alt_text": alt, "title": alt})
    print("media", name, "->", m["id"], m["source_url"]); return m["id"], m["source_url"]
icon_id, icon_url = upload("site-icon-512.png", "image/png", "נדלן: סימן המותג")
og_id, og_url = upload("og-default-1200x630.jpg", "image/jpeg", "נדלן: פרויקטים חדשים, דירות למכירה ומחירי דירות")

# 2. bridge
TOKEN = secrets.token_hex(24)
BRIDGE = r'''
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-brand-ops/v1', '/apply', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( isset( $b['token'] ) ? $b['token'] : '' ) ) ) { return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) ); }
			$out = array();
			$t = (array) get_option( 'wpseo_titles', array() ); $so = (array) get_option( 'wpseo_social', array() );
			$out['before'] = array( 'site_icon' => get_option( 'site_icon' ), 'company_logo' => $t['company_logo'] ?? null, 'company_logo_id' => $t['company_logo_id'] ?? null, 'company_name' => $t['company_name'] ?? null, 'og_default_image' => $so['og_default_image'] ?? null, 'og_default_image_id' => $so['og_default_image_id'] ?? null );
			if ( ! empty( $b['apply'] ) ) {
				update_option( 'site_icon', (int) $b['icon_id'] );
				$t['company_logo'] = (string) $b['icon_url']; $t['company_logo_id'] = (int) $b['icon_id']; update_option( 'wpseo_titles', $t );
				$so['og_default_image'] = (string) $b['og_url']; $so['og_default_image_id'] = (int) $b['og_id']; update_option( 'wpseo_social', $so );
				$ico = base64_decode( (string) $b['ico_b64'], true ); $svg = base64_decode( (string) $b['svg_b64'], true );
				if ( $ico ) { $p = ABSPATH . 'favicon.ico'; if ( file_exists( $p ) ) { copy( $p, $p . '.bak' . time() ); } file_put_contents( $p, $ico ); $out['ico'] = array( 'bytes' => filesize( $p ), 'md5' => md5_file( $p ) ); }
				if ( $svg ) { $p = WP_PLUGIN_DIR . '/nadlan-config/assets/branding/favicon.svg'; if ( file_exists( $p ) ) { copy( $p, $p . '.bak' . time() ); } file_put_contents( $p, $svg ); $out['svg'] = array( 'bytes' => filesize( $p ), 'md5' => md5_file( $p ) ); }
				$t2 = (array) get_option( 'wpseo_titles', array() ); $so2 = (array) get_option( 'wpseo_social', array() );
				$out['after'] = array( 'site_icon' => get_option( 'site_icon' ), 'company_logo' => $t2['company_logo'] ?? null, 'og_default_image' => $so2['og_default_image'] ?? null );
				do_action( 'litespeed_purge_all' ); $out['purged'] = 1;
			}
			return $out;
		},
	) );
} );
'''.replace("__TOKEN__", TOKEN)
s, c = snip("POST", "", {"name": f"tmp-brand-ops-{int(time.time())}", "code": "/* placeholder */", "scope": "global", "active": False}); must(s, c, "bridge create"); BR = c["id"]
try:
    s, u = snip("PUT", f"/{BR}", {"name": c["name"], "code": BRIDGE, "scope": "global", "active": False}); must(s, u, "bridge update")
    s, a = snip("PUT", f"/{BR}/activate", {}); must(s, a, "bridge activate")
    s, before, _ = req("POST", "/wp-json/nadlan-brand-ops/v1/apply", {"token": TOKEN}); must(s, before, "read before")
    print("BEFORE", json.dumps(before["before"], ensure_ascii=False))
    ico = open(os.path.join(OUT, "favicon.ico"), "rb").read(); svg = open(os.path.join(OUT, "favicon.svg"), "rb").read()
    s, r, _ = req("POST", "/wp-json/nadlan-brand-ops/v1/apply", {"token": TOKEN, "apply": 1, "icon_id": icon_id, "icon_url": icon_url, "og_id": og_id, "og_url": og_url, "ico_b64": base64.b64encode(ico).decode(), "svg_b64": base64.b64encode(svg).decode()}, timeout=240)
    must(s, r, "apply")
    print("AFTER ", json.dumps(r.get("after"), ensure_ascii=False)); print("ico", r.get("ico"), "local md5", hashlib.md5(ico).hexdigest()); print("svg", r.get("svg"), "local md5", hashlib.md5(svg).hexdigest())
finally:
    s1, _ = snip("PUT", f"/{BR}/deactivate", {}); s2, _ = snip("DELETE", f"/{BR}", None); print("bridge cleanup", s1, s2)

time.sleep(4)
s, body, hdrs = req("GET", "/favicon.ico?v=" + str(int(time.time())), raw=True, auth=False, extra={"User-Agent": "Mozilla/5.0 Chrome/128"})
print("/favicon.ico", s, hdrs.get("Content-Type"), len(body) if isinstance(body, (bytes, bytearray)) else body)
s, body, _ = req("GET", "/?b=" + str(int(time.time())), raw=True, auth=False, extra={"User-Agent": "Mozilla/5.0 Chrome/128"})
txt = body.decode("utf-8", "replace") if isinstance(body, (bytes, bytearray)) else ""
print("icon links:", re.findall(r'<link[^>]*rel="[^"]*icon[^"]*"[^>]*href="([^"]+)"', txt)[:5])
print("og:image home:", re.findall(r'<meta property="og:image" content="([^"]+)"', txt)[:2])
