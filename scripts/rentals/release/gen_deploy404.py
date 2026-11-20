# -*- coding: utf-8 -*-
"""Writes scripts/project-stage/deploy404.py in the main checkout: release 1.72.404 = HAD-383 rentals v2.2, ADMINISTRATORS ONLY
(option nadlan_rentals_v2 left unset = 'admin': everyone else keeps v1 at /my-rentals/; nlrm_billing left unset = 'off').

Built from deploy403.py (the standing safety chain: health gate, a one-run bridge, md5-guarded puts with .bak404, the version
bump on the live text, the fleet's page checks, rollback on any failed check) with a rentals main:
  - 22 NEW files from the branch claude/rentals-proptech-v2 (inc/rentals/*.php, assets/rentals/rm-*, rm.css, i18n/*), pinned by md5;
  - inc/rentals-manager.php: four hunks on the LIVE text (the v2 switch + loader, the /my-rentals/ route, the health line, one H1 for v1 visitors);
  - after the writes, through the bridge: the 11 tables and the data key made once (rm_init), the key escrowed to the owner's
    secrets folder (never printed), the key file checked NOT reachable over HTTP, /rm/boot run as the administrator (rm_probe);
  - as a visitor: v1 unchanged, health rentals_v2 false, the portal answers 410, a visitor cannot write.
No post, no option written.

  python scripts/rentals/release/gen_deploy404.py         (then: python scripts/project-stage/deploy404.py --dry, then without --dry)
"""
import hashlib, io, json, os, re, subprocess, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
WT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))          # this worktree
RENT_PLUG = os.path.join(WT, "plugins", "nadlan-config")
MAIN = r"C:\Users\777\nad-lan\nad-lan-co-il"
PS = os.path.join(MAIN, "scripts", "project-stage")
SRC = io.open(os.path.join(PS, "deploy403.py"), encoding="utf-8").read()
OUT = os.path.join(PS, "deploy404.py")


def md5(b):
    return hashlib.md5(b).hexdigest()


def must_replace(text, old, new, n=1, label=""):
    c = text.count(old)
    if c != n:
        raise SystemExit(f"FATAL generator: {label or old[:80]!r} x{c} (want {n})")
    return text.replace(old, new)


# ---------------------------------------------------------------- the files, pinned
RENT_FILES = ["inc/rentals/" + f + ".php" for f in ("store", "money", "billing", "rest", "portal", "lease", "legacy", "page")]
RENT_FILES += ["assets/rentals/" + f for f in ("rm-core.js", "rm-demo.js", "rm-views.js", "rm-drawers.js", "rm-lease.js", "rm-import.js", "rm-portal.js", "rm-boot.js", "rm-3d.js", "rm.css")]
RENT_FILES += ["assets/rentals/i18n/" + f for f in ("he.json", "en.json", "lease.json", "triage.json")]
PIN = {}
for rel in RENT_FILES:
    p = os.path.join(RENT_PLUG, *rel.split("/"))
    b = open(p, "rb").read()
    if b"\r\n" in b:
        raise SystemExit(f"FATAL: {rel} has CRLF line ends")
    if rel.endswith(".php"):
        r = subprocess.run(["php", "-l", p], capture_output=True, text=True)
        if r.returncode:
            raise SystemExit(f"FATAL: {rel}: {r.stdout}{r.stderr}")
    if rel.endswith(".js") and not rel.endswith("rm-3d.js"):
        r = subprocess.run(["node", "-e", "new Function(require('fs').readFileSync(process.argv[1],'utf8'))", p], capture_output=True, text=True)
        if r.returncode:
            raise SystemExit(f"FATAL: {rel} does not parse: {r.stderr[-300:]}")
    if rel.endswith(".json"):
        json.loads(b.decode("utf-8"))
    PIN[rel] = md5(b)
H = json.loads(open(os.path.join(RENT_PLUG, "assets/rentals/i18n/he.json"), encoding="utf-8").read())["ui"]
E = json.loads(open(os.path.join(RENT_PLUG, "assets/rentals/i18n/en.json"), encoding="utf-8").read())["ui"]
if set(H) != set(E):
    raise SystemExit("FATAL: he/en string tables differ")
MONEY = open(os.path.join(RENT_PLUG, "inc/rentals/money.php"), encoding="utf-8").read()
for must in ("function nlrm_money_fold(", "function nlrm_lease_end(", "function nlrm_lease_renew(", "function nlrm_deposit(", "INSERT IGNORE INTO", "function nlrm_purge("):
    if must not in MONEY:
        raise SystemExit("FATAL: money.php lacks " + must)
STORE = open(os.path.join(RENT_PLUG, "inc/rentals/store.php"), encoding="utf-8").read()
for must in ("UNIQUE KEY owner_auto (owner_id,auto_key)", "function nlrm_keyring(", "function nlrm_rotate_step(", "define( 'NLRM_DB_VERSION', '2.1.0' )"):
    if must not in STORE:
        raise SystemExit("FATAL: store.php lacks " + must)

# ---------------------------------------------------------------- rentals-manager.php: base (live 1.72.387) -> branch, as three hunks
BASE = subprocess.run(["git", "-C", WT, "show", "2ddf9192:plugins/nadlan-config/inc/rentals-manager.php"], capture_output=True).stdout.decode("utf-8").replace("\r\n", "\n")
BRANCH = open(os.path.join(RENT_PLUG, "inc/rentals-manager.php"), encoding="utf-8").read().replace("\r\n", "\n")
a1 = BRANCH.index("/* ---------- v2 (HAD-383")
a2 = BRANCH.index("/* ---------- CPT ---------- */")
V2BLOCK = BRANCH[a1:a2]
H1 = ("/* ---------- CPT ---------- */\nadd_action( 'init', function () {\n\tregister_post_type( 'nadlan_rentalprop'",
      V2BLOCK + "/* ---------- CPT ---------- */\nadd_action( 'init', function () {\n\tregister_post_type( 'nadlan_rentalprop'")
H2 = ("\tif ( ! nadlan_rm_on() ) { wp_safe_redirect( home_url( '/' ) ); exit; }\n\t$lang = function_exists( 'nadlan_ur_req_lang' )",
      "\tif ( ! nadlan_rm_on() ) { wp_safe_redirect( home_url( '/' ) ); exit; }\n\tif ( nadlan_rm_v2() ) {\n\t\tnlrm_maybe_install();\n\t\tnlrm_render_page( is_user_logged_in() ? 'app' : 'landing', nlrm_lang() );\n\t\texit;\n\t}\n\t$lang = function_exists( 'nadlan_ur_req_lang' )")
H3 = ("\t$out['rentals'] = nadlan_rm_on();\n\treturn $out;",
      "\t$out['rentals'] = nadlan_rm_on();\n\t$out['rentals_v2'] = function_exists( 'nadlan_rm_v2' ) && nadlan_rm_v2() ? ( defined( 'NLRM_DB_VERSION' ) ? NLRM_DB_VERSION : '1' ) : false;\n\treturn $out;")
H4 = ("\t\tget_header();\n",
      "\t\t/* one H1: the block theme's compat header prints the site name as an h1 (directory.php demotes it) */\n\t\tif ( function_exists( 'nadlan_dir_header_single_h1' ) ) { nadlan_dir_header_single_h1(); } else { get_header(); }\n")
HUNKS = [H1, H2, H3, H4]
t = BASE
for old, new in HUNKS:
    if t.count(old) != 1:
        raise SystemExit("FATAL: hunk anchor not once in the base: " + old[:60])
    t = t.replace(old, new)
if t != BRANCH:
    raise SystemExit("FATAL: the four hunks on the base do not give the branch's rentals-manager.php")
print("[gate] 22 files pinned (php -l, JS parse, JSON, LF); he/en parity", len(H), "strings; 4 hunks reproduce the branch's rentals-manager.php")

# ---------------------------------------------------------------- the runner, from deploy403.py
s = SRC
for a, b in (("1.72.403", "1.72.404"), (".bak403", ".bak404"), ("PS403", "PS404"), ("ps403", "ps404"), ("deploy403", "deploy404"),
             ("result-403", "result-404"), ("speed-403", "speed-404"), ("posts-before-403", "posts-before-404"),
             ("1.72.402", "1.72.403"), (".bak402", ".bak403"), ("range(402", "range(403")):
    s = s.replace(a, b)
doc_end = s.index('"""', 3) + 3
s = '''"""Release 1.72.404 (HAD-383, rentals v2.2: the money engine, the 3D drill-down; ADMINISTRATORS ONLY). GENERATED by
scripts/rentals/release/gen_deploy404.py (branch claude/rentals-proptech-v2) from deploy403.py; do not edit by hand.

Writes 22 NEW files (inc/rentals/*.php, assets/rentals/rm-*.js, rm.css, i18n/*.json) from the branch, inc/rentals-manager.php (three
hunks on the live text: the v2 switch and loader, the /my-rentals/ route, the health line) and nadlan-config.php (the version, on
the live text). The option nadlan_rentals_v2 is NOT written: its default 'admin' shows v2 to administrators only. Then, through the
bridge: the rentals tables and the data key made once, the key escrowed to the owner's secrets folder, the key file checked
unreachable over HTTP, /rm/boot run as the administrator. Rolls back on any failed check (.bak404, new files removed).

  python scripts/project-stage/deploy404.py [--dry | --rollback]
"""''' + s[doc_end:]
s = re.sub(r'PHP_RELS = \["inc/project-stage.php"\][^\n]*', 'PHP_RELS = ["inc/rentals-manager.php"]  # 1.72.404: three hunks on the live text, restored from .bak404 on rollback', s, count=1)
# never run while another release is still in flight (3.10: a dry run's opening sweep removed a running release's bridge)
s = must_replace(s, '\n# ---------------------------------------------------------------- health + bridge\n', '''
# ---------------------------------------------------------------- the previous release must be closed (released or rolled back)
_prev = os.path.join(QA, "deploy-result-403.json")
if os.path.exists(_prev):
    _st = str(json.load(open(_prev, encoding="utf-8")).get("state", ""))
    if not (_st.startswith("released") or _st.startswith("rolled back")):
        raise SystemExit("FATAL: release 1.72.403 is still in flight (its record says '" + _st + "'); wait until it is closed")
for _f in sorted(os.listdir(QA)):
    if _f.startswith("deploy-result-") and _f.endswith(".json") and _f > "deploy-result-404.json":
        raise SystemExit("FATAL: a later release record exists (" + _f + "); regenerate on top of it")

# ---------------------------------------------------------------- health + bridge
''')
# the bridge: four rentals operations, before the purge
BRIDGE_ADD = r"""			if ( ! empty( $b['rm_init'] ) ) { // 1.72.404 (HAD-383): the rentals tables and the data key, made once
				if ( function_exists( 'nlrm_install' ) && defined( 'NLRM_DB_VERSION' ) && get_option( 'nlrm_db_version' ) !== NLRM_DB_VERSION ) { delete_transient( 'nlrm_installing' ); nlrm_install(); }
				$ring = function_exists( 'nlrm_keyring' ) ? nlrm_keyring() : null;
				if ( function_exists( 'nlrm_keycheck_init' ) ) { nlrm_keycheck_init(); }
				global $wpdb;
				$out['rm_init'] = array(
					'db' => (string) get_option( 'nlrm_db_version' ),
					'tables' => (int) $wpdb->get_var( $wpdb->prepare( 'SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = DATABASE() AND table_name LIKE %s', $wpdb->esc_like( $wpdb->prefix . 'nlrm_' ) . '%' ) ),
					'key_src' => $ring ? (string) $ring['src'] : '', 'kid' => $ring ? (string) $ring['cur'] : '',
					'key_ok' => function_exists( 'nlrm_key_ok' ) ? (bool) nlrm_key_ok() : false,
					'mode' => (string) get_option( 'nadlan_rentals_v2', 'admin' ), 'billing' => (string) get_option( 'nlrm_billing', 'off' ),
					'key_url' => function_exists( 'nlrm_keyfile_path' ) ? str_replace( wp_normalize_path( ABSPATH ), '/', wp_normalize_path( nlrm_keyfile_path() ) ) : '',
				);
			}
			if ( ! empty( $b['rm_key'] ) && function_exists( 'nlrm_keyfile_path' ) ) {
				$f = nlrm_keyfile_path();
				$out['rm_key'] = is_readable( $f ) ? array( 'b64' => base64_encode( (string) file_get_contents( $f ) ), 'md5' => md5_file( $f ) ) : array( 'missing' => 1 );
			}
			if ( isset( $b['rm_mode'] ) && in_array( (string) $b['rm_mode'], array( '0', 'admin', '1' ), true ) ) {
				update_option( 'nadlan_rentals_v2', (string) $b['rm_mode'] );
				$out['rm_mode'] = (string) get_option( 'nadlan_rentals_v2' );
			}
			if ( isset( $b['rm_pilot'] ) && is_array( $b['rm_pilot'] ) ) { // the pilot landlords who see v2 before everyone (user ids or e-mails)
				$ids = array();
				foreach ( $b['rm_pilot'] as $w ) { $u = is_numeric( $w ) ? get_userdata( (int) $w ) : get_user_by( 'email', sanitize_email( (string) $w ) ); if ( $u ) { $ids[] = (int) $u->ID; } }
				update_option( 'nadlan_rentals_v2_pilot', array_values( array_unique( $ids ) ), false );
				$out['rm_pilot'] = get_option( 'nadlan_rentals_v2_pilot' );
			}
			if ( ! empty( $b['rm_cpi'] ) ) { // why the CBS calculator does or does not answer from the host
				$u = 'https://api.cbs.gov.il/index/data/calculator/120010?value=1000&date=01-01-2023&toDate=08-01-2026&format=json&download=false';
				$o2 = array();
				foreach ( array( 'wp' => array( 'timeout' => 20 ), 'browser' => array( 'timeout' => 20, 'headers' => array( 'User-Agent' => 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36 nad-lan.co.il', 'Accept' => 'application/json' ) ) ) as $k => $a ) {
					$t0 = microtime( true ); $rr2 = wp_remote_get( $u, $a );
					$o2[ $k ] = is_wp_error( $rr2 ) ? array( 'error' => $rr2->get_error_message(), 'ms' => (int) ( ( microtime( true ) - $t0 ) * 1000 ) ) : array( 'http' => wp_remote_retrieve_response_code( $rr2 ), 'body' => substr( (string) wp_remote_retrieve_body( $rr2 ), 0, 160 ), 'ms' => (int) ( ( microtime( true ) - $t0 ) * 1000 ) );
				}
				$o2['last_error'] = get_transient( 'nlrm_cpi_last_error' );
				$out['rm_cpi'] = $o2;
			}
			if ( ! empty( $b['rm_probe'] ) ) {
				$rr = rest_do_request( new WP_REST_Request( 'GET', '/nadlan/v1/rm/boot' ) );
				$dd = $rr->get_data();
				$rts = array_values( array_filter( array_keys( rest_get_server()->get_routes() ), function ( $x ) { return 0 === strpos( $x, '/nadlan/v1/rm/' ); } ) );
				$out['rm_probe'] = array( 'status' => $rr->get_status(), 'keys' => is_array( $dd ) ? array_keys( $dd ) : array(), 'role' => is_array( $dd ) ? (string) ( $dd['role'] ?? '' ) : '',
					'key_ok' => is_array( $dd ) && ! empty( $dd['key_ok'] ), 'plan' => is_array( $dd ) ? (string) ( $dd['plan']['id'] ?? '' ) : '', 'billing' => is_array( $dd ) ? (string) ( $dd['plan']['billing'] ?? '' ) : '',
					'routes' => $rts, 'v2' => function_exists( 'nadlan_rm_v2' ) ? (bool) nadlan_rm_v2() : null );
			}
"""
s = must_replace(s, "\t\t\tif ( ! empty( $b['purge'] ) ) {", BRIDGE_ADD + "\t\t\tif ( ! empty( $b['purge'] ) ) {")
# the module prelude: drop 403's posts (and its content pins), set the rentals files
i = s.index("HEAD = {rel: git_head(")
j = s.index('os.makedirs(os.path.join(QA, "live-backup"), exist_ok=True)')
PRELUDE = '''# ---------------------------------------------------------------- 1.72.404: the rentals files, from the branch claude/rentals-proptech-v2
RENT_PLUG = r"''' + RENT_PLUG + '''"
FILES = ''' + json.dumps(RENT_FILES) + '''
NEWFILES = set(FILES)
PIN = ''' + json.dumps(PIN, indent=1) + '''
RM_HUNKS = ''' + json.dumps(HUNKS, ensure_ascii=False) + '''
ESCROW_DIR = r"C:\\Users\\777\\Documents\\jus-tice-secrets\\nadlan-rentals"
NEW = {}
for rel in FILES:
    NEW[rel] = open(os.path.join(RENT_PLUG, *rel.split("/")), "rb").read()
    if md5(NEW[rel]) != PIN[rel]:
        raise SystemExit(f"FATAL: {rel} changed since gen_deploy404.py pinned it ({md5(NEW[rel])[:10]} != {PIN[rel][:10]}); run the generator again")
for rel in FILES:
    if rel.endswith(".php"):
        php_lint(NEW[rel], rel)
'''
s = s[:i] + PRELUDE + s[j:]
# the main
i = s.index('\ntry:\n    sweep("start")')
j = s.index("\nfinally:\n")
MAINCODE = r'''

def served_exact(tag):
    """each new asset as the site serves it to a page (?ver=1.72.404), byte for byte the pinned file (PHP is executed, not served)"""
    ok = True
    for rel in FILES:
        if rel.endswith(".php"):
            continue
        path = "/wp-content/plugins/nadlan-config/" + rel + "?ver=1.72.404&nlv=" + tag
        try:
            s2, b2 = req("GET", path, raw=True, auth=False, timeout=90)
        except Exception as e:
            s2, b2 = str(e)[:60], b""
        good = s2 == 200 and md5(b2) == PIN[rel]
        print(f"[served] {'OK ' if good else 'BAD'} {s2} {rel}: {md5(b2)[:10] if b2 else '-'} (want {PIN[rel][:10]})")
        ok = ok and good
    return ok


def rentals_checks(tag):
    """the rentals release, as a visitor and (through the bridge) as the administrator"""
    ok = True
    def say(name, good, info=""):
        nonlocal ok
        print(f"[rentals] {'OK ' if good else 'BAD'} {name}" + (f" | {info}" if info != "" else ""))
        ok = ok and good
    s2, hh = req("GET", "/wp-json/nadlan/v1/health?nlv=" + tag, auth=False)
    say("health as a visitor: rentals_v2 off (administrators only)", s2 == 200 and not hh.get("rentals_v2"), hh.get("rentals_v2"))
    for path in ("/my-rentals/", "/my-rentals/?lang=en"):
        s2, html = page(path + ("&" if "?" in path else "?") + "nlv=" + tag)
        say(f"{path} as a visitor is v1, unchanged", s2 == 200 and 'id="nlrm-mount"' in html and 'id="nlrm-root"' not in html and "rm-core.js" not in html, s2)
    s2, body = req("GET", "/wp-json/nadlan/v1/rm/portal", raw=True, auth=False)
    try:
        pmsg = json.loads(body.decode("utf-8", "replace")).get("message", "")
    except Exception:
        pmsg = ""
    say("the tenant portal without a link answers 410, in Hebrew", s2 == 410 and "הקישור אינו בתוקף" in pmsg, f"{s2} {pmsg[:40]}")
    s2, body = req("POST", "/wp-json/nadlan/v1/rm/pay", body={"data": {"lease_id": 1, "amount": 1}}, raw=True, auth=False)
    say("a visitor cannot write money", s2 in (401, 403), s2)
    s2, body = req("GET", "/wp-json/nadlan/v1/rm/cpi?amount=1000&from=2023-01-01&to=2026-08-01", raw=True, auth=False)
    print(f"[rentals] info: the CBS calculator through /rm/cpi: http {s2} {body[:100]!r}")
    print("[rentals] info: CBS from the host:", json.dumps(ops({"rm_cpi": 1}, "cbs probe").get("rm_cpi"), ensure_ascii=False)[:600])
    init = ops({"rm_init": 1}, "rentals init")["rm_init"]
    say("the tables and the data key", init.get("db") == "2.1.0" and init.get("tables") == 11 and init.get("key_src") == "file" and init.get("key_ok") is True and init.get("mode") == "admin" and init.get("billing") == "off",
        {k: v for k, v in init.items() if k != "key_url"})
    key = ops({"rm_key": 1}, "rentals key escrow")["rm_key"]
    if key.get("b64"):
        os.makedirs(ESCROW_DIR, exist_ok=True)
        fn = os.path.join(ESCROW_DIR, "nad-lan-rentals-key-" + str(init.get("kid")) + ".json")
        if not os.path.exists(fn):
            with open(fn, "w", encoding="utf-8") as fh:
                json.dump({"site": BASE, "kid": init.get("kid"), "file": init.get("key_url"), "md5": key.get("md5"), "b64": key["b64"], "saved": time.strftime("%Y-%m-%d %H:%M:%S"),
                           "note": "The rentals data key of nad-lan.co.il (uploads/nlrm-private/.nlrm-key.php). Without it the tenants' encrypted data cannot be read after a restore. Never print, commit or send."}, fh)
        say("the key escrowed to the owner's secrets folder (not printed)", os.path.exists(fn), "kid " + str(init.get("kid")) + ", md5 " + str(key.get("md5"))[:10])
    else:
        say("the key file exists", False, key)
    if init.get("key_url"):
        s2, body = req("GET", init["key_url"] + "?nlv=" + tag, raw=True, auth=False)
        leak = b'"keys"' in body or (key.get("b64") and key["b64"][:40].encode() in body)
        say("the key file is NOT readable over HTTP", not leak, f"http {s2}, {len(body)} bytes")
        s2, body = req("GET", init["key_url"].rsplit("/", 1)[0] + "/?nlv=" + tag, raw=True, auth=False)
        say("the private folder lists nothing", b".nlrm-key" not in body and b"Index of" not in body, f"http {s2}")
    pr = ops({"rm_probe": 1}, "rentals probe")["rm_probe"]
    need = ["/nadlan/v1/rm/boot", "/nadlan/v1/rm/pay", "/nadlan/v1/rm/ledger-act", "/nadlan/v1/rm/deposit", "/nadlan/v1/rm/lease-end", "/nadlan/v1/rm/lease-renew", "/nadlan/v1/rm/refund", "/nadlan/v1/rm/writeoff", "/nadlan/v1/rm/portal", "/nadlan/v1/rm/export", "/nadlan/v1/rm/plan-grant"]
    say("/rm/boot as the administrator: the books, the plan, the key", pr.get("status") == 200 and all(k in pr.get("keys", []) for k in ("money", "stats", "plan", "ledger", "leases")) and pr.get("role") == "owner" and pr.get("key_ok") is True and pr.get("billing") == "off" and pr.get("v2") is True,
        {k: pr.get(k) for k in ("status", "role", "key_ok", "plan", "billing", "v2")})
    say("the money routes are registered", all(r in pr.get("routes", []) for r in need), [r for r in need if r not in pr.get("routes", [])])
    return ok


try:
    sweep("start")
    bridge_up()
    if "--rollback" in ARGS:
        rollback(True)
        wait_version(LIVE_VER)
        if os.path.exists(RESULT):
            REC.update(json.load(open(RESULT, encoding="utf-8")))
            REC["rolled_back_files"] = REC.get("files") or REC.get("rolled_back_files") or {}
            record("rolled back (--rollback)", files={})
        raise SystemExit(0)
    if LIVE_VER != WANT_LIVE:
        raise SystemExit(f"FATAL: live is {LIVE_VER}, this runner is for {WANT_LIVE} -> 1.72.404 (its checks name the version); regenerate it")
    for rel in FILES:
        cur = live_get(rel)
        if not cur.get("missing"):
            raise SystemExit(f"FATAL: {rel} already exists on the site; this release makes it new")
    print(f"[drift] the {len(FILES)} rentals files are not on the site yet (new)")
    cur = live_get("inc/rentals-manager.php")
    if cur.get("missing"):
        raise SystemExit("FATAL live file missing: inc/rentals-manager.php")
    rm_live = base64.b64decode(cur["b64"])
    txt = rm_live.decode("utf-8"); crlf = "\r\n" in txt; txt = txt.replace("\r\n", "\n")
    for old, nw in RM_HUNKS:
        if nw in txt:
            raise SystemExit("FATAL: inc/rentals-manager.php already holds a v2 hunk; diff it before replacing it")
        if txt.count(old) != 1:
            raise SystemExit("FATAL: inc/rentals-manager.php: the anchor " + repr(old[:50]) + " is there " + str(txt.count(old)) + " times")
        txt = txt.replace(old, nw)
    rm_new = (txt.replace("\n", "\r\n") if crlf else txt).encode("utf-8")
    php_lint(rm_new, "inc/rentals-manager.php (live text + the v2 hunks)")
    print(f"[drift] live inc/rentals-manager.php {md5(rm_live)[:10]}: {len(RM_HUNKS)} hunks applied once; new {md5(rm_new)[:10]}")
    cur_main = live_get("nadlan-config.php")
    live_main = base64.b64decode(cur_main["b64"])
    stamp = time.strftime("%Y%m%dT%H%M%S")
    if not DRY:
        open(os.path.join(QA, "live-backup", f"rentals-manager.php.{stamp}.live"), "wb").write(rm_live)
        open(os.path.join(QA, "live-backup", f"nadlan-config.php.{stamp}.live"), "wb").write(live_main)
    text = live_main.decode("utf-8")
    m = re.search(r"\* Version: (\d+)\.(\d+)\.(\d+)", text)
    old = ".".join(m.groups())
    new = f"{m.group(1)}.{m.group(2)}.{int(m.group(3)) + 1}"
    if new != "1.72.404":
        raise SystemExit(f"FATAL: the bump would be {old} -> {new}, not 1.72.404")
    for a, b2 in ((f" * Version: {old}", f" * Version: {new}"), (f"define( 'NADLAN_CONFIG_VERSION', '{old}' )", f"define( 'NADLAN_CONFIG_VERSION', '{new}' )")):
        n = text.count(a)
        if n != 1:
            raise SystemExit(f"FATAL anchor x{n} in nadlan-config.php: {a}")
        text = text.replace(a, b2)
    if "'rentals-manager'" not in text and "rentals-manager.php" not in text:
        raise SystemExit("FATAL: nadlan-config.php does not load rentals-manager")
    new_main = text.encode("utf-8")
    php_lint(new_main, "nadlan-config.php (live text, bumped)")
    print(f"[plan] {old} -> {new}; {len(FILES)} new files, inc/rentals-manager.php (3 hunks), nadlan-config.php (version); no option, no post")
    if DRY:
        print("[dry] no writes")
        raise SystemExit(0)

    REC.update({"released": new, "from": old, "live_before": {"inc/rentals-manager.php": md5(rm_live), "nadlan-config.php": md5(live_main)}})
    FILES_MD5 = dict({rel: md5(NEW[rel]) for rel in FILES}, **{"nadlan-config.php": md5(new_main), "inc/rentals-manager.php": md5(rm_new)})
    try:
        created = True
        for rel in FILES:
            put(rel, NEW[rel], expect="missing")
        put("inc/rentals-manager.php", rm_new, expect=md5(rm_live))
        put("nadlan-config.php", new_main, expect=md5(live_main))
        record("files written, checks pending", files=FILES_MD5)
    except BaseException as e:
        print("[FAIL] during writes:", e)
        rollback(created)
        if REC.get("released"):
            record("rolled back during the writes: " + str(e)[:200], files={}, rolled_back_files=FILES_MD5)
        raise
    print("[purge]", ops({"purge": 1}, "purge"))

    healthy = wait_version(new)
    bad = run_checks("a") if healthy else ["health"]
    if not bad and not rentals_checks("a" + str(int(time.time()))):
        bad = ["rentals"]
    if bad:
        print("[checks] first round:", bad, "- purge and look again")
        ops({"purge": 1}, "purge again")
        time.sleep(12)
        healthy = wait_version(new, 45)
        bad = run_checks("b") if healthy else ["health"]
        if not bad and not rentals_checks("b" + str(int(time.time()))):
            bad = ["rentals"]
    if bad:
        print("[FAIL] pages:", bad)
        rollback(created)
        wait_version(old, 60)
        record("rolled back after the checks: " + ", ".join(bad), files={}, rolled_back_files=FILES_MD5)
        raise SystemExit("ROLLED BACK")
    record("released and verified", files=FILES_MD5, checks="verify_pages + served_exact (the 14 assets at ?ver=1.72.404, byte for byte) + verify_order + verify_home_order + verify_kh + rentals_checks (visitor v1, 410 portal, no visitor writes, tables 11, key file + escrow + not over HTTP, /rm/boot as admin): OK")
    print("RELEASE 1.72.404 LIVE: HAD-383 rentals v2.2 for ADMINISTRATORS (the money engine, the 3D drill-down); visitors keep v1")
'''
s = s[:i] + MAINCODE + s[j:]
io.open(OUT, "w", encoding="utf-8", newline="\n").write(s)
r = subprocess.run([sys.executable, "-m", "py_compile", OUT], capture_output=True, text=True)
if r.returncode:
    raise SystemExit("FATAL: deploy404.py does not compile: " + r.stderr[-500:])
print("written", OUT, len(s), "chars")
