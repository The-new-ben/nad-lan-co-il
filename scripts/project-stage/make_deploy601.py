# -*- coding: utf-8 -*-
"""make deploy601.py from deploy600.py: 1.72.601 (HAD-678, 7.11.2026), the marketing hub linked + the budget lines folded on phones.

  SWAP assets/instruments/tools/nlbudget.js (v1.1): the 17 budget lines sit in a native <details> fold, "כל שורות התקציב (17)" /
       "All budget lines (17)", closed under 768 px, open from 768 px (a 44 px summary in the anchors panel's open/close look). Tested in
       docs/research/2026-11-07-campaign-network/build/build-nlbudget/ (node 88 of 88, browser 344 of 344; the tool on a 390 px phone
       7,241 px tall open, 3,185 px folded). Written over the live file 1.72.600 wrote (deploy-result-600.json), new PIN below.
  Hunks on the LIVE text (ashira_601.py; every anchor exactly once, "/marketing/" absent before, or the runner stops before any write),
  one small additive link to https://nad-lan.co.il/marketing/ (page 8827) per place, in that place's own link style:
    inc/developers-page.php    /developers/: a third card in the existing .nldev-tour row, "כמה עולה לשווק פרויקט נדל״ן"
    inc/advertise-tiers.php    /advertise/: the fine-print line, after "כל המסלולים והמחירים", "כמה עולה לשווק פרויקט נדל״ן"
    inc/advertiser-center.php  the signed-in advertiser center: a .nlac-muted line under "מסלולי פרסום זמינים". NOTE: a visitor who is not
                               signed in (and Google) gets the THEME's gate (functions.php, nadlan_revenue_premium_gateway_markup), not
                               this file; the theme is not touched, so the public /advertiser-center/ shows no new link.
    inc/legal-links.php        the site footer: the plugin's own fourth column "מחשבונים וכלים" (the three other columns are the theme's
                               static part, not touched), Hebrew pages only: "מחשבון תקציב שיווק לפרויקט". This puts one link on EVERY
                               Hebrew page that has the theme footer at once: the owner's law asks Ben's explicit OK for a sitewide link.
                               Build without it:  python make_deploy601.py --no-footer
  Each file's live text is PROVEN before it is hunked: the last release record that wrote it (deploy-result-N.json "files") or, when no
  release since 1.72.432 wrote it, the live manifest read at 1.72.432 (.claude/worktrees/live-truth/live-truth/LIVE-MANIFEST.json); the
  repo copy must have that md5 (the repo text IS the live text), and the runner refuses unless the live md5 is that md5. A file whose
  live text cannot be proven is left out (printed), never hunked blind.
nadlan-config.php: the version only (the module list must still be the one 1.72.599 wrote, campaign-brief last).
PHP_RELS = the hunked PHP files: a rollback restores them (and nadlan-config.php, always, and nlbudget.js) from .bak601.
No page, post, option or meta is written. The repo copies of the hunked files get the same hunks (bookkeeping, as 1.72.597 to 600 did);
the repo nadlan-config.php is NOT touched."""
import hashlib, io, json, os, re, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
MANIFEST = os.path.join(REPO, ".claude", "worktrees", "live-truth", "live-truth", "LIVE-MANIFEST.json")
NL = chr(10)
FOOTER = "--no-footer" not in sys.argv[1:]
FILES = ["assets/instruments/tools/nlbudget.js"]
for _r in FILES:
    assert os.path.exists(os.path.join(PLUG, *_r.split("/"))), "missing " + _r
PIN = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
assert PIN["assets/instruments/tools/nlbudget.js"] != "d6b1e218d3020ca6ef6ac2c8a22ff4bd", "nlbudget.js is still the 1.72.600 file"
_nb = open(os.path.join(PLUG, "assets", "instruments", "tools", "nlbudget.js"), encoding="utf-8").read()
assert "linesHead: 'כל שורות התקציב ({n})'" in _nb and "linesHead: 'All budget lines ({n})'" in _nb and "matchMedia('(max-width:767px)')" in _nb, "nlbudget.js has no fold"
md5 = lambda b: hashlib.md5(b).hexdigest()

# ---------------------------------------------------------------- the proof of each file's live text
MF = {f["path"]: f["md5"] for f in json.load(open(MANIFEST, encoding="utf-8"))["files"]}
MF_VER = json.load(open(MANIFEST, encoding="utf-8"))["plugin_version"]
assert MF_VER == "1.72.432", MF_VER


def proof(rel):
    """(md5, why) of the live file at 1.72.600, from the records alone; None when it cannot be proven"""
    for n in range(600, 254, -1):
        p = os.path.join(QA, f"deploy-result-{n}.json")
        if not os.path.exists(p):
            if n > 432:
                return None  # a release after the manifest without a record: not provable
            continue
        f = (json.load(open(p, encoding="utf-8")).get("files") or {}).get(rel)
        if f:
            return f, f"written by 1.72.{n} (deploy-result-{n}.json)"
        if n == 433:
            break
    if rel in MF:
        return MF[rel], "the live manifest at 1.72.432 (7.10.2026); no release since wrote it (records 433 to 600)"
    return None


HUN = "כמה עולה לשווק פרויקט נדל״ן"
TOOL = "מחשבון תקציב שיווק לפרויקט"
PLACES = {
    "inc/developers-page.php": [(
        "\t\t<a class=\"nldev-tour\" href=\"<?php echo $sdedov; ?>\">\n\t\t\t<b>רובע שדה דב</b>\n\t\t\t<span>סיור עם מעבר בין המצב הקיים לתכנון העתידי</span>\n\t\t</a>\n\t</div>\n",
        "\t\t<a class=\"nldev-tour\" href=\"<?php echo $sdedov; ?>\">\n\t\t\t<b>רובע שדה דב</b>\n\t\t\t<span>סיור עם מעבר בין המצב הקיים לתכנון העתידי</span>\n\t\t</a>\n"
        "\t\t<a class=\"nldev-tour\" href=\"<?php echo esc_url( home_url( '/marketing/' ) ); ?>\">\n\t\t\t<b>" + HUN + "</b>\n"
        "\t\t\t<span>תקציב השיווק והמכירה של הפרויקט, שורה אחר שורה, עם המקור של כל מספר</span>\n\t\t</a>\n\t</div>\n", 1)],
    "inc/advertise-tiers.php": [(
        "<a href=\"' . esc_url( home_url( '/join-pro/' ) ) . '\">כל המסלולים והמחירים</a></p>';\n",
        "<a href=\"' . esc_url( home_url( '/join-pro/' ) ) . '\">כל המסלולים והמחירים</a><span aria-hidden=\"true\"> · </span>"
        "<a href=\"' . esc_url( home_url( '/marketing/' ) ) . '\">" + HUN + "</a></p>';  // 1.72.601 (HAD-678): the marketing hub\n", 1)],
    "inc/advertiser-center.php": [(
        "\t\t\t<?php endforeach; ?>\n\t\t</div>\n\t</section>\n</main>\n",
        "\t\t\t<?php endforeach; ?>\n\t\t</div>\n"
        "\t\t<p class=\"nlac-muted\">לפני שבוחרים מסלול לפרויקט: <a href=\"<?php echo esc_url( home_url( '/marketing/' ) ); ?>\">" + HUN + "</a></p>\n"
        "\t</section>\n</main>\n", 1)],
    "inc/legal-links.php": [(
        "'/new-projects/construction-input-index/' => 'מדד תשומות הבנייה' );\n",
        "'/new-projects/construction-input-index/' => 'מדד תשומות הבנייה',\n"
        "\t\t\t'/marketing/' => '" + TOOL + "' );  // 1.72.601 (HAD-678): the marketing hub, Hebrew pages only\n", 1)],
}
if not FOOTER:
    del PLACES["inc/legal-links.php"]
    print("--no-footer: inc/legal-links.php left out (no footer link)")

HUNKS, ABSENT, LIVE_MD5, PROOF, LEFT_OUT = {}, {}, {}, {}, {}
for rel, hunks in PLACES.items():
    pr = proof(rel)
    raw = open(os.path.join(PLUG, *rel.split("/")), "rb").read()
    txt = raw.decode("utf-8").replace("\r\n", NL)
    if "'/marketing/'" in txt and all(txt.count(new) == 1 for old, new, n in hunks):
        raw_before = None  # the repo copy already holds the hunk (a second run): prove the text before it instead
        before = txt
        for old, new, n in hunks:
            before = before.replace(new, old)
        raw_before = (before.replace(NL, "\r\n") if b"\r\n" in raw else before).encode("utf-8")
    else:
        raw_before = raw
    if pr is None:
        LEFT_OUT[rel] = "no record and no manifest line: the live text cannot be proven"
        continue
    if md5(raw_before) != pr[0]:
        LEFT_OUT[rel] = f"the repo copy {md5(raw_before)[:10]} is not the proven live {pr[0][:10]} ({pr[1]})"
        continue
    t0 = raw_before.decode("utf-8").replace("\r\n", NL)
    for old, new, n in hunks:
        assert t0.count(old) == n, (rel, "anchor", t0.count(old))
        assert "/marketing/" not in t0, (rel, "already links /marketing/")
        assert not re.search("[–—]", new), (rel, "long dash")
    HUNKS[rel], ABSENT[rel], LIVE_MD5[rel], PROOF[rel] = hunks, ["/marketing/"], pr[0], pr[1]
for rel, why in LEFT_OUT.items():
    print("LEFT OUT", rel + ":", why)
assert "inc/developers-page.php" in HUNKS and "inc/advertise-tiers.php" in HUNKS, "a required place could not be proven: " + json.dumps(LEFT_OUT, ensure_ascii=False)
RELS = list(HUNKS)
PHP_RELS = list(HUNKS)
FOOTER_ON = "inc/legal-links.php" in HUNKS

sys.path.insert(0, H)
import ashira_600 as P600  # noqa: E402  the live module list 1.72.599 wrote, unchanged by 1.72.600 and by this release
ML = P600.MAIN_LIST

# ---------------------------------------------------------------- the repo copies (bookkeeping, as 1.72.597 to 600)
for rel, hunks in HUNKS.items():
    p = os.path.join(PLUG, *rel.split("/"))
    raw = open(p, "rb").read(); crlf = b"\r\n" in raw
    t = raw.decode("utf-8").replace("\r\n", NL)
    if all(t.count(new) == 1 for old, new, n in hunks):
        print("repo " + rel + ": already holds the 1.72.601 hunk")
        continue
    assert "/marketing/" not in t, "repo " + rel + " holds a stray /marketing/; restore it first"
    for old, new, n in hunks:
        assert t.count(old) == n, ("repo anchor", rel, t.count(old))
        t = t.replace(old, new)
    io.open(p, "w", encoding="utf-8", newline="").write(t.replace(NL, "\r\n") if crlf else t)
    print("repo " + rel + ": the 1.72.601 hunk applied")

# ---------------------------------------------------------------- ashira_601.py
AP = ["# -*- coding: utf-8 -*-",
      '"""Release 1.72.601 (HAD-678): one link to /marketing/ per place, a hunk on the LIVE text of each file below (the runner\'s PX loop).',
      "A file is hunked only when its live md5 is LIVE_MD5[rel] (PROOF[rel] says why that is the live text); every anchor must be found exactly",
      "once and '/marketing/' must be absent, or the release stops before any write. No hunk on nadlan-config.php (the version only).",
      'Generated by make_deploy601.py."""',
      "RELS = " + repr(RELS), "HUNKS = " + repr(HUNKS), "ABSENT = " + repr(ABSENT), "LIVE_MD5 = " + repr(LIVE_MD5),
      "PROOF = " + repr(PROOF), "FOOTER = " + repr(FOOTER_ON), "MAIN_LIST = " + repr(ML), "", "",
      "def apply(rel, txt):", "    if rel not in HUNKS:", "        raise SystemExit('ashira_601: no hunk on ' + rel)",
      "    for s in ABSENT.get(rel, []):", "        if s in txt:",
      "            raise SystemExit('ashira_601: FATAL: the live %s already holds %r; read it before releasing' % (rel, s))",
      "    for old, new, n in HUNKS[rel]:", "        if new in txt:", "            raise SystemExit('ashira_601: FATAL: the live %s already holds the new text' % rel)",
      "        k = txt.count(old)", "        if k != n:", "            raise SystemExit('ashira_601: FATAL: anchor x%d (want %d) in the live %s: %r' % (k, n, rel, old[:90]))",
      "        txt = txt.replace(old, new)", "    return txt", ""]
open(os.path.join(H, "ashira_601.py"), "w", encoding="utf-8", newline="\n").write("\n".join(AP))

# ---------------------------------------------------------------- deploy601.py from deploy600.py
src = open(os.path.join(H, "deploy600.py"), encoding="utf-8").read()


def one(old, new, what):
    global src
    n = src.count(old)
    assert n == 1, "%s: anchor x%d" % (what, n)
    src = src.replace(old, new)


for a, b in [("1.72.600", "1.72.601"), ("ps600", "ps601"), ("bak600", "bak601"), ("make_deploy600", "make_deploy601"),
             ("deploy-result-600", "deploy-result-601"), ("speed-600", "speed-601"), ("posts-before-600", "posts-before-601"),
             ("deploy-result-599", "deploy-result-600"), ("1.72.599", "1.72.600")]:
    src = src.replace(a, b)
BS = chr(92)
src = re.sub(r"\?t600([a-z]?)=1", "?t601" + BS + "1=1", src)
src = re.sub(r"&t600([a-z]?)=1", "&t601" + BS + "1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(600, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import ashira_600 as PX  # noqa: E402 \(.*$", "import ashira_601 as PX  # noqa: E402 (1.72.601: one /marketing/ link per place, on proven live text)", src, flags=re.M); assert n == 1, n
src, n = re.subn(r'print\("RELEASE 1\.72\.601 LIVE: [^"]*"\)',
                 'print("RELEASE 1.72.601 LIVE: /marketing/ linked from ' + ", ".join(RELS) + '; nlbudget.js v1.1 (the budget lines fold under 768 px)")', src); assert n == 1, n
lines = src.split("\n")
seen = set()
for k, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
    elif l.startswith("NEWFILES = "):
        lines[k] = "NEWFILES = set()  # 1.72.601: nlbudget.js is a swap over the file 1.72.600 wrote; nothing new"; seen.add("NEWFILES")
    elif l.startswith("FILES = ["):
        lines[k] = "FILES = " + repr(FILES); seen.add("FILES")
    elif l.startswith("PHP_RELS = ["):
        lines[k] = "PHP_RELS = " + repr(PHP_RELS) + "  # 1.72.601: every hunked PHP file, restored from .bak601 on rollback (nadlan-config.php always is)"; seen.add("PHP_RELS")
assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
src = "\n".join(lines)

# the module list: the 1.72.599 list, kept by 1.72.600 and 1.72.601 (the global rename above said 1.72.600)
one('raise SystemExit("FATAL: the live module list is not the 1.72.600 one (campaign-brief last)")',
    'raise SystemExit("FATAL: the live module list is not the one 1.72.599 wrote (campaign-brief last)")', "ml fatal")
one("print(\"[plan] nadlan-config.php: the version only; the module list stays as 1.72.600 wrote it ('mortgage-market', 'campaign-brief' last)\")",
    "print(\"[plan] nadlan-config.php: the version only; the module list stays as 1.72.599 wrote it ('mortgage-market', 'campaign-brief' last)\")", "ml print")

# only a file whose live text is proven is hunked: the live md5 must be the proven one
one('        if _cur.get("missing"):\n            raise SystemExit("FATAL live file missing: " + _rel)\n        _live = base64.b64decode(_cur["b64"]);',
    '        if _cur.get("missing"):\n            raise SystemExit("FATAL live file missing: " + _rel)\n'
    '        if md5(base64.b64decode(_cur["b64"])) != PX.LIVE_MD5[_rel]:  # 1.72.601: only a file whose live text is proven is hunked\n'
    '            raise SystemExit(f"FATAL: the live {_rel} is {md5(base64.b64decode(_cur[\'b64\']))[:10]}, not the proven {PX.LIVE_MD5[_rel][:10]} ({PX.PROOF[_rel]}); read it before releasing")\n'
    '        _live = base64.b64decode(_cur["b64"]);', "px md5 gate")

# the bridge: read only, the signed-in advertiser center as the runner's own user sees it
one("\t\t\tif ( ! empty( $b['purge'] ) ) {",
    "\t\t\tif ( ! empty( $b['ac_probe'] ) ) { // 1.72.601: read only. The signed-in advertiser center (inc/advertiser-center.php) as the runner's own user sees it; a visitor gets the theme's gate\n"
    "\t\t\t\t$h = ''; $err = '';\n"
    "\t\t\t\tif ( function_exists( 'nadlan_ac_render_inner' ) ) { try { $h = (string) nadlan_ac_render_inner(); } catch ( \\Throwable $e ) { $err = substr( $e->getMessage(), 0, 200 ); } }\n"
    "\t\t\t\t$out['ac_probe'] = array( 'fn' => function_exists( 'nadlan_ac_render_inner' ) ? 1 : 0, 'bytes' => strlen( $h ), 'err' => $err,\n"
    "\t\t\t\t\t'mkt' => substr_count( $h, 'href=\"' . esc_url( home_url( '/marketing/' ) ) . '\"' ), 'label' => substr_count( $h, '" + HUN + "' ), 'fatal' => substr_count( $h, 'Fatal error' ) );\n"
    "\t\t\t}\n"
    "\t\t\tif ( ! empty( $b['purge'] ) ) {", "bridge ac_probe")

# the pages after the release (verify_pages): the three linked pages render, the public advertiser center is the theme's gate unchanged,
# /marketing/ carries both tools with the new nlbudget.js
ADD = [("/developers/?t601v=1", ['class="nldev-tours"', HUN], ["Fatal error"]),
       ("/advertise/?t601v=1", ['class="nladt__fine"', HUN, 'id="nladt"'], ["Fatal error"]),
       ("/advertiser-center/?t601v=1", ['class="nlrx-gate"'], ["Fatal error"]),
       ("/marketing/?t601m=1", ['data-nli="nlcamp"', 'data-nli="nlbudget"', "tools/nlbudget.js?ver=1.72.601", "tools/nlcamp.js?ver=1.72.601"], ["Fatal error"])]
if FOOTER_ON:
    ADD += [("/mortgage-calculator/?t601f=1", ['class="nlpc-footer-tools"', TOOL], []),
            ("/israel-mortgage-non-residents/?t601f=1", ['class="nlpc-footer-tools"', "Israeli mortgage from abroad"], [TOOL])]
_ca = [l for l in src.split("\n") if l.startswith("    ('/wp-content/plugins/nadlan-config/assets/instruments/tools/nlbudget.js?t601x=1',")]
assert len(_ca) == 1, len(_ca)
src = src.replace(_ca[0], "".join("    (%r, %r, %r),\n" % t for t in ADD) + _ca[0], 1)

VERIFY_MKT = '''MKT_FOOTER = ''' + repr(FOOTER_ON) + '''  # 1.72.601: the footer column carries the link (make_deploy601.py without --no-footer)
MKT_HREF = re.compile(r'href="(?:https://nad-lan\\.co\\.il)?/marketing/"')
MKT_LABEL = "''' + HUN + '''"


def _mkt_split(html):
    body = body_of(html)
    f = body.find('class="nlpc-site-footer"')
    return body, (body[:f] if f > -1 else body), (body[f:] if f > -1 else ""), f > -1


def verify_mkt(tag):
    """1.72.601 (HAD-678): /developers/ and /advertise/ each link /marketing/ exactly once in the page itself (with the words
    "''' + HUN + '''"), and once in the footer when the footer column carries it; one more Hebrew page carries the footer
    link once, an English page never; /marketing/ renders both tools with nlbudget.js at ?ver=1.72.601, no Fatal error."""
    ok = True
    for path in ("/developers/", "/advertise/", "/mortgage-calculator/", "/israel-mortgage-non-residents/", "/marketing/"):
        try:
            s, html = page(path + "?nlv=mk" + tag)
        except Exception as e:
            print(f"[mkt] BAD {path} {e}")
            ok = False
            continue
        body, main, foot, has_f = _mkt_split(html)
        nm, nf = len(MKT_HREF.findall(main)), len(MKT_HREF.findall(foot))
        want_f = 1 if (MKT_FOOTER and path != "/israel-mortgage-non-residents/") else 0
        if path in ("/developers/", "/advertise/"):
            good = nm == 1 and MKT_LABEL in main
        elif path == "/marketing/":
            good = 'data-nli="nlcamp"' in body and 'data-nli="nlbudget"' in body and "tools/nlbudget.js?ver=1.72.601" in html
        else:
            good = True
        good = good and s == 200 and nf == want_f and (has_f or not MKT_FOOTER) and "Fatal error" not in body and "critical error" not in body
        print(f"[mkt] {'OK ' if good else 'BAD'} {s} {path}: /marketing/ links in the page {nm}, in the footer {nf} (want {want_f})")
        ok = ok and good
    return ok


def verify_ac():
    """1.72.601: the signed-in advertiser center (inc/advertiser-center.php, rendered by the bridge as the runner's own user) links
    /marketing/ exactly once and renders without an error. Never raises: a failed probe is a failed check (and a rollback)."""
    try:
        s, r = req("POST", "/wp-json/" + NS + "/v1/apply", body={"token": TOKEN, "ac_probe": 1}, timeout=120)
    except Exception as e:
        print("[ac] BAD probe failed:", str(e)[:120])
        return False
    a = r.get("ac_probe") if isinstance(r, dict) else None
    good = s == 200 and isinstance(a, dict) and a.get("fn") == 1 and a.get("mkt") == 1 and a.get("label") == 1 and not a.get("err") and not a.get("fatal") and a.get("bytes", 0) > 2000
    print(f"[ac] {'OK ' if good else 'BAD'} {s} signed-in advertiser center: {json.dumps(a, ensure_ascii=False)}")
    return bool(good)


def run_checks(tag):'''
one("def run_checks(tag):", VERIFY_MKT, "verify_mkt def")
if not FOOTER_ON:
    pass
one('    if not bad and not verify_nlb():\n        bad = ["nlbudget"]\n    return bad',
    '    if not bad and not verify_nlb():\n        bad = ["nlbudget"]\n'
    '    if not bad and not verify_mkt("ps601m" + tag + str(int(time.time()))):\n        bad = ["marketing-links"]\n'
    + ('    if not bad and not verify_ac():\n        bad = ["advertiser-center"]\n' if "inc/advertiser-center.php" in HUNKS else "")
    + '    return bad', "verify_mkt hook")
if "inc/advertiser-center.php" not in HUNKS:
    one("\t\t\tif ( ! empty( $b['ac_probe'] ) ) {", "\t\t\tif ( false && ! empty( $b['ac_probe'] ) ) {", "ac_probe off")
src, n = re.subn(r'checks="verify_pages \(\+ the v104\.3 lines\)[^"]*"',
                 'checks="verify_pages + served_exact (nlbudget.js at ?ver=1.72.601, byte for byte) + verify_order + verify_home_order + verify_kh + verify_nlb + verify_mkt'
                 + (' + verify_ac' if "inc/advertiser-center.php" in HUNKS else '') + ': OK"', src); assert n == 1, n
assert "ashira_600" not in src and "t600" not in src and "deploy-result-599" not in src, "a 600 marker is left"
assert "599" not in "".join(l for l in src.split("\n") if l.startswith(("PIN = ", "NEWFILES = ", "FILES = ", "PHP_RELS = ", "BAK = ", "NS = ")))
assert src.count('WANT_LIVE = "1.72.600"') == 1 and src.count('BAK = ".bak601"') == 1 and src.count("range(600, 329, -1)") == 1
open(os.path.join(H, "deploy601.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy601.py + ashira_601.py written | t601 markers:", len(re.findall(r"t601[a-z]?=1", src)),
      "| pin:", {k.split("/")[-1]: v[:10] for k, v in PIN.items()}, "| PHP_RELS:", PHP_RELS, "| footer:", FOOTER_ON)
for rel in RELS:
    print("   ", rel, LIVE_MD5[rel][:10], "=", PROOF[rel])
