<?php
/* HAD-768 local test: forms-hub.php renders the life of a building from assets/forms/forms.json without notices; every item has a
   title, stage, kind and source, a unique anchor; files are on our server; the data block parses; the schema prints.
   With an argument (a path), it also writes a harness page (the hub inside a plain page with the real CSS/JS) to look at locally. */
error_reporting( E_ALL ); ini_set( 'display_errors', '1' );
define( 'ABSPATH', __DIR__ . '/' );
define( 'NADLAN_CONFIG_VERSION', 'test' );
$GLOBALS['__h'] = array(); $GLOBALS['__sc'] = array();
function add_filter( $h, $f, $p = 10 ) { $GLOBALS['__h'][ $h ][] = $f; }
function add_action( $h, $f, $p = 10 ) { $GLOBALS['__h'][ $h ][] = $f; }
function add_shortcode( $t, $f ) { $GLOBALS['__sc'][ $t ] = $f; }
function plugins_url( $p, $f ) { return 'https://nad-lan.co.il/wp-content/plugins/nadlan-config/' . $p; }
function esc_attr( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES ); }
function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES ); }
function esc_url( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES ); }
function sanitize_title( $s ) { return strtolower( preg_replace( '/[^A-Za-z0-9\-\x{0590}-\x{05FF}]+/u', '-', trim( (string) $s ) ) ); }
function sanitize_key( $s ) { return preg_replace( '/[^a-z0-9_\-]/', '', strtolower( (string) $s ) ); }
function wp_json_encode( $d, $f = 0 ) { return json_encode( $d, $f ); }
function home_url( $p = '/' ) { return 'https://nad-lan.co.il' . $p; }
function is_singular( $t = '' ) { return true; }
function get_post() { return (object) array( 'post_content' => '<p>x</p>[nadlan_forms]<h2>שאלות נפוצות</h2><h3>ש1?</h3><p>ת1</p><h3>ש2?</h3><p>ת2</p>' ); }
function get_the_title( $p = null ) { return 'טפסי מקרקעין ואישורי בנייה'; }
function get_permalink( $p = null ) { return 'https://nad-lan.co.il/forms/'; }
function get_post_modified_time( $f, $g, $p ) { return '2026-11-17T20:00:00+00:00'; }
function rest_url( $p = '' ) { return 'https://nad-lan.co.il/wp-json/' . $p; }
function nadlan_nli_faq( $html ) { return array( array( '@type' => 'Question', 'name' => 'ש1?' ), array( '@type' => 'Question', 'name' => 'ש2?' ) ); }
require __DIR__ . '/../../plugins/nadlan-config/inc/forms-hub.php';
$fails = 0;
$ok = function ( $c, $m ) use ( &$fails ) { if ( ! $c ) { $fails++; echo "FAIL: $m\n"; } };
$d = nadlan_fh_data();
$ok( count( $d['items'] ) >= 150, 'at least 150 items (' . count( $d['items'] ) . ')' );
$sids = array(); foreach ( $d['stages'] as $s ) { $sids[ $s['id'] ] = 1; $ok( ! empty( $s['name'] ) && ! empty( $s['n'] ), 'stage ' . $s['id'] ); }
$ok( 11 === count( $sids ), 'eleven stages' );
$rids = array(); foreach ( $d['roles'] as $r ) { $rids[ $r['id'] ] = 1; }
$ids = array(); $files = 0;
foreach ( $d['items'] as $it ) {
	$id = sanitize_title( $it['id'] );
	$ok( ! isset( $ids[ $id ] ), 'unique id ' . $id ); $ids[ $id ] = 1;
	$ok( ! empty( $it['title'] ) && isset( $sids[ $it['stage'] ] ) && isset( $d['kinds'][ $it['kind'] ] ), $id . ' title, stage, kind' );
	$ok( ! empty( $it['sources'] ) && 0 === strpos( $it['sources'][0]['url'], 'http' ), $id . ' has a source' );
	foreach ( (array) ( isset( $it['roles'] ) ? $it['roles'] : array() ) as $r ) { $ok( isset( $rids[ $r ] ), $id . ' role ' . $r ); }
	if ( ! empty( $it['form']['file'] ) ) { $files++; $ok( 0 === strpos( $it['form']['file'], 'https://nad-lan.co.il/wp-content/uploads/' ), $id . ' file on our server' ); }
	foreach ( array( 'title', 'what', 'expert', 'pitfall' ) as $k ) { if ( ! empty( $it[ $k ] ) ) { $ok( false === strpos( $it[ $k ], '—' ) && false === strpos( $it[ $k ], '–' ), $id . ' no long dash in ' . $k ); } }
}
$ok( $files >= 60, 'at least 60 official files (' . $files . ')' );
$out = $GLOBALS['__sc']['nadlan_forms']();
$ok( 0 === strpos( $out, '<section class="nlfm" id="nlfm"' ), 'section' );
$ok( count( $d['items'] ) === substr_count( $out, '<article class="nlfm-card' ), 'one card per item' );
$ok( 11 === substr_count( $out, 'data-fm-stage=' ), 'eleven spine tiles' );
$ok( false === strpos( $out, '<h1' ), 'no h1 in the hub' );
$ok( false !== strpos( $out, 'id="fairness"' ), 'fairness declaration' );
preg_match( '~<script type="application/json" id="nlfm-data">(.*?)</script>~s', $out, $m );
$j = json_decode( $m[1] ?? '', true );
$ok( is_array( $j ) && count( $j['items'] ) === count( $d['items'] ) && 11 === count( $j['stages'] ), 'data block parses' );
ob_start(); foreach ( $GLOBALS['__h']['wp_head'] as $f ) { $f(); } $head = ob_get_clean();
preg_match( '~<script type="application/ld\+json" id="nadlan-forms-ld">(.*?)</script>~s', $head, $m2 );
$ld = json_decode( $m2[1] ?? '', true );
$types = is_array( $ld ) ? array_column( $ld['@graph'], '@type' ) : array();
$ok( in_array( 'HowTo', $types, true ) && in_array( 'Dataset', $types, true ) && ! empty( $ld['@graph'][0]['citation'] ) && ! empty( $ld['@graph'][0]['about'] ), 'deep schema: HowTo, Dataset, citation, about' );
$ok( false !== strpos( $out, 'id="numbers"' ) && substr_count( $out, '<tr><th scope="row">' ) === count( $d['facts'] ), 'key numbers table' );
$ok( is_array( $ld ) && 'CollectionPage' === $ld['@graph'][0]['@type'] && $ld['@graph'][0]['mainEntity']['numberOfItems'] === $files && in_array( 'FAQPage', $types, true ), 'schema' );
if ( ! empty( $argv[1] ) ) {
	$css = file_get_contents( __DIR__ . '/../../plugins/nadlan-config/assets/forms/forms.css' );
	$js  = file_get_contents( __DIR__ . '/../../plugins/nadlan-config/assets/forms/forms.js' );
	$page = '<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>forms harness</title>'
		. '<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans+Hebrew:wght@400;500;600;700&family=Karantina:wght@700&display=swap" rel="stylesheet">'
		. '<style>body{margin:0;background:#F6F8F9;font-family:"IBM Plex Sans Hebrew",sans-serif}.wrap{max-width:1240px;margin:0 auto;padding:16px}h1{font:700 34px/1.25 "IBM Plex Sans Hebrew";margin:8px 0}</style><style>' . $css . '</style></head><body><div class="wrap">'
		. '<h1>טפסי מקרקעין ואישורי בנייה: מהתכנון ועד ההריסה</h1><p>פסקת הפתיחה של העמוד.</p>' . $out . '</div><script>' . $js . '</script></body></html>';
	file_put_contents( $argv[1], $page );
	echo "harness -> {$argv[1]}\n";
}
echo $fails ? "$fails failed\n" : "all passed\n";
exit( $fails ? 1 : 0 );
