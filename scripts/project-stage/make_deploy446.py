# -*- coding: utf-8 -*-
"""Writes deploy446.py from deploy445.py: 1.72.446 = inc/instruments.php with asset URLs from the plugin root (live fault of
1.72.445: 404 on the tool assets). Checks: both tool pages print the assets under /plugins/nadlan-config/assets/instruments/."""
import hashlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fix_446  # noqa: E402,F401
PLUG = os.path.join(os.path.dirname(os.path.dirname(HERE)), "plugins", "nadlan-config")
s = io.open(os.path.join(HERE, "deploy445.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


md5 = hashlib.md5(open(os.path.join(PLUG, "inc", "instruments.php"), "rb").read()).hexdigest()
rep("    import tools_445 as PX  # noqa: E402 (1.72.445: the Instruments engine, new files only)\n",
    "    import fix_446 as PX  # noqa: E402 (1.72.446: the Instruments asset URLs)\n")
rep('php_lint(PHPNEW[_rel], _rel + " (live text, 1.72.445)")', 'php_lint(PHPNEW[_rel], _rel + " (live text, 1.72.446)")')
rep('print("RELEASE 1.72.445 LIVE: NadLan Instruments, the tools engine (indexation + delay)")', 'print("RELEASE 1.72.446 LIVE: the Instruments asset URLs fixed")')
i = s.index("NEWFILES = set(["); j = s.index("\n", s.index("\nFILES = [", i) + 1)
s = s[:i] + "NEWFILES = set([])\nFILES = ['inc/instruments.php']\n" + s[j:]
i = s.index("PIN = {"); j = s.index("\n", i)
s = s[:i] + "PIN = {'inc/instruments.php': '" + md5 + "'}" + s[j:]
rep('    if "\'instruments\'" in text:\n        raise SystemExit("FATAL: instruments is already in the live module list")\n'
    '    text = text.replace("\'cta-sheet\', \'deal-sign\' ) as $nadlan_mod", "\'cta-sheet\', \'deal-sign\', \'instruments\' ) as $nadlan_mod")  # 1.72.445\n', "")
rep("text.count(\"'home-v3', 'pro-card', 'cta-sheet', 'deal-sign' ) as $nadlan_mod\") != 1",
    "text.count(\"'home-v3', 'pro-card', 'cta-sheet', 'deal-sign', 'instruments' ) as $nadlan_mod\") != 1")
rep("CHECKS += [('/new-projects/construction-input-index/', ['<h1'], ['nadlan-nli-indexation']), ('/new-projects/contractor-delay-compensation/', ['<h1'], ['nadlan-nli-delay'])]\n",
    "CHECKS += [('/new-projects/construction-input-index/', ['data-nli=\"indexation\"', '/plugins/nadlan-config/assets/instruments/tools/indexation.js?ver=1.72.446', '/plugins/nadlan-config/assets/instruments/data/cbs-200010.json?ver=1.72.446'], ['/inc/assets/instruments/']), "
    "('/new-projects/contractor-delay-compensation/', ['data-nli=\"delay\"', '/plugins/nadlan-config/assets/instruments/tools/delay.js?ver=1.72.446'], ['/inc/assets/instruments/'])]\n")
for x, y in (("1.72.445", "1.72.446"), (".bak445", ".bak446"), ("PS445", "PS446"), ("ps445", "ps446"), ("deploy445", "deploy446"),
             ("result-445", "result-446"), ("speed-445", "speed-446"), ("posts-before-445", "posts-before-446"), ("make_deploy445", "make_deploy446")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-444.json")', '_prev = os.path.join(QA, "deploy-result-445.json")'),
             ('"FATAL: release 1.72.444 is still in flight', '"FATAL: release 1.72.445 is still in flight'),
             ('WANT_LIVE = "1.72.444"  # the checks name ?ver=1.72.446: this runner is for the release right after 1.72.444',
              'WANT_LIVE = "1.72.445"  # the checks name ?ver=1.72.446: this runner is for the release right after 1.72.445'),
             ("        for n in range(444, 329, -1):", "        for n in range(445, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy446.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy446.py")
