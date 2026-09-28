# -*- coding: utf-8 -*-
"""The Somail projects on their official lots (design system ProjectMap v75, 28.9.2026). The research of 28.9
(docs/research/2026-09-28-stages/stage-geometry.md, the city's GIS lot layer 837 and permit layer 772) found:
  - H Infinity's pin 154 m off (32.086, 34.7821, an address guess); its address "the Jabotinsky corner" is lot 121, Hagag's
    other lot; H Infinity is lot 124, Ibn Gabirol 128; 53 floors by the amended permit (the page said 52);
  - its text had the streets reversed (Ibn Gabirol is WEST of the compound, Arlozorov SOUTH, Jabotinsky NORTH), distances
    measured from the wrong point, and "DUO 510 apartments" (668 by permit; 510 is the partners' marketable share);
  - DUO's pin 118 m off (32.0847, 34.7824) and its four language pages about 190 m off (32.084, 34.783).
Writes lat/lng/address/num_floors (meta) for H Infinity and the five DUO pages, and H Infinity's text fixes. Same mechanism
as rainbow_content4.py: the app password is decrypted in-process (DPAPI), never printed; each text fix must match exactly
once, guarded by the md5 of the content read just before; the old values and the old raw content are saved first.
  python scripts/project-stage/somail_locations.py            # show
  python scripts/project-stage/somail_locations.py --apply    # write"""
import base64, ctypes, ctypes.wintypes, hashlib, io, json, os, sys, time, urllib.request, urllib.error
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = "https://nad-lan.co.il"
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
    r.add_header("User-Agent", "Mozilla/5.0 NadLan-SOMAIL-LOC/1.0")
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



# the official lot centres (city GIS lot layer 837; docs/research/2026-09-28-stages/stage-geometry.md)
HINF = 6548
DUO_IDS = (4893, 5194, 5195, 5196, 5197)
META = {
    HINF: {"lat": 32.087284, "lng": 34.78272, "address": "אבן גבירול 128, מתחם סומייל", "num_floors": 53},
    4893: {"lat": 32.085698, "lng": 34.782856, "address": "אבן גבירול פינת ארלוזורוב, מתחם סומייל", "num_floors": 54},
}
for _i in DUO_IDS[1:]:
    META[_i] = {"lat": 32.085698, "lng": 34.782856, "address": "אבן גבירול פינת ארלוזורוב, מתחם סומייל"}

# H Infinity's text: where it stands and what surrounds it, from the corrected point
TEXT = [
    ("בין אבן גבירול לז'בוטינסקי, צמוד לכיכר רבין, לעירייה ולשתי תחנות רכבת קלה עתידיות בתוך המתחם. ",
     "ברחוב אבן גבירול 128, בין ארלוזורוב לז'בוטינסקי, קרוב לכיכר רבין ולבניין העירייה, ושתי תחנות רכבת קלה עתידיות בתוך המתחם. "),
    ("בין ארבעה רחובות מרכזיים: אבן גבירול ממזרח, ז'בוטינסקי מדרום, בן גוריון בהמשך הציר, וארלוזורוב מצפון.",
     "בין שלושה רחובות מרכזיים: אבן גבירול ממערב, ארלוזורוב מדרום וז'בוטינסקי מצפון. H Infinity עומד בחלקו הצפוני של המתחם."),
    ("כיכר רבין ובניין עיריית תל אביב כ-450 מטר דרומה - הלב האזרחי של העיר.",
     "כיכר רבין ובניין עיריית תל אביב כ-700 מטר דרומה - הלב האזרחי של העיר."),
    ("המרכז הרפואי איכילוב כ-900 מטר דרומית-מזרחית. פארק הירקון כ-800 מטר צפונה.",
     "המרכז הרפואי איכילוב כקילומטר דרומית-מזרחית. פארק הירקון צפונה, בהמשך אבן גבירול."),
    ("ובתוך המתחם עצמו: מגדלי DUO של אפריקה ישראל - 510 דירות בשני מגדלים שכבר בבנייה.",
     "ובתוך המתחם עצמו, בחלקו הדרומי: מגדלי DUO של אפריקה ישראל - 668 דירות בשני מגדלים, לפי היתר הבנייה."),
    ("<tr><th>המגרש</th><td>3,167 מ\"ר בחלק הצפוני של מתחם סומייל (גוש 6213, חלקה 1493). החברה רכשה אותו ב-2015.<small>הדוח השנתי 2025</small></td></tr>",
     "<tr><th>המגרש</th><td>3,167 מ\"ר ברחוב אבן גבירול 128, בחלק הצפוני של מתחם סומייל (גוש 6213, חלקה 1493). החברה רכשה אותו ב-2015."
     "<small>הדוח השנתי 2025. הכתובת: מאגר ההיתרים של עיריית תל אביב.</small></td></tr>"),
    ("<li><a href=\"https://www.globes.co.il/news/article.aspx?did=1001392692\" rel=\"nofollow noopener\">גלובס, 30.11.2021: סומייל הופך לפרויקט יזמי</a></li>",
     "<li><a href=\"https://www.globes.co.il/news/article.aspx?did=1001392692\" rel=\"nofollow noopener\">גלובס, 30.11.2021: סומייל הופך לפרויקט יזמי</a></li>"
     "<li><a href=\"https://gisn.tel-aviv.gov.il/iview2js4/index.aspx\" rel=\"nofollow noopener\">עיריית תל אביב: מפת המגרשים וההיתרים (GIS)</a></li>"),
]


def fix_text(raw):
    new = raw
    bad = []
    for old, rep in TEXT:
        n = new.count(old)
        print("[fix] x%d  %s..." % (n, old[:60]))
        if n != 1:
            bad.append(old[:60])
            continue
        new = new.replace(old, rep)
    return new, bad


def read(pid):
    s, d = req("GET", "/wp-json/wp/v2/nadlan_project/%d?context=edit&_fields=id,slug,modified_gmt,content,meta" % pid)
    if s != 200:
        raise SystemExit("FATAL read %s %s %s" % (pid, s, str(d)[:200]))
    return d


before = {}
for pid, want in META.items():
    d = read(pid)
    m = d.get("meta") or {}
    before[pid] = {k: m.get(k) for k in want}
    print("[meta] %d %s | %s -> %s" % (pid, d["slug"], json.dumps(before[pid], ensure_ascii=False), json.dumps(want, ensure_ascii=False)))
    missing = [k for k in want if k not in m]
    if missing:
        raise SystemExit("FATAL: meta not in REST for %d: %s" % (pid, missing))
h = read(HINF)
raw = h["content"]["raw"]
md5 = hashlib.md5(raw.encode("utf-8")).hexdigest()
new, bad = fix_text(raw)
print("[check] 510:", new.count("510"), "| ממזרח, ז'בוטינסקי מדרום:", new.count("ממזרח, ז'בוטינסקי מדרום"), "| 668:", new.count("668"))
if not APPLY:
    raise SystemExit(0)
if bad:
    raise SystemExit("FATAL: %s; nothing written" % bad)
os.makedirs(QA, exist_ok=True)
stamp = time.strftime("%Y%m%dT%H%M%S")
io.open(os.path.join(QA, "somail-meta.%s.before.json" % stamp), "w", encoding="utf-8").write(json.dumps(before, ensure_ascii=False, indent=1))
io.open(os.path.join(QA, "post-6548.raw.%s.before-loc.html" % stamp), "w", encoding="utf-8").write(raw)
if hashlib.md5(read(HINF)["content"]["raw"].encode("utf-8")).hexdigest() != md5:
    raise SystemExit("FATAL: the content changed while we read it; nothing written")
for pid, want in META.items():
    payload = {"meta": want}
    if pid == HINF:
        payload["content"] = new
    s, r = req("POST", "/wp-json/wp/v2/nadlan_project/%d" % pid, payload)
    d = read(pid)
    m = d.get("meta") or {}
    ok = all((abs(float(m.get(k) or 0) - v) < 1e-7) if isinstance(v, (int, float)) else (m.get(k) == v) for k, v in want.items()) and (pid != HINF or d["content"]["raw"] == new)
    print("[write] %d http %s | verified %s" % (pid, s, ok))
    if not ok:
        raise SystemExit("FATAL: %d not as written" % pid)
io.open(os.path.join(QA, "post-6548.raw.%s.after-loc.html" % stamp), "w", encoding="utf-8").write(new)
print("done")
