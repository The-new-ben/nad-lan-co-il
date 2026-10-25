<?php
/**
 * Local preview of the /projects/ hub (1.72.513): runs inc/projects-hub.php with small WordPress stand-ins and the plugin's
 * real data files, and writes preview.html (the hub as it will sit under the catalog grid, inside a page shell that loads the
 * site fonts). The tools are shown as their static panels (the live engine mounts them on the site).
 *   php docs/research/2026-10-25-projects-hub/preview/render.php
 */
define( 'ABSPATH', __DIR__ );
define( 'HOUR_IN_SECONDS', 3600 );
define( 'ARRAY_A', 'ARRAY_A' );
$GLOBALS['nlph_paged'] = isset( $argv[1] ) ? (int) $argv[1] : 0;
function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_attr( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_url( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function home_url( $p = '/' ) { return 'https://nad-lan.co.il' . $p; }
function plugins_url( $f, $base ) { return '/plugins/nadlan-config/' . $f; }
function add_query_arg( $k, $v, $u ) { return $u . ( false === strpos( $u, '?' ) ? '?' : '&' ) . $k . '=' . rawurlencode( $v ); }
function date_i18n( $f, $t ) { return date( $f, $t ); }
function get_transient( $k ) { return false; }
function set_transient( $k, $v, $t ) { return true; }
function add_action() {}
function add_filter() {}
function get_query_var( $k ) { return 'paged' === $k ? $GLOBALS['nlph_paged'] : ''; }
function is_post_type_archive( $t = '' ) { return true; }
function do_shortcode( $s ) {
	preg_match( '/id="([a-z]+)"/', $s, $m );
	return '<section class="nli"><div class="nli__panel" style="border:1px dashed #9AA6B0;border-radius:6px;padding:18px;background:#FBFCFD"><p class="nli__kicker" style="font:500 12px IBM Plex Mono,monospace;color:#5E6A75;margin:0">מחשבון</p><h2 class="nli__title" style="font:700 22px IBM Plex Sans Hebrew,sans-serif;color:#14213D;margin:4px 0">[' . $m[1] . ']</h2><p style="margin:0">המחשבון עולה כאן באתר החי.</p></div></section>';
}
class NLPH_DB {
	public $postmeta = 'wp_postmeta'; public $posts = 'wp_posts';
	function get_results( $q, $o = null ) {
		// the live counts from docs/research/2026-10-25-projects-hub/our-page.md (4.2)
		return array( array( 'v' => 'תכנית מאושרת לפני מימוש', 'n' => 334 ), array( 'v' => 'תכנון סטטוטורי', 'n' => 262 ), array( 'v' => 'תכנית מאושרת - אחרי רישוי', 'n' => 176 ),
			array( 'v' => 'תכנון ראשוני', 'n' => 115 ), array( 'v' => 'תכנית מאושרת במימוש', 'n' => 54 ), array( 'v' => 'בשיווק', 'n' => 5 ), array( 'v' => 'construction', 'n' => 3 ),
			array( 'v' => 'בבנייה', 'n' => 2 ), array( 'v' => 'בהקמה', 'n' => 2 ), array( 'v' => 'בתכנון', 'n' => 1 ), array( 'v' => 'בהיתר בנייה', 'n' => 1 ), array( 'v' => 'permits', 'n' => 1 ), array( 'v' => 'planning', 'n' => 1 ) );
	}
	function get_col( $q ) { $o = array(); for ( $i = 0; $i < 78; $i++ ) { $o[] = 'עיר ' . $i; } return $o; }
}
$wpdb = new NLPH_DB();
require dirname( __DIR__, 4 ) . '/plugins/nadlan-config/inc/projects-hub.php';
$facets = array( 'total' => 976, 'types' => array( 'pinui_binui' => 942, 'new_build' => 19, 'tama38' => 5 ), 'cities' => array() );
foreach ( array( 'ירושלים' => 197, 'תל אביב יפו' => 77, 'רמת גן' => 76, 'חיפה' => 44, 'נתניה' => 40, 'בת ים' => 37, 'פתח תקוה' => 37, 'הרצליה' => 25, 'חולון' => 25, 'גבעתים' => 24, 'חדרה' => 21, 'ראשון לציון' => 19, 'רמלה' => 17, 'אשדוד' => 17, 'קרית אונו' => 17, 'נהריה' => 15, 'יבנה' => 15, 'באר שבע' => 14, 'רחובות' => 14, 'טירת כרמל' => 14, 'לוד' => 13, 'כפר סבא' => 12 ) as $n => $c ) { $facets['cities'][] = array( 'name' => $n, 'n' => $c ); }
$body = nadlan_ph_body( $facets );
$shell = '<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>/projects/ hub preview</title>'
	. '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Hebrew:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">'
	. '<style>body{margin:0;background:#F7F8FA;font-family:"IBM Plex Sans Hebrew",sans-serif}.pv{background:#14213D;color:#fff;padding:14px max(16px,env(safe-area-inset-left,0px));font:500 13px "IBM Plex Mono",monospace}</style></head><body>'
	. '<div class="pv">Preview · the hub under the /projects/ grid · 1.72.513 · local data</div>' . $body . '</body></html>';
file_put_contents( __DIR__ . '/preview' . ( $GLOBALS['nlph_paged'] > 1 ? '-page2' : '' ) . '.html', $shell );
echo 'preview ' . strlen( $shell ) . " bytes\n";
