<?php
/* HAD-743 local test of inc/deal-alerts.php: first run marks what is there as seen (no mail), a new deal inside the area is collected
 * once, a deal outside the radius never, the mail block names terms, source and "not advice". */
error_reporting( E_ALL ); ini_set( 'display_errors', '1' );
define( 'ABSPATH', __DIR__ . '/' );
$GLOBALS['F'] = array(); $GLOBALS['M'] = array(); $GLOBALS['DEALS'] = array();
function add_filter( $h, $f, $p = 10, $n = 1 ) { $GLOBALS['F'][ $h ] = $f; }
function add_action( $h, $f, $p = 10, $n = 1 ) { $GLOBALS['F'][ $h ] = $f; }
function get_post_meta( $id, $k, $s = false ) { return $GLOBALS['M'][ $id ][ $k ] ?? ''; }
function update_post_meta( $id, $k, $v ) { $GLOBALS['M'][ $id ][ $k ] = $v; return true; }
function wp_list_pluck( $a, $k ) { return array_map( function ( $x ) use ( $k ) { return $x[ $k ]; }, $a ); }
function home_url( $p = '/' ) { return 'https://nad-lan.co.il' . $p; }
function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES ); }
function esc_url( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES ); }
function nadlan_dm_deals() { return $GLOBALS['DEALS']; }
function nadlan_na_km( $a, $b, $c, $d ) { $k = cos( deg2rad( $a ) ) * 111.32; return sqrt( pow( ( $d - $b ) * $k, 2 ) + pow( ( $c - $a ) * 110.57, 2 ) ); }
function nadlan_na_h2( $t ) { return '<h2>' . $t . '</h2>'; }
function nadlan_na_card( $r, $in ) { return '<div>' . $in . '</div>'; }
function nadlan_na_button( $u, $t ) { return '<a href="' . $u . '">' . $t . '</a>'; }
require __DIR__ . '/../../plugins/nadlan-config/inc/deal-alerts.php';
$fails = 0; $ok = function ( $c, $m ) use ( &$fails ) { if ( ! $c ) { $fails++; echo "FAIL: $m\n"; } };
$deal = function ( $id, $lat, $lng ) { return array( 'id' => $id, 'lat' => $lat, 'lng' => $lng, 'devFull' => 'D', 'city' => 'C', 'project' => 'P ' . $id, 'kind' => 'K', 'terms' => 'T', 'pub' => 'נובמבר 2026', 'src' => 'https://src.example/' ); };
$GLOBALS['DEALS'] = array( $deal( 'a', 32.075, 34.79 ), $deal( 'far', 31.25, 34.79 ) );
$s = array( 'id' => 7, 'what' => array( 'deal' ), 'p' => array( 'lat' => 32.075, 'lng' => 34.79, 'r' => 3 ) );
$col = $GLOBALS['F']['nadlan_na_collect_more'];
$o1 = $col( array( 'new' => array(), 'drop' => array(), 'proj' => array() ), $s, time(), null );
$ok( array() === $o1['deal'] && array( 'a' ) === $GLOBALS['M'][7]['nf_dseen'], 'first run: nothing sent, the deal already there is marked seen' );
$GLOBALS['DEALS'][] = $deal( 'b', 32.09, 34.80 ); // about 1.8 km away: inside 3 km
$o2 = $col( array( 'new' => array(), 'drop' => array(), 'proj' => array() ), $s, time(), null );
$ok( 1 === count( $o2['deal'] ) && 'b' === $o2['deal'][0]['id'], 'a new deal inside the area is collected, the far one is not' );
$GLOBALS['F']['nadlan_na_sent']( 7, $o2 );
$o3 = $col( array( 'new' => array(), 'drop' => array(), 'proj' => array() ), $s, time(), null );
$ok( array() === $o3['deal'], 'after the mail went out it is not sent again' );
$o4 = $col( array( 'new' => array(), 'drop' => array(), 'proj' => array() ), array( 'id' => 8, 'what' => array( 'new' ), 'p' => $s['p'] ), time(), null );
$ok( array() === $o4['deal'] && ! isset( $GLOBALS['M'][8] ), 'a row without "deal" is untouched' );
list( $b, $t ) = $GLOBALS['F']['nadlan_na_mail_more']( array( '', '' ), $s, $o2 );
$ok( false !== strpos( $b, 'P b' ) && false !== strpos( $b, 'https://src.example/' ) && false !== strpos( $b, 'זה לא ייעוץ' ) && false !== strpos( $t, 'P b' ), 'mail block: project, source, not advice, text twin' );
echo $fails ? "$fails failed\n" : "all passed\n";
exit( $fails ? 1 : 0 );
