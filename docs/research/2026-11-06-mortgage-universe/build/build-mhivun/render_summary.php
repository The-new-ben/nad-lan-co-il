<?php
/*
 * HAD-675: render the mhivun server summary of registry.php.txt against the real data files, outside WordPress.
 * Stubs: esc_html, and copies of the three helpers that already live in plugins/nadlan-config/inc/instruments.php
 * (nadlan_nli_mrates reading the plugin data folder, nadlan_nli_mr_nom, nadlan_nli_mr_pmt; same bodies, 1.72.588).
 * Run: php docs/research/2026-11-06-mortgage-universe/build/build-mhivun/render_summary.php   (test_mhivun.js runs it too)
 */
$repo = dirname( __DIR__, 5 );
function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function nadlan_nli_mrates() {
	static $x = null;
	if ( null !== $x ) { return $x; }
	$dir = dirname( __DIR__, 5 ) . '/plugins/nadlan-config/assets/instruments/data/';
	$j = function ( $f ) use ( $dir ) { return is_readable( $dir . $f ) ? json_decode( (string) file_get_contents( $dir . $f ), true ) : null; };
	$x = array( 'd' => $j( 'boi-mortgage.json' ), 'rt' => $j( 'boi-rate.json' ), 'cpi' => $j( 'cbs-120010.json' ), 'sys' => null );
	if ( is_array( $x['d'] ) && ! empty( $x['d']['by_bank']['latest']['table'] ) ) {
		foreach ( $x['d']['by_bank']['latest']['table'] as $row ) { if ( 'system' === $row['bank'] ) { $x['sys'] = $row; } }
	}
	return $x;
}
function nadlan_nli_mr_nom( $e ) { return 1200 * ( pow( 1 + $e / 100, 1 / 12 ) - 1 ); }
function nadlan_nli_mr_pmt( $b, $rm, $n ) { return $rm == 0 ? $b / $n : $b * $rm / ( 1 - pow( 1 + $rm, -$n ) ); }

require __DIR__ . '/registry.php.txt';
$out = nadlan_mhivun_registry_snippet( 'mhivun' );
if ( ! is_string( $out ) || '' === $out ) { fwrite( STDERR, "empty summary\n" ); exit( 1 ); }
echo $out, "\n";
