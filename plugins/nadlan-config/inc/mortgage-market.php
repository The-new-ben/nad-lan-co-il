<?php
/**
 * nadlan-config - The mortgage market this month (1.72.587, HAD-675, Ben 5.11.2026: "the best mortgage calculator page in the world",
 * "numbers, prices, data", "make AI engines cite it").
 *
 * [nadlan_mortgage_market] prints, as plain HTML that Google and AI engines read without scripts, the latest Bank of Israel numbers on
 * new mortgages: six headline figures, the average rates and the forecast all-in rate (IRR) by bank with the first payment on
 * 1,000,000 ILS over 25 years at each bank's own average mix, and the first payment on the median 4-room home in 24 cities and nationally. Every
 * figure is computed here from assets/instruments/data/boi-mortgage.json at render time, so a new monthly data file updates the page
 * by itself. A Dataset JSON-LD describes the tables on any page that holds the shortcode.
 * Also: nadlan_mm_quick_summary() for the [nadlan_tool id="mquick"] plain-text summary (inc/instruments.php).
 * Sources (in the data file, with dates): Bank of Israel, Banking Supervision, TamInt010.xls (rates and mix by bank), SDMX
 * BIR_MRTG_99 (new mortgages by LTV band, volume, count), the housing-loan stock; Israel Tax Authority median deal prices.
 *
 * English twin (HAD-675, /en/mortgage-calculator/): [nadlan_mortgage_market lang="en"] (or the shortcode on an /en/ page) prints
 * the same section in English, LTR, en-US numbers, bank names from by_bank.banks[].en and English city names; the Dataset JSON-LD
 * is English (inLanguage en) on that page; nadlan_mm_quick_summary( 'en' ) is the English quick-calculator summary. The Hebrew
 * output is byte-identical to 1.72.587 (the Hebrew code path is unchanged; the style block moved into nadlan_mm_css()).
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

	/** The section's style block (moved here unchanged from nadlan_mm_render, 1.72.587); English: LTR alignment, the Latin face first. */
	function nadlan_mm_css( $lang = 'he' ) {
		$css = '<style>.nlmm{margin:32px 0;font-family:"IBM Plex Sans Hebrew","IBM Plex Sans",system-ui,sans-serif;color:#12202A}.nlmm h2{margin:4px 0 8px;font-size:clamp(26px,5vw,34px);line-height:1.2;color:#1F4B5C!important}.nlmm h3{margin:28px 0 8px;font-size:20px;line-height:1.4;color:#12202A!important}.nlmm p{font-size:16px;line-height:1.75;color:#3E4C58;margin:0 0 12px}.nlmm__kick{font:500 13px/18px "IBM Plex Mono",ui-monospace,monospace!important;color:#5E6A75!important;margin:0!important}.nlmm__kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,150px),1fr));gap:10px;margin:16px 0}.nlmm__kpi{background:#fff;border:1px solid #D3DCE2;border-radius:6px;padding:14px;display:flex;flex-direction:column;gap:6px;min-width:0}.nlmm__kpi b{font:500 22px/28px "IBM Plex Mono",ui-monospace,monospace;color:#12202A;overflow-wrap:anywhere}@media (min-width:700px){.nlmm__kpi b{font-size:26px;line-height:32px}}.nlmm__kpi span{font-size:15px;line-height:22px;color:#3E4C58}.nlmm__kpi small{font:400 12px/16px "IBM Plex Mono",ui-monospace,monospace;color:#5E6A75}.nlmm__scroll{overflow-x:auto;background:#fff;border:1px solid #D3DCE2;border-radius:6px}.nlmm .nlmm__t{display:table!important;width:100%!important;border-collapse:collapse;margin:0;background:#fff!important;border:0!important}.nlmm .nlmm__t caption{caption-side:top;text-align:right;padding:10px 12px;font-size:13px;color:#5E6A75}.nlmm .nlmm__t thead{display:table-header-group!important}.nlmm .nlmm__t tbody{display:table-row-group!important}.nlmm .nlmm__t tr{display:table-row!important;background:#fff!important;border:0!important;box-shadow:none!important;margin:0!important;padding:0!important}.nlmm .nlmm__t th,.nlmm .nlmm__t td{display:table-cell!important;padding:10px 12px!important;border:0!important;border-bottom:1px solid #D3DCE2!important;text-align:right!important;font-size:14px!important;line-height:20px!important;color:#12202A!important;background:#fff!important;width:auto!important;white-space:nowrap}.nlmm .nlmm__t thead th{color:#3E4C58!important;font-weight:600!important;font-size:13px!important;border-bottom:1px solid #12202A!important}.nlmm .nlmm__t td.n{font-family:"IBM Plex Mono",ui-monospace,monospace!important}.nlmm .nlmm__t tr.is-sys th,.nlmm .nlmm__t tr.is-sys td{background:#E7EEF2!important;font-weight:600!important}.nlmm .nlmm__t td.is-key bdi{text-decoration:underline;text-decoration-color:#C42550;text-decoration-thickness:2px;text-underline-offset:5px}.nlmm__note,.nlmm__src{font-size:14px!important;line-height:1.7!important}.nlmm__src{font-family:"IBM Plex Mono",ui-monospace,monospace!important;font-size:12px!important;color:#5E6A75!important;border-top:1px solid #D3DCE2;padding-top:12px;margin-top:16px!important}</style>';
		if ( 'en' === $lang ) {
			$css = str_replace( array( 'text-align:right', '"IBM Plex Sans Hebrew","IBM Plex Sans"' ), array( 'text-align:left', '"IBM Plex Sans","IBM Plex Sans Hebrew"' ), $css );
		}
		return $css;
	}

	/** One or two plain sentences for the quick calculator's summary (readers without scripts, search engines, AI answers). */
	function nadlan_mm_quick_summary( $lang = 'he' ) {
		$d = nadlan_mm_data();
		if ( ! $d ) { return ''; }
		if ( 'en' === $lang ) {
			$i = count( $d['by_bank']['months'] ) - 1; $ym = $d['by_bank']['months'][ $i ];
			$p25 = nadlan_mm_pay( $d, 'system', $i ); $p30 = nadlan_mm_pay( $d, 'system', $i, 1000000, 30 ); $p20 = nadlan_mm_pay( $d, 'system', $i, 1000000, 20 );
			$irr = (float) ( $d['by_bank']['rate']['system']['irr'][ $i ] ?? 0 );
			return '<p class="nli__sum">A <bdi>₪1,000,000</bdi> mortgage at the average track mix and rates of all banks in ' . esc_html( nadlan_mm_month( $ym, 'en' ) )
				. ': the first monthly payment is <bdi>₪' . nadlan_mm_nf( $p25 ) . '</bdi> over 25 years, <bdi>₪' . nadlan_mm_nf( $p20 ) . '</bdi> over 20 years and <bdi>₪' . nadlan_mm_nf( $p30 ) . '</bdi> over 30 years (Spitzer schedule).'
				. ' Forecast all-in rate (IRR) across the banking system: <bdi>' . nadlan_mm_nf( $irr, 2 ) . '%</bdi>. Source: Bank of Israel, average rates on new mortgages by bank.</p>';
		}
		$i = count( $d['by_bank']['months'] ) - 1; $ym = $d['by_bank']['months'][ $i ];
		$p25 = nadlan_mm_pay( $d, 'system', $i ); $p30 = nadlan_mm_pay( $d, 'system', $i, 1000000, 30 ); $p20 = nadlan_mm_pay( $d, 'system', $i, 1000000, 20 );
		$irr = (float) ( $d['by_bank']['rate']['system']['irr'][ $i ] ?? 0 );
		return '<p class="nli__sum">משכנתא של <bdi>1,000,000 ₪</bdi> בתמהיל ובריביות הממוצעים של כל הבנקים ב' . esc_html( nadlan_mm_month( $ym ) )
			. ': ההחזר החודשי הראשון <bdi>' . nadlan_mm_nf( $p25 ) . ' ₪</bdi> ל־25 שנה, <bdi>' . nadlan_mm_nf( $p20 ) . ' ₪</bdi> ל־20 שנה ו־<bdi>' . nadlan_mm_nf( $p30 ) . ' ₪</bdi> ל־30 שנה (לוח שפיצר).'
			. ' הריבית הכוללת החזויה במערכת: <bdi>' . nadlan_mm_nf( $irr, 2 ) . '%</bdi>. מקור: בנק ישראל, ריביות ממוצעות במשכנתאות חדשות לפי בנק.</p>';
	}

	/**
	 * 1.72.615 (HAD-675, Ben 9.11.2026: "the best in the world", authority plan): the first payment on 1,000,000 ILS over 25 years,
	 * month by month, at the average mix and rates of every bank (Bank of Israel TamInt010, the same nadlan_mm_pay() as the table above).
	 * Rows: one per month in by_bank.months, oldest first: array( 'ym', system, hapoalim, leumi, discount, mizrahi, fibi, mercantile, jerusalem, irr ).
	 */
	function nadlan_mm_million_rows( $d ) {
		$bb = $d['by_bank'] ?? array(); $out = array();
		if ( empty( $bb['months'] ) ) { return $out; }
		$keys = array( 'system', 'hapoalim', 'leumi', 'discount', 'mizrahi', 'fibi', 'mercantile', 'jerusalem' );
		foreach ( $bb['months'] as $k => $ym ) {
			$r = array( 'ym' => (string) $ym );
			foreach ( $keys as $b ) { $r[ $b ] = isset( $bb['rate'][ $b ] ) ? round( nadlan_mm_pay( $d, $b, $k ) ) : 0; }
			$r['irr'] = (float) ( $bb['rate']['system']['irr'][ $k ] ?? 0 );
			$out[] = $r;
		}
		return $out;
	}

	/** "9.26" style short month label for the chart axis. */
	function nadlan_mm_short_month( $ym ) {
		$p = explode( '-', (string) $ym );
		return 2 === count( $p ) ? (int) $p[1] . '.' . substr( $p[0], 2 ) : (string) $ym;
	}

	/** The plain sentence a journalist can quote, from the newest month (also the copy text of the cite box). */
	function nadlan_mm_million_sentence( $d, $names ) {
		$rows = nadlan_mm_million_rows( $d ); $n = count( $rows );
		if ( $n < 2 ) { return ''; }
		$now = $rows[ $n - 1 ]; $prev = $n > 12 ? $rows[ $n - 13 ] : null;
		$big5 = array( 'hapoalim', 'leumi', 'discount', 'mizrahi', 'fibi' ); $lo = 'hapoalim';
		foreach ( $big5 as $b ) { if ( $now[ $b ] > 0 && $now[ $b ] < $now[ $lo ] ) { $lo = $b; } }
		$s = 'משכנתא של מיליון שקל ל־25 שנה, בתמהיל ובריביות הממוצעים של כל הבנקים, עלתה ב' . nadlan_mm_month( $now['ym'] ) . ' ' . nadlan_mm_nf( $now['system'] ) . ' ₪ בחודש הראשון';
		if ( $prev ) {
			$diff = $now['system'] - $prev['system'];
			$s .= ', ' . nadlan_mm_nf( abs( $diff ) ) . ' ₪ ' . ( $diff <= 0 ? 'פחות' : 'יותר' ) . ' מאשר ב' . nadlan_mm_month( $prev['ym'] );
		}
		return $s . '. הזול מבין חמשת הבנקים הגדולים: ' . ( $names[ $lo ] ?? $lo ) . ', ' . nadlan_mm_nf( $now[ $lo ] ) . ' ₪.';
	}

	/** The block itself: answer, a line chart of every month, the last 13 months by bank, the cite box and the CSV. */
	function nadlan_mm_million_html( $d, $names ) {
		$rows = nadlan_mm_million_rows( $d ); $n = count( $rows );
		if ( $n < 3 ) { return ''; }
		$bdi = function ( $t ) { return '<bdi>' . $t . '</bdi>'; };
		$now = $rows[ $n - 1 ]; $prev = $n > 12 ? $rows[ $n - 13 ] : null;
		$hi = 0; $lo = 0; foreach ( $rows as $k => $r ) { if ( $r['system'] > $rows[ $hi ]['system'] ) { $hi = $k; } if ( $r['system'] < $rows[ $lo ]['system'] ) { $lo = $k; } }
		$csv = rest_url( 'nadlan/v1/mortgage-million' );
		$url = get_permalink() ? get_permalink() . '#million' : home_url( '/mortgage-calculator/#million' );
		$sent = nadlan_mm_million_sentence( $d, $names );

		$h  = '<div class="nlmm__mil" id="million">';
		$h .= '<h3>כמה עולה משכנתא של מיליון שקל, חודש אחר חודש</h3>';
		$h .= '<p>ב' . esc_html( nadlan_mm_month( $now['ym'] ) ) . ' ההחזר הראשון על משכנתא של ' . $bdi( '1,000,000 ₪' ) . ' ל־25 שנה, בתמהיל ובריביות הממוצעים של כל הבנקים, היה ' . $bdi( nadlan_mm_nf( $now['system'] ) . ' ₪' )
			. ( $prev ? '. שנה קודם, ב' . esc_html( nadlan_mm_month( $prev['ym'] ) ) . ': ' . $bdi( nadlan_mm_nf( $prev['system'] ) . ' ₪' ) : '' )
			. '. הגבוה ב־' . $n . ' החודשים שבטבלה: ' . $bdi( nadlan_mm_nf( $rows[ $hi ]['system'] ) . ' ₪' ) . ' ב' . esc_html( nadlan_mm_month( $rows[ $hi ]['ym'] ) )
			. ', והנמוך: ' . $bdi( nadlan_mm_nf( $rows[ $lo ]['system'] ) . ' ₪' ) . ' ב' . esc_html( nadlan_mm_month( $rows[ $lo ]['ym'] ) ) . '.</p>';

		// line chart, time runs left to right as in Bank of Israel charts; the y axis is padded 40 ILS each side
		$w = 640; $hgt = 200; $pl = 66; $pr = 14; $pt = 22; $pb = 30;
		$vals = array_map( function ( $r ) { return $r['system']; }, $rows );
		$ymin = floor( ( min( $vals ) - 40 ) / 50 ) * 50; $ymax = ceil( ( max( $vals ) + 40 ) / 50 ) * 50; if ( $ymax <= $ymin ) { $ymax = $ymin + 100; }
		$x = function ( $k ) use ( $n, $w, $pl, $pr ) { return round( $pl + ( $w - $pl - $pr ) * $k / max( 1, $n - 1 ), 1 ); };
		$y = function ( $v ) use ( $ymin, $ymax, $hgt, $pt, $pb ) { return round( $pt + ( $hgt - $pt - $pb ) * ( $ymax - $v ) / ( $ymax - $ymin ), 1 ); };
		$pts = array(); foreach ( $rows as $k => $r ) { $pts[] = $x( $k ) . ',' . $y( $r['system'] ); }
		$lbl = 'קו: ההחזר הראשון על מיליון ₪ ל־25 שנה בתמהיל הממוצע של כל הבנקים, מ' . nadlan_mm_month( $rows[0]['ym'] ) . ' עד ' . nadlan_mm_month( $now['ym'] ) . ', בין ' . nadlan_mm_nf( $rows[ $lo ]['system'] ) . ' ל־' . nadlan_mm_nf( $rows[ $hi ]['system'] ) . ' ₪';
		$h .= '<figure class="nlmm__fig"><svg viewBox="0 0 ' . $w . ' ' . $hgt . '" width="' . $w . '" height="' . $hgt . '" role="img" aria-label="' . esc_attr( $lbl ) . '" dir="ltr">';
		for ( $g = $ymin; $g <= $ymax; $g += ( $ymax - $ymin > 300 ? 100 : 50 ) ) {
			$h .= '<line x1="' . $pl . '" x2="' . ( $w - $pr ) . '" y1="' . $y( $g ) . '" y2="' . $y( $g ) . '" class="g"/><text x="' . ( $pl - 6 ) . '" y="' . ( $y( $g ) + 4 ) . '" class="ya">' . nadlan_mm_nf( $g ) . '</text>';
		}
		foreach ( $rows as $k => $r ) {
			if ( 0 === $k % 3 || $k === $n - 1 ) { $h .= '<text x="' . $x( $k ) . '" y="' . ( $hgt - 8 ) . '" class="xa' . ( 0 === $k % 6 || $k === $n - 1 ? ' x6' : '' ) . ( $k === $n - 1 ? ' xe' : '' ) . '">' . esc_html( nadlan_mm_short_month( $r['ym'] ) ) . '</text>'; }
		}
		$h .= '<polyline points="' . implode( ' ', $pts ) . '" class="ln"/>';
		foreach ( array_unique( array( $hi, $lo, $n - 1 ) ) as $k ) {
			$under = ( $k === $lo && $k !== $n - 1 && $n - 1 - $k <= 3 );  // a low next to the last point: its label goes under the point
			$h .= '<circle cx="' . $x( $k ) . '" cy="' . $y( $rows[ $k ]['system'] ) . '" r="4" class="pt"/><text x="' . $x( $k ) . '" y="' . ( $y( $rows[ $k ]['system'] ) + ( $under ? 24 : -10 ) ) . '" class="pv' . ( $k === $n - 1 ? ' pe' : '' ) . '">' . nadlan_mm_nf( $rows[ $k ]['system'] ) . '</text>';
		}
		$h .= '</svg><figcaption>ההחזר החודשי הראשון על ' . $bdi( '1,000,000 ₪' ) . ' ל־25 שנה, לוח שפיצר, בתמהיל ובריביות הממוצעים של כל הבנקים בכל חודש. חישוב שלנו מנתוני בנק ישראל.</figcaption></figure>';

		// the last 13 months by bank
		$cols = array( 'system', 'hapoalim', 'leumi', 'discount', 'mizrahi', 'fibi' );
		$h .= '<div class="nlmm__scroll"><table class="nlmm__t"><caption>ההחזר הראשון על מיליון ₪ ל־25 שנה, לפי חודש ובנק, בתמהיל הממוצע של כל בנק</caption><thead><tr><th scope="col">חודש</th>';
		foreach ( $cols as $b ) { $h .= '<th scope="col">' . esc_html( $names[ $b ] ?? $b ) . '</th>'; }
		$h .= '<th scope="col">שינוי מהחודש הקודם</th></tr></thead><tbody>';
		for ( $k = $n - 1; $k >= max( 0, $n - 13 ); $k-- ) {
			$r = $rows[ $k ]; $ch = $k > 0 ? $r['system'] - $rows[ $k - 1 ]['system'] : 0;
			$h .= '<tr' . ( $k === $n - 1 ? ' class="is-sys"' : '' ) . '><th scope="row">' . esc_html( nadlan_mm_month( $r['ym'] ) ) . '</th>';
			foreach ( $cols as $b ) { $h .= '<td class="n">' . $bdi( nadlan_mm_nf( $r[ $b ] ) . ' ₪' ) . '</td>'; }
			$h .= '<td class="n">' . ( $k > 0 ? $bdi( ( $ch > 0 ? '+' : ( $ch < 0 ? '−' : '' ) ) . nadlan_mm_nf( abs( $ch ) ) . ' ₪' ) : '' ) . '</td></tr>';
		}
		$h .= '</tbody></table></div>';

		// cite box: the reader copies the sentence; the CSV holds every month and every bank
		$cite = $sent . ' מקור: נדל״ן (nad-lan.co.il), לפי נתוני בנק ישראל. ' . $url;
		$h .= '<div class="nlmm__cite"><p class="nlmm__cite-h">לציטוט</p><blockquote><p>' . esc_html( $sent ) . '</p></blockquote>'
			. '<p class="nlmm__cite-src">מקור: נדל״ן (nad-lan.co.il), לפי נתוני בנק ישראל, השוואת ריביות בהלוואות לדיור לפי בנק. הנתון מתעדכן בכל חודש, כשבנק ישראל מפרסם את הקובץ, בסביבות ה־20 בחודש.</p>'
			. '<p class="nlmm__cite-act"><button type="button" class="nlmm__copy" data-copy="' . esc_attr( $cite ) . '">העתקת הציטוט</button> <a class="nlmm__csv" href="' . esc_url( $csv ) . '">הורדת כל החודשים (CSV)</a></p></div>';
		$h .= '<script>(function(){if(window.nlmmCopy)return;window.nlmmCopy=1;document.addEventListener("click",function(e){var b=e.target.closest&&e.target.closest(".nlmm__copy");if(!b)return;var t=b.getAttribute("data-copy");var done=function(){var o=b.textContent;b.textContent="הועתק";setTimeout(function(){b.textContent=o;},2000);};var old=function(){var a=document.createElement("textarea");a.value=t;a.setAttribute("readonly","");a.style.position="fixed";a.style.opacity="0";document.body.appendChild(a);a.select();try{if(document.execCommand("copy")){done();}}catch(x){}a.remove();};if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(done,old);}else{old();}});})();</script>';
		return $h . '</div>';
	}

	/** The CSS for the block (appended to the section style). */
	function nadlan_mm_million_css() {
		return '<style>.nlmm__mil{margin:28px 0 0}.nlmm__fig{margin:12px 0;background:#fff;border:1px solid #D3DCE2;border-radius:6px;padding:10px 10px 6px}.nlmm__fig svg{display:block;width:100%;height:auto;aspect-ratio:640/200;direction:ltr}.nlmm__fig svg text{direction:ltr;unicode-bidi:plaintext}'
			. '.nlmm__fig .g{stroke:#E3E9ED;stroke-width:1}.nlmm__fig .ln{fill:none;stroke:#1F4B5C;stroke-width:2.5;stroke-linejoin:round}.nlmm__fig .pt{fill:#fff;stroke:#1F4B5C;stroke-width:2}'
			. '.nlmm__fig text{font:500 12px "IBM Plex Mono",ui-monospace,monospace;fill:#5E6A75}.nlmm__fig .ya{text-anchor:end}.nlmm__fig .xa{text-anchor:middle}.nlmm__fig .xa.xe{text-anchor:end}.nlmm__fig .pv{text-anchor:middle;fill:#12202A;font-size:13px}.nlmm__fig .pv.pe{text-anchor:end}@media (max-width:600px){.nlmm__fig text{font-size:20px}.nlmm__fig .pv{font-size:22px}.nlmm__fig .xa:not(.x6){display:none}}'
			. '.nlmm__fig figcaption{font-size:13px;line-height:1.5;color:#5E6A75;margin:6px 2px 0}'
			. '.nlmm__cite{margin:14px 0 0;border:1px solid #D3DCE2;border-inline-start:4px solid #2F6F86;border-radius:6px;background:#fff;padding:14px 16px}'
			. '.nlmm__cite-h{font:500 13px/18px "IBM Plex Mono",ui-monospace,monospace!important;color:#5E6A75!important;margin:0 0 6px!important}'
			. '.nlmm__cite blockquote{margin:0;padding:0;border:0}.nlmm__cite blockquote p{font-size:17px!important;line-height:1.7!important;color:#12202A!important;margin:0 0 8px!important}'
			. '.nlmm__cite-src{font-size:13px!important;line-height:1.5!important;color:#5E6A75!important}'
			. '.nlmm__cite-act{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:8px 0 0!important}'
			. 'html body .nlmm .nlmm__copy{min-height:44px;padding:0 16px;border:1px solid #2F6F86;background:#2F6F86;color:#fff!important;border-radius:6px;font:500 15px "IBM Plex Sans Hebrew",system-ui,sans-serif;cursor:pointer}'
			. 'html body .nlmm a.nlmm__csv{display:inline-flex;align-items:center;min-height:44px;padding:0 14px;border:1px solid #D3DCE2;border-radius:6px;color:#1F4B5C!important;text-decoration:none;font-weight:500}'
			. '.nlmm__copy:focus-visible,.nlmm__csv:focus-visible{outline:3px solid #12202A;outline-offset:2px}</style>';
	}

	/** CSV of every month and bank (BOM first, so Excel opens Hebrew correctly). */
	function nadlan_mm_million_csv() {
		$d = nadlan_mm_data(); $rows = $d ? nadlan_mm_million_rows( $d ) : array();
		$names = array(); foreach ( (array) ( $d['by_bank']['banks'] ?? array() ) as $b ) { $names[ $b['k'] ] = $b['he']; }
		$names['system'] = 'כל הבנקים';
		$keys = array( 'system', 'hapoalim', 'leumi', 'discount', 'mizrahi', 'fibi', 'mercantile', 'jerusalem' );
		$q = function ( $s ) { return '"' . str_replace( '"', '""', (string) $s ) . '"'; };
		$out = "\xEF\xBB\xBF" . $q( 'חודש' );
		foreach ( $keys as $b ) { $out .= ',' . $q( 'החזר ראשון על מיליון ל־25 שנה, ' . ( $names[ $b ] ?? $b ) . ' (₪)' ); }
		$out .= ',' . $q( 'ריבית כוללת חזויה, כל הבנקים (%)' ) . "\r\n";
		foreach ( $rows as $r ) {
			$out .= $q( $r['ym'] );
			foreach ( $keys as $b ) { $out .= ',' . (int) $r[ $b ]; }
			$out .= ',' . number_format( $r['irr'], 2, '.', '' ) . "\r\n";
		}
		$out .= $q( 'מקור: נדל״ן (nad-lan.co.il), חישוב לוח שפיצר לפי התמהיל והריבית האפקטיבית הממוצעים של כל בנק, מתוך בנק ישראל, השוואת ריביות בהלוואות לדיור (TamInt010). ממוצע ואינו הצעה.' ) . "\r\n";
		return $out;
	}

	/** The section itself. */
	function nadlan_mm_render( $lang = 'he' ) {
		if ( 'en' === $lang ) { return nadlan_mm_render_en(); }
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
		$h .= nadlan_mm_million_html( $d, $names );  // 1.72.615 (HAD-675): the month-by-month million series, cite box, CSV

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
		$h .= nadlan_mm_css() . nadlan_mm_million_css();
		return $h . '</section>';
	}

	/** English city names for the Tax Authority medians (keys are the Hebrew names in the data file); unknown names stay Hebrew. */
	function nadlan_mm_city_en( $c ) {
		$m = array(
			'ישראל' => 'All of Israel', 'אילת' => 'Eilat', 'אשדוד' => 'Ashdod', 'אשקלון' => 'Ashkelon', 'באר שבע' => 'Beersheba', 'בני ברק' => 'Bnei Brak',
			'בת ים' => 'Bat Yam', 'גבעתיים' => 'Givatayim', 'הוד השרון' => 'Hod HaSharon', 'הרצליה' => 'Herzliya', 'חולון' => 'Holon', 'חיפה' => 'Haifa',
			'יבנה' => 'Yavne', 'ירושלים' => 'Jerusalem', 'כפר סבא' => 'Kfar Saba', 'מודיעין מכבים רעות' => "Modi'in-Maccabim-Re'ut", 'נתניה' => 'Netanya',
			'פתח תקווה' => 'Petah Tikva', 'קריית אונו' => 'Kiryat Ono', 'ראשון לציון' => 'Rishon LeZion', 'רחובות' => 'Rehovot', 'רמת גן' => 'Ramat Gan',
			'רמת השרון' => 'Ramat HaSharon', 'רעננה' => "Ra'anana", 'תל אביב יפו' => 'Tel Aviv-Yafo',
		);
		return isset( $m[ $c ] ) ? esc_html( $m[ $c ] ) : '<span lang="he" dir="rtl">' . esc_html( $c ) . '</span>';
	}

	/** The data's quarter label "4-6.2026" as "Q2 2026"; anything else unchanged. */
	function nadlan_mm_quarter_en( $q ) {
		$q2 = array( '1-3' => 'Q1', '4-6' => 'Q2', '7-9' => 'Q3', '10-12' => 'Q4' );
		$p  = explode( '.', (string) $q );
		return ( 2 === count( $p ) && isset( $q2[ $p[0] ] ) ) ? $q2[ $p[0] ] . ' ' . $p[1] : (string) $q;
	}

	/** The section in English (the /en/ twin): the same data, the same math and the same order as the Hebrew one, LTR. */
	function nadlan_mm_render_en() {
		$d = nadlan_mm_data();
		if ( ! $d ) { return ''; }
		$bb = $d['by_bank']; $i = count( $bb['months'] ) - 1; $j = $i - 12; $ym = $bb['months'][ $i ]; $yp = $j >= 0 ? $bb['months'][ $j ] : '';
		$mon = nadlan_mm_month( $ym, 'en' ); $mon_p = $yp ? nadlan_mm_month( $yp, 'en' ) : '';
		$irr = function ( $b, $k ) use ( $bb ) { return (float) ( $bb['rate'][ $b ]['irr'][ $k ] ?? 0 ); };
		$pay_now = nadlan_mm_pay( $d, 'system', $i ); $pay_prev = $j >= 0 ? nadlan_mm_pay( $d, 'system', $j ) : 0;
		$names = array(); foreach ( (array) $bb['banks'] as $b ) { $names[ $b['k'] ] = ! empty( $b['en'] ) ? $b['en'] : $b['k']; }
		$names['system'] = 'All banks';
		$big5 = array( 'hapoalim', 'leumi', 'discount', 'mizrahi', 'fibi' );
		$lo = ''; $hi = ''; foreach ( $big5 as $b ) { if ( '' === $lo || $irr( $b, $i ) < $irr( $lo, $i ) ) { $lo = $b; } if ( '' === $hi || $irr( $b, $i ) > $irr( $hi, $i ) ) { $hi = $b; } }
		$pr_now = (float) ( $bb['mix']['system']['prime'][ $i ] ?? 0 ); $pr_prev = $j >= 0 ? (float) ( $bb['mix']['system']['prime'][ $j ] ?? 0 ) : 0;
		$f = $d['flows'] ?? array(); $fi = isset( $f['months'] ) ? count( $f['months'] ) - 1 : -1; $fm = $fi >= 0 ? nadlan_mm_month( $f['months'][ $fi ], 'en' ) : '';
		$loans = $fi >= 0 ? (float) ( $f['series']['loans']['v'][ $fi ] ?? 0 ) : 0; $vol = $fi >= 0 ? (float) ( $f['series']['volume_k']['v'][ $fi ] ?? 0 ) * 1000 : 0;
		$ltv60 = 0; if ( $fi >= 0 && ! empty( $f['ltv']['bands'] ) ) { foreach ( $f['ltv']['bands'] as $k => $band ) { if ( (float) $band[0] >= 60 ) { $ltv60 += (float) ( $f['ltv']['share'][ $fi ][ $k ] ?? 0 ); } } }
		$ltv75 = 0; if ( $fi >= 0 && ! empty( $f['ltv']['bands'] ) ) { foreach ( $f['ltv']['bands'] as $k => $band ) { if ( (float) $band[0] >= 75 ) { $ltv75 += (float) ( $f['ltv']['share'][ $fi ][ $k ] ?? 0 ); } } }
		$s = $d['stock'] ?? array(); $si = isset( $s['months'] ) ? count( $s['months'] ) - 1 : -1;
		$stock = $si >= 0 ? (float) ( $s['series']['total_k']['v'][ $si ] ?? 0 ) * 1000 : 0; $count = $si >= 0 ? (float) ( $s['series']['count']['v'][ $si ] ?? 0 ) : 0;
		$arr = $si >= 0 && $stock > 0 ? (float) ( $s['series']['arrears90_k']['v'][ $si ] ?? 0 ) * 1000 / $stock * 100 : 0;
		$bdi = function ( $t ) { return '<bdi>' . $t . '</bdi>'; };
		$ils = function ( $n ) { return '₪' . nadlan_mm_nf( $n ); };

		$h  = '<section class="nlmm" id="mortgage-market" dir="ltr" lang="en" aria-labelledby="nlmm-h">';
		$h .= '<p class="nlmm__kick">Bank of Israel data · updated every month</p>';
		$h .= '<h2 id="nlmm-h">Israel mortgage rates and payments, ' . esc_html( $mon ) . '</h2>';
		$h .= '<p class="nlmm__lead">In ' . esc_html( $mon ) . ' the forecast all-in rate (IRR) on new mortgages averaged ' . $bdi( nadlan_mm_nf( $irr( 'system', $i ), 2 ) . '%' ) . ' across all banks'
			. ( $mon_p ? ', against ' . $bdi( nadlan_mm_nf( $irr( 'system', $j ), 2 ) . '%' ) . ' in ' . esc_html( $mon_p ) : '' ) . '. A ' . $bdi( '₪1,000,000' ) . ' mortgage over 25 years at the average track mix cost '
			. $bdi( $ils( $pay_now ) ) . ' in its first month' . ( $pay_prev ? ( $pay_now <= $pay_prev ? ', ' . $bdi( $ils( $pay_prev - $pay_now ) ) . ' less than a year earlier' : ', ' . $bdi( $ils( $pay_now - $pay_prev ) ) . ' more than a year earlier' ) : '' )
			. '. Among the five largest banks, the lowest all-in rate was ' . $bdi( nadlan_mm_nf( $irr( $lo, $i ), 2 ) . '%' ) . ' at ' . esc_html( $names[ $lo ] ?? $lo ) . ' and the highest was ' . $bdi( nadlan_mm_nf( $irr( $hi, $i ), 2 ) . '%' ) . ' at ' . esc_html( $names[ $hi ] ?? $hi ) . '.</p>';

		$k = array(
			array( $ils( $pay_now ), 'First payment on a ₪1 million mortgage over 25 years', 'Average mix, ' . $mon ),
			array( nadlan_mm_nf( $irr( 'system', $i ), 2 ) . '%', 'Forecast all-in rate (IRR), all banks', $mon_p ? 'vs ' . nadlan_mm_nf( $irr( 'system', $j ), 2 ) . '% in ' . $mon_p : $mon ),
			array( nadlan_mm_nf( $pr_now, 1 ) . '%', 'Prime track share of new mortgages', $mon_p ? 'vs ' . nadlan_mm_nf( $pr_prev, 1 ) . '% in ' . $mon_p : $mon ),
		);
		if ( $loans ) { $k[] = array( nadlan_mm_nf( $loans ), 'New mortgages, ₪' . nadlan_mm_nf( $vol / 1e9, 2 ) . ' billion', $fm . ', average loan ' . $ils( $vol / $loans ) ); }
		if ( $ltv60 ) { $k[] = array( nadlan_mm_nf( $ltv60, 1 ) . '%', 'of new mortgage money at a loan to value above 60%', $fm . ', above 75%: ' . nadlan_mm_nf( $ltv75, 2 ) . '%' ); }
		if ( $stock ) { $k[] = array( '₪' . nadlan_mm_nf( $stock / 1e9, 1 ) . ' billion', 'Outstanding mortgages in Israel, ' . nadlan_mm_nf( $count ) . ' loans', nadlan_mm_month( $s['months'][ $si ], 'en' ) . ', 90 days or more in arrears: ' . nadlan_mm_nf( $arr, 2 ) . '%' ); }
		$h .= '<div class="nlmm__kpis">';
		foreach ( $k as $x ) { $h .= '<div class="nlmm__kpi"><b>' . $bdi( esc_html( $x[0] ) ) . '</b><span>' . esc_html( $x[1] ) . '</span><small>' . esc_html( $x[2] ) . '</small></div>'; }
		$h .= '</div>';

		// by bank
		$rows = array();
		foreach ( array_keys( $bb['rate'] ) as $b ) { $rows[] = array( $b, $irr( $b, $i ), nadlan_mm_pay( $d, $b, $i ) ); }
		usort( $rows, function ( $a, $b ) { return $a[1] <=> $b[1]; } );
		$h .= '<h3>Average mortgage rate by bank, ' . esc_html( $mon ) . '</h3>';
		$h .= '<div class="nlmm__scroll"><table class="nlmm__t"><caption>Effective annual rate on new mortgages by bank and track, ' . esc_html( $mon ) . '</caption><thead><tr><th scope="col">Bank</th><th scope="col">Forecast all-in rate (IRR)</th><th scope="col">Fixed, not linked</th><th scope="col">Prime track</th><th scope="col">Prime share</th><th scope="col">First payment on ₪1M over 25 years</th></tr></thead><tbody>';
		foreach ( $rows as $r ) {
			$b = $r[0]; $sys = 'system' === $b;
			$h .= '<tr' . ( $sys ? ' class="is-sys"' : '' ) . '><th scope="row">' . esc_html( $names[ $b ] ?? $b ) . '</th>'
				. '<td class="n' . ( $b === $lo ? ' is-key' : '' ) . '">' . $bdi( nadlan_mm_nf( $r[1], 2 ) . '%' ) . '</td>'
				. '<td class="n">' . $bdi( nadlan_mm_nf( $bb['rate'][ $b ]['fixed_nl'][ $i ] ?? 0, 2 ) . '%' ) . '</td>'
				. '<td class="n">' . $bdi( nadlan_mm_nf( $bb['rate'][ $b ]['prime'][ $i ] ?? 0, 2 ) . '%' ) . '</td>'
				. '<td class="n">' . $bdi( nadlan_mm_nf( $bb['mix'][ $b ]['prime'][ $i ] ?? 0, 1 ) . '%' ) . '</td>'
				. '<td class="n">' . $bdi( $ils( $r[2] ) ) . '</td></tr>';
		}
		$h .= '</tbody></table></div>';
		$gap = nadlan_mm_pay( $d, $hi, $i ) - nadlan_mm_pay( $d, $lo, $i );
		$h .= '<p class="nlmm__note">Between the cheapest and the most expensive of the five largest banks, each at its own average mix: ' . $bdi( $ils( abs( $gap ) ) ) . ' a month on every million. A bank\'s average depends on its mix and its customers and is not an offer; the way to know is an approval in principle from several banks, compared on the three uniform baskets.</p>';

		// by city, 4 rooms
		$pay1m = nadlan_mm_pay( $d, 'system', $i ); $ltv = (float) ( $d['homes']['payments']['ltv'] ?? 0.75 );
		$med = $d['homes']['medians'] ?? array(); $cities = array();
		if ( ! empty( $med['il']['r4']['median'] ) ) { $cities['ישראל'] = $med['il']; }
		foreach ( (array) ( $med['city'] ?? array() ) as $c => $v ) { if ( ! empty( $v['r4']['median'] ) ) { $cities[ $c ] = $v; } }
		uasort( $cities, function ( $a, $b ) { return $a['r4']['median'] <=> $b['r4']['median']; } );
		if ( $cities ) {
			$h .= '<h3>What a mortgage on a 4-room home costs in each city</h3>';
			$h .= '<p>The median price of 4-room homes sold in the city, a ' . $bdi( nadlan_mm_nf( $ltv * 100 ) . '%' ) . ' mortgage on it over 25 years, at the average mix and rates of ' . esc_html( $mon ) . '.</p>';
			$h .= '<div class="nlmm__scroll"><table class="nlmm__t"><caption>First monthly payment on a 4-room home at the median price, by city</caption><thead><tr><th scope="col">City</th><th scope="col">Median price, 4 rooms</th><th scope="col">Quarter</th><th scope="col">' . nadlan_mm_nf( $ltv * 100 ) . '% mortgage</th><th scope="col">First monthly payment</th></tr></thead><tbody>';
			foreach ( $cities as $c => $v ) {
				$loan = $v['r4']['median'] * $ltv;
				$h .= '<tr><th scope="row">' . nadlan_mm_city_en( $c ) . '</th><td class="n">' . $bdi( $ils( $v['r4']['median'] ) ) . '</td><td class="n">' . $bdi( esc_html( nadlan_mm_quarter_en( $v['r4']['quarter'] ?? '' ) ) ) . '</td><td class="n">' . $bdi( $ils( $loan ) ) . '</td><td class="n">' . $bdi( $ils( $loan / 1000000 * $pay1m ) ) . '</td></tr>';
			}
			$h .= '</tbody></table></div>';
		}
		$h .= '<p class="nlmm__src">Sources: Bank of Israel, Banking Supervision, interest rate comparison for housing loans by bank (file TamInt010, effective annual rate and track mix, ' . esc_html( $mon ) . '); Bank of Israel, new mortgage series BIR_MRTG_99 (' . esc_html( $fm ) . ') and the housing-loan balance; Israel Tax Authority, median deal prices by city and number of rooms. The payment uses a Spitzer schedule: each of the five tracks by its share of the mix, a monthly rate from the effective rate, and CPI-linked tracks with the index unchanged. The forecast all-in rate is the average over all of a bank\'s loans under the Directive 451 formula, not an offer.</p>';
		$h .= nadlan_mm_css( 'en' );
		return $h . '</section>';
	}
}

/* [nadlan_mortgage_market] prints the Hebrew section; lang="en", or the shortcode on an /en/ page (inc/page-lang.php), the English one. */
add_shortcode( 'nadlan_mortgage_market', function ( $atts = array() ) {
	$a = shortcode_atts( array( 'lang' => '' ), $atts );
	$l = 'en' === $a['lang'] || ( '' === $a['lang'] && function_exists( 'nadlan_pglang_lang' ) && 'en' === nadlan_pglang_lang() ) ? 'en' : 'he';
	return nadlan_mm_render( $l );
} );

/* 1.72.615 (HAD-675): the million series as CSV, every month and bank, for readers, journalists and the Dataset distribution. */
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/mortgage-million', array(
		'methods' => 'GET', 'permission_callback' => '__return_true',
		'callback' => function () {
			$csv = nadlan_mm_million_csv();
			if ( ! headers_sent() ) {
				header( 'Content-Type: text/csv; charset=utf-8' );
				header( 'Content-Disposition: inline; filename="nadlan-mortgage-1m-by-month.csv"' );
				header( 'Cache-Control: public, max-age=3600' );
			}
			echo $csv;  // phpcs:ignore WordPress.Security.EscapeOutput -- CSV body, every cell quoted or numeric
			exit;
		},
	) );
} );

/* A Dataset JSON-LD for the tables, on a page that holds the shortcode. */
add_action( 'wp_head', function () {
	if ( ! is_singular() ) { return; }
	$p = get_post();
	if ( ! $p || false === strpos( (string) $p->post_content, '[nadlan_mortgage_market' ) ) { return; }
	$d = nadlan_mm_data();
	if ( ! $d ) { return; }
	$m = $d['by_bank']['months']; $url = get_permalink( $p ) . '#mortgage-market';
	// English twin: the same Dataset in English on the English page (the shortcode with lang="en", or any /en/ page)
	$en = false !== strpos( (string) $p->post_content, '[nadlan_mortgage_market lang="en"' ) || ( function_exists( 'nadlan_pglang_lang' ) && 'en' === nadlan_pglang_lang() );
	if ( $en ) {
		$ld = array(
			'@context' => 'https://schema.org', '@type' => 'Dataset', '@id' => $url,
			'name' => 'Israel mortgage market: rates by bank and track, monthly payments and new mortgages',
			'description' => 'Effective annual rates on new Israeli mortgages by bank and track, the forecast all-in rate (IRR) and track mix of each bank, the first monthly payment on ILS 1,000,000 over 25 years at each bank\'s average mix, new mortgages by loan-to-value band, the outstanding housing-loan balance, and the first payment on a median-priced 4-room home in 24 cities and nationwide. Processed from Bank of Israel and Israel Tax Authority data, updated every month.',
			'url' => $url, 'inLanguage' => 'en', 'isAccessibleForFree' => true,
			'temporalCoverage' => $m[0] . '/' . end( $m ),
			'spatialCoverage' => array( '@type' => 'Place', 'name' => 'Israel' ),
			'dateModified' => (string) ( $d['built'] ?? '' ),
			'variableMeasured' => array( 'Fixed rate, not linked', 'Prime track rate', 'Variable rate, not linked', 'Variable rate, CPI-linked', 'Fixed rate, CPI-linked', 'Forecast all-in rate (IRR)', 'Share of each track in the mix', 'First monthly payment', 'Number of new mortgages', 'Volume of new mortgages', 'Loan to value' ),
			'isBasedOn' => array( 'https://www.boi.org.il/boi_files/Pikuah/TamInt010.xls', 'https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/data/dataflow/BOI.STATISTICS/BIR_MRTG_99/1.0/', 'https://data.nadlan.gov.il/' ),
			'creator' => array( '@type' => 'Organization', 'name' => 'nad-lan.co.il', 'url' => home_url( '/' ) ),
			'distribution' => array( array( '@type' => 'DataDownload', 'encodingFormat' => 'application/json', 'contentUrl' => plugins_url( 'assets/instruments/data/boi-mortgage.json', dirname( __DIR__ ) . '/nadlan-config.php' ) ) ),
		);
		echo "\n<script type=\"application/ld+json\" id=\"nadlan-mm-dataset\">" . wp_json_encode( $ld, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . "</script>\n";
		return;
	}
	$ld = array(
		'@context' => 'https://schema.org', '@type' => 'Dataset', '@id' => $url,
		'name' => 'שוק המשכנתאות בישראל: ריביות לפי בנק ומסלול, החזר חודשי ומשכנתאות חדשות',
		'description' => 'ריבית שנתית אפקטיבית במשכנתאות חדשות לפי בנק ומסלול, הריבית הכוללת החזויה (IRR) ותמהיל המסלולים של כל בנק, ההחזר החודשי הראשון על 1,000,000 ₪ ל־25 שנה לפי התמהיל הממוצע של כל בנק, משכנתאות חדשות לפי שיעור מימון, יתרת ההלוואות לדיור, וההחזר על דירת 4 חדרים במחיר החציון ב־24 ערים ובממוצע הארצי. מעובד מנתוני בנק ישראל ורשות המסים, מתעדכן בכל חודש.',
		'url' => $url, 'inLanguage' => 'he', 'isAccessibleForFree' => true,
		'temporalCoverage' => $m[0] . '/' . end( $m ),
		'spatialCoverage' => array( '@type' => 'Place', 'name' => 'Israel' ),
		'dateModified' => (string) ( $d['built'] ?? '' ),
		'variableMeasured' => array( 'ריבית קבועה לא צמודה', 'ריבית במסלול הפריים', 'ריבית משתנה לא צמודה', 'ריבית משתנה צמודה', 'ריבית קבועה צמודה', 'ריבית כוללת חזויה (IRR)', 'חלק כל מסלול בתמהיל', 'החזר חודשי ראשון', 'מספר המשכנתאות החדשות', 'היקף המשכנתאות החדשות', 'שיעור המימון' ),
		'isBasedOn' => array( 'https://www.boi.org.il/boi_files/Pikuah/TamInt010.xls', 'https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/data/dataflow/BOI.STATISTICS/BIR_MRTG_99/1.0/', 'https://data.nadlan.gov.il/' ),
		'creator' => array( '@type' => 'Organization', 'name' => 'nad-lan.co.il', 'url' => home_url( '/' ) ),
		'distribution' => array( array( '@type' => 'DataDownload', 'encodingFormat' => 'application/json', 'contentUrl' => plugins_url( 'assets/instruments/data/boi-mortgage.json', dirname( __DIR__ ) . '/nadlan-config.php' ) ),
			array( '@type' => 'DataDownload', 'encodingFormat' => 'text/csv', 'name' => 'ההחזר הראשון על מיליון ₪ לפי חודש ובנק', 'contentUrl' => rest_url( 'nadlan/v1/mortgage-million' ) ) ),
	);
	echo "\n<script type=\"application/ld+json\" id=\"nadlan-mm-dataset\">" . wp_json_encode( $ld, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . "</script>\n";
	// 1.72.615 (HAD-675): the million series as its own Dataset, and the page's calculators as one WebApplication
	$rows = nadlan_mm_million_rows( $d ); $pg = get_permalink( $p );
	if ( count( $rows ) > 2 ) {
		$mil = array(
			'@context' => 'https://schema.org', '@type' => 'Dataset', '@id' => $pg . '#million',
			'name' => 'כמה עולה משכנתא של מיליון שקל, חודש אחר חודש',
			'description' => 'ההחזר החודשי הראשון על משכנתא של 1,000,000 ₪ ל־25 שנה, בלוח שפיצר, בתמהיל ובריביות האפקטיביות הממוצעים של כל הבנקים ושל כל בנק בנפרד, לכל חודש מ' . nadlan_mm_month( $rows[0]['ym'] ) . ' עד ' . nadlan_mm_month( end( $rows )['ym'] ) . '. חישוב של נדל״ן מנתוני בנק ישראל, מתעדכן בכל חודש.',
			'url' => $pg . '#million', 'inLanguage' => 'he', 'isAccessibleForFree' => true,
			'temporalCoverage' => $rows[0]['ym'] . '/' . end( $rows )['ym'], 'spatialCoverage' => array( '@type' => 'Place', 'name' => 'Israel' ),
			'dateModified' => (string) ( $d['built'] ?? '' ),
			'variableMeasured' => array( 'החזר חודשי ראשון על מיליון ₪ ל־25 שנה, כל הבנקים', 'החזר חודשי ראשון לפי בנק', 'ריבית כוללת חזויה (IRR)' ),
			'isBasedOn' => 'https://www.boi.org.il/boi_files/Pikuah/TamInt010.xls',
			'creator' => array( '@type' => 'Organization', 'name' => 'nad-lan.co.il', 'url' => home_url( '/' ) ),
			'distribution' => array( array( '@type' => 'DataDownload', 'encodingFormat' => 'text/csv', 'contentUrl' => rest_url( 'nadlan/v1/mortgage-million' ) ) ),
		);
		echo '<script type="application/ld+json" id="nadlan-mm-million">' . wp_json_encode( $mil, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . "</script>\n";
	}
	$feat = array();
	if ( function_exists( 'nadlan_nli_page_ids' ) && function_exists( 'nadlan_nli_tools' ) && function_exists( 'nadlan_nli_t' ) ) {
		$tools = nadlan_nli_tools();
		foreach ( (array) nadlan_nli_page_ids() as $tid ) { if ( isset( $tools[ $tid ] ) ) { $t = nadlan_nli_t( $tools[ $tid ], 'he' ); if ( ! empty( $t['name'] ) ) { $feat[] = $t['name']; } } }
	}
	if ( count( $feat ) >= 3 ) {
		$app = array(
			'@context' => 'https://schema.org', '@type' => 'WebApplication', '@id' => $pg . '#calculators',
			'name' => 'מחשבון משכנתא', 'url' => $pg, 'inLanguage' => 'he', 'applicationCategory' => 'FinanceApplication', 'operatingSystem' => 'Any',
			'browserRequirements' => 'Requires JavaScript', 'isAccessibleForFree' => true, 'offers' => array( '@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'ILS' ),
			'featureList' => array_values( array_unique( $feat ) ), 'dateModified' => (string) ( $d['built'] ?? '' ),
			'publisher' => array( '@type' => 'Organization', 'name' => 'nad-lan.co.il', 'url' => home_url( '/' ) ),
		);
		echo '<script type="application/ld+json" id="nadlan-mm-webapp">' . wp_json_encode( $app, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . "</script>\n";
	}
}, 31 );

/* 1.72.615 (HAD-675): phone speed on the pages that hold the market section: the H1 and text fonts are fetched first, so the
   first paint already has the final line breaks (CLS 0.179 -> 0.07 on a slow phone, scratchpad probe 9.11.2026). */
if ( ! function_exists( 'nadlan_mm_speed_page' ) ) {
	function nadlan_mm_speed_page() {
		static $on = null;
		if ( null !== $on ) { return $on; }
		$p = is_singular() ? get_post() : null;
		$on = $p && false !== strpos( (string) $p->post_content, '[nadlan_mortgage_market' );
		return $on;
	}

	/** The two Hebrew variable font files the first screen paints with (H1: Noto Serif Hebrew, text: Assistant). */
	function nadlan_mm_font_preload() {
		$urls = get_transient( 'nadlan_mm_font_preload_v3' );
		if ( is_array( $urls ) && 3 === count( $urls ) ) { return $urls; }
		$urls = array(  // read from Google with a phone browser on 9.11.2026
			'https://fonts.gstatic.com/s/notoserifhebrew/v30/k3k5o9MMPvpLmixYH7euCwmkS9DohjX1-kRyiqyBqIxnoLbD-VBM2jVkL3Lr.woff2',
			'https://fonts.gstatic.com/s/assistant/v24/2sDcZGJYnIjSi6H75xkzamW5Kb8VZBHR.woff2',
			'https://fonts.gstatic.com/s/assistant/v24/2sDcZGJYnIjSi6H75xkzaGW5Kb8VZA.woff2',
		);
		$ttl = DAY_IN_SECONDS;
		$res = wp_remote_get( 'https://fonts.googleapis.com/css2?family=Noto+Serif+Hebrew:wght@500;600;700&family=Assistant:wght@300;400;600;700&display=swap',
			array( 'timeout' => 3, 'user-agent' => 'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Mobile Safari/537.36' ) );  // phones and Mac get these files; Windows gets hinted ones
		if ( ! is_wp_error( $res ) && 200 === (int) wp_remote_retrieve_response_code( $res ) ) {
			$css = (string) wp_remote_retrieve_body( $res ); $found = array();
			foreach ( array( array( 'hebrew', 'Noto Serif Hebrew' ), array( 'hebrew', 'Assistant' ), array( 'latin', 'Assistant' ) ) as $sf ) {
				if ( preg_match( "#/\\* " . $sf[0] . " \\*/\\s*@font-face\\s*\\{[^}]*font-family:\\s*'" . preg_quote( $sf[1], '#' ) . "'[^}]*src:\\s*url\\((https://fonts\\.gstatic\\.com/[^)]+\\.woff2)\\)#", $css, $m ) ) { $found[] = $m[1]; }
			}
			if ( 3 === count( $found ) ) { $urls = $found; $ttl = WEEK_IN_SECONDS; }
		}
		set_transient( 'nadlan_mm_font_preload_v3', $urls, $ttl );
		return $urls;
	}

	add_action( 'wp_head', function () {
		if ( ! nadlan_mm_speed_page() ) { return; }
		echo '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>' . "\n";
		foreach ( nadlan_mm_font_preload() as $u ) { echo '<link rel="preload" href="' . esc_url( $u ) . '" as="font" type="font/woff2" media="(max-width: 600px)" crossorigin>' . "\n"; }
	}, 2 );

}
