<?php
// HAD-694: the phone filter row and the new project card of inc/directory.php, rendered without WordPress.
// php -d extension=mbstring tools/seo/test_h694_card.php
define( 'ABSPATH', __DIR__ );
define( 'DAY_IN_SECONDS', 86400 ); define( 'MINUTE_IN_SECONDS', 60 ); define( 'HOUR_IN_SECONDS', 3600 );
function add_action() {} function add_filter() {} function add_shortcode() {} function is_admin() { return false; } function register_activation_hook() {}
function apply_filters( $h, $v ) { return $v; } function do_action() {} function get_option( $k, $d = false ) { return $d; } function update_option() {}
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
$GLOBALS['t_meta'] = array(
	1 => array( 'post_name' => 'rainbow-tel-aviv', 'title' => 'Rainbow Tel Aviv', 'city' => 'תל אביב יפו', 'num_units' => 459, 'project_status' => 'construction', 'developer_name' => 'ישראל קנדה', 'floors' => 0, 'thumb' => array( 1024, 768 ) ),
	2 => array( 'post_name' => 'some-renewal', 'title' => 'מתחם לדוגמה', 'city' => 'חולון', 'num_units' => 120, 'project_status' => 'planning', 'developer_name' => '', 'floors' => 12, 'thumb' => array( 1024, 1024 ) ),
	3 => array( 'post_name' => 'recanati-residence', 'title' => 'Recanati Residence', 'city' => 'תל אביב יפו', 'num_units' => 198, 'project_status' => 'completed', 'developer_name' => 'אשטרום', 'floors' => 16, 'thumb' => null, 'address' => 'אבן גבירול 1' ),
);
function get_post_meta( $id, $k = '', $s = false ) { $m = $GLOBALS['t_meta'][ $id ]; return isset( $m[ $k ] ) && ! is_array( $m[ $k ] ) ? $m[ $k ] : ''; }
function get_post_field( $f, $id ) { return $GLOBALS['t_meta'][ $id ][ $f ] ?? ''; }
function has_post_thumbnail( $id ) { return ! empty( $GLOBALS['t_meta'][ $id ]['thumb'] ); }
function get_the_post_thumbnail_url( $id, $s = '' ) { return 'https://nad-lan.co.il/wp-content/uploads/p' . $id . '.webp'; }
function get_post_thumbnail_id( $id ) { return 100 + $id; }
function wp_get_attachment_image_src( $aid, $s = '' ) { $t = $GLOBALS['t_meta'][ $aid - 100 ]['thumb']; return array( 'x', $t[0], $t[1], false ); }
function get_permalink( $id ) { return 'https://nad-lan.co.il/projects/' . $GLOBALS['t_meta'][ $id ]['post_name'] . '/'; }
function get_the_title( $id ) { return $GLOBALS['t_meta'][ $id ]['title']; }
function get_theme_file_path( $p ) { return ''; }
function wp_strip_all_tags( $s ) { return strip_tags( (string) $s ); } function add_query_arg( $k, $v, $u ) { return $u . "?" . $k . "=" . $v; }
require dirname( __DIR__, 2 ) . '/plugins/nadlan-config/inc/projects-hub.php';
require dirname( __DIR__, 2 ) . '/plugins/nadlan-config/inc/directory.php';

$bad = 0;
function ok( $cond, $what ) { global $bad; if ( ! $cond ) { $bad++; echo "FAIL $what\n"; } }

$r = nadlan_dir_market_row( 'rainbow-tel-aviv' );
ok( is_array( $r ) && 'construction' === $r['status'], 'market row by exact link' );
ok( null === nadlan_dir_market_row( 'some-renewal' ), 'no row without an exact link' );
$hi = nadlan_dir_market_row( 'h-infinity-somail-tel-aviv' );
ok( is_array( $hi ) && ! empty( $hi['deal'] ), 'h-infinity has its published deal' );

$facets = array( 'cities' => array( array( 'name' => 'ירושלים', 'n' => 213 ), array( 'name' => 'תל אביב יפו', 'n' => 87 ) ), 'types' => array( 'pinui_binui' => 975, 'new_build' => 28 ) );
$q = nadlan_dir_quickfilter_html( $facets );
ok( false !== strpos( $q, '<div class="nlqf" role="group" aria-label="סינון הפרויקטים">' ), 'filter row' );
ok( false !== strpos( $q, 'data-k="city" data-v="תל אביב יפו">תל אביב יפו · 87</button>' ), 'Tel Aviv chip with the catalog count' );
ok( false !== strpos( $q, 'data-v="new_build">בנייה חדשה · 28</button>' ), 'new-build chip' );
ok( false !== strpos( $q, 'data-a="all" class="nlqf-all" aria-expanded="false">כל הסינונים</button>' ), 'all filters chip' );
ok( false !== strpos( $q, '.nldir-results .nldc-project .nldc-media{aspect-ratio:8/5!important}' ), 'picture box 8:5' );
ok( false !== strpos( $q, 'object-position:50% 0' ), 'fill from the top' );

$c1 = nadlan_dir_project_card( 1 );
ok( false !== strpos( $c1, ' is-own"' ) && false !== strpos( $c1, '>לסיור בפרויקט</span>' ), 'own project: tour CTA' );
ok( false !== strpos( $c1, 'nldc-media has-real-photo is-fill' ) && false !== strpos( $c1, 'width="1024" height="768"' ), '4:3 plate fills from the top, with its size' );
ok( false !== strpos( $c1, '<b class="nldcp-tag is-build">בבנייה</b>' ), 'stage tag from the market row' );
ok( false === strpos( $c1, '<dt>סטטוס</dt>' ), 'no status twice when a tag says it' );
ok( 1 === preg_match( '~<a class="nldc nldc-project[^"]*" href="([^"]+)"~u', $c1 ), 'the enrichment marker still matches' );
ok( false !== strpos( $c1, 'alt="" loading="lazy"' ), 'the enrichment alt hook still matches' );
$c2 = nadlan_dir_project_card( 2 );
ok( false === strpos( $c2, 'is-fill' ) && false === strpos( $c2, 'is-own' ) && false !== strpos( $c2, '>לפרטי הפרויקט</span>' ), 'square plate stays whole; details CTA' );
ok( false === strpos( $c2, 'nldcp-tags' ) && false !== strpos( $c2, '<div class="is-word"><dt>סטטוס</dt><dd>בתכנון</dd></div>' ), 'no tag without a market row; status as a word chip' );
$c3 = nadlan_dir_project_card( 3 );
ok( false !== strpos( $c3, '<b class="nldcp-tag is-ready">לאכלוס מיידי</b>' ) && false !== strpos( $c3, '<dt>חדרים</dt><dd>3 עד 5 חדרים</dd>' ), 'ready tag + rooms chip' );
$li = nadlan_dir_itemlist_item( 1, 1 );
ok( 'ListItem' === $li['@type'] && 1 === $li['position'] && 'ApartmentComplex' === $li['item']['@type'], 'typed item' );
ok( 459 === $li['item']['numberOfAccommodationUnits'] && 'תל אביב יפו' === $li['item']['address']['addressLocality'], 'units + city' );
ok( ! isset( $li['item']['offers'] ), 'no price when none is published' );
$pv = array_column( $li['item']['additionalProperty'], 'value', 'name' );
ok( 'ישראל קנדה' === $pv['יזם'] && 'בבנייה' === $pv['שלב'], 'developer + stage ' . json_encode( $pv, JSON_UNESCAPED_UNICODE ) );
$li3 = nadlan_dir_itemlist_item( 3, 3 );
ok( 'אבן גבירול 1' === $li3['item']['address']['streetAddress'], 'street address' );
$mh = nadlan_ph_market_html();
ok( 564 === substr_count( $mh, '<tr data-reg=' ), 'all 564 market rows in the HTML: ' . substr_count( $mh, '<tr data-reg=' ) );
ok( 548 === substr_count( $mh, ' class="nlph-more">' ), 'rows after the first 16 collapsed: ' . substr_count( $mh, ' class="nlph-more">' ) );
ok( false !== strpos( $mh, 'data-full="1"' ), 'the table says it is full' );
$bh = nadlan_ph_budget_html(); $sh = nadlan_ph_stages_html(); $dh = nadlan_ph_devs_html(); $rh = nadlan_ph_ready_html();
ok( 6 === substr_count( $bh, 'role="tabpanel"' ) && 1 === substr_count( $bh, '<h2 id="nlph-budget-h">דירות חדשות עד 1.2 מיליון, עד 1.5 מיליון ועד 3 מיליון</h2>' ), 'budget: 6 panels + heading' );
ok( 5 === substr_count( $bh, ' hidden>' ) && false !== strpos( $bh, 'פרויקט חדש אחד מתוך 344 שפרסמו מחיר מתחיל ב־1,200,000 ₪ או פחות' ), 'budget opens on 1.2 million, honest count' );
ok( 5 === substr_count( $sh, '<tr><th scope="row">' ) && false !== strpos( $sh, '<h2 id="nlph-stages-h">פרויקטים חדשים על הנייר, בפריסייל ובבנייה</h2>' ), 'stages table' );
ok( false !== strpos( $dh, 'id="nlph-devs"' ) && false !== strpos( $dh, 'חברות עם פרויקט חדש אחד' ), 'developers board' );
ok( 7 === substr_count( $rh, 'class="nlrd-pic"' ) && 7 === substr_count( $rh, '<ul class="nlrd-chips">' ), 'pictures on 7 ready cards' );
ok( ! preg_match( '~(?:הכי טוב|הטוב ביותר|מומלץ|גרוע|בעייתי)~u', $bh . $sh . $dh ), 'no ranking or negative words' );
ok( ! preg_match( '/[\x00-\x08\x0b\x0c\x0e-\x1f]/', $q . $c1 . $c2 . $c3 ), 'no control characters' );
if ( ! empty( $argv[1] ) ) { file_put_contents( $argv[1], '<!doctype html><meta charset="utf-8">' . $q . '<div class="nldir-results">' . $c1 . $c2 . $c3 . '</div>' ); }
echo ( $bad ? "FAILED $bad" : 'all passed' ), "\n";
exit( $bad ? 1 : 0 );
