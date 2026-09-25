# -*- coding: utf-8 -*-
"""Read-only: fetch the live Code Snippets that carry site code (x-skin-a, x-catalog-plus, ...) and the live skin
stylesheet, and compare them with the repo's sources (HAD-300). Writes nothing on the site. The app password is
decrypted in-process (DPAPI), never printed.  python scripts/skin-a/pull_live_snippets.py [--write]"""
import base64, ctypes, ctypes.wintypes, hashlib, io, json, os, sys, urllib.request, urllib.error
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = "https://nad-lan.co.il"
REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
SECRETS_PATH = r"C:\Users\777\Documents\websites\.codex-secrets\wordpress-app-passwords\nad-lan.co.il.json"
WRITE = "--write" in sys.argv
class DB(ctypes.Structure):
    _fields_ = [("cb", ctypes.wintypes.DWORD), ("pb", ctypes.POINTER(ctypes.c_char))]
def dpapi(b64):
    raw = base64.b64decode(b64); bi = DB(len(raw), ctypes.cast(ctypes.create_string_buffer(raw, len(raw)), ctypes.POINTER(ctypes.c_char))); bo = DB()
    if not ctypes.windll.crypt32.CryptUnprotectData(ctypes.byref(bi), None, None, None, None, 0, ctypes.byref(bo)): raise RuntimeError("DPAPI")
    try: return ctypes.string_at(bo.pb, bo.cb).decode("utf-8")
    finally: ctypes.windll.kernel32.LocalFree(bo.pb)
with open(SECRETS_PATH, encoding="utf-8-sig") as f: sec = json.load(f)
AUTH = "Basic " + base64.b64encode((sec["username"] + ":" + dpapi(sec["password_dpapi"])).encode()).decode()
def get(path, auth=True):
    r = urllib.request.Request(BASE + path, headers={"User-Agent": "Mozilla/5.0 NadLan-Pull/1.0"})
    if auth: r.add_header("Authorization", AUTH)
    with urllib.request.urlopen(r, timeout=90) as resp: return resp.read()
lst = []
for page in range(1, 20):  # the list is paged (100 a page) and holds hundreds of old temporary bridges
    try:
        d = json.loads(get(f"/wp-json/code-snippets/v1/snippets?per_page=100&page={page}").decode("utf-8"))
    except urllib.error.HTTPError:
        break
    if not d:
        break
    lst += d
live = [x for x in lst if x.get("active") and not str(x.get("name", "")).startswith("x-tmp-")]
print("active snippets:", [(x["id"], x["name"]) for x in live])
MAP = {"x-skin-a": "plugins/nadlan-config/inc/skin-a.php", "x-catalog-plus": "plugins/nadlan-config/inc/catalog-plus.php", "x-catalog-plus-map": "plugins/nadlan-config/inc/catalog-plus-map.php"}
norm = lambda b: b.replace(b"\r\n", b"\n").strip()
for x in live:
    rel = MAP.get(x["name"])
    code = x.get("code", "").encode("utf-8")
    if not rel:
        continue
    p = os.path.join(REPO, *rel.split("/"))
    loc = open(p, "rb").read() if os.path.exists(p) else b""
    loc_body = norm(loc[5:] if loc.startswith(b"<?php") else loc)
    same = norm(code) == loc_body
    print(f"[{x['name']} #{x['id']}] live {len(code)} b md5 {hashlib.md5(norm(code)).hexdigest()[:10]} | repo {rel} {len(loc)} b md5 {hashlib.md5(loc_body).hexdigest()[:10]} -> {'SAME' if same else 'DIFFERENT'}")
    if WRITE and not same:
        open(p + ".live", "wb").write(b"<?php\n" + code.replace(b"\r\n", b"\n") + b"\n"); print("   wrote", rel + ".live")
css = get("/wp-content/uploads/nadlan-skin/skin-a.css?pull=1", auth=False)
lc = open(os.path.join(REPO, "assets", "skin-a", "skin-a.css"), "rb").read()
print(f"[skin-a.css] live {len(css)} b md5 {hashlib.md5(norm(css)).hexdigest()[:10]} | repo {len(lc)} b md5 {hashlib.md5(norm(lc)).hexdigest()[:10]} -> {'SAME' if norm(css) == norm(lc) else 'DIFFERENT'}")
if WRITE and norm(css) != norm(lc):
    open(os.path.join(REPO, "assets", "skin-a", "skin-a.css.live"), "wb").write(css); print("   wrote assets/skin-a/skin-a.css.live")
