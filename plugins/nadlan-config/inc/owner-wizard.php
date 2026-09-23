<?php
/**
 * nadlan-config · Owners publish on the same engine (x-owner-wizard) · v1.0.0 · 23.9.2026
 *
 * Owner order 23.9.2026: "the old wizard moves to the same engine": /post-listing/ keeps its address and its
 * one-step account, and everything after it is the broker engine (x-broker-drop):
 *   photos (up to 30, shrunk on the phone, location data removed) + a few lines in the owner's words
 *   -> the facts are read and checked (every number must be in the message; nothing is added)
 *   -> the page is written in the portal's voice and checked (no hype, no invented claims, no long dashes)
 *   -> a Latin address (/properties/florentin-4-rooms-for-sale/), published at once, WhatsApp and call to the owner
 * Before: login, then a free-text "AI" form, a pending listing that waited for an editor, a Hebrew address, 12 photos.
 * The one hold left: a message that trips the fair-housing check (nadlan_compliance_scan) waits for a person.
 * "My listings" on the same page: sold or let in one tap, a new price in two (reg. 19(c) spirit for owners too).
 * Brokers who reach this page are sent to their own free site (/brokers/#join) instead.
 *
 * Needs x-broker-drop 1.1. Installed as the persistent Code Snippet "x-owner-wizard" by
 * scripts/broker-drop/deploydrop.py. Rollback: deactivate the snippet; the plugin's own wizard returns as it was.
 */

if ( ! defined( 'ABSPATH' ) ) { return; }
if ( defined( 'NL_OWNER_VERSION' ) ) { return; }
define( 'NL_OWNER_VERSION', '1.0.0' );
define( 'NL_OWNER_MAX_ACTIVE', 5 );

/* The shortcode and the REST doors are taken over after the plugin registered its own (plugins load before init). */
add_action( 'init', function () {
	if ( ! function_exists( 'nl_drop_build' ) ) { return; }
	remove_shortcode( 'nadlan_listing_wizard' );
	add_shortcode( 'nadlan_listing_wizard', 'nl_owner_shortcode' );
	remove_action( 'wp_enqueue_scripts', 'nadlan_pwiz_assets' );
}, 30 );

/** The owner as the engine's publisher: a name and a phone, no licence, no site, Hebrew only. */
function nl_owner_pseudo( $uid, $name, $phone ) {
	$digits = preg_replace( '/\D+/', '', (string) $phone );
	if ( $digits !== '' && $digits[0] === '0' ) { $digits = '972' . substr( $digits, 1 ); }
	$nat  = strpos( $digits, '972' ) === 0 ? substr( $digits, 3 ) : '';
	$intl = strlen( $nat ) >= 8 ? '+972 ' . substr( $nat, 0, 2 ) . '-' . substr( $nat, 2, 3 ) . '-' . substr( $nat, 5 ) : (string) $phone;
	$name = trim( (string) $name );
	return array(
		'id' => 0, 'kind' => 'owner', 'user_id' => (int) $uid,
		'name_he' => $name, 'name_en' => $name, 'name_ru' => $name, 'brand_he' => '', 'brand_en' => '', 'license' => '',
		'phone' => (string) $phone, 'phone_intl' => $intl, 'wa' => $digits, 'female' => false,
		'site_he' => 0, 'site_en' => 0, 'site_ru' => 0, 'site_fr' => 0, 'auto' => true, 'on' => true, 'token' => '',
		'areas' => array(), 'areas_l' => array(), 'bio' => array(), 'portrait' => '', 'hero' => 0, 'tier' => 'owner', 'slug' => '',
		'langs' => array( 'he' ),
	);
}

function nl_owner_from_listing( $pid ) {
	$c = json_decode( (string) get_post_meta( $pid, 'nl_owner_contact', true ), true );
	return nl_owner_pseudo( (int) get_post_meta( $pid, 'owner_user_id', true ), $c['name'] ?? '', $c['phone'] ?? '' );
}

function nl_owner_rate( $uid, $bucket, $limit, $window ) {
	$k = 'nlowner_' . $bucket . '_' . (int) $uid;
	$n = (int) get_transient( $k );
	if ( $n >= $limit ) { return true; }
	set_transient( $k, $n + 1, $window );
	return false;
}

function nl_owner_phone( $raw ) {
	$d = preg_replace( '/\D+/', '', (string) $raw );
	if ( strpos( $d, '972' ) === 0 ) { $d = '0' . substr( $d, 3 ); }
	return preg_match( '/^05\d{8}$/', $d ) ? substr( $d, 0, 3 ) . '-' . substr( $d, 3 ) : '';
}

function nl_owner_listings( $uid, $only_ids = false ) {
	return get_posts( array(
		'post_type'        => 'nadlan_property',
		'post_status'      => array( 'publish', 'draft', 'pending' ),
		'numberposts'      => 50,
		'orderby'          => 'date',
		'order'            => 'DESC',
		'suppress_filters' => true,
		'fields'           => $only_ids ? 'ids' : 'all',
		'meta_query'       => array(
			array( 'key' => 'owner_user_id', 'value' => (int) $uid, 'type' => 'NUMERIC' ),
			array( 'key' => 'nl_owner', 'value' => '1' ),
		),
	) );
}

/* =====================================================================================================
 * REST: the owner's doors (logged in, the REST nonce), and the plugin's old doors answered honestly
 * ===================================================================================================== */
add_action( 'rest_api_init', function () {
	$in = function () { return is_user_logged_in(); };
	register_rest_route( 'nadlan/v1', '/owner/photo', array( 'methods' => 'POST', 'permission_callback' => $in, 'callback' => 'nl_owner_rest_photo' ) );
	register_rest_route( 'nadlan/v1', '/owner/submit', array( 'methods' => 'POST', 'permission_callback' => $in, 'callback' => 'nl_owner_rest_submit' ) );
	register_rest_route( 'nadlan/v1', '/owner/build/(?P<drop>\d+)', array( 'methods' => 'POST', 'permission_callback' => $in, 'callback' => 'nl_owner_rest_build' ) );
	register_rest_route( 'nadlan/v1', '/owner/listings', array( 'methods' => 'GET', 'permission_callback' => $in, 'callback' => 'nl_owner_rest_listings' ) );
	register_rest_route( 'nadlan/v1', '/owner/update', array( 'methods' => 'POST', 'permission_callback' => $in, 'callback' => 'nl_owner_rest_update' ) );
	// the first wizard's doors: a page opened before this change gets a clear answer instead of a pending listing
	$gone = function () { return new WP_Error( 'nl_owner_moved', 'הטופס עודכן. מרעננים את העמוד ושולחים שוב.', array( 'status' => 410 ) ); };
	foreach ( array( '/listing-ai-draft', '/listing-submit', '/listing-photo' ) as $r ) {
		register_rest_route( 'nadlan/v1', $r, array( 'methods' => 'POST', 'permission_callback' => '__return_true', 'callback' => $gone ), true );
	}
}, 20 );

function nl_owner_rest_photo( WP_REST_Request $req ) {
	$uid = get_current_user_id();
	if ( nl_owner_rate( $uid, 'photo', 90, HOUR_IN_SECONDS ) ) { return new WP_Error( 'rate', 'הרבה תמונות בשעה האחרונה. אפשר להמשיך בעוד כמה דקות.', array( 'status' => 429 ) ); }
	$files = $req->get_file_params();
	$f     = $files['photo'] ?? null;
	if ( ! is_array( $f ) || empty( $f['tmp_name'] ) ) { return new WP_Error( 'nofile', 'לא התקבל קובץ.', array( 'status' => 400 ) ); }
	if ( (int) $f['size'] > NL_DROP_MAX_BYTES ) { return new WP_Error( 'big', 'התמונה גדולה מ-15MB.', array( 'status' => 400 ) ); }
	$mimes = array( 'jpg|jpeg|jpe' => 'image/jpeg', 'png' => 'image/png', 'webp' => 'image/webp', 'heic' => 'image/heic', 'heif' => 'image/heif' );
	$check = wp_check_filetype_and_ext( $f['tmp_name'], $f['name'], $mimes );
	if ( empty( $check['type'] ) || strpos( (string) $check['type'], 'image/' ) !== 0 ) { return new WP_Error( 'type', 'אפשר להעלות תמונות בלבד.', array( 'status' => 400 ) ); }
	require_once ABSPATH . 'wp-admin/includes/file.php';
	require_once ABSPATH . 'wp-admin/includes/image.php';
	require_once ABSPATH . 'wp-admin/includes/media.php';
	$f['name'] = 'nadlan-owner-' . $uid . '-' . gmdate( 'Ymd-His' ) . '-' . wp_rand( 100, 999 ) . '.' . ( $check['ext'] ?: 'jpg' );
	$moved     = wp_handle_upload( $f, array( 'test_form' => false, 'mimes' => $mimes ) );
	if ( isset( $moved['error'] ) ) { return new WP_Error( 'upload', 'ההעלאה נכשלה. אפשר לנסות שוב.', array( 'status' => 500 ) ); }
	nl_drop_strip_gps( $moved['file'], $moved['type'] );
	$att = wp_insert_attachment( array( 'post_mime_type' => $moved['type'], 'post_title' => 'nadlan-owner-' . $uid, 'post_status' => 'inherit', 'post_author' => $uid ), $moved['file'] );
	if ( is_wp_error( $att ) || ! $att ) { return new WP_Error( 'insert', 'ההעלאה נכשלה.', array( 'status' => 500 ) ); }
	wp_update_attachment_metadata( $att, wp_generate_attachment_metadata( $att, $moved['file'] ) );
	update_post_meta( $att, 'nl_owner_user', (string) $uid );
	$m = wp_get_attachment_metadata( $att );
	return array( 'id' => (int) $att, 'url' => (string) wp_get_attachment_url( $att ), 'w' => (int) ( $m['width'] ?? 0 ), 'h' => (int) ( $m['height'] ?? 0 ) );
}

function nl_owner_rest_submit( WP_REST_Request $req ) {
	$uid = get_current_user_id();
	if ( (string) $req->get_param( 'who' ) === 'broker' ) {
		return array( 'state' => 'broker', 'url' => home_url( '/brokers/#join' ) );
	}
	if ( nl_owner_rate( $uid, 'submit', 8, DAY_IN_SECONDS ) ) { return new WP_Error( 'rate', 'הגעתם למכסת הפרסומים להיום.', array( 'status' => 429 ) ); }
	$active = 0;
	foreach ( nl_owner_listings( $uid ) as $p ) {
		if ( $p->post_status === 'publish' && (string) get_post_meta( $p->ID, 'nl_status', true ) === 'active' ) { $active++; }
	}
	if ( $active >= NL_OWNER_MAX_ACTIVE ) {
		return new WP_Error( 'cap', 'יש לכם כבר ' . NL_OWNER_MAX_ACTIVE . ' נכסים פעילים. נכס שנמכר או הושכר מסמנים ב"המודעות שלי", והמקום מתפנה.', array( 'status' => 429 ) );
	}
	$name  = trim( sanitize_text_field( wp_unslash( (string) $req->get_param( 'name' ) ) ) );
	$name  = function_exists( 'mb_substr' ) ? mb_substr( $name, 0, 30 ) : substr( $name, 0, 30 );
	$phone = nl_owner_phone( $req->get_param( 'phone' ) );
	if ( $name === '' || preg_match( '/https?:|www\.|@|\d/u', $name ) ) { return new WP_Error( 'name', 'כותבים שם פרטי, כפי שיופיע בעמוד.', array( 'status' => 400, 'field' => 'name' ) ); }
	if ( $phone === '' ) { return new WP_Error( 'phone', 'צריך מספר נייד ישראלי, לדוגמה 052-3631582.', array( 'status' => 400, 'field' => 'phone' ) ); }
	if ( (string) $req->get_param( 'consent' ) !== '1' || (string) $req->get_param( 'owner' ) !== '1' ) {
		return new WP_Error( 'consent', 'צריך לסמן את שתי ההצהרות.', array( 'status' => 400, 'field' => 'consent' ) );
	}
	$text = trim( sanitize_textarea_field( (string) $req->get_param( 'text' ) ) );
	$text = function_exists( 'mb_substr' ) ? mb_substr( $text, 0, 4000 ) : substr( $text, 0, 4000 );
	$ids  = array();
	foreach ( (array) $req->get_param( 'photos' ) as $id ) {
		$id = (int) $id;
		if ( $id && get_post_type( $id ) === 'attachment' && (string) get_post_meta( $id, 'nl_owner_user', true ) === (string) $uid && ! in_array( $id, $ids, true ) ) { $ids[] = $id; }
		if ( count( $ids ) >= NL_DROP_MAX_PHOTOS ) { break; }
	}
	if ( ( function_exists( 'mb_strlen' ) ? mb_strlen( $text ) : strlen( $text ) ) < 8 ) {
		return array( 'state' => 'held', 'missing' => array( 'כמה שורות על הנכס' ) );
	}
	update_user_meta( $uid, 'nl_owner_phone', $phone );
	update_user_meta( $uid, 'nl_owner_name', $name );
	@set_time_limit( 170 );
	$drop_id = wp_insert_post( array(
		'post_type'    => 'nadlan_drop',
		'post_status'  => 'private',
		'post_title'   => 'בעלי נכס · ' . $name . ' · ' . wp_date( 'j.n.Y H:i' ),
		'post_content' => $text,
		'post_author'  => nl_drop_author(),
	), true );
	if ( is_wp_error( $drop_id ) ) { return new WP_Error( 'save', 'השמירה נכשלה. אפשר לנסות שוב.', array( 'status' => 500 ) ); }
	update_post_meta( $drop_id, 'nl_owner_user', (string) $uid );
	update_post_meta( $drop_id, 'nl_owner_contact', wp_slash( wp_json_encode( array( 'name' => $name, 'phone' => $phone ), JSON_UNESCAPED_UNICODE ) ) );
	update_post_meta( $drop_id, 'nl_text', wp_slash( $text ) );
	update_post_meta( $drop_id, 'nl_photos', $ids );
	update_post_meta( $drop_id, 'nl_door', 'wizard' );
	update_post_meta( $drop_id, 'nl_state', 'reading' );
	$hits = function_exists( 'nadlan_compliance_scan' ) ? nadlan_compliance_scan( $text ) : array();
	if ( $hits ) { update_post_meta( $drop_id, 'nl_hold', wp_slash( wp_json_encode( $hits, JSON_UNESCAPED_UNICODE ) ) ); }
	$err = null;
	$b   = nl_owner_pseudo( $uid, $name, $phone );
	$f   = nl_drop_extract( $text, $b, $err );
	nl_drop_usage_save( $drop_id );
	update_post_meta( $drop_id, 'nl_facts', wp_slash( wp_json_encode( $f, JSON_UNESCAPED_UNICODE ) ) );
	if ( $err ) { update_post_meta( $drop_id, 'nl_ai', 'fallback:' . $err ); }
	$miss = nl_drop_missing( $f, $ids );
	if ( $miss ) {
		update_post_meta( $drop_id, 'nl_state', 'held' );
		update_post_meta( $drop_id, 'nl_missing', $miss );
		return array( 'state' => 'held', 'drop' => (int) $drop_id, 'missing' => $miss, 'summary' => nl_drop_summary( $f ) );
	}
	update_post_meta( $drop_id, 'nl_state', 'ready' );
	return array( 'state' => 'ready', 'drop' => (int) $drop_id, 'summary' => nl_drop_summary( $f ) );
}

function nl_owner_rest_build( WP_REST_Request $req ) {
	$uid  = get_current_user_id();
	$drop = (int) $req['drop'];
	if ( get_post_type( $drop ) !== 'nadlan_drop' || (string) get_post_meta( $drop, 'nl_owner_user', true ) !== (string) $uid ) {
		return new WP_Error( 'nf', 'לא נמצא.', array( 'status' => 404 ) );
	}
	$state = (string) get_post_meta( $drop, 'nl_state', true );
	if ( ! in_array( $state, array( 'ready', 'writing', 'published', 'draft', 'pending' ), true ) ) { return new WP_Error( 'state', 'חסרים פרטים.', array( 'status' => 409 ) ); }
	$c    = json_decode( (string) get_post_meta( $drop, 'nl_owner_contact', true ), true );
	$b    = nl_owner_pseudo( $uid, $c['name'] ?? '', $c['phone'] ?? '' );
	$hold = (string) get_post_meta( $drop, 'nl_hold', true ) !== '';
	if ( $hold ) { $b['auto'] = false; }
	if ( (string) $req->get_param( 'test' ) === '1' && current_user_can( 'manage_options' ) ) { $b['auto'] = false; }   // the owner's own test runs stay drafts
	@set_time_limit( 170 );
	$res = nl_drop_build( $drop, $b );
	if ( is_wp_error( $res ) ) { return new WP_Error( 'build', 'בניית העמוד נכשלה. אפשר לנסות שוב.', array( 'status' => 500 ) ); }
	if ( $hold && ! empty( $res['he_id'] ) && get_post_status( $res['he_id'] ) !== 'publish' ) {
		wp_update_post( array( 'ID' => (int) $res['he_id'], 'post_status' => 'pending' ) );
		$res['state'] = 'pending';
		update_post_meta( $drop, 'nl_state', 'pending' );
		@wp_mail( get_option( 'admin_email' ), '[nad-lan] מודעת בעלים ממתינה לבדיקה', 'הטקסט נעצר בבדיקת הפליה בדיור: ' . admin_url( 'post.php?post=' . (int) $res['he_id'] . '&action=edit' ) );
	}
	return $res;
}

function nl_owner_rest_listings( WP_REST_Request $req ) {
	$uid  = get_current_user_id();
	$rows = array();
	foreach ( nl_owner_listings( $uid ) as $p ) {
		$st    = (string) get_post_meta( $p->ID, 'nl_status', true );
		$deal  = (string) get_post_meta( $p->ID, 'listing_type', true ) === 'rent' ? 'rent' : 'sale';
		$price = (int) get_post_meta( $p->ID, 'price', true );
		$rows[] = array(
			'id'       => (int) $p->ID,
			'title'    => html_entity_decode( get_the_title( $p ), ENT_QUOTES, 'UTF-8' ),
			'url'      => (string) get_permalink( $p ),
			'cover'    => (string) get_the_post_thumbnail_url( $p->ID, 'medium' ),
			'deal'     => $deal,
			'status'   => in_array( $st, array( 'sold', 'rented' ), true ) ? $st : 'active',
			'price'    => $price ? nl_drop_price_text( $price, 'he' ) . ( $deal === 'rent' ? ' לחודש' : '' ) : '',
			'editable' => true,
			'live'     => $p->post_status === 'publish',
			'pending'  => $p->post_status === 'pending',
		);
	}
	return array( 'listings' => $rows );
}

function nl_owner_rest_update( WP_REST_Request $req ) {
	$uid = get_current_user_id();
	if ( nl_owner_rate( $uid, 'update', 60, HOUR_IN_SECONDS ) ) { return new WP_Error( 'rate', 'יותר מדי עדכונים בשעה האחרונה.', array( 'status' => 429 ) ); }
	$id = (int) $req->get_param( 'id' );
	if ( get_post_type( $id ) !== 'nadlan_property' || (int) get_post_meta( $id, 'owner_user_id', true ) !== (int) $uid || (string) get_post_meta( $id, 'nl_owner', true ) !== '1' ) {
		return new WP_Error( 'nf', 'המודעה לא נמצאה.', array( 'status' => 404 ) );
	}
	return nl_drop_apply_update( $id, nl_owner_from_listing( $id ), (string) $req->get_param( 'status' ), $req->get_param( 'price' ) );
}

/* =====================================================================================================
 * The page: the account gate for visitors, the tool and "my listings" for owners
 * ===================================================================================================== */
function nl_owner_shortcode() {
	if ( ! function_exists( 'nl_drop_build' ) ) { return ''; }
	$css = '<style>' . nl_owner_css() . '</style>';
	if ( ! is_user_logged_in() ) {
		$rest = esc_url( rest_url( 'nadlan/v1/quick-register' ) );
		$back = esc_url( get_permalink() );
		$h  = '<section class="nlow nlow-gate" dir="rtl" id="nlow-gate" data-rest="' . esc_attr( $rest ) . '" data-back="' . esc_attr( $back ) . '">';
		$h .= '<h2>פותחים חשבון ומפרסמים</h2><p class="nlow-lead">שם ומייל, ואתם בפנים. בלי כרטיס אשראי ובלי לחכות למייל אימות. החשבון שומר את המודעות שלכם, כדי שתוכלו לסמן נמכר או לעדכן מחיר.</p>';
		$h .= '<div class="nlow-grid"><label>שם מלא<input type="text" id="nlowg-name" autocomplete="name"></label><label>מייל<input type="email" id="nlowg-email" autocomplete="email" inputmode="email" dir="ltr"></label></div>';
		$h .= '<input type="text" id="nlowg-web" tabindex="-1" autocomplete="off" class="nlow-trap" aria-hidden="true">';
		$h .= '<button type="button" class="nlow-btn" id="nlowg-go">פתיחת חשבון והמשך</button>';
		$h .= '<p class="nlow-hint">כבר יש לכם חשבון? <a href="' . esc_url( wp_login_url( get_permalink() ) ) . '">כניסה</a></p>';
		$h .= '<p class="nlow-err" id="nlowg-err" role="alert" hidden></p>';
		$h .= '<p class="nlow-hint">מתווכים? לכם יש אתר משלכם וקישור אישי להעלאת נכסים, בחינם: <a href="' . esc_url( home_url( '/brokers/#join' ) ) . '">לפתיחת אתר למתווך</a>.</p></section>';
		$h .= '<script>(function(){var g=document.getElementById("nlow-gate"),b=document.getElementById("nlowg-go");if(!g||!b)return;b.addEventListener("click",function(){'
			. 'var e=document.getElementById("nlowg-email").value.trim(),n=document.getElementById("nlowg-name").value.trim(),w=document.getElementById("nlowg-web").value,err=document.getElementById("nlowg-err");'
			. 'if(!/.+@.+\\..+/.test(e)){err.hidden=false;err.textContent="צריך מייל תקין כדי לפתוח חשבון.";return;}'
			. 'b.disabled=true;b.textContent="פותחים חשבון…";'
			. 'fetch(g.dataset.rest,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({name:n,email:e,phone:"",website:w,back:g.dataset.back})})'
			. '.then(function(r){return r.json().then(function(j){return{s:r.status,j:j};});})'
			. '.then(function(x){if(x.j&&x.j.ok){location.reload();return;}b.disabled=false;b.textContent="פתיחת חשבון והמשך";err.hidden=false;'
			. 'if(x.s===409){err.innerHTML="יש כבר חשבון עם המייל הזה. <a href=\""+(x.j.login_url||"/wp-login.php")+"\">כניסה</a>";}'
			. 'else if(x.s===429){err.textContent="יותר מדי ניסיונות. נסו שוב בעוד שעה או היכנסו לחשבון.";}else{err.textContent="משהו השתבש. נסו שוב.";}'
			. '}).catch(function(){b.disabled=false;b.textContent="פתיחת חשבון והמשך";err.hidden=false;err.textContent="אין חיבור. נסו שוב.";});});})();</script>';
		return $css . $h;
	}
	$u     = wp_get_current_user();
	$name  = (string) get_user_meta( $u->ID, 'nl_owner_name', true );
	if ( $name === '' ) { $name = trim( (string) preg_split( '/\s+/u', (string) $u->display_name )[0] ); }
	if ( strpos( $name, '@' ) !== false ) { $name = ''; }
	$phone = (string) get_user_meta( $u->ID, 'nl_owner_phone', true );
	if ( $phone === '' ) { $phone = (string) get_user_meta( $u->ID, 'phone', true ); }
	$cfg = array( 'api' => esc_url_raw( rest_url( 'nadlan/v1/owner' ) ), 'nonce' => wp_create_nonce( 'wp_rest' ) );
	$ex  = 'למכירה, 4 חדרים, 98 מ״ר, קומה 3 מתוך 6 עם מעלית, מרפסת 10 מ״ר, ממ״ד וחניה. פלורנטין, תל אביב. 3.4 מיליון ש״ח. כניסה בינואר.';
	$h  = '<section class="nlow" dir="rtl" aria-labelledby="nlow-h">';
	$h .= '<h2 id="nlow-h">הנכס שלכם</h2>';
	$h .= '<form id="nlow-f" novalidate>';
	$h .= '<fieldset class="nlow-who"><legend>מי מפרסם</legend><label><input type="radio" name="who" value="owner" checked> בעלי הנכס</label><label><input type="radio" name="who" value="broker"> מתווך או מתווכת</label></fieldset>';
	$h .= '<div class="nlow-pick"><input type="file" id="nlow-files" accept="image/*" multiple><label for="nlow-files" class="nlow-btn nlow-btn--ghost">בחירת תמונות</label><span class="nlow-count" id="nlow-count" aria-live="polite"></span></div>';
	$h .= '<ul class="nlow-thumbs" id="nlow-thumbs" aria-label="התמונות שנבחרו"></ul><p class="nlow-hint" id="nlow-hint1" hidden>התמונה הראשונה היא התמונה הראשית. נגיעה בתמונה אחרת הופכת אותה לראשית.</p>';
	$h .= '<label for="nlow-txt" class="nlow-lbl">פרטי הנכס</label><textarea id="nlow-txt" rows="7" placeholder="' . esc_attr( 'לדוגמה: ' . $ex ) . '"></textarea>';
	$h .= '<p class="nlow-hint">כדאי לכתוב: למכירה או להשכרה, שכונה ועיר, חדרים, מ״ר, קומה, מרפסת, חניה ומחסן, מחיר, מתי אפשר להיכנס, ומה מיוחד בנכס. מה שלא נכתב לא יופיע בעמוד. הרחוב ומספר הבית לא מתפרסמים.</p>';
	$h .= '<div class="nlow-grid"><label>שם פרטי, כפי שיופיע בעמוד<input type="text" id="nlow-name" value="' . esc_attr( $name ) . '" autocomplete="given-name" maxlength="30"></label><label>טלפון נייד<input type="tel" id="nlow-phone" value="' . esc_attr( $phone ) . '" autocomplete="tel" inputmode="tel" dir="ltr" maxlength="20"></label></div>';
	$h .= '<label class="nlow-c"><input type="checkbox" id="nlow-owner" value="1"> <span>אני בעל הנכס או מורשה מטעם הבעלים, והפרטים נכונים.</span></label>';
	$h .= '<label class="nlow-c"><input type="checkbox" id="nlow-consent" value="1"> <span>השם הפרטי והטלפון יופיעו בעמוד הנכס, בכפתורי וואטסאפ וחיוג, עד שאסמן שהנכס נמכר או הושכר.</span></label>';
	$h .= '<div class="nlow-bar"><button type="submit" class="nlow-btn" id="nlow-send">פרסום הנכס</button></div>';
	$h .= '</form><div class="nlow-status" id="nlow-status" role="status" aria-live="polite" hidden></div></section>';
	$h .= '<section class="nlow" dir="rtl" aria-labelledby="nlow-mine-h"><h2 id="nlow-mine-h">המודעות שלי</h2><p class="nlow-lead nlow-small">נכס שנמכר או הושכר מסמנים כאן בנגיעה. העמוד נשאר עם הודעה מתאימה וכפתורי הפנייה יורדים.</p><ul class="nlow-mine" id="nlow-mine"><li class="nlow-muted">טוען…</li></ul></section>';
	$h .= '<div class="nlow-sheet" id="nlow-sheet" hidden><div class="nlow-sheet-in" role="dialog" aria-modal="true" aria-labelledby="nlow-sheet-t"><p id="nlow-sheet-t"></p><div id="nlow-sheet-f"></div><div class="nlow-sheet-b"><button type="button" class="nlow-btn" id="nlow-sheet-ok">אישור</button><button type="button" class="nlow-btn nlow-btn--ghost" id="nlow-sheet-no">ביטול</button></div></div></div>';
	$h .= '<script>window.NLOWNER=' . wp_json_encode( $cfg, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . ';</script><script>' . nl_owner_js() . '</script>';
	return $css . $h;
}

function nl_owner_css() {
	return <<<'NLOCSS'
.nlow{--o-ink:#14212B;--o-ink2:#3B4753;--o-mute:#6B7680;--o-line:#E3E1DA;--o-sea:#2F6F86;--o-seah:#255C70;--o-sand:#EEE9DD;--o-surf:#FFFFFF;--o-ok:#2E7D5B;--o-warn:#9A6A12;--o-bad:#B3261E;background:var(--o-surf);border:1px solid var(--o-line);border-radius:16px;padding:clamp(20px,4vw,32px);max-width:760px;margin:24px auto;box-sizing:border-box}
.nlow h2{font-family:'Noto Serif Hebrew','Frank Ruhl Libre',Georgia,serif!important;font-weight:600;font-size:clamp(22px,2.6vw,28px);margin:0 0 10px;color:var(--o-ink)!important}
.nlow .nlow-lead{margin:0 0 16px;color:var(--o-ink2);line-height:1.65}
.nlow .nlow-small{font-size:15px}
.nlow fieldset{border:0;padding:0;margin:0 0 16px;display:flex;flex-wrap:wrap;gap:6px 20px}
.nlow legend{width:100%;font-weight:700;margin:0 0 6px;color:var(--o-ink)}
.nlow fieldset label{display:inline-flex;gap:6px;align-items:center;font-weight:500}
.nlow .nlow-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px 16px;margin:14px 0}
@media (max-width:640px){.nlow .nlow-grid{grid-template-columns:minmax(0,1fr)}}
.nlow .nlow-grid label,.nlow .nlow-lbl{display:block;font-weight:700;font-size:15px;color:var(--o-ink)}
.nlow input[type=text],.nlow input[type=tel],.nlow input[type=email],.nlow textarea{display:block;width:100%;box-sizing:border-box;min-height:48px;margin-top:6px;border:1px solid var(--o-line);border-radius:10px;padding:10px 12px;font:inherit;font-size:16px;background:#FBFAF7;color:var(--o-ink)}
.nlow textarea{min-height:150px;resize:vertical;line-height:1.55}
.nlow input:focus,.nlow textarea:focus{outline:3px solid var(--o-sea);outline-offset:1px;border-color:transparent}
.nlow .nlow-hint{margin:8px 0 0;font-size:14px;color:var(--o-mute);line-height:1.55}
.nlow .nlow-hint a{color:var(--o-sea)}
.nlow .nlow-c{display:flex;gap:10px;align-items:flex-start;margin:12px 0 0;font-size:14.5px;line-height:1.55;color:var(--o-ink2)}
.nlow .nlow-c input{margin-top:4px;width:18px;height:18px;flex:0 0 auto}
.nlow .nlow-trap{position:absolute!important;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);opacity:0}
.nlow .nlow-btn{display:inline-flex;align-items:center;justify-content:center;min-height:50px;padding:10px 22px;border-radius:999px;border:1px solid var(--o-sea);background:var(--o-sea);color:#fff!important;font:700 16.5px/1.2 inherit;cursor:pointer;text-decoration:none!important}
.nlow .nlow-btn:hover{background:var(--o-seah);border-color:var(--o-seah)}
.nlow .nlow-btn:disabled{opacity:.6;cursor:default}
.nlow .nlow-btn--ghost{background:transparent;color:var(--o-sea)!important}
.nlow .nlow-btn--ghost:hover{background:var(--o-sand)}
.nlow .nlow-btn--small{min-height:38px;padding:6px 14px;font-size:14.5px}
.nlow .nlow-bar{margin-top:18px}
.nlow .nlow-bar .nlow-btn,.nlow-gate .nlow-btn{width:100%}
.nlow .nlow-pick{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.nlow .nlow-pick input{position:absolute;width:1px;height:1px;opacity:0;pointer-events:none}
.nlow .nlow-pick input:focus-visible+label{outline:3px solid var(--o-sea);outline-offset:2px}
.nlow .nlow-count{font-size:15px;color:var(--o-mute)}
.nlow .nlow-thumbs{list-style:none;margin:14px 0 0;padding:0;display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
.nlow .nlow-thumbs:empty{display:none}
@media (max-width:640px){.nlow .nlow-thumbs{grid-template-columns:repeat(3,1fr)}}
.nlow .nlow-thumbs li{position:relative;aspect-ratio:1;border-radius:10px;overflow:hidden;background:var(--o-sand);margin:0}
.nlow .nlow-thumbs button.face{all:unset;display:block;width:100%;height:100%;cursor:pointer}
.nlow .nlow-thumbs img{width:100%;height:100%;object-fit:cover;display:block}
.nlow .nlow-thumbs .cover{position:absolute;top:6px;inset-inline-start:6px;background:#1F4B5C;color:#fff;font-size:12px;font-weight:700;padding:2px 8px;border-radius:999px}
.nlow .nlow-thumbs .x{position:absolute;top:4px;inset-inline-end:4px;width:30px;height:30px;border-radius:50%;border:0;background:rgba(20,33,43,.72);color:#fff;font-size:18px;line-height:30px;cursor:pointer;padding:0}
.nlow .nlow-thumbs .st{position:absolute;inset-inline:0;bottom:0;height:4px}
.nlow .nlow-thumbs li[data-s="up"] .st{background:var(--o-sea)}
.nlow .nlow-thumbs li[data-s="ok"] .st{background:var(--o-ok)}
.nlow .nlow-thumbs li[data-s="err"] .st{background:var(--o-bad)}
.nlow .nlow-status{margin-top:16px;padding:14px 16px;border-radius:12px;background:var(--o-sand);color:var(--o-ink);line-height:1.6}
.nlow .nlow-status b{display:block;font-size:17px;margin-bottom:4px}
.nlow .nlow-status[data-k="ok"]{background:#EAF4EF;border:1px solid var(--o-ok)}
.nlow .nlow-status[data-k="warn"]{background:#FBF3E4;border:1px solid var(--o-warn)}
.nlow .nlow-status[data-k="bad"]{background:#FBEDEC;border:1px solid var(--o-bad)}
.nlow .nlow-status ul{margin:6px 0 0;padding-inline-start:20px}
.nlow .nlow-status .row{display:flex;flex-wrap:wrap;gap:10px;margin-top:12px}
.nlow .nlow-err{color:var(--o-bad);margin:10px 0 0}
.nlow .nlow-mine{list-style:none;margin:8px 0 0;padding:0}
.nlow .nlow-mine li{display:grid;grid-template-columns:64px 1fr;gap:12px;padding:12px 0;border-top:1px solid var(--o-line);margin:0}
.nlow .nlow-mine li:first-child{border-top:0}
.nlow .nlow-mine li.nlow-muted{display:block;color:var(--o-mute)}
.nlow .nlow-mine img,.nlow .nlow-mine .ph{width:64px;height:64px;border-radius:10px;object-fit:cover;background:var(--o-sand);display:block}
.nlow .nlow-mine .t{font-weight:700;line-height:1.35}
.nlow .nlow-mine .t a{color:var(--o-ink);text-decoration:none}
.nlow .nlow-mine .m{display:flex;flex-wrap:wrap;gap:6px 10px;font-size:14px;color:var(--o-mute);margin-top:2px}
.nlow .pill{display:inline-block;padding:1px 10px;border-radius:999px;font-size:13px;font-weight:700;border:1px solid var(--o-line)}
.nlow .pill--active{color:var(--o-ok);border-color:var(--o-ok)}
.nlow .pill--sold,.nlow .pill--rented,.nlow .pill--pending{color:var(--o-warn);border-color:var(--o-warn)}
.nlow .acts{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px;grid-column:2}
.nlow-sheet{position:fixed;inset:0;background:rgba(15,26,33,.55);display:flex;align-items:flex-end;justify-content:center;z-index:99999;padding:16px}
.nlow-sheet-in{background:#fff;color:#14212B;border-radius:16px;padding:20px;width:100%;max-width:520px}
.nlow-sheet-in p{margin:0 0 12px;font-weight:600}
.nlow-sheet-in input{width:100%;min-height:48px;border:1px solid #E3E1DA;border-radius:10px;padding:8px 12px;font-size:18px;direction:ltr;text-align:right;box-sizing:border-box}
.nlow-sheet-b{display:flex;gap:10px;margin-top:14px}
.nlow-sheet-b .nlow-btn{flex:1}
.nlow-sheet .nlow-btn{display:inline-flex;align-items:center;justify-content:center;min-height:48px;border-radius:999px;border:1px solid #2F6F86;background:#2F6F86;color:#fff;font-weight:700;cursor:pointer}
.nlow-sheet .nlow-btn--ghost{background:transparent;color:#2F6F86}
[hidden]{display:none!important}
NLOCSS;
}

function nl_owner_js() {
	return <<<'NLOJS'
(function(){
'use strict';
var C=window.NLOWNER||{},api=C.api||'';
var $=function(id){return document.getElementById(id);};
var items=[],seq=0,busy=false,queue=Promise.resolve();
var files=$('nlow-files'),thumbs=$('nlow-thumbs'),count=$('nlow-count'),hint=$('nlow-hint1'),txt=$('nlow-txt'),send=$('nlow-send'),st=$('nlow-status'),mine=$('nlow-mine');
if(!files)return;
try{var d=localStorage.getItem('nlow-draft');if(d&&!txt.value){txt.value=d;}}catch(e){}
txt.addEventListener('input',function(){try{localStorage.setItem('nlow-draft',txt.value);}catch(e){}});
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
function say(kind,html){st.hidden=false;st.setAttribute('data-k',kind||'');st.innerHTML=html;st.scrollIntoView({block:'nearest',behavior:'smooth'});}
function hdr(json){var h={'X-WP-Nonce':C.nonce};if(json){h['Content-Type']='application/json';}return h;}
function shrink(file){return new Promise(function(res){var url=URL.createObjectURL(file),img=new Image();img.onload=function(){try{var max=2400,w=img.naturalWidth,h=img.naturalHeight,s=Math.min(1,max/Math.max(w,h));var c=document.createElement('canvas');c.width=Math.round(w*s);c.height=Math.round(h*s);c.getContext('2d').drawImage(img,0,0,c.width,c.height);c.toBlob(function(b){URL.revokeObjectURL(url);res(b||file);},'image/jpeg',0.86);}catch(e){URL.revokeObjectURL(url);res(file);}};img.onerror=function(){URL.revokeObjectURL(url);res(file);};img.src=url;});}
function render(){
  thumbs.innerHTML='';
  items.forEach(function(it,i){
    var li=document.createElement('li');li.setAttribute('data-s',it.s);
    li.innerHTML='<button type="button" class="face" aria-label="'+(i?'הפיכה לתמונה הראשית':'התמונה הראשית')+'"><img alt="" src="'+it.preview+'"></button>'+(i===0?'<span class="cover">ראשית</span>':'')+'<button type="button" class="x" aria-label="הסרת התמונה">×</button><span class="st"></span>';
    li.querySelector('.face').addEventListener('click',function(){if(i>0){items.unshift(items.splice(i,1)[0]);render();}});
    li.querySelector('.x').addEventListener('click',function(){items.splice(i,1);render();});
    thumbs.appendChild(li);
  });
  var up=items.filter(function(x){return x.s==='up';}).length;
  count.textContent=items.length?(items.length+' תמונות'+(up?', מעלים '+up:'')):'';
  hint.hidden=items.length<2;
}
function upload(it){it.s='up';render();return shrink(it.file).then(function(blob){var fd=new FormData();fd.append('photo',blob,'photo.jpg');return fetch(api+'/photo',{method:'POST',body:fd,headers:hdr(false),credentials:'same-origin'});}).then(function(r){return r.json().then(function(j){return {ok:r.ok,j:j};});}).then(function(x){if(x.ok&&x.j&&x.j.id){it.id=x.j.id;it.s='ok';}else{it.s='err';}render();}).catch(function(){it.s='err';render();});}
files.addEventListener('change',function(){Array.prototype.forEach.call(files.files,function(f){if(!/^image\//.test(f.type)&&!/\.(heic|heif|jpe?g|png|webp)$/i.test(f.name)){return;}var it={k:++seq,file:f,preview:URL.createObjectURL(f),s:'wait',id:0};items.push(it);queue=queue.then(function(){return items.indexOf(it)>-1?upload(it):null;});});files.value='';render();});
function post(path,body){return fetch(api+path,{method:'POST',headers:hdr(true),body:JSON.stringify(body||{}),credentials:'same-origin'}).then(function(r){return r.json().then(function(j){return {ok:r.ok,j:j};});});}
function who(){var r=document.querySelector('input[name="who"]:checked');return r?r.value:'owner';}
$('nlow-f').addEventListener('submit',function(e){
  e.preventDefault();if(busy){return;}
  if(who()==='broker'){say('warn','<b>למתווכים יש דרך מהירה יותר</b>אתר משלכם וקישור אישי להעלאת נכסים מהטלפון, בחינם. <a href="/brokers/#join">לפתיחת אתר למתווך</a>');return;}
  var text=txt.value.trim(),name=$('nlow-name').value.trim(),phone=$('nlow-phone').value.trim();
  if(!items.length){say('warn','<b>חסרות תמונות</b>בוחרים לפחות תמונה אחת של הנכס.');return;}
  if(text.length<8){say('warn','<b>חסרים פרטים</b>כותבים כמה שורות על הנכס: חדרים, שטח, שכונה ומחיר.');txt.focus();return;}
  if(!$('nlow-owner').checked||!$('nlow-consent').checked){say('warn','<b>חסרות ההצהרות</b>מסמנים את שתי ההצהרות שמעל הכפתור.');return;}
  busy=true;send.disabled=true;say('','<b>מעלים את התמונות</b>עוד רגע.');
  queue.then(function(){
    var failed=items.filter(function(x){return x.s==='err';});
    if(failed.length){say('warn','<b>'+failed.length+' תמונות לא עלו</b>אפשר להסיר אותן בנגיעה ב-× ולשלוח שוב.');throw 'stop';}
    say('','<b>קוראים את הפרטים</b>זה לוקח כמה שניות.');
    return post('/submit',{text:text,photos:items.map(function(x){return x.id;}),name:name,phone:phone,who:'owner',owner:'1',consent:'1'});
  }).then(function(x){
    if(!x.ok){say('bad','<b>השליחה לא עברה</b>'+esc((x.j&&x.j.message)||'אפשר לנסות שוב בעוד רגע.'));throw 'stop';}
    if(x.j.state==='held'){say('warn','<b>חסרים כמה פרטים כדי לבנות עמוד</b>'+(x.j.summary?'<div>הבנו: '+esc(x.j.summary)+'</div>':'')+'<ul>'+(x.j.missing||[]).map(function(m){return '<li>'+esc(m)+'</li>';}).join('')+'</ul><div>מוסיפים אותם בטקסט ושולחים שוב. התמונות כבר למעלה.</div>');throw 'stop';}
    say('','<b>כותבים את העמוד</b>'+esc(x.j.summary||'')+'<div>עד דקה.</div>');
    var drop=x.j.drop;return post('/build/'+drop,{}).catch(function(){return post('/build/'+drop,{});});
  }).then(function(x){
    if(!x||!x.ok||!x.j||!x.j.url_he){say('bad','<b>בניית העמוד לא הושלמה</b>אפשר ללחוץ שוב על פרסום. שום דבר לא יוכפל.');throw 'stop';}
    if(x.j.state==='pending'){say('warn','<b>המודעה נשמרה ותעלה אחרי בדיקה קצרה</b>חלק מהניסוח דורש בדיקה של אדם לפני פרסום.');}
    else{say('ok','<b>הנכס עלה לאתר</b>'+esc(x.j.title||'')+'<div class="row"><a class="nlow-btn nlow-btn--small" href="'+esc(x.j.url_he)+'" target="_blank" rel="noopener">לצפייה בעמוד</a><button type="button" class="nlow-btn nlow-btn--small nlow-btn--ghost" id="nlow-again">נכס נוסף</button></div>');}
    var again=$('nlow-again');if(again){again.addEventListener('click',function(){items=[];render();txt.value='';try{localStorage.removeItem('nlow-draft');}catch(e){}st.hidden=true;});}
    try{localStorage.removeItem('nlow-draft');}catch(e){}
    load();
  }).catch(function(err){if(err!=='stop'){say('bad','<b>אין חיבור</b>בודקים את האינטרנט ושולחים שוב.');}}).then(function(){busy=false;send.disabled=false;});
});
var sheet=$('nlow-sheet'),sheetT=$('nlow-sheet-t'),sheetF=$('nlow-sheet-f'),okB=$('nlow-sheet-ok'),noB=$('nlow-sheet-no'),onOk=null;
function ask(text,withInput,cb){sheetT.textContent=text;sheetF.innerHTML=withInput?'<input id="nlow-sheet-in" inputmode="numeric" autocomplete="off" aria-label="מחיר חדש בש״ח">':'';onOk=cb;sheet.hidden=false;var i=$('nlow-sheet-in');(i||okB).focus();}
okB.addEventListener('click',function(){var i=$('nlow-sheet-in'),v=i?i.value:'';sheet.hidden=true;if(onOk){onOk(v);}});
noB.addEventListener('click',function(){sheet.hidden=true;});
function load(){
  fetch(api+'/listings',{headers:hdr(false),credentials:'same-origin'}).then(function(r){return r.json();}).then(function(j){
    var L=(j&&j.listings)||[];
    if(!L.length){mine.innerHTML='<li class="nlow-muted">עוד אין מודעות. המודעה הראשונה תופיע כאן.</li>';return;}
    mine.innerHTML='';
    L.forEach(function(x){
      var li=document.createElement('li');
      var s=x.pending?'pending':(x.live?x.status:'draft'),lab={active:'באוויר',sold:'נמכר',rented:'הושכר',draft:'טיוטה',pending:'בבדיקה'}[s];
      var off=x.deal==='rent'?'rented':'sold',offLab=x.deal==='rent'?'הושכר':'נמכר';
      li.innerHTML=(x.cover?'<img alt="" src="'+esc(x.cover)+'">':'<span class="ph"></span>')+'<div><div class="t"><a href="'+esc(x.url)+'" target="_blank" rel="noopener">'+esc(x.title)+'</a></div><div class="m"><span class="pill pill--'+s+'">'+lab+'</span>'+(x.price?'<span>'+esc(x.price)+'</span>':'')+'</div></div>'+
        '<div class="acts">'+(x.status==='active'?'<button type="button" class="nlow-btn nlow-btn--small nlow-btn--ghost" data-a="off">'+offLab+'</button>':'<button type="button" class="nlow-btn nlow-btn--small nlow-btn--ghost" data-a="on">החזרה לפרסום</button>')+'<button type="button" class="nlow-btn nlow-btn--small nlow-btn--ghost" data-a="price">עדכון מחיר</button></div>';
      var bOff=li.querySelector('[data-a="off"]'),bOn=li.querySelector('[data-a="on"]'),bP=li.querySelector('[data-a="price"]');
      if(bOff){bOff.addEventListener('click',function(){ask('לסמן את "'+x.title+'" כ'+offLab+'? העמוד יישאר עם הודעה, וכפתורי הפנייה יורדים.',false,function(){post('/update',{id:x.id,status:off}).then(load);});});}
      if(bOn){bOn.addEventListener('click',function(){post('/update',{id:x.id,status:'active'}).then(load);});}
      if(bP){bP.addEventListener('click',function(){ask('מחיר חדש בש״ח ל"'+x.title+'"',true,function(v){if(!v){return;}post('/update',{id:x.id,price:v}).then(function(r){if(!r.ok){say('bad','<b>המחיר לא עודכן</b>'+esc((r.j&&r.j.message)||''));}load();});});});}
      mine.appendChild(li);
    });
  }).catch(function(){mine.innerHTML='<li class="nlow-muted">לא הצלחנו לטעון את הרשימה. מרעננים את העמוד.</li>';});
}
load();render();
})();
NLOJS;
}

add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$out['owner_wizard'] = array(
		'version' => NL_OWNER_VERSION,
		'engine'  => function_exists( 'nl_drop_build' ),
		'live'    => count( get_posts( array( 'post_type' => 'nadlan_property', 'post_status' => 'publish', 'fields' => 'ids', 'numberposts' => 500, 'meta_query' => array( array( 'key' => 'nl_owner', 'value' => '1' ) ), 'suppress_filters' => true ) ) ),
	);
	return $out;
} );
