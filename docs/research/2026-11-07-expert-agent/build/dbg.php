<?php
// prints the provider's raw replies of one failing turn (no key printed)
require __DIR__ . '/wp_stubs.php';
$PLUG = dirname( __DIR__, 4 ) . '/plugins/nadlan-config';
$key = trim( strtok( trim( (string) @file_get_contents( 'C:/Users/777/Documents/jus-tice-secrets/openrouter/hadmaia-openrouter-key.txt' ) ), "\r\n" ) );
update_option( 'nadlan_advisor_or_key', $key );
$pages = json_decode( file_get_contents( __DIR__ . '/pages.json' ), true );
foreach ( $pages as $id => $p ) { $GLOBALS['POSTS'][ (int) $id ] = (object) array( 'ID' => (int) $id, 'post_type' => $p['type'], 'post_title' => $p['title'], 'url' => $p['url'], 'post_content' => $p['content'], 'post_excerpt' => '', 'meta' => array() ); }
require $PLUG . '/inc/expert-advisor.php';
function nadlan_dbg_call( $payload ) { return nadlan_adv_call( $payload ); }
$msgs = array( array( 'role' => 'user', 'content' => 'יש לי 700 אלף. כמה יהיה ההחזר החודשי על משכנתא של 1.8 מיליון ל-25 שנה?' ) );
$r = nadlan_adv_answer( 9, $msgs, 'he' );
echo is_wp_error( $r ) ? 'ERR ' . $r->get_error_code() : 'OK ' . mb_substr( $r['answer'], 0, 200 ), "\n";
foreach ( $GLOBALS['CALLS'] as $i => $c ) { echo "call $i http {$c['code']} msgs " . count( $c['req']['messages'] ) . ' tool_choice ' . ( $c['req']['tool_choice'] ?? '-' ) . "\n"; }
foreach ( $GLOBALS['CALLS'] as $i => $c ) { $j = json_decode( $c['resp'], true ); $m = $j['choices'][0]['message'] ?? array(); echo "resp $i finish=" . ( $j['choices'][0]['finish_reason'] ?? '?' ) . ' content=' . json_encode( mb_substr( (string) ( $m['content'] ?? '' ), 0, 300 ), JSON_UNESCAPED_UNICODE ) . ' tools=' . json_encode( array_map( function ( $t ) { return $t['function']['name'] . ' ' . $t['function']['arguments']; }, $m['tool_calls'] ?? array() ), JSON_UNESCAPED_UNICODE ) . ' usage=' . json_encode( $j['usage'] ?? null ) . "\n"; }
