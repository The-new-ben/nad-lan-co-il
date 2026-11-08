<?php
// Local test of inc/price-nudge.php pure logic with WordPress stubs (HAD-684). Run: php -d extension=mbstring tools/nudge/test_price_alert.php
define( 'ABSPATH', __DIR__ );
define( 'DAY_IN_SECONDS', 86400 );
define( 'HOUR_IN_SECONDS', 3600 );
$GLOBALS['T'] = array(); $GLOBALS['META'] = array(); $GLOBALS['TYPE'] = array();
function add_action() {} function add_filter() {} function register_rest_route() {}
function get_transient( $k ) { return $GLOBALS['T'][ $k ] ?? false; }
function set_transient( $k, $v, $t = 0 ) { $GLOBALS['T'][ $k ] = $v; return true; }
function get_post_meta( $id, $k, $s = false ) { return $GLOBALS['META'][ $id ][ $k ] ?? ''; }
function get_post_type( $id ) { return $GLOBALS['TYPE'][ $id ] ?? ''; }
function wp_strip_all_tags( $s ) { return strip_tags( $s ); }
require dirname( __DIR__, 2 ) . '/plugins/nadlan-config/inc/price-nudge.php';
$fail = 0;
function ok( $c, $m ) { global $fail; echo ( $c ? 'PASS ' : 'FAIL ' ) . $m . "\n"; if ( ! $c ) { $fail++; } }
// phones
foreach ( array( '050-123-4567' => '0501234567', '+972 50 123 4567' => '0501234567', '00972501234567' => '0501234567', '501234567' => '0501234567', '03-1234567' => '031234567', '077-1234567' => '0771234567', '12345' => '', '050123456' => '', 'abc' => '' ) as $in => $want ) {
	ok( nadlan_pa_phone( $in ) === $want, "phone $in -> " . nadlan_pa_phone( $in ) );
}
// the index
$ix = nadlan_pa_index();
ok( null !== $ix['nat'] && $ix['nat'] < 0, 'national 12m = ' . var_export( $ix['nat'], true ) . ' as of ' . $ix['asof'] );
ok( 6 === count( $ix['dist'] ), 'six districts: ' . json_encode( $ix['dist'], JSON_UNESCAPED_UNICODE ) );
// trends by city
$cases = array( 'תל אביב' => 'dist', 'תל אביב-יפו' => 'dist', 'רמת גן' => 'dist', 'קריית אתא' => 'dist', 'קרית אונו' => 'dist', 'ירושלים' => 'dist', 'יבנאל' => 'dist', 'כפר ורדים' => 'nat', '' => 'nat' );
$i = 100;
foreach ( $cases as $city => $src ) {
	$i++; $GLOBALS['TYPE'][ $i ] = 'nadlan_project'; $GLOBALS['META'][ $i ] = array( 'city' => $city );
	$t = nadlan_pa_trend( $i );
	ok( $t['src'] === $src && true === $t['down'], "trend '$city' -> " . json_encode( $t, JSON_UNESCAPED_UNICODE ) );
}
$GLOBALS['TYPE'][ 200 ] = 'nadlan_intl'; $GLOBALS['META'][ 200 ] = array( 'city' => 'דובאי' );
$t = nadlan_pa_trend( 200 );
ok( 'none' === $t['src'] && false === $t['down'] && '' === $t['city'], 'abroad has no arrow: ' . json_encode( $t, JSON_UNESCAPED_UNICODE ) );
// district mapping is right, not only the sign
$GLOBALS['TYPE'][ 201 ] = 'nadlan_project'; $GLOBALS['META'][ 201 ] = array( 'city' => 'חיפה' );
ok( abs( nadlan_pa_trend( 201 )['pct'] - $ix['dist']['חיפה'] ) < 0.001, 'Haifa uses the Haifa series' );
echo $fail ? "\n$fail FAILED\n" : "\nALL PASSED\n";
exit( $fail ? 1 : 0 );
