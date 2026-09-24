# -*- coding: utf-8 -*-
"""Rainbow's page text, corrected where it is wrong or where writer's notes leaked into public copy (24.9.2026, the site
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

# old text -> new text; each old must appear exactly once in the raw content
FIXES = [
    ("<strong>כ-480 לפי שיווק היזם</strong>", "<strong>459 דירות, לפי היזם</strong>"),
    ("<p>יש להציג בשקיפות גם את הפער מול נתוני היתר שפורסמו סביב 459 יחידות. אמת לפני שיווק.</p>",
     "<p>בתכנית העיצוב שאושרה ב-2023: 480 יחידות, 229 במגדל ו-251 בבנייני הבוטיק.</p>"),
    ("<strong>אומדן ציבורי בלבד</strong>", "<strong>כ-81,800 ₪ למ\"ר</strong>"),
    ("דיווחים ציבוריים הציגו עסקאות סביב עשרות אלפי שקלים למ\"ר, אך מחיר וזמינות מחייבים אישור יזם.",
     "הממוצע בדירות שנמכרו עד הרבעון הראשון של 2026, לפי דוחות היזם (ביזפורטל, 29.5.2026). מחיר וזמינות מחייבים אישור היזם."),
    # the lead extraction takes this paragraph to the top of the page and left the box with a bare label
    ("<strong>שורה תחתונה למשקיע ולרוכש:</strong>\n\t\t<p>", "<p>"),
    ("480 יחידות לפי שיווק היזם ואתר השיווק החדש. היתר הבנייה והמקורות התכנוניים-ביצועיים מציינים 459 דירות, ולכן יש לאמת את המספר המחייב מול היזם ומסמכי המכר.",
     "480 יחידות בתכנית העיצוב שאושרה ב-10.5.2023: 229 במגדל ו-251 בבנייני הבוטיק. היזם והקבלן מדברים היום על 459 דירות. את המספר המחייב בודקים מול מסמכי המכר."),
]


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


d = read()
raw = d["content"]["raw"]
md5 = hashlib.md5(raw.encode("utf-8")).hexdigest()
print("[read] modified", d.get("modified_gmt"), "| md5", md5[:10], "| chars", len(raw), "| ppsqm", (d.get("meta") or {}).get("project_3d_avg_price_per_sqm"))
new = raw
bad = False
for old, rep in FIXES:
    n = new.count(old)
    print("[fix] x%d  %s..." % (n, old[:60]))
    if n != 1:
        bad = True
        continue
    new = new.replace(old, rep)
# the note box held only the lead paragraph, which the page lifts to the top: unwrap it so no empty box is left behind
NOTE = '<div class="nadlan-guide__note">'
if not bad and new.count(NOTE) == 1:
    i = new.find(NOTE)
    j = new.find("</div>", i)
    inner = new[i + len(NOTE):j].strip()
    if inner.startswith("<p>") and inner.count("<p") == 1 and inner.endswith("</p>"):
        new = new[:i] + inner + new[j + len("</div>"):]
        print("[unwrap] the note box around the lead paragraph")
    else:
        print("[unwrap] skipped: the note box holds more than the lead")
for kw in ("שורה תחתונה למשקיע ולרוכש", "אמת לפני שיווק", "יש להציג בשקיפות", NOTE):
    i = new.find(kw)
    print("[left] %s: %s" % (kw, "none" if i < 0 else repr(new[max(0, i - 160):i + 220])))
if not APPLY:
    raise SystemExit(0)
if bad:
    raise SystemExit("FATAL: a fix does not match exactly once; nothing written")
os.makedirs(QA, exist_ok=True)
stamp = time.strftime("%Y%m%dT%H%M%S")
io.open(os.path.join(QA, "post-4464.raw.%s.before.html" % stamp), "w", encoding="utf-8").write(raw)
d2 = read()
if hashlib.md5(d2["content"]["raw"].encode("utf-8")).hexdigest() != md5:
    raise SystemExit("FATAL: the content changed while we read it; nothing written")
s, r = req("POST", "/wp-json/wp/v2/nadlan_project/%d" % PID, {"content": new, "meta": {"project_3d_avg_price_per_sqm": 81782}})
print("[write]", s, (r or {}).get("modified_gmt") if isinstance(r, dict) else r)
d3 = read()
ok = d3["content"]["raw"] == new
print("[verify] content as written:", ok, "| ppsqm now", (d3.get("meta") or {}).get("project_3d_avg_price_per_sqm"))
io.open(os.path.join(QA, "post-4464.raw.%s.after.html" % stamp), "w", encoding="utf-8").write(d3["content"]["raw"])
