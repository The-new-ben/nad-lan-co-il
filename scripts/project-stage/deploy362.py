"""Release 1.72.362 (28.9.2026): ProNetwork v98, the professionals' network card, and the privacy of private people.
The owner, 28.9: "professionals still look very basic with this circle and a letter ... we talked about a social network".
One renderer (nadlan_dir_card) prints the new card: a cover with the profession's pattern, a portrait or a designed monogram,
the strongest register fact (contractors: registered since, branches and classification from the contractors register,
data/register-facts.json), separate trust labels, verified-only stars, save with a private shortlist. The profile header
gets the same monogram, the register year and government recognition. A private person from a public register who has not
taken over the profile shows the city only: no street address (facts table, JSON-LD, REST), no phone (call button, JSON-LD).
Also: "ותק (שנים) 1963" and "1963+ שנות ניסיון" now read "פעילה מאז 1963".

  NEW inc/pro-card.php, assets/pronet/procard.css, data/register-facts.json
  inc/directory.php, inc/cards-render.php, inc/schema.php, inc/rest-privacy.php, inc/professional-profile.php,
  nadlan-config.php (version bump + 'pro-card' in the module list, on the LIVE text)

Same safety chain as deploy361.py.   python scripts/project-stage/deploy362.py [--dry | --rollback]
"""
import base64, ctypes, ctypes.wintypes, hashlib, io, json, os, re, secrets, subprocess, sys, tempfile, time, urllib.request, urllib.error, zlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = "https://nad-lan.co.il"
REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
SECRETS_PATH = r"C:\Users\777\Documents\websites\.codex-secrets\wordpress-app-passwords\nad-lan.co.il.json"
ARGS = sys.argv[1:]
DRY = "--dry" in ARGS
BAK = ".bak362"
CRLF, LF = bytes([13, 10]), bytes([10])


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
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) NadLan-PS362/1.0"


def req(method, path, body=None, timeout=120, raw=False, auth=True):
    r = urllib.request.Request(BASE + path, data=None if body is None else json.dumps(body, ensure_ascii=False).encode(), method=method)
    if auth:
        r.add_header("Authorization", AUTH)
    r.add_header("User-Agent", UA)
    if body is not None:
        r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            p = resp.read()
            return resp.status, (p if raw else json.loads(p.decode("utf-8") or "null"))
    except urllib.error.HTTPError as e:
        p = e.read()
        if raw:
            return e.code, p
        try:
            return e.code, json.loads(p.decode("utf-8"))
        except Exception:
            return e.code, {"raw": p[:300].decode("utf-8", "replace")}


def must(s, p, what, ok=(200, 201)):
    if s not in ok:
        raise SystemExit(f"FATAL {what}: HTTP {s}: {json.dumps(p, ensure_ascii=False)[:400]}")
    return p


def md5(b):
    return hashlib.md5(b).hexdigest()


def php_lint(data, label):
    with tempfile.NamedTemporaryFile("wb", suffix=".php", delete=False) as t:
        t.write(data)
        tmp = t.name
    try:
        out = subprocess.run(["php", "-l", tmp], capture_output=True, text=True)
    finally:
        os.unlink(tmp)
    if out.returncode != 0:
        raise SystemExit(f"FATAL local lint {label}: {out.stdout.strip()} {out.stderr.strip()}")
    print(f"[lint] {label}: ok")


def git_head(rel):
    out = subprocess.run(["git", "-C", REPO, "show", "HEAD:" + rel.replace(os.sep, "/")], capture_output=True)
    if out.returncode != 0:
        return None
    return out.stdout


# ---------------------------------------------------------------- health + bridge
s, h = req("GET", "/wp-json/nadlan/v1/health", auth=False)
must(s, h, "health")
LIVE_VER = h.get("version")
print("[health]", LIVE_VER, h.get("status"))
if h.get("status") != "ok":
    raise SystemExit("FATAL: live health is not ok before the release")

TOKEN = secrets.token_hex(24)
NS = 'nadlan-ps362-' + TOKEN[:8]  # one route per run: a bridge left over from a failed run can never answer for this one
BRIDGE = r'''
add_action( 'rest_api_init', function () {
	register_rest_route( '__NS__/v1', '/apply', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( $b['token'] ?? '' ) ) ) {
				return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) );
			}
			$root = WP_PLUGIN_DIR . '/nadlan-config/';
			$rel  = function ( $r ) { return ltrim( str_replace( array( '..', '\\' ), array( '', '/' ), (string) $r ), '/' ); };
			$out  = array();
			if ( ! empty( $b['get'] ) ) {
				$p = $root . $rel( $b['get'] );
				if ( ! is_readable( $p ) ) { $out['get'] = array( 'missing' => 1 ); }
				else { $d = file_get_contents( $p ); $out['get'] = array( 'b64' => base64_encode( $d ), 'md5' => md5( $d ) ); }
			}
			if ( ! empty( $b['put'] ) && is_array( $b['put'] ) ) {
				$p = $root . $rel( $b['put']['rel'] );
				$d = base64_decode( (string) $b['put']['b64'], true );
				if ( false !== $d && ! empty( $b['put']['z'] ) ) { $d = @gzuncompress( $d ); }
				if ( false === $d || md5( $d ) !== strtolower( (string) $b['put']['md5'] ) ) { return new WP_Error( 'md5', 'mismatch', array( 'status' => 400 ) ); }
				if ( '.php' === substr( $rel( $b['put']['rel'] ), -4 ) ) { try { token_get_all( $d, TOKEN_PARSE ); } catch ( ParseError $e ) { return new WP_Error( 'lint', $e->getMessage() . ' line ' . $e->getLine(), array( 'status' => 400 ) ); } }
				if ( isset( $b['put']['expect'] ) ) {
					$cur = file_exists( $p ) ? md5_file( $p ) : 'missing';
					if ( $cur !== (string) $b['put']['expect'] ) { return new WP_Error( 'drift', 'live file changed: ' . $cur, array( 'status' => 409 ) ); }
				}
				if ( ! is_dir( dirname( $p ) ) ) { wp_mkdir_p( dirname( $p ) ); } // a new folder (assets/nlds/) is made first
				if ( file_exists( $p ) && ! file_exists( $p . '__BAK__' ) ) { copy( $p, $p . '__BAK__' ); }
				$w = file_put_contents( $p, $d, LOCK_EX );
				clearstatcache( true, $p );
				$out['put'] = array( 'bytes' => $w, 'md5' => md5_file( $p ) );
			}
			if ( ! empty( $b['restore'] ) ) {
				$p = $root . $rel( $b['restore'] );
				if ( file_exists( $p . '__BAK__' ) ) { copy( $p . '__BAK__', $p ); clearstatcache( true, $p ); if ( function_exists( 'opcache_invalidate' ) ) { @opcache_invalidate( $p, true ); } $out['restore'] = md5_file( $p ); } else { $out['restore'] = 'no-bak'; }
			}
			if ( ! empty( $b['unlink'] ) ) {
				$p = $root . $rel( $b['unlink'] );
				$out['unlink'] = file_exists( $p ) ? ( @unlink( $p ) ? 1 : 0 ) : 'missing';
			}
			if ( ! empty( $b['diag'] ) ) {
				$q = '[out:json][timeout:25];(node(around:1200,32.1059,34.7845)[highway=bus_stop];);out tags center 5;';
				$res = array();
				foreach ( array( 'https://overpass-api.de/api/interpreter', 'https://overpass.kumi.systems/api/interpreter', 'https://maps.mail.ru/osm/tools/overpass/api/interpreter' ) as $ep ) {
					$t0 = microtime( true );
					$rr = wp_remote_post( $ep, array( 'timeout' => 14, 'body' => array( 'data' => $q ), 'headers' => array( 'User-Agent' => 'nadlan-config/2.0 (nad-lan.co.il)' ) ) );
					$res[] = array( 'ep' => $ep, 'code' => is_wp_error( $rr ) ? $rr->get_error_message() : wp_remote_retrieve_response_code( $rr ), 'secs' => round( microtime( true ) - $t0, 2 ) );
				}
				$over = 0; $now = time();
				foreach ( (array) _get_cron_array() as $ts => $hooks ) { if ( $ts < $now - 300 ) { $over += count( $hooks ); } }
				$out['diag'] = array( 'overpass' => $res, 'disable_wp_cron' => defined( 'DISABLE_WP_CRON' ) && DISABLE_WP_CRON ? 1 : 0, 'cron_overdue_5min' => $over, 'poi_down' => get_transient( 'nadlan_poi_down' ) ? 1 : 0, 'poi_rate' => (int) get_transient( 'nadlan_poi_rate' ), 'poi_events' => count( array_filter( (array) _get_cron_array(), function ( $h ) { return isset( $h['nadlan_poi_refresh'] ); } ) ) );
			}
			if ( ! empty( $b['legal'] ) && is_array( $b['legal'] ) ) {
				$res = array();
				foreach ( $b['legal'] as $slug => $d ) {
					$slug = sanitize_title( $slug );
					$pg   = get_page_by_path( $slug, OBJECT, 'page' );
					if ( $pg ) {
						$res[ $slug ] = array( 'exists' => (int) $pg->ID, 'status' => $pg->post_status );
					} else {
						$pid = wp_insert_post( array( 'post_type' => 'page', 'post_status' => 'publish', 'post_name' => $slug, 'post_title' => (string) $d['title'], 'post_content' => (string) $d['content'] ), true );
						$res[ $slug ] = is_wp_error( $pid ) ? $pid->get_error_message() : array( 'created' => (int) $pid );
					}
				}
				$priv = get_page_by_path( 'privacy', OBJECT, 'page' );
				if ( $priv && 'publish' === $priv->post_status ) { update_option( 'wp_page_for_privacy_policy', (int) $priv->ID ); }
				$res['privacy_policy_url'] = get_privacy_policy_url();
				$out['legal'] = $res;
			}
			if ( ! empty( $b['set_video'] ) && is_array( $b['set_video'] ) ) {
				$pid = (int) $b['set_video']['post'];
				if ( 'nadlan_professional' !== get_post_type( $pid ) ) { return new WP_Error( 'video', 'not a professional', array( 'status' => 400 ) ); }
				$val = (string) $b['set_video']['value'];
				if ( '' === $val ) { delete_post_meta( $pid, 'nl_video' ); } else { update_post_meta( $pid, 'nl_video', wp_slash( $val ) ); }
				$out['set_video'] = array( 'post' => $pid, 'now' => (string) get_post_meta( $pid, 'nl_video', true ) );
			}
			if ( ! empty( $b['seed_pl'] ) && is_array( $b['seed_pl'] ) ) {
				$d   = $b['seed_pl'];
				$ids = get_posts( array( 'post_type' => 'nadlan_placement', 'post_status' => 'any', 'title' => (string) $d['title'], 'numberposts' => 1, 'fields' => 'ids' ) );
				$pid = $ids ? (int) $ids[0] : (int) wp_insert_post( array( 'post_type' => 'nadlan_placement', 'post_status' => 'publish', 'post_title' => (string) $d['title'] ), true );
				if ( $pid <= 0 ) { return new WP_Error( 'seed', 'insert failed', array( 'status' => 500 ) ); }
				if ( 'publish' !== get_post_status( $pid ) ) { wp_update_post( array( 'ID' => $pid, 'post_status' => 'publish' ) ); }
				foreach ( (array) $d['meta'] as $k => $v ) { if ( 0 === strpos( (string) $k, 'pl_' ) ) { update_post_meta( $pid, $k, (string) $v ); } }
				$m = array();
				foreach ( array( 'pl_pro', 'pl_paths', 'pl_after_h2', 'pl_headline', 'pl_ask', 'pl_start', 'pl_end', 'pl_active' ) as $k ) { $m[ $k ] = get_post_meta( $pid, $k, true ); }
				$out['seed_pl'] = array( 'id' => $pid, 'created' => $ids ? 0 : 1, 'status' => get_post_status( $pid ), 'meta' => $m );
			}
			if ( ! empty( $b['pl_off'] ) ) {
				$pid = (int) $b['pl_off'];
				$out['pl_off'] = 'nadlan_placement' === get_post_type( $pid ) ? update_post_meta( $pid, 'pl_active', '0' ) : 'not-a-placement';
			}
			if ( ! empty( $b['head'] ) ) {
				$d = (string) @file_get_contents( $root . 'nadlan-config.php', false, null, 0, 1200 );
				$out['head'] = preg_match( '/Version:\s*([0-9.]+)/', $d, $m ) ? $m[1] : '';
			}
			if ( ! empty( $b['purge'] ) ) {
				if ( function_exists( 'opcache_invalidate' ) ) { foreach ( array( 'inc/project-stage.php', 'inc/project-experience.php', 'inc/sdedov-teaser.php', 'inc/home-v3.php', 'inc/i18n.php', 'inc/drone-map.php', 'inc/project-topbar.php', 'inc/facility-chips.php', 'inc/developer-redirect.php', 'inc/glossary-autolink.php', 'inc/conversion-cta.php', 'inc/wa-source.php', 'inc/scheduler.php', 'inc/project-stage.php', 'inc/calculators.php', 'inc/together.php', 'nadlan-config.php' ) as $f ) { @opcache_invalidate( $root . $f, true ); } }
				if ( function_exists( 'opcache_reset' ) ) { $out['opcache'] = @opcache_reset(); }
				do_action( 'litespeed_purge_all' ); wp_cache_flush(); $out['purged'] = 1;
			}
			return $out;
		},
	) );
} );
'''.replace("__TOKEN__", TOKEN).replace("__BAK__", BAK).replace("__NS__", NS)


def snip(method, path, body=None):
    return req(method, "/wp-json/code-snippets/v1/snippets" + path, body=body)


def ops(payload, what):
    payload["token"] = TOKEN
    s, r = req("POST", "/wp-json/" + NS + "/v1/apply", body=payload, timeout=180)
    return must(s, r, what)


BR = None


def bridge_up():
    global BR
    s, c = snip("POST", "", {"name": f"x-tmp-ps362-ops-{int(time.time())}", "code": BRIDGE, "scope": "global", "active": False})
    must(s, c, "bridge create")
    BR = c["id"]
    must(*snip("PUT", f"/{BR}/activate", {}), "bridge activate")
    for _ in range(10):
        s, r = req("POST", "/wp-json/" + NS + "/v1/apply", body={"token": TOKEN, "head": 1})
        if s == 200:
            print("[bridge] up, id", BR, "| live header version", r.get("head"))
            return
        time.sleep(1.5)
    raise SystemExit("FATAL bridge route never answered")


def bridge_down():
    if BR is None:
        return
    snip("PUT", f"/{BR}/deactivate", {})
    s, _ = snip("DELETE", f"/{BR}", None)
    time.sleep(1.5)
    s2, _ = req("POST", "/wp-json/" + NS + "/v1/apply", body={"token": TOKEN})
    print(f"[bridge] delete http {s}; route now http {s2} (want 404)")


def put(rel, data, expect=None):
    z = zlib.compress(data, 9)
    body = {"put": {"rel": rel, "b64": base64.b64encode(z).decode(), "z": 1, "md5": md5(data)}}
    if expect is not None:
        body["put"]["expect"] = expect
    r = ops(body, f"put {rel}")["put"]
    if r["md5"] != md5(data):
        raise SystemExit(f"FATAL {rel}: server md5 {r['md5']} != local {md5(data)}")
    print(f"[put] {rel}: {r['bytes']} bytes, md5 {r['md5'][:10]} verified")


def live_get(rel):
    return ops({"get": rel}, f"get {rel}")["get"]


def page(path):
    s, b = req("GET", path, raw=True, auth=False, timeout=90)
    return s, b.decode("utf-8", "replace")


def body_of(html):
    i = html.find("<body")
    return html[i:] if i > -1 else html


SLOW_PROJECTS = ["/projects/shikun-binui-sde-dov/"]
RB = "/projects/rainbow-tel-aviv/"
CHECKS = [
    ("/professionals/?profession=lawyer", ['<span class="nlpn-state is-demo"><i></i>פרופיל לדוגמה</span>', ' is-demo" style="--pc:'], ['<span class="nldc-sample">']),
    ("/professionals/%d7%92%d7%91%d7%90%d7%99-%d7%9e%d7%99%d7%9b%d7%90%d7%9c-2/", ['<h1 class="nlpp-name">גבאי מיכאל</h1>', 'class="nldir nldir-similar"', '<article class="nlpn', 'תחומי רישום: שיפוצים (סיווג 1)', '✓ רשום בפנקס הקבלנים מאז 2019, מספר', 'class="nlpp-avatar nlpp-mono"', ' style="fill:#334236">גמ</text>', 'רשום בפנקס מאז'], ['ישראל אלדד', '"telephone":"', 'href="tel:', '<a class="nldc nldc--pro"', '<span>סיווג רשמי</span>', 'style="--pc:#334236;--ps:#F1F4EE"></p>', '<p></a><br />', '<!--NLPPSHIELD']),
    ("/professionals/", ['<article class="nlpn', 'class="nlpn-role"', 'id="nlpn-js"', 'assets/pronet/procard.css?ver=1.72.362', 'class="nlpn-save"', 'קבלנים <i>', 'מתווכים <i>', '.nldc.nldc--pro .nldc-top{', 'id="nlhp-top"', 'nldc-slot41', 'text-align:start!important;min-height:0!important'], ['שמאי מקרקעין <i>2</i>', 'המוביל בישראל. תוכנית Pro', '<a class="nldc" href=', '<a class="nldc is-featured" href=']),
    (RB, ['class="nlps-page"', 'id="nlps"', 'id="nlps-t"', 'class="nlbsq"', 'class="nlbslot"', 'id="nlps-view"', 'id="nlps-view-k"', '<h1 id="nl-project-page-title" class="nlps-h1">', 'id="nlpjx-map"', 'class="nl-lead"', 'nlcp-projctx', 'nadlan-project-article', 'רישיון תיווך', 'פרסומת', 'רוצה להופיע כאן?', 'לקבלת תוכניות ומחירים', 'assets/project-stage/bridge.js?ver=1.72.362', 'poster.jpg?ver=1.72.362', 'stage.js?ver=1.72.362', 'id="nlps-tour"', 'living-25w-card.jpg?ver=1.72.362', 'class="nlps-ssr-poster"', 'poster-716.jpg?ver=1.72.362 716w', 'imagesrcset=', 'rel="modulepreload" href="https://nad-lan.co.il/wp-content/plugins/nadlan-config/assets/project-stage/rainbow/stage.js?ver=1.72.362"', '<style id="nadlan-ps-css">', 'balcony-25w-2k.jpg', 'balcony-25n-2k.jpg', 'balcony-25e-2k.jpg', 'balcony-25s-2k.jpg', 'מהסלון ומהמרפסת', r'\u05de\u05e8\u05e4\u05e1\u05d5\u05ea \u05d4\u05de\u05d2\u05d3\u05dc \u05d1\u05d5\u05dc\u05d8\u05d5\u05ea \u05e2\u05d3 2 \u05de\u05f3', '&quot;spot&quot;:&quot;balcony&quot;', 'data-nlps-tour-scenes=', 'living-25n-2k.jpg', 'living-25e-2k.jpg', 'living-25s-2k.jpg', 'קומות 10, 25 ו־36, בארבעת הכיוונים', 'class="nlps-steps"', 'grid-template-areas:"hero" "lead" "cta" "stage" "below"', '<h1 id="nl-project-page-title" class="nlps-h1">', 'id="nlps-near"', '.nlps-vpin{', 'data-nlps-step="inside"', 'living-36w-2k.jpg', 'balcony-10s-2k.jpg', '&quot;floor&quot;:36', 'data-nlps-tour-small=', 'הדמיית פנים להמחשה בלבד', 'הדירה לדוגמה מבפנים', 'class="qp-legend"', 'data-nlps-phase="today"', 'data-nlps-phase="building"', 'data-nlps-phase="selling"', 'data-nlps-phase="permit"', '&quot;phase&quot;:&quot;selling&quot;', '&quot;occupancy&quot;:2030', 'שנת אכלוס מוצגת רק כשהעמוד נותן אותה', 'class="nlps-src"', 'מקורות הבמה: קו המגרש והבניינים הקיימים סביבו לפי עיריית <span>תל אביב-יפו</span>', '&quot;quarter&quot;:{&quot;projects&quot;:[{&quot;id&quot;:4745', '&quot;places&quot;:[{&quot;kind&quot;:&quot;rail&quot;', '&quot;id&quot;:4747', '&quot;id&quot;:4743', 'mapbox-gl-rtl-text/v0.3.0', '<b>תכנון</b>1.2024', 'data-lang="he"', '.nlcp-surr .nlcp-surr__map{display:none', 'body.nl-skin-a .nlsdt .nlsdt-title{color:#1B1A17', '32.10354', 'nlps-ctawrap', 'nlps-hero__cta', 'class="nlpf"', 'class="nlprog"', 'nadlan-ps-faq', 'nadlan-ps-importmap', '<div class="nlps-kicker">', 'class="nlpd"', 'data-nlps-floor="6"', 'data-nlps-floor="13"', 'דירות שנמכרו בריינבו תל אביב, לפי קומה', '#nla11y{position:fixed;bottom:calc(20px', 'id="nlhp-top"', '<style id="nadlan-hp-css">', 'id="nadlan-hp-js"'],
     ['<style id="nadlan-ps-css">', 'class="nlpc-site-header"', 'hero-m-780.jpg', 'על המפה החיה למטה', 'id="nl-project-page-title" class="screen-reader-text"', 'דירות 82-210', 'class="nlms"', 'class="nlcard-facts"', 'class="nlps-shell"', 'id="nlps-hint"', '<p class="nlps-kicker">', 'rainbow-tel-aviv-hero.jpg', 'בחירת דירה בתלת ממד', '#nla11y{position:fixed;top:50%', '🏫', 'תכנית עיצוב 1.2024'], ['"hero" "cta" "stage" "below" "lead"']),
    ("/projects/h-infinity-somail-tel-aviv/", ['nadlan-project-article', 'class="nlcard-facts"', '#nla11y{position:fixed;bottom:calc(20px', 'id="nlhp-top"', '<h1 id="nl-project-page-title" class="nlpt-h1">', '<style id="nadlan-pt-css">'], ['id="nl-project-page-title" class="screen-reader-text"', 'class="nlpc-site-header"', 'id="nlps"', 'nadlan-ps-importmap', 'nadlan-ps-bridge', 'class="nlps-page"', 'class="nlpd"']),
    ("/projects/dimri-yama-sde-dov/", ['nadlan-project-article', 'id="nlps"', 'nadlan-ps-importmap', 'class="nlps-page"', '<h1 id="nl-project-page-title" class="nlps-h1">דמרי ימה שדה דב'], ['id="nl-project-page-title" class="screen-reader-text"', 'class="nlpt-h1"']),
    ("/projects/duo-tel-aviv/", ['nadlan-project-article', 'data-lang="he"', 'mapbox-gl-rtl-text/v0.3.0', 'id="nlps"', 'nadlan-ps-importmap'], ['🏫']),
    ("/projects/rainbow-tel-aviv-en/", ['#nla11y{position:fixed;bottom:calc(20px + env(safe-area-inset-bottom,0px));left:20px'], ['#nla11y{position:fixed;bottom:calc(20px + env(safe-area-inset-bottom,0px));right:20px', 'id="nlhp-top"']),
    ("/en/", ['class="nlpb-phase__h"', 'Find and check', 'Find a broker', 'licensed brokers', 'class="nlhv2-langbar"', 'class="nlcta-wa"', '#nla11y{position:fixed;bottom:calc(20px + env(safe-area-inset-bottom,0px));left:20px'], ['#nla11y{position:fixed;bottom:calc(20px + env(safe-area-inset-bottom,0px));right:20px', 'id="nlhp-top"', 'nadlan-hp-css', 'id="nlhp-page"', 'class="nlhv2-prosgrid"', '★ 4.9']),
    ("/projects/", ['975</strong> פרויקטים בקטלוג: 942 מתחמי פינוי בינוי', 'ו־5 פרויקטי תמ״א 38, לפי עיר, יזם וסטטוס', 'סטטוס בנייה, יחידות, מיקום וכל', 'id="nadlan-pc49"', '.nldir-results .nldc-project .nldc-media{aspect-ratio:16/9}', 'id="nlhp-top"', '<style id="nadlan-hp-css">', '.nlhp-top{position', 'id="nadlan-hp-js"', 'class="nlhp-top wp-block-template-part"'], ['פרויקטים חדשים ודירות מקבלן בקטלוג', 'מיקום מדויק', 'class="nldcp-reg"', 'class="nlpc-site-header"', 'hero-m-780.jpg', 'מפת רחפן חיה', ' LIVE</span>', '#nlhp-page .nlhp-film{margin-top:40px', '#nlhp-hero .nlhp-search__go{']),
    ("/properties/?listing_type=sale", ['id="nlhp-top"', '<div class="nlpl"', 'דירות למכירה</h1>', 'aria-current="page">למכירה', 'class="nlpl-sep"', 'מודעה לדוגמה', '<span class="nlpl-deal">למכירה</span>', '₪ למ״ר'], ['class="nlpc-site-header"', 'hero-m-780.jpg', 'בדיקה משפטית מקדימה', 'class="nlag-badge"', 'class="nlcta-start"']),
    ("/properties/", ['id="nlhp-top"', '<div class="nlpl"', 'דירות למכירה ולהשכרה</h1>', 'class="nlpl-tabs"', 'class="nlpl-filters"', 'id="nadlan-pl-css"', 'רישיון 3131540', 'nlpl-deal--rent', 'לחודש', '+ פרסום מודעה בחינם', 'class="nlpl-pager"', '"@type":"ItemList"'], ['class="nlpc-site-header"', 'בדיקה משפטית מקדימה', 'נכסים למכירה והשקעה', 'class="nlag-badge"', 'class="nlag-grid"', 'class="nlcta-start"', 'מודעה לדוגמה', 'רשומות']),
    ("/properties/?city=%D7%A0%D7%95%D7%A4%D7%99%20%D7%99%D7%9D", ['<div class="nlpl"', 'דירות למכירה ולהשכרה בנופי ים</h1>', '<a class="nlpl-card" href=', 'נופי ים, תל אביב-יפו'], ['אין כרגע מודעות', 'class="nlpl-bar"><span><b>0</b>']),
    ("/properties/?city=%D7%A2%D7%99%D7%A8%D7%A9%D7%9C%D7%90%D7%A7%D7%99%D7%99%D7%9E%D7%AA", ['<div class="nlpl"', 'אין כרגע מודעות'], ['class="nlpl-bar"']),
    ("/properties/florentin-tlv-2r-rent-demo/", ['<section class="nlld-demo"', 'זו לא דירה אמיתית', 'id="nadlan-ld-css"', 'לדירות למכירה ולהשכרה', 'דירות אמיתיות באתר'], ['<form class="nlcard-claim-form"', 'nadlanVisit(this', 'id="nlsch"', '<div class="nlx-cta">', 'class="nlcta-start"', 'נכס לדוגמה - להמחשת', '👁️', '🗓️']),
    ("/properties/%d7%9c%d7%9e%d7%9b%d7%99%d7%a8%d7%94-%d7%91%d7%90%d7%95%d7%a4%d7%a7%d7%99%d7%9d-%d7%a9%d7%9b%d7%95%d7%a0%d7%aa-%d7%a9%d7%a4%d7%99%d7%a8%d7%90-%d7%a7%d7%95%d7%98%d7%92-5-%d7%97%d7%93%d7%a8%d7%99%d7%9d/", ['<div class="nlx-cta">', 'class="nlx-badge">באתר ', 'id="nlsch"', 'class="nlcta-start"'], ['<th>קומה</th><td>0</td>', '👁️', '🗓️', '🏙️', ' צפיות</span>', '<section class="nlld-demo"']),
    ("/post-listing/", ['<section class="nlpub-how"', 'איך זה עובד', 'עד 30 תמונות מהטלפון', 'id="nadlan-pub-css"', '#nlcta.is-mini .nlcta-wa', 'html body #nlcta.is-clear{bottom:calc(env(safe-area-inset-bottom,0px) + var(--nlcta-lift,150px))!important}', "box.classList.toggle('is-clear'", 'class="nlcta-wa"'], ['class="nlpc-site-header"']),
    ("/projects/duo-tel-aviv/", ['<h1 id="nl-project-page-title" class="nlps-h1">מגדלי דואו תל אביב', '<div class="nl-lead"><p>DUO Tel Aviv הוא פרויקט', 'class="bottom-line" data-nl-lead="1"', '.bottom-line[data-nl-lead]{display:none'], ['<h1 id="nl-project-page-title" class="screen-reader-text"', 'class="nlpt-h1"']),
    ("/projects/aurelia/", ['<h1 id="nl-project-page-title" class="nlpt-h1">Aurelia Sports', 'id="nadlan-pt-css"'], ['<h1 id="nl-project-page-title" class="screen-reader-text"']),
    ("/projects/rainbow-tel-aviv-en/", ['<h1 id="nl-project-page-title" class="nlps-h1">', 'class="nl-lead"'], ['<h1 id="nl-project-page-title" class="screen-reader-text"']),
    ("/?counts302=1", ['פרויקטים של בנייה חדשה והתחדשות עירונית, דירות למכירה ולהשכרה, מחירי דירות מעסקאות', 'בקטלוג, לפי עיר ויזם', 'הפרויקטים בקטלוג', 'פרויקטים של בנייה חדשה והתחדשות עירונית</a>', 'New-build and urban-renewal projects, prices from real deals, licensed professionals', 'content="נדל״ן בישראל: '], ['הפרויקטים החדשים ←', 'הפרויקטים החדשים</a>', 'apartment selection from inside the building', '</b> פרויקטים חדשים</span>', ' פרויקטים חדשים</a> ודירות מקבלן']),
    ("/?map303=1", ['<section class="nlhp-band nlhp-mapband" aria-labelledby="nlhp-map-h">', 'id="nlhp-map-h">מפת הפרויקטים</h2>', '<p class="nlhp-maplead">', ' הפרויקטים בקטלוג מסומנים על המפה, ב־', 'class="nldrone-legend"', '"nl-city-blk"', 'פרויקט שמיקומו ידוע רק ברמת העיר נספר בעיגול של העיר', 'ProjectMap v52', 'var styleReady=false;', 'if(styleReady){addData()}', 'function ckey(c)', 'var farz=map.getZoom()<IN;', ' ב־76 ערים', 'function listHtml(list)', 'class="nldrone-pop__list"', 'map.getZoom()>=15.2', '.nldrone-pop__list li{'], ['if(map.loaded()||map.isStyleLoaded()){addData()}', 'מפת הפרויקטים החדשים', 'nldrone-head__eyebrow', 'איפה תרצו לגור?', 'class="nlhv2-band nlhv2-dronemap"', 'mapbox-gl-rtl-text.js",null,true']),
    ("/en/?map303=1", ['>Project map</h2>', 'projects in the catalogue are on the map, in', 'class="nldrone-legend"', 'A project with a 3D model'], ['The Live Project Map', 'Where do you want to live?']),
    ("/wp-json/nadlan/v1/project-map", ['"ok":true', '"items":[', '"conf":"compound-verified"'], []),
    ("/property-value/?pl307=1", ['class="nlds nlpl"', 'data-pl="', 'id="nadlan-placement-css"', 'מיטל קציר'], ['/nadlan_placement/', 'class="nlpl-card"']),
    ("/?lb308=1", ['<section class="nlhp-band nlhp-lband" aria-labelledby="nlhp-list-h">', 'id="nlhp-list-h">מודעות חדשות באתר</h2>', ' המודעות</a>', 'class="nlhl-tabs" role="tablist"', 'id="nlhl-t-sale"', 'id="nlhl-rent"', 'class="nlhl-areas"', '<a class="nlpl-card" href=', 'class="nlpl-by"', 'id="nadlan-hp-lband-css"', 'id="nadlan-hp-lband-js"', '.nlpl-card{position:relative'], ['class="nlhv2-cityrow"', 'class="nlhv2-listtabs', 'nlpl-card--demo', 'data-pane="sale"', 'nlhv2-alt nlhp-listings"']),
    ("/?hm309=1", ['header#nlhp-top.nlhp-top.is-open{-webkit-backdrop-filter:none!important', 'body.nlhp-lock #nlcta{display:none!important}', '.nlhp-nav .nlhp-mega__col a span{display:inline', '<p class="nlhp-mega__h">לפי חדרים</p>', 'listing_type=sale&#038;rooms_min=3', 'כל הדירות למכירה<span>'], ['">דירות בירושלים</a>', '">להשכרה בירושלים</a>', '">דירות ברמת גן</a>']),
    ("/projects/?hm309=1", ['header#nlhp-top.nlhp-top.is-open{-webkit-backdrop-filter:none!important', 'body.nlhp-lock #nlcta{display:none!important}', '.nlhp-nav .nlhp-mega__col a span{display:inline', '<p class="nlhp-mega__h">לפי חדרים</p>', 'listing_type=sale&#038;rooms_min=3', 'כל הדירות למכירה<span>'], ['">דירות בירושלים</a>', '">להשכרה בירושלים</a>', '">דירות ברמת גן</a>']),
    ("/buying-apartment/?hm309=1", ['header#nlhp-top.nlhp-top.is-open{-webkit-backdrop-filter:none!important', 'body.nlhp-lock #nlcta{display:none!important}', '.nlhp-nav .nlhp-mega__col a span{display:inline', '<p class="nlhp-mega__h">לפי חדרים</p>', 'listing_type=sale&#038;rooms_min=3', 'כל הדירות למכירה<span>'], ['">דירות בירושלים</a>', '">להשכרה בירושלים</a>', '">דירות ברמת גן</a>']),
    ("/?sv310=1", ['id="nlhp-svc-h">לבעלי דירות, לדיירים ולקונים</h2>', '<span class="nlhp-svcard__body"><small>סיור וירטואלי</small><h3>רובע שדה דב, לפי התכנית</h3>', 'assets/home/tour-sdedov-dusk-960.jpg?ver=1.72.362', 'tour-sdedov-dusk-640.jpg?ver=1.72.362 640w', '<i class="nlhp-svcard__tag">הדמיה להמחשה</i>', '#nlhp-page .nlhp-svcard--tour{grid-column:1/-1'], ['בוחרים דירה מתוך הבניין', 'רובע שדה דב של 2035', 'sdedov-tour-poster.jpg']),
    ("/wp-content/plugins/nadlan-config/assets/home/tour-sdedov-dusk-640.jpg", [], []),
    ("/tour/sde-dov/?t311=1", ['<li><b>39</b> קומות</li>', '<li><b>459</b> דירות</li>', '<li>סטטוס: <b>בבנייה</b></li>', '<h2>שלושה פרויקטים ברובע</h2>', "liStBuild: 'סטטוס: <b>בבנייה</b>'", "const NARR_FIX_BASE = 'https://nad-lan.co.il/wp-content/plugins/nadlan-config/assets/tours/';", 'WebGLRenderer'], ['ולבחירת דירה', 'בחרו דירה מתוך הבניין', 'חופש בחירה מלא', '<b>כ־38</b>', 'Pick your home from the building itself', 'pick an apartment']),
    ("/tour/sde-dov/?year=2035&t311=1", ['<h2>שלושה פרויקטים ברובע</h2>'], ['ולבחירת דירה']),
    ("/tour/somail/?t312=1", ['<li>סטטוס: <b>בבנייה</b> · השלמה מתוכננת 2027, לפי דוחות החברה</li>', '<h2>DUO תל אביב, בלב המתחם</h2>', 'SOMAIL_FIX_312', "mmEnd: 'לפרויקטים במתחם'", '</html>'], ['ולבחירת דירה', 'בחרו דירה ב־DUO', 'לבחירתכם', '2026-2027', 'Pick your home at DUO']),
    ("/tour/somail/?year=2035&t312=1", ['SOMAIL_FIX_312'], ['ולבחירת דירה']),
    ("/tour/sde-dov/?t313=1", ['<style id="tour-phone-v59">', '#menuBtn{pointer-events:auto}', '#hud .hudside{display:contents}', 'NARR_FIX_BASE'], []),
    ("/wp-content/plugins/nadlan-config/assets/project-stage/tour.css?ver=1.72.362", ['min-height: 44px; min-width: 64px; border-radius: 999px; /* v61: 44px targets (HAD-346) */', '.nlat-viewer__x { flex: none; }', '.nlat-viewer__dirs button { padding: 0 12px; min-width: 64px; }'], ['min-height: 38px;', 'min-height: 34px;']),
    ("/wp-content/plugins/nadlan-config/assets/project-stage/rainbow/stage.css?ver=1.72.362", ['TouchTargets v62', '.rbs-qpin::after { content: ""; position: absolute; inset: -10px -3px; }', '.rbs-presets button::after'], []),
    ("/wp-content/plugins/nadlan-config/assets/nlds/nlds.css?ver=1.72.362", [':root body .nlds .qp-chip{display:inline-flex !important;align-items:center !important;gap:7px !important;min-height:44px', '.nlps-near__list > li{padding:12px 0 !important'], [':root body .nlds .qp-chip{display:inline-flex !important;align-items:center !important;gap:7px !important;min-height:36px']),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/slice.css?ver=1.72.362', ['grid-auto-rows: max-content', 'nlsl__glass'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/duo/stage.js?ver=1.72.362', ['floorPlan(n, tower)', 'FloorSlice v87', 'export function mountDuoStage'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/dimri/stage.js?ver=1.72.362', ['floorPlan(n, tower)', 'FloorSlice v87', 'export function mountDimriStage'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/ashira/stage.js?ver=1.72.362', ['floorPlan(n, tower)', 'FloorSlice v87', 'export function mountAshiraStage'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/slice.js?ver=1.72.362', ['const uid = (side)', 'export function openSlice'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/bridge.js?ver=1.72.362', ['tower: tw', 'nlps-slice'], []),
    ('/wp-content/plugins/nadlan-config/assets/showroom-engine/mapbox-init.js?ver=1.72.362', ['getRTLTextPluginStatus'], []),
    ('/projects/duo-tel-aviv/?t344=1', ['mountDuoStage', 'דירות שנמכרו במגדלי דואו תל אביב, לפי קומה'], []),
    ('/projects/ashira-sde-dov/?t344=1', ['mountAshiraStage'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/slice.js?ver=1.72.362', ['קו החזית והמרפסות כמו בדגם שעל הבמה', 'const uid = (side)'], ['המרפסות בגל, כמו על הבמה']),
    ('/projects/rainbow-tel-aviv-en/?nlstage=1&t346=1', ['id="nlps"', 'mountRainbowStage', 'id="nadlan-stage-i18n"', 'nadlan-stage-i18n-js', '<!-- nadlan-lang-pages en '], ['nlfilm', 'class="nlbsq"', 'nadlan-basket-cfg', 'class="nlpd"']),
    ('/projects/rainbow-tel-aviv/?t346=1', ['id="nlps"', 'nadlan-basket-cfg', 'nlfilm', 'class="nlpd"'], ['nadlan-stage-i18n']),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/rainbow/stage.js?ver=1.72.362', ['StageCard v94', 'camera.setViewOffset(fw, fh', 'rbs-label-min', 'setCardMin'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/rainbow/stage.css?ver=1.72.362', ['.rbs-label.is-min > :not(.rbs-label-top)', '.rbs-ui > .rbs-label { z-index: 2; }'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/duo/stage.js?ver=1.72.362', ['StageCard v94', 'camera.setViewOffset(fw, fh', 'rbs-label-min', 'setCardMin'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/duo/stage.css?ver=1.72.362', ['.rbs-label.is-min > :not(.rbs-label-top)', '.rbs-ui > .rbs-label { z-index: 2; }'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/dimri/stage.js?ver=1.72.362', ['StageCard v94', 'camera.setViewOffset(fw, fh', 'rbs-label-min', 'setCardMin'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/dimri/stage.css?ver=1.72.362', ['.rbs-label.is-min > :not(.rbs-label-top)', '.rbs-ui > .rbs-label { z-index: 2; }'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/ashira/stage.js?ver=1.72.362', ['StageCard v94', 'camera.setViewOffset(fw, fh', 'rbs-label-min', 'setCardMin'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/ashira/stage.css?ver=1.72.362', ['.rbs-label.is-min > :not(.rbs-label-top)', '.rbs-ui > .rbs-label { z-index: 2; }'], []),
    ('/projects/rainbow-tel-aviv/?t357=1', ['<button type="button" class="nlps-facbtn" data-nlps-phase="facilities" aria-pressed="false"><i aria-hidden="true">✦</i>המתקנים בפרויקט <b>5</b></button>', ':root body .nlps-stage:has(>.nlps-facbtn) .rbs-hint{top:66px}', 'rainbow/stage.js?ver=1.72.362', 'id="nlps"', 'data-nlps-phase="facilities" aria-pressed="false"'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/rainbow/stage.js?ver=1.72.362', ['StageFacilities v95: never under the facilities pill', 'StageFacilities v95: and the facilities pill', "querySelector('.nlps-facbtn')", 'StageCard v94'], []),
    ('/projects/duo-tel-aviv/?t357=1', ['<button type="button" class="nlps-facbtn" data-nlps-phase="facilities" aria-pressed="false"><i aria-hidden="true">✦</i>המתקנים בפרויקט <b>6</b></button>', ':root body .nlps-stage:has(>.nlps-facbtn) .rbs-hint{top:66px}', 'duo/stage.js?ver=1.72.362', 'id="nlps"', 'data-nlps-phase="facilities" aria-pressed="false"'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/duo/stage.js?ver=1.72.362', ['StageFacilities v95: never under the facilities pill', 'StageFacilities v95: and the facilities pill', "querySelector('.nlps-facbtn')", 'StageCard v94'], []),
    ('/projects/dimri-yama-sde-dov/?t357=1', ['<button type="button" class="nlps-facbtn" data-nlps-phase="facilities" aria-pressed="false"><i aria-hidden="true">✦</i>המתקנים בפרויקט <b>8</b></button>', ':root body .nlps-stage:has(>.nlps-facbtn) .rbs-hint{top:66px}', 'dimri/stage.js?ver=1.72.362', 'id="nlps"', 'data-nlps-phase="facilities" aria-pressed="false"'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/dimri/stage.js?ver=1.72.362', ['StageFacilities v95: never under the facilities pill', 'StageFacilities v95: and the facilities pill', "querySelector('.nlps-facbtn')", 'StageCard v94'], []),
    ('/projects/ashira-sde-dov/?t357=1', ['<button type="button" class="nlps-facbtn" data-nlps-phase="facilities" aria-pressed="false"><i aria-hidden="true">✦</i>המתקנים בפרויקט <b>7</b></button>', ':root body .nlps-stage:has(>.nlps-facbtn) .rbs-hint{top:66px}', 'ashira/stage.js?ver=1.72.362', 'id="nlps"', 'data-nlps-phase="facilities" aria-pressed="false"'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/ashira/stage.js?ver=1.72.362', ['StageFacilities v95: never under the facilities pill', 'StageFacilities v95: and the facilities pill', "querySelector('.nlps-facbtn')", 'StageCard v94'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/bridge.js?ver=1.72.362', ["on && x.getAttribute('data-nlps-phase') === b.getAttribute('data-nlps-phase')"], ["x === b && on ? 'true'"]),
    ('/projects/rainbow-tel-aviv/?t361=1', ['&quot;places&quot;:1', 'data-places="https://nad-lan.co.il/wp-content/plugins/nadlan-config/assets/project-stage/rainbow/places.json?ver=1.72.362"', 'assets/arealife/areamap.js?ver=1.72.362', 'window.NLPJX_AREALIFE?{}:', 'id="nlps"', 'id="nlpjx-unimap"'], []),
    ('/projects/dimri-yama-sde-dov/?t361=1', ['assets/arealife/areamap.js?ver=1.72.362', 'id="nlpjx-unimap"', 'window.NLPJX_POIS='], ['data-places=']),
    ('/projects/rainbow-tel-aviv-en/?t361=1', ['id="nadlan-stage-i18n"', 'this way', 'assets/arealife/areamap.js?ver=1.72.362', 'data-places='], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/rainbow/places.json?ver=1.72.362', ['"places":[', '"iso":[', '"sight":', '"fp":"https://findplace.co.il/he/'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/arealife.js?ver=1.72.362', ['AreaLife (design system AreaLife v97', 'export function looksFor', 'export function viewLayer'], []),
    ('/wp-content/plugins/nadlan-config/assets/arealife/areamap.js?ver=1.72.362', ['window.NLPJX_AREALIFE = 1', 'AreaMap (design system AreaLife v97', 'nlam-iso'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/bridge.js?ver=1.72.362', ['alReady', 'al.looksFor(sc)', 'function walkOpts(startId)'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/tour.js?ver=1.72.362', ['nlat-look', 'getComputedStyle(L.el).position', 'BuildingWalk v96'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/tour.css?ver=1.72.362', ['.nlat-look {', '.nlat-lift {'], []),
    ('/wp-content/plugins/nadlan-config/assets/pronet/procard.css?ver=1.72.362', ['ProNetwork v98', '.nlpn-cover{', '.nlpn-saved.is-on'], ['.nlpc{']),
    ('/wp-json/wp/v2/nadlan_professional/4348?_fields=meta&t362=1', ['"registry_number":"33668"'], ['"address":', '"phone":']),
    ('/professionals/meital-katzir/?t362=1', ['<h1 class="nlpp-name">מיטל קציר', 'nlpp-photo'], ['nlpp-mono']),
    ('/professionals/?profession=kablan&t362=1', ['<article class="nlpn', 'רשום בפנקס הקבלנים מאז', '<span class="nlpn-state"><i></i>מהפנקס הרשמי</span>', 'class="nlpn-mono"'], ['<a class="nldc nldc--pro']),
    ('/projects/?t362=1', ['id="nadlan-pc49"'], ['<article class="nlpn']),
    ('/projects/rainbow-tel-aviv-en/?t360=1', ['class="nlps-facbtn"', 'facilities <b>5</b>', 'id="nadlan-stage-i18n"', '"You are here"'], []),
    ('/projects/duo-tel-aviv-ru/?t360=1', ['class="nlps-facbtn"', 'Объекты проекта <b>6</b>', 'Гостиная квартиры-примера на 25-м этаже в DUO'], []),
    ('/projects/rainbow-tel-aviv/?t360=1', ['המתקנים בפרויקט <b>5</b>', 'id="nlps"'], ['id="nadlan-stage-i18n"']),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/tour.js?ver=1.72.362', ['nlat-lift__here', 'BuildingWalk v96'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/tour.css?ver=1.72.362', ['.nlat-lift__stop .nlat-lift__here', 'back points left'], ["content: ' · אתם כאן'"]),
    ('/projects/duo-tel-aviv/?t359=1', ['&quot;walk&quot;:{', '&quot;aptStops&quot;:[{&quot;to&quot;:&quot;25-w&quot;', '&quot;aptDoor&quot;:{&quot;n&quot;:[117.4,-5.4]', '&quot;to&quot;:&quot;25-s&quot;', 'id="nlps"', 'class="nlps-facbtn"'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/bridge.js?ver=1.72.362', ['walk.aptStops', 'function walkOpts(startId)', '/^\\d+-/.test(d.to)'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/duo/facilities.json?ver=1.72.362', ['"aptStops"', '"walk"', '"doors"', '"src": "fac-pool.jpg"'], []),
    ('/projects/rainbow-tel-aviv/?t358=1', ['&quot;walk&quot;:{', '&quot;aptDoor&quot;:{&quot;w&quot;:[128.8,-4.9]', '&quot;doors&quot;:[{&quot;to&quot;:&quot;lift&quot;', '&quot;stopSub&quot;', 'bridge.js?ver=1.72.362', 'id="nlps"', 'class="nlps-facbtn"'], []),
    ('/projects/duo-tel-aviv/?t358=1', ['id="nlps"', 'bridge.js?ver=1.72.362'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/tour.js?ver=1.72.362', ['BuildingWalk v96', 'function walkTo(id, arrival, back)', 'nlat-viewer__places', 'placeDoors();', 'never two viewers'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/tour.css?ver=1.72.362', ['.nlat-door {', '.nlat-lift {', '.nlat-viewer.is-fac .nlat-viewer__dirs', 'min-height: 44px; min-width: 64px;'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/bridge.js?ver=1.72.362', ['function walkOpts(startId)', "split('-').pop()", "on && x.getAttribute('data-nlps-phase')"], ["split('-')[1]"]),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/rainbow/facilities.json?ver=1.72.362', ['"aptDoor"', '"walk"', '"doors"'], []),
    ('/wp-json/wp/v2/nadlan_professional?per_page=3&t356=1', ['"meta":{'], ['"owner_user_id"', '"claim_status"', '"boost_multiplier"', '"nl_tier"', '"email"']),
    ('/wp-json/wp/v2/nadlan_project?per_page=3&t356=1', ['"meta":{'], ['"owner_user_id"', '"paid_tier"', '"_nadlan_private_unit_journey"', '"phone"']),
    ('/wp-json/wp/v2/nadlan_property?per_page=3&t356=1', ['"meta":{'], ['"owner_user_id"', '"nl_card_key"', '"claim_status"']),
    ('/professionals/?t356=1', ['<article class="nlpn'], ['<a class="nldc nldc--pro']),
    ('/projects/duo-tel-aviv/?t355=1', ['duo/stage.js?ver=1.72.362', 'id="nlps"'], []),
    ('/ar/?t354=1', ['<!-- nadlan-lang-pages ar ', '<a class="nlhv2-list" href="https://nad-lan.co.il/en/brokers/meital-katzir/'], ['אחוזה פרטית של 700', 'מיני פנטהאוז של 5 חדרים']),
    ('/projects/duo-tel-aviv/?t353=1', ['id="nlps-tour"', 'living-25w-card.jpg?ver=1.72.362', 'living-25s-2k.jpg', 'living-25n-2k.jpg', 'living-25e-2k.jpg', 'בגובה של כ־89 מ׳', 'id="nlps"', 'nadlan-project-article'], []),
    ('/projects/duo-tel-aviv-en/?t353=1', ['id="nlps-tour"', 'This apartment is in the south tower', 'Step into the lobby'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/duo/facilities.json?ver=1.72.362', ['"src": "fac-pool.jpg"', '"src": "fac-lobby.jpg"', '"src": "fac-wellness.jpg"', 'חדר כושר יוצא דופן בגודלו'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/duo/tour/fac-pool-2k.jpg?ver=1.72.362', [], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/duo/tour/fac-lobby-2k.jpg?ver=1.72.362', [], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/duo/tour/fac-wellness-2k.jpg?ver=1.72.362', [], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/duo/tour/living-25s-card.jpg?ver=1.72.362', [], []),
    ('/projects/rainbow-tel-aviv/?t353=1', ['.nlps-steps button,.nlps-steps a', 'living-25w-card.jpg?ver=1.72.362'], []),
    ('/projects/rainbow-tel-aviv/?t352=1', ['id="nlcta"', 'html body #nlcta.is-clear{bottom:calc(env(safe-area-inset-bottom,0px) + var(--nlcta-lift,150px))!important}', 'StagePillClear v91', "closest('#nlps,.nlps-steps,#nlps-view-cta')", '--nlcta-lift'], ['html body #nlcta.is-clear{bottom:calc(env(safe-area-inset-bottom,0px) + 150px)!important}']),
    ('/projects/duo-tel-aviv-ru/?t352=1', ['id="nlcta"', 'html body #nlcta.is-clear{bottom:calc(env(safe-area-inset-bottom,0px) + var(--nlcta-lift,150px))!important}', 'StagePillClear v91', "closest('#nlps,.nlps-steps,#nlps-view-cta')", '--nlcta-lift'], ['html body #nlcta.is-clear{bottom:calc(env(safe-area-inset-bottom,0px) + 150px)!important}']),
    ('/?t352=1', ['id="nlcta"', 'html body #nlcta.is-clear{bottom:calc(env(safe-area-inset-bottom,0px) + var(--nlcta-lift,150px))!important}', 'StagePillClear v91', "closest('#nlps,.nlps-steps,#nlps-view-cta')", '--nlcta-lift'], ['html body #nlcta.is-clear{bottom:calc(env(safe-area-inset-bottom,0px) + 150px)!important}']),
    ('/post-listing/?t352=1', ['id="nlcta"', 'html body #nlcta.is-clear{bottom:calc(env(safe-area-inset-bottom,0px) + var(--nlcta-lift,150px))!important}', 'StagePillClear v91', "closest('#nlps,.nlps-steps,#nlps-view-cta')", '--nlcta-lift'], ['html body #nlcta.is-clear{bottom:calc(env(safe-area-inset-bottom,0px) + 150px)!important}']),
    ('/projects/rainbow-tel-aviv-en/?t351=1', ['id="nlps"', 'id="nadlan-stage-i18n"', 'nadlan-ps-importmap', 'nadlan-project-article', 'class="nl-lead"', '<!-- nadlan-lang-pages en '], ['%D7%A9%D7%9C%D7%95%D7%9D%2C%20%D7%90%D7%A9%D7%9E%D7%97%20%D7%9C%D7%A7%D7%91%D7%9C%20%D7%AA%D7%95%D7%9B%D7%A0%D7%99%D7%95%D7%AA%20%D7%95%D7%9E%D7%97%D7%99%D7%A8%D7%99%D7%9D']),
    ('/projects/duo-tel-aviv-fr/?t351=1', ['id="nlps"', 'id="nadlan-stage-i18n"', 'nadlan-ps-importmap', 'nadlan-project-article', 'class="nl-lead"', '<!-- nadlan-lang-pages fr '], ['%D7%A9%D7%9C%D7%95%D7%9D%2C%20%D7%90%D7%A9%D7%9E%D7%97%20%D7%9C%D7%A7%D7%91%D7%9C%20%D7%AA%D7%95%D7%9B%D7%A0%D7%99%D7%95%D7%AA%20%D7%95%D7%9E%D7%97%D7%99%D7%A8%D7%99%D7%9D']),
    ('/projects/dimri-yama-sde-dov-ru/?t351=1', ['id="nlps"', 'id="nadlan-stage-i18n"', 'nadlan-ps-importmap', 'nadlan-project-article', 'class="nl-lead"', '<!-- nadlan-lang-pages ru '], ['%D7%A9%D7%9C%D7%95%D7%9D%2C%20%D7%90%D7%A9%D7%9E%D7%97%20%D7%9C%D7%A7%D7%91%D7%9C%20%D7%AA%D7%95%D7%9B%D7%A0%D7%99%D7%95%D7%AA%20%D7%95%D7%9E%D7%97%D7%99%D7%A8%D7%99%D7%9D']),
    ('/projects/ashira-sde-dov-ar/?t351=1', ['id="nlps"', 'id="nadlan-stage-i18n"', 'nadlan-ps-importmap', 'nadlan-project-article', 'class="nl-lead"', '<!-- nadlan-lang-pages ar '], ['%D7%A9%D7%9C%D7%95%D7%9D%2C%20%D7%90%D7%A9%D7%9E%D7%97%20%D7%9C%D7%A7%D7%91%D7%9C%20%D7%AA%D7%95%D7%9B%D7%A0%D7%99%D7%95%D7%AA%20%D7%95%D7%9E%D7%97%D7%99%D7%A8%D7%99%D7%9D']),
    ('/projects/rainbow-tel-aviv/?t351=1', ['id="nlps"', '%D7%A9%D7%9C%D7%95%D7%9D%2C%20%D7%90%D7%A9%D7%9E%D7%97%20%D7%9C%D7%A7%D7%91%D7%9C%20%D7%AA%D7%95%D7%9B%D7%A0%D7%99%D7%95%D7%AA%20%D7%95%D7%9E%D7%97%D7%99%D7%A8%D7%99%D7%9D%20%D7%91%D7%A8%D7%99%D7%99%D7%A0%D7%91%D7%95%20%D7%AA%D7%9C%20%D7%90%D7%91%D7%99%D7%91%20%28nad-lan.co.il%29'], ['id="nadlan-stage-i18n"', '<!-- nadlan-lang-pages']),
    ('/projects/zohi-sde-dov-en/?t351=1', ['nadlan-project-article', '<!-- nadlan-lang-pages en '], ['id="nlps"']),
    ('/projects/rainbow-tel-aviv-en/?nlstage=1&t350=1', ['id="nlps"', 'Hello%2C%20I%20would%20like%20plans%20and%20prices%20for%20Rainbow%20Tel%20Aviv%20%28nad-lan.co.il%29', 'Hello, I would like plans and prices for the apartment on floor {floor}', 'id="nadlan-ps-ltr"'], ['%D7%A9%D7%9C%D7%95%D7%9D%2C%20%D7%90%D7%A9%D7%9E%D7%97%20%D7%9C%D7%A7%D7%91%D7%9C%20%D7%AA%D7%95%D7%9B%D7%A0%D7%99%D7%95%D7%AA%20%D7%95%D7%9E%D7%97%D7%99%D7%A8%D7%99%D7%9D']),
    ('/projects/duo-tel-aviv-ru/?nlstage=1&t350=1', ['id="nlps"', '%D0%97%D0%B4%D1%80%D0%B0%D0%B2%D1%81%D1%82%D0%B2%D1%83%D0%B9%D1%82%D0%B5%2C%20%D1%85%D0%BE%D1%87%D1%83%20%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B8%D1%82%D1%8C%20%D0%BF%D0%BB%D0%B0%D0%BD%D0%B8%D1%80%D0%BE%D0%B2%D0%BA%D0%B8%20%D0%B8%20%D1%86%D0%B5%D0%BD%D1%8B%3A%20DUO%20Tel%20Aviv%20%28nad-lan.co.il%29'], []),
    ('/projects/rainbow-tel-aviv/?t350=1', ['%D7%A9%D7%9C%D7%95%D7%9D%2C%20%D7%90%D7%A9%D7%9E%D7%97%20%D7%9C%D7%A7%D7%91%D7%9C%20%D7%AA%D7%95%D7%9B%D7%A0%D7%99%D7%95%D7%AA%20%D7%95%D7%9E%D7%97%D7%99%D7%A8%D7%99%D7%9D%20%D7%91%D7%A8%D7%99%D7%99%D7%A0%D7%91%D7%95%20%D7%AA%D7%9C%20%D7%90%D7%91%D7%99%D7%91%20%28nad-lan.co.il%29', 'id="nlps"'], ['id="nadlan-stage-i18n"']),
    ('/ru/guides/new-apartment-mamad/?t350=1', ['>Районы<', '>За рубежом<', '>Гиды<'], ['>Востребованные районы<', '>Недвижимость за рубежом<']),
    ('/fr/guides/new-apartment-mamad/?t350=1', ['>Quartiers<', '>À l&#039;étranger<'], ['>Quartiers prisés<']),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/slice.js?ver=1.72.362', ["const LTR = !!(I18N && I18N.lang !== 'he' && I18N.lang !== 'ar');", "T('דירה לדוגמה')"], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/bridge.js?ver=1.72.362', ["L.wa(d.unit ? 'unit' : 'floor'"], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/rainbow/stage.js?ver=1.72.362', ["window.__nlStageI18n.wa('ask'"], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/duo/stage.js?ver=1.72.362', ["window.__nlStageI18n.wa('ask'"], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/dimri/stage.js?ver=1.72.362', ["window.__nlStageI18n.wa('ask'"], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/ashira/stage.js?ver=1.72.362', ["window.__nlStageI18n.wa('ask'"], []),
    ('/fr/?t349=1', ['<!-- nadlan-lang-pages fr ', '<a class="nlhv2-list" href="https://nad-lan.co.il/en/brokers/meital-katzir/'], ['<a class="nlhv2-list" href="https://nad-lan.co.il/properties/tzukei-aviv-3-rooms-berlin-for-sale/"']),
    ('/ru/?t349=1', ['<!-- nadlan-lang-pages ru ', '<a class="nlhv2-list" href="https://nad-lan.co.il/en/brokers/meital-katzir/'], []),
    ('/en/?t349=1', ['<a class="nlhv2-list" href="https://nad-lan.co.il/en/brokers/meital-katzir/'], []),
    ('/projects/rainbow-tel-aviv-en/?t349=1', ['"addressLocality":"Tel Aviv-Yafo"'], ['"addressLocality":"תל אביב יפו"']),
    ('/projects/rainbow-tel-aviv/?t349=1', ['"addressLocality":"תל אביב יפו"'], ['Tel Aviv-Yafo"']),
    ('/en/?t348=1', ['<!-- nadlan-lang-pages en ', '<meta property="og:locale" content="en_US"', '<meta property="og:site_name" content="NadLan"', 'class="nlhv2-langbar"', 'Find a broker', '/en/brokers/meital-katzir/'], ['Architectי', 'מContractor', 'הGuides', 'Projects, דירות', 'Проекты חדשים', '>לדלג לתוכן<', '>קטלוג תלת ממד<', 'content="he_IL"', ' - נדלן</title>']),
    ('/ru/?t348=1', ['<!-- nadlan-lang-pages ru ', 'content="ru_RU"'], ['Architectי', 'מContractor', 'הGuides', 'Projects, דירות', 'Проекты חדשים', '>לדלג לתוכן<']),
    ('/ar/?t348=1', ['<!-- nadlan-lang-pages ar ', 'content="ar_AR"'], ['>לדלג לתוכן<', 'content="he_IL"']),
    ('/en/guides/new-apartment-sale-specification/?t348=1', ['<!-- nadlan-lang-pages en ', 'content="en_US"', 'Skip to content', 'class="entry-content'], ['>לדלג לתוכן<', '>מפת האתר המלאה', 'content="he_IL"']),
    ('/projects/rainbow-tel-aviv-en/?t348=1', ['<!-- nadlan-lang-pages en ', '| NadLan</title>', '"name":"Home","item":"https://nad-lan.co.il/en/"', 'nadlan-project-article'], ['ובחירה מהבניין', '"name":"בית"']),
    ('/projects/rainbow-tel-aviv/?t348=1', ['"name":"בית","item":"https://nad-lan.co.il/"', 'content="he_IL"', 'nadlan-project-article'], ['<!-- nadlan-lang-pages', '| NadLan</title>', 'content="NadLan"']),
    ('/?t348=1', ['content="he_IL"'], ['<!-- nadlan-lang-pages', 'content="NadLan"']),
    ('/wp-content/plugins/nadlan-config/i18n/lang-other.json?t348=1', ['"exact"'], []),
    ('/projects/rainbow-tel-aviv-en/?nlstage=1&t347=1', ['id="nadlan-ps-ltr"', 'This file is printed inline', 'mountRainbowStage'], []),
    ('/projects/duo-tel-aviv/?t347=1', ['mountDuoStage', 'דירות שנמכרו במגדלי דואו תל אביב, לפי קומה'], []),
    ('/projects/rainbow-tel-aviv/?t342=1', ['sliceNote', 'mountRainbowStage', 'הדירות שנמכרו בפרויקט ופורסמו עם הקומה שלהן, לפי נתוני רשות המסים כפי שפורסמו בעיתונות', 'living-25w-card.jpg'], ['מכירה מוקדמת לבעלי עניין']),
    ('/projects/duo-tel-aviv/?t342=1', ['דירות שנמכרו במגדלי דואו תל אביב, לפי קומה', 'לפי דיווח החברה: מכירה מוקדמת לבעלי עניין', '372 מתוך 510', 'data-nlps-floor="17"', 'mountDuoStage'], ['הדירות שנמכרו בפרויקט ופורסמו עם הקומה שלהן, לפי נתוני רשות המסים כפי שפורסמו בעיתונות']),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/rainbow/stage.js?ver=1.72.362', ['floorPlan(n)', 'FloorSlice v87', 'export function mountRainbowStage'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/bridge.js?ver=1.72.362', ['nlps-slice', "'./slice.js'", 'nl:facility-tour'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/slice.js?ver=1.72.362', ['export function openSlice', 'חתך להמחשה'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/slice.css?ver=1.72.362', ['nlsl__glass'], []),
    ('/projects/first-sde-dov/?t341=1', ['<meta name="description" content="FIRST שדה דב של קבוצת חגג'], ['content="כל המידע על']),
    ('/projects/yoo-tel-aviv/?t341=1', ['<meta name="description" content="מגדלי YOO בפארק צמרת הם שני מגדלי מגורים'], ['content="כל המידע על']),
    ('/projects/rainbow-tel-aviv/?t341=1', ['<meta name="description" content="ריינבו תל אביב (Rainbow Tel Aviv) של ישראל קנדה בשדה דב'], ['content="כל המידע על']),
    ('/projects/ashira-sde-dov/?t341=1', ['<title>פרויקט אשירה שדה דב (ASHIRA) של אביסרור | מחירים ודירות | נדלן</title>'], ['content="כל המידע על']),
    ('/projects/%D7%94%D7%92%D7%A4%D7%9F-8-10-%D7%A8%D7%92/?t341=1', ['<meta name="description" content="'], ['content="דירות למכירה ב', 'content="כל המידע על']),
    ('/projects/rainbow-tel-aviv/?t340=1', ['id="nadlan-basket-cfg"', 'assets/basket/basket.js', 'assets/basket/basket.css', '"slug":"rainbow-tel-aviv"', 'לעזרה: המחיר הממוצע בדירות שנמכרו בפרויקט עד 3.2026', 'living-25w-card.jpg', 'data-nlps-tour-title="קומה 25 · לכיוון הים"', 'mountRainbowStage'], []),
    ('/projects/duo-tel-aviv/?t340=1', ['id="nadlan-basket-cfg"', 'mountDuoStage', 'כ-71,000 ₪ למ״ר לפני מע״מ'], []),
    ('/projects/ashira-sde-dov/?t340=1', ['id="nadlan-basket-cfg"', 'mountAshiraStage'], ['"hint":"לעזרה']),
    ('/projects/h-infinity-somail-tel-aviv/?t340=1', ['nadlan-project-article'], ['nadlan-basket-cfg', 'assets/basket/basket.js']),
    ('/projects/rainbow-tel-aviv-en/?t340=1', ['<!-- nadlan-lang-pages en '], ['nadlan-basket-cfg']),
    ('/wp-json/nadlan/v1/basket/pros?profession=lawyer&city=%D7%AA%D7%9C%20%D7%90%D7%91%D7%99%D7%91%20%D7%99%D7%A4%D7%95&t340=1', ['"ok":true', '"pros":'], ['is_demo']),
    ('/wp-content/plugins/nadlan-config/assets/basket/basket.js?ver=1.72.362', ['nl-basket:', 'nlbk__legal', 'nl:facing'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/duo/stage.js?ver=1.72.362', ['rbs-qcard-360', 'export function mountDuoStage'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/ashira/stage.css?ver=1.72.362', ['rbs-qcard-360b'], []),
    ('/projects/rainbow-tel-aviv/?t339=1', ['living-25n-warm.jpg', 'living-25e-stone-thumb.jpg', 'living-25s-light-2k.jpg', 'living-25w-warm.jpg', 'mountRainbowStage'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/rainbow/tour/living-25s-stone-thumb.jpg?ver=1.72.362', [], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/rainbow/tour/living-25e-warm-2k.jpg?ver=1.72.362', [], []),
    ('/projects/rainbow-tel-aviv-en/?t339=1', ['Before you call the developer', '<!-- nadlan-lang-pages en '], ['Real estate - before you approach the developer']),
    ('/projects/rainbow-tel-aviv-en/?t338=1', ['<!-- nadlan-lang-pages en ', 'What does an apartment cost in Tel Aviv-Yafo?', 'Price: where the project stands against its area', 'Everything around the project', 'Accessibility statement', 'nadlan-project-article'], ['aria-label="מחירי הסביבה"']),
    ('/projects/duo-tel-aviv-ar/?t338=1', ['<!-- nadlan-lang-pages ar ', 'أسعار المنطقة', 'كم يبلغ سعر شقة في تل أبيب يافا؟', 'nadlan-project-article'], ['aria-label="מחירי הסביבה"']),
    ('/projects/dimri-yama-sde-dov-ru/?t338=1', ['<!-- nadlan-lang-pages ru ', 'На каком этапе проект', 'Сколько стоит квартира в городе Тель-Авив-Яффо?'], ['aria-label="מחירי הסביבה"']),
    ('/projects/the-park-bnei-brak-fr/?t338=1', ['<!-- nadlan-lang-pages fr ', 'Bnei Brak'], ['כמה עולה דירה ב', 'מחיר: איפה הפרויקט עומד מול הסביבה', 'כל מה שסביב הפרויקט', 'aria-label="מחירי הסביבה"']),
    ('/projects/rainbow-tel-aviv/?t338=1', ['מחירי הסביבה', 'כל מה שסביב הפרויקט', 'mountRainbowStage'], ['nadlan-lang-pages']),
    ('/projects/h-infinity-somail-tel-aviv/?t338=1', ['מחירי הסביבה', 'כל מה שסביב הפרויקט', 'nadlan-project-article'], ['nadlan-lang-pages']),
    ('/projects/rainbow-tel-aviv/?t337=1', ['fac-roofpool.jpg', 'fac-club.jpg', 'fac-lobby.jpg', 'mountRainbowStage'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/rainbow/stage.js?ver=1.72.362', ['rbs-qcard-360', 'nl:facility-tour'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/bridge.js?ver=1.72.362', ['nl:facility-tour', 'מתקן לדוגמה'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/rainbow/stage.css?ver=1.72.362', ['rbs-qcard-360b'], []),
    ('/projects/dimri-yama-sde-dov/?t336=1', ['mountDimriStage', 'project-stage/dimri/stage.js', 'Dimri Yama Sde Dov', 'data-nlps-phase="facilities"', 'הדמיה של דמרי ימה ברובע שדה דב', 'כ-700 מטר מקו המים', 'id="nlsch"', 'data-nlps-ev="hero-video"'], ['קו ראשון', 'data-nlps-step="inside"', 'מגדל ובנייני בוטיק סביב גינה']),
    ('/projects/ashira-sde-dov/?t336=1', ['id="nlps"', 'mountAshiraStage', 'project-stage/ashira/stage.js', 'class="nlps-h1"', 'פרויקט אשירה שדה דב', 'Ashira Sde Dov', 'data-nlps-phase="facilities"', 'הדמיה של פרויקט אשירה ברובע שדה דב', 'nadlan-project-article', 'id="nlsch"'], ['data-nlps-step="inside"', 'class="nlpt-h1"']),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/dimri/stage.js?ver=1.72.362', ['export function mountDimriStage'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/ashira/stage.js?ver=1.72.362', ['export function mountAshiraStage'], []),
    ('/projects/dimri-yama-sde-dov-en/?t336=1', ['nadlan-project-article'], []),
    ('/projects/rainbow-tel-aviv/?t335=1', ['living-25w-warm.jpg', 'living-25w-stone-thumb.jpg', 'warm', 'data-nlps-tour-scenes', 'data-nlps-ev="hero-film"'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/tour.js?ver=1.72.362', ['nlat-viewer__styles', 'applyStyle', 'getView'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/tour.css?ver=1.72.362', ['.nlat-viewer__styles', '.nlat-style'], []),
    ('/projects/duo-tel-aviv/?t335=1', ['mountDuoStage', 'data-nlps-tour-scenes'], []),
    ('/projects/rainbow-tel-aviv/?t334=1', ['id="nadlan-together-chooser-js"', 'data-nlps-ev="hero-video"', 'data-nlps-ev="hero-film"', 'mountRainbowStage'], ['id="nltg-root"', 'nadlan-together-css']),
    ('/projects/duo-tel-aviv/?t334=1', ['id="nadlan-together-chooser-js"', 'mountDuoStage'], ['id="nltg-root"']),
    ('/wp-json/nadlan/v1/room/available', ['"now"'], []),
    ('/wp-content/plugins/nadlan-config/assets/together/together.js?ver=1.72.362', ['nltg'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/rainbow/stage.js?ver=1.72.362', ['getView', 'pickPoint', 'mountRainbowStage'], []),
    ('/projects/h-infinity-somail-tel-aviv/?t334=1', ['nadlan-project-article'], ['id="nadlan-together-chooser-js"']),
    ('/projects/duo-tel-aviv/?t333=1', ['id="nlps"', 'mountDuoStage', 'project-stage/duo/stage.js', 'class="nlps-h1"', 'מגדלי דואו תל אביב', 'DUO Tel Aviv', 'data-nlps-phase="facilities"', 'הדמיה של מגדלי דואו תל אביב', 'שכבות המגרשים, המבנים, הרחובות', 'id="nlsch"', 'nadlan-project-article'], ['מגדל ובנייני בוטיק סביב גינה', 'class="nlpt-h1"']),
    ('/projects/rainbow-tel-aviv/?t333=1', ['data-nlps-step="inside"', 'מגדל ובנייני בוטיק סביב גינה', 'mountRainbowStage', 'data-nlps-ev="hero-film"'], ['mountDuoStage']),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/duo/stage.js?ver=1.72.362', ['export function mountDuoStage'], []),
    ('/projects/duo-tel-aviv-en/?t333=1', ['nadlan-project-article'], []),
    ('/projects/rainbow-tel-aviv/?t332=1', ['<button type="button" class="nlfilm-x" aria-label="סגירה">&#10005;</button><div class="nlfilm-box">', 'top:-56px', 'calc(100svh - 176px)', 'data-nlps-ev="hero-film"'], ['<div class="nlfilm-box"><button']),
    ('/projects/rainbow-tel-aviv/?t331=1', ['data-nlps-ev="hero-film"', 'id="nlfilm"', '"@type":"VideoObject"', 'rainbow-tel-aviv-film-wide.mp4', 'rainbow-tel-aviv-film-tall.mp4', 'סרטון הפרויקט', 'data-nlps-ev="hero-video"', 'id="nadlan-ps-faq"'], []),
    ('/projects/duo-tel-aviv/?t331=1', ['id="nlsch"'], ['id="nlfilm"', 'VideoObject']),
    ('/tour/somail/?t330=1', ["un: 278, f: '53 + 7'", 'בבנייה — לפי דוח החברה לשנת 2025', '[-30, 2, 13, 27, 7]'], ["un: 200, f: '52 + 7'"]),
    ('/tour/sde-dov/?t330=1', ["tagDimri: 'מגורים ומלון'", "finSpan1: 'מגורים ומלון · 39 קומות · 458 דירות'"], ["tagDimri: 'קו ראשון לים'", 'קו ראשון לים · 39 קומות']),
    ('/projects/rainbow-tel-aviv/?t329=1', ['ProjectDossier v74', '> table td small{display:block !important', 'ProjectDossier v67'], []),
    ('/projects/dimri-yama-sde-dov/?t329=1', ['ProjectDossier v74', 'ProjectDossier v67'], []),
    ('/projects/rainbow-tel-aviv/?t328=1', ['data-nlps-ev="hero-video"', 'id="nlsch"', 'data-kind="video"', 'שיחת וידאו עם נציג נדל״ן'], []),
    ('/projects/duo-tel-aviv/?t328=1', ['id="nlsch"', 'data-kind="video"', 'שיחת וידאו עם נציג נדל״ן', 'אינה מטעם היזם', 'data-nlps-ev="hero-video"'], []),
    ('/projects/duo-tel-aviv-en/?t328=1', ['id="nlsch"', 'A video call with a NadLan advisor'], []),
    ('/projects/rainbow-tel-aviv/?t327=1', ['data-nlps-phase="facilities"', 'qp-dot--facilities', '&quot;facilities&quot;', '&quot;roof:3&quot;'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/rainbow/stage.js?ver=1.72.362', ['FacilityHotspots v72', 'function openFacilityCard(it)', "facMode = ph === 'facilities'"], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/rainbow/stage.css?ver=1.72.362', ['FacilityHotspots v72', '.rbs-qpin--facility {', '.rbs-fic--pool {'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/bridge.js?ver=1.72.362', ['facilities: Array.isArray(cfg.facilities)'], []),
    ('/wp-content/plugins/nadlan-config/assets/project-stage/rainbow/facilities.json', ['FacilityHotspots v72', 'roof:3'], []),
    ('/projects/duo-tel-aviv/?t327=1', ['id="nlcta"', 'data-nlps-phase="facilities"'], []),
    ('/tour/sde-dov/?t326=1', ['<script id="tour-wa-v71s">', 'body.cardOpen #waFab{opacity:1!important;pointer-events:auto!important}', "encodeURIComponent(t+'\\n\\n'+s)"], []),
    ('/tour/somail/?t326=1', ['<script id="tour-wa-v71s">', 'body.cardOpen #waFab{opacity:1!important;pointer-events:auto!important}', "encodeURIComponent(t+'\\n\\n'+s)"], []),
    ('/?t326=1', ['v71: encodeURIComponent keeps spaces as %20', 'id="nadlan-wa-source"'], ['u.searchParams.set("text",(t?t:"")+stamp);']),
    ('/brokers/meital-katzir/?t325=1', ['<style id="nlcta-owned">', '@media (min-width:721px){html body .nlb .nlb-mbar{display:block;position:fixed;bottom:20px;inset-inline-end:20px;z-index:9990;', 'class="nlb-mbar"', 'wa.me/972523631582'], []),
    ('/site-map/?t325=1', ['<meta name="viewport" content="width=device-width, initial-scale=1">', 'id="nlcta"'], []),
    ('/buying-apartment/?t325=1', ['id="nlcta"'], []),
    ('/?t324=1', ['id="nlcta"', 'class="nlcta-wa"', 'PublishPage v48-69', 'html body #nlcta.is-clear{bottom:calc(env(safe-area-inset-bottom,0px) + var(--nlcta-lift,150px))!important}'], ['html body #nlcta.is-typing,html body #nlcta.is-clear{display:none!important}', 'body.nadlan-p3d-stage-active #nlcta{display:none}', 'body.single-nadlan_project #nlcta { display: none !important; }']),
    ('/projects/?t324=1', ['id="nlcta"', 'class="nlcta-wa"', 'PublishPage v48-69', 'html body #nlcta.is-clear{bottom:calc(env(safe-area-inset-bottom,0px) + var(--nlcta-lift,150px))!important}'], ['html body #nlcta.is-typing,html body #nlcta.is-clear{display:none!important}', 'body.nadlan-p3d-stage-active #nlcta{display:none}', 'body.single-nadlan_project #nlcta { display: none !important; }']),
    ('/projects/duo-tel-aviv/?t324=1', ['id="nlcta"', 'class="nlcta-wa"', 'PublishPage v48-69', 'html body #nlcta.is-clear{bottom:calc(env(safe-area-inset-bottom,0px) + var(--nlcta-lift,150px))!important}'], ['html body #nlcta.is-typing,html body #nlcta.is-clear{display:none!important}', 'body.nadlan-p3d-stage-active #nlcta{display:none}', 'body.single-nadlan_project #nlcta { display: none !important; }']),
    ('/properties/?t324=1', ['id="nlcta"', 'class="nlcta-wa"', 'PublishPage v48-69', 'html body #nlcta.is-clear{bottom:calc(env(safe-area-inset-bottom,0px) + var(--nlcta-lift,150px))!important}'], ['html body #nlcta.is-typing,html body #nlcta.is-clear{display:none!important}', 'body.nadlan-p3d-stage-active #nlcta{display:none}', 'body.single-nadlan_project #nlcta { display: none !important; }']),
    ('/brokers/?t324=1', ['id="nlcta"', 'class="nlcta-wa"', 'PublishPage v48-69', 'html body #nlcta.is-clear{bottom:calc(env(safe-area-inset-bottom,0px) + var(--nlcta-lift,150px))!important}'], ['html body #nlcta.is-typing,html body #nlcta.is-clear{display:none!important}', 'body.nadlan-p3d-stage-active #nlcta{display:none}', 'body.single-nadlan_project #nlcta { display: none !important; }']),
    ('/buying-apartment/?t324=1', ['id="nlcta"', 'class="nlcta-wa"', 'PublishPage v48-69', 'html body #nlcta.is-clear{bottom:calc(env(safe-area-inset-bottom,0px) + var(--nlcta-lift,150px))!important}'], ['html body #nlcta.is-typing,html body #nlcta.is-clear{display:none!important}', 'body.nadlan-p3d-stage-active #nlcta{display:none}', 'body.single-nadlan_project #nlcta { display: none !important; }']),
    ('/en/?t324=1', ['id="nlcta"', 'class="nlcta-wa"', 'PublishPage v48-69', 'html body #nlcta.is-clear{bottom:calc(env(safe-area-inset-bottom,0px) + var(--nlcta-lift,150px))!important}'], ['html body #nlcta.is-typing,html body #nlcta.is-clear{display:none!important}', 'body.nadlan-p3d-stage-active #nlcta{display:none}', 'body.single-nadlan_project #nlcta { display: none !important; }']),
    ('/site-map/?t324=1', ['id="nlcta"', 'class="nlcta-wa"', 'PublishPage v48-69', 'html body #nlcta.is-clear{bottom:calc(env(safe-area-inset-bottom,0px) + var(--nlcta-lift,150px))!important}'], ['html body #nlcta.is-typing,html body #nlcta.is-clear{display:none!important}', 'body.nadlan-p3d-stage-active #nlcta{display:none}', 'body.single-nadlan_project #nlcta { display: none !important; }']),
    ('/post-listing/?t324=1', ['id="nlcta"', 'class="nlcta-wa"', 'PublishPage v48-69', 'html body #nlcta.is-clear{bottom:calc(env(safe-area-inset-bottom,0px) + var(--nlcta-lift,150px))!important}'], ['html body #nlcta.is-typing,html body #nlcta.is-clear{display:none!important}', 'body.nadlan-p3d-stage-active #nlcta{display:none}', 'body.single-nadlan_project #nlcta { display: none !important; }']),
    ('/mortgage-calculator/?t324=1', ['id="nlcta"', 'class="nlcta-wa"', 'PublishPage v48-69', 'html body #nlcta.is-clear{bottom:calc(env(safe-area-inset-bottom,0px) + var(--nlcta-lift,150px))!important}'], ['html body #nlcta.is-typing,html body #nlcta.is-clear{display:none!important}', 'body.nadlan-p3d-stage-active #nlcta{display:none}', 'body.single-nadlan_project #nlcta { display: none !important; }']),
    ('/professionals/?t324=1', ['id="nlcta"', 'class="nlcta-wa"', 'PublishPage v48-69', 'html body #nlcta.is-clear{bottom:calc(env(safe-area-inset-bottom,0px) + var(--nlcta-lift,150px))!important}'], ['html body #nlcta.is-typing,html body #nlcta.is-clear{display:none!important}', 'body.nadlan-p3d-stage-active #nlcta{display:none}', 'body.single-nadlan_project #nlcta { display: none !important; }']),
    ('/projects/duo-tel-aviv/?t323=1', ['DS PublishPage v68', 'id="nlcta"', 'nlcta-wa'], ['body.single-nadlan_project #nlcta { display: none !important; }']),
    ('/projects/h-infinity-somail-tel-aviv/?t323=1', ['DS PublishPage v68', 'id="nlcta"', 'nlcta-wa'], ['body.single-nadlan_project #nlcta { display: none !important; }']),
    ('/projects/einstein-tower/?t323=1', ['DS PublishPage v68', 'id="nlcta"', 'nlcta-wa'], ['body.single-nadlan_project #nlcta { display: none !important; }']),
    ('/projects/rainbow-tel-aviv/?t323=1', ['DS PublishPage v68', 'id="nlcta"', 'nlcta-wa'], ['body.single-nadlan_project #nlcta { display: none !important; }']),
    ('/projects/ashira-sde-dov-en/?t323=1', ['DS PublishPage v68', 'id="nlcta"', 'nlcta-wa'], ['body.single-nadlan_project #nlcta { display: none !important; }']),
    ('/projects/rainbow-tel-aviv/?t322=1', ['ProjectDossier v67', 'html body.nlpc-project-page .nadlan-project-article > table{width:100% !important;margin:18px 0 26px !important;', 'html body.nlpc-project-page .nadlan-project-article > table tr:has(> :nth-child(3)) > :first-child{grid-column:1 / -1 !important}', 'ProjectFrame v63', 'TouchTargets v66', '<th>שם הפרויקט</th>'], []),
    ('/projects/dimri-yama-sde-dov/?t322=1', ['ProjectDossier v67', 'html body.nlpc-project-page .nadlan-project-article > table{width:100% !important;margin:18px 0 26px !important;', 'html body.nlpc-project-page .nadlan-project-article > table tr:has(> :nth-child(3)) > :first-child{grid-column:1 / -1 !important}', 'ProjectFrame v63', 'TouchTargets v66', '<th dir="rtl">משמעות לרוכש</th>'], ['ProjectDossier v64', 'ProjectDossier v65']),
    ('/projects/ashira-sde-dov/?t322=1', ['ProjectDossier v67', 'html body.nlpc-project-page .nadlan-project-article .nlv2-data-grid{display:grid !important;', 'class="nlv2-data-grid"'], []),
    ('/projects/h-infinity-somail-tel-aviv/?t322=1', ['ProjectFrame v63'], ['ProjectDossier v67', 'ProjectDossier v64', 'ProjectDossier v65']),
    ('/projects/duo-tel-aviv/?t321=1', ['.nlptop-c a{color:#6B4E1E;text-decoration:none;display:inline-block;padding:14px 3px 10px;margin:-14px -3px -10px}', '.nlptop-l a::after{content:"";position:absolute;inset:0 -2px -18px}', '.nlfc-hero .nlfc{row-gap:10px}.nlfc-hero .nlfc-chip{font-size:12.5px;padding:8.5px 13px;position:relative}', 'font-weight:700;border-radius:8px;padding:9px 14px}', 'display:inline-block;padding:14px 6px;margin:-14px -6px;color:#9C7A3C', '.nlpjx-comps a,.nlpjx-price-mapnote a,.nlpjx-fin-est a{display:inline-block;padding:13px 0;margin:-13px 0}', 'ProjectFrame v63', 'ProjectDossier v64'], ['.nlptop-c a{color:#6B4E1E;text-decoration:none}', 'border-radius:8px;padding:7px 14px}']),
    ('/projects/dimri-yama-sde-dov/?t321=1', ['.nlsdt-cta2{display:block;margin:0 0 -20px;padding:10px 0 20px;text-align:center}', 'padding:15px 0;margin-top:-15px;margin-bottom:-15px;color:#F2C14E'], ['.nlsdt-cta2{display:block;margin:10px 0 0;text-align:center}']),
    ('/projects/ashira-sde-dov/?t321=1', ['html body .nlv2-source-list > li{padding-block:4px !important}', '.nlv2-source-list a{display:inline-block;padding:8px 0;margin:-8px 0}'], []),
    ('/buying-apartment/?t321=1', ['display:inline-block;padding:14px 6px;margin:-14px -6px;color:#9C7A3C', '/site-map/'], []),
    ('/projects/einstein-tower/?t320=1', ['ProjectDossier v65', 'html body.nlpc-project-page .nadlan-project-article .nlfs-article .nlfs-fact-grid{display:grid !important;grid-template-columns:1fr 1fr !important;', 'html body.nlpc-project-page .nadlan-project-article .nlfs-article .nlfs-article__toc br{display:none !important}', 'html body.nlpc-project-page .nadlan-project-article .nlfs-article .nlfs-section details > summary{display:flex !important;', 'ProjectFrame v63', 'class="nlfs-fact-grid"', 'שם השיווק', '<summary>האם איינשטיין 18 היא הכתובת הרשמית של הפרויקט?</summary>', 'nadlan-einstein-he-dossier-v1'], ['ProjectDossier v64']),
    ('/projects/duo-tel-aviv/?t320=1', ['ProjectDossier v64', 'ProjectFrame v63'], ['ProjectDossier v65']),
    ('/projects/dimri-yama-sde-dov/?t320=1', ['ProjectFrame v63', 'nadlan-project-article'], ['ProjectDossier v64', 'ProjectDossier v65']),
    ('/projects/duo-tel-aviv/?t319=1', ['ProjectDossier v64', 'html body.nlpc-project-page .nadlan-project-article .project-article .buyer-checklist > p::before{content:counter(nlchk);', 'html body.nlpc-project-page .nadlan-project-article .project-article .data-table tr{display:grid !important;', 'html body.nlpc-project-page .nadlan-project-article .project-article .fact-card > br{display:none !important}', 'ProjectFrame v63', 'class="fact-cards"', 'הבדיקה הראשונה היא זיהוי הנכס', '<h3>מה הכתובת הרשמית של DUO Tel Aviv?</h3>', '<th>שם הפרויקט</th>'], []),
    ('/projects/duo-tel-aviv/?t318=1', ['ProjectFrame v63', 'html body.nlpc-project-page .nlpc-main .wp-block-post-content.is-layout-constrained > *{box-sizing:border-box;max-width:min(1400px, calc(100% - 24px)) !important;margin-inline:auto !important}', 'html body.nlpc-project-page .nlpc-main .wp-block-post-content.is-layout-constrained > .nadlan-project-article{max-width:min(812px, calc(100% - 24px)) !important;padding-inline:16px !important}', 'html body.nlpc-project-page .nlpc-main .wp-block-post-content.is-layout-constrained > .nlps-page{max-width:100% !important}', '@media(max-width:600px){.nlpjx-maplayers button{min-height:44px}}'], []),
    ('/projects/einstein-tower/?t318=1', ['ProjectFrame v63', 'html body.nlpc-project-page .nlpc-main .wp-block-post-content.is-layout-constrained > *{box-sizing:border-box;max-width:min(1400px, calc(100% - 24px)) !important;margin-inline:auto !important}', 'html body.nlpc-project-page .nlpc-main .wp-block-post-content.is-layout-constrained > .nadlan-project-article{max-width:min(812px, calc(100% - 24px)) !important;padding-inline:16px !important}', 'html body.nlpc-project-page .nlpc-main .wp-block-post-content.is-layout-constrained > .nlps-page{max-width:100% !important}', '@media(max-width:600px){.nlpjx-maplayers button{min-height:44px}}'], []),
    ('/projects/ashira-sde-dov-en/?t318=1', ['ProjectFrame v63', 'html body.nlpc-project-page .nlpc-main .wp-block-post-content.is-layout-constrained > *{box-sizing:border-box;max-width:min(1400px, calc(100% - 24px)) !important;margin-inline:auto !important}', 'html body.nlpc-project-page .nlpc-main .wp-block-post-content.is-layout-constrained > .nadlan-project-article{max-width:min(812px, calc(100% - 24px)) !important;padding-inline:16px !important}', 'html body.nlpc-project-page .nlpc-main .wp-block-post-content.is-layout-constrained > .nlps-page{max-width:100% !important}', '@media(max-width:600px){.nlpjx-maplayers button{min-height:44px}}'], []),
    ("/projects/rainbow-tel-aviv/?t317=1", ['@media(max-width:600px){.nlpjx-maplayers button{min-height:44px}}', 'ProjectFrame v63', "html body.nlpc-project-page .nlpc-main .wp-block-post-content.is-layout-constrained > .nlps-page{max-width:100% !important}"], []),
    ("/tour/sde-dov/?t314=1", ["yearNow: 'Today<small>2026</small>', yearQ: 'The quarter<small>2035</small>'", "['#year2026', 'yearNow'], ['#year2035', 'yearQ'],", '#exHelp{top:calc(406px + env(safe-area-inset-top))', 'top:calc(196px + env(safe-area-inset-top));padding:7px 7px 6px}'], ['top:calc(232px + env(safe-area-inset-top));padding:7px 7px 6px}']),
    ("/tour/somail/?t314=1", ["yearQ: 'The compound<small>2035</small>'", "['#year2026', 'yearNow'], ['#year2035', 'yearQ'],", '#exHelp{top:calc(406px + env(safe-area-inset-top))'], ['top:calc(232px + env(safe-area-inset-top));padding:7px 7px 6px}']),
    ("/tour/somail/?t313=1", ['<style id="tour-phone-v59">', '#menuBtn{pointer-events:auto}', '#hud .hudside{display:contents}', 'SOMAIL_FIX_312'], []),
    ("/wp-content/plugins/nadlan-config/assets/tours/narr-sdedov-he-3-v2.mp3", [], []),
    ("/properties/page/2/", ['<div class="nlpl"', 'class="nlpl-sep"', 'מודעה לדוגמה', 'nlpl-card--demo'], ['בדיקה משפטית מקדימה', 'class="nlag-badge"']),
    ("/buying-apartment/", ['id="nlhp-top"'], ['class="nlpc-site-header"']),
    ("/premium/", ['id="nlhp-top"'], ['מפת הפרויקטים החיה', ' LIVE</span>', 'class="nlpc-site-header"']),
    ("/ru/", ['class="nlpb-phase__h"', 'Найти риелтора', 'class="nlcta-wa"', '#nla11y{position:fixed;bottom:calc(20px + env(safe-area-inset-bottom,0px));left:20px', 'class="nlpc-site-header"'], ['#nla11y{position:fixed;bottom:calc(20px + env(safe-area-inset-bottom,0px));right:20px', 'id="nlhp-top"']),
    ("/ar/", ['class="nlpb-phase__h"', 'ابحثوا عن وسيط', 'class="nlcta-wa"', '#nla11y{position:fixed;bottom:calc(20px + env(safe-area-inset-bottom,0px));right:20px'], ['#nla11y{position:fixed;bottom:calc(20px + env(safe-area-inset-bottom,0px));left:20px']),
    ("/projects/aurelia/", [], ['id="nlps"', 'nadlan-ps-importmap']),
    ("/", ['class="nlcta-wa"', '#nla11y{position:fixed;bottom:calc(20px + env(safe-area-inset-bottom,0px));right:20px', 'id="nlhp-top"', 'id="nlhp-hero"', 'class="nlhp-cats"', 'id="nlhp-nav"', 'class="nlhp-dd"', 'hero-m-780.jpg?ver=1.72.362 720w', '<img fetchpriority="low" src=', 'decoding="async" fetchpriority="low"', 'hero-d-1400.jpg?ver=1.72.362 1400w', 'hero-d-1920.jpg?ver=1.72.362 1920w', 'media="(max-width: 760px)" fetchpriority="high"', 'media="(min-width: 761px)" fetchpriority="high"', '<style id="nadlan-hp-css">', 'id="nlhp-page"', '#nlhp-page .nlhp-film{margin-top:40px', '#nlhp-hero .nlhp-search__go{', 'class="nlhp-film"', 'ככה בוחרים דירה בנדלן', 'nadlan-promo-v2.mp4', 'id="nlhp-film-h"', 'לבחירת קומה בריינבו תל אביב', 'הסרטון והסיורים הם הדמיות להמחשה בלבד', 'class="nlhp-proj"', 'nlhp-lband', 'nlhp-prices', 'nlhp-citiesband', 'nlhp-services', 'class="nlhp-seo"', 'class="nlhp-postline"', 'מודעות חדשות באתר', 'id="nlhp-map-h">מפת הפרויקטים</h2>', 'מגזין נדל״ן', '<section class="nlhp-band nlhp-pros"', 'class="nlpb-phase__h"', 'מוצאים ובודקים', 'מממנים וחותמים', 'משפצים ובונים', 'מצאו מתווך', 'מצאו שמאי', 'בעלי רישיון תיווך', 'רשומים בפנקס הקבלנים', 'id="nadlan-pb-css"', 'אנשי המקצוע</a>', 'nlhv2-dronemap', 'nlhv2-mfoot', 'class="nlhv2-en"', 'nlhp-val', 'content-visibility:auto;contain-intrinsic-size:auto 560px', 'id="nadlan-hp-js"', '<h1>נדל״ן: פרויקטים חדשים, דירות למכירה ומחירי דירות</h1>', 'content="נדל״ן בישראל: ', 'nlhv2-search', 'nlhv2-tabs', 'data-action="https://nad-lan.co.il/properties/" data-extra="listing_type=rent"', 'nlhv2-mfoot', '/post-listing/', '/tour/sde-dov/'], ['id="nlps"', 'nadlan-ps-importmap', '#nla11y{position:fixed;top:50%', '#nla11y{position:fixed;bottom:calc(20px + env(safe-area-inset-bottom,0px));left:20px', 'class="nlhv2-langbar"', '<section class="nlsa-hero"', 'class="nlpc-site-header"', 'נכסים חדשים במערכת', 'מפת הפרויקטים החיה', ' LIVE</span>', 'מודל תלת', 'הדגמה חיה', 'על המודל', 'class="nlhv2-list nlhv2-cta-tile"', 'nlsa-more-row', 'nlhv2-renewal', 'nlhv2-rentals', 'nlhv2-tourvideo', 'nlhv2-cbs', 'class="nlhv2-areas"', 'class="nlsa-tools"', 'class="nlsa-cards"', 'nadlan-hero-israel-coastline-v2.jpg', 'סיורים תלת־ממד'], ['class="nlhv2-prosgrid"', 'רונית אלמוג', 'שירה גולן', 'אורי נחום', '★ 4.9', '★ 5.0', 'עוד 2,846 אנשי מקצוע', 'זמינות דירות לפי קומה ונוף', 'nadlan-hero-israel-coastline', 'בחירת דירה מתוך הבניין', 'בחירת דירה בתלת ממד', 'src="https://js.stripe.com/v3', 'id="nadlan-model-viewer-js"', 'id="pms-stripe-script-js"']),
    ("/brokers/", ['<h1 class="nlds-pagehead__title">', 'id="nlhp-top"', '<div class="nlds-blist">', 'class="nlds-citysec"', 'class="nlds-citysec__title"', '<a class="nlds-procard" href=', 'class="nlds-procard__mark"', 'class="nlds-procard__lic"', 'רישיון תיווך 3216531', '<details class="nlds-more">', 'class="nlds-more__less"', 'nlds-chips nlds-chips--scroll', 'class="nlds-licence__vf"', 'class="nlds-bfeat"', 'class="nlds-source"', 'nlds.css?ver=1.72.362'], ['id="nlps"', 'class="nlpc-site-header"', 'nlds-procard__pill', 'class="nlbl-city"', 'nlbl-more', 'icons/card-pin.svg']),
    ("/brokers/meital-katzir/", ['<style id="nadlan-broker-site-v44">', 'class="nlb-site-nav"', 'class="nlb-areagrid"', 'id="nlhp-top"', 'רישיון'], ['id="nlps"', 'class="nlpc-site-header"']),
    ("/professionals/meital-katzir/", ['<h1 class="nlpp-name">מיטל קציר <span class="nlpp-office">· ', 'class="nlpp-groups"', 'אזורי פעילות', '.wp-block-post-featured-image{display:none!important}', 'id="nlhp-top"'], ['nlpp-fomo">', 'id="nlps"', 'class="nlpc-site-header"']),
]
H1_EXACTLY_ONE = ["/", RB, "/projects/ashira-sde-dov/", "/projects/aurelia/", "/post-listing/", "/properties/", "/properties/?listing_type=sale", "/brokers/", "/brokers/meital-katzir/", "/professionals/meital-katzir/", "/projects/h-infinity-somail-tel-aviv/", "/projects/dimri-yama-sde-dov/", "/projects/duo-tel-aviv/", "/projects/rainbow-tel-aviv-en/"]
ORDER = ['<h1 id="nl-project-page-title" class="nlps-h1">', 'class="nl-lead"', 'nlps-hero__cta', 'id="nlps"', 'class="nlbsq"', 'class="nlpf"', 'id="nlps-view"', 'id="nlpjx-map"', 'id="nlps-tour"', 'class="nlpd"', 'nlcp-projctx', 'class="nl-projnotice"', 'nadlan-project-article']


def verify_order(tag):
    s, html = page(RB + "?nlv=" + tag)
    body = body_of(html)
    pos = [body.find(x) for x in ORDER]
    maps = body.count('id="nlpjx-map"')
    ok = s == 200 and all(p > -1 for p in pos) and pos == sorted(pos) and maps == 1
    print(f"[order] {'OK ' if ok else 'BAD'} {list(zip([o[:22] for o in ORDER], pos))} maps={maps}")
    return ok


# exact markup, each once: a bare class name also matches attributes (data-nlhp-projects on the hero moved 'nlhp-projects' first)
HOME_ORDER = ['id="nlhp-top"', 'id="nlhp-hero"', '<h1>', '<nav class="nlhp-cats"', '<section class="nlhp-film"', '<section class="nlhp-band nlhp-projects"', '<section class="nlhp-band nlhp-lband"', '<section class="nlhp-band nlhp-prices"', '<section class="nlhp-band nlhp-citiesband"', '<section class="nlhp-band nlhp-mapband"', '<section class="nlhp-band nlhp-pros"', 'nlhv2-alt nlhp-magazine"', '<section class="nlhp-band nlhp-services"', '<section class="nlhv2-en"', '<section class="nlhp-seo"', '<section class="nlhv2-mfoot"']


def verify_home_order(tag):
    s, html = page("/?nlv=" + tag)
    body = body_of(html)
    pos = [body.find(x) for x in HOME_ORDER]
    ok = s == 200 and all(p > -1 for p in pos) and pos == sorted(pos) and all(body.count(x) == 1 for x in HOME_ORDER if x != '<h1>')
    print(f"[home-order] {'OK ' if ok else 'BAD'} {list(zip([o[:18] for o in HOME_ORDER], pos))}")
    return ok


def ttfb(path):
    t0 = time.time()
    r = urllib.request.Request(BASE + path + ("&" if "?" in path else "?") + "nlt=" + secrets.token_hex(4), headers={"User-Agent": UA})
    with urllib.request.urlopen(r, timeout=60) as resp:
        resp.read(1)
        first = time.time() - t0
        resp.read()
        return resp.status, round(first, 2)


def speed(label):
    res = {}
    for pth in SLOW_PROJECTS:
        try:
            res[pth] = ttfb(pth)
        except Exception as e:
            res[pth] = ("ERR", str(e)[:80])
        print(f"[speed {label}] {res[pth]} {pth[:60]}")
    return res


def verify_pages(tag):
    bad = []
    for chk in CHECKS:
        path, need, never = chk[:3]
        never_html = chk[3] if len(chk) > 3 else []
        sep = "&" if "?" in path else "?"
        try:
            s, html = page(path + sep + "nlv=" + tag)
        except Exception as e:  # a timeout is a failed check, not a crash that skips the rollback
            print(f"[page] BAD --- {path[:70]} {e}")
            bad.append(path)
            continue
        body = body_of(html)
        miss = [n for n in need if n not in html]
        hit = [n for n in never if n in body] + ["html:" + n for n in never_html if n in html]
        if path in H1_EXACTLY_ONE and body.count("<h1") != 1:
            hit.append("h1 x%d" % body.count("<h1"))
        ok = s == 200 and not miss and not hit and "Fatal error" not in body and "critical error" not in body
        print(f"[page] {'OK ' if ok else 'BAD'} {s} {path[:70]} missing={miss} forbidden={hit}")
        if not ok:
            bad.append(path)
    return bad


def wait_version(want, secs=75):
    t0 = time.time()
    last = None
    while time.time() - t0 < secs:
        try:
            s, h2 = req("GET", "/wp-json/nadlan/v1/health?nlv=" + str(int(time.time())), auth=False)
            last = h2.get("version") if isinstance(h2, dict) else s
            if s == 200 and isinstance(h2, dict) and h2.get("version") == want and h2.get("status") == "ok":
                print(f"[health] {want} ok after {int(time.time() - t0)}s")
                return True
        except Exception as e:
            last = str(e)
        time.sleep(4)
    print(f"[health] still {last} after {secs}s")
    return False


def rollback(created_any):
    print("[rollback] restoring .bak362 files")
    for rel in ["nadlan-config.php"] + [r for r in FILES if r not in NEWFILES]:
        print("  ", rel, ops({"restore": rel}, "restore " + rel).get("restore"))
    for rel in sorted(NEWFILES):
        ops({"unlink": rel}, "unlink " + rel)
    print("   new files removed:", len(NEWFILES))
    ops({"purge": 1}, "purge")


# ---------------------------------------------------------------- main
NEWFILES = set(['inc/pro-card.php', 'assets/pronet/procard.css', 'data/register-facts.json'])
FILES = ['data/register-facts.json', 'assets/pronet/procard.css', 'inc/pro-card.php', 'inc/directory.php', 'inc/cards-render.php', 'inc/schema.php', 'inc/rest-privacy.php', 'inc/professional-profile.php']
NEW = {rel: open(os.path.join(PLUG, *rel.split("/")), "rb").read() for rel in FILES}
for rel in FILES:
    if rel.endswith(".php"):
        php_lint(NEW[rel], rel)
HEAD = {rel: git_head("plugins/nadlan-config/" + rel) for rel in FILES}
os.makedirs(os.path.join(QA, "live-backup"), exist_ok=True)

created = False
try:
    s, lst = snip("GET", "")
    for x in (lst if s == 200 and isinstance(lst, list) else []):
        if str(x.get("name", "")).startswith(("x-tmp-bl244-ops-", "x-tmp-bl245-ops-", "x-tmp-pl246-ops-", "x-tmp-wa247-ops-", "x-tmp-tc248-ops-", "x-tmp-bv249-ops-", "x-tmp-pe250-ops-", "x-tmp-fg251-ops-", "x-tmp-fg252-ops-", "x-tmp-bl253-ops-", "x-tmp-lg254-ops-", "x-tmp-ps255-ops-", "x-tmp-ps256-ops-", "x-tmp-ps258-ops-", "x-tmp-ps259-ops-", "x-tmp-ps260-ops-", "x-tmp-ps261-ops-", "x-tmp-ps262-ops-", "x-tmp-ps263-ops-", "x-tmp-ps264-ops-", "x-tmp-ps265-ops-", "x-tmp-ps266-ops-", "x-tmp-ps267-ops-", "x-tmp-ps268-ops-", "x-tmp-ps269-ops-", "x-tmp-ps270-ops-", "x-tmp-ps271-ops-", "x-tmp-ps272-ops-", "x-tmp-ps273-ops-", "x-tmp-ps274-ops-", "x-tmp-ps275-ops-", "x-tmp-ps276-ops-", "x-tmp-ps277-ops-", "x-tmp-ps278-ops-", "x-tmp-ps279-ops-", "x-tmp-ps280-ops-", "x-tmp-ps281-ops-", "x-tmp-ps282-ops-", "x-tmp-ps283-ops-", "x-tmp-ps284-ops-", "x-tmp-ps285-ops-", "x-tmp-ps286-ops-", "x-tmp-ps287-ops-", "x-tmp-ps288-ops-", "x-tmp-ps289-ops-", "x-tmp-ps290-ops-", "x-tmp-ps291-ops-", "x-tmp-ps292-ops-", "x-tmp-ps293-ops-", "x-tmp-ps294-ops-", "x-tmp-ps295-ops-", "x-tmp-ps296-ops-", "x-tmp-ps297-ops-", "x-tmp-ps298-ops-", "x-tmp-ps299-ops-", "x-tmp-ps300-ops-", "x-tmp-ps301-ops-", "x-tmp-ps302-ops-", "x-tmp-ps303-ops-", "x-tmp-ps304-ops-", "x-tmp-ps305-ops-", "x-tmp-ps306-ops-", "x-tmp-ps307-ops-", "x-tmp-ps308-ops-", "x-tmp-ps309-ops-", "x-tmp-ps310-ops-", "x-tmp-ps311-ops-", "x-tmp-ps312-ops-", "x-tmp-ps313-ops-", "x-tmp-ps314-ops-", "x-tmp-ps315-ops-", "x-tmp-ps316-ops-", "x-tmp-ps317-ops-", "x-tmp-ps318-ops-", "x-tmp-ps319-ops-", "x-tmp-ps320-ops-", "x-tmp-ps321-ops-", "x-tmp-ps322-ops-", "x-tmp-ps323-ops-", "x-tmp-ps324-ops-", "x-tmp-ps325-ops-", "x-tmp-ps326-ops-", "x-tmp-ps327-ops-", "x-tmp-ps328-ops-", "x-tmp-ps329-ops-", "x-tmp-ps330-ops-", "x-tmp-ps331-ops-", "x-tmp-ps332-ops-", "x-tmp-ps333-ops-", "x-tmp-ps334-ops-", "x-tmp-ps335-ops-", "x-tmp-ps336-ops-", "x-tmp-ps337-ops-", "x-tmp-ps338-ops-", "x-tmp-ps339-ops-", "x-tmp-ps340-ops-", "x-tmp-ps341-ops-", "x-tmp-ps342-ops-", "x-tmp-ps343-ops-", "x-tmp-ps344-ops-", "x-tmp-ps345-ops-", "x-tmp-ps346-ops-", "x-tmp-ps347-ops-", "x-tmp-ps348-ops-", "x-tmp-ps349-ops-", "x-tmp-ps350-ops-", "x-tmp-ps351-ops-", "x-tmp-ps352-ops-", "x-tmp-ps353-ops-", "x-tmp-ps354-ops-", "x-tmp-ps355-ops-", "x-tmp-ps356-ops-", "x-tmp-ps357-ops-", "x-tmp-ps358-ops-", "x-tmp-ps359-ops-", "x-tmp-ps360-ops-", "x-tmp-ps361-ops-", "x-tmp-ps362-ops-", "x-tmp-had247-ops-")) and x.get("active"):
            print("[sweep] deactivating leftover bridge", x["id"], snip("PUT", f"/{x['id']}/deactivate", {})[0])
    bridge_up()
    before = {}
    if "--rollback" in ARGS:
        rollback(True)
        wait_version(LIVE_VER)
        raise SystemExit(0)

    LIVE = {}
    for rel in FILES:
        cur = live_get(rel)
        if rel in NEWFILES:
            if not cur.get("missing"):
                raise SystemExit("FATAL new file already on the server: " + rel)
            LIVE[rel] = None
            print(f"[drift] {rel}: new file, not on the server yet (ok)")
            continue
        if cur.get("missing"):
            raise SystemExit("FATAL live file missing: " + rel)
        LIVE[rel] = base64.b64decode(cur["b64"])
        print(f"[drift] live {rel} {md5(LIVE[rel])[:10]} vs git HEAD {md5(HEAD[rel])[:10] if HEAD[rel] else '-'}")
        # line endings do not count: git stores LF, a file written on Windows may carry CRLF (24.9: that alone broke the compare)
        # 1.72.243 went live minutes ago and is committed together with this release: the live file must be what 243 wrote
        prev = None
        for res in ("project-stage-2026-09-24/deploy-result-361.json", "project-stage-2026-09-24/deploy-result-360.json", "project-stage-2026-09-24/deploy-result-359.json", "project-stage-2026-09-24/deploy-result-358.json", "project-stage-2026-09-24/deploy-result-357.json", "project-stage-2026-09-24/deploy-result-356.json", "project-stage-2026-09-24/deploy-result-355.json", "project-stage-2026-09-24/deploy-result-354.json", "project-stage-2026-09-24/deploy-result-353.json", "project-stage-2026-09-24/deploy-result-352.json", "project-stage-2026-09-24/deploy-result-351.json", "project-stage-2026-09-24/deploy-result-350.json", "project-stage-2026-09-24/deploy-result-349.json", "project-stage-2026-09-24/deploy-result-348.json", "project-stage-2026-09-24/deploy-result-347.json", "project-stage-2026-09-24/deploy-result-346.json", "project-stage-2026-09-24/deploy-result-345.json", "project-stage-2026-09-24/deploy-result-344.json", "project-stage-2026-09-24/deploy-result-343.json", "project-stage-2026-09-24/deploy-result-342.json", "project-stage-2026-09-24/deploy-result-341.json", "project-stage-2026-09-24/deploy-result-340.json", "project-stage-2026-09-24/deploy-result-339.json", "project-stage-2026-09-24/deploy-result-338.json", "project-stage-2026-09-24/deploy-result-337.json", "project-stage-2026-09-24/deploy-result-336.json", "project-stage-2026-09-24/deploy-result-335.json", "project-stage-2026-09-24/deploy-result-334.json", "project-stage-2026-09-24/deploy-result-333.json", "project-stage-2026-09-24/deploy-result-332.json", "project-stage-2026-09-24/deploy-result-331.json", "project-stage-2026-09-24/deploy-result-330.json", "project-stage-2026-09-24/deploy-result-329.json", "project-stage-2026-09-24/deploy-result-328.json", "project-stage-2026-09-24/deploy-result-327.json", "project-stage-2026-09-24/deploy-result-326.json", "project-stage-2026-09-24/deploy-result-325.json", "project-stage-2026-09-24/deploy-result-324.json", "project-stage-2026-09-24/deploy-result-323.json", "project-stage-2026-09-24/deploy-result-322.json", "project-stage-2026-09-24/deploy-result-321.json", "project-stage-2026-09-24/deploy-result-320.json", "project-stage-2026-09-24/deploy-result-319.json", "project-stage-2026-09-24/deploy-result-318.json", "project-stage-2026-09-24/deploy-result-317.json", "project-stage-2026-09-24/deploy-result-316.json", "project-stage-2026-09-24/deploy-result-315.json", "project-stage-2026-09-24/deploy-result-314.json", "project-stage-2026-09-24/deploy-result-313.json", "project-stage-2026-09-24/deploy-result-312.json", "project-stage-2026-09-24/deploy-result-311.json", "project-stage-2026-09-24/deploy-result-310.json", "project-stage-2026-09-24/deploy-result-309.json", "project-stage-2026-09-24/deploy-result-308.json", "project-stage-2026-09-24/deploy-result-307.json", "project-stage-2026-09-24/deploy-result-306.json", "project-stage-2026-09-24/deploy-result-305.json", "project-stage-2026-09-24/deploy-result-304.json", "project-stage-2026-09-24/deploy-result-303.json", "project-stage-2026-09-24/deploy-result-302.json", "project-stage-2026-09-24/deploy-result-301.json", "project-stage-2026-09-24/deploy-result-300.json", "project-stage-2026-09-24/deploy-result-299.json", "project-stage-2026-09-24/deploy-result-298.json", "project-stage-2026-09-24/deploy-result-297.json", "project-stage-2026-09-24/deploy-result-296.json", "project-stage-2026-09-24/deploy-result-295.json", "project-stage-2026-09-24/deploy-result-294.json", "project-stage-2026-09-24/deploy-result-293.json", "project-stage-2026-09-24/deploy-result-292.json", "project-stage-2026-09-24/deploy-result-291.json", "project-stage-2026-09-24/deploy-result-290.json", "project-stage-2026-09-24/deploy-result-289.json", "project-stage-2026-09-24/deploy-result-288.json", "project-stage-2026-09-24/deploy-result-287.json", "project-stage-2026-09-24/deploy-result-286.json", "project-stage-2026-09-24/deploy-result-285.json", "project-stage-2026-09-24/deploy-result-284.json", "project-stage-2026-09-24/deploy-result-283.json", "project-stage-2026-09-24/deploy-result-282.json", "project-stage-2026-09-24/deploy-result-281.json", "project-stage-2026-09-24/deploy-result-280.json", "project-stage-2026-09-24/deploy-result-279.json", "project-stage-2026-09-24/deploy-result-278.json", "project-stage-2026-09-24/deploy-result-277.json", "project-stage-2026-09-24/deploy-result-276.json", "project-stage-2026-09-24/deploy-result-275.json", "project-stage-2026-09-24/deploy-result-274.json", "project-stage-2026-09-24/deploy-result-273.json", "project-stage-2026-09-24/deploy-result-272.json", "project-stage-2026-09-24/deploy-result-271.json", "project-stage-2026-09-24/deploy-result-270.json", "project-stage-2026-09-24/deploy-result-269.json", "project-stage-2026-09-24/deploy-result-268.json", "project-stage-2026-09-24/deploy-result-267.json", "project-stage-2026-09-24/deploy-result-266.json", "project-stage-2026-09-24/deploy-result-265.json", "project-stage-2026-09-24/deploy-result-264.json", "project-stage-2026-09-24/deploy-result-263.json", "project-stage-2026-09-24/deploy-result-262.json", "project-stage-2026-09-24/deploy-result-261.json", "project-stage-2026-09-24/deploy-result-260.json", "project-stage-2026-09-24/deploy-result-259.json", "project-stage-2026-09-24/deploy-result-258.json", "recommendations-2026-09-24/deploy-result-257.json", "project-stage-2026-09-24/deploy-result-256.json", "project-stage-2026-09-24/deploy-result-255.json", "firgun-2026-09-24/deploy-result-251.json", "tour-calendar-2026-09-24/deploy-result-248.json", "profile-emoji-2026-09-24/deploy-result-250.json", "broker-video-2026-09-24/deploy-result-249.json", "tour-calendar-2026-09-24/deploy-result-248.json", "wa-pill-2026-09-24/deploy-result-247.json", "placements-2026-09-24/deploy-result-246.json"):
            prev = json.load(open(os.path.join(REPO, "docs", "qa", *res.split("/")), encoding="utf-8"))["files"].get(rel)
            if prev:
                break
        if prev:
            if md5(LIVE[rel]) != prev:
                raise SystemExit(f"FATAL: live {rel} is not what the last release wrote; diff it before replacing it")
        elif HEAD[rel] is None or LIVE[rel].replace(CRLF, LF) != HEAD[rel].replace(CRLF, LF):
            raise SystemExit(f"FATAL: live {rel} differs from git HEAD; diff it before replacing it")
    cur_main = live_get("nadlan-config.php")
    live_main = base64.b64decode(cur_main["b64"])
    stamp = time.strftime("%Y%m%dT%H%M%S")
    if not DRY:
        for rel in FILES:
            if LIVE[rel] is not None and rel not in NEWFILES:
                open(os.path.join(QA, "live-backup", rel.split("/")[-1] + f".{stamp}.live"), "wb").write(LIVE[rel])
        open(os.path.join(QA, "live-backup", f"nadlan-config.php.{stamp}.live"), "wb").write(live_main)

    # the version bump, on the live text
    text = live_main.decode("utf-8")
    m = re.search(r"\* Version: (\d+)\.(\d+)\.(\d+)", text)
    old = ".".join(m.groups())
    new = f"{m.group(1)}.{m.group(2)}.{int(m.group(3)) + 1}"
    for a, b2 in ((f" * Version: {old}", f" * Version: {new}"), (f"define( 'NADLAN_CONFIG_VERSION', '{old}' )", f"define( 'NADLAN_CONFIG_VERSION', '{new}' )")):
        n = text.count(a)
        if n != 1:
            raise SystemExit(f"FATAL anchor x{n} in nadlan-config.php: {a}")
        text = text.replace(a, b2)

    if text.count('body.single-nadlan_project #nlcta { display: none !important; }') != 0:
        raise SystemExit("FATAL: the pill-hiding rule is back in the live nadlan-config.php")
    NEWL = "'project-stage', 'together', 'lang-pages', 'basket', 'rest-privacy', 'home-v3', 'pro-card' ) as $nadlan_mod"
    if text.count(NEWL) != 1:
        for OLDL in ("'project-stage', 'together', 'lang-pages', 'basket', 'rest-privacy', 'home-v3' ) as $nadlan_mod", "'project-stage', 'together', 'lang-pages', 'basket', 'home-v3' ) as $nadlan_mod", "'project-stage', 'together', 'lang-pages', 'home-v3' ) as $nadlan_mod", "'project-stage', 'together', 'home-v3' ) as $nadlan_mod"):
            if text.count(OLDL) == 1:
                text = text.replace(OLDL, NEWL)  # LanguagePages v84 (1.72.338), BasketOne v86 (1.72.340)
                break
        else:
            raise SystemExit("FATAL: together / home-v3 are not in the live module list")
    new_main = text.encode("utf-8")
    php_lint(new_main, "nadlan-config.php (live text, bumped)")
    print(f"[plan] {old} -> {new}; replacing {', '.join(FILES)}")
    if DRY:
        print("[dry] no writes")
        raise SystemExit(0)

    try:
        created = True
        for rel in FILES:
            put(rel, NEW[rel], expect=("missing" if LIVE[rel] is None else md5(LIVE[rel])))
        put("nadlan-config.php", new_main, expect=md5(live_main))
    except BaseException as e:  # a write refused half way (drift, lint, md5): put everything back
        print("[FAIL] during writes:", e)
        rollback(created)
        raise
    print("[purge]", ops({"purge": 1}, "purge"))

    healthy = wait_version(new)
    bad = verify_pages("ps362" + str(int(time.time()))) if healthy else ["health"]
    if healthy and not bad and not verify_order("ps362o" + str(int(time.time()))):
        bad = ["order"]
    if healthy and not bad and not verify_home_order("ps362h" + str(int(time.time()))):
        bad = ["home-order"]
    after = speed("after") if healthy else {}
    slow_after = [k for k, v in after.items() if not (isinstance(v[1], float) and v[1] < 5)]
    if healthy and slow_after:
        print("[speed] still slow after the release:", slow_after)
    if bad:
        # one more purge and a patient second look before rolling back (OPcache/LiteSpeed lag)
        ops({"purge": 1}, "purge again")
        time.sleep(12)
        healthy = wait_version(new, 45)
        bad = verify_pages("ps362b" + str(int(time.time()))) if healthy else ["health"]
        if healthy and not bad and not verify_order("ps362p" + str(int(time.time()))):
            bad = ["order"]
        if healthy and not bad and not verify_home_order("ps362q" + str(int(time.time()))):
            bad = ["home-order"]
    if bad:
        print("[FAIL] pages:", bad)
        rollback(created)
        wait_version(old, 60)
        raise SystemExit("ROLLED BACK")
    json.dump({"released": new, "from": old, "at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "files": dict({rel: md5(NEW[rel]) for rel in FILES}, **{"nadlan-config.php": md5(new_main)}),
        "live_before": dict({rel: (md5(LIVE[rel]) if LIVE[rel] is not None else "missing") for rel in FILES}, **{"nadlan-config.php": md5(live_main)})},
        open(os.path.join(QA, "deploy-result-362.json"), "w", encoding="utf-8"), indent=2)
    json.dump({"before": before, "after": after}, open(os.path.join(QA, "speed-362.json"), "w", encoding="utf-8"), indent=2)
    print(f"RELEASE {new} LIVE")


finally:
    bridge_down()
