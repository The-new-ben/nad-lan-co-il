# -*- coding: utf-8 -*-
"""Writes gen_deploy400.py from gen_deploy399.py: release 1.72.400 = the language dictionary learns Kikar's name (design v104.27).
Since the data step of 2.10.2026 (Kikar 65,000/m2 in the neighbours' comparison table) the language pages of DUO and Rainbow printed
"מגדלי כיכר המדינה, תל אביב" in Hebrew in that table (tools/lang_pages_check.py: 12 pages). i18n/lang-pages.json gains the name in
the four languages, the same names Kikar's own language pages use (Arabic titles in English, owner 28.9). One file; the 1.72.399
PHP block is removed (that hunk is live)."""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(HERE, "gen_deploy399.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:90]!r}")
    s = s.replace(old, new)


a = s.index("# ---- 1.72.399: the finance line skips world pages")
b = s.index("# PHP_REL is used by rollback() (defined above main): give it a module-level name early\n")
s = s[:a] + s[b:]
rep('FILES = [] + NEWF', 'FILES = ["i18n/lang-pages.json"] + NEWF')
start = s.index("extra = f'''# 1.72.399 (Kikar V8 step 2a")
end = s.index("'''\n", start) + 4
s = s[:start] + '''extra = f\'\'\'# 1.72.400 (v104.27): the language dictionary learns Kikar's name (the neighbours' comparison table)
CHECKS += [
    ("{ASSET}i18n/lang-pages.json?ver={V}", ['"מגדלי כיכר המדינה, תל אביב"', '"Башни Кикар ха-Медина, Тель-Авив"'], []),
    # the table's link text only: the page also carries the dictionary itself (Hebrew keys) in a script for the browser
    ("/projects/duo-tel-aviv-en/", ['hamedina/">Kikar Hamedina Towers, Tel Aviv</a>'], ['hamedina/">מגדלי כיכר המדינה, תל אביב</a>']),
    ("/projects/duo-tel-aviv-ru/", ['hamedina/">Башни Кикар ха-Медина, Тель-Авив</a>'], ['hamedina/">מגדלי כיכר המדינה, תל אביב</a>']),
    ("/projects/duo-tel-aviv/", ["/projects/hamedina/"], []),
]
\'\'\'
''' + s[end:]
rep('''print("RELEASE 1.72.399 LIVE: Kikar V8 step 2a: the generic ~90 m2 finance line skips world pages")''',
    '''print("RELEASE 1.72.400 LIVE: the language dictionary learns Kikar's name (the neighbours' comparison table)")''')
for x, y in (("1.72.399", "1.72.400"), (".bak399", ".bak400"), ("PS399", "PS400"), ("ps399", "ps400"), ("deploy399", "deploy400"),
             ("result-399", "result-400"), ("speed-399", "speed-400"), ("bridge399", "bridge400"), ("posts-before-399", "posts-before-400"),
             ("1.72.398", "1.72.399"), (".bak398", ".bak399"), ("PS398", "PS399"), ("ps398", "ps399"), ("deploy398", "deploy399"),
             ("range(398", "range(399"), (r"1\\.72\\.398", r"1\\.72\\.399")):
    s = s.replace(x, y)
i = s.index(r't = must_replace(t, "\t\t\t$kh_write = array(')
j = s.index("\n", i) + 1
s = s[:i] + 't = must_replace(t, "\\t\\t\\t$kh_write = array(); // 1.72.399 writes no post", "\\t\\t\\t$kh_write = array(); // 1.72.400 writes no post")\n' + s[j:]
io.open(os.path.join(HERE, "gen_deploy400.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote gen_deploy400.py (i18n/lang-pages.json only)")
