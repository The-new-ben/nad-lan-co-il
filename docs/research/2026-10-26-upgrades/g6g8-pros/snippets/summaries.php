<?php
/* NOT APPLIED. Four branches to add inside nadlan_nli_summary( $id, $lang ) in plugins/nadlan-config/inc/instruments.php, next to the
   'pinui' branch: what the tools 'bedek', 'shamai', 'shamaireg' and 'orechdin' say, as plain text and a table, for readers without JS,
   search engines and AI answers. They read the same data files as the tools (bedek.json, shamai.json, orechdin.json); the words
   match tools/bedek.js, tools/shamai.js, tools/orechdin.js. Checked with snippets/test_summaries.php (php -l + a run on the real data). */
		if ( 'bedek' === $id ) {  // G6 /home-inspection/: the law's periods for every defect type and the published price ranges
			$path = dirname( __DIR__ ) . '/assets/instruments/data/bedek.json';
			$d = is_readable( $path ) ? json_decode( (string) file_get_contents( $path ), true ) : null;
			if ( ! is_array( $d ) || empty( $d['law']['items'] ) ) { return ''; }
			$yrs = function ( $y ) { return 1 === (int) $y ? 'שנה' : (int) $y . ' שנים'; };
			$env = function ( $kind, $rooms = null ) use ( $d ) { $lo = PHP_INT_MAX; $hi = 0; foreach ( $d['prices'] as $s ) { foreach ( $s['rows'] as $r ) { if ( $r[0] !== $kind ) { continue; } if ( null !== $rooms && ! empty( $r[4] ) && ( $rooms < $r[4][0] || $rooms > $r[4][1] ) ) { continue; } $lo = min( $lo, $r[2] ); $hi = max( $hi, $r[3] ); } } return array( $lo, $hi ); };
			$a4 = $env( 'apt', 4 ); $h = $env( 'house' );
			$p = '<p>בדק בית לפי חוק המכר (דירות), התשל"ג-1973: לכל סוג ליקוי תקופת בדק מיום המסירה, ואחריה ' . (int) $d['law']['warranty_y'] . ' שנות אחריות. בתקופת הבדק הקבלן אחראי אלא אם יוכיח שהליקוי נגרם בידי הקונה; '
				. 'בתקופת האחריות הקונה צריך להראות שמקור הליקוי בתכנון, בעבודה או בחומרים. ליקוי יסודי בשלד: ' . (int) $d['law']['struct_y'] . ' שנה. ליקוי שאפשר היה לראות במסירה: הודעה לקבלן בתוך שנה. '
				. 'קונה משנה נהנה מאותן תקופות, מהמסירה לקונה הראשון. מחירים שפורסמו לבדק בית: דירת 4 חדרים ' . number_format( $a4[0] ) . ' עד ' . number_format( $a4[1] ) . ' ₪, בית פרטי ' . number_format( $h[0] ) . ' עד ' . number_format( $h[1] ) . ' ₪ (במידרג כולל מע"מ; אצל השאר לא צוין).</p>';
			$p .= '<table><caption>תקופות הבדק והאחריות לפי סוג הליקוי</caption><thead><tr><th>סוג הליקוי</th><th>תקופת בדק</th><th>הקבלן אחראי בסך הכול</th></tr></thead><tbody>';
			foreach ( $d['law']['items'] as $it ) { $p .= '<tr><td>' . esc_html( $it['law'] ) . '</td><td>' . esc_html( $yrs( $it['y'] ) ) . '</td><td>' . esc_html( ( (int) $it['y'] + (int) $d['law']['warranty_y'] ) . ' שנים' ) . '</td></tr>'; }
			$p .= '<tr><td>אי התאמה יסודית בשלד וביציבות</td><td>' . (int) $d['law']['struct_y'] . ' שנה</td><td>' . (int) $d['law']['struct_y'] . ' שנה</td></tr>';
			return $p . '</tbody></table>';
		}
		if ( 'shamai' === $id || 'shamaireg' === $id ) {  // G7 /real-estate-appraiser/: who orders and pays, the deadlines, the decisive appraiser's fee, the register
			$path = dirname( __DIR__ ) . '/assets/instruments/data/shamai.json';
			$d = is_readable( $path ) ? json_decode( (string) file_get_contents( $path ), true ) : null;
			if ( ! is_array( $d ) || empty( $d['purposes'] ) ) { return ''; }
			$r = $d['register']; $dt = function ( $iso ) { $x = explode( '-', (string) $iso ); return 3 === count( $x ) ? (int) $x[2] . '.' . (int) $x[1] . '.' . $x[0] : (string) $iso; };
			if ( 'shamaireg' === $id ) {
				return '<p>פנקס שמאי המקרקעין של משרד המשפטים: ' . number_format( (int) $r['count'] ) . ' שמאים מורשים (עודכן ' . esc_html( $dt( $r['updated'] ) ) . '). לפי חוק שמאי מקרקעין, שמאי מקרקעין הוא מי שרשום בפנקס, '
					. 'ורק הוא רשאי לעשות שומת מקרקעין בשכר. בודקים שמאי לפי שם או מספר רישיון במאגר הרשמי: <a href="' . esc_url( $r['page'] ) . '">מאגר שמאי מקרקעין ב-data.gov.il</a>.</p>';
			}
			$fee = function ( $a ) use ( $d ) { $f = 0; foreach ( $d['decisive']['table'] as $b ) { $hi = $b[1] ? $b[1] : PHP_INT_MAX; if ( $a > $b[0] ) { $f += ( min( $a, $hi ) - $b[0] ) * $b[2]; } } return max( $d['decisive']['min'], min( $d['decisive']['max'], $f ) ); };
			$p = '<p>שמאי מקרקעין: ' . number_format( (int) $r['count'] ) . ' שמאים רשומים בפנקס של משרד המשפטים. ערר על היטל השבחה או בקשה לשמאי מכריע: בתוך ' . (int) $d['decisive']['appeal_days'] . ' ימים מהיום שהשומה הובאה לידיעת החייב. '
				. 'תביעה לפי סעיף 197: בתוך ' . (int) $d['s197_years'] . ' שנים מתחילת תוקף התכנית. שכר שמאי מכריע לפי התקנות: 3% עד 500,000 ₪, 2% עד מיליון, 1% עד 2 מיליון ו-0.5% מעל, לפחות ' . number_format( (int) $d['decisive']['min'] ) . ' ₪ ולכל היותר '
				. number_format( (int) $d['decisive']['max'] ) . ' ₪, ועוד מע"מ, מחצית לכל צד. על השבחה של מיליון ₪: ' . number_format( $fee( 1000000 ) ) . ' ₪.</p>';
			$p .= '<table><caption>איזו שומה צריך: מי מזמין, מי משלם ומה המועד</caption><thead><tr><th>מטרה</th><th>מי מזמין</th><th>מי משלם</th><th>מועד בחוק</th></tr></thead><tbody>';
			foreach ( $d['purposes'] as $x ) {
				$dl = empty( $x['deadline'] ) ? 'אין' : ( ! empty( $x['deadline']['days'] ) ? (int) $x['deadline']['days'] . ' ימים' : (int) $x['deadline']['years'] . ' שנים' );
				$p .= '<tr><td>' . esc_html( $x['label'] ) . '</td><td>' . esc_html( $x['who_s'] ) . '</td><td>' . esc_html( $x['pay_s'] ) . '</td><td>' . esc_html( $dl ) . '</td></tr>';
			}
			return $p . '</tbody></table>';
		}
		if ( 'orechdin' === $id ) {  // G8 /real-estate-lawyer/: the developer's-lawyer cap by price, the Bar's recommended tariff, the registry fees
			$path = dirname( __DIR__ ) . '/assets/instruments/data/orechdin.json';
			$d = is_readable( $path ) ? json_decode( (string) file_get_contents( $path ), true ) : null;
			if ( ! is_array( $d ) || empty( $d['cap'] ) ) { return ''; }
			$c = $d['cap']; $t = $d['tariff']; $f = array(); foreach ( $d['land'] as $x ) { $f[ $x[0] ] = $x[2]; }
			$tar = function ( $v ) use ( $t ) { if ( $v > $t['top'] ) { return $t['top_min']; } $s = 0; foreach ( $t['tiers'] as $b ) { if ( $v > $b[0] ) { $s += ( min( $v, $b[1] ) - $b[0] ) * $b[2]; } } return max( $t['min'], $s ); };
			$p = '<p>עורך דין מקרקעין: משרדים פרסמו ב-2026 שכר טרחה של כ-0.5% ממחיר הדירה ועוד מע"מ, עד 1%, עם מינימום של כ-5,000 עד 6,000 ₪. התעריף המינימלי המומלץ של לשכת עורכי הדין (המלצה שאינה מחייבת) לעריכת חוזה על 2 מיליון ₪: '
				. number_format( $tar( 2000000 ) ) . ' ₪. בדירה חדשה הקבלן רשאי לגבות מהקונה על עורך הדין שלו לכל היותר ' . number_format( (int) $c['fixed'] ) . ' ₪ (' . (int) $c['year'] . ') או 0.5% מהמחיר, הנמוך מביניהם, ועוד מע"מ, ועוד עד '
				. number_format( (int) $c['list_fee'] ) . ' ₪ לניהול רשימת הזכויות; מעל ' . number_format( (int) $c['ceiling'] ) . ' ₪ אין תקרה. אגרות הטאבו: הערת אזהרה ' . (int) $f['warn'] . ' ₪, רישום מכר ' . (int) $f['sale'] . ' ₪, רישום משכנתה ' . (int) $f['mortgage'] . ' ₪. '
				. 'הצהרה לרשות המסים בתוך 30 יום ומס רכישה בתוך 60 יום. המידע כללי ואינו ייעוץ משפטי.</p>';
			$p .= '<table><caption>מה מותר לקבלן לגבות על עורך הדין שלו, לפי מחיר הדירה</caption><thead><tr><th>מחיר הדירה</th><th>המרבי לפני מע"מ</th></tr></thead><tbody>';
			foreach ( array( 1000000, 1500000, 2000000, 3000000, 4000000, 5000000 ) as $v ) { $m = $v > $c['ceiling'] ? 'אין תקרה' : number_format( min( $c['fixed'], $v * $c['pct'] ) ) . ' ₪'; $p .= '<tr><td>' . number_format( $v ) . ' ₪</td><td>' . esc_html( $m ) . '</td></tr>'; }
			return $p . '</tbody></table>';
		}
