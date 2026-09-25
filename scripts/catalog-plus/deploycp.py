# -*- coding: utf-8 -*-
"""Catalog-plus deploy (owner GO 6.9.2026): uploads deals-context-v1.json to uploads/nadlan-skin/ and installs the persistent
snippet x-catalog-plus from plugins/nadlan-config/inc/catalog-plus.php (server-side PHP lint first). Purges LiteSpeed and verifies
that /projects/ carries the enriched cards, the search bar, the body copy and the ItemList schema.
Usage: python deploycp.py [--data-only] [--snippet-only] [--off]   (--off deactivates the snippet = rollback)"""
import base64, ctypes, ctypes.wintypes, hashlib, io, json, os, re, secrets, sys, time, urllib.request, urllib.error
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = "https://nad-lan.co.il"
REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
DATA = os.path.join(REPO, "tools", "deals", "deals-context-v1.json")
SECRETS_PATH = r"C:\Users\777\Documents\websites\.codex-secrets\wordpress-app-passwords\nad-lan.co.il.json"
DATA_ONLY = "--data-only" in sys.argv; SNIPPET_ONLY = "--snippet-only" in sys.argv; OFF = "--off" in sys.argv
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
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) NadLan-CatalogPlus/1.0"
def req(method, path, body=None, timeout=180, raw=False, auth=True, headers=None):
    data = None if body is None else json.dumps(body, ensure_ascii=False).encode()
    r = urllib.request.Request(BASE + path, data=data, method=method)
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
    if s not in ok: raise SystemExit(f"FATAL {what}: HTTP {s}: {json.dumps(p, ensure_ascii=False)[:500]}")
    return p
def snip(method, path, body=None): return req(method, "/wp-json/code-snippets/v1/snippets" + path, body)[:2]

s, h, _ = req("GET", "/wp-json/nadlan/v1/health"); must(s, h, "health"); print("health", h["version"], h["status"])

if OFF:
    s, lst = snip("GET", ""); must(s, lst, "list")
    for x in lst:
        if x["name"] == "x-catalog-plus":
            s2, _ = snip("PUT", f"/{x['id']}/deactivate", {}); print("x-catalog-plus deactivated", s2)
    req("POST", "/wp-json/nadlan-skin-ops/v1/apply", {"purge": 1})
    raise SystemExit(0)

TOKEN = secrets.token_hex(24)
BRIDGE = r'''
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-cp-ops/v1', '/apply', array(
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
					$out['files'][ $name ] = array( 'md5' => md5_file( $path ), 'bytes' => filesize( $path ) );
				}
				delete_transient( 'nadlan_cp_deals_v1' );
			}
			if ( ! empty( $b['purge'] ) ) { do_action( 'litespeed_purge_all' ); delete_transient( 'nadlan_cp_deals_v1' ); $out['purged'] = 1; }
			return $out;
		},
	) );
} );
'''.replace("__TOKEN__", TOKEN)
s, c = snip("POST", "", {"name": f"tmp-cp-ops-{int(time.time())}", "code": "/* placeholder */", "scope": "global", "active": False}); must(s, c, "bridge create"); BR = c["id"]
try:
    s, u = snip("PUT", f"/{BR}", {"name": c["name"], "code": BRIDGE, "scope": "global", "active": False}); must(s, u, "bridge update")
    s, a = snip("PUT", f"/{BR}/activate", {}); must(s, a, "bridge activate")
    def ops(payload, what):
        payload["token"] = TOKEN
        s, r, _ = req("POST", "/wp-json/nadlan-cp-ops/v1/apply", payload, timeout=240); must(s, r, what); return r
    if not SNIPPET_ONLY:
        files = []
        for name in ("deals-context-v1.json", "tlv-neighborhoods-psqm.geojson", "project-surroundings-v1.json"):
            fp = os.path.join(REPO, "tools", "deals", name)
            if os.path.exists(fp): files.append({"name": name, "b64": base64.b64encode(open(fp, "rb").read()).decode()})
        r = ops({"files": files}, "data")
        for name, info in r["files"].items():
            local = hashlib.md5(open(os.path.join(REPO, "tools", "deals", name), "rb").read()).hexdigest()
            print(name, info["bytes"], "bytes", "MATCH" if info["md5"] == local else "MISMATCH")
        ops({"purge": 1}, "purge-data")
    if not DATA_ONLY:
        php = open(os.path.join(REPO, "plugins", "nadlan-config", "inc", "catalog-plus.php"), encoding="utf-8").read()
        php2 = open(os.path.join(REPO, "plugins", "nadlan-config", "inc", "catalog-plus-map.php"), encoding="utf-8").read()
        code = re.sub(r'^\s*<\?php\s*', '', php, count=1) + "\n" + re.sub(r'^\s*<\?php\s*', '', php2, count=1)
        ops({"lint": code}, "lint"); print("lint ok on server")
        s, lst = snip("GET", ""); must(s, lst, "list")
        existing = [x for x in lst if x["name"] == "x-catalog-plus"]
        if existing:
            sid = existing[0]["id"]
            s, u2 = snip("PUT", f"/{sid}", {"name": "x-catalog-plus", "code": code, "scope": "global", "active": False}); must(s, u2, "x-catalog-plus update")
        else:
            s, c2 = snip("POST", "", {"name": "x-catalog-plus", "code": code, "scope": "global", "active": False}); must(s, c2, "x-catalog-plus create"); sid = c2["id"]
        s, a2 = snip("PUT", f"/{sid}/activate", {}); must(s, a2, "x-catalog-plus activate")
        print("x-catalog-plus snippet id", sid, "sha256", hashlib.sha256(code.encode()).hexdigest()[:16], "ACTIVE")
    ops({"purge": 1}, "purge")
finally:
    s1, _ = snip("PUT", f"/{BR}/deactivate", {}); s2, _ = snip("DELETE", f"/{BR}", None); print("bridge cleanup", s1, s2)

# ---- verify ----
time.sleep(5)
s, body, hdrs = req("GET", "/projects/?cp=" + str(int(time.time())), raw=True, auth=False, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/128 Safari/537.36"}, timeout=240)
txt = body.decode("utf-8", "replace") if isinstance(body, (bytes, bytearray)) else ""
checks = {"http": s, "bytes": len(txt), "cards_enriched": txt.count('class="nlcp-card"'), "ctx_lines": txt.count('class="nlcp-ctx"'), "more": txt.count('class="nlcp-more"'),
          "searchbar": 'id="nlcp-bar"' in txt, "body_copy": 'class="nlcp-body"' in txt, "pricemap": 'nlcp-pricemap' in txt, "drone_in_sidebar": ('nlcp-mapcard' in txt),
          "itemlist_schema": '"ItemList"' in txt, "mapthumb": 'id="nlcp-mapthumb"' in txt, "mapshell": 'id="nlcp-map"' in txt, "drone_removed": ('nldrone--toggle' not in txt), "faq_schema": '"FAQPage"' in txt, "rest_plus": 'projects-plus' in txt, "h2": len(re.findall(r"<h2", txt)), "php_notice": ("Warning:" in txt or "Fatal error" in txt or "Notice:" in txt)}
print("verify /projects/:", json.dumps(checks, ensure_ascii=False))
s, r, _ = req("GET", "/wp-json/nadlan/v1/projects-plus?city=%D7%AA%D7%9C%20%D7%90%D7%91%D7%99%D7%91&status=construction&per_page=6", auth=False)
print("REST projects-plus:", s, {k: (v if k != "html" else len(v)) for k, v in (r.items() if isinstance(r, dict) else [])} if isinstance(r, dict) else r)
s, h, _ = req("GET", "/wp-json/nadlan/v1/health"); print("health after", h.get("version"), h.get("status"), "| catalog_plus:", (h.get("catalog_plus") if isinstance(h, dict) else None))
