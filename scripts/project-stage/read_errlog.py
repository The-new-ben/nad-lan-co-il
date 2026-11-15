# -*- coding: utf-8 -*-
"""READ-ONLY (15.11.2026, main session: Ben says the host wrote that our plugins cause faults): where PHP writes its error log on
nad-lan.co.il, how big it is, and a count of its last ~2 MB by kind and by source (plugin / theme / core), plus how often the
_doing_it_wrong notice about 'read' appears. Prints counts and short samples only. A temporary admin bridge, deleted at the end.
python scripts/project-stage/read_errlog.py"""
import collections, io, json, os, re, secrets, time
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "errlog"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
req, snip = ns["req"], ns["snip"]
BRIDGE = r'''
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-errlog/v1', '/run', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( $b['token'] ?? '' ) ) ) { return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) ); }
			$cands = array_unique( array_filter( array( ini_get( 'error_log' ), WP_CONTENT_DIR . '/debug.log', ABSPATH . 'error_log', ABSPATH . 'wp-admin/error_log', dirname( ABSPATH ) . '/logs/error.log', dirname( ABSPATH ) . '/logs/php_error.log' ) ) );
			$out = array( 'wp_debug' => defined( 'WP_DEBUG' ) && WP_DEBUG, 'wp_debug_log' => defined( 'WP_DEBUG_LOG' ) ? WP_DEBUG_LOG : null, 'log_errors' => ini_get( 'log_errors' ), 'ini_error_log' => ini_get( 'error_log' ), 'files' => array() );
			foreach ( $cands as $f ) {
				if ( ! is_string( $f ) || '' === $f || ! @is_file( $f ) || ! @is_readable( $f ) ) { continue; }
				$size = filesize( $f ); $h = fopen( $f, 'rb' ); $take = min( $size, 2 * 1024 * 1024 ); fseek( $h, $size - $take ); $tail = fread( $h, $take ); fclose( $h );
				$out['files'][] = array( 'path' => str_replace( ABSPATH, '', $f ), 'size' => $size, 'mtime' => gmdate( 'Y-m-d H:i', filemtime( $f ) ), 'tail' => base64_encode( $tail ) );
			}
			$fd = WP_PLUGIN_DIR . '/file-manager-advanced';
			$out['fma'] = array( 'active' => in_array( 'file-manager-advanced/file_manager_advanced.php', (array) get_option( 'active_plugins', array() ), true ), 'dir' => is_dir( $fd ),
				'adminer_tpl' => file_exists( $fd . '/templates/adminer.php' ), 'templates' => is_dir( $fd . '/templates' ) ? array_values( array_diff( scandir( $fd . '/templates' ), array( '.', '..' ) ) ) : null,
				'menus_mtime' => file_exists( $fd . '/application/class_fma_admin_menus.php' ) ? gmdate( 'Y-m-d H:i', filemtime( $fd . '/application/class_fma_admin_menus.php' ) ) : null,
				'dir_mtime' => is_dir( $fd ) ? gmdate( 'Y-m-d H:i', filemtime( $fd ) ) : null, 'php' => PHP_VERSION,
				'plugins_fma' => array_values( array_filter( (array) get_option( 'active_plugins', array() ), function ( $p ) { return false !== strpos( $p, 'file-manager' ); } ) ) );
			return $out;
		},
	) );
} );
'''
tok = secrets.token_hex(24); nm = "tmp-errlog-%d" % int(time.time())
s, sn = snip("POST", "", {"name": nm, "code": "/* placeholder */", "scope": "global", "active": False}); bid = sn["id"]
try:
    s1, _ = snip("PUT", "/%d" % bid, {"name": nm, "code": BRIDGE.replace("__TOKEN__", tok), "scope": "global", "active": False})
    s2, _ = snip("PUT", "/%d/activate" % bid, {})
    assert s1 == 200 and s2 == 200, (s1, s2)
    time.sleep(2)
    s, res, _ = req("POST", "/wp-json/nadlan-errlog/v1/run", {"token": tok}, timeout=180)
finally:
    a, _ = snip("PUT", "/%d/deactivate" % bid, {}); b, _ = snip("DELETE", "/%d" % bid, None)
    c, _, _ = req("POST", "/wp-json/nadlan-errlog/v1/run", {"token": "x"})
    print("[bridge] deactivate", a, "| delete", b, "| route now", c, "(want 404)")
import base64
print("http", s, "| WP_DEBUG", res.get("wp_debug"), "| WP_DEBUG_LOG", res.get("wp_debug_log"), "| log_errors", res.get("log_errors"), "| ini error_log", res.get("ini_error_log"))
print("file manager advanced:", json.dumps(res.get("fma"), ensure_ascii=False))
summary = {"at": time.strftime("%Y-%m-%d %H:%M:%S"), "fma": res.get("fma"), "files": []}
for f in res.get("files", []):
    tail = base64.b64decode(f["tail"]).decode("utf-8", "replace").splitlines()
    dates = [m.group(1) for m in (re.match(r"^\[(\d{2}-\w{3}-\d{4} [\d:]+)", l) for l in tail) if m]
    kinds = collections.Counter(); srcs = collections.Counter(); reads = 0; samples = {}
    for l in tail:
        m = re.search(r"PHP (Fatal error|Warning|Notice|Deprecated|Parse error)", l); k = m.group(1) if m else ("doing_it_wrong" if "incorrectly" in l or "_doing_it_wrong" in l else "other")
        kinds[k] += 1
        if "must always check it against a specific post" in l and "read" in l: reads += 1
        m2 = re.search(r"wp-content/(plugins|themes|mu-plugins)/([^/ ]+)", l); sk = (m2.group(1) + "/" + m2.group(2)) if m2 else ("wp-includes/core" if "wp-includes" in l or "wp-admin" in l else "unknown")
        srcs[(k, sk)] += 1
        samples.setdefault((k, sk), re.sub(r"\s+", " ", l)[:220])
    row = {"path": f["path"], "size_mb": round(f["size"] / 1048576, 2), "mtime": f["mtime"], "lines_in_tail": len(tail), "tail_from": dates[0] if dates else "", "tail_to": dates[-1] if dates else "",
           "kinds": dict(kinds), "read_check_notices": reads, "top_sources": [[k, s_, n] for (k, s_), n in srcs.most_common(14)], "samples": [[k, s_, samples[(k, s_)]] for (k, s_), n in srcs.most_common(8)]}
    summary["files"].append(row)
    print(json.dumps({k: v for k, v in row.items() if k != "samples"}, ensure_ascii=False))
    for smp in row["samples"]:
        print("   ", smp[0], "|", smp[1], "|", smp[2][:200])
io.open(os.path.join(REPO, "docs", "qa", "had-740", "errlog-summary-%s.json" % time.strftime("%Y%m%dT%H%M%S")), "w", encoding="utf-8").write(json.dumps(summary, ensure_ascii=False, indent=1))
if not res.get("files"):
    print("no readable PHP error log at the usual places")
