# G1 · what the release adds to `plugins/nadlan-config/inc/instruments.php` (NOT applied)

The research session built the tools locally and did not touch `inc/instruments.php` (owner order 26.10.2026: no edits to live
files). The releaser pastes the two blocks below, after reading the LIVE copy of the file first (memory: the repo is not live
for every file; target = live + these additions), lints with `php -l`, and ships these files together:

| File | State |
|---|---|
| `plugins/nadlan-config/assets/instruments/tools/dirafit.js` | new (two tools: `dirafit`, `diracost`) |
| `plugins/nadlan-config/assets/instruments/data/dira-round.json` | new, built by `tools/instruments/build_dira_round.py` |
| `plugins/nadlan-config/inc/instruments.php` | live copy + block 1 + block 2 |
| `tools/instruments/build_dira_round.py`, `tools/instruments/test_dirafit.js` | repo only (`node tools/instruments/test_dirafit.js` must print ALL OK) |

`boi-mortgage.json` and `ptax.json` are already live and shared.

## Block 1: the registry (inside `nadlan_nli_tools()`, right after the `'dira'` entry)

```php
			/* G1 (26.10.2026): /dira-behanacha/ upgrade, two tools in one file tools/dirafit.js; data dira-round.json (official lottery
			   file + the ministry's releases of 25.5, 23.6 and 2.8.2026 + gov.il rules + invest.json), boi-mortgage.json, ptax.json */
			'dirafit' => array(
				'file' => 'dirafit', 'name' => 'דירה בהנחה: מי זכאי ואיפה הכי כדאי להירשם', 'cat' => 'UtilitiesApplication', 'kicker' => 'בדיקה אישית · דירה בהנחה',
				'desc' => 'בדיקת זכאות לדירה בהנחה (מחיר למשתכן) לפי ההגדרות של משרד הבינוי והשיכון: חסר דירה, משפר דיור או לא זכאי, עדיפות מילואים ובני מקום, ושלוש הערים שנתנו הכי הרבה דירות לכל משק בית שנרשם בהגרלה ה־11, לצד הסיכוי בכל עיר בקובץ הרשמי.',
				'data' => array( 'dira-round.json' ),
				'related' => array( '/mortgage-calculator/' => 'מחשבון משכנתא', '/apartment-purchase-cost-calculator/' => 'עלות רכישה כוללת', '/new-projects/presale-apartment/' => 'דירה על הנייר', '/real-estate-lawyer/' => 'עורך דין מקרקעין' ),
			),
			'diracost' => array(
				'file' => 'dirafit', 'name' => 'דירה בהנחה: המחיר מול מחירי העסקאות בעיר', 'cat' => 'FinanceApplication', 'kicker' => 'מחשבון · דירה בהנחה',
				'desc' => 'מחיר הדירה מההגרלה לפי המחיר למ״ר והשטח, עם מע״מ, מול חציון העסקאות של דירות באותו גודל בעיר, ההון העצמי לפי כללי התוכנית (75%, מסלול השמאי, מענק 40,000 או 60,000 ₪) וההחזר החודשי בריבית הממוצעת של בנק ישראל.',
				'data' => array( 'dira-round.json', 'boi-mortgage.json', 'ptax.json' ),
				'related' => array( '/mortgage-calculator/' => 'מחשבון משכנתא', '/apartment-prices/' => 'מחירי דירות בישראל', '/new-projects/construction-input-index/' => 'הצמדה למדד תשומות הבנייה', '/purchase-tax-calculator/' => 'מחשבון מס רכישה' ),
			),
```

## Block 2: the plain summaries (inside `nadlan_nli_summary()`, next to the `'dira'` branch)

For readers without scripts and for search engines; the script replaces them with the live tools. Numbers come from the same
JSON, nothing is typed twice.

```php
		if ( 'dirafit' === $id || 'diracost' === $id ) { // G1: round 11 by town and the rules, from dira-round.json
			$path = dirname( __DIR__ ) . '/assets/instruments/data/dira-round.json';
			$x = is_readable( $path ) ? json_decode( (string) file_get_contents( $path ), true ) : null;
			if ( ! is_array( $x ) || empty( $x['towns'] ) ) { return ''; }
			$r = $x['r11']; $f = function ( $n, $d = 0 ) { return esc_html( number_format( (float) $n, $d ) ); };
			if ( 'dirafit' === $id ) {
				$t = $x['towns']; usort( $t, function ( $a, $b ) { return $b['per100'] <=> $a['per100']; } );
				$rest = ( $r['units'] - $r['res_wins'] ) / max( 1, $r['households'] - $r['res_regs'] );
				$h = '<p>מי זכאי לדירה בהנחה: חסרי דירה (בלי דירה, או עד שליש דירה, ב־3 השנים האחרונות) שהם זוג נשוי או ידועים בציבור, זוג שמתחתן בתוך 3 חודשים, יחידים מגיל 35, הורה עם ילד רווק מתחת לגיל 21, נכים ואלמנים מגיל 21. משפרי דיור נרשמים רק להגרלות המשך. לא זכאים: מי שהחזיק שתי דירות במקביל, מי שכבר קנה בתוכנית של מחיר מפוקח, וחברי קיבוץ. אישור זכאות: 200 ₪, עד 10 ימי עבודה. בהגרלה ה־11 נרשמו '
					. $f( $r['households'] ) . ' משקי בית ל־' . $f( $r['units'] ) . ' דירות ב־19 יישובים; זכו ' . $f( 100 * $r['units'] / $r['households'], 1 ) . '% מכלל משקי הבית, '
					. $f( 100 * $r['res_wins'] / $r['res_regs'], 1 ) . '% ממשרתי המילואים ו־' . $f( 100 * $rest, 1 ) . '% מכל השאר (החישוב שלנו, לפי משרד הבינוי והשיכון).</p>'
					. '<table><thead><tr><th>עיר</th><th>דירות</th><th>משקי בית שנרשמו</th><th>דירות לכל 100 נרשמים</th><th>הסיכוי בהגרלה בקובץ</th><th>בני מקום בקובץ</th></tr></thead><tbody>';
				foreach ( $t as $c ) {
					$o = $c['hist']['odds']; $l = $c['hist']['lodds'];
					$h .= '<tr><td>' . esc_html( $c['n'] ) . '</td><td>' . $f( $c['units'] ) . '</td><td>' . $f( $c['hh'] ) . '</td><td>' . $f( $c['per100'], $c['per100'] < 1 ? 2 : 1 ) . '</td><td>'
						. ( null === $o ? 'אין' : $f( 100 * $o, 2 ) . '%' ) . '</td><td>' . ( null === $l ? 'אין' : $f( 100 * $l, 2 ) . '%' ) . '</td></tr>';
				}
				return $h . '</tbody></table>';
			}
			$h = '<p>המימון של זוכה בדירה בהנחה: משכנתא עד 75% מהמחיר, או לפי שווי שמאי באישור בנק ישראל עם 100,000 ₪ הון עצמי לפחות ושווי עד 2.1 מיליון ₪; מענק של 40,000 או 60,000 ₪ ביישובים מזכים. המחיר למ״ר בהגרלה מוצג לפני מע״מ. המחיר האחרון בקובץ הרשמי מול חציון העסקאות של דירות 4 חדרים בעיר, לדירה של 100 מ״ר עם מע״מ (החישוב שלנו):</p>'
				. '<table><thead><tr><th>עיר</th><th>מחיר למ״ר</th><th>תאריך</th><th>דירת 100 מ״ר עם מע״מ</th><th>חציון 4 חדרים</th><th>הפער</th></tr></thead><tbody>';
			foreach ( $x['towns'] as $c ) {
				if ( empty( $c['pm'] ) || empty( $c['mkt']['4'] ) || $c['pm']['date'] < '2024-01-01' ) { continue; }
				$p = $c['pm']['v'] * 100 * 1.18; $m = $c['mkt']['4']['price'];
				$h .= '<tr><td>' . esc_html( $c['n'] ) . '</td><td>' . $f( $c['pm']['v'] ) . ' ₪</td><td>' . esc_html( date_i18n( 'j.n.Y', strtotime( $c['pm']['date'] ) ) ) . '</td><td>' . $f( $p ) . ' ₪</td><td>' . $f( $m ) . ' ₪</td><td>' . $f( 100 * ( $m - $p ) / $m, 1 ) . '%</td></tr>';
			}
			return $h . '</tbody></table>';
		}
```

Optional (not needed for the page): to let a page open `dirafit` on a town, add `'local'` and `'family'` to the shortcode's `$set` keys
(`[nadlan_tool id="dirafit" local="קריית גת"]`), the same way `'town'` works for `dira`.

## Checks after the release (before the page writer runs)
- `GET /wp-json/nadlan/v1/health` shows the new version; `tools/dirafit.js?x=…` answers 200 and contains `register('dirafit'` and `register('diracost'`.
- A test page with `[nadlan_tool id="dirafit"]` and `[nadlan_tool id="diracost"]` prints the two summaries in the raw HTML and the two tools after the script.
- Then `python docs/research/2026-10-26-upgrades/g1-dira-behanacha/write_g1_page.py --dry` (REST GET only), then without `--dry`.
- After the page: rainbow + h-infinity spot check (law 7), `tools/source_audit.py` on /dira-behanacha/ before and after, `tools/content_first_check.py` is for project pages and does not apply here.
