<?php
// Offline check of inc/placements.php: which page lines match, and where the card lands in the real page content.
define( 'ABSPATH', __DIR__ . '/' );
function add_action() {}
function add_filter() {}
function wp_strip_all_tags( $s ) { return trim( strip_tags( preg_replace( '#<(script|style)[^>]*?>.*?</\1>#si', '', $s ) ) ); }
require $argv[1];
$paths = file_get_contents( __DIR__ . "/paths.txt" );
$default = 'מחיר';
foreach ( array( '/property-value/', '/property-value/building-rights-check/', '/north-tel-aviv/', '/north-tel-aviv/old-north/', '/north-tel-aviv-x/', '/new-projects/north-tel-aviv-new-projects/', '/ramat-aviv/', '/ramat-aviv/einstein/', '/herzliya-pituach-luxury/', '/brokers/' ) as $u ) {
	$m = nadlan_pl_match( $paths, $u );
	echo str_pad( $u, 48 ) . ' => ' . ( false === $m ? 'no' : ( '' === $m ? '(default)' : $m ) ) . "\n";
}
echo "\n";
$pages = json_decode( file_get_contents( $argv[2] ), true );
foreach ( $pages as $p ) {
	$here = parse_url( $p['link'], PHP_URL_PATH );
	$pos  = nadlan_pl_match( $paths, $here );
	if ( false === $pos ) { echo "NO MATCH $here\n"; continue; }
	$pos  = '' === $pos ? $default : $pos;
	$out  = nadlan_pl_insert( $p['content'], '<!--CARD-->', $pos );
	$at   = strpos( $out, '<!--CARD-->' );
	$before = $after = '';
	if ( preg_match_all( '/<h2\b[^>]*>(.*?)<\/h2>/is', substr( $out, 0, $at ), $b ) ) { $before = trim( wp_strip_all_tags( end( $b[1] ) ) ); }
	if ( preg_match( '/<h2\b[^>]*>(.*?)<\/h2>/is', substr( $out, $at ), $a ) ) { $after = trim( wp_strip_all_tags( $a[1] ) ); }
	$share = round( 100 * $at / max( 1, strlen( $out ) ) );
	echo "$here [$pos] at $share%\n    after:  " . mb_substr( html_entity_decode( $before ), 0, 70 ) . "\n    before: " . mb_substr( html_entity_decode( $after ), 0, 70 ) . "\n";
}
