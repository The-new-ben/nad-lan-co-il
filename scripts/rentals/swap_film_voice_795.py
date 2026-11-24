# -*- coding: utf-8 -*-
"""HAD-795, 24.11.2026: replace the two rentals tutorial films IN PLACE (same Media Library items 9295 he / 9296 en, same
addresses), Hebrew voice -> English voice (Ben 24.11.2026: "כרגע רק אנגלית עם תרגום בעברית"). No code release: the product row
points at the same addresses. A temporary admin bridge (deleted at the end, same pattern as live_read.py / deployskin.py) may
write ONLY the files attached to 9295 and 9296: chunks go to a .swap-tmp file, the commit checks the md5, keeps the live file as
<name>.bak-20261124-hevoice beside it, then moves the new file in and refreshes the attachment's size data. Then a public GET
(plain and cache-busted) whose md5 must equal the new file; the page HTML does not change, so no page purge is needed. The app password is decrypted in-process (DPAPI) and never printed.
  python scripts/rentals/swap_film_voice_795.py [--dry]"""
import base64, hashlib, json, os, secrets, sys, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
_src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
_ns = {"__name__": "swap_helpers"}
exec(compile(_src[:_src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), _ns)
req, must, snip, UA = _ns["req"], _ns["must"], _ns["snip"], _ns["UA"]
DRY = "--dry" in sys.argv
SRC = r"D:\Media\NadLan-Films\rentals-tutorial\out\v3"
JOBS = [(9295, os.path.join(SRC, "rentals-tutorial-he-phone.mp4")), (9296, os.path.join(SRC, "rentals-tutorial-en-phone.mp4"))]
CHUNK = 1024 * 1024
TOKEN = secrets.token_hex(24)
BRIDGE = r'''
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-film-swap/v1', '/op', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( isset( $b['token'] ) ? $b['token'] : '' ) ) ) { return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) ); }
			$id = (int) $b['id'];
			if ( ! in_array( $id, array( 9295, 9296 ), true ) ) { return new WP_Error( 'forbidden', 'id', array( 'status' => 403 ) ); }
			$path = get_attached_file( $id );
			if ( ! $path || ! is_file( $path ) || '.mp4' !== substr( $path, -4 ) ) { return new WP_Error( 'missing', 'file', array( 'status' => 404 ) ); }
			$tmp = $path . '.swap-tmp'; $bak = $path . '.bak-20261124-hevoice'; $op = (string) $b['op'];
			if ( 'status' === $op ) { return array( 'md5' => md5_file( $path ), 'bytes' => filesize( $path ), 'bak' => is_file( $bak ) ? md5_file( $bak ) : null, 'name' => basename( $path ) ); }
			if ( 'begin' === $op || 'append' === $op ) {
				$data = base64_decode( (string) $b['b64'], true );
				if ( false === $data ) { return new WP_Error( 'bad', 'b64', array( 'status' => 400 ) ); }
				$n = file_put_contents( $tmp, $data, 'append' === $op ? FILE_APPEND : 0 );
				return array( 'wrote' => $n, 'size' => filesize( $tmp ) );
			}
			if ( 'commit' === $op ) {
				clearstatcache();
				if ( ! is_file( $tmp ) || md5_file( $tmp ) !== (string) $b['md5'] ) { @unlink( $tmp ); return new WP_Error( 'bad', 'md5', array( 'status' => 409 ) ); }
				$old = md5_file( $path );
				if ( ! is_file( $bak ) && ! copy( $path, $bak ) ) { return new WP_Error( 'bad', 'backup', array( 'status' => 500 ) ); }
				if ( ! rename( $tmp, $path ) ) { return new WP_Error( 'bad', 'rename', array( 'status' => 500 ) ); }
				clearstatcache();
				$meta = wp_get_attachment_metadata( $id );
				if ( is_array( $meta ) ) { $meta['filesize'] = filesize( $path ); wp_update_attachment_metadata( $id, $meta ); }
				return array( 'old' => $old, 'md5' => md5_file( $path ), 'bytes' => filesize( $path ), 'bak' => md5_file( $bak ) );
			}
			return new WP_Error( 'bad', 'op', array( 'status' => 400 ) );
		},
	) );
} );
'''.replace("__TOKEN__", TOKEN)


def op(body):
    body["token"] = TOKEN
    s, r, _ = req("POST", "/wp-json/nadlan-film-swap/v1/op", body, timeout=300)
    return must(s, r, "op " + body.get("op", ""))


s, c = snip("POST", "", {"name": "tmp-film-swap-%d" % int(time.time()), "code": "/* placeholder */", "scope": "global", "active": False})
must(s, c, "bridge create"); BR = c["id"]
result = {}
try:
    s, u = snip("PUT", "/%d" % BR, {"name": c["name"], "code": BRIDGE, "scope": "global", "active": False}); must(s, u, "bridge update")
    s, a = snip("PUT", "/%d/activate" % BR, {}); must(s, a, "bridge activate")
    for mid, src in JOBS:
        data = open(src, "rb").read(); md5 = hashlib.md5(data).hexdigest()
        st = op({"id": mid, "op": "status"})
        print("[%d] live %s %d B md5 %s | new %d B md5 %s" % (mid, st["name"], st["bytes"], st["md5"][:10], len(data), md5[:10]))
        if st["md5"] == md5:
            print("  already the new file"); result[mid] = st; continue
        if DRY:
            continue
        for i in range(0, len(data), CHUNK):
            r = op({"id": mid, "op": "begin" if i == 0 else "append", "b64": base64.b64encode(data[i:i + CHUNK]).decode()})
        assert r["size"] == len(data), r
        r = op({"id": mid, "op": "commit", "md5": md5})
        assert r["md5"] == md5, r
        print("  swapped: old %s kept as .bak (%s), new %s" % (r["old"][:10], r["bak"][:10], r["md5"][:10]))
        result[mid] = r
finally:
    s1, _ = snip("PUT", "/%d/deactivate" % BR, {}); s2, _ = snip("DELETE", "/%d" % BR, None)
    print("[bridge] cleanup", s1, s2)
if DRY:
    raise SystemExit(0)
media = json.load(open(os.path.join(REPO, "docs", "rentals", "build", "film", "media.json"), encoding="utf-8"))
ok = True
for mid, src in JOBS:
    name = os.path.basename(src); url = media["files"][name]["url"]
    want = hashlib.md5(open(src, "rb").read()).hexdigest()
    with urllib.request.urlopen(urllib.request.Request(url + "?v=%d" % int(time.time()), headers={"User-Agent": UA}), timeout=300) as r:
        got = hashlib.md5(r.read()).hexdigest(); hdr = {k: v for k, v in r.headers.items() if k.lower() in ("x-litespeed-cache", "cache-control", "last-modified", "content-length", "x-cache")}
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=300) as r:
        plain = hashlib.md5(r.read()).hexdigest()
    print("[public] %s busted %s plain %s %s" % (url, "SAME" if got == want else "DIFFERS", "SAME" if plain == want else "STALE", hdr))
    ok = ok and got == want and plain == want
    media["files"][name].update({"md5": want, "bytes": os.path.getsize(src), "voice": "English (Kokoro af_heart), v3 24.11.2026", "hebrew_voice_backup_on_server": name + ".bak-20261124-hevoice"})
media["swapped_utc"] = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())
open(os.path.join(REPO, "docs", "rentals", "build", "film", "media.json"), "w", encoding="utf-8").write(json.dumps(media, ensure_ascii=False, indent=1))
print("OK" if ok else "CHECK: a public copy is stale or differs")
sys.exit(0 if ok else 1)
