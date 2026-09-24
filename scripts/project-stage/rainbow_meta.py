# -*- coding: utf-8 -*-
"""Rainbow's page truth, the fields around the text (the site loop, R2, 25.9.2026). The page had promises it does not keep
and pictures that are not true:
- the meta description and the social description promised "בחירת דירה בתלת ממד, תוכניות" (the page picks a floor and a
  direction, and has no plans yet);
- the social preview picture (twitter, and a second og:image) is the old showroom poster, which advertises
  "מודל 3D ובחירת דירות" and a sun simulation;
- the project card's gallery (photos_csv) held three AI resort pictures that put the tower on the beach with a lagoon pool
  in the courtyard. The tower stands about 700 m from the sea, and the pools are on two boutique roofs.
This reads every Yoast field of post 4464 plus photos_csv and the featured image (read-only), and with --apply writes:
the description (meta, og, twitter), the twitter picture and the og picture = the house-style plate that is already the
page's first og:image, and photos_csv emptied (the three files stay in the media library; the old value is saved in
docs/qa). Each write is guarded by the value read just before. Same token-gated temporary bridge as the release runners;
the app password is decrypted in-process (DPAPI), never printed.
  python scripts/project-stage/rainbow_meta.py            # read
  python scripts/project-stage/rainbow_meta.py --apply    # write"""
import base64, ctypes, ctypes.wintypes, io, json, os, secrets, sys, time, urllib.request, urllib.error
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = "https://nad-lan.co.il"
REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
QA = os.path.join(REPO, "docs", "qa", "rainbow-content-2026-09-24")
SECRETS_PATH = r"C:\Users\777\Documents\websites\.codex-secrets\wordpress-app-passwords\nad-lan.co.il.json"
APPLY = "--apply" in sys.argv
PID = 4464
PLATE = "https://nad-lan.co.il/wp-content/uploads/2026/07/rainbow-tel-aviv-plate-v3.webp"
DESC = ("ריינבו תל אביב (Rainbow Tel Aviv) של ישראל קנדה בשדה דב: מגדל 39 קומות, 459 דירות, "
        "כ-81,800 ₪ למ\"ר לפי דוחות היזם. בחירת קומה וכיוון והנוף מהקומה.")


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
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) NadLan-RB-META/1.0"


def req(method, path, body=None, timeout=60):
    r = urllib.request.Request(BASE + path, data=None if body is None else json.dumps(body, ensure_ascii=False).encode(), method=method)
    r.add_header("Authorization", AUTH)
    r.add_header("User-Agent", UA)
    if body is not None:
        r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8") or "null")
    except urllib.error.HTTPError as e:
        p = e.read()
        try:
            return e.code, json.loads(p.decode("utf-8"))
        except Exception:
            return e.code, {"raw": p[:300].decode("utf-8", "replace")}


TOKEN = secrets.token_hex(24)
NS = "nadlan-rbmeta-" + TOKEN[:8]
BRIDGE = r"""
add_action( 'rest_api_init', function () {
	register_rest_route( '__NS__/v1', '/run', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( $b['token'] ?? '' ) ) ) { return new WP_Error( 'forbidden', 'token', array( 'status' => 400 ) ); }
			$pid  = __PID__;
			$read = function () use ( $pid ) {
				$all = get_post_meta( $pid );
				$y   = array();
				foreach ( $all as $k => $v ) {
					if ( 0 === strpos( $k, '_yoast_wpseo_' ) ) { $y[ $k ] = is_array( $v ) ? $v[0] : $v; }
				}
				$ind = null;
				global $wpdb;
				$t = $wpdb->prefix . 'yoast_indexable';
				if ( $wpdb->get_var( $wpdb->prepare( 'SHOW TABLES LIKE %s', $t ) ) === $t ) {
					$ind = $wpdb->get_row( $wpdb->prepare( "SELECT id, description, open_graph_description, open_graph_image, open_graph_image_id, open_graph_image_source, open_graph_image_meta, twitter_description, twitter_image, twitter_image_id, twitter_image_source FROM $t WHERE object_id = %d AND object_type = 'post'", $pid ), ARRAY_A );
				}
				return array(
					'yoast'       => $y,
					'photos_csv'  => (string) get_post_meta( $pid, 'photos_csv', true ),
					'thumbnail'   => (int) get_post_thumbnail_id( $pid ),
					'thumb_url'   => (string) wp_get_attachment_url( get_post_thumbnail_id( $pid ) ),
					'plate_id'    => (int) attachment_url_to_postid( '__PLATE__' ),
					'indexable'   => $ind,
				);
			};
			$out = array( 'before' => $read() );
			if ( ! empty( $b['do'] ) ) {
				$w = (array) ( $b['write'] ?? array() );
				$done = array();
				foreach ( $w as $k => $pair ) {
					$cur = (string) get_post_meta( $pid, $k, true );
					if ( $cur !== (string) $pair[0] ) { $done[ $k ] = 'SKIP: changed since read'; continue; }
					if ( '' === (string) $pair[1] ) { delete_post_meta( $pid, $k ); } else { update_post_meta( $pid, $k, wp_slash( (string) $pair[1] ) ); }
					$done[ $k ] = 'ok';
				}
				// Yoast keeps its own copy of these fields (the indexable); rebuild it from the post
				if ( function_exists( 'YoastSEO' ) ) {
					try {
						$repo = YoastSEO()->classes->get( \Yoast\WP\SEO\Repositories\Indexable_Repository::class );
						$bld  = YoastSEO()->classes->get( \Yoast\WP\SEO\Builders\Indexable_Builder::class );
						$ix   = $repo->find_by_id_and_type( $pid, 'post', false );
						if ( $ix ) { $bld->build_for_id_and_type( $pid, 'post', $ix ); $done['indexable'] = 'rebuilt'; }
					} catch ( \Throwable $e ) { $done['indexable'] = 'error: ' . $e->getMessage(); }
				}
				clean_post_cache( $pid );
				do_action( 'litespeed_purge_post', $pid );
				do_action( 'litespeed_purge_all' );
				$out['done']  = $done;
				$out['after'] = $read();
			}
			return $out;
		},
	) );
} );
""".replace("__TOKEN__", TOKEN).replace("__NS__", NS).replace("__PID__", str(PID)).replace("__PLATE__", PLATE)

s, c = req("POST", "/wp-json/code-snippets/v1/snippets", {"name": "x-tmp-rbmeta-%d" % int(time.time()), "code": BRIDGE, "scope": "global", "active": False})
if s not in (200, 201):
    raise SystemExit("FATAL bridge create %s %s" % (s, str(c)[:200]))
BR = c["id"]
try:
    req("PUT", "/wp-json/code-snippets/v1/snippets/%s/activate" % BR, {})
    r = None
    for _ in range(10):
        s, r = req("POST", "/wp-json/" + NS + "/v1/run", {"token": TOKEN})
        if s == 200:
            break
        time.sleep(1.5)
    if s != 200:
        raise SystemExit("FATAL bridge call %s %s" % (s, str(r)[:300]))
    before = r["before"]
    print("[before]", json.dumps(before, ensure_ascii=False, indent=1))
    print("[desc] %d chars: %s" % (len(DESC), DESC))
    if APPLY:
        y = before["yoast"]
        write = {}
        for k in ("_yoast_wpseo_metadesc", "_yoast_wpseo_opengraph-description", "_yoast_wpseo_twitter-description"):
            if k in y or k == "_yoast_wpseo_metadesc":
                write[k] = [y.get(k, ""), DESC]
        # the user-set social pictures go; Yoast then uses the featured image, which is the plate (one og:image)
        if before.get("thumb_url") == PLATE:
            for k in ("_yoast_wpseo_twitter-image", "_yoast_wpseo_twitter-image-id", "_yoast_wpseo_opengraph-image", "_yoast_wpseo_opengraph-image-id"):
                if y.get(k):
                    write[k] = [y[k], ""]
        if before.get("photos_csv"):
            write["photos_csv"] = [before["photos_csv"], ""]
        os.makedirs(QA, exist_ok=True)
        stamp = time.strftime("%Y%m%dT%H%M%S")
        io.open(os.path.join(QA, "post-4464.meta.%s.before.json" % stamp), "w", encoding="utf-8").write(json.dumps(before, ensure_ascii=False, indent=1))
        print("[write plan]", json.dumps({k: v[1][:90] for k, v in write.items()}, ensure_ascii=False, indent=1))
        s, r2 = req("POST", "/wp-json/" + NS + "/v1/run", {"token": TOKEN, "do": 1, "write": write})
        print("[set]", s, json.dumps(r2.get("done") if isinstance(r2, dict) else r2, ensure_ascii=False))
        if isinstance(r2, dict) and r2.get("after"):
            io.open(os.path.join(QA, "post-4464.meta.%s.after.json" % stamp), "w", encoding="utf-8").write(json.dumps(r2["after"], ensure_ascii=False, indent=1))
            print("[after]", json.dumps(r2["after"], ensure_ascii=False, indent=1))
finally:
    req("PUT", "/wp-json/code-snippets/v1/snippets/%s/deactivate" % BR, {})
    s, _ = req("DELETE", "/wp-json/code-snippets/v1/snippets/%s" % BR)
    time.sleep(1.5)
    s2, _ = req("POST", "/wp-json/" + NS + "/v1/run", {"token": TOKEN})
    print("[bridge] delete http %s; route now http %s (want 404)" % (s, s2))
