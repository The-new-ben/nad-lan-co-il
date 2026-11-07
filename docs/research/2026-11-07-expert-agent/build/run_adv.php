<?php
// php run_adv.php <page_id> "question" ["question" ...]  - runs the real module against OpenRouter (one conversation)
require __DIR__ . '/wp_stubs.php';
$PLUG = dirname( __DIR__, 4 ) . '/plugins/nadlan-config';
$key = trim( (string) @file_get_contents( 'C:/Users/777/Documents/jus-tice-secrets/openrouter/hadmaia-openrouter-key.txt' ) );
$key = trim( strtok( $key, "\r\n" ) );
update_option( 'nadlan_advisor_or_key', $key );
if ( getenv( 'ADV_MODEL' ) ) { update_option( 'nadlan_advisor_model', getenv( 'ADV_MODEL' ) ); }
$pages = json_decode( file_get_contents( __DIR__ . '/pages.json' ), true );
foreach ( $pages as $id => $p ) { $GLOBALS['POSTS'][ (int) $id ] = (object) array( 'ID' => (int) $id, 'post_type' => $p['type'], 'post_title' => $p['title'], 'url' => $p['url'], 'post_content' => $p['content'], 'post_excerpt' => '', 'meta' => array() ); }
$GLOBALS['SEARCH'] = array( 101 => 'מס שבח: מתי משלמים ומה הפטורים', 102 => 'היטל השבחה: מי משלם ומתי' );
require $PLUG . '/inc/expert-advisor.php';
$page = (int) $argv[1]; $lang = nadlan_adv_lang( $page );
$msgs = array(); $tot = array( 'in' => 0, 'out' => 0, 'cost' => 0 );
foreach ( array_slice( $argv, 2 ) as $q ) {
	$msgs[] = array( 'role' => 'user', 'content' => $q );
	$t0 = microtime( true );
	$r = nadlan_adv_answer( $page, $msgs, $lang );
	$dt = round( microtime( true ) - $t0, 1 );
	echo "\n===== Q: $q\n";
	if ( is_wp_error( $r ) ) { echo 'ERROR ' . $r->get_error_code() . ' ' . json_encode( get_option( 'nadlan_adv_last_error' ) ) . "\n"; break; }
	echo $r['answer'] . "\n";
	foreach ( $r['cards'] as $c ) { echo '[card ' . $c['kind'] . '] ' . json_encode( array_intersect_key( $c['data'], array_flip( array( 'price', 'track', 'tax', 'monthly', 'rate_used', 'cash_needed', 'loan', 'years' ) ) ), JSON_UNESCAPED_UNICODE ) . "\n"; }
	echo '[meta] stage=' . $r['stage'] . ' handoff=' . ( $r['handoff'] ? 'yes' : 'no' ) . ' next=' . json_encode( $r['next'], JSON_UNESCAPED_UNICODE ) . "\n";
	echo '[usage] in=' . $r['usage']['in'] . ' out=' . $r['usage']['out'] . ' cost=$' . $r['usage']['cost'] . " time={$dt}s\n";
	foreach ( array( 'in', 'out', 'cost' ) as $k ) { $tot[ $k ] += $r['usage'][ $k ]; }
	$msgs[] = array( 'role' => 'assistant', 'content' => $r['answer'] );
	$GLOBALS['DUMP'][] = array( 'q' => $q, 'r' => $r );
}
if ( getenv( 'ADV_DUMP' ) ) { file_put_contents( getenv( 'ADV_DUMP' ), json_encode( $GLOBALS['DUMP'] ?? array(), JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT ) ); }
echo "\n[total] in={$tot['in']} out={$tot['out']} cost=\$" . round( $tot['cost'], 4 ) . ' model=' . nadlan_adv_model() . "\n";
