# -*- coding: utf-8 -*-
"""H Infinity's page text (design system ProjectDossier v74, 28.9.2026). The page had 284 words and numbers with no source:
"52 floors and a 7-floor boutique building, 242 apartments". Hagag's 2025 annual report (the periodic report, Somail 124):
permit 22.12.2021 and a change permit 9.12.2024 for a 53-floor tower and a building of 6 residential floors over a retail
floor, about 278 units; lot 3,167 m2 (block 6213 parcel 1493) bought in 2015; main contractor Electra Construction; the end
of construction estimated for Q4 2026. The lead gets the reported numbers (attributed), a fact table with a source under
each value follows the "page will be updated" paragraph, then three checks before contacting; the sources close the article.
The card's num_units meta goes from 242 to 278. Same mechanism as rainbow_content4.py: raw content over REST (the app
password is decrypted in-process, DPAPI, never printed), each fix must match exactly once, guarded by the md5 of the
content read just before, a copy of the old raw content is saved first.
  python scripts/project-stage/hinfinity_content.py            # show
  python scripts/project-stage/hinfinity_content.py --apply    # write"""
import base64, ctypes, ctypes.wintypes, hashlib, io, json, os, sys, time, urllib.request, urllib.error
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = "https://nad-lan.co.il"
PID = 6548
REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
QA = os.path.join(REPO, "docs", "qa", "hinfinity-content-2026-09-28")
SECRETS_PATH = r"C:\Users\777\Documents\websites\.codex-secrets\wordpress-app-passwords\nad-lan.co.il.json"
APPLY = "--apply" in sys.argv


class DB(ctypes.Structure):
    _fields_ = [("cb", ctypes.wintypes.DWORD), ("pb", ctypes.POINTER(ctypes.c_char))]


def dpapi(b64):
    raw = base64.b64decode(b64)
    bi = DB(len(raw), ctypes.cast(ctypes.create_string_buffer(raw, len(raw)), ctypes.POINTER(ctypes.c_char)))
    bo = DB()
    if not ctypes.windll.crypt32.CryptUnprotectData(ctypes.byref(bi), None, None, None, None, 0, ctypes.byref(bo)):
        raise RuntimeError("DPAPI")
    try:
        return ctypes.string_at(bo.pb, bo.cb).decode("utf-8")
    finally:
        ctypes.windll.kernel32.LocalFree(bo.pb)


with open(SECRETS_PATH, encoding="utf-8-sig") as f:
    sec = json.load(f)
AUTH = "Basic " + base64.b64encode((sec["username"] + ":" + dpapi(sec["password_dpapi"])).encode()).decode()


def req(method, path, body=None, timeout=90):
    r = urllib.request.Request(BASE + path, data=None if body is None else json.dumps(body, ensure_ascii=False).encode(), method=method)
    r.add_header("Authorization", AUTH)
    r.add_header("User-Agent", "Mozilla/5.0 NadLan-HINF-CONTENT/1.0")
    if body is not None:
        r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8") or "null")
    except urllib.error.HTTPError as e:
        p = e.read()
        try:
            return e.code, json.loads(p.decode("utf-8"))
        except Exception:
            return e.code, {"raw": p[:300].decode("utf-8", "replace")}


def read():
    s, d = req("GET", "/wp-json/wp/v2/nadlan_project/%d?context=edit&_fields=id,modified_gmt,content,meta" % PID)
    if s != 200:
        raise SystemExit("FATAL read %s %s" % (s, str(d)[:200]))
    return d




LEAD_OLD = "<p>במתחם סומייל, החלל הפתוח הגדול האחרון של מרכז תל אביב, מקימה קבוצת חג'ג' את H Infinity: מגדל יוקרה בן 52 קומות לצד בניין בוטיק בן 7 קומות - יחד 242 דירות, בתכנון פרופ' משה צור. בין אבן גבירול לז'בוטינסקי, צמוד לכיכר רבין, לעירייה ולשתי תחנות רכבת קלה עתידיות בתוך המתחם. בבניין: בריכת שחייה, מועדון דיירים וחדר כושר, ומסחר בחזית אבן גבירול. הפרויקט בבנייה.</p>"
LEAD_NEW = ("<p>במתחם סומייל, החלל הפתוח הגדול האחרון של מרכז תל אביב, בונה קבוצת חג'ג' את H Infinity: מגדל מגורים ולצדו בניין בוטיק מעל קומת מסחר, "
            "בתכנון פרופ' משה צור. לפי הדוח השנתי של החברה לשנת 2025, ההיתר מתיר מגדל בן 53 קומות ובניין בן 6 קומות מגורים, כ-278 דירות בסך הכול. "
            "בין אבן גבירול לז'בוטינסקי, צמוד לכיכר רבין, לעירייה ולשתי תחנות רכבת קלה עתידיות בתוך המתחם. "
            "לפי אתר הקבוצה, בבניין בריכת אינפיניטי, לובי בגובה של כ-10 מטרים, חדר דיירים ומתקני כושר. "
            "הפרויקט בבנייה, והחברה מעריכה שעבודות ההקמה יסתיימו ברבעון הרביעי של 2026.</p>")

ANCHOR = "<p>העמוד יתעדכן עם קבלת חומרים רשמיים מהיזם: תוכניות קומה, מפרט, מחירים וזמינות.</p>"

FACTS = (
    "<h2>H Infinity במספרים, לפי המקורות</h2>"
    "<p>הנתונים לקוחים מהדוח השנתי של קבוצת חג'ג' לשנת 2025 ומאתרי הקבוצה, כפי שפורסמו. כשהמקורות סותרים זה את זה, מופיעים כולם.</p>"
    "<table><tbody>"
    "<tr><th>יזם</th><td>קבוצת חג'ג' ייזום נדל\"ן, באמצעות חברת הבת קבוצת חג'ג' סומייל<small>הדוח השנתי 2025</small></td></tr>"
    "<tr><th>אדריכל</th><td>פרופ' משה צור<small>אתר קבוצת חג'ג'</small></td></tr>"
    "<tr><th>קבלן ראשי</th><td>אלקטרה בנייה<small>הדוח השנתי 2025</small></td></tr>"
    "<tr><th>הבניינים</th><td>מגדל מגורים בן 53 קומות, ולצדו בניין בן 6 קומות מגורים מעל קומת מסחר"
    "<small>היתר בנייה מ-22.12.2021 והיתר שינויים מ-9.12.2024, לפי הדוח השנתי 2025. באתר הקבוצה: מגדל בן 52 קומות ובניין בוטיק בן 7 קומות. בדף השיווק: 51 קומות.</small></td></tr>"
    "<tr><th>דירות</th><td>כ-278 יחידות דיור, מ-2 עד 6 חדרים, עם מרפסות נוף"
    "<small>מספר הדירות: הדוח השנתי 2025. גודל הדירות: דף השיווק של הפרויקט.</small></td></tr>"
    "<tr><th>המגרש</th><td>3,167 מ\"ר בחלק הצפוני של מתחם סומייל (גוש 6213, חלקה 1493). החברה רכשה אותו ב-2015."
    "<small>הדוח השנתי 2025</small></td></tr>"
    "<tr><th>מתקנים</th><td>בריכת אינפיניטי הצופה לקו החוף, לובי כניסה בגובה של כ-10 מטרים, חדר דיירים, פארק לרווחת הדיירים ומתקני כושר"
    "<small>אתר קבוצת חג'ג'</small></td></tr>"
    "<tr><th>מצב</th><td>בבנייה. החברה מעריכה שעבודות ההקמה יסתיימו ברבעון הרביעי של 2026."
    "<small>הדוח השנתי 2025. זו הערכה של החברה, לא התחייבות.</small></td></tr>"
    "<tr><th>מחירים שפורסמו</th><td>החל מ-65,000 ₪ למ\"ר, כך באתר הקבוצה. דירות החל מ-5.82 מיליון ₪, כך בדף השיווק."
    "<small>כפי שפורסמו בספטמבר 2026. אין זו הצעת מחיר; המחיר של דירה מסוימת נקבע מול היזם.</small></td></tr>"
    "</tbody></table>"
    "<h2>שלושה דברים לבדוק לפני שפונים</h2>"
    "<ol>"
    "<li><strong>תוכנית המכר העדכנית.</strong> המספרים השתנו לאורך השנים: ב-2021 דיווח גלובס על מגדל בן 47 קומות ו-237 דירות, וההיתר מ-2024 מתיר 53 קומות וכ-278 דירות. "
    "כדאי לבקש את תוכנית המכר ואת המפרט שעליהם חותמים.</li>"
    "<li><strong>תנאי לאכלוס.</strong> לפי הדוח השנתי, תנאי לאכלוס הפרויקט הוא הפקדה בפועל של תוכנית לתוספת 450 מ\"ר שטחי ציבור במגרש אחר של החברה, בבלי 3. "
    "כדאי לשאול מה מצבה ומה מועד המסירה הצפוי.</li>"
    "<li><strong>הבטחת הכסף ששילמתם.</strong> הפרויקט החל כקבוצת רכישה, ובסוף 2021 הפך לפרויקט יזמי (גלובס). "
    "חוק המכר מחייב יזם להבטיח את הכספים שרוכש משלם לו, בדרך כלל בערבות בנקאית. כדאי לוודא שמקבלים ערבות על כל תשלום.</li>"
    "</ol>"
)

SOURCES = (
    "<h2>מקורות</h2>"
    "<ul class=\"nlv2-source-list\">"
    "<li><a href=\"https://www.hagag-group.co.il/Uploads/2026/04/rln33jws7WiMM6.pdf\" rel=\"nofollow noopener\">קבוצת חג'ג': הדוח התקופתי לשנת 2025, פרויקט סומייל 124</a></li>"
    "<li><a href=\"https://www.hagag-group.co.il/projects/ResidentProjects/h_infinity\" rel=\"nofollow noopener\">קבוצת חג'ג': עמוד הפרויקט H INFINITY</a></li>"
    "<li><a href=\"https://infinity-hagag.co.il/infinity-tower/\" rel=\"nofollow noopener\">דף השיווק של Infinity Tower</a></li>"
    "<li><a href=\"https://www.globes.co.il/news/article.aspx?did=1001392692\" rel=\"nofollow noopener\">גלובס, 30.11.2021: סומייל הופך לפרויקט יזמי</a></li>"
    "</ul>"
    "<p>הנתונים נבדקו ב-28.9.2026. נדל״ן היא פלטפורמה עצמאית ואינה מטעם קבוצת חג'ג'.</p>"
)

FIXES = [
    (LEAD_OLD, LEAD_NEW),
    (ANCHOR, ANCHOR + FACTS),
]


def build(raw):
    new = raw
    bad = []
    for old, rep in FIXES:
        n = new.count(old)
        print("[fix] x%d  %s..." % (n, old[:60]))
        if n != 1:
            bad.append(old[:60])
            continue
        new = new.replace(old, rep)
    if "nlv2-source-list" in new:
        bad.append("sources already present")
    new = new + SOURCES
    return new, bad


d = read()
raw = d["content"]["raw"]
md5 = hashlib.md5(raw.encode("utf-8")).hexdigest()
meta = d.get("meta") or {}
print("[read] modified", d.get("modified_gmt"), "| md5", md5[:10], "| chars", len(raw), "| num_units", meta.get("num_units", "(not in REST)"))
new, bad = build(raw)
print("[check] 242 left:", new.count("242"), "| 278:", new.count("278"), "| table:", new.count("<table"), "| sources:", new.count("<li><a href"))
if not APPLY:
    raise SystemExit(0)
if bad:
    raise SystemExit("FATAL: %s; nothing written" % bad)
os.makedirs(QA, exist_ok=True)
stamp = time.strftime("%Y%m%dT%H%M%S")
io.open(os.path.join(QA, "post-6548.raw.%s.before.html" % stamp), "w", encoding="utf-8").write(raw)
d2 = read()
if hashlib.md5(d2["content"]["raw"].encode("utf-8")).hexdigest() != md5:
    raise SystemExit("FATAL: the content changed while we read it; nothing written")
payload = {"content": new}
if "num_units" in meta:
    payload["meta"] = {"num_units": 278 if isinstance(meta.get("num_units"), (int, float)) else "278"}
s, r = req("POST", "/wp-json/wp/v2/nadlan_project/%d" % PID, payload)
print("[write]", s)
d3 = read()
print("[verify] content as written:", d3["content"]["raw"] == new, "| num_units now", (d3.get("meta") or {}).get("num_units"))
io.open(os.path.join(QA, "post-6548.raw.%s.after.html" % stamp), "w", encoding="utf-8").write(d3["content"]["raw"])
