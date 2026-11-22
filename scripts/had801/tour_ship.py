# -*- coding: utf-8 -*-
"""HAD-801: ship Codex's Sde Dov 2036 tour folder to <site root>/tour/ through a temporary, token-gated admin bridge.
Every path the bridge touches is confined to ABSPATH/tour/. The bridge is created at start and always deleted at the end.
The old tour (plugin assets/tours/sde-dov-tour.html via inc/tour-routes.php) is never touched: while no physical folder
tour/sde-dov exists, WordPress serves it; rollback = rename the folder away.
  python tour_ship.py probe                      write tour/h801-probe/{index.php,t.json}, fetch, then remove them
  python tour_ship.py upload <zip> <stage>       upload zip in parts to tour/_h801/pkg.zip, extract to tour/<stage>
  python tour_ship.py verify <stage> <manifest>  md5 every file on the server against manifest.json
  python tour_ship.py rename <from> <to>         rename a folder under tour/
  python tour_ship.py ls [<dir>]                 list a folder under tour/
  python tour_ship.py rmzip                      remove tour/_h801 (the uploaded zip parts only)"""
import base64, hashlib, json, os, secrets, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
_src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); _ns = {"__name__": "h801ship"}
exec(compile(_src[:_src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), _ns)
req, must, snip = _ns["req"], _ns["must"], _ns["snip"]
TOKEN = secrets.token_hex(24)
NS = "nadlan-h801-ship-" + secrets.token_hex(4)
BRIDGE = r'''
add_action( 'rest_api_init', function () {
	register_rest_route( '__NS__/v1', '/op', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			@set_time_limit( 60 );
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( isset( $b['token'] ) ? $b['token'] : '' ) ) ) { return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) ); }
			$root = ABSPATH . 'tour/';
			$safe = function ( $rel ) { $rel = (string) $rel; return ( '' !== $rel && false === strpos( $rel, '..' ) && false === strpos( $rel, '\\' ) && '/' !== $rel[0] ); };
			$op = (string) $b['op'];
			if ( 'put' === $op ) {
				if ( ! $safe( $b['path'] ) ) { return new WP_Error( 'bad', 'path' ); }
				$p = $root . $b['path']; wp_mkdir_p( dirname( $p ) );
				$data = base64_decode( (string) $b['b64'], true ); if ( false === $data ) { return new WP_Error( 'bad', 'b64' ); }
				if ( isset( $b['offset'] ) ) { $fh = fopen( $p, 'c+' ); ftruncate( $fh, (int) $b['offset'] ); fseek( $fh, (int) $b['offset'] ); $n = fwrite( $fh, $data ); fclose( $fh ); }
				else { $n = file_put_contents( $p, $data, ! empty( $b['append'] ) ? FILE_APPEND : 0 ); }
				clearstatcache( true, $p );
				return array( 'wrote' => $n, 'size' => filesize( $p ) );
			}
			if ( 'md5' === $op ) {
				if ( ! $safe( $b['dir'] ) ) { return new WP_Error( 'bad', 'dir' ); }
				$out = array();
				foreach ( (array) $b['files'] as $f ) { $q = $root . $b['dir'] . '/' . $f; $out[ $f ] = ( $safe( $f ) && is_file( $q ) ) ? md5_file( $q ) : null; }
				return $out;
			}
			if ( 'unzip' === $op ) {
				if ( ! $safe( $b['zip'] ) || ! $safe( $b['dest'] ) ) { return new WP_Error( 'bad', 'path' ); }
				$z = new ZipArchive(); if ( true !== $z->open( $root . $b['zip'] ) ) { return new WP_Error( 'zip', 'open' ); }
				$n = $z->numFiles; $i = (int) $b['start']; $t0 = microtime( true ); $names = array();
				while ( $i < $n && microtime( true ) - $t0 < 18 ) {
					$nm = $z->getNameIndex( $i ); if ( ! $safe( $nm ) ) { $z->close(); return new WP_Error( 'bad', 'entry ' . $nm ); }
					$names[] = $nm; if ( count( $names ) >= 40 ) { if ( ! $z->extractTo( $root . $b['dest'], $names ) ) { $z->close(); return new WP_Error( 'zip', 'extract' ); } $names = array(); }
					$i++;
				}
				if ( $names && ! $z->extractTo( $root . $b['dest'], $names ) ) { $z->close(); return new WP_Error( 'zip', 'extract' ); }
				$z->close(); return array( 'next' => $i, 'total' => $n );
			}
			if ( 'dupjs' === $op ) {
				if ( ! $safe( $b['dir'] ) ) { return new WP_Error( 'bad', 'dir' ); }
				$base = $root . $b['dir'] . '/'; $t0 = microtime( true ); $made = 0; $left = 0;
				$it = new RecursiveIteratorIterator( new RecursiveDirectoryIterator( $base, FilesystemIterator::SKIP_DOTS ) );
				foreach ( $it as $f ) {
					$p = $f->getPathname(); $rel = substr( $p, strlen( $base ) );
					if ( 0 === strpos( $rel, 'transfer/' ) || 0 === strpos( $rel, 'pages/' ) || ! preg_match( '/\.(bin|json)$/', $p ) || file_exists( $p . '.js' ) ) { continue; }
					if ( microtime( true ) - $t0 > 18 ) { $left++; continue; }
					if ( ! copy( $p, $p . '.js' ) ) { return new WP_Error( 'copy', $rel ); }
					$made++;
				}
				return array( 'made' => $made, 'left' => $left );
			}
			if ( 'rename' === $op ) {
				if ( ! $safe( $b['from'] ) || ! $safe( $b['to'] ) || file_exists( $root . $b['to'] ) ) { return new WP_Error( 'bad', 'rename' ); }
				return array( 'ok' => rename( $root . $b['from'], $root . $b['to'] ) );
			}
			if ( 'ls' === $op ) {
				$d = $root . ( empty( $b['dir'] ) ? '' : ( $safe( $b['dir'] ) ? $b['dir'] : 'x-none' ) );
				return is_dir( $d ) ? array_values( array_diff( scandir( $d ), array( '.', '..' ) ) ) : null;
			}
			if ( 'rmtree' === $op ) {
				if ( ! in_array( $b['dir'], array( '_h801', 'h801-probe' ), true ) ) { return new WP_Error( 'bad', 'only the bridge scratch folders' ); }
				$d = $root . $b['dir']; if ( ! is_dir( $d ) ) { return array( 'gone' => true ); }
				foreach ( array_diff( scandir( $d ), array( '.', '..' ) ) as $f ) { @unlink( $d . '/' . $f ); }
				return array( 'gone' => @rmdir( $d ) );
			}
			return new WP_Error( 'bad', 'op' );
		},
	) );
} );
'''.replace("__TOKEN__", TOKEN).replace("__NS__", NS)


def op(**kw):
    kw["token"] = TOKEN
    for attempt in range(4):
        s, r, _ = req("POST", "/wp-json/%s/v1/op" % NS, kw, timeout=300)
        if s == 200:
            return r
        print("  retry", attempt, s, json.dumps(r)[:200]); time.sleep(5 + attempt * 10)
    raise SystemExit("FATAL op %s: %s %s" % (kw.get("op"), s, json.dumps(r)[:300]))


def get(path):
    rq = urllib.request.Request("https://nad-lan.co.il" + path, headers={"User-Agent": "Mozilla/5.0 h801"})
    try:
        with urllib.request.urlopen(rq, timeout=60) as r:
            return r.status, r.read(), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read(), dict(e.headers)


s, c = snip("POST", "", {"name": "tmp-h801-ship-%d" % int(time.time()), "code": "/* placeholder */", "scope": "global", "active": False})
must(s, c, "bridge create"); BR = c["id"]
try:
    s, u = snip("PUT", "/%s" % BR, {"name": c["name"], "code": BRIDGE, "scope": "global", "active": False}); must(s, u, "bridge update")
    s, a = snip("PUT", "/%s/activate" % BR, {}); must(s, a, "bridge activate")
    cmd = sys.argv[1]
    if cmd == "probe":
        print(op(op="put", path="h801-probe/index.php", b64=base64.b64encode(b"<?php header('X-H801: php'); echo 'h801-ok ' . PHP_VERSION;").decode()))
        print(op(op="put", path="h801-probe/t.json", b64=base64.b64encode(b'{"ok":1}').decode()))
        for p in ("/tour/h801-probe/", "/tour/h801-probe/index.php", "/tour/h801-probe/t.json", "/tour/h801-probe", "/tour/sde-dov/", "/tour/somail/"):
            st, body, hd = get(p); print(p, st, hd.get("Content-Type"), hd.get("X-H801"), hd.get("X-NL-Tour"), body[:40])
        print(op(op="rmtree", dir="h801-probe"))
    elif cmd == "upload":
        z, stage = sys.argv[2], sys.argv[3]
        size = os.path.getsize(z); CH = 6 * 1024 * 1024; t0 = time.time()
        pass
        with open(z, "rb") as f:
            i = 0
            while True:
                b = f.read(CH)
                if not b:
                    break
                r = op(op="put", path="_h801/pkg.zip", b64=base64.b64encode(b).decode(), offset=f.tell() - len(b))
                i += 1
                print("  part %d  %d / %d MB  %.0fs" % (i, r["size"] // 1048576, size // 1048576, time.time() - t0), flush=True)
                if r["size"] != f.tell():
                    raise SystemExit("size mismatch at part %d: server %s local %s" % (i, r["size"], f.tell()))
        md = hashlib.md5(open(z, "rb").read()).hexdigest()
        r = op(op="md5", dir="_h801", files=["pkg.zip"]); print("zip md5 local", md, "server", r["pkg.zip"])
        if r["pkg.zip"] != md:
            raise SystemExit("zip md5 mismatch")
        nxt = 0
        while True:
            r = op(op="unzip", zip="_h801/pkg.zip", dest=stage, start=nxt)
            nxt = r["next"]; print("  extracted %d / %d" % (nxt, r["total"]), flush=True)
            if nxt >= r["total"]:
                break
    elif cmd == "verify":
        stage, man = sys.argv[2], json.load(open(sys.argv[3], encoding="utf-8"))
        names = sorted(man); bad = []
        for k in range(0, len(names), 300):
            part = names[k:k + 300]; r = op(op="md5", dir=stage, files=part)
            bad += [n for n in part if r.get(n) != man[n]["md5"]]
        print("verified", len(names), "files; mismatches", len(bad), bad[:10])
        if bad:
            raise SystemExit(2)
    elif cmd == "dupjs":
        while True:
            r = op(op="dupjs", dir=sys.argv[2]); print("  twins made", r["made"], "left", r["left"], flush=True)
            if not r["left"]:
                break
    elif cmd == "rename":
        print(op(op="rename", **{"from": sys.argv[2], "to": sys.argv[3]}))
    elif cmd == "ls":
        print(op(op="ls", dir=sys.argv[2] if len(sys.argv) > 2 else ""))
    elif cmd == "rmzip":
        print(op(op="rmtree", dir="_h801"))
finally:
    s1, _ = snip("PUT", "/%s/deactivate" % BR, {}); s2, _ = snip("DELETE", "/%s" % BR, None)
    print("[bridge] cleanup", s1, s2)
