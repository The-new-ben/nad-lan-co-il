# -*- coding: utf-8 -*-
"""Controlled live test of join + four languages with an obviously fake broker ("בדיקת מערכת", marked nl_test=1).
ops:
  create                     nl_join_create as DRAFT (register skipped: the identity is fake), mail blocked; langs he,en,ru,fr; auto 0
  broker-publish ID          the test broker record published (so its drop link works), IndexNow detached
  publish ID / draft ID      every page of the test broker published (then re-rendered: language links, hreflang) or back to draft
  report ID                  the test broker's pages and their state
  trash ID                   every post of the test broker to the trash (only a broker marked nl_test=1)
"""
import importlib.util, io, json, secrets, sys, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ARGS = sys.argv[1:]
sys.argv = ["x"]
spec = importlib.util.spec_from_file_location("ms", r"C:/Users/777/nad-lan/nad-lan-co-il/handoff/meital-2026-09-17/runners/meital_site.py")
m = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(m)
except SystemExit:
    pass
TOKEN = secrets.token_hex(24)
BRIDGE = r'''
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-jointest/v1', '/run', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( $b['token'] ?? '' ) ) ) { return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) ); }
			if ( ! function_exists( 'nl_join_create' ) || ! function_exists( 'nl_drop_site_sync' ) ) { return new WP_Error( 'nomodule', 'modules not loaded', array( 'status' => 500 ) ); }
			remove_action( 'save_post', 'nadlan_config_indexnow_on_save', 20 );
			add_filter( 'pre_wp_mail', '__return_true' );
			$op  = (string) $b['op'];
			$bid = (int) ( $b['id'] ?? 0 );
			$is_test = function ( $bid ) { return $bid && get_post_type( $bid ) === 'nadlan_professional' && get_post_meta( $bid, 'nl_test', true ) === '1'; };
			$pages = function ( $bid ) {
				$ids = array();
				foreach ( array( 'nadlan_property', 'page' ) as $t ) {
					foreach ( array( 'nl_broker_id', 'nl_broker_auto' ) as $k ) {
						$ids = array_merge( $ids, get_posts( array( 'post_type' => $t, 'post_status' => array( 'publish', 'draft' ), 'numberposts' => 100, 'fields' => 'ids', 'suppress_filters' => true, 'meta_query' => array( array( 'key' => $k, 'value' => (string) $bid ) ) ) ) );
					}
				}
				return array_values( array_unique( array_map( 'intval', $ids ) ) );
			};
			if ( $op === 'create' ) {
				$r = nl_join_create( array(
					'licence' => '0000001', 'name_he' => 'בדיקת מערכת', 'name_en' => 'System Check', 'brand' => '', 'phone' => '052-0000000', 'email' => 'check@example.invalid',
					'areas' => array( 'פלורנטין', 'נווה צדק', 'יפו' ), 'bio' => 'עמוד בדיקה של המערכת. יורד מהאוויר בתוך דקות.', 'gender' => 'm',
					'register' => array( 'found' => false, 'name' => 'בדיקה', 'city' => '' ), 'lang' => 'he',
				), 'draft' );
				if ( is_wp_error( $r ) ) { return $r; }
				update_post_meta( $r['broker'], 'nl_test', '1' );
				update_post_meta( $r['broker'], 'nl_langs', 'he,en,ru,fr' );
				update_post_meta( $r['broker'], 'nl_auto_publish', '0' );
				$r['areas'] = array( 'en' => get_post_meta( $r['broker'], 'nl_areas_en', true ), 'ru' => get_post_meta( $r['broker'], 'nl_areas_ru', true ), 'fr' => get_post_meta( $r['broker'], 'nl_areas_fr', true ) );
				return $r;
			}
			if ( ! $is_test( $bid ) ) { return new WP_Error( 'refused', 'not a test broker', array( 'status' => 403 ) ); }
			if ( $op === 'broker-publish' ) { wp_update_post( array( 'ID' => $bid, 'post_status' => 'publish' ) ); return array( 'broker' => get_post_status( $bid ) ); }
			if ( $op === 'publish' || $op === 'draft' ) {
				$st = $op === 'publish' ? 'publish' : 'draft';
				foreach ( $pages( $bid ) as $id ) { wp_update_post( array( 'ID' => $id, 'post_status' => $st ) ); }
				$br = nl_drop_broker( $bid );
				foreach ( get_posts( array( 'post_type' => 'nadlan_property', 'post_status' => array( 'publish', 'draft' ), 'numberposts' => 50, 'fields' => 'ids', 'suppress_filters' => true, 'meta_query' => array( array( 'key' => 'nl_broker_id', 'value' => (string) $bid ) ) ) ) as $he ) { nl_drop_render_all( $he, $br ); }
				nl_drop_site_sync( $br );
				$ids = $pages( $bid );
				nl_drop_purge( $ids );
				$out = array();
				foreach ( $ids as $id ) { $out[] = array( $id, get_post_type( $id ), get_post_status( $id ), get_permalink( $id ) ); }
				return $out;
			}
			if ( $op === 'report' ) {
				$out = array( 'broker' => array( get_post_status( $bid ), get_permalink( $bid ) ), 'pages' => array() );
				foreach ( $pages( $bid ) as $id ) { $out['pages'][] = array( $id, get_post_type( $id ), get_post_status( $id ), get_permalink( $id ), get_post_meta( $id, 'nl_lang', true ), get_post_meta( $id, 'nl_hreflang', true ) ); }
				$drops = get_posts( array( 'post_type' => 'nadlan_drop', 'post_status' => 'private', 'numberposts' => 10, 'suppress_filters' => true, 'meta_query' => array( array( 'key' => 'nl_broker_id', 'value' => (string) $bid ) ) ) );
				foreach ( $drops as $d ) { $out['drops'][] = array( $d->ID, get_post_meta( $d->ID, 'nl_state', true ), get_post_meta( $d->ID, 'nl_usage', true ), get_post_meta( $d->ID, 'nl_plain', true ), get_post_meta( $d->ID, 'nl_result', true ) ); }
				return $out;
			}
			if ( $op === 'trash' ) {
				$out = array();
				foreach ( $pages( $bid ) as $id ) { wp_update_post( array( 'ID' => $id, 'post_status' => 'draft' ) ); $out[ $id ] = wp_trash_post( $id ) ? 'trashed' : 'failed'; }
				foreach ( get_posts( array( 'post_type' => 'nadlan_drop', 'post_status' => 'private', 'numberposts' => 20, 'fields' => 'ids', 'suppress_filters' => true, 'meta_query' => array( array( 'key' => 'nl_broker_id', 'value' => (string) $bid ) ) ) ) as $d ) { $out[ $d ] = wp_trash_post( $d ) ? 'trashed drop' : 'failed'; }
				delete_post_meta( $bid, '_nl_drop_token' );
				update_post_meta( $bid, 'nl_drop_on', '0' );
				wp_update_post( array( 'ID' => $bid, 'post_status' => 'draft' ) );
				$out[ $bid ] = wp_trash_post( $bid ) ? 'trashed broker' : 'failed';
				return $out;
			}
			return new WP_Error( 'op', 'unknown op' );
		},
	) );
} );
'''.replace("__TOKEN__", TOKEN)


def snip(method, path, body=None):
    return m.req(method, "/code-snippets/v1/snippets" + path, body)


s, c = snip("POST", "", {"name": f"tmp-jointest-{int(time.time())}", "code": "/* placeholder */", "scope": "global", "active": False})
br = c["id"]
try:
    snip("PUT", f"/{br}", {"name": c["name"], "code": BRIDGE, "scope": "global", "active": False})
    s, a = snip("PUT", f"/{br}/activate", {})
    print("bridge", s)
    body = {"token": TOKEN, "op": ARGS[0]}
    if len(ARGS) > 1:
        body["id"] = int(ARGS[1])
    s, r = m.req("POST", "/nadlan-jointest/v1/run", body)
    print(ARGS[0], s, json.dumps(r, ensure_ascii=False, indent=1)[:6000])
    if ARGS[0] == "create" and isinstance(r, dict) and r.get("drop"):
        open("test_drop_url.txt", "w", encoding="utf-8").write(r["drop"])
finally:
    s1, _ = snip("PUT", f"/{br}/deactivate", {})
    s2, _ = snip("DELETE", f"/{br}")
    print("bridge cleanup", s1, s2)
