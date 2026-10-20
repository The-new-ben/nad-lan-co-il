<?php
/**
 * nadlan-config · Broker self-edit (x-broker-edit) · v1.0.0 · 20.10.2026 (HAD-543 follow-up, Ben: "I want her to be able
 * to edit everything, the easiest and most accessible in the world, researched against the best interfaces").
 *
 * On the broker's private page (/drop/<token>/, built by x-broker-drop) every listing gets "עריכה", and the broker gets
 * "הפרופיל שלי". Nothing in x-broker-drop is changed: this module adds its own REST routes and appends its own script to
 * that page (an output buffer on the same request), and it builds on the engine's functions (nl_drop_*).
 *
 * The editor (pattern set from the research of 20.10.2026: Airbnb, Etsy, Booking.com, Google Business Profile, Shopify,
 * Instagram, Facebook Marketplace; WCAG 2.2 AA):
 *   - status (באוויר / נמכר or הושכר / חזרה לשוק) and photos save at once, with an undo toast;
 *   - every other section opens in its own sheet with one "שמירה": price; the details (deal, type, place, rooms, m²,
 *     floor of floors, balcony, garden, condition); the features (parking and how many, storage, lift, ממ"ד, air
 *     conditioning, furnished, view); entry and notes; the description (title, opening, up to three paragraphs);
 *   - photos: add (shrunk on the phone, location data removed by the engine's own route), delete, make cover, move;
 *     drag on a long press, and the same moves by taps (WCAG 2.5.7);
 *   - a "missing" line that opens the first empty field; a saved toast with the live page.
 * Facts are the broker's own: numbers are range-checked, never invented. When the details change, the page's text is
 * written again from them by the engine's gated writer (the same checks as a new listing). When the broker edits the
 * text, her Hebrew is kept as written (checked: no number that is not in the details, no banned words, no links) and the
 * other languages are written from it.
 * A listing built before the drop box (no stored facts) is prepared for editing on the first "עריכה": its page text and
 * photos go through the engine's reader and writer into a PENDING version; the live page changes only on the first save,
 * at the same address, in every language page that exists.
 * Profile: name, office, phone, about, areas, photo; saving refreshes the broker's site and the broker card on every
 * listing (no model call).
 *
 * Installed as the persistent Code Snippet "x-broker-edit" by scripts/broker-edit/deployedit.py (needs x-broker-drop).
 * Rollback: python scripts/broker-edit/deployedit.py --off  (the private page returns to what x-broker-drop alone shows).
 */

if ( ! defined( 'ABSPATH' ) ) { return; }
if ( defined( 'NL_EDIT_VERSION' ) ) { return; }
define( 'NL_EDIT_VERSION', '1.0.0' );

/* =====================================================================================================
 * The private page: the editor's script and sheet are appended to what x-broker-drop prints.
 * ===================================================================================================== */
add_action( 'parse_request', function () {
	if ( ! function_exists( 'nl_drop_broker_by_token' ) ) { return; }
	$path = trim( (string) wp_parse_url( isset( $_SERVER['REQUEST_URI'] ) ? wp_unslash( $_SERVER['REQUEST_URI'] ) : '', PHP_URL_PATH ), '/' );
	if ( ! preg_match( '#^drop/([a-z0-9]{24})$#', $path, $m ) ) { return; }
	$b = nl_drop_broker_by_token( $m[1] );
	if ( ! $b ) { return; }
	$cfg = array(
		'api'   => esc_url_raw( rest_url( 'nadlan/v1/drop/' . $m[1] ) ),
		'name'  => (string) $b['name_he'],
		'langs' => array_values( (array) ( $b['langs'] ?? array( 'he' ) ) ),
		'wa'    => '972525101555',
		'film'  => array( 'src' => 'https://nad-lan.co.il/wp-content/uploads/2026/10/nadlan-broker-edit-he.mp4', 'poster' => 'https://nad-lan.co.il/wp-content/uploads/2026/10/nadlan-broker-edit-he.jpg', 'len' => '2:42' ),
	);
	ob_start( function ( $html ) use ( $cfg ) {
		$at = strripos( (string) $html, '</body>' );
		if ( $at === false ) { return $html; }
		$add = '<style>' . nl_edit_css() . '</style><script>window.NLEDIT=' . wp_json_encode( $cfg, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . ';</script><script>' . nl_edit_js() . '</script>';
		return substr( $html, 0, $at ) . $add . substr( $html, $at );
	} );
}, -1 );

/* =====================================================================================================
 * REST
 * ===================================================================================================== */
add_action( 'rest_api_init', function () {
	$t = '/drop/(?P<token>[a-z0-9]{24})/edit';
	$o = array( 'permission_callback' => '__return_true' );
	register_rest_route( 'nadlan/v1', $t . '/listings', $o + array( 'methods' => 'GET', 'callback' => 'nl_edit_rest_list' ) );
	register_rest_route( 'nadlan/v1', $t . '/listing/(?P<id>\d+)', array(
		$o + array( 'methods' => 'GET', 'callback' => 'nl_edit_rest_get' ),
		$o + array( 'methods' => 'POST', 'callback' => 'nl_edit_rest_save' ),
	) );
	register_rest_route( 'nadlan/v1', $t . '/prepare/(?P<id>\d+)', $o + array( 'methods' => 'POST', 'callback' => 'nl_edit_rest_prepare' ) );
	register_rest_route( 'nadlan/v1', $t . '/profile', array(
		$o + array( 'methods' => 'GET', 'callback' => 'nl_edit_rest_profile' ),
		$o + array( 'methods' => 'POST', 'callback' => 'nl_edit_rest_profile_save' ),
	) );
} );

function nl_edit_broker( WP_REST_Request $req ) {
	if ( ! function_exists( 'nl_drop_rest_broker' ) ) { return new WP_Error( 'nl_edit_off', 'העריכה לא זמינה כרגע.', array( 'status' => 503 ) ); }
	$b = nl_drop_rest_broker( $req );
	if ( is_wp_error( $b ) ) { return $b; }
	if ( ( $b['kind'] ?? 'broker' ) !== 'broker' ) { return new WP_Error( 'nl_edit_kind', 'העריכה זמינה למתווכים.', array( 'status' => 403 ) ); }
	return $b;
}

/** The listing must be this broker's Hebrew listing. */
function nl_edit_own( $id, $b ) {
	$p = get_post( (int) $id );
	if ( ! $p || $p->post_type !== 'nadlan_property' ) { return new WP_Error( 'nl_edit_none', 'המודעה לא נמצאה.', array( 'status' => 404 ) ); }
	if ( (string) get_post_meta( $p->ID, 'nl_broker_id', true ) !== (string) (int) $b['id'] ) { return new WP_Error( 'nl_edit_owner', 'המודעה הזאת לא שייכת לקישור הזה.', array( 'status' => 403 ) ); }
	return $p;
}

function nl_edit_json( $id, $k ) {
	$v = json_decode( (string) get_post_meta( $id, $k, true ), true );
	return is_array( $v ) ? $v : null;
}

/* ---------------- the field model: the broker's own values, range-checked ---------------- */
function nl_edit_fields() {
	return array(
		'num'  => array( 'price' => array( 500, 500000000, 0 ), 'rooms' => array( 1, 30, 1 ), 'size_sqm' => array( 10, 5000, 0 ), 'balcony_sqm' => array( 1, 2000, 0 ),
			'garden_sqm' => array( 1, 20000, 0 ), 'floor' => array( -5, 120, 0 ), 'total_floors' => array( 1, 120, 0 ), 'parking_count' => array( 1, 20, 0 ) ),
		'bool' => array( 'parking', 'storage', 'elevator', 'protected_room', 'ac', 'furnished', 'exclusive' ),
		'enum' => array(
			'listing_type'  => array( 'sale', 'rent' ),
			'property_type' => array( 'apartment', 'penthouse', 'mini_penthouse', 'garden', 'duplex', 'villa', 'cottage', 'studio', 'other' ),
			'condition'     => array( 'new', 'renovated', 'good', 'needs_renovation' ),
		),
		'str'  => array( 'city_he' => 60, 'area_he' => 60, 'street_he' => 80, 'entry_he' => 60, 'view_he' => 60, 'notes_he' => 320 ),
	);
}

/** Merges the sent fields into the facts; returns the facts or an error that names the field. */
function nl_edit_merge_facts( $f, $in ) {
	$M = nl_edit_fields();
	$f = is_array( $f ) ? $f : array();
	$label = array( 'price' => 'המחיר', 'rooms' => 'מספר החדרים', 'size_sqm' => 'השטח', 'balcony_sqm' => 'שטח המרפסת', 'garden_sqm' => 'שטח הגינה',
		'floor' => 'הקומה', 'total_floors' => 'מספר הקומות בבניין', 'parking_count' => 'מספר החניות' );
	foreach ( $M['num'] as $k => $r ) {
		if ( ! array_key_exists( $k, $in ) ) { continue; }
		$v = $in[ $k ];
		if ( $v === null || $v === '' ) { $f[ $k ] = null; continue; }
		$v = str_replace( array( ',', ' ', '₪' ), '', (string) $v );
		if ( ! is_numeric( $v ) ) { return new WP_Error( 'nl_edit_num', 'כדאי לכתוב את ' . $label[ $k ] . ' במספרים בלבד.', array( 'status' => 400, 'field' => $k ) ); }
		$v = (float) $v;
		if ( $v < $r[0] || $v > $r[1] ) { return new WP_Error( 'nl_edit_range', $label[ $k ] . ' לא נראה תקין.', array( 'status' => 400, 'field' => $k ) ); }
		$f[ $k ] = $r[2] ? round( $v * 2 ) / 2 : (int) round( $v );
	}
	if ( isset( $f['floor'], $f['total_floors'] ) && $f['floor'] !== null && $f['total_floors'] !== null && $f['floor'] > $f['total_floors'] ) {
		return new WP_Error( 'nl_edit_floor', 'הקומה גבוהה ממספר הקומות בבניין.', array( 'status' => 400, 'field' => 'floor' ) );
	}
	foreach ( $M['bool'] as $k ) {
		if ( ! array_key_exists( $k, $in ) ) { continue; }
		$v = $in[ $k ];
		$f[ $k ] = ( $v === null || $v === '' ) ? null : ( $v === true || $v === 1 || $v === '1' || $v === 'true' );
	}
	if ( ! empty( $f['parking_count'] ) ) { $f['parking'] = true; }
	if ( isset( $f['parking'] ) && $f['parking'] === false ) { $f['parking_count'] = null; }
	foreach ( $M['enum'] as $k => $ok ) {
		if ( ! array_key_exists( $k, $in ) ) { continue; }
		$f[ $k ] = in_array( $in[ $k ], $ok, true ) ? $in[ $k ] : null;
	}
	foreach ( $M['str'] as $k => $max ) {
		if ( ! array_key_exists( $k, $in ) ) { continue; }
		$v = trim( wp_strip_all_tags( (string) $in[ $k ] ) );
		$v = function_exists( 'mb_substr' ) ? mb_substr( $v, 0, $max ) : substr( $v, 0, $max );
		$f[ $k ] = $v === '' ? null : ( function_exists( 'nl_drop_he_typo' ) ? nl_drop_he_typo( $v ) : $v );
	}
	if ( array_key_exists( 'features_he', $in ) ) {
		$list = array();
		foreach ( (array) $in['features_he'] as $s ) {
			$s = trim( wp_strip_all_tags( (string) $s ) );
			if ( $s !== '' ) { $list[] = function_exists( 'mb_substr' ) ? mb_substr( $s, 0, 60 ) : $s; }
			if ( count( $list ) >= 8 ) { break; }
		}
		$f['features_he'] = $list;
	}
	if ( empty( $f['listing_type'] ) ) { return new WP_Error( 'nl_edit_deal', 'חסר: למכירה או להשכרה.', array( 'status' => 400, 'field' => 'listing_type' ) ); }
	if ( empty( $f['area_he'] ) && empty( $f['city_he'] ) ) { return new WP_Error( 'nl_edit_place', 'חסר: שכונה או עיר.', array( 'status' => 400, 'field' => 'area_he' ) ); }
	return $f;
}

/** The broker's own words for the writer: the details as sentences, so every number in them is allowed. */
function nl_edit_message( $f, $prev = '' ) {
	$t = array();
	$deal = ( $f['listing_type'] ?? '' ) === 'rent' ? 'להשכרה' : 'למכירה';
	$t[] = $deal . ( ! empty( $f['property_type'] ) && function_exists( 'nl_drop_type_label' ) && $f['property_type'] !== 'other' ? ', ' . nl_drop_type_label( $f['property_type'], 'he' ) : '' ) . '.';
	if ( ! empty( $f['area_he'] ) || ! empty( $f['city_he'] ) ) { $t[] = trim( implode( ', ', array_filter( array( $f['area_he'] ?? '', $f['city_he'] ?? '' ) ) ) ) . '.'; }
	if ( ! empty( $f['rooms'] ) ) { $t[] = $f['rooms'] . ' חדרים.'; }
	if ( ! empty( $f['size_sqm'] ) ) { $t[] = $f['size_sqm'] . ' מ״ר.'; }
	if ( isset( $f['floor'] ) && $f['floor'] !== null ) { $t[] = ( $f['floor'] == 0 ? 'קומת קרקע' : 'קומה ' . $f['floor'] ) . ( ! empty( $f['total_floors'] ) ? ' מתוך ' . $f['total_floors'] : '' ) . '.'; }
	if ( ! empty( $f['balcony_sqm'] ) ) { $t[] = 'מרפסת של ' . $f['balcony_sqm'] . ' מ״ר.'; }
	if ( ! empty( $f['garden_sqm'] ) ) { $t[] = 'גינה של ' . $f['garden_sqm'] . ' מ״ר.'; }
	if ( ! empty( $f['parking_count'] ) ) { $t[] = $f['parking_count'] . ' חניות.'; } elseif ( ! empty( $f['parking'] ) ) { $t[] = 'חניה.'; }
	foreach ( array( 'storage' => 'מחסן', 'elevator' => 'מעלית', 'protected_room' => 'ממ״ד', 'ac' => 'מיזוג', 'furnished' => 'מרוהטת' ) as $k => $w ) {
		if ( ! empty( $f[ $k ] ) ) { $t[] = $w . '.'; }
	}
	$cond = array( 'new' => 'חדשה', 'renovated' => 'משופצת', 'good' => 'במצב טוב', 'needs_renovation' => 'דורשת שיפוץ' );
	if ( ! empty( $f['condition'] ) && isset( $cond[ $f['condition'] ] ) ) { $t[] = $cond[ $f['condition'] ] . '.'; }
	if ( ! empty( $f['view_he'] ) ) { $t[] = $f['view_he'] . '.'; }
	if ( ! empty( $f['entry_he'] ) ) { $t[] = 'כניסה: ' . $f['entry_he'] . '.'; }
	if ( ! empty( $f['price'] ) ) { $t[] = number_format( (float) $f['price'] ) . ' ש״ח' . ( ( $f['listing_type'] ?? '' ) === 'rent' ? ' לחודש' : '' ) . '.'; }
	if ( ! empty( $f['exclusive'] ) ) { $t[] = 'בלעדיות.'; }
	foreach ( (array) ( $f['features_he'] ?? array() ) as $x ) { $t[] = $x . '.'; }
	if ( ! empty( $f['notes_he'] ) ) { $t[] = $f['notes_he']; }
	$msg = implode( ' ', $t );
	// the earlier message keeps its words (a view, a story); a number in it that the details no longer carry is dropped
	if ( $prev !== '' ) {
		$keep = array();
		foreach ( preg_split( '/(?<=[.!?\n])\s+/u', (string) $prev ) as $s ) {
			$s = trim( $s );
			if ( $s === '' ) { continue; }
			if ( function_exists( 'nl_drop_nums_in_copy' ) && nl_drop_nums_in_copy( $s ) ) { continue; }
			$keep[] = $s;
		}
		if ( $keep ) { $msg .= "\n" . implode( ' ', array_slice( $keep, 0, 12 ) ); }
	}
	return $msg;
}

/* ---------------- what the editor shows ---------------- */
function nl_edit_missing( $f ) {
	$miss = array();
	foreach ( array( 'price' => 'מחיר', 'rooms' => 'חדרים', 'size_sqm' => 'מ״ר', 'floor' => 'קומה', 'entry_he' => 'מועד כניסה' ) as $k => $w ) {
		if ( ! isset( $f[ $k ] ) || $f[ $k ] === null || $f[ $k ] === '' ) { $miss[] = array( 'k' => $k, 'w' => $w ); }
	}
	if ( empty( $f['area_he'] ) && empty( $f['city_he'] ) ) { $miss[] = array( 'k' => 'area_he', 'w' => 'שכונה' ); }
	return $miss;
}

function nl_edit_view( $id, $b ) {
	$p       = get_post( (int) $id );
	$f       = nl_edit_json( $id, 'nl_facts' );
	$c       = nl_edit_json( $id, 'nl_copy' );
	$ph      = nl_edit_json( $id, 'nl_photos_json' );
	$pending = nl_edit_json( $id, '_nl_edit_pending' );
	$ready   = is_array( $f ) && is_array( $c );
	if ( ! $ready && $pending ) { $f = $pending['f']; $c = $pending['c']; $ph = $pending['ph']; }
	$he      = is_array( $c ) && isset( $c['he'] ) ? $c['he'] : array();
	$fill    = function ( $s ) use ( $f ) { return function_exists( 'nl_drop_fill' ) && is_array( $f ) ? nl_drop_fill( (string) $s, $f, 'he' ) : (string) $s; };
	$photos  = array();
	foreach ( (array) $ph as $x ) {
		$aid = (int) ( $x['id'] ?? 0 );
		if ( ! $aid ) { continue; }
		$th = wp_get_attachment_image_src( $aid, 'medium_large' );
		$photos[] = array( 'id' => $aid, 'url' => $th ? $th[0] : (string) ( $x['url'] ?? '' ) );
	}
	$st = (string) get_post_meta( $id, 'nl_status', true );
	$out = array(
		'id'       => (int) $id,
		'url'      => (string) get_permalink( $id ),
		'title'    => (string) get_the_title( $id ),
		'live'     => get_post_status( $id ) === 'publish',
		'status'   => in_array( $st, array( 'sold', 'rented' ), true ) ? $st : 'active',
		'ready'    => $ready,
		'pending'  => ! $ready && (bool) $pending,
		'modified' => human_time_diff( min( current_time( 'timestamp' ), max( (int) get_post_modified_time( 'U', false, $id ), (int) get_post_time( 'U', false, $id ) ) ), current_time( 'timestamp' ) ),
		'photos'   => $photos,
	);
	if ( is_array( $f ) ) {
		$keep = array_merge( array_keys( nl_edit_fields()['num'] ), nl_edit_fields()['bool'], array_keys( nl_edit_fields()['enum'] ), array_keys( nl_edit_fields()['str'] ), array( 'features_he' ) );
		$out['facts']   = array_intersect_key( $f, array_flip( $keep ) );
		$out['missing'] = nl_edit_missing( $f );
		$out['text']    = array( 'title' => $fill( $he['title'] ?? '' ), 'dek' => $fill( $he['dek'] ?? '' ), 'story' => array_map( $fill, (array) ( $he['story'] ?? array() ) ) );
	}
	return $out;
}

function nl_edit_rest_list( WP_REST_Request $req ) {
	$b = nl_edit_broker( $req );
	if ( is_wp_error( $b ) ) { return $b; }
	$rows = array();
	foreach ( nl_drop_broker_listings( $b['id'], 'he', false ) as $L ) {
		$f = nl_edit_json( $L['id'], 'nl_facts' );
		$rows[] = array( 'id' => $L['id'], 'url' => $L['url'], 'ready' => is_array( $f ), 'missing' => is_array( $f ) ? count( nl_edit_missing( $f ) ) : null );
	}
	return array( 'listings' => $rows );
}

function nl_edit_rest_get( WP_REST_Request $req ) {
	$b = nl_edit_broker( $req );
	if ( is_wp_error( $b ) ) { return $b; }
	$p = nl_edit_own( $req['id'], $b );
	if ( is_wp_error( $p ) ) { return $p; }
	return nl_edit_view( $p->ID, $b );
}

/* ---------------- an older listing, prepared for editing (the live page is untouched until the first save) ---------------- */
function nl_edit_page_photos( $id ) {
	$ids  = array();
	$th   = (int) get_post_thumbnail_id( $id );
	if ( $th ) { $ids[] = $th; }
	$html = (string) get_post_field( 'post_content', $id );
	if ( preg_match_all( '/wp-image-(\d+)/', $html, $m ) ) { foreach ( $m[1] as $x ) { $ids[] = (int) $x; } }
	if ( preg_match_all( '/<img[^>]+src="([^"]+)"/i', $html, $m ) ) {
		foreach ( $m[1] as $u ) {
			$u   = preg_replace( '/-\d+x\d+(?=\.(jpe?g|png|webp)$)/i', '', html_entity_decode( $u ) );
			$aid = attachment_url_to_postid( $u );
			if ( $aid ) { $ids[] = (int) $aid; }
		}
	}
	foreach ( array_filter( array_map( 'trim', explode( ',', (string) get_post_meta( $id, 'photos_csv', true ) ) ) ) as $u ) {
		$aid = attachment_url_to_postid( $u );
		if ( $aid ) { $ids[] = (int) $aid; }
	}
	$out = array();
	foreach ( array_unique( $ids ) as $aid ) { if ( wp_attachment_is_image( $aid ) ) { $out[] = $aid; } }
	return array_slice( $out, 0, 30 );
}

function nl_edit_rest_prepare( WP_REST_Request $req ) {
	$b = nl_edit_broker( $req );
	if ( is_wp_error( $b ) ) { return $b; }
	$p = nl_edit_own( $req['id'], $b );
	if ( is_wp_error( $p ) ) { return $p; }
	if ( is_array( nl_edit_json( $p->ID, 'nl_facts' ) ) || nl_edit_json( $p->ID, '_nl_edit_pending' ) ) { return nl_edit_view( $p->ID, $b ); }
	if ( nl_drop_rate( $b['id'], 'edit_ai', 40, HOUR_IN_SECONDS ) ) { return new WP_Error( 'rate', 'הרבה עדכונים בשעה האחרונה. אפשר להמשיך בעוד כמה דקות.', array( 'status' => 429 ) ); }
	if ( function_exists( 'set_time_limit' ) ) { @set_time_limit( 300 ); }
	$text = trim( (string) $p->post_title ) . "\n" . trim( preg_replace( '/\s+/u', ' ', wp_strip_all_tags( strip_shortcodes( (string) $p->post_content ) ) ) );
	$text = function_exists( 'mb_substr' ) ? mb_substr( $text, 0, 6000 ) : substr( $text, 0, 6000 );
	$err  = null;
	$f    = nl_drop_extract( $text, $b, $err );
	if ( ! is_array( $f ) ) { return new WP_Error( 'nl_edit_read', 'לא הצלחנו לקרוא את המודעה. אפשר לנסות שוב בעוד רגע.', array( 'status' => 502 ) ); }
	if ( empty( $f['listing_type'] ) ) { $f['listing_type'] = (string) get_post_meta( $p->ID, 'listing_type', true ) === 'rent' ? 'rent' : 'sale'; }
	$c   = nl_edit_write_all( $f, $text, $b, $p->ID );
	$ids = nl_edit_page_photos( $p->ID );
	$ph  = nl_drop_photos( $ids, nl_drop_fill( $c['he']['title'], $f, 'he' ) );
	update_post_meta( $p->ID, '_nl_edit_pending', wp_slash( wp_json_encode( array( 'f' => $f, 'c' => $c, 'ph' => $ph, 'text' => $text, 'at' => time() ), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) ) );
	return nl_edit_view( $p->ID, $b );
}

/** He and En from the engine's writer; Ru and Fr from its translator, for the languages that have a page. */
function nl_edit_write_all( $f, $text, $b, $id, $keep_he = null ) {
	$err  = null;
	$copy = nl_drop_write( $f, $text, $b, $err );
	if ( is_array( $keep_he ) ) { $copy['he'] = $keep_he; }
	$have = array_keys( nl_drop_twins( $id ) );
	$xl   = array_values( array_intersect( array( 'ru', 'fr' ), array_intersect( (array) ( $b['langs'] ?? array() ), $have ) ) );
	if ( $xl && function_exists( 'nl_drop_translate' ) ) {
		$terr = null;
		$tr   = nl_drop_translate( $copy, $f, $text, $xl, $terr );
		foreach ( (array) ( $tr['copy'] ?? array() ) as $l => $c ) { $copy[ $l ] = $c; }
	}
	return $copy;
}

/* ---------------- saving ---------------- */
function nl_edit_commit( $id, $b, $f, $c, $ph, $text = null ) {
	$pub = $f;
	update_post_meta( $id, 'nl_facts', wp_slash( wp_json_encode( $pub, JSON_UNESCAPED_UNICODE ) ) );
	update_post_meta( $id, 'nl_copy', wp_slash( wp_json_encode( $c, JSON_UNESCAPED_UNICODE ) ) );
	update_post_meta( $id, 'nl_photos_json', wp_slash( wp_json_encode( $ph, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) ) );
	update_post_meta( $id, 'photos_csv', implode( ',', wp_list_pluck( $ph, 'url' ) ) );
	if ( (string) get_post_meta( $id, 'source', true ) === '' ) { update_post_meta( $id, 'source', 'broker_drop' ); update_post_meta( $id, 'nl_edit_adopted', gmdate( 'c' ) ); }
	if ( $text !== null ) { update_post_meta( $id, 'nl_edit_text', wp_slash( (string) $text ) ); }
	delete_post_meta( $id, '_nl_edit_pending' );
	// the portal's own fields, the same map as a new listing
	$type_map = array( 'mini_penthouse' => 'penthouse', 'villa' => 'cottage' );
	$meta = array(
		'listing_type' => $f['listing_type'] ?? null, 'property_type' => ! empty( $f['property_type'] ) ? ( $type_map[ $f['property_type'] ] ?? $f['property_type'] ) : null,
		'price' => $f['price'] ?? null, 'rooms' => $f['rooms'] ?? null, 'floor' => $f['floor'] ?? null, 'total_floors' => $f['total_floors'] ?? null,
		'size_sqm' => $f['size_sqm'] ?? null, 'sqm' => $f['size_sqm'] ?? null, 'balcony_sqm' => $f['balcony_sqm'] ?? null, 'city' => $f['city_he'] ?? null,
		'neighborhood' => $f['area_he'] ?? null, 'parking' => $f['parking'] ?? null, 'elevator' => $f['elevator'] ?? null, 'ac' => $f['ac'] ?? null,
		'protected_room' => $f['protected_room'] ?? null, 'storage' => $f['storage'] ?? null, 'entry_date' => $f['entry_he'] ?? null, 'condition' => $f['condition'] ?? null,
		'highlights_csv' => implode( '|', array_slice( (array) ( $f['features_he'] ?? array() ), 0, 6 ) ),
	);
	foreach ( $meta as $k => $v ) {
		if ( $v === null || $v === '' ) { delete_post_meta( $id, $k ); } else { update_post_meta( $id, $k, is_bool( $v ) ? ( $v ? '1' : '0' ) : $v ); }
	}
	// every language page: title, cover; the page itself from the stored facts and copy
	$ids = array( 'he' => (int) $id ) + nl_drop_twins( $id );
	$had = nl_drop_kses_off();
	foreach ( $ids as $l => $pid ) {
		if ( empty( $c[ $l ]['title'] ) || ! get_post( $pid ) ) { continue; }
		wp_update_post( array( 'ID' => $pid, 'post_title' => nl_drop_fill( $c[ $l ]['title'], $f, $l ) ) );
		if ( $ph ) { set_post_thumbnail( $pid, (int) $ph[0]['id'] ); }
		if ( $l !== 'he' && (string) get_post_meta( $pid, 'source', true ) === '' ) { update_post_meta( $pid, 'source', 'broker_drop' ); }
	}
	nl_drop_kses_on( $had );
	foreach ( $ph as $i => $x ) {
		update_post_meta( (int) $x['id'], '_wp_attachment_image_alt', wp_slash( nl_drop_fill( $c['he']['title'], $f, 'he' ) . ( $i ? ' · ' . ( $i + 1 ) : '' ) ) );
	}
	nl_drop_render_all( $id, $b );
	nl_drop_site_sync( $b );
	nl_drop_purge( array_merge( array_values( $ids ), array( $b['site_he'] ?? 0, $b['site_en'] ?? 0, $b['site_ru'] ?? 0, $b['site_fr'] ?? 0 ) ) );
	update_post_meta( $id, 'nl_edit_last', gmdate( 'c' ) );
	return true;
}

function nl_edit_rest_save( WP_REST_Request $req ) {
	$b = nl_edit_broker( $req );
	if ( is_wp_error( $b ) ) { return $b; }
	$p = nl_edit_own( $req['id'], $b );
	if ( is_wp_error( $p ) ) { return $p; }
	if ( nl_drop_rate( $b['id'], 'edit', 300, HOUR_IN_SECONDS ) ) { return new WP_Error( 'rate', 'הרבה עדכונים בשעה האחרונה. אפשר להמשיך בעוד כמה דקות.', array( 'status' => 429 ) ); }
	$id   = $p->ID;
	$body = (array) $req->get_json_params();
	$sec  = (string) ( $body['section'] ?? '' );
	$data = (array) ( $body['data'] ?? array() );
	if ( $sec === 'status' ) {
		$st = (string) ( $data['status'] ?? '' );
		if ( ! in_array( $st, array( 'active', 'sold', 'rented' ), true ) ) { return new WP_Error( 'nl_edit_status', 'מצב לא מוכר.', array( 'status' => 400 ) ); }
		$r = nl_drop_apply_update( $id, $b, $st, null );
		if ( is_wp_error( $r ) ) { return $r; }
		return array( 'ok' => true, 'msg' => $st === 'active' ? 'המודעה חזרה לפרסום.' : ( $st === 'sold' ? 'המודעה סומנה כנמכרה.' : 'המודעה סומנה כמושכרת.' ), 'listing' => nl_edit_view( $id, $b ) );
	}
	$f  = nl_edit_json( $id, 'nl_facts' );
	$c  = nl_edit_json( $id, 'nl_copy' );
	$ph = nl_edit_json( $id, 'nl_photos_json' ) ?: array();
	$text = (string) get_post_meta( $id, 'nl_edit_text', true );
	if ( ! is_array( $f ) || ! is_array( $c ) ) {
		$pend = nl_edit_json( $id, '_nl_edit_pending' );
		if ( ! $pend ) { return new WP_Error( 'nl_edit_prepare', 'צריך להכין את המודעה לעריכה קודם.', array( 'status' => 409 ) ); }
		$f = $pend['f']; $c = $pend['c']; $ph = (array) $pend['ph']; $text = (string) ( $pend['text'] ?? '' );
	}
	if ( $text === '' ) {
		$did  = (int) get_post_meta( $id, 'nl_drop_id', true );
		$text = $did ? (string) get_post_meta( $did, 'nl_text', true ) : '';
	}
	if ( function_exists( 'set_time_limit' ) ) { @set_time_limit( 300 ); }
	$msg = 'נשמר. השינוי כבר מופיע באתר.';
	if ( $sec === 'price' ) {
		$f2 = nl_edit_merge_facts( $f, array( 'price' => $data['price'] ?? null ) );
		if ( is_wp_error( $f2 ) ) { return $f2; }
		$f = $f2;
		// the price lives as a token in the copy; a copy written before the price was known says "on request": write it again
		if ( ! empty( $f['price'] ) && strpos( wp_json_encode( $c['he'] ?? array(), JSON_UNESCAPED_UNICODE ), '{{PRICE}}' ) === false ) {
			if ( nl_drop_rate( $b['id'], 'edit_ai', 40, HOUR_IN_SECONDS ) ) { return new WP_Error( 'rate', 'הרבה עדכונים בשעה האחרונה.', array( 'status' => 429 ) ); }
			$text = nl_edit_message( $f, $text );
			$c    = nl_edit_write_all( $f, $text, $b, $id );
		}
	} elseif ( $sec === 'facts' ) {
		$f2 = nl_edit_merge_facts( $f, (array) ( $data['facts'] ?? array() ) );
		if ( is_wp_error( $f2 ) ) { return $f2; }
		if ( nl_drop_rate( $b['id'], 'edit_ai', 40, HOUR_IN_SECONDS ) ) { return new WP_Error( 'rate', 'הרבה עדכונים בשעה האחרונה.', array( 'status' => 429 ) ); }
		$f    = $f2;
		$text = nl_edit_message( $f, $text );
		$c    = nl_edit_write_all( $f, $text, $b, $id );
		$msg  = 'נשמר. העמוד נכתב מחדש לפי הפרטים, בכל השפות.';
	} elseif ( $sec === 'text' ) {
		$in    = array( 'title' => $data['title'] ?? '', 'dek' => $data['dek'] ?? '', 'story' => array_slice( (array) ( $data['story'] ?? array() ), 0, 3 ) );
		$clean = function ( $s, $max ) {
			$s = trim( preg_replace( '/\s+/u', ' ', wp_strip_all_tags( (string) $s ) ) );
			return function_exists( 'mb_substr' ) ? mb_substr( $s, 0, $max ) : substr( $s, 0, $max );
		};
		$he          = (array) $c['he'];
		$he['title'] = $clean( $in['title'], 90 );
		$he['dek']   = $clean( $in['dek'], 460 );
		$he['story'] = array_values( array_filter( array_map( function ( $s ) use ( $clean ) { return $clean( $s, 800 ); }, $in['story'] ) ) );
		if ( $he['title'] === '' ) { return new WP_Error( 'nl_edit_title', 'הכותרת לא יכולה להיות ריקה.', array( 'status' => 400, 'field' => 'title' ) ); }
		$allowed = nl_drop_allowed_numbers( $f, $text . ' ' . nl_edit_message( $f ) );
		$names   = array_values( array_filter( array( $f['area_he'] ?? '', $f['city_he'] ?? '' ) ) );
		foreach ( array( 'title' => 'בכותרת', 'dek' => 'בפתיח' ) as $k => $where ) {
			$iss = nl_drop_gate_str( nl_drop_price_token( $he[ $k ], $f ), 'he', $allowed, null, $names );
			if ( $iss ) { return nl_edit_gate_error( $iss, $where, $k ); }
		}
		foreach ( $he['story'] as $i => $s ) {
			$iss = nl_drop_gate_str( nl_drop_price_token( $s, $f ), 'he', $allowed, null, $names );
			if ( $iss ) { return nl_edit_gate_error( $iss, 'בפסקה ' . ( $i + 1 ), 'story' ); }
		}
		if ( ! $he['story'] ) { $he['story'] = (array) ( $c['he']['story'] ?? array() ); }
		foreach ( array( 'title', 'dek' ) as $k ) { $he[ $k ] = nl_drop_price_token( $he[ $k ], $f ); }
		$he['story'] = array_map( function ( $s ) use ( $f ) { return nl_drop_price_token( $s, $f ); }, $he['story'] );
		if ( nl_drop_rate( $b['id'], 'edit_ai', 40, HOUR_IN_SECONDS ) ) { return new WP_Error( 'rate', 'הרבה עדכונים בשעה האחרונה.', array( 'status' => 429 ) ); }
		// the other languages follow the broker's Hebrew, written by the engine's gated writer from it
		$words = nl_edit_message( $f ) . "\n" . $he['title'] . ". " . $he['dek'] . "\n" . implode( "\n", $he['story'] );
		$c     = nl_edit_write_all( $f, $words, $b, $id, $he );
		$msg   = 'נשמר. הטקסט בעברית כפי שכתבת, ושאר השפות עודכנו לפיו.';
	} elseif ( $sec === 'photos' ) {
		$order = array_values( array_unique( array_map( 'intval', (array) ( $data['ids'] ?? array() ) ) ) );
		if ( ! $order ) { return new WP_Error( 'nl_edit_nophoto', 'צריך לפחות תמונה אחת.', array( 'status' => 400 ) ); }
		$known = array_map( 'intval', wp_list_pluck( $ph, 'id' ) );
		foreach ( $order as $aid ) {
			$mine = in_array( $aid, $known, true ) || (string) get_post_meta( $aid, 'nl_drop_broker', true ) === (string) $b['id'];
			if ( ! $mine || ! wp_attachment_is_image( $aid ) ) { return new WP_Error( 'nl_edit_photo', 'אחת התמונות לא שייכת למודעה.', array( 'status' => 400 ) ); }
		}
		$ph  = nl_drop_photos( array_slice( $order, 0, 30 ), nl_drop_fill( $c['he']['title'], $f, 'he' ) );
		$msg = 'התמונות נשמרו.';
	} else {
		return new WP_Error( 'nl_edit_section', 'לא התקבל עדכון.', array( 'status' => 400 ) );
	}
	nl_edit_commit( $id, $b, $f, $c, $ph, $text );
	return array( 'ok' => true, 'msg' => $msg, 'listing' => nl_edit_view( $id, $b ) );
}

function nl_edit_gate_error( $iss, $where, $field ) {
	$n = array();
	foreach ( (array) $iss as $x ) {
		if ( strpos( (string) $x, 'number:' ) === 0 ) { $n[] = substr( $x, 7 ); }
	}
	if ( $n ) { return new WP_Error( 'nl_edit_gate', 'המספר ' . implode( ', ', array_unique( $n ) ) . ' ' . $where . ' לא מופיע בפרטי הנכס. מעדכנים אותו קודם בפרטים, ואז בטקסט.', array( 'status' => 400, 'field' => $field ) ); }
	if ( in_array( 'link', (array) $iss, true ) ) { return new WP_Error( 'nl_edit_gate', 'אי אפשר לשים קישור ' . $where . '.', array( 'status' => 400, 'field' => $field ) ); }
	return new WP_Error( 'nl_edit_gate', 'יש ' . $where . ' מילה שלא נכנסת לעמוד (למשל "מושלם" או "חלום"). כדאי לכתוב עובדה במקום תואר.', array( 'status' => 400, 'field' => $field ) );
}

/* ---------------- the broker's profile ---------------- */
function nl_edit_profile_view( $b ) {
	return array(
		'name'     => (string) $b['name_he'],
		'brand'    => (string) $b['brand_he'],
		'phone'    => (string) $b['phone'],
		'bio'      => (string) ( $b['bio']['he'] ?? '' ),
		'areas'    => implode( ', ', (array) $b['areas'] ),
		'license'  => (string) $b['license'],
		'portrait' => (string) $b['portrait'],
		'site'     => nl_drop_site_url( $b, 'he' ),
	);
}

function nl_edit_rest_profile( WP_REST_Request $req ) {
	$b = nl_edit_broker( $req );
	if ( is_wp_error( $b ) ) { return $b; }
	return nl_edit_profile_view( $b );
}

function nl_edit_rest_profile_save( WP_REST_Request $req ) {
	$b = nl_edit_broker( $req );
	if ( is_wp_error( $b ) ) { return $b; }
	if ( nl_drop_rate( $b['id'], 'profile', 30, HOUR_IN_SECONDS ) ) { return new WP_Error( 'rate', 'הרבה עדכונים בשעה האחרונה.', array( 'status' => 429 ) ); }
	$d   = (array) $req->get_json_params();
	$pid = (int) $b['id'];
	$s   = function ( $v, $max ) { $v = trim( wp_strip_all_tags( (string) $v ) ); return function_exists( 'mb_substr' ) ? mb_substr( $v, 0, $max ) : substr( $v, 0, $max ); };
	if ( array_key_exists( 'name', $d ) ) {
		$n = $s( $d['name'], 60 );
		if ( $n === '' ) { return new WP_Error( 'nl_edit_name', 'השם לא יכול להיות ריק.', array( 'status' => 400, 'field' => 'name' ) ); }
		update_post_meta( $pid, 'nl_name_he', $n );
	}
	if ( array_key_exists( 'brand', $d ) ) { update_post_meta( $pid, 'company_name', $s( $d['brand'], 80 ) ); }
	if ( array_key_exists( 'phone', $d ) ) {
		$ph = preg_replace( '/[^\d+\-\s]/', '', (string) $d['phone'] );
		if ( strlen( preg_replace( '/\D/', '', $ph ) ) < 9 ) { return new WP_Error( 'nl_edit_phone', 'מספר הטלפון לא נראה תקין.', array( 'status' => 400, 'field' => 'phone' ) ); }
		update_post_meta( $pid, 'phone', trim( $ph ) );
	}
	if ( array_key_exists( 'bio', $d ) ) {
		$bio = $s( $d['bio'], 1200 );
		$iss = function_exists( 'nl_drop_banned_hits' ) ? nl_drop_banned_hits( $bio, 'he' ) : array();
		if ( preg_match( '/https?:|www\./i', $bio ) ) { $iss[] = 'link'; }
		if ( $iss ) { return new WP_Error( 'nl_edit_bio', 'יש בטקסט מילה או קישור שלא נכנסים לאתר. כדאי לכתוב עובדות: ניסיון, אזורים, סוגי נכסים.', array( 'status' => 400, 'field' => 'bio' ) ); }
		update_post_meta( $pid, 'bio', $bio );
	}
	if ( array_key_exists( 'areas', $d ) ) {
		$a = array_slice( array_values( array_filter( array_map( function ( $x ) use ( $s ) { return $s( $x, 40 ); }, preg_split( '/[,\n]+/u', (string) $d['areas'] ) ) ) ), 0, 12 );
		update_post_meta( $pid, 'areas_served', implode( ',', $a ) );
	}
	if ( ! empty( $d['portrait'] ) ) {
		$aid = (int) $d['portrait'];
		if ( (string) get_post_meta( $aid, 'nl_drop_broker', true ) !== (string) $pid || ! wp_attachment_is_image( $aid ) ) { return new WP_Error( 'nl_edit_portrait', 'התמונה לא התקבלה.', array( 'status' => 400 ) ); }
		$rest = array_slice( array_filter( array_map( 'trim', explode( ',', (string) get_post_meta( $pid, 'photos_csv', true ) ) ) ), 1 );
		update_post_meta( $pid, 'photos_csv', implode( ',', array_merge( array( (string) wp_get_attachment_url( $aid ) ), $rest ) ) );
	}
	$b = nl_drop_broker( $pid );
	nl_drop_site_sync( $b );
	// the broker card on every listing built by the engine: the same facts and copy, no model call
	foreach ( nl_drop_broker_listings( $pid, 'he', false ) as $L ) {
		if ( is_array( nl_edit_json( $L['id'], 'nl_facts' ) ) ) { nl_drop_render_all( $L['id'], $b ); nl_drop_purge( nl_drop_listing_ids( $L['id'] ) ); }
	}
	return array( 'ok' => true, 'msg' => 'הפרופיל נשמר, והאתר שלך עודכן.', 'profile' => nl_edit_profile_view( $b ) );
}

/* =====================================================================================================
 * The editor's sheet and script (appended to the private page; uses the page's own colours and font)
 * ===================================================================================================== */
function nl_edit_css() {
	return <<<'NLECSS'
.nle-edit{margin-inline-start:6px}
.nle-film summary{cursor:pointer;font-weight:700;font-size:16px;min-height:44px;display:flex;align-items:center;gap:8px;list-style:none}.nle-film summary::-webkit-details-marker{display:none}.nle-film summary span{display:inline-grid;place-items:center;width:32px;height:32px;border-radius:50%;background:var(--deep);color:#fff;font-size:13px}.nle-film summary em{font-style:normal;color:var(--mute);font-weight:400}.nle-film video{display:block;width:100%;aspect-ratio:16/9;border-radius:12px;background:#000;margin-top:10px}.nle-film .nle-fl{color:var(--mute);font-size:14px;margin:8px 0 0}
.nle-prof{display:flex;gap:12px;align-items:center}
.nle-prof img{width:56px;height:56px;border-radius:50%;object-fit:cover;flex:none;background:var(--sand)}
.nle-prof .t{flex:1;min-width:0}.nle-prof b{display:block;font-size:17px}.nle-prof span{color:var(--mute);font-size:14px}
#nle{position:fixed;inset:0;z-index:50;background:var(--paper);overflow:auto;-webkit-overflow-scrolling:touch}
#nle[hidden]{display:none}
#nle .hd{position:sticky;top:0;z-index:2;background:var(--surf);border-bottom:1px solid var(--line);padding:10px max(16px,env(safe-area-inset-right)) 10px max(16px,env(safe-area-inset-left));display:flex;gap:10px;align-items:center}
#nle .hd b{flex:1;min-width:0;font-size:17px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#nle .in{max-width:720px;margin:0 auto;padding:16px max(16px,env(safe-area-inset-right)) 120px max(16px,env(safe-area-inset-left));display:grid;gap:14px}
.nle-card{background:var(--surf);border:1px solid var(--line);border-radius:14px;padding:14px}
.nle-seg{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}
.nle-seg button{min-height:48px;border-radius:10px;border:1.5px solid var(--line);background:var(--surf);color:var(--ink);font:600 15px inherit;cursor:pointer}
.nle-seg button[aria-pressed="true"]{background:var(--deep);border-color:var(--deep);color:#fff}
.nle-row{display:flex;align-items:center;gap:12px;width:100%;min-height:64px;padding:12px 14px;border:1px solid var(--line);border-radius:14px;background:var(--surf);color:var(--ink);text-align:start;font:inherit;cursor:pointer}
.nle-row:focus-visible,.nle-seg button:focus-visible,.nle-btn:focus-visible,.nle-chip:focus-visible,.nle-ph button:focus-visible{outline:3px solid var(--sea);outline-offset:2px}
.nle-row .k{flex:1;min-width:0}.nle-row .k b{display:block;font-size:16px}.nle-row .k span{display:block;color:var(--mute);font-size:14px;margin-top:2px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.nle-row .go{color:var(--sea);font-weight:700;font-size:14px;flex:none}
.nle-miss{display:block;width:100%;text-align:start;border:1px dashed var(--warn);background:transparent;color:var(--warn);border-radius:12px;padding:10px 12px;font:600 14px inherit;cursor:pointer;min-height:44px}
.nle-btn{min-height:48px;padding:10px 18px;border-radius:12px;border:1.5px solid var(--deep);background:var(--deep);color:#fff;font:700 16px inherit;cursor:pointer}
.nle-btn.ghost{background:transparent;color:var(--deep)}
.nle-btn[disabled]{opacity:.55;cursor:default}
#nles{position:fixed;inset:0;z-index:60;background:rgba(10,20,26,.5);display:flex;align-items:flex-end;justify-content:center}
#nles[hidden]{display:none}
#nles .sh{background:var(--surf);width:min(720px,100%);max-height:94vh;display:flex;flex-direction:column;border-radius:18px 18px 0 0}
#nles .sh-h{padding:14px 16px;border-bottom:1px solid var(--line);font-size:18px;font-weight:700}
#nles .sh-b{padding:14px 16px;overflow:auto;display:grid;gap:14px}
#nles .sh-f{padding:12px 16px calc(12px + env(safe-area-inset-bottom));border-top:1px solid var(--line);display:flex;gap:10px}
#nles .sh-f .nle-btn{flex:1}
.nle-f{display:grid;gap:6px}
.nle-f label,.nle-f .lb{font-weight:700;font-size:15px}
.nle-f input,.nle-f select,.nle-f textarea{width:100%;min-height:48px;border:1.5px solid var(--line);border-radius:10px;padding:10px 12px;font:400 17px inherit;background:var(--surf);color:var(--ink)}
.nle-f textarea{min-height:110px;line-height:1.55}
.nle-f input:focus,.nle-f select:focus,.nle-f textarea:focus{border-color:var(--sea);outline:none;box-shadow:0 0 0 3px rgba(47,111,134,.25)}
.nle-f .hint{color:var(--mute);font-size:13px}
.nle-f .err{color:var(--bad);font-size:14px;font-weight:600}
.nle-f[data-bad] input,.nle-f[data-bad] textarea{border-color:var(--bad)}
.nle-two{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.nle-chips{display:flex;flex-wrap:wrap;gap:8px}
.nle-chip{min-height:46px;padding:8px 14px;border-radius:999px;border:1.5px solid var(--line);background:var(--surf);color:var(--ink);font:600 15px inherit;cursor:pointer}
.nle-chip[aria-pressed="true"]{background:var(--sand);border-color:var(--deep);color:var(--deep)}
.nle-chip[aria-pressed="true"]::before{content:"✓ "}
.nle-ph{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;list-style:none;margin:0;padding:0}
.nle-ph li{position:relative;aspect-ratio:1;border-radius:10px;overflow:hidden;background:var(--sand);touch-action:manipulation}
.nle-ph li.drag{opacity:.45}
.nle-ph li img{width:100%;height:100%;object-fit:cover;display:block;pointer-events:none}
.nle-ph li button{position:absolute;inset:0;width:100%;height:100%;background:transparent;border:0;cursor:pointer}
.nle-ph li .cov{position:absolute;top:6px;right:6px;background:var(--deep);color:#fff;font-size:12px;font-weight:700;padding:3px 8px;border-radius:999px;pointer-events:none}
.nle-ph li .up{position:absolute;inset:auto 0 0 0;height:5px;background:var(--sea)}
.nle-ph li.add label{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;width:100%;height:100%;border:2px dashed var(--line);border-radius:10px;color:var(--deep);font-weight:700;font-size:14px;cursor:pointer;text-align:center}
.nle-acts{display:grid;gap:8px}
.nle-acts .nle-btn{width:100%}
#nlet{position:fixed;inset-inline:0;top:calc(74px + env(safe-area-inset-top));z-index:70;display:flex;justify-content:center;pointer-events:none;padding:0 16px}
#nlet div{pointer-events:auto;background:var(--ink);color:var(--paper);border-radius:12px;padding:12px 14px;display:flex;gap:12px;align-items:center;max-width:640px;font-size:15px;box-shadow:0 6px 24px rgba(0,0,0,.25)}
#nlet a,#nlet button{color:var(--paper);font-weight:700;background:none;border:0;text-decoration:underline;font:700 15px inherit;cursor:pointer;min-height:44px}
#nlew{position:fixed;inset:0;z-index:80;background:rgba(247,246,242,.92);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;padding:24px;text-align:center}
#nlew[hidden]{display:none}
#nlew i{width:46px;height:46px;border-radius:50%;border:4px solid var(--line);border-top-color:var(--deep);animation:nlesp 1s linear infinite}
#nlew p{max-width:34ch;font-size:17px;line-height:1.5;color:var(--ink)}
@keyframes nlesp{to{transform:rotate(360deg)}}
@media (prefers-reduced-motion:reduce){#nlew i{animation:none}}
NLECSS;
}

function nl_edit_js() {
	return <<<'NLEJS'
(function(){
var C=window.NLEDIT||{},API=C.api;if(!API)return;
var $=function(s,r){return (r||document).querySelector(s)},esc=function(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})};
var TYPES={apartment:'דירה',penthouse:'פנטהאוז',mini_penthouse:'מיני פנטהאוז',garden:'דירת גן',duplex:'דופלקס',villa:'וילה',cottage:'קוטג׳',studio:'סטודיו',other:'אחר'};
var CONDS={new:'חדשה',renovated:'משופצת',good:'במצב טוב',needs_renovation:'דורשת שיפוץ'};
var FEATS=[['parking','חניה'],['storage','מחסן'],['elevator','מעלית'],['protected_room','ממ״ד'],['ac','מיזוג'],['furnished','מרוהטת'],['exclusive','בלעדיות']];
function req(m,p,b){return fetch(API+p,{method:m,headers:b?{'Content-Type':'application/json'}:{},body:b?JSON.stringify(b):undefined,credentials:'omit'}).then(function(r){return r.json().catch(function(){return{}}).then(function(j){return{ok:r.ok,j:j}})}).catch(function(){return{ok:false,j:{message:'אין חיבור כרגע. השינויים שלכם שמורים בטלפון, אפשר לנסות שוב.'}}})}
function fmt(n){return n==null||n===''?'':Number(n).toLocaleString('he-IL')}
/* ---------- toast with undo ---------- */
var tw=document.createElement('div');tw.id='nlet';tw.setAttribute('role','status');tw.setAttribute('aria-live','polite');document.body.appendChild(tw);var tT=0;
function toast(msg,link,undo){clearTimeout(tT);tw.innerHTML='';var d=document.createElement('div');var s=document.createElement('span');s.textContent=msg;d.appendChild(s);
 if(link){var a=document.createElement('a');a.href=link;a.target='_blank';a.rel='noopener';a.textContent='צפייה בעמוד';d.appendChild(a);}
 if(undo){var u=document.createElement('button');u.type='button';u.textContent='ביטול';u.onclick=function(){tw.innerHTML='';undo();};d.appendChild(u);}
 tw.appendChild(d);tT=setTimeout(function(){tw.innerHTML=''},undo?9000:7000);}
/* ---------- waiting cover ---------- */
var wait=document.createElement('div');wait.id='nlew';wait.hidden=true;wait.innerHTML='<i aria-hidden="true"></i><p></p>';wait.setAttribute('role','status');document.body.appendChild(wait);
function busy(t){if(t){$('p',wait).textContent=t;wait.hidden=false}else wait.hidden=true}
/* ---------- the editor page ---------- */
var ed=document.createElement('div');ed.id='nle';ed.hidden=true;ed.setAttribute('role','dialog');ed.setAttribute('aria-modal','true');ed.setAttribute('aria-labelledby','nle-t');document.body.appendChild(ed);
var sh=document.createElement('div');sh.id='nles';sh.hidden=true;document.body.appendChild(sh);
var L=null,opener=null,dirty=false;
function closeEd(){ed.hidden=true;document.documentElement.style.overflow='';L=null;if(window.__nleReload)window.__nleReload();if(opener)try{opener.focus()}catch(e){}}
function head(title,url){return '<div class="hd"><button type="button" class="nle-btn ghost" data-x>חזרה</button><b id="nle-t">'+esc(title)+'</b>'+(url?'<a class="nle-btn ghost" href="'+esc(url)+'" target="_blank" rel="noopener">צפייה</a>':'')+'</div>'}
function summary(f){if(!f)return'';var p=[];p.push(f.listing_type==='rent'?'להשכרה':'למכירה');if(f.property_type&&f.property_type!=='other')p.push(TYPES[f.property_type]);if(f.area_he||f.city_he)p.push([f.area_he,f.city_he].filter(Boolean).join(', '));if(f.rooms)p.push(f.rooms+' חד׳');if(f.size_sqm)p.push(f.size_sqm+' מ״ר');if(f.floor!=null)p.push('קומה '+f.floor+(f.total_floors?' מתוך '+f.total_floors:''));return p.join(' · ')}
function feats(f){var p=[];FEATS.forEach(function(x){if(f&&f[x[0]])p.push(x[0]==='parking'&&f.parking_count?f.parking_count+' חניות':x[1])});if(f&&f.view_he)p.push(f.view_he);return p.length?p.join(' · '):'לא מולא'}
function renderEd(){
 var f=L.facts||{},off=f.listing_type==='rent'?'rented':'sold',offL=f.listing_type==='rent'?'הושכר':'נמכר';
 var h=head(L.title,L.url)+'<div class="in">';
 if(L.pending)h+='<p class="nle-card" role="note"><b>המודעה מוכנה לעריכה.</b><br>מה שתשנו יעלה לאתר ברגע שתלחצו "שמירה". עד אז העמוד באתר נשאר כפי שהוא.</p>';
 h+='<div class="nle-card"><div class="lb" style="font-weight:700;margin-bottom:8px">מצב המודעה</div><div class="nle-seg" role="group" aria-label="מצב המודעה">'+
  '<button type="button" data-st="active" aria-pressed="'+(L.status==='active')+'">באוויר</button>'+
  '<button type="button" data-st="'+off+'" aria-pressed="'+(L.status===off)+'">'+offL+'</button>'+
  '<button type="button" data-st="active" data-back aria-pressed="false"'+(L.status==='active'?' disabled':'')+'>חזרה לשוק</button></div></div>';
 if(L.missing&&L.missing.length)h+='<button type="button" class="nle-miss" data-miss="'+esc(L.missing[0].k)+'">חסרים '+L.missing.length+' פרטים: '+esc(L.missing.map(function(x){return x.w}).join(', '))+' · להשלמה</button>';
 var rows=[['price','מחיר',f.price?fmt(f.price)+' ₪'+(f.listing_type==='rent'?' לחודש':''):'לא מולא'],['photos','תמונות',L.photos.length+' תמונות'+(L.photos.length?' · הראשונה היא התמונה הראשית':'')],
  ['details','פרטי הנכס',summary(f)||'לא מולא'],['features','מה יש בנכס',feats(f)],['more','כניסה והערות',[f.entry_he?'כניסה: '+f.entry_he:'',f.notes_he||''].filter(Boolean).join(' · ')||'לא מולא'],
  ['text','התיאור בעמוד',(L.text&&L.text.title)||'']];
 rows.forEach(function(r){h+='<button type="button" class="nle-row" data-sec="'+r[0]+'"><span class="k"><b>'+r[1]+'</b><span>'+esc(r[2])+'</span></span><span class="go">עריכה</span></button>'});
 h+='<p class="hint" style="color:var(--mute);font-size:13px;text-align:center">עודכן לפני '+esc(L.modified)+'. כל שינוי מופיע באתר בכל השפות של המודעה.</p></div>';
 ed.innerHTML=h;
 $('[data-x]',ed).onclick=closeEd;
 ed.querySelectorAll('[data-st]').forEach(function(b){b.onclick=function(){if(b.getAttribute('aria-pressed')==='true')return;setStatus(b.dataset.st)}});
 ed.querySelectorAll('[data-sec]').forEach(function(b){b.onclick=function(){openSec(b.dataset.sec,null,b)}});
 var m=$('[data-miss]',ed);if(m)m.onclick=function(){var k=m.dataset.miss;openSec(k==='price'?'price':(k==='entry_he'?'more':'details'),k,m)};
}
function openListing(id,btn){opener=btn||null;busy('פותחים את המודעה…');req('GET','/edit/listing/'+id).then(function(r){
 if(!r.ok){busy();toast(r.j.message||'לא הצלחנו לפתוח.');return}
 var go=function(d){busy();L=d;ed.hidden=false;document.documentElement.style.overflow='hidden';renderEd();$('[data-x]',ed).focus()};
 if(r.j.ready||r.j.pending){go(r.j);return}
 busy('מכינים את המודעה לעריכה: קוראים את הפרטים והתמונות מהעמוד. זה לוקח עד שתי דקות, ורק פעם אחת.');
 req('POST','/edit/prepare/'+id,{}).then(function(p){if(!p.ok){busy();toast(p.j.message||'לא הצלחנו להכין את המודעה.');return}go(p.j)})})}
function setStatus(st){var prev=L.status;busy('מעדכנים…');save('status',{status:st},null,function(){toast(st==='active'?'המודעה באוויר.':(st==='sold'?'המודעה סומנה כנמכרה.':'המודעה סומנה כמושכרת.'),L.url,function(){save('status',{status:prev},null,function(){toast('בוטל.')})})},true)}
/* ---------- save ---------- */
function save(sec,data,form,done,quiet,waitText){
 if(waitText)busy(waitText);else if(!quiet)busy('שומרים…');
 req('POST','/edit/listing/'+L.id,{section:sec,data:data}).then(function(r){busy();
  if(!r.ok){var m=(r.j&&r.j.message)||'לא הצלחנו לשמור כרגע.';var fld=r.j&&r.j.data&&r.j.data.field;
   if(form&&fld){var w=form.querySelector('[data-f="'+fld+'"]')||form.querySelector('[data-f]');if(w){w.setAttribute('data-bad','');var e=w.querySelector('.err');if(e)e.textContent=m;var i=w.querySelector('input,textarea,select');if(i)i.focus()}}
   toast(m);return}
  L=r.j.listing;try{localStorage.removeItem('nle:'+L.id+':'+sec)}catch(e){}
  renderEd();if(sec!=='photos')closeSheet(true);if(done)done();else toast(r.j.msg||'נשמר.',L.url)})}
/* ---------- the sheet ---------- */
var shOpener=null;
function closeSheet(force){if(!force&&dirty&&!window.confirm){}sh.hidden=true;sh.innerHTML='';dirty=false;if(shOpener)try{shOpener.focus()}catch(e){}}
function sheet(title,body,onSave,saveLbl){
 sh.innerHTML='<div class="sh" role="dialog" aria-modal="true" aria-labelledby="nle-sh-t"><div class="sh-h" id="nle-sh-t">'+esc(title)+'</div><form class="sh-b" novalidate>'+body+'</form><div class="sh-f"><button type="button" class="nle-btn" data-save>'+(saveLbl||'שמירה')+'</button><button type="button" class="nle-btn ghost" data-cancel>ביטול</button></div></div>';
 sh.hidden=false;var form=$('form',sh);dirty=false;
 form.addEventListener('input',function(){dirty=true;form.querySelectorAll('[data-bad]').forEach(function(w){w.removeAttribute('data-bad');var e=w.querySelector('.err');if(e)e.textContent=''})});
 $('[data-cancel]',sh).onclick=function(){if(dirty){askLeave(function(){closeSheet(true)},function(){onSave(form)})}else closeSheet(true)};
 $('[data-save]',sh).onclick=function(){onSave(form)};
 form.addEventListener('submit',function(e){e.preventDefault();onSave(form)});
 sh.onclick=function(e){if(e.target===sh)$('[data-cancel]',sh).click()};
 var first=form.querySelector('input,select,textarea,button');if(first)first.focus();return form}
function askLeave(leave,keep){var box=document.createElement('div');box.className='nle-card';box.setAttribute('role','alertdialog');box.innerHTML='<p style="margin:0 0 10px;font-weight:700">יש שינויים שלא נשמרו. לשמור לפני שיוצאים?</p><div class="nle-acts"><button type="button" class="nle-btn" data-k>שמירה</button><button type="button" class="nle-btn ghost" data-l>לצאת בלי לשמור</button></div>';
 var b=$('.sh-b',sh);b.insertBefore(box,b.firstChild);$('[data-k]',box).onclick=function(){box.remove();keep()};$('[data-l]',box).onclick=function(){box.remove();leave()};$('[data-k]',box).focus()}
function fld(k,label,input,hint){return '<div class="nle-f" data-f="'+k+'"><label for="nle-'+k+'">'+label+'</label>'+input+(hint?'<span class="hint">'+hint+'</span>':'')+'<span class="err" aria-live="polite"></span></div>'}
function num(k,label,v,hint,ph){return fld(k,label,'<input id="nle-'+k+'" name="'+k+'" inputmode="decimal" autocomplete="off" value="'+esc(v==null?'':fmt(v))+'" placeholder="'+esc(ph||'')+'">',hint)}
function txt(k,label,v,hint,ph){return fld(k,label,'<input id="nle-'+k+'" name="'+k+'" value="'+esc(v||'')+'" placeholder="'+esc(ph||'')+'">',hint)}
function sel(k,label,v,opts){var o='<option value="">לבחור</option>';Object.keys(opts).forEach(function(x){o+='<option value="'+x+'"'+(x===v?' selected':'')+'>'+opts[x]+'</option>'});return fld(k,label,'<select id="nle-'+k+'" name="'+k+'">'+o+'</select>')}
function draft(sec,form){var key='nle:'+L.id+':'+sec;try{var d=JSON.parse(localStorage.getItem(key)||'null');if(d)Object.keys(d).forEach(function(n){var i=form.elements[n];if(i&&i.type!=='button')i.value=d[n]})}catch(e){}
 form.addEventListener('input',function(){var o={};Array.prototype.forEach.call(form.elements,function(i){if(i.name)o[i.name]=i.value});try{localStorage.setItem(key,JSON.stringify(o))}catch(e){}})}
function val(form,n){var i=form.elements[n];return i?i.value.trim():''}
function numv(form,n){var v=val(form,n).replace(/[,\s₪]/g,'');return v===''?null:v}
function openSec(sec,focusKey,btn){shOpener=btn||null;var f=L.facts||{},form;
 if(sec==='price'){
  form=sheet('מחיר',num('price',f.listing_type==='rent'?'שכר דירה לחודש (₪)':'מחיר (₪)',f.price,f.price?'המחיר הנוכחי: '+fmt(f.price)+' ₪':'אפשר להשאיר ריק, ואז בעמוד יופיע "מחיר בפנייה".','למשל 2,450,000'),function(fm){save('price',{price:numv(fm,'price')},fm)});draft('price',form);
  var pi=form.elements.price;pi.addEventListener('input',function(){var d=pi.value.replace(/\D/g,'');pi.value=d?Number(d).toLocaleString('he-IL'):''});
 }else if(sec==='details'){
  form=sheet('פרטי הנכס','<div class="nle-f" data-f="listing_type"><span class="lb">סוג העסקה</span><div class="nle-chips" role="group" aria-label="סוג העסקה"><button type="button" class="nle-chip" data-deal="sale" aria-pressed="'+(f.listing_type!=='rent')+'">למכירה</button><button type="button" class="nle-chip" data-deal="rent" aria-pressed="'+(f.listing_type==='rent')+'">להשכרה</button></div><input type="hidden" name="listing_type" value="'+(f.listing_type==='rent'?'rent':'sale')+'"><span class="err"></span></div>'+
   sel('property_type','סוג הנכס',f.property_type,TYPES)+'<div class="nle-two">'+txt('area_he','שכונה',f.area_he,'','למשל נופי ים')+txt('city_he','עיר',f.city_he,'','למשל תל אביב')+'</div>'+
   txt('street_he','רחוב (לא מוצג באתר)',f.street_he,'הכתובת המלאה נשמרת אצלנו ולא מתפרסמת.')+'<div class="nle-two">'+num('rooms','חדרים',f.rooms,'','4.5')+num('size_sqm','מ״ר',f.size_sqm,'','110')+'</div>'+
   '<div class="nle-two">'+num('floor','קומה',f.floor,'0 = קרקע','5')+num('total_floors','מתוך',f.total_floors,'קומות בבניין','8')+'</div><div class="nle-two">'+num('balcony_sqm','מרפסת (מ״ר)',f.balcony_sqm,'','12')+num('garden_sqm','גינה (מ״ר)',f.garden_sqm,'','')+'</div>'+
   sel('condition','מצב הנכס',f.condition,CONDS)+'<p class="hint" style="color:var(--mute);font-size:13px;margin:0">אחרי השמירה העמוד נכתב מחדש לפי הפרטים, בכל השפות. זה לוקח עד דקה.</p>',
   function(fm){var d={};['listing_type','property_type','area_he','city_he','street_he','condition'].forEach(function(n){d[n]=val(fm,n)});['rooms','size_sqm','floor','total_floors','balcony_sqm','garden_sqm'].forEach(function(n){d[n]=numv(fm,n)});
    save('facts',{facts:d},fm,null,false,'כותבים את העמוד לפי הפרטים שנתתם, בכל השפות. זה לוקח עד דקה.')});
  form.querySelectorAll('[data-deal]').forEach(function(b){b.onclick=function(){form.querySelectorAll('[data-deal]').forEach(function(x){x.setAttribute('aria-pressed',x===b)});form.elements.listing_type.value=b.dataset.deal;dirty=true}});draft('details',form);
 }else if(sec==='features'){
  var ch='';FEATS.forEach(function(x){ch+='<button type="button" class="nle-chip" data-feat="'+x[0]+'" aria-pressed="'+(!!f[x[0]])+'">'+x[1]+'</button>'});
  form=sheet('מה יש בנכס','<div class="nle-f"><span class="lb">נגיעה מסמנת, נגיעה נוספת מבטלת</span><div class="nle-chips" role="group" aria-label="מה יש בנכס">'+ch+'</div></div>'+num('parking_count','כמה חניות',f.parking_count,'','2')+txt('view_he','נוף',f.view_he,'רק אם יש: למשל נוף לים','')+
   fld('features_he','עוד דברים שכדאי לדעת','<textarea id="nle-features_he" name="features_he" rows="4" placeholder="שורה לכל דבר, למשל: מטבח שף חדש">'+esc((f.features_he||[]).join('\n'))+'</textarea>','עד 8 שורות. מספר שלא מופיע בפרטים לא ייכנס לעמוד.'),
   function(fm){var d={};fm.querySelectorAll('[data-feat]').forEach(function(b){d[b.dataset.feat]=b.getAttribute('aria-pressed')==='true'});d.parking_count=numv(fm,'parking_count');d.view_he=val(fm,'view_he');d.features_he=val(fm,'features_he').split('\n').map(function(s){return s.trim()}).filter(Boolean);
    save('facts',{facts:d},fm,null,false,'כותבים את העמוד לפי הפרטים שנתתם, בכל השפות. זה לוקח עד דקה.')});
  form.querySelectorAll('[data-feat]').forEach(function(b){b.onclick=function(){b.setAttribute('aria-pressed',b.getAttribute('aria-pressed')!=='true');dirty=true}});
 }else if(sec==='more'){
  form=sheet('כניסה והערות',txt('entry_he','מתי אפשר להיכנס',f.entry_he,'למשל: כניסה מיידית, או אוגוסט 2027')+fld('notes_he','הערות קצרות','<textarea id="nle-notes_he" name="notes_he" rows="4">'+esc(f.notes_he||'')+'</textarea>','עד 320 תווים.'),
   function(fm){save('facts',{facts:{entry_he:val(fm,'entry_he'),notes_he:val(fm,'notes_he')}},fm,null,false,'כותבים את העמוד לפי הפרטים שנתתם, בכל השפות. זה לוקח עד דקה.')});draft('more',form);
 }else if(sec==='text'){
  var t=L.text||{title:'',dek:'',story:[]},st=(t.story||[]).concat(['','','']).slice(0,3);
  form=sheet('התיאור בעמוד',fld('title','כותרת','<input id="nle-title" name="title" maxlength="90" value="'+esc(t.title)+'">','עד 90 תווים')+fld('dek','פתיח','<textarea id="nle-dek" name="dek" rows="4" maxlength="460">'+esc(t.dek)+'</textarea>','שתיים-שלוש שורות שמופיעות בראש העמוד')+
   st.map(function(p,i){return fld('story','פסקה '+(i+1),'<textarea id="nle-story'+i+'" name="story'+i+'" rows="5" maxlength="800">'+esc(p)+'</textarea>',i?'אפשר להשאיר ריק':'')}).join('')+
   '<p class="hint" style="color:var(--mute);font-size:13px;margin:0">העברית נשמרת כפי שכתבתם. מספרים בטקסט צריכים להתאים לפרטי הנכס. האנגלית ושאר השפות נכתבות מחדש לפי הטקסט שלכם.</p>',
   function(fm){save('text',{title:val(fm,'title'),dek:val(fm,'dek'),story:[val(fm,'story0'),val(fm,'story1'),val(fm,'story2')]},fm,null,false,'שומרים את הטקסט ומעדכנים את שאר השפות. זה לוקח עד דקה.')});draft('text',form);
 }else if(sec==='photos'){photos();return}
 if(focusKey){var i=form.querySelector('[name="'+focusKey+'"]');if(i)i.focus()}}
/* ---------- the photo manager ---------- */
function photos(){
 var ids=L.photos.map(function(p){return p.id}),urls={};L.photos.forEach(function(p){urls[p.id]=p.url});
 sheet('תמונות','<p class="hint" style="margin:0;color:var(--mute);font-size:14px">התמונה הראשונה היא התמונה הראשית. נגיעה בתמונה פותחת פעולות. אפשר גם ללחוץ ארוכה ולגרור.</p><ul class="nle-ph" id="nle-ph" aria-label="תמונות המודעה"></ul><div id="nle-pa"></div>',function(){commit(true)},'סיום');
 var ul=$('#nle-ph',sh),pa=$('#nle-pa',sh);
 function commit(close){if(close){closeSheet(true);return}}
 function persist(prev,msg){save('photos',{ids:ids},null,function(){toast(msg||'התמונות נשמרו.',L.url,prev?function(){ids=prev.slice();persist(null,'בוטל.')}:null);if(!sh.hidden)draw()},true)}
 function draw(){ul.innerHTML='';
  ids.forEach(function(id,i){var li=document.createElement('li');li.dataset.id=id;li.innerHTML='<img alt="" src="'+esc(urls[id]||'')+'">'+(i===0?'<span class="cov">תמונה ראשית</span>':'')+'<button type="button" aria-label="תמונה '+(i+1)+' מתוך '+ids.length+(i===0?', תמונה ראשית':'')+'. פעולות"></button>';
   $('button',li).onclick=function(){if(Date.now()-justDragged<400)return;acts(id)};dragable(li);ul.appendChild(li)});
  var add=document.createElement('li');add.className='add';add.innerHTML='<label><input type="file" accept="image/*" multiple hidden><span style="font-size:26px" aria-hidden="true">+</span>הוספת תמונות</label>';
  $('input',add).onchange=function(e){upload(Array.prototype.slice.call(e.target.files))};ul.appendChild(add)}
 function acts(id){var i=ids.indexOf(id);pa.innerHTML='<div class="nle-card nle-acts" role="group" aria-label="פעולות לתמונה '+(i+1)+'"><b>תמונה '+(i+1)+'</b>'+
  (i?'<button type="button" class="nle-btn" data-a="cover">הפוך לתמונה ראשית</button>':'')+(i?'<button type="button" class="nle-btn ghost" data-a="fw">הזזה קדימה</button>':'')+(i<ids.length-1?'<button type="button" class="nle-btn ghost" data-a="bw">הזזה אחורה</button>':'')+
  (ids.length>1?'<button type="button" class="nle-btn ghost" data-a="del" style="color:var(--bad);border-color:var(--bad)">מחיקה</button>':'')+'<button type="button" class="nle-btn ghost" data-a="x">סגירה</button></div>';
  pa.querySelectorAll('[data-a]').forEach(function(b){b.onclick=function(){var prev=ids.slice(),a=b.dataset.a;
   pa.innerHTML='';if(a==='x')return;
   if(a==='cover'){ids.splice(i,1);ids.unshift(id);persist(prev,'התמונה הראשית הוחלפה.')}
   if(a==='fw'){ids.splice(i,1);ids.splice(i-1,0,id);persist(prev,'הסדר נשמר.')}
   if(a==='bw'){ids.splice(i,1);ids.splice(i+1,0,id);persist(prev,'הסדר נשמר.')}
   if(a==='del'){ids.splice(i,1);persist(prev,'התמונה נמחקה מהמודעה.')}
   draw()}});var f=pa.querySelector('[data-a]');if(f)f.focus()}
 var dragging=null,justDragged=0;
 function dragable(li){var t=0,sx=0,sy=0;
  li.addEventListener('touchmove',function(e){if(dragging)e.preventDefault()},{passive:false});
  li.addEventListener('pointerdown',function(e){if(e.button>0)return;sx=e.clientX;sy=e.clientY;clearTimeout(t);
   var off=function(){document.removeEventListener('pointermove',cancel);document.removeEventListener('pointerup',stop);document.removeEventListener('pointercancel',stop)};
   var cancel=function(ev){if(Math.hypot(ev.clientX-sx,ev.clientY-sy)>8){clearTimeout(t);off()}};
   var stop=function(){clearTimeout(t);off()};
   document.addEventListener('pointermove',cancel);document.addEventListener('pointerup',stop);document.addEventListener('pointercancel',stop);
   t=setTimeout(function(){off();start(li)},320)})}
 function start(li){var prev=ids.slice();dragging=li;li.classList.add('drag');if(navigator.vibrate)try{navigator.vibrate(15)}catch(e){}
  var mv=function(e){e.preventDefault();var el=document.elementFromPoint(e.clientX,e.clientY),to=el&&el.closest&&el.closest('.nle-ph li[data-id]');
   if(to&&to!==li){var all=Array.prototype.slice.call(ul.querySelectorAll('li[data-id]')),a=all.indexOf(li),z=all.indexOf(to);ul.insertBefore(li,a<z?to.nextSibling:to)}};
  var up=function(){document.removeEventListener('pointermove',mv);document.removeEventListener('pointerup',up);document.removeEventListener('pointercancel',up);
   dragging=null;justDragged=Date.now();li.classList.remove('drag');ids=Array.prototype.map.call(ul.querySelectorAll('li[data-id]'),function(x){return +x.dataset.id});
   if(prev.join()!==ids.join())persist(prev,'הסדר נשמר.');draw()};
  document.addEventListener('pointermove',mv,{passive:false});document.addEventListener('pointerup',up);document.addEventListener('pointercancel',up)}
 function shrink(file){return new Promise(function(ok){if(!/^image\/(jpeg|png|webp)/.test(file.type)){ok(file);return}var img=new Image(),u=URL.createObjectURL(file);img.onload=function(){var m=2400,w=img.naturalWidth,h=img.naturalHeight,k=Math.min(1,m/Math.max(w,h));if(k===1&&file.size<3e6){URL.revokeObjectURL(u);ok(file);return}
  var c=document.createElement('canvas');c.width=Math.round(w*k);c.height=Math.round(h*k);c.getContext('2d').drawImage(img,0,0,c.width,c.height);URL.revokeObjectURL(u);c.toBlob(function(b){ok(b?new File([b],'photo.jpg',{type:'image/jpeg'}):file)},'image/jpeg',.86)};img.onerror=function(){ok(file)};img.src=u})}
 function upload(files){if(!files.length)return;var prev=ids.slice(),n=0;busy('מעלים '+files.length+' תמונות…');
  var next=function(){if(!files.length){busy();if(n)persist(prev,n+' תמונות נוספו.');return}var f=files.shift();shrink(f).then(function(file){var fd=new FormData();fd.append('photo',file,file.name||'photo.jpg');
   return fetch(API+'/photo',{method:'POST',body:fd,credentials:'omit'}).then(function(r){return r.json()}).then(function(j){if(j&&j.id){ids.push(j.id);urls[j.id]=j.url;n++}else toast((j&&j.message)||'תמונה אחת לא עלתה.')})}).catch(function(){toast('תמונה אחת לא עלתה. אפשר לנסות שוב.')}).then(function(){busy('מעלים… נשארו '+files.length);next()})};next()}
 draw()}
/* ---------- the how-to film, folded, at the top ---------- */
if(C.film&&C.film.src){var main=document.querySelector('main.wrap'),hf=document.createElement('details');hf.className='card nle-film';
 hf.innerHTML='<summary><span aria-hidden="true">▶</span> סרטון הדרכה: איך מנהלים את המודעות <em>('+esc(C.film.len||'')+')</em></summary><video controls playsinline preload="none" poster="'+esc(C.film.poster)+'"><source src="'+esc(C.film.src)+'" type="video/mp4"></video><p class="nle-fl">נכס חדש, נמכר או הושכר, מחיר, תמונות, פרטים, תיאור ופרופיל, שלב אחרי שלב.</p>';
 hf.addEventListener('toggle',function(){var vd=hf.querySelector('video');if(hf.open){try{vd.play()}catch(e){}}else vd.pause()});
 if(main)main.insertBefore(hf,main.firstChild)}
/* ---------- the profile ---------- */
var mineSec=document.getElementById('h-mine');
var pc=document.createElement('section');pc.className='card';pc.setAttribute('aria-labelledby','nle-pt');pc.innerHTML='<h2 id="nle-pt">הפרופיל שלי</h2><div class="nle-prof"><img alt="" id="nle-pimg"><div class="t"><b id="nle-pn"></b><span id="nle-pb"></span></div><button type="button" class="nle-btn ghost" id="nle-pe">עריכה</button></div>';
if(mineSec&&mineSec.closest('section'))mineSec.closest('section').parentNode.insertBefore(pc,mineSec.closest('section'));
var P=null;function loadP(){req('GET','/edit/profile').then(function(r){if(!r.ok)return;P=r.j;$('#nle-pn').textContent=P.name;$('#nle-pb').textContent=[P.brand,P.phone].filter(Boolean).join(' · ');var im=$('#nle-pimg');if(P.portrait)im.src=P.portrait;else im.removeAttribute('src')})}loadP();
$('#nle-pe',pc).onclick=function(){if(!P)return;shOpener=this;var port=null;
 var form=sheet('הפרופיל שלי','<div class="nle-prof"><img alt="" id="nle-pi" src="'+esc(P.portrait)+'"><label class="nle-btn ghost" style="display:inline-flex;align-items:center">החלפת תמונה<input type="file" accept="image/*" hidden id="nle-pf"></label></div>'+
  txt('name','השם כפי שיופיע באתר',P.name)+txt('brand','שם המשרד',P.brand)+fld('phone','טלפון לוואטסאפ ולשיחות','<input id="nle-phone" name="phone" type="tel" inputmode="tel" value="'+esc(P.phone)+'">','הכפתורים באתר ובכל המודעות יעברו למספר הזה.')+
  fld('bio','קצת עליי','<textarea id="nle-bio" name="bio" rows="6" maxlength="1200">'+esc(P.bio)+'</textarea>','עובדות עובדות טובות יותר מתארים: ניסיון, אזורים, סוגי נכסים.')+fld('areas','אזורי פעילות','<input id="nle-areas" name="areas" value="'+esc(P.areas)+'">','מופרדים בפסיק, למשל: נופי ים, רמת אביב, הרצליה פיתוח')+
  '<p class="hint" style="color:var(--mute);font-size:13px;margin:0">מספר הרישיון: '+esc(P.license||'—')+'. לשינוי שם או רישיון אפשר לכתוב לנו.</p>',
  function(fm){busy('שומרים ומעדכנים את האתר שלכם…');req('POST','/edit/profile',{name:val(fm,'name'),brand:val(fm,'brand'),phone:val(fm,'phone'),bio:val(fm,'bio'),areas:val(fm,'areas'),portrait:port}).then(function(r){busy();
   if(!r.ok){var w=fm.querySelector('[data-f="'+((r.j.data&&r.j.data.field)||'')+'"]');if(w){w.setAttribute('data-bad','');w.querySelector('.err').textContent=r.j.message}toast(r.j.message||'לא נשמר.');return}
   closeSheet(true);loadP();toast(r.j.msg||'נשמר.',P.site)})});
 $('#nle-pf',sh).onchange=function(e){var f=e.target.files[0];if(!f)return;busy('מעלים את התמונה…');var fd=new FormData();fd.append('photo',f,f.name);fetch(API+'/photo',{method:'POST',body:fd,credentials:'omit'}).then(function(r){return r.json()}).then(function(j){busy();if(j&&j.id){port=j.id;$('#nle-pi',sh).src=j.url;dirty=true}else toast((j&&j.message)||'התמונה לא עלתה.')}).catch(function(){busy();toast('התמונה לא עלתה.')})}};
/* ---------- the "my listings" list gets "עריכה" ---------- */
var mine=document.getElementById('mine'),map={};
function mark(){if(!mine)return;mine.querySelectorAll('li').forEach(function(li){if(li.querySelector('.nle-edit'))return;var a=li.querySelector('a[href]');if(!a)return;var row=map[a.href.replace(/\/$/,'')];if(!row)return;
 var acts=li.querySelector('.acts')||li;var b=document.createElement('button');b.type='button';b.className='btn btn--small nle-edit';b.textContent='עריכה';b.onclick=function(){openListing(row.id,b)};acts.insertBefore(b,acts.firstChild);
 if(row.missing){var m=document.createElement('span');m.className='pill';m.style.cssText='background:transparent;color:var(--warn);border:1px dashed var(--warn)';m.textContent='חסרים '+row.missing+' פרטים';var mm=li.querySelector('.m');if(mm)mm.appendChild(m)}})}
function loadMap(){return req('GET','/edit/listings').then(function(r){map={};((r.j&&r.j.listings)||[]).forEach(function(x){map[x.url.replace(/\/$/,'')]=x});mark()})}
window.__nleReload=function(){loadMap()};
if(mine){new MutationObserver(function(){mark()}).observe(mine,{childList:true});loadMap()}
var hm=/^#edit-(\d+)$/.exec(location.hash||'');if(hm)setTimeout(function(){openListing(+hm[1],null)},400);
window.addEventListener('hashchange',function(){var m=/^#edit-(\d+)$/.exec(location.hash||'');if(m)openListing(+m[1],null)});
document.addEventListener('keydown',function(e){if(e.key!=='Escape')return;if(!sh.hidden){$('[data-cancel]',sh).click();return}if(!ed.hidden)closeEd()});
})();
NLEJS;
}
