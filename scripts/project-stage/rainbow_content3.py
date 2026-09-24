# -*- coding: utf-8 -*-
"""Rainbow's page text, third pass (the site loop, R2): the second English status sentence that pass 2 did not reach
("סטטוס הפרויקט הוא Construction וסטטוס השיווק הוא Presale") is said in Hebrew. Same mechanism as rainbow_content2.py:
reads post 4464's raw content over REST (the app password is decrypted in-process, DPAPI, never printed), each fix must
match exactly once, guarded by the md5 of the content read just before, a copy of the old raw content is saved first.
  python scripts/project-stage/rainbow_content3.py            # show
  python scripts/project-stage/rainbow_content3.py --apply    # write"""
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
    ("לפי אתר השיווק החדש, סטטוס הפרויקט הוא Construction וסטטוס השיווק הוא Presale, עם אכלוס צפוי ב-2030.",
     "לפי אתר השיווק, הפרויקט בבנייה ובמכירה מוקדמת, והאכלוס צפוי ב-2030."),
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
print("[check] Construction left:", new.count("Construction"), "| Presale left:", new.count("Presale"))
if not APPLY:
    raise SystemExit(0)
if bad:
    raise SystemExit("FATAL: a fix does not match exactly once; nothing written")
os.makedirs(QA, exist_ok=True)
stamp = time.strftime("%Y%m%dT%H%M%S")
io.open(os.path.join(QA, "post-4464.raw.%s.before3.html" % stamp), "w", encoding="utf-8").write(raw)
d2 = read()
if hashlib.md5(d2["content"]["raw"].encode("utf-8")).hexdigest() != md5:
    raise SystemExit("FATAL: the content changed while we read it; nothing written")
s, r = req("POST", "/wp-json/wp/v2/nadlan_project/%d" % PID, {"content": new})
print("[write]", s)
d3 = read()
print("[verify] content as written:", d3["content"]["raw"] == new)
io.open(os.path.join(QA, "post-4464.raw.%s.after3.html" % stamp), "w", encoding="utf-8").write(d3["content"]["raw"])
