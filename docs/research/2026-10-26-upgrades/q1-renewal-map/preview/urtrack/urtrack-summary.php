<?php
/* NOT APPLIED. The branch to add inside nadlan_nli_summary( $id, $lang ) in plugins/nadlan-config/inc/instruments.php, next to
   the 'gwall' and 't466' branches: the "מה זז במאגר" count line and every change between the snapshots (T8), as plain text for
   readers without JS, search engines and AI. Reads the same renewal-track.json the tool reads; the words match tools/urtrack.js. */
		if ( 'urtrack' === $id ) {  // Q1 moat: the count line and the table of changes (T8)
			$path = dirname( __DIR__ ) . '/assets/instruments/data/renewal-track.json';
			$d = is_readable( $path ) ? json_decode( (string) file_get_contents( $path ), true ) : null;
			if ( ! is_array( $d ) || empty( $d['recs'] ) || empty( $d['agg'] ) ) { return ''; }
			$dt = function ( $iso ) { $p = explode( '-', (string) $iso ); return 3 === count( $p ) ? (int) $p[2] . '.' . (int) $p[1] . '.' . $p[0] : (string) $iso; };
			$st = array( 'ללא שלב', 'תכנון ראשוני', 'תכנון סטטוטורי', 'תכנית מאושרת', 'במימוש', 'אחרי רישוי' );
			$kind = array( 'new' => 'נוסף', 'up' => 'עלה שלב', 'down' => 'ירד שלב', 'chg' => 'השלב השתנה', 'gone' => 'ירד מהרשימה', 'back' => 'חזר לרשימה', 'trk' => 'המסלול השתנה', 'renum' => 'מספר מתחם חדש' );
			$order = array( 'up' => 0, 'new' => 1, 'down' => 2, 'chg' => 3, 'trk' => 4, 'renum' => 5, 'back' => 6, 'gone' => 7 );
			$s = function ( $i ) use ( $st ) { return $st[ max( 0, (int) $i ) ]; };
			$ft = function ( $c ) use ( $s, $d ) {
				switch ( $c[1] ) {
					case 'new':
					case 'back': return 'נכנס: ' . $s( $c[3] );
					case 'gone': return 'אחרון: ' . $s( $c[2] );
					case 'trk': return $d['tracks'][ (int) $c[2] ] . ' ← ' . $d['tracks'][ (int) $c[3] ];
					case 'renum': return $c[2] . ' ← ' . $c[3];
					default: return $s( $c[2] ) . ' ← ' . $s( $c[3] );
				}
			};
			$rows = array();
			foreach ( $d['recs'] as $r ) { foreach ( (array) ( $r['ch'] ?? array() ) as $c ) { $rows[] = array( $r, $c ); } }
			usort( $rows, function ( $x, $y ) use ( $order ) {
				return strcmp( $y[1][0], $x[1][0] ) ?: ( ( $order[ $x[1][1] ] ?? 9 ) - ( $order[ $y[1][1] ] ?? 9 ) ) ?: strcmp( $x[0]['c'], $y[0]['c'] ) ?: strcmp( $x[0]['n'], $y[0]['n'] );
			} );
			$a = $d['agg'];
			$pl = function ( $n, $one, $many ) { return number_format( (int) $n ) . ' ' . ( 1 === (int) $n ? $one : $many ); };
			$p = array( ( 1 === (int) $a['added'] ? 'נוסף ' : 'נוספו ' ) . $pl( $a['added'], 'מתחם', 'מתחמים' ), $pl( $a['up'], 'עלה שלב', 'עלו שלב' ) );
			if ( ! empty( $a['down'] ) ) { $p[] = $pl( $a['down'], 'ירד שלב', 'ירדו שלב' ); }
			if ( ! empty( $a['chg'] ) ) { $p[] = $pl( $a['chg'], 'שינה שלב', 'שינו שלב' ); }
			if ( ! empty( $a['gone'] ) ) { $p[] = $pl( $a['gone'], 'לא מופיע עוד', 'לא מופיעים עוד' ); }
			if ( ! empty( $a['renum'] ) ) { $p[] = $pl( $a['renum'], 'קיבל מספר מתחם חדש', 'קיבלו מספר מתחם חדש' ); }
			$last = array_pop( $p );
			$line = 'מאז ' . $dt( $a['since'] ) . ' ' . ( $p ? implode( ', ', $p ) . ' ו-' : '' ) . $last . ' (קובץ data.gov.il מול מפת הרשות של ' . $dt( $a['to'] ) . ').';
			$snaps = array(); $now = 0;
			foreach ( $d['snaps'] as $x ) { $snaps[] = $x['label'] . ' ' . $dt( $x['d'] ); if ( 'map' === $x['k'] ) { $now = (int) $x['n']; } }
			$t = '<table><caption>מה זז במאגר: כל השינויים בין הבדיקות (' . count( $rows ) . ')</caption><thead><tr><th>מתחם</th><th>עיר</th><th>מה השתנה</th><th>משלב ← לשלב</th><th>תאריך הבדיקה</th></tr></thead><tbody>';
			foreach ( $rows as $x ) {
				$t .= '<tr><td>' . esc_html( $x[0]['n'] ) . '</td><td>' . esc_html( $x[0]['c'] ) . '</td><td>' . esc_html( $kind[ $x[1][1] ] ?? $x[1][1] ) . '</td><td>' . esc_html( $ft( $x[1] ) ) . '</td><td>' . esc_html( $dt( $x[1][0] ) ) . '</td></tr>';
			}
			return '<p>' . esc_html( $line ) . ' במפת הרשות היום ' . number_format( $now ) . ' מתחמים. הבדיקות: ' . esc_html( implode( ', ', $snaps ) ) . '. כל שינוי מתוארך לבדיקה הראשונה שבה ראינו אותו. אין כאן שנת התחלת בנייה או אכלוס: המקורות לא מפרסמים אותן.</p>' . $t . '</tbody></table>';
		}
