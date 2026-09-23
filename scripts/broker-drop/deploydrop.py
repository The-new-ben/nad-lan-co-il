# -*- coding: utf-8 -*-
"""Broker drop box deploy (owner order 23.9.2026: "an address the broker throws photos and details at, the system
builds the property in the broker's website, no replies, no login, for every future broker").

Installs plugins/nadlan-config/inc/broker-drop.php as the persistent Code Snippet x-broker-drop (server-side PHP lint
first), then wires the first broker (Meital Katzir) and verifies. Setup writes go through a temporary, token-gated
bridge route with update_post_meta, so her live pages are NOT re-saved (no IndexNow re-pings, no revisions).

Usage:
  python deploydrop.py                 lint on the server + install/update x-broker-drop + verify
  python deploydrop.py --setup         also wire Meital (token, site pages, her 11 listings and their English twins)
  python deploydrop.py --auto 0|1      Meital's pages publish at once (1) or wait as drafts (0)
  python deploydrop.py --off           deactivate x-broker-drop (rollback)
  python deploydrop.py --verify        checks only
The drop link is printed once at --setup (it is the deliverable the owner forwards to the broker). The WordPress app
password is decrypted in-process (DPAPI) and never printed.
"""
import base64, ctypes, ctypes.wintypes, hashlib, io, json, os, re, secrets, sys, time, urllib.request, urllib.error
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = "https://nad-lan.co.il"
REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
MODULE = os.path.join(REPO, "plugins", "nadlan-config", "inc", "broker-drop.php")
IMAP = os.path.join(REPO, "handoff", "meital-2026-09-17", "package", "data", "import-map.json")
SECRETS_PATH = r"C:\Users\777\Documents\websites\.codex-secrets\wordpress-app-passwords\nad-lan.co.il.json"
ARGS = sys.argv[1:]
SNIPPET = "x-broker-drop"
BROKER = 7833

class DATA_BLOB(ctypes.Structure):
    _fields_ = [("cbData", ctypes.wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]

def dpapi_unprotect(b64):
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
    sec = json.load(f)
AUTH = "Basic " + base64.b64encode(f"{sec['username']}:{dpapi_unprotect(sec['password_dpapi'])}".encode()).decode()
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) NadLan-BrokerDrop/1.0"

def req(method, path, body=None, timeout=180, raw=False, auth=True, headers=None):
    data = None if body is None else json.dumps(body, ensure_ascii=False).encode()
    r = urllib.request.Request(BASE + path, data=data, method=method)
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
        try:
            return e.code, (p if raw else json.loads(p.decode())), dict(e.headers)
        except Exception:
            return e.code, {"raw": p[:300].decode("utf-8", "replace")}, dict(e.headers)

def must(s, p, what, ok=(200, 201)):
    if s not in ok:
        raise SystemExit(f"FATAL {what}: HTTP {s}: {json.dumps(p, ensure_ascii=False)[:500]}")
    return p

def snip(method, path, body=None):
    return req(method, "/wp-json/code-snippets/v1/snippets" + path, body)[:2]

def find_snippet(name):
    s, lst = snip("GET", "")
    must(s, lst, "list snippets")
    for x in lst:
        if x["name"] == name:
            return x
    return None

s, h, _ = req("GET", "/wp-json/nadlan/v1/health")
must(s, h, "health")
print("health", h["version"], h["status"])

if "--off" in ARGS:
    x = find_snippet(SNIPPET)
    if x:
        s2, _ = snip("PUT", f"/{x['id']}/deactivate", {})
        print(SNIPPET, "deactivated", s2)
    else:
        print(SNIPPET, "not installed")
    raise SystemExit(0)

TOKEN = secrets.token_hex(24)
BRIDGE = r'''
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-drop-ops/v1', '/apply', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( isset( $b['token'] ) ? $b['token'] : '' ) ) ) { return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) ); }
			$out = array();
			if ( ! empty( $b['lint'] ) ) {
				try { token_get_all( "<?php\n" . (string) $b['lint'], TOKEN_PARSE ); $out['lint'] = 'ok ' . PHP_VERSION; }
				catch ( ParseError $e ) { return new WP_Error( 'lint', $e->getMessage() . ' line ' . $e->getLine(), array( 'status' => 400 ) ); }
			}
			if ( ! empty( $b['meta'] ) && is_array( $b['meta'] ) ) {
				foreach ( $b['meta'] as $row ) {
					$pid = (int) $row['id'];
					if ( ! $pid || ! get_post( $pid ) ) { $out['meta_missing'][] = $pid; continue; }
					foreach ( (array) $row['set'] as $k => $v ) {
						if ( strpos( (string) $k, 'nl_' ) !== 0 ) { continue; }
						update_post_meta( $pid, sanitize_key( $k ), wp_slash( (string) $v ) );
					}
					$out['meta_ok'][] = $pid;
				}
			}
			if ( ! empty( $b['token_for'] ) ) {
				$pid = (int) $b['token_for'];
				$t   = (string) get_post_meta( $pid, 'nl_drop_token', true );
				if ( ! preg_match( '/^[a-z0-9]{24}$/', $t ) ) { $t = substr( bin2hex( random_bytes( 16 ) ), 0, 24 ); update_post_meta( $pid, 'nl_drop_token', $t ); }
				$out['drop_url'] = home_url( '/drop/' . $t . '/' );
			}
			if ( ! empty( $b['purge'] ) ) {
				foreach ( (array) $b['purge'] as $pid ) { clean_post_cache( (int) $pid ); do_action( 'litespeed_purge_post', (int) $pid ); }
				$out['purged'] = count( (array) $b['purge'] );
			}
			return $out;
		},
	) );
} );
'''.replace("__TOKEN__", TOKEN)

def install_and_setup():
    s, c = snip("POST", "", {"name": f"tmp-drop-ops-{int(time.time())}", "code": "/* placeholder */", "scope": "global", "active": False})
    must(s, c, "bridge create")
    br = c["id"]
    try:
        s, u = snip("PUT", f"/{br}", {"name": c["name"], "code": BRIDGE, "scope": "global", "active": False})
        must(s, u, "bridge update")
        s, a = snip("PUT", f"/{br}/activate", {})
        must(s, a, "bridge activate")

        def ops(payload, what):
            payload["token"] = TOKEN
            s, r, _ = req("POST", "/wp-json/nadlan-drop-ops/v1/apply", payload, timeout=240)
            return must(s, r, what)

        php = open(MODULE, encoding="utf-8").read()
        code = re.sub(r"^\s*<\?php\s*", "", php, count=1)
        print("lint on the server:", ops({"lint": code}, "lint")["lint"])
        if "--verify" not in ARGS or "--install" in ARGS:
            x = find_snippet(SNIPPET)
            body = {"name": SNIPPET, "code": code, "scope": "global", "active": False,
                    "desc": "Broker drop box: a private link per broker; photos and a few lines become a listing page in the broker's site. Source: plugins/nadlan-config/inc/broker-drop.php"}
            if x:
                sid = x["id"]
                s, u2 = snip("PUT", f"/{sid}", body)
                must(s, u2, "snippet update")
            else:
                s, c2 = snip("POST", "", body)
                must(s, c2, "snippet create")
                sid = c2["id"]
            s, a2 = snip("PUT", f"/{sid}/activate", {})
            must(s, a2, "snippet activate")
            print(SNIPPET, "id", sid, "sha256", hashlib.sha256(code.encode()).hexdigest()[:16], "ACTIVE")

        if "--setup" in ARGS:
            imap = json.load(open(IMAP, encoding="utf-8"))
            rows = [{"id": BROKER, "set": {"nl_drop_on": "1", "nl_name_he": "מיטל קציר", "nl_name_en": "Meital Katzir",
                                             "nl_brand_en": "Real Estate by the Sea", "nl_gender": "f",
                                             "nl_site_he": str(imap["broker-he"]), "nl_site_en": str(imap["broker-en"]), "nl_auto_publish": "1"}},
                    {"id": imap["broker-he"], "set": {"nl_broker_site": str(BROKER), "nl_lang": "he"}},
                    {"id": imap["broker-en"], "set": {"nl_broker_site": str(BROKER), "nl_lang": "en"}}]
            for n in range(1, 12):
                L = f"L{n:02d}"
                he, en = imap.get(L + "-he"), imap.get(L + "-en")
                if he:
                    rows.append({"id": he, "set": {"nl_broker_id": str(BROKER), "nl_card_key": L, "nl_status": "active", "nl_twin": str(en or "")}})
                if en:
                    rows.append({"id": en, "set": {"nl_broker_id": str(BROKER), "nl_card_key": L, "nl_status": "active", "nl_twin": str(he or "")}})
            r = ops({"meta": rows, "token_for": BROKER, "purge": [imap["broker-he"], imap["broker-en"]]}, "setup")
            print("setup: meta on", len(r.get("meta_ok", [])), "posts; missing", r.get("meta_missing", []))
            print("DROP LINK:", r["drop_url"])

        if "--auto" in ARGS:
            val = ARGS[ARGS.index("--auto") + 1]
            ops({"meta": [{"id": BROKER, "set": {"nl_auto_publish": "1" if val == "1" else "0"}}]}, "auto")
            print("auto publish ->", val)
    finally:
        s1, _ = snip("PUT", f"/{br}/deactivate", {})
        s2, _ = snip("DELETE", f"/{br}", None)
        print("bridge cleanup", s1, s2)
        s3, _, _ = req("POST", "/wp-json/nadlan-drop-ops/v1/apply", {"token": "x"})
        print("bridge route after cleanup:", s3, "(want 404)")

if "--verify" not in ARGS or "--setup" in ARGS or "--auto" in ARGS or "--install" in ARGS:
    install_and_setup()

# ---- verify ----
time.sleep(3)
s, hc, _ = req("GET", "/wp-json/nadlan/v1/healthcheck?nlv=%d" % time.time(), auth=False)
print("healthcheck:", s, "version", hc.get("version"), "| broker_drop:", json.dumps(hc.get("broker_drop"), ensure_ascii=False))
for path in ("/", "/brokers/meital-katzir/", "/en/brokers/meital-katzir/", "/properties/nofei-yam-3-rooms-balcony-for-rent/"):
    s, body, _ = req("GET", path + "?nlv=%d" % time.time(), raw=True, auth=False, headers={"User-Agent": "Mozilla/5.0 Chrome/128"}, timeout=120)
    t = body.decode("utf-8", "replace") if isinstance(body, (bytes, bytearray)) else ""
    b = t.split("<body", 1)[-1]
    cards = b.count('class="nlb-lcard"')
    err = ("Fatal error" in t) or ("Warning:" in b[:4000])
    print(f"GET {path}: {s} bytes={len(t)} cards={cards} php_error={err} soldbar={b.count('nlx-soldbar')}")
s, body, _ = req("GET", "/drop/000000000000000000000000/", raw=True, auth=False)
print("drop page with a dead token:", s, "(want 404)")
