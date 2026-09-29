<?php
// renders the site pill + ConsultSheet from the local plugin code (WordPress stubbed): php cta_harness.php <review|plain> <lang>
define( 'ABSPATH', __DIR__ . '/' );
$GLOBALS['H'] = array();
function add_action( $h, $cb, $p = 10 ) { $GLOBALS['H'][ $h ][] = $cb; }
function add_filter() {} function register_rest_route() {}
function is_admin() { return false; } function get_option( $k, $d = '' ) { return 'nadlan_owner_whatsapp' === $k ? getenv( 'NL_SITE_WA' ) : $d; }
function esc_attr( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES ); } function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES ); }
function esc_url( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES ); } function wp_json_encode( $v, $f = 0 ) { return json_encode( $v, $f ); }
$MODE = $argv[1] ?? 'review'; $LANG = $argv[2] ?? 'he';
function is_singular( $t = '' ) { return 'review' === $GLOBALS['MODE']; } function get_queried_object_id() { return 1; }
function nadlan_project_mode() { return 'review'; } function nadlan_project_self_lang() { return $GLOBALS['LANG'] === 'he' ? '' : $GLOBALS['LANG']; }
function nadlan_current_lang() { return $GLOBALS['LANG']; } function nadlan_lang_is_rtl( $l ) { return in_array( $l, array( 'he', 'ar' ), true ); }
$PN = dirname( __DIR__, 2 ) . '/plugins/nadlan-config';
$I18N = array();
function nadlan_i18n( $k ) { static $m = null; if ( null === $m ) { $src = file_get_contents( $GLOBALS['PN'] . '/inc/i18n.php' ); $m = array();
	foreach ( array( 'cta_wa_b', 'cta_wa_s', 'cta_wa_aria', 'cta_wa_msg' ) as $kk ) { if ( preg_match_all( "/'" . $kk . "' => '([^']*)'/u", $src, $mm ) ) { $m[ $kk ] = $mm[1]; } } }
	$i = array_search( $GLOBALS['LANG'], array( 'he', 'en', 'fr', 'ru', 'ar' ), true ); return $m[ $k ][ $i ] ?? ''; }
require $PN . '/inc/cta-sheet.php';
require $PN . '/inc/conversion-cta.php';
ob_start(); foreach ( $GLOBALS['H']['wp_footer'] as $cb ) { $cb(); } echo ob_get_clean();
