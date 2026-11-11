<?php
// php test-summary.php  (HAD-707). Loads inc/design-tools.php with WordPress stubs and checks the 17 no-JavaScript summaries and
// the registry filter: every tool registered with file 'design' and data design.json, every summary non-empty, carries a number,
// has no site name or URL, no blacklisted word, and its HTML is balanced. Writes summaries.html next to this file for reading.
define( 'ABSPATH', __DIR__ );
$GLOBALS['__f'] = array();
function add_filter( $h, $cb ) { $GLOBALS['__f'][ $h ][] = $cb; }
function apply_filters( $h, $v ) { foreach ( isset( $GLOBALS['__f'][ $h ] ) ? $GLOBALS['__f'][ $h ] : array() as $cb ) { $v = $cb( $v ); } return $v; }
function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
require __DIR__ . '/../../../../plugins/nadlan-config/inc/design-tools.php';

$pass = 0; $fail = 0;
function ok( $name, $cond ) { global $pass, $fail; if ( $cond ) { $pass++; } else { $fail++; } echo ( $cond ? 'ok   ' : 'FAIL ' ) . $name . "\n"; }
$tools = apply_filters( 'nadlan_nli_tools', array() );
ok( '17 tools added through the registry filter', 17 === count( $tools ) );
$out = '<!doctype html><html lang="he" dir="rtl"><meta charset="utf-8"><title>summaries</title><body style="font-family:sans-serif;max-width:760px;margin:auto">';
foreach ( $tools as $id => $t ) {
	ok( $id . ': registry entry has file design, data design.json, name, desc', 'design' === $t['file'] && array( 'design.json' ) === $t['data'] && $t['name'] && mb_strlen( $t['desc'] ) > 60 );
	$s = nadlan_dsg_summary( $id );
	$txt = trim( preg_replace( '/\s+/u', ' ', strip_tags( $s ) ) );
	ok( $id . ': summary printed with numbers', mb_strlen( $txt ) > 80 && preg_match( '/\d/', $txt ) );
	ok( $id . ': no site name, URL or blacklisted word', ! preg_match( '/https?:|www\.|\.co\.il|\.com\b|Google|גוגל|ממשק|סימולציה|תלת[ -־]?ממד|מודל|שכבה|—|אריח/u', $s . $t['name'] . $t['desc'] ) );
	$open = preg_match_all( '/<(table|tr|td|th|ol|li|p)\b/', $s ); $close = preg_match_all( '/<\/(table|tr|td|th|ol|li|p)>/', $s );
	ok( $id . ': balanced HTML', $open === $close );
	$out .= '<h2>' . esc_html( $t['name'] ) . '</h2>' . $s;
}
ok( 'unknown id gives an empty summary', '' === nadlan_dsg_summary( 'nope' ) );
file_put_contents( __DIR__ . '/summaries.html', $out . '</body></html>' );
echo "\n$pass passed, $fail failed\n";
exit( $fail ? 1 : 0 );
