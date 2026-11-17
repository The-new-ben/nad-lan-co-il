<?php
/* HAD-743 local test of inc/deals-guide.php: every deal has a line and a "worth checking" line, every number she says is in the
 * deal as published, no selling words, every line id the script uses exists, the gate, and a clip plays only for its own text. */
error_reporting( E_ALL ); ini_set( 'display_errors', '1' );
define( 'ABSPATH', __DIR__ . '/' );
$GLOBALS['__filters'] = array(); $GLOBALS['__page'] = 'developer-deals'; $GLOBALS['__opt'] = array();
function add_filter( $h, $f, $p = 10 ) { $GLOBALS['__filters'][ $h ][] = $f; }
function add_action( $h, $f, $p = 10 ) { $GLOBALS['__filters'][ $h ][] = $f; }
function get_option( $k, $d = false ) { return $GLOBALS['__opt'][ $k ] ?? $d; }
function plugins_url( $p, $f ) { return 'https://nad-lan.co.il/wp-content/plugins/nadlan-config/' . $p; }
function esc_attr( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES ); }
function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES ); }
function esc_url( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES ); }
function wp_json_encode( $d, $f = 0 ) { return json_encode( $d, $f ); }
function home_url( $p = '/' ) { return 'https://nad-lan.co.il' . $p; }
function rest_url( $p = '' ) { return 'https://nad-lan.co.il/wp-json/' . $p; }
function is_page() { return true; }
function get_queried_object() { return (object) array( 'post_name' => $GLOBALS['__page'] ); }
require __DIR__ . '/../../plugins/nadlan-config/inc/deals-map.php';
require __DIR__ . '/../../plugins/nadlan-config/inc/deals-guide.php';
$fails = 0;
$ok = function ( $c, $m ) use ( &$fails ) { if ( ! $c ) { $fails++; echo "FAIL: $m\n"; } };

$deals = nadlan_dm_deals();
$L     = nadlan_dg_lines();
foreach ( $deals as $d ) {
	$ok( isset( $L[ 'd-' . $d['id'] ], $L[ 'c-' . $d['id'] ] ), $d['id'] . ' has a line and a check line' );
	/* every number she says about a deal is in what was published (terms, kind, project) */
	$src = str_replace( ',', '', $d['terms'] . ' ' . $d['kind'] . ' ' . $d['project'] );
	preg_match_all( '~\d+(?:[.,]\d+)*~', str_replace( ',', '', ( $L[ 'd-' . $d['id'] ] ?? '' ) . ' ' . ( $L[ 'c-' . $d['id'] ] ?? '' ) ), $m );
	foreach ( $m[0] as $num ) { $ok( false !== strpos( $src, $num ), $d['id'] . ': the number ' . $num . ' is in the published deal' ); }
}
$ok( count( nadlan_dg_deal_lines() ) === count( $deals ), 'no line for a deal that is not on the map' );
/* she never sells and never claims to be a broker */
foreach ( $L as $id => $t ) {
	$ok( false === strpos( $t, 'כדאי' ) && false === strpos( $t, 'הזדמנות' ) && false === strpos( $t, 'מומלץ' ) && false === strpos( $t, 'אל תפספס' ), $id . ': no selling words' );
	$ok( false === strpos( $t, 'מתווכ' ) || false !== strpos( $t, 'לא מתווכת' ), $id . ': never a broker' );
	$ok( false === strpos( $t, 'ממליצ' ) || false !== strpos( $t, 'לא ממליצה' ), $id . ': "recommend" only in "I do not recommend"' );
	$ok( mb_strlen( $t ) <= 240, $id . ': short enough to say (' . mb_strlen( $t ) . ')' );
}
/* every id the script asks for exists */
$js = file_get_contents( __DIR__ . '/../../plugins/nadlan-config/assets/deals/guide.js' );
preg_match_all( "~(?:say|unasked|react|topic)\\('([a-z0-9]+)'\\s*[,)]~", $js, $u );
foreach ( array_unique( $u[1] ) as $id ) { $ok( isset( $L[ $id ] ), 'the script line ' . $id . ' exists' ); }
foreach ( array( 'who', 'best', 'q2080', 'qzero', 'qtrue', 'qloan', 'qindex', 'qbank', 'qvalid', 'qrent', 'alert', 'near0', 'ret0', 'nr', 'greet', 'hello' ) as $id ) { $ok( isset( $L[ $id ] ), $id . ' exists' ); }
for ( $i = 0; $i <= count( $deals ); $i++ ) { $ok( isset( $L[ 'cash' . $i ] ), 'cash' . $i . ' exists' ); }
for ( $i = 1; $i <= 8; $i++ ) { $ok( isset( $L[ 'near' . $i ], $L[ 'ret' . $i ] ), 'near/ret ' . $i ); }
$ok( false !== strpos( $L['cash2'], 'שני מבצעים' ) && false !== strpos( $L['greet'], 'שבעה עשר המבצעים' ), 'Hebrew counting forms' );
/* gate: Hebrew page with ?guide=on, or the option; never the English page */
$_SERVER['REQUEST_URI'] = '/developer-deals/'; $_GET = array();
$ok( nadlan_dg_on(), 'public on the Hebrew page, no switch' );
$_SERVER['REQUEST_URI'] = '/en/developer-deals/';
$ok( ! nadlan_dg_on(), 'never on the English page' );
$_SERVER['REQUEST_URI'] = '/developer-deals/'; $GLOBALS['__opt']['nadlan_dg'] = 'off';
$ok( ! nadlan_dg_on(), 'the option off takes her off' ); $GLOBALS['__opt']['nadlan_dg'] = 'on';
$GLOBALS['__page'] = 'projects'; $ok( ! nadlan_dg_on(), 'never on another page' ); $GLOBALS['__page'] = 'developer-deals';
/* a clip plays only for the exact text it says */
$GLOBALS['__opt']['nadlan_dg_clips'] = array(
	'greet' => array( 'f' => 'nadlan-guide/greet.mp3', 'h' => substr( md5( $L['greet'] ), 0, 8 ) ),
	'who'   => array( 'f' => 'nadlan-guide/who.mp3', 'h' => 'deadbeef' ),
);
$P = nadlan_dg_payload();
$ok( 2 === count( $P['lines']['greet'] ) && false !== strpos( $P['lines']['greet'][1], 'nadlan-guide/greet.mp3' ), 'a matching clip is used' );
$ok( 1 === count( $P['lines']['who'] ), 'a clip of another text is never played' );
$ok( false !== strpos( $P['lead'], '/wp-json/nadlan/v1/lead' ) && false !== strpos( $P['consent'], 'לפי רצונכם' ) && false !== strpos( $P['consent'], 'info@nad-lan.co.il' ), 'the lead address and the consent line' );
foreach ( $L as $id => $t ) { $ok( false === strpos( $t, 'וידאו' ) && false === strpos( $t, 'וואטסאפ' ), $id . ': offers details, not a video call or WhatsApp' ); }
$js = file_get_contents( __DIR__ . '/../../plugins/nadlan-config/assets/deals/guide.js' );
$ok( false === strpos( $js, 'וידאו' ) && false === strpos( $js, 'href: wa(' ), 'the script offers no video call and no WhatsApp' );
$ok( 4 === count( $P['face'] ) && is_array( json_decode( json_encode( $P, JSON_UNESCAPED_UNICODE ), true ) ), 'payload is JSON' );
echo $fails ? "$fails failed\n" : "all passed (" . count( $L ) . " lines)\n";
exit( $fails ? 1 : 0 );
