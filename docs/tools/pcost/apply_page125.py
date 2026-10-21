# -*- coding: utf-8 -*-
"""HAD-575 / Kikar tools #3 (Ben 15.10 + 21.10.2026): /apartment-purchase-cost-calculator/ (page 125) gets the Instruments tool
"pcost" in place of the old inline calculator (section.calc-shell + its script: the purchase tax typed by hand). Every field of
the old widget lives on in the new tool. The order after the hero: a one-paragraph answer with numbers, the tool, a worked market
example (one contextual link to /projects/hamedina/), then the guide as it is. Guard: the live content must equal the saved copy
(md5). Backup before, read-back after.   python docs/tools/pcost/apply_page125.py [--dry]"""
import hashlib, io, os, sys, time
REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "pcost125"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]
H = os.path.dirname(os.path.abspath(__file__))
s, b, _ = req("GET", "/wp-json/wp/v2/pages/125?context=edit&_fields=content,modified")
raw = b["content"]["raw"]
want_p = os.path.join(H, "page125-before.html")
if not os.path.exists(want_p):
    io.open(want_p, "w", encoding="utf-8", newline="").write(raw); print("saved page125-before.html")
want = io.open(want_p, encoding="utf-8", newline="").read()
if hashlib.md5(raw.encode()).hexdigest() != hashlib.md5(want.encode()).hexdigest():
    raise SystemExit("FATAL: page 125 changed since it was saved (%s); look before writing" % b["modified"])
a = raw.index('<section class="calc-shell wrap"')
z = raw.index("</section>", raw.index('class="mini-results"', a)) + len("</section>")
s0 = raw.index('<script id="nadlan-apartment-cost-calculator-js-20260528">')
s1 = raw.index("</script>", s0) + len("</script>")
assert a < z < s0 < s1 and raw[a:z].count('id="nap-') >= 10
NEW = ('<section class="wrap" aria-label="מחשבון עלות רכישה כוללת">\n'
       '<p><strong>כמה כסף צריך כדי לקנות דירה:</strong> על דירת יד שנייה ב־3,000,000 ₪, כדירה יחידה ועם משכנתא של 1,500,000 ₪, עלויות העסקה '
       'מעבר למחיר הן כ־137,048 ₪ (4.6%): מס רכישה 45,538 ₪, עורך דין 17,700 ₪ ותיווך 70,800 ₪ כולל מע״מ, שמאי, בדיקות ופתיחת תיק. עם מעבר, שיפוץ, '
       'ריהוט ומרווח ביטחון, ההון העצמי שצריך להכין הוא כ־1,819,048 ₪. בדירה נוספת או לתושב חוץ המס גבוה בהרבה, והבנק מממן עד 50% בלבד.</p>\n'
       '[nadlan_tool id="pcost"]\n'
       '<p><strong>דוגמה מהשוק:</strong> דירה חדשה ב<a href="/projects/hamedina/">מגדלי כיכר המדינה בתל אביב</a>, בסביבת 10,000,000 ₪ לפי העסקאות שפורסמו, '
       'כדירה נוספת או לתושב חוץ, עם משכנתא של 50% (המימון המרבי במסלולים האלה): מס רכישה 878,899 ₪, עורך דין 59,000 ₪ כולל מע״מ, ועוד שמאי, בדיקות '
       'ופתיחת תיק, יחד כ־940,909 ₪ (9.4% מהמחיר). ההון העצמי שצריך הוא כ־5,940,909 ₪, לפני מעבר וריהוט.</p>\n</section>')
out = raw[:a] + NEW + raw[z:s0] + raw[s1:]
assert out.count("[nadlan_tool") == 1 and 'id="nap-' not in out
print("[plan] page 125: %d -> %d chars; the old calculator (%d) and its script (%d) out" % (len(raw), len(out), z - a, s1 - s0))
if "--dry" in sys.argv:
    io.open(os.path.join(H, "page125-after.html"), "w", encoding="utf-8", newline="").write(out); raise SystemExit(0)
bk = os.path.join(REPO, "docs", "qa", "had-527", "page-backup"); os.makedirs(bk, exist_ok=True)
ts = time.strftime("%Y%m%d-%H%M%S")
io.open(os.path.join(bk, "125-%s.html" % ts), "w", encoding="utf-8", newline="").write(raw)
req("POST", "/wp-json/wp/v2/pages/125", {"content": out})
s, b3, _ = req("GET", "/wp-json/wp/v2/pages/125?context=edit&_fields=content")
print("written:", b3["content"]["raw"] == out, "| backup: 125-%s.html" % ts)
