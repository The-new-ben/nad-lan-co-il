<?php
// HAD-740: the project edit box never saves an empty number field as 0, and a stored 0 never blocks the next save.
// php -d extension=mbstring tools/seo/test_h740_save.php
define( 'ABSPATH', __DIR__ ); define( 'OBJECT', 'OBJECT' );
$GLOBALS['t_hooks'] = array(); $GLOBALS['t_meta'] = array();
function add_action( $h, $cb, $p = 10, $a = 1 ) { $GLOBALS['t_hooks'][ $h ][] = $cb; } function add_filter( $h, $cb = null, $p = 10, $a = 1 ) {}
function add_shortcode() {} function is_admin() { return true; } function apply_filters( $h, $v ) { return $v; } function do_action() {}
function get_option( $k, $d = false ) { return $d; } function update_option() {} function register_post_meta() {} function add_meta_box() {}
function wp_verify_nonce() { return true; } function current_user_can() { return true; } function wp_unslash( $v ) { return $v; }
function esc_url_raw( $v ) { return (string) $v; } function sanitize_text_field( $v ) { return trim( (string) $v ); } function sanitize_key( $v ) { return strtolower( (string) $v ); }
function esc_attr( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); } function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_textarea( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); } function esc_url( $s ) { return (string) $s; } function wp_json_encode( $d, $f = 0 ) { return json_encode( $d, $f ); }
function wp_nonce_field() {} function checked( $a, $b = true, $e = true ) { return $a == $b ? ' checked' : ''; } function selected( $a, $b = true, $e = true ) { return $a == $b ? ' selected' : ''; }
function get_post_type( $id ) { return 'nadlan_project'; } function get_post_field( $f, $id ) { return ''; } function get_the_title( $id ) { return 'T'; } function get_permalink( $id ) { return 'https://x/'; }
function wp_enqueue_media() {} function wp_enqueue_script() {} function wp_enqueue_style() {} function admin_url( $p = '' ) { return 'https://x/wp-admin/' . $p; } function plugins_url( $p = '', $f = '' ) { return 'https://x/' . $p; }
function get_post_meta( $id, $k = '', $s = false ) { return $GLOBALS['t_meta'][ $id ][ $k ] ?? ''; }
function update_post_meta( $id, $k, $v ) { $GLOBALS['t_meta'][ $id ][ $k ] = $v; return true; }
function delete_post_meta( $id, $k ) { unset( $GLOBALS['t_meta'][ $id ][ $k ] ); return true; }
function sanitize_textarea_field( $v ) { return (string) $v; } function absint( $n ) { return abs( (int) $n ); } function __( $s ) { return $s; } function esc_html__( $s ) { return $s; } function esc_attr__( $s ) { return $s; }
require dirname( __DIR__, 2 ) . '/plugins/nadlan-config/inc/showroom-support.php';

$bad = 0;
function ok( $cond, $what ) { global $bad; if ( ! $cond ) { $bad++; echo "FAIL $what\n"; } }
function save( $id, $post ) { $_POST = $post + array( 'nadlan_p3d_nonce' => 'x' ); foreach ( $GLOBALS['t_hooks']['save_post_nadlan_project'] ?? array() as $cb ) { try { $cb( $id ); } catch ( \Throwable $e ) { echo 'save threw: ' . $e->getMessage() . "\n"; } } }
function box( $id ) { ob_start(); try { nadlan_p3d_render_admin_metabox( (object) array( 'ID' => $id ) ); } catch ( \Throwable $e ) { echo 'render threw: ' . $e->getMessage(); } return ob_get_clean(); }
function fh_input( $h ) { preg_match( '~<input[^>]*name="project_3d_floor_height_m"[^>]*>~u', $h, $m ); return $m[0] ?? ''; }
ok( ! empty( $GLOBALS['t_hooks']['save_post_nadlan_project'] ), 'the save handler is registered' );

// a page whose showroom fields were never saved: the first save with empty fields stores nothing as 0
save( 2551, array( 'project_3d_floor_height_m' => '', 'project_3d_ground_elevation_m' => '', 'project_3d_avg_price_per_sqm' => '' ) );
ok( ! isset( $GLOBALS['t_meta'][2551]['project_3d_floor_height_m'] ), 'empty floor height is not stored (was 0)' );
ok( ! isset( $GLOBALS['t_meta'][2551]['project_3d_ground_elevation_m'] ) && ! isset( $GLOBALS['t_meta'][2551]['project_3d_avg_price_per_sqm'] ), 'empty elevation and price are not stored' );
$in = fh_input( box( 2551 ) );
ok( '' !== $in && false !== strpos( $in, 'value=""' ), 'after the first save the field prints empty: ' . $in );
// the second save of the same form goes through and still stores nothing
save( 2551, array( 'project_3d_floor_height_m' => '', 'project_3d_ground_elevation_m' => '', 'project_3d_avg_price_per_sqm' => '' ) );
ok( ! isset( $GLOBALS['t_meta'][2551]['project_3d_floor_height_m'] ), 'second save: still nothing stored' );
// a page that already carries the bad 0: it prints empty, so the browser no longer blocks the save
$GLOBALS['t_meta'][2552] = array( 'project_3d_floor_height_m' => '0', 'project_3d_ground_elevation_m' => '0', 'project_3d_avg_price_per_sqm' => '0' );
$in = fh_input( box( 2552 ) );
ok( false !== strpos( $in, 'value=""' ) && false !== strpos( $in, 'min="2.4"' ), 'a stored 0 prints empty under min 2.4: ' . $in );
// real values are kept and printed
save( 2553, array( 'project_3d_floor_height_m' => '3.2', 'project_3d_ground_elevation_m' => '0', 'project_3d_avg_price_per_sqm' => '52000' ) );
ok( 3.2 === $GLOBALS['t_meta'][2553]['project_3d_floor_height_m'] && 0.0 === $GLOBALS['t_meta'][2553]['project_3d_ground_elevation_m'] && 52000.0 === $GLOBALS['t_meta'][2553]['project_3d_avg_price_per_sqm'], 'typed numbers stored as before (an elevation of 0 is a real value)' );
$h = box( 2553 );
ok( false !== strpos( fh_input( $h ), 'value="3.2"' ) && false !== strpos( fh_input( $h ), 'max="5"' ), 'a real floor height prints with its limits' );
ok( 1 === preg_match( '~name="project_3d_ground_elevation_m" value="0"~u', $h ), 'elevation 0 prints as 0' );
// a stored value above the maximum keeps printing but does not block
$GLOBALS['t_meta'][2554] = array( 'project_3d_floor_height_m' => '5.4' );
$in = fh_input( box( 2554 ) ); ok( false !== strpos( $in, 'value="5.4"' ) && false === strpos( $in, 'max=' ), 'above the maximum: printed without the blocking max: ' . $in );
ok( '' === nadlan_p3d_sanitize_decimal_or_empty( '' ) && 3.05 === nadlan_p3d_sanitize_decimal_or_empty( '3.05' ), 'REST sanitizer keeps empty as empty' );
echo ( $bad ? "FAILED $bad" : 'all passed' ), "\n";
exit( $bad ? 1 : 0 );
