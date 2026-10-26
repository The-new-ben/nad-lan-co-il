<?php
/* NOT APPLIED. Two branches to add inside nadlan_nli_summary( $id, $lang ) in plugins/nadlan-config/inc/instruments.php, next to the
   'urtrack' branch: what the tools 'pinui' and 'urcity' say, as plain text and a table, for readers without JS, search engines and AI.
   They read the same data files as the tools (pinui.json, urcity.json, renewal-track.json); the words match tools/pinui.js and
   tools/urcity.js. Checked with snippets/test_summaries.php (php -l + a run on the real data). */
		if ( 'pinui' === $id ) {  // G2 /urban-renewal/pinui-binui/: the law's majorities for common building sizes, the 1ד clock, the tax ceiling
			$path = dirname( __DIR__ ) . '/assets/instruments/data/pinui.json';
			$d = is_readable( $path ) ? json_decode( (string) file_get_contents( $path ), true ) : null;
			if ( ! is_array( $d ) || empty( $d['law'] ) ) { return ''; }
			$k = $d['key2025']; $avg = end( $d['series']['approval_to_permit'] );
			$need = function ( $u ) { return ( $u >= 4 && $u <= 5 ) ? 3 : (int) ceil( $u * 3 / 5 - 1e-9 ); };
			$p = '<p>פינוי בינוי לפי חוק פינוי ובינוי (עידוד מיזמי פינוי ובינוי), התשס"ו-2006: רוב מיוחס הוא בעלים של שני שלישים לפחות מהדירות במקבץ, שלוש חמישיות לפחות מהדירות בכל בניין (בבניין של 4 או 5 דירות: 3 דירות ויותר משני בעלי דירות), ויותר ממחצית הרכוש המשותף בכל בניין. '
				. 'בעלי יותר משתי חמישיות מהדירות ומהרכוש המשותף בכל בניין יכולים לבקש מהרשות שמאי פינוי ובינוי בחינם. מהעסקה הראשונה: חצי מבעלי הדירות בתוך שנתיים, שלוש חמישיות בתוך 4 שנים ותכנית בתוך 4.5 שנים, אחרת רוב באסיפה כללית יכול לאפשר ביטול. '
				. 'תקרת הפטור ממס לדירת התמורה: הגבוה מבין 120 מ"ר, 150% מהשווי בניכוי הזכויות שעוברות ליזם, או 50% יותר עד 200 מ"ר. ב-2025 אושרו ' . (int) $k['pb_plans'] . ' תכניות עם ' . number_format( (int) $k['pb_units'] ) . ' דירות, ומאישור תכנית עד היתר ראשון עברו בממוצע ' . esc_html( number_format( (float) $avg[1], 1 ) ) . ' שנים (' . (int) $avg[2] . ' מתחמים, הרשות הממשלתית להתחדשות עירונית).</p>';
			$p .= '<table><caption>כמה חתימות צריך בבניין, לפי מספר הדירות</caption><thead><tr><th>דירות בבניין</th><th>שלוש חמישיות</th><th>שני שלישים (כל המקבץ)</th><th>יותר משתי חמישיות (שמאי הרשות)</th></tr></thead><tbody>';
			foreach ( array( 4, 5, 8, 12, 16, 24, 32, 48 ) as $u ) {
				$p .= '<tr><td>' . $u . '</td><td>' . $need( $u ) . '</td><td>' . (int) ceil( $u * 2 / 3 - 1e-9 ) . '</td><td>' . ( (int) floor( $u * 2 / 5 + 1e-9 ) + 1 ) . '</td></tr>';
			}
			return $p . '</tbody></table>';
		}
		if ( 'urcity' === $id ) {  // G3 /urban-renewal/: the complexes per city on the authority's map and the TAMA 38 line of the 2025 report
			$base = dirname( __DIR__ ) . '/assets/instruments/data/';
			$u = is_readable( $base . 'urcity.json' ) ? json_decode( (string) file_get_contents( $base . 'urcity.json' ), true ) : null;
			$t = is_readable( $base . 'renewal-track.json' ) ? json_decode( (string) file_get_contents( $base . 'renewal-track.json' ), true ) : null;
			if ( ! is_array( $u ) || ! is_array( $t ) || empty( $t['recs'] ) ) { return ''; }
			$lm = -1; foreach ( $t['snaps'] as $i => $s ) { if ( 'map' === $s['k'] ) { $lm = $i; } }
			if ( $lm < 0 ) { return ''; }
			$dt = function ( $iso ) { $p = explode( '-', (string) $iso ); return 3 === count( $p ) ? (int) $p[2] . '.' . (int) $p[1] . '.' . $p[0] : (string) $iso; };
			$c = array(); $n = 0; $appr = 0;
			foreach ( $t['recs'] as $r ) {
				$s = (int) $r['s'][ $lm ]; if ( -1 === $s ) { continue; }
				$x = $r['c']; if ( ! isset( $c[ $x ] ) ) { $c[ $x ] = array( 'n' => 0, 'a' => 0, 'p' => 0, 'pe' => 0, 'pp' => 0 ); }
				$c[ $x ]['n']++; $n++; if ( $s >= 3 ) { $c[ $x ]['a']++; $appr++; }
				$c[ $x ]['p'] += (int) ( $r['p'] ?? 0 ); if ( ! empty( $r['e'] ) && ! empty( $r['p'] ) ) { $c[ $x ]['pe'] += (int) $r['e']; $c[ $x ]['pp'] += (int) $r['p']; }
			}
			uasort( $c, function ( $a, $b ) { return $b['n'] <=> $a['n']; } );
			$tama = array(); foreach ( $u['replace'] as $r ) { $tama[ $r['c'] ] = $r['st'] . ( $r['ext'] ? '' : '; בלי הארכה לתמ"א 38' ); }
			$p = '<p>מתחמי התחדשות עירונית במפת הרשות הממשלתית להתחדשות עירונית, ' . esc_html( $dt( $t['snaps'][ $lm ]['d'] ) ) . ': ' . number_format( $n ) . ' מתחמים ב-' . count( $c ) . ' ערים, ' . number_format( $appr ) . ' מהם בתכנית מאושרת או במימוש. '
				. 'שלושה מסלולים: פינוי בינוי של מתחם, תמ"א 38 לבניין, ותכנית לרישוי מהיר לפי סעיף 145א1. תמ"א 38 פקעה באוקטובר 2023, ובערים שמקדמות תכנית מחליפה הוארכה עד מאי 2026 או עד אישור התכנית, המוקדם מביניהם (דוח הרשות לשנת 2025).</p>';
			$p .= '<table><caption>הערים עם הכי הרבה מתחמים</caption><thead><tr><th>עיר</th><th>מתחמים</th><th>מאושרת או במימוש</th><th>דירות אחרי הבנייה</th><th>מכפיל (חישוב שלנו)</th><th>תמ"א 38 בעיר</th></tr></thead><tbody>';
			foreach ( array_slice( $c, 0, 20, true ) as $x => $v ) {
				$p .= '<tr><td>' . esc_html( $x ) . '</td><td>' . $v['n'] . '</td><td>' . $v['a'] . '</td><td>' . number_format( $v['p'] ) . '</td><td>' . ( $v['pe'] ? esc_html( number_format( $v['pp'] / $v['pe'], 2 ) ) : '' ) . '</td><td>' . esc_html( $tama[ $x ] ?? '' ) . '</td></tr>';
			}
			return $p . '</tbody></table>';
		}
