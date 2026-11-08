<?php
// Local test of inc/owner-mail.php + inc/owner-morning.php with WordPress stubs (HAD-687). Writes the rendered sample mails next to this
// file (sample-lead.html, sample-morning.html; fictional people and numbers). Run: php -d extension=mbstring tools/ownermail/test_owner_mail.php
define( 'ABSPATH', __DIR__ );
define( 'DAY_IN_SECONDS', 86400 );
define( 'HOUR_IN_SECONDS', 3600 );
define( 'MINUTE_IN_SECONDS', 60 );
date_default_timezone_set( 'UTC' );
$GLOBALS['T'] = $GLOBALS['O'] = $GLOBALS['META'] = $GLOBALS['POST'] = $GLOBALS['F'] = $GLOBALS['MAIL'] = $GLOBALS['SCHED'] = array();
function add_action() {} function register_rest_route() {} function wp_add_dashboard_widget() {} function remove_action() {}
function add_filter( $h, $cb ) { $GLOBALS['F'][ $h ][] = $cb; }
function apply_filters( $h, $v ) { return $v; }
function get_transient( $k ) { return $GLOBALS['T'][ $k ] ?? false; }
function set_transient( $k, $v, $t = 0 ) { $GLOBALS['T'][ $k ] = $v; return true; }
function delete_transient( $k ) { unset( $GLOBALS['T'][ $k ] ); }
function get_option( $k, $d = false ) { return $GLOBALS['O'][ $k ] ?? $d; }
function update_option( $k, $v, $a = null ) { $GLOBALS['O'][ $k ] = $v; return true; }
function get_post_meta( $id, $k, $s = false ) { return $GLOBALS['META'][ $id ][ $k ] ?? ''; }
function update_post_meta( $id, $k, $v ) { $GLOBALS['META'][ $id ][ $k ] = $v; }
function delete_post_meta( $id, $k ) { unset( $GLOBALS['META'][ $id ][ $k ] ); }
function get_post( $id ) { return $GLOBALS['POST'][ $id ] ?? null; }
function get_post_type( $id ) { return isset( $GLOBALS['POST'][ $id ] ) ? $GLOBALS['POST'][ $id ]->post_type : ''; }
function get_post_field( $f, $id ) { return isset( $GLOBALS['POST'][ $id ] ) ? $GLOBALS['POST'][ $id ]->$f : ''; }
function get_the_title( $id ) { return $GLOBALS['POST'][ $id ]->post_title ?? ''; }
function get_permalink( $id ) { return 'https://nad-lan.co.il/?p=' . (int) $id; }
function get_post_time( $f, $g, $id ) { return strtotime( $GLOBALS['POST'][ $id ]->post_date_gmt . ' UTC' ); }
function get_the_date( $f, $id ) { return gmdate( $f, get_post_time( 'U', true, $id ) ); }
function get_posts( $a ) { $r = array_values( array_filter( $GLOBALS['POST'], function ( $p ) { return 'nadlan_lead' === $p->post_type; } ) ); return ! empty( $a['fields'] ) ? array() : $r; }
function wp_date( $f, $t = null ) { return gmdate( $f, null === $t ? time() : $t ); }
function wp_timezone() { return new DateTimeZone( 'Asia/Jerusalem' ); }
function wp_salt( $s ) { return 'test-salt'; }
function rest_url( $p ) { return 'https://nad-lan.co.il/wp-json/' . $p; }
function admin_url( $p ) { return 'https://nad-lan.co.il/wp-admin/' . $p; }
function add_query_arg( $a, $u ) { return $u . '?' . http_build_query( $a ); }
function esc_url( $u, $p = null ) { return htmlspecialchars( (string) $u, ENT_QUOTES ); }
function esc_url_raw( $u ) { return (string) $u; }
function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES ); }
function esc_attr( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES ); }
function wp_strip_all_tags( $s ) { return strip_tags( (string) $s ); }
function sanitize_key( $s ) { return preg_replace( '/[^a-z0-9_\-]/', '', strtolower( (string) $s ) ); }
function absint( $v ) { return abs( (int) $v ); }
function is_email( $e ) { return (bool) filter_var( $e, FILTER_VALIDATE_EMAIL ); }
function wp_parse_url( $u, $c = -1 ) { return parse_url( $u, $c ); }
function number_format_i18n( $n ) { return number_format( (float) $n ); }
function wp_json_encode( $v ) { return json_encode( $v, JSON_UNESCAPED_UNICODE ); }
function wp_next_scheduled( $h, $a = array() ) { return $GLOBALS['SCHED'][ $h . json_encode( $a ) ] ?? false; }
function wp_mail( $to, $s, $b, $h = array() ) { $GLOBALS['MAIL'][] = array( $to, $s, $b ); return true; }
function current_user_can() { return true; }
function get_current_user_id() { return 0; }
class WPDB_Stub {
	public $prefix = 'wp_', $posts = 'wp_posts', $postmeta = 'wp_postmeta';
	function prepare( $q ) { return $q; } function esc_like( $s ) { return $s; }
	function get_var( $q ) { return false !== strpos( $q, 'nadlan_pview' ) ? 14 : ( false !== strpos( $q, 'price_alert' ) ? 2 : 3 ); }
	function get_col( $q ) { return array(); }
	function get_results( $q ) {
		if ( false !== strpos( $q, 'lead_first_response_at' ) ) { return array( (object) array( 'd' => gmdate( 'Y-m-d H:i:s', time() - 3600 ), 'r' => time() - 3600 + 420 ) ); }
		return false !== strpos( $q, 'nadlan_pview' ) ? array( (object) array( 'post_id' => 901, 'v' => 9, 'r' => 5, 'c' => 1, 'g' => 6, 'w' => 2, 's' => 0 ) ) : array();
	}
}
$GLOBALS['wpdb'] = new WPDB_Stub();
require dirname( __DIR__, 2 ) . '/plugins/nadlan-config/inc/owner-mail.php';
require dirname( __DIR__, 2 ) . '/plugins/nadlan-config/inc/owner-morning.php';
$fail = 0;
function ok( $c, $m ) { global $fail; echo ( $c ? 'PASS ' : 'FAIL ' ) . $m . "\n"; if ( ! $c ) { $fail++; } }

// fixtures: a project, a property, a form lead and a price-window lead (fictional)
$now = time();
$GLOBALS['O']['admin_email'] = 'owner@example.com';
$GLOBALS['POST'][700] = (object) array( 'ID' => 700, 'post_type' => 'nadlan_project', 'post_title' => 'גפן 8-10, רמת גן', 'post_content' => '', 'post_date_gmt' => gmdate( 'Y-m-d H:i:s', $now ) );
$GLOBALS['POST'][901] = (object) array( 'ID' => 901, 'post_type' => 'nadlan_property', 'post_title' => 'דירת 4 חדרים בגבעתיים', 'post_content' => '', 'post_date_gmt' => gmdate( 'Y-m-d H:i:s', $now ) );
$GLOBALS['POST'][501] = (object) array( 'ID' => 501, 'post_type' => 'nadlan_lead', 'post_title' => 'lead', 'post_content' => 'מתעניינים בדירת 4 חדרים עם מרפסת, אפשר לקבל מחירים?', 'post_date_gmt' => gmdate( 'Y-m-d H:i:s', $now - 120 ) );
$GLOBALS['META'][501] = array( 'name' => 'דנה לוי', 'phone' => '050-123-4567', 'email' => 'dana@example.com', 'goal' => 'קבלת מחירים ותוכניות', 'rooms' => '4', 'budget' => '2,400,000 ₪', 'project_wp_id' => 700, 'source_url' => 'https://nad-lan.co.il/projects/gefen-8-10/', 'utm_source' => 'google', 'lead_status' => 'new', 'city' => 'רמת גן' );
$GLOBALS['POST'][502] = (object) array( 'ID' => 502, 'post_type' => 'nadlan_lead', 'post_title' => 'lead', 'post_content' => '', 'post_date_gmt' => gmdate( 'Y-m-d H:i:s', $now - 30 * HOUR_IN_SECONDS ) );
$GLOBALS['META'][502] = array( 'name' => 'יוסי כהן', 'phone' => '+972 52 765 4321', 'email' => 'yossi@example.com', 'goal' => 'עדכוני מחירים', 'project_wp_id' => 700, 'utm_source' => 'price_alert', 'pa_callback' => '1', 'lead_status' => 'new' );

// 1. signatures
$e = $now + 1000;
ok( nadlan_omx_check( 'contacted', 501, '', $e, nadlan_omx_sig( 'contacted', 501, '', $e ) ), 'a signed link checks' );
ok( ! nadlan_omx_check( 'lost', 501, '', $e, nadlan_omx_sig( 'contacted', 501, '', $e ) ), 'another action with the same signature fails' );
ok( ! nadlan_omx_check( 'contacted', 502, '', $e, nadlan_omx_sig( 'contacted', 501, '', $e ) ), 'another lead with the same signature fails' );
ok( ! nadlan_omx_check( 'contacted', 501, '', $now - 5, nadlan_omx_sig( 'contacted', 501, '', $now - 5 ) ), 'an expired link fails' );
ok( ! nadlan_omx_check( 'contacted', 501, '', $e, 'x' ), 'a short signature fails' );
parse_str( parse_url( nadlan_omx_url( 'mute', 0, 'hot' ), PHP_URL_QUERY ), $q );
ok( nadlan_omx_check( $q['a'], $q['l'], $q['k'], $q['e'], $q['s'] ) && $q['e'] > $now + 29 * DAY_IN_SECONDS, 'nadlan_omx_url makes a 30-day link that checks' );
// 2. phones
foreach ( array( '050-123-4567' => array( '972501234567', '050-123-4567' ), '+972 52 765 4321' => array( '972527654321', '052-765-4321' ), '03-1234567' => array( '97231234567', '03-123-4567' ), '+44 20 7946 0958' => array( '442079460958', '+442079460958' ) ) as $in => $w ) {
	$p = nadlan_omx_phone( $in );
	ok( $p[0] === $w[0] && $p[1] === '+' . $w[0] && $p[2] === $w[1], "phone $in -> " . json_encode( $p ) );
}
// 3. heat
$h1 = nadlan_omx_heat( 501 ); $h2 = nadlan_omx_heat( 502 );
ok( 'warm' === $h1['level'] || 'hot' === $h1['level'], 'form lead with rooms, budget and a message is warm or hot: ' . json_encode( $h1, JSON_UNESCAPED_UNICODE ) );
ok( isset( $h2['why']['בקשה לשיחה'] ), 'a price-window call-back counts as a call request: ' . json_encode( $h2, JSON_UNESCAPED_UNICODE ) );
// 4. the lead mail
list( $html, $text, $subj ) = nadlan_omx_lead_mail( 501 );
foreach ( array( 'href="tel:+972501234567"', 'https://wa.me/972501234567?text=', 'a=contacted', 'a=lost', 'a=snooze', 'a=mute', 'k=lead', '050-123-4567', 'גפן 8-10', 'dir="rtl"', 'חזרתי אליו', 'תזכיר לי מחר בבוקר' ) as $n ) {
	ok( false !== strpos( $html, $n ), "lead mail has $n" );
}
ok( 0 === strpos( $subj, 'ליד ' ) && false !== strpos( $subj, 'דנה לוי' ) && false !== strpos( $subj, '050-123-4567' ), "subject: $subj" );
ok( false !== strpos( $text, 'tel:+972501234567' ) && false !== strpos( $text, 'a=contacted' ), 'the plain-text twin has the call link and the actions' );
ok( strlen( $html ) < 60000, 'lead mail size ' . strlen( $html ) . ' bytes (Gmail clips at 102 KB)' );
ok( ! preg_match( "/[\x{2013}\x{2014}]/u", $html ), 'no long dash in the lead mail' );
file_put_contents( __DIR__ . '/sample-lead.html', $html );
// 5. once per lead, mute
ok( nadlan_omx_lead_alert( 501 ) && 1 === count( $GLOBALS['MAIL'] ), 'the first alert is sent' );
ok( ! nadlan_omx_lead_alert( 501 ) && 1 === count( $GLOBALS['MAIL'] ), 'the same lead is never mailed twice' );
nadlan_omx_mute( 'price_alert', true );
ok( ! nadlan_omx_lead_alert( 502 ) && 1 === count( $GLOBALS['MAIL'] ) && 0 === strpos( get_post_meta( 502, 'lead_omx_alert' ), 'muted' ), 'a muted kind is not mailed and is marked for the morning' );
nadlan_omx_mute( 'price_alert', false );
ok( ! nadlan_omx_muted( 'price_alert' ), 'unmute clears the mute' );
// 6. status, undo
nadlan_omx_set_status( 501, 'contacted' );
ok( 'contacted' === get_post_meta( 501, 'lead_status' ) && get_post_meta( 501, 'lead_first_response_at' ) > 0, 'contacted writes the status and the first response time' );
nadlan_omx_undo( 501 );
ok( 'new' === get_post_meta( 501, 'lead_status' ) && '' === get_post_meta( 501, 'lead_first_response_at' ), 'undo restores new and clears the first response time it set' );
// 7. the duplicate plain copy is held only when the card is scheduled
$GLOBALS['O']['admin_email'] = 'owner@example.com';
$pre = $GLOBALS['F']['pre_wp_mail'][0];
$atts = array( 'to' => 'owner@example.com', 'subject' => '[נדלן] ליד חדש - דנה', 'message' => "ניהול: https://nad-lan.co.il/wp-admin/post.php?post=501&action=edit" );
ok( null === $pre( null, $atts ), 'no scheduled card: the plain copy goes out' );
$GLOBALS['SCHED'][ 'nadlan_lead_rich_alert' . json_encode( array( 501 ) ) ] = $now + 120;
ok( true === $pre( null, $atts ), 'card scheduled: the plain copy is held' );
ok( null === $pre( null, array( 'to' => 'someone@example.com' ) + $atts ), 'a mail to anyone else is never touched' );
ok( null === $pre( null, array( 'subject' => 'ליד חם · ביקש/ה שיחה' ) + $atts ), 'the price window mail (another subject) is never touched' );
// 8. the morning mail
$GLOBALS['META'][502]['lead_omx_alert'] = '';
$GLOBALS['O']['nadlan_omx_gsc'] = array( 'at' => $now, 'days' => array( '2026-11-05' => array( 'c' => 41, 'i' => 3900 ), '2026-11-06' => array( 'c' => 52, 'i' => 4300 ) ) );
$m = nadlan_om_send( false );
foreach ( array( 'לטפל היום: 2', 'דנה לוי', 'יוסי כהן', 'מה השתנה מאתמול', 'לידים', 'נרשמים לעדכוני מחירים', 'קליקים מגוגל', '▲ +11', 'מי ראה נכסים אתמול', 'דירת 4 חדרים בגבעתיים', 'זמן חזרה ממוצע לליד (דקות)', 'a=contacted', 'href="tel:+972527654321"' ) as $n ) {
	ok( false !== strpos( $m, $n ), "morning mail has $n" );
}
ok( strlen( $m ) < 90000, 'morning mail size ' . strlen( $m ) . ' bytes' );
file_put_contents( __DIR__ . '/sample-morning.html', $m );
$GLOBALS['MAIL'] = array();
nadlan_om_send( true );
ok( 1 === count( $GLOBALS['MAIL'] ), 'the morning mail is sent once' );
nadlan_om_send( true );
ok( 1 === count( $GLOBALS['MAIL'] ) && 'skipped_repeat' === $GLOBALS['O']['nadlan_omx_log'][0]['r'], 'the same morning is not sent twice' );
echo $fail ? "\n$fail FAILED\n" : "\nALL PASSED\n";
exit( $fail ? 1 : 0 );
