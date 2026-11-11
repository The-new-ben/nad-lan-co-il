<?php
/**
 * nadlan-config - THE APARTMENT-DESIGN TOOLS (HAD-707, 11.11.2026; Ben: "tools on top of tools ... every page must be the best
 * on the web for its phrase"). Seventeen instruments of one family in assets/instruments/tools/design.js on
 * assets/instruments/data/design.json (tools/instruments/build_design_data.py, from the HAD-705 price research; never a site name).
 * This file adds them to the registry through the 'nadlan_nli_tools' filter (like garden-tools.php) and prints, for each one, the
 * plain summary the shortcode shows before the script runs (numbers readable without JavaScript, for search engines and AI answers).
 * Loaded by inc/instruments.php only if present; the summary is reached through one line in nadlan_nli_summary() (see
 * docs/design-lab/apartment-designer/tools/NOTES.md for the exact hunk), so a rollback that removes this file leaves the engine working.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_dsg_tools' ) ) {

	/** id => name, kicker, category, description (the SoftwareApplication JSON-LD reads these). */
	function nadlan_dsg_tools() {
		return array(
			'dsgfee'     => array( 'מחשבון עיצוב פנים: כמה עולה מעצב פנים לדירה', 'מחשבון · עיצוב פנים', 'FinanceApplication', 'כמה עולה מעצב פנים לדירה לפי השטח, מספר החדרים וסוג השירות (פגישות ייעוץ, תכנון בלבד, ליווי עד הכניסה), בכל שיטות התמחור זו לצד זו: לפי מטר, לפי גודל הדירה, לפי שעה, לפי פגישה ואחוז מתקציב העבודות, בטווחים שפורסמו בישראל בנובמבר 2026.' ),
			'dsgquote'   => array( 'בדיקת הצעת מחיר של מעצבת פנים', 'בדיקה · הצעת מחיר', 'UtilitiesApplication', 'בדיקת הצעת מחיר לעיצוב פנים: המחיר למטר מול הטווח שפורסם בישראל, מול המחיר לדירה באותו גודל, עם מע"מ ובלי, ועשרה פריטים שבדרך כלל נמצאים בהצעה מלאה (תכניות, הדמיות, כתב כמויות, תכנון מטבח ותאורה, ליווי ופיקוח) ומה עולה כל אחד בנפרד.' ),
			'dsgbudget'  => array( 'תקציב לעיצוב דירה חדשה', 'מחשבון · תקציב לעיצוב דירה', 'FinanceApplication', 'תקציב לעיצוב דירה חדשה מקבלן: רהיטים, מעצב פנים, מטבח, פרקט, מיזוג, נקודות חשמל, וילונות וצביעה, בשלוש רמות ועם רזרבה, חדר אחרי חדר, וכמה כל חלק לוקח מהסכום.' ),
			'dsgfurnish' => array( 'כמה עולה לרהט דירה', 'מחשבון · ריהוט דירה', 'FinanceApplication', 'כמה עולה לרהט דירת 2 עד 6 חדרים בשלוש רמות: סלון, פינת אוכל, חדרי שינה, חדר עבודה, מרפסת, תאורה ומוצרי חשמל, פריט אחרי פריט, לפי טווחי מחירים שפורסמו בישראל.' ),
			'dsgkitchen' => array( 'כמה עולה מטבח: מחשבון לפי מטר', 'מחשבון · מטבח', 'FinanceApplication', 'מחיר מטבח לפי אורך במטרים ורמת הארונות, עם משטח קוורץ או גרניט פורצלן, אי, כיור ומכשירים, ובדיקה מול המחיר שפורסם למטבח שלם ולתכנון מטבח.' ),
			'dsgfloor'   => array( 'מחשבון ריצוף ופרקט', 'מחשבון · ריצוף ופרקט', 'UtilitiesApplication', 'כמה מטר וכמה קרטונים להזמין ומה המחיר כולל עבודה: פורצלן 60, 80 ו־120, פרקט למינציה, פרקט עץ תלת שכבתי ו־SPC, עם פחת לפי הנחה ישרה, באלכסון או בפישבון, ופנלים.' ),
			'dsgpaint'   => array( 'מחשבון צביעת דירה', 'מחשבון · צביעת דירה', 'UtilitiesApplication', 'שטח הקירות בלי דלתות וחלונות, תקרות, כמה ליטר צבע ואילו פחים לקנות, ומחיר צבעי לפי מ"ר מול המחיר שפורסם לדירת 4 חדרים שלמה, או צביעה לבד.' ),
			'dsgsofa'    => array( 'האם הספה תיכנס: מידות ספה לסלון', 'בדיקה · מידות ספה לסלון', 'UtilitiesApplication', 'האם הספה נכנסת לסלון עם מעבר נוח מולה, ואם היא עוברת בפתח הכניסה, בפנייה במסדרון ובמעלית, עם שרטוט בקנה מידה שמתעדכן עם כל מידה.' ),
			'dsgrug'     => array( 'איזה גודל שטיח לסלון', 'בחירה · גודל שטיח לסלון', 'UtilitiesApplication', 'איזו מידת שטיח מוכנה מתאימה לפינת הישיבה לפי אורך הספה, המרחק עד המזנון ומידות הסלון, בשרטוט בקנה מידה, עם המחיר שפורסם למידה.' ),
			'dsgdining'  => array( 'פינת אוכל: כמה מקום צריך לשולחן ולכסאות', 'בדיקה · פינת אוכל', 'UtilitiesApplication', 'גודל שולחן האוכל למספר הסועדים, מלבני או עגול, המרווח מאחורי הכיסאות לפי הנחיות תכנון מקובלות, מספר הסועדים הגדול ביותר שנכנס, שרטוט בקנה מידה ומחיר.' ),
			'dsgbed'     => array( 'חדר שינה קטן: איזו מיטה נכנסת', 'בדיקה · חדר שינה', 'UtilitiesApplication', 'איזו מיטה נכנסת לחדר השינה עם מעבר בצדדים ולמרגלות, וארון בגדים מול המיטה או בצידה, בשרטוט בקנה מידה, עם המיטה הגדולה ביותר שנכנסת והמחירים.' ),
			'dsglight'   => array( 'תכנון תאורה לבית: כמה אור צריך בכל חדר', 'מחשבון · תכנון תאורה לבית', 'UtilitiesApplication', 'כמה לומן צריך בכל חדר לפי השטח, כמה ספוטים, גופי תקרה, מנורות תלויות או מטרים של פס לד, איזה גוון אור בקלווין, וכמה עולות נקודות התאורה.' ),
			'dsgpoints'  => array( 'נקודות חשמל בדירה חדשה: מה במפרט ומה להוסיף', 'מחשבון · נקודות חשמל', 'FinanceApplication', 'משווים את נקודות החשמל שבמפרט הדירה למה שרוצים בכל חדר, ומקבלים כמה נקודות להוסיף וכמה זה עולה לפי המחיר שפורסם לנקודה.' ),
			'dsgwho'     => array( 'מעצב פנים, הום סטיילינג או אדריכל: מי מתאים לכם', 'בחירה · איש המקצוע', 'UtilitiesApplication', 'ארבע שאלות על העבודה ועל העזרה שאתם רוצים, ותשובה: פגישת ייעוץ, הום סטיילינג, מעצב פנים לתכנון בלבד או לליווי מלא, או אדריכל, עם המחיר שפורסם לכל אפשרות.' ),
			'dsgtime'    => array( 'לוח זמנים לדירה חדשה: מהחתימה ועד המעבר', 'לוח זמנים · דירה חדשה', 'UtilitiesApplication', 'מחודש המסירה שבחוזה: סדר ההחלטות בדירה חדשה מקבלן, מבחירת המעצב והשינויים אצל היזם ועד המטבח, הרהיטים והמעבר, והחודש האחרון שהגיוני לסגור כל אחת, עם משך הבנייה הממוצע של הלשכה המרכזית לסטטיסטיקה.' ),
			'dsgstyle'   => array( 'סגנונות עיצוב פנים: איזה סגנון שלכם', 'שאלון · סגנונות עיצוב פנים', 'UtilitiesApplication', 'חמש שאלות, וסגנון עיצוב הפנים שלכם מתוך שבעה (מודרני, סקנדינבי, תעשייתי, כפרי, בוהו, יפני־סקנדינבי, ים תיכוני) עם חמישה צבעים, החומרים שלו ורשימת רהיטים לסלון בטווח מחיר.' ),
			'dsgcurtain' => array( 'כמה עולים וילונות ותריסים', 'מחשבון · וילונות ותריסים', 'FinanceApplication', 'לפי רוחב וגובה של כל חלון: שטח החלונות, ומה עולים וילונות בהזמנה ותריסי גלילה חשמליים לפי המחירים שפורסמו למ"ר.' ),
		);
	}

	add_filter( 'nadlan_nli_tools', function ( $tools ) {
		// Related links: live pages only. Add /design-studio/ and its two siblings here once Ben publishes them (NOTES.md).
		$rel = array( '/design-studio/' => 'עיצוב דירה אונליין', '/design-studio/designer-cost/' => 'מעצבת פנים מחיר', '/buying-apartment/' => 'מדריך קניית דירה', '/guides/new-apartment-buyer-changes/' => 'שינויי דיירים בדירה חדשה', '/home-inspection/' => 'בדק בית', '/apartment-purchase-cost-calculator/' => 'עלות רכישה כוללת' );
		foreach ( nadlan_dsg_tools() as $id => $t ) {
			$tools[ $id ] = array( 'file' => 'design', 'name' => $t[0], 'kicker' => $t[1], 'cat' => $t[2], 'desc' => $t[3], 'data' => array( 'design.json' ), 'related' => $rel );
		}
		return $tools;
	} );

	/* A design tool placed inside a section of a page titles itself one level under that section:
	   [nadlan_tool id="dsgsofa" h="4"] prints its name as an h4 (h="3" as an h3). Without h nothing changes. */
	add_filter( 'do_shortcode_tag', function ( $out, $tag, $attr ) {
		if ( 'nadlan_tool' !== $tag || ! is_array( $attr ) || empty( $attr['id'] ) || 0 !== strpos( (string) $attr['id'], 'dsg' ) || empty( $attr['h'] ) ) { return $out; }
		$h = (string) $attr['h'];
		if ( '3' !== $h && '4' !== $h ) { return $out; }
		$new = preg_replace( '/<h2 class="nli__title">(.*?)<\/h2>/s', '<h' . $h . ' class="nli__title">$1</h' . $h . '>', (string) $out, 1 );
		if ( null === $new ) { return $out; }
		// inside a page section the tool does not repeat its "related" row: a page with ten tools would print the same links ten times
		$cut = preg_replace( '/<nav class="nli__rel"[^>]*>.*?<\/nav>/s', '', $new, 1 );
		return null === $cut ? $new : $cut;
	}, 10, 3 );

	/** The plain summary of a design tool: one sentence and a table of the published ranges it uses (or of the rules it applies). */
	function nadlan_dsg_summary( $id ) {
		static $d = false; // the 36 KB file is read once per request, not once per tool
		if ( false === $d ) {
			$path = dirname( __DIR__ ) . '/assets/instruments/data/design.json';
			$d = is_readable( $path ) ? json_decode( (string) file_get_contents( $path ), true ) : null;
		}
		if ( ! is_array( $d ) || empty( $d['items'] ) || empty( $d['fees'] ) || ! is_array( $d['items'] ) || ! is_array( $d['fees'] ) || empty( $d['rules'] ) || ! is_array( $d['rules'] ) ) { return ''; }
		$all = $d['items'] + $d['fees']; $R = $d['rules'];
		$vat = array( 'included' => 'כולל מע"מ', 'mixed' => 'מעורב', 'unknown' => 'לא צוין' );
		$n = function ( $x ) { return number_format( (float) $x ); };
		$rng = function ( $it ) use ( $n ) {  // the usual band when published, else the full range; an open top says "and up"
			$typ = null !== $it['tlo'] && null !== $it['thi'];
			$lo = $typ ? $it['tlo'] : $it['low']; $hi = $typ ? $it['thi'] : $it['high'];
			$rough = 'low' === $it['conf'] || $it['n'] < 2 || ! $typ;
			$pct = 'אחוז מהתקציב' === $it['unit'];
			$s = null === $hi ? 'מ־' . $n( $lo ) . ' ₪ ומעלה' : ( $pct ? $n( $lo ) . '% עד ' . $n( $hi ) . '%' : $n( $lo ) . ' עד ' . $n( $hi ) . ' ₪' );
			return $s . ( $pct ? '' : ' ' . $it['unit'] ) . ( $rough ? ' (גס)' : '' );
		};
		$table = function ( $ids, $caption ) use ( $all, $rng, $vat ) {
			$t = '<table><caption>' . esc_html( $caption ) . '</caption><thead><tr><th>פריט</th><th>טווח שפורסם</th><th>מע"מ</th><th>מקורות</th></tr></thead><tbody>';
			foreach ( $ids as $k ) {
				if ( empty( $all[ $k ] ) ) { continue; }
				$it = $all[ $k ];
				$t .= '<tr><td>' . esc_html( preg_replace( '/^אריח /u', '', $it['name'] ) ) . '</td><td>' . esc_html( $rng( $it ) ) . '</td><td>' . esc_html( isset( $vat[ $it['vat'] ] ) ? $vat[ $it['vat'] ] : 'לא צוין' ) . '</td><td>' . (int) $it['n'] . '</td></tr>';
			}
			return $t . '</tbody></table>';
		};
		$rules = function ( $keys, $caption ) use ( $R ) {
			$kind = array( 'standard' => 'הנחיה או נתון רשמי', 'thumb' => 'כלל אצבע מקובל', 'assumption' => 'הנחה שלנו' );
			$t = '<table><caption>' . esc_html( $caption ) . '</caption><thead><tr><th>מה</th><th>כמה</th><th>על מה זה מבוסס</th></tr></thead><tbody>';
			foreach ( $keys as $k => $unit ) {
				if ( empty( $R[ $k ] ) || is_array( $R[ $k ]['v'] ) ) { continue; }
				$t .= '<tr><td>' . esc_html( $R[ $k ]['he'] ) . '</td><td>' . esc_html( $R[ $k ]['v'] . $unit ) . '</td><td>' . esc_html( $kind[ $R[ $k ]['kind'] ] ) . '</td></tr>';
			}
			return $t . '</tbody></table>';
		};
		$when = 'טווחי מחירים שפורסמו בישראל, נקראו ב' . esc_html( $d['readHe'] ) . '. "גס" = מקור אחד או ביטחון נמוך.';
		switch ( $id ) {
			case 'dsgfee':
				return '<p>מעצב פנים לדירה מתמחר בכמה שיטות: לפי מטר, לפי גודל הדירה, לפי שעה, לפי פגישה או באחוז מתקציב העבודות. דירת 4 חדרים של 100 מ"ר עם ליווי מלא: בערך 32,500 עד 45,000 ₪ לפי השטח. ' . $when . '</p>'
					. $table( array( 'fee_m2', 'fee_3rooms', 'fee_4rooms', 'fee_5rooms', 'fee_hour', 'fee_meeting', 'fee_percent', 'fee_room' ), 'מחירי מעצבי פנים בישראל' );
			case 'dsgquote':
				return '<p>כדי לבדוק הצעת מחיר של מעצבת פנים מחלקים את הסכום בשטח הדירה ומשווים למחיר למ"ר שפורסם, ובודקים שכתובים בה התוצרים: תכניות עבודה, הדמיות, כתב כמויות, תכנון מטבח ותאורה, ליווי ופיקוח ופריסת תשלומים. ' . $when . '</p>'
					. $table( array( 'fee_m2', 'fee_meeting', 'render_view', 'bill_of_quantities', 'fee_kitchen_plan', 'fee_lighting_plan', 'shopping_day' ), 'מה עולה כל חלק כשמזמינים אותו בנפרד' );
			case 'dsgbudget':
			case 'dsgfurnish':
				return '<p>' . ( 'dsgbudget' === $id ? 'תקציב לעיצוב דירה חדשה בונים מהרהיטים, מהמעצב, מהמטבח, מהפרקט, מהמיזוג ומנקודות החשמל, ומוסיפים רזרבה של 10% עד 15% (כלל אצבע). ' : 'כמה עולה לרהט דירה: מחברים את המחיר של כל פריט בכל חדר. ' ) . $when . '</p>'
					. $table( array( 'furnish_2_3r_basic', 'furnish_2_3r_mid', 'furnish_4_5r_basic', 'furnish_4_5r_mid', 'furnish_4_5r_high', 'sofa_3seat', 'dining_set_6', 'bed_double_with_mattress', 'wardrobe_sliding_2m', 'bed_single', 'desk', 'fridge', 'dishwasher', 'ac_minicentral_4rooms_total', 'engineered_parquet' ), 'ריהוט ופריטים, מחירים שפורסמו' );
			case 'dsgkitchen':
				return '<p>מחיר מטבח מחשבים לפי מטר: ארונות לפי הרמה כפול האורך, ועוד משטח, אי, כיור ומכשירים. המקורות לא מסכימים מה כלול ב"מחיר למטר", ולכן מבקשים שיהיה כתוב. ' . $when . '</p>'
					. $table( array( 'kitchen_cab_basic', 'kitchen_cab_mid', 'kitchen_cab_premium', 'worktop_quartz', 'worktop_porcelain', 'kitchen_island', 'kitchen_sink', 'kitchen_full', 'oven_builtin', 'hob', 'hood', 'dishwasher', 'fridge', 'fee_kitchen_plan' ), 'מחירי מטבחים' );
			case 'dsgfloor':
				return '<p>כמה להזמין: שטח הרצפה ועוד פחת (כלל אצבע: הנחה ישרה 8%, באלכסון או בפישבון 15%), חלקי המ"ר שבקרטון, מעוגל למעלה. 30 מ"ר בהנחה ישרה עם קרטונים של 2 מ"ר: 17 קרטונים. ' . $when . '</p>'
					. $table( array( 'tile_material_60', 'tile_material_80', 'tile_material_120', 'tile_laying', 'tile_supplied_laid', 'laminate', 'engineered_parquet', 'spc_vinyl', 'skirting' ), 'מחירי ריצוף ופרקט למ"ר' );
			case 'dsgpaint':
				return '<p>שטח הקירות הוא היקף החדר כפול הגובה, פחות דלתות (כ־1.7 מ"ר לדלת) וחלונות. ליטר צבע אקרילי צובע כ־10 מ"ר בכל פעם (כתוב על הפח), ובדרך כלל צובעים פעמיים. ' . $when . '</p>'
					. $table( array( 'wall_paint_m2', 'paint_4rooms', 'wallpaper_roll', 'wallpaper_hanging' ), 'מחירי צביעה' );
			case 'dsgsofa':
				return '<p>לפני שקונים ספה מודדים את הקיר, את העומק עד הטלוויזיה, את פתח הכניסה ואת המסדרון. מעבר נוח מול הספה 90 ס"מ, ובין הספה לשולחן הסלון 40 עד 50 ס"מ. ספה עוברת בפתח אם הצד הצר שלה (עומק או גובה) צר מהפתח.</p>'
					. $rules( array( 'walk_main_cm' => ' ס"מ', 'walk_min_cm' => ' ס"מ', 'sofa_table_gap_cm' => ' ס"מ' ), 'המרווחים בסלון' ) . $table( array( 'sofa_3seat', 'sofa_corner', 'coffee_table', 'tv_console' ), 'מחירי ספות ורהיטי סלון' );
			case 'dsgrug':
				return '<p>גודל שטיח לסלון: השטיח בולט 15 עד 20 ס"מ מכל צד של הספה, הרגליים הקדמיות של הספה עומדות עליו, ונשארת רצפה גלויה ליד הקירות. מידות מוכנות: 120×170, 160×230, 200×290, 240×340, 300×400 ס"מ. ' . $when . '</p>'
					. $table( array( 'rug_160x230', 'rug_200x300' ), 'מחירי שטיחים' );
			case 'dsgdining':
				return '<p>לכל סועד בשולחן מלבני 60 ס"מ, ושולחן ל־6 הוא בערך 180 על 90 ס"מ. מקצה השולחן לקיר: 81 ס"מ כשאין מעבר, 91 כשעוברים בצד, 112 כשעוברים מאחורי סועד.</p>'
					. $rules( array( 'seat_width_cm' => ' ס"מ', 'table_depth_cm' => ' ס"מ', 'chair_wall_cm' => ' ס"מ', 'chair_edge_cm' => ' ס"מ', 'chair_walk_cm' => ' ס"מ' ), 'המידות בפינת האוכל' ) . $table( array( 'dining_set_6', 'dining_table_6', 'dining_chair' ), 'מחירי פינות אוכל' );
			case 'dsgbed':
				return '<p>בצד המיטה שנכנסים ממנו משאירים 60 ס"מ, ולמרגלותיה 60 עד 90. ארון בגדים עמוק 60 ס"מ, ומולו 90 ס"מ לדלתות או 60 להזזה. מיטה זוגית 160 עם מעברים משני הצדדים צריכה חדר ברוחב 2.80 מטר לפחות.</p>'
					. $rules( array( 'bed_side_cm' => ' ס"מ', 'bed_foot_cm' => ' ס"מ', 'wardrobe_depth_cm' => ' ס"מ', 'wardrobe_front_hinged_cm' => ' ס"מ', 'wardrobe_front_sliding_cm' => ' ס"מ' ), 'המידות בחדר השינה' ) . $table( array( 'bed_double_with_mattress', 'bed_single', 'mattress_160', 'wardrobe_per_m', 'wardrobe_sliding_2m' ), 'מחירי מיטות וארונות' );
			case 'dsglight':
				$lux = $R['lux']['v']; $kel = $R['kelvin']['v'];
				$names = array( 'living' => 'סלון', 'dining' => 'פינת אוכל', 'kitchen' => 'מטבח', 'bedroom' => 'חדר שינה', 'kids' => 'חדר ילדים או עבודה', 'bath' => 'חדר רחצה', 'hall' => 'מסדרון' );
				$t = '<table><caption>תאורה כללית לפי חדר (כלל אצבע)</caption><thead><tr><th>חדר</th><th>לוקס</th><th>קלווין</th><th>לומן לחדר של 12 מ"ר</th></tr></thead><tbody>';
				foreach ( $names as $k => $nm ) { $t .= '<tr><td>' . esc_html( $nm ) . '</td><td>' . (int) $lux[ $k ] . '</td><td>' . esc_html( $kel[ $k ] ) . '</td><td>' . $n( $lux[ $k ] * 12 * $R['lumen_factor']['v'] ) . '</td></tr>'; }
				return '<p>כמה אור צריך: לוקס כפול השטח, ועוד 25% לאור שנבלע בקירות. סלון של 25 מ"ר: כ־4,700 לומן, 8 ספוטים של 600 לומן. ' . $when . '</p>' . $t . '</tbody></table>' . $table( array( 'lighting_point', 'fee_lighting_plan', 'lighting_fixtures_apartment' ), 'מחירי תאורה' );
			case 'dsgpoints':
				return '<p>נקודת חשמל שמוסיפים לפני הטיח, דרך השינויים אצל היזם, זולה בהרבה מנקודה שחוצבים אחרי המסירה. את המספר במפרט מעתיקים ממפרט הדירה. ' . $when . '</p>'
					. $table( array( 'electric_point', 'lighting_point', 'smart_home_basic' ), 'מחירי נקודות חשמל' );
			case 'dsgwho':
				return '<p>שינוי שדורש היתר עובר דרך אדריכל או מהנדס. כשאין עבודות בנייה, הום סטיילינג מלביש את הדירה. מעצב פנים מתכנן ומלווה גימורים, מטבח ושינויים. לאדריכל לא מצאנו מחיר שפורסם לדירה. ' . $when . '</p>'
					. $table( array( 'fee_meeting', 'styling_apartment', 'styling_room', 'fee_3rooms', 'fee_4rooms', 'fee_5rooms' ), 'מחירי אנשי המקצוע' );
			case 'dsgtime':
				$c = $R['build_months_cbs']['v'];
				$t = '<ol>';
				foreach ( $d['steps'] as $s ) { $m = (int) $s['m']; $t .= '<li>' . esc_html( $s['he'] ) . ': ' . esc_html( 0 === $m ? 'בחודש המסירה' : ( $m < 0 ? abs( $m ) . ' חודשים לפני המסירה' : $m . ' חודשים אחרי המסירה' ) ) . '</li>'; }
				return '<p>בניין שהסתיים ב־2025 נבנה בממוצע ' . esc_html( $c[0] ) . ' חודשים (' . esc_html( $c[1] ) . ' בממוצע לפי מספר הדירות, הלשכה המרכזית לסטטיסטיקה). הסדר שמקובל בדירה חדשה מקבלן, והחודש האחרון שהגיוני לסגור כל שלב (מקובל, לא כלל; החוזה עם היזם קובע):</p>' . $t . '</ol>';
			case 'dsgstyle':
				return '<p>שבעה סגנונות עיצוב פנים: מודרני נקי, סקנדינבי, תעשייתי, כפרי, בוהו, יפני־סקנדינבי וים תיכוני. המחיר של הרהיטים תלוי ברמה ולא בסגנון. ' . $when . '</p>'
					. $table( array( 'sofa_3seat', 'armchair', 'coffee_table', 'tv_console', 'rug_200x300', 'floor_lamp' ), 'רהיטי סלון, מחירים שפורסמו' );
			case 'dsgcurtain':
				return '<p>מחשבים את שטח החלונות (רוחב כפול גובה) וכופלים במחיר למ"ר. בתריס יש מחיר מינימום לחלון קטן. ' . $when . '</p>'
					. $table( array( 'curtain_m2', 'curtain_window', 'shutter_electric_m2' ), 'מחירי וילונות ותריסים' );
		}
		return '';
	}
}
