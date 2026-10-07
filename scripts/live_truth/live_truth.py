# -*- coding: utf-8 -*-
"""READ-ONLY: export the LIVE nadlan-config plugin folder and the Code Snippets of https://nad-lan.co.il, as the source of the
`live-truth` branch (CEO decision on HAD-443, 7.10.2026; Ben 7.10: "consult with the CEO and start doing things").
Writes nothing on the site except one temporary admin-only bridge snippet, always deactivated and deleted (route then 404).
The app password is decrypted in-process (DPAPI, via the deployskin helpers) and never printed.

  python scripts/live_truth/live_truth.py <out_dir>

Out:
  <out>/plugins/nadlan-config/...   every live file (byte-exact, md5-checked)
  <out>/snippets/<id>-<slug>.php    every snippet's code (active and inactive), plus snippets.json (id, name, active, scope, md5)
  <out>/LIVE-MANIFEST.json          the live listing: path, bytes, md5; the plugin version; the read time
Never run while another runner's bridge is up (the release lock in docs/coordination/claude-codex.md)."""
import base64
import hashlib
import io
import json
import os
import re
import secrets
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
OUT = sys.argv[1] if len(sys.argv) > 1 else None
if not OUT:
    raise SystemExit("usage: live_truth.py <out_dir>")
_src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
_ns = {"__name__": "live_truth_helpers"}
exec(compile(_src[:_src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), _ns)
req, must, snip = _ns["req"], _ns["must"], _ns["snip"]
TOKEN = secrets.token_hex(24)
NS = "nadlan-live-truth-" + TOKEN[:8]
BRIDGE = r'''
add_action( 'rest_api_init', function () {
	$ok = function ( $req ) {
		$b = $req->get_json_params();
		return is_array( $b ) && hash_equals( '__TOKEN__', (string) ( isset( $b['token'] ) ? $b['token'] : '' ) );
	};
	register_rest_route( '__NS__/v1', '/list', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) use ( $ok ) {
			if ( ! $ok( $req ) ) { return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) ); }
			$root = realpath( WP_PLUGIN_DIR . '/nadlan-config' );
			$out = array();
			$it = new RecursiveIteratorIterator( new RecursiveDirectoryIterator( $root, FilesystemIterator::SKIP_DOTS ) );
			foreach ( $it as $f ) {
				if ( ! $f->isFile() ) { continue; }
				$rel = str_replace( DIRECTORY_SEPARATOR, '/', substr( $f->getPathname(), strlen( $root ) + 1 ) );
				$out[] = array( $rel, $f->getSize(), md5_file( $f->getPathname() ) );
			}
			$v = get_file_data( $root . '/nadlan-config.php', array( 'v' => 'Version' ) );
			return array( 'files' => $out, 'version' => $v['v'] );
		},
	) );
	register_rest_route( '__NS__/v1', '/get', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) use ( $ok ) {
			if ( ! $ok( $req ) ) { return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) ); }
			$root = realpath( WP_PLUGIN_DIR . '/nadlan-config' );
			$out = array();
			foreach ( (array) $req->get_json_params()['rels'] as $rel ) {
				$path = realpath( $root . '/' . ltrim( (string) $rel, '/' ) );
				if ( ! $path || 0 !== strpos( $path, $root . DIRECTORY_SEPARATOR ) || ! is_file( $path ) ) { $out[ $rel ] = array( 'missing' => true ); continue; }
				$data = file_get_contents( $path );
				$out[ $rel ] = array( 'b64' => base64_encode( $data ), 'md5' => md5( $data ) );
			}
			return $out;
		},
	) );
} );
'''.replace("__TOKEN__", TOKEN).replace("__NS__", NS)

stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
s, c = snip("POST", "", {"name": f"x-tmp-live-truth-{int(time.time())}", "code": "/* placeholder */", "scope": "global", "active": False})
must(s, c, "bridge create")
BR = c["id"]
listing, version, got = None, None, {}
try:
    s, u = snip("PUT", f"/{BR}", {"name": c["name"], "code": BRIDGE, "scope": "global", "active": False}); must(s, u, "bridge update")
    s, a = snip("PUT", f"/{BR}/activate", {}); must(s, a, "bridge activate")
    print("[bridge] up, id", BR)
    s, L, _ = req("POST", f"/wp-json/{NS}/v1/list", {"token": TOKEN}, timeout=180); must(s, L, "list")
    listing, version = L["files"], L["version"]
    print(f"[list] {len(listing)} files, {sum(x[1] for x in listing) / 1e6:.1f} MB, plugin {version}")
    batch, size = [], 0
    for rel, b, m in sorted(listing, key=lambda x: x[0]):
        if batch and (size + b > 4_000_000 or len(batch) >= 60):
            s, r, _ = req("POST", f"/wp-json/{NS}/v1/get", {"token": TOKEN, "rels": batch}, timeout=240); must(s, r, "get")
            got.update(r); batch, size = [], 0
            print(f"[get] {len(got)}/{len(listing)}")
        batch.append(rel); size += b
    if batch:
        s, r, _ = req("POST", f"/wp-json/{NS}/v1/get", {"token": TOKEN, "rels": batch}, timeout=240); must(s, r, "get")
        got.update(r)
finally:
    s1, _ = snip("PUT", f"/{BR}/deactivate", {}); s2, _ = snip("DELETE", f"/{BR}", None)
    s3, _, _ = req("POST", f"/wp-json/{NS}/v1/list", {"token": TOKEN}, timeout=30)
    print("[bridge] deactivate", s1, "delete", s2, "route now", s3, "(want 404)")

bad = 0
for rel, b, m in listing:
    v = got.get(rel) or {}
    if v.get("missing"):
        print("[missing]", rel); bad += 1; continue
    data = base64.b64decode(v["b64"])
    if hashlib.md5(data).hexdigest() != m:
        print("[md5 mismatch]", rel); bad += 1; continue
    p = os.path.join(OUT, "plugins", "nadlan-config", *rel.split("/"))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "wb").write(data)
if bad:
    raise SystemExit(f"FATAL: {bad} files missing or mismatched")

# the snippets, through the Code Snippets REST API (read only)
s, sn, _ = req("GET", "/wp-json/code-snippets/v1/snippets?per_page=500", None, timeout=120); must(s, sn, "snippets")
os.makedirs(os.path.join(OUT, "snippets"), exist_ok=True)
man = []
for x in sn:
    if str(x.get("name", "")).startswith(("x-tmp-", "tmp-")):
        continue  # temporary bridges (including this run's) are never part of the truth
    code = str(x.get("code", ""))
    slug = re.sub(r"[^a-z0-9]+", "-", str(x.get("name", "")).lower()).strip("-")[:60] or "snippet"
    fn = f"{x['id']}-{slug}.php"
    io.open(os.path.join(OUT, "snippets", fn), "w", encoding="utf-8", newline="").write(code)
    man.append({"id": x["id"], "name": x.get("name"), "active": bool(x.get("active")), "scope": x.get("scope"), "file": fn,
                "md5": hashlib.md5(code.encode("utf-8")).hexdigest(), "modified": x.get("modified")})
io.open(os.path.join(OUT, "snippets", "snippets.json"), "w", encoding="utf-8").write(json.dumps(man, ensure_ascii=False, indent=1))
io.open(os.path.join(OUT, "LIVE-MANIFEST.json"), "w", encoding="utf-8").write(json.dumps(
    {"read_utc": stamp, "site": "https://nad-lan.co.il", "plugin_version": version,
     "files": [{"path": r, "bytes": b, "md5": m} for r, b, m in sorted(listing)],
     "snippets": len(man), "snippets_active": sum(1 for x in man if x["active"])}, ensure_ascii=False, indent=1))
print(f"[done] {len(listing)} plugin files, {len(man)} snippets ({sum(1 for x in man if x['active'])} active) -> {OUT}")
