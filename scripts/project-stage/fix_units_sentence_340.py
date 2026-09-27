# -*- coding: utf-8 -*-
"""Linear HAD-340 (28.9.2026, the owner: "don't wait"): one sentence of Rainbow's article inverted the sources on the unit
count. 459 is the developer's current number; 480 is the design plan of 10.5.2023 (229 + 251). The sentence alone is
replaced; the raw content is backed up first. The app password is decrypted in-process (DPAPI), never printed.
  python scripts/project-stage/fix_units_sentence_340.py [--dry]
"""
import base64, ctypes, ctypes.wintypes, hashlib, io, json, os, re, secrets, subprocess, sys, tempfile, time, urllib.request, urllib.error, zlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = "https://nad-lan.co.il"
REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
SECRETS_PATH = r"C:\Users\777\Documents\websites\.codex-secrets\wordpress-app-passwords\nad-lan.co.il.json"
ARGS = sys.argv[1:]
DRY = "--dry" in ARGS
CRLF, LF = bytes([13, 10]), bytes([10])


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
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) NadLan-Units340/1.0"


def req(method, path, body=None, timeout=120, raw=False, auth=True):
    r = urllib.request.Request(BASE + path, data=None if body is None else json.dumps(body, ensure_ascii=False).encode(), method=method)
    if auth:
        r.add_header("Authorization", AUTH)
    r.add_header("User-Agent", UA)
    if body is not None:
        r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            p = resp.read()
            return resp.status, (p if raw else json.loads(p.decode("utf-8") or "null"))
    except urllib.error.HTTPError as e:
        p = e.read()
        if raw:
            return e.code, p
        try:
            return e.code, json.loads(p.decode("utf-8"))
        except Exception:
            return e.code, {"raw": p[:300].decode("utf-8", "replace")}


def must(s, p, what, ok=(200, 201)):
    if s not in ok:
        raise SystemExit(f"FATAL {what}: HTTP {s}: {json.dumps(p, ensure_ascii=False)[:400]}")
    return p



def md5(b):
    return hashlib.md5(b).hexdigest()


PID = 4464  # Rainbow Tel Aviv (Hebrew)
OLD = "מספר היחידות עומד על 480 לפי שיווק היזם ואתר השיווק החדש, בעוד שהיתר הבנייה והמקורות התכנוניים-ביצועיים מציינים 459 דירות"
NEW = "לפי היזם ואשטרום, בפרויקט 459 דירות; בתכנית העיצוב שאושרה ב-10.5.2023 היו 480 יחידות (229 במגדל ו-251 בבנייני הבוטיק)"
s, p = req("GET", f"/wp-json/wp/v2/nadlan_project/{PID}?context=edit&_fields=id,slug,content,modified")
p = must(s, p, "read the post")
raw = p["content"]["raw"]
n = raw.count(OLD)
print(f"[read] {p['slug']} modified {p['modified']}; the sentence x{n}; {len(raw)} chars")
if n != 1:
    raise SystemExit("FATAL the sentence is not there exactly once; nothing changed")
os.makedirs(os.path.join(QA, "live-backup"), exist_ok=True)
stamp = time.strftime("%Y%m%dT%H%M%S")
bk = os.path.join(QA, "live-backup", f"post-{PID}-content.{stamp}.html")
open(bk, "w", encoding="utf-8").write(raw)
print("[backup]", bk, md5(raw.encode()))
if DRY:
    raise SystemExit("[dry] no writes")
new_raw = raw.replace(OLD, NEW)
s, q = req("POST", f"/wp-json/wp/v2/nadlan_project/{PID}", {"content": new_raw})
q = must(s, q, "update the post")
s, v = req("GET", f"/wp-json/wp/v2/nadlan_project/{PID}?context=edit&_fields=content")
v = must(s, v, "read back")
ok = v["content"]["raw"] == new_raw
print("[verify raw]", ok)
st, html = req("GET", "/projects/rainbow-tel-aviv/?u340=%d" % time.time(), raw=True, auth=False)
h = html.decode("utf-8", "replace")
print("[verify page]", st, "new" if NEW in h else "NEW MISSING", "old" if OLD in h else "old gone")
