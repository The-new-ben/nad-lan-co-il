<?php
/**
 * Renders what inc/project-stage.php prints for one project page, WITHOUT WordPress (the WordPress functions it calls are
 * stubbed below; the plugin's real assets folder is read, so every is_readable() gate answers as on the server).
 *
 *   php scripts/project-stage/ps_render_harness.php <project-stage.php> <slug> [<pre-compose.html>]
 *
 * Prints one JSON object: the stage config of that slug, nadlan_ps_current(), the composed page (nadlan_ps_compose on the
 * given pre-compose HTML, or on a small synthetic page), and every wp_head / wp_footer piece the file hooks, by priority.
 * Used by ps_identity_proof.py (the four stage projects byte for byte, before and after KikarHamedinaWorld) and by
 * preview_hamedina.py (the Kikar Hamedina page top, rendered for the local preview). Env: NL_SITE_WA (the site's WhatsApp
 * number, digits), NL_VER (the plugin version printed in ?ver=), NL_LAT / NL_LNG (post meta lat/lng).
 */
error_reporting( E_ALL & ~E_DEPRECATED );
$file = $argv[1] ?? '';
$slug = $argv[2] ?? '';
$pre  = $argv[3] ?? '';
$PLUG = str_replace( '\\', '/', dirname( __DIR__, 2 ) . '/plugins/nadlan-config' );
define( 'ABSPATH', $PLUG . '/' );
define( 'NADLAN_CONFIG_VERSION', getenv( 'NL_VER' ) ?: '1.72.368' );
$GLOBALS['NL_SLUG'] = $slug;
$GLOBALS['NL_HOOKS'] = array();

function add_action( $h, $cb, $p = 10 ) { $GLOBALS['NL_HOOKS'][ $h ][ $p ][] = $cb; }
function add_filter( $h, $cb, $p = 10 ) { $GLOBALS['NL_HOOKS'][ 'filter:' . $h ][ $p ][] = $cb; }
function add_meta_box() {}
function is_admin() { return false; }
function is_singular( $t = '' ) { return true; }
function get_queried_object_id() { return 101; }
function get_post_field( $f, $id = 0 ) { return 'post_name' === $f ? $GLOBALS['NL_SLUG'] : ''; }
function get_option( $k, $d = false ) { return $d; }
function post_password_required() { return false; }
function get_post_meta( $id, $k = '', $single = false ) {
	if ( 'lat' === $k ) { return getenv( 'NL_LAT' ) ?: ''; }
	if ( 'lng' === $k ) { return getenv( 'NL_LNG' ) ?: ''; }
	return '';
}
function get_post_type() { return ''; }
function get_post_status() { return ''; }
function nadlan_project_mode() { return 'review'; }
function nadlan_cta_whatsapp_number() { return getenv( 'NL_SITE_WA' ) ?: '972525101555'; }
function nlds_icon( $n ) { return '<svg class="nlds-ico" data-i="' . $n . '"></svg>'; }
function nadlan_sched_on() { return true; }
function home_url( $p = '/' ) { return 'https://nad-lan.co.il' . $p; }
function plugins_url( $path = '', $plugin = '' ) { return 'https://nad-lan.co.il/wp-content/plugins/nadlan-config/' . ltrim( $path, '/' ); }
function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_attr( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_url( $s ) { return str_replace( '&', '&#038;', (string) $s ); }
function wp_json_encode( $v, $f = 0 ) { return json_encode( $v, $f ); }
function wp_strip_all_tags( $s ) { return trim( strip_tags( preg_replace( '#<(script|style)[^>]*?>.*?</\1>#si', '', (string) $s ) ) ); }
function wp_kses( $s, $allowed ) { return strip_tags( (string) $s, '<' . implode( '><', array_keys( (array) $allowed ) ) . '>' ); }
function sanitize_key( $s ) { return strtolower( preg_replace( '/[^a-z0-9_\-]/i', '', (string) $s ) ); }
function wp_unslash( $s ) { return $s; }
function get_permalink() { return 'https://nad-lan.co.il/projects/' . $GLOBALS['NL_SLUG'] . '/'; }

// the file under test, read from wherever it is but run as if it sat in the plugin's inc/ folder (the real assets beside it)
$src = file_get_contents( $file );
if ( false === $src ) { fwrite( STDERR, "no file $file\n" ); exit( 2 ); }
$src = str_replace( array( 'dirname( __DIR__ )', 'dirname( __FILE__ )' ), array( "'" . $PLUG . "'", "'" . $PLUG . "/inc'" ), $src );
eval( '?>' . $src );

$out = array( 'file_md5' => md5_file( $file ), 'slug' => $slug );
$all = nadlan_ps_config();
$base = preg_replace( '/-(en|fr|ru|ar)$/', '', $slug );
$out['config'] = isset( $all[ $base ] ) ? json_encode( $all[ $base ], JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) : null;
$ps = nadlan_ps_current();
$out['current'] = $ps ? json_encode( $ps, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) : null;
if ( $pre && is_readable( $pre ) ) {
	$html = file_get_contents( $pre );
} else {
	$html = '<!doctype html><html><head><title>t</title></head><body><nav class="nlptop" aria-label="b"><div>crumbs</div></nav>'
		. '<main><h1 id="nl-project-page-title" class="screen-reader-text">TITLE OF ' . $slug . '</h1>'
		. '<div class="nl-lead"><p>An answer paragraph long enough to be the lead of the page, with the names, the place, the status and a sourced price line.</p></div>'
		. '<aside class="nlcp-projctx">area prices</aside>'
		. '<section id="nlpjx-map" class="nlpjx-sec" aria-label="m"><h2>map</h2><div id="nlpjx-unimap"></div></section>'
		. '<div class="bottom-line"><strong>שורה תחתונה:</strong> a bottom line</div>'
		. '<h2>שאלות נפוצות</h2><h3>q1</h3><p>a1</p><h3>q2</h3><p>a2</p>'
		. '<aside class="nl-projnotice" dir="rtl" role="note"><b>n</b><span>n</span></aside><div class="nadlan-project-article">article</div></main></body></html>';
}
$out['composed'] = $ps ? nadlan_ps_compose( $html, $ps ) : null;
foreach ( array( 'wp_head', 'wp_footer' ) as $h ) {
	$pr = $GLOBALS['NL_HOOKS'][ $h ] ?? array();
	ksort( $pr );
	foreach ( $pr as $p => $cbs ) {
		foreach ( $cbs as $i => $cb ) {
			ob_start();
			try { $cb(); } catch ( \Throwable $e ) { echo 'THROW ' . $e->getMessage(); }
			$out[ $h ][ $p . '#' . $i ] = ob_get_clean();
		}
	}
}
echo json_encode( $out, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT );
