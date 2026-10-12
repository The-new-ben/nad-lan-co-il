# -*- coding: utf-8 -*-
"""Writes deploy443.py from the released deploy442.py: release 1.72.443 = DealSign (HAD-495): the new module file
inc/deal-sign.php, loaded by adding 'deal-sign' to the module list in nadlan-config.php. Checks: the REST namespace lists the
four public routes and the two admin routes; nothing else moved."""
import hashlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sign_443  # noqa: E402,F401
PLUG = os.path.join(os.path.dirname(os.path.dirname(HERE)), "plugins", "nadlan-config")
s = io.open(os.path.join(HERE, "deploy442.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


md5 = hashlib.md5(open(os.path.join(PLUG, "inc", "deal-sign.php"), "rb").read()).hexdigest()
rep("    import data_442 as PX  # noqa: E402 (1.72.442: data only, the Sde Dov components in four languages)\n",
    "    import sign_443 as PX  # noqa: E402 (1.72.443: DealSign, a new module file; no project-stage hunk)\n")
rep('php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.442 data hunk)")',
    'php_lint(PHPNEW[_rel], _rel + " (live text, 1.72.443)")')
rep('print("RELEASE 1.72.442 LIVE: data only, the Sde Dov price list and map in four languages")',
    'print("RELEASE 1.72.443 LIVE: DealSign, the signing room of a developer cooperation (HAD-495)")')
rep("NEWFILES = set([])\nFILES = []\n", "NEWFILES = set(['inc/deal-sign.php'])\nFILES = ['inc/deal-sign.php']\n")
rep("PIN = {}\n", "PIN = {'inc/deal-sign.php': '" + md5 + "'}\n")
rep('        raise SystemExit("FATAL: the live module list is not the 1.72.408 one")\n',
    '        raise SystemExit("FATAL: the live module list is not the 1.72.408 one")\n'
    '    if "\'deal-sign\'" in text:\n        raise SystemExit("FATAL: deal-sign is already in the live module list")\n'
    '    text = text.replace("\'home-v3\', \'pro-card\', \'cta-sheet\' ) as $nadlan_mod", "\'home-v3\', \'pro-card\', \'cta-sheet\', \'deal-sign\' ) as $nadlan_mod")  # 1.72.443\n')
rep("PHP_RELS = ['inc/project-stage.php']  # 1.72.442: HAD-396, the package's 16 files on the live text, restored from .bak442 on rollback\n",
    "PHP_RELS = []  # 1.72.443: no project-stage hunk; the only file is the new inc/deal-sign.php (unlinked on rollback)\n")
rep('    for rel in FILES:\n        path = "/wp-content/plugins/nadlan-config/" + rel + "?ver=1.72.442&nlv=" + tag\n',
    '    for rel in [r for r in FILES if not r.endswith(".php")]:  # 1.72.443: a PHP module is never served as a file; the REST row proves it loads\n'
    '        path = "/wp-content/plugins/nadlan-config/" + rel + "?ver=1.72.442&nlv=" + tag\n')
rows = [("/wp-json/nadlan/v1", ['\/nadlan\/v1\/sg\/deal', '\/nadlan\/v1\/sg\/sign', '\/nadlan\/v1\/sg\/reg', '\/nadlan\/v1\/sg\/rev', '\/nadlan\/v1\/sg\/broker'], [])]
OLD = "# 1.72.442 (data only): the Sde Dov components in four languages\n"
rep(OLD, "# 1.72.443 (DealSign, HAD-495): the signing room routes\nCHECKS += " + repr(rows) + "\n" + OLD)
for x, y in (("1.72.442", "1.72.443"), (".bak442", ".bak443"), ("PS442", "PS443"), ("ps442", "ps443"), ("deploy442", "deploy443"),
             ("result-442", "result-443"), ("speed-442", "speed-443"), ("posts-before-442", "posts-before-443"), ("make_deploy442", "make_deploy443")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-441.json")', '_prev = os.path.join(QA, "deploy-result-442.json")'),
             ('"FATAL: release 1.72.441 is still in flight', '"FATAL: release 1.72.442 is still in flight'),
             ('WANT_LIVE = "1.72.441"  # the checks name ?ver=1.72.443: this runner is for the release right after 1.72.441',
              'WANT_LIVE = "1.72.442"  # the checks name ?ver=1.72.443: this runner is for the release right after 1.72.442'),
             ("        for n in range(441, 329, -1):", "        for n in range(442, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy443.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy443.py; deal-sign.php md5", md5[:10], "+", len(rows), "check row")
