# -*- coding: utf-8 -*-
"""T3: Echo City rebuild goes live on page 6695 via the x-echo-city snippet."""
import base64, ctypes, ctypes.wintypes, hashlib, io, json, os, re, secrets, sys, time, urllib.request, urllib.error
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

def req(method, path, body=None, ctype="application/json", extra=None, timeout=120, raw=False):
    r = urllib.request.Request(BASE + path, data=None if body is None else (body if isinstance(body, (bytes, bytearray)) else json.dumps(body, ensure_ascii=False).encode()), method=method)
    r.add_header("Authorization", AUTH)
    r.add_header("User-Agent", "NadLan-T3/1.0")
    if body is not None:
        r.add_header("Content-Type", ctype)
    for k, v in (extra or {}).items():
        r.add_header(k, v)
    try:
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            payload = resp.read()
            return resp.status, payload if raw else json.loads(payload.decode("utf-8") or "null")
    except urllib.error.HTTPError as e:
        p = e.read()
        try:
            return e.code, json.loads(p.decode("utf-8"))
        except Exception:
            return e.code, {"raw": p[:300].decode("utf-8", "replace")}

def must(s, p, what, ok=(200, 201)):
    if s not in ok:
        raise SystemExit(f"FATAL {what}: HTTP {s}: {json.dumps(p, ensure_ascii=False)[:400]}")
    return p

# 1. og image upload
og = open(os.path.join(HERE, "echo-city-og.jpg"), "rb").read()
s, m = req("POST", "/wp-json/wp/v2/media", body=og, ctype="image/jpeg",
           extra={"Content-Disposition": 'attachment; filename="echo-city-og-1200x630.jpg"'}, timeout=180)
must(s, m, "og upload")
OG_URL = m["source_url"]
req("POST", f"/wp-json/wp/v2/media/{m['id']}", body={"alt_text": "אקו סיטי תל אביב - הדמיה להמחשה", "title": "echo-city-og"})
print("[og]", m["id"], OG_URL)

# 2. final html
html = open(os.path.join(HERE, "echo-city-live.html"), encoding="utf-8").read().replace("__OG_URL__", OG_URL)
assert "__OG_URL__" not in html and "\u2014" not in html
print("[html]", len(html), "chars")

# 3. snippet: serve page 6695
marker = "NL_ECHO_HTML_" + secrets.token_hex(4)
code = (
    "/* x-echo-city v1.0 (27.8.2026, T3): the approved Echo City situation-room page\n"
    " * serves page 6695 (/echo-city/) in full. Rollback: deactivate this snippet\n"
    " * (?nl_old=1 previews the original WP page while active). */\n"
    "if ( ! function_exists( 'nadlan_echo_city_takeover' ) ) {\n"
    "\tfunction nadlan_echo_city_takeover() {\n"
    "\t\tif ( is_admin() || ! is_page( 6695 ) || isset( $_GET['nl_old'] ) || isset( $_GET['preview'] ) ) { return; }\n"
    "\t\tstatus_header( 200 );\n"
    "\t\theader( 'Content-Type: text/html; charset=UTF-8' );\n"
    "\t\techo <<<'" + marker + "'\n"
    + html + "\n"
    + marker + ";\n"
    "\t\texit;\n"
    "\t}\n"
    "\tadd_action( 'template_redirect', 'nadlan_echo_city_takeover', -50 );\n"
    "}\n"
)

def snip(method, path, body=None):
    return req(method, f"/wp-json/code-snippets/v1/snippets{path}", body=body)

s, created = snip("POST", "", {"name": "x-echo-city", "code": "/* placeholder */", "scope": "global", "active": False})
must(s, created, "snippet create")
SNIP = created["id"]
must(*snip("PUT", f"/{SNIP}", {"name": "x-echo-city", "code": code, "scope": "global", "active": False}), "snippet code")
s, got = snip("GET", f"/{SNIP}")
assert got.get("code", "").strip() == code.strip(), "snippet code mismatch after write"
must(*snip("PUT", f"/{SNIP}/activate", {}), "snippet activate")
print("[snippet]", SNIP, "sha", hashlib.sha256(code.encode()).hexdigest()[:16])

# 4. purge via a short-lived bridge action (reuse lite: create+use+delete)
TOKEN = secrets.token_hex(16)
purge_code = (
    "add_action( 'rest_api_init', function () {\n"
    "\tregister_rest_route( 'nadlan-t3-purge/v1', '/go', array(\n"
    "\t\t'methods' => 'POST',\n"
    "\t\t'permission_callback' => function () { return current_user_can( 'manage_options' ); },\n"
    "\t\t'callback' => function ( $req ) {\n"
    "\t\t\t$b = $req->get_json_params();\n"
    "\t\t\tif ( ! is_array( $b ) || ! hash_equals( '" + TOKEN + "', (string) ( isset( $b['token'] ) ? $b['token'] : '' ) ) ) { return new WP_Error( 'no', 'no', array( 'status' => 403 ) ); }\n"
    "\t\t\tdo_action( 'litespeed_purge_all' );\n"
    "\t\t\treturn array( 'purged' => 1 );\n"
    "\t\t},\n"
    "\t) );\n"
    "} );\n"
)
s, pc = snip("POST", "", {"name": f"tmp-t3-purge-{int(time.time())}", "code": purge_code, "scope": "global", "active": False})
must(s, pc, "purge bridge create")
PB = pc["id"]
must(*snip("PUT", f"/{PB}/activate", {}), "purge bridge activate")
must(*req("POST", "/wp-json/nadlan-t3-purge/v1/go", body={"token": TOKEN}), "purge")
s, d = snip("DELETE", f"/{PB}", None)
print("[purge-bridge-delete]", s)

# 5. verify
time.sleep(2)
s, page = req("GET", "/echo-city/", raw=True)
h = page.decode("utf-8", "replace")
title = (re.search(r"<title>(.*?)</title>", h, re.S) or [None, ""])[1]
print("[verify] http", s, "| bytes", len(page), "| h1", len(re.findall(r"<h1", h)),
      "| title:", title[:80], "| og:", OG_URL.split("/")[-1] in h, "| lead-js:", "nl-echo-lead" in h,
      "| plates:", h.count("plate-capsules.jpg"), "| emdash:", "\u2014" in h)
s2, old = req("GET", "/echo-city/?nl_old=1", raw=True)
print("[old-escape] http", s2, "| bytes", len(old), "| is-old:", b"nl-echo-lead" not in old)
s3, h3 = req("GET", "/wp-json/nadlan/v1/health")
print("[health]", h3.get("version"), h3.get("status"))
print("T3 DONE snippet", SNIP)
