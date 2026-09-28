<?php
/**
 * The apartment's basket, first step of the buying journey (design system L9Nqz7Viv7K3MYeZrBc9s8 version 86, BasketOne; the
 * journey is BuyJourney v78). The owner, 28.9.2026: "put it in the basket... the pipeline to work end to end... the real
 * payment we do with the representatives". On a project page with a stage the buyer collects, in one place:
 *  - the apartment picked on the stage (an example apartment: floor and direction), and the design style picked inside it;
 *  - a team for that apartment: real professionals from the directory, never a sample profile; where the directory has
 *    none yet, "לבקש המלצה" asks NadLan's team on WhatsApp;
 *  - the full price: the price the buyer enters (from the representative; a published average is shown as a hint with its
 *    source, never multiplied into a price), purchase tax by the brackets in force (inc/calculators.php) for a single home,
 *    an additional home or a foreign resident, and a lawyer's fee if the buyer types one;
 *  - two ways on: the basket to the representative on WhatsApp, and the shared viewing room (inc/together.php).
 * Nothing is sold or paid here: the apartment is never sold on the site, and money for it goes only to the project's
 * escrow against a Sale Law guarantee (the basket says so). Payments for services wait for the owner's decisions.
 * The basket lives in the visitor's browser (localStorage), per project. Off switch: option nadlan_basket = '0'.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_bk_on' ) ) {
	function nadlan_bk_on() {
		if ( '0' === (string) get_option( 'nadlan_basket', '1' ) || is_admin() ) { return false; }
		return function_exists( 'nadlan_ps_current' ) && nadlan_ps_current();
	}
}

if ( ! function_exists( 'nadlan_bk_team' ) ) {
	/** The team's slots, in the journey's order (BuyJourney v78): directory keys and the words the basket uses. */
	function nadlan_bk_team() {
		return array(
			array( 'interior_designer', 'מעצב/ת פנים', 'מעצב/ת פנים' ),
			array( 'lawyer', 'עו״ד מקרקעין', 'עורך/ת דין מקרקעין' ),
			array( 'shamai', 'שמאי מקרקעין', 'שמאי/ת מקרקעין' ),
			array( 'mashkanta', 'יועץ משכנתאות', 'יועץ/ת משכנתאות' ),
			array( 'accountant', 'רו״ח מיסוי נדל״ן', 'רואה/ת חשבון למיסוי נדל״ן' ),
			array( 'engineer', 'מהנדס/ת או מפקח/ת בנייה', 'מהנדס/ת או מפקח/ת בנייה' ),
		);
	}
}

/* REST: real professionals for a slot (never a sample profile), the project's city first, three at most */
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/basket/pros', array(
		'methods'             => 'GET',
		'permission_callback' => '__return_true',
		'args'                => array(
			'profession' => array( 'type' => 'string', 'required' => true ),
			'city'       => array( 'type' => 'string' ),
		),
		'callback'            => function ( $req ) {
			$prof  = sanitize_key( (string) $req->get_param( 'profession' ) );
			$city  = sanitize_text_field( (string) $req->get_param( 'city' ) );
			$keys  = array_map( function ( $t ) { return $t[0]; }, nadlan_bk_team() );
			if ( ! in_array( $prof, $keys, true ) ) { return new WP_Error( 'nadlan_bk_prof', 'unknown profession', array( 'status' => 400 ) ); }
			$profs = 'engineer' === $prof ? array( 'engineer', 'mefakeach' ) : array( $prof );
			$ck    = 'nlbk_' . md5( $prof . '|' . $city );
			$out   = get_transient( $ck );
			if ( false === $out ) {
				$out  = array();
				$base = array(
					'post_type'      => 'nadlan_professional',
					'post_status'    => 'publish',
					'posts_per_page' => 3,
					'no_found_rows'  => true,
					'meta_query'     => array(
						'relation' => 'AND',
						array( 'key' => 'profession', 'value' => $profs, 'compare' => 'IN' ),
						array( 'relation' => 'OR', array( 'key' => 'is_demo', 'compare' => 'NOT EXISTS' ), array( 'key' => 'is_demo', 'value' => array( '1', 'true' ), 'compare' => 'NOT IN' ) ),
					),
				);
				$ids = array();
				foreach ( '' !== $city ? array( true, false ) : array( false ) as $in_city ) {
					if ( count( $ids ) >= 3 ) { break; }
					$q = $base;
					if ( $in_city ) { $q['meta_query'][] = array( 'key' => 'city', 'value' => $city ); }
					if ( $ids ) { $q['post__not_in'] = $ids; }
					foreach ( get_posts( $q ) as $p ) {
						if ( count( $ids ) >= 3 ) { break; }
						$ids[] = $p->ID;
						$lic   = trim( (string) get_post_meta( $p->ID, 'license_number', true ) );
						$out[] = array(
							'id'      => (int) $p->ID,
							'name'    => function_exists( 'nadlan_prof_person_name' ) ? (string) nadlan_prof_person_name( $p->ID ) : get_the_title( $p ),
							'role'    => function_exists( 'nadlan_dir_prof_label' ) ? (string) nadlan_dir_prof_label( (string) get_post_meta( $p->ID, 'profession', true ), $p->ID ) : '',
							'city'    => (string) get_post_meta( $p->ID, 'city', true ),
							'license' => $lic,
							'url'     => get_permalink( $p->ID ),
						);
					}
				}
				set_transient( $ck, $out, HOUR_IN_SECONDS );
			}
			return array( 'ok' => true, 'pros' => $out );
		},
	) );
} );

/* the basket's settings and files, on a page with a stage */
add_action( 'wp_enqueue_scripts', function () {
	if ( ! nadlan_bk_on() ) { return; }
	$v = defined( 'NADLAN_CONFIG_VERSION' ) ? NADLAN_CONFIG_VERSION : '1';
	wp_enqueue_style( 'nadlan-basket', plugins_url( 'assets/basket/basket.css', dirname( __FILE__ ) ), array(), $v );
	wp_enqueue_script( 'nadlan-basket', plugins_url( 'assets/basket/basket.js', dirname( __FILE__ ) ), array(), $v, array( 'in_footer' => true, 'strategy' => 'defer' ) );
}, 30 );

add_action( 'wp_footer', function () {
	if ( ! nadlan_bk_on() ) { return; }
	$ps  = nadlan_ps_current();
	$id  = (int) $ps['id'];
	$tax = function_exists( 'nadlan_purchase_tax_config' ) ? nadlan_purchase_tax_config() : array();
	foreach ( array( 'single', 'additional' ) as $k ) { // the last ceiling is open; JSON has no PHP_INT_MAX
		foreach ( (array) ( $tax[ $k ] ?? array() ) as $i => $b ) { if ( (float) $b[0] >= PHP_INT_MAX ) { $tax[ $k ][ $i ][0] = null; } }
	}
	$team = array();
	foreach ( nadlan_bk_team() as $t ) { $team[] = array( 'key' => $t[0], 'label' => $t[1], 'ask' => $t[2] ); }
	$wa   = function_exists( 'nadlan_cta_whatsapp_number' ) ? preg_replace( '/\D/', '', (string) nadlan_cta_whatsapp_number() ) : '';
	$sec  = array();
	foreach ( (array) ( $ps['sectors'] ?? array() ) as $s ) { $sec[] = array( (float) $s[0], (float) $s[1], (string) $s[2] ); }
	$cfg  = array(
		'slug'    => (string) $ps['slug'],
		'name'    => (string) $ps['name'],
		'city'    => (string) get_post_meta( $id, 'city', true ),
		'wa'      => $wa,
		'sectors' => $sec,
		'hint'    => (string) ( $ps['basket_hint'] ?? '' ), // a published price, with its source: shown, never multiplied
		'tax'     => $tax,
		'team'    => $team,
		'rest'    => esc_url_raw( rest_url( 'nadlan/v1/basket/pros' ) ),
		'mortgage' => esc_url_raw( home_url( '/mortgage-calculator/' ) ),
		'join'    => esc_url_raw( home_url( '/advertise/' ) ),
	);
	echo '<script type="application/json" id="nadlan-basket-cfg">' . wp_json_encode( $cfg, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . '</script>' . "\n";
}, 40 );
