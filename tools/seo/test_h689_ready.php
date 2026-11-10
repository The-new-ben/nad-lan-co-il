<?php
// HAD-689 step 2: the immediate-occupancy block of inc/projects-hub.php, rendered on the real data file without WordPress.
// php tools/seo/test_h689_ready.php [out.html]
define( 'ABSPATH', __DIR__ );
function add_action() {} function add_filter() {} function add_shortcode() {} function is_admin() { return false; }
function number_format_i18n( $n ) { return number_format( $n ); } function selected() {} function wp_json_encode( $d ) { return json_encode( $d, JSON_UNESCAPED_UNICODE ); }
function get_transient() { return false; } function set_transient() {} function rest_url( $p = "" ) { return "https://nad-lan.co.il/wp-json/" . $p; }
function home_url( $p = '/' ) { return 'https://nad-lan.co.il' . $p; }
function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_attr( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_url( $s ) { return (string) $s; }
function date_i18n( $f, $t ) { return date( $f, $t ); }
function wp_parse_url( $u, $c = -1 ) { return parse_url( $u, $c ); }
function plugins_url( $p = '', $f = '' ) { return 'https://nad-lan.co.il/wp-content/plugins/nadlan-config/' . $p; }
function add_query_arg( $k, $v, $u ) { return $u . '?' . $k . '=' . $v; }
function get_query_var( $k ) { return 0; }
$GLOBALS['t_archive'] = true;
function is_post_type_archive( $t ) { return $GLOBALS['t_archive']; }
if ( 'off' !== getenv( 'NLREADY' ) ) { $_GET['nlready'] = '1'; } // NLREADY=off: the gated default, nothing changes on the page
require dirname( __DIR__, 2 ) . '/plugins/nadlan-config/inc/projects-hub.php';

$bad = 0;
function ok( $cond, $what ) { global $bad; if ( ! $cond ) { $bad++; echo "FAIL $what\n"; } }

$c = nadlan_ph_market_counts();
ok( 564 === $c['all'] && 57 === $c['immediate'] && 24 === $c['near_occupancy'], 'counts ' . json_encode( $c ) );
$rows = nadlan_ph_ready_rows();
ok( 81 === count( $rows ), 'ready rows ' . count( $rows ) );
ok( 'immediate' === $rows[0]['status'] && ! empty( $rows[0]['price_from'] ) && false !== strpos( $rows[0]['city'], 'תל אביב' ), 'first row: Tel Aviv, immediate, priced' );
$tlv_n = 0; foreach ( $rows as $k => $r ) { if ( false !== strpos( $r['city'], 'תל אביב' ) ) { $tlv_n++; ok( $k < 24, 'Tel Aviv rows come first' ); } }
ok( 24 === $tlv_n, 'Tel Aviv rows ' . $tlv_n );

$a = nadlan_ph_answer_html();
ok( false !== strpos( $a, '<strong>564</strong> פרויקטים חדשים ודירות חדשות מקבלן למכירה עכשיו' ), 'answer head' );
ok( false !== strpos( $a, '<a href="#nlph-ready"><b>57</b> לאכלוס מיידי</a>' ) && false !== strpos( $a, '<b>24</b> באכלוס קרוב' ), 'answer counts' );
ok( false !== strpos( $a, 'נבדק ב־9.11.2026' ), 'answer date' );

$h = nadlan_ph_ready_html();
ok( 1 === substr_count( $h, '<h2 id="nlph-ready-h">דירות חדשות לאכלוס מיידי: 57 פרויקטים, ועוד 24 לאכלוס קרוב</h2>' ), 'h2' );
ok( 81 === substr_count( $h, '<article class="nlrd-card' ), 'cards ' . substr_count( $h, '<article class="nlrd-card' ) );
ok( 15 === substr_count( $h, 'nlrd-card nlrd-more' ) && 57 === substr_count( $h, 'nlrd-card is-off' ), 'opens on Tel Aviv: 9 shown, 15 more, 57 of other cities off' );
ok( 1 === substr_count( $h, '<option value="תל אביב יפו" selected>תל אביב יפו (24)</option>' ) && 1 === substr_count( $h, 'id="nlrd-land">כל הארץ: 81 פרויקטים' ), 'city preselected, whole-country button' );
ok( 57 === substr_count( $h, 'data-st="immediate" data-city' ) && 24 === substr_count( $h, 'data-st="near_occupancy" data-city' ), 'statuses on cards' );
foreach ( array( 'Ensemble', 'הרביעייה בסמאטס', 'yad2', 'madlan', '0 חדרים', 'בבדיקה', '—', '–' ) as $no ) { ok( false === strpos( $h, $no ), "forbidden in section: $no" ); }
foreach ( array( 'דירות מוכנות מקבלן', 'לכניסה מיידית', 'פרויקטים מאוכלסים', 'מדד תשומות הבנייה', 'רשות המסים', 'חוק המכר' ) as $yes ) { ok( false !== strpos( $h, $yes ), "synonym or fact missing: $yes" ); }
ok( substr_count( $h, 'rel="nofollow noopener"' ) >= 20, 'developer source links ' . substr_count( $h, 'rel="nofollow noopener"' ) );
ok( false === strpos( $h, '<h1' ), 'no h1 in the section' );
foreach ( array( 'אכלוס קרוב · 06/2026', 'אכלוס קרוב · 07/2026', 'אכלוס קרוב · 10/2026' ) as $past ) { ok( false === strpos( $h, $past ), "a passed month shown: $past" ); }
ok( false !== strpos( $h, 'אכלוס קרוב · 12/2026' ) && false !== strpos( $h, 'אכלוס קרוב · 02/2027' ), 'future months kept' );

if ( 'off' === getenv( 'NLREADY' ) ) {
	ok( true === nadlan_ph_top_wanted(), 'live for everyone: no parameter needed' ); // 1.72.629
	$_GET['city'] = 'חיפה'; // a filtered view is judged per request; this process already cached "wanted", so only the rule is read here
	echo ( $bad ? "FAILED $bad" : 'all passed (no parameter)' ), "
"; exit( $bad ? 1 : 0 );
}
// the top block and the body agree
$top = nadlan_ph_top_html();
ok( 1 === substr_count( $top, '<style id="nlph-css">' ) && 1 === substr_count( $top, 'id="nlph-ready"' ) && 1 === substr_count( $top, 'id="nlph-market"' ), 'top block: css + ready + market, once each' );
ok( strpos( $top, 'id="nlph-ready"' ) < strpos( $top, 'id="nlph-market"' ), 'ready before market' );
$body = nadlan_ph_body( array() );
ok( false === strpos( $body, 'id="nlph-market"' ) && false === strpos( $body, '<style id="nlph-css">' ) && false !== strpos( $body, '<script id="nlph-js">' ), 'body skips the table and the css, keeps the js' );
ok( false !== strpos( $body, 'id="nlph-faq"' ), 'body keeps the FAQ' );
// HAD-697 (Ben 10.11.2026): Google's related searches answered in passing, in the FAQ, with numbers printed from the data
$core = nadlan_ph_faq_core(); $rel = nadlan_ph_faq_related(); $faq = nadlan_ph_faq(); $ff = nadlan_ph_faq_facts();
ok( 24 === count( $core ) && 11 === count( $rel ) && 35 === count( $faq ), 'faq: core ' . count( $core ) . ' + related ' . count( $rel ) );
ok( $faq[0][0] === $core[0][0] && $faq[34][0] === $rel[10][0], 'faq order: the old questions first, the new ones after them' );
ok( 564 === $ff['all'] && 1 === $ff['u12'] && 9 === $ff['u15'] && 64 === $ff['deal'] && 25 === $ff['d2080'] && 39 === $ff['presale'] && 12 === $ff['presale_tlv'] && 392 === $ff['marketing'] && 52 === $ff['construction'] && 344 === $ff['priced'], 'faq facts ' . json_encode( $ff ) );
$qs = array_column( $faq, 0 ); ok( count( $qs ) === count( array_unique( $qs ) ), 'no question twice' );
$relq = implode( ' | ', array_column( $rel, 0 ) ) . ' ' . implode( ' ', array_column( $rel, 1 ) );
foreach ( array( 'דירות חדשות עד 1.5 מיליון', 'עד 1.2 מיליון', 'מבצעי קבלנים', '20/80', 'הלוואת קבלן', 'פרויקטים חדשים בשיווק', 'פרויקטים בבנייה', 'פרויקטים חדשים על הנייר', 'פרויקטים חדשים במרכז', 'ברמת אביב', 'בית פרטי חדש מקבלן', 'דירות חדשות למכירה', 'פריסייל' ) as $ph ) { ok( false !== mb_strpos( $relq, $ph ), "related phrase missing: $ph" ); }
foreach ( $rel as $qa ) { ok( mb_strlen( $qa[1] ) <= 330 && ! preg_match( '~[–—]|  ~u', $qa[0] . $qa[1] ) && ( empty( $qa[2] ) || ! empty( $qa[3] ) ), 'short answer, no long dash: ' . $qa[0] . ' (' . mb_strlen( $qa[1] ) . ')' ); }
ok( 1 === substr_count( $top, '<option value="1200000">עד 1.2 מיליון ₪</option><option value="1500000">עד 1.5 מיליון ₪</option>' ), 'the table price filter carries 1.2 and 1.5' );
ok( 35 === substr_count( nadlan_ph_faq_html(), '<details>' ), 'faq html: 35 questions' );
if ( getenv( 'PRINTFAQ' ) ) { foreach ( $rel as $qa ) { echo "Q: {$qa[0]}\nA: {$qa[1]}" . ( ! empty( $qa[2] ) ? "\n   -> {$qa[2]} | {$qa[3]}" : '' ) . "\n\n"; } }

if ( ! empty( $argv[1] ) ) { file_put_contents( $argv[1], '<!doctype html><html lang="he" dir="rtl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500;600&family=IBM+Plex+Sans+Hebrew:wght@400;500;600;700&display=swap"><body style="margin:0;background:#F4F6FA">' . $a . $top . '</body></html>' ); }
echo ( $bad ? "FAILED $bad" : 'all passed' ), ' | section ', strlen( $h ), " bytes\n";
exit( $bad ? 1 : 0 );
