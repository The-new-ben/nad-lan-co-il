# -*- coding: utf-8 -*-
"""/investment/ (page 421) quick fixes from dna.md section 7 (Ben 25.10.2026: the small fixes first):
  1. the false claim "אין מקור ממשלתי שמפרסם תשואה": nadlan.gov.il shows a median annual rental yield per city (Tel Aviv 2.72%, 25.10.2026);
  2. the 8% purchase tax order gets its date (extended to purchases up to 10.2.2027, Tax Authority notice of 12.10.2026);
  3. ten "טעון אימות" hedges become plain instructions to the reader;
  4. the footer drops the banned "נדל״ן חכם" and the stale "עודכן יוני 2026"; the schema author name matches its own @id (ben-betesh),
     the publisher reads נדלן, dateModified is today.
Exact replacements (each must match; whitespace between table cells is matched loosely), backup, read-back, live check.
The full build (the yield and cash-flow map of 65 cities) is the next stage.   python .../fix_inv_quick.py [--dry]"""
import io, os, re, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "invq"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]; DRY = "--dry" in sys.argv
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
PID = 421
GOV = "אתר הנדל״ן הממשלתי מציג לכל עיר תשואת שכירות חציונית שנתית ברוטו (בתל אביב 2.72%, לפי האתר ב-25.10.2026)"
R = [  # (regex, replacement)
    (r"היא טעון אימות עד שנבדקת", "אינה עובדה עד שנבדקת"),
    (r"הוא טעון אימות\. אין מקור ממשלתי שמפרסם תשואה נטו מובטחת", "צריך לבדוק מול עסקאות ושכירויות בפועל. " + GOV + ", אבל אף מקור ממשלתי לא מפרסם תשואה נטו מובטחת"),
    (r"<td>אין מקור ממשלתי שמפרסם תשואה נטו רשמית לפי נכס</td>(\s*)<td>כל הבטחת תשואה היא טעון אימות</td>",
     r"<td>" + GOV + "; תשואה נטו לפי נכס אין</td>\1<td>הבטחת תשואה נבדקת מול שכירות ומחיר בפועל</td>"),
    (r"סטטוס מס רכישה אישי הוא תמיד טעון אימות מול", "סטטוס מס רכישה אישי בודקים תמיד מול"),
    (r"היא טעון אימות\.</p>", "צריכה בדיקה של עורך דין או רואה חשבון.</p>"),
    (r"בחירת מסלול מס היא טעון אימות לפי נתוני המשקיע\.", "את מסלול המס בוחרים לפי הנתונים של המשקיע, אחרי שמחשבים כל מסלול."),
    (r"נוסח חוזה ספציפי הוא טעון אימות\.", "את נוסח החוזה לנכס מסוים כדאי לבדוק עם עורך דין."),
    (r"נתוני מס אישיים הם תמיד טעון אימות\.", "את נתוני המס האישיים בודקים לפני שמחליטים."),
    (r"הערת אימות: לא נמצא מקור ממשלתי רשמי שמפרסם תשואה נטו מומלצת לפי עיר, שכונה ונכס\. לכן כל נתון תשואה נקודתי, הבטחת תשואה או דירוג עיר להשקעה הוא טעון אימות\.",
     "אתר הנדל״ן הממשלתי (nadlan.gov.il) מפרסם לכל עיר תשואת שכירות חציונית שנתית ברוטו, אבל לא תשואה נטו לפי שכונה ונכס. נתון תשואה נקודתי, הבטחת תשואה או דירוג עיר להשקעה בודקים מול עסקאות ושכירויות בפועל."),
    (r"בתקופת ההוראה הרלוונטית, מס רכישה על דירה נוספת", "בהוראת שעה שהוארכה לרכישות עד 10.2.2027 (הודעת רשות המסים מ-12.10.2026), מס רכישה על דירה נוספת"),
    (r"נכתב ונערך בידי מערכת נדל״ן חכם\. עודכן יוני 2026\.", "נכתב ונערך בידי צוות נדלן. עודכן 25.10.2026."),
    (r'"name": "מערכת נדל״ן חכם", "jobTitle": "עורך דין מקרקעין"', '"name": "בן בטש", "jobTitle": "עורך דין מקרקעין"'),
    (r'"publisher": \{"@type": "Organization", "name": "נדלן חכם"', '"publisher": {"@type": "Organization", "name": "נדלן"'),
    (r'"dateModified": "2026-05-30"', '"dateModified": "2026-10-25"'),
]
s, r, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,link" % PID)
raw = r["content"]["raw"]; new = raw
for pat, rep in R:
    new, n = re.subn(pat, rep, new)
    assert n == 1, (n, pat[:60])
left = new.count("טעון אימות")
vis = re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style)\b.*?</\1>", " ", new, flags=re.S))
print("[page %d] %d replacements | 'טעון אימות' left: %d | 'נדל״ן חכם' left in text: %d | 'אין מקור ממשלתי' left: %d" % (PID, len(R), left, vis.count("נדל״ן חכם") + vis.count("נדלן חכם"), new.count("אין מקור ממשלתי")))
if DRY:
    sys.exit(0)
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "page-%d-%s.html" % (PID, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8", newline="").write(raw)
req("POST", "/wp-json/wp/v2/pages/%d" % PID, {"content": new})
back = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content" % PID)[1]["content"]["raw"]
time.sleep(3)
page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?x=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
bd = page[page.find("<body"):]
ok = {"read-back": back == new, "one h1": bd.count("<h1") == 1, "no 'טעון אימות'": "טעון אימות" not in bd, "gov yield fact": "2.72%" in bd,
      "10.2.2027": "10.2.2027" in bd, "no stale footer": "עודכן יוני 2026" not in bd}
for k, v in ok.items(): print("   ", "OK " if v else "BAD", k)
