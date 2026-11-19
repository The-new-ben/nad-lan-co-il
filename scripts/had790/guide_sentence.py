# -*- coding: utf-8 -*-
"""HAD-790 item 7 (the film 19.11, gap 40): the buying guide /buying-apartment/ says of the site, in the line above the personal
plan tool, "האתר אינו משרד עורכי דין ואינו מתווך". The site never uses that word about itself (owner rule); the legal meaning stays
with "ואינו צד לעסקה" (not a party to the deal). One sentence in the page's post text, nothing else.

  python scripts/had790/guide_sentence.py            dry run: finds the page, proves the sentence is there once, writes nothing
  python scripts/had790/guide_sentence.py --go       backs up the raw post text, replaces the one sentence, reads it back
  python scripts/had790/guide_sentence.py --undo     restores the backup (only if the live text is still what --go wrote)

Credentials: the DPAPI-protected application password, decrypted here only, never printed."""
import base64, ctypes, ctypes.wintypes, hashlib, json, os, sys, time, urllib.request, urllib.error

BASE = "https://nad-lan.co.il"
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO, "docs", "qa", "had-790")
SECRETS_PATH = r"C:\Users\777\Documents\websites\.codex-secrets\wordpress-app-passwords\nad-lan.co.il.json"
OLD = "האתר אינו משרד עורכי דין ואינו מתווך;"
NEW = "האתר אינו משרד עורכי דין ואינו צד לעסקה;"
SLUG = "buying-apartment"


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
    _sec = json.load(f)
AUTH = "Basic " + base64.b64encode((_sec["username"] + ":" + dpapi(_sec["password_dpapi"])).encode()).decode()


def req(method, path, body=None):
    r = urllib.request.Request(BASE + path, data=None if body is None else json.dumps(body, ensure_ascii=False).encode(), method=method)
    r.add_header("Authorization", AUTH)
    r.add_header("User-Agent", "Mozilla/5.0 NadLan-HAD790/1.0")
    if body is not None:
        r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, timeout=90) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8") or "null")
    except urllib.error.HTTPError as e:
        return e.code, {"raw": e.read()[:300].decode("utf-8", "replace")}


md5 = lambda s: hashlib.md5(s.encode("utf-8")).hexdigest()


def page():
    s, p = req("GET", "/wp-json/wp/v2/pages?slug=%s&context=edit&_fields=id,status,content,modified" % SLUG)
    assert s == 200 and isinstance(p, list) and len(p) == 1, (s, str(p)[:200])
    return p[0]


def main():
    os.makedirs(OUT, exist_ok=True)
    p = page()
    pid, raw = p["id"], p["content"]["raw"]
    print("[page] %s id %d, %s, %d chars, md5 %s" % (SLUG, pid, p["status"], len(raw), md5(raw)[:10]))
    if "--undo" in sys.argv:
        res = json.load(open(os.path.join(OUT, "guide-sentence-result.json"), encoding="utf-8"))
        assert md5(raw) == res["after_md5"], "the live text is not what --go wrote; read it before undoing"
        old = open(os.path.join(OUT, res["backup"]), encoding="utf-8").read()
        s, r = req("POST", "/wp-json/wp/v2/pages/%d" % pid, {"content": old})
        assert s == 200, (s, r)
        print("[undo] restored", res["backup"])
        return
    n = raw.count(OLD)
    print("[check] the sentence with the word: %d time(s); the new wording already there: %d" % (n, raw.count(NEW)))
    assert n == 1, "want exactly one"
    if "--go" not in sys.argv:
        print("[dry] nothing written")
        return
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bk = "backup-%d-%s.html" % (pid, stamp)
    open(os.path.join(OUT, bk), "w", encoding="utf-8", newline="").write(raw)
    new = raw.replace(OLD, NEW)
    s, r = req("POST", "/wp-json/wp/v2/pages/%d" % pid, {"content": new})
    assert s == 200, (s, str(r)[:300])
    back = page()["content"]["raw"]
    ok = back == new
    res = {"page": pid, "slug": SLUG, "stamp": stamp, "backup": bk, "before_md5": md5(raw), "after_md5": md5(back), "read_back_equal": ok}
    json.dump(res, open(os.path.join(OUT, "guide-sentence-result.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("[go] written; read back equal: %s; backup %s" % (ok, bk))
    assert ok


if __name__ == "__main__":
    main()
