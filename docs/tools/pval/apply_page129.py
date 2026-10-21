# -*- coding: utf-8 -*-
"""HAD-575 / Kikar tools #1 (Ben 15.10 + 21.10.2026): /property-value-estimator/ (page 129) gets the Instruments tool "pval" in
place of the old inline calculator (section.calc-shell + its script: the price per m2 typed by hand). Every field of the old
widget lives on in the tool's "per m2" way. The order after the hero: a one-paragraph answer with official numbers, the tool, a
worked market example (one contextual link to /projects/hamedina/), then the guide as it is. Guard: the live content must equal
the saved copy (md5). Backup before, read-back after.   python docs/tools/pval/apply_page129.py [--dry]"""
import hashlib, io, os, re, sys, time
REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "pval129"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]
H = os.path.dirname(os.path.abspath(__file__))
s, b, _ = req("GET", "/wp-json/wp/v2/pages/129?context=edit&_fields=content,modified")
raw = b["content"]["raw"]
want_p = os.path.join(H, "page129-before.html")
if not os.path.exists(want_p):
    io.open(want_p, "w", encoding="utf-8", newline="").write(raw); print("saved page129-before.html")
want = io.open(want_p, encoding="utf-8", newline="").read()
if hashlib.md5(raw.encode()).hexdigest() != hashlib.md5(want.encode()).hexdigest():
    raise SystemExit("FATAL: page 129 changed since it was saved (%s); look before writing" % b["modified"])
a = raw.index('<section class="calc-shell wrap"')
depth, z = 0, None
for m in re.finditer(r"<section\b|</section>", raw[a:]):
    depth += 1 if m.group(0).startswith("<section") else -1
    if depth == 0:
        z = a + m.end(); break
s0 = raw.index('<script id="nadlan-property-value-estimator-js-20260528">')
s1 = raw.index("</script>", s0) + len("</script>")
assert z and a < z < s0 < s1 and raw[a:z].count('id="npv-') == raw.count('id="npv-') >= 10
NEW = ('<section class="wrap" aria-label="מחשבון שווי דירה">\n'
       '<p><strong>כמה שווה דירה:</strong> לפי העסקאות שנסגרו ברבעון הראשון של 2026 (נתוני רשות המסים), החציון של דירת 4 חדרים בתל אביב הוא '
       '5,229,800 ₪, ובשכונת הצפון החדש סביבת כיכר המדינה 6,835,800 ₪. בחיפה אותה דירה היא 1,597,500 ₪. המחשבון מתחיל מהחציון של השכונה '
       'שלכם ומספר החדרים, מוסיף את ההתאמות לדירה עצמה, ובודק מחיר מבוקש. אפשר לעבור גם לחישוב לפי מחיר למ״ר.</p>\n'
       '[nadlan_tool id="pval"]\n'
       '<p><strong>דוגמה מהשוק:</strong> בשכונה של <a href="/projects/hamedina/">כיכר המדינה בתל אביב</a> החציון של דירת 5 חדרים הוא 8,455,800 ₪, '
       'ובמגדלים החדשים בכיכר עצמה פורסמו עסקאות של 9.58 עד 10.63 מיליון ₪. דירה חדשה, קומה גבוהה ונוף פתוח מכניסים בשדות ההתאמה.</p>\n</section>')
out = raw[:a] + NEW + raw[z:s0] + raw[s1:]
assert out.count("[nadlan_tool") == 1 and 'id="npv-' not in out
print("[plan] page 129: %d -> %d chars; the old calculator (%d) and its script (%d) out" % (len(raw), len(out), z - a, s1 - s0))
if "--dry" in sys.argv:
    io.open(os.path.join(H, "page129-after.html"), "w", encoding="utf-8", newline="").write(out); raise SystemExit(0)
bk = os.path.join(REPO, "docs", "qa", "had-527", "page-backup"); os.makedirs(bk, exist_ok=True)
ts = time.strftime("%Y%m%d-%H%M%S")
io.open(os.path.join(bk, "129-%s.html" % ts), "w", encoding="utf-8", newline="").write(raw)
req("POST", "/wp-json/wp/v2/pages/129", {"content": out})
s, b3, _ = req("GET", "/wp-json/wp/v2/pages/129?context=edit&_fields=content")
print("written:", b3["content"]["raw"] == out, "| backup: 129-%s.html" % ts)
