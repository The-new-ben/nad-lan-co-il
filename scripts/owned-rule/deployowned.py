# -*- coding: utf-8 -*-
"""A listing with an owner + the professionals directory for brokers (HAD-251, HAD-249; 24.9.2026).

Ships plugin files to the live nadlan-config through a temporary, token-gated ops bridge (Code Snippets),
the pattern of the 1.72.2xx releases:
  - every live file is read first; a full-file swap happens only when the live bytes equal the repo HEAD
    version (nobody changed it live), and the write is compare-and-swap on that md5;
  - nadlan-config.php (shared with other sessions) is patched on the LIVE text by anchors: one module token
    ('property-owner') and the version bump;
  - lint chain: php -l locally on every file, then token_get_all on the server, all before the first write;
  - each live file keeps a .bak-had251 sibling (first write only) and a local copy in the scratchpad;
  - after every write the site is probed; a fatal page or a failed health check restores the .bak files;
  - the bridge is deleted at the end and its route is verified 404.
Also records Meital Katzir's licence check (verified_at on 7833) after a live look-up in the Ministry of
Justice brokers register on data.gov.il.

Usage:
  python deployowned.py             dry run: preflight, both lints, the planned writes; nothing is written
  python deployowned.py --apply     deploy
  python deployowned.py --rollback  put every .bak-had251 back and take the module out of nadlan-config.php
The WordPress app password is decrypted in-process (DPAPI) and never printed.
"""
import base64, ctypes, ctypes.wintypes, hashlib, io, json, os, re, secrets, subprocess, sys, tempfile, time, urllib.parse, urllib.request, urllib.error

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = "https://nad-lan.co.il"
REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
PLUGIN = os.path.join(REPO, "plugins", "nadlan-config")
SECRETS_PATH = r"C:\Users\777\Documents\websites\.codex-secrets\wordpress-app-passwords\nad-lan.co.il.json"
SCRATCH = os.environ.get("NL_SCRATCH") or tempfile.gettempdir()
ARGS = sys.argv[1:]
APPLY = "--apply" in ARGS
ROLLBACK = "--rollback" in ARGS
BAK = ".bak-had251"
# written in this order; the module file first (it is not loaded until nadlan-config.php lists it)
FULL = ["inc/property-owner.php", "inc/catalog-meta.php", "inc/cards-render.php", "inc/claim-prompt.php",
        "inc/breadcrumbs.php", "inc/directory.php", "inc/professional-profile.php"]
NEW_FILES = {"inc/property-owner.php"}
if "--only" in ARGS:   # a follow-up release of some of the files (e.g. --only inc/directory.php); nadlan-config.php gets the version bump
    FULL = [f for f in ARGS[ARGS.index("--only") + 1].split(",") if f in FULL]
MAIN = "nadlan-config.php"
MEITAL = 7833
LICENCE = "3131540"
REGISTER = "a0f56034-88db-4132-8803-854bcdb01ca1"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36 NadLan-Owned/1.0"


class DATA_BLOB(ctypes.Structure):
    _fields_ = [("cbData", ctypes.wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]


def dpapi(b64):
    raw = base64.b64decode(b64)
    bi = DATA_BLOB(len(raw), ctypes.cast(ctypes.create_string_buffer(raw, len(raw)), ctypes.POINTER(ctypes.c_char)))
    bo = DATA_BLOB()
    if not ctypes.windll.crypt32.CryptUnprotectData(ctypes.byref(bi), None, None, None, None, 0, ctypes.byref(bo)):
        raise RuntimeError("DPAPI")
    try:
        return ctypes.string_at(bo.pbData, bo.cbData).decode("utf-8")
    finally:
        ctypes.windll.kernel32.LocalFree(bo.pbData)


with open(SECRETS_PATH, encoding="utf-8-sig") as f:
    _sec = json.load(f)
AUTH = "Basic " + base64.b64encode(f"{_sec['username']}:{dpapi(_sec['password_dpapi'])}".encode()).decode()
del _sec


def req(method, path, body=None, timeout=180, raw=False, auth=True):
    data = None if body is None else json.dumps(body, ensure_ascii=False).encode()
    r = urllib.request.Request(BASE + path, data=data, method=method)
    if auth:
        r.add_header("Authorization", AUTH)
    r.add_header("User-Agent", UA)
    if body is not None:
        r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            p = resp.read()
            return resp.status, (p if raw else json.loads(p.decode() or "null"))
    except urllib.error.HTTPError as e:
        p = e.read()
        if raw:
            return e.code, p
        try:
            return e.code, json.loads(p.decode())
        except Exception:
            return e.code, {"raw": p[:300].decode("utf-8", "replace")}


def must(s, p, what, ok=(200, 201)):
    if s not in ok:
        raise SystemExit(f"FATAL {what}: HTTP {s}: {json.dumps(p, ensure_ascii=False)[:600]}")
    return p


def snip(method, path, body=None):
    return req(method, "/wp-json/code-snippets/v1/snippets" + path, body)


def lf(b):
    return b.replace(b"\r\n", b"\n")


def md5(b):
    return hashlib.md5(b).hexdigest()


def head_bytes(rel):
    p = subprocess.run(["git", "-C", REPO, "show", "HEAD:plugins/nadlan-config/" + rel], capture_output=True)
    return lf(p.stdout) if p.returncode == 0 else None


def local_lint(rel, data):
    fd, tmp = tempfile.mkstemp(suffix=".php")
    os.write(fd, data)
    os.close(fd)
    try:
        r = subprocess.run(["php", "-l", tmp], capture_output=True, text=True)
        return r.returncode == 0, (r.stdout + r.stderr).strip().replace(tmp, rel)
    finally:
        os.unlink(tmp)


def page(path):
    sep = "&" if "?" in path else "?"
    s, b = req("GET", path + sep + "nlv=%d" % int(time.time() * 1000), raw=True, auth=False, timeout=120)
    return s, (b.decode("utf-8", "replace") if isinstance(b, (bytes, bytearray)) else "")


def site_ok(tag):
    """A write is kept only while the site answers: health 200/ok and three real pages without a fatal."""
    s, h = req("GET", "/wp-json/nadlan/v1/health?nlv=%d" % time.time(), auth=False)
    bad = []
    if s != 200 or not isinstance(h, dict) or h.get("status") != "ok":
        bad.append(f"health {s}")
    for path in ("/properties/tzukei-aviv-3-rooms-berlin-for-sale/", "/professionals/meital-katzir/", "/professionals/"):
        st, t = page(path)
        if st != 200 or "critical error" in t or "Fatal error" in t or "Parse error" in t:
            bad.append(f"{path} {st}")
    print(f"   probe after {tag}: {'ok' if not bad else 'FAIL ' + ', '.join(bad)}")
    return not bad


# ------------------------------------------------------------------ preflight
s, h = req("GET", "/wp-json/nadlan/v1/health?nlv=%d" % time.time(), auth=False)
must(s, h, "health")
LIVE_VER = h["version"]
print("live:", LIVE_VER, h["status"])
m = re.match(r"^(\d+)\.(\d+)\.(\d+)$", LIVE_VER)
NEW_VER = f"{m.group(1)}.{m.group(2)}.{int(m.group(3)) + 1}"

TOKEN = secrets.token_hex(24)
BRIDGE = r'''
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-owned-ops/v1', '/apply', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( isset( $b['token'] ) ? $b['token'] : '' ) ) ) {
				return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) );
			}
			$root = WP_PLUGIN_DIR . '/nadlan-config/';
			$safe = function ( $rel ) use ( $root ) {
				$rel = (string) $rel;
				if ( ! preg_match( '#^(inc/)?[a-z0-9\-]+\.php$#', $rel ) ) { return ''; }
				return $root . $rel;
			};
			$out = array();
			if ( ! empty( $b['get'] ) ) {
				foreach ( (array) $b['get'] as $rel ) {
					$p = $safe( $rel );
					if ( '' === $p ) { return new WP_Error( 'path', (string) $rel, array( 'status' => 400 ) ); }
					if ( ! file_exists( $p ) ) { $out['get'][ $rel ] = null; continue; }
					$data = file_get_contents( $p );
					$out['get'][ $rel ] = array( 'b64' => base64_encode( $data ), 'md5' => md5( $data ), 'bak' => file_exists( $p . '__BAK__' ) );
				}
			}
			if ( ! empty( $b['lint'] ) ) {
				foreach ( (array) $b['lint'] as $rel => $b64 ) {
					$data = base64_decode( (string) $b64, true );
					try { token_get_all( $data, TOKEN_PARSE ); $out['lint'][ $rel ] = 'ok ' . PHP_VERSION; }
					catch ( ParseError $e ) { return new WP_Error( 'lint', $rel . ': ' . $e->getMessage() . ' line ' . $e->getLine(), array( 'status' => 400 ) ); }
				}
			}
			if ( ! empty( $b['put'] ) && is_array( $b['put'] ) ) {
				$rel  = (string) $b['put']['rel'];
				$p    = $safe( $rel );
				$data = base64_decode( (string) $b['put']['b64'], true );
				if ( '' === $p || false === $data ) { return new WP_Error( 'bad', $rel, array( 'status' => 400 ) ); }
				if ( md5( $data ) !== strtolower( (string) $b['put']['md5'] ) ) { return new WP_Error( 'md5', 'payload', array( 'status' => 400 ) ); }
				$cur = file_exists( $p ) ? md5_file( $p ) : '';
				if ( $cur !== (string) $b['put']['expect'] ) { return new WP_Error( 'changed', $rel . ' changed live: ' . $cur, array( 'status' => 409 ) ); }
				try { token_get_all( $data, TOKEN_PARSE ); } catch ( ParseError $e ) { return new WP_Error( 'lint', $e->getMessage(), array( 'status' => 400 ) ); }
				if ( file_exists( $p ) && ! file_exists( $p . '__BAK__' ) ) { copy( $p, $p . '__BAK__' ); }
				$w = file_put_contents( $p, $data, LOCK_EX );
				if ( false === $w ) { return new WP_Error( 'write', $rel, array( 'status' => 500 ) ); }
				if ( function_exists( 'opcache_invalidate' ) ) { opcache_invalidate( $p, true ); }
				$out['put'] = array( 'rel' => $rel, 'bytes' => $w, 'md5' => md5_file( $p ), 'bak' => file_exists( $p . '__BAK__' ) );
			}
			if ( ! empty( $b['restore'] ) ) {
				foreach ( (array) $b['restore'] as $rel ) {
					$p = $safe( $rel );
					if ( '' === $p ) { continue; }
					if ( file_exists( $p . '__BAK__' ) ) {
						copy( $p . '__BAK__', $p );
						if ( function_exists( 'opcache_invalidate' ) ) { opcache_invalidate( $p, true ); }
						$out['restore'][ $rel ] = 'from bak ' . md5_file( $p );
					} else {
						$out['restore'][ $rel ] = 'no bak';
					}
				}
			}
			if ( ! empty( $b['meta'] ) ) {
				foreach ( (array) $b['meta'] as $row ) {
					$pid = (int) $row['id'];
					if ( 'nadlan_professional' !== get_post_type( $pid ) ) { $out['meta'][ $pid ] = 'not a professional'; continue; }
					foreach ( (array) $row['set'] as $k => $v ) {
						if ( ! in_array( $k, array( 'verified_at', 'nl_verified_via' ), true ) ) { continue; }
						update_post_meta( $pid, $k, 'verified_at' === $k ? (int) $v : wp_slash( (string) $v ) );
					}
					$out['meta'][ $pid ] = array( 'verified_at' => (int) get_post_meta( $pid, 'verified_at', true ), 'via' => get_post_meta( $pid, 'nl_verified_via', true ) );
				}
			}
			if ( ! empty( $b['purge'] ) ) {
				do_action( 'litespeed_purge_all' );
				wp_cache_flush();
				delete_transient( 'nadlan_dir_sources_v1' );
				delete_transient( 'nadlan_dir_facets_v1' );
				$out['purged'] = 1;
			}
			return $out;
		},
	) );
} );
'''.replace("__TOKEN__", TOKEN).replace("__BAK__", BAK)

s, c = snip("POST", "", {"name": f"tmp-owned-ops-{int(time.time())}", "code": "/* placeholder */", "scope": "global", "active": False})
must(s, c, "bridge create")
BR = c["id"]
backup_dir = os.path.join(SCRATCH, "live-backup-had251-" + time.strftime("%Y%m%d-%H%M%S"))
try:
    must(*snip("PUT", f"/{BR}", {"name": c["name"], "code": BRIDGE, "scope": "global", "active": False}), "bridge code")
    must(*snip("PUT", f"/{BR}/activate", {}), "bridge activate")

    def ops(payload, what, ok=(200, 201)):
        payload["token"] = TOKEN
        s, r = req("POST", "/wp-json/nadlan-owned-ops/v1/apply", payload, timeout=240)
        return must(s, r, what, ok)

    if ROLLBACK:
        r = ops({"restore": [MAIN] + FULL[::-1], "purge": 1}, "restore")
        print(json.dumps(r.get("restore"), ensure_ascii=False, indent=1))
        raise SystemExit(0)

    live = ops({"get": FULL + [MAIN]}, "get")["get"]
    os.makedirs(backup_dir, exist_ok=True)
    plan = {}
    for rel in FULL:
        cur = live.get(rel)
        cur_b = base64.b64decode(cur["b64"]) if cur else None
        if cur_b is not None:
            open(os.path.join(backup_dir, rel.replace("/", "__")), "wb").write(cur_b)
        new_b = lf(open(os.path.join(PLUGIN, rel.replace("/", os.sep)), "rb").read())
        if rel in NEW_FILES:
            if cur is not None and md5(cur_b) != md5(new_b):
                raise SystemExit(f"STOP {rel}: already exists live with other content ({md5(cur_b)[:10]})")
            plan[rel] = (new_b, "" if cur is None else md5(cur_b))
            print(f"{rel:32s} new file ({len(new_b)} bytes){' (already live, identical)' if cur is not None else ''}")
            continue
        hb = head_bytes(rel)
        if cur_b is None or hb is None:
            raise SystemExit(f"STOP {rel}: missing live or in HEAD")
        if md5(lf(cur_b)) != md5(hb):
            raise SystemExit(f"STOP {rel}: the live file is not the repo HEAD version (live {md5(cur_b)[:10]}, HEAD {md5(hb)[:10]}). Someone changed it; rebase first.")
        plan[rel] = (new_b, md5(cur_b))
        print(f"{rel:32s} live == HEAD {md5(cur_b)[:10]} -> new {md5(new_b)[:10]} ({len(new_b) - len(cur_b):+d} bytes)")

    # nadlan-config.php: anchors on the live text (another session may have shipped its own module token)
    main_b = base64.b64decode(live[MAIN]["b64"])
    open(os.path.join(backup_dir, MAIN), "wb").write(main_b)
    t = main_b.decode("utf-8")
    edits = [("'property-showroom', 'property-wizard'", "'property-showroom', 'property-owner', 'property-wizard'"),
             (" * Version: " + LIVE_VER + "\n", " * Version: " + NEW_VER + "\n"),
             ("define( 'NADLAN_CONFIG_VERSION', '" + LIVE_VER + "' )", "define( 'NADLAN_CONFIG_VERSION', '" + NEW_VER + "' )")]
    if "'property-owner'" in t:
        edits = edits[1:]
    for old, new in edits:
        n = t.count(old)
        if n != 1:
            raise SystemExit(f"STOP nadlan-config.php anchor found {n} times: {old[:70]!r}")
        t = t.replace(old, new)
    plan[MAIN] = (t.encode("utf-8"), md5(main_b))
    print(f"{MAIN:32s} live {md5(main_b)[:10]} -> module token + version {LIVE_VER} -> {NEW_VER}")

    # lint chain: local first, then the server's own PHP, all before the first write
    for rel, (b, _) in plan.items():
        ok, msg = local_lint(rel, b)
        if not ok:
            raise SystemExit("STOP local lint: " + msg)
    print("local lint: all", len(plan), "files clean (php", subprocess.run(["php", "-r", "echo PHP_VERSION;"], capture_output=True, text=True).stdout + ")")
    r = ops({"lint": {rel: base64.b64encode(b).decode() for rel, (b, _) in plan.items()}}, "server lint")
    print("server lint:", sorted(set(r["lint"].values())))
    print("local copies of the live files:", backup_dir)

    if not APPLY:
        print("DRY RUN: nothing written. Add --apply to deploy.")
        raise SystemExit(0)

    # Meital's licence: a live look-up in the brokers register, then the check is recorded (no post re-save, no ping)
    url = "https://data.gov.il/api/3/action/datastore_search?" + urllib.parse.urlencode({"resource_id": REGISTER, "q": LICENCE, "limit": 5})
    reg = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 nad-lan-licence-check"}), timeout=60))
    hits = [x for x in reg.get("result", {}).get("records", []) if str(x.get("מס רשיון")) == LICENCE and "קציר" in str(x.get("שם המתווך")) and "מיטל" in str(x.get("שם המתווך"))]
    if hits:
        via = "data.gov.il metavhim %s record %s: %s, %s, checked %s" % (REGISTER[:8], hits[0].get("_id"), hits[0].get("שם המתווך"), hits[0].get("עיר מגורים"), time.strftime("%Y-%m-%d %H:%M"))
        r = ops({"meta": [{"id": MEITAL, "set": {"verified_at": int(time.time()), "nl_verified_via": via}}]}, "meital verified_at")
        print("Meital licence", LICENCE, "found in the register ->", r["meta"])
    else:
        print("Meital licence NOT found in the register: verified_at not written (the badge will not show)")

    written = []
    order = FULL + [MAIN]
    for rel in order:
        b, expect = plan[rel]
        w = ops({"put": {"rel": rel, "b64": base64.b64encode(b).decode(), "md5": md5(b), "expect": expect}}, "put " + rel)["put"]
        written.append(rel)
        print(f"PUT {rel:32s} md5 {w['md5'][:10]} bytes {w['bytes']} bak={w['bak']}")
        time.sleep(1.5)
        if not site_ok(rel):
            print("ROLLBACK: restoring", written[::-1])
            print(json.dumps(ops({"restore": written[::-1], "purge": 1}, "restore").get("restore"), ensure_ascii=False))
            raise SystemExit("DEPLOY FAILED and rolled back")
    ops({"purge": 1}, "purge")
    print("purged")
finally:
    s1, _ = snip("PUT", f"/{BR}/deactivate", {})
    s2, _ = snip("DELETE", f"/{BR}", None)
    s3, _ = req("POST", "/wp-json/nadlan-owned-ops/v1/apply", {"token": "x"})
    print("bridge cleanup", s1, s2, "| route after cleanup:", s3, "(want 404)")

time.sleep(3)
s, h2 = req("GET", "/wp-json/nadlan/v1/health?nlv=%d" % time.time(), auth=False)
print("health after:", s, h2.get("version") if isinstance(h2, dict) else h2, h2.get("status") if isinstance(h2, dict) else "")
