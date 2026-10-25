# -*- coding: utf-8 -*-
"""Q5: the official source for "רשמי או מחייב" on /glossary/תי-466/ (term 5366), read in the gazette PDF on 26.10.2026:
Reshumot, Kovetz HaTakanot 12253, 8.2.2026 (gov.il), "תקנות התכנון והבנייה (הקמת מכון בקרה ודרכי עבודתו) (תיקון), התשפ"ו-2026":
p.2 adds the definition "ת"י 466 - תקן ישראלי ת"י 466 - חוקת הבטון" after the definition of ת"י 413; p.18 adds "ות"י 466" to the
structural-design item of the schedule, whose new sub-item lists the main structural elements (slabs, columns, foundations, transfer
slab, prestressed member, shoring) with the required reinforcement. Exact insertion before the errata section, backup, read-back, live check.
  python docs/research/2026-10-26-upgrades/q5-ti-466/write_q5_reshumot.py [--dry]"""
import io, os, re, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "q5r"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]; DRY = "--dry" in sys.argv
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
PID = 5366
URL = "https://www.gov.il/BlobFolder/guide/training_control_institute/he/regulations-file-12253.pdf"
T = ("<h3>מה כתוב בתקנות על ת\"י 466</h3>\n"
     "<p>בתיקון לתקנות התכנון והבנייה (הקמת מכון בקרה ודרכי עבודתו), שפורסם ברשומות ב-8.2.2026, נוספה לתקנות הגדרה של \"ת\"י 466\" כתקן ישראלי ת\"י 466, חוקת הבטון. "
     "באותו תיקון ת\"י 466 נוסף לפרט שעוסק בתכן הקונסטרוקציה, לצד תכן הרכיבים הראשיים של המבנה וחישוב הזיון שלהם: תקרות, עמודים, ביסוס, תקרת טרנספורמציה, רכיב דרוך ודיפון. "
     "כלומר, גם כששדה המעמד באתר מכון התקנים ריק, התקן נזכר בשמו בתקנות שלפיהן עובד מכון הבקרה.</p>\n"
     "<p><small>לבדיקה במקור: <a href=\"%s\" rel=\"noopener\">רשומות, קובץ התקנות 12253, 8.2.2026</a></small></p>\n" % URL)
A = "<h2>תיקוני טעות, גיליונות תיקון ותקופות מעבר</h2>"
s, r, _ = req("GET", "/wp-json/wp/v2/nadlan_term/%d?context=edit&_fields=content,link" % PID)
raw = r["content"]["raw"]
assert raw.count(A) == 1 and "12253" not in raw, (raw.count(A), "already there?")
new = raw.replace(A, T + A)
vis = re.sub(r"<[^>]+>", " ", T)
assert not re.search(r"[–—]", vis) and not re.search(r"ממשק|פלטפורמה|בקרוב", vis)
print("[term %d] +%d words" % (PID, len(re.findall(r"[\w֐-׿\"']+", vis))))
if DRY:
    sys.exit(0)
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "term-%d-%s.html" % (PID, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8", newline="").write(raw)
req("POST", "/wp-json/wp/v2/nadlan_term/%d" % PID, {"content": new})
back = req("GET", "/wp-json/wp/v2/nadlan_term/%d?context=edit&_fields=content" % PID)[1]["content"]["raw"]
time.sleep(3)
page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?x=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
ok = {"read-back": back.strip() == new.strip(), "gov link": URL in page, "one h1": page[page.find("<body"):].count("<h1") == 1, "one FAQPage": page.count('"@type":"FAQPage"') == 1}
for k, v in ok.items(): print("   ", "OK " if v else "BAD", k)
