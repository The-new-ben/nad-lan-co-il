# -*- coding: utf-8 -*-
"""HAD-247 follow-up release 1.72.229 (plan and walk-through kept on cottages, lighter hero on phones, walk-through copy). Based on deploy247.py.

HAD-247 release (owner order 17.9.2026, "the 3D on listing pages is sloppy, no hotspots, loads and hammers
the page; smaller, with hotspots, on all pages"): the listing opens with its real photo, the building
illustration loads only on request with markers from the listing's own facts, and every photo opens full screen.

Ships two plugin files plus a version bump, through a temporary token-gated bridge (wordpress-agent-deploy):
  inc/property-gallery.php    new: the photo viewer (loaded from property-showroom.php)
  inc/property-showroom.php   the template: hero photo, on-request illustration, no model-viewer on load
  nadlan-config.php           version X.Y.Z -> X.Y.(Z+1), patched on the LIVE text (header + constant only)

Rules kept: the live property-showroom.php must equal git HEAD before it is replaced (no silent drift); every
replaced file keeps a .bak247 sibling on the server and a copy in docs/qa/had-247-3d-gallery/live-backup/; the
server lints every file before writing it; OPcache reset + LiteSpeed purge; health polled patiently; pages checked;
automatic rollback if health or a page fails; the bridge is deleted at the end (verified 404).
The WordPress app password is decrypted in-process (DPAPI) and never printed.

  python scripts/had-247/deploy247.py            deploy + verify
  python scripts/had-247/deploy247.py --dry      checks only (live md5 vs HEAD, lint), no writes
  python scripts/had-247/deploy247.py --rollback restore the .bak247 files (property-gallery.php stays, unused)
"""
import base64, ctypes, ctypes.wintypes, hashlib, io, json, os, re, secrets, subprocess, sys, tempfile, time, urllib.request, urllib.error, zlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = "https://nad-lan.co.il"
REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
QA = os.path.join(REPO, "docs", "qa", "had-247-3d-gallery")
SECRETS_PATH = r"C:\Users\777\Documents\websites\.codex-secrets\wordpress-app-passwords\nad-lan.co.il.json"
ARGS = sys.argv[1:]
DRY = "--dry" in ARGS
BAK = ".bak229"
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
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) NadLan-HAD247/1.0"


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
NS = 'nadlan-had247-' + TOKEN[:8]  # one route per run: a bridge left over from a failed run can never answer for this one
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
			if ( ! empty( $b['head'] ) ) {
				$d = (string) @file_get_contents( $root . 'nadlan-config.php', false, null, 0, 1200 );
				$out['head'] = preg_match( '/Version:\s*([0-9.]+)/', $d, $m ) ? $m[1] : '';
			}
			if ( ! empty( $b['purge'] ) ) {
				if ( function_exists( 'opcache_invalidate' ) ) { foreach ( array( 'inc/property-showroom.php', 'inc/property-gallery.php', 'inc/interior-fp.php', 'nadlan-config.php' ) as $f ) { @opcache_invalidate( $root . $f, true ); } }
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
    s, c = snip("POST", "", {"name": f"x-tmp-had247-ops-229-{int(time.time())}", "code": BRIDGE, "scope": "global", "active": False})
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


OFAKIM = "/properties/%d7%9c%d7%9e%d7%9b%d7%99%d7%a8%d7%94-%d7%91%d7%90%d7%95%d7%a4%d7%a7%d7%99%d7%9d-%d7%a9%d7%9b%d7%95%d7%a0%d7%aa-%d7%a9%d7%a4%d7%99%d7%a8%d7%90-%d7%a7%d7%95%d7%98%d7%92-5-%d7%97%d7%93%d7%a8%d7%99%d7%9d/"
MV_TAG = re.compile(r"<script[^>]+src=[\"'][^\"']*model-viewer[^\"']*\.js")  # a real script tag, not the data-mv attribute
CHECKS = [
    # path, must be in the page, must NOT be in the body
    # markup only: the class names also sit inside the inline CSS/JS of every listing (the 24.9 false alarm)
    (OFAKIM, ["<figure class=\"nlps-cover\"", "nadlan-pgal-js", "2 כיווני אוויר", "<h2>תוכנית הבית</h2>", "(max-width: 600px) 64vw", "הדמיה להמחשה בלבד, לפי נתוני הדירה", "<section class=\"nlps-facade\""], ["<model-viewer", "nadlan-model-viewer-js", "class=\"nlps-view nlps-view-out", "class=\"nlps-facade-svg\"", "class=\"nlps-view nlps-view-3d\"", "מפה חיה"]),
    ("/properties/bialik-rg-4r-demo/", ["data-has3d=\"1\"", "class=\"nlps-view nlps-view-3d\"", "data-hs=", "nadlan-pgal-js"], ["<model-viewer", "nadlan-model-viewer-js", "מפה חיה"]),
    ("/properties/mazeh-tlv-3r-demo/", ["class=\"nlps-view nlps-view-3d\"", "nadlan-pgal-js"], ["<model-viewer", "nadlan-model-viewer-js"]),
    ("/properties/tzukei-aviv-3-rooms-berlin-for-sale/", ["<article class=\"nlx", "nadlan-pgal-js"], ["<model-viewer", "nadlan-model-viewer-js", "<figure class=\"nlps-cover\"", "class=\"nlps-view nlps-view-3d\""]),
    ("/en/brokers/meital-katzir/tzukei-aviv-3-room-apartment-for-sale/", ["<article class=\"nlx", "nadlan-pgal-js"], ["nadlan-model-viewer-js"]),
    ("/", [], []),
    ("/projects/rainbow-tel-aviv/", [], []),
    ("/projects/h-infinity-somail-tel-aviv/", [], []),
]
LISTING_PATHS = {c[0] for c in CHECKS[:5]}


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
        if path in LISTING_PATHS and MV_TAG.search(body):
            hit.append("model-viewer script tag")
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


def rollback(created_gallery):
    # 24.9.2026 lesson: the rollback that deleted property-gallery.php while OPcache still held the new
    # property-showroom.php (require_once of it) took the site to HTTP 500 for about 2 minutes. Now: restore the old
    # files (each invalidated in OPcache on the spot), reset OPcache, and LEAVE property-gallery.php on disk; an
    # unused file is harmless, a missing required file is an outage.
    print("[rollback] restoring .bak247 files (property-gallery.php stays on disk, unused)")
    for rel in ("inc/property-showroom.php", "inc/interior-fp.php", "nadlan-config.php"):
        print("  ", rel, ops({"restore": rel}, "restore " + rel).get("restore"))
    ops({"purge": 1}, "purge")


# ---------------------------------------------------------------- main
FILES = ["inc/property-showroom.php", "inc/interior-fp.php"]
NEW = {rel: open(os.path.join(PLUG, *rel.split("/")), "rb").read() for rel in FILES}
for rel in FILES:
    php_lint(NEW[rel], rel)
HEAD = {rel: git_head("plugins/nadlan-config/" + rel) for rel in FILES}
os.makedirs(os.path.join(QA, "live-backup"), exist_ok=True)

created = False
try:
    s, lst = snip("GET", "")
    for x in (lst if s == 200 and isinstance(lst, list) else []):
        if str(x.get("name", "")).startswith("x-tmp-had247-ops-") and x.get("active"):
            print("[sweep] deactivating leftover bridge", x["id"], snip("PUT", f"/{x['id']}/deactivate", {})[0])
    bridge_up()
    if "--rollback" in ARGS:
        rollback(True)
        wait_version(LIVE_VER)
        raise SystemExit(0)

    LIVE = {}
    for rel in FILES:
        cur = live_get(rel)
        if cur.get("missing"):
            raise SystemExit("FATAL live file missing: " + rel)
        LIVE[rel] = base64.b64decode(cur["b64"])
        print(f"[drift] live {rel} {md5(LIVE[rel])[:10]} vs git HEAD {md5(HEAD[rel])[:10] if HEAD[rel] else '-'}")
        # line endings do not count: git stores LF, a file written on Windows may carry CRLF (24.9: that alone broke the compare)
        if HEAD[rel] is None or md5(LIVE[rel].replace(CRLF, LF)) != md5(HEAD[rel].replace(CRLF, LF)):
            raise SystemExit(f"FATAL: live {rel} differs from git HEAD; diff it before replacing it")
    cur_main = live_get("nadlan-config.php")
    live_main = base64.b64decode(cur_main["b64"])
    stamp = time.strftime("%Y%m%dT%H%M%S")
    if not DRY:
        for rel in FILES:
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
            put(rel, NEW[rel], expect=md5(LIVE[rel]))
        put("nadlan-config.php", new_main, expect=md5(live_main))
    except BaseException as e:  # a write refused half way (drift, lint, md5): put everything back
        print("[FAIL] during writes:", e)
        rollback(created)
        raise
    print("[purge]", ops({"purge": 1}, "purge"))

    healthy = wait_version(new)
    bad = verify_pages("had247" + str(int(time.time()))) if healthy else ["health"]
    if bad:
        # one more purge and a patient second look before rolling back (OPcache/LiteSpeed lag)
        ops({"purge": 1}, "purge again")
        time.sleep(12)
        healthy = wait_version(new, 45)
        bad = verify_pages("had247b" + str(int(time.time()))) if healthy else ["health"]
    if bad:
        print("[FAIL] pages:", bad)
        rollback(created)
        wait_version(old, 60)
        raise SystemExit("ROLLED BACK")
    json.dump({"released": new, "from": old, "at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "files": dict({rel: md5(NEW[rel]) for rel in FILES}, **{"nadlan-config.php": md5(new_main)}),
        "live_before": dict({rel: md5(LIVE[rel]) for rel in FILES}, **{"nadlan-config.php": md5(live_main)})},
        open(os.path.join(QA, "deploy-result-229.json"), "w", encoding="utf-8"), indent=2)
    print(f"RELEASE {new} LIVE")
finally:
    bridge_down()
