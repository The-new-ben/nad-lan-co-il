<?php
// Offline check of the calendar link: the featured broker card and the helper, with the real plugin code.
define( 'ABSPATH', __DIR__ . '/' );
$GLOBALS['META'] = array(
	7833 => array( 'profession' => 'metavech', 'phone' => '052-3631582', 'license_number' => '3131540', 'company_name' => 'נדל״ן על הים', 'city' => 'תל אביב יפו', 'areas_served' => 'נופי ים, כוכב הצפון', 'nl_name_he' => 'מיטל קציר', 'gender' => 'f' ),
);
function add_action() {} function add_filter() {} function register_post_meta() {} function add_meta_box() {} function add_shortcode() {}
function get_post_meta( $id, $k = '', $single = false ) { return $GLOBALS['META'][ $id ][ $k ] ?? ''; }
function get_the_title( $id ) { return 'מיטל קציר · נדל״ן על הים'; }
function get_permalink( $id ) { return 'https://nad-lan.co.il/professionals/meital-katzir/'; }
function get_post_status( $id ) { return 'publish'; }
function has_post_thumbnail( $id ) { return false; }
function get_posts( $a ) { return array(); }
function wp_parse_args( $a, $d ) { return array_merge( $d, $a ); }
function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_attr( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_url( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function wp_http_validate_url( $u ) { return filter_var( $u, FILTER_VALIDATE_URL ) ? $u : false; }
function nlds_icon( $n ) { return '<svg data-i="' . $n . '"></svg>'; }
function nadlan_dir_prof_label( $p, $id ) { return 'מתווכת'; }
function nadlan_dir_registry_verified( $id ) { return true; }
function plugins_url( $a, $b ) { return 'https://nad-lan.co.il/wp-content/plugins/nadlan-config/' . $a; }
require $argv[1] . '/inc/professional-profile.php';
require $argv[1] . '/inc/brokers-list.php';

$cases = array(
	'no link'           => '',
	'google'            => 'https://calendar.app.google/AbCdEf123',
	'calendly'          => 'https://calendly.com/meital/tour',
	'http (refused)'    => 'http://calendly.com/meital/tour',
	'javascript (refused)' => 'javascript:alert(1)',
);
$ok = true;
foreach ( $cases as $label => $url ) {
	$GLOBALS['META'][7833]['calendar_url'] = $url;
	$helper = nadlan_prof_calendar_url( 7833 );
	$card   = nadlan_bl_feature_card( 7833 );
	$ad     = nadlan_bl_feature_card( 7833, array( 'calendar' => false, 'wa_label' => 'התייעצות בוואטסאפ', 'link_attrs' => ' data-nl-ev="place_click"' ) );
	$want_cal = in_array( $label, array( 'google', 'calendly' ), true );
	$card_cal = false !== strpos( $card, 'data-nl-ev="tour"' ) && false !== strpos( $card, esc_url( $url ) );
	$card_wa  = false !== strpos( $card, 'https://wa.me/972523631582' );
	$ad_cal   = false !== strpos( $ad, 'data-nl-ev="tour"' );
	$pass = ( $want_cal ? ( $helper === $url && $card_cal && ! $card_wa ) : ( '' === $helper && ! $card_cal && $card_wa ) ) && ! $ad_cal && 1 === substr_count( $card, 'nlds-btn--primary' );
	$ok = $ok && $pass;
	printf( "%-22s helper=%-40s card: calendar=%s whatsapp=%s | ad keeps WhatsApp=%s => %s\n", $label, var_export( $helper, true ), $card_cal ? 'yes' : 'no', $card_wa ? 'yes' : 'no', $ad_cal ? 'NO' : 'yes', $pass ? 'OK' : 'FAIL' );
}
echo $ok ? "ALL OK\n" : "FAILED\n";
