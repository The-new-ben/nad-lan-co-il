<?php
/**
 * Local preview of /xx/projects/ (1.72.514): runs inc/projects-hub.php + inc/projects-hub-lang.php with WordPress stand-ins and
 * the plugin's real data files; writes preview-<lang>.html.  php render_lang.php en
 */
define( 'ABSPATH', __DIR__ ); define( 'HOUR_IN_SECONDS', 3600 ); define( 'ARRAY_A', 'ARRAY_A' ); define( 'OBJECT', 'OBJECT' );
$lang = $argv[1] ?? 'en';
function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_attr( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_url( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function home_url( $p = '/' ) { return 'https://nad-lan.co.il' . $p; }
function untrailingslashit( $s ) { return rtrim( $s, '/' ); }
function plugins_url( $f, $b ) { return '/plugins/nadlan-config/' . $f; }
function add_query_arg( $k, $v, $u ) { return $u . ( false === strpos( $u, '?' ) ? '?' : '&' ) . $k . '=' . rawurlencode( $v ); }
function date_i18n( $f, $t ) { return date( $f, $t ); }
function get_transient( $k ) { return false; } function set_transient( $k, $v, $t ) { return true; }
function add_action() {} function add_filter() {} function add_shortcode() {}
function get_query_var( $k ) { return 0; } function is_post_type_archive( $t = '' ) { return false; } function is_page() { return true; }
function get_permalink( $id = 0 ) { return $id ? 'https://nad-lan.co.il/projects/sample-' . $id . '/' : 'https://nad-lan.co.il/' . $GLOBALS['lang'] . '/projects/'; }
function get_the_title( $id ) { return 'Featured project ' . $id; } function get_the_post_thumbnail_url( $id, $s ) { return ''; }
function get_post_meta( $id, $k, $s ) { return 'תל אביב יפו'; } function get_post_field( $f, $id ) { return 'sample-' . $id . '-en'; } function get_page_by_path( $p, $o, $t ) { return null; }
function get_post_type_archive_link( $t ) { return 'https://nad-lan.co.il/projects/'; }
function wp_strip_all_tags( $s ) { return strip_tags( $s ); } function wp_json_encode( $d, $f = 0 ) { return json_encode( $d, $f ); }
function sanitize_key( $s ) { return strtolower( preg_replace( '/[^a-z0-9_\-]/i', '', $s ) ); }
function shortcode_atts( $d, $a ) { return array_merge( $d, (array) $a ); }
function do_shortcode( $s ) { preg_match( '/id="([a-z]+)"/', $s, $m ); return '<section class="nli"><div class="nli__panel" style="border:1px dashed #9AA6B0;border-radius:6px;padding:16px;background:#FBFCFD"><b>[' . $m[1] . ' tool]</b> mounts here on the live site.</div></section>'; }
class NLPH_DB { public $postmeta = 'wp_postmeta'; public $posts = 'wp_posts';
	function get_results( $q, $o = null ) { return array( array( 'v' => 'תכנון סטטוטורי', 'n' => 262 ) ); }
	function get_col( $q ) { if ( false !== strpos( $q, "post_name LIKE" ) ) { return array( 101, 102, 103, 104, 105, 106 ); } $o = array(); for ( $i = 0; $i < 78; $i++ ) { $o[] = 'c' . $i; } return $o; }
	function prepare( $q ) { $a = func_get_args(); array_shift( $a ); foreach ( $a as $x ) { $q = preg_replace( '/%s/', "'" . $x . "'", $q, 1 ); } return $q; }
	function esc_like( $s ) { return $s; } }
$wpdb = new NLPH_DB(); $GLOBALS['lang'] = $lang;
function nadlan_dir_project_facets() { $c = array(); foreach ( array( 'ירושלים' => 197, 'תל אביב יפו' => 77, 'רמת גן' => 76, 'חיפה' => 44, 'נתניה' => 40, 'בת ים' => 37, 'פתח תקוה' => 37, 'הרצליה' => 25, 'חולון' => 25, 'באר שבע' => 14, 'רחובות' => 14, 'כפר סבא' => 12 ) as $n => $k ) { $c[] = array( 'name' => $n, 'n' => $k ); } return array( 'total' => 976, 'types' => array(), 'cities' => $c ); }
require dirname( __DIR__, 4 ) . '/plugins/nadlan-config/inc/projects-hub.php';
$d = nadlan_phl_dict( $lang );
$body = nadlan_phl_render( $lang );
$font = 'ru' === $lang ? 'IBM+Plex+Sans:wght@400;500;600;700&subset=cyrillic' : 'IBM+Plex+Sans:wght@400;500;600;700';
$shell = '<!doctype html><html lang="' . $lang . '" dir="ltr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>' . esc_html( $d['page_title'] ?? '' ) . '</title>'
	. '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=' . $font . '&family=IBM+Plex+Mono:wght@400;500&display=swap">'
	. '<style>body{margin:0;background:#F7F8FA;font-family:"IBM Plex Sans",system-ui,sans-serif}.pv{background:#14213D;color:#fff;padding:12px 16px;font:500 13px "IBM Plex Mono",monospace}h1.pg{font:700 34px/1.2 "IBM Plex Sans",sans-serif;color:#14213D;max-width:1240px;margin:24px auto 0;padding:0 16px}.nlph{font-family:"IBM Plex Sans",system-ui,sans-serif!important}.nlph h2,.nlph h3{font-family:"IBM Plex Sans",sans-serif!important}</style></head><body>'
	. '<div class="pv">Preview · /' . $lang . '/projects/ · 1.72.514 · local data</div><h1 class="pg">' . esc_html( $d['page_title'] ?? '' ) . '</h1>' . $body . '</body></html>';
file_put_contents( __DIR__ . '/preview-' . $lang . '.html', $shell );
echo 'preview-' . $lang . ' ' . strlen( $shell ) . " bytes\n";
