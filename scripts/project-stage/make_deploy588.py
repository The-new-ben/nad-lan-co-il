# -*- coding: utf-8 -*-
"""make deploy588.py from deploy587.py: 1.72.588 MortgageWorld B (HAD-675): the six practical tools of the mortgage page.
NEW files (built and tested in docs/research/2026-11-05-mortgage-world/build/, copied here): tools/mbudget.js ("כמה דירה זה קונה,
ואיפה", the homes on the site read only when the tool comes into view), tools/moffers.js ("שלוש הצעות, טבלה אחת"), tools/mready.js
+ data/mready.json ("מוכנים לאישור עקרוני?", every document sourced and dated), tools/mrates-common.js + tools/mdecision.js +
tools/mreplay.js + tools/mexit.js (the rate decision, "אם 2022 חוזרת", the exit cost). Swapped WHOLE: tools/mquick.js (written by
1.72.587; v2: the amount field first, id-scoped rules over the theme, the tools switcher). FOUR insert/replace hunks on the LIVE
inc/instruments.php (written by 1.72.587): six registry entries before the 'invest' entry; the rate tools' data helper before
nadlan_nli_summary(); six plain-text summary branches before the 'mortgage' one; the enqueue line learns 'deps' (a tool's own
scripts load first, once). nadlan-config.php: the version only (the module list stays the 1.72.587 one). The page content (the
switcher and the six mounts) follows with docs/research/2026-11-05-mortgage-world/build/release-b/write_page_b.py."""
import hashlib, io, os, re
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
BLD = os.path.join(REPO, "docs", "research", "2026-11-05-mortgage-world", "build")
TOOLS = ["mbudget", "moffers", "mready", "mrates-common", "mdecision", "mreplay", "mexit"]
FILES = ["assets/instruments/tools/%s.js" % t for t in TOOLS] + ["assets/instruments/data/mready.json", "assets/instruments/tools/mquick.js"]
NEW = set(FILES) - {"assets/instruments/tools/mquick.js"}
RELS = ["inc/instruments.php"]
PIN = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}


def rd(p):
    return io.open(p, encoding="utf-8").read().replace("\r\n", "\n")


def php_body(txt):
    """A snippet file without its leading '<?php' line."""
    return re.sub(r"^<\?php\s*\n", "", txt)


# ---------------------------------------------------------------- the registry entries
REG_ANCHOR = "\t\t\t/* 1.72.523 (HAD-601, U2): the yield and cash-flow map; invest.json from 148 nadlan.gov.il files (20.8.2026), BoI 4.62% (8.2026) */\n"
reg = ""
for t in ("mbudget", "moffers", "mready"):
    reg += php_body(rd(os.path.join(BLD, t, "registry.php.txt"))).rstrip("\n") + "\n"
_mr = rd(os.path.join(BLD, "mrates", "registry.php.txt"))
_a = _mr.index("\t\t\t/* 1.72.xxx (HAD-675): the three rate tools")
_b = _mr.index("/* ------", _a)
reg += _mr[_a:_b].rstrip("\n").replace("1.72.xxx", "1.72.588") + "\n"
reg = reg.replace("1.72.5xx", "1.72.588")
# ---------------------------------------------------------------- the summaries
SUM_ANCHOR = "\t\t// 1.72.523 (HAD-601, U1): Mortgage 2.0 as plain text\n\t\tif ( 'mortgage' === $id ) {\n"
summ = ""
for t in ("mbudget", "moffers", "mready"):
    summ += php_body(rd(os.path.join(BLD, t, "summary.php.txt"))).rstrip("\n") + "\n"
_ms = rd(os.path.join(BLD, "mrates", "summary.php.txt"))
_ha = _ms.index("\t/** HAD-675: the data of the three rate tools")
_hb = _ms.index("/* ------", _ha)
HELPER = _ms[_ha:_hb].rstrip("\n") + "\n\n"
_sa = _ms.index("\t\tif ( 'mdecision' === $id )")
_sb = _ms.rindex("}") + 1
summ += _ms[_sa:_sb].rstrip("\n") + "\n"
# keep only the branch code: the mrates file's tail may hold notes after the last brace of the mexit branch
assert summ.count("if ( 'mexit' === $id )") == 1 and summ.count("if ( 'mbudget' === $id )") == 1, "summary branches"
HELPER_ANCHOR = "\tfunction nadlan_nli_summary( $id, $lang = 'he' ) {\n"
FILES_OLD = "\t\t$files = array(); foreach ( $ids as $id ) { $files[ ! empty( $tl[ $id ]['file'] ) ? $tl[ $id ]['file'] : $id ] = 1; }\n"
FILES_NEW = ("\t\t// 1.72.588 (HAD-675): a tool's own scripts ('deps', tool ids or shared files) load first, once, in order\n"
             "\t\t$files = array(); foreach ( $ids as $id ) { foreach ( isset( $tl[ $id ]['deps'] ) ? (array) $tl[ $id ]['deps'] : array() as $dep ) { $files[ $dep ] = 1; } $files[ ! empty( $tl[ $id ]['file'] ) ? $tl[ $id ]['file'] : $id ] = 1; }\n")
HUNKS = {"inc/instruments.php": [(REG_ANCHOR, reg + REG_ANCHOR, 1), (HELPER_ANCHOR, HELPER + HELPER_ANCHOR, 1), (SUM_ANCHOR, summ + SUM_ANCHOR, 1), (FILES_OLD, FILES_NEW, 1)]}

# the repo copy carries the same hunks
_ip = os.path.join(PLUG, "inc", "instruments.php")
_it = rd(_ip)
if "'mbudget' => array(" not in _it:
    for old, new, n in HUNKS["inc/instruments.php"]:
        assert _it.count(old) == n, ("repo anchor", old[:60], _it.count(old))
        _it = _it.replace(old, new)
    io.open(_ip, "w", encoding="utf-8", newline="").write(_it)
    print("repo inc/instruments.php: the four hunks applied")
_it = rd(_ip)
for old, new, n in HUNKS["inc/instruments.php"]:
    assert _it.count(new) == 1, ("repo instruments.php does not hold the hunk", new[:80])

AP = [
    "# -*- coding: utf-8 -*-",
    '"""Release 1.72.588 MortgageWorld B: four hunks on the LIVE inc/instruments.php. Generated by make_deploy588.py."""',
    "RELS = " + repr(RELS),
    "HUNKS = " + repr(HUNKS),
    "",
    "",
    "def apply(rel, txt):",
    "    if rel not in HUNKS:",
    "        raise SystemExit('ashira_588: no hunk on ' + rel)",
    "    for old, new, n in HUNKS[rel]:",
    "        if new in txt:",
    "            raise SystemExit('ashira_588: the live %s already holds the new text' % rel)",
    "        k = txt.count(old)",
    "        if k != n:",
    "            raise SystemExit('ashira_588: anchor x%d (want %d) in the live %s' % (k, n, rel))",
    "        txt = txt.replace(old, new)",
    "    return txt",
    "",
]
open(os.path.join(H, "ashira_588.py"), "w", encoding="utf-8", newline="\n").write("\n".join(AP))
src = open(os.path.join(H, "deploy587.py"), encoding="utf-8").read()


def one(old, new, what):
    global src
    n = src.count(old)
    assert n == 1, "%s: anchor x%d" % (what, n)
    src = src.replace(old, new)


# ---------------------------------------------------------------- 1. the module list stays the 1.72.587 one
_ml587 = "'project-facts', 'near-finder', 'near-alerts', 'mortgage-market' ) as $nadlan_mod"
_ml586 = "'project-facts', 'near-finder', 'near-alerts' ) as $nadlan_mod"
one(_ml586 + '") != 1 or "' + "'mortgage-market'" + '" in text:\n        raise SystemExit("FATAL: the live module list is not the 1.72.586 one (near-finder, near-alerts last, no mortgage-market)")\n'
    "    text = text.replace(" + repr(_ml586) + ", " + repr(_ml587) + ")\n",
    _ml587 + '") != 1:\n        raise SystemExit("FATAL: the live module list is not the 1.72.@587@ one (mortgage-market last)")\n', "module list")
one('raise SystemExit("FATAL: the live inc/near-finder.php is not what 1.72.586 wrote; 1.72.587 assumes 1.72.586 is live")',
    'raise SystemExit("FATAL: the live inc/near-finder.php is not what 1.72.586 wrote (1.72.@587@ did not touch it)")', "nf msg")

# ---------------------------------------------------------------- 2. the inherited mortgage-page checks now expect the 5.11 page
one("    ('/mortgage-calculator/?t587b=1', ['class=\"yoast-schema-graph\"'], ['\"breadcrumb\":{\"@id\"']),\n",
    "    ('/mortgage-calculator/?t587b=1', ['class=\"yoast-schema-graph\"', 'id=\"nadlan-page-crumbs\"', 'class=\"nlbc nlbc--page\"'], []),\n", "crumbs check")
one("['Fatal error', 'nlmm__kpis']),", "['Fatal error']),", "market check")

# ---------------------------------------------------------------- 3. the 588 checks
V = "?ver=1.72.@588@"
ADD = [("/wp-content/plugins/nadlan-config/assets/instruments/tools/%s.js?t@588@%s=1" % (t, "abcdefg"[i]), ["NadLanInstruments" if t != "mrates-common" else "NLMR"], ["Fatal error"]) for i, t in enumerate(TOOLS)]
ADD += [
    ("/wp-content/plugins/nadlan-config/assets/instruments/tools/mquick.js?t@588@q=1", ["mquick v1", "wireSwitch", "nlmx-sw", 'id="nlmq"', "אפשר לחשב גם"], ["Fatal error"]),
    ("/wp-content/plugins/nadlan-config/assets/instruments/data/mready.json?t@588@r=1", ['"docs"', '"rules"'], ["Fatal error"]),
    ("/mortgage-calculator/?t@588@m=1", ['data-nli="mquick"', 'tools/mquick.js' + V, 'data-nli="mortgage"', 'id="mortgage-market"', '"@type":"Dataset"', 'id="nadlan-page-crumbs"'], ["Fatal error"]),
    ("/mortgage-calculator/mortgage-repayment-capacity/?t@588@m=1", ['data-nli="afford"', 'tools/afford.js' + V], ["Fatal error"]),
]
_ca = [l for l in src.split("\n") if l.startswith("    ('/wp-content/plugins/nadlan-config/assets/instruments/tools/mquick.js?t587q=1',")][0]
assert src.count(_ca) == 1
src = src.replace(_ca, "".join("    (%r, %r, %r),\n" % t for t in ADD) + _ca)

# ---------------------------------------------------------------- 4. the runner's own lines, then the renames (587 -> 588, 586 -> 587)
lines = src.split("\n")
for i, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[i] = "PIN = " + repr(PIN)
    elif l.startswith("NEWFILES = "):
        lines[i] = "NEWFILES = " + repr(NEW) + "  # 1.72.588: the six tools of the mortgage page and mready.json"
    elif l.startswith("FILES = ["):
        lines[i] = "FILES = " + repr(FILES)
    elif l.startswith("PHP_RELS = ["):
        lines[i] = "PHP_RELS = " + repr(RELS) + "  # 1.72.588: the hunked instruments.php, restored from .bak588 on rollback BEFORE the new files are removed"
src = "\n".join(lines)
for a, b in [("1.72.587", "1.72.588"), ("ps587", "ps588"), ("bak587", "bak588"), ("make_deploy587", "make_deploy588"),
             ("deploy-result-587", "deploy-result-588"), ("speed-587", "speed-588"), ("posts-before-587", "posts-before-5_87"),
             ("deploy-result-586", "deploy-result-587"), ("1.72.586", "1.72.587")]:
    src = src.replace(a, b)
src = src.replace("posts-before-5_87", "posts-before-588")
src = re.sub(r"\?t587([a-z]?)=1", r"?t588\1=1", src)
src = re.sub(r"&t587([a-z]?)=1", r"&t588\1=1", src)
src = src.replace("@588@", "588").replace("@587@", "587")
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(587, 329, -1)", src)
assert n == 1, n
src, n = re.subn(r"import ashira_587 as PX  # noqa: E402 \([^)]*\)", "import ashira_588 as PX  # noqa: E402 (1.72.588: the four instruments.php hunks)", src)
assert n == 1, n
src, n = re.subn(r'print\("RELEASE 1\.72\.588 LIVE: [^"]*"\)', 'print("RELEASE 1.72.588 LIVE: the six mortgage tools (mbudget, moffers, mready, mdecision, mreplay, mexit), mquick v2 with the switcher, deps in the enqueue; the page content follows with write_page_b.py")', src)
assert n == 1, n
open(os.path.join(H, "deploy588.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy588.py + ashira_588.py written; page checks:", len(ADD), "| pins:", {k.split("/")[-1]: v[:10] for k, v in PIN.items()})
