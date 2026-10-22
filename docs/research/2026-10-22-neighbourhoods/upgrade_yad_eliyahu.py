# -*- coding: utf-8 -*-
"""Neighbourhood wave 1, the upgrade (HAD-583 / HAD-592): /tel-aviv-plans/yad-eliyahu/ (page 7103) already owns the words yad and
eliyahu, so the prices go into the existing page instead of a new URL. Added, nothing removed (the additive law):
  - before the section "מהתכנון אל הדירות": a price section (the answer paragraph with the official medians, the value tool opened on
    the neighbourhood, the 8-quarter table from blocks/65210057.html, the five-year line);
  - after that section: a FAQ (h3 questions, so the page gets FAQPage from the tool module);
  - the Yoast title and description now say prices + renewal (the H1, the WordPress title, stays the planning headline).
Backup in page-backup/, read-back, live checks.   python docs/research/2026-10-22-neighbourhoods/upgrade_yad_eliyahu.py [--dry]"""
import io, os, re, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(H)))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "yad"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]; DRY = "--dry" in sys.argv
PID = 7103
TABLE = io.open(os.path.join(H, "blocks", "65210057.html"), encoding="utf-8").read().strip()
NOTE = ('<p>המספר המודגש הוא החציון של השכונה, ומתחתיו, בקטן, החציון של כל העיר באותו רבעון. רבעון שבו נמכרו בשכונה מעט מדי דירות '
        'מאותו סוג אין בו חציון רשמי, ואז כתוב אין. המקור: הקובץ הרשמי של רשות המסים באתר נתוני הנדל״ן הממשלתי, בגרסה מ־20.8.2026.</p>')
PRICES = ('<section class="nlhood-prices" id="yad-eliyahu-prices"><h2>מחירי הדירות ביד אליהו לפי חדרים</h2>'
          '<p><strong>כמה עולה דירה ביד אליהו:</strong> דירת 3 חדרים בשכונה נמכרה ברבעון הראשון של 2026 במחיר חציוני של 3,160,100 ₪, '
          'ודירת 4 חדרים ב־3,774,500 ₪. זה 25% ו־28% פחות מהחציון של כל תל אביב-יפו באותו רבעון (4,225,800 ₪ ו־5,229,800 ₪). '
          'אלה החציונים הרשמיים של העסקאות שדווחו לרשות המסים. בכלי שלמטה בודקים כמה שווה דירה בשכונה, לפי מספר החדרים וההתאמות שלכם.</p>\n'
          '[nadlan_tool id="pval" city="תל אביב יפו" hood="65210057" rooms="4"]\n'
          '<h3>המחירים רבעון אחרי רבעון</h3>\n' + NOTE + '\n' + TABLE + '\n'
          '<p>בחמש שנים דירת 3 חדרים ביד אליהו עלתה מ־2,662,800 ₪ ברבעון הראשון של 2021 ל־3,160,100 ₪ ברבעון הראשון של 2026, כ־19%. '
          'באותן שנים החציון של כל העיר עלה בכ־38%, ולכן הפער בין השכונה לעיר גדל מכ־13% לכ־25%. בדירות 4 חדרים התמונה דומה: '
          'מ־3,487,400 ₪ ברבעון השני של 2021 ל־3,774,500 ₪, כ־8%, מול כ־34% בעיר. רוב העסקאות בשכונה הן בבניינים הוותיקים, '
          'ולכן פרויקט התחדשות שמסתיים, או מגדל חדש, יכולים להזיז את החציון מרבעון לרבעון יותר מכל שינוי בשוק.</p>'
          '<p>לפני שמגישים הצעה כדאי לחשב את כל העסקה: <a href="/purchase-tax-calculator/">מס הרכישה</a>, '
          '<a href="/apartment-purchase-cost-calculator/">העלות הכוללת עם עורך דין ושמאי</a> ו<a href="/mortgage-calculator/">ההחזר החודשי של המשכנתא</a>. '
          'ההשוואה לשכונות אחרות בעיר נמצאת ב<a href="/tel-aviv-apartment-prices/">מחירי הדירות בתל אביב</a>.</p></section>')
FAQ = ('<section class="nlhood-faq"><h2>שאלות נפוצות על יד אליהו</h2>'
       '<h3>כמה עולה דירת 3 חדרים ביד אליהו?</h3><p>החציון הרשמי ברבעון הראשון של 2026 הוא 3,160,100 ₪, לפי העסקאות שדווחו לרשות המסים. '
       'חצי מהדירות נמכרו ביותר וחצי בפחות, ולכן דירה מסוימת יכולה להיות רחוקה מהמספר.</p>'
       '<h3>כמה עולה דירת 4 חדרים ביד אליהו?</h3><p>החציון הרשמי ברבעון הראשון של 2026 הוא 3,774,500 ₪. בכל העיר החציון לדירת 4 חדרים '
       'באותו רבעון היה 5,229,800 ₪.</p>'
       '<h3>האם יד אליהו זולה משאר תל אביב?</h3><p>כן. ברבעון הראשון של 2026 דירות 3 חדרים בשכונה נמכרו ב־25% פחות מהחציון של העיר, '
       'ודירות 4 חדרים ב־28% פחות. הפער גדל בחמש השנים האחרונות, כי העיר עלתה מהר יותר מהשכונה.</p>'
       '<h3>למה ברבעונים מסוימים אין חציון רשמי?</h3><p>כשנמכרות בשכונה מעט מדי דירות מאותו סוג ברבעון, הקובץ הרשמי לא מפרסם חציון. '
       'בטבלה כתוב אז אין, והחציון של העיר מופיע לידו להשוואה.</p>'
       '<h3>איך ההתחדשות העירונית משפיעה על המחירים בשכונה?</h3><p>רוב העסקאות ביד אליהו הן בבניינים ותיקים. כשבניין עובר תמ״א 38 '
       'או פינוי בינוי, הדירות החדשות נמכרות במחיר אחר, ולכן כדאי לבדוק לכל כתובת באיזה שלב התכנון נמצא, כפי שמוסבר למעלה בעמוד.</p></section>')
SEO_T = "יד אליהו בתל אביב: מחירי דירות, התחדשות ותכניות"
SEO_D = "דירת 3 חדרים ביד אליהו נמכרה ב־2026 בחציון של 3.16 מיליון ₪, 25% פחות מתל אביב. המחירים הרשמיים לפי רבעון, מחשבון שווי, ומה התכניות משנות."
ANCHOR = '<section class="nltlv-next"><h2>מהתכנון אל הדירות</h2>'

s, b, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,link,meta" % PID)
raw = b["content"]["raw"]; link = b["link"]
assert raw.count(ANCHOR) == 1, "anchor x%d" % raw.count(ANCHOR)
if "nlhood-prices" in raw:
    raise SystemExit("already upgraded")
i = raw.index(ANCHOR); j = raw.index("</section>", i) + len("</section>")
new = raw[:i] + PRICES + "\n" + raw[i:j] + "\n" + FAQ + raw[j:]
print("page", PID, link, "| before", len(raw), "after", len(new), "| yoast now:", (b.get("meta") or {}).get("_yoast_wpseo_title"))
if DRY:
    raise SystemExit("[dry] no write")
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "page-%d-%s.html" % (PID, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8", newline="").write(raw)
req("POST", "/wp-json/wp/v2/pages/%d" % PID, {"content": new, "meta": {"_yoast_wpseo_title": SEO_T, "_yoast_wpseo_metadesc": SEO_D}})
back = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,meta" % PID)[1]
time.sleep(2)
html = urllib.request.urlopen(urllib.request.Request(link + "?nlv=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
body = html[html.find("<body"):]
checks = {"read-back equal": back["content"]["raw"] == new, "yoast title": back["meta"].get("_yoast_wpseo_title") == SEO_T,
          "one h1": body.count("<h1") == 1, "tool on the hood": 'data-nli="pval"' in body and "65210057" in body,
          "table": "יד אליהו מול תל אביב-יפו" in body, "FAQPage": "FAQPage" in html, "seo title live": SEO_T in html,
          "old text kept": "לה גווארדיה אמור לפעול כרחוב" in body and "מהתכנון אל הדירות" in body, "no shortcode left": "[nadlan_tool" not in body}
for k, v in checks.items(): print("   ", "OK " if v else "BAD", k)
print("ALL OK" if all(checks.values()) else "CHECK FAILED")
