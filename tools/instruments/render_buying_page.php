<?php
/**
 * HAD-683 (from render_prices_page.php): render the /buying-apartment/ content file the way WordPress would print it, locally, with the REAL inc/instruments.php:
 * every [nadlan_tool id="…"] goes through the registered shortcode (the server summary with real numbers, the data URLs, the
 * related links), and the wp_head JSON-LD the engine prints (SoftwareApplication per tool + FAQPage from the page's own
 * "שאלות נפוצות" section) is printed too. No network, no WordPress, no writes outside the output path.
 *
 *   php tools/instruments/render_prices_page.php <content.html> <out-content.html> <out-head-jsonld.json> [<asset-base-url>]
 *
 * asset-base-url: what plugins_url() returns for the plugin root (default: ../../plugins/nadlan-config/, right for a harness in
 * tools/instruments/). Exit 1 when a shortcode in the content is not registered or renders empty.
 */
error_reporting( E_ALL );
define( 'ABSPATH', __DIR__ . '/' );
define( 'NADLAN_CONFIG_VERSION', 'local' );
$GLOBALS['SC'] = array(); $GLOBALS['HOOKS'] = array();
$BASE = isset( $argv[4] ) ? $argv[4] : '../../plugins/nadlan-config/';
function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_attr( $s ) { return esc_html( $s ); }
function esc_url( $s ) { return esc_html( $s ); }
function home_url( $p = '' ) { return $p; }  // relative links in the local preview
function plugins_url( $p, $f ) { return $GLOBALS['BASE'] . ltrim( $p, '/' ); }
function add_shortcode( $t, $cb ) { $GLOBALS['SC'][ $t ] = $cb; }
function add_action( $h, $cb = null, $p = 10, $n = 1 ) { $GLOBALS['HOOKS'][ $h ][] = $cb; }
function add_filter( $h, $cb = null, $p = 10, $n = 1 ) { $GLOBALS['HOOKS'][ $h ][] = $cb; }
function apply_filters( $t, $v ) { $a = func_get_args(); array_shift( $a ); foreach ( isset( $GLOBALS['HOOKS'][ $t ] ) ? $GLOBALS['HOOKS'][ $t ] : array() as $cb ) { $a[0] = call_user_func_array( $cb, $a ); } return $a[0]; }  // real filters: the module adds its tools and its summaries
function shortcode_atts( $d, $a ) { $o = array(); foreach ( $d as $k => $v ) { $o[ $k ] = isset( $a[ $k ] ) ? $a[ $k ] : $v; } return $o; }
function sanitize_key( $k ) { return preg_replace( '/[^a-z0-9_\-]/', '', strtolower( (string) $k ) ); }
function sanitize_text_field( $s ) { return trim( strip_tags( (string) $s ) ); }
function wp_json_encode( $d, $o = 0 ) { return json_encode( $d, $o ); }
function wp_strip_all_tags( $t, $r = false ) { $t = preg_replace( '@<(script|style)[^>]*?>.*?</\1>@si', '', (string) $t ); $t = strip_tags( $t ); return $r ? preg_replace( '/[\r\n\t ]+/', ' ', $t ) : $t; }
function date_i18n( $f, $t = null ) { return date( $f, null === $t ? time() : $t ); }
function get_transient( $k ) { return false; } function set_transient() { return true; } function delete_transient() { return true; }
function is_singular() { return true; } function is_post_type_archive() { return false; } function get_query_var( $k ) { return ''; }
function get_permalink() { return 'https://nad-lan.co.il/buying-apartment/'; }
$GLOBALS['POST'] = null;
function get_post() { return $GLOBALS['POST']; }
function get_option( $k, $d = false ) { return $d; }

$in = $argv[1]; $out = $argv[2]; $ld = $argv[3];
$content = file_get_contents( $in );
$GLOBALS['POST'] = (object) array( 'ID' => 9, 'post_type' => 'page', 'post_content' => $content );
require dirname( __DIR__, 2 ) . '/plugins/nadlan-config/inc/instruments.php';
require dirname( __DIR__, 2 ) . '/plugins/nadlan-config/inc/buying-hub.php';  // the module (nadlan-config.php loads it at release)
if ( empty( $GLOBALS['SC']['nadlan_tool'] ) ) { fwrite( STDERR, "the nadlan_tool shortcode is not registered\n" ); exit( 1 ); }
$bad = array();
$html = preg_replace_callback( '/\[nadlan_tool\s+([^\]]*)\]/', function ( $m ) use ( &$bad ) {
	preg_match_all( '/([a-z]+)="([^"]*)"/', $m[1], $kv, PREG_SET_ORDER ); $a = array(); foreach ( $kv as $x ) { $a[ $x[1] ] = $x[2]; }
	$h = call_user_func( $GLOBALS['SC']['nadlan_tool'], $a );
	$h = apply_filters( 'do_shortcode_tag', $h, 'nadlan_tool', $a, null );  // WordPress runs this after every shortcode
	if ( '' === trim( (string) $h ) || false === strpos( $h, 'nli__panel' ) ) { $bad[] = $m[0]; }
	return $h;
}, $content );
// a shortcode of another live module (not loaded here): kept as a marker the harness fills from the live page
$html = preg_replace( '/\[nadlan_price_guide key="apartment-prices"\]/', '<!--nlpg-live-->', $html, -1, $nlpg );
echo 'live-only shortcodes left as markers: ' . (int) $nlpg . "
";
if ( preg_match_all( '/\[[a-z_]+[^\]]*\]/', $html, $left ) ) { foreach ( $left[0] as $l ) { if ( 0 === strpos( $l, '[nadlan_' ) ) { $bad[] = 'unrendered ' . $l; } } }
// the engine's wp_head graph (SoftwareApplication per tool, FAQPage from the content)
$graph = array(); $tools = nadlan_nli_tools();
foreach ( nadlan_nli_ids_in( $content ) as $id ) { $t = $tools[ $id ]; $graph[] = array( '@type' => 'SoftwareApplication', 'name' => $t['name'], 'description' => $t['desc'], 'applicationCategory' => $t['cat'] ); }
$faq = nadlan_nli_faq( $content ); if ( $faq ) { $graph[] = array( '@type' => 'FAQPage', 'mainEntity' => $faq ); }
$bfaq = nadlan_bhub_faq( $content ); if ( $bfaq ) { $graph[] = array( '@type' => 'FAQPage', 'mainEntity' => $bfaq ); } $faq = array_merge( $faq, $bfaq );
foreach ( nadlan_nli_ids_in( $content ) as $id ) { if ( in_array( $id, nadlan_bhub_tool_ids(), true ) && false === strpos( $html, 'data-bhub-sum="' . $id . '"' ) ) { $bad[] = 'no server summary for ' . $id; } }
file_put_contents( $out, $html );
file_put_contents( $ld, json_encode( array( '@context' => 'https://schema.org', '@graph' => $graph ), JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES ) );
// the engine's own data checks: every tool's data file exists, deps exist
$miss = array();
foreach ( nadlan_nli_ids_in( $content ) as $id ) {
	$t = $tools[ $id ]; $dir = dirname( __DIR__, 2 ) . '/plugins/nadlan-config/assets/instruments/';
	foreach ( $t['data'] as $f ) { if ( ! is_readable( $dir . 'data/' . $f ) ) { $miss[] = $id . ': data/' . $f; } }
	foreach ( isset( $t['deps'] ) ? $t['deps'] : array() as $d ) { if ( ! is_readable( $dir . 'tools/' . $d . '.js' ) ) { $miss[] = $id . ': tools/' . $d . '.js'; } }
	$file = ! empty( $t['file'] ) ? $t['file'] : $id; if ( ! is_readable( $dir . 'tools/' . $file . '.js' ) ) { $miss[] = $id . ': tools/' . $file . '.js'; }
}
echo 'tools: ' . implode( ', ', nadlan_nli_ids_in( $content ) ) . ' | FAQ questions: ' . count( $faq ) . ' | graph nodes: ' . count( $graph ) . "\n";
if ( $bad || $miss ) { fwrite( STDERR, "FAILED: " . implode( '; ', array_merge( $bad, $miss ) ) . "\n" ); exit( 1 ); }
echo "OK\n";
