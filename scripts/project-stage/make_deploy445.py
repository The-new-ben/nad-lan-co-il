# -*- coding: utf-8 -*-
"""Writes deploy445.py from the released deploy444.py: release 1.72.445 = the Instruments engine (HAD-527): new files
inc/instruments.php and assets/instruments/*, 'instruments' added to the module list. served_exact proves every asset byte for
byte; the pages get the tools by content edits after the release."""
import hashlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tools_445  # noqa: E402,F401
PLUG = os.path.join(os.path.dirname(os.path.dirname(HERE)), "plugins", "nadlan-config")
NEW = ["inc/instruments.php", "assets/instruments/core.css", "assets/instruments/core.js", "assets/instruments/tools/indexation.js",
       "assets/instruments/tools/delay.js", "assets/instruments/data/cbs-200010.json", "assets/instruments/data/cbs-120010.json"]
s = io.open(os.path.join(HERE, "deploy444.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


pin = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in NEW}
rep("    import rail_444 as PX  # noqa: E402 (1.72.444: DealSign v2 + Meital's square off the Rainbow rail)\n",
    "    import tools_445 as PX  # noqa: E402 (1.72.445: the Instruments engine, new files only)\n")
rep('php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.444 rail hunk)")', 'php_lint(PHPNEW[_rel], _rel + " (live text, 1.72.445)")')
rep('print("RELEASE 1.72.444 LIVE: DealSign v2 (brokerage agreement alone, the materials tab) + Rainbow rail without the square")',
    'print("RELEASE 1.72.445 LIVE: NadLan Instruments, the tools engine (indexation + delay)")')
rep("NEWFILES = set([])\nFILES = ['inc/deal-sign.php']\n", "NEWFILES = set(" + repr(NEW) + ")\nFILES = " + repr(NEW) + "\n")
i = s.index("PIN = {'inc/deal-sign.php': '"); j = s.index("\n", i)
s = s[:i] + "PIN = " + repr(pin) + s[j:]
rep("PHP_RELS = ['inc/project-stage.php']  # 1.72.444: the rail hunk, restored from .bak444 on rollback\n",
    "PHP_RELS = []  # 1.72.445: no hunk; the new files are unlinked on rollback\n")
rep('        raise SystemExit("FATAL: the live module list is not the 1.72.408 one")\n',
    '        raise SystemExit("FATAL: the live module list is not the 1.72.408 one")\n'
    '    if "\'instruments\'" in text:\n        raise SystemExit("FATAL: instruments is already in the live module list")\n'
    '    text = text.replace("\'cta-sheet\', \'deal-sign\' ) as $nadlan_mod", "\'cta-sheet\', \'deal-sign\', \'instruments\' ) as $nadlan_mod")  # 1.72.445\n')
rows = [("/new-projects/construction-input-index/", ['<h1'], ['nadlan-nli-indexation']), ("/new-projects/contractor-delay-compensation/", ['<h1'], ['nadlan-nli-delay'])]
OLD = "# 1.72.444 (DealSign v2, HAD-495): the file route; Rainbow without Meital's square\n"
rep(OLD, "# 1.72.445 (Instruments, HAD-527): the engine ships; no page carries a tool yet\nCHECKS += " + repr(rows) + "\n" + OLD)
for x, y in (("1.72.444", "1.72.445"), (".bak444", ".bak445"), ("PS444", "PS445"), ("ps444", "ps445"), ("deploy444", "deploy445"),
             ("result-444", "result-445"), ("speed-444", "speed-445"), ("posts-before-444", "posts-before-445"), ("make_deploy444", "make_deploy445")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-443.json")', '_prev = os.path.join(QA, "deploy-result-444.json")'),
             ('"FATAL: release 1.72.443 is still in flight', '"FATAL: release 1.72.444 is still in flight'),
             ('WANT_LIVE = "1.72.443"  # the checks name ?ver=1.72.445: this runner is for the release right after 1.72.443',
              'WANT_LIVE = "1.72.444"  # the checks name ?ver=1.72.445: this runner is for the release right after 1.72.444'),
             ("        for n in range(443, 329, -1):", "        for n in range(444, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy445.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy445.py;", len(NEW), "new files")
