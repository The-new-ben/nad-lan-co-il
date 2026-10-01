# -*- coding: utf-8 -*-
"""Writes gen_deploy381.py from gen_deploy380.py (the multi-PHP live-text runner): release 1.72.381 = design v104.10. The WhatsApp
bar's fallback when its column has no free place: the place of LEAST overlap with the stage's actual controls (its resting place
and the controls' edges as candidates), instead of a fixed 30% of the screen height that landed it on whatever was there.
inc/conversion-cta.php on its live text, one anchor. Measured (Kikar, phone, 75 positions through the open tower card): the bar
over a fold heading 7 -> 0, over any stage control 24 -> 3 (he) / 1 (en); Rainbow and DUO 0 -> 0 (the fallback never fires there)."""
import io, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(HERE, "gen_deploy380.py"), encoding="utf-8").read()
FIX = json.load(open(os.path.join(HERE, "barfix381.json"), encoding="utf-8"))


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:90]!r}")
    s = s.replace(old, new)


i0 = s.index("PHP_EDITS = [\n")
i1 = s.index("]\n", s.index("inc/project-stage.php", i0)) + 2
s = s[:i0] + "PHP_EDITS = [\n    [\"inc/conversion-cta.php\", " + json.dumps(FIX["old"]) + ", " + json.dumps(FIX["new"]) + "],\n]\n" + s[i1:]
start = s.index("extra = f'''# 1.72.380 (v104.9)")
end = s.index("'''\n", start) + 4
s = s[:start] + '''extra = f\'\'\'# 1.72.381 (v104.10): the WhatsApp bar's no-free-place fallback is the place of least overlap
CHECKS += [
    ("/projects/hamedina/", ["if(null===best){{var raw=[];", "#nlps-view-cta a,#nlps summary')"], ["if(null===best)best=lo;"]),
    (RB, ["if(null===best){{var raw=[];"], ["if(null===best)best=lo;"]),
]
\'\'\'
''' + s[end:]
rep('print("RELEASE 1.72.380 LIVE: v104.9: the fold headings count as controls for the WhatsApp bar and the accessibility corner (WCAG 2.4.11)")',
    'print("RELEASE 1.72.381 LIVE: v104.10: the WhatsApp bar falls back to the place of least overlap, never a fixed 30% (Kikar 24 -> 3 positions over a control)")')
# deploy380 (the source now) already carries PHP_RELS and the rollback loop with it: the two hunks that added them are replaced by one
# that rewrites the existing PHP_RELS line (placeholders survive the renumbering below)
NL = chr(10)
r0 = s.index("t = must_replace(t, '    for rel in [\"nadlan-config.php\"] + [r for r in FILES if r not in NEWFILES]:'")
r1 = s.index(NL, s.index(NL, r0) + 1) + 1
s = s[:r0] + s[r1:]
b0 = s.index("t = must_replace(t, 'BAK = \".bak380\"', 'BAK = \".bak380\"" + chr(92) + "nPHP_RELS")
b1 = s.index(NL, b0) + 1
s = s[:b0] + ("t = must_replace(t, 'PHP_RELS = [\"inc/conversion-cta.php\", \"inc/project-stage.php\"]  # @@OLDV@@: edited on the live text, restored from @@OLDB@@ on rollback', "
              "'PHP_RELS = [\"inc/conversion-cta.php\"]  # @@NEWV@@: edited on the live text, restored from @@NEWB@@ on rollback')" + NL) + s[b1:]
rep('" (live text + #nlps summary)"', '" (live text + the least-overlap fallback)"')
rep("""; PHP on the live text: {', '.join(LIVEP)} (#nlps summary)")""", """; PHP on the live text: {', '.join(LIVEP)} (the bar's least-overlap fallback)")""")
for a, b in (("1.72.380", "1.72.381"), (".bak380", ".bak381"), ("PS380", "PS381"), ("ps380", "ps381"), ("deploy380", "deploy381"),
             ("result-380", "result-381"), ("speed-380", "speed-381"), ("bridge380", "bridge381"),
             ("1.72.379", "1.72.380"), (".bak379", ".bak380"), ("PS379", "PS380"), ("ps379", "ps380"), ("deploy379", "deploy380"),
             ("range(379", "range(380"), (r"1\\.72\\.379", r"1\\.72\\.380")):
    s = s.replace(a, b)
s = s.replace("@@OLDV@@", "1.72.380").replace("@@OLDB@@", ".bak380").replace("@@NEWV@@", "1.72.381").replace("@@NEWB@@", ".bak381")
io.open(os.path.join(HERE, "gen_deploy381.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote gen_deploy381.py")
