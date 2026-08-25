# -*- coding: utf-8 -*-
"""Micro-fix: update x-aurelia-experience snippet (id 601) with the corrected tour back-link param."""
import base64, ctypes, ctypes.wintypes, hashlib, io, json, os, re, sys, urllib.request, urllib.error
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = "https://nad-lan.co.il"
HERE = os.path.dirname(os.path.abspath(__file__))
SECRETS_PATH = r"C:\Users\777\Documents\websites\.codex-secrets\wordpress-app-passwords\nad-lan.co.il.json"

class DATA_BLOB(ctypes.Structure):
    _fields_ = [("cbData", ctypes.wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]

def dpapi(b64):
    raw = base64.b64decode(b64)
    bi = DATA_BLOB(len(raw), ctypes.cast(ctypes.create_string_buffer(raw, len(raw)), ctypes.POINTER(ctypes.c_char)))
    bo = DATA_BLOB()
    if not ctypes.windll.crypt32.CryptUnprotectData(ctypes.byref(bi), None, None, None, None, 0, ctypes.byref(bo)):
        raise RuntimeError("dpapi")
    try:
        return ctypes.string_at(bo.pbData, bo.cbData).decode("utf-8")
    finally:
        ctypes.windll.kernel32.LocalFree(bo.pbData)

sec = json.load(open(SECRETS_PATH, encoding="utf-8-sig"))
AUTH = "Basic " + base64.b64encode(f"{sec['username']}:{dpapi(sec['password_dpapi'])}".encode()).decode()

def req(method, path, body=None):
    r = urllib.request.Request(BASE + path, data=None if body is None else json.dumps(body, ensure_ascii=False).encode(), method=method)
    r.add_header("Authorization", AUTH)
    r.add_header("User-Agent", "NadLan-Aurelia-Fix/1.0")
    if body is not None:
        r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, timeout=90) as resp:
            return resp.status, json.loads(resp.read().decode() or "null")
    except urllib.error.HTTPError as e:
        return e.code, {"raw": e.read()[:300].decode("utf-8", "replace")}

with open(os.path.join(HERE, "deploy100-evidence.json"), encoding="utf-8") as f:
    ev = json.load(f)
SNIP = ev["experience_snippet_id"]
POST_ID = ev["post_id"]
PANO = ev["media"]["aurelia-living-panorama-360.jpg"]

with open(os.path.join(HERE, "snippet_experience.php"), encoding="utf-8") as f:
    code = f.read().replace("{{POST_ID}}", str(POST_ID)).replace("{{PANO_LIVING_URL}}", PANO)
code = re.sub(r"^<\?php\s*", "", code, count=1)

s, cur = req("GET", f"/wp-json/code-snippets/v1/snippets/{SNIP}")
assert s == 200, cur
s, upd = req("PUT", f"/wp-json/code-snippets/v1/snippets/{SNIP}", {"name": "x-aurelia-experience", "code": code, "scope": "global", "active": True})
print("update:", s, "active:", (upd or {}).get("active"))
s, after = req("GET", f"/wp-json/code-snippets/v1/snippets/{SNIP}")
print("verify active:", after.get("active"), "len:", len(after.get("code", "")), "sha:", hashlib.sha256(after.get("code", "").encode()).hexdigest()[:16])
assert after.get("active") is True and "?unit=" in after.get("code", "")
s, t = req("GET", "/projects/aurelia/?aurelia_tour=aur-t-14-c")
print("tour probe:", s)
print("OK")
