# -*- coding: utf-8 -*-
"""Release 1.72.258 (24.9.2026): Rainbow's facts, from the official record (the site loop, item R1; sources in
docs/research/2026-09-24-rainbow-run/rainbow-facts.md and lot 111's outline in the Tel Aviv plans layer).
  assets/project-stage/rainbow/stage.js     the tower in lot 111's north-east corner, 39 floors above the entrance, 3.75 m
                                            floors; the two pools on two boutique roofs (not in the courtyard); the scene
                                            turned 10° east like the lot; the shore 713 m from the lot's centre
  assets/project-stage/rainbow/poster.jpg   rendered from the corrected scene
  inc/project-stage.php                     the view and the beam start at the tower (32.10354, 34.78466), not the lot's centre
  inc/project-experience.php                a demo unit (its own note: "יחידת הדגמה") never feeds a public number: the price
                                            band's "דירות 82-210 מ״ר" came from the six demo units
  nadlan-config.php                         version bump only
After the code: scripts/project-stage/rainbow_content.py --apply fixes the page text (writer's notes that leaked into
the cards, the units row, the price card) and sets the NIS/m² to the developer's reported 81,782.

Release 1.72.256 (24.9.2026): on Rainbow's page, when a direction is picked the area map turns so that way is up and
centres 450 m ahead of the building, so the beam is seen against the sea or the city (at 1.72.255 the map centred on the
building and the sea stayed just outside the frame). And the stage puts the shore where it is (owner: "Rainbow is not
located so close to the sea, check it"): the OSM coastline is 713 m from the project's parcel coordinates (nearest point
at 287°; 798 m due west), the stage had the waterline 142 m from the tower. Now 713 m, with the quarter's blocks between;
a new opening view and a new poster from the corrected scene.
  assets/project-stage/bridge.js            the map centres ahead; the poster URL is versioned
  assets/project-stage/rainbow/stage.js     the shore at 713 m, the quarter west to the coastal park, opening view, haze
  assets/project-stage/rainbow/poster.jpg   rendered from the corrected scene
  inc/project-stage.php                     the versioned poster (preload and the stage's option)
  nadlan-config.php                         version bump only

Release 1.72.255 (24.9.2026): Rainbow's page top at a new level (owner: "put Rainbow inside the page... what happens
when you click a floor... the beam on the map, relative to the sea, the city, the buildings... Meital at the side with a
square you can click, and an empty square: 'do you want to appear here?'... plans are very important"). Designed first in
Claude Design (artifact L9Nqz7Viv7K3MYeZrBc9s8 version 10: ProjectStage, BrokerSquare, BrokerSlot).
  inc/project-stage.php (NEW)               the page's one h1 becomes the visible title (developer and quarter under it);
                                            under the lead: the stage, a side rail (Meital's square, labelled an
                                            advertisement, and the empty "רוצה להופיע כאן?"), then the view from the floor
                                            next to the area map with the beam; directions said by what lies there;
                                            "לקבלת תוכניות ומחירים" to WhatsApp. Composed on the finished HTML, fails open.
  assets/project-stage/bridge.js (NEW)      the view (Mapbox, the floor's estimated height), the beam, the WhatsApp text
  assets/project-stage/rainbow/ (NEW)       the Rainbow stage (three.js), its CSS and poster
  assets/nlds/nlds.css                      rebuilt from the design system (the page top, BrokerSquare, BrokerSlot)
  nadlan-config.php                         'project-stage' in the module list (on the LIVE text)
Only /projects/rainbow-tel-aviv/ changes; every other page must look exactly as before.

Release 1.72.254 (24.9.2026): terms of use and a privacy policy, basic and editable (owner order), linked in the footer.
  inc/legal-links.php (NEW)  "תנאי שימוש · מדיניות פרטיות · הצהרת נגישות" in the footer's bottom line (the accessibility
                             statement had no footer link); a link shows only when its page is published
  nadlan-config.php          'legal-links' in the module list (on the LIVE text)
After the code: the pages /privacy/ and /terms/ are created from docs/legal/ ONLY when missing (never overwriting an
edit), as ordinary pages anyone with wp-admin can edit, and /privacy/ becomes WordPress's privacy-policy page.

Release 1.72.253 (24.9.2026): the brokers list shows six brokers per city; the rest open in place ("עוד 44 מתווכים
בתל אביב יפו"). All 120 cards stay in the page. On a phone the page ran about 34,000px.
  inc/brokers-list.php

Release 1.72.252 (24.9.2026): two fixes to the professionals network, found in the browser check of 1.72.251.
  inc/pro-network.php  a wrong or old private link answers 400 with "הקישור לא תקין. אפשר לבקש קישור חדש." (uPress turns a
                       403 into its 404 page, so the visitor saw only "משהו לא עבד")
  inc/firgun.php       the form shows the qualities before the one line, as the design system does; "closed" answers 400

Release 1.72.250 (24.9.2026): no emoji on a professional's card (owner: no AI tells; design system: no emoji, no
dingbats as icons). The camera before "פגישת וידאו", the globe on language chips, the eye before the view count and the
sparkles on the question box go; area chips get the design system's pin (icons/card-pin.svg). Rating stars stay.
  inc/professional-profile.php

Release 1.72.249 (24.9.2026): the broker's listings video on the broker's card (owner: "שלכל מתווך יהיה וידאו על כל הנכסים שלו").
  inc/professional-profile.php  ListingsVideo from the design system (artifact version 5): meta nl_video (JSON: both files,
                                both posters, count, seconds, date); no autoplay, preload none; upright on phones, wide elsewhere
  assets/nlds/nlds.css          rebuilt from the design system (the ListingsVideo rules)
After the code is live and checked, the runner writes Meital's nl_video (the files were uploaded by
scripts/broker-video/upload_media.py) and checks her card again. If the card fails with the video, the meta is removed.

Release 1.72.248 (24.9.2026): a broker's own booking page for "תיאום סיור" (owner: "תיאום מועד ביומן, אולי Calendly").
  inc/professional-profile.php  calendar_url (registered meta, an admin box "יומן לתיאום סיור", https only, validated);
                                with a link, the profile's "תיאום סיור" opens it and counts as a tour in the insights
  inc/brokers-list.php          the featured card's tour button opens the booking page when there is one
  inc/placements.php            an advertisement on an article keeps WhatsApp (a conversation, not a tour)
No broker has a link yet, so every page must look exactly as before.

Release 1.72.247 (24.9.2026): the floating WhatsApp pill, readable, with the real NadLan mark (fixed in the design
system first, artifact L9Nqz7Viv7K3MYeZrBc9s8 version 4).
  inc/conversion-cta.php  a deep WhatsApp green #0F7A63 (white on it 5.27:1; on #25D366 it was 1.98:1, and the pill
                          stood out from the page at 1.83:1), the sub-line full white, the Skin A glow re-tinted, and
                          the brand chip is the NadLan mark on a paper tile instead of the old black tile with gold bars
  assets/nlds/nlds.css    rebuilt from the design system (wa-green, shadow-wa and the pill's two rules)

Release 1.72.246 (24.9.2026): Meital's card on the value calculator and her neighbourhood guides, with the mechanism.
  inc/brokers-list.php   the BrokerFeatureCard takes arguments, so an advertisement on a content page can reuse it
  inc/placements.php     the placement card is that design system card under a "פרסומת" label; its position is a number
                         of sections or a word from a section heading, per page line; a page without that section gets
                         no card
After the code is live and checked, the runner publishes one placement (idempotent, by title): Meital's card (7833) on
/property-value/, the Tel Aviv luxury value guide, North Tel Aviv, Ramat Aviv and Herzliya Pituach, each right after the
prices section. If the pages fail with the card, the placement is switched off (pl_active 0), not the code.

Release 1.72.245 (24.9.2026): the brokers list on phones, and the design system shielded from the theme.
  assets/nlds/nlds.css   rebuilt: every component scoped under ":root body .nlds" with !important (the theme forced
                         19-24px Frank Ruhl headings with 28px margins and 18px paragraphs on the cards); the artifact's
                         phone rules (.nlds-phone X) are the real phone layout (max-width 600px)
  assets/nlds/icons/     NEW: the design system's 48 icon files (Icons + Professions), used as <img> like the artifact
  inc/brokers-list.php   the featured card's buttons are a direct child of the card (the artifact's phone markup): full
                         width under the photo on a phone; the broker cards use profession-broker.svg and card-pin.svg
  inc/design-system.php  nlds_asset_url()

Release 1.72.244 (24.9.2026): the design system tokens are namespaced (--nlds-*): the theme already defines --space-20 as 80px, which squeezed every card on /brokers/; link-based components take their colours back (the primary button text was invisible).

Release 1.72.243 (24.9.2026): the design system on the site, the brokers list, and "מתווכים" in the header.

  assets/nlds/nlds.css   NEW: the NadLan design system (Claude Design artifact L9Nqz7Viv7K3MYeZrBc9s8), tokens + components,
                         built by scripts/nlds/build_nlds_css.py
  inc/design-system.php  NEW: loads nlds.css on the site; shared inline icons (nlds_icon)
  inc/brokers-list.php   NEW: /brokers/ opens with the brokers list: PageHeader (one H1 "מתווכי נדל״ן"), the featured broker
                         (Meital, BrokerFeatureCard with her portrait), every licensed broker by city (ProfessionalCard);
                         the offer for brokers stays below, its H1 now an H2; "מתווכים" joins the header after "אנשי מקצוע"
  nadlan-config.php      version bump + 'design-system', 'brokers-list' in the module list, both on the LIVE text

Same safety chain as deploy234.py. The app password is decrypted in-process (DPAPI), never printed.
  python scripts/legal/deploy254.py [--dry | --rollback]
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
BAK = ".bak258"
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
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) NadLan-PS258/1.0"


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
NS = 'nadlan-ps258-' + TOKEN[:8]  # one route per run: a bridge left over from a failed run can never answer for this one
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
				if ( function_exists( 'opcache_invalidate' ) ) { foreach ( array( 'inc/project-stage.php', 'inc/project-experience.php', 'nadlan-config.php' ) as $f ) { @opcache_invalidate( $root . $f, true ); } }
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
    s, c = snip("POST", "", {"name": f"x-tmp-ps258-ops-{int(time.time())}", "code": BRIDGE, "scope": "global", "active": False})
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
    (RB, ['id="nlps"', 'class="nlbsq"', 'class="nlbslot"', 'id="nlps-view"', '<h1 id="nl-project-page-title" class="nlps-h1">', 'id="nlpjx-map"', 'class="nl-lead"', 'nlcp-projctx', 'nadlan-project-article', 'רישיון תיווך', 'פרסומת', 'רוצה להופיע כאן?', 'לקבלת תוכניות ומחירים', 'assets/project-stage/bridge.js?ver=1.72.258', 'poster.jpg?ver=1.72.258', '32.10354', 'nadlan-ps-importmap'],
     ['על המפה החיה למטה', 'id="nl-project-page-title" class="screen-reader-text"', 'דירות 82-210']),
    ("/projects/h-infinity-somail-tel-aviv/", ['nadlan-project-article'], ['id="nlps"', 'nadlan-ps-importmap', 'nadlan-ps-bridge']),
    ("/projects/dimri-yama-sde-dov/", ['nadlan-project-article'], ['id="nlps"', 'nadlan-ps-importmap']),
    ("/projects/duo-tel-aviv/", ['nadlan-project-article'], ['id="nlps"', 'nadlan-ps-importmap']),
    ("/projects/rainbow-tel-aviv-en/", [], ['id="nlps"', 'nadlan-ps-importmap']),
    ("/projects/aurelia/", [], ['id="nlps"', 'nadlan-ps-importmap']),
    ("/", ['class="nlcta-wa"'], ['id="nlps"', 'nadlan-ps-importmap']),
    ("/brokers/", ['<h1 class="nlds-pagehead__title">'], ['id="nlps"']),
    ("/professionals/meital-katzir/", ['<h1 class="nlpp-name">'], ['id="nlps"']),
]
H1_EXACTLY_ONE = [RB, "/brokers/", "/professionals/meital-katzir/", "/projects/h-infinity-somail-tel-aviv/", "/projects/dimri-yama-sde-dov/", "/projects/duo-tel-aviv/", "/projects/rainbow-tel-aviv-en/"]
ORDER = ['<h1 id="nl-project-page-title" class="nlps-h1">', 'class="nl-lead"', 'id="nlps"', 'class="nlbsq"', 'id="nlps-view"', 'id="nlpjx-map"', 'nlcp-projctx', 'nadlan-project-article']


def verify_order(tag):
    s, html = page(RB + "?nlv=" + tag)
    body = body_of(html)
    pos = [body.find(x) for x in ORDER]
    maps = body.count('id="nlpjx-map"')
    ok = s == 200 and all(p > -1 for p in pos) and pos == sorted(pos) and maps == 1
    print(f"[order] {'OK ' if ok else 'BAD'} {list(zip([o[:22] for o in ORDER], pos))} maps={maps}")
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
    for path, need, never in CHECKS:
        sep = "&" if "?" in path else "?"
        try:
            s, html = page(path + sep + "nlv=" + tag)
        except Exception as e:  # a timeout is a failed check, not a crash that skips the rollback
            print(f"[page] BAD --- {path[:70]} {e}")
            bad.append(path)
            continue
        body = body_of(html)
        miss = [n for n in need if n not in html]
        hit = [n for n in never if n in body]
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
    print("[rollback] restoring .bak258 files")
    for rel in ["nadlan-config.php"] + [r for r in FILES if r not in NEWFILES]:
        print("  ", rel, ops({"restore": rel}, "restore " + rel).get("restore"))
    for rel in sorted(NEWFILES):
        ops({"unlink": rel}, "unlink " + rel)
    print("   new files removed:", len(NEWFILES))
    ops({"purge": 1}, "purge")


# ---------------------------------------------------------------- main
NEWFILES = set()
FILES = ["assets/project-stage/rainbow/stage.js", "assets/project-stage/rainbow/poster.jpg", "inc/project-stage.php", "inc/project-experience.php"]
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
        if str(x.get("name", "")).startswith(("x-tmp-bl244-ops-", "x-tmp-bl245-ops-", "x-tmp-pl246-ops-", "x-tmp-wa247-ops-", "x-tmp-tc248-ops-", "x-tmp-bv249-ops-", "x-tmp-pe250-ops-", "x-tmp-fg251-ops-", "x-tmp-fg252-ops-", "x-tmp-bl253-ops-", "x-tmp-lg254-ops-", "x-tmp-ps255-ops-", "x-tmp-ps256-ops-", "x-tmp-ps258-ops-", "x-tmp-had247-ops-")) and x.get("active"):
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
        for res in ("recommendations-2026-09-24/deploy-result-257.json", "project-stage-2026-09-24/deploy-result-256.json", "project-stage-2026-09-24/deploy-result-255.json", "firgun-2026-09-24/deploy-result-251.json", "tour-calendar-2026-09-24/deploy-result-248.json", "profile-emoji-2026-09-24/deploy-result-250.json", "broker-video-2026-09-24/deploy-result-249.json", "tour-calendar-2026-09-24/deploy-result-248.json", "wa-pill-2026-09-24/deploy-result-247.json", "placements-2026-09-24/deploy-result-246.json"):
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
    bad = verify_pages("ps258" + str(int(time.time()))) if healthy else ["health"]
    if healthy and not bad and not verify_order("ps258o" + str(int(time.time()))):
        bad = ["order"]
    after = speed("after") if healthy else {}
    slow_after = [k for k, v in after.items() if not (isinstance(v[1], float) and v[1] < 5)]
    if healthy and slow_after:
        print("[speed] still slow after the release:", slow_after)
    if bad:
        # one more purge and a patient second look before rolling back (OPcache/LiteSpeed lag)
        ops({"purge": 1}, "purge again")
        time.sleep(12)
        healthy = wait_version(new, 45)
        bad = verify_pages("ps258b" + str(int(time.time()))) if healthy else ["health"]
        if healthy and not bad and not verify_order("ps258p" + str(int(time.time()))):
            bad = ["order"]
    if bad:
        print("[FAIL] pages:", bad)
        rollback(created)
        wait_version(old, 60)
        raise SystemExit("ROLLED BACK")
    json.dump({"released": new, "from": old, "at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "files": dict({rel: md5(NEW[rel]) for rel in FILES}, **{"nadlan-config.php": md5(new_main)}),
        "live_before": dict({rel: (md5(LIVE[rel]) if LIVE[rel] is not None else "missing") for rel in FILES}, **{"nadlan-config.php": md5(live_main)})},
        open(os.path.join(QA, "deploy-result-258.json"), "w", encoding="utf-8"), indent=2)
    json.dump({"before": before, "after": after}, open(os.path.join(QA, "speed-258.json"), "w", encoding="utf-8"), indent=2)
    print(f"RELEASE {new} LIVE")


finally:
    bridge_down()
