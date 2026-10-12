# -*- coding: utf-8 -*-
"""Writes deploy444.py from the released deploy443.py: release 1.72.444 = DealSign v2 (inc/deal-sign.php, an existing file now)
+ the Rainbow rail hunk (rail_444.py). Checks: the REST index lists /sg/file; Rainbow keeps its stage and slot box without
Meital's square; the order check no longer expects the square."""
import hashlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rail_444  # noqa: E402,F401
PLUG = os.path.join(os.path.dirname(os.path.dirname(HERE)), "plugins", "nadlan-config")
s = io.open(os.path.join(HERE, "deploy443.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


md5 = hashlib.md5(open(os.path.join(PLUG, "inc", "deal-sign.php"), "rb").read()).hexdigest()
rep("    import sign_443 as PX  # noqa: E402 (1.72.443: DealSign, a new module file; no project-stage hunk)\n",
    "    import rail_444 as PX  # noqa: E402 (1.72.444: DealSign v2 + Meital's square off the Rainbow rail)\n")
rep('php_lint(PHPNEW[_rel], _rel + " (live text, 1.72.443)")', 'php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.444 rail hunk)")')
rep('print("RELEASE 1.72.443 LIVE: DealSign, the signing room of a developer cooperation (HAD-495)")',
    'print("RELEASE 1.72.444 LIVE: DealSign v2 (brokerage agreement alone, the materials tab) + Rainbow rail without the square")')
rep("NEWFILES = set(['inc/deal-sign.php'])\n", "NEWFILES = set([])\n")
rep("PIN = {'inc/deal-sign.php': '", "PIN = {'inc/deal-sign.php': '" + md5 + "'}  # was '")
rep("PHP_RELS = []  # 1.72.443: no project-stage hunk; the only file is the new inc/deal-sign.php (unlinked on rollback)\n",
    "PHP_RELS = ['inc/project-stage.php']  # 1.72.444: the rail hunk, restored from .bak444 on rollback\n")
# the module list already holds deal-sign
rep('    if "\'deal-sign\'" in text:\n        raise SystemExit("FATAL: deal-sign is already in the live module list")\n'
    '    text = text.replace("\'home-v3\', \'pro-card\', \'cta-sheet\' ) as $nadlan_mod", "\'home-v3\', \'pro-card\', \'cta-sheet\', \'deal-sign\' ) as $nadlan_mod")  # 1.72.443\n', "")
rep("text.count(\"'home-v3', 'pro-card', 'cta-sheet' ) as $nadlan_mod\") != 1",
    "text.count(\"'home-v3', 'pro-card', 'cta-sheet', 'deal-sign' ) as $nadlan_mod\") != 1")
# Rainbow: the square leaves; the slot box stays
i = s.index("    (RB, ['class=\"nlps-page\"', 'id=\"nlps\"', 'id=\"nlps-t\"', 'class=\"nlbsq\"', ")
j = s.index("\n", i)
line = s[i:j]
for x in ("'class=\"nlbsq\"', ", "'רישיון תיווך', ", "'פרסומת', "):
    if line.count(x) != 1:
        raise SystemExit("RB row lacks " + x)
    line = line.replace(x, "", 1)
s = s[:i] + line + s[j:]
rep("'id=\"nlps\"', 'class=\"nlbsq\"', 'class=\"nlpf\"'", "'id=\"nlps\"', 'class=\"nlpf\"'")
rows = [("/wp-json/nadlan/v1", ['\/nadlan\/v1\/sg\/file', '\/nadlan\/v1\/sg\/deal'], []),
        ("/projects/rainbow-tel-aviv/", ['id="nlps"', 'class="nlbslot"', 'רוצה להופיע כאן?'], ['class="nlbsq"', 'meital-katzir-portrait'])]
OLD = "# 1.72.443 (DealSign, HAD-495): the signing room routes\n"
rep(OLD, "# 1.72.444 (DealSign v2, HAD-495): the file route; Rainbow without Meital's square\nCHECKS += " + repr(rows) + "\n" + OLD)
for x, y in (("1.72.443", "1.72.444"), (".bak443", ".bak444"), ("PS443", "PS444"), ("ps443", "ps444"), ("deploy443", "deploy444"),
             ("result-443", "result-444"), ("speed-443", "speed-444"), ("posts-before-443", "posts-before-444"), ("make_deploy443", "make_deploy444")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-442.json")', '_prev = os.path.join(QA, "deploy-result-443.json")'),
             ('"FATAL: release 1.72.442 is still in flight', '"FATAL: release 1.72.443 is still in flight'),
             ('WANT_LIVE = "1.72.442"  # the checks name ?ver=1.72.444: this runner is for the release right after 1.72.442',
              'WANT_LIVE = "1.72.443"  # the checks name ?ver=1.72.444: this runner is for the release right after 1.72.443'),
             ("        for n in range(442, 329, -1):", "        for n in range(443, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy444.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy444.py; deal-sign.php md5", md5[:10], "+", len(rows), "check rows")
