<?php
/* Runs the four NOT-APPLIED summary branches of summaries.php on the real data files, outside WordPress.
   php docs/research/2026-10-26-upgrades/g6g8-pros/snippets/test_summaries.php */
function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_url( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
$repo = dirname( __DIR__, 5 );
$src = file_get_contents( __DIR__ . '/summaries.php' );
$src = preg_replace( '/^<\?php/', '', $src );
$src = str_replace( "dirname( __DIR__ ) . '/assets/instruments/data/", "'" . str_replace( '\\', '/', $repo ) . "/plugins/nadlan-config/assets/instruments/data/", $src );
eval( 'function nadlan_nli_summary_t( $id ) { ' . $src . ' return ""; }' );
$bad = 0;
foreach ( array( 'bedek' => 1, 'shamai' => 1, 'shamaireg' => 0, 'orechdin' => 1 ) as $id => $tables ) {
	$h = nadlan_nli_summary_t( $id );
	$ok = strlen( $h ) > 300 && substr_count( $h, '<table>' ) === $tables && ! preg_match( '/[\x{2013}\x{2014}]/u', $h ) && ! preg_match( '/(?<![\d.,])0 ₪/u', $h );
	if ( ! $ok ) { $bad++; }
	echo ( $ok ? 'OK   ' : 'BAD  ' ) . $id . ': ' . strlen( $h ) . " bytes, " . substr_count( $h, '<tr>' ) . " rows\n";
}
$want = array(
	'bedek' => array( '<td>7 שנים</td><td>10 שנים</td>', '<td>שנה</td><td>4 שנים</td>', '20 שנה', '1,200 עד 2,500 ₪', '1,947 עד 6,000 ₪' ),
	'shamai' => array( '3,182 שמאים', '45 ימים', '25,000 ₪', '<td>3 שנים</td>' ),
	'shamaireg' => array( '3,182 שמאים מורשים', 'datasets/ministry_of_justice/shamaim' ),
	'orechdin' => array( '5,915 ₪ (2026)', '4,642,750', '<td>1,000,000 ₪</td><td>5,000 ₪</td>', '<td>5,000,000 ₪</td><td>אין תקרה</td>', '23,322 ₪', 'הערת אזהרה 188 ₪' ),
);
foreach ( $want as $id => $list ) {
	$h = nadlan_nli_summary_t( $id );
	foreach ( $list as $w ) { $ok = false !== strpos( $h, $w ); if ( ! $ok ) { $bad++; } echo ( $ok ? 'OK   ' : 'BAD  ' ) . $id . ' has ' . $w . "\n"; }
}
echo $bad ? "FAIL\n" : "PASS\n";
exit( $bad ? 1 : 0 );
