<?php
/* Checks the NOT-APPLIED registry entries of registry.php against the real tool and data files, outside WordPress.
   php docs/research/2026-10-26-upgrades/g6g8-pros/snippets/test_registry.php */
require __DIR__ . '/registry.php';
$repo = str_replace( '\\', '/', dirname( __DIR__, 5 ) );
$base = $repo . '/plugins/nadlan-config/assets/instruments/';
$bad = 0;
$ok = function ( $c, $msg ) use ( &$bad ) { if ( ! $c ) { $bad++; } echo ( $c ? 'OK   ' : 'BAD  ' ) . $msg . "\n"; };
foreach ( nadlan_g6g8_registry_snippet() as $id => $t ) {
	$file = isset( $t['file'] ) ? $t['file'] : $id;
	$js = $base . 'tools/' . $file . '.js';
	$ok( is_readable( $js ), "$id: tools/$file.js exists" );
	$ok( is_readable( $js ) && false !== strpos( file_get_contents( $js ), "register('" . $id . "'" ), "$id: $file.js registers '$id'" );
	foreach ( $t['data'] as $d ) { $j = is_readable( $base . 'data/' . $d ) ? json_decode( file_get_contents( $base . 'data/' . $d ), true ) : null; $ok( is_array( $j ) && ! empty( $j['key'] ), "$id: data/$d is JSON with a key" ); }
	foreach ( array( 'name', 'cat', 'kicker', 'desc' ) as $k ) { $ok( ! empty( $t[ $k ] ) && ! preg_match( '/[\x{2013}\x{2014}]/u', $t[ $k ] ), "$id: $k set, no long dash" ); }
	$ok( ! preg_match( '/המערכת|פלטפורמ|אטלס|הדמו|עורך הדין שלנו|השמאי שלנו/u', $t['name'] . $t['desc'] ), "$id: no banned words" );
	$ok( count( $t['related'] ) >= 3, "$id: " . count( $t['related'] ) . ' related links' );
}
echo $bad ? "FAIL\n" : "PASS\n";
exit( $bad ? 1 : 0 );
