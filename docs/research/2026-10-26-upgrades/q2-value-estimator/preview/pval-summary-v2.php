<?php
/**
 * OPTIONAL (not applied): a v2 body for the 'pval' branch of nadlan_nli_summary() in plugins/nadlan-config/inc/instruments.php
 * (Q2, 26.10.2026). The plain summary printed before the script runs, for readers without JS, search engines and AI answers.
 * Part 1 is today's branch unchanged (the city table; Yavne appears in it by itself once value.json carries it).
 * Part 2 is new: the CBS dwelling price index of the latest month, the three checks in one sentence and the worked example
 * (dna.md V10), every number computed from the data files, nothing typed in.
 *
 * To apply: inside `if ( 'pval' === $id ) { ... }` replace the body with `return nadlan_nli_pval_summary_v2( dirname( __DIR__ ) . '/assets/instruments/data' );`
 * and add this function above nadlan_nli_summary(). Check: php preview/pval-summary-v2.php (prints the summary from the repo data).
 */
if ( ! function_exists( 'nadlan_nli_pval_summary_v2' ) ) {
	function nadlan_nli_pval_summary_v2( $dir ) {
		$read = function ( $f ) use ( $dir ) { $p = $dir . '/' . $f; return is_readable( $p ) ? json_decode( (string) file_get_contents( $p ), true ) : null; };
		$x = $read( 'value.json' );
		if ( ! is_array( $x ) || empty( $x['cities'] ) ) { return ''; }
		$rows = '';
		foreach ( $x['cities'] as $name => $c ) { $rows .= '<tr><td>' . esc_html( $name ) . '</td><td>' . ( $c['r3'] ? esc_html( number_format( $c['r3'] ) ) : '-' ) . '</td><td>' . ( $c['r4'] ? esc_html( number_format( $c['r4'] ) ) : '-' ) . '</td><td>' . ( $c['r5'] ? esc_html( number_format( $c['r5'] ) ) : '-' ) . '</td></tr>'; }
		$h = '<p>המחיר החציוני של דירות שנמכרו לפי מספר החדרים, ברבעון האחרון שפורסם לכל עיר (ברובן 1-3.2026), לפי נתוני רשות המסים (₪):</p><table><thead><tr><th>עיר</th><th>3 חדרים</th><th>4 חדרים</th><th>5 חדרים</th></tr></thead><tbody>' . $rows . '</tbody></table>';
		$s = $read( 'value-series.json' );
		if ( ! is_array( $s ) || empty( $s['cbs']['s']['40010']['v'] ) || empty( $s['q'] ) ) { return $h; }
		$mi = function ( $k ) { $p = explode( '-', $k ); return (int) $p[0] * 12 + (int) $p[1] - 1; };
		$mon = function ( $k ) { $p = explode( '-', $k ); return (int) $p[1] . '.' . $p[0]; };
		$pct = function ( $r ) { return ( $r < 0 ? '-' : '+' ) . number_format( abs( 100 * $r ), 1 ) . '%'; };
		$n = $s['cbs']['s']['40010']['v']; $c = count( $n ); $latest = $s['cbs']['latest'];
		$t = 'מדד מחירי הדירות של הלמ״ס ל־' . $mon( $latest ) . ': ' . number_format( $n[ $c - 1 ], 1 ) . ' נקודות (ממוצע 1993 = 100), ' . $pct( $n[ $c - 1 ] / $n[ $c - 13 ] - 1 ) . ' בשנה. הערכים של החודשים האחרונים זמניים ומתעדכנים מדי חודש.';
		$y = isset( $s['city']['יבנה']['r4'] ) ? $s['city']['יבנה']['r4'] : null;
		$d = isset( $s['cbs']['s']['60300'] ) ? $s['cbs']['s']['60300'] : null;
		$q0 = $s['q'][0]; $m0 = explode( '.', $q0 ); $m0 = $m0[1] . '-' . sprintf( '%02d', (int) substr( $m0[0], strpos( $m0[0], '-' ) + 1 ) );  // "1-3.2021" -> "2021-03", the purchase month of the example
		$i0 = $d ? $mi( $m0 ) - $mi( $d['from'] ) : -1;
		if ( $y && ! empty( $y[0] ) && $d && $i0 >= 0 && isset( $d['v'][ $i0 ] ) ) {
			$b = round( $y[0] * end( $d['v'] ) / $d['v'][ $i0 ] / 100 ) * 100;
			$last = -1; for ( $k = count( $y ) - 1; $k >= 0; $k-- ) { if ( ! empty( $y[ $k ] ) ) { $last = $k; break; } }
			$t .= ' שלוש בדיקות לשווי היום: החציון הרשמי היום, מחיר הקנייה לפי מדד המחוז, ומחיר הקנייה לפי החציון מאז הקנייה. דוגמה: דירת 4 חדרים ביבנה שנקנתה ב־' . number_format( $y[0] ) . ' ₪, החציון של ' . $q0
				. ', שווה כ־' . number_format( $b ) . ' ₪ לפי מדד מחוז המרכז (' . $mon( $m0 ) . ' עד ' . $mon( $latest ) . '), וחציון 4 חדרים ביבנה ב־' . $s['q'][ $last ] . ' הוא ' . number_format( $y[ $last ] ) . ' ₪. הערכה ראשונית, לא חוות דעת שמאית.';
		}
		return $h . '<p>' . esc_html( $t ) . '</p>';
	}
}

if ( PHP_SAPI === 'cli' && isset( $argv[0] ) && realpath( $argv[0] ) === realpath( __FILE__ ) ) {  // the check: print it from the repo data
	if ( ! function_exists( 'esc_html' ) ) { function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); } }
	echo nadlan_nli_pval_summary_v2( dirname( __DIR__, 5 ) . '/plugins/nadlan-config/assets/instruments/data' ), "\n";
}
