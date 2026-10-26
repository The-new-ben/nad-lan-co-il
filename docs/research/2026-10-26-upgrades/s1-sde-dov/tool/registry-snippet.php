<?php
/**
 * S1 (Sde Dov hub moat), NOT APPLIED: the two pieces that go into plugins/nadlan-config/inc/instruments.php when the tool ships.
 * (1) the registry entry, inside nadlan_nli_tools() (next to 'urtrack'); (2) the no-script summary, inside nadlan_nli_summary()
 * (next to the 'urtrack' branch). Kept here as two plain functions so tool/test_summary.php can lint and run them on the real data.
 */

/* (1) registry entry ------------------------------------------------------------------------------------------------------ */
function s1_sdplan_registry_entry() {
	return array(
		/* S1 (HAD-601 loop, Sde Dov hub moat): "כל מגרש ברובע שדה דב"; sdplan.json from the Tel Aviv GIS (plots 837, plans and design plans 528, permits 772, construction sites 499, green line stations 764), the Israel Land Authority tender files and the OSM waterline (docs/research/2026-10-26-upgrades/s1-sde-dov/build_s1_data.py, 26.10.2026) */
		'sdplan' => array(
			'name' => 'כל מגרש ברובע שדה דב: מי זכה בו, בכמה, ובאיזה שלב הוא היום', 'cat' => 'ReferenceApplication', 'kicker' => 'מגרש אחר מגרש · רובע שדה דב',
			'desc' => 'לכל אחד מ־73 המגרשים למגורים, למלונאות ולתעסוקה ברובע שדה דב: היעוד והשטח בתכנית, מכרז רשות מקרקעי ישראל (הזוכה כפי שנרשם, יחידות הדיור, מספר ההצעות, סכום הזכייה והוצאות הפיתוח, וקרקע ופיתוח ליחידת דיור), תכנית העיצוב האדריכלי ותאריך אישורה, בקשה להיתר, היתר ותחילת עבודות לפי העירייה, תחנת הקו הירוק הקרובה והמרחק מהים, ובפרויקט שבשיווק: המחיר שדווח. מפה של כל מתחם לפי השלב הרשמי, וטבלה שמסדרים לפי שלב, הצעות, מחיר קרקע ליחידה או מרחק.',
			'data' => array( 'sdplan.json' ),
			'related' => array( '/sde-dov/prices/' => 'מחירי דירות בשדה דב', '/sde-dov/eshkol/' => 'מתחם אשכול', '/sde-dov/merkaz/' => 'מתחם המרכז', '/sde-dov/tzafon/' => 'מתחם הצפון', '/sde-dov/transport/' => 'תחבורה והקו הירוק', '/purchase-tax-calculator/' => 'מחשבון מס רכישה' ),
		),
	);
}

/* (2) no-script summary: the branch for nadlan_nli_summary( $id, $lang ) ------------------------------------------------------ */
function s1_sdplan_summary( $path ) {
	// in instruments.php: if ( 'sdplan' === $id ) { $path = dirname( __DIR__ ) . '/assets/instruments/data/sdplan.json'; ... }
	$d = is_readable( $path ) ? json_decode( (string) file_get_contents( $path ), true ) : null;
	if ( ! is_array( $d ) || empty( $d['plots'] ) || empty( $d['stages'] ) ) { return ''; }
	$dt = function ( $iso ) { $p = explode( '-', (string) $iso ); return 3 === count( $p ) ? (int) $p[2] . '.' . (int) $p[1] . '.' . $p[0] : (string) $iso; };
	$cn = array( 'eshkol' => 'מתחם אשכול', 'merkaz' => 'מרכז הרובע', 'tzafon' => 'צפון הרובע' );
	$use = array( 'res' => 'מגורים', 'special' => 'דיור מוגן ודיור מיוחד', 'hotel' => 'מלונאות', 'biz' => 'תעסוקה ומסחר' );
	$st = $d['stages']; $by = array_fill( 0, count( $st ), 0 ); $units = 0; $open = 0;
	$num = function ( $id ) { return (int) preg_replace( '/\D/', '', (string) $id ); };
	foreach ( $d['plots'] as $r ) {
		$by[ (int) $r['s'] ]++;
		if ( ! empty( $r['open'] ) ) { $open++; }
		if ( ! empty( $r['t']['units'] ) ) {
			$first = true; foreach ( (array) ( $r['t']['with'] ?? array() ) as $w ) { if ( $num( $w ) < $num( $r['id'] ) ) { $first = false; } }
			if ( $first ) { $units += (int) $r['t']['units']; }
		}
	}
	$cell = function ( $r ) use ( $st, $dt ) {
		$s = $st[ (int) $r['s'] ];
		if ( ! empty( $r['open'] ) ) { return $s . ', מכרז פתוח עד ' . $dt( $r['open']['close'] ); }
		if ( ! empty( $r['nobid'] ) && empty( $r['t'] ) ) { return $s . ', מכרז בלי הצעות'; }
		if ( 5 === (int) $r['s'] && ! empty( $r['works']['start'] ) ) { return $s . ' מ-' . $dt( $r['works']['start'] ); }
		if ( 4 === (int) $r['s'] && ! empty( $r['permit']['first'] ) ) { return $s . ' ' . $dt( $r['permit']['first'] ); }
		if ( 3 === (int) $r['s'] && ! empty( $r['req']['open'] ) ) { return $s . ' ' . $dt( $r['req']['open'] ); }
		if ( 2 === (int) $r['s'] && ! empty( $r['design'] ) ) { return $s . ' ' . $dt( $r['design'] ); }
		if ( 1 === (int) $r['s'] && ! empty( $r['t']['close'] ) ) { return $s . ' ' . $dt( $r['t']['close'] ); }
		return $s;
	};
	$who = function ( $r ) use ( $use ) {
		if ( ! empty( $r['p']['n'] ) ) { return $r['p']['n']; }
		if ( ! empty( $r['t']['winner'] ) ) { return $r['t']['winner']; }
		if ( ! empty( $r['open'] ) ) { return 'במכרז פתוח'; }
		if ( ! empty( $r['nobid'] ) ) { return 'לא הוגשו הצעות'; }
		return $use[ $r['use'] ] ?? '';
	};
	$parts = array(); foreach ( $st as $i => $s ) { if ( $by[ $i ] ) { $parts[] = $s . ': ' . number_format( $by[ $i ] ); } }
	$p = '<p>רובע שדה דב, ' . esc_html( $dt( $d['built'] ) ) . ': ' . number_format( count( $d['plots'] ) ) . ' מגרשים למגורים, למלונאות ולתעסוקה בשלוש התכניות (תמ״ל/3001, תא/1/4444, תא/2/4444). '
		. esc_html( implode( '; ', $parts ) ) . '. במכרזי רשות מקרקעי ישראל שווקו ' . number_format( $units ) . ' יחידות דיור, ו־' . number_format( $open ) . ' מגרשים במכרז פתוח. '
		. 'השלב הוא הרישום הרשמי האחרון: תוצאות המכרז, תכנית העיצוב, הבקשה להיתר, ההיתר ותחילת העבודות לפי העירייה. המרחקים בקו אווירי. אין כאן מועד מסירה או אכלוס.</p>';
	$t = '<table><caption>כל המגרשים ברובע שדה דב והשלב שלהם (' . count( $d['plots'] ) . ')</caption><thead><tr><th>מגרש</th><th>מתחם</th><th>פרויקט או זוכה</th><th>יח״ד</th><th>השלב היום</th><th>תחנת הקו הירוק הקרובה</th></tr></thead><tbody>';
	$order = array( 'eshkol' => 0, 'merkaz' => 1, 'tzafon' => 2 ); $rows = $d['plots'];
	usort( $rows, function ( $a, $b ) use ( $order, $num ) { return ( $order[ $a['c'] ] - $order[ $b['c'] ] ) ?: ( $num( $a['id'] ) - $num( $b['id'] ) ); } );
	foreach ( $rows as $r ) {
		$u = ! empty( $r['t']['units'] ) ? number_format( (int) $r['t']['units'] ) : ( ! empty( $r['open']['units'] ) ? number_format( (int) $r['open']['units'] ) : '' );
		$t .= '<tr><td>' . esc_html( $r['id'] ) . '</td><td>' . esc_html( $cn[ $r['c'] ] ?? '' ) . '</td><td>' . esc_html( $who( $r ) ) . '</td><td>' . $u . '</td><td>' . esc_html( $cell( $r ) ) . '</td><td>' . esc_html( $r['st'][0] . ', כ־' . number_format( (int) $r['st'][1] ) . ' מ׳' ) . '</td></tr>';
	}
	return $p . $t . '</tbody></table>';
}
