<?php
/**
 * HAD-256 local test bench. NEVER install on a real site.
 *
 * Runs inside WordPress Playground (SQLite) on 127.0.0.1 only. It:
 *   - loads the real nadlan-config modules the owner journey uses, from wp-content/nlj-code/ (the "after" variant
 *     mounts this worktree's plugins/nadlan-config/inc; the "before" variant mounts the files of commit 6e9cf930):
 *     broker-drop.php, owner-wizard.php, funnel.php, auth.php, property-owner.php, conversion-cta.php;
 *   - stubs what those modules expect from the rest of the plugin: the nadlan_property / nadlan_professional post
 *     types (same public args as nadlan-config.php, without the listing capability map), the plugin's own
 *     [nadlan_listing_wizard] shortcode (which owner-wizard.php replaces), and nadlan_compliance_scan (the same rules
 *     as inc/ai-features.php, copied);
 *   - turns every AI path off (NADLAN_DISABLE_AI) and blocks every outbound HTTP request (pre_http_request);
 *   - catches every email into wp-content/mail-sink/*.json (pre_wp_mail) - no mail leaves the machine;
 *   - creates the synthetic accounts of seed.json and the /post-listing/ page;
 *   - exposes test-only REST helpers (nlj-test/v1: reset, fault, state, mail) and the fault hooks the tests use:
 *     pause or kill a run at x-broker-drop's checkpoints, kill between a listing's INSERT and its first meta row,
 *     shorten the lock TTL, shorten the password-reset expiry. Off unless a test sets them.
 */
if ( ! defined( 'ABSPATH' ) ) { return; }
define( 'NADLAN_DISABLE_AI', true );
/* the caller's real address, kept for the test helpers; a test may present a synthetic documentation address
   (192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24) to prove per-address limits */
$GLOBALS['nlj_real_ip'] = (string) ( $_SERVER['REMOTE_ADDR'] ?? '' );
if ( ! empty( $_SERVER['HTTP_X_NLJ_IP'] ) && preg_match( '/^(?:192\.0\.2|198\.51\.100|203\.0\.113)\.\d{1,3}$/', (string) $_SERVER['HTTP_X_NLJ_IP'] ) ) {
	$_SERVER['REMOTE_ADDR'] = (string) $_SERVER['HTTP_X_NLJ_IP'];
}
define( 'NLJ_VARIANT', trim( (string) @file_get_contents( WP_CONTENT_DIR . '/nlj-variant.txt' ) ) ?: 'after' );

/* ---------------- stubs ---------------- */
add_action( 'init', function () {
	$base = array( 'public' => true, 'show_in_rest' => true, 'supports' => array( 'title', 'editor', 'thumbnail', 'custom-fields', 'excerpt' ) );
	register_post_type( 'nadlan_property', array_merge( $base, array( 'labels' => array( 'name' => 'NadLan Properties' ), 'has_archive' => 'properties', 'rewrite' => array( 'slug' => 'properties' ) ) ) );
	register_post_type( 'nadlan_professional', array_merge( $base, array( 'labels' => array( 'name' => 'NadLan Professionals' ), 'has_archive' => 'professionals', 'rewrite' => array( 'slug' => 'professionals' ) ) ) );
	add_shortcode( 'nadlan_listing_wizard', function () { return '<p>(the plugin\'s own wizard: a bench stub, replaced by x-owner-wizard)</p>'; } );
}, 5 );

if ( ! function_exists( 'nadlan_compliance_scan' ) ) {
	/** The rules of plugins/nadlan-config/inc/ai-features.php nadlan_compliance_scan(), copied for the bench. */
	function nadlan_compliance_scan( $text ) {
		$rules = array(
			array( '/מתאים\s+ל?(?:משפחות|זוגות\s+צעירים|רווקים|פנסיונרים)/u', 'family/age steering (familial status)' ),
			array( '/great\s+for\s+(?:families|young\s+professionals|empty\s+nesters)/i', 'family/age steering' ),
			array( '/perfect\s+for\s+(?:families|couples|singles)/i', 'familial steering' ),
			array( '/קרוב\s+ל(?:בית\s+כנסת|מסגד|כנסייה)/u', 'religious steering' ),
			array( '/שכונה\s+(?:דתית|חרדית|חילונית|ערבית|יהודית)/u', 'religious/ethnic steering' ),
			array( '/קהילה\s+(?:דתית|חרדית|חילונית|ערבית|יהודית|נוצרית|מוסלמית)/u', 'religious/ethnic steering' ),
			array( '/close\s+to\s+(?:church|synagogue|mosque|temple)/i', 'religious steering' ),
			array( '/walking\s+distance/i', 'ableist phrasing (use "near")' ),
			array( '/exclusive\s+(?:community|neighborhood)/i', 'exclusionary phrasing' ),
		);
		$hits = array();
		foreach ( $rules as $r ) {
			if ( preg_match( $r[0], (string) $text, $m ) ) { $hits[] = array( 'phrase' => $m[0], 'reason' => $r[1] ); }
		}
		return $hits;
	}
}

/* ---------------- the real modules ---------------- */
foreach ( array( 'broker-drop.php', 'owner-wizard.php', 'funnel.php', 'auth.php', 'property-owner.php', 'conversion-cta.php' ) as $nlj_f ) {
	if ( file_exists( WP_CONTENT_DIR . '/nlj-code/' . $nlj_f ) ) { require_once WP_CONTENT_DIR . '/nlj-code/' . $nlj_f; }
}

/* ---------------- nothing leaves the machine ---------------- */
add_filter( 'pre_http_request', function ( $pre, $args, $url ) {
	$host = (string) wp_parse_url( $url, PHP_URL_HOST );
	if ( in_array( $host, array( '127.0.0.1', 'localhost' ), true ) ) { return $pre; }
	@file_put_contents( WP_CONTENT_DIR . '/nlj-blocked-http.log', gmdate( 'c' ) . ' ' . $url . "\n", FILE_APPEND );
	return new WP_Error( 'nlj_offline', 'HAD-256 bench: outbound HTTP is blocked' );
}, 1, 3 );

add_filter( 'pre_wp_mail', function ( $null, $atts ) {
	$dir = WP_CONTENT_DIR . '/mail-sink';
	wp_mkdir_p( $dir );
	$name = gmdate( 'Ymd-His' ) . '-' . substr( md5( uniqid( '', true ) ), 0, 8 ) . '.json';
	@file_put_contents( $dir . '/' . $name, wp_json_encode( array( 'to' => $atts['to'], 'subject' => $atts['subject'], 'message' => $atts['message'], 'headers' => $atts['headers'], 't' => time() ), JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) );
	return true;
}, 1, 2 );

/* the toolbar stays off for owners, as on the live site */
add_filter( 'show_admin_bar', function ( $show ) { return current_user_can( 'edit_posts' ) ? $show : false; } );

/* the design system's two families, for screenshots that look like the live site (the live theme loads them) */
add_action( 'wp_enqueue_scripts', function () {
	wp_enqueue_style( 'nlj-fonts', 'https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700;800&family=Noto+Serif+Hebrew:wght@600;700&display=swap', array(), null );
} );

/* ---------------- the synthetic site ---------------- */
function nlj_seed() {
	$s = json_decode( (string) @file_get_contents( WP_CONTENT_DIR . '/nlj-seed.json' ), true );
	return is_array( $s ) ? $s : array( 'users' => array() );
}

function nlj_setup_users() {
	foreach ( nlj_seed()['users'] as $u ) {
		$id = email_exists( $u['email'] );
		if ( ! $id ) {
			$id = wp_insert_user( array( 'user_login' => $u['login'], 'user_email' => $u['email'], 'user_pass' => $u['password'], 'display_name' => $u['name'], 'first_name' => $u['name'], 'role' => $u['role'] ) );
		} else {
			wp_set_password( $u['password'], $id );
			wp_update_user( array( 'ID' => $id, 'role' => $u['role'], 'display_name' => $u['name'], 'first_name' => $u['name'] ) );
		}
		if ( ! is_wp_error( $id ) ) {
			foreach ( array( 'nl_owner_name', 'nl_owner_phone', 'phone' ) as $k ) { delete_user_meta( $id, $k ); }
		}
	}
}

add_action( 'init', function () {
	if ( get_option( 'nlj_setup' ) === '3' || ! file_exists( WP_CONTENT_DIR . '/nlj-seed.json' ) ) { return; }
	update_option( 'users_can_register', 1 );
	update_option( 'default_role', 'subscriber' );
	update_option( 'blogname', 'nad-lan bench (local)' );
	update_option( 'permalink_structure', '/%postname%/' );
	update_option( 'nadlan_owner_whatsapp', (string) ( nlj_seed()['whatsapp_stub'] ?? '972000000000' ) );
	nlj_setup_users();
	$admin = get_user_by( 'email', 'bench.admin@example.test' );
	if ( $admin ) { update_option( 'nl_drop_author', $admin->ID ); update_option( 'admin_email', 'bench.admin@example.test' ); }
	if ( ! get_page_by_path( 'post-listing' ) ) {
		wp_insert_post( array( 'post_type' => 'page', 'post_status' => 'publish', 'post_name' => 'post-listing', 'post_title' => 'פרסום נכס', 'post_content' => '<!-- wp:shortcode -->[nadlan_listing_wizard]<!-- /wp:shortcode -->' ) );
	}
	foreach ( array( 'terms' => 'תנאי שימוש', 'privacy' => 'מדיניות פרטיות' ) as $slug => $t ) {
		if ( ! get_page_by_path( $slug ) ) { wp_insert_post( array( 'post_type' => 'page', 'post_status' => 'publish', 'post_name' => $slug, 'post_title' => $t, 'post_content' => '(bench placeholder)' ) ); }
	}
	flush_rewrite_rules( false );
	update_option( 'nlj_setup', '3' );
}, 50 );

/* ---------------- fault hooks (off unless a test sets them) ---------------- */
function nlj_fault( $name ) {
	global $wpdb;
	$raw = $wpdb->get_var( $wpdb->prepare( "SELECT option_value FROM {$wpdb->options} WHERE option_name = %s", 'nlj_fault_' . $name ) );
	return $raw === null ? null : json_decode( (string) $raw, true );
}

function nlj_fault_take( $name ) {
	global $wpdb;
	$f = nlj_fault( $name );
	if ( ! $f ) { return null; }
	$left = (int) ( $f['n'] ?? 1 ) - 1;
	if ( $left <= 0 ) { $wpdb->delete( $wpdb->options, array( 'option_name' => 'nlj_fault_' . $name ) ); }
	else { $f['n'] = $left; $wpdb->update( $wpdb->options, array( 'option_value' => wp_json_encode( $f ) ), array( 'option_name' => 'nlj_fault_' . $name ) ); }
	return $f;
}

function nlj_log( $line ) {
	@file_put_contents( WP_CONTENT_DIR . '/nlj-faults.log', gmdate( 'H:i:s' ) . ' pid' . getmypid() . ' ' . $line . "\n", FILE_APPEND );
}

function nlj_kill( $where ) {
	nlj_log( 'KILL at ' . $where );
	if ( ! headers_sent() ) { status_header( 500 ); header( 'Content-Type: application/json' ); }
	echo '{"code":"nlj_killed","where":' . wp_json_encode( $where ) . '}';
	exit;   // the process stops here: no finally block, no lock release, no further write
}

/* x-broker-drop 1.1.4 checkpoints (the "after" code only) */
add_action( 'nl_drop_checkpoint', function ( $where, $drop ) {
	$p = nlj_fault( 'pause' );
	if ( $p && $p['where'] === $where ) {
		nlj_fault_take( 'pause' );
		nlj_log( 'PAUSE ' . (int) $p['secs'] . 's at ' . $where . ' drop ' . $drop );
		sleep( (int) $p['secs'] );
		nlj_log( 'RESUME at ' . $where . ' drop ' . $drop );
	}
	$k = nlj_fault( 'kill' );
	if ( $k && $k['where'] === $where ) { nlj_fault_take( 'kill' ); nlj_kill( $where ); }
}, 10, 2 );

/* both variants: kill between a listing's INSERT and its first meta row (the first add_post_metadata of a nadlan_property) */
add_filter( 'add_post_metadata', function ( $check, $object_id ) {
	$k = nlj_fault( 'kill' );
	if ( $k && $k['where'] === 'row_meta' && get_post_type( $object_id ) === 'nadlan_property' ) { nlj_fault_take( 'kill' ); nlj_kill( 'row_meta (post ' . (int) $object_id . ')' ); }
	return $check;
}, 1, 2 );

/* both variants: kill right after a listing row is inserted (before any later write) */
add_action( 'wp_insert_post', function ( $id, $post, $update ) {
	if ( $post->post_type !== 'nadlan_property' ) { return; }
	$k = nlj_fault( 'kill' );
	if ( $k && $k['where'] === 'row' && ! $update ) { nlj_fault_take( 'kill' ); nlj_kill( 'row (post ' . (int) $id . ', status ' . $post->post_status . ')' ); }
	$p = nlj_fault( 'pause' );
	if ( $p && $p['where'] === 'row' && ! $update ) { nlj_fault_take( 'pause' ); nlj_log( 'PAUSE ' . (int) $p['secs'] . 's after insert ' . $id ); sleep( (int) $p['secs'] ); }
}, 1, 3 );

/* both variants: widen the window between reading nl_result and writing it (the 1.1.3 race) */
add_action( 'save_post_nadlan_property', function () {
	$s = nlj_fault( 'slow' );
	if ( $s ) { usleep( (int) ( (float) $s['secs'] * 1000000 ) ); }
}, 1 );

add_filter( 'nl_drop_lock_ttl', function ( $ttl ) { $t = nlj_fault( 'ttl' ); return $t ? (int) $t['secs'] : $ttl; } );
add_filter( 'password_reset_expiration', function ( $s ) { $t = nlj_fault( 'reset_ttl' ); return $t ? (int) $t['secs'] : $s; } );

/* ---------------- test-only REST helpers (127.0.0.1 only) ---------------- */
add_action( 'rest_api_init', function () {
	$local = function () { return in_array( (string) $GLOBALS['nlj_real_ip'], array( '127.0.0.1', '::1', '' ), true ); };
	register_rest_route( 'nlj-test/v1', '/reset', array( 'methods' => 'POST', 'permission_callback' => $local, 'callback' => 'nlj_reset' ) );
	register_rest_route( 'nlj-test/v1', '/fault', array( 'methods' => 'POST', 'permission_callback' => $local, 'callback' => function ( WP_REST_Request $r ) {
		$name = sanitize_key( (string) $r->get_param( 'name' ) );
		$val  = $r->get_param( 'value' );
		delete_option( 'nlj_fault_' . $name );
		if ( $val !== null && $val !== '' ) { add_option( 'nlj_fault_' . $name, wp_json_encode( $val ), '', 'no' ); }
		return array( 'ok' => true, 'name' => $name, 'value' => $val );
	} ) );
	register_rest_route( 'nlj-test/v1', '/state', array( 'methods' => 'GET', 'permission_callback' => $local, 'callback' => 'nlj_state' ) );
	register_rest_route( 'nlj-test/v1', '/mail', array( 'methods' => 'GET', 'permission_callback' => $local, 'callback' => function () {
		$out = array();
		foreach ( (array) glob( WP_CONTENT_DIR . '/mail-sink/*.json' ) as $f ) { $out[] = json_decode( (string) file_get_contents( $f ), true ) + array( 'file' => basename( $f ) ); }
		return $out;
	} ) );
	register_rest_route( 'nlj-test/v1', '/user', array( 'methods' => 'GET', 'permission_callback' => $local, 'callback' => function ( WP_REST_Request $r ) {
		$u = get_user_by( 'email', (string) $r->get_param( 'email' ) );
		return $u ? array( 'id' => $u->ID, 'login' => $u->user_login ) : array( 'id' => 0 );
	} ) );
} );

function nlj_reset() {
	global $wpdb;
	foreach ( array( 'nadlan_drop', 'nadlan_property', 'attachment' ) as $t ) {
		foreach ( $wpdb->get_col( $wpdb->prepare( "SELECT ID FROM {$wpdb->posts} WHERE post_type = %s", $t ) ) as $id ) { wp_delete_post( (int) $id, true ); }
	}
	foreach ( $wpdb->get_col( "SELECT ID FROM {$wpdb->posts} WHERE post_status = 'auto-draft'" ) as $id ) { wp_delete_post( (int) $id, true ); }
	$like = array( 'nl\\_drop\\_lock\\_%', 'nl\\_pub\\_%', 'nl\\_att\\_%', 'nl\\_owner\\_ck\\_%', 'nlj\\_fault\\_%', '\\_transient\\_%nlowner%', '\\_transient\\_timeout\\_%nlowner%', '\\_transient\\_%nlauth%', '\\_transient\\_timeout\\_%nlauth%', '\\_transient\\_%nlqr%', '\\_transient\\_timeout\\_%nlqr%' );
	foreach ( $like as $l ) { $wpdb->query( "DELETE FROM {$wpdb->options} WHERE option_name LIKE '" . $l . "'" ); }
	wp_cache_flush();
	foreach ( (array) glob( WP_CONTENT_DIR . '/mail-sink/*.json' ) as $f ) { @unlink( $f ); }
	@file_put_contents( WP_CONTENT_DIR . '/nlj-faults.log', '' );
	foreach ( get_users( array( 'fields' => 'ID' ) ) as $uid ) {
		$u = get_userdata( $uid );
		$known = wp_list_pluck( nlj_seed()['users'], 'email' );
		if ( $u && ! in_array( $u->user_email, $known, true ) && ! user_can( $uid, 'manage_options' ) ) { require_once ABSPATH . 'wp-admin/includes/user.php'; wp_delete_user( $uid ); }
	}
	nlj_setup_users();
	return array( 'ok' => true, 'variant' => NLJ_VARIANT );
}

function nlj_state( WP_REST_Request $r ) {
	global $wpdb;
	$drop = (int) $r->get_param( 'drop' );
	$out  = array( 'variant' => NLJ_VARIANT );
	$props = $wpdb->get_results( "SELECT ID, post_status, post_name, post_title, guid FROM {$wpdb->posts} WHERE post_type = 'nadlan_property' ORDER BY ID", ARRAY_A );
	foreach ( $props as &$p ) { $p['nl_drop_id'] = get_post_meta( $p['ID'], 'nl_drop_id', true ); $p['meta_n'] = (int) $wpdb->get_var( $wpdb->prepare( "SELECT COUNT(*) FROM {$wpdb->postmeta} WHERE post_id = %d", $p['ID'] ) ); }
	$out['properties'] = $props;
	$out['drops']      = $wpdb->get_results( "SELECT ID, post_status, post_title FROM {$wpdb->posts} WHERE post_type = 'nadlan_drop' ORDER BY ID", ARRAY_A );
	$out['attachments'] = $wpdb->get_results( "SELECT ID, post_status, guid, post_parent FROM {$wpdb->posts} WHERE post_type = 'attachment' ORDER BY ID", ARRAY_A );
	$out['options']    = $wpdb->get_results( "SELECT option_name, option_value FROM {$wpdb->options} WHERE option_name LIKE 'nl\\_drop\\_lock\\_%' OR option_name LIKE 'nl\\_pub\\_%' OR option_name LIKE 'nl\\_att\\_%' OR option_name LIKE 'nlj\\_fault\\_%'", ARRAY_A );
	if ( $drop ) {
		$m = array();
		foreach ( array( 'nl_state', 'nl_result', 'nl_fence', 'nl_pub_req', 'nl_pub_rev', 'nl_lock_takeover', 'nl_reconciled', 'nl_draft', 'nl_hold' ) as $k ) { $m[ $k ] = get_post_meta( $drop, $k, true ); }
		$out['drop'] = $m;
	}
	$out['faults_log'] = (string) @file_get_contents( WP_CONTENT_DIR . '/nlj-faults.log' );
	return $out;
}
