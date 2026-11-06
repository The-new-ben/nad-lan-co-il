<?php
/* HAD-675 · renders the mkashe branch of registry.php.txt against the real data files, with WordPress stubs, into summary.out.html.
   Run from the repo root:  php docs/research/2026-11-06-mortgage-universe/build/build-mkashe/render_summary.php
   nadlan_nli_mrates() and nadlan_nli_mr_pmt() are copied from inc/instruments.php (read only) so the branch runs unchanged. */
$here   = __DIR__;
$plugin = realpath( $here . '/../../../../../plugins/nadlan-config' );
function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function nadlan_nli_mrates() {
	global $plugin; static $x = null; if ( null !== $x ) { return $x; }
	$dir = $plugin . '/assets/instruments/data/';
	$j = function ( $f ) use ( $dir ) { return is_readable( $dir . $f ) ? json_decode( (string) file_get_contents( $dir . $f ), true ) : null; };
	$x = array( 'd' => $j( 'boi-mortgage.json' ), 'rt' => null, 'cpi' => null, 'sys' => null );
	return $x;
}
function nadlan_nli_mr_pmt( $b, $rm, $n ) { return $rm == 0 ? $b / $n : $b * $rm / ( 1 - pow( 1 + $rm, -$n ) ); }
$code = (string) file_get_contents( $here . '/registry.php.txt' );
$code = str_replace( "dirname( __DIR__ ) . '/assets/instruments/data/", "'" . str_replace( '\\', '/', $plugin ) . "/assets/instruments/data/", $code );
eval( '?>' . $code );
$entries = nadlan_mkashe_registry_snippet( 'none' );
$html = nadlan_mkashe_registry_snippet( 'mkashe' );
if ( ! is_array( $entries ) || empty( $entries['mkashe']['data'] ) ) { fwrite( STDERR, "entry missing\n" ); exit( 1 ); }
if ( ! is_string( $html ) || '' === $html ) { fwrite( STDERR, "summary empty\n" ); exit( 1 ); }
file_put_contents( $here . '/summary.out.html', $html . "\n" );
$need = array( '6 חודשים', '21 ימי עסקים', 'עד 3 חודשים', 'עד 3 פעמים', '18 חודשים', '12 חודשים בלי ריבית פיגורים', '2.5 מיליון', '5,627 ₪', '5,723 ₪', 'הסתיים' );
$miss = array_filter( $need, function ( $s ) use ( $html ) { return false === strpos( $html, $s ); } );
echo 'entry: ' . $entries['mkashe']['name'] . ' · data ' . implode( ', ', $entries['mkashe']['data'] ) . "\n";
echo 'summary: ' . strlen( $html ) . ' bytes; ' . ( $miss ? 'MISSING: ' . implode( ' | ', $miss ) : 'all ' . count( $need ) . ' key numbers present' ) . "\n";
echo ( preg_match( '/[\x{2013}\x{2014}]/u', $html ) ? "LONG DASH FOUND\n" : "no long dash\n" );
exit( $miss ? 1 : 0 );
