<?php
// DRAFT smoke test (HAD-436): the exposure module's logic with WordPress stubbed. php smoke-test.php -> ok=32 bad=0. Not a substitute for the live checks.
define( 'ABSPATH', __DIR__ ); define( 'OBJECT', 'OBJECT' );
$GLOBALS['opt'] = array();
$GLOBALS['meta'] = array();
$GLOBALS['posts'] = array();
$GLOBALS['admin'] = false;
$GLOBALS['actions'] = array();
function get_option( $k, $d = false ) { return $GLOBALS['opt'][ $k ] ?? $d; }
function update_option( $k, $v, $a = null ) { $GLOBALS['opt'][ $k ] = $v; return true; }
function get_post_meta( $id, $k, $s = true ) { return $GLOBALS['meta'][ $id ][ $k ] ?? ''; }
function get_post_type( $id ) { return $GLOBALS['posts'][ $id ]['type'] ?? false; }
function get_post_status( $id ) { return $GLOBALS['posts'][ $id ]['status'] ?? false; }
function get_post_field( $f, $id ) { return $GLOBALS['posts'][ $id ][ $f ] ?? ''; }
function get_permalink( $id ) { return 'https://nad-lan.co.il/' . ( $GLOBALS['posts'][ $id ]['path'] ?? ( 'p' . $id ) ) . '/'; }
function get_the_title( $id ) { return $GLOBALS['posts'][ $id ]['title'] ?? ''; }
function current_user_can( $c ) { return $GLOBALS['admin']; }
function is_admin() { return false; }
function sanitize_key( $s ) { return preg_replace( '/[^a-z0-9_\-]/', '', strtolower( (string) $s ) ); }
function sanitize_title( $s ) { return preg_replace( '/[^a-z0-9\-]/', '', strtolower( (string) $s ) ); }
function sanitize_text_field( $s ) { return trim( strip_tags( (string) $s ) ); }
function wp_unslash( $s ) { return $s; }
function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES ); }
function esc_attr( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES ); }
function esc_url( $s ) { return (string) $s; }
function esc_url_raw( $s ) { return (string) $s; }
function do_action( ...$a ) { $GLOBALS['actions'][] = $a[0]; }
function nocache_headers() {}
function has_post_thumbnail( $id ) { return false; }
function add_filter( ...$a ) {}
function add_action( ...$a ) {}
function nlds_icon( $k ) { return '<svg/>'; }
function nadlan_prof_wa_digits( $p ) { $d = preg_replace( '/\D/', '', (string) $p ); return '' === $d ? '' : ( '0' === $d[0] ? '972' . substr( $d, 1 ) : $d ); }
function nadlan_dir_prof_label( $k, $id ) { return 'f' === get_post_meta( $id, 'nl_gender' ) ? 'מתווכת' : 'מתווך'; }
function nadlan_dir_registry_verified( $id ) { return (int) get_post_meta( $id, 'verified_at' ) > 0; }
function nadlan_ps_close( $html, $start, $tag ) { $depth = 0; $pos = $start; while ( preg_match( '#<(/?)' . $tag . '\b[^>]*>#i', $html, $m, PREG_OFFSET_CAPTURE, $pos ) ) { $depth += '/' === $m[1][0] ? -1 : 1; $pos = $m[0][1] + strlen( $m[0][0] ); if ( 0 === $depth ) { return $pos; } } return 0; }
function nadlan_ps_config() { return array( 'rainbow-tel-aviv' => array( 'name' => 'ריינבו תל אביב', 'name_en' => 'Rainbow Tel Aviv', 'rail' => array( 7833 ) ), 'hamedina' => array( 'name' => 'מגדלי כיכר המדינה', 'name_en' => 'Kikar Hamedina Towers', 'rail' => array(), 'i18n' => array( 'ru' => array( 'name' => 'Башни Кикар ха-Медина' ) ) ) ); }

require __DIR__ . '/broker-exposure.php';

// Meital (legacy, featured by tier, rail on Rainbow), Gili (new, private, no licence), an imported broker (legacy listed)
$GLOBALS['posts'][7833] = array( 'type' => 'nadlan_professional', 'status' => 'publish', 'title' => 'מיטל קציר · נדל״ן על הים', 'post_date_gmt' => '2026-09-17 10:00:00', 'path' => 'professionals/meital-katzir' );
$GLOBALS['meta'][7833]  = array( 'profession' => 'metavech', 'nl_tier' => 'pro', 'license_number' => '3131540', 'verified_at' => 1790245052, 'nl_name_he' => 'מיטל קציר', 'nl_name_en' => 'Meital Katzir', 'company_name' => 'נדל״ן על הים', 'nl_brand_en' => 'Real Estate by the Sea', 'nl_gender' => 'f', 'phone' => '052-3631582', 'nl_site_he' => 7644, 'nl_site_en' => 7804, 'areas_served' => 'נופי ים,כוכב הצפון,צוקי אביב', 'nl_areas_en' => 'Nofei Yam,Kochav HaTzafon' );
$GLOBALS['posts'][7644] = array( 'type' => 'page', 'status' => 'publish', 'path' => 'brokers/meital-katzir' );
$GLOBALS['posts'][7804] = array( 'type' => 'page', 'status' => 'publish', 'path' => 'en/brokers/meital-katzir' );
$GLOBALS['posts'][9001] = array( 'type' => 'nadlan_professional', 'status' => 'private', 'title' => 'גיל נסים · ה׳ באייר נדל״ן', 'post_date_gmt' => '2026-10-06 10:00:00', 'path' => 'professionals/heh-biyar' );
$GLOBALS['meta'][9001]  = array( 'profession' => 'metavech', 'license_number' => '', 'nl_name_he' => 'גיל נסים', 'nl_name_en' => 'Gil Nissim', 'company_name' => 'ה׳ באייר נדל״ן', 'nl_brand_en' => 'Heh B’iyar Real Estate', 'nl_gender' => 'm', 'phone' => '054-2442555', 'nl_site_he' => 9002, 'nl_site_en' => 9003, 'areas_served' => 'כיכר המדינה,הצפון הישן,הצפון החדש', 'nl_areas_en' => 'Kikar Hamedina,Old North,New North' );
$GLOBALS['posts'][9002] = array( 'type' => 'page', 'status' => 'private', 'path' => 'brokers/heh-biyar' );
$GLOBALS['posts'][9003] = array( 'type' => 'page', 'status' => 'private', 'path' => 'en/brokers/heh-biyar' );
$GLOBALS['posts'][5555] = array( 'type' => 'nadlan_professional', 'status' => 'publish', 'title' => 'מתווך מהפנקס', 'post_date_gmt' => '2026-08-01 10:00:00' );
$GLOBALS['meta'][5555]  = array( 'profession' => 'metavech', 'source' => 'metavhim' );

$ok = 0; $bad = 0;
function t( $name, $cond ) { global $ok, $bad; if ( $cond ) { $ok++; } else { $bad++; echo "FAIL $name\n"; } }

// 1. before the release (no since, no entries): today's behaviour
t( 'meital legacy featured', 4 === nadlan_bx_rank( 7833 ) && nadlan_bx_can( 7833, 'featured' ) );
t( 'meital legacy on rainbow he', array( 7833 ) === nadlan_bx_project_brokers( 'rainbow-tel-aviv', 'he' ) );
t( 'meital legacy not on rainbow en', array() === nadlan_bx_project_brokers( 'rainbow-tel-aviv-en', 'en' ) );
t( 'imported legacy listed', 2 === nadlan_bx_rank( 5555 ) && nadlan_bx_can( 5555, 'directory' ) && ! nadlan_bx_can( 5555, 'featured' ) );

// 2. the release seeds: since + Meital's entry (byte-identical) + Gili hidden with Kikar ticked
$GLOBALS['admin'] = true;
nadlan_bx_seed( array(
	7833 => array( 'level' => 'featured', 'projects' => array( 'rainbow-tel-aviv' => array( 'he' ) ), 'licence_ok' => 1, 'licence_note' => 'verified_at 24.9.2026', 'menu' => 0, 'order' => 10 ),
	9001 => array( 'level' => 'hidden', 'projects' => array( 'hamedina' => array( 'he', 'en', 'fr', 'ru', 'ar' ) ), 'licence_ok' => 0, 'licence_note' => 'not in the active register 3.10.2026', 'menu' => 1, 'order' => 20 ),
) );
$GLOBALS['opt']['nadlan_bx_since'] = strtotime( '2026-10-06 00:00:00 UTC' );
nadlan_bx_store( true );
$GLOBALS['admin'] = false;
t( 'meital seeded same', array( 7833 ) === nadlan_bx_project_brokers( 'rainbow-tel-aviv', 'he' ) && nadlan_bx_can( 7833, 'featured' ) && ! nadlan_bx_can( 7833, 'menu' ) );
t( 'gili hidden anon kikar he', array() === nadlan_bx_project_brokers( 'hamedina', 'he' ) );
t( 'gili hidden anon kikar ru', array() === nadlan_bx_project_brokers( 'hamedina-ru', 'ru' ) );
t( 'gili hidden anon site', '' === nadlan_bx_site_url( 9001, 'he' ) && ! nadlan_bx_can( 9001, 'directory' ) && empty( nadlan_bx_menu_links() ) );
t( 'imported still listed after release', nadlan_bx_can( 5555, 'directory' ) );

// 3. a new card created after the release with no entry: hidden
$GLOBALS['posts'][9100] = array( 'type' => 'nadlan_professional', 'status' => 'publish', 'title' => 'חדש', 'post_date_gmt' => '2026-10-07 10:00:00' );
$GLOBALS['meta'][9100]  = array( 'profession' => 'metavech', 'license_number' => '1234567', 'verified_at' => 1 );
t( 'new card default hidden', 0 === nadlan_bx_rank( 9100 ) && ! nadlan_bx_can( 9100, 'directory' ) );
$GLOBALS['meta'][9100]['source'] = 'broker_join';
t( 'new join default listed', 2 === nadlan_bx_rank( 9100 ) && nadlan_bx_can( 9100, 'directory' ) );

// 4. admin preview of Gili on the Kikar page, all five languages
$GLOBALS['admin'] = true;
$_GET['nlbx_preview'] = '9001';
t( 'preview he', array( 9001 ) === nadlan_bx_project_brokers( 'hamedina', 'he' ) );
t( 'preview ar', array( 9001 ) === nadlan_bx_project_brokers( 'hamedina-ar', 'ar' ) );
t( 'preview site private ok', 'https://nad-lan.co.il/brokers/heh-biyar/' === nadlan_bx_site_url( 9001, 'he' ) );
t( 'preview ar site = en', 'https://nad-lan.co.il/en/brokers/heh-biyar/' === nadlan_bx_site_url( 9001, 'ar' ) );
$ps = nadlan_ps_config()['hamedina'] + array( 'slug' => 'hamedina', 'lang' => 'ru' );
$sq = nadlan_bx_square_html( 9001, $ps );
t( 'square ru no hebrew', '' !== $sq && ! preg_match( '/\p{Hebrew}/u', strip_tags( $sq ) ) && false !== strpos( $sq, 'Только для администратора' ) && false !== strpos( $sq, rawurlencode( 'Башни Кикар ха-Медина' ) ) );
$ps['lang'] = 'he';
$sqh = nadlan_bx_square_html( 9001, $ps );
t( 'square he has office, ad label, preview badge, site button', false !== strpos( $sqh, 'ה׳ באייר נדל״ן' ) && false !== strpos( $sqh, 'פרסומת' ) && false !== strpos( $sqh, 'תצוגה למנהל בלבד' ) && false !== strpos( $sqh, 'לאתר של גיל' ) );
t( 'no commission words', ! preg_match( '/עמלה|דמי תיווך|commission/u', $sqh . $sq ) );
// the line inside #nlws-sale
$html = '<body><section class="nlws" id="nlws-ask"><p>x</p></section><section class="nlws" id="nlws-sale"><h2>למכירה</h2><p>אפשר לעיין ולפנות ל<a href="https://nad-lan.co.il/brokers/">מתווכי נדל״ן</a> עם תיאור.</p><h3>השכרה</h3><p>y</p></section><section id="z"></section></body>';
$out = nadlan_bx_strip_insert( $html, $ps );
$i_strip = strpos( $out, 'nlbx-strip' ); $i_h3 = strpos( $out, '<h3>השכרה' ); $i_link = strpos( $out, 'מתווכי נדל״ן</a>' );
t( 'strip after the brokers paragraph, before rent', false !== $i_strip && $i_link < $i_strip && $i_strip < $i_h3 );
t( 'strip once', $out === nadlan_bx_strip_insert( $out, $ps ) );
t( 'no section, no strip', '<body><p>a</p></body>' === nadlan_bx_strip_insert( '<body><p>a</p></body>', $ps ) );
unset( $_GET['nlbx_preview'] );

// 5. the licence gate on save, then Ben confirms and raises Gili
$GLOBALS['admin'] = true;
t( 'save refused without licence', 'licence' === nadlan_bx_save( 9001, array( 'level' => 'projects', 'projects' => array( 'hamedina' => array( 'he', 'en', 'fr', 'ru', 'ar' ) ), 'licence_ok' => 1 ) ) );
$GLOBALS['meta'][9001]['license_number'] = '7654321';
t( 'save refused licence not confirmed', 'licence' === nadlan_bx_save( 9001, array( 'level' => 'projects', 'projects' => array( 'hamedina' => array( 'he' ) ), 'licence_ok' => 0 ) ) );
function clean_post_cache( $id ) {}
function wp_transition_post_status( $n, $o, $p ) {}
function get_post( $id ) { return (object) array( 'ID' => $id ); }
function get_current_user_id() { return 1; }
function get_page_by_path( $p, $o = null, $t = 'page' ) { return null; }
class FakeDb { public $posts = 'wp_posts'; function update( $t, $d, $w ) { $GLOBALS['posts'][ $w['ID'] ]['status'] = $d['post_status']; return 1; } }
$GLOBALS['wpdb'] = new FakeDb();
function wp_json_encode( $v ) { return json_encode( $v ); }
function wp_date( $f, $t ) { return date( $f, $t ); }
$err = nadlan_bx_save( 9001, array( 'level' => 'featured', 'projects' => array( 'hamedina' => array( 'he', 'en', 'fr', 'ru', 'ar' ) ), 'licence_ok' => 1, 'licence_note' => 'Ben, by phone', 'menu' => 1, 'order' => 20 ) );
t( 'save ok', '' === $err );
t( 'statuses flipped public', 'publish' === get_post_status( 9001 ) && 'publish' === get_post_status( 9002 ) && 'publish' === get_post_status( 9003 ) );
t( 'purge all on directory/featured/menu change', in_array( 'litespeed_purge_all', $GLOBALS['actions'], true ) );
$GLOBALS['admin'] = false;
t( 'gili public on kikar 5 langs', array( 9001 ) === nadlan_bx_project_brokers( 'hamedina', 'he' ) && array( 9001 ) === nadlan_bx_project_brokers( 'hamedina-fr', 'fr' ) );
t( 'gili in menu', 1 === count( nadlan_bx_menu_links() ) );
$sq2 = nadlan_bx_square_html( 9001, $ps );
t( 'public square has licence, no preview badge', false !== strpos( $sq2, '7654321' ) && false === strpos( $sq2, 'תצוגה למנהל' ) );
// 6. Ben lowers him back to hidden
$GLOBALS['admin'] = true;
t( 'lower to hidden ok', '' === nadlan_bx_save( 9001, array( 'level' => 'hidden', 'projects' => array( 'hamedina' => array( 'he' ) ), 'licence_ok' => 1 ) ) );
$GLOBALS['admin'] = false;
t( 'hidden again everywhere', array() === nadlan_bx_project_brokers( 'hamedina', 'he' ) && 'private' === get_post_status( 9001 ) && 'private' === get_post_status( 9002 ) && empty( nadlan_bx_menu_links() ) );
t( 'log kept', 2 === count( nadlan_bx_entry( 9001 )['log'] ) && isset( nadlan_bx_entry( 9001 )['log'][0]['flips'] ) );

echo "ok=$ok bad=$bad\n";
