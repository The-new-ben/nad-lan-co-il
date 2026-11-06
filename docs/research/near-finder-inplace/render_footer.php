<?php
/**
 * Local harness (near-finder in place, 6.11.2026): runs the REAL nadlan_nf_launcher() from the edited
 * plugins/nadlan-config/inc/near-finder.php with tiny WordPress stubs, and prints the footer markup for each context as JSON.
 * The public values (the Mapbox public token, the product link) are read from the saved live HTML, never from a secret.
 * Usage: php render_footer.php <path-to-near-finder.php> <live-home.html>
 */
define( 'ABSPATH', __DIR__ . '/' );
$GLOBALS['nf_live'] = file_get_contents( $argv[2] );
function add_action() {}
function add_filter() {}
function add_shortcode() {}
function apply_filters( $tag, $v ) { return $v; }
function esc_attr( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_url( $s ) { return str_replace( '&', '&#038;', (string) $s ); }
function rest_url( $p ) { return 'https://nad-lan.co.il/wp-json/' . ltrim( $p, '/' ); }
function home_url( $p = '' ) { return 'https://nad-lan.co.il' . $p; }
function add_query_arg( $k, $v, $u ) { return $u . ( false === strpos( $u, '?' ) ? '?' : '&' ) . $k . '=' . $v; }
function get_post_type( $id ) { return 490 === (int) $id ? 'product' : ''; }
function get_post_status( $id ) { return 'publish'; }
function get_permalink( $id ) { preg_match( '/class="nlnf__own-b">.*?<a href="([^"]+)"/s', $GLOBALS['nf_live'], $m ); return $m ? $m[1] : ''; }
function get_option( $k, $d = '' ) { return $d; }
function nadlan_cp_mapbox_token() { preg_match( '/data-mb="([^"]+)"/', $GLOBALS['nf_live'], $m ); return $m ? $m[1] : ''; }
require $argv[1];

$portal = 'דירות למכירה ולהשכרה על המפה';
$ctx = array( // as the new nadlan_nf_context() returns them
	'home'       => array( 'mode' => 'portal', 'deal' => 'sale', 'title' => $portal, 'inline' => false, 'broker' => 0, 'host' => '#nldrone' ),
	'properties' => array( 'mode' => 'portal', 'deal' => '', 'title' => $portal, 'inline' => true, 'broker' => 0, 'host' => '' ),
	'rent'       => array( 'mode' => 'portal', 'deal' => 'rent', 'title' => 'דירות להשכרה על המפה', 'inline' => false, 'broker' => 0, 'host' => '#listings' ),
	'broker'     => array( 'mode' => 'broker', 'deal' => 'sale', 'title' => 'הנכסים של מיטל קציר על המפה', 'inline' => false, 'broker' => 7833, 'host' => '#listings' ),
	'card'       => array(), // her professional card: no context any more (no map or listings section there)
);
$out = array();
foreach ( $ctx as $k => $c ) { $out[ $k ] = $c ? nadlan_nf_launcher( $c ) : ''; }
echo json_encode( $out, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT );
