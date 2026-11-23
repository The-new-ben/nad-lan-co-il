"""HAD-795, 23.11.2026: the rentals tutorial film (v2, 2:02) into the site's Media Library, so no heavy file rides in the plugin.
Uploads the two phone copies (Hebrew captions / English captions, burned in) and the poster from
D:\\Media\\NadLan-Films\\rentals-tutorial\\deliver\\ through the WordPress REST media endpoint (app password, decrypted here only,
never printed). Idempotent: a file whose slug is already in the library is not uploaded again. Writes the ids and addresses to
docs/rentals/build/film/media.json.   Usage: python scripts/rentals/upload_film_795.py
"""
import base64, ctypes, ctypes.wintypes, hashlib, io, json, os, sys, urllib.request, urllib.error
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", line_buffering=True)
BASE = "https://nad-lan.co.il"
REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
SRC = r"D:\Media\NadLan-Films\rentals-tutorial\deliver"
SECRETS_PATH = r"C:\Users\777\Documents\websites\.codex-secrets\wordpress-app-passwords\nad-lan.co.il.json"
FILES = [
    ("rentals-tutorial-he-phone.mp4", "video/mp4", "מדריך השכרות נדל״ן: אין מים חמים בדירה (עברית)"),
    ("rentals-tutorial-en-phone.mp4", "video/mp4", "NadLan Rentals tutorial: no hot water (English captions)"),
    ("rentals-tutorial-poster.webp", "image/webp", "מדריך השכרות נדל״ן: תמונת פתיחה"),
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
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) NadLan-PS464/1.0"


def call(method, path, data=None, headers=None, timeout=300):
    r = urllib.request.Request(BASE + path, data=data, method=method)
    r.add_header("Authorization", AUTH); r.add_header("User-Agent", UA)
    for k, v in (headers or {}).items():
        r.add_header(k, v)
    try:
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8") or "null")
    except urllib.error.HTTPError as e:
        return e.code, {"raw": e.read()[:300].decode("utf-8", "replace")}


out = {"uploaded_utc": None, "files": {}}
import datetime
for name, mime, title in FILES:
    data = open(os.path.join(SRC, name), "rb").read()
    slug = os.path.splitext(name)[0]
    s, found = call("GET", "/wp-json/wp/v2/media?slug=%s&context=edit&per_page=5" % slug)
    item = found[0] if s == 200 and isinstance(found, list) and found else None
    if item:
        print("already in the library:", name, item["id"])
    else:
        s, item = call("POST", "/wp-json/wp/v2/media", data, {"Content-Type": mime, "Content-Disposition": 'attachment; filename="%s"' % name})
        if s not in (200, 201):
            raise SystemExit("FATAL upload %s: HTTP %s %s" % (name, s, json.dumps(item, ensure_ascii=False)[:300]))
        call("POST", "/wp-json/wp/v2/media/%d" % item["id"], json.dumps({"title": title, "alt_text": "" if mime.startswith("video") else ""}).encode(), {"Content-Type": "application/json"})
        print("uploaded:", name, item["id"])
    url = item["source_url"]
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=300) as r:
        got = r.read()
    same = hashlib.md5(got).hexdigest() == hashlib.md5(data).hexdigest()
    print("  ", url, "bytes", len(got), "md5 same" if same else "MD5 DIFFERS")
    if not same:
        raise SystemExit("FATAL: the served file differs from the deliverable")
    out["files"][name] = {"id": item["id"], "url": url, "bytes": len(data), "md5": hashlib.md5(data).hexdigest()}
out["uploaded_utc"] = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
os.makedirs(os.path.join(REPO, "docs", "rentals", "build", "film"), exist_ok=True)
open(os.path.join(REPO, "docs", "rentals", "build", "film", "media.json"), "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1))
print("OK", len(out["files"]), "files")
