<?php
/* Runs the two NOT-APPLIED summary branches of summaries.php on the real data files, outside WordPress.
   php docs/research/2026-10-26-upgrades/g2g3-urban-renewal/snippets/test_summaries.php */
function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
$repo = dirname( __DIR__, 5 );
$src = file_get_contents( __DIR__ . '/summaries.php' );
$src = preg_replace( '/^<\?php/', '', $src );
$src = str_replace( "dirname( __DIR__ ) . '/assets/instruments/data/", "'" . str_replace( '\\', '/', $repo ) . "/plugins/nadlan-config/assets/instruments/data/", $src );
eval( 'function nadlan_nli_summary_t( $id ) { ' . $src . ' return ""; }' );
$bad = 0;
foreach ( array( 'pinui', 'urcity' ) as $id ) {
	$h = nadlan_nli_summary_t( $id );
	$ok = strlen( $h ) > 400 && substr_count( $h, '<table>' ) === 1 && ! preg_match( '/[\x{2013}\x{2014}]/u', $h );
	if ( ! $ok ) { $bad++; }
	echo ( $ok ? 'OK   ' : 'BAD  ' ) . $id . ': ' . strlen( $h ) . " bytes, " . substr_count( $h, '<tr>' ) . " rows\n";
}
$p = nadlan_nli_summary_t( 'pinui' );
foreach ( array( '<td>16</td><td>10</td><td>11</td><td>7</td>', '<td>48</td><td>29</td><td>32</td><td>20</td>', '186 תכניות', '4.0 שנים' ) as $want ) {
	$ok = false !== strpos( $p, $want ); if ( ! $ok ) { $bad++; } echo ( $ok ? 'OK   ' : 'BAD  ' ) . 'pinui has ' . $want . "\n";
}
$u = nadlan_nli_summary_t( 'urcity' );
foreach ( array( '993 מתחמים ב-79 ערים', '<td>ירושלים</td><td>215</td>', 'בלי הארכה לתמ&quot;א 38' ) as $want ) {
	$ok = false !== strpos( $u, $want ); if ( ! $ok ) { $bad++; } echo ( $ok ? 'OK   ' : 'BAD  ' ) . 'urcity has ' . $want . "\n";
}
echo $bad ? "FAIL\n" : "PASS\n";
exit( $bad ? 1 : 0 );
