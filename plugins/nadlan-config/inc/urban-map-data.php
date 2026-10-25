<?php
/**
 * nadlan-config: the renewal map's data layer (1.72.520, Ben 25.10.2026, Q1 of docs/loop/UPGRADE-LOOP.md).
 * Everything here reads data/renewal-stats.json (tools/urban/build_renewal_stats.py): the Ministry of Construction and Housing open
 * file of urban renewal complexes (data.gov.il) and the counts of the authority's live map (gov.il). Every table and chart prints its
 * source and date. Stat tiles, stage table + funnel, approved and in-execution lists, a table per district, the declarations-per-year,
 * districts, tracks and top-15 charts, the stage dictionary, approval-to-permit years, where to check what, 20 visible questions (the
 * same list feeds FAQPage) and the sources. Identity: the NadLan Instruments tokens (ink, sea, survey red; IBM Plex Sans Hebrew,
 * Karantina for figures, IBM Plex Mono for amounts). Loaded by inc/urban-map.php only if this file exists.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_urd' ) ) {
	function nadlan_urd() {
		static $d = null;
		if ( null === $d ) {
			$f = dirname( __DIR__ ) . '/data/renewal-stats.json';
			$d = is_readable( $f ) ? json_decode( (string) file_get_contents( $f ), true ) : array();
			if ( ! is_array( $d ) ) { $d = array(); }
		}
		return $d;
	}
	function nadlan_urd_n( $x ) { return number_format( (float) $x ); }
	function nadlan_urd_date( $iso ) { $t = strtotime( (string) $iso ); return $t ? date( 'j.n.Y', $t ) : ''; }
	function nadlan_urd_dmy( $s ) { return preg_match( '#^(\d{2})/(\d{2})/(\d{4})$#', (string) $s, $m ) ? ( (int) $m[1] ) . '.' . ( (int) $m[2] ) . '.' . $m[3] : (string) $s; }
	function nadlan_urd_src( $txt ) { return '<p class="nlur2-src">' . $txt . '</p>'; }
	function nadlan_urd_city( $name ) {
		$d = nadlan_urd();
		foreach ( (array) ( $d['file']['cities'] ?? array() ) as $c ) { if ( $c['city'] === $name ) { return $c; } }
		return null;
	}
}

/* 20 questions in searchers' words; numbers from the data file and the research facts (docs/research/2026-10-26-upgrades/q1-renewal-map) */
if ( ! function_exists( 'nadlan_urd_faq' ) ) {
	function nadlan_urd_faq() {
		$d = nadlan_urd(); $f = $d['file'] ?? array(); $m = $d['map'] ?? array();
		$fd = nadlan_urd_date( $f['last_modified'] ?? '' ); $md = nadlan_urd_date( $m['last_edit'] ?? '' );
		$appr = 0; foreach ( (array) ( $f['by_status'] ?? array() ) as $k => $v ) { if ( 0 === strpos( $k, 'תכנית מאושרת' ) ) { $appr += (int) $v['n']; } }
		$mult = ! empty( $f['existing'] ) ? number_format( $f['proposed'] / $f['existing'], 2 ) : '';
		$y = (array) ( $f['by_year'] ?? array() );
		$cn = function ( $n ) { $c = nadlan_urd_city( $n ); return $c ? (int) $c['n'] : 0; };
		return array(
			array( 'איפה רואים את מפת ההתחדשות העירונית הרשמית?', 'הרשות הממשלתית להתחדשות עירונית מפרסמת באתר gov.il מפה של מתחמי פינוי בינוי, שלפי הרשות מתעדכנת מדי יום. ב-' . $md . ' היו בה ' . nadlan_urd_n( $m['total'] ?? 0 ) . ' מתחמים ב-' . (int) ( $m['localities'] ?? 0 ) . ' ערים. בעמוד הזה המתחמים מוצגים לפי עיר, עם טבלה לכל שלב ולכל מחוז.' ),
			array( 'איך בודקים אם הבניין שלי נמצא במתחם פינוי בינוי?', 'מקישים על העיר במפה או מחפשים את הרחוב ברשימת המתחמים של העיר. כשמתחם מופיע, בודקים את מספר התכנית באתר מינהל התכנון ואת סוג המתחם ברשימת הרשות. אפשר להתחיל גם בבדיקת הבניין החינמית באתר.' ),
			array( 'מה זה מתחם התחדשות עירונית מוכרז?', 'מתחם שהרשות הכריזה עליו כמתאים להתחדשות, למשל לפי סעיף 14 לחוק הרשות. ההכרזה פותחת מסלול תכנון, אבל היא עדיין לא תכנית מאושרת ולא היתר בנייה.' ),
			array( 'מה ההבדל בין מסלול מיסוי למסלול רשויות?', 'בקובץ הרשמי מ-' . $fd . ' יש ' . nadlan_urd_n( $f['tracks']['מיסוי'] ?? 0 ) . ' מתחמים במסלול מיסוי ו-' . nadlan_urd_n( $f['tracks']['רשויות'] ?? 0 ) . ' במסלול רשויות. במסלול מיסוי היזם יוזם והמתחם זכאי להטבות מס, ובמסלול רשויות הרשות המקומית מקדמת את התכנון.' ),
			array( 'מה ההבדל בין הכרזה על מתחם לבין תכנית מאושרת?', 'הכרזה קובעת שהמתחם מתאים להתחדשות. תכנית מאושרת היא תכנית שהוועדה אישרה ופרסמה, ורק אחריה מגישים בקשה להיתר. בקובץ הרשמי ' . nadlan_urd_n( $appr ) . ' מתחמים עם תכנית מאושרת.' ),
			array( 'אילו מתחמי פינוי בינוי מאושרים יש בעיר שלי?', 'בטבלת המתחמים המאושרים בעמוד, לפי מחוז ועיר, עם מספר התכנית, קישור לאתר מינהל התכנון, וכמה דירות יש היום וכמה יהיו אחרי הבנייה.' ),
			array( 'איזה פרויקטים של פינוי בינוי כבר בשלבי בנייה?', 'בקובץ הרשמי ' . nadlan_urd_n( $f['in_execution'] ?? 0 ) . ' מתחמים מסומנים בביצוע, ובכ-' . nadlan_urd_n( $f['permits_complexes'] ?? 0 ) . ' מתחמים נרשמו היתרים ל-' . nadlan_urd_n( $f['permits_units'] ?? 0 ) . ' יחידות דיור (' . $fd . '). הרשימה בטבלת הביצוע בעמוד.' ),
			array( 'כמה זמן עובר מאישור התכנית ועד היתר בנייה?', 'לפי דוח הרשות לשנת 2025, בממוצע 4.0 שנים בפינוי בינוי, על פי 28 מתחמים שקיבלו היתר ראשון ב-2025. זה ממוצע של שנה אחת ולא תחזית למתחם מסוים.' ),
			array( 'מה אומר כל שלב: תכנון ראשוני, תכנון סטטוטורי, תכנית מאושרת?', 'תכנון ראשוני: עבודה על המתחם לפני שתכנית הוגשה. תכנון סטטוטורי: התכנית בדיונים בוועדות. תכנית מאושרת לפני מימוש: יש תכנית ועוד אין היתר. במימוש: הביצוע התחיל. אחרי רישוי: ניתנו היתרים.' ),
			array( 'מה זה מכפיל בפינוי בינוי?', 'היחס בין מספר הדירות אחרי הבנייה למספר הדירות היום. בקובץ הרשמי ' . nadlan_urd_n( $f['existing'] ?? 0 ) . ' דירות היום ו-' . nadlan_urd_n( $f['proposed'] ?? 0 ) . ' אחרי הבנייה, מכפיל ממוצע ' . $mult . ' (חישוב שלנו).' ),
			array( 'כמה בעלי דירות צריכים להסכים לפינוי בינוי?', '66% מבעלי הדירות במתחם, ולפחות 60% מבעלי הדירות בכל בניין, לפי השאלות והתשובות של הרשות.' ),
			array( 'כמה דירות צריך כדי שבניין ייכנס למתחם פינוי בינוי?', 'מתחם פינוי בינוי כולל לפחות 24 דירות קיימות, ובמצב החדש לפחות 70 דירות או פי שניים מהקיים, הגבוה מביניהם (דוח הרשות לשנת 2025).' ),
			array( 'למה המתחם שלי לא מופיע במפה?', 'הקובץ הפתוח עודכן לאחרונה ב-' . $fd . ', ומפת הרשות כוללת ' . nadlan_urd_n( $m['total'] ?? 0 ) . ' מתחמים נכון ל-' . $md . '. מתחם חדש, או בניין שלא נכלל במתחם, לא יופיע. בודקים ברשימת המתחמים של הרשות ובמינהלת ההתחדשות העירונית בעירייה.' ),
			array( 'האם פרויקטים של תמ"א 38 מופיעים במפה?', 'לא. הקובץ הרשמי כולל מתחמי התחדשות עירונית, בעיקר פינוי בינוי, ופרויקטים של תמ"א 38 לבניין בודד לא נמצאים בו.' ),
			array( 'כל כמה זמן מתעדכנת מפת ההתחדשות העירונית?', 'מפת הרשות מתעדכנת לפי הרשות מדי יום, והעדכון האחרון בה היה ב-' . $md . '. הקובץ הפתוח ב-data.gov.il עודכן ב-' . $fd . '. בעמוד הזה מופיע התאריך של כל מקור.' ),
			array( 'איך מוצאים תכנית לפי גוש וחלקה או לפי כתובת?', 'באתר מינהל התכנון ובמפת התכניות שלו מחפשים לפי מספר תכנית, גוש וחלקה או כתובת, ושם מופיעים שלב התכנית ותאריכי ההפקדה והאישור.' ),
			array( 'מה זה מתחם מועדף לדיור ובמה הוא שונה ממתחם מוכרז?', 'ברשימת הרשות יש חמישה סוגי מתחמים: מתחם שהוכרז לפי סעיף 14 לחוק הרשות, מתחם של גוף ציבורי, מתחם של יזם שעבר סף תכנוני, מתחם מועדף לדיור, ומתחם בביצוע. מתחם מועדף לדיור מקודם במסלול תכנון נפרד.' ),
			array( 'מה זו מינהלת התחדשות עירונית ואיפה יש כזו?', 'מינהלה עירונית שמלווה את התושבים ואת התכנון בעיר. לפי דוח הרשות לשנת 2025 פועלות 51 מינהלות ברחבי הארץ.' ),
			array( 'כמה מתחמי פינוי בינוי יש בירושלים, בתל אביב ובראשון לציון?', 'בקובץ הרשמי מ-' . $fd . ': ירושלים ' . $cn( 'ירושלים' ) . ' מתחמים, תל אביב יפו ' . $cn( 'תל אביב יפו' ) . ', ראשון לציון ' . $cn( 'ראשון לציון' ) . '. כל הערים בטבלאות לפי מחוז בעמוד.' ),
			array( 'כמה מתחמים חדשים הוכרזו בשנה האחרונה?', 'לפי תאריכי ההכרזה בקובץ הרשמי: ' . (int) ( $y['2025'] ?? 0 ) . ' מתחמים ב-2025 ו-' . (int) ( $y['2024'] ?? 0 ) . ' ב-2024, ו-' . (int) ( $y['2026'] ?? 0 ) . ' ב-2026 עד ' . nadlan_urd_dmy( $f['last_declaration'] ?? '' ) . '.' ),
		);
	}
	function nadlan_urd_faq_schema() {
		$e = array();
		foreach ( nadlan_urd_faq() as $qa ) { $e[] = array( '@type' => 'Question', 'name' => $qa[0], 'acceptedAnswer' => array( '@type' => 'Answer', 'text' => $qa[1] ) ); }
		return array( '@context' => 'https://schema.org', '@type' => 'FAQPage', 'mainEntity' => $e );
	}
}

if ( ! function_exists( 'nadlan_urd_html' ) ) {
	function nadlan_urd_html() {
		$d = nadlan_urd();
		if ( empty( $d['file']['total'] ) ) { return ''; }
		$f = $d['file']; $m = $d['map'] ?? array();
		$fd = nadlan_urd_date( $f['last_modified'] ); $md = nadlan_urd_date( $m['last_edit'] ?? '' );
		$fsrc = 'המקור: <a href="' . esc_url( $f['url'] ) . '" rel="noopener">קובץ מתחמי ההתחדשות העירונית של משרד הבינוי והשיכון, data.gov.il</a>, עודכן ' . esc_html( $fd ) . '.';
		$msrc = 'מפת הרשות הממשלתית להתחדשות עירונית ב-gov.il, נכון ל-' . esc_html( $md ) . ' (ספירה בלבד).';
		$h = '';
		/* stat tiles */
		$h .= '<div class="nlur2-tiles">'
			. '<div><span>מתחמים בקובץ הרשמי</span><b>' . nadlan_urd_n( $f['total'] ) . '</b><small>' . (int) $f['localities'] . ' ערים · ' . esc_html( $fd ) . '</small></div>'
			. '<div><span>במפת הרשות</span><b>' . nadlan_urd_n( $m['total'] ?? 0 ) . '</b><small>' . (int) ( $m['localities'] ?? 0 ) . ' ערים · ' . esc_html( $md ) . '</small></div>'
			. '<div><span>דירות היום ואחרי הבנייה</span><b>' . nadlan_urd_n( $f['existing'] ) . ' → ' . nadlan_urd_n( $f['proposed'] ) . '</b><small>בקובץ הרשמי</small></div>'
			. '<div><span>היתרים שנרשמו</span><b>' . nadlan_urd_n( $f['permits_units'] ) . '</b><small>יחידות דיור ב-' . nadlan_urd_n( $f['permits_complexes'] ) . ' מתחמים</small></div>'
			. '</div>';
		$h .= '<p class="nlur2-moved">בין הקובץ של 15.8.2026 למפת הרשות של 20.10.2026 נוספו 36 מתחמים ו-17 מתחמים עלו שלב, רובם מתכנון סטטוטורי לתכנית מאושרת (חישוב שלנו, השוואה לפי מספר מתחם).</p>';
		/* stages */
		$st = (array) $f['by_status']; $mx = 1; foreach ( $st as $v ) { $mx = max( $mx, (int) $v['n'] ); }
		$map_st = (array) ( $m['by_stage'] ?? array() );
		$rows = ''; $bars = ''; $i = 0;
		foreach ( $st as $k => $v ) {
			if ( ! $v['n'] ) { continue; }
			$mv = isset( $map_st[ $k ] ) ? nadlan_urd_n( $map_st[ $k ] ) : ( 'תכנית מאושרת אחרי רישוי' === $k ? 'לא מופיע כשלב במפה' : '' );
			$rows .= '<tr><th scope="row">' . esc_html( $k ) . '</th><td>' . nadlan_urd_n( $v['n'] ) . '</td><td>' . nadlan_urd_n( $v['existing'] ) . '</td><td>' . nadlan_urd_n( $v['proposed'] ) . '</td><td>' . esc_html( $mv ) . '</td></tr>';
			$w = max( 4, round( 412 * $v['n'] / $mx ) ); $y = 6 + $i * 52;
			$bars .= '<text x="416" y="' . ( $y + 13 ) . '" text-anchor="end" class="lb">' . esc_html( $k ) . '</text>'
				. '<rect x="' . ( 416 - $w ) . '" y="' . ( $y + 20 ) . '" width="' . $w . '" height="16" rx="2" class="s' . $i . '"/>'
				. '<text x="416" y="' . ( $y + 50 ) . '" text-anchor="end" class="nv">' . nadlan_urd_n( $v['n'] ) . ' מתחמים · ' . nadlan_urd_n( $v['proposed'] ) . ' דירות אחרי הבנייה</text>';
			$i++;
		}
		$h .= '<section id="nlur2-stages"><h2>מתחמי פינוי בינוי לפי שלב</h2>'
			. '<p>הקובץ הרשמי מחלק את המתחמים לשלבי תכנון. הכרזה על מתחם עדיין אינה תכנית מאושרת, ותכנית מאושרת עדיין אינה היתר. בעמודה האחרונה: כמה מתחמים מופיעים באותו שלב במפת הרשות העדכנית יותר.</p>'
			. '<svg class="nlur2-svg" viewBox="0 0 420 ' . ( 10 + $i * 52 ) . '" role="img" aria-label="מתחמים לפי שלב בקובץ הרשמי">' . $bars . '</svg>'
			. '<div class="nlur2-tw"><table class="nlur2-t"><caption>מתחמים לפי שלב</caption><thead><tr><th scope="col">שלב</th><th scope="col">מתחמים בקובץ</th><th scope="col">דירות היום</th><th scope="col">דירות אחרי הבנייה</th><th scope="col">במפת הרשות</th></tr></thead><tbody>' . $rows . '</tbody></table></div>'
			. nadlan_urd_src( $fsrc . ' ' . $msrc . ' 188 מתחמים במפה מופיעים בלי שלב.' ) . '</section>';
		/* tracks: one stacked bar */
		$tr = (array) $f['tracks']; $tt = max( 1, array_sum( $tr ) ); $x = 418; $seg = ''; $leg = ''; $j = 0;
		foreach ( array( 'מיסוי', 'רשויות', 'טרם הוכרז', 'ללא מסלול בקובץ' ) as $k ) {
			$v = (int) ( $tr[ $k ] ?? 0 ); if ( ! $v ) { continue; }
			$w = round( 416 * $v / $tt ); $x -= $w;
			$seg .= '<rect x="' . $x . '" y="4" width="' . $w . '" height="26" class="t' . $j . '"/>';
			$leg .= '<span class="t' . $j . '"><i></i>' . esc_html( $k ) . ' <b>' . nadlan_urd_n( $v ) . '</b></span>';
			$j++;
		}
		$h .= '<section id="nlur2-tracks"><h2>מסלול מיסוי, מסלול רשויות ומתחמים שטרם הוכרזו</h2>'
			. '<p>במסלול מיסוי היזם יוזם והמתחם זכאי להטבות מס. במסלול רשויות הרשות המקומית מקדמת את התכנון. בחלק מהשורות בקובץ שדה המסלול ריק, והן מוצגות כאן בנפרד.</p>'
			. '<svg class="nlur2-svg" viewBox="0 0 420 34" role="img" aria-label="מתחמים לפי מסלול">' . $seg . '</svg><p class="nlur2-leg">' . $leg . '</p>'
			. nadlan_urd_src( $fsrc ) . '</section>';
		/* approved + execution */
		$by_d = array( 'ירושלים' => array(), 'תל אביב' => array(), 'המרכז' => array(), 'חיפה' => array(), 'הצפון' => array(), 'הדרום' => array(), 'יהודה ושומרון' => array() );
		$city_d = array(); foreach ( (array) $f['cities'] as $c ) { $city_d[ $c['city'] ] = $c['district']; $by_d[ $c['district'] ][] = $c; }
		$ap_by = array(); foreach ( (array) $f['approved'] as $a ) { $ap_by[ $city_d[ $a['city'] ] ?? 'המרכז' ][] = $a; }
		$ap = '';
		foreach ( array_keys( $by_d ) as $dn ) {
			$list = $ap_by[ $dn ] ?? array(); if ( ! $list ) { continue; }
			$r = '';
			foreach ( $list as $a ) {
				$plan = $a['plan'] ? ( $a['link'] ? '<a href="' . esc_url( $a['link'] ) . '" rel="noopener nofollow">' . esc_html( $a['plan'] ) . '</a>' : esc_html( $a['plan'] ) ) : '';
				$r .= '<tr><th scope="row">' . esc_html( $a['name'] ) . '</th><td>' . esc_html( $a['city'] ) . '</td><td>' . esc_html( str_replace( 'תכנית מאושרת ', '', $a['status'] ) ) . '</td><td>' . $plan . '</td><td>' . nadlan_urd_n( $a['ex'] ) . ' ← ' . nadlan_urd_n( $a['prop'] ) . '</td></tr>';
			}
			$ap .= '<details class="nlur2-d"><summary>מחוז ' . esc_html( $dn ) . ' · ' . count( $list ) . ' מתחמים מאושרים</summary><div class="nlur2-tw"><table class="nlur2-t"><caption>מתחמים מאושרים, מחוז ' . esc_html( $dn ) . '</caption><thead><tr><th scope="col">מתחם</th><th scope="col">עיר</th><th scope="col">שלב</th><th scope="col">מספר תכנית</th><th scope="col">דירות היום ← אחרי</th></tr></thead><tbody>' . $r . '</tbody></table></div></details>';
		}
		$h .= '<section id="nlur2-approved"><h2>מתחמי פינוי בינוי מאושרים</h2><p>' . nadlan_urd_n( count( (array) $f['approved'] ) ) . ' מתחמים בקובץ הרשמי עם תכנית מאושרת, לפי מחוז. מספר התכנית מוביל לאתר מינהל התכנון, שם מופיעים מסמכי התכנית ותאריכיה.</p>' . $ap . nadlan_urd_src( $fsrc ) . '</section>';
		$ex = (array) $f['execution']; $r = ''; $more = '';
		foreach ( $ex as $k => $a ) {
			$row = '<tr><th scope="row">' . esc_html( $a['name'] ) . '</th><td>' . esc_html( $a['city'] ) . '</td><td>' . nadlan_urd_n( $a['permits'] ) . '</td><td>' . nadlan_urd_n( $a['prop'] ) . '</td></tr>';
			if ( $k < 30 ) { $r .= $row; } else { $more .= $row; }
		}
		$head = '<thead><tr><th scope="col">מתחם</th><th scope="col">עיר</th><th scope="col">היתרים (יח"ד)</th><th scope="col">מתוך יח"ד מוצעות</th></tr></thead>';
		$h .= '<section id="nlur2-exec"><h2>פרויקטי פינוי בינוי בביצוע</h2><p>' . nadlan_urd_n( $f['in_execution'] ) . ' מתחמים מסומנים בקובץ כבביצוע, ובכ-' . nadlan_urd_n( $f['permits_complexes'] ) . ' מתחמים נרשמו היתרים. הטבלה מסודרת לפי מספר יחידות הדיור שקיבלו היתר.</p>'
			. '<div class="nlur2-tw"><table class="nlur2-t"><caption>המתחמים עם הכי הרבה היתרים</caption>' . $head . '<tbody>' . $r . '</tbody></table></div>'
			. ( $more ? '<details class="nlur2-d"><summary>עוד ' . ( count( $ex ) - 30 ) . ' מתחמים עם היתרים או בביצוע</summary><div class="nlur2-tw"><table class="nlur2-t"><caption>שאר המתחמים בביצוע</caption>' . $head . '<tbody>' . $more . '</tbody></table></div></details>' : '' )
			. nadlan_urd_src( $fsrc ) . '</section>';
		/* districts chart + a table per district */
		$dsum = array(); foreach ( $by_d as $dn => $cs ) { $dsum[ $dn ] = array_sum( wp_list_pluck( $cs, 'n' ) ); }
		$dmx = max( 1, max( $dsum ) ); $bars = ''; $i = 0;
		foreach ( $dsum as $dn => $v ) {
			if ( ! $v ) { continue; }
			$w = max( 4, round( 300 * $v / $dmx ) ); $y = 6 + $i * 30;
			$bars .= '<text x="416" y="' . ( $y + 15 ) . '" text-anchor="end" class="lb">' . esc_html( $dn ) . '</text><rect x="' . ( 316 - $w ) . '" y="' . ( $y + 2 ) . '" width="' . $w . '" height="18" rx="2" class="s2"/><text x="' . ( 310 - $w ) . '" y="' . ( $y + 15 ) . '" text-anchor="end" class="nv">' . nadlan_urd_n( $v ) . '</text>';
			$i++;
		}
		$tabs = '';
		foreach ( $by_d as $dn => $cs ) {
			if ( ! $cs ) { continue; }
			usort( $cs, function ( $a, $b ) { return $b['n'] - $a['n']; } );
			$r = '';
			foreach ( $cs as $c ) {
				$r .= '<tr><th scope="row">' . esc_html( $c['city'] ) . '</th><td>' . (int) $c['n'] . '</td><td>' . (int) $c['approved'] . '</td><td>' . (int) $c['exec'] . '</td><td>' . (int) $c['tax'] . '</td><td>' . (int) $c['auth'] . '</td><td>' . nadlan_urd_n( $c['existing'] ) . '</td><td>' . nadlan_urd_n( $c['proposed'] ) . '</td><td>' . ( $c['mult'] ? '× ' . esc_html( number_format( $c['mult'], 2 ) ) : '' ) . '</td><td>' . esc_html( nadlan_urd_dmy( $c['last_decl'] ) ) . '</td></tr>';
			}
			$tabs .= '<h3>מחוז ' . esc_html( $dn ) . '</h3><div class="nlur2-tw"><table class="nlur2-t nlur2-t--w"><caption>מתחמי התחדשות עירונית, מחוז ' . esc_html( $dn ) . '</caption><thead><tr><th scope="col">עיר</th><th scope="col">מתחמים</th><th scope="col">מאושרים</th><th scope="col">בביצוע</th><th scope="col">מסלול מיסוי</th><th scope="col">מסלול רשויות</th><th scope="col">דירות היום</th><th scope="col">אחרי הבנייה</th><th scope="col">מכפיל</th><th scope="col">הכרזה אחרונה</th></tr></thead><tbody>' . $r . '</tbody></table></div>';
		}
		$h .= '<section id="nlur2-cities"><h2>מפת התחדשות עירונית לפי עיר</h2><p>כל ' . (int) $f['localities'] . ' הערים בקובץ הרשמי, לפי מחוז: כמה מתחמים, כמה מאושרים ובביצוע, באיזה מסלול, כמה דירות יש היום וכמה יהיו אחרי הבנייה. המכפיל הוא חישוב שלנו: דירות אחרי הבנייה חלקי דירות היום.</p>'
			. '<svg class="nlur2-svg" viewBox="0 0 420 ' . ( 12 + $i * 30 ) . '" role="img" aria-label="מתחמים לפי מחוז">' . $bars . '</svg>' . $tabs . nadlan_urd_src( $fsrc . ' המחוז לפי רשימת היישובים של הלמ"ס ב-data.gov.il.' ) . '</section>';
		/* top 15 cities: today vs after building */
		$cs = (array) $f['cities']; usort( $cs, function ( $a, $b ) { return $b['proposed'] - $a['proposed']; } ); $cs = array_slice( $cs, 0, 15 );
		$pmx = max( 1, $cs[0]['proposed'] ?? 1 ); $bars = '';
		foreach ( $cs as $i => $c ) {
			$y = 6 + $i * 50; $wp = max( 4, round( 412 * $c['proposed'] / $pmx ) ); $we = max( 2, round( 412 * $c['existing'] / $pmx ) );
			$bars .= '<text x="416" y="' . ( $y + 13 ) . '" text-anchor="end" class="lb">' . esc_html( $c['city'] ) . '</text>'
				. '<text x="4" y="' . ( $y + 13 ) . '" text-anchor="start" class="nv">' . nadlan_urd_n( $c['existing'] ) . ' → ' . nadlan_urd_n( $c['proposed'] ) . ( $c['mult'] ? ' · ×' . esc_html( number_format( $c['mult'], 2 ) ) : '' ) . '</text>'
				. '<rect x="' . ( 416 - $wp ) . '" y="' . ( $y + 20 ) . '" width="' . $wp . '" height="20" rx="2" class="s2"/><rect x="' . ( 416 - $we ) . '" y="' . ( $y + 25 ) . '" width="' . $we . '" height="10" rx="2" class="s0"/>';
		}
		$h .= '<section id="nlur2-top"><h2>15 הערים עם הכי הרבה דירות אחרי הבנייה</h2><p>הפס הבהיר: דירות היום. הפס הכהה: דירות אחרי הבנייה לפי הקובץ הרשמי.</p>'
			. '<svg class="nlur2-svg" viewBox="0 0 420 ' . ( 10 + count( $cs ) * 50 ) . '" role="img" aria-label="דירות היום ואחרי הבנייה ב-15 ערים">' . $bars . '</svg>' . nadlan_urd_src( $fsrc ) . '</section>';
		/* declarations per year */
		$yr = (array) $f['by_year']; $ymx = max( 1, max( $yr ) ); $bars = ''; $k = 0; $n = count( $yr ); $bw = floor( 400 / max( 1, $n ) );
		foreach ( $yr as $year => $v ) {
			$hgt = round( 150 * $v / $ymx ); $x = 10 + $k * $bw; $cls = in_array( $year, array( '2024', '2025' ), true ) ? 'hi' : ( (string) $year === date( 'Y' ) ? 's0' : 's2' );
			$bars .= '<rect x="' . $x . '" y="' . ( 170 - $hgt ) . '" width="' . ( $bw - 3 ) . '" height="' . $hgt . '" class="' . $cls . '"/>';
			if ( 0 === $k % 5 || 'hi' === $cls || $k === $n - 1 ) { $bars .= '<text x="' . ( $x + ( $bw - 3 ) / 2 ) . '" y="186" text-anchor="middle" class="ax">' . esc_html( $year ) . '</text>'; }
			if ( 'hi' === $cls ) { $bars .= '<text x="' . ( $x + ( $bw - 3 ) / 2 ) . '" y="' . ( 164 - $hgt ) . '" text-anchor="middle" class="nv">' . (int) $v . '</text>'; }
			$k++;
		}
		$h .= '<section id="nlur2-years"><h2>כמה מתחמים הוכרזו בכל שנה</h2><p>לפי תאריך ההכרזה של כל מתחם בקובץ הרשמי. ב-2024 וב-2025 הוכרזו יותר מתחמים מבכל שנה קודמת. השנה האחרונה חלקית: עד ' . esc_html( nadlan_urd_dmy( $f['last_declaration'] ) ) . '.</p>'
			. '<svg class="nlur2-svg" viewBox="0 0 420 192" role="img" aria-label="מתחמים שהוכרזו בכל שנה">' . $bars . '</svg>' . nadlan_urd_src( $fsrc ) . '</section>';
		/* what a complex is, the stages, approval to permit, where to check */
		$h .= '<section id="nlur2-what"><h2>מה זה מתחם התחדשות עירונית</h2>'
			. '<p>ברשימת המתחמים של הרשות הממשלתית להתחדשות עירונית יש חמישה סוגים: מתחם שהוכרז לפי סעיף 14 לחוק הרשות, מתחם של גוף ציבורי, מתחם של יזם שעבר סף תכנוני, מתחם מועדף לדיור, ומתחם בביצוע, שבו ההיתרים נספרים מתוך הדירות המוצעות. מתחם פינוי בינוי כולל לפחות 24 דירות קיימות, ובמצב החדש לפחות 70 דירות או פי שניים מהקיים, הגבוה מביניהם.</p>'
			. '<p>ההכרזה פותחת מסלול. היא לא תכנית מאושרת ולא היתר, ולכן אין בה תאריך התחלת בנייה או אכלוס. בפינוי בינוי נדרשת הסכמה של 66% מבעלי הדירות במתחם, ולפחות 60% בכל בניין.</p></section>';
		$h .= '<section id="nlur2-time"><h2>כמה זמן עובר מאישור התכנית ועד היתר</h2><p>הרשות מפרסמת כמה שנים עברו בממוצע מאישור תכנית פינוי בינוי ועד ההיתר הראשון, לפי שנת ההיתר. זה ממוצע של מתחמים שכבר קיבלו היתר, ולא תחזית למתחם מסוים.</p>'
			. '<div class="nlur2-tw"><table class="nlur2-t"><caption>מאישור תכנית עד היתר ראשון, פינוי בינוי</caption><thead><tr><th scope="col">שנת ההיתר</th><th scope="col">שנים בממוצע</th><th scope="col">מתחמים</th></tr></thead><tbody>'
			. '<tr><th scope="row">2025</th><td>4.0</td><td>28</td></tr><tr><th scope="row">2024</th><td>4.0</td><td>43</td></tr><tr><th scope="row">2023</th><td>3.9</td><td>28</td></tr><tr><th scope="row">2022</th><td>4.1</td><td>33</td></tr><tr><th scope="row">2021</th><td>4.9</td><td>23</td></tr><tr><th scope="row">2016</th><td>6.0</td><td>7</td></tr>'
			. '</tbody></table></div>' . nadlan_urd_src( 'המקור: <a href="https://www.gov.il/he/pages/urban_renewal_report_2025" rel="noopener">דוח הרשות הממשלתית להתחדשות עירונית לשנת 2025</a>.' )
			. '<h3>מילון השלבים</h3><div class="nlur2-tw"><table class="nlur2-t"><caption>מה אומר כל שלב</caption><thead><tr><th scope="col">השלב בקובץ</th><th scope="col">מה זה אומר</th><th scope="col">מה בדרך כלל הצעד הבא</th></tr></thead><tbody>'
			. '<tr><th scope="row">תכנון ראשוני</th><td>עבודה על המתחם לפני שתכנית הוגשה לוועדה</td><td>הגשת תכנית לוועדה</td></tr>'
			. '<tr><th scope="row">תכנון סטטוטורי</th><td>התכנית בדיונים בוועדות התכנון</td><td>הפקדה, התנגדויות ואישור</td></tr>'
			. '<tr><th scope="row">תכנית מאושרת לפני מימוש</th><td>יש תכנית מאושרת ועוד אין היתר</td><td>בקשה להיתר בנייה</td></tr>'
			. '<tr><th scope="row">תכנית מאושרת במימוש</th><td>הביצוע התחיל</td><td>בנייה ומסירה</td></tr>'
			. '<tr><th scope="row">תכנית מאושרת אחרי רישוי</th><td>ניתנו היתרים לפי התכנית</td><td>תחילת עבודות</td></tr>'
			. '</tbody></table></div></section>';
		$h .= '<section id="nlur2-check"><h2>איך בודקים סטטוס של מתחם</h2><ol class="nlur2-steps">'
			. '<li>מקישים על העיר במפה בעמוד הזה ובוחרים את המתחם.</li>'
			. '<li>בודקים את סוג המתחם ברשימת המתחמים של הרשות.</li>'
			. '<li>מחפשים את מספר התכנית באתר מינהל התכנון ורואים את שלבה ואת תאריכי ההפקדה והאישור.</li>'
			. '<li>שואלים את מינהלת ההתחדשות העירונית בעירייה על ההסכמות ועל היזם.</li></ol>'
			. '<div class="nlur2-tw"><table class="nlur2-t"><caption>איפה בודקים מה</caption><thead><tr><th scope="col">מה רוצים לדעת</th><th scope="col">איפה</th><th scope="col">מה התשובה לא אומרת</th></tr></thead><tbody>'
			. '<tr><th scope="row">האם הבניין במתחם, ובאיזה שלב</th><td><a href="https://www.gov.il/he/departments/topics/mapa-renewal" rel="noopener">מפת הרשות ב-gov.il</a></td><td>מתי תתחיל בנייה</td></tr>'
			. '<tr><th scope="row">סוג המתחם</th><td><a href="https://www.gov.il/he/pages/mitchamim" rel="noopener">רשימת המתחמים של הרשות</a></td><td>מצב ההסכמות בבניין</td></tr>'
			. '<tr><th scope="row">שלב התכנית ותאריכיה</th><td><a href="https://mavat.iplan.gov.il/" rel="noopener">אתר מינהל התכנון</a></td><td>מי היזם ומה ההצעה</td></tr>'
			. '<tr><th scope="row">כל המתחמים בטבלה אחת</th><td><a href="' . esc_url( $f['url'] ) . '" rel="noopener">הקובץ הפתוח ב-data.gov.il</a></td><td>שינויים מאז העדכון האחרון של הקובץ</td></tr>'
			. '<tr><th scope="row">רוב ההסכמות והזכויות</th><td><a href="https://www.gov.il/he/departments/faq/renewal_faq" rel="noopener">שאלות ותשובות של הרשות</a></td><td>את המצב בבניין שלכם</td></tr>'
			. '</tbody></table></div></section>';
		/* FAQ, visible (the same list is the FAQPage schema) */
		$q = ''; foreach ( nadlan_urd_faq() as $qa ) { $q .= '<h3>' . esc_html( $qa[0] ) . '</h3><p>' . esc_html( $qa[1] ) . '</p>'; }
		$h .= '<section id="nlur2-faq"><h2>שאלות נפוצות על מפת ההתחדשות העירונית</h2>' . $q . '</section>';
		$h .= '<section id="nlur2-sources"><h2>איך נאסף המידע</h2><p>הטבלאות והגרפים בנויים מקובץ מתחמי ההתחדשות העירונית של משרד הבינוי והשיכון ב-data.gov.il (עודכן ' . esc_html( $fd ) . ', לפי תנאי השימוש של האתר, עם ציון המקור), ומספירת המתחמים במפת הרשות ב-gov.il (' . esc_html( $md ) . '). החישובים של מכפיל, מחוזות ושינויים בין המקורות הם שלנו. הנתונים לא כוללים תאריכי התחלת בנייה או אכלוס, ואנחנו לא מנחשים אותם. כשמקור אחד מתעדכן לפני השני, מוצגים שניהם עם התאריך.</p>'
			. '<ul class="nlur2-links"><li><a href="' . esc_url( $f['url'] ) . '" rel="noopener">קובץ מתחמי ההתחדשות העירונית, data.gov.il</a></li><li><a href="https://www.gov.il/he/departments/topics/mapa-renewal" rel="noopener">מפת מתחמי פינוי בינוי, gov.il</a></li><li><a href="https://www.gov.il/he/pages/mitchamim" rel="noopener">רשימת המתחמים של הרשות</a></li><li><a href="https://www.gov.il/he/departments/faq/renewal_faq" rel="noopener">שאלות ותשובות של הרשות</a></li><li><a href="https://www.gov.il/he/pages/urban_renewal_report_2025" rel="noopener">דוח הרשות לשנת 2025</a></li><li><a href="https://mavat.iplan.gov.il/" rel="noopener">מינהל התכנון</a></li></ul></section>';
		$css = '<style id="nlur2-css">.nlur2{--w:#fff;--i:#12202A;--i2:#3E4C58;--mu:#5E6A75;--ln:#D3DCE2;--sea:#2F6F86;--deep:#1F4B5C;--red:#C42550;--sea-t:#E6F0F3;--sans:"IBM Plex Sans Hebrew","IBM Plex Sans",system-ui,sans-serif;--disp:"Karantina","IBM Plex Sans Hebrew",system-ui,sans-serif;--mono:"IBM Plex Mono",ui-monospace,monospace;direction:rtl;color:var(--i2);font-family:var(--sans);margin-top:30px}'
			. '.nlur2 *{box-sizing:border-box}.nlur2 h2{font:600 clamp(1.25rem,2.4vw,1.55rem)/1.3 var(--sans)!important;color:var(--i)!important;margin:30px 0 10px!important}.nlur2 h3{font:600 1.05rem/1.4 var(--sans)!important;color:var(--i)!important;margin:18px 0 6px!important}'
			. '.nlur2 p{font:400 15.5px/1.75 var(--sans);max-width:72ch;margin:0 0 12px}.nlur2 a{color:var(--deep);text-decoration:underline;text-underline-offset:2px}'
			. '.nlur2-tiles{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border:1px solid var(--ln);border-radius:6px;background:var(--w);overflow:hidden;margin:6px 0 10px}.nlur2-tiles div{padding:12px 14px;border-inline-start:1px solid var(--ln);display:grid;gap:2px}.nlur2-tiles div:first-child{border-inline-start:0}'
			. '.nlur2-tiles span{font:500 12.5px/1.4 var(--sans);color:var(--mu)}.nlur2-tiles b{font:700 30px/1 var(--disp);color:var(--i);direction:ltr;text-align:right;unicode-bidi:plaintext;font-variant-numeric:tabular-nums}.nlur2-tiles small{font:400 11.5px/1.4 var(--mono);color:var(--mu)}'
			. '.nlur2-moved{font:500 14px/1.6 var(--sans)!important;color:var(--i)!important;border-inline-start:3px solid var(--red);padding:4px 10px;background:#FBE9EE}'
			. '.nlur2-svg{width:100%;max-width:640px;height:auto;display:block;margin:8px 0 6px}.nlur2-svg .lb{font:600 14px var(--sans);fill:var(--i)}.nlur2-svg .nv{font:500 12.5px var(--mono);fill:var(--i2)}.nlur2-svg .ax{font:400 11px var(--mono);fill:var(--mu)}'
			. '.nlur2-svg .s0{fill:#9DB7C3}.nlur2-svg .s1{fill:#5C93A8}.nlur2-svg .s2{fill:var(--sea)}.nlur2-svg .s3{fill:var(--deep)}.nlur2-svg .s4{fill:var(--i)}.nlur2-svg .s5{fill:#B9C3CA}.nlur2-svg .hi{fill:var(--red)}'
			. '.nlur2-svg .t0{fill:var(--sea)}.nlur2-svg .t1{fill:var(--deep)}.nlur2-svg .t2{fill:#9DB7C3}.nlur2-svg .t3{fill:#D3DCE2}.nlur2-leg{display:flex;flex-wrap:wrap;gap:14px;font:500 13px var(--sans)}.nlur2-leg i{display:inline-block;width:10px;height:10px;margin-inline-end:5px;vertical-align:-1px}'
			. '.nlur2-leg .t0 i{background:var(--sea)}.nlur2-leg .t1 i{background:var(--deep)}.nlur2-leg .t2 i{background:#9DB7C3}.nlur2-leg .t3 i{background:#D3DCE2}'
			. '.nlur2-tw{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:6px 0 4px}.nlur2-t{width:100%;border-collapse:collapse;font:400 13.5px/1.5 var(--sans);background:var(--w)}.nlur2-t caption{text-align:right;font:600 13px var(--sans);color:var(--mu);padding:0 0 6px}'
			. '.nlur2-t th,.nlur2-t td{border-bottom:1px solid var(--ln);padding:7px 8px;text-align:right;vertical-align:top}.nlur2-t thead th{font-weight:600;color:var(--i);background:var(--sea-t);white-space:nowrap}.nlur2-t td{font-family:var(--mono);font-size:12.5px;font-variant-numeric:tabular-nums}.nlur2-t--w{min-width:780px}'
			. '.nlur2-d{border:1px solid var(--ln);border-radius:6px;background:var(--w);margin:8px 0;padding:0 12px}.nlur2-d summary{cursor:pointer;font:600 14px/2.6 var(--sans);color:var(--i)}'
			. '.nlur2-src{font:400 12px/1.6 var(--sans)!important;color:var(--mu)!important}.nlur2-steps{font:400 15px/1.8 var(--sans);padding-inline-start:20px}.nlur2-links{font:400 14px/1.9 var(--sans)}'
			. '@media(max-width:720px){.nlur2-tiles{grid-template-columns:repeat(2,minmax(0,1fr))}.nlur2-tiles div:nth-child(3){border-inline-start:0}.nlur2-tiles div{border-top:1px solid var(--ln)}.nlur2-tiles b{font-size:26px}}</style>';
		return $css . '<div class="nlur2" id="nlur2">' . $h . '</div>';
	}
}
