<?php
// php render_section.php <page_id>  - prints the section markup exactly as the module's wp_footer prints it (for the design card)
require __DIR__ . '/wp_stubs.php';
$GLOBALS['HOOKS'] = array();
function add_action_capture( $h, $f ) { $GLOBALS['HOOKS'][ $h ][] = $f; }
function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_attr( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_url( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function is_admin() { return false; } function is_singular() { return true; }
function get_queried_object_id() { return (int) $GLOBALS['QID']; }
$PLUG = dirname( __DIR__, 4 ) . '/plugins/nadlan-config';
$pages = json_decode( file_get_contents( __DIR__ . '/pages.json' ), true );
foreach ( $pages as $id => $p ) { $GLOBALS['POSTS'][ (int) $id ] = (object) array( 'ID' => (int) $id, 'post_type' => $p['type'], 'post_title' => $p['title'], 'url' => $p['url'], 'post_content' => '', 'post_excerpt' => '', 'meta' => array() ); }
$GLOBALS['QID'] = (int) $argv[1]; $_GET['advisor'] = 'on';
$src = file_get_contents( $PLUG . '/inc/expert-advisor.php' );
$src = str_replace( "add_action( 'wp_footer'", "add_action_capture( 'wp_footer'", $src );
$tmp = __DIR__ . '/_mod.php'; file_put_contents( $tmp, $src ); require $tmp; unlink( $tmp );
foreach ( $GLOBALS['HOOKS']['wp_footer'] as $f ) { $f(); }
