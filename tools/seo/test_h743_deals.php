<?php
/* HAD-743 local test: deals-map.php renders without notices, every deal has its fields, the JSON parses, and the page check works. */
error_reporting( E_ALL ); ini_set( 'display_errors', '1' );
define( 'ABSPATH', __DIR__ . '/' );
$GLOBALS['__filters'] = array(); $GLOBALS['__page'] = 'developer-deals';
function add_filter( $h, $f, $p = 10 ) { $GLOBALS['__filters'][ $h ][] = $f; }
function add_action( $h, $f, $p = 10 ) { $GLOBALS['__filters'][ $h ][] = $f; }
function get_option( $k, $d = false ) { return $d; }
function plugins_url( $p, $f ) { return 'https://nad-lan.co.il/wp-content/plugins/nadlan-config/' . $p; }
function esc_attr( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES ); }
function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES ); }
function esc_url( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES ); }
function wp_json_encode( $d, $f = 0 ) { return json_encode( $d, $f ); }
function home_url( $p = '/' ) { return 'https://nad-lan.co.il' . $p; }
function rest_url( $p = '' ) { return 'https://nad-lan.co.il/wp-json/' . $p; }
function is_page() { return true; }
function in_the_loop() { return true; }
function is_main_query() { return true; }
function get_queried_object() { return (object) array( 'post_name' => $GLOBALS['__page'] ); }
require __DIR__ . '/../../plugins/nadlan-config/inc/deals-map.php';
function nlrun( $c ) { $f = $GLOBALS['__filters']['the_content']; $c = $f[1]( $c ); return $f[0]( $c ); } // priority 6 (map) then 7 (discount section)
$fails = 0;
$ok = function ( $c, $m ) use ( &$fails ) { if ( ! $c ) { $fails++; echo "FAIL: $m\n"; } };
$deals = nadlan_dm_deals();
$ok( count( $deals ) === 17, 'seventeen deals' );
$ids = array();
foreach ( $deals as $d ) {
	foreach ( array( 'id', 'dev', 'devFull', 'project', 'city', 'lat', 'lng', 'color', 'k', 'kind', 'short', 'terms', 'bar', 'pub' ) as $f ) { $ok( isset( $d[ $f ] ) && '' !== $d[ $f ], $d['id'] . ' has ' . $f ); }
	$ok( $d['lat'] > 29.4 && $d['lat'] < 33.4 && $d['lng'] > 34.2 && $d['lng'] < 35.9, $d['id'] . ' inside Israel' );
	$sum = 0; foreach ( $d['bar'] as $b ) { $sum += $b[0]; } $ok( 100 === $sum, $d['id'] . ' bar sums to 100' );
	$ok( ! isset( $ids[ $d['id'] ] ), 'unique ' . $d['id'] ); $ids[ $d['id'] ] = 1;
}
$_SERVER['REQUEST_URI'] = '/developer-deals/';
$out = nlrun( '<p>ARTICLE</p>' );
$ok( 0 === strpos( $out, '<section id="nldm"' ), 'map section first' );
$ok( false !== strpos( $out, '<p>ARTICLE</p>' ), 'article kept' );
$ok( 1 === substr_count( $out, 'id="nldm-data"' ), 'one data block' );
preg_match( '~<script type="application/json" id="nldm-data">(.*?)</script>~s', $out, $m );
$j = json_decode( $m[1] ?? '', true );
$ok( is_array( $j ) && 17 === count( $j['deals'] ) && 'gindi-love' === $j['hotId'], 'json parses' );
$ok( 17 === substr_count( $out, 'data-pick=' ), 'seventeen list rows' );
$ok( false === strpos( $out, '<h1' ), 'no second h1' );
$ok( nlrun( $out ) === $out, 'no double insert' );
$o2 = nlrun( '<h1>H</h1><p>ARTICLE</p>' );
$ok( 0 === strpos( $o2, '<h1>H</h1><section id="nldm"' ), 'map right under the article h1' );
$art = '<h1>H</h1>' . str_repeat( '<h2>X</h2><p>t</p>', 10 );
$o3 = nlrun( $art );
$ok( 1 === substr_count( $o3, 'nldm-disc' ) - 0 + 0 || substr_count( $o3, 'id="nldm-disc-h"' ) === 1, 'discount section once' );
$ok( strpos( $o3, 'id="nldm-disc-h"' ) > strpos( $o3, 'id="nldm-data"' ) && substr_count( substr( $o3, 0, strpos( $o3, 'class="nldm nldm-disc"' ) ), '<h2>X</h2>' ) === 5, 'discount section after 5 of the 10 article h2 (the middle)' );
$ok( false !== strpos( $o3, 'href="/dira-behanacha/"' ) && false !== strpos( $o3, 'id="nldm-calc"' ), 'link to the state programme page; calculator present' );
$ok( false !== strpos( $out, 'id="nldm-alert"' ) && false !== strpos( $out, '"alertUrl":"https://nad-lan.co.il/wp-json/nadlan/v1/near-alerts"' ) && false !== strpos( $out, 'class="nldm-toalert"' ), 'area alert box, its endpoint and the button in the deal card' );
$ok( 1 === substr_count( $out, 'application/ld+json' ) && false !== strpos( $out, '"@type":"ApartmentComplex"' ) && false !== strpos( $out, '"@type":"Dataset"' ), 'Hebrew structured data' );
$_SERVER['REQUEST_URI'] = '/en/developer-deals/';
$en = nlrun( '<h1>E</h1><h2>a</h2><h2>b</h2>' );
$ok( 0 === strpos( $en, '<h1>E</h1><section id="nldm" class="nldm" dir="ltr" lang="en"' ), 'English map under the English h1' );
$ok( false === strpos( $en, 'nldm-disc' ) && 1 === substr_count( $en, 'application/ld+json' ) && false !== strpos( $en, 'Israel developer deals map' ), 'English: no Hebrew programme section, its own structured data' );
preg_match( '~<script type="application/json" id="nldm-data">(.*?)</script>~s', $en, $me ); $je = json_decode( $me[1] ?? '', true );
$ok( is_array( $je ) && 'en' === $je['lang'] && 17 === count( $je['deals'] ) && 'LOVE Glil Yam, Herzliya' === $je['deals'][0]['project'] && ! preg_match( '/[\x{05D0}-\x{05EA}]/u', implode( ' ', array_map( function ( $d ) { return $d['project'] . $d['terms'] . $d['kind'] . $d['short'] . implode( '', array_column( $d['bar'], 1 ) ); }, $je['deals'] ) ) ), 'English deals: all 17, no Hebrew left in their text' );
$ok( isset( $je['t']['בקשו מחיר'] ) && is_array( $je['fx'] ), 'English strings and dollar rate passed to the script' );
$_SERVER['REQUEST_URI'] = '/fr/developer-deals/';
$ok( '<p>X</p>' === nlrun( '<p>X</p>' ), 'not on /fr/' );
$GLOBALS['__page'] = 'projects'; $_SERVER['REQUEST_URI'] = '/projects/';
$ok( '<p>X</p>' === nlrun( '<p>X</p>' ), 'not on other pages' );
echo $fails ? "$fails failed\n" : "all passed\n";
exit( $fails ? 1 : 0 );
