# -*- coding: utf-8 -*-
"""Press every OwnerMail button on the live site and prove each step (HAD-687).

  python tools/ownermail/press_buttons.py send            send a real lead card (the latest handled lead) and a sample morning mail to the owner
  python tools/ownermail/press_buttons.py press URL...    press the given action links (taken from the real mail), each: open (nothing may
                                                          change), confirm (the change is saved), undo (back to the start)
  python tools/ownermail/press_buttons.py press --lead N  the same with fresh links from the admin preview of lead N

The lead state is read through the admin preview after every step. The action links are pressed with no cookie and no login, as from a
mail app. The application password is decrypted here and never printed. POSTs are spaced 9 s apart (the site allows 8 a minute).
"""
import base64, ctypes, ctypes.wintypes, html, json, re, sys, time, urllib.parse, urllib.request

BASE = "https://nad-lan.co.il"
SECRETS_PATH = r"C:\Users\777\Documents\websites\.codex-secrets\wordpress-app-passwords\nad-lan.co.il.json"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) NadLan-OwnerMail-Test/1.0"


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


def call(method, url, body=None, auth=False):
    h = {"User-Agent": UA}
    if auth:
        h["Authorization"] = AUTH
    data = None
    if body is not None:
        data = json.dumps(body).encode() if auth else b""
        h["Content-Type"] = "application/json" if auth else "application/x-www-form-urlencoded"
    req = urllib.request.Request(url if url.startswith("http") else BASE + url, data=data, method=method, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")


def state(lid):
    s, b = call("GET", "/wp-json/nadlan/v1/om-lead-preview?l=%d" % lid, auth=True)
    j = json.loads(b)
    return {"status": j.get("status"), "snooze": j.get("snooze"), "mutes": sorted(k for k, t in (j.get("mutes") or {}).items() if int(t) > time.time())}, j


def title(page):
    m = re.search(r"<h1>(.*?)</h1>", page, re.S)
    return html.unescape(m.group(1)).strip() if m else "(no h1)"


def form_action(page):
    m = re.search(r'<form method="post" action="([^"]+)"', page)
    return html.unescape(m.group(1)) if m else None


def press(url, lid, start):
    q = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(url).query))
    a = q.get("a")
    ok = True
    s, page = call("GET", url)
    after_open, _ = state(lid)
    same = after_open == start
    print(f"  [{a}] open: HTTP {s} | '{title(page)}' | nothing changed: {same}")
    ok &= s == 200 and same and form_action(page) is not None
    s, page = call("POST", form_action(page))
    time.sleep(1)
    after, _ = state(lid)
    want = {"contacted": lambda x: x["status"] == "contacted", "lost": lambda x: x["status"] == "lost",
            "snooze": lambda x: bool(x["snooze"]), "mute": lambda x: q.get("k") in x["mutes"]}[a](after)
    print(f"  [{a}] confirm: HTTP {s} | '{title(page)}' | saved: {want} | state {after}")
    ok &= s == 200 and want
    undo = form_action(page)
    if undo:
        time.sleep(9)
        s, page = call("POST", undo)
        time.sleep(1)
        back, _ = state(lid)
        print(f"  [{a}] undo: HTTP {s} | '{title(page)}' | back to start: {back == start} | state {back}")
        ok &= s == 200 and back == start
    print(f"  [{a}] {'PASS' if ok else 'FAIL'}")
    time.sleep(9)
    return ok


def main():
    if sys.argv[1:2] == ["send"]:
        s, b = call("POST", "/wp-json/nadlan/v1/om-sample", {"which": "lead", "l": 0}, auth=True)
        print("lead card:", s, b[:200])
        s, b = call("POST", "/wp-json/nadlan/v1/om-sample", {"which": "morning"}, auth=True)
        print("morning sample:", s, b[:200])
        return
    args = sys.argv[2:]
    if args[:1] == ["--lead"]:
        lid = int(args[1])
        _, j = state(lid)
        urls = [html.unescape(u) for u in re.findall(r'href="([^"]*om-act[^"]*)"', j["html"])]
    else:
        urls = args
        lid = int(dict(urllib.parse.parse_qsl(urllib.parse.urlparse(next(u for u in urls if "&l=" in u and "l=0&" not in u)).query))["l"])
    urls = list(dict.fromkeys(urls))
    start, _ = state(lid)
    print("lead", lid, "start", start, "| buttons:", [dict(urllib.parse.parse_qsl(urllib.parse.urlparse(u).query)).get("a") for u in urls])
    res = [press(u, lid, start) for u in urls]
    end, _ = state(lid)
    print("RESULT", "ALL PASS" if all(res) else "FAILED", "| end state equals start:", end == start, end)


if __name__ == "__main__":
    main()
