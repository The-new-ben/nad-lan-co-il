# -*- coding: utf-8 -*-
"""HAD-247 housekeeping: list, and with --delete remove, every temporary x-tmp-had247-ops-* Code Snippet.
A bridge left active after a failed run keeps a privileged route alive; this makes the cleanup explicit and verified.
The WordPress app password is decrypted in-process (DPAPI) and never printed."""
import base64, ctypes, ctypes.wintypes, io, json, sys, time, urllib.request, urllib.error
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = "https://nad-lan.co.il"
SECRETS_PATH = r"C:\Users\777\Documents\websites\.codex-secrets\wordpress-app-passwords\nad-lan.co.il.json"


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


sec = json.load(open(SECRETS_PATH, encoding="utf-8-sig"))
AUTH = "Basic " + base64.b64encode((sec["username"] + ":" + dpapi(sec["password_dpapi"])).encode()).decode()


def req(method, path, body=None):
    r = urllib.request.Request(BASE + path, data=None if body is None else json.dumps(body).encode(), method=method)
    r.add_header("Authorization", AUTH)
    r.add_header("User-Agent", "NadLan-HAD247-cleanup/1.0")
    if body is not None:
        r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, timeout=60) as resp:
            p = resp.read()
            return resp.status, json.loads(p.decode() or "null")
    except urllib.error.HTTPError as e:
        p = e.read()
        try:
            return e.code, json.loads(p.decode())
        except Exception:
            return e.code, {"raw": p[:200].decode("utf-8", "replace")}


s, lst = req("GET", "/wp-json/code-snippets/v1/snippets")
if s != 200:
    raise SystemExit(f"list failed: {s} {lst}")
mine = [x for x in lst if str(x.get("name", "")).startswith("x-tmp-had247-ops-")]
for x in mine:
    print("found", x["id"], x["name"], "active" if x.get("active") else "inactive")
if "--delete" in sys.argv:
    for x in mine:
        s1, _ = req("PUT", f"/wp-json/code-snippets/v1/snippets/{x['id']}/deactivate", {})
        s2, _ = req("DELETE", f"/wp-json/code-snippets/v1/snippets/{x['id']}")
        print("deactivate", s1, "delete", s2, "id", x["id"])
    time.sleep(2)
    s, lst = req("GET", "/wp-json/code-snippets/v1/snippets")
    left = [x for x in lst if str(x.get("name", "")).startswith("x-tmp-had247-ops-")]
    print("left after delete:", [(x["id"], "active" if x.get("active") else "inactive") for x in left])
    s3, _ = req("POST", "/wp-json/nadlan-had247-ops/v1/apply", {"token": "x"})
    print("bridge route now http", s3, "(want 404)")
