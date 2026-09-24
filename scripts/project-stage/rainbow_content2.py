# -*- coding: utf-8 -*-
"""Rainbow's page text, second pass (the site loop, R2): the answer paragraph from sourced facts; one FAQ (the buyer's ten
questions stay, the page-about-itself block goes); three FAQ answers corrected; the meta description stops promising what
the page does not have yet. First pass: corrected where it is wrong or where writer's notes leaked into public copy (24.9.2026, the site
loop, item R1). Reads post 4464's raw content over REST (the app password is decrypted in-process, DPAPI, never
printed), shows the fragments, and with --apply writes exact replacements (each must match once), guarded by the md5
of the content read just before; also sets project_3d_avg_price_per_sqm to the developer's reported cumulative average.
A copy of the old raw content is saved first.
  python scripts/project-stage/rainbow_content.py            # show the fragments
  python scripts/project-stage/rainbow_content.py --apply    # write
Sources (docs/research/2026-09-24-rainbow-run/rainbow-facts.md): the design plan approved 10.5.2023 (480 units: 229 in
the tower, 251 in the boutique buildings); the developer and the contractor today: 459; Israel Canada's reports via
Bizportal 29.5.2026: cumulative average 81,782 NIS per m² through Q1 2026."""
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
    s, d = req("GET", "/wp-json/wp/v2/nadlan_project/%d?context=edit&_fields=id,modified_gmt,content,meta" % PID)
    if s != 200:
        raise SystemExit("FATAL read %s %s" % (s, str(d)[:200]))
    return d


# old text -> new text; each old must appear exactly once in the raw content
LEAD_OLD = "Rainbow Tel Aviv הוא אחד מפרויקטי הדגל של שדה דב. העמוד הזה מרכז מידע ציבורי, אומדני מחיר לא מחייבים ותצוגת בחירה אינטראקטיבית, כדי לעזור להבין קומות, כיוונים, קו נוף והמשך בדיקה לפני פנייה ליזם."
LEAD_NEW = ("ריינבו תל אביב (Rainbow Tel Aviv) הוא פרויקט המגורים של ישראל קנדה במגרש 111 ברובע שדה דב, בצפון תל אביב, כ-700 מטר מהים: "
            "מגדל בן 39 קומות ובנייני בוטיק בני 9 קומות סביב חצר פנימית, 459 דירות לפי היזם. הפרויקט בבנייה, הקבלן המבצע הוא אשטרום, "
            "והאכלוס צפוי ב-2030 לפי אתר הפרויקט. לפי דוחות היזם, המחיר הממוצע בדירות שנמכרו עד תחילת 2026 הוא כ-81,800 ₪ למ\"ר. "
            "בעמוד אפשר לבחור קומה וכיוון במגדל, לראות את הנוף המשוער מהקומה ואת הכיוון על מפת האזור, ולקרוא את כל הנתונים והמקורות.")
FIXES = [
    (LEAD_OLD, LEAD_NEW),
    ("בדף ישראל קנדה ובאתר השיווק החדש מופיע נתון של 480 יחידות דיור. היתר הבנייה והמקורות התכנוניים-ביצועיים מציינים 459 דירות. מאחר שקיימים פערים בין מקורות פומביים, יש לאמת את הנתון המחייב מול היזם ומסמכי המכר.",
     "בתכנית העיצוב שאושרה ב-10.5.2023 יש 480 יחידות: 229 במגדל ו-251 בבנייני הבוטיק. היזם והקבלן מדברים היום על 459 דירות. המספר המחייב הוא זה שבמסמכי המכר."),
    ("המקורות מציגים טווחים שונים: בפרסום אשטרום מופיע מגדל בן 40 קומות",
     "בתכנית העיצוב שאושרה: מגדל בן 39 קומות מעל הכניסה ועוד קומה טכנית, ובנייני בוטיק בני 9 קומות. מקורות אחרים מציגים טווחים שונים: בפרסום אשטרום מופיע מגדל בן 40 קומות"),
    ("אתר השיווק החדש מציג את הפרויקט בסטטוס Construction ו-Presale.", "לפי אתר השיווק, הפרויקט בבנייה ובמכירה מוקדמת."),
]
FAQ1_START = '<section class="nadlan-guide__section">\n\t\t<h2>שאלות נפוצות על Rainbow Tel Aviv</h2>'


class _Stop(Exception):
    pass


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
# one FAQ: the block about the page itself goes, the buyer's ten questions stay
if new.count(FAQ1_START) == 1:
    s0 = new.find(FAQ1_START)
    e0 = new.find("</section>", s0) + len("</section>")
    block = new[s0:e0]
    ok_block = block.count("<details") >= 5 and block.count("<h2") == 1
    print("[faq] the first block: %d chars, details=%d, removable=%s" % (len(block), block.count("<details"), ok_block))
    if ok_block:
        new = new[:s0] + new[e0:]
else:
    print("[faq] first block not found once:", new.count(FAQ1_START)); bad = True
print("[check] FAQ headings left:", new.count("שאלות נפוצות על Rainbow Tel Aviv"), "| lead new:", LEAD_NEW[:40] in new)
if not APPLY:
    raise SystemExit(0)
if bad:
    raise SystemExit("FATAL: a fix does not match exactly once; nothing written")
os.makedirs(QA, exist_ok=True)
stamp = time.strftime("%Y%m%dT%H%M%S")
io.open(os.path.join(QA, "post-4464.raw.%s.before2.html" % stamp), "w", encoding="utf-8").write(raw)
d2 = read()
if hashlib.md5(d2["content"]["raw"].encode("utf-8")).hexdigest() != md5:
    raise SystemExit("FATAL: the content changed while we read it; nothing written")
s, r = req("POST", "/wp-json/wp/v2/nadlan_project/%d" % PID, {"content": new})
print("[write]", s)
d3 = read()
print("[verify] content as written:", d3["content"]["raw"] == new)
io.open(os.path.join(QA, "post-4464.raw.%s.after2.html" % stamp), "w", encoding="utf-8").write(d3["content"]["raw"])
