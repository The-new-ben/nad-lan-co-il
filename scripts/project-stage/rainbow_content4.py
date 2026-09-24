# -*- coding: utf-8 -*-
"""Rainbow's page text, fourth pass (the site loop, R2, 25.9.2026): the article stops describing the old engine. It
promised a "מודל בחירה", unit selection, lead fields that keep "the floor, the unit, the direction, the area", a gallery
"in this card" (its three AI pictures were removed from photos_csv the same night) and a pitch to developers; the byline
said June 2026. Now it says what the page does: prices with their source, a floor and a direction in the virtual tour,
the estimated view and the map, and a WhatsApp request for plans and prices. Same mechanism as rainbow_content2.py:
reads post 4464's raw content over REST (the app password is decrypted in-process, DPAPI, never printed), each fix must
match exactly once, guarded by the md5 of the content read just before, a copy of the old raw content is saved first.
  python scripts/project-stage/rainbow_content4.py            # show
  python scripts/project-stage/rainbow_content4.py --apply    # write"""
import base64, ctypes, ctypes.wintypes, hashlib, io, json, os, sys, time, urllib.request, urllib.error
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = "https://nad-lan.co.il"
PID = 4464
REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
QA = os.path.join(REPO, "docs", "qa", "rainbow-content-2026-09-24")
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
    r.add_header("User-Agent", "Mozilla/5.0 NadLan-RB-CONTENT/1.0")
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
    s, d = req("GET", "/wp-json/wp/v2/nadlan_project/%d?context=edit&_fields=id,modified_gmt,content" % PID)
    if s != 200:
        raise SystemExit("FATAL read %s %s" % (s, str(d)[:200]))
    return d


FIXES = [
    ('<div class="nadlan-guide__byline">עודכן ביוני 2026 · ', '<div class="nadlan-guide__byline">עודכן בספטמבר 2026 · '),
    ("לכן העמוד מציג מודל בחירה, אומדן מחיר לא מחייב כאשר יש מקור ציבורי, ושדות פנייה שמאפשרים לשמור את הקומה, היחידה, הכיוון, השטח והכוונה של המתעניין.",
     "לכן בעמוד אפשר לקרוא את המחירים המדווחים עם המקור והתאריך, לבחור קומה וכיוון במגדל ולראות את הנוף המשוער מהקומה, ולבקש בוואטסאפ תוכניות ומחירים לקומה ולכיוון שבחרתם."),
    ("<h2>למה המודל התלת ממדי חשוב לרוכשים וליזמים</h2>", "<h2>למה חשוב לראות את הקומה והכיוון לפני שפונים</h2>"),
    ("הוא מנסה להבין איפה הדירה יושבת במגדל, לאיזה כיוון היא פונה, מה רואים מהמרפסת, כמה אור יש, ומה השלב הבא אם זה מתאים. לכן תצוגת הפרויקט מחברת בין המודל, בחירת יחידה, אומדן לא מחייב, ליווי מקצועי ופנייה מסודרת.",
     "הוא מנסה להבין באיזה גובה הדירה, לאיזה כיוון היא פונה ומה רואים ממנה. לכן בראש העמוד יש סיור וירטואלי במגדל: בוחרים קומה ואחר כך נקודה בטבעת הקומה, ורואים את הנוף המשוער מהגובה ומהכיוון האלה ואת הכיוון על מפת האזור, מול הים, העיר והבניינים שמסביב."),
    ("<p>ליזם או מנהל שיווק, זה יוצר עמוד מכירה מדיד: כל לחיצה על דירה, צפייה במבט, בקשת תוכנית או בדיקת רכישה יכולה להפוך לפנייה מסודרת עם הקשר מלא, במקום להיעלם בשיחה שלא נשמרת.</p>",
     "<p>הסיור מבוסס על מקורות פומביים ועל מפה, והוא להמחשה בלבד: אינו תוכנית מכר ואינו צילום מהדירה. את הקומה והכיוון שבחרתם אפשר לשלוח בוואטסאפ, בבקשה לקבלת תוכניות ומחירים.</p>"),
    ("<p>מי שבודק דירות למכירה ב-Rainbow תל אביב יכול להשתמש במודל כדי להשוות קומה, כיוון, שטח ומבט, ואז לשלוח פנייה לבדיקה לא מחייבת של זמינות ומחיר מול היזם.</p>",
     "<p>מי שבודק דירות למכירה ב-Rainbow תל אביב יכול להשוות בסיור קומות וכיוונים ואת הנוף המשוער מכל אחד מהם, ואז לבקש תוכניות ומחירים לקומה ולכיוון שבחר.</p>"),
    ("<p>הגלריה בכרטיס זה כוללת הדמיות מקוריות שנוצרו לצורך המחשה בלבד. הן אינן תמונות רשמיות של היזם",
     "<p>ההדמיות בעמוד, כולל הסיור הווירטואלי, נוצרו לצורך המחשה בלבד. הן אינן תמונות רשמיות של היזם"),
]

d = read()
raw = d["content"]["raw"]
md5 = hashlib.md5(raw.encode("utf-8")).hexdigest()
print("[read] modified", d.get("modified_gmt"), "| md5", md5[:10], "| chars", len(raw))
new = raw
bad = False
for old, rep in FIXES:
    n = new.count(old)
    print("[fix] x%d  %s..." % (n, old[:60]))
    if n != 1:
        bad = True
        continue
    new = new.replace(old, rep)
print("[check] מודל left:", new.count("מודל"), "(one is the management model) | תלת ממד left:", new.count("תלת ממד"), "| בחירת יחידה left:", new.count("בחירת יחידה"))
if not APPLY:
    raise SystemExit(0)
if bad:
    raise SystemExit("FATAL: a fix does not match exactly once; nothing written")
os.makedirs(QA, exist_ok=True)
stamp = time.strftime("%Y%m%dT%H%M%S")
io.open(os.path.join(QA, "post-4464.raw.%s.before4.html" % stamp), "w", encoding="utf-8").write(raw)
d2 = read()
if hashlib.md5(d2["content"]["raw"].encode("utf-8")).hexdigest() != md5:
    raise SystemExit("FATAL: the content changed while we read it; nothing written")
s, r = req("POST", "/wp-json/wp/v2/nadlan_project/%d" % PID, {"content": new})
print("[write]", s)
d3 = read()
print("[verify] content as written:", d3["content"]["raw"] == new)
io.open(os.path.join(QA, "post-4464.raw.%s.after4.html" % stamp), "w", encoding="utf-8").write(d3["content"]["raw"])
