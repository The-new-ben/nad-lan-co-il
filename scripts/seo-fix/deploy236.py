# -*- coding: utf-8 -*-
"""Release 1.72.236 (24.9.2026): the city suffix on the project H1 only for urban-renewal compounds (1.72.235 made Rainbow read "... תל אביב, תל אביב יפו"). Based on deploy235.py.

Release 1.72.235 (24.9.2026): the SEO gaps the full-site crawl found, plus Madlan out of the code strings.

  inc/seo-gaps.php            NEW: professional cards get "{name}: {trade} ב{city} | נדלן" instead of "{name} - נדלן"
                              (2,698 contractor cards), and a description from their register facts; glossary terms and
                              other pages without a description get their own opening sentence. Demo cards untouched.
  inc/bulk-project-seo.php    the city from the imported `city` meta when no city term is set (217 duplicate titles);
                              urban-renewal compounds stop promising prices and apartments: "{name}, {city}: התחדשות
                              עירונית, N יח״ד | נדלן"
  inc/showroom-engine.php     the project H1 carries the city ("יוספטל, רמלה"); a Madlan source line in a seed string
  inc/premium-catalog.php, inc/showroom-support.php, assets/showroom-engine/i18n.js   "מדלן" out of visible strings
  nadlan-config.php           version bump + 'seo-gaps' in the module list, both patched on the LIVE text

Same safety chain as deploy234.py. The app password is decrypted in-process (DPAPI), never printed.
  python scripts/seo-fix/deploy235.py [--dry | --rollback]
"""
import base64, ctypes, ctypes.wintypes, hashlib, io, json, os, re, secrets, subprocess, sys, tempfile, time, urllib.request, urllib.error, zlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = "https://nad-lan.co.il"
REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
QA = os.path.join(REPO, "docs", "qa", "seo-fix-2026-09-24", "r236")
SECRETS_PATH = r"C:\Users\777\Documents\websites\.codex-secrets\wordpress-app-passwords\nad-lan.co.il.json"
ARGS = sys.argv[1:]
DRY = "--dry" in ARGS
BAK = ".bak236"
CRLF, LF = bytes([13, 10]), bytes([10])


class DB(ctypes.Structure):
    _fields_ = [("cb", ctypes.wintypes.DWORD), ("pb", ctypes.POINTER(ctypes.c_char))]


def dpapi(b64):
    raw = base64.b64decode(b64)
    bi = DB(len(raw), ctypes.cast(ctypes.create_string_buffer(raw, len(raw)), ctypes.POINTER(ctypes.c_char)))
    bo = DB()
    if not ctypes.windll.crypt32.CryptUnprotectData(ctypes.byref(bi), None, None, None, None, 0, ctypes.byref(bo)):
        raise RuntimeError("DPAPI")
    try:
        return ctypes.string_at(bo.pb, bo.cb).decode("utf-8")
    finally:
        ctypes.windll.kernel32.LocalFree(bo.pb)


with open(SECRETS_PATH, encoding="utf-8-sig") as f:
    sec = json.load(f)
AUTH = "Basic " + base64.b64encode((sec["username"] + ":" + dpapi(sec["password_dpapi"])).encode()).decode()
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) NadLan-SEO235/1.0"


def req(method, path, body=None, timeout=120, raw=False, auth=True):
    r = urllib.request.Request(BASE + path, data=None if body is None else json.dumps(body, ensure_ascii=False).encode(), method=method)
    if auth:
        r.add_header("Authorization", AUTH)
    r.add_header("User-Agent", UA)
    if body is not None:
        r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            p = resp.read()
            return resp.status, (p if raw else json.loads(p.decode("utf-8") or "null"))
    except urllib.error.HTTPError as e:
        p = e.read()
        if raw:
            return e.code, p
        try:
            return e.code, json.loads(p.decode("utf-8"))
        except Exception:
            return e.code, {"raw": p[:300].decode("utf-8", "replace")}


def must(s, p, what, ok=(200, 201)):
    if s not in ok:
        raise SystemExit(f"FATAL {what}: HTTP {s}: {json.dumps(p, ensure_ascii=False)[:400]}")
    return p


def md5(b):
    return hashlib.md5(b).hexdigest()


def php_lint(data, label):
    with tempfile.NamedTemporaryFile("wb", suffix=".php", delete=False) as t:
        t.write(data)
        tmp = t.name
    try:
        out = subprocess.run(["php", "-l", tmp], capture_output=True, text=True)
    finally:
        os.unlink(tmp)
    if out.returncode != 0:
        raise SystemExit(f"FATAL local lint {label}: {out.stdout.strip()} {out.stderr.strip()}")
    print(f"[lint] {label}: ok")


def git_head(rel):
    out = subprocess.run(["git", "-C", REPO, "show", "HEAD:" + rel.replace(os.sep, "/")], capture_output=True)
    if out.returncode != 0:
        return None
    return out.stdout


# ---------------------------------------------------------------- health + bridge
s, h = req("GET", "/wp-json/nadlan/v1/health", auth=False)
must(s, h, "health")
LIVE_VER = h.get("version")
print("[health]", LIVE_VER, h.get("status"))
if h.get("status") != "ok":
    raise SystemExit("FATAL: live health is not ok before the release")

TOKEN = secrets.token_hex(24)
NS = 'nadlan-seo236-' + TOKEN[:8]  # one route per run: a bridge left over from a failed run can never answer for this one
BRIDGE = r'''
add_action( 'rest_api_init', function () {
	register_rest_route( '__NS__/v1', '/apply', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( $b['token'] ?? '' ) ) ) {
				return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) );
			}
			$root = WP_PLUGIN_DIR . '/nadlan-config/';
			$rel  = function ( $r ) { return ltrim( str_replace( array( '..', '\\' ), array( '', '/' ), (string) $r ), '/' ); };
			$out  = array();
			if ( ! empty( $b['get'] ) ) {
				$p = $root . $rel( $b['get'] );
				if ( ! is_readable( $p ) ) { $out['get'] = array( 'missing' => 1 ); }
				else { $d = file_get_contents( $p ); $out['get'] = array( 'b64' => base64_encode( $d ), 'md5' => md5( $d ) ); }
			}
			if ( ! empty( $b['put'] ) && is_array( $b['put'] ) ) {
				$p = $root . $rel( $b['put']['rel'] );
				$d = base64_decode( (string) $b['put']['b64'], true );
				if ( false !== $d && ! empty( $b['put']['z'] ) ) { $d = @gzuncompress( $d ); }
				if ( false === $d || md5( $d ) !== strtolower( (string) $b['put']['md5'] ) ) { return new WP_Error( 'md5', 'mismatch', array( 'status' => 400 ) ); }
				try { token_get_all( $d, TOKEN_PARSE ); } catch ( ParseError $e ) { return new WP_Error( 'lint', $e->getMessage() . ' line ' . $e->getLine(), array( 'status' => 400 ) ); }
				if ( isset( $b['put']['expect'] ) ) {
					$cur = file_exists( $p ) ? md5_file( $p ) : 'missing';
					if ( $cur !== (string) $b['put']['expect'] ) { return new WP_Error( 'drift', 'live file changed: ' . $cur, array( 'status' => 409 ) ); }
				}
				if ( file_exists( $p ) && ! file_exists( $p . '__BAK__' ) ) { copy( $p, $p . '__BAK__' ); }
				$w = file_put_contents( $p, $d, LOCK_EX );
				clearstatcache( true, $p );
				$out['put'] = array( 'bytes' => $w, 'md5' => md5_file( $p ) );
			}
			if ( ! empty( $b['restore'] ) ) {
				$p = $root . $rel( $b['restore'] );
				if ( file_exists( $p . '__BAK__' ) ) { copy( $p . '__BAK__', $p ); clearstatcache( true, $p ); if ( function_exists( 'opcache_invalidate' ) ) { @opcache_invalidate( $p, true ); } $out['restore'] = md5_file( $p ); } else { $out['restore'] = 'no-bak'; }
			}
			if ( ! empty( $b['unlink'] ) ) {
				$p = $root . $rel( $b['unlink'] );
				$out['unlink'] = file_exists( $p ) ? ( @unlink( $p ) ? 1 : 0 ) : 'missing';
			}
			if ( ! empty( $b['diag'] ) ) {
				$q = '[out:json][timeout:25];(node(around:1200,32.1059,34.7845)[highway=bus_stop];);out tags center 5;';
				$res = array();
				foreach ( array( 'https://overpass-api.de/api/interpreter', 'https://overpass.kumi.systems/api/interpreter', 'https://maps.mail.ru/osm/tools/overpass/api/interpreter' ) as $ep ) {
					$t0 = microtime( true );
					$rr = wp_remote_post( $ep, array( 'timeout' => 14, 'body' => array( 'data' => $q ), 'headers' => array( 'User-Agent' => 'nadlan-config/2.0 (nad-lan.co.il)' ) ) );
					$res[] = array( 'ep' => $ep, 'code' => is_wp_error( $rr ) ? $rr->get_error_message() : wp_remote_retrieve_response_code( $rr ), 'secs' => round( microtime( true ) - $t0, 2 ) );
				}
				$over = 0; $now = time();
				foreach ( (array) _get_cron_array() as $ts => $hooks ) { if ( $ts < $now - 300 ) { $over += count( $hooks ); } }
				$out['diag'] = array( 'overpass' => $res, 'disable_wp_cron' => defined( 'DISABLE_WP_CRON' ) && DISABLE_WP_CRON ? 1 : 0, 'cron_overdue_5min' => $over, 'poi_down' => get_transient( 'nadlan_poi_down' ) ? 1 : 0, 'poi_rate' => (int) get_transient( 'nadlan_poi_rate' ), 'poi_events' => count( array_filter( (array) _get_cron_array(), function ( $h ) { return isset( $h['nadlan_poi_refresh'] ); } ) ) );
			}
			if ( ! empty( $b['head'] ) ) {
				$d = (string) @file_get_contents( $root . 'nadlan-config.php', false, null, 0, 1200 );
				$out['head'] = preg_match( '/Version:\s*([0-9.]+)/', $d, $m ) ? $m[1] : '';
			}
			if ( ! empty( $b['purge'] ) ) {
				if ( function_exists( 'opcache_invalidate' ) ) { foreach ( array( 'inc/seo-gaps.php', 'inc/bulk-project-seo.php', 'inc/showroom-engine.php', 'inc/premium-catalog.php', 'inc/showroom-support.php', 'nadlan-config.php' ) as $f ) { @opcache_invalidate( $root . $f, true ); } }
				if ( function_exists( 'opcache_reset' ) ) { $out['opcache'] = @opcache_reset(); }
				do_action( 'litespeed_purge_all' ); wp_cache_flush(); $out['purged'] = 1;
			}
			return $out;
		},
	) );
} );
'''.replace("__TOKEN__", TOKEN).replace("__BAK__", BAK).replace("__NS__", NS)


def snip(method, path, body=None):
    return req(method, "/wp-json/code-snippets/v1/snippets" + path, body=body)


def ops(payload, what):
    payload["token"] = TOKEN
    s, r = req("POST", "/wp-json/" + NS + "/v1/apply", body=payload, timeout=180)
    return must(s, r, what)


BR = None


def bridge_up():
    global BR
    s, c = snip("POST", "", {"name": f"x-tmp-seo236-ops-{int(time.time())}", "code": BRIDGE, "scope": "global", "active": False})
    must(s, c, "bridge create")
    BR = c["id"]
    must(*snip("PUT", f"/{BR}/activate", {}), "bridge activate")
    for _ in range(10):
        s, r = req("POST", "/wp-json/" + NS + "/v1/apply", body={"token": TOKEN, "head": 1})
        if s == 200:
            print("[bridge] up, id", BR, "| live header version", r.get("head"))
            return
        time.sleep(1.5)
    raise SystemExit("FATAL bridge route never answered")


def bridge_down():
    if BR is None:
        return
    snip("PUT", f"/{BR}/deactivate", {})
    s, _ = snip("DELETE", f"/{BR}", None)
    time.sleep(1.5)
    s2, _ = req("POST", "/wp-json/" + NS + "/v1/apply", body={"token": TOKEN})
    print(f"[bridge] delete http {s}; route now http {s2} (want 404)")


def put(rel, data, expect=None):
    z = zlib.compress(data, 9)
    body = {"put": {"rel": rel, "b64": base64.b64encode(z).decode(), "z": 1, "md5": md5(data)}}
    if expect is not None:
        body["put"]["expect"] = expect
    r = ops(body, f"put {rel}")["put"]
    if r["md5"] != md5(data):
        raise SystemExit(f"FATAL {rel}: server md5 {r['md5']} != local {md5(data)}")
    print(f"[put] {rel}: {r['bytes']} bytes, md5 {r['md5'][:10]} verified")


def live_get(rel):
    return ops({"get": rel}, f"get {rel}")["get"]


def page(path):
    s, b = req("GET", path, raw=True, auth=False, timeout=90)
    return s, b.decode("utf-8", "replace")


def body_of(html):
    i = html.find("<body")
    return html[i:] if i > -1 else html


SLOW_PROJECTS = ["/projects/shikun-binui-sde-dov/"]
YOSEFTAL = "/projects/%D7%99%D7%95%D7%A1%D7%A4%D7%98%D7%9C/"
CHECKS = [
    # path, must be in the raw HTML, must NOT be in the body
    ("/", [], []),
    ("/projects/rainbow-tel-aviv/", ["<h1", ">Rainbow Tel Aviv - ריינבו תל אביב</h1>"], ["ריינבו תל אביב, תל אביב יפו"]),
    ("/projects/h-infinity-somail-tel-aviv/", ["<h1"], []),
    (YOSEFTAL, ["התחדשות עירונית", "יח״ד | נדלן</title>", "מתחם התחדשות עירונית יוספטל"], ["מחירים, דירות ובחירה מהבניין | נדלן</title>"]),
    ("/professionals/%d7%9e%d7%95%d7%99%d7%90%d7%9c-%d7%99%d7%a0%d7%99%d7%91/", ["מויאל יניב: קבלן שיפוצים בניר משה | נדלן</title>", "רשום בפנקס הקבלנים, מספר 33944"], []),
    ("/professionals/meital-katzir/", ["<h1"], []),
    ("/professionals/demo-shira-golan-mortgage/", [], []),
]


def ttfb(path):
    t0 = time.time()
    r = urllib.request.Request(BASE + path + ("&" if "?" in path else "?") + "nlt=" + secrets.token_hex(4), headers={"User-Agent": UA})
    with urllib.request.urlopen(r, timeout=60) as resp:
        resp.read(1)
        first = time.time() - t0
        resp.read()
        return resp.status, round(first, 2)


def speed(label):
    res = {}
    for pth in SLOW_PROJECTS:
        try:
            res[pth] = ttfb(pth)
        except Exception as e:
            res[pth] = ("ERR", str(e)[:80])
        print(f"[speed {label}] {res[pth]} {pth[:60]}")
    return res


def verify_pages(tag):
    bad = []
    for path, need, never in CHECKS:
        sep = "&" if "?" in path else "?"
        try:
            s, html = page(path + sep + "nlv=" + tag)
        except Exception as e:  # a timeout is a failed check, not a crash that skips the rollback
            print(f"[page] BAD --- {path[:70]} {e}")
            bad.append(path)
            continue
        body = body_of(html)
        miss = [n for n in need if n not in html]
        hit = [n for n in never if n in body]
        ok = s == 200 and not miss and not hit and "Fatal error" not in body and "critical error" not in body
        print(f"[page] {'OK ' if ok else 'BAD'} {s} {path[:70]} missing={miss} forbidden={hit}")
        if not ok:
            bad.append(path)
    return bad


def wait_version(want, secs=75):
    t0 = time.time()
    last = None
    while time.time() - t0 < secs:
        try:
            s, h2 = req("GET", "/wp-json/nadlan/v1/health?nlv=" + str(int(time.time())), auth=False)
            last = h2.get("version") if isinstance(h2, dict) else s
            if s == 200 and isinstance(h2, dict) and h2.get("version") == want and h2.get("status") == "ok":
                print(f"[health] {want} ok after {int(time.time() - t0)}s")
                return True
        except Exception as e:
            last = str(e)
        time.sleep(4)
    print(f"[health] still {last} after {secs}s")
    return False


def rollback(created_any):
    print("[rollback] restoring .bak236 files")
    for rel in ("nadlan-config.php", "inc/bulk-project-seo.php"):
        print("  ", rel, ops({"restore": rel}, "restore " + rel).get("restore"))
    ops({"purge": 1}, "purge")


# ---------------------------------------------------------------- main
FILES = ["inc/bulk-project-seo.php"]
NEWFILES = set()
NEW = {rel: open(os.path.join(PLUG, *rel.split("/")), "rb").read() for rel in FILES}
for rel in FILES:
    php_lint(NEW[rel], rel)
HEAD = {rel: git_head("plugins/nadlan-config/" + rel) for rel in FILES}
os.makedirs(os.path.join(QA, "live-backup"), exist_ok=True)

created = False
try:
    s, lst = snip("GET", "")
    for x in (lst if s == 200 and isinstance(lst, list) else []):
        if str(x.get("name", "")).startswith(("x-tmp-seo236-ops-", "x-tmp-had247-ops-")) and x.get("active"):
            print("[sweep] deactivating leftover bridge", x["id"], snip("PUT", f"/{x['id']}/deactivate", {})[0])
    bridge_up()
    before = {}
    if "--rollback" in ARGS:
        rollback(True)
        wait_version(LIVE_VER)
        raise SystemExit(0)

    LIVE = {}
    for rel in FILES:
        cur = live_get(rel)
        if rel in NEWFILES:
            if not cur.get("missing"):
                raise SystemExit("FATAL new file already on the server: " + rel)
            LIVE[rel] = None
            print(f"[drift] {rel}: new file, not on the server yet (ok)")
            continue
        if cur.get("missing"):
            raise SystemExit("FATAL live file missing: " + rel)
        LIVE[rel] = base64.b64decode(cur["b64"])
        print(f"[drift] live {rel} {md5(LIVE[rel])[:10]} vs git HEAD {md5(HEAD[rel])[:10] if HEAD[rel] else '-'}")
        # line endings do not count: git stores LF, a file written on Windows may carry CRLF (24.9: that alone broke the compare)
        # 1.72.235 went live minutes ago and is not committed yet: the live file must be exactly what that release wrote
        prev = json.load(open(os.path.join(REPO, "docs", "qa", "seo-fix-2026-09-24", "deploy-result-235.json"), encoding="utf-8"))["files"].get(rel)
        if md5(LIVE[rel]) != prev and (HEAD[rel] is None or md5(LIVE[rel].replace(CRLF, LF)) != md5(HEAD[rel].replace(CRLF, LF))):
            raise SystemExit(f"FATAL: live {rel} is neither release 235 nor git HEAD; diff it before replacing it")
    cur_main = live_get("nadlan-config.php")
    live_main = base64.b64decode(cur_main["b64"])
    stamp = time.strftime("%Y%m%dT%H%M%S")
    if not DRY:
        for rel in FILES:
            if LIVE[rel] is not None:
                open(os.path.join(QA, "live-backup", rel.split("/")[-1] + f".{stamp}.live"), "wb").write(LIVE[rel])
        open(os.path.join(QA, "live-backup", f"nadlan-config.php.{stamp}.live"), "wb").write(live_main)

    # the version bump, on the live text
    text = live_main.decode("utf-8")
    m = re.search(r"\* Version: (\d+)\.(\d+)\.(\d+)", text)
    old = ".".join(m.groups())
    new = f"{m.group(1)}.{m.group(2)}.{int(m.group(3)) + 1}"
    for a, b2 in ((f" * Version: {old}", f" * Version: {new}"), (f"define( 'NADLAN_CONFIG_VERSION', '{old}' )", f"define( 'NADLAN_CONFIG_VERSION', '{new}' )")):
        n = text.count(a)
        if n != 1:
            raise SystemExit(f"FATAL anchor x{n} in nadlan-config.php: {a}")
        text = text.replace(a, b2)
    new_main = text.encode("utf-8")
    php_lint(new_main, "nadlan-config.php (live text, bumped)")
    print(f"[plan] {old} -> {new}; replacing {', '.join(FILES)}")
    if DRY:
        print("[dry] no writes")
        raise SystemExit(0)

    try:
        created = True
        for rel in FILES:
            put(rel, NEW[rel], expect=("missing" if LIVE[rel] is None else md5(LIVE[rel])))
        put("nadlan-config.php", new_main, expect=md5(live_main))
    except BaseException as e:  # a write refused half way (drift, lint, md5): put everything back
        print("[FAIL] during writes:", e)
        rollback(created)
        raise
    print("[purge]", ops({"purge": 1}, "purge"))

    healthy = wait_version(new)
    bad = verify_pages("seo236" + str(int(time.time()))) if healthy else ["health"]
    after = speed("after") if healthy else {}
    slow_after = [k for k, v in after.items() if not (isinstance(v[1], float) and v[1] < 5)]
    if healthy and slow_after:
        print("[speed] still slow after the release:", slow_after)
    if bad:
        # one more purge and a patient second look before rolling back (OPcache/LiteSpeed lag)
        ops({"purge": 1}, "purge again")
        time.sleep(12)
        healthy = wait_version(new, 45)
        bad = verify_pages("seo236b" + str(int(time.time()))) if healthy else ["health"]
    if bad:
        print("[FAIL] pages:", bad)
        rollback(created)
        wait_version(old, 60)
        raise SystemExit("ROLLED BACK")
    json.dump({"released": new, "from": old, "at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "files": dict({rel: md5(NEW[rel]) for rel in FILES}, **{"nadlan-config.php": md5(new_main)}),
        "live_before": dict({rel: (md5(LIVE[rel]) if LIVE[rel] is not None else "missing") for rel in FILES}, **{"nadlan-config.php": md5(live_main)})},
        open(os.path.join(QA, "deploy-result-236.json"), "w", encoding="utf-8"), indent=2)
    json.dump({"before": before, "after": after}, open(os.path.join(QA, "speed-236.json"), "w", encoding="utf-8"), indent=2)
    print(f"RELEASE {new} LIVE")
finally:
    bridge_down()
