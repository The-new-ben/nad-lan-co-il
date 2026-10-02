# -*- coding: utf-8 -*-
"""Writes gen_deploy398.py from gen_deploy397.py: release 1.72.398 = the HAD-391 follow-up on Rainbow. rainbow/stage.js loaded
stage.css and city.json WITHOUT the module's ?ver (max-age one year), the same stale-cache trap the owner's phone hit on Kikar.
Both now carry the module's ?ver. One file; the 1.72.397 PHP block is removed (those hunks are live)."""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(HERE, "gen_deploy397.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:90]!r}")
    s = s.replace(old, new)


a = s.index("# ---- 1.72.397: the ConsultBand hunks on the live text of two PHP files (HAD-390) ----")
b = s.index("# PHP_REL is used by rollback() (defined above main): give it a module-level name early\n")
s = s[:a] + s[b:]
rep('FILES = ["assets/project-stage/world/example.js"] + NEWF', 'FILES = ["assets/project-stage/rainbow/stage.js"] + NEWF')
start = s.index("extra = f'''# 1.72.397 (HAD-390 ConsultBand R2 + R3 + R3b)")
end = s.index("'''\n", start) + 4
s = s[:start] + '''extra = f\'\'\'# 1.72.398 (HAD-391 follow-up): Rainbow's stage.css and city.json carry the module's ?ver
CHECKS += [
    ("{ASSET}assets/project-stage/rainbow/stage.js?ver={V}", ["new URL('./stage.css' + new URL(import.meta.url).search, import.meta.url)", "new URL('./city.json' + new URL(import.meta.url).search, import.meta.url)"], ["l.href = new URL('./stage.css', import.meta.url).href;"]),
]
\'\'\'
''' + s[end:]
rep('''print("RELEASE 1.72.397 LIVE: HAD-390 ConsultBand (R2 + R3 + R3b): the consult bar and the accessibility button in a band of their own on world pages")''',
    '''print("RELEASE 1.72.398 LIVE: HAD-391 follow-up: Rainbow's stage.css and city.json carry the module's ?ver")''')
for x, y in (("1.72.397", "1.72.398"), (".bak397", ".bak398"), ("PS397", "PS398"), ("ps397", "ps398"), ("deploy397", "deploy398"),
             ("result-397", "result-398"), ("speed-397", "speed-398"), ("bridge397", "bridge398"), ("posts-before-397", "posts-before-398"),
             ("1.72.396", "1.72.397"), (".bak396", ".bak397"), ("PS396", "PS397"), ("ps396", "ps397"), ("deploy396", "deploy397"),
             ("range(396", "range(397"), (r"1\\.72\\.396", r"1\\.72\\.397")):
    s = s.replace(x, y)
i = s.index(r't = must_replace(t, "\t\t\t$kh_write = array(')
j = s.index("\n", i) + 1
s = s[:i] + 't = must_replace(t, "\\t\\t\\t$kh_write = array(); // 1.72.397 writes no post", "\\t\\t\\t$kh_write = array(); // 1.72.398 writes no post")\n' + s[j:]
io.open(os.path.join(HERE, "gen_deploy398.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote gen_deploy398.py (rainbow/stage.js only)")
