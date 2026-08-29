# -*- coding: utf-8 -*-
"""Replace contaminated photo heroes with the series plates on 6693/6694 (sketch-only law)."""
import base64, ctypes, ctypes.wintypes, io, json, secrets, sys, time, urllib.request, urllib.error
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = "https://nad-lan.co.il"
SECRETS_PATH = r"C:\Users\777\Documents\websites\.codex-secrets\wordpress-app-passwords\nad-lan.co.il.json"

class DB(ctypes.Structure):
    _fields_ = [("cb", ctypes.wintypes.DWORD), ("pb", ctypes.POINTER(ctypes.c_char))]

def dp(b):
    raw = base64.b64decode(b)
    bi = DB(len(raw), ctypes.cast(ctypes.create_string_buffer(raw, len(raw)), ctypes.POINTER(ctypes.c_char)))
    bo = DB()
    assert ctypes.windll.crypt32.CryptUnprotectData(ctypes.byref(bi), None, None, None, None, 0, ctypes.byref(bo))
    try:
        return ctypes.string_at(bo.pb, bo.cb).decode()
    finally:
        ctypes.windll.kernel32.LocalFree(bo.pb)

sec = json.load(open(SECRETS_PATH, encoding="utf-8-sig"))
AUTH = "Basic " + base64.b64encode((sec["username"] + ":" + dp(sec["password_dpapi"])).encode()).decode()

def req(method, path, body=None):
    r = urllib.request.Request(BASE + path, data=None if body is None else json.dumps(body, ensure_ascii=False).encode(), method=method)
    r.add_header("Authorization", AUTH)
    r.add_header("User-Agent", "NadLan-hero/1.0")
    if body is not None:
        r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, timeout=90) as resp:
            return resp.status, json.loads(resp.read().decode() or "null")
    except urllib.error.HTTPError as e:
        return e.code, {"raw": e.read()[:200].decode("utf-8", "replace")}

BNEI_PLATE = "https://nad-lan.co.il/wp-content/uploads/2026/08/bnei-dan-54-56-plate-capsules.jpg"
STRICKER_PLATE = "https://nad-lan.co.il/wp-content/uploads/2026/08/stricker-13-brandeis-14-plate-capsules.jpg"
TOKEN = secrets.token_hex(16)
CODE = (
    "add_action( 'rest_api_init', function () {\n"
    "\tregister_rest_route( 'nadlan-poster-fix/v1', '/go', array(\n"
    "\t\t'methods' => 'POST',\n"
    "\t\t'permission_callback' => function () { return current_user_can( 'manage_options' ); },\n"
    "\t\t'callback' => function ( $req ) {\n"
    "\t\t\t$b = $req->get_json_params();\n"
    "\t\t\tif ( ! is_array( $b ) || ! hash_equals( '" + TOKEN + "', (string) ( $b['token'] ?? '' ) ) ) { return new WP_Error( 'no', 'no', array( 'status' => 403 ) ); }\n"
    "\t\t\t$out = array();\n"
    "\t\t\tforeach ( array( 6693 => '" + BNEI_PLATE + "', 6694 => '" + STRICKER_PLATE + "' ) as $pid => $url ) {\n"
    "\t\t\t\t$out[ $pid ]['old_img'] = (string) get_post_meta( $pid, 'project_model_poster', true );\n"
    "\t\t\t\t$out[ $pid ]['old_poster'] = (string) get_post_meta( $pid, 'project_model_poster', true );\n"
    "\t\t\t\tupdate_post_meta( $pid, 'project_model_poster', esc_url_raw( $url ) );\n"
    "\t\t\t\t$out[ $pid ]['new'] = $url;\n"
    "\t\t\t}\n"
    "\t\t\tdo_action( 'litespeed_purge_all' );\n"
    "\t\t\treturn $out;\n"
    "\t\t},\n"
    "\t) );\n"
    "} );\n"
)
s, c = req("POST", "/wp-json/code-snippets/v1/snippets", {"name": f"tmp-hero-fix-{int(time.time())}", "code": CODE, "scope": "global", "active": False})
assert s in (200, 201), c
SID = c["id"]
s, a = req("PUT", f"/wp-json/code-snippets/v1/snippets/{SID}/activate", {})
assert s in (200, 201), a
s, r = req("POST", "/wp-json/nadlan-poster-fix/v1/go", {"token": TOKEN})
print("hero fix:", s, json.dumps(r, ensure_ascii=False)[:500])
s, d = req("DELETE", f"/wp-json/code-snippets/v1/snippets/{SID}", None)
print("bridge deleted:", s)
assert s == 204 and "6693" in json.dumps(r)
print("OK")

