<?php
// HAD-740: the default card picture (inc/project-default-image.php + nadlan_dir_project_card), rendered without WordPress.
// php -d extension=mbstring tools/seo/test_h740_default.php
define( 'ABSPATH', __DIR__ ); define( 'OBJECT', 'OBJECT' );
define( 'DAY_IN_SECONDS', 86400 ); define( 'MINUTE_IN_SECONDS', 60 ); define( 'HOUR_IN_SECONDS', 3600 );
function add_action() {} function add_filter() {} function add_shortcode() {} function is_admin() { return false; } function register_activation_hook() {}
function apply_filters( $h, $v ) { return $v; } function do_action() {} function update_option() {}
$GLOBALS['t_opt'] = array();
function get_option( $k, $d = false ) { return array_key_exists( $k, $GLOBALS['t_opt'] ) ? $GLOBALS['t_opt'][ $k ] : $d; }
function number_format_i18n( $n, $d = 0 ) { return number_format( $n, $d ); } function selected() {} function wp_json_encode( $d ) { return json_encode( $d, JSON_UNESCAPED_UNICODE ); }
function get_transient() { return false; } function set_transient() {} function delete_transient() {} function rest_url( $p = '' ) { return 'https://nad-lan.co.il/wp-json/' . $p; }
function home_url( $p = '/' ) { return 'https://nad-lan.co.il' . $p; }
function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_attr( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_url( $s ) { return (string) $s; }
function date_i18n( $f, $t ) { return date( $f, $t ); } function wp_parse_url( $u, $c = -1 ) { return parse_url( $u, $c ); }
function plugins_url( $p = '', $f = '' ) { return 'https://nad-lan.co.il/wp-content/plugins/nadlan-config/' . $p; }
function plugin_dir_path( $f ) { return dirname( $f ) . '/'; } function plugin_dir_url( $f ) { return 'https://nad-lan.co.il/wp-content/plugins/nadlan-config/'; }
function sanitize_title( $s ) { return strtolower( trim( (string) $s ) ); } function absint( $n ) { return abs( (int) $n ); }
function get_query_var( $k ) { return 0; } function is_post_type_archive( $t = '' ) { return true; }
function wp_strip_all_tags( $s ) { return strip_tags( (string) $s ); } function add_query_arg( $k, $v, $u ) { return $u . '?' . $k . '=' . $v; }
function get_theme_file_path( $p ) { return ''; }
// posts: 1 own featured, 2 photos_csv, 3 nothing, 4 nothing (-en twin of 5 with featured), 5 Hebrew with featured, 6 -en of 7 (no featured)
$GLOBALS['t_meta'] = array(
	1 => array( 'post_name' => 'has-thumb', 'title' => 'A', 'city' => 'חולון', 'thumb' => 501 ),
	2 => array( 'post_name' => 'has-csv', 'title' => 'B', 'city' => 'חולון', 'photos_csv' => 'https://example.com/b.jpg' ),
	3 => array( 'post_name' => 'bare', 'title' => 'C', 'city' => 'חולון' ),
	4 => array( 'post_name' => 'twin-en', 'title' => 'D', 'city' => 'Holon' ),
	5 => array( 'post_name' => 'twin', 'title' => 'D he', 'city' => 'חולון', 'thumb' => 505 ),
	6 => array( 'post_name' => 'lonely-en', 'title' => 'E', 'city' => 'Holon' ),
	7 => array( 'post_name' => 'lonely', 'title' => 'E he', 'city' => 'חולון' ),
);
foreach ( array( 3, 4, 5 ) as $_i ) { $GLOBALS['t_meta'][ $_i ]['project_type'] = 'pinui_binui'; }
$GLOBALS['t_att'] = array( 501 => array( 1024, 768 ), 505 => array( 1024, 640 ), 8913 => array( 1024, 640 ) );
function get_post_meta( $id, $k = '', $s = false ) { $m = $GLOBALS['t_meta'][ $id ] ?? array(); return isset( $m[ $k ] ) ? $m[ $k ] : ''; }
function get_post_field( $f, $id ) { return $GLOBALS['t_meta'][ $id ][ $f ] ?? ''; }
function has_post_thumbnail( $id ) { return ! empty( $GLOBALS['t_meta'][ $id ]['thumb'] ); }
function get_post_thumbnail_id( $id ) { return (int) ( $GLOBALS['t_meta'][ $id ]['thumb'] ?? 0 ); }
function get_the_post_thumbnail_url( $id, $s = '' ) { return 'https://nad-lan.co.il/wp-content/uploads/a' . get_post_thumbnail_id( $id ) . '.webp'; }
function wp_get_attachment_image_src( $aid, $s = '' ) { if ( ! isset( $GLOBALS['t_att'][ $aid ] ) ) { return false; } $t = $GLOBALS['t_att'][ $aid ]; return array( 'https://nad-lan.co.il/wp-content/uploads/a' . $aid . '-' . $t[0] . 'x' . $t[1] . '.webp', $t[0], $t[1], true ); }
function wp_get_attachment_image_srcset( $aid, $s = '' ) { return isset( $GLOBALS['t_att'][ $aid ] ) ? 'https://nad-lan.co.il/wp-content/uploads/a' . $aid . '-768x480.webp 768w, https://nad-lan.co.il/wp-content/uploads/a' . $aid . '-1024x640.webp 1024w' : ''; }
function get_post_type( $id ) { return isset( $GLOBALS['t_att'][ $id ] ) ? 'attachment' : ( isset( $GLOBALS['t_meta'][ $id ] ) ? 'nadlan_project' : false ); }
function wp_attachment_is_image( $id ) { return isset( $GLOBALS['t_att'][ $id ] ); }
function get_page_by_path( $path, $o = 'OBJECT', $pt = 'page' ) { foreach ( $GLOBALS['t_meta'] as $id => $m ) { if ( $m['post_name'] === $path ) { return (object) array( 'ID' => $id ); } } return null; }
function get_permalink( $id ) { return 'https://nad-lan.co.il/projects/' . $GLOBALS['t_meta'][ $id ]['post_name'] . '/'; }
function get_the_title( $id ) { return $GLOBALS['t_meta'][ $id ]['title']; }
require dirname( __DIR__, 2 ) . '/plugins/nadlan-config/inc/projects-hub.php';
require dirname( __DIR__, 2 ) . '/plugins/nadlan-config/inc/directory.php';

$bad = 0;
function ok( $cond, $what ) { global $bad; if ( ! $cond ) { $bad++; echo "FAIL $what\n"; } }
function media_of( $card ) { preg_match( '~<div class="nldc-media([^"]*)">\s*<img ([^>]*)>~u', $card, $m ); return array( trim( $m[1] ?? '' ), $m[2] ?? '' ); }
$DEF = 'a8913-1024x640.webp';

// 1. gate closed: nothing changes (the bare card keeps the old fallback)
$GLOBALS['t_opt'] = array( 'nadlan_pd_attachment' => 8913 ); unset( $_GET['pics'] );
$closed = array(); foreach ( array( 1, 2, 3, 4, 6 ) as $i ) { $closed[ $i ] = nadlan_dir_project_card( $i ); }
list( $c3, $i3 ) = media_of( $closed[3] );
ok( false !== strpos( $c3, 'has-concept-art' ) && false === strpos( $i3, $DEF ) && false !== strpos( $i3, 'alt=""' ), 'gate closed: the old fallback, alt empty for the enrichment' );
ok( false === strpos( implode( '', $closed ), 'has-default-pic' ), 'gate closed: no default anywhere' );

// 2. gate open by ?pics=next
$_GET['pics'] = 'next';
list( $c1, $i1 ) = media_of( nadlan_dir_project_card( 1 ) );
ok( false !== strpos( $c1, 'has-real-photo' ) && false !== strpos( $i1, 'uploads/a501.webp' ), 'own featured picture wins' );
ok( nadlan_dir_project_card( 1 ) === $closed[1], 'a card with its own picture is byte-identical with the gate open' );
list( $c2, $i2 ) = media_of( nadlan_dir_project_card( 2 ) );
ok( false !== strpos( $c2, 'has-real-photo' ) && false !== strpos( $i2, 'example.com/b.jpg' ), 'photos_csv wins' );
list( $c3, $i3 ) = media_of( nadlan_dir_project_card( 3 ) );
$card3 = nadlan_dir_project_card( 3 );
ok( false !== strpos( $card3, 'nldc-media has-plate' ) && false !== strpos( $card3, '<span class="nlsp" aria-hidden="true">' ) && false === strpos( $card3, 'has-concept-art' ), 'HAD-743: no picture on a Hebrew card -> the street sign, no concept-art class' );
ok( false !== strpos( $card3, $DEF ) && 0 === substr_count( $card3 . nadlan_dir_project_card( 3 ), 'id="nlsp-css"' ) /* already printed by the first sign on this page */, 'HAD-743 v3: the brand picture stays under the small sign; its CSS prints once per page' );
ok( false === strpos( nadlan_dir_project_card( 3 ), 'nldcp-type' ), 'nothing printed over the default picture (no type label)' );
ok( false !== strpos( nadlan_dir_project_card( 4 ), 'nldcp-type' ), 'a twin picture keeps its type label' );
unset( $_GET['pics'] ); ok( false !== strpos( nadlan_dir_project_card( 3 ), 'nldcp-type' ), 'gate closed: the type label stays as today' ); $_GET['pics'] = 'next';
ok( 'ערבי נחל' === nadlan_sp_street( 'ערבי נחל, גבעתיים: פינוי בינוי', '', 'גבעתיים' ) && 'שכונה' === nadlan_sp_street( 'GINDI VOGUE', 'שכונה', 'תל אביב' ) && 'חיפה' === nadlan_sp_street( 'X', '', 'חיפה' ) && 'איינשטיין 2.4.6.8' === nadlan_sp_street( 'איינשטיין 2.4.6.8: חן ואיתי גינדי וקבוצת שבירו', '', 'תל אביב' ), 'HAD-743: street from the title, else neighbourhood, else city' );
list( $c4, $i4 ) = media_of( nadlan_dir_project_card( 4 ) );
ok( false !== strpos( $c4, 'has-real-photo' ) && false !== strpos( $i4, 'a505-1024x640.webp' ) && false !== strpos( $i4, 'alt=""' ), 'language page: its Hebrew page picture (alt left to the enrichment)' );
list( $c6, $i6 ) = media_of( nadlan_dir_project_card( 6 ) );
ok( false !== strpos( $c6, 'has-default-pic' ) && false !== strpos( $i6, 'alt="NadLan: choose your apartment on the building.' ), 'language page without a Hebrew picture: the default with the English alt' );
foreach ( array( 'fr' => "NadLan : choisissez", 'ru' => 'NadLan: выберите', 'ar' => 'NadLan: اختاروا', 'he' => 'נדל״ן: בחרו' ) as $l => $a ) { ok( 0 === strpos( nadlan_pd_alt( $l ), $a ), 'alt ' . $l ); }

// 3. option empty or the media gone: exactly the old behaviour
$GLOBALS['t_opt'] = array(); list( $c3e, $i3e ) = media_of( nadlan_dir_project_card( 3 ) );
ok( nadlan_dir_project_card( 3 ) === $closed[3], 'option empty: byte-identical with the closed gate' );
$GLOBALS['t_opt'] = array( 'nadlan_pd_attachment' => 9999 );
ok( null === nadlan_pd_default( 'he' ) && nadlan_dir_project_card( 3 ) === $closed[3], 'media deleted: null and the old card' );
// 4. the public switch
unset( $_GET['pics'] ); $GLOBALS['t_opt'] = array( 'nadlan_pd_attachment' => 8913, 'nadlan_pd_public' => '1' );
ok( false !== strpos( nadlan_dir_project_card( 3 ), 'has-plate' ), 'nadlan_pd_public=1 opens it without ?pics=next (the sign on a Hebrew card)' );
// 4b. a photos_csv picture that is a plugin file (batch-01 sketch, 1440x1080) fills from the top; another address stays as it was
$GLOBALS['t_meta'][8] = array( 'post_name' => 'sketch-csv', 'title' => 'F', 'city' => 'חיפה', 'photos_csv' => 'https://nad-lan.co.il/wp-content/plugins/nadlan-config/assets/projects/batch-01/01-hagana-salvador-haifa-sketch.webp,https://nad-lan.co.il/wp-content/plugins/nadlan-config/assets/projects/batch-01/01-hagana-salvador-haifa-photo.webp' );
list( $c8, $i8 ) = media_of( nadlan_dir_project_card( 8 ) );
ok( false !== strpos( $c8, 'has-real-photo is-fill' ) && false !== strpos( $i8, 'width="1440" height="1080"' ) && false !== strpos( $i8, '01-hagana-salvador-haifa-sketch.webp' ), 'plugin sketch from photos_csv: real size, fills: ' . $c8 . ' ' . $i8 );
list( $c2b, $i2b ) = media_of( nadlan_dir_project_card( 2 ) );
ok( false === strpos( $c2b, 'is-fill' ) && false === strpos( $i2b, 'width=' ), 'photos_csv from another address: unchanged' );
$GLOBALS['t_meta'][9] = array( 'post_name' => 'bad-csv', 'title' => 'G', 'city' => 'חיפה', 'photos_csv' => 'https://nad-lan.co.il/wp-content/plugins/nadlan-config/../wp-config.php' );
ok( false === strpos( nadlan_dir_project_card( 9 ), 'width=' ), 'no path tricks' );
// 5. the enrichment hooks still match on every card kind
foreach ( array( 1, 2, 3, 4, 6 ) as $i ) { ok( 1 === preg_match( '~^<a class="nldc nldc-project[^"]*" href="([^"]+)"~u', ltrim( nadlan_dir_project_card( $i ) ) ), 'enrichment marker ' . $i ); }
$all = implode( '', array_map( 'nadlan_dir_project_card', array( 1, 2, 3, 4, 6 ) ) ) . file_get_contents( dirname( __DIR__, 2 ) . '/plugins/nadlan-config/inc/project-default-image.php' );
ok( ! preg_match( '/[\x00-\x08\x0b\x0c\x0e-\x1f]/', $all ), 'no control characters' );
echo ( $bad ? "FAILED $bad" : 'all passed' ), "\n";
exit( $bad ? 1 : 0 );
