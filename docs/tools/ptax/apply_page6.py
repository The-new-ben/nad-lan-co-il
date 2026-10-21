# -*- coding: utf-8 -*-
"""HAD-527 / Kikar tools #2 (Ben 15.10 + 21.10.2026): /purchase-tax-calculator/ (page 6) gets the Instruments tool "ptax" in
place of the old inline widget (.nlc-ptx: two tracks, cream and gold, the banned look, and it sat above any answer). The
content-first order becomes: H1, a one-paragraph answer with numbers, the tool, a worked market example (one contextual link
to /projects/hamedina/), then the guide as it is. Guard: the live content must equal the saved copy (md5) or nothing is
written. Backup before, read-back after.   python docs/tools/ptax/apply_page6.py [--dry]"""
import hashlib, io, os, re, sys, time
REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "ptax6"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]
H = os.path.dirname(os.path.abspath(__file__))
BK = os.path.join(REPO, "docs", "qa", "had-527", "page-backup")
os.makedirs(BK, exist_ok=True)
s, b, _ = req("GET", "/wp-json/wp/v2/pages/6?context=edit&_fields=content,modified")
raw = b["content"]["raw"]
want = io.open(os.path.join(H, "page6-before.html"), encoding="utf-8", newline="").read()
if hashlib.md5(raw.encode()).hexdigest() != hashlib.md5(want.encode()).hexdigest():
    raise SystemExit("FATAL: page 6 changed since it was saved (%s); look before writing" % b["modified"])
a = raw.index("<style>\n.nlc-ptx") if "<style>\n.nlc-ptx" in raw else raw.index("<style>")
assert ".nlc-ptx" in raw[a:a + 200], "the old widget is not where expected"
z = raw.index("</script>", a) + len("</script>")
assert raw.count("nlc-ptx", z) == 0, "the old widget continues after its script"
NEW = ("\n<!-- wp:paragraph -->\n<p><strong>מס רכישה על דירה יחידה ב־2026:</strong> אין מס עד 1,978,745 ₪, ומעל הסכום הזה המס עולה במדרגות של "
       "3.5%, 5%, 8% ו־10%. על דירה נוספת ולתושב חוץ: 8% עד 6,055,070 ₪ ו־10% מעל. לדוגמה, על דירה יחידה ב־3,000,000 ₪ המס הוא 45,538 ₪, "
       "ועל אותה דירה כדירה נוספת 240,000 ₪. המדרגות בתוקף מ־16.1.2025 ומוקפאות עד 15.1.2028.</p>\n<!-- /wp:paragraph -->\n\n"
       "<!-- wp:shortcode -->\n[nadlan_tool id=\"ptax\"]\n<!-- /wp:shortcode -->\n\n"
       "<!-- wp:paragraph -->\n<p><strong>דוגמה מהשוק:</strong> דירה במגדל חדש ב<a href=\"/projects/hamedina/\">כיכר המדינה בתל אביב</a>, "
       "בסביבת 10,000,000 ₪ לפי העסקאות שפורסמו. כדירה יחידה המס הוא 513,886 ₪, כ־5.1% מהמחיר. כדירה נוספת או לתושב חוץ הוא 878,899 ₪, "
       "כ־8.8%, ולעולה חדש 335,976 ₪.</p>\n<!-- /wp:paragraph -->\n")
out = raw[:a] + NEW + raw[z:]
assert out.count("[nadlan_tool") == 1 and out.count("<h1") == 1
print("[plan] page 6: %d -> %d chars; removed %d chars of the old widget" % (len(raw), len(out), z - a))
if "--dry" in sys.argv:
    io.open(os.path.join(H, "page6-after.html"), "w", encoding="utf-8").write(out); raise SystemExit(0)
ts = time.strftime("%Y%m%d-%H%M%S")
io.open(os.path.join(BK, "6-%s.html" % ts), "w", encoding="utf-8").write(raw)
s, b2, _ = req("POST", "/wp-json/wp/v2/pages/6", {"content": out})
s, b3, _ = req("GET", "/wp-json/wp/v2/pages/6?context=edit&_fields=content")
back = b3["content"]["raw"]
print("written:", back == out, "| backup:", "6-%s.html" % ts)
if back != out:
    raise SystemExit("FATAL: read-back differs")
