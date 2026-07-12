<?php
/**
 * nadlan-config - RENTAL MANAGEMENT for private landlords (v1, 2026-07-12).
 *
 * The Israeli small-landlord product nobody offers free + self-serve:
 * every rented apartment managed FROM THE 3D BUILDING on a portfolio map.
 * Flow (owner order): /my-rentals/ dashboard opens with the PORTFOLIO MAP
 * on top; click a building pin -> its 3D model loads; click your apartment
 * on the model -> the management panel: tenancy, rent ledger, deadline
 * chips (contract end, option, the Jan-30 tax date), documents checklist,
 * maintenance log, real actions (WhatsApp reminder to the tenant, find a
 * professional, list the apartment).
 *
 * HONEST SCOPE v1: tracking + reminders + documents. NO payment
 * processing, NO tenant screening (rent moves by checks/bank transfer in
 * Israel - we track it, we do not move it). Tax figures are reminders
 * only, always "verify with רשות המסים".
 *
 * PRIVACY: CPT nadlan_rentalprop is public=false, no rewrite, no REST
 * show. Owner-only access (member invites = later). The ONLY public read
 * is GET /rental-demo serving the is_demo portfolio for the landing.
 *
 * MONETIZATION INFRA: free now; each property carries rm_plan meta
 * (default 'free') so paid tiers can gate features later without schema
 * change. Feature gate: option nadlan_feature_rentals ('1' = on).
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_rm_on' ) ) {
	function nadlan_rm_on() { return get_option( 'nadlan_feature_rentals', '1' ) === '1'; }
}

/* ---------- CPT ---------- */
add_action( 'init', function () {
	register_post_type( 'nadlan_rentalprop', array(
		'labels'              => array( 'name' => 'נכסים מושכרים', 'singular_name' => 'נכס מושכר' ),
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

/* ---------- vocab ---------- */
if ( ! function_exists( 'nadlan_rm_doc_keys' ) ) {
	function nadlan_rm_doc_keys() {
		return array(
			'contract'  => 'חוזה שכירות חתום',
			'nesach'    => 'נסח טאבו',
			'protocol'  => 'פרוטוקול מסירה + תמונות',
			'securities' => 'ביטחונות (צ\'ק ביטחון / שטר חוב / ערבים)',
			'insurance' => 'ביטוח מבנה',
		);
	}
}
if ( ! function_exists( 'nadlan_rm_unit_statuses' ) ) {
	/* label + hotspot color; status is DERIVED in JS from tenant + ledger */
	function nadlan_rm_unit_statuses() {
		return array(
			'ok'     => array( 'שולם', '#517048' ),
			'due'    => array( 'החודש טרם סומן', '#9C7A3C' ),
			'late'   => array( 'בפיגור', '#C2563A' ),
			'vacant' => array( 'פנויה', '#A79E8D' ),
			'unowned' => array( 'לא שלי', '#D8D2C4' ),
		);
	}
}
if ( ! function_exists( 'nadlan_rm_clean_units' ) ) {
	function nadlan_rm_clean_units( $raw ) {
		$dirs = array( 'west', 'east', 'north', 'south' );
		$out = array();
		foreach ( (array) $raw as $u ) {
			if ( ! is_array( $u ) || empty( $u['id'] ) ) { continue; }
			$docs = array();
			foreach ( array_keys( nadlan_rm_doc_keys() ) as $dk ) { $docs[ $dk ] = ! empty( $u['docs'][ $dk ] ); }
			$ledger = array();
			foreach ( (array) ( $u['ledger'] ?? array() ) as $m => $v ) {
				if ( preg_match( '/^\d{4}-\d{2}$/', (string) $m ) ) { $ledger[ (string) $m ] = 'paid' === $v ? 'paid' : 'open'; }
			}
			$maint = array();
			foreach ( array_slice( (array) ( $u['maintenance'] ?? array() ), 0, 60 ) as $mm ) {
				if ( ! is_array( $mm ) || '' === trim( (string) ( $mm['text'] ?? '' ) ) ) { continue; }
				$maint[] = array(
					'text'   => mb_substr( sanitize_text_field( (string) $mm['text'] ), 0, 300 ),
					'at'     => mb_substr( sanitize_text_field( (string) ( $mm['at'] ?? current_time( 'mysql' ) ) ), 0, 25 ),
					'status' => in_array( $mm['status'] ?? '', array( 'open', 'done' ), true ) ? $mm['status'] : 'open',
				);
			}
			$out[] = array(
				'id'          => sanitize_key( $u['id'] ),
				'floor'       => max( 0, min( 60, (int) ( $u['floor'] ?? 0 ) ) ),
				'pos'         => max( 0, min( 20, (int) ( $u['pos'] ?? 0 ) ) ),
				'dir'         => in_array( $u['dir'] ?? '', $dirs, true ) ? $u['dir'] : 'west',
				'label'       => mb_substr( sanitize_text_field( (string) ( $u['label'] ?? '' ) ), 0, 60 ),
				'tenant_name' => mb_substr( sanitize_text_field( (string) ( $u['tenant_name'] ?? '' ) ), 0, 80 ),
				'tenant_phone' => preg_replace( '/[^0-9+]/', '', (string) ( $u['tenant_phone'] ?? '' ) ),
				'rent'        => max( 0, min( 200000, (int) ( $u['rent'] ?? 0 ) ) ),
				'start'       => preg_match( '/^\d{4}-\d{2}-\d{2}$/', (string) ( $u['start'] ?? '' ) ) ? $u['start'] : '',
				'end'         => preg_match( '/^\d{4}-\d{2}-\d{2}$/', (string) ( $u['end'] ?? '' ) ) ? $u['end'] : '',
				'option_until' => preg_match( '/^\d{4}-\d{2}-\d{2}$/', (string) ( $u['option_until'] ?? '' ) ) ? $u['option_until'] : '',
				'linkage'     => in_array( $u['linkage'] ?? '', array( 'none', 'madad' ), true ) ? $u['linkage'] : 'none',
				'docs'        => $docs,
				'ledger'      => $ledger,
				'maintenance' => $maint,
				'note'        => mb_substr( sanitize_textarea_field( (string) ( $u['note'] ?? '' ) ), 0, 500 ),
			);
			if ( count( $out ) >= 200 ) { break; }
		}
		return $out;
	}
}

/* ---------- access ---------- */
if ( ! function_exists( 'nadlan_rm_can' ) ) {
	function nadlan_rm_can( $id ) {
		if ( current_user_can( 'manage_options' ) ) { return true; }
		return get_current_user_id() > 0 && (int) get_post_meta( $id, 'owner_user_id', true ) === get_current_user_id();
	}
}
if ( ! function_exists( 'nadlan_rm_prop_ok' ) ) {
	function nadlan_rm_prop_ok( $id ) {
		$p = get_post( $id );
		return $p && 'nadlan_rentalprop' === $p->post_type && 'trash' !== $p->post_status;
	}
}

/* ---------- payload ---------- */
if ( ! function_exists( 'nadlan_rm_payload' ) ) {
	function nadlan_rm_payload( $id ) {
		$units = json_decode( (string) get_post_meta( $id, 'rm_units', true ), true );
		$city  = (string) get_post_meta( $id, 'city', true );
		$p = get_post( $id );
		return array(
			'id'       => (int) $id,
			'title'    => $p ? $p->post_title : '', // raw: private posts get a "פרטי:" prefix via get_the_title
			'address'  => (string) get_post_meta( $id, 'address', true ),
			'city'     => $city,
			'floors'   => (int) get_post_meta( $id, 'floors', true ),
			'units_per_floor' => (int) get_post_meta( $id, 'units_per_floor', true ),
			'units'    => is_array( $units ) ? $units : array(),
			'is_demo'  => '1' === (string) get_post_meta( $id, 'is_demo', true ),
			'plan'     => (string) ( get_post_meta( $id, 'rm_plan', true ) ?: 'free' ),
			'can_manage' => nadlan_rm_can( $id ),
			'statuses' => nadlan_rm_unit_statuses(),
			'doc_keys' => nadlan_rm_doc_keys(),
			'centroid' => function_exists( 'nadlan_ur_space_centroid' ) ? nadlan_ur_space_centroid( $city ) : null,
		);
	}
}
if ( ! function_exists( 'nadlan_rm_my_props' ) ) {
	function nadlan_rm_my_props() {
		return get_posts( array( 'post_type' => 'nadlan_rentalprop', 'post_status' => 'any', 'posts_per_page' => 30,
			'fields' => 'ids', 'meta_query' => array( array( 'key' => 'owner_user_id', 'value' => get_current_user_id() ) ) ) );
	}
}

/* ---------- REST ---------- */
add_action( 'rest_api_init', function () {
	$own = function ( $req ) { return is_user_logged_in() && nadlan_rm_on() && nadlan_rm_prop_ok( (int) $req['id'] ) && nadlan_rm_can( (int) $req['id'] ); };

	/* public read-only demo portfolio for the landing */
	register_rest_route( 'nadlan/v1', '/rental-demo', array(
		'methods' => 'GET',
		'permission_callback' => function () { return nadlan_rm_on(); },
		'callback' => function () {
			$p = get_transient( 'nlrm_demo_payload' );
			if ( ! is_array( $p ) ) {
				$ids = get_posts( array( 'post_type' => 'nadlan_rentalprop', 'post_status' => 'any', 'posts_per_page' => 5,
					'fields' => 'ids', 'meta_query' => array( array( 'key' => 'is_demo', 'value' => '1' ) ) ) );
				if ( ! $ids ) { return new WP_Error( 'not_found', 'no demo portfolio', array( 'status' => 404 ) ); }
				$p = array_map( function ( $id ) { $x = nadlan_rm_payload( $id ); $x['can_manage'] = false; return $x; }, $ids );
				set_transient( 'nlrm_demo_payload', $p, 10 * MINUTE_IN_SECONDS );
			}
			foreach ( $p as &$x ) { $x['can_manage'] = false; }
			return array( 'props' => $p );
		},
	) );

	register_rest_route( 'nadlan/v1', '/rental-prop', array(
		'methods' => 'POST',
		'permission_callback' => function () { return is_user_logged_in() && nadlan_rm_on(); },
		'callback' => function ( WP_REST_Request $req ) {
			if ( function_exists( 'nadlan_ur_rate_limited' ) && nadlan_ur_rate_limited( 'rmprop', 5, DAY_IN_SECONDS ) ) {
				return new WP_Error( 'rate_limited', 'אפשר להוסיף עד 5 נכסים ביום.', array( 'status' => 429 ) );
			}
			$city   = mb_substr( sanitize_text_field( (string) $req->get_param( 'city' ) ), 0, 60 );
			$addr   = mb_substr( sanitize_text_field( (string) $req->get_param( 'address' ) ), 0, 120 );
			$floors = max( 1, min( 40, (int) $req->get_param( 'floors' ) ) );
			$upf    = max( 1, min( 12, (int) $req->get_param( 'units_per_floor' ) ) );
			if ( '' === $addr || '' === $city ) { return new WP_Error( 'bad_request', 'נדרשות עיר וכתובת.', array( 'status' => 400 ) ); }
			$id = wp_insert_post( array( 'post_type' => 'nadlan_rentalprop', 'post_status' => 'private',
				'post_title' => $addr . ', ' . $city ), true );
			if ( is_wp_error( $id ) ) { return $id; }
			update_post_meta( $id, 'owner_user_id', get_current_user_id() );
			update_post_meta( $id, 'address', $addr );
			update_post_meta( $id, 'city', $city );
			update_post_meta( $id, 'floors', $floors );
			update_post_meta( $id, 'units_per_floor', $upf );
			update_post_meta( $id, 'rm_plan', 'free' );
			update_post_meta( $id, 'rm_units', wp_slash( wp_json_encode( array(), JSON_UNESCAPED_UNICODE ) ) );
			return array( 'id' => (int) $id );
		},
	) );

	register_rest_route( 'nadlan/v1', '/rental-props', array(
		'methods' => 'GET',
		'permission_callback' => function () { return is_user_logged_in() && nadlan_rm_on(); },
		'callback' => function () {
			return array( 'props' => array_map( 'nadlan_rm_payload', nadlan_rm_my_props() ) );
		},
	) );

	register_rest_route( 'nadlan/v1', '/rental-prop/(?P<id>\d+)', array(
		'methods' => 'GET', 'permission_callback' => $own,
		'callback' => function ( $req ) { return nadlan_rm_payload( (int) $req['id'] ); },
	) );

	register_rest_route( 'nadlan/v1', '/rental-prop/(?P<id>\d+)/units', array(
		'methods' => 'POST', 'permission_callback' => $own,
		'callback' => function ( WP_REST_Request $req ) {
			$id = (int) $req['id'];
			update_post_meta( $id, 'rm_units', wp_slash( wp_json_encode( nadlan_rm_clean_units( (array) $req->get_param( 'units' ) ), JSON_UNESCAPED_UNICODE ) ) );
			return nadlan_rm_payload( $id );
		},
	) );

	/* admin-only idempotent demo seed (the landing's live example) */
	register_rest_route( 'nadlan/v1', '/rental-demo-seed', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function () {
			$exists = get_posts( array( 'post_type' => 'nadlan_rentalprop', 'post_status' => 'any', 'posts_per_page' => 1,
				'fields' => 'ids', 'meta_query' => array( array( 'key' => 'is_demo', 'value' => '1' ) ) ) );
			if ( $exists ) { return array( 'existed' => true, 'ids' => $exists ); }
			$mk = function ( $title, $addr, $city, $floors, $upf, $units ) {
				$id = wp_insert_post( array( 'post_type' => 'nadlan_rentalprop', 'post_status' => 'private', 'post_title' => $title ) );
				update_post_meta( $id, 'owner_user_id', 0 );
				update_post_meta( $id, 'is_demo', '1' );
				update_post_meta( $id, 'address', $addr );
				update_post_meta( $id, 'city', $city );
				update_post_meta( $id, 'floors', $floors );
				update_post_meta( $id, 'units_per_floor', $upf );
				update_post_meta( $id, 'rm_plan', 'free' );
				update_post_meta( $id, 'rm_units', wp_slash( wp_json_encode( nadlan_rm_clean_units( $units ), JSON_UNESCAPED_UNICODE ) ) );
				return (int) $id;
			};
			$y = (int) gmdate( 'Y' ); $m = (int) gmdate( 'n' );
			$mm = function ( $off ) use ( $y, $m ) { $t = mktime( 0, 0, 0, $m + $off, 1, $y ); return gmdate( 'Y-m', $t ); };
			$led_ok = array(); for ( $i = -11; $i <= 0; $i++ ) { $led_ok[ $mm( $i ) ] = 'paid'; }
			$led_due = $led_ok; unset( $led_due[ $mm( 0 ) ] );
			$led_late = $led_ok; unset( $led_late[ $mm( 0 ) ], $led_late[ $mm( -1 ) ] );
			$ids = array();
			$ids[] = $mk( 'דוגמה: ארלוזורוב 78, תל אביב', 'ארלוזורוב 78', 'תל אביב-יפו', 5, 3, array(
				array( 'id' => 'f3-1', 'floor' => 3, 'pos' => 0, 'dir' => 'west', 'label' => 'דירה 7', 'tenant_name' => 'משפחת לוי (דוגמה)', 'tenant_phone' => '9725' . '00000001', 'rent' => 7800, 'start' => ( $y - 1 ) . '-08-01', 'end' => $y . '-07-31', 'option_until' => ( $y + 1 ) . '-07-31', 'linkage' => 'madad',
						'docs' => array( 'contract' => true, 'nesach' => true, 'protocol' => true, 'securities' => true, 'insurance' => true ),
						'ledger' => $led_ok, 'maintenance' => array( array( 'text' => 'תוקן דוד שמש (דוגמה)', 'at' => $y . '-03-02', 'status' => 'done' ) ), 'note' => 'נתוני דוגמה' ),
				array( 'id' => 'f5-2', 'floor' => 5, 'pos' => 1, 'dir' => 'south', 'label' => 'דירה 14', 'tenant_name' => 'ד. כהן (דוגמה)', 'tenant_phone' => '9725' . '00000002', 'rent' => 6400, 'start' => $y . '-01-15', 'end' => ( $y + 1 ) . '-01-14', 'option_until' => '', 'linkage' => 'none',
						'docs' => array( 'contract' => true, 'nesach' => true, 'protocol' => false, 'securities' => true, 'insurance' => false ),
						'ledger' => $led_due, 'maintenance' => array( array( 'text' => 'טפטוף בברז המטבח (דוגמה)', 'at' => gmdate( 'Y-m-d' ), 'status' => 'open' ) ), 'note' => 'נתוני דוגמה' ),
			) );
			$ids[] = $mk( 'דוגמה: ז\'בוטינסקי 12, רמת גן', 'ז\'בוטינסקי 12', 'רמת גן', 8, 4, array(
				array( 'id' => 'f2-3', 'floor' => 2, 'pos' => 2, 'dir' => 'east', 'label' => 'דירה 7', 'tenant_name' => 'ר. מזרחי (דוגמה)', 'tenant_phone' => '9725' . '00000003', 'rent' => 5900, 'start' => ( $y - 2 ) . '-10-01', 'end' => $y . '-09-30', 'option_until' => '', 'linkage' => 'madad',
						'docs' => array( 'contract' => true, 'nesach' => true, 'protocol' => true, 'securities' => true, 'insurance' => true ),
						'ledger' => $led_late, 'maintenance' => array(), 'note' => 'נתוני דוגמה' ),
				array( 'id' => 'f6-1', 'floor' => 6, 'pos' => 0, 'dir' => 'north', 'label' => 'דירה 21', 'tenant_name' => '', 'tenant_phone' => '', 'rent' => 0, 'start' => '', 'end' => '', 'option_until' => '', 'linkage' => 'none',
						'docs' => array(), 'ledger' => array(), 'maintenance' => array( array( 'text' => 'צביעה לפני שוכר חדש (דוגמה)', 'at' => gmdate( 'Y-m-d' ), 'status' => 'open' ) ), 'note' => 'פנויה - נתוני דוגמה' ),
			) );
			delete_transient( 'nlrm_demo_payload' );
			return array( 'created' => true, 'ids' => $ids );
		},
	) );
} );

add_action( 'save_post_nadlan_rentalprop', function () { delete_transient( 'nlrm_demo_payload' ); } );

/* ---------- /my-rentals/ route ---------- */
add_action( 'init', function () {
	add_rewrite_rule( '^my-rentals/?$', 'index.php?nadlan_my_rentals=1', 'top' );
	if ( get_option( 'nadlan_my_rentals_rewrite_v1' ) !== '1' ) {
		flush_rewrite_rules( false );
		update_option( 'nadlan_my_rentals_rewrite_v1', '1' );
	}
} );
add_filter( 'query_vars', function ( $v ) { $v[] = 'nadlan_my_rentals'; return $v; } );

add_action( 'template_redirect', function () {
	if ( ! get_query_var( 'nadlan_my_rentals' ) ) { return; }
	if ( ! nadlan_rm_on() ) { wp_safe_redirect( home_url( '/' ) ); exit; }
	$has = is_user_logged_in() && nadlan_rm_my_props();
	nadlan_rm_render( $has ? 'live' : 'landing' );
	exit;
} );

/* ---------- render ---------- */
if ( ! function_exists( 'nadlan_rm_mount' ) ) {
	function nadlan_rm_mount( $mode ) {
		$glb = esc_url( function_exists( 'nadlan_showroom_engine_base_url' ) ? nadlan_showroom_engine_base_url() . 'models/standard-residential.glb' : '' );
		$token = function_exists( 'nadlan_mapbox_token' ) ? nadlan_mapbox_token() : '';
		$js = esc_url( plugins_url( 'assets/rentals/rental-manager.js', dirname( __FILE__ ) ) . '?v=' . rawurlencode( NADLAN_CONFIG_VERSION ) );
		?>
<div id="nlrm-mount" class="nlrm-app" data-loading="1"
	data-mode="<?php echo esc_attr( $mode ); ?>"
	data-rest="<?php echo esc_url( rest_url( 'nadlan/v1' ) ); ?>"
	data-nonce="<?php echo esc_attr( is_user_logged_in() ? wp_create_nonce( 'wp_rest' ) : '' ); ?>"
	data-glb="<?php echo $glb; // phpcs:ignore ?>"
	data-mapbox="<?php echo esc_attr( $token ); ?>"
	data-pros="<?php echo esc_url( home_url( '/professionals/' ) ); ?>"
	data-wizard="<?php echo esc_url( home_url( '/list-property/' ) ); ?>">טוענים את הנכסים...</div>
<script defer src="<?php echo $js; // phpcs:ignore ?>"></script>
		<?php
	}
}

if ( ! function_exists( 'nadlan_rm_render' ) ) {
	function nadlan_rm_render( $mode ) {
		$landing = ( 'landing' === $mode );
		$self = home_url( '/my-rentals/' );
		$title = 'ניהול השכרות חינם לבעלי דירות: המפה, הבניין בתלת-ממד וכל דירה מושכרת במקום אחד | נדלן';
		$desc  = 'מערכת חינמית לניהול דירות מושכרות: כל הנכסים על מפה, כל בניין במודל תלת-ממדי, ולכל דירה - שוכר, שכר דירה, מעקב תשלומים, תזכורות חוזה ומס, מסמכים ותחזוקה. בלי סליקה, בלי עמלות.';
		if ( $landing ) {
			add_filter( 'pre_get_document_title', function () use ( $title ) { return $title; }, 99 );
			add_action( 'wp_head', function () use ( $desc, $self ) {
				echo '<meta name="description" content="' . esc_attr( $desc ) . '">' . "\n";
				echo '<link rel="canonical" href="' . esc_url( $self ) . '">' . "\n";
			}, 4 );
		} else {
			nocache_headers();
			header( 'X-Robots-Tag: noindex, nofollow' );
		}
		get_header();
		?>
<div class="nlrm" dir="rtl">
	<style>
	.nlrm{max-width:1120px;margin:0 auto;padding:24px 16px 60px;font-family:Heebo,sans-serif;color:#1B1A17}
	.nlrm h1,.nlrm h2,.nlrm h3{font-family:"Frank Ruhl Libre",Georgia,serif}
	.nlrm-hero{text-align:center;padding:30px 0 10px}
	.nlrm-kicker{font:700 12.5px Heebo;letter-spacing:.06em;color:#9C7A3C;text-transform:uppercase;margin:0 0 10px}
	.nlrm-hero h1{font-size:clamp(1.6rem,3.8vw,2.4rem);margin:0 0 12px;line-height:1.3}
	.nlrm-hero .sub{color:#51483A;font:400 15px/1.7 Heebo;max-width:640px;margin:0 auto 20px}
	.nlrm-ctas{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}
	.nlrm-cta{display:inline-block;border-radius:12px;padding:15px 26px;font:700 15px Heebo;text-decoration:none}
	.nlrm-cta--go{background:#C2563A;color:#FAF7F1;box-shadow:0 14px 30px -12px rgba(194,86,58,.55)}
	.nlrm-badges{color:#8E877A;font:600 12px Heebo;margin:14px 0 22px}
	.nlrm-steps{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:10px 0 30px}
	@media(max-width:760px){.nlrm-steps{grid-template-columns:1fr}}
	.nlrm-step{background:#fff;border:1px solid #E2DCD0;border-radius:16px;padding:18px;text-align:start}
	.nlrm-step i{display:block;width:36px;height:36px;border-radius:50%;background:#9C7A3C;color:#FAF7F1;font:700 16px/36px "Frank Ruhl Libre",serif;font-style:normal;text-align:center;margin-bottom:10px}
	.nlrm-step b{display:block;font-family:"Frank Ruhl Libre",serif;margin-bottom:4px}
	.nlrm-step p{font:400 13px/1.65 Heebo;color:#51483A;margin:0}
	.nlrm-demo{background:#F3EEE3;border:1px solid #E2DCD0;border-radius:22px;padding:18px;margin:0 0 30px}
	.nlrm-demo-head{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;margin-bottom:12px}
	.nlrm-demo-head h2{margin:0;font-size:1.3rem}
	.nlrm-demo-head .lbl{background:#1B1A17;color:#E9D9A8;font:600 12px Heebo;border-radius:999px;padding:7px 13px}
	.nlrm-honest{background:#fff;border:1px solid #E2DCD0;border-radius:14px;padding:14px 18px;font:400 13px/1.7 Heebo;color:#51483A;margin:0 0 30px}
	/* app */
	.nlrm-app{min-height:200px}
	.nlrm-app[data-loading]{color:#8E877A;text-align:center;padding:30px 0}
	.nlrm-map{height:300px;border-radius:16px;overflow:hidden;background:#EFEAE0;border:1px solid #E2DCD0}
	.nlrm-props{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0}
	.nlrm-props button{border:1px solid #E2DCD0;border-radius:999px;padding:9px 15px;font:600 13px Heebo;color:#51483A;background:#fff;cursor:pointer}
	.nlrm-props button.is-on{background:#1B1A17;color:#FAF7F1;border-color:#1B1A17}
	.nlrm-3d{position:relative;height:52vh;min-height:400px;max-height:600px;border-radius:18px;overflow:hidden;background:radial-gradient(ellipse at 50% 30%,#26221733 0%,transparent 65%),#14130F;border:1px solid #2A251B;margin-top:8px}
	@media(max-width:600px){.nlrm-3d{height:58vh}}
	.nlrm-3d model-viewer{width:100%;height:100%;direction:ltr;background:transparent}
	.nlrm-hot{width:30px;height:30px;border-radius:50%;border:2px solid #fff;color:#fff;font:700 10.5px Heebo;cursor:pointer;background:#A79E8D}
	.nlrm-hot:not([data-visible]){opacity:0;pointer-events:none}
	.nlrm-hot.is-ghost{background:rgba(216,210,196,.35);border-style:dashed;color:#F3EEE3}
	.nlrm-legend{display:flex;gap:12px;flex-wrap:wrap;margin:10px 2px;font:600 12px Heebo;color:#51483A}
	.nlrm-legend i{display:inline-block;width:11px;height:11px;border-radius:50%;margin-inline-end:4px;vertical-align:-1px}
	.nlrm-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px}
	@media(max-width:860px){.nlrm-grid{grid-template-columns:1fr}}
	.nlrm-card{background:#fff;border:1px solid #E2DCD0;border-radius:16px;padding:18px 20px}
	.nlrm-card h4{font-family:"Frank Ruhl Libre",serif;margin:0 0 10px;font-size:1.06rem}
	.nlrm-note{font:400 12px/1.6 Heebo;color:#8E877A}
	.nlrm-btn{background:#C2563A;color:#FAF7F1;border:0;border-radius:10px;padding:11px 18px;font:700 13.5px Heebo;cursor:pointer;margin-top:8px}
	.nlrm-btn--ghost{background:#fff;color:#1B1A17;border:1.5px solid #9C7A3C}
	.nlrm input,.nlrm select,.nlrm textarea{width:100%;border:1px solid #E2DCD0;border-radius:10px;padding:10px;font:400 14px Heebo;background:#FAF7F1;box-sizing:border-box}
	.nlrm-f{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:8px 0}
	.nlrm-f label{display:flex;flex-direction:column;gap:4px;font:600 12px Heebo;color:#51483A}
	.nlrm-chips{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0}
	.nlrm-chip{display:inline-block;border-radius:999px;padding:6px 12px;font:600 12px Heebo;background:#F3EEE3;border:1px solid #E2DCD0;color:#51483A}
	.nlrm-chip--warn{background:#FCEFE9;border-color:#C2563A;color:#7A2E1D}
	.nlrm-chip--gold{background:#F7F1E3;border-color:#C99C49;color:#6b5a33}
	.nlrm-ledger{display:grid;grid-template-columns:repeat(6,1fr);gap:6px;margin:8px 0}
	@media(max-width:520px){.nlrm-ledger{grid-template-columns:repeat(4,1fr)}}
	.nlrm-ledger button{border:1px solid #E2DCD0;border-radius:8px;padding:8px 2px;font:600 11px Heebo;background:#FAF7F1;cursor:pointer;color:#51483A}
	.nlrm-ledger button.is-paid{background:#517048;border-color:#517048;color:#FAF7F1}
	.nlrm-docrow{display:flex;align-items:center;gap:8px;font:400 13.5px Heebo;margin:5px 0}
	.nlrm-docrow input{width:auto}
	.nlrm-maint li{font:400 13px/1.6 Heebo;border-bottom:1px solid #F3EEE3;padding:6px 0;list-style:none;display:flex;justify-content:space-between;gap:8px}
	.nlrm-maint li.is-done{color:#8E877A;text-decoration:line-through}
	.nlrm-actions{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}
	.nlrm-actions a{border:1px solid #E2DCD0;border-radius:10px;padding:10px 14px;font:700 12.5px Heebo;color:#1B1A17;text-decoration:none;background:#fff}
	.nlrm-actions a:hover{border-color:#9C7A3C}
	.nlrm-new{background:#fff;border:1.5px solid #9C7A3C;border-radius:16px;padding:18px;margin:14px 0}
	h1:empty{display:none}
	</style>
	<?php if ( $landing ) : ?>
	<header class="nlrm-hero">
		<p class="nlrm-kicker">ניהול השכרות · חינם לבעלי דירות</p>
		<h1>כל הדירות המושכרות שלכם: על המפה, בתוך הבניין, בשליטה מלאה</h1>
		<p class="sub">מוסיפים נכס, מסמנים את הדירות שלכם על מודל תלת-ממדי של הבניין, ומנהלים הכל מדירה אחת: שוכר, שכר דירה, מעקב תשלומים, תזכורות חוזה ומס, מסמכים ותחזוקה. בלי אקסל ובלי עמלות.</p>
		<div class="nlrm-ctas">
			<a class="nlrm-cta nlrm-cta--go" href="<?php echo esc_url( is_user_logged_in() ? '#nlrm-new' : wp_login_url( $self ) ); ?>">מתחילים לנהל, חינם</a>
		</div>
		<p class="nlrm-badges">חינם לבעלי דירות · מעקב ותזכורות, לא סליקה · פרטי ולא מופיע בחיפוש</p>
	</header>
	<div class="nlrm-steps">
		<div class="nlrm-step"><i>1</i><b>מוסיפים נכס</b><p>עיר, כתובת, קומות - ונבנה לכם מודל תלת-ממדי של הבניין על המפה.</p></div>
		<div class="nlrm-step"><i>2</i><b>מסמנים את הדירות שלכם</b><p>מקישים על הדירות שבבעלותכם על המודל וממלאים שוכר, שכר דירה ותאריכי חוזה.</p></div>
		<div class="nlrm-step"><i>3</i><b>הכל במעקב אחד</b><p>צבע הדירה אומר הכל: שולם, ממתין, בפיגור, פנויה. תזכורות חוזה, מסמכים ותחזוקה - במקום אחד.</p></div>
	</div>
	<section class="nlrm-demo">
		<div class="nlrm-demo-head"><h2>הדגמה חיה: תיק של משכיר עם שתי דירות</h2><span class="lbl">נתוני דוגמה</span></div>
		<?php nadlan_rm_mount( 'demo' ); ?>
	</section>
	<div class="nlrm-honest">הגינות מלאה: המערכת עוקבת ומזכירה - היא לא גובה כסף ולא מבצעת סליקה. שכר הדירה ממשיך לעבור כרגיל (העברה בנקאית או צ'קים). תזכורות המס הן תזכורות בלבד - את המספרים המחייבים בודקים מול רשות המסים.</div>
	<?php if ( is_user_logged_in() ) : ?>
	<section class="nlrm-new" id="nlrm-new">
		<h2 style="margin:0 0 10px;font-size:1.15rem">הוספת הנכס הראשון</h2>
		<div class="nlrm-f">
			<label>עיר<input type="text" id="nlrm-city"></label>
			<label>רחוב ומספר<input type="text" id="nlrm-addr"></label>
			<label>קומות<input type="number" id="nlrm-floors" min="1" max="40" value="4"></label>
			<label>דירות בקומה<input type="number" id="nlrm-upf" min="1" max="12" value="3"></label>
		</div>
		<button type="button" class="nlrm-btn" id="nlrm-create">יצירת הנכס</button>
		<div id="nlrm-createmsg" class="nlrm-note" aria-live="polite"></div>
	</section>
	<?php endif; ?>
	<script type="application/ld+json"><?php echo wp_json_encode( array(
		'@context' => 'https://schema.org', '@type' => 'FAQPage', 'mainEntity' => array(
			array( '@type' => 'Question', 'name' => 'כמה זה עולה?', 'acceptedAnswer' => array( '@type' => 'Answer', 'text' => 'ניהול ההשכרות חינמי לבעלי דירות. אין עמלות ואין סליקה - שכר הדירה ממשיך לעבור ישירות אליכם.' ) ),
			array( '@type' => 'Question', 'name' => 'מי רואה את הנתונים שלי?', 'acceptedAnswer' => array( '@type' => 'Answer', 'text' => 'רק אתם. הנכסים פרטיים, לא מופיעים בחיפוש, והגישה מוגנת בחשבון שלכם.' ) ),
			array( '@type' => 'Question', 'name' => 'מה עם הצמדה למדד ומס?', 'acceptedAnswer' => array( '@type' => 'Answer', 'text' => 'מסמנים חוזה צמוד מדד ומקבלים תזכורת עדכון; המערכת מזכירה גם את מועד הדיווח השנתי (30 בינואר במסלול 10 אחוזים). המספרים המחייבים נבדקים תמיד מול רשות המסים.' ) ),
		) ), JSON_UNESCAPED_UNICODE ); ?></script>
	<?php else : ?>
	<header style="margin-bottom:6px">
		<h1 style="margin:0 0 4px">הנכסים המושכרים שלי</h1>
		<p class="nlrm-note">פרטי לחשבון שלכם בלבד ואינו מופיע בחיפוש. מעקב ותזכורות - לא סליקה.</p>
	</header>
	<?php nadlan_rm_mount( 'live' ); ?>
	<section class="nlrm-new" id="nlrm-new" style="margin-top:18px">
		<h2 style="margin:0 0 10px;font-size:1.1rem">הוספת נכס נוסף</h2>
		<div class="nlrm-f">
			<label>עיר<input type="text" id="nlrm-city"></label>
			<label>רחוב ומספר<input type="text" id="nlrm-addr"></label>
			<label>קומות<input type="number" id="nlrm-floors" min="1" max="40" value="4"></label>
			<label>דירות בקומה<input type="number" id="nlrm-upf" min="1" max="12" value="3"></label>
		</div>
		<button type="button" class="nlrm-btn" id="nlrm-create">יצירת הנכס</button>
		<div id="nlrm-createmsg" class="nlrm-note" aria-live="polite"></div>
	</section>
	<?php endif; ?>
	<?php if ( $landing && is_user_logged_in() ) : ?><?php endif; ?>
	<script>
	(function(){
		var b=document.getElementById("nlrm-create");if(!b)return;
		b.addEventListener("click",function(){
			var m=document.getElementById("nlrm-createmsg");m.textContent="יוצרים...";
			fetch("<?php echo esc_url( rest_url( 'nadlan/v1/rental-prop' ) ); ?>",{method:"POST",
				headers:{"Content-Type":"application/json","X-WP-Nonce":"<?php echo esc_js( wp_create_nonce( 'wp_rest' ) ); ?>"},
				body:JSON.stringify({city:document.getElementById("nlrm-city").value,address:document.getElementById("nlrm-addr").value,floors:document.getElementById("nlrm-floors").value,units_per_floor:document.getElementById("nlrm-upf").value})})
			.then(function(r){return r.json().then(function(j){if(!r.ok)throw j;return j})})
			.then(function(){location.href="<?php echo esc_url( $self ); ?>"})
			.catch(function(e){m.textContent=(e&&e.message)||"שגיאה"});
		});
	})();
	document.addEventListener("DOMContentLoaded",function(){document.querySelectorAll("h1").forEach(function(h){if(!h.textContent.trim()&&!h.children.length){h.remove()}})});
	</script>
</div>
		<?php
		get_footer();
	}
}

/* healthcheck visibility */
add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$out['rentals'] = nadlan_rm_on();
	return $out;
} );
