<?php
/**
 * nadlan-config - THE BUYING HUB TOOLS (HAD-683, Ben 7.11.2026: "the best home-buying page in Israel and abroad"). Four instruments of one
 * family in assets/instruments/tools/buying.js (math in window.NLBH, tested by tools/instruments/test_buying_hub.js) on
 * /buying-apartment/ (page 9):
 *   bplan   "קניית דירה צעד אחר צעד לפי המצב שלך" (12 buyer statuses, type, stage: the rules that apply and a step plan that remembers)
 *   bequity "קניית דירה ללא הון עצמי" (equity sources and their monthly cost; the handover stress test of a low-down-payment offer)
 *   bladder "איך לקנות דירה בארץ עם 100 אלף..." (equity + status -> maximum price by the LTV rule -> cities and rooms that fit)
 *   boffer  "הצעת מחיר לרכישת דירה" (asking price against the median deals, neighbourhood share, an opening range with its basis)
 * Data: buying.json (content only) + ptax, nrm, zakaut, orechdin, boi-mortgage, cost, cbs-200010, prices-hub, value (all dated).
 * This file: the registry entries (filter nadlan_nli_tools), the plain server summaries with the real numbers (nadlan_bhub_summary,
 * the same math as buying.js), and the FAQPage of the page's "קניית דירה: השאלות שלא שואלים את עורך הדין" section.
 * The summary reaches the shortcode through the engine branch (one line in nadlan_nli_summary, see the release note) or, until that
 * line exists, through WordPress's own do_shortcode_tag filter; a marker keeps it from printing twice.
 * Loaded from the module list in nadlan-config.php ('buying-hub'); every function is guarded, so a rollback of this file is clean.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_bhub_tool_ids' ) ) {

	function nadlan_bhub_tool_ids() { return array( 'bplan', 'bequity', 'bladder', 'boffer' ); }

	add_filter( 'nadlan_nli_tools', function ( $tools ) {
		$tools['bplan'] = array( 'file' => 'buying', 'deps' => array( 'prices-common' ),
			'name' => 'קניית דירה צעד אחר צעד לפי המצב שלך', 'cat' => 'UtilitiesApplication', 'kicker' => 'התוכנית שלי לקניית דירה',
			'desc' => 'תוכנית אישית לקניית דירה: בוחרים אחד מ־12 מצבים (דירה ראשונה, יחידה, חלופית, שנייה, להשקעה, זוג צעיר, חיילים משוחררים, אנשי קבע, מילואים, עולים, תושבי חוץ, נכות), יד שנייה או מקבלן ואת השלב, ומקבלים את מדרגות מס הרכישה, שיעור המימון ותוספות הזכאות שחלים עליכם, עם המקור והתאריך, ואת הצעדים הבאים עם המדריך של כל צעד. ההתקדמות נשמרת בדפדפן.',
			'data' => array( 'buying.json', 'ptax.json', 'nrm.json', 'zakaut.json', 'orechdin.json' ),
			'related' => array( '/buying-apartment/buying-apartment-step-by-step/' => 'איך כדאי לקנות דירה', '/apartment-buying-checklist/' => 'בדיקות לפני קניית דירה', '/purchase-tax-calculator/' => 'מחשבון מס רכישה', '/real-estate-lawyer/' => 'עורך דין מקרקעין' ) );
		$tools['bequity'] = array( 'file' => 'buying', 'deps' => array( 'prices-common' ),
			'name' => 'קניית דירה ללא הון עצמי: מאיפה מגיע הכסף ומה הוא עולה', 'cat' => 'FinanceApplication', 'kicker' => 'מחשבון · מקורות ההון העצמי',
			'desc' => 'כמה הון עצמי צריך לדירה לפי המצב שלכם (שיעור המימון של בנק ישראל, מס רכישה ועורך דין), מאיפה אפשר להביא אותו (חסכונות, מתנה, שותפים, משכנתא על דירת ההורים, הלוואה כנגד קרן השתלמות, הלוואה) ומה כל מקור מוסיף להחזר החודשי; ומבחן ליום המסירה של מבצע קבלן עם מעט תשלום עכשיו: ההצמדה, המשכנתא והכסף שצריך באותו יום.',
			'data' => array( 'buying.json', 'nrm.json', 'boi-mortgage.json', 'ptax.json', 'cost.json', 'cbs-200010.json', 'prices-hub.json' ),
			'related' => array( '/mortgage-calculator/mortgage-ltv-ratio/' => 'אחוז מימון למשכנתא', '/mortgage-calculator/mortgage-for-any-purpose/' => 'משכנתא לכל מטרה', '/new-projects/construction-input-index/' => 'הצמדה למדד תשומות הבנייה', '/developer-deals/' => 'מבצעי קבלנים' ) );
		$tools['bladder'] = array( 'file' => 'buying', 'deps' => array( 'prices-common' ),
			'name' => 'איך לקנות דירה בארץ עם 100 אלף, 300 אלף או 500 אלף ש״ח', 'cat' => 'FinanceApplication', 'kicker' => 'סולם הון עצמי · ערים וחדרים',
			'desc' => 'ההון העצמי והמצב שלכם (והכנסה, אם רוצים) נותנים את המחיר המרבי לפי כללי המימון של בנק ישראל אחרי מס רכישה ועורך דין, ואת 24 הערים ומספרי החדרים שבהם המחיר החציוני של הדירות שנמכרו נכנס בתקציב, לפי העסקאות שדווחו לרשות המסים.',
			'data' => array( 'buying.json', 'nrm.json', 'ptax.json', 'cost.json', 'boi-mortgage.json', 'prices-hub.json' ),
			'related' => array( '/affordable-apartments-israel-2026/' => 'דירות זולות בישראל', '/apartment-prices/' => 'מחירי דירות לפי עיר', '/mortgage-calculator/mortgage-repayment-capacity/' => 'מחשבון כושר החזר', '/dira-behanacha/' => 'דירה בהנחה' ) );
		$tools['boffer'] = array( 'file' => 'buying', 'deps' => array( 'prices-common' ),
			'name' => 'הצעת מחיר לרכישת דירה: המחיר המבוקש מול העסקאות בעיר', 'cat' => 'ReferenceApplication', 'kicker' => 'משא ומתן · דירה יד שנייה',
			'desc' => 'המחיר המבוקש של דירה יד שנייה מול המחיר החציוני של העסקאות שנסגרו באותה עיר ובאותו מספר חדרים, כמה מהשכונות בעיר נמכרו בחציון נמוך יותר, מדד המחוז, וטווח פתיחה להצעה עם הבסיס שלו, בלי "הנחה מקובלת" שאין לה מקור.',
			'data' => array( 'prices-hub.json', 'value.json' ),
			'related' => array( '/property-value-estimator/' => 'מחשבון שווי דירה', '/real-estate-appraiser/' => 'שמאי מקרקעין', '/buying-new-apartment-developer-2026-negotiation/' => 'משא ומתן מול קבלן', '/home-inspection/' => 'בדק בית' ) );
		return $tools;
	} );

	/** The plain summaries (no JS, search engines, AI answers): the same numbers the tools show, as sentences and tables. */
	function nadlan_bhub_summary( $id, $dir = null ) {
		$dir = $dir ? $dir : dirname( __DIR__ ) . '/assets/instruments/data/';
		$rd  = function ( $f ) use ( $dir ) { return is_readable( $dir . $f ) ? json_decode( (string) file_get_contents( $dir . $f ), true ) : null; };
		$BU = $rd( 'buying.json' ); $PT = $rd( 'ptax.json' ); $NR = $rd( 'nrm.json' );
		if ( ! is_array( $BU ) || ! is_array( $PT ) || ! is_array( $NR ) ) { return ''; }
		$n0  = function ( $x ) { return number_format( round( (float) $x ) ); };
		$pc  = function ( $x, $d = 2 ) { return rtrim( rtrim( number_format( 100 * (float) $x, $d, '.', '' ), '0' ), '.' ); };
		$dt  = function ( $iso ) { $p = explode( '-', (string) $iso ); return 3 === count( $p ) ? (int) $p[2] . '.' . (int) $p[1] . '.' . $p[0] : ( 2 === count( $p ) ? (int) $p[1] . '.' . $p[0] : (string) $iso ); };
		$tax = function ( $price, $track, $dis = false ) use ( $PT ) {
			if ( $dis && 'single' === $track && $price <= $PT['disabled']['single_cap'] ) { return max( 0, $price - $PT['tracks']['single'][0][0] ) * $PT['disabled']['rate']; }
			$t = 0; $lo = 0; foreach ( $PT['tracks'][ $track ] as $b ) { $hi = null === $b[0] ? INF : (float) $b[0]; $top = min( $price, $hi ); if ( $top > $lo ) { $t += ( $top - $lo ) * (float) $b[1]; } if ( $price <= $hi ) { break; } $lo = $hi; }
			return $t;
		};
		$brk = function ( $track ) use ( $PT, $n0, $pc ) { $o = array(); $lo = 0; foreach ( $PT['tracks'][ $track ] as $b ) { $o[] = null === $b[0] ? $pc( $b[1] ) . '% מעל ' . $n0( $lo ) . ' ₪' : $pc( $b[1] ) . '% עד ' . $n0( $b[0] ) . ' ₪'; $lo = $b[0]; } $l = array_pop( $o ); return implode( ', ', $o ) . ' ו־' . $l; };
		$nom = function ( $e ) { return 1200 * ( pow( 1 + $e / 100, 1 / 12 ) - 1 ); };
		$pmt = function ( $L, $e, $y ) use ( $nom ) { $r = $nom( $e ) / 1200; $n = (int) round( $y * 12 ); return $L <= 0 ? 0 : ( 0.0 === $r ? $L / $n : $L * $r / ( 1 - pow( 1 + $r, -$n ) ) ); };
		$lastq = function ( $arr, $Q ) { for ( $i = count( (array) $arr ) - 1; $i >= 0; $i-- ) { if ( null !== $arr[ $i ] ) { return array( 'v' => (float) $arr[ $i ], 'q' => $Q[ $i ], 'i' => $i ); } } return null; };
		$HM  = array( 'ינואר', 'פברואר', 'מרץ', 'אפריל', 'מאי', 'יוני', 'יולי', 'אוגוסט', 'ספטמבר', 'אוקטובר', 'נובמבר', 'דצמבר' );
		$ql  = function ( $q ) use ( $HM ) { $p = explode( '.', $q ); $a = explode( '-', $p[0] ); return $HM[ (int) $a[0] - 1 ] . ' עד ' . $HM[ (int) $a[1] - 1 ] . ' ' . $p[1]; };
		$st  = function ( $sid ) use ( $BU ) { foreach ( $BU['statuses'] as $s ) { if ( $s['id'] === $sid ) { return $s; } } return $BU['statuses'][0]; };
		$has = function ( $s, $f ) { return in_array( $f, (array) $s['flags'], true ); };
		$CO = $rd( 'cost.json' ); $BM = $rd( 'boi-mortgage.json' ); $PH = $rd( 'prices-hub.json' );
		$law = function ( $P ) use ( $CO ) { return $P * $CO['lawyer']['from'] / 100 * ( 1 + $CO['vat'] ); };
		$rate = is_array( $BM ) ? (float) $BM['rates']['fixed_nl']['rate'] : null; $rmon = is_array( $BM ) ? end( $BM['rates']['fixed_nl']['hist'] )[0] : '';
		$wrap = function ( $h ) use ( $id ) { return '<div class="nlbh-sum" data-bhub-sum="' . esc_attr( $id ) . '">' . $h . '</div>'; };

		if ( 'bplan' === $id ) {
			$Z = $rd( 'zakaut.json' ); $O = $rd( 'orechdin.json' );
			if ( ! is_array( $Z ) || ! is_array( $O ) ) { return ''; }
			$M = array( 'ptax' => $PT, 'zakaut' => $Z, 'orechdin' => $O );
			$M['orechdin']['cap']['pctx'] = $pc( $O['cap']['pct'] ); $M['orechdin']['cgt_advance']['afterx'] = $pc( $O['cgt_advance']['after_paid'] ); $M['orechdin']['cgt_advance']['ratex'] = $pc( $O['cgt_advance']['rate'] );
			$fill = function ( $s ) use ( $M ) { return preg_replace_callback( '/\{([a-z0-9_.]+)\}/i', function ( $m ) use ( $M ) { $v = $M; foreach ( explode( '.', $m[1] ) as $k ) { if ( ! is_array( $v ) || ! array_key_exists( $k, $v ) ) { return $m[0]; } $v = $v[ $k ]; } return is_numeric( $v ) && floor( (float) $v ) == (float) $v ? number_format( (float) $v ) : (string) $v; }, $s ); };
			$h = '<p>קניית דירה מתחילה במצב שלכם: אותה דירה עולה במס רכישה אחר ובהון עצמי אחר לקונה של דירה יחידה, למי שכבר יש לו דירה, לעולה או לתושב חוץ. הטבלה מסכמת את 12 המצבים שאנשים מחפשים, לפי רשות המסים (נבדק ' . esc_html( $dt( $PT['checked'] ) ) . ') ולפי הוראה 329 של בנק ישראל (נבדק ' . esc_html( $dt( $NR['checked'] ) ) . ').</p>';
			$h .= '<table><caption>מס רכישה ושיעור המימון המרבי לפי מצב הקונה</caption><thead><tr><th>מצב</th><th>מס רכישה</th><th>מימון מרבי</th><th>תוספות</th></tr></thead><tbody>';
			$tr = array( 'single' => 'מדרגות דירה יחידה', 'extra' => 'דירה נוספת: ' . $brk( 'extra' ), 'oleh' => 'מסלול עולים: ' . $brk( 'oleh' ), 'foreign' => 'תושבי חוץ: ' . $brk( 'foreign' ) );
			foreach ( $BU['statuses'] as $s ) {
				$x = array();
				if ( $has( $s, 'zakaut' ) ) { $x[] = 'הלוואת זכאות'; } if ( $has( $s, 'service' ) ) { $x[] = $Z['service']['pct_per_month'] . '% לכל חודש שירות'; } if ( $has( $s, 'reserve' ) ) { $x[] = 'תוספת מילואים ' . $Z['reserve']['min_pct'] . '% עד ' . $Z['reserve']['max_pct_person'] . '%'; }
				if ( $has( $s, 'disability' ) ) { $x[] = 'נקודות נכות'; } if ( $has( $s, 'ptax_disabled' ) ) { $x[] = 'מס ' . $pc( $PT['disabled']['rate'] ) . '% מעל ' . $n0( $PT['tracks']['single'][0][0] ) . ' ₪ עד ' . $n0( $PT['disabled']['single_cap'] ) . ' ₪'; }
				if ( $has( $s, 'upgrader' ) ) { $x[] = 'מכירת הקיימת בתוך ' . (int) $PT['upgrader'][0]['months'] . ' חודשים'; } if ( $has( $s, 'career' ) ) { $x[] = 'אין טבלה נפרדת אצל משרד הבינוי'; }
				$h .= '<tr><td>' . esc_html( $s['label'] ) . '</td><td>' . esc_html( $tr[ $s['ptax'] ] ) . '</td><td>' . esc_html( $pc( $NR['ltv_by_status'][ $s['ltv'] ] ) ) . '%</td><td>' . esc_html( $x ? implode( ' · ', $x ) : '·' ) . '</td></tr>';
			}
			$h .= '</tbody></table><p>מדרגות דירה יחידה: ' . esc_html( $brk( 'single' ) ) . ', קפואות עד ' . esc_html( $dt( $PT['frozen_until'] ) ) . '. דירה נוספת ותושבי חוץ: לרכישה עד ' . esc_html( $dt( $PT['valid']['extra'] ) ) . '. הלוואת הזכאות בטבלת המשפחות הוותיקות: מ־' . $n0( $Z['bands']['rows'][0][2] ) . ' ₪ ועד ' . $n0( end( $Z['bands']['rows'] )[2] ) . ' ₪ (משרד הבינוי והשיכון).</p>';
			$h .= '<ol>';
			foreach ( $BU['stages'] as $g ) { $t = array(); foreach ( $BU['steps'] as $x ) { if ( (int) $x['st'] === (int) $g['id'] && empty( $x['only'] ) ) { $t[] = $fill( $x['t'] ); } } $h .= '<li><strong>' . esc_html( $g['t'] ) . ':</strong> ' . esc_html( implode( ' · ', $t ) ) . '.</li>'; }
			return $wrap( $h . '</ol>' );
		}

		if ( ! is_array( $CO ) || ! is_array( $BM ) || ! is_array( $PH ) ) { return ''; }
		$il4 = $lastq( $PH['il']['r4'], $PH['q'] );

		if ( 'bequity' === $id ) {
			$C = $rd( 'cbs-200010.json' ); $P = $il4['v']; $l = (float) $NR['ltv_by_status']['cit_first'];
			$tx = $tax( $P, 'single' ); $lw = $law( $P ); $need = $P * ( 1 - $l ) + $tx + $lw; $mort = $P * $l;
			$ks = array_keys( $C['months'] ); sort( $ks ); $k = end( $ks ); $ky = ( (int) substr( $k, 0, 4 ) - 1 ) . substr( $k, 4 ); $g = $C['months'][ $k ] / $C['months'][ $ky ] - 1;
			$paid = 0.1 * $P; $def = $P - $paid; $add = $def * 0.5 * ( pow( 1 + $g, 30 / 12 ) - 1 ); $due = $def + $add; $loan = min( $l * ( $P + $add ), $due ); $cash = max( 0, $due - $loan );
			$h = '<p>דירת 4 חדרים במחיר החציוני הארצי, ' . $n0( $P ) . ' ₪ (' . esc_html( $ql( $il4['q'] ) ) . ', רשות המסים), דורשת מקונה של דירה יחידה <strong>' . $n0( $need ) . ' ₪ מכספו</strong>: ' . $n0( $P * ( 1 - $l ) ) . ' ₪ שהבנק לא מממן (' . $pc( 1 - $l ) . '%), מס רכישה ' . $n0( $tx ) . ' ₪ ועורך דין מ־' . $n0( $lw ) . ' ₪. המשכנתא של ' . $n0( $mort ) . ' ₪ ל־25 שנה בריבית ' . esc_html( $rate ) . '% (' . esc_html( $BM['rates']['fixed_nl']['label'] ) . ', ממוצע בנק ישראל ל־' . esc_html( $dt( $rmon ) ) . ') היא החזר של כ־' . $n0( $pmt( $mort, $rate, 25 ) ) . ' ₪ בחודש.</p>';
			$h .= '<p>מקורות אפשריים להון העצמי: חסכונות, מתנה מההורים, שותפים, משכנתא על הדירה של ההורים, הלוואה כנגד קרן השתלמות או קופת גמל, והלוואה מבנק או מגוף חוץ בנקאי. כל הלוואה מוסיפה החזר חודשי, והבנק למשכנתאות מוריד התחייבויות קבועות של יותר מ־18 חודשים מההכנסה הפנויה (הוראה 329, נספח א).</p>';
			$h .= '<p>מבצע של קבלן עם 10% עכשיו: על אותה דירה, אחרי 30 חודשים, כשמחצית מכל תשלום צמודה ומדד תשומות הבנייה עולה כמו ב־12 החודשים האחרונים (' . $pc( $g, 1 ) . '%, ' . esc_html( $dt( $ky ) ) . ' עד ' . esc_html( $dt( $k ) ) . ', הלמ״ס), היתרה לקבלן ביום המסירה היא ' . $n0( $due ) . ' ₪. המשכנתא מממנת ' . $n0( $loan ) . ' ₪, ולכן <strong>ביום המסירה צריך עוד ' . $n0( $cash ) . ' ₪ מכספכם</strong>. בריבית גבוהה בנקודה ההחזר החודשי עולה מ־' . $n0( $pmt( $loan, $rate, 25 ) ) . ' ₪ ל־' . $n0( $pmt( $loan, $rate + 1, 25 ) ) . ' ₪.</p>';
			return $wrap( $h );
		}

		if ( 'bladder' === $id ) {
			$o = array( 'ltv' => (float) $NR['ltv_by_status']['cit_first'] );
			$cash = function ( $P ) use ( $o, $tax, $law ) { return $P - $o['ltv'] * $P + $tax( $P, 'single' ) + $law( $P ); };
			$h = '<table><caption>הון עצמי, המחיר המרבי בדירה יחידה (מימון ' . $pc( $o['ltv'] ) . '%, אחרי מס רכישה ועורך דין) ומספר הערים, מתוך ' . count( $PH['city'] ) . ', שבהן המחיר החציוני נכנס בתקציב</caption><thead><tr><th>הון עצמי</th><th>מחיר מרבי</th><th>3 חדרים</th><th>4 חדרים</th><th>5 חדרים</th><th>הערים הזולות לדירת 4 חדרים</th></tr></thead><tbody>';
			foreach ( array( 100000, 300000, 500000, 1000000 ) as $E ) {
				$lo = 0; $hi = 1e8; for ( $i = 0; $i < 80; $i++ ) { $mid = ( $lo + $hi ) / 2; if ( $cash( $mid ) <= $E ) { $lo = $mid; } else { $hi = $mid; } } $P = floor( $lo / 1000 ) * 1000;
				$cnt = array( 3 => 0, 4 => 0, 5 => 0 ); $fit4 = array();
				foreach ( $PH['city'] as $c ) { foreach ( array( 3, 4, 5 ) as $r ) { $x = $lastq( $c[ 'r' . $r ], $PH['q'] ); if ( $x && $x['v'] <= $P ) { $cnt[ $r ]++; if ( 4 === $r ) { $fit4[ $c['n'] ] = $x['v']; } } } }
				asort( $fit4 );
				$h .= '<tr><td>' . $n0( $E ) . ' ₪</td><td>' . $n0( $P ) . ' ₪</td><td>' . $cnt[3] . '</td><td>' . $cnt[4] . '</td><td>' . $cnt[5] . '</td><td>' . esc_html( $fit4 ? implode( ', ', array_slice( array_keys( $fit4 ), 0, 5 ) ) : '·' ) . '</td></tr>';
			}
			return $wrap( $h . '</tbody></table><p>המחיר החציוני הוא של הדירות שנמכרו בכל עיר ברבעון האחרון שפורסם, לפי העסקאות שדווחו לרשות המסים (אתר הנדל״ן הממשלתי, גרסה ' . esc_html( $PH['vsrc']['version'] ) . '). שיעור המימון לפי הוראה 329 של בנק ישראל; מס רכישה לפי המדרגות של רשות המסים; עורך דין ' . esc_html( $CO['lawyer']['from'] ) . '% ועוד מע״מ. בלי שמאי, תיווך, מעבר ושיפוץ.</p>' );
		}

		if ( 'boffer' === $id ) {
			$c = null; foreach ( $PH['city'] as $x ) { if ( 'רמת גן' === $x['n'] ) { $c = $x; } } if ( ! $c ) { $c = $PH['city'][0]; }
			$L = $lastq( $c['r4'], $PH['q'] ); $four = array(); for ( $i = $L['i']; $i >= 0 && count( $four ) < 4; $i-- ) { if ( null !== $c['r4'][ $i ] ) { $four[] = array( (float) $c['r4'][ $i ], $PH['q'][ $i ] ); } }
			$low = $four[0]; foreach ( $four as $f ) { if ( $f[0] < $low[0] ) { $low = $f; } }
			$ask = round( $L['v'] * 1.08 / 10000 ) * 10000; $lo = $L['v'] * $low[0] / $L['v'];
			$h = '<p>הצעת מחיר לדירה יד שנייה נשענת על העסקאות שנסגרו, לא על המודעות. דוגמה: דירת 4 חדרים ב' . esc_html( $c['n'] ) . ' במחיר מבוקש של ' . $n0( $ask ) . ' ₪. החציון של העסקאות בעיר היה ' . $n0( $L['v'] ) . ' ₪ ב' . esc_html( $ql( $L['q'] ) ) . ', כלומר המחיר המבוקש גבוה ב־' . $pc( $ask / $L['v'] - 1, 1 ) . '% מהחציון. הרבעון הנמוך מבין ארבעת האחרונים היה ' . $n0( $low[0] ) . ' ₪ (' . esc_html( $ql( $low[1] ) ) . '). טווח פתיחה עם בסיס: מ־' . $n0( $lo ) . ' ₪ ועד ' . $n0( min( $ask, $L['v'] ) ) . ' ₪. מחיר מבוקש שכבר מתחת לטווח לא משאיר בסיס שוק לירידה, ואז הבסיס הוא הדירה עצמה: בדק בית, תיקונים, רישום ולוח זמנים.</p>';
			return $wrap( $h . '<p>מקורות: רשות המסים דרך אתר הנדל״ן הממשלתי (חציון לפי עיר וחדרים וחציון לפי שכונה), הלשכה המרכזית לסטטיסטיקה (מדד מחירי הדירות לפי מחוז). אין כאן "הנחה מקובלת", כי לא מצאנו לה מקור מתוארך.</p>' );
		}
		return '';
	}

	/* Until the engine branch exists: put the summary inside the tool's panel, after its title, once. */
	add_filter( 'do_shortcode_tag', function ( $out, $tag, $attr ) {
		if ( 'nadlan_tool' !== $tag || ! is_array( $attr ) || empty( $attr['id'] ) || ! in_array( $attr['id'], nadlan_bhub_tool_ids(), true ) || false !== strpos( (string) $out, 'data-bhub-sum' ) ) { return $out; }
		$sum = nadlan_bhub_summary( $attr['id'] );
		$at  = strpos( (string) $out, '</h2></div></div>' );
		return ( $sum && false !== $at ) ? substr( $out, 0, $at + 5 ) . $sum . substr( $out, $at + 5 ) : $out;
	}, 10, 3 );

	/** FAQPage from the page's own "קניית דירה: השאלות שלא שואלים את עורך הדין" section (h3 question, then its paragraphs). */
	function nadlan_bhub_faq( $html ) {
		$html = preg_replace( '/<!--.*?-->/s', '', (string) $html );
		if ( ! preg_match( '/<h2[^>]*>[^<]{0,40}השאלות שלא שואלים את עורך הדין[^<]{0,40}<\/h2>(.*?)(?=<h2|$)/su', $html, $m ) ) { return array(); }
		preg_match_all( '/<h3[^>]*>(.*?)<\/h3>\s*((?:<p[^>]*>.*?<\/p>\s*)+)/su', $m[1], $qa, PREG_SET_ORDER );
		$out = array();
		foreach ( $qa as $x ) { $q = trim( wp_strip_all_tags( $x[1] ) ); $a = trim( preg_replace( '/\s+/u', ' ', wp_strip_all_tags( $x[2] ) ) ); if ( $q && $a ) { $out[] = array( '@type' => 'Question', 'name' => $q, 'acceptedAnswer' => array( '@type' => 'Answer', 'text' => $a ) ); } }
		return count( $out ) >= 2 ? $out : array();
	}

	add_action( 'wp_head', function () {
		if ( ! function_exists( 'nadlan_nli_page_ids' ) || ! array_intersect( nadlan_nli_page_ids(), nadlan_bhub_tool_ids() ) || ! is_singular() ) { return; }
		$p = get_post(); $faq = $p ? nadlan_bhub_faq( $p->post_content ) : array();
		if ( ! $faq ) { return; }
		echo '<script type="application/ld+json" id="nadlan-bhub-faq">' . wp_json_encode( array( '@context' => 'https://schema.org', '@type' => 'FAQPage', 'url' => get_permalink(), 'mainEntity' => $faq ), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . '</script>' . "\n";
	}, 31 );
}
