# -*- coding: utf-8 -*-
"""Writes deploy462.py from the released deploy461.py: 1.72.462 (HAD-543): no project lists itself among the nearby comps (inc/project-experience.php, a hunk on the live text, ashira_462.py). Old docstring of 461 follows:
: 1.72.461 (Ben 15.10.2026): (1) the health check tells the truth about
Morning: the old probe read the API base URL, which answers 404 by design, so every check and agent said "Morning is broken";
now it reports whether Morning answers and how many Morning payment methods the checkout offers (inc/health.php); (2) the
soil content guard is removed (Ben: no content filters); the project pages stay clean at the source (cleaned in the CMS)."""
import hashlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import names_457 as _  # noqa: E402,F401  (no hunk: same module shape)
PLUG = os.path.join(os.path.dirname(os.path.dirname(HERE)), "plugins", "nadlan-config")
FILES = []
NEW = []
s = io.open(os.path.join(HERE, "deploy461.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


pin = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
rep('php_lint(PHPNEW[_rel], _rel + " (live text, 1.72.461)")', 'php_lint(PHPNEW[_rel], _rel + " (live text, 1.72.462)")')
rep('    import names_457 as PX  # noqa: E402 (1.72.461: the soil page without names)', '    import ashira_462 as PX  # noqa: E402 (1.72.462: no project is its own comp)')
rep('print("RELEASE 1.72.461 LIVE: the health check tells the truth about Morning; no content guard")', 'print("RELEASE 1.72.462 LIVE: no project lists itself among the nearby comps")')
i = s.index("NEWFILES = set("); j = s.index("\n", s.index("\nFILES = [", i) + 1)
s = s[:i] + "NEWFILES = set(" + repr(NEW) + ")\nFILES = " + repr(FILES) + "\n" + s[j:]
i = s.index("PIN = {"); j = s.index("\n", i)
s = s[:i] + "PIN = " + repr(pin) + s[j:]
for x, y in (("1.72.461", "1.72.462"), (".bak461", ".bak462"), ("PS461", "PS462"), ("ps461", "ps462"), ("deploy461", "deploy462"),
             ("result-461", "result-462"), ("speed-461", "speed-462"), ("posts-before-461", "posts-before-462"), ("make_deploy461", "make_deploy462")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-460.json")', '_prev = os.path.join(QA, "deploy-result-461.json")'),
             ('"FATAL: release 1.72.460 is still in flight', '"FATAL: release 1.72.461 is still in flight'),
             ('WANT_LIVE = "1.72.460"  # the checks name ?ver=1.72.462: this runner is for the release right after 1.72.460',
              'WANT_LIVE = "1.72.461"  # the checks name ?ver=1.72.462: this runner is for the release right after 1.72.461'),
             ("        for n in range(460, 329, -1):", "        for n in range(461, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy462.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy462.py")
