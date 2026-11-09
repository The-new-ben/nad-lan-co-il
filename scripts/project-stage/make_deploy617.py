# -*- coding: utf-8 -*-
"""make deploy617.py from deploy616.py: 1.72.617 = HAD-686 (Ben 8.11.2026, by voice: the buying guide on /buying-apartment/ must be the
best and biggest in the world, with proof): the guide's reading layer and five new tools.
  NEW  assets/instruments/tools/buying3.js (bpay, bsign, bkeys, breg, bmemo + the guide map and the glossary filter)
  NEW  assets/instruments/tools/buying3.css (the .nlbg-* reading layer, h3 tool titles)
  SWAP inc/buying-hub.php (15 tool ids, the five summaries, h="3" on every buying tool, buying3 enqueue),
       assets/instruments/tools/buying.js (the h3 title survives a redraw), assets/instruments/tools/buying2.js (bdates saves the signing date),
       assets/instruments/data/buying.json (pay, sign, keys, reg, memo; the land8, move_kz, m_notice, water_kz sources)
  The four swapped files are exactly what 1.72.608 wrote (proven below against deploy-result-608 and git HEAD) plus this release's edits.
nadlan-config.php, on its LIVE text: the version only. NO inc/ hunk. No page, post, option or meta: page 9's content is written after
this release is verified (scripts/seo/write_buying_v3_page.py). inc/price-nudge.php and assets/nudge/ are not touched (HAD-684)."""
import hashlib, json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
md5 = lambda b: hashlib.md5(b).hexdigest()
SWAP = ["inc/buying-hub.php", "assets/instruments/tools/buying.js", "assets/instruments/tools/buying2.js", "assets/instruments/data/buying.json"]
NEWF = ["assets/instruments/tools/buying3.js", "assets/instruments/tools/buying3.css"]
FILES = SWAP + NEWF
PIN = {r: md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()) for r in FILES}
for r in FILES:
    b = open(os.path.join(PLUG, *r.split("/")), "rb").read()
    assert b"\r\n" not in b, "CRLF in " + r + " (LF is pinned)"
    assert not re.search("[–—]", b.decode("utf-8")), "long dash in " + r
    if r.endswith(".json"):
        json.loads(b.decode("utf-8"))
assert not [r for r in FILES if "price-nudge" in r or "/nudge/" in r], "HAD-684 files never ride this release"
_bh = open(os.path.join(PLUG, "inc", "buying-hub.php"), encoding="utf-8").read()
assert "function nadlan_bhub_tool_ids() { return array( 'bplan', 'bequity', 'bladder', 'boffer', 'bsell', 'bdates', 'bcompare', 'bvisit', 'bwho', 'bhelp', 'bpay', 'bsign', 'bkeys', 'breg', 'bmemo' ); }" in _bh, "buying-hub.php: the 15 tools"
assert "$b3 = array( 'file' => 'buying3', 'deps' => array( 'prices-common', 'buying', 'buying2' ) );" in _bh, "buying-hub.php: buying3.js after buying2.js"
assert "wp_enqueue_style( 'nadlan-nli-buying3', nadlan_nli_url( 'tools/buying3.css' ), array( 'nadlan-nli' ), $v );" in _bh, "buying-hub.php: buying3.css"
_b3 = open(os.path.join(PLUG, "assets", "instruments", "tools", "buying3.js"), encoding="utf-8").read()
for _id in ("bpay", "bsign", "bkeys", "breg", "bmemo"):
    assert _b3.count("register('%s'" % _id) == 1, "buying3.js: " + _id
# the four swapped files: what 1.72.608 wrote is git HEAD, and nothing released after 608 touched them
_r608 = json.load(open(os.path.join(QA, "deploy-result-608.json"), encoding="utf-8"))
for r in SWAP:
    _head = subprocess.run(["git", "show", "HEAD:plugins/nadlan-config/" + r], cwd=REPO, capture_output=True).stdout
    assert (_r608.get("files") or {}).get(r) == md5(_head), "1.72.608 wrote %s = git HEAD" % r
for n in range(609, 617):
    _f = (json.load(open(os.path.join(QA, "deploy-result-%d.json" % n), encoding="utf-8")).get("files") or {})
    assert not [k for k in _f if k in FILES], "1.72.%d touched a buying file" % n
_php = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
_php = next((os.path.join(_php, d, "php.exe") for d in sorted(os.listdir(_php)) if d.startswith("PHP.PHP.8.1_")), "php") if os.path.isdir(_php) else "php"
for _cmd, _what in ([["node", os.path.join(REPO, "tools", "instruments", "test_buying_hub.js")], "node test_buying_hub.js"],
                    [["node", os.path.join(REPO, "tools", "instruments", "test_prices_hub.js")], "node test_prices_hub.js"],
                    [[_php, "-l", os.path.join(PLUG, "inc", "buying-hub.php")], "php -l buying-hub.php"],
                    [["node", "--check", os.path.join(PLUG, "assets", "instruments", "tools", "buying.js")], "node --check buying.js"],
                    [["node", "--check", os.path.join(PLUG, "assets", "instruments", "tools", "buying2.js")], "node --check buying2.js"],
                    [["node", "--check", os.path.join(PLUG, "assets", "instruments", "tools", "buying3.js")], "node --check buying3.js"]):
    _o = subprocess.run(_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    _last = (_o.stdout.strip().splitlines() or ["ok"])[-1]
    assert _o.returncode == 0 and "FAILED" not in _o.stdout, _what + ": " + _last + " " + _o.stderr[-300:]
    print("[tests]", _what + ":", _last)
_r616 = json.load(open(os.path.join(QA, "deploy-result-616.json"), encoding="utf-8"))
assert str(_r616.get("state", "")).startswith("released"), "1.72.616 record: " + str(_r616.get("state"))
print("[616] released")

AP = open(os.path.join(H, "ashira_616.py"), encoding="utf-8").read().replace("ashira_616", "ashira_617").replace("Release 1.72.616", "Release 1.72.617").replace("make_deploy616.py", "make_deploy617.py")
open(os.path.join(H, "ashira_617.py"), "w", encoding="utf-8", newline="\n").write(AP)
src = open(os.path.join(H, "deploy616.py"), encoding="utf-8").read()


def one(old, new, what):
    global src
    n = src.count(old)
    assert n == 1, "%s: anchor x%d" % (what, n)
    src = src.replace(old, new)


for a, b in [("1.72.616", "1.72.617"), ("ps616", "ps617"), ("bak616", "bak617"), ("make_deploy616", "make_deploy617"),
             ("deploy-result-616", "deploy-result-617"), ("speed-616", "speed-617"), ("posts-before-616", "posts-before-617"),
             ("deploy-result-615", "deploy-result-616"), ("1.72.615", "1.72.616")]:
    src = src.replace(a, b)
BS = chr(92)
src = re.sub(r"\?t616([a-z]?)=1", "?t617" + BS + "1=1", src)
src = re.sub(r"&t616([a-z]?)=1", "&t617" + BS + "1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(616, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import ashira_616 as PX  # noqa: E402 \(.*$", "import ashira_617 as PX  # noqa: E402 (1.72.617: no inc/ hunk; the module list unchanged)", src, flags=re.M); assert n == 1, n
src, n = re.subn(r'print\("RELEASE 1\.72\.617 LIVE: [^"]*"\)',
                 'print("RELEASE 1.72.617 LIVE: the buying guide reading layer + bpay, bsign, bkeys, breg, bmemo (buying3.js, buying3.css). NEXT: write page 9 v3 (scripts/seo/write_buying_v3_page.py), then press every tool at 390 and 1366")', src); assert n == 1, n
lines = src.split("\n"); seen = set()
for k, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
    elif l.startswith("NEWFILES = "):
        lines[k] = "NEWFILES = set(" + repr(sorted(NEWF)) + ")  # 1.72.617: buying3.js + buying3.css; the four buying files are swaps (from .bak617)"; seen.add("NEWFILES")
    elif l.startswith("FILES = ["):
        lines[k] = "FILES = " + repr(FILES); seen.add("FILES")
    elif l.startswith("PHP_RELS = ["):
        lines[k] = "PHP_RELS = []  # 1.72.617: no hunked PHP; nadlan-config.php is restored from .bak617 on rollback as always"; seen.add("PHP_RELS")
assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
src = "\n".join(lines)
one("'inc/owner-mail.php', 'inc/mortgage-market.php', 'nadlan-config.php' ) as $f ) { @opcache_invalidate( $root . $f, true ); }",
    "'inc/owner-mail.php', 'inc/mortgage-market.php', 'inc/buying-hub.php', 'nadlan-config.php' ) as $f ) { @opcache_invalidate( $root . $f, true ); }", "opcache list")
one("$o['js2'] = is_readable( WP_PLUGIN_DIR . '/nadlan-config/assets/instruments/tools/buying2.js' );",
    "$o['js2'] = is_readable( WP_PLUGIN_DIR . '/nadlan-config/assets/instruments/tools/buying2.js' ); $o['js3'] = is_readable( WP_PLUGIN_DIR . '/nadlan-config/assets/instruments/tools/buying3.js' ); $o['css3'] = is_readable( WP_PLUGIN_DIR . '/nadlan-config/assets/instruments/tools/buying3.css' );", "probe files")
one("foreach ( array( 'bplan', 'bequity', 'bladder', 'boffer', 'bsell', 'bdates', 'bcompare', 'bvisit', 'bwho', 'bhelp' ) as $id )",
    "foreach ( array( 'bplan', 'bequity', 'bladder', 'boffer', 'bsell', 'bdates', 'bcompare', 'bvisit', 'bwho', 'bhelp', 'bpay', 'bsign', 'bkeys', 'breg', 'bmemo' ) as $id )", "probe ids")
one('all(p.get(k) is True for k in ("module", "json", "js", "js2", "bplan", "bequity", "bladder", "boffer", "bsell", "bdates", "bcompare", "bvisit", "bwho", "bhelp"))',
    'all(p.get(k) is True for k in ("module", "json", "js", "js2", "js3", "css3", "bplan", "bequity", "bladder", "boffer", "bsell", "bdates", "bcompare", "bvisit", "bwho", "bhelp", "bpay", "bsign", "bkeys", "breg", "bmemo"))', "verify_buy keys")
src, n = re.subn(r"served_exact \(\d+ files at \?ver=1\.72\.617, byte for byte\)", "served_exact (5 files at ?ver=1.72.617, byte for byte)", src); assert n == 1, n
one("\nH1_EXACTLY_ONE = ",
    "\n# 1.72.617 (HAD-686): the guide's reading layer and the five new tools are served, and page 9 loads them\n"
    "CHECKS += [\n"
    "    ('/buying-apartment/?t617g=1', ['<body', '<h1', 'data-nli=\"bplan\"', 'tools/buying3.js?ver=1.72.617', 'tools/buying3.css?ver=1.72.617'], ['Fatal error']),\n"
    "    ('/wp-content/plugins/nadlan-config/assets/instruments/tools/buying3.js?t617h=1', [\"register('bpay'\", \"register('bsign'\", \"register('bkeys'\", \"register('breg'\", \"register('bmemo'\", 'nlbg-map', 'nlbg-gloss'], ['Fatal error']),\n"
    "    ('/wp-content/plugins/nadlan-config/assets/instruments/tools/buying3.css?t617i=1', ['.nlbg-map', '.nlbg-note--fig', '.nlbg-tbl'], ['<html']),\n"
    "    ('/wp-content/plugins/nadlan-config/assets/instruments/data/buying.json?t617j=1', ['\"land8\"', '\"m_notice\"', '\"water_kz\"', '\"help_out\"', '\"who_contract\"'], ['<html']),\n"
    "    ('/apartment-prices/?t617k=1', ['<body', '<h1'], ['Fatal error']),\n"
    "]\nH1_EXACTLY_ONE = ", "617 rows")
assert "ashira_616 as PX" not in src and "t616" not in src and "deploy-result-615" not in src
assert src.count('WANT_LIVE = "1.72.616"') == 1 and src.count('BAK = ".bak617"') == 1 and src.count("range(616, 329, -1)") == 1 and src.count("def verify_buy():") == 1
open(os.path.join(H, "deploy617.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy617.py + ashira_617.py written | pins:", {k.split("/")[-1]: v[:10] for k, v in PIN.items()})
