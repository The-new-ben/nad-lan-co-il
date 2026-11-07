# -*- coding: utf-8 -*-
"""make deploy606.py from deploy605.py: 1.72.606 the prices hub tools (HAD-681, Ben 7.11.2026, "the strongest prices page in the world").
Three new instruments for /apartment-prices/ (page 7151): pmarket "מחירי הדירות עכשיו", pcity "מחירי דירות לפי עיר וחדרים", panatomy
"מה יש בתוך המחיר של דירה חדשה". Built and tested in docs/research/2026-11-07-prices-buying/ (node tools/instruments/test_prices_hub.js:
the math, the data honesty and the PHP summaries against the JS; tools/instruments/shot_prices.py: phone 390 and desktop 1366, presses).
  NEW assets/instruments/tools/prices-common.js, pmarket.js, pcity.js, panatomy.js
  NEW assets/instruments/data/prices-hub.json (build_prices_hub.py), anatomy.json (build_anatomy_data.py)
Hunks on the LIVE text (ashira_606.py): inc/instruments.php only, three insertions (the 3 registry entries, nadlan_phub_summary, the
routing line in nadlan_nli_summary), each anchor found exactly once, applied only when the live file is the proven one (1.72.600 wrote
it; records 601 to 605 do not touch it; it equals git HEAD). The hunks applied to HEAD give exactly the tested local file (checked here).
nadlan-config.php: the version only (the module list stays as 1.72.603 wrote it). No page, post, option or meta: the content of page 7151
is written separately, after this release is verified. The advisor (HAD-680) is OFF since 7.11.2026 20:56 (options-only, Ben's word):
the checks prove it stays off (no ?advisor=on section, no key, pages []), with no provider call."""
import hashlib, io, json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
NL = chr(10)
FILES = ["assets/instruments/tools/prices-common.js", "assets/instruments/tools/pmarket.js", "assets/instruments/tools/pcity.js",
         "assets/instruments/tools/panatomy.js", "assets/instruments/data/prices-hub.json", "assets/instruments/data/anatomy.json"]
RELS = ["inc/instruments.php"]
PHP_RELS = ["inc/instruments.php"]  # the one hunked PHP file, restored from .bak606 on rollback (nadlan-config.php always is)
md5 = lambda b: hashlib.md5(b).hexdigest()
for _r in FILES:
    assert os.path.exists(os.path.join(PLUG, *_r.split("/"))), "missing " + _r
PIN = {r: md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()) for r in FILES}

# ---------------------------------------------------------------- the files are the tested ones
for _r in FILES:
    _t = io.open(os.path.join(PLUG, *_r.split("/")), encoding="utf-8").read()
    assert not re.search("[–—]", _t), "long dash in " + _r
    if _r.endswith(".json"):
        json.loads(_t)
for _cmd, _what in ([["node", os.path.join(REPO, "tools", "instruments", "test_prices_hub.js")], "node test_prices_hub.js"],
                    [["php", "-l", os.path.join(PLUG, "inc", "instruments.php")], "php -l instruments.php (repo)"]):
    _o = subprocess.run(_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    _last = (_o.stdout.strip().splitlines() or ["(no output)"])[-1]
    assert _o.returncode == 0 and "FAILED" not in _last, _what + ": " + _last + " " + _o.stderr[-300:]
    print("[tests]", _what + ":", _last)
_r605 = json.load(open(os.path.join(QA, "deploy-result-605.json"), encoding="utf-8"))
assert str(_r605.get("state", "")).startswith("released"), "1.72.605 is not released and verified"

# ---------------------------------------------------------------- the instruments.php hunks: proven live text -> the tested file
LOCAL = io.open(os.path.join(PLUG, "inc", "instruments.php"), encoding="utf-8", newline="").read()
HEADTXT = subprocess.run(["git", "show", "HEAD:plugins/nadlan-config/inc/instruments.php"], capture_output=True, cwd=REPO).stdout
LIVE600 = None
for _n in range(605, 329, -1):  # the last release that wrote the file
    _p = os.path.join(QA, f"deploy-result-{_n}.json")
    if os.path.exists(_p):
        _f = (json.load(open(_p, encoding="utf-8")).get("files") or {}).get("inc/instruments.php")
        if _f:
            LIVE600 = (_n, _f)
            break
assert LIVE600 and LIVE600[0] == 600, LIVE600
assert md5(HEADTXT) == LIVE600[1], "git HEAD instruments.php is not what 1.72.600 wrote"
HEADTXT = HEADTXT.decode("utf-8")
assert "\r\n" not in HEADTXT and "\r\n" not in LOCAL


def block(start, end):
    a = LOCAL.find(start); b = LOCAL.find(end, a)
    assert a > -1 and b > a and LOCAL.count(start) == 1, start[:60]
    return LOCAL[a:b]


A_REG = block("\t\t\t/* HAD-681 (Ben 7.11.2026): the three tools of /apartment-prices/", "\t\t) );\n\t}\n\n\tfunction nadlan_nli_url(")
A_SUM = block("\t/** HAD-681 (7.11.2026): the plain summaries of pmarket, pcity and panatomy", "\t/** Effective annual % -> nominal for a monthly payment")
ROUTE_OLD = "\t\tif ( 'nlbudget' === $id ) { return function_exists( 'nadlan_nlb_summary' ) ? nadlan_nlb_summary( 'he' ) : ''; }  // 7.11.2026 (HAD-678)\n"
ROUTE_ADD = "\t\tif ( in_array( $id, array( 'pmarket', 'pcity', 'panatomy' ), true ) ) { return function_exists( 'nadlan_phub_summary' ) ? nadlan_phub_summary( $id ) : ''; }  // 7.11.2026 (HAD-681)\n"
REG_OLD = "\t\t\t),\n\t\t) );\n\t}\n\n\tfunction nadlan_nli_url("
SUM_OLD = "\t/** Effective annual % -> nominal for a monthly payment (the Bank of Israel conversion), and the Spitzer payment. */\n"
HUNKS = {"inc/instruments.php": [(REG_OLD, "\t\t\t),\n" + A_REG + "\t\t) );\n\t}\n\n\tfunction nadlan_nli_url(", 1),
                                 (ROUTE_OLD, ROUTE_OLD + ROUTE_ADD, 1),
                                 (SUM_OLD, A_SUM + SUM_OLD, 1)]}
ABSENT = {"inc/instruments.php": ["'pmarket' => array(", "function nadlan_phub_summary(", "prices-hub.json"]}
_t = HEADTXT
for _old, _new, _k in HUNKS["inc/instruments.php"]:
    assert _t.count(_old) == _k, "anchor x%d in HEAD: %r" % (_t.count(_old), _old[:70])
    _t = _t.replace(_old, _new)
assert _t == LOCAL, "the three hunks on HEAD do not give the tested local instruments.php"
LIVE_MD5 = {"inc/instruments.php": LIVE600[1]}
PROOF = {"inc/instruments.php": "written by 1.72.600 (deploy-result-600.json); records 601 to 605 do not write it; equals git HEAD"}
print("[hunks] instruments.php: 3 insertions (%d + %d + %d chars) on the 1.72.600 text %s give the tested file %s" % (
    len(A_REG), len(ROUTE_ADD), len(A_SUM), LIVE600[1][:10], md5(LOCAL.encode("utf-8"))[:10]))

sys.path.insert(0, H)
import ashira_605 as P605  # noqa: E402  the module list 1.72.603 wrote (kept by 604, 605)
AP = ["# -*- coding: utf-8 -*-",
      '"""Release 1.72.606 (HAD-681, the prices hub tools): three insertions on the LIVE inc/instruments.php (the registry entries pmarket,',
      "pcity, panatomy; the routing line; nadlan_phub_summary). A file is hunked only when its live md5 is LIVE_MD5[rel] (PROOF[rel] says why);",
      "every anchor must be found exactly once and the new text must be absent, or the release stops before any write. The module list in",
      "nadlan-config.php stays as 1.72.603 wrote it. Generated by make_deploy606.py.\"\"\"",
      "RELS = " + repr(RELS), "HUNKS = " + repr(HUNKS), "ABSENT = " + repr(ABSENT), "LIVE_MD5 = " + repr(LIVE_MD5), "PROOF = " + repr(PROOF),
      "MAIN_LIST = " + repr(P605.MAIN_LIST), "MAIN_NEW = " + repr(P605.MAIN_NEW), "", "",
      "def apply(rel, txt):", "    if rel not in HUNKS:", "        raise SystemExit('ashira_606: no hunk on ' + rel)",
      "    for s in ABSENT.get(rel, []):", "        if s in txt:",
      "            raise SystemExit('ashira_606: FATAL: the live %s already holds %r; read it before releasing' % (rel, s))",
      "    for old, new, n in HUNKS[rel]:",
      "        k = txt.count(old)", "        if k != n:", "            raise SystemExit('ashira_606: FATAL: anchor x%d (want %d) in the live %s: %r' % (k, n, rel, old[:90]))",
      "        txt = txt.replace(old, new)", "        print('[hunk] %s: anchor found once, %d chars inserted' % (rel, len(new) - len(old)))", "    return txt", "", "",
      "def apply_main(txt):", '    """the module list stays as 1.72.603 wrote it"""', "    if txt.count(MAIN_LIST) != 1:",
      "        raise SystemExit('ashira_606: FATAL: the live module list is not the one 1.72.603 wrote')", "    return txt", ""]
open(os.path.join(H, "ashira_606.py"), "w", encoding="utf-8", newline="\n").write("\n".join(AP))

# ---------------------------------------------------------------- deploy606.py from deploy605.py
src = open(os.path.join(H, "deploy605.py"), encoding="utf-8").read()


def one(old, new, what):
    global src
    n = src.count(old)
    assert n == 1, "%s: anchor x%d" % (what, n)
    src = src.replace(old, new)


for a, b in [("1.72.605", "1.72.606"), ("ps605", "ps606"), ("bak605", "bak606"), ("make_deploy605", "make_deploy606"),
             ("deploy-result-605", "deploy-result-606"), ("speed-605", "speed-606"), ("posts-before-605", "posts-before-606"),
             ("deploy-result-604", "deploy-result-605"), ("1.72.604", "1.72.605")]:
    src = src.replace(a, b)
BS = chr(92)
src = re.sub(r"\?t605([a-z]?)=1", "?t606" + BS + "1=1", src)
src = re.sub(r"&t605([a-z]?)=1", "&t606" + BS + "1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(605, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import ashira_605 as PX  # noqa: E402 \(.*$", "import ashira_606 as PX  # noqa: E402 (1.72.606: the prices hub, three insertions on the live inc/instruments.php)", src, flags=re.M); assert n == 1, n
src, n = re.subn(r'print\("RELEASE 1\.72\.606 LIVE: [^"]*"\)',
                 'print("RELEASE 1.72.606 LIVE: the prices hub tools (HAD-681): pmarket, pcity, panatomy + prices-common.js, prices-hub.json, anatomy.json; instruments.php registry and summaries. NEXT: the content of page 7151 (docs/research/2026-11-07-prices-buying/page-7151-new.html), then press /apartment-prices/ on a phone")', src); assert n == 1, n
lines = src.split("\n")
seen = set()
for k, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
    elif l.startswith("NEWFILES = "):
        lines[k] = "NEWFILES = set(" + repr(sorted(FILES)) + ")  # 1.72.606: the four tool files and two data files, all new"; seen.add("NEWFILES")
    elif l.startswith("FILES = ["):
        lines[k] = "FILES = " + repr(FILES); seen.add("FILES")
    elif l.startswith("PHP_RELS = ["):
        lines[k] = "PHP_RELS = " + repr(PHP_RELS) + "  # 1.72.606: the hunked PHP file, restored from .bak606 on rollback (nadlan-config.php always is)"; seen.add("PHP_RELS")
assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
# the advisor is OFF (options-only, 7.11.2026 20:56): its "on" rows become "stays off" rows (the files are still served)
na = 0
for k, l in enumerate(lines):
    if l.startswith("    ('/") and "advisor=on" in l and "'id=\"nladv\"'" in l.split("], [")[0]:
        path = re.match(r"    \('([^']+)'", l).group(1)
        lines[k] = "    (%r, ['<body'], ['Fatal error'], ['id=\"nladv\"', 'window.NL_ADV_CFG=']),  # 1.72.606: the advisor stays OFF (Ben, 7.11.2026)" % path; na += 1
assert na == 4, na
src = "\n".join(lines)
a = src.find("def verify_adv():"); b = src.find("\n\n\ndef run_checks(tag):", a)
assert a > -1 and b > a
src = src[:a] + '''def verify_adv():
    """1.72.606: the advisor (HAD-680) stays OFF as Ben set it on 7.11.2026 (options-only): /healthcheck shows expert_advisor 0.1.2 with
    no pages and no key; the three pages with ?advisor=on carry no section. No provider call, no key read."""
    try:
        s, h2 = req("GET", "/wp-json/nadlan/v1/healthcheck?nlv=adv" + str(int(time.time())), auth=False)
    except Exception as e:
        s, h2 = str(e)[:60], {}
    ea = h2.get("expert_advisor") if isinstance(h2, dict) else None
    ok = s == 200 and isinstance(ea, dict) and ea.get("version") == "0.1.2" and ea.get("pages") == [] and ea.get("key_present") is False
    print(f"[adv] {'OK ' if ok else 'BAD'} /healthcheck {s} expert_advisor off: {json.dumps(ea, ensure_ascii=False)[:200]}")
    for _p in ("/buying-apartment/", "/projects/hamedina/", "/en/buy-property-in-israel/"):
        try:
            _s, _h = page(_p + "?advisor=on&nlv=advo" + str(int(time.time())))
        except Exception as e:
            _s, _h = str(e)[:60], ""
        _g = _s == 200 and 'id="nladv"' not in _h
        print(f"[adv] {'OK ' if _g else 'BAD'} {_p}?advisor=on: no section ({_s})")
        ok = ok and _g
    return ok


def verify_phub():
    """1.72.606 (HAD-681): the prices hub on the live PHP and files. The bridge's phub_probe (the runner's own admin user) finds the three
    tools registered with their deps and data files, and their server summaries rendered from the live data with real tables; the six new
    files are served byte for byte (served_exact); /apartment-prices/ still answers 200 with its current content (the new content is a
    separate, later step)."""
    try:
        s, r = req("POST", "/wp-json/" + NS + "/v1/apply", body={"token": TOKEN, "phub_probe": 1}, timeout=120)
    except Exception as e:
        s, r = str(e)[:60], {}
    p = r.get("phub_probe") if isinstance(r, dict) else None
    want = {"pmarket": (1, 1500, "מדד מחירי הדירות של הלמ״ס"), "pcity": (1, 5000, "-apartment-prices/"), "panatomy": (1, 1500, "כשליש")}
    good = s == 200 and isinstance(p, dict) and all(isinstance(p.get(k), dict) and p[k].get("reg") is True and p[k].get("deps") == ["prices-common"]
                                                    and p[k].get("tables", 0) >= w[0] and p[k].get("len", 0) > w[1] and p[k].get("mark") is True and p[k].get("data_ok") is True
                                                    for k, w in want.items())
    print(f"[phub] {'OK ' if good else 'BAD'} {s} the three tools on the live PHP: {json.dumps(p, ensure_ascii=False)[:500]}")
    return good''' + src[b:]
one('    if not bad and not verify_adv():\n        bad = ["expert-advisor"]\n    return bad',
    '    if not bad and not verify_adv():\n        bad = ["expert-advisor-off"]\n    if not bad and not verify_phub():\n        bad = ["prices-hub"]\n    return bad', "verify_phub hook")
# the bridge: the prices hub on the live PHP (registry, data files, summaries), read only
one("\t\t\tif ( ! empty( $b['purge'] ) ) {",
    "\t\t\tif ( ! empty( $b['phub_probe'] ) ) { // 1.72.606 (HAD-681): the three prices tools on the live PHP; nothing is written\n"
    "\t\t\t\ttry {\n"
    "\t\t\t\t\t$t = function_exists( 'nadlan_nli_tools' ) ? nadlan_nli_tools() : array(); $o = array(); $dd = WP_PLUGIN_DIR . '/nadlan-config/assets/instruments/';\n"
    "\t\t\t\t\t$mk = array( 'pmarket' => 'מדד מחירי הדירות של הלמ״ס', 'pcity' => '-apartment-prices/', 'panatomy' => 'כשליש' );\n"
    "\t\t\t\t\tforeach ( $mk as $id => $m ) {\n"
    "\t\t\t\t\t\t$sm = isset( $t[ $id ] ) && function_exists( 'nadlan_nli_summary' ) ? (string) nadlan_nli_summary( $id, 'he' ) : ''; $dok = isset( $t[ $id ] );\n"
    "\t\t\t\t\t\tif ( $dok ) { foreach ( $t[ $id ]['data'] as $f ) { $dok = $dok && is_readable( $dd . 'data/' . $f ); } foreach ( (array) $t[ $id ]['deps'] as $f ) { $dok = $dok && is_readable( $dd . 'tools/' . $f . '.js' ); } $dok = $dok && is_readable( $dd . 'tools/' . $id . '.js' ); }\n"
    "\t\t\t\t\t\t$o[ $id ] = array( 'reg' => isset( $t[ $id ] ), 'deps' => isset( $t[ $id ]['deps'] ) ? array_values( (array) $t[ $id ]['deps'] ) : null, 'len' => strlen( $sm ), 'tables' => substr_count( $sm, '<table' ), 'mark' => false !== strpos( $sm, $m ), 'data_ok' => $dok );\n"
    "\t\t\t\t\t}\n"
    "\t\t\t\t\t$out['phub_probe'] = $o;\n"
    "\t\t\t\t} catch ( \\Throwable $e ) { $out['phub_probe'] = array( 'err' => substr( $e->getMessage(), 0, 200 ) ); }\n"
    "\t\t\t}\n"
    "\t\t\tif ( ! empty( $b['purge'] ) ) {", "bridge phub_probe")
# the pages: /apartment-prices/ still answers with its content, and the tools' files as served (byte for byte in served_exact)
T = "/wp-content/plugins/nadlan-config/assets/instruments/"
ADD = [("/apartment-prices/?t606p=1", ['class="nlprice"', "<h1>"], ["Fatal error"]),
       (T + "tools/pmarket.js?t606p=1", ["NI.register('pmarket'", "מחירי הדירות עכשיו"], ["Fatal error"]),
       (T + "tools/pcity.js?t606p=1", ["NI.register('pcity'", "מחירי דירות לפי עיר וחדרים"], ["Fatal error"]),
       (T + "tools/panatomy.js?t606p=1", ["NI.register('panatomy'", "מה יש בתוך המחיר של דירה חדשה"], ["Fatal error"]),
       (T + "tools/prices-common.js?t606p=1", ["window.NLPH = {", "function hpiAt("], ["Fatal error"]),
       (T + "data/prices-hub.json?t606p=1", ['"key":"phub"', '"hpi":{'], ["Fatal error"]),
       (T + "data/anatomy.json?t606p=1", ['"key":"anatomy"', '"boi13"'], ["Fatal error"])]
_ca = [l for l in src.split("\n") if l.startswith("    ('/wp-content/plugins/nadlan-config/assets/expert-advisor/advisor.js?t606x=1',")]
assert len(_ca) == 1, len(_ca)
src = src.replace(_ca[0], "".join("    (%s),\n" % ", ".join(repr(x) for x in t) for t in ADD) + _ca[0], 1)
src, n = re.subn(r'checks="verify_pages \+ served_exact [^"]*"',
                 'checks="verify_pages + served_exact (the 6 prices hub files at ?ver=1.72.606, byte for byte) + verify_order + verify_home_order + verify_kh + verify_nlb + verify_mkt + verify_ac + verify_vt + verify_adv (OFF stays off) + verify_phub: OK"', src); assert n == 1, n
assert "ashira_605 as PX" not in src and "t605" not in src and "deploy-result-604" not in src
assert src.count('WANT_LIVE = "1.72.605"') == 1 and src.count('BAK = ".bak606"') == 1 and src.count("range(605, 329, -1)") == 1
assert src.count("$b['phub_probe']") == 1 and src.count('"phub_probe": 1') == 1 and src.count("def verify_phub():") == 1 and "a real question" not in src
open(os.path.join(H, "deploy606.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy606.py + ashira_606.py written | pins:", {k.split("/")[-1]: v for k, v in PIN.items()}, "| PHP_RELS:", PHP_RELS,
      "| instruments.php live", LIVE_MD5["inc/instruments.php"][:10], "->", md5(LOCAL.encode("utf-8"))[:10])
