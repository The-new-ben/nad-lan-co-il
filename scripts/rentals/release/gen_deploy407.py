# -*- coding: utf-8 -*-
"""Writes scripts/project-stage/deploy407.py in the main checkout: release 1.72.407 = HAD-383 rentals B22/B23 + clause numbers, still ADMINISTRATORS
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
SRC = io.open(os.path.join(PS, "deploy406.py"), encoding="utf-8").read()
OUT = os.path.join(PS, "deploy407.py")


def md5(b):
    return hashlib.md5(b).hexdigest()


def must_replace(text, old, new, n=1, label=""):
    c = text.count(old)
    if c != n:
        raise SystemExit(f"FATAL generator: {label or old[:80]!r} x{c} (want {n})")
    return text.replace(old, new)


# ---------------------------------------------------------------- what 1.72.404 wrote (the live md5 each changed file must still have)
R404 = json.load(open(os.path.join(QA, "deploy-result-406.json"), encoding="utf-8"))  # the release this one chains on (1.72.406)
if not str(R404.get("state", "")).startswith("released"):
    raise SystemExit("FATAL: release 1.72.406 is not 'released': " + str(R404.get("state")))
R0 = json.load(open(os.path.join(QA, "deploy-result-404.json"), encoding="utf-8"))  # the rentals files 1.72.404 wrote and 406 did not touch
LIVE404 = {k: v for k, v in R0["files"].items() if k not in ("nadlan-config.php", "inc/rentals-manager.php")}
LIVE404.update({k: v for k, v in R404["files"].items() if k != "nadlan-config.php" and not k.startswith("assets/rentals/help/")})
CHANGED, SAME = [], []
for rel, h in LIVE404.items():
    cur = md5(open(os.path.join(RENT_PLUG, *rel.split("/")), "rb").read())
    (CHANGED if cur != h else SAME).append(rel)
HELP = []  # 1.72.407 adds no file
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
for need in ("links_title", "link_revoke", "help_pdf"):
    if need not in H:
        raise SystemExit("FATAL: the string table lacks " + need)
REST = open(os.path.join(RENT_PLUG, "inc/rentals/rest.php"), encoding="utf-8").read()
if "'/rm/evidence'" not in REST or "function nlrm_doc_store_bytes(" not in REST:
    raise SystemExit("FATAL: rest.php lacks /rm/evidence or nlrm_doc_store_bytes")
PORTAL = open(os.path.join(RENT_PLUG, "inc/rentals/portal.php"), encoding="utf-8").read()
if "function nlrm_sig_png_ok(" not in PORTAL or "{200,400000}$" in PORTAL:
    raise SystemExit("FATAL: portal.php still has the uncompilable signature regex")
if '"version": "2026-10-03.1"' not in open(os.path.join(RENT_PLUG, "assets/rentals/i18n/lease.json"), encoding="utf-8").read():
    raise SystemExit("FATAL: lease.json is not 2026-10-03.1")
imgs = []
total = sum(os.path.getsize(os.path.join(RENT_PLUG, *r.split("/"))) for r in FILES)
print(f"[gate] {len(CHANGED)} changed ({', '.join(CHANGED)}), {len(SAME)} unchanged since 1.72.404, {len(HELP)} new manual files ({len(imgs)} images, 2 PDFs); "
      f"{total:,} bytes; he/en parity {len(H)} strings")

# ---------------------------------------------------------------- the runner, from deploy405.py
s = SRC
for a, b in (("1.72.406", "1.72.407"), (".bak406", ".bak407"), ("PS406", "PS407"), ("ps406", "ps407"), ("gen_deploy406", "gen_deploy407"), ("deploy406", "deploy407"),
             ("result-406", "result-407"), ("speed-406", "speed-407"), ("posts-before-406", "posts-before-407")):
    s = s.replace(a, b)
for a, b in (("1.72.405", "1.72.406"), (".bak405", ".bak406")):
    s = s.replace(a, b)
doc_end = s.index('"""', 3) + 3
s = '''"""Release 1.72.407 (HAD-383 B23 + B22: a tenant can sign through the sign link again - the signature check never compiled
since 1.72.404 - and the exact signed text is kept as an encrypted lease document; the lease's clause numbers run in order;
ADMINISTRATORS ONLY). GENERATED by scripts/rentals/release/gen_deploy407.py (branch claude/rentals-proptech-v2) from deploy406.py; do
not edit by hand.

Writes the changed rentals files (each guarded by the md5 the live site must have: 1.72.406's or 1.72.404's) and nadlan-config.php
(the version). Through the bridge after the checks: nlrm_sig_png_ok accepts a real signature and refuses a short one, the lease
template is 2026-10-03.1. Rolls back on any failed check (.bak407).

  python scripts/project-stage/deploy407.py [--dry | --rollback]
"""''' + s[doc_end:]
s = re.sub(r'PHP_RELS = \[[^\]]*\][^\n]*', 'PHP_RELS = []  # 1.72.407: no PHP hunk on a live text (rest.php is a whole file pinned by md5)', s, count=1)
# the in-flight guard: 1.72.406 must be closed, and no record later than this one
g0 = s.index("# ---------------------------------------------------------------- the previous release must be closed")
g1 = s.index("# ---------------------------------------------------------------- health + bridge")
s = s[:g0] + '''# ---------------------------------------------------------------- the previous release must be closed (released or rolled back)
_prev = os.path.join(QA, "deploy-result-406.json")
if os.path.exists(_prev):
    _st = str(json.load(open(_prev, encoding="utf-8")).get("state", ""))
    if not (_st.startswith("released") or _st.startswith("rolled back")):
        raise SystemExit("FATAL: release 1.72.406 is still in flight (its record says '" + _st + "'); wait until it is closed")
for _f in sorted(os.listdir(QA)):
    if _f.startswith("deploy-result-") and _f.endswith(".json") and _f > "deploy-result-407.json":
        raise SystemExit("FATAL: a later release record exists (" + _f + "); regenerate on top of it")

''' + s[g1:]
# the bridge: the plans as DRAFT products (made once, found by their meta), next to the rentals operations 1.72.404 added
BRIDGE_ADD = r"""			if ( ! empty( $b['rm_sigtest'] ) ) { // 1.72.407 (B23): the signature check compiles and decides right; the lease template version
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
PRELUDE = '''WANT_LIVE = "1.72.406"  # the checks name ?ver=1.72.407: this runner is for the release right after 1.72.406
RENT_PLUG = r"''' + RENT_PLUG + '''"
FILES = ''' + json.dumps(FILES) + '''
NEWFILES = set(''' + json.dumps(HELP) + ''')
PIN = ''' + json.dumps(PIN, indent=0) + '''
LIVE404 = ''' + json.dumps({r: LIVE404[r] for r in CHANGED}) + '''  # the md5 1.72.404 wrote: each changed file must still be that on the site
RESULT = os.path.join(QA, "deploy-result-407.json")
POSTS = []
NEW = {}
for rel in FILES:
    NEW[rel] = open(os.path.join(RENT_PLUG, *rel.split("/")), "rb").read()
    if md5(NEW[rel]) != PIN[rel]:
        raise SystemExit(f"FATAL: {rel} changed since gen_deploy407.py pinned it ({md5(NEW[rel])[:10]} != {PIN[rel][:10]}); run the generator again")
for rel in FILES:
    if rel.endswith(".php"):
        php_lint(NEW[rel], rel)
'''
s = s[:i] + PRELUDE + s[j:]
# served_exact: the static files only (PHP is executed, not served)
a = s.index("def served_exact(tag):")
bnd = s.index("\ndef ", a + 10)
s = s[:a] + '''def served_exact(tag):
    """each written static file as the site serves it (?ver=1.72.407), byte for byte the pinned file (PHP is executed, not served)"""
    ok = True
    for rel in FILES:
        if rel.endswith(".php"):
            continue
        path = "/wp-content/plugins/nadlan-config/" + rel + "?ver=1.72.407&nlv=" + tag
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
    if LIVE_VER != WANT_LIVE:
        raise SystemExit(f"FATAL: live is {LIVE_VER}, this runner is for {WANT_LIVE} -> 1.72.407 (its checks name the version); regenerate it")
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
    if new != "1.72.407":
        raise SystemExit(f"FATAL: the bump would be {old} -> {new}, not 1.72.407")
    for a, b2 in ((f" * Version: {old}", f" * Version: {new}"), (f"define( 'NADLAN_CONFIG_VERSION', '{old}' )", f"define( 'NADLAN_CONFIG_VERSION', '{new}' )")):
        n = text.count(a)
        if n != 1:
            raise SystemExit(f"FATAL anchor x{n} in nadlan-config.php: {a}")
        text = text.replace(a, b2)
    if "rentals-manager" not in text:
        raise SystemExit("FATAL: nadlan-config.php does not load rentals-manager")
    new_main = text.encode("utf-8")
    php_lint(new_main, "nadlan-config.php (live text, bumped)")
    print(f"[plan] {old} -> {new}; {len(FILES) - len(NEWFILES)} changed files, nadlan-config.php (version); then the signature self-test; no option, no post")
    if DRY:
        print("[dry] no writes")
        raise SystemExit(0)

    REC.update({"released": new, "from": old, "live_before": dict(LIVE404, **{"nadlan-config.php": md5(live_main)})})
    FILES_MD5 = dict({rel: md5(NEW[rel]) for rel in FILES}, **{"nadlan-config.php": md5(new_main)})
    try:
        created = True
        for rel in FILES:
            put(rel, NEW[rel], expect=("missing" if rel in NEWFILES else LIVE404[rel]))
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
    record("released and verified", files=FILES_MD5, checks="verify_pages + served_exact (the 7 changed + 84 manual files at ?ver=1.72.407, byte for byte) + verify_order + verify_home_order + verify_kh + rentals_checks (visitor v1, 410 portal, no visitor evidence/links/cancel, tables 11 + key, /rm/boot as admin, /rm/evidence registered): OK")
    st = ops({"rm_sigtest": 1}, "signature self-test").get("rm_sigtest", {})
    good = st.get("fn") is True and st.get("good") is True and st.get("short") is False and st.get("store") is True and st.get("lease_version") == "2026-10-03.1"
    print(f"[sign] {'OK ' if good else 'BAD'} " + json.dumps(st, ensure_ascii=False))
    record("released and verified", files=FILES_MD5, sigtest=st, checks="see above; signature self-test " + ("OK" if good else "NOT as expected, see the log"))
    print("RELEASE 1.72.407 LIVE: HAD-383 rentals for ADMINISTRATORS: signing through the link works again (B23), the signed text kept (B22), clause numbers in order")
'''
s = s[:i] + MAINCODE + s[j:]
for must in ("def verify_kh(", "def verify_home_order(", "def run_checks(", "def rollback(", "rm_sigtest", "deploy-result-407.json", 'WANT_LIVE = "1.72.406"'):
    if must not in s:
        raise SystemExit("FATAL generator: the runner lacks " + must)
if "1.72.404" in s.replace("1.72.404 wrote", "").replace("what 1.72.404", "").replace("(from 1.72.404)", "").replace("1.72.404 added", ""):
    hits = sorted(set(m.start() for m in re.finditer(r"1\.72\.404", s)))
    print("[note] 1.72.404 still named at", len(hits), "places (comments / the drift pins)")
io.open(OUT, "w", encoding="utf-8", newline="\n").write(s)
r = subprocess.run([sys.executable, "-m", "py_compile", OUT], capture_output=True, text=True)
if r.returncode:
    raise SystemExit("FATAL: deploy407.py does not compile: " + r.stderr[-500:])
print("written", OUT, len(s), "chars")
