# -*- coding: utf-8 -*-
"""make deploy600.py from deploy599.py: 1.72.600 the marketing budget tool nlbudget (HAD-678, 7.11.2026), "כמה עולה לשווק את הפרויקט".
Built and tested in docs/research/2026-11-07-campaign-network/build/build-nlbudget/ (node 84, PHP 23, browser 317); the exact PHP of the
release step is that folder's registry.php.txt (the entry, the two summary branches, the summary function nadlan_nlb_summary()).
  NEW assets/instruments/tools/nlbudget.js   the tool (window.NLBUDGET, register('nlbudget'))
  NEW assets/instruments/data/nlbudget.json  every number it shows (33 figures, 17 budget lines; built by build_nlbudget_data.py)
Hunks on the LIVE inc/instruments.php only (ashira_600.py, every anchor must be found exactly once or the runner stops before any write):
  (1) the nlbudget entry right after the nlcamp entry (anchor: the nlcamp entry's last three lines + the 1.72.593 mkeys comment),
  (2a) the Hebrew summary branch right after the nlcamp Hebrew branch of nadlan_nli_summary(), (2b) the English branch right after the
  nlcamp English branch of nadlan_nli_summary_en(), (2c) the function nadlan_nlb_summary() right after nadlan_nli_mrates() (anchor: its
  closing lines + the "Effective annual %" comment). Fetched, hunked, linted and written by the runner's PX loop.
nadlan-config.php: the version only (no new inc/ module, so the module list is checked, not changed: it must still end 'campaign-brief').
PHP_RELS = ['inc/instruments.php']: a rollback restores it (and nadlan-config.php, always) from .bak600, then removes the two new files.
No page, post, option or meta is written: [nadlan_tool id="nlbudget"] on /marketing/ (page 8827) follows on its own.
The repo inc/instruments.php gets the same four hunks (as 1.72.597 / 598 / 599 did); the repo nadlan-config.php is NOT touched."""
import hashlib, io, os, re, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
D = os.path.join(REPO, "docs", "research", "2026-11-07-campaign-network", "build", "build-nlbudget")
NL = chr(10)
FILES = ["assets/instruments/tools/nlbudget.js", "assets/instruments/data/nlbudget.json"]
RELS = ["inc/instruments.php"]        # fetched, hunked and written by the runner's PX loop
PHP_RELS = ["inc/instruments.php"]    # every hunked PHP file: restored from .bak600 on rollback (nadlan-config.php is always restored)
for _r in FILES:
    assert os.path.exists(os.path.join(PLUG, *_r.split("/"))), "missing " + _r
PIN = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}

# ---------------------------------------------------------------- the hunks, cut from registry.php.txt
reg = io.open(os.path.join(D, "registry.php.txt"), encoding="utf-8").read().replace(chr(13) + NL, NL)
_k = reg.index("\t\t\t/* 7.11.2026 (HAD-678): ")
_close = NL + "\t\t\t)," + NL
_e = reg.index(_close, reg.index("\t\t\t'nlbudget' => array(", _k)) + len(_close)
ENTRY = reg[_k:_e]
assert ENTRY.count("'nlbudget' => array(") == 1 and ENTRY.count("'en' => array(") == 1 and ENTRY.endswith(_close[1:]), "entry cut"
assert "'data' => array( 'nlbudget.json' )," in ENTRY, "entry data file"


def line(t, needle):
    assert t.count(needle) == 1, ("needle", needle, t.count(needle))
    c = t.index(needle); a = t.rfind(NL, 0, c) + 1; b = t.index(NL, c) + 1
    return t[a:b]


SUM_HE = line(reg, "nadlan_nlb_summary( 'he' )")
SUM_EN = line(reg, "nadlan_nlb_summary( 'en' )")
for _s in (SUM_HE, SUM_EN):
    assert _s.startswith("\t\tif ( 'nlbudget' === $id ) { return function_exists( 'nadlan_nlb_summary' )"), _s
_f = reg.index("\t/** HAD-678 (7.11.2026): the plain summary of nlbudget")
FUNC = reg[_f:].rstrip() + NL
assert FUNC.endswith("\t\t}" + NL + "\t}" + NL) and FUNC.count("function nadlan_nlb_summary(") == 1 and FUNC.count("if ( ! function_exists( 'nadlan_nlb_summary' ) ) {") == 1, "function cut"
assert "dirname( __DIR__ ) . '/assets/instruments/data/nlbudget.json'" in FUNC, "data path"
assert not re.search("[–—]", ENTRY + SUM_HE + SUM_EN + FUNC), "long dash"

# the anchors on the live 1.72.599 text (what 1.72.599 wrote: the nlcamp entry and its two branches; nadlan_nli_mrates() of 1.72.588)
NLCAMP_TAIL = ("\t\t\t\t\t'related' => array(),  // no English B2B page is confirmed yet; empty, so the Hebrew links stay off the English page\n"
               "\t\t\t\t),\n\t\t\t),\n")
A1 = "\t\t\t/* 1.72.593 (HAD-675, T4): from contract to keys, the 7th tool of /mortgage-calculator/"
CB_HE = "\t\tif ( 'nlcamp' === $id ) { return function_exists( 'nadlan_cb_summary' ) ? nadlan_cb_summary( 'he' ) : ''; }  // 7.11.2026: inc/campaign-brief.php\n"
CB_EN = "\t\tif ( 'nlcamp' === $id ) { return function_exists( 'nadlan_cb_summary' ) ? nadlan_cb_summary( 'en' ) : ''; }  // 7.11.2026: inc/campaign-brief.php\n"
MR_END = "\t\treturn $x;\n\t}\n"
A4 = "\t/** Effective annual % -> nominal for a monthly payment (the Bank of Israel conversion), and the Spitzer payment. */\n"
sys.path.insert(0, H)
import ashira_599 as P599  # noqa: E402  the 600 anchors are 599's own new text (nlcamp), so they are proven against what 599 wrote
_n599 = "".join(new for old, new, n in P599.HUNKS["inc/instruments.php"])
assert (NLCAMP_TAIL + A1) in _n599 and CB_HE in _n599 and CB_EN in _n599, "the 600 anchors are not the 599 text"
HUNKS = {"inc/instruments.php": [(NLCAMP_TAIL + A1, NLCAMP_TAIL + ENTRY + A1, 1),
                                 (CB_HE, CB_HE + SUM_HE, 1),
                                 (CB_EN, CB_EN + SUM_EN, 1),
                                 (MR_END + A4, MR_END + FUNC + A4, 1)]}
ABSENT = {"inc/instruments.php": ["'nlbudget' => array(", "nadlan_nlb_summary("]}
ML599 = ("'home-v3', 'pro-card', 'cta-sheet', 'deal-sign', 'instruments', 'compound-tool', 'price-nudge', 'project-kit', 'city-projects', "
         "'radius-prices', 'project-facts', 'near-finder', 'near-alerts', 'mortgage-market', 'campaign-brief' ) as $nadlan_mod")
assert ML599 == P599.MAIN_NEW, "the live module list is the one 1.72.599 wrote"

# ---------------------------------------------------------------- the repo inc/instruments.php (bookkeeping, as 1.72.597 / 598 / 599)
_ip = os.path.join(PLUG, "inc", "instruments.php")
_raw = open(_ip, "rb").read(); _crlf = b"\r\n" in _raw
_it = _raw.decode("utf-8").replace("\r\n", NL)
if "'nlbudget' => array(" in _it:
    assert all(_it.count(new) == 1 for old, new, n in HUNKS["inc/instruments.php"]), "repo instruments.php holds only part of nlbudget; restore it first"
    print("repo inc/instruments.php: already holds the four nlbudget hunks")
else:
    assert "nadlan_nlb_summary(" not in _it, "repo instruments.php holds a stray nadlan_nlb_summary; restore it first"
    for old, new, n in HUNKS["inc/instruments.php"]:
        assert _it.count(old) == n, ("repo anchor", old[:60], _it.count(old))
        _it = _it.replace(old, new)
    io.open(_ip, "w", encoding="utf-8", newline="").write(_it.replace(NL, "\r\n") if _crlf else _it)
    print("repo inc/instruments.php: the four nlbudget hunks applied")

# ---------------------------------------------------------------- ashira_600.py
AP = ["# -*- coding: utf-8 -*-",
      '"""Release 1.72.600 (HAD-678, the budget tool nlbudget): four insert hunks on the LIVE inc/instruments.php (the runner\'s PX loop):',
      "the entry after nlcamp's, the he / en summary branches after nlcamp's, nadlan_nlb_summary() after nadlan_nli_mrates(). No hunk on",
      "nadlan-config.php (the version only). Every anchor must be found exactly once and the new text must be absent, or the release stops",
      'before any write. Generated by make_deploy600.py."""',
      "RELS = " + repr(RELS), "HUNKS = " + repr(HUNKS), "ABSENT = " + repr(ABSENT), "MAIN_LIST = " + repr(ML599), "", "",
      "def apply(rel, txt):", "    if rel not in HUNKS:", "        raise SystemExit('ashira_600: no hunk on ' + rel)",
      "    for s in ABSENT.get(rel, []):", "        if s in txt:",
      "            raise SystemExit('ashira_600: FATAL: the live %s already holds %r; read it before releasing' % (rel, s))",
      "    for old, new, n in HUNKS[rel]:", "        if new in txt:", "            raise SystemExit('ashira_600: FATAL: the live %s already holds the new text' % rel)",
      "        k = txt.count(old)", "        if k != n:", "            raise SystemExit('ashira_600: FATAL: anchor x%d (want %d) in the live %s: %r' % (k, n, rel, old[:90]))",
      "        txt = txt.replace(old, new)", "    return txt", ""]
open(os.path.join(H, "ashira_600.py"), "w", encoding="utf-8", newline="\n").write("\n".join(AP))

# ---------------------------------------------------------------- deploy600.py from deploy599.py
src = open(os.path.join(H, "deploy599.py"), encoding="utf-8").read()


def one(old, new, what):
    global src
    n = src.count(old)
    assert n == 1, "%s: anchor x%d" % (what, n)
    src = src.replace(old, new)


for a, b in [("1.72.599", "1.72.600"), ("ps599", "ps600"), ("bak599", "bak600"), ("make_deploy599", "make_deploy600"),
             ("deploy-result-599", "deploy-result-600"), ("speed-599", "speed-600"), ("posts-before-599", "posts-before-600"),
             ("deploy-result-598", "deploy-result-599"), ("1.72.598", "1.72.599")]:
    src = src.replace(a, b)
BS = chr(92)
src = re.sub(r"\?t599([a-z]?)=1", "?t600" + BS + "1=1", src)
src = re.sub(r"&t599([a-z]?)=1", "&t600" + BS + "1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(599, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import ashira_599 as PX  # noqa: E402 \([^)]*\)", "import ashira_600 as PX  # noqa: E402 (1.72.600: the nlbudget entry, its two summaries, nadlan_nlb_summary())", src); assert n == 1, n
src, n = re.subn(r'print\("RELEASE 1\.72\.600 LIVE: [^"]*"\)', 'print("RELEASE 1.72.600 LIVE: the budget tool nlbudget (HAD-678): tools/nlbudget.js + data/nlbudget.json, its registry entry and he / en summaries; the nlbudget shortcode on /marketing/ follows on its own")', src); assert n == 1, n
lines = src.split("\n")
seen = set()
for k, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
    elif l.startswith("NEWFILES = "):
        lines[k] = "NEWFILES = set(" + repr(sorted(FILES)) + ")  # 1.72.600: the budget tool and its data file, both new"; seen.add("NEWFILES")
    elif l.startswith("FILES = ["):
        lines[k] = "FILES = " + repr(FILES); seen.add("FILES")
    elif l.startswith("PHP_RELS = ["):
        lines[k] = "PHP_RELS = " + repr(PHP_RELS) + "  # 1.72.600: the one hunked PHP file, restored from .bak600 on rollback (nadlan-config.php always is)"; seen.add("PHP_RELS")
assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
src = "\n".join(lines)

# the module list: 1.72.600 adds no module; the live list must still be the one 1.72.599 wrote (campaign-brief last), and is not changed
_a = src.index('    if text.count("\'project-stage\', \'together\'") != 1 or text.count(')
_b = src.index('    new_main = text.encode("utf-8")', _a)
_blk = src[_a:_b]
assert src.count('    if text.count("\'project-stage\', \'together\'") != 1 or text.count(') == 1
assert "PX.apply_main(text)" in _blk and "'mortgage-market' ) as $nadlan_mod\") != 1:" in _blk and _blk.count("\n") == 4, _blk
src = src[:_a] + (
    '    if text.count("\'project-stage\', \'together\'") != 1 or text.count(PX.MAIN_LIST) != 1:\n'
    '        raise SystemExit("FATAL: the live module list is not the 1.72.599 one (campaign-brief last)")\n'
    "    print(\"[plan] nadlan-config.php: the version only; the module list stays as 1.72.599 wrote it ('mortgage-market', 'campaign-brief' last)\")\n"
) + src[_b:]
assert "apply_main" not in src

# inc/near-finder.php c7fffca3f0 was written by 1.72.595 (deploy-result-595.json); the carried-over messages named the release before
one("    # private), on the live near-finder.php that 1.72.599 wrote (", "    # private), on the live near-finder.php that 1.72.595 wrote (", "nf comment")
one('is not what 1.72.599 wrote (1.72.600 does not touch it)")', 'is not what 1.72.595 wrote (1.72.600 does not touch it)")', "nf fatal")
one("c7fffca3f0 = 1.72.599's; read, not written", "c7fffca3f0 = 1.72.595's; read, not written", "nf print")

# a shipped data file must parse before anything is written
one('        print(f"[lint] {rel}: node --check ok")\nHEAD = {',
    '        print(f"[lint] {rel}: node --check ok")\n'
    '    elif rel.endswith(".json"):  # 1.72.600: a data file must parse before it is written\n'
    '        try:\n'
    '            _j = json.loads(NEW[rel].decode("utf-8"))\n'
    '        except Exception as _e:\n'
    '            raise SystemExit(f"FATAL local JSON {rel}: {_e}")\n'
    '        print(f"[lint] {rel}: JSON ok ({len(_j.get(\'figures\') or {}) if isinstance(_j, dict) else \'-\'} figures)")\n'
    'HEAD = {', "json lint")

# the checks after the release: the tool and its data as served, /marketing/ (page 8827) and the mortgage page still render
T = "/wp-content/plugins/nadlan-config/assets/instruments/"
ADD = [(T + "tools/nlbudget.js?t600x=1", ["NLBUDGET", "register('nlbudget'"], ["Fatal error"]),
       (T + "data/nlbudget.json?t600x=1", ['"nlbudget"', '"figures"', '"sp_sm"', '"se_ex"', '"nl_plans"'], ["Fatal error"]),
       ("/marketing/?t600v=1", ['data-nli="nlcamp"'], ["Fatal error"]),
       ("/mortgage-calculator/?t600v=1", ['data-nli="mquick"', 'data-nli="mrishum"'], ["Fatal error"])]
_ca = [l for l in src.split("\n") if l.startswith("    ('/wp-content/plugins/nadlan-config/assets/instruments/tools/nlcamp.js?t600x=1',")]
assert len(_ca) == 1, len(_ca)
src = src.replace(_ca[0], "".join("    (%r, %r, %r),\n" % t for t in ADD) + _ca[0], 1)

# the data file parses as served and holds the build's counts; the tool file carries its register line
VERIFY_NLB = '''def verify_nlb():
    """1.72.600 (HAD-678): the budget tool as the site serves it. tools/nlbudget.js carries register('nlbudget' and window.NLBUDGET;
    data/nlbudget.json parses as JSON, key nlbudget, 33 figures and 17 budget lines (the counts of build-nlbudget/README.md)."""
    T = "/wp-content/plugins/nadlan-config/assets/instruments/"
    q = "&nlv=nb" + str(int(time.time()))
    try:
        s, b = req("GET", T + "tools/nlbudget.js?t600x=1" + q, raw=True, auth=False, timeout=90)
    except Exception as e:
        s, b = str(e)[:60], b""
    nreg = b.count(b"register('nlbudget'")
    good_js = s == 200 and nreg >= 1 and b"window.NLBUDGET" in b
    print(f"[nlb] {'OK ' if good_js else 'BAD'} tools/nlbudget.js {s} {len(b)} bytes, register('nlbudget' x{nreg}")
    s2, d, err = "-", None, ""
    try:
        s2, b2 = req("GET", T + "data/nlbudget.json?t600x=1" + q, raw=True, auth=False, timeout=90)
        d = json.loads(b2.decode("utf-8"))
    except Exception as e:
        err = str(e)[:80]
    figs = d.get("figures") if isinstance(d, dict) else None
    nf = len(figs) if isinstance(figs, dict) else -1
    nl = len(d.get("lines") or []) if isinstance(d, dict) else -1
    good_json = s2 == 200 and isinstance(d, dict) and d.get("key") == "nlbudget" and nf == 33 and nl == 17
    print(f"[nlb] {'OK ' if good_json else 'BAD'} data/nlbudget.json {s2}: key {d.get('key') if isinstance(d, dict) else '-'}, {nf} figures (want 33), {nl} lines (want 17) {err}")
    return good_js and good_json


def run_checks(tag):'''
one("def run_checks(tag):", VERIFY_NLB, "verify_nlb def")
one('    if not bad and not verify_cb():\n        bad = ["campaign-brief"]\n    return bad',
    '    if not bad and not verify_cb():\n        bad = ["campaign-brief"]\n    if not bad and not verify_nlb():\n        bad = ["nlbudget"]\n    return bad', "verify_nlb hook")
assert "599" not in "".join(l for l in src.split("\n") if l.startswith(("PIN = ", "NEWFILES = ", "FILES = ", "PHP_RELS = ", "BAK = ", "NS = ")))
assert "ashira_599" not in src and "t599" not in src, "a 599 marker is left"
open(os.path.join(H, "deploy600.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy600.py + ashira_600.py written | t600 markers:", len(re.findall(r"t600[a-z]?=1", src)),
      "| pins:", {k.split("/")[-1]: v[:10] for k, v in PIN.items()}, "| PHP_RELS:", PHP_RELS)
