# -*- coding: utf-8 -*-
"""make deploy599.py from deploy598.py: 1.72.599 the international campaign planner for developers (HAD-678, Ben 7.11.2026).
Built and tested in docs/research/2026-11-07-campaign-network/build/build-nlcamp/ (node 90, PHP 66, browser 529); the exact PHP of the
release step is that folder's registry.php.txt.
  NEW assets/instruments/tools/nlcamp.js  "מתכנן הקמפיין" (window.NLCAMP, register('nlcamp'))
  NEW inc/campaign-brief.php             POST /wp-json/nadlan/v1/campaign-brief, the private type nadlan_camp_brief, NLCAMP_CONFIG,
                                         the summary nadlan_cb_summary(), the line campaign_brief (1.1.0) of the
                                         nadlan_config_healthcheck filter (served at /healthcheck; /health is inc/health.php's own)
Hunks on the LIVE text (ashira_599.py, every anchor must be found exactly once or the runner stops before any write):
  inc/instruments.php  (1) the nlcamp entry before the mkeys entry (anchor A1, the one 1.72.597 used), (2a) the Hebrew summary branch
                       right after the 'en' hand-off line of nadlan_nli_summary() (A2), (2b) the English branch at the top of
                       nadlan_nli_summary_en() (A3). Fetched, hunked and written by the runner's PX loop.
  nadlan-config.php    'campaign-brief' after 'mortgage-market' at the end of the module list (ML, the tail the 1.72.598 runner proved
                       once on the live text), applied by the runner on the bumped live text (one write of the main file).
PHP_RELS = both hunked PHP files, so a rollback restores both from .bak599 before it removes the two new files.
No page, post, option or meta is written: /international-campaigns/ follows on its own (url_word_audit first).
The repo inc/instruments.php gets the same three hunks (as 1.72.597 / 598 did); the repo nadlan-config.php is NOT touched (its module
list is not the live one)."""
import hashlib, io, os, re, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
D = os.path.join(REPO, "docs", "research", "2026-11-07-campaign-network", "build", "build-nlcamp")
NL = chr(10)
FILES = ["assets/instruments/tools/nlcamp.js", "inc/campaign-brief.php"]
RELS = ["inc/instruments.php"]                         # fetched, hunked and written by the runner's PX loop
PHP_RELS = ["inc/instruments.php", "nadlan-config.php"]  # every hunked PHP file: restored from .bak599 on rollback
for _r in FILES:
    assert os.path.exists(os.path.join(PLUG, *_r.split("/"))), "missing " + _r
PIN = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}

# ---------------------------------------------------------------- the hunks, cut from registry.php.txt
reg = io.open(os.path.join(D, "registry.php.txt"), encoding="utf-8").read().replace(chr(13) + NL, NL)
_k = reg.index("\t\t\t/* 7.11.2026 (Ben): the international campaign planner")
_close = NL + "\t\t\t)," + NL
_e = reg.index(_close, reg.index("\t\t\t'nlcamp' => array(", _k)) + len(_close)
ENTRY = reg[_k:_e]
assert ENTRY.count("'nlcamp' => array(") == 1 and ENTRY.count("'en' => array(") == 1 and ENTRY.endswith(_close[1:]), "entry cut"


def line(t, needle):
    assert t.count(needle) == 1, ("needle", needle, t.count(needle))
    c = t.index(needle); a = t.rfind(NL, 0, c) + 1; b = t.index(NL, c) + 1
    return t[a:b]


SUM_HE = line(reg, "nadlan_cb_summary( 'he' )")
SUM_EN = line(reg, "nadlan_cb_summary( 'en' )")
for _s in (SUM_HE, SUM_EN):
    assert _s.startswith("\t\tif ( 'nlcamp' === $id ) { return function_exists( 'nadlan_cb_summary' )"), _s
assert not re.search("[–—]", ENTRY + SUM_HE + SUM_EN), "long dash"
A1 = "\t\t\t/* 1.72.593 (HAD-675, T4): from contract to keys, the 7th tool of /mortgage-calculator/"
A2 = "\t\tif ( 'en' === $lang ) { return nadlan_nli_summary_en( $id ); }\n"
A3 = "\tfunction nadlan_nli_summary_en( $id ) {\n"
ML = ("'home-v3', 'pro-card', 'cta-sheet', 'deal-sign', 'instruments', 'compound-tool', 'price-nudge', 'project-kit', 'city-projects', "
      "'radius-prices', 'project-facts', 'near-finder', 'near-alerts', 'mortgage-market' ) as $nadlan_mod")
ML_NEW = ML.replace("'mortgage-market' ) as $nadlan_mod", "'mortgage-market', 'campaign-brief' ) as $nadlan_mod")
assert ML_NEW != ML and ML_NEW.count("'campaign-brief'") == 1
HUNKS = {"inc/instruments.php": [(A1, ENTRY + A1, 1), (A2, A2 + SUM_HE, 1), (A3, A3 + SUM_EN, 1)],
         "nadlan-config.php": [(ML, ML_NEW, 1)]}
ABSENT = {"inc/instruments.php": ["'nlcamp' => array(", "nadlan_cb_summary("], "nadlan-config.php": ["'campaign-brief'"]}

# ---------------------------------------------------------------- the repo inc/instruments.php (bookkeeping, as 1.72.597 / 598)
_ip = os.path.join(PLUG, "inc", "instruments.php")
_raw = open(_ip, "rb").read(); _crlf = b"\r\n" in _raw
_it = _raw.decode("utf-8").replace("\r\n", NL)
if "'nlcamp' => array(" in _it:
    assert all(_it.count(new) == 1 for old, new, n in HUNKS["inc/instruments.php"]), "repo instruments.php holds only part of nlcamp; restore it first"
    print("repo inc/instruments.php: already holds the three nlcamp hunks")
else:
    for old, new, n in HUNKS["inc/instruments.php"]:
        assert _it.count(old) == n, ("repo anchor", old[:60], _it.count(old))
        _it = _it.replace(old, new)
    io.open(_ip, "w", encoding="utf-8", newline="").write(_it.replace(NL, "\r\n") if _crlf else _it)
    print("repo inc/instruments.php: the three nlcamp hunks applied")

# ---------------------------------------------------------------- ashira_599.py
AP = ["# -*- coding: utf-8 -*-",
      '"""Release 1.72.599 (HAD-678, the campaign planner): three insert hunks on the LIVE inc/instruments.php (the runner\'s PX loop) and one on the',
      "LIVE nadlan-config.php module list (apply_main, on the bumped text). Every anchor must be found exactly once and the new text must be absent,",
      'or the release stops before any write. Generated by make_deploy599.py."""',
      "RELS = " + repr(RELS), "HUNKS = " + repr(HUNKS), "ABSENT = " + repr(ABSENT), "MAIN_NEW = " + repr(ML_NEW), "", "",
      "def apply(rel, txt):", "    if rel not in HUNKS:", "        raise SystemExit('ashira_599: no hunk on ' + rel)",
      "    for s in ABSENT.get(rel, []):", "        if s in txt:",
      "            raise SystemExit('ashira_599: FATAL: the live %s already holds %r; read it before releasing' % (rel, s))",
      "    for old, new, n in HUNKS[rel]:", "        if new in txt:", "            raise SystemExit('ashira_599: FATAL: the live %s already holds the new text' % rel)",
      "        k = txt.count(old)", "        if k != n:", "            raise SystemExit('ashira_599: FATAL: anchor x%d (want %d) in the live %s: %r' % (k, n, rel, old[:90]))",
      "        txt = txt.replace(old, new)", "    return txt", "", "",
      "def apply_main(txt):", '    """the module list of the bumped live nadlan-config.php: \'campaign-brief\' after \'mortgage-market\', once"""',
      "    txt = apply('nadlan-config.php', txt)", "    if txt.count(MAIN_NEW) != 1:",
      "        raise SystemExit('ashira_599: FATAL: the module list does not end with campaign-brief exactly once')", "    return txt", ""]
open(os.path.join(H, "ashira_599.py"), "w", encoding="utf-8", newline="\n").write("\n".join(AP))

# ---------------------------------------------------------------- deploy599.py from deploy598.py
src = open(os.path.join(H, "deploy598.py"), encoding="utf-8").read()


def one(old, new, what):
    global src
    n = src.count(old)
    assert n == 1, "%s: anchor x%d" % (what, n)
    src = src.replace(old, new)


for a, b in [("1.72.598", "1.72.599"), ("ps598", "ps599"), ("bak598", "bak599"), ("make_deploy598", "make_deploy599"),
             ("deploy-result-598", "deploy-result-599"), ("speed-598", "speed-599"), ("posts-before-598", "posts-before-5_98"),
             ("deploy-result-597", "deploy-result-598"), ("1.72.597", "1.72.598")]:
    src = src.replace(a, b)
src = src.replace("posts-before-5_98", "posts-before-599")
BS = chr(92)
src = re.sub(r"\?t598([a-z]?)=1", "?t599" + BS + "1=1", src)
src = re.sub(r"&t598([a-z]?)=1", "&t599" + BS + "1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(598, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import ashira_598 as PX  # noqa: E402 \([^)]*\)", "import ashira_599 as PX  # noqa: E402 (1.72.599: the nlcamp entry, its two summaries, the campaign-brief module)", src); assert n == 1, n
src, n = re.subn(r'print\("RELEASE 1\.72\.599 LIVE: [^"]*"\)', 'print("RELEASE 1.72.599 LIVE: the campaign planner nlcamp + inc/campaign-brief.php (HAD-678); the page /international-campaigns/ follows on its own")', src); assert n == 1, n
lines = src.split("\n")
seen = set()
for k, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
    elif l.startswith("NEWFILES = "):
        lines[k] = "NEWFILES = set(" + repr(sorted(FILES)) + ")  # 1.72.599: the planner and its server file, both new"; seen.add("NEWFILES")
    elif l.startswith("FILES = ["):
        lines[k] = "FILES = " + repr(FILES); seen.add("FILES")
    elif l.startswith("PHP_RELS = ["):
        lines[k] = "PHP_RELS = " + repr(PHP_RELS) + "  # 1.72.599: the two hunked PHP files, restored from .bak599 on rollback"; seen.add("PHP_RELS")
assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
src = "\n".join(lines)

# the checks after the release: the planner file as served, and the mortgage page still renders with the new registry
T = "/wp-content/plugins/nadlan-config/assets/instruments/"
ADD = [(T + "tools/nlcamp.js?t599x=1", ["NLCAMP", "register('nlcamp'"], ["Fatal error"]),
       ("/mortgage-calculator/?t599w=1", ['data-nli="mquick"', 'data-nli="mrishum"'], ["Fatal error"])]
_ca = [l for l in src.split("\n") if l.startswith("    ('/wp-content/plugins/nadlan-config/assets/instruments/tools/mcheck.js?t599m=1',")]
assert len(_ca) == 1, len(_ca)
src = src.replace(_ca[0], "".join("    (%r, %r, %r),\n" % t for t in ADD) + _ca[0], 1)

# /health names campaign_brief 1.1.0, and the REST route answers 400 to an empty body (not 404)
VERIFY_CB = '''def verify_cb():
    """1.72.599 (HAD-678): the campaign-brief module is loaded. /health (inc/health.php, its own fixed answer, cached 2 minutes) says
    1.72.599; the module's line campaign_brief 1.1.0 rides the nadlan_config_healthcheck filter, which is served at /healthcheck, not at
    /health (checked 7.11 on the live site: /health has 12 keys, /healthcheck carries every module line). POST
    /wp-json/nadlan/v1/campaign-brief answers 400 nlc_bad to an empty body (404 = the route is not registered); an empty body is refused
    before the rate limit and the store: nothing is saved, mailed or counted."""
    ok = True
    for pth in ("/wp-json/nadlan/v1/health", "/wp-json/nadlan/v1/healthcheck"):
        try:
            s, h2 = req("GET", pth + "?nlv=cb" + str(int(time.time())), auth=False)
        except Exception as e:
            s, h2 = str(e)[:60], {}
        cb = h2.get("campaign_brief") if isinstance(h2, dict) else None
        good = s == 200 and isinstance(h2, dict) and h2.get("version") == "1.72.599"
        if pth.endswith("/healthcheck"):
            good = good and isinstance(cb, dict) and cb.get("version") == "1.1.0"
        print(f"[cb] {'OK ' if good else 'BAD'} {pth} {s} {h2.get('version') if isinstance(h2, dict) else '-'} campaign_brief {json.dumps(cb, ensure_ascii=False)}")
        ok = ok and good
    r = urllib.request.Request(BASE + "/wp-json/nadlan/v1/campaign-brief", data=b"", method="POST", headers={"User-Agent": UA, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(r, timeout=60) as resp:
            s2, b2 = resp.status, resp.read()
    except urllib.error.HTTPError as e:
        s2, b2 = e.code, e.read()
    except Exception as e:
        s2, b2 = str(e)[:60], b""
    good = s2 == 400 and b'"nlc_bad"' in b2
    print(f"[cb] {'OK ' if good else 'BAD'} POST /wp-json/nadlan/v1/campaign-brief, empty body: {s2} {b2[:160].decode('utf-8', 'replace')} (want 400 nlc_bad)")
    return ok and good


def run_checks(tag):'''
one("def run_checks(tag):", VERIFY_CB, "verify_cb def")
one('    if not bad and not verify_nf3():\n        bad = ["near-finder-v3"]\n    return bad',
    '    if not bad and not verify_nf3():\n        bad = ["near-finder-v3"]\n    if not bad and not verify_cb():\n        bad = ["campaign-brief"]\n    return bad', "verify_cb hook")

# the module list hunk, on the bumped live text (after the check that it is the 1.72.598 list, mortgage-market last)
one('        raise SystemExit("FATAL: the live module list is not the 1.72.598 one (mortgage-market last)")\n    new_main = text.encode("utf-8")',
    '        raise SystemExit("FATAL: the live module list is not the 1.72.598 one (mortgage-market last)")\n'
    "    text = PX.apply_main(text)  # 1.72.599 (HAD-678): 'campaign-brief' joins the module list after 'mortgage-market' (ashira_599, anchor x1)\n"
    "    print(\"[plan] nadlan-config.php: the module list now ends 'mortgage-market', 'campaign-brief'\")\n"
    '    new_main = text.encode("utf-8")', "module hunk")
# nadlan-config.php is in PHP_RELS now: the rollback restores it once
one('    for rel in ["nadlan-config.php"] + PHP_RELS + [r for r in FILES if r not in NEWFILES]:',
    '    for rel in list(dict.fromkeys(["nadlan-config.php"] + PHP_RELS + [r for r in FILES if r not in NEWFILES])):  # 1.72.599: once each, main file first',
    "rollback list")
assert "598" not in "".join(l for l in src.split("\n") if l.startswith(("PIN = ", "NEWFILES = ", "FILES = ", "PHP_RELS = ", "BAK = ", "NS = ")))
open(os.path.join(H, "deploy599.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy599.py + ashira_599.py written | t599 markers:", len(re.findall(r"t599[a-z]?=1", src)),
      "| pins:", {k.split("/")[-1]: v[:10] for k, v in PIN.items()}, "| PHP_RELS:", PHP_RELS)
