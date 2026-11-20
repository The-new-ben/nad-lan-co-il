# -*- coding: utf-8 -*-
"""Writes scripts/project-stage/deploy406.py in the main checkout: release 1.72.406 = HAD-383/HAD-401 rentals, still ADMINISTRATORS
ONLY (the option nadlan_rentals_v2 is not written; nlrm_billing stays 'off').

Built from deploy405.py (the newest safety chain and fleet checks: health gate, a one-run bridge, md5-guarded puts with .bak406, the
version bump on the live text, verify_pages / served_exact / verify_order / verify_home_order / verify_kh, rollback on any failed
check), with a rentals main:
  - 7 CHANGED files (rest.php, rm-core/demo/views/drawers.js, i18n he/en), each guarded by the md5 release 1.72.404 wrote;
  - 84 NEW files: the manual (assets/rentals/help/he.html, en.html, 80 screenshots, manual-he.pdf, manual-en.pdf);
  - after the checks pass, through the bridge: the landlord's plans as two WooCommerce DRAFT products (hidden, not purchasable; the
    prices 39 / 199 are the owner's proposal, not approved), made once and found by the meta _nlrm_plan.
No post, no option, no rentals-manager.php change.

  python scripts/rentals/release/gen_deploy406.py         (then: python scripts/project-stage/deploy406.py --dry, then without --dry)
"""
import hashlib, io, json, os, re, subprocess, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
WT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
RENT_PLUG = os.path.join(WT, "plugins", "nadlan-config")
MAIN = r"C:\Users\777\nad-lan\nad-lan-co-il"
PS = os.path.join(MAIN, "scripts", "project-stage")
QA = os.path.join(MAIN, "docs", "qa", "project-stage-2026-09-24")
SRC = io.open(os.path.join(PS, "deploy405.py"), encoding="utf-8").read()
OUT = os.path.join(PS, "deploy406.py")


def md5(b):
    return hashlib.md5(b).hexdigest()


def must_replace(text, old, new, n=1, label=""):
    c = text.count(old)
    if c != n:
        raise SystemExit(f"FATAL generator: {label or old[:80]!r} x{c} (want {n})")
    return text.replace(old, new)


# ---------------------------------------------------------------- what 1.72.404 wrote (the live md5 each changed file must still have)
R404 = json.load(open(os.path.join(QA, "deploy-result-404.json"), encoding="utf-8"))
if not str(R404.get("state", "")).startswith("released"):
    raise SystemExit("FATAL: release 1.72.404 is not 'released': " + str(R404.get("state")))
R405 = json.load(open(os.path.join(QA, "deploy-result-405.json"), encoding="utf-8"))
if not str(R405.get("state", "")).startswith("released"):
    raise SystemExit("FATAL: release 1.72.405 is not closed as released: " + str(R405.get("state")))
LIVE404 = {k: v for k, v in R404["files"].items() if k not in ("nadlan-config.php", "inc/rentals-manager.php")}
CHANGED, SAME = [], []
for rel, h in LIVE404.items():
    cur = md5(open(os.path.join(RENT_PLUG, *rel.split("/")), "rb").read())
    (CHANGED if cur != h else SAME).append(rel)
HELP = ["assets/rentals/help/he.html", "assets/rentals/help/en.html", "assets/rentals/help/manual-he.pdf", "assets/rentals/help/manual-en.pdf"]
HELP += sorted("assets/rentals/help/img/" + f for f in os.listdir(os.path.join(RENT_PLUG, "assets", "rentals", "help", "img")) if f.endswith(".webp"))
FILES = CHANGED + HELP
PIN = {}
for rel in FILES:
    p = os.path.join(RENT_PLUG, *rel.split("/"))
    b = open(p, "rb").read()
    if rel.endswith((".php", ".js", ".json", ".html", ".css")) and b"\r\n" in b:
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
    if rel.endswith(".pdf") and b[:4] != b"%PDF":
        raise SystemExit(f"FATAL: {rel} is not a PDF")
    if rel.endswith(".webp") and (b[:4] != b"RIFF" or b[8:12] != b"WEBP"):
        raise SystemExit(f"FATAL: {rel} is not a WebP")
    PIN[rel] = md5(b)
H = json.loads(open(os.path.join(RENT_PLUG, "assets/rentals/i18n/he.json"), encoding="utf-8").read())["ui"]
E = json.loads(open(os.path.join(RENT_PLUG, "assets/rentals/i18n/en.json"), encoding="utf-8").read())["ui"]
if set(H) != set(E):
    raise SystemExit("FATAL: he/en string tables differ")
for need in ("links_title", "link_revoke", "help_pdf", "floor_repairs_none", "rep_year_pick", "csv_ledger_name"):
    if need not in H:
        raise SystemExit("FATAL: the string table lacks " + need)
REST = open(os.path.join(RENT_PLUG, "inc/rentals/rest.php"), encoding="utf-8").read()
if "'/rm/evidence'" not in REST:
    raise SystemExit("FATAL: rest.php lacks /rm/evidence")
imgs = [r for r in HELP if r.endswith(".webp")]
for lang in ("he", "en"):
    html = open(os.path.join(RENT_PLUG, "assets/rentals/help", lang + ".html"), encoding="utf-8").read()
    for src in re.findall(r'<img[^>]+src="([^"]+)"', html):
        if "assets/rentals/help/" + src not in HELP:
            raise SystemExit(f"FATAL: help/{lang}.html names {src}, which is not shipped")
total = sum(os.path.getsize(os.path.join(RENT_PLUG, *r.split("/"))) for r in FILES)
print(f"[gate] {len(CHANGED)} changed ({', '.join(CHANGED)}), {len(SAME)} unchanged since 1.72.404, {len(HELP)} new manual files ({len(imgs)} images, 2 PDFs); "
      f"{total:,} bytes; he/en parity {len(H)} strings; every image the guide names is shipped")

# ---------------------------------------------------------------- the runner, from deploy405.py
s = SRC
for a, b in (("1.72.405", "1.72.406"), (".bak405", ".bak406"), ("PS405", "PS406"), ("ps405", "ps406"), ("gen_deploy405", "gen_deploy406"), ("deploy405", "deploy406"),
             ("result-405", "result-406"), ("speed-405", "speed-406"), ("posts-before-405", "posts-before-406")):
    s = s.replace(a, b)
for a, b in (("1.72.404", "1.72.405"), (".bak404", ".bak405")):
    s = s.replace(a, b)
doc_end = s.index('"""', 3) + 3
s = '''"""Release 1.72.406 (HAD-383 / HAD-401, rentals: the manual in the app + PDF, the former tenant's payment (B21), personal links with
Cancel, the full evidence file, honest texts; ADMINISTRATORS ONLY). GENERATED by scripts/rentals/release/gen_deploy406.py (branch
claude/rentals-proptech-v2) from deploy405.py; do not edit by hand.

Writes 7 changed rentals files (each guarded by the md5 1.72.404 wrote), 84 NEW manual files (assets/rentals/help/: he.html, en.html,
80 screenshots, 2 PDFs) and nadlan-config.php (the version, on the live text). After the checks pass, through the bridge: the
landlord's plans as two WooCommerce DRAFT products (hidden, nothing can be bought; billing stays off). Rolls back on any failed check
(.bak406, the new files removed).

  python scripts/project-stage/deploy406.py [--dry | --rollback]
"""''' + s[doc_end:]
s = re.sub(r'PHP_RELS = \[[^\]]*\][^\n]*', 'PHP_RELS = []  # 1.72.406: no PHP hunk on a live text (rest.php is a whole file pinned by md5)', s, count=1)
# the in-flight guard: 1.72.405 must be closed, and no record later than this one
g0 = s.index("# ---------------------------------------------------------------- the previous release must be closed")
g1 = s.index("# ---------------------------------------------------------------- health + bridge")
s = s[:g0] + '''# ---------------------------------------------------------------- the previous release must be closed (released or rolled back)
_prev = os.path.join(QA, "deploy-result-405.json")
if os.path.exists(_prev):
    _st = str(json.load(open(_prev, encoding="utf-8")).get("state", ""))
    if not (_st.startswith("released") or _st.startswith("rolled back")):
        raise SystemExit("FATAL: release 1.72.405 is still in flight (its record says '" + _st + "'); wait until it is closed")
for _f in sorted(os.listdir(QA)):
    if _f.startswith("deploy-result-") and _f.endswith(".json") and _f > "deploy-result-406.json":
        raise SystemExit("FATAL: a later release record exists (" + _f + "); regenerate on top of it")
_own = os.path.join(QA, "deploy-result-406.json")
if os.path.exists(_own) and "--finish" not in sys.argv[1:] and "--rollback" not in sys.argv[1:]:
    _st = str(json.load(open(_own, encoding="utf-8")).get("state", ""))
    if _st.startswith("files written") or _st.startswith("written"):
        raise SystemExit("FATAL: release 1.72.406 itself is in flight (its record says '" + _st + "'): a second run would sweep its bridge; finish it (--finish) or roll it back (--rollback)")

''' + s[g1:]
# the bridge: the plans as DRAFT products (made once, found by their meta), next to the rentals operations 1.72.404 added
BRIDGE_ADD = r"""			if ( ! empty( $b['rm_products'] ) && is_array( $b['rm_products'] ) ) { // 1.72.406 (HAD-383): the landlord's plans as DRAFT products (prices not approved; hidden; nothing can be bought)
				$res = array();
				if ( class_exists( 'WC_Product_Simple' ) && function_exists( 'wc_get_products' ) ) {
					$have = array();
					foreach ( (array) wc_get_products( array( 'limit' => 20, 'status' => array( 'publish', 'draft', 'private', 'pending' ), 'meta_key' => '_nlrm_plan' ) ) as $pp ) { $have[ (string) $pp->get_meta( '_nlrm_plan' ) ] = $pp; }
					foreach ( $b['rm_products'] as $plan => $d ) {
						if ( ! in_array( $plan, array( 'pro', 'business' ), true ) || ! is_array( $d ) ) { continue; }
						if ( isset( $have[ $plan ] ) ) { $pp = $have[ $plan ]; $res[ $plan ] = array( 'id' => (int) $pp->get_id(), 'status' => $pp->get_status(), 'price' => (string) $pp->get_regular_price(), 'visibility' => $pp->get_catalog_visibility(), 'existed' => 1 ); continue; }
						$pp = new WC_Product_Simple();
						$pp->set_name( sanitize_text_field( (string) ( $d['name'] ?? '' ) ) );
						$pp->set_status( 'draft' ); $pp->set_catalog_visibility( 'hidden' ); $pp->set_virtual( true ); $pp->set_sold_individually( true );
						$pp->set_regular_price( (string) (float) ( $d['price'] ?? 0 ) );
						$pp->set_short_description( sanitize_text_field( (string) ( $d['short'] ?? '' ) ) );
						$pp->update_meta_data( '_nlrm_plan', $plan ); $pp->update_meta_data( '_nlrm_days', 30 );
						$id = (int) $pp->save();
						$res[ $plan ] = array( 'id' => $id, 'status' => (string) get_post_status( $id ), 'price' => (string) $pp->get_regular_price(), 'visibility' => $pp->get_catalog_visibility(), 'created' => 1 );
					}
				} else {
					$res['error'] = 'WooCommerce is not loaded';
				}
				$out['rm_products'] = $res;
			}
			if ( ! empty( $b['rm_sigtest'] ) ) { // B23: the signature check compiles and decides right; the lease template version
				$tpl = function_exists( 'nlrm_json' ) ? nlrm_json( 'lease' ) : array();
				$out['rm_sigtest'] = array( 'fn' => function_exists( 'nlrm_sig_png_ok' ),
					'good' => function_exists( 'nlrm_sig_png_ok' ) && nlrm_sig_png_ok( 'data:image/png;base64,' . base64_encode( random_bytes( 3000 ) ) ),
					'short' => function_exists( 'nlrm_sig_png_ok' ) && nlrm_sig_png_ok( 'data:image/png;base64,AAAA' ),
					'store' => function_exists( 'nlrm_doc_store_bytes' ) && function_exists( 'nlrm_lease_signed_html' ),
					'lease_version' => is_array( $tpl ) ? (string) ( $tpl['version'] ?? '' ) : '' );
			}
"""
s = must_replace(s, "\t\t\tif ( ! empty( $b['rm_probe'] ) ) {", BRIDGE_ADD + "\t\t\tif ( ! empty( $b['rm_probe'] ) ) {", label="the rm_probe op (from 1.72.404)")
# the prelude: this release's files
i = s.index("WANT_LIVE = ")
j = s.index('os.makedirs(os.path.join(QA, "live-backup"), exist_ok=True)')
PRELUDE = '''WANT_LIVE = "1.72.405"  # the checks name ?ver=1.72.406: this runner is for the release right after 1.72.405
RENT_PLUG = r"''' + RENT_PLUG + '''"
FILES = ''' + json.dumps(FILES) + '''
NEWFILES = set(''' + json.dumps(HELP) + ''')
PIN = ''' + json.dumps(PIN, indent=0) + '''
LIVE404 = ''' + json.dumps({r: LIVE404[r] for r in CHANGED}) + '''  # the md5 1.72.404 wrote: each changed file must still be that on the site
RESULT = os.path.join(QA, "deploy-result-406.json")
POSTS = []
PRODUCTS = {"pro": {"name": "ניהול השכרות · פרו (חודשי)", "price": 39, "short": "עד 50 דירות. טיוטה: המחיר לא אושר."},
            "business": {"name": "ניהול השכרות · עסקי (חודשי)", "price": 199, "short": "עד 2,000 דירות. טיוטה: המחיר לא אושר."}}
NEW = {}
for rel in FILES:
    NEW[rel] = open(os.path.join(RENT_PLUG, *rel.split("/")), "rb").read()
    if md5(NEW[rel]) != PIN[rel]:
        raise SystemExit(f"FATAL: {rel} changed since gen_deploy406.py pinned it ({md5(NEW[rel])[:10]} != {PIN[rel][:10]}); run the generator again")
for rel in FILES:
    if rel.endswith(".php"):
        php_lint(NEW[rel], rel)
'''
s = s[:i] + PRELUDE + s[j:]
# served_exact: the static files only (PHP is executed, not served)
a = s.index("def served_exact(tag):")
bnd = s.index("\ndef ", a + 10)
s = s[:a] + '''def served_exact(tag):
    """each written static file as the site serves it (?ver=1.72.406), byte for byte the pinned file (PHP is executed, not served)"""
    ok = True
    for rel in FILES:
        if rel.endswith(".php"):
            continue
        path = "/wp-content/plugins/nadlan-config/" + rel + "?ver=1.72.406&nlv=" + tag
        try:
            s2, b2 = req("GET", path, raw=True, auth=False, timeout=90)
        except Exception as e:
            s2, b2 = str(e)[:60], b""
        good = s2 == 200 and md5(b2) == PIN[rel]
        if not good or not rel.endswith(".webp"):
            print(f"[served] {'OK ' if good else 'BAD'} {s2} {rel}: {md5(b2)[:10] if b2 else '-'} (want {PIN[rel][:10]})")
        ok = ok and good
    print(f"[served] {sum(1 for r in FILES if r.endswith('.webp'))} manual screenshots checked byte for byte")
    return ok

''' + s[bnd + 1:]
# a gateway error (502/503/504) on a page is the host - a cold heavy page right after the purge, seen 3.10 on /projects/ and
# /projects/hamedina-en/ while both answered 200 a moment later - not the page: one more look after a pause; any other status fails
s = must_replace(s, """            s, html = page(path + sep + "nlv=" + tag)
        except Exception as e:""", """            s, html = page(path + sep + "nlv=" + tag)
            if s in (502, 503, 504):
                print(f"[page] gateway {s} on {path[:70]}: one more look in 8 s")
                time.sleep(8)
                s, html = page(path + sep + "nlv=" + tag + "r")
        except Exception as e:""", label="verify_pages: the page fetch")
# the main
i = s.index("\ncreated = False\ntry:\n")
j = s.index("\nfinally:\n")
MAINCODE = r'''
def ops_retry(payload, what, tries=3):
    """a bridge operation that is safe to repeat (restore, unlink, purge), tried again after a dropped connection or a gateway error"""
    for k in range(tries):
        try:
            return ops(dict(payload), what)
        except SystemExit as e:
            if k == tries - 1 or not any(c in str(e) for c in ("HTTP 502", "HTTP 503", "HTTP 504")):
                raise
        except Exception:
            if k == tries - 1:
                raise
        print(f"[retry] {what}: again in {6 + 6 * k} s")
        time.sleep(6 + 6 * k)


def rollback(created_any, posts_state=None):
    """the files back from .bak406, the new files removed - every step tried again on a dropped connection (the host was unstable on 3.10)"""
    print("[rollback] restoring .bak406 files")
    for rel in ["nadlan-config.php"] + PHP_RELS + [r for r in FILES if r not in NEWFILES]:
        print("  ", rel, ops_retry({"restore": rel}, "restore " + rel).get("restore"))
    for rel in sorted(NEWFILES):
        ops_retry({"unlink": rel}, "unlink " + rel)
    print("   new files removed:", len(NEWFILES))
    ops_retry({"purge": 1}, "purge")


def put_safe(rel, data, expect=None, tries=3):
    """a write that survives a dropped connection or a gateway error (3.10: the host closed the connection on the first image
    after two 2 MB PDFs): look at what the site holds, accept it if it is already the new file, write again if it is still the
    old one, stop if it is neither"""
    for k in range(tries):
        try:
            put(rel, data, expect=expect)
            time.sleep(0.3)
            return
        except SystemExit as e:
            if not any(c in str(e) for c in ("HTTP 502", "HTTP 503", "HTTP 504")):
                raise
            err = str(e)
        except Exception as e:
            err = str(e)
        print(f"[put] {rel}: {err[:90]} - looking at the site before trying again")
        time.sleep(8 + 8 * k)
        try:
            cur = live_get(rel)
        except BaseException as e2:
            print(f"[put] {rel}: the look failed too: {str(e2)[:80]}")
            continue
        if cur.get("md5") == md5(data):
            print(f"[put] {rel}: already on the site, md5 {md5(data)[:10]} verified")
            return
        if (expect == "missing" and not cur.get("missing")) or (expect not in (None, "missing") and cur.get("md5") != expect):
            raise SystemExit(f"FATAL {rel}: after a dropped connection the site holds {cur.get('md5', 'missing')}, neither the old file nor the new one")
    raise SystemExit(f"FATAL {rel}: {tries} tries failed")


def rentals_checks(tag):
    """the rentals release as a visitor and (through the bridge) as the administrator"""
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
    for path in ("/wp-json/nadlan/v1/rm/evidence?lease_id=1", "/wp-json/nadlan/v1/rm/links"):
        s2, body = req("GET", path, raw=True, auth=False)
        say(f"a visitor gets nothing from {path.split('/rm/')[1].split('?')[0]}", s2 in (401, 403), s2)
    s2, body = req("POST", "/wp-json/nadlan/v1/rm/link-revoke", body={"id": 1}, raw=True, auth=False)
    say("a visitor cannot cancel a link", s2 in (401, 403), s2)
    init = ops({"rm_init": 1}, "rentals init")["rm_init"]
    say("the tables and the data key (unchanged)", init.get("db") == "2.1.0" and init.get("tables") == 11 and init.get("key_src") == "file" and init.get("key_ok") is True and init.get("mode") == "admin" and init.get("billing") == "off",
        {k: v for k, v in init.items() if k != "key_url"})
    pr = ops({"rm_probe": 1}, "rentals probe")["rm_probe"]
    need = ["/nadlan/v1/rm/boot", "/nadlan/v1/rm/pay", "/nadlan/v1/rm/evidence", "/nadlan/v1/rm/links", "/nadlan/v1/rm/link-revoke", "/nadlan/v1/rm/lease-end", "/nadlan/v1/rm/portal", "/nadlan/v1/rm/export"]
    say("/rm/boot as the administrator", pr.get("status") == 200 and pr.get("role") == "owner" and pr.get("key_ok") is True and pr.get("billing") == "off" and pr.get("v2") is True,
        {k: pr.get(k) for k in ("status", "role", "key_ok", "plan", "billing", "v2")})
    say("the routes are registered (with /rm/evidence)", all(r in pr.get("routes", []) for r in need), [r for r in need if r not in pr.get("routes", [])])
    return ok


created = False
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
    FINISH = "--finish" in ARGS
    if FINISH:
        # a run cut after its writes (3.10 run 3: another session's dry run swept the bridge during the checks): the files are
        # on the site; check they are exactly this release's, then run every check, the products and the signature test
        if LIVE_VER != "1.72.406":
            raise SystemExit(f"FATAL --finish: live is {LIVE_VER}, not 1.72.406")
        prev = json.load(open(RESULT, encoding="utf-8"))
        if not str(prev.get("state", "")).startswith("files written"):
            raise SystemExit("FATAL --finish: the record says '" + str(prev.get("state")) + "', not 'files written, checks pending'")
        REC.update(prev)
        FILES_MD5 = prev["files"]
        for rel in FILES:
            cur = live_get(rel)
            if cur.get("md5") != PIN[rel]:
                raise SystemExit(f"FATAL --finish: live {rel} is {cur.get('md5', 'missing')}, not this release's {PIN[rel][:10]}")
        if live_get("nadlan-config.php").get("md5") != FILES_MD5.get("nadlan-config.php"):
            raise SystemExit("FATAL --finish: nadlan-config.php is not the one this release wrote")
        old, new, created = "1.72.405", "1.72.406", True
        print(f"[finish] the {len(FILES)} files and nadlan-config.php are exactly what run 3 wrote; checking again from the start")
    else:
        if LIVE_VER != WANT_LIVE:
            raise SystemExit(f"FATAL: live is {LIVE_VER}, this runner is for {WANT_LIVE} -> 1.72.406 (its checks name the version); regenerate it")
        for rel in FILES:
            cur = live_get(rel)
            if rel in NEWFILES:
                if not cur.get("missing"):
                    raise SystemExit(f"FATAL: {rel} already exists on the site; this release makes it new")
            elif cur.get("missing") or cur.get("md5") != LIVE404[rel]:
                raise SystemExit(f"FATAL drift: live {rel} is {cur.get('md5', 'missing')}, not what 1.72.404 wrote ({LIVE404[rel][:10]})")
        print(f"[drift] {len(FILES) - len(NEWFILES)} changed files are exactly what 1.72.404 wrote; {len(NEWFILES)} manual files are new")
        cur_main = live_get("nadlan-config.php")
        live_main = base64.b64decode(cur_main["b64"])
        stamp = time.strftime("%Y%m%dT%H%M%S")
        if not DRY:
            open(os.path.join(QA, "live-backup", f"nadlan-config.php.{stamp}.live"), "wb").write(live_main)
        text = live_main.decode("utf-8")
        m = re.search(r"\* Version: (\d+)\.(\d+)\.(\d+)", text)
        old = ".".join(m.groups())
        new = f"{m.group(1)}.{m.group(2)}.{int(m.group(3)) + 1}"
        if new != "1.72.406":
            raise SystemExit(f"FATAL: the bump would be {old} -> {new}, not 1.72.406")
        for a, b2 in ((f" * Version: {old}", f" * Version: {new}"), (f"define( 'NADLAN_CONFIG_VERSION', '{old}' )", f"define( 'NADLAN_CONFIG_VERSION', '{new}' )")):
            n = text.count(a)
            if n != 1:
                raise SystemExit(f"FATAL anchor x{n} in nadlan-config.php: {a}")
            text = text.replace(a, b2)
        if "rentals-manager" not in text:
            raise SystemExit("FATAL: nadlan-config.php does not load rentals-manager")
        new_main = text.encode("utf-8")
        php_lint(new_main, "nadlan-config.php (live text, bumped)")
        print(f"[plan] {old} -> {new}; {len(FILES) - len(NEWFILES)} changed + {len(NEWFILES)} new files, nadlan-config.php (version); then 2 DRAFT products; no option, no post")
        if DRY:
            print("[dry] no writes")
            raise SystemExit(0)

        REC.update({"released": new, "from": old, "live_before": dict(LIVE404, **{"nadlan-config.php": md5(live_main)})})
        FILES_MD5 = dict({rel: md5(NEW[rel]) for rel in FILES}, **{"nadlan-config.php": md5(new_main)})
        try:
            created = True
            for rel in FILES:
                put_safe(rel, NEW[rel], expect=("missing" if rel in NEWFILES else LIVE404[rel]))
            put_safe("nadlan-config.php", new_main, expect=md5(live_main))
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
    record("released and verified", files=FILES_MD5, checks="verify_pages + served_exact (the 7 changed + 84 manual files at ?ver=1.72.406, byte for byte) + verify_order + verify_home_order + verify_kh + rentals_checks (visitor v1, 410 portal, no visitor evidence/links/cancel, tables 11 + key, /rm/boot as admin, /rm/evidence registered): OK")
    # the plans as DRAFT products, once (a file rollback would not touch them; drafts are hidden and cannot be bought)
    pd = ops({"rm_products": PRODUCTS}, "plans as draft products").get("rm_products", {})
    good = all(isinstance(pd.get(k), dict) and pd[k].get("status") == "draft" and pd[k].get("visibility") == "hidden" for k in ("pro", "business"))
    print(f"[products] {'OK ' if good else 'BAD'} " + json.dumps(pd, ensure_ascii=False))
    pr = ops({"rm_probe": 1}, "rentals probe after the products")["rm_probe"]
    print(f"[products] billing after: {pr.get('billing')} (must stay off; no offer is shown while it is off)")
    st = ops({"rm_sigtest": 1}, "signature self-test").get("rm_sigtest", {})
    sgood = st.get("fn") is True and st.get("good") is True and st.get("short") is False and st.get("store") is True and st.get("lease_version") == "2026-10-03.1"
    print(f"[sign] {'OK ' if sgood else 'BAD'} " + json.dumps(st, ensure_ascii=False))
    record("released and verified", files=FILES_MD5, products=pd, sigtest=st, checks="see above; products: " + ("two drafts, hidden" if good else "NOT as expected, see the log") + "; signature self-test: " + ("OK" if sgood else "NOT as expected"))
    print("RELEASE 1.72.406 LIVE: HAD-383/HAD-401 rentals for ADMINISTRATORS: the manual (app + PDF), B21, personal links with Cancel, the full evidence file, signing works again (B23), the signed text kept (B22), clause numbers in order; plans as draft products")
'''
s = s[:i] + MAINCODE + s[j:]
for must in ("def verify_kh(", "def verify_home_order(", "def run_checks(", "def rollback(", "rm_products", "deploy-result-406.json", 'WANT_LIVE = "1.72.405"'):
    if must not in s:
        raise SystemExit("FATAL generator: the runner lacks " + must)
if "1.72.404" in s.replace("1.72.404 wrote", "").replace("what 1.72.404", "").replace("(from 1.72.404)", "").replace("1.72.404 added", ""):
    hits = sorted(set(m.start() for m in re.finditer(r"1\.72\.404", s)))
    print("[note] 1.72.404 still named at", len(hits), "places (comments / the drift pins)")
io.open(OUT, "w", encoding="utf-8", newline="\n").write(s)
r = subprocess.run([sys.executable, "-m", "py_compile", OUT], capture_output=True, text=True)
if r.returncode:
    raise SystemExit("FATAL: deploy406.py does not compile: " + r.stderr[-500:])
print("written", OUT, len(s), "chars")
