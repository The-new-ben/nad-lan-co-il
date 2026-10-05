# -*- coding: utf-8 -*-
"""HAD-256 release runner: the owner listing journey (x-owner-wizard, snippet 707) on the engine x-broker-drop 1.1.4.
Main runs it; nobody else. What it writes: two Code Snippets (x-broker-drop by its 8 hunks, then 707 whole, with the
private-folder prelude), optionally page 4958's copy (--page A|B), and the folder dirname( ABSPATH ) . '/nl-private'.
Everything comes from scripts/project-stage/had256_release.py (pinned by SHA-256; regenerate it with
scripts/had-256/make_release.py --snap <commit>). Credentials: deployskin.py's prefix (the app password decrypted
in-process by DPAPI, never printed), exactly as scripts/project-stage/upload_project_films.py loads it.

  python scripts/had-256/deploy_had256.py --dry --page B          read, back up, build, lint, private-folder check; no write
  python scripts/had-256/deploy_had256.py --package 202 --page B  the 2.0.2 package (had256_release_202.py) instead of 2.0.1
  python scripts/had-256/deploy_had256.py --page B                the release (--page keep: no page change)
  python scripts/had-256/deploy_had256.py --rollback docs/qa/had-256/live-backup/<UTC>
  rehearsal on a local bench only (never the live site, no secret read):
  python scripts/had-256/deploy_had256.py --bench http://127.0.0.1:9408 --bench-auth <file "user:app password"> [--bench-fail-check]

Steps: 1 the release lock line + live health (own step; refuses unless the last RELEASE line is DONE or ROLLED BACK, no
other release bridge active); 2 read snippet 707 and x-broker-drop, refuse unless they are the expected bases; 3 save both
bodies to docs/qa/had-256/live-backup/<UTC>/ before anything else; 4 build the package, lint locally (php -l) and on the
server (the bridge's lint_code); 5 the private folder: made, writable, outside ABSPATH and the document root, a test file
NOT reachable over HTTP (403/404), test file removed; 6 write the engine first, then 707 (then the page), read each back
and compare hashes; 7 purge; 8 the check strings (anonymous, cache-busted, then plain); a failure after a second purge
rolls back AUTOMATICALLY (707 first, then the engine, then the page; purge; the rollback checks); 9 the bridge goes down
and its route must answer 404. The record: docs/qa/had-256/deploy-result-had256.json.
"""
import base64, hashlib, io, json, os, re, secrets, shutil, signal, subprocess, sys, tempfile, time, urllib.error, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", line_buffering=True)
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
QA = os.path.join(REPO, "docs", "qa", "had-256")
RESULT = os.path.join(QA, "deploy-result-had256.json")
sys.path.insert(0, os.path.join(REPO, "scripts", "project-stage"))
ARGS = sys.argv[1:]
# --package 202: the 2.0.2 module (had256_release_202.py); default: had256_release.py
import importlib  # noqa: E402
R = importlib.import_module("had256_release" + ("_" + ARGS[ARGS.index("--package") + 1] if "--package" in ARGS else ""))


def arg(name, default=None):
    return ARGS[ARGS.index(name) + 1] if name in ARGS and ARGS.index(name) + 1 < len(ARGS) else default


DRY = "--dry" in ARGS
ROLLBACK_DIR = arg("--rollback")
PAGE = arg("--page")
BENCH = arg("--bench")
FAIL_CHECK = "--bench-fail-check" in ARGS   # rehearsal only: one need-string that cannot be there, to prove the automatic rollback
CRASH = "--bench-crash-after-write" in ARGS   # rehearsal only: an error right after the engine is written
FLAKE = {"left": 2 if "--bench-net-flake" in ARGS else 0}   # rehearsal only: the first two check fetches fail as on the live run
if not ROLLBACK_DIR and PAGE not in ("A", "B", "keep"):
    raise SystemExit("usage: --page A|B|keep is required (A: no page paragraph; B: the truthful paragraph; keep: page 4958 untouched)")
sha = lambda s: hashlib.sha256((s if isinstance(s, bytes) else s.encode("utf-8"))).hexdigest()
lf = lambda s: (s or "").replace("\r\n", "\n")
UTC = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())

# ---------------------------------------------------------------- the connection
if BENCH:
    if "nad-lan.co.il" in BENCH or not re.match(r"^http://(127\.0\.0\.1|localhost):\d+$", BENCH):
        raise SystemExit("FATAL: --bench takes a loopback bench address only")
    BASE = BENCH
    _u = open(arg("--bench-auth"), encoding="utf-8").read().strip()
    AUTH = "Basic " + base64.b64encode(_u.encode()).decode()
    del _u
    UA = "Mozilla/5.0 NadLan-HAD256-rehearsal/1.0"

    def req(method, path, body=None, timeout=180, raw=False, auth=True, headers=None):
        r = urllib.request.Request(BASE + path, data=(json.dumps(body, ensure_ascii=False).encode() if body is not None else None), method=method)
        if auth:
            r.add_header("Authorization", AUTH)
        r.add_header("User-Agent", UA)
        if body is not None:
            r.add_header("Content-Type", "application/json")
        for k, v in (headers or {}).items():
            r.add_header(k, v)
        try:
            with urllib.request.urlopen(r, timeout=timeout) as resp:
                p = resp.read()
                return resp.status, (p if raw else json.loads(p.decode() or "null")), dict(resp.headers)
        except urllib.error.HTTPError as e:
            p = e.read()
            if raw:
                return e.code, p, dict(e.headers)
            try:
                return e.code, json.loads(p.decode()), dict(e.headers)
            except Exception:
                return e.code, {"raw": p[:300].decode("utf-8", "replace")}, dict(e.headers)

    def must(s, p, what, ok=(200, 201)):
        if s not in ok:
            raise SystemExit(f"FATAL {what}: HTTP {s}: {json.dumps(p, ensure_ascii=False)[:400]}")
        return p

    def snip(method, path, body=None):
        return req(method, "/wp-json/code-snippets/v1/snippets" + path, body)[:2]
else:
    # deployskin.py's prefix: BASE, AUTH (DPAPI, in-process), req, must, snip; as upload_project_films.py loads it
    _src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
    # deployskin re-wraps sys.stdout too; a second wrapper orphans this runner's wrapper, whose collection closes the shared buffer
    # ("I/O operation on closed file" on the first live dry run, 6.10.2026). The runner already wraps stdout, so skip that line.
    _src = _src.replace('sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")', "pass", 1)
    _ns = {"__name__": "had256_helpers"}
    exec(compile(_src[:_src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), _ns)
    req, must, snip, BASE = _ns["req"], _ns["must"], _ns["snip"], _ns["BASE"]
    del _src, _ns
    if BASE != "https://nad-lan.co.il":
        raise SystemExit("FATAL: deployskin.py's BASE is not the live site: " + BASE)


import http.client, socket  # noqa: E402

NET_ERRORS = (http.client.IncompleteRead, http.client.HTTPException, urllib.error.URLError, ConnectionError, TimeoutError, socket.timeout)


def net(fn, what):
    """A check's network call, tried up to 3 times on a NETWORK error (a cut answer, a reset, a timeout): main's live run
    of 6.10 rolled back on one IncompleteRead. An HTTP status is an answer, not a network error, and is never retried here;
    a content failure is judged by the check. Three network failures in a row = None (the check counts it as failed)."""
    for i in range(3):
        try:
            if BENCH and FLAKE["left"]:
                FLAKE["left"] -= 1
                raise http.client.IncompleteRead(b"rehearsal", 1000)
            return fn()
        except urllib.error.HTTPError:
            raise
        except NET_ERRORS as e:
            print(f"[net] {what}: {type(e).__name__} (try {i + 1} of 3)")
            time.sleep(3)
    return None


def get_page(path, tag=None):
    url = path + (("&" if "?" in path else "?") + "nlv=" + tag if tag else "")
    r = net(lambda: req("GET", url, raw=True, auth=False, timeout=90, headers={"Cache-Control": "no-cache"} if tag else None), "GET " + url)
    if r is None:
        return 0, ""
    s, b, h = r
    return s, (b.decode("utf-8", "replace") if isinstance(b, (bytes, bytearray)) else json.dumps(b))


def get_json(path):
    r = net(lambda: req("GET", path, auth=False), "GET " + path)
    return (0, {}) if r is None else (r[0], r[1])


REC = {}


def record(state, **extra):
    REC.update({"state": state, "at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "base": BASE, "package": R.SNAPSHOT,
                "owner": R.OWNER_VERSION, "engine": R.BROKER_VERSION, "page": PAGE})
    REC.update(extra)
    if BENCH:
        REC["bench"] = True
    tmp = RESULT + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(REC, fh, ensure_ascii=False, indent=2)
    os.replace(tmp, RESULT if not BENCH else RESULT.replace(".json", ".bench.json"))
    print(f"[record] {state}")


def php_lint_local(body, label):
    exe = shutil.which("php") or (r"C:\Users\777\tools\php-8.3\php.exe" if os.path.exists(r"C:\Users\777\tools\php-8.3\php.exe") else None)
    if not exe:
        raise SystemExit("FATAL: no local php for php -l")
    with tempfile.NamedTemporaryFile("wb", suffix=".php", delete=False) as t:
        t.write(("<?php\n" + body).encode("utf-8"))
        tmp = t.name
    try:
        out = subprocess.run([exe, "-l", tmp], capture_output=True, text=True)
    finally:
        os.unlink(tmp)
    if out.returncode != 0:
        raise SystemExit(f"FATAL local php -l {label}: {out.stdout.strip()} {out.stderr.strip()}")
    print(f"[lint] local php -l {label}: ok")


# ---------------------------------------------------------------- the bridge (a temporary token-gated, admin-only snippet)
TOKEN = secrets.token_hex(24)
NS = "nadlan-h256r-" + TOKEN[:8]
BRIDGE = r'''
add_action( 'rest_api_init', function () {
	register_rest_route( '__NS__/v1', '/apply', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( $b['token'] ?? '' ) ) ) { return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) ); }
			$out = array();
			if ( ! empty( $b['head'] ) ) { $out['head'] = defined( 'NADLAN_CONFIG_VERSION' ) ? NADLAN_CONFIG_VERSION : ''; $out['php'] = PHP_VERSION; }
			if ( isset( $b['lint_code'] ) ) {   // a Code Snippets body, linted as PHP with the opening tag it is stored without
				try { token_get_all( "<?php\n" . (string) $b['lint_code'], TOKEN_PARSE ); $out['lint_code'] = 'ok ' . PHP_VERSION; }
				catch ( ParseError $e ) { return new WP_Error( 'lint', $e->getMessage() . ' line ' . $e->getLine(), array( 'status' => 400 ) ); }
			}
			if ( ! empty( $b['page'] ) && is_array( $b['page'] ) ) {   // page 4958's raw content, written only over the expected text
				$c  = $b['page'];
				$pg = get_page_by_path( (string) $c['path'], OBJECT, 'page' );
				if ( ! $pg ) { return new WP_Error( 'page', 'no page ' . (string) $c['path'], array( 'status' => 404 ) ); }
				$cur = (string) get_post_field( 'post_content', $pg->ID, 'raw' );
				if ( ! empty( $c['get'] ) ) { $out['page'] = array( 'id' => (int) $pg->ID, 'b64' => base64_encode( $cur ), 'sha' => hash( 'sha256', $cur ) ); }
				else {
					if ( empty( $c['force'] ) && hash( 'sha256', $cur ) !== (string) $c['expect'] ) { return new WP_Error( 'drift', 'content changed: ' . hash( 'sha256', $cur ), array( 'status' => 409 ) ); }
					$new = base64_decode( (string) $c['b64'], true );
					if ( false === $new || hash( 'sha256', $new ) !== (string) $c['sha'] ) { return new WP_Error( 'sha', 'content mismatch', array( 'status' => 400 ) ); }
					kses_remove_filters();
					$r = wp_update_post( wp_slash( array( 'ID' => $pg->ID, 'post_content' => $new ) ), true );
					kses_init_filters();
					if ( is_wp_error( $r ) ) { return $r; }
					clean_post_cache( $pg->ID );
					do_action( 'litespeed_purge_post', $pg->ID );
					$now = (string) get_post_field( 'post_content', $pg->ID, 'raw' );
					$out['page'] = array( 'id' => (int) $pg->ID, 'sha' => hash( 'sha256', $now ) );
				}
			}
			if ( ! empty( $b['privdir'] ) && is_array( $b['privdir'] ) ) {   // the owners' private photo folder (the prelude's own expression)
				$p    = $b['privdir'];
				$dir  = __PRIVDIR__;
				$real = function ( $x ) { $r = realpath( $x ); return false === $r ? '' : rtrim( str_replace( '\\', '/', $r ), '/' ) . '/'; };
				$abs  = $real( ABSPATH );
				$doc  = ! empty( $_SERVER['DOCUMENT_ROOT'] ) ? $real( (string) $_SERVER['DOCUMENT_ROOT'] ) : '';
				if ( ! empty( $p['make'] ) && ! is_dir( $dir ) ) { wp_mkdir_p( $dir ); }
				$rd   = $real( $dir );
				$o    = array( 'dir' => $dir, 'exists' => is_dir( $dir ), 'writable' => is_dir( $dir ) && wp_is_writable( $dir ), 'parent_writable' => wp_is_writable( dirname( $dir ) ),
					'inside_abspath' => '' !== $rd && '' !== $abs && 0 === strpos( $rd, $abs ), 'inside_docroot' => '' !== $rd && '' !== $doc && 0 === strpos( $rd, $doc ),
					'open_basedir' => (string) ini_get( 'open_basedir' ), 'defined_now' => defined( 'NL_OWNER_PRIVATE_DIR' ) ? (string) NL_OWNER_PRIVATE_DIR : null );
				if ( ! empty( $p['probe'] ) && $o['writable'] ) {
					$name = 'had256-http-probe-' . preg_replace( '/[^a-f0-9]/', '', (string) $p['probe'] ) . '.txt';
					$o['probe_written'] = false !== @file_put_contents( $dir . '/' . $name, 'had256 probe ' . (string) $p['probe'] );
					$o['probe_name'] = $name;
					$urls = array( home_url( '/nl-private/' . $name ), home_url( '/../nl-private/' . $name ), content_url( '/nl-private/' . $name ), content_url( '/uploads/nl-private/' . $name ) );
					if ( $o['inside_docroot'] ) { $urls[] = home_url( '/' . ltrim( substr( $rd, strlen( $doc ) ), '/' ) . $name ); }
					$o['urls'] = array_values( array_unique( $urls ) );
				}
				if ( ! empty( $p['clean'] ) ) {
					$name = 'had256-http-probe-' . preg_replace( '/[^a-f0-9]/', '', (string) $p['clean'] ) . '.txt';
					$o['cleaned'] = file_exists( $dir . '/' . $name ) ? ( @unlink( $dir . '/' . $name ) ? 1 : 0 ) : 'missing';
				}
				$out['privdir'] = $o;
			}
			if ( ! empty( $b['ymeta'] ) && is_array( $b['ymeta'] ) ) {   // page 4958's Yoast texts (_yoast_wpseo_* only), written only over the expected value
				$c  = $b['ymeta'];
				$pg = get_page_by_path( (string) $c['path'], OBJECT, 'page' );
				if ( ! $pg ) { return new WP_Error( 'page', 'no page ' . (string) $c['path'], array( 'status' => 404 ) ); }
				if ( ! empty( $c['get'] ) ) {
					$vals = array();
					foreach ( (array) $c['get'] as $k ) {
						$k = (string) $k;
						if ( 0 !== strpos( $k, '_yoast_wpseo_' ) ) { continue; }
						$v = (string) get_post_meta( $pg->ID, $k, true );
						$vals[ $k ] = array( 'exists' => metadata_exists( 'post', $pg->ID, $k ), 'b64' => base64_encode( $v ), 'sha' => hash( 'sha256', $v ) );
					}
					$out['ymeta'] = array( 'id' => (int) $pg->ID, 'vals' => $vals );
				} elseif ( ! empty( $c['set'] ) ) {
					$k = (string) $c['set'];
					if ( 0 !== strpos( $k, '_yoast_wpseo_' ) ) { return new WP_Error( 'key', 'only Yoast keys', array( 'status' => 400 ) ); }
					$cur = (string) get_post_meta( $pg->ID, $k, true );
					if ( empty( $c['force'] ) && hash( 'sha256', $cur ) !== (string) $c['expect'] ) { return new WP_Error( 'drift', 'meta changed: ' . hash( 'sha256', $cur ), array( 'status' => 409 ) ); }
					$new = base64_decode( (string) $c['b64'], true );
					if ( false === $new || hash( 'sha256', $new ) !== (string) $c['sha'] ) { return new WP_Error( 'sha', 'meta mismatch', array( 'status' => 400 ) ); }
					update_post_meta( $pg->ID, $k, wp_slash( $new ) );
					clean_post_cache( $pg->ID );
					do_action( 'litespeed_purge_post', $pg->ID );
					$now = (string) get_post_meta( $pg->ID, $k, true );
					$out['ymeta'] = array( 'id' => (int) $pg->ID, 'key' => $k, 'sha' => hash( 'sha256', $now ) );
				}
			}
			if ( ! empty( $b['purge'] ) ) {
				if ( function_exists( 'opcache_reset' ) ) { $out['opcache'] = @opcache_reset(); }
				do_action( 'litespeed_purge_all' );
				wp_cache_flush();
				$out['purged'] = 1;
			}
			return $out;
		},
	) );
} );
'''.replace("__TOKEN__", TOKEN).replace("__NS__", NS).replace("__PRIVDIR__", R.PRIVATE_DIR_EXPR)
BR = None


def ops(payload, what):
    payload = dict(payload, token=TOKEN)
    s, r, _ = req("POST", "/wp-json/" + NS + "/v1/apply", payload, timeout=180)
    return must(s, r, what)


def bridge_up():
    global BR
    s, c = snip("POST", "", {"name": f"x-tmp-h256r-ops-{int(time.time())}", "code": BRIDGE, "scope": "global", "active": False})
    must(s, c, "bridge create")
    BR = c["id"]
    must(*snip("PUT", f"/{BR}/activate", {}), "bridge activate")
    for _ in range(12):
        s, r, _ = req("POST", "/wp-json/" + NS + "/v1/apply", {"token": TOKEN, "head": 1})
        if s == 200:
            print("[bridge] up, id", BR, "| plugin", r.get("head"), "| PHP", r.get("php"))
            return
        time.sleep(1.5)
    raise SystemExit("FATAL: the bridge route never answered")


def bridge_down():
    if BR is None:
        return
    a = snip("PUT", f"/{BR}/deactivate", {})[0]
    d = snip("DELETE", f"/{BR}", None)[0]
    time.sleep(1.5)
    s2, _, _ = req("POST", "/wp-json/" + NS + "/v1/apply", {"token": TOKEN})
    print(f"[bridge] deactivate {a}, delete {d}; route now {s2} (want 404)")
    if s2 != 404:
        print("[bridge] WARNING: the bridge route still answers; delete snippet", BR, "by hand")
    return s2


# ---------------------------------------------------------------- snippets
def snippets():
    s, lst = snip("GET", "")
    return must(s, lst, "snippet list")


def find_engine(lst):
    rows = [x for x in lst if x.get("name") == "x-broker-drop"]
    if len(rows) != 1:
        raise SystemExit(f"FATAL: {len(rows)} snippets named x-broker-drop")
    return int(rows[0]["id"])


def read_snippet(sid):
    s, x = snip("GET", f"/{sid}")
    x = must(s, x, f"snippet {sid}")
    return x


def write_snippet(sid, name, code, want_sha, label):
    must(*snip("PUT", f"/{sid}", {"name": name, "code": code, "scope": "global", "active": False}), f"{label} update")
    must(*snip("PUT", f"/{sid}/activate", {}), f"{label} activate")
    x = read_snippet(sid)
    got = sha(lf(x.get("code")))
    if got != want_sha or not x.get("active"):
        raise SystemExit(f"FATAL: {label} after the write is {got[:12]} active={x.get('active')}, want {want_sha[:12]} active")
    print(f"[write] {label} (snippet {sid}): {got[:12]}, active, read back")


# ---------------------------------------------------------------- the check strings (RELEASE.md)
V = R.OWNER_VERSION
NEED_PL = ['id="nlj-app"', f'data-v="{V}"', '<style id="nlj-css">', '<script id="nlj-js">', '"engine":true', f'"v":"{V}"',
           'id="nlhp-top"', 'class="nlpc-site-footer"', 'id="nlcta"', 'id="nla11y-btn"']
NEVER_PL = ['id="nlow-gate"', "nlowg-go", '"engine":false', "nadlan-pwiz", "nlj-test", "nlj_fault", "NLJ_VARIANT", "had256probe", ">nl-drop-", "Fatal error"]
V202 = tuple(int(x) for x in V.split(".")) >= (2, 0, 2)
if V202:
    NEVER_PL.append('class="nlpub-how"')   # 2.0.2: one "how it works" box, the journey's own
OLD_PAR = "עם כפתורי וואטסאפ וחיוג אליכם"   # the promise 2.0 does not keep (the phone only with consent)
CHECKS = [
    ("/post-listing/", NEED_PL + ['dir="rtl" lang="he" data-v=', '<h1 class="wp-block-heading">פרסום נכס למכירה או להשכרה, בחינם</h1>'],
     NEVER_PL + ([OLD_PAR] if V202 and PAGE in ("A", "B") else [])),   # before 2.0.2 the plugin's own box still says it (rehearsal R5)
    ("/post-listing/?lang=en", NEED_PL + ['dir="ltr" lang="en" data-v=', '"lang":"en"'] + (['<div class="nlj-shell" lang="en" dir="ltr"><h1 class="wp-block-heading">List your property for sale or rent, free</h1>'] if V202 else []),
     NEVER_PL + ([OLD_PAR] if V202 else [])),
]
if PAGE == "B":
    CHECKS[0][1].append("בלי עמלה ובלי כרטיס אשראי. הטלפון שלכם מופיע במודעה רק אם תבחרו לפרסם אותו.")
if PAGE in ("A", "B") and hasattr(R, "META_NEW"):
    CHECKS[0][1].append(f'<meta name="description" content="{R.META_NEW}"')   # Yoast prints the page's new description
if not BENCH:
    CHECKS[0][1].append("<meta name='robots' content='index, follow")   # indexing is the owner's: unchanged
if FAIL_CHECK:
    CHECKS[0][1].append("had256-rehearsal-this-string-is-never-on-the-page")
BROKER_PATHS = [] if BENCH else ["/brokers/meital-katzir/", "/en/brokers/meital-katzir/"]
LISTING = None if BENCH else ("/properties/nofei-yam-3-rooms-balcony-for-rent/", ["3 חדרים עם מרפסת של 20 מ״ר ו-2 חניות, נופי ים", "wa.me/972523631582"],
                               [r'class="(?:[^"]*\s)?nlx-plate(?:\s[^"]*)?"'])   # the class token (main, 6.10: the live attribute carries more names)


def body_of(html):
    return html.split("<body", 1)[-1]


def broker_counts(tag):
    out = {}
    for p in BROKER_PATHS:
        s, html = get_page(p, tag)
        out[p] = (s, body_of(html).count('class="nlb-lcard"'), len(re.findall(r"<h1[ >]", body_of(html))))
    return out


def run_checks(tag, cards_before):
    bad = []
    for path, need, never in CHECKS:
        s, html = get_page(path, tag)
        b = body_of(html)
        miss = [x for x in need if x not in html]
        hit = [x for x in never if x in html]
        h1 = len(re.findall(r"<h1[ >]", b))
        ok = s == 200 and not miss and not hit and h1 == 1 and "Warning:" not in b[:4000]
        print(f"[check] {'OK ' if ok else 'BAD'} {path} ({'busted' if tag else 'plain'}): {s}, h1 {h1}" + (f", missing {miss}" if miss else "") + (f", found {hit}" if hit else ""))
        if not ok:
            bad.append(path)
    for p, (s, n, h1) in broker_counts(tag).items():
        want = cards_before.get(p, (None, None))[1]
        ok = s == 200 and n == want and h1 == 1
        print(f"[check] {'OK ' if ok else 'BAD'} {p}: {s}, {n} listing cards (before {want}), h1 {h1}")
        if not ok:
            bad.append(p)
    if LISTING:
        s, html = get_page(LISTING[0], tag)
        miss = [x for x in LISTING[1] if x not in html] + [x for x in LISTING[2] if not re.search(x, html)]
        ok = s == 200 and not miss and len(re.findall(r"<h1[ >]", body_of(html))) == 1 and "Fatal error" not in html and ">nl-drop-" not in html
        print(f"[check] {'OK ' if ok else 'BAD'} {LISTING[0]}: {s}" + (f", missing {miss}" if miss else ""))
        if not ok:
            bad.append(LISTING[0])
    s, hc = get_json("/wp-json/nadlan/v1/healthcheck" + ("?nlv=" + tag if tag else ""))
    ow, bd = (hc or {}).get("owner_wizard") or {}, (hc or {}).get("broker_drop") or {}
    ok = s == 200 and ow.get("version") == V and ow.get("engine") is True and ow.get("sealed") is True and bd.get("version") == R.BROKER_VERSION
    print(f"[check] {'OK ' if ok else 'BAD'} healthcheck: owner {ow.get('version')} engine {ow.get('engine')} sealed {ow.get('sealed')}, engine {bd.get('version')}")
    if not ok:
        bad.append("healthcheck")
    for method, path, want in (("POST", "/wp-json/nadlan/v1/listing-submit", 410), ("POST", "/wp-json/nadlan/v1/owner/draft", 401), ("GET", "/drop/000000000000000000000000/", 404)):
        r = net(lambda: req(method, path, {} if method == "POST" else None, auth=False, raw=True), method + " " + path)
        s = 0 if r is None else r[0]
        print(f"[check] {'OK ' if s == want else 'BAD'} {method} {path}: {s} (want {want})")
        if s != want:
            bad.append(path)
    return bad


def rollback_checks(tag, cards_before):
    bad = []
    s, html = get_page("/post-listing/", tag)
    gate, app = 'id="nlow-gate"' in html, 'id="nlj-app"' in html
    ok = s == 200 and gate and not app and "Fatal error" not in html
    print(f"[rollback-check] {'OK ' if ok else 'BAD'} /post-listing/: {s}, the 1.0 gate {gate}, the 2.0 app {app}")
    if not ok:
        bad.append("/post-listing/")
    for p, (s, n, h1) in broker_counts(tag).items():
        want = cards_before.get(p, (None, None))[1]
        ok = s == 200 and n == want
        print(f"[rollback-check] {'OK ' if ok else 'BAD'} {p}: {s}, {n} cards (before {want})")
        if not ok:
            bad.append(p)
    s, hc = get_json("/wp-json/nadlan/v1/healthcheck?nlv=" + tag)
    print(f"[rollback-check] healthcheck: {s}, owner {((hc or {}).get('owner_wizard') or {}).get('version')}, engine {((hc or {}).get('broker_drop') or {}).get('version')}")
    return bad


def restore(backup, page_written):
    """707 first (2.0 never runs on the 1.1.3 engine), then the engine, then the page."""
    meta = json.load(open(os.path.join(backup, "snippets.json"), encoding="utf-8"))
    for key in ("owner", "engine"):
        m = meta[key]
        code = io.open(os.path.join(backup, m["file"]), encoding="utf-8", newline="").read()
        if sha(code) != m["sha256_raw"]:
            if sha(lf(code)) != m["sha256_lf"]:   # a checkout may have turned LF into CRLF (core.autocrlf): the LF text is the body
                raise SystemExit(f"FATAL: the backup {m['file']} is not the saved body")
            code = lf(code)
        must(*snip("PUT", f"/{m['id']}", {"name": m["name"], "code": code, "scope": m.get("scope") or "global", "active": False}), f"restore {m['name']}")
        if m.get("active"):
            must(*snip("PUT", f"/{m['id']}/activate", {}), f"reactivate {m['name']}")
        x = read_snippet(m["id"])
        print(f"[restore] {m['name']} (snippet {m['id']}): {sha(lf(x.get('code')))[:12]} (saved {m['sha256_lf'][:12]}), active {x.get('active')}")
    yf = os.path.join(backup, "yoast-4958.json")
    if page_written and os.path.exists(yf):
        saved = json.load(open(yf, encoding="utf-8"))
        cur = ops({"ymeta": {"path": R.PAGE_PATH, "get": list(saved["vals"])}}, "yoast read")["ymeta"]["vals"]
        for k, v in saved["vals"].items():
            if not v.get("exists") or cur.get(k, {}).get("sha") == v["sha"]:
                continue
            r = ops({"ymeta": {"path": R.PAGE_PATH, "set": k, "force": 1, "b64": v["b64"], "sha": v["sha"]}}, "yoast restore " + k)["ymeta"]
            print(f"[restore] page {r['id']} {k}: {r['sha'][:12]} (saved {v['sha'][:12]})")
    pf = os.path.join(backup, "page-4958.html")
    if page_written and os.path.exists(pf):
        old = open(pf, "rb").read()
        cur = ops({"page": {"path": R.PAGE_PATH, "get": 1}}, "page read")["page"]
        if cur["sha"] == sha(old):
            print(f"[restore] page {cur['id']}: already the saved text {sha(old)[:12]}")
        else:
            r = ops({"page": {"path": R.PAGE_PATH, "force": 1, "b64": base64.b64encode(old).decode(), "sha": sha(old)}}, "page restore")["page"]
            print(f"[restore] page {r['id']}: {r['sha'][:12]} (saved {sha(old)[:12]})")


def _stop(signum, frame):
    raise KeyboardInterrupt(f"signal {signum}")


for _sg in ("SIGTERM", "SIGBREAK"):
    if hasattr(signal, _sg):
        try:
            signal.signal(getattr(signal, _sg), _stop)
        except Exception:
            pass


# ---------------------------------------------------------------- 1. the release lock line + live health (its own step)
def step_lock_health():
    if BENCH:
        lock = arg("--bench-lock")
    else:
        common = subprocess.run(["git", "-C", REPO, "rev-parse", "--path-format=absolute", "--git-common-dir"], capture_output=True, text=True).stdout.strip()
        lock = os.path.join(os.path.dirname(common), "docs", "coordination", "claude-codex.md")
    if lock:
        lines = [x.rstrip("\n") for x in io.open(lock, encoding="utf-8") if x.startswith("RELEASE ")]
        last = lines[-1] if lines else ""
        print("[lock]", lock)
        print("[lock] last line:", last[:220])
        if not (last.startswith("RELEASE DONE") or "ROLLED BACK" in last.upper()):
            raise SystemExit("FATAL: the last RELEASE line is not DONE / ROLLED BACK: another release is in flight")
    else:
        print("[lock] bench rehearsal without a lock file")
    if os.path.exists(RESULT) and not BENCH and not ROLLBACK_DIR:
        st = str(json.load(open(RESULT, encoding="utf-8")).get("state", ""))
        if st.startswith("writing") or st.startswith("written") or st.startswith("checking"):
            raise SystemExit(f"FATAL: this release's own record says '{st}': finish or roll it back (--rollback <backup dir>) first")
    s, h, _ = req("GET", "/wp-json/nadlan/v1/health", auth=False)
    must(s, h, "health")
    print("[health]", h.get("version"), h.get("status"))
    if h.get("status") != "ok":
        if not BENCH:
            raise SystemExit("FATAL: live health is not ok")
        print("[health] the bench reports", h.get("status"), "(no payment / mail services on a bench): accepted for the rehearsal only")
    other = [x for x in snippets() if re.match(r"x-tmp-[a-z0-9]+-ops-", str(x.get("name", ""))) and x.get("active")]
    if other:
        raise SystemExit("FATAL: another release bridge is active: " + ", ".join(f"{x['id']} {x['name']}" for x in other))
    print(f"[lock] lines for docs/coordination/claude-codex.md: RELEASE IN PROGRESS HAD-256 x-owner-wizard {V} + x-broker-drop {R.BROKER_VERSION} (page {PAGE}) by <session> start <time>")
    return h.get("version")


# ---------------------------------------------------------------- the run
def main():
    live_ver = step_lock_health()
    if ROLLBACK_DIR:
        return do_rollback(ROLLBACK_DIR)
    # 2. read and gate
    lst = snippets()
    eng_id = find_engine(lst)
    own, eng = read_snippet(R.SNIPPET_707), read_snippet(eng_id)
    if own.get("name") != "x-owner-wizard":
        raise SystemExit(f"FATAL: snippet {R.SNIPPET_707} is named {own.get('name')!r}, not x-owner-wizard")
    own_code, eng_code = own.get("code") or "", eng.get("code") or ""
    own_sha, eng_sha = sha(lf(own_code)), sha(lf(eng_code))
    print(f"[read] 707 x-owner-wizard {own_sha[:12]} active {own.get('active')} | {eng_id} x-broker-drop {eng_sha[:12]} active {eng.get('active')}")
    if own_sha == R.OWNER_LIVE_SHA256 and eng_sha == R.BROKER_NEW_SHA256:
        print("[read] both snippets already carry this package: nothing to do")
        return 0
    if own_sha != R.OWNER_BASE_SHA256 or eng_sha != R.BROKER_BASE_SHA256 or not own.get("active") or not eng.get("active"):
        raise SystemExit(f"FATAL: not the expected bases (707 want {R.OWNER_BASE_SHA256[:12]}, x-broker-drop want {R.BROKER_BASE_SHA256[:12]}, both active)")
    # 3. the backup, before anything else
    backup = os.path.join(QA, "live-backup", UTC + ("-bench" if BENCH else ""))
    os.makedirs(backup, exist_ok=False)
    ga = os.path.join(QA, "live-backup", ".gitattributes")
    if not os.path.exists(ga):   # the saved bodies stay byte for byte in git (no end-of-line conversion)
        open(ga, "w", encoding="utf-8").write("* -text" + chr(10))
    for x, fn in ((own, "x-owner-wizard-707.code.txt"), (eng, f"x-broker-drop-{eng_id}.code.txt")):
        io.open(os.path.join(backup, fn), "w", encoding="utf-8", newline="").write(x.get("code") or "")
    json.dump({"owner": {"id": R.SNIPPET_707, "name": own.get("name"), "active": bool(own.get("active")), "scope": own.get("scope"), "file": "x-owner-wizard-707.code.txt", "sha256_raw": sha(own_code), "sha256_lf": own_sha},
               "engine": {"id": eng_id, "name": eng.get("name"), "active": bool(eng.get("active")), "scope": eng.get("scope"), "file": f"x-broker-drop-{eng_id}.code.txt", "sha256_raw": sha(eng_code), "sha256_lf": eng_sha},
               "read_at_utc": UTC, "base": BASE, "plugin": live_ver}, open(os.path.join(backup, "snippets.json"), "w", encoding="utf-8"), indent=2)
    print("[backup]", os.path.relpath(backup, REPO))
    record("backed up" if not DRY else "dry: backed up", backup=os.path.relpath(backup, REPO))
    # 4. the package, linted here and on the server
    new_eng = R.apply("snippet:x-broker-drop", lf(eng_code))
    new_own = R.apply("snippet:x-owner-wizard", lf(own_code))
    if sha(new_eng) != R.BROKER_NEW_SHA256 or sha(new_own) != R.OWNER_LIVE_SHA256:
        raise SystemExit("FATAL: the built bodies are not the pinned package")
    php_lint_local(new_eng, "x-broker-drop " + R.BROKER_VERSION)
    php_lint_local(new_own, "x-owner-wizard " + V)
    cards_before = broker_counts(str(int(time.time())))
    print("[before] broker pages:", cards_before)
    bridge_up()
    try:
        print("[lint] server x-broker-drop:", ops({"lint_code": new_eng}, "lint engine")["lint_code"])
        print("[lint] server x-owner-wizard:", ops({"lint_code": new_own}, "lint owner")["lint_code"])
        pg = ops({"page": {"path": R.PAGE_PATH, "get": 1}}, "page read")["page"]
        live_page = base64.b64decode(pg["b64"])
        if not BENCH and pg["id"] != R.PAGE_ID:
            raise SystemExit(f"FATAL: /{R.PAGE_PATH}/ is page {pg['id']}, not {R.PAGE_ID}")
        open(os.path.join(backup, "page-4958.html"), "wb").write(live_page)
        meta_plan = {}
        if PAGE in ("A", "B") and hasattr(R, "META_KEYS") and not (BENCH and "--bench-skip-meta" in ARGS):   # the flag replays 6.10's live run
            ym = ops({"ymeta": {"path": R.PAGE_PATH, "get": list(R.META_KEYS)}}, "yoast read")["ymeta"]
            json.dump({"id": ym["id"], "vals": ym["vals"]}, open(os.path.join(backup, "yoast-4958.json"), "w", encoding="utf-8"), indent=2)
            for k, v in ym["vals"].items():
                txt = base64.b64decode(v["b64"]).decode("utf-8")
                if R.OLD_PROMISE in txt:
                    meta_plan[k] = (v["sha"], R.apply("meta:4958:" + k, txt))   # FATAL unless it is the known old text
            print("[yoast]", {k: (v["sha"][:12], "-> new " + sha(meta_plan[k][1])[:12] if k in meta_plan else ("kept" if v["exists"] else "absent")) for k, v in ym["vals"].items()})
        new_page = None
        if PAGE in ("A", "B"):
            new_page = R.apply("page:4958:" + PAGE, lf(live_page.decode("utf-8"))).encode("utf-8")
            print(f"[page] {pg['id']} live {pg['sha'][:12]} (deploydrop's text {R.PAGE_OLD_SHA256[:12]}) -> variant {PAGE} {sha(new_page)[:12]}")
        # 5. the private folder
        probe = secrets.token_hex(8)
        pd = ops({"privdir": {"make": 0 if DRY else 1, "probe": "" if DRY else probe}}, "private folder")["privdir"]
        print("[private]", json.dumps({k: pd.get(k) for k in ("dir", "exists", "writable", "parent_writable", "inside_abspath", "inside_docroot", "defined_now")}, ensure_ascii=False))
        if pd.get("inside_abspath") or pd.get("inside_docroot"):
            raise SystemExit("FATAL: the private folder is inside the web root")
        if DRY:
            if not (pd.get("exists") and pd.get("writable")) and not pd.get("parent_writable"):
                raise SystemExit("FATAL: the private folder cannot be made (parent not writable)")
        else:
            if not pd.get("writable") or not pd.get("probe_written"):
                raise SystemExit("FATAL: the private folder is not writable")
            reach = []
            for u in pd.get("urls") or []:
                path = u[len(BASE):] if u.startswith(BASE) else None
                if path is None:
                    continue
                s, b, _ = req("GET", path, auth=False, raw=True)
                text = b.decode("utf-8", "replace") if isinstance(b, (bytes, bytearray)) else str(b)
                exposed = probe in text   # the test file's own words in the answer = reachable (a 404 page or a redirect is not)
                print(f"[private] GET {path}: {s}{' EXPOSED' if exposed else ' (not the test file)'}")
                if exposed:
                    reach.append((path, s))
            print("[private] test file removed:", ops({"privdir": {"clean": probe}}, "private clean")["privdir"].get("cleaned"))
            if reach:
                raise SystemExit(f"FATAL: the private folder answers over HTTP: {reach}")
        if DRY:
            record("dry: done", lint="ok", private=pd)
            print("[dry] everything up to the write passed; nothing was written")
            return 0
        # 6. write: the engine first, then 707, then the page. From the first write on, ANY failure (a failed check, a
        #    FATAL, a network error, a stop from outside) restores the saved bodies before the bridge goes down.
        state = {"writing": False, "page": False, "rolled": False}

        def auto_rollback(why):
            if state["rolled"]:
                return
            state["rolled"] = True
            print("[rollback] automatic:", why)
            try:
                restore(backup, state["page"])
                ops({"purge": 1}, "purge after rollback")
                time.sleep(2)
                rb = rollback_checks(str(int(time.time())), cards_before)
            except BaseException as e2:   # keep the record honest when even the rollback cannot finish
                record("ROLLBACK INCOMPLETE", failed=str(why)[:300], rollback_error=str(e2)[:300])
                raise SystemExit(f"RELEASE FAILED AND THE ROLLBACK DID NOT FINISH ({e2}); run --rollback {os.path.relpath(backup, REPO)} by hand")
            record("rolled back (auto)", failed=str(why)[:300], rollback_checks_bad=rb)
            raise SystemExit("RELEASE FAILED, ROLLED BACK" + (" (rollback checks NOT clean: " + ", ".join(rb) + ")" if rb else " (rollback checks clean)"))

        try:
            record("writing", private=pd)
            state["writing"] = True
            write_snippet(eng_id, "x-broker-drop", new_eng, R.BROKER_NEW_SHA256, "x-broker-drop " + R.BROKER_VERSION)
            if CRASH and BENCH:
                raise RuntimeError("rehearsal: a crash right after the engine write")
            write_snippet(R.SNIPPET_707, "x-owner-wizard", new_own, R.OWNER_LIVE_SHA256, "x-owner-wizard " + V)
            for k, (old_sha, new_txt) in meta_plan.items():
                state["page"] = True   # from here the rollback also restores page 4958's Yoast texts and its content
                nb = new_txt.encode("utf-8")
                r = ops({"ymeta": {"path": R.PAGE_PATH, "set": k, "expect": old_sha, "b64": base64.b64encode(nb).decode(), "sha": sha(nb)}}, "yoast write " + k)["ymeta"]
                if r["sha"] != sha(nb):
                    raise SystemExit(f"FATAL: {k} after the write is {r['sha'][:12]}")
                print(f"[write] page {r['id']} {k}: {r['sha'][:12]}")
            if new_page is not None:
                state["page"] = True
                r = ops({"page": {"path": R.PAGE_PATH, "expect": pg["sha"], "b64": base64.b64encode(new_page).decode(), "sha": sha(new_page)}}, "page write")["page"]
                if r["sha"] != sha(new_page):
                    raise SystemExit("FATAL: the page after the write is " + r["sha"][:12])
                print(f"[write] page {r['id']}: {r['sha'][:12]}")
            record("written", page_written=state["page"])
            # 7. purge, 8. checks (cache-busted, then plain), a second chance after another purge, else the rollback
            print("[purge]", ops({"purge": 1}, "purge"))
            time.sleep(2)

            def all_checks():
                # the prelude is live: snippet 707 now defines the folder the runner made and probed
                pd2 = ops({"privdir": {"check": 1}}, "private folder after the write").get("privdir") or {}
                pre = [] if pd2.get("defined_now") == pd.get("dir") else ["private-folder-constant"]
                print(f"[private] NL_OWNER_PRIVATE_DIR now {pd2.get('defined_now')!r} (want {pd.get('dir')!r}){' BAD' if pre else ''}")
                return pre + run_checks(str(int(time.time())), cards_before) + run_checks(None, cards_before)

            bad = all_checks()
            if bad:
                print("[checks] first round:", bad, "- purge and look again")
                ops({"purge": 1}, "purge again")
                time.sleep(4)
                bad = all_checks()
            if bad:
                print("[checks] FAILED:", bad)
                auto_rollback("checks failed: " + ", ".join(bad))
        except BaseException as e:
            if state["writing"] and not state["rolled"]:
                auto_rollback(f"{type(e).__name__}: {e}")
            raise
        record("released", checks="all OK")
        print(f"RELEASE DONE: x-owner-wizard {V} + x-broker-drop {R.BROKER_VERSION}" + (f" + page variant {PAGE}" if state["page"] else "") + "; all checks OK; backup " + os.path.relpath(backup, REPO))
        return 0
    finally:
        bridge_down()


def do_rollback(backup):
    backup = os.path.abspath(backup)
    meta = json.load(open(os.path.join(backup, "snippets.json"), encoding="utf-8"))
    print("[rollback] from", os.path.relpath(backup, REPO), "| saved", meta["owner"]["sha256_lf"][:12], meta["engine"]["sha256_lf"][:12])
    rec = json.load(open(RESULT if not BENCH else RESULT.replace(".json", ".bench.json"), encoding="utf-8")) if os.path.exists(RESULT if not BENCH else RESULT.replace(".json", ".bench.json")) else {}
    REC.update(rec)
    cards = broker_counts(str(int(time.time())))
    bridge_up()
    try:
        restore(backup, page_written=True)   # the page only when it differs from the saved text
        ops({"purge": 1}, "purge after rollback")
        time.sleep(2)
        rb = rollback_checks(str(int(time.time())), cards)
        record("rolled back (--rollback)", rollback_checks_bad=rb)
        print("ROLLED BACK" + (" (checks NOT clean: " + ", ".join(rb) + ")" if rb else " (rollback checks clean)"))
        return 0
    finally:
        bridge_down()


if __name__ == "__main__":
    sys.exit(main())
