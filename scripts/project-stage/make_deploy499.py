# -*- coding: utf-8 -*-
"""make deploy499.py from deploy498.py: 1.72.499 (HAD-592, the page loop, Greece wave 1).
  - assets/instruments/tools/greece.js (NEW): grbuy, grgv, gryield, one file for the family; data/greece.json (NEW) from the facts pack.
  - assets/instruments/core.css: a long select no longer pushes the form past a 390 px phone.
  - inc/instruments.php: the Greece tools in the registry with their plain summaries; a family shares one script file.
  - inc/breadcrumbs.php: [nadlan_crumbs hub="..;.."] takes several levels (Global > Greece > page).
  - inc/global-worlds.php: one H1 on /global/ routes (the fallback header's site name becomes a paragraph), the world page lists its
    published guides, /global/ and the world pages join the page sitemap, and the Greece facts are corrected (2026 rent brackets,
    the island rule of the golden visa, the proposed 15.45% transfer tax, the treaty line).
No hunk."""
import hashlib, os, re
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
FILES = ["assets/instruments/tools/greece.js", "assets/instruments/data/greece.json", "assets/instruments/core.css", "inc/instruments.php",
         "inc/breadcrumbs.php", "inc/global-worlds.php"]
NEW = ["assets/instruments/tools/greece.js", "assets/instruments/data/greece.json"]
PIN = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
src = open(os.path.join(H, "deploy498.py"), encoding="utf-8").read()
lines = src.split("\n")
for i, l in enumerate(lines):
    if l.startswith("PIN = {"): lines[i] = "PIN = " + repr(PIN)
    elif l.startswith("NEWFILES = set("): lines[i] = "NEWFILES = set(" + repr(NEW) + ")"
    elif l.startswith("FILES = ["): lines[i] = "FILES = " + repr(FILES)
    elif l.startswith("PHP_RELS = ["): lines[i] = "PHP_RELS = []  # 1.72.499: no hunk; the files come back from .bak on rollback, the new ones are removed"
src = "\n".join(lines)
for a, b in [("1.72.498", "1.72.499"), ("ps498", "ps499"), ("bak498", "bak499"), ("make_deploy498", "make_deploy499"),
             ("deploy-result-498", "deploy-result-499"), ("speed-498", "speed-499"), ("posts-before-498", "posts-before-499"),
             ("ashira_498", "ashira_499"), ("deploy-result-497", "deploy-result-498"), ("1.72.497", "1.72.498")]:
    src = src.replace(a, b)
src = re.sub(r"\?t498([a-z]?)=1", r"?t499\1=1", src)
src = re.sub(r"&t498([a-z]?)=1", r"&t499\1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(498, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import ashira_499 as PX  # noqa: E402 \([^)]*\)", "import ashira_499 as PX  # noqa: E402 (1.72.499: no hunk)", src); assert n == 1, n
old = "    ('/wp-content/plugins/nadlan-config/assets/instruments/tools/dira.js?t499d=1',"
assert src.count(old) == 1, src.count(old)
NO_LOGO_H1 = '<h1><a href="https://nad-lan.co.il/">'
ADD = [
    ("/wp-content/plugins/nadlan-config/assets/instruments/tools/greece.js?t499g=1", ["NLGR", "register('grbuy'", "register('grgv'", "register('gryield'"], []),
    ("/wp-content/plugins/nadlan-config/assets/instruments/data/greece.json?t499j=1", ['"key":"greece"', '"regions"', "athens-center"], []),
    ("/wp-content/plugins/nadlan-config/assets/instruments/core.css?t499c=1", [".nli__in select{min-width:0", ".nli__pre{"], []),
    ("/global/greece/?t499w=1", ['class="nlgw-sitename"', "25% עד 24 אלף", "15.45%"], [NO_LOGO_H1]),
    ("/global/?t499h=1", ['class="nlgw-sitename"'], [NO_LOGO_H1]),
    ("/global/cyprus/?t499y=1", ['class="nlgw-sitename"'], [NO_LOGO_H1]),
]
src = src.replace(old, "".join("    (%r, %r, %r),\n" % t for t in ADD) + old)
src = re.sub(r'print\("RELEASE 1\.72\.499 LIVE: [^"]*"\)', 'print("RELEASE 1.72.499 LIVE: the Greece tools, one H1 and the sitemap on /global/, multi-level page trails")', src)
open(os.path.join(H, "deploy499.py"), "w", encoding="utf-8", newline="\n").write(src)
open(os.path.join(H, "ashira_499.py"), "w", encoding="utf-8", newline="\n").write(
    '# -*- coding: utf-8 -*-\n"""Release 1.72.499 (HAD-592): the Greece tools, one H1 and the sitemap on /global/, multi-level page trails. No hunk."""\n'
    'RELS = []\n\n\ndef apply(rel, txt):\n    return txt\n')
print("deploy499.py + ashira_499.py written")
