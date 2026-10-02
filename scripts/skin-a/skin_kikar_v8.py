# -*- coding: utf-8 -*-
"""Kikar V8 (design v104.26, DS version 175, 2.10.2026): Kikar Hamedina leads the projects band on the Hebrew home and on the four
language homes. The band's list lives in the persistent Code Snippet x-skin-a (#638, source plugins/nadlan-config/inc/skin-a.php),
not in the plugin, so this is its own small release:

  1. read the LIVE snippet code; it must equal the repo's committed skin-a.php (no drift) and hold the anchor exactly once;
  2. apply the one hunk to the live text; the result must equal the repo's working copy (one source of truth);
  3. back the live code up to docs/qa/v8-traffic/, lint the new code on the server (token_get_all, TOKEN_PARSE) through a temporary
     bridge, update the snippet, purge the cache;
  4. check the five homes (each links to its own Kikar page and still to Rainbow) and three controls; any failure puts the old
     code back and purges again. The bridge is always deleted.

The app password is decrypted in-process (DPAPI) and never printed.   python scripts/skin-a/skin_kikar_v8.py [--dry]"""
import base64, hashlib, io, json, os, re, secrets, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
DRY = "--dry" in sys.argv
SID = 638
REL = "plugins/nadlan-config/inc/skin-a.php"
QA = os.path.join(REPO, "docs", "qa", "v8-traffic")
OLD = ("\t\t$prefer = array( 'rainbow-tel-aviv', 'h-infinity-somail-tel-aviv', 'six-8-herbert-samuel-tel-aviv', 'dimri-yama-sde-dov', "
       "'ashira-sde-dov', 'einstein-tower' );\n")
NEW = ("\t\t/* v104.26 (2.10.2026, Kikar V8): Kikar Hamedina leads every home's projects band, Hebrew and the four languages\n"
       "\t\t   (its own language page); the rest in the order of their Search Console impressions. */\n"
       "\t\t$prefer = array( 'hamedina', 'rainbow-tel-aviv', 'h-infinity-somail-tel-aviv', 'ashira-sde-dov', 'dimri-yama-sde-dov', "
       "'six-8-herbert-samuel-tel-aviv', 'einstein-tower' );\n")
CHECKS = [  # path, must link (in the body), must not
    ("/", ["/projects/hamedina/", "/projects/rainbow-tel-aviv/", "/projects/h-infinity-somail-tel-aviv/", "nlhp-pcard--lead"], []),
    ("/en/", ["/projects/hamedina-en/", "/projects/rainbow-tel-aviv-en/", "/projects/ashira-sde-dov-en/"], []),
    ("/fr/", ["/projects/hamedina-fr/", "/projects/rainbow-tel-aviv-fr/", "/projects/ashira-sde-dov-fr/"], []),
    ("/ru/", ["/projects/hamedina-ru/", "/projects/rainbow-tel-aviv-ru/", "/projects/ashira-sde-dov-ru/"], []),
    ("/ar/", ["/projects/hamedina-ar/", "/projects/rainbow-tel-aviv-ar/", "/projects/ashira-sde-dov-ar/"], []),
    ("/projects/", ["/projects/hamedina/"], []),
    ("/projects/hamedina/", ["nlps-stage--world"], []),
    ("/projects/rainbow-tel-aviv/", ["mountRainbowStage"], []),
]

# the auth + request helpers of deployskin.py (same secrets path, same DPAPI), without its file uploads
_src = open(os.path.join(HERE, "deployskin.py"), encoding="utf-8").read()
_ns = {"__name__": "skin_kikar_v8_helpers"}
exec(compile(_src[:_src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), _ns)
req, must, snip = _ns["req"], _ns["must"], _ns["snip"]
# (the helpers wrap sys.stdout in UTF-8 themselves; wrapping it twice closes the stream)


def strip_open(php):
    return re.sub(r'^\s*<\?php\s*', '', php, count=1)


def body(path):
    s, b, _ = req("GET", path + ("&" if "?" in path else "?") + "nlv8=" + str(int(time.time() * 1000)), raw=True, auth=False,
                  headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/130 Safari/537.36"})
    t = b.decode("utf-8", "replace") if isinstance(b, (bytes, bytearray)) else json.dumps(b)
    i = t.find("<body")
    return s, (t[i:] if i > -1 else t)


def run_checks(tag):
    bad = []
    for path, need, nope in CHECKS:
        s, b = body(path)
        miss = [n for n in need if n not in b]
        extra = [n for n in nope if n in b]
        ok = s == 200 and not miss and not extra
        print(f"[{tag}] {'OK ' if ok else 'BAD'} {s} {path}" + (f" missing {miss}" if miss else "") + (f" unwanted {extra}" if extra else ""))
        if not ok:
            bad.append(path)
    return bad


s, h, _ = req("GET", "/wp-json/nadlan/v1/health"); must(s, h, "health"); print("[health]", h.get("version"), h.get("status"))
head = strip_open(subprocess.run(["git", "show", "HEAD:" + REL], cwd=REPO, capture_output=True, text=True, encoding="utf-8", check=True).stdout)
work = strip_open(open(os.path.join(REPO, *REL.split("/")), encoding="utf-8").read())
s, sn = snip("GET", f"/{SID}"); must(s, sn, "snippet read")
if sn.get("name") != "x-skin-a" or not sn.get("active"):
    raise SystemExit(f"FATAL: snippet {SID} is {sn.get('name')!r}, active={sn.get('active')}")
live = sn["code"]
if NEW in live:
    raise SystemExit("FATAL: the live snippet already holds the v104.26 order")
if live != head:
    raise SystemExit(f"FATAL drift: live x-skin-a ({hashlib.md5(live.encode()).hexdigest()[:10]}) != repo HEAD {REL} "
                     f"({hashlib.md5(head.encode()).hexdigest()[:10]}); diff before replacing")
if live.count(OLD) != 1:
    raise SystemExit(f"FATAL: the anchor is in the live code {live.count(OLD)} times")
new = live.replace(OLD, NEW)
if new != work:
    raise SystemExit("FATAL: live + hunk != the repo working copy; the repo must hold exactly this change")
print(f"[drift] none: live == HEAD ({hashlib.md5(live.encode()).hexdigest()[:10]}); new {hashlib.md5(new.encode()).hexdigest()[:10]} == working copy")
os.makedirs(QA, exist_ok=True)
stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
bak = os.path.join(QA, f"x-skin-a-638.{stamp}.live.php")
io.open(bak, "w", encoding="utf-8", newline="").write(live)
print("[backup]", os.path.relpath(bak, REPO))
before = run_checks("before")
if DRY:
    print("[dry] stop here: nothing written"); sys.exit(0)

TOKEN = secrets.token_hex(24)
BRIDGE = r'''
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-skin-ops/v1', '/apply', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( isset( $b['token'] ) ? $b['token'] : '' ) ) ) { return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) ); }
			$out = array();
			if ( ! empty( $b['lint'] ) ) {
				try { token_get_all( "<?php\n" . (string) $b['lint'], TOKEN_PARSE ); $out['lint'] = 'ok'; }
				catch ( ParseError $e ) { return new WP_Error( 'lint', $e->getMessage() . ' line ' . $e->getLine(), array( 'status' => 400 ) ); }
			}
			if ( ! empty( $b['purge'] ) ) { do_action( 'litespeed_purge_all' ); if ( function_exists( 'wp_cache_flush' ) ) { wp_cache_flush(); } $out['purged'] = 1; }
			return $out;
		},
	) );
} );
'''.replace("__TOKEN__", TOKEN)
s, c = snip("POST", "", {"name": f"tmp-skin-v8-ops-{int(time.time())}", "code": "/* placeholder */", "scope": "global", "active": False})
must(s, c, "bridge create")
BR = c["id"]
written = False
ok = False
try:
    s, u = snip("PUT", f"/{BR}", {"name": c["name"], "code": BRIDGE, "scope": "global", "active": False}); must(s, u, "bridge update")
    s, a = snip("PUT", f"/{BR}/activate", {}); must(s, a, "bridge activate")

    def ops(payload, what):
        payload["token"] = TOKEN
        s, r, _ = req("POST", "/wp-json/nadlan-skin-ops/v1/apply", payload, timeout=240); must(s, r, what); return r

    ops({"lint": new}, "lint"); print("[lint] ok on the server")
    s, u2 = snip("PUT", f"/{SID}", {"name": "x-skin-a", "code": new, "scope": "global", "active": False}); must(s, u2, "x-skin-a update")
    written = True
    s, a2 = snip("PUT", f"/{SID}/activate", {}); must(s, a2, "x-skin-a activate")
    s, back = snip("GET", f"/{SID}"); must(s, back, "x-skin-a read back")
    if back.get("code") != new or not back.get("active"):
        raise SystemExit("FATAL: the snippet read back differs or is inactive")
    print("[write] x-skin-a #638 updated and active; sha256", hashlib.sha256(new.encode()).hexdigest()[:16])
    ops({"purge": 1}, "purge"); print("[purge] done")
    time.sleep(6)
    bad = run_checks("after")
    if bad:
        raise SystemExit("FATAL checks failed: " + ", ".join(bad))
    ok = True
finally:
    if written and not ok:
        print("[rollback] putting the old x-skin-a code back")
        s, r1 = snip("PUT", f"/{SID}", {"name": "x-skin-a", "code": live, "scope": "global", "active": False})
        s2, r2 = snip("PUT", f"/{SID}/activate", {})
        print("[rollback] update", s, "activate", s2)
        try:
            ops({"purge": 1}, "purge after rollback")
        except BaseException as e:  # noqa: BLE001
            print("[rollback] purge failed:", e)
    s1, _ = snip("PUT", f"/{BR}/deactivate", {}); s2, _ = snip("DELETE", f"/{BR}", None)
    print("[bridge] cleanup", s1, s2)
s, h, _ = req("GET", "/wp-json/nadlan/v1/health"); print("[health after]", h.get("version"), h.get("status"))
rec = {"release": "skin x-skin-a v104.26 (Kikar V8)", "at": stamp, "snippet": SID, "live_before_md5": hashlib.md5(live.encode()).hexdigest(),
       "new_md5": hashlib.md5(new.encode()).hexdigest(), "backup": os.path.relpath(bak, REPO), "checks_before_bad": before, "ok": ok}
io.open(os.path.join(QA, "skin-v8-result.json"), "w", encoding="utf-8").write(json.dumps(rec, ensure_ascii=False, indent=1))
print("RELEASE LIVE: Kikar Hamedina leads the projects band on the Hebrew home and on /en/ /fr/ /ru/ /ar/" if ok else "NOT RELEASED")
