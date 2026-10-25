# -*- coding: utf-8 -*-
"""Q3: two public tenders that price by Dekel, read in the tender PDFs on 26.10.2026 (official sources for the page):
  - Ministry of Energy, tender 42/2025 (gov.il PDF, p.2, 9, 40 to 42): "המכרז מבוסס על מחירון דקל"; bidders are scored on a discount
    percentage from Dekel; viewing rights to the list come from Dekel and may cost money; work not priced in Dekel is offered apart.
  - Sheba Medical Center, annual price tender 22598198 for water and fire-sprinkler maintenance (mr.gov.il PDF, p.2, 14, 40 to 42):
    payment by "מחירון דקל לבניה ותשתיות במהדורתו האחרונה" less the bid discount, on all chapters with no main or sub contractor
    split; work outside Dekel is paid by a price analysis.
Exact insertion before the "בפרויקט אמיתי" section, backup, read-back, live check.   python .../write_q3_tenders.py [--dry]"""
import io, os, re, sys, time, urllib.parse, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "q3t"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]; DRY = "--dry" in sys.argv
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
PID = 5395
GOV = "https://www.gov.il/BlobFolder/rfp/tender-42-2025/he/tender-42-2025.pdf"
MR = "https://mr.gov.il/ilgstorefront/he/p/attachment/005056BFAF4C1FE0A09457C65CD2B2EE/%D7%97%D7%95%D7%91%D7%A8%D7%AA%20%D7%94%D7%9E%D7%9B%D7%A8%D7%96"
ROWS = [
    ("משרד האנרגיה, מכרז 42/2025", "מערכות מתח נמוך ואבטחה במתקני המשרד", "המכרז מבוסס על מחירון דקל, והציון כולל את אחוז ההנחה מהמחירון", "המציע מקבל הרשאות צפייה מדקל, ושייתכן שבתשלום"),
    ("המרכז הרפואי שיבא, מכרז מחירון שנתי", "אחזקה והתקנה של מערכות מים וכיבוי אש במים", "תשלום לפי מחירון דקל לבנייה ותשתיות במהדורה האחרונה, פחות אחוז ההנחה שהוצע, בכל הפרקים בלי הבחנה בין קבלן ראשי לקבלן משנה", "עבודה שאינה במחירון משולמת לפי ניתוח מחיר"),
]
T = ("<p>כך נראה המחירון במכרזים ציבוריים: המזמין קובע את דקל כבסיס, והקבלנים מתחרים על אחוז ההנחה. שתי דוגמאות מתוך מסמכי מכרז שפורסמו:</p>\n"
     "<figure class=\"wp-block-table\"><table><caption>מחירון דקל בשני מכרזים ציבוריים (מסמכי המכרז, נקראו ב-26.10.2026)</caption><thead><tr><th scope=\"col\">המכרז</th><th scope=\"col\">העבודה</th><th scope=\"col\">איך דקל משמש</th><th scope=\"col\">מה עוד כתוב</th></tr></thead><tbody>"
     + "".join("<tr><th scope=\"row\">%s</th><td>%s</td><td>%s</td><td>%s</td></tr>" % r for r in ROWS) + "</tbody></table></figure>\n"
     "<p><small>לבדיקה במקור: <a href=\"%s\" rel=\"noopener\">מכרז 42/2025 של משרד האנרגיה</a> · <a href=\"%s\" rel=\"noopener\">מכרז המחירון של המרכז הרפואי שיבא</a></small></p>\n" % (GOV, MR))
A = "<h2>בפרויקט אמיתי</h2>"
s, r, _ = req("GET", "/wp-json/wp/v2/nadlan_term/%d?context=edit&_fields=content,link" % PID)
raw = r["content"]["raw"]
assert raw.count(A) == 1 and "מכרז 42/2025" not in raw, (raw.count(A), "already there?")
new = raw.replace(A, T + A)
vis = re.sub(r"<[^>]+>", " ", T)
assert not re.search(r"[–—]", vis) and not re.search(r"ממשק|פלטפורמה|בקרוב", vis)
print("[term %d] +%d words, tables %d -> %d" % (PID, len(re.findall(r"[\w֐-׿\"']+", vis)), raw.count("<table"), new.count("<table")))
if DRY:
    sys.exit(0)
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "term-%d-%s.html" % (PID, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8", newline="").write(raw)
req("POST", "/wp-json/wp/v2/nadlan_term/%d" % PID, {"content": new})
back = req("GET", "/wp-json/wp/v2/nadlan_term/%d?context=edit&_fields=content" % PID)[1]["content"]["raw"]
time.sleep(3)
page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?x=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
ok = {"read-back": back.strip() == new.strip(), "gov link": GOV in page, "mr link": "mr.gov.il/ilgstorefront" in page, "one h1": page[page.find("<body"):].count("<h1") == 1}
for k, v in ok.items(): print("   ", "OK " if v else "BAD", k)
