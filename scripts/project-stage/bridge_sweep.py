"""Lists the temporary release bridges (Code Snippets named x-tmp-*-ops-*) on nad-lan.co.il and deactivates and deletes any
that are still there. A runner stopped from outside (a shell timeout) cannot run its own bridge_down(); this closes it.
Nothing else is touched. Credentials are read only here, as in every runner, and never printed.
  python scripts/project-stage/bridge_sweep.py [--list]"""
import base64, ctypes, ctypes.wintypes, io, json, re, sys, urllib.request, urllib.error
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = "https://nad-lan.co.il"
SECRETS_PATH = r"C:\Users\777\Documents\websites\.codex-secrets\wordpress-app-passwords\nad-lan.co.il.json"
LIST_ONLY = "--list" in sys.argv[1:]


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


def snip(method, path, body=None):
    r = urllib.request.Request(BASE + "/wp-json/code-snippets/v1/snippets" + path, method=method,
                               data=None if body is None else json.dumps(body).encode())
    r.add_header("Authorization", AUTH); r.add_header("User-Agent", "Mozilla/5.0 NadLan-BridgeSweep/1.0")
    if body is not None:
        r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, timeout=60) as resp:
            p = resp.read(); return resp.status, json.loads(p.decode("utf-8") or "null")
    except urllib.error.HTTPError as e:
        return e.code, None


s, lst = snip("GET", "")
rows = [x for x in (lst if s == 200 and isinstance(lst, list) else []) if re.match(r"x-tmp-[a-z0-9]+-ops-", str(x.get("name", "")))]
print(f"[sweep] {len(rows)} temporary bridges found (http {s})")
for x in rows:
    print(f"  id {x['id']} active={bool(x.get('active'))} name={x['name']}")
    if LIST_ONLY:
        continue
    if x.get("active"):
        print("    deactivate:", snip("PUT", f"/{x['id']}/deactivate", {})[0])
    print("    delete:", snip("DELETE", f"/{x['id']}", None)[0])
