<?php
/**
 * nadlan-config - URBAN RENEWAL PROJECT SPACE (L4, 2026-07-12).
 *
 * The private building room: per-apartment consent tracked and painted on
 * the 3D standard model, the 10-stage bureaucratic ladder, an updates feed
 * (send-gated, deliverability-last), invite-by-token membership, and the
 * /my-renewal/ dashboard. Documents live in urban-docs.php.
 *
 * PRIVACY BY CONSTRUCTION: CPT nadlan_renewal is public=false, no rewrite,
 * no REST show - there is NO front-end URL to index. All access flows
 * through the dashboard route + membership-checked REST. A renewal space
 * never touches the public nadlan_project machinery (indexnow, milestones,
 * facets, schema) - that is why it is a separate CPT.
 *
 * Feature gate: option nadlan_feature_renewal_space ('1' = on).
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_ur_space_on' ) ) {
	function nadlan_ur_space_on() { return get_option( 'nadlan_feature_renewal_space', '1' ) === '1'; }
}

/* ---------- CPT ---------- */
add_action( 'init', function () {
	register_post_type( 'nadlan_renewal', array(
		'labels'              => array( 'name' => 'חדרי התחדשות', 'singular_name' => 'חדר התחדשות' ),
		'public'              => false,
		'show_ui'             => true,
		'show_in_rest'        => false,
		'exclude_from_search' => true,
		'publicly_queryable'  => false,
		'rewrite'             => false,
		'has_archive'         => false,
		'show_in_menu'        => 'edit.php?post_type=nadlan_project',
		'supports'            => array( 'title' ),
		'capability_type'     => 'post',
		'map_meta_cap'        => true,
	) );
} );

/* ---------- consent enum + sanitizers ---------- */
if ( ! function_exists( 'nadlan_ur_consent_statuses' ) ) {
	function nadlan_ur_consent_statuses() {
		return array(
			'consented'    => array( 'חתמו', '#517048' ),
			'in_process'   => array( 'בתהליך', '#9C7A3C' ),
			'missing_docs' => array( 'חסרים מסמכים', '#C2563A' ),
			'refused'      => array( 'סירבו', '#7A2E1D' ),
			'unreached'    => array( 'טרם הושג קשר', '#A79E8D' ),
		);
	}
}
if ( ! function_exists( 'nadlan_ur_doc_keys' ) ) {
	function nadlan_ur_doc_keys() {
		return array( 'id_copy' => 'צילום תעודת זהות', 'ownership_nesach' => 'נסח טאבו', 'signed_agreement' => 'הסכם חתום', 'poa' => 'ייפוי כוח' );
	}
}
if ( ! function_exists( 'nadlan_ur_clean_apartments' ) ) {
	function nadlan_ur_clean_apartments( $raw ) {
		$statuses = array_keys( nadlan_ur_consent_statuses() );
		$dirs = array( 'west', 'east', 'north', 'south' );
		$out = array();
		foreach ( (array) $raw as $u ) {
			if ( ! is_array( $u ) || empty( $u['id'] ) ) { continue; }
			$docs = array();
			foreach ( array_keys( nadlan_ur_doc_keys() ) as $dk ) { $docs[ $dk ] = ! empty( $u['docs'][ $dk ] ); }
			$out[] = array(
				'id'             => sanitize_key( $u['id'] ),
				'floor'          => max( 0, min( 60, (int) ( $u['floor'] ?? 0 ) ) ),
				'pos'            => max( 0, min( 20, (int) ( $u['pos'] ?? 0 ) ) ),
				'dir'            => in_array( $u['dir'] ?? '', $dirs, true ) ? $u['dir'] : 'west',
				'label'          => mb_substr( sanitize_text_field( (string) ( $u['label'] ?? '' ) ), 0, 60 ),
				'consent_status' => in_array( $u['consent_status'] ?? '', $statuses, true ) ? $u['consent_status'] : 'unreached',
				'docs'           => $docs,
				'contact_note'   => mb_substr( sanitize_text_field( (string) ( $u['contact_note'] ?? '' ) ), 0, 200 ),
				'note'           => mb_substr( sanitize_text_field( (string) ( $u['note'] ?? '' ) ), 0, 400 ),
				'updated'        => current_time( 'mysql' ),
			);
			if ( count( $out ) >= 400 ) { break; }
		}
		return $out;
	}
}
if ( ! function_exists( 'nadlan_ur_apartment_completion' ) ) {
	function nadlan_ur_apartment_completion( $unit ) {
		$done = array(); $missing = array();
		foreach ( nadlan_ur_doc_keys() as $k => $label ) {
			if ( ! empty( $unit['docs'][ $k ] ) ) { $done[] = $label; } else { $missing[] = $label; }
		}
		$n = count( $done ) + count( $missing );
		return array( 'score' => $n ? (int) round( count( $done ) / $n * 100 ) : 0, 'done' => $done, 'missing' => $missing );
	}
}

/* ---------- membership ---------- */
if ( ! function_exists( 'nadlan_ur_members' ) ) {
	function nadlan_ur_members( $space_id ) {
		$m = json_decode( (string) get_post_meta( $space_id, 'member_emails', true ), true );
		return is_array( $m ) ? $m : array();
	}
}
if ( ! function_exists( 'nadlan_ur_can_manage' ) ) {
	function nadlan_ur_can_manage( $space_id ) {
		if ( current_user_can( 'manage_options' ) ) { return true; }
		return (int) get_post_meta( $space_id, 'owner_user_id', true ) === get_current_user_id() && get_current_user_id() > 0;
	}
}
if ( ! function_exists( 'nadlan_ur_can_view' ) ) {
	function nadlan_ur_can_view( $space_id ) {
		if ( nadlan_ur_can_manage( $space_id ) ) { return true; }
		$u = wp_get_current_user();
		if ( ! $u || ! $u->exists() ) { return false; }
		foreach ( nadlan_ur_members( $space_id ) as $m ) {
			if ( isset( $m['email'] ) && strtolower( $m['email'] ) === strtolower( $u->user_email ) ) { return true; }
		}
		return false;
	}
}
if ( ! function_exists( 'nadlan_ur_space_ok' ) ) {
	function nadlan_ur_space_ok( $id ) {
		$p = get_post( $id );
		return $p && 'nadlan_renewal' === $p->post_type && 'trash' !== $p->post_status;
	}
}

/* ---------- space payload ---------- */
if ( ! function_exists( 'nadlan_ur_space_payload' ) ) {
	function nadlan_ur_space_payload( $id ) {
		$apts = json_decode( (string) get_post_meta( $id, 'renewal_apartments', true ), true );
		$apts = is_array( $apts ) ? $apts : array();
		$total = count( $apts );
		$yes = count( array_filter( $apts, function ( $a ) { return ( $a['consent_status'] ?? '' ) === 'consented'; } ) );
		return array(
			'id'        => (int) $id,
			'title'     => get_the_title( $id ),
			'address'   => (string) get_post_meta( $id, 'address', true ),
			'city'      => (string) get_post_meta( $id, 'city', true ),
			'floors'    => (int) get_post_meta( $id, 'floors', true ),
			'units_per_floor' => (int) get_post_meta( $id, 'units_per_floor', true ),
			'track'     => (string) get_post_meta( $id, 'track', true ),
			'stage'     => (int) get_post_meta( $id, 'renewal_stage', true ),
			'ladder'    => function_exists( 'nadlan_ur_ladder_labels' ) ? nadlan_ur_ladder_labels() : array(),
			'apartments' => $apts,
			'consents'  => array( 'yes' => $yes, 'total' => $total, 'pct' => $total ? round( $yes / $total * 100, 1 ) : 0 ),
			'updates'   => array_slice( (array) json_decode( (string) get_post_meta( $id, 'renewal_updates', true ), true ), 0, 30 ),
			'can_manage' => nadlan_ur_can_manage( $id ),
			'statuses'  => nadlan_ur_consent_statuses(),
			'doc_keys'  => nadlan_ur_doc_keys(),
		);
	}
}

/* ---------- REST ---------- */
add_action( 'rest_api_init', function () {
	$view_perm = function ( $req ) { return is_user_logged_in() && nadlan_ur_space_on() && nadlan_ur_space_ok( (int) $req['id'] ) && nadlan_ur_can_view( (int) $req['id'] ); };
	$mng_perm  = function ( $req ) { return is_user_logged_in() && nadlan_ur_space_on() && nadlan_ur_space_ok( (int) $req['id'] ) && nadlan_ur_can_manage( (int) $req['id'] ); };

	register_rest_route( 'nadlan/v1', '/renewal-space', array(
		'methods' => 'POST',
		'permission_callback' => function () { return is_user_logged_in() && nadlan_ur_space_on(); },
		'callback' => function ( WP_REST_Request $req ) {
			if ( nadlan_ur_rate_limited( 'space', 5, DAY_IN_SECONDS ) ) {
				return new WP_Error( 'rate_limited', 'אפשר לפתוח עד 5 חדרים ביום.', array( 'status' => 429 ) );
			}
			$city   = mb_substr( sanitize_text_field( (string) $req->get_param( 'city' ) ), 0, 60 );
			$addr   = mb_substr( sanitize_text_field( (string) $req->get_param( 'address' ) ), 0, 120 );
			$floors = max( 1, min( 40, (int) $req->get_param( 'floors' ) ) );
			$upf    = max( 1, min( 12, (int) $req->get_param( 'units_per_floor' ) ) );
			if ( '' === $addr || '' === $city ) { return new WP_Error( 'bad_request', 'נדרשות עיר וכתובת.', array( 'status' => 400 ) ); }
			$id = wp_insert_post( array(
				'post_type' => 'nadlan_renewal', 'post_status' => 'private',
				'post_title' => $addr . ', ' . $city,
			), true );
			if ( is_wp_error( $id ) ) { return $id; }
			// seed the consent grid: every apartment starts unreached
			$dirs = array( 'west', 'south', 'east', 'north' );
			$apts = array();
			for ( $f = 1; $f <= $floors; $f++ ) {
				for ( $p = 0; $p < $upf; $p++ ) {
					$apts[] = array( 'id' => 'f' . $f . '-' . ( $p + 1 ), 'floor' => $f, 'pos' => $p,
						'dir' => $dirs[ $p % 4 ], 'label' => 'דירה ' . ( ( $f - 1 ) * $upf + $p + 1 ),
						'consent_status' => 'unreached', 'docs' => array(), 'contact_note' => '', 'note' => '' );
				}
			}
			update_post_meta( $id, 'owner_user_id', get_current_user_id() );
			update_post_meta( $id, 'address', $addr );
			update_post_meta( $id, 'city', $city );
			update_post_meta( $id, 'floors', $floors );
			update_post_meta( $id, 'units_per_floor', $upf );
			update_post_meta( $id, 'track', sanitize_key( (string) $req->get_param( 'track' ) ) );
			update_post_meta( $id, 'renewal_stage', 0 );
			update_post_meta( $id, 'renewal_apartments', wp_slash( wp_json_encode( nadlan_ur_clean_apartments( $apts ), JSON_UNESCAPED_UNICODE ) ) );
			update_post_meta( $id, 'member_emails', wp_slash( wp_json_encode( array(), JSON_UNESCAPED_UNICODE ) ) );
			update_post_meta( $id, 'invite_token', wp_generate_password( 24, false, false ) );
			return array( 'id' => (int) $id, 'url' => home_url( '/my-renewal/?space=' . (int) $id ) );
		},
	) );

	register_rest_route( 'nadlan/v1', '/renewal-space/(?P<id>\d+)', array(
		'methods' => 'GET', 'permission_callback' => $view_perm,
		'callback' => function ( $req ) { return nadlan_ur_space_payload( (int) $req['id'] ); },
	) );

	register_rest_route( 'nadlan/v1', '/renewal-space/(?P<id>\d+)/apartments', array(
		'methods' => 'POST', 'permission_callback' => $mng_perm,
		'callback' => function ( WP_REST_Request $req ) {
			$id = (int) $req['id'];
			$clean = nadlan_ur_clean_apartments( (array) $req->get_param( 'apartments' ) );
			update_post_meta( $id, 'renewal_apartments', wp_slash( wp_json_encode( $clean, JSON_UNESCAPED_UNICODE ) ) );
			return nadlan_ur_space_payload( $id );
		},
	) );

	register_rest_route( 'nadlan/v1', '/renewal-space/(?P<id>\d+)/stage', array(
		'methods' => 'POST', 'permission_callback' => $mng_perm,
		'callback' => function ( WP_REST_Request $req ) {
			$id = (int) $req['id'];
			$st = max( 0, min( 9, (int) $req->get_param( 'stage' ) ) );
			update_post_meta( $id, 'renewal_stage', $st );
			$log = (array) json_decode( (string) get_post_meta( $id, 'renewal_stage_log', true ), true );
			$log[] = array( 'stage' => $st, 'at' => current_time( 'mysql' ), 'by' => get_current_user_id() );
			update_post_meta( $id, 'renewal_stage_log', wp_slash( wp_json_encode( array_slice( $log, -60 ), JSON_UNESCAPED_UNICODE ) ) );
			nadlan_ur_queue_notice( $id, 'הפרויקט התקדם לשלב: ' . ( nadlan_ur_ladder_labels()[ $st ] ?? $st ) );
			return nadlan_ur_space_payload( $id );
		},
	) );

	register_rest_route( 'nadlan/v1', '/renewal-space/(?P<id>\d+)/update', array(
		'methods' => 'POST', 'permission_callback' => $mng_perm,
		'callback' => function ( WP_REST_Request $req ) {
			$id = (int) $req['id'];
			$text = mb_substr( sanitize_textarea_field( (string) $req->get_param( 'text' ) ), 0, 1000 );
			if ( '' === $text ) { return new WP_Error( 'bad_request', 'עדכון ריק.', array( 'status' => 400 ) ); }
			$ups = (array) json_decode( (string) get_post_meta( $id, 'renewal_updates', true ), true );
			array_unshift( $ups, array( 'text' => $text, 'at' => current_time( 'mysql' ), 'by' => get_current_user_id() ) );
			update_post_meta( $id, 'renewal_updates', wp_slash( wp_json_encode( array_slice( $ups, 0, 200 ), JSON_UNESCAPED_UNICODE ) ) );
			nadlan_ur_queue_notice( $id, $text );
			return nadlan_ur_space_payload( $id );
		},
	) );

	register_rest_route( 'nadlan/v1', '/renewal-space/(?P<id>\d+)/invite', array(
		'methods' => 'POST', 'permission_callback' => $mng_perm,
		'callback' => function ( $req ) {
			$id = (int) $req['id'];
			$tok = wp_generate_password( 24, false, false );
			update_post_meta( $id, 'invite_token', $tok );
			return array( 'join_url' => home_url( '/my-renewal/?join=' . rawurlencode( $tok ) ) );
		},
	) );

	register_rest_route( 'nadlan/v1', '/renewal-join/(?P<token>[A-Za-z0-9]{24})', array(
		'methods' => 'POST',
		'permission_callback' => function () { return is_user_logged_in() && nadlan_ur_space_on(); },
		'callback' => function ( $req ) {
			$tok = (string) $req['token'];
			$q = get_posts( array( 'post_type' => 'nadlan_renewal', 'post_status' => 'any', 'posts_per_page' => 1, 'fields' => 'ids',
				'meta_query' => array( array( 'key' => 'invite_token', 'value' => $tok ) ) ) );
			if ( ! $q ) { return new WP_Error( 'bad_token', 'קישור ההזמנה אינו תקף.', array( 'status' => 404 ) ); }
			$id = (int) $q[0];
			$u = wp_get_current_user();
			$members = nadlan_ur_members( $id );
			foreach ( $members as $m ) { if ( strtolower( $m['email'] ?? '' ) === strtolower( $u->user_email ) ) { return array( 'id' => $id, 'joined' => true ); } }
			$members[] = array( 'email' => $u->user_email, 'joined' => current_time( 'mysql' ) );
			update_post_meta( $id, 'member_emails', wp_slash( wp_json_encode( array_slice( $members, 0, 400 ), JSON_UNESCAPED_UNICODE ) ) );
			return array( 'id' => $id, 'joined' => true );
		},
	) );

	register_rest_route( 'nadlan/v1', '/renewal-notify-queue', array(
		'methods' => 'GET',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function () {
			return array( 'enabled' => get_option( 'nadlan_renewal_notify_enabled', '0' ) === '1',
				'log' => (array) get_option( 'nadlan_ur_notify_log', array() ) );
		},
	) );
} );

/* ---------- member notices (deliverability-last: OFF until flipped) ---------- */
if ( ! function_exists( 'nadlan_ur_queue_notice' ) ) {
	function nadlan_ur_queue_notice( $space_id, $text ) {
		$members = nadlan_ur_members( $space_id );
		$entry = array( 'space' => (int) $space_id, 'text' => mb_substr( $text, 0, 200 ),
			'recipients' => count( $members ), 'at' => current_time( 'mysql' ), 'sent' => false );
		if ( get_option( 'nadlan_renewal_notify_enabled', '0' ) === '1' && $members ) {
			$subject = 'עדכון מחדר ההתחדשות: ' . get_the_title( $space_id );
			$body = '<div dir="rtl" style="font-family:Heebo,Arial,sans-serif;max-width:540px;margin:0 auto">' .
				'<p style="color:#1B1A17;line-height:1.7">' . esc_html( $text ) . '</p>' .
				'<p><a href="' . esc_url( home_url( '/my-renewal/?space=' . (int) $space_id ) ) . '" style="display:inline-block;background:#9C7A3C;color:#FAF7F1;font-weight:700;border-radius:10px;padding:12px 18px;text-decoration:none">לחדר הפרויקט</a></p>' .
				'<p style="font-size:11.5px;color:#6D665C">קיבלתם עדכון זה כחברים בחדר ההתחדשות של הבניין באתר nad-lan.co.il.</p></div>';
			foreach ( $members as $m ) {
				if ( ! empty( $m['email'] ) && is_email( $m['email'] ) ) {
					wp_mail( $m['email'], $subject, $body, array( 'Content-Type: text/html; charset=UTF-8' ) );
				}
			}
			$entry['sent'] = true;
		}
		$q = (array) get_option( 'nadlan_ur_notify_log', array() );
		array_unshift( $q, $entry );
		update_option( 'nadlan_ur_notify_log', array_slice( $q, 0, 40 ), false );
	}
}

/* ---------- /my-renewal/ dashboard ---------- */
add_action( 'init', function () {
	add_rewrite_rule( '^my-renewal/?$', 'index.php?nadlan_my_renewal=1', 'top' );
	if ( get_option( 'nadlan_my_renewal_rewrite_v1' ) !== '1' ) {
		flush_rewrite_rules( false );
		update_option( 'nadlan_my_renewal_rewrite_v1', '1' );
	}
} );
add_filter( 'query_vars', function ( $v ) { $v[] = 'nadlan_my_renewal'; return $v; } );

add_action( 'template_redirect', function () {
	if ( ! get_query_var( 'nadlan_my_renewal' ) ) { return; }
	if ( ! nadlan_ur_space_on() ) { wp_safe_redirect( home_url( '/urban-renewal/' ) ); exit; }
	if ( ! is_user_logged_in() ) { wp_safe_redirect( wp_login_url( home_url( '/my-renewal/' ) ) ); exit; }

	// join flow
	$join = isset( $_GET['join'] ) ? sanitize_text_field( wp_unslash( $_GET['join'] ) ) : '';
	if ( $join && preg_match( '/^[A-Za-z0-9]{24}$/', $join ) ) {
		$q = get_posts( array( 'post_type' => 'nadlan_renewal', 'post_status' => 'any', 'posts_per_page' => 1, 'fields' => 'ids',
			'meta_query' => array( array( 'key' => 'invite_token', 'value' => $join ) ) ) );
		if ( $q ) {
			$id = (int) $q[0]; $u = wp_get_current_user();
			$members = nadlan_ur_members( $id ); $have = false;
			foreach ( $members as $m ) { if ( strtolower( $m['email'] ?? '' ) === strtolower( $u->user_email ) ) { $have = true; break; } }
			if ( ! $have ) {
				$members[] = array( 'email' => $u->user_email, 'joined' => current_time( 'mysql' ) );
				update_post_meta( $id, 'member_emails', wp_slash( wp_json_encode( array_slice( $members, 0, 400 ), JSON_UNESCAPED_UNICODE ) ) );
			}
			wp_safe_redirect( home_url( '/my-renewal/?space=' . $id ) ); exit;
		}
	}
	nadlan_ur_render_dashboard();
	exit;
} );

if ( ! function_exists( 'nadlan_ur_render_dashboard' ) ) {
	function nadlan_ur_render_dashboard() {
		$uid = get_current_user_id();
		$u = wp_get_current_user();
		// owned + member spaces
		$owned = get_posts( array( 'post_type' => 'nadlan_renewal', 'post_status' => 'any', 'posts_per_page' => 20, 'fields' => 'ids',
			'meta_query' => array( array( 'key' => 'owner_user_id', 'value' => $uid ) ) ) );
		$member = get_posts( array( 'post_type' => 'nadlan_renewal', 'post_status' => 'any', 'posts_per_page' => 40, 'fields' => 'ids',
			'meta_query' => array( array( 'key' => 'member_emails', 'value' => $u->user_email, 'compare' => 'LIKE' ) ) ) );
		$spaces = array_values( array_unique( array_merge( $owned, $member ) ) );
		$sel = isset( $_GET['space'] ) ? (int) $_GET['space'] : 0;
		if ( $sel && ( ! nadlan_ur_space_ok( $sel ) || ! nadlan_ur_can_view( $sel ) ) ) { $sel = 0; }
		if ( ! $sel && $spaces ) { $sel = (int) $spaces[0]; }
		$glb = esc_url( function_exists( 'nadlan_showroom_engine_base_url' ) ? nadlan_showroom_engine_base_url() . 'models/standard-residential.glb' : '' );
		$nonce = wp_create_nonce( 'wp_rest' );
		nocache_headers();
		header( 'X-Robots-Tag: noindex, nofollow' );
		get_header();
		?>
<div class="nlurd" dir="rtl" id="nlurd" data-rest="<?php echo esc_url( rest_url( 'nadlan/v1' ) ); ?>" data-nonce="<?php echo esc_attr( $nonce ); ?>" data-space="<?php echo (int) $sel; ?>" data-glb="<?php echo $glb; // phpcs:ignore ?>">
	<header class="nlurd-head">
		<h1>חדר ההתחדשות שלי</h1>
		<p>ניהול פנימי לבניין: הסכמות על המודל, שלבים, מסמכים ועדכונים. העמוד פרטי לחברי הבניין בלבד ואינו מופיע בחיפוש.</p>
	</header>
	<?php if ( ! $spaces ) : ?>
	<section class="nlurd-new">
		<h2>פתיחת חדר לבניין</h2>
		<div class="nlurd-f">
			<label>עיר<input type="text" id="nlurd-city"></label>
			<label>רחוב ומספר<input type="text" id="nlurd-addr"></label>
			<label>קומות<input type="number" id="nlurd-floors" min="1" max="40" value="4"></label>
			<label>דירות בקומה<input type="number" id="nlurd-upf" min="1" max="12" value="3"></label>
		</div>
		<button type="button" id="nlurd-create">פתיחת חדר</button>
		<div id="nlurd-createmsg" aria-live="polite"></div>
	</section>
	<?php else : ?>
	<nav class="nlurd-spaces">
		<?php foreach ( $spaces as $sid ) : ?>
		<a href="<?php echo esc_url( home_url( '/my-renewal/?space=' . (int) $sid ) ); ?>" class="<?php echo $sid === $sel ? 'is-on' : ''; ?>"><?php echo esc_html( get_the_title( $sid ) ); ?></a>
		<?php endforeach; ?>
	</nav>
	<main id="nlurd-app" data-loading="1">טוען את חדר הפרויקט...</main>
	<?php endif; ?>
</div>
<style>
.nlurd{max-width:1080px;margin:0 auto;padding:24px 16px 60px;font-family:Heebo,sans-serif;color:#1B1A17}
.nlurd-head h1{font-family:"Frank Ruhl Libre",Georgia,serif;margin:0 0 4px}
.nlurd-head p{color:#6D665C;font-size:13.5px;margin:0 0 18px}
.nlurd-new,.nlurd-card{background:#fff;border:1px solid #E2DCD0;border-radius:16px;padding:20px;margin-bottom:14px}
.nlurd-f{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:10px;margin:10px 0}
.nlurd-f label{display:flex;flex-direction:column;gap:5px;font:600 12.5px Heebo}
.nlurd-f input,.nlurd textarea,.nlurd select{border:1px solid #E2DCD0;border-radius:10px;padding:11px;font:400 14.5px Heebo;background:#FAF7F1}
#nlurd-create,.nlurd-btn{background:#C2563A;color:#FAF7F1;border:0;border-radius:10px;padding:12px 20px;font:700 14px Heebo;cursor:pointer}
.nlurd-spaces{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px}
.nlurd-spaces a{border:1px solid #E2DCD0;border-radius:999px;padding:9px 15px;font:600 13px Heebo;color:#51483A;text-decoration:none;background:#fff}
.nlurd-spaces a.is-on{background:#1B1A17;color:#FAF7F1;border-color:#1B1A17}
.nlurd-grid{display:grid;grid-template-columns:1.2fr .8fr;gap:14px}
@media(max-width:900px){.nlurd-grid{grid-template-columns:1fr}}
.nlurd-3d{position:relative;height:460px;border-radius:16px;overflow:hidden;background:#14130F}
.nlurd-3d model-viewer{width:100%;height:100%;direction:ltr;background:transparent}
.nlur-apt{width:30px;height:30px;border-radius:50%;border:2px solid #fff;color:#fff;font:700 10.5px Heebo;cursor:pointer;background:#A79E8D}
.nlur-apt:not([data-visible]){opacity:0;pointer-events:none}
.nlurd-legend{display:flex;gap:10px;flex-wrap:wrap;margin-top:10px;font:600 12px Heebo;color:#51483A}
.nlurd-legend i{display:inline-block;width:11px;height:11px;border-radius:50%;margin-inline-end:4px;vertical-align:-1px}
.nlurd-gauge{font-family:"Frank Ruhl Libre",serif;font-size:1.5rem;margin:8px 0}
.nlurd-ladder{display:flex;gap:4px;overflow-x:auto;margin:10px 0}
.nlurd-ladder span{flex:1;min-width:76px;text-align:center;font:600 10.5px/1.3 Heebo;color:#8E877A;background:#F3EEE3;border-radius:8px;padding:8px 4px;cursor:default}
.nlurd-ladder span.is-done{background:#E7E0CE;color:#6b5a33}
.nlurd-ladder span.is-now{background:#C2563A;color:#FAF7F1}
.nlurd-panel{border-top:1px solid #F3EEE3;margin-top:12px;padding-top:12px}
.nlurd-panel h4{font-family:"Frank Ruhl Libre",serif;margin:0 0 8px}
.nlurd-docrow{display:flex;align-items:center;gap:8px;font:400 13.5px Heebo;margin:4px 0}
.nlurd-meter{height:8px;background:#F3EEE3;border-radius:999px;overflow:hidden;margin:8px 0}
.nlurd-meter i{display:block;height:100%;background:#517048}
.nlurd-updates li{font:400 13.5px/1.6 Heebo;border-bottom:1px solid #F3EEE3;padding:8px 0;list-style:none}
.nlurd-updates time{color:#8E877A;font-size:11.5px;display:block}
.nlurd-invite input{width:100%;direction:ltr;text-align:left}
.nlurd-note{font:400 12px/1.6 Heebo;color:#8E877A}
</style>
<script id="nlurd-js">
(function(){
	var root=document.getElementById("nlurd"),rest=root.dataset.rest,nonce=root.dataset.nonce,glb=root.dataset.glb;
	function api(path,opts){opts=opts||{};opts.headers=Object.assign({"Content-Type":"application/json","X-WP-Nonce":nonce},opts.headers||{});return fetch(rest+path,opts).then(function(r){return r.json().then(function(j){if(!r.ok)throw j;return j})})}
	var create=document.getElementById("nlurd-create");
	if(create){create.addEventListener("click",function(){
		var m=document.getElementById("nlurd-createmsg");m.textContent="פותחים חדר...";
		api("/renewal-space",{method:"POST",body:JSON.stringify({city:document.getElementById("nlurd-city").value,address:document.getElementById("nlurd-addr").value,floors:document.getElementById("nlurd-floors").value,units_per_floor:document.getElementById("nlurd-upf").value})})
		.then(function(d){location.href=d.url}).catch(function(e){m.textContent=(e&&e.message)||"שגיאה"});
	});return}
	var app=document.getElementById("nlurd-app"),spaceId=root.dataset.space,S=null,sel=null;
	function esc(s){return String(s==null?"":s).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}
	function load(){api("/renewal-space/"+spaceId).then(function(d){S=d;render()}).catch(function(){app.textContent="אין לכם גישה לחדר הזה."})}
	function fmt(){return S.consents.yes+" מתוך "+S.consents.total+" ("+S.consents.pct+"%)"}
	function render(){
		var h='<div class="nlurd-grid"><div class="nlurd-card"><div class="nlurd-gauge">חתמו: '+fmt()+'</div><div class="nlurd-3d" id="nlurd-3dhost"></div><div class="nlurd-legend">';
		Object.keys(S.statuses).forEach(function(k){h+='<span><i style="background:'+S.statuses[k][1]+'"></i>'+esc(S.statuses[k][0])+'</span>'});
		h+='</div><div class="nlurd-panel" id="nlurd-apt"><p class="nlurd-note">הקישו על דירה במודל לפרטים ולעדכון.</p></div></div>';
		h+='<div><div class="nlurd-card"><h4>השלב בתהליך</h4><div class="nlurd-ladder">';
		S.ladder.forEach(function(l,i){h+='<span class="'+(i<S.stage?"is-done":i===S.stage?"is-now":"")+'"'+(S.can_manage?' data-st="'+i+'" style="cursor:pointer"':'')+'>'+esc(l)+'</span>'});
		h+='</div><p class="nlurd-note">השלב כפי שעודכן על ידי נציגות הבניין.</p></div>';
		h+='<div class="nlurd-card"><h4>עדכונים לשכנים</h4>'+(S.can_manage?'<textarea id="nlurd-uptext" rows="2" placeholder="מה חדש בפרויקט?"></textarea><button class="nlurd-btn" id="nlurd-upsend" style="margin-top:8px">פרסום עדכון</button>':'')+'<ul class="nlurd-updates">';
		(S.updates||[]).forEach(function(u){h+='<li>'+esc(u.text)+'<time>'+esc(u.at)+'</time></li>'});
		h+='</ul></div>';
		if(S.can_manage){h+='<div class="nlurd-card nlurd-invite"><h4>הזמנת שכנים</h4><p class="nlurd-note">כל מי שנכנס עם הקישור מצטרף לחדר (קריאה בלבד).</p><button class="nlurd-btn" id="nlurd-invbtn">יצירת קישור הזמנה</button><input type="text" id="nlurd-invurl" readonly style="margin-top:8px" hidden></div>'}
		h+='</div></div>';
		app.innerHTML=h;app.removeAttribute("data-loading");
		boot3d();wire();
	}
	function wire(){
		app.querySelectorAll("[data-st]").forEach(function(el){el.addEventListener("click",function(){
			api("/renewal-space/"+spaceId+"/stage",{method:"POST",body:JSON.stringify({stage:el.dataset.st})}).then(function(d){S=d;render()});
		})});
		var us=document.getElementById("nlurd-upsend");
		if(us)us.addEventListener("click",function(){
			var t=document.getElementById("nlurd-uptext").value;if(!t)return;
			api("/renewal-space/"+spaceId+"/update",{method:"POST",body:JSON.stringify({text:t})}).then(function(d){S=d;render()});
		});
		var inv=document.getElementById("nlurd-invbtn");
		if(inv)inv.addEventListener("click",function(){
			api("/renewal-space/"+spaceId+"/invite",{method:"POST"}).then(function(d){var i=document.getElementById("nlurd-invurl");i.hidden=false;i.value=d.join_url;i.select();try{navigator.clipboard.writeText(d.join_url)}catch(e){}});
		});
	}
	var FH=3.05,HALF=13.2,DIRV={west:[-1,0],east:[1,0],north:[0,1],south:[0,-1]};
	function aptPos(a){
		var v=DIRV[a.dir]||[-1,0];
		var off=(a.pos%3-1)*7; // spread along the facade
		var x=v[0]*HALF+(v[1]!==0?off:0),z=v[1]*HALF+(v[0]!==0?off:0);
		return x.toFixed(2)+"m "+(a.floor*FH+FH*0.4).toFixed(2)+"m "+z.toFixed(2)+"m";
	}
	function boot3d(){
		var host=document.getElementById("nlurd-3dhost");if(!host||!glb)return;
		var build=function(){
			var mv=document.createElement("model-viewer");
			mv.setAttribute("src",glb);mv.setAttribute("camera-controls","");mv.setAttribute("interaction-prompt","none");
			mv.setAttribute("environment-image","neutral");mv.setAttribute("exposure","0.95");mv.setAttribute("shadow-intensity","0.5");mv.setAttribute("touch-action","pan-y");
			(S.apartments||[]).forEach(function(a){
				var b=document.createElement("button");
				b.setAttribute("slot","hotspot-"+a.id);
				b.setAttribute("data-position",aptPos(a));
				var v=DIRV[a.dir]||[-1,0];
				b.setAttribute("data-normal",v[0]+" 0 "+v[1]);
				b.setAttribute("data-visibility-attribute","visible");
				b.className="nlur-apt";b.style.background=(S.statuses[a.consent_status]||S.statuses.unreached)[1];
				b.textContent=a.floor;b.title=a.label;
				b.addEventListener("click",function(){select(a.id)});
				mv.appendChild(b);
			});
			host.innerHTML="";host.appendChild(mv);
		};
		if(window.customElements&&customElements.get("model-viewer")){build();return}
		var s=document.createElement("script");s.type="module";s.src="https://unpkg.com/@google/model-viewer@3.5.0/dist/model-viewer.min.js";s.onload=build;document.head.appendChild(s);
	}
	function select(id){
		sel=(S.apartments||[]).filter(function(a){return a.id===id})[0];if(!sel)return;
		var box=document.getElementById("nlurd-apt");
		var done=0,total=0,rows="";
		Object.keys(S.doc_keys).forEach(function(k){total++;var on=sel.docs&&sel.docs[k];if(on)done++;
			rows+='<label class="nlurd-docrow"><input type="checkbox" data-doc="'+k+'"'+(on?" checked":"")+(S.can_manage?"":" disabled")+'> '+esc(S.doc_keys[k])+'</label>'});
		var pct=total?Math.round(done/total*100):0;
		var h='<h4>'+esc(sel.label)+' · קומה '+sel.floor+'</h4>';
		if(S.can_manage){h+='<select id="nlurd-aptstatus">';Object.keys(S.statuses).forEach(function(k){h+='<option value="'+k+'"'+(k===sel.consent_status?" selected":"")+'>'+esc(S.statuses[k][0])+'</option>'});h+='</select>'}
		else{h+='<p><b>'+esc((S.statuses[sel.consent_status]||[])[0]||"")+'</b></p>'}
		h+='<div class="nlurd-meter"><i style="width:'+pct+'%"></i></div><p class="nlurd-note">מסמכים: '+done+' מתוך '+total+'</p>'+rows;
		if(S.can_manage){h+='<button class="nlurd-btn" id="nlurd-aptsave" style="margin-top:10px">שמירה</button>'}
		box.innerHTML=h;
		var save=document.getElementById("nlurd-aptsave");
		if(save)save.addEventListener("click",function(){
			sel.consent_status=document.getElementById("nlurd-aptstatus").value;
			sel.docs=sel.docs||{};
			box.querySelectorAll("[data-doc]").forEach(function(c){sel.docs[c.dataset.doc]=c.checked});
			api("/renewal-space/"+spaceId+"/apartments",{method:"POST",body:JSON.stringify({apartments:S.apartments})}).then(function(d){S=d;render()});
		});
	}
	if(spaceId&&spaceId!=="0")load();
})();
</script>
		<?php
		get_footer();
	}
}

/* healthcheck visibility */
add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	if ( isset( $out['urban_renewal'] ) && is_array( $out['urban_renewal'] ) ) {
		$out['urban_renewal']['space'] = nadlan_ur_space_on();
	}
	return $out;
} );
