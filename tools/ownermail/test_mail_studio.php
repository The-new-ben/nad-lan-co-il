<?php
// Local test of inc/mail-studio.php with WordPress stubs (HAD-687 part 2). Writes the three looks next to this file (studio-letter.html,
// studio-listings.html, studio-update.html; fictional people and listings marked as examples). Run: php -d extension=mbstring tools/ownermail/test_mail_studio.php
define( 'ABSPATH', __DIR__ );
define( 'DAY_IN_SECONDS', 86400 );
define( 'MINUTE_IN_SECONDS', 60 );
date_default_timezone_set( 'UTC' );
$GLOBALS['O'] = array( 'admin_email' => 'owner@example.com' ); $GLOBALS['META'] = $GLOBALS['POST'] = $GLOBALS['F'] = array();
function add_action() {} function register_post_type() {} function register_rest_route() {}
function add_filter( $h, $cb ) { $GLOBALS['F'][ $h ][] = $cb; }
function get_option( $k, $d = false ) { return $GLOBALS['O'][ $k ] ?? $d; }
function update_option( $k, $v, $a = null ) { $GLOBALS['O'][ $k ] = $v; }
function wp_parse_args( $a, $d ) { return array_merge( $d, (array) $a ); }
function wp_get_current_user() { return new class { public $display_name = 'בן'; public $user_email = 'owner@example.com'; function exists() { return true; } }; }
function get_post_meta( $id, $k, $s = false ) { return $GLOBALS['META'][ $id ][ $k ] ?? ''; }
function get_post( $id ) { return $GLOBALS['POST'][ $id ] ?? null; }
function get_post_type( $id ) { return isset( $GLOBALS['POST'][ $id ] ) ? $GLOBALS['POST'][ $id ]->post_type : ''; }
function get_the_title( $id ) { return $GLOBALS['POST'][ $id ]->post_title ?? ''; }
function get_permalink( $id ) { return 'https://nad-lan.co.il/?p=' . (int) $id; }
function get_the_post_thumbnail_url( $id, $s ) { return ''; }
function url_to_postid( $u ) { return preg_match( '/[?&]p=(\d+)/', $u, $m ) ? (int) $m[1] : 0; }
function get_site_icon_url( $s ) { return 'https://nad-lan.co.il/wp-content/uploads/site-icon-96.png'; }
function home_url( $p = '' ) { return 'https://nad-lan.co.il' . $p; }
function rest_url( $p ) { return 'https://nad-lan.co.il/wp-json/' . $p; }
function add_query_arg( $a, $u ) { return $u . '?' . http_build_query( $a ); }
function wp_salt( $s ) { return 'test-salt'; }
function esc_url( $u, $p = null ) { return htmlspecialchars( (string) $u, ENT_QUOTES ); }
function esc_url_raw( $u ) { return (string) $u; }
function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES ); }
function esc_attr( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES ); }
function wp_strip_all_tags( $s ) { return strip_tags( (string) $s ); }
function sanitize_text_field( $s ) { return trim( strip_tags( (string) $s ) ); }
function sanitize_textarea_field( $s ) { return trim( strip_tags( (string) $s ) ); }
function sanitize_email( $s ) { return filter_var( trim( (string) $s ), FILTER_VALIDATE_EMAIL ) ? trim( (string) $s ) : ''; }
function wp_unslash( $s ) { return $s; }
function is_email( $e ) { return (bool) filter_var( $e, FILTER_VALIDATE_EMAIL ); }
function wp_json_encode( $v, $f = 0 ) { return json_encode( $v, $f ); }
function wp_date( $f, $t = null ) { return gmdate( $f, null === $t ? time() : $t ); }
require dirname( __DIR__, 2 ) . '/plugins/nadlan-config/inc/mail-studio.php';
$fail = 0;
function ok( $c, $m ) { global $fail; echo ( $c ? 'PASS ' : 'FAIL ' ) . $m . "\n"; if ( ! $c ) { $fail++; } }

// fictional listings (examples only)
$GLOBALS['POST'][801] = (object) array( 'post_type' => 'nadlan_property', 'post_status' => 'publish', 'post_title' => 'דירת 4 חדרים עם מרפסת (דוגמה)' );
$GLOBALS['META'][801] = array( 'city' => 'רמת גן', 'neighborhood' => 'מרום נווה', 'rooms' => '4', 'size_sqm' => '104', 'price' => '2890000', 'listing_type' => 'sale' );
$GLOBALS['POST'][802] = (object) array( 'post_type' => 'nadlan_project', 'post_status' => 'publish', 'post_title' => 'פרויקט לדוגמה בגבעתיים' );
$GLOBALS['META'][802] = array( 'city' => 'גבעתיים', 'num_units' => '120' );
$GLOBALS['POST'][803] = (object) array( 'post_type' => 'nadlan_lead', 'post_status' => 'private', 'post_title' => 'not a listing' );

// 1. the text
$h = nadlan_ms_text( "## כותרת\nשורה ראשונה\nשורה שנייה\n\n- אחת\n- **שתיים**\n\nקישור https://nad-lan.co.il/projects/ ל{שם}", 'דנה' );
ok( false !== strpos( $h, '<h2' ) && false !== strpos( $h, '<br>' ) && 2 === substr_count( $h, '<li' ) && false !== strpos( $h, '<strong' ), 'subheading, lines, bullets, bold' );
ok( false !== strpos( $h, 'href="https://nad-lan.co.il/projects/"' ) && false !== strpos( $h, 'לדנה' ), 'a link and the first name' );
ok( false === strpos( nadlan_ms_text( '<script>x</script>', '' ), '<script' ), 'HTML in the text is escaped' );
// 2. items
ok( array( 801, 802 ) === nadlan_ms_resolve( "801\nhttps://nad-lan.co.il/?p=802\n803\n999" ), 'listings by number and link; a lead and a missing id are dropped' );
$it = nadlan_ms_item( 801 );
ok( '2,890,000 ₪' === $it['price'] && in_array( '4 חדרים', $it['facts'], true ) && in_array( '104 מ״ר', $it['facts'], true ), 'property facts: ' . json_encode( $it, JSON_UNESCAPED_UNICODE ) );
$ip = nadlan_ms_item( 802 );
ok( '' === $ip['price'] && in_array( '120 יח״ד', $ip['facts'], true ), 'a project without a price shows no price (unknown is left out)' );
// 3. fields and the law
$f = nadlan_ms_fields( array( 'kind' => 'dist', 'look' => 'listings', 'subject' => 'דירות חדשות ברמת גן', 'body' => 'x', 'items' => '801' ) );
ok( 0 === mb_strpos( $f['subject'], 'פרסומת: ' ) && $f['ad'], 'a distribution subject starts with "פרסומת:" (30A)' );
$f2 = nadlan_ms_fields( array( 'kind' => 'dist', 'subject' => 'פרסומת: כבר יש' ) );
ok( 'פרסומת: כבר יש' === $f2['subject'], 'no double prefix' );
$fp = nadlan_ms_fields( array( 'kind' => 'personal', 'subject' => 'פגישה מחר', 'to' => 'dana@example.com' ) );
ok( 'פגישה מחר' === $fp['subject'] && ! $fp['ad'], 'a personal mail has no ad prefix' );
// 4. the unsubscribe link
$u = nadlan_ms_unsub_url( 'Dana@Example.com' );
parse_str( parse_url( $u, PHP_URL_QUERY ), $q );
ok( hash_equals( nadlan_ms_unsub_sig( rawurldecode( $q['e'] ) ), $q['s'] ) && 'dana@example.com' === rawurldecode( $q['e'] ), 'the refusal link is signed for the lower-case address' );
ok( nadlan_ms_unsub_sig( 'a@example.com' ) !== nadlan_ms_unsub_sig( 'b@example.com' ), 'one signature per address' );

// 5. the three looks
$base = array( 'sign' => true, 'greeting' => 'שלום {שם},' );
$looks = array(
	'letter'   => $base + array( 'look' => 'letter', 'subject' => 'בהמשך לשיחה שלנו', 'pre' => 'הסיכום והצעדים הבאים', 'title' => 'בהמשך לשיחה שלנו', 'body' => "תודה על השיחה היום. ריכזתי את מה שדיברנו עליו:\n\n- המחיר שהוצע מול עסקאות דומות באזור\n- מה לבדוק בחוזה לפני חתימה\n- **השלב הבא:** סיור בדירה ביום חמישי\n\nאם משהו לא ברור, אפשר פשוט להשיב למייל הזה.", 'cta_text' => 'קביעת סיור', 'cta_url' => 'https://nad-lan.co.il/' ),
	'listings' => $base + array( 'look' => 'listings', 'ad' => true, 'subject' => 'פרסומת: שתי הזדמנויות ברמת גן ובגבעתיים', 'pre' => 'דירת 4 חדרים ופרויקט חדש, עם כל הפרטים', 'title' => 'שתי הזדמנויות שכדאי לראות השבוע', 'body' => 'בחרנו בשבילך שני נכסים שמתאימים למה שחיפשת. כל הנתונים מעודכנים להיום.', 'items' => array( 801, 802 ), 'cta_text' => 'לכל הנכסים באזור', 'cta_url' => 'https://nad-lan.co.il/properties/' ),
	'update'   => $base + array( 'look' => 'update', 'ad' => true, 'subject' => 'פרסומת: מה קרה למחירי הדירות השנה', 'pre' => 'מדד מחירי הדירות ירד ב־1.8% ב־12 חודשים', 'figure' => '-1.8%', 'figure_cap' => 'מדד מחירי הדירות, 12 חודשים (הלמ״ס, נתוני דוגמה)', 'title' => 'המחירים זזים. הנה מה שזה אומר בשבילך', 'body' => "## מה השתנה\nהמחירים ירדו מעט ברוב האזורים, והמשכנתאות התייקרו.\n\n## מה לעשות עכשיו\n- לבדוק עסקאות אמיתיות באזור לפני הצעה\n- לבנות תוכנית הון עצמי", 'cta_text' => 'למחשבון ולמפה', 'cta_url' => 'https://nad-lan.co.il/apartment-prices/' ),
);
foreach ( $looks as $k => $f ) {
	$html = nadlan_ms_render( $f, 'דנה', ! empty( $f['ad'] ) ? nadlan_ms_unsub_url( 'dana@example.com' ) : '' );
	file_put_contents( __DIR__ . '/studio-' . $k . '.html', $html );
	ok( false !== strpos( $html, 'lang="he" dir="rtl"' ) && false !== strpos( $html, 'role="article"' ) && false !== strpos( $html, '<h1' ), "$k: lang, dir, article role, one h1" );
	ok( 1 === substr_count( $html, '<h1' ) && strlen( $html ) < 60000 && ! preg_match( "/[\x{2013}\x{2014}]/u", $html ), "$k: one h1, " . strlen( $html ) . ' bytes, no long dash' );
	ok( ! empty( $f['ad'] ) === ( false !== strpos( $html, 'להסרה מרשימת התפוצה</a>' ) && false !== strpos( $html, '>פרסומת<' ) ), "$k: the ad label and the refusal link exactly when it is an ad" );
	ok( false !== strpos( $html, 'שלום דנה,' ), "$k: the greeting names the reader" );
}
$pl = nadlan_ms_plain( $looks['listings'], 'דנה', 'https://x/unsub' );
ok( false !== strpos( $pl, 'להסרה מרשימת התפוצה: https://x/unsub' ) && false !== strpos( $pl, '2,890,000 ₪' ), 'the plain-text twin carries the listings and the refusal link' );
echo $fail ? "\n$fail FAILED\n" : "\nALL PASSED\n";
exit( $fail ? 1 : 0 );
