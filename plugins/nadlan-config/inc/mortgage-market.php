<?php
/**
 * nadlan-config - The mortgage market this month (1.72.587, HAD-675, Ben 5.11.2026: "the best mortgage calculator page in the world",
 * "numbers, prices, data", "make AI engines cite it").
 *
 * [nadlan_mortgage_market] prints, as plain HTML that Google and AI engines read without scripts, the latest Bank of Israel numbers on
 * new mortgages: six headline figures, the average rates and the forecast all-in rate (IRR) by bank with the first payment on
 * 1,000,000 ILS over 25 years at each bank's own average mix, and the first payment on the median 4-room home in 25 cities. Every
 * figure is computed here from assets/instruments/data/boi-mortgage.json at render time, so a new monthly data file updates the page
 * by itself. A Dataset JSON-LD describes the tables on any page that holds the shortcode.
 * Also: nadlan_mm_quick_summary() for the [nadlan_tool id="mquick"] plain-text summary (inc/instruments.php).
 * Sources (in the data file, with dates): Bank of Israel, Banking Supervision, TamInt010.xls (rates and mix by bank), SDMX
 * BIR_MRTG_99 (new mortgages by LTV band, volume, count), the housing-loan stock; Israel Tax Authority median deal prices.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_mm_data' ) ) {
	function nadlan_mm_data() {
		static $d = null;
		if ( null !== $d ) { return $d; }
		$p = dirname( __DIR__ ) . '/assets/instruments/data/boi-mortgage.json';
		$x = is_readable( $p ) ? json_decode( (string) file_get_contents( $p ), true ) : null;
		$d = ( is_array( $x ) && ! empty( $x['by_bank']['months'] ) ) ? $x : array();
		return $d;
	}

	/** First monthly payment on $loan over $years at a bank's average mix and rates for month index $i (effective rates). */
	function nadlan_mm_pay( $d, $bank, $i, $loan = 1000000, $years = 25 ) {
		$tr = array( 'fixed_nl', 'prime', 'var_nl_other', 'var_cpi', 'fixed_cpi' );
		if ( empty( $d['by_bank']['mix'][ $bank ] ) || empty( $d['by_bank']['rate'][ $bank ] ) ) { return 0; }
		$mix = $d['by_bank']['mix'][ $bank ]; $rate = $d['by_bank']['rate'][ $bank ];
		$tot = 0; foreach ( $tr as $t ) { $tot += (float) ( $mix[ $t ][ $i ] ?? 0 ); }
		if ( $tot <= 0 ) { return 0; }
		$n = $years * 12; $pay = 0;
		foreach ( $tr as $t ) {
			$p = $loan * (float) $mix[ $t ][ $i ] / $tot;
			$r = pow( 1 + (float) $rate[ $t ][ $i ] / 100, 1 / 12 ) - 1;
			$pay += $r > 0 ? $p * $r / ( 1 - pow( 1 + $r, -$n ) ) : $p / $n;
		}
		return $pay;
	}

	function nadlan_mm_month( $ym, $lang = 'he' ) {
		$p = explode( '-', (string) $ym );
		if ( 2 !== count( $p ) ) { return (string) $ym; }
		$he = array( 1 => 'ינואר', 'פברואר', 'מרץ', 'אפריל', 'מאי', 'יוני', 'יולי', 'אוגוסט', 'ספטמבר', 'אוקטובר', 'נובמבר', 'דצמבר' );
		$en = array( 1 => 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December' );
		$m = (int) $p[1];
		return ( 'en' === $lang ? ( $en[ $m ] ?? $p[1] ) : ( $he[ $m ] ?? $p[1] ) ) . ' ' . $p[0];
	}

	function nadlan_mm_nf( $n, $dec = 0 ) { return number_format( (float) $n, $dec ); }

	/** One or two plain sentences for the quick calculator's summary (readers without scripts, search engines, AI answers). */
	function nadlan_mm_quick_summary() {
		$d = nadlan_mm_data();
		if ( ! $d ) { return ''; }
		$i = count( $d['by_bank']['months'] ) - 1; $ym = $d['by_bank']['months'][ $i ];
		$p25 = nadlan_mm_pay( $d, 'system', $i ); $p30 = nadlan_mm_pay( $d, 'system', $i, 1000000, 30 ); $p20 = nadlan_mm_pay( $d, 'system', $i, 1000000, 20 );
		$irr = (float) ( $d['by_bank']['rate']['system']['irr'][ $i ] ?? 0 );
		return '<p class="nli__sum">משכנתא של <bdi>1,000,000 ₪</bdi> בתמהיל ובריביות הממוצעים של כל הבנקים ב' . esc_html( nadlan_mm_month( $ym ) )
			. ': ההחזר החודשי הראשון <bdi>' . nadlan_mm_nf( $p25 ) . ' ₪</bdi> ל־25 שנה, <bdi>' . nadlan_mm_nf( $p20 ) . ' ₪</bdi> ל־20 שנה ו־<bdi>' . nadlan_mm_nf( $p30 ) . ' ₪</bdi> ל־30 שנה (לוח שפיצר).'
			. ' הריבית הכוללת החזויה במערכת: <bdi>' . nadlan_mm_nf( $irr, 2 ) . '%</bdi>. מקור: בנק ישראל, ריביות ממוצעות במשכנתאות חדשות לפי בנק.</p>';
	}

	/** The section itself. */
	function nadlan_mm_render( $lang = 'he' ) {
		$d = nadlan_mm_data();
		if ( ! $d ) { return ''; }
		$bb = $d['by_bank']; $i = count( $bb['months'] ) - 1; $j = $i - 12; $ym = $bb['months'][ $i ]; $yp = $j >= 0 ? $bb['months'][ $j ] : '';
		$mon = nadlan_mm_month( $ym ); $mon_p = $yp ? nadlan_mm_month( $yp ) : '';
		$irr = function ( $b, $k ) use ( $bb ) { return (float) ( $bb['rate'][ $b ]['irr'][ $k ] ?? 0 ); };
		$pay_now = nadlan_mm_pay( $d, 'system', $i ); $pay_prev = $j >= 0 ? nadlan_mm_pay( $d, 'system', $j ) : 0;
		$names = array(); foreach ( (array) $bb['banks'] as $b ) { $names[ $b['k'] ] = $b['he']; }
		$names['system'] = 'כל הבנקים';
		$big5 = array( 'hapoalim', 'leumi', 'discount', 'mizrahi', 'fibi' );
		$lo = ''; $hi = ''; foreach ( $big5 as $b ) { if ( '' === $lo || $irr( $b, $i ) < $irr( $lo, $i ) ) { $lo = $b; } if ( '' === $hi || $irr( $b, $i ) > $irr( $hi, $i ) ) { $hi = $b; } }
		$pr_now = (float) ( $bb['mix']['system']['prime'][ $i ] ?? 0 ); $pr_prev = $j >= 0 ? (float) ( $bb['mix']['system']['prime'][ $j ] ?? 0 ) : 0;
		$f = $d['flows'] ?? array(); $fi = isset( $f['months'] ) ? count( $f['months'] ) - 1 : -1; $fm = $fi >= 0 ? nadlan_mm_month( $f['months'][ $fi ] ) : '';
		$loans = $fi >= 0 ? (float) ( $f['series']['loans']['v'][ $fi ] ?? 0 ) : 0; $vol = $fi >= 0 ? (float) ( $f['series']['volume_k']['v'][ $fi ] ?? 0 ) * 1000 : 0;
		$ltv60 = 0; if ( $fi >= 0 && ! empty( $f['ltv']['bands'] ) ) { foreach ( $f['ltv']['bands'] as $k => $band ) { if ( (float) $band[0] >= 60 ) { $ltv60 += (float) ( $f['ltv']['share'][ $fi ][ $k ] ?? 0 ); } } }
		$ltv75 = 0; if ( $fi >= 0 && ! empty( $f['ltv']['bands'] ) ) { foreach ( $f['ltv']['bands'] as $k => $band ) { if ( (float) $band[0] >= 75 ) { $ltv75 += (float) ( $f['ltv']['share'][ $fi ][ $k ] ?? 0 ); } } }
		$s = $d['stock'] ?? array(); $si = isset( $s['months'] ) ? count( $s['months'] ) - 1 : -1;
		$stock = $si >= 0 ? (float) ( $s['series']['total_k']['v'][ $si ] ?? 0 ) * 1000 : 0; $count = $si >= 0 ? (float) ( $s['series']['count']['v'][ $si ] ?? 0 ) : 0;
		$arr = $si >= 0 && $stock > 0 ? (float) ( $s['series']['arrears90_k']['v'][ $si ] ?? 0 ) * 1000 / $stock * 100 : 0;
		$bdi = function ( $t ) { return '<bdi>' . $t . '</bdi>'; };

		$h  = '<section class="nlmm" id="mortgage-market" dir="rtl" lang="he" aria-labelledby="nlmm-h">';
		$h .= '<p class="nlmm__kick">נתוני בנק ישראל · מתעדכן בכל חודש</p>';
		$h .= '<h2 id="nlmm-h">שוק המשכנתאות, ' . esc_html( $mon ) . '</h2>';
		$h .= '<p class="nlmm__lead">ב' . esc_html( $mon ) . ' הריבית הכוללת החזויה על משכנתאות חדשות הייתה ' . $bdi( nadlan_mm_nf( $irr( 'system', $i ), 2 ) . '%' ) . ' בממוצע בכל הבנקים'
			. ( $mon_p ? ', מול ' . $bdi( nadlan_mm_nf( $irr( 'system', $j ), 2 ) . '%' ) . ' ב' . esc_html( $mon_p ) : '' ) . '. משכנתא של ' . $bdi( '1,000,000 ₪' ) . ' ל־25 שנה בתמהיל הממוצע עלתה '
			. $bdi( nadlan_mm_nf( $pay_now ) . ' ₪' ) . ' בחודש הראשון' . ( $pay_prev ? ( $pay_now <= $pay_prev ? ', ' . $bdi( nadlan_mm_nf( $pay_prev - $pay_now ) . ' ₪' ) . ' פחות משנה קודם' : ', ' . $bdi( nadlan_mm_nf( $pay_now - $pay_prev ) . ' ₪' ) . ' יותר משנה קודם' ) : '' )
			. '. מבין חמשת הבנקים הגדולים, הריבית הכוללת הנמוכה הייתה ב' . esc_html( $names[ $lo ] ?? $lo ) . ' (' . $bdi( nadlan_mm_nf( $irr( $lo, $i ), 2 ) . '%' ) . ') והגבוהה ב' . esc_html( $names[ $hi ] ?? $hi ) . ' (' . $bdi( nadlan_mm_nf( $irr( $hi, $i ), 2 ) . '%' ) . ').</p>';

		$k = array(
			array( nadlan_mm_nf( $pay_now ) . ' ₪', 'החזר ראשון על משכנתא של מיליון ₪ ל־25 שנה', 'תמהיל ממוצע, ' . $mon ),
			array( nadlan_mm_nf( $irr( 'system', $i ), 2 ) . '%', 'ריבית כוללת חזויה, כל הבנקים', $mon_p ? 'מול ' . nadlan_mm_nf( $irr( 'system', $j ), 2 ) . '% ב' . $mon_p : $mon ),
			array( nadlan_mm_nf( $pr_now, 1 ) . '%', 'חלק מסלול הפריים במשכנתאות החדשות', $mon_p ? 'מול ' . nadlan_mm_nf( $pr_prev, 1 ) . '% ב' . $mon_p : $mon ),
		);
		if ( $loans ) { $k[] = array( nadlan_mm_nf( $loans ), 'משכנתאות חדשות, ' . nadlan_mm_nf( $vol / 1e9, 2 ) . ' מיליארד ₪', $fm . ', הלוואה ממוצעת ' . nadlan_mm_nf( $vol / $loans ) . ' ₪' ); }
		if ( $ltv60 ) { $k[] = array( nadlan_mm_nf( $ltv60, 1 ) . '%', 'מהכסף החדש במימון של יותר מ־60%', $fm . ', מעל 75%: ' . nadlan_mm_nf( $ltv75, 2 ) . '%' ); }
		if ( $stock ) { $k[] = array( nadlan_mm_nf( $stock / 1e9, 1 ) . ' מיליארד ₪', 'יתרת המשכנתאות בישראל, ' . nadlan_mm_nf( $count ) . ' הלוואות', nadlan_mm_month( $s['months'][ $si ] ) . ', בפיגור 90 יום ומעלה: ' . nadlan_mm_nf( $arr, 2 ) . '%' ); }
		$h .= '<div class="nlmm__kpis">';
		foreach ( $k as $x ) { $h .= '<div class="nlmm__kpi"><b>' . $bdi( esc_html( $x[0] ) ) . '</b><span>' . esc_html( $x[1] ) . '</span><small>' . esc_html( $x[2] ) . '</small></div>'; }
		$h .= '</div>';

		// by bank
		$rows = array();
		foreach ( array_keys( $bb['rate'] ) as $b ) { $rows[] = array( $b, $irr( $b, $i ), nadlan_mm_pay( $d, $b, $i ) ); }
		usort( $rows, function ( $a, $b ) { return $a[1] <=> $b[1]; } );
		$h .= '<h3>ריבית משכנתא ממוצעת לפי בנק, ' . esc_html( $mon ) . '</h3>';
		$h .= '<div class="nlmm__scroll"><table class="nlmm__t"><caption>ריבית שנתית אפקטיבית במשכנתאות חדשות לפי בנק ומסלול, ' . esc_html( $mon ) . '</caption><thead><tr><th scope="col">בנק</th><th scope="col">ריבית כוללת חזויה</th><th scope="col">קבועה לא צמודה</th><th scope="col">מסלול הפריים</th><th scope="col">חלק הפריים</th><th scope="col">החזר ראשון על מיליון ל־25 שנה</th></tr></thead><tbody>';
		foreach ( $rows as $r ) {
			$b = $r[0]; $sys = 'system' === $b;
			$h .= '<tr' . ( $sys ? ' class="is-sys"' : '' ) . '><th scope="row">' . esc_html( $names[ $b ] ?? $b ) . '</th>'
				. '<td class="n' . ( $b === $lo ? ' is-key' : '' ) . '">' . $bdi( nadlan_mm_nf( $r[1], 2 ) . '%' ) . '</td>'
				. '<td class="n">' . $bdi( nadlan_mm_nf( $bb['rate'][ $b ]['fixed_nl'][ $i ] ?? 0, 2 ) . '%' ) . '</td>'
				. '<td class="n">' . $bdi( nadlan_mm_nf( $bb['rate'][ $b ]['prime'][ $i ] ?? 0, 2 ) . '%' ) . '</td>'
				. '<td class="n">' . $bdi( nadlan_mm_nf( $bb['mix'][ $b ]['prime'][ $i ] ?? 0, 1 ) . '%' ) . '</td>'
				. '<td class="n">' . $bdi( nadlan_mm_nf( $r[2] ) . ' ₪' ) . '</td></tr>';
		}
		$h .= '</tbody></table></div>';
		$gap = nadlan_mm_pay( $d, $hi, $i ) - nadlan_mm_pay( $d, $lo, $i );
		$h .= '<p class="nlmm__note">בין הבנק הזול לבנק היקר מבין חמשת הגדולים, לפי התמהיל הממוצע של כל אחד: ' . $bdi( nadlan_mm_nf( abs( $gap ) ) . ' ₪' ) . ' בחודש על כל מיליון. ממוצע של בנק תלוי בתמהיל ובלקוחות שלו ואינו הצעה; ההצעה שלכם נבדקת בכלי ההשוואה בראש הדף.</p>';

		// by city, 4 rooms
		$pay1m = nadlan_mm_pay( $d, 'system', $i ); $ltv = (float) ( $d['homes']['payments']['ltv'] ?? 0.75 );
		$med = $d['homes']['medians'] ?? array(); $cities = array();
		if ( ! empty( $med['il']['r4']['median'] ) ) { $cities['ישראל'] = $med['il']; }
		foreach ( (array) ( $med['city'] ?? array() ) as $c => $v ) { if ( ! empty( $v['r4']['median'] ) ) { $cities[ $c ] = $v; } }
		uasort( $cities, function ( $a, $b ) { return $a['r4']['median'] <=> $b['r4']['median']; } );
		if ( $cities ) {
			$h .= '<h3>כמה עולה משכנתא על דירת 4 חדרים בכל עיר</h3>';
			$h .= '<p>מחיר החציון של דירת 4 חדרים שנמכרה בעיר, משכנתא של ' . $bdi( nadlan_mm_nf( $ltv * 100 ) . '%' ) . ' ממנו ל־25 שנה, בתמהיל ובריביות הממוצעים של ' . esc_html( $mon ) . '.</p>';
			$h .= '<div class="nlmm__scroll"><table class="nlmm__t"><caption>החזר חודשי ראשון על דירת 4 חדרים במחיר החציון, לפי עיר</caption><thead><tr><th scope="col">עיר</th><th scope="col">מחיר חציוני, 4 חדרים</th><th scope="col">רבעון</th><th scope="col">משכנתא של ' . nadlan_mm_nf( $ltv * 100 ) . '%</th><th scope="col">החזר ראשון בחודש</th></tr></thead><tbody>';
			foreach ( $cities as $c => $v ) {
				$loan = $v['r4']['median'] * $ltv;
				$h .= '<tr><th scope="row">' . esc_html( $c ) . '</th><td class="n">' . $bdi( nadlan_mm_nf( $v['r4']['median'] ) . ' ₪' ) . '</td><td class="n">' . $bdi( esc_html( $v['r4']['quarter'] ?? '' ) ) . '</td><td class="n">' . $bdi( nadlan_mm_nf( $loan ) . ' ₪' ) . '</td><td class="n">' . $bdi( nadlan_mm_nf( $loan / 1000000 * $pay1m ) . ' ₪' ) . '</td></tr>';
			}
			$h .= '</tbody></table></div>';
		}
		$h .= '<p class="nlmm__src">מקורות: בנק ישראל, הפיקוח על הבנקים, השוואת ריביות בהלוואות לדיור לפי בנק (קובץ TamInt010, ריבית שנתית אפקטיבית ותמהיל המסלולים, ' . esc_html( $mon ) . '); בנק ישראל, סדרות המשכנתאות החדשות BIR_MRTG_99 (' . esc_html( $fm ) . ') ויתרת ההלוואות לדיור; רשות המסים, חציוני מחירי העסקאות לפי עיר ומספר חדרים. ההחזר מחושב בלוח שפיצר, חמשת המסלולים לפי חלקם בתמהיל, ריבית חודשית מהריבית האפקטיבית, ובמסלולים הצמודים בלי שינוי במדד. הריבית הכוללת החזויה היא ממוצע של כל ההלוואות בבנק לפי נוסחת הוראה 451, לא הצעה.</p>';
		$h .= '<style>.nlmm{margin:32px 0;font-family:"IBM Plex Sans Hebrew","IBM Plex Sans",system-ui,sans-serif;color:#12202A}.nlmm h2{margin:4px 0 8px;font-size:clamp(26px,5vw,34px);line-height:1.2;color:#1F4B5C!important}.nlmm h3{margin:28px 0 8px;font-size:20px;line-height:1.4;color:#12202A!important}.nlmm p{font-size:16px;line-height:1.75;color:#3E4C58;margin:0 0 12px}.nlmm__kick{font:500 13px/18px "IBM Plex Mono",ui-monospace,monospace!important;color:#5E6A75!important;margin:0!important}.nlmm__kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,150px),1fr));gap:10px;margin:16px 0}.nlmm__kpi{background:#fff;border:1px solid #D3DCE2;border-radius:6px;padding:14px;display:flex;flex-direction:column;gap:6px;min-width:0}.nlmm__kpi b{font:500 22px/28px "IBM Plex Mono",ui-monospace,monospace;color:#12202A;overflow-wrap:anywhere}@media (min-width:700px){.nlmm__kpi b{font-size:26px;line-height:32px}}.nlmm__kpi span{font-size:15px;line-height:22px;color:#3E4C58}.nlmm__kpi small{font:400 12px/16px "IBM Plex Mono",ui-monospace,monospace;color:#5E6A75}.nlmm__scroll{overflow-x:auto;background:#fff;border:1px solid #D3DCE2;border-radius:6px}.nlmm .nlmm__t{display:table!important;width:100%!important;border-collapse:collapse;margin:0;background:#fff!important;border:0!important}.nlmm .nlmm__t caption{caption-side:top;text-align:right;padding:10px 12px;font-size:13px;color:#5E6A75}.nlmm .nlmm__t thead{display:table-header-group!important}.nlmm .nlmm__t tbody{display:table-row-group!important}.nlmm .nlmm__t tr{display:table-row!important;background:#fff!important;border:0!important;box-shadow:none!important;margin:0!important;padding:0!important}.nlmm .nlmm__t th,.nlmm .nlmm__t td{display:table-cell!important;padding:10px 12px!important;border:0!important;border-bottom:1px solid #D3DCE2!important;text-align:right!important;font-size:14px!important;line-height:20px!important;color:#12202A!important;background:#fff!important;width:auto!important;white-space:nowrap}.nlmm .nlmm__t thead th{color:#3E4C58!important;font-weight:600!important;font-size:13px!important;border-bottom:1px solid #12202A!important}.nlmm .nlmm__t td.n{font-family:"IBM Plex Mono",ui-monospace,monospace!important}.nlmm .nlmm__t tr.is-sys th,.nlmm .nlmm__t tr.is-sys td{background:#E7EEF2!important;font-weight:600!important}.nlmm .nlmm__t td.is-key bdi{text-decoration:underline;text-decoration-color:#C42550;text-decoration-thickness:2px;text-underline-offset:5px}.nlmm__note,.nlmm__src{font-size:14px!important;line-height:1.7!important}.nlmm__src{font-family:"IBM Plex Mono",ui-monospace,monospace!important;font-size:12px!important;color:#5E6A75!important;border-top:1px solid #D3DCE2;padding-top:12px;margin-top:16px!important}</style>';
		return $h . '</section>';
	}
}

add_shortcode( 'nadlan_mortgage_market', function () { return nadlan_mm_render( 'he' ); } );

/* A Dataset JSON-LD for the tables, on a page that holds the shortcode. */
add_action( 'wp_head', function () {
	if ( ! is_singular() ) { return; }
	$p = get_post();
	if ( ! $p || false === strpos( (string) $p->post_content, '[nadlan_mortgage_market' ) ) { return; }
	$d = nadlan_mm_data();
	if ( ! $d ) { return; }
	$m = $d['by_bank']['months']; $url = get_permalink( $p ) . '#mortgage-market';
	$ld = array(
		'@context' => 'https://schema.org', '@type' => 'Dataset', '@id' => $url,
		'name' => 'שוק המשכנתאות בישראל: ריביות לפי בנק ומסלול, החזר חודשי ומשכנתאות חדשות',
		'description' => 'ריבית שנתית אפקטיבית במשכנתאות חדשות לפי בנק ומסלול, הריבית הכוללת החזויה (IRR) ותמהיל המסלולים של כל בנק, ההחזר החודשי הראשון על 1,000,000 ₪ ל־25 שנה לפי התמהיל הממוצע של כל בנק, משכנתאות חדשות לפי שיעור מימון, יתרת ההלוואות לדיור, וההחזר על דירת 4 חדרים במחיר החציון ב־25 ערים. מעובד מנתוני בנק ישראל ורשות המסים, מתעדכן בכל חודש.',
		'url' => $url, 'inLanguage' => 'he', 'isAccessibleForFree' => true,
		'temporalCoverage' => $m[0] . '/' . end( $m ),
		'spatialCoverage' => array( '@type' => 'Place', 'name' => 'Israel' ),
		'dateModified' => (string) ( $d['built'] ?? '' ),
		'variableMeasured' => array( 'ריבית קבועה לא צמודה', 'ריבית במסלול הפריים', 'ריבית משתנה לא צמודה', 'ריבית משתנה צמודה', 'ריבית קבועה צמודה', 'ריבית כוללת חזויה (IRR)', 'חלק כל מסלול בתמהיל', 'החזר חודשי ראשון', 'מספר המשכנתאות החדשות', 'היקף המשכנתאות החדשות', 'שיעור המימון' ),
		'isBasedOn' => array( 'https://www.boi.org.il/boi_files/Pikuah/TamInt010.xls', 'https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/data/dataflow/BOI.STATISTICS/BIR_MRTG_99/1.0/', 'https://data.nadlan.gov.il/' ),
		'creator' => array( '@type' => 'Organization', 'name' => 'nad-lan.co.il', 'url' => home_url( '/' ) ),
		'distribution' => array( array( '@type' => 'DataDownload', 'encodingFormat' => 'application/json', 'contentUrl' => plugins_url( 'assets/instruments/data/boi-mortgage.json', dirname( __DIR__ ) . '/nadlan-config.php' ) ) ),
	);
	echo "\n<script type=\"application/ld+json\" id=\"nadlan-mm-dataset\">" . wp_json_encode( $ld, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . "</script>\n";
}, 31 );
