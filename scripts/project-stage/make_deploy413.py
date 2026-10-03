# -*- coding: utf-8 -*-
"""Writes deploy413.py from the released and verified deploy412.py: release 1.72.413 = urban's HAD-393 focus-only fix
(commit f8947090, Maya ACCEPT 6/6 at 09:29 UTC; urban defers the run to main; Ben's approval relayed by Maya 09:20 UTC).
  - inc/smart-form.php: sf_413.py on the LIVE text (four anchors, each once), php -l, .bak413.
  - nadlan-config.php: the version bump on the live text.
No asset, no post, no new file. Every inherited check stays."""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(HERE, "deploy412.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:100]!r}")
    s = s.replace(old, new)


rep("PIN = {'assets/project-stage/world/world.css': 'bbd39ef852d340c0011ba20d75afc0fa'}\nNEWFILES = set([])\nFILES = ['assets/project-stage/world/world.css']\n",
    "PIN = {}\nNEWFILES = set([])\nFILES = []\n")
rep("    import cc_r4 as PX  # noqa: E402 (1.72.412: the focus reveal)\n", "    import sf_413 as PX  # noqa: E402 (1.72.413: HAD-393, the smart form's first-render focus)\n")
rep('    for _rel in ("inc/conversion-cta.php",):\n', '    for _rel in ("inc/smart-form.php",):\n')
rep('(live text + the 1.72.412 focus reveal)', '(live text + the 1.72.413 smart-form focus fix)')
rep('PHP_RELS = ["inc/conversion-cta.php"]  # 1.72.412: HAD-390 R4 hunk on the live text (v104.34), restored from .bak412 on rollback',
    'PHP_RELS = ["inc/smart-form.php"]  # 1.72.413: HAD-393 hunks on the live text (urban f8947090), restored from .bak413 on rollback')
rep('print("RELEASE 1.72.412 LIVE: HAD-390 R4: on a phone the 3D, the tower step and the floor slider share the free screen; keyboard focus never under the header or the band")',
    'print("RELEASE 1.72.413 LIVE: HAD-393: the smart form takes no focus on its first render, so the page no longer jumps to the form on load")')
rep('''    ("/projects/rainbow-tel-aviv/", ["HAD-390 R4", 'class="nlps-page"'], []),
]
''', '''    ("/projects/rainbow-tel-aviv/", ["HAD-390 R4", 'class="nlps-page"'], []),
]
# 1.72.413 (HAD-393, urban f8947090): no focus on the smart form's first render
CHECKS += [
    ("/urban-renewal/", ['acted=false', 'if(acted)input.focus({preventScroll:true});', 'input.focus({preventScroll:true});return}'], ['if(input){input.focus();if(answers[s.k])']),
    ("/buying-apartment/", ['acted=false', 'if(acted)input.focus({preventScroll:true});'], ['if(input){input.focus();if(answers[s.k])']),
    ("/sell-by-auction/", ['acted=false', 'if(acted)input.focus({preventScroll:true});'], ['if(input){input.focus();if(answers[s.k])']),
]
''')
for x, y in (("1.72.412", "1.72.413"), (".bak412", ".bak413"), ("PS412", "PS413"), ("ps412", "ps413"), ("deploy412", "deploy413"),
             ("result-412", "result-413"), ("speed-412", "speed-413"), ("posts-before-412", "posts-before-413"), ("make_deploy412", "make_deploy413")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-411.json")', '_prev = os.path.join(QA, "deploy-result-412.json")'),
             ('"FATAL: release 1.72.411 is still in flight', '"FATAL: release 1.72.412 is still in flight'),
             ('WANT_LIVE = "1.72.411"  # the checks name ?ver=1.72.413: this runner is for the release right after 1.72.411',
              'WANT_LIVE = "1.72.412"  # the checks name ?ver=1.72.413: this runner is for the release right after 1.72.412'),
             ("        for n in range(411, 329, -1):", "        for n in range(412, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy413.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy413.py")
