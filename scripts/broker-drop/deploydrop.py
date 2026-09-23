# -*- coding: utf-8 -*-
"""Broker drop box deploy (owner orders 23.9.2026: "an address the broker throws photos and details at, the system
builds the property in the broker's website, no replies, no login, for every future broker"; then "every broker joins
alone", "a listing in four languages from the same message", "the old wizard moves to the same engine").

Installs the modules as persistent Code Snippets, each after a PHP lint on the server itself:
  x-broker-drop   plugins/nadlan-config/inc/broker-drop.php    the engine: drop link, four languages, broker sites
  x-broker-join   plugins/nadlan-config/inc/broker-join.php    brokers join alone (needs x-broker-drop)
  x-owner-wizard  plugins/nadlan-config/inc/owner-wizard.php   /post-listing/ on the same engine (needs x-broker-drop)
Setup writes go through a temporary, token-gated bridge route with update_post_meta, so live pages are NOT re-saved
(no IndexNow re-pings, no revisions). The bridge is deleted at the end of every run (verified 404).

Usage:
  python deploydrop.py                       lint + install/update every module + verify
  python deploydrop.py --only x-broker-join  the same for the named modules (comma separated)
  python deploydrop.py --setup               also wire Meital (token, site pages, her 11 listings and their English twins)
  python deploydrop.py --meital-langs        Meital's new listings in Hebrew, English, Russian and French (+ her brand photo)
  python deploydrop.py --auto 0|1            Meital's pages publish at once (1) or wait as drafts (0)
  python deploydrop.py --rotate              a new personal link for Meital (the old one stops working at once)
  python deploydrop.py --off [--only name]   deactivate modules (rollback); the pages already built stay
  python deploydrop.py --verify              checks only
The drop link is printed only at --setup / --rotate (the deliverable the owner forwards). The WordPress app password is
decrypted in-process (DPAPI) and never printed.
"""
import base64, ctypes, ctypes.wintypes, hashlib, io, json, os, re, secrets, sys, time, urllib.request, urllib.error
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = "https://nad-lan.co.il"
REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
INC = os.path.join(REPO, "plugins", "nadlan-config", "inc")
MODULES = {
    "x-broker-drop": ("broker-drop.php", "Broker drop box: a private link per broker; photos and a few lines become a listing in the broker's site, in up to four languages. Source: plugins/nadlan-config/inc/broker-drop.php"),
    "x-broker-join": ("broker-join.php", "Brokers join alone: licence checked against the Ministry of Justice register, a free site and a personal link. Source: plugins/nadlan-config/inc/broker-join.php"),
    "x-owner-wizard": ("owner-wizard.php", "Owners publish from /post-listing/ through the same engine: Latin slug, language gate, no waiting. Source: plugins/nadlan-config/inc/owner-wizard.php"),
}
IMAP = os.path.join(REPO, "handoff", "meital-2026-09-17", "package", "data", "import-map.json")
SECRETS_PATH = r"C:\Users\777\Documents\websites\.codex-secrets\wordpress-app-passwords\nad-lan.co.il.json"
ARGS = sys.argv[1:]
BROKER = 7833
ONLY = [x for x in (ARGS[ARGS.index("--only") + 1].split(",") if "--only" in ARGS else list(MODULES)) if x in MODULES]
ONLY = [m for m in ONLY if os.path.exists(os.path.join(INC, MODULES[m][0]))]


class DATA_BLOB(ctypes.Structure):
    _fields_ = [("cbData", ctypes.wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]


def dpapi_unprotect(b64):
    raw = base64.b64decode(b64)
    bi = DATA_BLOB(len(raw), ctypes.cast(ctypes.create_string_buffer(raw, len(raw)), ctypes.POINTER(ctypes.c_char)))
    bo = DATA_BLOB()
    if not ctypes.windll.crypt32.CryptUnprotectData(ctypes.byref(bi), None, None, None, None, 0, ctypes.byref(bo)):
        raise RuntimeError("DPAPI")
    try:
        return ctypes.string_at(bo.pbData, bo.cbData).decode("utf-8")
    finally:
        ctypes.windll.kernel32.LocalFree(bo.pbData)


with open(SECRETS_PATH, encoding="utf-8-sig") as f:
    sec = json.load(f)
AUTH = "Basic " + base64.b64encode(f"{sec['username']}:{dpapi_unprotect(sec['password_dpapi'])}".encode()).decode()
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) NadLan-BrokerDrop/1.1"


def req(method, path, body=None, timeout=180, raw=False, auth=True, headers=None):
    data = None if body is None else json.dumps(body, ensure_ascii=False).encode()
    r = urllib.request.Request(BASE + path, data=data, method=method)
    if auth:
        r.add_header("Authorization", AUTH)
    r.add_header("User-Agent", UA)
    if body is not None:
        r.add_header("Content-Type", "application/json")
    for k, v in (headers or {}).items():
        r.add_header(k, v)
    try:
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            p = resp.read()
            return resp.status, (p if raw else json.loads(p.decode() or "null")), dict(resp.headers)
    except urllib.error.HTTPError as e:
        p = e.read()
        try:
            return e.code, (p if raw else json.loads(p.decode())), dict(e.headers)
        except Exception:
            return e.code, {"raw": p[:300].decode("utf-8", "replace")}, dict(e.headers)


def must(s, p, what, ok=(200, 201)):
    if s not in ok:
        raise SystemExit(f"FATAL {what}: HTTP {s}: {json.dumps(p, ensure_ascii=False)[:500]}")
    return p


def snip(method, path, body=None):
    return req(method, "/wp-json/code-snippets/v1/snippets" + path, body)[:2]


def find_snippet(name):
    s, lst = snip("GET", "")
    must(s, lst, "list snippets")
    for x in lst:
        if x["name"] == name:
            return x
    return None


s, h, _ = req("GET", "/wp-json/nadlan/v1/health")
must(s, h, "health")
print("health", h["version"], h["status"])

if "--off" in ARGS:
    for name in reversed(ONLY):
        x = find_snippet(name)
        if x:
            s2, _ = snip("PUT", f"/{x['id']}/deactivate", {})
            print(name, "deactivated", s2)
        else:
            print(name, "not installed")
    raise SystemExit(0)

TOKEN = secrets.token_hex(24)
BRIDGE = r'''
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-drop-ops/v1', '/apply', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( isset( $b['token'] ) ? $b['token'] : '' ) ) ) { return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) ); }
			$out = array();
			if ( ! empty( $b['lint'] ) ) {
				try { token_get_all( "<?php\n" . (string) $b['lint'], TOKEN_PARSE ); $out['lint'] = 'ok ' . PHP_VERSION; }
				catch ( ParseError $e ) { return new WP_Error( 'lint', $e->getMessage() . ' line ' . $e->getLine(), array( 'status' => 400 ) ); }
			}
			if ( ! empty( $b['meta'] ) && is_array( $b['meta'] ) ) {
				foreach ( $b['meta'] as $row ) {
					$pid = (int) $row['id'];
					if ( ! $pid || ! get_post( $pid ) ) { $out['meta_missing'][] = $pid; continue; }
					foreach ( (array) $row['set'] as $k => $v ) {
						if ( strpos( (string) $k, 'nl_' ) !== 0 ) { continue; }
						update_post_meta( $pid, sanitize_key( $k ), wp_slash( (string) $v ) );
					}
					$out['meta_ok'][] = $pid;
				}
			}
			if ( ! empty( $b['token_for'] ) ) {
				$pid = (int) $b['token_for'];
				$t   = (string) get_post_meta( $pid, '_nl_drop_token', true );
				if ( ! empty( $b['rotate'] ) || ! preg_match( '/^[a-z0-9]{24}$/', $t ) ) { $t = substr( bin2hex( random_bytes( 16 ) ), 0, 24 ); update_post_meta( $pid, '_nl_drop_token', $t ); }
				delete_post_meta( $pid, 'nl_drop_token' );
				$out['drop_url'] = home_url( '/drop/' . $t . '/' );
			}
			if ( ! empty( $b['yoast'] ) && is_array( $b['yoast'] ) ) {
				foreach ( $b['yoast'] as $row ) {
					$pid = (int) $row['id'];
					if ( ! $pid || ! get_post( $pid ) ) { continue; }
					update_post_meta( $pid, '_yoast_wpseo_title', wp_slash( (string) $row['title'] ) );
					update_post_meta( $pid, '_yoast_wpseo_metadesc', wp_slash( (string) $row['desc'] ) );
					$out['yoast_ok'][] = $pid;
				}
			}
			if ( ! empty( $b['attachment_by_url'] ) ) {
				$out['attachment'] = (int) attachment_url_to_postid( (string) $b['attachment_by_url'] );
			}
			if ( ! empty( $b['purge'] ) ) {
				foreach ( (array) $b['purge'] as $pid ) { clean_post_cache( (int) $pid ); do_action( 'litespeed_purge_post', (int) $pid ); }
				$out['purged'] = count( (array) $b['purge'] );
			}
			return $out;
		},
	) );
} );
'''.replace("__TOKEN__", TOKEN)


def install_and_setup():
    s, c = snip("POST", "", {"name": f"tmp-drop-ops-{int(time.time())}", "code": "/* placeholder */", "scope": "global", "active": False})
    must(s, c, "bridge create")
    br = c["id"]
    try:
        s, u = snip("PUT", f"/{br}", {"name": c["name"], "code": BRIDGE, "scope": "global", "active": False})
        must(s, u, "bridge update")
        s, a = snip("PUT", f"/{br}/activate", {})
        must(s, a, "bridge activate")

        def ops(payload, what):
            payload["token"] = TOKEN
            s, r, _ = req("POST", "/wp-json/nadlan-drop-ops/v1/apply", payload, timeout=240)
            return must(s, r, what)

        if "--verify" not in ARGS or "--install" in ARGS:
            codes = {}
            for name in ONLY:
                php = open(os.path.join(INC, MODULES[name][0]), encoding="utf-8").read()
                codes[name] = re.sub(r"^\s*<\?php\s*", "", php, count=1)
                print("lint on the server:", name, ops({"lint": codes[name]}, "lint " + name)["lint"])
            for name in ONLY:   # the engine first: the others need its functions
                code = codes[name]
                x = find_snippet(name)
                body = {"name": name, "code": code, "scope": "global", "active": False, "desc": MODULES[name][1]}
                if x:
                    sid = x["id"]
                    s, u2 = snip("PUT", f"/{sid}", body)
                    must(s, u2, "snippet update " + name)
                else:
                    s, c2 = snip("POST", "", body)
                    must(s, c2, "snippet create " + name)
                    sid = c2["id"]
                s, a2 = snip("PUT", f"/{sid}/activate", {})
                must(s, a2, "snippet activate " + name)
                print(name, "id", sid, "sha256", hashlib.sha256(code.encode()).hexdigest()[:16], "ACTIVE")

        if "--setup" in ARGS:
            imap = json.load(open(IMAP, encoding="utf-8"))
            rows = [{"id": BROKER, "set": {"nl_drop_on": "1", "nl_name_he": "מיטל קציר", "nl_name_en": "Meital Katzir",
                                             "nl_brand_en": "Real Estate by the Sea", "nl_gender": "f",
                                             "nl_site_he": str(imap["broker-he"]), "nl_site_en": str(imap["broker-en"]), "nl_auto_publish": "1"}},
                    {"id": imap["broker-he"], "set": {"nl_broker_site": str(BROKER), "nl_lang": "he"}},
                    {"id": imap["broker-en"], "set": {"nl_broker_site": str(BROKER), "nl_lang": "en"}}]
            for n in range(1, 12):
                L = f"L{n:02d}"
                he, en = imap.get(L + "-he"), imap.get(L + "-en")
                if he:
                    rows.append({"id": he, "set": {"nl_broker_id": str(BROKER), "nl_card_key": L, "nl_status": "active", "nl_twin": str(en or "")}})
                if en:
                    rows.append({"id": en, "set": {"nl_broker_id": str(BROKER), "nl_card_key": L, "nl_status": "active", "nl_twin": str(he or "")}})
            r = ops({"meta": rows, "token_for": BROKER, "purge": [imap["broker-he"], imap["broker-en"]]}, "setup")
            print("setup: meta on", len(r.get("meta_ok", [])), "posts; missing", r.get("meta_missing", []))
            print("DROP LINK:", r["drop_url"])

        if "--meital-langs" in ARGS:
            hero = ops({"attachment_by_url": "https://nad-lan.co.il/wp-content/uploads/2026/09/meital-katzir-sea-terrace.jpg"}, "hero")["attachment"]
            r = ops({"meta": [{"id": BROKER, "set": {"nl_langs": "he,en,ru,fr", "nl_tier": "studio", "nl_slug": "meital-katzir",
                                                     "nl_hero": str(hero or ""), "nl_areas_en": "Nofei Yam,Kochav HaTzafon,Tzukei Aviv,Ramat Aviv,Sarona,Herzliya Pituach",
                                                     "nl_areas_ru": "Нофей Ям,Кохав ха-Цафон,Цукей Авив,Рамат-Авив,Сарона,Герцлия-Питуах",
                                                     "nl_areas_fr": "Nofei Yam,Kochav HaTzafon,Tsoukei Aviv,Ramat Aviv,Sarona,Herzliya Pituah"}}]}, "meital langs")
            print("Meital: listings in he, en, ru, fr; hero attachment", hero, r.get("meta_ok"))

        if "--pages" in ARGS:
            # the "for brokers" page in four languages, each ending with the sign-up form (x-broker-join fills the mount)
            pages_dir = os.path.join(REPO, "scripts", "broker-drop", "pages")
            spec = {"he": (7645, 0, "מיניסייט למתווכים ולמשרדי תיווך", "מיניסייט למתווכים | האתר שלכם בתוך פורטל הנדל״ן nad-lan",
                           "אתר על שמכם בחינם, עמוד מלא לכל נכס, עברית ואנגלית, והעלאת נכס מהטלפון בתוך דקה. הרישיון נבדק מול פנקס המתווכים."),
                    "en": (7803, 5011, "Minisites for Real Estate Brokers and Agencies", "Broker Minisites | Your Real Estate Site Inside nad-lan",
                           "A free site under your name, a full page for every listing, Hebrew and English, and a listing live from your phone in a minute. Licence checked against the register."),
                    "ru": (0, 5056, "Мини-сайт для риелторов и агентств недвижимости", "Мини-сайт для риелторов в Израиле | nad-lan",
                           "Бесплатный сайт с вашим именем, страница для каждого объекта, публикация с телефона за минуту. Лицензия проверяется по реестру риелторов."),
                    "fr": (0, 5055, "Mini-site pour agents immobiliers et agences", "Mini-site pour agents immobiliers en Israël | nad-lan",
                           "Un site gratuit à votre nom, une page par bien, publication depuis le téléphone en une minute. Licence vérifiée dans le registre des agents.")}
            yo = []
            for lang, (pid, parent, title, ytitle, ydesc) in spec.items():
                content = open(os.path.join(pages_dir, f"brokers-{lang}.html"), encoding="utf-8").read()
                if not pid:
                    s, found, _ = req("GET", f"/wp-json/wp/v2/pages?slug=brokers&parent={parent}&status=publish,draft&_fields=id")
                    pid = found[0]["id"] if isinstance(found, list) and found else 0
                if pid:
                    s, r, _ = req("POST", f"/wp-json/wp/v2/pages/{pid}", {"content": content, "title": title})
                    must(s, r, f"page {lang}")
                else:
                    s, r, _ = req("POST", "/wp-json/wp/v2/pages", {"content": content, "title": title, "slug": "brokers", "parent": parent, "status": "publish"})
                    must(s, r, f"page {lang} create")
                    pid = r["id"]
                print(f"brokers page {lang}: id {pid} {r.get('link')}")
                yo.append({"id": pid, "title": ytitle, "desc": ydesc})
            ops({"yoast": yo, "purge": [y["id"] for y in yo]}, "yoast")

        if "--rotate" in ARGS:
            r = ops({"token_for": BROKER, "rotate": 1}, "rotate")
            print("NEW DROP LINK:", r["drop_url"])
            with open(os.path.join(os.environ.get("NL_SCRATCH", "."), "drop_url.txt"), "w", encoding="utf-8") as fh:
                fh.write(r["drop_url"] + chr(10))

        if "--auto" in ARGS:
            val = ARGS[ARGS.index("--auto") + 1]
            ops({"meta": [{"id": BROKER, "set": {"nl_auto_publish": "1" if val == "1" else "0"}}]}, "auto")
            print("auto publish ->", val)
    finally:
        s1, _ = snip("PUT", f"/{br}/deactivate", {})
        s2, _ = snip("DELETE", f"/{br}", None)
        print("bridge cleanup", s1, s2)
        s3, _, _ = req("POST", "/wp-json/nadlan-drop-ops/v1/apply", {"token": "x"})
        print("bridge route after cleanup:", s3, "(want 404)")


if "--verify" not in ARGS or any(a in ARGS for a in ("--setup", "--auto", "--install", "--rotate", "--meital-langs", "--pages")):
    install_and_setup()

# ---- verify ----
time.sleep(3)
s, hc, _ = req("GET", "/wp-json/nadlan/v1/healthcheck?nlv=%d" % time.time(), auth=False)
print("healthcheck:", s, "version", hc.get("version"), "| broker_drop:", json.dumps(hc.get("broker_drop"), ensure_ascii=False),
      "| broker_join:", json.dumps(hc.get("broker_join"), ensure_ascii=False), "| owner_wizard:", json.dumps(hc.get("owner_wizard"), ensure_ascii=False))
for path in ("/", "/brokers/", "/en/brokers/", "/ru/brokers/", "/fr/brokers/", "/brokers/meital-katzir/", "/en/brokers/meital-katzir/", "/properties/nofei-yam-3-rooms-balcony-for-rent/", "/post-listing/"):
    s, body, _ = req("GET", path + "?nlv=%d" % time.time(), raw=True, auth=False, headers={"User-Agent": "Mozilla/5.0 Chrome/128"}, timeout=120)
    t = body.decode("utf-8", "replace") if isinstance(body, (bytes, bytearray)) else ""
    b = t.split("<body", 1)[-1]
    cards = b.count('class="nlb-lcard"')
    err = ("Fatal error" in t) or ("Warning:" in b[:4000])
    print(f"GET {path}: {s} bytes={len(t)} cards={cards} php_error={err} h1={len(re.findall(r'<h1[ >]', b))} join_form={b.count('nljoin-form')}")
s, pro, _ = req("GET", "/wp-json/wp/v2/nadlan_professional/%d?nlv=%d" % (BROKER, time.time()), auth=False)
leak = [k for k in ((pro or {}).get("meta") or {}) if "token" in k or k == "_nl_email"]
print("public REST record of the broker:", s, "secret keys exposed:", leak or "none")
s, body, _ = req("GET", "/drop/000000000000000000000000/", raw=True, auth=False)
print("drop page with a dead token:", s, "(want 404)")
