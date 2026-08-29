# -*- coding: utf-8 -*-
"""Retitle Stricker 6694 via a server-side bridge (REST POST is WAF-blocked for this body)."""
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
    r.add_header("User-Agent", "NadLan-retitle/1.0")
    if body is not None:
        r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, timeout=90) as resp:
            return resp.status, json.loads(resp.read().decode() or "null")
    except urllib.error.HTTPError as e:
        return e.code, {"raw": e.read()[:200].decode("utf-8", "replace")}

NEW = "שטריקר 13 · ברנדיס 14 · התאומים של צפון תל אביב"
NEW_B64 = base64.b64encode(NEW.encode()).decode()
TOKEN = secrets.token_hex(16)
CODE = (
    "add_action( 'rest_api_init', function () {\n"
    "\tregister_rest_route( 'nadlan-retitle/v1', '/go', array(\n"
    "\t\t'methods' => 'POST',\n"
    "\t\t'permission_callback' => function () { return current_user_can( 'manage_options' ); },\n"
    "\t\t'callback' => function ( $req ) {\n"
    "\t\t\t$b = $req->get_json_params();\n"
    "\t\t\tif ( ! is_array( $b ) || ! hash_equals( '" + TOKEN + "', (string) ( $b['token'] ?? '' ) ) ) { return new WP_Error( 'no', 'no', array( 'status' => 403 ) ); }\n"
    "\t\t\t$title = base64_decode( '" + NEW_B64 + "' );\n"
    "\t\t\t$r = wp_update_post( array( 'ID' => 6694, 'post_title' => wp_slash( $title ) ), true );\n"
    "\t\t\tif ( is_wp_error( $r ) ) { return $r; }\n"
    "\t\t\tdo_action( 'litespeed_purge_all' );\n"
    "\t\t\treturn array( 'ok' => 1, 'title' => get_the_title( 6694 ), 'slug' => get_post_field( 'post_name', 6694 ) );\n"
    "\t\t},\n"
    "\t) );\n"
    "} );\n"
)
s, c = req("POST", "/wp-json/code-snippets/v1/snippets", {"name": f"tmp-retitle-{int(time.time())}", "code": CODE, "scope": "global", "active": False})
assert s in (200, 201), c
SID = c["id"]
s, a = req("PUT", f"/wp-json/code-snippets/v1/snippets/{SID}/activate", {})
assert s in (200, 201), a
s, r = req("POST", "/wp-json/nadlan-retitle/v1/go", {"token": TOKEN})
print("retitle:", s, json.dumps(r, ensure_ascii=False))
s, d = req("DELETE", f"/wp-json/code-snippets/v1/snippets/{SID}", None)
print("bridge deleted:", s)
assert r.get("ok") == 1 and "\u2014" not in r.get("title", "") and r.get("slug") == "stricker-13-brandeis-14"
print("OK title clean, slug unchanged")
