# -*- coding: utf-8 -*-
"""make deploy602.py from deploy601.py: 1.72.602 the visit trail (HAD-678, Ben 7.11.2026): "record what visitors click and choose on the
project pages, show me who clicked what" (Hotjar cannot see inside the 3D stage).
Built and tested in docs/research/2026-11-07-campaign-network/build/build-visit-trail/ (node test_trail.js, PHP test_visit_trail.php on
WordPress stubs, browser verify.py on the saved live copy of /projects/rainbow-tel-aviv/); this generator runs the two unit suites again and
refuses unless verify.json passed on the very trail.js it pins.
  NEW assets/visit-trail/trail.js  the recorder (window.NL_TRAIL): listens to the stage's own nl:* window events and to CTA taps, batches to
                                   POST /wp-json/nadlan/v1/trail every 20 s and on pagehide; nothing under GPC / Do Not Track / webdriver.
                                   assets/showroom-engine/engine.js and the stage files are NOT touched (it only listens).
  NEW inc/visit-trail.php          the route, the two tables (dbDelta, created on the first admin page view or the first batch), the lead link
                                   (wp_after_insert_post on nadlan_lead: no lead module is edited), the admin screen "מסלולי ביקור" under Lead
                                   Inbox, the box on the lead's edit screen, the leads list column, the timeline in the rich new-lead email
                                   (the action nadlan_lead_rich_alert + wp_mail), the 12-month daily clean-up, the healthcheck line
                                   visit_trail 1.0.0. Enqueues trail.js on project stage pages only (nadlan_ps_current()).
Hunks on the LIVE text (ashira_602.py): nadlan-config.php only: 'visit-trail' after 'campaign-brief' at the end of the module list (the list
1.72.599 wrote and 1.72.600 / 1.72.601 kept, proven again by the runner on the live text), applied on the bumped live text (one write).
No other PHP file is hunked (RELS = []): PHP_RELS = ['nadlan-config.php'], restored from .bak602 on rollback before the two new files go.
No page, post, option or meta is written by the release. The privacy policy paragraph is a separate, later step:
scripts/legal/privacy_visit_trail.py (dry by default; --go after this release is live and verified).
The repo nadlan-config.php is NOT touched (its module list is not the live one)."""
import hashlib, io, json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
D = os.path.join(REPO, "docs", "research", "2026-11-07-campaign-network", "build", "build-visit-trail")
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
NL = chr(10)
FILES = ["assets/visit-trail/trail.js", "inc/visit-trail.php"]
RELS = []                         # no inc/ file is hunked: the module hooks in
PHP_RELS = ["nadlan-config.php"]  # the one hunked PHP file (the module list): restored from .bak602 on rollback
for _r in FILES:
    assert os.path.exists(os.path.join(PLUG, *_r.split("/"))), "missing " + _r
PIN = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}

# ---------------------------------------------------------------- the two files are the tested ones
_js = io.open(os.path.join(PLUG, "assets", "visit-trail", "trail.js"), encoding="utf-8").read()
_php = io.open(os.path.join(PLUG, "inc", "visit-trail.php"), encoding="utf-8").read()
assert "NadLan visit trail 1.0.0" in _js and "var VERSION = '1.0.0';" in _js and "window.NL_TRAIL_CFG" in _js and "'X-NL-Visit'" in _js, "trail.js is not 1.0.0"
assert "define( 'NADLAN_VT_VERSION', '1.0.0' );" in _php and "register_rest_route( 'nadlan/v1', '/trail'" in _php and "add_action( 'wp_after_insert_post', 'nadlan_vt_after_insert', 5, 3 );" in _php, "visit-trail.php is not 1.0.0"
assert "function nadlan_vt_selftest()" in _php and "nadlan_ps_current()" in _php and "add_submenu_page( 'nadlan-inbox', 'מסלולי ביקור'" in _php, "visit-trail.php: selftest / stage gate / screen"
assert "engine.js" not in re.sub(r"/\*[\s\S]*?\*/", "", _js) and "showroom-engine" not in re.sub(r"/\*[\s\S]*?\*/|//[^\n]*", "", _js), "trail.js must not reach into the frozen engine"
for _n, _t in (("trail.js", _js), ("visit-trail.php", _php)):
    assert not re.search("[–—]", _t), "long dash in " + _n
for _cmd, _what in ((["node", os.path.join(D, "test_trail.js")], "node test_trail.js"), (["php", os.path.join(D, "test_visit_trail.php")], "php test_visit_trail.php")):
    _o = subprocess.run(_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    _last = (_o.stdout.strip().splitlines() or ["(no output)"])[-1]
    assert _o.returncode == 0 and "passed" in _last and "FAILED" not in _last, _what + ": " + _last
    print("[tests]", _what + ":", _last)
_vj = json.load(io.open(os.path.join(D, "verify.json"), encoding="utf-8"))
assert _vj.get("failed") == 0 and _vj.get("passed", 0) >= 90, "verify.json: the browser run did not pass"
assert _vj.get("trail_md5") == PIN["assets/visit-trail/trail.js"], "verify.json was made on another trail.js (%s); run verify.py again" % str(_vj.get("trail_md5"))[:10]
print("[tests] verify.py (browser, saved live page): %d of %d passed on this trail.js" % (_vj["passed"], _vj["passed"] + _vj["failed"]))

# ---------------------------------------------------------------- the module list hunk (on the live text the runner reads)
sys.path.insert(0, H)
import ashira_601 as P601  # noqa: E402  the live module list 1.72.599 wrote, kept by 1.72.600 and 1.72.601
ML = P601.MAIN_LIST
assert ML.endswith("'mortgage-market', 'campaign-brief' ) as $nadlan_mod") and ML.count("'campaign-brief'") == 1 and "'visit-trail'" not in ML, ML[-80:]
ML_NEW = ML.replace("'campaign-brief' ) as $nadlan_mod", "'campaign-brief', 'visit-trail' ) as $nadlan_mod")
assert ML_NEW != ML and ML_NEW.count("'visit-trail'") == 1
HUNKS = {"nadlan-config.php": [(ML, ML_NEW, 1)]}
ABSENT = {"nadlan-config.php": ["'visit-trail'"]}
_p601 = os.path.join(QA, "deploy-result-601.json")
assert os.path.exists(_p601) and str(json.load(open(_p601, encoding="utf-8")).get("state", "")).startswith("released"), "1.72.601 is not released and verified"

# ---------------------------------------------------------------- ashira_602.py
AP = ["# -*- coding: utf-8 -*-",
      '"""Release 1.72.602 (HAD-678, the visit trail): one hunk on the LIVE nadlan-config.php module list (apply_main, on the bumped text):',
      "'visit-trail' after 'campaign-brief'. No other file is hunked (RELS is empty: the runner's PX loop does nothing). The anchor must be found",
      "exactly once and 'visit-trail' must be absent, or the release stops before any write. Generated by make_deploy602.py.\"\"\"",
      "RELS = " + repr(RELS), "HUNKS = " + repr(HUNKS), "ABSENT = " + repr(ABSENT), "LIVE_MD5 = {}", "PROOF = {}",
      "MAIN_LIST = " + repr(ML), "MAIN_NEW = " + repr(ML_NEW), "", "",
      "def apply(rel, txt):", "    if rel not in HUNKS:", "        raise SystemExit('ashira_602: no hunk on ' + rel)",
      "    for s in ABSENT.get(rel, []):", "        if s in txt:",
      "            raise SystemExit('ashira_602: FATAL: the live %s already holds %r; read it before releasing' % (rel, s))",
      "    for old, new, n in HUNKS[rel]:", "        if new in txt:", "            raise SystemExit('ashira_602: FATAL: the live %s already holds the new text' % rel)",
      "        k = txt.count(old)", "        if k != n:", "            raise SystemExit('ashira_602: FATAL: anchor x%d (want %d) in the live %s: %r' % (k, n, rel, old[:90]))",
      "        txt = txt.replace(old, new)", "    return txt", "", "",
      "def apply_main(txt):", '    """the module list of the bumped live nadlan-config.php: \'visit-trail\' after \'campaign-brief\', once"""',
      "    txt = apply('nadlan-config.php', txt)", "    if txt.count(MAIN_NEW) != 1:",
      "        raise SystemExit('ashira_602: FATAL: the module list does not end with visit-trail exactly once')", "    return txt", ""]
open(os.path.join(H, "ashira_602.py"), "w", encoding="utf-8", newline="\n").write("\n".join(AP))

# ---------------------------------------------------------------- deploy602.py from deploy601.py
src = open(os.path.join(H, "deploy601.py"), encoding="utf-8").read()


def one(old, new, what):
    global src
    n = src.count(old)
    assert n == 1, "%s: anchor x%d" % (what, n)
    src = src.replace(old, new)


for a, b in [("1.72.601", "1.72.602"), ("ps601", "ps602"), ("bak601", "bak602"), ("make_deploy601", "make_deploy602"),
             ("deploy-result-601", "deploy-result-602"), ("speed-601", "speed-602"), ("posts-before-601", "posts-before-602"),
             ("deploy-result-600", "deploy-result-601"), ("1.72.600", "1.72.601")]:
    src = src.replace(a, b)
BS = chr(92)
src = re.sub(r"\?t601([a-z]?)=1", "?t602" + BS + "1=1", src)
src = re.sub(r"&t601([a-z]?)=1", "&t602" + BS + "1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(601, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import ashira_601 as PX  # noqa: E402 \(.*$", "import ashira_602 as PX  # noqa: E402 (1.72.602: the visit trail; the module list only, no inc/ hunk)", src, flags=re.M); assert n == 1, n
src, n = re.subn(r'print\("RELEASE 1\.72\.602 LIVE: [^"]*"\)',
                 'print("RELEASE 1.72.602 LIVE: the visit trail (HAD-678): assets/visit-trail/trail.js + inc/visit-trail.php, \'visit-trail\' in the module list; the admin screen מסלולי ביקור under Lead Inbox. NEXT: python scripts/legal/privacy_visit_trail.py (dry), then --go")', src); assert n == 1, n
lines = src.split("\n")
seen = set()
for k, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
    elif l.startswith("NEWFILES = "):
        lines[k] = "NEWFILES = set(" + repr(sorted(FILES)) + ")  # 1.72.602: the recorder and its module, both new"; seen.add("NEWFILES")
    elif l.startswith("FILES = ["):
        lines[k] = "FILES = " + repr(FILES); seen.add("FILES")
    elif l.startswith("PHP_RELS = ["):
        lines[k] = "PHP_RELS = " + repr(PHP_RELS) + "  # 1.72.602: the one hunked PHP file (the module list), restored from .bak602 on rollback"; seen.add("PHP_RELS")
assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
src = "\n".join(lines)

# the module list: proven to be the 1.72.599 list on the live text, then 'visit-trail' joins it (one write of the main file, as 1.72.599 did)
one("    print(\"[plan] nadlan-config.php: the version only; the module list stays as 1.72.599 wrote it ('mortgage-market', 'campaign-brief' last)\")\n",
    "    text = PX.apply_main(text)  # 1.72.602 (HAD-678): 'visit-trail' joins the module list after 'campaign-brief' (ashira_602, anchor x1)\n"
    "    print(\"[plan] nadlan-config.php: the module list now ends 'campaign-brief', 'visit-trail'\")\n", "module hunk")

# the bridge: the module's self-test on the live PHP, as the runner's own admin user (creates its two tables once, as its admin_init would)
one("\t\t\tif ( ! empty( $b['purge'] ) ) {",
    "\t\t\tif ( ! empty( $b['vt_probe'] ) ) { // 1.72.602: the visit trail on the live PHP (tables, a sample batch cleaned, the admin screen); no visit row written\n"
    "\t\t\t\ttry { $out['vt_probe'] = function_exists( 'nadlan_vt_selftest' ) ? nadlan_vt_selftest() : array( 'fn' => 0 ); } catch ( \\Throwable $e ) { $out['vt_probe'] = array( 'err' => substr( $e->getMessage(), 0, 200 ) ); }\n"
    "\t\t\t}\n"
    "\t\t\tif ( ! empty( $b['purge'] ) ) {", "bridge vt_probe")

# the pages after the release: trail.js and its config on stage pages (he, en, a world page, DUO), the file as served, never elsewhere
T = "/wp-content/plugins/nadlan-config/assets/visit-trail/trail.js"
CFG = 'window.NL_TRAIL_CFG={"endpoint":"https://nad-lan.co.il/wp-json/nadlan/v1/trail"'
ADD = [(T + "?t602x=1", ["NadLan visit trail 1.0.0", "NL_TRAIL_CFG", "'nl:facing'", "X-NL-Visit", "globalPrivacyControl"], ["Fatal error"]),
       ("/projects/rainbow-tel-aviv/?t602v=1", ["assets/visit-trail/trail.js?ver=1.72.602", CFG, '"lang":"he"', 'id="nlps"'], ["Fatal error"]),
       ("/projects/rainbow-tel-aviv-en/?t602v=1", ["assets/visit-trail/trail.js?ver=1.72.602", CFG, '"lang":"en"'], ["Fatal error"]),
       ("/projects/hamedina/?t602v=1", ["assets/visit-trail/trail.js?ver=1.72.602", CFG], ["Fatal error"]),
       ("/projects/duo-tel-aviv/?t602v=1", ["assets/visit-trail/trail.js?ver=1.72.602", CFG], ["Fatal error"]),
       ("/mortgage-calculator/?t602n=1", ['data-nli="mquick"'], ["Fatal error"], ["visit-trail/trail.js", "NL_TRAIL_CFG"]),
       ("/?t602n=1", ['<body'], ["Fatal error"], ["visit-trail/trail.js", "NL_TRAIL_CFG"]),
       ("/projects/h-infinity-somail-tel-aviv/?t602n=1", ["nadlan-project-article"], ["Fatal error"], ["visit-trail/trail.js", "NL_TRAIL_CFG"])]
_ca = [l for l in src.split("\n") if l.startswith("    ('/wp-content/plugins/nadlan-config/assets/instruments/tools/nlbudget.js?t602x=1',")]
assert len(_ca) == 1, len(_ca)
src = src.replace(_ca[0], "".join("    (%s),\n" % ", ".join(repr(x) for x in t) for t in ADD) + _ca[0], 1)

VERIFY_VT = '''def verify_vt():
    """1.72.602 (HAD-678): the visit trail is loaded and works on the live PHP. /healthcheck carries visit_trail 1.0.0, on; POST
    /wp-json/nadlan/v1/trail answers 400 nlvt_bad to an empty body (404 = the route is not registered; an empty body is refused before
    anything is stored or counted); the bridge's vt_probe (the runner's own admin user) finds the two tables (created once, as the module's
    admin_init would), keeps 4 of the 5 sample events with the phone dropped, renders the screen "מסלולי ביקור", and sees the REST route
    and the lead hook. No visit row is written by these checks."""
    ok = True
    try:
        s, h2 = req("GET", "/wp-json/nadlan/v1/healthcheck?nlv=vt" + str(int(time.time())), auth=False)
    except Exception as e:
        s, h2 = str(e)[:60], {}
    vt = h2.get("visit_trail") if isinstance(h2, dict) else None
    good = s == 200 and isinstance(h2, dict) and h2.get("version") == "1.72.602" and isinstance(vt, dict) and vt.get("version") == "1.0.0" and vt.get("on") is True
    print(f"[vt] {'OK ' if good else 'BAD'} /healthcheck {s} {h2.get('version') if isinstance(h2, dict) else '-'} visit_trail {json.dumps(vt, ensure_ascii=False)}")
    ok = ok and good
    r = urllib.request.Request(BASE + "/wp-json/nadlan/v1/trail", data=b"", method="POST", headers={"User-Agent": UA, "Content-Type": "text/plain;charset=UTF-8"})
    try:
        with urllib.request.urlopen(r, timeout=60) as resp:
            s2, b2 = resp.status, resp.read()
    except urllib.error.HTTPError as e:
        s2, b2 = e.code, e.read()
    except Exception as e:
        s2, b2 = str(e)[:60], b""
    good = s2 == 400 and b'"nlvt_bad"' in b2
    print(f"[vt] {'OK ' if good else 'BAD'} POST /wp-json/nadlan/v1/trail, empty body: {s2} {b2[:160].decode('utf-8', 'replace')} (want 400 nlvt_bad)")
    ok = ok and good
    try:
        s3, r3 = req("POST", "/wp-json/" + NS + "/v1/apply", body={"token": TOKEN, "vt_probe": 1}, timeout=120)
    except Exception as e:
        s3, r3 = str(e)[:60], {}
    p = r3.get("vt_probe") if isinstance(r3, dict) else None
    good = (s3 == 200 and isinstance(p, dict) and p.get("version") == "1.0.0" and p.get("db") == 1 and p.get("tables") == 1 and p.get("clean") == 4
            and p.get("no_phone") == 1 and p.get("admin_title") == 1 and p.get("route") is True and p.get("lead_hook") is True and p.get("on") is True)
    print(f"[vt] {'OK ' if good else 'BAD'} {s3} the module on the live PHP: {json.dumps(p, ensure_ascii=False)[:400]}")
    return ok and good


def run_checks(tag):'''
one("def run_checks(tag):", VERIFY_VT, "verify_vt def")
one('    if not bad and not verify_ac():\n        bad = ["advertiser-center"]\n    return bad',
    '    if not bad and not verify_ac():\n        bad = ["advertiser-center"]\n    if not bad and not verify_vt():\n        bad = ["visit-trail"]\n    return bad', "verify_vt hook")
src, n = re.subn(r'checks="verify_pages \+ served_exact [^"]*"',
                 'checks="verify_pages + served_exact (trail.js at ?ver=1.72.602, byte for byte) + verify_order + verify_home_order + verify_kh + verify_nlb + verify_mkt + verify_ac + verify_vt: OK"', src); assert n == 1, n
assert "ashira_601" not in src and "t601" not in src and "deploy-result-600" not in src, "a 601 marker is left"
assert "601" not in "".join(l for l in src.split("\n") if l.startswith(("PIN = ", "NEWFILES = ", "FILES = ", "PHP_RELS = ", "BAK = ", "NS = ")))
assert src.count('WANT_LIVE = "1.72.601"') == 1 and src.count('BAK = ".bak602"') == 1 and src.count("range(601, 329, -1)") == 1 and src.count("PX.apply_main(text)") == 1
assert src.count("$b['vt_probe']") == 1 and src.count('"vt_probe": 1') == 1 and src.count("def verify_vt():") == 1
open(os.path.join(H, "deploy602.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy602.py + ashira_602.py written | t602 markers:", len(re.findall(r"t602[a-z]?=1", src)),
      "| pins:", {k.split("/")[-1]: v[:10] for k, v in PIN.items()}, "| PHP_RELS:", PHP_RELS, "| module list: ... 'campaign-brief', 'visit-trail'")
