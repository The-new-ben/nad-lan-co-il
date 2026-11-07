<?php
/*
 * nlcamp build (7.11.2026): a PHP test of plugins/nadlan-config/inc/campaign-brief.php with small WordPress stubs (no WordPress,
 * no database, no mail leaves the machine). Run from anywhere:
 *   php docs/research/2026-11-07-campaign-network/build/build-nlcamp/test_campaign_brief.php            the checks (exit 1 on a failure)
 *   php .../test_campaign_brief.php --json                   plans, markets, languages and budget as JSON (read by test_nlcamp.js)
 *   php .../test_campaign_brief.php --summary he|en          the server summary the shortcode prints (pasted into preview.html)
 */
define( 'ABSPATH', __DIR__ . '/' );
define( 'HOUR_IN_SECONDS', 3600 ); define( 'DAY_IN_SECONDS', 86400 );
$GLOBALS['T'] = array( 'opt' => array( 'admin_email' => 'owner@example.test' ), 'tr' => array(), 'posts' => array(), 'meta' => array(), 'mail' => array(), 'act' => array(), 'flt' => array(),
	'routes' => array(), 'inline' => array(), 'enq' => array(), 'dup' => 0, 'cpt' => array() );
class WP_Error { public $c; public $m; public $d; function __construct( $c = '', $m = '', $d = array() ) { $this->c = $c; $this->m = $m; $this->d = $d; } function get_error_code() { return $this->c; } function get_error_data() { return $this->d; } }
class WP_REST_Response { public $data; public $status; function __construct( $d = null, $s = 200 ) { $this->data = $d; $this->status = $s; } }
class Req { public $b; public $h; function __construct( $b, $h = array() ) { $this->b = $b; $this->h = $h; } function get_body() { return $this->b; } function get_header( $k ) { return $this->h[ $k ] ?? null; } }
function is_wp_error( $x ) { return $x instanceof WP_Error; }
function add_action( $h, $f, $p = 10 ) { $GLOBALS['T']['act'][ $h ][] = $f; }
function add_filter( $h, $f, $p = 10 ) { $GLOBALS['T']['flt'][ $h ][] = $f; }
function apply_filters( $h, $v ) { foreach ( $GLOBALS['T']['flt'][ $h ] ?? array() as $f ) { $v = $f( $v ); } return $v; }
function do_action_x( $h, ...$a ) { foreach ( $GLOBALS['T']['act'][ $h ] ?? array() as $f ) { $f( ...$a ); } }
function get_option( $k, $d = false ) { return $GLOBALS['T']['opt'][ $k ] ?? $d; }
function register_post_type( $t, $a ) { $GLOBALS['T']['cpt'][ $t ] = $a; }
function register_rest_route( $ns, $r, $a ) { $GLOBALS['T']['routes'][ $ns . $r ] = $a; }
function sanitize_key( $k ) { return preg_replace( '/[^a-z0-9_\-]/', '', strtolower( (string) $k ) ); }
function sanitize_text_field( $s ) { $s = strip_tags( (string) $s ); $s = preg_replace( '/[\r\n\t ]+/', ' ', $s ); return trim( $s ); }
function sanitize_textarea_field( $s ) { return trim( strip_tags( (string) $s ) ); }
function sanitize_email( $s ) { $s = trim( (string) $s ); return filter_var( $s, FILTER_VALIDATE_EMAIL ) ? $s : ''; }
function is_email( $s ) { return (bool) filter_var( $s, FILTER_VALIDATE_EMAIL ); }
function wp_parse_url( $u, $c = -1 ) { return parse_url( $u, $c ); }
function home_url( $p = '' ) { return 'https://nad-lan.co.il' . $p; }
function rest_url( $p = '' ) { return 'https://nad-lan.co.il/wp-json/' . $p; }
function admin_url( $p = '' ) { return 'https://nad-lan.co.il/wp-admin/' . $p; }
function get_privacy_policy_url() { return 'https://nad-lan.co.il/privacy/'; }
function add_query_arg( $k, $v, $u ) { return $u . ( false === strpos( $u, '?' ) ? '?' : '&' ) . rawurlencode( $k ) . '=' . rawurlencode( (string) $v ); }
function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_url_raw( $s ) { return (string) $s; }
function wp_json_encode( $d, $f = 0 ) { return json_encode( $d, $f ); }
function wp_slash( $s ) { return addslashes( $s ); }
function get_transient( $k ) { return $GLOBALS['T']['tr'][ $k ] ?? false; }
function set_transient( $k, $v, $e ) { $GLOBALS['T']['tr'][ $k ] = $v; return true; }
function get_posts( $a ) { if ( $GLOBALS['T']['dup'] > 0 ) { $GLOBALS['T']['dup']--; return array( 1 ); } return array(); }
function wp_insert_post( $a, $e = false ) { $id = 100 + count( $GLOBALS['T']['posts'] ); $GLOBALS['T']['posts'][ $id ] = $a; return $id; }
function update_post_meta( $id, $k, $v ) { $GLOBALS['T']['meta'][ $id ][ $k ] = $v; return true; }
function get_post_meta( $id, $k, $s = false ) { return $GLOBALS['T']['meta'][ $id ][ $k ] ?? ''; }
function wp_mail( $to, $sub, $body ) { $GLOBALS['T']['mail'][] = array( $to, $sub, $body ); return true; }
function wp_script_is( $h, $w ) { return in_array( $h, $GLOBALS['T']['enq'], true ); }
function wp_add_inline_script( $h, $js, $pos ) { $GLOBALS['T']['inline'][] = array( $h, $js, $pos ); return true; }
function add_meta_box() {}

require dirname( __DIR__, 5 ) . '/plugins/nadlan-config/inc/campaign-brief.php';

$mode = $argv[1] ?? '';
if ( '--json' === $mode ) {
	echo json_encode( array( 'plans' => nadlan_cb_plans(), 'markets' => nadlan_cb_markets(), 'langs' => array_keys( nadlan_cb_langs() ), 'buyers' => array_keys( nadlan_cb_buyers() ),
		'channels' => array_keys( nadlan_cb_channels() ), 'budget' => nadlan_cb_budget(), 'kinds' => array_keys( nadlan_cb_kinds() ),
		'rec' => array_map( 'nadlan_cb_recommend', range( 0, 10 ) ), 'first' => nadlan_cb_first_amount(),
		'firstPay' => array_map( 'nadlan_cb_first_pay', nadlan_cb_plans() ) ), JSON_UNESCAPED_UNICODE );
	exit( 0 );
}
if ( '--summary' === $mode ) { echo nadlan_cb_summary( 'en' === ( $argv[2] ?? 'he' ) ? 'en' : 'he' ); exit( 0 ); }

$n = 0; $fails = 0;
function ok( $c, $name, $got = null ) { global $n, $fails; $n++; if ( ! $c ) { $fails++; } echo ( $c ? '  ok   ' : '  FAIL ' ) . $name . ( null === $got ? '' : '  [' . ( is_string( $got ) ? $got : json_encode( $got, JSON_UNESCAPED_UNICODE ) ) . ']' ) . "\n"; }
$ip = 0;
function call( $p, $h = array( 'origin' => 'https://nad-lan.co.il' ), $raw = null ) {
	global $ip; $ip++; $_SERVER['REMOTE_ADDR'] = '10.0.0.' . $ip;  // a fresh visitor for every call unless the test says otherwise
	$f = $GLOBALS['T']['routes']['nadlan/v1/campaign-brief']['callback'];
	return $f( new Req( null === $raw ? json_encode( $p, JSON_UNESCAPED_UNICODE ) : $raw, $h ) );
}
function good( $ch = array() ) {
	return array_merge( array( 'v' => 1, 'lang' => 'he', 'markets' => array( 'fr', 'ca' ), 'buyer' => 'invest', 'budget' => 25000, 'shares' => array( 50, 25, 20, 5 ), 'kind' => 'existing',
		'project' => 'מגדלי הים, בת ים', 'plan' => 'three', 'name' => 'דנה לוי', 'company' => 'לוי יזמות', 'phone' => '050-123 4567', 'email' => 'dana@example.test', 'consent' => true,
		'consent_text' => 'אנחנו מאשרים', 'hp' => '', 't' => 42000, 'page' => '/international-campaigns/' ), $ch );
}
function field_of( $r ) { return $r instanceof WP_Error ? ( $r->d['field'] ?? $r->c ) : 'ok'; }
function status_of( $r ) { return $r instanceof WP_Error ? (int) ( $r->d['status'] ?? 0 ) : (int) $r->status; }
$DASH = '/[' . "\u{2013}\u{2014}" . ']/u';

echo "1. hooks\n";
do_action_x( 'init' ); do_action_x( 'rest_api_init' );
$cpt = $GLOBALS['T']['cpt']['nadlan_camp_brief'] ?? null;
ok( $cpt && false === $cpt['public'] && false === $cpt['publicly_queryable'] && false === $cpt['show_in_rest'] && false === $cpt['rewrite'] && true === $cpt['exclude_from_search'], 'the brief type is private: not public, not queryable, not in REST, no URL, not in search' );
$rt = $GLOBALS['T']['routes']['nadlan/v1/campaign-brief'] ?? null;
ok( $rt && 'POST' === $rt['methods'] && 'nadlan_cb_rest' === $rt['callback'], 'POST /wp-json/nadlan/v1/campaign-brief is registered (POST only)' );

echo "\n2. a good brief\n";
$r = call( good() );
ok( 201 === status_of( $r ) && true === $r->data['ok'] && preg_match( '/^NLC-\d{6}-[A-F0-9]{4}$/', $r->data['ref'] ), '201 with ok and a reference id NLC-yymmdd-XXXX', $r->data ?? field_of( $r ) );
ok( 'three' === $r->data['plan'] && 72000 === $r->data['price'], 'the answer names the plan and its price (72,000)' );
$id = array_key_last( $GLOBALS['T']['posts'] ); $post = $GLOBALS['T']['posts'][ $id ]; $meta = $GLOBALS['T']['meta'][ $id ];
ok( 'nadlan_camp_brief' === $post['post_type'] && 'private' === $post['post_status'] && false !== strpos( $post['post_title'], $r->data['ref'] ), 'saved as a private nadlan_camp_brief, the reference in the title', $post['post_title'] );
$b = json_decode( stripslashes( $meta['_nlc_brief'] ), true );
ok( $meta['_nlc_ref'] === $r->data['ref'] && 'new' === $meta['_nlc_status'] && ! empty( $meta['_nlc_consent_at'] ), 'meta: reference, status new, consent time' );
ok( array( 'fr', 'ca' ) === $b['markets'] && array( 'en', 'fr' ) === $b['langs'] && 300000 === $b['yearly'] && 72000 === $b['price'] && 'three' === $b['recommended'], 'computed on the server: languages en+fr, yearly 300,000, price 72,000, recommended three', $b['langs'] );
ok( array( 'meta' => 50, 'google' => 25, 'press' => 20, 'boards' => 5 ) === $b['shares'] && '0501234567' === $b['phone'], 'the split by channel; the phone without spaces and hyphens', $b['phone'] );
$m = end( $GLOBALS['T']['mail'] );
ok( 'owner@example.test' === $m[0] && false !== strpos( $m[1], $r->data['ref'] ) && false !== strpos( $m[1], 'לוי יזמות' ), 'mailed to the site admin, the reference and company in the subject', $m[1] );
ok( false !== strpos( $m[2], 'שווקים וקהילות: צרפת, קנדה' ) && false !== strpos( $m[2], '25,000 ₪ בחודש, 300,000 ₪ בשנה' ) && false !== strpos( $m[2], 'שלושה שווקים, 72,000 ₪ לשנה' ) && false !== strpos( $m[2], 'הלקוח קיבל כפתור לתשלום ראשון של 18,000 ₪ (מוצר 8823). את היתרה, 54,000 ₪, לשלוח לו בקישורים של עד 18,000 ₪' ) && false !== strpos( $m[2], 'post.php?post=' . $id ), 'the mail: markets, budget, plan, the first payment (product 8823) and the rest of 54,000 to send in links, the admin link' );
ok( ! preg_match( $DASH, $m[2] . $post['post_content'] ) && false === strpos( $m[2], 'מע' ) && false === strpos( $m[2], 'VAT' ), 'no long dash and no VAT wording in the saved text and the mail' );
$r = call( good( array( 'plan' => 'flag', 'markets' => array( 'ca', 'fr', 'fr', 'zz', '<x>' ), 'price' => 1, 'yearly' => 1, 'langs' => array( 'xx' ) ) ) );
$b = json_decode( stripslashes( end( $GLOBALS['T']['meta'] )['_nlc_brief'] ), true );
ok( 201 === status_of( $r ) && array( 'fr', 'ca' ) === $b['markets'] && 144000 === $b['price'] && array( 'en', 'fr' ) === $b['langs'] && 'three' === $b['recommended'], 'unknown and repeated markets dropped, the fixed order kept; price, yearly and languages from the browser ignored', $b['markets'] );
ok( false !== strpos( end( $GLOBALS['T']['mail'] )[2], '(המומלצת לפי מספר השווקים: שלושה שווקים)' ), 'a plan other than the recommended one is said in the mail' );
$r = call( good( array( 'name' => '<b>דנה</b> <script>x</script>לוי', 'project' => "<a href='x'>פרויקט</a>\nשני", 'kind' => 'new' ) ) );
$b = json_decode( stripslashes( end( $GLOBALS['T']['meta'] )['_nlc_brief'] ), true );
ok( 201 === status_of( $r ) && false === strpos( $b['name'] . $b['project'], '<' ) && 'new' === $b['kind'], 'tags stripped from the text fields', $b['name'] . ' | ' . $b['project'] );
$r = call( good( array( 'kind' => 'new', 'project' => '' ) ) );
ok( 201 === status_of( $r ), 'a new project may come without a name' );
$r = call( good( array( 'lang' => 'en', 'markets' => array( 'us', 'uk', 'au', 'za', 'olim' ), 'plan' => 'flag' ) ) );
$b = json_decode( stripslashes( end( $GLOBALS['T']['meta'] )['_nlc_brief'] ), true );
ok( 201 === status_of( $r ) && 'en' === $b['lang'] && array( 'en', 'fr', 'ru' ) === $b['langs'] && 'flag' === $b['recommended'], 'an English brief, five markets: the languages en, fr, ru; recommended flagship' );

echo "\n3. refused\n";
foreach ( array(
	array( 'markets', array( 'markets' => array() ) ), array( 'markets', array( 'markets' => array( 'zz', 'il' ) ) ), array( 'buyer', array( 'buyer' => 'tourists' ) ),
	array( 'budget', array( 'budget' => 2000 ) ), array( 'budget', array( 'budget' => 61000 ) ), array( 'budget', array( 'budget' => 25500 ) ), array( 'budget', array( 'budget' => 'abc' ) ), array( 'budget', array( 'budget' => 25000.5 ) ),
	array( 'split', array( 'shares' => array( 50, 25, 20 ) ) ), array( 'split', array( 'shares' => array( 55, 25, 15, 0 ) ) ), array( 'split', array( 'shares' => array( 52, 28, 15, 5 ) ) ), array( 'split', array( 'shares' => array( 105, -5, 0, 0 ) ) ),
	array( 'kind', array( 'kind' => 'land' ) ), array( 'ref', array( 'kind' => 'existing', 'project' => ' ' ) ),
	array( 'plan', array( 'plan' => 'gold' ) ), array( 'plan', array( 'plan' => 'one' ) ), array( 'plan', array( 'plan' => 'three', 'markets' => array( 'fr', 'us', 'uk', 'ca' ) ) ),
	array( 'name', array( 'name' => 'ד' ) ), array( 'company', array( 'company' => '' ) ), array( 'phone', array( 'phone' => '1234' ) ), array( 'phone', array( 'phone' => '050-123-4567 ext 9' ) ),
	array( 'email', array( 'email' => 'dana@' ) ), array( 'consent', array( 'consent' => false ) ), array( 'consent', array( 'consent' => 'true' ) ),
) as $c ) {
	$r = call( good( $c[1] ) );
	ok( 400 === status_of( $r ) && field_of( $r ) === $c[0], 'refused, field ' . $c[0] . ': ' . json_encode( $c[1], JSON_UNESCAPED_UNICODE ), field_of( $r ) );
}
$before = count( $GLOBALS['T']['posts'] );
$r = call( good( array( 'hp' => 'http://spam' ) ) ); ok( 400 === status_of( $r ) && 'nlc_spam' === $r->c, 'the honeypot filled: refused' );
$r = call( good( array( 't' => 900 ) ) ); ok( 400 === status_of( $r ) && 'nlc_spam' === $r->c, 'filled in under 2 seconds: refused' );
$r = call( good(), array( 'origin' => 'https://evil.example' ) ); ok( 403 === status_of( $r ), 'another site (Origin evil.example): 403' );
$r = call( good(), array( 'origin' => 'null' ) ); ok( 403 === status_of( $r ), 'Origin "null": 403' );
$r = call( good(), array( 'origin' => 'https://www.nad-lan.co.il' ) ); ok( 201 === status_of( $r ), 'www.nad-lan.co.il: accepted' );
$r = call( good(), array() ); ok( 201 === status_of( $r ), 'no Origin header (old browser or server): accepted, still limited' );
$r = call( null, array( 'origin' => 'https://nad-lan.co.il' ), str_repeat( 'x', 9000 ) ); ok( 413 === status_of( $r ), 'a body over 8 KB: 413' );
$r = call( null, array( 'origin' => 'https://nad-lan.co.il' ), '{bad json' ); ok( 400 === status_of( $r ), 'not JSON: 400' );
ok( count( $GLOBALS['T']['posts'] ) === $before + 2, 'nothing refused was saved (only the two accepted ones)', count( $GLOBALS['T']['posts'] ) - $before );

echo "\n4. limits and the reference\n";
$f = $GLOBALS['T']['routes']['nadlan/v1/campaign-brief']['callback']; $_SERVER['REMOTE_ADDR'] = '10.9.9.9'; $codes = array();
for ( $i = 0; $i < 6; $i++ ) { $codes[] = status_of( $f( new Req( json_encode( good() ), array( 'origin' => 'https://nad-lan.co.il' ) ) ) ); }
ok( array( 201, 201, 201, 201, 201, 429 ) === $codes, 'one visitor: 5 briefs an hour, the 6th gets 429', $codes );
$GLOBALS['T']['tr'][ 'nadlan_cb_rl_' . md5( 'day|' . gmdate( 'Ymd' ) ) ] = 60;
$r = call( good() ); ok( 429 === status_of( $r ), 'the site: 60 briefs a day, then 429' );
$GLOBALS['T']['tr'] = array();
$GLOBALS['T']['dup'] = 2; $ref = nadlan_cb_new_ref();
ok( preg_match( '/^NLC-\d{6}-[A-F0-9]{4,6}$/', $ref ) && 0 === $GLOBALS['T']['dup'], 'a reference that exists already is drawn again', $ref );

echo "\n5. the page config and the health line\n";
$GLOBALS['T']['inline'] = array(); do_action_x( 'wp_enqueue_scripts' );
ok( ! $GLOBALS['T']['inline'], 'no config on a page without the tool' );
$GLOBALS['T']['enq'] = array( 'nadlan-nli-nlcamp' ); do_action_x( 'wp_enqueue_scripts' );
$in = $GLOBALS['T']['inline'][0] ?? array( '', '', '' ); $cfg = json_decode( preg_replace( '/^window\.NLCAMP_CONFIG=|;$/', '', $in[1] ), true );
$CO = 'https://nad-lan.co.il/checkout/?add-to-cart=';
$fp = function ( $c ) { return array( $c['plans']['one']['firstPay'], $c['plans']['three']['firstPay'], $c['plans']['flag']['firstPay'] ); };
$pu = function ( $c ) { return array( $c['plans']['one']['productUrl'], $c['plans']['three']['productUrl'], $c['plans']['flag']['productUrl'] ); };
$cf = function () { $GLOBALS['T']['inline'] = array(); do_action_x( 'wp_enqueue_scripts' ); return json_decode( preg_replace( '/^window\.NLCAMP_CONFIG=|;$/', '', $GLOBALS['T']['inline'][0][1] ), true ); };
ok( 'nadlan-nli-nlcamp' === $in[0] && 'before' === $in[2] && 'https://nad-lan.co.il/wp-json/nadlan/v1/campaign-brief' === $cfg['endpoint'] && 'https://nad-lan.co.il/privacy/' === $cfg['privacy'], 'window.NLCAMP_CONFIG before nlcamp.js: the REST address and the privacy page', $in[1] );
ok( array( $CO . '8822', $CO . '8823', $CO . '8824' ) === $pu( $cfg ) && array( 18000, 18000, 18000 ) === $fp( $cfg ), 'options unset (the release as is): the first-payment products 8822 / 8823 / 8824 and firstPay 18,000 on every plan', $pu( $cfg ) );
$GLOBALS['T']['opt']['nadlan_cb_first_amount'] = 0; $GLOBALS['T']['opt']['nadlan_cb_product_one'] = 8809; $GLOBALS['T']['opt']['nadlan_cb_product_three'] = '8810'; $GLOBALS['T']['opt']['nadlan_cb_product_flag'] = 8811;
$c2 = $cf();
ok( array( $CO . '8809', $CO . '8810', $CO . '8811' ) === $pu( $c2 ) && array( null, null, null ) === $fp( $c2 ), 'once Morning raises the cap (first amount 0, products 8809 / 8810 / 8811): the full plans, no firstPay', $pu( $c2 ) );
$r = call( good() ); ok( false !== strpos( end( $GLOBALS['T']['mail'] )[2], 'הלקוח קיבל כפתור לתשלום המלא (מוצר 8810).' ), 'then the mail says the developer got the full payment button (product 8810)' );
$GLOBALS['T']['opt']['nadlan_cb_first_amount'] = 40000; $GLOBALS['T']['opt']['nadlan_cb_product_one'] = 0;
$c3 = $cf();
ok( null === $c3['plans']['one']['productUrl'] && array( null, 40000, 40000 ) === $fp( $c3 ), 'a product option set to 0: no link; a first amount not below the price (40,000 on 36,000): no firstPay on that plan', $fp( $c3 ) );
$r = call( good( array( 'plan' => 'one', 'markets' => array( 'fr' ) ) ) ); ok( false !== strpos( end( $GLOBALS['T']['mail'] )[2], 'לשלוח ללקוח קישור לתשלום עוד היום' ), 'no product: the mail says to send a payment link today' );
$GLOBALS['T']['opt']['nadlan_cb_first_amount'] = ''; $c4 = $cf(); ok( 18000 === $c4['plans']['three']['firstPay'], 'an empty first-amount option reads as the default 18,000' );
foreach ( array( 'nadlan_cb_first_amount', 'nadlan_cb_product_one', 'nadlan_cb_product_three', 'nadlan_cb_product_flag' ) as $o ) { unset( $GLOBALS['T']['opt'][ $o ] ); }
$h = apply_filters( 'nadlan_config_healthcheck', array() );
ok( '1.1.0' === $h['campaign_brief']['version'] && array( 'one' => 8822, 'three' => 8823, 'flag' => 8824 ) === $h['campaign_brief']['products'] && 18000 === $h['campaign_brief']['first_amount'], '/health shows the version, the three product ids and the first amount', $h['campaign_brief'] );
$bad = array( 'מע״מ', 'מע"מ', 'VAT' ); $mails = implode( "\n", array_column( $GLOBALS['T']['mail'], 2 ) );
ok( ! preg_match( $DASH, $mails ) && ! array_filter( $bad, function ( $w ) use ( $mails ) { return false !== strpos( $mails, $w ); } ), 'no long dash and no VAT wording in any mail' );

echo "\n6. the server summary\n";
$he = nadlan_cb_summary( 'he' ); $en = nadlan_cb_summary( 'en' );
ok( false !== strpos( $he, 'שוק אחד <bdi>36,000</bdi> ₪ לשנה' ) && false !== strpos( $he, 'שלושה שווקים <bdi>72,000</bdi> ₪ לשנה' ) && false !== strpos( $he, 'פרויקט דגל <bdi>144,000</bdi> ₪ לשנה' ), 'Hebrew: the three plans with their yearly prices' );
ok( 10 === count( array_filter( nadlan_cb_markets(), function ( $m ) use ( $he ) { return false !== strpos( $he, $m['he'] ); } ) ) && false !== strpos( $he, 'אנגלית, צרפתית, רוסית' ) && false !== strpos( $he, 'מכוון לפי מדינה, עיר ושפה' ) && false !== strpos( $he, 'בוואטסאפ' ), 'Hebrew: all 10 markets, the languages, the targeting line, the WhatsApp lead line' );
ok( false !== strpos( $en, 'One market ₪<bdi>36,000</bdi> a year' ) && false !== strpos( $en, 'Flagship ₪<bdi>144,000</bdi> a year' ) && false !== strpos( $en, 'aimed by country, city and language' ), 'English: the plans a year, the targeting line' );
$bad = array( 'מע״מ', 'מע"מ', 'VAT', 'ממשק', 'מערכת', 'פלטפורמ', 'אלגוריתם', 'דמו', 'סימולציה', 'interface', 'platform', 'system', 'algorithm', 'demo', 'simulation', 'יהוד', 'Jewish' );
ok( ! preg_match( $DASH, $he . $en ) && ! array_filter( $bad, function ( $w ) use ( $he, $en ) { return false !== stripos( $he . $en, $w ); } ) && ! preg_match( '/\bAI\b/', $he . $en ), 'no long dash, no VAT wording, no tech word, no religion targeting word, in either language' );

echo "\n" . ( $n - $fails ) . " of $n passed" . ( $fails ? ", $fails FAILED" : '' ) . "\n";
exit( $fails ? 1 : 0 );
