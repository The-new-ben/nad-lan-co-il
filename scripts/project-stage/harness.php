<?php
/* Runs inc/project-stage.php's composition on a saved copy of the live Rainbow page, with WordPress stubbed.
   php harness.php <in.html> <out.html> */
define( 'ABSPATH', __DIR__ . '/' );
define( 'NADLAN_CONFIG_VERSION', '1.72.255' );
function add_action() {} function add_filter() {}
function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_attr( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_url( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function wp_json_encode( $d ) { return json_encode( $d, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ); }
function plugins_url( $p, $f ) { return 'https://nad-lan.co.il/wp-content/plugins/nadlan-config/' . $p; }
function home_url( $p = '' ) { return 'https://nad-lan.co.il' . $p; }
function get_option( $k, $d = '' ) { return 'nadlan_mapbox_token' === $k ? 'pk.TEST' : $d; }
function get_post_meta( $id, $k, $single = true ) {
	$m = array( 4464 => array( 'lat' => '32.103168', 'lng' => '34.784441' ),
		7833 => array( 'profession' => 'metavech', 'license_number' => '3131540', 'areas_served' => 'נופי ים,כוכב הצפון,צוקי אביב,רמת אביב', 'phone' => '0501234567', 'nl_site_he' => '' ) );
	return $m[ $id ][ $k ] ?? '';
}
function get_post_type( $id ) { return 7833 === (int) $id ? 'nadlan_professional' : 'nadlan_project'; }
function get_post_status( $id ) { return 'publish'; }
function get_permalink( $id ) { return 'https://nad-lan.co.il/professionals/meital-katzir/'; }
function has_post_thumbnail( $id ) { return true; }
function get_the_post_thumbnail( $id, $size, $attr ) { return '<img src="https://nad-lan.co.il/wp-content/uploads/meital.jpg" alt="' . esc_attr( $attr['alt'] ) . '">'; }
function wp_strip_all_tags( $s ) { return trim( strip_tags( $s ) ); }
function nlds_icon( $n ) { return '<svg class="nlds-ico"></svg>'; }
function nadlan_prof_person_name( $id ) { return 'מיטל קציר'; }
function nadlan_dir_prof_label( $k, $id ) { return 'מתווכת'; }
function nadlan_prof_wa_digits( $p ) { return '972' . substr( preg_replace( '/\D/', '', $p ), 1 ); }
function nadlan_cta_whatsapp_number() { return '972500000000'; }
require 'C:/Users/777/nad-lan/nad-lan-co-il/plugins/nadlan-config/inc/project-stage.php';
$ps  = array_merge( nadlan_ps_config()['rainbow-tel-aviv'], array( 'id' => 4464, 'slug' => 'rainbow-tel-aviv' ) );
$in  = file_get_contents( $argv[1] );
$out = nadlan_ps_compose( $in, $ps );
file_put_contents( $argv[2], $out );
$body = substr( $out, strpos( $out, '<body' ) );
$pos  = function ( $needle ) use ( $body ) { $p = strpos( $body, $needle ); return false === $p ? -1 : $p; };
$rep  = array(
	'changed'          => $out !== $in,
	'h1_count'         => substr_count( $body, '<h1' ),
	'h1_visible'       => $pos( '<h1 id="nl-project-page-title" class="nlps-h1">' ),
	'lead'             => $pos( '<div class="nl-lead">' ),
	'stage'            => $pos( 'id="nlps"' ),
	'rail_square'      => $pos( 'class="nlbsq"' ),
	'slot'             => $pos( 'class="nlbslot"' ),
	'view'             => $pos( 'id="nlps-view"' ),
	'map'              => $pos( 'id="nlpjx-map"' ),
	'map_count'        => substr_count( $body, 'id="nlpjx-map"' ),
	'prices_block'     => $pos( 'class="nlcp-projctx"' ),
	'notice'           => $pos( 'class="nl-projnotice"' ),
	'article'          => $pos( 'nadlan-project-article' ),
	'old_note_gone'    => false === strpos( $body, 'על המפה החיה למטה' ),
	'words_in'         => str_word_count( strip_tags( substr( $in, strpos( $in, '<body' ) ) ) ),
	'words_out'        => str_word_count( strip_tags( $body ) ),
	'len_in'           => strlen( $in ),
	'len_out'          => strlen( $out ),
);
echo json_encode( $rep, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE ), "\n";
// fail-open checks
echo 'no lead -> unchanged: ', var_export( nadlan_ps_compose( str_replace( '<div class="nl-lead">', '<div class="nl-leadx">', $in ), $ps ) === str_replace( '<div class="nl-lead">', '<div class="nl-leadx">', $in ), true ), "\n";
echo 'twice -> once: ', var_export( nadlan_ps_compose( $out, $ps ) === $out, true ), "\n";
