# -*- coding: utf-8 -*-
"""Uploads a broker's rendered listings video (web size) and its posters to the WordPress media library (24.9.2026).

  python scripts/broker-video/upload_media.py <folder with the files> <broker slug> [--only poster]

Files expected in the folder: <slug>_1080x1920_web.mp4, <slug>_1920x1080_web.mp4, <slug>_1080x1920_poster.jpg,
<slug>_1920x1080_poster.jpg (the renderer's output names). They are uploaded as <slug>-listings-tall.mp4 and so on, so the
public file names carry no Hebrew. An upload whose name is already in the library is not repeated. Prints one JSON line
with the four URLs. The app password is decrypted in-process (DPAPI) and never printed.
"""
import base64, ctypes, ctypes.wintypes, io, json, os, sys, urllib.parse, urllib.request, urllib.error

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = "https://nad-lan.co.il"
SECRETS_PATH = r"C:\Users\777\Documents\websites\.codex-secrets\wordpress-app-passwords\nad-lan.co.il.json"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) NadLan-Media/1.0"


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


def call(method, path, data=None, headers=None, timeout=600):
    r = urllib.request.Request(BASE + path, data=data, method=method)
    r.add_header("Authorization", AUTH)
    r.add_header("User-Agent", UA)
    for k, v in (headers or {}).items():
        r.add_header(k, v)
    try:
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8") or "null")
    except urllib.error.HTTPError as e:
        body = e.read()[:400].decode("utf-8", "replace")
        return e.code, {"error": body}


def existing(name):
    # by the attachment's slug (made from the file name); a search looks at the title, which the upload renames
    # (24.9.2026: the search missed two posters and they were uploaded twice, ids 8097 and 8098)
    stem = os.path.splitext(name)[0]
    s, r = call("GET", "/wp-json/wp/v2/media?slug=" + urllib.parse.quote(stem) + "&_fields=id,source_url")
    for m in (r if s == 200 and isinstance(r, list) else []):
        if m["source_url"].rsplit("/", 1)[-1] == name:
            return m
    return None


def upload(path, name, mime, alt):
    have = existing(name)
    if have:
        print(f"[media] {name}: already there, id {have['id']}")
        return have
    data = open(path, "rb").read()
    s, r = call("POST", "/wp-json/wp/v2/media", data=data, headers={"Content-Type": mime, "Content-Disposition": f'attachment; filename="{name}"'})
    if s not in (200, 201):
        raise SystemExit(f"FATAL upload {name}: HTTP {s} {json.dumps(r, ensure_ascii=False)[:300]}")
    call("POST", f"/wp-json/wp/v2/media/{r['id']}", data=json.dumps({"alt_text": alt, "title": alt}).encode("utf-8"), headers={"Content-Type": "application/json"})
    print(f"[media] {name}: uploaded, id {r['id']}, {len(data)} bytes")
    return r


folder, slug = sys.argv[1], sys.argv[2]
only = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else ""
plan = [
    ("poster_tall", f"{slug}_1080x1920_poster.jpg", f"{slug}-listings-tall-poster.jpg", "image/jpeg"),
    ("poster_wide", f"{slug}_1920x1080_poster.jpg", f"{slug}-listings-wide-poster.jpg", "image/jpeg"),
    ("tall", f"{slug}_1080x1920_web.mp4", f"{slug}-listings-tall.mp4", "video/mp4"),
    ("wide", f"{slug}_1920x1080_web.mp4", f"{slug}-listings-wide.mp4", "video/mp4"),
]
out = {}
for key, src, name, mime in plan:
    if only and only not in key:
        continue
    m = upload(os.path.join(folder, src), name, mime, "סרטון הנכסים" if "poster" not in key else "סרטון הנכסים: תמונת פתיחה")
    out[key] = m["source_url"]
print(json.dumps(out, ensure_ascii=False))
