# -*- coding: utf-8 -*-
"""Read-only state check: post 7514 status/meta summary, media 7500-7513. No writes."""
import base64, ctypes, ctypes.wintypes, io, json, sys, urllib.request, urllib.error
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = "https://nad-lan.co.il"
SECRETS_PATH = r"C:\Users\777\Documents\websites\.codex-secrets\wordpress-app-passwords\nad-lan.co.il.json"

class DATA_BLOB(ctypes.Structure):
    _fields_ = [("cbData", ctypes.wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]

def dpapi_unprotect(b64):
    raw = base64.b64decode(b64)
    blob_in = DATA_BLOB(len(raw), ctypes.cast(ctypes.create_string_buffer(raw, len(raw)), ctypes.POINTER(ctypes.c_char)))
    blob_out = DATA_BLOB()
    if not ctypes.windll.crypt32.CryptUnprotectData(ctypes.byref(blob_in), None, None, None, None, 0, ctypes.byref(blob_out)):
        raise RuntimeError("DPAPI decrypt failed")
    try:
        return ctypes.string_at(blob_out.pbData, blob_out.cbData).decode("utf-8")
    finally:
        ctypes.windll.kernel32.LocalFree(blob_out.pbData)

with open(SECRETS_PATH, encoding="utf-8-sig") as f:
    sec = json.load(f)
AUTH = "Basic " + base64.b64encode(f"{sec['username']}:{dpapi_unprotect(sec['password_dpapi'])}".encode()).decode()

def get(path):
    pass
def call(method, path, body=None):
    r = urllib.request.Request(BASE + path, data=(json.dumps(body).encode() if body is not None else None), method=method)
    r.add_header("Authorization", AUTH); r.add_header("User-Agent", "Mozilla/5.0 NadLan-Check/1.0"); r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, timeout=60) as resp: return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e: return e.code, {"raw": e.read()[:200].decode("utf-8","replace")}
s, st = call("GET", "/wp-json/wp/v2/settings"); print("settings http", s, "| og default before:", (st or {}).get("nadlan_og_default_image"), "| site_icon:", (st or {}).get("site_icon"))
s2, st2 = call("POST", "/wp-json/wp/v2/settings", {"nadlan_og_default_image": "https://nad-lan.co.il/wp-content/uploads/2026/09/og-default-1200x630-1.jpg"})
print("update http", s2, "| og default after:", (st2 or {}).get("nadlan_og_default_image"))
