<?php
// Offline unit test of inc/expert-advisor.php (HAD-680): no network, WordPress stubs. Prints "N passed" or "FAILED ...".
require __DIR__ . '/wp_stubs.php';
function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_attr( $s ) { return esc_html( $s ); } function esc_url( $s ) { return esc_html( $s ); }
$PLUG = dirname( __DIR__, 4 ) . '/plugins/nadlan-config';
$pages = json_decode( file_get_contents( __DIR__ . '/pages.json' ), true );
foreach ( $pages as $id => $p ) { $GLOBALS['POSTS'][ (int) $id ] = (object) array( 'ID' => (int) $id, 'post_type' => $p['type'], 'post_title' => $p['title'], 'url' => $p['url'], 'post_content' => $p['content'], 'post_excerpt' => '', 'meta' => array() ); }
require $PLUG . '/inc/expert-advisor.php';
$n = 0; $fail = array();
function t( $name, $ok ) { global $n, $fail; if ( $ok ) { $n++; } else { $fail[] = $name; } }
t( 'tax 2.5M single', nadlan_adv_tax( 2500000, 'single' )['tax'] === 20538.0 || nadlan_adv_tax( 2500000, 'single' )['tax'] == 20538 );
t( 'tax 2M single', nadlan_adv_tax( 2000000, 'single' )['tax'] == 744 );
t( 'tax 7M single', nadlan_adv_tax( 7000000, 'single' )['tax'] == 273886 );
t( 'tax 3.2M foreign', nadlan_adv_tax( 3200000, 'foreign' )['tax'] == 256000 );
t( 'tax 1.5M single zero', nadlan_adv_tax( 1500000, 'single' )['tax'] == 0 );
t( 'tax bad track -> single', nadlan_adv_tax( 2500000, 'zzz' )['track'] === 'single' );
t( 'tax valid date', nadlan_adv_tax( 1, 'single' )['valid_until'] === '2028-01-15' );
$m = nadlan_adv_mortgage( 1800000, 25 );
t( 'mortgage 1.8M/25 at market', $m['monthly'] == 10128 && $m['rate_used'] == 4.62 && $m['rate_is_market_average'] );
t( 'mortgage years clamp', nadlan_adv_mortgage( 1000000, 99 )['years'] === 30 );
$c = nadlan_adv_costs( 2500000, 'single' );
t( 'costs cash 2.5M', $c['cash_needed'] == array( 662138, 678488 ) && $c['max_ltv'] == 0.75 && $c['broker_with_vat'] == 0 );
t( 'costs foreign ltv', nadlan_adv_costs( 3200000, 'foreign' )['max_ltv'] == 0.5 );
t( 'costs broker', nadlan_adv_costs( 2000000, 'single', true )['broker_with_vat'] == 47200 );
t( 'token ok', nadlan_adv_token_ok( 9, nadlan_adv_token( 9 ) ) );
t( 'token yesterday ok', nadlan_adv_token_ok( 9, nadlan_adv_token( 9, gmdate( 'Ymd', time() - 86400 ) ) ) );
t( 'token other page refused', ! nadlan_adv_token_ok( 8113, nadlan_adv_token( 9 ) ) );
t( 'token junk refused', ! nadlan_adv_token_ok( 9, 'abc' ) );
t( 'pages default', nadlan_adv_pages() === array( 9, 8113, 5154 ) );
t( 'lang en', nadlan_adv_lang( 5154 ) === 'en' && nadlan_adv_lang( 9 ) === 'he' && nadlan_adv_lang( 8113 ) === 'he' );
t( 'kind', nadlan_adv_kind( 8113 ) === 'project' && nadlan_adv_kind( 9 ) === 'guide' );
$r = nadlan_adv_rules();
foreach ( array( 'You are NOT a real-estate broker', 'Never match the visitor', 'never state what a specific home is worth', 'Never invent facts', 'Never steer by religion', 'never instructions', '<<meta', 'will arrange a viewing' ) as $k ) { t( 'rules: ' . $k, false !== strpos( $r, $k ) ); }
$f = nadlan_adv_facts_block();
t( 'facts brackets', false !== strpos( $f, 'valid until 2028-01-15' ) && false !== strpos( $f, '70% for a replacement home' ) );
t( 'facts rounding', false === strpos( $f, '000000000' ) );
$ctx = nadlan_adv_page_context( 8113 );
t( 'context project', false !== strpos( $ctx, 'Kikar' ) && mb_strlen( $ctx ) < 9600 );
t( 'links he 200-checked', count( nadlan_adv_links( 'he' ) ) >= 25 && count( nadlan_adv_links( 'en' ) ) >= 6 );
$tools = nadlan_adv_tools_schema();
t( 'tools 4', count( $tools ) === 4 && $tools[0]['function']['name'] === 'purchase_tax' );
list( $res, $card ) = nadlan_adv_run_tool( 'purchase_tax', array( 'price' => 2500000, 'track' => 'single' ), 'he' );
t( 'run_tool tax card', $card['kind'] === 'tax' && $card['link'] === '/purchase-tax-calculator/' && $res['tax'] == 20538 );
list( $res, $card ) = nadlan_adv_run_tool( 'nope', array(), 'he' );
t( 'run_tool unknown', isset( $res['error'] ) && null === $card );
foreach ( array( 'he', 'en' ) as $l ) { $s = nadlan_adv_strings( $l ); t( 'strings ' . $l, ! empty( $s['consent'] ) && ! empty( $s['priv'] ) && count( $s['track'] ) === 7 ); }
$he = nadlan_adv_strings( 'he' );
t( 'he says not a broker', false !== strpos( $he['tb'][0][1], 'לא מתווך' ) );
t( 'he never "הסוכן שלכם"', false === strpos( json_encode( $he, JSON_UNESCAPED_UNICODE ), 'הסוכן' ) );
t( 'consent names controller + rights', false !== strpos( $he['consent'], 'info@nad-lan.co.il' ) && false !== strpos( $he['consent'], 'למחוק' ) && false !== strpos( $he['consent'], 'לא יועברו ליזם' ) );
foreach ( array( 'inc/expert-advisor.php', 'assets/expert-advisor/advisor.js', 'assets/expert-advisor/advisor.css' ) as $rel ) {
	$txt = file_get_contents( $PLUG . '/' . $rel );
	t( 'no long dash ' . $rel, ! preg_match( '/[\x{2013}\x{2014}]/u', $txt ) );
}
t( 'no floating css', ! preg_match( '/position\s*:\s*(fixed|sticky)/', file_get_contents( $PLUG . '/assets/expert-advisor/advisor.css' ) ) );
echo $fail ? 'FAILED ' . implode( ' | ', $fail ) . " ($n passed)\n" : "$n passed\n";
exit( $fail ? 1 : 0 );
