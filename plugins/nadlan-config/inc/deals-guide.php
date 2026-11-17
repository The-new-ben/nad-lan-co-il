<?php
/**
 * nadlan-config - the guide of the developer deals map (HAD-743 + HAD-682, Ben 16.11.2026). Design: Claude Design canvas board 13.
 * A small computer-made face in the corner of /developer-deals/ that reacts to what the visitor does ON THE PAGE (the cash he
 * set, the deal he tapped, a pause on the map, a return visit) with one true, positive fact from the published deal, what is
 * worth checking, and the plain words that she does not recommend and this is not advice. She also acts: shows a deal on the
 * map, lights the deals that fit, opens the calculator or the area alert, through the map's own functions (window.NLDM).
 *
 * Laws: never sells, never "כדאי" or "הזדמנות", never invents a number (every number comes from the deal as published),
 * never a broker (no viewings, no offers), says when she has no checked answer. Injected by JavaScript only, no headings and
 * no keyword text in the page. Sound only after a tap. One tap closes her and she stays closed.
 * Public on the Hebrew page since 1.72.693 (Ben 17.11.2026); the option nadlan_dg = 'off' takes her off. She offers to leave a name
 * and a mobile number (an ordinary lead in the Lead Inbox, source deals_guide, with the site's consent line), never a video call.
 * Voice: every line is fixed text with an id. A recorded clip plays only if the option nadlan_dg_clips lists the line id with
 * the md5 prefix of its CURRENT text, so a changed line can never play an old recording. Without a clip she shows captions.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_dg_on' ) ) {
	function nadlan_dg_on() {
		if ( ! function_exists( 'nadlan_dm_is_page' ) || ! nadlan_dm_is_page() ) { return false; }
		/* public since 1.72.693 (Ben 17.11: "stop putting things behind switches"); the option nadlan_dg = 'off' takes her off */
		return 'off' !== get_option( 'nadlan_dg', 'on' );
	}
}

if ( ! function_exists( 'nadlan_dg_deal_lines' ) ) {
	/** What she says about each deal (true, from the published terms) and what is worth checking. Keyed by the deal id. */
	function nadlan_dg_deal_lines() {
		$g = function ( $where, $years, $from ) {
			return array(
				$where . ' של גינדי: 20% בחתימה ו-50% במסירה. את היתרה לוקחים כהלוואה ומחזירים ' . $years . ' שנים אחרי האכלוס, והחברה נושאת בריבית ובהצמדה של ההלוואה.',
				'המחיר שפורסם, מ-' . $from . ' מיליון שקל, לא כולל את ההלוואה. שווה לבקש את המחיר המלא איתה, ולבדוק מול הבנק.',
			);
		};
		return array(
			'gindi-love'   => $g( 'LOVE בגליל ים, הרצליה,', '10', '4.2' ),
			'gindi-efal'   => $g( 'רמת אפעל ברמת גן', '10', '3.3' ),
			'gindi-azar'   => $g( 'כפר אז"ר', '8', '2.7' ),
			'gindi-ayalon' => $g( 'נווה איילון באור יהודה', '10', '2.1' ),
			'melisron'     => array( 'אביב מליסרון, בשמונה פרויקטים: 0% הון עצמי בכניסה, בעזרת הלוואה כנגד נכס קיים, גם של ההורים. החברה נושאת במימון ובריבית עד האכלוס.', 'שווה לבדוק באילו דירות זה חל, ומה ההלוואה דורשת מהנכס שמשעבדים.' ),
			'upview'       => array( 'UPVIEW בלוד, של קבוצת אהרוני: 0% הון עצמי עד המסירה, במגדל ובבנייני הבוטיק. מ-2.15 מיליון שקל, לפי הפרסום.', 'במסירה משלמים את רוב המחיר, ולכן שווה אישור עקרוני למשכנתא כבר עכשיו.' ),
			'infinity'     => array( 'H Infinity בתל אביב, של קבוצת חג׳ג׳: מיליון שקל בחתימה ומקבלים מפתח. היתרה כשלוש שנים אחרי האכלוס, בלי ריבית ובלי הצמדה.', 'שווה לקרוא בחוזה איך מובטחת השכירות המינימלית, ומי משלם אותה.' ),
			'ytown'        => array( 'Y TOWN בראשון לציון, של צרפתי: הטבה של עד 7,000 שקל בחודש, לכ-4 שנים עד האכלוס.', 'הסכום הוא עד 7,000. שווה לשאול כמה מקבלים בדירה שבחרתם.' ),
			'benshemen'    => array( 'נופי בן שמן בלוד, של אאורה: נכנסים עם 550 אלף שקל, והיתרה בעוד שנה וחצי.', 'שווה לבדוק אם היתרה צמודה למדד, ומה המחיר בתשלום רגיל.' ),
			'noga'         => array( 'נגה בנוף הגליל, של בראל: מסלול 11/89, הלוואת קבלן של חצי מהמחיר שהיזם מממן, והנחה של 8 עד 10 אחוזים מהמחירון.', 'שווה לבקש את תנאי הלוואת הקבלן בכתב: מתי מחזירים ומה קורה אם מוכרים.' ),
			'biltmore'     => array( 'Biltmore 16 בכיכר המדינה: 0% בחתימה, בבניין בוטיק של 7 קומות. 5 חדרים מ-7.65 מיליון שקל.', 'שווה לשאול מתי משלמים את היתרה, ואם היא צמודה.' ),
			'east'         => array( 'EAST&TLV בתל אביב: חצי מהמחיר עכשיו, והיתרה בעוד שנתיים, עם בחירה של מסלול התשלום ומועד הכניסה.', 'שווה לבדוק אם היתרה צמודה למדד עד אז.' ),
			'kata'         => array( 'TRIO בעין גנים, פתח תקווה, של קטה: שלוש שנים בלי דמי ניהול, בשווי של כ-25 אלף שקל לדירה.', 'שווה לבדוק מה כלול בדמי הניהול, ומה המחיר בלי המבצע.' ),
			'sharet'       => array( 'שרת 38 בתל אביב: דירת 4 חדרים, 102 מטר, מרוהטת ומעוצבת, עם מרפסת, ממ"ד וחניה. 6.66 מיליון שקל.', 'שווה לבקש רשימה של מה שכלול בריהוט.' ),
			'rayk'         => array( 'RAYK בלוד החדשה: בדירת 4 חדרים משלמים 215 אלף שקל, והיתרה באכלוס, עם הלוואת קבלן מסובסדת. יש גם הטבות ללוחמים.', 'האכלוס צפוי ביוני 2029. שווה אישור עקרוני למשכנתא מראש, ולבדוק את ההצמדה.' ),
			'tzahala'      => array( 'רמות צהלה בתל אביב, של דנקנר קנלוב: דירת 6 חדרים אחרונה, במחיר פריסייל של 7.65 מיליון שקל.', 'מחיר פריסייל לא אומר כמה הנחה יש. שווה להשוות לעסקאות באזור.' ),
			'isa'          => array( 'ISA במבשרת ציון: שוכרים דירה גמורה, וחלק משכר הדירה, לפעמים כולו, נזקף כהון עצמי אם קונים בסוף התקופה.', 'מחיר לא פורסם. שווה לבדוק בחוזה כמה מהשכירות נזקף, ועד מתי.' ),
		);
	}
}

if ( ! function_exists( 'nadlan_dg_lines' ) ) {
	/** Every line she can say: id => text. Fixed text, so each one can be recorded once and checked. */
	function nadlan_dg_lines() {
		$deals = function_exists( 'nadlan_dm_deals' ) ? nadlan_dm_deals() : array();
		$n     = count( $deals );
		$num   = array( 'אף', 'אחד', 'שני', 'שלושה', 'ארבעה', 'חמישה', 'שישה', 'שבעה', 'שמונה', 'תשעה', 'עשרה', 'אחד עשר', 'שנים עשר', 'שלושה עשר', 'ארבעה עשר', 'חמישה עשר', 'שישה עשר', 'שבעה עשר', 'שמונה עשר', 'תשעה עשר', 'עשרים' );
		$L     = array(
			'greet'   => 'שלום. אני מכירה את ' . ( $num[ $n ] ?? $n ) . ' המבצעים שעל המפה, ומה שפורסם בכל אחד. הזיזו את הסכום שיש לכם ביד, ואראה לכם מה פתוח.',
			'hello'   => 'אני כאן. לחצו על מבצע במפה, או שאלו אותי על מבצעי קבלנים.',
			'nr'      => 'אני לא ממליצה על מבצע מסוים, וזה לא ייעוץ.',
			'ret0'    => 'טוב שחזרתם. מאז הביקור הקודם לא נוסף מבצע חדש, והמפה מעודכנת.',
			'idle'    => 'אפשר להשאיר במפה רק מבצעים של תשלום מדורג, כמו 20/80. לחצו, ואני אסנן.',
			'calc'    => 'כאן מחשבים כמה שווה מבצע באמת: הכסף שנשאר אצלכם עד המפתח, ההצמדה שנחסכה, והטבות. בחרו מבצע, וזה מתמלא לבד.',
			'alert'   => 'אפשר לקבל מייל רק כשנכנס מבצע חדש באזור שבחרתם. מייל אחד לאישור, וביטול בלחיצה.',
			'unknown' => 'על זה אין לי תשובה בדוקה. השאירו שם ונייד, ונחזור אליכם עם תשובה.',
			'who'     => 'אני דמות ממוחשבת של נדלן. אני מכירה את המבצעים שעל המפה ואת מה שפורסם בהם. אני לא מתווכת, ולא ממליצה על מבצע.',
			'best'    => 'אני לא ממליצה על מבצע מסוים. מה שמתאים תלוי בכמה יש לכם ביד, ומתי תצטרכו את השאר. הזיזו את הסכום, ואראה מה פתוח.',
			'q2080'   => 'ב-20/80 משלמים 20 אחוז בחתימה, ואת השאר במסירה. הכסף נשאר אצלכם עד המפתח. שווה לבדוק אם המחיר גבוה יותר מבתשלום רגיל, ואם היתרה צמודה.',
			'qzero'   => 'הדלקתי במפה את המבצעים שבהם לא משלמים בחתימה, או משלמים 0% הון עצמי עד המסירה.',
			'qtrue'   => 'מבצע הוא לא תמיד הנחה. ההנחה האמיתית היא כמה שווה הכסף שנשאר אצלכם, פחות תוספת למחיר אם יש. פתחתי לכם את המחשבון.',
			'qloan'   => 'הלוואת קבלן היא כסף שהיזם מממן במקומכם לתקופה, כדי שתשלמו פחות עכשיו. שווה לקבל בכתב מתי מחזירים, ומי משלם את הריבית.',
			'qindex'  => 'עד המסירה, חלק מכל תשלום צמוד בדרך כלל למדד תשומות הבנייה. בחלק מהמבצעים יש פטור. שווה לראות את זה בחוזה עצמו.',
			'qbank'   => 'הבנק בודק הכנסה והון עצמי. כשמשלמים מעט בחתימה, את רוב הכסף צריך במסירה, ולכן שווה אישור עקרוני מראש. יועץ משכנתאות יכול לעזור, בחינם.',
			'qvalid'  => 'כל מבצע מסומן מתי פורסם ומתי בדקנו. מבצעים משתנים מהר, ולכן לפני החלטה שווה לבדוק מול היזם. השאירו פרטים, ונבדוק בשבילכם.',
			'qrent'   => 'יש מבצעים שבהם היזם משלם הטבה חודשית או שכר דירה עד האכלוס. הדלקתי אותם במפה.',
			'near0'   => 'לא מצאתי מבצע על המפה באזור הזה. אפשר לבקש התראה, ותדעו כשיהיה.',
			'bye'     => 'סגרתי. אם תרצו, אני כאן בפינה.',
		);
		for ( $i = 0; $i <= $n; $i++ ) {
			$L[ 'cash' . $i ] = 0 === $i ? 'עם הסכום שבחרתם עוד לא נפתח מבצע עם סכום שפורסם. נסו להזיז קצת למעלה.' : ( 1 === $i ? 'עם הסכום שבחרתם נפתח מבצע אחד. הדלקתי אותו במפה.' : 'עם הסכום שבחרתם נפתחים ' . ( $num[ $i ] ?? $i ) . ' מבצעים. הדלקתי אותם במפה.' );
		}
		for ( $i = 1; $i <= min( 8, $n ); $i++ ) {
			$L[ 'near' . $i ] = 1 === $i ? 'יש מבצע אחד באזור הזה. הראיתי אותו במפה.' : 'יש ' . $num[ $i ] . ' מבצעים באזור הזה. הדלקתי אותם במפה.';
			$L[ 'ret' . $i ]  = 1 === $i ? 'טוב שחזרתם. מאז הביקור הקודם נוסף מבצע חדש אחד. הדלקתי אותו במפה.' : 'טוב שחזרתם. מאז הביקור הקודם נוספו ' . $num[ $i ] . ' מבצעים חדשים. הדלקתי אותם במפה.';
		}
		foreach ( nadlan_dg_deal_lines() as $id => $two ) {
			$L[ 'd-' . $id ] = $two[0];
			$L[ 'c-' . $id ] = $two[1];
		}
		return $L;
	}
}

if ( ! function_exists( 'nadlan_dg_payload' ) ) {
	function nadlan_dg_payload() {
		$clips = get_option( 'nadlan_dg_clips', array() );
		$clips = is_array( $clips ) ? $clips : array();
		$base  = home_url( '/wp-content/uploads/' );
		$out   = array();
		foreach ( nadlan_dg_lines() as $id => $text ) {
			$c = $clips[ $id ] ?? null; // array( 'f' => 'nadlan-guide/xx.mp3', 'h' => md5 prefix of the text it says )
			$ok = is_array( $c ) && ! empty( $c['f'] ) && ( $c['h'] ?? '' ) === substr( md5( $text ), 0, 8 );
			$out[ $id ] = $ok ? array( $text, $base . ltrim( (string) $c['f'], '/' ) ) : array( $text );
		}
		$up = home_url( '/wp-content/uploads/2026/11/' );
		return array(
			'lines' => $out,
			'face'  => array( $up . 'nlagent-face-v1.webp', $up . 'nlagent-mouth-b-v1.webp', $up . 'nlagent-mouth-c-v1.webp', $up . 'nlagent-blink-v1.webp' ),
			'wa'    => preg_replace( '/\D+/', '', (string) get_option( 'nadlan_whatsapp_e164', '972525101555' ) ),
			'lead'  => home_url( '/wp-json/nadlan/v1/lead' ),
			/* the site's lead consent line (the advisor's, inc/expert-advisor.php), §11 at the form */
			'consent' => 'מסירת הפרטים היא לפי רצונכם, ובלי פרטים לא נוכל לחזור אליכם. הפרטים, והמבצע שעליו שאלתם, נשמרים אצל נדל״ן רק כדי לחזור אליכם בעניין שביקשתם, ולא יועברו ליזם, למתווך או לכל גורם אחר בלי שתבקשו. לעיון בפרטים, לתיקון או למחיקה: info@nad-lan.co.il',
			'cities' => array( 'תל אביב' => array( 32.08, 34.79 ), 'רמת גן' => array( 32.07, 34.82 ), 'גבעתיים' => array( 32.07, 34.81 ), 'הרצליה' => array( 32.16, 34.81 ), 'פתח תקווה' => array( 32.09, 34.88 ), 'ראשון לציון' => array( 31.97, 34.79 ), 'לוד' => array( 31.95, 34.89 ), 'אור יהודה' => array( 32.03, 34.85 ), 'כפר אז"ר' => array( 32.06, 34.86 ), 'נתניה' => array( 32.32, 34.86 ), 'ירושלים' => array( 31.77, 35.21 ), 'מבשרת ציון' => array( 31.80, 35.15 ), 'נוף הגליל' => array( 32.70, 35.32 ), 'חיפה' => array( 32.79, 34.99 ), 'באר שבע' => array( 31.25, 34.79 ) ),
		);
	}
}

add_action( 'wp_enqueue_scripts', function () {
	if ( ! nadlan_dg_on() ) { return; }
	$base = plugins_url( 'assets/deals/', dirname( __FILE__ ) );
	$dir  = dirname( __DIR__ ) . '/assets/deals/';
	wp_enqueue_style( 'nadlan-deals-guide', $base . 'guide.css', array(), (string) @filemtime( $dir . 'guide.css' ) );
	wp_enqueue_script( 'nadlan-deals-guide', $base . 'guide.js', array( 'nadlan-deals-map' ), (string) @filemtime( $dir . 'guide.js' ), true );
	wp_add_inline_script( 'nadlan-deals-guide', 'window.NLDG=' . wp_json_encode( nadlan_dg_payload(), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . ';', 'before' );
}, 20 );
