# -*- coding: utf-8 -*-
"""make deploy603.py from deploy602.py: 1.72.603 the NadLan real-estate advisor, a PROTOTYPE for Ben's review (HAD-680, Ben 7.11.2026):
"an advisor with the whole résumé of 40 years in Israeli real estate ... designed with Claude Design ... tested on certain pages", and
"do not write that it is a broker". Seen ONLY with ?advisor=on on three listed pages; without the parameter every page is unchanged.
Built and tested in docs/research/2026-11-07-expert-agent/build/ (php test_adv_unit.php offline, run_adv.php against the provider with the
saved live page text, design cards replaying real answers: Claude Design v107 ExpertAdvisor, artifact L9Nqz7Viv7K3MYeZrBc9s8 version 276).
  NEW assets/expert-advisor/advisor.css  the section's look (NadLan Instruments tokens, scoped to #nladv, no fixed or sticky element)
  NEW assets/expert-advisor/advisor.js   places the section in the reading order, the conversation, readout cells, the team form that posts
                                         to the existing /wp-json/nadlan/v1/lead (source expert_advisor, with the visit-trail id when there is one)
  NEW inc/expert-advisor.php             the gate (?advisor=on + option nadlan_advisor_pages, no cookie, no page cache), POST
                                         /wp-json/nadlan/v1/advisor (OpenRouter, four tools on the site's own data files, a page token, per-visitor
                                         and daily spending caps, counters only, no conversation stored), the healthcheck line expert_advisor 0.1.0
Hunk on the LIVE text (ashira_603.py): nadlan-config.php only: 'expert-advisor' after 'visit-trail' at the end of the module list (the list
1.72.602 wrote, proven again by the runner on the live text). No other PHP file is hunked (RELS = []).
Options written by the bridge after the files (undone by rollback): nadlan_advisor_or_key (the OpenRouter key, read here from the local
secrets file and sent only in the bridge body: never printed, never in the record) and nadlan_advisor_pages [9, 8113, 5154].
No page, post or meta is written. The repo nadlan-config.php is NOT touched (its module list is not the live one)."""
import hashlib, io, json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
D = os.path.join(REPO, "docs", "research", "2026-11-07-expert-agent", "build")
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
FILES = ["assets/expert-advisor/advisor.css", "assets/expert-advisor/advisor.js", "inc/expert-advisor.php"]
RELS = []                         # no inc/ file is hunked: the module hooks in
PHP_RELS = ["nadlan-config.php"]  # the one hunked PHP file (the module list): restored from .bak603 on rollback
for _r in FILES:
    assert os.path.exists(os.path.join(PLUG, *_r.split("/"))), "missing " + _r
PIN = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}

# ---------------------------------------------------------------- the three files are the tested ones
_js = io.open(os.path.join(PLUG, "assets", "expert-advisor", "advisor.js"), encoding="utf-8").read()
_css = io.open(os.path.join(PLUG, "assets", "expert-advisor", "advisor.css"), encoding="utf-8").read()
_php = io.open(os.path.join(PLUG, "inc", "expert-advisor.php"), encoding="utf-8").read()
assert "NadLan real-estate advisor 0.1.0" in _js and "var VERSION = '0.1.0';" in _js and "w.NL_ADV_CFG" in _js and "source: 'expert_advisor'" in _js, "advisor.js is not 0.1.0"
assert "define( 'NADLAN_ADV_VERSION', '0.1.0' );" in _php and "register_rest_route( 'nadlan/v1', '/advisor'" in _php and "nadlan_adv_requested()" in _php, "expert-advisor.php is not 0.1.0"
assert "'nadlan_advisor_pages', array( 9, 8113, 5154 )" in _php and "X-LiteSpeed-Cache-Control: no-cache" in _php and "DONOTCACHEPAGE" in _php, "gate / no-cache"
assert "html body #nladv" in _css and not re.search(r"position\s*:\s*(fixed|sticky)", _css), "advisor.css: scoped, nothing floating"
for _n, _t in (("advisor.js", _js), ("advisor.css", _css), ("expert-advisor.php", _php)):
    assert not re.search("[\u2013\u2014]", _t), "long dash in " + _n
for _cmd, _what in ((["php", "-l", os.path.join(PLUG, "inc", "expert-advisor.php")], "php -l"),
                    (["node", "--check", os.path.join(PLUG, "assets", "expert-advisor", "advisor.js")], "node --check"),
                    (["php", os.path.join(D, "test_adv_unit.php")], "php test_adv_unit.php")):
    _o = subprocess.run(_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=D)
    _last = (_o.stdout.strip().splitlines() or ["(no output)"])[-1]
    assert _o.returncode == 0 and "FAILED" not in _last, _what + ": " + _last + " " + _o.stderr[-300:]
    print("[tests]", _what + ":", _last)
_key_file = r"C:\Users\777\Documents\jus-tice-secrets\openrouter\hadmaia-openrouter-key.txt"
assert os.path.exists(_key_file), "the OpenRouter key file is missing (TOOLS-AND-KEYS.md)"

# ---------------------------------------------------------------- the module list hunk (on the live text the runner reads)
sys.path.insert(0, H)
import ashira_602 as P602  # noqa: E402  the live module list 1.72.602 wrote
ML = P602.MAIN_NEW
assert ML.endswith("'campaign-brief', 'visit-trail' ) as $nadlan_mod") and ML.count("'visit-trail'") == 1 and "'expert-advisor'" not in ML, ML[-80:]
ML_NEW = ML.replace("'visit-trail' ) as $nadlan_mod", "'visit-trail', 'expert-advisor' ) as $nadlan_mod")
assert ML_NEW != ML and ML_NEW.count("'expert-advisor'") == 1
HUNKS = {"nadlan-config.php": [(ML, ML_NEW, 1)]}
ABSENT = {"nadlan-config.php": ["'expert-advisor'"]}
_p602 = os.path.join(QA, "deploy-result-602.json")
assert os.path.exists(_p602) and str(json.load(open(_p602, encoding="utf-8")).get("state", "")).startswith("released"), "1.72.602 is not released and verified"

# ---------------------------------------------------------------- ashira_603.py
AP = ["# -*- coding: utf-8 -*-",
      '"""Release 1.72.603 (HAD-680, the NadLan advisor prototype): one hunk on the LIVE nadlan-config.php module list (apply_main, on the bumped',
      "text): 'expert-advisor' after 'visit-trail'. No other file is hunked (RELS is empty). The anchor must be found exactly once and",
      "'expert-advisor' must be absent, or the release stops before any write. Generated by make_deploy603.py.\"\"\"",
      "RELS = " + repr(RELS), "HUNKS = " + repr(HUNKS), "ABSENT = " + repr(ABSENT), "LIVE_MD5 = {}", "PROOF = {}",
      "MAIN_LIST = " + repr(ML), "MAIN_NEW = " + repr(ML_NEW), "", "",
      "def apply(rel, txt):", "    if rel not in HUNKS:", "        raise SystemExit('ashira_603: no hunk on ' + rel)",
      "    for s in ABSENT.get(rel, []):", "        if s in txt:",
      "            raise SystemExit('ashira_603: FATAL: the live %s already holds %r; read it before releasing' % (rel, s))",
      "    for old, new, n in HUNKS[rel]:", "        if new in txt:", "            raise SystemExit('ashira_603: FATAL: the live %s already holds the new text' % rel)",
      "        k = txt.count(old)", "        if k != n:", "            raise SystemExit('ashira_603: FATAL: anchor x%d (want %d) in the live %s: %r' % (k, n, rel, old[:90]))",
      "        txt = txt.replace(old, new)", "    return txt", "", "",
      "def apply_main(txt):", '    """the module list of the bumped live nadlan-config.php: \'expert-advisor\' after \'visit-trail\', once"""',
      "    txt = apply('nadlan-config.php', txt)", "    if txt.count(MAIN_NEW) != 1:",
      "        raise SystemExit('ashira_603: FATAL: the module list does not end with expert-advisor exactly once')", "    return txt", ""]
open(os.path.join(H, "ashira_603.py"), "w", encoding="utf-8", newline="\n").write("\n".join(AP))

# ---------------------------------------------------------------- deploy603.py from deploy602.py
src = open(os.path.join(H, "deploy602.py"), encoding="utf-8").read()


def one(old, new, what):
    global src
    n = src.count(old)
    assert n == 1, "%s: anchor x%d" % (what, n)
    src = src.replace(old, new)


for a, b in [("1.72.602", "1.72.603"), ("ps602", "ps603"), ("bak602", "bak603"), ("make_deploy602", "make_deploy603"),
             ("deploy-result-602", "deploy-result-603"), ("speed-602", "speed-603"), ("posts-before-602", "posts-before-603"),
             ("deploy-result-601", "deploy-result-602"), ("1.72.601", "1.72.602")]:
    src = src.replace(a, b)
BS = chr(92)
src = re.sub(r"\?t602([a-z]?)=1", "?t603" + BS + "1=1", src)
src = re.sub(r"&t602([a-z]?)=1", "&t603" + BS + "1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(602, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import ashira_602 as PX  # noqa: E402 \(.*$", "import ashira_603 as PX  # noqa: E402 (1.72.603: the advisor prototype; the module list only, no inc/ hunk)", src, flags=re.M); assert n == 1, n
src, n = re.subn(r'print\("RELEASE 1\.72\.603 LIVE: [^"]*"\)',
                 'print("RELEASE 1.72.603 LIVE: the NadLan advisor PROTOTYPE (HAD-680): assets/expert-advisor/advisor.css + advisor.js + inc/expert-advisor.php, \'expert-advisor\' in the module list; seen only with ?advisor=on on /buying-apartment/, /projects/hamedina/, /en/buy-property-in-israel/. NEXT: press it in a real browser, phone and desktop")', src); assert n == 1, n
lines = src.split("\n")
seen = set()
for k, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
    elif l.startswith("NEWFILES = "):
        lines[k] = "NEWFILES = set(" + repr(sorted(FILES)) + ")  # 1.72.603: the advisor's three files, all new"; seen.add("NEWFILES")
    elif l.startswith("FILES = ["):
        lines[k] = "FILES = " + repr(FILES); seen.add("FILES")
    elif l.startswith("PHP_RELS = ["):
        lines[k] = "PHP_RELS = " + repr(PHP_RELS) + "  # 1.72.603: the one hunked PHP file (the module list), restored from .bak603 on rollback"; seen.add("PHP_RELS")
assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
src = "\n".join(lines)

# the advisor key: read from the local secrets file at run time, sent only in the bridge body, never printed or recorded
one("UNDO = []  # 1.72.603: the snippet / page / meta writes, undone by rollback() in reverse order\n",
    "UNDO = []  # 1.72.603: the snippet / page / meta / advisor-option writes, undone by rollback() in reverse order\n"
    "ADV_KEY_FILE = r\"" + _key_file + "\"  # 1.72.603 (HAD-680): read at run time, sent only in the bridge body, never printed or recorded\n", "UNDO line")

# the module list: proven to be the 1.72.602 list on the live text, then 'expert-advisor' joins it
one("    text = PX.apply_main(text)  # 1.72.603 (HAD-678): 'visit-trail' joins the module list after 'campaign-brief' (ashira_602, anchor x1)\n"
    "    print(\"[plan] nadlan-config.php: the module list now ends 'campaign-brief', 'visit-trail'\")\n",
    "    text = PX.apply_main(text)  # 1.72.603 (HAD-680): 'expert-advisor' joins the module list after 'visit-trail' (ashira_603, anchor x1)\n"
    "    print(\"[plan] nadlan-config.php: the module list now ends 'visit-trail', 'expert-advisor'\")\n", "module hunk")

# the bridge: the advisor's options (the key is stored, never echoed) and a probe of the module on the live PHP
one("\t\t\tif ( ! empty( $b['purge'] ) ) {",
    "\t\t\tif ( isset( $b['adv_cfg'] ) && is_array( $b['adv_cfg'] ) ) { // 1.72.603 (HAD-680): the advisor's options; the key is never echoed\n"
    "\t\t\t\t$ac = $b['adv_cfg'];\n"
    "\t\t\t\tif ( ! empty( $ac['clear'] ) ) { delete_option( 'nadlan_advisor_or_key' ); delete_option( 'nadlan_advisor_pages' ); }\n"
    "\t\t\t\tif ( isset( $ac['key'] ) && preg_match( '/^sk-or-[A-Za-z0-9_-]{20,200}$/', (string) $ac['key'] ) ) { update_option( 'nadlan_advisor_or_key', (string) $ac['key'], false ); }\n"
    "\t\t\t\tif ( isset( $ac['pages'] ) && is_array( $ac['pages'] ) ) { update_option( 'nadlan_advisor_pages', array_values( array_filter( array_map( 'absint', $ac['pages'] ) ) ), false ); }\n"
    "\t\t\t\t$out['adv_cfg'] = array( 'key_present' => '' !== trim( (string) get_option( 'nadlan_advisor_or_key', '' ) ), 'pages' => get_option( 'nadlan_advisor_pages', null ) );\n"
    "\t\t\t}\n"
    "\t\t\tif ( ! empty( $b['adv_probe'] ) ) { // 1.72.603: the advisor module on the live PHP (data files, tools, rules, route); no provider call\n"
    "\t\t\t\ttry {\n"
    "\t\t\t\t\t$out['adv_probe'] = function_exists( 'nadlan_adv_tax' ) ? array( 'version' => NADLAN_ADV_VERSION, 'tax' => nadlan_adv_tax( 2500000, 'single' )['tax'],\n"
    "\t\t\t\t\t\t'monthly' => nadlan_adv_mortgage( 1800000, 25 )['monthly'], 'cash' => nadlan_adv_costs( 2500000, 'single' )['cash_needed'], 'rules' => strlen( nadlan_adv_rules() ),\n"
    "\t\t\t\t\t\t'facts' => strlen( nadlan_adv_facts_block() ), 'ctx' => strlen( nadlan_adv_page_context( 8113 ) ), 'pages' => nadlan_adv_pages(), 'key' => '' !== nadlan_adv_key(),\n"
    "\t\t\t\t\t\t'route' => isset( rest_get_server()->get_routes()['/nadlan/v1/advisor'] ), 'search' => count( nadlan_adv_search( 'משכנתא' ) ) ) : array( 'fn' => 0 );\n"
    "\t\t\t\t} catch ( \\Throwable $e ) { $out['adv_probe'] = array( 'err' => substr( $e->getMessage(), 0, 200 ) ); }\n"
    "\t\t\t}\n"
    "\t\t\tif ( ! empty( $b['purge'] ) ) {", "bridge adv_cfg + adv_probe")

# rollback: the advisor options go with the files
one("            elif _kind == \"meta\":\n",
    "            elif _kind == \"adv\":  # 1.72.603: the advisor key and pages are removed with the module\n"
    "                print(\"[rollback] advisor options cleared\", ops({\"adv_cfg\": {\"clear\": 1}}, \"advisor options clear\").get(\"adv_cfg\"))\n"
    "            elif _kind == \"meta\":\n", "rollback adv")

# the options are written right after the files, before the purge and the checks
one('        record("written, checks pending", files=FILES_MD5, post_after={p["slug"]: p["content_md5"] for p in POSTS})\n',
    '        record("written, checks pending", files=FILES_MD5, post_after={p["slug"]: p["content_md5"] for p in POSTS})\n'
    '        UNDO.append(("adv", {}))  # 1.72.603: from here a rollback also clears the advisor options\n'
    '        with open(ADV_KEY_FILE, encoding="utf-8-sig") as _fh:\n'
    '            _ak = (_fh.read().strip().splitlines() or [""])[0].strip()\n'
    '        if not _ak.startswith("sk-or-"):\n'
    '            raise SystemExit("FATAL the advisor key file does not hold an OpenRouter key")\n'
    '        _ac = ops({"adv_cfg": {"key": _ak, "pages": [9, 8113, 5154]}}, "advisor options").get("adv_cfg")\n'
    '        _ak = None\n'
    '        print("[adv] options stored (the key is not printed):", json.dumps(_ac))\n'
    '        if not (isinstance(_ac, dict) and _ac.get("key_present") is True and _ac.get("pages") == [9, 8113, 5154]):\n'
    '            raise SystemExit("FATAL the advisor options were not stored")\n', "adv options after the files")

# the pages after the release: the section only with ?advisor=on on the three listed pages, never without it, never elsewhere
A = "/wp-content/plugins/nadlan-config/assets/expert-advisor/"
ADD = [(A + "advisor.js?t603x=1", ["NadLan real-estate advisor 0.1.0", "NL_ADV_CFG", "nadlan/v1/lead", "expert_advisor"], ["Fatal error"]),
       (A + "advisor.css?t603x=1", ["html body #nladv", "--a-sea:#2F6F86"], ["Fatal error"]),
       ("/buying-apartment/?advisor=on&t603a=1", ['id="nladv"', "expert-advisor/advisor.js?ver=0.1.0", "window.NL_ADV_CFG=", '"kind":"guide"', "שאלו את יועץ הנדל״ן", "לא אדם ולא מתווך", "info@nad-lan.co.il"], ["Fatal error"]),
       ("/projects/hamedina/?advisor=on&t603a=1", ['id="nladv"', '"kind":"project"', "מה חשוב לבדוק לפני שקונים כאן?", 'id="nlps"'], ["Fatal error"]),
       ("/en/buy-property-in-israel/?advisor=on&t603a=1", ['id="nladv"', "nladv--en", "Ask the NadLan advisor", '"lang":"en"'], ["Fatal error"]),
       ("/buying-apartment/?t603n=1", ["<body"], ["Fatal error"], ['id="nladv"', "expert-advisor/advisor", "NL_ADV_CFG"]),
       ("/projects/hamedina/?t603n=1", ['id="nlps"'], ["Fatal error"], ['id="nladv"', "expert-advisor/advisor", "NL_ADV_CFG"]),
       ("/en/buy-property-in-israel/?t603n=1", ["<body"], ["Fatal error"], ['id="nladv"', "expert-advisor/advisor"]),
       ("/mortgage-calculator/?advisor=on&t603n=1", ['data-nli="mquick"'], ["Fatal error"], ['id="nladv"', "expert-advisor/advisor"]),
       ("/?advisor=on&t603n=1", ["<body"], ["Fatal error"], ['id="nladv"', "expert-advisor/advisor"])]
_ca = [l for l in src.split("\n") if l.startswith("    ('/wp-content/plugins/nadlan-config/assets/visit-trail/trail.js?t603x=1',")]
assert len(_ca) == 1, len(_ca)
src = src.replace(_ca[0], "".join("    (%s),\n" % ", ".join(repr(x) for x in t) for t in ADD) + _ca[0], 1)

VERIFY_ADV = '''def verify_adv():
    """1.72.603 (HAD-680): the advisor is loaded and answers on the live PHP. /healthcheck carries expert_advisor 0.1.0, on, the key
    present and the three pages; POST /wp-json/nadlan/v1/advisor refuses a wrong page token (400 nladv_page) before any provider call; the
    bridge's adv_probe computes 20,538 purchase tax on 2,500,000 (single home), 10,128 a month on 1,800,000 over 25 years, reads the rules,
    the official numbers and the project page text, and sees the route; then ONE real question with the page's own token gets an answer
    (one provider call, about 0.02 USD). The advisor page is served with the no-cache headers."""
    ok = True
    try:
        s, h2 = req("GET", "/wp-json/nadlan/v1/healthcheck?nlv=adv" + str(int(time.time())), auth=False)
    except Exception as e:
        s, h2 = str(e)[:60], {}
    ea = h2.get("expert_advisor") if isinstance(h2, dict) else None
    good = (s == 200 and isinstance(h2, dict) and h2.get("version") == "1.72.603" and isinstance(ea, dict) and ea.get("version") == "0.1.0"
            and ea.get("on") is True and ea.get("key_present") is True and ea.get("pages") == [9, 8113, 5154])
    print(f"[adv] {'OK ' if good else 'BAD'} /healthcheck {s} expert_advisor {json.dumps(ea, ensure_ascii=False)}")
    ok = ok and good
    try:
        s2, b2 = req("POST", "/wp-json/nadlan/v1/advisor", body={"page": 9, "tok": "x" * 24, "messages": [{"role": "user", "content": "שלום"}]}, auth=False, timeout=60)
    except Exception as e:
        s2, b2 = str(e)[:60], {}
    good = s2 == 400 and isinstance(b2, dict) and b2.get("code") == "nladv_page"
    print(f"[adv] {'OK ' if good else 'BAD'} wrong token: {s2} {json.dumps(b2, ensure_ascii=False)[:120]} (want 400 nladv_page)")
    ok = ok and good
    try:
        s3, r3 = req("POST", "/wp-json/" + NS + "/v1/apply", body={"token": TOKEN, "adv_probe": 1}, timeout=120)
    except Exception as e:
        s3, r3 = str(e)[:60], {}
    p = r3.get("adv_probe") if isinstance(r3, dict) else None
    good = (s3 == 200 and isinstance(p, dict) and p.get("version") == "0.1.0" and p.get("tax") == 20538 and p.get("monthly") == 10128
            and p.get("cash") == [662138, 678488] and p.get("rules", 0) > 8000 and p.get("facts", 0) > 800 and p.get("ctx", 0) > 1000
            and p.get("route") is True and p.get("key") is True and p.get("pages") == [9, 8113, 5154])
    print(f"[adv] {'OK ' if good else 'BAD'} {s3} the module on the live PHP: {json.dumps(p, ensure_ascii=False)[:400]}")
    ok = ok and good
    try:
        s4, html = page("/buying-apartment/?advisor=on&nlv=advq" + str(int(time.time())))
        m = re.search(r'"tok":"([0-9a-f]{24})"', html)
        rq = urllib.request.Request(BASE + "/buying-apartment/?advisor=on&nlv=advh" + str(int(time.time())), headers={"User-Agent": UA})
        with urllib.request.urlopen(rq, timeout=90) as resp:
            hdr = {k.lower(): v for k, v in resp.getheaders()}
        s5, r5 = req("POST", "/wp-json/nadlan/v1/advisor", body={"page": 9, "tok": m.group(1) if m else "", "lang": "he",
                     "messages": [{"role": "user", "content": "כמה מס רכישה על דירה יחידה במחיר 2,000,000 ₪?"}]}, auth=False, timeout=120)
    except Exception as e:
        s4, s5, r5, hdr, m = "x", str(e)[:80], {}, {}, None
    ans = (r5.get("answer") or "") if isinstance(r5, dict) else ""
    good = (s4 == 200 and m is not None and s5 == 200 and isinstance(r5, dict) and r5.get("ok") is True and len(ans) > 40
            and "no-cache" in hdr.get("x-litespeed-cache-control", "") and hdr.get("x-nl-advisor") == "preview")
    cards = [c.get("kind") for c in (r5.get("cards") or [])] if isinstance(r5, dict) else []
    print(f"[adv] {'OK ' if good else 'BAD'} a real question: page {s4}, token {'found' if m else 'MISSING'}, answer {s5}, {len(ans)} chars, cards {cards}, "
          f"usage {json.dumps(r5.get('usage') if isinstance(r5, dict) else None)}, headers no-cache={hdr.get('x-litespeed-cache-control')} advisor={hdr.get('x-nl-advisor')}")
    print("[adv] the answer begins:", ans[:220].replace("\\n", " "))
    return ok and good


def run_checks(tag):'''
one("def run_checks(tag):", VERIFY_ADV, "verify_adv def")
one('    if not bad and not verify_vt():\n        bad = ["visit-trail"]\n    return bad',
    '    if not bad and not verify_vt():\n        bad = ["visit-trail"]\n    if not bad and not verify_adv():\n        bad = ["expert-advisor"]\n    return bad', "verify_adv hook")
src, n = re.subn(r'checks="verify_pages \+ served_exact [^"]*"',
                 'checks="verify_pages + served_exact (advisor.css, advisor.js byte for byte) + verify_order + verify_home_order + verify_kh + verify_nlb + verify_mkt + verify_ac + verify_vt + verify_adv: OK"', src); assert n == 1, n
assert "ashira_602 as PX" not in src and "t602" not in src and "deploy-result-601" not in src, "a 602 marker is left"
assert "602" not in "".join(l for l in src.split("\n") if l.startswith(("PIN = ", "NEWFILES = ", "FILES = ", "PHP_RELS = ", "BAK = ", "NS = ")))
assert src.count('WANT_LIVE = "1.72.602"') == 1 and src.count('BAK = ".bak603"') == 1 and src.count("range(602, 329, -1)") == 1 and src.count("PX.apply_main(text)") == 1
assert src.count("$b['adv_cfg']") == 3 and src.count('"adv_probe": 1') == 1 and src.count("def verify_adv():") == 1 and src.count('UNDO.append(("adv", {}))') == 1
assert "print(_ak" not in src and "ADV_KEY_FILE" in src
open(os.path.join(H, "deploy603.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy603.py + ashira_603.py written | t603 markers:", len(re.findall(r"t603[a-z]?=1", src)),
      "| pins:", {k.split("/")[-1]: v[:10] for k, v in PIN.items()}, "| PHP_RELS:", PHP_RELS, "| module list: ... 'visit-trail', 'expert-advisor'")
