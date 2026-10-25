# -*- coding: utf-8 -*-
"""Retarget page 4484 /new-projects/new-projects-tel-aviv/ to "דירות חדשות באכלוס מיידי בתל אביב" (Ben 25.10.2026: "what you said
about immediate occupancy in Tel Aviv sounds logical"). Why: it competed with /projects/ for "פרויקטים חדשים" (GSC: ranks 12-15 for
פרויקטים חדשים למגורים / מחירים / פרויקט נדלן חדש) while it already holds the immediate-occupancy intent (11.8 for "פרויקטים חדשים
אכלוס מיידי תל אביב 2026", position 7 for "דירות חדשות אכלוס מיידי תל אביב" in Ben's Chrome, serp.md query 3).
No URL change, no redirect. Changes: page title (H1), Yoast title, description, focus keyword, breadcrumb title; the article schema
headline; a new answer paragraph that sends the general intent to /projects/; a table of the Tel Aviv projects with immediate or
near occupancy (data/projects-market.json, as published, 25.10.2026); "what to check in a ready apartment"; three questions; one
heading reworded. Everything else on the page stays.
Guard: the live raw content must still be the backup this script read (md5); reads back after the write; checks the live page.
  python docs/research/2026-10-25-projects-hub/retarget_tlv.py [--dry]"""
import hashlib, html as HT, io, json, os, re, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(H)))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "rt4484"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]; DRY = "--dry" in sys.argv
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
PID = 4484
TITLE = "דירות חדשות באכלוס מיידי בתל אביב: פרויקטים מוכנים ואכלוס קרוב"
SEO_T = "אכלוס מיידי בתל אביב 2026: דירות חדשות מוכנות מקבלן | nad-lan"
SEO_D = "דירות חדשות באכלוס מיידי ובאכלוס קרוב בתל אביב: הפרויקטים המוכנים או לקראת מסירה, המחירים שפרסמו היזמים, מה בודקים בדירה גמורה ואיך משווים לפני חתימה."
CRUMB = "אכלוס מיידי בתל אביב"
FOCUS = "אכלוס מיידי בתל אביב"

s, b, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=id,title,content,meta,link,modified" % PID)
raw = b["content"]["raw"]; md5 = hashlib.md5(raw.encode("utf-8")).hexdigest()
bk = sorted(f for f in os.listdir(os.path.join(REPO, "docs", "qa", "projects-hub")) if f.startswith("page-4484-before-") and f.endswith(".html"))[-1]
bk_raw = io.open(os.path.join(REPO, "docs", "qa", "projects-hub", bk), encoding="utf-8").read()
assert raw == bk_raw, "page 4484 changed since the backup %s: read it again before retargeting" % bk
print("[guard] live raw = backup", bk, md5[:10])

m = json.load(io.open(os.path.join(REPO, "plugins", "nadlan-config", "data", "projects-market.json"), encoding="utf-8"))
rows = [p for p in m["projects"] if "תל אביב" in p["city"] and p.get("status") in ("immediate", "near_occupancy")]
rows.sort(key=lambda p: (0 if p.get("status") == "immediate" else 1, -(p.get("price_from") or 0) == 0, p.get("price_from") or 9e12))
ST = {"immediate": "אכלוס מיידי", "near_occupancy": "אכלוס קרוב"}
e = HT.escape
tr = ""
for p in rows:
    name = e(p["name"])
    if p.get("url"):
        name = '<a href="%s">%s</a>' % (p["url"], name)
    price = ("%s ₪" % format(p["price_from"], ",")) if p.get("price_from") else "לפי פנייה ליזם"
    when = ST[p["status"]] + ((" · " + e(p["delivery"])) if p.get("delivery") and p["delivery"] not in ("אכלוס מיידי",) else "")
    tr += ('<tr><th scope="row">%s<small>%s</small></th><td data-l="יזם">%s</td><td data-l="חדרים">%s</td><td data-l="החל מ">%s</td><td data-l="אכלוס">%s</td></tr>'
           % (name, e(p.get("neighbourhood") or "תל אביב יפו"), e(p.get("developer") or ""), e(p.get("rooms") or ""), price, when))
n_imm = sum(1 for p in rows if p["status"] == "immediate"); n_near = len(rows) - n_imm
CSS = ('<style>.nlrt-t{width:100%;border-collapse:collapse;margin:14px 0;font-size:16px}.nlrt-t th,.nlrt-t td{padding:10px;border-bottom:1px solid #dce8e1;text-align:right;vertical-align:top}'
       '.nlrt-t thead th{background:#f2faf5;color:#2f433b;font-size:14px}.nlrt-t tbody th{color:#08382d}.nlrt-t small{display:block;color:#5b6b64;font-weight:400;font-size:13px}'
       '.nlrt-w{overflow-x:auto}.nlrt-src{font-size:14px!important;color:#5b6b64!important}'
       '@media(max-width:640px){.nlrt-t thead{display:none}.nlrt-t tr{display:block;border:1px solid #dce8e1;border-radius:12px;margin:0 0 8px;padding:6px 10px}.nlrt-t th,.nlrt-t td{display:block;border:0;padding:3px 0}'
       '.nlrt-t td[data-l]::before{content:attr(data-l) ": ";color:#5b6b64;font-size:13px}}</style>')
INTRO = ('<p dir="rtl"><strong>מחפשים דירה חדשה בתל אביב שאפשר להיכנס אליה עכשיו או בקרוב?</strong> ברשימה שלמטה %d פרויקטים חדשים בתל אביב יפו: '
         '%d באכלוס מיידי ו־%d באכלוס קרוב, מנאות אפקה ורמת אביב ועד יד אליהו ויפו, עם היזם, החדרים והמחיר שהיזם פרסם. דירה גמורה רואים בעיניים לפני '
         'החתימה, נכנסים אליה בלי שנים של המתנה ומשלמים בלי הצמדה ארוכה למדד. ומי שמחפש את כל הפרויקטים החדשים בישראל ובתל אביב, גם על הנייר ובפריסייל, '
         'ימצא אותם ב<a href="/projects/">עמוד הפרויקטים החדשים</a>, עם 566 פרויקטים בשיווק, מחירים לפי עיר ומחשבונים.</p>') % (len(rows), n_imm, n_near)
TABLE = ('%s<h2 dir="rtl">פרויקטים באכלוס מיידי ובאכלוס קרוב בתל אביב</h2>'
         '<p dir="rtl">הפרויקטים שבהם הדירות מוכנות או שהמסירה צפויה בחודשים הקרובים, לפי מה שפרסמו היזמים. "אכלוס מיידי": הבניין קיבל טופס 4 או שהדירות כבר נמסרות. '
         '"אכלוס קרוב": מסירה צפויה עד כשנה וחצי, לפי פרסום היזם.</p>'
         '<div class="nlrt-w"><table class="nlrt-t"><thead><tr><th scope="col">פרויקט</th><th scope="col">יזם</th><th scope="col">חדרים</th><th scope="col">החל מ</th><th scope="col">אכלוס</th></tr></thead><tbody>%s</tbody></table></div>'
         '<p dir="rtl" class="nlrt-src">כפי שפרסמו היזמים באתריהם ובפרסומי השיווק של הפרויקטים, נכון ל־25.10.2026. המחיר הסופי, הדירות שנותרו ומועד המסירה נקבעים מול היזם ובחוזה. '
         'כל הפרויקטים בשיווק בתל אביב, גם על הנייר: <a href="/projects/#nlph-market">טבלת הפרויקטים החדשים בשיווק</a>.</p>'
         '<h2 dir="rtl">מה בודקים בדירה חדשה באכלוס מיידי</h2><ul dir="rtl">'
         '<li><strong>טופס 4 ותעודת גמר:</strong> האישור לחבר את הבניין לחשמל, למים ולגז. בלי טופס 4 אין אכלוס.</li>'
         '<li><strong>בדק בית לפני המסירה:</strong> ליקויים שרואים במסירה מדווחים ליזם בכתב תוך שנה, ולכל סוג ליקוי יש תקופת בדק של שנה עד שבע שנים לפי חוק המכר.</li>'
         '<li><strong>המפרט מול הדירה:</strong> ריצוף, מטבח, מיזוג, ממ"ד, חניה ומחסן כפי שנכתבו במפרט החתום.</li>'
         '<li><strong>רישום הבית המשותף:</strong> היזם רושם את הבניין תוך שנה מהמסירה ואת הזכויות על שמכם תוך 6 חודשים אחר כך. כדאי לשאול באיזה שלב הרישום.</li>'
         '<li><strong>לוח התשלומים:</strong> בדירה גמורה משלמים מהר, ולכן כדאי לוודא שהמשכנתא מאושרת לפני החתימה ושכל תשלום עובר בשובר עם ערבות.</li>'
         '<li><strong>מס רכישה ומשפרי דיור:</strong> מי שמוכר דירה קיימת מקבל 12 חודשים מקבלת הדירה החדשה, או 24 חודשים מהקנייה, המאוחר מביניהם.</li></ul>') % (CSS, tr)
FAQ_ADD = ('<h3 dir="rtl">איפה יש דירות חדשות באכלוס מיידי בתל אביב?</h3><p dir="rtl">בטבלה שבראש העמוד %d פרויקטים חדשים בתל אביב יפו באכלוס מיידי או באכלוס קרוב, '
           'בנאות אפקה, ברמת אביב, בצפון הישן והחדש, ביד אליהו, בביצרון וביפו. לכל פרויקט מופיעים היזם, החדרים, המחיר שפורסם ומועד המסירה.</p>'
           '<h3 dir="rtl">מה ההבדל בין אכלוס מיידי לאכלוס קרוב?</h3><p dir="rtl">באכלוס מיידי הבניין כבר קיבל טופס 4 והדירות נמסרות, כך שאפשר לבדוק את הדירה הגמורה ולהיכנס אליה מיד אחרי '
           'החתימה והתשלום. באכלוס קרוב הבניין לקראת סיום והמסירה צפויה בחודשים הקרובים, ולכן עדיין חלה ההצמדה למדד עד מועד המסירה שבחוזה.</p>'
           '<h3 dir="rtl">איפה רואים את כל הפרויקטים החדשים בתל אביב?</h3><p dir="rtl">בעמוד הפרויקטים החדשים של נדל"ן: 566 פרויקטים בשיווק בישראל, 143 מהם בתל אביב, עם המחיר שפרסם היזם, '
           'פרק מיוחד על פרויקטים חדשים בתל אביב לפי אזור, מחירי עסקאות לפי שכונה ומחשבונים.</p>') % len(rows)

new = raw
def rep(a, b2, n=1):
    global new
    assert new.count(a) == n, (new.count(a), a[:80])
    new = new.replace(a, b2)

# the article schema headline and date
rep('"headline":"פרויקטים חדשים בתל אביב: מחירים, אכלוס והשוואה לפני חתימה"', '"headline":"' + TITLE + '"')
rep('"dateModified":"2026-06-04"', '"dateModified":"2026-10-25"')
# the answer first: a new opening paragraph, then the old one stays as the second paragraph
first_p = new[new.find('<p dir="rtl">פרויקט חדש בתל אביב יכול להיות החלטה'):]
first_p = first_p[:first_p.find("</p>") + 4]
rep(first_p, INTRO + first_p + TABLE)
# the general head phrase leaves the headings and the first line
rep('<h2 dir="rtl">פרויקטים חדשים בתל אביב: מה באמת משווים לפני שמשאירים פרטים</h2>', '<h2 dir="rtl">דירה מוכנה, אכלוס קרוב או על הנייר: מה באמת משווים לפני שמשאירים פרטים</h2>')
rep('השוואה נכונה בין פרויקטים חדשים בתל אביב אינה מתחילה', 'השוואה נכונה בין דירות חדשות בתל אביב אינה מתחילה')
# three questions first in the FAQ
rep('<h2 dir="rtl">שאלות נפוצות</h2>', '<h2 dir="rtl">שאלות נפוצות</h2>' + FAQ_ADD)
assert not re.search(r"[–—]", re.sub(r"<[^>]+>", " ", INTRO + TABLE + FAQ_ADD)), "dash in the new copy"
print("[plan] title:", TITLE, "| seo:", SEO_T, "| rows:", len(rows), "(%d immediate, %d near)" % (n_imm, n_near), "| +%d chars" % (len(new) - len(raw)))
io.open(os.path.join(REPO, "docs", "qa", "projects-hub", "page-4484-after.html"), "w", encoding="utf-8").write(new)
if DRY:
    print("[dry] no write"); sys.exit(0)
s2, b2, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content" % PID)
assert hashlib.md5(b2["content"]["raw"].encode("utf-8")).hexdigest() == md5, "page changed during the run"
body = {"title": TITLE, "content": new, "meta": {"_yoast_wpseo_title": SEO_T, "_yoast_wpseo_metadesc": SEO_D, "_yoast_wpseo_bctitle": CRUMB, "_yoast_wpseo_focuskw": FOCUS}}
s3, b3, _ = req("POST", "/wp-json/wp/v2/pages/%d" % PID, body)
print("[write]", s3)
s4, back, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,title,meta,link" % PID)
print("[read-back] content same:", back["content"]["raw"] == new, "| title:", back["title"]["raw"] == TITLE, "| seo title:", back["meta"].get("_yoast_wpseo_title") == SEO_T)
time.sleep(3)
page = urllib.request.urlopen(urllib.request.Request(back["link"] + "?rt=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
bd = page[page.find("<body"):]
t = HT.unescape(re.search(r"<title>(.*?)</title>", page, re.S).group(1)).strip()
h1 = [HT.unescape(re.sub("<[^>]+>", "", x)).strip() for x in re.findall(r"<h1[^>]*>(.*?)</h1>", bd, re.S)]
print("[live] title:", t); print("[live] h1:", h1)
print("[live] table rows:", bd.count("<tr><th scope=\"row\">"), "| link to /projects/:", bd.count('href="/projects/"') + bd.count('href="https://nad-lan.co.il/projects/"'), "| FAQPage:", "FAQPage" in page)
